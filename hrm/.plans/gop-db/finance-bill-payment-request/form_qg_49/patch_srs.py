# -*- coding: utf-8 -*-
"""Vá SRS "Phiếu đề nghị thanh toán" (bản Drive tải 28/10) theo FORM "Danh mục quốc gia" (TPE Pass).

    python patch_srs.py            # drive_0710/SRS_Drive.docx -> out/SRS - Phiếu đề nghị thanh toán.docx (+ PDF)
    python patch_srs.py --no-word  # bỏ bước Word (mục lục / số trang / PDF)

Khuôn chép từ màn 27 (finance-product-import-direct-transfer/form_qg/patch_srs.py). Luôn đọc bản Drive gốc.
Khác màn 27: dòng đường dẫn menu của bản Drive có ICON chèn giữa chữ (người khác làm tay) → KHÔNG ghi đè dòng,
chỉ chèn thêm cấp menu còn thiếu (chữ + icon chụp từ dev) vào đúng chỗ.
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
NAME = 'SRS - Phiếu đề nghị thanh toán'
OUT = os.path.join(OUT_DIR, NAME + '.docx')
UML = os.path.join(HERE, 'uml')
ICONS = os.path.join(HERE, 'hdsd_shots', 'icons')
DRAWING = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing'

# ============================================================== DỮ LIỆU MÀN
SCREEN = 'Phiếu đề nghị thanh toán'
TAIL = ' Chỉ bổ sung quy tắc riêng của %s.' % SCREEN
# finance.js: hubGroup 'Khởi tạo' > 'Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi' > 'Đề nghị thanh toán'
#             hubGroup 'Quản lý tiền' > 'Đề nghị' > 'Đề nghị thanh toán'
#             hubGroup 'Chờ duyệt' > 'Phê duyệt - Công nợ - Thu - Chi' > 'Phiếu đề nghị thanh toán chờ duyệt' (?mode=pending)
G_KT = 'Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi'
G_QLT = 'Đề nghị'
G_CD = 'Phê duyệt - Công nợ - Thu - Chi'
MENU_ALL = 'Phân hệ Tài chính => Khởi tạo => %s => Đề nghị thanh toán' % G_KT
MENU_ALL2 = 'Phân hệ Tài chính => Quản lý tiền => %s => Đề nghị thanh toán' % G_QLT
MENU_PD = 'Phân hệ Tài chính => Chờ duyệt => %s => Phiếu đề nghị thanh toán chờ duyệt' % G_CD

UNSAVED = ('• Bấm Quay lại / chọn menu khác / đóng tab trình duyệt: nếu chưa nhập hoặc thay đổi gì thì rời màn '
           'ngay; nếu đã nhập dữ liệu thì hiện hộp xác nhận “Thông tin chưa lưu” với nội dung “Bạn có thông tin chưa '
           'lưu. Có chắc chắn muốn thoát?” (Thoát / Ở lại).')
UNSAVED_EV = ['After:', '– Chưa nhập hoặc thay đổi gì → rời màn ngay.',
              '– Đã nhập dữ liệu → hiện hộp xác nhận “Thông tin chưa lưu”; bấm Thoát thì rời màn và bỏ thay đổi, '
              'bấm Ở lại thì giữ nguyên màn.']
DUE = ('• Thao tác “Duyệt đề nghị thanh toán” được khai chặn hàng quá hạn (Khai Quy chế – Cấu hình) mà nhân viên '
       'thuộc phòng ban người dùng quản lý còn hàng quá hạn → hệ thống chặn thao tác, hiện thông báo lý do; tài '
       'khoản Super admin không bị chặn.')

ACTOR_LIST = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình (màn không gắn quyền truy '
              'cập riêng). Chế độ Tất cả: phạm vi phiếu theo quyền Xem tất cả phiếu đề nghị thanh toán của tổng công '
              'ty / công ty / phòng ban / bộ phận (V1–V4), không có quyền nào thì chỉ thấy phiếu của mình. Chế độ '
              'Chờ duyệt: người có quyền duyệt Q2–Q5 hoặc quyền Kế toán thanh toán (Q6).')
COND_LIST = ('1. Đăng nhập thành công.\n'
             '2. Có quyền xem theo Phần 2 (V1–V4; Q2–Q6 với chế độ Chờ duyệt); không có quyền nào vẫn xem được phiếu '
             'do chính mình tạo.')
ACTOR_FORM = ('Người tạo phiếu — người dùng đang tạo hoặc sửa phiếu của chính mình (chức năng không gắn quyền '
              'riêng).')
COND_FORM = '1. Đăng nhập thành công.\n2. Là người tạo phiếu (chức năng không gắn quyền riêng).\n3. Đang ở màn Tạo mới hoặc Chỉnh sửa phiếu'
ACTOR_OWNER = 'Người tạo phiếu — người dùng có quyền thực hiện chức năng: chỉ người đã tạo phiếu (chức năng không gắn quyền riêng).'
COND_OWNER = ('1. Đăng nhập thành công.\n2. Là người tạo phiếu (chức năng không gắn quyền riêng).\n'
              '3. Phiếu đang ở trạng thái Đang tạo hoặc Không duyệt.')
ACTOR_SCOPE = ('Người dùng có quyền xem phiếu: người tạo phiếu; người đã duyệt phiếu ở bất kỳ cấp nào; người có quyền '
               'V1–V4 trong phạm vi được giao; hoặc người có quyền duyệt / xử lý phiếu (Q2–Q6) ở đúng trạng thái hiện '
               'tại của phiếu.')
COND_SCOPE = ('1. Đăng nhập thành công.\n2. Có quyền xem phiếu như mục Tác nhân.\n'
              '3. Phiếu nằm trong phạm vi dữ liệu của người dùng; phiếu Đang tạo chỉ người tạo xem được.')
ACTOR_APPR = ('Người dùng có quyền duyệt của đúng cấp đang giữ phiếu: Trưởng phòng duyệt đề nghị thanh toán (Q2) / '
              'Kế toán công nợ duyệt đề nghị thanh toán (Q3) / Kế toán trưởng duyệt đề nghi thanh toán (Q4) / Ban '
              'giám đốc duyệt đề nghi thanh toán (Q5).')
COND_APPR = ('1. Đăng nhập thành công.\n'
             '2. Có quyền duyệt của đúng cấp đang giữ phiếu (Q2–Q5), cùng công ty với phiếu; với Q2 phiếu phải thuộc '
             'phòng ban được giao quản lý.\n'
             '3. Phiếu đang ở trạng thái Chờ TP duyệt / Chờ kế toán công nợ duyệt / Chờ kế toán trưởng duyệt / Chờ '
             'ban giám đốc duyệt tương ứng.')

SECTIONS = {
    r'^2\.1 Xem danh sách': ('Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', ACTOR_LIST, COND_LIST),
    r'^2\.2 Tìm kiếm': ('Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang.', ACTOR_LIST,
                        COND_LIST + '\n3. Đang ở màn danh sách phiếu (bất kỳ chế độ xem nào).'),
    r'^2\.3 Cài đặt bộ lọc': ('Cấu hình bộ lọc và Tùy chỉnh cột.', ACTOR_LIST,
                              COND_LIST + '\n3. Đang ở màn danh sách phiếu.'),
    r'^2\.4 Lập phiếu': ('Màn Thêm mới, Validate dữ liệu, Thông báo, UI/UX và Quy tắc ghi lịch sử.',
                         'Người tạo phiếu — người dùng có quyền thực hiện chức năng: mọi người dùng vào được màn hình '
                         '(chức năng lập phiếu không gắn quyền riêng).',
                         '1. Đăng nhập thành công.\n'
                         '2. Vào được màn Phiếu đề nghị thanh toán (lập phiếu không gắn quyền riêng).\n'
                         '3. Đang ở màn danh sách chế độ Tất cả (chế độ Chờ duyệt không có nút Tạo mới).'),
    r'^2\.5 Chọn đối tượng': ('Popup chọn dữ liệu, Dropdown và Validate dữ liệu.', ACTOR_FORM,
                              COND_FORM + ', loại chi khác Thanh toán chi phí vận chuyển NCC.'),
    r'^2\.6 Lấy dữ liệu': ('Validate dữ liệu và Thông báo.', ACTOR_FORM,
                           COND_FORM + ', Loại chi là Thanh toán chi phí vận chuyển NCC.'),
    r'^2\.7 Nạp khối': ('Validate dữ liệu, Dropdown và Thông báo.', ACTOR_FORM,
                        COND_FORM + ', Hình thức thanh toán là CK.'),
    r'^2\.8 Quản lý file': ('Validate dữ liệu và Thông báo.', ACTOR_FORM, COND_FORM + '.'),
    r'^2\.9 Sửa phiếu': ('Màn Chỉnh sửa, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.10 Xem chi tiết': ('Màn Xem chi tiết và Phân quyền.', ACTOR_SCOPE, COND_SCOPE),
    r'^2\.11 Duyệt': ('Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.', ACTOR_APPR, COND_APPR),
    r'^2\.12 Từ chối': ('Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.', ACTOR_APPR, COND_APPR),
    r'^2\.13 Xóa': ('Quy tắc Xóa, Thông báo và Quy tắc ghi lịch sử.', ACTOR_OWNER, COND_OWNER),
    r'^2\.14 In': ('Quy tắc màn In, Quy tắc Excel và bố cục bản in.', ACTOR_SCOPE,
                   COND_SCOPE.replace('\n3.', '\n3. In / Xuất Excel từ danh sách hoặc màn chi tiết;')),
    r'^2\.15 Xem lịch sử': ('Quy tắc ghi lịch sử và hiển thị lịch sử.', ACTOR_SCOPE, COND_SCOPE),
}

# Câu popup đặt cuối khối đường dẫn (thay câu cũ nếu có)
POPUPS = {
    r'^2\.3 ': 'Modal Cài đặt bộ lọc và Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
    r'^2\.5 ': ('Modal Chọn khách hàng, Chọn nhà cung cấp và Chọn hợp đồng được mở ngay trên màn hình Tạo mới hoặc '
                'Chỉnh sửa phiếu theo đường dẫn ở trên.'),
    r'^2\.6 ': ('Modal Chi tiết chuyến xe được mở ngay trên màn hình Tạo mới, Chỉnh sửa hoặc Chi tiết phiếu theo đường '
                'dẫn ở trên.'),
    r'^2\.8 ': ('Hộp xác nhận xóa file đính kèm được mở ngay trên màn hình Tạo mới hoặc Chỉnh sửa phiếu theo đường dẫn '
                'ở trên.'),
    r'^2\.11 ': ('Modal Xác nhận duyệt và Modal Xác nhận chuyển duyệt được mở ngay trên màn hình chi tiết phiếu theo '
                 'đường dẫn ở trên.'),
    r'^2\.12 ': 'Modal Từ chối phiếu được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.',
    r'^2\.13 ': ('Modal Xác nhận xóa được mở ngay trên màn hình danh sách (mục Xóa trong nút ba chấm của dòng) hoặc '
                 'màn hình chi tiết phiếu (nút Xóa) theo đường dẫn ở trên.'),
    r'^2\.14 ': ('Cửa sổ Xem trước bản in được mở ngay trên màn hình danh sách hoặc màn hình chi tiết phiếu theo đường '
                 'dẫn ở trên; Xuất Excel tải tệp về máy, không mở cửa sổ.'),
    r'^2\.15 ': ('Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên; khối Lịch sử nằm '
                 'cuối màn hình chi tiết phiếu.'),
}

USECASES = {
    r'^2\.4 ': ('Người tạo phiếu', 'FR-04', 'Lập phiếu đề nghị thanh toán', 'crud'),
    r'^2\.5 ': ('Người tạo phiếu', 'FR-05', 'Chọn đối tượng và hợp đồng', 'crud'),
    r'^2\.6 ': ('Người tạo phiếu', 'FR-06', 'Lấy dữ liệu chuyến xe', 'crud'),
    r'^2\.7 ': ('Người tạo phiếu', 'FR-07', 'Nạp thông tin ngân hàng', 'crud'),
    r'^2\.8 ': ('Người tạo phiếu', 'FR-08', 'Quản lý file đính kèm', 'io'),
    r'^2\.9 ': ('Người tạo phiếu', 'FR-09', 'Sửa phiếu', 'crud'),
    r'^2\.10 ': ('Người dùng có quyền', 'FR-10', 'Xem chi tiết phiếu', 'view'),
    r'^2\.11 ': ('Cấp duyệt', 'FR-11', 'Duyệt phiếu theo cấp', 'action'),
    r'^2\.12 ': ('Cấp duyệt', 'FR-12', 'Từ chối phiếu', 'action'),
    r'^2\.13 ': ('Người tạo phiếu', 'FR-13', 'Xóa phiếu', 'action'),
    r'^2\.14 ': ('Người dùng có quyền', 'FR-14', 'In phiếu và xuất Excel', 'io'),
}

PART5 = [  # STT | Nhóm | Màn hình | Đường dẫn
    ('1', 'Tài chính', 'Phiếu chi (lập phiếu chi từ phiếu đề nghị hình thức tiền mặt ở trạng thái Chờ tạo phiếu chi; '
     'gửi duyệt / duyệt / hủy phiếu chi thì đổi trạng thái phiếu đề nghị sang Chờ duyệt phiếu chi / Duyệt phiếu chi / '
     'Đã hủy; số tiền thực chi hiện ở cột Số tiền chi)',
     'Tài chính -> Quản lý tiền -> Thanh toán tiền mặt -> Phiếu chi'),
    ('2', 'Tài chính', 'Phiếu ủy nhiệm chi (lập giấy ủy nhiệm chi từ phiếu đề nghị hình thức chuyển khoản ở trạng thái '
     'Chờ tạo phiếu chi; đổi trạng thái phiếu đề nghị như Phiếu chi)',
     'Tài chính -> Quản lý tiền -> Thanh toán tiền mặt -> Phiếu ủy nhiệm chi'),
]


# ============================================================== helper dùng chung với màn 48
import importlib.util as _ilu  # noqa: E402
_spec = _ilu.spec_from_file_location('p48', os.path.join(HERE, '..', '..', 'finance-bill-income-request', 'form_qg_48',
                                                        'patch_srs.py'))
P48 = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(P48)
set_menu, fix_ui_widths, keep_image_with_caption, clean_ui = (P48.set_menu, P48.fix_ui_widths,
                                                               P48.keep_image_with_caption, P48.clean_ui)
# Cột Loại 1350 dxa vẫn bẻ "Table/Grid" thành 2 dòng ở cỡ chữ của bản Drive → nới riêng cho màn này.
P48.UI_COL_W['Loại'] = 1550
P48.UI_COL_W8['Loại'] = 1500
P48.UI_COL_W8['Tên đối tượng'] = 1250

SHOT = os.path.join(HERE, 'hdsd_shots')
# Ảnh thay bằng ảnh chụp dev 28/10 (giao diện hiện tại): số Hình CŨ của bản Drive -> file
NEW_IMAGES = {2: '01_list', 5: '02_filter', 7: '26_filtercfg', 8: '25_colcfg', 10: '10_create', 11: '13_create_ck',
              13: '30_changetype', 14: '31_confirm_send', 16: '32_unsaved', 18: '11_supplier', 21: '14_delivery',
              26: '10b_create_filled', 29: '16_edit', 30: '17b_detail_view', 32: '17_detail', 33: '18_approve',
              35: '19_reject', 37: '15_delete', 39: '21_print'}
NEW_CAPTION = {11: 'Hình thức chuyển khoản: có ô Nhà cung cấp và khối Thông tin ngân hàng (chưa chọn nhà cung cấp)',
               26: 'Khối File đính kèm với một dòng chờ chọn tệp',
               32: 'Màn chi tiết ở cấp Kế toán trưởng: có nút Duyệt, Chuyển duyệt BGĐ và Từ chối',
               39: 'Cửa sổ Xem trước phiếu đề nghị thanh toán'}


def replace_images(doc):
    its = items(doc)
    for i, e in enumerate(its):
        m = e.tag == W('p') and re.match(r'^Hình (\d+):', txt(e))
        if not m or int(m.group(1)) not in NEW_IMAGES:
            continue
        n = int(m.group(1))
        img = its[i - 1]
        assert list(img.iter(L.A_NS + 'blip')), 'Không thấy ảnh trước Hình %d' % n
        set_image(doc, img, os.path.join(SHOT, NEW_IMAGES[n] + '.png'))
        if n in NEW_CAPTION:
            set_runs_text(e, 'Hình %d: %s' % (n, NEW_CAPTION[n]))
        log('Thay ảnh Hình %d → %s' % (n, NEW_IMAGES[n]))


M1, M2, MP = MENU_ALL, MENU_ALL2, MENU_PD
TL = 'bấm ô Khách hàng (Nhà cung cấp) hoặc ô hợp đồng của dòng chi tiết'
WAIT = 'Mã phiếu (phiếu đang chờ cấp mình duyệt)'
MENU_LINES = {
    r'^2\.1 ': (['Menu: %s' % M1, 'Hoặc: %s' % M2, 'Hoặc (chế độ Chờ duyệt): %s' % MP], None),
    r'^2\.2 ': (['Menu: %s => Tìm kiếm nâng cao' % M1, 'Hoặc: %s => Tìm kiếm nâng cao' % M2], None),
    r'^2\.3 ': (['Menu: %s => Cài đặt bộ lọc / Cấu hình cột hiển thị' % M1,
                 'Hoặc: %s => Cài đặt bộ lọc / Cấu hình cột hiển thị' % M2], None),
    r'^2\.4 ': (['Menu: %s => Tạo mới' % M1, 'Hoặc: %s => Tạo mới' % M2], None),
    r'^2\.5 ': (['Menu: %s => Tạo mới / Sửa => %s' % (M1, TL), 'Hoặc: %s => Tạo mới / Sửa => %s' % (M2, TL)], None),
    r'^2\.6 ': (['Menu: %s => Tạo mới / Sửa (Loại chi Thanh toán chi phí vận chuyển NCC) => Lấy dữ liệu' % M1,
                 'Hoặc: %s => Tạo mới / Sửa (Loại chi Thanh toán chi phí vận chuyển NCC) => Lấy dữ liệu' % M2], None),
    r'^2\.7 ': (['Menu: %s => Tạo mới / Sửa (Hình thức thanh toán CK)' % M1,
                 'Hoặc: %s => Tạo mới / Sửa (Hình thức thanh toán CK)' % M2], None),
    r'^2\.8 ': (['Menu: %s => Tạo mới / Sửa => khối File đính kèm' % M1,
                 'Hoặc: %s => Tạo mới / Sửa => khối File đính kèm' % M2], None),
    r'^2\.9 ': (['Menu: %s => Sửa (trên dòng phiếu) / Mã phiếu => Sửa' % M1,
                 'Hoặc: %s => Sửa (trên dòng phiếu) / Mã phiếu => Sửa' % M2], None),
    r'^2\.10 ': (['Menu: %s => Mã phiếu' % M1, 'Hoặc: %s => Mã phiếu' % M2, 'Hoặc: %s => Mã phiếu' % MP], None),
    r'^2\.11 ': (['Menu: %s => Duyệt (trên dòng phiếu) / Mã phiếu => Duyệt / Chuyển duyệt BGĐ' % MP,
                  'Hoặc: %s => %s => Duyệt / Chuyển duyệt BGĐ' % (M1, WAIT),
                  'Hoặc: %s => %s => Duyệt / Chuyển duyệt BGĐ' % (M2, WAIT)], None),
    r'^2\.12 ': (['Menu: %s => Duyệt (trên dòng phiếu) / Mã phiếu => Từ chối' % MP,
                  'Hoặc: %s => %s => Từ chối' % (M1, WAIT), 'Hoặc: %s => %s => Từ chối' % (M2, WAIT)], None),
    r'^2\.13 ': (['Menu: %s => nút ba chấm trên dòng phiếu => Xóa / Mã phiếu => Xóa' % M1,
                  'Hoặc: %s => nút ba chấm trên dòng phiếu => Xóa / Mã phiếu => Xóa' % M2], None),
    r'^2\.14 ': (['Menu: %s => In phiếu / Xuất Excel (trên dòng phiếu) / Mã phiếu => In / Xuất Excel' % M1,
                  'Hoặc: %s => In phiếu / Xuất Excel (trên dòng phiếu) / Mã phiếu => In / Xuất Excel' % M2,
                  'Hoặc: %s => In phiếu / Xuất Excel (trên dòng phiếu)' % MP], None),
    r'^2\.15 ': (['Menu: %s => Lịch sử (trên dòng phiếu) / Mã phiếu => Xem lịch sử' % M1,
                  'Hoặc: %s => Lịch sử (trên dòng phiếu) / Mã phiếu => Xem lịch sử' % M2,
                  'Hoặc: %s => Lịch sử (trên dòng phiếu)' % MP], None),
}


# ============================================================== tiện ích ô bảng
def split_big_images(doc):
    """Bản Drive có chỗ dán ảnh màn hình chung đoạn với dòng menu (vd 2.7) → set_menu xóa dòng menu sẽ mất ảnh.
    Tách run ảnh lớn (> 3 inch) ra đoạn riêng ngay sau trước khi dựng lại đường dẫn."""
    ext = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent'
    for p in list(doc.element.body.iter(W('p'))):
        if '=>' not in txt(p):
            continue
        big = [r for r in p.findall(W('r'))
               if any(int(x.get('cx')) > 3 * L.EMU for x in r.iter(ext))]
        if not big:
            continue
        np_ = strip_ids(copy.deepcopy(p))
        for ch in list(np_):
            if ch.tag != W('pPr'):
                np_.remove(ch)
        for r in big:
            p.remove(r)
            np_.append(r)
        p.addnext(np_)
        log('Tách ảnh màn hình khỏi dòng menu: ' + txt(p)[:40])


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


def ev_cell(ev, event_regex):
    return cells(find_row(ev, 1, event_regex))[3]


def ev_edit(ev, event_regex, old_regex, new, rid=None):
    tc = ev_cell(ev, event_regex)
    write_cell(tc, lines_replace(cell_lines(tc), old_regex, new), rid)


def ui_set(ui, name_regex, col_name, value):
    """Ghi 1 ô; ô đang TRỐNG thì mượn định dạng chữ của ô tên (rPr dấu đoạn của ô trống nhỏ hơn chữ bảng)."""
    tr = find_row(ui, 1, name_regex)
    tc = cells(tr)[header_index(ui, col_name)]
    if not txt(tc).strip():
        src = cells(tr)[1].find('.//' + W('r'))
        p = tc.find(W('p'))
        if src is not None and p is not None:
            p.append(copy.deepcopy(src))
    write_cell(tc, [value])


def normalize_types(doc):
    """Cột Loại của mọi bảng Mô tả giao diện + loại event, theo checklist (bỏ Badge/Number/Modal/Loading/Text…)."""
    n = 0
    for tbl in doc.element.body.iter(W('tbl')):
        hdr = [txt(c).strip() for c in cells(rows(tbl)[0])]
        if 'Tên đối tượng' in hdr and 'Loại' in hdr:
            ci, ni = hdr.index('Loại'), hdr.index('Tên đối tượng')
            for tr in rows(tbl)[1:]:
                cs = cells(tr)
                name, typ = txt(cs[ni]).strip(), txt(cs[ci]).strip()
                new = None
                if typ == 'Badge':
                    new = 'Table/Grid'
                elif typ == 'Number':
                    new = 'Table/Grid' if name.startswith('Cột') else 'Textbox'
                elif typ == 'Loading':
                    new = 'Label'
                elif typ == 'Text':
                    new = 'Label'
                elif typ == 'Modal':
                    new = 'Checkbox' if 'tích' in name else 'Popup'
                if new:
                    write_cell(cs[ci], [new])
                    n += 1
        if 'Loại event' in hdr:
            ci = hdr.index('Loại event')
            for tr in rows(tbl)[1:]:
                c = cells(tr)[ci]
                if txt(c).strip() in ('Keypress', 'Blur'):
                    write_cell(c, ['Change'])
                    n += 1
    log('Chuẩn hóa cột Loại / loại event: %d ô' % n)


def fix_ranges(doc):
    """Phạm vi ký tự: '0255' mất dấu → '0–255'; cột chữ DB kiểu text (lý do chi, ghi chú) → không giới hạn."""
    unlimited = re.compile(r'^(Lý do chi|Cột Ghi chú của dòng|Ghi chú của <cấp đang giữ phiếu>|Lý do không duyệt)$')
    n = 0
    for tbl in doc.element.body.iter(W('tbl')):
        hdr = [txt(c).strip() for c in cells(rows(tbl)[0])]
        if 'Tên đối tượng' not in hdr or 'Phạm vi' not in hdr:
            continue
        ni, pi = hdr.index('Tên đối tượng'), hdr.index('Phạm vi')
        for tr in rows(tbl)[1:]:
            cs = cells(tr)
            v = txt(cs[pi]).strip()
            if unlimited.match(txt(cs[ni]).strip()) and 'ký tự' in v:
                write_cell(cs[pi], ['Không giới hạn số ký tự'])
                n += 1
            elif re.match(r'^0-?255 ký tự$', v):
                write_cell(cs[pi], ['0–255 ký tự'])
                n += 1
    log('Sửa phạm vi ký tự: %d ô' % n)


# ============================================================== XỬ LÝ
def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(UML, exist_ok=True)
    doc = docx.Document(SRC)
    rid = link_rid(doc)
    body = doc.element.body
    replace_images(doc)  # trước khi đánh lại số Hình
    # Đoạn trống ngay trước đoạn ngắt trang → dễ sinh trang trắng (như màn 48)
    for p in list(body.iter(W('p'))):
        if any(b.get(W('type')) == 'page' for b in p.iter(W('br'))):
            prev = p.getprevious()
            if prev is not None and prev.tag == W('p') and not txt(prev).strip() and not list(prev.iter(L.A_NS + 'blip')):
                prev.getparent().remove(prev)

    for old, new in (('V1V4', 'V1–V4'), ('ab / N', 'a–b / N')):
        log('Sửa chữ "%s" → "%s": %d chỗ' % (old, new, replace_in_texts(body, old, new)))

    for rx, (tail, actor, cond) in SECTIONS.items():
        sec = section(doc, rx)
        set_rule_tail(sec_par(sec, r'^Quy tắc (chung|áp dụng):'), ' - ' + tail + TAIL)
        kv = sec_kv(sec)
        kv_set(kv, 'Tác nhân', actor)
        kv_set(kv, 'Điều kiện ban đầu', cond)

    split_big_images(doc)
    for rx, (menu, _) in MENU_LINES.items():
        set_menu(doc, section(doc, rx), menu, POPUPS.get(rx))

    normalize_types(doc)
    fix_ranges(doc)
    for k in range(1, 16):
        try:
            ui = sec_ui(section(doc, r'^2\.%d ' % k))
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
            add_usecase(doc, sec, section(doc, r'^2\.4 '), png, 'Biểu đồ Use Case — %s %s' % (code, name))
        else:
            set_image(doc, blk[1], png)
            set_runs_text(blk[2], 'Hình 0: Biểu đồ Use Case — %s %s' % (code, name))
    renumber_subheadings(doc)
    log('Số Hình sau khi đánh lại: %d' % renumber_figures(doc))
    keep_image_with_caption(doc)

    # Đoạn chỉ chứa ngắt trang đứng trước Heading1: bảng trước nó vừa kín trang thì đoạn ngắt tràn sang trang mới
    # → trang trắng. Bỏ đoạn đó, gắn "ngắt trang trước" vào chính tiêu đề.
    for p in list(body.iter(W('p'))):
        nxt = p.getnext()
        if (not txt(p).strip() and any(b.get(W('type')) == 'page' for b in p.iter(W('br')))
                and nxt is not None and nxt.tag == W('p') and style_of(nxt) == 'Heading1'):
            p.getparent().remove(p)
            ppr = nxt.find(W('pPr'))
            if ppr.find(W('pageBreakBefore')) is None:
                ps = ppr.find(W('pStyle'))
                ps.addnext(L._el('pageBreakBefore'))
            log('Đổi ngắt trang trước: ' + txt(nxt))
    doc.save(OUT)
    print('Đã ghi', OUT)
    for m in L.LOG:
        print(' -', m)
    if '--no-word' not in sys.argv:
        word_finalize(OUT, os.path.join(OUT_DIR, NAME + '.pdf'))


def patch_sections(doc, rid):
    # ---------------- 2.1 Xem danh sách (4 chế độ theo code, menu chỉ có 2 lối vào)
    s = section(doc, r'^2\.1 ')
    set_rule_tail(sec_par(s, r'^Quy tắc chung'), ' - Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.'
                  + TAIL)
    kv = sec_kv(s)
    kv_set(kv, 'Mô tả', 'Hiển thị bảng phiếu đề nghị thanh toán theo chế độ xem, kèm phân trang, sắp xếp và tổng số '
           'bản ghi khớp bộ lọc. Màn có bốn chế độ xem (Tất cả, Của tôi, Chờ duyệt, Đã duyệt) nhưng giao diện chỉ có '
           'lối vào cho hai chế độ Tất cả và Chờ duyệt qua menu; màn không có thanh chuyển chế độ.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^1\. ', [
        '1. Người dùng vào menu %s (hoặc %s) để xem chế độ Tất cả; hoặc vào menu %s để xem chế độ Chờ duyệt. '
        'Hai chế độ Của tôi và Đã duyệt không có mục menu, chỉ mở được bằng đường dẫn trực tiếp.'
        % (MENU_ALL, MENU_ALL2, MENU_PD)])
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. Hệ thống xác định chế độ',
            '2. Hệ thống xác định chế độ xem theo đường dẫn; giá trị lạ hoặc không có thì dùng chế độ Tất cả.')
    ui = sec_ui(s)
    ui_set(ui, r'^Tiêu đề trang$', 'Mô tả', 'Phiếu đề nghị thanh toán (Tất cả) / … của tôi / … chờ duyệt / … đã duyệt.')
    ui_set(ui, r'^Cột Ngày tạo$', 'Tên đối tượng', 'Cột Ngày lập')
    ui_set(ui, r'^Cột Ngày lập$', 'Mô tả', 'Ngày giờ lập phiếu (ngày tạo bản ghi). Sắp xếp được.')
    ui_set(ui, r'^Cột Người tạo$', 'Tên đối tượng', 'Cột Người lập')
    ui_set(ui, r'^Cột Người lập$', 'Mô tả', 'Người lập phiếu (người tạo bản ghi).')
    ui_set(ui, r'^Cột Hình thức TT$', 'Mô tả', 'TM (tiền mặt) hoặc CK (chuyển khoản). Không sắp xếp.')
    ui_set(ui, r'^Cột Trạng thái$', 'Mô tả', 'Hiển thị dạng nhãn màu: Duyệt phiếu chi nền xanh, các trạng thái khác '
           'nền đỏ; sắp xếp được.')
    ui_set(ui, r'^Cột Hành động$', 'Mô tả', 'Cột bắt buộc. Gồm Sửa, Duyệt (mở màn chi tiết), Tạo phiếu chi / Tạo ủy '
           'nhiệm chi, In phiếu, Xuất Excel, Xóa, Lịch sử theo quyền và trạng thái; hiện tối đa 3 nút, các nút còn lại '
           'nằm trong nút ba chấm. Không có nút Xem chi tiết (bấm Mã phiếu).')
    ev = sec_ev(s)
    tr = find_row(ev, 1, r'^Đổi chế độ xem$')
    write_cell(cells(tr)[1], ['Vào màn bằng mục menu khác (đổi chế độ xem)'])
    write_cell(cells(tr)[2], ['System'])

    # ---------------- 2.2 Tìm kiếm
    s = section(doc, r'^2\.2 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Người tạo$', 'Tên đối tượng', 'Người lập')
    ui_set(ui, r'^Người lập$', 'Mô tả', 'Lọc theo người lập phiếu (người tạo bản ghi).')
    ui_set(ui, r'^Ngày tạo từ$', 'Tên đối tượng', 'Ngày lập từ')
    ui_set(ui, r'^Ngày tạo đến$', 'Tên đối tượng', 'Ngày lập đến')
    ui_set(ui, r'^Số tiền đề nghị từ$', 'Phạm vi', '≥ 0, chỉ nhập số')
    ui_set(ui, r'^Số tiền đề nghị đến$', 'Phạm vi', '≥ 0, chỉ nhập số')
    ev = sec_ev(s)
    write_cell(cells(find_row(ev, 1, r'^Nhập từ khóa ô Khách hàng'))[1],
               ['Nhập từ khóa và chọn ở ô Khách hàng / Nhà cung cấp'])
    kv = sec_kv(s)
    kv_edit(kv, 'Mô tả', r'.', 'Thu hẹp danh sách theo mã phiếu, cấp tổ chức, loại chi, hình thức thanh toán, trạng '
            'thái, lý do chi, khách hàng, nhà cung cấp, người lập, khoảng số tiền đề nghị và khoảng ngày lập.')

    # ---------------- 2.3 Cài đặt bộ lọc / Tùy chỉnh cột
    s = section(doc, r'^2\.3 ')
    kv_edit(sec_kv(s), 'Yêu cầu đặc biệt', r'.', 'Cấu hình bộ lọc lưu riêng cho từng chế độ xem; cấu hình cột dùng '
            'CHUNG cho cả bốn chế độ vì có cùng bộ cột.')
    kv_edit(sec_kv(s), 'Dòng sự kiện phụ', r'^• Bấm Đóng',
            '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận, không lưu thay đổi.')
    set_col(sec_ev(s), 2, r'^Bỏ tích một mục', 'Change')

    # ---------------- 2.4 Lập phiếu
    s = section(doc, r'^2\.4 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ',
            '5. Người dùng bấm Lưu nháp, Lưu và tiếp tục, hoặc bấm Lưu và gửi duyệt rồi xác nhận.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ',
            '6. Hệ thống kiểm tra dữ liệu theo nút được bấm, sinh mã phiếu và lưu phiếu (Lưu nháp / Lưu và tiếp tục: '
            'trạng thái Đang tạo; Lưu và gửi duyệt: trạng thái Chờ TP duyệt).')
    kv_edit(kv, 'Dòng sự kiện chính', r'^7\. ', [
        '7. Ghi nhận hành động Tạo mới trong lịch sử của phiếu; gửi duyệt thì gửi thông báo cho nhóm Trưởng phòng '
        'duyệt cùng công ty.',
        '8. Hệ thống hiển thị thông báo thành công và quay về màn danh sách; riêng Lưu và tiếp tục thì ở lại màn Tạo '
        'mới với biểu mẫu trống để lập phiếu tiếp.'])
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn', [UNSAVED, DUE])
    kv_edit(kv, 'Yêu cầu đặc biệt', r'.', 'Ràng buộc dữ liệu khác nhau giữa các nút lưu: Lưu nháp và Lưu và tiếp tục '
            'chỉ bắt buộc Loại chi (các ô khác chỉ kiểm tra định dạng khi có nhập); Lưu và gửi duyệt bắt buộc thêm Hình '
            'thức thanh toán, Loại tiền, Tỷ giá, Lý do chi, bảng chi tiết, khối ngân hàng (nếu chuyển khoản) và file '
            'đính kèm (nếu loại Chi trả nhà cung cấp).')
    ui = sec_ui(s)
    for nm in (r'^Hình thức thanh toán$', r'^Loại tiền$', r'^Tỷ giá \(VND\)$', r'^Lý do chi$'):
        ui_set(ui, nm, 'Bắt buộc', 'Có khi gửi duyệt')
    ui_set(ui, r'^Lý do chi$', 'Mô tả', 'Không bắt buộc ở Lưu nháp / Lưu và tiếp tục.')
    ui_set(ui, r'^Nút Lưu nháp$', 'Mô tả', 'Lưu phiếu ở trạng thái Đang tạo và quay về danh sách.')
    clone_row_after(ui, r'^Nút Lưu nháp$', [None, 'Nút Lưu và tiếp tục', None, None, '', '', 'Hiển thị',
                                            'Chỉ có ở màn Tạo mới. Lưu phiếu ở trạng thái Đang tạo rồi mở lại màn Tạo '
                                            'mới với biểu mẫu trống.'])
    ev = sec_ev(s)
    write_cell(ev_cell(ev, r'^Bấm Lưu nháp$'), [
        'During:',
        '– Bỏ trống Loại chi → hiển thị “Bắt buộc nhập”.',
        '– Các ô khác không bắt buộc, chỉ kiểm tra định dạng khi có nhập (Tỷ giá phải lớn hơn 0, số tiền phải là '
        'số, ngày đúng định dạng); sai thì báo lỗi ngay dưới ô.',
        ERR_LINE,
        'After:',
        '– Sinh mã phiếu theo dạng <mã công ty>.DNTT<tháng năm>.<5 chữ số>; ghi phiếu ở trạng thái Đang tạo cùng '
        'công ty / phòng ban / bộ phận của người tạo.',
        '– Ghi nhận hành động Tạo mới trong lịch sử của phiếu.',
        '– Hiển thị “Lưu phiếu đề nghị thanh toán thành công!” và quay về màn danh sách.'], rid)
    write_cell(cells(find_row(ev, 1, r'^Bấm Lưu nháp$'))[1], ['Bấm Lưu nháp / Lưu và tiếp tục'])
    ev_edit(ev, r'^Bấm Lưu nháp / Lưu và tiếp tục$', r'quay về màn danh sách',
            '– Hiển thị “Lưu phiếu đề nghị thanh toán thành công!”; Lưu nháp thì quay về màn danh sách, Lưu và tiếp '
            'tục thì mở lại màn Tạo mới với biểu mẫu trống.', rid)
    ev_edit(ev, r'^Bấm Lưu và gửi duyệt$', r'^.?\s*Áp toàn bộ kiểm tra của Lưu nháp',
            '– Áp toàn bộ kiểm tra của Lưu nháp, cộng thêm: Hình thức thanh toán, Loại tiền, Tỷ giá, Lý do chi trống '
            '→ “Bắt buộc nhập”;', rid)
    ev_edit(ev, r'^Bấm Lưu và gửi duyệt$', r'Ghi một dòng lịch sử', '– Ghi nhận hành động Tạo mới trong lịch sử '
            'của phiếu.', rid)
    add_err_line(ev, r'^Bấm Lưu và gửi duyệt$', rid)
    tr = find_row(ev, 1, r'^Bấm Quay lại')
    write_cell(cells(tr)[1], ['Bấm Quay lại / chọn menu khác / đóng tab trình duyệt'])
    write_cell(cells(tr)[3], UNSAVED_EV)

    # ---------------- 2.5 Chọn đối tượng / hợp đồng
    s = section(doc, r'^2\.5 ')
    kv = sec_kv(s)
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận; dòng chi tiết giữ nguyên.'])

    # ---------------- 2.8 File đính kèm
    s = section(doc, r'^2\.8 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Cột Dung lượng$', 'Loại', 'Label')

    # ---------------- 2.9 Sửa phiếu
    s = section(doc, r'^2\.9 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ', [
        '5. Hệ thống kiểm tra quyền và dữ liệu rồi ghi lại phiếu.',
        '6. Ghi nhận các thay đổi (theo từng trường, từng dòng chi tiết và danh sách file) trong lịch sử của phiếu; '
        'chuyển sang Chờ TP duyệt thì gửi thông báo cho nhóm Trưởng phòng duyệt.'])
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. Hệ thống hiển thị',
            '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Rời màn', [UNSAVED, DUE])
    ui = sec_ui(s)
    ui_set(ui, r'^Hình thức thanh toán$', 'Bắt buộc', 'Có khi gửi duyệt')
    ui_set(ui, r'^Loại tiền$', 'Bắt buộc', 'Có khi gửi duyệt')
    ui_set(ui, r'^Tỷ giá \(VND\)$', 'Bắt buộc', 'Có khi gửi duyệt')
    ui_set(ui, r'^Lý do chi$', 'Bắt buộc', 'Có khi gửi duyệt')
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$', r'Ghi một dòng lịch sử',
            '– Ghi nhận các thay đổi trong lịch sử của phiếu (“Thay đổi thông tin”, liệt kê từng trường đã đổi).', rid)
    add_err_line(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$', rid)
    clone_row_after(ev, r'^Bấm Lưu nháp / Lưu và gửi duyệt$',
                    [None, 'Bấm Quay lại / chọn menu khác / đóng tab trình duyệt', 'Click', UNSAVED_EV])

    # ---------------- 2.10 Xem chi tiết
    s = section(doc, r'^2\.10 ')
    ui = sec_ui(s)
    ui_set(ui, r'^Nút In$', 'Mô tả', 'Mở cửa sổ Xem trước bản in (khổ ngang) ngay trên màn hình.')
    ui_set(ui, r'^Nút Duyệt$', 'Mô tả', 'Người xem có quyền duyệt ở đúng trạng thái hiện tại của phiếu. Ẩn khi '
           'không đủ điều kiện.')

    # ---------------- 2.11 Duyệt
    s = section(doc, r'^2\.11 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^6\. ',
            '6. Người dùng xác nhận; hệ thống kiểm tra quyền và trạng thái, ghi số tiền, đổi trạng thái phiếu và ghi '
            'nhận hành động Thay đổi trạng thái (kèm số tiền cấp đó đã ghi) trong lịch sử của phiếu.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^7\. ',
            '7. Hệ thống gửi thông báo cho các bên liên quan, hiển thị thông báo “Phiếu đề nghị thanh toán đã được gửi '
            'đến <cấp nhận phiếu>!” và nạp lại màn chi tiết.')
    write_cell(kv_row(kv, 'Dòng sự kiện phụ'), kv_get(kv, 'Dòng sự kiện phụ') + [
        '• Phiếu không có dòng chi tiết → báo “Phiếu không có dòng chi tiết để duyệt”, không mở hộp xác nhận.', DUE])
    ev = sec_ev(s)
    add_err_line(ev, r'^Bấm nút Duyệt ở màn chi tiết$', rid)
    add_err_line(ev, r'^Bấm nút Chuyển duyệt BGĐ$', rid)

    # ---------------- 2.12 Từ chối
    s = section(doc, r'^2\.12 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Bấm Đóng',
            '• Bấm Đóng / (x) / click ra ngoài cửa sổ → cửa sổ đóng ngay, không hỏi xác nhận kể cả khi đã nhập; phiếu '
            'giữ nguyên; mở lại thì hai ô trở về trống.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. ',
            '5. Hệ thống kiểm tra quyền và ghi chú, đổi trạng thái phiếu, ghi nhận hành động Thay đổi trạng thái kèm '
            'ghi chú trong lịch sử của phiếu và gửi thông báo.')
    add_err_line(sec_ev(s), r'^Bấm nút Từ chối trong cửa sổ$', rid)

    # ---------------- 2.13 Xóa
    s = section(doc, r'^2\.13 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Dòng sự kiện chính', r'^4\. ', [
        '4. Hệ thống kiểm tra người tạo và trạng thái phiếu.',
        '5. Ghi nhận hành động Xóa (kèm nội dung phiếu trước khi xóa) trong lịch sử, rồi xóa các dòng chi tiết và '
        'xóa phiếu.'])
    kv_edit(kv, 'Dòng sự kiện chính', r'^5\. Hệ thống hiển thị',
            '6. Hệ thống hiển thị thông báo “Xóa thành công”: xóa từ danh sách thì nạp lại danh sách, xóa từ màn chi '
            'tiết thì quay về màn danh sách.')
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm nút Xóa trong hộp xác nhận$', r'Xóa toàn bộ dòng chi tiết rồi xóa phiếu', [
        '– Ghi nhận hành động Xóa (kèm nội dung phiếu trước khi xóa) trong lịch sử.',
        '– Xóa toàn bộ dòng chi tiết rồi xóa phiếu.'], rid)
    add_err_line(ev, r'^Bấm nút Xóa trong hộp xác nhận$', rid)

    # ---------------- 2.14 In / Xuất Excel — bản in mở POPUP xem trước, không mở tab mới
    s = section(doc, r'^2\.14 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Mô tả', r'.', 'Mở cửa sổ Xem trước bản in Phiếu đề nghị thanh toán (khổ ngang) ngay trên màn hình, '
            'hoặc tải file Excel của phiếu. Hai đầu ra dùng chung dữ liệu nên số liệu luôn khớp nhau.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^2\. ',
            '2. Với In: hệ thống mở cửa sổ Xem trước bản in ngay trên màn hình, nạp dữ liệu và dựng bản in; người '
            'dùng bấm nút In trên cửa sổ để mở hộp thoại in của trình duyệt.')
    kv_edit(kv, 'Dòng sự kiện chính', r'^3\. ',
            '3. Với Xuất Excel: hệ thống dựng file và trình duyệt tải file về (tên file De-nghi-thanh-toan-<mã phiếu>), '
            'hiển thị “Xuất Excel thành công”.')
    ui = sec_ui(s)
    ui_set(ui, r'^Nút In$', 'Mô tả', 'Nằm trên tiêu đề cửa sổ Xem trước; mở hộp thoại in của trình duyệt, không xuất '
           'hiện trên bản in.')
    ui_set(ui, r'^Logo và thông tin công ty$', 'Loại', 'Label')
    ev = sec_ev(s)
    ev_edit(ev, r'^Bấm nút In phiếu$', r'Mở tab mới', '– Mở cửa sổ Xem trước bản in của phiếu tương ứng ngay trên màn '
            'hình.')
    write_cell(cells(find_row(ev, 1, r'^Bấm nút In trên bản in$'))[1], ['Bấm nút In trên cửa sổ Xem trước'])
    ev_edit(ev, r'^Bấm nút In trên cửa sổ Xem trước$', r'ẩn nút In', '– Mở hộp thoại in của trình duyệt; nút In và '
            'khung cửa sổ không xuất hiện trên bản in.')

    # ---------------- 2.15 Lịch sử — tạo / xóa cũng ghi lịch sử
    s = section(doc, r'^2\.15 ')
    kv = sec_kv(s)
    kv_edit(kv, 'Mô tả', r'.', 'Hiển thị toàn bộ thao tác đã tác động lên phiếu theo dòng thời gian: tạo mới, thay đổi '
            'thông tin, thay đổi trạng thái (duyệt, chuyển duyệt, từ chối), kèm người thực hiện, giá trị trước / sau và '
            'số tiền từng cấp duyệt đã ghi.')
    kv_edit(kv, 'Dòng sự kiện phụ', r'^• Phiếu chưa từng',
            '• Phiếu lập từ hệ thống cũ, chưa có thao tác nào trên hệ thống mới → hiện “Chưa có lịch sử thao tác nào.”')
    ui = sec_ui(s)
    ui_set(ui, r'^Trạng thái rỗng$', 'Mô tả', 'Hiện “Chưa có lịch sử thao tác nào.” với phiếu lập từ hệ thống cũ, chưa '
           'có thao tác nào trên hệ thống mới.')


def part_heading(doc, n):
    for e in items(doc):
        if e.tag == W('p') and style_of(e) == 'Heading1' and re.match(r'^Phần %d\b' % n, txt(e)):
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

    def row(code):
        return find_row(tbl, 1, '^%s$' % code)

    # BR-02: đủ 4 chế độ theo code (bản Drive mới ghi 2)
    write_cell(cells(row('BR-02'))[3], [
        '– Chế độ Tất cả: áp phạm vi quyền xem theo thứ tự V1 → V2 → V3 → V4; không có cấp nào thì chỉ thấy phiếu do '
        'chính mình tạo; phiếu Đang tạo của người khác luôn bị ẩn.',
        '– Chế độ Của tôi: phiếu do chính mình tạo (kể cả phiếu Đang tạo).',
        '– Chế độ Chờ duyệt: phiếu cùng công ty với người đăng nhập VÀ đang ở đúng trạng thái mà người đó có quyền '
        'duyệt / xử lý; không giữ vai nào thì danh sách rỗng.',
        '– Chế độ Đã duyệt: phiếu chính người đăng nhập đã duyệt.',
        '– Menu chỉ có lối vào chế độ Tất cả và Chờ duyệt; Của tôi và Đã duyệt chỉ mở bằng đường dẫn trực tiếp.'])
    write_cell(cells(row('BR-8'))[3], [
        '– Lưu nháp / Lưu và tiếp tục: chỉ bắt buộc Loại chi; các ô khác (hình thức thanh toán, loại tiền, tỷ giá, lý '
        'do chi, đối tượng, khối ngân hàng, bảng chi tiết, file đính kèm) không bắt buộc nhưng có nhập thì vẫn kiểm '
        'tra định dạng.',
        '– Lưu và gửi duyệt: bắt buộc thêm hình thức thanh toán, loại tiền, tỷ giá, lý do chi, ít nhất một dòng chi '
        'tiết hợp lệ (đủ đối tượng, hợp đồng và số tiền từ 1 trở lên), khối ngân hàng (nếu chuyển khoản) và file đính '
        'kèm (nếu loại Chi trả nhà cung cấp).'])
    clone_row_after(tbl, r'^BR-14$', [None, 'BR-99', 'Chặn khi còn hàng quá hạn', [
        '– Lưu nháp, Lưu và gửi duyệt và Duyệt đi qua kiểm tra “Duyệt đề nghị thanh toán” của cấu hình chặn hàng quá '
        'hạn (Khai Quy chế – Cấu hình).',
        '– Nhân viên thuộc phòng ban người dùng quản lý còn hàng quá hạn → hệ thống chặn thao tác và hiện thông báo lý '
        'do; tài khoản Super admin không bị chặn.'], '- Tạo phiếu / - Sửa phiếu / - Duyệt'], col=1)
    for i, tr in enumerate(rows(tbl)[1:], 1):
        write_cell(cells(tr)[1], ['BR-%02d' % i])
    renumber_stt(tbl)
    log('Phần 4: đánh lại %d quy tắc BR-01..BR-%02d liên tục' % (len(rows(tbl)) - 1, len(rows(tbl)) - 1))


def add_part5(doc):
    h4 = part_heading(doc, 4)
    anchor = doc.element.body[-1].getprevious()
    h5 = clone_heading(h4, 'Phần 5: Bảng Danh sách các màn hình tham chiếu dữ liệu', anchor)
    intro = docxlib.clone_par_after(h5, h4.getnext(), 'Các màn hình dưới đây đọc hoặc cập nhật dữ liệu do %s ghi ra '
                                    '(phiếu đã duyệt xong ở trạng thái Chờ tạo phiếu chi).' % SCREEN)
    strip_ids(intro)
    tpl = sec_ev(section(doc, r'^2\.1 '))
    new_table_like(tpl, intro, ['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], PART5, [850, 1500, 3600, 2900])
    log('Thêm Phần 5 (%d màn tham chiếu)' % len(PART5))


if __name__ == '__main__':
    main()
