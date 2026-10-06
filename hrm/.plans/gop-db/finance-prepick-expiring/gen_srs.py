# -*- coding: utf-8 -*-
"""Sinh SRS man "Hang sap het han giu" theo FORM CHUAN (srs-documenter).

Man CHI DOC, anh em cua "Danh sach hang giu" (dung chung PrepickStockReportService,
chi bat them co `expiring_only`).

Nguon: code HRM nhanh `gop_db`
  BE  Modules/Finance/Http/Controllers/V1/PrepickExpiringController.php
      Modules/Finance/Services/{PrepickStockReportService,PrepickConfigService}.php
      Modules/Finance/Resources/views/prints/prepick-stock-list.blade.php
  FE  pages/finance/prepick-expiring/{index.vue,components/export-excel.js}
      components/finance/prepick/PrepickStockLogModal.vue (prop apiPath)
Anh chup that: ./prepick_expiring_shots (dev, 05/10/2026, tai khoan DNS Admin).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, '..', '..', '..', '.claude', 'skills',
                                'srs-documenter', 'assets'))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(BASE, 'prepick_expiring_shots')
OUT = os.path.join(BASE, 'SRS - Hang sap het han giu.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Giữ hàng => Hàng sắp hết hạn giữ'
ACTOR = 'Người quản lý giữ hàng'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/prepick-expiring',
           full_url='http://hrm-crm.eteksofts.com/finance/prepick-expiring',
           img_prefix='hshhg_')

# ============================================================== TRANG DAU
d.title_block('Hàng sắp hết hạn giữ')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Hàng sắp hết hạn giữ thuộc phân hệ Tài '
    'chính, nhóm Giữ hàng, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và phạm vi dữ liệu của màn hình.',
    'Làm rõ bản chất màn hình: đây là báo cáo tra cứu CHỈ ĐỌC, không có thao tác thêm, sửa, xóa '
    'và không làm thay đổi tồn hàng giữ.',
    'Ghi rõ QUY TẮC CỬA SỔ NGÀY của màn hình: màn hình chỉ liệt kê lô hàng giữ có hạn giữ nằm '
    'trong N ngày GẦN ĐÂY tính tới HÔM NAY (N là số ngày cảnh báo cấu hình chung), tức là hàng '
    'ĐÃ hoặc VỪA hết hạn giữ — giữ nguyên hành vi của hệ thống cũ theo quyết định đã chốt.',
    'Giải thích hệ quả của quy tắc trên để kiểm thử không báo nhầm lỗi: cột Trạng thái của màn '
    'hình chỉ có thể là “Hết hạn” hoặc “Đến hạn”, KHÔNG bao giờ là “Trong hạn”.',
    'Mô tả cấu trúc cây 3 tầng Hàng hóa → Nhân viên → Khách hàng/lô, cùng các chức năng Xuất '
    'Excel, In danh sách và Lịch sử giữ hàng.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng, đứng tên một nhân viên kinh '
                 'doanh và có hạn giữ. Tồn hàng giữ tách riêng khỏi tồn kho thông thường.'),
    ('Lô hàng giữ', 'Một phần hàng giữ có cùng hàng hóa, nhân viên, khách hàng và hạn giữ. Mỗi '
                    'dòng tầng 3 của bảng là một lô.'),
    ('Hạn giữ', 'Ngày cuối cùng hàng được giữ cho khách hàng.'),
    ('Số ngày cảnh báo (N)', 'Tham số cấu hình chung của nhóm Giữ hàng, dùng chung với màn Yêu cầu '
                             'gia hạn hàng giữ. Trên dữ liệu đang dùng N = 7.'),
    ('Cửa sổ ngày', 'Khoảng [hôm nay − N ngày, hôm nay], tính cả hai đầu. Chỉ lô có hạn giữ '
                    'nằm trong khoảng này mới xuất hiện trên màn hình.'),
    ('Trạng thái hạn giữ', 'Tính tại thời điểm xem, không lưu: Hết hạn (hạn giữ trước hôm nay), '
                           'Đến hạn (hạn giữ đúng hôm nay), Trong hạn (hạn giữ sau hôm nay).'),
    ('Tổng SL trong kho', 'Tổng tồn kho kế toán của hàng hóa trên mọi kho kế toán thuộc phạm vi '
                          'công ty người dùng được xem.'),
    ('Kho kế toán', 'Kho dùng để hạch toán tồn, dạng “LN01 - Liên Ninh - Hàng bán”. Một kho vật lý '
                    'có thể có nhiều kho kế toán.'),
    ('Đơn vị cơ bản', 'Đơn vị tính gốc của hàng hóa. Tồn hàng giữ luôn lưu theo đơn vị này.'),
], widths=[1.7, 4.8])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Màn hình dùng lại bộ quyền sẵn có của nhóm nghiệp vụ Giữ hàng, KHÔNG khai thêm quyền mới.')

d.p('Nhóm quyền truy cập màn hình:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý giữ hàng',
     'Điều kiện BẮT BUỘC để xem dữ liệu của màn hình (Super Admin được miễn). Thiếu quyền này '
     'thì mọi chức năng (danh sách, chi tiết, lịch sử, xuất Excel, in) đều bị từ chối với thông '
     'báo “Bạn không có quyền xem danh sách hàng sắp hết hạn giữ”.'),
], widths=[0.8, 1.9, 3.8])

d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét theo thứ tự, lấy cấp cao nhất người dùng có):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu hàng giữ theo tổng công ty',
     'Xem lô hàng giữ của mọi công ty. Ô lọc Công ty được hiển thị.'),
    ('V2', 'Xem phiếu hàng giữ theo công ty',
     'Xem lô hàng giữ thuộc công ty đang đăng nhập.'),
    ('V3', 'Xem phiếu hàng giữ theo phòng ban',
     'Xem lô do nhân viên thuộc các phòng ban mình quản lý và phòng ban của chính mình đứng tên '
     'giữ, cộng lô của chính mình.'),
], widths=[0.8, 1.9, 3.8])

d.p('Ba quy tắc chung:')
d.bullets([
    'Người có Q1 nhưng không có V1, V2, V3 chỉ thấy lô hàng do CHÍNH MÌNH đứng tên giữ.',
    'Super Admin được xem như có Q1 và V1.',
    'Phạm vi dữ liệu áp đồng thời cho cả ba tầng của bảng, danh sách lựa chọn của ô lọc Nhân '
    'viên / Thương hiệu / Model, tệp Excel và bản in. Cột Tổng SL trong kho và ô lọc Kho bó theo '
    'công ty đang đăng nhập khi người dùng không có V1.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1 + V1', 'Q1 + V2/V3', 'Chỉ Q1', 'Không có Q1'], [
    ('FR-01 Xem danh sách hàng sắp hết hạn giữ', '✅', '✅ (trong phạm vi)',
     '✅ (lô của mình)', '❌'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅ (không có ô Công ty)', '✅ (không có ô Công ty)', '❌'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '❌'),
    ('FR-04 Tuỳ chỉnh cột hiển thị', '✅', '✅', '✅', '❌'),
    ('FR-05 Xem chi tiết giữ hàng theo nhân viên và khách hàng', '✅', '✅ (trong phạm vi)',
     '✅ (lô của mình)', '❌'),
    ('FR-06 Xem lịch sử giữ hàng của lô', '✅', '✅', '✅', '❌'),
    ('FR-07 Xuất danh sách ra Excel', '✅', '✅ (trong phạm vi)', '✅ (lô của mình)', '❌'),
    ('FR-08 In danh sách', '✅', '✅ (trong phạm vi)', '✅ (lô của mình)', '❌'),
], widths=[2.3, 0.75, 1.15, 1.0, 0.8])

# ================================================ PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0])],
    [('FR-01', 'Xem danh sách hàng sắp hết hạn giữ', 'view')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-05', 'Xem chi tiết giữ hàng theo nhân viên và khách hàng', 'view', 'extend', [0], None),
     ('FR-06', 'Xem lịch sử giữ hàng của lô', 'view', 'extend', [0], None),
     ('FR-07', 'Xuất danh sách ra Excel', 'io', 'extend', [0], None),
     ('FR-08', 'In danh sách', 'io', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Hàng sắp hết hạn giữ')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách hàng sắp hết hạn giữ')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Hàng sắp hết hạn giữ tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách hàng sắp hết hạn giữ',
    mota='Hiển thị danh sách HÀNG HÓA có ít nhất một lô hàng giữ có hạn giữ nằm trong cửa sổ ngày '
         '[hôm nay − N ngày, hôm nay], trong phạm vi dữ liệu của người đăng nhập. Mỗi dòng tầng 1 '
         'là một hàng hóa; số SL giữ là tổng các lô trong cửa sổ ngày của hàng hóa đó.',
    tacnhan=ACTOR,
    dieukien='Người dùng đã đăng nhập và có quyền Quản lý giữ hàng (hoặc là Super Admin).',
    chinh='1. Người dùng vào menu Tài chính → Giữ hàng → Hàng sắp hết hạn giữ.\n'
          '2. Hệ thống kiểm tra quyền Quản lý giữ hàng.\n'
          '3. Hệ thống đọc số ngày cảnh báo N và lọc các lô có hạn giữ từ (hôm nay − N) tới hôm '
          'nay.\n'
          '4. Hệ thống áp phạm vi dữ liệu theo cấp quyền xem, gom theo hàng hóa và sắp theo Tên '
          'hàng hóa A → Z.\n'
          '5. Bảng hiển thị trang 1, 10 dòng; ô “Hiển thị a–b / N” cho biết tổng số hàng hóa.',
    phu='• Không có quyền Quản lý giữ hàng → hệ thống báo “Bạn không có quyền xem danh sách hàng '
        'sắp hết hạn giữ”, bảng không có dữ liệu.\n'
        '• Không có lô nào trong cửa sổ ngày → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Bộ lọc của lần vào trước (trong vòng 10 phút) còn hiệu lực thì được khôi phục.\n'
        '• Mở màn kèm tham số hàng hóa trên đường dẫn (liên kết từ màn khác) → chỉ hiện đúng hàng '
        'hóa đó, đè lên bộ lọc đã lưu.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Hàng sắp hết hạn giữ lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Hàng sắp hết hạn giữ', 'Tiêu đề cố định.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ xem trước bản in theo bộ lọc đang áp dụng (FR-08).'),
    ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
     'Mở cửa sổ chọn trường xuất (FR-07); bị khóa trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-04).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Nút mở rộng',
     'Ở dòng hàng hóa là nút tròn mở / thu chi tiết (FR-05); dòng con hiển thị ký hiệu nhánh. '
     'Cột cố định, không tắt được.'),
    ('Cột Mã hàng hóa / Nhân viên / Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tầng 1: mã hàng hóa (chữ thường, không phải liên kết). Tầng 2: tên nhân viên. Tầng 3: '
     '“mã khách hàng - tên khách hàng”. Cột cố định, sắp xếp được.'),
    ('Cột Tên hàng hóa / Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tầng 1: tên hàng hóa. Tầng 2: phòng ban của nhân viên. Tầng 3: để trống. Sắp xếp được.'),
    ('Cột Đơn vị', 'Dropdown', 'Enable / Read-only', 'Các đơn vị của hàng hóa', 'Đơn vị cơ bản',
     'Chỉ là ô chọn khi hàng hóa có từ 2 đơn vị trở lên; còn lại hiển thị chữ. Đổi đơn vị thì '
     'quy đổi số lượng của dòng đó và mọi dòng con.'),
    ('Cột Model / Thương hiệu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Chỉ có giá trị ở tầng 1.'),
    ('Cột Tổng SL trong kho', 'Table/Grid', 'Read-only', '≥ 0, 1,234.56', 'Theo dữ liệu',
     'Tổng tồn kho kế toán trong phạm vi công ty. Chỉ ở tầng 1; không có tồn thì để trống. '
     'Sắp xếp được.'),
    ('Cột SL giữ', 'Table/Grid', 'Read-only', '> 0, 1,234.56', 'Theo dữ liệu',
     'Tầng 1: tổng các lô trong cửa sổ ngày. Tầng 2: tổng của nhân viên. Tầng 3: số của lô. '
     'Làm tròn XUỐNG 2 chữ số thập phân. Sắp xếp được.'),
    ('Cột Hạn giữ', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
     'Chỉ có giá trị ở tầng 3 (từng lô). Tầng 1 và 2 để trống là đúng.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Hết hạn / Đến hạn', 'Theo dữ liệu',
     'Chỉ ở tầng 3. Hết hạn màu đỏ, Đến hạn màu vàng. Không bao giờ ra Trong hạn (xem BR-01).'),
    ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Chỉ ở tầng 3 có nút Lịch sử giữ hàng (FR-06). Cột cố định cuối bảng.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số HÀNG HÓA (tầng 1) khớp bộ lọc, không phải số lô.'),
    ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, 10 dòng',
     'Dòng tầng 2, 3 chèn thêm không tính vào số dòng mỗi trang.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi không có hàng hóa nào khớp.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị',
     'Hiện khi vào màn và trong lúc nạp lại dữ liệu.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng; không có → báo không có quyền, không trả dữ '
     'liệu.\n'
     '– Khôi phục bộ lọc đã lưu (10 phút); tham số hàng hóa trên đường dẫn đè bộ lọc đã lưu.\n'
     'During:\n– Bật cờ cửa sổ ngày phía máy chủ (không phụ thuộc giao diện gửi lên).\n'
     '– Lọc lô có số lượng > 0 và hạn giữ trong [hôm nay − N, hôm nay].\n'
     '– Áp phạm vi dữ liệu V1 → V2 → V3 → chỉ lô của mình.\n'
     'After:\n– Trả trang 1 sắp theo Tên hàng hóa A → Z, kèm danh sách đơn vị của từng hàng '
     'hóa; nạp nguồn dữ liệu cho các ô lọc.'),
    ('Bấm tiêu đề cột có mũi tên sắp xếp', 'Click',
     'During:\n– Chỉ 4 cột sắp xếp được: Mã hàng hóa, Tên hàng hóa, Tổng SL trong kho, SL giữ.\n'
     '– Sắp cột mới thì bỏ sắp xếp cột cũ.\n'
     'After:\n– Nạp lại từ trang 1, đóng mọi dòng đang mở rộng.'),
    ('Đổi đơn vị ở cột Đơn vị', 'Change',
     'During:\n– Số lượng = số theo đơn vị cơ bản ÷ hệ số của đơn vị chọn, làm tròn xuống 2 chữ '
     'số.\n'
     'After:\n– Cập nhật Tổng SL trong kho, SL giữ của dòng hàng hóa và mọi dòng con; không gọi lại '
     'máy chủ.'),
    ('Bấm số trang / đổi số dòng mỗi trang', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\n'
     '– Đổi số dòng mỗi trang thì về trang 1.\n'
     'After:\n– Nạp dữ liệu trang mới, đóng mọi dòng đang mở rộng và xóa bộ nhớ chi tiết cũ.'),
])

# ------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các tiêu chí lọc riêng của '
           'màn Hàng sắp hết hạn giữ tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách hàng sắp hết hạn giữ',
    mota='Thu hẹp danh sách bằng ô tìm nhanh theo khách hàng và tám tiêu chí lọc nâng cao. Mọi '
         'điều kiện lọc đều cộng thêm vào cửa sổ ngày, không thay thế nó.',
    tacnhan=ACTOR,
    dieukien='Đang ở màn Hàng sắp hết hạn giữ.',
    chinh='1. Người dùng gõ vào ô tìm nhanh hoặc bấm Tìm kiếm nâng cao để mở khu vực lọc.\n'
          '2. Người dùng nhập / chọn tiêu chí.\n'
          '3. Người dùng bấm Tìm kiếm (bắt buộc với ô tìm nhanh).\n'
          '4. Hệ thống nạp lại danh sách từ trang 1.',
    phu='• Đổi giá trị một ô lọc nâng cao → tự nạp lại, không cần bấm Tìm kiếm.\n'
        '• Bấm Làm mới → xóa mọi điều kiện lọc và sắp xếp, tự nạp lại danh sách.\n'
        '• Không có hàng hóa nào khớp → “Không có dữ liệu phù hợp bộ lọc.”.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('02-bo-loc-nang-cao.png'),
         shot_caption='Khu vực Tìm kiếm nâng cao đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Placeholder “Nhập tên, số điện thoại hoặc mã KH để tìm kiếm”. Tìm gần đúng theo tên, mã '
     'hoặc số điện thoại KHÁCH HÀNG của lô. Chỉ áp dụng khi bấm Tìm kiếm.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', 'Hiển thị', 'Áp dụng toàn bộ điều kiện lọc.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Xóa hết điều kiện lọc, bỏ sắp xếp và tự nạp lại.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–',
     'Tìm kiếm nâng cao', 'Đóng / mở khu vực lọc nâng cao.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (FR-03).'),
    ('Ô Mã hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Tìm gần đúng theo mã hàng hóa.'),
    ('Ô Tên hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Tìm gần đúng theo tên hàng hóa.'),
    ('Ô Lọc theo kho', 'Dropdown', 'Enable', 'Kho kế toán đang hoạt động', 'Trống',
     'Placeholder “Chọn kho”. Chỉ liệt kê kho kế toán ĐANG HOẠT ĐỘNG (bỏ kho Chờ xóa và kho '
     'ngừng dùng), trong phạm vi công ty. Giữ lại hàng hóa CÓ tồn kho kế toán ở kho đã chọn.'),
    ('Ô Thương hiệu', 'Dropdown', 'Enable', 'Thương hiệu có hàng đang giữ', 'Trống',
     'Chỉ liệt kê thương hiệu của hàng hóa đang có tồn giữ trong phạm vi.'),
    ('Ô Model', 'Dropdown', 'Enable', 'Model có hàng đang giữ', 'Trống',
     'Chỉ liệt kê model của hàng hóa đang có tồn giữ trong phạm vi.'),
    ('Ô Trạng thái', 'Dropdown', 'Enable', 'Hết hạn / Đến hạn', 'Trống',
     'Lựa chọn Trong hạn bị bỏ khỏi danh sách vì không bao giờ có dữ liệu.'),
    ('Ô Nhân viên', 'Dropdown', 'Enable', 'Nhân viên đang giữ hàng', 'Trống',
     'Chỉ liệt kê người đang đứng tên giữ hàng trong phạm vi; thu hẹp theo Công ty / Phòng ban '
     'đang chọn.'),
    ('Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống',
     'Chỉ hiện với người có quyền V1 hoặc Super Admin. Biểu tượng ổ khóa cạnh nhãn là công tắc '
     '“Hiện cả công ty đã khoá”, không phải ô bị khóa.'),
    ('Ô Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Trống',
     'Lọc lô do nhân viên thuộc phòng ban đã chọn đứng tên. Biểu tượng ổ khóa là công tắc '
     '“Hiện cả phòng ban đã khoá”. Đổi Công ty / Phòng ban thì ô Nhân viên bị xóa giá trị.'),
], required=False)

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm', 'Click',
     'During:\n– Gom mọi điều kiện, kể cả ô tìm nhanh, cộng thêm cửa sổ ngày.\n'
     'After:\n– Nạp lại từ trang 1, đóng các dòng đang mở rộng.'),
    ('Gõ ô tìm nhanh nhưng chưa bấm Tìm kiếm', 'Change',
     'After:\n– Không nạp lại danh sách.'),
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'After:\n– Tự nạp lại danh sách từ trang 1.'),
    ('Bấm Làm mới', 'Click',
     'During:\n– Xóa mọi điều kiện lọc và sắp xếp (kể cả tham số hàng hóa từ đường dẫn).\n'
     'After:\n– Nạp lại danh sách mặc định trang 1; cửa sổ ngày vẫn giữ nguyên.'),
    ('Rời màn rồi quay lại trong 10 phút', 'System',
     'After:\n– Khôi phục bộ lọc và trạng thái đóng / mở khu vực lọc nâng cao.'),
])

# ------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc', 'view', (), actor=ACTOR,
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Bộ lọc và Cấu hình cột.', anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc hiển thị',
    mota='Cho phép người dùng chọn ô lọc nào được hiện và sắp xếp thứ tự các ô lọc.',
    tacnhan=ACTOR,
    dieukien='Đang ở màn Hàng sắp hết hạn giữ.',
    chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
          '2. Cửa sổ liệt kê 8 mục: Mã hàng hóa, Tên hàng hóa, Lọc theo kho, Thương hiệu, Model, '
          'Trạng thái, Nhân viên, Công ty – Phòng ban.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ⠿ để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu; khu vực lọc vẽ lại theo cấu hình mới.',
    phu='• Bấm Khôi phục mặc định → đủ 8 mục theo thứ tự gốc.\n'
        '• Bấm Đóng hoặc dấu × → thoát, không lưu.\n'
        '• Bỏ tích một ô đang có giá trị lọc → giá trị đó bị xóa khỏi điều kiện lọc.',
    dacbiet='Cấu hình lưu riêng theo từng người dùng và từng màn hình.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('03-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Cài đặt bộ lọc', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng '
     'màn hình.”'),
    ('Danh sách ô lọc', 'Table/Grid', 'Enable', '8 mục', 'Tích đủ 8 mục',
     'Mỗi mục có số thứ tự, tay nắm kéo thả, ô tích và tên. Mục Công ty – Phòng ban bật / tắt '
     'cả hai ô cùng lúc.'),
    ('Nút Lưu', 'Button', 'Enable', '–', 'Hiển thị', 'Ghi cấu hình và đóng cửa sổ.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Hiển thị', 'Đưa về cấu hình gốc.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Thoát, không lưu.'),
], required=False)

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu danh sách ô lọc được tích và thứ tự theo người dùng; vẽ lại khu vực lọc.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Tích lại đủ 8 mục theo thứ tự gốc.'),
    ('Kéo thả một mục', 'Click', 'After:\n– Đổi vị trí mục trong danh sách.'),
])

# ------------------------------------------------------------ 2.4
d.h3('2.4 Tuỳ chỉnh cột hiển thị')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view', (), actor=ACTOR,
            caption='Biểu đồ Use Case — FR-04 Tuỳ chỉnh cột hiển thị')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Cấu hình cột hiển thị.', anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh cột hiển thị của bảng',
    mota='Cho phép bật / tắt và sắp xếp các cột của bảng.',
    tacnhan=ACTOR,
    dieukien='Đang ở màn Hàng sắp hết hạn giữ.',
    chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
          '2. Cửa sổ “Tuỳ chỉnh cột” liệt kê 11 cột kèm ô tích.\n'
          '3. Người dùng tích / bỏ tích và kéo biểu tượng ≡ để sắp xếp.\n'
          '4. Người dùng bấm Lưu; bảng vẽ lại.',
    phu='• Ba cột STT, Mã hàng hóa / Nhân viên / Khách hàng và Hành động bị khóa, luôn hiện.\n'
        '• Bấm Đóng → thoát, không lưu.',
    dacbiet='Cấu hình lưu riêng theo từng người dùng.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột hiển thị', shot=shot('04-cau-hinh-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách cột', 'Table/Grid', 'Enable', '11 cột', 'Tích đủ 11 cột',
     'STT, Mã hàng hóa / Nhân viên / Khách hàng, Tên hàng hóa / Phòng ban, Đơn vị, Model, '
     'Thương hiệu, Tổng SL trong kho, SL giữ, Hạn giữ, Trạng thái, Hành động.'),
    ('Ô tích của cột bị khóa', 'Icon Button', 'Disable', '–', 'Đang tích',
     'STT và Mã hàng hóa / Nhân viên / Khách hàng có biểu tượng ổ khóa; Hành động mờ, không bỏ '
     'tích được.'),
    ('Nút Lưu', 'Button', 'Enable', '–', 'Hiển thị', 'Ghi cấu hình và vẽ lại bảng.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Thoát, không lưu.'),
], required=False)

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu cột được tích và thứ tự theo người dùng; vẽ lại bảng.'),
    ('Bỏ tích cột bị khóa', 'Click',
     'During:\n– Không cho bỏ tích STT, Mã hàng hóa / Nhân viên / Khách hàng, Hành động.'),
])

# ------------------------------------------------------------ 2.5
d.h3('2.5 Xem chi tiết giữ hàng theo nhân viên và khách hàng')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Xem chi tiết giữ hàng theo nhân viên và khách hàng', 'view', (),
            actor=ACTOR,
            caption='Biểu đồ Use Case — FR-05 Xem chi tiết giữ hàng theo nhân viên và khách hàng')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Danh sách và Màn Xem chi tiết.', anchor='detail')
d.intro_table(
    ten='Mở rộng một hàng hóa xem nhân viên giữ và từng lô theo khách hàng',
    mota='Bấm nút tròn ở cột STT của dòng hàng hóa để chèn ngay bên dưới tầng 2 (mỗi nhân viên '
         'đang giữ hàng hóa đó) và tầng 3 (từng lô theo khách hàng, kèm hạn giữ và trạng thái).',
    tacnhan=ACTOR,
    dieukien='Danh sách có ít nhất một hàng hóa.',
    chinh='1. Người dùng bấm nút mở rộng ở cột STT của một dòng hàng hóa.\n'
          '2. Hệ thống tải chi tiết của hàng hóa đó với ĐÚNG bộ lọc và cửa sổ ngày đang áp.\n'
          '3. Tầng 2 hiện tên nhân viên, phòng ban, tổng SL giữ của nhân viên.\n'
          '4. Tầng 3 hiện “mã KH - tên KH”, SL giữ, Hạn giữ, Trạng thái và nút Lịch sử giữ hàng.\n'
          '5. Bấm lại nút để thu gọn.',
    phu='• Lỗi khi tải → báo “Lỗi khi tải chi tiết giữ hàng”, dòng không mở.\n'
        '• Mở lại hàng hóa đã tải → hiện ngay, không tải lại.\n'
        '• Đổi bộ lọc, sắp xếp hoặc lật trang → mọi dòng đang mở tự thu lại.',
    dacbiet='Tổng SL giữ các nhân viên ở tầng 2 bằng SL giữ của dòng hàng hóa tầng 1.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Mở rộng dòng hàng hóa', shot=shot('05-mo-rong-nhan-vien-khach-hang.png'),
         shot_caption='Dòng hàng hóa đã mở rộng tới nhân viên và khách hàng')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút mở rộng / thu gọn', 'Icon Button', 'Enable', '–', 'Mũi tên phải',
     'Mở thì đổi thành mũi tên xuống; đang tải hiện biểu tượng xoay. Tooltip “Xem chi tiết giữ '
     'hàng” / “Thu gọn”.'),
    ('Dòng tầng 2 — Nhân viên', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Nền xanh lá nhạt. Biểu tượng người + tên nhân viên; cột thứ ba là phòng ban; cột SL giữ là '
     'tổng của nhân viên. Sắp theo tên nhân viên.'),
    ('Dòng tầng 3 — Khách hàng / lô', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Nền xanh dương nhạt. “mã KH - tên KH”, SL giữ, Hạn giữ dd/mm/yyyy, nhãn Trạng thái và '
     'nút Lịch sử giữ hàng. Sắp theo tên khách hàng rồi hạn giữ.'),
    ('Nhãn Trạng thái', 'Badge', 'Read-only', 'Hết hạn / Đến hạn', 'Theo dữ liệu',
     'Hết hạn: hạn giữ trước hôm nay (đỏ). Đến hạn: hạn giữ đúng hôm nay (vàng).'),
], required=False)

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút mở rộng', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng.\n'
     'During:\n– Lấy các lô của hàng hóa, áp phạm vi dữ liệu, cửa sổ ngày và mọi điều kiện lọc '
     'đang áp (khách hàng, nhân viên, công ty, phòng ban, trạng thái).\n'
     '– Gom theo nhân viên, cộng tổng SL giữ.\n'
     'After:\n– Chèn tầng 2 và tầng 3 dưới dòng hàng hóa; ghi nhớ để mở lại không tải lại.'),
    ('Bấm nút thu gọn', 'Click', 'After:\n– Ẩn các dòng tầng 2, 3 của hàng hóa đó.'),
])

# ------------------------------------------------------------ 2.6
d.h3('2.6 Xem lịch sử giữ hàng của lô')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Xem lịch sử giữ hàng của lô', 'view', (), actor=ACTOR,
            caption='Biểu đồ Use Case — FR-06 Xem lịch sử giữ hàng của lô')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Xem sổ biến động số lượng giữ của một lô',
    mota='Cửa sổ “Lịch sử giữ hàng” liệt kê mọi lần số lượng giữ tăng / giảm của bộ hàng hóa × '
         'nhân viên × khách hàng × công ty, kèm chứng từ gây ra biến động.',
    tacnhan=ACTOR,
    dieukien='Đã mở rộng một hàng hóa tới tầng 3.',
    chinh='1. Người dùng bấm nút Lịch sử giữ hàng ở dòng tầng 3.\n'
          '2. Cửa sổ hiện khối thông tin: Mã hàng, Tên hàng, Kinh doanh, Khách hàng, Trạng thái '
          '(kèm “Hạn giữ hiện tại”).\n'
          '3. Bảng biến động sắp CŨ → MỚI: STT, SL biến động, Ngày, SL giữ, Hạn giữ, Chứng từ.\n'
          '4. Dòng tiêu đề phụ ghi “Số lượng giữ hiện tại: X ĐVT.”.\n'
          '5. Người dùng bấm Đóng.',
    phu='• Chưa có biến động → “Chưa có biến động nào.”.\n'
        '• Lỗi khi tải → “Không tải được lịch sử giữ hàng.” kèm nút Thử lại.\n'
        '• Bấm mã chứng từ → mở chứng từ ở thẻ mới.',
    dacbiet='Lịch sử KHÔNG bị bó theo cửa sổ ngày: hiện cả biến động của các lần giữ / gia hạn '
            'cũ. Sắp cũ → mới là chủ ý vì SL giữ là số cộng dồn sau mỗi biến động.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Mở rộng dòng => Lịch sử giữ hàng', modal='Lịch sử giữ hàng',
         shot=shot('06-lich-su-giu-hang.png'),
         shot_caption='Cửa sổ Lịch sử giữ hàng của một lô')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử giữ hàng',
     'Dòng phụ “Hàng hóa: mã - tên”.'),
    ('Khối thông tin lô', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mã hàng, Tên hàng, Kinh doanh (mã - tên nhân viên), Khách hàng (mã - tên), Trạng thái '
     '(nhãn + “Hạn giữ hiện tại: dd/mm/yyyy”).'),
    ('Cột SL biến động', 'Table/Grid', 'Read-only', '+x / −x', 'Theo dữ liệu',
     'Số dương màu xanh, số âm màu đỏ.'),
    ('Cột Ngày', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Ngày phát sinh.'),
    ('Cột SL giữ', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Số lượng giữ sau biến động (cộng dồn).'),
    ('Cột Hạn giữ', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Hạn giữ của lô.'),
    ('Cột Chứng từ', 'Link', 'Enable', 'PXG-…, PGHHG-…', 'Theo dữ liệu',
     'Mã chứng từ gây biến động; là liên kết khi chứng từ có màn xem.'),
    ('Dòng Số lượng giữ hiện tại', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Theo đơn vị đang chọn ở dòng hàng hóa.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lịch sử giữ hàng', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng.\n'
     'During:\n– Lấy mọi lô cùng hàng hóa, nhân viên, khách hàng, công ty và nhật ký biến động '
     'của chúng; KHÔNG áp cửa sổ ngày.\n'
     'After:\n– Hiển thị biến động sắp cũ → mới, số lượng quy theo đơn vị đang chọn.'),
    ('Bấm Thử lại', 'Click', 'After:\n– Tải lại nhật ký biến động.'),
    ('Bấm Đóng / ×', 'Click', 'After:\n– Đóng cửa sổ, bảng giữ nguyên trạng thái mở rộng.'),
])

# ------------------------------------------------------------ 2.7
d.h3('2.7 Xuất danh sách ra Excel')

d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xuất danh sách ra Excel', 'io', (), actor=ACTOR,
            caption='Biểu đồ Use Case — FR-07 Xuất danh sách ra Excel')

d.p('2.7.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất danh sách hàng sắp hết hạn giữ ra tệp Excel',
    mota='Xuất toàn bộ LÔ khớp bộ lọc đang áp (không phân trang) ra tệp phẳng, mỗi dòng một lô, '
         'với các trường người dùng chọn.',
    tacnhan=ACTOR,
    dieukien='Đang ở màn Hàng sắp hết hạn giữ.',
    chinh='1. Người dùng bấm Xuất Excel.\n'
          '2. Cửa sổ “Chọn trường xuất Excel” mở với đủ 12 trường đã tích.\n'
          '3. Người dùng tích / bỏ tích, kéo ≡ để đổi thứ tự cột.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống tải về tệp hang_sap_het_han_giu.xlsx và báo “Xuất Excel thành công”.',
    phu='• Bấm Bỏ chọn hết rồi Xuất file → không xuất.\n'
        '• Lỗi trong lúc xuất → “Lỗi khi xuất Excel”.\n'
        '• Bấm Đóng → thoát, không xuất.',
    dacbiet='Số lượng trong tệp luôn theo ĐƠN VỊ CƠ BẢN, không theo đơn vị đang chọn trên màn. '
            'Tệp sắp theo Phòng ban → Nhân viên → Tên hàng hóa, không theo sắp xếp trên màn.')

d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất Excel',
         shot=shot('07-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất Excel')

d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     '“Tích chọn trường cần xuất, kéo ≡ để đổi thứ tự cột trong file.”'),
    ('Danh sách trường', 'Table/Grid', 'Enable', '12 trường', 'Tích đủ 12',
     'Mã hàng hóa, Tên hàng hóa, ĐVT, Model, Thương hiệu, Nhân viên giữ, Phòng ban, Khách hàng, '
     'SL giữ, Tổng SL trong kho, Hạn giữ, Trạng thái.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', 'Hiển thị', '–'),
    ('Dòng “Đang chọn x/12 trường”', 'Label', 'Read-only', '–', '12/12', 'Đếm số trường đang tích.'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', 'Hiển thị', 'Bị khóa khi đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Thoát, không xuất.'),
], required=False)

d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền; khóa nút để tránh bấm hai lần.\n'
     'During:\n– Lấy mọi lô khớp phạm vi, cửa sổ ngày và bộ lọc đang áp.\n'
     'After:\n– Dựng tệp: dòng 1 “DANH SÁCH HÀNG SẮP HẾT HẠN GIỮ”, dòng 2 tiêu đề cột, cột STT '
     'luôn đứng đầu, các cột theo thứ tự trong danh sách; số ghi kiểu số định dạng #,##0.##; ngày '
     'dd/mm/yyyy.\n'
     '– Tải tệp, đóng cửa sổ, báo “Xuất Excel thành công”.'),
])

# ------------------------------------------------------------ 2.8
d.h3('2.8 In danh sách')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'In danh sách', 'io', (), actor=ACTOR,
            caption='Biểu đồ Use Case — FR-08 In danh sách')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX.', anchor='notice')
d.intro_table(
    ten='In danh sách hàng sắp hết hạn giữ',
    mota='Dựng bản in theo bộ lọc đang áp, gom Phòng ban → Nhân viên → từng lô, hiển thị trong '
         'cửa sổ xem trước khổ ngang rồi gửi lệnh in.',
    tacnhan=ACTOR,
    dieukien='Đang ở màn Hàng sắp hết hạn giữ.',
    chinh='1. Người dùng bấm In.\n'
          '2. Hệ thống dựng bản in và mở cửa sổ “Xem trước danh sách hàng sắp hết hạn giữ”.\n'
          '3. Người dùng bấm In trong cửa sổ để gửi lệnh in.',
    phu='• Không có dữ liệu → cửa sổ báo “Không có dữ liệu để in”.\n'
        '• Vượt 10,000 dòng in → báo danh sách vượt mức in tối đa, đề nghị thu hẹp bộ lọc hoặc '
        'dùng Xuất Excel; không hiện bản xem trước.\n'
        '• Bấm × → đóng cửa sổ.',
    dacbiet='Tiêu đề công ty (letterhead) theo công ty người đang đăng nhập. Số lượng theo đơn vị '
            'cơ bản.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => In', modal='Xem trước danh sách hàng sắp hết hạn giữ',
         shot=shot('08-in-danh-sach.png'),
         shot_caption='Cửa sổ xem trước bản in danh sách hàng sắp hết hạn giữ')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bản in', 'Label', 'Hiển thị', '–', 'DANH SÁCH HÀNG SẮP HẾT HẠN GIỮ', '–'),
    ('Khối thông tin chung', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Ngày in (dd/mm/yyyy), Số phòng ban, Số nhân viên, Số mục hàng (= số lô).'),
    ('Dòng nhóm Phòng ban', 'Table/Grid', 'Read-only', 'STT 1, 2…', 'Theo dữ liệu',
     '“Tên phòng ban - x nhân viên - y mục hàng”. Nhân viên chưa gán phòng ban gom vào “Chưa gán '
     'phòng ban”.'),
    ('Dòng nhóm Nhân viên', 'Table/Grid', 'Read-only', 'STT 1.1…', 'Theo dữ liệu',
     '“Tên nhân viên - y mục hàng”.'),
    ('Dòng mục hàng', 'Table/Grid', 'Read-only', 'STT 1.1.1…', 'Theo dữ liệu',
     'Tên hàng hóa, Mã hàng, ĐVT, SL giữ, Hạn giữ, Khách hàng, Trạng thái.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Gửi lệnh in của trình duyệt.'),
    ('Nút ×', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ xem trước.'),
], required=False)

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In ở thanh công cụ', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng.\n'
     'During:\n– Lấy mọi lô khớp phạm vi, cửa sổ ngày, bộ lọc; gom Phòng ban → Nhân viên → lô; '
     'đếm dòng in.\n'
     'After:\n– ≤ 10,000 dòng: mở bản xem trước. Vượt: hiện câu nhắc thu hẹp bộ lọc.'),
    ('Bấm In trong cửa sổ', 'Click', 'After:\n– Mở hộp thoại in của trình duyệt.'),
])

# ==================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('- Quy tắc chung toàn hệ thống. Bảng dưới đây chỉ liệt kê quy tắc đặc thù của màn '
           'Hàng sắp hết hạn giữ.', head='Quy tắc áp dụng', anchor='list')

d.rule_table([
    ('BR-01', 'Cửa sổ ngày “sắp hết hạn” (giữ nguyên hệ thống cũ)', [
        '– Chỉ lấy lô có số lượng giữ > 0 và hạn giữ nằm trong [hôm nay − N ngày, hôm nay], tính '
        'cả hai đầu. N = số ngày cảnh báo cấu hình chung (hiện 7).',
        '– Ví dụ hôm nay 05/10/2026, N = 7: lấy hạn giữ từ 28/09/2026 đến 05/10/2026; lô hạn '
        '27/09/2026 hoặc 06/10/2026 KHÔNG hiện.',
        '– Tức màn hình liệt kê hàng ĐÃ / VỪA hết hạn giữ trong N ngày gần đây, ngược chiều với '
        'màn Yêu cầu gia hạn hàng giữ (nhìn tới trước). Đây là quyết định CÓ CHỦ ĐÍCH để đối chiếu '
        'số liệu với hệ thống cũ, KHÔNG phải lỗi.',
        '– Hệ quả: cột và ô lọc Trạng thái chỉ có Hết hạn (hạn trước hôm nay) và Đến hạn (hạn đúng '
        'hôm nay); KHÔNG BAO GIỜ có Trong hạn.',
        '– Cờ cửa sổ ngày do máy chủ tự bật cho mọi chức năng của màn, giao diện không gửi lên.',
    ], ['Xem danh sách', 'Xem chi tiết', 'Xuất Excel', 'In']),
    ('BR-02', 'Quyền truy cập', [
        '– Bắt buộc có quyền Quản lý giữ hàng (Super Admin được miễn), khác hệ thống cũ vốn mở '
        'cho mọi tài khoản.',
        '– Thiếu quyền: mọi chức năng báo “Bạn không có quyền xem danh sách hàng sắp hết hạn giữ”. '
        'Mục menu không gắn quyền nên vẫn hiển thị.',
    ], 'Toàn màn hình'),
    ('BR-03', 'Phạm vi dữ liệu', [
        '– Thứ tự: tổng công ty → công ty → phòng ban → chỉ lô của mình.',
        '– Cấp phòng ban: lô do nhân viên thuộc phòng ban mình quản lý và phòng ban của mình đứng '
        'tên, cộng lô của chính mình.',
        '– Áp cho cả 3 tầng, nguồn ô lọc, tệp Excel và bản in.',
    ], 'Toàn màn hình'),
    ('BR-04', 'Cấu trúc 3 tầng và cách cộng số', [
        '– Tầng 1 = hàng hóa; SL giữ = tổng SL các lô trong cửa sổ ngày khớp bộ lọc (KHÔNG phải '
        'toàn bộ hàng đang giữ của hàng hóa).',
        '– Tầng 2 = nhân viên; tổng các tầng 2 = SL giữ tầng 1.',
        '– Tầng 3 = lô theo khách hàng và hạn giữ; chỉ tầng này có Hạn giữ, Trạng thái, Lịch sử.',
        '– Tầng 2, 3 dùng CHUNG bộ lọc với tầng 1 (vá lỗi hệ thống cũ bung chi tiết luôn rỗng).',
    ], ['Xem danh sách', 'Xem chi tiết']),
    ('BR-05', 'Tổng SL trong kho', [
        '– Tổng tồn kho kế toán của hàng hóa trên mọi kho kế toán thuộc công ty trong phạm vi '
        '(người không có V1 chỉ tính công ty đang đăng nhập; chọn ô Công ty thì tính công ty đó).',
        '– Ô Lọc theo kho chỉ quyết định hàng hóa nào được hiện, KHÔNG thu hẹp số Tổng SL trong '
        'kho về riêng kho đã chọn.',
        '– Không có tồn kho → để trống.',
    ], ['Xem danh sách', 'Xuất Excel']),
    ('BR-06', 'Đơn vị tính', [
        '– Mặc định đơn vị cơ bản. Hàng hóa có ≥ 2 đơn vị mới có ô chọn.',
        '– Số hiển thị = số cơ bản ÷ hệ số, làm tròn XUỐNG 2 chữ số; định dạng 1,234.56.',
        '– Tệp Excel và bản in luôn theo đơn vị cơ bản.',
    ], ['Xem danh sách', 'Xem chi tiết', 'Lịch sử']),
    ('BR-07', 'Nguồn dữ liệu ô lọc', [
        '– Lọc theo kho: chỉ kho kế toán đang hoạt động (bỏ kho Chờ xóa, ngừng dùng) trong phạm vi '
        'công ty; màn Danh sách hàng giữ vẫn liệt kê cả kho đã khóa.',
        '– Nhân viên / Thương hiệu / Model: lấy theo hàng đang giữ trong phạm vi, CHƯA bó theo cửa '
        'sổ ngày nên có thể chọn ra bảng rỗng.',
        '– Trạng thái: chỉ Hết hạn, Đến hạn.',
        '– Ô tìm nhanh tìm theo tên, mã, số điện thoại khách hàng.',
    ], 'Tìm kiếm và lọc'),
    ('BR-08', 'Màn hình chỉ đọc', [
        '– Không có Thêm, Sửa, Xóa, Import; không thay đổi tồn hàng giữ.',
        '– Muốn xử lý lô hết hạn: dùng màn Yêu cầu gia hạn hàng giữ hoặc Yêu cầu hủy hàng giữ.',
    ], 'Toàn màn hình'),
    ('BR-09', 'Lịch sử giữ hàng', [
        '– Không bó theo cửa sổ ngày; sắp cũ → mới; SL giữ là số cộng dồn.',
        '– Chứng từ là liên kết mở thẻ mới khi có màn xem.',
    ], 'Lịch sử giữ hàng'),
    ('BR-10', 'Xuất Excel và In', [
        '– Phẳng 1 dòng = 1 lô, sắp Phòng ban → Nhân viên → Tên hàng hóa, không theo sắp xếp màn.',
        '– Bản in tối đa 10,000 dòng (tính cả dòng nhóm); vượt thì không in, nhắc thu hẹp bộ lọc.',
        '– Số mục hàng trên bản in = số lô, có thể lớn hơn tổng N ở chân bảng (đếm hàng hóa).',
    ], ['Xuất Excel', 'In']),
])

d.save()
