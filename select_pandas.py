from psycopg2.errors import ProgrammingError
from conexao_livraria import nova_conexao
import pandas as pd

sql = '''
    SELECT nome_autor, sexo_autor, estado_editora, ano_publicacao
    FROM livros
    WHERE sexo_autor = 'F' AND ano_publicacao > 2008
'''

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
    except ProgrammingError as e:
        print(f'Erro: {e.pgerror}')

data = pd.DataFrame(data=resultados, columns=['Autor', 'Sexo', 'Estado', 'Ano'])

print(data)
