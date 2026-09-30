# -*- coding: utf-8 -*-
"""Sinh SRS man "Phieu xuat giu" (PXG) theo FORM CHUAN 2026-08-28.

Nguon: code HRM nhanh `gop_db`
  BE  Modules/Finance/{Entities/PrepickExport/WarehousePrepickRequest.php,
      Services/WarehousePrepickRequestService.php,
      Http/Controllers/V1/WarehousePrepickRequestController.php,
      Http/Requests/PrepickExport/WarehousePrepickRequestStoreRequest.php}
  FE  pages/finance/warehouse-prepick-requests/*
Anh chup that: ./warehouse_prepick_shots (Playwright MCP, 1440x900, ngay 18/09/2026).
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
from srs_docx_lib import SrsDoc, ACTOR_P1, ACTOR_BOTH  # noqa: E402

SHOTS = os.path.join(BASE, 'warehouse_prepick_shots')
OUT = os.path.join(BASE, 'SRS - Phieu xuat giu.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Giữ hàng => Phiếu xuất giữ'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/warehouse-prepick-requests',
           full_url='https://<host-hrm>/finance/warehouse-prepick-requests',
           img_prefix='pxg_')

# ============================================================== TRANG DAU
d.title_block('Phiếu xuất giữ')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu xuất giữ (mã phiếu PXG), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, luồng xử lý và phân quyền của màn hình.',
    'Làm rõ vị trí của màn hình trong nghiệp vụ giữ hàng: đây là chứng từ DUY NHẤT sinh ra lô '
    'hàng giữ trong toàn hệ thống.',
    'Làm rõ quan hệ cha – con với màn Yêu cầu xuất giữ: mỗi phiếu xuất giữ luôn thuộc về đúng '
    'một yêu cầu, và không tồn tại độc lập.',
    'Làm rõ ba trạng thái của phiếu cùng tác động của từng trạng thái lên yêu cầu nguồn.',
    'Làm rõ điểm dễ sai nhất: chủ lô hàng giữ là NGƯỜI LẬP YÊU CẦU, không phải Kế toán lập phiếu.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hàng giữ', 'Số lượng hàng hóa trong kho được giữ lại cho một khách hàng cụ thể, do một '
                 'nhân viên kinh doanh đứng tên giữ, tới một hạn nhất định.'),
    ('Lô hàng giữ', 'Một dòng tồn hàng giữ, xác định bởi bộ: người giữ – khách hàng – hàng hóa '
                    '– hạn giữ – công ty.'),
    ('Yêu cầu xuất giữ', 'Phiếu đề nghị giữ hàng do nhân viên kinh doanh lập, mã PYCXG. Là '
                         'phiếu CHA của phiếu xuất giữ.'),
    ('Phiếu xuất giữ', 'Phiếu do Kế toán lập từ một yêu cầu đã qua đủ các cấp duyệt, mã PXG. '
                       'Duyệt phiếu này là lúc hàng thực sự được giữ.'),
    ('Người yêu cầu', 'Người đã lập yêu cầu xuất giữ. Chính người này đứng tên giữ hàng sau khi '
                      'phiếu được duyệt.'),
    ('Phòng yêu cầu', 'Phòng ban của người yêu cầu tại thời điểm lập yêu cầu.'),
    ('SL có thể giữ', 'Tồn kho khả dụng của hàng hóa, đã trừ phần hàng khuyến mại.'),
    ('SL yêu cầu', 'Số lượng người lập yêu cầu đã xin giữ cho dòng hàng đó.'),
    ('SL xuất giữ', 'Số lượng Kế toán chốt thực xuất giữ. Không vượt quá SL yêu cầu.'),
    ('SL giữ (ĐV cơ bản)', 'Số lượng đã quy đổi về đơn vị cơ bản và cộng thật vào tồn hàng giữ. '
                           'Chỉ hiển thị ở màn chi tiết của phiếu đã duyệt.'),
    ('Đang tạo', 'Trạng thái nháp của phiếu. Chưa ghi tồn hàng giữ; yêu cầu nguồn đang ở '
                 'Đang xuất giữ.'),
    ('Đã duyệt', 'Phiếu đã được duyệt, tồn hàng giữ đã được ghi, yêu cầu nguồn chuyển sang '
                 'Đã duyệt.'),
], widths=[1.6, 4.4])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Màn hình này không có chức năng “Tạo mới” độc lập: phiếu luôn được lập từ một yêu cầu xuất '
    'giữ đang ở bước Kế toán xử lý. Vì vậy quyền lập phiếu chính là quyền xử lý bước Kế toán '
    'của yêu cầu.')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán duyệt hàng giữ',
     'Lập được phiếu xuất giữ từ một yêu cầu đang ở Chờ KT duyệt, cùng công ty với mình. Đây '
     'cũng là quyền cho phép bấm Duyệt giữ hàng — bước ghi tồn hàng giữ. Người có quyền này '
     'còn xem được mọi phiếu trong công ty mình.'),
], widths=[0.8, 2.0, 3.2])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu hàng giữ theo tổng công ty', 'Toàn bộ phiếu của mọi công ty.'),
    ('V2', 'Xem phiếu hàng giữ theo công ty', 'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem phiếu hàng giữ theo phòng ban',
     'Phiếu thuộc các phòng ban mà người đăng nhập được phân công quản lý, cộng phòng ban của '
     'chính người đó, cộng phiếu do chính người đó lập.'),
    ('—', '(không có cấp nào)', 'Chỉ phiếu do chính mình lập.'),
], widths=[0.8, 2.0, 3.2])

d.p('Bốn quy tắc chung áp cho mọi cấp:')
d.bullets([
    'Phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy, kể cả với người có quyền xem rộng nhất.',
    'Công ty và phòng ban của phiếu lấy theo NGƯỜI LẬP YÊU CẦU, không phải người lập phiếu. Vì '
    'vậy phạm vi dữ liệu của phiếu chạy theo tổ chức của bên yêu cầu.',
    'Chỉ người lập phiếu mới sửa hoặc xóa được phiếu của mình, và chỉ khi phiếu còn nháp.',
    'Màn danh sách và màn chi tiết dùng CÙNG một bộ điều kiện: nhìn thấy phiếu trong danh sách '
    'thì mở được chi tiết, và ngược lại.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1/V2/V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ (cả công ty)', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột hiển thị', '✅', '✅', '✅'),
    ('FR-05 Lập phiếu xuất giữ', '✅ (từ yêu cầu Chờ KT duyệt)', '❌', '❌'),
    ('FR-06 Chỉnh sửa phiếu', '✅ (phiếu của mình, Đang tạo)', '✅ (nt)', '✅ (nt)'),
    ('FR-07 Xem chi tiết phiếu', '✅', '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-08 Duyệt giữ hàng', '✅ (phiếu của mình, Đang tạo)', '❌', '❌'),
    ('FR-09 Xóa phiếu', '✅ (phiếu của mình, Đang tạo)', '✅ (nt)', '✅ (nt)'),
    ('FR-10 In phiếu / In danh sách', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-11 Xuất Excel danh sách', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-12 Xem lịch sử thay đổi', '✅', '✅', '✅ (phiếu của mình)'),
], widths=[2.3, 1.5, 1.2, 1.0])

# ================================================ PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [('Kế toán', [0, 1, 2, 3]),
     ('Người xem theo quyền', [0, 3])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu xuất giữ', 'crud'),
     ('FR-06', 'Chỉnh sửa phiếu nháp', 'crud'),
     ('FR-07', 'Xem chi tiết phiếu', 'view')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-11', 'Xuất Excel danh sách', 'io', 'extend', [0], None),
     ('FR-09', 'Xóa phiếu', 'action', 'extend', [0], None),
     ('FR-13', 'Chọn yêu cầu nguồn', 'crud', 'include', [1], None),
     ('FR-08', 'Duyệt giữ hàng', 'action', 'extend', [1, 2], None),
     ('FR-10', 'In phiếu', 'io', 'extend', [3], None),
     ('FR-12', 'Xem lịch sử thay đổi', 'view', 'extend', [3], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu xuất giữ')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách phiếu')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu xuất giữ tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu xuất giữ',
    mota='Hiển thị bảng phiếu nằm trong phạm vi dữ liệu của người đăng nhập, kèm bộ lọc, '
         'phân trang và ô thống kê tổng số phiếu khớp bộ lọc.',
    tacnhan='Kế toán; Người dùng có quyền xem theo cấp; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng vào menu Tài chính → Giữ hàng → Phiếu xuất giữ.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem của người dùng.\n'
          '3. Người có quyền Kế toán duyệt hàng giữ được xem thêm toàn bộ phiếu trong công ty '
          'mình.\n'
          '4. Hệ thống loại khỏi phạm vi mọi phiếu Đang tạo không phải của người dùng.\n'
          '5. Hệ thống trả về trang đầu tiên của danh sách và tổng số phiếu.\n'
          '6. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Phiếu Đang tạo của người khác không xuất hiện trong danh sách.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet='Phạm vi dữ liệu chạy theo công ty và phòng ban của NGƯỜI LẬP YÊU CẦU, vì phiếu chép '
            'tổ chức từ yêu cầu nguồn chứ không lấy theo Kế toán lập phiếu.')

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Phiếu xuất giữ lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Phiếu xuất giữ',
     'Tiêu đề cố định phía trên bảng.'),
    ('Nút Lập từ yêu cầu', 'Button', 'Enable', '–', 'Hiển thị',
     'Điều hướng sang màn Yêu cầu xuất giữ để chọn yêu cầu cần lập phiếu. Chú thích khi rê '
     'chuột: “Lập phiếu xuất giữ từ một yêu cầu đã được duyệt”.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ xem trước bản in danh sách theo đúng bộ lọc đang áp.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ chọn trường xuất; bị khóa trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục', 'Cột cố định.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PXG-NNNNN', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết. Cột cố định, sắp xếp được.'),
    ('Cột Yêu cầu xuất giữ', 'Table/Grid', 'Read-only', 'PYCXG-NNNNN', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết của yêu cầu nguồn trong tab mới.'),
    ('Cột Người yêu cầu / Phòng yêu cầu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là người lập yêu cầu và phòng ban của họ, KHÔNG phải người lập phiếu này.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Người lập phiếu xuất giữ, tức Kế toán. Cột Ngày tạo sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Đang tạo / Đã duyệt', 'Theo dữ liệu',
     'Đang tạo màu xám; Đã duyệt màu xanh lá. Dữ liệu cũ còn có thể mang trạng thái Chờ duyệt '
     'màu cam.'),
    ('Cột Người duyệt / Ngày duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Để trống cho tới khi phiếu được duyệt. Cột Ngày duyệt sắp xếp được.'),
    ('Cột Khách hàng / Giữ đến ngày / Người cập nhật / Ngày cập nhật / Ghi chú', 'Table/Grid',
     'Read-only', '–', 'Ẩn mặc định',
     'Bật lên trong cửa sổ Tuỳ chỉnh cột. Cột Giữ đến ngày sắp xếp được.'),
    ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Cột cố định cuối bảng, chứa các nút thao tác của dòng.'),
    ('Nút Sửa / Xóa', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện với phiếu do chính mình lập và đang ở trạng thái Đang tạo.'),
    ('Nút In / Lịch sử', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'In mở cửa sổ xem trước bản in phiếu; Lịch sử mở cửa sổ lịch sử thay đổi.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc trong phạm vi quyền.'),
    ('Phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100', 'Trang 1, 10 dòng', '–'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện dòng “Không có dữ liệu phù hợp.” khi không có phiếu nào khớp.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị',
     'Hiện ngay khi vào màn và trong lúc nạp lại dữ liệu.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định cấp quyền xem của người dùng theo thứ tự ưu tiên tổng công ty → '
     'công ty → phòng ban → chỉ phiếu của mình.\n'
     'During:\n– Áp phạm vi dữ liệu; người có quyền Kế toán duyệt hàng giữ được cộng thêm toàn '
     'bộ phiếu cùng công ty.\n'
     '– Loại khỏi kết quả mọi phiếu Đang tạo không do người dùng lập.\n'
     '– Khôi phục bộ lọc đã lưu của người dùng nếu còn hiệu lực (10 phút).\n'
     'After:\n– Trả về trang 1, tổng số phiếu và danh sách trạng thái để đổ vào ô lọc.'),
    ('Bấm vào mã phiếu', 'Click',
     'Before:\n– Kiểm tra người dùng có được xem phiếu này không.\n'
     '– Nếu không → hệ thống báo không có quyền xem phiếu và không mở màn chi tiết.\n'
     'After:\n– Mở màn chi tiết của phiếu.'),
    ('Bấm vào mã yêu cầu xuất giữ', 'Click',
     'After:\n– Mở màn chi tiết của yêu cầu nguồn trong TAB MỚI, không rời màn đang xem.'),
    ('Bấm tiêu đề cột có mũi tên sắp xếp', 'Click',
     'During:\n– Chỉ bốn cột Mã phiếu, Ngày tạo, Ngày duyệt và Giữ đến ngày sắp xếp được.\n'
     'After:\n– Nạp lại danh sách từ trang 1 theo thứ tự mới, giữ nguyên bộ lọc.'),
    ('Bấm số trang / nút tiến lùi / đổi số dòng mỗi trang', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu trang mới; số thứ tự tiếp tục liên tục.'),
    ('Bấm nút Lập từ yêu cầu', 'Click',
     'After:\n– Điều hướng sang màn Yêu cầu xuất giữ; người dùng chọn yêu cầu ở đó rồi bấm Lập '
     'phiếu xuất giữ.'),
])

# ------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu xuất giữ',
    mota='Thu hẹp danh sách theo mã phiếu, mã yêu cầu nguồn, trạng thái, người tạo, người duyệt, '
         'người yêu cầu, khách hàng, hàng hóa, khoảng ngày tạo và khối công ty – phòng ban.',
    tacnhan='Kế toán; Người dùng có quyền xem theo cấp',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh hoặc bấm Tìm kiếm nâng cao.\n'
          '2. Người dùng chọn / nhập các tiêu chí cần lọc.\n'
          '3. Hệ thống nạp lại danh sách ngay khi một ô lọc nâng cao thay đổi; riêng ô tìm '
          'nhanh chờ người dùng bấm nút Tìm kiếm.\n'
          '4. Bảng hiển thị kết quả và cập nhật lại tổng số phiếu.',
    phu='• Không có phiếu nào khớp → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Bấm Làm mới → xóa toàn bộ tiêu chí, bỏ sắp xếp và nạp lại danh sách từ đầu.\n'
        '• Bộ lọc được ghi nhớ trong 10 phút.',
    dacbiet='Ô lọc “Tên, mã hàng” chỉ tìm trong những dòng hàng ĐƯỢC TÍCH “Cần xuất”, tức những '
            'dòng thực sự được xuất giữ.')

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('02-bo-loc-nang-cao.png'),
         shot_caption='Bảng lọc nâng cao đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Gợi ý “Tìm theo mã phiếu...”. Chỉ tìm khi bấm nút Tìm kiếm hoặc nhấn Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', 'Hiển thị', 'Áp dụng ô tìm nhanh, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Xóa mọi tiêu chí lọc và nạp lại danh sách.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Đang thu gọn',
     'Đóng / mở bảng lọc nâng cao.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ bật / tắt và sắp xếp thứ tự các ô lọc.'),
    ('Công ty / Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Trống',
     'Hiện theo cấp quyền xem của người dùng.'),
    ('Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Lọc riêng theo mã phiếu xuất giữ.'),
    ('Yêu cầu xuất giữ', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Lọc theo mã yêu cầu nguồn.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách trạng thái', 'Trống', '–'),
    ('Người tạo / Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống',
     'Là người lập và người duyệt của chính phiếu xuất giữ.'),
    ('Người yêu cầu', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống',
     'Lọc theo người lập yêu cầu nguồn — cũng là người sẽ đứng tên giữ hàng.'),
    ('Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng', 'Trống', '–'),
    ('Tên, mã hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Một ô lọc chung cho cả tên và mã hàng hóa; chỉ xét dòng có tích Cần xuất.'),
    ('Ngày tạo từ / Ngày tạo đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống',
     'Lọc theo khoảng ngày lập phiếu, không phải ngày duyệt và không phải hạn giữ.'),
], required=False)

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'During:\n– Ghi giá trị mới vào bộ tiêu chí đang áp.\n'
     'After:\n– Về trang 1 và nạp lại danh sách ngay, không cần bấm nút.'),
    ('Bấm nút Tìm kiếm', 'Click',
     'After:\n– Áp thêm nội dung ô tìm nhanh, về trang 1 và nạp lại danh sách.\n'
     '– Từ khóa dài từ 2 ký tự trở lên còn được dùng để xếp kết quả: trùng khít lên trước, rồi '
     'tới bắt đầu bằng, rồi tới chỉ chứa.'),
    ('Bấm nút Làm mới', 'Click',
     'During:\n– Đặt lại mọi ô lọc về trống và bỏ thứ tự sắp xếp.\n'
     'After:\n– Nạp lại danh sách từ trang 1 theo phạm vi quyền.'),
    ('Lọc theo Yêu cầu xuất giữ', 'Change',
     'After:\n– Chỉ giữ những phiếu có yêu cầu nguồn khớp mã đã nhập.\n'
     '– Điều kiện này áp cả cho bản in danh sách và tệp Excel xuất ra.'),
])

# ------------------------------------------------------------ 2.3
d.h3('2.3 Cài đặt bộ lọc')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc', 'view',
            [('include', 'Lưu cấu hình theo từng người dùng'),
             ('extend', 'Khôi phục mặc định')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Bộ lọc và Cấu hình cột.', anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc hiển thị',
    mota='Cho phép người dùng tự chọn những ô lọc muốn hiển thị và kéo sắp xếp lại thứ tự. '
         'Cấu hình lưu riêng theo từng người dùng và từng màn hình.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc.\n'
          '2. Hệ thống mở cửa sổ liệt kê các ô lọc của màn.\n'
          '3. Người dùng bỏ tích ô không dùng, kéo đổi thứ tự nếu cần.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình và vẽ lại bảng lọc.',
    phu='• Bấm Khôi phục mặc định → đưa danh sách ô lọc về trạng thái ban đầu.\n'
        '• Bấm Đóng → giữ nguyên cấu hình cũ.',
    dacbiet=None)

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('04-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc',
     'Kèm dòng hướng dẫn tích chọn và kéo sắp xếp.'),
    ('Danh sách ô lọc', 'Table/Grid', 'Enable', '11 mục', '–', 'Theo cấu hình đã lưu',
     'Mỗi mục gồm số thứ tự, tay kéo, ô tích và tên ô lọc.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình và đóng cửa sổ.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đưa về danh sách và thứ tự ban đầu.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
])

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Cài đặt bộ lọc', 'Click',
     'After:\n– Mở cửa sổ với cấu hình hiện tại của người dùng.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Ghi cấu hình theo người dùng và vẽ lại bảng lọc nâng cao.'),
])

# ------------------------------------------------------------ 2.4
d.h3('2.4 Tuỳ chỉnh cột hiển thị')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view',
            [('include', 'Lưu cấu hình cột theo từng người dùng')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-04 Tuỳ chỉnh cột hiển thị')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Cấu hình cột hiển thị.', anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh cột hiển thị của bảng danh sách',
    mota='Cho phép bật / tắt và kéo sắp xếp các cột của bảng. Ba cột STT, Mã phiếu và Hành động '
         'bị khóa, luôn hiển thị.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
          '2. Hệ thống mở cửa sổ Tuỳ chỉnh cột.\n'
          '3. Người dùng bật / tắt cột, kéo đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình và vẽ lại bảng.',
    phu='• Bấm Đóng → giữ nguyên cấu hình cũ.\n'
        '• Ba cột bị khóa không bỏ tích và không kéo được.',
    dacbiet='Năm cột Khách hàng, Giữ đến ngày, Người cập nhật, Ngày cập nhật và Ghi chú mặc '
            'định TẮT.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột hiển thị', shot=shot('05-cau-hinh-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '15 cột', '–', 'Theo cấu hình đã lưu',
     'Mỗi dòng gồm ô tích, tên cột và tay kéo.'),
    ('Cột bị khóa', 'Icon', 'Read-only', '–', '–', 'Biểu tượng ổ khóa',
     'STT, Mã phiếu và Hành động luôn hiển thị.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình và vẽ lại bảng.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bỏ tích một cột', 'Change',
     'During:\n– Cột bị khóa thì không cho bỏ tích.\n'
     'After:\n– Đánh dấu cột sẽ ẩn; chưa ghi cho tới khi bấm Lưu.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Ghi cấu hình theo người dùng và vẽ lại bảng theo đúng thứ tự đã chọn.'),
])

# ------------------------------------------------------------ 2.5
d.h3('2.5 Lập phiếu xuất giữ')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Lập phiếu xuất giữ từ một yêu cầu', 'crud',
            [('include', 'Kiểm tra yêu cầu đang ở bước Kế toán xử lý'),
             ('include', 'Chép thông tin khách hàng và tổ chức từ yêu cầu'),
             ('include', 'Sinh mã phiếu tự động'),
             ('extend', 'Đính kèm tệp')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-05 Lập phiếu xuất giữ')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Lập phiếu xuất giữ từ một yêu cầu đã duyệt đủ cấp',
    mota='Kế toán chốt số lượng thực xuất giữ và hạn giữ cho một yêu cầu đang ở bước Chờ KT '
         'duyệt. Phiếu có thể lưu nháp, hoặc duyệt luôn để ghi tồn hàng giữ.',
    tacnhan='Kế toán',
    dieukien='Yêu cầu nguồn đang ở trạng thái Chờ KT duyệt; người dùng có quyền Kế toán duyệt '
             'hàng giữ và cùng công ty với yêu cầu.',
    chinh='1. Kế toán mở màn chi tiết yêu cầu xuất giữ rồi bấm Lập phiếu xuất giữ.\n'
          '2. Hệ thống mở màn lập phiếu, gắn sẵn yêu cầu nguồn và nạp toàn bộ dòng hàng đã được '
          'xin giữ.\n'
          '3. Hệ thống điền sẵn khách hàng, hợp đồng, người yêu cầu, phòng yêu cầu và Giữ đến '
          'ngày theo yêu cầu nguồn.\n'
          '4. Kế toán bỏ tích những dòng không xuất, sửa lại SL xuất giữ nếu cần.\n'
          '5. Kế toán bấm Lưu nháp, hoặc Duyệt giữ hàng.\n'
          '6. Hệ thống kiểm tra dữ liệu, sinh mã phiếu và ghi phiếu.\n'
          '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Lưu nháp → phiếu ở trạng thái Đang tạo; yêu cầu nguồn chuyển sang Đang xuất giữ.\n'
        '• Duyệt giữ hàng → hệ thống ghi tồn hàng giữ; yêu cầu nguồn chuyển sang Đã duyệt.\n'
        '• Không tích dòng nào, hoặc tích nhưng số lượng đều bằng 0 → báo lỗi, không lưu.\n'
        '• SL xuất giữ vượt SL yêu cầu → báo lỗi tại dòng, không lưu.\n'
        '• Duyệt mà tồn kho không đủ → báo “Kho không đủ số lượng (còn …).” và không lưu.\n'
        '• Yêu cầu đã có phiếu xuất giữ → hệ thống báo và không cho lập phiếu thứ hai.',
    dacbiet='Màn này KHÔNG có nút Tạo mới độc lập. Không vào được màn lập phiếu nếu không đi từ '
            'một yêu cầu đang ở bước Kế toán xử lý.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Lập từ yêu cầu', shot=shot('03-lap-phieu.png'),
         shot_caption='Màn lập phiếu xuất giữ, dữ liệu nạp sẵn từ yêu cầu nguồn')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Người lập – Ngày lập', 'Label', 'Read-only', '–', '–',
     'Người đăng nhập – ngày hiện tại', 'Hiển thị ở góc phải khối Thông tin chung.'),
    ('Yêu cầu xuất giữ', 'Link', 'Read-only', 'PYCXG-NNNNN', '–', 'Theo yêu cầu nguồn',
     'Là liên kết mở yêu cầu nguồn trong tab mới. Ô khóa có biểu tượng ⓘ giải thích vì sao '
     'không đổi được yêu cầu nguồn.'),
    ('Loại yêu cầu', 'Textbox', 'Disable', '–', '–', 'Theo yêu cầu nguồn', 'Chỉ hiển thị.'),
    ('Hợp đồng', 'Textbox', 'Disable', '–', '–', 'Theo yêu cầu nguồn',
     'Ẩn hẳn khi yêu cầu nguồn thuộc loại Xuất giữ khác, vì loại đó không gắn hợp đồng.'),
    ('Người yêu cầu / Phòng yêu cầu', 'Textbox', 'Disable', '–', '–', 'Theo yêu cầu nguồn',
     'Là người lập yêu cầu và phòng ban của họ. Chính người này sẽ đứng tên giữ hàng.'),
    ('Giữ đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Theo yêu cầu nguồn',
     'Kế toán sửa lại được. Dưới ô có dòng nhắc hạn này sẽ ghi thẳng vào lô hàng giữ khi bấm '
     'Duyệt giữ hàng.'),
    ('Khách hàng / Địa chỉ', 'Textbox', 'Disable', '–', '–', 'Theo yêu cầu nguồn',
     'Ô Địa chỉ ẩn hẳn khi dữ liệu trống, để không hiện một ô xám rỗng.'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Theo yêu cầu nguồn', '–'),
    ('Chọn tệp đính kèm', 'Button', 'Enable',
     'PDF, ảnh, Word, Excel; tối đa 13 MB mỗi tệp', 'Không', 'Chưa có tệp',
     'Chọn được nhiều tệp; mỗi tệp có nút gỡ khỏi phiếu.'),
    ('Cột Cần xuất', 'Checkbox', 'Enable', '–', '–', 'Tích sẵn theo yêu cầu',
     'Bỏ tích thì dòng bị làm mờ, ô số lượng khóa lại và dòng được lưu với số lượng 0.'),
    ('Cột Tên hàng hóa / Mã hàng hóa / Model / Thương hiệu', 'Table/Grid', 'Read-only', '–', '–',
     'Theo yêu cầu nguồn', 'Không sửa được; không thêm hay xóa dòng.'),
    ('Cột SL có thể giữ', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo tồn kho',
     'Tồn kho khả dụng đã trừ hàng khuyến mại — đúng con số hệ thống dùng khi duyệt.'),
    ('Cột SL yêu cầu', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo yêu cầu nguồn',
     'Là trần của SL xuất giữ.'),
    ('Cột SL xuất giữ', 'Number', 'Enable', '> 0 và ≤ SL yêu cầu', 'Có', 'Bằng SL yêu cầu',
     'Chỉ nhận ký tự số. Nhập sai thì báo đỏ tại dòng và giữ nguyên số đã gõ.'),
    ('Cột ĐVT', 'Table/Grid', 'Read-only', '–', '–', 'Theo yêu cầu nguồn',
     'Không đổi được đơn vị tính ở màn này.'),
    ('Dòng Tổng cộng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Cộng cột SL yêu cầu và SL xuất giữ.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Ghi phiếu ở trạng thái Đang tạo, chưa ghi tồn hàng giữ.'),
    ('Nút Duyệt giữ hàng', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Ghi tồn hàng giữ. Có hộp thoại xác nhận riêng vì thao tác không hoàn tác được.'),
    ('Nút Không duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu phiếu ở trạng thái Đang tạo, giống nút Lưu nháp. Nút này KHÔNG trả yêu cầu về cho '
     'người lập.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi tại ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi; không tự sửa giá trị người dùng đã nhập.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn lập phiếu', 'System',
     'Before:\n– Kiểm tra yêu cầu nguồn tồn tại và đang ở trạng thái Chờ KT duyệt.\n'
     '– Kiểm tra người dùng có quyền Kế toán duyệt hàng giữ và cùng công ty với yêu cầu.\n'
     '– Nếu không → báo “Yêu cầu này không ở bước Kế toán xử lý, hoặc bạn không đủ quyền lập '
     'phiếu xuất giữ.”.\n'
     'During:\n– Nạp các dòng hàng ĐÃ ĐƯỢC TÍCH Cần xuất của yêu cầu nguồn.\n'
     '– Tính SL có thể giữ theo tồn kho khả dụng của công ty yêu cầu.\n'
     'After:\n– Điền sẵn khách hàng, hợp đồng, người yêu cầu, phòng yêu cầu và Giữ đến ngày.'),
    ('Bỏ tích một dòng ở cột Cần xuất', 'Change',
     'After:\n– Dòng bị làm mờ, ô SL xuất giữ khóa lại và dòng sẽ được lưu với số lượng 0.'),
    ('Nhập SL xuất giữ', 'Change / Blur',
     'During:\n– Chỉ nhận ký tự số.\n'
     '– Bằng 0 mà dòng vẫn tích Cần xuất → báo “Phải lớn hơn 0.”.\n'
     '– Vượt SL yêu cầu → báo “Vượt số lượng đề nghị của yêu cầu (…).”.\n'
     'After:\n– Giữ nguyên giá trị người dùng đã gõ, không tự kéo về mức trần.'),
    ('Bấm Lưu nháp hoặc Không duyệt', 'Click',
     'During:\n– Kiểm tra Giữ đến ngày và các dòng hàng.\n'
     '– KHÔNG kiểm tra tồn kho ở bước này.\n'
     'After:\n– Sinh mã phiếu dạng PXG-NNNNN, ghi phiếu ở trạng thái Đang tạo.\n'
     '– Chuyển yêu cầu nguồn sang trạng thái Đang xuất giữ.\n'
     '– Ghi một dòng lịch sử “Tạo mới” cho phiếu và một dòng lịch sử cho yêu cầu nguồn.'),
    ('Bấm Duyệt giữ hàng', 'Click',
     'Before:\n– Hiển thị hộp thoại “Xác nhận duyệt giữ hàng” nêu rõ thao tác không hoàn tác '
     'được; người dùng hủy thì không làm gì.\n'
     'During:\n– Kiểm tra đủ như khi lưu nháp.\n'
     '– Kiểm tra thêm tồn kho khả dụng của từng dòng; thiếu thì báo “Kho không đủ số lượng '
     '(còn …).” và không lưu.\n'
     'After:\n– Ghi tồn hàng giữ cho người yêu cầu (xem chi tiết ở mục 2.8).\n'
     '– Đóng dấu người duyệt và thời điểm duyệt lên phiếu.\n'
     '– Chuyển yêu cầu nguồn sang trạng thái Đã duyệt.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.6
d.h3('2.6 Chỉnh sửa phiếu nháp')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Chỉnh sửa phiếu xuất giữ còn nháp', 'crud',
            [('include', 'Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo'),
             ('extend', 'Duyệt giữ hàng ngay tại màn sửa')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-06 Chỉnh sửa phiếu nháp')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Chỉnh sửa phiếu xuất giữ còn nháp',
    mota='Sửa lại số lượng, hạn giữ, ghi chú và tệp đính kèm của phiếu còn nháp, rồi lưu tiếp '
         'hoặc duyệt giữ hàng.',
    tacnhan='Kế toán — người lập phiếu',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.',
    chinh='1. Người dùng bấm nút Sửa ở màn danh sách hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở màn sửa với dữ liệu đã lưu của phiếu.\n'
          '3. Người dùng chỉnh sửa số lượng, hạn giữ, ghi chú, tệp đính kèm.\n'
          '4. Người dùng bấm Lưu nháp hoặc Duyệt giữ hàng.',
    phu='• Phiếu đã duyệt → nút Sửa không hiển thị; mở thẳng bằng đường dẫn thì hệ thống từ '
        'chối và báo không có quyền xem hoặc sửa phiếu này.\n'
        '• Phiếu của người khác → hệ thống từ chối, trừ người có vai trò quản trị hệ thống.\n'
        '• Không đổi được yêu cầu nguồn và danh sách hàng hóa.\n'
        '• Các nhánh lỗi nhập liệu giống chức năng Lập phiếu.',
    dacbiet='Phiếu đã duyệt KHÔNG sửa được trong mọi trường hợp, vì tồn hàng giữ đã được ghi.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('10-sua-phieu.png'),
         shot_caption='Màn sửa phiếu xuất giữ còn nháp')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mã phiếu', 'Textbox', 'Disable', 'PXG-NNNNN', '–', 'Theo dữ liệu',
     'Chỉ hiển thị, không sửa được.'),
    ('Trạng thái', 'Badge', 'Read-only', '–', '–', 'Đang tạo', 'Nhãn màu xám.'),
    ('Yêu cầu xuất giữ', 'Link', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Khóa hẳn; mở yêu cầu nguồn trong tab mới.'),
    ('Giữ đến ngày / Ghi chú / Tệp đính kèm', 'Datepicker, Textbox, Button', 'Enable', '–', '–',
     'Theo dữ liệu', 'Ba nhóm thông tin sửa được ở màn này.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu đã lưu',
     'Sửa được ô tích Cần xuất và SL xuất giữ; không thêm hay xóa dòng.'),
    ('Nút Lưu nháp / Duyệt giữ hàng / Không duyệt / Quay lại', 'Button', 'Enable', '–', '–',
     'Hiển thị', 'Cùng bộ nút với màn lập phiếu.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System',
     'Before:\n– Kiểm tra phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.\n'
     '– Nếu không → hệ thống từ chối và không mở màn sửa.\n'
     'After:\n– Nạp dữ liệu phiếu cùng số tồn kho khả dụng mới nhất của từng dòng.'),
    ('Bấm Lưu nháp', 'Click',
     'After:\n– Ghi lại phiếu, giữ trạng thái Đang tạo.\n'
     '– Ghi một dòng lịch sử “Chỉnh sửa”, nêu rõ những giá trị đã thay đổi.'),
    ('Bấm Duyệt giữ hàng', 'Click',
     'After:\n– Xử lý giống như duyệt ở màn lập phiếu: kiểm tồn kho, ghi tồn hàng giữ và đưa '
     'yêu cầu nguồn sang Đã duyệt.'),
])

# ------------------------------------------------------------ 2.7
d.h3('2.7 Xem chi tiết phiếu')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu xuất giữ',
    mota='Hiển thị toàn bộ thông tin phiếu ở chế độ chỉ đọc: thông tin chung, tệp đính kèm, '
         'bảng hàng hóa và lịch sử thay đổi.',
    tacnhan='Kế toán; Người dùng có quyền xem theo cấp',
    dieukien='Người dùng nằm trong phạm vi được xem phiếu.',
    chinh='1. Người dùng bấm vào mã phiếu ở màn danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống hiển thị màn chi tiết ở chế độ chỉ đọc.\n'
          '4. Các nút thao tác ở cuối màn hiện theo đúng quyền và trạng thái của phiếu.',
    phu='• Không đủ quyền xem → hệ thống báo không có quyền xem phiếu này.\n'
        '• Phiếu Đang tạo của người khác → không mở được.\n'
        '• Phiếu đã duyệt hiện thêm cột SL giữ (ĐV cơ bản) và dòng giải thích ý nghĩa cột đó.',
    dacbiet='Cột SL giữ (ĐV cơ bản) là con số đã cộng thật vào tồn hàng giữ. Khi đối chiếu với '
            'màn Lịch sử giữ hàng phải nhìn cột này, không nhìn cột SL xuất giữ.')

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('07-chi-tiet.png'),
         shot_caption='Màn chi tiết phiếu đã duyệt, ở chế độ chỉ đọc')

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu xuất giữ: <mã phiếu>', '–'),
    ('Khối Thông tin chung', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm Mã phiếu, Trạng thái, Yêu cầu xuất giữ, Loại yêu cầu, Hợp đồng, Người yêu cầu, '
     'Phòng yêu cầu, Giữ đến ngày, Khách hàng, Địa chỉ và Ghi chú.'),
    ('Khối File đính kèm', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Danh sách tệp mở xem được; không có tệp thì hiện “Chưa có tệp đính kèm”.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cột STT, Cần xuất, Tên hàng hóa, Mã hàng hóa, Model, Thương hiệu, SL có thể giữ, '
     'SL yêu cầu, SL xuất giữ, ĐVT và SL giữ (ĐV cơ bản), kèm dòng Tổng cộng.'),
    ('Dòng chú thích cột SL giữ', 'Label', 'Read-only', '–', 'Ẩn',
     'Chỉ hiện với phiếu đã duyệt; nhắc đối chiếu Lịch sử giữ hàng theo cột này.'),
    ('Khối Lịch sử thay đổi', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Chỉ nạp dữ liệu khi người dùng bấm Xem lịch sử.'),
    ('Nút thao tác cuối màn', 'Button', 'Enable / Ẩn', '–', 'Theo quyền và trạng thái',
     'Gồm Sửa, Xóa, In và Quay lại; nút không dùng được thì ẩn hẳn.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu theo phạm vi dữ liệu và quyền Kế toán.\n'
     '– Không đủ quyền → báo không có quyền xem phiếu này.\n'
     'After:\n– Hiển thị dữ liệu phiếu và các nút thao tác hợp lệ.'),
    ('Bấm vào mã yêu cầu xuất giữ', 'Click',
     'After:\n– Mở màn chi tiết của yêu cầu nguồn trong tab mới.'),
    ('Bấm Xem lịch sử ở khối Lịch sử thay đổi', 'Click',
     'After:\n– Nạp và hiển thị danh sách mốc thay đổi của phiếu, mới nhất trước.'),
])

# ------------------------------------------------------------ 2.8
d.h3('2.8 Duyệt giữ hàng')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Duyệt giữ hàng', 'action',
            [('include', 'Kiểm tra tồn kho khả dụng của từng dòng'),
             ('include', 'Quy đổi số lượng về đơn vị cơ bản'),
             ('include', 'Ghi tồn hàng giữ cho người yêu cầu'),
             ('extend', 'Đóng dấu duyệt lên yêu cầu nguồn')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-08 Duyệt giữ hàng')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Duyệt giữ hàng — bước ghi tồn hàng giữ',
    mota='Bước quan trọng nhất của toàn nghiệp vụ giữ hàng: hệ thống cộng số lượng vào tồn hàng '
         'giữ và sinh ra lô hàng giữ mà các màn Danh sách hàng giữ, Gia hạn, Hủy, Điều chuyển '
         'sẽ dùng.',
    tacnhan='Kế toán — người lập phiếu',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.',
    chinh='1. Kế toán mở màn lập hoặc màn sửa phiếu.\n'
          '2. Kế toán rà lại từng dòng: ô tích Cần xuất, SL xuất giữ và Giữ đến ngày.\n'
          '3. Kế toán bấm Duyệt giữ hàng.\n'
          '4. Hệ thống hỏi xác nhận, nêu rõ thao tác không hoàn tác được.\n'
          '5. Hệ thống kiểm tra tồn kho khả dụng của từng dòng.\n'
          '6. Hệ thống quy đổi số lượng về đơn vị cơ bản rồi cộng vào tồn hàng giữ.\n'
          '7. Hệ thống đóng dấu duyệt lên phiếu và đưa yêu cầu nguồn sang Đã duyệt.',
    phu='• Người dùng hủy ở hộp thoại xác nhận → không làm gì.\n'
        '• Tồn kho không đủ ở bất kỳ dòng nào → báo lỗi tại dòng và KHÔNG ghi gì cả.\n'
        '• Không tích dòng nào → báo “Chưa chọn hàng hoá nào cần xuất giữ, hoặc số lượng đều '
        'bằng 0.”.',
    dacbiet='⚠ Chủ lô hàng giữ là NGƯỜI LẬP YÊU CẦU, không phải Kế toán bấm duyệt. Công ty của '
            'lô cũng lấy theo yêu cầu nguồn. Hạn giữ lấy theo ô Giữ đến ngày trên chính phiếu '
            'xuất giữ này.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Lập từ yêu cầu => Duyệt giữ hàng', shot=shot('03-lap-phieu.png'),
         shot_caption='Nút Duyệt giữ hàng nằm ở cuối màn lập phiếu')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Duyệt giữ hàng', 'Button', 'Enable', '–', 'Hiển thị',
     'Chú thích khi rê chuột: “Duyệt và ghi tồn hàng giữ cho người yêu cầu”.'),
    ('Hộp thoại xác nhận', 'Modal', 'Hiển thị', '–', 'Ẩn',
     'Tiêu đề “Xác nhận duyệt giữ hàng”; nội dung nêu rõ thao tác sẽ ghi tồn hàng giữ và không '
     'hoàn tác được. Nút xác nhận ghi “Duyệt giữ hàng”.'),
    ('Ô Giữ đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Theo yêu cầu nguồn',
     'Giá trị tại thời điểm bấm duyệt chính là hạn giữ ghi vào lô hàng.'),
    ('Cột SL giữ (ĐV cơ bản)', 'Table/Grid', 'Read-only', '–', 'Ẩn',
     'Chỉ hiện ở màn chi tiết sau khi phiếu đã duyệt; là con số đã cộng vào tồn hàng giữ.'),
], required=False)

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Duyệt giữ hàng', 'Click',
     'Before:\n– Hiển thị hộp thoại xác nhận; hủy thì dừng ngay.\n'
     'During:\n– Kiểm tra Giữ đến ngày: bắt buộc, hợp lệ và là ngày tương lai.\n'
     '– Kiểm tra từng dòng có tích Cần xuất: số lượng lớn hơn 0 và không vượt SL yêu cầu.\n'
     '– Kiểm tra tồn kho khả dụng, tính bằng tồn kho trừ hàng khuyến mại, so với số lượng đã '
     'quy đổi về đơn vị cơ bản; thiếu thì báo “Kho không đủ số lượng (còn …).”.\n'
     '– Có bất kỳ lỗi nào thì KHÔNG thực hiện bước After.\n'
     'After:\n– Với mỗi dòng cần xuất: quy đổi số lượng về đơn vị cơ bản, ghi lại con số quy '
     'đổi vào cột SL giữ (ĐV cơ bản).\n'
     '– Tìm lô hàng giữ khớp đúng bộ hàng hóa – người yêu cầu – khách hàng – hạn giữ – công ty; '
     'chưa có thì tạo lô mới.\n'
     '– Cộng số lượng vào lô và ghi một dòng nhật ký biến động của lô.\n'
     '– Đóng dấu người duyệt, thời điểm duyệt lên phiếu; phiếu chuyển sang Đã duyệt.\n'
     '– Đưa yêu cầu nguồn sang Đã duyệt, ghi người duyệt và thời điểm duyệt lên yêu cầu.\n'
     '– Ghi lịch sử cho cả phiếu và yêu cầu nguồn, nêu rõ số lô đã ghi.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.9
d.h3('2.9 Xóa phiếu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Xóa phiếu xuất giữ còn nháp', 'action',
            [('include', 'Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo'),
             ('extend', 'Đưa yêu cầu nguồn về lại bước Kế toán xử lý')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-09 Xóa phiếu')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa và Thông báo.', anchor='delete')
d.intro_table(
    ten='Xóa phiếu xuất giữ còn nháp',
    mota='Xóa hẳn một phiếu đang ở trạng thái Đang tạo do chính người dùng lập. Yêu cầu nguồn '
         'quay lại bước Kế toán xử lý để lập phiếu khác.',
    tacnhan='Kế toán — người lập phiếu',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.',
    chinh='1. Người dùng bấm nút Xóa ở cột Hành động hoặc ở màn chi tiết.\n'
          '2. Hệ thống hiển thị hộp thoại xác nhận kèm mã phiếu.\n'
          '3. Người dùng chọn Xóa.\n'
          '4. Hệ thống xóa phiếu, đưa yêu cầu nguồn về Chờ KT duyệt và nạp lại danh sách.',
    phu='• Chọn Hủy → đóng hộp thoại, không xóa gì.\n'
        '• Phiếu đã duyệt → nút Xóa không hiển thị; gọi thẳng chức năng xóa thì hệ thống báo '
        '“Không thể xóa phiếu này.”.',
    dacbiet='Phiếu đã duyệt KHÔNG xóa được, vì xóa sẽ mất dấu vết của lô hàng giữ đã sinh ra.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('11-xac-nhan-xoa.png'),
         shot_caption='Hộp thoại Xác nhận xóa phiếu, mở ngay trên màn danh sách')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Tiêu đề cố định.'),
    ('Nội dung hỏi ở màn danh sách', 'Label', 'Hiển thị',
     'Bạn có chắc muốn xóa phiếu <mã phiếu>?', 'Có nêu rõ mã phiếu để tránh xóa nhầm.'),
    ('Nội dung hỏi ở màn chi tiết', 'Label', 'Hiển thị',
     'Xóa phiếu <mã phiếu>? Yêu cầu xuất giữ sẽ quay lại bước Kế toán xử lý.',
     'Nói rõ hệ quả với yêu cầu nguồn.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Nút nhóm nguy hiểm, màu đỏ.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không thực hiện gì.'),
], required=False, scope=False)

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa', 'Click',
     'Before:\n– Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo.\n'
     '– Nếu không → nút không hiển thị; gọi thẳng chức năng thì hệ thống từ chối.\n'
     'After:\n– Mở hộp thoại xác nhận.'),
    ('Xác nhận Xóa', 'Click',
     'After:\n– Xóa phiếu cùng các dòng hàng của phiếu; lịch sử thay đổi được giữ lại.\n'
     '– Nếu yêu cầu nguồn đang ở Đang xuất giữ thì đưa về Chờ KT duyệt và ghi một dòng lịch sử '
     'cho yêu cầu.\n'
     '– ⚠ Tồn hàng giữ không thay đổi, vì phiếu nháp chưa từng ghi tồn.\n'
     '– Hiển thị thông báo “Xóa thành công.” và nạp lại danh sách.'),
])

# ------------------------------------------------------------ 2.10
d.h3('2.10 In phiếu và In danh sách')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'In phiếu và In danh sách', 'io',
            [('extend', 'In một phiếu'),
             ('extend', 'In danh sách theo bộ lọc đang áp')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-10 In phiếu và In danh sách')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc màn In và Xuất dữ liệu.', anchor='excel')
d.intro_table(
    ten='In phiếu xuất giữ và in danh sách',
    mota='Mở cửa sổ xem trước để in một phiếu, hoặc in toàn bộ danh sách theo đúng bộ lọc '
         'đang áp dụng.',
    tacnhan='Kế toán; Người dùng có quyền xem theo cấp',
    dieukien='Với bản in phiếu: người dùng xem được phiếu đó.',
    chinh='1. Người dùng bấm nút In ở cột Hành động, ở màn chi tiết, hoặc nút In ở thanh công '
          'cụ danh sách.\n'
          '2. Hệ thống mở cửa sổ xem trước ngay trên màn đang đứng.\n'
          '3. Người dùng bấm nút In trên cửa sổ xem trước để gửi lệnh in.',
    phu='• Bản in danh sách dùng khổ A4 ngang.\n'
        '• Bản in danh sách in đúng phạm vi và điều kiện lọc đang áp.\n'
        '• Phiếu chưa duyệt thì bảng Thông tin duyệt trên bản in để TRỐNG.',
    dacbiet='Phần đầu bản in lấy theo công ty ghi trên phiếu, tức công ty của người yêu cầu, '
            'không lấy theo người đang in.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In', shot=shot('09-in-phieu.png'),
         shot_caption='Cửa sổ Xem trước phiếu xuất giữ')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In trên cửa sổ xem trước', 'Button', 'Enable', '–', 'Hiển thị',
     'Nằm cạnh tiêu đề cửa sổ.'),
    ('Phần đầu chứng từ', 'Label', 'Read-only', '–', 'Theo công ty của phiếu',
     'Gồm logo và thông tin liên hệ của công ty ghi trên phiếu.'),
    ('Khối thông tin phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Yêu cầu xuất giữ, loại yêu cầu, hợp đồng, người yêu cầu, phòng yêu cầu, khách hàng, '
     'địa chỉ, giữ đến ngày và trạng thái.'),
    ('Bảng hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cột hàng hóa, SL xuất giữ, SL giữ theo đơn vị cơ bản và dòng Tổng cộng.'),
    ('Bảng Thông tin duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người duyệt và thời gian duyệt; để trống khi phiếu chưa duyệt.'),
    ('Khối ký tên', 'Label', 'Read-only', '–', 'Hiển thị',
     'Hai ô ký: Người lập và Kế toán duyệt, kèm dòng ngày tháng năm.'),
    ('Bản in danh sách', 'Table/Grid', 'Read-only', '–', 'Theo bộ lọc',
     'Khổ A4 ngang, có dòng tổng số phiếu và các cột chính của màn danh sách.'),
], required=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In ở dòng hoặc ở màn chi tiết', 'Click',
     'After:\n– Mở cửa sổ xem trước bản in của đúng phiếu đó.'),
    ('Bấm nút In ở thanh công cụ danh sách', 'Click',
     'After:\n– Mở cửa sổ xem trước bản in danh sách theo đúng bộ lọc đang áp, khổ ngang.'),
])

# ------------------------------------------------------------ 2.11
d.h3('2.11 Xuất Excel danh sách')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xuất Excel danh sách phiếu', 'io',
            [('include', 'Chọn trường cần xuất'),
             ('include', 'Lấy dữ liệu theo bộ lọc đang áp')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-11 Xuất Excel danh sách')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách phiếu xuất giữ',
    mota='Xuất danh sách phiếu ra tệp Excel. Người dùng tự chọn các trường cần xuất và thứ tự '
         'cột trong tệp chạy theo đúng thứ tự đã chọn.',
    tacnhan='Kế toán; Người dùng có quyền xem theo cấp',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ Chọn trường xuất Excel với 14 trường, mặc định chọn hết.\n'
          '3. Người dùng bỏ chọn các trường không cần.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống lấy toàn bộ dữ liệu khớp bộ lọc và tải tệp về máy.',
    phu='• Trong lúc đang xuất, nút bị khóa để tránh bấm nhiều lần.\n'
        '• Xuất thất bại → hiển thị thông báo lỗi, không tải tệp.',
    dacbiet='Tệp xuất chứa toàn bộ dòng khớp bộ lọc trong phạm vi quyền, không giới hạn ở trang '
            'đang xem.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('06-chon-truong-xuat-excel.png'),
         shot_caption='Cửa sổ Chọn trường xuất Excel')

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất Excel', '–'),
    ('Ô chọn trường xuất', 'Dropdown', 'Enable', '14 trường', 'Có', 'Chọn hết 14 trường',
     'Mã phiếu, Yêu cầu xuất giữ, Người yêu cầu, Phòng yêu cầu, Người tạo, Ngày tạo, '
     'Khách hàng, Giữ đến ngày, Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, '
     'Ngày cập nhật, Ghi chú.'),
    ('Dòng xem trước thứ tự cột', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn',
     'Liệt kê thứ tự cột sẽ có trong tệp.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Bị khóa trong lúc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
])

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xuất Excel', 'Click', 'After:\n– Mở cửa sổ chọn trường xuất.'),
    ('Bấm Xuất file', 'Click',
     'During:\n– Lấy dữ liệu theo đúng bộ lọc và phạm vi quyền hiện tại.\n'
     'After:\n– Dựng tệp Excel theo thứ tự trường đã chọn và tải về máy.\n'
     '– Hiển thị thông báo “Xuất Excel thành công” và đóng cửa sổ.'),
])

# ------------------------------------------------------------ 2.12
d.h3('2.12 Xem lịch sử thay đổi')

d.p('2.12.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Hiển thị các mốc thao tác đã thực hiện trên phiếu: tạo phiếu, chỉnh sửa, duyệt giữ '
         'hàng, kèm người thực hiện, thời điểm và nội dung thay đổi.',
    tacnhan='Kế toán; Người dùng có quyền xem theo cấp',
    dieukien='Người dùng xem được phiếu.',
    chinh='1. Người dùng bấm biểu tượng Lịch sử ở cột Hành động, hoặc bấm Xem lịch sử ở khối '
          'Lịch sử thay đổi trong màn chi tiết.\n'
          '2. Hệ thống nạp danh sách mốc thay đổi của phiếu.\n'
          '3. Danh sách hiển thị theo thứ tự mới nhất trước.',
    phu='• Phiếu chưa có thao tác nào được ghi nhận → hiện dòng “Chưa có lịch sử thao tác nào.”.\n'
        '• Bấm Làm mới → nạp lại danh sách.',
    dacbiet='Mốc “Duyệt giữ hàng” ghi rõ số lô hàng giữ đã được ghi tồn, ví dụ “Đã ghi tồn giữ '
            'cho 1 lô hàng.”.')

d.p('2.12.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Xem lịch sử', shot=shot('08-lich-su-thay-doi.png'),
         shot_caption='Khối Lịch sử thay đổi ở cuối màn chi tiết')

d.p('2.12.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề khối', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi',
     'Kèm số mốc thay đổi khi đã nạp dữ liệu.'),
    ('Nút Xem lịch sử / Thu gọn', 'Button', 'Enable', '–', 'Thu gọn',
     'Chỉ nạp dữ liệu ở lần bấm mở đầu tiên.'),
    ('Nút Làm mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Chỉ hiện khi khối đang mở.'),
    ('Danh sách mốc thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi mốc gồm nhóm thao tác, người thực hiện, thời điểm và chi tiết giá trị thay đổi.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện dòng “Chưa có lịch sử thao tác nào.”.'),
], required=False)

d.p('2.12.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem lịch sử', 'Click',
     'After:\n– Nạp danh sách mốc thay đổi và hiển thị, mới nhất trước.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Nạp lại danh sách mốc thay đổi.'),
])

# ==================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu xuất giữ; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Phiếu xuất giữ là chứng từ DUY NHẤT ghi tồn hàng giữ', [
        '– Không có màn nào khác trong hệ thống sinh ra lô hàng giữ mới.',
        '– Các màn Danh sách hàng giữ, Gia hạn, Hủy và Điều chuyển đều tiêu thụ lô do màn này '
        'sinh ra.',
        '– Chỉ bước Duyệt giữ hàng mới ghi tồn; lưu nháp không đụng tới tồn hàng giữ.',
    ], 'Toàn màn hình'),
    ('BR-02', 'Phiếu luôn thuộc về một yêu cầu xuất giữ', [
        '– Không lập được phiếu nếu không đi từ một yêu cầu đang ở trạng thái Chờ KT duyệt.',
        '– Một yêu cầu chỉ có tối đa một phiếu xuất giữ.',
        '– Yêu cầu nguồn và danh sách hàng hóa không đổi được sau khi phiếu đã lập.',
        '– Nút Lập từ yêu cầu ở thanh công cụ chỉ điều hướng sang màn Yêu cầu xuất giữ.',
    ], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-03', 'Ba trạng thái và tác động lên yêu cầu nguồn', [
        '– Đang tạo (nháp): yêu cầu nguồn chuyển sang Đang xuất giữ.',
        '– Đã duyệt: tồn hàng giữ đã ghi, yêu cầu nguồn chuyển sang Đã duyệt.',
        '– Phiếu nháp bị xóa: yêu cầu nguồn quay lại Chờ KT duyệt.',
        '– Trạng thái Chờ duyệt chỉ còn tồn tại ở dữ liệu cũ; hệ thống không sinh trạng thái này '
        'nữa.',
    ], 'Toàn màn hình'),
    ('BR-04', 'Tổ chức của phiếu lấy theo người lập YÊU CẦU', [
        '– Công ty, phòng ban và bộ phận của phiếu chép từ người lập yêu cầu, không lấy theo '
        'Kế toán lập phiếu.',
        '– Vì vậy phạm vi dữ liệu, bản in và thống kê của phiếu đều chạy theo tổ chức bên yêu '
        'cầu.',
        '– Chủ lô hàng giữ sinh ra cũng là người lập yêu cầu.',
    ], 'Toàn màn hình'),
    ('BR-05', 'Số lượng xuất giữ', [
        '– Phải lớn hơn 0 với mọi dòng có tích Cần xuất.',
        '– Không vượt quá SL yêu cầu của chính dòng đó trên yêu cầu nguồn.',
        '– Phải có ít nhất một dòng tích Cần xuất với số lượng lớn hơn 0.',
        '– Dòng không tích Cần xuất vẫn được lưu với số lượng 0.',
        '– Nhập sai thì hệ thống báo đỏ ngay tại dòng và giữ nguyên giá trị đã gõ.',
    ], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-06', 'Kiểm tra tồn kho chỉ khi duyệt', [
        '– Lưu nháp: KHÔNG kiểm tra tồn kho, để Kế toán lưu lại làm tiếp.',
        '– Duyệt giữ hàng: từng dòng phải có tồn kho khả dụng đủ cho số lượng đã quy đổi về đơn '
        'vị cơ bản.',
        '– Tồn kho khả dụng là tồn kho trừ đi phần hàng khuyến mại.',
        '– Thiếu ở bất kỳ dòng nào thì hệ thống KHÔNG ghi gì cả, báo lỗi tại đúng dòng.',
    ], ['Lập phiếu', 'Chỉnh sửa', 'Duyệt giữ hàng']),
    ('BR-07', 'Cách ghi tồn hàng giữ khi duyệt', [
        '– Số lượng được quy đổi về đơn vị cơ bản theo hệ số của đơn vị tính trên dòng.',
        '– Hệ thống tìm lô hàng giữ khớp đúng bộ: hàng hóa – người yêu cầu – khách hàng – hạn '
        'giữ – công ty; chưa có thì tạo lô mới.',
        '– Cộng số lượng vào lô và ghi một dòng nhật ký biến động kèm số trước, số thay đổi và '
        'số sau.',
        '– Hạn giữ của lô lấy theo ô Giữ đến ngày trên phiếu xuất giữ tại thời điểm duyệt.',
        '– Con số đã cộng được ghi lại ở cột SL giữ (ĐV cơ bản) của màn chi tiết.',
    ], 'Duyệt giữ hàng'),
    ('BR-08', 'Giữ đến ngày trên phiếu', [
        '– Bắt buộc nhập khi duyệt giữ hàng; phải hợp lệ và là ngày tương lai.',
        '– Điền sẵn theo yêu cầu nguồn, tức hạn giữ mà Ban giám đốc đã chốt ở bước duyệt của họ.',
        '– Kế toán sửa lại được trước khi duyệt.',
    ], ['Lập phiếu', 'Chỉnh sửa', 'Duyệt giữ hàng']),
    ('BR-09', 'Nút Không duyệt KHÔNG trả phiếu về cho người lập yêu cầu', [
        '– Nút này lưu phiếu ở trạng thái Đang tạo, giống hệt nút Lưu nháp.',
        '– Muốn trả yêu cầu về cho người lập thì phải sang màn Yêu cầu xuất giữ và bấm Từ chối.',
        '– Đây là điểm dễ hiểu nhầm nhất của màn hình, cần nêu rõ khi đào tạo người dùng.',
    ], ['Lập phiếu', 'Chỉnh sửa']),
    ('BR-10', 'Sửa và xóa phiếu', [
        '– Chỉ sửa hoặc xóa được phiếu do chính mình lập và đang ở trạng thái Đang tạo.',
        '– Người có vai trò quản trị hệ thống được sửa, xóa phiếu nháp của người khác.',
        '– Phiếu đã duyệt KHÔNG sửa và KHÔNG xóa được trong mọi trường hợp.',
        '– Nút không dùng được thì ẩn hẳn, không để ở trạng thái mờ.',
        '– Xóa phiếu thì các dòng hàng bị xóa theo, lịch sử thay đổi được giữ lại.',
    ], ['Chỉnh sửa', 'Xóa']),
    ('BR-11', 'Phạm vi dữ liệu', [
        '– Áp theo thứ tự ưu tiên: tổng công ty → công ty → phòng ban → chỉ phiếu của mình.',
        '– Người có quyền Kế toán duyệt hàng giữ được xem thêm mọi phiếu trong công ty mình.',
        '– Phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy.',
        '– Màn danh sách và màn chi tiết dùng cùng một bộ điều kiện.',
        '– Phạm vi này áp cho cả danh sách, màn chi tiết, bản in và tệp Excel xuất ra.',
    ], 'Toàn màn hình'),
    ('BR-12', 'Tệp đính kèm', [
        '– Nhận các định dạng PDF, ảnh, Word, Excel.',
        '– Mỗi tệp tối đa 13 MB; đính kèm được nhiều tệp trên một phiếu.',
        '– Không bắt buộc với mọi loại yêu cầu nguồn.',
    ], ['Lập phiếu', 'Chỉnh sửa']),
])

d.save()
