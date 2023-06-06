"""empty message

Revision ID: c49c575347d0
Revises: 94020e5af467
Create Date: 2023-05-31 14:28:36.982871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c49c575347d0'
down_revision = '94020e5af467'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('application', 'created_at')
    # ### end Alembic commands ###
