from flask import Blueprint, request, make_response, jsonify, abort
from models import Perfil, Usuario
from app import db

rotas_usuario = Blueprint("minhas_rotas", __name__)

def get_perfil(id):
    query = db.select(Perfil).where(Perfil.id == id)
    perfil = db.session.execute(query).scalar()
    return perfil

@rotas_usuario.route("/perfis", methods=['GET', 'POST'])
def perfis():
    if request.method == "GET":
        query = db.select(Perfil)
        perfis = db.session.execute(query).all()
        resultado = []
        for perfil in perfis:
            perfil = {"id": perfil[0].id, "nome": perfil[0].nome}
            resultado.append(perfil)
        return make_response(jsonify(resultado))

    elif request.method == "POST":
        pass
        dados = request.get_json()
        perfil_novo = Perfil(nome=dados['nome'])
        db.session.add(perfil_novo)
        db.session.commit()
        return make_response(jsonify("Perfil inserido com sucesso"), 200)

    else:
        abort(404)

@rotas_usuario.route('/perfil/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def tarefa(id):
    # Obtém o perfil no banco
    perfil = get_perfil(id)
    if perfil is None:
        return make_response(jsonify("Perfil não encontrado!"), 400)
    else:
        if request.method == "GET":
            return make_response(jsonify({"id": perfil.id, "nome": perfil.nome}))

        elif request.method == "PUT":
            dados = request.get_json()
            novo_nome = dados['nome']

            perfil.nome = novo_nome
            db.session.add(perfil)
            db.session.commit()
            return make_response(jsonify("Perfil Editado com sucesso"), 200)

        elif request.method == "DELETE":
            db.session.delete(perfil)
            db.session.commit()
            return make_response(jsonify("Perfil Apagado com sucesso"), 200)
        else:
            abort(400)

@rotas_usuario.route("/usuarios", methods=['GET', 'POST'])
def usuarios():
    if request.method == "GET":
        query = db.select(Usuario, Perfil).join(Perfil.usuarios)
        users = db.session.execute(query)
        resultado = []
        for usuario in users:
            us = {"id": usuario[0].id, "usuario": usuario[0].usuario, "senha": usuario[0].senha, "perfil": {"id": usuario[1].id, "nome": usuario[1].nome}}
            resultado.append(us)
        return make_response(jsonify(resultado))

    elif request.method == "POST":
        dados = request.get_json()
        nome_usuario = dados["usuario"]
        senha = dados["senha"]
        perfil = dados["id_perfil"]
        # Buscar o perfil
        perfil = get_perfil(perfil)
        if perfil is None:
            return make_response(jsonify({"tipo": "ERRO", "mensagem":"Usuário não encontrado"}), 400)
        else:
            us = Usuario(usuario=nome_usuario, senha=senha, perfil=perfil)
            db.session.add(us)
            db.session.commit()
            return make_response(jsonify({"tipo": "SUCESSO", "mensagem": "Usuário inserido com sucesso"}), 200)
    else:
        abort(404)

@rotas_usuario.route('/usuario/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def usuario(id):
    # Obtém o usuario no banco
    query = db.select(Usuario).where(Usuario.id == id)
    user = db.session.execute(query).scalar()
    if user is None:
        return make_response(jsonify("Usuário não encontrado!"), 400)
    else:
        if request.method == "GET":
            return make_response(jsonify({"id": user.id, "usuario": user.usuario, "senha": user.senha, "perfil": {"id": user.perfil.id, "nome": user.perfil.nome}}))

        elif request.method == "PUT":
            dados = request.get_json()
            if "usuario" in dados:
                user.usuario = dados["usuario"]
            if "senha" in dados:
                user.senha = dados["senha"]
            if "id_perfil" in dados:
                perfil = get_perfil(dados['id_perfil'])
                if perfil is not None:
                    user.perfil = perfil
                else:
                    return make_response(jsonify({"tipo": "ERRO", "mensagem": "Perfil não encontrado"}), 400)

            db.session.add(user)
            db.session.commit()
            return make_response(jsonify({"tipo": "SUCESSO", "mensagem": "Usuário editado com sucesso"}), 200)

        elif request.method == "DELETE":
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({"tipo": "SUCESSO", "mensagem": "Usuário deletado com sucesso"}), 200)
        else:
            abort(400)