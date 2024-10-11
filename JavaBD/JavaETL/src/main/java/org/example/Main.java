package org.example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.S3Event;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.List;

public class Main implements RequestHandler<S3Event, String>{

        private final AmazonS3 s3Client = AmazonS3ClientBuilder.defaultClient();
        private static final String DESTINATION_BUCKET = "s3-safeserver-trusted";

        @Override
        public String handleRequest(S3Event s3Event, Context context) {

            String sourceBucket = s3Event.getRecords().get(0).getS3().getBucket().getName();
            String sourceKey = s3Event.getRecords().get(0).getS3().getObject().getKey();

            try {
                InputStream s3InputStrem = s3Client.getObject(sourceBucket, sourceKey).getObjectContent();

                Mapper mapper = new Mapper();
                List<Dado> dados = mapper.map(s3InputStrem);

                CsvWriter csvWriter = new CsvWriter();
                ByteArrayOutputStream csvOutputStream = csvWriter.writeCsv(dados);

                InputStream csvInputStream = new ByteArrayInputStream(csvOutputStream.toByteArray());

                s3Client.putObject(DESTINATION_BUCKET, sourceKey.replace(".json", ".csv"), csvInputStream, null);

                return "Sucesso no processamento!";
            } catch (Exception e){
                context.getLogger().log("Erro" + e.getMessage());
                return "Erro no processamento";
            }
        }
}