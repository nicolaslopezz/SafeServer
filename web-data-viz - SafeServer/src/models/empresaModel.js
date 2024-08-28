var database = require("../database/config");

function buscarPorId(idEmpresa) {
  var instrucaoSql = `SELECT * FROM empresa WHERE idEmpresa = '${idEmpresa}'`;

  return database.executar(instrucaoSql);
}

function listar() {
  var instrucaoSql = `SELECT idEmpresa, nomeFantasia, razaoSocial, CNPJ, chaveAcesso FROM empresa`;

  return database.executar(instrucaoSql);
}

function buscarPorCnpj(CNPJ) {
  var instrucaoSql = `SELECT * FROM empresa WHERE CNPJ = '${CNPJ}'`;

  return database.executar(instrucaoSql);
}

function cadastrar(nomeFantasia, razaoSocial, CNPJ) {
  var instrucaoSql = `INSERT INTO empresa (nomeFantasia, razaoSocial, CNPJ) VALUES ('${nomeFantasia}', '${razaoSocial}', '${CNPJ}')`;

  return database.executar(instrucaoSql);
}

module.exports = { buscarPorCnpj, buscarPorId, cadastrar, listar };
