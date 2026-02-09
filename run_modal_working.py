"""
Working Modal script to run notebook on GPU.
This version includes your project files in the image.

Usage: modal run run_modal_working.py
"""

import modal

app = modal.App("lazy-artist-notebook")

# Create image with dependencies AND your project files
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "numpy",
        "pillow",
        "matplotlib",
        "torch",
        "torchvision",
        "nbformat",
    )
    .apt_install("git")
    # Copy your project files into the image
    .copy_local_file("notebooks/01_experiments_checkpointed.ipynb", "/root/notebook.ipynb")
    .copy_local_file("src/utils/__init__.py", "/root/src/utils/__init__.py")
    .copy_local_file("src/utils/task_utils.py", "/root/src/utils/task_utils.py")
    .copy_local_file("src/utils/checkpoint.py", "/root/src/utils/checkpoint.py")
    .copy_local_file("src/utils/io.py", "/root/src/utils/io.py")
    .copy_local_file("src/utils/outputs.py", "/root/src/utils/outputs.py")
    .run_commands("mkdir -p /root/src/utils /root/notebooks")
)

# Create volume for outputs
volume = modal.Volume.from_name("lazy-artist-outputs", create_if_missing=True)


@app.function(
    image=image,
    gpu=modal.gpu.T4(),  # Using T4 for testing (cheaper), change to A10G() for production
    volumes={"/outputs": volume},
    timeout=3600,
    memory=16384,
)
def run_notebook(task: str = None):
    """Run the notebook on GPU."""
    import sys
    from pathlib import Path
    import torch
    import json
    import nbformat
    from nbconvert import PythonExporter
    
    print("="*60)
    print("Running on Modal GPU")
    print("="*60)
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    print("="*60)
    
    # Set up paths
    project_root = Path("/root")
    sys.path.insert(0, str(project_root))
    
    # Set up output directory
    output_dir = Path("/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read notebook
    notebook_path = project_root / "notebook.ipynb"
    if not notebook_path.exists():
        return {"error": f"Notebook not found at {notebook_path}"}
    
    print(f"\nReading notebook: {notebook_path}")
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Set up environment
    import numpy as np
    import random
    
    # Set device to GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Set seed
    SEED = 0
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
    
    # Import utilities
    from src.utils import task_utils
    task_utils.OUTPUT_ROOT = output_dir
    
    # Execute notebook cells
    executed = 0
    errors = []
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != 'code':
            continue
        
        source = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
        
        if not source.strip():
            continue
        
        # Filter by task if specified
        if task and task.lower() not in source.lower():
            continue
        
        try:
            print(f"\n[{i+1}] Executing cell...")
            exec(source, globals())
            executed += 1
        except Exception as e:
            error_msg = f"Cell {i+1}: {str(e)}"
            print(f"ERROR: {error_msg}")
            errors.append(error_msg)
            # Continue with next cell
            continue
    
    # Commit volume
    volume.commit()
    
    return {
        "status": "completed",
        "executed": executed,
        "errors": len(errors),
        "outputs": str(output_dir)
    }


@app.local_entrypoint()
def main(task: str = None):
    """Run the notebook."""
    print("Starting Modal run...")
    result = run_notebook.remote(task=task)
    print("\n" + "="*60)
    print("Results:")
    print("="*60)
    print(result)
    print("\nTo download outputs:")
    print("  modal volume download lazy-artist-outputs ./outputs")

