var database = require("../database/config")

async function getServidores() {
  var instrucaoSql = `
      SELECT idServidor, identificacao 
      FROM servidor;
  `;
  console.log("Executando a instrução SQL:\n", instrucaoSql);
  var [rows] = await database.executar(instrucaoSql);
  console.log("Resultado da consulta (getServidores):", rows);
  return Array.isArray(rows) ? rows : [rows];
}

async function getDesvioPadraoCPU(servidorId) {
  var instrucaoSql = `
    SELECT STDDEV(percent_use_cpu) AS desvio_padrao_cpu
    FROM registro
    WHERE fkServidor = ${servidorId} AND dtHora >= NOW() - INTERVAL 1 HOUR;
  `;
  console.log("Executando a instrução SQL: \n" + instrucaoSql);
  var rows = await database.executar(instrucaoSql);
  var desvioPadraoCPU;

  if (Array.isArray(rows)) {
    desvioPadraoCPU = rows[0]?.desvio_padrao_cpu;
  } else {
    desvioPadraoCPU = rows.desvio_padrao_cpu;
  }

  return desvioPadraoCPU || null;
}

async function getDesvioPadraoRAM(servidorId) {
  var instrucaoSql = `
    SELECT STDDEV(percent_use_ram) AS desvio_padrao_ram
    FROM registro
    WHERE fkServidor = ${servidorId} AND dtHora >= NOW() - INTERVAL 1 HOUR;
  `;
  console.log("Executando a instrução SQL: \n" + instrucaoSql);
  var rows = await database.executar(instrucaoSql);
  var desvioPadraoRAM;

  if (Array.isArray(rows)) {
    desvioPadraoRAM = rows[0]?.desvio_padrao_ram;
  } else {
    desvioPadraoRAM = rows.desvio_padrao_ram;
  }

  return desvioPadraoRAM || null;
}

async function guardarResultado(servidorId, componente, desvioPadrao, oscilacao) {
  var instrucaoSql = `
    INSERT INTO estatisticas_horarias (fkServidor, componente, timestamp, desvio_padrao, oscilacao)
    VALUES (${servidorId}, "${componente}", NOW(), ${desvioPadrao}, ${oscilacao});
  `;
  console.log("Executando a instrução SQL: \n" + instrucaoSql);
  await database.executar(instrucaoSql, [servidorId, componente, desvioPadrao, oscilacao]);
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
    var rows = await database.executar(instrucaoSql, [serverId]);

    console.log("Resultado da consulta:", rows);
    console.log("Tipo de rows:", typeof rows);
    console.log("Estrutura de rows:", rows);

    // Verifica se rows é um array, caso contrário coloca em um array
    rows = Array.isArray(rows) ? rows : [rows];
    console.log("Estrutura de rows após transformação:", rows);

    if (rows.length > 0) {
      console.log("Mapeando datas:", rows.map(row => row.date));
      return rows.map(row => row.date);  // Retorna todas as datas encontradas
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
    var rows = await database.executar(instrucaoSql, [serverId, component, date]);

    console.log("Resultado da consulta:", rows);

    if (Array.isArray(rows) && rows.length === 0) {
      console.log("Nenhum dado encontrado para os parâmetros fornecidos.");
      return [];
    } else {
      console.log("Dados encontrados:", rows);
      return rows;
    }
  } catch (erro) {
    console.error("Erro ao executar consulta:", erro);
    throw erro;
  }
}

async function getDados(servidorId) {
  var instrucaoSql = `
      SELECT dtHora, percent_use_cpu, percent_use_ram
      FROM registro
      WHERE fkServidor = ${servidorId} AND dtHora >= NOW() - INTERVAL 1 HOUR;
  `;
  console.log("Consulta SQL: \n", instrucaoSql); 
  const resultado = await database.executar(instrucaoSql);
  
  console.log("Resultado da consulta:", JSON.stringify(resultado));

  if (Array.isArray(resultado) && resultado.length > 0) {
      return resultado;
  } else {
      console.log("Nenhum dado encontrado.");
      return []; 
  }
}

module.exports = {
  getServidores,
  getDesvioPadraoCPU,
  getDesvioPadraoRAM,
  guardarResultado,
  datasDisponiveis,
  dadosGrafico,
  getDados
};