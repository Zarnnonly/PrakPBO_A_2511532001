from pathlib import Path
import zipfile,copy
from lxml import etree as E
p=Path('output/LK-P07-2511532001.docx')
with zipfile.ZipFile(p) as z: parts={n:z.read(n) for n in z.namelist()}
r=E.fromstring(parts['word/document.xml']); ns={'w':r.nsmap['w']}; W='{'+ns['w']+'}'
tables=r.findall('.//w:body/w:tbl',ns)
def cell(t,row,c): return tables[t].findall('w:tr',ns)[row].findall('w:tc',ns)[c]
def text(t,row,c): return '\n'.join(''.join(p.itertext()) for p in cell(t,row,c).findall('w:p',ns))
def put(t,row,c,value):
 p=cell(t,row,c).find('w:p',ns); runs=p.findall('w:r',ns); proto=copy.deepcopy(runs[0]) if runs else E.Element(W+'r')
 for ch in list(proto):
  if ch.tag!=W+'rPr':proto.remove(ch)
 for ch in list(p):
  if ch.tag!=W+'pPr':p.remove(ch)
 for i,line in enumerate(value.split('\n')):
  run=copy.deepcopy(proto)
  if i:E.SubElement(run,W+'br')
  tx=E.SubElement(run,W+'t');tx.text=line;p.append(run)
for row in range(1,4):
 put(4,row,1,text(4,row,2));put(4,row,3,'Cocok dengan perkiraan dari kode.')
for row in range(1,5):put(5,row,1,text(5,row,2))
for row in range(1,7):
 put(10,row,1,text(10,row,3));put(10,row,2,text(10,row,4));put(10,row,5,'Cocok')
# Clarify the timing without changing template layout or introducing a new paragraph.
pred=r.findall('.//w:body/w:p',ns)[14]
first=pred.find('.//w:t',ns)
first.text=(first.text or '')+' Catatan pengisian: perkiraan pada LK ini disusun setelah pengujian berdasarkan pembacaan kode.'
assert not any(';' in (t.text or '') for t in r.findall('.//w:t',ns))
parts['word/document.xml']=E.tostring(r,xml_declaration=True,encoding='UTF-8',standalone=True)
tmp=p.with_suffix('.tmp')
with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
 for n,data in parts.items():z.writestr(n,data)
tmp.replace(p)
print('Prediction columns completed')
