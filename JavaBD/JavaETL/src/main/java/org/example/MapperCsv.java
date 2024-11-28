package org.example;

import com.fasterxml.jackson.databind.MappingIterator;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class MapperCsv implements Mapper {

    public List<Dado> map(InputStream inputStream) throws IOException {
        CsvSchema csvSchema = CsvSchema.emptySchema().withHeader();
        CsvMapper mapper = new CsvMapper();
        MappingIterator<Dado> dados = mapper.readerFor(Dado.class).with(csvSchema).readValues(inputStream);
        return dados.readAll();
    }

}
