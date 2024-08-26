import psutil
import mysql.connector
import time

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="??", ## Senha do seu banco 
    database="registros"
)

mycursor = mydb.cursor()

while True:
    cpuPercentual = psutil.cpu_percent(interval=3)
    quantidadeCPU = psutil.cpu_count()
    nucleosCPU = psutil(logical=False)
    contextoCPU = psutil.cpu_times()
    
    usoMemoria = psutil.virtual_memory().used
    memoriaLivre = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    totalMemoria = psutil.virtual_memory().free
    
    discoLivre = psutil.disk_usage('/').free
    usoDisco = psutil.disk_usage('/').used
    tamanhoDisco = psutil.disk_usage('/').total

    print(cpuPercentual)
    
    sql = "INSERT INTO cpu_UsageData (comp_id, cpu_usage_percent) VALUES (%s, %s)"
    val = (1, cpuPercentual)

    sql2 = "INSERT INTO mem_usage_info (comp_id, used_mem, freeMemory) VALUES (%s, %s, %s)"  
    val2 = (1,usoMemoria,memoriaLivre)

    sql3 = "INSERT INTO diskUsage (comp_id, free_disk) values (%s, %s)"
    val3 = (1, usoDisco)





    

    mycursor.execute(sql, val)
    mycursor.execute(sql2, val2)
    mycursor.execute(sql3, val3)

    mydb.commit()

    print(cpuPercentual,"%")