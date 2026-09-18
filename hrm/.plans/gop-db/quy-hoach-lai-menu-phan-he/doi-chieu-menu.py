# -*- coding: utf-8 -*-
"""
Đối chiếu TỰ ĐỘNG: mọi chức năng trong sheet quy hoạch (bỏ mục gạch ngang) đã có trong menu
của phân hệ tương ứng chưa.

- Nguồn tài liệu: book.xlsx (5 sheet), cột D "Chức năng" + E "Chức năng nhỏ", forward-fill cột C.
- Nguồn menu: các file menu trong hrm-client (lấy mọi nhãn: label / title / n / chuỗi trong screens).
- So khớp mềm: bỏ dấu, bỏ ngoặc, bỏ dấu câu; coi là CÓ nếu một chuỗi chứa chuỗi kia.
"""
import re, unicodedata, openpyxl, os, sys

# Chạy:  python doi-chieu-menu.py [đường-dẫn-hrm-client] [đường-dẫn-book.xlsx]
#
# Tải tài liệu trước khi chạy (sheet quy hoạch phân hệ, chốt 04/09/2026):
#   curl -sL -o book.xlsx "https://docs.google.com/spreadsheets/d/1s8fb8lWuP6o4LjUcwk77Wkh5nx0x8tkq9dNeV1P41tg/export?format=xlsx"
#
# Cần `pip install openpyxl` — bản .xlsx đọc được GẠCH NGANG (mục đã bỏ) và MÀU NỀN,
# CSV thì không. Mục bị gạch ngang được loại khỏi phép đối chiếu.
WT = sys.argv[1] if len(sys.argv) > 1 else 'D:\\CompanyProject\\hrm\\hrm-client\\.worktrees\\gop-db'
BOOK = sys.argv[2] if len(sys.argv) > 2 else 'book.xlsx'

# phân hệ trong sheet -> (khoá, danh sách file menu, tên export nếu file có nhiều export)
MAP = {
    'Thông tin nhân sự': ('human', ['components/menu.js'], 'menuItemsHuman'),
    'Danh mục dùng chung': ('master-data', ['components/subsystem-menu/master-data.js'], None),
    'Quản trị hệ thống': ('admin', ['components/subsystem-menu/admin.js'], None),
    'Chấm công': ('timesheet', ['components/menu.js'], 'menuItemsTimeSheet'),
    'Quản lý cơm': ('rice', ['components/default-menu/rice.js'], None),
    'Tính lương': ('payroll', ['components/menu.js'], 'menuItemsPayroll'),
    'Bảo hiểm': ('insurance', ['components/subsystem-menu/insurance.js'], None),
    'Thuế TNCN': ('tax', ['components/subsystem-menu/tax.js'], None),
    'Tuyển dụng': ('recruitment', ['components/subsystem-menu/recruitment.js'], None),
    'Đánh giá KPI': ('kpi', ['components/subsystem-menu/kpi.js'], None),
    'Hoạt động pháp lý': ('legal', ['components/subsystem-menu/legal.js'], None),
    'Quản lý tài sản': ('asset', ['components/subsystem-menu/asset.js'], None),
    'Hoạt động ISO (QUẢN LÝ QUY TRÌNH)': ('iso', ['components/subsystem-menu/iso.js'], None),
    'Quản lý an toàn 5s': ('safety-5s', ['components/subsystem-menu/safety-5s.js'], None),
    'Ban hành văn bản nội bộ (Quyết định - quy định - quy chế)': (
        'operation', ['components/subsystem-menu/operation-hub.js'], None),
    'Ban hành văn bản nội bộ': ('decision', ['components/default-menu/decision.js'], None),
    'Đào tạo - đánh giá': ('training', ['components/menu-sidebar.js'], 'menuItemsTraining'),
    'Quản lý công việc': ('assign', ['components/menu-sidebar.js'], 'menuItemsAssign'),
    'Meeting': ('meeting', ['components/subsystem-menu/meeting.js'], None),
    'Quản lý sản xuất': ('production', ['components/subsystem-menu/production.js'], None),
    'Mua hàng': ('purchase', ['components/subsystem-menu/purchase.js'], None),
    'Kho': ('warehouse', ['components/subsystem-menu/warehouse.js'], None),
    'Vận chuyển': ('transport', ['components/subsystem-menu/transport.js'], None),
    'Tra cứu - thông báo': ('lookup', ['components/subsystem-menu/lookup.js'], None),
    'Quản lý CSKH trước khi bán': ('presale', ['components/subsystem-menu/presale.js'], None),
    'Quản lý Bán hàng': ('sale', ['components/subsystem-menu/sale-hub.js'], None),
    'CRM': ('customer-care', ['components/subsystem-menu/customer-care.js'], None),
    'Tài chính': ('finance', ['components/subsystem-menu/finance.js'], None),
}

EXPORT_ORDER = {
    'components/menu.js': ['menuItemsHuman', 'menuItemsTimeSheet', 'menuItemsPayroll'],
    'components/menu-sidebar.js': ['menuItemsAssign', 'menuItemsTraining'],
}


def chuan(s):
    s = str(s or '')
    s = s.split('\n')[0]
    s = re.sub(r'\(.*?\)', ' ', s)                      # bỏ phần trong ngoặc
    s = re.sub(r'(?i)t[êe]n c[uũ].*', ' ', s)           # bỏ "tên cũ: ..."
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.replace('đ', 'd').replace('Đ', 'D')
    s = re.sub(r'[^a-zA-Z0-9]+', ' ', s).strip().lower()
    return re.sub(r'\s+', ' ', s)


def nhan_menu(path, export=None):
    src = open(os.path.join(WT, path), encoding='utf-8').read()
    if export:
        order = EXPORT_ORDER.get(path, [])
        if export in order:
            i = src.index('export const ' + export)
            nxt = [src.index('export const ' + e) for e in order if e != export and src.find('export const ' + e) > i]
            src = src[i:min(nxt) if nxt else len(src)]
    labels = []
    for m in re.finditer(r"(?:label|title|name|n)\s*:\s*'([^']+)'", src):
        labels.append(m.group(1))
    # chuỗi trần trong mảng screens: [...]
    for m in re.finditer(r"screens:\s*\[(.*?)\]", src, re.S):
        labels += re.findall(r"'([^']+)'", m.group(1))
    return set(filter(None, (chuan(x) for x in labels)))


def doc_sheet():
    wb = openpyxl.load_workbook(BOOK)
    ds = {}
    for ten in ['QUẢN TRỊ LÕI', 'NHÂN SỰ', 'VĂN PHÒNG SỐ', 'SẢN XUẤT - CUNG ỨNG', 'KINH DOANH - TÀI CHÍNH']:
        ws = wb[ten]
        phan_he = None
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=6):
            c_ph, c_cn, c_cnn = row[2], row[3], row[4]
            if c_ph.value and not (c_ph.font and c_ph.font.strike):
                phan_he = str(c_ph.value).split('\n')[0].strip()
            if not phan_he:
                continue
            for cell in (c_cn, c_cnn):
                if cell.value is None:
                    continue
                if cell.font and cell.font.strike:
                    continue           # mục bị gạch = đã bỏ/chuyển đi
                txt = str(cell.value).split('\n')[0].strip()
                if not txt or txt in ('Chức năng', 'Chức năng nhỏ'):
                    continue
                ds.setdefault(phan_he, []).append((cell.row, txt))
    return ds


# Mục tài liệu KHÔNG phải lỗi menu — đã xử lý có lý do, ghi rõ để lần chạy sau còn đối chiếu được.
BO_QUA = {
    # (phân hệ trong sheet, chuẩn(mục)) -> lý do
    ('Quản lý Bán hàng (chuyển sang nền tảng HRM)', 'nhom nganh'): 'đã chuyển sang phân hệ Danh mục dùng chung',
    ('Quản lý Bán hàng (chuyển sang nền tảng HRM)', 'nhom giai phap'): 'đã chuyển sang phân hệ Danh mục dùng chung',
    ('Quản lý Bán hàng (chuyển sang nền tảng HRM)', 'ung dung'): 'đã chuyển sang phân hệ Danh mục dùng chung',
    ('Quản lý Bán hàng (chuyển sang nền tảng HRM)', 'lap dat sc bh'): 'menu khai "Lắp đặt - BH - SC" (đảo thứ tự chữ)',
    ('Quản lý Bán hàng (chuyển sang nền tảng HRM)', 'quy che thiep lap'): 'sheet gõ nhầm, menu có "Quy chế - Thiết lập"',
    ('Đào tạo - đánh giá', 'de xuat dao dao tao can duyet'): 'sheet gõ nhầm "đào đào", menu có "Đề xuất đào tạo cần duyệt"',
    # User chốt 16/09/2026: 3 dòng này trong sheet là ghi tạm cho có, nghiệp vụ chưa chốt phân bổ
    # -> KHÔNG khai vào menu phân hệ Tài chính.
    ('Tài chính', 'quy thu chi'): 'user chốt: tài liệu ghi tạm, chưa phân bổ',
    ('Tài chính', 'bao cao tai chinh'): 'user chốt: tài liệu ghi tạm, chưa phân bổ',
    ('Tài chính', 'bao cao dong tien'): 'user chốt: tài liệu ghi tạm, chưa phân bổ',
}


def bo_qua(ph, t):
    return (ph, t) in BO_QUA


sheet = doc_sheet()
tong_thieu = 0
for ph, muc in sheet.items():
    key = None
    for ten_sheet, (k, files, export) in MAP.items():
        if chuan(ten_sheet) == chuan(ph):
            key, ff, ex = k, files, export
            break
    if not key:
        print('?? KHÔNG MAP ĐƯỢC PHÂN HỆ:', repr(ph[:60]))
        continue
    co = set()
    for f in ff:
        co |= nhan_menu(f, ex)
    thieu = []
    for r, txt in muc:
        t = chuan(txt)
        if not t or len(t) < 3:
            continue
        if any(t == c or t in c or c in t for c in co):
            continue
        if t.startswith('https') or bo_qua(ph, t):
            continue
        thieu.append((r, txt))
    # bỏ trùng
    seen = set()
    thieu = [x for x in thieu if not (chuan(x[1]) in seen or seen.add(chuan(x[1])))]
    tong_thieu += len(thieu)
    dau = 'OK ' if not thieu else 'THIEU'
    print('%s | %-45s | tài liệu %3d mục | thiếu %d' % (dau, ph[:45], len(muc), len(thieu)))
    for r, txt in thieu:
        print('        - dòng %-4s %s' % (r, txt[:80]))
print('\nTỔNG SỐ MỤC THIẾU:', tong_thieu)
