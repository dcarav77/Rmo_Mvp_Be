from flask import request, jsonify
from app import db
from app.models import TechnicalObject

def init_app(app):
   
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({"message": "Welcome to the Flask API!"})
    
    @app.route('/technical_objects', methods=['GET'])
    def get_technical_objects():
        objects = TechnicalObject.query.all()
        return jsonify([obj.to_dict() for obj in objects])
