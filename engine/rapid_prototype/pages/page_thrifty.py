import streamlit as st
import time
import json


st.sidebar.subheader("Select a Cloud Provider")
cloud_provider = st.sidebar.selectbox("Cloud Provider", ["AWS", "Azure", "GCP"])


# st.title("Cloud Thrifty")
data = json.load(open("./pages/dummy.json")) 

## Sidebar
st.sidebar.title("Cloud Thrifty")
st.sidebar.header("Observe")
cards_data = {
    "error":{
        "title": "Error",
        "color": "#ff0000"
    },
    "ok":{
        "title": "Ok",
        "color": "#5dbb63"
    },
    "alarm":{
        "title": "Alarm",
        "color": "#ff0000"
    },
    "info":{
        "title": "Info",
        "color": "#0000ff"
    },
    "skip":{
        "title": "Skip",
        "color": "#000000"
    },
    
}
# Steampipe Thrifty Page
def main(current_obj):
    st.title(current_obj['title'])

    columns = st.columns(5)
    alpha_summary_list = list((current_obj['summary']['status']).keys())

    for index, x in enumerate(alpha_summary_list):
        with columns[index]:
            st.markdown(
                f"""
                <div style="background-color:{cards_data[x]['color']}; padding: 10px; border-radius: 10px;">
                    <h4 style="color: white;">{cards_data[x]['title']}: {current_obj['summary']['status'][x]}</h4>
                </div>
                """,unsafe_allow_html=True
            )

    ## horizontal line
    st.markdown("---")
    st.subheader(current_obj['description'])


    ## Streammlit Collapsible Text
    for x in current_obj['controls']:
        with st.expander(f"**{x['title']}**"):
            st.markdown(f"{x['description']}")

            ## Write Severity with bold
            st.markdown("**Severity:** " + x["severity"])
            st.markdown("**Control Id:** " + x["control_id"])

    pass


# Dropdown
if cloud_provider == "AWS":
    st.sidebar.subheader("Select a Service")
    service = st.sidebar.selectbox("Service", ["EC2", "RDS", "Cost Explorer"])
    if service == "EC2":
        st.sidebar.subheader("Select a Benchmark")
        main_data = open("./data/ec2.json","r")
        main_data = json.load(main_data)
        main(main_data['groups'][0])
        benchmark = st.sidebar.selectbox("Benchmark", ["ec2_instance_type", "ec2_instance_type_summary", "ec2_instance_type_summary"])
    
    elif service == "Cost Explorer":
        st.sidebar.subheader("Select a Benchmark")
        main_data = open("./data/rds.json","r")
        main_data = json.load(main_data)
        main(main_data['groups'][0])
        benchmark = st.sidebar.selectbox("Benchmark", ["rds_instance_type", "rds_instance_type_summary", "rds_instance_type_summary"])
    
    elif service == "S3":
        st.sidebar.subheader("Select a Benchmark")
        main_data = open("./data/cost_explorer.json","r")
        main_data = json.load(main_data)
        main(main_data['groups'][0])
        benchmark = st.sidebar.selectbox("Benchmark", ["s3_bucket", "s3_bucket_summary", "s3_bucket_summary"])
