import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

file_path = "C:\\Users\\JuuhF\\Videos\\dadosColetados.xlsx"

try:
    df = pd.read_excel(file_path)
    
    # convertendo para tipo numérico
    df['percent_use_cpu'] = pd.to_numeric(df['percent_use_cpu'], errors='coerce')
    df['recebido_rede'] = pd.to_numeric(df['recebido_rede'], errors='coerce')
    # remover NaN
    df = df.dropna(subset=['percent_use_cpu', 'recebido_rede'])
    

except FileNotFoundError:
    print(f"Erro: Arquivo '{file_path}' não encontrado.")
except Exception as e:
    print(f"Ocorreu um erro ao importar o arquivo: {e}")

x = df['percent_use_cpu'].values.reshape(-1, 1)  #  variável independente
y = df['recebido_rede'].values  # variável dependente

# divisão dos dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=50)

# treinamento o modelo de regressão linear
modelo = LinearRegression()
modelo.fit(X_train, y_train)


y_pred = modelo.predict(X_test)
r2_score = modelo.score(X_test, y_test)
print(f"R² do modelo: {r2_score}")

# Regressão linear
plt.scatter(x, y, color='blue')
plt.plot(x, modelo.predict(x), color='red')
plt.title('Regressão Linear - CPU (%) vs REDE_RECEBIDA (GB)')
plt.xlabel('CPU%')
plt.ylabel('REDE_REC')
plt.show()
