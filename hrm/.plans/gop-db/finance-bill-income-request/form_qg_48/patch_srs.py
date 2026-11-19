# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu đề nghị thu tiền" (bản Drive tải 28/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Phiếu đề nghị thu tiền.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Chạy lại bao nhiêu lần cũng được: luôn đọc bản Drive gốc. Khuôn chép từ màn 27
(finance-product-import-direct-transfer/form_qg/patch_srs.py); hàm chung ở phieu-theo-form-quoc-gia/formqg_lib.py.
"""
import copy, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
import docx  # noqa: E402
from formqg_lib import *  # noqa: E402,F401
import formqg_lib as L  # noqa: E402
import docxlib  # noqa: E402

SRC = os.path.join(HERE, 'drive_0710', 'SRS_Drive.docx')
OUT_DIR = os.path.join(HERE, 'out')
NAME = 'SRS - Phiếu đề nghị thu tiền'
OUT = os.path.join(OUT_DIR, NAME + '.docx')
UML = os.path.join(HERE, 'uml')
SHOT = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Phiếu đề nghị thu tiền'
# finance.js: hubGroup 'Khởi tạo' > nhóm 'Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi' > mục; lối 2 'Quản lý tiền' > 'Đề nghị'
M1 = 'Phân hệ Tài chính => Khởi tạo => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi => Đề nghị thu tiền'
M2 = 'Phân hệ Tài chính => Quản lý tiền => Đề nghị => Đề nghị thu tiền'
MP = 'Phân hệ Tài chính => Chờ duyệt => Phê duyệt - Công nợ - Thu - Chi => Phiếu đề nghị thu tiền chờ duyệt'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp “Thông tin chưa lưu” với câu “Bạn có thông tin chưa lưu. Có chắc '
           'chắn muốn thoát?” (Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp “Thông tin chưa lưu”; bấm Thoát thì rời màn và bỏ thay đổi, bấm Ở lại '
              'thì giữ nguyên màn và dữ liệu.']
CLOSE_NOASK = '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận; phiếu giữ nguyên.'

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem tất cả phiếu đề nghị thu của tổng công ty / công '
              'ty / phòng ban / bộ phận (V1–V4); không có quyền nào thì chỉ thấy phiếu của mình.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (V1–V4); không có quyền nào vẫn xem được phiếu do chính mình lập.')
ACTOR_OWNER = 'Người lập phiếu — người dùng có quyền thực hiện chức năng: chỉ người đã lập phiếu (chức năng không gắn quyền riêng).'
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Đang tạo hoặc Không duyệt.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu, hoặc người có quyền Xem tất cả phiếu đề nghị thu của '
               'tổng công ty / công ty / phòng ban / bộ phận (V1–V4) trong phạm vi được giao, hoặc Kế toán thanh toán '
               '(Q1) với phiếu chờ duyệt cùng công ty.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Đang tạo chỉ người lập xem được.')
ACTOR_KT = 'Người dùng có quyền Kế toán thanh toán (Q1).'
COND_KT = ('1. Đăng nhập thành công.\n'
           '2. Có quyền Kế toán thanh toán (Q1).\n'
           '3. Phiếu đang ở trạng thái Chờ KT duyệt.')

SECTIONS = {
    r'^2\.1 Xem danh sách': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 Tìm kiếm': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang và quy tắc bộ lọc chọn nhiều giá trị.',
                        ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách hoặc màn chờ duyệt.'),
    r'^2\.3 Cài đặt bộ lọc': ('Cấu hình bộ lọc và Tùy chỉnh cột.', ACTOR_LIST,
                              COND_LIST + '\n3. Đang ở màn danh sách hoặc màn chờ duyệt.'),
    r'^2\.4 Lập phiếu': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
                         'Người lập phiếu — người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình '
                         '(chức năng lập phiếu không gắn quyền riêng).',
                         '1. Đăng nhập thành công.\n'
                         '2. Vào được màn Phiếu đề nghị thu tiền (lập phiếu không gắn quyền riêng).\n'
                         '3. Đang ở màn danh sách phiếu.'),
    r'^2\.5 Chọn đối tượng': ('Dropdown, Popup chọn dữ liệu và Validate dữ liệu.',
                              'Người lập phiếu — người dùng đang lập hoặc sửa phiếu của chính mình (chức năng không '
                              'gắn quyền riêng).',
                              '1. Đăng nhập thành công.\n2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
                              '3. Đang ở màn Tạo mới hoặc Chỉnh sửa phiếu, bảng Chi tiết đã có ít nhất một dòng.'),
    r'^2\.6 Sửa phiếu': ('Màn Chỉnh sửa, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.7 Xem chi tiết': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.8 Xem danh sách phiếu chờ duyệt': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.',
                                             ACTOR_KT, '1. Đăng nhập thành công.\n2. Có quyền Kế toán thanh toán (Q1).'),
    r'^2\.9 Không duyệt': ('Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.', ACTOR_KT, COND_KT),
    r'^2\.10 Xóa': ('Quy tắc Xóa, Thông báo và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.11 In': ('Quy tắc màn In, Thông báo và UI/UX.', ACTOR_SCOPE,
                   '1. Đăng nhập thành công.\n2. Có quyền xem phiếu như mục Tác nhân (chức năng không gắn quyền riêng).\n'
                   '3. Phiếu nằm trong phạm vi dữ liệu của người dùng.'),
    r'^2\.12 Xem lịch sử': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

# Đường dẫn: danh sách dòng menu (dòng đầu thay đoạn "Menu:") + câu popup (None = không có)
MENU_LINES = {
    r'^2\.1 ': (['Menu: %s' % M1, 'Hoặc: %s' % M2], None),
    r'^2\.2 ': (['Menu: %s => Tìm kiếm nâng cao' % M1, 'Hoặc: %s => Tìm kiếm nâng cao' % M2], None),
    r'^2\.3 ': (['Menu: %s => Cài đặt bộ lọc / Cấu hình cột hiển thị' % M1,
                 'Hoặc: %s => Cài đặt bộ lọc / Cấu hình cột hiển thị' % M2],
                'Modal Cài đặt bộ lọc và Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.4 ': (['Menu: %s => Tạo mới' % M1, 'Hoặc: %s => Tạo mới' % M2], None),
    r'^2\.5 ': (['Menu: %s => Tạo mới / Sửa => bấm ô Khách hàng (Nhà cung cấp) hoặc ô Số đơn hàng/Hợp đồng của dòng '
                 'chi tiết' % M1,
                 'Hoặc: %s => Tạo mới / Sửa => bấm ô Khách hàng (Nhà cung cấp) hoặc ô Số đơn hàng/Hợp đồng của dòng '
                 'chi tiết' % M2],
                'Modal Chọn khách hàng, Chọn nhà cung cấp và Chọn đơn hàng/hợp đồng được mở ngay trên màn hình Tạo mới '
                'hoặc Chỉnh sửa phiếu theo đường dẫn ở trên.'),
    r'^2\.6 ': (['Menu: %s => Sửa (trên dòng phiếu) / Mã phiếu => Sửa' % M1,
                 'Hoặc: %s => Sửa (trên dòng phiếu) / Mã phiếu => Sửa' % M2], None),
    r'^2\.7 ': (['Menu: %s => Mã phiếu' % M1, 'Hoặc: %s => Mã phiếu' % M2, 'Hoặc: %s => Mã phiếu' % MP], None),
    r'^2\.8 ': (['Menu: %s' % MP], None),
    r'^2\.9 ': (['Menu: %s => Mã phiếu => Không duyệt' % MP,
                 'Hoặc: %s => Mã phiếu (phiếu Chờ KT duyệt) => Không duyệt' % M1],
                'Modal Không duyệt phiếu được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
    r'^2\.10 ': (['Menu: %s => nút ba chấm trên dòng phiếu => Xóa / Mã phiếu => Xóa' % M1,
                  'Hoặc: %s => nút ba chấm trên dòng phiếu => Xóa / Mã phiếu => Xóa' % M2],
                 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (mục Xóa trên dòng phiếu) hoặc màn hình chi '
                 'tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.11 ': (['Menu: %s => In phiếu (trên dòng phiếu) / Mã phiếu => In phiếu' % M1,
                  'Hoặc: %s => In phiếu (trên dòng phiếu) / Mã phiếu => In phiếu' % M2,
                  'Hoặc: %s => In phiếu (trên dòng phiếu)' % MP],
                 'Cửa sổ Xem trước phiếu đề nghị thu tiền được mở ngay trên màn hình danh sách hoặc màn hình chi tiết '
                 'phiếu theo đường dẫn ở trên.'),
    r'^2\.12 ': (['Menu: %s => Lịch sử (trên dòng phiếu) / Mã phiếu => Xem lịch sử' % M1,
                  'Hoặc: %s => Lịch sử (trên dòng phiếu) / Mã phiếu => Xem lịch sử' % M2],
                 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách (nút Lịch sử trên dòng phiếu); khối Lịch '
                 'sử nằm cuối màn hình chi tiết phiếu.'),
}

USECASES = {
    r'^2\.4 ': ('Người lập phiếu', 'FR-04', 'Lập phiếu đề nghị thu tiền', 'crud'),
    r'^2\.5 ': ('Người lập phiếu', 'FR-05', 'Chọn đối tượng và hợp đồng', 'crud'),
    r'^2\.6 ': ('Người lập phiếu', 'FR-06', 'Sửa phiếu', 'crud'),
    r'^2\.7 ': ('Người dùng có quyền', 'FR-07', 'Xem chi tiết phiếu', 'view'),
    r'^2\.9 ': ('Kế toán thanh toán', 'FR-09', 'Không duyệt phiếu', 'action'),
    r'^2\.10 ': ('Người lập phiếu', 'FR-10', 'Xóa phiếu', 'action'),
    r'^2\.11 ': ('Người dùng có quyền', 'FR-11', 'In phiếu', 'io'),
}

# Ảnh thay bằng ảnh chụp dev 28/10 (giao diện hiện tại): số Hình CŨ của bản Drive -> file
NEW_IMAGES = {2: '01_list', 3: '02_filter', 5: '26_filtercfg', 6: '25_colcfg', 8: '10_create',
              11: '14_confirm_send', 12: '15_unsaved', 13: '13b_changetype', 15: '11_customer',
              17: '11b_supplier', 19: '19_edit', 20: '17_detail', 21: '21_pending', 23: '15_reject',
              25: '13_delete', 27: '18_print'}
NEW_CAPTION = {27: 'Cửa sổ Xem trước phiếu đề nghị thu tiền'}

PART5 = [
    ('1', 'Tài chính', 'Phiếu thu (lập phiếu thu từ phiếu đề nghị đang Chờ KT duyệt: chọn phiếu đề nghị, nạp các dòng '
     'chi tiết; lưu/gửi duyệt, duyệt, hủy phiếu thu thì đổi trạng thái phiếu đề nghị sang Đã tạo phiếu thu / Đã hạch '
     'toán / Hủy; lọc phiếu thu theo mã phiếu đề nghị; xuất Excel phiếu thu lấy loại thu của phiếu đề nghị)',
     'Tài chính -> Quản lý tiền -> Thanh toán tiền mặt'),
]


# ============================================================== HÀM RIÊNG
def lines_replace(lines, old_regex, new):
    out, hit = [], False
    for l in lines:
        if re.search(old_regex, l):
            hit = True
            if new is not None:
                out.extend(new if isinstance(new, list) else [new])
        else:
            out.append(l)
    assert hit, 'Không thấy dòng: ' + old_regex
    return out


def kv_edit(kv, key, old_regex, new):
    write_cell(kv_row(kv, key), lines_replace(kv_get(kv, key), old_regex, new))


def kv_add(kv, key, line):
    write_cell(kv_row(kv, key), [l for l in kv_get(kv, key) if l.strip()] + [line])


def ev_edit(ev, event_regex, old_regex, new):
    tc = cells(find_row(ev, 1, event_regex))[3]
    write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))


def cell_set(tbl, name_regex, header, value):
    write_cell(cells(find_row(tbl, 1, name_regex))[header_index(tbl, header)], [value])


def rebuild_rows(tbl, data_rows):
    """Viết lại toàn bộ dòng dữ liệu (giữ dòng tiêu đề + khuôn dòng thân đầu tiên)."""
    trs = rows(tbl)
    body = trs[1]
    for tr in trs[1:]:
        tbl.remove(tr)
    for vals in data_rows:
        tr = strip_ids(copy.deepcopy(body))
        for tc, v in zip(cells(tr), vals):
            write_cell(tc, v if isinstance(v, list) else v.split('\n'))
        tbl.append(tr)
    renumber_stt(tbl)


def clean_ui(tbl):
    """Chuẩn hóa chung bảng mô tả giao diện: loại đối tượng + ô 'Giá trị ban đầu' của nút."""
    li = header_index(tbl, 'Loại')
    try:
        gi = header_index(tbl, 'Giá trị ban đầu')
    except KeyError:
        gi = None
    fix = {'Number': None, 'Modal': 'Popup', 'Text': 'Label', 'Loading': None}
    for tr in rows(tbl)[1:]:
        cs = cells(tr)
        name = txt(cs[1]).strip()
        typ = txt(cs[li]).strip()
        if typ in fix:
            if fix[typ]:
                new = fix[typ]
            else:  # Number: cột / ô chỉ đọc -> Table/Grid, ô nhập -> Textbox
                ro = name.startswith('Cột') or 'Read-only' in [txt(c).strip() for c in cs]
                new = 'Table/Grid' if ro else 'Textbox'
            L.log('Loại [%s]: %s → %s' % (name, typ, new))
            write_cell(cs[li], [new])
        if gi is not None and typ in ('Button', 'Icon Button') and txt(cs[gi]).strip() == 'Hiển thị':
            write_cell(cs[gi], [''])
        for c in cs:
            t = txt(c)
            if re.search(r'\b0255 ký tự|\bab / N|V1V4', t):
                write_cell(c, [x.replace('0255 ký tự', 'Không giới hạn').replace('ab / N', 'a–b / N')
                               .replace('V1V4', 'V1–V4') for x in cell_lines(c)])


def set_menu(doc, sec, menu_lines, popup):
    els = sec[1]
    start = None
    for i, e in enumerate(els):
        if e.tag == W('p') and txt(e).strip().startswith('Đường dẫn màn hình'):
            start = i
            break
    assert start is not None, 'Không có Đường dẫn màn hình: ' + txt(sec[0])
    i = start + 1
    menu_p = None
    old = []
    while i < len(els):
        e = els[i]
        t = txt(e).strip()
        if e.tag != W('p'):
            break
        if t.startswith('Menu:') and menu_p is None:
            menu_p = e
        elif '=>' in t or t == 'Hoặc':
            old.append(e)
        else:
            break
        i += 1
    for e in old:
        e.getparent().remove(e)
    if menu_p is None:
        menu_p = strip_ids(copy.deepcopy(els[start]))
        els[start].addnext(menu_p)
    set_runs_text(menu_p, menu_lines[0])
    set_bold(menu_p, False)
    last = menu_p
    for line in menu_lines[1:]:
        p = strip_ids(copy.deepcopy(menu_p))
        set_runs_text(p, line)
        last.addnext(p)
        last = p
    nxt = last.getnext()
    if popup:
        if nxt is not None and nxt.tag == W('p') and re.search(r'được mở ngay', txt(nxt)):
            set_runs_text(nxt, popup)
        else:
            p = strip_ids(copy.deepcopy(menu_p))
            set_runs_text(p, popup)
            last.addnext(p)


UI_COL_W = {'STT': 550, 'Tên đối tượng': 1400, 'Loại': 1350, 'Trạng thái': 1100, 'Phạm vi': 1000,
            'Bắt buộc': 1000, 'Giá trị ban đầu': 1150}
UI_COL_W8 = {'STT': 550, 'Tên đối tượng': 1300, 'Loại': 1350, 'Trạng thái': 1050, 'Phạm vi': 950,
             'Bắt buộc': 1000, 'Giá trị ban đầu': 1000}
TOTAL_W = 9200


def fix_ui_widths(tbl):
    """Bảng mô tả giao diện bản Drive để cột Loại / Trạng thái quá hẹp → 'Table/Grid', 'Read-only' bị bẻ đôi,
    nhìn như lệch cột. Đặt lại độ rộng cột cố định, phần còn lại dồn cho cột Mô tả."""
    hdr = [txt(c).strip() for c in cells(rows(tbl)[0])]
    cw = UI_COL_W8 if len(hdr) >= 8 else UI_COL_W
    ws = [cw.get(h, 0) for h in hdr]
    rest = TOTAL_W - sum(ws)
    ws = [w if w else rest for w in ws]
    grid = tbl.find(W('tblGrid'))
    for gc, w in zip(grid.findall(W('gridCol')), ws):
        gc.set(W('w'), str(w))
    tblpr = tbl.find(W('tblPr'))
    tw = tblpr.find(W('tblW'))
    if tw is not None:
        tw.set(W('w'), str(TOTAL_W))
        tw.set(W('type'), 'dxa')
    for tr in rows(tbl):
        for tc, w in zip(cells(tr), ws):
            tcpr = tc.find(W('tcPr'))
            if tcpr is None:
                tcpr = L._el('tcPr')
                tc.insert(0, tcpr)
            tcw = tcpr.find(W('tcW'))
            if tcw is None:
                tcw = L._el('tcW')
                tcpr.insert(0, tcw)
            tcw.set(W('w'), str(w))
            tcw.set(W('type'), 'dxa')


def keep_image_with_caption(doc):
    """keepNext cho đoạn ảnh đứng ngay trước chú thích 'Hình N' → chú thích không rơi sang trang sau."""
    its = items(doc)
    n = 0
    for i, e in enumerate(its[1:], 1):
        if e.tag == W('p') and re.match(r'^Hình \d+:', txt(e)) and list(its[i - 1].iter(L.A_NS + 'blip')):
            p = its[i - 1]
            ppr = p.find(W('pPr'))
            if ppr is None:
                ppr = L._el('pPr')
                p.insert(0, ppr)
            if ppr.find(W('keepNext')) is None:
                kn = L._el('keepNext')
                ps = ppr.find(W('pStyle'))
                (ps.addnext(kn) if ps is not None else ppr.insert(0, kn))
                n += 1
    L.log('keepNext ảnh-chú thích: %d' % n)


def replace_images(doc):
    its = items(doc)
    for i, e in enumerate(its):
        m = e.tag == W('p') and re.match(r'^Hình (\d+):', txt(e))
        if not m:
            continue
        n = int(m.group(1))
        if n not in NEW_IMAGES:
            continue
        img = its[i - 1]
        assert list(img.iter(L.A_NS + 'blip')), 'Không thấy ảnh trước Hình %d' % n
        set_image(doc, img, os.path.join(SHOT, NEW_IMAGES[n] + '.png'))
        if n in NEW_CAPTION:
            set_runs_text(e, 'Hình %d: %s' % (n, NEW_CAPTION[n]))
        L.log('Thay ảnh Hình %d → %s' % (n, NEW_IMAGES[n]))


# ============================================================== XỬ LÝ
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)

    replace_images(doc)  # trước khi đánh lại số Hình

    # Đoạn trống đứng ngay trước đoạn ngắt trang: bảng dài hơn → đoạn trống tràn sang trang mới rồi mới ngắt → trang trắng
    for p in list(doc.element.body.iter(W('p'))):
        if any(b.get(W('type')) == 'page' for b in p.iter(W('br'))):
            prev = p.getprevious()
            if prev is not None and prev.tag == W('p') and not txt(prev).strip() and not list(prev.iter(L.A_NS + 'blip')):
                prev.getparent().remove(prev)

    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    for rx, (menu, popup) in MENU_LINES.items():
        set_menu(doc, section(doc, rx), menu, popup)

    for rx in [r'^2\.%d ' % k for k in range(1, 13)]:
        sec = section(doc, rx)
        try:
            ui = sec_ui(sec)
        except KeyError:
            continue
        clean_ui(ui)
        fix_ui_widths(ui)

    patch_sections(doc, rid)
    patch_part4(doc)
    add_part5(doc)

    remove_usecase(doc, section(doc, r'^2\.3 '))
    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.9 '), png, 'Biểu đồ Use Case — %s %s' % (code, name))
        else:
            set_image(doc, blk[1], png)
            set_runs_text(blk[2], 'Hình 0: Biểu đồ Use Case — %s %s' % (code, name))
    renumber_subheadings(doc)
    nfig = renumber_figures(doc)
    keep_image_with_caption(doc)
    L.log('Số Hình sau khi đánh lại: %d' % nfig)

    # Lỗi chữ còn sót ngoài bảng mô tả
    body = doc.element.body
    for a, b in [('0255 ký tự', 'Không giới hạn'), ('ab / N', 'a–b / N'), ('V1V4', 'V1–V4')]:
        n = replace_in_texts(body, a, b)
        if n:
            L.log('Sửa chữ "%s": %d chỗ' % (a, n))

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        word_finalize(OUT, os.path.join(OUT_DIR, NAME + '.pdf'))


def patch_sections(doc, rid):
    # ---------------- 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. Người dùng vào menu',
            '1. Người dùng vào menu %s (hoặc %s).' % (M1, M2))
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', '5. Bảng hiển thị dữ liệu; dòng “Hiển thị a–b / N” cho biết khoảng dòng '
            'đang xem và tổng số phiếu khớp bộ lọc.')
    ui = sec_ui(s)
    cell_set(ui, r'^Cột Trạng thái$', 'Loại', 'Table/Grid')
    cell_set(ui, r'^Cột Trạng thái$', 'Mô tả', 'Nhãn màu: Đã tạo phiếu thu, Đã hạch toán nền xanh; Đang tạo, Chờ KT duyệt, '
             'Hủy, Không duyệt nền đỏ.')
    cell_set(ui, r'^Cột Hành động$', 'Mô tả', 'Cột bắt buộc. Hiện tối đa 3 nút, các nút còn lại gom vào nút ba chấm '
             '(Hành động khác). Gồm: Sửa (phiếu của mình, Đang tạo / Không duyệt), Tạo phiếu thu (Kế toán thanh toán, '
             'phiếu Chờ KT duyệt chưa có phiếu thu), In phiếu, Xóa (cùng điều kiện với Sửa), Lịch sử.')
    cell_set(ui, r'^Cột Mã phiếu$', 'Mô tả', 'Là liên kết mở màn chi tiết (FR-07); sắp xếp được; cột bắt buộc.')
    cell_set(ui, r'Hiển thị a', 'Tên đối tượng', 'Dòng “Hiển thị a–b / N”')
    cell_set(ui, r'Hiển thị a', 'Mô tả', 'a–b là khoảng dòng của trang đang xem; N là tổng số phiếu khớp bộ lọc, không '
             'phải tổng toàn hệ thống.')

    # ---------------- 2.2 Tìm kiếm
    s = section(doc, r'^2\.2 ')
    ui = sec_ui(s)
    cell_set(ui, r'^Ô Tìm theo mã phiếu$', 'Phạm vi', 'Không giới hạn')
    cell_set(ui, r'^Số đơn hàng/hợp đồng$', 'Phạm vi', 'Không giới hạn')
    cell_set(ui, r'^Khách hàng$', 'Mô tả', 'Ô gõ tay; tìm được cả theo mã và theo tên khách hàng.')
    cell_set(ui, r'^Công ty$', 'Mô tả', 'Hiện với người có quyền V1. Đổi công ty thì xóa giá trị Phòng ban và Bộ phận.')
    ev = sec_ev(s)
    tr = find_row(ev, 1, r'^Nhập từ khóa ô Nhà cung cấp')
    write_cell(cells(tr)[1], ['Nhập từ khóa và chọn ở ô Nhà cung cấp'])
    write_cell(cells(tr)[2], ['Change'])

    # ---------------- 2.3 Cài đặt bộ lọc / Tùy chỉnh cột
    s = section(doc, r'^2\.3 ')
    ui = sec_ui(s)
    for rx in (r'^Ô tích chọn từng tiêu chí', r'^Ô tích chọn từng cột'):
        cell_set(ui, rx, 'Loại', 'Checkbox')
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'^• Bấm Đóng', '• Bấm Đóng / (x) / click ra ngoài cửa sổ → thoát ngay, '
            'không hỏi xác nhận, không lưu thay đổi.')
    clone_row_after(sec_ev(s), r'^Bỏ tích một mục', [None, 'Kéo thả để đổi thứ tự', 'Drag',
                    ['After:', '– Đổi vị trí tiêu chí / cột trong cửa sổ; mục bắt buộc (STT, Mã phiếu, Hành động) '
                     'không kéo được; chưa áp lên màn hình cho tới khi bấm Lưu.']])

    # ---------------- 2.4 Lập phiếu
    s = section(doc, r'^2\.4 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', '4. Người dùng bấm Lưu nháp, Lưu và tiếp tục, hoặc Lưu và gửi duyệt rồi '
            'xác nhận.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống kiểm tra dữ liệu theo nút được bấm, sinh mã phiếu, ghi phiếu và các dòng chi tiết (Lưu nháp / '
        'Lưu và tiếp tục: trạng thái Đang tạo; Lưu và gửi duyệt: trạng thái Chờ KT duyệt).',
        '6. Ghi nhận hành động Tạo mới trong lịch sử của phiếu; gửi duyệt thì gửi thông báo cho Kế toán thanh toán '
        'cùng công ty.'])
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. Hệ thống hiển thị', '7. Hệ thống hiển thị thông báo thành công và quay về '
            'màn danh sách (Lưu và tiếp tục: ở lại màn Thêm mới, form trống để lập tiếp phiếu khác).')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn khi đã nhập dở', UNSAVED)
    ui = sec_ui(s)
    cell_set(ui, r'^Loại tiền$', 'Giá trị ban đầu', 'VNĐ')
    cell_set(ui, r'^Lý do thu$', 'Phạm vi', 'Không giới hạn')
    cell_set(ui, r'^Tỷ giá', 'Loại', 'Textbox')
    cell_set(ui, r'^Cột Số tiền đề nghị thu', 'Loại', 'Textbox')
    cell_set(ui, r'^Cột Khách hàng / Nhà cung cấp', 'Mô tả', 'Bấm vào ô để mở cửa sổ chọn đối tượng (FR-05); gợi ý '
             '“Nhấn vào đây để chọn khách hàng” (hoặc nhà cung cấp); nhãn cột đổi theo Loại thu.')
    cell_set(ui, r'^Cột Số đơn hàng/Hợp đồng', 'Mô tả', 'Bị khóa cho tới khi dòng đã chọn đối tượng; chọn xong đối '
             'tượng thì gợi ý “Nhấn vào đây để chọn hợp đồng”.')
    cell_set(ui, r'^Thông báo lỗi dưới ô$', 'Loại', 'Label')
    cell_set(ui, r'^Hộp xác nhận lưu và gửi duyệt$', 'Mô tả', 'Tiêu đề “Xác nhận lưu và gửi duyệt”, nội dung “Bạn đồng ý '
             'lưu và duyệt?”, hai nút Xác nhận và Hủy.')
    clone_row_after(ui, r'^Nút Lưu nháp$', [None, 'Nút Lưu và tiếp tục', None, None, None, None, None,
                    'Chỉ có ở màn Tạo mới. Lưu phiếu ở trạng thái Đang tạo rồi làm mới form để lập tiếp phiếu khác.'])
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Lưu nháp', rid)
    add_err_line(ev, r'^Bấm Lưu và gửi duyệt', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp', [None, 'Bấm Lưu và tiếp tục', 'Click', 'x'])
    write_cell(cells(find_row(ev, 1, r'^Bấm Lưu và tiếp tục'))[3], [
        'During:', '– Kiểm tra dữ liệu như Lưu nháp.', L.ERR_LINE, 'After:',
        '– Sinh mã phiếu, ghi phiếu ở trạng thái Đang tạo; ghi một dòng lịch sử “Tạo mới”.',
        '– Hiển thị thông báo thành công, ở lại màn Thêm mới với form trống như lúc mới mở.'], rid)
    tr = find_row(ev, 1, r'^Bấm Quay lại')
    write_cell(cells(tr)[1], ['Bấm Quay lại / chọn menu khác / đóng tab trình duyệt'])
    write_cell(cells(tr)[3], UNSAVED_EV)

    # ---------------- 2.5 Chọn đối tượng và hợp đồng
    s = section(doc, r'^2\.5 ')
    ui = sec_ui(s)
    for tr in rows(ui)[1:]:  # ô tìm trong popup không giới hạn độ dài
        c = cells(tr)[header_index(ui, 'Phạm vi')]
        if txt(c).strip() == '255 ký tự':
            write_cell(c, ['Không giới hạn'])
    kv_add(sec_kv(s), 'Dòng sự kiện phụ', CLOSE_NOASK.replace('phiếu giữ nguyên', 'dòng chi tiết giữ nguyên'))

    # ---------------- 2.6 Sửa phiếu
    s = section(doc, r'^2\.6 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống kiểm tra dữ liệu, ghi lại phiếu và các dòng chi tiết.',
        '6. Ghi nhận các thay đổi (theo từng trường và từng dòng chi tiết) trong lịch sử của phiếu.'])
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. Hệ thống hiển thị', '7. Hệ thống hiển thị thông báo thành công và quay về '
            'màn danh sách.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn khi đã sửa', UNSAVED)
    ui = sec_ui(s)
    cell_set(ui, r'^Tỷ giá', 'Loại', 'Textbox')
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # ---------------- 2.7 Xem chi tiết
    s = section(doc, r'^2\.7 ')
    ui = sec_ui(s)
    cell_set(ui, r'^Nút In phiếu$', 'Mô tả', 'Mở cửa sổ Xem trước bản in ngay trên màn hình (FR-11).')
    cell_set(ui, r'^Nút In phiếu$', 'Giá trị ban đầu', '')
    cell_set(ui, r'^Nút Quay lại$', 'Giá trị ban đầu', '')
    ev_edit(sec_ev(s), r'^Bấm nút In phiếu', r'ở tab mới', '– Mở cửa sổ Xem trước bản in của phiếu ngay trên màn hình (FR-11).')

    # ---------------- 2.8 Chờ duyệt
    s = section(doc, r'^2\.8 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^1\. ', '1. Người dùng vào menu %s.' % MP)

    # ---------------- 2.9 Không duyệt
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ', [
        '6. Ghi nhận hành động Thay đổi trạng thái (Chờ KT duyệt → Không duyệt) kèm lý do trong lịch sử của phiếu.',
        '7. Hệ thống hiển thị “Không duyệt phiếu đề nghị thu thành công!”, đóng hộp thoại và nạp lại màn chi tiết.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Đóng', '• Bấm Đóng / (x) / click ra ngoài cửa sổ → hộp thoại đóng ngay, '
            'không hỏi xác nhận kể cả khi đã nhập lý do; phiếu giữ nguyên, mở lại thì ô lý do trở về trống.')
    ui = sec_ui(s)
    cell_set(ui, r'^Lý do không duyệt$', 'Phạm vi', 'Không giới hạn')
    cell_set(ui, r'^Thông báo lỗi dưới ô$', 'Loại', 'Label')
    add_err_line(sec_ev(s), r'^Bấm nút Không duyệt trong hộp thoại', rid)

    # ---------------- 2.10 Xóa
    s = section(doc, r'^2\.10 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', '5. Hệ thống ghi nhận hành động Xóa (kèm nội dung phiếu trước khi xóa) '
            'trong lịch sử, xóa các dòng chi tiết và xóa phiếu.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ', '6. Hệ thống hiển thị “Xóa thành công”: xóa từ danh sách thì nạp lại '
            'danh sách; xóa từ màn chi tiết thì quay về màn danh sách.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Hủy', '• Bấm Hủy / (x) / click ra ngoài hộp thoại → đóng hộp thoại, phiếu '
            'giữ nguyên.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. ', '1. Người dùng bấm nút ba chấm (Hành động khác) ở cột Hành động rồi '
            'chọn Xóa (hoặc bấm nút Xóa ở màn chi tiết).')
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm nút Xóa trong hộp xác nhận', rid)
    ev_edit(ev, r'^Bấm nút Xóa trong hộp xác nhận', r'Hiển thị “Xóa thành công”',
            '– Hiển thị “Xóa thành công”; xóa từ danh sách thì nạp lại danh sách, xóa từ màn chi tiết thì quay về màn '
            'danh sách.')

    # ---------------- 2.11 In phiếu (popup xem trước — không còn mở tab mới)
    s = section(doc, r'^2\.11 ')
    kv = sec_kv(s)
    kv_set(kv, 'Mô tả', 'Mở cửa sổ Xem trước bản in của một phiếu ngay trên màn hình (không mở tab mới), theo mẫu in '
           'của hệ thống; bấm In để gửi lệnh in tới trình duyệt.')
    kv_set(kv, 'Dòng sự kiện chính', '1. Người dùng bấm nút In phiếu ở cột Hành động hoặc ở màn chi tiết.\n'
           '2. Hệ thống mở cửa sổ Xem trước phiếu đề nghị thu tiền, hiện “Đang tải dữ liệu in…”.\n'
           '3. Hệ thống chọn mẫu in theo Loại thu và Loại tiền của phiếu, điền dữ liệu phiếu (Số tiền còn nợ tính lại '
           'theo sổ kế toán) và hiển thị bản xem trước.\n'
           '4. Người dùng bấm nút In để mở hộp thoại in của trình duyệt.')
    kv_set(kv, 'Dòng sự kiện phụ', '• Phiếu loại Thu nhà cung cấp → dùng mẫu in nhà cung cấp; hai cột đổi nhãn thành Nhà '
           'cung cấp và Hợp đồng mua.\n'
           '• Phiếu dùng ngoại tệ → dùng mẫu in ngoại tệ, có thêm Tỷ giá.\n'
           '• Không tìm thấy mẫu in trên hệ thống → cửa sổ báo lỗi “Không tìm thấy mẫu in phiếu đề nghị thu tiền …”.\n'
           '• Bấm (x) → đóng cửa sổ xem trước, quay lại màn đang đứng.')
    kv_set(kv, 'Yêu cầu đặc biệt', 'Mẫu in dùng chung với hệ thống ERP: 4 mẫu theo Loại thu (bán hàng / nhà cung cấp) × '
           'Loại tiền (VNĐ / ngoại tệ). Đầu trang (logo, thông tin công ty) lấy theo công ty ghi trên phiếu.')
    rebuild_rows(sec_ui(s), [
        ['', 'Tiêu đề cửa sổ', 'Label', 'Xem trước phiếu đề nghị thu tiền <mã phiếu>', ''],
        ['', 'Nút In', 'Button', '', 'Mở hộp thoại in của trình duyệt; không xuất hiện trên bản in.'],
        ['', 'Nút (x)', 'Button', '', 'Đóng cửa sổ xem trước.'],
        ['', 'Đầu trang', 'Image', 'Theo công ty của phiếu', 'Logo và thông tin công ty ghi trên phiếu.'],
        ['', 'Tiêu đề bản in', 'Label', 'Theo mẫu in', 'Phiếu thu bán hàng: “PHIẾU ĐỀ NGHỊ THU TIỀN BÁN HÀNG”; phiếu thu '
         'nhà cung cấp dùng tiêu đề của mẫu nhà cung cấp.'],
        ['', 'Dòng ngày', 'Label', 'Theo dữ liệu', 'Dạng “Ngày dd Tháng mm Năm yyyy” theo ngày lập phiếu.'],
        ['', 'Khối thông tin', 'Label', 'Theo dữ liệu', 'Họ và tên người đề nghị, Phòng ban, Lý do thu, Diễn giải (nội '
         'dung ô Ghi chú của phiếu); mẫu ngoại tệ có thêm Tỷ giá.'],
        ['', 'Bảng chi tiết', 'Table/Grid', 'Theo dữ liệu', 'STT, Khách hàng (Nhà cung cấp), Số đơn hàng/Hợp đồng (Hợp '
         'đồng mua), Số tiền còn nợ, Số tiền đề nghị thu, Ghi chú; dòng cuối “Tổng cộng (quy đổi VND)”.'],
        ['', 'Khối ký tên', 'Label', 'Theo mẫu in', 'TRƯỞNG PHÒNG và NGƯỜI ĐỀ NGHỊ (kèm ngày lập và tên người lập).'],
    ])
    rebuild_rows(sec_ev(s), [
        ['', 'Bấm nút In phiếu (dòng phiếu hoặc màn chi tiết)', 'Click',
         ['After:', '– Mở cửa sổ Xem trước phiếu đề nghị thu tiền ngay trên màn hình đang đứng.']],
        ['', 'Mở cửa sổ xem trước', 'System',
         ['During:', '– Chọn mẫu in theo Loại thu × Loại tiền; nạp dữ liệu phiếu, tính lại Số tiền còn nợ của từng dòng.',
          'After:', '– Hiển thị bản xem trước; không tìm thấy mẫu in thì báo lỗi trong cửa sổ.']],
        ['', 'Bấm nút In', 'Click', ['After:', '– Mở hộp thoại in của trình duyệt với đúng nội dung bản xem trước.']],
        ['', 'Bấm nút (x)', 'Click', ['After:', '– Đóng cửa sổ xem trước, không thay đổi dữ liệu.']],
    ])

    # ---------------- 2.12 Lịch sử
    s = section(doc, r'^2\.12 ')
    kv = sec_kv(s)
    kv_set(kv, 'Mô tả', 'Hiển thị các thao tác đã tác động lên phiếu theo dòng thời gian: tạo mới, thay đổi thông tin '
           '(kể cả thêm / sửa / bỏ dòng chi tiết), thay đổi trạng thái (gửi duyệt, không duyệt, đã tạo phiếu thu, đã '
           'hạch toán, hủy), kèm người thực hiện và giá trị trước / sau.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa từng', '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ '
            'thống mới → hiện “Chưa có lịch sử thao tác nào.”.')
    ui = sec_ui(s)
    cell_set(ui, r'^Tiêu đề cửa sổ$', 'Giá trị ban đầu', 'Lịch sử thay đổi: <mã phiếu>')
    cell_set(ui, r'^Tiêu đề cửa sổ$', 'Mô tả', '')
    cell_set(ui, r'^Trạng thái rỗng$', 'Mô tả', 'Hiện “Chưa có lịch sử thao tác nào.” với phiếu lập từ hệ thống cũ, chưa '
             'có thao tác nào trên hệ thống mới.')
    cell_set(ui, r'^Nút Đóng / Thu gọn$', 'Giá trị ban đầu', '')


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and re.match(r'^Phần %d\b' % n, txt(e)):
            return e
    raise KeyError(n)


def patch_part4(doc):
    h = part_heading(doc, 4)
    intro = h.getnext()
    while txt(intro).strip() == '':
        intro = intro.getnext()
    set_rule_head(intro, 'Quy tắc áp dụng: Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
    set_rule_tail(intro, '. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có trong SRS '
                         'quy tắc chung.' % SCREEN)
    tbl = intro.getnext()
    while tbl.tag != W('tbl'):
        tbl = tbl.getnext()
    # dòng trống thừa trong mô tả BR-09
    for tr in rows(tbl)[1:]:
        tc = cells(tr)[3]
        ls = [l for l in cell_lines(tc) if l.strip()]
        write_cell(tc, ls)
    tc = cells(find_row(tbl, 1, r'^BR-10$'))[3]
    write_cell(tc, lines_replace(cell_lines(tc), r'cộng dồn ngay', ' Số tiền quy đổi VND của một dòng bằng Số tiền đề '
                                 'nghị thu nhân với tỷ giá; dòng Tổng cộng cộng dồn ngay theo từng giá trị nhập.'))
    tc = cells(find_row(tbl, 1, r'^BR-04$'))[3]
    write_cell(tc, lines_replace(cell_lines(tc), r'^\s*Lưu nháp:', ' Lưu nháp và Lưu và tiếp tục: cho phép bỏ trống Lý '
                                 'do thu và cho phép bảng Chi tiết chưa có dòng nào.'))
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i
    # Quy tắc quay về danh sách sau thao tác (giữ theo chuẩn, ghi rõ ngoại lệ đúng code)
    clone_row_after(tbl, r'^BR-%02d$' % (len(rows(tbl)) - 1), [None, 'BR-%02d' % len(rows(tbl)),
                    'Màn hình sau khi thao tác xong', [
                        ' Lưu nháp, Lưu và gửi duyệt (tạo mới hoặc sửa), Xóa ở màn chi tiết: thao tác xong quay về '
                        'màn danh sách.',
                        ' Lưu và tiếp tục: ở lại màn Thêm mới với form trống để lập tiếp phiếu khác.',
                        ' Không duyệt: đóng hộp thoại và nạp lại màn chi tiết của phiếu; Xóa ở màn danh sách: nạp lại '
                        'danh sách.'], '- Tạo phiếu / - Sửa phiếu / - Xóa phiếu / - Không duyệt phiếu'.split(' / ')], col=1)


def add_part5(doc):
    h4 = part_heading(doc, 4)
    last = doc.element.body[-1]
    anchor = last.getprevious()
    h5 = clone_heading(h4, 'Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    ppr = h5.find(W('pPr'))
    if ppr is not None and ppr.find(W('pageBreakBefore')) is None:
        pb = L._el('pageBreakBefore')
        ps = ppr.find(W('pStyle'))
        (ps.addnext(pb) if ps is not None else ppr.insert(0, pb))
    intro = docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc hoặc cập nhật dữ liệu do %s ghi ra '
                                    '(thông tin phiếu, các dòng chi tiết và trạng thái phiếu).' % SCREEN)
    strip_ids(intro)
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1500, 3600, 2900])
    L.log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()
