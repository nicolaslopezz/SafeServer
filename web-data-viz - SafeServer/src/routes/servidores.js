var express = require("express");
var router = express.Router();

var servidoresController = require("../controllers/servidoresController.js");

router.get("/buscarServidor/:idEmpresa", function(req, res){
    servidoresController.buscarServidor(req, res);
})

module.exports = router;