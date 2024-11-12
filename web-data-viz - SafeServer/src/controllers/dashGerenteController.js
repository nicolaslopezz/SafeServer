var dashGerenteModel = require("../models/dashGerenteModel.js");


function obterDados(req, res) {
    var idEmpresa = req.body.idEmpresaServer;

    if (idEmpresa == undefined) {
        res.status(400).send("A empresa está indefinida!");
    } else {
        dashGerenteModel.obterDados(idEmpresa)
            .then(
                function (resultadoSelect) {
                    console.log(`\nResultados encontrados: ${resultadoSelect.length}`);
                    console.log(`Resultados: ${JSON.stringify(resultadoSelect)}`); // transforma JSON em String

                    if (resultadoSelect.length == 0) {
                        res.status(403).send("Nenhum resultado encontrado");
                    } else {
                        var alertas = [];
                        var dia = [];
                        var servidor = [];
                        var componente = [];
                        for (i = 0; i < resultadoSelect.length; i++) {
                            alertas.push(resultadoSelect[i].alertas)
                            componente.push(resultadoSelect[i].componente)
                            dia.push( `"${resultadoSelect[i].dia}"`)
                            servidor.push(resultadoSelect[i].servidor)
                        }
                        res.json({
                            alertas: alertas,
                            dia: dia,
                            servidor: servidor,
                            componente: componente
                        })
                    }


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