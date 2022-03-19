# syntax=docker/dockerfile:1
FROM python:3.11.0a6-bullseye
run apt-get update
copy . /lf_etl
run python3 -m pip install -r /lf_etl/requirements.txt
#run sh <(wget -qO - https://downloads.nordcdn.com/apps/linux/install.sh)
ENV PATH /lf_etl:$PATH
run sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
run wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
run apt-get install postgresql -y

cmd ["sh","/lf_etl/runme.sh"]