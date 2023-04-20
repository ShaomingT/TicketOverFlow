

echo "remove previous test environment..."
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network prune --force

echo "build docker network..."
docker network create ticketoverflow

echo "start mongodb test environment..."
cd ./db/test_local
python3 build_mongodb_test_env.py
cd ../..


echo "start service_user services..."
cd ./service_user
docker build -t service_user .
docker-compose build
docker-compose up -d
cd ..
