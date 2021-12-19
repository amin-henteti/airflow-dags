#* make a test if there is a modification if so copy otherwise exit
# latest_modif_file=$(ls -alt | grep -e "\w*\.py" -m 1 -o)
# if 


for file in $(ls /c/Users/Public/mydags/*.py)
do
docker cp "$file" c5:/opt/airflow/dags

done
# docker exec -it c5 airflow webserver


