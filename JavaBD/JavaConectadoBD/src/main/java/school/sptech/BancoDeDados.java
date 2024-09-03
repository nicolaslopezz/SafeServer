package school.sptech;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.ResultSet;

public class BancoDeDados {
    public static void main(String[] args) {
        String urlBD = "jdbc:mysql://localhost:3306/registrar"; /* fazendo conexão local (possivel tbm remoto)
                                                                   depois de "3306/ coloque o nome do banco de dados (no meu caso, registrar)
                                                                */
        String nomeUsuario = "root";
        String senhaUsuario = "??"; // Coloque a senha do seu BD

        Connection conexao = null;
        Statement comando = null;

        try{
            conexao = DriverManager.getConnection(urlBD, nomeUsuario,senhaUsuario);
            System.out.println("Conectado com sucesso");

            comando = conexao.createStatement();

            String mySql = "select * from registroCPU"; // selecione de alguma tabela do seu BD
            ResultSet resultado = comando.executeQuery(mySql);

            while (resultado.next()){
                System.out.println("coluna1: " + resultado.getString("CpuID"));
                System.out.println("coluna2: " + resultado.getString("cpuPercent"));
            }
            resultado.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }   finally {
            try {
                if (comando != null) {
                    comando.close();
                }
                if (conexao != null) {
                    conexao.close();


                }
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

}
