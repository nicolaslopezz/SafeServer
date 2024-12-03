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

function buscarCpueRam(req, res){
    var idServidor = req.params.idServidor;

    console.log(`Recuperando últimos dados de Ram e Cpu para o servidor com ID: ${idServidor}`);

dashboardModel.buscarCpueRam(idServidor).then((resultado) => {
   if(resultado.length > 0){
    res.status(200).json(resultado);
   } else{
    res.status(204).send("Nenhum resultado encontrado!")
   }
    
})
}

function buscarDadosRec(req, res){
    var idServidor = req.params.idServidor;

    console.log(`Recuperando últimos dados de redeRecebida para o sevidor com ID: ${idServidor}`)

    dashboardModel.buscarDadosRec(idServidor).then((resultado) =>{
        if(resultado.length > 0){
            res.status(200).json(resultado);
        } else{
            res.status(204).send("Nenhum resultado encontrado.")
        }
    })
}

function buscarDadosEnv(req, res){
    var idServidor = req.params.idServidor;

    console.log(`Recuperando últimos dasos de RedeEnviada para o servidor com ID: ${idServidor}`)

    dashboardModel.buscarDadosEnv(idServidor).then((resultado) =>{
        if(resultado.length > 0){
            res.status(200).json(resultado);
        } else{
            res.status(204).send("Nenhum resultado encontrado.")
        }
    })
}

function cadastrarCargo(req, res) {
    var nome = req.body.nomeServer;
    var nivelPermissao = req.body.nivelPermissaoServer;
    var fkEmpresa = req.body.fkEmpresaServer;

    if (nome == undefined) {
        res.status(400).send("Seu nome está undefined!");
    } else if (nivelPermissao == undefined) {
        res.status(400).send("Seu email está undefined!");
    } else if (fkEmpresa == undefined) {
        res.status(400).send("Sua senha está undefined!");
    } else {
        dashboardModel.cadastrarCargo(nome, nivelPermissao, fkEmpresa)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro do cargo! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}

function registrar_servidor(req, res) {
    var nome = req.body.nomeServer;
    var regiao = req.body.regiaoServer;
    var fkEmpresa = req.body.fkEmpresaServer;

    if (nome == undefined) {
        res.status(400).send("Seu nome está undefined!");
    } else if (regiao == undefined) {
        res.status(400).send("Sua região está undefined!");
    } else if (fkEmpresa == undefined) {
        res.status(400).send("Sua região está undefined!");
    } else {
        dashboardModel.registrar_servidor(nome, regiao, fkEmpresa)
            .then(
                function (resultado) {
                    res.json(resultado);
                }
            ).catch(
                function (erro) {
                    console.log(erro);
                    console.log(
                        "\nHouve um erro ao realizar o cadastro do cargo! Erro: ",
                        erro.sqlMessage
                    );
                    res.status(500).json(erro.sqlMessage);
                }
            );
    }
}

function wordcloud(req, res) { 

    dashboardModel.wordcloud()
        .then(
         
            function (resultado) {
                res.status(200).json(resultado);
            }
        )
        .catch(
            function (erro) {
             
                console.log(erro);
                console.log("Houve um erro ao realizar o post: ", erro.sqlMessage);
                res.status(500).json(erro.sqlMessage);
            }
        );
}

function feriado(req, res) { 
    const empresa = req.params.empresa;
    const nomeServidor = req.params.nomeServidor
   
    dashboardModel.feriado(empresa,nomeServidor)
        .then(
         
            function (resultado) {
                res.status(200).json(resultado);
            }
        )
        .catch(
            function (erro) {
             
                console.log(erro);
                console.log("Houve um erro ao realizar o post: ", erro.sqlMessage);
                res.status(500).json(erro.sqlMessage);
            }
        );
}

function servidor(req, res) { 
    const empresa = req.params.empresa;

    dashboardModel.servidor(empresa)
        .then(
         
            function (resultado) {
                res.status(200).json(resultado);
            }
        )
        .catch(
            function (erro) {
             
                console.log(erro);
                console.log("Houve um erro ao realizar o post: ", erro.sqlMessage);
                res.status(500).json(erro.sqlMessage);
            }
        );
}


function periodo(req, res) { 
    const empresa = req.params.empresa;

    dashboardModel.periodo(empresa)
        .then(
         
            function (resultado) {
                res.status(200).json(resultado);
            }
        )
        .catch(
            function (erro) {
             
                console.log(erro);
                console.log("Houve um erro ao realizar o post: ", erro.sqlMessage);
                res.status(500).json(erro.sqlMessage);
            }
        );
}


function analisar(req, res) {

    console.log(req.query)
    // Acessando os parâmetros da query string
    const servidores = JSON.parse(req.query.servidores);  
    const periodos = JSON.parse(req.query.periodos);  
    const componentes = JSON.parse(req.query.componentes);  
  
    console.log('Servidores:',servidores);
    console.log('Períodos:',periodos);
    console.log('Componentes:',componentes);

    dashboardModel.analisar(servidores, periodos, componentes)
      .then((resultado) => {
        if (resultado.length > 0) {
          res.status(200).json(resultado);
        } else {
          res.status(204).send("Nenhum resultado encontrado!");
        }
      })
      .catch((erro) => {
        console.error('Erro ao buscar relatório:', erro);
        res.status(500).send('Erro ao buscar relatório');
      });
  }


  function comparar(req, res) {
    const servidores = JSON.parse(req.query.servidores);  
    const periodos = JSON.parse(req.query.periodos);  
    const componentes = JSON.parse(req.query.componentes);  
  
    dashboardModel.comparar(servidores, periodos, componentes)
      .then((resultado) => {
        if (resultado.length > 0) {
          res.status(200).json(resultado);
        } else {
          res.status(204).send("Nenhum resultado encontrado!");
        }
      })
      .catch((erro) => {
        console.error('Erro ao buscar relatório:', erro);
        res.status(500).send('Erro ao buscar relatório');
      });
  }



  function comparar2(req, res) {
    const servidores = JSON.parse(req.query.servidores);  
    const periodos = JSON.parse(req.query.periodos);  
    const componentes = JSON.parse(req.query.componentes);  
  
    dashboardModel.comparar2(servidores, periodos, componentes)
      .then((resultado) => {
        if (resultado.length > 0) {
          res.status(200).json(resultado);
        } else {
          res.status(204).send("Nenhum resultado encontrado!");
        }
      })
      .catch((erro) => {
        console.error('Erro ao buscar relatório:', erro);
        res.status(500).send('Erro ao buscar relatório');
      });
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
}