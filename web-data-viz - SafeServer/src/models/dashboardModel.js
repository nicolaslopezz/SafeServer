// const { obterCargos } = require("../controllers/dashboardController");
var database = require("../database/config")

function obterCargos(idEmpresa) {
    var instrucaoSql = `
        SELECT cargo, nivelPermissao, chave FROM chaveAcesso 
            WHERE fkEmpresa = '${idEmpresa}';
    `;
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function obterFunc(idEmpresa) {
    var instrucaoSql = `
        SELECT nome, email, cpf, cargo FROM obterFunc WHERE fkEmpresa = ${idEmpresa};
    `;
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function cadastrarCargo(cargo, nivelPermissao, idEmpresa) {
    let codigo = gerarCodigo();
    var instrucaoSql = `
        INSERT INTO chaveAcesso(chave, nivelPermissao, fkEmpresa, cargo) VALUES 
            ("${codigo}", "${nivelPermissao}", "${idEmpresa}", "${cargo}");
    `;
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function registrar_servidor(nome, regiao) {
    var fkEmpresa = sessionStorage.getItem("ID_EMPRESA")
    var instrucaoSql = `
        INSERT INTO servidor(nome, regiao, fkEmpresa) VALUES 
            ("${nome}", "${regiao}", "${fkEmpresa}");
    `;
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function gerarCodigo() {
    return Math.random().toString(36).substr(-8).toUpperCase()
}

// Coloque os mesmos parâmetros aqui. Vá para a var instrucaoSql

module.exports = {
    obterCargos,
    obterFunc,
    cadastrarCargo,
    registrar_servidor
};