from pathlib import Path
import sys,zipfile,copy
from lxml import etree as E
sys.path.insert(0,r'C:\Users\lenovo\.codex\skills\docx')
from scripts.document import Document
base=Path('output/lk-evidence')
doc=Document(base/'unpacked',author='Az Zahrand Solichul Tajussalathin',initials='AZ',rsid='B14A7416')
root=E.fromstring(doc['word/document.xml'].dom.toxml().encode())
ns={'w':root.nsmap['w']}; W='{'+ns['w']+'}'
tables=root.findall('.//w:body/w:tbl',ns)
def put(t,r,c,text):
 cell=tables[t].findall('w:tr',ns)[r].findall('w:tc',ns)[c]
 p=cell.find('w:p',ns); runs=p.findall('w:r',ns)
 proto=copy.deepcopy(runs[0]) if runs else E.Element(W+'r')
 for child in list(proto):
  if child.tag!=W+'rPr': proto.remove(child)
 for child in list(p):
  if child.tag!=W+'pPr': p.remove(child)
 # Retain all table/paragraph/run properties and use existing answer cell.
 for i,line in enumerate(text.split('\n')):
  run=copy.deepcopy(proto)
  if i: E.SubElement(run,W+'br')
  tx=E.SubElement(run,W+'t'); tx.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); tx.text=line
  p.append(run)
 for extra in cell.findall('w:p',ns)[1:]:
  # Existing answer cells have one paragraph; do not alter structure.
  pass
def one(t,text): put(t,0,0,text)
def evidence(name): return (base/name).read_text(encoding='utf-8-sig').strip()
vals=['Az Zahrand Solichul Tajussalathin','2511532001','BELUM DIISI - konfirmasi kelas praktikum.','BELUM DIISI - isi tanggal pelaksanaan praktikum.','openjdk version "24.0.2" 2025-07-15\nCatatan: pengujian memakai Java 24 dengan --enable-preview; syarat modul Java 25 belum terpenuhi.','Rp200000','3','1']
for i,v in enumerate(vals,1):put(0,i,1,v)
for col,vals in [(1,['NumberFormatException','Unchecked','For input string: "dua"','CrashDemo.java:28, readQuantity','CrashDemo.java:43, main','Teks "dua" dikonversi dengan Integer.parseInt, sehingga gagal dibaca sebagai bilangan bulat.']),(2,['NullPointerException','Unchecked','Cannot invoke "shop.model.Address.getCity()" because the return value of "shop.demo.CrashDemo$Customer.getAddress()" is null','CrashDemo.java:32, shippingCity','CrashDemo.java:44, main','Alamat Customer belum diisi. getAddress() mengembalikan null, lalu kode memanggil getCity() pada nilai tersebut.'])]:
 for row,v in enumerate(vals,1):put(1,row,col,v)
one(2,'Jawaban: Jumlah -2 berhasil dibaca sebagai int. Perulangan penambahan barang langsung dilewati karena i = 0 tidak memenuhi i < -2, sehingga keranjang tidak bertambah. NumberFormatException tidak muncul karena format -2 sah; aturan jumlah positif harus diperiksa tersendiri dengan if.')
one(3,'Jawaban: Setelah teks berhasil dibaca sebagai int, batas nomor produk dapat diperiksa dengan if sebelum catalog.get dipanggil. Teks seperti abc gagal saat Integer.parseInt dijalankan, sehingga NumberFormatException ditangkap agar pengguna bisa mengisi ulang.')
outs=['A1 mulai\nA2 jumlah = 12\nA4 finally\nA5 lanjut\nA1 mulai\nA3 bukan angka\nA4 finally\nA5 lanjut','B1 bulan = 3\nB2 cicilan = 100000\nB4 finally\nB5 hasil = 100000\nB1 bulan = 0\nB4 finally\nB7 main menangkap: / by zero','C1 cek stok\nC2 finally\nC3 sisa = 4']
exps=['Input 12 berhasil dikonversi; 12rb masuk catch. finally dan baris sesudahnya tetap dijalankan pada kedua pemanggilan.','Pembagian dengan nol melempar ArithmeticException, yang ditangkap di main sesudah finally partB. Baris B6 dan pencetakan B5 kedua dilewati.','Nilai return 4 dihitung di try, lalu finally dicetak sebelum nilai itu diterima main.']
for r,(out,exp) in enumerate(zip(outs,exps),1):
 put(4,r,1,'BELUM DIISI - prediksi sebelum run belum tercatat.');put(4,r,2,out);put(4,r,3,'BELUM DIISI - cocokkan prediksi pribadi.');put(4,r,4,exp)
ds=['D1 SKU: RDG-002\nD5 pencarian selesai','D2 nomor harus bilangan bulat\nD5 pencarian selesai','D3 nomor di luar katalog: Index 7 out of bounds for length 3\nD5 pencarian selesai','D4 Berikan satu nomor produk.\nD5 pencarian selesai']
de=['Tidak masuk catch; indeks 1 valid. finally tetap dijalankan.','catch NumberFormatException menangkap kegagalan parse abc.','catch ArrayIndexOutOfBoundsException menangkap akses indeks 7 pada array berukuran 3.','catch IllegalArgumentException menangkap exception yang dilempar saat args kosong.']
for r in range(1,5):
 put(5,r,1,'BELUM DIISI - prediksi awal belum tercatat.');put(5,r,2,ds[r-1]);put(5,r,3,de[r-1])
one(6,'Pesan error:\n'+evidence('catch-error.txt'))
one(7,'Artinya: NumberFormatException adalah turunan IllegalArgumentException, sehingga catch induk di atas sudah menangkapnya dan catch khusus di bawah tidak dapat dicapai.')
one(8,'Jumlah error: BELUM DIISI. File: BELUM DIISI.\nCatatan: kondisi tepat sesudah interface diubah belum direkam. Isi dari catatan atau hasil kompilasi pada tahap L3.c, jangan memakai jumlah perkiraan modul.')
one(9,'Alasan: Semua implementasi PaymentMethod harus mengikuti tipe hasil dan deklarasi exception yang baru. Pemanggil pay juga harus menyesuaikan penggunaan nilai hasil serta menangkap atau meneruskan checked exception PaymentFailedException.')
results=['[SALDO]','[BAYAR]','[STOK]','[SALDO]','[INVALID]','[OK]']
for r,res in enumerate(results,1):
 put(10,r,1,'BELUM DIISI - prediksi awal.');put(10,r,2,'BELUM DIISI - prediksi stok/saldo.');put(10,r,3,res);put(10,r,4,'3 / 1 / '+('3 / Rp120000' if r==6 else '5 / Rp200000'));put(10,r,5,'BELUM DIISI - cocokkan prediksi.')
one(11,'Jawaban: Pada S3, Rendang pertama berhasil dipesan sehingga stok sementara menjadi 0. Pemesanan Rendang kedua gagal dan seluruh stok yang sudah dipesan dikembalikan, sehingga stok akhirnya tetap 1. Pesan menyebut "diminta 1" karena checkout memanggil reserve(sku, 1) untuk setiap barang di keranjang.')
one(12,'Jawaban: Checkout mengembalikan barang yang sudah dipesan agar transaksi gagal tidak mengurangi stok. throw e meneruskan jenis exception dan datanya ke ShopApp.buy, tempat pesan pembeli dibuat. Jika release dihapus, stok yang sempat dipesan tetap berkurang meskipun pembayaran atau pemesanan berikutnya gagal.')
one(13,'Jawaban: InsufficientBalanceException adalah turunan PaymentFailedException, sehingga catch khusus saldo harus lebih dulu. Jika ditukar, compiler menolak catch InsufficientBalanceException karena exception itu sudah ditangkap oleh catch PaymentFailedException.')
for r,vals in enumerate([['3','KUE-003;Kue Lapis Legit;95rb;800','Harga 95rb gagal dibaca sebagai long.','NumberFormatException (ditangkap catch IllegalArgumentException)'],['5','BATIK-005;Kain Batik Tulis','Hanya ada 2 field; diperlukan 4 field.','IllegalArgumentException'],['6','SAMB-006;Sambal Lado Mudo 200g;-45000;250','Harga negatif ditolak oleh konstruktor produk.','IllegalArgumentException']],1):
 for c,v in enumerate(vals):put(14,r,c,v)
one(15,'Output:\n'+evidence('missing.txt'))
one(16,'Jawaban: e.getMessage() berisi "Katalog gagal dibaca: katalog-cadangan.csv". e.getCause() adalah java.nio.file.NoSuchFileException: katalog-cadangan.csv. Jika hanya cause.getMessage() dicetak, pengguna hanya melihat nama file tanpa keterangan bahwa katalog gagal dibaca.')
reviews=[['Kegagalan pembayaran ditangkap oleh catch kosong.','Pemanggil mengira pembayaran selesai meskipun saldo kurang.','Hapus catch kosong, deklarasikan throws PaymentFailedException, lalu tangani kegagalan di main.'],['Pengecekan ketersediaan memakai reserve dan release.','Pengecekan memiliki efek samping sementara pada stok dan memakai exception untuk kondisi ya/tidak.','Periksa inventory.available(sku) > 0.'],['Cause diganti null saat IOException dibungkus.','Penyebab kegagalan file hilang dari rantai exception.','Teruskan e ke new CatalogLoadException(message, e).'],['Kesalahan input dan stok habis digabung dalam satu multi-catch.','Pembeli menerima pesan teknis dan sulit membedakan input keliru dari stok kurang.','Tangani NumberFormatException secara khusus, validasi jumlah positif, lalu tangani OutOfStockException dengan pesan stok.']]
for r,vs in enumerate(reviews,1):
 for c,v in enumerate(vs,1):put(17,r,c,v)
one(18,'Output:\n'+evidence('review.FragileShop.txt'))
line=next(x for x in evidence('selfcheck.SelfCheck.txt').splitlines() if x.startswith('=== HASIL:'))
one(19,line+'\nCatatan: L0.1 gagal karena runtime Java 24. Jalankan ulang dengan JDK 25 untuk hasil akhir sesuai modul.')
one(20,'BELUM DIISI - baris === TANTANGAN tidak dicetak karena bagian bonus di SelfCheck masih dikomentari. Jangan mengarang hasil bonus.')
one(21,'Jawaban: Kesalahan ketik dapat diperbaiki dengan meminta input ulang setelah NumberFormatException ditangkap. Exception ini unchecked karena berasal dari konversi teks. Stok habis adalah kegagalan bisnis yang dilaporkan lewat checked exception OutOfStockException, sehingga pemanggil reserve wajib menangkap atau meneruskannya.')
one(22,'Jawaban: Pesan teknis perlu diubah ke bahasa yang dipahami pembeli. Saat jumlah diisi dua, aplikasi dapat mencetak "Input harus berupa angka." dan meminta input ulang. Detail For input string: "dua" lebih berguna untuk pemeriksaan kode.')
one(23,'BELUM DIISI - tulis satu hal yang masih membingungkan atau ingin ditanyakan berdasarkan pengalaman sendiri.')
# Only document.xml changes; all original package parts, styles and layout remain byte-for-byte.
src=base/'template/LK-P07.docx'; out=Path('output/LK-P07-2511532001.docx')
with zipfile.ZipFile(src) as z,zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as dest:
 for info in z.infolist():dest.writestr(info,E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True) if info.filename=='word/document.xml' else z.read(info.filename))
print(out.resolve())
