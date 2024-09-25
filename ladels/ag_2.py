import csv
import uuid  # Importing uuid for generating unique IDs

# Define input and output file paths
data_gas_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/data_gas.csv'
data_bulk_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/data_bulk.csv'
data_bulk_time_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/data_bulk_time.csv'
data_wire_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/data_wire.csv'
data_wire_time_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/data_wire_time.csv'
data_arc_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/data_arc.csv'
data_temp_file = '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/data_temp.csv'

asset_nodes = set()
component_nodes = set()
condition_nodes = set()
edges = []

# Function to create nodes and edges from a CSV file
def create_node_edge_from_csv(file_path, node_type, relationship):
    with open(file_path, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            # Create unique ID for the node
            node_id = f"{node_type}_{uuid.uuid4()}"
            node = {'_id': node_id, **row}  # Add all row data to the node
            
            # Add node to the corresponding node set
            if node_type == 'gas':
                asset_nodes.add(tuple(node.items()))
            elif node_type == 'bulk' or node_type == 'wire' or node_type == 'arc':
                component_nodes.add(tuple(node.items()))
            elif node_type == 'temperature':
                condition_nodes.add(tuple(node.items()))
            
            # Create edge
            if relationship:
                edge = {'_from': node_id, '_to': relationship, 'relationship': f'has_{node_type}'}
                edges.append(edge)

# Process each file
create_node_edge_from_csv(data_gas_file, 'gas', None)
create_node_edge_from_csv(data_bulk_file, 'bulk', None)
create_node_edge_from_csv(data_bulk_time_file, 'bulk_time', None)
create_node_edge_from_csv(data_wire_file, 'wire', None)
create_node_edge_from_csv(data_wire_time_file, 'wire_time', None)
create_node_edge_from_csv(data_arc_file, 'arc', None)
create_node_edge_from_csv(data_temp_file, 'temperature', None)

# Write nodes to CSVs
def write_nodes_to_csv(nodes, filename, fieldnames):
    with open(filename, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for node in nodes:
            writer.writerow(dict(node))

# Define fieldnames for nodes (adjust these as per the content of your CSVs)
asset_fieldnames = ['_id', 'gas_type', 'amount', 'time']  # Example for gas
component_fieldnames = ['_id', 'bulk_element', 'amount']  # Example for bulk
condition_fieldnames = ['_id', 'temperature', 'measurement_time']  # Example for temp

# Write nodes and edges to CSV files
write_nodes_to_csv(asset_nodes, '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/asset_nodes.csv', asset_fieldnames)
write_nodes_to_csv(component_nodes, '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/component_nodes.csv', component_fieldnames)
write_nodes_to_csv(condition_nodes, '/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/condition_nodes.csv', condition_fieldnames)

# Write edges to CSV
with open('/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/ladels/edges.csv', mode='w', newline='') as outfile:
    fieldnames = ['_from', '_to', 'relationship']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for edge in edges:
        writer.writerow(edge)
