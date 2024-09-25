from app import db

class TechnicalObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aircraft_make = db.Column(db.String(255), nullable=True)  # Re-added aircraft_make
    aircraft_model = db.Column(db.String(255), nullable=True)  # Re-added aircraft_model
    type = db.Column(db.String(255), nullable=True)
    next_maintenance_due = db.Column(db.Date, nullable=True)
    revision_compliance_status = db.Column(db.String(50), nullable=True)
    control_number = db.Column(db.String(255), unique=True, nullable=True)
    difficulty_date = db.Column(db.Date, nullable=True)
    
    # Relationships for Subsystems
    subsystems = db.relationship('Subsystem', back_populates='technical_object', cascade='all, delete-orphan')  # Subsystems that belong to this technical object
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'control_number': self.control_number, 
            'status': self.status,
            'aircraft_make': self.aircraft_make,
            'aircraft_model': self.aircraft_model,
            'next_maintenance_due': self.next_maintenance_due.isoformat() if self.next_maintenance_due else None,
            'current_oem_revision': self.current_oem_revision,
            'revision_compliance_status': self.revision_compliance_status,
            'subsystems': [subsystem.to_dict() for subsystem in self.subsystems]  # List of subsystems
        }

# Subsystem Model
class Subsystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(255), nullable=False) 
    part_condition = db.Column(db.String(50))
    part_number = db.Column(db.String(255), nullable=False)  # Part number or identifier for the subsystem
    part_location = db.Column(db.String(255))
    repair_classification = db.Column(db.String(50))  # Repair type (e.g., Internal, External)
    repair_vendor = db.Column(db.String(255))  # External repair vendor (if applicable)
    
    # Foreign Key to link Subsystem to TechnicalObject
    technical_object_id = db.Column(db.Integer, db.ForeignKey('technical_object.id'))
    technical_object = db.relationship('TechnicalObject', back_populates='subsystems')  # Relationship back to TechnicalObject
    
    def to_dict(self):
        return {
            'id': self.id,
            'part_name': self.part_name, 
            'part_condition': self.part_condition,
            'part_number': self.part_number,
            'part_location': self.part_location,
            'repair_classification': self.repair_classification,
            'repair_vendor': self.repair_vendor
        }
