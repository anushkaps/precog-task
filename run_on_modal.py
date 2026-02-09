"""
Modal app to run the notebook experiments on GPU.
Usage: modal run run_on_modal.py
"""

import modal

# Define the image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "numpy",
        "pillow",
        "matplotlib",
        "torch",
        "torchvision",
        "jupyter",
        "ipykernel",
    )
    .apt_install("git")
)

app = modal.App("lazy-artist-notebook", image=image)

# Mount the project directory
project_mount = modal.Mount.from_local_dir(".", remote_path="/root/project")

# Create a volume for outputs (persistent storage)
outputs_volume = modal.Volume.from_name("lazy-artist-outputs", create_if_missing=True)


@app.function(
    gpu=modal.gpu.A10G(),  # Use A10G GPU (or change to T4, A100, etc.)
    volumes={"/root/outputs": outputs_volume},
    mounts=[project_mount],
    timeout=3600,  # 1 hour timeout
    workdir="/root/project",
)
def run_notebook_task(task_name: str = "all"):
    """
    Run a specific task or all tasks from the notebook.
    
    Args:
        task_name: One of "task0", "task1", "task2", "task3", "task4", "task5", "task6", or "all"
    """
    import sys
    from pathlib import Path
    import torch
    import numpy as np
    import random
    
    # Set up paths
    project_root = Path("/root/project")
    sys.path.insert(0, str(project_root))
    
    # Set device to GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    # Import utilities
    from src.utils import (
        OUTPUT_ROOT,
        get_task_dir,
        get_task_figures_dir,
        get_task_checkpoints_dir,
        save_json,
        append_csv,
        save_fig,
        atomic_torch_save,
        load_checkpoint,
        save_checkpoint,
        save_best,
        save_task_outputs,
    )
    
    # Fix OUTPUT_ROOT to use mounted volume
    from src.utils import task_utils
    task_utils.OUTPUT_ROOT = Path("/root/outputs")
    OUTPUT_ROOT = Path("/root/outputs")
    OUTPUT_ROOT.mkdir(exist_ok=True)
    
    # Set seed for reproducibility
    SEED = 0
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    
    # Import notebook code
    import importlib.util
    
    # Load notebook code - we'll need to extract the Python code from notebook
    # For now, let's create a wrapper that imports the key functions
    
    # Configuration
    NUM_CLASSES = 10
    P_BIAS = 0.95
    BATCH_SIZE = 128
    EPOCHS = 5
    
    # Save config
    save_json({
        'device': device,
        'NUM_CLASSES': NUM_CLASSES,
        'P_BIAS': P_BIAS,
        'BATCH_SIZE': BATCH_SIZE,
        'EPOCHS': EPOCHS,
        'SEED': SEED,
    }, OUTPUT_ROOT / 'config.json')
    
    print(f"\n{'='*60}")
    print(f"Running {task_name} on Modal GPU")
    print(f"{'='*60}\n")
    
    # Import and run notebook code
    # This is a simplified version - you may want to extract specific cells
    exec(open(project_root / "notebooks" / "01_experiments_checkpointed.ipynb").read())
    
    # Commit volume changes
    outputs_volume.commit()
    
    return f"Task {task_name} completed successfully!"


@app.function(
    gpu=modal.gpu.A10G(),
    volumes={"/root/outputs": outputs_volume},
    mounts=[project_mount],
    timeout=3600,
    workdir="/root/project",
)
def run_task1_training():
    """Run Task 1 training specifically."""
    import sys
    from pathlib import Path
    import torch
    import numpy as np
    import random
    
    project_root = Path("/root/project")
    sys.path.insert(0, str(project_root))
    
    device = "cuda"
    print(f"Device: {device}")
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    # Import utilities
    from src.utils import (
        OUTPUT_ROOT,
        get_task_dir,
        get_task_figures_dir,
        get_task_checkpoints_dir,
        save_json,
        append_csv,
        save_fig,
        load_checkpoint,
        save_checkpoint,
        save_best,
    )
    
    from src.utils import task_utils
    task_utils.OUTPUT_ROOT = Path("/root/outputs")
    OUTPUT_ROOT = Path("/root/outputs")
    OUTPUT_ROOT.mkdir(exist_ok=True)
    
    # Set seed
    SEED = 0
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    
    # Now import and run your actual training code
    # You'll need to extract the relevant cells from your notebook
    # For now, this is a template
    
    outputs_volume.commit()
    return "Task 1 training completed!"


@app.local_entrypoint()
def main(task: str = "all"):
    """
    Main entrypoint to run tasks on Modal.
    
    Usage:
        modal run run_on_modal.py --task task1
        modal run run_on_modal.py --task all
    """
    if task == "all":
        result = run_notebook_task.remote("all")
    else:
        result = run_notebook_task.remote(task)
    
    print(result)

