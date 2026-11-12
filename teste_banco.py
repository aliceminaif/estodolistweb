from database import consultar_tarefa

tarefas = consultar_tarefa()
print(len(tarefas), "tarefa(s) no banco")
for tarefa in tarefas:
    print(tarefa)