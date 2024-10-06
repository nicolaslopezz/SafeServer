import pandas as pd
import psutil
import boto3
from botocore.exceptions import ClientError
import os
import logging

# Definir credenciais da AWS
AWS_ACCESS_KEY = 'your_access_key'
AWS_SECRET_KEY = 'your_secret_key'
AWS_REGION = 'your_aws_region'  # us-west-1

# Função para configurar o cliente S3 usando credenciais da AWS
def create_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
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

    
      
    i += 1

# Criar DataFrame e salvar como CSV
df = pd.DataFrame({
    'CPU%': dados_cpu,
    'RAM-GB-Livre': dados_livre_ram,
    'RAM-GB-USO': dados_uso_ram,
    'RAM%': dados_ram_perc,
    'REDE_REC': dados_rede_recebidos, 
    'REDE_ENV': dados_rede_enviados })
df.to_csv('dadosColetados.csv', index=False)

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
upload_file('dadosColetados.csv', 's3safeserver-raw')
