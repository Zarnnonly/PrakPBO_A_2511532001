package praktikumMinggu1;

public class Rekening {
    String nomorRekening;
    String namaPemilik;
    double saldo;

    public Rekening(String nomor, String nama, double saldoAwal) {
        nomorRekening = nomor;
        namaPemilik = nama;
        saldo = saldoAwal;
        System.out.println("Rekening atas nama " + namaPemilik + " berhasil dibuat dengan saldo Rp" + saldo);
    }

    public void setorTunai(double nominal) {
        if (nominal > 0) {
            saldo += nominal;
            System.out.println("Setor tunai Rp" + nominal + " berhasil. Saldo saat ini: Rp" + saldo);
        } else if (nominal < 10000) {
            System.out.println("Gagal: Nominal setor harus lebih dari Rp. 10.000!");
        } else {
            System.out.println("Gagal: Nominal setor harus lebih dari Rp. 10.000!");
        }
        
    }

    public void cekInformasi() {
        System.out.println("--- INFO REKENING ---");
        System.out.println("No. Rekening : " + nomorRekening);
        System.out.println("Nama Pemilik : " + namaPemilik);
        System.out.println("Saldo Akhir  : Rp" + saldo);
        System.out.println("--------------------");
    }
    
    public void tarikTunai(double nominal) {
    	if (nominal < 10000) {
    		System.out.println("Penarikan gagal! Minimal penarikan saldo adalah Rp10.000!");
    	} else if (saldo < nominal) {
    		System.out.println("Penarikan gagal! Saldo anda tidak mencukupi, saldo anda saat ini adalah Rp:" + saldo);
    	} else {
    		saldo = saldo - nominal;
    		System.out.println("Tarik tunai Rp" + nominal + " berhasil. Saldo saat ini: Rp" + saldo);
    	}
    }
}