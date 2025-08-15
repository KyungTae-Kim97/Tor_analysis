import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import math

from time import time
from utils.utils import *
from model import ZOHLinearLayer, StackedZOHModel

def run_experiment(num_epochs, train_loader, test_loader, device, result_file, early_stage=False):
    # Experiment loop

    f = open(f'{result_file}', 'a')  # open log file

    machine = StackedZOHModel(
                input_dim=8,
                hidden_dim=128, 
                kernel = 10,
                depth=2, 
                delta=0.01, 
                timestamp=2000,
                num_classes= 10,
                device = device,
                early_stage = early_stage
                ).to(device)

    if early_stage:
        criterion = nn.CrossEntropyLoss().to(device)
        optimizer = optim.Adam(machine.parameters(), lr=0.001, weight_decay=1e-5) 
    else:
        criterion = nn.CrossEntropyLoss().to(device)
        optimizer = optim.Adam(machine.parameters(), lr=0.001, weight_decay=1e-5) 

    # Training steps
    print("training")
    accuracy_list =[]
    total_results = np.zeros((10, 100))
    for idx, epoch in enumerate(range(num_epochs)):
        start = time()
        machine.train()
        correct = 0
        total = 0
        loss_sum = 0
        for x_batch, y_batch in train_loader:
            x_batch = x_batch.to(device)
            y_batch = y_batch.to(device)
            
            if early_stage:
                # Forward pass
                outputs = machine(x_batch) # (batch, timestamp, num_classes)
                predicted = torch.argmax(outputs, dim=1)  # get predicted class
                correct += (predicted == y_batch).sum().item()
                total += y_batch.size(0)
            else:
                # Forward pass
                outputs = machine(x_batch)
                predicted = torch.argmax(outputs, dim=1)  # get predicted class
                correct += (predicted == y_batch).sum().item()
                total += y_batch.size(0)
            # Compute loss
            loss = criterion(outputs, y_batch)
            loss_sum += loss.item()
            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward(retain_graph=True)
            optimizer.step()
        
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss_sum/len(train_loader):.4f}')
        accuracy = correct / total
        print(f"Train Accuracy: {accuracy * 100:.2f}%") 
        
        # Inference steps
        with torch.no_grad():
            machine.eval()
            correct = 0
            total = 0
            if early_stage:
                for i in range(10):
                    percent = (i+1) * 10
                    correct = 0
                    total = 0   
                    for x_batch, y_batch in test_loader:
                        x_batch = x_batch.to(device)
                        y_batch = y_batch.to(device)
                        outputs= machine.inference(x_batch, percent) 
                        
                        predicted = torch.argmax(outputs, dim=1)  # get predicted class
                        correct += (predicted == y_batch).sum().item()
                        total += y_batch.size(0)
                    accuracy = correct / total
                    total_results[i][epoch] = accuracy
                    print(f"Percent: {percent}%, Test Accuracy: {accuracy * 100:.2f}%") 
            else:
                for x_batch, y_batch in test_loader:
                    x_batch = x_batch.to(device)
                    y_batch = y_batch.to(device)
        
                    outputs= machine(x_batch)
                    # Forward pass
                    predicted = torch.argmax(outputs, dim=1)  # get predicted class
                    correct += (predicted == y_batch).sum().item()
                    total += y_batch.size(0)
        
                accuracy = correct / total
                accuracy_list.append(accuracy)
                print(f"Test Accuracy: {accuracy * 100:.2f}%")    
    
    if early_stage:
        for i in range(10):
            max_value = max(total_results[i])
            f.write(f'percentage: {(i+1)*10}\n')
            f.write(f'max accuracy: {max_value}\n')
        f.write("************\n")
        f.close()               
    else: 
        f.write(f'max accuracy: {max(accuracy_list)}\n')
        f.write("************\n")
        f.close()                    # close file
