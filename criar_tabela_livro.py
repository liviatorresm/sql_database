from psycopg2.errors import ProgrammingError
from conexao_livraria import nova_conexao

tabela_livros = '''
CREATE TABLE IF NOT EXISTS livros(
    id SERIAL PRIMARY KEY,
    nome_livro VARCHAR(30),
    nome_autor VARCHAR(30),
    sexo_autor CHAR(1),
    numero_paginas integer,
    nome_editora VARCHAR(30),
    valor_livro real,
    estado_editora CHAR(2),
    ano_publicacao integer
)'''

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.execute(tabela_livros)
        conexao.commit()
    except ProgrammingError as e:
        print(f'Erro: {e.pgerror}')
    else:
        print('Tabela inserida')
