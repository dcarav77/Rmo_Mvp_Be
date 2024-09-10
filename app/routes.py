from flask import request, jsonify
import os
from app.models import TechnicalObject
from app.utils import process_csv_data  # Import the utility function
from app import db

def init_app(app):
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({"message": "Welcome to the Flask API!"})

    @app.route('/upload_csv', methods=['POST'])
    def upload_csv():
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and file.filename.endswith('.csv'):
            # Save the uploaded file temporarily
            file_path = os.path.join('/tmp', file.filename)  # Save in /tmp or desired directory
            file.save(file_path)
            
            # Call the function to process the CSV and insert data into the database
            result_message = process_csv_data(file_path)
            
            return jsonify({"message": result_message}), 201
        
    @app.route('/technical_objects', methods=['GET'])
    def get_technical_objects():
        technical_objects = TechnicalObject.query.all()

        if not technical_objects:
            return jsonify([]), 200 
        
        result = []
        for obj in technical_objects:
            result.append({
                "id": obj.id,
                "name": obj.name,
                "serial_number": obj.serial_number,
                "status": obj.status,
                "last_maintenance_date": obj.last_maintenance_date,
                "next_maintenance_due": obj.next_maintenance_due,
                "current_oem_revision": obj.current_oem_revision,
                "revision_compliance_status": obj.revision_compliance_status
            })

        return jsonify(result), 200
