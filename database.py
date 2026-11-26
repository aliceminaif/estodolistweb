import mysql.connector
from mysql.connector import Error 

def conectar():
    try: 

        conexao = mysql.connector.connect(
        host="localhost", #endereço
        user="root", #usúario 
        password="senai", #senha
        database="estodolist" #database criado
        )

        cursor = conexao.cursor(dictionary=True) #devolve no formato dict
        #retorna duas informações: conexão e cursor
        return conexao, cursor 
    
    except Error as erro:
        print(f"ERRO! Falha ao se conectar com o banco de dados!: {erro}.")
        return None,None

    
def inserir_tarefa(nome_tarefa,descricao,categoria,data_prazo,prioridade):
    conexao, cursor = conectar() 
    if conexao is None:
        return False

    try:
        # %s sql para evitar sql injection
        sql = "INSERT INTO tarefa (nomeTarefa,descricao,categoria,dataPrazo,prioridade) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql,(nome_tarefa,descricao,categoria,data_prazo,prioridade))
        #salva as alterações 
        conexao.commit()
        return True 
    except Error as erro:
        print(f"ERRO! Falha ao inserir os dados: {erro}.")
        return False
    finally: #executa independente se der certo ou não
        cursor.close()
        conexao.close()

#retorna todas astarefas cadastradas no banco de dados
def consultar_tarefa():
    #chama a funcção conectar
    conexao, cursor = conectar()
    if conexao is None: 
        return [] #Lista vazia
    try: #tente
        sql = """
                SELECT 
                    idTarefa AS idtarefa,
                    dataPrazo AS data_prazo,
                    nomeTarefa AS nome_tarefa,
                    status,
                    descricao,
                    categoria,
                    prioridade
                FROM tarefa
                """

        #executa o comando da variável sql
        cursor.execute(sql)

        #Buscar todas as linhas da consulta executada
        tarefas = cursor.fetchall()

        return tarefas

    except Error as erro: #se der erro
        print(f"ERRO! Falha ao listar as terefas: {erro}")
        return[] #retorna lista vazia em caso de erro

    finally: #finalize sempre
        cursor.close()
        conexao.close()


def concluir_tarefa(idtarefa):
    conexao, cursor = conectar()
    if conexao is None :
        return False
    try:
        sql = "UPDATE tarefa SET status = 'Concluída' WHERE idTarefa = %s"
        cursor.execute(sql,(idtarefa,))
        conexao.commit()
        return True

    except Error as erro: #se der erro
            print(f"ERRO! Falha ao listar as terefas: {erro}")
            return[] #retorna lista vazia em caso de erro
    
    finally: #finalize sempre
            cursor.close()
            conexao.close()

def alterar_tarefa(idTarefa):
    conexao, cursor = conectar()
    if conexao is None :
        return False
    try:
        sql = """UPDATE tarefa
        SET 
        nomeTarefa = %s, 
        descricao = %s, 
        prioridade = %s, 
        categoria = %s, 
        dataPrazo = %s 
        WHERE idTarefa = %s"""
        cursor.execute(sql,(nome_tarefa, descricao, prioridade, categoria, data_prazo, idTarefa))
        conexao.commit()
        return True

    except Error as erro: #se der erro
            print(f"ERRO! Falha ao editar a terefas: {erro}")
            return[] #retorna lista vazia em caso de erro
    
    finally: #finalize sempre
            cursor.close()
            conexao.close()

def apagar_tarefa(idTarefa):
    conexao, cursor = conectar()
    if conexao is None :
        return False
    try:
        sql = """DELETE FROM tarefa WHERE idTarefa = %s"""
        cursor.execute(sql,(idTarefa,))
        conexao.commit()
        return True

    except Error as erro: #se der erro
            print(f"ERRO! Falha ao editar a terefas: {erro}")
            return[] #retorna lista vazia em caso de erro
    
    finally: #finalize sempre
            cursor.close()
            conexao.close()


def buscar_tarefa(idtarefa):
    conexao, cursor = conectar()
    if conexao is None:
          return None
    try: 
        sql = """ 
                SELECT idTarefa AS idtarefa, dataPrazo AS data_prazo,   nomeTarefa AS nome_tarefa, status, descricao, categoria, prioridade
                FROM tarefa WHERE idTarefa = %s 
                """

        cursor.execute(sql, (idtarefa,))
        return cursor.fetchone() #Um dicionário, ou none se não existir
    except Error as erro:
        print(f"ERRO! Falha ao buscar a tarefa: {erro}")
        return None
    finally: 
        cursor.close()
        conexao.close()
    
     

