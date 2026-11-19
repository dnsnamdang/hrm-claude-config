# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu xử lý yêu cầu" (STT 233, bản Drive 28/10) theo FORM "Danh mục quốc gia".

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/<tên file Drive>.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Chạy lại bao nhiêu lần cũng được: luôn đọc bản Drive gốc. Khuôn: finance-product-import-direct-transfer/form_qg.
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
NAME = 'SRS - Phiếu xử lý yêu cầu'
OUT = os.path.join(OUT_DIR, NAME + '.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Phiếu xử lý yêu cầu'
# customer-care.js: phân hệ "CSKH sau bán" > nhóm "Kiểm tra bảo hành sửa chữa" > mục màn (?type=all) — lối vào DUY NHẤT
MENU = 'Phân hệ CSKH sau bán => Kiểm tra bảo hành sửa chữa => Phiếu xử lý yêu cầu'
TAIL = ' Chỉ bổ sung quy tắc riêng của màn %s.' % SCREEN
UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?” '
           '(Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”; '
              'bấm Thoát thì rời màn và bỏ thay đổi, bấm Ở lại thì giữ nguyên màn.']
CLOSE_POPUP = ('• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận kể cả khi đã '
               'nhập; dữ liệu giữ nguyên.')

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem phiếu xử lý yêu cầu đi kiểm tra sửa chữa - bảo hành '
              'theo tổng công ty / công ty / phòng ban (V1–V3); không có quyền nào thì chỉ thấy phiếu của mình.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (V1–V3); không có quyền nào vẫn xem được phiếu do chính mình tạo.')
ACTOR_OWNER = ('Người xử lý — người dùng có quyền thực hiện chức năng: chỉ người đã tạo phiếu '
               '(chức năng không gắn quyền riêng).')
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người tạo phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Đang tạo.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người tạo phiếu; người có quyền Xem phiếu xử lý yêu cầu đi kiểm tra '
               'sửa chữa - bảo hành theo tổng công ty / công ty / phòng ban (V1–V3) trong phạm vi được giao.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Đang tạo chỉ người tạo xem được.')
ACTOR_Q1 = 'Người tạo phiếu cung cấp thông tin — người dùng có quyền Tạo phiếu cung cấp thông tin (Q1).'
COND_Q1 = ('1. Đăng nhập thành công.\n'
           '2. Có quyền Tạo phiếu cung cấp thông tin (Q1) — không ràng buộc phòng ban.\n'
           '3. Phiếu đang ở trạng thái Chờ CCTT.')

SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST,
                COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.3 ': ('Cấu hình bộ lọc và Tùy chỉnh cột.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.4 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
                'Người xử lý — người dùng có quyền Xử lý yêu cầu sửa chữa (Q2), thuộc phòng tiếp nhận xử lý của '
                'phiếu yêu cầu gốc.',
                '1. Đăng nhập thành công.\n'
                '2. Có quyền Xử lý yêu cầu sửa chữa (Q2) và thuộc phòng tiếp nhận xử lý của phiếu yêu cầu gốc.\n'
                '3. Phiếu yêu cầu gốc đang ở trạng thái Chờ xử lý và chưa có phiếu xử lý nào.'),
    r'^2\.5 ': ('Màn Chỉnh sửa, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.6 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.7 ': ('Màn Thêm mới danh mục, Validate dữ liệu và Thông báo.',
                'Người xử lý có quyền Quản lý danh mục công việc - lỗi thiết bị (Q3).',
                '1. Đăng nhập thành công.\n2. Có quyền Quản lý danh mục công việc - lỗi thiết bị (Q3).\n'
                '3. Đang ở màn Tạo phiếu hoặc Sửa phiếu xử lý.'),
    r'^2\.8 ': ('Quy tắc điều hướng sang chứng từ tiếp theo và Phân quyền.', ACTOR_Q1, COND_Q1),
    r'^2\.9 ': ('Quy tắc thao tác trạng thái, Thông báo và Quy tắc ghi lịch sử.', ACTOR_Q1, COND_Q1),
    r'^2\.10 ': ('Quy tắc Xóa, Thông báo và Quy định xác nhận.', ACTOR_OWNER, COND_OWNER),
    r'^2\.11 ': ('Quy tắc In và Mẫu in chứng từ.', ACTOR_SCOPE,
                 '1. Đăng nhập thành công.\n2. Có quyền xem phiếu như mục Tác nhân.\n'
                 '3. In phiếu: phiếu nằm trong phạm vi dữ liệu của người dùng; In danh sách: đang ở màn danh sách.'),
    r'^2\.12 ': ('Quy tắc Excel và Cấu hình cột.', ACTOR_LIST, COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.13 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

POPUPS = {
    r'^2\.3 ': 'Modal Cài đặt bộ lọc và Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    r'^2\.7 ': ('Modal Thêm nhanh công việc / lỗi thiết bị được mở ngay trên màn hình Tạo phiếu hoặc Sửa phiếu xử lý '
                '(nút Thêm nhanh lỗi thiết bị ở cột Nguyên nhân) theo đường dẫn ở trên.'),
    r'^2\.9 ': ('Modal Không duyệt phiếu xử lý yêu cầu được mở ngay trên màn hình danh sách (biểu tượng Không duyệt '
                'ở cột Hành động) hoặc màn hình chi tiết phiếu (nút Không duyệt) theo đường dẫn ở trên.'),
    r'^2\.10 ': ('Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa ở cột Hành động) hoặc màn '
                 'hình chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.11 ': ('Cửa sổ Xem trước phiếu xử lý yêu cầu được mở ngay trên màn hình danh sách (In ở cột Hành động hoặc '
                 'menu Hành động khác) hoặc màn hình chi tiết phiếu (nút In); cửa sổ Xem trước danh sách mở trên màn '
                 'hình danh sách (nút In danh sách) theo đường dẫn ở trên.'),
    r'^2\.12 ': 'Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    r'^2\.13 ': ('Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách (Lịch sử ở cột Hành động hoặc menu '
                 'Hành động khác) theo đường dẫn ở trên; khối Lịch sử nằm cuối màn hình chi tiết phiếu.'),
}

IMAGES = {2: '01_list', 3: '02_filter', 4: '25_colcfg', 5: '26_filtercfg', 7: '10_create', 10: '12_edit',
          11: '17_detail', 12: '14_wait_detail', 14: '11_quickadd', 18: '15_reject', 20: '13_delete', 22: '18_print',
          25: '20_export'}

USECASES = {
    r'^2\.4 ': ('Người xử lý', 'FR-04', 'Tạo phiếu xử lý', 'crud'),
    r'^2\.5 ': ('Người xử lý', 'FR-05', 'Sửa phiếu xử lý', 'crud'),
    r'^2\.6 ': ('Người dùng có quyền', 'FR-06', 'Xem chi tiết phiếu', 'view'),
    r'^2\.7 ': ('Người xử lý', 'FR-07', 'Thêm nhanh nguyên nhân', 'crud'),
    r'^2\.8 ': ('Người tạo phiếu CCTT', 'FR-08', 'Tạo phiếu cung cấp thông tin', 'action'),
    r'^2\.9 ': ('Người tạo phiếu CCTT', 'FR-09', 'Không duyệt phiếu xử lý', 'action'),
    r'^2\.10 ': ('Người xử lý', 'FR-10', 'Xóa phiếu xử lý', 'action'),
    r'^2\.11 ': ('Người dùng có quyền', 'FR-11', 'In phiếu và in danh sách', 'io'),
    r'^2\.12 ': ('Người dùng có quyền', 'FR-12', 'Xuất Excel', 'io'),
}

PART5 = [  # grep code hrm-api 28/10/2026
    ('1', 'CSKH sau bán', 'Yêu cầu kiểm tra sửa chữa - bảo hành (phiếu yêu cầu gốc: ẩn các thao tác của phòng tiếp '
     'nhận khi đã có phiếu xử lý; nhận lại trạng thái, Người xử lý, Ngày xử lý do phiếu xử lý ghi ngược)',
     'CSKH sau bán -> Kiểm tra bảo hành sửa chữa'),
    ('2', 'CSKH sau bán', 'Phiếu cung cấp thông tin làm báo giá (lập từ phiếu xử lý: chép dòng thiết bị có Hành động '
     'Cung cấp thông tin làm báo giá cùng nguyên nhân; tìm theo số phiếu xử lý; ghi ngược trạng thái Đang CCTT / Đã '
     'CCTT)', 'CSKH sau bán -> Kiểm tra bảo hành sửa chữa'),
    ('3', 'CSKH sau bán', 'Công việc, lỗi thiết bị (chặn xóa nguyên nhân đã được chọn trên phiếu xử lý)',
     'CSKH sau bán -> Danh mục'),
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


def rebuild_ui(doc, sec, tpl, header, data):
    """Bảng mô tả giao diện thiếu cột -> dựng lại theo khuôn bảng đủ cột (tpl), giữ độ rộng cột của khuôn."""
    old = sec_ui(sec)
    widths = [int(g.get(W('w'))) for g in tpl.find(W('tblGrid')).findall(W('gridCol'))]
    anchor = old.getprevious()
    new_table_like(tpl, anchor, header, data, widths)
    old.getparent().remove(old)


# ============================================================== XỬ LÝ
def fix_menu_paragraphs(doc):
    body = doc.element.body
    for old, new in [('  => Yêu cầu kiểm tra sửa chữa bảo hành ', ' => Yêu cầu kiểm tra sửa chữa - bảo hành '),
                     ('  =>', ' =>'),
                     (' => Click vào Số phiếu để xem chi tiết', ' => Bấm vào Số phiếu (Xem chi tiết)'),
                     (' => Click vào Số phiếu để Xem chi tiết ', ' => Bấm vào Số phiếu (Xem chi tiết) '),
                     ('=> Không duyệt ', '=> Không duyệt '),
                     (' => Xuất excel ', ' => Xuất Excel '),
                     (' => Lịch sử', ' => Lịch sử (cột Hành động / menu Hành động khác)'),
                     (' => Tạo phiếu cung cấp thông tin ', ' => Tạo phiếu cung cấp thông tin (cột Hành động / màn chi tiết) '),
                     (' => Xóa ', ' => Xóa (cột Hành động / màn chi tiết) '),
                     (' => In ', ' => In (cột Hành động / menu Hành động khác / màn chi tiết) hoặc In danh sách '),
                     (' => Thêm nhanh ', ' => Thêm nhanh lỗi thiết bị '),
                     (' => Tạo phiếu xử lý yêu cầu ', ' => Tạo phiếu xử lý yêu cầu (cột Hành động / màn chi tiết của phiếu yêu cầu) ')]:
        n = replace_in_texts(body, old, new)
        log('Đường dẫn: "%s" → "%s" (%d chỗ)' % (old.strip(), new.strip(), n))
    its = items(doc)
    n = 0
    for i, e in enumerate(its):
        if e.tag != W('p'):
            continue
        ts = [t for t in e.iter(W('t')) if t.text]
        if not ts or 'Phân hệ CSKH ' not in ts[0].text:
            continue
        ts[0].text = ts[0].text.replace('Phân hệ CSKH ', 'Phân hệ CSKH sau bán ', 1)
        if not ts[0].text.startswith('Menu:') and not txt(its[i - 1]).strip().startswith('Menu:'):
            ts[0].text = 'Menu: ' + ts[0].text
        n += 1
    log('Đổi "Phân hệ CSKH" → "Phân hệ CSKH sau bán" + nhãn Menu: %d dòng' % n)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)
    body = doc.element.body

    fix_menu_paragraphs(doc)
    n = replace_in_texts(body, 'FR-04 tạo phiếu xử lý', 'FR-04 Tạo phiếu xử lý')
    log('Viết hoa FR-04: %d chỗ' % n)

    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    tpl_popup = sec_par(section(doc, r'^2\.10 '), r'^Modal ')
    for rx, popup in POPUPS.items():
        sec = section(doc, rx)
        try:
            set_runs_text(sec_par(sec, r'^Modal '), popup)
        except KeyError:
            paths = [e for e in sec[1] if e.tag == W('p') and '=>' in txt(e)]
            strip_ids(docxlib.clone_par_after(paths[-1], tpl_popup, popup))

    for n_, name in IMAGES.items():
        cap = fig_par(doc, n_)
        set_image(doc, cap.getprevious(), os.path.join(SHOTS, name + '.png'))
        log('Thay ảnh Hình %d (%s) bằng %s.png' % (n_, txt(cap)[len('Hình %d: ' % n_):], name))

    patch_sections(doc, rid)
    patch_part4(doc)
    add_part5(doc)

    for rx, (actor, code, name, grp) in USECASES.items():
        png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
        draw_usecase_qg(png, actor, code, name, grp)
        sec = section(doc, rx)
        blk = usecase_block(sec)
        if blk is None:
            add_usecase(doc, sec, section(doc, r'^2\.8 '), png, 'Biểu đồ Use Case — %s %s' % (code, name))
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
    # ---- 2.1 Xem danh sách: bảng giao diện thiếu cột Trạng thái / Giá trị ban đầu -> dựng lại (theo code)
    s = section(doc, r'^2\.1 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. Người dùng vào màn hình', '1. Người dùng vào menu %s.' % MENU)
    tpl7 = sec_ui(section(doc, r'^2\.3 '))  # khuôn 7 cột
    H7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
    rows = [
        ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Phiếu xử lý yêu cầu', 'Tiêu đề cố định.'),
        ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục', 'Luôn hiển thị, ghim trái khi cuộn ngang.'),
        ('Cột Số phiếu xử lý', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Là liên kết mở màn chi tiết. Sắp xếp '
         'được. Không tắt được.'),
        ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Hiển thị dạng “mã khách hàng - tên khách hàng”.'),
        ('Cột Số phiếu yêu cầu', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định', 'Là liên kết mở phiếu yêu cầu gốc.'),
        ('Cột Tên thiết bị liên quan', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
         'Hiện 2 dòng đầu, còn lại thu gọn sau liên kết “Xem thêm” / “Thu gọn”.'),
        ('Cột Người yêu cầu / Ngày nhận yêu cầu', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
         'Lấy từ phiếu yêu cầu gốc.'),
        ('Cột Địa chỉ sửa chữa', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định', '–'),
        ('Cột Ngày xử lý', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn mặc định',
         'Chỉ có giá trị khi đã tạo phiếu cung cấp thông tin; sắp xếp được.'),
        ('Cột Người xử lý / Ngày tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
         'Người xử lý là người tạo phiếu. Ngày tạo sắp xếp được, mặc định giảm dần.'),
        ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
         'Người cập nhật bản ghi gần nhất / Ngày giờ cập nhật bản ghi gần nhất.'),
        ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 6 giá trị', 'Theo dữ liệu',
         'Chữ và màu do máy chủ quyết định, xem Phần 4 BR-02.'),
        ('Cột Hành động', 'Table/Grid', 'Enable / Ẩn', '–', 'Theo điều kiện từng phiếu',
         'Phiếu có tối đa 3 thao tác thì hiện đủ biểu tượng; nhiều hơn thì hiện 2 thao tác đầu và menu “Hành động '
         'khác”. Thao tác không đủ điều kiện thì ẩn hẳn.'),
        ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả', 'N là tổng số phiếu khớp bộ lọc.'),
        ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, 10 dòng',
         'Có nút về đầu, lùi, số trang, tiến, về cuối.'),
    ]
    rebuild_ui(doc, s, tpl7, H7, [[str(i)] + list(r) for i, r in enumerate(rows, 1)])
    log('2.1.3: dựng lại bảng giao diện đủ cột (Trạng thái, Giá trị ban đầu)')

    # ---- 2.2 Tìm kiếm
    s = section(doc, r'^2\.2 ')
    set_col(sec_ev(s), 2, r'^Bấm Tìm kiếm hoặc nhấn Enter', 'Click')
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Ngày tạo từ / đến$'))[1], ['Ngày tạo (từ → đến)'])
    write_cell(cells(find_row(ui, 1, r'^Ngày tạo'))[-1],
               ['Một ô gồm 2 lịch chọn ngày nối bằng dấu →. Lọc theo ngày tạo phiếu xử lý, tính trọn ngày ở cả hai đầu.'])
    write_cell(cells(find_row(ui, 1, r'^Tên thiết bị$'))[-1], ['Lọc theo tên thiết bị trong phiếu. Chờ Enter hoặc nút Tìm kiếm.'])
    write_cell(cells(find_row(ui, 1, r'^Model$'))[-1], ['Lọc theo model thiết bị trong phiếu. Chờ Enter hoặc nút Tìm kiếm.'])
    write_cell(cells(find_row(ui, 1, r'^Nút Tìm kiếm / Làm mới$'))[4], ['–'])

    # ---- 2.3
    s = section(doc, r'^2\.3 ')
    ui = sec_ui(s)
    li = header_index(ui, 'Loại')
    set_col(ui, li, r'^Danh sách cột$', 'Checkbox')
    set_col(ui, li, r'^Danh sách ô lọc$', 'Checkbox')
    write_cell(cells(find_row(ui, 1, r'^Danh sách ô lọc$'))[4], ['Danh sách 7 ô lọc'])
    ev = sec_ev(s)
    write_cell(ev_cell(ev, r'^Bấm Chọn tất cả'),
               ['After:', '– Chọn tất cả: tích tất cả các cột.',
                '– Bỏ chọn hết: bỏ tích các cột không bắt buộc; cột bắt buộc giữ nguyên.',
                '– Cập nhật dòng “Đang chọn x/y cột”; bảng chưa đổi cho tới khi bấm Lưu.'])
    clone_row_after(ev, r'^Bấm Khôi phục mặc định',
                    [None, 'Kéo thả biểu tượng ở đầu / cuối dòng', 'Drag',
                     ['After:', '– Đổi thứ tự cột / ô lọc trong cửa sổ; áp dụng khi bấm Lưu.']])

    # ---- 2.4 Tạo phiếu: bảng giao diện thiếu cột -> dựng lại 8 cột
    s = section(doc, r'^2\.4 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống kiểm tra dữ liệu, sinh số phiếu, lưu phiếu và cập nhật ngược trạng thái phiếu yêu cầu gốc '
        '(Lưu và gửi: Chờ CCTT, gửi thông báo cho người có quyền Tạo phiếu cung cấp thông tin).',
        '6. Ghi nhận hành động Tạo mới (kèm Thay đổi trạng thái khi gửi) trong lịch sử của phiếu.',
        '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Thoát màn khi đã nhập', UNSAVED)
    tpl8 = sec_ui(section(doc, r'^2\.5 '))
    H8 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả']
    rows = [
        ('Phiếu yêu cầu', 'Textbox', 'Disable', '–', 'Có', 'Số phiếu yêu cầu gốc',
         'Chỉ đọc; ở màn chi tiết là liên kết mở phiếu yêu cầu gốc.'),
        ('Người yêu cầu / Phòng yêu cầu / Ngày nhận yêu cầu', 'Textbox', 'Disable', '–', 'Không',
         'Lấy từ phiếu yêu cầu gốc', 'Chỉ đọc.'),
        ('Khách hàng', 'Textbox', 'Disable', '–', 'Có', 'Lấy từ phiếu yêu cầu gốc', 'Chỉ đọc, không đổi được.'),
        ('Người liên hệ', 'Textbox', 'Disable', '–', 'Có khi Lưu và gửi', 'Lấy từ phiếu yêu cầu gốc', 'Chỉ đọc.'),
        ('Số điện thoại liên hệ / Địa chỉ sửa chữa', 'Textbox', 'Disable', '–', 'Không', 'Lấy từ phiếu yêu cầu gốc',
         'Chỉ đọc.'),
        ('Lý do không duyệt', 'Label', 'Read-only', '–', '–', 'Ẩn khi chưa từng bị Không duyệt',
         'Chữ xám, hiện lý do lần bị Không duyệt gần nhất.'),
        ('Bảng thiết bị – Tên hàng hóa', 'Table/Grid', 'Read-only', '–', 'Có', 'Lấy từ phiếu yêu cầu gốc',
         'Thiết bị khách khai tự do có thêm nút “Chọn hàng hóa tương đương”.'),
        ('Bảng thiết bị – Thương hiệu / Model / Serial / Số BBBGNT-BBXNCV / Nội dung yêu cầu', 'Table/Grid',
         'Read-only', '–', 'Không', 'Lấy từ phiếu yêu cầu gốc', 'Chỉ đọc.'),
        ('Bảng thiết bị – Nguyên nhân', 'Dropdown', 'Enable', 'Danh sách nguyên nhân của đúng hàng hóa',
         'Có khi Lưu và gửi', 'Trống', 'Chọn được nhiều giá trị. Hàng hóa chưa khai nguyên nhân thì hiện dòng nhắc. '
         'Nguyên nhân đã khóa hiển thị kèm biểu tượng ổ khóa.'),
        ('Bảng thiết bị – Nút Thêm nhanh lỗi thiết bị', 'Button', 'Enable', '–', '–', 'Hiển thị',
         'Nằm dưới ô Nguyên nhân của mọi dòng; mở cửa sổ khai bổ sung nguyên nhân, xem mục 2.7.'),
        ('Bảng thiết bị – Hành động', 'Dropdown', 'Enable', 'Tư vấn điện thoại / Cung cấp thông tin làm báo giá',
         'Có khi Lưu và gửi', 'Trống', 'Quyết định hướng đi tiếp của thiết bị.'),
        ('Bảng thiết bị – Nội dung xử lý', 'Textarea', 'Enable / Ẩn', '0–1000 ký tự', 'Có khi chọn Tư vấn điện thoại',
         'Ẩn', 'Chỉ hiện khi Hành động là Tư vấn điện thoại; đổi hành động khác thì bị xóa trắng. Bắt buộc kể cả '
         'khi Lưu nháp.'),
        ('Bảng thiết bị – File đính kèm', 'Button', 'Enable', 'PDF, ảnh, Word, Excel', 'Không', 'Trống',
         'Tải lên ngay khi chọn tệp.'),
        ('Bảng thiết bị – Xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         'Bỏ thiết bị khỏi phiếu xử lý. Không có nút thêm dòng — thiết bị chỉ chép từ phiếu gốc.'),
        ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu ở trạng thái Đang tạo.'),
        ('Nút Lưu và gửi', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Có bước xác nhận “Bạn đồng ý lưu và gửi?”.'),
        ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ]
    rebuild_ui(doc, s, tpl8, H8, [[str(i)] + list(r) for i, r in enumerate(rows, 1)])
    log('2.4.4: dựng lại bảng giao diện đủ cột (Trạng thái, Giá trị ban đầu)')
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Lưu nháp', rid)
    ev_edit(ev, r'^Bấm Lưu nháp', r'^– Ghi một dòng lịch sử', '– Ghi nhận hành động Tạo mới trong lịch sử của phiếu.')
    add_err_line(ev, r'^Bấm Lưu và gửi', rid)
    ev_edit(ev, r'^Bấm Lưu và gửi', r'^– Hiển thị “Gửi phiếu xử lý thành công”',
            ['– Ghi nhận hành động Tạo mới và Thay đổi trạng thái trong lịch sử của phiếu.',
             '– Hiển thị “Gửi phiếu xử lý thành công” và quay về danh sách.'])
    clone_row_after(ev, r'^Bấm Lưu và gửi',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # ---- 2.5 Sửa phiếu
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', [
        '4. Hệ thống kiểm tra dữ liệu, lưu phiếu và cập nhật ngược phiếu yêu cầu gốc khi gửi.',
        '5. Ghi nhận các thay đổi (theo từng trường và từng dòng thiết bị: thêm, bớt, sửa Serial / Nguyên nhân / '
        'Hành động…) trong lịch sử của phiếu.',
        '6. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.'])
    kv_add(kv, 'Dòng sự kiện phụ', [UNSAVED])
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Lưu nháp / Lưu và gửi', rid)
    ev_edit(ev, r'^Bấm Lưu nháp / Lưu và gửi', r'^– Ghi lại phiếu; ghi một dòng lịch sử',
            ['– Ghi lại phiếu; ghi nhận lịch sử “Thay đổi thông tin” liệt kê đúng những trường và dòng thiết bị đã đổi.',
             '– Hiển thị thông báo thành công và quay về danh sách.'])
    clone_row_after(ev, r'^Bấm Lưu nháp / Lưu và gửi',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # ---- 2.6 Xem chi tiết
    s = section(doc, r'^2\.6 ')
    ui = sec_ui(s)
    write_cell(cells(find_row(ui, 1, r'^Khối Lịch sử$'))[-1], ['Bấm “Xem lịch sử” để mở; xem mục 2.13.'])

    # ---- 2.7 Thêm nhanh nguyên nhân (đối chiếu code: nút KHÔNG ẩn theo quyền, máy chủ chặn khi Lưu)
    s = section(doc, r'^2\.7 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. ', '1. Người dùng bấm Thêm nhanh lỗi thiết bị ở ô Nguyên nhân của một '
            'dòng thiết bị.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Không có quyền',
            ['• Nút Thêm nhanh lỗi thiết bị hiển thị ở mọi dòng; người không có quyền Quản lý danh mục công việc - '
             'lỗi thiết bị bấm Lưu thì hệ thống từ chối và báo không có quyền.', CLOSE_POPUP])
    ui = sec_ui(s)
    li = header_index(ui, 'Loại')
    for rx in (r'^Định mức công$', r'^Định mức đàm phán', r'^VAT', r'^Đơn giá bán$', r'^Hệ số công nghệ$'):
        set_col(ui, li, rx, 'Textbox')
    add_err_line(sec_ev(s), r'^Bấm Lưu', rid)

    # ---- 2.8 Tạo phiếu CCTT
    s = section(doc, r'^2\.8 ')
    ui = sec_ui(s)
    li = header_index(ui, 'Loại')
    set_col(ui, li, r'^Nút Tạo phiếu cung cấp thông tin$', 'Button')
    write_cell(cells(find_row(ui, 1, r'^Menu Hành động khác$'))[-1],
               ['Ở dòng phiếu Chờ CCTT: hiện thẳng Tạo phiếu cung cấp thông tin và Không duyệt; menu chứa In, Lịch sử.'])
    set_col(ui, li, r'^Menu Hành động khác$', 'Button')

    # ---- 2.9 Không duyệt
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', [
        '4. Hệ thống chuyển phiếu về trạng thái Đang tạo và lưu lý do (phiếu yêu cầu gốc giữ nguyên).',
        '5. Ghi nhận hành động Không duyệt kèm lý do trong lịch sử của phiếu và gửi thông báo cho người tạo phiếu.',
        '6. Hệ thống báo thành công và nạp lại màn đang đứng (danh sách hoặc chi tiết phiếu).'])
    kv_add(kv, 'Dòng sự kiện phụ', [CLOSE_POPUP])
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm Không duyệt trong cửa sổ', rid)
    ev_edit(ev, r'^Bấm Không duyệt trong cửa sổ', r'^– Hiển thị “Không duyệt phiếu thành công”',
            '– Hiển thị “Không duyệt phiếu thành công” và nạp lại màn đang đứng (danh sách hoặc chi tiết).')

    # ---- 2.10 Xóa
    s = section(doc, r'^2\.10 ')
    add_err_line(sec_ev(s), r'^Bấm Xóa ở hộp xác nhận', rid)
    ev_edit(sec_ev(s), r'^Bấm Xóa ở hộp xác nhận', r'^– Ghi một dòng lịch sử “Xóa”',
            ['– Ghi nhận hành động Xóa trong lịch sử.',
             '– Hiển thị “Xóa thành công”; xóa từ danh sách thì nạp lại danh sách, xóa từ màn chi tiết thì quay về '
             'danh sách.'])

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

    # ---- 2.13 Lịch sử (code #11644: bảng thiết bị ĐÃ được ghi lịch sử)
    s = section(doc, r'^2\.13 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa có thao tác nào',
            '• Phiếu tạo từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện “Chưa có lịch sử thao tác nào.”')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu tạo từ hệ thống cũ không', None)
    kv_edit(kv, 'Yêu cầu đặc biệt', r'.',
            'Thay đổi ở bảng thiết bị được ghi rõ thiết bị nào thêm mới, bị xóa, hoặc sửa ô nào (Serial, Nguyên nhân, '
            'Hành động, Nội dung xử lý…).')
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

    write_cell(row('BR-08')[4], ['- Chỉnh sửa phiếu', '- Xóa phiếu'])
    write_cell(row('BR-01')[4], ['- Tạo phiếu'])
    write_cell(row('BR-02')[4], ['- Toàn màn hình'])
    tc = row('BR-01')[3]
    write_cell(tc, lines_replace(cell_lines(tc), r'^– Số phiếu theo khuôn',
                                 '– Số phiếu theo khuôn “<mã công ty ghi trên phiếu>.PXL.<năm 4 số><số thứ tự 6 chữ '
                                 'số>”, ví dụ TPE.PXL.2026006619.'))
    for i, tr in enumerate(rows(tbl)[1:], 1):
        assert txt(cells(tr)[1]).strip() == 'BR-%02d' % i, 'Mã BR không liên tục ở dòng %d' % i


def add_part5(doc):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    intro = strip_ids(docxlib.clone_par_after(
        h5, h4.getnext(), 'Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của %s.' % SCREEN))
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1500, 3600, 2900])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()
