import csv
import uuid  # Importing uuid for generating unique IDs

# Define input and output file paths
input_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/input.csv'
asset_nodes_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/asset_nodes.csv'
component_nodes_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/component_nodes.csv'
condition_nodes_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/condition_nodes.csv'
edges_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/edges.csv'

# Initialize sets and lists to store node and edge data
asset_nodes = set()
component_nodes = set()
condition_nodes = set()
edges = []

# Read the input CSV
with open(input_file, mode='r') as infile:
    reader = csv.DictReader(infile)
    
    for row in reader:
        # Create an asset node (this could be an aircraft, machine, vehicle, etc.)
        asset_id = row.get('Asset ID', 'Unknown').replace("/", "_")
        asset_type = row.get('Asset Type', 'Unknown')  # e.g., Aircraft, Machine, Vehicle
        asset_model = row.get('Asset Model', 'Unknown')
        asset_node = {
            '_id': f"assets_{asset_id}", 
            'asset_type': asset_type,
            'asset_model': asset_model
        }
        asset_nodes.add(tuple(asset_node.items()))
        
        # Create a component node (e.g., engine, motor, part)
        component_name = row.get('Component Name', 'Unknown')
        component_type = row.get('Component Type', 'Unknown')  # e.g., Engine, Part
        component_id = f"{component_type}_{component_name}".replace("/", "_")
        component_node = {
            '_id': f"components_{component_id}", 
            'component_name': component_name,
            'component_type': component_type
        }
        component_nodes.add(tuple(component_node.items()))
        
        # Create edge between asset and component
        edge_asset_component = {
            '_from': asset_node['_id'],
            '_to': component_node['_id'], 
            'relationship': 'has_component'
        }
        edges.append(edge_asset_component)
        
        # Create a condition node (e.g., WORN, OPERATIONAL, CRACKED)
        condition_state = row.get('Condition State', 'Unknown')  # e.g., WORN, OPERATIONAL
        condition_id = f"conditions_{condition_state}".replace("/", "_")
        condition_node = {
            '_id': f"conditions_{condition_id}",
            'condition_state': condition_state
        }
        condition_nodes.add(tuple(condition_node.items()))
        
        # Create edge between component and condition
        edge_component_condition = {
            '_from': component_node['_id'],
            '_to': condition_node['_id'],
            'relationship': 'has_condition'
        }
        edges.append(edge_component_condition)

# Write nodes to CSVs
def write_nodes_to_csv(nodes, filename, fieldnames):
    with open(filename, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for node in nodes:
            writer.writerow(dict(node))

# Define fieldnames for nodes
asset_fieldnames = ['_id', 'asset_type', 'asset_model']
component_fieldnames = ['_id', 'component_name', 'component_type']
condition_fieldnames = ['_id', 'condition_state']

# Write asset nodes to CSV
write_nodes_to_csv(asset_nodes, asset_nodes_file, asset_fieldnames)

# Write component nodes to CSV
write_nodes_to_csv(component_nodes, component_nodes_file, component_fieldnames)

# Write condition nodes to CSV
write_nodes_to_csv(condition_nodes, condition_nodes_file, condition_fieldnames)

# Write edges to CSV
with open(edges_file, mode='w', newline='') as outfile:
    fieldnames = ['_from', '_to', 'relationship']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for edge in edges:
        writer.writerow(edge)
