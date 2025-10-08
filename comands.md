# Guia de Comandos e Operações do Projeto SoilAnalysis
## Este arquivo é o manual completo para instalar, executar e gerenciar o projeto.

# 🚀 Guia Rápido para Iniciar (Workflow Principal)
Siga estes 3 passos para colocar o projeto no ar e recebendo dados.

## 1. Subir o Ambiente (Site + Banco de Dados)
Este é o primeiro comando. Ele constrói e inicia todos os "containers" do Docker.

Abra um terminal e execute:

```
docker-compose up --build
```

Use a opção --build sempre que houver alterações nos arquivos Dockerfile ou requirements.txt.

## 2. Criar as Tabelas no Banco (Apenas na Primeira Vez)
Se for a primeira vez rodando, o banco de dados estará vazio. Este comando cria as tabelas.

Abra um NOVO terminal e execute:

```
docker-compose exec web python manage.py migrate
```

## 3. Iniciar o Coletor de Dados do Sensor (Ouvinte MQTT)
Este comando inicia o script que recebe os dados do sensor e salva no banco. Ele deve ser mantido rodando em um terminal separado.

Abra um TERCEIRO terminal e execute:

```
docker-compose exec web python manage.py start_mqtt_listener
```

## ⚙️ Gerenciamento do Ambiente Docker
Comandos úteis para o dia a dia.

Verificar containers ativos:

```
docker compose ps
```

Parar o ambiente:
(Para todos os containers e remove as redes)

```
docker compose down
```

Visualizar a lista de imagens Docker:
```
docker image list
```

## 🐍 Comandos Comuns do Django
Estes comandos devem ser executados "dentro" do container web.

Criar um superusuário (para acessar a área de admin):

```
docker-compose exec web python manage.py createsuperuser
```

Criar novas "migrações" (após alterar os models.py):

```
docker-compose exec web python manage.py makemigrations
```

## 🛠️ Avançado e Solução de Problemas
Instalação do Portainer (Interface Gráfica para o Docker):
(Opcional, para quem prefere gerenciar os containers visualmente)

```
docker run -d -p 9000:9000 -p 8000:8000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
```
Acesse em: http://localhost:9000/

Solução para erro com psycopg2 (conector do PostgreSQL):
(Se ocorrer um erro de compilação durante o build)

```
pip install psycopg2-binary
pip freeze > requirements.txt
```
