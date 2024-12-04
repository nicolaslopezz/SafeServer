library(dplyr)
library(RMySQL)
library(readr)

dados <- read.csv("/app/feriados.csv")

feriados_frequencia <- dados %>%
  group_by(english_name) %>%
  summarise(frequencia = n()) %>%
  arrange(desc(frequencia))

feriado <- head(feriados_frequencia, 20)

con <- dbConnect(MySQL(), 
                 dbname = "SafeSever",   
                 host = "imagembanco",  #serviço docker-compose
                 user = "root",          
                 password = "urubu100")  

dbExecute(con, "
  CREATE TABLE IF NOT EXISTS feriado_freq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomeFeriado VARCHAR(50),
    frequencia INT
  );
")

# Inserir dados
for (i in 1:nrow(feriado)) {
  dbExecute(con, "
    INSERT INTO feriado_freq (nomeFeriado, frequencia)
    VALUES (?, ?)", 
    params = list(feriado$english_name[i], feriado$frequencia[i])
  )
}

print(head(feriado, 5))

dbDisconnect(con)
