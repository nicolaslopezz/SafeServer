package school.sptech.entity;

import java.time.LocalDateTime;

public class Registro {
    private int idRegistro;
    private LocalDateTime dataHora;
    private Float percentUseCpu;
    private Long usoRamGb;
    private Long livreRamGb;
    private Long totalRamGb;
    private Long usoDiscoGb;
    private Long livreDiscoGb;
    private Long totalDiscoGb;
    private Integer totalNucleosCpu;
    private Integer fkServidor;

    public int getIdRegistro() {
        return idRegistro;
    }

    public void setIdRegistro(int idRegistro) {
        this.idRegistro = idRegistro;
    }

    public LocalDateTime getDataHora() {
        return dataHora;
    }

    public void setDataHora(LocalDateTime dataHora) {
        this.dataHora = dataHora;
    }

    public Float getPercentUseCpu() {
        return percentUseCpu;
    }

    public void setPercentUseCpu(Float percentUseCpu) {
        this.percentUseCpu = percentUseCpu;
    }

    public Long getUsoRamGb() {
        return usoRamGb;
    }

    public void setUsoRamGb(Long usoRamGb) {
        this.usoRamGb = usoRamGb;
    }

    public Long getLivreRamGb() {
        return livreRamGb;
    }

    public void setLivreRamGb(Long livreRamGb) {
        this.livreRamGb = livreRamGb;
    }

    public Long getTotalRamGb() {
        return totalRamGb;
    }

    public void setTotalRamGb(Long totalRamGb) {
        this.totalRamGb = totalRamGb;
    }

    public Long getUsoDiscoGb() {
        return usoDiscoGb;
    }

    public void setUsoDiscoGb(Long usoDiscoGb) {
        this.usoDiscoGb = usoDiscoGb;
    }

    public Long getLivreDiscoGb() {
        return livreDiscoGb;
    }

    public void setLivreDiscoGb(Long livreDiscoGb) {
        this.livreDiscoGb = livreDiscoGb;
    }

    public Long getTotalDiscoGb() {
        return totalDiscoGb;
    }

    public void setTotalDiscoGb(Long totalDiscoGb) {
        this.totalDiscoGb = totalDiscoGb;
    }

    public Integer getTotalNucleosCpu() {
        return totalNucleosCpu;
    }

    public void setTotalNucleosCpu(Integer totalNucleosCpu) {
        this.totalNucleosCpu = totalNucleosCpu;
    }

    public Integer getFkServidor() {
        return fkServidor;
    }

    public void setFkServidor(Integer fkServidor) {
        this.fkServidor = fkServidor;
    }
}
