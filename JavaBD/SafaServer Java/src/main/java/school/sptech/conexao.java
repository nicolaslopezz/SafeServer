package school.sptech;
import org.apache.commons.dbcp2.BasicDataSource;
import org.springframework.jdbc.core.JdbcTemplate;

public class conexao {
    private JdbcTemplate template;
    private BasicDataSource dataSource;

    public conexao() {


        BasicDataSource dataSource = new BasicDataSource();
        dataSource.setDriverClassName("com.mysql.cj.jdbc.Driver");
        // exemplo para MySQL: "com.mysql.cj.jdbc.Driver"
        dataSource.setUrl("jdbc:mysql://localhost:3306/SafeServer");
        // exemplo para MySQL: "jdbc:mysql://localhost:3306/meubanco"
        dataSource.setUsername("root");
        dataSource.setPassword("*********");
        this.template = new JdbcTemplate(dataSource);
    }
    public JdbcTemplate getTemplate() {
        return template;
    }
    public BasicDataSource getDataSource() {
        return dataSource;
    }
}





