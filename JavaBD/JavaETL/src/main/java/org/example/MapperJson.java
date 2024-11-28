package org.example;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

public class MapperJson implements Mapper {

    public List<Dado> map(InputStream inputStream) throws IOException {

        ObjectMapper mapper = new ObjectMapper();

        return mapper.readValue(inputStream, new TypeReference<List<Dado>>() {
        });
    }
}
