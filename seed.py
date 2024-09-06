from app import create_app, db
from app.models import TechnicalObject, Subsystem

# Create the Flask app
app = create_app()

# Use app context to interact with the database
with app.app_context():
    # Mock technical object (an engine in this case)
    engine = TechnicalObject(
        name="A320 Engine",
        type="Aircraft Engine",
        serial_number="EN12345",
        status="Active",
        last_maintenance_date="2024-01-01",
        next_maintenance_due="2024-06-01",
        current_oem_revision="REV-2024-01",
        revision_compliance_status="Compliant"
    )

    # Mock subsystems for the engine
    fan_module = Subsystem(
        name="Fan Module",
        status="Under Repair",
        part_number="FM5678",
        location="Vendor Repair Shop",
        repair_classification="External",
        repair_vendor="VendorX Repair"
    )

    core_assembly = Subsystem(
        name="Core Assembly",
        status="In Use",
        part_number="CA7890",
        location="Internal Maintenance Shop",
        repair_classification="Internal"
    )

    # Add subsystems to the engine
    engine.subsystems.append(fan_module)
    engine.subsystems.append(core_assembly)

    # Save the engine and its subsystems to the database
    db.session.add(engine)
    db.session.commit()

    print("Mock data added successfully!")
