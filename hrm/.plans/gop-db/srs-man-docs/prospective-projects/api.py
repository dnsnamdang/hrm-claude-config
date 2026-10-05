import json, sys, urllib.request
s = json.load(open('/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/bao-cao-docs/.auth_state.json'))
TOK = [i['value'] for o in s['origins'] for i in o['localStorage'] if i['name'] == 'access_token'][0]
def call(method, path, payload=None):
    req = urllib.request.Request('http://127.0.0.1:8003/api/v1/' + path, method=method,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={'Authorization': 'Bearer ' + TOK, 'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return r.status, json.loads(r.read() or b'null')
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b'null')
if __name__ == '__main__':
    st, d = call(sys.argv[1], sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else None)
    print(st); print(json.dumps(d, ensure_ascii=False)[:3000])
