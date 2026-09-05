# -*- coding: utf-8 -*-
"""Sinh SRS (.docx) cho man "Phieu chuyen hang nhap thang" (phan he Tai chinh) theo FORM CHUAN
2026-08-28 (ban mau: .claude/skills/srs-documenter/assets/SRS_MAU.docx = SRS Phieu de nghi thu tien).

Anh chup that dung CHUNG voi HDSD: hdsd_product_import_direct_transfer_shots/ (khong commit).

Chay:  python .plans/gop-db/finance-product-import-direct-transfer/gen_srs.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills',
                                'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, 'hdsd_product_import_direct_transfer_shots')
OUT = os.path.join(HERE, 'SRS - Phiếu chuyển hàng nhập thẳng.docx')

HOST = 'http://hrm-crm.eteksofts.com'
ROUTE = '/finance/product-import-direct-transfers'
MENU = 'Phân hệ Tài chính => Điều chuyển => Phiếu chuyển hàng nhập thẳng'

ACTOR_LAP = 'Người lập phiếu'
ACTOR_KT = 'Kế toán kho'


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT, menu=MENU, route=ROUTE, full_url=HOST + ROUTE, img_prefix='pidt_')

# ============================================================== TRANG ĐẦU
d.title_block('Phiếu chuyển hàng nhập thẳng')
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1. GIỚI THIỆU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu chuyển hàng nhập thẳng thuộc phân hệ '
    'Tài chính, nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho trọn vòng đời một '
    'phiếu chuyển hàng nhập thẳng: lập nháp → gửi duyệt → kế toán kho duyệt hoặc từ chối.',
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ cơ chế phạm vi dữ liệu theo bốn cấp quyền xem, kèm quy tắc luôn ẩn phiếu nháp của '
    'người khác.',
    'Làm rõ khác biệt giữa hai nút lưu: Lưu nháp chỉ bắt buộc Người nhận, Lưu và gửi duyệt bắt '
    'buộc đủ cả bảng hàng hóa.',
    'Làm rõ thời điểm tồn hàng nhập thẳng thực sự bị trừ: chỉ khi phiếu được duyệt, không phải '
    'lúc lập phiếu.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hàng nhập thẳng',
     'Hàng mua về giao thẳng cho một nhân viên, không nhập qua kho. Tồn của loại hàng này được '
     'theo dõi theo từng nhân viên chứ không theo kho.'),
    ('Phiếu chuyển hàng nhập thẳng',
     'Chứng từ đề nghị chuyển một phần tồn hàng nhập thẳng từ người lập phiếu sang một nhân viên '
     'khác cùng công ty.'),
    ('Người nhận', 'Nhân viên sẽ đứng tên phần tồn sau khi phiếu được duyệt.'),
    ('Đơn vị cơ bản',
     'Đơn vị nhỏ nhất dùng để quy đổi và ghi nhận tồn. Số lượng nhập theo đơn vị đang chọn được '
     'nhân với hệ số quy đổi để ra số lượng theo đơn vị cơ bản.'),
    ('Tồn hiện có',
     'Số lượng hàng nhập thẳng mà người lập phiếu còn đứng tên tại thời điểm mở phiếu, tính theo '
     'đơn vị cơ bản.'),
    ('Đang tạo', 'Phiếu nháp; chỉ người lập nhìn thấy, sửa và xóa được.'),
    ('Chờ duyệt', 'Phiếu đã gửi, đang chờ Kế toán kho xử lý.'),
    ('Đã duyệt',
     'Kế toán kho đã chấp thuận; tồn đã được trừ của người lập và ghi sang người nhận.'),
    ('Không duyệt',
     'Kế toán kho từ chối kèm lý do bắt buộc; phiếu quay lại cho người lập chỉnh sửa và gửi lại.'),
    ('Chờ tôi duyệt',
     'Cách xem nhanh chỉ liệt kê phiếu đang Chờ duyệt thuộc công ty của người đăng nhập, dành cho '
     'Kế toán kho.'),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2. PHÂN QUYỀN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán kho',
     'Xem được mọi phiếu của công ty mình; hiện nút Duyệt và nút Từ chối ở màn chi tiết của phiếu '
     'đang Chờ duyệt; hiện cách xem nhanh Chờ tôi duyệt.'),
], widths=[0.8, 2.0, 3.2])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu chuyển hàng nhập thẳng theo tổng công ty',
     'Phiếu của mọi công ty trong hệ thống.'),
    ('V2', 'Xem phiếu chuyển hàng nhập thẳng theo công ty',
     'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem phiếu chuyển hàng nhập thẳng theo phòng ban',
     'Phiếu thuộc các phòng ban mà người đăng nhập được giao quản lý.'),
    ('V4', 'Xem phiếu chuyển hàng nhập thẳng theo bộ phận',
     'Phiếu thuộc các bộ phận mà người đăng nhập được giao quản lý.'),
    ('—', '(không có cấp nào)', 'Chỉ phiếu do chính người đăng nhập lập.'),
], widths=[0.8, 2.0, 3.2])
d.p('Ràng buộc bổ sung áp cho mọi cấp: phiếu ở trạng thái Đang tạo của người khác luôn bị ẩn, kể '
    'cả với người có quyền V1. Việc lập phiếu không gắn quyền — mọi người dùng vào được màn hình '
    'đều lập được phiếu của mình. Sửa và xóa chỉ áp cho phiếu do chính mình lập và đang ở trạng '
    'thái Đang tạo hoặc Không duyệt. Duyệt và Từ chối còn đòi thêm điều kiện phiếu phải thuộc '
    'đúng công ty của người xử lý, kể cả với quản trị hệ thống.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1', 'V2', 'V3', 'V4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách phiếu', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc danh sách', '✅', '✅', '✅', '✅', '✅', '✅ (trong phạm vi của mình)'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Lập phiếu chuyển hàng nhập thẳng', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Chọn hàng hóa từ tồn nhập thẳng', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Sửa phiếu', '✅ (phiếu của mình)', '✅ (phiếu của mình)', '✅ (phiếu của mình)',
     '✅ (phiếu của mình)', '✅ (phiếu của mình)', '✅ (phiếu của mình)'),
    ('FR-07 Xem chi tiết phiếu', '✅ (công ty mình)', '✅', '✅ (công ty mình)',
     '✅ (phòng ban mình quản lý)', '✅ (bộ phận mình quản lý)', '✅ (chỉ phiếu của mình)'),
    ('FR-08 Duyệt phiếu', '✅ (công ty mình)', '❌', '❌', '❌', '❌', '❌'),
    ('FR-09 Từ chối phiếu', '✅ (công ty mình)', '❌', '❌', '❌', '❌', '❌'),
    ('FR-10 Xóa phiếu', '✅ (phiếu của mình)', '✅ (phiếu của mình)', '✅ (phiếu của mình)',
     '✅ (phiếu của mình)', '✅ (phiếu của mình)', '✅ (phiếu của mình)'),
    ('FR-11 In phiếu và in danh sách', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-12 Xuất Excel danh sách', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-13 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
], widths=[2.0, 0.62, 0.5, 0.5, 0.5, 0.5, 1.38])

# ================================================ PHẦN 3. ĐẶC TẢ CHI TIẾT
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
# Chi 4 use case duoi day la "man hinh" that su -> noi thang toi actor. Cac thao tac con lai
# deu nam NGAY TREN mot trong 4 man do (loc/cau hinh/xoa/in/xuat o man danh sach; popup chon
# hang trong form lap-sua; duyet, tu choi, lich su o man chi tiet).
d.overview_figure2(
    [(ACTOR_LAP, [0, 1, 2, 3]),
     (ACTOR_KT, [0, 3])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-04', 'Lập phiếu chuyển hàng', 'crud'),
     ('FR-06', 'Sửa phiếu', 'crud'),
     ('FR-07', 'Xem chi tiết phiếu', 'view')],
    [('FR-02', 'Tìm kiếm và lọc danh sách', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-10', 'Xóa phiếu', 'action', 'extend', [0], 'Phiếu của mình, chưa duyệt'),
     ('FR-12', 'Xuất Excel danh sách', 'io', 'extend', [0], None),
     ('FR-05', 'Chọn hàng hóa từ tồn nhập thẳng', 'crud', 'include', [1, 2], None),
     ('FR-08', 'Duyệt phiếu', 'action', 'extend', [3], 'Chỉ Kế toán kho'),
     ('FR-09', 'Từ chối phiếu', 'action', 'extend', [3], 'Chỉ Kế toán kho'),
     ('FR-11', 'In phiếu và in danh sách', 'io', 'extend', [3], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [3],
      'Mở từ danh sách hoặc màn chi tiết')],
    'Sơ đồ Use Case tổng quan màn Phiếu chuyển hàng nhập thẳng')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1 FR-01
d.h3('2.1 Xem danh sách phiếu chuyển hàng nhập thẳng')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Phiếu chuyển hàng nhập thẳng tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem danh sách phiếu chuyển hàng nhập thẳng',
    mota='Hiển thị bảng phiếu nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân trang, sắp '
         'xếp và tổng số bản ghi khớp bộ lọc.',
    tacnhan='Người lập phiếu; Kế toán kho; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và đang ở phân hệ Tài chính.',
    chinh='1. Người dùng vào menu Điều chuyển → Phiếu chuyển hàng nhập thẳng.\n'
          '2. Hệ thống xác định cấp quyền xem theo thứ tự V1 → V2 → V3 → V4; không có cấp nào '
          'thì giới hạn ở phiếu do chính người đó lập.\n'
          '3. Hệ thống loại bỏ phiếu ở trạng thái Đang tạo của người khác.\n'
          '4. Hệ thống trả về trang đầu tiên, sắp xếp phiếu lập gần nhất lên trước, kèm tổng số '
          'bản ghi.\n'
          '5. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện dòng báo không có dữ liệu.\n'
        '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó thay cho bộ cột mặc định.\n'
        '• Người có quyền Kế toán kho → hiện thêm cách xem nhanh Chờ tôi duyệt.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách Phiếu chuyển hàng nhập thẳng lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Phiếu chuyển hàng nhập thẳng',
     'Hiển thị trên thanh tiêu đề và tiêu đề bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Không gắn quyền; mở màn lập phiếu.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'In danh sách phiếu đang lọc, khổ ngang.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ chọn trường cần xuất.'),
    ('Nút Tuỳ chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ chọn cột hiển thị và thứ tự cột.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cột bắt buộc, không ẩn và không đổi vị trí được.'),
    ('Cột Số phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết; sắp xếp được; cột bắt buộc.'),
    ('Cột Người nhận', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Nhân viên sẽ nhận hàng; hiển thị mặc định.'),
    ('Cột Công ty', 'Table/Grid', 'Read-only', '–', 'Ẩn',
     'Ẩn mặc định, bật trong Tuỳ chỉnh cột.'),
    ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Ẩn',
     'Phòng ban của người nhận; ẩn mặc định.'),
    ('Cột Ghi chú', 'Table/Grid', 'Read-only', '–', 'Ẩn', 'Ẩn mặc định; tự xuống dòng khi dài.'),
    ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Ẩn',
     'Ẩn mặc định; trống khi phiếu chưa được xử lý.'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Hiển thị mặc định.'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Ẩn', 'Ẩn mặc định.'),
    ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn', 'Ẩn mặc định.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 4 giá trị', 'Theo dữ liệu',
     'Đang tạo, Chờ duyệt, Đã duyệt, Không duyệt.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo quyền và trạng thái',
     'Cột bắt buộc. Chứa Sửa, Xóa, Duyệt và nút ba chấm (In, Lịch sử).'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc, không phải tổng toàn hệ thống.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách', '10',
     'Đổi giá trị thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
     'Có nút về đầu / lùi / số trang / tiến / về cuối.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', 'Hiện khi không có phiếu nào khớp.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Ẩn', 'Hiện trong lúc nạp dữ liệu.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định cấp quyền xem theo thứ tự V1 → V2 → V3 → V4; không có cấp nào thì giới '
     'hạn ở phiếu do chính người dùng lập.\n'
     'During:\n– Áp phạm vi dữ liệu; loại bỏ phiếu Đang tạo của người khác.\n'
     '– Khôi phục bộ lọc đã lưu gần nhất và cấu hình cột của người dùng.\n'
     'After:\n– Trả về trang 1, sắp xếp theo ngày tạo giảm dần, kèm tổng số bản ghi.'),
    ('Bấm vào số phiếu', 'Click',
     'After:\n– Mở màn chi tiết của phiếu tương ứng (FR-07).\n'
     '– Bấm chuột phải cho phép mở ở tab mới.'),
    ('Bấm tiêu đề cột có sắp xếp', 'Click',
     'Before:\n– Chỉ hai cột Số phiếu và Ngày tạo hỗ trợ sắp xếp.\n'
     'After:\n– Đổi chiều sắp xếp, quay về trang 1 và nạp lại danh sách.'),
    ('Bấm biểu tượng Duyệt trên dòng', 'Click',
     'Before:\n– Biểu tượng chỉ hiện với phiếu đang Chờ duyệt mà người dùng có quyền xử lý.\n'
     'After:\n– Mở màn CHI TIẾT của phiếu, không duyệt ngay tại danh sách, để người duyệt xem '
     'hàng hóa trước.'),
    ('Bấm số trang / nút tiến lùi', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'),
    ('Đổi Số dòng/trang', 'Change',
     'After:\n– Quay về trang 1 và nạp lại danh sách theo số dòng mới.'),
])

# ---------------------------------------------------------------- 2.2 FR-02
d.h3('2.2 Tìm kiếm và lọc danh sách')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown và Phân trang. Chỉ bổ sung các tiêu chí tìm '
           'kiếm và lọc riêng của Phiếu chuyển hàng nhập thẳng.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu',
    mota='Thu hẹp danh sách theo số phiếu, cấp tổ chức, trạng thái, tên hoặc mã hàng hóa, người '
         'nhận, người tạo và khoảng ngày tạo.',
    tacnhan='Người lập phiếu; Kế toán kho; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách.',
    chinh='1. Người dùng bấm Tìm kiếm nâng cao để mở khối tiêu chí.\n'
          '2. Người dùng chọn hoặc nhập giá trị cho một hoặc nhiều tiêu chí.\n'
          '3. Hệ thống lọc ngay khi giá trị thay đổi và quay về trang 1.\n'
          '4. Riêng ô tìm nhanh chỉ lọc khi người dùng bấm nút Tìm kiếm hoặc nhấn Enter.\n'
          '5. Hệ thống ghi nhớ bộ lọc để khôi phục khi người dùng quay lại màn hình.',
    phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, nạp lại danh sách từ trang 1.\n'
        '• Không có kết quả → bảng hiện dòng báo không có dữ liệu.\n'
        '• Đổi Công ty → hệ thống xóa giá trị đang chọn ở Phòng ban và Bộ phận.\n'
        '• Tiêu chí bị tắt trong Cài đặt bộ lọc → giá trị của tiêu chí đó cũng bị xóa, danh sách '
        'không bị lọc ngầm.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('02-bo-loc-nang-cao.png'),
         shot_caption='Khối Tìm kiếm nâng cao ở trạng thái mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo số phiếu hoặc người tạo; chỉ lọc khi bấm Tìm kiếm.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Áp giá trị ô tìm nhanh và quay về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Xóa toàn bộ tiêu chí đang lọc và nạp lại danh sách.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở hoặc thu gọn khối tiêu chí.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở cửa sổ chọn tiêu chí hiển thị (FR-03).'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Chỉ hiện với người có quyền V1.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Chỉ liệt kê phòng ban của công ty đang chọn.'),
    ('Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Chỉ liệt kê bộ phận của phòng ban đang chọn.'),
    ('Số phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo một phần số phiếu.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống',
     'Đang tạo, Chờ duyệt, Đã duyệt, Không duyệt.'),
    ('Tên/mã hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm phiếu có chứa hàng hóa khớp tên hoặc mã.'),
    ('Người nhận', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Danh sách nhân viên tìm từ xa theo từ khóa.'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Chọn nhân sự đã lập phiếu.'),
    ('Ngày tạo từ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc phiếu lập từ ngày này trở đi.'),
    ('Ngày tạo đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc phiếu lập đến hết ngày này.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Đổi giá trị một tiêu chí nâng cao', 'Change',
     'During:\n– Gom các tiêu chí đang có giá trị thành một điều kiện lọc.\n'
     'After:\n– Nạp lại danh sách từ trang 1 và ghi nhớ bộ lọc.'),
    ('Bấm nút Tìm kiếm', 'Click',
     'After:\n– Áp thêm từ khóa của ô tìm nhanh, nạp lại danh sách từ trang 1.'),
    ('Nhấn Enter trong ô tìm nhanh', 'Keypress', 'After:\n– Xử lý như bấm nút Tìm kiếm.'),
    ('Bấm nút Làm mới', 'Click',
     'During:\n– Xóa mọi tiêu chí nâng cao và ô tìm nhanh.\n'
     'After:\n– Nạp lại danh sách đầy đủ trong phạm vi dữ liệu, từ trang 1.'),
    ('Đổi Công ty', 'Change',
     'After:\n– Xóa giá trị Phòng ban và Bộ phận đang chọn, nạp lại danh mục phòng ban theo công '
     'ty mới.'),
])

# ---------------------------------------------------------------- 2.3 FR-03
d.h3('2.3 Cài đặt bộ lọc và tuỳ chỉnh cột')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view',
            [('include', 'Lưu cấu hình theo từng người dùng'),
             ('extend', 'Khôi phục cấu hình mặc định')],
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Quy tắc Cấu hình cột và lưu cấu hình theo người dùng. Chỉ bổ sung danh mục tiêu chí '
           'và danh mục cột riêng của màn này.', anchor='excel')
d.intro_table(
    ten='Cài đặt bộ lọc và tuỳ chỉnh cột hiển thị',
    mota='Cho phép mỗi người dùng tự chọn những tiêu chí lọc và những cột muốn thấy trên bảng, '
         'cấu hình được lưu riêng cho từng người.',
    tacnhan='Người lập phiếu; Kế toán kho; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách.',
    chinh='1. Người dùng bấm Cài đặt bộ lọc hoặc biểu tượng Tuỳ chỉnh cột.\n'
          '2. Hệ thống mở cửa sổ kèm danh sách tiêu chí hoặc danh sách cột kèm ô tích chọn.\n'
          '3. Người dùng tích hoặc bỏ tích, có thể kéo đổi thứ tự cột.\n'
          '4. Người dùng bấm nút lưu.\n'
          '5. Hệ thống lưu cấu hình cho riêng người dùng và áp ngay vào màn hình.',
    phu='• Bỏ tích một tiêu chí đang có giá trị lọc → giá trị đó bị xóa để danh sách không bị lọc '
        'ngầm.\n'
        '• Ba cột STT, Số phiếu và Hành động luôn hiển thị và không đổi vị trí được.\n'
        '• Đóng cửa sổ mà không lưu → giữ nguyên cấu hình cũ.',
    dacbiet=None)

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc',
         note='Hai cửa sổ Cài đặt bộ lọc và Tuỳ chỉnh cột được mở ngay trên màn danh sách theo '
              'đường dẫn ở trên.',
         shot=shot('03-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('04-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột', width_in=6.2)

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc / Tuỳ chỉnh cột',
     'Theo cửa sổ đang mở.'),
    ('Danh sách tiêu chí lọc', 'Table/Grid', 'Enable', 'Danh sách', 'Không', 'Theo cấu hình đã lưu',
     'Mỗi dòng là một tiêu chí kèm ô tích chọn.'),
    ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách', 'Không', 'Theo cấu hình đã lưu',
     'Mỗi dòng là một cột kèm ô tích chọn; kéo thả để đổi thứ tự.'),
    ('Ô tích của cột bắt buộc', 'Icon Button', 'Disable', '–', '–', 'Đang tích',
     'STT, Số phiếu và Hành động không bỏ tích được.'),
    ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích toàn bộ dòng trong danh sách.'),
    ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Bỏ tích toàn bộ trừ các mục bắt buộc.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình cho người dùng hiện tại.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, bỏ qua thay đổi.'),
])

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc / Tuỳ chỉnh cột', 'Click',
     'After:\n– Mở cửa sổ tương ứng, nạp cấu hình đang lưu của người dùng.'),
    ('Tích / bỏ tích một dòng', 'Change',
     'Before:\n– Mục bắt buộc không cho bỏ tích.\n'
     'After:\n– Cập nhật lựa chọn tạm trong cửa sổ, chưa áp lên màn hình.'),
    ('Kéo thả đổi thứ tự cột', 'Change',
     'Before:\n– Ba cột bắt buộc giữ nguyên vị trí.\n'
     'After:\n– Cập nhật thứ tự tạm trong cửa sổ.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi cấu hình theo từng người dùng.\n'
     'After:\n– Đóng cửa sổ, áp cấu hình mới vào bảng; tiêu chí bị tắt thì xóa luôn giá trị đang '
     'lọc và nạp lại danh sách.'),
])

# ---------------------------------------------------------------- 2.4 FR-04
d.h3('2.4 Lập phiếu chuyển hàng nhập thẳng')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Lập phiếu chuyển hàng nhập thẳng', 'crud',
            [('include', 'Chọn hàng hóa từ tồn nhập thẳng'),
             ('include', 'Kiểm tra đủ tồn của người lập'),
             ('extend', 'Gửi duyệt và thông báo cho Kế toán kho')],
            caption='Biểu đồ Use Case — FR-04 Lập phiếu chuyển hàng nhập thẳng')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung các quy tắc riêng '
           'của Phiếu chuyển hàng nhập thẳng.', anchor='create')
d.intro_table(
    ten='Lập phiếu chuyển hàng nhập thẳng',
    mota='Tạo phiếu đề nghị chuyển một phần tồn hàng nhập thẳng của chính người lập sang một nhân '
         'viên khác cùng công ty; lưu nháp hoặc gửi Kế toán kho duyệt.',
    tacnhan='Người lập phiếu; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập; chức năng không gắn quyền riêng.',
    chinh='1. Người dùng bấm Tạo mới ở màn danh sách.\n'
          '2. Người dùng chọn Người nhận; hệ thống tự điền Phòng ban của người nhận và khóa ô đó.\n'
          '3. Người dùng bấm Thêm hàng hóa, chọn hàng từ tồn nhập thẳng của mình (FR-05).\n'
          '4. Người dùng chọn đơn vị tính và nhập số lượng cho từng dòng; hệ thống quy đổi ra số '
          'lượng theo đơn vị cơ bản.\n'
          '5. Người dùng bấm Lưu nháp hoặc Lưu và gửi duyệt.\n'
          '6. Hệ thống kiểm tra dữ liệu, sinh số phiếu, lưu phiếu và quay về màn danh sách.',
    phu='• Bấm Lưu nháp → chỉ bắt buộc Người nhận, bảng hàng hóa để trống vẫn lưu được, phiếu ở '
        'trạng thái Đang tạo.\n'
        '• Bấm Lưu và gửi duyệt → bắt buộc có ít nhất một dòng hàng hợp lệ, phiếu chuyển sang Chờ '
        'duyệt và hệ thống thông báo cho Kế toán kho cùng công ty.\n'
        '• Số lượng vượt tồn hiện có → báo đỏ ngay tại dòng, giữ nguyên con số vừa nhập.\n'
        '• Rời màn khi còn thay đổi chưa lưu → hệ thống hỏi xác nhận trước khi rời.\n'
        '• Hàng đã bị chuyển bớt sau lúc mở form → khi lưu hệ thống báo rõ hàng nào không đủ.',
    dacbiet='Tồn hàng nhập thẳng CHƯA bị trừ ở bước này; tồn chỉ thay đổi khi Kế toán kho duyệt '
            'phiếu.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới',
         shot=shot('09-form-tao-moi.png'),
         shot_caption='Form lập phiếu chuyển hàng nhập thẳng')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Người nhận', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống',
     'Chỉ liệt kê nhân viên cùng công ty với người lập và loại trừ chính người lập.'),
    ('Phòng ban', 'Textbox', 'Read-only', '–', 'Không', 'Trống',
     'Tự điền theo người nhận; ô khóa kèm biểu tượng giải thích.'),
    ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Vượt 255 ký tự thì báo “Không được nhập quá 255 ký tự”.'),
    ('Nút Thêm hàng hóa', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở cửa sổ chọn hàng từ tồn nhập thẳng (FR-05).'),
    ('Cột STT của bảng hàng hóa', 'Table/Grid', 'Read-only', '–', '–', 'Số thứ tự liên tục', '–'),
    ('Cột Tên hàng', 'Table/Grid', 'Read-only', '–', 'Có', 'Theo dữ liệu đã chọn',
     'Không sửa tay được, chỉ lấy từ cửa sổ chọn hàng.'),
    ('Cột Mã hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu đã chọn', '–'),
    ('Cột ĐVT', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Đơn vị mặc định của hàng',
     'Đổi đơn vị thì hệ thống tính lại số lượng theo hệ số quy đổi.'),
    ('Cột Số lượng', 'Textbox', 'Enable', '> 0 và ≤ tồn hiện có', 'Có', 'Trống',
     'Chỉ nhận chữ số, dấu chấm thập phân và dấu phẩy hàng nghìn; ký tự khác bị loại ngay khi gõ '
     'hoặc dán.'),
    ('Cột SL theo ĐV cơ bản', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo tính toán',
     'Bằng số lượng nhân hệ số quy đổi của đơn vị đang chọn.'),
    ('Cột Tồn hiện có', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
     'Tồn hàng nhập thẳng của người lập phiếu tại thời điểm mở form.'),
    ('Nút Xóa dòng hàng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Xóa dòng hàng khỏi phiếu, không hỏi xác nhận.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu phiếu ở trạng thái Đang tạo.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu và chuyển phiếu sang trạng thái Chờ duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Về màn danh sách; hỏi xác nhận nếu còn thay đổi chưa lưu.'),
    ('Thông báo lỗi tại ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện ngay dưới ô sai kèm viền đỏ.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Người nhận', 'Change',
     'During:\n– Lấy phòng ban của người nhận và điền vào ô Phòng ban đang khóa.\n'
     'After:\n– Ô Người nhận hết báo đỏ nếu trước đó đang thiếu.'),
    ('Đổi ĐVT của một dòng hàng', 'Change',
     'During:\n– Tính lại số lượng theo hệ số quy đổi của đơn vị mới.\n'
     'After:\n– Cập nhật cột SL theo ĐV cơ bản và kiểm tra lại điều kiện không vượt tồn.'),
    ('Nhập Số lượng', 'Keypress',
     'During:\n– Loại bỏ mọi ký tự không phải chữ số, dấu chấm thập phân hoặc dấu phẩy hàng nghìn, '
     'kể cả khi dán từ nơi khác.\n'
     '– Số lượng lớn hơn tồn hiện có → báo đỏ “Chỉ còn … theo đơn vị đang chọn” và GIỮ NGUYÊN con '
     'số vừa nhập.\n'
     'After:\n– Cập nhật cột SL theo ĐV cơ bản.'),
    ('Bấm Lưu nháp', 'Click',
     'Before:\n– Người nhận trống → hiển thị “Bắt buộc phải nhập” và dừng xử lý.\n'
     'During:\n– Bảng hàng hóa được phép để trống; dòng hàng nào có thì vẫn phải đủ đơn vị tính và '
     'số lượng lớn hơn 0.\n'
     '– Kiểm tra tổng số lượng từng mặt hàng không vượt tồn của người lập.\n'
     'After:\n– Sinh số phiếu, lưu phiếu ở trạng thái Đang tạo, ghi một dòng lịch sử tạo mới.\n'
     '– Hiển thị thông báo lưu thành công và quay về màn danh sách.'),
    ('Bấm Lưu và gửi duyệt', 'Click',
     'Before:\n– Người nhận trống → “Bắt buộc phải nhập”.\n'
     '– Bảng hàng hóa trống → “Bắt buộc phải nhập”.\n'
     '– Dòng hàng thiếu đơn vị tính hoặc số lượng → báo đỏ tại đúng dòng, mọi dòng sai đều được '
     'đánh dấu.\n'
     '– Số lượng bằng 0 → “Số lượng phải lớn hơn 0”.\n'
     '– Có bất kỳ lỗi nào → không thực hiện bước After.\n'
     'During:\n– Gộp các dòng cùng một mặt hàng rồi so với tồn của người lập; thiếu thì báo rõ tên '
     'hàng không đủ số lượng.\n'
     'After:\n– Lưu phiếu ở trạng thái Chờ duyệt, ghi lịch sử gửi duyệt.\n'
     '– Gửi thông báo cho những người có quyền Kế toán kho cùng công ty với phiếu.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
    ('Bấm Quay lại khi còn thay đổi chưa lưu', 'Click',
     'Before:\n– Hệ thống hỏi xác nhận rời màn.\n'
     'After:\n– Đồng ý thì về danh sách và bỏ thay đổi; từ chối thì ở lại form.'),
])

# ---------------------------------------------------------------- 2.5 FR-05
d.h3('2.5 Chọn hàng hóa từ tồn nhập thẳng')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chọn hàng hóa từ tồn nhập thẳng', 'crud',
            [('include', 'Tra tồn hàng nhập thẳng theo nhân viên'),
             ('extend', 'Tìm theo tên hoặc mã hàng')],
            caption='Biểu đồ Use Case — FR-05 Chọn hàng hóa từ tồn nhập thẳng')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Quy tắc cửa sổ chọn dữ liệu, tìm kiếm trong cửa sổ và phân trang.', anchor='search')
d.intro_table(
    ten='Chọn hàng hóa từ tồn hàng nhập thẳng của nhân viên',
    mota='Liệt kê những mặt hàng nhập thẳng mà người lập phiếu còn tồn, cho tích chọn nhiều dòng '
         'một lần rồi đưa vào bảng hàng hóa của phiếu.',
    tacnhan='Người lập phiếu; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở form lập phiếu hoặc form sửa phiếu.',
    chinh='1. Người dùng bấm Thêm hàng hóa.\n'
          '2. Hệ thống mở cửa sổ Tồn hàng nhập thẳng của nhân viên và nạp danh sách hàng còn tồn.\n'
          '3. Người dùng nhập từ khóa để thu hẹp danh sách nếu cần.\n'
          '4. Người dùng tích chọn một hoặc nhiều dòng.\n'
          '5. Người dùng bấm nút Chọn; hệ thống thêm các dòng đã chọn vào bảng hàng hóa của phiếu.',
    phu='• Ở form sửa phiếu, danh sách lấy theo tồn của NGƯỜI LẬP phiếu, không phải người đang '
        'đăng nhập.\n'
        '• Hàng đã có trong phiếu không hiện lại trong cửa sổ để tránh trùng dòng.\n'
        '• Người lập không còn tồn nhập thẳng nào → cửa sổ hiện danh sách rỗng.\n'
        '• Đóng cửa sổ mà không bấm Chọn → phiếu giữ nguyên.',
    dacbiet=None)

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Thêm hàng hóa',
         note='Cửa sổ Tồn hàng nhập thẳng của nhân viên được mở ngay trên form lập hoặc sửa phiếu '
              'theo đường dẫn ở trên.',
         shot=shot('10-popup-chon-hang.png'),
         shot_caption='Cửa sổ chọn hàng từ tồn hàng nhập thẳng của nhân viên')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tồn hàng nhập thẳng của nhân viên', '–'),
    ('Ô tìm kiếm', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo tên hoặc mã hàng.'),
    ('Ô tích chọn dòng', 'Icon Button', 'Enable', '–', 'Không', 'Chưa tích',
     'Tích được nhiều dòng, giữ lựa chọn khi chuyển trang.'),
    ('Cột Tên hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '–'),
    ('Cột Mã hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '–'),
    ('Cột ĐVT', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Đơn vị cơ bản của mặt hàng.'),
    ('Cột Số lượng tồn', 'Table/Grid', 'Read-only', '> 0', '–', 'Theo dữ liệu',
     'Tồn của người lập phiếu theo đơn vị cơ bản.'),
    ('Phân trang trong cửa sổ', 'Pagination', 'Enable', '–', '–', 'Trang 1', '–'),
    ('Nút Chọn (n)', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Số trong ngoặc là số dòng đang tích; chưa tích dòng nào thì không thêm gì.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, bỏ lựa chọn.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở cửa sổ chọn hàng', 'System',
     'Before:\n– Xác định chủ tồn cần tra: form lập là người đăng nhập, form sửa là người lập '
     'phiếu.\n'
     'During:\n– Nạp danh sách hàng còn tồn của chủ tồn đó, loại các mặt hàng đã có trong phiếu.\n'
     'After:\n– Hiển thị trang đầu tiên.'),
    ('Nhập từ khóa tìm kiếm', 'Change',
     'After:\n– Lọc danh sách theo tên hoặc mã hàng và quay về trang 1.'),
    ('Tích chọn dòng', 'Change',
     'After:\n– Cập nhật số đếm trên nút Chọn; lựa chọn được giữ khi chuyển trang.'),
    ('Bấm nút Chọn', 'Click',
     'During:\n– Thêm mỗi dòng đã tích thành một dòng hàng của phiếu, đơn vị tính đặt mặc định '
     'theo hàng.\n'
     'After:\n– Đóng cửa sổ; các dòng mới hiện ở cuối bảng hàng hóa, số lượng để trống chờ nhập.'),
])

# ---------------------------------------------------------------- 2.6 FR-06
d.h3('2.6 Sửa phiếu')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Sửa phiếu', 'crud',
            [('include', 'Kiểm tra phiếu do chính mình lập và chưa duyệt'),
             ('include', 'Chọn hàng hóa từ tồn nhập thẳng'),
             ('extend', 'Gửi duyệt lại sau khi bị từ chối')],
            caption='Biểu đồ Use Case — FR-06 Sửa phiếu')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Chỉ bổ sung điều kiện được sửa '
           'và cách xử lý phiếu bị từ chối.', anchor='create')
d.intro_table(
    ten='Sửa phiếu chuyển hàng nhập thẳng',
    mota='Chỉnh sửa người nhận, ghi chú và bảng hàng hóa của phiếu do chính mình lập khi phiếu '
         'chưa được duyệt.',
    tacnhan='Người lập phiếu; Người dùng đã đăng nhập',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Đang tạo hoặc Không duyệt.',
    chinh='1. Người dùng bấm Sửa ở màn danh sách hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở form kèm dữ liệu hiện có của phiếu.\n'
          '3. Người dùng chỉnh các trường và bảng hàng hóa.\n'
          '4. Người dùng bấm Lưu nháp hoặc Lưu và gửi duyệt.\n'
          '5. Hệ thống kiểm tra dữ liệu, lưu phiếu và quay về màn danh sách.',
    phu='• Phiếu đã Chờ duyệt hoặc Đã duyệt → nút Sửa không hiển thị.\n'
        '• Phiếu bị người khác đổi trạng thái trong lúc đang sửa → hệ thống từ chối lưu và yêu cầu '
        'tải lại.\n'
        '• Phiếu bị xóa trong lúc đang sửa → hệ thống báo không tìm thấy dữ liệu và đưa về danh '
        'sách.\n'
        '• Phiếu Không duyệt được sửa rồi gửi duyệt lại → quay về trạng thái Chờ duyệt và thông '
        'báo lại cho Kế toán kho.',
    dacbiet='Danh sách hàng trong cửa sổ chọn hàng lấy theo tồn của NGƯỜI LẬP phiếu, kể cả khi '
            'người đang sửa là quản trị hệ thống.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa',
         shot=shot('13-man-sua.png'),
         shot_caption='Form sửa phiếu với dữ liệu đã có')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Số phiếu', 'Textbox', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Ô khóa; số phiếu do hệ thống sinh, không sửa được.'),
    ('Trạng thái', 'Badge', 'Read-only', 'Danh sách 4 giá trị', '–', 'Theo dữ liệu', '–'),
    ('Người nhận', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Theo dữ liệu',
     'Vẫn loại trừ người lập phiếu.'),
    ('Phòng ban', 'Textbox', 'Read-only', '–', 'Không', 'Theo người nhận', 'Ô khóa.'),
    ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Theo dữ liệu', '–'),
    ('Bảng hàng hóa', 'Table/Grid', 'Enable', '–', 'Có khi gửi duyệt', 'Theo dữ liệu',
     'Thêm, sửa số lượng, đổi đơn vị và xóa dòng như ở form lập phiếu.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Giữ phiếu ở trạng thái Đang tạo.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Chuyển phiếu sang Chờ duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu còn thay đổi chưa lưu.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở form sửa', 'System',
     'Before:\n– Kiểm tra phiếu do chính người dùng lập và đang ở trạng thái Đang tạo hoặc Không '
     'duyệt; không thỏa thì báo không có quyền và đưa về danh sách.\n'
     'After:\n– Nạp dữ liệu phiếu vào form và ghi nhận trạng thái ban đầu để so sánh thay đổi.'),
    ('Bấm Lưu nháp / Lưu và gửi duyệt', 'Click',
     'Before:\n– Áp cùng bộ kiểm tra của form lập phiếu.\n'
     '– Phiếu đã bị người khác đổi trạng thái → từ chối lưu và yêu cầu tải lại trang.\n'
     'During:\n– Ghi lại bảng hàng hóa theo đúng danh sách hiện có trên form.\n'
     'After:\n– Lưu phiếu, ghi lịch sử theo từng trường và từng dòng hàng đã đổi.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
    ('Mở phiếu vừa bị xóa', 'System',
     'After:\n– Hiển thị “Không tìm thấy dữ liệu” và chuyển về màn danh sách.'),
])

# ---------------------------------------------------------------- 2.7 FR-07
d.h3('2.7 Xem chi tiết phiếu')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung bố cục và điều kiện hiện nút của màn '
           'này.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu chuyển hàng nhập thẳng',
    mota='Hiển thị toàn bộ thông tin phiếu ở chế độ chỉ đọc, kèm khối lịch sử thay đổi và các nút '
         'thao tác theo quyền và trạng thái.',
    tacnhan='Người lập phiếu; Kế toán kho; Người dùng đã đăng nhập',
    dieukien='Phiếu nằm trong phạm vi dữ liệu của người đăng nhập.',
    chinh='1. Người dùng bấm số phiếu ở màn danh sách.\n'
          '2. Hệ thống kiểm tra người dùng có được xem phiếu này không.\n'
          '3. Hệ thống hiển thị thông tin chung, bảng hàng hóa và khối lịch sử ở dạng thu gọn.\n'
          '4. Hệ thống hiển thị các nút thao tác đúng theo quyền và trạng thái của phiếu.',
    phu='• Phiếu ngoài phạm vi dữ liệu → báo không có quyền và đưa về danh sách.\n'
        '• Phiếu không tồn tại hoặc vừa bị xóa → báo không tìm thấy dữ liệu và đưa về danh sách.\n'
        '• Phiếu Đã duyệt hoặc Không duyệt → hiện thêm người duyệt; phiếu bị từ chối hiện lý do.\n'
        '• Người không phải Kế toán kho → không thấy nút Duyệt và Từ chối.',
    dacbiet=None)

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết',
         shot=shot('11-chi-tiet-cho-duyet.png'),
         shot_caption='Màn chi tiết một phiếu đang Chờ duyệt, nhìn bằng tài khoản Kế toán kho')

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu chuyển hàng nhập thẳng: <số phiếu>',
     '–'),
    ('Người nhận', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', 'Ô khóa.'),
    ('Phòng ban', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', 'Ô khóa.'),
    ('Số phiếu', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', 'Ô khóa.'),
    ('Trạng thái', 'Badge', 'Read-only', 'Danh sách 4 giá trị', 'Theo dữ liệu', '–'),
    ('Ghi chú', 'Textarea', 'Read-only', '–', 'Theo dữ liệu', 'Ô khóa; để trống nếu không có.'),
    ('Người duyệt', 'Textbox', 'Read-only', '–', 'Theo dữ liệu',
     'Trống khi phiếu chưa được duyệt hoặc từ chối.'),
    ('Bảng hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm Tên hàng, Mã hàng, ĐVT, Số lượng, SL theo ĐV cơ bản và Tồn hiện có.'),
    ('Khối Lịch sử thay đổi', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Bấm Xem lịch sử mới nạp dữ liệu (FR-13).'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Theo quyền và trạng thái',
     'Chỉ hiện với người lập phiếu khi phiếu Đang tạo hoặc Không duyệt.'),
    ('Nút Duyệt', 'Button', 'Enable / Ẩn', '–', 'Theo quyền và trạng thái',
     'Chỉ hiện với Kế toán kho cùng công ty khi phiếu Chờ duyệt.'),
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Theo quyền và trạng thái',
     'Điều kiện hiện giống nút Duyệt.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Mở màn in phiếu (FR-11).'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Theo quyền và trạng thái',
     'Điều kiện hiện giống nút Sửa.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra phiếu nằm trong phạm vi dữ liệu của người dùng: là phiếu của chính mình, '
     'hoặc thuộc công ty mình khi có quyền Kế toán kho, hoặc khớp một trong bốn cấp quyền xem.\n'
     '– Không thỏa → báo không có quyền và chuyển về danh sách.\n'
     'During:\n– Nạp thông tin phiếu, bảng hàng hóa và các cờ cho biết được sửa, xóa hay duyệt.\n'
     'After:\n– Hiển thị dữ liệu ở chế độ chỉ đọc và các nút đúng theo cờ đã nhận.'),
    ('Bấm Xem lịch sử', 'Click',
     'After:\n– Nạp và hiển thị các mốc lịch sử của phiếu, mới nhất lên trước (FR-13).'),
    ('Bấm Quay lại', 'Click',
     'After:\n– Về màn danh sách, giữ nguyên bộ lọc và trang đang xem trước đó.'),
])

# ---------------------------------------------------------------- 2.8 FR-08
d.h3('2.8 Duyệt phiếu')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Duyệt phiếu', 'action',
            [('include', 'Kiểm tra quyền Kế toán kho và cùng công ty'),
             ('include', 'Trừ tồn của người lập và ghi tồn cho người nhận'),
             ('extend', 'Thông báo kết quả cho người lập phiếu')],
            caption='Biểu đồ Use Case — FR-08 Duyệt phiếu', actor=ACTOR_KT)

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX của thao tác đổi trạng thái.', anchor='notice')
d.intro_table(
    ten='Duyệt phiếu chuyển hàng nhập thẳng',
    mota='Kế toán kho chấp thuận phiếu; hệ thống trừ tồn hàng nhập thẳng của người lập và ghi phần '
         'tồn tương ứng sang người nhận.',
    tacnhan='Kế toán kho',
    dieukien='Phiếu đang ở trạng thái Chờ duyệt và thuộc đúng công ty của người duyệt.',
    chinh='1. Kế toán kho mở màn chi tiết của phiếu đang Chờ duyệt.\n'
          '2. Kế toán kho xem lại bảng hàng hóa rồi bấm Duyệt.\n'
          '3. Hệ thống hiện hộp Xác nhận duyệt.\n'
          '4. Kế toán kho bấm Xác nhận.\n'
          '5. Hệ thống trừ tồn của người lập theo thứ tự lô hàng có trước dùng trước, ghi tồn cho '
          'người nhận và chuyển phiếu sang Đã duyệt.\n'
          '6. Hệ thống báo duyệt thành công và quay về màn danh sách.',
    phu='• Hàng đã bị chuyển hoặc dùng bớt sau lúc lập phiếu → hệ thống chặn, báo rõ hàng nào, cần '
        'bao nhiêu và hiện còn bao nhiêu; phiếu giữ nguyên trạng thái Chờ duyệt.\n'
        '• Phiếu không còn dòng hàng nào có số lượng → hệ thống chặn, không cho duyệt một phiếu '
        'rỗng.\n'
        '• Phiếu vừa được người khác xử lý → hệ thống từ chối và yêu cầu tải lại trang.\n'
        '• Bấm Hủy ở hộp xác nhận → không có gì thay đổi.',
    dacbiet='Đây là thao tác GHI TỒN THẬT và không hoàn tác được; vì vậy hệ thống không cho duyệt '
            'thẳng từ màn danh sách mà bắt buộc mở màn chi tiết.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Duyệt',
         note='Hộp Xác nhận duyệt được mở ngay trên màn chi tiết theo đường dẫn ở trên.',
         shot=shot('17-xac-nhan-duyet.png'),
         shot_caption='Hộp thoại Xác nhận duyệt phiếu')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận duyệt', '–'),
    ('Câu hỏi xác nhận', 'Label', 'Hiển thị', 'Bạn xác nhận duyệt phiếu?', '–'),
    ('Nút Xác nhận', 'Button', 'Enable', 'Hiển thị', 'Thực hiện duyệt phiếu.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không thay đổi gì.'),
    ('Nút đóng ở góc phải', 'Icon Button', 'Enable', 'Hiển thị', 'Tương đương nút Hủy.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     'Hiện thông báo thành công, hoặc câu báo lỗi nêu rõ hàng nào không đủ.'),
], required=False, scope=False)

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Duyệt', 'Click',
     'Before:\n– Kiểm tra người dùng có quyền Kế toán kho và phiếu thuộc đúng công ty của người '
     'đó; phiếu phải đang Chờ duyệt.\n'
     'After:\n– Mở hộp Xác nhận duyệt.'),
    ('Bấm Xác nhận trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra lại quyền và trạng thái phiếu.\n'
     '– Phiếu không còn dòng hàng nào có số lượng → hiển thị “Phiếu không có dòng hàng hóa nào để '
     'chuyển.” và dừng xử lý.\n'
     'During:\n– Với từng mặt hàng, khóa các lô tồn của người lập rồi trừ dần theo thứ tự lô có '
     'trước dùng trước.\n'
     '– Tồn không đủ → hiển thị câu báo nêu rõ tên hàng, số cần và số còn lại; toàn bộ thao tác bị '
     'hủy, phiếu giữ nguyên trạng thái.\n'
     'After:\n– Chuyển phiếu sang Đã duyệt, ghi người duyệt.\n'
     '– Ghi nhận biến động tồn của cả người lập và người nhận.\n'
     '– Ghi một dòng lịch sử duyệt phiếu và gửi thông báo cho người lập.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
    ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp thoại, phiếu và tồn giữ nguyên.'),
])

# ---------------------------------------------------------------- 2.9 FR-09
d.h3('2.9 Từ chối phiếu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Từ chối phiếu', 'action',
            [('include', 'Nhập lý do từ chối'),
             ('extend', 'Thông báo kết quả cho người lập phiếu')],
            caption='Biểu đồ Use Case — FR-09 Từ chối phiếu', actor=ACTOR_KT)

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX của thao tác đổi trạng thái.', anchor='notice')
d.intro_table(
    ten='Từ chối phiếu chuyển hàng nhập thẳng',
    mota='Kế toán kho không chấp thuận phiếu và ghi lý do; phiếu quay lại cho người lập chỉnh sửa '
         'và gửi lại.',
    tacnhan='Kế toán kho',
    dieukien='Phiếu đang ở trạng thái Chờ duyệt và thuộc đúng công ty của người xử lý.',
    chinh='1. Kế toán kho mở màn chi tiết của phiếu đang Chờ duyệt.\n'
          '2. Kế toán kho bấm Từ chối.\n'
          '3. Hệ thống mở cửa sổ Từ chối phiếu kèm ô Lý do từ chối.\n'
          '4. Kế toán kho nhập lý do rồi bấm Từ chối.\n'
          '5. Hệ thống chuyển phiếu sang Không duyệt, lưu lý do và báo cho người lập.',
    phu='• Không nhập lý do → hệ thống báo bắt buộc nhập và không thực hiện thao tác.\n'
        '• Bấm Đóng → cửa sổ đóng lại, phiếu giữ nguyên.\n'
        '• Phiếu vừa được người khác xử lý → hệ thống từ chối và yêu cầu tải lại trang.',
    dacbiet='Thao tác này KHÔNG động vào tồn; tồn chỉ thay đổi khi phiếu được duyệt.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Từ chối',
         note='Cửa sổ Từ chối phiếu được mở ngay trên màn chi tiết theo đường dẫn ở trên.',
         shot=shot('18-tu-choi-phieu.png'),
         shot_caption='Cửa sổ Từ chối phiếu với ô Lý do từ chối bắt buộc')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Từ chối phiếu', '–'),
    ('Ô Lý do từ chối', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     'Gợi ý nhập “Nhập lý do từ chối”; lý do được lưu và hiện lại ở màn chi tiết và lịch sử.'),
    ('Nút Từ chối', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thực hiện từ chối phiếu.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không thay đổi gì.'),
    ('Thông báo lỗi tại ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện khi bấm Từ chối mà chưa nhập lý do.'),
])

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Từ chối trên màn chi tiết', 'Click',
     'Before:\n– Kiểm tra quyền Kế toán kho, cùng công ty và phiếu đang Chờ duyệt.\n'
     'After:\n– Mở cửa sổ Từ chối phiếu với ô lý do để trống.'),
    ('Bấm Từ chối trong cửa sổ', 'Click',
     'Before:\n– Lý do trống → hiển thị báo bắt buộc nhập và dừng xử lý.\n'
     '– Phiếu đã bị người khác xử lý → từ chối thao tác và yêu cầu tải lại trang.\n'
     'During:\n– Lưu lý do vào phiếu và ghi nhận người xử lý.\n'
     'After:\n– Chuyển phiếu sang Không duyệt, ghi một dòng lịch sử kèm lý do.\n'
     '– Gửi thông báo cho người lập phiếu.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
    ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, phiếu giữ nguyên trạng thái.'),
])

# --------------------------------------------------------------- 2.10 FR-10
d.h3('2.10 Xóa phiếu')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu', 'action',
            [('include', 'Kiểm tra phiếu do chính mình lập và chưa duyệt'),
             ('extend', 'Xác nhận trước khi xóa')],
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa và Thông báo.', anchor='delete')
d.intro_table(
    ten='Xóa phiếu chuyển hàng nhập thẳng',
    mota='Xóa hẳn một phiếu do chính mình lập khi phiếu chưa được duyệt.',
    tacnhan='Người lập phiếu; Người dùng đã đăng nhập',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Đang tạo hoặc Không duyệt.',
    chinh='1. Người dùng bấm biểu tượng Xóa trên dòng phiếu, hoặc nút Xóa ở màn chi tiết.\n'
          '2. Hệ thống hiện hộp Xác nhận xóa kèm số phiếu.\n'
          '3. Người dùng bấm Xóa.\n'
          '4. Hệ thống xóa phiếu cùng các dòng hàng hóa của phiếu.\n'
          '5. Hệ thống báo xóa thành công và nạp lại danh sách.',
    phu='• Phiếu đã Chờ duyệt hoặc Đã duyệt → biểu tượng Xóa không hiển thị.\n'
        '• Bấm Hủy → đóng hộp thoại, không xóa gì.\n'
        '• Phiếu vừa bị người khác xóa → hệ thống báo không tìm thấy dữ liệu.',
    dacbiet='Phiếu chưa duyệt nên chưa từng động vào tồn; xóa phiếu không làm thay đổi tồn của ai.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa',
         note='Hộp Xác nhận xóa được mở ngay trên màn danh sách hoặc màn chi tiết theo đường dẫn ở '
              'trên.',
         shot=shot('19-xac-nhan-xoa.png'),
         shot_caption='Hộp thoại Xác nhận xóa phiếu')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', '–'),
    ('Câu hỏi xác nhận', 'Label', 'Hiển thị', 'Bạn có chắc muốn xóa phiếu <số phiếu>?',
     'Có nêu đúng số phiếu đang xóa.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa phiếu.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
    ('Nút đóng ở góc phải', 'Icon Button', 'Enable', 'Hiển thị', 'Tương đương nút Hủy.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Xóa', 'Click',
     'Before:\n– Biểu tượng chỉ hiện với phiếu của chính mình đang Đang tạo hoặc Không duyệt.\n'
     'After:\n– Mở hộp Xác nhận xóa kèm số phiếu.'),
    ('Bấm Xóa trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra lại điều kiện được xóa; không thỏa thì báo không có quyền.\n'
     'During:\n– Xóa phiếu và các dòng hàng hóa của phiếu.\n'
     'After:\n– Ghi một dòng lịch sử xóa, hiển thị thông báo thành công và nạp lại danh sách từ '
     'đầu.'),
    ('Bấm Hủy', 'Click', 'After:\n– Đóng hộp thoại, phiếu giữ nguyên.'),
])

# --------------------------------------------------------------- 2.11 FR-11
d.h3('2.11 In phiếu và in danh sách')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'In phiếu và in danh sách', 'io',
            [('include', 'Lấy mẫu in tương ứng'),
             ('extend', 'In danh sách theo bộ lọc đang áp dụng')],
            caption='Biểu đồ Use Case — FR-11 In phiếu và in danh sách')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc màn In và bố cục bản in.', anchor='detail')
d.intro_table(
    ten='In phiếu và in danh sách phiếu',
    mota='In một phiếu theo mẫu Phiếu yêu cầu chuyển hàng, hoặc in danh sách phiếu đang lọc theo '
         'khổ giấy ngang.',
    tacnhan='Người lập phiếu; Kế toán kho; Người dùng đã đăng nhập',
    dieukien='Phiếu nằm trong phạm vi dữ liệu của người đăng nhập.',
    chinh='1. Người dùng bấm biểu tượng In trên dòng phiếu, hoặc nút In ở màn chi tiết, hoặc nút '
          'In trên thanh công cụ của danh sách.\n'
          '2. Hệ thống mở màn xem trước bản in kèm dữ liệu đã điền vào mẫu.\n'
          '3. Người dùng bấm In để gửi lệnh in ra máy in hoặc lưu thành tệp PDF.',
    phu='• In danh sách lấy đúng bộ lọc đang áp dụng, không in toàn bộ dữ liệu.\n'
        '• Danh sách rỗng → bản in chỉ có phần tiêu đề và bảng không có dòng nào.\n'
        '• Số lượng có phần thập phân được in đầy đủ, không làm tròn.',
    dacbiet=None)

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In',
         shot=shot('14-ban-in-phieu.png'),
         shot_caption='Bản in một phiếu theo mẫu Phiếu yêu cầu chuyển hàng')
d.figure(shot('15-ban-in-danh-sach.png'), 'Bản in danh sách phiếu, khổ giấy ngang', width_in=6.2)

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bản in phiếu', 'Label', 'Hiển thị', '–', 'PHIẾU YÊU CẦU CHUYỂN HÀNG', '–'),
    ('Khối thông tin chung', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm số phiếu, ngày lập, người lập, người nhận, phòng ban và ghi chú.'),
    ('Bảng hàng hóa trên bản in', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm số thứ tự, tên hàng, mã hàng, đơn vị tính và số lượng.'),
    ('Khối ký', 'Label', 'Read-only', '–', 'Theo mẫu in',
     'Các ô ký của người lập, người nhận và người duyệt.'),
    ('Bản in danh sách', 'Table/Grid', 'Read-only', '–', 'Theo bộ lọc',
     'Khổ ngang, gồm số thứ tự, số phiếu, ngày lập, người lập, người nhận và trạng thái.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Đặt ở góc phải; mở hộp in của trình duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn trước đó.'),
], required=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In trên dòng phiếu hoặc màn chi tiết', 'Click',
     'Before:\n– Kiểm tra phiếu nằm trong phạm vi dữ liệu của người dùng.\n'
     'During:\n– Lấy mẫu in của phiếu và điền dữ liệu; ô không có dữ liệu được để trống.\n'
     'After:\n– Mở màn xem trước bản in.'),
    ('Bấm In trên thanh công cụ của danh sách', 'Click',
     'During:\n– Lấy đúng danh sách theo bộ lọc đang áp dụng và điền vào mẫu in danh sách.\n'
     'After:\n– Mở màn xem trước bản in khổ ngang.'),
    ('Bấm nút In ở màn xem trước', 'Click', 'After:\n– Mở hộp in của trình duyệt.'),
])

# --------------------------------------------------------------- 2.12 FR-12
d.h3('2.12 Xuất Excel danh sách')

d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Xuất Excel danh sách', 'io',
            [('include', 'Chọn trường cần xuất'),
             ('extend', 'Xuất theo bộ lọc đang áp dụng')],
            caption='Biểu đồ Use Case — FR-12 Xuất Excel danh sách')

d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách phiếu',
    mota='Xuất danh sách phiếu đang lọc ra tệp Excel, cho phép chọn trước những trường cần đưa vào '
         'tệp.',
    tacnhan='Người lập phiếu; Kế toán kho; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách.',
    chinh='1. Người dùng bấm Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ chọn trường cần xuất, mặc định tích sẵn toàn bộ.\n'
          '3. Người dùng tích hoặc bỏ tích các trường.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống tạo tệp Excel theo bộ lọc đang áp dụng và tải về máy.',
    phu='• Bỏ tích hết các trường → hệ thống không cho xuất.\n'
        '• Danh sách rỗng → tệp chỉ có dòng tiêu đề.\n'
        '• Tệp xuất ra lấy đúng bộ lọc đang áp dụng, không phải toàn bộ dữ liệu.',
    dacbiet=None)

d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel',
         note='Cửa sổ chọn trường xuất được mở ngay trên màn danh sách theo đường dẫn ở trên.',
         shot=shot('05-chon-truong-xuat-excel.png'),
         shot_caption='Cửa sổ chọn trường cần xuất ra Excel')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Xuất Excel', '–'),
    ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 11 trường', 'Có ít nhất một trường',
     'Tích sẵn toàn bộ',
     'Gồm số phiếu, người nhận, công ty, phòng ban, ghi chú, người duyệt, người tạo, ngày tạo, '
     'người cập nhật, ngày cập nhật và trạng thái.'),
    ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích toàn bộ trường.'),
    ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích toàn bộ trường.'),
    ('Nút Xuất file', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tạo và tải tệp Excel.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
])

d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ chọn trường với toàn bộ trường được tích sẵn.'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Chưa tích trường nào → không cho xuất.\n'
     'During:\n– Lấy dữ liệu theo bộ lọc đang áp dụng và dựng tệp Excel với đúng những cột đã '
     'chọn.\n'
     'After:\n– Tải tệp về máy người dùng và đóng cửa sổ.'),
])

# --------------------------------------------------------------- 2.13 FR-13
d.h3('2.13 Xem lịch sử thay đổi')

d.p('2.13.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử thay đổi.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Hiển thị các mốc thao tác đã diễn ra trên phiếu: tạo mới, sửa, gửi duyệt, duyệt, từ chối '
         'và xóa, kèm người thực hiện và thời điểm.',
    tacnhan='Người lập phiếu; Kế toán kho; Người dùng đã đăng nhập',
    dieukien='Phiếu nằm trong phạm vi dữ liệu của người đăng nhập.',
    chinh='1. Người dùng bấm Lịch sử trong menu ba chấm ở màn danh sách, hoặc bấm Xem lịch sử ở '
          'màn chi tiết.\n'
          '2. Hệ thống nạp các mốc lịch sử của phiếu.\n'
          '3. Hệ thống hiển thị danh sách mốc theo thứ tự mới nhất lên trước, mỗi mốc nêu rõ '
          'trường nào đổi từ giá trị nào sang giá trị nào.',
    phu='• Phiếu chưa có mốc nào → hiện dòng báo chưa có lịch sử thao tác.\n'
        '• Mốc từ chối hiển thị kèm lý do mà Kế toán kho đã nhập.\n'
        '• Thao tác thực hiện bên hệ thống cũ không sinh mốc lịch sử ở màn này.',
    dacbiet=None)

d.p('2.13.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử',
         note='Cửa sổ Lịch sử mở từ menu ba chấm của màn danh sách; khối Lịch sử thay đổi nằm cuối '
              'màn chi tiết.',
         shot=shot('08-popup-lich-su.png'),
         shot_caption='Cửa sổ Lịch sử mở từ màn danh sách')
d.figure(shot('12-khoi-lich-su-chi-tiet.png'), 'Khối Lịch sử thay đổi ở màn chi tiết',
         width_in=6.2)

d.p('2.13.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ / khối', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi', '–'),
    ('Nút Xem lịch sử', 'Button', 'Enable', '–', 'Hiển thị',
     'Chỉ có ở màn chi tiết; bấm mới nạp dữ liệu.'),
    ('Mốc lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi mốc gồm thao tác, người thực hiện, thời điểm và danh sách thay đổi.'),
    ('Dòng thay đổi của một trường', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Nêu tên trường kèm giá trị cũ và giá trị mới.'),
    ('Dòng thay đổi của bảng hàng hóa', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Ghi theo từng dòng hàng, chỉ in dòng có thay đổi.'),
    ('Lý do từ chối', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Hiện ở mốc từ chối phiếu.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện khi phiếu chưa có mốc lịch sử nào.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Chỉ có ở cửa sổ mở từ danh sách.'),
], required=False)

d.p('2.13.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lịch sử ở menu ba chấm', 'Click',
     'During:\n– Nạp các mốc lịch sử của phiếu tương ứng.\n'
     'After:\n– Mở cửa sổ Lịch sử, sắp xếp mới nhất lên trước.'),
    ('Bấm Xem lịch sử ở màn chi tiết', 'Click',
     'During:\n– Nạp dữ liệu lần đầu; các lần bấm sau chỉ mở hoặc thu gọn khối.\n'
     'After:\n– Hiển thị danh sách mốc ngay trong màn chi tiết.'),
])

# ================================================= PHẦN 4. QUY TẮC NGHIỆP VỤ
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.p('Quy tắc áp dụng: Áp dụng SRS Các quy tắc chung [SRS_Các quy tắc chung_VN_1.0]. Bảng dưới đây '
    'chỉ liệt kê những quy tắc đặc thù của màn Phiếu chuyển hàng nhập thẳng.')
d.rule_table([
    ('BR-01', 'Phạm vi dữ liệu theo cấp quyền xem', [
        '– Hệ thống xét bốn cấp quyền theo thứ tự tổng công ty → công ty → phòng ban → bộ phận, '
        'cấp nào có trước thì áp cấp đó.',
        '– Không có cấp nào thì người dùng chỉ thấy phiếu do chính mình lập.',
        '– Người có quyền Kế toán kho luôn thấy được mọi phiếu của công ty mình.',
        '– Phiếu ở trạng thái Đang tạo của người khác luôn bị ẩn với mọi cấp quyền.',
    ], ['Xem danh sách', 'Xem chi tiết', 'Tìm kiếm và lọc']),

    ('BR-02', 'Điều kiện được sửa và xóa phiếu', [
        '– Chỉ người lập phiếu mới sửa và xóa được phiếu của mình.',
        '– Chỉ sửa và xóa khi phiếu đang ở trạng thái Đang tạo hoặc Không duyệt.',
        '– Phiếu đã Chờ duyệt hoặc Đã duyệt thì không sửa, không xóa dưới bất kỳ quyền nào.',
        '– Nút không dùng được thì ẩn hẳn khỏi màn hình chứ không để mờ.',
    ], ['Sửa phiếu', 'Xóa phiếu']),

    ('BR-03', 'Người nhận phải khác người lập và cùng công ty', [
        '– Danh sách Người nhận chỉ gồm nhân viên cùng công ty với người lập phiếu.',
        '– Người lập phiếu bị loại khỏi danh sách; hệ thống chặn cả trường hợp cố tình gửi lên '
        'chính mình, kèm câu báo “Người nhận phải khác người lập phiếu”.',
        '– Phòng ban tự điền theo người nhận và không sửa tay được.',
    ], ['Lập phiếu', 'Sửa phiếu']),

    ('BR-04', 'Khác biệt giữa Lưu nháp và Lưu và gửi duyệt', [
        '– Lưu nháp chỉ bắt buộc Người nhận; bảng hàng hóa để trống vẫn lưu được, phiếu ở trạng '
        'thái Đang tạo.',
        '– Lưu và gửi duyệt bắt buộc có ít nhất một dòng hàng hợp lệ, phiếu chuyển sang Chờ duyệt.',
        '– Dù lưu bằng nút nào, dòng hàng đã có vẫn phải đủ đơn vị tính và số lượng lớn hơn 0.',
    ], ['Lập phiếu', 'Sửa phiếu']),

    ('BR-05', 'Quy đổi số lượng theo đơn vị tính', [
        '– Số lượng theo đơn vị cơ bản bằng số lượng nhập nhân hệ số quy đổi của đơn vị đang chọn.',
        '– Đổi đơn vị tính thì hệ thống tính lại số lượng theo hệ số mới.',
        '– Mọi phép so tồn đều thực hiện theo đơn vị cơ bản.',
    ], ['Lập phiếu', 'Sửa phiếu', 'Duyệt phiếu']),

    ('BR-06', 'Ràng buộc nhập số lượng', [
        '– Ô số lượng chỉ nhận chữ số, dấu chấm thập phân và dấu phẩy hàng nghìn; ký tự khác bị '
        'loại ngay khi gõ hoặc khi dán.',
        '– Số lượng phải lớn hơn 0.',
        '– Vượt tồn hiện có thì hệ thống BÁO ĐỎ tại đúng dòng và giữ nguyên con số vừa nhập, tuyệt '
        'đối không tự kéo về mức tồn tối đa.',
        '– Bấm lưu khi còn dòng sai thì mọi dòng sai đều được đánh dấu, không chỉ dòng đầu tiên.',
    ], ['Lập phiếu', 'Sửa phiếu']),

    ('BR-07', 'Nguồn tồn dùng cho cửa sổ chọn hàng', [
        '– Cửa sổ chọn hàng luôn tra tồn của NGƯỜI LẬP phiếu, không phải người đang đăng nhập.',
        '– Quy tắc này giữ cho danh sách hàng chọn được và phép kiểm tra lúc lưu dùng chung một '
        'nguồn, tránh trường hợp chọn được hàng nhưng lưu lại báo không đủ.',
        '– Hàng đã có trong phiếu không hiện lại trong cửa sổ.',
    ], ['Chọn hàng hóa', 'Sửa phiếu']),

    ('BR-08', 'Kiểm tra đủ tồn khi lưu phiếu', [
        '– Trước khi lưu, hệ thống gộp các dòng cùng một mặt hàng rồi mới so với tồn của người lập.',
        '– Thiếu tồn thì chặn lưu và nêu rõ tên hàng không đủ số lượng.',
        '– Phép kiểm tra này chỉ để cảnh báo sớm; tồn thật vẫn chưa bị trừ ở bước lưu.',
    ], ['Lập phiếu', 'Sửa phiếu']),

    ('BR-09', 'Tồn chỉ thay đổi khi phiếu được duyệt', [
        '– Lập phiếu, sửa phiếu, gửi duyệt và từ chối đều KHÔNG làm thay đổi tồn của bất kỳ ai.',
        '– Khi duyệt, hệ thống trừ tồn của người lập theo thứ tự lô hàng có trước dùng trước rồi '
        'ghi phần tồn tương ứng sang người nhận, đồng thời lưu vết biến động của cả hai bên.',
        '– Toàn bộ việc trừ và ghi tồn diễn ra trọn vẹn hoặc không diễn ra; lỗi giữa chừng thì mọi '
        'thay đổi bị hủy và phiếu giữ nguyên trạng thái Chờ duyệt.',
        '– Thao tác duyệt không hoàn tác được.',
    ], ['Duyệt phiếu']),

    ('BR-10', 'Chặn duyệt khi tồn không đủ hoặc phiếu rỗng', [
        '– Tồn tại thời điểm duyệt ít hơn số lượng trên phiếu thì hệ thống chặn và báo rõ hàng '
        'nào, cần bao nhiêu và hiện còn bao nhiêu theo đơn vị cơ bản.',
        '– Đây là lỗi nghiệp vụ chứ không phải lỗi hệ thống; tuyệt đối không hiển thị câu báo lỗi '
        'máy chủ chung chung.',
        '– Phiếu không còn dòng hàng nào có số lượng thì cũng bị chặn, để không tồn tại phiếu đã '
        'duyệt mà tồn không đổi.',
    ], ['Duyệt phiếu']),

    ('BR-11', 'Điều kiện duyệt và từ chối', [
        '– Chỉ người có quyền Kế toán kho và thuộc đúng công ty của phiếu mới duyệt hoặc từ chối '
        'được; quản trị hệ thống cũng phải cùng công ty.',
        '– Chỉ phiếu đang ở trạng thái Chờ duyệt mới xử lý được.',
        '– Từ chối bắt buộc nhập lý do; lý do được lưu, hiện lại ở màn chi tiết và trong lịch sử.',
        '– Hệ thống không cho duyệt thẳng từ màn danh sách: biểu tượng Duyệt trên dòng chỉ mở màn '
        'chi tiết để người duyệt xem hàng hóa trước.',
    ], ['Duyệt phiếu', 'Từ chối phiếu']),

    ('BR-12', 'Thông báo theo luồng duyệt', [
        '– Khi phiếu chuyển sang Chờ duyệt, hệ thống gửi thông báo cho những người có quyền Kế '
        'toán kho thuộc CÙNG CÔNG TY với phiếu.',
        '– Khi phiếu được duyệt hoặc bị từ chối, hệ thống gửi thông báo cho người lập phiếu.',
        '– Bấm vào thông báo mở đúng phiếu tương ứng.',
        '– Lỗi gửi thông báo không làm hỏng thao tác nghiệp vụ đang thực hiện.',
    ], ['Lập phiếu', 'Sửa phiếu', 'Duyệt phiếu', 'Từ chối phiếu']),

    ('BR-13', 'Sinh số phiếu', [
        '– Số phiếu do hệ thống sinh khi lưu lần đầu, theo mã công ty của người lập kèm số thứ tự '
        'tăng dần.',
        '– Số phiếu không sửa được và không đổi khi phiếu được sửa hay đổi trạng thái.',
    ], ['Lập phiếu']),

    ('BR-14', 'Ghi lịch sử thay đổi', [
        '– Các thao tác tạo mới, sửa, gửi duyệt, duyệt, từ chối và xóa đều được ghi một mốc lịch '
        'sử kèm người thực hiện và thời điểm.',
        '– Lịch sử theo dõi Người nhận, Ghi chú, Trạng thái và bảng hàng hóa.',
        '– Bảng hàng hóa được ghi theo TỪNG DÒNG: sửa một ô số lượng chỉ in đúng dòng đó, không in '
        'lại cả bảng.',
        '– Mốc từ chối ghi kèm lý do mà Kế toán kho đã nhập.',
        '– Lịch sử lưu theo tên hiển thị nên đổi tên danh mục về sau không làm sai lịch sử cũ.',
        '– Các mốc được sắp xếp mới nhất lên trước và hiển thị giống nhau ở cả cửa sổ mở từ danh '
        'sách lẫn khối ở màn chi tiết.',
    ], 'Toàn màn hình'),

    ('BR-15', 'Xử lý xung đột khi nhiều người thao tác cùng lúc', [
        '– Khi phiếu vừa bị người khác đổi trạng thái, mọi thao tác ghi đều bị từ chối kèm lời '
        'nhắc tải lại trang để lấy dữ liệu mới nhất.',
        '– Phiếu vừa bị xóa thì hệ thống báo không tìm thấy dữ liệu và đưa người dùng về danh sách '
        'thay vì để lại màn trắng.',
        '– Hai người cùng duyệt một phiếu thì chỉ ghi nhận một lần, tồn không bị trừ hai lần.',
    ], ['Sửa phiếu', 'Xóa phiếu', 'Duyệt phiếu', 'Từ chối phiếu']),

    ('BR-16', 'Ghi nhớ bộ lọc và cấu hình hiển thị theo người dùng', [
        '– Bộ lọc đang áp dụng được ghi nhớ để khôi phục khi người dùng quay lại màn hình.',
        '– Cấu hình tiêu chí lọc và cấu hình cột lưu riêng theo từng người dùng.',
        '– Ba cột STT, Số phiếu và Hành động luôn hiển thị và không đổi vị trí được.',
        '– Tắt một tiêu chí trong Cài đặt bộ lọc thì giá trị đang lọc của tiêu chí đó cũng bị xóa, '
        'danh sách không bị lọc ngầm.',
    ], ['Xem danh sách', 'Tìm kiếm và lọc', 'Cài đặt bộ lọc']),

    ('BR-17', 'Sau mỗi thao tác đưa người dùng về danh sách', [
        '– Lưu, duyệt, từ chối và xóa xong đều đưa người dùng về màn danh sách và nạp lại dữ liệu.',
        '– Màn danh sách giữ nguyên bộ lọc và trang đang xem trước đó.',
    ], 'Toàn màn hình'),
])

d.save()
