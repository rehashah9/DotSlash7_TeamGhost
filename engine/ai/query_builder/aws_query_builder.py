import google.generativeai as genai
import os
import re
import logging
genai.configure(api_key="AIzaSyAZzGyJ9DlHZYjmTJHR33FkmN09LU0W8-Q")


class AWS_Query_Builder_Driver:
    def __init__(self,service:str=None):
        self.genai : genai.GenerativeModel = self.initalize_model()
        self.prompt_parts = self.prompt_generator(service)


    def query(self, query) -> str:
        self.prompt_parts.append(query)
        sql_query = self.generate_sql_query(self.prompt_parts)
        edited_sql_query = self.edit_sql_query(sql_query)
        logging.info(f"Generated SQL Query: {edited_sql_query}")
        return edited_sql_query


    def generate_sql_query(self, prompt_parts: list) -> str:
        total_characters = sum(len(s) for s in prompt_parts)

        print("Total Prompt Size: ", total_characters)

        response = self.genai.generate_content(prompt_parts)
        return response.text

    def initalize_model(self, model_name="gemini-pro") -> genai.GenerativeModel:
        return genai.GenerativeModel(model_name=model_name) 
    
    def prompt_generator(self, service: str = None) -> list:
        if service == None:
            return []
        
        prompt_parts = []
        if service == "aws_ec2":
            all_files = os.listdir(os.path.join(os.path.dirname(__file__), "../data"))

            # Filter files starting with "aws_ec2"
            filtered_files = [filename for filename in all_files if filename.startswith(f"{service}_")]

            prompt_parts.append(self.file_to_text(f"{service}.txt"))
            for filename in filtered_files:
                prompt_parts.append(self.file_to_text(filename))

        return prompt_parts


    def file_to_text(self, file_name:str) -> str:
        with open(os.path.join(os.path.dirname(__file__), f"../data/{file_name}"), "r") as f:
            return f.read()

    def edit_sql_query(self,sql_query):
        table_name_pattern = re.compile(r'\bFROM\s+(\w+)', re.IGNORECASE)
        modified_query = re.sub(table_name_pattern, r'FROM {{connection_name}}.\1', sql_query)
        return modified_query


aws_query_builder = {
    "aws_ec2": AWS_Query_Builder_Driver("aws_ec2"),
}




    

    

    
    

