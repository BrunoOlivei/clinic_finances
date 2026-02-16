"""add id_claim as primary key for insurance_claims

Revision ID: 42812ae5297c
Revises: dd26f3c77a69
Create Date: 2026-02-16 20:16:55.115192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42812ae5297c'
down_revision: Union[str, Sequence[str], None] = 'dd26f3c77a69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Add id_claim column as nullable first
    op.add_column(
        'insurance_claims',
        sa.Column(
            'id_claim',
            sa.String(length=36),
            nullable=True,
            comment='ID único do atendimento concatenando número do atendimento, código do paciente e código do procedimento',
        ),
    )

    # 2. Populate id_claim for existing rows: nr_claim + numeric part of cd_patient + cd_procedure
    op.execute(
        """
        UPDATE insurance_claims
        SET id_claim = nr_claim || regexp_replace(cd_patient, '[^0-9]', '', 'g') || cd_procedure
        """
    )

    # 3. Set id_claim as NOT NULL
    op.alter_column('insurance_claims', 'id_claim', nullable=False)

    # 4. Drop old primary key on nr_claim
    op.drop_constraint('insurance_claims_pkey', 'insurance_claims', type_='primary')

    # 5. Create new primary key on id_claim
    op.create_primary_key('insurance_claims_pkey', 'insurance_claims', ['id_claim'])


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Drop primary key on id_claim
    op.drop_constraint('insurance_claims_pkey', 'insurance_claims', type_='primary')

    # 2. Restore primary key on nr_claim
    op.create_primary_key('insurance_claims_pkey', 'insurance_claims', ['nr_claim'])

    # 3. Drop id_claim column
    op.drop_column('insurance_claims', 'id_claim')
