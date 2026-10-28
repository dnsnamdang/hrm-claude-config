# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu yêu cầu chuyển hàng" (STT 26, bản Drive 28/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Phiếu yêu cầu chuyển hàng.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Chạy lại bao nhiêu lần cũng được: luôn đọc bản Drive gốc. Khuôn chép từ màn 27
(finance-product-import-direct-transfer/form_qg/patch_srs.py); hàm dùng chung ở
../../phieu-theo-form-quoc-gia/formqg_lib.py. Nội dung đã đối chiếu CODE nhánh develop (28/10/2026):
hrm-client/pages/finance/product-transfer-requests/*, hrm-api ProductTransferRequest*.
"""
import copy
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
import docx  # noqa: E402
from formqg_lib import *  # noqa: E402,F401
import formqg_lib as L  # noqa: E402
import docxlib  # noqa: E402

SRC = os.path.join(HERE, 'drive_0710', 'SRS_Drive.docx')
OUT_DIR = os.path.join(HERE, 'out')
OUT = os.path.join(OUT_DIR, 'SRS - Phiếu yêu cầu chuyển hàng.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Phiếu yêu cầu chuyển hàng'
# finance.js: hubGroup 'Hàng hoá - Dịch vụ - Vận chuyển' > nhóm 'Xuất hàng' > 'Phiếu yêu cầu chuyển hàng'
# (bản Drive ghi nhầm "Điều chuyển => Phiếu điều chuyển hàng" — đó là màn KHÁC, /finance/product-transfers)
MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Xuất hàng => Phiếu yêu cầu chuyển hàng'
# sale-hub.js: nhóm 'Yêu cầu' > 'Hàng hóa' > 'YC chuyển hàng' (cùng route)
MENU_SALE = 'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => YC chuyển hàng'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; '
              'bấm Thoát thì rời màn và bỏ thay đổi, bấm Ở lại thì giữ nguyên màn.']

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem yêu cầu chuyển hàng theo tổng công ty / công ty / '
              'phòng ban / bộ phận (V1–V4); không có quyền nào thì chỉ thấy phiếu do mình lập.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (V1–V4); không có quyền nào vẫn xem được phiếu do chính mình lập.')
ACTOR_OWNER = ('Người lập phiếu — người dùng có quyền thực hiện chức năng: chỉ người đã lập phiếu '
               '(chức năng không gắn quyền riêng).')
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Đang tạo.')
ACTOR_VIEW = ('Người dùng có quyền xem phiếu: người lập phiếu; người có quyền Kế toán kho (Q1) cùng công ty với '
              'phiếu; hoặc quản trị hệ thống.')
COND_VIEW = ('1. Đăng nhập thành công.\n'
             '2. Là người lập phiếu, hoặc có quyền Kế toán kho (Q1) cùng công ty với phiếu, hoặc là quản trị hệ thống.\n'
             '3. Phiếu Đang tạo chỉ người lập xem được.')
ACTOR_KTK = 'Người dùng có quyền Kế toán kho (Q1) (hoặc quản trị hệ thống), cùng công ty với phiếu.'
COND_KTK = ('1. Đăng nhập thành công.\n'
            '2. Có quyền Kế toán kho (Q1) hoặc là quản trị hệ thống, và cùng công ty với phiếu.\n'
            '3. Phiếu đang ở trạng thái Chờ duyệt.')
ACTOR_FORM = ('Người lập phiếu — người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình '
              '(chức năng không gắn quyền riêng).')
COND_FORM = ('1. Đăng nhập thành công.\n2. Vào được màn Phiếu yêu cầu chuyển hàng (không gắn quyền riêng).\n'
             '3. Đang ở màn Tạo mới hoặc Sửa phiếu.')

# Mục 2.x: regex tiêu đề -> (vế sau link "Quy tắc chung", Tác nhân, Điều kiện ban đầu)
SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST,
                COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.3 ': ('Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.', ACTOR_LIST,
                COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.4 ': ('Quy tắc Excel và Cấu hình cột.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.5 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_FORM,
                '1. Đăng nhập thành công.\n2. Vào được màn Phiếu yêu cầu chuyển hàng (lập phiếu không gắn quyền '
                'riêng).'),
    r'^2\.6 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.7 ': ('Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.', ACTOR_FORM, COND_FORM),
    r'^2\.8 ': ('Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.', ACTOR_FORM,
                COND_FORM + '\n4. Phiếu đã có ít nhất một dòng hàng hoá.'),
    r'^2\.9 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_VIEW, COND_VIEW),
    r'^2\.10 ': ('Quy tắc xóa và Thông báo.', ACTOR_OWNER, COND_OWNER),
    r'^2\.11 ': ('Thông báo, Validate dữ liệu, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.',
                 ACTOR_KTK, COND_KTK),
    r'^2\.12 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_KTK, COND_KTK),
    r'^2\.13 ': ('Quy tắc màn In và bố cục bản in.', ACTOR_VIEW,
                 COND_VIEW.replace('3. Phiếu Đang tạo chỉ người lập xem được.', '3. Phiếu nằm trong phạm vi xem '
                                   'chi tiết như mục Tác nhân.')),
    r'^2\.14 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_LIST,
                 COND_LIST + '\n3. Nhìn thấy phiếu trên danh sách hoặc mở được màn chi tiết phiếu.'),
}

# Dòng "Menu:" + câu popup ngay sau (None = không có popup)
MENU_LINES = {
    r'^2\.1 ': ('Menu: %s' % MENU, None),
    r'^2\.2 ': ('Menu: %s => Tìm kiếm nâng cao' % MENU, None),
    r'^2\.3 ': ('Menu: %s => Cài đặt bộ lọc / Tùy chỉnh cột' % MENU,
                'Modal Cài đặt bộ lọc và Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.4 ': ('Menu: %s => Xuất Excel' % MENU,
                'Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.5 ': ('Menu: %s => Tạo mới' % MENU, None),
    r'^2\.6 ': ('Menu: %s => Sửa (trên dòng phiếu) / Xem chi tiết => Sửa' % MENU,
                'Hộp xác nhận xóa tệp đính kèm được mở ngay trên màn hình Sửa phiếu theo đường dẫn ở trên.'),
    r'^2\.7 ': ('Menu: %s => Tạo mới / Sửa => dấu + ở tiêu đề bảng hàng hóa' % MENU,
                'Modal Thêm hàng hoá được mở ngay trên màn hình Tạo mới hoặc Sửa phiếu theo đường dẫn ở trên.'),
    r'^2\.8 ': ('Menu: %s => Tạo mới / Sửa => ô Khách hàng của dòng hàng hóa' % MENU,
                'Modal Chọn khách hàng được mở ngay trên màn hình Tạo mới hoặc Sửa phiếu theo đường dẫn ở trên.'),
    r'^2\.9 ': ('Menu: %s => bấm Mã yêu cầu (Xem chi tiết)' % MENU, None),
    r'^2\.10 ': ('Menu: %s => Xóa (trên dòng phiếu)' % MENU,
                 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.11 ': ('Menu: %s => Xem chi tiết => Không duyệt' % MENU,
                 'Modal Xác nhận không duyệt được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
    r'^2\.12 ': ('Menu: %s => Tổng hợp (trên dòng phiếu) / Xem chi tiết => Tổng hợp' % MENU,
                 'Bấm Tổng hợp chuyển sang màn Tạo yêu cầu xuất hàng (Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận '
                 'chuyển => Xuất hàng => Yêu cầu xuất hàng) ngay trên tab hiện tại, nạp sẵn phiếu đang xem.'),
    r'^2\.13 ': ('Menu: %s => In (trên dòng phiếu) / Xem chi tiết => In' % MENU,
                 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo '
                 'đường dẫn ở trên.'),
    r'^2\.14 ': ('Menu: %s => Lịch sử (trên dòng phiếu; phiếu Đang tạo nằm trong menu ba chấm) / Xem chi tiết => '
                 'khối Lịch sử' % MENU,
                 'Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử nằm '
                 'cuối màn hình chi tiết phiếu.'),
}

# Use Case (vẽ lại kiểu quốc gia: tác nhân -> 1 use case)
USECASES = {
    r'^2\.4 ': ('Người dùng có quyền', 'FR-04', 'Xuất Excel danh sách', 'io'),
    r'^2\.5 ': ('Người lập phiếu', 'FR-05', 'Tạo mới phiếu yêu cầu chuyển hàng', 'crud'),
    r'^2\.6 ': ('Người lập phiếu', 'FR-06', 'Sửa phiếu', 'crud'),
    r'^2\.7 ': ('Người lập phiếu', 'FR-07', 'Chọn hàng hóa từ popup', 'crud'),
    r'^2\.8 ': ('Người lập phiếu', 'FR-08', 'Chọn khách hàng từ popup', 'crud'),
    r'^2\.9 ': ('Người dùng có quyền', 'FR-09', 'Xem chi tiết phiếu', 'view'),
    r'^2\.10 ': ('Người lập phiếu', 'FR-10', 'Xóa phiếu', 'action'),
    r'^2\.11 ': ('Kế toán kho', 'FR-11', 'Không duyệt phiếu', 'action'),
    r'^2\.12 ': ('Kế toán kho', 'FR-12', 'Tổng hợp sang Yêu cầu xuất hàng', 'action'),
    r'^2\.13 ': ('Người dùng có quyền', 'FR-13', 'In phiếu', 'io'),
}

# Ảnh thay bằng ảnh chụp DEV 28/10 (bộ ảnh HDSD): regex chú thích -> (ảnh, chú thích mới | None)
IMAGES = [
    (r'lúc mới truy cập', '01_list', 'Màn danh sách Phiếu yêu cầu chuyển hàng lúc mới truy cập'),
    (r'Khối Tìm kiếm nâng cao', '02_filter', 'Khối Tìm kiếm nâng cao khi đang mở (5 ô lọc)'),
    (r'Cửa sổ Cài đặt bộ lọc', '26_filtercfg', None),
    (r'Cửa sổ Tùy chỉnh cột', '25_colcfg', None),
    (r'Cửa sổ Chọn trường xuất file', '20_export', 'Cửa sổ Chọn trường xuất file (tích sẵn các cột đang hiển thị)'),
    (r'khi vừa mở', '10_create_empty', None),
    (r'Màn Thêm phiếu sau khi', '10_create', 'Màn Thêm phiếu sau khi đã thêm hàng hoá và dòng khách hàng'),
    (r'Màn Sửa phiếu', '12_edit', None),
    (r'Cửa sổ Thêm hàng hoá', '11_product', None),
    (r'Cửa sổ Chọn khách hàng', '11b_customer', None),
    (r'Màn chi tiết phiếu Chờ duyệt', '17_detail', 'Màn chi tiết phiếu Chờ duyệt, xem bằng tài khoản có quyền Kế '
                                                  'toán kho — có Không duyệt, In, Tổng hợp, Quay lại'),
    (r'Màn chi tiết phiếu nháp', '17b_detail_draft', 'Màn chi tiết phiếu Đang tạo của chính người xem — có Sửa, In, '
                                                     'Quay lại'),
    (r'Hộp xác nhận xóa phiếu', '13_delete', None),
    (r'Hộp xác nhận không duyệt', '15_reject', 'Hộp xác nhận không duyệt kèm ô Ghi chú duyệt'),
    (r'Vui lòng nhập ghi chú duyệt', '15b_reject_err', 'Lỗi “Vui lòng nhập ghi chú duyệt” khi bấm Không duyệt lúc ô '
                                                     'Ghi chú duyệt còn trống'),
    (r'Nút Tổng hợp', '19_summary', 'Màn Tạo yêu cầu xuất hàng mở từ nút Tổng hợp, nạp sẵn phiếu yêu cầu chuyển hàng'),
    (r'Bản in phiếu', '18_print', 'Cửa sổ Xem trước phiếu yêu cầu chuyển hàng'),
    (r'Cửa sổ Lịch sử thay đổi', '16_history', None),
]

PART5 = [  # STT | Nhóm (phân hệ) | Màn hình | Đường dẫn (menu cha) — grep code 28/10/2026
    ('1', 'Tài chính', 'Yêu cầu xuất hàng — loại Xuất điều chuyển kho chi nhánh: chọn và nạp phiếu yêu cầu chuyển '
     'hàng (cùng một người yêu cầu), gắn mã yêu cầu xuất hàng vào phiếu; nút Tổng hợp mở màn này',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('2', 'Tài chính', 'Đề nghị nhập kho — duyệt đề nghị nhập kho của yêu cầu xuất hàng loại điều chuyển chi nhánh '
     'cập nhật trạng thái các phiếu yêu cầu chuyển hàng liên quan',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Nhập hàng'),
    ('3', 'Tài chính', 'Phiếu xuất hàng — xuất hàng cho yêu cầu xuất hàng loại điều chuyển chi nhánh cập nhật trạng '
     'thái các phiếu yêu cầu chuyển hàng liên quan', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('4', 'Tài chính', 'Phiếu phân bổ hàng điều chuyển chi nhánh — đọc dòng hàng và dòng khách hàng của phiếu để '
     'phân bổ (mở từ nút Phân bổ hàng ở chi tiết Phiếu nhập hàng)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Nhập hàng -> Phiếu nhập hàng'),
    ('5', 'Danh mục', 'Hàng hoá, vật tư — xóa hàng hóa: chặn khi hàng đã có trên phiếu yêu cầu chuyển hàng',
     'Danh mục -> Hàng hoá'),
]


# ============================================================== HÀM PHỤ
def lines_replace(lines, old_regex, new):
    out = []
    for l in lines:
        if re.search(old_regex, l):
            if new is not None:
                out.extend(new if isinstance(new, list) else [new])
        else:
            out.append(l)
    return out


def kv_edit(kv, key, old_regex, new):
    write_cell(kv_row(kv, key), lines_replace(kv_get(kv, key), old_regex, new))


def kv_put(kv, key, lines, rid=None):
    write_cell(kv_row(kv, key), lines if isinstance(lines, list) else lines.split('\n'), rid)


def ev_edit(ev, event_regex, old_regex, new):
    tc = cells(find_row(ev, 1, event_regex))[3]
    write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))


def ev_put(ev, event_regex, lines, name=None, kind=None):
    tr = find_row(ev, 1, event_regex)
    if name:
        write_cell(cells(tr)[1], [name])
    if kind:
        write_cell(cells(tr)[2], [kind])
    write_cell(cells(tr)[3], lines)


def row_put(tbl, regex, **cols):
    """Sửa ô theo TÊN cột tiêu đề: row_put(ui, '^Ngày lập$', **{'Tên đối tượng': 'Ngày tạo', 'Loại': 'Textbox'})."""
    tr = find_row(tbl, 1, regex)
    for name, val in cols.items():
        write_cell(cells(tr)[header_index(tbl, name)], val if isinstance(val, list) else [val])


def set_rows(tbl, data):
    """Dựng lại toàn bộ dòng dữ liệu của bảng theo khuôn dòng dữ liệu đầu (cột STT tự đánh)."""
    trs = rows(tbl)
    tpl = trs[1]
    for tr in trs[1:]:
        tbl.remove(tr)
    for vals in data:
        tr = strip_ids(copy.deepcopy(tpl))
        tbl.append(tr)
        for tc, v in zip(cells(tr)[1:], vals):
            write_cell(tc, v if isinstance(v, list) else [v])
    renumber_stt(tbl)


def replace_img(doc, cap_regex, png, new_cap=None):
    for e in items(doc):
        if e.tag == W('p') and re.match(r'^Hình \d+: .*' + cap_regex, txt(e)):
            img = e.getprevious()
            assert list(img.iter(A_NS + 'blip')), 'không thấy ảnh trước chú thích ' + txt(e)
            set_image(doc, img, os.path.join(SHOTS, png + '.png'))
            if new_cap:
                n = re.match(r'^(Hình \d+:)', txt(e)).group(1)
                set_runs_text(e, '%s %s' % (n, new_cap))
            return
    raise KeyError(cap_regex)


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and re.match(r'^Phần %d\b' % n, txt(e)):
            return e
    raise KeyError(n)


# ============================================================== XỬ LÝ
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)

    # 1. Quy tắc chung / Tác nhân / Điều kiện ban đầu
    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    # 2. Dòng Menu + câu popup
    for rx, (menu, popup) in MENU_LINES.items():
        sec = section(doc, rx)
        p = sec_par(sec, r'^Menu:')
        set_runs_text(p, menu)
        nxt = p.getnext()
        is_old = nxt is not None and nxt.tag == W('p') and re.search(r'được mở|Nút Tổng hợp nằm', txt(nxt))
        if popup and is_old:
            set_runs_text(nxt, popup)
        elif popup:
            strip_ids(docxlib.clone_par_after(p, p, popup))
    p = sec_par(section(doc, r'^2\.1 '), r'^Menu:')
    strip_ids(docxlib.clone_par_after(p, p, 'Hoặc Menu: %s (cùng màn hình).' % MENU_SALE))
    log('Đường dẫn menu: Điều chuyển => Phiếu điều chuyển hàng  →  Xuất hàng => Phiếu yêu cầu chuyển hàng')

    patch_part1_2(doc)
    patch_sections(doc, rid)
    patch_part4(doc)
    add_part5(doc)

    # 3. Ảnh chụp mới
    for rx, png, cap in IMAGES:
        replace_img(doc, rx, png, cap)
    log('Thay %d ảnh màn hình bằng ảnh chụp DEV 28/10' % len(IMAGES))

    # 4. Use Case: bỏ ở FR-03, thêm FR-09, vẽ lại các sơ đồ còn lại
    remove_usecase(doc, section(doc, r'^2\.3 '))
    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.10 '), png, 'Biểu đồ Use Case — %s %s' % (code, name))
        else:
            set_image(doc, blk[1], png)
            set_runs_text(blk[2], re.match(r'^(Hình \d+:)', txt(blk[2])).group(1) +
                          ' Biểu đồ Use Case — %s %s' % (code, name))
    renumber_subheadings(doc)
    nfig = renumber_figures(doc)
    log('Số Hình sau khi đánh lại: %d' % nfig)

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        word_finalize(OUT, os.path.join(OUT_DIR, 'SRS - Phiếu yêu cầu chuyển hàng.pdf'))


def patch_part1_2(doc):
    """Thuật ngữ + ma trận: Tổng hợp nay sang màn HRM Yêu cầu xuất hàng – Tạo mới (không còn tab ERP)."""
    for t in doc.element.body.iter(W('tbl')):
        hdr = [txt(c).strip() for c in cells(rows(t)[0])]
        if hdr[:2] == ['Thuật ngữ', 'Mô tả']:
            write_cell(cells(find_row(t, 0, r'^Tổng hợp$'))[1], [
                'Thao tác chuyển sang màn Tạo yêu cầu xuất hàng của hệ thống HRM (loại Xuất điều chuyển kho chi '
                'nhánh) ngay trên tab hiện tại, nạp sẵn phiếu đang xem. Không làm đổi trạng thái phiếu.'])
            write_cell(cells(find_row(t, 0, r'^SL tồn$'))[1], [
                'Tồn tham khảo tại kho đang chọn ở ô “Xem tồn theo kho”, đã quy đổi theo đơn vị tính đang chọn. '
                'Chưa chọn kho hoặc chưa có dữ liệu tồn thì ô để trống. Hệ thống không chặn khi số lượng đề nghị '
                'vượt tồn.'])
        if hdr and hdr[0] == 'Chức năng':
            for tr in rows(t)[1:]:
                tc = cells(tr)[0]
                if 'FR-12' in txt(tc):
                    write_cell(tc, ['FR-12 Tổng hợp sang Yêu cầu xuất hàng'])


def patch_sections(doc, rid):
    # ---------------- 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. Người dùng vào menu',
            '1. Người dùng vào menu %s (hoặc %s).' % (MENU, MENU_SALE))
    ui = sec_ui(s)
    row_put(ui, r'^Cột Người tiếp nhận$', **{'Mô tả': 'Chưa ai xử lý thì để trống.'})
    row_put(ui, r'^Cột Trạng thái$', **{'Loại': 'Table/Grid'})
    row_put(ui, r'^Cột Hành động$', **{'Mô tả': (
        'Luôn hiển thị, không tắt được. Thứ tự nút: Sửa, Xóa (phiếu Đang tạo của chính mình), Tổng hợp (Kế toán kho, '
        'phiếu Chờ duyệt cùng công ty), In, Lịch sử; nút không đủ điều kiện bị ẩn. Từ 4 nút trở lên thì hiện 2 nút '
        'đầu + nút ba chấm chứa phần còn lại.')})
    delete_row(ui, r'^Vòng quay chờ')

    # ---------------- 2.2 Tìm kiếm và lọc
    s = section(doc, r'^2\.2 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Khoảng ngày ngược', None)
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Màn không có ô lọc Công ty / Phòng ban; phạm vi phiếu do quyền xem quyết định.'])
    ui = sec_ui(s)
    row_put(ui, r'^Nút Tìm kiếm nâng cao$', **{'Mô tả': 'Đóng/mở khối 5 ô lọc; đổi chữ thành “Ẩn tìm kiếm nâng cao” '
                                                       'khi đang mở.'})
    row_put(ui, r'^Ô lọc Ngày tạo từ$', **{'Tên đối tượng': 'Ô lọc Ngày tạo', 'Phạm vi': 'dd/mm/yyyy – dd/mm/yyyy',
                                          'Mô tả': 'Một ô chọn khoảng ngày (từ ngày – đến ngày); lọc theo Ngày tạo '
                                                   'phiếu, lấy trọn ngày cuối.'})
    delete_row(ui, r'^Ô lọc Ngày tạo đến$')
    ev = sec_ev(s)
    delete_row(ev, r'^Gõ vào ô tìm nhanh')
    tr = find_row(ev, 1, r'^Bấm nút Tìm kiếm$')
    write_cell(cells(tr)[1], ['Bấm nút Tìm kiếm hoặc nhấn Enter trong ô tìm nhanh'])
    write_cell(cells(tr)[3], ['Before:', '– Gõ vào ô tìm nhanh chỉ ghi nhận giá trị, chưa truy vấn.'] +
               cell_lines(cells(tr)[3]))

    # ---------------- 2.3 Cài đặt bộ lọc / Tùy chỉnh cột
    s = section(doc, r'^2\.3 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'đủ 6 ô',
            '• Bấm Khôi phục mặc định ở cửa sổ Cài đặt bộ lọc → đưa về đủ 5 ô theo thứ tự ban đầu.')
    ui = sec_ui(s)
    row_put(ui, r'^Tay cầm kéo thả$', **{'Loại': 'Icon Button'})

    # ---------------- 2.4 Xuất Excel
    s = section(doc, r'^2\.4 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. ',
            '2. Hệ thống mở cửa sổ Chọn trường xuất file, tích sẵn đúng các cột đang hiển thị trên bảng danh sách.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ',
            '3. Người dùng tích / bỏ tích các trường và kéo biểu tượng ☰ để đổi thứ tự cột trong tệp.')
    kv_put(kv, 'Yêu cầu đặc biệt', ['Tên tệp cố định: danh_sach_yeu_cau_chuyen_hang.xlsx. Tệp có ảnh tiêu đề thư ở '
                                    'đầu, dòng tiêu đề “DANH SÁCH YÊU CẦU CHUYỂN HÀNG”, dòng khoảng ngày (nếu có '
                                    'lọc Ngày tạo), dòng tên cột và khối ký “Người lập”.'])
    ui = sec_ui(s)
    row_put(ui, r'^Ô Trường xuất$', **{'Tên đối tượng': 'Danh sách trường', 'Loại': 'Checkbox',
                                      'Phạm vi': 'Danh sách 6 trường', 'Bắt buộc': 'Có ít nhất một trường',
                                      'Giá trị ban đầu': 'Tích sẵn các cột đang hiển thị trên bảng',
                                      'Mô tả': 'Sáu trường: Mã yêu cầu, Người tiếp nhận, Người tạo, Ngày tạo, Trạng '
                                               'thái, Ngày tiếp nhận. Mỗi dòng có ô tích và biểu tượng ☰ để kéo đổi '
                                               'thứ tự cột.'})
    row_put(ui, r'^Dòng “Thứ tự cột trong file”$', **{
        'Tên đối tượng': 'Dòng hướng dẫn',
        'Giá trị ban đầu': 'Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file.', 'Mô tả': '–'})
    row_put(ui, r'^Dòng “Đang chọn n/6 trường”$', **{'Giá trị ban đầu': 'Đang chọn x/6 trường (x = số cột đang hiện)'})
    row_put(ui, r'^Nút Chọn tất cả$', **{'Mô tả': 'Tích lại đủ 6 trường.'})
    row_put(ui, r'^Nút Xuất file$', **{'Mô tả': 'Không bấm được khi chưa tích trường nào hoặc đang dựng tệp.'})
    ev = sec_ev(s)
    ev_put(ev, r'^Bấm nút Xuất Excel$', ['After:', '– Mở cửa sổ Chọn trường xuất file, tích sẵn đúng các cột đang '
                                                   'hiển thị trên bảng.'])

    # ---------------- 2.5 Tạo mới
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_put(kv, 'Dòng sự kiện chính', [
        '1. Người dùng bấm nút Tạo mới.',
        '2. Hệ thống mở màn Thêm phiếu yêu cầu chuyển hàng, điền sẵn Ngày tạo là hôm nay, Người tạo là người đang '
        'đăng nhập và chọn sẵn kho mặc định ở ô Xem tồn theo kho.',
        '3. Người dùng thêm hàng hoá từ popup (FR-07), chọn đơn vị tính, nhập các dòng khách hàng (khách hàng – '
        'FR-08, số lượng, ngày cần, ghi chú) và bấm Thêm tài liệu để đính kèm tệp PDF.',
        '4. Người dùng bấm Lưu nháp (trạng thái Đang tạo), Lưu và tiếp tục (lưu nháp rồi lập tiếp phiếu khác) hoặc '
        'Lưu và gửi duyệt (trạng thái Chờ duyệt, có hộp xác nhận).',
        '5. Hệ thống kiểm tra dữ liệu, ghi phiếu, sinh mã tự động dạng PYCCH kèm 5 chữ số và ghi công ty / phòng ban '
        '/ bộ phận theo hồ sơ người lập.',
        '6. Ghi nhận hành động Tạo mới trong lịch sử của phiếu.',
        '7. Nếu gửi duyệt, hệ thống gửi thông báo cho mọi người có quyền Kế toán kho cùng công ty với phiếu.',
        '8. Hệ thống hiển thị thông báo thành công và quay về màn danh sách (Lưu và tiếp tục: ở lại màn Tạo mới với '
        'form trống).'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Quay lại khi đã nhập dở', UNSAVED)
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Bấm Lưu và tiếp tục → lưu như Lưu nháp (trạng thái Đang tạo), hiển thị thông báo thành công rồi mở lại '
        'form Tạo mới trống.'])
    kv_edit(kv, 'Yêu cầu đặc biệt', r'Giá niêm yết và SL tồn',
            'Lưu nháp KHÔNG gửi thông báo cho ai và phiếu chỉ người lập nhìn thấy. Ô Giá niêm yết và SL tồn chỉ để '
            'tham khảo, không lưu vào phiếu và không chặn khi số lượng vượt tồn.')
    ui = sec_ui(s)
    row_put(ui, r'^Ngày lập$', **{'Tên đối tượng': 'Ngày tạo', 'Loại': 'Textbox'})
    row_put(ui, r'^Người lập$', **{'Tên đối tượng': 'Người tạo', 'Loại': 'Textbox'})
    row_put(ui, r'^Ô Xem tồn theo kho$', **{'Mô tả': 'Đổi kho làm nạp lại cột SL tồn của mọi dòng. Chọn “Xem tồn” '
                                                    '(rỗng) thì cột SL tồn để trống, không truy vấn tồn.'})
    row_put(ui, r'^Cột Giá niêm yết$', **{'Loại': 'Table/Grid', 'Mô tả': 'Chỉ tham khảo, không lưu vào phiếu, không '
                                                                         'có trên bản in. Chưa có giá thì để trống.'})
    row_put(ui, r'^Cột SL tồn$', **{'Loại': 'Table/Grid', 'Mô tả': 'Đã quy đổi theo đơn vị đang chọn. Chưa chọn kho '
                                                                   'hoặc chưa có dữ liệu tồn thì để trống. Không chặn '
                                                                   'khi số lượng vượt tồn.'})
    row_put(ui, r'^Ô SL của dòng con$', **{'Loại': 'Textbox', 'Phạm vi': '1 – 999,999,999'})
    row_put(ui, r'^Khối File đính kèm$', **{
        'Loại': 'Table/Grid', 'Mô tả': 'Bấm Thêm tài liệu để chọn tệp PDF (tối đa 20 MB mỗi tệp); tệp tải lên ngay để '
                                      'xem trước. Bắt buộc ít nhất 1 tệp khi tạo mới.'})
    clone_row_after(ui, r'^Nút Lưu nháp$', [None, 'Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', None, None,
                                           'Hiển thị', 'Chỉ có ở màn Tạo mới. Lưu như Lưu nháp rồi mở lại form trống '
                                                       'để lập tiếp phiếu khác.'])
    row_put(ui, r'^Nút Quay lại$', **{'Mô tả': 'Về màn danh sách; hỏi xác nhận nếu còn thay đổi chưa lưu.'})
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm nút Tạo mới$', r'Mở màn Thêm phiếu',
            '– Mở màn Thêm phiếu với Ngày tạo là hôm nay, Người tạo là người đang đăng nhập, bảng hàng hóa trống và '
            'kho mặc định đã chọn sẵn.')
    ev_edit(ev, r'^Đổi ô Xem tồn theo kho$', r'Nạp lại SL tồn',
            '– Nạp lại SL tồn cho toàn bộ dòng hàng hoá. Chọn giá trị rỗng thì để trống cột SL tồn mà không truy vấn.')
    tr = find_row(ev, 1, r'^Chọn tệp đính kèm$')
    write_cell(cells(tr)[1], ['Bấm Thêm tài liệu và chọn tệp'])
    ev_edit(ev, r'^Bấm Thêm tài liệu', r'danh sách chờ',
            '– Tệp hợp lệ được tải lên ngay và hiện trong bảng File đính kèm (xem trước được); chỉ gắn vào phiếu khi '
            'bấm lưu.')
    ev_edit(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$', r'KHÔNG thực hiện bước After',
            '– Nếu có lỗi thì cuộn tới ô lỗi đầu tiên.')
    add_err_line(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$', [None, 'Bấm Lưu và tiếp tục', 'Click', [
        'Before:', '– Áp cùng bộ kiểm tra của nút Lưu nháp.',
        'After:', '– Lưu phiếu ở trạng thái Đang tạo, ghi một dòng lịch sử “Tạo mới”.',
        '– Hiển thị thông báo lưu thành công, ở lại màn Tạo mới với form trống (không về màn danh sách).']])
    add_err_line(ev, r'^Bấm Lưu và tiếp tục$', rid)
    ev_put(ev, r'^Bấm Quay lại khi đã nhập dở$', UNSAVED_EV, name='Bấm Quay lại / chọn menu khác / đóng tab trình duyệt')

    # ---------------- 2.6 Sửa
    s = section(doc, r'^2\.6 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ',
            '6. Ghi nhận các thay đổi trong lịch sử của phiếu; nếu trạng thái đổi thì ghi riêng một dòng thay đổi '
            'trạng thái.')
    write_cell(kv_row(kv, 'Dòng sự kiện chính'), kv_get(kv, 'Dòng sự kiện chính') + [
        '8. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Quay lại khi đã sửa dở', UNSAVED)
    ui = sec_ui(s)
    row_put(ui, r'^Ngày lập$', **{'Tên đối tượng': 'Ngày tạo', 'Loại': 'Textbox'})
    row_put(ui, r'^Người lập$', **{'Tên đối tượng': 'Người tạo', 'Loại': 'Textbox'})
    row_put(ui, r'^Khối File đính kèm$', **{'Loại': 'Table/Grid'})
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$', r'^– Nếu có lỗi', None)
    add_err_line(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])
    add_err_line(ev, r'^Bấm nút xoá tệp đính kèm đã lưu$', rid)

    # ---------------- 2.7 Chọn hàng hóa (popup dùng chung màn Báo giá: QuotationProductSearchModal)
    s = section(doc, r'^2\.7 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ',
            '3. Người dùng lọc theo cây catalog, gõ vào ô tìm nhanh (mã, tên, model, barcode, mã đặt hàng) hoặc bấm '
            'Tìm kiếm nâng cao, rồi tích chọn một hoặc nhiều dòng.')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Bấm Đóng / (x) → cửa sổ đóng ngay, không hỏi xác nhận; click ra ngoài cửa sổ không đóng cửa sổ.'])
    set_rows(sec_ui(s), [
        ['Ô tìm trong cây catalog', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Lọc nhanh các nhóm trong cây catalog bên trái.'],
        ['Cây catalog', 'Table/Grid', 'Enable', '–', 'Không', 'Tất cả hàng hoá',
         'Chọn nhóm để lọc danh sách hàng; mỗi nhóm kèm số hàng hoá.'],
        ['Ô tìm nhanh hàng hoá', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         'Gợi ý “Tìm theo mã, tên hàng hoá, model, barcode, mã đặt hàng”.'],
        ['Công tắc Còn tồn', 'Checkbox', 'Enable', '–', 'Không', 'Tắt', 'Bật thì chỉ hiện hàng còn tồn.'],
        ['Công tắc Gồm hàng ngoài catalog', 'Checkbox', 'Enable', '–', 'Không', 'Bật',
         'Bật thì hiện cả hàng chưa xếp vào catalog.'],
        ['Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Mở thêm các ô lọc chi tiết của danh mục hàng hoá.'],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa điều kiện tìm, nạp lại danh sách.'],
        ['Ô tích chọn dòng', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Bỏ tích',
         'Hàng đã có trong phiếu bị khóa, không chọn lại được.'],
        ['Bảng danh mục hàng hoá', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
         'Cột STT, Ảnh, Mã hàng, Tên hàng hoá, Model, Thương hiệu, Loại sản phẩm và các cột giá, tồn.'],
        ['Phân trang của cửa sổ', 'Pagination', 'Enable', '–', '–', 'Trang 1, cỡ 20',
         'Chuyển trang không làm mất các dòng đã tích.'],
        ['Nút Thêm N hàng hoá', 'Button', 'Enable / Disable', '–', '–', 'Thêm 0 hàng hoá',
         'N theo số dòng đang tích; chưa tích dòng nào thì không bấm được.'],
        ['Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; các hàng đã thêm vẫn giữ trên bảng.'],
    ])

    # ---------------- 2.8 Chọn khách hàng (ChooseErpCustomerModal)
    s = section(doc, r'^2\.8 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ',
            '3. Người dùng nhập Tên / Mã khách hàng, Mã số thuế hoặc Số điện thoại rồi bấm Tìm kiếm.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Đóng',
            '• Bấm Đóng / (x) → cửa sổ đóng ngay, không hỏi xác nhận; ô Khách hàng giữ nguyên giá trị cũ.')
    ui = sec_ui(s)
    row_put(ui, r'^Bảng danh sách khách hàng$', **{
        'Mô tả': 'Cột: STT, Mã KH - Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP. Bấm vào dòng '
                 'để chọn.'})
    ev_edit(ev := sec_ev(s), r'^Bấm vào một dòng khách hàng$', r'^– Tự đóng cửa sổ',
            '– Tự đóng cửa sổ và hiển thị thông báo “Chọn khách hàng thành công”.')

    # ---------------- 2.9 Xem chi tiết
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện phụ', r'không có tệp đính kèm',
            '• Phiếu không có tệp đính kèm → không hiển thị khối File đính kèm.')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Màn chi tiết không có nút Xóa; xóa phiếu thực hiện ở màn danh sách (FR-10).'])
    ui = sec_ui(s)
    row_put(ui, r'^Tiêu đề màn$', **{'Giá trị ban đầu': 'Chi tiết phiếu yêu cầu chuyển hàng <mã phiếu>',
                                    'Mô tả': 'Góc phải khối Thông tin chung ghi “Người tạo - ngày giờ tạo”.'})
    row_put(ui, r'^Mã yêu cầu$', **{'Loại': 'Textbox'})
    row_put(ui, r'^Ngày lập$', **{'Tên đối tượng': 'Ngày tạo', 'Loại': 'Textbox'})
    row_put(ui, r'^Người lập$', **{'Tên đối tượng': 'Người tạo', 'Loại': 'Textbox'})
    row_put(ui, r'^Người tiếp nhận$', **{'Loại': 'Textbox', 'Mô tả': 'Hiển thị “Họ tên · ngày giờ tiếp nhận”; chưa '
                                                                    'có thì để trống.'})
    row_put(ui, r'^Ghi chú$', **{'Loại': 'Textarea', 'Mô tả': '–'})
    row_put(ui, r'^Khối File đính kèm$', **{'Mô tả': 'Chỉ hiện khi phiếu có tệp; xem trước hoặc tải xuống được, '
                                                    'không có nút xóa ở màn này.'})
    row_put(ui, r'^Bảng hàng hoá$', **{'Mô tả': 'Cột STT, Hàng hóa (tên, Model, Mã hàng), ĐVT, Giá niêm yết, Khách '
                                               'hàng; cuối mỗi hàng có dòng Tổng cộng.'})
    row_put(ui, r'^Khối Ghi chú duyệt$', **{'Loại': 'Textarea', 'Trạng thái': 'Read-only / Ẩn',
                                          'Giá trị ban đầu': 'Ẩn khi phiếu chưa có ghi chú duyệt',
                                          'Mô tả': 'Chỉ đọc; hiện ghi chú của lần Không duyệt gần nhất. Lý do không '
                                                   'duyệt nhập trong hộp xác nhận (FR-11).'})
    clone_row_after(ui, r'^Khối Ghi chú duyệt$', [None, 'Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
                                                  'Nằm cuối màn; bấm tiêu đề để mở, chỉ nạp dữ liệu ở lần mở đầu '
                                                  '(FR-14).'])
    row_put(ui, r'^Nút Quay lại$', **{'Mô tả': 'Về màn danh sách.'})
    ev_put(sec_ev(s), r'^Bấm tên tệp đính kèm$', ['After:', '– Xem trước: mở bản xem trước của tệp; Tải xuống: tải tệp '
                                                  'về máy.'], name='Bấm Xem trước / Tải xuống ở khối File đính kèm')

    # ---------------- 2.10 Xóa
    s = section(doc, r'^2\.10 ')
    ui = sec_ui(s)
    row_put(ui, r'^Nội dung hộp thoại$', **{
        'Giá trị ban đầu': 'Bạn có chắc muốn xóa phiếu yêu cầu chuyển hàng \'<mã phiếu>\'?'})
    add_err_line(sec_ev(s), r'^Bấm Xóa trong hộp xác nhận$', rid)

    # ---------------- 2.11 Không duyệt (lý do nhập NGAY TRONG hộp xác nhận — base-confirm-modal show-input)
    s = section(doc, r'^2\.11 ')
    kv = sec_kv(s)
    kv_put(kv, 'Dòng sự kiện chính', [
        '1. Người dùng mở màn chi tiết của phiếu đang Chờ duyệt.',
        '2. Người dùng bấm nút Không duyệt.',
        '3. Hệ thống mở hộp Xác nhận không duyệt nêu rõ mã phiếu, hệ quả và ô Ghi chú duyệt (bắt buộc).',
        '4. Người dùng nhập Ghi chú duyệt và bấm Không duyệt trong hộp.',
        '5. Hệ thống kiểm tra quyền, chuyển phiếu về trạng thái Đang tạo, lưu ghi chú duyệt, ghi người tiếp nhận và '
        'thời điểm tiếp nhận.',
        '6. Ghi nhận hành động Từ chối kèm ghi chú duyệt trong lịch sử của phiếu và gửi thông báo cho người lập.',
        '7. Hệ thống hiển thị thông báo “Đã từ chối yêu cầu chuyển hàng”, nạp lại màn chi tiết và khối Lịch sử.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Ghi chú duyệt để trống',
            '• Ghi chú duyệt để trống → hộp xác nhận báo đỏ “Vui lòng nhập ghi chú duyệt” ngay dưới ô, không gửi xử '
            'lý.')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Bấm Hủy / (x) → đóng hộp xác nhận, phiếu giữ nguyên.'])
    set_rows(sec_ui(s), [
        ['Nút Không duyệt (màn chi tiết)', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện',
         'Mở hộp Xác nhận không duyệt.'],
        ['Nội dung hộp xác nhận', 'Label', 'Hiển thị', '–', '–',
         'Bạn có chắc muốn KHÔNG DUYỆT phiếu \'<mã phiếu>\'? Phiếu sẽ chuyển về trạng thái Đang tạo để người lập '
         'sửa lại.', 'Nêu rõ mã phiếu và hệ quả.'],
        ['Ô Ghi chú duyệt', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống',
         'Có dấu * đỏ; gợi ý “Nhập lý do không duyệt”.'],
        ['Lỗi dưới ô Ghi chú duyệt', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
         '“Vui lòng nhập ghi chú duyệt”, ô viền đỏ; hiện khi bấm Không duyệt lúc ô còn trống.'],
        ['Nút Không duyệt (trong hộp)', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thực hiện không duyệt.'],
        ['Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng hộp, phiếu giữ nguyên.'],
    ])
    ev = sec_ev(s)
    ev_put(ev, r'^Bấm nút Không duyệt$', [
        'Before:', '– Nút chỉ hiển thị khi phiếu ở trạng thái Chờ duyệt, người dùng có quyền Kế toán kho hoặc là quản '
                   'trị hệ thống, và cùng công ty với phiếu.',
        'After:', '– Mở hộp Xác nhận không duyệt kèm ô Ghi chú duyệt.'])
    ev_put(ev, r'^Xác nhận Không duyệt$', [
        'Before:', '– Ghi chú duyệt trống → báo đỏ “Vui lòng nhập ghi chú duyệt” dưới ô, không gửi xử lý.',
        '– Chống bấm nhiều lần: bỏ qua nếu đang có một lần xử lý chưa xong.',
        'During:', '– Kiểm tra lại ở phía máy chủ: phiếu Chờ duyệt, người dùng có quyền và cùng công ty; không thoả → '
                   '“Bạn không có quyền thực hiện thao tác này” và nạp lại phiếu.',
        'After:', '– Chuyển phiếu về trạng thái Đang tạo, lưu ghi chú duyệt, ghi người tiếp nhận và thời điểm tiếp nhận.',
        '– Ghi một dòng lịch sử Từ chối (nhóm Thay đổi trạng thái) kèm ghi chú duyệt.',
        '– Gửi thông báo cho người lập phiếu; lỗi gửi thông báo không làm hỏng thao tác.',
        '– Hiển thị thông báo “Đã từ chối yêu cầu chuyển hàng”, nạp lại màn chi tiết và khối Lịch sử.'],
        name='Bấm Không duyệt trong hộp xác nhận')
    add_err_line(ev, r'^Bấm Không duyệt trong hộp xác nhận$', rid)

    # ---------------- 2.12 Tổng hợp (FE: $router.push product-export-requests/create?product_transfer_request_id=)
    s = section(doc, r'^2\.12 ')
    n = replace_in_texts(s[0], 'phiếu đề nghị xuất hàng', 'Yêu cầu xuất hàng')
    log('Đổi tiêu đề 2.12 (%d chỗ)' % n)
    kv = sec_kv(s)
    kv_put(kv, 'Tên chức năng', 'Tổng hợp phiếu sang màn Tạo yêu cầu xuất hàng')
    kv_put(kv, 'Mô tả', 'Chuyển sang màn Tạo yêu cầu xuất hàng của hệ thống HRM (loại Xuất điều chuyển kho chi nhánh) '
                        'ngay trên tab hiện tại, nạp sẵn phiếu đang xem, để bộ phận kho lập yêu cầu xuất hàng.')
    kv_put(kv, 'Dòng sự kiện chính', [
        '1. Người dùng bấm nút Tổng hợp trên màn chi tiết, hoặc nút Tổng hợp trên dòng của màn danh sách.',
        '2. Hệ thống chuyển sang màn Tạo yêu cầu xuất hàng, chọn sẵn loại Xuất điều chuyển kho chi nhánh, nạp sẵn '
        'phiếu yêu cầu chuyển hàng và danh sách hàng hoá của phiếu.',
        '3. Người dùng hoàn tất thao tác ở màn Tạo yêu cầu xuất hàng.'])
    kv_put(kv, 'Dòng sự kiện phụ', ['• Không đủ điều kiện → nút Tổng hợp không hiển thị.'])
    kv_put(kv, 'Yêu cầu đặc biệt', 'Thao tác này KHÔNG làm đổi trạng thái phiếu và không ghi lịch sử. Trạng thái chỉ '
                                   'đổi khi bộ phận kho hoàn tất nghiệp vụ ở các màn xuất – nhập kho.')
    ui = sec_ui(s)
    row_put(ui, r'^Nút Tổng hợp trên màn chi tiết$', **{'Mô tả': 'Nằm ở thanh nút cuối màn, sau nút In.'})
    ev_put(sec_ev(s), r'^Bấm nút Tổng hợp$', [
        'Before:', '– Nút chỉ hiển thị khi phiếu ở trạng thái Chờ duyệt, người dùng có quyền Kế toán kho hoặc là quản '
                   'trị hệ thống, và cùng công ty với phiếu.',
        'After:', '– Chuyển sang màn Tạo yêu cầu xuất hàng ngay trên tab hiện tại (không mở tab mới), chọn sẵn loại '
                  'Xuất điều chuyển kho chi nhánh và nạp sẵn phiếu đang xem.',
        '– Phiếu không đổi trạng thái và không phát sinh lịch sử.'])

    # ---------------- 2.13 In (popup Xem trước — reportPrintPreviewMixin)
    s = section(doc, r'^2\.13 ')
    kv = sec_kv(s)
    kv_put(kv, 'Mô tả', 'Mở cửa sổ Xem trước bản in của phiếu ngay trên màn đang đứng (không mở tab mới) theo mẫu in '
                        'của hệ thống, kèm ảnh tiêu đề thư của công ty ghi trên phiếu.')
    kv_put(kv, 'Dòng sự kiện chính', [
        '1. Người dùng bấm nút In trên màn chi tiết hoặc trên dòng của màn danh sách.',
        '2. Hệ thống mở cửa sổ Xem trước bản in, kiểm tra quyền xem, lấy mẫu in và điền dữ liệu phiếu vào mẫu.',
        '3. Hệ thống thay khối tiêu đề mặc định của mẫu bằng ảnh tiêu đề thư của công ty ghi trên phiếu.',
        '4. Người dùng bấm In cạnh tiêu đề cửa sổ để mở hộp thoại in của trình duyệt; bấm (x) để đóng cửa sổ.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Không tìm thấy mẫu in',
            '• Không tìm thấy mẫu in → cửa sổ Xem trước hiện thông báo lỗi, không có bản in.')
    ui = sec_ui(s)
    row_put(ui, r'^Ảnh tiêu đề thư$', **{'Loại': 'Label'})
    row_put(ui, r'^Ngày yêu cầu / Người yêu cầu$', **{'Mô tả': 'Lấy từ Ngày tạo và Người tạo của phiếu.'})
    row_put(ui, r'^Nút In$', **{'Mô tả': 'Nằm cạnh tiêu đề cửa sổ Xem trước; chỉ bấm được khi bản xem trước đã nạp '
                                         'xong; mở hộp thoại in của trình duyệt.'})
    clone_row_after(ui, r'^Nút In$', [None, 'Nút đóng (x)', 'Icon Button', 'Enable', '–', 'Hiển thị',
                                      'Đóng cửa sổ Xem trước, giữ nguyên màn đang đứng.'])
    ev = sec_ev(s)
    ev_put(ev, r'^Bấm nút In$', ['After:', '– Mở cửa sổ Xem trước bản in ngay trên màn hiện tại (không mở tab mới).'])
    tr = find_row(ev, 1, r'^Mở trang in$')
    write_cell(cells(tr)[1], ['Nạp bản xem trước'])
    ev_edit(ev, r'^Nạp bản xem trước$', r'không hiển thị trang trắng',
            '– Không tìm thấy mẫu in → cửa sổ hiện thông báo lỗi, không có bản in.')

    # ---------------- 2.14 Lịch sử
    s = section(doc, r'^2\.14 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. ',
            '1. Người dùng bấm nút Lịch sử trên dòng phiếu (với phiếu Đang tạo thì nút nằm trong menu ba chấm), hoặc '
            'mở khối Lịch sử ở cuối màn chi tiết phiếu.')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện “Chưa có lịch sử thao tác nào.”'])
    ui = sec_ui(s)
    row_put(ui, r'^Tiêu đề cửa sổ$', **{'Giá trị ban đầu': 'Lịch sử thay đổi: <mã phiếu>'})
    delete_row(ui, r'^Phụ đề$')


def patch_part4(doc):
    h = part_heading(doc, 4)
    intro = h.getnext()
    set_rule_head(intro, 'Quy tắc áp dụng: Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
    set_rule_tail(intro, '. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc đã có trong SRS '
                         'quy tắc chung.' % SCREEN)
    tbl = intro.getnext()
    while tbl.tag != W('tbl'):
        tbl = tbl.getnext()

    def desc(code, old_regex, new):
        tc = cells(find_row(tbl, 1, '^%s$' % code))[3]
        write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))

    def name(code, new):
        write_cell(cells(find_row(tbl, 1, '^%s$' % code))[2], [new])

    desc('BR-08', r'^– Khi tạo mới: bắt buộc',
         '– Khi tạo mới: bắt buộc ít nhất một tệp PDF, mỗi tệp tối đa 20 MB; tệp tải lên ngay lúc chọn để xem trước.')
    desc('BR-09', r'dấu gạch ngang',
         '– Chưa chọn kho ở ô Xem tồn theo kho, hoặc chưa có dữ liệu tồn, thì ô SL tồn để trống và không truy vấn tồn.')
    desc('BR-05', r'^– Ghi chú duyệt là bắt buộc',
         '– Ghi chú duyệt nhập trong hộp xác nhận Không duyệt và là bắt buộc; để trống thì báo “Vui lòng nhập ghi chú '
         'duyệt”.')
    desc('BR-05', r'^– Không duyệt đưa phiếu',
         ['– Không duyệt đưa phiếu về trạng thái Đang tạo, KHÔNG phải hủy phiếu.',
          '– Tổng hợp chuyển sang màn Tạo yêu cầu xuất hàng của HRM (loại Xuất điều chuyển kho chi nhánh) trên tab '
          'hiện tại, nạp sẵn phiếu; không đổi trạng thái phiếu.'])
    desc('BR-12', r'Bộ lọc và trạng thái đóng/mở', None)
    desc('BR-12', r'^– Mốc “Ngày tạo đến”',
         '– Ô Ngày tạo là một ô chọn khoảng ngày; ngày cuối khoảng được lấy trọn ngày.')
    desc('BR-13', r'^– Thứ tự cột trong tệp',
         '– Cửa sổ Chọn trường xuất file tích sẵn đúng các cột đang hiển thị trên bảng; thứ tự cột trong tệp chạy theo '
         'thứ tự người dùng sắp ở cửa sổ.')
    name('BR-16', 'Nội dung lịch sử riêng của phiếu')
    desc('BR-16', r'^– Xem lịch sử không cần quyền riêng', None)
    # Quy tắc "thao tác xong" — ghi ĐÚNG code hiện tại
    last = rows(tbl)[-1]
    new = strip_ids(copy.deepcopy(last))
    last.addnext(new)
    for tc, v in zip(cells(new)[1:], [
            'BR-17', 'Sau mỗi thao tác đưa người dùng về đâu',
            ['– Lưu nháp / Lưu và gửi duyệt (tạo mới, sửa) xong quay về màn danh sách; Lưu và tiếp tục ở lại màn Tạo '
             'mới với form trống.',
             '– Xóa thực hiện ngay trên màn danh sách và nạp lại danh sách.',
             '– Không duyệt xong ở lại màn chi tiết, nạp lại phiếu và khối Lịch sử.'],
            'Tạo mới phiếu / Sửa phiếu / Xóa phiếu / Không duyệt phiếu']):
        write_cell(tc, v if isinstance(v, list) else [v])
    renumber_stt(tbl)
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5: Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    intro = docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc hoặc cập nhật dữ liệu do %s ghi ra '
                                    '(phiếu, dòng hàng hoá và dòng khách hàng của phiếu).' % SCREEN)
    strip_ids(intro)
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1500, 3600, 2900])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()
