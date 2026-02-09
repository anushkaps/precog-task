# Precog Recruitment Task 2026

This repository implements a comprehensive analysis of CNN bias, interpretability, and robustness through 7 interconnected tasks. The project demonstrates how CNNs can exploit spurious correlations (color-digit associations) and explores methods to train robust models that focus on shape rather than color.

## Repository Structure

```
notebook_repo_checkpointed_template/
│
├── README.md                          # This file - project documentation
├── requirements.txt                   # Python package dependencies
│
├── notebooks/                         # Main experiment notebook
│   ├── 01_experiments_checkpointed.ipynb  # Single notebook with all tasks (MANDATORY)
│   └── data/                          # MNIST dataset (auto-downloaded on first run)
│
├── outputs/                           # All experimental outputs (organized by task)
│   ├── config.json                    # Global configuration (device, hyperparameters)
│   ├── artifacts/                     # Shared artifacts (e.g., dataset splits)
│   ├── task0/                         # Dataset generation outputs
│   ├── task1/                         # Biased model training (checkpoints, figures, metrics)
│   ├── task2/                         # Neuron visualization outputs
│   ├── task3/                         # Grad-CAM implementation outputs
│   ├── task4/                         # Robust model training (DANN, Saliency, CF Invar)
│   ├── task5/                         # Adversarial attack results
│   └── task6/                         # Sparse Autoencoder outputs
│
└── src/                               # Utility modules (imported by notebook)
    └── utils/
        ├── task_utils.py              # Directory path utilities
        ├── checkpoint.py              # Model checkpoint save/load
        ├── io.py                      # File I/O (JSON, CSV, figures)
        └── outputs.py                # Standardized task output saving
```

### Important Folders

- **`notebooks/01_experiments_checkpointed.ipynb`**: Main notebook containing all 7 tasks (Task 0-6). This is the single source of truth for all experiments.
- **`outputs/`**: All experimental results organized by task. Each task folder contains:
  - `checkpoints/`: Model checkpoints (`.pt` files) for resuming training
  - `figures/`: Visualizations (PNG files)
  - `metrics.json`: Quantitative results
- **`src/utils/`**: Helper utility functions for path management, checkpointing, and file I/O operations.

## Prerequisites

- **Python 3.8+** (tested with Python 3.10)
- **pip** (Python package manager)
- **(Optional) CUDA-capable GPU** for faster training (CPU works but is slower)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd notebook_repo_checkpointed_template
   ```

2. **Create a virtual environment** (recommended)

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Commands to Run

### Option 1: VS Code (Recommended)

1. Install VS Code extensions: **Python** + **Jupyter**
2. Open `notebooks/01_experiments_checkpointed.ipynb`
3. Select the `.venv` interpreter (Ctrl+Shift+P → "Python: Select Interpreter")
4. Run All cells (or run cells sequentially)

### Option 2: Jupyter Notebook

```bash
# Activate virtual environment first
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows

# Launch Jupyter Notebook
jupyter notebook notebooks/01_experiments_checkpointed.ipynb
```

**Note**: The notebook is **restart-safe**. If execution is interrupted, restart the kernel and run all cells again. The notebook will automatically load checkpoints and skip completed work.

## Dependencies

All dependencies are listed in `requirements.txt`:

- **torch**, **torchvision**: Deep learning framework
- **numpy**: Numerical computations
- **matplotlib**: Plotting and visualization
- **pillow**: Image processing
- **jupyter**, **ipykernel**: Notebook environment

## Project Tasks

The notebook implements 7 sequential tasks:

- **Task 0: The Biased Canvas** - Generate Colored-MNIST dataset with spurious correlations
- **Task 1: The Cheater** - Train biased CNN that exploits color
- **Task 2: The Prober** - Visualize neuron activations
- **Task 3: The Interrogation** - Implement Grad-CAM
- **Task 4: The Intervention** - Train robust models (DANN, Saliency, CF Invar)
- **Task 5: The Invisible Cloak** - Adversarial attack evaluation
- **Task 6: The Decomposition** - Sparse Autoencoder analysis

## Notes

- The notebook is the **single source of truth** - all experiments run here
- Outputs are saved automatically to `outputs/taskX/` directories
- Training can be resumed from checkpoints if interrupted
- Fixed random seeds ensure reproducible results
