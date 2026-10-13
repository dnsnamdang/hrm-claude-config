# -*- coding: utf-8 -*-
"""SRS: thay ảnh cửa sổ Tùy chỉnh cột + thêm dòng Chọn tất cả / Bỏ chọn hết / Đang chọn x/y vào bảng
Mô tả giao diện và bảng Event của mục đó. python3 srs_edit.py [id…] -> out/<id>.docx"""
import copy, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'hdsd'))
from edit import Doc, NS, W, text, embeds  # noqa

S = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(S, '..', 'hdsd', 'shots') + '/'
CAP = re.compile(r'^\s*Hình\s*\d+\s*[:.]\s*(Cửa sổ|Popup|Hộp)?\s*[“"]?\s*(Tùy|Tuỳ)\s*chỉnh cột', re.I)
ROUTE = {  # theo tên SRS
    'Danh mục serial thiết bị làm dịch vụ': 'customer-care/serials', 'Danh mục tài khoản': 'finance/accounts',
    'Phiếu yêu cầu gia hạn hàng mượn': 'finance/borrow-extend-requests', 'Danh mục Đường-Phố': 'human/hamlets',
    'Phieu huy hang giu': 'finance/prepick-cancels', 'Phiếu chuyển hàng nhập thẳng': 'finance/product-import-direct-transfers',
    'Danh mục khu vực': 'human/areas', 'Danh mục vụ việc': 'finance/works',
    'Danh mục ghi chú kiểm tra bảo dưỡng': 'customer-care/note-maintenances', 'Yêu cầu hủy hàng giữ': 'finance/prepick-cancel-requests',
    'Danh mục tiền tệ': 'finance/currencies', 'Cấp dịch vụ bảo dưỡng': 'customer-care/levels',
    'Danh mục nguồn vốn': 'finance/source-capitals', 'Phiếu đề nghị thanh toán': 'finance/bill-payment-requests',
    'Phiếu chi tiền': 'finance/bill-payments', 'Danh mục loại tài khoản': 'finance/type-accounts',
    'Danh mục ngân hàng': 'human/banks', 'Phiếu xử lý yêu cầu': 'customer-care/warranty-repair-handle-requests',
    'Danh mục tài khoản ngân hàng': 'finance/account-banks', 'Phiếu yêu cầu gia hạn giữ hàng': 'finance/prepick-extend-requests',
    'Danh mục Tỉnh-TP': 'human/provinces', 'Yêu cầu xuất giữ': 'finance/product-prepick-requests',
    'Danh mục dịch vụ sửa chữa và chi phí khác': 'customer-care/costs', 'Phiếu xuất giữ': 'finance/warehouse-prepick-requests',
    'Yêu cầu điều chuyển hàng giữ': 'finance/prepick-transfer-requests', 'Danh mục công việc, lỗi thiết bị': 'customer-care/device-errors',
    'Phiếu thu tiền': 'finance/bill-incomes', 'Danh mục khách hàng': 'assign/customers',
    'Hàng sắp hết hạn giữ': 'finance/prepick-expiring', 'Phiếu đề nghị thu tiền': 'finance/bill-income-requests',
    'Phiếu_báo_có': 'finance/bill-income-reports', 'Phiếu ủy nhiệm chi': 'finance/bill-payment-authorizations',
    'Danh mục mã phí': 'finance/cost-debts', 'Danh mục gói bảo dưỡng': 'customer-care/services',
    'Phiếu yêu cầu chuyển hàng': 'finance/product-transfer-requests', 'Danh sách hàng giữ': 'finance/prepick-stocks',
    'Danh mục quốc gia': 'human/nations', 'Danh mục Phường-Xã': 'human/wards',
    'Yêu cầu kiểm tra sửa chữa - bảo hành': 'customer-care/warranty-repair-requests', 'Danh mục Quận-Huyện': 'human/districts',
}
NAMES = {}
for l in open(S + '/ids.txt'):
    p = l.split()
    NAMES[p[0]] = ' '.join(p[2:])


def nfc(s):
    return unicodedata.normalize('NFC', s)


def set_cell(tc, lines):
    ps = tc.findall('w:p', NS)
    for p in ps[1:]:
        tc.remove(p)
    tpl = ps[0]
    prev = None
    for i, line in enumerate(lines):
        p = tpl if i == 0 else copy.deepcopy(tpl)
        runs = p.findall('w:r', NS)
        r0 = next((r for r in runs if r.find('w:t', NS) is not None), runs[0] if runs else None)
        for c in list(p):
            if c.tag != W + 'pPr':
                p.remove(c)
        nr = copy.deepcopy(r0) if r0 is not None else etree_el('r')
        for c in list(nr):
            if c.tag != W + 'rPr':
                nr.remove(c)
        t = nr.makeelement(W + 't', {})
        t.text = line
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        nr.append(t)
        p.append(nr)
        if i:
            prev.addnext(p)
        prev = p


def etree_el(tag):
    from lxml import etree
    return etree.Element(W + tag)


def cells(tr):
    return tr.findall('w:tc', NS)


def renumber(tbl):
    n = 0
    for tr in tbl.findall('w:tr', NS)[1:]:
        c0 = cells(tr)[0]
        if re.fullmatch(r'\s*\d+\s*', text(c0)):
            n += 1
            set_cell(c0, [str(n)])


def process(id):
    name = nfc(NAMES[id].replace('SRS - ', '').replace('.docx', ''))
    route = ROUTE[name]
    d = Doc(S + '/orig/%s.docx' % id)
    kids = list(d.body)
    caps = [i for i, k in enumerate(kids) if k.tag == W + 'p' and CAP.match(text(k)) and i > 1
            and (embeds(kids[i - 1]) or embeds(kids[i - 2]))]
    if not caps:
        return None, 'KHÔNG THẤY CHÚ THÍCH'
    c = caps[-1]
    m = next(k for k in (c - 1, c - 2) if embeds(kids[k]))
    shot = SHOTS + route.replace('/', '__') + '.png'
    if not os.path.exists(shot):
        return None, 'THIẾU ẢNH ' + route
    d.set_blip(kids[m], shot, keep='cx')
    notes = ['ảnh']

    tbls = []
    for k in kids[c + 1:c + 8]:
        tbls += [k] if k.tag == W + 'tbl' else k.findall('.//w:tbl', NS)
    ui = next((t for t in tbls if 'Tên đối tượng' in text(t.find('w:tr', NS))), None)
    ev = next((t for t in tbls if 'Event' in text(t.find('w:tr', NS)) or 'event' in text(t.find('w:tr', NS))), None)
    if ui is not None:
        hdr = [text(x).strip() for x in cells(ui.find('w:tr', NS))]
        rows = ui.findall('w:tr', NS)[1:]
        luu = next((r for r in rows if re.search(r'(?i)\bLưu\b', text(cells(r)[1]))), rows[-1])
        chung = bool(re.search(r'(?i)bộ lọc|ô lọc', text(ui)))
        new = []
        spec = [('Nút Chọn tất cả', 'Button', 'Enable', 'Hiển thị',
                 'Nằm phía trên danh sách cột. Tích tất cả các cột; chưa áp dụng lên bảng cho tới khi bấm Lưu.'),
                ('Nút Bỏ chọn hết', 'Button', 'Enable', 'Hiển thị',
                 'Bỏ tích tất cả các cột không bắt buộc; cột bắt buộc (có biểu tượng ổ khóa) vẫn luôn hiển thị.'),
                ('Số cột đang chọn', 'Label', 'Read-only', 'Đang chọn x/y cột',
                 'Góc trái cuối cửa sổ, cập nhật ngay khi tích / bỏ tích hoặc bấm Chọn tất cả / Bỏ chọn hết.')]
        co_san = [text(cells(r)[1]) for r in rows]
        for ten, loai, tt, gt, mt in spec:
            if any(ten.replace('Nút ', '') in x for x in co_san):
                continue
            r = copy.deepcopy(luu)
            cs = cells(r)
            for j, h in enumerate(hdr):
                if j == 0:
                    continue
                if 'Tên' in h:
                    set_cell(cs[j], [ten])
                elif h.startswith('Loại'):
                    set_cell(cs[j], [loai])
                elif 'Trạng thái' in h:
                    set_cell(cs[j], [tt])
                elif 'ban đầu' in h:
                    set_cell(cs[j], [gt])
                elif 'Mô tả' in h:
                    set_cell(cs[j], [('Chỉ có ở cửa sổ Tùy chỉnh cột. ' if chung else '') + mt])
                elif 'Bắt buộc' in h or 'Phạm vi' in h:
                    set_cell(cs[j], ['–'])
            new.append(r)
        anchor = luu
        for r in new:
            anchor.addprevious(r)
        renumber(ui)
        notes.append('bảng giao diện +3')
    if ev is not None and 'Chọn tất cả' in text(ev):
        ev = None
    if ev is not None:
        rows = ev.findall('w:tr', NS)[1:]
        luu = next((r for r in rows if re.search(r'(?i)Bấm\s*(nút\s*)?[“"]?Lưu', text(cells(r)[1]))), None)
        r = copy.deepcopy(luu if luu is not None else rows[-1])
        cs = cells(r)
        set_cell(cs[1], ['Bấm Chọn tất cả / Bỏ chọn hết'])
        set_cell(cs[2], ['Click'])
        set_cell(cs[3], ['After:', '– Chọn tất cả: tích tất cả các cột.',
                         '– Bỏ chọn hết: bỏ tích các cột không bắt buộc; cột bắt buộc giữ nguyên.',
                         '– Cập nhật dòng “Đang chọn x/y cột”; bảng chưa đổi cho tới khi bấm Lưu.'])
        if luu is not None:
            luu.addprevious(r)
        else:
            rows[-1].addnext(r)
        renumber(ev)
        notes.append('bảng event +1')
    return d, ', '.join(notes)


if __name__ == '__main__':
    os.makedirs(S + '/out', exist_ok=True)
    ids = sys.argv[1:] or [os.path.basename(f)[:-5] for f in sorted(os.listdir(S + '/orig')) if f.endswith('.docx')]
    for id in ids:
        id = id.replace('.docx', '')
        try:
            d, msg = process(id)
            if d is not None:
                d.save(S + '/out/%s.docx' % id)
        except Exception as ex:
            import traceback; traceback.print_exc()
            msg = 'LỖI ' + repr(ex)
        print(id, NAMES[id], '|', msg)
