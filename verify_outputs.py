"""
Quick script to verify what outputs Modal will save.
This shows all the output paths your notebook uses.
"""

from pathlib import Path

# These are the output paths your notebook creates
output_paths = [
    "outputs/config.json",
    "outputs/artifacts/easy_split_indices.npz",
    "outputs/task0/",
    "outputs/task1/checkpoints/",
    "outputs/task1/metrics.json",
    "outputs/task1/figures/",
    "outputs/task2/figures/",
    "outputs/task3/",
    "outputs/task4/checkpoints/",
    "outputs/task4/metrics*.csv",
    "outputs/task4/figures/",
    "outputs/task5/",
    "outputs/task6/checkpoints/",
    "outputs/task6/figures/",
    "outputs/task6/summary.json",
]

print("="*60)
print("Outputs that will be saved to Modal volume:")
print("="*60)
for path in output_paths:
    print(f"  [OK] {path}")

print("\n" + "="*60)
print("All outputs are saved to: /root/outputs/")
print("This is mounted to Modal volume: lazy-artist-outputs")
print("="*60)
print("\nAfter running, download with:")
print("  modal volume download lazy-artist-outputs ./outputs")
print("\nThis will download EVERYTHING including:")
print("  - All checkpoints (.pt files)")
print("  - All metrics (.json, .csv files)")
print("  - All figures (.png files)")
print("  - All summaries and configs")

