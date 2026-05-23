import sys
sys.path.append(".")

from infrastructure.database import engine, Base
from infrastructure import models

print("Criando tabelas no banco de dados...")
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas com sucesso!")