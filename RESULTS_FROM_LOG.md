# Results Extracted from Execution Log

## ✅ All Tasks Completed Successfully

### Task 1 - Biased Model
- **Easy Train Acc:** 95.74%
- **Easy Val Acc:** 95.98%
- **Hard Test Acc:** 15.77% ✅ (Goal: <20% - ACHIEVED!)
- **Epochs:** 4 (stopped early)
- **Best Hard:** 0.1580

### Task 2 - Neuron Visualization
- ✅ All channel visualizations generated
- ✅ One-proto sheet created
- ✅ One-color overview created
- ✅ 89+ figure files created

### Task 3 - Grad-CAM
- ✅ Grad-CAM implemented from scratch
- ✅ Biased vs conflicting examples analyzed

### Task 4 - Robust Models

**DANN Twostep:**
- HardTest: **75.43%** ✅ (Goal: >70%)
- Metrics saved to: `task4/metrics_dann_twostep.csv`

**Saliency Chroma Masked:**
- HardTest: **78.63%** ✅ (Goal: >70%)
- Metrics saved to: `task4/metrics_sal_chroma_masked.csv`

**CF Invar (BEST!):**
- HardTest: **96.78%** ✅✅ (Goal: >70% - EXCEEDED!)
- Metrics saved to: `task4/metrics.json`

### Task 5 - Adversarial Attacks
**All 20 samples processed:**

Success Rates:
- Baseline (biased): 20% success, median eps=0.0457
- DANN Twostep: 50% success, median eps=0.0460
- **CF Invar: 60% success, median eps=0.0421** (most robust!)
- Saliency Chroma Masked: 40% success, median eps=0.0393

### Task 6 - SAE Decomposition
- ✅ All layer combinations trained
- ✅ Color-selective features identified
- ✅ Digit-selective features identified
- ✅ Intervention demo completed

**Strongest Color-Selective Configs:**
1. gap/vector: top_color=0.974 (feat=358)
2. relu2/spatial_mean: top_color=0.972 (feat=126)
3. relu1/spatial_mean: top_color=0.971 (feat=45)

**Strongest Digit-Selective Configs:**
1. relu3/per_position: top_digit=0.500 (feat=51)
2. relu3/spatial_mean: top_digit=0.489 (feat=167)

## Key Achievements

1. ✅ **Task 1 Goal Met:** HardTest=15.77% (<20% target)
2. ✅ **Task 4 Goal Exceeded:** CF Invar achieved 96.78% (>70% target)
3. ✅ **Task 5 Complete:** All 20 adversarial samples processed
4. ✅ **Task 6 Complete:** SAE decomposition and interventions done

## Files That Were Created (But Lost)

All these files were created during execution but lost due to path mismatch:
- `outputs/task1/checkpoints/task1_lazy_best.pt`
- `outputs/task1/metrics.json`
- `outputs/task1/figures/confusion_matrix_hard.png`
- `outputs/task2/figures/*.png` (89+ files)
- `outputs/task4/checkpoints/*.pt` (all 3 models)
- `outputs/task4/metrics*.csv`
- `outputs/task5/*.csv`, `*.pt`, `*.png`
- `outputs/task6/*.pt`, `*.png`, `*.json`

## Fastest Recovery Option

If you need files, the fastest is to run just Task 4 (the most important):
```bash
modal run run_modal_final.py --task task4
```
This takes ~15-20 minutes and will save all Task 4 outputs correctly.

