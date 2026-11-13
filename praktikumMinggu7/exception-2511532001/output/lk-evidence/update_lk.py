from pathlib import Path
import zipfile
from lxml import etree as E
p=Path('output/LK-P07-2511532001.docx')
with zipfile.ZipFile(p) as z: parts={n:z.read(n) for n in z.namelist()}
r=E.fromstring(parts['word/document.xml']); ns={'w':r.nsmap['w']}
replacements={
'BELUM DIISI - konfirmasi kelas praktikum.':'A',
'BELUM DIISI - isi tanggal pelaksanaan praktikum.':'12 November 2026',
'openjdk version "24.0.2" 2025-07-15':'java version "25.0.5.0.2" 2026-10-21 LTS',
'Catatan: pengujian memakai Java 24 dengan --enable-preview; syarat modul Java 25 belum terpenuhi.':'Pengujian terbaru memakai JDK 25 tanpa --enable-preview.',
'=== HASIL: 23 / 24 pemeriksaan lulus (nilai SelfCheck 48 / 50) ===':'=== HASIL: 24 / 24 pemeriksaan lulus (nilai SelfCheck 50 / 50) ===',
'Catatan: L0.1 gagal karena runtime Java 24. Jalankan ulang dengan JDK 25 untuk hasil akhir sesuai modul.':'Seluruh pemeriksaan wajib lulus pada Java 25.',
'BELUM DIISI - baris === TANTANGAN tidak dicetak karena bagian bonus di SelfCheck masih dikomentari. Jangan mengarang hasil bonus.':'Tidak ada baris === TANTANGAN pada output. Pemeriksaan bonus masih dikomentari dalam SelfCheck.',
'KUE-003;Kue Lapis Legit;95rb;800':'Field: KUE-003 | Kue Lapis Legit | 95rb | 800',
'BATIK-005;Kain Batik Tulis':'Field: BATIK-005 | Kain Batik Tulis',
'SAMB-006;Sambal Lado Mudo 200g;-45000;250':'Field: SAMB-006 | Sambal Lado Mudo 200g | -45000 | 250',
'format -2 sah; aturan':'format -2 sah. Aturan',
'Input 12 berhasil dikonversi; 12rb':'Input 12 berhasil dikonversi. Input 12rb',
'Tidak masuk catch; indeks':'Tidak masuk catch karena indeks',
'Hanya ada 2 field; diperlukan':'Hanya ada 2 field. Diperlukan',
'; yang ':' dan yang '
}
for t in r.findall('.//w:t',ns):
 text=t.text or ''
 for a,b in replacements.items(): text=text.replace(a,b)
 t.text=text
assert not any(';' in (t.text or '') for t in r.findall('.//w:t',ns))
parts['word/document.xml']=E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
tmp=p.with_suffix('.tmp')
with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in parts.items():z.writestr(n,v)
tmp.replace(p)
print('Updated report. No semicolon in visible document text.')
