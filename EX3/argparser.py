import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Mamba Experiment Arguments")

    parser.add_argument('--num_epochs', type=int, default=100, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=64, help='Mini-batch size')
    parser.add_argument('--file_name', type=str, default="dataset_WTCM/USA1", help='path of the dataset')
    parser.add_argument('--device', type=str, default='cuda', choices=['cpu', 'cuda'], help='Device to use for computation')
    parser.add_argument('--num_cls', type=int, default=5, help='Number of classes')
    parser.add_argument('--data_size_per_class', type=int, default=300, help='number of instances per class')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--early_stage', type=bool, default=False, help='early_stage')
    parser.add_argument('--result', type=str, default='../results/EX3/accuracy_vs_traffic_percentage.txt', help='where to save results')

    return parser.parse_args()
