package school.sptech;

import org.apache.commons.dbcp2.BasicDataSource;
import org.springframework.jdbc.core.JdbcTemplate;

public class DataBaseConfiguration {

    private JdbcTemplate template;

    public DataBaseConfiguration() {
        BasicDataSource dataSource = new BasicDataSource();
        dataSource.setDriverClassName("org.h2.Driver");
        dataSource.setUrl("jdbc:h2:file:./livro_teste");
        dataSource.setUsername("sa");
        dataSource.setPassword("");
        this.template = new JdbcTemplate(dataSource);
    }

    public JdbcTemplate getTemplate() {
        return template;
    }
}
