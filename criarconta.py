from SolucaoWeb import app, database, bcrypt
from SolucaoWeb.models import Usuario

with app.app_context():

    novo_usuario = Usuario(
        email="ricardo1@gmail.com",
        nome="Ricardo Eletronuclear",
        senha=bcrypt.generate_password_hash("123123").decode("utf-8")
    )

    database.session.add(novo_usuario)

    database.session.commit()

print("Usuário criado com sucesso!")
