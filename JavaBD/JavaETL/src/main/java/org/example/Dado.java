package org.example;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDateTime;

public class Dado {

    @JsonProperty("CPU%")
    private Double dados_cpu;

    @JsonProperty("DataHora")
    private LocalDateTime data_hora;

    @JsonProperty("RAM-GB-Livre")
    private Double dados_ramGB_livre;

    @JsonProperty("RAM-GB-USO")
    private Double dados_ramGB_uso;

    @JsonProperty("RAM%")
    private Double dados_ram_porcentagem;

    @JsonProperty("REDE_REC")
    private Integer dados_rede_rec;

    @JsonProperty("REDE_ENV")
    private Integer dados_rede_env;

    public Double getDados_cpu() {
        return dados_cpu;
    }

    public void setDados_cpu(Double dados_cpu) {
        this.dados_cpu = dados_cpu;
    }

    public LocalDateTime getData_hora() {
        return data_hora;
    }

    public void setData_hora(LocalDateTime data_hora) {
        this.data_hora = data_hora;
    }

    public Double getDados_ramGB_livre() {
        return dados_ramGB_livre;
    }

    public void setDados_ramGB_livre(Double dados_ramGB_livre) {
        this.dados_ramGB_livre = dados_ramGB_livre;
    }

    public Double getDados_ramGB_uso() {
        return dados_ramGB_uso;
    }

    public void setDados_ramGB_uso(Double dados_ramGB_uso) {
        this.dados_ramGB_uso = dados_ramGB_uso;
    }

    public Double getDados_ram_porcentagem() {
        return dados_ram_porcentagem;
    }

    public void setDados_ram_porcentagem(Double dados_ram_porcentagem) {
        this.dados_ram_porcentagem = dados_ram_porcentagem;
    }

    public Integer getDados_rede_rec() {
        return dados_rede_rec;
    }

    public void setDados_rede_rec(Integer dados_rede_rec) {
        this.dados_rede_rec = dados_rede_rec;
    }

    public Integer getDados_rede_env() {
        return dados_rede_env;
    }

    public void setDados_rede_env(Integer dados_rede_env) {
        this.dados_rede_env = dados_rede_env;
    }
}
