#!/usr/bin/env python3
"""Add tour-stop photos.
Usage: python3 add_photos.py <folder> [--credit "Photo by John Thomas"]
Files in <folder> must be named by stop number: 12.jpg, 16.png, ...
Optional captions: a captions.csv in <folder> with lines: stop,caption,credit
Each photo is resized to ~1200px wide, saved as images/<stop>.jpg (~150KB), and linked in stories/woodstock.json.
Requires Pillow (pip install pillow). Only use photos you took or have permission to use."""
import sys,os,io,csv,json,re
from PIL import Image,ImageOps
STORY='stories/woodstock.json';OUT='images';W=1200;TARGET=150_000
def compress(path,dest):
    im=ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    if im.width>W: im=im.resize((W,round(im.height*W/im.width)),Image.LANCZOS)
    for q in range(85,34,-5):
        b=io.BytesIO();im.save(b,'JPEG',quality=q,optimize=True,progressive=True)
        if b.tell()<=TARGET:break
    open(dest,'wb').write(b.getvalue());return b.tell()
def main():
    a=sys.argv[1:]
    if not a: print(__doc__);sys.exit(1)
    folder=a[0];credit=a[a.index('--credit')+1] if '--credit' in a else ''
    S=json.load(open(STORY,encoding='utf-8'));R={r['stop']:r for r in S['route']}
    caps={}
    cp=os.path.join(folder,'captions.csv')
    if os.path.exists(cp):
        for row in csv.reader(open(cp,encoding='utf-8')):
            if row and row[0].strip().isdigit(): caps[int(row[0])]=(row+['',''])[1:3]
    os.makedirs(OUT,exist_ok=True);n=0
    for f in sorted(os.listdir(folder)):
        m=re.fullmatch(r'(\d+)\.(jpe?g|png)',f,re.I)
        if not m: continue
        s=int(m.group(1))
        if s not in R: print('skip',f,'(no such stop)');continue
        size=compress(os.path.join(folder,f),os.path.join(OUT,f'{s}.jpg'))
        cap,cr=caps.get(s,('',''))
        old=R[s].get('photo') or {}
        R[s]['photo']={'src':f'images/{s}.jpg','alt':old.get('alt') or R[s]['name'],
            'caption':cap or old.get('caption',''),'credit':cr or credit or old.get('credit','')}
        print(f'stop {s}: images/{s}.jpg {size//1024} KB');n+=1
    json.dump(S,open(STORY,'w',encoding='utf-8'),indent=1,ensure_ascii=False)
    print(n,'photo(s) added. Upload images/ and stories/woodstock.json.')
if __name__=='__main__':main()
