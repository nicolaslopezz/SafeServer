import psutil
import time
import mysql.connector
from jira import JIRA
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import pandas as pd
import boto3
from botocore.exceptions import ClientError
import os
import logging
from datetime import datetime

# Limites dos componentes para usar como parâmetro de chamado
limiteCPU = 75.0 
limiteMEM = 85.0
limiteREDE = 1.0  # GB

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'SafeServerUser',
    'password': 'safeserver123',
    'database': 'SafeServer'
}

servidor_id = 1

# Crie o cliente usando o token de autenticação do Slack
client = WebClient(token='')

# Função para enviar a mensagem diretamente
def enviar_mensagem(categoria):
    try:
        # Configurar o envio da mensagem para o canal especificado
        response = client.chat_postMessage(
        channel='',
        text=f"⚠️ *Alerta de Uso* ⚠️\n\n"
            f"💻 Categoria: *{categoria}*\n"
            f"🔧 Chamado Aberto no Servidor: *{servidor_id}*\n"
            f"📌 Por favor, verifique imediatamente!"
)
        print(f"Mensagem enviada: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Erro ao enviar mensagem: {e.response['error']}")

# Configurações do Jira
jira_options = {
    'server': 'https://safe-server.atlassian.net/'  # Substitua pelo seu domínio
}

email_jira = ''  # Substitua pelo seu e-mail
api_token = ''  # Substitua pelo seu token de API
jira = JIRA(options=jira_options, basic_auth=(email_jira, api_token))

    # Configuração das credenciais temporárias da AWS
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
AWS_SESSION_TOKEN = ''  # Coloque aqui o token de sessão
AWS_REGION = 'us-east-1'  # Defina a região da AWS

#Array para enviar os dados para o bucket
dados_cpu = []
dados_uso_ram = []
dados_livre_ram = []
dados_ram_perc = []
dados_rede_recebidos = []
dados_rede_enviados = []
data_hora_atual = []
dados_id_servidor = []

# Função para configurar o cliente S3 usando credenciais temporárias da AWS
def create_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN,  # Adicionar o token de sessão
        region_name=AWS_REGION
    )

def abrir_chamado_jira(categoria, tipo, limite_atual, servidor_id):
   

    issue_dict = {
        'project': {'key': 'SUP'},  # Substitua pela chave do seu projeto
        'summary': f"Servidor {servidor_id} - Limite de {categoria} excedido",
        'description':f"O uso de {categoria} ultrapassou o limite de {tipo}. Utilização atual: {limite_atual:.2f}%, no servidor{servidor_id}." ,
        'issuetype': {'name': 'Task'}
    }
    
    # Chama a função para enviar a mensagem do slack
    enviar_mensagem(categoria)

    try:
        new_issue = jira.create_issue(fields=issue_dict)
        print(f"Chamado criado com sucesso no Jira para {categoria}: {new_issue.key}")
    except Exception as e:
        print(f"Falha ao criar chamado para {categoria}. Erro: {e}")

def monitorar_e_enviar_dados(servidor_id):
    contador_mem = 0
    contador_cpu = 0
    contador_rede_enviados = 0
    contador_rede_recebidos = 0
    meusql = mysql.connector.connect(**db_config)
    meucursor = meusql.cursor()

    print("Conexão com o banco de dados bem-sucedida!.")

    while True:
        # Coletando dados e arredondando para 2 casas decimais
        Porcentagem_CPU = round(psutil.cpu_percent(interval=1), 2)
        GB_RAM_uso = round(psutil.virtual_memory().used / (1024 ** 3), 2)
        GB_RAM_livre = round(psutil.virtual_memory().free / (1024 ** 3), 2)
        Porcentagem_RAM_uso = round(psutil.virtual_memory().percent, 2)
        GB_rede_recebidos = round(psutil.net_io_counters().bytes_recv / (1024 ** 3), 2)
        GB_rede_enviados = round(psutil.net_io_counters().bytes_sent / (1024 ** 3), 2)
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Formato: YYYY-MM-DD HH:MM:SS

        dados_cpu.append(Porcentagem_CPU)
        data_hora_atual.append(data_hora)
        dados_livre_ram.append(GB_RAM_livre)
        dados_uso_ram.append(GB_RAM_uso)
        dados_ram_perc.append(Porcentagem_RAM_uso)
        dados_rede_recebidos.append(GB_rede_recebidos)
        dados_rede_enviados.append(GB_rede_enviados)
        dados_id_servidor.append(servidor_id)

                # Criar DataFrame e salvar como JSON
        df = pd.DataFrame({
            'ID_SERVIDOR': dados_id_servidor,
            'CPU%': dados_cpu,
            'DataHora': data_hora_atual,
            'RAM-GB-Livre': dados_livre_ram,
            'RAM-GB-USO': dados_uso_ram,
            'RAM%': dados_ram_perc,
            'REDE_REC': dados_rede_recebidos, 
            'REDE_ENV': dados_rede_enviados })
        df.to_json('dadosColetados.json', orient="records", lines="false")

        # Função para upload do arquivo para o bucket S3
        def upload_file(file_name, bucket, object_name=None):
            if object_name is None:
                object_name = os.path.basename(file_name)

            s3_client = create_s3_client()
            try:
                response = s3_client.upload_file(file_name, bucket, object_name)
            except ClientError as e:
                logging.error(e)
                return False
            return True

        # Upload do arquivo
        upload_file('dadosColetados.json', 'safeserver-s3-raw')

        fk_servidor = servidor_id

        # Correção na consulta SQL
        query = '''
        INSERT INTO registro (
            percent_use_cpu, 
            percent_use_ram,
            uso_ram_gb,
            livre_ram_gb,
            recebido_rede,
            enviado_rede,
            fkServidor
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        values = (Porcentagem_CPU,Porcentagem_RAM_uso, GB_RAM_uso, GB_RAM_livre, GB_rede_recebidos, GB_rede_enviados, fk_servidor)

        meucursor.execute(query, values)
        meusql.commit()

        print(f"Dados inseridos: CPU: {Porcentagem_CPU:.1f}%, RAM Usada: {GB_RAM_uso:.1f} GB, "
              f"RAM Livre: {GB_RAM_livre:.1f} GB, Percentual de RAM: {Porcentagem_RAM_uso:.1f}%, "
              f"Dados de rede recebidos: {GB_rede_recebidos:.1f} GB, Dados de rede enviados: {GB_rede_enviados:.1f} GB")

          # Verificação de limites e contagem de capturas seguidas
        if Porcentagem_CPU > limiteCPU:
            contador_cpu += 1
        else:
            contador_cpu = 0

        if Porcentagem_RAM_uso > limiteMEM:
            contador_mem += 1
        else:
            contador_mem = 0
        
        if GB_rede_enviados > limiteREDE:
            contador_rede_enviados += 1
        else:
            contador_rede_enviados = 0

        if GB_rede_recebidos > limiteREDE:
            contador_rede_recebidos += 1
        else:
            contador_rede_recebidos = 0

        query = '''
            SELECT idRegistro FROM registro WHERE fkServidor = 1 ORDER BY dtHora Desc LIMIT 1;
        '''

        values = (fk_servidor)
        meusql2 = mysql.connector.connect(**db_config)

        cursor2 = meusql2.cursor(buffered=True) 
        cursor2.execute(query)
        meusql2.commit()
        idUltimoRegistro = cursor2.fetchall()[0][0]


        # Verifica se chegou a 10 capturas seguidas acima do limite e abre chamado para rede enviada
        if contador_rede_enviados >= 10:
            query = '''
            INSERT INTO alerta (componente, fkRegistro) VALUES ("rede-enviada", %s)
            '''
            values = [idUltimoRegistro]
            meucursor.execute(query, values)

            abrir_chamado_jira(
                "Rede Enviada", 
                "GB Enviados", 
                GB_rede_enviados, 
                servidor_id
            )
            contador_rede_enviados = 0

# Verifica se chegou a 10 capturas seguidas acima do limite e abre chamado para rede recebida
        if contador_rede_recebidos >= 10:
            query = '''
            INSERT INTO alerta (componente, fkRegistro) VALUES ("rede-recebida", %s)
            '''
            values = [idUltimoRegistro]
            meucursor.execute(query, values)

            abrir_chamado_jira(
                "Rede Recebida", 
                "GB Recebidos", 
                 GB_rede_recebidos, 
                servidor_id
            )
            contador_rede_recebidos = 0

            # Verifica se chegou a 10 capturas seguidas acima do limite e abre chamado
        if contador_cpu >= 10:
                query = '''
                INSERT INTO alerta (componente, fkRegistro) VALUES ("cpu", %s)
                '''
                values = [idUltimoRegistro]
                meucursor.execute(query, values)


                abrir_chamado_jira("CPU", limiteCPU, Porcentagem_CPU, servidor_id)
                meusql.commit()
                contador_cpu = 0  

        if contador_mem >= 10:
                query = '''
                INSERT INTO alerta (componente, fkRegistro) VALUES ("ram", %s)
                '''
                values = [idUltimoRegistro]
                meucursor.execute(query, values)
                idUltimoRegistro = meucursor.fetchall()

                abrir_chamado_jira("Memória", limiteMEM, Porcentagem_RAM_uso, servidor_id)
                contador_mem = 0  

        time.sleep(1)

            # Verifica se chegou a 10 capturas seguidas acima do limite e abre chamado

# Chamada da função para monitorar e enviar dados
monitorar_e_enviar_dados(servidor_id)
