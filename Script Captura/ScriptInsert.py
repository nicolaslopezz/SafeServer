import psutil
import time
import mysql.connector

# Configurações do banco de dados
db_config = {
    'host': '',
    'user': 'root',
    'password': '',
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
        disco = psutil.disk_usage('/')

        servidor_id = '(ALTERAR PARA QUAL O ID DO SERVIDOR DA SUA MAQUINA(1 OU 2)'

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
        values = (cpu, used_memoriagb, livre_memoriagb, total_memoriagb, used_discogb, livre_discogb, total_discogb, servidor_id)

        meucursor.execute(query, values)
        meusql.commit()

        # Impressão dos dados inseridos
        print(f"Dados inseridos: CPU: {cpu:.1f}%, RAM Usada: {used_memoriagb:.1f} GB, RAM Livre: {livre_memoriagb:.1f} GB, "
              f"Total RAM: {total_memoriagb:.1f} GB, Disco Usado: {used_discogb:.1f} GB, Disco Livre: {livre_discogb:.1f} GB, "
              f"Total Disco: {total_discogb:.1f} GB")

        time.sleep(2)

# Chamada da função para monitorar e enviar dados
monitorar_e_enviar_dados('MUDAR PARA O ID DO SERVIDOR DA SUA MAQUINA(1 OU 2)')


