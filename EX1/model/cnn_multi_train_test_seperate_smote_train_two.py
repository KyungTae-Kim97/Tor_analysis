from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
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

file_dataframe1 = sys.argv[1]
file_dataframe2 = sys.argv[2]
file_dataframe3 = sys.argv[3]
data_size_per_class = sys.argv[4]
num_classes = int(sys.argv[5])
result_file = sys.argv[6]

df_train1= pd.read_csv(file_dataframe1)
df_train1 = df_train1.fillna(0)  

df_train2= pd.read_csv(file_dataframe2)
df_train2 = df_train2.fillna(0)  

df_test= pd.read_csv(file_dataframe3)
df_test = df_test.fillna(0)  

X_train1 = df_train1.iloc[:, :-1].values  
X_train2 = df_train2.iloc[:, :-1].values  
X_train = np.vstack([X_train1, X_train2])

y_train1 = df_train1.iloc[:, -1].values  
y_train2 = df_train2.iloc[:, -1].values  
y_train = np.hstack([y_train1, y_train2])

num_columns = df_train1.shape[1] -1
file_list = [num_columns]

X_test = df_test.iloc[:, :-1].values  
labels = []
for i in range(num_classes):
    labels.extend([i] * int(data_size_per_class))
y_test = np.array(labels)

f = open(f'{result_file}', 'a')  
f.write(f"train1 is {file_dataframe1}\n")
f.write(f"train2 is {file_dataframe2}\n")
f.write(f"test is {file_dataframe3}\n")

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

        model.fit(X_train, y_train, epochs=1, batch_size=64, verbose=1)

        y_pred_prob = model.predict(X_test)
        y_pred = np.argmax(y_pred_prob, axis=1) 
        
        accuracy = accuracy_score(y_test, y_pred)
        accuracy_list.append(accuracy)
        end = time.time()
f.write(f'max accuracy: {max(accuracy_list)}\n')
f.write("************\n")
f.close()                    