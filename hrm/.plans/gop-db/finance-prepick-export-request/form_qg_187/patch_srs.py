# -*- coding: utf-8 -*-
"""Vá SRS "Yêu cầu xuất giữ" (STT 187, bản Drive 28/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Yêu cầu xuất giữ.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Chạy lại bao nhiêu lần cũng được: luôn đọc bản Drive gốc. Khuôn: finance-product-import-direct-transfer/form_qg.
Khác màn 27: bản Drive này đặt mục con 2.x.y là Heading4 (vài mục còn là đoạn thường) → hàm `is_sub` /
`renumber_subheadings` ở đây xét cả 2 và đặt Heading4 đồng loạt.
"""
import copy, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia')
sys.path.insert(0, LIB)
import docx  # noqa: E402
from formqg_lib import *  # noqa: E402,F401
import formqg_lib as L  # noqa: E402
import docxlib  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402

SRC = os.path.join(HERE, 'drive_0710', 'SRS_Drive.docx')
OUT_DIR = os.path.join(HERE, 'out')
NAME = 'SRS - Yêu cầu xuất giữ'
OUT = os.path.join(OUT_DIR, NAME + '.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Yêu cầu xuất giữ'
OLD_MENU = 'Phân hệ Tài chính => Giữ hàng => '
# finance.js: hubGroup 'Hàng hoá - Dịch vụ - Vận chuyển' > nhóm 'Giữ hàng' > mục 'Yêu cầu xuất giữ'
MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng => Yêu cầu xuất giữ'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Hủy).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; '
              'bấm Thoát thì rời màn và bỏ thay đổi, bấm Hủy thì giữ nguyên màn.']

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem phiếu hàng giữ theo tổng công ty / công ty / '
              'phòng ban (V1–V3) và quyền xử lý Trưởng phòng / Ban giám đốc / Kế toán duyệt hàng giữ (Q1–Q3); '
              'không có quyền nào thì chỉ thấy phiếu của mình.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (V1–V3, Q1–Q3); không có quyền nào vẫn xem được phiếu do chính mình lập.')
COND_LIST_ON = COND_LIST + '\n3. Đang ở màn danh sách phiếu.'
ACTOR_OWNER = ('Người lập phiếu — người dùng có quyền thực hiện chức năng: chỉ người đã lập phiếu (chức năng không '
               'gắn quyền riêng; người có vai trò quản trị hệ thống cũng thao tác được).')
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Đang tạo.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu; người có quyền Xem phiếu hàng giữ theo tổng công ty '
               '/ công ty / phòng ban (V1–V3) trong phạm vi được giao; hoặc người có quyền xử lý (Q1–Q3) với phiếu '
               'đang chờ chính mình.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Đang tạo chỉ người lập xem được.')

SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST, COND_LIST_ON),
    r'^2\.3 ': ('Bộ lọc và lưu cấu hình theo người dùng.', ACTOR_LIST, COND_LIST_ON),
    r'^2\.4 ': ('Cấu hình cột hiển thị và lưu cấu hình theo người dùng.', ACTOR_LIST, COND_LIST_ON),
    r'^2\.5 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
                'Người lập phiếu — người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình '
                '(lập yêu cầu xuất giữ không gắn quyền riêng).',
                '1. Đăng nhập thành công.\n'
                '2. Vào được màn Yêu cầu xuất giữ (lập phiếu không gắn quyền riêng).\n'
                '3. Không bị chặn do còn hàng quá hạn theo cấu hình hạn của thao tác “Lập yêu cầu xuất giữ” (BR-15).'),
    r'^2\.6 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.7 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.8 ': ('Thông báo, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.',
                'Người dùng có quyền Trưởng phòng duyệt hàng giữ (Q1) — quản lý phòng ban ghi trên phiếu — hoặc '
                'Ban giám đốc duyệt hàng giữ (Q2); cùng công ty với phiếu.',
                '1. Đăng nhập thành công.\n'
                '2. Có quyền Q1 (và quản lý phòng ban ghi trên phiếu) hoặc Q2; cùng công ty với phiếu.\n'
                '3. Phiếu đang ở trạng thái Chờ TP duyệt (Q1) hoặc Chờ BGĐ duyệt (Q2).'),
    r'^2\.9 ': ('Thông báo, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.',
                'Người dùng có quyền xử lý bước hiện tại của phiếu: Trưởng phòng duyệt hàng giữ (Q1), Ban giám đốc '
                'duyệt hàng giữ (Q2) hoặc Kế toán duyệt hàng giữ (Q3); cùng công ty với phiếu.',
                '1. Đăng nhập thành công.\n'
                '2. Có quyền Q1 / Q2 / Q3 đúng với bước hiện tại và cùng công ty với phiếu.\n'
                '3. Phiếu đang ở trạng thái Chờ TP duyệt, Chờ BGĐ duyệt hoặc Chờ KT duyệt.'),
    r'^2\.10 ': ('Quy tắc xóa, Thông báo và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.11 ': ('Thông báo, Phân quyền và Quy tắc ghi lịch sử.',
                 'Người dùng có quyền Kế toán duyệt hàng giữ (Q3), cùng công ty với phiếu.',
                 '1. Đăng nhập thành công.\n'
                 '2. Có quyền Kế toán duyệt hàng giữ (Q3) và cùng công ty với phiếu.\n'
                 '3. Phiếu đang ở trạng thái Chờ KT duyệt.'),
    r'^2\.12 ': ('Quy tắc màn In và bố cục bản in.', ACTOR_SCOPE,
                 '1. Đăng nhập thành công.\n2. Có quyền xem phiếu như mục Tác nhân.\n'
                 '3. In phiếu: phiếu nằm trong phạm vi dữ liệu của người dùng; In danh sách: đang ở màn danh sách.'),
    r'^2\.13 ': ('Quy tắc Excel và Cấu hình cột.', ACTOR_LIST, COND_LIST_ON),
    r'^2\.14 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

# Mục 2.x: (dòng Menu mới hoặc None, câu popup hoặc None) — áp cho dòng "Menu:" ĐẦU TIÊN của mục.
MENU_LINES = {
    r'^2\.3 ': ('Menu: %s => Cài đặt bộ lọc' % MENU,
                'Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.4 ': ('Menu: %s => Cấu hình cột hiển thị' % MENU,
                'Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.8 ': ('Menu: %s => Xem chi tiết => TP duyệt / BGĐ duyệt' % MENU,
                'Modal Xác nhận duyệt được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
    r'^2\.9 ': ('Menu: %s => Xem chi tiết => Từ chối' % MENU,
                'Modal Từ chối yêu cầu xuất giữ được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
    r'^2\.10 ': ('Menu: %s => Xóa (trên dòng phiếu) / Xem chi tiết => Xóa' % MENU,
                 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa trên dòng) hoặc màn hình '
                 'chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.12 ': ('Menu: %s => In (in danh sách, hoặc biểu tượng In trên dòng phiếu) / Xem chi tiết => In' % MENU,
                 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo '
                 'đường dẫn ở trên.'),
    r'^2\.13 ': ('Menu: %s => Xuất Excel' % MENU,
                 'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.14 ': ('Menu: %s => Lịch sử (biểu tượng trên dòng phiếu) / Xem chi tiết => Xem lịch sử' % MENU,
                 'Modal Lịch sử yêu cầu xuất giữ được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối '
                 'Lịch sử thay đổi nằm cuối màn hình chi tiết phiếu.'),
}

USECASES = {
    r'^2\.5 ': ('Người lập phiếu', 'FR-05', 'Tạo mới phiếu', 'crud'),
    r'^2\.6 ': ('Người lập phiếu', 'FR-06', 'Chỉnh sửa phiếu', 'crud'),
    r'^2\.7 ': ('Người dùng có quyền', 'FR-07', 'Xem chi tiết phiếu', 'view'),
    r'^2\.8 ': ('Trưởng phòng / BGĐ', 'FR-08', 'Duyệt phiếu', 'action'),
    r'^2\.9 ': ('TP / BGĐ / Kế toán', 'FR-09', 'Từ chối phiếu', 'action'),
    r'^2\.10 ': ('Người lập phiếu', 'FR-10', 'Xóa phiếu', 'action'),
    r'^2\.11 ': ('Kế toán', 'FR-11', 'Lập phiếu xuất giữ', 'action'),
    r'^2\.12 ': ('Người dùng có quyền', 'FR-12', 'In phiếu và In danh sách', 'io'),
    r'^2\.13 ': ('Người dùng có quyền', 'FR-13', 'Xuất Excel danh sách', 'io'),
}

# Ảnh thay mới (giao diện hiện tại: khối File đính kèm dạng lưới, nút mới...): regex chú thích -> (ảnh, chú thích mới)
SHOTS_REPLACE = [
    (r'^Hình \d+: Màn Yêu cầu xuất giữ lúc mới truy cập', '01_list', None),
    (r'^Hình \d+: Bảng lọc nâng cao đang mở', '02_filter', None),
    (r'^Hình \d+: Cửa sổ Cài đặt bộ lọc', '26_filtercfg', None),
    (r'^Hình \d+: Cửa sổ Tùy chỉnh cột', '25_colcfg', None),
    (r'^Hình \d+: Màn lập yêu cầu xuất giữ lúc mới mở', '10_create', None),
    (r'^Hình \d+: Cửa sổ Chọn hợp đồng', '11_contract', None),
    (r'^Hình \d+: Phiếu loại có hợp đồng', '11b_create_hd', None),
    (r'^Hình \d+: Phiếu loại Xuất giữ khác', '12_create_khac',
     'Phiếu loại Xuất giữ khác: chọn Khách hàng, tự thêm từng dòng hàng (Thêm hàng hóa) và chọn đơn vị tính'),
    (r'^Hình \d+: Màn sửa phiếu loại Xuất giữ khác', '12_edit', None),
    (r'^Hình \d+: Màn chi tiết phiếu đã duyệt', '17_detail',
     'Màn chi tiết phiếu Chờ KT duyệt nhìn từ Kế toán: nút In, Từ chối và Lập phiếu xuất giữ ở cuối màn'),
    (r'^Hình \d+: Màn chi tiết nhìn từ người có quyền duyệt', '14_approve_detail', None),
    (r'^Hình \d+: Nút duyệt của cấp hiện tại', '14_approve', 'Hộp thoại Xác nhận duyệt ở bước Ban giám đốc'),
    (r'^Hình \d+: Cửa sổ Từ chối yêu cầu xuất giữ', '15_reject', None),
    (r'^Hình \d+: Hộp thoại Xác nhận xóa phiếu', '13_delete', None),
    (r'^Hình \d+: Yêu cầu ở trạng thái Chờ KT duyệt', '17_detail', None),
    (r'^Hình \d+: Cửa sổ Xem trước yêu cầu xuất giữ', '18_print', None),
    (r'^Hình \d+: Cửa sổ Chọn trường xuất Excel', '20_export', None),
    (r'^Hình \d+: Cửa sổ Lịch sử thay đổi của phiếu', '16_history', None),
]

PART5 = [  # STT | Nhóm (phân hệ) | Màn hình | Đường dẫn (menu cha)
    ('1', 'Tài chính', 'Phiếu xuất giữ (lập từ yêu cầu đang Chờ KT duyệt: nạp dòng hàng được tích Cần xuất, khách hàng, '
     'hợp đồng, người yêu cầu, Giữ đến ngày; lưu nháp / duyệt / xóa phiếu xuất giữ thì đổi trạng thái yêu cầu sang '
     'Đang xuất giữ / Đã duyệt / Chờ KT duyệt)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('2', 'Tài chính', 'Yêu cầu gia hạn hàng giữ (lô hàng giữ sinh từ phiếu xuất giữ được lần ngược về yêu cầu xuất '
     'giữ gốc để lấy hợp đồng của lô)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('3', 'Tài chính', 'Phiếu Yêu cầu điều chuyển hàng giữ (lấy hợp đồng của lô qua yêu cầu xuất giữ gốc, như dòng 2)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
]


# ============================================================== HÀM RIÊNG (mục con Heading4)
def is_sub(e):
    return e.tag == W('p') and style_of(e) in ('', None, 'Heading4') and re.match(r'^\d+\.\d+\.\d+ ', txt(e))


L.is_sub = is_sub  # usecase_block / remove_usecase / add_usecase của thư viện dùng hàm này


def set_style(p, sid):
    ppr = p.find(W('pPr'))
    if ppr is None:
        ppr = L._el('pPr')
        p.insert(0, ppr)
    ps = ppr.find(W('pStyle'))
    if ps is None:
        ps = L._el('pStyle')
        ppr.insert(0, ps)
    ps.set(W('val'), sid)


def renumber_subheadings(doc):
    """2.x.1..2.x.n liên tục trong từng mục, đặt style Heading4 đồng loạt (bản Drive còn vài mục là đoạn thường)."""
    cur, k = None, 0
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading3':
            m = re.match(r'^(\d+\.\d+)\s', txt(e))
            cur, k = (m.group(1) if m else None), 0
        elif cur and is_sub(e):
            k += 1
            title = re.sub(r'^\d+\.\d+\.\d+\s+', '', txt(e))
            new = '%s.%d %s' % (cur, k, title)
            if style_of(e) != 'Heading4':
                log('Đặt style Heading4 cho mục con: ' + txt(e))
                set_style(e, 'Heading4')
            if new != txt(e):
                log('Đánh lại mục con: %s → %s' % (txt(e), new))
                set_runs_text(e, new)


def sec_pars(sec, regex):
    return [e for e in sec[1] if e.tag == W('p') and re.search(regex, txt(e))]


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


def kv_append(kv, key, extra):
    write_cell(kv_row(kv, key), kv_get(kv, key) + (extra if isinstance(extra, list) else [extra]))


def ev_edit(ev, event_regex, old_regex, new, rid=None):
    tc = cells(find_row(ev, 1, event_regex))[3]
    write_cell(tc, lines_replace(cell_lines(tc), old_regex, new), rid)


def ui_set(ui, name_regex, values):
    """values: {chỉ số cột: chữ mới}."""
    tr = find_row(ui, 1, name_regex)
    for i, v in values.items():
        write_cell(cells(tr)[i], v if isinstance(v, list) else [v])


def col(ui, name):
    return header_index(ui, name)


def replace_shot(doc, cap_regex, png, new_cap=None):
    its = items(doc)
    for i, e in enumerate(its):
        if e.tag == W('p') and re.match(cap_regex, txt(e)):
            img = its[i - 1]
            assert list(img.iter(L.A_NS + 'blip')), 'Không có ảnh trước: ' + txt(e)
            set_image(doc, img, os.path.join(SHOTS, png + '.png'))
            if new_cap:
                set_runs_text(e, re.match(r'^Hình \d+:', txt(e)).group(0) + ' ' + new_cap)
            return
    raise KeyError(cap_regex)


def fit_tall_image(doc, max_in=7.6):
    """Ảnh màn dài: giới hạn chiều cao để không tràn trang (thu cả bề rộng theo tỉ lệ)."""
    for ext in doc.element.body.iter(L.WP_NS + 'extent'):
        cx, cy = int(ext.get('cx')), int(ext.get('cy'))
        lim = int(max_in * L.EMU)
        if cy > lim:
            ncx = int(cx * lim / cy)
            ext.set('cx', str(ncx))
            ext.set('cy', str(lim))
            for x in ext.getparent().iter(L.A_NS + 'ext'):
                if x.get('cx'):
                    x.set('cx', str(ncx))
                    x.set('cy', str(lim))


def drop_blank_after_toc(doc):
    """Mục lục vừa kín trang 1 -> đoạn trống sau mục lục bị đẩy sang trang 2, rồi Phần 1 (Heading1 ngắt trang
    trước) sang trang 3 => trang 2 trắng. Bỏ đoạn trống đó và thu nhỏ đoạn kết field của mục lục."""
    sdt = doc.element.body.find(W('sdt'))
    nxt = sdt.getnext()
    while nxt is not None and nxt.tag == W('p') and not txt(nxt).strip() and not list(nxt.iter(L.A_NS + 'blip')):
        rm, nxt = nxt, nxt.getnext()
        rm.getparent().remove(rm)
    ps = sdt.findall('.//' + W('p'))
    last = ps[-1]
    if not txt(last).strip() and len(ps) > 1:
        # đoạn cuối chỉ chứa dấu kết field: chuyển run đó lên cuối dòng mục lục trước rồi bỏ đoạn trống
        prev = ps[-2]
        for r in list(last.findall(W('r'))):
            prev.append(r)
        last.getparent().remove(last)


# ============================================================== XỬ LÝ
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)
    body = doc.element.body

    # 1. Đường dẫn menu đủ cấp ở mọi chỗ
    n = replace_in_texts(body, OLD_MENU, MENU.rsplit('=> ', 1)[0] + '=> ')
    log('Đổi đường dẫn menu: %d chỗ' % n)

    # 2. Quy tắc chung / Tác nhân / Điều kiện ban đầu
    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    # 3. Dòng Menu + câu popup (dòng Menu đầu tiên của mục)
    for rx, (menu, popup) in MENU_LINES.items():
        sec = section(doc, rx)
        p = sec_par(sec, r'^Menu:')
        if menu:
            set_runs_text(p, menu)
        if popup:
            strip_ids(docxlib.clone_par_after(p, p, popup))
    # 2.5: 4 khối Layout — Hình chọn hợp đồng là popup; Hình 11-12 là màn TẠO MỚI (bản Drive ghi nhầm "=> Sửa")
    sec = section(doc, r'^2\.5 ')
    ms = sec_pars(sec, r'^Menu:')
    assert len(ms) == 4, len(ms)
    strip_ids(docxlib.clone_par_after(ms[1], ms[1], 'Modal Chọn hợp đồng được mở ngay trên màn hình Tạo mới theo '
                                                    'đường dẫn ở trên.'))
    set_runs_text(ms[2], 'Menu: %s => Tạo mới (loại có hợp đồng)' % MENU)
    set_runs_text(ms[3], 'Menu: %s => Tạo mới (loại Xuất giữ khác)' % MENU)

    patch_part2(doc)
    patch_sections(doc, rid)
    patch_part4(doc)
    add_part5(doc)
    drop_blank_after_toc(doc)

    # 4. Ảnh chụp mới
    for cap, png, new_cap in SHOTS_REPLACE:
        replace_shot(doc, cap, png, new_cap)
    fit_tall_image(doc)

    # 5. Use Case: bỏ ở 2.3 / 2.4, thêm 2.7, vẽ lại các sơ đồ còn lại kiểu quốc gia
    remove_usecase(doc, section(doc, r'^2\.3 '))
    remove_usecase(doc, section(doc, r'^2\.4 '))
    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.8 '), png, 'Biểu đồ Use Case — %s %s' % (code, name))
        else:
            set_image(doc, blk[1], png)
    renumber_subheadings(doc)
    nfig = renumber_figures(doc)
    log('Số Hình sau khi đánh lại: %d' % nfig)

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        pdf = os.path.join(OUT_DIR, NAME + '.pdf')
        word_finalize(OUT, pdf)
        fix_blank_page2(pdf)


def fix_blank_page2(pdf):
    """Mục lục kín trang 1 -> Word đẩy đoạn kết field sang trang 2 rồi Phần 1 (Heading1 ngắt trang trước) sang
    trang 3 => trang 2 trắng. Khi gặp thì tắt ngắt-trang-trước của riêng tiêu đề Phần 1 và cho Word chạy lại."""
    import pymupdf
    with pymupdf.open(pdf) as p:
        blank = len(p) > 2 and not p[1].get_text().strip() and not p[1].get_images()
    if not blank:
        return
    doc = docx.Document(OUT)
    h = part_heading(doc, 1)
    ppr = h.find(W('pPr'))
    pb = L._el('pageBreakBefore')
    pb.set(W('val'), '0')
    ppr.find(W('pStyle')).addnext(pb)
    doc.save(OUT)
    log('Trang 2 trắng -> bỏ ngắt trang trước ở tiêu đề Phần 1')
    import time
    time.sleep(5)
    try:
        word_finalize(OUT, pdf)
    except RuntimeError:  # lỗi RPC lúc mở/đóng Word liền nhau -> thử lại 1 lần (BRIEF mục Word COM)
        time.sleep(10)
        word_finalize(OUT, pdf)


def patch_part2(doc):
    n = replace_in_texts(doc.element.body, 'Bước này cho phép nhập lại Giữ đến ngày.',
                         'Ở bước này hệ thống kiểm tra lại hạn Giữ đến ngày đang ghi trên phiếu (màn chi tiết không '
                         'có ô nhập lại).')
    assert n == 1, n


def patch_sections(doc, rid):
    # 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    ui = sec_ui(s)
    set_col(ui, col(ui, 'Loại'), r'^Cột Trạng thái$', 'Table/Grid')
    delete_row(ui, r'^Vòng quay chờ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^1\. Người dùng vào menu', '1. Người dùng vào menu %s.' % MENU)

    # 2.2 Tìm kiếm: Enter gộp vào sự kiện Tìm kiếm; ô Ngày tạo là MỘT ô chọn khoảng ngày (code hiện tại)
    s = section(doc, r'^2\.2 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Ngày tạo từ / Ngày tạo đến$', {
        1: 'Ngày tạo', col(ui, 'Phạm vi'): 'dd/mm/yyyy → dd/mm/yyyy',
        col(ui, 'Mô tả'): 'Một ô chọn khoảng ngày (từ ngày → đến ngày) theo ngày tạo phiếu; không phải ngày duyệt '
                          'và không phải hạn giữ.'})
    ui_set(ui, r'^Ô tìm nhanh$', {col(ui, 'Mô tả'): 'Gợi ý “Tìm theo mã phiếu...”. Chỉ tìm khi bấm nút Tìm kiếm '
                                                     'hoặc nhấn Enter.'})
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Bấm nút Tìm kiếm$'))[1], ['Bấm nút Tìm kiếm hoặc nhấn Enter trong ô tìm nhanh'])

    # 2.3 Cài đặt bộ lọc
    s = section(doc, r'^2\.3 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Danh sách ô lọc$', {col(ui, 'Phạm vi'): '10 mục'})
    clone_row_after(sec_ev(s), r'^Bấm Lưu$', [None, 'Kéo thả một ô lọc', 'Drag',
                                             ['After:', '– Đổi thứ tự ô lọc trong cửa sổ; chưa ghi cho tới khi bấm Lưu.']])
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'^• Bấm Đóng', '• Bấm Đóng / (x) → đóng cửa sổ ngay, giữ nguyên cấu hình cũ.')

    # 2.4 Tùy chỉnh cột
    s = section(doc, r'^2\.4 ')
    ui = sec_ui(s)
    set_col(ui, col(ui, 'Loại'), r'^Cột bị khóa$', 'Label')
    clone_row_after(sec_ev(s), r'^Bấm Lưu$', [None, 'Kéo thả một cột', 'Drag',
                                             ['After:', '– Đổi thứ tự cột trong cửa sổ; chưa ghi cho tới khi bấm Lưu.']])

    # 2.5 Tạo mới
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ', '6. Người dùng bấm Lưu nháp, Gửi duyệt hoặc Lưu và tiếp tục.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^8\. ', [
        '8. Ghi nhận hành động Tạo mới (kèm Gửi duyệt nếu bấm Gửi duyệt) trong lịch sử của phiếu.',
        '9. Hệ thống hiển thị thông báo thành công và quay về màn danh sách (Lưu và tiếp tục: ở lại màn Tạo mới để '
        'lập phiếu kế tiếp).'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn khi đã nhập', UNSAVED)
    kv_append(kv, 'Dòng sự kiện phụ', '• Người lập còn hàng quá hạn theo cấu hình hạn của thao tác “Lập yêu cầu xuất '
                                      'giữ” → hệ thống báo “Có hàng … quá hạn!”, không lưu (BR-15).')
    ui = sec_ui(s)
    C = col(ui, 'Loại')
    ui_set(ui, r'^Chọn tệp đính kèm$', {
        1: 'Khối File đính kèm (nút Thêm tài liệu)', C: 'Table/Grid',
        col(ui, 'Giá trị ban đầu'): 'Chưa có dòng tệp',
        col(ui, 'Mô tả'): 'Bấm Thêm tài liệu để thêm một dòng rồi chọn tệp; tệp tải lên ngay. Mỗi dòng có Xem trước, '
                          'Tải xuống, Thay đổi, Xóa và cột Dung lượng.'})
    set_col(ui, C, r'^Cột Đề nghị$', 'Textbox')
    set_col(ui, C, r'^Thông báo lỗi tại ô$', 'Label')
    ui_set(ui, r'^Nút Gửi duyệt$', {col(ui, 'Mô tả'): 'Ghi phiếu và chuyển sang Chờ TP duyệt.'})
    ev = sec_ev(s)
    set_col(ev, 2, r'^Nhập SL đề nghị$', 'Change')
    ev_edit(ev, r'^Nhập SL đề nghị$', r'^– Bằng 0 mà dòng',
            '– Chỉ kiểm khi Gửi duyệt: vượt số Có thể giữ hoặc phần còn lại của hợp đồng → báo “SL đề nghị – Vượt … '
            '(còn …).” ngay dưới ô.')
    ev_edit(ev, r'^Nhập SL đề nghị$', r'^– Vượt phần còn lại', None)
    ev_edit(ev, r'^Bấm Gửi duyệt$', r'thông báo cho Trưởng phòng',
            '– Ghi phiếu ở trạng thái Chờ TP duyệt; ghi lịch sử Tạo mới / Gửi duyệt.')
    for e_rx in (r'^Bấm Lưu nháp$', r'^Bấm Gửi duyệt$', r'^Bấm Lưu và tiếp tục$'):
        add_err_line(ev, e_rx, rid)
    clone_row_after(ev, r'^Bấm Lưu và tiếp tục$',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # 2.6 Chỉnh sửa
    s = section(doc, r'^2\.6 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống kiểm tra dữ liệu, đặt lại toàn bộ các bước duyệt và ghi phiếu theo trạng thái đã chọn.',
        '6. Ghi nhận các thay đổi (kèm Gửi duyệt nếu bấm Gửi duyệt) trong lịch sử của phiếu.',
        '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_append(kv, 'Dòng sự kiện phụ', UNSAVED)
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Gửi duyệt$', rid)
    clone_row_after(ev, r'^Mở màn Sửa$', [None, 'Bấm Lưu nháp', 'Click', [
        'During:', '– Kiểm tra dữ liệu giống chức năng Tạo mới; KHÔNG kiểm tra tồn kho.',
        'After:', '– Ghi lại phiếu, giữ trạng thái Đang tạo; đặt lại dấu duyệt của cả ba cấp.',
        '– Ghi một dòng lịch sử “Chỉnh sửa”, nêu rõ những giá trị đã thay đổi.',
        '– Hiển thị thông báo thành công và quay về màn danh sách.']])
    add_err_line(ev, r'^Bấm Lưu nháp$', rid)  # ghi lại ô để câu {LINK} thành hyperlink
    clone_row_after(ev, r'^Bấm Gửi duyệt$',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # 2.7 Xem chi tiết
    s = section(doc, r'^2\.7 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Khối File đính kèm$', {col(ui, 'Loại'): 'Table/Grid', col(ui, 'Mô tả'):
           'Lưới tệp đính kèm (STT, tệp, Dung lượng); bấm để xem trước hoặc tải xuống.'})
    ui_set(ui, r'^Khối Lịch sử thay đổi$', {col(ui, 'Mô tả'):
           'Thu gọn sẵn; số mốc thay đổi hiện ngay cạnh tiêu đề. Bấm Xem lịch sử để mở danh sách.'})
    ev_edit(sec_ev(s), r'^Bấm Xem lịch sử', r'^– Nạp và hiển thị',
            '– Mở danh sách mốc thay đổi của phiếu (đã nạp sẵn khi vào màn), mới nhất trước.')

    # 2.8 Duyệt — màn chi tiết KHÔNG có ô nhập lại Giữ đến ngày: hệ thống gửi lại hạn đang ghi trên phiếu
    s = section(doc, r'^2\.8 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống chuyển phiếu sang bước tiếp theo.',
        '6. Ghi nhận hành động Duyệt trong lịch sử của phiếu.',
        '7. Hệ thống hiển thị thông báo kết quả và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. Hệ thống hiển thị', None)
    kv_append(kv, 'Dòng sự kiện phụ', '• Trưởng phòng bị chặn theo cấu hình “Chặn trưởng phòng duyệt” của thao tác '
                                      '“Duyệt yêu cầu xuất giữ” → hệ thống báo lỗi, không duyệt (BR-15).')
    kv_set(kv, 'Yêu cầu đặc biệt', 'Màn chi tiết không có ô nhập lại Giữ đến ngày. Khi Ban giám đốc duyệt, hệ thống '
                                   'gửi lại đúng hạn giữ đang ghi trên phiếu và kiểm tra lại hạn đó (bắt buộc, là ngày '
                                   'tương lai, không vượt trần); hạn không hợp lệ thì báo lỗi, không duyệt.')
    ui = sec_ui(s)
    ui_set(ui, r'^Hộp thoại xác nhận duyệt$', {col(ui, 'Loại'): 'Label', col(ui, 'Mô tả'):
           'Tiêu đề “Xác nhận duyệt”; nội dung nêu mã phiếu, bước Ban giám đốc nói thêm phiếu sẽ chuyển sang Kế toán. '
           'Hai nút Duyệt / Hủy.'})
    ui_set(ui, r'^Ô Giữ đến ngày ở bước Ban giám đốc$', {
        1: 'Giữ đến ngày', col(ui, 'Loại'): 'Textbox', col(ui, 'Trạng thái'): 'Disable',
        col(ui, 'Giá trị ban đầu'): 'Theo dữ liệu',
        col(ui, 'Mô tả'): 'Chỉ hiển thị, không sửa được. Ở bước Ban giám đốc, hệ thống gửi lại giá trị này khi duyệt '
                          'và kiểm tra lại hạn giữ.'})
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm nút duyệt', r'^– Bước Ban giám đốc: Giữ đến ngày',
            '– Bước Ban giám đốc: hạn giữ đang ghi trên phiếu trống, không hợp lệ, là ngày quá khứ hoặc vượt trần → '
            'báo lỗi và dừng.')
    ev_edit(ev, r'^Bấm nút duyệt', r'^– Ban giám đốc duyệt: ghi lại hạn giữ mới',
            '– Ban giám đốc duyệt: ghi lại người duyệt, thời điểm duyệt và chuyển sang Chờ KT duyệt.')
    ev_edit(ev, r'^Bấm nút duyệt', r'gửi thông báo cho cấp kế tiếp', '– Ghi một dòng lịch sử “Duyệt”.')
    add_err_line(ev, r'^Bấm nút duyệt', rid)

    # 2.9 Từ chối
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống đưa phiếu về trạng thái Đang tạo và lưu lý do.',
        '6. Ghi nhận hành động Từ chối kèm lý do trong lịch sử của phiếu.',
        '7. Hệ thống báo “Đã từ chối yêu cầu xuất giữ.” và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Lý do quá 255', '• Ô Lý do từ chối nhận tối đa 255 ký tự.')
    kv_append(kv, 'Dòng sự kiện phụ', '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác '
                                      'nhận kể cả khi đã nhập lý do; phiếu giữ nguyên.')
    ui = sec_ui(s)
    ui_set(ui, r'^Lý do$', {1: 'Lý do từ chối'})
    ui_set(ui, r'^Nút xác nhận$', {1: 'Nút Xác nhận từ chối'})
    ui_set(ui, r'^Nút đóng cửa sổ$', {1: 'Nút Đóng'})
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Bấm xác nhận từ chối$'))[1], ['Bấm Xác nhận từ chối'])
    ev_edit(ev, r'^Bấm Xác nhận từ chối$', r'^– Lý do quá 255', None)
    ev_edit(ev, r'^Bấm Xác nhận từ chối$', r'^– Ghi một dòng lịch sử', '– Ghi một dòng lịch sử Từ chối kèm lý do.')
    ev_edit(ev, r'^Bấm Xác nhận từ chối$', r'^– Hiển thị thông báo thành công',
            '– Hiển thị “Đã từ chối yêu cầu xuất giữ.” và quay về màn danh sách.')
    add_err_line(ev, r'^Bấm Xác nhận từ chối$', rid)

    # 2.10 Xóa
    s = section(doc, r'^2\.10 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^4\. ', [
        '4. Hệ thống xóa phiếu và ghi nhận hành động Xóa trong lịch sử của phiếu.',
        '5. Hệ thống báo “Xóa thành công.”: xóa từ danh sách thì nạp lại danh sách, xóa từ màn chi tiết thì quay về '
        'màn danh sách.'])
    ev = sec_ev(s)
    ev_edit(ev, r'^Xác nhận Xóa$', r'^– Xóa phiếu cùng',
            '– Xóa phiếu cùng các dòng hàng của phiếu; ghi một dòng lịch sử Xóa, lịch sử thay đổi được giữ lại.')
    add_err_line(ev, r'^Xác nhận Xóa$', rid)

    # 2.11 Lập phiếu xuất giữ
    s = section(doc, r'^2\.11 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^5\. ',
            '5. Lưu nháp (hoặc nút Không duyệt — nút này cũng chỉ lưu nháp) → yêu cầu chuyển sang Đang xuất giữ.')

    # 2.13 Xuất Excel
    s = section(doc, r'^2\.13 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Ô chọn trường xuất$', {1: 'Danh sách trường xuất', col(ui, 'Loại'): 'Checkbox',
           col(ui, 'Mô tả'): 'Mỗi trường một ô tích kèm tay kéo đổi thứ tự: Mã phiếu, Loại yêu cầu, Người tạo, Ngày '
                             'tạo, Hợp đồng, Khách hàng, Giữ đến ngày, Trạng thái, Người duyệt, Ngày duyệt, Người cập '
                             'nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối.'})
    ui_set(ui, r'^Dòng xem trước thứ tự cột$', {1: 'Số trường đang chọn', col(ui, 'Giá trị ban đầu'): 'Đang chọn 15/15 '
           'trường', col(ui, 'Mô tả'): 'Góc trái cuối cửa sổ; thứ tự cột trong tệp theo đúng thứ tự trong danh sách.'})
    kv_append(sec_kv(s), 'Dòng sự kiện phụ', '• Kết quả lọc rỗng → vẫn xuất tệp gồm tiêu đề và dòng tên cột, không có '
                                             'dòng dữ liệu.')
    clone_row_after(sec_ev(s), r'^Bấm Xuất file$', [None, 'Kéo thả một trường', 'Drag',
                                                   ['After:', '– Đổi thứ tự cột sẽ có trong tệp.']])

    # 2.14 Lịch sử
    s = section(doc, r'^2\.14 ')
    kv = sec_kv(s)
    kv_set(kv, 'Mô tả', 'Hiển thị các mốc thao tác đã thực hiện trên phiếu: tạo mới, chỉnh sửa, gửi duyệt, duyệt, từ '
                        'chối, kèm người thực hiện, thời điểm và nội dung thay đổi.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa có thao tác',
            '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện dòng “Chưa có lịch sử thao tác '
            'nào.”')
    kv_append(kv, 'Dòng sự kiện phụ', '• Bấm Bộ lọc → lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.')
    ui = sec_ui(s)
    ui_set(ui, r'^Nút Xem lịch sử / Thu gọn$', {col(ui, 'Mô tả'): 'Ở màn chi tiết: thu gọn sẵn, bấm để mở / đóng '
                                                                  'danh sách.'})
    clone_row_after(ui, r'^Nút Làm mới$', [None, 'Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị',
                                            'Mở hàng lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.'])
    clone_row_after(ui, r'^Nút Bộ lọc$', [None, 'Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị',
                                           'Chỉ có ở Modal mở từ màn danh sách; đóng cửa sổ.'])
    ui_set(ui, r'^Trạng thái rỗng$', {col(ui, 'Mô tả'): 'Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống '
                                                         'mới: Modal hiện “Chưa có lịch sử thay đổi.”, khối ở màn chi '
                                                         'tiết hiện “Chưa có lịch sử thao tác nào.”.'})
    clone_row_after(sec_ev(s), r'^Bấm Xem lịch sử$', [None, 'Bấm biểu tượng Lịch sử ở cột Hành động', 'Click',
                                                     ['After:', '– Mở Modal Lịch sử yêu cầu xuất giữ của phiếu, mới '
                                                      'nhất trước.']])


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and txt(e).startswith('Phần %d' % n):
            return e
    raise KeyError(n)


def patch_part4(doc):
    h = part_heading(doc, 4)
    tbl = h.getnext()
    while tbl.tag != W('tbl'):
        tbl = tbl.getnext()

    def desc(code, old_regex, new):
        tc = cells(find_row(tbl, 1, '^%s$' % code))[3]
        write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))

    desc('BR-03', r'^– Ban giám đốc nhập lại Giữ đến ngày',
         '– Ở bước Ban giám đốc duyệt, hệ thống kiểm tra lại hạn giữ đang ghi trên phiếu (màn chi tiết không có ô '
         'nhập lại).')
    desc('BR-06', r'^– Ban giám đốc duyệt: nhập lại',
         '– Ban giám đốc duyệt: hệ thống kiểm tra lại hạn giữ rồi chuyển sang Chờ KT duyệt.')
    desc('BR-09', r'^– Nhãn nút là', '– Nút “Không duyệt” ở màn lập Phiếu xuất giữ CHỈ lưu nháp phiếu xuất giữ (yêu '
                                    'cầu sang Đang xuất giữ), KHÔNG trả yêu cầu về người lập; muốn trả về thì Kế toán '
                                    'bấm Từ chối ở màn chi tiết yêu cầu.')
    desc('BR-12', r'^– Nút không dùng được thì ẩn', None)
    last = rows(tbl)[-1]
    for code, name, lines, scope in [
        ('BR-15', 'Chặn khi còn hàng quá hạn theo cấu hình hạn', [
            '– Lập và sửa phiếu bị chặn khi người lập còn hàng quá hạn thuộc nhóm đã cấu hình cho thao tác “Lập yêu '
            'cầu xuất giữ” (hàng giữ / hàng mượn / hàng nhập thẳng quá hạn); câu báo “Có hàng … quá hạn!”.',
            '– Trưởng phòng duyệt bị chặn theo cấu hình “Chặn trưởng phòng duyệt” của thao tác “Duyệt yêu cầu xuất '
            'giữ”.',
            '– Thao tác chưa có cấu hình thì không bị chặn; người có vai trò quản trị hệ thống không bị chặn.'],
         'Tạo mới / Chỉnh sửa / Duyệt'),
        ('BR-16', 'Sau mỗi thao tác đưa người dùng về danh sách', [
            '– Lưu nháp, Gửi duyệt, Duyệt, Từ chối và Xóa ở màn chi tiết xong đều đưa người dùng về màn danh sách.',
            '– Riêng Lưu và tiếp tục ở lại màn Tạo mới để lập phiếu kế tiếp.'], 'Toàn màn hình'),
    ]:
        tr = strip_ids(copy.deepcopy(last))
        tbl.append(tr)
        cs = cells(tr)
        write_cell(cs[1], [code])
        write_cell(cs[2], [name])
        write_cell(cs[3], lines)
        write_cell(cs[4], [scope])
        last = tr
    renumber_stt(tbl)
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5: Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    intro = strip_ids(docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc dữ liệu do %s ghi ra '
                                              '(yêu cầu nguồn, dòng hàng được tích Cần xuất, hợp đồng và hạn giữ).'
                                              % SCREEN))
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1500, 3600, 2900])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()
