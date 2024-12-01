var dashGerente02Model = require("../models/dashGerente02Model.js");

async function calcularDesvioPadrao() {
    try {
        console.log("Iniciando cálculo automático do desvio padrão...");

        var servidores = await dashGerente02Model.getServidores();

        for (var servidor of servidores) {
            console.log(`Processando servidor: ${servidor.idServidor} - ${servidor.identificacao}`);
            var desvioPadraoCPU = await dashGerente02Model.getDesvioPadraoCPU(servidor.idServidor);

            if (desvioPadraoCPU !== null && !isNaN(desvioPadraoCPU) && typeof desvioPadraoCPU === 'number') {
                await dashGerente02Model.guardarResultado(servidor.idServidor, 'cpu', desvioPadraoCPU);
                console.log(`Servidor: ${servidor.identificacao}, Componente: CPU, Desvio Padrão: ${desvioPadraoCPU}`);
            } else {
                console.log(`Desvio padrão da CPU não encontrado ou é inválido para o servidor ${servidor.identificacao}`);
            }

            var desvioPadraoRAM = await dashGerente02Model.getDesvioPadraoRAM(servidor.idServidor);

            if (desvioPadraoRAM !== null && !isNaN(desvioPadraoRAM) && typeof desvioPadraoRAM === 'number') {
                await dashGerente02Model.guardarResultado(servidor.idServidor, 'ram', desvioPadraoRAM);
                console.log(`Servidor: ${servidor.identificacao}, Componente: RAM, Desvio Padrão: ${desvioPadraoRAM}`);
            } else {
                console.log(`Desvio padrão da RAM não encontrado ou é inválido para o servidor ${servidor.identificacao}`);
            }
        }
    } catch (error) {
        console.error('Erro ao calcular desvio padrão:', error.message);
        console.error(error);
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