var dashboardModel = require("../models/dashboardModel");

function obterCargos(req, res) {
    var idEmpresa = req.body.idEmpresaServer;
    console.log("CHEGUEI NO CONTROLLER COM:", idEmpresa)

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
                    // var devolucao = {
                    //     "cargo": [],
                    //     "nivelPermissao": [],
                    //     "chave": []
                    // };
                    // for(i = 0; i < resultadoSelect.length; i++) {
                    //     devolucao.cargo.push(resultadoSelect[i].cargo)
                    //     devolucao.nivelPermissao.push(resultadoSelect[i].nivelPermissao)
                    //     devolucao.chave.push(resultadoSelect[i].chave)
                    // }
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

                            //    const usuario = resultadoAutenticar[0]
                            //     res.json({
                            //         idFuncionario: resultadoAutenticar[0].idFuncionario,
                            //         email: resultadoAutenticar[0].email,
                            //         nome: resultadoAutenticar[0].nome,
                            //         senha: resultadoAutenticar[0].senha,
                            //         nivelPermissao: resultadoAutenticar[0].nivelPermissao,
                            //         idEmpresa: resultadoAutenticar[0].idEmpresa
                            //     });                                
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
    obterCargos
}