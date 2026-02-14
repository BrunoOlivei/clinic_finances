"""rename_patient_columns_to_english

Revision ID: 5898701e0bbe
Revises: 182c5913da7d
Create Date: 2026-02-14 17:28:08.109358

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '5898701e0bbe'
down_revision: Union[str, Sequence[str], None] = '182c5913da7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rename columns
    op.alter_column('patients', 'cd_patiente', new_column_name='cd_patient')
    op.alter_column('patients', 'nm_patiente', new_column_name='nm_patient')
    op.alter_column('patients', 'ds_endereco', new_column_name='ds_address')

    # Recreate indexes with new names
    op.drop_index('idx_patients_cd_patiente', table_name='patients')
    op.drop_index('idx_patients_nm_patiente', table_name='patients')
    op.drop_constraint('patients_cd_patiente_key', 'patients', type_='unique')
    op.create_index(op.f('ix_patients_cd_patient'), 'patients', ['cd_patient'], unique=True)
    op.create_index(op.f('ix_patients_nm_patient'), 'patients', ['nm_patient'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop new indexes
    op.drop_index(op.f('ix_patients_nm_patient'), table_name='patients')
    op.drop_index(op.f('ix_patients_cd_patient'), table_name='patients')

    # Rename columns back
    op.alter_column('patients', 'cd_patient', new_column_name='cd_patiente')
    op.alter_column('patients', 'nm_patient', new_column_name='nm_patiente')
    op.alter_column('patients', 'ds_address', new_column_name='ds_endereco')

    # Recreate original indexes
    op.create_unique_constraint('patients_cd_patiente_key', 'patients', ['cd_patiente'])
    op.create_index('idx_patients_cd_patiente', 'patients', ['cd_patiente'], unique=False)
    op.create_index('idx_patients_nm_patiente', 'patients', ['nm_patiente'], unique=False)
