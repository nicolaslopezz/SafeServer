import psutil
import time

# Função para monitorar o componente e obter os dados
def monitorar_componente(componente, tipo_dado, num_dados=10):
    dados = []
    
    for i in range(num_dados):
        if componente == "cpu":
            dados.append(psutil.cpu_percent(interval=1))
        elif componente == "memoria":
            memoria = psutil.virtual_memory()
            if tipo_dado == "UD":
                dados.append(memoria.used / (1024 ** 3))  # Valor em GB
        elif componente == "disco":
            disco = psutil.disk_usage('/')
            if tipo_dado == "UD":
                dados.append(disco.used / (1024 ** 3))  # Valor em GB
        else:
            print("Componente inválido.")
            return None

    return dados

# Função para exibir o menu e capturar as escolhas do usuário
def exibir_menu():
    time.sleep(1)

    print("\nQual componente você deseja monitorar?")
    print("Opções: cpu, memoria, disco")
    componente = input("Componente escolhido: ").lower()

    if componente == "cpu":
        metrica = "%"
    elif componente in ["memoria", "disco"]:
        metrica = "GB"  # Usaremos GigaBytes como exemplo de métrica padrão
    else:
        print("Componente inválido.")
        return

    tipo_dado = "UD"  # Vamos usar o tipo de dado UD (uso direto)

    alerta = None
    if tipo_dado == "UD":
        print("\nDeseja configurar um alerta para o uso de CPU, memória ou disco? (s/n)")
        configurar_alerta = input().lower()
        if configurar_alerta == 's':
            if componente == "cpu":
                alerta = float(input(f"Digite o valor de alerta para uso de CPU ({metrica}): "))
            elif componente == "memoria":
                alerta = float(input(f"Digite o valor de alerta para uso de Memória ({metrica}): "))
            elif componente == "disco":
                alerta = float(input(f"Digite o valor de alerta para uso de Disco ({metrica}): "))

    while True:
        if componente in ["cpu", "memoria", "disco"]:
            if tipo_dado == "UD":
                valores = monitorar_componente(componente, tipo_dado, num_dados=10)
                for valor in valores:
                    if componente == "cpu":
                        if alerta is not None and valor > alerta:
                            print(f"CPU (%): {valor:.1f}% | ALERTA! Valor atual excede o limite configurado de {alerta}%.")
                        else:
                            print(f"CPU (%): {valor:.1f}%")
                    else:
                        if alerta is not None and valor > alerta:
                            print(f"{componente.capitalize()} (GB): {valor:.1f} GB | ALERTA! Valor atual excede o limite configurado de {alerta} GB.")
                        else:
                            print(f"{componente.capitalize()} (GB): {valor:.1f} GB")

        print("\nDeseja continuar? (Digite s para continuar ou n para sair)")
        continuar = input().lower()
        if continuar != 's':
            break

# Chama a função para exibir o menu
exibir_menu()
