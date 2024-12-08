import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pymysql

file_path = "C:\\Users\\JuuhF\\Videos\\dadosColetados.xlsx"

try:
    df = pd.read_excel(file_path)

    df['percent_use_cpu'] = pd.to_numeric(df['percent_use_cpu'], errors='coerce')
    df['recebido_rede'] = pd.to_numeric(df['recebido_rede'], errors='coerce')
    
    # Remover NaN
    df = df.dropna(subset=['percent_use_cpu', 'recebido_rede'])
except FileNotFoundError:
    print(f"Erro: Arquivo '{file_path}' não encontrado.")
except Exception as e:
    print(f"Ocorreu um erro ao importar o arquivo: {e}")


x = df['recebido_rede'].values.reshape(-1, 1)  
y = df['percent_use_cpu'].values 


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=50)

modelo = LinearRegression()
modelo.fit(X_train, y_train)

y_pred = modelo.predict(X_test)
r2_score = modelo.score(X_test, y_test)
print(f"R² do modelo: {r2_score}")


plt.scatter(x, y, color='blue')
plt.plot(x, modelo.predict(x), color='red')
plt.title('Regressão Linear - REDE_RECEBIDA (GB) vs CPU (%)')
plt.xlabel('REDE_RECEBIDA (GB)')
plt.ylabel('CPU%')
plt.show()

import pymysql

conn = pymysql.connect(
    host='3.210.133.0',        
    user='root',               
    password='urubu100',    
    database='SafeServer'      
)


cursor = conn.cursor()

for i in range(len(X_test)):
    cursor.execute("""
        INSERT INTO regressao_linear (percent_use_cpu, recebido_rede, predicted_value,R)
        VALUES (%s, %s, %s,%s)
    """, (y_test[i], X_test[i][0], y_pred[i],r2_score))  


conn.commit()

print("Dados inseridos na tabela")


cursor.close()
conn.close()
