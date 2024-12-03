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

function buscarDadosRec(idServidor) {
    var instrucaoSql = `SELECT idServidor, recebido_rede, time(dtHora) as hora from registro JOIN servidor ON idServidor = fkServidor 
     WHERE fkServidor = ${idServidor};`

    console.log("Executando instrução SQL: " + instrucaoSql)
    return database.executar(instrucaoSql);
}

function buscarDadosEnv(idServidor) {
    var instrucaoSql = `SELECT idServidor, enviado_rede, time(dtHora) as hora from registro JOIN servidor ON idServidor = fkServidor 
     WHERE fkServidor = ${idServidor};`

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

function analisar(servidores, periodos, componentes) {
    const mapComponentes = {
        'cpu': 'percent_use_cpu',
        'ram': 'percent_use_ram',
        'rede_recebida': 'recebido_rede',
        'rede_enviada': 'enviado_rede'
    };

    // Construindo a consulta SQL base
    let queryBase = `
        SELECT 
            'componenteDaVez' AS componente,
            s.identificacao AS servidor, 
            MIN(r.componenteDaVez) AS min, 
            MAX(r.componenteDaVez) AS max,
            ROUND(AVG(r.componenteDaVez), 2) AS media
        FROM 
            registro r
        JOIN 
            servidor s ON r.fkServidor = s.idServidor
        WHERE 
            MONTH(r.dtHora) IN (${periodos.join(', ')}) 
            AND s.identificacao IN (${servidores.map(s => `'${s}'`).join(', ')})
        GROUP BY 
            s.identificacao
    `;

    //consultas dinâmicas para cada componente
    let unionQueries = componentes.map(componente => {
        let queryComponente = queryBase.replace(/'componenteDaVez'/g, `'${mapComponentes[componente]}'`)
            .replace(/componenteDaVez/g, mapComponentes[componente]);
        return queryComponente;
    }).join(' UNION ALL ');


    return database.executar(unionQueries);
}



function comparar(servidores, periodos, componentes) {


    const instrucaoSql = `
        SELECT 
    s.identificacao AS servidor,
    COUNT(a.idAlerta) AS total_alertas
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
    s.identificacao 
ORDER BY 
    total_alertas DESC; 

    `;

    console.log(instrucaoSql)

    return database.executar(instrucaoSql);
}

function comparar2(servidores, periodos, componentes) {


    const instrucaoSql = `
      SELECT 
    a.componente AS componente,
    COUNT(a.idAlerta) AS total_alertas
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
    a.componente
ORDER BY 
    total_alertas DESC;

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
    analisar,
    comparar,
    comparar2
};