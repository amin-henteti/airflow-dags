
docker exec -it dc airflow scheduler -D

sleep 10

docker exec -it dc airflow webserver -D


