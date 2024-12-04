FROM rocker/r-base:latest
# Defina o diretório de trabalho
WORKDIR /app
# Copie os arquivos necessários para o container
COPY ./Dados_tratados.R /app/Dados_tratados.R
COPY ./feriados.csv /app/feriados.csv
# Instale as dependências do sistema e pacotes R necessários
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libmysqlclient-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# Instale pacotes R necessários
RUN R -e "install.packages(c('readr', 'RMySQL', 'dplyr'), repos='http://cran.r-project.org')"
# Comando padrão de execução
CMD ["Rscript", "/app/Dados_tratados.R"]

