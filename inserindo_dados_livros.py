from psycopg2.errors import ProgrammingError
from conexao_livraria import nova_conexao

sql = '''
    INSERT INTO livros(nome_livro, nome_autor, sexo_autor, numero_paginas,
                       nome_editora, valor_livro, estado_editora,
                       ano_publicacao)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'''

args = (
    ('Cavaleiro Real', 'Ana Claudia', 'F', 465, 'Atlas', 49.9, 'RJ', 2009),
    ('SQL para leigos',	'João Nunes', 'M', 450,	'Addison', 98, 'SP', 2018),
    ('Receitas Caseiras', 'Celia Tavares', 'F', 210, 'Atlas', 45, 'RJ', 2008),
    ('Pessoas Efetivas', 'Eduardo Santos', 'M', 390, 'Beta', 78.99, 'RJ', 2018),
    ('Habitos Saudáveis', 'Eduardo Santos', 'M', 630, 'Beta', 150.98, 'RJ', 2019),
    ('A Casa Marrom', 'Hermes Macedo', 'M', 250, 'Bubba', 60, 'MG', 2016),
    ('Estacio Querido', 'Geraldo Francisco', 'M', 310, 'Insignia', 100, 'ES', 2015),
    ('Pra sempre amigas', 'Leda Silva', 'F', 510, 'Insignia', 78.98, 'ES', 2011),
    ('Copas Inesqueciveis', 'Marco Alcantara', 'M', 200, 'Larson', 130.98, 'RS', 2018),
    ('O poder da mente', 'Clara Mafra', 'F', 120, 'Continental', 56.58, 'SP', 2017)
    )

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.executemany(sql, args)
        conexao.commit()
    except ProgrammingError as e:
        print(f'Erro: {e.pgerror}')
    else:
        print('Os dados foram inseridos')
