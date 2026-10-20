# 1) make light uniform product backgrounds pure white  2) trim product photos to the object
import glob
from PIL import Image, ImageChops
def corners(im):
    w,h=im.size;pts=[(2,2),(w-3,2),(2,h-3),(w-3,h-3),(w//2,2),(w//2,h-3)]
    return [im.getpixel(p) for p in pts]
def whiten(im):
    c=corners(im);lum=[sum(p)/3 for p in c]
    if min(lum)<205 or max(lum)>=252 or max(lum)-min(lum)>10: return im,False
    m=[min(p[i] for p in c) for i in range(3)];lut=[]
    for i in range(3):
        k=255/max(m[i]-2,1);lut+=[min(255,int(v*k)) for v in range(256)]
    return im.point(lut),True
def trim(im):
    if min(sum(p)/3 for p in corners(im))<250: return im,False
    g=im.convert('L').point(lambda v:255 if v<244 else 0)
    bb=g.getbbox()
    if not bb: return im,False
    w,h=im.size;x0,y0,x1,y1=bb
    if x0<=1 and y0<=1 and x1>=w-1 and y1>=h-1: return im,False
    pad=max(4,int(0.02*max(x1-x0,y1-y0)))
    bb=(max(0,x0-pad),max(0,y0-pad),min(w,x1+pad),min(h,y1+pad))
    if (bb[2]-bb[0])>=w-2 and (bb[3]-bb[1])>=h-2: return im,False
    return im.crop(bb),True
n=0
for f in sorted(glob.glob('p/**/*.jpg',recursive=True)):
    if '/race/' in f: continue
    im=Image.open(f).convert('RGB');ch=False
    im,a=whiten(im);ch|=a
    im,b=trim(im);ch|=b
    if ch: im.save(f,'JPEG',quality=84,optimize=True,progressive=True);n+=1
print('processed',n)
