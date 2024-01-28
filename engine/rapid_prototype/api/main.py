import requests
import os

base_url = os.environ.get('API_ENDPOINT')
org_id = os.environ.get('ORGANIZATION_ID')

def get_profile_connections():
    try:
        url = f"{base_url}/connection"
        response = requests.get(f"{url}?organization_id={org_id}")
        return (response.json())['data']
    except Exception as e:
        print(e)
        return None
    

def get_user_query_stageone(query,connection_name,service):
    try:
        url = f"{base_url}/execute_raw/ai"
        payload = {
            "user_query": query,
            "connection_name": connection_name,
            "service": service
        }
        response = requests.post(url, json=payload)
        return (response.json())['data']
    except Exception as e:
        print(e)
        return None
    


def get_meterics(query, instance_id):
    try:
        url = f"{base_url}/execute_raw/aws"
        payload = { 
            "query": query,
            "variable":{
                "connection_id": "aws_demo",
                "instance_id": instance_id
            }
        }

        response = requests.post(url, json=payload)
        return (response.json())['data']

    except Exception as e:
        print(e)
        return None
    


def execute_raw(query, variable):
    try:
        url = f"{base_url}/execute_raw/aws"
        payload = { 
            "query": query,
            "variable": variable
        }
        print(payload)
        response = requests.post(url, json=payload)
        return (response.json())['data']

    except Exception as e:
        print(e)
        return None
