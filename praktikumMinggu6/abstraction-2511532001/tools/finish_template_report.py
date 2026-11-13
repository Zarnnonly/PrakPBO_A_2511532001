from pathlib import Path
import json
import zipfile
import hashlib
from lxml import etree as E

root=Path(__file__).resolve().parents[1]
qa=root/'laporan/qa_pekan6'
path=root/'laporan/Laporan_Praktikum_PBO_Pekan_6.docx'
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
tag=lambda t:'{'+ns['w']+'}'+t
pages=json.loads((qa/'pagination.json').read_text(encoding='utf-8-sig'))
targets=dict(json.loads((qa/'toc_targets.json').read_text(encoding='utf-8')))
with zipfile.ZipFile(path) as z: parts={n:z.read(n) for n in z.namelist()}
doc=E.fromstring(parts['word/document.xml'])
toc=False
for par in doc.find(tag('body')):
    text=''.join(par.xpath('.//w:t/text()',namespaces=ns))
    if text=='DAFTAR ISI': toc=True;continue
    if text=='KATA PENGANTAR': break
    if not toc: continue
    # Text nodes are separated by a Word tab element, not a literal tab in w:t.
    ts=par.findall('.//'+tag('t'))
    if len(ts)<2: continue
    label=ts[0].text
    if label in targets:
        ts[-1].text=str(pages[targets[label]])
parts['word/document.xml']=E.tostring(doc,xml_declaration=True,encoding='UTF-8',standalone=True)
with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
    for n,data in parts.items():z.writestr(n,data)
baseline=json.loads((qa/'package_inventory.json').read_text())
reference=Path('C:/Users/lenovo/Documents/Laporan Praktikum PBO Pekan 5.docx')
assert hashlib.sha256(reference.read_bytes()).hexdigest()==baseline['reference_sha256']
for n,record in baseline['parts'].items():
    if n not in ['word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml']:
        assert hashlib.sha256(parts[n]).hexdigest()==record['sha256'],n
with zipfile.ZipFile(reference) as z:
    original=E.fromstring(z.read('word/document.xml'))
old=original.findall('.//'+tag('sectPr'))
new=doc.findall('.//'+tag('sectPr'))
assert len(old)==len(new)==4
for a,b in zip(old,new):
    for name in ['pgSz','pgMar']:
        assert a.find(tag(name)).attrib==b.find(tag(name)).attrib
(qa/'verification.json').write_text(json.dumps({'reference_unchanged':True,'original_package_parts_preserved':25,'section_count':4,'toc_actual_word_pages':pages},indent=2),encoding='utf-8')
print('TOC updated; original logo, styles, sections, headers and footers verified.')
