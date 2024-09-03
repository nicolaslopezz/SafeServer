import psutil
import time
import threading

# Função para exibir o menu e capturar a escolha do usuário
def exibir_menu():
    
    time.sleep(1.5)

    print("\nEscolha a máquina que você quer monitorar:")
    print("Opções: m1 ou m2")
    maquina = input("Máquina escolhida: ").lower()

    print("\nQual componente você deseja monitorar?")
    print("Opções: cpu, memoria, disco")
    componente = input("Componente escolhido: ").lower()

    if componente == "cpu":
        print("\nEscolha a métrica para CPU:")
        print("A) Porcentagem (Digite: %)")
    elif componente in ["memoria", "disco"]:
        print(f"\nEscolha a métrica para {componente.capitalize()}:")
        print("A) Bytes (Digite: B)")
        print("B) MegaBytes (Digite: MB)")
        print("C) GigaBytes (Digite: GB)")
    else:
        print("Componente inválido.")
        return

    metrica = input("Métrica escolhida: ").upper()

    print("\nEscolha o tipo de dado:")
    print("Opções: Dado Normal (Digite DN), Média da máquina escolhida (Digite MM), Média de todas as máquinas (Digite MT)")
    tipo_dado = input("Tipo de dado escolhido: ").upper()

    servidor_id = None
    if maquina in ["m1", "m2"]:
        servidor_id = 1 if maquina == "m1" else 2
    else:
        print("Máquina inválida.")
        return

    print("\nInforme o intervalo de monitoramento em segundos:")
    intervalo = float(input("Intervalo: "))

    print("\nDeseja configurar um alerta para o uso de CPU, memória ou disco? (s/n)")
    configurar_alerta = input().lower()

    alerta_cpu = None
    alerta_memoria = None
    alerta_disco = None

    if configurar_alerta == 's':
        if componente == "cpu":
            alerta_cpu = float(input(f"Digite o valor de alerta para uso de CPU (%): "))
        elif componente == "memoria":
            alerta_memoria = float(input(f"Digite o valor de alerta para uso de Memória ({metrica}): "))
        elif componente == "disco":
            alerta_disco = float(input(f"Digite o valor de alerta para uso de Disco ({metrica}): "))
        else:
            print("Componente para alerta inválido.")
            return

    def monitorar():
        while True:
            valor = monitorar_componente(componente, metrica, tipo_dado, servidor_id)

            if valor is not None:
                if componente == "cpu":
                    if tipo_dado in ["DN", "MM", "MT"]:
                        if alerta_cpu is not None and valor > alerta_cpu:
                            print(f"CPU (%): {valor:.1f}% | ALERTA! Valor atual excede o limite configurado de {alerta_cpu}%.")
                        else:
                            print(f"CPU (%): {valor:.1f}%")
                elif componente == "memoria":
                    if tipo_dado in ["DN", "MM", "MT"]:
                        valor_em_gb = valor if metrica == "GB" else valor / 1024 if metrica == "MB" else valor / (1024 ** 3)
                        if alerta_memoria is not None and valor > alerta_memoria:
                            print(f"Memória ({metrica}): {valor:.1f} {metrica} | ALERTA! Valor atual excede o limite configurado de {alerta_memoria} {metrica}.")
                        else:
                            print(f"Memória ({metrica}): {valor:.1f} {metrica}")
                elif componente == "disco":
                    if tipo_dado in ["DN", "MM", "MT"]:
                        valor_em_gb = valor if metrica == "GB" else valor / 1024 if metrica == "MB" else valor / (1024 ** 3)
                        if alerta_disco is not None and valor > alerta_disco:
                            print(f"Disco ({metrica}): {valor:.1f} {metrica} | ALERTA! Valor atual excede o limite configurado de {alerta_disco} {metrica}.")
                        else:
                            print(f"Disco ({metrica}): {valor:.1f} {metrica}")

            time.sleep(intervalo)

    monitor_thread = threading.Thread(target=monitorar)
    monitor_thread.daemon = True
    monitor_thread.start()

    while True:
        parar = input("\nSe deseja parar de monitorar, digite (n):\n").lower()
        if parar == 'n':
            print("\nEncerrando monitoramento...")
            break

# Função para calcular a média do componente escolhido pelo usuário
def calcular_media_componente(componente, metrica, tipo_dado, servidor_id=None):
    # Código de cálculo de média removido
    return None

# Função para monitorar o componente escolhido pelo usuário
def monitorar_componente(componente, metrica, tipo_dado, servidor_id=None):
    valor = None

    if tipo_dado == "DN":
        if componente == "cpu":
            valor = psutil.cpu_percent(interval=1)
        elif componente == 'memoria':
            memoria = psutil.virtual_memory()
            if metrica == 'MB':
                valor = round(memoria.used / 1024 ** 2)
            elif metrica == 'GB':
                valor = round(memoria.used / (1024 ** 3), 1)
            elif metrica == 'B':
                valor = memoria.used
        elif componente == 'disco':
            disco = psutil.disk_usage('/')
            if metrica == 'MB':
                valor = round(disco.used / 1024 ** 2)
            elif metrica == 'GB':
                valor = round(disco.used / (1024 ** 3), 1)
            elif metrica == 'B':
                valor = disco.used

    elif tipo_dado in ["MM", "MT"]:
        valor = calcular_media_componente(componente, metrica, tipo_dado, servidor_id)

    return valor

# Chamaa a função para exibir o menu
exibir_menu()
