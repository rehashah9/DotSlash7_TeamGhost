from flask import Blueprint, jsonify, current_app, request
from app.helpers.steampipe import steampipe
import json
import os
import logging
import re
steampipe_app = Blueprint('route_steampipe', __name__)


@steampipe_app.route('/start', methods=['POST'])
def start_steampipe_service():
    try:
        result = steampipe.start_steampipe_service()
        return jsonify({
            "status": result
        })
    except Exception as e:
        print("Error at Start Steampipe Service: ", e)
        return jsonify("Error")
    

@steampipe_app.route('/stop', methods=['POST'])
def stop_steampipe_service():
    try:
        result = steampipe.stop_steampipe_service()
        return jsonify({
            "status": result
        })
    except Exception as e:
        print("Error at Stop Steampipe Service: ", e)
        return jsonify("Error")
    

@steampipe_app.route('/status', methods=['GET'])
def get_status():
    try:
        result = steampipe.get_status()
        return jsonify({
            "status": result
        })
    except Exception as e:
        print("Error at Get Status: ", e)
        return jsonify("Error")