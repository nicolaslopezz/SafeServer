package org.example;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDateTime;
@JsonIgnoreProperties(ignoreUnknown = true)
public class Dado {

    @JsonProperty("CPU%")
    private Double dados_cpu;

    @JsonProperty("DataHora")
    private String data_hora;

    @JsonProperty("RAM-GB-Livre")
    private Double dados_ramGB_livre;

    @JsonProperty("RAM-GB-USO")
    private Double dados_ramGB_uso;

    @JsonProperty("RAM%")
    private Double dados_ram_porcentagem;

    @JsonProperty("REDE_REC")
    private Double dados_rede_rec;

    @JsonProperty("REDE_ENV")
    private Double dados_rede_env;

    public Double getDados_cpu() {
        return dados_cpu;
    }

    public void setDados_cpu(Double dados_cpu) {
        this.dados_cpu = dados_cpu;
    }

    public String getData_hora() {
        return data_hora;
    }

    public void setData_hora(String data_hora) {
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

    public Double getDados_rede_rec() {
        return dados_rede_rec;
    }

    public void setDados_rede_rec(Double dados_rede_rec) {
        this.dados_rede_rec = dados_rede_rec;
    }

    public Double getDados_rede_env() {
        return dados_rede_env;
    }

    public void setDados_rede_env(Double dados_rede_env) {
        this.dados_rede_env = dados_rede_env;
    }

    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder("Dado{");
        sb.append("dados_cpu=").append(dados_cpu);
        sb.append(", data_hora='").append(data_hora).append('\'');
        sb.append(", dados_ramGB_livre=").append(dados_ramGB_livre);
        sb.append(", dados_ramGB_uso=").append(dados_ramGB_uso);
        sb.append(", dados_ram_porcentagem=").append(dados_ram_porcentagem);
        sb.append(", dados_rede_rec=").append(dados_rede_rec);
        sb.append(", dados_rede_env=").append(dados_rede_env);
        sb.append('}');
        return sb.toString();
    }
}
