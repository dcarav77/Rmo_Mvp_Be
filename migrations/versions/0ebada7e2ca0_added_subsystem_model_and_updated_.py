"""Added Subsystem model and updated TechnicalObject.

Revision ID: 0ebada7e2ca0
Revises: fcc33dbf4359
Create Date: 2024-09-06 14:10:45.028645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ebada7e2ca0'
down_revision = 'fcc33dbf4359'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subsystem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('part_number', sa.String(length=255), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('repair_classification', sa.String(length=50), nullable=True),
    sa.Column('repair_vendor', sa.String(length=255), nullable=True),
    sa.Column('technical_object_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['technical_object_id'], ['technical_object.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('technical_object', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_oem_revision', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('revision_compliance_status', sa.String(length=50), nullable=True))
        batch_op.create_unique_constraint(None, ['serial_number'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('technical_object', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('revision_compliance_status')
        batch_op.drop_column('current_oem_revision')

    op.drop_table('subsystem')
    # ### end Alembic commands ###
