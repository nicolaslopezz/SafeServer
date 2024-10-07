import psutil
import time
import mysql.connector

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'batatas123',
    'database': 'SafeServer'
}
servidor_id = 1

# Estabelecendo conexão ao BD
mydb = mysql.connector.connect(**db_config)
cursor = mydb.cursor()

# Verificando se o servidor está cadastrado
sql = "SELECT idServidor FROM Servidor WHERE idServidor = %s;"
cursor.execute(sql, (servidor_id,))
resultado = cursor.fetchall()

if len(resultado) < 1:
    print("Seu servidor não está cadastrado no sistema.")
else:
    print("Servidor encontrado. Começando a monitorar...")

    # Definindo o intervalo e limite
    tempo = int(input("Escolha o intervalo de capturas (segundos): "))
    limite = int(input("Escolha o número de vezes que o sistema deve capturar: "))

    # Opções de monitoramento
    print("\nEscolha quais dados deseja monitorar:")
    print("1 - Uso da CPU")
    print("2 - Uso de RAM")
    print("3 - Memória RAM Livre")
    print("4 - Porcentagem RAM")
    print("5 - Rede Recebidos")
    print("6 - Rede Enviados")
    
    opcoes_selecionadas = input("Digite os números separados por vírgula (ex: 1,2): ").split(',')

    while limite > 0:
        # Coletando dados
        uso_cpu = round(psutil.cpu_percent(), 2)
        uso_ram = round(psutil.virtual_memory().used / (1024 ** 3), 2)
        ram_livre = round(psutil.virtual_memory().free / (1024 ** 3), 2)
        porcentagem_ram = round(psutil.virtual_memory().percent, 2)
        rede_recebidos = round(psutil.net_io_counters().bytes_recv / (1024 ** 3), 2)
        rede_enviados = round(psutil.net_io_counters().bytes_sent / (1024 ** 3), 2)

        # Exibindo dados selecionados
        for opcao in opcoes_selecionadas:
            if opcao == '1':
                print(f"Uso da CPU: {uso_cpu:.2f}%")
            elif opcao == '2':
                print(f"Uso de RAM: {uso_ram:.2f} GB")
            elif opcao == '3':
                print(f"Memória RAM Livre: {ram_livre:.2f} GB")
            elif opcao == '4':
                print(f"Porcentagem de RAM: {porcentagem_ram:.2f}%")
            elif opcao == '5':
                print(f"Rede Recebidos: {rede_recebidos:.2f} GB")
            elif opcao == '6':
                print(f"Rede Enviados: {rede_enviados:.2f} GB")

        # Inserindo dados no banco de dados
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
        values = (uso_cpu, porcentagem_ram, uso_ram, ram_livre, rede_recebidos, rede_enviados, servidor_id)
        cursor.execute(query, values)
        mydb.commit()

        limite -= 1  # Reduzindo o limite
        time.sleep(tempo)  # Esperando pelo intervalo definido

    print("Monitoramento finalizado.")

# Fechando a conexão com o banco de dados
cursor.close()
mydb.close()
