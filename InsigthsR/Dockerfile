FROM rocker/r-base:latest
WORKDIR /app
COPY ./Dados_tratados.R /app/Dados_tratados.R
COPY ./feriados.csv /app/feriados.csv
RUN R -e "install.packages(c('readr','RMySQL'))"
CMD ["Rscript", "/app/Dados_tratados.R"]

