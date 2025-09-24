
docker image list [Para visualizar a lista de imagens ativas no docker]

Subir o projeto com Docker Compose
docker-compose up -d
Reconstrói todas as imagens se necessário.


Verificar containers ativos
docker compose ps

Acessar o container Django 
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000


Parar o ambiente
docker compose down
Para todos os containers e remove a rede criada pelo Compose.
As imagens não são removidas, apenas os containers temporários.

Se fizer alterações no requirements.txt ou Dockerfile, sempre use:
docker compose up --build
docker-compose up -d

Portainer commando
docker run -d -p 9000:9000 -p 8000:8000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce

Porta do Portainer:
http://localhost:9000/

erro com psycopg2: 
pip install psycopg-binary 
pip freeze | Select-String psycopg2
pip freeze | Select-String psycopg2 > requirements.txt

environments ip: 127.0.0.1


9001
https://www.hivemq.com/demos/websocket-client/
host: localhost
port: 9001
desmarcar ssl / a conexão é por tcp/WebSocket