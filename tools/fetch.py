import json,os,io,sys,time,urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
rows=json.load(open('tools/manifest.json'))
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36','Referer':'https://www.google.com/'}
fail=[]
def one(r):
    full=f"p/{r['id']}.jpg"; th=f"p/t/{r['id']}.jpg"
    if os.path.exists(full) and os.path.exists(th): return
    for a in range(3):
        try:
            data=urllib.request.urlopen(urllib.request.Request(r['url'],headers=UA),timeout=60).read()
            im=Image.open(io.BytesIO(data))
            if im.mode in ('RGBA','LA','P'):
                im=im.convert('RGBA');bg=Image.new('RGB',im.size,(255,255,255));bg.paste(im,mask=im.split()[3]);im=bg
            else: im=im.convert('RGB')
            os.makedirs(os.path.dirname(full),exist_ok=True);os.makedirs(os.path.dirname(th),exist_ok=True)
            f=im.copy();f.thumbnail((3000,3000));f.save(full,'JPEG',quality=84,optimize=True,progressive=True)
            t=im.copy();t.thumbnail((900,1400));t.save(th,'JPEG',quality=80,optimize=True,progressive=True)
            return
        except Exception as e:
            err=str(e);time.sleep(3)
    fail.append([r['id'],r['url'],err])
with ThreadPoolExecutor(6) as ex: list(ex.map(one,rows))
json.dump(fail,open('tools/failed.json','w'),indent=0)
print('failed',len(fail))
