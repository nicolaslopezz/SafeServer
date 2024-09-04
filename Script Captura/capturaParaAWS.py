import psutil
import time
import mysql.connector

# Configurações do banco de dados
db_config = {
    'host': '10.18.33.38',
    'user': 'root',
    'password': 'Afro@0703',
    'database': 'SafeServer'
}

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        print("Tentando conectar ao banco de dados...")
        conexao = mysql.connector.connect(**db_config)
        print("Conexão com o banco de dados bem-sucedida.")
        return conexao
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Função para monitorar o componente e obter os dados
def monitorar_componente(componente, metrica, tipo_dado, servidor_id):
    conexao = conectar_banco()
    if conexao is None:
        print("Não foi possível conectar ao banco de dados.")
        return None
    
    try:
        cursor = conexao.cursor()

        # Mapeamento do componente para o nome da coluna
        if componente == "cpu":
            coluna = "percent_use_cpu"
        elif componente == "memoria":
            coluna = "uso_ram_gb"
        elif componente == "disco":
            coluna = "uso_disco_gb"
        else:
            print("Componente inválido.")
            return None
        
        if tipo_dado == "UD":  # Último dado
            query = f"SELECT {coluna} FROM registro WHERE fkServidor = %s ORDER BY dataHora DESC LIMIT 1"
            cursor.execute(query, (servidor_id,))
        elif tipo_dado == "MM":  # Média da máquina escolhida
            query = f"SELECT AVG({coluna}) FROM registro WHERE fkServidor = %s"
            cursor.execute(query, (servidor_id,))
        elif tipo_dado == "MT":  # Média de todas as máquinas
            query = f"SELECT AVG({coluna}) FROM registro"
            cursor.execute(query)
        
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    
    finally:
        cursor.close()
        conexao.close()

# Função para exibir o menu e capturar as escolhas do usuário
def exibir_menu():
    time.sleep(1)

    print("\nEscolha a máquina que você quer monitorar:")
    print("Opções: m1 ou m2")
    maquina = input("Máquina escolhida: ").lower()

    if maquina == "m1":
        servidor_id = 1
    elif maquina == "m2":
        servidor_id = 2
    else:
        print("Máquina inválida.")
        return

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
        valor = monitorar_componente(componente, metrica, tipo_dado, servidor_id)

        if valor is not None:
            if componente == "cpu":
                if alerta is not None and valor > alerta:
                    print(f"CPU (%): {valor:.1f}% | ALERTA! Valor atual excede o limite configurado de {alerta}%.")
                else:
                    print(f"CPU (%): {valor:.1f}%")
            elif componente == "memoria" or componente == "disco":
                valor_em_gb = valor if metrica == "GB" else valor / 1024 if metrica == "MB" else valor / (1024 ** 3)
                if alerta is not None and valor > alerta:
                    print(f"{componente.capitalize()} ({metrica}): {valor_em_gb:.1f} {metrica} | ALERTA! Valor atual excede o limite configurado de {alerta} {metrica}.")
                else:
                    print(f"{componente.capitalize()} ({metrica}): {valor_em_gb:.1f} {metrica}")
        else:
            print(f"Nenhum dado encontrado para o componente {componente} na máquina {servidor_id}.")

        print("\nDeseja continuar? (Digite s para continuar ou n para sair)")
        continuar = input().lower()
        if continuar != 's':
            break

# Chama a função para exibir o menu
exibir_menu()


# SCRIPT DO BANCO

'''
DROP DATABASE IF EXISTS SafeServer;

create database SafeServer;

use SafeServer;

create table empresa(
idEmpresa int primary key auto_increment,
nomeFantasia varchar(60) not null,
razaoSocial varchar(200) not null,
CNPJ char(14) not null,
chaveAcesso varchar(50));

create table funcionario (
idFuncionario int primary key auto_increment,
nome varchar(200) not null,
email varchar(200) not null,
telefone int not null,
senha varchar(45) not null,
fkEmpresa int, 
fkGerente int,
constraint fkGerenteFuncionario foreign key (fkGerente) references funcionario (idFuncionario),
constraint fkFuncionarioEmpresa foreign key (fkEmpresa) references empresa (idEmpresa));

create table servidor (
idServidor int primary key auto_increment,
identificacao varchar(45) not null,
fkEmpresa int,
constraint fkEmpresaServidores foreign key (fkEmpresa) references empresa (idEmpresa));

create table registro (
idRegistro int primary key auto_increment,
dataHora datetime default current_timestamp,
percent_use_cpu float, 
uso_ram_gb float,
livre_ram_gb float,
total_ram_gb float,
uso_disco_gb float,
livre_disco_gb float,
total_disco_gb float,
toltal_nucleos_cpu int,
fkServidor int,
constraint fkServidorRegistros foreign key (fkServidor) references servidor (idServidor));


insert into empresa values 
(default, "Instagram", "Instagram Meta Platforms INC Facebook Serviços Online do Brasil LTDA", "12345678912345","ABCD1234");

insert into servidor(identificacao, fkEmpresa) values
('m1', 1),
('m2', 1),
('m3, 1);

select * from registro;

select * from empresa;

select * from funcionario;

truncate registro;
'''

