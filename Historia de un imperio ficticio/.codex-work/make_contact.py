from PIL import Image,ImageDraw
from pathlib import Path
import sys, math
src=Path(sys.argv[1]); out=Path(sys.argv[2]); imgs=[]
for p in sorted(src.glob('page-*.png')):
 im=Image.open(p).convert('RGB'); im.thumbnail((220,285)); imgs.append((p.name,im.copy()))
w=220*5; h=310*math.ceil(len(imgs)/5); sheet=Image.new('RGB',(w,h),'white'); d=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(imgs):
 x=(i%5)*220;y=(i//5)*310;sheet.paste(im,(x,y));d.text((x+3,y+287),name,fill='black')
sheet.save(out)
