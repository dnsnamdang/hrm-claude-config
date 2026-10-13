import json,subprocess,urllib.request,time,hashlib,sys
base={x['ID']:x['ModTime'][:19] for x in json.load(open('list.json'))}
names={x['ID']:x['Name'] for x in json.load(open('list.json'))}
ids=sys.argv[1:] or list(json.load(open('map.json')))
def tok():
    subprocess.run(['rclone','about','gdrive:'],capture_output=True)
    c=json.loads(subprocess.run(['rclone','config','dump'],capture_output=True,text=True).stdout)
    return json.loads(c['gdrive']['token'])['access_token']
T=tok(); log=[]
for id in ids:
    h={'Authorization':'Bearer '+T}
    time.sleep(3)
    for k in range(6):
        try:
            meta=json.load(urllib.request.urlopen(urllib.request.Request(f'https://www.googleapis.com/drive/v3/files/{id}?fields=modifiedTime,md5Checksum&supportsAllDrives=true',headers=h))); break
        except Exception as e:
            print('chờ',e); time.sleep(10*(k+1))
    if meta['modifiedTime'][:19]!=base[id]:
        print('BỎ QUA (Drive vừa đổi)',names[id],meta['modifiedTime']); continue
    data=open(f'out/{id}.docx','rb').read()
    for k in range(6):
        try:
            r=urllib.request.Request(f'https://www.googleapis.com/upload/drive/v3/files/{id}?uploadType=media&supportsAllDrives=true&fields=id,md5Checksum,modifiedTime',data=data,method='PATCH',headers={**h,'Content-Type':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})
            res=json.load(urllib.request.urlopen(r)); break
        except Exception as e:
            print('thử lại',id,e); time.sleep(15*(k+1))
    ok=res['md5Checksum']==hashlib.md5(data).hexdigest()
    print('OK' if ok else 'LỆCH MD5',names[id],res['modifiedTime']); log.append({'id':id,'name':names[id],'mod':res['modifiedTime'],'md5ok':ok})
json.dump(log,open('push_log.json','w'),ensure_ascii=False,indent=1)
