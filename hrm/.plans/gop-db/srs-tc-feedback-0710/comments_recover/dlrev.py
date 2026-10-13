import json,subprocess,urllib.request,time,os
ids=json.load(open('ids.json'))
subprocess.run(['rclone','about','gdrive:'],capture_output=True)
c=json.loads(subprocess.run(['rclone','config','dump'],capture_output=True,text=True).stdout)
T=json.loads(c['gdrive']['token'])['access_token']; h={'Authorization':'Bearer '+T}
def get(u):
    for k in range(6):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers=h)).read()
        except Exception as e:
            b=e.read().decode()[:160] if hasattr(e,'read') else ''
            print('  wait',k,e,b.replace('\n',' ')); time.sleep(15*(k+1))
    return None
meta={}
for name,id in ids.items():
    v=json.loads(get(f'https://www.googleapis.com/drive/v3/files/{id}/revisions?fields=revisions(id,modifiedTime,lastModifyingUser/displayName)'))
    meta[id]=v['revisions']
    for r in v['revisions']:
        fn=f"revs/{id}_{r['modifiedTime'][:19].replace(':','')}.docx"
        if os.path.exists(fn): continue
        if r['modifiedTime']>'2026-10-07T00': continue
        data=get(f"https://www.googleapis.com/drive/v3/files/{id}/revisions/{r['id']}?alt=media")
        if data: open(fn,'wb').write(data); print('ok',name[:30],r['modifiedTime'][:16],r['lastModifyingUser'].get('displayName'),flush=True)
        time.sleep(3)
json.dump(meta,open('revs/meta.json','w'),ensure_ascii=False,indent=1)
