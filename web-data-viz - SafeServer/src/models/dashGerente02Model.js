var database = require("../database/config")

async function getServidores() {
  var instrucaoSql = 'SELECT idServidor, identificacao FROM servidor';
  console.log("Executando a instrução SQL: \n" + instrucaoSql);
  var [rows] = await database.executar(instrucaoSql);
  return rows;
}

async function getDesvioPadraoCPU(servidorId) {
  var instrucaoSql = `
    SELECT STDDEV(percent_use_cpu) AS desvio_padrao_cpu
    FROM registro
    WHERE fkServidor = ${servidorId} AND dtHora >= NOW() - INTERVAL 1 HOUR;
  `;
  console.log("Executando a instrução SQL: \n" + instrucaoSql);
  var [rows] = await database.executar(instrucaoSql, [servidorId]);
  return rows[0]?.desvio_padrao_cpu;
}

async function getDesvioPadraoRAM(servidorId) {
  var instrucaoSql = `
    SELECT STDDEV(percent_use_ram) AS desvio_padrao_ram
    FROM registro
    WHERE fkServidor = ${servidorId} AND dtHora >= NOW() - INTERVAL 1 HOUR;
  `;
  console.log("Executando a instrução SQL: \n" + instrucaoSql);
  var [rows] = await database.executar(instrucaoSql, [servidorId]);
  return rows[0]?.desvio_padrao_ram;
}

async function guardarResultado(servidorId, componente, desvioPadrao) {
  var instrucaoSql = `
    INSERT INTO estatisticas_horarias (fkServidor, componente, timestamp, desvio_padrao)
    VALUES (${servidorId}, ${componente}, NOW(), ${desvioPadrao});
  `;
  console.log("Executando a instrução SQL: \n" + instrucaoSql);
  await database.executar(instrucaoSql, [servidorId, componente, desvioPadrao]);
}

async function datasDisponiveis(serverId) {
  var instrucaoSql = `
      SELECT DISTINCT DATE_FORMAT(timestamp, '%Y-%m-%d') AS date
        FROM estatisticas_horarias
        WHERE fkServidor = ${serverId}
        ORDER BY date DESC;
  `;
  console.log("Executando a instrução SQL: \n", instrucaoSql);
  console.log("Parametros para consulta:", [serverId]);

  try {
    var [rows] = await database.executar(instrucaoSql, [serverId]);

    console.log("Resultado da consulta:", rows);
    console.log("Tipo de rows:", typeof rows);
    console.log("Estrutura de rows:", rows);

    rows = Array.isArray(rows) ? rows : [rows];
    console.log("Estrutura de rows após transformação:", rows);

    if (rows.length > 0) {
      console.log("Mapeando datas:", rows.map(row => row.date));
      return rows.map(row => row.date);
    } else {
      console.log("Nenhuma data encontrada.");
      return [];
    }
  } catch (error) {
    console.error("Erro ao executar a consulta:", error);
    throw error;
  }
}


async function dadosGrafico(serverId, component, date) {
  var instrucaoSql = `
      SELECT HOUR(timestamp) AS hour, desvio_padrao
        FROM estatisticas_horarias
        WHERE fkServidor = ${serverId}
          AND componente = "${component}"
          AND DATE(timestamp) = "${date}"
        ORDER BY hour;
  `;
  console.log("Consulta SQL a ser executada: \n", instrucaoSql);
  console.log("Parâmetros para consulta:", [serverId, component, date]);

  try {
    // Executando a consulta
    var [rows] = await database.executar(instrucaoSql, [serverId, component, date]);
    
    // Log após execução da consulta para mostrar o resultado
    console.log("Resultado da consulta:", rows);

    // Garantir que o retorno seja tratado como um array
    if (!Array.isArray(rows)) {
      rows = [rows]; // Converte para array caso o resultado seja um único objeto
    }

    // Verificar se o array de resultados tem dados
    if (rows.length === 0) {
      console.log("Nenhum dado encontrado para os parâmetros fornecidos.");
      return []; // Retorna um array vazio
    } else {
      console.log("Dados encontrados:", rows);
      return rows; // Retorna os dados encontrados
    }
  } catch (erro) {
    // Se ocorrer um erro na execução da consulta
    console.error("Erro ao executar consulta:", erro);
    throw erro; // Relança o erro para que possa ser tratado em outro lugar, se necessário
  }
}


module.exports = {
  getServidores,
  getDesvioPadraoCPU,
  getDesvioPadraoRAM,
  guardarResultado,
  datasDisponiveis,
  dadosGrafico
};