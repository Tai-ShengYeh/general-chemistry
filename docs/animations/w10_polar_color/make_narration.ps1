Add-Type -AssemblyName System.Speech
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$cache = Join-Path $dir '.render-cache'
New-Item -ItemType Directory -Force -Path $cache | Out-Null
$data = Get-Content -LiteralPath (Join-Path $dir 'storyboard.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice('Microsoft Hanhan Desktop')
$s.Rate = -1
$s.Volume = 100
try {
  for ($i=0; $i -lt $data.scenes.Count; $i++) {
    $out = Join-Path $cache ('speech-{0:D3}.wav' -f $i)
    $s.SetOutputToWaveFile($out)
    $s.Speak($data.scenes[$i].speech)
    $s.SetOutputToNull()
  }
} finally { $s.Dispose() }
