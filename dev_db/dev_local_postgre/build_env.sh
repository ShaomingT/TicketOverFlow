echo "> init db"
docker-compose down
docker-compose build
docker-compose up -d
echo "> insert init data"
python3 ./insert_init_data.py