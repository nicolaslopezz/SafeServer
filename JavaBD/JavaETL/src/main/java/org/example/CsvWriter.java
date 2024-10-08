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
        CSVPrinter csvPrinter =new CSVPrinter(writer, CSVFormat.DEFAULT.withHeader("CPU%", "RAMGB", "REDE_RECV"));

        for (Dado dado : dados) {
            csvPrinter.printRecord(
                dado.getDados_cpu(),
                dado.getDados_ram(),
                dado.getDados_rede()
            );
        }
            csvPrinter.flush();
            csvPrinter.close();
            writer.close();

        return outputStream;
    }
}
