# Đẩy out/<id>.docx đè lên Drive theo ID (giữ link). Chặn nếu ModTime trên Drive khác lúc tải.
import json,subprocess,urllib.request,time,hashlib,sys,os
L={x['id']:x for x in json.load(open('srs_list.json'))}
ids=sys.argv[1:]
subprocess.run(['rclone','about','gdrive:'],capture_output=True)
c=json.loads(subprocess.run(['rclone','config','dump'],capture_output=True,text=True).stdout)
T=json.loads(c['gdrive']['token'])['access_token']
log=json.load(open('push_log.json')) if os.path.exists('push_log.json') else []
for id in ids:
    x=L[id]; h={'Authorization':'Bearer '+T}
    if 'google-apps' in x.get('mime',''): print('BỎ QUA Google Doc gốc',x['name']); continue
    time.sleep(3)
    for k in range(6):
        try:
            meta=json.load(urllib.request.urlopen(urllib.request.Request(f'https://www.googleapis.com/drive/v3/files/{id}?fields=modifiedTime&supportsAllDrives=true',headers=h))); break
        except Exception as e: print('chờ',e); time.sleep(10*(k+1))
    if meta['modifiedTime']!=x['mod']:
        print('BỎ QUA (Drive vừa đổi)',x['name'],meta['modifiedTime'],'≠',x['mod']); continue
    data=open(f'out/{id}.docx','rb').read()
    for k in range(6):
        try:
            r=urllib.request.Request(f'https://www.googleapis.com/upload/drive/v3/files/{id}?uploadType=media&supportsAllDrives=true&fields=id,md5Checksum,modifiedTime',data=data,method='PATCH',headers={**h,'Content-Type':'application/vnd.openxmlformats-officedocument.wordprocessingml.document'})
            res=json.load(urllib.request.urlopen(r)); break
        except Exception as e: print('thử lại',x['name'],e); time.sleep(15*(k+1))
    ok=res['md5Checksum']==hashlib.md5(data).hexdigest()
    print('OK' if ok else 'LỆCH MD5',x['name'],res['modifiedTime'],flush=True)
    log.append({'id':id,'name':x['name'],'mod':res['modifiedTime'],'md5ok':ok})
    x['mod']=res['modifiedTime']
    json.dump(log,open('push_log.json','w'),ensure_ascii=False,indent=1)
json.dump(list(L.values()),open('srs_list.json','w'),ensure_ascii=False,indent=1)
