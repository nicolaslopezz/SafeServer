import psutil
import time
from jira import JIRA
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import threading  # Para monitoramento paralelo

# Limites dos componentes para usar como parâmetro de chamado
limiteCPU = 5.0 
limiteMEM = 85.0
limiteREDE = 0.1  # GB

# Configurações do Slack
client = WebClient(token='')  # Substitua com seu token

# Função para enviar a mensagem diretamente
def enviar_mensagem(categoria, servidor_id, data_hora):
    try:
        response = client.chat_postMessage(
            channel='C07MD4V0LET',  # Substitua com o canal do Slack
            text=f"⚠️ *Alerta de Uso* ⚠️\n\n"
                 f"📅 Data/Hora: *{data_hora}*\n"
                 f"💻 Categoria: *{categoria}*\n"
                 f"🔧 Chamado Aberto no Servidor: *{servidor_id}*\n"
                 f"📌 Por favor, verifique imediatamente!"
        )
        print(f"Mensagem enviada: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Erro ao enviar mensagem: {e.response['error']}")

# Configurações do Jira
jira_options = {
    'server': ''  # Substitua pelo seu domínio
}

email_jira = ''  # Substitua pelo seu e-mail
api_token =''  # Substitua pelo seu token de API
jira = JIRA(options=jira_options, basic_auth=(email_jira, api_token))

# Função para abrir um chamado no Jira
def abrir_chamado_jira(categoria, tipo, limite_atual, servidor_id, data_hora):
    issue_dict = {
        'project': {'key': 'SUP'},  # Substitua pela chave do seu projeto
        'summary': f"Servidor {servidor_id} - Limite de {categoria} excedido",
        'description': f"O uso de {categoria} ultrapassou o limite de {tipo}. Utilização atual: {limite_atual:.2f}%, no servidor {servidor_id}.\nData/Hora do Alerta: {data_hora}",
        'issuetype': {'name': 'Task'}
    }
    try:
        new_issue = jira.create_issue(fields=issue_dict)
        print(f"Chamado criado com sucesso no Jira para {categoria}: {new_issue.key}")
    except Exception as e:
        print(f"Falha ao criar chamado para {categoria}. Erro: {e}")
    # Enviar mensagem de alerta no Slack
    enviar_mensagem(categoria, servidor_id, data_hora)

# Função para monitorar e enviar dados para o Jira
def monitorar_e_enviar_dados(servidor_id):
    contador_cpu = 0
    contador_mem = 0
    contador_rede_enviados = 0
    contador_rede_recebidos = 0

    while True:
        # Coletando dados dos componentes
        Porcentagem_CPU = round(psutil.cpu_percent(interval=1), 2)
        GB_RAM_uso = round(psutil.virtual_memory().used / (1024 ** 3), 2)
        GB_RAM_livre = round(psutil.virtual_memory().free / (1024 ** 3), 2)
        Porcentagem_RAM_uso = round(psutil.virtual_memory().percent, 2)
        GB_rede_recebidos = round(psutil.net_io_counters().bytes_recv / (1024 ** 3), 2)
        GB_rede_enviados = round(psutil.net_io_counters().bytes_sent / (1024 ** 3), 2)
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Formato: YYYY-MM-DD HH:MM:SS

        print(f"Data/Hora: {data_hora} | CPU: {Porcentagem_CPU}% | RAM Usada: {GB_RAM_uso} GB | RAM Livre: {GB_RAM_livre} GB | Rede Recebida: {GB_rede_recebidos} GB | Rede Enviada: {GB_rede_enviados} GB")

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

        # Verifica se chegou a 10 capturas seguidas acima do limite e abre chamado
        if contador_cpu >= 10:
            abrir_chamado_jira("CPU", "Percentual de CPU", Porcentagem_CPU, servidor_id, data_hora)
            contador_cpu = 0

        if contador_mem >= 10:
            abrir_chamado_jira("Memória", "Percentual de Memória", Porcentagem_RAM_uso, servidor_id, data_hora)
            contador_mem = 0

        if contador_rede_enviados >= 10:
            abrir_chamado_jira("Rede Enviada", "GB Enviados", GB_rede_enviados, servidor_id, data_hora)
            contador_rede_enviados = 0

        if contador_rede_recebidos >= 10:
            abrir_chamado_jira("Rede Recebida", "GB Recebidos", GB_rede_recebidos, servidor_id, data_hora)
            contador_rede_recebidos = 0

        # Aguardar 1 segundo antes de coletar novamente
        time.sleep(1)

# Função para monitorar múltiplos servidores usando threads
def monitorar_multiple_servers(servidores):
    threads = []
    for servidor_id in servidores:
        thread = threading.Thread(target=monitorar_e_enviar_dados, args=(servidor_id,))
        threads.append(thread)
        thread.start()

    # Esperar todas as threads terminarem
    for thread in threads:
        thread.join()

# Lista de servidores para monitorar
servidores = [1, 2, 3]  # IDs dos servidores que você quer monitorar

# Iniciar o monitoramento
monitorar_multiple_servers(servidores)
