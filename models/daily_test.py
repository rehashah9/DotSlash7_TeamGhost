import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import joblib
import streamlit as st

# Load the saved SVM model
loaded_svm_model = joblib.load('svm_model_daily.pkl')

# Load the original training data
original_data = pd.read_csv('aws_ec2_instance_metric_cpu_utilization_daily.csv')
original_data['timestamp'] = pd.to_datetime(original_data['timestamp'])  
original_data.set_index('timestamp', inplace=True)
original_data = original_data[['maximum']].resample('D').mean().fillna(method='ffill')

# Normalize the original data using the same scaler as before
scaler = MinMaxScaler()
original_data_scaled = scaler.fit_transform(original_data)

# Create lagged features and target variable for the original data
look_back = 4
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

# Number of days to forecast beyond the original data
forecast_days = 30  # You can adjust this value as needed

# Initialize the last known sequence to start forecasting
last_sequence = X_original[-1]

# Forecast into the future
forecasted_values = []
for _ in range(forecast_days):
    # Reshape the last known sequence for prediction
    prediction_features = last_sequence.reshape(1, -1)
    
    # Make prediction using the loaded SVM model
    next_prediction = loaded_svm_model.predict(prediction_features)
    
    # Inverse transform the prediction
    next_prediction_inv = scaler.inverse_transform(next_prediction.reshape(-1, 1)).flatten()
    
    # Append the prediction to the forecasted values
    forecasted_values.append(next_prediction_inv[0])
    
    # Update the last sequence by removing the first entry and adding the predicted value
    last_sequence = np.roll(last_sequence, -1)
    last_sequence[-1] = next_prediction
    
# Extend the index to include the forecasted days
forecast_index = pd.date_range(start=original_data.index[-1] + pd.Timedelta(days=1), periods=forecast_days, freq='D')

st.title('Support Vector Machine Time Series Prediction')
st.write("### Actual vs Predicted CPU Utilization")

# Plot the original data and the forecasted values
fig = plt.figure(figsize=(12,6))
plt.plot(original_data.index[look_back:], y_original_inv, label='Actual')
plt.plot(original_data.index[look_back:], y_pred_original_inv, label='Predicted')
plt.plot(forecast_index, forecasted_values, label='Forecast', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Maximum CPU Utilization')
plt.legend()
plt.title('Support Vector Machine Time Series Prediction (Original Data + Forecast)')
st.write(fig)
