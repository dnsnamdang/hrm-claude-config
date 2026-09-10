# -*- coding: utf-8 -*-
"""Sinh SRS man "Yeu cau dieu chuyen hang giu" theo FORM CHUAN 2026-08-28.

Nguon: code HRM nhanh `gop_db`
  BE  Modules/Finance/{Entities/PrepickTransfer, Services/PrepickTransferRequestService.php,
      Http/Controllers/V1/PrepickTransferRequestController.php, Http/Requests/PrepickTransfer/*}
  FE  pages/finance/prepick-transfer-requests/*
Anh chup that: ./prepick_transfer_shots (Playwright MCP, 1440x900, ngay 05/09/2026).
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

SHOTS = os.path.join(BASE, 'prepick_transfer_shots')
OUT = os.path.join(BASE, 'SRS - Yeu cau dieu chuyen hang giu.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Giữ hàng => Phiếu Yêu cầu điều chuyển hàng giữ'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/prepick-transfer-requests',
           full_url='https://<host-hrm>/finance/prepick-transfer-requests',
           img_prefix='dchg_')

# ============================================================== TRANG DAU
d.title_block('Yêu cầu điều chuyển hàng giữ')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Yêu cầu điều chuyển hàng giữ '
    '(mã phiếu ĐCHG), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, luồng duyệt và phân quyền của màn hình.',
    'Làm rõ bản chất nghiệp vụ: chuyển hàng đang giữ từ người giữ hiện tại sang một nhân viên '
    'khác và một khách hàng khác.',
    'Làm rõ màn hình KHÔNG có trạng thái nháp: lập phiếu là vào thẳng bước chờ Trưởng phòng duyệt.',
    'Làm rõ luồng duyệt 3 cấp và điều kiện đặc thù: Trưởng phòng duyệt xét theo phòng ban của '
    'NGƯỜI NHẬN, không phải phòng ban của người lập.',
    'Làm rõ thời điểm hệ thống thực sự đổi chủ hàng giữ: chỉ khi Kế toán duyệt ở bước cuối.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên '
                 'kinh doanh đứng tên giữ.'),
    ('Lô hàng giữ', 'Một dòng tồn hàng giữ, xác định bởi bộ: nhân viên giữ – khách hàng – '
                    'hàng hóa – hạn giữ – công ty.'),
    ('Điều chuyển hàng giữ', 'Chuyển một phần hoặc toàn bộ số lượng của lô hàng giữ sang một '
                             'nhân viên nhận và một khách hàng nhận khác. Hạn giữ giữ nguyên '
                             'theo lô nguồn.'),
    ('Người nhận', 'Nhân viên sẽ đứng tên giữ hàng sau khi phiếu được duyệt.'),
    ('Khách hàng nhận', 'Khách hàng mà hàng sẽ được giữ cho sau khi phiếu được duyệt.'),
    ('Từ xuất giữ', 'Lô hàng giữ nguồn được chọn để lấy hàng chuyển đi, hiển thị dạng '
                    'số lượng – hạn giữ.'),
    ('Đang giữ', 'Số lượng còn lại của chính lô hàng giữ nguồn.'),
    ('Có thể giữ', 'Tồn kho khả dụng của hàng hóa trong công ty; là số tham khảo, khác với '
                   '“Đang giữ”.'),
    ('TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán — ba cấp duyệt của phiếu.'),
    ('Không duyệt', 'Trạng thái phiếu bị cấp duyệt trả về. Đây là trạng thái riêng của màn này '
                    'và cũng là trạng thái duy nhất cho phép sửa lại phiếu.'),
], widths=[1.6, 4.4])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Màn hình KHÔNG có quyền riêng cho Thêm / Sửa / Xóa: mọi người dùng đã đăng nhập đều lập '
    'được phiếu điều chuyển cho hàng giữ của chính mình, và chỉ sửa / xóa được phiếu do chính '
    'mình lập khi phiếu đang ở trạng thái Không duyệt.')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Trưởng phòng duyệt hàng giữ',
     'Nút TP duyệt và Từ chối với phiếu đang ở trạng thái Chờ TP duyệt. Ngoài quyền còn phải '
     'quản lý phòng ban của NGƯỜI NHẬN.'),
    ('Q2', 'Ban giám đốc duyệt hàng giữ',
     'Nút BGĐ duyệt và Từ chối với phiếu đang ở trạng thái Chờ BGĐ duyệt.'),
    ('Q3', 'Kế toán duyệt hàng giữ',
     'Nút KT duyệt và Từ chối với phiếu đang ở trạng thái Chờ KT duyệt. Đây là bước DUY NHẤT '
     'đổi chủ hàng giữ.'),
], widths=[0.8, 2.0, 3.2])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu hàng giữ theo tổng công ty', 'Toàn bộ phiếu của mọi công ty.'),
    ('V2', 'Xem phiếu hàng giữ theo công ty', 'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem phiếu hàng giữ theo phòng ban',
     'Phiếu thuộc các phòng ban mà người đăng nhập được phân công quản lý, cộng phòng ban của '
     'chính người đó.'),
    ('—', '(không có cấp nào)',
     'Chỉ phiếu do chính mình lập, cộng thêm những phiếu đang chờ chính mình duyệt.'),
], widths=[0.8, 2.0, 3.2])

d.p('Ba quy tắc chung áp cho mọi cấp:')
d.bullets([
    'Phiếu ở trạng thái Không duyệt chỉ người lập nhìn thấy.',
    'Người có quyền duyệt được xem mọi phiếu khác trạng thái Không duyệt trong cùng công ty.',
    'Mọi thao tác duyệt / từ chối đều yêu cầu người thực hiện cùng công ty với phiếu.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'V1/V2/V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅', '✅', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột hiển thị', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo mới phiếu', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Chỉnh sửa phiếu', '✅ (phiếu của mình, Không duyệt)', '✅ (nt)', '✅ (nt)', '✅ (nt)',
     '✅ (nt)'),
    ('FR-07 Xem chi tiết phiếu', '✅', '✅', '✅', '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-08 Duyệt phiếu', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '✅ (Chờ KT duyệt)', '❌',
     '❌'),
    ('FR-09 Từ chối phiếu', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '✅ (Chờ KT duyệt)', '❌',
     '❌'),
    ('FR-10 Xóa phiếu', '✅ (phiếu của mình, Không duyệt)', '✅ (nt)', '✅ (nt)', '✅ (nt)',
     '✅ (nt)'),
    ('FR-11 In phiếu / In danh sách', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-12 Xuất Excel danh sách', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-13 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
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
     ('FR-12', 'Xuất Excel danh sách', 'io', 'extend', [0], None),
     ('FR-10', 'Xóa phiếu', 'action', 'extend', [0], None),
     ('FR-14', 'Chọn hàng và lô hàng giữ', 'crud', 'include', [1, 2], None),
     ('FR-15', 'Chọn hợp đồng', 'crud', 'include', [1, 2], None),
     ('FR-08', 'Duyệt phiếu', 'action', 'extend', [3], None),
     ('FR-09', 'Từ chối phiếu', 'action', 'extend', [3], None),
     ('FR-11', 'In phiếu', 'io', 'extend', [3], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [3], None)],
    'Sơ đồ Use Case tổng quan màn Yêu cầu điều chuyển hàng giữ')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách phiếu')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Yêu cầu điều chuyển hàng giữ tại phần mô tả '
           'chi tiết.', anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu yêu cầu điều chuyển hàng giữ',
    mota='Hiển thị bảng phiếu nằm trong phạm vi dữ liệu của người đăng nhập, kèm bộ lọc, '
         'phân trang và ô thống kê tổng số phiếu khớp bộ lọc.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng vào menu Tài chính → Giữ hàng → Phiếu Yêu cầu điều chuyển hàng giữ.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem của người dùng.\n'
          '3. Hệ thống bổ sung vào phạm vi những phiếu đang chờ chính người dùng duyệt.\n'
          '4. Hệ thống trả về trang đầu tiên của danh sách và tổng số phiếu.\n'
          '5. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Phiếu ở trạng thái Không duyệt của người khác không xuất hiện trong danh sách.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Yêu cầu điều chuyển hàng giữ lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Yêu cầu điều chuyển hàng giữ',
     'Tiêu đề cố định phía trên bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Mở màn lập phiếu mới.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở màn in danh sách theo đúng bộ lọc đang áp.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ chọn trường xuất; bị khóa trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục', 'Cột cố định.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'ĐCHG-NNNNN', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết. Cột cố định, sắp xếp được.'),
    ('Cột Người tạo / Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Cột Ngày tạo sắp xếp được.'),
    ('Cột Người nhận', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Nhân viên sẽ đứng tên giữ hàng sau khi phiếu được duyệt.'),
    ('Cột Khách nhận', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Khách hàng sẽ được giữ hàng sau khi phiếu được duyệt.'),
    ('Cột Trạng thái', 'Badge', 'Read-only',
     'Chờ TP duyệt / Chờ BGĐ duyệt / Chờ KT duyệt / Đã duyệt / Không duyệt', 'Theo dữ liệu',
     'Ba trạng thái chờ duyệt màu cam; Đã duyệt màu xanh lá; Không duyệt màu đỏ.'),
    ('Cột Người duyệt / Ngày duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Bước duyệt gần nhất. Cột Ngày duyệt sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật / Phòng ban / Ghi chú / Lý do không duyệt',
     'Table/Grid', 'Read-only', '–', 'Ẩn mặc định', 'Bật lên trong cửa sổ Tuỳ chỉnh cột.'),
    ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Cột cố định cuối bảng, chứa các nút thao tác của dòng.'),
    ('Nút Sửa / Xóa', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện với phiếu do chính mình lập và đang ở trạng thái Không duyệt.'),
    ('Nút Duyệt', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện khi phiếu đang chờ chính người dùng duyệt ở đúng cấp của mình; điều hướng sang '
     'màn chi tiết.'),
    ('Nút In / Lịch sử', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'In mở màn in phiếu; Lịch sử mở cửa sổ lịch sử thay đổi.'),
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
     'During:\n– Áp phạm vi dữ liệu; bổ sung các phiếu đang chờ chính người dùng duyệt.\n'
     '– Khôi phục bộ lọc đã lưu của người dùng nếu còn hiệu lực (10 phút).\n'
     'After:\n– Trả về trang 1, tổng số phiếu và danh sách trạng thái để đổ vào ô lọc.'),
    ('Bấm vào mã phiếu', 'Click',
     'Before:\n– Kiểm tra người dùng có được xem phiếu này không.\n'
     '– Nếu không → hệ thống báo không có quyền xem phiếu và không mở màn chi tiết.\n'
     'After:\n– Mở màn chi tiết của phiếu.'),
    ('Bấm tiêu đề cột có mũi tên sắp xếp', 'Click',
     'During:\n– Chỉ ba cột Mã phiếu, Ngày tạo, Ngày duyệt sắp xếp được.\n'
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
    ten='Tìm kiếm và lọc danh sách phiếu',
    mota='Thu hẹp danh sách theo mã phiếu, trạng thái, người nhận, khách nhận, người tạo, '
         'người duyệt, hàng hóa, số hợp đồng, khoảng ngày tạo và khối công ty – phòng ban.',
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
    dacbiet='Ô lọc “Số hợp đồng” là bổ sung riêng của hệ thống mới; bản cũ có xử lý điều kiện '
            'này nhưng không dựng ô lọc tương ứng.')

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
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Trống', '–'),
    ('Người nhận', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống',
     'Lọc theo nhân viên sẽ nhận hàng giữ.'),
    ('Khách nhận', 'Dropdown', 'Enable', 'Danh sách khách hàng', 'Trống',
     'Lọc theo khách hàng sẽ được giữ hàng.'),
    ('Người tạo / Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', '–'),
    ('Tên, mã hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Một ô lọc chung cho cả tên và mã hàng hóa.'),
    ('Số hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Lọc theo số hợp đồng gắn ở dòng hàng.'),
    ('Ngày tạo từ / Ngày tạo đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống',
     'Lọc theo khoảng ngày lập phiếu.'),
], required=False)

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'During:\n– Ghi giá trị mới vào bộ tiêu chí đang áp.\n'
     'After:\n– Về trang 1 và nạp lại danh sách ngay, không cần bấm nút.'),
    ('Bấm nút Tìm kiếm', 'Click',
     'After:\n– Áp thêm nội dung ô tìm nhanh, về trang 1 và nạp lại danh sách.'),
    ('Bấm nút Làm mới', 'Click',
     'During:\n– Đặt lại mọi ô lọc về trống và bỏ thứ tự sắp xếp.\n'
     'After:\n– Nạp lại danh sách từ trang 1 theo phạm vi quyền.'),
    ('Lọc theo Số hợp đồng', 'Change',
     'After:\n– Chỉ giữ những phiếu có ít nhất một dòng hàng gắn hợp đồng khớp số đã nhập.\n'
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
    dacbiet='Màn này có nhiều ô lọc hơn hai màn cùng nhóm nên cài đặt bộ lọc đặc biệt hữu ích.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('07-cai-dat-bo-loc.png'),
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
    dacbiet='Năm cột Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú và Lý do không duyệt '
            'mặc định TẮT.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột hiển thị', shot=shot('08-cau-hinh-cot.png'),
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
d.h3('2.5 Tạo mới phiếu')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Tạo mới phiếu yêu cầu điều chuyển hàng giữ', 'crud',
            [('include', 'Chọn hàng hóa đang giữ của người lập'),
             ('include', 'Chọn lô hàng giữ nguồn'),
             ('include', 'Sinh mã phiếu tự động'),
             ('extend', 'Chọn hợp đồng cho dòng hàng'),
             ('extend', 'Đính kèm tệp')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-05 Tạo mới phiếu')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới phiếu yêu cầu điều chuyển hàng giữ',
    mota='Lập phiếu đề nghị chuyển hàng đang giữ của chính mình sang một nhân viên nhận và một '
         'khách hàng nhận khác.',
    tacnhan='Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Người lập đang giữ ít nhất một lô hàng còn hàng và chưa hết hạn giữ.',
    chinh='1. Người dùng bấm nút Tạo mới ở màn danh sách.\n'
          '2. Người dùng chọn Người nhận và Khách hàng nhận.\n'
          '3. Người dùng bấm Thêm hàng hóa để chọn hàng mình đang giữ.\n'
          '4. Với mỗi dòng, người dùng chọn lô nguồn ở ô “Từ xuất giữ” và nhập Số lượng chuyển.\n'
          '5. Người dùng chọn Hợp đồng cho dòng hàng nếu cần.\n'
          '6. Người dùng bấm Gửi duyệt.\n'
          '7. Hệ thống kiểm tra dữ liệu, sinh mã phiếu và ghi phiếu ở trạng thái Chờ TP duyệt.\n'
          '8. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Màn hình KHÔNG có nút Lưu nháp: lập phiếu là vào thẳng bước chờ Trưởng phòng duyệt.\n'
        '• Chưa chọn lô nguồn → báo lỗi tại dòng, không lưu.\n'
        '• Lô đã chọn ở dòng khác → báo lỗi nêu rõ đã được chọn ở dòng nào.\n'
        '• Lô đã hết hạn giữ → báo lỗi nêu rõ ngày hết hạn, không lưu.\n'
        '• Số lượng vượt số đang giữ của lô → báo lỗi, không lưu.\n'
        '• Rời màn khi đã nhập mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
    dacbiet='Hạn giữ của hàng sau khi chuyển lấy theo LÔ NGUỒN, không phải theo phiếu. '
            'Điều chuyển không kéo dài thời gian giữ hàng.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('05-sua-phieu.png'),
         shot_caption='Màn lập phiếu yêu cầu điều chuyển hàng giữ (bố cục dùng chung với màn Sửa)')
d.layout(menu=MENU + ' => Tạo mới => Thêm hàng hóa', shot=shot('06-popup-chon-hang.png'),
         shot_caption='Popup Hàng bạn đang giữ')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Người lập – Ngày lập', 'Label', 'Read-only', '–', '–',
     'Người đăng nhập – ngày hiện tại', 'Hiển thị ở góc phải khối Thông tin chung.'),
    ('Người nhận', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Có', 'Trống',
     'Nhân viên sẽ đứng tên giữ hàng sau khi phiếu được duyệt.'),
    ('Khách hàng nhận', 'Dropdown', 'Enable', 'Danh sách khách hàng', 'Có', 'Trống',
     'Khách hàng sẽ được giữ hàng sau khi phiếu được duyệt.'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Chọn tệp đính kèm', 'Button', 'Enable',
     'PDF, ảnh, Word, Excel; tối đa 13 MB mỗi tệp', 'Không', 'Chưa có tệp',
     'Chọn được nhiều tệp; mỗi tệp có nút gỡ khỏi phiếu.'),
    ('Nút Thêm hàng hóa', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở popup liệt kê hàng mà chính người lập đang giữ, không giới hạn theo khách hàng.'),
    ('Cột Tên hàng hóa / Mã hàng hóa', 'Table/Grid', 'Read-only', '–', '–',
     'Theo hàng hóa đã chọn', 'Không sửa được.'),
    ('Cột ĐVT', 'Table/Grid', 'Read-only', '–', '–', 'Đơn vị cơ bản',
     'Có biểu tượng ⓘ giải thích vì sao không đổi được đơn vị.'),
    ('Cột Từ xuất giữ', 'Dropdown', 'Enable', 'Danh sách lô hàng giữ của người lập', 'Có',
     'Trống', 'Hiển thị dạng số lượng – hạn giữ. Có nút tìm kiếm lô bên cạnh.'),
    ('Cột Có thể giữ', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo tồn kho',
     'Tồn kho khả dụng; có biểu tượng ⓘ phân biệt với cột Đang giữ.'),
    ('Cột Đang giữ', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo lô nguồn',
     'Là liên kết mở cửa sổ lịch sử biến động của lô đó.'),
    ('Cột Chuyển', 'Number', 'Enable', '> 0 và ≤ Đang giữ, tối đa 6 chữ số', 'Có', 'Trống',
     'Số lượng chuyển sang người nhận. Nhập sai thì báo đỏ tại dòng và giữ nguyên số đã gõ.'),
    ('Cột Hạn giữ', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', '–', 'Theo lô nguồn',
     'Hạn giữ giữ nguyên sau khi chuyển.'),
    ('Cột Hợp đồng', 'Textbox', 'Enable', '–', 'Không', 'Trống',
     'Chọn từ popup hợp đồng bằng nút tìm kiếm bên cạnh.'),
    ('Nút xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Bỏ hẳn dòng hàng khỏi phiếu.'),
    ('Nút Gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu phiếu và chuyển thẳng sang trạng thái Chờ TP duyệt.'),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Chỉ có ở màn Tạo mới: lưu rồi ở lại để lập phiếu kế tiếp.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi tại ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi; không tự sửa giá trị người dùng đã nhập.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Thêm hàng hóa', 'Click',
     'During:\n– Popup liệt kê hàng mà chính người lập đang giữ cho MỌI khách hàng.\n'
     '– Các hàng đã có trong phiếu được loại khỏi danh sách.\n'
     'After:\n– Các dòng được tích sẽ được thêm vào bảng Chi tiết.'),
    ('Chọn lô ở ô Từ xuất giữ', 'Change',
     'During:\n– Chỉ liệt kê lô do chính người lập đang giữ, còn hàng.\n'
     'After:\n– Điền số Đang giữ và Hạn giữ của lô đã chọn vào dòng.'),
    ('Nhập Số lượng chuyển', 'Change / Blur',
     'During:\n– Chỉ nhận ký tự số.\n– Bằng 0 → báo “Số lượng chuyển – Phải lớn hơn 0.”.\n'
     '– Vượt số đang giữ → báo “Số lượng chuyển – Không được vượt số đang giữ (…)”.\n'
     'After:\n– Giữ nguyên giá trị người dùng đã gõ, không tự kéo về mức trần.'),
    ('Bấm Gửi duyệt', 'Click',
     'Before:\n– Không yêu cầu quyền riêng; ai đăng nhập cũng lập được phiếu của mình.\n'
     'During:\n– Người nhận hoặc Khách hàng nhận trống → hiển thị “Bắt buộc phải chọn”.\n'
     '– Chưa có dòng hàng nào → hiển thị “Bắt buộc phải chọn”.\n'
     '– Lô nguồn không thuộc người lập → hiển thị “Từ xuất giữ – Lô hàng giữ không còn tồn tại '
     'hoặc không thuộc người lập phiếu.”.\n'
     '– Lô đã chọn ở dòng khác → hiển thị “Từ xuất giữ – Lô hàng giữ này đã được chọn ở dòng …”.\n'
     '– Lô đã hết hạn → hiển thị “Từ xuất giữ – Lô hàng đã hết hạn giữ ngày …”.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Sinh mã phiếu dạng ĐCHG-NNNNN, ghi phiếu ở trạng thái Chờ TP duyệt.\n'
     '– Gửi thông báo cho Trưởng phòng quản lý phòng ban của NGƯỜI NHẬN.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.6
d.h3('2.6 Chỉnh sửa phiếu')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Chỉnh sửa phiếu yêu cầu điều chuyển hàng giữ', 'crud',
            [('include', 'Kiểm tra phiếu do chính mình lập và đang ở trạng thái Không duyệt'),
             ('extend', 'Đặt lại toàn bộ các bước duyệt')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-06 Chỉnh sửa phiếu')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Chỉnh sửa phiếu yêu cầu điều chuyển hàng giữ',
    mota='Sửa lại phiếu đã bị cấp duyệt trả về, sau đó gửi duyệt lại từ đầu.',
    tacnhan='Nhân viên kinh doanh — người lập phiếu',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Không duyệt.',
    chinh='1. Người dùng bấm nút Sửa ở màn danh sách hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở màn sửa với dữ liệu đã lưu của phiếu.\n'
          '3. Người dùng chỉnh sửa theo lý do bị trả về.\n'
          '4. Người dùng bấm Gửi duyệt.\n'
          '5. Hệ thống đặt lại toàn bộ các bước duyệt và đưa phiếu về Chờ TP duyệt.',
    phu='• Phiếu đang chờ duyệt hoặc đã duyệt → nút Sửa không hiển thị; mở thẳng bằng đường dẫn '
        'thì hệ thống từ chối.\n'
        '• Phiếu của người khác → hệ thống từ chối.\n'
        '• Các nhánh lỗi nhập liệu giống chức năng Tạo mới.',
    dacbiet='⚠ Đây là điểm KHÁC hai màn cùng nhóm: màn này không có trạng thái nháp, nên chỉ '
            'phiếu bị Không duyệt mới sửa lại được.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('05-sua-phieu.png'),
         shot_caption='Màn sửa phiếu bị trả về, trạng thái hiển thị nhãn đỏ Không duyệt')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mã phiếu', 'Textbox', 'Disable', 'ĐCHG-NNNNN', '–', 'Theo dữ liệu',
     'Chỉ hiển thị, không sửa được.'),
    ('Trạng thái', 'Badge', 'Read-only', '–', '–', 'Không duyệt', 'Nhãn màu đỏ.'),
    ('Phòng ban yêu cầu', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu',
     'Phòng ban của người lập tại thời điểm lập phiếu.'),
    ('Người nhận / Khách hàng nhận', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Theo dữ liệu',
     'Sửa lại được.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu đã lưu',
     'Các dòng đã lưu được nạp sẵn kèm lô nguồn, số lượng và hợp đồng.'),
    ('Nút Gửi duyệt / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Màn sửa không có nút Lưu và tiếp tục.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System',
     'Before:\n– Kiểm tra phiếu do chính người dùng lập và đang ở trạng thái Không duyệt.\n'
     '– Nếu không → hệ thống từ chối và không mở màn sửa.\n'
     'After:\n– Nạp dữ liệu phiếu kèm các lô nguồn đã chọn.'),
    ('Bấm Gửi duyệt', 'Click',
     'During:\n– Kiểm tra dữ liệu giống chức năng Tạo mới.\n'
     'After:\n– ĐẶT LẠI toàn bộ ba bước duyệt Trưởng phòng, Ban giám đốc và Kế toán.\n'
     '– Đưa phiếu về trạng thái Chờ TP duyệt và thông báo cho Trưởng phòng của người nhận.\n'
     '– Ghi một dòng lịch sử “Chỉnh sửa”, nêu rõ những giá trị đã thay đổi.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.7
d.h3('2.7 Xem chi tiết phiếu')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu yêu cầu điều chuyển hàng giữ',
    mota='Hiển thị toàn bộ thông tin phiếu ở chế độ chỉ đọc: thông tin chung, tệp đính kèm, '
         'bảng hàng hóa, lịch sử duyệt và lịch sử thay đổi.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Người dùng nằm trong phạm vi được xem phiếu.',
    chinh='1. Người dùng bấm vào mã phiếu ở màn danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống hiển thị màn chi tiết ở chế độ chỉ đọc.\n'
          '4. Các nút thao tác ở cuối màn hiện theo đúng quyền và trạng thái của phiếu.',
    phu='• Không đủ quyền xem → hệ thống báo không có quyền xem phiếu này.\n'
        '• Phiếu Không duyệt của người khác → không mở được.\n'
        '• Bấm vào số ở cột Đang giữ → mở cửa sổ lịch sử biến động của lô hàng giữ đó.',
    dacbiet=None)

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('03-chi-tiet.png'),
         shot_caption='Màn chi tiết phiếu ở chế độ chỉ đọc')

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–',
     'Chi tiết yêu cầu điều chuyển hàng giữ: <mã phiếu>', '–'),
    ('Khối Thông tin chung', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm Mã phiếu, Trạng thái, Phòng ban yêu cầu, Người nhận, Khách hàng nhận, Ghi chú, người '
     'lập và ngày lập.'),
    ('Khối File đính kèm', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Danh sách tệp mở xem được; không có tệp thì hiện “Chưa có tệp đính kèm”.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cột STT, Tên hàng hóa, Mã hàng hóa, ĐVT, Từ xuất giữ, Có thể giữ, Số lượng (gồm hai '
     'cột con Đang giữ và Chuyển), Hạn giữ và Hợp đồng.'),
    ('Khối Lịch sử duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cột Cấp duyệt, Người duyệt, Thời gian và Ghi chú; hiển thị đủ mọi dòng đã duyệt kể cả '
     'khi không có ghi chú.'),
    ('Khối Lịch sử thay đổi', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Chỉ nạp dữ liệu khi người dùng bấm Xem lịch sử.'),
    ('Nút thao tác cuối màn', 'Button', 'Enable / Ẩn', '–', 'Theo quyền và trạng thái',
     'Gồm nút duyệt của cấp hiện tại, Sửa, Xóa, In, Từ chối và Quay lại; nút không dùng được '
     'thì ẩn hẳn.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu theo phạm vi dữ liệu và quyền duyệt.\n'
     '– Không đủ quyền → báo không có quyền xem phiếu này.\n'
     'After:\n– Hiển thị dữ liệu phiếu và các nút thao tác hợp lệ.'),
    ('Bấm vào số ở cột Đang giữ', 'Click',
     'After:\n– Mở cửa sổ lịch sử biến động của lô hàng giữ đó.'),
    ('Bấm Xem lịch sử ở khối Lịch sử thay đổi', 'Click',
     'After:\n– Nạp và hiển thị danh sách mốc thay đổi của phiếu, mới nhất trước.'),
])

# ------------------------------------------------------------ 2.8
d.h3('2.8 Duyệt phiếu')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Duyệt phiếu yêu cầu điều chuyển hàng giữ', 'action',
            [('include', 'Kiểm tra quyền duyệt đúng cấp và cùng công ty'),
             ('include', 'Kiểm tra tồn hàng giữ còn đủ'),
             ('extend', 'Xác định có phải qua Ban giám đốc hay không'),
             ('extend', 'Đổi chủ hàng giữ sang người nhận và khách nhận')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-08 Duyệt phiếu')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Duyệt phiếu yêu cầu điều chuyển hàng giữ',
    mota='Ký duyệt phiếu ở một trong ba cấp Trưởng phòng, Ban giám đốc, Kế toán. Bước Kế toán '
         'duyệt là bước duy nhất đổi chủ hàng giữ.',
    tacnhan='Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Phiếu đang ở đúng trạng thái chờ cấp đó duyệt; người duyệt có quyền tương ứng và '
             'cùng công ty với phiếu.',
    chinh='1. Người duyệt mở màn chi tiết phiếu.\n'
          '2. Người duyệt xem lại các dòng hàng và số lượng chuyển.\n'
          '3. Người duyệt bấm nút duyệt của cấp mình.\n'
          '4. Hệ thống kiểm tra quyền, trạng thái và dữ liệu dòng hàng.\n'
          '5. Hệ thống chuyển phiếu sang bước tiếp theo, ghi lịch sử và gửi thông báo.\n'
          '6. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Trưởng phòng duyệt: nếu phiếu thuộc diện phải qua Ban giám đốc thì chuyển sang '
        'Chờ BGĐ duyệt, ngược lại chuyển thẳng sang Chờ KT duyệt.\n'
        '• Ban giám đốc duyệt → chuyển sang Chờ KT duyệt.\n'
        '• Kế toán duyệt → phiếu chuyển sang Đã duyệt và hệ thống đổi chủ hàng giữ.\n'
        '• Phiếu đã được người khác xử lý trước đó → báo “Phiếu không ở trạng thái chờ duyệt.”.\n'
        '• Người dùng không đúng cấp → báo “Bạn không có quyền duyệt bước này.”.',
    dacbiet='⚠ Trưởng phòng duyệt xét theo phòng ban của NGƯỜI NHẬN, không phải phòng ban của '
            'người lập phiếu. Đây là điểm khác so với màn Yêu cầu gia hạn hàng giữ.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Duyệt', shot=shot('03-chi-tiet.png'),
         shot_caption='Nút duyệt của cấp hiện tại nằm ở cuối màn chi tiết')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút duyệt của cấp hiện tại', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Nhãn nêu rõ cấp đang ký: TP duyệt / BGĐ duyệt / KT duyệt. Chú thích khi rê chuột nói rõ '
     'phiếu sẽ đi đâu tiếp; riêng bước Kế toán ghi rõ đây là bước ghi tồn hàng giữ.'),
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện cùng lúc với nút duyệt của cấp đó. Nhãn nút là “Từ chối”, trong khi trạng thái '
     'phiếu sau đó hiển thị là “Không duyệt”.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người duyệt KHÔNG sửa được số lượng và lô nguồn.'),
], required=False)

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút duyệt của cấp hiện tại', 'Click',
     'Before:\n– Kiểm tra quyền duyệt đúng cấp và cùng công ty với phiếu.\n'
     '– Trưởng phòng còn phải quản lý phòng ban của NGƯỜI NHẬN.\n'
     '– Nếu không → hiển thị “Bạn không có quyền duyệt bước này.” và dừng xử lý.\n'
     'During:\n– Phiếu không còn ở trạng thái chờ duyệt → hiển thị “Phiếu không ở trạng thái '
     'chờ duyệt.”.\n'
     '– Lô nguồn không còn đủ số lượng → báo lỗi và dừng.\n'
     'After:\n– Ghi lại người duyệt, thời điểm duyệt và ghi chú của cấp đó.\n'
     '– Trưởng phòng duyệt: chuyển sang Chờ BGĐ duyệt hoặc Chờ KT duyệt tuỳ điều kiện; hiển '
     'thị “Yêu cầu đã được chuyển đến Ban giám đốc.” hoặc “Yêu cầu đã được chuyển đến Kế toán.”.\n'
     '– Kế toán duyệt: chuyển phiếu sang Đã duyệt, trừ số lượng ở lô nguồn và cộng vào lô của '
     'người nhận với khách nhận, giữ nguyên hạn giữ của lô nguồn.\n'
     '– Ghi một dòng lịch sử “Duyệt”; gửi thông báo cho cấp kế tiếp hoặc cho người lập.\n'
     '– Hiển thị “Duyệt phiếu thành công.” và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.9
d.h3('2.9 Từ chối phiếu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Từ chối phiếu yêu cầu điều chuyển hàng giữ', 'action',
            [('include', 'Kiểm tra quyền duyệt đúng cấp'),
             ('include', 'Bắt buộc nhập lý do')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-09 Từ chối phiếu')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Từ chối phiếu yêu cầu điều chuyển hàng giữ',
    mota='Trả phiếu về cho người lập kèm lý do. Phiếu chuyển sang trạng thái Không duyệt — đây '
         'cũng là trạng thái duy nhất cho phép người lập sửa lại phiếu.',
    tacnhan='Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Phiếu đang ở đúng trạng thái chờ cấp đó duyệt.',
    chinh='1. Người duyệt bấm nút Từ chối ở màn chi tiết.\n'
          '2. Hệ thống mở cửa sổ nhập lý do.\n'
          '3. Người duyệt nhập lý do.\n'
          '4. Người duyệt bấm nút xác nhận.\n'
          '5. Hệ thống chuyển phiếu sang trạng thái Không duyệt, ghi lý do và gửi thông báo cho '
          'người lập.',
    phu='• Bỏ trống lý do → báo bắt buộc nhập, cửa sổ không đóng.\n'
        '• Lý do quá 255 ký tự → báo “Không được vượt quá 255 ký tự”.\n'
        '• Phiếu đã được xử lý trước đó → báo phiếu không ở trạng thái chờ duyệt.',
    dacbiet='Nhãn nút là “Từ chối” theo bộ chữ chuẩn của hệ thống, còn tên trạng thái hiển thị '
            'là “Không duyệt” theo dữ liệu nghiệp vụ. Đây là khác biệt có chủ ý.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Từ chối', shot=shot('11-popup-tu-choi.png'),
         shot_caption='Cửa sổ Từ chối yêu cầu điều chuyển hàng giữ')
d.layout(menu=MENU + ' => Sửa', shot=shot('05-sua-phieu.png'),
         shot_caption='Phiếu sau khi bị từ chối mang trạng thái Không duyệt và sửa lại được')
d.p('Cửa sổ Từ chối được mở ngay trên màn chi tiết theo đường dẫn ở trên.')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Từ chối yêu cầu điều chuyển hàng giữ',
     'Kèm dòng phụ hiển thị mã phiếu.'),
    ('Lý do', 'Textarea', 'Enable', '0–255 ký tự', 'Trống',
     'Gợi ý nhập lý do trả lại phiếu cho người lập. Bắt buộc nhập.'),
    ('Nút xác nhận', 'Button', 'Enable', '–', 'Hiển thị', 'Bị khóa trong lúc đang xử lý.'),
    ('Nút đóng cửa sổ', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng và bỏ nội dung đã nhập.'),
], required=False)

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Từ chối', 'Click',
     'Before:\n– Kiểm tra người dùng đang ở đúng cấp duyệt của phiếu.\n'
     '– Nếu không → hiển thị “Bạn không có quyền từ chối phiếu này.”.\n'
     'After:\n– Mở cửa sổ nhập lý do.'),
    ('Bấm xác nhận từ chối', 'Click',
     'During:\n– Lý do trống → hiển thị thông báo bắt buộc nhập, cửa sổ không đóng.\n'
     '– Lý do quá 255 ký tự → hiển thị “Không được vượt quá 255 ký tự”.\n'
     'After:\n– Chuyển phiếu sang trạng thái Không duyệt và ghi lý do.\n'
     '– ⚠ Hàng giữ KHÔNG thay đổi.\n'
     '– Ghi một dòng lịch sử; gửi thông báo cho người lập phiếu.\n'
     '– Hiển thị thông báo thành công và nạp lại danh sách.'),
])

# ------------------------------------------------------------ 2.10
d.h3('2.10 Xóa phiếu')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu yêu cầu điều chuyển hàng giữ', 'action',
            [('include', 'Kiểm tra phiếu do chính mình lập và đang ở trạng thái Không duyệt')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa và Thông báo.', anchor='delete')
d.intro_table(
    ten='Xóa phiếu yêu cầu điều chuyển hàng giữ',
    mota='Xóa hẳn một phiếu đang ở trạng thái Không duyệt do chính người dùng lập.',
    tacnhan='Nhân viên kinh doanh — người lập phiếu',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Không duyệt.',
    chinh='1. Người dùng bấm nút Xóa ở cột Hành động hoặc ở màn chi tiết.\n'
          '2. Hệ thống hiển thị hộp thoại xác nhận kèm mã phiếu.\n'
          '3. Người dùng chọn Xóa.\n'
          '4. Hệ thống xóa phiếu và nạp lại danh sách.',
    phu='• Chọn Hủy → đóng hộp thoại, không xóa gì.\n'
        '• Phiếu đang chờ duyệt hoặc đã duyệt → nút Xóa không hiển thị; gọi thẳng chức năng xóa '
        'thì hệ thống từ chối.',
    dacbiet='Phiếu đã duyệt không xóa được vì đã đổi chủ hàng giữ.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('12-xac-nhan-xoa.png'),
         shot_caption='Hộp thoại Xác nhận xóa phiếu')
d.p('Hộp thoại xác nhận xóa được mở ngay trên màn danh sách theo đường dẫn ở trên.')

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
     'Before:\n– Kiểm tra phiếu do chính mình lập và đang ở trạng thái Không duyệt.\n'
     '– Nếu không → nút không hiển thị; gọi thẳng chức năng thì hệ thống từ chối.\n'
     'After:\n– Mở hộp thoại xác nhận.'),
    ('Xác nhận Xóa', 'Click',
     'After:\n– Xóa phiếu; các dòng hàng của phiếu được giữ lại phục vụ tra cứu lịch sử.\n'
     '– Hiển thị thông báo xóa thành công và nạp lại danh sách.'),
])

# ------------------------------------------------------------ 2.11
d.h3('2.11 In phiếu và In danh sách')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'In phiếu và In danh sách', 'io',
            [('extend', 'In một phiếu'),
             ('extend', 'In danh sách theo bộ lọc đang áp')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-11 In phiếu và In danh sách')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc màn In và Xuất dữ liệu.', anchor='excel')
d.intro_table(
    ten='In phiếu yêu cầu điều chuyển hàng giữ và in danh sách',
    mota='Mở bản xem trước để in một phiếu, hoặc in toàn bộ danh sách theo đúng bộ lọc '
         'đang áp dụng.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Với bản in phiếu: người dùng xem được phiếu đó.',
    chinh='1. Người dùng bấm nút In ở cột Hành động, ở màn chi tiết, hoặc nút In ở thanh công '
          'cụ danh sách.\n'
          '2. Hệ thống mở tab mới hiển thị bản xem trước đúng khổ giấy.\n'
          '3. Người dùng bấm nút In trên bản xem trước để gửi lệnh in.',
    phu='• Cả bản in phiếu và bản in danh sách đều dùng khổ A4 ngang.\n'
        '• Bản in danh sách in đúng phạm vi và điều kiện lọc đang áp, gồm cả ô lọc Số hợp đồng.',
    dacbiet='Phần đầu bản in lấy theo công ty ghi trên phiếu, không lấy theo người đang in. '
            'Bảng lịch sử duyệt trên bản in in đủ mọi dòng đã duyệt, kể cả dòng không có ghi chú.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In phiếu', shot=shot('04-in-phieu.png'),
         shot_caption='Bản in phiếu yêu cầu điều chuyển hàng giữ')
d.layout(menu=MENU + ' => In danh sách', shot=shot('10-in-danh-sach.png'),
         shot_caption='Bản in danh sách phiếu yêu cầu điều chuyển hàng giữ')

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In trên bản xem trước', 'Button', 'Enable', '–', 'Hiển thị',
     'Nằm phía trên, canh phải mép giấy.'),
    ('Phần đầu chứng từ', 'Label', 'Read-only', '–', 'Theo công ty của phiếu',
     'Gồm logo và thông tin liên hệ của công ty ghi trên phiếu.'),
    ('Khối thông tin phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người yêu cầu, Phòng ban, Người nhận, Trạng thái.'),
    ('Bảng hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cột STT, Tên hàng hóa, Mã hàng hóa, ĐVT, Từ xuất giữ, Đang giữ, Chuyển, Hạn giữ, '
     'Hợp đồng và dòng Tổng cộng.'),
    ('Bảng lịch sử duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Bốn cột Cấp duyệt, Người duyệt, Thời gian và Ghi chú.'),
    ('Khối ký tên', 'Label', 'Read-only', '–', 'Hiển thị',
     'Bốn ô ký: Người lập, Trưởng phòng, Ban giám đốc, Kế toán.'),
    ('Bản in danh sách', 'Table/Grid', 'Read-only', '–', 'Theo bộ lọc',
     'Có dòng Tổng số phiếu và các cột STT, Mã phiếu, Người tạo, Ngày tạo, Người nhận, '
     'Khách nhận, Trạng thái, Người duyệt, Ngày duyệt.'),
], required=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In ở dòng hoặc ở màn chi tiết', 'Click',
     'After:\n– Mở tab mới hiển thị bản in của đúng phiếu đó.'),
    ('Bấm nút In ở thanh công cụ danh sách', 'Click',
     'After:\n– Mở tab mới hiển thị bản in danh sách theo đúng bộ lọc đang áp.'),
])

# ------------------------------------------------------------ 2.12
d.h3('2.12 Xuất Excel danh sách')

d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Xuất Excel danh sách phiếu', 'io',
            [('include', 'Chọn trường cần xuất'),
             ('include', 'Lấy dữ liệu theo bộ lọc đang áp')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-12 Xuất Excel danh sách')

d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách phiếu',
    mota='Xuất danh sách phiếu ra tệp Excel. Người dùng tự chọn các trường cần xuất và thứ tự '
         'cột trong tệp chạy theo đúng thứ tự đã chọn.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ Chọn trường xuất Excel với 13 trường, mặc định chọn hết.\n'
          '3. Người dùng bỏ chọn các trường không cần.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống lấy toàn bộ dữ liệu khớp bộ lọc và tải tệp về máy.',
    phu='• Trong lúc đang xuất, nút bị khóa để tránh bấm nhiều lần.\n'
        '• Xuất thất bại → hiển thị thông báo lỗi, không tải tệp.',
    dacbiet='Tệp xuất chứa toàn bộ dòng khớp bộ lọc trong phạm vi quyền, không giới hạn ở trang '
            'đang xem.')

d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('09-chon-truong-xuat-excel.png'),
         shot_caption='Cửa sổ Chọn trường xuất Excel')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất Excel', '–'),
    ('Ô chọn trường xuất', 'Dropdown', 'Enable', '13 trường', 'Có', 'Chọn hết 13 trường',
     'Mã phiếu, Người tạo, Ngày tạo, Người nhận, Khách nhận, Trạng thái, Người duyệt, '
     'Ngày duyệt, Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do không duyệt.'),
    ('Dòng xem trước thứ tự cột', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn',
     'Liệt kê thứ tự cột sẽ có trong tệp.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Bị khóa trong lúc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
])

d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xuất Excel', 'Click', 'After:\n– Mở cửa sổ chọn trường xuất.'),
    ('Bấm Xuất file', 'Click',
     'During:\n– Lấy dữ liệu theo đúng bộ lọc và phạm vi quyền hiện tại.\n'
     'After:\n– Dựng tệp Excel theo thứ tự trường đã chọn và tải về máy.\n'
     '– Hiển thị thông báo xuất thành công và đóng cửa sổ.'),
])

# ------------------------------------------------------------ 2.13
d.h3('2.13 Xem lịch sử thay đổi')

d.p('2.13.1 Giới thiệu')
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
    dacbiet=None)

d.p('2.13.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Lịch sử', shot=shot('03-chi-tiet.png'),
         shot_caption='Khối Lịch sử thay đổi ở cuối màn chi tiết')

d.p('2.13.3 Mô tả chi tiết giao diện')
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

d.p('2.13.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xem lịch sử', 'Click',
     'After:\n– Nạp danh sách mốc thay đổi và hiển thị, mới nhất trước.'),
    ('Bấm Làm mới', 'Click', 'After:\n– Nạp lại danh sách mốc thay đổi.'),
])

# ==================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu điều chuyển hàng giữ; không '
           'lặp lại các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Màn hình không có trạng thái nháp', [
        '– Lập phiếu là vào thẳng trạng thái Chờ TP duyệt; không có nút Lưu nháp.',
        '– Chỉ phiếu ở trạng thái Không duyệt mới sửa hoặc xóa lại được.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xóa']),
    ('BR-02', 'Nguồn hàng và lô nguồn', [
        '– Popup chọn hàng chỉ liệt kê hàng mà chính người lập đang giữ, cho mọi khách hàng.',
        '– Ô “Từ xuất giữ” chỉ liệt kê lô do chính người lập đang giữ và còn hàng.',
        '– Mỗi lô chỉ được chọn ở MỘT dòng; chọn trùng thì báo lỗi nêu rõ đã chọn ở dòng nào.',
        '– Lô đã hết hạn giữ không được chọn; hệ thống báo lỗi kèm ngày hết hạn.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-03', 'Số lượng chuyển', [
        '– Phải lớn hơn 0 và không vượt quá số lượng đang giữ của lô nguồn.',
        '– Tối đa 6 chữ số.',
        '– Nhập sai thì hệ thống báo đỏ ngay tại dòng và giữ nguyên giá trị đã gõ.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-04', 'Người nhận và Khách hàng nhận là bắt buộc', [
        '– Cả hai ô đều bắt buộc chọn khi lập và khi sửa phiếu.',
        '– Đây là hai thông tin quyết định hàng sẽ thuộc về ai sau khi duyệt.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-05', 'Luồng duyệt ba cấp', [
        '– Gửi duyệt đưa phiếu về trạng thái Chờ TP duyệt.',
        '– Trưởng phòng duyệt: phiếu chuyển sang Chờ BGĐ duyệt nếu thuộc diện phải qua Ban '
        'giám đốc, ngược lại chuyển thẳng sang Chờ KT duyệt.',
        '– Ban giám đốc duyệt: chuyển sang Chờ KT duyệt.',
        '– Kế toán duyệt: phiếu chuyển sang Đã duyệt.',
    ], 'Duyệt'),
    ('BR-06', 'Trưởng phòng duyệt xét theo phòng ban NGƯỜI NHẬN', [
        '– Ngoài quyền và điều kiện cùng công ty, Trưởng phòng còn phải quản lý phòng ban của '
        'NGƯỜI NHẬN hàng.',
        '– ⚠ Đây là điểm khác với màn Yêu cầu gia hạn hàng giữ (xét theo phòng ban ghi trên '
        'phiếu).',
        '– Người có vai trò quản trị hệ thống được bỏ qua ràng buộc phòng ban.',
    ], 'Duyệt'),
    ('BR-07', 'Điều kiện phải qua Ban giám đốc', [
        '– Xét từng dòng hàng của phiếu.',
        '– Dòng có gắn hợp đồng: nếu tỉ lệ tiền đã thu trên tổng giá trị hợp đồng thấp hơn '
        'ngưỡng phần trăm cấu hình theo loại hợp đồng của công ty thì phiếu phải qua Ban '
        'giám đốc.',
        '– Dòng không gắn hợp đồng: cộng dồn giá trị hàng chuyển; vượt hạn mức cấu hình của '
        'công ty thì phiếu phải qua Ban giám đốc.',
        '– Chỉ cần một dòng thỏa điều kiện là cả phiếu phải qua Ban giám đốc.',
    ], 'Duyệt'),
    ('BR-08', 'Thời điểm đổi chủ hàng giữ', [
        '– Chỉ bước Kế toán duyệt mới ghi hàng giữ. Hai bước trước đó không đụng tới hàng giữ.',
        '– Hệ thống trừ số lượng ở lô nguồn rồi cộng vào lô của người nhận với khách hàng nhận, '
        'cùng hàng hóa và CÙNG HẠN GIỮ với lô nguồn; chưa có lô đó thì tạo mới.',
        '– Lô đích lấy công ty theo lô nguồn, không lấy theo người đang duyệt.',
        '– Mỗi lần chuyển ghi hai dòng nhật ký biến động: một dòng trừ ở lô nguồn và một dòng '
        'cộng ở lô đích.',
        '– Điều chuyển KHÔNG kéo dài thời gian giữ hàng.',
    ], 'Duyệt'),
    ('BR-09', 'Từ chối phiếu', [
        '– Lý do là bắt buộc, tối đa 255 ký tự.',
        '– Phiếu chuyển sang trạng thái Không duyệt và chỉ người lập nhìn thấy.',
        '– Nhãn nút là “Từ chối” theo bộ chữ chuẩn, tên trạng thái hiển thị là “Không duyệt” '
        'theo dữ liệu nghiệp vụ.',
    ], ['Duyệt', 'Từ chối']),
    ('BR-10', 'Sửa lại phiếu thì đặt lại toàn bộ các bước duyệt', [
        '– Khi người lập sửa và gửi lại, hệ thống xóa dấu duyệt của cả ba cấp.',
        '– Phiếu đi lại quy trình duyệt từ đầu, bắt đầu ở Chờ TP duyệt.',
    ], 'Chỉnh sửa'),
    ('BR-11', 'Phạm vi dữ liệu', [
        '– Áp theo thứ tự ưu tiên: tổng công ty → công ty → phòng ban → chỉ phiếu của mình.',
        '– Người có quyền duyệt được xem thêm mọi phiếu khác trạng thái Không duyệt trong cùng '
        'công ty.',
        '– Phiếu ở trạng thái Không duyệt chỉ người lập nhìn thấy.',
        '– Phạm vi này áp cho cả danh sách, màn chi tiết, bản in và tệp Excel xuất ra.',
    ], 'Toàn màn hình'),
    ('BR-12', 'Đơn vị tính và hợp đồng của dòng hàng', [
        '– Hàng giữ luôn ghi theo đơn vị cơ bản của hàng hóa nên cột ĐVT chỉ hiển thị.',
        '– Hợp đồng của dòng hàng do người lập chọn tay từ popup, không suy tự động từ lô nguồn.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-13', 'Tệp đính kèm', [
        '– Nhận các định dạng PDF, ảnh, Word, Excel.',
        '– Mỗi tệp tối đa 13 MB; đính kèm được nhiều tệp trên một phiếu.',
    ], ['Tạo mới', 'Chỉnh sửa']),
])

d.save()
