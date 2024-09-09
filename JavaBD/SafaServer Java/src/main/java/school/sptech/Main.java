package school.sptech;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.BeanPropertyRowMapper;

import java.util.Scanner;


public class Main {
    public static void main(String[] args) {

        conexao conexao = new conexao();
        JdbcTemplate template = conexao.getTemplate();


        RegistroDao registroDao = new RegistroDao(template);

        Scanner opcao = new Scanner(System.in);
        System.out.println("Bem vindo, escolha uma opção");
        System.out.println("1- Monitorar ambos servidores");
        System.out.println("2- Monitorar um servidor específico");
        System.out.println("Digite sua opção:");
        Integer escolha = opcao.nextInt();

        if (escolha == 1) {
            registroDao.listarTodos();
        }
        else if (escolha == 2) {
            System.out.println("Escolha a maquina que deseja monitorar:");
            System.out.println("1- Máquina 1");
            System.out.println("2- Máquina 2");
            System.out.println("Escolha a máquina:");
            Integer escolha2 = opcao.nextInt();
            if (escolha2 == 1) {
                registroDao.listarMaquina1();
            } else if (escolha2 == 2){
                registroDao.listarMaquina2();
            }

        }


    }
}
