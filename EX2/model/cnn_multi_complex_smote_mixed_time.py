from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, BatchNormalization
from keras.optimizers import Adam
from keras.utils import to_categorical
import sys
from sklearn.metrics import confusion_matrix
import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import time
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
print("TensorFlow version:", tf.__version__)
print("Num GPUs Available:", len(tf.config.list_physical_devices('GPU')))

week_1 = sys.argv[1]
week_2 = sys.argv[2]
data_size_per_class = int(sys.argv[3])
num_classes = int(sys.argv[4])
result_file = sys.argv[5]

df_week_1= pd.read_csv(week_1)
df_week_1 = df_week_1.fillna(0)  

df= pd.read_csv(week_2)
df = df.fillna(0)  

num_columns = df.shape[1] -1
file_list = [num_columns]

f = open(f'{result_file}', 'a')  
f.write(f"train1 is {week_1}\n")
f.write(f"train2 is {week_2}\n")
f.write(f"test is {week_2}\n")

for number in file_list:
    model = Sequential([
    Conv1D(filters=32, kernel_size=3, padding="same", activation='relu', input_shape=(number, 1)),
    Conv1D(filters=32, kernel_size=3,padding="same", activation='relu'),
    BatchNormalization(),
    MaxPooling1D(pool_size=2),
    Dropout(0.25),  

    Conv1D(filters=64, kernel_size=3,padding="same", activation='relu'),
    Conv1D(filters=64, kernel_size=3,padding="same", activation='relu'),
    BatchNormalization(),
    MaxPooling1D(pool_size=2),
    Dropout(0.25),  

    Conv1D(filters=128, kernel_size=3, padding="same", activation='relu'),
    Conv1D(filters=128, kernel_size=3, padding="same", activation='relu'),
    BatchNormalization(),
    MaxPooling1D(pool_size=2),
    Dropout(0.25),  

    Flatten(),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),  

    Dense(num_classes, activation='softmax') 
    ])

    model.compile(optimizer=Adam(learning_rate=0.001),
              loss='categorical_crossentropy', 
              metrics=['accuracy'])
    accuracy_list = []

    X_original = df.iloc[:(data_size_per_class*num_classes), :-1].values  
    y_original = df.iloc[:(data_size_per_class*num_classes), -1].values   
    indices = np.arange(len(y_original))

    test_X_scaled = X_original.reshape(-1, number, 1)

    _, X_test, _, y_test, idx_train, idx_test = train_test_split(test_X_scaled, y_original, indices, stratify=y_original, test_size=0.2, random_state=42)

    X_week_1 = df_week_1.iloc[:, :-1].values  
    y_week_1 = df_week_1.iloc[:, -1].values

    X = df.iloc[:, :-1].values  
    y = df.iloc[:, -1].values   

    X_test = X[idx_test]
    y_test = y[idx_test]
    X = np.delete(X, idx_test, axis=0)
    y = np.delete(y, idx_test, axis=0)
    
    X_train = np.vstack([X_week_1, X])
    y_train = np.hstack([y_week_1, y])

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train) 

    X_test = scaler.transform(X_test)

    X_train = X_train.reshape(-1, number, 1)
    X_test = X_test.reshape(-1, number, 1)

    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)
    y_test = np.argmax(y_test, axis=1)

    for i in range(100):
        start = time.time()
        print(f"idx: {i}")
        
        model.fit(X_train, y_train, epochs=1, batch_size=64)

        y_pred_prob = model.predict(X_test)
        y_pred = np.argmax(y_pred_prob, axis=1) 

        accuracy = accuracy_score(y_test, y_pred)
        accuracy_list.append(accuracy)
        end = time.time()
f.write(f'max accuracy: {max(accuracy_list)}\n')
f.write("************\n")
f.close()                    
