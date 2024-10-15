DROP DATABASE IF EXISTS SafeServer;

-- CREATE USER 'SafeServerUser'@'localhost' IDENTIFIED BY 'safeserver123';
-- GRANT ALL PRIVILEGES ON SafeServer.* TO 'SafeServerUser'@'localhost';

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
cpf char(11) not null,
senha varchar(45) not null,
cargo varchar(45),
fkEmpresa int, 
constraint fkFuncionarioEmpresa foreign key (fkEmpresa) references empresa (idEmpresa));

create table servidor (
idServidor int primary key auto_increment,
identificacao varchar(45) not null,
fkEmpresa int,
constraint fkEmpresaServidores foreign key (fkEmpresa) references empresa (idEmpresa));

create table registro (
idRegistro int primary key auto_increment,
dtHora datetime default current_timestamp,
percent_use_cpu float, 
percent_use_ram float, 
uso_ram_gb float,
livre_ram_gb float,
recebido_rede float,
enviado_rede float,
fkServidor int,
constraint fkServidorRegistros foreign key (fkServidor) references servidor (idServidor));

insert into empresa values 
(default, "Instagram", "Instagram Meta Platforms INC Facebook Serviços Online do Brasil LTDA", "12345678912345","ABCD1234");
insert into servidor(identificacao, fkEmpresa) values
('m1', 1),
('m2', 1);

-- select * from registro;

select * from empresa;

select * from funcionario;

-- truncate regis