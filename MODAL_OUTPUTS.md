# Modal Outputs - What Gets Saved

## ✅ YES - All Outputs Are Saved and Downloadable

All outputs from your notebook are saved to the Modal volume and can be downloaded.

## What Gets Saved

### Task 0 (Dataset Generation)
- `outputs/config.json` - Global configuration
- `outputs/artifacts/easy_split_indices.npz` - Cached train/val split

### Task 1 (Biased Model Training)
- `outputs/task1/checkpoints/task1_lazy_best.pt` - Best model checkpoint
- `outputs/task1/checkpoints/task1_lazy_last.pt` - Last epoch checkpoint
- `outputs/task1/metrics.json` - Training metrics
- `outputs/task1/figures/confusion_matrix_hard.png` - Confusion matrix

### Task 2 (Neuron Visualization)
- `outputs/task2/figures/allchannels/*.png` - All channel visualizations
- `outputs/task2/figures/oneproto/*.png` - Prototype visualizations
- `outputs/task2/figures/onecolor/*.png` - Color visualizations
- `outputs/task2/metrics.json` - Task 2 metrics

### Task 3 (Grad-CAM)
- `outputs/task3/figures/*.png` - Grad-CAM heatmaps
- `outputs/task3/summary.md` - Task 3 summary

### Task 4 (Robust Models)
- `outputs/task4/checkpoints/task4_*.pt` - All model checkpoints
  - `task4_dann_twostep_best.pt`
  - `task4_cf_invar_best.pt`
  - `task4_sal_chroma_masked_best.pt`
- `outputs/task4/metrics*.csv` - Training metrics for each model
- `outputs/task4/figures/viz/*.png` - Comparison visualizations

### Task 5 (Adversarial Attacks)
- `outputs/task5/samples_shared_correct.pt` - Attack samples
- `outputs/task5/task5_results_per_sample.csv` - Per-sample results
- `outputs/task5/task5_summary.csv` - Summary statistics
- `outputs/task5/panels/*.png` - Attack visualizations
- `outputs/task5/plots/*.png` - Analysis plots

### Task 6 (SAE Decomposition)
- `outputs/task6/sae_checkpoints/*.pt` - SAE model checkpoints
- `outputs/task6/figures/*.png` - Selectivity plots
- `outputs/task6/summary.json` - SAE analysis summary
- `outputs/task6/metrics.json` - Training metrics

## How to Download

### Download Everything
```bash
modal volume download lazy-artist-outputs ./outputs
```

This downloads the entire `outputs/` directory to your local `./outputs/` folder.

### Download Specific Task
```bash
# Download only Task 1 outputs
modal volume download lazy-artist-outputs ./outputs --path task1

# Download only Task 4 outputs
modal volume download lazy-artist-outputs ./outputs --path task4
```

### List What's in Volume (Before Downloading)
```bash
modal run modal_notebook_runner.py --list-only
```

## Verification

The Modal script automatically:
1. ✅ Lists all created files before committing
2. ✅ Commits the volume to persist outputs
3. ✅ Reports total files created

You can verify outputs were saved by checking the logs or running:
```bash
modal run modal_notebook_runner.py --list-only
```

## Important Notes

- **All outputs persist** between runs (stored in Modal volume)
- **Checkpoints are large** (~50-100MB each) - download may take time
- **Volume persists** even if you delete the app
- **Free tier**: 5GB storage included, then $0.10/GB/month

## File Sizes (Approximate)

- Checkpoint files: ~50-100MB each
- Figure files: ~100KB-1MB each
- Metrics files: ~1-10KB each
- Total for full run: ~500MB-1GB

