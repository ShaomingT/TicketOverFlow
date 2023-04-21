

echo "remove previous test environment..."
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network prune --force

echo "build docker network..."
docker network create ticketoverflow


echo ">>[MONGODB]"
echo "start mongodb test environment..."
cd ./db/test_local
python3 build_mongodb_test_env.py
cd ../..


echo ">>[SERVICE_USER]"
echo "start service_user services..."
cd ./service_user
docker build -t service_user .
docker-compose build
docker-compose up -d
cd ..


echo ">>[SERVICE_TICKET]"
echo "start service_ticket services..."
cd ./service_ticket
docker build -t service_ticket .
docker-compose build
docker-compose up -d
cd ..

echo ">>[SERVICE_HAMILTON]"
echo "start hamilton services..."
cd ./service_hamilton
docker build -t service_hamilton .
docker-compose build
docker-compose up -d
cd ..

echo ">>[SERVICE_CONCERT]"
# echo "start service_concert services..."
# cd ./service_concert
# docker build -t service_concert .
# docker-compose build
# docker-compose up -d
# cd ..


echo "Done"
