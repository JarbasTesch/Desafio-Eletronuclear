from SolucaoWeb import app, database, bcrypt
from flask import render_template, url_for, redirect, request, flash
from SolucaoWeb.models import Usuario, Arquivos, Orcamentos
from flask_login import login_required, login_user, logout_user, current_user
from SolucaoWeb.forms import FormLogin, FormOrcamento, FormArquivos, FormEdicaoOrcamento
import os
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort

@app.route("/", methods=["GET","POST"])
def homepage():
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario)
            return redirect(url_for("perfilusuario", id=usuario.id))

    return render_template("homepage.html", form=form)

@app.route("/perfil/<id>", methods=["GET", "POST"])
@login_required
def perfilusuario(id):
    if int(id) == current_user.id:
        form_orcamento = FormOrcamento()
        form_arquivos = FormArquivos()
        nome_usuario = current_user.nome

        if request.method == "POST":
            if form_orcamento.validate_on_submit():
                area_orcamento = request.form.get("area_orcamento")
                dados_orcamento = request.form.get("dados_orcamento")
                mes_orcamento = request.form.get("mes_orcamento")

                valor_orcamento_str = request.form.get("valor_orcamento")
                valor_orcamento = float(valor_orcamento_str.replace(',', '.'))

                orcamento = Orcamentos(
                    area_orcamento=area_orcamento,
                    mes_orcamento=mes_orcamento,
                    dados_orcamento=dados_orcamento,
                    valor_orcamento=valor_orcamento,
                    id_usuario=current_user.id
                )

                database.session.add(orcamento)
                database.session.commit()
                return redirect(url_for("perfilusuario", id=current_user.id))

            elif form_arquivos.validate_on_submit():
                arquivo = request.files.get("arquivo_db")
                nome_seguro_arquivo = secure_filename(arquivo.filename)
                #arquivo na pasta:
                caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro_arquivo)
                arquivo.save(caminho)

                # arquivo no bdd:
                arquivo_para_db = Arquivos(
                                            arquivo_db=nome_seguro_arquivo,
                                            id_usuario=current_user.id
                                            )
                database.session.add(arquivo_para_db)
                database.session.commit()

                return redirect(url_for("perfilusuario", id=current_user.id))

        return render_template("usuario.html", nome_usuario=nome_usuario, form_orcamento=form_orcamento, form_arquivos=form_arquivos, id=current_user.id)

    else:
        return redirect(url_for("homepage"))



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/perfil/<id>/meus_dados", methods=["GET", "POST"])
@login_required
def meus_dados(id):
    if int(id) == current_user.id:
        form_orcamento = FormOrcamento()
        form_arquivos = FormArquivos()
        nome_usuario = current_user.nome
        orcamentos = Orcamentos.query.all()
        nomes_arquivos = Arquivos.query.filter_by(id_usuario=current_user.id).all()

        return render_template("meus_dados.html", nome_usuario=nome_usuario, orcamentos=orcamentos, nomes_arquivos=nomes_arquivos, current_user=current_user, form_orcamento=form_orcamento, form_arquivos=form_arquivos)

    else:
        return redirect(url_for("homepage"))


@app.route("/excluir_orcamento/<int:orcamento_id>", methods=["POST"])
@login_required
def excluir_orcamento(orcamento_id):
    print(f"Tentativa de excluir orçamento ID: {orcamento_id}")
    orcamento = Orcamentos.query.get_or_404(orcamento_id)

    if orcamento.usuario != current_user:
        abort(403)

    database.session.delete(orcamento)
    database.session.commit()

    flash("Orçamento excluído com sucesso.", "success")
    return redirect(url_for("meus_dados", id=current_user.id))


@app.route("/excluir_arquivo/<int:arquivo_id>", methods=["POST"])
@login_required
def excluir_arquivo(arquivo_id):
    print(f"Tentativa de excluir arquivo ID: {arquivo_id}")
    arquivo = Arquivos.query.get_or_404(arquivo_id)

    if arquivo.usuario != current_user:
        abort(403)

    database.session.delete(arquivo)
    database.session.commit()

    flash("Arquivo excluído com sucesso.", "success")
    return redirect(url_for("meus_dados", id=current_user.id))


@app.route("/editar_orcamento/<int:orcamento_id>", methods=["GET", "POST"])
@login_required
def editar_orcamento(orcamento_id):

    orcamento = Orcamentos.query.get_or_404(orcamento_id)

    if orcamento.usuario != current_user:
        abort(403)

    form_edicao = FormEdicaoOrcamento(obj=orcamento)

    if form_edicao.validate_on_submit():

        orcamento.area_orcamento = form_edicao.area_orcamento.data
        orcamento.mes_orcamento = form_edicao.mes_orcamento.data
        orcamento.dados_orcamento = form_edicao.dados_orcamento.data
        orcamento.valor_orcamento = form_edicao.valor_orcamento.data

        database.session.commit()

        flash("Orçamento editado com sucesso.", "success")
        return redirect(url_for("perfilusuario", id=current_user.id))

    return render_template("editar_dados.html", form_edicao=form_edicao, orcamento=orcamento)