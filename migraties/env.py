import os

from alembic import context
from sqlalchemy import create_engine

from cargohub.database import Basis

url = os.environ["DATABASE_URL"]
if context.is_offline_mode():
    context.configure(url=url, target_metadata=Basis.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    with create_engine(url).connect() as verbinding:
        context.configure(connection=verbinding, target_metadata=Basis.metadata)
        with context.begin_transaction():
            context.run_migrations()
