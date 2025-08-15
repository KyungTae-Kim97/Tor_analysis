#!/bin/bash

#USA1
python model/cnn_multi_complex_smote.py ../dataset/smote_900/USA1/125_250614_smote_900.csv 300 10 ../results/EX1/same_location.txt
python model/cnn_multi_complex_smote.py ../dataset/smote_900/USA1/141_250614_smote_900.csv 300 10 ../results/EX1/same_location.txt
python model/cnn_multi_complex_smote.py ../dataset/smote_900/USA1/cumul_250614_smote_900.csv 300 10 ../results/EX1/same_location.txt

#USA2
python model/cnn_multi_complex_smote.py ../dataset/smote_900/USA2/125_250614_smote_900.csv 300 10 ../results/EX1/same_location.txt
python model/cnn_multi_complex_smote.py ../dataset/smote_900/USA2/141_250614_smote_900.csv 300 10 ../results/EX1/same_location.txt
python model/cnn_multi_complex_smote.py ../dataset/smote_900/USA2/cumul_250614_smote_900.csv 300 10 ../results/EX1/same_location.txt

#South_Korea
python model/cnn_multi_complex_smote.py ../dataset/smote_900/South_Korea/125_250702_smote_900.csv 300 10 ../results/EX1/same_location.txt
python model/cnn_multi_complex_smote.py ../dataset/smote_900/South_Korea/141_250702_smote_900.csv 300 10 ../results/EX1/same_location.txt
python model/cnn_multi_complex_smote.py ../dataset/smote_900/South_Korea/cumul_250702_smote_900.csv 300 10 ../results/EX1/same_location.txt
