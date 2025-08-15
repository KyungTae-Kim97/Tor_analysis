import torch
import torch.nn as nn
from scipy.linalg import expm
import numpy as np
from utils.utils import *
import math

class FixedPositionalEncoding(nn.Module):
    def __init__(self, hidden_dim, max_len=2000):
        super().__init__()

        pe = torch.zeros(max_len, hidden_dim)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, hidden_dim, 2).float() * (-math.log(10000.0) / hidden_dim))
        
        pe[:, 0::2] = torch.sin(position * div_term)  # even dims
        pe[:, 1::2] = torch.cos(position * div_term)  # odd dims

        pe = pe.unsqueeze(0)  # shape: (1, max_len, hidden_dim)
        self.register_buffer('pe', pe)  # non-learnable

    def forward(self, x):
        # x: (batch, timestamp, hidden_dim)
        seq_len = x.size(1)
        return x + self.pe[:, :seq_len, :]

class CausalConv1d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size):
        super(CausalConv1d, self).__init__()
        self.padding = kernel_size - 1
        self.conv = nn.Conv1d(
            in_channels, out_channels,
            kernel_size=kernel_size,
            padding=self.padding
        )

    def forward(self, x):
        out = self.conv(x)
        return out[:, :, :-self.padding]  # Remove future-padding output

class CausalCNN(nn.Module):
    def __init__(self, input_channels=1, hidden_channels=64, depth=3, kernel_size=3):
        super().__init__()
        layers = []
        for i in range(depth):
            in_ch = input_channels if i == 0 else hidden_channels
            layers.append(CausalConv1d(in_ch, hidden_channels, kernel_size))
            layers.append(nn.BatchNorm1d(hidden_channels))
            layers.append(nn.ReLU())
            # layers.append(nn.Dropout(0.1))

        self.network = nn.Sequential(*layers)

    def forward(self, x):
        # x: (batch, channels, timestamp)
        x = self.network(x)  # (batch, hidden, timestamp)
        x = x.transpose(1,2) # (batch, timestamp, hidden)
        return x

class ZOHLinearLayer(nn.Module):
    def __init__(self, dim, delta, timestamp, device):
        super().__init__()
        self.dim = dim
        self.delta = delta
        self.timestamp = timestamp
        self.device = device
        # self.A = nn.Parameter(torch.randn(dim, dim) * 0.001)
        self.A = nn.Parameter(torch.eye(dim) * -0.01 + torch.randn(dim, dim) * 0.001)
        self.B = nn.Parameter(torch.randn(dim, 1) * 0.01)
        self.C = nn.Parameter(torch.randn(1, dim) * 0.01)
        # self.K_BAR = self.get_K_bar(self.timestamp)

    def _zoh_discretize(self):
        A_bar = torch.matrix_exp(self.delta * self.A)  # autograd-friendly
        I = torch.eye(self.dim, device=self.A.device, dtype=self.A.dtype)
        A_stable = self.A + 1e-3 * I
        A_inv = torch.linalg.inv(A_stable)  # use torch, not numpy
        B_bar = A_inv @ (A_bar - I) @ (self.delta * self.B)
        return A_bar, B_bar

    def _compute_K_bar(self, A_bar, B_bar, M):
        A_power = torch.eye(self.dim, device=A_bar.device)
        C = self.C.to(self.device)
        K_terms = []

        for _ in range(M):
            term = C @ (A_power @ B_bar)  # shape: (1, 1)
            K_terms.append(term)
            A_power = A_bar @ A_power

        K_bar = torch.cat(K_terms, dim=1)  # shape: (1, M)
        K_bar = torch.flip(K_bar, dims=[1]) # reversed_x
        return K_bar

class StackedZOHModel(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=256, kernel=3, depth=5, delta=0.1, timestamp=104, num_classes=5, device='cuda', early_stage=False):
        super().__init__()
        self.timestamp = timestamp
        self.early_stage = early_stage
        self.cnn_layers= CausalCNN(input_dim, hidden_dim, depth, kernel)
        self.pe = FixedPositionalEncoding(hidden_dim= hidden_dim)
        
        self.layers = nn.ModuleList([ZOHLinearLayer(hidden_dim, delta, timestamp, device).to(device) for _ in range(depth)])
        self.input_proj = nn.Linear(hidden_dim, hidden_dim)

        self.fc_temp = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim), 
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_dim, num_classes)
        )

        self.device = device
        self.num_classes = num_classes
        
    def forward(self, x):
        # x: (batch, C*2 + 2, timestamp)
        x = self.cnn_layers(x)  # (batch, timestamp, hidden_dim)
        x = self.pe(x)
        x = self.input_proj(x)  # (batch, timestamp, hidden_dim)

        for layer in self.layers: #recompute K_BAR dynamically
            A_bar, B_bar = layer._zoh_discretize()
            K_bar = layer._compute_K_bar(A_bar, B_bar, self.timestamp)  # (1, T)
            K_bar = K_bar / (K_bar.norm(p=2) + 1e-6)  # normalize
            K_bar = K_bar.unsqueeze(-1)  # (1, T, 1)
            x = (x * K_bar) # (batch, timstamp, hidden_dim)
        if self.early_stage:
            x = x.mean(dim = 1) # (batch, hidden_dim)
            logits = self.fc_temp(x) # (batch, num_classes)
        else:
            x = x.mean(dim = 1) # (batch, hidden_dim)
            logits = self.fc_temp(x) # (batch, num_classes)
        return logits
    
    def inference(self, x, percent):
        # x: (batch, timestamp, 1)
        x = self.cnn_layers(x)  # (batch, timestamp, hidden_dim)
        x = self.pe(x)
        x = self.input_proj(x)  # (batch, timestamp, hidden_dim)

        for layer in self.layers: #recompute K_BAR dynamically
            A_bar, B_bar = layer._zoh_discretize()
            K_bar = layer._compute_K_bar(A_bar, B_bar, self.timestamp)  # (1, T)
            K_bar = K_bar / (K_bar.norm(p=2) + 1e-6)  # normalize
            K_bar = K_bar.unsqueeze(-1)  # (1, T, 1)
            x = (x * K_bar) # (batch, timstamp, hidden_dim)
        if self.early_stage:            
            # x = last_percent_elements(x, self.percentage) # (batch, timestamp*percent, hidden_dim)
            x = last_percent_elements(x, percent) # (batch, timestamp*percent, hidden_dim)
            x = x.mean(dim = 1) # (batch, hidden_dim)
            logits = self.fc_temp(x) # (batch, num_classes) 

        return logits