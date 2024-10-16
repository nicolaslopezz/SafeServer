package org.example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.S3Event;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.ObjectMetadata;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.List;

public class Main implements RequestHandler<S3Event, String> {

    private final AmazonS3 s3Client = AmazonS3ClientBuilder.defaultClient();
    private static final String DESTINATION_BUCKET = "s3safeserver-trusted";

    @Override
    public String handleRequest(S3Event s3Event, Context context) {
        // Verifica se o evento contém registros
        if (s3Event.getRecords().isEmpty()) {
            context.getLogger().log("Evento S3 sem registros.");
            return "Erro no processamento: Evento S3 sem registros.";
        }

        // Obtém o nome do bucket e a chave do arquivo
        String sourceBucket = s3Event.getRecords().get(0).getS3().getBucket().getName();
        String sourceKey = s3Event.getRecords().get(0).getS3().getObject().getKey();
        context.getLogger().log("Source bucket: " + sourceBucket);
        context.getLogger().log("Source key: " + sourceKey);

        try {
            // Obtém o arquivo do bucket raw
            InputStream s3InputStream = s3Client.getObject(sourceBucket, sourceKey).getObjectContent();

            // Mapeia o conteúdo JSON para um objeto
            Mapper mapper = new Mapper();
            List<Dado> dados = mapper.map(s3InputStream);

            // Escreve os dados em formato CSV
            CsvWriter csvWriter = new CsvWriter();
            ByteArrayOutputStream csvOutputStream = csvWriter.writeCsv(dados);

            // Prepara o InputStream do CSV gerado
            InputStream csvInputStream = new ByteArrayInputStream(csvOutputStream.toByteArray());

            // Configura os metadados do arquivo CSV para o S3
            ObjectMetadata metadata = new ObjectMetadata();
            metadata.setContentType("text/csv");
            metadata.setContentLength(csvOutputStream.size());

            // Envia o arquivo CSV para o bucket "trusted"
            s3Client.putObject(DESTINATION_BUCKET, sourceKey.replace(".json", ".csv"), csvInputStream, metadata);

            return "Sucesso no processamento!!";
        } catch (Exception e) {
            context.getLogger().log("Erro: " + e.getMessage());
            return "Erro no processamento: " + e.getMessage();
        }
    }
}
