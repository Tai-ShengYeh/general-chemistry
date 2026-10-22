#!/usr/bin/env python3
"""Render sentence-aligned teaching clips (Pillow, ffmpeg, ElevenLabs or Windows Hanhan).

Each lesson wrapper passes its folder. Speech is synthesized sentence-by-sentence
so subtitles and visual changes follow measured WAV durations, not text estimates.
Narration backend: ElevenLabs when ELEVENLABS_API_KEY is set (or CHEM_TTS=elevenlabs),
otherwise the Windows Hanhan voice through make_narration.ps1. Existing WAVs in
.render-cache/ are reused when speech-text.json matches the storyboard.
Set CHEM_FONT/CHEM_BOLD to override the default Traditional Chinese fonts.
"""
from pathlib import Path
import json, math, os, subprocess, sys, wave
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1280, 720, 24
FONT_CANDIDATES = ['/mnt/c/Windows/Fonts/msjh.ttc', '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                   '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc']
BOLD_CANDIDATES = ['/mnt/c/Windows/Fonts/msjhbd.ttc', '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
                   '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc']


def pick_font(env, candidates):
    chosen = os.environ.get(env)
    if chosen:
        return chosen
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError('No Traditional Chinese font found; set ' + env)


FONT = pick_font('CHEM_FONT', FONT_CANDIDATES)
BOLD = pick_font('CHEM_BOLD', BOLD_CANDIDATES)
DARK = (26, 44, 64)


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True, errors='replace')


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def wrap(text, face, width):
    # Character-based wrapping also works for Chinese without whitespace.
    lines = []
    for paragraph in text.split('\n'):
        line = ''
        for char in paragraph:
            if line and face.getlength(line + char) > width:
                lines.append(line)
                line = ''
            line += char
        lines.append(line)
    return '\n'.join(lines)


def fit_text(draw, box, text, size=36, bold=False, color=DARK):
    x1, y1, x2, y2 = box
    for n in range(size, 15, -1):
        face = font(n, bold)
        wrapped = wrap(text, face, x2-x1)
        bounds = draw.multiline_textbbox((0, 0), wrapped, font=face, spacing=8)
        if bounds[3]-bounds[1] <= y2-y1:
            draw.multiline_text(((x1+x2)/2, (y1+y2)/2), wrapped,
                                font=face, fill=color, anchor='mm', align='center', spacing=8)
            return
    raise ValueError('Text cannot fit: ' + text)


def timestamp(value, sep=','):
    ms = round(value*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}{sep}{ms%1000:03}'


def frame(data, index, progress, caption):
    im = Image.new('RGB', (W, H), (246, 251, 255))
    d = ImageDraw.Draw(im)
    blue = tuple(data['color'])
    d.text((42, 25), '普通化學 ' + data['week'] + '｜錨點概念短片', font=font(22), fill=blue)
    fit_text(d, (42, 60, 1238, 120), data['title'], 36, True)
    d.rounded_rectangle((42, 137, 1238, 146), radius=4, fill=(221, 238, 250))
    if progress:
        d.rounded_rectangle((42, 137, 42+1196*progress, 146), radius=4, fill=blue)
    scene = data['scenes'][index]
    fit_text(d, (65, 160, 1215, 215), scene['heading'], 32, True, blue)
    # Lesson-specific causal steps, revealed one-by-one across the sentence.
    for k, label in enumerate(scene['steps']):
        x = 65+k*405
        visible = progress >= scene['start_fraction'] + (scene['end_fraction']-scene['start_fraction'])*k/4
        d.rounded_rectangle((x, 245, x+340, 425), radius=22,
                            fill=(255,255,255) if visible else (237,242,247),
                            outline=blue if visible else (205,218,228), width=3)
        if visible:
            d.ellipse((x+140, 259, x+200, 319), fill=blue)
            d.text((x+170, 289), str(k+1), font=font(28, True), anchor='mm', fill='white')
            fit_text(d, (x+20, 327, x+320, 408), label, 30, True)
        if k < 2:
            d.line((x+350, 335, x+390, 335), fill=blue, width=6)
            d.polygon([(x+390,335),(x+378,326),(x+378,344)], fill=blue)
    fit_text(d, (65, 444, 1215, 516), scene['formula'], 38, True, blue)
    d.rounded_rectangle((50, 535, 1230, 684), radius=20, fill='white', outline=(197,221,238), width=2)
    fit_text(d, (78, 550, 1202, 668), caption, 29)
    return im


def render(root):
    root = Path(root)
    data = json.loads((root/'storyboard.json').read_text(encoding='utf-8'))
    cache = root/'.render-cache'
    cache.mkdir(exist_ok=True)
    speech_text = json.dumps([s['speech'] for s in data['scenes']], ensure_ascii=False)
    manifest = cache/'speech-text.json'
    complete = all((cache/f'speech-{i:03}.wav').exists() for i in range(len(data['scenes'])))
    if not complete or not manifest.exists() or manifest.read_text(encoding='utf-8') != speech_text:
        backend = os.environ.get('CHEM_TTS', 'elevenlabs' if os.environ.get('ELEVENLABS_API_KEY') else 'hanhan')
        if backend == 'elevenlabs':
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from make_narration_elevenlabs import synthesize_scenes
            synthesize_scenes([s['speech'] for s in data['scenes']], cache)
        else:
            ps = run(['wslpath', '-w', str(root/'make_narration.ps1')]).stdout.strip()
            run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps])
        manifest.write_text(speech_text, encoding='utf-8')
    durations = []
    assert data['scenes'], 'Storyboard must contain at least one spoken scene'
    with wave.open(str(cache/'speech-000.wav'), 'rb') as first:
        params = first.getparams()
    with wave.open(str(root/'narration.wav'), 'wb') as out:
        out.setparams(params)
        for i, scene in enumerate(data['scenes']):
            with wave.open(str(cache/f'speech-{i:03}.wav'), 'rb') as wav:
                assert wav.getnchannels() == params.nchannels and wav.getsampwidth() == params.sampwidth
                assert wav.getframerate() == params.framerate
                durations.append(wav.getnframes()/wav.getframerate())
                out.writeframes(wav.readframes(wav.getnframes()))
    speech_total = sum(durations)
    # Rounded up to a video frame; two seconds of silence preserve the ending.
    total = math.ceil((speech_total+2)*FPS)/FPS
    cues, start = [], 0.0
    for i, (scene, duration) in enumerate(zip(data['scenes'], durations)):
        end = start+duration
        scene['start_fraction'], scene['end_fraction'] = start/total, end/total
        cues.append({'start':start, 'end':end, 'text':scene['speech']})
        start = end
    data['timing'] = {'speech_seconds':speech_total, 'video_seconds':total, 'cues':cues}
    (root/'storyboard.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    slug = data['slug']
    srt, vtt = [], ['WEBVTT', '']
    for i, cue in enumerate(cues, 1):
        # Same full spoken text in SRT, browser VTT, and burned-in captions.
        text = wrap(cue['text'], font(29), 1100)
        srt.extend([str(i), timestamp(cue['start'])+' --> '+timestamp(cue['end']), text, ''])
        vtt.extend([str(i), timestamp(cue['start'], '.')+' --> '+timestamp(cue['end'], '.'), text, ''])
    (root/(slug+'_animation.srt')).write_text('\n'.join(srt).rstrip()+'\n', encoding='utf-8')
    (root/(slug+'_animation.vtt')).write_text('\n'.join(vtt).rstrip()+'\n', encoding='utf-8')
    # Four visual beats per spoken sentence, keeping rendering fast and auditable.
    listing = []
    for i, cue in enumerate(cues):
        for beat in range(4):
            path = cache/f'frame-{i:03}-{beat}.png'
            t = cue['start']+(cue['end']-cue['start'])*(beat+.1)/4
            frame(data, i, t/total, cue['text']).save(path)
            listing.extend([f"file '{path.name}'", f"duration {(cue['end']-cue['start'])/4:.9f}"])
    final = cache/'ending.png'
    frame(data, len(cues)-1, 1, data['answer']).save(final)
    listing.extend([f"file '{final.name}'", f'duration {total-speech_total:.9f}', f"file '{final.name}'"])
    (cache/'frames.txt').write_text('\n'.join(listing)+'\n')
    frame(data, 0, data['scenes'][0]['end_fraction'], data['anchor']).save(root/'poster.jpg', quality=92)
    run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(cache/'frames.txt'),
         '-i', str(root/'narration.wav'), '-vf', f'fps={FPS}', '-af', 'apad', '-t', str(total),
         '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', str(root/(slug+'_animation.mp4'))])
    print(json.dumps({'slug':slug, 'speech':speech_total, 'video':total, 'sentences':len(cues)}))


if __name__ == '__main__':
    render(Path(sys.argv[1]))
