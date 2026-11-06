# Tugas Praktikum 6

Nama: Az Zahrand Solichul Tajussalathin  
NIM: 2511532001  
Kelas: A

## Menjalankan (PowerShell, JDK 17)

```powershell
$sources = @(Get-ChildItem src -Recurse -Filter *.java | ForEach-Object FullName)
javac -encoding UTF-8 -d bin $sources
java -cp bin tools.NimParams 2511532001
java -cp bin selfcheck.SelfCheck
java -cp bin selfcheck.TugasCheck
java -cp bin shop.app.TugasApp
java -cp bin review.fixed.BadShopRefactored
```

Hasil verifikasi: SelfCheck 23/23; TugasCheck 10/10.
Grand total Ekspres: e-wallet Rp268000, transfer Rp271000, kartu Rp273360.
SMS maksimum 101 karakter termasuk `...`. Siti menerima lewat 4 kanal, Budi 2.
Kanal notifikasi berupa simulasi konsol; tidak mengirim pesan ke layanan eksternal.

## Isi tugas

- T1: adminFee default, override biaya, grandTotal, dan penyelesaian diamond policy.
- T2: package `shop.notification`, demo `TugasApp`, UML `laporan/notification.puml` dan diagram pada PDF.
- T3: refactor terpisah di `src/review/fixed/BadShopRefactored.java`; file asli dipertahankan.
- T4 dan penjelasan error: `laporan/Laporan_Tugas_2511532001.pdf`.
- Bukti stdout/stderr mentah dan gambar transkrip: `laporan/bukti/`.

## Sebelum mengumpulkan

Gambar pada laporan adalah **render transkrip eksekusi**, bukan screenshot desktop.
Modul meminta screenshot: ambil screenshot terminal untuk NimParams, SelfCheck,
TugasCheck, TugasApp dan percobaan error L1/L3/L4/T1.a/T1.e, lalu tambahkan ke
laporan atau lampirkan bersama PDF. Error tersebut sudah direproduksi dan disimpan
di `laporan/bukti/`. T1.a menghasilkan 4 error; T1.e menghasilkan konflik default policy.

Laporan dapat dibuat ulang dengan `python tools/build_report.py` jika lingkungan
memiliki `fpdf2` dan `Pillow`. Script memakai salinan source di direktori sementara
untuk percobaan error sehingga proyek utama tetap dapat dikompilasi.

Nama dan kelas diambil dari nama arsip latihan dan folder repository; periksa
ejaannya sebelum mengumpulkan. Push GitHub dan unggah CODATA belum dilakukan.
Tujuan pada modul adalah `<YOUR_REPOSITORY>/Praktikum6/Tugas`; workspace saat ini
berada di `praktikumMinggu6/abstraction-2511532001` sehingga penempatan repository
perlu disesuaikan ketika mengunggah.
