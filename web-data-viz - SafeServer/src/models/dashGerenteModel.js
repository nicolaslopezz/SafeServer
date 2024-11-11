// const { obterCargos } = require("../controllers/dashboardController");
var database = require("../database/config")

function obterDados(idEmpresa) {
    var instrucaoSql = `
        SELECT count(idAlerta) as alertas, componente, DATE(dtHora) as dia, fkServidor, fkEmpresa
	FROM alerta 
    JOIN registro ON idRegistro = fkRegistro 
    JOIN servidor ON fkServidor = idServidor
    WHERE DATE(dtHora) between '2024-11-01' and '2024-11-20' AND fkEmpresa = '${idEmpresa}'
	GROUP BY DATE(dtHora), 
    componente, 
    fkServidor
    ORDER BY DATE(dtHora);
    `;
    // var instrucaoSql = `
    //     select alertas, dia, fkServidor from obterDadosAlerta where fkEmpresa = ${idEmpresa};
    // `
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

module.exports = {
    obterDados
};