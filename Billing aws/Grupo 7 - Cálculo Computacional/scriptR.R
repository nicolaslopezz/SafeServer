dadosGiorgio <- Previsoes...Giorgio
View(dadosGiorgio)

dadosJuliana <- Previsoes...Juliana
View(dadosJuliana)

dadosFernando <- Previsoes...Fernando
View(dadosFernando)

dadosNicolas <- Previsoes...Nicolas
View(dadosNicolas)

dadosLeandro <- Previsoes...Leandro
View(dadosLeandro)

totalAgosto <- sum(dadosJuliana[4,2], dadosFernando[4,2], dadosNicolas[4,2], dadosGiorgio[4,2], dadosLeandro[4,2])
totalAgosto

totalSetembro <- sum(dadosJuliana[4,3], dadosFernando[4,3], dadosNicolas[4,3], dadosGiorgio[4,3], dadosLeandro[4,3])
totalSetembro

totalOutubro <- sum(dadosJuliana[4,4], dadosFernando[4,4], dadosNicolas[4,4], dadosGiorgio[4,4], dadosLeandro[4,4])
totalOutubro

totalNovembro <- sum(dadosJuliana[4,5], dadosFernando[4,5], dadosNicolas[4,5], dadosGiorgio[4,5], dadosLeandro[4,5])
totalNovembro

totalPorMes <- data.frame(totalAgosto, totalSetembro, totalOutubro)
totalPorMes <- as.numeric(totalPorMes)
View(totalPorMes)

totalEC2Other <- sum(dadosFernando[1,6], dadosGiorgio[1,6], dadosJuliana[1,6], dadosLeandro[1,6], dadosNicolas[1,6]) 

totalEC2 <- sum(dadosFernando[2,6], dadosGiorgio[2,6], dadosJuliana[2,6], dadosLeandro[2,6], dadosNicolas[2,6])

totalVPC <- sum(dadosFernando[3,6], dadosGiorgio[3,6], dadosJuliana[3,6], dadosLeandro[3,6], dadosNicolas[3,6])

totalServicos <- data.frame(totalEC2Other, totalEC2, totalVPC)
View(totalServicos)

install.packages("forecast")
library(forecast)

#custo total do grupo e previsão para o mês de novembro

tempo1 <- 8:10
modelo_lm <- lm(totalPorMes ~ tempo1)
previsao_lm <- predict(modelo_lm, newdata = data.frame(tempo1 = 11))  
previsao_lm
previsaoNovembro <- data.frame(totalPorMes)

previsaoNovembro <- data.frame(totalPorMes = c(totalAgosto, totalSetembro, totalOutubro, previsao_lm))

View(previsaoNovembro)

previsao_lm



mes <- c("agosto", "setembro", "outubro", "novembro")

previsaoNovembro <- cbind(mes, previsaoNovembro$totalPorMes)

dados <- data.frame(previsaoNovembro)

install.packages("ggplot2")

library(ggplot2)


colnames(dados)[1] <- "MES"
colnames(dados)[2] <- "valortotal"

dados$valortotal <- as.numeric(dados$valortotal)

dados<- arrange(dados, valortotal)
dados <- dados[order(dados$valortotal), ]

dados$MES <- factor(dados$MES, levels = dados$MES)


ggplot(dados, aes(x = MES, y = valortotal, fill = MES)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = round(valortotal, 2)), size = 4, vjust = -0.3) +
  scale_fill_manual(values = c("blue", "blue", "blue", "green")) +
  labs(title = "Billing Cloud Costs", x = "Mês", y = "Gasto mensal") +
  theme_minimal()

#comparando o mês de novembro a previsão e o gasto do grupo até o dia 18/11

nome <- c("custo_atual","previsão")
prev_custo <- data.frame(previsao_lm)
custo_atual<- data.frame(totalNovembro)
nome_custo <- data.frame(nome)
mes1 <-  c("novembro","novembro")
custo <- rbind(custo_atual$totalNovembro, prev_custo$previsao_lm)
comparar1 <- data.frame(custo,mes1,nome)
comparar1

colnames(comparar1)[1] <- "custo"
colnames(comparar1)[2] <- "previsao"
colnames(comparar1)[3] <- "identificacao_custo"

ggplot(comparar1, aes(x = identificacao_custo, y = custo, fill = identificacao_custo)) +
  geom_bar(stat = "identity", width = 0.6) +
  geom_text(aes(label = round(custo, 2)), size = 4) +
  coord_flip() + 
  labs(title = "Comparação de custos: Atual (18/11) vs Previsão do mês de novembro",
       x = "Identificação do Custo",
       y = "Valor do Custo",
       fill = "Tipo de Custo") +
  theme_minimal()



# previsões até agosto do próximo ano do grupo
novos_meses <- 11:20
previsoes <- predict(modelo_lm, newdata = data.frame(tempo1 = novos_meses))


meses_futuros <- c("novembro", "dezembro", "janeiro", "fevereiro", "março", "abril", 
                   "maio", "junho", "julho", "agosto")
dados_previsoes <- data.frame(MES = meses_futuros, valortotal = previsoes)


dados_previsoes$MES <- factor(dados_previsoes$MES, levels = meses_futuros)


ggplot(dados_previsoes, aes(x = MES, y = valortotal)) +
  geom_bar(stat = "identity", fill = "green") +
  geom_text(aes(label = round(valortotal,2)), size = 4, vjust = -0.3) +
  labs(title = "Billing Cloud Costs (Previsões até agosto do próximo ano)",
       x = "Mês",
       y = "Gasto mensal") +
  theme_minimal()

# distribuição dos custos por serviço (grupo)

custo_total_servicos <- c(totalEC2Other, totalEC2, totalVPC)

nomes_servicos <- c("EC2 Other", "EC2", "VPC")

percentuais <- round(custo_total_servicos / sum(custo_total_servicos) * 100, 1)

rotulos <- paste(nomes_servicos, "(",percentuais,"%)")

pie(custo_total_servicos, labels = rotulos, main = "Distribuição de Gastos por Serviço na AWS (Agosto a Outubro)", col = rainbow(length(custo_total_servicos)))


#Juliana

totalJuliana <- c(dadosJuliana[4,2], dadosJuliana[4,3], dadosJuliana[4,4])

totalJulianaDF <- data.frame(custo_Juliana = totalJuliana)


modelo_lm_Juliana <- lm(custo_Juliana ~ tempo1, data = totalJulianaDF)

previsao_lm_Juliana <- predict(modelo_lm_Juliana, newdata = data.frame(tempo1 = 11))  

previsaoJuliana <- c(totalJuliana, previsao_lm_Juliana)

previsaoJulianaDF <- data.frame(mes = mes, valortotalJuliana = previsaoJuliana)


previsaoJulianaDF$valortotaJulianal <- as.numeric(previsaoJulianaDF$valortotalJuliana)
previsaoJulianaDF <- previsaoJulianaDF[order(previsaoJulianaDF$valortotalJuliana), ]
previsaoJulianaDF$mes <- factor(previsaoJulianaDF$mes, levels = previsaoJulianaDF$mes)

ggplot(previsaoJulianaDF, aes(x = mes, y = valortotalJuliana, fill = mes)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = round(valortotalJuliana, 2)), size = 4, vjust = -0.3) +
  scale_fill_manual(values = c("blue", "blue", "blue", "green")) +
  labs(title = "Gastos Mensais de Juliana (Cloud Billing)", x = "Mês", y = "Gasto mensal") +
  theme_minimal()

#Giorgio

totalGiorgio <- c(dadosGiorgio[4,2], dadosGiorgio[4,3], dadosGiorgio[4,4])

totalGiorgioDF <- data.frame(custo_Giorgio = totalGiorgio)

modelo_lm_Giorgio <- lm(custo_Giorgio ~ tempo1, data = totalGiorgioDF)

previsao_lm_Giorgio <- predict(modelo_lm_Giorgio, newdata = data.frame(tempo1 = 11))
previsaoGiorgio <- c(totalGiorgio, previsao_lm_Giorgio)


previsaoGiorgioDF <- data.frame(mes = mes, valortotalGiorgio = previsaoGiorgio)

previsaoGiorgioDF$mes <- factor(previsaoGiorgioDF$mes, levels = c("agosto", "setembro", "outubro", "novembro"))

ggplot(previsaoGiorgioDF, aes(x = mes, y = valortotalGiorgio, fill = mes)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = round(valortotalGiorgio, 2)), size = 4, vjust = -0.3) + 
  scale_fill_manual(values = c("blue", "blue", "blue", "green")) +
  labs(title = "Gastos Mensais de Giorgio (Cloud Billing)", x = "Mês", y = "Gasto mensal") +
  theme_minimal()

#Leandro

totalLeandro <- c(dadosLeandro[4,2], dadosLeandro[4,3], dadosLeandro[4,4])

totalLeandroDF <- data.frame(custo_Leandro = totalLeandro)

modelo_lm_Leandro <- lm(custo_Leandro ~ tempo1, data = totalLeandroDF)

previsao_lm_Leandro <- predict(modelo_lm_Leandro, newdata = data.frame(tempo1 = 11))
previsaoLeandro <- c(totalLeandro, previsao_lm_Leandro)

previsaoLeandroDF <- data.frame(mes = mes, valortotalLeandro = previsaoLeandro)

previsaoLeandroDF$mes <- factor(previsaoLeandroDF$mes, levels = c("agosto", "setembro", "outubro", "novembro"))

ggplot(previsaoLeandroDF, aes(x = mes, y = valortotalLeandro, fill = mes)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = round(valortotalLeandro, 2)), size = 4, vjust = -0.3) + 
  scale_fill_manual(values = c("blue", "blue", "blue", "green")) +
  labs(title = "Gastos Mensais de Leandro (Cloud Billing)", x = "Mês", y = "Gasto mensal") +
  theme_minimal()

# Nicolas
totalNicolas <- c(dadosNicolas[4,2], dadosNicolas[4,3], dadosNicolas[4,4])

totalNicolasDF <- data.frame(custo_Nicolas = totalNicolas)

modelo_lm_Nicolas <- lm(custo_Nicolas ~ tempo1, data = totalNicolasDF)

previsao_lm_Nicolas <- predict(modelo_lm_Nicolas, newdata = data.frame(tempo1 = 11))
previsaoNicolas <- c(totalNicolas, previsao_lm_Nicolas)

previsaoNicolasDF <- data.frame(mes = mes, valortotalNicolas = previsaoNicolas)

previsaoNicolasDF$mes <- factor(previsaoNicolasDF$mes, levels = c("agosto", "setembro", "outubro", "novembro"))

ggplot(previsaoNicolasDF, aes(x = mes, y = valortotalNicolas, fill = mes)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = round(valortotalNicolas, 2)), size = 4, vjust = -0.3) + 
  scale_fill_manual(values = c("blue", "blue", "blue", "green")) +
  labs(title = "Gastos Mensais de Nicolas (Cloud Billing)", x = "Mês", y = "Gasto mensal") +
  theme_minimal()

# Fernando
totalFernando <- c(dadosFernando[4,2], dadosFernando[4,3], dadosFernando[4,4])

totalFernandoDF <- data.frame(custo_Fernando = totalFernando)

modelo_lm_Fernando <- lm(custo_Fernando ~ tempo1, data = totalFernandoDF)

previsao_lm_Fernando <- predict(modelo_lm_Fernando, newdata = data.frame(tempo1 = 11))
previsaoFernando <- c(totalFernando, previsao_lm_Fernando)

previsaoFernandoDF <- data.frame(mes = mes, valortotalFernando = previsaoFernando)

previsaoFernandoDF$mes <- factor(previsaoFernandoDF$mes, levels = c("agosto", "setembro", "outubro", "novembro"))

ggplot(previsaoFernandoDF, aes(x = mes, y = valortotalFernando, fill = mes)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label = round(valortotalFernando, 2)), size = 4, vjust = -0.3) + 
  scale_fill_manual(values = c("blue", "blue", "blue", "green")) +
  labs(title = "Gastos Mensais de Fernando (Cloud Billing)", x = "Mês", y = "Gasto mensal") +
  theme_minimal()



