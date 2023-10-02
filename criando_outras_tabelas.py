from psycopg2.errors import ProgrammingError
from conexao_livraria import nova_conexao

tabela_endereco = '''
CREATE TABLE IF NOT EXISTS endereco(
    idEndereco SERIAL PRIMARY KEY,
    rua VARCHAR(30) NOT NULL,
    bairro VARCHAR(30) NOT NULL,
    cidade VARCHAR(30) NOT NULL,
    estado CHAR(2),
    FOREIGN KEY (proprietario_id) REFERENCES Proprietario (proprietario_id)
)'''


tabela_telefone = '''
    CREATE TYPE tipo AS ENUM ('res', 'com', 'cel');
    CREATE TABLE IF NOT EXISTS telefone(
    idTelefone SERIAL PRIMARY KEY,
    tipo tipo,
    numero VARCHAR(10) NOT NULL
    FOREIGN KEY (proprietario_id) REFERENCES Proprietario (proprietario_id)
    )
'''

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.execute(tabela_endereco)
        cursor.execute(tabela_telefone)
        conexao.commit()
    except ProgrammingError as e:
        print(f'Erro: {e.pgerror}')
    else:
        print('Tabela inserida')
