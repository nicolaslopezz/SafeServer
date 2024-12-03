package org.example.writers;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;
import org.example.dados.Dado;
import org.example.dados.DadoRegistro;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class CsvWriterRegistro implements CsvWriter {

    public ByteArrayOutputStream writeCsv(List<Dado> dados) throws IOException {

            ByteArrayOutputStream outputStream =new ByteArrayOutputStream();
            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream, StandardCharsets.UTF_8));
            CSVPrinter csvPrinter = new CSVPrinter(writer, CSVFormat.DEFAULT.withHeader("CPU%",
                    "DataHora",
                    "RAM%",
                    "REDE_REC",
                    "REDE_ENV"));
            for (Dado dado : dados) {
                csvPrinter.printRecord(
                        ((DadoRegistro) dado).getDados_cpu(),
                        ((DadoRegistro) dado).getData_hora(),
                        ((DadoRegistro) dado).getDados_ram_porcentagem(),
                        ((DadoRegistro) dado).getDados_rede_rec(),
                        ((DadoRegistro) dado).getDados_rede_env());
            }
            csvPrinter.flush();
            csvPrinter.close();
            writer.close();
            return outputStream;
    }
}
