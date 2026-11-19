# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu hủy hàng giữ" (STT 191, bản Drive tải 28/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Phiếu hủy hàng giữ.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Riêng bản Drive này: MỌI tiêu đề 2.x.y là đoạn thường (đặt lại Heading4), dòng đường dẫn thiếu chữ "Menu:" và
chèn icon menu giữa dòng, câu popup mục 2.6 ghi sai màn (phải là màn Tạo mới), câu dẫn Phần 4 thiếu ý "không lặp
lại". Màn chỉ có 2 cấp phạm vi (tổng công ty / công ty), không có Sửa/Xóa, có 2 lối vào màn lập phiếu.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'phieu-theo-form-quoc-gia'))
import docx  # noqa: E402
from srs_common import *  # noqa: E402,F401,F403
import formqg_lib as L  # noqa: E402

SRC = os.path.join(HERE, 'drive_0710', 'SRS_Drive.docx')
OUT_DIR = os.path.join(HERE, 'out')
OUT = os.path.join(OUT_DIR, 'SRS - Phiếu hủy hàng giữ.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'màn Phiếu hủy hàng giữ'
MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng => Phiếu hủy hàng giữ'
MENU_REQ = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng => Yêu cầu hủy hàng giữ'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Xem phiếu hàng giữ theo tổng công ty / công ty (V1–V2) '
              'và quyền Quản lý giữ hàng (Q1 — xem phiếu thuộc công ty mình); không có quyền nào thì chỉ thấy phiếu do '
              'mình lập hoặc sinh ra từ phiếu yêu cầu do mình lập.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (Q1, V1–V2); không có quyền nào vẫn xem được phiếu liên quan tới mình.')
COND_LIST3 = COND_LIST + '\n3. Đang ở màn danh sách Phiếu hủy hàng giữ.'
ACTOR_Q1 = 'Người dùng có quyền Quản lý giữ hàng (Q1).'
COND_CREATE = ('1. Đăng nhập thành công.\n'
               '2. Có quyền Quản lý giữ hàng (Q1).\n'
               '3. Có ít nhất một phiếu yêu cầu hủy hàng giữ đang ở trạng thái Chờ duyệt cùng công ty.')
COND_PICK = ('1. Đăng nhập thành công.\n'
             '2. Có quyền Quản lý giữ hàng (Q1); thiếu quyền thì cửa sổ luôn rỗng.\n'
             '3. Đang ở màn Lập phiếu hủy hàng giữ (Tạo mới).')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu hủy; người lập phiếu yêu cầu gốc; người có quyền Quản '
               'lý giữ hàng (Q1) cùng công ty; hoặc người có quyền Xem phiếu hàng giữ theo tổng công ty / công ty '
               '(V1–V2) trong phạm vi được giao.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng.')

SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST, COND_LIST3),
    r'^2\.3 ': ('Bộ lọc và lưu cấu hình theo người dùng.', ACTOR_LIST, COND_LIST3),
    r'^2\.4 ': ('Cấu hình cột hiển thị.', ACTOR_LIST, COND_LIST3),
    r'^2\.5 ': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.', ACTOR_Q1, COND_CREATE),
    r'^2\.6 ': ('Quy tắc cửa sổ chọn dữ liệu, Kịch bản tìm kiếm và Phân trang.', ACTOR_Q1, COND_PICK),
    r'^2\.7 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.8 ': ('Quy tắc màn In và bố cục bản in.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.9 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.10 ': ('Quy tắc Excel và Cấu hình cột.', ACTOR_LIST, COND_LIST3),
}

# 2.1 / 2.2 bản Drive tách đường dẫn làm 2 dòng ("… => Giữ hàng [icon]" + "=> Phiếu hủy hàng giữ [icon]") -> gộp
DROP_PARS = [r'^\s*=> Phiếu hủy hàng giữ\s*$']
MENU_LINES = {
    (r'^2\.1 ', 0): ('Menu: %s' % MENU, None),
    (r'^2\.2 ', 0): ('Menu: %s => Tìm kiếm nâng cao' % MENU, None),
    (r'^2\.3 ', 0): ('Menu: %s => Cài đặt bộ lọc' % MENU,
                     'Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    (r'^2\.4 ', 0): ('Menu: %s => Cấu hình cột hiển thị' % MENU,
                     'Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    (r'^2\.5 ', 0): ('Menu: %s => Tạo mới' % MENU,
                     'Hoặc Menu: %s => Duyệt (trên dòng phiếu Chờ duyệt) / Xem chi tiết => Tạo phiếu hủy hàng giữ '
                     '(màn lập phiếu mở sẵn đúng phiếu yêu cầu đó).' % MENU_REQ),
    (r'^2\.6 ', 0): ('Menu: %s => Tạo mới => biểu tượng tra cứu cạnh ô Phiếu yêu cầu hủy hàng giữ' % MENU,
                     'Modal Phiếu yêu cầu hủy hàng giữ chờ duyệt được mở ngay trên màn hình Tạo mới (Lập phiếu hủy '
                     'hàng giữ) theo đường dẫn ở trên.'),
    (r'^2\.7 ', 0): ('Menu: %s => bấm Mã phiếu' % MENU, None),
    (r'^2\.8 ', 0): ('Menu: %s => In (trên dòng phiếu) / Xem chi tiết => In' % MENU,
                     'Modal Xem trước phiếu hủy hàng giữ được mở ngay trên màn hình danh sách hoặc màn hình chi tiết '
                     'phiếu theo đường dẫn ở trên.'),
    (r'^2\.9 ', 0): ('Menu: %s => Lịch sử (trên dòng phiếu) / Xem chi tiết => Xem lịch sử' % MENU,
                     'Modal Lịch sử phiếu hủy hàng giữ được mở ngay trên màn hình danh sách theo đường dẫn ở trên; '
                     'khối Lịch sử thay đổi nằm cuối màn hình chi tiết phiếu.'),
    (r'^2\.10 ', 0): ('Menu: %s => Xuất Excel' % MENU,
                      'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
}

USECASES = {
    r'^2\.5 ': ('Quản lý giữ hàng', 'FR-05', 'Lập phiếu hủy hàng giữ', 'crud'),
    r'^2\.6 ': ('Quản lý giữ hàng', 'FR-06', 'Chọn phiếu yêu cầu từ cửa sổ tra cứu', 'crud'),
    r'^2\.7 ': ('Người dùng có quyền', 'FR-07', 'Xem chi tiết phiếu', 'view'),
    r'^2\.8 ': ('Người dùng có quyền', 'FR-08', 'In phiếu', 'io'),
    r'^2\.10 ': ('Người dùng có quyền', 'FR-10', 'Xuất Excel danh sách', 'io'),
}
NO_UC = [r'^2\.3 ', r'^2\.4 ']

IMAGES = [
    (r'lúc mới truy cập', '01_list', None),
    (r'Khu vực Tìm kiếm nâng cao đang mở', '02_filter', None),
    (r'Cửa sổ Cài đặt bộ lọc', '26_filtercfg', None),
    (r'Cửa sổ Tùy chỉnh cột hiển thị', '25_colcfg', None),
    (r'khi chưa chọn phiếu yêu cầu', '10_create_empty', None),
    (r'sau khi đã chọn phiếu yêu cầu', '10_create', None),
    (r'Cửa sổ chọn phiếu yêu cầu', '11_request', None),
    (r'Màn Chi tiết phiếu hủy hàng giữ', '17_detail', None),
    (r'Cửa sổ xem trước bản in', '18_print', None),
    (r'Khối Lịch sử thay đổi', '16_history_detail', None),
    (r'Cửa sổ Chọn trường xuất Excel', '20_export', None),
]

PART5 = [
    ('1', 'Tài chính', 'Yêu cầu hủy hàng giữ (màn chi tiết phiếu yêu cầu Đã duyệt: ô Phiếu hủy hàng giữ hiện mã và '
     'liên kết tới phiếu hủy đã lập)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('2', 'Tài chính', 'Danh sách hàng giữ (cửa sổ lịch sử biến động của lô: cột Chứng từ hiện mã và liên kết tới '
     'phiếu hủy hàng giữ đã trừ tồn)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('3', 'Tài chính', 'Hàng sắp hết hạn giữ (cửa sổ lịch sử biến động của lô, như màn Danh sách hàng giữ)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('4', 'Danh mục', 'Hàng hoá, vật tư (xóa hàng hóa: chặn khi hàng đã có trên phiếu hủy hàng giữ)',
     'Danh mục -> Hàng hoá -> Hàng hoá, vật tư'),
]
PART5_INTRO = ('Các màn hình dưới đây đọc dữ liệu do màn Phiếu hủy hàng giữ ghi ra (phiếu hủy, dòng hàng và nhật ký '
               'biến động hàng giữ ghi khi lập phiếu).')


# ============================================================== XỬ LÝ
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)
    normalize_subheadings(doc)

    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    drop_pars(doc, DROP_PARS)
    apply_menu_lines(doc, MENU_LINES)
    patch_sections(doc, rid)
    patch_part4(doc)
    add_part5(doc, PART5, PART5_INTRO)
    replace_images(doc, IMAGES, SHOTS)

    for rx in NO_UC:
        remove_usecase(doc, section(doc, rx))
    redraw_usecases(doc, USECASES, UML, tpl_rx=r'^2\.5 ')
    renumber_subheadings(doc)
    log('Số Hình sau khi đánh lại: %d' % renumber_figures(doc))
    drop_empty_before_h1(doc)
    check_types(doc)

    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        word_finalize(OUT, os.path.splitext(OUT)[0] + '.pdf')


def patch_sections(doc, rid):
    # 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. Người dùng vào menu', '1. Người dùng vào menu %s.' % MENU)
    ui = sec_ui(s)
    ui_set(ui, r'^Cột Trạng thái$', {'Loại': 'Table/Grid'})
    ui_set(ui, r'^Nút Tạo mới$', {'Mô tả': 'Mở màn Lập phiếu hủy hàng giữ. Người thiếu quyền Quản lý giữ hàng vẫn mở '
                                          'được màn nhưng cửa sổ chọn phiếu yêu cầu không có dòng nào.'})
    delete_row(ui, r'^Vòng quay chờ')

    # 2.2 Tìm kiếm: 6 ô lọc, ô Ngày tạo là MỘT ô khoảng ngày, ô tìm nhanh chỉ tìm theo mã
    s = section(doc, r'^2\.2 ')
    kv_set(sec_kv(s), 'Mô tả', 'Thu hẹp danh sách theo ô tìm nhanh và sáu tiêu chí lọc nâng cao.')
    ui = sec_ui(s)
    ui_set(ui, r'^Ô tìm nhanh$', {'Mô tả': 'Gợi ý “Tìm theo mã phiếu, mã phiếu yêu cầu...”. Tìm theo mã phiếu hủy và '
                                          'mã phiếu yêu cầu. Chỉ áp dụng khi bấm Tìm kiếm hoặc nhấn Enter.'})
    ui_set(ui, r'^Ô lọc Ngày tạo từ$', {'Tên đối tượng': 'Ô lọc Ngày tạo', 'Phạm vi': 'dd/mm/yyyy → dd/mm/yyyy',
                                        'Mô tả': 'Một ô chọn khoảng ngày (từ ngày → đến ngày), lọc theo ngày tạo phiếu '
                                                 'hủy.'})
    delete_row(ui, r'^Ô lọc Ngày tạo đến$')

    # 2.3 Cài đặt bộ lọc
    s = section(doc, r'^2\.3 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'bảy ô lọc', '2. Cửa sổ hiện danh sách sáu ô lọc kèm ô tích chọn.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'Khôi phục mặc định', '• Bấm Khôi phục mặc định → đưa về đủ sáu ô lọc theo thứ tự '
            'gốc.')
    ui = sec_ui(s)
    ui_set(ui, r'^Danh sách ô lọc$', {'Phạm vi': 'Sáu ô lọc'})
    ev = sec_ev(s)
    ev_set(ev, r'^Bấm Khôi phục mặc định$', ['After:', '– Đưa danh sách về đủ sáu ô lọc theo thứ tự gốc.'])
    tr = find_row(ev, 1, r'^Kéo thả một dòng$')
    write_cell(cells(tr)[2], ['Drag'])

    # 2.4 Tùy chỉnh cột
    s = section(doc, r'^2\.4 ')
    set_runs_text(s[0], '2.4 Tùy chỉnh cột hiển thị')
    ui_set(sec_ui(s), r'^Ô tích chọn của cột bị khóa$', {'Loại': 'Checkbox'})
    write_cell(cells(find_row(sec_ev(s), 1, r'^Bỏ tích một cột bị khóa$'))[2], ['Change'])

    # 2.5 Lập phiếu hủy (= duyệt phiếu yêu cầu)
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_set(kv, 'Dòng sự kiện chính',
           '1. Người dùng mở màn lập phiếu theo một trong hai lối: bấm Tạo mới ở màn danh sách Phiếu hủy hàng giữ; '
           'hoặc ở màn Yêu cầu hủy hàng giữ bấm Duyệt (trên dòng phiếu Chờ duyệt) / Tạo phiếu hủy hàng giữ (màn chi '
           'tiết) — khi đó phiếu yêu cầu đã được chọn sẵn, bỏ qua bước 2–3.\n'
           '2. Người dùng bấm nút tra cứu cạnh ô Phiếu yêu cầu hủy hàng giữ để mở cửa sổ chọn phiếu.\n'
           '3. Người dùng chọn một phiếu yêu cầu đang chờ duyệt.\n'
           '4. Hệ thống điền sẵn Người yêu cầu, Phòng ban yêu cầu, Khách hàng và nạp các dòng hàng hóa được đề nghị '
           'hủy, kèm số Có thể hủy tính lại tại thời điểm mở form; Duyệt hủy điền sẵn bằng số Yêu cầu hủy.\n'
           '5. Người dùng tích / bỏ tích cột Cần hủy và sửa số ở cột Duyệt hủy nếu cần; nhập Ghi chú (không bắt buộc).\n'
           '6. Người dùng bấm Duyệt (hoặc Duyệt và tiếp tục) và xác nhận trên hộp “Xác nhận duyệt”.\n'
           '7. Hệ thống lưu phiếu, trừ tồn hàng giữ, chuyển phiếu yêu cầu sang Đã duyệt.\n'
           '8. Ghi nhận hành động Tạo mới trong lịch sử phiếu hủy và hành động Duyệt trong lịch sử phiếu yêu cầu; gửi '
           'thông báo cho người lập phiếu yêu cầu.\n'
           '9. Hệ thống báo thành công và quay về màn danh sách Phiếu hủy hàng giữ (Duyệt và tiếp tục: mở lại màn lập '
           'phiếu trống).')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Hủy trên hộp thoại xác nhận', [
        '• Bấm Hủy trên hộp Xác nhận duyệt → không lưu, giữ nguyên dữ liệu đang nhập.',
        '• Nút Duyệt và tiếp tục chỉ có khi vào bằng nút Tạo mới (lối 1).',
        '• Bấm Quay lại: vào bằng lối 1 → về danh sách Phiếu hủy hàng giữ; vào bằng lối 2 → về danh sách Yêu cầu hủy '
        'hàng giữ.', UNSAVED])
    ui = sec_ui(s)
    ui_set(ui, r'^Ô Ghi chú$', {'Loại': 'Textarea'})
    ui_set(ui, r'^Cột Cần hủy$', {'Loại': 'Checkbox'})
    ui_set(ui, r'^Ô Duyệt hủy$', {'Loại': 'Textbox', 'Phạm vi': '> 0 và ≤ Có thể hủy, tối đa 2 số lẻ'})
    ui_set(ui, r'^Nút Duyệt và tiếp tục$', {'Mô tả': 'Chỉ hiện khi vào bằng nút Tạo mới (không có khi mở từ phiếu yêu '
                                                    'cầu) và đã chọn phiếu yêu cầu.'})
    ui_set(ui, r'^Nút Quay lại$', {'Mô tả': 'Về danh sách Phiếu hủy hàng giữ (lối 1) hoặc danh sách Yêu cầu hủy hàng '
                                           'giữ (lối 2); có thay đổi chưa lưu thì hỏi xác nhận.'})
    ui_set(ui, r'^Thông báo lỗi dưới ô$', {'Loại': 'Label'})
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Nhập ô Duyệt hủy$'))[2], ['Change'])
    write_cell(cells(find_row(ev, 1, r'^Bỏ tích ô Cần hủy$'))[2], ['Change'])
    tc = cells(find_row(ev, 1, r'^Bấm Duyệt$'))[3]
    lines = cell_lines(tc)
    i = lines.index('After:') if 'After:' in lines else len(lines)
    lines = lines[:i] + ['After:', '– Lưu phiếu hủy, trừ tồn hàng giữ, chuyển phiếu yêu cầu sang Đã duyệt.',
                         '– Ghi nhận hành động Tạo mới (phiếu hủy) và Duyệt (phiếu yêu cầu) trong lịch sử; gửi thông '
                         'báo cho người lập phiếu yêu cầu.',
                         '– Báo “Duyệt phiếu thành công” và quay về danh sách Phiếu hủy hàng giữ.']
    write_cell(tc, lines)
    add_err_line(ev, r'^Bấm Duyệt$', rid)
    tr = find_row(ev, 1, r'^Rời màn khi chưa lưu$')
    write_cell(cells(tr)[1], ['Bấm Quay lại / chọn menu khác / đóng tab trình duyệt'])
    write_cell(cells(tr)[2], ['Click'])
    write_cell(cells(tr)[3], UNSAVED_EV)

    # 2.6 Cửa sổ chọn phiếu yêu cầu
    s = section(doc, r'^2\.6 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ', '3. Người dùng có thể lọc theo Mã phiếu hoặc Người tạo rồi bấm Tìm '
            'kiếm (Làm mới để xóa điều kiện lọc).')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm ra ngoài', '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, '
            'không chọn gì, màn lập phiếu giữ nguyên.')
    ui = sec_ui(s)
    clone_row_after(ui, r'^Ô lọc Người tạo$', [None, 'Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
                                              'Lọc lại danh sách theo Mã phiếu, Người tạo.'])
    clone_row_after(ui, r'^Nút Tìm kiếm$', [None, 'Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
                                           'Xóa điều kiện lọc và nạp lại danh sách.'])
    clone_row_after(ui, r'^Trạng thái rỗng$', [None, 'Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị',
                                              'Đóng cửa sổ, không chọn phiếu nào.'])
    ev = sec_ev(s)
    tr = find_row(ev, 1, r'^Nhập ô lọc rồi tìm$')
    write_cell(cells(tr)[1], ['Bấm Tìm kiếm / Làm mới'])
    write_cell(cells(tr)[2], ['Click'])
    write_cell(cells(tr)[3], ['After:', '– Tìm kiếm: nạp lại danh sách trong cửa sổ theo điều kiện lọc.',
                              '– Làm mới: xóa điều kiện lọc và nạp lại danh sách.'])

    # 2.7 Xem chi tiết
    s = section(doc, r'^2\.7 ')
    ui_set(sec_ui(s), r'^Ô Ghi chú$', {'Loại': 'Textarea'})

    # 2.8 In phiếu
    s = section(doc, r'^2\.8 ')
    ui_set(sec_ui(s), r'^Tiêu đề cửa sổ$', {'Giá trị ban đầu': 'Xem trước phiếu <mã phiếu> (mở từ danh sách) / Xem '
                                                                'trước phiếu hủy hàng giữ (mở từ màn chi tiết)'})
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'^• Bấm đóng', '• Bấm (x) → đóng cửa sổ xem trước, không in.')

    # 2.9 Lịch sử
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_set(kv, 'Dòng sự kiện phụ',
           '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → cửa sổ hiện “Chưa có lịch sử thay '
           'đổi.”, khối ở màn chi tiết hiện “Chưa có lịch sử thao tác nào.”.\n'
           '• Bấm Làm mới (khối ở màn chi tiết) → nạp lại danh sách mốc.\n'
           '• Bấm Thu gọn → đóng khối lịch sử; bấm Đóng / (x) → đóng cửa sổ lịch sử.')
    ui_set(sec_ui(s), r'^Trạng thái rỗng$', {'Mô tả': 'Hiện “Chưa có lịch sử thay đổi.” (cửa sổ) / “Chưa có lịch sử '
                                                      'thao tác nào.” (khối ở màn chi tiết).'})

    # 2.10 Xuất Excel
    s = section(doc, r'^2\.10 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ', '3. Người dùng tích thêm hoặc bỏ bớt trường, kéo biểu tượng ☰ để đổi '
            'thứ tự cột.')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Kết quả lọc rỗng → vẫn xuất tệp gồm tiêu đề và dòng tên cột, không có dòng dữ liệu.'])
    ui = sec_ui(s)
    ui_set(ui, r'^Danh sách trường$', {'Loại': 'Checkbox', 'Mô tả': 'Gồm Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người '
                                       'tạo, Ngày tạo, Trạng thái, Người cập nhật, Ngày cập nhật, Khách hàng, Ghi chú. '
                                       'Kéo biểu tượng ☰ để đổi thứ tự cột trong tệp.'})
    clone_row_after(ui, r'^Nút Đóng$', [None, 'Số trường đang chọn', 'Label', 'Read-only', 'Đang chọn x/10 trường',
                                       'Góc trái cuối cửa sổ, cập nhật ngay khi tích / bỏ tích.'])


def patch_part4(doc):
    tbl = part4_intro(doc, SCREEN)
    br_desc(tbl, 'BR-03', r'^– Vượt khoảng thì báo lỗi ngay dưới ô', None)
    clone_row_after(tbl, r'^BR-07$', [None, 'BR-08', 'Lối vào màn lập phiếu và màn hình trở về', [
        '– Lối 1: nút Tạo mới ở danh sách Phiếu hủy hàng giữ — tự chọn phiếu yêu cầu qua cửa sổ tra cứu; có thêm nút '
        'Duyệt và tiếp tục.',
        '– Lối 2: nút Duyệt / Tạo phiếu hủy hàng giữ ở màn Yêu cầu hủy hàng giữ — phiếu yêu cầu được chọn sẵn.',
        '– Duyệt xong (cả 2 lối) → về danh sách Phiếu hủy hàng giữ; Duyệt và tiếp tục → mở lại màn lập phiếu trống.',
        '– Quay lại khi chưa duyệt → về danh sách của lối đã vào.'], 'Lập phiếu hủy'])
    check_br(tbl)


if __name__ == '__main__':
    main()
