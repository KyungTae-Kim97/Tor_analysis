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

### 1. Experiment 1 (EX1): Impact of Geographical Variation on WF Accuracy
```{shell}
cd EX1
```
[1] Baseline: Same-location Training and Testing (Table 2)
```{shell}
./same_location.sh
cat ../results/EX1/same_location.txt
```
[2] Cross-location Testing: Train on One Location, Test on Another. (Table 3)
```{shell}
./cross_location.sh
cat ../results/EX1/cross_location.txt
```
[3] Mixed-location Training: Train on Multiple Locations, Test on One (Table 4)
```{shell}
./mixed_location.sh
cat ../results/EX1/mixed_location.txt
```

### 2. Experiment 2 (EX2): Temporal Drift and Its Effect on Model Performance
```{shell}
cd EX2
```
[1] Cross-Time Validation (Table 5)
```{shell}
./cross_time.sh
cat ../results/EX2/cross_time.txt
```
[2] Reverse Cross-Time Validation (Table 6)
```{shell}
./reverse_cross_time.sh
cat ../results/EX2/reverse_cross_time.txt
```
[3] Accumulate Robustness with Mixed Dates (Table 7)
```{shell}
./accumulate_robustness_with_mixed_dates.sh
cat ../results/EX2/accumulate_robustness_with_mixed_dates.txt
```
### 3. Experiment 3 (EX3): Reexaming Partial-Trace Detection-is 30\% Really Enough?
```{shell}
cd EX3
```
[1] Accuracy vs Traffic Percentage (Elapsed Time) (Figure 7)
```{shell}
./accuracy_vs_traffic_percentage.sh
cat ../results/EX3/accuracy_vs_traffic_percentage.txt
```


