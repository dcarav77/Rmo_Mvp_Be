import random
import string
import time
from arango import ArangoClient

# Initialize the ArangoDB client with the correct cloud endpoint
client = ArangoClient(hosts='https://2848c95cbeb4.arangodb.cloud:8529')

# Connect to the "Animals" database with the root credentials
db = client.db(
    'Animals',  # Your database name
    username='root',  # Root username
    password='X4BwfpN64GSWGEk3Iphv'  # Root password
)

# Ensure collections exist, create if not
collections = ['Aircraft', 'Part', 'Technician', 'MaintenanceEvent', 'Schedule']
for collection_name in collections:
    if not db.has_collection(collection_name):
        db.create_collection(collection_name)
        print(f"Collection {collection_name} created.")
    else:
        print(f"Collection {collection_name} already exists.")

# Ensure edge collections exist
edge_collections = ['requires_maintenance', 'assigned_to', 'tracks']
for edge_collection_name in edge_collections:
    if not db.has_collection(edge_collection_name):
        db.create_collection(edge_collection_name, edge=True)
        print(f"Edge collection {edge_collection_name} created.")
    else:
        print(f"Edge collection {edge_collection_name} already exists.")

# Check if the graph exists; if not, create it
if not db.has_graph('Zoo'):
    graph = db.create_graph('Zoo')
    print("Graph 'Zoo' created.")
else:
    graph = db.graph('Zoo')
    print("Graph 'Zoo' already exists.")

# Ensure vertex collections are registered in the graph
for collection_name in collections:
    if not graph.has_vertex_collection(collection_name):
        graph.create_vertex_collection(collection_name)
        print(f"Vertex collection {collection_name} added to the graph.")
    else:
        print(f"Vertex collection {collection_name} already in the graph.")

# Ensure edge definitions are in the graph by checking for existing edge definitions
existing_edge_definitions = {edge['edge_collection'] for edge in graph.edge_definitions()}

if 'requires_maintenance' not in existing_edge_definitions:
    graph.create_edge_definition(
        edge_collection='requires_maintenance',
        from_vertex_collections=['Aircraft'],
        to_vertex_collections=['MaintenanceEvent']
    )
    print("Edge definition 'requires_maintenance' created.")

if 'assigned_to' not in existing_edge_definitions:
    graph.create_edge_definition(
        edge_collection='assigned_to',
        from_vertex_collections=['MaintenanceEvent'],
        to_vertex_collections=['Technician']
    )
    print("Edge definition 'assigned_to' created.")

if 'tracks' not in existing_edge_definitions:
    graph.create_edge_definition(
        edge_collection='tracks',
        from_vertex_collections=['MaintenanceEvent'],
        to_vertex_collections=['Schedule']
    )
    print("Edge definition 'tracks' created.")

# Helper function to generate random strings
def random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Insert or update documents
def insert_document(collection, document):
    try:
        collection.insert(document)
        print(f"Document with _key '{document['_key']}' inserted into collection {collection.name}.")
    except Exception as e:
        print(f"Error inserting document: {e}")

# Generate random data and insert into collections
for i in range(1, 6):
    timestamp = str(int(time.time()))  # Generate a timestamp to ensure unique keys
    
    print(f"\n--- Inserting dataset {i} ---")
    
    # Random Aircraft with unique key
    aircraft = {
        '_key': f'aircraft_{timestamp}_{i}',  # Unique key using timestamp
        'type': 'Aircraft',
        'flight_hours': random.randint(1000, 5000),
        'registration_number': random_string(6)
    }
    print(f"Inserting aircraft: {aircraft}")
    insert_document(graph.vertex_collection('Aircraft'), aircraft)

    # Random Maintenance Events with unique key
    maintenance_event = {
        '_key': f'maintenance_{timestamp}_{i}',  # Unique key using timestamp
        'type': 'MaintenanceEvent',
        'description': random.choice(['Engine Inspection', 'Tire Replacement', 'Oil Check']),
        'status': random.choice(['Scheduled', 'Completed'])
    }
    print(f"Inserting maintenance event: {maintenance_event}")
    insert_document(graph.vertex_collection('MaintenanceEvent'), maintenance_event)

    # Random Technicians with unique key
    technician = {
        '_key': f'technician_{timestamp}_{i}',  # Unique key using timestamp
        'type': 'Technician',
        'name': random.choice(['John Doe', 'Jane Smith', 'Mike Johnson']),
        'role': random.choice(['Engineer', 'Mechanic'])
    }
    print(f"Inserting technician: {technician}")
    insert_document(graph.vertex_collection('Technician'), technician)

    # Random Schedules with unique key
    schedule = {
        '_key': f'schedule_{timestamp}_{i}',  # Unique key using timestamp
        'type': 'Schedule',
        'date': f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        'interval': random.randint(50, 300),
        'last_completed': f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    }
    print(f"Inserting schedule: {schedule}")
    insert_document(graph.vertex_collection('Schedule'), schedule)

    # Create edges with unique key
    requires_maintenance_edge = {
        '_key': f'aircraft_{timestamp}_{i}-maintenance_{timestamp}_{i}',  # Unique key using timestamp
        '_from': f'Aircraft/aircraft_{timestamp}_{i}',
        '_to': f'MaintenanceEvent/maintenance_{timestamp}_{i}',
        'relationship': 'requires_maintenance'
    }
    print(f"Inserting edge requires_maintenance: {requires_maintenance_edge}")
    insert_document(graph.edge_collection('requires_maintenance'), requires_maintenance_edge)

    assigned_to_edge = {
        '_key': f'maintenance_{timestamp}_{i}-technician_{timestamp}_{i}',  # Unique key using timestamp
        '_from': f'MaintenanceEvent/maintenance_{timestamp}_{i}',
        '_to': f'Technician/technician_{timestamp}_{i}',
        'relationship': 'assigned_to'
    }
    print(f"Inserting edge assigned_to: {assigned_to_edge}")
    insert_document(graph.edge_collection('assigned_to'), assigned_to_edge)

    tracks_edge = {
        '_key': f'maintenance_{timestamp}_{i}-schedule_{timestamp}_{i}',  # Unique key using timestamp
        '_from': f'MaintenanceEvent/maintenance_{timestamp}_{i}',
        '_to': f'Schedule/schedule_{timestamp}_{i}',
        'relationship': 'tracks'
    }
    print(f"Inserting edge tracks: {tracks_edge}")
    insert_document(graph.edge_collection('tracks'), tracks_edge)

    print(f"Dataset {i} inserted successfully.")

print("Random data insertion complete.")
