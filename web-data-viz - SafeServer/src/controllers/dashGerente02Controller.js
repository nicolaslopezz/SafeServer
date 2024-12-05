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
        console.error("Erro ao buscar dados do gráfico de estabilidade:", error);
        res.status(500).json({ error: 'Erro ao buscar dados do gráfico.' });
    }
}

async function dadosGraficoOscilacao(req, res) {
    var { serverId, component, date } = req.query;
    try {
        var data = await dashGerente02Model.dadosGraficoOscilacao(serverId, component, date);
        res.json(data);
    } catch (error) {
        console.error("Erro ao buscar dados do gráfico de oscilação:", error);
        res.status(500).json({ error: 'Erro ao buscar dados do gráfico.' });
    }
}

async function getMaiorMenorEstabilidade(req, res) {
    var { serverId, component, date } = req.query;
    try {
        var maiorEstabilidade = await dashGerente02Model.getMaiorEstabilidade(serverId, component, date);
        var menorEstabilidade = await dashGerente02Model.getMenorEstabilidade(serverId, component, date);

        res.json({
            maiorEstabilidade: maiorEstabilidade[0],
            menorEstabilidade: menorEstabilidade[0]
        });
    } catch (error) {
        console.error("Erro ao buscar dados do gráfico de estabilidade:", error);
        res.status(500).json({ error: 'Erro ao buscar dados do gráfico de estabilidade.' });
    }
}

async function getMaiorMenorOscilacao(req, res) {
    var { serverId, component, date } = req.query;
    try {
        var maiorOscilacao = await dashGerente02Model.getMaiorOscilacao(serverId, component, date);
        var menorOscilacao = await dashGerente02Model.getMenorOscilacao(serverId, component, date);

        res.json({
            maiorOscilacao: maiorOscilacao[0],
            menorOscilacao: menorOscilacao[0]
        });
    } catch (error) {
        console.error("Erro ao buscar dados do gráfico de oscilação:", error);
        res.status(500).json({ error: 'Erro ao buscar dados do gráfico de oscilação.' });
    }
}

async function contarExcedentesDesvioPadrao(req, res) {
    var { serverId, component, date, limite } = req.query;
    try {
        var contagemExcedentes = await dashGerente02Model.contarExcedentesDesvioPadrao(serverId, component, date, limite);

        res.json({
            contagemExcedentes: contagemExcedentes[0]
        });
    } catch (error) {
        console.error("Erro ao buscar dados de excedentes de desvio padrão:", error);
        res.status(500).json({ error: 'Erro ao buscar dados de excedentes de desvio padrão' });
    }
}

async function contarExcedentesOscilacao(req, res) {
    var { serverId, component, date, limite } = req.query;
    try {
        var contagemExcedentes = await dashGerente02Model.contarExcedentesOscilacao(serverId, component, date, limite);

        res.json({
            contagemExcedentes: contagemExcedentes[0]
        });
    } catch (error) {
        console.error("Erro ao buscar dados de excedentes de oscilação:", error);
        res.status(500).json({ error: 'Erro ao buscar dados de excedentes de oscilação' });
    }
}

async function obterServidores(req, res) {
    var empresa = req.params.empresa;
    try {
        var servers = await dashGerente02Model.obterServidores(empresa);
        res.json(servers);
    } catch (error) {
        console.error("Erro ao buscar servidores cadastrados:", error);
        res.status(500).json({ error: 'Erro ao buscar servidores cadastrados.' });
    }
}

module.exports = {
    calcularDesvioPadraoeOscilacao,
    datasDisponiveis,
    dadosGrafico,
    dadosGraficoOscilacao,
    getMaiorMenorEstabilidade,
    getMaiorMenorOscilacao,
    contarExcedentesDesvioPadrao,
    contarExcedentesOscilacao,
    obterServidores
}