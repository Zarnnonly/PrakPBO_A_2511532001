package praktikumMinggu1;

public class RekeningTabungan extends Rekening {
	
	// atribut spesifik tabungan
	private double sukuBunga;
	
	// constructor subclass
	public RekeningTabungan(String nomor, String nama, double saldoAwal, String pinAwal, double sukuBunga) {
		//super() memanggil constructor rekening
		super(nomor, nama, saldoAwal, pinAwal);
		this.sukuBunga = sukuBunga;
	}
	
	public void tambahBungaAkhirBulan() {
		// Menghitung bunga
		double nominalBunga = saldo * (sukuBunga / 100);
		saldo += nominalBunga;
		
		// Mencatat riwayat transaksi
		String idTrx = "TRX-B-" + System.currentTimeMillis();
		riwayatTransaksi.add(new Transaksi(idTrx, "Bunga", nominalBunga));
		
		System.out.println("Bunga " + sukuBunga + "% berhasil ditambahkan: Rp" + nominalBunga);;
	}
	

}
