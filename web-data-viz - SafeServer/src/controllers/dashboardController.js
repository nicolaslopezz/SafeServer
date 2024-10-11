var usuarioModel = require("../models/usuarioModel");

function obterCargos(req, res) {
    var idEmpresa = req.body.emailServer;

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
                    res.json({
                        // seguir amanhã
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
                console.log("\nHouve um erro ao realizar o login! Erro: ", erro.sqlMessage);
                res.status(500).json(erro.sqlMessage);
            }
        );
    }

}

module.exports = {
    obterCargos
}