echo "remove previous test environment..."
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network prune --force

echo "build docker network..."
docker network create ticketoverflow


ENV_FILE=local.env

echo ">>[POSTGRES]"
cd ./dev_db/dev_local_postgres || exit
docker-compose up -d
sleep 5
python3 insert_init_data.py
cd ../..


echo ">>[SERVICE_USER]"
echo "start service_user services..."
cd ./service_user || exit
docker build -t service_user .
docker-compose build
docker-compose up -d
cd ..

echo ">>[SERVICE_TICKET]"
echo "start service_ticket services..."
cd ./service_ticket || exit
docker build -t service_ticket .
docker-compose up -d --build
cd ..

echo ">>[SERVICE_CONCERT]"
echo "start service_concert services..."
cd ./service_concert || exit
docker build -t service_concert .
docker-compose build
docker-compose up -d
cd ..

echo ">>[DEV_HAMILTON]"
echo "start dev_hamilton services..."
cd ./dev_hamilton || exit
docker build -t dev_hamilton .
docker-compose build
docker-compose up -d
cd ..

echo "Done"
