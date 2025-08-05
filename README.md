# API de Formulários Dinâmicos

API para um sistema de formulários dinâmicos com perguntas cadastradas pelos próprios usuários, desenvolvida com FastAPI, SQLAlchemy e PostgreSQL.

## Estrutura do Projeto

```
app/
├── api/
│   ├── endpoints/
│   │   ├── formularios.py
│   │   └── perguntas.py
│   └── api.py
├── core/
│   └── config.py
├── crud/
│   ├── formulario.py
│   └── pergunta.py
├── db/
│   └── database.py
├── models/
│   └── models.py
├── schemas/
│   ├── formulario.py
│   └── pergunta.py
└── main.py
```

## Requisitos

- Python 3.8+
- PostgreSQL
- Dependências listadas em `requirements.txt`

## Configuração do Ambiente

### Método 1: Instalação Local

1. Clone o repositório:

```bash
git clone https://github.com/d4nielantoni/dynamic-forms-api
cd teste_tecnico_fbgenios
```

2. Crie um ambiente virtual e ative-o:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:

   - Crie um arquivo `.env` na raiz do projeto baseado no arquivo `.env.example`
   - Configure as variáveis de ambiente para conexão com o PostgreSQL

```
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=forms_db
```

5. Crie o banco de dados no PostgreSQL:

```bash
# Acesse o PostgreSQL
psql -U postgres

# Crie o banco de dados
CREATE DATABASE forms_db;
```

### Método 2: Usando Docker (Recomendado)

1. Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

2. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd teste_tecnico_fbgenios
```

3. Inicie os containers:

```bash
docker-compose up -d
```

Este comando irá:
- Construir a imagem da aplicação
- Iniciar um container PostgreSQL
- Iniciar a aplicação conectada ao banco de dados
- Configurar todas as variáveis de ambiente necessárias

## Executando a Aplicação

### Método Local

1. Inicie a aplicação:

```bash
python main.py
```

2. Para carregar dados de exemplo (opcional):

```bash
python seed_data.py
```

### Método Docker

A aplicação já estará rodando após executar `docker-compose up -d`.

Para carregar dados de exemplo (opcional):

```bash
docker-compose exec app python seed_data.py
```

## Acessando a API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints Disponíveis

### Formulários

- `GET /api/v1/formularios/` - Listar todos os formulários
- `POST /api/v1/formularios/` - Criar um novo formulário
- `GET /api/v1/formularios/{formulario_id}` - Obter um formulário específico
- `PUT /api/v1/formularios/{formulario_id}` - Atualizar um formulário
- `DELETE /api/v1/formularios/{formulario_id}` - Excluir um formulário

### Perguntas

- `GET /api/v1/perguntas/` - Listar todas as perguntas (com filtros, ordenação e paginação)
- `POST /api/v1/perguntas/` - Criar uma nova pergunta
- `GET /api/v1/perguntas/{pergunta_id}` - Obter uma pergunta específica
- `PUT /api/v1/perguntas/{pergunta_id}` - Atualizar uma pergunta
- `DELETE /api/v1/perguntas/{pergunta_id}` - Excluir uma pergunta
- `GET /api/v1/perguntas/formulario/{formulario_id}` - Listar perguntas de um formulário específico

## Testes

O projeto inclui testes unitários e de integração.

### Executando os Testes

```bash
# Executar todos os testes
pytest

# Executar apenas testes unitários
pytest tests/unit/

# Executar apenas testes de integração
pytest tests/integration/
```

### Estrutura dos Testes

```
tests/
├── unit/
│   ├── test_formularios.py  # Testes para endpoints de formulários
│   └── test_perguntas.py    # Testes para endpoints de perguntas
└── integration/
    └── test_api_flow.py     # Testes de fluxo completo da API
```

## Exemplos de Uso

### Criar um Formulário

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/formularios/' \
  -H 'Content-Type: application/json' \
  -d '{
  "titulo": "Pesquisa de Satisfação",
  "descricao": "Formulário para avaliar a satisfação dos clientes",
  "ordem": 1
}'
```

### Criar uma Pergunta

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/perguntas/' \
  -H 'Content-Type: application/json' \
  -d '{
  "id_formulario": 1,
  "titulo": "Você está satisfeito com nosso serviço?",
  "codigo": "satisfacao",
  "tipo_pergunta": "Sim_Não",
  "obrigatoria": true,
  "ordem": 1
}'
```

### Listar Perguntas com Filtros

```bash
curl -X 'GET' \
  'http://localhost:8000/api/v1/perguntas/formulario/1?tipo_pergunta=Sim_Não&obrigatoria=true&sort_by=ordem&sort_order=asc'
```
