from pathlib import Path
import sys
import pypdfium2 as P
from PIL import Image, ImageDraw

source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
pdf=P.PdfDocument(source)
thumbnails=[]
for i,page in enumerate(pdf):
    image=page.render(scale=1.5).to_pil()
    image.save(out/f'page-{i+1}.png')
    image.thumbnail((306,420));thumbnails.append(image.copy())
for start in range(0,len(thumbnails),8):
    canvas=Image.new('RGB',(1224,900),'#cccccc');draw=ImageDraw.Draw(canvas)
    for j,image in enumerate(thumbnails[start:start+8]):
        x=j%4*306;y=j//4*450
        canvas.paste(image,(x,y+22));draw.text((x+5,y+3),str(start+j+1),fill='black')
    canvas.save(out/f'contact-{start//8+1}.png')
print('Rendered',len(pdf),'pages')
