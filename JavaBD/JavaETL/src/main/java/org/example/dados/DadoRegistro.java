package org.example.dados;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class DadoRegistro implements Dado {

    @JsonProperty("CPU%")
    private Double dados_cpu;

    @JsonProperty("DataHora")
    private String data_hora;

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
        sb.append(", dados_ram_porcentagem=").append(dados_ram_porcentagem);
        sb.append(", dados_rede_rec=").append(dados_rede_rec);
        sb.append(", dados_rede_env=").append(dados_rede_env);
        sb.append('}');
        return sb.toString();
    }
}
