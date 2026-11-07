import json, sys, subprocess, os, tempfile
import mlx_whisper
src, out = sys.argv[1], sys.argv[2]
chunks = [(0,12),(10,24),(22,36),(34,48),(46,58),(56,66.9)]
allw = []
for a,b in chunks:
    t = tempfile.mktemp(suffix='.wav')
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',src,t],check=True)
    r = mlx_whisper.transcribe(t, path_or_hf_repo='mlx-community/whisper-large-v3-turbo', word_timestamps=True, language='hi', condition_on_previous_text=False)
    for seg in r['segments']:
        for w in seg.get('words',[]):
            allw.append({'w':w['word'].strip(),'s':round(w['start']+a,2),'e':round(w['end']+a,2),'chunk':a})
json.dump(allw, open(out,'w'), ensure_ascii=False, indent=0)
for a,b in chunks:
    print(f'--- {a}-{b}:', ' '.join(f"{w['s']:.1f}:{w['w']}" for w in allw if w['chunk']==a))
