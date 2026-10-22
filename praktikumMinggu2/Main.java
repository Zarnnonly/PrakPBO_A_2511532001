package praktikumMinggu1;

import java.util.Scanner;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        ArrayList<Rekening> daftarRekening = new ArrayList<>();
        Rekening akunAktif = null; 
        
        boolean isRunning = true;

        System.out.println("========== SISTEM PERBANKAN MINI ==========");

        while (isRunning) {
            System.out.println("\nMenu Utama:");
            System.out.println("1. Buka Rekening Baru");
            System.out.println("2. Setor Tunai");
            System.out.println("3. Tarik Tunai");
            System.out.println("4. Cek Informasi Rekening");
            System.out.println("5. Ganti Akun"); 
            System.out.println("6. Cetak Mutasi"); // Tambahan menu Tugas 2
            System.out.println("7. Cetak 3 Terbaru");
            System.out.println("0. Keluar");
            System.out.print("Pilih menu: ");
            int pilihan = input.nextInt();
            input.nextLine(); // Membersihkan buffer enter

            switch (pilihan) {
                case 1:
                    System.out.print("Masukkan No Rekening: ");
                    String no = input.nextLine();
                    System.out.print("Masukkan Nama Pemilik: ");
                    String nama = input.nextLine();
                    System.out.print("Masukkan Saldo Awal: ");
                    double saldo = input.nextDouble();
                    
                    Rekening akunBaru = new Rekening(no, nama, saldo);
                    daftarRekening.add(akunBaru);
                    akunAktif = akunBaru;
                    break;
                case 2:
                    if (akunAktif == null) {
                        System.out.println("Error: Mohon maaf, Anda belum memiliki nomor rekening aktif!");
                    } else {
                        System.out.print("Masukkan nominal setor: ");
                        double setor = input.nextDouble();
                        akunAktif.setorTunai(setor); 
                    }
                    break;
                case 3:
                    if (akunAktif == null) {
                        System.out.println("Error: Mohon maaf, Anda belum memiliki nomor rekening aktif!");
                    } else {
                        System.out.print("Masukkan nominal tarik tunai: ");
                        double tarik = input.nextDouble();
                        akunAktif.tarikTunai(tarik);
                    }
                    break;
                case 4:
                    if (akunAktif == null) {
                        System.out.println("Error: Anda belum membuka rekening!");
                    } else {
                        akunAktif.cekInformasi();
                    }
                    break;
                case 5:
                    if (daftarRekening.isEmpty()) {
                        System.out.println("Error: Belum ada rekening yang terdaftar di sistem!");
                    } else {
                        System.out.print("Masukkan No Rekening yang ingin diakses: ");
                        String noCari = input.nextLine();
                        boolean ditemukan = false;
                        
                        for (Rekening rek : daftarRekening) {
                            if (rek.nomorRekening.equals(noCari)) {
                                akunAktif = rek;
                                ditemukan = true;
                                System.out.println("Berhasil ganti akun ke: " + akunAktif.namaPemilik);
                                break;
                            }
                        }
                        
                        if (!ditemukan) {
                            System.out.println("Error: Rekening tidak ditemukan!");
                        }
                    }
                    break;
                case 6:
                    // Tugas 2, Pemanggilan method cetakMutasi()
                    if (akunAktif == null) {
                        System.out.println("Error: Anda belum membuka rekening!");
                    } else {
                        akunAktif.cetakMutasi(); // memanggil fungsi dari class Rekening
                    }
                    break;
                case 7:
                    // Challenge 3
                    if (akunAktif == null) {
                        System.out.println("Error: Anda belum membuka rekening!");
                    } else {
                        akunAktif.cetakTigaTerbaru(); 
                    }
                    break;
                case 0:
                    isRunning = false;
                    System.out.println("Sistem ditutup. Terima kasih!");
                    break;
                default:
                    System.out.println("Pilihan tidak valid!");
            }
        }
        input.close();
    }
}