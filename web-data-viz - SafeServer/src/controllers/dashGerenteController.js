var dashGerenteModel = require("../models/dashGerenteModel.js");


function obterDados(req, res) {
    var idEmpresa = req.body.idEmpresaServer;

    if (idEmpresa == undefined) {
        res.status(400).send("A empresa está indefinida!");
    } else {
        dashGerenteModel.obterDados(idEmpresa)
            .then(
                function (resultadoSelect) {
                    // console.log(`\nResultados encontrados: ${resultadoSelect.length}`);
                    // console.log(`Resultados: ${JSON.stringify(resultadoSelect)}`); // transforma JSON em String

                    if (resultadoSelect.length == 0) {
                        res.status(403).send("Nenhum resultado encontrado");
                    }
                    res.json(resultadoSelect)
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log("\nHouve um erro ao obter os dados! Erro: ", erro.sqlMessage);
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}

module.exports = {
    obterDados
}