import json, subprocess
t = json.load(open('timeline2.json'))
cuts = [c for c in t['cuts'] if c[1] > c[0]]
dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',t['webm']],capture_output=True,text=True).stdout.strip())
# đoạn giữ lại
keep, pos = [], 0.0
for a, b in sorted(cuts):
    if a > pos: keep.append((pos, a))
    pos = max(pos, b)
keep.append((pos, dur))
def shift(x):  # mốc gốc -> mốc sau khi cắt
    return x - sum(min(b, x) - a for a, b in cuts if a < x)
args = ['ffmpeg','-y','-loglevel','error','-i',t['webm']]
for s in t['timeline']: args += ['-i', s['file']]
fc = []
for k,(a,b) in enumerate(keep):
    fc.append(f"[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS[v{k}]")
fc.append(''.join(f'[v{k}]' for k in range(len(keep))) + f"concat=n={len(keep)}:v=1:a=0[vout]")
labels = []
for k, s in enumerate(t['timeline'], start=1):
    ms = int(round((shift(s['start']) + 0.4) * 1000))
    fc.append(f"[{k}:a]aresample=44100,adelay={ms}|{ms}[a{k}]"); labels.append(f'[a{k}]')
fc.append(''.join(labels) + f"amix=inputs={len(labels)}:normalize=0,volume=1.15,alimiter=limit=0.89:level=false[aout]")
args += ['-filter_complex', ';'.join(fc), '-map','[vout]','-map','[aout]','-c:v','libx264','-preset','medium','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-ac','2','-b:a','192k','-movflags','+faststart','-shortest','huong-dan-phan-quyen.mp4']
subprocess.run(args, check=True)
print('cuts', [(round(a,1), round(b,1)) for a,b in cuts])
print('scene starts', [round(shift(s['start']),1) for s in t['timeline']])
print(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration,size','-of','default=nw=1','huong-dan-phan-quyen.mp4'],capture_output=True,text=True).stdout)
