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

// Coloque os mesmos parâmetros aqui. Vá para a var instrucaoSql

module.exports = {
    obterCargos
};