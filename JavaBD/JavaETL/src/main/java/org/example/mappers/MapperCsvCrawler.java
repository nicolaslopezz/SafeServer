package org.example.mappers;

import com.fasterxml.jackson.databind.MappingIterator;
import com.fasterxml.jackson.dataformat.csv.CsvMapper;
import com.fasterxml.jackson.dataformat.csv.CsvSchema;
import org.example.dados.Dado;
import org.example.dados.DadoCrawler;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class MapperCsvCrawler implements Mapper {
    @Override
    public List<Dado> map(InputStream inputStream) throws IOException {
        CsvSchema csvSchema = CsvSchema.emptySchema().withHeader();
        CsvMapper mapper = new CsvMapper();
        MappingIterator<Dado> dados = mapper.readerFor(DadoCrawler.class).with(csvSchema).readValues(inputStream);
        return dados.readAll();
    }
}
