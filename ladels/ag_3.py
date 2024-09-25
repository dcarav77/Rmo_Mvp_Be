import csv
import uuid  # For generating unique IDs

# Define input and output file paths (these will be user-defined)
input_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/input.csv'  # Generic CSV input file
nodes_output_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/nodes.csv'
edges_output_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/edges.csv'

# Initialize sets and lists to store node and edge data
nodes = set()
edges = []

# User-defined mappings for entities and relationships
node_definitions = [
    {'node_type': 'aircraft', 'fields': ['Control Number', 'Aircraft Make', 'Aircraft Model', 'Difficulty Date'], 'primary_key': 'Control Number'},
    {'node_type': 'engine', 'fields': ['Engine Make', 'Engine Model'], 'primary_key': ['Engine Make', 'Engine Model']},
    {'node_type': 'part', 'fields': ['Part Number', 'Part Name', 'Part Condition', 'Part Location'], 'primary_key': 'Part Number'}
]

# User-defined relationships between entities
relationship_definitions = [
    {'from_type': 'aircraft', 'to_type': 'engine', 'relationship': 'has_engine'},
    {'from_type': 'aircraft', 'to_type': 'part', 'relationship': 'has_part'},
    {'from_type': 'engine', 'to_type': 'part', 'relationship': 'engine_to_part'}
]

# Function to create unique IDs for each node
def create_node_id(node_type, primary_key):
    if isinstance(primary_key, list):
        return f"{node_type}_{'_'.join([str(k).replace('/', '_') for k in primary_key])}"
    return f"{node_type}_{str(primary_key).replace('/', '_')}"

# Function to create nodes and edges dynamically
def create_node_edge_from_csv(file_path, node_definitions, relationship_definitions):
    with open(file_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # Create nodes based on the defined node types
            node_map = {}  # To track created nodes for relationships
            for node_def in node_definitions:
                primary_key = row[node_def['primary_key']] if isinstance(node_def['primary_key'], str) else [row[k] for k in node_def['primary_key']]
                node_id = create_node_id(node_def['node_type'], primary_key)
                
                node = {
                    '_id': node_id,
                    **{field.lower().replace(" ", "_"): row.get(field, 'Unknown') for field in node_def['fields']}
                }
                nodes.add(tuple(node.items()))
                node_map[node_def['node_type']] = node_id
            
            # Create edges based on the relationships
            for rel_def in relationship_definitions:
                from_node = node_map.get(rel_def['from_type'])
                to_node = node_map.get(rel_def['to_type'])
                if from_node and to_node:
                    edge = {
                        '_from': from_node,
                        '_to': to_node,
                        'relationship': rel_def['relationship']
                    }
                    edges.append(edge)

# Process the input file
create_node_edge_from_csv(input_file, node_definitions, relationship_definitions)

# Write nodes to CSV
def write_nodes_to_csv(nodes, filename, fieldnames):
    with open(filename, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for node in nodes:
            writer.writerow(dict(node))

# Write edges to CSV
def write_edges_to_csv(edges, filename):
    with open(filename, mode='w', newline='') as outfile:
        fieldnames = ['_from', '_to', 'relationship']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for edge in edges:
            writer.writerow(edge)

# Define dynamic fieldnames for nodes based on user-defined mappings
node_fieldnames = ['_id'] + [field.lower().replace(" ", "_") for node_def in node_definitions for field in node_def['fields']]

# Write nodes and edges to their respective CSVs
write_nodes_to_csv(nodes, nodes_output_file, node_fieldnames)
write_edges_to_csv(edges, edges_output_file)
