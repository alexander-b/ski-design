# Make light uniform product-photo backgrounds pure white so they blend into the card
import glob,sys
from PIL import Image
def bg(im):
    w,h=im.size;pts=[(2,2),(w-3,2),(2,h-3),(w-3,h-3),(w//2,2),(w//2,h-3)]
    return [im.getpixel(p) for p in pts]
def fix(path):
    im=Image.open(path).convert('RGB');c=bg(im)
    lum=[sum(p)/3 for p in c]
    if min(lum)<205 or max(lum)>=252 or max(lum)-min(lum)>10: return False
    m=[min(p[i] for p in c) for i in range(3)]
    lut=[]
    for i in range(3):
        k=255/max(m[i]-2,1); lut+= [min(255,int(v*k)) for v in range(256)]
    im.point(lut).save(path,'JPEG',quality=84,optimize=True,progressive=True);return True
n=0
for f in sorted(glob.glob('p/**/*.jpg',recursive=True)):
    if '/race/' in f or '/bind/' in f: continue
    if fix(f): n+=1
print('whitened',n)
