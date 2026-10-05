import json, sys, urllib.request
S='/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs/.auth_state.json'
TOK=[i['value'] for o in json.load(open(S))['origins'] for i in o['localStorage'] if i['name']=='access_token'][0]
def call(method, path, body=None):
    req=urllib.request.Request('http://127.0.0.1:8003/api/v1/'+path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={'Authorization':'Bearer '+TOK,'Content-Type':'application/json','Accept':'application/json'})
    try:
        with urllib.request.urlopen(req) as r: return r.status, json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e: return e.code, e.read().decode()[:2000]
if __name__=='__main__':
    m,p=sys.argv[1],sys.argv[2]; b=json.loads(sys.argv[3]) if len(sys.argv)>3 else None
    st,res=call(m,p,b); print(st); print(json.dumps(res,ensure_ascii=False)[:3000] if not isinstance(res,str) else res)
