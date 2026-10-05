import sys,glob
from PIL import Image, ImageDraw
files=sys.argv[2:]; out=sys.argv[1]
ims=[Image.open(f).convert('RGB') for f in files]
W=max(i.width for i in ims); 
H=sum(i.height+20 for i in ims)
sh=Image.new('RGB',(W,H),(200,200,200)); d=ImageDraw.Draw(sh); y=0
for f,i in zip(files,ims):
    d.text((2,y),f,fill='black'); sh.paste(i,(0,y+14)); y+=i.height+20
sh.save(out)
