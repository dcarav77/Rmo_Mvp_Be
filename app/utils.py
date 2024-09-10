import pandas as pd
from datetime import datetime
from app import db
from app.models import TechnicalObject, Subsystem

def convert_date_format(date_str):
    """Converts dates in 'MM/DD/YY' or 'MM/DD/YYYY' format to 'YYYY-MM-DD' format."""
    if pd.isna(date_str) or not isinstance(date_str, str):
        return None
    try:
        return datetime.strptime(date_str, '%m/%d/%y').strftime('%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            return None

def process_csv_data(csv_path):
    """Reads the CSV file, processes the data, and inserts it into the database."""
    df = pd.read_csv(csv_path)

    # Clean the headers
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('[^A-Za-z0-9_]+', '', regex=True)
    
    for index, row in df.iterrows():
        control_number = row.get('Control_Number', 'Unknown')
        difficulty_date = convert_date_format(row.get('Difficulty_Date', None))
        aircraft_make = row.get('Aircraft_Make', 'Unknown Aircraft')
        aircraft_model = row.get('Aircraft_Model', 'Unknown Model')
        engine_make = row.get('Engine_Make', 'Unknown Engine Make')
        engine_model = row.get('Engine_Model', 'Unknown Engine Model')

        # Important fields that should have values
        part_name = row.get('Part_Name', 'Unknown Part')
        part_condition = row.get('Part_Condition', 'Unknown Condition')
        
        # Ensure part_number is not NaN or None
        part_number = row.get('Part_Number')
        if pd.isna(part_number) or not part_number:
            part_number = 'Unknown'

        part_location = row.get('Part_Location', 'Unknown Location')

        # Check if the TechnicalObject already exists
        existing_object = TechnicalObject.query.filter_by(serial_number=control_number).first()

        if not existing_object:
            # Create a new TechnicalObject entry
            new_object = TechnicalObject(
                name=aircraft_make,
                type="Aircraft",
                serial_number=control_number,
                status="Active",
                last_maintenance_date=difficulty_date,
                current_oem_revision="REV-2024-01"
            )
            db.session.add(new_object)
            db.session.commit()  # Commit to get the new_object ID

            # Now, create the Subsystem entry
            new_subsystem = Subsystem(
                name=part_name,
                status=part_condition,
                part_number=part_number,  # This should now default to 'Unknown' if missing
                location=part_location,
                technical_object_id=new_object.id
            )
            db.session.add(new_subsystem)
        else:
            # If the object already exists, update or add subsystems
            new_subsystem = Subsystem(
                name=part_name,
                status=part_condition,
                part_number=part_number,  # This should now default to 'Unknown' if missing
                location=part_location,
                technical_object_id=existing_object.id
            )
            db.session.add(new_subsystem)

    db.session.commit()
    return "Data processed and inserted into the database."
