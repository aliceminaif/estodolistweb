
# ==========================================
# IMPORTAÇÕES
# ==========================================

# Importa ferramentas do Flask para criar nosso site.
from flask import Flask, render_template, request, session, redirect, flash

# Importa funções responsáveis por consultar e inserir tarefas no banco de dados.
from database import consultar_tarefa, inserir_tarefa

# Importa a biblioteca date para trabalhar com datas.
from datetime import date


# ==========================================
# CONFIGURAÇÃO DO FLASK
# ==========================================

# Cria a aplicação Flask.
# __name__ identifica o módulo atual do Python.
app = Flask(__name__)

# Define uma chave secreta utilizada pelo Flask para proteger sessões
# e permitir o funcionamento de mensagens flash.
app.secret_key = "senai"


# ==========================================
# DADOS DO ADMINISTRADOR
# ==========================================

# E-mail e senha definidos para o administrador.
ADM_EMAIL = "aliceminaif123@gmail.com"
ADM_SENHA = "12345678"

# Lista com as categorias disponíveis para cadastrar tarefas.
CATEGORIAS = [
    "Escola",
    "Trabalho",
    "Projetos",
    "Pessoal",
    "Saúde",
    "Outros"
]


# ==========================================
# FUNÇÃO DE VALIDAÇÃO DE TAREFAS
# ==========================================

# def cria uma função.
# Os parâmetros são os dados que a função receberá.
def validar_tarefa(nome, descricao, categoria, prazo, prioridade):

    # Cria uma lista vazia para armazenar os erros encontrados.
    erros = []

    # Verifica se o nome possui menos de 5 caracteres,
    # mais de 30 caracteres OU se contém somente números.
    # Se pelo menos uma condição for verdadeira, adiciona um erro.
    if len(nome) < 5 or len(nome) > 30 or nome.isdigit():
        erros.append("Nome: de 5 a 30 caracteres, são só números.")

    # Verifica se a descrição ultrapassa 100 caracteres.
    if len(descricao) > 100:
        erros.append("Descrição: No máximo 100 caracteres.")

    # Verifica se a categoria possui menos de 5 caracteres,
    # mais de 30 caracteres OU contém somente números.
    if len(categoria) < 5 or len(categoria) > 30 or categoria.isdigit():
        erros.append("Categoria: de 5 a 30 caracteres, não só números.")

    # Verifica se a prioridade NÃO está entre os valores permitidos.
    # As únicas prioridades aceitas são ALTA, MEDIA e BAIXA.
    if prioridade not in ("ALTA", "MEDIA", "BAIXA"):
        erros.append("Prioridade inválida.")

    # try tenta executar um código que pode gerar um erro.
    try:

        # Converte o texto do prazo em uma data real.
        # O formato esperado é AAAA-MM-DD.
        data = date.fromisoformat(prazo)

        # Compara a data informada com a data atual.
        # Se o prazo for anterior a hoje, adiciona um erro.
        if data < date.today():
            erros.append("Prazo: a data não pode ser no passado.")

    # Se a conversão da data gerar ValueError,
    # o except captura esse erro e adiciona uma mensagem.
    except ValueError:
        erros.append("Prazo: informe uma data válida.")

    # Devolve a lista de erros para quem chamou a função.
    # Se não houver erros, devolve uma lista vazia.
    return erros


# ==========================================
# ROTA PRINCIPAL - PÁGINA INICIAL
# ==========================================

# @app.route("/") associa a função ao endereço principal do site.
@app.route("/")
def index():

    # Verifica se existe a chave "login" na sessão do usuário.
    # Se não existir, significa que ele não está autenticado.
    if "login" not in session:

        # Redireciona o usuário para a página de login.
        return redirect("/login")

    # Se o usuário estiver logado, consulta as tarefas no banco.
    tarefas = consultar_tarefa()

    # Apresenta o arquivo index.html.
    # Envia a variável tarefas para o HTML através de t.
    return render_template("index.html", t=tarefas)


# ==========================================
# ROTA DE LOGIN
# ==========================================

# A rota /login aceita dois métodos:
# GET: acessar a página de login.
# POST: enviar os dados do formulário.
@app.route("/login", methods=["GET", "POST"])
def login():

    # Verifica se o usuário já possui login na sessão.
    if "login" in session:

        # Se já estiver logado, encaminha para a página inicial.
        return redirect("/")

    # Verifica se o método utilizado foi GET.
    if request.method == "GET":

        # Apresenta a página de login.
        return render_template("login.html")

    # Se chegou aqui, significa que a requisição foi POST.

    # Pega o valor enviado pelo campo chamado "email" no formulário.
    email = request.form.get("email")

    # Pega o valor enviado pelo campo chamado "senha".
    senha = request.form.get("senha")

    # Compara o e-mail e a senha informados com os dados do administrador.
    # AND significa que as duas condições precisam ser verdadeiras.
    if email == ADM_EMAIL and senha == ADM_SENHA:

        # Cria uma informação chamada "login" dentro da sessão.
        # O valor True indica que o usuário está autenticado.
        session["login"] = True

        # Redireciona o usuário para a página inicial.
        return redirect("/")

    # Se o e-mail OU a senha estiverem incorretos:
    else:

        # Apresenta novamente o login com uma mensagem de erro.
        return render_template(
            "login.html",
            msgerro="ERRO: Email OU Senha INCORRETOS!"
        )


# ==========================================
# ROTA DE LOGOUT - SAIR DA CONTA
# ==========================================

# Cria a rota /logout.
@app.route("/logout")
def logout():

    # Apaga todas as informações armazenadas na sessão.
    # Isso encerra o login do usuário.
    session.clear()

    # Redireciona para a página de login.
    return redirect("/login")


# ==========================================
# TRATAMENTO DE ERRO 404
# ==========================================

# Registra uma função para tratar erros HTTP 404.
# Esse erro acontece quando uma página ou rota não é encontrada.
@app.errorhandler(404)
def not_found(erro):

    # Apresenta uma página HTML personalizada de erro 404.
    return render_template("erro404.html")


# ==========================================
# ROTA PARA ADICIONAR TAREFAS
# ==========================================

# Cria a rota /adicionar.
# Aceita GET e POST.
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():

    # Se o usuário acessar a rota utilizando GET:
    if request.method == "GET":

        # Apresenta o formulário vazio.
        # categorias envia as categorias disponíveis.
        # dados={} envia um dicionário vazio.
        # erros=[] envia uma lista de erros vazia.
        return render_template(
            "formulario.html",
            categorias=CATEGORIAS,
            dados={},
            erros=[]
        )

    # Se chegou aqui, significa que o formulário foi enviado por POST.

    # Pega o nome da tarefa.
    # get busca o campo e retorna "" se ele não existir.
    # strip remove espaços do início e do final.
    nome_tarefa = request.form.get("nome_tarefa", "").strip()

    # Pega a descrição da tarefa e remove espaços das extremidades.
    descricao = request.form.get("descricao", "").strip()

    # Pega a categoria e remove espaços das extremidades.
    categoria = request.form.get("categoria", "").strip()

    # Pega a data do prazo.
    # Se o campo não existir, retorna uma string vazia.
    data_prazo = request.form.get("data_prazo", "")

    # Pega a prioridade.
    prioridade = request.form.get("prioridade", "")

    # Chama a função de validação criada anteriormente.
    # Envia todos os dados para serem verificados.
    erros = validar_tarefa(
        nome_tarefa,
        descricao,
        categoria,
        data_prazo,
        prioridade
    )

    # Verifica se a lista erros possui algum elemento.
    # Lista com erros = True.
    # Lista vazia = False.
    if erros:

        # Se houver erros, apresenta novamente o formulário.
        # Envia as categorias, os dados preenchidos e as mensagens de erro.
        return render_template(
            "formulario.html",
            categorias=CATEGORIAS,
            dados=request.form,
            erros=erros
        )

    # Se não houver erros, tenta inserir a tarefa no banco de dados.
    # A função inserir_tarefa retorna um resultado verdadeiro ou falso.
    if inserir_tarefa(
        nome_tarefa,
        descricao,
        categoria,
        data_prazo,
        prioridade
    ):

        # Se a inserção funcionar, apresenta uma mensagem de sucesso.
        flash("Tarefa adicionada com sucesso!")

    # Se a inserção não funcionar:
    else:

        # Apresenta uma mensagem informando que houve falha.
        flash("Não foi possível salvar. Confira a conexão com o banco.")

    # Depois de tentar salvar, redireciona para a página inicial.
    return redirect("/")


# ==========================================
# EXECUÇÃO DA APLICAÇÃO
# ==========================================

# Verifica se este arquivo está sendo executado diretamente.
# __name__ == "__main__" indica que o arquivo é o programa principal.
if __name__ == "__main__":

    # Inicia o servidor Flask.
    # debug=True ativa o modo de depuração.
    # port=5000 define a porta utilizada pelo servidor.
    app.run(debug=True, port=5000)
