"""Hạ tầng e2e Phase 3 (GAP 0308) — API :8003, FE :3002, DB local_hrm_erp. Token đọc từ E2E_TOKEN_DIR
(tok.txt = namdangit id 13 có đủ quyền, tok_cannt.txt = cannt.kd1 id 25 không quyền "Quản lý BOM mẫu")."""
import json, os, subprocess, urllib.request

TOKEN_DIR = os.environ.get('E2E_TOKEN_DIR', '/private/tmp/claude-501/-Users-manhcuong-Desktop-dns-HRM/48345148-7d74-4a08-868e-521b2108aea7/scratchpad')
API = 'http://127.0.0.1:8003/api/v1/'
FE = 'http://127.0.0.1:3002'
ADMIN_EMAIL, ADMIN_PASS = 'namdangit@gmail.com', '2025Dns@2'
LIMITED_EMAIL, LIMITED_PASS = 'cannt.kd1@tanphat.com', 'Test@123'


def token(name='tok'):
    return open(os.path.join(TOKEN_DIR, name + '.txt')).read().strip()


def api(method, url, payload=None, tok=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + url, data=data, method=method, headers={
        'Authorization': 'Bearer ' + (tok or token()), 'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            raw = r.read()
            ctype = r.headers.get('Content-Type', '')
            return r.status, (json.loads(raw or b'{}') if 'json' in ctype else raw)
    except urllib.error.HTTPError as e:
        b = e.read()
        try:
            return e.code, json.loads(b)
        except Exception:
            return e.code, {'raw': b[:800].decode(errors='ignore')}


def sql(q):
    """Trả list dòng (list chuỗi) — chỉ đọc/ghi DB local."""
    out = subprocess.run(['mysql', '-uroot', 'local_hrm_erp', '-N', '-B', '-e', q], capture_output=True, text=True)
    if out.returncode:
        raise RuntimeError(out.stderr)
    return [ln.split('\t') for ln in out.stdout.strip().split('\n') if ln]


RESULTS = []


def check(name, cond, info=''):
    RESULTS.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name + ('' if cond else '  -> ' + str(info)[:900]), flush=True)


def summary():
    f = [n for n, ok in RESULTS if not ok]
    print(f'\n==== {len(RESULTS) - len(f)}/{len(RESULTS)} PASS')
    for n in f:
        print('  FAIL:', n)
    return not f


def ui_login(page, email=ADMIN_EMAIL, password=ADMIN_PASS):
    page.goto(FE + '/login', wait_until='domcontentloaded', timeout=120000)
    page.wait_for_selector('#emailaddress', timeout=120000)
    page.fill('#emailaddress', email)
    page.fill('input[type=password]', password)
    page.keyboard.press('Enter')
    page.wait_for_url(lambda u: '/login' not in u, timeout=60000)
    # Nuxt còn lưu token + nạp quyền sau khi đổi URL — chuyển trang ngay dễ bị đá về /login (đã gặp)
    page.wait_for_function("() => !!localStorage.getItem('access_token')", timeout=60000)
    page.wait_for_timeout(4000)
    if '/login' in page.url:
        raise RuntimeError('Đăng nhập thất bại: ' + email)


VM_JS = "(m) => Array.from(document.querySelectorAll('*')).map(e => e.__vue__).find(v => v && v.$options && v.$options.methods && v.$options.methods[m])"
