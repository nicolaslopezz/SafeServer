var dashGerente02Model = require("../models/dashGerente02Model.js");

async function calcularDesvioPadrao() {
    try {
        var servidores = await dashGerente02Model.getServidores();

        for (var servidor of servidores) {

            var desvioPadraoCPU = await dashGerente02Model.getDesvioPadraoCPU(servidor.id);
            if (desvioPadraoCPU !== null) {
                await dashGerente02Model.guardarResultado(servidor.id, 'cpu', desvioPadraoCPU);
                console.log(`Servidor: ${servidor.nome}, Componente: CPU, Desvio Padrão: ${desvioPadraoCPU}`);
            }

            var desvioPadraoRAM = await dashGerente02Model.getDesvioPadraoRAM(servidor.id);
            if (desvioPadraoRAM !== null) {
                await dashGerente02Model.guardarResultado(servidor.id, 'ram', desvioPadraoRAM);
                console.log(`Servidor: ${servidor.nome}, Componente: RAM, Desvio Padrão: ${desvioPadraoRAM}`);
            }
        }
    } catch (error) {
        console.error('Erro ao calcular desvio padrão:', error.message);
    }
}

async function datasDisponiveis(req, res) {
    var { serverId } = req.query;
    try {
        var dates = await dashGerente02Model.datasDisponiveis(serverId);
        res.json(dates);
    } catch (error) {
        console.error("Erro ao buscar datas disponíveis:", error);
        res.status(500).json({ error: 'Erro ao buscar datas disponíveis.' });
    }
}

// Controlador para dados do gráfico
async function dadosGrafico(req, res) {
    var { serverId, component, date } = req.query;
    try {
        var data = await dashGerente02Model.dadosGrafico(serverId, component, date);
        res.json(data);
    } catch (error) {
        console.error("Erro ao buscar dados do gráfico:", error);
        res.status(500).json({ error: 'Erro ao buscar dados do gráfico.' });
    }
}

module.exports = {
    calcularDesvioPadrao,
    datasDisponiveis,
    dadosGrafico
}