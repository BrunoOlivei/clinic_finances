"""reorder columns in insurance_claims to put id_claim first

Revision ID: 6cd71b06164f
Revises: 42812ae5297c
Create Date: 2026-02-16 20:18:53.539257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cd71b06164f'
down_revision: Union[str, Sequence[str], None] = '42812ae5297c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


COLUMNS = [
    "id_claim",
    "nr_claim",
    "nr_request",
    "cd_patient",
    "dt_issue",
    "dm_service",
    "st_claim",
    "tp_claim",
    "fg_return",
    "cd_procedure",
    "nm_procedure",
    "qt_procedure",
    "created_at",
    "updated_at",
]


def upgrade() -> None:
    """Upgrade schema.

    PostgreSQL does not support column reordering natively.
    Strategy: create a temp table with the desired order, copy data, swap.
    """
    cols = ", ".join(COLUMNS)

    # 1. Create new table with desired column order (temp constraint names)
    op.execute(
        """
        CREATE TABLE insurance_claims_new (
            id_claim       VARCHAR(36)  NOT NULL,
            nr_claim       VARCHAR(8)   NOT NULL,
            nr_request     VARCHAR(8),
            cd_patient     VARCHAR(30)  NOT NULL,
            dt_issue       DATE         NOT NULL,
            dm_service     TIMESTAMP    NOT NULL,
            st_claim       VARCHAR(20)  NOT NULL,
            tp_claim       VARCHAR(20)  NOT NULL,
            fg_return      BOOLEAN      NOT NULL,
            cd_procedure   VARCHAR(20)  NOT NULL,
            nm_procedure   VARCHAR(200) NOT NULL,
            qt_procedure   INTEGER      NOT NULL,
            created_at     TIMESTAMP    NOT NULL DEFAULT now(),
            updated_at     TIMESTAMP    NOT NULL DEFAULT now(),
            CONSTRAINT insurance_claims_new_pkey PRIMARY KEY (id_claim),
            CONSTRAINT insurance_claims_new_cd_patient_fkey
                FOREIGN KEY (cd_patient) REFERENCES patients(cd_patient)
        );
        """
    )

    # 2. Copy comments
    op.execute("COMMENT ON TABLE insurance_claims_new IS 'Atendimentos realizados no período, importados da operadora São Lucas';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.id_claim IS 'ID único do atendimento concatenando número do atendimento, código do paciente e código do procedimento';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.nr_claim IS 'Número do atendimento (guia)';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.nr_request IS 'Número da solicitação';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.cd_patient IS 'Código do paciente (código do beneficiário)';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.dt_issue IS 'Data de emissão do atendimento';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.dm_service IS 'Data e hora de realização do atendimento';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.st_claim IS 'Status do atendimento (ex: Autorizada, Pendente)';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.tp_claim IS 'Tipo do atendimento (ex: Consulta, Senha)';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.fg_return IS 'Flag indicando se o atendimento é retorno';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.cd_procedure IS 'Código do procedimento realizado';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.nm_procedure IS 'Nome do procedimento realizado';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.qt_procedure IS 'Quantidade do procedimento realizado';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.created_at IS 'Data e hora de criação do registro';")
    op.execute("COMMENT ON COLUMN insurance_claims_new.updated_at IS 'Data e hora da última atualização do registro';")

    # 3. Copy data
    op.execute(f"INSERT INTO insurance_claims_new ({cols}) SELECT {cols} FROM insurance_claims;")

    # 4. Drop old table and rename new one
    op.execute("DROP TABLE insurance_claims;")
    op.execute("ALTER TABLE insurance_claims_new RENAME TO insurance_claims;")

    # 5. Rename constraints to final names
    op.execute("ALTER TABLE insurance_claims RENAME CONSTRAINT insurance_claims_new_pkey TO insurance_claims_pkey;")
    op.execute("ALTER TABLE insurance_claims RENAME CONSTRAINT insurance_claims_new_cd_patient_fkey TO insurance_claims_cd_patient_fkey;")


def downgrade() -> None:
    """Downgrade schema.

    Column order is cosmetic; downgrade is a no-op since the data and
    constraints are identical.
    """
    pass
