from flask import Flask, request, jsonify
from arango import ArangoClient
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

# Connect to ArangoDB
client = ArangoClient(hosts='https://2848c95cbeb4.arangodb.cloud:8529')
db_arango = client.db('Animals', username='root', password='X4BwfpN64GSWGEk3Iphv')

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

#Add or update a part in ArangoDB
@app.route('/parts', methods=['GET', 'POST', 'PUT'])
def upsert_part():
    if request.method == 'GET':
        parts = db_arango.collection('Part').all()
        return jsonify([part for part in parts]), 200
    
    data = request.json
    part_collection = db_arango.collection('Part')

    if request.method == 'POST':  # Add new part
        part_collection.insert({
            '_key': data['part_id'],
            'type': 'Part',
            'name': data['name'],
            'condition': data['condition']
        })
        return jsonify({'message': 'Part added successfully!'}), 201

    if request.method == 'PUT':  # Update existing part
        if part_collection.has(data['part_id']):
            part_collection.update({
                '_key': data['part_id'],
                'name': data['name'],
                'condition': data['condition']
            })
            return jsonify({'message': 'Part updated successfully!'}), 200
        else:
            return jsonify({'error': 'Part not found'}), 404

# Add or update an aircraft in ArangoDB
@app.route('/aircraft', methods=['GET', 'POST', 'PUT'])
def upsert_aircraft():
    if request.method == 'GET':
        aircrafts = db_arango.collection('Aircraft').all()
        return jsonify([aircraft for aircraft in aircrafts]), 200
    
    data = request.json
    aircraft_collection = db_arango.collection('Aircraft')

    if request.method == 'POST':  # Add new aircraft
        aircraft_collection.insert({
            '_key': data['aircraft_id'],
            'type': 'Aircraft',
            'flight_hours': data['flight_hours'],
            'registration_number': data['registration_number']
        })
        return jsonify({'message': 'Aircraft added successfully!'}), 201

    if request.method == 'PUT':  # Update existing aircraft
        if aircraft_collection.has(data['aircraft_id']):
            aircraft_collection.update({
                '_key': data['aircraft_id'],
                'flight_hours': data['flight_hours'],
                'registration_number': data['registration_number']
            })
            return jsonify({'message': 'Aircraft updated successfully!'}), 200
        else:
            return jsonify({'error': 'Aircraft not found'}), 404

# Add or update a technician in ArangoDB
@app.route('/technician', methods=['GET', 'POST', 'PUT'])
def upsert_technician():
    if request.method == 'GET':
        technicians = db_arango.collection('Technician').all()
        return jsonify([tech for tech in technicians]), 200
    
    data = request.json
    technician_collection = db_arango.collection('Technician')

    if request.method == 'POST':  # Add new technician
        technician_collection.insert({
            '_key': data['technician_id'],
            'type': 'Technician',
            'name': data['name'],
            'role': data['role']
        })
        return jsonify({'message': 'Technician added successfully!'}), 201

    if request.method == 'PUT':  # Update existing technician
        if technician_collection.has(data['technician_id']):
            technician_collection.update({
                '_key': data['technician_id'],
                'name': data['name'],
                'role': data['role']
            })
            return jsonify({'message': 'Technician updated successfully!'}), 200
        else:
            return jsonify({'error': 'Technician not found'}), 404

# Add or update a maintenance event in ArangoDB
@app.route('/maintenance_event', methods=['GET', 'POST', 'PUT'])
def upsert_maintenance_event():
    if request.method == 'GET':
        maintenance_events = db_arango.collection('MaintenanceEvent').all()
        return jsonify([event for event in maintenance_events]), 200
    
    data = request.json
    maintenance_event_collection = db_arango.collection('MaintenanceEvent')

    if request.method == 'POST':  # Add new maintenance event
        maintenance_event_collection.insert({
            '_key': data['maintenance_event_id'],
            'type': 'MaintenanceEvent',
            'description': data['description'],
            'status': data['status']
        })
        return jsonify({'message': 'Maintenance event added successfully!'}), 201

    if request.method == 'PUT':  # Update existing maintenance event
        if maintenance_event_collection.has(data['maintenance_event_id']):
            maintenance_event_collection.update({
                '_key': data['maintenance_event_id'],
                'description': data['description'],
                'status': data['status']
            })
            return jsonify({'message': 'Maintenance event updated successfully!'}), 200
        else:
            return jsonify({'error': 'Maintenance event not found'}), 404

# Add or update a schedule in ArangoDB
@app.route('/schedule', methods=['GET', 'POST', 'PUT'])
def upsert_schedule():
    if request.method == 'GET':
        schedules = db_arango.collection('Schedule').all()
        return jsonify([schedule for schedule in schedules]), 200

    data = request.json
    schedule_collection = db_arango.collection('Schedule')

    if request.method == 'POST':  # Add new schedule
        schedule_collection.insert({
            '_key': data['schedule_id'],
            'type': 'Schedule',
            'date': data['date'],
            'interval': data['interval'],
            'last_completed': data['last_completed']
        })
        return jsonify({'message': 'Schedule added successfully!'}), 201

    if request.method == 'PUT':  # Update existing schedule
        if schedule_collection.has(data['schedule_id']):
            schedule_collection.update({
                '_key': data['schedule_id'],
                'date': data['date'],
                'interval': data['interval'],
                'last_completed': data['last_completed']
            })
            return jsonify({'message': 'Schedule updated successfully!'}), 200
        else:
            return jsonify({'error': 'Schedule not found'}), 404

# Trigger maintenance event based on flight hours
@app.route('/trigger_maintenance', methods=['GET'])
def trigger_maintenance():
    aircrafts = db_arango.collection('Aircraft').all() 
    for aircraft in aircrafts:
        if aircraft['flight_hours'] >= 1000:  # Example trigger condition
            create_maintenance_event_for_aircraft(aircraft['_key'])
    return jsonify({'message': 'Maintenance check triggered'}), 200

# Helper function for creating maintenance events
def create_maintenance_event_for_aircraft(aircraft_id):
    maintenance_collection = db_arango.collection('MaintenanceEvent')
    maintenance_collection.insert({
        '_key': f'maintenance_{aircraft_id}',
        'type': 'MaintenanceEvent',
        'description': 'Scheduled maintenance due to flight hours',
        'status': 'Scheduled'
    })

if __name__ == '__main__':
    app.run(debug=True)
