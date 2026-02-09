"""
Final working Modal script - properly includes project files.
Usage: modal run run_modal_final.py
"""

import modal

app = modal.App("lazy-artist-notebook")

# Create image with project files included
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "numpy",
        "pillow",
        "matplotlib",
        "torch",
        "torchvision",
        "nbformat",
        "nbconvert",
    )
    .apt_install("git")
    .add_local_dir("src", "/root/src")  # Add src directory
    .add_local_file("notebooks/01_experiments_checkpointed.ipynb", "/root/notebook.ipynb")  # Add notebook
)

# Create volume for outputs
volume = modal.Volume.from_name("lazy-artist-outputs", create_if_missing=True)


@app.function(
    image=image,
    gpu="T4",  # Using T4 for testing (cheaper), change to "A10G" for production
    volumes={"/root/outputs": volume},  # Mount at /root/outputs to match notebook's expected path
    timeout=14400,  # 4 hours - Task 5 needs more time for adversarial attacks
    memory=16384,
)
def run_notebook(task: str = None):
    """Run the notebook on GPU."""
    import sys
    from pathlib import Path
    import torch
    import json
    import nbformat
    
    print("="*60)
    print("Running on Modal GPU")
    print("="*60)
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    print("="*60)
    
    # Set up paths
    project_root = Path("/root")
    sys.path.insert(0, str(project_root))
    
    # Set up output directory - notebook will set this to /root/outputs
    output_dir = Path("/root/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Import and configure utilities - notebook will override this, but set it anyway
    from src.utils import task_utils
    task_utils.OUTPUT_ROOT = output_dir
    
    # Read notebook
    notebook_path = project_root / "notebook.ipynb"
    print(f"\nReading notebook: {notebook_path}")
    
    if not notebook_path.exists():
        return {"error": f"Notebook not found at {notebook_path}"}
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Set up environment
    import numpy as np
    import random
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    SEED = 0
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
    
    # Execute cells
    executed = 0
    errors = []
    last_commit_cell = 0
    
    def commit_volume(reason=""):
        """Helper to commit volume with logging."""
        print(f"\n[Checkpoint] Committing volume{reason}...")
        volume.commit()
        print("[OK] Volume committed")
    
    # If task filter is specified, find task boundaries
    task_start_idx = None
    task_end_idx = None
    if task:
        task_lower = task.lower()
        task_num = None
        if 'task5' in task_lower or 'task 5' in task_lower:
            task_num = 5
        elif 'task6' in task_lower or 'task 6' in task_lower:
            task_num = 6
        
        # Find where the task starts
        for i, cell in enumerate(nb.cells):
            if cell.cell_type != 'code':
                continue
            source = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
            # Look for task markers
            if task_num and f'task{task_num}' in source.lower():
                task_start_idx = i
                # Find where next task starts (or end of notebook)
                for j in range(i+1, len(nb.cells)):
                    if nb.cells[j].cell_type != 'code':
                        continue
                    next_source = ''.join(nb.cells[j].source) if isinstance(nb.cells[j].source, list) else nb.cells[j].source
                    if task_num < 6 and f'task{task_num+1}' in next_source.lower():
                        task_end_idx = j
                        break
                if task_end_idx is None:
                    task_end_idx = len(nb.cells)  # Run to end
                break
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != 'code':
            continue
        
        source = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
        
        if not source.strip():
            continue
        
        # If task filter specified: run all setup cells, then task-specific cells
        if task and task_start_idx is not None:
            # Run setup cells (before task) - these will use existing checkpoints
            if i < task_start_idx:
                # Run setup but notebook will skip if checkpoints exist
                pass  # Continue to execute
            # Run task cells
            elif i >= task_start_idx and (task_end_idx is None or i < task_end_idx):
                pass  # Continue to execute
            else:
                # After task, skip
                continue
        elif task and task_start_idx is None:
            # Task not found, skip this cell
            continue
        
        try:
            print(f"\n[Cell {i+1}] Executing...")
            exec(source, globals())
            executed += 1
            
            # Commit volume periodically (every 5 cells)
            if executed - last_commit_cell >= 5:
                commit_volume(f" after {executed} cells")
                last_commit_cell = executed
            
            # Also commit after task completion markers
            source_lower = source.lower()
            if any(marker in source_lower for marker in ["[task", "task1", "task2", "task3", "task4", "task5", "task6"]):
                # Check if this looks like end of a task (contains completion markers)
                if any(marker in source_lower for marker in ["done", "completed", "finished", "summary"]):
                    commit_volume(" (task completion detected)")
                    last_commit_cell = executed
                    
        except Exception as e:
            error_msg = f"Cell {i+1}: {str(e)}"
            print(f"ERROR: {error_msg}")
            errors.append(error_msg)
            # Commit even on error to save partial outputs
            commit_volume(" (error checkpoint)")
            continue
    
    # Final commit
    commit_volume(" (final)")
    
    print(f"\nCompleted: {executed} cells executed, {len(errors)} errors")
    
    return {
        "status": "completed",
        "executed": executed,
        "errors": len(errors),
        "outputs": str(output_dir),
        "volume_mount": "/root/outputs"
    }


@app.local_entrypoint()
def main(task: str = None):
    """Run the notebook."""
    print("Starting Modal GPU run...")
    
    # If no task specified, run tasks 5 and 6
    if task is None:
        tasks_to_run = ["task5", "task6"]
    elif task.lower() in ["task5", "task 5", "5"]:
        tasks_to_run = ["task5"]
    elif task.lower() in ["task6", "task 6", "6"]:
        tasks_to_run = ["task6"]
    elif task.lower() in ["task56", "tasks56", "5and6", "5 and 6"]:
        tasks_to_run = ["task5", "task6"]
    else:
        tasks_to_run = [task]
    
    all_results = []
    for t in tasks_to_run:
        print(f"\n{'='*60}")
        print(f"Running {t.upper()}")
        print(f"{'='*60}")
        result = run_notebook.remote(task=t)
        all_results.append((t, result))
        print(f"\n{t.upper()} completed:")
        print(result)
    
    print("\n" + "="*60)
    print("All Results Summary:")
    print("="*60)
    for t, result in all_results:
        print(f"{t}: {result.get('status', 'unknown')} - {result.get('executed', 0)} cells, {result.get('errors', 0)} errors")
    
    print("\nTo download outputs:")
    print("  modal volume get lazy-artist-outputs ./outputs")
