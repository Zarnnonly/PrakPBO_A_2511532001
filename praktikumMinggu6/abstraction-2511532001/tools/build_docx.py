"""Build an editable Word report from the same content as the PDF (stdlib only)."""
import ast
from pathlib import Path
import re
import zipfile
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'laporan'
outputs = {p.stem: p.read_text(encoding='utf-8') for p in (DOC / 'bukti').glob('*.txt')}
blocks = []

def paragraph(text, style=None):
    props = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
    runs = '<w:br/>'.join('<w:t xml:space="preserve">' + escape(line) + '</w:t>'
                         for line in str(text).split('\n'))
    return f'<w:p>{props}<w:r>{runs}</w:r></w:p>'

def heading(text):
    blocks.append(paragraph(text, 'Heading1'))

def para(text):
    blocks.append(paragraph(text))

def table(headers, rows):
    width = 9900 // len(headers)
    xml = '<w:tbl><w:tblPr><w:tblW w:w="9900" w:type="dxa"/><w:tblBorders>'
    for edge in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        xml += f'<w:{edge} w:val="single" w:sz="4" w:color="B8C4D1"/>'
    xml += '</w:tblBorders><w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>'
    xml += ''.join(f'<w:gridCol w:w="{width}"/>' for _ in headers) + '</w:tblGrid>'
    for idx, row in enumerate([headers, *rows]):
        xml += '<w:tr>' + ('<w:trPr><w:tblHeader/></w:trPr>' if idx == 0 else '')
        for cell in row:
            shading = '<w:shd w:fill="E8EEF5"/>' if idx == 0 else ''
            xml += f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shading}</w:tcPr>'
            xml += paragraph(cell) + '</w:tc>'
        xml += '</w:tr>'
    blocks.append(xml + '</w:tbl>')
    para('')

def uml():
    para('Diagram disajikan sebagai kotak class dan tabel relasi yang dapat diedit. '
         'Sumber diagram PlantUML: notification.puml.')
    text = (DOC / 'notification.puml').read_text(encoding='utf-8')
    for kind, name, marker, members in re.findall(
            r'(interface|abstract class|class) (\w+)([^\n{]*)\s*\{\n(.*?)\n\}', text, re.S):
        table([f'{kind} {name} {marker.strip()}'], [[s.strip()] for s in members.splitlines()])
    for name in ['EmailChannel', 'WhatsAppChannel']:
        if f'class {name}\n' in text:
            table([name], [['extends AbstractChannel']])
    table(['Dari', 'Relasi', 'Ke'], [
        ['AbstractChannel', 'implements', 'NotificationChannel'],
        ['EmailChannel', 'extends', 'AbstractChannel'],
        ['SmsChannel', 'extends', 'AbstractChannel'],
        ['WhatsAppChannel', 'extends', 'AbstractChannel'],
        ['NotificationService', 'agregasi 0..*', 'NotificationChannel'],
        ['NotificationChannel', 'dependency (parameter)', 'CustomerContact'],
        ['NotificationService', 'dependency (parameter)', 'CustomerContact']])

tree = ast.parse((ROOT / 'tools/build_report.py').read_text(encoding='utf-8'))
env = {'outputs': outputs}
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'explanations' for t in node.targets):
        explanations = ast.literal_eval(node.value)
    if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
        continue
    call = node.value
    if not isinstance(call.func, ast.Name) or call.func.id not in ['heading', 'para', 'table']:
        continue
    args = [eval(compile(ast.Expression(arg), '<report content>', 'eval'), {'__builtins__': {}}, env)
            for arg in call.args]
    # All extracted expressions are local content literals or the saved outputs dictionary.
    if call.func.id == 'para' and str(args[0]).startswith('Lampiran berikut adalah gambar transkrip'):
        args = ['Lampiran berikut berupa transkrip hasil eksekusi sungguhan yang dapat diedit, '
                'bukan screenshot desktop. File teks dan gambar transkrip tersedia di laporan/bukti. '
                'Screenshot terminal asli dapat ditambahkan melalui Insert > Pictures di Word.']
    {'heading': heading, 'para': para, 'table': table}[call.func.id](*args)
    if call.func.id == 'heading' and str(args[0]).startswith('Diagram UML'):
        uml()

for label in ['L1', 'L3', 'L4', 'T1a', 'T1e', 'NimParams', 'SelfCheck', 'TugasCheck', 'TugasApp']:
    heading(label)
    if label in explanations:
        para(explanations[label])
    for line in outputs[label].splitlines():
        blocks.append(paragraph(line, 'Code'))

ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{ns}"><w:body>{''.join(blocks)}
<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>
<w:pgMar w:top="1134" w:right="1000" w:bottom="1134" w:left="1000"/>
</w:sectPr></w:body></w:document>'''
styles = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{ns}">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>
<w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="160"/><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:b/><w:color w:val="17365D"/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/>
<w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/><w:shd w:fill="F2F4F7"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="16"/></w:rPr></w:style>
</w:styles>'''
content_types = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''
rels = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
doc_rels = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
parts = {'[Content_Types].xml': content_types, '_rels/.rels': rels,
         'word/document.xml': document, 'word/styles.xml': styles, 'word/_rels/document.xml.rels': doc_rels}
dest = DOC / 'Laporan_Tugas_2511532001.docx'
with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name, xml in parts.items():
        ET.fromstring(xml)
        archive.writestr(name, xml.encode('utf-8'))
with zipfile.ZipFile(dest) as archive:
    assert archive.testzip() is None
    doc = ET.fromstring(archive.read('word/document.xml'))
    assert len(doc.findall('.//{' + ns + '}tbl')) >= 4
print(dest)
print('DOCX valid; teks, tabel, dan transkrip dapat diedit.')
