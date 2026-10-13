#!/usr/bin/env python3
"""Verify every W05–W16 package; write machine-readable evidence.

Run from any directory. Requires ffmpeg/ffprobe; no third-party Python packages.
"""
from pathlib import Path
from html.parser import HTMLParser
import argparse, json, re, subprocess
from urllib.parse import unquote, urlsplit

BASE = Path(__file__).resolve().parent
DOCS = BASE.parent


class Resources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.videos = 0
        self.tracks = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'video':
            self.videos += 1
        if tag == 'track':
            self.tracks.append(attrs)
        for key in ('src', 'poster', 'href'):
            if key in attrs:
                self.refs.append(attrs[key])


def command(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def normalize(text):
    return re.sub(r'\s+', '', text)


def validate(decode=True):
    folders = sorted(p for p in BASE.glob('w*') if p.is_dir() and int(p.name[1:3]) in range(5,17))
    assert len(folders) == 12, len(folders)
    rows = []
    for p in folders:
        data = json.loads((p/'storyboard.json').read_text(encoding='utf-8'))
        slug = data['slug']
        mp4 = p/(slug+'_animation.mp4')
        for name in ('poster.jpg','narration.txt','make_narration.ps1','render_animation.py',slug+'_animation.srt',slug+'_animation.vtt'):
            assert (p/name).is_file(), p/name
        probe = json.loads(command(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(mp4)]))
        video = next(s for s in probe['streams'] if s['codec_type']=='video')
        audio = next(s for s in probe['streams'] if s['codec_type']=='audio')
        duration = float(probe['format']['duration'])
        timing = data['timing']
        assert video['codec_name']=='h264' and audio['codec_name']=='aac'
        assert (video['width'],video['height']) == (1280,720)
        assert abs(duration-timing['video_seconds']) < .05
        assert abs(float(video['duration'])-float(audio['duration'])) < .05
        assert duration-timing['speech_seconds'] >= 1.95
        cues = timing['cues']
        assert len(cues)==len(data['scenes'])==8
        assert cues[0]['start']==0 and abs(cues[-1]['end']-timing['speech_seconds'])<.001
        for a,b in zip(cues,cues[1:]):
            assert abs(a['end']-b['start']) < .001
        narration = (p/'narration.txt').read_text(encoding='utf-8')
        assert normalize(narration)==normalize(''.join(c['text'] for c in cues))
        for suffix in ('srt','vtt'):
            text=(p/(slug+'_animation.'+suffix)).read_text(encoding='utf-8')
            stripped=re.sub(r'^WEBVTT\s*', '', text)
            stripped=re.sub(r'^\d+\s*$', '', stripped, flags=re.M)
            stripped=re.sub(r'^\d\d:\d\d:\d\d[.,]\d{3} --> .*$', '', stripped, flags=re.M)
            assert normalize(stripped)==normalize(narration),(slug,suffix)
            assert text.count(' --> ')==len(cues)
        page=DOCS/data['source_page']; html=page.read_text(encoding='utf-8')
        parser=Resources();parser.feed(html)
        assert parser.videos==1,(page,parser.videos)
        assert len(parser.tracks)==1 and parser.tracks[0]['src'].endswith('.vtt')
        assert parser.tracks[0]['srclang']=='zh-Hant' and 'default' not in parser.tracks[0]  # MP4 already has full burned-in captions
        refs=[]
        for ref in parser.refs:
            split=urlsplit(ref)
            if split.scheme or split.netloc or not split.path:continue
            target=page.parent/unquote(split.path)
            assert target.is_file(),(page,ref)
            refs.append(ref)
        sections=re.findall(r'<section.*?</section>',html,re.S)
        assert 'animation-slide' in sections[3]
        assert 'body.scroll .animation-layout{grid-template-columns:1fr}' in html
        assert "e.target.closest('video,a,button,input,select,textarea')" in html
        assert "s.querySelectorAll('video').forEach(v=>v.pause())" in html
        if decode:
            command(['ffmpeg','-v','error','-i',str(mp4),'-f','null','-'])
        rows.append({'week':data['week'],'page':str(page.relative_to(DOCS)),
                     'mp4':str(mp4.relative_to(DOCS)), 'duration_seconds':duration,
                     'audio_seconds':float(audio['duration']), 'video_seconds':float(video['duration']),
                     'speech_seconds':timing['speech_seconds'],'frames':int(video['nb_read_frames']),
                     'size_bytes':int(probe['format']['size']),'caption_cues':len(cues),
                     'relative_references_checked':refs,'full_decode_passed':decode})
    return {'verified_count':len(rows),'caption_cues':sum(x['caption_cues'] for x in rows),
            'duration_seconds':sum(x['duration_seconds'] for x in rows),'videos':rows}


if __name__=='__main__':
    args=argparse.ArgumentParser()
    args.add_argument('--output',type=Path,default=BASE/'w05-w16-validation.json')
    parsed=args.parse_args()
    report=validate()
    parsed.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
