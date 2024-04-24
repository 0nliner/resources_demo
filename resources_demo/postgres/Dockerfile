FROM postgres:15

# Устанавливаем пакеты, необходимые для компиляции и установки PL/Python3
RUN apt-get update &&\
	apt-get install -y build-essential python3-dev &&\
	apt-get install postgresql-plpython3-15


# Устанавливаем PL/Python3
RUN echo "CREATE EXTENSION plpython3u;" > /docker-entrypoint-initdb.d/plpython3.sql

