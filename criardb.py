from SolucaoWeb import database, app
from SolucaoWeb.models import Usuario, Arquivos, Orcamentos

with app.app_context():
    database.create_all()