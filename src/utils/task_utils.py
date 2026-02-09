"""Task-based directory structure utilities"""
from __future__ import annotations
from pathlib import Path

# Output directory setup
OUTPUT_ROOT = Path('outputs')

def get_task_dir(task_num: int) -> Path:
    """Get task-specific output directory: outputs/task{task_num}/"""
    task_dir = OUTPUT_ROOT / f'task{task_num}'
    task_dir.mkdir(parents=True, exist_ok=True)
    return task_dir

def get_task_figures_dir(task_num: int) -> Path:
    """Get task-specific figures directory: outputs/task{task_num}/figures/"""
    fig_dir = get_task_dir(task_num) / 'figures'
    fig_dir.mkdir(parents=True, exist_ok=True)
    return fig_dir

def get_task_checkpoints_dir(task_num: int) -> Path:
    """Get task-specific checkpoints directory: outputs/task{task_num}/checkpoints/"""
    ckpt_dir = get_task_dir(task_num) / 'checkpoints'
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    return ckpt_dir

