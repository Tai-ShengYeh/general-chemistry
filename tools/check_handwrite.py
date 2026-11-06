"""Browser integration checks, either under a local Pages prefix or on the live site."""
import argparse,io,json,re,threading
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote,urlsplit,quote
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';OUT=ROOT/'reports/handwrite'
OUT.mkdir(parents=True,exist_ok=True)
class Links(HTMLParser):
    def __init__(self):super().__init__();self.refs=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for key in ['href','src']:
            if key in a:self.refs.append(a[key])
        if 'srcdoc' in a:
            p=Links();p.feed(a['srcdoc']);self.refs+=p.refs
def audit():
    checked=0
    for file in (DOCS/'handwrite').rglob('*.html'):
        p=Links();p.feed(file.read_text(encoding='utf-8'))
        for ref in p.refs:
            u=urlsplit(ref)
            if u.scheme or u.netloc or not u.path:continue
            target=(file.parent/unquote(u.path)).resolve()
            assert target.is_relative_to(DOCS.resolve()) and target.exists(),(file,ref)
            checked+=1
    return checked
def serve():
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):super().__init__(*a,directory=str(DOCS),**kw)
        def translate_path(self,path):
            if path.startswith('/general-chemistry/'):path=path[len('/general-chemistry'):]
            return super().translate_path(path)
        def send_head(self):
            path=Path(self.translate_path(self.path));m=re.fullmatch(r'bytes=(\d+)-(\d*)',self.headers.get('Range',''))
            if path.is_file() and m:
                size=path.stat().st_size;start=int(m[1]);end=min(int(m[2]) if m[2] else size-1,size-1)
                if start>=size or end<start:self.send_error(416);return None
                with path.open('rb') as stream:stream.seek(start);data=stream.read(end-start+1)
                self.send_response(206);self.send_header('Content-Type',self.guess_type(str(path)));self.send_header('Accept-Ranges','bytes');self.send_header('Content-Range',f'bytes {start}-{end}/{size}');self.send_header('Content-Length',str(len(data)));self.end_headers();return io.BytesIO(data)
            return super().send_head()
        def log_message(self,*a):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,f'http://127.0.0.1:{server.server_port}/general-chemistry/'
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base');parser.add_argument('--preview',action='store_true');args=parser.parse_args()
    server=None
    if args.base:base=args.base.rstrip('/')+'/'
    else:server,base=serve()
    name='live' if args.base else 'local'
    report=dict(base=base,preview=args.preview,units=[],chapters=[],static_references=audit(),page_errors=[],failed_requests=[],http_errors=[])
    with sync_playwright() as p:
        browser=p.chromium.launch(channel='msedge',headless=True);page=browser.new_page(viewport={'width':1440,'height':1000})
        page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
        page.on('requestfailed',lambda r:report['failed_requests'].append({'url':r.url,'error':r.failure}) if r.failure!='net::ERR_ABORTED' and r.url.startswith(base) else None)
        page.on('response',lambda r:report['http_errors'].append({'url':r.url,'status':r.status}) if r.status>=400 and r.url.startswith(base) else None)
        records=page.request.get(base+'handwrite/course-manifest.json').json()
        assert records==json.loads((DOCS/'handwrite/course-manifest.json').read_text(encoding='utf-8'))
        assert len(records)==40 and (args.preview or all(r['audio'] for r in records))
        catalog=page.request.get(base+'handwrite/source/catalog.json').json()
        page.goto(base);assert page.locator('a.handwrite-week').count()==18
        page.locator('#handwrite-course a').click();assert page.locator('a.unit').count()==18
        page.screenshot(path=str(OUT/f'{name}-overview.png'),full_page=True)
        for unit in catalog:
            u=unit['unit'];selected=[r for r in records if r['unit']==u]
            print('Checking deck',u,flush=True)
            page.goto(base+f'handwrite/{u}.html');assert page.locator('a.chapter').count()==len(selected)
            page.goto(base+quote(unit['file'])+'#1')
            assert page.locator('.slide').count()==unit['slides']+1
            assert page.locator('.slide').first.locator('a[href="handwrite/'+u+'.html"]').count()==1
            assert page.locator('#mtb a.handwrite-toolbar').get_attribute('href')==f'handwrite/{u}.html'
            assert page.locator('#handwrite a.handwrite-chapter').count()==len(selected)
            page.evaluate("document.body.classList.remove('scroll');fit();show(slides.length-1)")
            for size in [{'width':1280,'height':720},{'width':844,'height':390}]:
                page.set_viewport_size(size);page.evaluate('fit()')
                page.wait_for_function('''()=>[...document.querySelectorAll('#handwrite a')].every(a=>{let r=a.getBoundingClientRect();return r.left>=-1&&r.right<=innerWidth+1&&r.top>=-1&&r.bottom<=innerHeight+1})''',timeout=5000)
            if u in ['w01','w01b','w13','w16']:page.screenshot(path=str(OUT/f'{name}-{u}-deck.png'))
            page.evaluate('show(0)');page.keyboard.press('ArrowRight');assert page.evaluate('cur')==1
            page.evaluate("let i=slides.findIndex(s=>s.querySelector('.sol'));show(i);window.__oldSol=i")
            assert not page.evaluate("slides[cur].classList.contains('reveal')")
            page.keyboard.press('ArrowRight');assert page.evaluate("cur===window.__oldSol&&slides[cur].classList.contains('reveal')")
            page.keyboard.press('ArrowRight');assert page.evaluate('cur===window.__oldSol+1')
            page.set_viewport_size({'width':390,'height':844});page.locator('#mtb-mode').click()
            assert page.evaluate("document.body.classList.contains('scroll')")
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),u
            page.evaluate("document.getElementById('handwrite').scrollIntoView({block:'start'})")
            page.locator('#handwrite a.handwrite-chapter').first.click();page.wait_for_function('lessonPlayer.ready')
            assert u in page.url
            page.set_viewport_size({'width':1440,'height':1000})
            report['units'].append(dict(unit=u,original_slides=unit['slides'],chapters=len(selected),projection=True,mobile=True,original_answers=True))
        for r in records:
            print('Checking player',r['id'],flush=True)
            page.goto(base+f'handwrite/{r["id"]}/player.html');page.wait_for_function('lessonPlayer.ready')
            meta=page.evaluate('lessonPlayer.meta');frame=page.frame_locator('#frame')
            assert len(meta['scenes'])==r['scenes']
            if not args.preview:
                assert frame.locator('audio').count()==r['scenes']
                # Exercise playback after seeking to an actual later audio clip.
                voices=frame.locator('audio').evaluate_all('xs=>xs.map(a=>Number(a.dataset.start))')
                start=voices[min(1,len(voices)-1)]
                page.evaluate('t=>lessonPlayer.jump(t)',start+.5);page.locator('#speed').select_option('1.25');page.locator('#play').click()
                page.wait_for_function('''[...document.querySelector('#frame').contentDocument.querySelectorAll('audio')].some(a=>!a.paused&&!a.seeking&&a.readyState>=2&&a.playbackRate===1.25)''',timeout=15000)
                current="[...document.querySelector('#frame').contentDocument.querySelectorAll('audio')].find(a=>!a.paused).currentTime"
                before=page.evaluate(current);page.wait_for_timeout(500);after=page.evaluate(current)
                assert after-before>.25,(r['id'],before,after)
                page.locator('#play').click();page.locator('#speed').select_option('1')
            gate=next(s for s in meta['scenes'] if s['pause'])
            page.evaluate('t=>lessonPlayer.jump(t)',gate['end']-.55);page.locator('#play').click()
            page.wait_for_function("!lessonPlayer.playing&&document.querySelector('#play').textContent==='繼續'")
            page.locator('#play').click();page.wait_for_function('lessonPlayer.playing');page.locator('#play').click()
            page.locator('#reset').click();assert page.evaluate('lessonPlayer.time')==0
            assert frame.locator(f'#sc{len(meta["scenes"])}').evaluate("e=>getComputedStyle(e).visibility")=='hidden'
            assert page.locator('#course-nav a').first.get_attribute('href')==f'../{r["unit"]}.html'
            page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            page.locator('#next').click();page.evaluate('t=>lessonPlayer.jump(t)',meta['scenes'][1]['end']-.5)
            if r['id'] in ['w01-01-measure','w10-01-polarity','w13-01-emulsion','w16-02-oxidation']:page.screenshot(path=str(OUT/f'{name}-{r["id"]}-mobile.png'),full_page=True)
            page.set_viewport_size({'width':1440,'height':1000})
            report['chapters'].append(dict(id=r['id'],audio=not args.preview,seek_speed_reset=True,pause=True,mobile=True))
        browser.close()
    if server:server.shutdown()
    (OUT/f'{name}-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    assert not report['page_errors'],report['page_errors']
    assert not report['failed_requests'],report['failed_requests']
    assert not report['http_errors'],report['http_errors']
    print(json.dumps(dict(target=name,units=len(report['units']),chapters=len(report['chapters']),static_references=report['static_references'],errors=0)))
if __name__=='__main__':main()
