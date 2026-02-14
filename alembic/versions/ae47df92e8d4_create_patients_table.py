"""create_patients_table

Revision ID: ae47df92e8d4
Revises:
Create Date: 2026-02-14 14:01:52.863607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae47df92e8d4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'patients',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('cd_patiente', sa.String(length=30), nullable=False),
        sa.Column('nm_patiente', sa.String(length=200), nullable=False),
        sa.Column('ds_endereco', sa.String(length=300), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cd_patiente')
    )
    op.create_index('idx_patients_cd_patiente', 'patients', ['cd_patiente'])
    op.create_index('idx_patients_nm_patiente', 'patients', ['nm_patiente'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_patients_nm_patiente', table_name='patients')
    op.drop_index('idx_patients_cd_patiente', table_name='patients')
    op.drop_table('patients')
