from psycopg2 import connect
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

parametros = dict(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
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
