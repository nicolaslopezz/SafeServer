import psutil
import time
import mysql.connector
from jira import JIRA
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Limites dos componentes para usar como parâmetro de chamado
limiteCPU = 75.0 
limiteMEM = 85.0
limiteREDE = 1.0  # GB

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'batatas123',
    'database': 'SafeServer'
}

servidor_id = 1

# Crie o cliente usando o token de autenticação do Slack
client = WebClient(token='')

# Função para enviar a mensagem diretamente
def enviar_mensagem(categoria):
    try:
        # Envia uma mensagem para o canal especificado
        response = client.chat_postMessage(channel='', text=f'Alerta! O uso de {categoria} - Chamado aberto')
        print(f"Mensagem enviada: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Erro ao enviar mensagem: {e.response['error']}")

# Configurações do Jira
jira_options = {
    'server': ''  # Substitua pelo seu domínio
}

email_jira = ''  # Substitua pelo seu e-mail
api_token = ''  # Substitua pelo seu token de API
jira = JIRA(options=jira_options, basic_auth=(email_jira, api_token))

def abrir_chamado_jira(categoria, tipo, limite_atual):
    descricao = f"O uso de {categoria} ultrapassou o limite de {tipo}. Utilização atual: {limite_atual:.2f}%."
    
    issue_dict = {
        'project': {'key': 'SUP'},  # Substitua pela chave do seu projeto
        'summary': f"Limite de {categoria} excedido - Uso de {limite_atual:.2f}%",
        'description': descricao,
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
    meusql = mysql.connector.connect(**db_config)
    meucursor = meusql.cursor()

    print("Conexão com o banco de dados bem-sucedida.")

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

        print(f"Dados inseridos: CPU: {Porcentagem_CPU:.1f}%, RAM Usada: {GB_RAM_uso:.1f} GB, "
              f"RAM Livre: {GB_RAM_livre:.1f} GB, Percentual de RAM: {Porcentagem_RAM_uso:.1f}%, "
              f"Dados de rede recebidos: {GB_rede_recebidos:.1f} GB, Dados de rede enviados: {GB_rede_enviados:.1f} GB")

        if Porcentagem_CPU > limiteCPU:
            abrir_chamado_jira("CPU", limiteCPU, Porcentagem_CPU)

        elif Porcentagem_RAM_uso > limiteMEM:
            abrir_chamado_jira("Memória", limiteMEM, Porcentagem_RAM_uso)
        
        elif GB_rede_enviados > limiteREDE:
            abrir_chamado_jira("Rede - tráfego de entrada", limiteREDE, GB_rede_enviados)

        elif GB_rede_recebidos > limiteREDE:
            abrir_chamado_jira("Rede - tráfego de saída", limiteREDE, GB_rede_recebidos) 

        time.sleep(4)

# Chamada da função para monitorar e enviar dados
monitorar_e_enviar_dados(servidor_id)
