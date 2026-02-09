"""
Modal script to run notebook on GPU.
This version assumes your code is in a git repository.

Usage:
    modal run run_modal.py
"""

import modal

app = modal.App("lazy-artist-notebook")

# Create image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "numpy",
        "pillow",
        "matplotlib", 
        "torch",
        "torchvision",
        "nbformat",
        "gitpython",
    )
    .apt_install("git")
)

# Create volume for persistent outputs
volume = modal.Volume.from_name("lazy-artist-outputs", create_if_missing=True)


@app.function(
    image=image,
    gpu=modal.gpu.A10G(),  # Change to T4() for cheaper option
    volumes={"/outputs": volume},
    timeout=7200,  # 2 hours
    memory=16384,  # 16GB
)
def run_notebook(git_url: str = None, task: str = None):
    """
    Run notebook on GPU.
    
    Args:
        git_url: Git repository URL (optional, can clone your repo)
        task: Task name to run (e.g., "task1")
    """
    import sys
    import subprocess
    from pathlib import Path
    import torch
    import json
    
    print("="*60)
    print("Running on Modal GPU")
    print("="*60)
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    print("="*60)
    
    # Set up paths
    project_dir = Path("/root/project")
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # If git_url provided, clone the repo
    if git_url:
        print(f"Cloning {git_url}...")
        subprocess.run(["git", "clone", git_url, str(project_dir)], check=True)
    else:
        # For now, you need to upload files manually or use Modal's file system
        print("Note: Files need to be uploaded. Using current directory structure.")
    
    sys.path.insert(0, str(project_dir))
    
    # Set up output directory
    output_dir = Path("/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Your notebook execution code would go here
    # This is a template - you'll need to add your actual notebook execution
    
    print("\nTask completed!")
    print(f"Outputs saved to: {output_dir}")
    
    # Commit volume to persist outputs
    volume.commit()
    
    return {
        "status": "success",
        "outputs": str(output_dir)
    }


@app.local_entrypoint()
def main(git_url: str = None, task: str = None):
    """
    Run the notebook.
    
    Usage:
        # If your code is in a git repo:
        modal run run_modal.py --git-url https://github.com/yourusername/yourrepo.git
        
        # Or run with task filter:
        modal run run_modal.py --task task1
    """
    result = run_notebook.remote(git_url=git_url, task=task)
    print("\nResults:")
    print(result)
    print("\nTo download outputs:")
    print("  modal volume download lazy-artist-outputs ./outputs")

