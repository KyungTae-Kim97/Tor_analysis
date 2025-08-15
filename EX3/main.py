import torch.nn as nn
import torch.optim as optim
from utils.data_loader import *
from engine import run_experiment
from argparser import get_args


if __name__ == "__main__":
    
    args = get_args()

    f = open(f'{args.result}', 'a')  # open log file
    f.write(f"dataset is {args.file_name}\n")
    f.close()
    
    train_loader, test_loader = get_data_loader(    
        file_dataframe=args.file_name, 
        batch_size=args.batch_size, 
        seed=args.seed, 
        num_cls=args.num_cls,
        data_size_per_class=args.data_size_per_class,
        early_stage = args.early_stage
    )

    run_experiment(
        args.num_epochs, 
        train_loader, 
        test_loader, 
        args.device,
        args.result,
        args.early_stage
        )