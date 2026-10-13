import json,subprocess,urllib.request,time,os,sys
L=json.load(open('srs_list.json'))
subprocess.run(['rclone','about','gdrive:'],capture_output=True)
c=json.loads(subprocess.run(['rclone','config','dump'],capture_output=True,text=True).stdout)
T=json.loads(c['gdrive']['token'])['access_token']; h={'Authorization':'Bearer '+T}
def get(url):
    for k in range(8):
        try: return urllib.request.urlopen(urllib.request.Request(url,headers=h)).read()
        except Exception as e:
            print('  chờ',e); time.sleep(8*(k+1))
    raise SystemExit('fail '+url)
for x in L:
    if x.get('mod') and os.path.exists(f"drive/{x['id']}.docx") and '--force' not in sys.argv: continue
    m=json.loads(get(f"https://www.googleapis.com/drive/v3/files/{x['id']}?fields=id,name,mimeType,modifiedTime,size,lastModifyingUser(displayName)&supportsAllDrives=true"))
    x.update(mime=m['mimeType'],mod=m['modifiedTime'],dname=m['name'],who=m.get('lastModifyingUser',{}).get('displayName'))
    if 'google-apps' in m['mimeType']:
        url=f"https://www.googleapis.com/drive/v3/files/{x['id']}/export?mimeType=application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        url=f"https://www.googleapis.com/drive/v3/files/{x['id']}?alt=media&supportsAllDrives=true"
    open(f"drive/{x['id']}.docx",'wb').write(get(url))
    print(x['part'],x['name'][:40],m['mimeType'][-12:],m['modifiedTime'][:16],x['who'],flush=True)
    json.dump(L,open('srs_list.json','w'),ensure_ascii=False,indent=1)
    time.sleep(1.5)
