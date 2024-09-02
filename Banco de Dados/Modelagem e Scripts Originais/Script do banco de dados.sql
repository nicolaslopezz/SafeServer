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
uso_ram_gb Bigint,
livre_ram_gb bigint,
total_ram_gb bigint,
uso_disco_gb bigint,
livre_disco_gb bigint,
total_disco_gb bigint,
toltal_nucleos_cpu int,
fkServidor int,
constraint fkServidorRegistros foreign key (fkServidor) references servidor (idServidor));


insert into empresa values 
(default, "Instagram", "Instagram Meta Platforms INC Facebook Serviços Online do Brasil LTDA", "12345678912345","ABCD1234");

select * from registro;

select * from empresa;

select * from funcionario;



truncate registros;
