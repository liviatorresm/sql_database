from psycopg2.errors import ProgrammingError
from conexao_livraria import nova_conexao

sql = '''
    SELECT nome_livro, estado_editora
    FROM livros
    WHERE sexo_autor = 'M'
'''

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
    except ProgrammingError as e:
        print(f'Erro: {e.pgerror}')
    else:
        print(resultados)
