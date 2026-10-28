# -*- coding: utf-8 -*-
"""Vá SRS "Yêu cầu hủy hàng giữ" (STT 32, bản Drive tải 28/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Yêu cầu hủy hàng giữ.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Chạy lại bao nhiêu lần cũng được: luôn đọc bản Drive gốc. Khuôn chép từ màn 27
(finance-product-import-direct-transfer/form_qg/patch_srs.py); phần hàm chung + riêng 2 màn hàng giữ ở
../srs_common.py.
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
OUT = os.path.join(OUT_DIR, 'SRS - Yêu cầu hủy hàng giữ.docx')
UML = os.path.join(HERE, 'uml')
SHOTS = os.path.join(HERE, 'hdsd_shots')

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'màn Yêu cầu hủy hàng giữ'
OLD_MENU = 'Phân hệ Tài chính => Giữ hàng => '
# finance.js: hubGroup 'Hàng hoá - Dịch vụ - Vận chuyển' > nhóm 'Giữ hàng' > mục màn
MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Giữ hàng => Yêu cầu hủy hàng giữ'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Phạm vi phiếu nhìn thấy theo quyền Quản lý giữ hàng (Q1) và quyền Xem phiếu hàng giữ theo '
              'tổng công ty / công ty / phòng ban (V1–V3); không có quyền nào thì chỉ thấy phiếu của mình.')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (Q1, V1–V3); không có quyền nào vẫn xem được phiếu do chính mình lập.')
COND_LIST3 = COND_LIST + '\n3. Đang ở màn danh sách phiếu.'
ACTOR_CREATE = ('Người lập phiếu — người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình '
                '(chức năng lập phiếu không gắn quyền riêng).')
COND_CREATE = ('1. Đăng nhập thành công.\n'
               '2. Vào được màn Yêu cầu hủy hàng giữ (lập phiếu không gắn quyền riêng).\n'
               '3. Người lập đang giữ hàng cho ít nhất một khách hàng.')
ACTOR_OWNER = ('Người lập phiếu — người dùng có quyền thực hiện chức năng: chỉ người đã lập phiếu '
               '(chức năng không gắn quyền riêng).')
COND_OWNER = ('1. Đăng nhập thành công.\n'
              '2. Là người lập phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Đang tạo (kể cả phiếu bị Không duyệt trả về).')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người lập phiếu; người có quyền Quản lý giữ hàng (Q1) — xem mọi phiếu '
               'khác Đang tạo; hoặc người có quyền Xem phiếu hàng giữ theo tổng công ty / công ty / phòng ban (V1–V3) '
               'trong phạm vi được giao.')
COND_SCOPE = ('1. Đăng nhập thành công.\n'
              '2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Đang tạo chỉ người lập xem được.')
ACTOR_Q1 = 'Người dùng có quyền Quản lý giữ hàng (Q1).'
COND_Q1 = ('1. Đăng nhập thành công.\n'
           '2. Có quyền Quản lý giữ hàng (Q1).\n'
           '3. Phiếu đang ở trạng thái Chờ duyệt.')
FORM_RULE = 'Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.'
STATE_RULE = 'Thông báo, Quy tắc ghi lịch sử và UI/UX của thao tác đổi trạng thái.'

SECTIONS = {
    r'^2\.1 ': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 ': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST, COND_LIST3),
    r'^2\.3 ': ('Bộ lọc và lưu cấu hình theo người dùng.', ACTOR_LIST, COND_LIST3),
    r'^2\.4 ': ('Cấu hình cột hiển thị.', ACTOR_LIST, COND_LIST3),
    r'^2\.5 ': (FORM_RULE, ACTOR_CREATE, COND_CREATE),
    r'^2\.6 ': (FORM_RULE, ACTOR_OWNER, COND_OWNER),
    r'^2\.7 ': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.8 ': (STATE_RULE, ACTOR_Q1, COND_Q1),
    r'^2\.9 ': (STATE_RULE, ACTOR_Q1, COND_Q1),
    r'^2\.10 ': ('Quy tắc xóa và Thông báo.', ACTOR_OWNER, COND_OWNER),
    r'^2\.11 ': ('Quy tắc màn In và bố cục bản in.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.12 ': ('Quy tắc Excel và Cấu hình cột.', ACTOR_LIST, COND_LIST3),
    r'^2\.13 ': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

# Dòng "Menu:" thứ k của mục -> (chữ mới, câu popup đặt ngay sau | None)
MENU_LINES = {
    (r'^2\.1 ', 0): ('Menu: %s' % MENU, None),
    (r'^2\.2 ', 0): ('Menu: %s => Tìm kiếm nâng cao' % MENU, None),
    (r'^2\.3 ', 0): ('Menu: %s => Cài đặt bộ lọc' % MENU,
                     'Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    (r'^2\.4 ', 0): ('Menu: %s => Cấu hình cột hiển thị' % MENU,
                     'Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    (r'^2\.5 ', 0): ('Menu: %s => Tạo mới' % MENU, None),
    (r'^2\.5 ', 1): ('Menu: %s => Tạo mới / Sửa => Thêm hàng hóa' % MENU,
                     'Modal Hàng đang giữ cho khách hàng được mở ngay trên màn hình Tạo mới hoặc Chỉnh sửa phiếu '
                     'theo đường dẫn ở trên.'),
    (r'^2\.6 ', 0): ('Menu: %s => Sửa (trên dòng phiếu) / Xem chi tiết => Sửa' % MENU, None),
    (r'^2\.7 ', 0): ('Menu: %s => bấm Mã phiếu' % MENU, None),
    (r'^2\.8 ', 0): ('Menu: %s => Duyệt (trên dòng phiếu) / Xem chi tiết => Tạo phiếu hủy hàng giữ' % MENU, None),
    (r'^2\.9 ', 0): ('Menu: %s => Xem chi tiết => Không duyệt' % MENU,
                     'Modal Không duyệt yêu cầu hủy hàng giữ được mở ngay trên màn hình chi tiết phiếu theo đường '
                     'dẫn ở trên.'),
    (r'^2\.9 ', 1): ('Menu: %s => Sửa (phiếu bị Không duyệt trả về)' % MENU, None),
    (r'^2\.10 ', 0): ('Menu: %s => Xóa (trên dòng phiếu) / Xem chi tiết => Xóa' % MENU,
                      'Modal Xác nhận xóa được mở ngay trên màn hình danh sách (biểu tượng Xóa trên dòng) hoặc màn '
                      'hình chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    (r'^2\.11 ', 0): ('Menu: %s => In (trên dòng phiếu) / Xem chi tiết => In' % MENU,
                      'Modal Xem trước bản in được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo '
                      'đường dẫn ở trên.'),
    (r'^2\.12 ', 0): ('Menu: %s => Xuất Excel' % MENU,
                      'Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
    (r'^2\.13 ', 0): ('Menu: %s => Lịch sử (trên dòng phiếu) / Xem chi tiết => Xem lịch sử' % MENU,
                      'Modal Lịch sử yêu cầu hủy hàng giữ được mở ngay trên màn hình danh sách theo đường dẫn ở trên; '
                      'khối Lịch sử thay đổi nằm cuối màn hình chi tiết phiếu.'),
}
# Câu popup cũ đặt sai chỗ / sai màn -> bỏ (câu mới đã đặt ngay sau dòng Menu)
DROP_PARS = [r'^Cửa sổ Không duyệt được mở ngay', r'^Hộp thoại xác nhận xóa được mở ngay']

USECASES = {
    r'^2\.5 ': ('Người lập phiếu', 'FR-05', 'Tạo mới phiếu', 'crud'),
    r'^2\.6 ': ('Người lập phiếu', 'FR-06', 'Chỉnh sửa phiếu', 'crud'),
    r'^2\.7 ': ('Người dùng có quyền', 'FR-07', 'Xem chi tiết phiếu', 'view'),
    r'^2\.8 ': ('Quản lý giữ hàng', 'FR-08', 'Duyệt — lập Phiếu hủy hàng giữ', 'action'),
    r'^2\.9 ': ('Quản lý giữ hàng', 'FR-09', 'Không duyệt phiếu', 'action'),
    r'^2\.10 ': ('Người lập phiếu', 'FR-10', 'Xóa phiếu', 'action'),
    r'^2\.11 ': ('Người dùng có quyền', 'FR-11', 'In phiếu', 'io'),
    r'^2\.12 ': ('Người dùng có quyền', 'FR-12', 'Xuất Excel danh sách', 'io'),
}
NO_UC = [r'^2\.3 ', r'^2\.4 ']

# Ảnh cũ (giao diện trước đợt sửa: 2 ô Ngày tạo từ/đến, 9 ô lọc, Ghi chú 1 dòng, chú thích dưới ô Khách hàng,
# bản in mở tab riêng...) -> thay bằng ảnh chụp dev 28/10 (dùng chung bộ ảnh HDSD)
IMAGES = [
    (r'lúc mới truy cập', '01_list', None),
    (r'Bảng lọc nâng cao đang mở', '02_filter', None),
    (r'Cửa sổ Cài đặt bộ lọc', '26_filtercfg', None),
    (r'Cửa sổ Tuỳ chỉnh cột', '25_colcfg', 'Cửa sổ Tùy chỉnh cột'),
    (r'Màn lập phiếu yêu cầu hủy', '10_create', None),
    (r'Popup Hàng đang giữ', '11_stock', None),
    (r'Màn sửa phiếu, có khối', '12_edit', 'Màn sửa phiếu yêu cầu hủy hàng giữ'),
    (r'Màn chi tiết phiếu đã duyệt', '17_detail_approved', None),
    (r'Nút Tạo phiếu hủy hàng giữ nằm', '17_detail', None),
    (r'Cửa sổ Không duyệt', '15_reject', None),
    (r'Khối Lý do không duyệt hiển thị', '19_reason', None),
    (r'Hộp thoại Xác nhận xóa', '13_delete', None),
    (r'Bản in phiếu yêu cầu', '18_print', 'Cửa sổ Xem trước bản in phiếu yêu cầu hủy hàng giữ'),
    (r'Cửa sổ Chọn trường xuất Excel', '20_export', None),
    (r'Khối Lịch sử thay đổi ở cuối', '16_history_detail', None),
]

PART5 = [  # STT | Nhóm | Màn hình | Đường dẫn
    ('1', 'Tài chính', 'Phiếu hủy hàng giữ (cửa sổ chọn phiếu yêu cầu đang Chờ duyệt để lập phiếu hủy; cột Phiếu yêu '
     'cầu, Người yêu cầu ở danh sách và ô Phiếu yêu cầu hủy hàng giữ ở màn chi tiết đọc từ phiếu yêu cầu)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Giữ hàng'),
    ('2', 'Danh mục', 'Hàng hoá, vật tư (xóa hàng hóa: chặn khi hàng đã có trên phiếu yêu cầu hủy hàng giữ)',
     'Danh mục -> Hàng hoá -> Hàng hoá, vật tư'),
]
PART5_INTRO = ('Các màn hình dưới đây đọc dữ liệu do màn Yêu cầu hủy hàng giữ ghi ra (phiếu yêu cầu và dòng hàng '
               'của phiếu).')


# ============================================================== XỬ LÝ
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)
    normalize_subheadings(doc)

    n = replace_in_texts(doc.element.body, OLD_MENU, MENU.rsplit('=> ', 1)[0] + '=> ')
    log('Đổi đường dẫn menu: %d chỗ' % n)

    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    drop_pars(doc, DROP_PARS)
    remove_in_danh_sach(doc)
    apply_menu_lines(doc, MENU_LINES)
    patch_sections(doc, rid)
    patch_part2(doc)
    patch_part4(doc)
    add_part5(doc, PART5, PART5_INTRO)
    replace_images(doc, IMAGES, SHOTS)

    for rx in NO_UC:
        remove_usecase(doc, section(doc, rx))
    redraw_usecases(doc, USECASES, UML, tpl_rx=r'^2\.8 ')
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


def remove_in_danh_sach(doc):
    """Redmine #11149: nút In danh sách đã gỡ -> FR-11 chỉ còn In phiếu."""
    h, _ = section(doc, r'^2\.11 ')
    set_runs_text(h, '2.11 In phiếu')
    sec = section(doc, r'^2\.11 ')
    p = sec_par(sec, r'^Menu: .*In danh sách')
    blk = [p.getprevious(), p, p.getnext(), p.getnext().getnext()]
    assert txt(blk[0]).startswith('Đường dẫn') and txt(blk[3]).startswith('Hình '), 'khối In danh sách lạ'
    for x in blk:
        x.getparent().remove(x)
    log('Bỏ khối Layout + Hình "Bản in danh sách" (Redmine #11149)')
    sec = section(doc, r'^2\.11 ')
    kv = sec_kv(sec)
    kv_set(kv, 'Tên chức năng', 'In phiếu yêu cầu hủy hàng giữ')
    kv_set(kv, 'Mô tả', 'Mở cửa sổ xem trước bản in của một phiếu rồi gửi lệnh in. Màn danh sách không có chức năng '
                        'in cả danh sách (đã gỡ theo yêu cầu nghiệp vụ, Redmine #11149).')
    kv_set(kv, 'Dòng sự kiện chính',
           '1. Người dùng bấm nút In ở cột Hành động hoặc nút In ở màn chi tiết.\n'
           '2. Hệ thống dựng bản in và mở cửa sổ Xem trước bản in ngay trên màn hình đang đứng (không mở tab mới).\n'
           '3. Người dùng bấm In trên cửa sổ xem trước để gửi lệnh in.')
    kv_set(kv, 'Dòng sự kiện phụ',
           '• Bản in phiếu dùng khổ A4 dọc.\n'
           '• Bấm (x) → đóng cửa sổ xem trước, không in.')
    kv_set(kv, 'Yêu cầu đặc biệt', 'Phần đầu bản in lấy theo công ty ghi trên phiếu, không lấy theo người đang in.')
    ui = sec_ui(sec)
    delete_row(ui, r'^Bản in danh sách')
    ui_set(ui, r'^Nút In trên bản xem trước', {'Mô tả': 'Nằm trên tiêu đề cửa sổ xem trước, cạnh tên bản in.'})
    ev = sec_ev(sec)
    delete_row(ev, r'^Mở bản in danh sách')
    write_cell(cells(find_row(ev, 1, r'^Bấm nút In'))[3],
               ['After:', '– Mở cửa sổ Xem trước bản in của đúng phiếu đó ngay trên màn hình đang đứng.'])
    clone_row_after(ev, r'^Bấm nút In', [None, 'Bấm In trên cửa sổ xem trước', 'Click',
                                         ['After:', '– Gửi lệnh in của trình duyệt.']])


def patch_sections(doc, rid):
    # 2.1 Xem danh sách
    s = section(doc, r'^2\.1 ')
    kv_edit(sec_kv(s), 'Dòng sự kiện chính', r'^1\. Người dùng vào menu', '1. Người dùng vào menu %s.' % MENU)
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'Không có phiếu nào trong phạm vi',
            '• Không có phiếu nào trong phạm vi → bảng hiện dòng “Không có dữ liệu phù hợp bộ lọc.”.')
    ui = sec_ui(s)
    ui_set(ui, r'^Cột Trạng thái$', {'Loại': 'Table/Grid'})
    ui_set(ui, r'^Nút In / Lịch sử$', {'Mô tả': 'In mở cửa sổ Xem trước bản in của phiếu; Lịch sử mở cửa sổ lịch sử '
                                               'thay đổi của phiếu.'})
    ui_set(ui, r'^Trạng thái rỗng$', {'Mô tả': 'Hiện dòng “Không có dữ liệu phù hợp bộ lọc.” khi không có phiếu nào khớp.'})
    delete_row(ui, r'^Vòng quay chờ')

    # 2.2 Tìm kiếm: ô Ngày tạo nay là MỘT ô khoảng ngày
    s = section(doc, r'^2\.2 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Ngày tạo từ / Ngày tạo đến$', {
        'Tên đối tượng': 'Ngày tạo', 'Phạm vi': 'dd/mm/yyyy → dd/mm/yyyy',
        'Mô tả': 'Một ô chọn khoảng ngày (từ ngày → đến ngày), lọc theo ngày tạo phiếu.'})
    ui_set(ui, r'^Ô tìm nhanh$', {'Mô tả': 'Gợi ý “Tìm theo mã phiếu...”. Chỉ tìm khi bấm nút Tìm kiếm hoặc nhấn Enter.'})
    kv_edit(sec_kv(s), 'Mô tả', r'.', 'Thu hẹp danh sách theo mã phiếu, trạng thái, người tạo, người duyệt, tên / mã '
            'hàng hóa, khoảng ngày tạo và khối công ty – phòng ban.')

    # 2.3 Cài đặt bộ lọc
    s = section(doc, r'^2\.3 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Danh sách ô lọc$', {'Phạm vi': '8 mục'})
    ui_set(ui, r'^Ô tích từng mục$', {'Loại': 'Checkbox'})
    clone_row_after(sec_ev(s), r'^Bấm Lưu$', [None, 'Kéo biểu tượng ⠿ của một ô lọc', 'Drag',
                                             ['After:', '– Đổi vị trí ô lọc trong danh sách; chưa ghi cho tới khi bấm Lưu.']])

    # 2.4 Tùy chỉnh cột
    s = section(doc, r'^2\.4 ')
    h, _ = s
    set_runs_text(h, '2.4 Tùy chỉnh cột hiển thị')

    # 2.5 Tạo mới
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    kv_set(kv, 'Dòng sự kiện chính',
           '1. Người dùng bấm nút Tạo mới ở màn danh sách.\n'
           '2. Hệ thống mở màn Thêm yêu cầu hủy hàng giữ và nạp danh sách khách hàng mà người lập đang giữ hàng.\n'
           '3. Người dùng chọn Khách hàng, nhập Ghi chú (không bắt buộc).\n'
           '4. Người dùng bấm Thêm hàng hóa, tích các hàng đang giữ cho khách đó rồi bấm Chọn.\n'
           '5. Người dùng nhập số Yêu cầu hủy cho từng dòng.\n'
           '6. Người dùng bấm Lưu nháp, Lưu và tiếp tục, hoặc Lưu và gửi duyệt (xác nhận ở hộp “Xác nhận lưu và '
           'gửi duyệt”).\n'
           '7. Hệ thống kiểm tra dữ liệu, sinh mã phiếu và lưu phiếu (Lưu nháp / Lưu và tiếp tục: trạng thái Đang '
           'tạo; Lưu và gửi duyệt: trạng thái Chờ duyệt, gửi thông báo cho người có quyền Quản lý giữ hàng).\n'
           '8. Ghi nhận hành động Tạo mới (kèm Gửi duyệt nếu bấm Lưu và gửi duyệt) trong lịch sử của phiếu.\n'
           '9. Hệ thống hiển thị thông báo thành công và quay về màn danh sách (Lưu và tiếp tục: mở lại màn Tạo mới '
           'trống).')
    kv_set(kv, 'Dòng sự kiện phụ',
           '• Người lập không giữ hàng cho khách nào → ô Khách hàng rỗng, gợi ý “Không có khách hàng đang giữ hàng”, '
           'chưa lập được phiếu.\n'
           '• Chưa chọn Khách hàng → nút Thêm hàng hóa bị khóa, rê chuột thấy chú thích “Chọn khách hàng trước khi thêm '
           'hàng hóa”.\n'
           '• Đổi Khách hàng → các dòng hàng đã chọn bị xóa hết (hàng giữ tính theo từng khách).\n'
           '• Lưu nháp KHÔNG bắt buộc phải có dòng hàng; Lưu và gửi duyệt thì bắt buộc ít nhất một dòng có số lượng '
           'lớn hơn 0.\n'
           '• Số lượng vượt phần có thể hủy → báo lỗi tại dòng, không lưu.\n' + UNSAVED)
    ui = sec_ui(s)
    ui_set(ui, r'^Khách hàng$', {'Mô tả': 'Có biểu tượng ⓘ cạnh nhãn giải thích danh sách chỉ gồm khách đang có hàng '
                                         'giữ của người lập. Khóa lại ở màn Sửa.'})
    ui_set(ui, r'^Ghi chú$', {'Loại': 'Textarea', 'Phạm vi': '0–255 ký tự'})
    ui_set(ui, r'^Nút Thêm hàng hóa$', {'Mô tả': 'Chỉ bấm được khi đã chọn Khách hàng; khi khóa, rê chuột thấy chú '
                                                 'thích nhắc chọn khách hàng trước.'})
    ui_set(ui, r'^Popup Hàng đang giữ', {
        'Loại': 'Table/Grid',
        'Mô tả': 'Cửa sổ có hai ô tìm Mã hàng hóa, Tên hàng hóa, nút Tìm kiếm, Làm mới; bảng Hàng đang giữ (Mã hàng '
                 'hóa, Tên hàng hóa, Model, Thương hiệu, ĐVT, Đang giữ) có ô tích từng dòng, phân trang; nút Chọn '
                 '(kèm số dòng đã tích) và nút Đóng.'})
    ui_set(ui, r'^Cột Cần hủy$', {'Loại': 'Checkbox'})
    ui_set(ui, r'^Cột Yêu cầu hủy$', {'Loại': 'Textbox', 'Phạm vi': '> 0 và ≤ Có thể hủy, tối đa 6 chữ số, 2 số lẻ'})
    ui_set(ui, r'^Thông báo lỗi tại ô$', {'Loại': 'Label'})
    ui_set(ui, r'^Nút Lưu và gửi duyệt$', {'Mô tả': 'Hỏi xác nhận “Bạn đồng ý lưu và duyệt?” (Xác nhận / Hủy) rồi lưu '
                                                    'phiếu và chuyển sang trạng thái Chờ duyệt.'})
    ui_set(ui, r'^Nút Quay lại$', {'Mô tả': 'Về màn danh sách; hỏi xác nhận nếu có thay đổi chưa lưu.'})
    ev = sec_ev(s)
    ev_set(ev, r'^Chọn Khách hàng$', ['After:', '– Mở khóa nút Thêm hàng hóa.',
                                      '– Xóa hết các dòng hàng đã chọn của khách cũ (nếu có).'])
    ev_set(ev, r'^Bấm Thêm hàng hóa$', [
        'Before:', '– Phải đã chọn Khách hàng.', 'During:',
        '– Cửa sổ “Hàng đang giữ cho khách hàng” liệt kê hàng mà chính người lập đang giữ cho khách hàng đã chọn; '
        'hàng đã có trong phiếu không tích được.',
        'After:', '– Bấm Chọn: các dòng được tích được thêm vào bảng Chi tiết với ô Cần hủy tích sẵn, số Yêu cầu hủy '
        'điền sẵn bằng số đang giữ.', '– Bấm Đóng / (x): đóng cửa sổ, không thêm dòng nào.'])
    tr = find_row(ev, 1, r'^Nhập Số lượng yêu cầu hủy')
    write_cell(cells(tr)[2], ['Change'])
    write_cell(cells(tr)[3], [
        'During:', '– Chỉ nhận ký tự số, tối đa 2 số lẻ.', '– Bỏ trống → “Yêu cầu hủy – Chưa nhập số lượng”.',
        '– Bằng 0 → “Yêu cầu hủy – Phải lớn hơn 0”.',
        '– Vượt số Có thể hủy → “Yêu cầu hủy – Không được vượt <số> (số đang giữ)” tại dòng.',
        'After:', '– Giữ nguyên giá trị người dùng đã gõ, không tự kéo về mức trần.'])
    ev_set(ev, r'^Bấm Lưu nháp$', [
        'During:', '– Khách hàng trống → báo lỗi bắt buộc ngay dưới ô.',
        '– Dòng đang tích có số lượng sai → báo đỏ tại dòng kèm thông báo “Bạn chưa nhập đầy đủ thông tin.”.',
        '– KHÔNG bắt buộc có dòng hàng.',
        'After:', '– Sinh mã phiếu dạng PYCHHG-NNNNN, ghi phiếu ở trạng thái Đang tạo.',
        '– Ghi nhận hành động Tạo mới trong lịch sử của phiếu.',
        '– Hiển thị thông báo lưu thành công và quay về màn danh sách.'])
    add_err_line(ev, r'^Bấm Lưu nháp$', rid)
    ev_set(ev, r'^Bấm Lưu và gửi duyệt$', [
        'Before:', '– Hiện hộp “Xác nhận lưu và gửi duyệt”; bấm Hủy thì đóng hộp, không lưu.',
        'During:', '– Bắt buộc có ít nhất một dòng hàng được tích với số lượng lớn hơn 0, nếu không hiển thị “Phải chọn '
        'ít nhất 1 hàng hoá cần hủy với số lượng lớn hơn 0”.',
        '– Kiểm tra tồn hàng giữ còn đủ; thiếu thì hiển thị thông báo nêu rõ tên hàng không đủ số lượng đang giữ.',
        'After:', '– Ghi phiếu ở trạng thái Chờ duyệt.',
        '– Ghi nhận hành động Tạo mới và Gửi duyệt trong lịch sử của phiếu.',
        '– Gửi thông báo cho những người có quyền Quản lý giữ hàng.',
        '– Hiển thị thông báo thành công và quay về màn danh sách.'])
    add_err_line(ev, r'^Bấm Lưu và gửi duyệt$', rid)
    clone_row_after(ev, r'^Bấm Lưu và gửi duyệt$', [None, 'Bấm Lưu và tiếp tục', 'Click', [
        'After:', '– Lưu nháp giống nút Lưu nháp (cùng kiểm tra, cùng ghi lịch sử).',
        '– Lưu xong mở lại màn Tạo mới trống để lập phiếu kế tiếp.']])
    clone_row_after(ev, r'^Bấm Lưu và tiếp tục$', [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt',
                                                    'Click', UNSAVED_EV])

    # 2.6 Chỉnh sửa
    s = section(doc, r'^2\.6 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống kiểm tra dữ liệu và cập nhật phiếu (Lưu và gửi duyệt: hỏi xác nhận, chuyển sang Chờ duyệt và gửi '
        'thông báo cho người có quyền Quản lý giữ hàng).',
        '6. Ghi nhận các thay đổi (kèm Gửi duyệt nếu bấm Lưu và gửi duyệt) trong lịch sử của phiếu.'])
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. Hệ thống hiển thị', '7. Hệ thống hiển thị thông báo thành công và quay về '
            'màn danh sách.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu của người khác',
            '• Phiếu của người khác hoặc không còn ở trạng thái Đang tạo → nút Sửa không hiển thị; nếu vẫn gửi lưu thì '
            'hệ thống từ chối.')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [UNSAVED])
    ui = sec_ui(s)
    ui_set(ui, r'^Ghi chú$', {'Loại': 'Textarea'})
    ev = sec_ev(s)
    ev_set(ev, r'^Mở màn Sửa$', [
        'Before:', '– Nút Sửa chỉ hiện với phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.',
        'After:', '– Nạp dữ liệu phiếu; giữ nguyên khách hàng đã chọn kể cả khi khách đó không còn hàng giữ nào.'])
    ev_set(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$', [
        'Before:', '– Lưu và gửi duyệt: hiện hộp “Xác nhận lưu và gửi duyệt”.',
        'During:', '– Kiểm tra dữ liệu giống chức năng Tạo mới; kiểm tra lại người lập và trạng thái Đang tạo.',
        'After:', '– Cập nhật phiếu; Lưu và gửi duyệt thì chuyển sang Chờ duyệt và thông báo cho người có quyền Quản lý '
        'giữ hàng.', '– Ghi nhận hành động Chỉnh sửa (nêu rõ giá trị thay đổi), kèm Gửi duyệt, trong lịch sử của phiếu.',
        '– Hiển thị thông báo thành công và quay về màn danh sách.'])
    add_err_line(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # 2.7 Xem chi tiết
    s = section(doc, r'^2\.7 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Ô Phiếu hủy hàng giữ$', {'Loại': 'Label'})

    # 2.8 Duyệt = lập Phiếu hủy hàng giữ
    s = section(doc, r'^2\.8 ')
    p = sec_par(s, r'^Màn lập Phiếu hủy hàng giữ thuộc màn hình')
    set_runs_text(p, 'Màn lập Phiếu hủy hàng giữ thuộc màn hình Phiếu hủy hàng giữ, được mở từ đường dẫn ở trên. Modal '
                     'Xác nhận duyệt được mở ngay trên màn hình lập Phiếu hủy hàng giữ khi bấm Duyệt.')
    kv = sec_kv(s)
    kv_set(kv, 'Dòng sự kiện chính',
           '1. Người duyệt bấm biểu tượng Duyệt ở cột Hành động, hoặc mở chi tiết phiếu và bấm nút Tạo phiếu hủy hàng '
           'giữ.\n'
           '2. Hệ thống mở màn Lập phiếu hủy hàng giữ, điền sẵn phiếu yêu cầu, người yêu cầu, phòng ban, khách hàng và '
           'các dòng hàng (Duyệt hủy điền sẵn bằng số Yêu cầu hủy).\n'
           '3. Người duyệt xem lại, điều chỉnh số Duyệt hủy hoặc bỏ tích Cần hủy ở dòng không đồng ý.\n'
           '4. Người duyệt bấm Duyệt và xác nhận ở hộp “Xác nhận duyệt”.\n'
           '5. Hệ thống kiểm tra tồn, lưu Phiếu hủy hàng giữ, trừ tồn hàng giữ và chuyển phiếu yêu cầu sang Đã duyệt.\n'
           '6. Ghi nhận hành động Duyệt (kèm mã phiếu hủy) trong lịch sử của phiếu yêu cầu, Tạo mới trong lịch sử của '
           'phiếu hủy, và gửi thông báo cho người lập phiếu yêu cầu.\n'
           '7. Hệ thống báo duyệt thành công và quay về màn danh sách Phiếu hủy hàng giữ.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Dòng có số lượng bằng 0',
            '• Dòng bỏ tích Cần hủy → không đưa vào phiếu hủy, không trừ tồn.')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Bấm Hủy ở hộp Xác nhận duyệt → đóng hộp, giữ nguyên dữ liệu đang nhập, chưa trừ tồn.',
        '• Bấm Quay lại khi chưa duyệt → về danh sách phiếu yêu cầu; đã sửa số liệu thì hỏi xác nhận thoát.'])
    ui = sec_ui(s)
    ui_set(ui, r'^Biểu tượng duyệt ở cột Hành động$', {'Tên đối tượng': 'Biểu tượng Duyệt ở cột Hành động'})
    ui_set(ui, r'^Cột Duyệt hủy trên màn lập phiếu hủy$', {
        'Loại': 'Textbox', 'Phạm vi': '> 0 và ≤ Có thể hủy (không bị chặn bởi số Yêu cầu hủy)'})
    ev = sec_ev(s)
    tr = find_row(ev, 1, r'^Lưu Phiếu hủy hàng giữ$')
    write_cell(cells(tr)[1], ['Bấm Duyệt trên màn lập phiếu hủy và xác nhận'])
    write_cell(cells(tr)[3], [
        'Before:', '– Hiện hộp “Xác nhận duyệt”: “Lập phiếu hủy sẽ TRỪ TỒN HÀNG GIỮ ngay lập tức và không thể hoàn tác. '
        'Bạn có chắc chắn không?” (Duyệt / Hủy).', '– Kiểm tra lại quyền và trạng thái phiếu yêu cầu.',
        'During:', '– Không dòng nào có số lượng lớn hơn 0 → hiển thị “Phải chọn ít nhất 1 hàng hoá cần hủy với số '
        'lượng lớn hơn 0”.', '– Hàng không nằm trong phiếu yêu cầu → hiển thị thông báo từ chối.',
        '– Tồn hàng giữ không đủ → hiển thị lỗi và hủy toàn bộ thao tác.',
        'After:', '– Ghi Phiếu hủy hàng giữ với mã dạng PHHG-NNNNN.',
        '– Trừ tồn hàng giữ theo thứ tự hạn giữ sớm trước, ghi nhật ký biến động tồn hàng giữ.',
        '– Chuyển phiếu yêu cầu sang trạng thái Đã duyệt, ghi người duyệt và thời điểm duyệt.',
        '– Ghi nhận hành động Duyệt trong lịch sử phiếu yêu cầu; gửi thông báo cho người lập phiếu yêu cầu.',
        '– Hiển thị thông báo thành công và quay về màn danh sách Phiếu hủy hàng giữ.'])
    add_err_line(ev, r'^Bấm Duyệt trên màn lập phiếu hủy', rid)

    # 2.9 Không duyệt
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', '4. Người duyệt bấm nút Xác nhận không duyệt.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống đưa phiếu về trạng thái Đang tạo và lưu lý do.',
        '6. Ghi nhận hành động Không duyệt kèm lý do trong lịch sử của phiếu và gửi thông báo cho người lập.',
        '7. Hệ thống báo thành công và quay về màn danh sách.'])
    kv_set(kv, 'Dòng sự kiện phụ',
           '• Bỏ trống lý do → báo “Bắt buộc phải nhập lý do không duyệt”, cửa sổ không đóng.\n'
           '• Ô Lý do giới hạn 255 ký tự, không gõ thêm được quá giới hạn.\n'
           '• Phiếu đã được xử lý trước đó → báo phiếu không ở trạng thái chờ duyệt.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận kể cả khi đã nhập lý do; '
           'phiếu giữ nguyên.')
    ui = sec_ui(s)
    ui_set(ui, r'^Lý do không duyệt$', {'Phạm vi': '1–255 ký tự'})
    ui_set(ui, r'^Nút xác nhận$', {'Tên đối tượng': 'Nút Xác nhận không duyệt'})
    ui_set(ui, r'^Nút đóng cửa sổ$', {'Tên đối tượng': 'Nút Đóng', 'Mô tả': 'Đóng cửa sổ, bỏ nội dung đã nhập, '
                                                                            'không hỏi xác nhận.'})
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm xác nhận không duyệt$', r'quá 255 ký tự', None)
    ev_edit(ev, r'^Bấm xác nhận không duyệt$', r'^– Ghi một dòng lịch sử',
            '– Ghi nhận hành động Không duyệt kèm lý do trong lịch sử của phiếu; gửi thông báo cho người lập phiếu.')
    write_cell(cells(find_row(ev, 1, r'^Bấm xác nhận không duyệt$'))[1], ['Bấm Xác nhận không duyệt'])
    add_err_line(ev, r'^Bấm Xác nhận không duyệt$', rid)

    # 2.10 Xóa
    s = section(doc, r'^2\.10 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', '4. Hệ thống xóa phiếu, thông báo “Xóa thành công.” và hiển thị màn danh '
            'sách (xóa từ màn chi tiết thì quay về màn danh sách).')
    ev = sec_ev(s)
    ev_set(ev, r'^Xác nhận Xóa$', ['After:', '– Xóa phiếu cùng các dòng hàng của phiếu.',
                                   '– Hiển thị thông báo “Xóa thành công.” và nạp lại / quay về màn danh sách.'])
    add_err_line(ev, r'^Xác nhận Xóa$', rid)

    # 2.12 Xuất Excel
    s = section(doc, r'^2\.12 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. ', '2. Hệ thống mở cửa sổ Chọn trường xuất Excel với 12 trường, mặc định '
            'tích hết.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ', '3. Người dùng bỏ tích trường không cần, kéo biểu tượng ☰ để đổi thứ tự cột.')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Kết quả lọc rỗng → vẫn xuất tệp gồm tiêu đề và dòng tên cột, không có dòng dữ liệu.'])
    ui = sec_ui(s)
    ui_set(ui, r'^Ô chọn trường xuất$', {
        'Tên đối tượng': 'Danh sách trường xuất', 'Loại': 'Checkbox',
        'Mô tả': 'Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, '
                 'Khách hàng, Phòng ban, Ghi chú, Lý do không duyệt. Kéo biểu tượng ☰ để đổi thứ tự cột trong tệp.'})
    ui_set(ui, r'^Dòng xem trước thứ tự cột$', {
        'Tên đối tượng': 'Số trường đang chọn', 'Giá trị ban đầu': 'Đang chọn 12/12 trường',
        'Mô tả': 'Góc trái cuối cửa sổ, cập nhật ngay khi tích / bỏ tích hoặc bấm Chọn tất cả / Bỏ chọn hết.'})
    ev_set(sec_ev(s), r'^Bấm Xuất file$', [
        'During:', '– Lấy dữ liệu theo đúng bộ lọc và phạm vi quyền hiện tại.',
        'After:', '– Dựng tệp Excel với đúng những trường đã tích, theo đúng thứ tự trong danh sách, tải về máy.',
        '– Hiển thị thông báo “Xuất Excel thành công” và đóng cửa sổ.'])

    # 2.13 Lịch sử
    s = section(doc, r'^2\.13 ')
    kv = sec_kv(s)
    kv_set(kv, 'Mô tả', 'Hiển thị các mốc thao tác đã diễn ra trên phiếu: tạo mới, chỉnh sửa, gửi duyệt, duyệt (kèm mã '
                        'phiếu hủy đã lập) và không duyệt (kèm lý do), cùng người thực hiện, thời điểm và giá trị thay đổi.')
    kv_set(kv, 'Dòng sự kiện chính',
           '1. Người dùng bấm biểu tượng Lịch sử ở cột Hành động (mở cửa sổ Lịch sử yêu cầu hủy hàng giữ), hoặc bấm '
           'Xem lịch sử ở khối Lịch sử thay đổi trong màn chi tiết.\n'
           '2. Hệ thống nạp danh sách mốc thay đổi của phiếu.\n'
           '3. Danh sách hiển thị theo thứ tự mới nhất trước.')
    kv_set(kv, 'Dòng sự kiện phụ',
           '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → cửa sổ hiện “Chưa có lịch sử thay '
           'đổi.”, khối ở màn chi tiết hiện “Chưa có lịch sử thao tác nào.”.\n'
           '• Bấm Làm mới (khối ở màn chi tiết) → nạp lại danh sách.\n'
           '• Bấm Đóng / (x) → đóng cửa sổ lịch sử.')
    ui = sec_ui(s)
    ui_set(ui, r'^Trạng thái rỗng$', {'Mô tả': 'Hiện “Chưa có lịch sử thay đổi.” (cửa sổ) / “Chưa có lịch sử thao tác '
                                                'nào.” (khối ở màn chi tiết) với phiếu chưa có thao tác nào trên hệ '
                                                'thống mới.'})


def patch_part2(doc):
    t = table_by_header(doc, 'Chức năng')
    tr = find_row(t, 0, r'^FR-11 ')
    write_cell(cells(tr)[0], ['FR-11 In phiếu'])
    log('Ma trận quyền: FR-11 chỉ còn In phiếu')


def patch_part4(doc):
    tbl = part4_intro(doc, SCREEN)
    br_desc(tbl, 'BR-04', r'^– Nhập sai thì hệ thống báo đỏ', None)
    br_desc(tbl, 'BR-09', r'^– Nút không dùng được thì ẩn hẳn', None)
    clone_row_after(tbl, r'^BR-11$', [None, 'BR-12', 'Màn hình trở về sau thao tác', [
        '– Lưu nháp, Lưu và gửi duyệt, Không duyệt, Xóa (ở màn chi tiết) xong → quay về màn danh sách phiếu yêu cầu.',
        '– Lưu và tiếp tục xong → mở lại màn Tạo mới trống.',
        '– Duyệt (lập Phiếu hủy hàng giữ) xong → về màn danh sách Phiếu hủy hàng giữ; bấm Quay lại khi chưa duyệt → về '
        'màn danh sách phiếu yêu cầu.'], 'Tạo mới / Chỉnh sửa / Duyệt / Không duyệt / Xóa'])
    check_br(tbl)


if __name__ == '__main__':
    main()
