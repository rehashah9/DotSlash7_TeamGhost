import numpy as np
import pandas as pd
import tensorflow as tf
tf.config.run_functions_eagerly(True)
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('aws_ec2_instance_metric_cpu_utilization_daily.csv')
data['timestamp'] = pd.to_datetime(data['timestamp'])  
data.set_index('timestamp', inplace=True)
data = data[['maximum']]
data = data.resample('D').mean()
data = data.fillna(method='ffill')

# Normalize data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Split data
train_size = int(len(data) * 0.8)
val_size = int(len(data) * 0.1)
test_size = len(data) - train_size - val_size

train_data, val_data, test_data = (
    data_scaled[:train_size],
    data_scaled[train_size:train_size + val_size],
    data_scaled[train_size + val_size:],
)

# Create sequences
def create_sequences(data, look_back):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back)])
        y.append(data[i + look_back])
    return np.array(X), np.array(y)

look_back = 25
X_train, y_train = create_sequences(train_data, look_back)
X_val, y_val = create_sequences(val_data, look_back)
X_test, y_test = create_sequences(test_data, look_back)

# Reshape input data for CNN
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_val = X_val.reshape(X_val.shape[0], X_val.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# CNN Model
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(look_back, 1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(1))

model.compile(loss='mse', optimizer=Adam(learning_rate=0.0001), metrics=['mse'])

# Train the model
early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min')
history = model.fit(X_train, y_train, epochs=100, batch_size=64, validation_data=(X_val, y_val), callbacks=[early_stopping], verbose=2)

# Make predictions
y_pred = model.predict(X_test)
y_pred = y_pred.reshape(-1)
y_pred = scaler.inverse_transform(y_pred.reshape(-1, 1)).reshape(-1)

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(data[train_size + val_size + look_back:], y_pred))
print(f'Root Mean Squared Error (RMSE) on Test Data: {rmse}')

# Plot the data
actual_data = data[train_size + look_back:]
date_range = data.index[train_size + look_back:train_size + look_back + len(y_pred)]

# Plot the data
plt.figure(figsize=(12, 6))
# Ensure that date_range and actual_data have the same length
date_range = date_range[:len(y_pred)]
actual_data = actual_data[:len(y_pred)]
plt.plot(date_range, actual_data, label='Actual')
plt.plot(date_range, y_pred, label='Predicted')
plt.xlabel('Date')
plt.ylabel('Maximum CPU Utilization')
plt.legend()
plt.title('CNN Time Series Prediction')
plt.show()

