import csv
import uuid  # Importing uuid for generating unique IDs

input_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/faa_manuals/blah.csv'
aircraft_nodes_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/faa_manuals/aircraft_nodes.csv'
engine_nodes_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/faa_manuals/engine_nodes.csv'
part_nodes_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/faa_manuals/part_nodes.csv'
edges_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/faa_manuals/edges.csv'

# Initialize sets and lists to store node and edge data
aircraft_nodes = set()
engine_nodes = set()
part_nodes = set()
edges = []

# Read the input CSV
with open(input_file, mode='r') as infile:
    reader = csv.DictReader(infile)
    
    for row in reader:
        # Create an aircraft node
        aircraft_id = row.get('Control Number', 'Unknown').replace("/", "_")
        difficulty_date = row.get('Difficulty Date', 'Unknown').replace("/", "_")
        aircraft_node = {
            '_id': f"aircrafts_{aircraft_id}", 
            'aircraft_make': row.get('Aircraft Make', 'Unknown'),
            'aircraft_model': row.get('Aircraft Model', 'Unknown'),
            'difficulty_date': difficulty_date
        }
        aircraft_nodes.add(tuple(aircraft_node.items()))
        
        # Create an engine node
        engine_make = row.get('Engine Make', 'Unknown')
        engine_model = row.get('Engine Model', 'Unknown')
        engine_id = f"{engine_make}_{engine_model}".replace("/", "_")
        engine_node = {
            '_id': f"engines_{engine_id}", 
            'engine_make': engine_make,
            'engine_model': engine_model
        }
        engine_nodes.add(tuple(engine_node.items()))
        
        # Create edge between aircraft and engine
        edge_aircraft_engine = {
            '_from': aircraft_node['_id'],
            '_to': engine_node['_id'], 
            'relationship': 'has_engine'
        }
        edges.append(edge_aircraft_engine)
        
        # Create a part node, generate a unique ID if Part Number is 'Unknown'
        part_id = row.get('Part Number', 'Unknown')
        if part_id:
            part_id = part_id.strip()
        else:
            part_id = str(uuid.uuid4())
                 
        part_node = {
            '_id': f"parts_{part_id}",
            'part_name': row.get('Part Name', ''),
            'part_condition': row.get('Part Condition', ''),
            'part_number': part_id,
            'part_location': row.get('Part Location', '')
        }
        part_nodes.add(tuple(part_node.items()))
        
        # Create edge between aircraft and part
        edge_aircraft_part = {
            '_from': aircraft_node['_id'],
            '_to': part_node['_id'],
            'relationship': 'has_part'
        }
        edges.append(edge_aircraft_part)
        
        # Create edge between engine and part
        edge_enginetopart = {
            '_from': engine_node['_id'],
            '_to': part_node['_id'],
            'relationship': 'engine_to_part'
        }
        edges.append(edge_enginetopart)

# Write nodes to CSVs
def write_nodes_to_csv(nodes, filename, fieldnames):
    with open(filename, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for node in nodes:
            writer.writerow(dict(node))

# Define fieldnames for nodes
aircraft_fieldnames = ['_id', 'aircraft_make', 'aircraft_model', 'difficulty_date']
engine_fieldnames = ['_id', 'engine_make', 'engine_model']
part_fieldnames = ['_id', 'part_name', 'part_condition', 'part_number', 'part_location']

# Write aircraft nodes to CSV
write_nodes_to_csv(aircraft_nodes, aircraft_nodes_file, aircraft_fieldnames)

# Write engine nodes to CSV
write_nodes_to_csv(engine_nodes, engine_nodes_file, engine_fieldnames)

# Write part nodes to CSV
write_nodes_to_csv(part_nodes, part_nodes_file, part_fieldnames)

# Write edges to CSV
with open(edges_file, mode='w', newline='') as outfile:
    fieldnames = ['_from', '_to', 'relationship']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for edge in edges:
        writer.writerow(edge)
