
    docker build -t soilanalysis . [Constroi o container/imagens]
    docker run -p 8000:8000 soilanalysis [verificar se ficou obsoleto conforme fui implementando o docker-compose + implementei o postgreSQL]
    docker compose up --build [roda o container criado]
    docker image list [Para visualizar a lista de imagens ativas no docker]
