import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load and preprocess the data
data = pd.read_csv('aws_ec2_instance_metric_cpu_utilization_daily.csv')
data['timestamp'] = pd.to_datetime(data['timestamp'])  
data.set_index('timestamp', inplace=True)
data = data[['maximum']].resample('D').mean().fillna(method='ffill')

# Normalize the data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Create lagged features and target variable
look_back = 25
X, y = [], []
for i in range(len(data_scaled) - look_back):
    X.append(data_scaled[i:(i + look_back)].flatten())
    y.append(data_scaled[i + look_back])

X, y = np.array(X), np.array(y)

# Split the dataset into training and test sets
train_size = int(len(X) * 0.8)
test_size = len(X) - train_size

X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Support Vector Machine model
svm_model = SVR(kernel='rbf', C=100, gamma='auto')  # Adjust hyperparameters as needed
svm_model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = svm_model.predict(X_test)

# Inverse transform the predictions and actual values
y_pred_inv = scaler.inverse_transform(y_pred.reshape(-1, 1)).flatten()
y_test_inv = scaler.inverse_transform(y_test)

# Calculate RMSE on the test data
rmse = np.sqrt(mean_squared_error(y_test_inv, y_pred_inv))
print(f'Root Mean Squared Error (RMSE) on Test Data: {rmse}')

# Plot the data
date_range = data.index[train_size + look_back:]

plt.figure(figsize=(12, 6))
plt.plot(date_range, y_test_inv, label='Actual')
plt.plot(date_range, y_pred_inv, label='Predicted')
plt.xlabel('Date')
plt.ylabel('Maximum CPU Utilization')
plt.legend()
plt.title('Support Vector Machine Time Series Prediction')
plt.show()
