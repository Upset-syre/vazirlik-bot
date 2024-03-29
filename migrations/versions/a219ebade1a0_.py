"""empty message

Revision ID: a219ebade1a0
Revises: c49c575347d0
Create Date: 2023-05-31 14:33:48.085340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a219ebade1a0'
down_revision = 'c49c575347d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('text', sa.Column('step5', sa.Text(), nullable=True))
    op.add_column('text', sa.Column('step6', sa.Text(), nullable=True))
    op.add_column('text', sa.Column('step7', sa.Text(), nullable=True))
    op.add_column('text', sa.Column('step8', sa.Text(), nullable=True))
    op.add_column('text', sa.Column('step9', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('text', 'step9')
    op.drop_column('text', 'step8')
    op.drop_column('text', 'step7')
    op.drop_column('text', 'step6')
    op.drop_column('text', 'step5')
    # ### end Alembic commands ###
