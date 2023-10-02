# Interação entre PostgreSQL e Python

## 1. Por que PostegreSQL?

Ao estudar como estabelecer uma comunicação entre um banco de dados e Python, observei que a maioria dos tutoriais e artigos se concentrava no SGBD MySQL. No entanto, entre os sistemas de gerenciamento de banco de dados de código aberto, o segundo mais amplamente utilizado é o [PostgreSQL](https://www.statista.com/statistics/809750/worldwide-popularity-ranking-database-management-systems/). Isso me inspirou a criar este breve tutorial.

## 2. Para começar: Python Enhancement Proposals (PEP)

Os PEPs (Python Enhancement Proposals) são documentos disponíveis para a comunidade Python e funcionam como guias para novos recursos de sintaxe e linguagem, módulos de biblioteca e padronização de convenções de codificação.

Com isso em mente, busquei seguir de perto o [PEP 249](https://peps.python.org/pep-0249/), que trata da API de banco de dados em Python. Em essência, este documento estabelece especificações para criar semelhanças entre os módulos Python usados para acessar bancos de dados, tornando-os mais compreensíveis e facilitando a transição entre diferentes sistemas de gerenciamento de bancos de dados.

## 3. Mão na massa!

### 3.1 Requisitos necessários

* **Instalação do pacote Psycopg**
    O Psycopg [(documentação aqui)](https://www.psycopg.org/docs/index.html) é um adaptador de banco de dados PostgreSQL para APIs construídas com a linguagem Python. Um adaptador é um componente que permite a comunicação de um aplicativo com um SGBD, o intuito é  facilitar a troca de informações e operações, sem a necessidade de mudar de ambientes.

    A instalação se dá como qualquer outro pacote python, através do pip.

    ```
    pip install psycopg2 
    ```

### 3.2 Configurar acesso ao banco de dados

Aqui, criamos um arquivo Python que armazenará os requisitos necessários para a conexão com o banco de dados. Esse arquivo tem o propósito de evitar a repetição de código toda vez que houver a necessidade de interagir com o banco de dados. Além disso, ele garante que a conexão seja fechada adequadamente e que os recursos sejam liberados de forma eficaz.

* **Começamos importando pacotes necessário**

    ```
    from psycopg2 import connect
    from contextlib import contextmanager
    ```
    O módulo connect do psycopg2 encapsula uma sessão de banco de dados. Enquanto isso, o módulo contextlib permite criar um decorator para que possamos acessar o banco de dados através da instrução with, o que nos permite tratar exceções e garantir o encerramento adequado da conexão.

* **Agora passamos os parâmetros para conexão no banco**

    Aqui vamos criar um dicionário onde as chaves são os parâmetros do método connect e os valores, as informações do banco de dados.

    ```
    parametros = dict(
        host='localhost',
        port=5432,
        user='user',
        password='senha',
        database='nome_do_banco'
    )
    ```
   Você pode estar se perguntando: Por que é necessário passar o nome do banco de dados para o método? Não posso simplesmente me conectar ao PostgreSQL e executar o script "CREATE DATABASE..."?

    A resposta é que o PostgreSQL não permite a criação de bancos de dados dentro de um bloco de transação. Portanto, a criação do banco de dados deve ser feita usando a linha de comando psql ou alguma interface gráfica de usuário específica para essa finalidade.

* **Em seguida criamos um decorator com o contextmanager**

    ```
    @contextmanager
    def nova_conexao():
        conexao = connect(**parametros)
        try:
            yield conexao
        finally:
            if conexao and not conexao.closed:
                conexao.close()
    ```

    1. A variável conexao recebe o módulo connect do psycopg2 com os parâmetros previamente definidos.
    2. Tente estabelecer a conexão e, em seguida, retorne a conexão.
    3. Por fim, se a variável conexao existe e não é None E não foi fechada, então a feche.

### 3.3 Tudo pronto!

#### 3.3.1 Vamos iniciar nossa interação com o banco de dados criando uma tabela

* **Primeiro importamos os pacotes necessários e nosso módulo de conexão**

    ```
    from psycopg2.errors import ProgrammingError
    from conexao_livraria import nova_conexao
    ```

* **Agora armazenamos nosso script SQL em uma variável**

    ```
    tabela_livros = '''
    CREATE TABLE IF NOT EXISTS livros(
        id SERIAL PRIMARY KEY,
        nome_livro VARCHAR(30) NOT NULL,
        nome_autor VARCHAR(30) NOT NULL,
        sexo_autor CHAR(1) NOT NULL,
        numero_paginas integer NOT NULL,
        nome_editora VARCHAR(30) NOT NULL,
        valor_livro real NOT NULL,
        estado_editora CHAR(2) NOT NULL,
        ano_publicacao integer NOT NULL
    )'''
    ```

* **Com o script pronto vamos agora conectar ao banco e excutar a criação da tabela**

    ```
    with nova_conexao() as conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(tabela_livros)
            conexao.commit()
            cursor.close()
        except ProgrammingError as e:
            print(f'Erro: {e.pgerror}')
        else:
            print('Tabela inserida.')
    ```

    Aqui, chamamos o módulo nova_conexao() com o bloco with, tentamos estabelecer uma conexão e, caso ocorra algum erro, a mensagem de erro será exibida na tela. Isso facilita a compreensão dos erros e evita saídas extensas e confusas.

#### 3.3.2 Agora vamos inserir algumas informações na nossa tabela

* **Vamos salvar o script na variável**

    ```
    sql = '''
        INSERT INTO livros(nome_livro, nome_autor, sexo_autor, numero_paginas,
                        nome_editora, valor_livro, estado_editora,
                        ano_publicacao)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'''
    ```

* **Vamos passar os dados como argumentos**

    ```
    args = (
        ('Cavaleiro Real', 'Ana Claudia', 'F', 465, 'Atlas', 49.9, 'RJ', 2009),
        ('SQL para leigos', 'João Nunes', 'M', 450,	'Addison', 98, 'SP', 2018),
        ('Receitas Caseiras', 'Celia Tavares', 'F', 210, 'Atlas', 45, 'RJ', 2008),
        ('Pessoas Efetivas', 'Eduardo Santos', 'M', 390, 'Beta', 78.99, 'RJ', 2018),
        ('Habitos Saudáveis', 'Eduardo Santos', 'M', 630, 'Beta', 150.98, 'RJ', 2019)
        )
    ```

* **Agora conectamos com o banco e excutamos o script de inserção**

    ```
    with nova_conexao() as conexao:
        try:
            cursor = conexao.cursor()
            cursor.executemany(sql, args)
            conexao.commit()
            cursor.close()
        except ProgrammingError as e:
            print(f'Erro: {e.pgerror}')
        else:
            print('Os dados foram inseridos')
    ```

    Veja que aqui utilizamos o método executemany do módulo cursor do psycopg2. Dessa forma, podemos inserir várias linhas de comando no script de inserção.


#### 3.3.4 Primeiros select

```
from psycopg2.errors import ProgrammingError
from conexao_livraria import nova_conexao

sql = '''
    SELECT *
    FROM livros
'''

with nova_conexao() as conexao:
    try:
        cursor = conexao.cursor()
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
    except ProgrammingError as e:
        print(f'Erro: {e.pgerror}')
    else:
        print(resultados)
```

O output será uma lista de tuplas:

```
[('João Nunes', 'M', 'SP'), ('Eduardo Santos', 'M', 'RJ'), ('Eduardo Santos', 'M', 'RJ')]
```

#### 3.3.5 Armazenando resultados de um select como data frame com pandas

Também é possível enviar suas consultas SQL para a biblioteca pandas, o que elimina a necessidade de criar arquivos intermediários para iniciar suas análises.

```
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
        try:
            cursor.execute(sql)
            resultados = cursor.fetchall()
            cursor.close()
        finally:
            cursor.close()
    except ProgrammingError as e:
        print(f'Erro: {e.pgerror}')

data = pd.DataFrame(data=resultados, columns=['Autor', 'Sexo', 'Estado', 'Ano'])

print(data)
```

O output será:

id|Autor | Sexo | Estado | Ano
--|------|------|--------|----
0 |Ana Claudia  |  F   |  RJ | 2009
1 |  Leda Silva |  F   |  ES | 2011
2 | Clara Mafra |  F   |  SP | 2017


Espero que o tutorial tenha sido útil e que você tenha encontrado as informações que estava buscando. Se surgirem dúvidas, não hesite em entrar em contato. Além disso, se tiver sugestões para melhorias ou se encontrar algum erro, por favor, fique à vontade para compartilhá-los comigo. Estou aqui para ajudar e aprimorar o conteúdo.

Lívia Pinheiro.