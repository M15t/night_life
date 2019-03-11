#!/usr/bin/env bash

# Ensure the MySQL server is online and usable
# echo "Waiting for MySQL"
until docker exec -i night-life.db mysql -h localhost -umysql -pmysql -P 3308 -e "SELECT 1" &> /dev/null
do
  # printf "."
  sleep 1
done
