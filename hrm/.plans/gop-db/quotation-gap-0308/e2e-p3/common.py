"""Hạ tầng e2e Phase 3 (GAP 0308). Token đọc từ E2E_TOKEN_DIR
(tok.txt = namdangit id 13 có đủ quyền, tok_cannt.txt = cannt.kd1 id 25 không quyền "Quản lý BOM mẫu").
E2E_ENV=local (mặc định): API :8003, FE :3002, DB local_hrm_erp, id dữ liệu = LOCAL_IDS.
E2E_ENV=dev: dev-hrm.eteksofts.com, DB hrm_erp_test qua tunnel 127.0.0.1:33306 (mật khẩu ở E2E_DB_PW_FILE),
id dữ liệu đọc từ ids_dev.json do seed_dev.py sinh. TK hạn chế đăng nhập UI bằng token (không đổi mật khẩu người thật)."""
import json, os, subprocess, urllib.request
ENV = os.environ.get('E2E_ENV', 'local')

TOKEN_DIR = os.environ.get('E2E_TOKEN_DIR', '/private/tmp/claude-501/-Users-manhcuong-Desktop-dns-HRM/48345148-7d74-4a08-868e-521b2108aea7/scratchpad' + ('/dev' if os.environ.get('E2E_ENV') == 'dev' else ''))
API = 'https://dev-hrm.eteksofts.com/api/v1/' if ENV == 'dev' else 'http://127.0.0.1:8003/api/v1/'
FE = 'https://dev-hrm.eteksofts.com' if ENV == 'dev' else 'http://127.0.0.1:3002'
HERE = os.path.dirname(os.path.abspath(__file__))
# id dữ liệu test theo môi trường (local: dữ liệu seed_test_data.py trên local_hrm_erp)
LOCAL_IDS = {
    'KH': 210, 'KH_LABEL': 'KH210', 'Q_DEMAND': 219, 'Q_DIRECT': 218, 'Q_EDIT': 218, 'Q_PICK': 217, 'Q_PROJECT': 92,
    'PROJECT': 154, 'Q_GROUPS': 24, 'Q_SPECS': 45, 'Q_VAT': 6, 'BOM': 30, 'P_STOCK': 43508, 'P_LOW': 3900,
    'DEM_OTHER': 3, 'STOCK_CUSTOMER': 21195, 'STOCK_PIDS': [20972, 20973], 'QT_TPL': 3, 'QT_TPL2': 2,
    'QT_NAME': 'Báo giá trạm sạc Schneider', 'QT_NAME2': 'BMW', 'DT_TPL': 2, 'BT_TPL': 1,
    'BT_NAME': 'BOM mẫu khoang sửa chữa', 'MEETING_CODE': 'TPE.MET',
}
IDS = json.load(open(os.path.join(HERE, 'ids_dev.json'))) if ENV == 'dev' and os.path.exists(os.path.join(HERE, 'ids_dev.json')) else LOCAL_IDS
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
    """Trả list dòng (list chuỗi) — DB local, hoặc DB dev hrm_erp_test qua tunnel (E2E_ENV=dev)."""
    if ENV == 'dev':
        pw = open(os.environ.get('E2E_DB_PW_FILE', os.path.join(TOKEN_DIR, '..', 'hrmdb_pw.txt'))).read().strip().strip('"')
        out = subprocess.run(['mysql', '-h127.0.0.1', '-P33306', '-uhrm_tpe', 'hrm_erp_test', '-N', '-B', '-e', q],
                             capture_output=True, text=True, env={**os.environ, 'MYSQL_PWD': pw})
    else:
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
    if ENV == 'dev' and email == LIMITED_EMAIL:
        # dev: không biết / không đổi mật khẩu người thật — nạp token sinh bằng tinker rồi tải lại
        page.goto(FE + '/login', wait_until='domcontentloaded', timeout=120000)
        page.evaluate("(t) => localStorage.setItem('access_token', t)", token('tok_cannt'))
        page.goto(FE + '/', wait_until='domcontentloaded', timeout=120000)
        page.wait_for_timeout(8000)
        if '/login' in page.url:
            raise RuntimeError('Nạp token TK hạn chế thất bại')
        return
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
