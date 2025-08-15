#!/bin/bash

#USA1
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA1/125_250614_smote_900.csv ../dataset/USA2/125_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA1/125_250614_smote_900.csv ../dataset/South_Korea/125_250702.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA1/141_250614_smote_900.csv ../dataset/USA2/141_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA1/141_250614_smote_900.csv ../dataset/South_Korea/141_250702.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA1/cumul_250614_smote_900.csv ../dataset/USA2/cumul_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA1/cumul_250614_smote_900.csv ../dataset/South_Korea/cumul_250702.csv 300 10 ../results/EX1/cross_location.txt

#USA2
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA2/125_250614_smote_900.csv ../dataset/USA1/125_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA2/125_250614_smote_900.csv ../dataset/South_Korea/125_250702.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA2/141_250614_smote_900.csv ../dataset/USA1/141_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA2/141_250614_smote_900.csv ../dataset/South_Korea/141_250702.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA2/cumul_250614_smote_900.csv ../dataset/USA1/cumul_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/USA2/cumul_250614_smote_900.csv ../dataset/South_Korea/cumul_250702.csv 300 10 ../results/EX1/cross_location.txt

#South_Korea
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/South_Korea/125_250702_smote_900.csv ../dataset/USA2/125_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/South_Korea/125_250702_smote_900.csv ../dataset/USA1/125_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/South_Korea/141_250702_smote_900.csv ../dataset/USA2/141_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/South_Korea/141_250702_smote_900.csv ../dataset/USA1/141_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/South_Korea/cumul_250702_smote_900.csv ../dataset/USA2/cumul_250614.csv 300 10 ../results/EX1/cross_location.txt
python model/cnn_multi_train_test_seperate_smote.py ../dataset/smote_900/South_Korea/cumul_250702_smote_900.csv ../dataset/USA1/cumul_250614.csv 300 10 ../results/EX1/cross_location.txt

