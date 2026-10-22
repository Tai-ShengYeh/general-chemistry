#!/usr/bin/env python3
"""Replace the W03 soundtrack while keeping the existing picture.

W03 has no frame renderer in the repo, so the narration is rebuilt from one
ElevenLabs clip per sentence in narration.txt (.render-cache/speech-NNN.wav) and
placed at the sentence start times of the original recording (START, seconds).
A clip that runs past the next start pushes the following clips later. The video
stream is copied untouched (-c:v copy); only the AAC track is re-encoded.

    python remix_narration.py           # needs the WAVs in .render-cache/
    ELEVENLABS_API_KEY=... python remix_narration.py --synthesize
"""
from pathlib import Path
import json, os, subprocess, sys, wave

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / '.render-cache'
VIDEO = ROOT / 'w03_mole_salt_animation.mp4'
START = [0.18, 6.82, 15.04, 22.44, 25.42, 35.66, 46.06, 49.66, 59.62]
GAP = 0.35  # minimum silence between sentences when a clip overruns


def main():
    sentences = [l.strip() for l in (ROOT / 'narration.txt').read_text(encoding='utf-8').splitlines() if l.strip()]
    assert len(sentences) == len(START)
    if '--synthesize' in sys.argv:
        sys.path.insert(0, str(ROOT.parent))
        from make_narration_elevenlabs import synthesize_scenes
        synthesize_scenes(sentences, CACHE)
    clips = [CACHE / f'speech-{i:03}.wav' for i in range(len(sentences))]
    with wave.open(str(clips[0])) as w:
        params = w.getparams()
    rate = params.framerate
    frames, cursor, cues = b'', 0.0, []
    for text, start, clip in zip(sentences, START, clips):
        with wave.open(str(clip)) as w:
            assert w.getframerate() == rate and w.getnchannels() == params.nchannels
            pcm = w.readframes(w.getnframes())
            dur = w.getnframes() / rate
        start = max(start, cursor + GAP if cursor else start)
        pad = int(round((start - cursor) * rate)) * params.sampwidth * params.nchannels
        frames += b'\0' * pad + pcm
        cues.append({'start': round(start, 3), 'end': round(start + dur, 3), 'text': text})
        cursor = start + dur
    out = ROOT / 'narration.wav'
    with wave.open(str(out), 'wb') as w:
        w.setparams(params)
        w.writeframes(frames)
    (CACHE / 'narration-cues.json').write_text(json.dumps(cues, ensure_ascii=False, indent=1), encoding='utf-8')
    tmp = ROOT / 'w03_mole_salt_animation.tmp.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(VIDEO), '-i', str(out), '-map', '0:v:0', '-map', '1:a:0',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-af', 'apad', '-shortest',
                    '-movflags', '+faststart', str(tmp)], check=True)
    tmp.replace(VIDEO)
    print(json.dumps({'speech_end': round(cursor, 2), 'cues': len(cues)}))


if __name__ == '__main__':
    main()
