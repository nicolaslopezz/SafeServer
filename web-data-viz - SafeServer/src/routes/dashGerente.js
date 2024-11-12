var express = require("express");
var router = express.Router();

var dashGerenteController = require("../controllers/dashGerenteController.js");

router.post("/obterDados", function (req, res) {
    dashGerenteController.obterDados(req, res);
});

module.exports = router;