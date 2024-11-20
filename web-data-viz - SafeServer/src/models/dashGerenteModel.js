// const { obterCargos } = require("../controllers/dashboardController");
var database = require("../database/config")

function obterDados(idEmpresa) {
    var instrucaoSql = `
            select dia, mes, ano, alertas, componente, regiao from obterDadosAlerta where fkEmpresa = ${idEmpresa} ORDER BY ano, mes, dia;
    `;
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

module.exports = {
    obterDados
};