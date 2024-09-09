package school.sptech;

import microsoft.sql.DateTimeOffset;
import org.apache.commons.dbcp2.BasicDataSource;
import org.springframework.jdbc.core.BeanPropertyRowMapper;
import org.springframework.jdbc.core.JdbcTemplate;

import java.sql.Date;
import java.sql.Time;

public class registro {
    private Integer idRegistro;
    private Time dtHora;
    private Date dtDia;
    private Float percent_use_cpu;
    private Float uso_ram_gb;
    private Float livre_ram_gb;
    private Float total_ram_gb;
    private Float uso_disco_gb;
    private Float livre_disco_gb;
    private Float total_disco_gb;
    private Integer fkServidor;

    public registro() {
    }

    public registro(Integer idRegistro, Time dtHora, Date dtDia, Float percent_use_cpu, Float uso_ram_gb, Float livre_ram_gb, Float total_ram_gb, Float uso_disco_gb, Float livre_disco_gb, Float total_disco_gb, Integer fkServidor) {
        this.idRegistro = idRegistro;
        this.dtHora = dtHora;
        this.dtDia = dtDia;
        this.percent_use_cpu = percent_use_cpu;
        this.uso_ram_gb = uso_ram_gb;
        this.livre_ram_gb = livre_ram_gb;
        this.total_ram_gb = total_ram_gb;
        this.uso_disco_gb = uso_disco_gb;
        this.livre_disco_gb = livre_disco_gb;
        this.total_disco_gb = total_disco_gb;
        this.fkServidor = fkServidor;
    }

    public Integer getIdRegistro() {
        return idRegistro;
    }

    public void setIdRegistro(Integer idRegistro) {
        this.idRegistro = idRegistro;
    }

    public Time getDtHora() {
        return dtHora;
    }

    public void setDtHora(Time dtHora) {
        this.dtHora = dtHora;
    }

    public Date getDtDia() {
        return dtDia;
    }

    public void setDtDia(Date dtDia) {
        this.dtDia = dtDia;
    }

    public Float getPercent_use_cpu() {
        return percent_use_cpu;
    }

    public void setPercent_use_cpu(Float percent_use_cpu) {
        this.percent_use_cpu = percent_use_cpu;
    }

    public Float getUso_ram_gb() {
        return uso_ram_gb;
    }

    public void setUso_ram_gb(Float uso_ram_gb) {
        this.uso_ram_gb = uso_ram_gb;
    }

    public Float getLivre_ram_gb() {
        return livre_ram_gb;
    }

    public void setLivre_ram_gb(Float livre_ram_gb) {
        this.livre_ram_gb = livre_ram_gb;
    }

    public Float getTotal_ram_gb() {
        return total_ram_gb;
    }

    public void setTotal_ram_gb(Float total_ram_gb) {
        this.total_ram_gb = total_ram_gb;
    }

    public Float getUso_disco_gb() {
        return uso_disco_gb;
    }

    public void setUso_disco_gb(Float uso_disco_gb) {
        this.uso_disco_gb = uso_disco_gb;
    }

    public Float getLivre_disco_gb() {
        return livre_disco_gb;
    }

    public void setLivre_disco_gb(Float livre_disco_gb) {
        this.livre_disco_gb = livre_disco_gb;
    }

    public Float getTotal_disco_gb() {
        return total_disco_gb;
    }

    public void setTotal_disco_gb(Float total_disco_gb) {
        this.total_disco_gb = total_disco_gb;
    }

    public Integer getFkServidor() {
        return fkServidor;
    }

    public void setFkServidor(Integer fkServidor) {
        this.fkServidor = fkServidor;
    }
}