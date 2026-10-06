import sys,glob
from PIL import Image
files=sys.argv[2:]; out=sys.argv[1]
ims=[Image.open(f).convert('RGB') for f in files]
W=max(i.width for i in ims); H=sum(i.height+8 for i in ims)
S=Image.new('RGB',(W,H),(200,0,200)); y=0
for i in ims: S.paste(i,(0,y)); y+=i.height+8
S.save(out)
