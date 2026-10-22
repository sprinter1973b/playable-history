import subprocess,time,json
from playwright.sync_api import sync_playwright
srv=subprocess.Popen(['python3','-m','http.server','8765'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
S=json.load(open('stories/woodstock.json'));res=[]
with sync_playwright() as p:
 b=p.chromium.launch();pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
 errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
 pg.goto('http://localhost:8765/index.html');pg.wait_for_selector('#go')
 pg.screenshot(path='screenshot-start.png',full_page=True)
 def walk(prefix):
  pg.goto('http://localhost:8765/index.html');pg.click('#go')
  for i in prefix: pg.click(f'button[data-i="{i}"]')
  if pg.locator('#again').count(): res.append((prefix,pg.locator('h2').inner_text()));return
  n=pg.locator('button[data-i]').count()
  for i in range(n): walk(prefix+[i])
 walk([])
 pg.goto('http://localhost:8765/index.html');pg.click('#go');pg.click('button[data-i="0"]');pg.click('button[data-i="0"]');pg.click('button[data-i="0"]')
 pg.screenshot(path='screenshot-scene.png',full_page=True)
 assert pg.locator('.stop a').count()==1
 pg.click('#map');pg.wait_for_selector('.route');assert pg.locator('.route li').count()==len(S['route'])
 pg.screenshot(path='screenshot-map.png',full_page=True)
 pg.click('#tourgo');pg.wait_for_selector('.quiz')
 for k in range(len(S['route'])):
  r=S['route'][k];assert ('Stop %d of'%r['stop']) in pg.inner_text('.top')
  pg.click('button[data-q="%d"]'%r['quiz']['answer']);assert pg.inner_text('#qr')=='Correct!'
  if k==16: pg.screenshot(path='screenshot-tour-stop.png',full_page=True)
  assert pg.locator('.photo').count()==(1 if r.get('photo') else 0)
  if k<len(S['route'])-1: pg.click('#next')
 pg.click('#tl');pg.wait_for_selector('.route')
 pg.click('a.open[data-s="17"]');pg.wait_for_selector('#play');pg.click('#play');pg.wait_for_selector('button[data-i]')
 pg.click('#map');pg.wait_for_selector('#back');pg.click('#back');pg.wait_for_selector('button[data-i]')
 pg.click('#rs');assert pg.locator('#go').count()==1
 b.close()
srv.kill();print(res,'errors:',errs);assert not errs
