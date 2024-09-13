from flask import request, jsonify
import os
from app.models import TechnicalObject, Subsystem  # Import Subsystem model
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
        
        return jsonify({"error": "Invalid file format. Please upload a CSV file."}), 400

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
                "type": obj.type,
                "control_number": obj.control_number,
                "next_maintenance_due": obj.next_maintenance_due,
                "revision_compliance_status": obj.revision_compliance_status,
                "aircraft_make": obj.aircraft_make,
                "aircraft_model": obj.aircraft_model,
                "difficulty_date": obj.difficulty_date 
            })

        return jsonify(result), 200

    @app.route('/subsystems', methods=['GET'])
    def get_subsystems():
        subsystems = Subsystem.query.all()

        if not subsystems:
            return jsonify([]), 200

        result = []
        for subsystem in subsystems:
            result.append({
                "id": subsystem.id,
                "name": subsystem.name,
                "status": subsystem.status,
                "part_number": subsystem.part_number,
                "location": subsystem.location,
                "repair_classification": subsystem.repair_classification,
                "repair_vendor": subsystem.repair_vendor,
                "technical_object_id": subsystem.technical_object_id
            })

        return jsonify(result), 200
