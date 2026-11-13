"""Rebuild week 6 report by cloning the supplied week 5 OOXML package."""
from pathlib import Path
from copy import deepcopy
import ast
import hashlib
import json
import re
import textwrap
import zipfile
from lxml import etree as E
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / 'laporan/qa_pekan6'
REF = Path('C:/Users/lenovo/Documents/Laporan Praktikum PBO Pekan 5.docx')
OUT = ROOT / 'laporan/Laporan_Praktikum_PBO_Pekan_6.docx'
QA.mkdir(exist_ok=True, parents=True)
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS = {'w': W, 'r': R}
def w(name): return '{' + W + '}' + name
def node(tag, **attrs):
    n = E.Element(w(tag))
    for key, val in attrs.items(): n.set(w(key), str(val))
    return n

with zipfile.ZipFile(REF) as z:
    parts = {name: z.read(name) for name in z.namelist()}
inventory = {k: {'bytes': len(v), 'sha256': hashlib.sha256(v).hexdigest()} for k,v in parts.items()}
(QA / 'package_inventory.json').write_text(json.dumps({'reference_sha256':hashlib.sha256(REF.read_bytes()).hexdigest(), 'parts':inventory}, indent=2))
doc = E.fromstring(parts['word/document.xml'])
body = doc.find(w('body'))
src = list(body)
for child in list(body): body.remove(child)

def p(text='', pattern=56, heading=False, page=False):
    result = E.Element(w('p'))
    pp = deepcopy(src[pattern].find(w('pPr')))
    if pp is None: pp = node('pPr')
    for s in pp.findall(w('sectPr')): pp.remove(s)
    if heading: pp.append(node('keepNext'))
    if page: pp.append(node('pageBreakBefore'))
    result.append(pp)
    rp = src[pattern].find('w:r/w:rPr', NS)
    for i, line in enumerate(str(text).split('\n')):
        run = node('r')
        if rp is not None: run.append(deepcopy(rp))
        if i: run.append(node('br'))
        for j, bit in enumerate(line.split('\t')):
            if j: run.append(node('tab'))
            t = node('t'); t.set('{http://www.w3.org/XML/1998/namespace}space','preserve'); t.text = bit; run.append(t)
        result.append(run)
    return result

toc_entries = []
def add(text, pattern=56, heading=False, page=False):
    x = p(text, pattern, heading, page); body.append(x); return x
def h(text, page=False):
    add(text,55,True,page); toc_entries.append((text, text))
def chapter(num,title):
    while len(body) and body[-1].tag==w('p') and not ''.join(t.text or '' for t in body[-1].iter(w('t'))) and body[-1].find('w:pPr/w:sectPr',NS) is None:
        body.remove(body[-1])
    add('BAB '+str(num),53,True,True); add(title,54,True)
    toc_entries.append(('BAB '+['','I','II','III','IV'][num]+' '+title,'BAB '+str(num)))
def para(text): add(text)
def code(text,compact=False):
    text = re.sub(r'[A-Za-z]:[^\n]*?abstraction-evidence-[^\\/\s]+[\\/]', '[folder sementara]/', text)
    # Keep exact results; shorten only temporary compiler file path prefixes.
    for line in text.splitlines():
        if compact and not line.strip(): continue
        for wrap in textwrap.wrap(line, width=73, replace_whitespace=False, drop_whitespace=False) or ['']:
            add(wrap,71)
    add('',56)

def table(headers, rows):
    total = 8271
    widths = {3:[2150,1800,4321],4:[1750,2100,2200,2221]}.get(len(headers),[total//len(headers)]*len(headers))
    t = node('tbl'); pr = node('tblPr'); pr.append(node('tblW',w=total,type='dxa'))
    borders = node('tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        borders.append(node(edge,val='single',sz=4,color='808080'))
    pr.append(borders); pr.append(node('tblLayout',type='fixed')); margins=node('tblCellMar')
    for edge in ['top','left','bottom','right']: margins.append(node(edge,w=80,type='dxa'))
    pr.append(margins); t.append(pr); grid=node('tblGrid')
    for width in widths: grid.append(node('gridCol',w=width))
    t.append(grid)
    for i,row in enumerate([headers,*rows]):
        tr=node('tr'); trpr=node('trPr'); trpr.append(node('cantSplit'))
        if i==0: trpr.append(node('tblHeader'))
        tr.append(trpr)
        for width, val in zip(widths,row):
            cell=node('tc'); cp=node('tcPr'); cp.append(node('tcW',w=width,type='dxa')); cp.append(node('vAlign',val='center')); cell.append(cp)
            par=p(val,55 if i==0 else 56)
            pp=par.find(w('pPr')); ind=pp.find(w('ind'))
            if ind is not None: pp.remove(ind)
            pp.append(node('ind',firstLine=0))
            jc=pp.find(w('jc')); jc.set(w('val'),'left')
            cell.append(par);tr.append(cell)
        t.append(tr)
    body.append(t); add('')

outputs={q.stem:q.read_text(encoding='utf-8') for q in (ROOT/'laporan/bukti').glob('*.txt')}
# Reuse the prior report content, rather than inventing external findings.
events=[]
tree=ast.parse((ROOT/'tools/build_report.py').read_text(encoding='utf-8'))
explanations={}
for n in tree.body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='explanations' for t in n.targets): explanations=ast.literal_eval(n.value)
    if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id in ['heading','para','table']:
        args=[eval(compile(ast.Expression(a),'<report>','eval'),{'__builtins__':{}},{'outputs':outputs}) for a in n.value.args]
        events.append((n.value.func.id,args))
def previous_section(prefix):
    active=False
    for kind,args in events:
        if kind=='heading':
            if active: break
            active=str(args[0]).startswith(prefix)
        elif active:
            if kind=='para' and args[0]==outputs['BadShopRefactored']:
                code(args[0])
            else:
                {'para':para,'table':table}[kind](*args)

# Cover is retained verbatim except week number.
for child in src[:20]: body.append(deepcopy(child))
for t in body[1].iter(w('t')):
    if t.text: t.text=t.text.replace('5','6')
add('DAFTAR ISI',20)
toc_start=len(body)
toc_place=node('p');body.append(toc_place)
add('KATA PENGANTAR',42,True,True)
for i in [43,44,45]: body.append(deepcopy(src[i]))
body.append(deepcopy(src[52]))

chapter(1,'PENDAHULUAN')
h('1.1 Latar Belakang')
para('Abstraction memisahkan kontrak yang digunakan oleh pemanggil dari rincian implementasinya. Pada proyek toko online, Product menjadi dasar produk fisik dan digital, sedangkan PaymentMethod dan Shippable menyatakan kemampuan pembayaran dan pengiriman. CheckoutService dapat memproses produk serta metode pembayaran melalui kontrak tersebut tanpa bergantung pada setiap class konkret.')
h('1.2 Tujuan Praktikum')
para('Praktikum ini bertujuan menerapkan abstract class, interface, default method, static method, private method, interface inheritance, final, dan nested class dalam Java. Tugas lanjutannya menerapkan evolusi API biaya admin, penyelesaian konflik default method, sistem notifikasi, serta review dan refactor desain BadShop.')
h('1.3 Manfaat Praktikum')
para('Penerapan kontrak memungkinkan penambahan kemampuan tanpa mengubah seluruh pemanggil. Rumus bersama dapat dipertahankan melalui final method, data alamat dibuat immutable, dan implementasi kanal baru dapat didaftarkan melalui NotificationChannel. Hasilnya dapat diperiksa melalui SelfCheck dan TugasCheck.')

chapter(2,'PEMBAHASAN')
h('2.1 Implementasi Latihan Abstraction')
para('Product adalah abstract class dengan data SKU, nama, dan harga. PhysicalProduct mengimplementasikan Shippable serta menolak berat kurang dari atau sama dengan nol. DigitalProduct mengimplementasikan Discountable dengan diskon 10 persen sehingga harga e-book Rp50000 menjadi Rp45000. Perhitungan subtotal menggunakan getFinalPrice() sehingga diskon dipanggil secara polimorfik.')
para('PaymentMethod menjadi kontrak getName() dan pay(long). EWalletPayment mengurangi saldo saat pembayaran berhasil. BankTransferPayment menyimulasikan pembayaran untuk nominal positif. CreditCardPayment mengimplementasikan RefundablePayment dan InstallmentPayment sekaligus. Cicilan memakai pembulatan ke atas dan dibatasi maksimal 12 bulan.')
para('ShippingService memusatkan rumus ongkir pada calculateCost() yang final; subclass hanya menentukan ratePerKg(). Berat 700 gram dibulatkan menjadi satu kilogram. Address adalah final class dengan field private final tanpa setter. Order.Line dibuat static nested, Order.Receipt dibuat inner untuk membaca data pesanan, dan voucher ShopApp menggunakan anonymous class.')
para('Keranjang contoh berisi kopi Rp85000, rendang Rp120000, dan e-book setelah diskon Rp45000. Subtotalnya Rp250000, berat kiriman 700 gram, total Reguler Rp260000, dan total Ekspres Rp268000 sebelum biaya admin.')
h('2.2 Pemeriksaan Latihan dan Error Compiler')
para('SelfCheck menghasilkan 23 dari 23 pemeriksaan lulus. Percobaan error dilakukan pada source sementara agar program akhir tetap dapat dikompilasi. Bukti berikut adalah transkrip eksekusi, bukan screenshot desktop.')
for label in ['L1','L3','L4']:
    add('Percobaan '+label,55,True); para(explanations[label]);code(outputs[label])
add('Hasil SelfCheck',55,True,True);code(outputs['SelfCheck'],compact=True)

chapter(3,'TUGAS')
h('3.1 Evolusi API dan Konflik Diamond')
add('Parameter Pribadi Berdasarkan NIM',55,True)
code(outputs['NimParams'])
para('NIM 2511532001 memiliki digit terakhir 1 dan dua digit terakhir 01. CARD_ADMIN_PERCENT = 2, TRANSFER_ADMIN_FEE = Rp3000, dan SMS_MAX_LENGTH = 101. Identitas dan ketiga konstanta disimpan pada StudentInfo.')
previous_section('T1 ')
for label in ['T1a','T1e']:
    add('Error Compiler '+label,55,True);para(explanations[label]);code(outputs[label])
h('3.2 Sistem Notifikasi Pesanan',True)
previous_section('T2 ')
para('CustomerContact merupakan final class; name wajib, sedangkan null pada email dan phone diubah menjadi string kosong. EmailChannel menerima alamat yang mengandung @. SmsChannel menerima nomor berawalan 08 dan memotong pesan menjadi tepat 101 karakter termasuk tiga titik. WhatsAppChannel menerima nomor 08 atau +62 dengan panjang minimal 10 serta menambahkan awalan [Toko UMKM].')
para('TugasApp mendaftarkan tiga kanal tersebut dan satu kanal log berupa anonymous class NotificationChannel. Pesan lebih dari 200 karakter dikirim kepada Siti Rahma yang memiliki email dan nomor 08 serta Budi yang hanya memiliki nomor +62. Hasilnya Siti menerima melalui empat kanal, sedangkan Budi menerima melalui dua kanal.')

# Draw the actual class diagram as a readable high-resolution technical figure.
scale=3
im=Image.new('RGB',(1500,1530),'white');draw=ImageDraw.Draw(im)
font=ImageFont.truetype('C:/Windows/Fonts/times.ttf',30)
bold=ImageFont.truetype('C:/Windows/Fonts/timesbd.ttf',30)
def box(x,y,width,title,lines):
    height=62+len(lines)*35; draw.rectangle((x,y,x+width,y+height),outline='black',width=3)
    draw.text((x+width/2,y+14),title,font=bold,fill='black',anchor='mt')
    draw.line((x,y+52,x+width,y+52),fill='black',width=2)
    for i,line in enumerate(lines): draw.text((x+12,y+64+i*35),line,font=font,fill='black')
    return y+height
box(330,30,840,'«interface» NotificationChannel',['+ channelName(): String','+ send(CustomerContact, String): boolean'])
box(250,285,1000,'«abstract» AbstractChannel',['- sentCount: int; - lastDelivered: String','+ send(CustomerContact, String): boolean {final}','# resolveRecipient(CustomerContact): String {abstract}','# deliver(String, String): boolean {abstract}','# prepare(String): String','+ getSentCount(): int; + getLastDelivered(): String'])
for y in range(180,280,16): draw.line((750,y,750,y+8),fill='black',width=3)
draw.polygon([(750,162),(735,185),(765,185)],fill='white',outline='black',width=3)
for x,title,lines in [(30,'EmailChannel',['+ channelName()','# resolveRecipient()','# deliver()']),(530,'SmsChannel',['- maxLength: int','+ SmsChannel(int)','# prepare(), # deliver()','# resolveRecipient()']),(1030,'WhatsAppChannel',['+ channelName()','# prepare(), # deliver()','# resolveRecipient()'])]:
    box(x,760,440,title,lines);draw.line((x+220,760,x+220,660,750,660),fill='black',width=3)
draw.line((750,660,750,640,750,570),fill='black',width=3)
draw.polygon([(750,560),(735,585),(765,585)],fill='white',outline='black',width=3)
box(30,1110,700,'NotificationService',['- channels: List<NotificationChannel>','+ register(NotificationChannel): void','+ broadcast(CustomerContact, String): int'])
box(800,1110,670,'«final» CustomerContact',['- name, email, phone: String {final}','+ CustomerContact(String, String, String)','+ getName(), getEmail(), getPhone()'])
draw.text((40,1400),'NotificationService o── 0..* NotificationChannel',font=font,fill='black')
draw.text((40,1440),'NotificationService dan NotificationChannel ..> CustomerContact',font=font,fill='black')
diagram=QA/'uml.png';im.save(diagram)
def image_par(rel_id,cx,cy):
    xml=f'''<w:p xmlns:w="{W}" xmlns:r="{R}" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="999" name="Diagram UML Notifikasi" descr="Relasi interface, abstract class, kanal, service dan kontak"/><wp:cNvGraphicFramePr/><a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic><pic:nvPicPr><pic:cNvPr id="0" name="notification.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'''
    return E.fromstring(xml.encode())
add('Diagram UML Sistem Notifikasi',55,True,True)
body.append(image_par('rIdNotificationUml',5252000,5357040))
para('Garis segitiga putus-putus menyatakan implements, sedangkan garis segitiga utuh menyatakan extends. NotificationService menyimpan nol atau lebih NotificationChannel; interface dan service memakai CustomerContact sebagai parameter. Sumber diagram yang dapat diedit tersedia pada notification.puml.')
add('Hasil TugasApp',55,True,True);code(outputs['TugasApp'])
add('Hasil TugasCheck',55,True,True);code(outputs['TugasCheck'])
h('3.3 Code Review dan Refactor BadShop',True)
previous_section('T3 ')
h('3.4 Refleksi Pilihan Desain',True)
previous_section('T4 ')

chapter(4,'KESIMPULAN')
h('4.1 Ringkasan Hasil Praktikum')
para('Abstraction pada proyek toko online diwujudkan melalui Product dan ShippingService sebagai abstract class serta PaymentMethod, Shippable, Discountable, dan NotificationChannel sebagai interface. Default method memungkinkan penambahan biaya admin tanpa mewajibkan seluruh implementasi lama diubah. Konflik dua default policy diselesaikan secara eksplisit pada CreditCardPayment.')
para('Algoritma pengiriman notifikasi dikunci melalui send() yang final dan dilengkapi hook untuk tiap kanal. Address menjaga data alamat melalui field private final tanpa setter. Refactor BadShop menghilangkan ongkir Ekspres nol, perubahan alamat pesanan lain, dan exception pengiriman voucher. Verifikasi yang sudah dijalankan menghasilkan SelfCheck 23/23 dan TugasCheck 10/10 pemeriksaan lulus.')
h('4.2 Link Github')
link=add('https://github.com/Zarnnonly/PrakPBO_A_2511532001',186)
link.find(w('pPr')).append(deepcopy(src[186].find('w:pPr/w:sectPr',NS)))
add('DAFTAR PUSTAKA',187,True)
add('[1] Program Studi S1 Informatika Universitas Andalas. Modul Praktikum OOP 6 – Abstraction. Bagian C–E, halaman 6–22.',188)
add('[2] Az Zahrand Solichul Tajussalathin. Kode sumber proyek abstraction-2511532001 dan hasil eksekusi SelfCheck, TugasCheck, serta TugasApp. NIM 2511532001.',188)
body.append(deepcopy(src[189]))

# Keep the source TOC tab leader and font. Word-pagination pass fills actual values.
toc=[('DAFTAR ISI','i'),('KATA PENGANTAR','ii'),*[(label,'1') for label,target in toc_entries],('DAFTAR PUSTAKA','iii')]
for offset,(label,page) in enumerate(toc):
    entry=p(label+'\t'+page,21);body.insert(toc_start+offset,entry)
body.remove(toc_place)
(QA/'toc_targets.json').write_text(json.dumps(toc_entries,ensure_ascii=False),encoding='utf-8')
parts['word/document.xml']=E.tostring(doc,xml_declaration=True,encoding='UTF-8',standalone=True)
rels=E.fromstring(parts['word/_rels/document.xml.rels'])
relationship=E.SubElement(rels,'{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
relationship.set('Id','rIdNotificationUml');relationship.set('Type',R+'/image');relationship.set('Target','media/notification.png')
parts['word/_rels/document.xml.rels']=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
parts['word/media/notification.png']=diagram.read_bytes()
ct=E.fromstring(parts['[Content_Types].xml'])
if not any(c.get('Extension')=='png' for c in ct):
    c=E.SubElement(ct,'{http://schemas.openxmlformats.org/package/2006/content-types}Default');c.set('Extension','png');c.set('ContentType','image/png')
parts['[Content_Types].xml']=E.tostring(ct,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED) as z:
    for name,data in parts.items(): z.writestr(name,data)
preserved=[name for name in inventory if name not in ['word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml']]
with zipfile.ZipFile(OUT) as z:
    assert all(hashlib.sha256(z.read(name)).hexdigest()==inventory[name]['sha256'] for name in preserved)
assert len(doc.findall('.//w:sectPr',NS))==4
print(OUT)
print('Preserved original package parts:',len(preserved))
