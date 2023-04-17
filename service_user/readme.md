```
pipenv run flask run  
```


docker build -t service_user .
docker run -p 8888:8888 service_user
docker run -e DOCUMENTDB_DATABASE_URI="mongodb+srv://ticketoverflow:OW41ZGgFa8ixZj2p@ticketoverflow.zdgf5aw.mongodb.net/?retryWrites=true&w=majority" -p 8888:8888 service_user

http://localhost:8888/api/v1/users
