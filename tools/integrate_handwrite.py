"""Integrate published handwritten micro-lessons into existing standalone decks."""
import argparse,hashlib,html,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs';PACKAGE=ROOT.parent/'general-chemistry-handwrite';DEST=DOCS/'handwrite'
START='<!-- HANDWRITE:BEGIN -->';END='<!-- HANDWRITE:END -->'
def clean(s):return re.sub(re.escape(START)+'.*?'+re.escape(END),'',s,flags=re.S)
def block(s):return START+s+END
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');args=parser.parse_args()
    records=json.loads((PACKAGE/'course-manifest.json').read_text(encoding='utf-8'))
    catalog=json.loads((PACKAGE/'source/catalog.json').read_text(encoding='utf-8'))
    assert len(records)==40 and (args.preview or all(r['audio'] for r in records))
    DEST.mkdir(exist_ok=True)
    for r in records:
        src=PACKAGE/r['id'];dst=DEST/r['id'];dst.mkdir(exist_ok=True)
        for name in ['index.html','player.html','layout.json','lesson.json','lesson.script.json','timing.json','lesson-notes.md']:
            if (src/name).exists():shutil.copy2(src/name,dst/name)
        shutil.copytree(src/'assets',dst/'assets',dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.raw.mp3','asr_scores.json'))
        shutil.copy2(PACKAGE/(r['id']+'.lesson.json'),DEST/(r['id']+'.lesson.json'))
    for name in ['index.html','course-manifest.json','teacher-notes.md','使用說明.md','source-map.md',*[r['unit']+'.html' for r in catalog]]:shutil.copy2(PACKAGE/name,DEST/name)
    shutil.copytree(PACKAGE/'notes',DEST/'notes',dirs_exist_ok=True)
    (DEST/'source').mkdir(exist_ok=True)
    shutil.copy2(PACKAGE/'source/catalog.json',DEST/'source/catalog.json')
    (DEST/'licenses').mkdir(exist_ok=True)
    skill=ROOT.parent/'handwrite-teaching'
    for p in (skill/'assets/fonts').glob('OFL*.txt'):shutil.copy2(p,DEST/'licenses'/p.name)
    shutil.copy2(skill/'assets/vendor/THIRD-PARTY.txt',DEST/'licenses/THIRD-PARTY.txt')
    (DEST/'licenses/ATTRIBUTION.md').write_text('教材改編：Tai-ShengYeh普通化學課程與OpenStax Chemistry 2e（CC BY 4.0）。手寫引擎原始作者：阿亮老師（曾慶良）／3A科技研究社。字型採各OFL授權，GSAP來源與授權見THIRD-PARTY.txt。技能來源庫未隨本教材發布。\n',encoding='utf-8')
    home=clean((DOCS/'index.html').read_text(encoding='utf-8'))
    for row in catalog:
        unit=row['unit'];file=DOCS/row['file'];original=clean(file.read_text(encoding='utf-8'))
        # The source snapshot is immutable evidence. Only marked additions are made.
        assert hashlib.sha256(original.encode()).hexdigest()==row['sha256'],f'Concurrent edit: {file.name}'
        selected=[r for r in records if r['unit']==unit]
        link=f'handwrite/{unit}.html'
        pattern=r'(<a\s+href="'+re.escape(row['file'])+r'"[^>]*>.*?</a>)'
        home,n=re.subn(pattern,lambda m:m[1]+block(f' <a class="handwrite-week" href="{link}">✍ 手寫動畫</a>'),home,count=1,flags=re.S)
        assert n==1,(unit,'homepage link')
        shortcut=block(f'<p class="handwrite-shortcut"><a href="{link}">✍ 手寫動畫 · {len(selected)}章</a></p>')
        # Append to title slide without changing any original slide number.
        first_end=original.index('</section>')
        content=original[:first_end]+shortcut+original[first_end:]
        cards=''.join(f'<a class="handwrite-chapter" href="handwrite/{r["id"]}/player.html">{i+1}．{html.escape(r["title"])}</a>' for i,r in enumerate(selected))
        section=block(f'<section class="slide handwrite-slide" id="handwrite"><h2>手寫動畫：先想，再核對</h2><p>題目會自動停下；準備好再按「繼續」。</p><div class="handwrite-cards">{cards}</div><p><a href="{link}">本主題動畫目錄 →</a>　<a href="handwrite/index.html">全部動畫</a></p></section>')
        marker='</div></div>\n<script>'
        assert marker in content,file.name
        content=content.replace(marker,section+marker,1)
        extra=block(f'''<style>.handwrite-shortcut a{{display:inline-block;font-size:20px;color:#117a65;border:1px solid #117a65;border-radius:7px;padding:5px 12px;text-decoration:none}}.handwrite-cards{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:24px 0}}.handwrite-chapter{{display:block;padding:14px 18px;background:#edf5f1;border:1px solid #a3c1b6;border-radius:8px;color:#135e52;font-size:23px;text-decoration:none;line-height:1.5}}body.scroll .two-col>div{{width:100%;max-width:100%}}body.scroll .handwrite-cards{{grid-template-columns:1fr}}#mtb .handwrite-toolbar{{white-space:nowrap}}@media(max-width:640px){{#mtb .ttl{{min-width:0;overflow:hidden;text-overflow:ellipsis}}.handwrite-chapter{{font-size:18px}}}}</style><script>(()=>{{const bar=document.getElementById('mtb');if(bar&&!bar.querySelector('.handwrite-toolbar')){{const a=document.createElement('a');a.href={json.dumps(link)};a.className='handwrite-toolbar';a.textContent='✍ 動畫';a.title='開啟本主題手寫動畫';bar.insertBefore(a,bar.querySelector('button'));}}}})();</script>''')
        content=content.replace('</body>',extra+'</body>')
        file.write_text(content,encoding='utf-8')
    minutes=sum(r['minutes'] for r in records)
    overview=block(f'<section id="handwrite-course" class="note"><h2>✍ 手寫動畫教室</h2><p>16個教學主題＋2個延伸專題，共40章、{sum(r["scenes"] for r in records)}幕、約{minutes:.0f}分鐘。觀念逐步圖解，例題先作答再看解答；可暫停、拖曳與調速。</p><p><a href="handwrite/index.html">選擇主題，開始手寫動畫 →</a></p><p>各週進度表也有動畫入口。下載使用時請保留完整播放器與音訊資料夾。</p></section>')
    home=home.replace('<h2>學生練習</h2>',overview+'<h2>學生練習</h2>')
    home=home.replace('</head>',block('<style>.handwrite-week{display:inline-block;color:#126353;font-weight:700;padding:3px 9px;border:1px solid #9abbb0;border-radius:6px;margin:6px 0;text-decoration:none;font-size:14px}#handwrite-course h2{margin-top:0}</style>')+'</head>')
    (DOCS/'index.html').write_text(home,encoding='utf-8')
    print(json.dumps({'units':len(catalog),'chapters':len(records),'scenes':sum(r['scenes'] for r in records),'audio':sum(r['scenes'] for r in records),'minutes':round(minutes,2)},ensure_ascii=False))
if __name__=='__main__':main()
