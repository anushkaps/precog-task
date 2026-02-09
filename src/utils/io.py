from __future__ import annotations
from pathlib import Path
import csv
import json
import os
import tempfile
import matplotlib.pyplot as plt
import torch

def atomic_write_bytes(dst: str | Path, data: bytes) -> None:
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(dst.parent), prefix=dst.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        Path(tmp).replace(dst)
    finally:
        # If replace failed, cleanup
        try:
            if Path(tmp).exists():
                Path(tmp).unlink()
        except Exception:
            pass

def atomic_write_text(dst: str | Path, text: str, encoding: str = "utf-8") -> None:
    atomic_write_bytes(dst, text.encode(encoding))

def save_json(obj, path: Path, indent: int = 2) -> None:
    """Save object as JSON file"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=indent, default=str)

def append_csv(path: Path, row: dict) -> None:
    """Append a row to a CSV file, creating header if file doesn't exist"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not exists:
            w.writeheader()
        w.writerow(row)

def save_fig(path: Path, fig=None, close: bool = True) -> None:
    """Save matplotlib figure to file
    
    Args:
        path: Path to save figure to
        fig: Figure object (optional, uses current figure if not provided)
        close: Whether to close the figure after saving
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    if fig is None:
        fig = plt.gcf()
    
    fig.savefig(path, dpi=200, bbox_inches='tight')
    if close:
        plt.close(fig)

def atomic_torch_save(obj, path: Path) -> None:
    """Atomically save PyTorch object"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    torch.save(obj, tmp)
    tmp.replace(path)

def append_csv_row(dst: str | Path, header: list[str], row: dict) -> None:
    """Legacy function - use append_csv instead"""
    append_csv(dst, row)
