# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu chuyển hàng nhập thẳng" (bản Drive 07/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Phiếu chuyển hàng nhập thẳng.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Chạy lại bao nhiêu lần cũng được: luôn đọc bản Drive gốc, không đọc file out.
Màn khác: chép file này, sửa khối DỮ LIỆU MÀN (SCREEN, MENU, ACTOR_*, các dict theo mục) — phần hàm nằm ở
../../phieu-theo-form-quoc-gia/formqg_lib.py.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
import docx  # noqa: E402
from formqg_lib import *  # noqa: E402,F401
import formqg_lib as L  # noqa: E402
import docxlib  # noqa: E402

SRC = os.path.join(HERE, '..', 'drive_0710', 'SRS_Drive.docx')
OUT_DIR = os.path.join(HERE, 'out')
OUT = os.path.join(OUT_DIR, 'SRS - Phiếu chuyển hàng nhập thẳng.docx')
UML = os.path.join(HERE, 'uml')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Phiếu chuyển hàng nhập thẳng'
OLD_MENU = 'Phân hệ Tài chính => Điều chuyển => '
# finance.js: hubGroup 'Hàng hoá - Dịch vụ - Vận chuyển' > nhóm 'Điều chuyển' > mục màn
MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Điều chuyển => Phiếu chuyển hàng nhập thẳng'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Ở lại).')

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Kế toán kho (Q1) và quyền Xem phiếu chuyển hàng nhập '
              'thẳng theo tổng công ty / công ty / phòng ban / bộ phận (V1–V4); không có quyền nào thì chỉ thấy '
              'phiếu của mình.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (Q1, V1–V4); không có quyền nào vẫn xem được phiếu do chính mình lập.')
ACTOR_OWNER = ('Người lập phiếu — người dùng có quyền thực hiện chức năng: chỉ người đã lập phiếu '
               '(chức năng không gắn quyền riêng).')
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Đang tạo hoặc Không duyệt.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu; người có quyền Kế toán kho (Q1) cùng công ty; '
               'hoặc người có quyền Xem phiếu chuyển hàng nhập thẳng theo tổng công ty / công ty / phòng ban / '
               'bộ phận (V1–V4) trong phạm vi được giao.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Đang tạo chỉ người lập xem được.')
ACTOR_KTK = 'Người dùng có quyền Kế toán kho (Q1), cùng công ty với phiếu.'
COND_KTK = ('1. Đăng nhập thành công.\n'
            '2. Có quyền Kế toán kho (Q1) và cùng công ty với phiếu.\n'
            '3. Phiếu đang ở trạng thái Chờ duyệt.')

# Mục 2.x: regex tiêu đề -> vế sau link "Quy tắc chung", Tác nhân, Điều kiện ban đầu
SECTIONS = {
    r'^2\.1 Xem danh sách': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 Tìm kiếm': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST,
                        COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.3 Cài đặt bộ lọc': ('Bộ lọc, Cấu hình cột và lưu cấu hình theo người dùng.', ACTOR_LIST,
                              COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.4 Lập phiếu': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
                         'Người lập phiếu — người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình '
                         '(chức năng lập phiếu không gắn quyền riêng).',
                         '1. Đăng nhập thành công.\n'
                         '2. Vào được màn Phiếu chuyển hàng nhập thẳng (lập phiếu không gắn quyền riêng).\n'
                         '3. Muốn gửi duyệt thì người lập phải còn tồn hàng nhập thẳng.'),
    r'^2\.5 Chọn hàng': ('Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.',
                         'Người lập phiếu — người dùng đang lập hoặc sửa phiếu của chính mình (chức năng không gắn '
                         'quyền riêng).',
                         '1. Đăng nhập thành công.\n2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
                         '3. Đang ở màn Tạo mới hoặc Chỉnh sửa phiếu.'),
    r'^2\.6 Sửa phiếu': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
                         ACTOR_OWNER, COND_OWNER),
    r'^2\.7 Xem chi tiết': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.8 Duyệt': ('Thông báo, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.', ACTOR_KTK, COND_KTK),
    r'^2\.9 Từ chối': ('Thông báo, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.', ACTOR_KTK, COND_KTK),
    r'^2\.10 Xóa': ('Quy tắc xóa và Thông báo.', ACTOR_OWNER, COND_OWNER),
    r'^2\.11 In': ('Quy tắc màn In và bố cục bản in.', ACTOR_SCOPE,
                   '1. Đăng nhập thành công.\n2. Có quyền xem phiếu như mục Tác nhân.\n'
                   '3. In phiếu: phiếu nằm trong phạm vi dữ liệu của người dùng; In danh sách: đang ở màn danh sách.'),
    r'^2\.12 Xuất Excel': ('Quy tắc Excel và Cấu hình cột.', ACTOR_LIST,
                           COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.13 Xem lịch sử': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

# Dòng "Menu:" (đã đổi OLD_MENU -> MENU) + câu popup đặt ngay sau dòng Menu
MENU_LINES = {
    r'^2\.3 ': ('Menu: %s => Cài đặt bộ lọc / Tùy chỉnh cột' % MENU,
                'Modal Cài đặt bộ lọc và Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.5 ': ('Menu: %s => Tạo mới / Chỉnh sửa => Thêm hàng hóa' % MENU,
                'Modal Tồn hàng nhập thẳng của nhân viên được mở ngay trên màn hình Tạo mới hoặc Chỉnh sửa phiếu '
                'theo đường dẫn ở trên.'),
    r'^2\.6 ': ('Menu: %s => Chỉnh sửa' % MENU, None),
    r'^2\.8 ': ('Menu: %s => Xem chi tiết => Duyệt' % MENU,
                'Modal Xác nhận duyệt được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
    r'^2\.9 ': ('Menu: %s => Xem chi tiết => Từ chối' % MENU,
                'Modal Từ chối phiếu được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
    r'^2\.10 ': ('Menu: %s => Xóa (trên dòng phiếu) / Xem chi tiết => Xóa' % MENU,
                 'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa trên dòng) hoặc màn hình '
                 'chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.11 ': ('Menu: %s => In (in danh sách, hoặc In trong menu ba chấm của dòng phiếu) / Xem chi tiết => In' % MENU,
                 'Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo '
                 'đường dẫn ở trên.'),
    r'^2\.12 ': ('Menu: %s => Xuất Excel' % MENU,
                 'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    r'^2\.13 ': ('Menu: %s => Lịch sử (menu ba chấm của dòng phiếu) / Xem chi tiết => Xem lịch sử' % MENU,
                 'Modal Lịch sử phiếu chuyển hàng nhập thẳng được mở ngay trên màn hình danh sách theo đường dẫn ở '
                 'trên; khối Lịch sử thay đổi nằm cuối màn hình chi tiết phiếu.'),
}

# Use Case từng chức năng thao tác: regex mục -> (actor, mã, tên, nhóm màu)
USECASES = {
    r'^2\.4 ': ('Người lập phiếu', 'FR-04', 'Lập phiếu chuyển hàng nhập thẳng', 'crud'),
    r'^2\.5 ': ('Người lập phiếu', 'FR-05', 'Chọn hàng hóa từ tồn nhập thẳng', 'crud'),
    r'^2\.6 ': ('Người lập phiếu', 'FR-06', 'Sửa phiếu', 'crud'),
    r'^2\.7 ': ('Người dùng có quyền', 'FR-07', 'Xem chi tiết phiếu', 'view'),
    r'^2\.8 ': ('Kế toán kho', 'FR-08', 'Duyệt phiếu', 'action'),
    r'^2\.9 ': ('Kế toán kho', 'FR-09', 'Từ chối phiếu', 'action'),
    r'^2\.10 ': ('Người lập phiếu', 'FR-10', 'Xóa phiếu', 'action'),
    r'^2\.11 ': ('Người dùng có quyền', 'FR-11', 'In phiếu và in danh sách', 'io'),
    r'^2\.12 ': ('Người dùng có quyền', 'FR-12', 'Xuất Excel danh sách', 'io'),
}
REDRAW_ALL_UC = True  # vẽ lại cả sơ đồ cũ (còn include/extend) theo kiểu mẫu: actor + 1 use case

PART5 = [  # STT | Nhóm (phân hệ) | Màn hình | Đường dẫn (menu cha)
    ('1', 'Tài chính', 'Yêu cầu xuất giữ (chặn lập yêu cầu khi người lập còn hàng nhập thẳng quá hạn — '
     'tồn hàng nhập thẳng do phiếu ghi sang người nhận khi duyệt)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('2', 'Danh mục', 'Hàng hoá, vật tư (xóa hàng hóa: chặn khi hàng đã có trên phiếu chuyển hàng nhập thẳng '
     'hoặc trong tồn hàng nhập thẳng)', 'Danh mục -> Hàng hoá'),
]


# ============================================================== XỬ LÝ
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)
    body = doc.element.body

    # 1. Đường dẫn menu đủ cấp ở mọi chỗ (Layout + Dòng sự kiện chính FR-01)
    n = replace_in_texts(body, OLD_MENU, MENU.rsplit('=> ', 1)[0] + '=> ')
    log('Đổi đường dẫn menu: %d chỗ' % n)

    # 2. Từng mục 2.x: dòng Quy tắc chung, Tác nhân, Điều kiện ban đầu
    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    # 3. Dòng Menu + câu popup
    for rx, (menu, popup) in MENU_LINES.items():
        sec = section(doc, rx)
        p = sec_par(sec, r'^Menu:')
        set_runs_text(p, menu)
        nxt = p.getnext()
        is_old_popup = nxt is not None and nxt.tag == W('p') and re.search(r'được mở|mở từ menu', txt(nxt))
        if popup and is_old_popup:
            set_runs_text(nxt, popup)
        elif popup:
            strip_ids(docxlib.clone_par_after(p, p, popup))

    patch_sections(doc, rid)
    patch_part4(doc)
    sync_code_1028(doc, rid)
    add_part5(doc)

    # 4. Use Case: bỏ ở FR-03, thêm FR-07, vẽ lại các sơ đồ còn lại
    remove_usecase(doc, section(doc, r'^2\.3 '))
    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.8 '), png, 'Biểu đồ Use Case — %s %s' % (code, name))
        elif REDRAW_ALL_UC:
            set_image(doc, blk[1], png)
    renumber_subheadings(doc)
    nfig = renumber_figures(doc)
    log('Số Hình sau khi đánh lại: %d' % nfig)

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        word_finalize(OUT, os.path.join(OUT_DIR, 'SRS - Phiếu chuyển hàng nhập thẳng.pdf'))


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


def ev_edit(ev, event_regex, old_regex, new):
    tc = cells(find_row(ev, 1, event_regex))[3]
    write_cell(tc, lines_replace(cell_lines(tc), old_regex, new))


def patch_sections(doc, rid):
    # 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    ui = sec_ui(s)
    set_col(ui, header_index(ui, 'Loại'), r'^Cột Trạng thái$', 'Table/Grid')
    delete_row(ui, r'^Vòng quay chờ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^1\. Người dùng vào menu',
            '1. Người dùng vào menu %s.' % MENU)

    # 2.2 Tìm kiếm: gộp Enter vào sự kiện Tìm kiếm (không dùng loại Keypress)
    s = section(doc, r'^2\.2 ')
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Bấm nút Tìm kiếm$'))[1], ['Bấm nút Tìm kiếm hoặc nhấn Enter trong ô tìm nhanh'])
    delete_row(ev, r'^Nhấn Enter')

    # 2.3 Cài đặt bộ lọc / Tùy chỉnh cột
    s = section(doc, r'^2\.3 ')
    ui = sec_ui(s)
    set_col(ui, header_index(ui, 'Loại'), r'^Ô tích của cột bắt buộc', 'Checkbox')
    set_col(sec_ev(s), 2, r'^Kéo thả', 'Drag')

    # 2.4 Lập phiếu
    s = section(doc, r'^2\.4 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ', [
        '6. Hệ thống kiểm tra dữ liệu, sinh số phiếu và lưu phiếu (Lưu nháp: trạng thái Đang tạo; Lưu và gửi '
        'duyệt: trạng thái Chờ duyệt).',
        '7. Ghi nhận hành động Tạo mới (kèm Gửi duyệt nếu bấm Lưu và gửi duyệt) trong lịch sử của phiếu.',
        '8. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn khi còn thay đổi', UNSAVED)
    ui = sec_ui(s)
    set_col(ui, header_index(ui, 'Loại'), r'^Ghi chú$', 'Textbox')
    ev = sec_ev(s)
    set_col(ev, 2, r'^Nhập Số lượng', 'Change')
    add_err_line(ev, r'^Bấm Lưu nháp', rid)
    add_err_line(ev, r'^Bấm Lưu và gửi duyệt', rid)
    unsaved_ev = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
                  '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; '
                  'bấm Thoát thì rời màn và bỏ thay đổi, bấm Ở lại thì giữ nguyên màn.']
    tr = find_row(ev, 1, r'^Bấm Quay lại')
    write_cell(cells(tr)[1], ['Bấm Quay lại / chọn menu khác / đóng tab trình duyệt'])
    write_cell(cells(tr)[3], unsaved_ev)

    # 2.5 Chọn hàng
    s = section(doc, r'^2\.5 ')
    ui = sec_ui(s)
    set_col(ui, header_index(ui, 'Loại'), r'^Ô tích chọn dòng', 'Checkbox')
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'^• Đóng cửa sổ mà không bấm Chọn',
            '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận; lựa chọn đang tích '
            'bị bỏ, phiếu giữ nguyên.')

    # 2.6 Sửa phiếu
    s = section(doc, r'^2\.6 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống kiểm tra dữ liệu và lưu phiếu.',
        '6. Ghi nhận các thay đổi (theo từng trường và từng dòng hàng, kèm Gửi duyệt nếu bấm Lưu và gửi duyệt) '
        'trong lịch sử của phiếu.',
        '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [UNSAVED])
    ui = sec_ui(s)
    set_col(ui, header_index(ui, 'Loại'), r'^Ghi chú$', 'Textbox')
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', unsaved_ev])

    # 2.7 Xem chi tiết
    s = section(doc, r'^2\.7 ')
    ui = sec_ui(s)
    set_col(ui, header_index(ui, 'Loại'), r'^Ghi chú$', 'Textbox')
    ev = sec_ev(s)
    ev_edit(ev, r'^Mở màn chi tiết', r'các cờ cho biết',
            '– Nạp thông tin phiếu, bảng hàng hóa và xác định người dùng được sửa, xóa hay duyệt phiếu.')
    ev_edit(ev, r'^Mở màn chi tiết', r'theo cờ đã nhận',
            '– Hiển thị dữ liệu ở chế độ chỉ đọc và các nút đúng theo quyền và trạng thái phiếu.')

    # 2.8 Duyệt
    s = section(doc, r'^2\.8 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^6\. ', [
        '6. Ghi nhận hành động Duyệt trong lịch sử của phiếu và gửi thông báo cho người lập.',
        '7. Hệ thống báo duyệt thành công và quay về màn danh sách.'])
    add_err_line(sec_ev(s), r'^Bấm Xác nhận', rid)

    # 2.9 Từ chối
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống chuyển phiếu sang Không duyệt và lưu lý do.',
        '6. Ghi nhận hành động Từ chối kèm lý do trong lịch sử của phiếu và gửi thông báo cho người lập.',
        '7. Hệ thống báo thành công và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Đóng',
            '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận kể cả khi đã nhập '
            'lý do; phiếu giữ nguyên.')
    add_err_line(sec_ev(s), r'^Bấm Từ chối trong cửa sổ', rid)

    # 2.10 Xóa
    s = section(doc, r'^2\.10 ')
    add_err_line(sec_ev(s), r'^Bấm Xóa trong hộp thoại', rid)

    # 2.12 Xuất Excel
    s = section(doc, r'^2\.12 ')
    ui = sec_ui(s)
    set_col(ui, header_index(ui, 'Loại'), r'^Danh sách trường', 'Checkbox chọn nhiều')
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'^• Danh sách rỗng',
            '• Kết quả lọc rỗng → vẫn xuất tệp gồm tiêu đề và dòng tên cột, không có dòng dữ liệu.')
    ev_edit(sec_ev(s), r'^Bấm Xuất file', r'với đúng những cột đã chọn',
            '– Lấy dữ liệu theo bộ lọc đang áp dụng và dựng tệp Excel với đúng những cột đã chọn, theo đúng thứ '
            'tự đã tích.')

    # 2.13 Lịch sử
    s = section(doc, r'^2\.13 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Mô tả', r'.', 'Hiển thị các mốc thao tác đã diễn ra trên phiếu: tạo mới, sửa, gửi duyệt, duyệt '
            'và từ chối, kèm người thực hiện và thời điểm.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa có mốc nào',
            '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện dòng “Chưa có lịch sử '
            'thao tác nào.”')
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Trạng thái rỗng'))[-1],
               ['Hiện “Chưa có lịch sử thao tác nào.” với phiếu lập từ hệ thống cũ, chưa có thao tác nào trên '
                'hệ thống mới.'])


MENU_SALE = 'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => Chuyển hàng nhập thẳng'  # sale-hub.js (lối vào thứ 2)


def sync_code_1028(doc, rid):
    """Đợt rà 28/10/2026: sửa cho khớp CODE HIỆN TẠI (hrm-client/hrm-api nhánh develop)."""
    # (9) Lối vào thứ 2: sale-hub.js nhóm 'Yêu cầu' > 'Hàng hóa' > 'Chuyển hàng nhập thẳng' (cùng route)
    s = section(doc, r'^2\.1 ')
    p = sec_par(s, r'^Menu:')
    strip_ids(docxlib.clone_par_after(p, p, 'Hoặc Menu: %s (cùng màn hình).' % MENU_SALE))
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^1\. Người dùng vào menu',
            '1. Người dùng vào menu %s (hoặc %s).' % (MENU, MENU_SALE))

    # (3) Ô lọc Bộ phận đang tắt (index.vue: V2BaseCompanyDepartmentFilter :disable_part="true")
    # + Ngày tạo là MỘT ô chọn khoảng ngày (type 'date-range'), không phải 2 ô Từ/Đến
    s = section(doc, r'^2\.2 ')
    ui = sec_ui(s)
    delete_row(ui, r'^Bộ phận$')
    tr = find_row(ui, 1, r'^Ngày tạo từ$')
    write_cell(cells(tr)[1], ['Ngày tạo'])
    write_cell(cells(tr)[4], ['dd/mm/yyyy – dd/mm/yyyy'])
    write_cell(cells(tr)[-1], ['Một ô chọn khoảng ngày (từ ngày – đến ngày); lọc phiếu lập trong khoảng, lấy trọn '
                               'ngày cuối.'])
    delete_row(ui, r'^Ngày tạo đến$')
    write_cell(cells(find_row(ui, 1, r'^Phòng ban$'))[-1],
               ['Chỉ liệt kê phòng ban của công ty đang chọn. Màn không có ô lọc Bộ phận.'])
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Đổi Công ty', '• Đổi Công ty → hệ thống xóa giá trị đang chọn ở Phòng ban.')
    ev_edit(sec_ev(s), r'^Đổi Công ty$', r'Xóa giá trị Phòng ban',
            '– Xóa giá trị Phòng ban đang chọn, nạp lại danh mục phòng ban theo công ty mới.')

    # (1) Tạo mới có nút "Lưu và tiếp tục" (footerMenu.submit_and_continue = !isEdit; lưu nhánh nháp)
    s = section(doc, r'^2\.4 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ',
            '5. Người dùng bấm Lưu nháp, Lưu và tiếp tục hoặc Lưu và gửi duyệt.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^8\. ',
            '8. Hệ thống hiển thị thông báo thành công và quay về màn danh sách (Lưu và tiếp tục: ở lại màn Tạo mới '
            'với form trống để lập tiếp phiếu khác).')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), lines_replace(
        kv_get(kv, 'Dòng sự kiện phụ'), r'^• Bấm Lưu nháp →',
        [l for l in kv_get(kv, 'Dòng sự kiện phụ') if l.startswith('• Bấm Lưu nháp →')] +
        ['• Bấm Lưu và tiếp tục → lưu như Lưu nháp (trạng thái Đang tạo), rồi mở lại form Tạo mới trống để lập '
         'tiếp phiếu khác.']))
    ui = sec_ui(s)
    clone_row_after(ui, r'^Nút Lưu nháp$',
                    [None, 'Nút Lưu và tiếp tục', None, None, None, None, None,
                     'Chỉ có ở màn Tạo mới. Lưu phiếu ở trạng thái Đang tạo rồi mở lại form trống để lập tiếp.'])
    ev = sec_ev(s)
    clone_row_after(ev, r'^Bấm Lưu nháp$', [None, 'Bấm Lưu và tiếp tục', 'Click', [
        'Before:', '– Áp cùng bộ kiểm tra của nút Lưu nháp.',
        'After:', '– Lưu phiếu ở trạng thái Đang tạo, ghi một dòng lịch sử tạo mới.',
        '– Hiển thị thông báo lưu thành công, ở lại màn Tạo mới với form trống (không về màn danh sách).']])
    add_err_line(ev, r'^Bấm Lưu và tiếp tục$', rid)

    # (6) Popup chọn hàng có ô "Tìm hàng hóa" + nút Tìm kiếm + Làm mới (StockSearchModal.vue);
    # hàng đã có trong phiếu VẪN hiện nhưng ô tích bị khóa
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ',
            '3. Người dùng nhập tên hoặc mã hàng vào ô Tìm hàng hóa rồi bấm Tìm kiếm (hoặc nhấn Enter) để thu hẹp '
            'danh sách nếu cần; bấm Làm mới để bỏ từ khóa.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Hàng đã có trong phiếu',
            '• Hàng đã có trong phiếu vẫn hiện trong cửa sổ nhưng ô tích bị khóa (di chuột vào hiện “Hàng hóa đã có '
            'trong phiếu”) để tránh trùng dòng.')
    ui = sec_ui(s)
    tr = find_row(ui, 1, r'^Ô tìm kiếm$')
    write_cell(cells(tr)[1], ['Ô Tìm hàng hóa'])
    write_cell(cells(tr)[-1], ['Gợi ý “Nhập tên hoặc mã hàng hóa”; chỉ lọc khi bấm Tìm kiếm hoặc nhấn Enter.'])
    clone_row_after(ui, r'^Ô Tìm hàng hóa$', [None, 'Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
                                             'Lọc danh sách theo từ khóa đang nhập, quay về trang 1.'])
    clone_row_after(ui, r'^Nút Tìm kiếm$', [None, 'Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
                                           'Xóa từ khóa và các dòng đang tích, nạp lại danh sách từ trang 1.'])
    tr = find_row(ui, 1, r'^Ô tích chọn dòng$')
    write_cell(cells(tr)[3], ['Enable / Disable'])
    write_cell(cells(tr)[-1], ['Tích được nhiều dòng, giữ lựa chọn khi chuyển trang. Hàng đã có trong phiếu bị khóa '
                               'ô tích.'])
    clone_row_after(ui, r'^Cột Tên hàng$', [None, 'Cột Hãng sản xuất', None, None, None, None, None, '–'])
    ev = sec_ev(s)
    ev_edit(ev, r'^Mở cửa sổ chọn hàng$', r'loại các mặt hàng đã có',
            '– Nạp danh sách hàng còn tồn của chủ tồn đó; mặt hàng đã có trong phiếu bị khóa ô tích.')
    tr = find_row(ev, 1, r'^Nhập từ khóa tìm kiếm$')
    write_cell(cells(tr)[1], ['Bấm Tìm kiếm (hoặc nhấn Enter trong ô Tìm hàng hóa)'])
    write_cell(cells(tr)[2], ['Click'])
    write_cell(cells(tr)[3], ['After:', '– Lọc danh sách theo tên hoặc mã hàng và quay về trang 1.'])
    clone_row_after(ev, r'^Bấm Tìm kiếm', [None, 'Bấm Làm mới', 'Click',
                                          ['After:', '– Xóa từ khóa, bỏ các dòng đang tích, nạp lại danh sách từ '
                                                     'trang 1.']])

    # (2) Màn Sửa KHÔNG có Số phiếu / Trạng thái (form chỉ render 2 ô này khi isShow)
    s = section(doc, r'^2\.6 ')
    ui = sec_ui(s)
    delete_row(ui, r'^Số phiếu$')
    delete_row(ui, r'^Trạng thái$')

    # (5) Xóa KHÔNG ghi lịch sử (ProductImportDirectTransferService::destroy chỉ xóa dòng hàng + phiếu)
    s = section(doc, r'^2\.10 ')
    ev_edit(sec_ev(s), r'^Bấm Xóa trong hộp thoại', r'^– Ghi một dòng lịch sử xóa',
            '– Hiển thị thông báo thành công và nạp lại danh sách từ đầu.')
    kv = sec_kv(s)
    write_cell(kv_row(kv, 'Yêu cầu đặc biệt'), kv_get(kv, 'Yêu cầu đặc biệt') + [
        'Thao tác xóa không ghi dòng lịch sử (phiếu bị xóa hẳn cùng các dòng hàng hóa).'])

    # (7) In: mở popup Xem trước bản in ngay trên màn (reportPrintPreviewMixin + ReportPrintPreviewModal)
    s = section(doc, r'^2\.11 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. ',
            '2. Hệ thống mở cửa sổ Xem trước bản in ngay trên màn đang đứng (không mở tab mới), kèm dữ liệu đã điền '
            'vào mẫu.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ',
            '3. Người dùng bấm In cạnh tiêu đề cửa sổ để gửi lệnh in ra máy in hoặc lưu thành tệp PDF; bấm (x) để '
            'đóng cửa sổ.')
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Nút In$'))[-1],
               ['Nằm cạnh tiêu đề cửa sổ Xem trước; mở hộp in của trình duyệt. Chỉ bấm được khi bản xem trước đã '
                'nạp xong.'])
    tr = find_row(ui, 1, r'^Nút Quay lại$')
    write_cell(cells(tr)[1], ['Nút đóng (x)'])
    write_cell(cells(tr)[2], ['Icon Button'])
    write_cell(cells(tr)[-1], ['Đóng cửa sổ Xem trước, giữ nguyên màn đang đứng.'])
    ev = sec_ev(s)
    for rx in (r'^Bấm In trên dòng phiếu', r'^Bấm In trên thanh công cụ'):
        tc = cells(find_row(ev, 1, rx))[3]
        write_cell(tc, [re.sub(r'Mở màn xem trước bản in', 'Mở cửa sổ Xem trước bản in ngay trên màn hiện tại', l)
                        for l in cell_lines(tc)])

    # (4) Popup "Chọn trường xuất Excel" tích sẵn ĐÚNG các cột đang hiện (exportFieldsMixin.visibleExportFields)
    # (8) File Excel dựng ở FE (export-excel.js, ExcelJS): KHÔNG có logo
    s = section(doc, r'^2\.12 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. ',
            '2. Hệ thống mở cửa sổ Chọn trường xuất Excel, tích sẵn đúng các cột đang hiển thị trên bảng danh sách.')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Tệp gồm dòng tiêu đề “DANH SÁCH PHIẾU CHUYỂN HÀNG NHẬP THẲNG”, dòng khoảng ngày (khi có lọc Ngày tạo), '
        'dòng tên cột (STT luôn đứng đầu) và dữ liệu; tệp KHÔNG có logo công ty. Tên tệp: '
        'danh_sach_phieu_chuyen_hang_nhap_thang.xlsx.'])
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Tiêu đề cửa sổ$'))[-2], ['Chọn trường xuất Excel'])
    tr = find_row(ui, 1, r'^Danh sách trường$')
    write_cell(cells(tr)[-2], ['Tích sẵn các cột đang hiển thị trên bảng'])
    write_cell(cells(tr)[-1], ['Gồm số phiếu, ngày tạo, người tạo, người nhận, trạng thái, người duyệt, công ty, phòng '
                               'ban, ghi chú, người cập nhật và ngày cập nhật; kéo biểu tượng ☰ để đổi thứ tự cột '
                               'trong tệp.'])
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm Xuất Excel$', r'toàn bộ trường được tích sẵn',
            '– Mở cửa sổ Chọn trường xuất Excel, tích sẵn đúng các cột đang hiển thị trên bảng.')
    ev_edit(ev, r'^Bấm Xuất file$', r'^– Tải tệp về máy',
            '– Dựng tệp (tiêu đề, dòng khoảng ngày nếu có, dòng tên cột, dữ liệu; không có logo), tải về máy người '
            'dùng và đóng cửa sổ.')
    log('Đồng bộ code 28/10: 9 điểm (Lưu và tiếp tục, màn Sửa, Bộ phận, chọn trường Excel, Xóa không ghi lịch sử, '
        'Tìm kiếm/Làm mới popup, In popup, Excel không logo, lối vào Bán hàng) + ô Ngày tạo khoảng ngày')


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and txt(e).startswith('Phần %d' % n):
            return e
    raise KeyError(n)


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

    # Bỏ phần trùng quy tắc chung (ẩn nút, lịch sử chung, ghi nhớ bộ lọc/cấu hình theo người dùng)
    desc('BR-02', r'^– Nút không dùng được thì ẩn', None)
    desc('BR-10', r'câu báo lỗi máy chủ',
         '– Đây là lỗi nghiệp vụ: câu báo phải nêu rõ hàng thiếu, không dùng câu báo lỗi chung chung.')
    name('BR-14', 'Nội dung lịch sử riêng của phiếu')
    desc('BR-14', r'^– (Các thao tác tạo mới|Lịch sử lưu theo tên|Các mốc được sắp xếp)', None)
    name('BR-16', 'Cột bắt buộc và tiêu chí lọc bị tắt')
    desc('BR-16', r'^– (Bộ lọc đang áp dụng được ghi nhớ|Cấu hình tiêu chí lọc và cấu hình cột lưu riêng)', None)
    # Mã BR liên tục
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    last = doc.element.body[-1]  # sectPr
    anchor = last.getprevious()
    h5 = clone_heading(h4, 'Phần 5: Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    import docxlib
    intro = docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc dữ liệu do %s ghi ra (dòng hàng '
                                    'của phiếu và tồn hàng nhập thẳng ghi cho người nhận khi phiếu được duyệt).' % SCREEN)
    strip_ids(intro)
    tpl = sec_ev(section(doc, r'^2\.1 '))  # bảng 4 cột cùng khuôn chữ của tài liệu
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1500, 3600, 2900])  # tổng 8850 = bảng event
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()
