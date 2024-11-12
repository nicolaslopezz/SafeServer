
install.packages("readr")
install.packages("dplyr")
install.packages("RMySQL")


library(dplyr)
library(RMySQL)

# Carregar o arquivo CSV
dados <- read.csv("/Users/JuuhF/Music/att.csv")



feriados_frequencia <- dados %>%
  group_by(english_name) %>%
  summarise(frequencia = n()) %>%
  arrange(desc(frequencia))

feriado <- head(feriados_frequencia, 20)

con <- dbConnect(MySQL(), 
                 dbname = "SafeServer",   
                 host = "localhost",             
                 user = "root",            
                 password = "batatas123")  

dbExecute(con, "
  CREATE TABLE IF NOT EXISTS feriado_freq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nomeFeriado VARCHAR(50),
    frequencia INT
  );
")

for (i in 1:nrow(feriado)) {
  query <- paste0("INSERT INTO feriado_freq(nomeFeriado, frequencia) 
                   VALUES ('", feriado$english_name[i], "', ", 
                  feriado$frequencia[i], ");")
  dbExecute(con, query)
}

feriado
head(feriado,5)


dados_agrupados <- group_by(dados, english_name) 
dados_resumidos <- summarise(dados_agrupados, frequencia = n(), media_CPU = mean(CPU_perc, na.rm = TRUE))
dados_ordenados <- arrange(dados_resumidos, desc(frequencia)) 
dados_top <- head(dados_ordenados, 5)
dados_top



