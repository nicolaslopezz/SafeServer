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

function buscarCpueRam(idServidor) {
    var instrucaoSql = `
    SELECT idServidor, percent_use_cpu, percent_use_ram, time(dtHora) as hora from registro JOIN servidor ON idServidor = fkServidor
    WHERE fkServidor = ${idServidor};
    `
    console.log("Executando instrução SQL: " + instrucaoSql)
    return database.executar(instrucaoSql);
}

function buscarDadosRec(idServidor){
    var instrucaoSql= `SELECT recebido_rede, time(dtHora) as hora from registro WHERE fkServidor= ${idServidor};`

    console.log("Executando instrução SQL: " + instrucaoSql)
    return database.executar(instrucaoSql);
}

function buscarDadosEnv(idServidor){
    var instrucaoSql = `SELECT enviado_rede, time(dtHora) as hora from registro JOIN servidor on fkServidor= ${idServidor};`

    console.log("Executando instução SQL: " + instrucaoSql)
    return database.executar(instrucaoSql);
}

function registrar_servidor(nome, regiao, fkEmpresa) {
    var instrucaoSql = `
        INSERT INTO servidor (identificacao, regiao, fkEmpresa) VALUES 
            ("${nome}", "${regiao}", ${fkEmpresa});
    `;
    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function gerarCodigo() {
    return Math.random().toString(36).substr(-8).toUpperCase()
}

function wordcloud() {
    var instrucaoSql = `select * from feriado_freq`;

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function feriado(empresa, nomeServidor) {
    var instrucaoSql = `SELECT 
    DATE(r.dtHora) AS dataRegistro,
    s.identificacao AS nomeServidor,
    AVG(r.percent_use_cpu) AS mediaPercentualCPU
FROM 
    registro r
JOIN 
    servidor s ON r.fkServidor = s.idServidor
WHERE 
    DATE(r.dtHora) IN ('2024-12-25', '2024-01-01', '2024-03-29', '2024-03-31', '2024-05-01')
    AND s.fkEmpresa = ${empresa}
    AND s.identificacao = "${nomeServidor}"
GROUP BY 
    DATE(r.dtHora), s.identificacao
ORDER BY 
    dataRegistro, nomeServidor;
`;

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function servidor(empresa) {
    var instrucaoSql = `select identificacao,idServidor from servidor where fkEmpresa = ${empresa} `;

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}

function periodo(empresa) {
    var instrucaoSql = `SELECT DISTINCT MONTH(r.dtHora) AS mes
FROM registro r
JOIN servidor s ON r.fkServidor = s.idServidor
JOIN empresa e ON s.fkEmpresa = e.idEmpresa
WHERE e.idEmpresa = ${empresa}
ORDER BY mes DESC;
 `;

    console.log("Executando a instrução SQL: \n" + instrucaoSql);
    return database.executar(instrucaoSql);
}


function analisar(servidores,periodos,componentes) { 
    
    console.log('Servidoresss:', servidores);
    console.log('Períodosss:', periodos);
    console.log('Componentesss:', componentes);

    const instrucaoSql = `
        SELECT 
            a.componente,
            s.identificacao AS servidor,
            MONTH(r.dtHora) AS mes,
            COUNT(a.idAlerta) AS total_alertas,
            AVG(CASE 
                WHEN a.componente = 'CPU' THEN r.percent_use_cpu
                WHEN a.componente = 'RAM' THEN r.percent_use_ram
                WHEN a.componente = 'REDE (RECEBIDA)' THEN r.recebido_rede
                WHEN a.componente = 'REDE (ENVIADA)' THEN r.enviado_rede
                ELSE NULL
            END) AS valor_medio
        FROM 
            alerta a
        JOIN 
            registro r ON a.fkRegistro = r.idRegistro
        JOIN 
            servidor s ON r.fkServidor = s.idServidor
        WHERE 
            s.identificacao IN (${servidores.map(servidor => `'${servidor}'`).join(', ')}) 
            AND MONTH(r.dtHora) IN (${periodos.join(', ')}) 
            AND a.componente IN (${componentes.map(componente => `'${componente}'`).join(', ')})
        GROUP BY 
            a.componente, s.identificacao, MONTH(r.dtHora)
        ORDER BY 
            mes DESC, a.componente;
    `;

    console.log(instrucaoSql)

    return database.executar(instrucaoSql);
}

module.exports = {
    obterCargos,
    obterFunc,
    buscarCpueRam,
    buscarDadosRec,
    buscarDadosEnv,
    cadastrarCargo,
    registrar_servidor,
    wordcloud,
    feriado,
    servidor,
    periodo,
    analisar
};