import sqlalchemy as sa
from alembic import op

revision = "0001_bestellingen"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "bestelling",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("klant_id", sa.BigInteger(), nullable=False),
        sa.Column("magazijn_id", sa.BigInteger(), nullable=False),
        sa.Column("afleverklant_id", sa.BigInteger()),
        sa.Column("factuurklant_id", sa.BigInteger()),
        sa.Column("besteldatum", sa.Date(), nullable=False),
        sa.Column("gewenste_datum", sa.Date()),
        sa.Column("referentie", sa.String()),
        sa.Column("inkoopordernummer", sa.String()),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("verzendnotities", sa.String()),
        sa.Column("aangemaakt_op", sa.DateTime(timezone=True), server_default=sa.func.now(),
                  nullable=False),
        sa.Column("bijgewerkt_op", sa.DateTime(timezone=True), server_default=sa.func.now(),
                  nullable=False),
    )
    op.create_index("ix_bestelling_klant_id", "bestelling", ["klant_id"])
    op.create_table(
        "bestelregel",
        sa.Column("id", sa.BigInteger(), sa.Identity(), primary_key=True),
        sa.Column("bestelling_id", sa.BigInteger(),
                  sa.ForeignKey("bestelling.id", ondelete="CASCADE"), nullable=False),
        sa.Column("artikel_id", sa.String(), nullable=False),
        sa.Column("aantal", sa.BigInteger(), nullable=False),
        sa.Column("stukprijs", sa.Numeric(14, 2)),
        sa.CheckConstraint("aantal > 0", name="ck_bestelregel_aantal"),
        sa.CheckConstraint("stukprijs >= 0", name="ck_bestelregel_stukprijs"),
    )
    op.create_index("ix_bestelregel_bestelling_id", "bestelregel", ["bestelling_id"])


def downgrade():
    op.drop_table("bestelregel")
    op.drop_table("bestelling")
