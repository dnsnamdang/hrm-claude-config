# -*- coding: utf-8 -*-
"""Sinh SRS man "Yeu cau xuat giu" (PYCXG) theo FORM CHUAN 2026-08-28.

Nguon: code HRM nhanh `gop_db`
  BE  Modules/Finance/{Entities/PrepickExport/ProductPrepickRequest.php,
      Services/ProductPrepickRequestService.php, Services/PrepickExportContractService.php,
      Http/Controllers/V1/ProductPrepickRequestController.php,
      Http/Requests/PrepickExport/ProductPrepickRequest*Request.php}
  FE  pages/finance/product-prepick-requests/*
Anh chup that: ./product_prepick_shots (Playwright MCP, 1440x900, ngay 18/09/2026).
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

SHOTS = os.path.join(BASE, 'product_prepick_shots')
OUT = os.path.join(BASE, 'SRS - Yeu cau xuat giu.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Giữ hàng => Yêu cầu xuất giữ'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/product-prepick-requests',
           full_url='https://<host-hrm>/finance/product-prepick-requests',
           img_prefix='ycxg_')

# ============================================================== TRANG DAU
d.title_block('Yêu cầu xuất giữ')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Yêu cầu xuất giữ (mã phiếu PYCXG), '
    'nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, luồng duyệt và phân quyền của màn hình.',
    'Làm rõ bản chất nghiệp vụ: nhân viên kinh doanh đề nghị giữ hàng trong kho cho một khách '
    'hàng tới một hạn nhất định.',
    'Làm rõ điểm dễ hiểu nhầm nhất của màn hình: yêu cầu này KHÔNG ghi tồn hàng giữ. Hàng chỉ '
    'thực sự được giữ khi Kế toán lập Phiếu xuất giữ và duyệt phiếu đó.',
    'Làm rõ sáu loại yêu cầu và hai kiểu form khác hẳn nhau: loại lấy hàng theo hợp đồng và '
    'loại tự thêm hàng bằng tay.',
    'Làm rõ luồng duyệt ba cấp, cách phiếu bị trả về và cách người lập gửi lại.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hàng giữ', 'Số lượng hàng hóa trong kho được giữ lại cho một khách hàng cụ thể, do một '
                 'nhân viên kinh doanh đứng tên giữ, tới một hạn nhất định.'),
    ('Yêu cầu xuất giữ', 'Phiếu đề nghị giữ hàng, mã PYCXG. Là phiếu ĐỀ NGHỊ, chưa ghi tồn '
                         'hàng giữ.'),
    ('Phiếu xuất giữ', 'Phiếu do Kế toán lập từ một yêu cầu đã qua đủ các cấp duyệt, mã PXG. '
                       'Đây mới là chứng từ ghi tồn hàng giữ.'),
    ('Loại yêu cầu', 'Sáu loại: Xuất giữ thường, Xuất giữ khuyến mại, Xuất giữ HĐDV, '
                     'Xuất giữ HĐDA, Xuất giữ HĐ hãng và Xuất giữ khác.'),
    ('Xuất giữ khác', 'Loại yêu cầu KHÔNG gắn hợp đồng; người lập tự chọn khách hàng và tự thêm '
                      'từng dòng hàng hóa.'),
    ('Giữ đến ngày', 'Hạn giữ hàng đề nghị. Bắt buộc, phải là ngày tương lai và không vượt trần '
                     'cấu hình của hệ thống.'),
    ('SL Có thể giữ', 'Tồn kho khả dụng của hàng hóa, đã trừ phần hàng khuyến mại. Là con số '
                      'tham khảo khi nhập số lượng đề nghị.'),
    ('SL Đề nghị', 'Số lượng người lập xin giữ cho từng dòng hàng.'),
    ('Cần xuất', 'Ô tích đánh dấu dòng hàng thực sự được xin giữ. Dòng không tích được lưu với '
                 'số lượng 0.'),
    ('TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán — ba cấp xử lý của phiếu.'),
    ('Đang tạo', 'Trạng thái nháp. Cũng là trạng thái phiếu quay về sau khi bị một cấp trả lại, '
                 'kèm lý do ở ô Lý do từ chối gần nhất.'),
    ('Đang xuất giữ', 'Kế toán đã lập Phiếu xuất giữ nhưng còn để ở dạng nháp, chưa duyệt.'),
], widths=[1.6, 4.4])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Màn hình KHÔNG có quyền riêng cho Thêm / Sửa / Xóa: mọi người dùng đã đăng nhập đều lập '
    'được yêu cầu xuất giữ, và chỉ sửa / xóa được phiếu do chính mình lập khi phiếu đang ở '
    'trạng thái Đang tạo.')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Trưởng phòng duyệt hàng giữ',
     'Nút TP duyệt và Từ chối với phiếu đang ở trạng thái Chờ TP duyệt. Ngoài quyền còn phải '
     'cùng công ty với phiếu và quản lý phòng ban ghi trên phiếu.'),
    ('Q2', 'Ban giám đốc duyệt hàng giữ',
     'Nút BGĐ duyệt và Từ chối với phiếu đang ở trạng thái Chờ BGĐ duyệt. Bước này cho phép '
     'nhập lại Giữ đến ngày.'),
    ('Q3', 'Kế toán duyệt hàng giữ',
     'Nút Lập phiếu xuất giữ và Từ chối với phiếu đang ở trạng thái Chờ KT duyệt. Ở màn này Kế '
     'toán KHÔNG có nút duyệt riêng.'),
], widths=[0.8, 2.0, 3.2])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu hàng giữ theo tổng công ty', 'Toàn bộ phiếu của mọi công ty.'),
    ('V2', 'Xem phiếu hàng giữ theo công ty', 'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem phiếu hàng giữ theo phòng ban',
     'Phiếu thuộc các phòng ban mà người đăng nhập được phân công quản lý, cộng phòng ban của '
     'chính người đó, cộng phiếu do chính người đó lập.'),
    ('—', '(không có cấp nào)',
     'Chỉ phiếu do chính mình lập, cộng thêm những phiếu đang chờ chính mình xử lý.'),
], widths=[0.8, 2.0, 3.2])

d.p('Bốn quy tắc chung áp cho mọi cấp:')
d.bullets([
    'Phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy, kể cả với người có quyền xem rộng nhất.',
    'Người có quyền xử lý luôn nhìn thấy những phiếu đang chờ chính mình, dù không có quyền xem '
    'theo cấp: Trưởng phòng thấy phiếu Chờ TP duyệt thuộc phòng mình quản lý, Ban giám đốc thấy '
    'phiếu Chờ BGĐ duyệt, Kế toán thấy phiếu Chờ KT duyệt và Đang xuất giữ.',
    'Mọi thao tác duyệt / từ chối / lập phiếu xuất giữ đều yêu cầu người thực hiện cùng công ty '
    'với phiếu.',
    'Màn danh sách và màn chi tiết dùng CÙNG một bộ điều kiện: nhìn thấy phiếu trong danh sách '
    'thì mở được chi tiết, và ngược lại.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'V1/V2/V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅', '✅', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột hiển thị', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo mới phiếu', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Chỉnh sửa phiếu', '✅ (phiếu của mình, Đang tạo)', '✅ (nt)', '✅ (nt)', '✅ (nt)',
     '✅ (nt)'),
    ('FR-07 Xem chi tiết phiếu', '✅', '✅', '✅', '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-08 Duyệt phiếu', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '❌ (dùng FR-11)', '❌', '❌'),
    ('FR-09 Từ chối phiếu', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '✅ (Chờ KT duyệt)', '❌',
     '❌'),
    ('FR-10 Xóa phiếu', '✅ (phiếu của mình, Đang tạo)', '✅ (nt)', '✅ (nt)', '✅ (nt)', '✅ (nt)'),
    ('FR-11 Lập phiếu xuất giữ', '❌', '❌', '✅ (Chờ KT duyệt)', '❌', '❌'),
    ('FR-12 In phiếu / In danh sách', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-13 Xuất Excel danh sách', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-14 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
], widths=[1.7, 0.95, 0.95, 0.95, 0.85, 0.9])

# ================================================ PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [('Nhân viên kinh doanh', [0, 1, 2, 3]),
     ('Trưởng phòng / BGĐ / Kế toán', [0, 3])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Tạo mới phiếu', 'crud'),
     ('FR-06', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-07', 'Xem chi tiết phiếu', 'view')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-13', 'Xuất Excel danh sách', 'io', 'extend', [0], None),
     ('FR-10', 'Xóa phiếu', 'action', 'extend', [0], None),
     ('FR-15', 'Chọn hợp đồng', 'crud', 'include', [1, 2], None),
     ('FR-16', 'Chọn hàng hóa và đơn vị tính', 'crud', 'include', [1, 2], None),
     ('FR-08', 'Duyệt phiếu', 'action', 'extend', [3], None),
     ('FR-09', 'Từ chối phiếu', 'action', 'extend', [3], None),
     ('FR-11', 'Lập phiếu xuất giữ', 'action', 'extend', [3], None),
     ('FR-12', 'In phiếu', 'io', 'extend', [3], None),
     ('FR-14', 'Xem lịch sử thay đổi', 'view', 'extend', [3], None)],
    'Sơ đồ Use Case tổng quan màn Yêu cầu xuất giữ')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách phiếu')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Yêu cầu xuất giữ tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách yêu cầu xuất giữ',
    mota='Hiển thị bảng phiếu nằm trong phạm vi dữ liệu của người đăng nhập, kèm bộ lọc, '
         'phân trang và ô thống kê tổng số phiếu khớp bộ lọc.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng vào menu Tài chính → Giữ hàng → Yêu cầu xuất giữ.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem của người dùng.\n'
          '3. Hệ thống bổ sung vào phạm vi những phiếu đang chờ chính người dùng xử lý.\n'
          '4. Hệ thống loại khỏi phạm vi mọi phiếu Đang tạo không phải của người dùng.\n'
          '5. Hệ thống trả về trang đầu tiên của danh sách và tổng số phiếu.\n'
          '6. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Phiếu Đang tạo của người khác không xuất hiện trong danh sách.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet='Kế toán nhìn thấy cả phiếu Chờ KT duyệt lẫn phiếu Đang xuất giữ, vì hai trạng thái '
            'này đều là việc còn dở của họ.')

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Yêu cầu xuất giữ lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Yêu cầu xuất giữ',
     'Tiêu đề cố định phía trên bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Mở màn lập yêu cầu mới.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ xem trước bản in danh sách theo đúng bộ lọc đang áp.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ chọn trường xuất; bị khóa trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục', 'Cột cố định.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PYCXG-NNNNN', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết. Cột cố định, sắp xếp được.'),
    ('Cột Loại yêu cầu', 'Table/Grid', 'Read-only',
     'Xuất giữ thường / khuyến mại / HĐDV / HĐDA / HĐ hãng / khác', 'Theo dữ liệu',
     'Quyết định phiếu có gắn hợp đồng hay không.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Cột Ngày tạo sắp xếp được.'),
    ('Cột Hợp đồng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Số hợp đồng gắn ở đầu phiếu. Loại Xuất giữ khác để trống.'),
    ('Cột Trạng thái', 'Badge', 'Read-only',
     'Đang tạo / Chờ TP duyệt / Chờ BGĐ duyệt / Chờ KT duyệt / Đang xuất giữ / Đã duyệt',
     'Theo dữ liệu',
     'Đang tạo màu xám; bốn trạng thái chờ xử lý màu cam; Đã duyệt màu xanh lá.'),
    ('Cột Người duyệt / Ngày duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là bước duyệt CUỐI cùng — tức là Kế toán. Để trống cho tới khi phiếu Đã duyệt. Cột Ngày '
     'duyệt sắp xếp được.'),
    ('Cột Khách hàng / Giữ đến ngày / Người cập nhật / Ngày cập nhật / Phòng ban / Ghi chú / '
     'Lý do từ chối', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Bật lên trong cửa sổ Tuỳ chỉnh cột. Cột Giữ đến ngày sắp xếp được.'),
    ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Cột cố định cuối bảng, chứa các nút thao tác của dòng.'),
    ('Nút Sửa / Xóa', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện với phiếu do chính mình lập và đang ở trạng thái Đang tạo.'),
    ('Nút Duyệt', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện khi phiếu đang chờ chính người dùng duyệt ở cấp Trưởng phòng hoặc Ban giám đốc; '
     'điều hướng sang màn chi tiết.'),
    ('Nút Lập phiếu xuất giữ', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện với Kế toán đủ điều kiện và phiếu đang ở Chờ KT duyệt.'),
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
     'During:\n– Áp phạm vi dữ liệu; bổ sung các phiếu đang chờ chính người dùng xử lý.\n'
     '– Loại khỏi kết quả mọi phiếu Đang tạo không do người dùng lập.\n'
     '– Khôi phục bộ lọc đã lưu của người dùng nếu còn hiệu lực (10 phút).\n'
     'After:\n– Trả về trang 1, tổng số phiếu và danh sách trạng thái, loại yêu cầu để đổ vào '
     'ô lọc.'),
    ('Bấm vào mã phiếu', 'Click',
     'Before:\n– Kiểm tra người dùng có được xem phiếu này không.\n'
     '– Nếu không → hệ thống báo không có quyền xem phiếu và không mở màn chi tiết.\n'
     'After:\n– Mở màn chi tiết của phiếu.'),
    ('Bấm tiêu đề cột có mũi tên sắp xếp', 'Click',
     'During:\n– Chỉ bốn cột Mã phiếu, Ngày tạo, Ngày duyệt và Giữ đến ngày sắp xếp được.\n'
     'After:\n– Nạp lại danh sách từ trang 1 theo thứ tự mới, giữ nguyên bộ lọc.'),
    ('Bấm số trang / nút tiến lùi / đổi số dòng mỗi trang', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu trang mới; số thứ tự tiếp tục liên tục.'),
])

# ------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách yêu cầu xuất giữ',
    mota='Thu hẹp danh sách theo mã phiếu, loại yêu cầu, trạng thái, người tạo, người duyệt, '
         'khách hàng, hàng hóa, số hợp đồng, khoảng ngày tạo và khối công ty – phòng ban.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh hoặc bấm Tìm kiếm nâng cao.\n'
          '2. Người dùng chọn / nhập các tiêu chí cần lọc.\n'
          '3. Hệ thống nạp lại danh sách ngay khi một ô lọc nâng cao thay đổi; riêng ô tìm '
          'nhanh chờ người dùng bấm nút Tìm kiếm.\n'
          '4. Bảng hiển thị kết quả và cập nhật lại tổng số phiếu.',
    phu='• Không có phiếu nào khớp → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Bấm Làm mới → xóa toàn bộ tiêu chí, bỏ sắp xếp và nạp lại danh sách từ đầu.\n'
        '• Bộ lọc được ghi nhớ trong 10 phút.',
    dacbiet='Ô lọc “Tên, mã hàng” chỉ tìm trong những dòng hàng ĐƯỢC TÍCH “Cần xuất”. Dòng không '
            'tích là hàng của hợp đồng mà người lập không xin giữ, tìm ra sẽ gây hiểu nhầm.')

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
    ('Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Lọc riêng theo mã phiếu.'),
    ('Loại yêu cầu', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Trống', '–'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Trống', '–'),
    ('Người tạo / Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống',
     'Người duyệt xét theo bước duyệt cuối (Kế toán).'),
    ('Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng', 'Trống', '–'),
    ('Tên, mã hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Một ô lọc chung cho cả tên và mã hàng hóa; chỉ xét dòng có tích Cần xuất.'),
    ('Số hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Lọc theo số hợp đồng gắn ở đầu phiếu, áp cho cả năm loại có hợp đồng.'),
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
    ('Lọc theo Số hợp đồng', 'Change',
     'After:\n– Chỉ giữ những phiếu có hợp đồng khớp số đã nhập.\n'
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
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('03-cai-dat-bo-loc.png'),
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
    dacbiet='Bảy cột Khách hàng, Giữ đến ngày, Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú '
            'và Lý do từ chối mặc định TẮT.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột hiển thị', shot=shot('04-cau-hinh-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '17 cột', '–', 'Theo cấu hình đã lưu',
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
d.h3('2.5 Tạo mới phiếu')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Tạo mới yêu cầu xuất giữ', 'crud',
            [('include', 'Chọn loại yêu cầu'),
             ('include', 'Sinh mã phiếu tự động'),
             ('extend', 'Chọn hợp đồng và nạp hàng hóa theo hợp đồng'),
             ('extend', 'Chọn khách hàng và tự thêm hàng hóa'),
             ('extend', 'Đính kèm tệp')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-05 Tạo mới phiếu')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới yêu cầu xuất giữ',
    mota='Lập phiếu đề nghị giữ hàng trong kho cho một khách hàng tới một hạn nhất định. Phiếu '
         'có thể lưu nháp hoặc gửi thẳng cho Trưởng phòng duyệt.',
    tacnhan='Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng bấm nút Tạo mới ở màn danh sách.\n'
          '2. Người dùng chọn Loại yêu cầu.\n'
          '3. Với loại có hợp đồng: người dùng chọn hợp đồng; hệ thống nạp sẵn khách hàng và '
          'toàn bộ hàng hóa của hợp đồng vào bảng Chi tiết.\n'
          '4. Với loại Xuất giữ khác: người dùng chọn Khách hàng rồi tự thêm từng dòng hàng và '
          'chọn đơn vị tính.\n'
          '5. Người dùng nhập Giữ đến ngày, tích Cần xuất và nhập SL đề nghị cho từng dòng.\n'
          '6. Người dùng bấm Lưu nháp hoặc Gửi duyệt.\n'
          '7. Hệ thống kiểm tra dữ liệu, sinh mã phiếu và ghi phiếu ở trạng thái tương ứng.\n'
          '8. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Lưu nháp → phiếu ở trạng thái Đang tạo, chỉ người lập nhìn thấy.\n'
        '• Gửi duyệt → phiếu sang Chờ TP duyệt và hệ thống kiểm tra thêm tồn kho.\n'
        '• Không tích dòng nào, hoặc tích nhưng số lượng đều bằng 0 → báo lỗi, không lưu.\n'
        '• Số lượng vượt phần còn lại của hợp đồng → báo lỗi tại dòng, không lưu.\n'
        '• Số lượng vượt tồn kho khả dụng khi gửi duyệt → báo lỗi tại dòng, không lưu.\n'
        '• Rời màn khi đã nhập mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
    dacbiet='Loại Xuất giữ khác bắt buộc thêm ba thông tin mà năm loại kia không cần: '
            'Khách hàng, Ghi chú và ít nhất một tệp đính kèm.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('06-tao-moi.png'),
         shot_caption='Màn lập yêu cầu xuất giữ lúc mới mở')
d.layout(menu=MENU + ' => Tạo mới => Chọn hợp đồng', shot=shot('16-popup-chon-hop-dong.png'),
         shot_caption='Cửa sổ Chọn hợp đồng của loại yêu cầu có gắn hợp đồng')
d.layout(menu=MENU + ' => Sửa', shot=shot('08-sua-loai-hop-dong.png'),
         shot_caption='Phiếu loại có hợp đồng: bảng hàng hóa nạp sẵn từ hợp đồng, chỉ tích và '
                      'nhập số lượng')
d.layout(menu=MENU + ' => Sửa', shot=shot('07-sua-loai-khac.png'),
         shot_caption='Phiếu loại Xuất giữ khác: tự thêm từng dòng hàng và chọn đơn vị tính')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Người lập – Ngày lập', 'Label', 'Read-only', '–', '–',
     'Người đăng nhập – ngày hiện tại', 'Hiển thị ở góc phải khối Thông tin chung.'),
    ('Loại yêu cầu', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Có', 'Trống',
     'Sau khi phiếu đã lưu thì khóa lại; ô khóa có biểu tượng ⓘ giải thích vì sao.'),
    ('Hợp đồng', 'Textbox + Button', 'Read-only + Enable', '–', 'Có (loại 1–5)',
     'Chưa chọn hợp đồng',
     'Chỉ hiện với năm loại có hợp đồng. Chọn bằng nút Chọn, mở cửa sổ tìm hợp đồng. Bảng hợp '
     'đồng nguồn đổi theo loại yêu cầu.'),
    ('Mã khách hàng', 'Textbox', 'Disable', '–', 'Không', 'Tự điền theo hợp đồng',
     'Chỉ hiện với loại có hợp đồng; có biểu tượng ⓘ giải thích ô khóa.'),
    ('Khách hàng', 'Dropdown / Textbox', 'Enable hoặc Disable', 'Danh sách khách hàng',
     'Có (loại Xuất giữ khác)', 'Trống hoặc tự điền theo hợp đồng',
     'Loại Xuất giữ khác tự chọn; năm loại kia lấy theo hợp đồng và khóa lại. Ô tìm khách hàng '
     'cần gõ tối thiểu 2 ký tự.'),
    ('Giữ đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Trống',
     'Lịch chặn sẵn ngày quá khứ và ngày vượt trần. Dưới ô có dòng nhắc “Không giữ quá …”.'),
    ('Số điện thoại / Địa chỉ / Địa chỉ giao hàng', 'Textbox', 'Disable', '–', 'Không',
     'Tự điền theo hợp đồng hoặc khách hàng', 'Ba ô chỉ đọc, in ra phiếu; đều có biểu tượng ⓘ.'),
    ('Phòng ban yêu cầu', 'Textbox', 'Disable', '–', 'Không', 'Phòng ban của người lập',
     'Hệ thống tự điền, có biểu tượng ⓘ giải thích.'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Có với loại Xuất giữ khác', 'Trống', '–'),
    ('Lý do từ chối gần nhất', 'Textbox', 'Disable', '–', '–', 'Ẩn',
     'Chỉ hiện khi phiếu đã từng bị trả về; đây là chỗ DUY NHẤT người lập biết vì sao bị trả.'),
    ('Chọn tệp đính kèm', 'Button', 'Enable',
     'PDF, ảnh, Word, Excel; tối đa 13 MB mỗi tệp', 'Có với loại Xuất giữ khác', 'Chưa có tệp',
     'Chọn được nhiều tệp; mỗi tệp có nút gỡ khỏi phiếu.'),
    ('Nút Thêm hàng hóa', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện với loại Xuất giữ khác; mở cửa sổ tìm hàng hóa còn tồn kho.'),
    ('Cột Cần xuất', 'Checkbox', 'Enable / Ẩn', '–', '–', 'Bỏ tích',
     'Chỉ hiện với loại có hợp đồng. Dòng không tích bị làm mờ và lưu với số lượng 0.'),
    ('Cột Tên hàng hóa / Mã hàng hóa / Model / Thương hiệu', 'Table/Grid', 'Read-only', '–', '–',
     'Theo hàng hóa', 'Không sửa được.'),
    ('Cột Có thể giữ', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo tồn kho',
     'Tồn kho khả dụng đã trừ hàng khuyến mại. Là số tham khảo.'),
    ('Cột SL hợp đồng / Đã xuất kho', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo hợp đồng',
     'Chỉ hiện với loại có hợp đồng; loại Xuất giữ HĐDV ẩn hai cột này.'),
    ('Cột Đề nghị', 'Number', 'Enable', '> 0, tối đa 6 chữ số', 'Có', 'Trống',
     'Chỉ nhận ký tự số. Nhập sai thì báo đỏ tại dòng và giữ nguyên số đã gõ.'),
    ('Cột ĐVT', 'Dropdown / Label', 'Enable hoặc Read-only', 'Danh sách đơn vị của hàng hóa',
     'Có với loại Xuất giữ khác', 'Đơn vị cơ bản',
     'Chỉ loại Xuất giữ khác được chọn; đổi đơn vị thì hệ thống tính lại số Có thể giữ.'),
    ('Cột Đơn giá / Thành tiền', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Thành tiền bằng Đơn giá nhân SL đề nghị.'),
    ('Nút xóa dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện với loại Xuất giữ khác.'),
    ('Dòng Tổng cộng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Cộng các cột số lượng và thành tiền của bảng.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Ghi phiếu ở trạng thái Đang tạo, chưa gửi đi đâu.'),
    ('Nút Gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Ghi phiếu và chuyển sang Chờ TP duyệt.'),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị ở màn Tạo mới',
     'Lưu nháp rồi ở lại để lập phiếu kế tiếp.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi tại ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi; không tự sửa giá trị người dùng đã nhập.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Loại yêu cầu', 'Change',
     'During:\n– Loại có hợp đồng → hiện ô Hợp đồng và nút Chọn, khóa ô Khách hàng.\n'
     '– Loại Xuất giữ khác → hiện ô chọn Khách hàng, nút Thêm hàng hóa và ô ĐVT trên từng dòng.\n'
     'After:\n– Xóa sạch bảng Chi tiết đang có để tránh trộn hàng của hai loại.'),
    ('Bấm Chọn hợp đồng', 'Click',
     'During:\n– Cửa sổ liệt kê hợp đồng theo đúng bảng nguồn của loại đang chọn, tìm được theo '
     'số hợp đồng hoặc tên khách hàng.\n'
     'After:\n– Điền số hợp đồng, mã và tên khách hàng, số điện thoại, địa chỉ vào phiếu.\n'
     '– Nạp toàn bộ hàng hóa của hợp đồng vào bảng Chi tiết kèm SL hợp đồng và Đã xuất kho.'),
    ('Bấm Thêm hàng hóa (loại Xuất giữ khác)', 'Click',
     'During:\n– Cửa sổ liệt kê hàng hóa còn tồn kho.\n'
     'After:\n– Các dòng được chọn thêm vào bảng Chi tiết, mặc định đơn vị cơ bản.'),
    ('Đổi ĐVT của một dòng', 'Change',
     'After:\n– Hệ thống tính lại số Có thể giữ theo đơn vị mới; số lượng đã gõ giữ nguyên.'),
    ('Nhập SL đề nghị', 'Change / Blur',
     'During:\n– Chỉ nhận ký tự số.\n'
     '– Bằng 0 mà dòng vẫn tích Cần xuất → báo “Phải lớn hơn 0.”.\n'
     '– Vượt phần còn lại của hợp đồng → báo “Vượt số lượng còn lại của hợp đồng (còn …).”.\n'
     'After:\n– Giữ nguyên giá trị người dùng đã gõ, không tự kéo về mức trần.'),
    ('Bấm Lưu nháp', 'Click',
     'During:\n– Kiểm tra Giữ đến ngày và các ràng buộc theo loại yêu cầu.\n'
     '– KHÔNG kiểm tra tồn kho ở bước này.\n'
     'After:\n– Sinh mã phiếu dạng PYCXG-NNNNN, ghi phiếu ở trạng thái Đang tạo.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.'),
    ('Bấm Gửi duyệt', 'Click',
     'During:\n– Kiểm tra đủ như khi lưu nháp.\n'
     '– Kiểm tra thêm tồn kho khả dụng của từng dòng; thiếu thì báo “Vượt số có thể giữ '
     '(còn …).” và không lưu.\n'
     '– Chưa tích dòng nào hoặc số lượng đều bằng 0 → báo “Chưa chọn hàng hoá nào cần giữ, hoặc '
     'số lượng đề nghị đều bằng 0.”.\n'
     'After:\n– Ghi phiếu ở trạng thái Chờ TP duyệt và thông báo cho Trưởng phòng quản lý phòng '
     'ban của người lập.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
    ('Bấm Lưu và tiếp tục', 'Click',
     'After:\n– Lưu nháp phiếu hiện tại rồi làm mới màn hình để lập phiếu kế tiếp, không quay '
     'về danh sách.'),
])

# ------------------------------------------------------------ 2.6
d.h3('2.6 Chỉnh sửa phiếu')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Chỉnh sửa yêu cầu xuất giữ', 'crud',
            [('include', 'Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo'),
             ('extend', 'Đặt lại toàn bộ các bước duyệt')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-06 Chỉnh sửa phiếu')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Chỉnh sửa yêu cầu xuất giữ',
    mota='Sửa lại phiếu còn nháp, hoặc phiếu vừa bị một cấp trả về, rồi gửi duyệt lại từ đầu.',
    tacnhan='Nhân viên kinh doanh — người lập phiếu',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.',
    chinh='1. Người dùng bấm nút Sửa ở màn danh sách hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở màn sửa với dữ liệu đã lưu của phiếu.\n'
          '3. Người dùng chỉnh sửa; nếu phiếu bị trả về thì đọc ô Lý do từ chối gần nhất.\n'
          '4. Người dùng bấm Lưu nháp hoặc Gửi duyệt.\n'
          '5. Hệ thống đặt lại toàn bộ các bước duyệt và ghi phiếu theo trạng thái đã chọn.',
    phu='• Phiếu đang chờ duyệt hoặc đã duyệt → nút Sửa không hiển thị; mở thẳng bằng đường dẫn '
        'thì hệ thống từ chối.\n'
        '• Phiếu của người khác → hệ thống từ chối, trừ người có vai trò quản trị hệ thống.\n'
        '• Không đổi được Loại yêu cầu và Hợp đồng ở màn Sửa.\n'
        '• Các nhánh lỗi nhập liệu giống chức năng Tạo mới.',
    dacbiet='Với loại Xuất giữ khác, tệp đính kèm vẫn bắt buộc khi sửa: gỡ hết tệp rồi lưu sẽ '
            'bị chặn, vì phiếu báo giữ là chứng từ gốc của loại này.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('07-sua-loai-khac.png'),
         shot_caption='Màn sửa phiếu loại Xuất giữ khác, trạng thái Đang tạo')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mã phiếu', 'Textbox', 'Disable', 'PYCXG-NNNNN', '–', 'Theo dữ liệu',
     'Chỉ hiển thị, không sửa được.'),
    ('Trạng thái', 'Badge', 'Read-only', '–', '–', 'Đang tạo', 'Nhãn màu xám.'),
    ('Loại yêu cầu / Hợp đồng', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu',
     'Khóa hẳn ở màn Sửa; ô khóa có biểu tượng ⓘ giải thích.'),
    ('Khách hàng', 'Dropdown / Textbox', 'Enable hoặc Disable', 'Danh sách khách hàng', '–',
     'Theo dữ liệu', 'Chỉ loại Xuất giữ khác mới đổi được khách hàng.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu đã lưu',
     'Các dòng đã lưu được nạp sẵn kèm ô tích Cần xuất và số lượng.'),
    ('Nút Lưu nháp / Gửi duyệt / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Màn sửa không có nút Lưu và tiếp tục.'),
], )

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System',
     'Before:\n– Kiểm tra phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.\n'
     '– Nếu không → hệ thống từ chối và không mở màn sửa.\n'
     'After:\n– Nạp dữ liệu phiếu, kèm lý do bị trả về gần nhất nếu có.'),
    ('Bấm Gửi duyệt', 'Click',
     'During:\n– Kiểm tra dữ liệu giống chức năng Tạo mới, gồm cả kiểm tra tồn kho.\n'
     '– Tồn kho được tính theo CHỦ PHIẾU, tức người lập, không phải người đang sửa.\n'
     'After:\n– ĐẶT LẠI dấu duyệt của cả ba cấp Trưởng phòng, Ban giám đốc và Kế toán.\n'
     '– Xóa lý do bị trả về cũ, đưa phiếu về trạng thái Chờ TP duyệt.\n'
     '– Ghi một dòng lịch sử “Chỉnh sửa”, nêu rõ những giá trị đã thay đổi.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.7
d.h3('2.7 Xem chi tiết phiếu')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết yêu cầu xuất giữ',
    mota='Hiển thị toàn bộ thông tin phiếu ở chế độ chỉ đọc: thông tin chung, tệp đính kèm, '
         'bảng hàng hóa, lịch sử duyệt và lịch sử thay đổi.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Người dùng nằm trong phạm vi được xem phiếu.',
    chinh='1. Người dùng bấm vào mã phiếu ở màn danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống hiển thị màn chi tiết ở chế độ chỉ đọc.\n'
          '4. Các nút thao tác ở cuối màn hiện theo đúng quyền và trạng thái của phiếu.',
    phu='• Không đủ quyền xem → hệ thống báo không có quyền xem phiếu này.\n'
        '• Phiếu Đang tạo của người khác → không mở được.\n'
        '• Phiếu đã có Phiếu xuất giữ → khối Lịch sử duyệt ghi rõ phiếu được duyệt qua mã PXG '
        'tương ứng.',
    dacbiet='Các nút ở cuối màn chi tiết luôn khớp với các nút ở cột Hành động ngoài danh sách '
            'của cùng phiếu đó; riêng nút Từ chối chỉ có ở màn chi tiết.')

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('09-chi-tiet.png'),
         shot_caption='Màn chi tiết phiếu đã duyệt, ở chế độ chỉ đọc')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('10-chi-tiet-nguoi-duyet.png'),
         shot_caption='Màn chi tiết nhìn từ người có quyền duyệt: nút BGĐ duyệt và Từ chối ở '
                      'cuối màn')

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Chi tiết yêu cầu xuất giữ: <mã phiếu>', '–'),
    ('Khối Thông tin chung', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm Mã phiếu, Trạng thái, Loại yêu cầu, Hợp đồng, Khách hàng, Giữ đến ngày, Phòng ban '
     'yêu cầu, Địa chỉ, Ghi chú, người lập và ngày lập.'),
    ('Khối File đính kèm', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Danh sách tệp mở xem được; không có tệp thì hiện “Chưa có tệp đính kèm”.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Đủ các cột của màn lập phiếu, kèm dòng Tổng cộng. Người xem không sửa được ô nào.'),
    ('Khối Lịch sử duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Ghi rõ từng cấp đã duyệt, người duyệt và thời điểm.'),
    ('Khối Lịch sử thay đổi', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Chỉ nạp dữ liệu khi người dùng bấm Xem lịch sử.'),
    ('Nút thao tác cuối màn', 'Button', 'Enable / Ẩn', '–', 'Theo quyền và trạng thái',
     'Gồm Sửa, Xóa, In, nút duyệt của cấp hiện tại, Từ chối, Lập phiếu xuất giữ và Quay lại; '
     'nút không dùng được thì ẩn hẳn.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu theo phạm vi dữ liệu và quyền xử lý.\n'
     '– Không đủ quyền → báo không có quyền xem phiếu này.\n'
     'After:\n– Hiển thị dữ liệu phiếu và các nút thao tác hợp lệ.'),
    ('Bấm Xem lịch sử ở khối Lịch sử thay đổi', 'Click',
     'After:\n– Nạp và hiển thị danh sách mốc thay đổi của phiếu, mới nhất trước.'),
])

# ------------------------------------------------------------ 2.8
d.h3('2.8 Duyệt phiếu')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Duyệt yêu cầu xuất giữ', 'action',
            [('include', 'Kiểm tra quyền duyệt đúng cấp và cùng công ty'),
             ('extend', 'Xác định có phải qua Ban giám đốc hay không'),
             ('extend', 'Nhập lại Giữ đến ngày ở bước Ban giám đốc')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-08 Duyệt phiếu')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Duyệt yêu cầu xuất giữ',
    mota='Ký duyệt phiếu ở cấp Trưởng phòng hoặc Ban giám đốc. Hai bước này KHÔNG ghi tồn hàng '
         'giữ; hàng chỉ được giữ ở bước cuối, khi Kế toán lập và duyệt Phiếu xuất giữ.',
    tacnhan='Trưởng phòng; Ban giám đốc',
    dieukien='Phiếu đang ở đúng trạng thái chờ cấp đó duyệt; người duyệt có quyền tương ứng và '
             'cùng công ty với phiếu.',
    chinh='1. Người duyệt mở màn chi tiết phiếu.\n'
          '2. Người duyệt xem lại các dòng hàng và số lượng đề nghị.\n'
          '3. Người duyệt bấm nút duyệt của cấp mình.\n'
          '4. Hệ thống hỏi xác nhận và kiểm tra quyền, trạng thái.\n'
          '5. Hệ thống chuyển phiếu sang bước tiếp theo, ghi lịch sử và gửi thông báo.\n'
          '6. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Trưởng phòng duyệt: nếu phiếu thuộc diện phải qua Ban giám đốc thì chuyển sang '
        'Chờ BGĐ duyệt và báo “Yêu cầu đã được chuyển đến Ban giám đốc.”, ngược lại chuyển '
        'thẳng sang Chờ KT duyệt và báo “Yêu cầu đã được chuyển đến Kế toán.”.\n'
        '• Ban giám đốc duyệt → chuyển sang Chờ KT duyệt.\n'
        '• Phiếu đã được người khác xử lý trước đó → báo “Phiếu không ở trạng thái chờ duyệt.”.\n'
        '• Người dùng không đúng cấp → báo “Bạn không có quyền duyệt bước này.”.',
    dacbiet='Bước Ban giám đốc BẮT BUỘC nhập lại Giữ đến ngày. Hạn giữ do Ban giám đốc chốt sẽ '
            'là hạn đi tiếp xuống Kế toán.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Duyệt', shot=shot('10-chi-tiet-nguoi-duyet.png'),
         shot_caption='Nút duyệt của cấp hiện tại nằm ở cuối màn chi tiết')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút duyệt của cấp hiện tại', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Nhãn nêu rõ cấp đang ký: TP duyệt hoặc BGĐ duyệt. Chú thích khi rê chuột nói rõ phiếu sẽ '
     'đi đâu tiếp.'),
    ('Hộp thoại xác nhận duyệt', 'Modal', 'Hiển thị', '–', 'Ẩn',
     'Tiêu đề “Xác nhận duyệt”, nội dung nêu rõ mã phiếu và bước kế tiếp.'),
    ('Ô Giữ đến ngày ở bước Ban giám đốc', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy', 'Ẩn',
     'Chỉ hiện ở bước Ban giám đốc; bắt buộc nhập, vẫn chịu trần hạn giữ của hệ thống.'),
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Hiện cùng lúc với nút duyệt của cấp đó, và hiện cả với Kế toán ở bước Chờ KT duyệt.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người duyệt KHÔNG sửa được số lượng đề nghị.'),
], required=False)

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút duyệt của cấp hiện tại', 'Click',
     'Before:\n– Kiểm tra quyền duyệt đúng cấp và cùng công ty với phiếu.\n'
     '– Trưởng phòng còn phải quản lý phòng ban ghi trên phiếu.\n'
     '– Nếu không → hiển thị “Bạn không có quyền duyệt bước này.” và dừng xử lý.\n'
     'During:\n– Hiển thị hộp thoại xác nhận; người dùng hủy thì không làm gì.\n'
     '– Phiếu không còn ở trạng thái chờ duyệt → hiển thị “Phiếu không ở trạng thái chờ '
     'duyệt.”.\n'
     '– Bước Ban giám đốc: Giữ đến ngày trống, không hợp lệ, là ngày quá khứ hoặc vượt trần → '
     'báo lỗi và dừng.\n'
     'After:\n– Ghi lại người duyệt và thời điểm duyệt của cấp đó.\n'
     '– Trưởng phòng duyệt: chuyển sang Chờ BGĐ duyệt hoặc Chờ KT duyệt tùy điều kiện.\n'
     '– Ban giám đốc duyệt: ghi lại hạn giữ mới và chuyển sang Chờ KT duyệt.\n'
     '– Ghi một dòng lịch sử “Duyệt”; gửi thông báo cho cấp kế tiếp.\n'
     '– Hiển thị thông báo tương ứng và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.9
d.h3('2.9 Từ chối phiếu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Từ chối yêu cầu xuất giữ', 'action',
            [('include', 'Kiểm tra quyền xử lý đúng cấp'),
             ('include', 'Bắt buộc nhập lý do')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-09 Từ chối phiếu')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Từ chối yêu cầu xuất giữ',
    mota='Trả phiếu về cho người lập kèm lý do. Phiếu quay về đúng trạng thái Đang tạo để người '
         'lập sửa rồi gửi lại.',
    tacnhan='Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Phiếu đang ở đúng trạng thái chờ cấp đó xử lý.',
    chinh='1. Người xử lý bấm nút Từ chối ở màn chi tiết.\n'
          '2. Hệ thống mở cửa sổ nhập lý do.\n'
          '3. Người xử lý nhập lý do.\n'
          '4. Người xử lý bấm nút xác nhận.\n'
          '5. Hệ thống đưa phiếu về trạng thái Đang tạo, ghi lý do và gửi thông báo cho người '
          'lập.',
    phu='• Bỏ trống lý do → báo bắt buộc nhập, cửa sổ không đóng.\n'
        '• Lý do quá 255 ký tự → báo “Không được vượt quá 255 ký tự”.\n'
        '• Phiếu đã được xử lý trước đó → báo “Bạn không có quyền từ chối phiếu này.”.',
    dacbiet='⚠ Hệ thống KHÔNG có trạng thái “Từ chối” riêng: phiếu bị trả về nằm chung trạng '
            'thái Đang tạo với phiếu chưa gửi bao giờ. Phân biệt bằng cột Lý do từ chối, hoặc '
            'ô Lý do từ chối gần nhất ở màn sửa.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Từ chối', shot=shot('11-popup-tu-choi.png'),
         shot_caption='Cửa sổ Từ chối yêu cầu xuất giữ')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Từ chối yêu cầu xuất giữ',
     'Kèm dòng phụ hiển thị mã phiếu.'),
    ('Lý do', 'Textarea', 'Enable', '1–255 ký tự', 'Trống',
     'Gợi ý nhập lý do trả lại phiếu cho người lập. Bắt buộc nhập.'),
    ('Nút xác nhận', 'Button', 'Enable', '–', 'Hiển thị', 'Bị khóa trong lúc đang xử lý.'),
    ('Nút đóng cửa sổ', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng và bỏ nội dung đã nhập.'),
], required=False)

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Từ chối', 'Click',
     'Before:\n– Kiểm tra người dùng đang ở đúng cấp xử lý của phiếu.\n'
     '– Nếu không → hiển thị “Bạn không có quyền từ chối phiếu này.”.\n'
     'After:\n– Mở cửa sổ nhập lý do.'),
    ('Bấm xác nhận từ chối', 'Click',
     'During:\n– Lý do trống → hiển thị thông báo bắt buộc nhập, cửa sổ không đóng.\n'
     '– Lý do quá 255 ký tự → hiển thị “Không được vượt quá 255 ký tự”.\n'
     'After:\n– Đưa phiếu về trạng thái Đang tạo và ghi lý do vào phiếu.\n'
     '– ⚠ Hàng giữ KHÔNG thay đổi, vì yêu cầu chưa từng ghi tồn.\n'
     '– Ghi một dòng lịch sử; gửi thông báo cho người lập phiếu.\n'
     '– Hiển thị thông báo thành công và nạp lại danh sách.'),
])

# ------------------------------------------------------------ 2.10
d.h3('2.10 Xóa phiếu')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa yêu cầu xuất giữ', 'action',
            [('include', 'Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa và Thông báo.', anchor='delete')
d.intro_table(
    ten='Xóa yêu cầu xuất giữ',
    mota='Xóa hẳn một phiếu đang ở trạng thái Đang tạo do chính người dùng lập.',
    tacnhan='Nhân viên kinh doanh — người lập phiếu',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.',
    chinh='1. Người dùng bấm nút Xóa ở cột Hành động hoặc ở màn chi tiết.\n'
          '2. Hệ thống hiển thị hộp thoại xác nhận kèm mã phiếu.\n'
          '3. Người dùng chọn Xóa.\n'
          '4. Hệ thống xóa phiếu và nạp lại danh sách.',
    phu='• Chọn Hủy → đóng hộp thoại, không xóa gì.\n'
        '• Phiếu đang chờ duyệt hoặc đã duyệt → nút Xóa không hiển thị; gọi thẳng chức năng xóa '
        'thì hệ thống báo “Không thể xóa phiếu này.”.',
    dacbiet='Lịch sử thay đổi của phiếu được giữ lại sau khi xóa để phục vụ tra cứu.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('12-xac-nhan-xoa.png'),
         shot_caption='Hộp thoại Xác nhận xóa phiếu')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Tiêu đề cố định.'),
    ('Nội dung hỏi', 'Label', 'Hiển thị', 'Bạn có chắc muốn xóa phiếu <mã phiếu>?',
     'Có nêu rõ mã phiếu để tránh xóa nhầm.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Nút nhóm nguy hiểm, màu đỏ.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không thực hiện gì.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa', 'Click',
     'Before:\n– Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo.\n'
     '– Nếu không → nút không hiển thị; gọi thẳng chức năng thì hệ thống từ chối.\n'
     'After:\n– Mở hộp thoại xác nhận.'),
    ('Xác nhận Xóa', 'Click',
     'After:\n– Xóa phiếu cùng các dòng hàng của phiếu; lịch sử thay đổi được giữ lại.\n'
     '– Hiển thị thông báo xóa thành công và nạp lại danh sách.'),
])

# ------------------------------------------------------------ 2.11
d.h3('2.11 Lập phiếu xuất giữ')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Lập phiếu xuất giữ từ yêu cầu', 'action',
            [('include', 'Kiểm tra quyền Kế toán và trạng thái Chờ KT duyệt'),
             ('include', 'Chuyển sang màn lập Phiếu xuất giữ'),
             ('extend', 'Chặn lập trùng khi yêu cầu đã có phiếu xuất giữ')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-11 Lập phiếu xuất giữ')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Thông báo và Phân quyền.', anchor='notice')
d.intro_table(
    ten='Lập phiếu xuất giữ từ một yêu cầu đã duyệt đủ cấp',
    mota='Bước cuối của luồng. Kế toán không bấm “duyệt” ở màn này mà lập Phiếu xuất giữ; chính '
         'phiếu đó khi được duyệt mới ghi tồn hàng giữ và đóng dấu Đã duyệt lên yêu cầu.',
    tacnhan='Kế toán',
    dieukien='Phiếu đang ở trạng thái Chờ KT duyệt; người dùng có quyền Kế toán duyệt hàng giữ '
             'và cùng công ty với phiếu.',
    chinh='1. Kế toán mở màn chi tiết của yêu cầu.\n'
          '2. Kế toán bấm nút Lập phiếu xuất giữ.\n'
          '3. Hệ thống chuyển sang màn lập Phiếu xuất giữ, gắn sẵn yêu cầu nguồn.\n'
          '4. Kế toán đối chiếu số lượng rồi lưu nháp hoặc duyệt giữ hàng.\n'
          '5. Lưu nháp → yêu cầu chuyển sang Đang xuất giữ.\n'
          '6. Duyệt giữ hàng → hệ thống ghi tồn hàng giữ và yêu cầu chuyển sang Đã duyệt.',
    phu='• Yêu cầu đã có phiếu xuất giữ → hệ thống báo yêu cầu này đã có phiếu, kèm mã phiếu.\n'
        '• Người dùng không đủ quyền → báo “Bạn không đủ quyền lập phiếu xuất giữ cho yêu cầu '
        'này.”.\n'
        '• Phiếu xuất giữ còn nháp bị xóa → yêu cầu quay lại Chờ KT duyệt.',
    dacbiet='⚠ Chủ lô hàng giữ là NGƯỜI LẬP YÊU CẦU, không phải Kế toán lập phiếu. Công ty, '
            'phòng ban của lô cũng lấy theo người lập yêu cầu.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Lập phiếu xuất giữ',
         shot=shot('15-cho-ke-toan-lap-phieu.png'),
         shot_caption='Yêu cầu ở trạng thái Chờ KT duyệt, nút Lập phiếu xuất giữ hiện ở cuối màn')

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Lập phiếu xuất giữ', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện với Kế toán đủ điều kiện, phiếu ở Chờ KT duyệt. Chú thích khi rê chuột nói rõ '
     'đây là bước ghi tồn hàng giữ.'),
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Kế toán vẫn từ chối được ở bước này, đưa phiếu về Đang tạo.'),
    ('Trạng thái sau khi lưu nháp phiếu con', 'Badge', 'Read-only', '–', 'Đang xuất giữ',
     'Nhãn màu cam; người lập biết kế toán đang xử lý dở.'),
], required=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lập phiếu xuất giữ', 'Click',
     'Before:\n– Kiểm tra quyền Kế toán duyệt hàng giữ, cùng công ty và trạng thái Chờ KT '
     'duyệt.\n'
     'After:\n– Điều hướng sang màn lập Phiếu xuất giữ, gắn sẵn yêu cầu nguồn.'),
    ('Phiếu xuất giữ được lưu nháp', 'System',
     'After:\n– Yêu cầu chuyển sang trạng thái Đang xuất giữ và ghi một dòng lịch sử.'),
    ('Phiếu xuất giữ được duyệt', 'System',
     'After:\n– Hệ thống ghi tồn hàng giữ cho người lập yêu cầu.\n'
     '– Yêu cầu chuyển sang Đã duyệt; cột Người duyệt và Ngày duyệt được điền.\n'
     '– Ghi một dòng lịch sử nêu rõ phiếu được duyệt qua mã phiếu xuất giữ nào.'),
    ('Phiếu xuất giữ còn nháp bị xóa', 'System',
     'After:\n– Yêu cầu quay lại trạng thái Chờ KT duyệt để Kế toán lập lại.'),
])

# ------------------------------------------------------------ 2.12
d.h3('2.12 In phiếu và In danh sách')

d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'In phiếu và In danh sách', 'io',
            [('extend', 'In một phiếu'),
             ('extend', 'In danh sách theo bộ lọc đang áp')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-12 In phiếu và In danh sách')

d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc màn In và Xuất dữ liệu.', anchor='excel')
d.intro_table(
    ten='In yêu cầu xuất giữ và in danh sách',
    mota='Mở cửa sổ xem trước để in một phiếu, hoặc in toàn bộ danh sách theo đúng bộ lọc '
         'đang áp dụng.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Với bản in phiếu: người dùng xem được phiếu đó.',
    chinh='1. Người dùng bấm nút In ở cột Hành động, ở màn chi tiết, hoặc nút In ở thanh công '
          'cụ danh sách.\n'
          '2. Hệ thống mở cửa sổ xem trước ngay trên màn đang đứng.\n'
          '3. Người dùng bấm nút In trên cửa sổ xem trước để gửi lệnh in.',
    phu='• Bản in danh sách dùng khổ A4 ngang.\n'
        '• Bản in danh sách in đúng phạm vi và điều kiện lọc đang áp.\n'
        '• Phiếu chưa duyệt thì ô Ngày duyệt trên bản in để TRỐNG.',
    dacbiet='Phần đầu bản in lấy theo công ty ghi trên phiếu, không lấy theo người đang in.')

d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In', shot=shot('14-in-phieu.png'),
         shot_caption='Cửa sổ Xem trước yêu cầu xuất giữ')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In trên cửa sổ xem trước', 'Button', 'Enable', '–', 'Hiển thị',
     'Nằm cạnh tiêu đề cửa sổ.'),
    ('Phần đầu chứng từ', 'Label', 'Read-only', '–', 'Theo công ty của phiếu',
     'Gồm logo và thông tin liên hệ của công ty ghi trên phiếu.'),
    ('Khối thông tin phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Loại yêu cầu, hợp đồng, khách hàng, địa chỉ, người yêu cầu, phòng ban, giữ đến ngày, '
     'trạng thái.'),
    ('Bảng hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cột hàng hóa, số lượng đề nghị, đơn vị tính, đơn giá, thành tiền và dòng Tổng cộng.'),
    ('Bảng thông tin duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người duyệt và thời gian duyệt từng cấp; bước chưa duyệt để trống.'),
    ('Khối ký tên', 'Label', 'Read-only', '–', 'Hiển thị',
     'Các ô ký theo mẫu chứng từ của công ty.'),
    ('Bản in danh sách', 'Table/Grid', 'Read-only', '–', 'Theo bộ lọc',
     'Khổ A4 ngang, có dòng tổng số phiếu và các cột chính của màn danh sách.'),
], required=False)

d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In ở dòng hoặc ở màn chi tiết', 'Click',
     'After:\n– Mở cửa sổ xem trước bản in của đúng phiếu đó.'),
    ('Bấm nút In ở thanh công cụ danh sách', 'Click',
     'After:\n– Mở cửa sổ xem trước bản in danh sách theo đúng bộ lọc đang áp, khổ ngang.'),
])

# ------------------------------------------------------------ 2.13
d.h3('2.13 Xuất Excel danh sách')

d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'Xuất Excel danh sách phiếu', 'io',
            [('include', 'Chọn trường cần xuất'),
             ('include', 'Lấy dữ liệu theo bộ lọc đang áp')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-13 Xuất Excel danh sách')

d.p('2.13.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách yêu cầu xuất giữ',
    mota='Xuất danh sách phiếu ra tệp Excel. Người dùng tự chọn các trường cần xuất và thứ tự '
         'cột trong tệp chạy theo đúng thứ tự đã chọn.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ Chọn trường xuất Excel với 15 trường, mặc định chọn hết.\n'
          '3. Người dùng bỏ chọn các trường không cần.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống lấy toàn bộ dữ liệu khớp bộ lọc và tải tệp về máy.',
    phu='• Trong lúc đang xuất, nút bị khóa để tránh bấm nhiều lần.\n'
        '• Xuất thất bại → hiển thị thông báo lỗi, không tải tệp.',
    dacbiet='Tệp xuất chứa toàn bộ dòng khớp bộ lọc trong phạm vi quyền, không giới hạn ở trang '
            'đang xem.')

d.p('2.13.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('05-chon-truong-xuat-excel.png'),
         shot_caption='Cửa sổ Chọn trường xuất Excel')

d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất Excel', '–'),
    ('Ô chọn trường xuất', 'Dropdown', 'Enable', '15 trường', 'Có', 'Chọn hết 15 trường',
     'Mã phiếu, Loại yêu cầu, Người tạo, Ngày tạo, Hợp đồng, Khách hàng, Giữ đến ngày, '
     'Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, '
     'Lý do từ chối.'),
    ('Dòng xem trước thứ tự cột', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn',
     'Liệt kê thứ tự cột sẽ có trong tệp.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Bị khóa trong lúc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
])

d.p('2.13.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xuất Excel', 'Click', 'After:\n– Mở cửa sổ chọn trường xuất.'),
    ('Bấm Xuất file', 'Click',
     'During:\n– Lấy dữ liệu theo đúng bộ lọc và phạm vi quyền hiện tại.\n'
     'After:\n– Dựng tệp Excel theo thứ tự trường đã chọn và tải về máy.\n'
     '– Hiển thị thông báo “Xuất Excel thành công” và đóng cửa sổ.'),
])

# ------------------------------------------------------------ 2.14
d.h3('2.14 Xem lịch sử thay đổi')

d.p('2.14.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Hiển thị các mốc thao tác đã thực hiện trên phiếu: tạo mới, chỉnh sửa, duyệt, từ chối, '
         'kèm người thực hiện, thời điểm và nội dung thay đổi.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Người dùng xem được phiếu.',
    chinh='1. Người dùng bấm biểu tượng Lịch sử ở cột Hành động, hoặc bấm Xem lịch sử ở khối '
          'Lịch sử thay đổi trong màn chi tiết.\n'
          '2. Hệ thống nạp danh sách mốc thay đổi của phiếu.\n'
          '3. Danh sách hiển thị theo thứ tự mới nhất trước.',
    phu='• Phiếu chưa có thao tác nào được ghi nhận → hiện dòng “Chưa có lịch sử thao tác nào.”.\n'
        '• Bấm Làm mới → nạp lại danh sách.',
    dacbiet='Các phiếu lập từ trước khi hệ thống bật tính năng ghi lịch sử sẽ không có mốc nào.')

d.p('2.14.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử', shot=shot('13-lich-su-thay-doi.png'),
         shot_caption='Cửa sổ Lịch sử thay đổi của phiếu')

d.p('2.14.3 Mô tả chi tiết giao diện')
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

d.p('2.14.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem lịch sử', 'Click',
     'After:\n– Nạp danh sách mốc thay đổi và hiển thị, mới nhất trước.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Nạp lại danh sách mốc thay đổi.'),
])

# ==================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu xuất giữ; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Yêu cầu xuất giữ KHÔNG ghi tồn hàng giữ', [
        '– Mọi trạng thái của phiếu này, kể cả Đã duyệt, đều không tự ghi tồn hàng giữ.',
        '– Hàng chỉ thực sự được giữ khi Kế toán lập Phiếu xuất giữ và duyệt phiếu đó.',
        '– Phiếu chuyển sang Đã duyệt là HỆ QUẢ của việc Phiếu xuất giữ được duyệt.',
    ], 'Toàn màn hình'),
    ('BR-02', 'Sáu loại yêu cầu và hai kiểu form', [
        '– Năm loại có hợp đồng (thường, khuyến mại, HĐDV, HĐDA, HĐ hãng): bắt buộc chọn hợp '
        'đồng; khách hàng và danh sách hàng hóa lấy theo hợp đồng; không thêm hay xóa dòng.',
        '– Loại Xuất giữ khác: không gắn hợp đồng; bắt buộc chọn Khách hàng, nhập Ghi chú và '
        'đính kèm ít nhất một tệp; tự thêm, xóa dòng hàng và chọn đơn vị tính.',
        '– Loại yêu cầu KHÔNG đổi được sau khi phiếu đã lưu.',
        '– Loại Xuất giữ HĐDV ẩn hai cột SL hợp đồng và Đã xuất kho.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-03', 'Giữ đến ngày', [
        '– Bắt buộc nhập ở cả lưu nháp lẫn gửi duyệt.',
        '– Phải là ngày tương lai; ngày quá khứ bị chặn ngay trên lịch chọn.',
        '– Không vượt trần cấu hình của hệ thống; loại Xuất giữ HĐDA dùng trần riêng.',
        '– Vượt trần thì hệ thống báo đỏ, KHÔNG tự kéo giá trị về mức trần.',
        '– Ban giám đốc nhập lại Giữ đến ngày ở bước duyệt của mình.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Duyệt']),
    ('BR-04', 'Số lượng đề nghị', [
        '– Phải lớn hơn 0 với mọi dòng có tích Cần xuất; tối đa 6 chữ số.',
        '– Phải có ít nhất một dòng tích Cần xuất với số lượng lớn hơn 0.',
        '– Loại có hợp đồng: không vượt phần còn lại của hợp đồng, tính bằng SL hợp đồng trừ đi '
        'SL đã xuất kho, xét theo đúng cặp hàng hóa và đơn vị tính.',
        '– Hợp đồng nguyên tắc được bỏ qua ràng buộc số lượng còn lại.',
        '– Loại Xuất giữ khác không bị ràng buộc theo hợp đồng.',
        '– Dòng không tích Cần xuất vẫn được lưu với số lượng 0 để giữ nguyên khuôn bảng của '
        'hợp đồng.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-05', 'Kiểm tra tồn kho chỉ khi gửi duyệt', [
        '– Lưu nháp: KHÔNG kiểm tra tồn kho.',
        '– Gửi duyệt: từng dòng phải có tồn kho khả dụng đủ cho số lượng quy đổi về đơn vị cơ '
        'bản; thiếu thì báo “Vượt số có thể giữ (còn …).”.',
        '– Tồn kho khả dụng là tồn kho trừ đi phần hàng khuyến mại.',
        '– Khi sửa phiếu, tồn kho được tính theo NGƯỜI LẬP phiếu, không theo người đang sửa.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-06', 'Luồng duyệt ba cấp', [
        '– Gửi duyệt đưa phiếu về trạng thái Chờ TP duyệt.',
        '– Trưởng phòng duyệt: chuyển sang Chờ BGĐ duyệt nếu phiếu thuộc diện phải trình Ban '
        'giám đốc, ngược lại chuyển thẳng sang Chờ KT duyệt.',
        '– Ban giám đốc duyệt: nhập lại Giữ đến ngày rồi chuyển sang Chờ KT duyệt.',
        '– Kế toán: không có nút duyệt riêng; lập Phiếu xuất giữ. Lưu nháp phiếu con thì yêu cầu '
        'sang Đang xuất giữ; duyệt phiếu con thì yêu cầu sang Đã duyệt.',
    ], ['Duyệt', 'Lập phiếu xuất giữ']),
    ('BR-07', 'Điều kiện phải qua Ban giám đốc', [
        '– Phiếu có hợp đồng: nếu tỉ lệ tiền đã thu trên tổng giá trị hợp đồng thấp hơn ngưỡng '
        'phần trăm cấu hình theo loại hợp đồng của công ty thì phiếu phải qua Ban giám đốc.',
        '– Phiếu không có hợp đồng (loại Xuất giữ khác): tổng thành tiền các dòng cần xuất vượt '
        'hạn mức cấu hình của công ty thì phải qua Ban giám đốc.',
        '– Hệ thống tự xác định, người duyệt không chọn được.',
    ], 'Duyệt'),
    ('BR-08', 'Trưởng phòng duyệt xét theo phòng ban ghi trên phiếu', [
        '– Ngoài quyền và điều kiện cùng công ty, Trưởng phòng còn phải quản lý phòng ban ghi '
        'trên phiếu, tức phòng ban của người lập lúc lập phiếu.',
        '– Người có vai trò quản trị hệ thống được bỏ qua ràng buộc phòng ban.',
    ], 'Duyệt'),
    ('BR-09', 'Từ chối đưa phiếu về Đang tạo', [
        '– Cả ba cấp đều từ chối được, kể cả Kế toán ở bước Chờ KT duyệt.',
        '– Lý do bắt buộc, tối đa 255 ký tự.',
        '– Phiếu quay về đúng trạng thái Đang tạo; hệ thống KHÔNG có trạng thái “Từ chối” riêng.',
        '– Phân biệt phiếu bị trả về với phiếu chưa gửi bao giờ bằng cột Lý do từ chối.',
        '– Nhãn nút là “Từ chối” theo bộ chữ chuẩn của hệ thống.',
    ], ['Duyệt', 'Từ chối']),
    ('BR-10', 'Sửa lại phiếu thì đặt lại toàn bộ các bước duyệt', [
        '– Khi người lập sửa và lưu lại, hệ thống xóa dấu duyệt của cả ba cấp.',
        '– Gửi duyệt lại thì lý do bị trả về cũ được xóa và phiếu đi lại từ bước Chờ TP duyệt.',
    ], 'Chỉnh sửa'),
    ('BR-11', 'Phạm vi dữ liệu', [
        '– Áp theo thứ tự ưu tiên: tổng công ty → công ty → phòng ban → chỉ phiếu của mình.',
        '– Người có quyền xử lý được xem thêm những phiếu đang chờ chính mình ở đúng cấp.',
        '– Phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy.',
        '– Màn danh sách và màn chi tiết dùng cùng một bộ điều kiện.',
        '– Phạm vi này áp cho cả danh sách, màn chi tiết, bản in và tệp Excel xuất ra.',
    ], 'Toàn màn hình'),
    ('BR-12', 'Sửa và xóa phiếu', [
        '– Chỉ sửa hoặc xóa được phiếu do chính mình lập và đang ở trạng thái Đang tạo.',
        '– Người có vai trò quản trị hệ thống được sửa, xóa phiếu Đang tạo của người khác.',
        '– Nút không dùng được thì ẩn hẳn, không để ở trạng thái mờ.',
        '– Xóa phiếu thì các dòng hàng bị xóa theo, lịch sử thay đổi được giữ lại.',
    ], ['Chỉnh sửa', 'Xóa']),
    ('BR-13', 'Tệp đính kèm', [
        '– Nhận các định dạng PDF, ảnh, Word, Excel.',
        '– Mỗi tệp tối đa 13 MB; đính kèm được nhiều tệp trên một phiếu.',
        '– Loại Xuất giữ khác bắt buộc có ít nhất một tệp, cả khi tạo mới lẫn khi sửa.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-14', 'Một yêu cầu chỉ có một phiếu xuất giữ', [
        '– Yêu cầu đã có phiếu xuất giữ thì không lập thêm phiếu thứ hai.',
        '– Phiếu xuất giữ còn nháp bị xóa thì yêu cầu quay lại Chờ KT duyệt để lập lại.',
    ], 'Lập phiếu xuất giữ'),
])

d.save()
