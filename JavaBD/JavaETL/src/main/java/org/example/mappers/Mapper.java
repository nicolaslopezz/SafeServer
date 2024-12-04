package org.example.mappers;

import org.example.dados.Dado;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public interface Mapper {
    public List<Dado> map(InputStream inputStream) throws IOException;

    public static Mapper ObterTipoArquivo(String nome) {
        if (nome.contains("feriado")) {
            return new MapperCsvCrawler();
        } else if (nome.contains("json")) {
            return new MapperJson();
        } else if (nome.contains("csv")){
            return new MapperCsvRegistro();
        }
        return null;
    }
}
