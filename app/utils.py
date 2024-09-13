import pandas as pd
from datetime import datetime
from app import db
from app.models import TechnicalObject, Subsystem
from sqlalchemy.exc import SQLAlchemyError

def convert_date_format(date_str):
    """Converts dates in 'MM/DD/YY' or 'MM/DD/YYYY' format to a datetime.date object."""
    if pd.isna(date_str) or not isinstance(date_str, str):
        return None
    date_str = date_str.strip()  # Strip leading and trailing whitespace
    try:
        # Try MM/DD/YY format
        return datetime.strptime(date_str, '%m/%d/%y').date()
    except ValueError:
        try:
            # Try MM/DD/YYYY format
            return datetime.strptime(date_str, '%m/%d/%Y').date()
        except ValueError:
            print(f"Unrecognized date format: {date_str}")
            return None

def handle_null(value, default=None):
    """Returns default if the value is NaN or an empty string, otherwise returns the value."""
    return default if pd.isna(value) or value == "" else value

def process_csv_data(csv_path):
    """Reads the CSV file, processes the data, and inserts or updates it in the database."""
    try:
        # Read CSV, disabling automatic date parsing in pandas
        df = pd.read_csv(csv_path, dtype=str)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return "Failed to read CSV"

    # Clean the headers: convert to lowercase, replace spaces, and remove non-alphanumeric characters
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('[^a-z0-9_]+', '', regex=True)

    # Loop through each row
    for index, row in df.iterrows():
        control_number = handle_null(row.get('control_number'))
        aircraft_make = handle_null(row.get('aircraft_make'))
        aircraft_model = handle_null(row.get('aircraft_model'))
        engine_make = handle_null(row.get('engine_make'))
        part_name = handle_null(row.get('part_name'))
        part_condition = handle_null(row.get('part_condition'))
        engine_model = handle_null(row.get('engine_model'))
        part_number = handle_null(row.get('part_number'), 'UNKNOWN')  # Provide a default value if missing
        part_location = handle_null(row.get('part_location'))
        difficulty_date = convert_date_format(row.get('difficulty_date'))

        # Log missing fields
        if not control_number:
            print(f"Skipping row with missing control number at index {index}.")
            continue  # Skip rows with missing control numbers

        if difficulty_date is None:
            print(f"Missing or invalid difficulty date for control number {control_number}")
        else:
            print(f"Parsed difficulty date: {difficulty_date}")

        # Check if the TechnicalObject already exists
        existing_object = TechnicalObject.query.filter_by(control_number=control_number).first()

        if not existing_object:
            print(f"Inserting new TechnicalObject: control_number={control_number}, difficulty_date={difficulty_date}, aircraft_make={aircraft_make}, aircraft_model={aircraft_model}")
            new_object = TechnicalObject(
                name=aircraft_make or 'Unknown Aircraft',
                type="Aircraft",
                control_number=control_number,
                aircraft_make=aircraft_make,
                aircraft_model=aircraft_model,
                difficulty_date=difficulty_date  # Make sure the parsed date is assigned here
            )
            try:
                db.session.add(new_object)
                db.session.commit()
                print(f"Inserted: control_number={control_number}, difficulty_date={new_object.difficulty_date}")

                # Create the Subsystem entry
                new_subsystem = Subsystem(
                    name=part_name or 'Unknown Part',
                    status=part_condition or 'Unknown Condition',
                    part_number=part_number,
                    location=part_location or 'Unknown Location',
                    technical_object_id=new_object.id
                )
                db.session.add(new_subsystem)
                db.session.commit()
                print(f"Inserted Subsystem for: control_number={control_number}")

            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"Error inserting TechnicalObject or Subsystem for control_number={control_number}: {e}")

        else:
            # If the object already exists, ensure fields like difficulty_date and aircraft_model are updated if they are missing
            print(f"Updating existing TechnicalObject: control_number={control_number}")
            if not existing_object.difficulty_date and difficulty_date:
                existing_object.difficulty_date = difficulty_date  # Update difficulty date if not set
                print(f"Updated difficulty_date for control_number={control_number}: {difficulty_date}")

            if not existing_object.aircraft_model and aircraft_model:
                existing_object.aircraft_model = aircraft_model  # Update aircraft_model if not set
                print(f"Updated aircraft_model for control_number={control_number}: {aircraft_model}")

            try:
                db.session.commit()  # Commit any updates made to the existing object

                # Optionally, add new Subsystems for existing TechnicalObject
                new_subsystem = Subsystem(
                    name=part_name or 'Unknown Part',
                    status=part_condition or 'Unknown Condition',
                    part_number=part_number,
                    location=part_location or 'Unknown Location',
                    technical_object_id=existing_object.id
                )
                db.session.add(new_subsystem)
                db.session.commit()
                print(f"Inserted Subsystem for existing control_number={control_number}")
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"Error updating TechnicalObject or inserting Subsystem for control_number={control_number}: {e}")

    db.session.commit()  # Final commit after all iterations
    return "Data processed and inserted into the database."


# Example of calling the function
csv_path = "/Users/dustin_caravaglia/Documents/repo/Rmo_Mvp_Be/blah.csv"
result = process_csv_data(csv_path)
print(result)
