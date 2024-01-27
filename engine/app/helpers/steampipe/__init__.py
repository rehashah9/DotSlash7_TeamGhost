import json
import os
import subprocess
import logging
import app.helpers.functions as fn
from sqlalchemy import create_engine, text,Engine
from app.helpers.database.db import main_db
from sqlalchemy import create_engine, MetaData, Table, select, update, insert, and_


class Steampipe:
    def __init__(self):
        self.create_connection()
        self.aws_query_dict = json.load(open(os.path.join(os.path.dirname(__file__), "../../queries/aws_steampipe.json"), 'r'))
        self.db : Engine = self.connect_to_db()

    def get_status(self):
        try:
            self.db.execute(text("SELECT 1"))
            return "OK"
        except Exception as e:
            print("Error: ", e)
            return None

    def execute(self, query: str) -> list:
        try:
            if not query:
                return None
            
            result = self.db.execute(text(query))
            print("Query: " + query)
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result]

            return data  
        
        except Exception as e:
            print("Error: ", e)
            return None

    def execute_cli(self, query: str) -> list:
        try:
            if not query:
                return None
            
            result = subprocess.run(["steampipe", "query", query], capture_output=True, text=True)
            
            # Check Error Code
            if result.returncode != 0:
                raise Exception(f"Command {query} returned code {result.returncode}")

            return result.stdout  
        
        except Exception as e:
            print("Error: ", e)
            return None

    def connect_to_db(self) -> Engine:
        try:
            self.start_steampipe_service()
            engine = (create_engine('postgresql://steampipe:7e77_4db6_a095@127.0.0.1:9193/steampipe')).connect()
            return engine
        except Exception as e:
            logging.error("Error at Create Engine: ", e)
            return None
        
    def start_steampipe_service(self):
        try:
            if(self.status_steampipe_service() == "OK"):
                logging.info("Steampipe Service is running!")
                return "OK"
            
            command = ["steampipe", "service", "start", "--database-password", "adminadmin", "--show-password"]

            # Run the subprocess with stdout and stderr redirected to subprocess.PIPE
            process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = process.stdout
            if "Steampipe service is already running" in output:
                return "OK"

            # Check the return code
            return_code = process.returncode

            # If the return code is not 0, raise an exception
            if return_code != 0:
                raise Exception(f"Command {command} returned code {return_code}")

            return "OK"
        except Exception as e:
            print("Error at Start Steampipe Service: ", e)
            return "Error"
        
    def stop_steampipe_service(self):
        try:
            subprocess.run(["steampipe", "service", "stop"], check=True)
            return "OK"
        except Exception as e:
            print("Error at Stop Steampipe Service: ", e)
            return "Error"
        
    def status_steampipe_service(self):
        try:
            command = ["steampipe", "service", "start", "--database-password", "adminadmin", "--show-password"]

            # Run the subprocess with stdout and stderr redirected to subprocess.PIPE
            process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = process.stdout
            if "Steampipe service is already running" in output:
                return "OK"

            # Check the return code
            return_code = process.returncode

            # If the return code is not 0, raise an exception
            if return_code != 0:
                raise Exception(f"Command {command} returned code {return_code}")

            return "OK"
        except Exception as e:
            logging.error("Error at Status Steampipe Service: ", e)
            return "Error"
        
    def update_config_file(self, connections):
        try:
            config_file_path = os.path.expanduser('~/.steampipe/config/aws.spc')
            
            new_config_content = ''
            for connection in connections:
                new_config_content += f'''
                connection "{connection['name']}" {{
                    plugin     = "aws"
                    secret_key = "{connection['secret_key']}"
                    access_key = "{connection['access_key']}"
                    regions    = {json.dumps(connection['regions'])}
                }}
                '''
            with open(config_file_path, 'w') as config_file:
                config_file.write(new_config_content)

            return "OK"
        except Exception as e:
            print(e)
            logging.error(f"Error at Update Config File: {e}")
            return "Error"

    def create_connection(self):
        try:
            connection_table = main_db.metadata.tables['connection']
            engine = main_db.engine

            ## Get All connection of with "connection_plugin" == "aws" and user_id == os.environ['USER_ID']

            org_id = os.environ['ORGANIZATION_ID']
        
            connection_table = main_db.metadata.tables['connection']
            engine = main_db.engine

            # Build and execute the select query
            select_query = connection_table.select().where(and_(connection_table.c.connection_plugin == 'aws', connection_table.c.user_id == org_id))
            
            with engine.connect() as conn:
                result = conn.execute(select_query)
                connections_db = result.fetchall()

            connections = []

            for x in connections_db:

                connection_data = x[3]

                connection = {
                    'name': x[4],
                    'secret_key': connection_data['secret_key'],
                    'access_key': connection_data['access_key'],
                    'regions': connection_data['regions'],
                    'plugin': x[2]
                }

                connections.append(connection)

            self.update_config_file(connections)

            return "OK"
        except Exception as e:
            print(e)
            logging.error(f"Error at Create Connection: {e}")
            return "Error"
    
        
        
    

steampipe = Steampipe()
