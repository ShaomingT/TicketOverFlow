
[] service_user helath, how to test 503 and 500

# testing
for testinh:
service_user is running on 8888
service_ticket is running on 9999
service_concert is running on 7777


# how to test

conda activate ticketoverflow
./build_test_env.sh
run tests in tests folder


interface:
https://csse6400.uqcloud.net/assessment/ticketoverflow/



# service_user
```
pipenv run flask run  
```


docker build -t service_user .
docker run -e DOCUMENTDB_DATABASE_URI="mongodb+srv://ticketoverflow:OW41ZGgFa8ixZj2p@ticketoverflow.zdgf5aw.mongodb.net/?retryWrites=true&w=majority" -p 8888:8888 service_user

docker run -e DOCUMENTDB_DATABASE_URI="mongodb+srv://ticketoverflow:OW41ZGgFa8ixZj2p@ticketoverflow.zdgf5aw.mongodb.net/?retryWrites=true&w=majority" --network my-net -p 8888:8888 service_user


http://localhost:8888/api/v1/users


## connect running container service_user to my-net
docker network connect my-net [containerid]



tickets:
if no paras are given, return all ticket list
if given user_id or concert_id paras. return list of matched
only accept two para, user_id and concert_id. if other para is provided, such as "price". return 404




# Cases
Tickets:
There can be more than one concert a day in one venue, even they have the same name. same data, and same capacity. In this assignment, there is only date, but no time. so we assume that in one day, mutiple same concert can be hold. (it is like in UQ, there are lecture, and lecture 2. All of them are same)


cases not considered. 
[ ] every time, when buy a new ticket, it need to see whether the concert is full or not. if it is full, don't sell this ticket and return chaneg the status of concert to SOLD_OUT.