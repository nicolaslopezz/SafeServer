import psutil
import time

# Função para monitorar o componente e obter os dados
def monitorar_componente(componente, tipo_dado):
   
    if componente == "cpu":
        return psutil.cpu_percent(interval=1)
    elif componente == "memoria":
        memoria = psutil.virtual_memory()
        if tipo_dado == "UD":  
            return memoria.used / (1024 ** 3)  
        elif tipo_dado in ["MM", "MT"]:  
            return memoria.total / (1024 ** 3), memoria.used / (1024 ** 3) 
    elif componente == "disco":
        disco = psutil.disk_usage('/')
        if tipo_dado == "UD": 
            return disco.used / (1024 ** 3)  
        elif tipo_dado in ["MM", "MT"]:  
            return disco.total / (1024 ** 3), disco.used / (1024 ** 3) 
    else:
        print("Componente inválido.")
        return None

# Função para exibir o menu e capturar as escolhas do usuário
def exibir_menu():
    time.sleep(1)

    print("\nQual componente você deseja monitorar?")
    print("Opções: cpu, memoria, disco")
    componente = input("Componente escolhido: ").lower()

    if componente == "cpu":
        print("\nEscolha a métrica para CPU:")
        print("A) Porcentagem (Digite: %)")
        metrica = "%"
    elif componente in ["memoria", "disco"]:
        print(f"\nEscolha a métrica para {componente.capitalize()}:")
        print("A) Bytes (Digite: B)")
        print("B) MegaBytes (Digite: MB)")
        print("C) GigaBytes (Digite: GB)")
        metrica = input("Métrica escolhida: ").upper()
    else:
        print("Componente inválido.")
        return

    print("\nEscolha o tipo de dado:")
    print("Opções: Último Dado (Digite UD), Média da máquina escolhida (Digite MM), Média de todas as máquinas (Digite MT)")
    tipo_dado = input("Tipo de dado escolhido: ").upper()

    alerta = None
    if tipo_dado == "UD":
        print("\nDeseja configurar um alerta para o uso de CPU, memória ou disco? (s/n)")
        configurar_alerta = input().lower()
        if configurar_alerta == 's':
            if componente == "cpu":
                alerta = float(input(f"Digite o valor de alerta para uso de CPU (%): "))
            elif componente == "memoria":
                alerta = float(input(f"Digite o valor de alerta para uso de Memória ({metrica}): "))
            elif componente == "disco":
                alerta = float(input(f"Digite o valor de alerta para uso de Disco ({metrica}): "))

    while True:
        if componente in ["cpu", "memoria", "disco"]:
            if tipo_dado == "UD":
                if componente == "cpu":
                    valor = monitorar_componente(componente, tipo_dado)
                    if alerta is not None and valor > alerta:
                        print(f"CPU (%): {valor:.1f}% | ALERTA! Valor atual excede o limite configurado de {alerta}%.")
                    else:
                        print(f"CPU (%): {valor:.1f}%")
                else:
                    valor = monitorar_componente(componente, tipo_dado)
                    if alerta is not None and valor > alerta:
                        print(f"{componente.capitalize()} (GB): {valor:.1f} GB | ALERTA! Valor atual excede o limite configurado de {alerta} GB.")
                    else:
                        print(f"{componente.capitalize()} (GB): {valor:.1f} GB")
            else:
                print("A lógica para calcular a média ainda não foi implementada.")
        else:
            print(f"Nenhum dado encontrado para o componente {componente}.")

        print("\nDeseja continuar? (Digite s para continuar ou n para sair)")
        continuar = input().lower()
        if continuar != 's':
            break

# Chama a função para exibir o menu
exibir_menu()
