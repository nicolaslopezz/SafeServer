FROM mysql:latest
WORKDIR /
ENV MYSQL_ROOT_PASSWORD=batatas123
COPY ./Script/init.sql /docker-entrypoint-initdb.d/
EXPOSE 3306
