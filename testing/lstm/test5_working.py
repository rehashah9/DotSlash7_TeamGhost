import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pymongo
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential

# Function to save data to MongoDB
def save_to_mongodb(data_dict, database_name, collection_name):
    client = pymongo.MongoClient("")
    db = client[database_name]
    collection = db[collection_name]
    collection.insert_one(data_dict)

# Function to load data from MongoDB
def load_from_mongodb(database_name, collection_name):
    client = pymongo.MongoClient("")
    db = client[database_name]
    collection = db[collection_name]
    data = collection.find_one()
    return pd.DataFrame(data)

def normalize_data(data, scaler=None):
    # If a scaler is provided, use it for transformation; otherwise, create and fit a new scaler
    if scaler is None:
        scaler = MinMaxScaler()
        data_scaled = scaler.fit_transform(data)
    else:
        data_scaled = scaler.transform(data)
    
    return data_scaled, scaler

def create_sequences(data, look_back):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back)])
        y.append(data[i + look_back])
    return np.array(X), np.array(y)

def build_lstm_model(look_back):
    model = Sequential()
    model.add(LSTM(200, input_shape=(look_back, 1), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(200))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam', metrics=['mse'], run_eagerly=True)
    return model

def train_lstm_model(model, X_train, y_train, epochs, batch_size, validation_split, X_val, y_val):
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min')
    history = model.fit(X_train, y_train, epochs=100, batch_size=64, validation_data=(X_val, y_val), callbacks=[early_stopping], verbose=2)
    # history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=2, validation_split=validation_split)
    return model, history

def evaluate_model(model, data, scaler, train_size, val_size, look_back, X_test, y_test):
    # X_test, y_test = create_sequences(data[train_size:], look_back)
    y_pred = model.predict(X_test)
    y_pred = scaler.inverse_transform(y_pred)
    y_pred = y_pred.reshape(-1)
    
    rmse = np.sqrt(mean_squared_error(data[train_size + val_size + look_back:], y_pred))
    return rmse, y_pred

def save_model_to_mongodb(model, database_name, collection_name):
    client = pymongo.MongoClient("")
    db = client[database_name]
    collection = db[collection_name]
    model_json = model.to_json()
    collection.insert_one({'model_json': model_json})


def load_model_from_mongodb(database_name, collection_name):
    client = pymongo.MongoClient("")
    db = client[database_name]
    collection = db[collection_name]
    model_data = collection.find_one()
    model_json = model_data['model_json']
    model = model_from_json(model_json)

    # Compile the model if needed
    model.compile(optimizer='adam', loss='mean_squared_error')  # Adjust the compilation parameters

    return model

# Streamlit app
st.title("CSV to MongoDB and Visualization")

# Handle the warning
st.set_option('deprecation.showPyplotGlobalUse', False)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], key="csv_uploader")
if uploaded_file is not None:
    st.write("Uploading and saving the data to MongoDB...")

    # Read the CSV file
    data = pd.read_csv(uploaded_file)
    df = pd.DataFrame(data)
    data_dict = df.to_dict('list')

    # Save data to MongoDB
    save_to_mongodb(data_dict, 'User1', 'train')

    st.write("Data saved to MongoDB")

# Display graphs
st.header("Data Visualization")

if st.button("Load and Display Data from MongoDB"):
    st.write("Loading data from MongoDB and displaying graphs...")

    # Load data from MongoDB
    loaded_data = load_from_mongodb('User1', 'train')
    df = pd.DataFrame(loaded_data)

    # Display boxplot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='instance_id', y='maximum', data=df)
    plt.title('CPU Utilization by Instance Type')
    plt.xlabel('Instance Type')
    plt.ylabel('CPU Utilization')
    plt.xticks(rotation=45)
    st.pyplot()

    # Display lineplot
    st.header("Max, Min and Avg Utilization by Instance Type")
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='instance_id', y='maximum', data=df, label='Maximum', markers=True, color='red')
    sns.lineplot(x='instance_id', y='minimum', data=df, label='Minimum', markers=True, color='green')
    sns.lineplot(x='instance_id', y='average', data=df, label='Average', markers=True, color='blue')
    plt.title('Max, Min and Avg Utilization by Instance Type')
    plt.xlabel('Instance Type')
    plt.ylabel('Utilization')
    plt.xticks(rotation=45)
    plt.legend(title='Metric')
    st.pyplot()

# Train and save the LSTM model from the loaded data in train
if st.button("Train and Save LSTM Model from Loaded Data"):
    st.write("Training and saving the LSTM model from the loaded data...")

    # Load data from train
    loaded_data = load_from_mongodb('User1', 'train')
    loaded_df = pd.DataFrame(loaded_data)

    # Set the index of the loaded DataFrame to the 'timestamp' column
    loaded_df['timestamp'] = pd.to_datetime(loaded_df['timestamp'])
    loaded_df.set_index('timestamp', inplace=True)

    # Preprocess the loaded data (similar to what was done during training)
    data = loaded_df[['maximum']].resample('D').mean().fillna(method='ffill')
    data_scaled, scaler = normalize_data(data)

    # Define the look-back period (should match the one used for training)
    look_back = 25

    # Create sequences from the loaded data
    # X_train, y_train = create_sequences(data_scaled, look_back)

    # Build and train the LSTM model
    model = build_lstm_model(look_back)

    # Train the model with a validation split
    train_size = int(len(data) * 0.8)
    val_size = int(len(data) * 0.1)
    test_size = len(data) - train_size - val_size
    
    train_data, val_data, test_data = (
        data_scaled[:train_size],
        data_scaled[train_size:train_size + val_size],
        data_scaled[train_size + val_size:],
    )
    
    X_train, y_train = create_sequences(train_data, look_back)
    X_val, y_val = create_sequences(val_data, look_back)
    X_test, y_test = create_sequences(test_data, look_back)
    
    train_lstm_model(model, X_train, y_train, epochs=100, batch_size=64, validation_split=0.1, X_val=X_val, y_val=y_val)

    # Evaluate the model on the loaded data
    rmse, y_pred = evaluate_model(model, data_scaled, scaler, train_size, val_size, look_back, X_test, y_test)
    st.write(f'Root Mean Squared Error (RMSE) on Loaded Data: {rmse}')

    # Save the trained model to MongoDB
    save_model_to_mongodb(model, 'User1', 'model')


test_uploaded_file = st.file_uploader("Upload a Test CSV file", type=["csv"], key="test_csv_uploader")
if test_uploaded_file is not None:
    st.write("Uploading and saving the data to MongoDB...")

    # Read the CSV file
    data = pd.read_csv(test_uploaded_file)
    df = pd.DataFrame(data)
    data_dict = df.to_dict('list')

    # Save data to MongoDB
    save_to_mongodb(data_dict, 'User1', 'test')

    st.write("Data saved to MongoDB")

# Load and predict with the trained model
if st.button("Load Model and Make Predictions"):
    st.write("Loading the trained model...")

    # Load the trained model from MongoDB
    loaded_model = load_model_from_mongodb('User1', 'model')

    # Ask users to upload the test data (test.csv)
    st.write("Making predictions on the test data...")

    # Load and preprocess the test data
    loaded_data = load_from_mongodb('User1', 'test')
    test_data = pd.DataFrame(loaded_data)
    
    test_data['timestamp'] = pd.to_datetime(test_data['timestamp'])
    test_data.set_index('timestamp', inplace=True)
    test_data = test_data[['maximum']]
    test_data = test_data.resample('D').mean()
    test_data = test_data.fillna(method='ffill')
    
    scaler = MinMaxScaler()
    scaler.fit(test_data)
    # Normalize the test data using the fitted scaler from the training phase
    test_data_scaled, _ = normalize_data(test_data, scaler)

    # Define the look-back period (should match the one used for training)
    look_back = 30

    # Create sequences from the test data
    X_test, y_test = create_sequences(test_data_scaled, look_back)

    # Make predictions using the loaded model
    y_pred = loaded_model.predict(X_test)
    y_pred = scaler.inverse_transform(y_pred)

    # Calculate RMSE or any other evaluation metric
    rmse = np.sqrt(mean_squared_error(test_data[look_back:], y_pred))
    st.write(f'Root Mean Squared Error (RMSE) on Test Data: {rmse}')

    # Plot the results
    plt.figure(figsize=(12, 6))
    plt.plot(test_data.index[look_back:], test_data[look_back:], label='Actual')
    plt.plot(test_data.index[look_back:], y_pred, label='Predicted')
    plt.xlabel('Date')
    plt.ylabel('Maximum CPU Utilization')
    plt.legend()
    plt.title('LSTM Time Series Prediction (Test Data)')
    st.pyplot()
