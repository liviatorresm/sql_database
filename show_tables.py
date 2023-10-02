from psycopg2.errors import ProgrammingError
from conexao_livraria import nova_conexao

sql = '''
    SELECT *
    FROM pg_catalog.pg_tables
    WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema'; 
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
