import psutil
import time
import mysql.connector

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'palmeiras21',
    'database': 'SafeServer'
}

# Função para monitorar e enviar dados para o banco de dados
def monitorar_e_enviar_dados(servidor_id):
    meusql = mysql.connector.connect(**db_config)
    meucursor = meusql.cursor()

    print(f"Conexão com o banco de dados bem-sucedida para o servidor {servidor_id}.")

    while True:
        memoria = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        

        servidor_id = 2

        total_memoriagb = memoria.total / (1024 ** 3)
        used_memoriagb = round(memoria.used / (1024 ** 3),2)
        livre_memoriagb = round((total_memoriagb - used_memoriagb),2)
        

        query = '''
        INSERT INTO registro (percent_use_cpu, uso_ram_gb, livre_ram_gb, fkServidor)
        VALUES (%s, %s, %s, %s)
        '''
        values = (cpu, used_memoriagb, livre_memoriagb, servidor_id)

        meucursor.execute(query, values)
        meusql.commit()

        # Impressão dos dados inseridos
        print(f"Dados inseridos: CPU: {cpu:.1f}%, RAM Usada: {used_memoriagb:.1f} GB, RAM Livre: {livre_memoriagb:.1f} GB, "
              f"Total RAM: {total_memoriagb:.1f} GB ")

        time.sleep(2)

# Chamada da função para monitorar e enviar dados
monitorar_e_enviar_dados('MUDAR PARA O ID DO SERVIDOR DA SUA MAQUINA(1 OU 2)')


