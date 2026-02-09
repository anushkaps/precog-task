# Running Notebook on Modal GPU

This guide explains how to run your notebook experiments on Modal's GPU infrastructure.

## Setup

1. **Install Modal:**
   ```bash
   pip install modal
   python3 -m modal setup
   ```
   This will open a browser to authenticate and create an API token.

2. **Verify installation:**
   ```bash
   modal --version
   ```

## Running the Notebook

### Option 1: Run All Tasks
```bash
modal run modal_notebook_runner.py
```

### Option 2: Run Specific Task
```bash
# Run only Task 1 (training biased model)
modal run modal_notebook_runner.py --task task1

# Run only Task 4 (robust models)
modal run modal_notebook_runner.py --task task4
```

### Option 3: Use Cheaper GPU (T4 instead of A10G)
```bash
modal run modal_notebook_runner.py --gpu-type T4
```

## GPU Options

- **T4**: Cheaper, good for smaller models (~$0.40/hour)
- **A10G**: Default, good balance (~$1.10/hour)
- **A100**: Fastest, for large models (~$3.50/hour)

To change GPU type, edit `modal_notebook_runner.py` and change:
```python
gpu=modal.gpu.A10G()  # Change to T4() or A100()
```

## Outputs

All outputs are saved to a Modal volume that persists between runs:
- Checkpoints: `/root/outputs/task*/checkpoints/`
- Metrics: `/root/outputs/task*/metrics.json`
- Figures: `/root/outputs/task*/figures/`

### Downloading Outputs

After running, download outputs to your local machine:
```bash
# Download all outputs
modal volume download lazy-artist-outputs ./outputs

# Or download specific task
modal volume download lazy-artist-outputs ./outputs --path task1
```

## Monitoring

View logs in real-time:
```bash
modal app logs lazy-artist-notebook
```

## Cost Estimation

- **Task 1** (5 epochs): ~5-10 minutes = ~$0.10-0.20
- **Task 4** (15 epochs, multiple models): ~30-60 minutes = ~$0.50-1.10
- **Full notebook**: ~2-3 hours = ~$2-3

## Troubleshooting

### Out of Memory
Increase memory in the function:
```python
memory=32768,  # 32GB instead of 16GB
```

### Timeout
Increase timeout:
```python
timeout=14400,  # 4 hours instead of 2
```

### Import Errors
Make sure all dependencies are in the `image` definition in `modal_notebook_runner.py`.

## Tips

1. **Start with Task 1** to test the setup:
   ```bash
   modal run modal_notebook_runner.py --task task1
   ```

2. **Use T4 GPU** for testing (cheaper):
   ```bash
   modal run modal_notebook_runner.py --task task1 --gpu-type T4
   ```

3. **Check outputs** before running full notebook:
   ```bash
   modal volume download lazy-artist-outputs ./outputs --path task1
   ```

4. **Monitor costs** in Modal dashboard: https://modal.com/apps

