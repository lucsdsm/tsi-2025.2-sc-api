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

3. Criar as Tabelas no Banco (Migrations)
    - Em um novo terminal, com os containers em execução, rode o comando para que o Django crie as tabelas no banco de dados com base nos modelos definidos:

        ```docker-compose exec web python manage.py migrate```

4. (Opcional) Popular o Banco com Dados de Exemplo
- Para que a API retorne alguns dados, você pode inserir os registros de exemplo diretamente no banco de dados.
Execute o comando abaixo para acessar o cliente psql dentro do container do banco:

    ```docker-compose exec db psql -U admin -d api-db```

    Agora, copie e cole o bloco SQL a seguir no terminal do psql e pressione Enter:

    ```
    -- Inserindo Correntistas
    INSERT INTO core_correntista (nome_correntista, saldo) VALUES ('João Silva', 1500.00);
    INSERT INTO core_correntista (nome_correntista, saldo) VALUES ('Maria Oliveira', 2500.50);
    INSERT INTO core_correntista (nome_correntista, saldo) VALUES ('Carlos Pereira', 800.75);

    -- Inserindo Movimentações
    INSERT INTO core_movimentacao (tipo_operacao, correntista_id, valor_operacao, data_operacao, descricao, correntista_beneficiario_id) 
    VALUES ('C', 1, 500.00, NOW(), 'Depósito em conta', NULL);

    INSERT INTO core_movimentacao (tipo_operacao, correntista_id, valor_operacao, data_operacao, descricao, correntista_beneficiario_id) 
    VALUES ('D', 2, 150.00, NOW(), 'Pagamento: Conta de Luz', NULL);

    INSERT INTO core_movimentacao (tipo_operacao, correntista_id, valor_operacao, data_operacao, descricao, correntista_beneficiario_id) 
    VALUES ('D', 1, 200.00, NOW(), 'Transferência para Maria Oliveira', 2);

    INSERT INTO core_movimentacao (tipo_operacao, correntista_id, valor_operacao, data_operacao, descricao, correntista_beneficiario_id) 
    VALUES ('C', 2, 200.00, NOW(), 'Transferência recebida de João Silva', NULL);
    ```

    Para sair do psql, digite \q e pressione Enter.

## Testando a API
A API agora está pronta para ser testada.

### Endpoint Principal
- Método: GET
- URL: http://localhost:8000/api/movimentacoes/

    Você pode acessar esta URL diretamente no seu navegador ou usar uma ferramenta de API como Postman, Insomnia ou o comando curl no terminal:

    ```curl http://localhost:8000/api/movimentacoes/```

### Resposta esperada
Se você inseriu os dados de exemplo, a resposta deverá ser um JSON similar a este:

```
[
    {
        "id": 1,
        "tipo_operacao_display": "Crédito",
        "valor_operacao": "500.00",
        "data_operacao": "2025-09-26T16:30:00.123456Z",
        "descricao": "Depósito em conta",
        "correntista": {
            "id": 1,
            "nome_correntista": "João Silva"
        },
        "correntista_beneficiario": null
    },
    {
        "id": 2,
        "tipo_operacao_display": "Débito",
        "valor_operacao": "150.00",
        "data_operacao": "2025-09-26T16:30:10.123456Z",
        "descricao": "Pagamento: Conta de Luz",
        "correntista": {
            "id": 2,
            "nome_correntista": "Maria Oliveira"
        },
        "correntista_beneficiario": null
    },
    {
        "id": 3,
        "tipo_operacao_display": "Débito",
        "valor_operacao": "200.00",
        "data_operacao": "2025-09-26T16:30:20.123456Z",
        "descricao": "Transferência para Maria Oliveira",
        "correntista": {
            "id": 1,
            "nome_correntista": "João Silva"
        },
        "correntista_beneficiario": {
            "id": 2,
            "nome_correntista": "Maria Oliveira"
        }
    },
    {
        "id": 4,
        "tipo_operacao_display": "Crédito",
        "valor_operacao": "200.00",
        "data_operacao": "2025-09-26T16:30:30.123456Z",
        "descricao": "Transferência recebida de João Silva",
        "correntista": {
            "id": 2,
            "nome_correntista": "Maria Oliveira"
        },
        "correntista_beneficiario": null
    }
]
```

# Parando a aplicação
Para parar todos os containers relacionados ao projeto, pressione Ctrl + C no terminal onde o docker-compose up está rodando, ou execute o seguinte comando no diretório raiz do projeto:

```
docker-compose down
```

Este comando irá parar e remover os containers, mas os dados do banco de dados serão preservados no volume do Docker.