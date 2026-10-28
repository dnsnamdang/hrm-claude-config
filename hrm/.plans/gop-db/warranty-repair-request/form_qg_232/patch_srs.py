# -*- coding: utf-8 -*-
"""Vá SRS "Yêu cầu kiểm tra sửa chữa – bảo hành" (STT 232, bản Drive 28/10) theo FORM "Danh mục quốc gia".

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/<tên file Drive>.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Chạy lại bao nhiêu lần cũng được: luôn đọc bản Drive gốc. Khuôn: finance-product-import-direct-transfer/form_qg.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
import docx  # noqa: E402
from formqg_lib import *  # noqa: E402,F401
import formqg_lib as L  # noqa: E402
import docxlib  # noqa: E402

SRC = os.path.join(HERE, 'drive_0710', 'SRS_Drive.docx')
OUT_DIR = os.path.join(HERE, 'out')
NAME = 'SRS - Yêu cầu kiểm tra sửa chữa - bảo hành'
OUT = os.path.join(OUT_DIR, NAME + '.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Yêu cầu kiểm tra sửa chữa - bảo hành'
# customer-care.js: phân hệ "CSKH sau bán" (subsystems.js) > nhóm "Kiểm tra bảo hành sửa chữa" > mục màn (?type=all)
MENU = 'Phân hệ CSKH sau bán => Kiểm tra bảo hành sửa chữa => Yêu cầu kiểm tra sửa chữa - bảo hành'
TAIL = ' Chỉ bổ sung quy tắc riêng của màn %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; '
              'bấm Thoát thì rời màn và bỏ thay đổi, bấm Ở lại thì giữ nguyên màn.']
CLOSE_POPUP = ('• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận kể cả khi đã '
               'nhập; phiếu giữ nguyên.')

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem yêu cầu đi kiểm tra sửa chữa - bảo hành theo tổng '
              'công ty / công ty / phòng ban (V1–V3) và quyền Xử lý yêu cầu sửa chữa (Q1); không có quyền nào thì '
              'chỉ thấy phiếu của mình.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (Q1, V1–V3); không có quyền nào vẫn xem được phiếu do chính mình lập.')
ACTOR_OWNER = ('Người lập phiếu — người dùng có quyền thực hiện chức năng: chỉ người đã lập phiếu '
               '(chức năng không gắn quyền riêng).')
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Đang tạo.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu; người có quyền Xem yêu cầu đi kiểm tra sửa chữa - '
               'bảo hành theo tổng công ty / công ty / phòng ban (V1–V3) trong phạm vi được giao; người có quyền Xử lý '
               'yêu cầu sửa chữa (Q1) với phiếu gửi về phòng mình.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Đang tạo chỉ người lập xem được.')
ACTOR_Q1 = ('Phòng tiếp nhận xử lý — người dùng có quyền Xử lý yêu cầu sửa chữa (Q1), thuộc phòng tiếp nhận xử lý '
            'của phiếu.')
COND_Q1 = ('1. Đăng nhập thành công.\n'
           '2. Có quyền Xử lý yêu cầu sửa chữa (Q1) và thuộc phòng tiếp nhận xử lý của phiếu.\n'
           '3. Phiếu đang ở trạng thái Chờ xử lý và chưa có phiếu xử lý yêu cầu.')

SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST,
                COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.3 ': ('Cấu hình bộ lọc và Tùy chỉnh cột.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.4 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
                'Người lập phiếu — người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình '
                '(chức năng lập phiếu không gắn quyền riêng).',
                '1. Đăng nhập thành công.\n'
                '2. Vào được màn Yêu cầu kiểm tra sửa chữa - bảo hành (lập phiếu không gắn quyền riêng).'),
    r'^2\.5 ': ('Màn Chỉnh sửa, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.6 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.7 ': ('Quy tắc thao tác trạng thái, Thông báo và Quy tắc ghi lịch sử.', ACTOR_Q1, COND_Q1),
    r'^2\.8 ': ('Quy tắc thao tác trạng thái, Thông báo và Quy tắc ghi lịch sử.', ACTOR_Q1, COND_Q1),
    r'^2\.9 ': ('Quy tắc điều hướng sang chứng từ tiếp theo và Phân quyền.', ACTOR_Q1, COND_Q1),
    r'^2\.10 ': ('Quy tắc Xóa, Thông báo và Quy định xác nhận.', ACTOR_OWNER, COND_OWNER),
    r'^2\.11 ': ('Quy tắc In và Mẫu in chứng từ.', ACTOR_SCOPE,
                 '1. Đăng nhập thành công.\n2. Có quyền xem phiếu như mục Tác nhân.\n'
                 '3. In phiếu: phiếu nằm trong phạm vi dữ liệu của người dùng; In danh sách: đang ở màn danh sách.'),
    r'^2\.12 ': ('Quy tắc Excel và Cấu hình cột.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.13 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

# Câu popup đặt ngay sau dòng đường dẫn (ghi ĐÚNG màn mở popup — đối chiếu code)
POPUPS = {
    r'^2\.3 ': 'Modal Cài đặt bộ lọc và Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    r'^2\.4 ': 'Modal Chọn khách hàng được mở ngay trên màn hình Tạo mới (bấm vào ô Khách hàng) theo đường dẫn ở trên.',
    r'^2\.7 ': ('Modal Chuyển phòng tiếp nhận được mở ngay trên màn hình danh sách (biểu tượng Chuyển phòng tiếp nhận '
                'ở cột Hành động) hoặc màn hình chi tiết phiếu (nút Chuyển phòng tiếp nhận) theo đường dẫn ở trên.'),
    r'^2\.8 ': ('Modal Từ chối yêu cầu được mở ngay trên màn hình danh sách (Từ chối trong menu Hành động khác của '
                'dòng phiếu) hoặc màn hình chi tiết phiếu (nút Từ chối) theo đường dẫn ở trên.'),
    r'^2\.10 ': ('Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa ở cột Hành động) hoặc màn '
                 'hình chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.11 ': ('Cửa sổ Xem trước phiếu yêu cầu được mở ngay trên màn hình danh sách (In ở cột Hành động hoặc menu '
                 'Hành động khác) hoặc màn hình chi tiết phiếu (nút In); cửa sổ Xem trước danh sách mở trên màn hình '
                 'danh sách (nút In danh sách) theo đường dẫn ở trên.'),
    r'^2\.12 ': 'Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    r'^2\.13 ': ('Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách (Lịch sử ở cột Hành động hoặc menu '
                 'Hành động khác) theo đường dẫn ở trên; khối Lịch sử nằm cuối màn hình chi tiết phiếu.'),
}

# Thay ảnh cũ lệch giao diện hiện tại (số Hình theo bản Drive gốc -> ảnh chụp mới trên dev 28/10)
IMAGES = {2: '01_list', 3: '02_filter', 4: '25_colcfg', 5: '26_filtercfg', 7: '10_create', 8: '11_customer',
          10: '12_edit', 11: '17_detail', 13: '14_transfer', 15: '15_reject', 19: '13_delete', 21: '18_print',
          25: '20_export'}

USECASES = {
    r'^2\.4 ': ('Người lập phiếu', 'FR-04', 'Lập phiếu yêu cầu', 'crud'),
    r'^2\.5 ': ('Người lập phiếu', 'FR-05', 'Sửa phiếu yêu cầu', 'crud'),
    r'^2\.6 ': ('Người dùng có quyền', 'FR-06', 'Xem chi tiết phiếu', 'view'),
    r'^2\.7 ': ('Phòng tiếp nhận xử lý', 'FR-07', 'Chuyển phòng tiếp nhận', 'action'),
    r'^2\.8 ': ('Phòng tiếp nhận xử lý', 'FR-08', 'Từ chối yêu cầu', 'action'),
    r'^2\.9 ': ('Phòng tiếp nhận xử lý', 'FR-09', 'Tạo phiếu xử lý yêu cầu', 'action'),
    r'^2\.10 ': ('Người lập phiếu', 'FR-10', 'Xóa phiếu yêu cầu', 'action'),
    r'^2\.11 ': ('Người dùng có quyền', 'FR-11', 'In phiếu và in danh sách', 'io'),
    r'^2\.12 ': ('Người dùng có quyền', 'FR-12', 'Xuất Excel', 'io'),
}

SALE_ENTRIES = [
    'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => YC kiểm tra sửa chữa - bảo hành  (hiển thị: chỉ phiếu do chính '
    'người đăng nhập lập)',
    'Phân hệ Bán hàng => Yêu cầu => Lắp đặt - BH - SC => YC sửa chữa - bảo hành  (hiển thị: toàn bộ phiếu trong '
    'phạm vi quyền của người đăng nhập)',
]

PART5 = [  # STT | Nhóm (phân hệ) | Màn hình | Đường dẫn (menu cha) — grep code hrm-api 28/10/2026
    ('1', 'CSKH sau bán', 'Phiếu xử lý yêu cầu (lập từ phiếu yêu cầu, chép khách hàng và thiết bị; ghi ngược trạng '
     'thái, Người xử lý, Ngày xử lý; xóa phiếu xử lý trả phiếu yêu cầu về Chờ xử lý)',
     'CSKH sau bán -> Kiểm tra bảo hành sửa chữa'),
    ('2', 'CSKH sau bán', 'Phiếu cung cấp thông tin làm báo giá (hiện và tìm theo số phiếu yêu cầu; ghi ngược trạng '
     'thái Đang CCTT / Đã CCTT báo giá)', 'CSKH sau bán -> Kiểm tra bảo hành sửa chữa'),
    ('3', 'Bán hàng', 'Báo giá dịch vụ SC-BD-BT — Danh sách báo giá (hiện số phiếu yêu cầu, người yêu cầu; ghi ngược '
     'trạng thái Đã báo giá)', 'Bán hàng -> Bán dịch vụ -> Báo giá dịch vụ SC-BD-BT'),
    ('4', 'Bán hàng', 'Hợp đồng dịch vụ — Danh sách hợp đồng (lấy phòng tiếp nhận xử lý ghi trên phiếu yêu cầu gốc '
     'của báo giá)', 'Bán hàng -> Bán dịch vụ -> HĐ Sửa chữa - Bảo dưỡng - Bảo trì'),
]


# ============================================================== XỬ LÝ
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


def kv_add(kv, key, lines):
    write_cell(kv_row(kv, key), kv_get(kv, key) + lines)


def ev_cell(ev, event_regex):
    return cells(find_row(ev, 1, event_regex))[3]


def ev_edit(ev, event_regex, old_regex, new):
    tc = ev_cell(ev, event_regex)
    write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))


def fig_par(doc, n):
    for e in items(doc):
        if e.tag == W('p') and re.match(r'^Hình %d:' % n, txt(e)):
            return e
    raise KeyError(n)


def fix_menu_paragraphs(doc):
    """Đường dẫn: 'Menu:' + tên phân hệ đúng (CSKH sau bán), bỏ khoảng trắng / mũi tên thừa. Giữ icon nội dòng."""
    body = doc.element.body
    for old, new in [('  => => Tạo mới ', ' => Tạo mới '), ('  =>', ' =>'),
                     (' => Bán dịch vụ ', ' => Bán dịch vụ => Báo giá dịch vụ SC-BD-BT '),
                     (' => Xuất excel ', ' => Xuất Excel '),
                     (' => Click vào số phiếu để Xem chi tiết', ' => Bấm vào Số phiếu (Xem chi tiết)'),
                     (' => Lịch sử ', ' => Lịch sử (cột Hành động / menu Hành động khác) '),
                     (' => Chuyển phòng tiếp nhận ', ' => Chuyển phòng tiếp nhận (cột Hành động / màn chi tiết) '),
                     (' => Từ chối ', ' => Từ chối (menu Hành động khác / màn chi tiết) '),
                     (' => Xóa ', ' => Xóa (cột Hành động / màn chi tiết) '),
                     (' => Tạo phiếu xử lý yêu cầu ', ' => Tạo phiếu xử lý yêu cầu (cột Hành động / màn chi tiết) ')]:
        n = replace_in_texts(body, old, new)
        log('Đường dẫn: "%s" → "%s" (%d chỗ)' % (old.strip(), new.strip(), n))
    its = items(doc)
    n = 0
    for i, e in enumerate(its):
        if e.tag != W('p'):
            continue
        ts = [t for t in e.iter(W('t')) if t.text]
        if not ts or not ts[0].text.startswith('Phân hệ CSKH '):
            continue
        ts[0].text = ts[0].text.replace('Phân hệ CSKH ', 'Phân hệ CSKH sau bán ', 1)
        prev = its[i - 1]
        if not txt(prev).strip().startswith('Menu:'):
            ts[0].text = 'Menu: ' + ts[0].text
        n += 1
    log('Đổi "Phân hệ CSKH" → "Phân hệ CSKH sau bán" + nhãn Menu: %d dòng' % n)
    # 2.11: dòng "=> In" tách riêng — gắn nhãn cho rõ
    replace_in_texts(body, '=> In ', '=> In (cột Hành động / menu Hành động khác / màn chi tiết) hoặc In danh sách ')


def add_sale_entries(doc, sec, tpl_par):
    p = sec_par(sec, r'^Phân hệ Bán hàng')
    anchor = p
    for s in SALE_ENTRIES:
        anchor = strip_ids(docxlib.clone_par_after(anchor, tpl_par, s))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)

    fix_menu_paragraphs(doc)
    menu_label = sec_par(section(doc, r'^2\.1 '), r'^Menu:\s*$')
    for rx in (r'^2\.1 ', r'^2\.2 '):
        add_sale_entries(doc, section(doc, rx), menu_label)

    # Quy tắc chung / Tác nhân / Điều kiện ban đầu
    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    # Câu popup
    tpl_popup = sec_par(section(doc, r'^2\.7 '), r'^Modal ')
    for rx, popup in POPUPS.items():
        sec = section(doc, rx)
        try:
            set_runs_text(sec_par(sec, r'^Modal '), popup)
        except KeyError:
            paths = [e for e in sec[1] if e.tag == W('p') and '=>' in txt(e)]
            strip_ids(docxlib.clone_par_after(paths[-1], tpl_popup, popup))

    # Ảnh chụp mới
    for n, name in IMAGES.items():
        cap = fig_par(doc, n)
        img = cap.getprevious()
        set_image(doc, img, os.path.join(SHOTS, name + '.png'))
        log('Thay ảnh Hình %d (%s) bằng %s.png' % (n, txt(cap)[len('Hình %d: ' % n):], name))

    patch_sections(doc, rid)
    patch_part4(doc)
    add_part5(doc)

    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.7 '), png, 'Biểu đồ Use Case — %s %s' % (code, name))
        else:
            set_image(doc, blk[1], png)
            set_runs_text(blk[2], 'Hình 0: Biểu đồ Use Case — %s %s' % (code, name))
    renumber_subheadings(doc)
    log('Số Hình sau khi đánh lại: %d' % renumber_figures(doc))

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        word_finalize(OUT, os.path.join(OUT_DIR, NAME + '.pdf'))


def patch_sections(doc, rid):
    # ---- 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. Người dùng vào màn hình',
            '1. Người dùng vào menu %s (hoặc một trong các lối vào ở mục Layout).' % MENU)
    ui = sec_ui(s)
    li = header_index(ui, 'Loại')
    set_col(ui, li, r'^Cột Trạng thái$', 'Table/Grid')
    set_col(ui, li, r'^Cột Hành động$', 'Table/Grid')
    write_cell(cells(find_row(ui, 1, r'^Cột Hành động$'))[-1],
               ['Phiếu có tối đa 3 thao tác thì hiện đủ biểu tượng; nhiều hơn thì hiện 2 thao tác đầu và menu '
                '“Hành động khác” chứa các thao tác còn lại. Thao tác không đủ điều kiện thì ẩn hẳn.'])

    # ---- 2.2 Tìm kiếm
    s = section(doc, r'^2\.2 ')
    ev = sec_ev(s)
    set_col(ev, 2, r'^Bấm Tìm kiếm hoặc nhấn Enter', 'Click')
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Ngày yêu cầu từ / đến$'))[1], ['Ngày yêu cầu (từ → đến)'])
    write_cell(cells(find_row(ui, 1, r'^Ngày yêu cầu'))[-1],
               ['Một ô gồm 2 lịch chọn ngày nối bằng dấu →. Lọc theo ngày tạo phiếu, tính trọn ngày ở cả hai đầu.'])

    # ---- 2.3 Cài đặt bộ lọc / Tùy chỉnh cột
    s = section(doc, r'^2\.3 ')
    ui = sec_ui(s)
    li = header_index(ui, 'Loại')
    set_col(ui, li, r'^Danh sách cột$', 'Checkbox')
    set_col(ui, li, r'^Danh sách ô lọc$', 'Checkbox')
    write_cell(cells(find_row(ui, 1, r'^Danh sách ô lọc$'))[4], ['Danh sách 7 ô lọc'])
    tr = find_row(ui, 1, r'^Cột bị khóa$')  # dòng lệch cột ở bản Drive
    for tc, v in zip(cells(tr), ['2', 'Cột bị khóa', 'Icon', 'Read-only', '–', '–', 'Hiển thị',
                                 'Biểu tượng ổ khóa ở các cột bắt buộc hiển thị (STT, Số phiếu, Hành động).']):
        write_cell(tc, [v])
    ev = sec_ev(s)
    write_cell(ev_cell(ev, r'^Bấm Chọn tất cả'),
               ['After:', '– Chọn tất cả: tích tất cả các cột.',
                '– Bỏ chọn hết: bỏ tích các cột không bắt buộc; cột bắt buộc giữ nguyên.',
                '– Cập nhật dòng “Đang chọn x/y cột”; bảng chưa đổi cho tới khi bấm Lưu.'])
    clone_row_after(ev, r'^Bấm Khôi phục mặc định',
                    [None, 'Kéo thả biểu tượng ở đầu / cuối dòng', 'Drag',
                     ['After:', '– Đổi thứ tự cột / ô lọc trong cửa sổ; áp dụng khi bấm Lưu.']])

    # ---- 2.4 Lập phiếu
    s = section(doc, r'^2\.4 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ',
            '5. Người dùng bấm Lưu nháp, Lưu và gửi hoặc Lưu và tiếp tục.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ', [
        '6. Hệ thống kiểm tra dữ liệu, sinh số phiếu và lưu phiếu (Lưu nháp / Lưu và tiếp tục: trạng thái Đang tạo; '
        'Lưu và gửi: trạng thái Chờ xử lý, ghi Ngày gửi yêu cầu và gửi thông báo cho phòng tiếp nhận xử lý).',
        '7. Ghi nhận hành động Tạo mới trong lịch sử của phiếu.',
        '8. Hệ thống hiển thị thông báo thành công và quay về màn danh sách (Lưu và tiếp tục: ở lại màn Tạo mới với '
        'các ô để trống để lập phiếu tiếp).'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Thoát màn khi đã nhập', UNSAVED)
    ui = sec_ui(s)
    li = header_index(ui, 'Loại')
    set_col(ui, li, r'^Thông báo lỗi inline$', 'Label')
    clone_row_after(ui, r'^Nút Lưu và gửi$',
                    [None, 'Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị',
                     'Chỉ có ở màn Tạo mới. Lưu nháp như nút Lưu nháp rồi ở lại màn Tạo mới với các ô để trống.'])
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Lưu nháp', rid)
    ev_edit(ev, r'^Bấm Lưu nháp', r'^– Ghi một dòng lịch sử', '– Ghi nhận hành động Tạo mới trong lịch sử của phiếu.')
    add_err_line(ev, r'^Bấm Lưu và gửi', rid)
    ev_edit(ev, r'^Bấm Lưu và gửi', r'^– Ghi một dòng lịch sử; hiển thị',
            ['– Ghi nhận hành động Tạo mới trong lịch sử của phiếu.',
             '– Hiển thị “Gửi yêu cầu thành công” và quay về danh sách.'])
    clone_row_after(ev, r'^Bấm Lưu và gửi',
                    [None, 'Bấm Lưu và tiếp tục', 'Click',
                     ['During:', '– Kiểm tra như Lưu nháp.', 'After:',
                      '– Sinh số phiếu, ghi phiếu ở trạng thái Đang tạo; ghi nhận Tạo mới trong lịch sử.',
                      '– Hiển thị “Lưu thành công”, ở lại màn Tạo mới với các ô để trống.']])
    add_err_line(ev, r'^Bấm Lưu và tiếp tục', rid)
    tr = find_row(ev, 1, r'^Bấm Quay lại')
    write_cell(cells(tr)[1], ['Bấm Quay lại / chọn menu khác / đóng tab trình duyệt'])
    write_cell(cells(tr)[3], UNSAVED_EV)

    # ---- 2.5 Sửa phiếu
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', [
        '4. Hệ thống kiểm tra dữ liệu và lưu phiếu (Lưu và gửi: chuyển trạng thái Chờ xử lý, gửi thông báo cho phòng '
        'tiếp nhận xử lý).',
        '5. Ghi nhận các thay đổi (theo từng trường và từng dòng thiết bị: thêm mới, bị xóa, sửa trường nào) trong '
        'lịch sử của phiếu.',
        '6. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_add(kv, 'Dòng sự kiện phụ', [UNSAVED])
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Lưu nháp / Lưu và gửi', rid)
    ev_edit(ev, r'^Bấm Lưu nháp / Lưu và gửi', r'^– Ghi lại phiếu; ghi một dòng lịch sử',
            ['– Ghi lại phiếu; ghi nhận lịch sử “Thay đổi thông tin” liệt kê đúng những trường đã đổi (kể cả thiết '
             'bị thêm mới, bị xóa, bị sửa).', '– Hiển thị thông báo thành công và quay về danh sách.'])
    clone_row_after(ev, r'^Bấm Lưu nháp / Lưu và gửi',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # ---- 2.6 Xem chi tiết
    s = section(doc, r'^2\.6 ')
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Khối Lịch sử$'))[-1], ['Bấm “Xem lịch sử” để mở; xem mục 2.13.'])
    write_cell(cells(find_row(ui, 1, r'^Nút In$'))[-1], ['Luôn hiển thị. Mở cửa sổ Xem trước phiếu yêu cầu.'])

    # ---- 2.7 Chuyển phòng tiếp nhận
    s = section(doc, r'^2\.7 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', [
        '4. Hệ thống đổi phòng tiếp nhận, làm mới mốc ngày gửi yêu cầu (trạng thái giữ nguyên Chờ xử lý).',
        '5. Ghi nhận thay đổi Phòng tiếp nhận (cũ → mới) trong lịch sử của phiếu và gửi thông báo cho phòng mới.',
        '6. Hệ thống báo thành công và nạp lại màn đang đứng (danh sách hoặc chi tiết phiếu).'])
    kv_add(kv, 'Dòng sự kiện phụ', [CLOSE_POPUP])
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Xác nhận', rid)
    ev_edit(ev, r'^Bấm Xác nhận', r'nạp lại danh sách',
            '– Hiển thị “Chuyển phòng tiếp nhận thành công” và nạp lại màn đang đứng (danh sách hoặc chi tiết).')

    # ---- 2.8 Từ chối
    s = section(doc, r'^2\.8 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', [
        '4. Hệ thống chuyển phiếu về trạng thái Đang tạo và lưu lý do.',
        '5. Ghi nhận hành động Từ chối kèm lý do trong lịch sử của phiếu và gửi thông báo cho người lập phiếu.',
        '6. Hệ thống báo thành công và nạp lại màn đang đứng (danh sách hoặc chi tiết phiếu).'])
    kv_add(kv, 'Dòng sự kiện phụ', [CLOSE_POPUP])
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Từ chối trong cửa sổ', rid)
    ev_edit(ev, r'^Bấm Từ chối trong cửa sổ', r'^– Hiển thị “Từ chối yêu cầu thành công”',
            '– Hiển thị “Từ chối yêu cầu thành công” và nạp lại màn đang đứng (danh sách hoặc chi tiết).')

    # ---- 2.9 Tạo phiếu xử lý: Loại event / đối tượng
    s = section(doc, r'^2\.9 ')
    ui = sec_ui(s)
    li = header_index(ui, 'Loại')
    set_col(ui, li, r'^Nút Tạo phiếu xử lý yêu cầu$', 'Button')

    # ---- 2.10 Xóa
    s = section(doc, r'^2\.10 ')
    add_err_line(sec_ev(s), r'^Bấm Xóa ở hộp xác nhận', rid)
    ev_edit(sec_ev(s), r'^Bấm Xóa ở hộp xác nhận', r'^– Ghi một dòng lịch sử “Xóa”',
            '– Ghi nhận hành động Xóa trong lịch sử.')
    ev_edit(sec_ev(s), r'^Bấm Xóa ở hộp xác nhận', r'^– Hiển thị “Xóa thành công”',
            '– Hiển thị “Xóa thành công”; xóa từ danh sách thì nạp lại danh sách, xóa từ màn chi tiết thì quay về '
            'danh sách.')

    # ---- 2.11 In
    s = section(doc, r'^2\.11 ')
    ui = sec_ui(s)
    li = header_index(ui, 'Loại')
    set_col(ui, li, r'^Nút In \(từng phiếu\)$', 'Button')
    set_col(ui, li, r'^Cửa sổ xem trước$', 'Popup')
    set_col(ui, li, r'^Lời nhắc vượt trần in$', 'Label')

    # ---- 2.12 Xuất Excel
    s = section(doc, r'^2\.12 ')
    ui = sec_ui(s)
    set_col(ui, header_index(ui, 'Loại'), r'^Trường xuất$', 'Checkbox')
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'^• Bỏ chọn hết trường', '• Bỏ chọn hết trường → nút Xuất file không dùng được.')

    # ---- 2.13 Lịch sử
    s = section(doc, r'^2\.13 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Mô tả', r'.', 'Xem ai đã làm gì với phiếu: tạo mới, sửa những trường nào (giá trị cũ → giá trị mới), '
            'đổi phòng tiếp nhận, đổi trạng thái (gửi, từ chối kèm lý do) và xóa.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa có thao tác nào',
            '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện “Chưa có lịch sử thao tác nào.”')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bản ghi tạo từ hệ thống cũ', None)
    ui = sec_ui(s)
    set_col(ui, header_index(ui, 'Loại'), r'^Dòng thời gian$', 'Label')


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and txt(e).startswith('Phần %d' % n):
            return e
    raise KeyError(n)


def patch_part4(doc):
    h = part_heading(doc, 4)
    intro = h.getnext()
    set_rule_head(intro, 'Quy tắc áp dụng: Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
    set_rule_tail(intro, '. Phần này chỉ ghi các quy tắc đặc thù của màn %s; không lặp lại các quy tắc đã có trong SRS '
                         'quy tắc chung.' % SCREEN)
    tbl = intro.getnext()
    while tbl.tag != W('tbl'):
        tbl = tbl.getnext()

    def row(code):
        return cells(find_row(tbl, 1, '^%s$' % code))

    write_cell(row('BR-9')[1], ['BR-09'])
    write_cell(row('BR-05')[2], ['Điều kiện sửa và xóa'])
    write_cell(row('BR-05')[3], ['– Chỉ sửa và xóa được phiếu ở trạng thái Đang tạo và do chính người đăng nhập lập.',
                                 '– Điều kiện được kiểm tra ở máy chủ, không chỉ ẩn nút trên giao diện.'])
    write_cell(row('BR-05')[4], ['- Chỉnh sửa phiếu', '- Xóa phiếu'])
    write_cell(row('BR-10')[4], ['- In phiếu', '- In danh sách'])
    tc = row('BR-08')[3]
    write_cell(tc, lines_replace(cell_lines(tc), r'^– Vào từ Bán hàng',
                                 '– Vào từ Bán hàng (Bán dịch vụ => Báo giá dịch vụ SC-BD-BT, hoặc Yêu cầu => Hàng hóa): '
                                 'chỉ hiển thị phiếu do chính người đăng nhập lập, bất kể người đó có quyền xem theo cấp '
                                 'nào. Vào từ Bán hàng => Yêu cầu => Lắp đặt - BH - SC: như vào từ CSKH.'))
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    intro = strip_ids(docxlib.clone_par_after(
        h5, h4.getnext(), 'Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của phiếu %s.' % SCREEN))
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1500, 3600, 2900])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()
