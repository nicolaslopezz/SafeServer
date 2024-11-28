package org.example;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.List;

public class CsvWriter {

    public ByteArrayOutputStream writeCsv(List<Dado> dados) throws IOException {

        ByteArrayOutputStream outputStream =new ByteArrayOutputStream();
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(outputStream, StandardCharsets.UTF_8));
        CSVPrinter csvPrinter =new CSVPrinter(writer, CSVFormat.DEFAULT.withHeader("CPU%",
                                                                                   "DataHora",
                                                                                   "RAM-GB-LIVRE",
                                                                                   "RAM-GB-USO",
                                                                                   "RAM%",
                                                                                   "REDE_REC",
                                                                                   "REDE_ENV"));

        for (Dado dado : dados) {
            csvPrinter.printRecord(
                dado.getDados_cpu(),
                dado.getData_hora(),
                dado.getDados_ramGB_livre(),
                dado.getDados_ramGB_uso(),
                dado.getDados_ram_porcentagem(),
                dado.getDados_rede_rec(),
                dado.getDados_rede_env()
            );
        }
            csvPrinter.flush();
            csvPrinter.close();
            writer.close();

        return outputStream;
    }
}
