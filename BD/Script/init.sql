DROP DATABASE IF EXISTS SafeServer;

-- CREATE USER 'SafeServerUser'@'localhost' IDENTIFIED BY 'safeserver123';
-- GRANT ALL PRIVILEGES ON SafeServer.* TO 'SafeServerUser'@'localhost';

create database SafeServer;
 
use SafeServer;

create table empresa(
idEmpresa int primary key auto_increment,
nomeFantasia varchar(60) not null,
razaoSocial varchar(200) not null,
CNPJ char(14) not null);

create table chaveAcesso (
idChave int primary key AUTO_INCREMENT,
chave varchar(20),
nivelPermissao int,
fkEmpresa int,
cargo varchar(45),
foreign key (fkEmpresa) references empresa(idEmpresa)
);

create table funcionario (
idFuncionario int primary key auto_increment,
nome varchar(200) not null,
email varchar(200) not null,
cpf char(11) not null,
senha varchar(45) not null,
fkEmpresa int, 
fkChave int, 
foreign key (fkChave) references chaveAcesso(idChave),
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

create table alerta (
idAlerta int primary key auto_increment,
componente varchar(45),
fkRegistro int,
nivelPrioridade int,
constraint fkRegistrosAlerta foreign key (fkRegistro) references registro (idRegistro)
);


INSERT INTO empresa (nomeFantasia, razaoSocial, CNPJ) VALUES
('INSTAGRAM', 'INSTAGRAM LTDA', '98765432000196');

-- Inserir dados na tabela chaveAcesso
INSERT INTO chaveAcesso (chave, nivelPermissao, fkEmpresa, cargo) VALUES
('abcd', 2, 1, 'Analista');

INSERT INTO servidor (identificacao, fkEmpresa) VALUES 
('reader', 1);
INSERT INTO servidor (identificacao, fkEmpresa) VALUES 
('writer', 1);


-- Inserir dados na tabela funcionario
INSERT INTO funcionario (nome, email, cpf, senha, fkEmpresa, fkChave) VALUES
('Marta', 'marta1@gmail.com', '12345678900', '123456', 1, 1),
('Marta', 'marta@gmail.com', '12345678901', '123456', 1, 1);

-- Inserir registros para o dia 25 de dezembro
INSERT INTO registro (dtHora, percent_use_cpu, percent_use_ram, uso_ram_gb, livre_ram_gb, recebido_rede, enviado_rede, fkServidor)
VALUES 
('2024-12-25 10:00:00', 92, 93, 32, 1, 700, 450, 1),  
('2024-12-25 18:00:00', 89, 91, 30, 2, 720, 400, 1),  
('2024-12-25 10:00:00', 91, 91, 31, 1, 680, 400, 2),  
('2024-12-25 18:00:00', 90, 93, 33, 1, 730, 440, 2),  

('2024-01-01 10:00:00', 88, 90, 28, 3, 500, 300, 1),  
('2024-01-01 18:00:00', 83, 85, 29, 2, 580, 350, 1),  
('2024-01-01 10:00:00', 84, 88, 28, 3, 480, 280, 2),  
('2024-01-01 18:00:00', 87, 89, 31, 1, 530, 340, 2),  

('2024-04-18 10:00:00', 75, 80, 27, 5, 560, 330, 1),  
('2024-04-18 18:00:00', 70, 74, 25, 5, 580, 320, 1),  
('2024-04-18 10:00:00', 73, 78, 26, 4, 580, 310, 2),  
('2024-04-18 18:00:00', 72, 77, 27, 4, 590, 350, 2),  

('2024-04-20 10:00:00', 68, 70, 25, 5, 490, 300, 1),  
('2024-04-20 18:00:00', 71, 72, 26, 4, 550, 340, 1),  
('2024-04-20 10:00:00', 69, 72, 26, 4, 510, 320, 2),  
('2024-04-20 18:00:00', 70, 73, 26, 4, 550, 350, 2),  

('2024-05-01 10:00:00', 76, 78, 28, 3, 600, 350, 1),  
('2024-05-01 18:00:00', 73, 75, 26, 4, 610, 360, 1),  
('2024-05-01 10:00:00', 74, 78, 27, 3, 620, 340, 2),  
('2024-05-01 18:00:00', 75, 77, 28, 2, 630, 330, 2);


-- select*from chaveAcesso;
-- SELECT DATE(dtHora) AS data, AVG(percent_use_cpu) AS mediaDeUsoCPU
-- FROM registro GROUP BY DATE(dtHora) ORDER BY mediaDeUsoCPU DESC;
    


CREATE VIEW obterFunc as (SELECT nome, email, cpf, cargo, chaveAcesso.fkEmpresa FROM funcionario JOIN chaveAcesso ON fkChave = idChave);

-- select * from registro;

-- select * from empresa;

select * from funcionario;

-- truncate regis