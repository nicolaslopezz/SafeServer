// const { obterCargos } = require("../controllers/dashboardController");
var database = require("../database/config")

function obterDados(idEmpresa) {
    var instrucaoSql = `
            select alertas, ano, mes, dia, componente, fkServidor from obterDadosAlerta where fkEmpresa = ${idEmpresa};
    `;
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

module.exports = {
    obterDados
};