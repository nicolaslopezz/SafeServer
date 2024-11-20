var servidoresdModel = require("../models/servidoresModel");

function buscarServidor(req, res){
    var idEmpresa = req.params.idEmpresa;

    console.log(`Recuperando últimos servidores de empresa com ID: ${idEmpresa}`);

    servidoresdModel.buscarServidor(idEmpresa).then((resultado) => {
       if(resultado.length > 0){
        res.status(200).json(resultado);
       } else{
        res.status(204).send("Nenhum resultado encontrado!")
       }
    })
}

module.exports = {
    buscarServidor
}