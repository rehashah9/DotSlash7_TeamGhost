import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Define create_sequences function
def create_sequences(data, look_back):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back)])
        y.append(data[i + look_back])
    return np.array(X), np.array(y)

# Load and preprocess the data
data = pd.read_csv('aws_ec2_instance_metric_cpu_utilization_daily.csv')
data['timestamp'] = pd.to_datetime(data['timestamp'])  
data.set_index('timestamp', inplace=True)
data = data[['maximum']].resample('D').mean().fillna(method='ffill')

# Normalize the data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Split the dataset into training, validation, and test sets
train_size = int(len(data_scaled) * 0.8)
val_size = int(len(data_scaled) * 0.1)
test_size = len(data_scaled) - train_size - val_size

train_data, val_data, test_data = (
    data_scaled[:train_size],
    data_scaled[train_size:train_size + val_size],
    data_scaled[train_size + val_size:]
)

# Create sequences for training, validation, and test sets
look_back = 25
X_train, y_train = create_sequences(train_data, look_back)
X_val, y_val = create_sequences(val_data, look_back)
X_test, y_test = create_sequences(test_data, look_back)

# LSTM Model
model = Sequential([
    LSTM(200, input_shape=(look_back, 1), return_sequences=True),
    Dropout(0.2),
    LSTM(200),
    Dropout(0.2),
    Dense(1)
])

model.compile(loss='mse', optimizer=Adam(learning_rate=0.0001), metrics=['mse'])

# Train the model with early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min')
history = model.fit(X_train, y_train, epochs=100, batch_size=64, 
                    validation_data=(X_val, y_val), callbacks=[early_stopping], verbose=2)

# Make predictions on the test data
y_pred = model.predict(X_test)
y_pred = scaler.inverse_transform(y_pred).reshape(-1)

# Calculate RMSE on the test data
rmse = np.sqrt(mean_squared_error(data_scaled[train_size + val_size + look_back:], y_pred))
print(f'Root Mean Squared Error (RMSE) on Test Data: {rmse}')

# Plot the data
actual_data = data[train_size + look_back:]
date_range = actual_data.index

plt.figure(figsize=(12, 6))
plt.plot(date_range, actual_data, label='Actual')
plt.plot(date_range[:len(y_pred)], y_pred, label='Predicted')
plt.xlabel('Date')
plt.ylabel('Maximum CPU Utilization')
plt.legend()
plt.title('LSTM Time Series Prediction')
plt.show()
