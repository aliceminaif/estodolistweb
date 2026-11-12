INSERT INTO tarefa (nomeTarefa, descricao, categoria,
                    dataPrazo, prioridade, status)
VALUES
('Trabalho de História','Capítulo 4 e resumo de 2 páginas','Escola', '2026-12-10', 'ALTA', 'Pendente'),
('Trabalho de portugues','Verbos no passado', 'Escola', '2026-11-26', 'MEDIA', 'Pendente'),
('Estudar para Matemática', 'Revisar equações de 2º grau', 'Escola', '2026-11-28', 'ALTA', 'Pendente'),
('Projeto de Ciências', 'Pesquisar sobre fontes de energia', 'Escola', '2026-12-05', 'ALTA', 'Pendente'),
('Leitura Obrigatória', 'Ler os capítulos 1 e 2 do livro literário', 'Escola', '2026-11-30', 'BAIXA', 'Pendente'),
('Estudar para PSS', 'Matemática, LP', 'Estudo', '2026-11-30', 'ALTA', 'Concluída');

 
SELECT * FROM tarefa;