import pandas as pd
import psutil
import boto3
from botocore.exceptions import ClientError
import os
import logging
import datetime

# Definir credenciais temporárias da AWS (com token de sessão)
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
AWS_SESSION_TOKEN = ''  # Coloque aqui o token de sessão
AWS_REGION = 'us-west-1'  # Defina a região da AWS

# Função para configurar o cliente S3 usando credenciais temporárias da AWS
def create_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN,  # Adicionar o token de sessão
        region_name=AWS_REGION
    )

# Coletar dados do sistema
dados_cpu = []
dados_uso_ram = []
dados_livre_ram = []
dados_ram_perc = []
dados_rede_recebidos = []
dados_rede_enviados = []

i = 0
while i < 5:
# Armazenando dados arredondados
    dados_cpu.append(round(psutil.cpu_percent(), 2))
    dados_uso_ram.append(round(psutil.virtual_memory().used / (1024 ** 3), 2))
    dados_livre_ram.append(round(psutil.virtual_memory().free / (1024 ** 3), 2))
    dados_ram_perc.append(round(psutil.virtual_memory().percent, 2))
    dados_rede_recebidos.append(round(psutil.net_io_counters().bytes_recv / (1024 ** 3), 2)) 
    dados_rede_enviados.append(round(psutil.net_io_counters().bytes_sent / (1024 ** 3), 2))  
    data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Formato: YYYY-MM-DD HH:MM:SS
    i += 1

# Criar DataFrame e salvar como JSON
df = pd.DataFrame({
    'CPU%': dados_cpu,
    'DataHora': data_hora_atual,
    'RAM-GB-Livre': dados_livre_ram,
    'RAM-GB-USO': dados_uso_ram,
    'RAM%': dados_ram_perc,
    'REDE_REC': dados_rede_recebidos, 
    'REDE_ENV': dados_rede_enviados })
df.to_json('dadosColetados.json', index=False)

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
upload_file('dadosColetados.json', 's3safeserver-raw')