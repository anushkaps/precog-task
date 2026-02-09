"""Standardized task output saving utilities"""
from __future__ import annotations
from pathlib import Path
from .task_utils import get_task_dir, get_task_figures_dir
from .io import save_json, save_fig

def save_task_outputs(task_num: int, figures=None, metrics=None, summary=None, subfolder=None):
    """
    Standardized function to save task outputs to outputs/task{task_num}/
    
    Args:
        task_num: Task number (0-6)
        figures: Dict of {filename: matplotlib figure} or list of (filename, figure) tuples
        metrics: Dict to save as metrics.json
        summary: String or dict to save as summary.md (if string, saved as-is; if dict, formatted)
        subfolder: Optional subfolder within figures/ (e.g., 'training', 'evaluation')
    
    Returns:
        Dict with paths to saved files
    """
    task_dir = get_task_dir(task_num)
    saved_paths = {}
    
    # Save figures
    if figures is not None:
        fig_dir = get_task_figures_dir(task_num)
        if subfolder:
            fig_dir = fig_dir / subfolder
            fig_dir.mkdir(parents=True, exist_ok=True)
        
        if isinstance(figures, dict):
            fig_items = figures.items()
        elif isinstance(figures, list):
            fig_items = figures
        else:
            raise ValueError("figures must be dict or list of (filename, figure) tuples")
        
        for item in fig_items:
            if isinstance(item, tuple):
                filename, fig = item
            else:
                filename, fig = item
            # Ensure .png extension
            if not filename.endswith('.png'):
                filename += '.png'
            fig_path = fig_dir / filename
            save_fig(fig_path, fig=fig, close=False)
            saved_paths[f'figure_{filename}'] = str(fig_path)
    
    # Save metrics
    if metrics is not None:
        metrics_path = task_dir / 'metrics.json'
        save_json(metrics, metrics_path)
        saved_paths['metrics'] = str(metrics_path)
    
    # Save summary
    if summary is not None:
        summary_path = task_dir / 'summary.md'
        if isinstance(summary, dict):
            # Format dict as markdown
            lines = [f"# Task {task_num}: {summary.get('title', 'Summary')}\n"]
            if 'description' in summary:
                lines.append(f"\n## Description\n\n{summary['description']}\n")
            if 'findings' in summary:
                lines.append("\n## Key Findings\n")
                for finding in summary['findings']:
                    lines.append(f"- {finding}\n")
            if 'results' in summary:
                lines.append("\n## Results\n")
                for key, value in summary['results'].items():
                    lines.append(f"- **{key}**: {value}\n")
            if 'visualizations' in summary:
                lines.append("\n## Visualizations\n")
                for viz in summary['visualizations']:
                    lines.append(f"- `{viz}`: [description]\n")
            if 'insights' in summary:
                lines.append("\n## Key Insights\n\n")
                lines.append(summary['insights'] + "\n")
            summary_text = "".join(lines)
        else:
            summary_text = str(summary)
        
        summary_path.write_text(summary_text, encoding='utf-8')
        saved_paths['summary'] = str(summary_path)
    
    return saved_paths

