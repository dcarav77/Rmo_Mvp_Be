from arango import ArangoClient

# Initialize the ArangoDB client with the correct cloud endpoint
client = ArangoClient(hosts='https://2848c95cbeb4.arangodb.cloud:8529')

# Connect to the "Animals" database with the root credentials
db = client.db(
    'Animals',  # Your database name
    username='root',  # Root username
    password='X4BwfpN64GSWGEk3Iphv'  # Root password
)

# Ensure the Aircraft collection exists, if not, create it
if not db.has_collection('Aircraft'):
    db.create_collection('Aircraft')

# Ensure other collections exist, create if not
if not db.has_collection('Part'):
    db.create_collection('Part')

if not db.has_collection('Technician'):
    db.create_collection('Technician')

if not db.has_collection('MaintenanceEvent'):
    db.create_collection('MaintenanceEvent')

if not db.has_collection('Schedule'):
    db.create_collection('Schedule')

# Ensure edge collections exist
if not db.has_collection('requires_maintenance'):
    db.create_collection('requires_maintenance', edge=True)

if not db.has_collection('assigned_to'):
    db.create_collection('assigned_to', edge=True)

if not db.has_collection('tracks'):
    db.create_collection('tracks', edge=True)

# Check if the Zoo graph exists; if not, create it
if not db.has_graph('Zoo'):
    graph = db.create_graph('Zoo')
    print("Zoo graph created successfully!")
else:
    graph = db.graph('Zoo')

# Ensure the vertex collections are registered in the graph
if not graph.has_vertex_collection('Aircraft'):
    graph.create_vertex_collection('Aircraft')

if not graph.has_vertex_collection('Part'):
    graph.create_vertex_collection('Part')

if not graph.has_vertex_collection('Technician'):
    graph.create_vertex_collection('Technician')

if not graph.has_vertex_collection('MaintenanceEvent'):
    graph.create_vertex_collection('MaintenanceEvent')

if not graph.has_vertex_collection('Schedule'):
    graph.create_vertex_collection('Schedule')

# Ensure the edge definitions are in the graph by checking for existing edge definitions
existing_edge_definitions = {edge['edge_collection'] for edge in graph.edge_definitions()}

# Add edge definition for requires_maintenance if it doesn't already exist
if 'requires_maintenance' not in existing_edge_definitions:
    graph.create_edge_definition(
        edge_collection='requires_maintenance',
        from_vertex_collections=['Aircraft'],
        to_vertex_collections=['MaintenanceEvent']
    )
    print("Edge definition 'requires_maintenance' created.")

# Add edge definition for assigned_to if it doesn't already exist
if 'assigned_to' not in existing_edge_definitions:
    graph.create_edge_definition(
        edge_collection='assigned_to',
        from_vertex_collections=['MaintenanceEvent'],
        to_vertex_collections=['Technician']
    )
    print("Edge definition 'assigned_to' created.")

# Add edge definition for tracks if it doesn't already exist
if 'tracks' not in existing_edge_definitions:
    graph.create_edge_definition(
        edge_collection='tracks',
        from_vertex_collections=['MaintenanceEvent'],
        to_vertex_collections=['Schedule']
    )
    print("Edge definition 'tracks' created.")

# Insert or update data into collections
def upsert_document(collection, document):
    if collection.has(document['_key']):
        collection.update(document)
        print(f"Document with _key '{document['_key']}' updated successfully!")
    else:
        collection.insert(document)
        print(f"Document with _key '{document['_key']}' inserted successfully!")

# Upsert aircraft
aircraft_collection = graph.vertex_collection('Aircraft')
aircraft = {
    '_key': 'aircraft_1',
    'type': 'Aircraft',
    'flight_hours': 1500,
    'registration_number': 'N12345'
}
upsert_document(aircraft_collection, aircraft)

# Upsert maintenance event
maintenance_event_collection = graph.vertex_collection('MaintenanceEvent')
maintenance_event = {
    '_key': 'maintenance_1',
    'type': 'MaintenanceEvent',
    'description': 'Engine Inspection',
    'status': 'Scheduled'
}
upsert_document(maintenance_event_collection, maintenance_event)

# Upsert technician
technician_collection = graph.vertex_collection('Technician')
technician = {
    '_key': 'technician_1',
    'type': 'Technician',
    'name': 'John Doe',
    'role': 'Engineer'
}
upsert_document(technician_collection, technician)

# Upsert schedule
schedule_collection = graph.vertex_collection('Schedule')
schedule = {
    '_key': 'schedule_1',
    'type': 'Schedule',
    'date': '2024-09-25',
    'interval': 100,
    'last_completed': '2024-06-20'
}
upsert_document(schedule_collection, schedule)

# Insert edges (relationships)
requires_maintenance = graph.edge_collection('requires_maintenance')
if not requires_maintenance.has('aircraft_1-maintenance_1'):
    requires_maintenance.insert({
        '_key': 'aircraft_1-maintenance_1',
        '_from': 'Aircraft/aircraft_1',
        '_to': 'MaintenanceEvent/maintenance_1',
        'relationship': 'requires_maintenance'
    })
    print("Edge 'requires_maintenance' inserted successfully!")

assigned_to = graph.edge_collection('assigned_to')
if not assigned_to.has('maintenance_1-technician_1'):
    assigned_to.insert({
        '_key': 'maintenance_1-technician_1',
        '_from': 'MaintenanceEvent/maintenance_1',
        '_to': 'Technician/technician_1',
        'relationship': 'assigned_to'
    })
    print("Edge 'assigned_to' inserted successfully!")

tracks = graph.edge_collection('tracks')
if not tracks.has('maintenance_1-schedule_1'):
    tracks.insert({
        '_key': 'maintenance_1-schedule_1',
        '_from': 'MaintenanceEvent/maintenance_1',
        '_to': 'Schedule/schedule_1',
        'relationship': 'tracks'
    })
    print("Edge 'tracks' inserted successfully!")

print("Nodes and relationships upserted successfully into the Zoo graph!")
