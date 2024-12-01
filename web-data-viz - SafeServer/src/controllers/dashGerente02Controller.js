var dashGerente02Model = require("../models/dashGerente02Model.js");

async function calcularDesvioPadraoeOscilacao() {
    try {
        console.log("Iniciando cálculo automático de desvio padrão e oscilação...");

        var servidores = await dashGerente02Model.getServidores();

        for (var servidor of servidores) {
            console.log(`Processando servidor: ${servidor.idServidor} - ${servidor.identificacao}`);

            var dados = await dashGerente02Model.getDados(servidor.idServidor);

            console.log("Dados:", JSON.stringify(dados));
            var desvioPadraoCPU = await dashGerente02Model.getDesvioPadraoCPU(servidor.idServidor);
            var desvioPadraoRAM = await dashGerente02Model.getDesvioPadraoRAM(servidor.idServidor);

            let cpuOscillation = 0;
            let ramOscillation = 0;

            for (let i = 1; i < dados.length; i++) {
                cpuOscillation += Math.abs(dados[i].percent_use_cpu - dados[i - 1].percent_use_cpu);
                ramOscillation += Math.abs(dados[i].percent_use_ram - dados[i - 1].percent_use_ram);
            }

            if (desvioPadraoCPU !== null && !isNaN(desvioPadraoCPU) && typeof desvioPadraoCPU === 'number') {
                await dashGerente02Model.guardarResultado(servidor.idServidor, 'cpu', desvioPadraoCPU, cpuOscillation);
                console.log(`Servidor: ${servidor.identificacao}, Componente: CPU, Desvio Padrão: ${desvioPadraoCPU}, Oscilação: ${cpuOscillation}`);
            } else {
                console.log(`Desvio padrão da CPU não encontrado ou é inválido para o servidor ${servidor.identificacao}`);
            }

            if (desvioPadraoRAM !== null && !isNaN(desvioPadraoRAM) && typeof desvioPadraoRAM === 'number') {
                await dashGerente02Model.guardarResultado(servidor.idServidor, 'ram', desvioPadraoRAM, ramOscillation);
                console.log(`Servidor: ${servidor.identificacao}, Componente: RAM, Desvio Padrão: ${desvioPadraoRAM}, Oscilação: ${ramOscillation}`);
            } else {
                console.log(`Desvio padrão da RAM não encontrado ou é inválido para o servidor ${servidor.identificacao}`);
            }
        }
    } catch (error) {
        console.error('Erro ao calcular desvio padrão e oscilação:', error.message);
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
    calcularDesvioPadraoeOscilacao,
    datasDisponiveis,
    dadosGrafico
}