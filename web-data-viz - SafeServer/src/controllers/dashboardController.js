var dashboardModel = require("../models/dashboardModel");

function obterCargos(req, res) {
    var idEmpresa = req.body.idEmpresaServer;

    if (idEmpresa == undefined) {
        res.status(400).send("A empresa está indefinida!");
    } else {
        dashboardModel.obterCargos(idEmpresa)
            .then(
                function (resultadoSelect) {
                    console.log(`\nResultados encontrados: ${resultadoSelect.length}`);
                    console.log(`Resultados: ${JSON.stringify(resultadoSelect)}`); // transforma JSON em String

                    if (resultadoSelect.length == 0) {
                        res.status(403).send("Nenhum resultado encontrado");
                    } else {
                        var cargo = [];
                        var nivelPermissao = [];
                        var chave = [];
                        for (i = 0; i < resultadoSelect.length; i++) {
                            cargo.push(resultadoSelect[i].cargo)
                            nivelPermissao.push(resultadoSelect[i].nivelPermissao)
                            chave.push(resultadoSelect[i].chave)
                        }
                        console.log(cargo, nivelPermissao, chave)
                        // console.log(devolucao)
                        res.json({
                            cargo: cargo,
                            nivelPermissao: nivelPermissao,
                            chave: chave
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

function obterFunc(req, res) {
    var idEmpresa = req.body.idEmpresaServer;

    if (idEmpresa == undefined) {
        res.status(400).send("A empresa está indefinida!");
    } else {
        dashboardModel.obterFunc(idEmpresa)
            .then(
                function (resultadoSelect) {
                    console.log(`\nResultados encontrados: ${resultadoSelect.length}`);
                    console.log(`Resultados: ${JSON.stringify(resultadoSelect)}`); // transforma JSON em String

                    if (resultadoSelect.length == 0) {
                        res.status(403).send("Nenhum resultado encontrado");
                    } else {
                        var nome = [];
                        var email = [];
                        var cpf = [];
                        var cargo = [];
                        for (i = 0; i < resultadoSelect.length; i++) {
                            nome.push(resultadoSelect[i].nome)
                            cargo.push(resultadoSelect[i].cargo)
                            email.push(resultadoSelect[i].email)
                            cpf.push(resultadoSelect[i].cpf)
                        }
                        res.json({
                            nome: nome,
                            email: email,
                            cpf: cpf,
                            cargo: cargo,
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
    obterCargos,
    obterFunc
}