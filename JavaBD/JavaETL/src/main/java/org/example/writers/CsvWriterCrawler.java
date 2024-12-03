package org.example.writers;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.example.dados.Dado;
import org.example.dados.DadoCrawler;
import org.example.dados.DadoRegistro;

import java.io.BufferedWriter;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class CsvWriterCrawler implements CsvWriter {

    public ByteArrayOutputStream writeCsv(List<Dado> dados) throws IOException {

        ByteArrayOutputStream outputStream =new ByteArrayOutputStream();
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream, StandardCharsets.UTF_8));
        CSVPrinter csvPrinter = new CSVPrinter(writer, CSVFormat.DEFAULT.withHeader("Feriado",
                "País"));
        for (Dado dado : dados) {
            csvPrinter.printRecord(
                    ((DadoCrawler) dado).getEnglish_name(),
                    ((DadoCrawler) dado).getNome_pais());
        }
        csvPrinter.flush();
        csvPrinter.close();
        writer.close();
        return outputStream;
    }
}