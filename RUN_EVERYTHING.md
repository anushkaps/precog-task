# How to Run Everything on Modal GPU

## Quick Start

### Run All Tasks
```bash
modal run run_modal_final.py
```

### Run Specific Task
```bash
modal run run_modal_final.py --task task1
modal run run_modal_final.py --task task4
```

## Periodic Saves

The script automatically saves outputs:
- ✅ **Every 5 cells** - Regular checkpoints
- ✅ **After each task** - When task completion is detected
- ✅ **On errors** - Saves partial outputs even if something fails
- ✅ **At the end** - Final commit

**Your outputs are safe!** Even if the script times out, everything up to the last checkpoint is saved.

## Download Outputs

After running (or during, if you want to check progress):

```bash
# Download everything from Modal volume to local ./outputs
modal volume get lazy-artist-outputs / ./outputs
```

## Monitor Progress

You can check what's been saved without downloading:

```bash
# List files in the volume
modal volume ls lazy-artist-outputs
```

## Timeout Settings

Current timeout: **4 hours** (14400 seconds)

If you need longer:
1. Edit `run_modal_final.py`
2. Change `timeout=14400` to a higher value (e.g., `timeout=21600` for 6 hours)

## GPU Options

Current: **T4** (cheaper, good for testing)

To use A10G (faster, more expensive):
- Edit `run_modal_final.py`
- Change `gpu="T4"` to `gpu="A10G"`

## What Gets Saved

All outputs from your notebook:
- ✅ Task 0: Dataset artifacts
- ✅ Task 1: Model checkpoints, metrics, confusion matrices
- ✅ Task 2: Neuron visualizations
- ✅ Task 3: Grad-CAM heatmaps
- ✅ Task 4: Robust model checkpoints and metrics
- ✅ Task 5: Adversarial attack results
- ✅ Task 6: SAE decompositions

## Troubleshooting

**Volume is empty?**
- The script hasn't run yet, or it failed before first checkpoint
- Run the script first: `modal run run_modal_final.py`

**Timeout error?**
- Increase timeout in `run_modal_final.py`
- Or run tasks separately: `modal run run_modal_final.py --task task1`

**Can't download?**
- Make sure the script has run at least once
- Check volume exists: `modal volume list`
- Try: `modal volume get lazy-artist-outputs / ./outputs`

