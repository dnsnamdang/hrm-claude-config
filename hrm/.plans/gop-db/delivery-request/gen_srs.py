# -*- coding: utf-8 -*-
"""SRS màn "Phiếu yêu cầu vận chuyển, bốc xếp" (mã {cty}.YCVC{mmyy}.NNNNN) — form chuẩn Danh mục quốc gia (30/10/2026).

Chạy: python gen_srs.py  → SRS - Phiếu yêu cầu vận chuyển, bốc xếp.docx
Khung: srs-documenter (SrsDoc) + checklist ../phieu-theo-form-quoc-gia/CHECKLIST.md. Khuôn thư mục: bank-account-catalog.
Nguồn đọc 30/10/2026 (nhánh develop, cả 2 repo):
  BE  Modules/Finance/{Entities/DeliveryRequest/*, Services/DeliveryRequest{,Write,Notify,Attachment}Service.php,
      Http/Controllers/V1/DeliveryRequestController.php, Http/Requests/DeliveryRequest/*}
  FE  pages/finance/delivery-requests/**, components/subsystem-menu/sale-hub.js
  Spec docs/superpowers/specs/gop-db/2026-10-08-delivery-request-design.md
Ảnh: ./ycvc_shots (dev-hrm 30/10/2026, tài khoản DNS Admin, script ycvc_shots/_capture/capture.js).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
HRM = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(HRM, '.claude', 'skills', 'srs-documenter', 'assets'))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from srs_docx_lib import SrsDoc  # noqa: E402
from srs_split_rows import split_ui_rows  # noqa: E402  (tách dòng gộp: mỗi đối tượng 1 hàng)

TEN = 'Phiếu yêu cầu vận chuyển, bốc xếp'
SHOTS = os.path.join(HERE, 'ycvc_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # sơ đồ Use Case; HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => YC vận chuyển, bốc xếp'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu yêu cầu vận chuyển, bốc xếp.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_LAP = 'Người lập phiếu'
A_TK = 'Thủ kho'
TN_MOI = 'Người dùng có quyền thực hiện chức năng: mọi người dùng đã đăng nhập (không cần quyền riêng).'
TN_XEM = ('Người dùng có quyền thực hiện chức năng: người lập phiếu; thủ kho của kho xuất hàng; người có một trong '
          'các quyền Xem tất cả phiếu yêu cầu vận chuyển của tổng công ty / của công ty / của phòng ban / của bộ phận.')
TN_SUA = 'Người dùng có quyền thực hiện chức năng: người lập phiếu (không cần quyền riêng).'
TN_TK = 'Người dùng có quyền thực hiện chức năng: thủ kho của kho xuất hàng trên phiếu yêu cầu xuất hàng.'
DK_XEM = '1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Phiếu yêu cầu vận chuyển, bốc xếp.'

d = SrsDoc(out=OUT, menu=MENU, route='/finance/delivery-requests', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Bán hàng': 'menu_phanhe', 'Yêu cầu': 'menu_yeucau', 'Hàng hóa': 'menu_hanghoa',
    'YC vận chuyển, bốc xếp': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Sửa': 'btn_sua_row', 'Xóa': 'btn_xoa_row', 'Duyệt': 'btn_duyet', 'Từ chối': 'btn_tuchoi',
    'Xuất Excel': 'btn_xuatexcel', 'Lịch sử': 'btn_lichsu_row',
}.items()})


# Mô tả riêng cho hàng sau khi tách dòng gộp (srs_split_rows) — mỗi đối tượng 1 hàng.
UI_OVER = {
    'Khách hàng': 'Khách hàng của phiếu YCXH, tự điền khi chọn phiếu.',
    'Người liên hệ': 'Người liên hệ trên phiếu YCXH, tự điền.',
    'Số ĐT người liên hệ': 'Số điện thoại người liên hệ trên phiếu YCXH, tự điền.',
    'Địa điểm giao hàng': 'Địa điểm giao trên phiếu YCXH, tự điền.',
    'Cột Ngày tạo': 'Sắp xếp được.',
    'Cột Ngày cập nhật': ['- Thời điểm sửa phiếu gần nhất', '- Sắp xếp được'],
    'Cột Ngày duyệt': ['- Thời điểm thủ kho duyệt / từ chối', '- Sắp xếp được'],
    'Cột Người tạo': 'Người lập phiếu, dạng “Họ tên - Phòng ban”.',
    'Cột Người cập nhật': 'Người sửa phiếu gần nhất, dạng “Họ tên - Phòng ban”.',
    'Cột Người duyệt': 'Thủ kho đã duyệt / từ chối, dạng “Họ tên - Phòng ban”.',
    'Công ty': {'scope': 'Danh sách công ty', 'desc': 'Chỉ hiện với V1.'},
    'Phòng ban': {'scope': 'Danh sách phòng ban', 'desc': ['- Hiện với V1, V2, V3', '- Chỉ còn phòng ban của Công ty đã chọn',
                                                          '- Đổi Công ty thì bị xóa']},
    'Bộ phận': {'scope': 'Danh sách bộ phận', 'desc': ['- Hiện theo cấp quyền', '- Chỉ còn bộ phận của Phòng ban đã chọn',
                                                      '- Đổi Phòng ban thì bị xóa']},
    'Người duyệt': 'Thủ kho đã duyệt / từ chối; hiện khi phiếu Đã duyệt hoặc Từ chối.',
    'Ngày duyệt': {'scope': 'dd/mm/yyyy hh:mm', 'desc': 'Thời điểm duyệt / từ chối; hiện khi phiếu Đã duyệt hoặc Từ chối.'},
    'File đính kèm': 'STT, tên file (xem / tải), Dung lượng.',
    'Bảng Chi tiết': 'STT, Tên hàng, Model, Mã hàng hóa, ĐVT, Số lượng, Số kiện.',
    'Nút Sửa': 'Mở màn Sửa; chỉ người lập, phiếu Đang tạo / Từ chối.',
    'Nút Xóa': 'Mở hộp Xác nhận xóa; chỉ người lập, phiếu Đang tạo / Từ chối.',
    'Nút Duyệt': 'Mở hộp Xác nhận duyệt; chỉ thủ kho, phiếu Chờ duyệt.',
    'Nút Từ chối': 'Mở cửa sổ Từ chối; chỉ thủ kho, phiếu Chờ duyệt.',
    ('Nút Tìm kiếm / Làm mới', 'Nút Tìm kiếm'): 'Lọc theo mã đã nhập (và Loại hợp đồng), về trang 1.',
    ('Nút Tìm kiếm / Làm mới', 'Nút Làm mới'): 'Xóa điều kiện tìm trong cửa sổ, nạp lại.',
}
_RO = lambda n, t, scope, desc: (n, t, 'Read-only', scope, 'Theo dữ liệu', desc)  # noqa: E731
UI_EXPLICIT = {
    'Các ô thông tin vận chuyển và bốc xếp': [
        _RO('Mã phiếu', 'Textbox', '–', 'Mã do hệ thống sinh.'),
        _RO('Đơn hàng/Hợp đồng', 'Textbox', '–', 'Liên kết mở chứng từ ở tab mới.'),
        _RO('Phiếu YCXH', 'Textbox', '–', 'Liên kết mở chi tiết phiếu yêu cầu xuất hàng ở tab mới.'),
        _RO('Khách hàng', 'Textbox', '–', 'Theo phiếu YCXH.'),
        _RO('Người liên hệ', 'Textbox', '–', 'Theo phiếu YCXH.'),
        _RO('Số ĐT người liên hệ', 'Textbox', '–', 'Theo phiếu YCXH.'),
        _RO('Địa điểm giao hàng', 'Textbox', '–', 'Theo phiếu YCXH.'),
        _RO('Thời gian vận chuyển', 'Datepicker', 'dd/mm/yyyy hh:mm', '–'),
        _RO('Ghi chú', 'Textarea', '0–5000 ký tự', '–'),
        _RO('Tổng số kiện', 'Textbox', 'Số nguyên ≥ 0', '–'),
        _RO('Phương thức bốc xếp', 'Textbox', '0–255 ký tự', '–'),
        _RO('Địa điểm bốc xếp', 'Textbox', '0–255 ký tự', '–'),
        _RO('Thời gian bốc xếp', 'Datepicker', 'dd/mm/yyyy hh:mm', '–'),
    ],
}


def uc(code, name, group, actor):
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None):
    """Một chức năng 2.x: (Biểu đồ Usecase) · Giới thiệu · Layout · Mô tả giao diện · Event."""
    d.h3('2.%d %s' % (no, title))
    k = 1
    if usecase:
        d.p('2.%d.%d Biểu đồ Usecase' % (no, k))
        uc(*usecase)
        k += 1
    d.p('2.%d.%d Giới thiệu' % (no, k))
    tail, anchor = rule
    d.rule_ref(tail + ' ' + RIENG, anchor=anchor)
    d.intro_table(**intro)
    k += 1
    d.p('2.%d.%d Layout màn hình' % (no, k))
    d.layout(**layout)
    k += 1
    assert ui and ev, 'Thiếu bảng giao diện / event ở 2.%d' % no
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (no, k))
    d.ui_table(split_ui_rows(ui, UI_OVER, UI_EXPLICIT), **(ui_kw or {}))
    k += 1
    d.p('2.%d.%d Danh sách event và xử lý event' % (no, k))
    d.event_table(ev)


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.h2('Mục lục')
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu yêu cầu vận chuyển, bốc xếp (mã phiếu …YCVC…), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng duyệt của màn hình.',
    'Làm rõ cách người lập gắn phiếu với đơn hàng/hợp đồng và phiếu yêu cầu xuất hàng, rồi đề nghị thủ kho '
    'bố trí vận chuyển và bốc xếp.',
    'Làm rõ người duyệt (thủ kho của kho xuất hàng), điều kiện Sửa / Xóa và phạm vi dữ liệu theo từng cấp quyền.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu yêu cầu vận chuyển', 'Phiếu của màn này, mã dạng <mã công ty>.YCVC<tháng năm>.NNNNN, ví dụ TPE.YCVC1026.00004.'),
    ('Phiếu YCXH', 'Phiếu yêu cầu xuất hàng — nguồn lấy khách hàng, người liên hệ, địa điểm giao và danh sách hàng.'),
    ('Đơn hàng/Hợp đồng', 'Chứng từ bán hàng gắn với phiếu (hợp đồng bán, hợp đồng dịch vụ BH-SC, hợp đồng mua…).'),
    ('Thủ kho', 'Nhân viên được khai là thủ kho của kho xuất hàng trên phiếu YCXH — người duyệt / từ chối.'),
    ('Số kiện', 'Số kiện hàng của từng dòng, người lập tự nhập để bố trí bốc xếp.'),
    ('Đang tạo / Chờ duyệt / Đã duyệt / Từ chối', 'Bốn trạng thái của phiếu.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Lập phiếu không cần quyền riêng. Sửa / Xóa: chỉ người lập, khi phiếu Đang tạo hoặc Từ chối. Duyệt / Từ chối: '
    'thủ kho của kho xuất hàng (Super admin cũng duyệt được), khi phiếu Chờ duyệt.')
d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét từ trên xuống, có cấp nào áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả phiếu yêu cầu vận chuyển của tổng công ty', 'Toàn bộ phiếu của mọi công ty.'),
    ('V2', 'Xem tất cả phiếu yêu cầu vận chuyển của công ty', 'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem tất cả phiếu yêu cầu vận chuyển của phòng ban',
     'Phiếu thuộc phòng ban người đăng nhập quản lý / đang ngồi + phiếu mình lập.'),
    ('V4', 'Xem tất cả phiếu yêu cầu vận chuyển của bộ phận', 'Phiếu thuộc bộ phận mình quản lý + phiếu mình lập.'),
    ('—', '(không có quyền nào)', 'Phiếu mình lập.'),
], widths=[0.8, 2.4, 2.8])
d.p('Mọi cấp đều thấy thêm: phiếu mình đã duyệt / từ chối và phiếu mình là thủ kho của kho xuất hàng. Phiếu Đang tạo '
    'của người khác luôn ẩn.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người lập', 'Thủ kho', 'V1–V4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅'),
    ('FR-05 Lập phiếu', '✅', '✅', '✅', '✅'),
    ('FR-06 Chọn đơn hàng/hợp đồng', '✅', '✅', '✅', '✅'),
    ('FR-07 Chọn phiếu YCXH', '✅', '✅', '✅', '✅'),
    ('FR-08 Chỉnh sửa', '✅ (Đang tạo, Từ chối)', '❌', '❌', '❌'),
    ('FR-09 Xóa', '✅ (Đang tạo, Từ chối)', '❌', '❌', '❌'),
    ('FR-10 Xem chi tiết', '✅', '✅', '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-11 Duyệt', '❌', '✅ (Chờ duyệt)', '❌', '❌'),
    ('FR-12 Từ chối', '❌', '✅ (Chờ duyệt)', '❌', '❌'),
    ('FR-13 Xuất Excel', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-14 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅ (phiếu của mình)'),
], widths=[2.0, 1.2, 1.0, 1.0, 1.3])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_LAP, [0, 1, 2, 3, 6]), (A_TK, [0, 4, 5, 6])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu', 'crud'),
     ('FR-08', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-09', 'Xóa phiếu', 'action'),
     ('FR-11', 'Duyệt phiếu', 'action'),
     ('FR-12', 'Từ chối phiếu', 'action'),
     ('FR-13', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-10', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-14', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn đơn hàng/hợp đồng', 'crud', 'extend', [1, 2], None),
     ('FR-07', 'Chọn phiếu YCXH', 'crud', 'extend', [1, 2], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu yêu cầu vận chuyển, bốc xếp')

d.h2('2 Đặc tả chi tiết từng chức năng')

FORM_UI = [
    ('Mã phiếu', 'Textbox', 'Read-only', '–', '–', 'Hệ thống sinh khi lưu', 'Chỉ hiện ở màn Sửa / Chi tiết.'),
    ('Đơn hàng/Hợp đồng', 'Textbox', 'Enable', 'Danh sách đơn hàng/hợp đồng', 'Có', 'Trống', [
        '- Gợi ý “Chọn đơn hàng/hợp đồng...”; bấm vào ô → mở cửa sổ Chọn đơn hàng/hợp đồng (FR-06)',
        '- Có dấu × để bỏ chọn; đổi hợp đồng thì xóa Phiếu YCXH đã chọn', '- Lỗi: “Bắt buộc phải nhập”']),
    ('Phiếu YCXH', 'Textbox', 'Enable', 'Danh sách phiếu YCXH', 'Có', 'Trống', [
        '- Gợi ý “Chọn phiếu yêu cầu xuất hàng...”; bấm → mở cửa sổ Chọn phiếu yêu cầu xuất hàng (FR-07)',
        '- Chưa chọn hợp đồng: báo “Vui lòng chọn đơn hàng/hợp đồng trước.”', '- Lỗi: “Bắt buộc phải nhập”']),
    ('Khách hàng / Người liên hệ / Số ĐT người liên hệ / Địa điểm giao hàng', 'Textbox', 'Read-only', '–', '–',
     '“Lấy theo phiếu YCXH”', 'Tự điền từ phiếu YCXH đã chọn.'),
    ('Thời gian vận chuyển', 'Datepicker', 'Enable', 'dd/mm/yyyy hh:mm', 'Không', 'Trống', 'Gợi ý “Chọn thời gian vận chuyển”.'),
    ('Ghi chú', 'Textarea', 'Enable', '0–5000 ký tự', 'Không', 'Trống', 'Lỗi: “Vui lòng nhập tối đa 5000 ký tự.”'),
    ('Tổng số kiện', 'Textbox', 'Enable', 'Số nguyên ≥ 0', 'Không', 'Trống', 'Lỗi: “Vui lòng nhập số nguyên.”'),
    ('Phương thức bốc xếp', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Gợi ý “Nhập phương thức bốc xếp”.'),
    ('Địa điểm bốc xếp', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Gợi ý “Nhập địa điểm bốc xếp”.'),
    ('Thời gian bốc xếp', 'Datepicker', 'Enable', 'dd/mm/yyyy hh:mm', 'Không', 'Trống', '–'),
    ('File đính kèm', 'Table/Grid', 'Enable', 'pdf, xlsx, xls, jpeg, jpg, png; tối đa 20 MB / file', 'Không', 'Chưa có file',
     ['- Nút Thêm tài liệu; bảng STT, Upload / File, Dung lượng', '- Lỗi: “Định dạng file không hợp lệ” / “File quá lớn”']),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Có', '“Không có dữ liệu”', [
        '- Cột STT, Tên hàng, Model, Mã hàng hóa, ĐVT, Số lượng: lấy từ các dòng hàng của phiếu YCXH (số lượng > 0)',
        '- Bảng trống khi đã chọn phiếu YCXH: “Bắt buộc phải nhập”']),
    ('Cột Số kiện', 'Textbox', 'Enable', 'Số nguyên ≥ 0', 'Không', 'Trống', 'Gợi ý “Nhập số kiện”; lỗi “Vui lòng nhập số nguyên.”'),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu ở trạng thái Đang tạo.'),
    ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Lưu ở trạng thái Chờ duyệt, báo thủ kho.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách; hỏi xác nhận nếu có thay đổi chưa lưu.'),
]

SAVE_EV = [
    ('Bấm Lưu nháp / Gửi duyệt', 'Click',
     'Before:\n– Sửa: kiểm tra người lập và phiếu Đang tạo / Từ chối; phiếu đã đổi trạng thái → “Trạng thái đã bị thay '
     'đổi. Vui lòng load lại trang”.\n'
     'During:\n– Thiếu Đơn hàng/Hợp đồng, Phiếu YCXH hoặc bảng Chi tiết trống → “Bắt buộc phải nhập” dưới ô, thông báo '
     '“Vui lòng kiểm tra lại thông tin đã nhập”.\n'
     '– Số kiện / Tổng số kiện không phải số nguyên → “Vui lòng nhập số nguyên.”; quá giới hạn ký tự → “Vui lòng nhập '
     'tối đa N ký tự.”.\n'
     '– Phiếu YCXH không còn chọn được → “Phiếu này không còn chọn được, vui lòng chọn phiếu khác.”; chưa gắn khách '
     'hàng → “Phiếu chưa gắn khách hàng, vui lòng chọn phiếu khác.”; hợp đồng không còn → “Đơn hàng/hợp đồng không tồn '
     'tại, vui lòng chọn lại.”.\n'
     '– Gửi duyệt mà kho xuất hàng chưa có thủ kho → “Kho xuất hàng chưa có thủ kho, chưa gửi duyệt được.”.\n' + ERR + '\n'
     'After:\n– Khách hàng, người liên hệ, địa điểm giao, dòng hàng lấy lại từ phiếu YCXH lúc lưu.\n'
     '– Lập mới: sinh mã <mã công ty>.YCVC<mmyy>.NNNNN; công ty, phòng ban, bộ phận theo người lập.\n'
     '– Ghi nhận trong lịch sử (Tạo mới / Thay đổi thông tin; gửi duyệt ghi thêm mốc Thay đổi trạng thái).\n'
     '– Gửi duyệt: báo “[YCVC] Chờ duyệt” cho mọi thủ kho của kho xuất hàng; gửi lại sau Từ chối thì xóa lý do cũ.\n'
     '– Báo “Thêm mới thành công.” / “Cập nhật thành công.” / “Gửi duyệt thành công.”, quay về màn danh sách.'),
    ('Bấm Quay lại / rời màn', 'Click', 'Before:\n– Có thay đổi chưa lưu → hỏi xác nhận rời trang.\nAfter:\n– Về màn danh sách.'),
]

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu yêu cầu vận chuyển, bốc xếp',
       mota='Hiển thị các phiếu trong phạm vi dữ liệu của người đăng nhập, mới tạo xếp trên.',
       tacnhan=TN_XEM, dieukien='1. Người dùng đăng nhập thành công.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống áp phạm vi dữ liệu theo quyền (Phần 2).\n'
             '3. Hệ thống hiển thị trang đầu 10 dòng kèm tổng số phiếu.',
       phu='• Phiếu Đang tạo của người khác không hiện.\n• Không có phiếu → “Không có dữ liệu phù hợp.”.',
       dacbiet=None),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Phiếu yêu cầu vận chuyển, bốc xếp'),
   ui_kw=dict(required=False),
   ui=[
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Mở màn Tạo phiếu (FR-05).'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', 'Mở cửa sổ Chọn trường xuất Excel (FR-13).'),
       ('Nút Cấu hình cột hiển thị', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Tùy chỉnh cột (FR-04).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Cột khóa, luôn hiện.'),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Bấm mã → mở màn chi tiết (FR-10)', '- Sắp xếp được; cột khóa']),
       ('Cột Số hợp đồng/đơn hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Bấm số → mở chứng từ ở tab mới (hợp đồng trên HRM mở màn HRM, hợp đồng ERP mở ERP)', '- Sắp xếp được']),
       ('Cột Phiếu YCXH', 'Table/Grid', 'Read-only', '–', 'Ẩn', 'Bấm mã → mở chi tiết phiếu yêu cầu xuất hàng ở tab mới.'),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Sắp xếp được.'),
       ('Cột Ngày tạo / Ngày cập nhật / Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', 'Sắp xếp được.'),
       ('Cột Người tạo / Người cập nhật / Người duyệt', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Dạng “Họ tên - Phòng ban”.'),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Đang tạo: xám', '- Chờ duyệt: cam', '- Đã duyệt: xanh lá', '- Từ chối: đỏ']),
       ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị', [
           '- Sửa, Xóa: người lập, phiếu Đang tạo / Từ chối', '- Duyệt: thủ kho, phiếu Chờ duyệt; bấm → mở chi tiết',
           '- Lịch sử: luôn hiện']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả', 'N: tổng phiếu khớp bộ lọc trong phạm vi quyền.'),
       ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, 10 dòng', '–'),
   ],
   ev=[
       ('Mở màn hình', 'System', 'Before:\n– Xác định phạm vi theo quyền.\nAfter:\n– Hiển thị trang 1, mới tạo xếp trên.'),
       ('Bấm Mã phiếu', 'Click', 'After:\n– Mở màn chi tiết (FR-10).'),
       ('Bấm tiêu đề cột sắp xếp được', 'Click', 'After:\n– Sắp xếp tăng / giảm, về trang 1, giữ bộ lọc.'),
       ('Đổi trang / số dòng', 'Click', 'After:\n– Nạp lại dữ liệu; đổi số dòng thì về trang 1.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu',
       mota='Thu hẹp danh sách theo mã phiếu / số hợp đồng / mã YCXH, khách hàng, hợp đồng, người tạo, trạng thái, ngày tạo '
            'và công ty – phòng ban – bộ phận.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi bấm Tìm kiếm, hoặc bấm Tìm kiếm nâng cao.\n'
             '2. Người dùng chọn / nhập tiêu chí lọc.\n3. Hệ thống nạp lại danh sách.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí, nạp lại từ trang 1.', dacbiet=None),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách'),
   ui=[
       ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo mã phiếu, số hợp đồng, mã phiếu YCXH...”', '- Chạy khi bấm Tìm kiếm']),
       ('Nút Tìm kiếm / Làm mới / Tìm kiếm nâng cao / Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Công ty / Phòng ban / Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Theo quyền', 'Không', 'Trống',
        ['- Công ty: chỉ V1', '- Phòng ban, Bộ phận: theo cấp quyền; phụ thuộc ô cấp trên']),
       ('Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng', 'Không', 'Trống', 'Gõ để tìm khách hàng.'),
       ('Hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Gợi ý “Nhập số hợp đồng/đơn hàng”.'),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', '–'),
       ('Trạng thái', 'Dropdown', 'Enable', 'Đang tạo, Chờ duyệt, Đã duyệt, Từ chối', 'Không', 'Trống', '–'),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Từ ngày → đến ngày.'),
   ],
   ev=[
       ('Đổi giá trị ô lọc nâng cao', 'Change', 'After:\n– Về trang 1, nạp lại danh sách.'),
       ('Bấm Tìm kiếm', 'Click', 'After:\n– Áp ô tìm nhanh (mã phiếu, số hợp đồng, mã phiếu YCXH), về trang 1.'),
       ('Bấm Làm mới', 'Click', 'After:\n– Xóa mọi tiêu chí, nạp lại.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị', mota='Bật / tắt, sắp thứ tự ô lọc; lưu theo người dùng.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Bấm Cài đặt bộ lọc.\n2. Tích / bỏ tích, kéo đổi thứ tự.\n3. Bấm Lưu.',
              phu='• Khôi phục mặc định → về cấu hình ban đầu.\n• Đóng → bỏ thay đổi.', dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Danh sách ô lọc', 'Table/Grid', 'Enable', '6 mục', '–', 'Theo cấu hình',
        'Công ty – Phòng ban – Bộ phận, Khách hàng, Hợp đồng, Người tạo, Trạng thái, Ngày tạo.'),
       ('Nút Lưu / Khôi phục mặc định / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ],
   ev=[('Kéo đổi vị trí', 'Drag', 'After:\n– Đổi thứ tự; lưu khi bấm Lưu.'),
       ('Bấm Lưu', 'Click', 'After:\n– Lưu theo người dùng, vẽ lại khối lọc.')])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Tùy chỉnh cột của bảng danh sách', mota='Bật / tắt, kéo sắp xếp 13 cột; STT, Mã phiếu, Hành động bị khóa.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Bấm nút Cấu hình cột hiển thị.\n2. Tích / bỏ tích, kéo đổi thứ tự.\n3. Bấm Lưu.',
              phu='• Đóng → bỏ thay đổi.', dacbiet='Cột Phiếu YCXH mặc định ẩn.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Danh sách cột', 'Table/Grid', 'Enable', '13 cột', '–', 'Theo cấu hình',
        'STT, Mã phiếu, Số hợp đồng/đơn hàng, Phiếu YCXH, Khách hàng, Ngày tạo, Người tạo, Ngày cập nhật, Người cập nhật, '
        'Ngày duyệt, Người duyệt, Trạng thái, Hành động.'),
       ('Cột bị khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích', 'STT, Mã phiếu, Hành động.'),
       ('Nút Chọn tất cả / Bỏ chọn hết / Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
   ],
   ev=[('Kéo biểu tượng ba gạch', 'Drag', 'After:\n– Đổi thứ tự cột.'),
       ('Bấm Lưu', 'Click', 'After:\n– Lưu theo người dùng, vẽ lại bảng.')])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu yêu cầu vận chuyển, bốc xếp', usecase=('FR-05', 'Lập phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu yêu cầu vận chuyển, bốc xếp',
       mota='Chọn đơn hàng/hợp đồng và phiếu yêu cầu xuất hàng, nhập thông tin vận chuyển, bốc xếp, số kiện; lưu nháp '
            'hoặc gửi thủ kho duyệt.',
       tacnhan=TN_MOI, dieukien='1. Người dùng đăng nhập thành công.',
       chinh='1. Người dùng bấm Tạo mới.\n2. Hệ thống mở màn “Tạo phiếu yêu cầu vận chuyển, bốc xếp”.\n'
             '3. Người dùng chọn Đơn hàng/Hợp đồng (FR-06) rồi Phiếu YCXH (FR-07).\n'
             '4. Hệ thống điền khách hàng, người liên hệ, số điện thoại, địa điểm giao và bảng hàng.\n'
             '5. Người dùng nhập thời gian vận chuyển, ghi chú, thông tin bốc xếp, số kiện, đính kèm file (tùy chọn).\n'
             '6. Người dùng bấm Lưu nháp hoặc Gửi duyệt.\n'
             '7. Hệ thống kiểm tra, sinh mã, lưu phiếu, ghi nhận trong lịch sử; gửi duyệt thì báo thủ kho.\n'
             '8. Hệ thống báo thành công, quay về màn danh sách.',
       phu='• Lỗi kiểm tra → báo đỏ tại ô, thông báo “Vui lòng kiểm tra lại thông tin đã nhập”.\n'
           '• Bấm Lưu và tiếp tục → lưu nháp rồi mở form trống để lập tiếp.\n'
           '• Đổi Đơn hàng/Hợp đồng → Phiếu YCXH và các thông tin lấy theo YCXH bị xóa.\n'
           '• Rời màn khi có thay đổi chưa lưu → hỏi xác nhận rời trang.',
       dacbiet='Khách hàng, người liên hệ, địa điểm giao, dòng hàng luôn lấy lại từ phiếu YCXH lúc lưu, người dùng chỉ '
               'nhập Số kiện.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'), shot_caption='Màn Tạo phiếu yêu cầu vận chuyển, bốc xếp đã nhập dữ liệu'),
   ui=FORM_UI + [('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
                  'Chỉ ở màn Tạo; lưu nháp rồi mở form trống.')],
   ev=SAVE_EV)

# ------------------------------------------------------------ 2.6
PICK_UI = lambda code_label, extra: [  # noqa: E731
    (code_label, 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Gợi ý “Nhập %s”.' % code_label.lower()),
] + extra + [
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1, 10 dòng', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không chọn.'),
]
fr(6, 'Chọn đơn hàng/hợp đồng', usecase=('FR-06', 'Chọn đơn hàng/hợp đồng', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn đơn hàng/hợp đồng cho phiếu',
       mota='Cửa sổ liệt kê đơn hàng/hợp đồng từ các nguồn: hợp đồng bán, hợp đồng dịch vụ BH-SC, hợp đồng bán đầu kỳ, '
            'hợp đồng mua hàng (ngoài / trong nước), hợp đồng mua dịch vụ, hợp đồng mua đầu kỳ, phiếu xử lý hàng thiếu, '
            'xác nhận bảo hành hãng.',
       tacnhan=TN_MOI, dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo / Sửa phiếu.',
       chinh='1. Người dùng bấm vào ô Đơn hàng/Hợp đồng.\n2. Hệ thống mở cửa sổ “Chọn đơn hàng/hợp đồng”.\n'
             '3. Người dùng tìm theo số, lọc Loại hợp đồng nếu cần, bấm vào dòng.\n4. Hệ thống điền ô và đóng cửa sổ.',
       phu='• Bấm số hợp đồng trên dòng → mở chứng từ ở tab mới, không chọn dòng.\n• Bấm Đóng → không chọn.',
       dacbiet='Hợp đồng bán và hợp đồng BH-SC chỉ lấy hợp đồng còn hiệu lực, cùng công ty người đăng nhập.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('11_contract'), shot_caption='Cửa sổ Chọn đơn hàng/hợp đồng',
               note='Modal Chọn đơn hàng/hợp đồng được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui=PICK_UI('Số đơn hàng/Hợp đồng', [
       ('Loại hợp đồng', 'Dropdown', 'Enable', 'Danh sách loại', 'Không', 'Tất cả', 'Đổi loại → lọc lại ngay.'),
       ('Bảng hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Số đơn hàng/Hợp đồng (link tab mới), Loại hợp đồng, Ngày tạo', '- Mới tạo xếp trên']),
   ]),
   ev=[('Mở cửa sổ', 'System', 'After:\n– Liệt kê đơn hàng/hợp đồng theo nguồn và điều kiện ở mục Yêu cầu đặc biệt.'),
       ('Bấm Tìm kiếm / đổi Loại hợp đồng', 'Change', 'After:\n– Lọc lại, về trang 1.'),
       ('Bấm một dòng', 'Click', 'After:\n– Điền ô Đơn hàng/Hợp đồng; nếu khác hợp đồng cũ thì xóa Phiếu YCXH đã chọn.')])

# ------------------------------------------------------------ 2.7
fr(7, 'Chọn phiếu yêu cầu xuất hàng', usecase=('FR-07', 'Chọn phiếu YCXH', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn phiếu yêu cầu xuất hàng cho phiếu',
       mota='Cửa sổ liệt kê phiếu yêu cầu xuất hàng có thể chọn; chọn xong hệ thống điền thông tin giao hàng và bảng hàng.',
       tacnhan=TN_MOI, dieukien='1. Người dùng đăng nhập thành công.\n2. Đã chọn Đơn hàng/Hợp đồng.',
       chinh='1. Người dùng bấm vào ô Phiếu YCXH.\n2. Hệ thống mở cửa sổ “Chọn phiếu yêu cầu xuất hàng”.\n'
             '3. Người dùng tìm theo mã, bấm vào dòng.\n'
             '4. Hệ thống điền khách hàng, người liên hệ, số điện thoại, địa điểm giao và các dòng hàng có số lượng > 0.',
       phu='• Chưa chọn hợp đồng → “Vui lòng chọn đơn hàng/hợp đồng trước.”, không mở cửa sổ.\n'
           '• Phiếu không còn chọn được → báo lỗi dưới ô Phiếu YCXH, không điền form.\n'
           '• Bấm mã phiếu trên dòng → mở chi tiết YCXH ở tab mới.',
       dacbiet='Chỉ hiện phiếu YCXH trạng thái 1/2/3/10/11 (giống ERP, kể cả Đang tạo) và đã gắn khách hàng.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('12_export_request'), shot_caption='Cửa sổ Chọn phiếu yêu cầu xuất hàng',
               note='Modal Chọn phiếu yêu cầu xuất hàng được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui=PICK_UI('Mã phiếu', [
       ('Bảng phiếu YCXH', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột STT, Mã phiếu (link tab mới), Ngày tạo', '- Mới tạo xếp trên']),
   ]),
   ev=[('Bấm một dòng', 'Click',
        'During:\n– Phiếu không còn chọn được / chưa gắn khách hàng → báo lỗi dưới ô.\n' + ERR + '\n'
        'After:\n– Điền thông tin giao hàng và bảng hàng; đóng cửa sổ.')])

# ------------------------------------------------------------ 2.8
fr(8, 'Chỉnh sửa phiếu', usecase=('FR-08', 'Chỉnh sửa phiếu', 'crud', A_LAP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Chỉnh sửa phiếu yêu cầu vận chuyển, bốc xếp',
       mota='Người lập sửa phiếu Đang tạo hoặc Từ chối, lưu nháp lại hoặc gửi duyệt.',
       tacnhan=TN_SUA,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người lập phiếu.\n'
                '3. Phiếu đang ở trạng thái Đang tạo hoặc Từ chối.',
       chinh='1. Bấm Sửa ở cột Hành động hoặc ở màn chi tiết.\n2. Hệ thống mở màn “Sửa phiếu yêu cầu vận chuyển, bốc xếp: <mã>”.\n'
             '3. Người dùng sửa thông tin (quy tắc như FR-05).\n4. Bấm Lưu nháp hoặc Gửi duyệt.\n'
             '5. Hệ thống lưu, ghi nhận Thay đổi thông tin (và Thay đổi trạng thái khi gửi duyệt) trong lịch sử, quay về danh sách.',
       phu='• Phiếu vừa đổi trạng thái ở nơi khác → “Trạng thái đã bị thay đổi. Vui lòng load lại trang”, chuyển sang màn chi tiết.\n'
           '• Giữ nguyên phiếu YCXH cũ thì không bắt phiếu đó còn chọn được.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('19_edit'), shot_caption='Màn Sửa phiếu yêu cầu vận chuyển, bốc xếp'),
   ui=FORM_UI, ev=SAVE_EV)

# ------------------------------------------------------------ 2.9
fr(9, 'Xóa phiếu', usecase=('FR-09', 'Xóa phiếu', 'action', A_LAP),
   rule=('- Quy tắc Xóa và Thông báo.', 'delete'),
   intro=dict(
       ten='Xóa phiếu yêu cầu vận chuyển, bốc xếp', mota='Người lập xóa hẳn phiếu Đang tạo / Từ chối cùng các dòng hàng.',
       tacnhan=TN_SUA,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người lập.\n3. Phiếu Đang tạo hoặc Từ chối.',
       chinh='1. Bấm Xóa ở cột Hành động hoặc màn chi tiết.\n2. Hệ thống hiện hộp “Xác nhận xóa”.\n3. Bấm Xóa.\n'
             '4. Hệ thống xóa phiếu, ghi nhận Xóa trong lịch sử, báo “Xóa thành công.”.',
       phu='• Bấm Hủy → không xóa.\n• Phiếu vừa đổi trạng thái → “Trạng thái đã bị thay đổi. Vui lòng load lại trang”.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp xác nhận xóa phiếu',
               note='Modal Xác nhận xóa được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nội dung', 'Label', 'Hiển thị', '–', '“Bạn có chắc muốn xóa phiếu yêu cầu vận chuyển \'<mã>\'?”'),
       ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Xác nhận xóa.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.')],
   ev=[('Bấm Xóa', 'Click', 'Before:\n– Kiểm tra người lập và trạng thái.\n' + ERR + '\n'
        'After:\n– Xóa phiếu và dòng hàng; ghi nhận Xóa trong lịch sử; báo “Xóa thành công.”, nạp lại danh sách.')])

# ------------------------------------------------------------ 2.10
fr(10, 'Xem chi tiết phiếu', usecase=('FR-10', 'Xem chi tiết phiếu', 'view', A_LAP),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu yêu cầu vận chuyển, bốc xếp', mota='Xem toàn bộ phiếu ở chế độ chỉ đọc, kèm nút theo quyền.',
       tacnhan=TN_XEM, dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu nằm trong phạm vi xem.',
       chinh='1. Bấm Mã phiếu ở danh sách.\n2. Hệ thống mở màn “Chi tiết phiếu yêu cầu vận chuyển, bốc xếp: <mã>”, tiêu đề '
             'kèm nhãn trạng thái.',
       phu='• Ngoài phạm vi → “Bạn không có quyền xem phiếu này”.', dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn chi tiết phiếu Chờ duyệt (thủ kho)'),
   ui_kw=dict(required=False),
   ui=[
       ('Các ô thông tin vận chuyển và bốc xếp', 'Textbox', 'Read-only', '–', 'Theo dữ liệu',
        'Như màn Tạo; Đơn hàng/Hợp đồng và Phiếu YCXH là liên kết mở tab mới.'),
       ('Người duyệt / Ngày duyệt', 'Textbox', 'Read-only', '–', 'Ẩn', 'Hiện khi phiếu Đã duyệt hoặc Từ chối.'),
       ('Lý do từ chối', 'Textarea', 'Read-only', '–', 'Ẩn', 'Hiện khi phiếu Từ chối.'),
       ('File đính kèm / Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', 'Bấm Xem lịch sử để mở (FR-14).'),
       ('Nút Sửa / Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Người lập, phiếu Đang tạo / Từ chối.'),
       ('Nút Duyệt / Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Thủ kho, phiếu Chờ duyệt.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
   ],
   ev=[('Mở màn chi tiết', 'System', 'Before:\n– Kiểm tra phạm vi xem.\nAfter:\n– Hiển thị dữ liệu và các nút theo điều kiện.')])

# ------------------------------------------------------------ 2.11
fr(11, 'Duyệt phiếu', usecase=('FR-11', 'Duyệt phiếu', 'action', A_TK),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Duyệt phiếu yêu cầu vận chuyển, bốc xếp', mota='Thủ kho đồng ý vận chuyển, bốc xếp theo phiếu.',
       tacnhan=TN_TK,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là thủ kho của kho xuất hàng (hoặc Super admin).\n'
                '3. Phiếu Chờ duyệt.',
       chinh='1. Bấm Duyệt ở màn chi tiết (nút Duyệt trên dòng danh sách mở màn chi tiết).\n2. Hệ thống hỏi “Xác nhận duyệt”.\n'
             '3. Bấm Duyệt.\n4. Hệ thống chuyển phiếu Đã duyệt, ghi người / ngày duyệt; phiếu YCXH đổi hình thức vận chuyển '
             'thành “Công ty vận chuyển”.\n5. Ghi nhận Thay đổi trạng thái trong lịch sử, báo người lập, hiện “Duyệt thành công.”.',
       phu='• Bấm Hủy → không duyệt.\n• Phiếu vừa đổi trạng thái → “Trạng thái đã bị thay đổi. Vui lòng load lại trang”.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết => Duyệt', shot=shot('14_approve'), shot_caption='Hộp xác nhận duyệt',
               note='Modal Xác nhận duyệt được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Nội dung', 'Label', 'Hiển thị', '–', '“Bạn có chắc muốn duyệt phiếu yêu cầu vận chuyển \'<mã>\'?”'),
       ('Nút Duyệt', 'Button', 'Enable', 'Hiển thị', 'Xác nhận duyệt.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp.')],
   ev=[('Bấm Duyệt', 'Click',
        'Before:\n– Kiểm tra thủ kho và trạng thái Chờ duyệt.\nDuring:\n– Kiểm tra phiếu YCXH còn hợp lệ.\n' + ERR + '\n'
        'After:\n– Phiếu Đã duyệt; phiếu YCXH đổi hình thức vận chuyển thành Công ty vận chuyển.\n'
        '– Ghi nhận Thay đổi trạng thái (Chờ duyệt → Đã duyệt).\n– Báo “[YCVC] Đã duyệt” cho người lập; hiện “Duyệt thành công.”.')])

# ------------------------------------------------------------ 2.12
fr(12, 'Từ chối phiếu', usecase=('FR-12', 'Từ chối phiếu', 'action', A_TK),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Từ chối phiếu yêu cầu vận chuyển, bốc xếp', mota='Thủ kho không đồng ý, bắt buộc nhập lý do.',
       tacnhan=TN_TK,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là thủ kho của kho xuất hàng.\n3. Phiếu Chờ duyệt.',
       chinh='1. Bấm Từ chối ở màn chi tiết.\n2. Hệ thống mở cửa sổ “Từ chối phiếu yêu cầu vận chuyển”.\n'
             '3. Nhập Lý do từ chối, bấm Từ chối.\n4. Hệ thống chuyển phiếu Từ chối, lưu lý do, ghi lịch sử, báo người lập, '
             'hiện “Từ chối thành công.”.',
       phu='• Lý do trống → “Bắt buộc phải nhập”.\n• Bấm Hủy → đóng cửa sổ.',
       dacbiet='Phiếu Từ chối, người lập được sửa và gửi duyệt lại.'),
   layout=dict(menu=MENU + ' => Xem chi tiết => Từ chối', shot=shot('15_reject'), shot_caption='Cửa sổ Từ chối phiếu',
               note='Modal Từ chối phiếu yêu cầu vận chuyển được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   ui=[('Tiêu đề', 'Label', 'Hiển thị', '–', '–', '–', '“Từ chối phiếu yêu cầu vận chuyển”, kèm “Phiếu: <mã>”.'),
       ('Lý do từ chối', 'Textarea', 'Enable', '1–5000 ký tự', 'Có', 'Trống',
        ['- Gợi ý “Nhập lý do từ chối”', '- Lỗi: “Bắt buộc phải nhập” / “Vui lòng nhập tối đa 5000 ký tự.”']),
       ('Nút Từ chối', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Màu đỏ; xác nhận từ chối.'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ.')],
   ev=[('Bấm Từ chối', 'Click',
        'Before:\n– Kiểm tra thủ kho và trạng thái.\nDuring:\n– Lý do trống → “Bắt buộc phải nhập”.\n' + ERR + '\n'
        'After:\n– Phiếu Từ chối, lưu lý do, người / ngày duyệt.\n– Ghi nhận Thay đổi trạng thái kèm lý do.\n'
        '– Báo “[YCVC] Từ chối” kèm lý do cho người lập; hiện “Từ chối thành công.”.')])

# ------------------------------------------------------------ 2.13
fr(13, 'Xuất danh sách ra Excel', usecase=('FR-13', 'Xuất Excel', 'io', A_LAP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu ra Excel', mota='Chọn trường, thứ tự cột rồi xuất theo bộ lọc đang áp.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Bấm Xuất Excel.\n2. Hệ thống mở “Chọn trường xuất Excel” (10 trường).\n3. Tích trường, kéo đổi thứ tự, bấm Xuất file.\n'
             '4. Hệ thống tải file “DANH SÁCH PHIẾU YÊU CẦU VẬN CHUYỂN, BỐC XẾP”, báo “Xuất Excel thành công.”.',
       phu='• Không có phiếu khớp → báo “Không có dữ liệu phù hợp.”, không tải file.\n• Bấm Đóng → không xuất.',
       dacbiet='Dữ liệu lớn tải theo từng đợt, hiện tiến độ “Đã tải x/y dòng…”.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Danh sách trường', 'Table/Grid', 'Enable', '10 trường', 'Ít nhất 1', 'Tích tất cả',
        'Mã phiếu, Số hợp đồng/đơn hàng, Khách hàng, Ngày tạo, Người tạo, Ngày cập nhật, Người cập nhật, Ngày duyệt, '
        'Người duyệt, Trạng thái.'),
       ('Nút Chọn tất cả / Bỏ chọn hết / Xuất file / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   ev=[('Bấm Xuất file', 'Click', 'During:\n– Lấy phiếu theo bộ lọc + phạm vi quyền.\n' + ERR + '\n'
        'After:\n– Tải file có logo, tiêu đề, các cột đã chọn; báo “Xuất Excel thành công.”.')])

# ------------------------------------------------------------ 2.14
fr(14, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(ten='Xem lịch sử thay đổi của phiếu',
              mota='Xem các mốc Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa: người thực hiện, thời điểm, giá trị cũ → mới.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Bấm Lịch sử ở cột Hành động, hoặc Xem lịch sử ở khối Lịch sử màn chi tiết.\n2. Hệ thống hiển thị các mốc, mới nhất trên.',
              phu='• Bộ lọc → lọc theo loại hành động, người thực hiện, khoảng ngày.', dacbiet=None),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
       '- Thay đổi thông tin: từng trường cũ → mới, dòng hàng sửa (số kiện), file thêm / bớt',
       '- Thay đổi trạng thái: “Trạng thái: <cũ> → <mới>”; từ chối kèm lý do']),
       ('Nút Bộ lọc / Đóng', 'Button', 'Enable', '–', 'Hiển thị', '–')],
   ev=[('Mở lịch sử', 'Click', 'Before:\n– Kiểm tra quyền xem phiếu.\nAfter:\n– Hiển thị các mốc.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu yêu cầu vận chuyển, bốc xếp; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Dữ liệu lấy theo phiếu YCXH', [
        '– Khách hàng, người liên hệ, số điện thoại, địa điểm giao và dòng hàng (số lượng > 0) lấy từ phiếu YCXH, đọc lại lúc lưu.',
        '– Người dùng chỉ nhập Số kiện từng dòng.', '– Đổi Đơn hàng/Hợp đồng thì xóa phiếu YCXH đã chọn.'],
     ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-02', 'Phiếu YCXH chọn được', [
        '– Trạng thái 1/2/3/10/11 (giống ERP), đã gắn khách hàng.',
        '– Sửa phiếu mà giữ nguyên phiếu YCXH cũ thì không kiểm lại trạng thái.'], ['Chọn phiếu YCXH', 'Lập phiếu', 'Chỉnh sửa']),
    ('BR-03', 'Người duyệt', [
        '– Mọi thủ kho của kho xuất hàng trên phiếu YCXH (và Super admin).',
        '– Gửi duyệt khi kho chưa có thủ kho → chặn.'], ['Lập phiếu', 'Duyệt', 'Từ chối']),
    ('BR-04', 'Vòng đời trạng thái', [
        '– Lưu nháp → Đang tạo; Gửi duyệt → Chờ duyệt.', '– Thủ kho duyệt → Đã duyệt; từ chối (bắt buộc lý do) → Từ chối.',
        '– Sửa / Xóa: người lập, phiếu Đang tạo hoặc Từ chối; gửi lại sau Từ chối thì xóa lý do cũ.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa', 'Duyệt', 'Từ chối']),
    ('BR-05', 'Duyệt cập nhật phiếu YCXH', ['– Duyệt thành công thì phiếu YCXH đổi hình thức vận chuyển thành Công ty vận chuyển.'],
     ['Duyệt']),
    ('BR-06', 'Mã phiếu', ['– <mã công ty>.YCVC<tháng năm>.NNNNN, chạy chung dãy với ERP.'], ['Lập phiếu']),
    ('BR-07', 'Phạm vi xem', [
        '– Theo V1 → V4, không có quyền thì phiếu mình lập.',
        '– Luôn thấy thêm phiếu mình đã duyệt / từ chối và phiếu mình là thủ kho.', '– Phiếu Đang tạo của người khác luôn ẩn.'],
     ['Xem danh sách', 'Xem chi tiết', 'Xuất Excel']),
    ('BR-08', 'Thông báo', ['– Gửi duyệt → mọi thủ kho; Duyệt / Từ chối (kèm lý do) → người lập.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Duyệt', 'Từ chối']),
    ('BR-09', 'Thao tác xong quay về danh sách', ['– Lưu nháp, Gửi duyệt, Xóa thành công đều quay về màn danh sách.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc dữ liệu do màn Phiếu yêu cầu vận chuyển, bốc xếp ghi ra.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Hàng hóa', 'Phiếu yêu cầu xuất hàng — hình thức vận chuyển đổi thành Công ty vận chuyển khi phiếu vận chuyển được duyệt',
     'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => YC xuất hàng'),
], widths=[0.45, 1.0, 2.6, 2.4])

d.save()
print('Đã ghi', OUT)
