summary(dados1)

dados1

head(dados1)

correlacao_cpu_ram <- cor(dados1$CPU., dados1$RAM.)
correlacao_cpu_rede <- cor(dados1$CPU., dados1$REDE_REC)
cat("Correlação entre CPU e RAM em uso:", correlacao_cpu_ram, "\n")
cat("Correlação entre CPU e tráfego de rede recebida:", correlacao_cpu_rede, "\n")

library(ggplot2)

#Disperção entre o uso da CPU em relação ao tráfego de Rede Recebida
ggplot(dados1, aes(x = REDE_REC, y = CPU.)) +
  geom_point(color = "darkblue") +
  geom_smooth(method = "lm", se = FALSE, color = "red") +
  labs(title = "Relação entre Uso da CPU e Tráfego de Rede Recebida",
       x = "Tráfego de Rede Recebida",
       y = "Uso da CPU (%)") +
  theme_minimal()

# Gráfico de uso da CPU ao longo do tempo
ggplot(dados1, aes(x = as.POSIXct(DataHora, format="%Y-%m-%d %H:%M:%S"), y = CPU.)) +
  geom_line(color = "blue") +
  labs(title = "Tendência do Uso da CPU ao Longo do Tempo",
       x = "Data e Hora",
       y = "Uso de CPU (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

#Disperção do uso de CPU em relação so uso de RAM_%
ggplot(dados1, aes(x = RAM., y = CPU.)) +
  geom_point(color = "blue") +
  geom_smooth(method = "loess", color = "red", se = FALSE) + # Linha de tendência opcional
  labs(title = "Relação entre Uso de CPU e Uso de RAM",
       x = "Uso de RAM (%)",
       y = "Uso de CPU (%)") +
  theme_minimal()

dados_ram <- data.frame(
  Categoria = c("RAM Livre", "RAM Usada"),
  Valor = c(sum(dados1$RAM.GB.Livre), sum(dados1$RAM.GB.USO))
)

#Gráfico de pizza do uso de RAMGB uso e livre ao total
ggplot(dados_ram, aes(x = "", y = Valor, fill = Categoria)) +
  geom_bar(width = 1, stat = "identity") +
  coord_polar("y") +
  labs(title = "Distribuição do Uso de RAM (GB)") +
  theme_void() +
  scale_fill_manual(values = c("gray", "darkblue")) +
  geom_text(aes(label = paste0(round(Valor), "GB")),
            position = position_stack(vjust = 0.5))

