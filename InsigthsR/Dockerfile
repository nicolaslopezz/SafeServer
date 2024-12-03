FROM rocker/r-base:latest
WORKDIR /app
COPY ./InsigthsR/Dados_tratados.R /app/Dados_tratados.R
COPY ./InsigthsR/feriados.csv /app/feriados.csv
RUN R -e "install.packages(c('readr', 'ggplot2', 'RMySQL'))"
CMD ["Rscript", "/app/Dados_tratados.R"]

