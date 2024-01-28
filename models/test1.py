import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import joblib

# Load the saved SVM model
loaded_svm_model = joblib.load('svm_model.pkl')

# Load the original training data
original_data = pd.read_csv('random_live_data.csv')
original_data['timestamp'] = pd.to_datetime(original_data['timestamp'])  
original_data.set_index('timestamp', inplace=True)
original_data = original_data[['maximum']].resample('S').mean().fillna(method='ffill')

# Normalize the original data using the same scaler as before
scaler = MinMaxScaler()
original_data_scaled = scaler.fit_transform(original_data)

# Create lagged features and target variable for the original data
look_back = 27
X_original, y_original = [], []
for i in range(len(original_data_scaled) - look_back):
    X_original.append(original_data_scaled[i:(i + look_back)].flatten())
    y_original.append(original_data_scaled[i + look_back])

X_original, y_original = np.array(X_original), np.array(y_original)

# Make predictions using the loaded SVM model
y_pred_original = loaded_svm_model.predict(X_original)

# Inverse transform the predictions and actual values
y_pred_original_inv = scaler.inverse_transform(y_pred_original.reshape(-1, 1)).flatten()
y_original_inv = scaler.inverse_transform(y_original)

# Calculate RMSE on the original data
rmse_original = np.sqrt(mean_squared_error(y_original_inv, y_pred_original_inv))
print(f'Root Mean Squared Error (RMSE) on Original Data: {rmse_original}')

# Plot the original data
plt.figure(figsize=(12, 6))
plt.plot(original_data.index[look_back:], y_original_inv, label='Actual')
plt.plot(original_data.index[look_back:], y_pred_original_inv, label='Predicted')
plt.xlabel('Date')
plt.ylabel('Maximum CPU Utilization')
plt.legend()
plt.title('Support Vector Machine Time Series Prediction (Original Data)')
plt.show()
