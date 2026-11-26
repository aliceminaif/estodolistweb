from flask import Flask, render_template, request, session, redirect, flash
from database import consultar_tarefa, inserir_tarefa 
from datetime import date

app = Flask(__name__)
app.secret_key = "senai" #exigencia para toda vez que se cria a sessão


ADM_EMAIL = "aliceminaif123@gmail.com"
ADM_SENHA = "12345678"
CATEGORIAS = ["Escola", "Trabalho", "Projetos", "Pessoal", "Saúde", "Outros"]

def validar_tarefa(nome,descricao, categoria, prazo, prioridade):
    erros = []
    if len(nome) < 5 or len(nome) > 30 or nome.isdigit():
        erros.append("Nome: de 5 a 30 caracteries, são só números.")
    if len(descricao) > 100:
        erros.append("Descrição: No máximo 100 caracteres.")
    if len(categoria) < 5 or len(categoria) > 30 or categoria.isdigit():
        erros.append("Categoria: de 5 a 30 caracteres, não só números.")
    if prioridade not in ("ALTA", "MEDIA", "BAIXA"):
        erros.append("Prioridade inválida.")
    try:
        data = date.fromisoformat(prazo)
        if data < date.today():
            erros.append("Prazo: a data não pode ser no passado.")

    except ValueError:
        erros.append("Prazo: informe uma data válida.")
    return erros


@app.route("/") # Home page / Pagina inicial
def index():
    if "login" not in session:
        return redirect("/login")

    #usuário logado
    tarefas = consultar_tarefa() 
    return render_template("index.html", t=tarefas)

@app.route("/login", methods=["GET","POST"])
def login():
    if "login" in session:
        return redirect("/")
    if request.method == "GET": 
        return render_template("login.html")
    # POST
    email = request.form.get("email") #pegando a informação que esta no form 
    senha = request.form.get("senha")


    if email == ADM_EMAIL and senha == ADM_SENHA:
        session["login"] = True
        return redirect("/") #redireciona para a rota inicial
    else :
        return render_template("login.html", msgerro = "ERRO: Email OU Senha INCORRETOS!")
    

@app.route("/logout")
def logout():
    session.clear() #apaga a lista da sessão
    return redirect("/login")

@app.errorhandler(404)
def not_found(erro):
    return render_template("erro404.html")

@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "GET":
        return render_template("formulario.html", categorias=CATEGORIAS, dados={}, erros=[])

    # POST: ler o que veio do formulário
    nome_tarefa = request.form.get("nome_tarefa", "").strip()
    descricao = request.form.get("descricao", "").strip()
    categoria = request.form.get("categoria", "").strip()
    data_prazo = request.form.get("data_prazo", "")
    prioridade = request.form.get("prioridade", "")

    erros = validar_tarefa(nome_tarefa, descricao, categoria,
                            data_prazo, prioridade)

    if erros:
        return render_template("formulario.html", categorias=CATEGORIAS,
                                dados=request.form, erros=erros)

    if inserir_tarefa(nome_tarefa, descricao, categoria, data_prazo, prioridade):
        flash("Tarefa adicionada com sucesso!")
    else:
        flash("Não foi possível salvar. Confira a conexão com o banco.")
    return redirect("/")



if __name__ == "__main__": #evita que a pessoa abra o app por outra rota sem ser o host
    app.run(debug=True, port=5000)




