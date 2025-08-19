# 1. Pre-setting
### 1. Download the repository

```{shell}
download it at the top right of the site
```

### 2. Creating conda envs

```{shell}
conda create -n tor_analysis python=3.12
conda activate tor_analysis
```

### 3. Install requirements 

```{shell}
pip install -r requirements.txt
```

# 2. How to run

### 1.Experiment 1 (EX1): Impact of Geographical Variation on WF Accuracy
```{shell}
cd EX1
```
[1] Baseline: Same-location Training and Testing (table 2)
```{shell}
./same_location.sh
cat ../results/same_location.txt
```
[2] Cross-location Testing: Train on One Location, Test on Another. (table 3)
```{shell}
./cross_location.sh
cat ../results/cross_location.txt
```
[3] Mixed-location Training: Train on Multiple Locations, Test on One (table 4)
```{shell}
./mixed_location.sh
cat ../results/mixed_location.txt
```

*Experiment 2 (EX2): Temporal Drift and Its Effect on Model Performance* 
* `cross_time` experiment
* `reverse_cross_time` experiment
* `accumulate_robustness_with_mixed_data` experiment

*Experiment 3 (EX3): Reexaming Partial-Trace Detection-is 30\% Really Enough?*
* `accuracy_vs_traffic_percentage` experiment


### 4. Implement 
```{shell}
cd EX1
./same_location.sh
```

### 5. Results 
```{shell}
cd results
cd EX1
vi same_location.txt
```
