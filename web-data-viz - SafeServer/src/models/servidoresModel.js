var database = require("../database/config")

function buscarServidor(idEmpresa){
    var instrucaoSql = `SELECT * from servidor WHERE fkEmpresa = ${idEmpresa};`

    console.log("Executando instução SQL: " + instrucaoSql)
    return database.executar(instrucaoSql);
}


module.exports = {
    buscarServidor
};