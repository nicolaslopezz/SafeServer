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

# Função para monitorar e enviar dados para o banco de dados
def monitorar_e_enviar_dados(servidor_id):
    meusql = mysql.connector.connect(**db_config)
    meucursor = meusql.cursor()

    print(f"Conexão com o banco de dados bem-sucedida para o servidor {servidor_id}.")

    while True:
        memoria = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        disco = psutil.disk_usage('/')

        servidor_id = '(ALTERAR PARA QUAL O ID DO SERVIDOR DA SUA MAQUINA(1 OU 2)'

        total_memoriagb = round(memoria.total / (1024 ** 3), 1)
        used_memoriagb = round(memoria.used / (1024 ** 3), 1)
        total_discogb = round(disco.total / (1024 ** 3), 1)
        used_discogb = round(disco.used / (1024 ** 3), 1)
        livre_memoriagb = round(total_memoriagb - used_memoriagb, 1)
        livre_discogb = round(total_discogb - used_discogb, 1)

        query = '''
        INSERT INTO registro (percent_use_cpu, uso_ram_gb, livre_ram_gb, total_ram_gb, uso_disco_gb, livre_disco_gb, total_disco_gb, fkServidor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = (cpu, used_memoriagb, livre_memoriagb, total_memoriagb, used_discogb, livre_discogb, total_discogb, servidor_id)

        meucursor.execute(query, values)
        meusql.commit()

        # Impressão dos dados inseridos
        print(f"Dados inseridos: CPU: {cpu:.1f}%, RAM Usada: {used_memoriagb:.1f} GB, RAM Livre: {livre_memoriagb:.1f} GB, "
              f"Total RAM: {total_memoriagb:.1f} GB, Disco Usado: {used_discogb:.1f} GB, Disco Livre: {livre_discogb:.1f} GB, "
              f"Total Disco: {total_discogb:.1f} GB")

        time.sleep(2)

# Chamada da função para monitorar e enviar dados
monitorar_e_enviar_dados('MUDAR PARA O ID DO SERVIDOR DA SUA MAQUINA(1 OU 2)')

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
('m3', 1);  -- Corrigido a vírgula aqui

select * from registro;

select * from empresa;

select * from funcionario;

truncate registro;
'''
