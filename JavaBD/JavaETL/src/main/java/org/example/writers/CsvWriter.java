package org.example.writers;

import org.example.dados.Dado;
import org.example.dados.DadoCrawler;
import org.example.dados.DadoRegistro;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.List;

public interface CsvWriter {
    public ByteArrayOutputStream writeCsv(List<Dado> dados) throws IOException;

    public static CsvWriter escolherWriter(Dado dado) {
        if (dado instanceof DadoRegistro) {
            return new CsvWriterRegistro();
        } else if (dado instanceof DadoCrawler){
            return new CsvWriterCrawler();
        }
        System.out.println("A lista não está em nenhum formato válido");
        return null;
    }
}
