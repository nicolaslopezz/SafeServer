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
    'user': 'root',
    'password': '#Gf49053476881',
    'database': 'SafeServer'
}

servidor_id = 1

# Crie o cliente usando o token de autenticação do Slack
client = WebClient(token='')

# Configuração do Jira
jira_options = {
    'server': ''  # Substitua pelo seu domínio
}
email_jira = ''  # Substitua pelo seu e-mail
api_token = ''  # Substitua pelo seu token de API
jira = JIRA(options=jira_options, basic_auth=(email_jira, api_token))

# Configuração das credenciais temporárias da AWS
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
AWS_SESSION_TOKEN = ''  # Coloque aqui o token de sessão
AWS_REGION = 'us-west-1'  # Defina a região da AWS

dados_cpu = []
dados_uso_ram = []
dados_livre_ram = []
dados_ram_perc = []
dados_rede_recebidos = []
dados_rede_enviados = []
data_hora_atual = []
dados_id_servidor = []

#---------Captura dos dados----------

def capturar_dados():
    Porcentagem_CPU = round(psutil.cpu_percent(interval=1), 2)
    GB_RAM_uso = round(psutil.virtual_memory().used / (1024 ** 3), 2)
    GB_RAM_livre = round(psutil.virtual_memory().free / (1024 ** 3), 2)
    Porcentagem_RAM_uso = round(psutil.virtual_memory().percent, 2)
    GB_rede_recebidos = round(psutil.net_io_counters().bytes_recv / (1024 ** 3), 2)
    GB_rede_enviados = round(psutil.net_io_counters().bytes_sent / (1024 ** 3), 2)
    data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Armazena os dados nos arrays
    dados_cpu.append(Porcentagem_CPU)
    data_hora_atual.append(data_hora)
    dados_livre_ram.append(GB_RAM_livre)
    dados_uso_ram.append(GB_RAM_uso)
    dados_ram_perc.append(Porcentagem_RAM_uso)
    dados_rede_recebidos.append(GB_rede_recebidos)
    dados_rede_enviados.append(GB_rede_enviados)
    dados_id_servidor.append(servidor_id)


    return Porcentagem_CPU, GB_RAM_uso, GB_RAM_livre, Porcentagem_RAM_uso, GB_rede_recebidos, GB_rede_enviados

# ----------Upload do JSON-----------

def create_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        region_name=AWS_REGION
    )

def salvar_dados_json():

    df = pd.DataFrame({
        'ID_SERVIDOR': dados_id_servidor,
        'CPU%': dados_cpu,
        'DataHora': data_hora_atual,
        'RAM-GB-Livre': dados_livre_ram,
        'RAM-GB-USO': dados_uso_ram,
        'RAM%': dados_ram_perc,
        'REDE_REC': dados_rede_recebidos,
        'REDE_ENV': dados_rede_enviados
    })
    df.to_json('dadosColetados.json', orient="records", lines="false")

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = create_s3_client()
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# -------------Integração com o Jira--------------

def enviar_mensagem(categoria, servidor_id):
    try:
        response = client.chat_postMessage(channel='', text=f'Alerta! O uso de {categoria} - Chamado aberto - Servidor {servidor_id}')
        print(f"Mensagem enviada: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Erro ao enviar mensagem: {e.response['error']}")

def abrir_chamado_jira(categoria, tipo, limite_atual, servidor_id):
    descricao = f"O uso de {categoria} ultrapassou o limite de {tipo}. Utilização atual: {limite_atual:.2f}%, no servidor."
    issue_dict = {
        'project': {'key': 'SUP'},  # Substitua pela chave do seu projeto
        'summary': f"Servidor {servidor_id} - Limite de {categoria} excedido - Uso de {limite_atual:.2f}%",
        'description': descricao,
        'issuetype': {'name': 'Task'}
    }

    enviar_mensagem(categoria, servidor_id)

    try:
        new_issue = jira.create_issue(fields=issue_dict)
        print(f"Chamado criado com sucesso no Jira para {categoria}: {new_issue.key}")
    except Exception as e:
        print(f"Falha ao criar chamado para {categoria}. Erro: {e}")

# ----------Monitoramento e upload do arquivo-----------

def monitorar_e_enviar_dados(servidor_id):
    contador_cpu = contador_mem = contador_rede = 0
    meusql = mysql.connector.connect(**db_config)
    meucursor = meusql.cursor()
    print("Conexão com o banco de dados bem-sucedida!")

    while True:
        # Captura os dados
        Porcentagem_CPU, GB_RAM_uso, GB_RAM_livre, Porcentagem_RAM_uso, GB_rede_recebidos, GB_rede_enviados = capturar_dados()

        salvar_dados_json()
        upload_file('dadosColetados.json', 's3safeserver-raw')

        # Insere os dados no banco de dados
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
        values = (Porcentagem_CPU, Porcentagem_RAM_uso, GB_RAM_uso, GB_RAM_livre, GB_rede_recebidos, GB_rede_enviados, servidor_id)
        meucursor.execute(query, values)
        meusql.commit()

        print(f"Dados inseridos: CPU: {Porcentagem_CPU:.1f}%, RAM Usada: {GB_RAM_uso:.1f} GB, RAM Livre: {GB_RAM_livre:.1f} GB, "
              f"Percentual de RAM: {Porcentagem_RAM_uso:.1f}%, Dados de rede recebidos: {GB_rede_recebidos:.1f} GB, "
              f"Dados de rede enviados: {GB_rede_enviados:.1f} GB")

        # Verificação de limites e contagem de capturas seguidas
        contador_cpu = contador_cpu + 1 if Porcentagem_CPU > limiteCPU else 0
        contador_mem = contador_mem + 1 if Porcentagem_RAM_uso > limiteMEM else 0
        contador_rede = contador_rede + 1 if GB_rede_enviados > limiteREDE or GB_rede_recebidos > limiteREDE else 0

        # Verifica se chegou a 10 capturas seguidas acima do limite e abre chamado
        if contador_cpu >= 10:
            abrir_chamado_jira("CPU", limiteCPU, Porcentagem_CPU, servidor_id)
            contador_cpu = 0
        if contador_mem >= 10:
            abrir_chamado_jira("Memória", limiteMEM, Porcentagem_RAM_uso, servidor_id)
            contador_mem = 0
        if contador_rede >= 10:
            abrir_chamado_jira("Rede", limiteREDE, max(GB_rede_enviados, GB_rede_recebidos), servidor_id)
            contador_rede = 0

        time.sleep(1)

# Chama a função principal para monitorar e enviar dados
monitorar_e_enviar_dados(servidor_id)
