"""
Simple Modal script to run your notebook on GPU.
Usage: modal run run_modal_simple.py
"""

import modal

app = modal.App("lazy-artist")

# Create image with dependencies
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
)

# Create volume for outputs
volume = modal.Volume.from_name("lazy-artist-outputs", create_if_missing=True)


@app.function(
    image=image,
    gpu=modal.gpu.A10G(),
    volumes={"/outputs": volume},
    timeout=7200,
    secrets=[modal.Secret.from_name("my-secret")] if False else [],  # Add if needed
)
def run_task():
    """Run your notebook code on GPU."""
    import subprocess
    import sys
    from pathlib import Path
    
    # The notebook file needs to be available
    # Option 1: Upload via git
    # Option 2: Copy file into image
    # Option 3: Use Modal's file system
    
    print("="*60)
    print("Modal GPU Runner")
    print("="*60)
    
    # Set up output directory
    output_dir = Path("/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Your code would go here
    # For now, this is a template
    
    volume.commit()
    return "Task completed!"


if __name__ == "__main__":
    with app.run():
        result = run_task.remote()
        print(result)

