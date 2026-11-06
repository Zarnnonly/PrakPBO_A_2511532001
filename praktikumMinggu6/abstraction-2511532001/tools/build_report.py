"""Reproduce compiler evidence, build the report and package the local project."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import textwrap
import zipfile
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'laporan'
EVIDENCE = DOC / 'bukti'
EVIDENCE.mkdir(parents=True, exist_ok=True)

def run(args, expected=0):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if expected is not None and result.returncode != expected:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout + result.stderr

outputs = {}
for label, cls, args in [
    ('NimParams', 'tools.NimParams', ['2511532001']),
    ('SelfCheck', 'selfcheck.SelfCheck', []),
    ('TugasCheck', 'selfcheck.TugasCheck', []),
    ('TugasApp', 'shop.app.TugasApp', []),
    ('BadShop', 'review.BadShop', []),
    ('BadShopRefactored', 'review.fixed.BadShopRefactored', []),
]:
    outputs[label] = run(['java', '-cp', 'bin', cls, *args], 1 if label == 'BadShop' else 0)

with tempfile.TemporaryDirectory(prefix='abstraction-evidence-') as temp:
    base = Path(temp)
    probes = {
        'L1': 'class Probe { Object p = new shop.model.Product("X", "Uji", 1000); }',
        'L3': 'class Probe { void test() { new shop.service.CheckoutService().refund(new shop.payment.BankTransferPayment("Bank Nagari"), 1000); } }',
        'L4': 'class Probe extends shop.shipping.ShippingService { Probe() { super("Gratis"); } protected long ratePerKg() { return 0; } public long calculateCost(int grams) { return 0; } }',
    }
    for label, source in probes.items():
        probe = base / 'Probe.java'
        probe.write_text(source, encoding='utf-8')
        outputs[label] = run(['javac', '-cp', 'bin', '-d', str(base), str(probe)], 1)

    # These copies reproduce intermediate states without breaking the working project.
    for label in ['T1a', 'T1e']:
        copy = base / label
        shutil.copytree(ROOT / 'src', copy)
        payment = copy / 'shop/payment/PaymentMethod.java'
        card = copy / 'shop/payment/CreditCardPayment.java'
        if label == 'T1a':
            text = payment.read_text(encoding='utf-8')
            text = re.sub(r'default long adminFee\(long amount\)\s*\{\s*return 0;\s*\}', 'long adminFee(long amount);', text)
            payment.write_text(text, encoding='utf-8')
            for path in [card, copy / 'shop/payment/BankTransferPayment.java']:
                text = path.read_text(encoding='utf-8')
                text = re.sub(r'\s*@Override\s+public long adminFee\(long amount\)\s*\{[^}]*\}', '', text)
                path.write_text(text, encoding='utf-8')
            # Exclude later T2/T3 code to observe precisely the three methods and voucher from L3.
            sources = [p for p in copy.rglob('*.java') if 'notification' not in p.parts
                       and p.name != 'TugasApp.java' and 'fixed' not in p.parts]
        else:
            text = card.read_text(encoding='utf-8')
            text = re.sub(r'\s*@Override\s+public String policy\(\)\s*\{[^}]*\}', '', text)
            card.write_text(text, encoding='utf-8')
            sources = list(copy.rglob('*.java'))
        outputs[label] = run(['javac', '-encoding', 'UTF-8', '-d', str(base / ('out-' + label)), *map(str, sources)], 1)

for label, output in outputs.items():
    (EVIDENCE / (label + '.txt')).write_text(output, encoding='utf-8')

assert '10 / 10' in outputs['TugasCheck']
assert '23 / 23' in outputs['SelfCheck']
assert '4 errors' in outputs['T1a'], outputs['T1a']

# Images are explicitly labelled transcript renderings, not desktop screenshots.
font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 16)
for label, output in outputs.items():
    lines = [f'TRANSKRIP EKSEKUSI: {label} (render dari stdout/stderr)', '']
    for line in output.splitlines():
        lines.extend(textwrap.wrap(line, 112, replace_whitespace=False) or [''])
    im = Image.new('RGB', (1140, 40 + len(lines) * 23), '#101827')
    draw = ImageDraw.Draw(im)
    for i, line in enumerate(lines):
        draw.text((16, 14 + i * 23), line, font=font, fill='#e4edf7')
    im.save(EVIDENCE / (label + '.png'))

uml = '''@startuml
package shop.notification {
interface NotificationChannel {
  +channelName(): String
  +send(contact: CustomerContact, message: String): boolean
}
abstract class AbstractChannel {
  -sentCount: int
  -lastDelivered: String
  +send(contact: CustomerContact, message: String): boolean {leaf}
  #resolveRecipient(contact: CustomerContact): String {abstract}
  #deliver(recipient: String, message: String): boolean {abstract}
  #prepare(message: String): String
  +getSentCount(): int
  +getLastDelivered(): String
}
class CustomerContact <<final>> {
  -name: String {readOnly}
  -email: String {readOnly}
  -phone: String {readOnly}
  +getName(): String
  +getEmail(): String
  +getPhone(): String
}
class EmailChannel
class SmsChannel {
  -maxLength: int {readOnly}
  +SmsChannel(maxLength: int)
  #prepare(message: String): String
}
class WhatsAppChannel {
  #prepare(message: String): String
}
class NotificationService {
  -channels: List<NotificationChannel>
  +register(channel: NotificationChannel): void
  +broadcast(contact: CustomerContact, message: String): int
}
NotificationChannel <|.. AbstractChannel
AbstractChannel <|-- EmailChannel
AbstractChannel <|-- SmsChannel
AbstractChannel <|-- WhatsAppChannel
NotificationService o-- "0..*" NotificationChannel
NotificationChannel ..> CustomerContact
NotificationService ..> CustomerContact
}
@enduml
'''
(DOC / 'notification.puml').write_text(uml, encoding='utf-8')

# A vector UML diagram embedded in the PDF; PlantUML source is also included.
pdf = FPDF()
pdf.set_auto_page_break(True, margin=16)
pdf.add_font('Body', '', 'C:/Windows/Fonts/arial.ttf')
pdf.add_font('Body', 'B', 'C:/Windows/Fonts/arialbd.ttf')
pdf.set_font('Body', size=10)

def heading(text):
    pdf.set_font('Body', 'B', 14)
    pdf.multi_cell(0, 8, text, new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Body', size=10)

def para(text):
    pdf.multi_cell(0, 5.5, text, new_x='LMARGIN', new_y='NEXT')
    pdf.ln(2)

def table(headers, rows):
    with pdf.table(col_widths=tuple([1] * len(headers)), line_height=5,
                   first_row_as_headings=False, text_align='LEFT', padding=2) as tab:
        for row in [headers, *rows]:
            cells = tab.row()
            for cell in row:
                cells.cell(str(cell))
    pdf.ln(4)

pdf.add_page()
heading('Laporan Tugas Praktikum 6 — Abstraction')
para('Nama: Az Zahrand Solichul Tajussalathin\nNIM: 2511532001\nKelas: A\nTanggal: 6 November 2026')
heading('Parameter pribadi')
para(outputs['NimParams'])
para('Digit terakhir NIM = 1; dua digit terakhir = 01. Maka admin kartu = 1 + (1 mod 3) = 2%; biaya transfer = 2500 + 500 × (1 mod 5) = Rp3000; batas SMS = 100 + 1 = 101 karakter.')
heading('T1 — Evolusi API dan konflik default method')
para('T1.a menghasilkan 4 error untuk keadaan L3: EWalletPayment, BankTransferPayment, CreditCardPayment, dan anonymous class voucher di ShopApp. Method abstract yang baru menjadi kewajiban semua implementasi konkret. Anonymous class juga class implementasi, sehingga tetap wajib menyediakan adminFee(long). Percobaan dilakukan pada salinan source keadaan sebelum override biaya admin; proyek akhir tetap dapat dikompilasi.')
para('Default adminFee mengembalikan 0 sehingga implementasi lama tetap sah. Kartu kredit meng-override dengan persentase dari StudentInfo, transfer memakai biaya tetap, dan e-wallet mewarisi 0. Checkout membayar grandTotal: total produk dan ongkir ditambah biaya admin untuk total tersebut.')
para('EWalletPayment hanya mewarisi satu policy dari RefundablePayment, sehingga tidak mengalami konflik. CreditCardPayment mewarisi dua default policy dari interface yang tidak saling lebih spesifik. Java tidak dapat menebak kebijakan bisnis yang dimaksud; class harus memilih atau menggabungkannya secara eksplisit. Override menggunakan RefundablePayment.super.policy() + "; " + InstallmentPayment.super.policy().')
table(['Metode (Ekspres)', 'Total sebelum admin', 'Admin', 'Grand total'], [
    ['E-wallet', 'Rp268000', 'Rp0', 'Rp268000'],
    ['Transfer', 'Rp268000', 'Rp3000', 'Rp271000'],
    ['Kartu kredit', 'Rp268000', 'Rp5360', 'Rp273360']])
heading('T2 — Keputusan desain notifikasi')
para('Interface NotificationChannel menyatakan kemampuan mengirim. AbstractChannel menyimpan penghitung dan pesan terakhir serta menyediakan urutan pengiriman bersama. Keduanya dibutuhkan agar kanal biasa bisa memakai ulang algoritma, sementara kanal log sekali pakai tetap dapat mengimplementasikan kontrak langsung.')
para('send dibuat final agar subclass tidak melewati validasi, penyiapan pesan, atau pencatatan. Subclass hanya mengisi resolveRecipient dan deliver, serta boleh mengganti prepare. Jika send dapat di-override, kanal dapat melaporkan berhasil tanpa memperbarui penghitung atau mengirim pesan yang belum divalidasi.')
para('NotificationService menyimpan List<NotificationChannel> agar menerima seluruh implementasi kontrak, termasuk anonymous class log yang bukan AbstractChannel. Kanal baru cukup didaftarkan, tanpa mengubah broadcast. Pengiriman di tugas ini berupa simulasi cetak konsol, bukan akses layanan email/SMS/WhatsApp sungguhan.')

pdf.add_page()
heading('Diagram UML — shop.notification')
def box(x, y, w, title, members):
    h = 13 + len(members) * 5
    pdf.rect(x, y, w, h)
    pdf.set_font('Body', 'B', 9)
    pdf.set_xy(x + 2, y + 2)
    pdf.cell(w - 4, 5, title, align='C')
    pdf.line(x, y + 10, x + w, y + 10)
    pdf.set_font('Body', size=8)
    for i, line in enumerate(members):
        pdf.set_xy(x + 2, y + 12 + i * 5)
        pdf.cell(w - 4, 4, line)
    return (x + w / 2, y, y + h)

box(55, 30, 100, '«interface» NotificationChannel', ['+channelName(): String', '+send(CustomerContact, String): boolean'])
box(50, 80, 110, '«abstract» AbstractChannel', ['-sentCount: int; -lastDelivered: String', '+send(CustomerContact, String): boolean {final}', '#resolveRecipient(CustomerContact): String {abstract}', '#deliver(String, String): boolean {abstract}', '#prepare(String): String', '+getSentCount(): int; +getLastDelivered(): String'])
for x, title, fields in [(10, 'EmailChannel', ['+channelName()', '#resolveRecipient()', '#deliver()']),
                          (75, 'SmsChannel', ['-maxLength: int {final}', '+SmsChannel(int)', '#prepare(), #resolveRecipient()', '#deliver(), +channelName()']),
                          (140, 'WhatsAppChannel', ['#prepare(), #resolveRecipient()', '#deliver(), +channelName()'])]:
    box(x, 165, 60, title, fields)
    pdf.line(x + 30, 165, x + 30, 145)
    pdf.line(x + 30, 145, 105, 145)
pdf.line(105, 145, 105, 123)
pdf.polyline([(102, 127), (105, 123), (108, 127), (102, 127)])
pdf.set_dash_pattern(2, 1)
pdf.line(105, 80, 105, 53)
pdf.set_dash_pattern()
pdf.polyline([(102, 57), (105, 53), (108, 57), (102, 57)])
box(10, 225, 95, 'NotificationService', ['-channels: List<NotificationChannel>', '+register(NotificationChannel): void', '+broadcast(CustomerContact, String): int'])
box(115, 225, 85, '«final» CustomerContact', ['-name, -email, -phone: String {final}', '+CustomerContact(String, String, String)', '+getName(), +getEmail(), +getPhone()'])
pdf.line(10, 240, 5, 240)
pdf.line(5, 240, 5, 41)
pdf.line(5, 41, 55, 41)
pdf.polyline([(51, 39), (55, 41), (51, 43)])
pdf.set_font('Body', size=8)
pdf.set_xy(27, 35)
pdf.cell(20, 5, '0..*')
pdf.set_dash_pattern(2, 1)
pdf.line(105, 243, 115, 243)
pdf.set_dash_pattern()
pdf.polyline([(111, 241), (115, 243), (111, 245)])
pdf.set_xy(10, 207)
pdf.set_font('Body', size=9)
pdf.multi_cell(190, 5, 'Panah segitiga putus-putus: implements; segitiga penuh: extends.\nAsosiasi: NotificationService menyimpan 0..* NotificationChannel.\nDependency: channel dan service memakai CustomerContact pada parameter.')
pdf.add_page()
heading('T3 — Review BadShop')
table(['Lokasi', 'Masalah', 'Dampak nyata', 'Perbaikan'], [
    ['StoreOperations / GiftVoucher', 'Kontrak mencampur pembayaran, refund, pengiriman, struk.', 'ship/refund voucher melempar UnsupportedOperationException.', 'Voucher hanya implements PaymentMethod.'],
    ['Courier.cost', 'Switch String mengenali jenis kurir; typo EXPRES masuk default.', 'Ongkir 2 kg menjadi 0; kanal baru perlu ubah switch.', 'ShippingService dan ExpressShipping; rumus final.'],
    ['Courier / JneCourier', 'Abstract class tanpa variasi abstrak; subclass kosong.', 'Pewarisan tidak memberi perilaku kurir.', 'ratePerKg abstrak, calculateCost final.'],
    ['Address / SimpleOrder', 'Alamat mutable dibagi dua pesanan; final hanya referensi.', 'Mengubah ORD-2 ikut mengubah ORD-1.', 'Address final, field final, tanpa setter; alamat baru untuk ORD-2.'],
    ['Cart.Item', 'Inner class tanpa kebutuhan mengakses Cart.', 'Menyimpan referensi luar; konstruksi bergantung objek Cart.', 'Jadikan static nested; new Cart.Item(...).'],
    ['Discount.apply', 'Default method memakai instanceof class konkret.', 'Promo baru perlu edit interface; kontrak bergantung implementasi.', 'Discountable.discountPercent dan default applyDiscount.'],
    ['GiftVoucher.pay', 'Uang double; amount negatif tidak ditolak.', 'pay(-1000) justru menambah saldo; representasi uang tidak konsisten.', 'Saldo long; tolak amount <= 0 dan saldo kurang.'],
    ['Cart.Item / Cart.add', 'Tidak memvalidasi jumlah, harga, nama, null.', 'Subtotal negatif atau NullPointerException saat total.', 'Validasi constructor dan add sebelum menyimpan.']])
para('Refactor tersimpan terpisah pada src/review/fixed/BadShopRefactored.java. File BadShop.java asli tidak diubah. Versi refactor memakai ulang ShippingService, ExpressShipping, Discountable, dan PaymentMethod dari proyek. Semua gejala utama pada demo hilang.')
para(outputs['BadShopRefactored'])
heading('T4 — Refleksi pilihan desain')
table(['Kondisi', 'Pilihan', 'Alasan dan contoh proyek'], [
    ['Berbagi field dan constructor', 'Abstract class', 'Product memusatkan sku, name, price dan validasi constructor untuk produk fisik/digital.'],
    ['Beberapa kemampuan sekaligus', 'Interface', 'CreditCardPayment implements RefundablePayment dan InstallmentPayment.'],
    ['Rumus bersama tidak boleh diganti', 'Abstract class + final method', 'ShippingService.calculateCost final mengunci pembulatan; ratePerKg tetap abstrak.'],
    ['Kontrak berkembang', 'Interface + default method', 'PaymentMethod.adminFee default 0 menjaga implementasi lama tetap dapat dikompilasi.']])
table(['Kondisi', 'Pilihan', 'Alasan dan contoh proyek'], [
    ['Pembantu tanpa data objek luar', 'Static nested', 'Order.Line memakai product dan quantity sendiri; dapat dibuat tanpa Order.'],
    ['Perlu membaca field objek luar', 'Inner', 'Order.Receipt membaca Order.this.orderId dan shippingAddress.'],
    ['Implementasi sekali pakai', 'Anonymous', 'TugasApp mendaftarkan kanal log konsol melalui new NotificationChannel() { ... }.']])

explanations = {
    'L1': 'Product abstrak belum memberikan implementasi category(), sehingga tidak dapat diinstansiasi langsung.',
    'L3': 'Parameter refund harus RefundablePayment; BankTransferPayment hanya PaymentMethod sehingga ditolak pada waktu kompilasi.',
    'L4': 'calculateCost final tidak dapat di-override. Kurir mengubah ratePerKg, bukan rumus pembulatan bersama.',
    'T1a': 'Ada 4 error pada tiga metode pembayaran dan anonymous voucher. Semuanya belum menyediakan method abstract adminFee yang baru.',
    'T1e': 'CreditCardPayment mewarisi dua default policy yang tidak saling lebih spesifik. Override eksplisit diperlukan untuk menggabungkannya.',
}
pdf.add_page()
heading('Bukti eksekusi dan error compiler')
para('Lampiran berikut adalah gambar transkrip hasil stdout/stderr dari eksekusi sungguhan, bukan screenshot desktop. Untuk memenuhi format screenshot pada modul secara harfiah, ambil screenshot terminal sendiri memakai perintah di README_TUGAS.md. File teks mentah tersedia di laporan/bukti. Error direproduksi pada source sementara agar kode proyek akhir tetap dapat dikompilasi.')
for label in ['L1', 'L3', 'L4', 'T1a', 'T1e', 'NimParams', 'SelfCheck', 'TugasCheck', 'TugasApp']:
    pdf.add_page()
    heading(label)
    if label in explanations:
        para(explanations[label])
    path = EVIDENCE / (label + '.png')
    image = Image.open(path)
    width = 190
    height = width * image.height / image.width
    if height > 235:
        width *= 235 / height
    pdf.image(str(path), x=10, w=width)

pdf.output(str(DOC / 'Laporan_Tugas_2511532001.pdf'))
print('PDF dan bukti berhasil dibuat:', DOC)
