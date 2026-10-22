package praktikumMinggu1;

import java.util.Scanner;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {

        Scanner input = new Scanner(System.in);

        ArrayList<Rekening> daftarRekening = new ArrayList<>();
        Rekening akunAktif = null;

        boolean isRunning = true;

        while (isRunning) {

            System.out.println("\n=== SISTEM PERBANKAN MINI ===");
            System.out.println("1. Buka Rekening Baru");
            System.out.println("2. Setor Tunai");
            System.out.println("3. Tarik Tunai");
            System.out.println("4. Cek Informasi Rekening");
            System.out.println("5. Ganti Akun");
            System.out.println("6. Keluar");

            System.out.print("Pilih menu: ");
            int pilihan = input.nextInt();
            input.nextLine();

            switch (pilihan) {

                case 1:
                    System.out.print("Masukkan No Rekening: ");
                    String no = input.nextLine();

                    System.out.print("Masukkan Nama Pemilik: ");
                    String nama = input.nextLine();

                    System.out.print("Masukkan Saldo Awal: ");
                    double saldo = input.nextDouble();
                    input.nextLine();

                    Rekening rekeningBaru =
                        new Rekening(no, nama, saldo);

                    daftarRekening.add(rekeningBaru);
                    akunAktif = rekeningBaru;

                    break;

                case 2:
                    if (akunAktif == null) {
                        System.out.println("Belum ada akun aktif.");
                    } else {
                        System.out.print("Masukkan nominal setor: ");
                        double setor = input.nextDouble();
                        input.nextLine();

                        akunAktif.setorTunai(setor);
                    }
                    break;

                case 3:
                    if (akunAktif == null) {
                        System.out.println("Belum ada akun aktif.");
                    } else {
                        System.out.print("Masukkan nominal tarik: ");
                        double tarik = input.nextDouble();
                        input.nextLine();

                        akunAktif.tarikTunai(tarik);
                    }
                    break;

                case 4:
                    if (akunAktif == null) {
                        System.out.println("Belum ada akun aktif.");
                    } else {
                        akunAktif.cekInformasi();
                    }
                    break;

                case 5:
                    System.out.print("Masukkan nomor rekening: ");
                    String cariNomor = input.nextLine();

                    boolean ditemukan = false;

                    for (Rekening rekening : daftarRekening) {
                        if (rekening.nomorRekening.equals(cariNomor)) {
                            akunAktif = rekening;
                            ditemukan = true;
                            System.out.println("Akun berhasil diganti.");
                            break;
                        }
                    }

                    if (!ditemukan) {
                        System.out.println("Rekening tidak ditemukan.");
                    }

                    break;

                case 6:
                    isRunning = false;
                    System.out.println("Sistem ditutup.");
                    break;

                default:
                    System.out.println("Pilihan tidak valid.");
            }
        }

        input.close();
    }
}