"""Updated the Media model to accept nullable entry for either the scout_id or athlete_id

Revision ID: ef2f82ea94c8
Revises: fd0a48d091fc
Create Date: 2024-09-24 21:17:13.151586

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ef2f82ea94c8'
down_revision = 'fd0a48d091fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.alter_column('athlete_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('scout_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.alter_column('scout_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('athlete_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
