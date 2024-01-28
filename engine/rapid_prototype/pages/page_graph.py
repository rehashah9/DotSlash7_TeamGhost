import streamlit as st
import pandas as pd
from datetime import datetime
import time
import plotly.express as px
import json
import random
import altair as alt
from api.main import execute_raw






# Function to generate random values within a range
def generate_random_value(min_value, max_value):
    return random.uniform(min_value, max_value)


def get_metrics():
    # Assuming get_metrics is a function to fetch data from the API or some source
    # Replace this function with your actual data fetching logic
    # For demonstration purposes, using a dummy JSON file
    alpha_data = json.load(open("./pages/dummy.json"))
    return alpha_data

# Initial data fetching
# data = get_metrics()["data"]





st.set_page_config(
    page_title='Real-Time Data Science Dashboard',
    page_icon='✅',
    layout='wide'
)

# Dashboard title
st.title("Monitoring Dashboard")

# Create an empty container for the chart
chart_container = st.empty()


alpha = execute_raw("aws_ec2_list",{
        "connection_id": "aws_demo"
    })

list_of_instances = []
for x in alpha:
    list_of_instances.append(x["instance_id"])


# Create DropDown to Select Instance
instance_id = st.selectbox(
    'Select Instance',
    list_of_instances
)


def create_graph_daily(daily_utilization_data,hourly_utilization_data):
    for entry in daily_utilization_data + hourly_utilization_data:
        entry["timestamp"] = datetime.strptime(entry["timestamp"], "%a, %d %b %Y %H:%M:%S GMT")

    # Convert data to Pandas DataFrames
    daily_df = pd.DataFrame(daily_utilization_data)
    hourly_df = pd.DataFrame(hourly_utilization_data)

    # Streamlit app
    st.title("Utilization Line Charts")

    # Daily Line chart
    st.subheader("Daily Utilization Line Chart")
    daily_chart = alt.Chart(daily_df).mark_line().encode(
        x='timestamp:T',
        y='average:Q'
    ).properties(width=800, height=400)
    st.altair_chart(daily_chart, use_container_width=True)

    # Hourly Line chart
    st.subheader("Hourly Utilization Line Chart")
    hourly_chart = alt.Chart(hourly_df).mark_line().encode(
        x='timestamp:T',
        y='average:Q'
    ).properties(width=800, height=400)
    st.altair_chart(hourly_chart, use_container_width=True)

    # Display raw data
    st.subheader("Raw Data - Daily")
    st.write(daily_df)

    st.subheader("Raw Data - Hourly")
    st.write(hourly_df)

    



# Create a new data point
if instance_id:
    instance_data = execute_raw("aws_ec2_instance_details",{
        "connection_id": "aws_demo",
        "instance_id": instance_id
    })
    

    print(instance_id)

    instance_daily = execute_raw("aws_ec2_instance_metric_cpu_utilization_daily",{
            "connection_id": "aws_demo",
            "instance_id": instance_id
        })
    
    print("This is instance daily: ",instance_daily)
    instance_hourly = execute_raw("aws_ec2_instance_metric_cpu_utilization_hourly",{
            "connection_id": "aws_demo",
            "instance_id": instance_id
        })
    
    print("")
    
    open("./pages/dummy.json","w").write(json.dumps(instance_hourly))
    if instance_daily == None or instance_hourly == None:
        st.write("No Data")
    else:
        create_graph_daily(instance_daily,instance_hourly)
    



# Function to display AWS EC2 instance data
def display_ec2_instance_data(ec2_instance_data):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Basic Information")
        st.write(f"Instance ID: {ec2_instance_data['instance_id']}")
        st.write(f"Instance State: {ec2_instance_data['instance_state']}")
        st.write(f"Instance Type: {ec2_instance_data['instance_type']}")
        st.write(f"Launch Time: {ec2_instance_data['launch_time']}")

    with col2:
        st.subheader("Instance Status")
        st.write(f"Availability Zone: {ec2_instance_data['instance_status']['AvailabilityZone']}")
        st.write(f"Status: {ec2_instance_data['instance_status']['InstanceStatus']['Status']}")

    with col3:
        st.subheader("Network Information")
        for interface in ec2_instance_data['network_interfaces']:
            st.write(f"Interface ID: {interface['NetworkInterfaceId']}")
            st.write(f"Private IP Address: {interface['PrivateIpAddress']}")
            st.write(f"Subnet ID: {interface['SubnetId']}")
            st.write(f"Security Groups: {', '.join(group['GroupName'] for group in interface['Groups'])}")
            st.write("---")


if instance_data:
    display_ec2_instance_data(instance_data[0])







data = []
for x in range(9):
# Create a new data point
    new_data_point = {
        "average": 0,
        "instance_id": "i-0cf85c68cb9355c23",
        "maximum": 0,
        "minimum": 0,
        "sample_count": 0,
        "timestamp": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    }
    time.sleep(1)
    data.append(new_data_point)
min_value=generate_random_value(1,100)
max_value=generate_random_value(1,20)

chart_containe_text = st.empty()
# st.text_input("Maximum",key="max")
# st.text_input("Minimum",key="min")
# st.text_input("Sample Count",key="sc")
# st.text_input("Timestamp",key="ts")
avg_box=st.empty()
sc_box=st.empty()
ts_box=st.empty()
while True:
    # Take max and min of the current hour
    max_value = generate_random_value(abs(max_value-20),min(100,(max_value+20)))
    min_value = generate_random_value(abs(max_value-5),min(20,(max_value+5)))
    sample_count = random.uniform(30, 60)
    # Create a new data point
    new_data_point = {
        "average": (min_value+max_value)//2,
        "instance_id": "i-0cf85c68cb9355c23",
        "maximum": max_value,
        "minimum": min_value,
        "sample_count": sample_count,
        "timestamp": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    }
    time.sleep(1)

    # Write the Average , Max and Min to the Streamlit app

    

    # Append the new data point to the data
    data.append(new_data_point)
    # Remove the oldest data point if the length exceeds a certain limit (e.g., 200)
    if len(data) > 50:
        data.pop(0)
    print(data)
    # Create a DataFrame from the updated data
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Update the chart within the container

    avg_box.text("Average:"+str(new_data_point["average"]))
    sc_box.text("Sample Count:"+str(new_data_point["sample_count"]))
    ts_box.text("Timestamp:"+str(new_data_point["timestamp"]))

    with chart_container:
        

        fig = px.line(df, x=df['timestamp'], y=[df['average'],df['maximum'],df['minimum']], labels={'value': 'Values', 'variable': 'Metrics'},
                    title='AWS EC2 Instance Monitoring', width=1200, height=600)
        st.write(fig)
       
