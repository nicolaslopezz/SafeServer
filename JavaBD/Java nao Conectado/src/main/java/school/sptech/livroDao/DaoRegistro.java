package school.sptech.livroDao;

import org.springframework.jdbc.core.JdbcTemplate;
import school.sptech.DataBaseConfiguration;
import school.sptech.entity.Registro;

import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

public class DaoRegistro {

    DataBaseConfiguration databaseConfiguration = new DataBaseConfiguration();
    public JdbcTemplate template = databaseConfiguration.getTemplate();


    public List<Registro> listarRegistros() {
        // Selecionando todos os dados da tabela registro
        String sql = "SELECT * FROM registro";

        //Criando lista para armazenar os objetos resgatados do banco.
        List<Registro> registros = new ArrayList<>();


        // Fazendo uma "query" com o "template" para definir o tipo de dado de cada coluna da tabela que será
        // armazenado na Lista criada anteriormente.
        /*
         O que é "template"? Template é a variável que foi definida dentro da classe "DataBaseConfiguration"
         para executar os métodos do java sobre os dados resgatados na conexão entre SQL e Java.
         */
        template.query(sql, (ResultSet rs) -> {
            while (rs.next()) {
                Registro registro = new Registro();
                registro.setIdRegistro(rs.getInt("idRegistro"));
                registro.setDataHora(rs.getTimestamp("dataHora").toLocalDateTime());
                registro.setPercentUseCpu(rs.getFloat("percent_use_cpu"));
                registro.setUsoRamGb(rs.getLong("uso_ram_gb"));
                registro.setLivreRamGb(rs.getLong("livre_ram_gb"));
                registro.setTotalRamGb(rs.getLong("total_ram_gb"));
                registro.setUsoDiscoGb(rs.getLong("uso_disco_gb"));
                registro.setLivreDiscoGb(rs.getLong("livre_disco_gb"));
                registro.setTotalDiscoGb(rs.getLong("total_disco_gb"));
                registro.setTotalNucleosCpu(rs.getInt("toltal_nucleos_cpu"));
                registro.setFkServidor(rs.getInt("fkServidor"));
                registros.add(registro);
            }
            return null;
        });

        return registros;
    }

    // Função de exibir os registros de forma formatada para o Java.
    public void printAllRegistros() {
        List<Registro> registros = listarRegistros();

        for (Registro registro : registros) {
            System.out.println("ID: = %s ".formatted(registro.getIdRegistro()));
            System.out.println("DataHora = %s ".formatted(registro.getDataHora()) );
            System.out.println("PercentUseCpu = ".formatted(registro.getPercentUseCpu()) );
            System.out.println("UsoRamGb = ".formatted(registro.getUsoRamGb()));
            System.out.println("LivreRamGb = ".formatted(registro.getLivreRamGb()));
            System.out.println("TotalRamGb = ".formatted(registro.getTotalRamGb()) );
            System.out.println("UsoDiscoGb = ".formatted(registro.getUsoDiscoGb()) );
            System.out.println("LivreDiscoGb = ".formatted(registro.getLivreDiscoGb()));
            System.out.println("TotalDiscoGb = ".formatted(registro.getTotalDiscoGb()));
            System.out.println("TotalNucleosCpu = ".formatted(registro.getTotalNucleosCpu()));
            System.out.println("FkServidor = ".formatted(registro.getFkServidor()));
            System.out.println();
        }
    }
}
