"""Changed some columns to nullable in Athlete and Scout table

Revision ID: fd0a48d091fc
Revises: 148d90d38ea3
Create Date: 2024-09-23 17:58:01.300747

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fd0a48d091fc'
down_revision = '148d90d38ea3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('athletes', schema=None) as batch_op:
        batch_op.alter_column('country',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('state',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('height',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('age',
               existing_type=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('scouts', schema=None) as batch_op:
        batch_op.alter_column('country',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('state',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('height',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('age',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('scouts', schema=None) as batch_op:
        batch_op.alter_column('age',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('height',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('state',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('country',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('athletes', schema=None) as batch_op:
        batch_op.alter_column('age',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('height',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('state',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('country',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###
