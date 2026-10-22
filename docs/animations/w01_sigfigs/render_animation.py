
from pathlib import Path
import json, math, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'storyboard.json').read_text(encoding='utf-8'))
W,H,FPS=1280,720,24
AUDIO=ROOT/'narration.wav'; OUT=ROOT/(DATA['slug']+'_animation.mp4')
import os
FONT=os.environ.get('CHEM_FONT','/mnt/c/Windows/Fonts/msjh.ttc'); BOLD=os.environ.get('CHEM_BOLD','/mnt/c/Windows/Fonts/msjhbd.ttc')
for _f in ['/mnt/c/Windows/Fonts/mingliu.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc','/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc']:
 if not Path(FONT).exists() and Path(_f).exists(): FONT=BOLD=_f
def ft(n,b=False): return ImageFont.truetype(BOLD if b else FONT,n)
F={'title':ft(48,1),'h1':ft(38,1),'body':ft(28),'small':ft(21),'num':ft(54,1),'formula':ft(34,1)}
BG=(246,251,255); DARK=(26,44,64); BLUE=tuple(DATA['color']); RED=(213,79,93); TEAL=(33,166,153); ORANGE=(244,151,64); GRAY=(88,104,120); LIGHT=(221,238,250)
def duration(p):
 r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(p)],capture_output=True,text=True,check=True); return float(r.stdout.strip())
TOTAL=max(58,duration(AUDIO)+0.2)
def cl(x): return max(0,min(1,x))
def sm(x): x=cl(x); return x*x*(3-2*x)
def rr(d,xy,r,fill,outline=None,w=2): d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=w)
def center(d,xy,text,font,fill=DARK,sp=8): d.multiline_text(xy,text,font=font,fill=fill,anchor='mm',align='center',spacing=sp)
def header(d,t):
 d.text((42,28),f"普通化學 {DATA['week']}｜教學動畫",font=F['small'],fill=BLUE)
 d.text((42,60),DATA['title'],font=F['h1'],fill=DARK)
 rr(d,(42,104,W-42,116),7,(226,238,247)); rr(d,(42,104,42+(W-84)*cl(t/TOTAL),116),7,BLUE)
def caption(d,i):
 top,bottom=DATA['caps'][i]
 rr(d,(150,595,1130,695),24,(255,255,255),(197,221,238),2); center(d,(640,637),top+'\n'+bottom,F['body'])
def card(d,xy,title,body,color):
 x1,y1,x2,y2=xy; rr(d,xy,24,(255,255,255),color,4); d.text((x1+24,y1+20),title,font=F['h1'],fill=color); d.multiline_text((x1+24,y1+78),body,font=F['body'],fill=DARK,spacing=8)
def frame(t):
 im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
 for x in range(0,W,85): d.line((x,126,x+150,H),fill=(235,246,252),width=1)
 header(d,t); i=min(len(DATA['caps'])-1,int(t/(TOTAL/len(DATA['caps'])))); p=sm((t-i*(TOTAL/len(DATA['caps'])))/(TOTAL/len(DATA['caps'])))
 if i==0:
  card(d,(120,205,565,480),'情境問題',DATA['caps'][0][0]+'\n'+DATA['caps'][0][1],BLUE)
  rr(d,(680,235,1080,450),24,(255,255,255),RED,4); center(d,(880,330),DATA['answer'],F['num'],RED); center(d,(880,405),'先判斷數字代表什麼',F['body'],GRAY)
 elif i==1:
  center(d,(640,180),DATA['formula'],F['num'],BLUE)
  for k,b in enumerate(DATA['bullets']):
   rr(d,(180,270+k*88,1100,335+k*88),18,(255,255,255),BLUE,3); d.text((215,285+k*88),str(k+1),font=F['h1'],fill=BLUE); d.text((280,288+k*88),b,font=F['body'],fill=DARK)
 elif i==2:
  center(d,(640,180),'把文字變成可計算的量',F['title'],DARK)
  labels=['讀標示','看單位','用公式','檢查合理性']
  for k,lab in enumerate(labels):
   x=135+k*285; rr(d,(x,300,x+230,430),22,(255,255,255),BLUE,4); center(d,(x+115,365),lab,F['h1'],BLUE)
   if k<3: d.line((x+235,365,x+278,365),fill=ORANGE,width=8)
 elif i==3:
  center(d,(640,168),'常見錯誤：只看數字，不看意義',F['title'],RED)
  card(d,(145,255,585,475),'錯誤想法',DATA['caps'][3][0],RED)
  card(d,(695,255,1135,475),'正確做法',DATA['caps'][3][1],TEAL)
 else:
  center(d,(640,175),'帶走一句話',F['title'],DARK)
  center(d,(640,315),DATA['caps'][4][0],F['num'],RED)
  center(d,(640,410),DATA['caps'][4][1],F['h1'],BLUE)
  d.text((640,520),'資料來源：普通化學 '+DATA['week']+' 教材頁',font=F['small'],fill=GRAY,anchor='mm')
 caption(d,i); return im
def ts(x):
 h=int(x//3600); m=int((x%3600)//60); s=int(x%60); ms=int((x-int(x))*1000); return f'{h:02}:{m:02}:{s:02},{ms:03}'
def srt():
 seg=TOTAL/len(DATA['caps']); out=[]
 for n,(a,b) in enumerate(DATA['caps'],1): out += [str(n),f'{ts((n-1)*seg)} --> {ts(min(n*seg,TOTAL))}',a+'\n'+b,'']
 (ROOT/(DATA['slug']+'_animation.srt')).write_text('\n'.join(out),encoding='utf-8')
def render():
 srt(); n=int(TOTAL*FPS); cmd=['ffmpeg','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(AUDIO),'-c:v','libx264','-preset','medium','-crf','24','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-af','apad','-shortest',str(OUT)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE); assert p.stdin
 for k in range(n): p.stdin.write(frame(k/FPS).tobytes())
 p.stdin.close(); rc=p.wait();
 if rc: raise SystemExit(rc)
 print(OUT)
if __name__=='__main__': render()
