import json,os,io,time,urllib.request,threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from PIL import Image
rows=json.load(open('tools/manifest.json'))
BR='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36'
WM='ski-design-archive/1.0 (https://github.com/alexander-b/ski-design; personal research archive)'
locks={}
fail=[]
def get(url):
    h=urlparse(url).hostname
    slow=('wikimedia' in h) or ('archive.org' in h)
    ua=WM if 'wikimedia' in h else BR
    lk=locks.setdefault(h if slow else url,threading.Lock())
    with lk:
        if slow: time.sleep(1.5)
        return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':ua}),timeout=90).read()
def one(r):
    full=f"p/{r['id']}.jpg"; th=f"p/t/{r['id']}.jpg"
    if os.path.exists(full) and os.path.exists(th): return
    err=''
    for a in range(6):
        try:
            im=Image.open(io.BytesIO(get(r['url'])))
            if im.mode in ('RGBA','LA','P'):
                im=im.convert('RGBA');bg=Image.new('RGB',im.size,(255,255,255));bg.paste(im,mask=im.split()[3]);im=bg
            else: im=im.convert('RGB')
            os.makedirs(os.path.dirname(full),exist_ok=True);os.makedirs(os.path.dirname(th),exist_ok=True)
            f=im.copy();f.thumbnail((3000,3000));f.save(full,'JPEG',quality=84,optimize=True,progressive=True)
            t=im.copy();t.thumbnail((900,1400));t.save(th,'JPEG',quality=80,optimize=True,progressive=True)
            return
        except Exception as e:
            err=str(e);time.sleep(5*(a+1))
    fail.append([r['id'],r['url'],err])
with ThreadPoolExecutor(8) as ex: list(ex.map(one,rows))
json.dump(fail,open('tools/failed.json','w'),indent=0)
print('failed',len(fail))
