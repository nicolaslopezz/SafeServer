DROP DATABASE IF EXISTS SafeServer;

create database SafeServer;

use SafeServer;

create table empresa(
idEmpresa int primary key auto_increment,
nomeFantasia varchar(60) not null,
razaoSocial varchar(60) not null,
CNPJ char(14) not null,
chaveAcesso int);

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

create table servidores (
idServidor int primary key auto_increment,
identificacao varchar(45) not null,
fkEmpresa int,
constraint fkEmpresaServidores foreign key (fkEmpresa) references empresa (idEmpresa));

create table registros (
idRegistros int primary key auto_increment,
dataHora datetime default current_timestamp,
percent_cpu float, 
temp_cpu float,
uso_ram float,
livre_ram float,
total_ram float,
uso_disco float,
livre_disco float,
total_disco float,
fkServidor int,
constraint fkServidorRegistros foreign key (fkServidor) references servidores (idServidor));





	







