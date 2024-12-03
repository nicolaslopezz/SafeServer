package org.example.dados;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class DadoCrawler implements Dado {
    @JsonProperty("english_name")
    private String english_name;
    @JsonProperty("country_name")
    private String nome_pais;

    public String getEnglish_name() {
        return english_name;
    }

    public void setEnglish_name(String english_name) {
        this.english_name = english_name;
    }

    public String getNome_pais() {
        return nome_pais;
    }

    public void setNome_pais(String nome_pais) {
        this.nome_pais = nome_pais;
    }

    @Override
    public String toString() {
        final StringBuilder sb = new StringBuilder("DadoCrawler{");
        sb.append("feriado='").append(english_name).append('\'');
        sb.append(", nome_pais='").append(nome_pais).append('\'');
        sb.append('}');
        return sb.toString();
    }
}
