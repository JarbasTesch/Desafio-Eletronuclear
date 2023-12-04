from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao = SubmitField("Fazer Login")

class FormOrcamento(FlaskForm):
    area_orcamento = StringField("Área do orçamento", validators=[DataRequired()])
    mes_orcamento = StringField("Mês referente ao orçamento", validators=[DataRequired()])
    dados_orcamento = StringField("Dados relevantes", validators=[DataRequired()])
    valor_orcamento = StringField("Valor do orçamento", validators=[DataRequired()])
    botao_confirmacao_orcamento = SubmitField("Enviar orçamento")

class FormArquivos(FlaskForm):
    arquivo_db = StringField("Arquivo em PDF ou CSV...", validators=[DataRequired()])
    botao_confirmacao_arquivo = SubmitField("Enviar arquivo(s)")


class FormEdicaoOrcamento(FlaskForm):
    area_orcamento = StringField("Nova Área do Orçamento", validators=[DataRequired()])
    mes_orcamento = StringField("Novo Mês referente ao Orçamento", validators=[DataRequired()])
    dados_orcamento = StringField("Novos Dados Relevantes", validators=[DataRequired()])
    valor_orcamento = StringField("Novo Valor do Orçamento", validators=[DataRequired()])
    botao_confirmacao_edicao = SubmitField("Salvar Alterações")