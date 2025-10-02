# API de Movimentações Bancárias

Este projeto é uma API RESTful desenvolvida em Django e Django REST Framework para gerenciar movimentações bancárias. A aplicação é totalmente containerizada com Docker, utilizando um banco de dados PostgreSQL.

Por ora, a API expõe um endpoint que lista todas as movimentações financeiras cadastradas, simulando um extrato bancário.

## Tecnologias utilizadas

- Backend: Django, Django REST Framework
- Banco de Dados: PostgreSQL
- Containerização: Docker, Docker Compose
- Linguagem: Python 3.11

## Pré-requisitos
Para executar este projeto, você precisará ter instalado em sua máquina:

- Docker
- Docker Compose (geralmente já vem com o Docker Desktop)
- Git (para clonar o repositório)

Nenhuma outra dependência (Python, Django, PostgreSQL) precisa ser instalada localmente. Todo o ambiente é gerenciado pelo Docker.

## Como utilizar o projeto

1. Clonar o Repositório
    - Abra seu terminal e clone o projeto para sua máquina local e navegue até o diretório raiz do projeto.

2.  Iniciar os Containers.
    - Com o Docker em execução na sua máquina, execute o seguinte comando na raiz do projeto:

        ```docker-compose up --build```
    
        - O comando docker-compose up irá ler o arquivo docker-compose.yml, construir a imagem da aplicação Django (web), baixar a imagem do PostgreSQL (db) e iniciar ambos os serviços.

3. Criar as tabelas no bBanco (Migrations)
    - Em um novo terminal, com os containers em execução, rode o comando para que o Django crie as tabelas no banco de dados com base nos modelos definidos:

        ```docker-compose exec web python manage.py migrate```

4. (Opcional) Popular o banco com dados de exemplo
- Para que a API retorne alguns dados, você pode inserir os registros de exemplo diretamente no banco de dados.
Execute o comando abaixo para acessar o cliente psql dentro do container do banco:

    ```docker-compose exec db psql -U admin -d api-db```

    Agora, copie e cole o bloco SQL a seguir no terminal do psql e pressione Enter:

    ```
    -- Inserindo Correntistas
    INSERT INTO core_correntista (nome_correntista, saldo) VALUES ('João Silva', 1500.00);
    INSERT INTO core_correntista (nome_correntista, saldo) VALUES ('Maria Oliveira', 2500.50);
    INSERT INTO core_correntista (nome_correntista, saldo) VALUES ('Carlos Pereira', 800.75);
    ```

    Para sair do psql, digite \q e pressione Enter.

## Testando a API

**1. Exibir o Extrato (GET):**
- Busca todas as movimentações de um correntista específico.
    - URL: ```http://localhost:8000/api/correntistas/1/extrato/```

    - Método: **GET**

- Abra a URL acima diretamente no seu navegador. Você verá uma página com a lista de movimentações do correntista de ID 1, formatada em JSON.

**2. Operação de Depósito (POST):**
- Adiciona um valor ao saldo de um correntista.

    - URL: ```http://localhost:8000/api/depositar/```
    - Método: **POST**

- Acesse a URL http://localhost:8000/api/depositar/ no seu navegador. No campo "Content", cole o seguinte JSON para depositar R$ 200,00 na conta do correntista de ID 1:

    ```
    {
        "correntista_id": 1,
        "valor": "200.00"
    }
    ```
- Clique no botão POST. Você deverá receber uma mensagem de sucesso.

**3. Operação de Saque (POST)**
- Subtrai um valor do saldo de um correntista.

    - ```URL: http://localhost:8000/api/sacar/```
    - Método: **POST**

- Acesse a URL http://localhost:8000/api/sacar/ no seu navegador. No campo "Content", cole o seguinte JSON para sacar R$ 50,00 da conta do correntista de ID 2:

```
{
    "correntista_id": 2,
    "valor": "50.00"
}
```
- Clique no botão POST.

**4. Operação de Pagamento (POST)**
- Funciona como um saque, mas registra uma descrição específica para o débito.

    - URL: ```http://localhost:8000/api/pagar/```
    - Método: **POST**

- Acesse a URL http://localhost:8000/api/pagar/ no seu navegador. No campo "Content", cole o seguinte JSON para pagar uma "Conta de Internet" de R$ 99,90 usando a conta do correntista de ID 1:

```
{
    "correntista_id": 1,
    "valor": "99.90",
    "descricao": "Conta de Internet"
}
```
- Clique no botão POST.

**5. Operação de Transferência (POST)**
- Esta operação transfere um valor entre duas contas, debitando da origem e creditando no destino.

    - URL: ```http://localhost:8000/api/transferir/```
    - Método: **POST**

- Acesse a URL http://localhost:8000/api/transferir/ no seu navegador. No campo "Content", cole o seguinte JSON para transferir R$ 150,00 da conta de origem (ID 2) para a conta de destino (ID 3):

```
{
    "correntista_origem_id": 2,
    "correntista_destino_id": 3,
    "valor": "150.00"
}
```
- Clique no botão POST. A API irá realizar as duas movimentações (débito e crédito) e atualizar o saldo de ambas as contas.

# Parando a aplicação
Para parar todos os containers relacionados ao projeto, pressione Ctrl + C no terminal onde o docker-compose up está rodando, ou execute o seguinte comando no diretório raiz do projeto:

```
docker-compose down
```

Este comando irá parar e remover os containers, mas os dados do banco de dados serão preservados no volume do Docker.