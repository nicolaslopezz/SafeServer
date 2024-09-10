import psutil
import time
import mysql.connector

# Não esqueça de dar pip install em todas as bibliotecas utilizadas abaixo.
import requests
import json
from dotenv import load_dotenv
import os


#carregando o ambiente onde estão as credenciais
load_dotenv('configuracoes.env')

#pegando as credenciais definidas no arquivo "ambiente.env"
email_jira = os.getenv('JIRA_EMAIL')
chave_jira = os.getenv('CHAVE_DO_JIRA')


# Limites dos componentes para usar como parametro de chamado
limiteCPU = 90.0
limiteMEM = 85.0
limiteDSK = 85.0

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Numero2005',
    'database': 'SafeServer'
}


# Em 'Auth", não esqueça de colocar o email que você usa na equipe do Jira
# Ainda em 'Auth', coloque o Token do Projeto que enviei por EMAIL

def abrir_chamado_jira(categoria, tipo, limite_atual):
    url = "https://safeserver.atlassian.net/rest/api/2/issue"
    auth = (email_jira, chave_jira)
    headers = {"Content-Type": "application/json"}
    descricao = f"O uso de {categoria} ultrapassou o limite de {tipo}. Utilização atual: {limite_atual:.2f}%."

    dados_chamado = {
        "fields": {
            "project": {"key": "SAF"},
            "summary": f"Limite de {categoria} excedido - Uso de {limite_atual:.2f}%",
            "description": descricao,
            "issuetype": {"name": "Task"}
        }
    }

    response = requests.post(url, auth=auth, headers=headers, data=json.dumps(dados_chamado))
    
    if response.status_code == 201:
        print(f"Chamado criado com sucesso no Jira para {categoria}!")
    else:
        print(f"Falha ao criar chamado para {categoria}. Status: {response.status_code}, Erro: {response.text}")



def monitorar_e_enviar_dados():
    meusql = mysql.connector.connect(**db_config)
    meucursor = meusql.cursor()

    print("Conexão com o banco de dados bem-sucedida.")

    while True:
        memoria = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        disco = psutil.disk_usage('/')

        total_memoriagb = memoria.total / (1024 ** 3)
        used_memoriagb = memoria.used / (1024 ** 3)
        total_discogb = disco.total / (1024 ** 3)
        used_discogb = disco.used / (1024 ** 3)
        livre_memoriagb = total_memoriagb - used_memoriagb
        livre_discogb = total_discogb - used_discogb

        query = '''
        INSERT INTO registro (percent_use_cpu, uso_ram_gb, livre_ram_gb, total_ram_gb, uso_disco_gb, livre_disco_gb, total_disco_gb, fkServidor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (cpu, used_memoriagb, livre_memoriagb, total_memoriagb, used_discogb, livre_discogb, total_discogb, 2)

        meucursor.execute(query, values)
        meusql.commit()

        print(f"Dados inseridos: CPU: {cpu:.1f}%, RAM Usada: {used_memoriagb:.1f} GB, RAM Livre: {livre_memoriagb:.1f} GB, "
              f"Total RAM: {total_memoriagb:.1f} GB, Disco Usado: {used_discogb:.1f} GB, Disco Livre: {livre_discogb:.1f} GB, "
              f"Total Disco: {total_discogb:.1f} GB")
        
        if cpu > limiteCPU:
            abrir_chamado_jira("CPU", cpu, limiteCPU)
        
        if (used_memoriagb / total_memoriagb * 100) > limiteMEM:
            abrir_chamado_jira("Memória", (used_memoriagb / total_memoriagb * 100), limiteMEM)
        
        if (used_discogb / total_discogb * 100) > limiteDSK:
            abrir_chamado_jira("Disco", (used_discogb / total_discogb * 100), limiteDSK)

        time.sleep(2)

# Chamada da função para monitorar e enviar dados
monitorar_e_enviar_dados()
