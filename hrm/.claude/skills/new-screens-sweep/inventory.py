#!/usr/bin/env python3
"""
Kiểm kê "màn MỚI" của hrm-client để rà/sửa đồng loạt theo 1 quy tắc chung mà không sót.

Màn MỚI = file .vue (pages/ hoặc components/) có dùng component <V2Base*>.
Đây là dấu hiệu duy nhất đáng tin: màn dự án + màn chuyển đổi ERP->HRM đều dựng trên V2Base,
màn cũ thì không — KHÔNG suy theo tên phân hệ (human/, timesheet/, meeting/ cũng có màn mới).

Phân loại mỗi file (1 file có thể nhiều loại):
  list   có <V2BaseDataTable>                     -> màn danh sách / tab danh sách / popup chọn có bảng
  table  có V2Base nhưng bảng tự viết (<table>/<b-table>) -> VÙNG XÁM: bảng con trong form, popup chọn phiếu
  form   có ô nhập V2Base (Input/Select/DatePicker/Textarea/Currency/...) -> form thêm/sửa, popup nhập liệu
  modal  có <V2BaseModal> / <b-modal>
  print  file print.vue
  other  còn lại (chi tiết, dashboard...)

Cách dùng (chạy từ bất kỳ đâu):
  python3 inventory.py                               # toàn bộ màn mới, gom theo phân hệ
  python3 inventory.py --kind list                   # chỉ màn có V2BaseDataTable
  python3 inventory.py --kind list,table --has "Người tạo|Người cập nhật"   # phạm vi 1 task
  python3 inventory.py --kind list --has "Người tạo" --lacks "created_by_name"  # VERIFY: còn file chưa sửa
  python3 inventory.py --kind list --order "title: 'Người tạo';;title: 'Người cập nhật'"  # sai thứ tự cột
  python3 inventory.py --kind list --be            # kèm Controller BE (dò Routes/*.php)
  python3 inventory.py --kind list --format checklist > /tmp/scope.md   # checklist dán vào plan.md
  python3 inventory.py --root ../worktrees/gop_db-client                # quét worktree khác
  python3 inventory.py --format json                                    # cho script khác / subagent

--has / --lacks là regex Python, so khớp trên NỘI DUNG file (dùng cờ re.S).
Mỗi dòng kết quả kèm: route để mở bằng Playwright, trang cha import nó (với component/tab/modal),
và các endpoint API mà file gọi (để lần sang BE: Modules/*/Routes/*.php -> Controller -> Resource).
"""
import argparse
import json
import os
import re
import signal
import sys
from collections import OrderedDict, defaultdict

INPUT_TAGS = ('V2BaseInput', 'V2BaseSelect', 'V2BaseSelectInModal', 'V2BaseSelectRemote',
              'V2BaseDatePicker', 'V2BaseTextarea', 'V2BaseCurrencyInput', 'V2BaseCodeInput',
              'V2BaseCheckbox', 'V2BaseRadio', 'V2BaseFile', 'V2BasePickerField', 'V2BaseImageField')
KIND_ORDER = ('list', 'table', 'form', 'modal', 'print', 'other')

RE_V2 = re.compile(r'<V2Base[A-Z]')
RE_DT = re.compile(r'<V2BaseDataTable\b')
RE_RAW_TABLE = re.compile(r'<table\b|<b-table\b')
RE_INPUT = re.compile(r'<(?:%s)\b' % '|'.join(INPUT_TAGS))
RE_MODAL = re.compile(r'<V2BaseModal\b|<b-modal\b|<BaseModal\b')
# dispatch('apiGetMethod', `assign/x?...`) | dispatch('apiPostMethod', { url: 'finance/x', ... })
RE_API = re.compile(r"dispatch\(\s*['\"]api[A-Za-z]*['\"]\s*,\s*(?:\{[^}]*?url\s*:\s*)?[`'\"]([^`'\"]+)[`'\"]", re.S)
RE_URL_KEY = re.compile(r"\burl\s*:\s*[`'\"]([a-z][\w\-]*/[^`'\"]+)[`'\"]")
RE_AXIOS = re.compile(r"\$axios\.\$?(?:get|post|put|delete|patch)\(\s*[`'\"]([^`'\"]+)[`'\"]")
RE_IMPORT = re.compile(r"import\s+\w+\s+from\s+['\"]([^'\"]+)['\"]")


def find_root(arg):
    """--root > $HRM_CLIENT > dò ngược từ thư mục đang đứng (chính nó, hoặc <cha>/hrm-client)."""
    def ok(d):
        return os.path.isdir(os.path.join(d, 'pages')) and os.path.isdir(os.path.join(d, 'components'))
    for d in (arg, os.environ.get('HRM_CLIENT')):
        if d:
            if ok(d):
                return os.path.abspath(d)
            sys.exit('Không phải thư mục hrm-client: %s' % d)
    d = os.path.abspath(os.getcwd())
    while True:
        for cand in (d, os.path.join(d, 'hrm-client')):
            if ok(cand) and os.path.isfile(os.path.join(cand, 'nuxt.config.js')):
                return cand
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    sys.exit('Không tìm thấy hrm-client. Đứng trong HRM/ hoặc hrm-client/, hoặc truyền --root <path>.')


def clean_api(path):
    path = path.split('\n')[0]
    path = re.sub(r'\$\{[^}]*\}', '{x}', path)   # template literal -> {x}
    path = re.sub(r'\$\{.*$', '', path)           # template chưa đóng (nhiều dòng)
    path = re.sub(r'(?<!/)\{x\}.*$', '', path)      # ${query} dính đuôi -> bỏ
    path = path.split('?')[0].strip().strip('/')
    if not re.match(r'^[a-z][\w\-]*/', path):
        return None
    return path


_ROUTE_CACHE = {}


def be_controllers(api_root, path):
    """Dò tĩnh trong Routes/*.php: group prefix khớp tài nguyên chính -> các Controller trong group.
    Chỉ là GỢI Ý để lần sang BE (route:list hay vỡ vì 1 controller thiếu là sập cả lệnh)."""
    seg = [x for x in path.split('/') if x and x != '{x}']
    if len(seg) < 2:
        return []
    mod, res = seg[0], seg[1]
    files = []
    mdir = os.path.join(api_root, 'Modules')
    if os.path.isdir(mdir):
        for m in os.listdir(mdir):
            if m.lower() == mod.lower().replace('-', ''):
                rd = os.path.join(mdir, m, 'Routes')
                files += [os.path.join(rd, f) for f in sorted(os.listdir(rd)) if f.endswith('.php')] if os.path.isdir(rd) else []
    if not files:
        rd = os.path.join(api_root, 'routes')
        files = [os.path.join(rd, f) for f in ('api.php',) if os.path.isfile(os.path.join(rd, f))]
    pat = re.compile(r"prefix['\"]?\s*(?:=>|\()\s*['\"]/?(?:%s/)?%s['\"]" % (re.escape(mod), re.escape(res)))
    found = []
    for f in files:
        if f not in _ROUTE_CACHE:
            with open(f, encoding='utf-8', errors='ignore') as fh:
                _ROUTE_CACHE[f] = fh.read().split('\n')
        lines = _ROUTE_CACHE[f]
        for i, line in enumerate(lines):
            if pat.search(line):
                # đọc đúng khối function(){...} của group (đếm ngoặc), không tràn sang group kế
                depth, buf, started = 0, [], False
                for ln in lines[i:i + 400]:
                    buf.append(ln)
                    depth += ln.count('{') - ln.count('}')
                    started = started or '{' in ln
                    if started and depth <= 0:
                        break
                block = '\n'.join(buf)
                for c in re.findall(r'(\w+Controller)(?:::class|@)', block):
                    if c not in found:
                        found.append(c)
                break
        if found:
            break
    return found[:3]


def route_of(rel):
    """pages/assign/tasks/_id/edit.vue -> /assign/tasks/{id}/edit"""
    if not rel.startswith('pages/'):
        return None
    p = rel[len('pages/'):-len('.vue')]
    parts = [('{%s}' % s[1:]) if s.startswith('_') else s for s in p.split('/')]
    if parts and parts[-1] == 'index':
        parts = parts[:-1]
    return '/' + '/'.join(parts)


def is_page_route(rel):
    """File nằm trong pages/ nhưng ở thư mục components/ thì không phải route."""
    return rel.startswith('pages/') and '/components/' not in rel


def module_of(rel):
    seg = rel.split('/')
    if seg[0] == 'pages':
        return seg[1] if len(seg) > 2 else '(root)'
    return 'components/' + (seg[1] if len(seg) > 2 else '')


def main():
    if hasattr(signal, 'SIGPIPE'):
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # cho phép | head
    ap = argparse.ArgumentParser(description='Kiểm kê màn MỚI (V2Base) của hrm-client')
    ap.add_argument('--root', help='Thư mục hrm-client (mặc định tự dò)')
    ap.add_argument('--kind', help='Lọc loại, phẩy: list,table,form,modal,print,other')
    ap.add_argument('--module', help='Lọc phân hệ (regex trên đường dẫn), vd "finance|assign"')
    ap.add_argument('--has', help='Regex: chỉ giữ file có nội dung khớp')
    ap.add_argument('--lacks', help='Regex: chỉ giữ file KHÔNG khớp (dùng để verify còn file chưa sửa)')
    ap.add_argument('--order', help='"REGEX_A;;REGEX_B": chỉ giữ file mà B xuất hiện TRƯỚC A (vi phạm thứ tự). Vd cột người tạo phải trước người cập nhật')
    ap.add_argument('--include-old', action='store_true', help='Tính cả file KHÔNG dùng V2Base (màn cũ)')
    ap.add_argument('--be', action='store_true', help='Kèm Controller BE đoán từ endpoint (dò Routes/*.php của hrm-api cạnh hrm-client)')
    ap.add_argument('--format', choices=('table', 'checklist', 'json', 'paths'), default='table')
    a = ap.parse_args()

    root = find_root(a.root)
    files = []
    for top in ('pages', 'components'):
        for r, dirs, fs in os.walk(os.path.join(root, top)):
            dirs[:] = [d for d in dirs if d not in ('node_modules', '.nuxt')]
            for f in fs:
                if f.endswith('.vue'):
                    full = os.path.join(r, f)
                    rel = os.path.relpath(full, root).replace(os.sep, '/')
                    # bỏ chính các component nền V2Base* — chúng là gốc, sửa riêng
                    if rel.startswith('components/') and os.path.basename(rel).startswith('V2Base'):
                        continue
                    files.append(rel)

    src = {}
    for rel in files:
        with open(os.path.join(root, rel), encoding='utf-8', errors='ignore') as fh:
            src[rel] = fh.read()

    # đồ thị import ngược: component -> các file import nó
    known = set(files)

    def resolve(importer, imp):
        if imp.startswith(('@/', '~/')):
            p = imp[2:]
        elif imp.startswith('.'):
            p = os.path.normpath(os.path.join(os.path.dirname(importer), imp)).replace(os.sep, '/')
        else:
            return None
        for cand in (p, p + '.vue', p + '/index.vue'):
            if cand in known:
                return cand
        return None

    imported_by = defaultdict(set)
    for rel, s in src.items():
        for imp in RE_IMPORT.findall(s):
            target = resolve(rel, imp)
            if target and target != rel:
                imported_by[target].add(rel)

    def owner_routes(rel, seen=None):
        """Đi ngược import tới file route gần nhất (để biết mở màn nào mà test)."""
        if is_page_route(rel):
            return {route_of(rel)}
        seen = seen or set()
        out = set()
        for parent in imported_by.get(rel, ()):
            if parent in seen:
                continue
            seen.add(parent)
            out |= owner_routes(parent, seen)
        return out

    re_has = re.compile(a.has, re.S) if a.has else None
    re_lacks = re.compile(a.lacks, re.S) if a.lacks else None
    want_kind = set(a.kind.split(',')) if a.kind else None
    re_mod = re.compile(a.module) if a.module else None
    order = None
    if a.order:
        pa, pb = a.order.split(';;', 1)
        order = (re.compile(pa, re.S), re.compile(pb, re.S))

    rows = []
    for rel in sorted(files):
        s = src[rel]
        is_new = bool(RE_V2.search(s))
        if not is_new and not a.include_old:
            continue
        kinds = []
        if RE_DT.search(s):
            kinds.append('list')
        elif is_new and RE_RAW_TABLE.search(s):
            kinds.append('table')
        if RE_INPUT.search(s):
            kinds.append('form')
        if RE_MODAL.search(s):
            kinds.append('modal')
        if rel.endswith('/print.vue'):
            kinds.append('print')
        if not kinds:
            kinds.append('other')
        if want_kind and not (want_kind & set(kinds)):
            continue
        if re_mod and not re_mod.search(rel):
            continue
        if re_has and not re_has.search(s):
            continue
        if re_lacks and re_lacks.search(s):
            continue
        if order:
            ma, mb = order[0].search(s), order[1].search(s)
            if not (ma and mb and mb.start() < ma.start()):
                continue
        apis = []
        for raw in RE_API.findall(s) + RE_URL_KEY.findall(s) + RE_AXIOS.findall(s):
            c = clean_api(raw)
            if c and c not in apis:
                apis.append(c)
        ctrls = []
        if a.be:
            api_root = os.path.join(os.path.dirname(root), 'hrm-api')
            for ap_ in apis[:6]:
                for c in be_controllers(api_root, ap_):
                    if c not in ctrls:
                        ctrls.append(c)
        rows.append(OrderedDict(
            file=rel,
            module=module_of(rel),
            kinds=kinds,
            new=is_new,
            route=route_of(rel) if is_page_route(rel) else None,
            used_in=sorted(r for r in owner_routes(rel) if r),
            apis=apis,
            controllers=ctrls,
        ))

    if a.format == 'json':
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if a.format == 'paths':
        print('\n'.join(r['file'] for r in rows))
        return

    groups = OrderedDict()
    for r in sorted(rows, key=lambda x: (x['module'], x['file'])):
        groups.setdefault(r['module'], []).append(r)

    count = defaultdict(int)
    for r in rows:
        for k in r['kinds']:
            count[k] += 1
    summary = ' · '.join('%s=%d' % (k, count[k]) for k in KIND_ORDER if count[k])
    filt = ' '.join(x for x in (
        a.kind and '--kind ' + a.kind, a.module and '--module "%s"' % a.module,
        a.has and '--has "%s"' % a.has, a.lacks and '--lacks "%s"' % a.lacks,
        a.order and '--order "%s"' % a.order) if x)

    print('# Kiểm kê màn mới — %d file (%s)' % (len(rows), summary or 'rỗng'))
    print('root: %s%s\n' % (root, ('  ·  lọc: ' + filt) if filt else ''))
    for mod, items in groups.items():
        print('## %s (%d)' % (mod, len(items)))
        for r in items:
            where = r['route'] or ('trong ' + ', '.join(r['used_in'][:3]) if r['used_in'] else 'chưa thấy nơi dùng')
            api = (' · API: ' + ', '.join(r['apis'][:4]) + (' …' if len(r['apis']) > 4 else '')) if r['apis'] else ''
            if r['controllers']:
                api += ' · BE: ' + ', '.join(r['controllers'][:4])
            box = '- [ ] ' if a.format == 'checklist' else '- '
            print('%s`%s` [%s] → %s%s' % (box, r['file'], ','.join(r['kinds']), where, api))
        print()


if __name__ == '__main__':
    main()
