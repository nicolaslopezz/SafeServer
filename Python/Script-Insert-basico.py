import psutil
import time
import mysql.connector

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'batatas123',
    'database': 'SafeServer'
}

servidor_id = 1

# Função para monitorar e enviar dados para o banco de dados
def monitorar_e_enviar_dados(servidor_id):
    meusql = mysql.connector.connect(**db_config)
    meucursor = meusql.cursor()

    print(f"Conexão com o banco de dados bem-sucedida para o servidor {servidor_id}.")

    while True:
        # Coletando dados e arredondando para 2 casas decimais
        Porcentagem_CPU = round(psutil.cpu_percent(interval=1), 2)
        GB_RAM_uso = round(psutil.virtual_memory().used / (1024 ** 3), 2)
        GB_RAM_livre = round(psutil.virtual_memory().free / (1024 ** 3), 2)
        Porcentagem_RAM_uso = round(psutil.virtual_memory().percent, 2)
        GB_rede_recebidos = round(psutil.net_io_counters().bytes_recv / (1024 ** 3), 2)
        GB_rede_enviados = round(psutil.net_io_counters().bytes_sent / (1024 ** 3), 2)

        fk_servidor = servidor_id

        # Correção na consulta SQL
        query = '''
        INSERT INTO registro (
            percent_use_cpu,
            percent_use_ram, 
            uso_ram,
            livre_ram_gb,
            recebido_rede,
            enviado_rede,
            fkServidor
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        values = (Porcentagem_CPU, GB_RAM_uso, GB_RAM_livre, Porcentagem_RAM_uso, GB_rede_recebidos, GB_rede_enviados, fk_servidor)

        meucursor.execute(query, values)
        meusql.commit()

        print(f"Dados inseridos: CPU: {Porcentagem_CPU:.1f}%, RAM Usada: {GB_RAM_uso:.1f} GB, RAM Livre: {GB_RAM_livre:.1f} GB, "
              f"Percentual de RAM: {Porcentagem_RAM_uso:.1f}%, Dados de rede recebido: {GB_rede_recebidos:.1f} GB, "
              f"Dados de rede enviados: {GB_rede_enviados:.1f} GB")

        time.sleep(2)

monitorar_e_enviar_dados(servidor_id)