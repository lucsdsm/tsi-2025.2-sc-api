# **API de Movimentações Bancárias & Frontend React**

Este projeto é uma aplicação full-stack desenvolvida com Django (backend) e React (frontend). A aplicação simula um sistema bancário simples, permitindo que utilizadores se autentiquem, visualizem os seus extratos e realizem operações financeiras como levantamentos, depósitos, pagamentos e transferências. **A aplicação inclui notificações em tempo real via WebSocket**, informando imediatamente os utilizadores sobre todas as suas operações bancárias.

A aplicação é totalmente contentorizada com Docker, utilizando uma base de dados PostgreSQL, o que simplifica enormemente o processo de configuração e execução.


## **Tecnologias Utilizadas**

- **Frontend:** React

- **Backend:** Django, Django REST Framework, Django Channels

- **Comunicação em Tempo Real:** WebSocket (Django Channels + Daphne)

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

**Notificações em Tempo Real:** Sempre que realizar uma operação (depósito, saque, pagamento ou transferência), receberá uma notificação instantânea no canto superior direito da tela, confirmando a operação. No caso de transferências, tanto o remetente quanto o destinatário recebem notificações simultâneas.