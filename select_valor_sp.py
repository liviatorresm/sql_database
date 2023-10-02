from psycopg2.errors import ProgrammingError
from conexao_livraria import nova_conexao

sql = '''
    SELECT nome_livro, valor_livro, estado_editora
    FROM livros
    WHERE estado_editora = 'SP'
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
