#!/usr/bin/env python3
"""Synthesize narration with the ElevenLabs text-to-speech API.

Used by render_teaching_animation.py when ELEVENLABS_API_KEY is set (or
CHEM_TTS=elevenlabs). Can also be run directly:

    python make_narration_elevenlabs.py w08_thermochemistry      # per-sentence WAVs in .render-cache/
    python make_narration_elevenlabs.py w01_sigfigs --whole      # narration.txt -> narration.wav

Voice and model default to the ones used for the published clips:
Ling (Taiwan Mandarin, voice_id Z8Aisvg1z70p27kGvkZZ) on eleven_v4.
Override with CHEM_ELEVEN_VOICE / CHEM_ELEVEN_MODEL.
"""
from pathlib import Path
import json, os, sys, time, urllib.request, wave

VOICE = os.environ.get('CHEM_ELEVEN_VOICE', 'Z8Aisvg1z70p27kGvkZZ')
MODEL = os.environ.get('CHEM_ELEVEN_MODEL', 'eleven_v4')
RATE = 44100


def tts_pcm(text, api_key):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=pcm_{RATE}'
    body = json.dumps({'text': text, 'model_id': MODEL}).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='POST', headers={
        'xi-api-key': api_key, 'Content-Type': 'application/json', 'Accept': 'audio/pcm'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except Exception as exc:  # network hiccup / 429: retry briefly
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def write_wav(path, pcm):
    with wave.open(str(path), 'wb') as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(pcm)


def synthesize_scenes(sentences, cache):
    api_key = os.environ['ELEVENLABS_API_KEY']
    cache = Path(cache)
    cache.mkdir(exist_ok=True)
    for i, text in enumerate(sentences):
        write_wav(cache / f'speech-{i:03}.wav', tts_pcm(text, api_key))


def synthesize_whole(text, out):
    write_wav(out, tts_pcm(text, os.environ['ELEVENLABS_API_KEY']))


if __name__ == '__main__':
    root = Path(sys.argv[1]).resolve()
    if '--whole' in sys.argv:
        synthesize_whole((root / 'narration.txt').read_text(encoding='utf-8').strip(), root / 'narration.wav')
    else:
        data = json.loads((root / 'storyboard.json').read_text(encoding='utf-8'))
        synthesize_scenes([s['speech'] for s in data['scenes']], root / '.render-cache')
