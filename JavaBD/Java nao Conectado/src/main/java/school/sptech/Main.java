package school.sptech;

import school.sptech.livroDao.DaoRegistro;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        DaoRegistro daoRegistro = new DaoRegistro();
        Scanner sc = new Scanner(System.in);

        System.out.println("| Registro SPTECH\n" +
                "| 1) Exibir Registros\n" +
                "| 2) Sair");


        Integer opcao = sc.nextInt();



        while (opcao != 2) {
            sc.nextInt();
            if (opcao == 1) {
                daoRegistro.printAllRegistros();
            }else if(opcao == 2){
                System.out.println("Saindo...");
                sc.close();
            }else if(opcao != (1) || opcao != 2){
                System.out.println("Opção inválida. Tente novamente.");

            }
            }
        }

    }

