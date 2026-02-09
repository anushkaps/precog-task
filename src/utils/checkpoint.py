from __future__ import annotations
from pathlib import Path
import torch
from .task_utils import get_task_checkpoints_dir
from .io import atomic_torch_save

def load_checkpoint(task: str, model=None, optimizer=None, extra_keys=(), task_num=None):
    """Load checkpoint from task-specific directory"""
    if task_num is None:
        raise ValueError("task_num must be provided")
    ckpt_path = get_task_checkpoints_dir(task_num) / f'{task}_last.pt'
    
    if not ckpt_path.exists():
        return 0, {}
    ckpt = torch.load(ckpt_path, map_location='cpu')
    if model is not None and 'model' in ckpt:
        model.load_state_dict(ckpt['model'])
    if optimizer is not None and 'optim' in ckpt:
        optimizer.load_state_dict(ckpt['optim'])
    start_epoch = int(ckpt.get('epoch', -1)) + 1
    extra = {k: ckpt.get(k) for k in extra_keys}
    print(f'[resume] {task}: loaded {ckpt_path} -> start_epoch={start_epoch}')
    return start_epoch, extra

def save_checkpoint(task: str, epoch: int, model, optimizer=None, task_num=None, **extra):
    """Save checkpoint to task-specific directory"""
    if task_num is None:
        raise ValueError("task_num must be provided")
    payload = {'epoch': int(epoch), 'model': model.state_dict()}
    if optimizer is not None:
        payload['optim'] = optimizer.state_dict()
    payload.update(extra)
    ckpt_path = get_task_checkpoints_dir(task_num) / f'{task}_last.pt'
    atomic_torch_save(payload, ckpt_path)

def save_best(task: str, model, optimizer=None, task_num=None, **extra):
    """Save best checkpoint to task-specific directory"""
    if task_num is None:
        raise ValueError("task_num must be provided")
    payload = {'model': model.state_dict()}
    if optimizer is not None:
        payload['optim'] = optimizer.state_dict()
    payload.update(extra)
    ckpt_path = get_task_checkpoints_dir(task_num) / f'{task}_best.pt'
    atomic_torch_save(payload, ckpt_path)
