var express = require("express");
var router = express.Router();

var dashGerente02Controller = require("../controllers/dashGerente02Controller.js");

router.post('/calcular-desvio-padrao', async (req, res) => {
  try {
    await dashGerente02Controller.calcularDesvioPadrao();
    res.status(200).send('Cálculo realizado com sucesso.');
  } catch (error) {
    res.status(500).send('Erro ao calcular desvio padrão.');
  }
});

router.get('/datas', dashGerente02Controller.datasDisponiveis);
router.get('/grafico', dashGerente02Controller.dadosGrafico);
router.get('/grafico/osc', dashGerente02Controller.dadosGraficoOscilacao);
router.get('/metricas/stab', dashGerente02Controller.getMaiorMenorEstabilidade);
router.get('/metricas/osc', dashGerente02Controller.getMaiorMenorOscilacao);
router.get('/metricas/stab/exc', dashGerente02Controller.contarExcedentesDesvioPadrao);
router.get('/metricas/osc/exc', dashGerente02Controller.contarExcedentesOscilacao);

module.exports = router;
