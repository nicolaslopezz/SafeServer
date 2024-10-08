package org.example;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Dado {

    @JsonProperty("CPU%")
    private Double dados_cpu;

    @JsonProperty("RAMGB")
    private Double dados_ram;

    @JsonProperty("REDE_RECV")
    private Double dados_rede;

    public Double getDados_cpu() {
        return dados_cpu;
    }

    public void setDados_cpu(Double dados_cpu) {
        this.dados_cpu = dados_cpu;
    }

    public Double getDados_ram() {
        return dados_ram;
    }

    public void setDados_ram(Double dados_ram) {
        this.dados_ram = dados_ram;
    }

    public Double getDados_rede() {
        return dados_rede;
    }

    public void setDados_rede(Double dados_rede) {
        this.dados_rede = dados_rede;
    }
}
