import pandas as pd;
import psutil;
import boto3;
from botocore.exceptions import ClientError;
import os;
import logging;

dados_cpu = []
dados_ram = []
dados_rede = []

i = 0
while i < 5:
    dados_cpu.append(psutil.cpu_percent(interval = 1))
    dados_ram.append(psutil.virtual_memory().used / (1024 ** 3))
    dados_rede.append(psutil.net_io_counters().bytes_recv)
    i+= 1

df = pd.DataFrame({'CPU%': dados_cpu,
                   'RAMGB': dados_ram,
                   'REDE_RECV': dados_rede})

df.to_json('dadosColetados.json', index=False)

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

upload_file('dadosColetados.json', 's3safeserver-raw')
