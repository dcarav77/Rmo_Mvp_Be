from app import db

class TechnicalObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255))  # Type of object (e.g., Aircraft Engine, Component)
    control_number = db.Column(db.String(255), unique=True)  # Unique identifier for the object
    status = db.Column(db.String(50))  # Status of the object (e.g., Active, Inactive, Under Maintenance)
    
    # Maintenance Data
    last_maintenance_date = db.Column(db.Date)  # Last date when maintenance was performed
    next_maintenance_due = db.Column(db.Date)  # Date when the next maintenance is due
    
    # OEM Compliance
    current_oem_revision = db.Column(db.String(255))  # Current OEM revision applicable to the object
    revision_compliance_status = db.Column(db.String(50))  # Compliance status with the OEM revision (e.g., Compliant, Non-compliant)
    
    # Relationships for Subsystems
    subsystems = db.relationship('Subsystem', back_populates='technical_object', cascade='all, delete-orphan')  # Subsystems that belong to this technical object
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'control_number': self.control_number, 
            'status': self.status,
            'last_maintenance_date': self.last_maintenance_date.isoformat() if self.last_maintenance_date else None,
            'next_maintenance_due': self.next_maintenance_due.isoformat() if self.next_maintenance_due else None,
            'current_oem_revision': self.current_oem_revision,
            'revision_compliance_status': self.revision_compliance_status,
            'subsystems': [subsystem.to_dict() for subsystem in self.subsystems]  # List of subsystems
        }

# Subsystem Model
class Subsystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # e.g., Fan Module, Core Assembly
    status = db.Column(db.String(50))  # e.g., Removed, In Use, Under Repair
    part_number = db.Column(db.String(255), nullable=False)  # Part number or identifier for the subsystem
    location = db.Column(db.String(255))  # Where the subsystem is located (e.g., shop, external vendor)
    repair_classification = db.Column(db.String(50))  # Repair type (e.g., Internal, External)
    repair_vendor = db.Column(db.String(255))  # External repair vendor (if applicable)
    
    # Foreign Key to link Subsystem to TechnicalObject
    technical_object_id = db.Column(db.Integer, db.ForeignKey('technical_object.id'))
    technical_object = db.relationship('TechnicalObject', back_populates='subsystems')  # Relationship back to TechnicalObject
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'part_number': self.part_number,
            'location': self.location,
            'repair_classification': self.repair_classification,
            'repair_vendor': self.repair_vendor
        }
