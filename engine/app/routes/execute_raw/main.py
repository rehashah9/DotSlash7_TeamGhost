from flask import Blueprint, jsonify, current_app, request
from app.helpers.steampipe import steampipe
from app.helpers.functions import is_sql_query
import json
import os
import logging
import re
excute_raw_app = Blueprint('main', __name__)



@excute_raw_app.route('/aws', methods=['POST'])
def excute_raw_aws():
    aws_query_dict : dict = json.load(open(os.path.join(os.path.dirname(__file__), "../../queries/aws_steampipe.json"), 'r'))
    try:
        body = request.get_json()
        query:str = body['query']
        variables :dict = body['variable']
        
        if not is_sql_query(query=query):
            if not aws_query_dict[query]:
                return jsonify({'error': 'Query not found!'})

            formatted_query = re.sub(r"{{(.*?)}}", lambda x: variables.get(x.group(1), x.group(0)), aws_query_dict[query]["query"])
            alpha = steampipe.execute(formatted_query)
            return jsonify({
                'message': 'Execute Raw Data!',
                'data': alpha
            })
        else:
            if not aws_query_dict[query]:
                return jsonify({'error': 'Query not found!'})
            
            formatted_query = re.sub(r"{{(.*?)}}", lambda x: variables.get(x.group(1), x.group(0)), query)
            return jsonify({
                'message': 'Execute Raw Data!',
                'data': steampipe.execute(formatted_query)
            })
    
    except Exception as e:
        print("Error: ", e)
        return jsonify({'error': 'Error!'})