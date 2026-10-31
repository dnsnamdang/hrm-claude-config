# -*- coding: utf-8 -*-
"""SRS màn "Phiếu yêu cầu vận chuyển, bốc xếp" (mã {cty}.YCVC{mmyy}.NNNNN) — form chuẩn Danh mục quốc gia (30/10/2026).

Chạy: python gen_srs.py  → SRS - Phiếu yêu cầu vận chuyển, bốc xếp.docx
Khung: srs-documenter (SrsDoc) + checklist ../phieu-theo-form-quoc-gia/CHECKLIST.md. Khuôn thư mục: bank-account-catalog.
Nguồn đọc 30/10/2026 (nhánh develop, cả 2 repo):
  BE  Modules/Finance/{Entities/DeliveryRequest/*, Services/DeliveryRequest{,Write,Notify,Attachment}Service.php,
      Http/Controllers/V1/DeliveryRequestController.php, Http/Requests/DeliveryRequest/*}
  FE  pages/finance/delivery-requests/**, components/subsystem-menu/sale-hub.js
  Spec docs/superpowers/specs/gop-db/2026-10-08-delivery-request-design.md
31/10/2026: nâng chi tiết theo SRS_MAU (bảng giao diện / event Before-During-After đối chiếu code nhánh develop).
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


# Bảng giao diện viết sẵn mỗi đối tượng 1 hàng (31/10/2026) — giữ khung split_ui_rows để chặn dòng gộp.
UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None, figs=None):
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
    for f, cap in (figs or []):
        d.figure(shot(f), cap, width_in=6.2)
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

CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
SYS_ERR = '“Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”'
DK_LAP = '1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Phiếu yêu cầu vận chuyển, bốc xếp.'


def form_ui(edit):
    """Bảng giao diện màn Tạo (edit=False) / Sửa (edit=True) — chung 1 form DeliveryRequestForm."""
    rows = [
        ('Tiêu đề màn', 'Label', 'Hiển thị', '–', '–',
         'Sửa phiếu yêu cầu vận chuyển, bốc xếp: <mã>' if edit else 'Tạo phiếu yêu cầu vận chuyển, bốc xếp',
         ['- Hiện trên thanh tiêu đề và tab trình duyệt',
          '- Kèm nhãn màu trạng thái hiện tại của phiếu (Đang tạo / Từ chối)' if edit else
          '- Phiếu chưa có mã, mã do hệ thống sinh khi lưu']),
        ('Dòng người lập', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', [
            '- Góc phải tiêu đề khối Thông tin vận chuyển: tên người lập và thời điểm lập phiếu',
            '- Lấy theo phiếu đã lưu' if edit else
            '- Phiếu chưa lưu: hiện người đang đăng nhập và thời điểm hiện tại']),
    ]
    if edit:
        rows.append(('Mã phiếu', 'Textbox', 'Read-only', '–', '–', 'Theo dữ liệu',
                     ['- Mã do hệ thống sinh lúc lập, không sửa được']))
    rows += [
        ('Đơn hàng/Hợp đồng', 'Textbox', 'Enable', 'Chọn từ danh sách', 'Có', 'Trống' if not edit else 'Theo dữ liệu', [
            '- Gợi ý “Chọn đơn hàng/hợp đồng...”',
            '- Bấm vào ô → mở cửa sổ Chọn đơn hàng/hợp đồng (mục 2.6)',
            '- Dấu × cuối ô: bỏ chọn, đồng thời xóa Phiếu YCXH, Khách hàng, Người liên hệ, Số ĐT người liên hệ, '
            'Địa điểm giao hàng và bảng Chi tiết',
            '- Bỏ trống khi bấm lưu → viền đỏ, dưới ô “Bắt buộc phải nhập”']),
        ('Phiếu YCXH', 'Textbox', 'Enable', 'Chọn từ danh sách', 'Có', 'Trống' if not edit else 'Theo dữ liệu', [
            '- Gợi ý “Chọn phiếu yêu cầu xuất hàng...”',
            '- Bấm vào ô → mở cửa sổ Chọn phiếu yêu cầu xuất hàng (mục 2.7)',
            '- Chưa chọn Đơn hàng/Hợp đồng: không mở cửa sổ, báo “Vui lòng chọn đơn hàng/hợp đồng trước.”',
            '- Dấu × cuối ô: bỏ chọn, xóa các ô lấy theo phiếu YCXH và bảng Chi tiết, giữ Đơn hàng/Hợp đồng',
            '- Kho xuất hàng của phiếu chưa có thủ kho: dưới ô hiện chữ xám “Kho của phiếu này chưa có thủ kho — '
            'chỉ lưu nháp được, chưa gửi duyệt được.”',
            '- Bỏ trống khi bấm lưu → viền đỏ, dưới ô “Bắt buộc phải nhập”']),
        ('Khách hàng', 'Textbox', 'Read-only', '–', '–', 'Gợi ý “Lấy theo phiếu YCXH”',
         ['- Dạng “Mã - Tên khách hàng” của phiếu YCXH', '- Tự điền khi chọn phiếu YCXH, không nhập tay']),
        ('Người liên hệ', 'Textbox', 'Read-only', '–', '–', 'Gợi ý “Lấy theo phiếu YCXH”',
         ['- Người liên hệ ghi trên phiếu YCXH', '- Tự điền, không nhập tay']),
        ('Số ĐT người liên hệ', 'Textbox', 'Read-only', '–', '–', 'Gợi ý “Lấy theo phiếu YCXH”',
         ['- Số điện thoại người liên hệ trên phiếu YCXH', '- Tự điền, không nhập tay']),
        ('Địa điểm giao hàng', 'Textbox', 'Read-only', '–', '–', 'Gợi ý “Lấy theo phiếu YCXH”',
         ['- Địa điểm giao ghi trên phiếu YCXH', '- Tự điền, không nhập tay']),
        ('Thời gian vận chuyển', 'Datepicker', 'Enable', 'dd/mm/yyyy hh:mm', 'Không', 'Trống',
         ['- Gợi ý “Chọn thời gian vận chuyển”', '- Chọn ngày và giờ phút']),
        ('Ghi chú', 'Textarea', 'Enable', '0–5000 ký tự', 'Không', 'Trống',
         ['- Gợi ý “Nhập ghi chú”', '- Quá 5000 ký tự → dưới ô “Vui lòng nhập tối đa 5000 ký tự.”']),
    ]
    if edit:
        rows.append(('Lý do từ chối', 'Textarea', 'Read-only', '–', '–', 'Ẩn', [
            '- Chỉ hiện khi phiếu đang ở trạng thái Từ chối: lý do thủ kho đã nhập',
            '- Gửi duyệt lại thì lý do cũ bị xóa']))
    rows += [
        ('Tổng số kiện', 'Textbox', 'Enable', 'Số nguyên 0–2147483647', 'Không', 'Trống', [
            '- Gợi ý “Nhập tổng số kiện”', '- Chỉ nhận chữ số, ký tự khác bị bỏ ngay khi gõ',
            '- Không phải số nguyên → “Vui lòng nhập số nguyên.”',
            '- Vượt giới hạn → “Giá trị nhập vào không được vượt quá 2147483647.”']),
        ('Phương thức bốc xếp', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         ['- Gợi ý “Nhập phương thức bốc xếp”', '- Ô không cho gõ quá 255 ký tự']),
        ('Địa điểm bốc xếp', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         ['- Gợi ý “Nhập địa điểm bốc xếp”', '- Ô không cho gõ quá 255 ký tự']),
        ('Thời gian bốc xếp', 'Datepicker', 'Enable', 'dd/mm/yyyy hh:mm', 'Không', 'Trống',
         ['- Gợi ý “Chọn thời gian bốc xếp”', '- Chọn ngày và giờ phút']),
        ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, xlsx, xls, jpeg, jpg, png; tối đa 20 MB / file', 'Không',
         'Theo dữ liệu' if edit else 'Chưa có file', [
             '- Cột STT, Upload / File, Dung lượng',
             '- Mỗi file có icon Xem trước (ảnh, pdf…), Tải xuống; file chưa lưu có thêm icon Thay đổi']),
        ('Nút Thêm tài liệu', 'Button', 'Enable', '–', '–', 'Hiển thị', [
            '- Thêm 1 dòng trống có nút Chọn tệp',
            '- Rê chuột hiện “Chấp nhận pdf, xlsx, xls, jpeg, jpg, png — tối đa 20MB/file”']),
        ('Nút Chọn tệp', 'Button', 'Enable', '–', '–', 'Hiển thị', [
            '- Chọn file → tải lên ngay, trong lúc tải hiện “Đang tải lên <tên file>...”',
            '- Sai đuôi → “File \"<tên file>\" không thuộc định dạng cho phép”',
            '- Quá dung lượng → “File \"<tên file>\" vượt quá 20MB”']),
        ('Icon Xóa file', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
         ['- File chưa lưu: bỏ khỏi danh sách ngay',
          '- File đã lưu: hỏi “Bạn có chắc muốn xóa file đính kèm này?”; đồng ý thì xóa ngay, báo “Xóa file thành công”']
         if edit else ['- Bỏ file / dòng trống khỏi danh sách']),
        ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Có', 'Theo dữ liệu' if edit else '“Không có dữ liệu”', [
            '- Cột STT, Tên hàng, Model, Mã hàng hóa, ĐVT, Số lượng: chép từ các dòng hàng có số lượng > 0 của phiếu YCXH',
            '- Chưa có dòng nào: giữa bảng hiện “Không có dữ liệu”',
            '- Đã chọn phiếu YCXH mà bảng trống, bấm lưu → dưới bảng “Bắt buộc phải nhập”']),
        ('Cột Số kiện', 'Textbox', 'Enable', 'Số nguyên 0–2147483647', 'Không', 'Trống' if not edit else 'Theo dữ liệu', [
            '- Ô nhập trên từng dòng hàng, gợi ý “Nhập số kiện”', '- Chỉ nhận chữ số',
            '- Lỗi dưới ô: “Vui lòng nhập số nguyên.” / “Giá trị nhập vào không được vượt quá 2147483647.”']),
        ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         ['- Lưu phiếu ở trạng thái Đang tạo', '- Khóa trong lúc đang lưu']),
        ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
         ['- Lưu phiếu ở trạng thái Chờ duyệt và báo cho thủ kho', '- Không hỏi xác nhận', '- Khóa trong lúc đang lưu']),
    ]
    if not edit:
        rows.append(('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
                     ['- Chỉ có ở màn Tạo', '- Lưu nháp phiếu này rồi mở lại form trống để lập phiếu mới']))
    rows += [
        ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Về màn danh sách', '- Có thay đổi chưa lưu → hiện hộp Thông tin chưa lưu']),
        ('Hộp Thông tin chưa lưu', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', [
            '- Tiêu đề “Thông tin chưa lưu”', '- Nội dung “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”',
            '- Nút Thoát: bỏ thay đổi, rời màn', '- Nút Ở lại: đóng hộp, giữ nguyên dữ liệu đang nhập']),
        ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
            '- Ô lỗi viền đỏ, chữ đỏ ngay dưới ô; chỉ hiện sau lần bấm lưu đầu tiên',
            '- Kèm thông báo góc màn hình “Vui lòng kiểm tra lại thông tin đã nhập”, màn tự cuộn tới ô lỗi đầu tiên']),
        ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
            '- Lưu nháp: “Cập nhật thành công.”' if edit else '- Lưu nháp: “Thêm mới thành công.”',
            '- Gửi duyệt: “Gửi duyệt thành công.”',
            '- Lỗi hệ thống: ' + SYS_ERR]),
    ]
    return rows


FIELD_EV = [
    ('Bấm vào ô Đơn hàng/Hợp đồng', 'Click',
     'Before:\n– Ô đang ở chế độ nhập (màn Tạo / Sửa).\n'
     'After:\n– Mở cửa sổ Chọn đơn hàng/hợp đồng (mục 2.6).'),
    ('Chọn đơn hàng/hợp đồng khác', 'Change',
     'Before:\n– So với đơn hàng/hợp đồng đang chọn.\n'
     'During:\n– Khác hợp đồng cũ → xóa Phiếu YCXH, Khách hàng, Người liên hệ, Số ĐT, Địa điểm giao và bảng Chi tiết; '
     'bỏ ghi chú thủ kho dưới ô Phiếu YCXH.\n'
     'After:\n– Ô Đơn hàng/Hợp đồng hiện số vừa chọn; lỗi cũ dưới ô bị xóa.'),
    ('Bấm dấu × ô Đơn hàng/Hợp đồng', 'Click',
     'Before:\n– Ô đang có đơn hàng/hợp đồng (dấu × chỉ hiện khi ô có giá trị).\n'
     'After:\n– Bỏ chọn đơn hàng/hợp đồng; xóa luôn Phiếu YCXH, các ô lấy theo phiếu YCXH và bảng Chi tiết.'),
    ('Bấm vào ô Phiếu YCXH', 'Click',
     'Before:\n– Kiểm tra đã chọn Đơn hàng/Hợp đồng; chưa chọn → báo “Vui lòng chọn đơn hàng/hợp đồng trước.”, '
     'không mở cửa sổ và dừng xử lý.\n'
     'After:\n– Mở cửa sổ Chọn phiếu yêu cầu xuất hàng (mục 2.7).'),
    ('Bấm dấu × ô Phiếu YCXH', 'Click',
     'Before:\n– Ô đang có phiếu YCXH (dấu × chỉ hiện khi ô có giá trị).\n'
     'After:\n– Bỏ chọn phiếu YCXH; xóa Khách hàng, Người liên hệ, Số ĐT, Địa điểm giao và bảng Chi tiết; giữ Đơn hàng/Hợp đồng.'),
    ('Nhập Tổng số kiện / Số kiện', 'Change',
     'Before:\n– Ô đang ở chế độ nhập (màn Tạo / Sửa).\n'
     'During:\n– Bỏ ngay ký tự không phải chữ số.\n'
     'After:\n– Ghi nhận giá trị; lỗi cũ dưới ô của dòng đó bị xóa.'),
    ('Bấm Chọn tệp ở khối File đính kèm', 'Click',
     'Before:\n– Kiểm tra đuôi file thuộc pdf, xlsx, xls, jpeg, jpg, png và dung lượng ≤ 20MB.\n'
     'During:\n– Sai đuôi → “File \"<tên file>\" không thuộc định dạng cho phép”; quá dung lượng → “File \"<tên file>\" '
     'vượt quá 20MB”; tải lên lỗi → “Tải lên thất bại: <tên file>”.\n' + ERR + '\n'
     'After:\n– File được tải lên ngay, hiện tên file và dung lượng; file chỉ gắn vào phiếu khi bấm lưu.'),
]


def save_ev(edit, draft):
    """Event Lưu nháp (draft=True) / Gửi duyệt (draft=False) của màn Tạo / Sửa."""
    if edit:
        before = ('Before:\n– Kiểm tra người lập phiếu: người khác → “Bạn không có quyền sửa phiếu này” và dừng xử lý.\n'
                  '– Kiểm tra phiếu còn ở trạng thái Đang tạo hoặc Từ chối; đã đổi trạng thái → ' + CONFLICT +
                  ', chuyển sang màn Chi tiết phiếu và dừng xử lý.\n'
                  '– Chặn bấm lặp trong lúc đang lưu.\n')
    else:
        before = ('Before:\n– Không kiểm tra quyền riêng: mọi người dùng đã đăng nhập đều lập được phiếu.\n'
                  '– Chặn bấm lặp trong lúc đang lưu.\n')
    during = ('During:\n– Đơn hàng/Hợp đồng trống → “Bắt buộc phải nhập”.\n'
              '– Phiếu YCXH trống → “Bắt buộc phải nhập”.\n'
              '– Đã chọn phiếu YCXH mà bảng Chi tiết trống → “Bắt buộc phải nhập” dưới bảng.\n'
              '– Có lỗi ở trên → thông báo “Vui lòng kiểm tra lại thông tin đã nhập”, cuộn tới ô lỗi đầu tiên, không gửi lên máy chủ.\n')
    if edit:
        during += ('– Đổi sang phiếu YCXH khác mà phiếu đó không còn chọn được → “Phiếu này không còn chọn được, vui lòng '
                   'chọn phiếu khác.” (giữ nguyên phiếu YCXH cũ thì không kiểm lại).\n')
    else:
        during += '– Phiếu YCXH không còn ở trạng thái chọn được → “Phiếu này không còn chọn được, vui lòng chọn phiếu khác.”\n'
    during += ('– Phiếu YCXH chưa gắn khách hàng → “Phiếu chưa gắn khách hàng, vui lòng chọn phiếu khác.”\n'
               '– Đơn hàng/hợp đồng không còn → “Đơn hàng/hợp đồng không tồn tại, vui lòng chọn lại.”\n'
               '– Dòng hàng không thuộc phiếu YCXH → “Không thuộc phiếu yêu cầu xuất hàng đã chọn, vui lòng chọn lại phiếu.”\n'
               '– Ghi chú quá 5000 ký tự → “Vui lòng nhập tối đa 5000 ký tự.”; Phương thức / Địa điểm bốc xếp quá 255 ký tự → '
               '“Vui lòng nhập tối đa 255 ký tự.”\n'
               '– Tổng số kiện / Số kiện không phải số nguyên → “Vui lòng nhập số nguyên.”; vượt giới hạn → “Giá trị nhập vào '
               'không được vượt quá 2147483647.”\n'
               '– Thời gian vận chuyển / bốc xếp sai định dạng → “Không hợp lệ”.\n')
    if not draft:
        during += '– Kho xuất hàng của phiếu YCXH chưa có thủ kho → “Kho xuất hàng chưa có thủ kho, chưa gửi duyệt được.” dưới ô Phiếu YCXH.\n'
    during += ERR + '\n'
    after = ('After:\n– Khách hàng, người liên hệ, số điện thoại, địa điểm giao và các dòng hàng được đọc lại từ phiếu YCXH lúc '
             'lưu (BR-01); người dùng chỉ quyết Số kiện.\n')
    if not edit:
        after += ('– Sinh mã <mã công ty>.YCVC<tháng năm>.NNNNN (BR-08); công ty, phòng ban, bộ phận lấy theo người lập.\n')
    after += '– Lưu phiếu ở trạng thái %s; gắn các file vừa tải lên.\n' % ('Đang tạo' if draft else 'Chờ duyệt')
    if not draft and edit:
        after += '– Gửi lại sau khi bị từ chối: xóa lý do từ chối, người duyệt, ngày duyệt cũ.\n'
    if edit:
        after += ('– Ghi nhận hành động “Thay đổi thông tin” trong lịch sử của phiếu (từng trường cũ → mới, dòng hàng đổi '
                  'Số kiện, file thêm / bớt); trạng thái đổi thì ghi thêm “Thay đổi trạng thái” (<cũ> → %s).\n'
                  % ('Đang tạo' if draft else 'Chờ duyệt'))
    else:
        after += '– Ghi nhận hành động “Tạo mới” trong lịch sử của phiếu.\n'
    if not draft:
        after += ('– Gửi thông báo cho mọi thủ kho của kho xuất hàng: “[YCVC] Chờ duyệt: <mã phiếu>. KH: … Phiếu xuất: … '
                  'Ngày giao: … Nơi giao: … Người lập: … Ghi chú: …”.\n')
    msg = ('“Gửi duyệt thành công.”' if not draft else ('“Cập nhật thành công.”' if edit else '“Thêm mới thành công.”'))
    after += '– Hiển thị thông báo %s, quay về màn danh sách.' % msg
    name = 'Bấm Lưu nháp' if draft else 'Bấm Gửi duyệt'
    return (name, 'Click', before + during + after)


LEAVE_EV = ('Bấm Quay lại / rời màn', 'Click',
            'Before:\n– So dữ liệu đang nhập với lúc mở màn.\n'
            'During:\n– Có thay đổi chưa lưu → hiện hộp “Thông tin chưa lưu”; tải lại / đóng tab trình duyệt thì trình duyệt '
            'hỏi xác nhận rời trang.\n'
            'After:\n– Bấm Thoát → bỏ thay đổi, về màn danh sách; bấm Ở lại → giữ nguyên màn.\n'
            '– Không có thay đổi → về màn danh sách ngay.')

PICK_CLOSE = ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
              'Before:\n– Cửa sổ chỉ để chọn, không có dữ liệu nhập cần giữ.\n'
              'After:\n– Đóng cửa sổ, không thay đổi ô đang chọn trên form; mở lại thì ô tìm và bộ lọc về trống.')


def pick_ui(title, code_label, extra, empty, code_desc):
    """Bảng giao diện popup chọn bản ghi (RecordPickerModal)."""
    return [
        ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', title, ['- Kèm icon tròn bên trái tiêu đề']),
        ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', ['- Góc phải tiêu đề; đóng cửa sổ, không chọn']),
        ('Ô ' + code_label, 'Textbox', 'Enable', 'Chuỗi ký tự', 'Không', 'Trống', [
            '- Gợi ý “Nhập %s”' % code_label.lower(), '- Tìm gần đúng theo %s' % code_desc,
            '- Nhấn Enter = bấm Tìm kiếm']),
    ] + extra + [
        ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Áp điều kiện tìm, về trang 1']),
        ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
         ['- Xóa ô tìm' + (' và Loại hợp đồng' if extra else '') + ', bỏ sắp xếp, nạp lại từ trang 1']),
        ('Bảng kết quả', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', [
            '- Mặc định xếp ngày tạo mới → cũ', '- Rê chuột lên dòng: nền xanh nhạt',
            '- Bấm vào dòng → chọn bản ghi đó, cửa sổ tự đóng']),
        ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Số thứ tự liên tục qua các trang']),
        ('Cột ' + code_label, 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', [
            '- Là liên kết: bấm mở chứng từ ở tab mới, KHÔNG chọn dòng', '- Sắp xếp được']),
    ]


def pick_tail(empty):
    return [
        ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', '–', 'Theo dữ liệu', ['- Sắp xếp được']),
        ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', '–', 'Theo kết quả', [
            '- a–b: thứ tự dòng đầu–cuối của trang; N: tổng bản ghi khớp điều kiện tìm',
            '- N = 0: hiện “Không có mục nào.”']),
        ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', '10', [
            '- Mặc định: 10', '- Lựa chọn: 10, 20, 50, 100', '- Đổi giá trị → về trang 1']),
        ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1', ['- Nút về đầu, lùi, số trang, tiến, về cuối']),
        ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', ['- Hiện “%s” giữa bảng khi không có kết quả' % empty]),
        ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Đóng cửa sổ, không chọn']),
        ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
         ['- Lỗi khi nạp danh sách → “Lỗi khi tải dữ liệu”, bảng trống']),
    ]


PICK_COMMON_EV = [
    ('Bấm Tìm kiếm / nhấn Enter ở ô tìm', 'Click',
     'Before:\n– Giữ Loại hợp đồng (nếu có) và số dòng/trang đang chọn.\n'
     'After:\n– Tìm gần đúng theo nội dung ô tìm, về trang 1.'),
    ('Bấm Làm mới', 'Click',
     'Before:\n– Không cần điều kiện.\n'
     'After:\n– Xóa điều kiện tìm, bỏ sắp xếp, nạp lại từ trang 1.'),
    ('Bấm tiêu đề cột sắp xếp được', 'Click',
     'Before:\n– Chỉ cột mã / số chứng từ và cột Ngày tạo sắp xếp được; giữ điều kiện tìm.\n'
     'After:\n– Lần đầu xếp tăng dần, bấm lại đổi giảm dần; về trang 1.'),
    ('Đổi trang / Số dòng/trang', 'Click',
     'Before:\n– Giữ điều kiện tìm và thứ tự sắp xếp.\n'
     'After:\n– Nạp dữ liệu trang mới; đổi số dòng/trang thì về trang 1.'),
    ('Bấm liên kết mã / số chứng từ trên dòng', 'Click',
     'Before:\n– Bấm đúng vào chữ liên kết.\n'
     'After:\n– Mở chứng từ ở tab mới; dòng không bị chọn, cửa sổ vẫn mở.'),
]

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu yêu cầu vận chuyển, bốc xếp',
       mota='Hiển thị các phiếu yêu cầu vận chuyển, bốc xếp nằm trong phạm vi dữ liệu của người đăng nhập để theo dõi '
            'việc đề nghị thủ kho bố trí vận chuyển, bốc xếp hàng theo phiếu yêu cầu xuất hàng. Bảng có phân trang, sắp '
            'xếp, tổng số phiếu khớp bộ lọc và các thao tác theo từng dòng (Sửa, Xóa, Duyệt, Lịch sử).',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng để vào màn; phạm vi dữ liệu theo quyền V1–V4 '
                '(Phần 2), không có quyền nào thì thấy phiếu mình lập.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem theo thứ tự V1 → V2 → V3 → V4; không có cấp nào thì giới hạn ở phiếu do '
             'chính người dùng lập.\n'
             '3. Hệ thống cộng thêm phiếu người dùng đã duyệt / từ chối và phiếu thuộc kho người dùng là thủ kho; loại bỏ '
             'phiếu Đang tạo của người khác.\n'
             '4. Hệ thống áp cấu hình cột đã lưu của người dùng, khôi phục bộ lọc nếu vừa rời sang màn Tạo / Sửa / Chi '
             'tiết trong vòng 10 phút.\n'
             '5. Hệ thống trả trang 1, 10 dòng, phiếu lập gần nhất lên trước, kèm dòng “Hiển thị a–b / N”.',
       phu='• Không có phiếu nào → giữa bảng hiện “Không có dữ liệu phù hợp.”, dưới bảng “Không có phiếu nào.”.\n'
           '• Phiếu Đang tạo của người khác không bao giờ hiện, kể cả với người có quyền V1.\n'
           '• Thủ kho không giữ quyền xem nào vẫn thấy phiếu thuộc kho mình để duyệt.\n'
           '• Lỗi hệ thống khi nạp → thông báo ' + SYS_ERR + ', bảng giữ trống.\n'
           '• Phiên đăng nhập hết hạn → hệ thống chuyển về màn đăng nhập.',
       dacbiet=None),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Phiếu yêu cầu vận chuyển, bốc xếp'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Phiếu yêu cầu vận chuyển, bốc xếp',
        ['- Hiện trên thanh tiêu đề trang và đầu bảng']),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Không gắn quyền: mọi người vào được màn đều thấy', '- Bấm → mở màn Tạo phiếu (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', [
           '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.13)',
           '- Khóa trong lúc đang xuất; bên trái nút hiện tiến độ “Đã tải x/y dòng…” rồi “Đang dựng file x/y dòng…”']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        ['- Icon cột, rê chuột hiện “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tùy chỉnh cột (mục 2.4)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
        ['- Đánh số liên tục qua các trang', '- Cột khóa trong Tùy chỉnh cột, ghim bên trái khi cuộn ngang']),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Dạng <mã công ty>.YCVC<tháng năm>.NNNNN, ví dụ TPE.YCVC1026.00004',
           '- Bấm mã → mở màn Chi tiết phiếu (mục 2.10); chuột phải mở được ở tab mới',
           '- Sắp xếp được', '- Cột khóa, ghim bên trái']),
       ('Cột Số hợp đồng/đơn hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Số đơn hàng/hợp đồng đã chọn trên phiếu',
           '- Bấm số → mở chứng từ ở tab mới: loại đã có màn trên HRM mở màn HRM, loại chưa có mở màn ERP',
           '- Loại chứng từ không xác định được: hiện chữ thường, không bấm được', '- Sắp xếp được']),
       ('Cột Phiếu YCXH', 'Table/Grid', 'Read-only', '–', 'Ẩn', [
           '- Mã phiếu yêu cầu xuất hàng của phiếu',
           '- Bấm mã → mở chi tiết phiếu yêu cầu xuất hàng ở tab mới (quyền xem do màn đó tự xét)',
           '- Mặc định ẩn, bật trong Tùy chỉnh cột', '- Không sắp xếp']),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Dạng “Mã - Tên khách hàng”, lấy theo phiếu YCXH lúc lưu', '- Tự xuống dòng khi dài', '- Sắp xếp được']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', [
           '- Thời điểm lập phiếu', '- Sắp xếp được; khi chưa chọn sắp xếp, danh sách xếp theo cột này giảm dần']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Người lập phiếu, dạng “Họ tên - Mã phòng ban”', '- Không sắp xếp']),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        ['- Thời điểm thao tác ghi gần nhất (lưu, gửi duyệt, duyệt, từ chối)', '- Sắp xếp được']),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Người thao tác ghi gần nhất, kể cả thủ kho duyệt / từ chối', '- Dạng “Họ tên - Mã phòng ban”',
           '- Không sắp xếp']),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', [
           '- Thời điểm thủ kho duyệt hoặc từ chối',
           '- Trống khi phiếu chưa được xử lý; gửi duyệt lại sau Từ chối thì trống lại', '- Sắp xếp được']),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Họ tên thủ kho đã duyệt / từ chối', '- Trống khi phiếu chưa được xử lý', '- Không sắp xếp']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 4 giá trị', 'Theo dữ liệu', [
           '- Nhãn màu theo trạng thái:', '- Đang tạo: xám', '- Chờ duyệt: cam', '- Đã duyệt: xanh lá', '- Từ chối: đỏ',
           '- Không sắp xếp']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo điều kiện từng dòng', [
           '- Icon Sửa (bút): chỉ hiện với người lập, phiếu Đang tạo / Từ chối; bấm → mở màn Sửa (mục 2.8)',
           '- Icon Xóa (thùng rác đỏ): cùng điều kiện; bấm → hộp Xác nhận xóa (mục 2.9)',
           '- Icon Duyệt: chỉ hiện với thủ kho của kho xuất hàng (hoặc Super admin), phiếu Chờ duyệt; bấm → mở màn '
           'Chi tiết để duyệt / từ chối (mục 2.11, 2.12)',
           '- Icon Lịch sử: luôn hiện; bấm → cửa sổ Lịch sử thay đổi (mục 2.14)',
           '- Không dùng được thì icon ẩn hẳn; cột khóa trong Tùy chỉnh cột']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả', [
           '- a–b: thứ tự dòng đầu–cuối của trang đang xem',
           '- N: tổng phiếu khớp bộ lọc trong phạm vi quyền, không phải tổng toàn hệ thống',
           '- N = 0: hiện “Không có phiếu nào.”']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', '10', [
           '- Mặc định: 10', '- Lựa chọn: 5, 10, 20, 50, 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', ['- Nút về đầu, lùi, số trang, tiến, về cuối']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- Hiện “Không có dữ liệu phù hợp.” giữa bảng khi không có phiếu nào']),
       ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- Lỗi hệ thống khi nạp → ' + SYS_ERR]),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định cấp quyền xem theo thứ tự V1 → V2 → V3 → V4; không có cấp nào thì giới hạn ở phiếu do '
        'chính người dùng lập.\n– Nạp cấu hình cột đã lưu; khôi phục bộ lọc nếu vừa rời sang màn Tạo / Sửa / Chi tiết '
        'trong vòng 10 phút.\n'
        'During:\n– Cộng thêm phiếu người dùng đã duyệt / từ chối và phiếu thuộc kho người dùng là thủ kho (BR-09).\n'
        '– Loại bỏ phiếu Đang tạo của người khác.\n– Lỗi hệ thống → thông báo ' + SYS_ERR + '.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, ngày tạo giảm dần, kèm “Hiển thị a–b / N”; icon Sửa / Xóa / Duyệt hiện theo '
        'điều kiện từng dòng.'),
       ('Bấm Mã phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem của người dùng.\n– Lưu lại bộ lọc đang dùng để khôi phục khi quay lại.\n'
        'After:\n– Mở màn Chi tiết phiếu (mục 2.10); chuột phải cho phép mở ở tab mới.'),
       ('Bấm Số hợp đồng/đơn hàng', 'Click',
        'Before:\n– Xác định loại chứng từ của phiếu; loại không xác định được thì số hiện chữ thường, không bấm được.\n'
        'After:\n– Mở chứng từ ở tab mới (màn HRM nếu đã có, ngược lại mở màn ERP); màn danh sách giữ nguyên.'),
       ('Bấm mã Phiếu YCXH', 'Click',
        'Before:\n– Cột Phiếu YCXH đã được bật trong Tùy chỉnh cột.\n'
        'After:\n– Mở chi tiết phiếu yêu cầu xuất hàng ở tab mới; quyền xem do màn đó xét.'),
       ('Bấm tiêu đề cột sắp xếp được', 'Click',
        'Before:\n– Chỉ 6 cột Mã phiếu, Số hợp đồng/đơn hàng, Khách hàng, Ngày tạo, Ngày cập nhật, Ngày duyệt sắp xếp được.\n'
        '– Giữ nguyên bộ lọc đang áp.\n'
        'After:\n– Lần đầu xếp tăng dần, bấm lại đổi giảm dần; về trang 1 và nạp lại danh sách.'),
       ('Bấm số trang / nút tiến lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp.\n'
        'After:\n– Nạp dữ liệu trang mới; số thứ tự chạy tiếp theo trang.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\n'
        'After:\n– Về trang 1, nạp lại theo số dòng mới.'),
       ('Bấm icon Duyệt trên dòng', 'Click',
        'Before:\n– Icon chỉ hiện với thủ kho của kho xuất hàng (hoặc Super admin) khi phiếu Chờ duyệt.\n'
        'After:\n– Mở màn Chi tiết phiếu; việc duyệt / từ chối thực hiện ở đó (mục 2.11, 2.12), không duyệt thẳng từ danh sách.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu',
       mota='Thu hẹp danh sách theo mã phiếu / số hợp đồng / mã phiếu YCXH ở ô tìm nhanh và các tiêu chí khách hàng, '
            'hợp đồng, người tạo, trạng thái, ngày tạo, công ty – phòng ban – bộ phận. Kết quả luôn nằm trong phạm vi '
            'dữ liệu của người đăng nhập.',
       tacnhan=TN_XEM, dieukien=DK_XEM + '\n3. Ô Công ty / Phòng ban / Bộ phận chỉ hiện theo cấp quyền xem.',
       chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh rồi nhấn Enter hoặc bấm Tìm kiếm.\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối tiêu chí, chọn / nhập giá trị.\n'
             '3. Ô chọn (Khách hàng, Người tạo, Trạng thái, Ngày tạo, Công ty, Phòng ban, Bộ phận) lọc ngay khi đổi; ô gõ '
             'tay Hợp đồng chỉ lọc khi nhấn Enter hoặc bấm Tìm kiếm.\n'
             '4. Hệ thống nạp lại danh sách từ trang 1 và ghi nhớ bộ lọc.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → giữa bảng “Không có dữ liệu phù hợp.”.\n'
           '• Đổi Công ty → xóa Phòng ban, Bộ phận đang chọn; đổi Phòng ban → xóa Bộ phận.\n'
           '• Ô Khách hàng gõ dưới 2 ký tự → chưa gợi ý.\n'
           '• Tiêu chí bị tắt trong Cài đặt bộ lọc → không hiện ở khối tìm kiếm nâng cao.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách ở trạng thái mở'),
   ui=[
       ('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', 'Bộ lọc danh sách', ['- Kèm icon phễu bên trái']),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Chuỗi ký tự', 'Không', 'Trống', [
           '- Gợi ý “Tìm theo mã phiếu, số hợp đồng, mã phiếu YCXH...”',
           '- Tìm gần đúng đồng thời trên mã phiếu, số hợp đồng/đơn hàng, mã phiếu YCXH',
           '- Chỉ lọc khi nhấn Enter hoặc bấm Tìm kiếm', '- Dấu × cuối ô: xóa nhanh nội dung đã gõ']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Áp ô tìm nhanh và ô Hợp đồng, về trang 1']),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị', [
           '- Mở / thu gọn khối tiêu chí', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”',
           '- Trạng thái mở / thu gọn được ghi nhớ cùng bộ lọc']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Mở cửa sổ Cài đặt bộ lọc (mục 2.3)']),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống', [
           '- Chỉ hiện với người có quyền V1 (hoặc Super admin)', '- Mặc định: trống (mọi công ty)',
           '- Đổi giá trị → xóa Phòng ban, Bộ phận đang chọn, lọc ngay']),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Không', 'Trống', [
           '- Hiện với V1, V2, V3', '- Chỉ liệt kê phòng ban của Công ty đang chọn', '- Mặc định: trống',
           '- Đổi giá trị → xóa Bộ phận đang chọn, lọc ngay']),
       ('Bộ phận', 'Dropdown', 'Enable / Disable', 'Danh sách bộ phận', 'Không', 'Trống', [
           '- Mở cho V1, V2, V4; còn lại bị khóa', '- Chỉ liệt kê bộ phận của Phòng ban đang chọn', '- Mặc định: trống']),
       ('Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng', 'Không', 'Trống', [
           '- Gợi ý “Gõ để tìm khách hàng...”', '- Gõ tối thiểu 2 ký tự mới gợi ý; tìm theo mã hoặc tên',
           '- Tối đa 20 gợi ý, dạng “Mã - Tên”; chỉ liệt kê khách hàng, không có nhà cung cấp',
           '- Chọn xong lọc ngay']),
       ('Hợp đồng', 'Textbox', 'Enable', 'Chuỗi ký tự', 'Không', 'Trống', [
           '- Gợi ý “Nhập số hợp đồng/đơn hàng”', '- Tìm gần đúng theo số đơn hàng/hợp đồng của phiếu',
           '- Chỉ lọc khi nhấn Enter hoặc bấm Tìm kiếm']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống (mọi người tạo)', '- Chọn 1 nhân viên đã lập phiếu, lọc ngay']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống', [
           '- Mặc định: trống (mọi trạng thái)', '- Lựa chọn:', '- Đang tạo', '- Chờ duyệt', '- Đã duyệt', '- Từ chối',
           '- Chọn xong lọc ngay']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', [
           '- Chọn khoảng từ ngày → đến ngày trong cùng 1 ô',
           '- Lấy trọn ngày biên: phiếu lập trong chính ngày đầu / ngày cuối vẫn nằm trong kết quả']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Không có phiếu khớp → giữa bảng “Không có dữ liệu phù hợp.”']),
   ],
   ev=[
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Không cần điều kiện.\n'
        'After:\n– Mở / thu gọn khối tiêu chí, nhãn nút đổi tương ứng; trạng thái được ghi nhớ cùng bộ lọc.'),
       ('Nhập ô tìm nhanh rồi nhấn Enter / bấm Tìm kiếm', 'Click',
        'Before:\n– Gõ chữ ở ô tìm nhanh chưa lọc ngay.\n'
        'During:\n– Tìm gần đúng trên mã phiếu, số hợp đồng/đơn hàng, mã phiếu YCXH, trong phạm vi quyền.\n'
        'After:\n– Về trang 1, nạp lại danh sách theo mọi tiêu chí đang có.'),
       ('Nhập ô Hợp đồng rồi nhấn Enter', 'Change',
        'Before:\n– Gõ chữ chưa lọc ngay.\n'
        'After:\n– Lọc gần đúng theo số đơn hàng/hợp đồng, về trang 1.'),
       ('Đổi ô chọn (Khách hàng, Người tạo, Trạng thái, Ngày tạo)', 'Change',
        'Before:\n– So với giá trị trước đó; không đổi thì không nạp lại.\n'
        'After:\n– Về trang 1, nạp lại danh sách ngay; ghi nhớ bộ lọc.'),
       ('Đổi Công ty', 'Change',
        'Before:\n– Ô chỉ hiện với V1 / Super admin.\n'
        'During:\n– Xóa giá trị Phòng ban và Bộ phận đang chọn.\n'
        'After:\n– Nạp danh sách phòng ban theo công ty mới và nạp lại danh sách phiếu.'),
       ('Đổi Phòng ban', 'Change',
        'Before:\n– Ô chỉ hiện với V1, V2, V3; danh sách theo Công ty đang chọn.\n'
        'During:\n– Xóa giá trị Bộ phận đang chọn.\n'
        'After:\n– Nạp danh sách bộ phận theo phòng ban mới và nạp lại danh sách phiếu.'),
       ('Gõ từ khóa ở ô Khách hàng', 'Change',
        'Before:\n– Chỉ gợi ý khi từ khóa từ 2 ký tự trở lên.\n'
        'After:\n– Hiển thị tối đa 20 khách hàng dạng “Mã - Tên”; chọn một dòng thì lọc ngay.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Không cần điều kiện.\n'
        'After:\n– Đặt mọi tiêu chí về trống, xóa nhãn khách hàng đã chọn, bỏ sắp xếp, về trang 1 và nạp lại danh sách.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho mỗi người dùng tự chọn tiêu chí lọc nào hiện ở khối Tìm kiếm nâng cao và sắp lại thứ tự của chúng. '
                   'Cấu hình lưu riêng theo người dùng và theo màn hình.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” với 6 tiêu chí kèm ô tích.\n'
                    '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống lưu cấu hình, đóng cửa sổ, báo “Cập nhật thành công” và vẽ lại khối lọc.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ 6 tiêu chí theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bỏ mọi thay đổi chưa lưu (không hỏi xác nhận).\n'
                  '• Lưu lỗi → “Thao tác thất bại”, cửa sổ giữ nguyên.', dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', ['- Kèm icon bánh răng']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', ['- Đóng cửa sổ, bỏ thay đổi chưa lưu']),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        ['- “Tích chọn trường lọc muốn hiển thị; kéo ⋮⋮ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”']),
       ('Danh sách tiêu chí', 'Table/Grid', 'Enable', 'Danh sách 6 tiêu chí', 'Không', 'Theo cấu hình đã lưu', [
           '- Công ty – Phòng ban – Bộ phận', '- Khách hàng', '- Hợp đồng', '- Người tạo', '- Trạng thái', '- Ngày tạo']),
       ('Ô tích từng tiêu chí', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu',
        ['- Bỏ tích → tiêu chí không hiện ở khối Tìm kiếm nâng cao']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Biểu tượng ⋮⋮ đầu mỗi dòng; kéo để đổi thứ tự tiêu chí']),
       ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Lưu cấu hình cho người dùng hiện tại, đóng cửa sổ', '- Khóa trong lúc đang lưu']),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Tích lại đủ 6 tiêu chí, thứ tự như thiết kế; chưa lưu']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Đóng cửa sổ, bỏ thay đổi chưa lưu']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình đang lưu của người dùng.'),
       ('Tích / bỏ tích một tiêu chí', 'Change',
        'Before:\n– Áp cho mọi tiêu chí.\nAfter:\n– Ghi nhận trong cửa sổ, chưa áp lên màn cho tới khi bấm Lưu.'),
       ('Kéo đổi vị trí tiêu chí', 'Drag',
        'Before:\n– Kéo bằng tay nắm ⋮⋮.\nAfter:\n– Đổi thứ tự trong cửa sổ; lưu khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Chặn bấm lặp trong lúc đang lưu.\n'
        'During:\n– Ghi cấu hình theo người dùng và màn hình; lỗi → “Thao tác thất bại”.\n' + ERR + '\n'
        'After:\n– Đóng cửa sổ, báo “Cập nhật thành công”, vẽ lại khối Tìm kiếm nâng cao theo cấu hình mới.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không cần điều kiện.\nAfter:\n– Tích lại đủ 6 tiêu chí theo thứ tự gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, trả danh sách về cấu hình đang áp dụng.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Tùy chỉnh cột của bảng danh sách',
              mota='Cho mỗi người dùng tự chọn cột nào hiện trên bảng danh sách và thứ tự cột. Cấu hình lưu riêng theo '
                   'người dùng; ba cột STT, Mã phiếu, Hành động bị khóa.',
              tacnhan=TN_XEM, dieukien=DK_XEM,
              chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” với 13 cột kèm ô tích.\n'
                    '3. Người dùng tích / bỏ tích, kéo biểu tượng ≡ để đổi thứ tự.\n4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống lưu cấu hình, đóng cửa sổ, báo “Cập nhật thành công” và vẽ lại bảng.',
              phu='• Bấm Chọn tất cả / Bỏ chọn hết → không tác động tới 3 cột khóa.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, trả về cấu hình đang áp dụng (không hỏi xác nhận).\n'
                  '• Lưu lỗi → “Thao tác thất bại”.',
              dacbiet='Cột Phiếu YCXH mặc định ẩn; cấu hình đã lưu cũng quyết định các trường được tích sẵn khi Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', ['- Kèm icon tròn bên trái']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', ['- Đóng cửa sổ, bỏ thay đổi chưa lưu']),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        ['- “Tích chọn cột cần hiển thị, kéo ≡ để đổi thứ tự cột trên bảng.”']),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Tích mọi cột (cột khóa giữ nguyên)']),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Bỏ tích mọi cột trừ 3 cột khóa']),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 13 cột', 'Không', 'Theo cấu hình đã lưu', [
           '- STT, Mã phiếu, Số hợp đồng/đơn hàng, Phiếu YCXH, Khách hàng, Ngày tạo, Người tạo, Ngày cập nhật, '
           'Người cập nhật, Ngày duyệt, Người duyệt, Trạng thái, Hành động', '- Phiếu YCXH mặc định không tích']),
       ('Ô tích từng cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình đã lưu', [
           '- Bỏ tích → cột ẩn khỏi bảng',
           '- Cột khóa STT, Mã phiếu, Hành động: ô tích xám, luôn tích, icon ổ khóa; rê chuột “Cột bắt buộc — không thể '
           'ẩn hoặc đổi vị trí”']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Biểu tượng ≡ cuối mỗi dòng; kéo để đổi thứ tự', '- Cột khóa không kéo được']),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Lưu cấu hình theo người dùng, đóng cửa sổ']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Đóng cửa sổ, bỏ thay đổi chưa lưu']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu của người dùng.'),
       ('Tích / bỏ tích một cột', 'Change',
        'Before:\n– Cột khóa (STT, Mã phiếu, Hành động) không cho bỏ tích.\n'
        'After:\n– Ghi nhận trong cửa sổ, chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bấm Chọn tất cả / Bỏ chọn hết', 'Click',
        'Before:\n– Bỏ qua 3 cột khóa.\nAfter:\n– Tích / bỏ tích mọi cột còn lại trong cửa sổ.'),
       ('Kéo biểu tượng ≡', 'Drag',
        'Before:\n– Cột khóa không kéo được.\nAfter:\n– Đổi thứ tự cột trong cửa sổ.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Không cần quyền riêng.\n'
        'During:\n– Ghi cấu hình cho người dùng hiện tại; lỗi → “Thao tác thất bại”.\n' + ERR + '\n'
        'After:\n– Đóng cửa sổ, báo “Cập nhật thành công”, vẽ lại bảng theo bộ cột và thứ tự mới.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, danh sách cột trở về cấu hình đang áp dụng.'),
   ])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu yêu cầu vận chuyển, bốc xếp', usecase=('FR-05', 'Lập phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu yêu cầu vận chuyển, bốc xếp',
       mota='Tạo phiếu đề nghị thủ kho bố trí vận chuyển và bốc xếp hàng: người lập chọn đơn hàng/hợp đồng và phiếu yêu '
            'cầu xuất hàng, hệ thống tự điền khách hàng, địa điểm giao, danh sách hàng; người lập nhập thời gian vận '
            'chuyển, thông tin bốc xếp, số kiện, đính kèm file rồi lưu nháp hoặc gửi thủ kho duyệt.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng; người dùng đang ở màn danh sách.\n'
                '3. Có phiếu yêu cầu xuất hàng ở trạng thái chọn được và đã gắn khách hàng (BR-02).',
       chinh='1. Người dùng bấm Tạo mới.\n2. Hệ thống mở màn “Tạo phiếu yêu cầu vận chuyển, bốc xếp”, các ô trống, bảng '
             'Chi tiết “Không có dữ liệu”.\n'
             '3. Người dùng chọn Đơn hàng/Hợp đồng (mục 2.6) rồi Phiếu YCXH (mục 2.7).\n'
             '4. Hệ thống điền Khách hàng, Người liên hệ, Số ĐT, Địa điểm giao và các dòng hàng có số lượng > 0.\n'
             '5. Người dùng nhập Thời gian vận chuyển, Ghi chú, khối Bốc xếp, Số kiện từng dòng, đính kèm file (tùy chọn).\n'
             '6. Người dùng bấm Lưu nháp hoặc Gửi duyệt.\n'
             '7. Hệ thống kiểm tra dữ liệu, đọc lại thông tin từ phiếu YCXH, sinh mã phiếu, lưu phiếu và dòng hàng.\n'
             '8. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu.\n'
             '9. Gửi duyệt: hệ thống gửi thông báo “[YCVC] Chờ duyệt” cho mọi thủ kho của kho xuất hàng.\n'
             '10. Hệ thống báo “Thêm mới thành công.” / “Gửi duyệt thành công.”, quay về màn danh sách.',
       phu='• Thiếu Đơn hàng/Hợp đồng, Phiếu YCXH hoặc bảng Chi tiết trống → viền đỏ, “Bắt buộc phải nhập” dưới ô, thông '
           'báo “Vui lòng kiểm tra lại thông tin đã nhập”, không lưu.\n'
           '• Bấm ô Phiếu YCXH khi chưa chọn hợp đồng → “Vui lòng chọn đơn hàng/hợp đồng trước.”.\n'
           '• Đổi / bỏ Đơn hàng/Hợp đồng → Phiếu YCXH và các thông tin lấy theo YCXH bị xóa.\n'
           '• Kho xuất hàng chưa có thủ kho → chỉ lưu nháp được; bấm Gửi duyệt bị chặn “Kho xuất hàng chưa có thủ kho, '
           'chưa gửi duyệt được.”.\n'
           '• Bấm Lưu và tiếp tục → lưu nháp rồi mở lại form trống để lập tiếp.\n'
           '• Rời màn khi có thay đổi chưa lưu → hộp “Thông tin chưa lưu” (Thoát / Ở lại).\n'
           '• Lỗi hệ thống → ' + SYS_ERR + ', giữ nguyên dữ liệu đã nhập.',
       dacbiet='Lưu nháp và Gửi duyệt cùng bắt buộc Đơn hàng/Hợp đồng, Phiếu YCXH và ít nhất 1 dòng hàng (BR-04). Khách '
               'hàng, người liên hệ, địa điểm giao, dòng hàng luôn lấy lại từ phiếu YCXH lúc lưu; người dùng chỉ nhập Số kiện. '
               'Các nút lưu bị khóa trong lúc đang xử lý.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'), shot_caption='Màn Tạo phiếu yêu cầu vận chuyển, bốc xếp đã nhập dữ liệu'),
   figs=[('10_create', 'Màn Tạo phiếu lúc vừa mở'), ('10b_validate', 'Thông báo bắt buộc nhập khi bấm lưu thiếu dữ liệu')],
   ui=form_ui(False),
   ev=[('Bấm Tạo mới (mở màn Tạo)', 'System',
        'Before:\n– Không kiểm tra quyền riêng.\n'
        'After:\n– Mở form trống; dòng người lập hiện người đang đăng nhập và giờ hiện tại; bảng Chi tiết “Không có dữ liệu”.')]
      + FIELD_EV + [save_ev(False, True), save_ev(False, False),
                    ('Bấm Lưu và tiếp tục', 'Click',
                     'Before:\n– Như Bấm Lưu nháp.\nDuring:\n– Kiểm tra như Bấm Lưu nháp.\n' + ERR + '\n'
                     'After:\n– Lưu phiếu ở trạng thái Đang tạo, ghi “Tạo mới” trong lịch sử, báo “Thêm mới thành công.”.\n'
                     '– Mở lại form trống ngay trên màn Tạo (không về danh sách).'),
                    LEAVE_EV])

# ------------------------------------------------------------ 2.6
CONTRACT_TYPES = ['Hợp đồng bán', 'Hợp đồng bán (ERP)', 'Hợp đồng dịch vụ BH-SC', 'Hợp đồng bán đầu kỳ', 'Hợp đồng mua hàng',
                  'Hợp đồng mua hàng ngoài', 'Hợp đồng mua hàng trong nước', 'Hợp đồng mua dịch vụ', 'Hợp đồng mua đầu kỳ',
                  'Phiếu xử lý hàng thiếu', 'Xác nhận bảo hành hãng']
fr(6, 'Chọn đơn hàng/hợp đồng', usecase=('FR-06', 'Chọn đơn hàng/hợp đồng', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn đơn hàng/hợp đồng cho phiếu',
       mota='Cửa sổ liệt kê đơn hàng/hợp đồng từ 11 loại chứng từ (hợp đồng bán, hợp đồng dịch vụ BH-SC, hợp đồng bán '
            'đầu kỳ, các loại hợp đồng mua, phiếu xử lý hàng thiếu, xác nhận bảo hành hãng) để người lập gắn phiếu vận '
            'chuyển với đúng chứng từ bán / mua hàng.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo hoặc Sửa phiếu.',
       chinh='1. Người dùng bấm vào ô Đơn hàng/Hợp đồng.\n2. Hệ thống mở cửa sổ “Chọn đơn hàng/hợp đồng”, liệt kê chứng '
             'từ chọn được (BR-03), mới tạo lên trước.\n'
             '3. Người dùng gõ số rồi nhấn Enter / bấm Tìm kiếm, lọc Loại hợp đồng nếu cần.\n'
             '4. Người dùng bấm vào một dòng.\n'
             '5. Hệ thống điền ô Đơn hàng/Hợp đồng và đóng cửa sổ; hợp đồng khác hợp đồng cũ thì xóa Phiếu YCXH đã chọn.',
       phu='• Bấm số hợp đồng trên dòng → mở chứng từ ở tab mới, không chọn dòng.\n'
           '• Không có kết quả → “Không có đơn hàng/hợp đồng có hiệu lực phù hợp.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không chọn (cửa sổ không có dữ liệu nhập cần hỏi xác nhận).\n'
           '• Lỗi khi nạp → “Lỗi khi tải dữ liệu”.',
       dacbiet='Hợp đồng bán (HRM và ERP) và hợp đồng dịch vụ BH-SC chỉ lấy hợp đồng còn hiệu lực do người cùng công ty với người đăng '
               'nhập lập; các hợp đồng mua hàng (trừ hợp đồng mua dịch vụ) chỉ lấy hợp đồng đã phát sinh công nợ phải trả '
               'nhà cung cấp.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('11_contract'), shot_caption='Cửa sổ Chọn đơn hàng/hợp đồng',
               note='Modal Chọn đơn hàng/hợp đồng được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui=pick_ui('Chọn đơn hàng/hợp đồng', 'Số đơn hàng/Hợp đồng', [
       ('Loại hợp đồng', 'Dropdown', 'Enable', 'Danh sách 11 giá trị', 'Không', 'Tất cả',
        ['- Mặc định: Tất cả (gợi ý “Tất cả”)', '- Lựa chọn:'] + ['- ' + x for x in CONTRACT_TYPES] +
        ['- Đổi giá trị → lọc lại ngay, về trang 1']),
   ], 'Không có đơn hàng/hợp đồng có hiệu lực phù hợp.', 'số đơn hàng/hợp đồng; hợp đồng mua còn khớp theo số ghi trên bút toán công nợ')
      + [('Cột Loại hợp đồng', 'Table/Grid', 'Read-only', 'Danh sách 11 giá trị', '–', 'Theo dữ liệu',
          ['- Tên loại chứng từ của dòng', '- Không sắp xếp'])]
      + pick_tail('Không có đơn hàng/hợp đồng có hiệu lực phù hợp.'),
   ev=[('Mở cửa sổ', 'System',
        'Before:\n– Ô tìm và Loại hợp đồng về trống, bỏ sắp xếp.\n'
        'During:\n– Gom chứng từ từ 11 loại theo điều kiện từng loại (BR-03); không xác định được công ty người đăng nhập '
        'thì bỏ hẳn các loại cần cùng công ty.\n– Lỗi → “Lỗi khi tải dữ liệu”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, mới tạo lên trước; nạp danh sách Loại hợp đồng.'),
       ('Đổi Loại hợp đồng', 'Change',
        'Before:\n– Giữ nội dung ô Số đơn hàng/Hợp đồng.\nAfter:\n– Chỉ còn chứng từ của loại đã chọn, về trang 1.')]
      + PICK_COMMON_EV + [
       ('Bấm một dòng', 'Click',
        'Before:\n– Bấm vào vùng dòng, không phải chữ liên kết.\n'
        'During:\n– So với đơn hàng/hợp đồng đang chọn trên form.\n'
        'After:\n– Điền ô Đơn hàng/Hợp đồng, đóng cửa sổ; khác hợp đồng cũ thì xóa Phiếu YCXH, các ô lấy theo YCXH và bảng Chi tiết.'),
       PICK_CLOSE])

# ------------------------------------------------------------ 2.7
fr(7, 'Chọn phiếu yêu cầu xuất hàng', usecase=('FR-07', 'Chọn phiếu YCXH', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn phiếu yêu cầu xuất hàng cho phiếu',
       mota='Cửa sổ liệt kê phiếu yêu cầu xuất hàng có thể chọn. Chọn xong hệ thống điền khách hàng, người liên hệ, số '
            'điện thoại, địa điểm giao và danh sách hàng vào form, đồng thời cho biết kho xuất hàng đã có thủ kho để gửi '
            'duyệt hay chưa.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo hoặc Sửa phiếu.\n3. Đã chọn Đơn hàng/Hợp đồng.',
       chinh='1. Người dùng bấm vào ô Phiếu YCXH.\n2. Hệ thống mở cửa sổ “Chọn phiếu yêu cầu xuất hàng”.\n'
             '3. Người dùng gõ mã rồi nhấn Enter / bấm Tìm kiếm, bấm vào một dòng.\n'
             '4. Hệ thống đóng cửa sổ, kiểm tra phiếu còn chọn được và đã gắn khách hàng.\n'
             '5. Hệ thống điền Khách hàng, Người liên hệ, Số ĐT, Địa điểm giao và các dòng hàng có số lượng > 0 (Số kiện để trống).\n'
             '6. Kho xuất hàng chưa có thủ kho → dưới ô hiện ghi chú chỉ lưu nháp được.',
       phu='• Chưa chọn hợp đồng → “Vui lòng chọn đơn hàng/hợp đồng trước.”, không mở cửa sổ.\n'
           '• Phiếu vừa chuyển sang trạng thái không chọn được → dưới ô “Không thể chọn phiếu này.”, thông báo “Vui lòng '
           'kiểm tra lại thông tin đã nhập”, giữ lựa chọn cũ.\n'
           '• Phiếu chưa gắn khách hàng → “Phiếu chưa gắn khách hàng, vui lòng chọn phiếu khác.”.\n'
           '• Lỗi khác khi lấy dữ liệu → “Không lấy được dữ liệu phiếu yêu cầu xuất hàng.”.\n'
           '• Bấm mã phiếu trên dòng → mở chi tiết YCXH ở tab mới.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không chọn.',
       dacbiet='Chỉ hiện phiếu YCXH ở trạng thái Đã đề nghị, Chờ duyệt, Đang tạo, Đợi TP duyệt, Đợi BGD duyệt (giống ERP) '
               'và đã gắn khách hàng; danh sách không lọc theo hợp đồng đã chọn.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('12_export_request'), shot_caption='Cửa sổ Chọn phiếu yêu cầu xuất hàng',
               note='Modal Chọn phiếu yêu cầu xuất hàng được mở ngay trên màn hình Tạo / Sửa phiếu theo đường dẫn ở trên.'),
   ui=pick_ui('Chọn phiếu yêu cầu xuất hàng', 'Mã phiếu', [], 'Không có phiếu yêu cầu xuất hàng phù hợp.',
              'mã phiếu yêu cầu xuất hàng')
      + pick_tail('Không có phiếu yêu cầu xuất hàng phù hợp.')
      + [('Thông báo lỗi dưới ô Phiếu YCXH', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
          '- Sau khi chọn dòng: “Không thể chọn phiếu này.” hoặc “Phiếu chưa gắn khách hàng, vui lòng chọn phiếu khác.”',
          '- Kèm thông báo góc màn hình “Vui lòng kiểm tra lại thông tin đã nhập”'])],
   ev=[('Mở cửa sổ', 'System',
        'Before:\n– Đã chọn Đơn hàng/Hợp đồng (kiểm ở ô Phiếu YCXH, mục 2.5).\n'
        'During:\n– Lấy phiếu YCXH ở 5 trạng thái chọn được và đã gắn khách hàng (BR-02).\n– Lỗi → “Lỗi khi tải dữ liệu”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, mới tạo lên trước.')]
      + PICK_COMMON_EV + [
       ('Bấm một dòng', 'Click',
        'Before:\n– Bấm vào vùng dòng, không phải chữ liên kết; cửa sổ đóng ngay.\n'
        'During:\n– Phiếu không còn ở trạng thái chọn được → “Không thể chọn phiếu này.” dưới ô.\n'
        '– Phiếu chưa gắn khách hàng → “Phiếu chưa gắn khách hàng, vui lòng chọn phiếu khác.” dưới ô.\n'
        '– Lỗi khác → “Không lấy được dữ liệu phiếu yêu cầu xuất hàng.”.\n' + ERR + '\n'
        'After:\n– Điền mã phiếu YCXH, Khách hàng “Mã - Tên”, Người liên hệ, Số ĐT, Địa điểm giao, bảng hàng (Số kiện trống); '
        'xóa lỗi cũ trên form.\n– Kho chưa có thủ kho → hiện ghi chú “Kho của phiếu này chưa có thủ kho — chỉ lưu nháp '
        'được, chưa gửi duyệt được.”.'),
       PICK_CLOSE])

# ------------------------------------------------------------ 2.8
fr(8, 'Chỉnh sửa phiếu', usecase=('FR-08', 'Chỉnh sửa phiếu', 'crud', A_LAP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Chỉnh sửa phiếu yêu cầu vận chuyển, bốc xếp',
       mota='Người lập sửa phiếu đang ở trạng thái Đang tạo hoặc bị thủ kho Từ chối, rồi lưu nháp lại hoặc gửi duyệt '
            '(lại). Quy tắc nhập liệu giống màn Tạo; mọi thay đổi được ghi vào lịch sử của phiếu.',
       tacnhan=TN_SUA,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người lập phiếu (không cần quyền riêng).\n'
                '3. Phiếu đang ở trạng thái Đang tạo hoặc Từ chối.',
       chinh='1. Người dùng bấm icon Sửa ở cột Hành động hoặc nút Sửa ở màn Chi tiết.\n'
             '2. Hệ thống mở màn “Sửa phiếu yêu cầu vận chuyển, bốc xếp: <mã>”, tiêu đề kèm nhãn trạng thái; phiếu Từ '
             'chối hiện thêm Lý do từ chối.\n'
             '3. Người dùng sửa thông tin (quy tắc như mục 2.5), xóa / thêm file.\n4. Người dùng bấm Lưu nháp hoặc Gửi duyệt.\n'
             '5. Hệ thống kiểm tra, lưu phiếu, ghi nhận hành động “Thay đổi thông tin” (và “Thay đổi trạng thái” khi '
             'trạng thái đổi) trong lịch sử của phiếu.\n'
             '6. Gửi duyệt: gửi thông báo “[YCVC] Chờ duyệt” cho thủ kho; gửi lại sau Từ chối thì xóa lý do cũ.\n'
             '7. Hệ thống báo “Cập nhật thành công.” / “Gửi duyệt thành công.”, quay về màn danh sách.',
       phu='• Mở màn Sửa của phiếu không sửa được (người khác lập / đã gửi duyệt) → chuyển sang màn Chi tiết.\n'
           '• Phiếu không tồn tại hoặc ngoài phạm vi xem → chuyển sang trang không tìm thấy.\n'
           '• Phiếu vừa đổi trạng thái ở nơi khác → ' + CONFLICT + ', chuyển sang màn Chi tiết.\n'
           '• Giữ nguyên phiếu YCXH cũ thì không bắt phiếu đó còn ở trạng thái chọn được.\n'
           '• Xóa file đã lưu → hỏi xác nhận, xóa ngay, ghi lịch sử, không cần bấm lưu.\n'
           '• Rời màn khi có thay đổi chưa lưu → hộp “Thông tin chưa lưu”.',
       dacbiet='Màn Sửa không có nút Lưu và tiếp tục. Các nút lưu bị khóa trong lúc đang xử lý.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('19_edit'), shot_caption='Màn Sửa phiếu yêu cầu vận chuyển, bốc xếp'),
   ui=form_ui(True),
   ev=[('Mở màn Sửa', 'System',
        'Before:\n– Kiểm tra phiếu tồn tại và nằm trong phạm vi xem; không đạt → chuyển sang trang không tìm thấy.\n'
        '– Kiểm tra người lập và trạng thái Đang tạo / Từ chối; không đạt → chuyển sang màn Chi tiết phiếu.\n'
        'After:\n– Điền dữ liệu phiếu, file đính kèm, bảng hàng kèm Số kiện; phiếu Từ chối hiện Lý do từ chối.')]
      + FIELD_EV + [
       ('Bấm icon Xóa của file đã lưu', 'Click',
        'Before:\n– Kiểm tra người lập và trạng thái Đang tạo / Từ chối; không đạt → “Bạn không có quyền sửa phiếu này” '
        'hoặc ' + CONFLICT + '.\n'
        'During:\n– Hiện hộp “Bạn có chắc muốn xóa file đính kèm này?”; Hủy thì dừng.\n'
        '– File không thuộc phiếu → “File không thuộc phiếu này.”.\n' + ERR + '\n'
        'After:\n– Xóa file khỏi phiếu và kho lưu trữ; ghi nhận “Thay đổi thông tin” (file đã xóa) trong lịch sử của phiếu.\n'
        '– Hiển thị “Xóa file thành công”.'),
       save_ev(True, True), save_ev(True, False), LEAVE_EV])

# ------------------------------------------------------------ 2.9
fr(9, 'Xóa phiếu', usecase=('FR-09', 'Xóa phiếu', 'action', A_LAP),
   rule=('- Quy tắc Xóa và Thông báo.', 'delete'),
   intro=dict(
       ten='Xóa phiếu yêu cầu vận chuyển, bốc xếp',
       mota='Người lập xóa hẳn phiếu đang ở trạng thái Đang tạo hoặc Từ chối cùng toàn bộ dòng hàng. Lịch sử ghi nhận '
            'hành động Xóa kèm ảnh chụp dữ liệu phiếu trước khi xóa.',
       tacnhan=TN_SUA,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người lập phiếu.\n'
                '3. Phiếu đang ở trạng thái Đang tạo hoặc Từ chối.',
       chinh='1. Người dùng bấm icon Xóa ở cột Hành động hoặc nút Xóa ở màn Chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa” với nội dung “Bạn có chắc muốn xóa phiếu yêu cầu vận chuyển \'<mã>\'?”.\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm tra người lập và trạng thái, ghi nhận hành động “Xóa” trong lịch sử của phiếu, xóa phiếu và dòng hàng.\n'
             '5. Hệ thống báo “Xóa thành công.”; ở danh sách thì nạp lại giữ bộ lọc, ở màn Chi tiết thì về danh sách.',
       phu='• Bấm Hủy / (x) / click ra ngoài hộp → đóng hộp, không xóa.\n'
           '• Phiếu vừa đổi trạng thái ở nơi khác → ' + CONFLICT + '; ở màn Chi tiết thì tải lại trang.\n'
           '• Người không phải người lập gọi xóa → “Bạn không có quyền xóa phiếu này”.\n'
           '• Lỗi hệ thống → ' + SYS_ERR + '.',
       dacbiet='Nút xác nhận Xóa màu đỏ; chặn bấm lặp trong lúc đang xóa.'),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp xác nhận xóa phiếu',
               note='Modal Xác nhận xóa được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận xóa', ['- Kèm icon cảnh báo đỏ']),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', ['- Đóng hộp, không xóa']),
       ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
        ["- “Bạn có chắc muốn xóa phiếu yêu cầu vận chuyển '<mã>'?”", '- <mã>: mã phiếu đang chọn']),
       ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', ['- Màu đỏ', '- Xác nhận xóa phiếu']),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', ['- Đóng hộp, không xóa']),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', 'Ẩn', ['- “Xóa thành công.”']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', 'Ẩn', [
           '- Không phải người lập: “Bạn không có quyền xóa phiếu này”', '- Phiếu đã đổi trạng thái: ' + CONFLICT,
           '- Lỗi hệ thống: ' + SYS_ERR])],
   ev=[('Bấm icon Xóa trên dòng / nút Xóa ở màn Chi tiết', 'Click',
        'Before:\n– Icon / nút chỉ hiện với người lập khi phiếu Đang tạo hoặc Từ chối.\n'
        'After:\n– Hiện hộp “Xác nhận xóa” kèm mã phiếu.'),
       ('Bấm Xóa trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra người lập phiếu: người khác → “Bạn không có quyền xóa phiếu này” và dừng xử lý.\n'
        '– Kiểm tra trạng thái Đang tạo / Từ chối: đã đổi → ' + CONFLICT + ' và dừng xử lý.\n'
        'During:\n– Chặn bấm lặp trong lúc đang xóa.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Xóa” kèm dữ liệu phiếu, dòng hàng, file trước khi xóa.\n'
        '– Xóa phiếu và toàn bộ dòng hàng.\n'
        '– Hiển thị “Xóa thành công.”; ở danh sách nạp lại giữ bộ lọc, ở màn Chi tiết quay về danh sách.'),
       ('Bấm Hủy / (x) / click ra ngoài hộp', 'Click',
        'Before:\n– Không cần điều kiện.\nAfter:\n– Đóng hộp, phiếu giữ nguyên.')])

# ------------------------------------------------------------ 2.10
DETAIL_RO = lambda n, t, scope, init, desc: (n, t, 'Read-only', scope, init, desc)  # noqa: E731
fr(10, 'Xem chi tiết phiếu', usecase=('FR-10', 'Xem chi tiết phiếu', 'view', A_LAP),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu yêu cầu vận chuyển, bốc xếp',
       mota='Xem toàn bộ thông tin phiếu ở chế độ chỉ đọc: thông tin vận chuyển, bốc xếp, file đính kèm, danh sách hàng, '
            'kết quả duyệt và lịch sử thay đổi. Màn là nơi thủ kho duyệt / từ chối và người lập sửa / xóa phiếu.',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu nằm trong phạm vi xem (BR-09).\n'
                '3. Phiếu Đang tạo chỉ người lập (hoặc Super admin) xem được.',
       chinh='1. Người dùng bấm Mã phiếu ở danh sách (hoặc icon Duyệt, hoặc liên kết trong thông báo).\n'
             '2. Hệ thống kiểm tra quyền xem phiếu.\n'
             '3. Hệ thống mở màn “Chi tiết phiếu yêu cầu vận chuyển, bốc xếp: <mã>”, tiêu đề kèm nhãn trạng thái.\n'
             '4. Hệ thống hiển thị các khối thông tin, khối Lịch sử thu gọn và các nút theo điều kiện.',
       phu='• Phiếu ngoài phạm vi xem hoặc không tồn tại → chuyển sang trang không tìm thấy.\n'
           '• Phiếu chưa được duyệt → không hiện Người duyệt, Ngày duyệt.\n'
           '• Phiếu không có file → ẩn hẳn khối File đính kèm.\n'
           '• Không đủ điều kiện thao tác → chỉ còn nút Quay lại.\n'
           '• Lỗi hệ thống → ' + SYS_ERR + '.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn chi tiết phiếu Chờ duyệt (thủ kho)'),
   figs=[('17b_detail_rej', 'Màn chi tiết phiếu Từ chối có Người duyệt, Ngày duyệt, Lý do từ chối')],
   ui_kw=dict(required=False),
   ui=[
       DETAIL_RO('Tiêu đề màn', 'Label', '–', 'Chi tiết phiếu yêu cầu vận chuyển, bốc xếp: <mã>',
                 ['- Kèm nhãn màu trạng thái (Đang tạo xám, Chờ duyệt cam, Đã duyệt xanh lá, Từ chối đỏ)']),
       DETAIL_RO('Dòng người lập', 'Label', '–', 'Theo dữ liệu', ['- Góc phải khối Thông tin vận chuyển: tên người lập và thời điểm lập']),
       DETAIL_RO('Mã phiếu', 'Textbox', '–', 'Theo dữ liệu', ['- Mã phiếu do hệ thống sinh']),
       DETAIL_RO('Đơn hàng/Hợp đồng', 'Link', '–', 'Theo dữ liệu',
                 ['- Bấm → mở chứng từ ở tab mới (màn HRM hoặc ERP theo loại)', '- Loại không xác định: chữ thường']),
       DETAIL_RO('Phiếu YCXH', 'Link', '–', 'Theo dữ liệu', ['- Bấm → mở chi tiết phiếu yêu cầu xuất hàng ở tab mới']),
       DETAIL_RO('Khách hàng', 'Textbox', '–', 'Theo dữ liệu', ['- Dạng “Mã - Tên khách hàng”']),
       DETAIL_RO('Người liên hệ', 'Textbox', '–', 'Theo dữ liệu', ['- Theo phiếu YCXH lúc lưu']),
       DETAIL_RO('Số ĐT người liên hệ', 'Textbox', '–', 'Theo dữ liệu', ['- Theo phiếu YCXH lúc lưu']),
       DETAIL_RO('Địa điểm giao hàng', 'Textbox', '–', 'Theo dữ liệu', ['- Theo phiếu YCXH lúc lưu']),
       DETAIL_RO('Thời gian vận chuyển', 'Datepicker', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Trống nếu người lập không nhập']),
       DETAIL_RO('Ghi chú', 'Textarea', '0–5000 ký tự', 'Theo dữ liệu', ['- Trống nếu không nhập']),
       DETAIL_RO('Người duyệt', 'Textbox', '–', 'Ẩn', ['- Chỉ hiện khi phiếu Đã duyệt hoặc Từ chối', '- Họ tên thủ kho đã xử lý']),
       DETAIL_RO('Ngày duyệt', 'Textbox', 'dd/mm/yyyy hh:mm', 'Ẩn', ['- Chỉ hiện cùng Người duyệt', '- Thời điểm duyệt / từ chối']),
       DETAIL_RO('Lý do từ chối', 'Textarea', '–', 'Ẩn', ['- Chỉ hiện khi phiếu có lý do từ chối', '- Gửi duyệt lại thì lý do bị xóa']),
       DETAIL_RO('Tổng số kiện', 'Textbox', 'Số nguyên ≥ 0', 'Theo dữ liệu', ['- Trống nếu không nhập']),
       DETAIL_RO('Phương thức bốc xếp', 'Textbox', '0–255 ký tự', 'Theo dữ liệu', ['- Trống nếu không nhập']),
       DETAIL_RO('Địa điểm bốc xếp', 'Textbox', '0–255 ký tự', 'Theo dữ liệu', ['- Trống nếu không nhập']),
       DETAIL_RO('Thời gian bốc xếp', 'Datepicker', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', ['- Trống nếu không nhập']),
       DETAIL_RO('Khối File đính kèm', 'Table/Grid', '–', 'Ẩn khi không có file', [
           '- Cột STT, Upload / File, Dung lượng', '- Mỗi file có icon Xem trước (ảnh, pdf…) và Tải xuống', '- Không thêm / xóa được']),
       DETAIL_RO('Bảng Chi tiết', 'Table/Grid', '–', 'Theo dữ liệu', [
           '- Cột STT, Tên hàng, Model, Mã hàng hóa, ĐVT, Số lượng, Số kiện', '- Số kiện chỉ đọc, trống nếu không nhập']),
       DETAIL_RO('Khối Lịch sử thay đổi', 'Table/Grid', '–', 'Thu gọn', [
           '- Nút Xem lịch sử / Thu gọn ở đầu khối; mở lần đầu mới nạp dữ liệu',
           '- Khi mở có nút Làm mới; nội dung như cửa sổ Lịch sử thay đổi (mục 2.14)']),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', ['- Chỉ hiện với người lập, phiếu Đang tạo / Từ chối', '- Bấm → mở màn Sửa (mục 2.8)']),
       ('Nút Duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn', [
           '- Chỉ hiện với thủ kho của kho xuất hàng (hoặc Super admin), phiếu Chờ duyệt',
           '- Bấm → hộp Xác nhận duyệt (mục 2.11)', '- Khóa trong lúc đang xử lý']),
       ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn', [
           '- Màu đỏ; cùng điều kiện với nút Duyệt', '- Bấm → cửa sổ Từ chối (mục 2.12)']),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', [
           '- Màu đỏ; cùng điều kiện với nút Sửa', '- Bấm → hộp Xác nhận xóa (mục 2.9)']),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', ['- Về màn danh sách (giữ bộ lọc đã dùng)']),
   ],
   ev=[('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra quyền xem: người lập, Super admin, thủ kho của kho xuất hàng, người đã duyệt / từ chối, hoặc '
        'theo quyền V1–V4; phiếu Đang tạo chỉ người lập xem.\n'
        '– Không đạt hoặc phiếu không tồn tại → chuyển sang trang không tìm thấy và dừng xử lý.\n'
        'During:\n– Nạp dữ liệu phiếu, dòng hàng, file; lỗi hệ thống → ' + SYS_ERR + '.\n'
        'After:\n– Hiển thị các khối chỉ đọc, khối Lịch sử thu gọn; nút Sửa / Xóa / Duyệt / Từ chối hiện theo điều kiện.'),
       ('Bấm liên kết Đơn hàng/Hợp đồng', 'Click',
        'Before:\n– Loại chứng từ xác định được.\nAfter:\n– Mở chứng từ ở tab mới.'),
       ('Bấm liên kết Phiếu YCXH', 'Click',
        'Before:\n– Phiếu có mã YCXH.\nAfter:\n– Mở chi tiết phiếu yêu cầu xuất hàng ở tab mới; quyền xem do màn đó xét.'),
       ('Bấm Xem trước / Tải xuống file', 'Click',
        'Before:\n– Xem trước chỉ có với file xem được trên trình duyệt (ảnh, pdf…).\nAfter:\n– Mở xem trước hoặc tải file về máy.'),
       ('Bấm Xem lịch sử', 'Click',
        'Before:\n– Người dùng xem được phiếu.\nAfter:\n– Mở khối, nạp lịch sử lần đầu; bấm Thu gọn để đóng (mục 2.14).'),
       ('Bấm Sửa', 'Click',
        'Before:\n– Nút chỉ hiện với người lập, phiếu Đang tạo / Từ chối.\nAfter:\n– Mở màn Sửa (mục 2.8).'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Không cần điều kiện.\nAfter:\n– Về màn danh sách, khôi phục bộ lọc đã dùng trong vòng 10 phút.'),
   ])

# ------------------------------------------------------------ 2.11
fr(11, 'Duyệt phiếu', usecase=('FR-11', 'Duyệt phiếu', 'action', A_TK),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Duyệt phiếu yêu cầu vận chuyển, bốc xếp',
       mota='Thủ kho của kho xuất hàng đồng ý bố trí vận chuyển, bốc xếp theo phiếu. Duyệt xong phiếu yêu cầu xuất hàng '
            'chuyển hình thức vận chuyển sang Công ty vận chuyển và người lập nhận thông báo.',
       tacnhan=TN_TK,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là thủ kho của kho xuất hàng trên phiếu YCXH (hoặc Super admin).\n'
                '3. Phiếu ở trạng thái Chờ duyệt.',
       chinh='1. Thủ kho mở màn Chi tiết phiếu (bấm mã phiếu, icon Duyệt trên dòng danh sách hoặc thông báo).\n'
             '2. Thủ kho bấm Duyệt.\n'
             '3. Hệ thống hiện hộp “Xác nhận duyệt”: “Bạn có chắc muốn duyệt phiếu yêu cầu vận chuyển \'<mã>\'?”.\n'
             '4. Thủ kho bấm Duyệt trong hộp.\n'
             '5. Hệ thống kiểm tra quyền, trạng thái, phiếu YCXH; chuyển phiếu sang Đã duyệt, ghi người / ngày duyệt; phiếu '
             'YCXH đổi hình thức vận chuyển thành “Công ty vận chuyển”.\n'
             '6. Hệ thống ghi nhận hành động “Thay đổi trạng thái” (Chờ duyệt → Đã duyệt) trong lịch sử của phiếu.\n'
             '7. Hệ thống gửi thông báo “[YCVC] Đã duyệt” cho người lập, báo “Duyệt thành công.”, quay về danh sách.',
       phu='• Bấm Hủy / (x) / click ra ngoài hộp → không duyệt.\n'
           '• Phiếu vừa đổi trạng thái ở nơi khác → ' + CONFLICT + ', tải lại trang.\n'
           '• Phiếu YCXH đã chuyển sang trạng thái không còn hợp lệ → “Phiếu yêu cầu xuất hàng không hợp lệ.”, không duyệt.\n'
           '• Người không phải thủ kho gọi duyệt → “Bạn không có quyền duyệt phiếu này”.',
       dacbiet='Nút Duyệt khóa trong lúc đang xử lý; lỗi gửi thông báo không làm hỏng việc duyệt.'),
   layout=dict(menu=MENU + ' => Xem chi tiết => Duyệt', shot=shot('14_approve'), shot_caption='Hộp xác nhận duyệt',
               note='Modal Xác nhận duyệt được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[('Tiêu đề hộp', 'Label', 'Hiển thị', 'Xác nhận duyệt', ['- Kèm icon dấu hỏi']),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', ['- Đóng hộp, không duyệt']),
       ('Nội dung', 'Label', 'Hiển thị', 'Theo dữ liệu',
        ["- “Bạn có chắc muốn duyệt phiếu yêu cầu vận chuyển '<mã>'?”", '- <mã>: mã phiếu đang xem']),
       ('Nút Duyệt', 'Button', 'Enable', 'Hiển thị', ['- Xác nhận duyệt phiếu']),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', ['- Đóng hộp, không duyệt']),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', 'Ẩn', ['- “Duyệt thành công.”']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', 'Ẩn', [
           '- Không phải thủ kho: “Bạn không có quyền duyệt phiếu này”', '- Phiếu đã đổi trạng thái: ' + CONFLICT,
           '- Phiếu YCXH không hợp lệ: “Phiếu yêu cầu xuất hàng không hợp lệ.”', '- Lỗi hệ thống: ' + SYS_ERR])],
   ev=[('Bấm Duyệt ở màn Chi tiết', 'Click',
        'Before:\n– Nút chỉ hiện với thủ kho của kho xuất hàng (hoặc Super admin) khi phiếu Chờ duyệt.\n'
        'After:\n– Hiện hộp “Xác nhận duyệt” kèm mã phiếu.'),
       ('Bấm Duyệt trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra thủ kho của kho xuất hàng / Super admin: không phải → “Bạn không có quyền duyệt phiếu này” '
        'và dừng xử lý.\n– Kiểm tra phiếu còn Chờ duyệt: đã đổi → ' + CONFLICT + ', tải lại trang và dừng xử lý.\n'
        '– Chặn bấm lặp trong lúc đang xử lý.\n'
        'During:\n– Phiếu YCXH không còn ở trạng thái chọn được → “Phiếu yêu cầu xuất hàng không hợp lệ.”.\n' + ERR + '\n'
        'After:\n– Phiếu chuyển Đã duyệt; ghi người duyệt, ngày duyệt, người cập nhật.\n'
        '– Phiếu YCXH đổi hình thức vận chuyển thành “Công ty vận chuyển” (BR-07).\n'
        '– Ghi một dòng lịch sử “Thay đổi trạng thái”: Chờ duyệt → Đã duyệt.\n'
        '– Gửi thông báo cho người lập: “[YCVC] Đã duyệt: <mã phiếu>. KH: … Ngày giao: … Người duyệt: …”.\n'
        '– Hiển thị “Duyệt thành công.”, quay về màn danh sách.'),
       ('Bấm Hủy / (x) / click ra ngoài hộp', 'Click',
        'Before:\n– Không cần điều kiện.\nAfter:\n– Đóng hộp, phiếu giữ trạng thái Chờ duyệt.')])

# ------------------------------------------------------------ 2.12
fr(12, 'Từ chối phiếu', usecase=('FR-12', 'Từ chối phiếu', 'action', A_TK),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Từ chối phiếu yêu cầu vận chuyển, bốc xếp',
       mota='Thủ kho không đồng ý bố trí vận chuyển, bốc xếp và trả phiếu về cho người lập. Lý do từ chối là bắt buộc, '
            'được lưu trên phiếu, ghi vào lịch sử và gửi kèm thông báo để người lập sửa rồi gửi duyệt lại.',
       tacnhan=TN_TK,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là thủ kho của kho xuất hàng (hoặc Super admin).\n'
                '3. Phiếu ở trạng thái Chờ duyệt.',
       chinh='1. Thủ kho bấm Từ chối ở màn Chi tiết.\n2. Hệ thống mở cửa sổ “Từ chối phiếu yêu cầu vận chuyển”, dòng phụ '
             '“Phiếu: <mã>”, con trỏ đặt sẵn ở ô Lý do từ chối.\n'
             '3. Thủ kho nhập Lý do từ chối, bấm Từ chối.\n'
             '4. Hệ thống kiểm tra quyền, trạng thái, lý do; chuyển phiếu sang Từ chối, lưu lý do, người / ngày xử lý.\n'
             '5. Hệ thống ghi nhận hành động “Thay đổi trạng thái” (Chờ duyệt → Từ chối) kèm lý do trong lịch sử của phiếu.\n'
             '6. Hệ thống gửi thông báo “[YCVC] Từ chối” kèm lý do cho người lập, báo “Từ chối thành công.”, đóng cửa sổ, '
             'quay về danh sách.',
       phu='• Lý do trống hoặc chỉ có khoảng trắng → viền đỏ, “Bắt buộc phải nhập” dưới ô, không gửi.\n'
           '• Lý do quá 5000 ký tự → “Vui lòng nhập tối đa 5000 ký tự.”.\n'
           '• Phiếu vừa đổi trạng thái ở nơi khác → ' + CONFLICT + ', tải lại trang.\n'
           '• Bấm Hủy / (x) / click ra ngoài cửa sổ → đóng, không hỏi xác nhận dù đã nhập lý do; mở lại thì ô trống.',
       dacbiet='Phiếu Từ chối, người lập được sửa và gửi duyệt lại; nút Từ chối khóa trong lúc đang gửi.'),
   layout=dict(menu=MENU + ' => Xem chi tiết => Từ chối', shot=shot('15_reject'), shot_caption='Cửa sổ Từ chối phiếu',
               note='Modal Từ chối phiếu yêu cầu vận chuyển được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   figs=[('15b_reject_err', 'Thông báo bắt buộc nhập Lý do từ chối')],
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Từ chối phiếu yêu cầu vận chuyển', ['- Kèm icon tròn màu đỏ']),
       ('Dòng phụ', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu', ['- “Phiếu: <mã>”, <mã> là mã phiếu đang xem']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', ['- Đóng cửa sổ, không từ chối']),
       ('Lý do từ chối', 'Textarea', 'Enable', '1–5000 ký tự', 'Có', 'Trống', [
           '- Gợi ý “Nhập lý do từ chối”; con trỏ đặt sẵn khi mở', '- Bỏ khoảng trắng đầu / cuối trước khi lưu']),
       ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
           '- Trống: viền đỏ, “Bắt buộc phải nhập”; chỉ hiện sau lần bấm Từ chối đầu',
           '- Quá 5000 ký tự: thông báo góc màn hình “Vui lòng nhập tối đa 5000 ký tự.”']),
       ('Nút Từ chối', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Màu đỏ; xác nhận từ chối', '- Khóa trong lúc đang gửi']),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Đóng cửa sổ, không từ chối']),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- “Từ chối thành công.”']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
           '- Không phải thủ kho: “Bạn không có quyền từ chối phiếu này”', '- Phiếu đã đổi trạng thái: ' + CONFLICT,
           '- Lỗi hệ thống: ' + SYS_ERR])],
   ev=[('Bấm Từ chối ở màn Chi tiết', 'Click',
        'Before:\n– Nút chỉ hiện với thủ kho của kho xuất hàng (hoặc Super admin) khi phiếu Chờ duyệt.\n'
        'After:\n– Mở cửa sổ, ô Lý do trống, con trỏ đặt sẵn ở ô.'),
       ('Nhập Lý do từ chối', 'Change',
        'Before:\n– Lỗi chỉ hiện sau lần bấm Từ chối đầu.\nAfter:\n– Có ký tự khác khoảng trắng thì lỗi “Bắt buộc phải nhập” mất.'),
       ('Bấm Từ chối trong cửa sổ', 'Click',
        'Before:\n– Kiểm tra thủ kho của kho xuất hàng / Super admin: không phải → “Bạn không có quyền từ chối phiếu này” '
        'và dừng xử lý.\n– Kiểm tra phiếu còn Chờ duyệt: đã đổi → ' + CONFLICT + ', tải lại trang và dừng xử lý.\n'
        'During:\n– Lý do trống / chỉ khoảng trắng → “Bắt buộc phải nhập”.\n'
        '– Lý do quá 5000 ký tự → “Vui lòng nhập tối đa 5000 ký tự.”.\n' + ERR + '\n'
        'After:\n– Phiếu chuyển Từ chối; lưu lý do, người xử lý, ngày xử lý, người cập nhật.\n'
        '– Ghi một dòng lịch sử “Thay đổi trạng thái”: Chờ duyệt → Từ chối, kèm lý do.\n'
        '– Gửi thông báo cho người lập: “[YCVC] Từ chối: <mã phiếu>. Người từ chối: … Lý do: …”.\n'
        '– Hiển thị “Từ chối thành công.”, đóng cửa sổ, quay về màn danh sách.'),
       ('Bấm Hủy / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận dù đã nhập lý do.\nAfter:\n– Đóng cửa sổ, phiếu giữ Chờ duyệt.')])

# ------------------------------------------------------------ 2.13
EXPORT_FIELDS = ['Mã phiếu', 'Số hợp đồng/đơn hàng', 'Khách hàng', 'Ngày tạo', 'Người tạo', 'Ngày cập nhật', 'Người cập nhật',
                 'Ngày duyệt', 'Người duyệt', 'Trạng thái']
fr(13, 'Xuất danh sách ra Excel', usecase=('FR-13', 'Xuất Excel', 'io', A_LAP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu ra Excel',
       mota='Xuất các phiếu đang khớp bộ lọc (trong phạm vi quyền) ra file Excel để theo dõi, báo cáo. Người dùng chọn '
            'trường và thứ tự cột; file có tiêu đề “DANH SÁCH PHIẾU YÊU CẦU VẬN CHUYỂN, BỐC XẾP” và cột STT đầu tiên.',
       tacnhan=TN_XEM, dieukien=DK_XEM + '\n3. Không có lượt xuất nào đang chạy.',
       chinh='1. Người dùng bấm Xuất Excel.\n2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 10 trường, tích sẵn các '
             'trường đang hiện trên bảng.\n3. Người dùng tích / bỏ tích, kéo đổi thứ tự, bấm Xuất file.\n'
             '4. Hệ thống đóng cửa sổ, tải dữ liệu theo từng đợt (hiện tiến độ cạnh nút Xuất Excel) theo bộ lọc và thứ tự '
             'sắp xếp đang áp.\n'
             '5. Hệ thống dựng và tải file “danh_sach_phieu_yeu_cau_van_chuyen.xlsx” (trang tính “Yêu cầu vận chuyển”), '
             'báo “Xuất Excel thành công.”.',
       phu='• Không có phiếu nào khớp → báo “Không có dữ liệu phù hợp.”, không tải file.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → không xuất.\n'
           '• Lỗi hệ thống → ' + SYS_ERR + '.',
       dacbiet='Không giới hạn số dòng; dữ liệu lớn tải theo từng đợt, cạnh nút hiện “Đã tải x/y dòng…” rồi “Đang dựng file '
               'x/y dòng…”. Nút Xuất Excel khóa trong lúc đang xuất.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất Excel', ['- Kèm icon tròn bên trái']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', ['- Đóng cửa sổ, không xuất']),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        ['- “Tích chọn trường cần xuất, kéo ≡ để đổi thứ tự cột trong file.”']),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Tích cả 10 trường']),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Bỏ tích mọi trường']),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 10 trường', 'Ít nhất 1', 'Tích các trường đang hiện trên bảng',
        ['- ' + x for x in EXPORT_FIELDS]),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Không', 'Theo cột đang hiện',
        ['- Mặc định tích đúng các cột đang hiện trên bảng danh sách', '- Bỏ tích → trường không có trong file']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Biểu tượng ≡ cuối mỗi dòng; kéo để đổi vị trí cột trong file']),
       ('Dòng “Đang chọn x/y trường”', 'Label', 'Hiển thị', '–', '–', 'Theo lựa chọn',
        ['- x: số trường đang tích; y: tổng 10 trường']),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → đóng cửa sổ và bắt đầu xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Đóng cửa sổ, không xuất']),
       ('Tiến độ xuất', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Cạnh nút Xuất Excel: “Đang chuẩn bị dữ liệu…”, “Đã tải x/y dòng…”, “Đang dựng file x/y dòng…”']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', [
           '- Thành công: “Xuất Excel thành công.”', '- Không có dữ liệu: “Không có dữ liệu phù hợp.”',
           '- Lỗi hệ thống: ' + SYS_ERR])],
   ev=[('Bấm Xuất Excel', 'Click',
        'Before:\n– Đang có lượt xuất chạy thì bỏ qua.\n'
        'After:\n– Mở cửa sổ, tích sẵn các trường ứng với cột đang hiện trên bảng.'),
       ('Tích / bỏ tích một trường', 'Change',
        'Before:\n– Áp cho cả 10 trường.\nAfter:\n– Cập nhật “Đang chọn x/y trường”; 0 trường thì khóa nút Xuất file.'),
       ('Bấm Chọn tất cả / Bỏ chọn hết', 'Click',
        'Before:\n– Không cần điều kiện.\nAfter:\n– Tích / bỏ tích cả 10 trường.'),
       ('Kéo biểu tượng ≡', 'Drag',
        'Before:\n– Kéo bằng tay nắm.\nAfter:\n– Đổi thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích.\n– Không kiểm tra quyền riêng; dữ liệu giới hạn theo phạm vi xem của '
        'người dùng (BR-09) và bộ lọc, thứ tự sắp xếp đang áp.\n'
        'During:\n– Tải dữ liệu theo từng đợt, cập nhật tiến độ.\n– Không có phiếu nào → “Không có dữ liệu phù hợp.”, '
        'không tải file.\n' + ERR + '\n'
        'After:\n– Tải file “danh_sach_phieu_yeu_cau_van_chuyen.xlsx”: tiêu đề “DANH SÁCH PHIẾU YÊU CẦU VẬN CHUYỂN, BỐC '
        'XẾP”, cột STT rồi các trường đã chọn đúng thứ tự.\n– Hiển thị “Xuất Excel thành công.”.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.')])

# ------------------------------------------------------------ 2.14
fr(14, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(ten='Xem lịch sử thay đổi của phiếu',
              mota='Xem các mốc Tạo mới, Thay đổi thông tin, Thay đổi trạng thái, Xóa của phiếu: ai thực hiện, lúc nào, '
                   'giá trị cũ → mới, kèm lý do khi từ chối. Cùng nội dung ở cửa sổ mở từ danh sách và khối Lịch sử màn Chi tiết.',
              tacnhan=TN_XEM, dieukien=DK_XEM + '\n3. Phiếu nằm trong phạm vi xem.',
              chinh='1. Người dùng bấm icon Lịch sử ở cột Hành động (hoặc Xem lịch sử ở màn Chi tiết).\n'
                    '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <mã>”.\n'
                    '3. Hệ thống hiển thị các mốc, mới nhất lên trên.\n'
                    '4. Người dùng bấm Bộ lọc để lọc theo loại hành động, người thực hiện, khoảng ngày (lọc ngay khi chọn).',
              phu='• Không có mốc nào → “Chưa có lịch sử thao tác nào.”.\n'
                  '• Lọc không ra mốc nào → “Không có lịch sử phù hợp bộ lọc.”.\n'
                  '• Lỗi khi nạp → hiện thông báo lỗi kèm nút Thử lại.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng cửa sổ.', dacbiet=None),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi: <mã>', ['- <mã>: mã phiếu của dòng đã bấm']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', ['- Đóng cửa sổ']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', ['- Mở / thu gọn vùng ô lọc; vùng lọc ghim đầu khi cuộn']),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách', 'Trống', [
           '- Gợi ý “Chọn loại hành động”; mặc định trống (tất cả)', '- Các loại có trong lịch sử của phiếu, như Tạo mới, '
           'Thay đổi thông tin, Thay đổi trạng thái', '- Chọn xong lọc ngay; có dấu × bỏ chọn']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách', 'Trống',
        ['- Gợi ý “Chọn người thực hiện”; mặc định trống', '- Chọn xong lọc ngay']),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', ['- Gợi ý “Từ ngày”; chọn xong lọc ngay']),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', ['- Gợi ý “Đến ngày”; chọn xong lọc ngay']),
       ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', ['- Xóa 4 ô lọc, hiện lại mọi mốc']),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm, tên hành động (màu theo loại), “Người thực hiện: …”',
           '- Thay đổi thông tin: từng trường cũ → mới; dòng hàng đổi Số kiện; file thêm / bớt',
           '- Thay đổi trạng thái: “<cũ> → <mới>”; từ chối kèm lý do', '- Xếp mới nhất lên trên']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', [
           '- Chưa có mốc: “Chưa có lịch sử thao tác nào.”', '- Lọc không ra: “Không có lịch sử phù hợp bộ lọc.”']),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', ['- Đóng cửa sổ'])],
   ev=[('Bấm icon Lịch sử trên dòng', 'Click',
        'Before:\n– Icon luôn hiện; dữ liệu chỉ trả khi người dùng xem được phiếu.\n'
        'During:\n– Nạp các mốc của phiếu; lỗi → hiện thông báo lỗi kèm nút Thử lại.\n'
        'After:\n– Mở cửa sổ “Lịch sử thay đổi: <mã>”, các mốc mới nhất lên trên.'),
       ('Đổi ô lọc (Loại hành động, Người thực hiện, Từ ngày, Đến ngày)', 'Change',
        'Before:\n– Vùng lọc đã mở bằng nút Bộ lọc.\nAfter:\n– Lọc ngay các mốc đang có; không ra mốc nào thì hiện “Không có '
        'lịch sử phù hợp bộ lọc.”.'),
       ('Bấm Làm mới trong vùng lọc', 'Click',
        'Before:\n– Không cần điều kiện.\nAfter:\n– Xóa 4 ô lọc, hiện lại mọi mốc.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không có dữ liệu nhập cần giữ.\nAfter:\n– Đóng cửa sổ; mở lại thì nạp lại lịch sử.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu yêu cầu vận chuyển, bốc xếp; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Dữ liệu lấy theo phiếu YCXH', [
        '– Khách hàng, người liên hệ, số điện thoại, địa điểm giao và dòng hàng (số lượng > 0) lấy từ phiếu YCXH, đọc lại lúc lưu.',
        '– Người dùng chỉ nhập Số kiện từng dòng.', '– Đổi / bỏ Đơn hàng/Hợp đồng thì xóa phiếu YCXH đã chọn.'],
     ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-02', 'Phiếu YCXH chọn được', [
        '– Trạng thái Đã đề nghị, Chờ duyệt, Đang tạo, Đợi TP duyệt, Đợi BGD duyệt (giống ERP) và đã gắn khách hàng.',
        '– Không lọc theo hợp đồng đã chọn.',
        '– Sửa phiếu mà giữ nguyên phiếu YCXH cũ thì không kiểm lại trạng thái.'],
     ['Chọn phiếu YCXH', 'Lập phiếu', 'Chỉnh sửa']),
    ('BR-03', 'Đơn hàng/hợp đồng chọn được', [
        '– 11 loại: ' + ', '.join(CONTRACT_TYPES) + '.',
        '– Hợp đồng bán, Hợp đồng bán (ERP), hợp đồng dịch vụ BH-SC: còn hiệu lực, người lập cùng công ty với người đăng nhập.',
        '– Hợp đồng mua hàng, mua hàng ngoài, mua hàng trong nước, mua đầu kỳ: chỉ hợp đồng đã phát sinh công nợ phải trả '
        'nhà cung cấp.', '– Phiếu xử lý hàng thiếu, xác nhận bảo hành hãng: lọc theo trạng thái như ERP.', '– Hợp đồng bán đầu kỳ, hợp đồng mua dịch vụ: không lọc thêm.'],
     ['Chọn đơn hàng/hợp đồng']),
    ('BR-04', 'Trường bắt buộc khi lưu', [
        '– Lưu nháp và Gửi duyệt cùng bắt buộc Đơn hàng/Hợp đồng, Phiếu YCXH và ít nhất 1 dòng hàng.',
        '– Số kiện, Tổng số kiện: số nguyên 0–2147483647; Ghi chú ≤ 5000 ký tự; Phương thức / Địa điểm bốc xếp ≤ 255 ký tự.',
        '– File đính kèm: pdf, xlsx, xls, jpeg, jpg, png, tối đa 20 MB / file.'],
     ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-05', 'Người duyệt', [
        '– Mọi thủ kho của kho xuất hàng trên phiếu YCXH (và Super admin).',
        '– Gửi duyệt khi kho chưa có thủ kho → chặn; lưu nháp vẫn được.'], ['Lập phiếu', 'Chỉnh sửa', 'Duyệt', 'Từ chối']),
    ('BR-06', 'Vòng đời trạng thái', [
        '– Lưu nháp → Đang tạo; Gửi duyệt → Chờ duyệt.', '– Thủ kho duyệt → Đã duyệt; từ chối (bắt buộc lý do) → Từ chối.',
        '– Sửa / Xóa: chỉ người lập, phiếu Đang tạo hoặc Từ chối; gửi lại sau Từ chối thì xóa lý do, người duyệt, ngày duyệt cũ.',
        '– Phiếu Đã duyệt không sửa, xóa, duyệt lại được.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa', 'Duyệt', 'Từ chối']),
    ('BR-07', 'Duyệt cập nhật phiếu YCXH', [
        '– Duyệt thành công thì phiếu YCXH đổi hình thức vận chuyển thành Công ty vận chuyển.',
        '– Phiếu YCXH không còn ở trạng thái chọn được thì không duyệt được.'], ['Duyệt']),
    ('BR-08', 'Mã phiếu', ['– <mã công ty>.YCVC<tháng năm>.NNNNN, chạy chung dãy số với ERP; không trùng khi nhiều người lưu cùng lúc.'],
     ['Lập phiếu']),
    ('BR-09', 'Phạm vi xem', [
        '– Theo V1 → V4, không có quyền thì phiếu mình lập.',
        '– Luôn thấy thêm phiếu mình đã duyệt / từ chối và phiếu thuộc kho mình là thủ kho.',
        '– Phiếu Đang tạo của người khác luôn ẩn (trừ Super admin ở màn Chi tiết).'],
     ['Xem danh sách', 'Xem chi tiết', 'Xuất Excel', 'Xem lịch sử']),
    ('BR-10', 'Thông báo', [
        '– Gửi duyệt → mọi thủ kho: “[YCVC] Chờ duyệt: <mã>. KH, Phiếu xuất, Ngày giao, Nơi giao, Người lập, Ghi chú”.',
        '– Duyệt → người lập: “[YCVC] Đã duyệt: <mã>. KH, Ngày giao, Người duyệt”.',
        '– Từ chối → người lập: “[YCVC] Từ chối: <mã>. Người từ chối, Lý do”.',
        '– Bấm thông báo mở màn Chi tiết phiếu; lỗi gửi thông báo không làm hỏng thao tác chính.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Duyệt', 'Từ chối']),
    ('BR-11', 'Phiếu đổi trạng thái giữa chừng', [
        '– Người lập / thủ kho thao tác trên phiếu vừa đổi trạng thái ở nơi khác → “Trạng thái đã bị thay đổi. Vui lòng '
        'load lại trang”, không ghi dữ liệu.',
        '– Người không liên quan → thông báo không có quyền tương ứng (sửa / xóa / duyệt / từ chối).'],
     ['Chỉnh sửa', 'Xóa', 'Duyệt', 'Từ chối']),
    ('BR-12', 'Lịch sử thay đổi', [
        '– Ghi: Tạo mới; Thay đổi thông tin (trường, dòng hàng, file); Thay đổi trạng thái (gửi duyệt, duyệt, từ chối kèm lý do); Xóa.',
        '– Xóa file đã lưu ở màn Sửa cũng ghi Thay đổi thông tin.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa', 'Duyệt', 'Từ chối', 'Xem lịch sử']),
    ('BR-13', 'Thao tác xong quay về danh sách', [
        '– Lưu nháp, Gửi duyệt, Duyệt, Từ chối, Xóa ở màn Chi tiết thành công đều quay về màn danh sách.',
        '– Lưu và tiếp tục: ở lại màn Tạo với form trống.'],
     ['Lập phiếu', 'Chỉnh sửa', 'Xóa', 'Duyệt', 'Từ chối']),
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
