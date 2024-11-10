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
module.exports = router;