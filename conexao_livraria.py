from psycopg2 import connect
from contextlib import contextmanager

parametros = dict(
    host='localhost',
    port=5432,
    user='livia',
    password='livia',
    database='livraria'
)


@contextmanager
def nova_conexao():
    # generator usa yield para retornar a conexão
    conexao = connect(**parametros)
    try:
        yield conexao
    finally:
        if conexao and not conexao.closed:
            conexao.close()
