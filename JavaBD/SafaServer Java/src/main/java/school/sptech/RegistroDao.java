package school.sptech;

import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import java.util.List;

public class RegistroDao {


    private JdbcTemplate jdbcTemplate;

    // Construtor para injetar JdbcTemplate
    public RegistroDao(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }


    public List<registro> listarTodos() {
        String sqlSelect = "SELECT * FROM registro";
        List<registro> registros = jdbcTemplate.query(sqlSelect, new BeanPropertyRowMapper<>(registro.class));
        Integer captura = 1;
        for (registro registroDaVez : registros) {
            System.out.println(captura + "° Captura");
            System.out.println("Dados Base --> || Id da máquina = " + (registroDaVez.getFkServidor()) + " || Data: " + registroDaVez.getDtDia() + " || Hora: " + (registroDaVez.getDtHora()) + " || " );
            System.out.println("Dados CPU  --> || Porcentagem da CPU = %.1f" .formatted(registroDaVez.getPercent_use_cpu()) + "% ||");
            System.out.println("Dados Memória Ram -->  || Memória Total = %.1f "  .formatted(registroDaVez.getTotal_ram_gb()) + "GB" + " || Memória em Uso = %.1f "  .formatted(registroDaVez.getUso_ram_gb()) + "GB || Memória Livre = %.1f " .formatted(registroDaVez.getLivre_ram_gb()) + "GB ||");
            System.out.println("Dados Disco -->  || Disco Total = %.1f" .formatted(registroDaVez.getTotal_disco_gb()) + "GB" + " || Disco Ocupado = %.1f " .formatted(registroDaVez.getUso_disco_gb()) + "GB || Disco Livre = %.1f " .formatted(registroDaVez.getLivre_disco_gb()) + "GB ||");
            System.out.println("////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////");
            captura++;
        }

        return registros;
    }

    public List<registro> listarMaquina1() {
        String sqlSelect = "SELECT * FROM registro where fkServidor = 1";
        List<registro> registros = jdbcTemplate.query(sqlSelect, new BeanPropertyRowMapper<>(registro.class));
        Integer captura = 1;
        for (registro registroDaVez : registros) {
            System.out.println(captura + "° Captura");
            System.out.println("Dados Base --> || Id da máquina = " + (registroDaVez.getFkServidor()) + " || Data: " + registroDaVez.getDtDia() + " || Hora: " + (registroDaVez.getDtHora()) + " || " );
            System.out.println("Dados CPU  --> || Porcentagem da CPU = %.1f" .formatted(registroDaVez.getPercent_use_cpu()) + "% ||");
            System.out.println("Dados Memória Ram -->  || Memória Total = %.1f "  .formatted(registroDaVez.getTotal_ram_gb()) + "GB" + " || Memória em Uso = %.1f "  .formatted(registroDaVez.getUso_ram_gb()) + "GB || Memória Livre = %.1f " .formatted(registroDaVez.getLivre_ram_gb()) + "GB ||");
            System.out.println("Dados Disco -->  || Disco Total = %.1f" .formatted(registroDaVez.getTotal_disco_gb()) + "GB" + " || Disco Ocupado = %.1f " .formatted(registroDaVez.getUso_disco_gb()) + "GB || Disco Livre = %.1f " .formatted(registroDaVez.getLivre_disco_gb()) + "GB ||");
            System.out.println("////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////");
            captura++;
        }

        return registros;
    }

    public List<registro> listarMaquina2() {
        String sqlSelect = "SELECT * FROM registro where fkServidor = 2";
        List<registro> registros = jdbcTemplate.query(sqlSelect, new BeanPropertyRowMapper<>(registro.class));
        Integer captura = 1;
        for (registro registroDaVez : registros) {
            System.out.println(captura + "° Captura");
            System.out.println("Dados Base --> || Id da máquina = " + (registroDaVez.getFkServidor()) + " || Data: " + registroDaVez.getDtDia() + " || Hora: " + (registroDaVez.getDtHora()) + " || " );
            System.out.println("Dados CPU  --> || Porcentagem da CPU = %.1f" .formatted(registroDaVez.getPercent_use_cpu()) + "% ||");
            System.out.println("Dados Memória Ram -->  || Memória Total = %.1f "  .formatted(registroDaVez.getTotal_ram_gb()) + "GB" + " || Memória em Uso = %.1f "  .formatted(registroDaVez.getUso_ram_gb()) + "GB || Memória Livre = %.1f " .formatted(registroDaVez.getLivre_ram_gb()) + "GB ||");
            System.out.println("Dados Disco -->  || Disco Total = %.1f" .formatted(registroDaVez.getTotal_disco_gb()) + "GB" + " || Disco Ocupado = %.1f " .formatted(registroDaVez.getUso_disco_gb()) + "GB || Disco Livre = %.1f " .formatted(registroDaVez.getLivre_disco_gb()) + "GB ||");
            System.out.println("////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////");
            captura++;
        }

        return registros;
    }


}
