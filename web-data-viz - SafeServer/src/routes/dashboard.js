var express = require("express");
var router = express.Router();

var dashboardController = require("../controllers/dashboardController");

//Recebendo os dados do html e direcionando para a função cadastrar de usuarioController.js
router.post("/obterCargos", function (req, res) {
    dashboardController.obterCargos(req, res);
})

router.post("/obterFunc", function (req, res) {
    dashboardController.obterFunc(req, res);
})

router.get("/buscarCpueRam/:idServidor", function(req, res){
    dashboardController.buscarCpueRam(req, res);
})

router.get("/buscarDadosRec/:idServidor", function(req, res){
    dashboardController.buscarDadosRec(req, res);
})

router.get("/buscarDadosEnv/:idServidor", function(req, res){
    dashboardController.buscarDadosEnv(req, res);
})

router.post("/cadastrarCargo", function (req, res) {
    dashboardController.cadastrarCargo(req, res);
})

router.post("/registrar_servidor", function (req, res) {
    dashboardController.registrar_servidor(req, res);
})

router.get("/wordcloud", function (req, res) {
    dashboardController.wordcloud(req, res);
})


router.get("/feriado/:nomeServidor/:empresa", function (req, res) {
    dashboardController.feriado(req, res);
});

router.get("/servidor/:empresa", function (req, res) {
    dashboardController.servidor(req, res);
})

router.get("/periodo/:empresa", function (req, res) {
    dashboardController.periodo(req, res);
})

router.get("/analisar", function (req, res) {
    dashboardController.analisar(req, res);
});

router.get("/comparar", function (req, res) {
    dashboardController.comparar(req, res);
});


module.exports = router;