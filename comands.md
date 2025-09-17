
    docker build -t soilanalysis . [Constroi o container/imagens]
    docker run -p 8000:8000 soilanalysis [verificar se ficou obsoleto conforme fui implementando o docker-compose + implementei o postgreSQL]
    docker compose up --build [roda o container criado]
    docker image list [Para visualizar a lista de imagens ativas no docker]




     Subir o projeto com Docker Compose
     docker compose up --build
     Reconstrói todas as imagens se necessário.
Sobe os containers (Django + PostgreSQL) e conecta-os na rede interna definida pelo Compose.
Saída dos logs aparecerá no terminal.


Verificar containers ativos
docker compose ps

Acessar o container Django (opcional)
docker compose exec django-web bash
web é o nome do serviço Django definido no docker-compose.yml.
Permite rodar comandos dentro do container, por exemplo:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000

Listar imagens Docker (opcional)
docker image list

Parar o ambiente
docker compose down
Para todos os containers e remove a rede criada pelo Compose.
As imagens não são removidas, apenas os containers temporários.

Se fizer alterações no requirements.txt ou Dockerfile, sempre use:
docker compose up --build