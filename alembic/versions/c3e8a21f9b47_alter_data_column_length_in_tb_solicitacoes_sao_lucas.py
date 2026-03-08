"""alter data column length in tb_solicitacoes_sao_lucas

Revision ID: c3e8a21f9b47
Revises: b1f9f88d502a
Create Date: 2026-03-07 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3e8a21f9b47'
down_revision: Union[str, Sequence[str], None] = 'b1f9f88d502a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('tb_solicitacoes_sao_lucas', 'data',
               existing_type=sa.String(length=10),
               type_=sa.String(length=19),
               comment='Data da abertura da solicitação (formato: dd/mm/yyyy)',
               existing_comment='Data da abertura da solicitação (formato: dd/mm/yyyy)',
               existing_nullable=False,
               schema='brz')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('tb_solicitacoes_sao_lucas', 'data',
               existing_type=sa.String(length=19),
               type_=sa.String(length=10),
               comment='Data da abertura da solicitação (formato: dd/mm/yyyy)',
               existing_comment='Data da abertura da solicitação (formato: dd/mm/yyyy)',
               existing_nullable=False,
               schema='brz')
