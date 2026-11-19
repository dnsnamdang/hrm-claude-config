#!/usr/bin/env python3
"""ui.py <1|2> dump | tap x y | text "..." | swipe x1 y1 x2 y2 | shot name | find "label" """
import json, subprocess, sys, time
M='/Users/dnsnamdang/.npm/_npx/e41f45e886283da6/node_modules/@mobilenext/mobilecli-darwin-arm64/mobilecli-darwin-arm64'
DEV={'1':'D0C0E274-8590-4D39-9196-CD5D535338DD','2':'FE6D3E86-49A0-4D92-AFDD-58C5DAF761BB'}
def run(*a): return subprocess.run([M,*a],capture_output=True,text=True).stdout
def elems(d):
    out=[]
    def walk(o):
        if isinstance(o,dict):
            l=(o.get('label') or o.get('text') or o.get('name') or '').strip()
            r=o.get('rect') or {}
            if l and r: out.append((l.replace('\n',' | '),r.get('x',0),r.get('y',0),r.get('width',0),r.get('height',0),o.get('type','')))
            for v in o.values(): walk(v)
        elif isinstance(o,list):
            for v in o: walk(v)
    walk(json.loads(run('dump','ui','--device',d)))
    return out
if __name__=='__main__':
    dev=DEV[sys.argv[1]]; cmd=sys.argv[2]
    if cmd=='dump':
        seen=set()
        for l,x,y,w,h,t in elems(dev):
            k=(l,x,y)
            if k in seen: continue
            seen.add(k); print(f'{x:>4},{y:<4} {w:>3}x{h:<3} {t[:10]:10} {l[:110]}')
    elif cmd=='tap': run('io','tap',f'{sys.argv[3]},{sys.argv[4]}','--device',dev)
    elif cmd=='text': run('io','text',sys.argv[3],'--device',dev)
    elif cmd=='swipe': run('io','swipe',','.join(sys.argv[3:7]),'--device',dev,*(['--duration',sys.argv[7]] if len(sys.argv)>7 else []))
    elif cmd=='shot':
        subprocess.run(['xcrun','simctl','io',dev,'screenshot',sys.argv[3]],capture_output=True)
        subprocess.run(['sips','-Z','600',sys.argv[3]],capture_output=True)
