import pandas as pd
from datetime import datetime
from app import db
from app.models import TechnicalObject, Subsystem
from sqlalchemy.exc import SQLAlchemyError

print("Script has started successfully")

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
    
    # Disable automatic date parsing in pandas
    df = pd.read_csv(csv_path, dtype=str)

    # Print the first few rows of the CSV to verify data
    print("First few rows of the CSV:")
    print(df.head())  # Ensure the CSV is being read correctly

    # Clean the headers: convert to lowercase, replace spaces, and remove non-alphanumeric characters
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('[^a-z0-9_]+', '', regex=True)

    # Print the cleaned headers to ensure they are correct
    print("Cleaned CSV Headers:", df.columns)

    for index, row in df.iterrows():
        # Use lowercase 'control_number' now that headers are normalized
        control_number = row.get('control_number', None)

        # Debugging: Print control number and difficulty date
        difficulty_date = convert_date_format(row.get('difficulty_date', None))
        print(f"Control Number: {control_number}, Difficulty Date: {difficulty_date}")

        # Ensure control number is valid
        if not control_number or '/' in control_number:
            print(f"Skipping invalid control number: {control_number}")
            continue  # Skip rows with invalid or missing control numbers

        # Use the get method to retrieve values and handle missing data
        aircraft_make = row.get('aircraft_make', 'Unknown Aircraft')
        engine_make = row.get('engine_make', 'Unknown Engine Make')
        part_name = row.get('part_name', 'Unknown Part')
        part_condition = row.get('part_condition', 'Unknown Condition')
        aircraft_model = row.get('aircraft_model', 'Unknown Model')
        engine_model = row.get('engine_model', 'Unknown Engine Model')
        part_number = row.get('part_number', 'DEFAULT_PART_NUMBER')  # Provide a default value if missing
        part_location = row.get('part_location', 'Unknown Location')

        # Check if the TechnicalObject already exists
        existing_object = TechnicalObject.query.filter_by(control_number=control_number).first()

        if not existing_object:
            # Create a new TechnicalObject entry
            new_object = TechnicalObject(
                name=aircraft_make,
                type="Aircraft",
                control_number=control_number,
                status="Active",
                last_maintenance_date=difficulty_date,  # Map difficulty_date to last_maintenance_date
                current_oem_revision="REV-2024-01"
            )
            try:
                db.session.add(new_object)
                db.session.commit()  # Commit to get the new_object ID
                print(f"Inserted new TechnicalObject with control_number: {control_number}")

                # Now, create the Subsystem entry, with the default part_number if necessary
                new_subsystem = Subsystem(
                    name=part_name,
                    status=part_condition,
                    part_number=part_number,  # Use the default value if part_number was missing
                    location=part_location,
                    technical_object_id=new_object.id
                )
                db.session.add(new_subsystem)
                db.session.commit()
                print(f"Inserted new Subsystem for control_number: {control_number}")

            except SQLAlchemyError as e:
                db.session.rollback()  # Rollback in case of error
                print(f"Error inserting TechnicalObject or Subsystem: {e}")

        else:
            print(f"TechnicalObject with control_number {control_number} already exists")

            # Optionally, update existing TechnicalObject or add new Subsystems if part_number is valid
            try:
                new_subsystem = Subsystem(
                    name=part_name,
                    status=part_condition,
                    part_number=part_number,  # Use the default value if part_number was missing
                    location=part_location,
                    technical_object_id=existing_object.id
                )
                db.session.add(new_subsystem)
                db.session.commit()
                print(f"Inserted new Subsystem for existing control_number: {control_number}")
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"Error inserting Subsystem for existing control_number {control_number}: {e}")
    
    db.session.commit()  # Final commit after all iterations
    return "Data processed and inserted into the database."


# Example of calling the function
csv_path = "/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/blah.csv"
process_csv_data(csv_path)
