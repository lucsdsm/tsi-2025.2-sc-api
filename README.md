# **API de Movimentações Bancárias & Frontend React**

Este projeto é uma aplicação full-stack desenvolvida com Django (backend) e React (frontend). A aplicação simula um sistema bancário simples, permitindo que utilizadores se autentiquem, visualizem os seus extratos e realizem operações financeiras como levantamentos, depósitos, pagamentos e transferências.

A aplicação é totalmente contentorizada com Docker, utilizando uma base de dados PostgreSQL, o que simplifica enormemente o processo de configuração e execução.


## **Tecnologias Utilizadas**

- **Frontend:** React

- **Backend:** Django, Django REST Framework

- **Autenticação:** DRF Token Authentication

- **Base de Dados:** PostgreSQL

- **Contentorização:** Docker, Docker Compose

- **Linguagem:** Python 3.11, JavaScript (ES6+)


## **Pré-requisitos**

Para executar este projeto, precisará de ter instalado na sua máquina:

- Docker

- Docker Compose (geralmente já vem com o Docker Desktop)

- Git (para clonar o repositório)

Nenhuma outra dependência (Python, Node.js, PostgreSQL, etc.) precisa de ser instalada localmente. Todo o ambiente é gerido pelo Docker.


## **Como Executar o Projeto**

Siga os passos abaixo para configurar e executar a aplicação. A configuração inicial dos utilizadores de teste é feita **automaticamente**.


### **1. Clonar o Repositório**

Abra o seu terminal, clone o projeto para a sua máquina local e navegue até ao diretório raiz.


### **2. Iniciar os Contentores**

Com o Docker em execução na sua máquina, execute o seguinte comando na raiz do projeto para construir as imagens e iniciar os três serviços (base de dados, backend e frontend) em segundo plano:

```
docker-compose up --build -d
```


### **3. Criar Tabelas e Utilizadores de Teste (Configuração Automática)**

Execute o comando migrate. Este único comando irá criar todas as tabelas necessárias na base de dados e, em seguida, irá popular a base de dados com dois utilizadores de teste (joao e maria) e as suas respetivas contas bancárias.

```
docker-compose exec backend python manage.py migrate
```

A configuração está completa! A aplicação backend está a ser executada em http\://localhost:8000 e o frontend em http\://localhost:3000.


## **Testar a Aplicação**

Aceda à interface web do projeto no seu navegador:

- **URL:** http\://localhost:3000

Para testar, utilize um dos utilizadores que foram criados automaticamente pelo processo de migração:

```
Utilizador: joao

Senha: 123456
```

```
Utilizador: maria

Senha: 123456
```

Após o login, será redirecionado para o Dashboard, onde poderá visualizar o extrato e utilizar os formulários para testar todas as operações da API (depósito, levantamento, pagamento e transferência) através da interface gráfica.


## **Arquitetura da API e Fluxo de Requisições**

A aplicação segue uma arquitetura de **Single Page Application (SPA)**, onde o frontend (React) é completamente desacoplado do backend (Django). A comunicação entre eles é feita exclusivamente através de uma API RESTful.

\[Frontend React (Porta 3000)] <--- (Requisições HTTP/JSON) ---> \[Backend Django (Porta 8000)]


### **1. Autenticação: Obtendo o Token de Acesso**

O primeiro passo para utilizar a aplicação é a autenticação. Este fluxo garante que apenas utilizadores válidos possam aceder aos dados.

- **Endpoint:** POST /api/api-token-auth/

**Como funciona:**

1. O utilizador insere o seu nome de utilizador e senha no formulário de login do React.

2. O frontend utiliza a biblioteca axios para enviar uma requisição POST para o endpoint acima, contendo as credenciais em formato JSON.

    - **Corpo da Requisição:** {"username": "joao", "password": "123456"}

3. O backend Django recebe a requisição. A view obtain\_auth\_token do Django REST Framework valida as credenciais na base de dados.

4. Se as credenciais estiverem corretas, o Django gera (ou obtém, se já existir) um token de autenticação único para esse utilizador.

5. O backend responde com um status 200 OK e o token no corpo da resposta.

    - **Corpo da Resposta:** {"token": "a1b2c3d4e5f6..."}

6. O frontend React recebe o token e armazena-o no localStorage do navegador. Isto permite que o utilizador permaneça autenticado mesmo que atualize a página.


### **2. Requisições Autenticadas: Usando o Token**

Após o login, todas as outras requisições para a API (extrato, depósito, etc.) devem ser autenticadas.

**Como funciona:**

1. Para qualquer operação (ex: obter o extrato), o frontend primeiro lê o token que foi guardado no localStorage.

2. Ele monta uma requisição GET para o endpoint /api/extrato/.

3. **Este é o passo crucial:** Antes de enviar a requisição, ele adiciona um **cabeçalho (Header)** chamado Authorization. O valor deste cabeçalho deve seguir o formato Token \<seu\_token\_aqui>.

    - **Exemplo de Cabeçalho:** Authorization: Token a1b2c3d4e5f6...

4. O backend Django recebe a requisição. O middleware TokenAuthentication interceta-a antes de chegar à view.

5. O middleware verifica o cabeçalho Authorization, extrai o token, procura-o na base de dados e encontra o utilizador associado.

6. Se o token for válido, o middleware anexa o objeto User encontrado ao objeto request (request.user).

7. A requisição finalmente chega à ExtratoView. A view agora pode aceder a request.user para saber quem está a fazer o pedido e filtrar o extrato para mostrar apenas as movimentações daquele utilizador. Este mecanismo impede que um utilizador veja os dados de outro.


### **Resumo dos Endpoints da API**

|            |                      |                |                                              |                                                    |
| ---------- | -------------------- | -------------- | -------------------------------------------- | -------------------------------------------------- |
| **Método** | **Endpoint**         | **Protegido?** | **Descrição**                                | **Exemplo de Corpo (JSON)**                        |
| POST       | /api/api-token-auth/ | Não            | Obtém o token de autenticação.               | {"username": "...", "password": "..."}             |
| GET        | /api/extrato/        | **Sim**        | Retorna o extrato do utilizador autenticado. | (Nenhum)                                           |
| POST       | /api/depositar/      | **Sim**        | Deposita um valor na conta do utilizador.    | {"valor": "200.00"}                                |
| POST       | /api/sacar/          | **Sim**        | Levanta um valor da conta do utilizador.     | {"valor": "50.00"}                                 |
| POST       | /api/pagar/          | **Sim**        | Realiza um pagamento a partir da conta.      | {"valor": "99.90", "descricao": "..."}             |
| POST       | /api/transferir/     | **Sim**        | Transfere um valor para outra conta.         | {"valor": "150.00", "correntista\_destino\_id": 2} |


## **Parar a Aplicação**

Para parar todos os contentores relacionados com o projeto, execute o seguinte comando no diretório raiz:

```
docker-compose down
```
