# The Lazy Artist: CNN Bias Detection and Intervention

This repository implements a comprehensive analysis of CNN bias, interpretability, and robustness through 7 interconnected tasks. The project satisfies the submission requirement of a **mandatory notebook** that clearly logs all experiments and results.

## Repository Structure

```
notebook_repo_checkpointed_template/
│
├── README.md                    # This file - project overview and setup
├── requirements.txt             # Python dependencies
│
├── notebooks/
│   ├── 01_experiments_checkpointed.ipynb  # Main experiment notebook (MANDATORY)
│   └── data/                    # MNIST dataset (auto-downloaded)
│
├── outputs/                     # All task outputs (organized by task)
│   ├── task0/                   # Dataset generation
│   │   ├── figures/             # Visualizations
│   │   ├── metrics.json        # Quantitative results
│   │   └── summary.md           # Human-readable summary
│   ├── task1/                   # Biased model training
│   ├── task2/                   # Neuron visualization
│   ├── task3/                   # Grad-CAM implementation
│   ├── task4/                   # Robust model training
│   ├── task5/                   # Adversarial attacks
│   └── task6/                   # Sparse Autoencoders
│
├── src/                         # Optional helper utilities
│   └── utils/
│       ├── checkpoint.py        # Model checkpointing
│       ├── io.py                # I/O utilities
│       ├── outputs.py           # Task output saving
│       └── task_utils.py        # Task directory utilities
```

## Key Features

- **Single Notebook**: All experiments (Task 0-6) are logged in `notebooks/01_experiments_checkpointed.ipynb`
- **Task-Based Outputs**: Results organized in `outputs/taskX/` with standardized structure
- **Standardized Saving**: Use `save_task_outputs()` helper function for consistent output organization
- **Reproducible**: Seed setting, config saving, and checkpointing for full reproducibility
- **Resumable**: Training can be resumed from checkpoints if interrupted

## Setup

### Prerequisites

- Python 3.8+
- pip
- (Optional) CUDA-capable GPU for faster training

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd notebook_repo_checkpointed_template
   ```

2. **Create a virtual environment**

   Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Notebook

**Option 1: VS Code (Recommended)**
1. Install VS Code extensions: **Python** + **Jupyter**
2. Open `notebooks/01_experiments_checkpointed.ipynb`
3. Select the `.venv` interpreter (Ctrl+Shift+P → "Python: Select Interpreter")
4. Run All cells (or run cells sequentially)

**Option 2: Jupyter Notebook/Lab**
```bash
jupyter notebook notebooks/01_experiments_checkpointed.ipynb
# or
jupyter lab notebooks/01_experiments_checkpointed.ipynb
```

**Option 3: Command Line**
```bash
jupyter nbconvert --to notebook --execute notebooks/01_experiments_checkpointed.ipynb
```

## Project Tasks

The notebook implements 7 tasks:

- **Task 0: The Biased Canvas** - Generate Colored-MNIST dataset with spurious color-digit correlations
- **Task 1: The Cheater** - Train a CNN that exploits color bias (high train acc, low test acc)
- **Task 2: The Prober** - Visualize what individual neurons "see" through activation optimization
- **Task 3: The Interrogation** - Implement Grad-CAM from scratch to show where the model focuses
- **Task 4: The Intervention** - Train robust models that ignore color and focus on shape
- **Task 5: The Invisible Cloak** - Perform targeted adversarial attacks on robust models
- **Task 6: The Decomposition** - Train Sparse Autoencoders to decompose hidden states

## Output Organization

### Standardized Saving

Use the `save_task_outputs()` helper function for consistent output organization:

```python
# Example: Save Task 1 outputs
save_task_outputs(
    task_num=1,
    figures={
        'confusion_matrix': fig1,
        'training_curves': fig2
    },
    metrics={
        'train_acc': 0.95,
        'test_acc': 0.11
    },
    summary={
        'title': 'The Cheater',
        'description': 'Trained biased model that exploits color',
        'findings': ['Model achieves 95% train accuracy', 'Drops to 11% on hard test set'],
        'results': {'train_acc': '95.5%', 'test_acc': '11.4%'},
        'insights': 'Model learned color instead of digit shape'
    }
)
```

### Output Structure

Each task folder (`outputs/taskX/`) contains:
- `figures/` - All visualizations (PNG files)
- `metrics.json` - Quantitative results in JSON format
- `summary.md` - Human-readable summary of findings
- `checkpoints/` - Model checkpoints (if applicable)

## Reproducibility & Resumability

### Reproducibility
- Fixed random seeds for deterministic results
- Config files saved with hyperparameters
- All outputs saved with clear naming conventions

### Resumability
The notebook is designed to be restart-safe:
- Training checkpoints saved after each epoch
- Expensive computations cached in artifacts
- If kernel stops, restart and rerun; notebook will load checkpoints and continue

## Dependencies

See `requirements.txt` for full list. Key libraries:
- `torch`, `torchvision` - Deep learning framework
- `numpy` - Numerical computations
- `matplotlib` - Plotting and visualization
- `pillow` - Image processing
- `jupyter`, `ipykernel` - Notebook environment

## Methodology

This project follows a systematic approach:
1. **Create bias** - Synthetically generate biased dataset
2. **Demonstrate cheating** - Show model exploits bias
3. **Probe internals** - Visualize what neurons learn
4. **Interrogate** - Use Grad-CAM to show attention
5. **Intervene** - Train robust models with custom strategies
6. **Attack** - Test robustness with adversarial examples
7. **Decompose** - Use SAEs to understand representations

## Results Location

All results are organized in `outputs/taskX/`:
- **Figures**: `outputs/taskX/figures/`
- **Metrics**: `outputs/taskX/metrics.json`
- **Summaries**: `outputs/taskX/summary.md`

Each task's `summary.md` provides:
- What was done
- Key findings
- Results and metrics
- Visualizations with descriptions
- What worked / what didn't
- Key insights

## Notes

- The notebook is the **single source of truth** - all experiments run here
- Outputs are saved automatically using standardized paths
- Checkpoints allow resuming training if interrupted
- All code is self-contained in the notebook (helpers in `src/` are optional)
