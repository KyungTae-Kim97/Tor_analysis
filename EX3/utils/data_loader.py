import torch
import pandas as pd
from torch.utils.data import DataLoader, Dataset, Subset
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import glob
from utils.utils import *

class CSV_Dataset(Dataset):
    def __init__(
        self, 
        file_dataframe:str, 
        num_classes:int=5,
        data_size_per_class:int=150,
        early_stage = False
        ):
        super(CSV_Dataset, self).__init__()
        self.file_dataframe_dir = file_dataframe
        self.data = []
        self.labels = []
        self.early_stage = early_stage

        csv_files = sorted(glob.glob(f"{self.file_dataframe_dir}/*.csv"))
        
        for file in csv_files:
            df = pd.read_csv(file, header = None)
            df = df.fillna(0)  
            self.data.append(df)

        for i in range(num_classes):
            self.labels.extend([i] * int(data_size_per_class))
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        
        # Load the .npy file
        sample = self.data[idx]
        
        # Convert to tensor
        sample = torch.tensor(sample.values, dtype=torch.float)
        if self.early_stage:
            label = self.labels[idx]
        else:
            label = self.labels[idx]
        label = torch.tensor(label)
        return sample, label

def get_data_loader(
    file_dataframe:str, 
    batch_size:int, 
    seed:int=42, 
    num_cls:int=5,
    data_size_per_class:int=150,
    early_stage=False
    ):

    """
    """
    dataset = CSV_Dataset(
        file_dataframe, 
        num_cls,
        data_size_per_class,
        early_stage
        )
    indices = list(range(len(dataset)))
    print("number of data: ",len(dataset)) 
    print("number of label: ",len(dataset.labels)) 
    if early_stage:
        print("early_stage: on")

    train_indices, test_indices = train_test_split(
        indices, 
        test_size=0.2, 
        random_state=seed,
        stratify = dataset.labels
        )

    train_dataset = Subset(
        dataset, 
        train_indices
        )
    test_dataset = Subset(
        dataset, 
        test_indices
        )

    train_loader = DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=True
        )
    test_loader = DataLoader(
        test_dataset, 
        batch_size=batch_size, 
        shuffle=False
        )

    return train_loader, test_loader