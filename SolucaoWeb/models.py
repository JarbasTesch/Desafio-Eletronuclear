from SolucaoWeb import login_manager, database
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, nullable=False, unique=True)
    nome = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    arquivos = database.relationship("Arquivos", backref="usuario",lazy=True)
    orcamentos = database.relationship("Orcamentos", backref="usuario",lazy=True)


class Arquivos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    arquivo_db = database.Column(database.String, nullable=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

class Orcamentos(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    area_orcamento = database.Column(database.String, nullable=False)
    mes_orcamento = database.Column(database.String, nullable=False)
    dados_orcamento = database.Column(database.String, nullable=False)
    valor_orcamento = database.Column(database.Float, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)