# API de Movimentações Bancárias

Este projeto é uma API RESTful desenvolvida em Django e Django REST Framework para gerenciar movimentações bancárias. A aplicação é totalmente containerizada com Docker, utilizando um banco de dados PostgreSQL.

Esta versão (v3) implementa uma autenticação segura baseada em Token (TokenAuthentication). Todos os endpoints de operações financeiras são protegidos, permitindo que apenas usuários autenticados acessem e gerenciem seus próprios dados.

## Tecnologias utilizadas

- Backend: Django, Django REST Framework
- Autenticação: DRF Token Authentication
- Banco de Dados: PostgreSQL
- Containerização: Docker, Docker Compose
- Linguagem: Python 3.11

## Pré-requisitos
Para executar este projeto, você precisará ter instalado em sua máquina:

- Docker
- Docker Compose (geralmente já vem com o Docker Desktop)
- Git (para clonar o repositório)
- Uma ferramenta de cliente de API, como Postman ou Insomnia. (Necessário para testar a API autenticada).

Nenhuma outra dependência (Python, Django, PostgreSQL) precisa ser instalada localmente. Todo o ambiente é gerenciado pelo Docker.

## Como utilizar o projeto

1. Clonar o Repositório
    - Abra seu terminal e clone o projeto para sua máquina local e navegue até o diretório raiz do projeto.

2.  Iniciar os Containers.
    - Com o Docker em execução na sua máquina, execute o seguinte comando na raiz do projeto:

        ```docker-compose up --build```
    
        - O comando docker-compose up irá ler o arquivo docker-compose.yml, construir a imagem da aplicação Django (web), baixar a imagem do PostgreSQL (db) e iniciar ambos os serviços.

3. Criar as tabelas no banco (migrations)
    - Em um novo terminal, com os containers em execução, rode o comando para que o Django crie as tabelas no banco de dados com base nos modelos definidos:

        ```docker-compose exec web python manage.py migrate```

4. Criar Usuários e Contas (Novo Fluxo)
- Como a API agora é segura, precisamos criar logins de usuário e associá-los às suas respectivas contas de correntista.

    4.1 Crie os usuários
    - Vamos criar dois usuários de exemplo (joao e maria). Você será solicitado a definir uma senha para cada um.

    ###### Crie o primeiro usuário
    ```docker-compose exec web python manage.py createsuperuser```

    ###### Crie o segundo usuário
    ```docker-compose exec web python manage.py createsuperuser```
    <br> <br>

    4.2 Crie as contas de correntista (via Admin) <br>
    - 4.2.1: Acesse a interface de administração do Django no seu navegador: http://localhost:8000/admin/
    - 4.2.2: Faça login com o primeiro usuário que você criou (ex: joao).
    - 4.2.3: Na seção "CORE", clique em "Correntistas" e depois em "ADD CORRENTISTA".
    - 4.2.4: Preencha os campos com os dados: 
        - User: Selecione o usuário joao na lista.
        - Nome correntista: João Silva
        - Saldo: 1500.00
        - Clique em "Save".
    - 4.2.5: Faça logout (canto superior direito), e faça login com o segundo usuário (ex: maria).
    - 4.2.6: Repita o processo: vá em "Correntistas", clique em "ADD CORRENTISTA":
        - User: Selecione o usuário maria.
        - Nome correntista: Maria Oliveira
        - Saldo: 2500.00
        - Clique em "Save".

    Ao salvar, anote o ID de cada correntista (a URL no admin irá mostrar, ex: .../core/correntista/2/change/). Vamos assumir que Maria é a Correntista de ID 2.

## Testando a API

Todos os endpoints de operações agora são protegidos. O teste deve ser feito com um cliente de API (Postman, Insomnia) e segue um fluxo de 2 etapas:

1. Obter um Token de Autenticação.
2. Usar esse Token para acessar os endpoints protegidos. <br> <br>

**Etapa 1: Obter seu Token de Autenticação**
- Para se autenticar como joao, envie uma requisição POST para o endpoint de login.
    - Método: **POST**
    - URL: ```http://localhost:8000/api/api-token-auth/```
    - Corpo (Body) JSON:
        ```
        {
            "username": "joao", 
            "password": "sua_senha_aqui"
        }
        ```

    A API irá responder com seu token de acesso:
    - Resposta (Response) JSON:
        ```
        {
            "token": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
        }
        ```

    Copie este valor do token. Ele será usado em todas as requisições seguintes.

**Etapa 2: Acessar os Endpoints Protegidos**
- Para todas as requisições abaixo, você deve adicionar um Cabeçalho (Header) de autenticação. A API saberá quem você é (ex: joao) através deste token.

    - Header Key: ```Authorization```
    - Header Value: ```Token a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2```


### 1. Exibir o Extrato (GET)
Busca o extrato de movimentações do usuário autenticado (dono do token).

- URL: ```http://localhost:8000/api/extrato/```
- Método: ```GET```
- Cabeçalho (Header): 
    - Header Key: ```Authorization```
    - Header Value: ```Token a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2```

### 2. Operação de Depósito (POST)
Adiciona um valor ao saldo do usuário autenticado.

- URL: ```http://localhost:8000/api/depositar/```
- Método: ```POST```
- Cabeçalho (Header): 
    - Header Key: ```Authorization```
    - Header Value: ```Token a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2```
- Corpo (Body) JSON: <br> <br>
    ```
    {
        "valor": 200.00
    }
    ```

### 3. Operação de Saque (POST)
Subtrai um valor do saldo do usuário autenticado.

- URL: ```http://localhost:8000/api/sacar/```
- Método: ```POST```
- Cabeçalho (Header): 
    - Header Key: ```Authorization```
    - Header Value: ```Token a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2```
- Corpo (Body) JSON: <br> <br>
    ```
    {
        "valor": "50.00"
    }
    ```

### 4. Operação de Pagamento (POST)
Subtrai um valor do saldo do usuário autenticado.

- URL: ```http://localhost:8000/api/pagar/```
- Método: ```POST```
- Cabeçalho (Header): 
    - Header Key: ```Authorization```
    - Header Value: ```Token a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2```
- Corpo (Body) JSON: <br> <br>
    ```
    {
        "valor": "99.90",
        "descricao": "Conta de Internet"
    }
    ```

### 5. Operação de Transferência (POST)
Transfere um valor do usuário autenticado (origem) para outro correntista (destino).

- URL: ```http://localhost:8000/api/transferir/```
- Método: ```POST```
- Cabeçalho (Header): 
    - Header Key: ```Authorization```
    - Header Value: ```Token a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2```
- Corpo (Body) JSON: <br> <br>
    ```
    {
        "correntista_destino_id": 2,
        "valor": "150.00"
    }
    ```
    A API irá debitar 150.00 da conta do joao e creditar na conta da maria.

## Parando a aplicação
Para parar todos os containers relacionados ao projeto, execute o seguinte comando no diretório raiz:

```
docker-compose down
```

Este comando irá parar e remover os containers. Se quiser apagar também o volume do banco de dados (recomeçar do zero), use ```docker-compose down -v```.