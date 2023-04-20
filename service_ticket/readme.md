docker run -e DOCUMENTDB_DATABASE_URI="mongodb+srv://ticketoverflow:OW41ZGgFa8ixZj2p@ticketoverflow.zdgf5aw.mongodb.net/?retryWrites=true&w=majority" --network my-net -p 8888:8888 service_ticket




```
pipenv run flask run  
```


docker build -t service_user .
docker run -e DOCUMENTDB_DATABASE_URI="mongodb+srv://ticketoverflow:OW41ZGgFa8ixZj2p@ticketoverflow.zdgf5aw.mongodb.net/?retryWrites=true&w=majority" -p 8888:8888 service_user

docker run -e DOCUMENTDB_DATABASE_URI="mongodb+srv://ticketoverflow:OW41ZGgFa8ixZj2p@ticketoverflow.zdgf5aw.mongodb.net/?retryWrites=true&w=majority" --network my-net -p 8888:8888 service_user


http://localhost:8888/api/v1/users


## connect running container service_user to my-net
docker network connect my-net [containerid]