import json, os, urllib.request
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN = open(os.path.join(HERE, '..', 'token.txt')).read().strip()
API = 'http://127.0.0.1:8003/api/v1/'
ERP = 'http://127.0.0.1:8001'
FE = 'http://127.0.0.1:3002'

def api(method, url, payload=None, token=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + url, data=data, method=method, headers={
        'Authorization': 'Bearer ' + (token or TOKEN), 'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        b = e.read()
        try:
            return e.code, json.loads(b)
        except Exception:
            return e.code, {'raw': b[:800].decode(errors='ignore')}

def erp_login(ctx):
    p = ctx.new_page()
    p.goto(ERP + '/sso/callback?token=' + TOKEN, wait_until='domcontentloaded', timeout=120000)
    p.goto(ERP + '/admin/select-company/1', wait_until='domcontentloaded', timeout=120000)
    return p

RESULTS = []
def check(name, cond, info=''):
    RESULTS.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name + ('' if cond else '  -> ' + str(info)[:900]), flush=True)

def summary():
    f = [n for n, ok in RESULTS if not ok]
    print(f'\n==== {len(RESULTS) - len(f)}/{len(RESULTS)} PASS')
    for n in f:
        print('  FAIL:', n)
