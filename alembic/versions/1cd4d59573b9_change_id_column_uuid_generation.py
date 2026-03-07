"""change id column UUID generation

Revision ID: 1cd4d59573b9
Revises: b06bac82c554
Create Date: 2026-03-07 17:06:48.621276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cd4d59573b9'
down_revision: Union[str, Sequence[str], None] = 'b06bac82c554'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('tb_atendimentos_sao_lucas', 'id',
               existing_type=sa.VARCHAR(length=36),
               type_=sa.UUID(),
               server_default=sa.text("gen_random_uuid()"),
               existing_comment='Identificador único do registro (UUID)',
               existing_nullable=False,
               postgresql_using='id::uuid',
               schema='brz')
    op.alter_column('tb_atendimentos_sao_lucas', 'id',
               existing_type=sa.VARCHAR(length=36),
               type_=sa.UUID(),
               server_default=sa.text("gen_random_uuid()"),
               existing_comment='Identificador único do registro (UUID)',
               existing_nullable=False,
               postgresql_using='id::uuid',
               schema='slv')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('tb_atendimentos_sao_lucas', 'id',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(length=36),
               server_default=None,
               existing_comment='Identificador único do registro (UUID)',
               existing_nullable=False,
               postgresql_using='id::text',
               schema='slv')
    op.alter_column('tb_atendimentos_sao_lucas', 'id',
               existing_type=sa.UUID(),
               type_=sa.VARCHAR(length=36),
               server_default=None,
               existing_comment='Identificador único do registro (UUID)',
               existing_nullable=False,
               postgresql_using='id::text',
               schema='brz')
