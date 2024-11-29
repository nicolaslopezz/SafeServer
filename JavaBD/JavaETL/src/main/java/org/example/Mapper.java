package org.example;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public interface Mapper {
    public List<Dado> map(InputStream inputStream) throws IOException;

    public static Mapper ObterTipoAqruivo(String nome) {
        if (nome.contains("json")) {
            return new MapperJson();
        } else if (nome.contains("csv")){
            return new MapperCsv();
        }
        return null;
    }
}
