install.packages("readr")
install.packages("dplyr")
install.packages("RMySQL")

library(dplyr)
library(RMySQL)

dados <- read.csv("/Users/JuuhF/Music/att.csv")

feriados_frequencia <- dados %>%
  group_by(english_name) %>%
  summarise(frequencia = n()) %>%
  arrange(desc(frequencia))

feriado <- head(feriados_frequencia, 20)

con <- dbConnect(MySQL(), 
                 dbname = "SafeServer",   
                 host = "3.210.133.0",             
                 user = "root",            
                 password = "urubu100")  

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
head(feriado, 5)