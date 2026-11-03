#  Smart School | Projeto Integrador SENAI "Roberto Mange"

Repositório backend desenvolvido para o Projeto Integrador do SENAI, focado na gestão e no monitoramento de dispositivos IoT (microcontroladores e sensores) por meio de uma API REST completa, segura e robusta.

---

## Stack Tecnológica

- **Linguagem:** Python 3.x
- **Framework Web:** Django e Django REST Framework (DRF)
- **Banco de Dados:** MySQL
- **Filtros e Ordenação:** `django-filter` e `rest_framework.filters`
- **Testes de API:** Bruno (ou Insomnia)

---

##  Estrutura do Projeto

```text
PWBE-Integrador/
│
├── Docs/                           # Documentação do projeto
├── Validates/                      # Arquivos de validação
│
├── smart_school/                   # Projeto Django
│   ├── api/                        # App principal
│   │   ├── management/             # Comandos customizados do Django
│   │   ├── migrations/             # Migrações do banco de dados
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py               # Modelos: User, Laboratory, Microcontroller, Sensor, SensorReading...
│   │   ├── permissions.py          # Permissões (IsSuperUserOrAdminOrReadOnly)
│   │   ├── serializers.py          # Serializers da API
│   │   ├── tests.py
│   │   ├── urls.py                 # Rotas do app
│   │   ├── viewSensor.py           # ViewSets de sensores, modelos e leituras
│   │   ├── viewsLaboratory.py      # ViewSets de laboratórios
│   │   ├── viewsMeasurementUnit.py # ViewSets de unidades de medida
│   │   ├── viewsMicrocontroller.py # ViewSets de microcontroladores
│   │   └── viewsUser.py            # ViewSets de usuários
│   │
│   ├── data/                       # Massa de dados inicial em CSV
│   │   ├── microcontroller.csv
│   │   ├── sensor.csv
│   │   └── sensormodel.csv
│   │
│   ├── smart_school/               # Configurações do projeto Django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── db.sqlite3                  # Banco SQLite local (desenvolvimento)
│   ├── manage.py                   # Gerenciador de comandos do Django
│   └── popula_csv.py               # Script de importação via CSV e ORM
│
├── .gitignore
├── popular_db.sql                  # Script SQL de população do banco
└── README.md                       # Documentação oficial do projeto
```

---

## Como Executar o Projeto Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/gaby-mart/PWBE-Integrador
cd PWBE-Integrador
```

### 2. Criar e ativar o ambiente virtual

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o banco de dados (MySQL)

Em `smart_school/settings.py`, configure as credenciais:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_do_banco',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Executar as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

---

##  População de Dados (Task 4.3)

Para popular o banco com modelos de sensores, microcontroladores e sensores a partir dos CSVs da pasta `data/`, além de gerar automaticamente 100 leituras simuladas para os dispositivos ativos:

```bash
python popula_csv.py
```

---

##  Documentação dos Endpoints da API

A API segue o padrão REST, com nomenclaturas, variáveis e rotas em inglês.

> **Permissões:** operações de escrita (`POST`, `PUT`, `PATCH`, `DELETE`) exigem permissão de administrador (`IsSuperUserOrAdminOrReadOnly`). Leituras (`GET`) são públicas.

### 1. Sensor Models: `/api/sensor-models/`

Gerencia os tipos e especificações dos modelos de sensores suportados.

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/sensor-models/` | Lista todos os modelos cadastrados |
| `POST` | `/api/sensor-models/` | Cadastra um novo modelo de sensor |
| `GET` | `/api/sensor-models/{id}/` | Exibe os detalhes de um modelo |
| `PUT` / `PATCH` | `/api/sensor-models/{id}/` | Atualiza um modelo de sensor |
| `DELETE` | `/api/sensor-models/{id}/` | Remove um modelo de sensor |

### 2. Microcontrollers: `/api/microcontrollers/`

Gerencia as placas microcontroladoras (ESP32) instaladas nos laboratórios e ambientes.

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/microcontrollers/` | Lista todos os microcontroladores |
| `POST` | `/api/microcontrollers/` | Cadastra um novo microcontrolador |
| `GET` | `/api/microcontrollers/{id}/` | Exibe os detalhes de um microcontrolador |
| `PUT` / `PATCH` | `/api/microcontrollers/{id}/` | Atualiza os dados de um microcontrolador |
| `DELETE` | `/api/microcontrollers/{id}/` | Remove um microcontrolador |

### 3. Sensors: `/api/sensors/`

Gerencia os sensores físicos associados aos modelos e microcontroladores.

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/sensors/` | Lista todos os sensores |
| `POST` | `/api/sensors/` | Cadastra um novo sensor |
| `GET` | `/api/sensors/{id}/` | Exibe os detalhes de um sensor |
| `PUT` / `PATCH` | `/api/sensors/{id}/` | Atualiza os dados de um sensor |
| `DELETE` | `/api/sensors/{id}/` | Remove um sensor |

### 4. Sensor Readings: `/api/sensor-readings/`

Gerencia o registro de coletas e medições enviadas pelos dispositivos.

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/sensor-readings/` | Lista todas as leituras (suporta `?sr_sen=ID` e `?ordering=-sr_measured_at`) |
| `POST` | `/api/sensor-readings/` | Registra uma nova leitura |
| `GET` | `/api/sensor-readings/{id}/` | Exibe os detalhes de uma leitura |
| `PUT` / `PATCH` | `/api/sensor-readings/{id}/` | Atualiza uma leitura |
| `DELETE` | `/api/sensor-readings/{id}/` | Remove uma leitura |

---

##  Endpoints Extras e Consultas Personalizadas

Além do CRUD padrão, há ações customizadas em `sensor-readings`, otimizadas para dashboards e análises rápidas:

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/sensor-readings/statistics/?sr_sen=ID` | Resumo estatístico de um sensor (total de registros, valor mínimo, máximo e média) |
| `GET` | `/api/sensor-readings/recentes/` | Leituras registradas nas últimas 24 horas |
| `GET` | `/api/sensor-readings/ultima-por-sensor/` | Leitura mais recente (último estado) de cada sensor |

---

##  Testando no Bruno (ou Insomnia)

1. Inicie o servidor local:

```bash
python manage.py runserver
```

2. Abra o Bruno, crie sua collection e aponte as requisições para `http://127.0.0.1:8000/api/...`
3. Use os métodos descritos nas tabelas acima para validar as rotas e as regras de negócio.