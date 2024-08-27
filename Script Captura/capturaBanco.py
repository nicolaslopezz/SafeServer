import psutil
import time
import mysql.connector

# Criação da conexão com o banco de dados
meusql = mysql.connector.connect(
    host='localhost',
    user='root',
    password='e21s20@1',
    database='SafeServer'
)

meucursor = meusql.cursor()

while True:
    memoria = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=1)
    nucleosCPU = psutil(logical=False)
    disco = psutil.disk_usage('/')

    # Cálculo das variáveis com formatação para uma casa decimal
    total_memoriagb = round(memoria.total / (1024 ** 3), 1)
    used_memoriagb = round(memoria.used / (1024 ** 3), 1)
    total_discogb = round(disco.total / (1024 ** 3), 1)
    used_discogb = round(disco.used / (1024 ** 3), 1)
    livre_memoriagb = round(total_memoriagb - used_memoriagb, 1)
    livre_discogb = round(total_discogb - used_discogb, 1)

    # Consulta SQL para inserir os dados no banco de dados
    query = '''
    INSERT INTO registros (percent_use_cpu, uso_ram_gb, livre_ram_gb, total_ram_gb, uso_disco_gb, livre_disco_gb, total_disco_gb, toltal_nucleos_cpu)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    
    values = (cpu, used_memoriagb, livre_memoriagb, total_memoriagb, used_discogb, livre_discogb, total_discogb, nucleosCPU)

    meucursor.execute(query, values)
    meusql.commit()
    
    # Impressão dos resultados formatados
    print('Percentual de uso da CPU =', cpu, '%')
    print('Memoria em uso = {:.1f}'.format(used_memoriagb), 'GB')
    print('Memoria livre = {:.1f}'.format(livre_memoriagb), 'GB')
    print('Total memoria = {:.1f}'.format(total_memoriagb), 'GB') 
    print('Disco em uso = {:.1f}'.format(used_discogb), 'GB')
    print('Disco livre = {:.1f}'.format(livre_discogb), 'GB')
    print('Total Disco = {:.1f}'.format(total_discogb), 'GB')
    print('=' * 55)
    time.sleep(2)
