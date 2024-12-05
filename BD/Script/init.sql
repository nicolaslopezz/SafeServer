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
regiao varchar(45),
fkEmpresa int,
constraint fkEmpresaServidores foreign key (fkEmpresa) references empresa (idEmpresa));

create table registro (
idRegistro int primary key auto_increment,
dtHora datetime default current_timestamp,
percent_use_cpu float, 
percent_use_ram float, 
recebido_rede float,
enviado_rede float,
fkServidor int,
constraint fkServidorRegistros foreign key (fkServidor) references servidor (idServidor));

CREATE TABLE estatisticas_horarias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fkServidor INT NOT NULL,
    componente ENUM('cpu', 'ram') NOT NULL,
    timestamp DATETIME NOT NULL,
    desvio_padrao DECIMAL(4, 2) NOT NULL,
    horaCalculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    oscilacao FLOAT,
    FOREIGN KEY (fkServidor) REFERENCES servidor(idServidor) 
);


select * from registro;


create table alerta (
idAlerta int primary key auto_increment,
componente varchar(45),
fkRegistro int,
constraint fkRegistrosAlerta foreign key (fkRegistro) references registro (idRegistro)
);


INSERT INTO empresa (nomeFantasia, razaoSocial, CNPJ) VALUES
('INSTAGRAM', 'INSTAGRAM LTDA', '98765432000196');

INSERT INTO chaveAcesso (chave, nivelPermissao, fkEmpresa, cargo) VALUES
('abcd', 2, 1, 'Gerente');

INSERT INTO servidor (identificacao, fkEmpresa, regiao) VALUES 
('reader', 1, 'US-EAST-1'),
('writer', 1, 'US-EAST-1');

INSERT INTO funcionario (nome, email, cpf, senha, fkEmpresa, fkChave) VALUES
('Marta', 'marta1@gmail.com', '12345678900', '123456', 1, 1),
('Roberto', 'roberto@gmail.com', '12345678901', '123456', 1, 1);


INSERT INTO registro (dtHora, percent_use_cpu, percent_use_ram, recebido_rede, enviado_rede, fkServidor)
VALUES  
('2024-12-25 10:00:00', 93, 95, 240, 250, 1),  
('2024-12-25 18:00:00', 89, 90, 220, 230, 1),  
('2024-12-25 10:00:00', 97, 91, 260, 240, 2),  
('2024-12-25 18:00:00', 95, 93, 210, 220, 2),  

('2024-01-01 10:00:00', 88, 90, 200, 250, 1),  
('2024-01-01 18:00:00', 83, 85, 230, 210, 1),  
('2024-01-01 10:00:00', 84, 88, 240, 200, 2),  
('2024-01-01 18:00:00', 87, 89, 220, 260, 2),  

('2024-03-29 10:00:00', 97, 80, 210, 240, 1),  
('2024-03-29 18:00:00', 80, 74, 200, 250, 1),  
('2024-03-29 10:00:00', 98, 78, 230, 260, 2),  
('2024-03-29 18:00:00', 78, 77, 240, 220, 2),  

('2024-03-31 10:00:00', 88, 70, 220, 200, 1),  
('2024-03-31 18:00:00', 90, 72, 250, 230, 1),  
('2024-03-31 10:00:00', 93, 72, 240, 210, 2),  
('2024-03-31 18:00:00', 75, 73, 260, 240, 2),  

('2024-05-01 10:00:00', 76, 78, 200, 230, 1),  
('2024-05-01 18:00:00', 79, 75, 240, 220, 1),  
('2024-05-01 10:00:00', 79, 72, 230, 210, 2),  
('2024-05-01 18:00:00', 98, 77, 260, 200, 2),
('2024-12-03 10:00:00', 45, 30, 98, 85, 2),
('2024-12-03 10:00:00', 50, 45, 100, 100, 2);

INSERT INTO alerta (componente, fkRegistro) 
VALUES  
-- Alertas para CPU > 75
('cpu', 1),
('cpu', 2),
('cpu', 3),
('cpu', 4),
('cpu', 5),
('cpu', 9),
('cpu', 13),
('cpu', 14),
('cpu', 15),
('cpu', 16),
('cpu', 17),
('cpu', 20),

-- Alertas para RAM > 85
('ram', 1),
('ram', 2),
('ram', 3),
('ram', 4),
('ram', 5),
('ram', 7),
('ram', 8),

-- Alertas para rede_recebida > 200 GB
('rede_recebida', 1),
('rede_recebida', 2),
('rede_recebida', 3),
('rede_recebida', 4),
('rede_recebida', 6),
('rede_recebida', 7),
('rede_recebida', 8),
('rede_recebida', 9),
('rede_recebida', 11),
('rede_recebida', 13),
('rede_recebida', 15),
('rede_recebida', 16),
('rede_recebida', 17),

-- Alertas para rede_enviada > 200 GB
('rede_enviada', 1),
('rede_enviada', 2),
('rede_enviada', 3),
('rede_enviada', 4),
('rede_enviada', 5),
('rede_enviada', 7),
('rede_enviada', 8),
('rede_enviada', 9),
('rede_enviada', 10),
('rede_enviada', 11),
('rede_enviada', 13),
('rede_enviada', 15),
('rede_enviada', 16),
('rede_enviada', 17),
('rede_enviada', 16);

-- select*from chaveAcesso;
-- SELECT DATE(dtHora) AS data, AVG(percent_use_cpu) AS mediaDeUsoCPU
-- FROM registro GROUP BY DATE(dtHora) ORDER BY mediaDeUsoCPU DESC;
    


CREATE VIEW obterFunc as (SELECT nome, email, cpf, cargo, chaveAcesso.fkEmpresa FROM funcionario JOIN chaveAcesso ON fkChave = idChave);

-- select * from registro;

-- select * from empresa;

select * from funcionario;

-- truncate regis
select * from registro;
  
            
CREATE VIEW obterDadosAlerta AS (SELECT count(idAlerta) as alertas, componente, year(dtHora) as ano, month(dtHora) as mes, day(dtHora) as dia, fkEmpresa, regiao
	FROM alerta
    JOIN registro ON idRegistro = fkRegistro
    JOIN servidor ON fkServidor = idServidor
    GROUP BY componente, dia, mes, ano, fkEmpresa, regiao
    ORDER BY regiao, ano, mes, dia);	