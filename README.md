#  Smart School | Projeto Integrador SENAI "Roberto Mange"

Repositório backend desenvolvido para o Projeto Integrador do SENAI, focado na gestão e no monitoramento de dispositivos IoT (microcontroladores e sensores) por meio de uma API REST completa, segura e robusta.

---

## Stack Tecnológica

- **Linguagem:** Python 3.x
- **Framework Web:** Django e Django REST Framework (DRF)
- **Banco de Dados:** MySQL (local) / MariaDB (produção no Alwaysdata)
- **Autenticação:** JWT (`djangorestframework-simplejwt`)
- **Documentação:** Swagger e Redoc (`drf-yasg`)
- **Hospedagem:** Alwaysdata
- **Filtros e Ordenação:** `django-filter` e `rest_framework.filters`
- **Testes de API:** Bruno

---

## API em Produção (Alwaysdata)

A API está publicada e pode ser acessada sem instalar nada:

| Recurso | Endereço |
|---------|----------|
| Documentação interativa (Swagger) | https://gabrielly.alwaysdata.net/swagger/ |
| Documentação alternativa (Redoc) | https://gabrielly.alwaysdata.net/redoc/ |
| Painel administrativo (Django Admin) | https://gabrielly.alwaysdata.net/admin/ |
| Base da API | https://gabrielly.alwaysdata.net/api/ |

> **Importante:** todas as rotas da API exigem autenticação. Abrir `/api/laboratories/` diretamente no navegador, sem token, retorna erro 401. Isso é o comportamento esperado.

### Como acessar a API pelo Swagger

1. Abra https://gabrielly.alwaysdata.net/swagger/.
2. Role até a rota **`POST /api/token/`** e clique em **Try it out**.
3. Preencha o corpo da requisição com seu usuário e senha:

   ```json
   {
     "username": "seu_usuario",
     "password": "sua_senha"
   }
   ```

4. Clique em **Execute**. A resposta traz dois tokens:

   ```json
   {
     "refresh": "eyJ...",
     "access": "eyJ..."
   }
   ```

5. Copie o valor de **`access`**, clique no botão **Authorize** (cadeado, no topo da página) e digite:

   ```text
   Bearer SEU_TOKEN_ACCESS
   ```

   Inclua a palavra `Bearer` e um espaço antes do token. Clique em **Authorize** e depois em **Close**.
6. Pronto: agora todas as rotas do Swagger funcionam. Teste, por exemplo, `GET /api/laboratories/` ou `GET /api/me/`.

> Não tem usuário? Solicite as credenciais ao responsável pelo projeto. Cada usuário é criado pelo administrador.

### Validade dos tokens

| Token | Validade | Uso |
|-------|----------|-----|
| `access` | 60 minutos | Enviado no cabeçalho de cada requisição |
| `refresh` | 12 horas | Usado em `POST /api/token/refresh/` para gerar um novo `access` |

Quando o `access` expirar (erro 401), renove-o enviando o `refresh`:

```json
{ "refresh": "eyJ..." }
```

para `POST /api/token/refresh/`.

### Como acessar a API pelo Bruno, Insomnia ou Postman

1. Faça `POST https://gabrielly.alwaysdata.net/api/token/` com `username` e `password` no corpo (JSON).
2. Copie o `access` da resposta.
3. Nas demais requisições, adicione o cabeçalho:

   ```text
   Authorization: Bearer SEU_TOKEN_ACCESS
   ```

4. Exemplo: `GET https://gabrielly.alwaysdata.net/api/sensor-readings/`

### Como acessar por código (exemplo em JavaScript)

```javascript
const BASE_URL = "https://gabrielly.alwaysdata.net/api";

const login = await fetch(`${BASE_URL}/token/`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ username: "seu_usuario", password: "sua_senha" }),
});
const { access } = await login.json();

const resposta = await fetch(`${BASE_URL}/sensors/`, {
  headers: { Authorization: `Bearer ${access}` },
});
const sensores = await resposta.json();
```

> Se o seu front-end tiver um domínio próprio, ele precisa estar liberado no CORS do servidor. Veja a seção **Deploy no Alwaysdata**.

### Acessando o painel administrativo

Abra https://gabrielly.alwaysdata.net/admin/ e entre com um usuário administrador (`is_staff`). Por ele é possível cadastrar usuários, laboratórios, sensores e outros registros pela interface web.

---

##  Estrutura do Projeto

```text
PWBE-Integrador/
│
├── .venv/                              # Ambiente virtual (não versionado)
├── Docs/                               # Documentação do projeto
├── Validates/                          # Arquivos de validação
│
├── smart_school/                       # Projeto Django (execute o manage.py aqui)
│   ├── api/                            # App principal
│   │   ├── management/                 # Comandos customizados do Django
│   │   │   ├── commands/
│   │   │   │   ├── __init__.py
│   │   │   │   └── generate_readings.py  # Gera leituras simuladas de sensores
│   │   │   └── __init__.py
│   │   ├── migrations/                 # Migrações do banco de dados
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py                   # Modelos: User, Laboratory, Microcontroller, Sensor, SensorReading...
│   │   ├── permissions.py              # Permissões (IsSuperUserOrAdminOrReadOnly)
│   │   ├── serializers.py              # Serializers da API
│   │   ├── tests.py
│   │   ├── urls.py                     # Rotas do app
│   │   ├── viewSensor.py               # ViewSets de sensores, modelos e leituras
│   │   ├── viewsLaboratory.py          # ViewSets de laboratórios
│   │   ├── viewsMeasurementUnit.py     # ViewSets de unidades de medida
│   │   ├── viewsMicrocontroller.py     # ViewSets de microcontroladores
│   │   └── viewsUser.py                # ViewSets de usuários
│   │
│   ├── data/                           # Massa de dados inicial em CSV
│   │   ├── microcontroller.csv
│   │   ├── sensor.csv
│   │   └── sensormodel.csv
│   │
│   ├── smart_school/                   # Configurações do projeto Django
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── db.sqlite3                      # Banco SQLite local (desenvolvimento)
│   ├── manage.py                       # Gerenciador de comandos do Django
│   └── popula_csv.py                   # Script de importação via CSV e ORM
│
├── .gitignore
├── popular_db.sql                      # Script SQL de população do banco
├── README.md                           # Documentação oficial do projeto
└── requirements.txt                    # Dependências do projeto
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

Crie o banco antes de rodar o projeto (pelo MySQL Workbench ou terminal):

```sql
CREATE DATABASE smart_school_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

O `settings.py` lê as credenciais de **variáveis de ambiente** e, se elas não existirem, usa estes valores padrão para desenvolvimento local:

| Variável | Padrão local |
|----------|--------------|
| `DB_NAME` | `smart_school_db` |
| `DB_USER` | `root` |
| `DB_PASSWORD` | `root` |
| `DB_HOST` | `localhost` |
| `DB_PORT` | `3306` |

Se a senha do seu MySQL local for diferente, defina a variável antes de rodar os comandos:

**Windows (PowerShell):**

```powershell
$env:DB_PASSWORD="sua_senha"
```

**Linux/Mac:**

```bash
export DB_PASSWORD='sua_senha'
```

> Use Python **3.10 a 3.13** (recomendado 3.12). Versões muito novas podem não ter instaladores prontos de algumas dependências, como o `mysqlclient`.

### 5. Executar as migrações

Entre na pasta do projeto Django (onde está o `manage.py`) e rode:

```bash
cd smart_school
python manage.py makemigrations
python manage.py migrate
```

> **Atenção:** todos os comandos `python manage.py ...` e `python popula_csv.py` abaixo devem ser executados de dentro da pasta `smart_school/`, com o ambiente virtual ativado.

### 6. Iniciar o servidor

```bash
python manage.py runserver
```

A API ficará disponível em `http://127.0.0.1:8000/`.

---

##  População de Dados (Task 4.3)

Para popular o banco com modelos de sensores, microcontroladores e sensores a partir dos CSVs da pasta `data/`, além de gerar automaticamente 100 leituras simuladas para os dispositivos ativos:

```bash
python popula_csv.py
```

Alternativamente, é possível usar o script SQL `popular_db.sql`, localizado na raiz do repositório.

---

##  Gerando Leituras Simuladas (`generate_readings`)

O projeto possui um comando customizado do Django que simula leituras de sensores, útil para testar a API, os filtros e os endpoints de estatísticas sem precisar de hardware real.

**Arquivo:** `smart_school/api/management/commands/generate_readings.py`

### Como funciona

Ao ser executado, o comando:

1. Busca todos os sensores ativos (`sen_is_active=True`).
2. Para cada sensor, gera um valor aleatório entre **0 e 100** (com 2 casas decimais).
3. Cria um registro `SensorReading` associado ao sensor.
4. Exibe no terminal quantas leituras foram geradas.

Se não houver nenhum sensor ativo, o comando exibe um aviso e não cria nenhum registro.

### Como executar

Dentro da pasta `smart_school/`, com o ambiente virtual ativado e as migrações aplicadas:

```bash
python manage.py generate_readings
```

> O nome do comando é o nome do arquivo, sem o `.py`.

### Exemplos de saída

**Sucesso:**

```text
Sucesso! 12 leituras simuladas foram geradas.
```

**Nenhum sensor ativo:**

```text
Nenhum sensor ativo encontrado.
```

### Dicas

- Cada execução gera **uma leitura por sensor ativo**. Execute várias vezes para gerar mais dados.
- Para simular leituras contínuas, rode o comando em loop:

  **Linux/Mac** (a cada 10 segundos):

  ```bash
  while true; do python manage.py generate_readings; sleep 10; done
  ```

  **Windows (PowerShell):**

  ```powershell
  while ($true) { python manage.py generate_readings; Start-Sleep -Seconds 10 }
  ```

- Certifique-se de que existem sensores cadastrados e ativos (por exemplo, após rodar o `popula_csv.py`). Caso contrário, nenhuma leitura será criada.
- Depois de gerar as leituras, valide o resultado em `GET /api/sensor-readings/` ou nos endpoints de consultas personalizadas descritos abaixo.

---

##  Documentação dos Endpoints da API

A API segue o padrão REST, com nomenclaturas, variáveis e rotas em inglês.

> **Permissões:** todas as rotas exigem autenticação via token JWT. Usuários autenticados podem fazer leituras (`GET`). Operações de escrita (`POST`, `PUT`, `PATCH`, `DELETE`) exigem permissão de administrador (`IsSuperUserOrAdminOrReadOnly`), e o gerenciamento de usuários é restrito ao superusuário.

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

1. Inicie o servidor local (dentro de `smart_school/`):

```bash
python manage.py runserver
```

2. (Opcional) Gere dados de teste com `python manage.py generate_readings`.
3. Crie um usuário administrador: `python manage.py createsuperuser`.
4. Abra o Bruno, crie sua collection e faça login em `POST http://127.0.0.1:8000/api/token/`.
5. Envie o `access` no cabeçalho `Authorization: Bearer SEU_TOKEN` e aponte as requisições para `http://127.0.0.1:8000/api/...` (ou para `https://gabrielly.alwaysdata.net/api/...` em produção).
6. Use os métodos descritos nas tabelas acima para validar as rotas e as regras de negócio.

---

## Deploy no Alwaysdata

Passo a passo para publicar este backend em uma conta do [Alwaysdata](https://www.alwaysdata.com). Os exemplos usam `SEUUSUARIO` no lugar do nome da conta.

### 1. Preparar o código

O `settings.py` já está pronto para produção: `SECRET_KEY`, `DEBUG`, banco, hosts e CORS são lidos de variáveis de ambiente, e os arquivos estáticos são servidos pelo **WhiteNoise**. Antes de publicar, ajuste em `smart_school/smart_school/settings.py` os valores padrão de `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` para o seu domínio `SEUUSUARIO.alwaysdata.net` e envie tudo para o GitHub.

### 2. Criar o banco de dados

No painel, em **Databases → MySQL**:

1. Crie um banco (ex.: `smart_school`, que vira `SEUUSUARIO_smart_school`).
2. Crie um usuário MySQL e dê a ele acesso total ao banco.
3. O servidor do banco é `mysql-SEUUSUARIO.alwaysdata.net`.

> O Alwaysdata usa MariaDB, compatível com o Django. Para popular o banco, use `popula_csv.py`, não o `popular_db.sql`.

### 3. Ativar o SSH e baixar o projeto

Em **Remote access → SSH/SFTP**, habilite o acesso e defina uma senha. Depois:

```bash
ssh SEUUSUARIO@ssh-SEUUSUARIO.alwaysdata.net
cd ~/www
git clone https://github.com/gaby-mart/PWBE-Integrador.git
cd PWBE-Integrador
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar o site

Em **Web → Sites → Add a site**:

| Campo | Valor |
|-------|-------|
| Addresses | `SEUUSUARIO.alwaysdata.net` |
| Type | Python WSGI |
| Application path | `www/PWBE-Integrador/smart_school/smart_school/wsgi.py` |
| Working directory | `www/PWBE-Integrador/smart_school` |
| virtualenv directory | `www/PWBE-Integrador/.venv` |
| Static paths | deixar **vazio** (o WhiteNoise cuida dos estáticos) |

No campo **Environment variables**, uma por linha, sem aspas:

```text
SECRET_KEY=uma_chave_longa_e_aleatoria
DEBUG=False
DB_NAME=SEUUSUARIO_smart_school
DB_USER=SEUUSUARIO_usuario_mysql
DB_PASSWORD=senha_do_banco
DB_HOST=mysql-SEUUSUARIO.alwaysdata.net
DB_PORT=3306
```

Para gerar a `SECRET_KEY`:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Para liberar um front-end hospedado em outro domínio, adicione também:

```text
CORS_EXTRA_ORIGINS=https://seu-front.com
```

### 5. Criar as tabelas e os dados

No terminal SSH, com o ambiente virtual ativo, exporte as mesmas variáveis (o terminal não lê as do painel) e rode:

```bash
cd ~/www/PWBE-Integrador/smart_school
source ../.venv/bin/activate

export DB_NAME=SEUUSUARIO_smart_school
export DB_USER=SEUUSUARIO_usuario_mysql
export DB_PASSWORD='senha_do_banco'
export DB_HOST=mysql-SEUUSUARIO.alwaysdata.net
export DB_PORT=3306
export DEBUG=False
export SECRET_KEY=qualquercoisa

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python popula_csv.py
```

### 6. Reiniciar e testar

Em **Web → Sites**, clique em **Submit** no site para reiniciar e abra `https://SEUUSUARIO.alwaysdata.net/swagger/`.

### Atualizando o site depois

```bash
cd ~/www/PWBE-Integrador
git pull
```

Se alterou dependências ou modelos, rode também `pip install -r requirements.txt` e `python manage.py migrate` (com as variáveis exportadas). Depois reinicie o site no painel (**Web → Sites → Submit**).

### Problemas comuns

| Sintoma | Causa provável |
|---------|----------------|
| Swagger ou Admin sem estilo / `404` em `/static/` | WhiteNoise não instalado ou `collectstatic` não executado; deixe **Static paths** vazio |
| `Can't connect to local server through socket` | Variáveis `DB_*` não definidas (usando `localhost`) |
| `Access denied for user` | Usuário ou senha do banco incorretos |
| `DisallowedHost` | Domínio ausente em `ALLOWED_HOSTS` |
| Erro `403` ao fazer login no `/admin/` | Falta `CSRF_TRUSTED_ORIGINS` com `https://` |
| Erro de CORS no navegador | Domínio do front-end ausente em `CORS_EXTRA_ORIGINS` |
| Erro `500` | Consulte o log em **Logs** (no menu do site, no painel) |