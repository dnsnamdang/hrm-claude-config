# -*- coding: utf-8 -*-
"""Sinh SRS man "Yeu cau gia han hang giu" theo FORM CHUAN 2026-08-28.

Nguon: code HRM nhanh `gop_db`
  BE  Modules/Finance/{Entities/PrepickExtend, Services/PrepickExtendRequestService.php,
      Http/Controllers/V1/PrepickExtendRequestController.php,
      Http/Requests/PrepickExtend/*}
  FE  pages/finance/prepick-extend-requests/*
Anh chup that: ./prepick_extend_shots (Playwright MCP, 1440x900, ngay 05/09/2026).
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

SHOTS = os.path.join(BASE, 'prepick_extend_shots')
OUT = os.path.join(BASE, 'SRS - Yeu cau gia han hang giu.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Giữ hàng => Yêu cầu gia hạn hàng giữ'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/prepick-extend-requests',
           full_url='https://<host-hrm>/finance/prepick-extend-requests',
           img_prefix='pghhg_')

# ============================================================== TRANG DAU
d.title_block('Yêu cầu gia hạn hàng giữ')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Yêu cầu gia hạn hàng giữ '
    '(mã phiếu PGHHG), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, luồng duyệt và phân quyền của màn hình.',
    'Làm rõ nguồn dữ liệu dòng hàng: phiếu chỉ liệt kê các lô hàng giữ SẮP HẾT HẠN của '
    'chính người lập phiếu, không phải mọi lô đang giữ.',
    'Làm rõ luồng duyệt 3 cấp và điều kiện rẽ nhánh có phải qua Ban giám đốc hay không.',
    'Làm rõ thời điểm hệ thống thực sự ghi tồn hàng giữ: chỉ khi Kế toán duyệt ở bước cuối.',
    'Làm rõ phạm vi dữ liệu mà mỗi cấp quyền xem được.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên '
                 'kinh doanh đứng tên giữ. Mỗi lô hàng giữ có một hạn giữ riêng.'),
    ('Lô hàng giữ', 'Một dòng tồn hàng giữ, xác định bởi bộ: nhân viên giữ – khách hàng – '
                    'hàng hóa – hạn giữ – công ty.'),
    ('Hạn giữ', 'Ngày cuối cùng lô hàng còn được giữ. Quá ngày này lô bị coi là hết hạn giữ.'),
    ('Hạn giữ mới', 'Ngày hết hạn mà người lập phiếu đề nghị gia hạn tới.'),
    ('Gia hạn hàng giữ', 'Chuyển một phần hoặc toàn bộ số lượng của lô hàng giữ sang một hạn '
                         'giữ mới muộn hơn. Hệ thống trừ số lượng ở lô cũ và cộng vào lô có '
                         'hạn giữ mới.'),
    ('Số ngày cảnh báo', 'Cấu hình chung của hệ thống, hiện là 7 ngày. Chỉ những lô có hạn giữ '
                         'trước “hôm nay + số ngày cảnh báo” mới hiện ra để lập phiếu gia hạn.'),
    ('Số ngày giữ tối đa', 'Cấu hình chung của hệ thống, hiện là 30 ngày. Hạn giữ mới không '
                           'được vượt quá “hôm nay + số ngày giữ tối đa”.'),
    ('TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán — ba cấp duyệt của phiếu.'),
    ('Đang giữ', 'Số lượng còn lại của chính lô hàng giữ đang xem.'),
    ('Có thể giữ', 'Tồn kho khả dụng của hàng hóa trong công ty, cho biết kho còn bao nhiêu để '
                   'giữ tiếp. Đây là con số tham khảo, khác với “Đang giữ”.'),
], widths=[1.6, 4.4])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Màn hình KHÔNG có quyền riêng cho Thêm / Sửa / Xóa: mọi người dùng đã đăng nhập đều lập '
    'được phiếu gia hạn cho hàng giữ của chính mình, và chỉ sửa / xóa được phiếu do chính mình '
    'lập khi phiếu còn ở trạng thái Đang tạo.')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Trưởng phòng duyệt hàng giữ',
     'Nút TP duyệt và Từ chối với phiếu đang ở trạng thái Chờ TP duyệt. Ngoài quyền còn phải '
     'quản lý đúng phòng ban của phiếu.'),
    ('Q2', 'Ban giám đốc duyệt hàng giữ',
     'Nút BGĐ duyệt và Từ chối với phiếu đang ở trạng thái Chờ BGĐ duyệt.'),
    ('Q3', 'Kế toán duyệt hàng giữ',
     'Nút KT duyệt và Từ chối với phiếu đang ở trạng thái Chờ KT duyệt. Đây là bước DUY NHẤT '
     'ghi tồn hàng giữ.'),
], widths=[0.8, 2.0, 3.2])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu hàng giữ theo tổng công ty', 'Toàn bộ phiếu của mọi công ty.'),
    ('V2', 'Xem phiếu hàng giữ theo công ty',
     'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem phiếu hàng giữ theo phòng ban',
     'Phiếu thuộc các phòng ban mà người đăng nhập được phân công quản lý, cộng phòng ban của '
     'chính người đó.'),
    ('—', '(không có cấp nào)',
     'Chỉ phiếu do chính mình lập, cộng thêm những phiếu đang chờ chính mình duyệt.'),
], widths=[0.8, 2.0, 3.2])

d.p('Ba quy tắc chung áp cho mọi cấp:')
d.bullets([
    'Phiếu ở trạng thái Đang tạo là bản nháp, chỉ người lập nhìn thấy và mở được.',
    'Người có quyền duyệt được xem mọi phiếu khác nháp trong cùng công ty với mình.',
    'Mọi thao tác duyệt / từ chối đều yêu cầu người thực hiện cùng công ty với phiếu.',
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
    ('FR-08 Duyệt phiếu', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '✅ (Chờ KT duyệt)', '❌',
     '❌'),
    ('FR-09 Từ chối phiếu', '✅ (Chờ TP duyệt)', '✅ (Chờ BGĐ duyệt)', '✅ (Chờ KT duyệt)', '❌',
     '❌'),
    ('FR-10 Xóa phiếu', '✅ (phiếu của mình, Đang tạo)', '✅ (nt)', '✅ (nt)', '✅ (nt)', '✅ (nt)'),
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
     ('FR-08', 'Duyệt phiếu', 'action', 'extend', [3], None),
     ('FR-09', 'Từ chối phiếu', 'action', 'extend', [3], None),
     ('FR-11', 'In phiếu', 'io', 'extend', [3], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [3], None)],
    'Sơ đồ Use Case tổng quan màn Yêu cầu gia hạn hàng giữ')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1 Xem danh sach
d.h3('2.1 Xem danh sách phiếu')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Yêu cầu gia hạn hàng giữ tại phần mô tả '
           'chi tiết.', anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu yêu cầu gia hạn hàng giữ',
    mota='Hiển thị bảng phiếu nằm trong phạm vi dữ liệu của người đăng nhập, kèm bộ lọc, '
         'phân trang và ô thống kê tổng số phiếu khớp bộ lọc.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng vào menu Tài chính → Giữ hàng → Yêu cầu gia hạn hàng giữ.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem của người dùng.\n'
          '3. Hệ thống bổ sung vào phạm vi những phiếu đang chờ chính người dùng duyệt.\n'
          '4. Hệ thống trả về trang đầu tiên của danh sách và tổng số phiếu.\n'
          '5. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Phiếu ở trạng thái Đang tạo của người khác không xuất hiện trong danh sách.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Yêu cầu gia hạn hàng giữ lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Yêu cầu gia hạn hàng giữ',
     'Tiêu đề cố định phía trên bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở màn lập phiếu mới. Hiện với mọi người dùng đã đăng nhập.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở màn in danh sách theo đúng bộ lọc đang áp.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ chọn trường xuất; bị khóa trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cột cố định, không tắt được, đánh số liên tục theo trang.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PGHHG-NNNNN', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết. Cột cố định, sắp xếp được.'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người lập phiếu.'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only',
     'Đang tạo / Chờ TP duyệt / Chờ BGĐ duyệt / Chờ KT duyệt / Đã duyệt', 'Theo dữ liệu',
     'Đang tạo màu xám; ba trạng thái chờ duyệt màu cam; Đã duyệt màu xanh lá.'),
    ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người duyệt ở bước gần nhất; trống khi chưa ai duyệt.'),
    ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Lần chỉnh sửa gần nhất của phiếu.'),
    ('Cột Phòng ban / Ghi chú / Lý do từ chối', 'Table/Grid', 'Read-only', '–',
     'Ẩn mặc định', 'Bật lên trong cửa sổ Tuỳ chỉnh cột.'),
    ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Cột cố định cuối bảng, chứa các nút thao tác của dòng.'),
    ('Nút Sửa (biểu tượng bút chì)', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện với phiếu do chính mình lập, đang ở trạng thái Đang tạo.'),
    ('Nút Xóa (biểu tượng thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Điều kiện hiển thị giống nút Sửa.'),
    ('Nút Duyệt / Từ chối', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện khi phiếu đang chờ chính người dùng duyệt ở đúng cấp của mình.'),
    ('Nút In / Lịch sử', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'In mở màn in phiếu; Lịch sử mở cửa sổ lịch sử thay đổi.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc trong phạm vi quyền, không phải tổng toàn hệ thống.'),
    ('Phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100', 'Trang 1, 10 dòng',
     'Có nút về đầu / lùi / số trang / tiến / về cuối và ô chọn số dòng mỗi trang.'),
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

# ------------------------------------------------------------ 2.2 Tim kiem va loc
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các tiêu chí lọc riêng của '
           'màn Yêu cầu gia hạn hàng giữ tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu',
    mota='Thu hẹp danh sách theo mã phiếu, trạng thái, người tạo, người duyệt, hàng hóa, '
         'khoảng ngày tạo và khối công ty – phòng ban.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh hoặc bấm Tìm kiếm nâng cao để mở bảng lọc.\n'
          '2. Người dùng chọn / nhập các tiêu chí cần lọc.\n'
          '3. Hệ thống nạp lại danh sách ngay khi một ô lọc nâng cao thay đổi; riêng ô tìm '
          'nhanh chờ người dùng bấm nút Tìm kiếm.\n'
          '4. Bảng hiển thị kết quả và cập nhật lại tổng số phiếu.',
    phu='• Không có phiếu nào khớp → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Bấm Làm mới → xóa toàn bộ tiêu chí, bỏ sắp xếp và nạp lại danh sách từ đầu.\n'
        '• Bộ lọc được ghi nhớ trong 10 phút; quay lại màn trong khoảng đó vẫn giữ điều kiện cũ.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('02-bo-loc-nang-cao.png'),
         shot_caption='Bảng lọc nâng cao đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Gợi ý “Tìm theo mã phiếu...”. Chỉ tìm khi bấm nút Tìm kiếm hoặc nhấn Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', 'Hiển thị', 'Áp dụng ô tìm nhanh, về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Xóa mọi tiêu chí lọc và nạp lại danh sách; giữ nguyên phạm vi dữ liệu theo quyền.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Đang thu gọn',
     'Đóng / mở bảng lọc nâng cao.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ bật / tắt và sắp xếp thứ tự các ô lọc.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống',
     'Chỉ hiện với người có quyền xem theo tổng công ty.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Trống',
     'Chỉ hiện với người có quyền xem theo công ty trở lên; phụ thuộc công ty đã chọn.'),
    ('Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Lọc riêng theo mã phiếu.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 trạng thái', 'Trống',
     'Danh sách trạng thái do hệ thống trả về cùng danh sách phiếu.'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', '–'),
    ('Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', '–'),
    ('Tên hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Lọc phiếu có chứa hàng hóa khớp tên.'),
    ('Mã hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Trống',
     'Lọc phiếu có chứa hàng hóa khớp mã.'),
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
    ('Chọn lại Công ty', 'Change',
     'After:\n– Xóa giá trị Phòng ban đang chọn và nạp lại danh sách phòng ban tương ứng.'),
])

# ------------------------------------------------------------ 2.3 Cai dat bo loc
d.h3('2.3 Cài đặt bộ lọc')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc', 'view',
            [('include', 'Lưu cấu hình theo từng người dùng'),
             ('extend', 'Khôi phục mặc định')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Bộ lọc và Cấu hình cột. Chỉ bổ sung phần riêng của màn Yêu cầu gia hạn hàng giữ '
           'tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc hiển thị',
    mota='Cho phép người dùng tự chọn những ô lọc muốn hiển thị và kéo sắp xếp lại thứ tự. '
         'Cấu hình lưu riêng theo từng người dùng và từng màn hình.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc.\n'
          '2. Hệ thống mở cửa sổ liệt kê 9 ô lọc của màn, kèm ô tích và tay kéo.\n'
          '3. Người dùng bỏ tích ô không dùng, kéo đổi thứ tự nếu cần.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho riêng người dùng và vẽ lại bảng lọc.',
    phu='• Bấm Khôi phục mặc định → đưa danh sách ô lọc về trạng thái ban đầu.\n'
        '• Bấm Đóng → giữ nguyên cấu hình cũ, không lưu thay đổi.',
    dacbiet='Cấu hình chỉ ảnh hưởng tới người dùng hiện tại, không ảnh hưởng người khác.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('03-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc',
     'Kèm dòng hướng dẫn tích chọn và kéo sắp xếp.'),
    ('Danh sách ô lọc', 'Table/Grid', 'Enable', '9 mục', '–', 'Theo cấu hình đã lưu',
     'Mỗi mục gồm số thứ tự, tay kéo, ô tích và tên ô lọc.'),
    ('Ô tích từng mục', 'Button', 'Enable', '–', '–', 'Đang tích',
     'Bỏ tích thì ô lọc đó không hiện ở bảng lọc nâng cao.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình và đóng cửa sổ.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đưa về danh sách và thứ tự ban đầu.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
])

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Cài đặt bộ lọc', 'Click',
     'After:\n– Mở cửa sổ với cấu hình hiện tại của người dùng.'),
    ('Kéo đổi vị trí một mục', 'Click',
     'After:\n– Cập nhật số thứ tự các mục trong danh sách; chưa ghi lại cho tới khi bấm Lưu.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi cấu hình theo người dùng và theo màn hình.\n'
     'After:\n– Đóng cửa sổ và vẽ lại bảng lọc nâng cao theo cấu hình mới.'),
])

# ------------------------------------------------------------ 2.4 Tuy chinh cot
d.h3('2.4 Tuỳ chỉnh cột hiển thị')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view',
            [('include', 'Lưu cấu hình cột theo từng người dùng')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-04 Tuỳ chỉnh cột hiển thị')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Cấu hình cột hiển thị. Chỉ bổ sung phần riêng của màn Yêu cầu gia hạn hàng giữ '
           'tại phần mô tả chi tiết.', anchor='excel')
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
    dacbiet='Ba cột Phòng ban, Ghi chú và Lý do từ chối mặc định TẮT; người dùng tự bật khi cần.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột hiển thị', shot=shot('04-cau-hinh-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '13 cột', '–', 'Theo cấu hình đã lưu',
     'Mỗi dòng gồm ô tích, tên cột và tay kéo.'),
    ('Cột bị khóa', 'Icon', 'Read-only', '–', '–', 'Biểu tượng ổ khóa',
     'STT, Mã phiếu và Hành động luôn hiển thị, không tắt được.'),
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

# ------------------------------------------------------------ 2.5 Tao moi
d.h3('2.5 Tạo mới phiếu')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Tạo mới phiếu yêu cầu gia hạn hàng giữ', 'crud',
            [('include', 'Nạp danh sách lô hàng giữ sắp hết hạn của người lập'),
             ('include', 'Sinh mã phiếu tự động'),
             ('extend', 'Đính kèm tệp'),
             ('extend', 'Xem lịch sử biến động của lô hàng giữ')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-05 Tạo mới phiếu')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới phiếu yêu cầu gia hạn hàng giữ',
    mota='Lập phiếu đề nghị gia hạn cho các lô hàng giữ sắp hết hạn của chính người lập. '
         'Phiếu có thể lưu nháp để sửa tiếp hoặc gửi thẳng cho Trưởng phòng duyệt.',
    tacnhan='Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Người lập đang giữ ít nhất một lô hàng có hạn giữ trước “hôm nay + 7 ngày”.',
    chinh='1. Người dùng bấm nút Tạo mới ở màn danh sách.\n'
          '2. Hệ thống mở màn lập phiếu và nạp sẵn toàn bộ lô hàng giữ sắp hết hạn của người '
          'lập vào bảng Chi tiết.\n'
          '3. Người dùng nhập Ghi chú, đính kèm tệp nếu cần.\n'
          '4. Người dùng tích chọn cột “Cần gia hạn” ở các dòng muốn gia hạn, nhập Số lượng '
          'cần gia hạn và chọn Hạn giữ mới.\n'
          '5. Người dùng bấm Lưu nháp hoặc Gửi duyệt.\n'
          '6. Hệ thống kiểm tra dữ liệu, sinh mã phiếu và ghi phiếu.\n'
          '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Người lập không có lô nào sắp hết hạn → bảng Chi tiết trống kèm câu giải thích, '
        'không lập được phiếu.\n'
        '• Bỏ trống Ghi chú → báo lỗi “Bắt buộc phải nhập” ngay dưới ô, không lưu.\n'
        '• Không tích dòng nào → báo “Chưa tích chọn hàng hoá nào cần gia hạn.”.\n'
        '• Số lượng vượt số Đang giữ → báo lỗi đỏ tại dòng, không lưu.\n'
        '• Hạn giữ mới không hợp lệ hoặc vượt trần → báo lỗi đỏ tại dòng, không lưu.\n'
        '• Bấm Lưu và tiếp tục → lưu nháp rồi ở lại màn để lập phiếu kế tiếp.\n'
        '• Rời màn khi đã nhập mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
    dacbiet='Bảng Chi tiết KHÔNG có nút thêm dòng bằng tay: hệ thống tự nạp đúng các lô sắp '
            'hết hạn của người lập. Ô Đơn vị tính bị khóa vì tồn hàng giữ luôn ghi theo đơn vị '
            'cơ bản của hàng hóa.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('06-tao-moi.png'),
         shot_caption='Màn lập phiếu yêu cầu gia hạn hàng giữ')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Người lập – Ngày lập', 'Label', 'Read-only', '–', '–',
     'Người đăng nhập – ngày hiện tại', 'Hiển thị ở góc phải khối Thông tin chung.'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
     'Lý do xin gia hạn; cả ba cấp duyệt đều đọc dòng này.'),
    ('Chọn tệp đính kèm', 'Button', 'Enable',
     'PDF, ảnh, Word, Excel; tối đa 13 MB mỗi tệp', 'Không', 'Chưa có tệp',
     'Chọn được nhiều tệp; mỗi tệp có nút gỡ khỏi phiếu.'),
    ('Cột Cần gia hạn', 'Table/Grid', 'Enable', '–', 'Không', 'Không tích',
     'Bỏ tích thì hai ô Số lượng và Hạn giữ mới của dòng bị khóa và dòng bị làm mờ.'),
    ('Cột Tên hàng hóa / Khách hàng / Hợp đồng', 'Table/Grid', 'Read-only', '–', '–',
     'Theo lô hàng giữ', 'Lấy từ lô hàng giữ, không sửa được.'),
    ('Cột ĐVT', 'Table/Grid', 'Read-only', '–', '–', 'Đơn vị cơ bản',
     'Có biểu tượng ⓘ giải thích vì sao không đổi được đơn vị.'),
    ('Cột Có thể giữ', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo tồn kho',
     'Tồn kho khả dụng của hàng hóa; có biểu tượng ⓘ phân biệt với cột Đang giữ.'),
    ('Cột Đang giữ', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo lô hàng giữ',
     'Số lượng còn lại của chính lô đang xem.'),
    ('Cột Cần gia hạn (số lượng)', 'Number', 'Enable / Disable', '> 0 và ≤ Đang giữ, tối đa 6 '
     'chữ số', 'Có (khi dòng được tích)', 'Bằng số Đang giữ',
     'Chỉ nhập được số; vượt số Đang giữ thì báo đỏ tại dòng và giữ nguyên số đã gõ.'),
    ('Cột Ngày bắt đầu giữ / Hạn giữ hiện tại', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', '–',
     'Theo lô hàng giữ', '–'),
    ('Cột Hạn giữ mới', 'Datepicker', 'Enable / Disable', 'Từ ngày mai đến hôm nay + 30 ngày',
     'Có (khi dòng được tích)', 'Trống',
     'Các ngày ngoài khoảng cho phép bị chặn ngay trên lịch.'),
    ('Cột Lịch sử', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở cửa sổ lịch sử biến động của lô hàng giữ đó.'),
    ('Dòng hướng dẫn dưới bảng', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     'Nhắc hạn giữ mới phải sau hôm nay và không quá ngày trần.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu phiếu ở trạng thái Đang tạo; bị khóa trong lúc đang lưu.'),
    ('Nút Gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu phiếu và chuyển sang trạng thái Chờ TP duyệt.'),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Chỉ có ở màn Tạo mới: lưu nháp rồi ở lại để lập phiếu kế tiếp.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi tại ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi; không tự sửa giá trị người dùng đã nhập.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Tạo mới', 'System',
     'During:\n– Nạp các lô hàng giữ của chính người lập, còn số lượng, cùng công ty và có hạn '
     'giữ trước “hôm nay + 7 ngày”.\n'
     '– Nạp thêm tồn kho khả dụng để hiển thị cột Có thể giữ.\n'
     'After:\n– Hiển thị bảng Chi tiết; nếu không có lô nào thì hiện câu giải thích thay cho '
     'bảng.'),
    ('Tích / bỏ tích ô Cần gia hạn', 'Change',
     'During:\n– Tích: mở khóa ô Số lượng và Hạn giữ mới, điền sẵn số lượng bằng số Đang giữ.\n'
     '– Bỏ tích: khóa hai ô đó và làm mờ dòng.\n'
     'After:\n– Dòng không tích sẽ không được gửi lên khi lưu.'),
    ('Nhập Số lượng cần gia hạn', 'Change / Blur',
     'During:\n– Chỉ nhận ký tự số.\n'
     '– Bằng 0 → báo “Số lượng gia hạn – Phải lớn hơn 0.”.\n'
     '– Vượt số Đang giữ → báo “Số lượng gia hạn – Không được vượt số đang giữ (…)”.\n'
     'After:\n– Giữ nguyên giá trị người dùng đã gõ, không tự kéo về mức trần.'),
    ('Chọn Hạn giữ mới', 'Change',
     'During:\n– Ngày trong quá khứ hoặc hôm nay → báo “Hạn giữ mới – Phải là ngày tương lai.”.\n'
     '– Ngày vượt “hôm nay + 30 ngày” → báo “Hạn giữ mới – Không được giữ quá …”.\n'
     'After:\n– Ghi nhận ngày hợp lệ vào dòng.'),
    ('Bấm Lưu nháp', 'Click',
     'Before:\n– Không yêu cầu quyền riêng; ai đăng nhập cũng lập được phiếu của mình.\n'
     'During:\n– Ghi chú trống → hiển thị “Bắt buộc phải nhập”.\n'
     '– Không tích dòng nào → hiển thị “Chưa tích chọn hàng hoá nào cần gia hạn.”.\n'
     '– Lô không còn thuộc người lập → hiển thị “Lô hàng giữ không còn tồn tại hoặc không '
     'thuộc người lập phiếu.”.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Sinh mã phiếu dạng PGHHG-NNNNN, ghi phiếu ở trạng thái Đang tạo.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Hiển thị thông báo lưu thành công và quay về màn danh sách.'),
    ('Bấm Gửi duyệt', 'Click',
     'During:\n– Kiểm tra giống Lưu nháp.\n'
     'After:\n– Ghi phiếu ở trạng thái Chờ TP duyệt.\n'
     '– Gửi thông báo cho những người có quyền Trưởng phòng duyệt hàng giữ ở phòng ban của '
     'phiếu.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
    ('Bấm Lưu và tiếp tục', 'Click',
     'After:\n– Lưu phiếu ở trạng thái Đang tạo rồi làm mới màn để lập phiếu kế tiếp, '
     'không quay về danh sách.'),
])

# ------------------------------------------------------------ 2.6 Chinh sua
d.h3('2.6 Chỉnh sửa phiếu')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Chỉnh sửa phiếu yêu cầu gia hạn hàng giữ', 'crud',
            [('include', 'Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo'),
             ('extend', 'Đính kèm tệp')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-06 Chỉnh sửa phiếu')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Chỉnh sửa phiếu yêu cầu gia hạn hàng giữ',
    mota='Sửa lại ghi chú, tệp đính kèm và các dòng hàng của phiếu còn ở trạng thái Đang tạo, '
         'sau đó lưu nháp tiếp hoặc gửi duyệt.',
    tacnhan='Nhân viên kinh doanh — người lập phiếu',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Đang tạo. Phiếu bị từ chối '
             'cũng quay về trạng thái này nên sửa lại được.',
    chinh='1. Người dùng bấm nút Sửa ở màn danh sách hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở màn sửa với dữ liệu đã lưu của phiếu.\n'
          '3. Người dùng chỉnh sửa thông tin cần thiết.\n'
          '4. Người dùng bấm Lưu nháp hoặc Gửi duyệt.\n'
          '5. Hệ thống kiểm tra dữ liệu, cập nhật phiếu và ghi lịch sử thay đổi.\n'
          '6. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Phiếu đã gửi duyệt hoặc đã duyệt → nút Sửa không hiển thị; mở thẳng bằng đường dẫn '
        'thì hệ thống từ chối.\n'
        '• Phiếu của người khác → hệ thống từ chối, không cho mở màn sửa.\n'
        '• Các nhánh lỗi nhập liệu giống chức năng Tạo mới.',
    dacbiet='Lịch sử thay đổi ghi lại chi tiết từng dòng hàng được thêm, sửa hoặc bỏ khỏi phiếu.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('06-tao-moi.png'),
         shot_caption='Màn sửa phiếu dùng chung bố cục với màn lập phiếu')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mã phiếu', 'Textbox', 'Disable', 'PGHHG-NNNNN', '–', 'Theo dữ liệu',
     'Chỉ hiển thị, không sửa được.'),
    ('Trạng thái', 'Badge', 'Read-only', '–', '–', 'Đang tạo', '–'),
    ('Phòng ban yêu cầu', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu',
     'Phòng ban của người lập tại thời điểm lập phiếu.'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Theo dữ liệu', '–'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu đã lưu',
     'Các dòng đã chọn được tích sẵn và điền sẵn số lượng, hạn giữ mới.'),
    ('Nút Lưu nháp / Gửi duyệt / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Màn sửa không có nút Lưu và tiếp tục.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System',
     'Before:\n– Kiểm tra phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.\n'
     '– Nếu không → hệ thống từ chối và không mở màn sửa.\n'
     'After:\n– Nạp dữ liệu phiếu, tích sẵn các dòng đã chọn.'),
    ('Bấm Lưu nháp / Gửi duyệt', 'Click',
     'During:\n– Kiểm tra dữ liệu giống chức năng Tạo mới.\n'
     'After:\n– Cập nhật phiếu; Gửi duyệt thì chuyển sang Chờ TP duyệt và thông báo cho '
     'Trưởng phòng.\n'
     '– Ghi một dòng lịch sử “Chỉnh sửa”, nêu rõ những giá trị đã thay đổi.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.7 Xem chi tiet
d.h3('2.7 Xem chi tiết phiếu')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung phần riêng của màn Yêu cầu gia hạn '
           'hàng giữ tại phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu yêu cầu gia hạn hàng giữ',
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
        '• Người đang ở đúng cấp duyệt của phiếu → được sửa lại ô Hạn giữ mới ngay tại màn này '
        'trước khi bấm duyệt.',
    dacbiet=None)

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('07-chi-tiet.png'),
         shot_caption='Màn chi tiết phiếu ở chế độ chỉ đọc')

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Chi tiết yêu cầu gia hạn hàng giữ: <mã phiếu>',
     '–'),
    ('Khối Thông tin chung', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm Mã phiếu, Trạng thái, Phòng ban yêu cầu, Ghi chú, người lập và ngày lập.'),
    ('Khối File đính kèm', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Danh sách tệp mở xem được; không có tệp thì hiện “Chưa có tệp đính kèm”.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Hiển thị đủ các cột như màn lập phiếu; cột Cần gia hạn chỉ hiện với người đang ở đúng '
     'cấp duyệt.'),
    ('Khối Lịch sử duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Bốn cột Cấp duyệt, Kết quả, Người thực hiện, Thời gian và Ghi chú. Dòng từ chối hiển thị '
     'nhãn đỏ “Từ chối”, dòng duyệt hiển thị nhãn xanh “Đã duyệt”.'),
    ('Khối Lịch sử thay đổi', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Chỉ nạp dữ liệu khi người dùng bấm Xem lịch sử.'),
    ('Nút thao tác cuối màn', 'Button', 'Enable / Ẩn', '–', 'Theo quyền và trạng thái',
     'Gồm Duyệt, Sửa, Xóa, In, Từ chối và Quay lại; nút không dùng được thì ẩn hẳn.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu theo phạm vi dữ liệu và quyền duyệt.\n'
     '– Không đủ quyền → báo không có quyền xem phiếu này.\n'
     'After:\n– Hiển thị dữ liệu phiếu và các nút thao tác hợp lệ.'),
    ('Bấm biểu tượng Lịch sử ở một dòng hàng', 'Click',
     'After:\n– Mở cửa sổ lịch sử biến động của lô hàng giữ đó.'),
    ('Bấm Xem lịch sử ở khối Lịch sử thay đổi', 'Click',
     'After:\n– Nạp và hiển thị danh sách mốc thay đổi của phiếu, mới nhất trước.'),
])

# ------------------------------------------------------------ 2.8 Duyet
d.h3('2.8 Duyệt phiếu')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Duyệt phiếu yêu cầu gia hạn hàng giữ', 'action',
            [('include', 'Kiểm tra quyền duyệt đúng cấp và cùng công ty'),
             ('include', 'Kiểm tra tồn hàng giữ còn đủ'),
             ('extend', 'Xác định có phải qua Ban giám đốc hay không'),
             ('extend', 'Ghi tồn hàng giữ sang hạn giữ mới')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-08 Duyệt phiếu')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Duyệt phiếu yêu cầu gia hạn hàng giữ',
    mota='Ký duyệt phiếu ở một trong ba cấp Trưởng phòng, Ban giám đốc, Kế toán. Bước Kế toán '
         'duyệt là bước duy nhất ghi tồn hàng giữ.',
    tacnhan='Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Phiếu đang ở đúng trạng thái chờ cấp đó duyệt; người duyệt có quyền tương ứng và '
             'cùng công ty với phiếu. Riêng Trưởng phòng còn phải quản lý phòng ban của phiếu.',
    chinh='1. Người duyệt mở màn chi tiết phiếu.\n'
          '2. Người duyệt xem lại các dòng hàng, có thể sửa lại ô Hạn giữ mới.\n'
          '3. Người duyệt bấm nút duyệt của cấp mình.\n'
          '4. Hệ thống kiểm tra quyền, trạng thái và dữ liệu dòng hàng.\n'
          '5. Hệ thống chuyển phiếu sang bước tiếp theo, ghi lịch sử và gửi thông báo.\n'
          '6. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Trưởng phòng duyệt: nếu phiếu thuộc diện phải qua Ban giám đốc thì chuyển sang '
        'Chờ BGĐ duyệt, ngược lại chuyển thẳng sang Chờ KT duyệt.\n'
        '• Ban giám đốc duyệt → chuyển sang Chờ KT duyệt.\n'
        '• Kế toán duyệt → phiếu chuyển sang Đã duyệt và hệ thống ghi tồn hàng giữ.\n'
        '• Phiếu đã được người khác xử lý trước đó → báo “Phiếu không ở trạng thái chờ duyệt.”.\n'
        '• Người dùng không đúng cấp → báo “Bạn không có quyền duyệt bước này.”.\n'
        '• Bỏ tích hết các dòng rồi mới duyệt → báo “Phải giữ lại ít nhất 1 hàng hoá cần gia '
        'hạn thì mới duyệt được.”.',
    dacbiet='Gia hạn KHÔNG sửa hạn của lô cũ. Hệ thống trừ số lượng ở lô cũ rồi cộng vào lô có '
            'hạn giữ mới; nếu chưa có lô đó thì tạo mới. Mỗi lần chuyển ghi hai dòng nhật ký '
            'biến động tồn hàng giữ.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Duyệt', shot=shot('08-chi-tiet-nguoi-duyet.png'),
         shot_caption='Màn chi tiết dưới góc nhìn người duyệt — có nút duyệt và Từ chối')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Cột Cần gia hạn', 'Table/Grid', 'Enable', '–', 'Không', 'Theo dữ liệu',
     'Người duyệt được bỏ tích dòng không đồng ý gia hạn.'),
    ('Cột Hạn giữ mới', 'Datepicker', 'Enable', 'Từ ngày mai đến hôm nay + 30 ngày', 'Có',
     'Theo dữ liệu', 'Người duyệt ở mọi cấp được sửa lại ngày trước khi ký duyệt.'),
    ('Cột Cần gia hạn (số lượng)', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Người duyệt KHÔNG sửa được số lượng.'),
    ('Nút duyệt của cấp hiện tại', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Nhãn nêu rõ cấp đang ký: TP duyệt / BGĐ duyệt / KT duyệt.'),
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện cùng lúc với nút duyệt của cấp đó.'),
])

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút duyệt của cấp hiện tại', 'Click',
     'Before:\n– Kiểm tra quyền duyệt đúng cấp, cùng công ty với phiếu; Trưởng phòng còn phải '
     'quản lý phòng ban của phiếu.\n'
     '– Nếu không → hiển thị “Bạn không có quyền duyệt bước này.” và dừng xử lý.\n'
     'During:\n– Phiếu không còn ở trạng thái chờ duyệt → hiển thị “Phiếu không ở trạng thái '
     'chờ duyệt.”.\n'
     '– Không còn dòng nào được tích → hiển thị “Phải giữ lại ít nhất 1 hàng hoá cần gia hạn '
     'thì mới duyệt được.”.\n'
     '– Hạn giữ mới hoặc số lượng không hợp lệ → báo lỗi tương ứng và dừng.\n'
     'After:\n– Ghi lại người duyệt, thời điểm duyệt và ghi chú của cấp đó.\n'
     '– Trưởng phòng duyệt: chuyển sang Chờ BGĐ duyệt hoặc Chờ KT duyệt tuỳ điều kiện; hiển '
     'thị “Yêu cầu đã được chuyển đến Ban giám đốc.” hoặc “Yêu cầu đã được chuyển đến Kế toán.”.\n'
     '– Kế toán duyệt: chuyển phiếu sang Đã duyệt, trừ số lượng ở lô cũ và cộng vào lô có hạn '
     'giữ mới, ghi nhật ký biến động tồn hàng giữ.\n'
     '– Ghi một dòng lịch sử “Duyệt”; gửi thông báo cho cấp kế tiếp hoặc cho người lập.\n'
     '– Hiển thị “Duyệt phiếu thành công.” và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.9 Tu choi
d.h3('2.9 Từ chối phiếu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Từ chối phiếu yêu cầu gia hạn hàng giữ', 'action',
            [('include', 'Kiểm tra quyền duyệt đúng cấp'),
             ('include', 'Bắt buộc nhập lý do từ chối')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-09 Từ chối phiếu')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Từ chối phiếu yêu cầu gia hạn hàng giữ',
    mota='Trả phiếu về cho người lập kèm lý do. Phiếu quay lại trạng thái Đang tạo để người '
         'lập sửa và gửi lại.',
    tacnhan='Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Phiếu đang ở đúng trạng thái chờ cấp đó duyệt.',
    chinh='1. Người duyệt bấm nút Từ chối ở màn chi tiết hoặc ở cột Hành động của danh sách.\n'
          '2. Hệ thống mở cửa sổ Từ chối yêu cầu gia hạn hàng giữ.\n'
          '3. Người duyệt nhập lý do từ chối.\n'
          '4. Người duyệt bấm nút xác nhận.\n'
          '5. Hệ thống đưa phiếu về trạng thái Đang tạo, ghi lý do và gửi thông báo cho '
          'người lập.',
    phu='• Bỏ trống lý do → báo “Bắt buộc phải nhập lý do từ chối”, cửa sổ không đóng.\n'
        '• Lý do quá 255 ký tự → báo “Không được vượt quá 255 ký tự”.\n'
        '• Phiếu đã được xử lý trước đó → báo phiếu không ở trạng thái chờ duyệt.',
    dacbiet='Hệ thống KHÔNG có trạng thái “Từ chối” riêng. Vì phiếu quay về đúng trạng thái '
            'Đang tạo nên lý do từ chối là thông tin duy nhất cho người lập biết vì sao bị '
            'trả lại — do đó bắt buộc nhập.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Từ chối', shot=shot('12-popup-tu-choi.png'),
         shot_caption='Cửa sổ Từ chối yêu cầu gia hạn hàng giữ')
d.p('Cửa sổ Từ chối được mở ngay trên màn chi tiết hoặc màn danh sách theo đường dẫn ở trên.')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Từ chối yêu cầu gia hạn hàng giữ',
     'Kèm dòng phụ hiển thị mã phiếu.'),
    ('Lý do từ chối', 'Textarea', 'Enable', '0–255 ký tự', 'Trống',
     'Gợi ý “Nhập lý do trả lại phiếu cho người lập...”. Bắt buộc nhập.'),
    ('Dòng nhắc trạng thái', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Nhắc rằng phiếu sẽ quay về trạng thái Đang tạo để người lập sửa và gửi lại.'),
    ('Nút xác nhận từ chối', 'Button', 'Enable', '–', 'Hiển thị',
     'Bị khóa trong lúc đang xử lý.'),
    ('Nút đóng cửa sổ', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng và bỏ nội dung đã nhập.'),
], required=False)

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Từ chối', 'Click',
     'Before:\n– Kiểm tra người dùng đang ở đúng cấp duyệt của phiếu.\n'
     '– Nếu không → hiển thị “Bạn không có quyền từ chối phiếu này.”.\n'
     'After:\n– Mở cửa sổ nhập lý do.'),
    ('Bấm xác nhận từ chối', 'Click',
     'During:\n– Lý do trống → hiển thị “Bắt buộc phải nhập lý do từ chối”, cửa sổ không đóng.\n'
     '– Lý do quá 255 ký tự → hiển thị “Không được vượt quá 255 ký tự”.\n'
     'After:\n– Đưa phiếu về trạng thái Đang tạo, ghi lý do vào phiếu và vào bộ cột của cấp '
     'vừa từ chối.\n'
     '– Ghi một dòng lịch sử “Từ chối”; gửi thông báo cho người lập phiếu.\n'
     '– Hiển thị thông báo thành công và nạp lại danh sách.'),
])

# ------------------------------------------------------------ 2.10 Xoa
d.h3('2.10 Xóa phiếu')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu yêu cầu gia hạn hàng giữ', 'action',
            [('include', 'Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa và Thông báo.', anchor='delete')
d.intro_table(
    ten='Xóa phiếu yêu cầu gia hạn hàng giữ',
    mota='Xóa hẳn một phiếu còn ở trạng thái Đang tạo do chính người dùng lập.',
    tacnhan='Nhân viên kinh doanh — người lập phiếu',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.',
    chinh='1. Người dùng bấm nút Xóa ở cột Hành động hoặc ở màn chi tiết.\n'
          '2. Hệ thống hiển thị hộp thoại xác nhận kèm mã phiếu.\n'
          '3. Người dùng chọn Xóa.\n'
          '4. Hệ thống xóa phiếu và nạp lại danh sách.',
    phu='• Chọn Hủy → đóng hộp thoại, không xóa gì.\n'
        '• Phiếu đã gửi duyệt hoặc đã duyệt → nút Xóa không hiển thị; gọi thẳng chức năng xóa '
        'thì hệ thống từ chối.',
    dacbiet='Phiếu đã duyệt không xóa được vì đã ghi tồn hàng giữ.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('13-xac-nhan-xoa.png'),
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
     'Before:\n– Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo.\n'
     '– Nếu không → nút không hiển thị; gọi thẳng chức năng thì hệ thống từ chối.\n'
     'After:\n– Mở hộp thoại xác nhận.'),
    ('Xác nhận Xóa', 'Click',
     'After:\n– Xóa phiếu cùng các dòng hàng của phiếu.\n'
     '– Hiển thị “Xóa thành công.” và nạp lại danh sách.'),
])

# ------------------------------------------------------------ 2.11 In
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
    ten='In phiếu yêu cầu gia hạn hàng giữ và in danh sách',
    mota='Mở bản xem trước để in một phiếu, hoặc in toàn bộ danh sách theo đúng bộ lọc '
         'đang áp dụng.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Với bản in phiếu: người dùng xem được phiếu đó.',
    chinh='1. Người dùng bấm nút In ở cột Hành động, ở màn chi tiết, hoặc nút In ở thanh công '
          'cụ danh sách.\n'
          '2. Hệ thống mở tab mới hiển thị bản xem trước đúng khổ giấy.\n'
          '3. Người dùng bấm nút In trên bản xem trước để gửi lệnh in.',
    phu='• Bản in phiếu dùng khổ A4 dọc; bản in danh sách dùng khổ A4 ngang.\n'
        '• Bản in danh sách in đúng phạm vi và điều kiện lọc đang áp, không chỉ trang hiện tại.',
    dacbiet='Phần đầu bản in lấy theo công ty ghi trên phiếu, không lấy theo người đang in.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In phiếu', shot=shot('10-in-phieu.png'),
         shot_caption='Bản in phiếu yêu cầu gia hạn hàng giữ')
d.layout(menu=MENU + ' => In danh sách', shot=shot('11-in-danh-sach.png'),
         shot_caption='Bản in danh sách phiếu yêu cầu gia hạn hàng giữ')

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In trên bản xem trước', 'Button', 'Enable', '–', 'Hiển thị',
     'Nằm phía trên, canh phải mép giấy.'),
    ('Phần đầu chứng từ', 'Label', 'Read-only', '–', 'Theo công ty của phiếu',
     'Gồm logo và thông tin liên hệ của công ty ghi trên phiếu.'),
    ('Khối thông tin phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người yêu cầu, Phòng ban, Trạng thái, Ghi chú.'),
    ('Bảng hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cột STT, Tên hàng hóa, Model, Mã hàng hóa, Khách hàng, Hợp đồng, ĐVT, SL gia hạn, '
     'Hạn giữ hiện tại, Hạn giữ mới và dòng Tổng cộng.'),
    ('Bảng lịch sử duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Bốn cột Cấp duyệt, Người duyệt, Thời gian và Ghi chú; in đủ mọi dòng đã duyệt kể cả khi '
     'không có ghi chú.'),
    ('Khối ký tên', 'Label', 'Read-only', '–', 'Hiển thị',
     'Bốn ô ký: Người lập, Trưởng phòng, Ban giám đốc, Kế toán.'),
    ('Bản in danh sách', 'Table/Grid', 'Read-only', '–', 'Theo bộ lọc',
     'Có dòng Tổng số phiếu và bảy cột STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, '
     'Người duyệt, Ngày duyệt.'),
], required=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In ở dòng hoặc ở màn chi tiết', 'Click',
     'After:\n– Mở tab mới hiển thị bản in của đúng phiếu đó.'),
    ('Bấm nút In ở thanh công cụ danh sách', 'Click',
     'After:\n– Mở tab mới hiển thị bản in danh sách theo đúng bộ lọc đang áp.'),
])

# ------------------------------------------------------------ 2.12 Xuat Excel
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
          '2. Hệ thống mở cửa sổ Chọn trường xuất Excel với 11 trường, mặc định chọn hết.\n'
          '3. Người dùng bỏ chọn các trường không cần.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống lấy toàn bộ dữ liệu khớp bộ lọc và tải tệp về máy.',
    phu='• Trong lúc đang xuất, nút bị khóa để tránh bấm nhiều lần.\n'
        '• Xuất thất bại → hiển thị thông báo lỗi, không tải tệp.',
    dacbiet='Tệp xuất chứa toàn bộ dòng khớp bộ lọc trong phạm vi quyền, không giới hạn ở '
            'trang đang xem.')

d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('05-chon-truong-xuat-excel.png'),
         shot_caption='Cửa sổ Chọn trường xuất Excel')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất Excel', '–'),
    ('Ô chọn trường xuất', 'Dropdown', 'Enable', '11 trường', 'Có', 'Chọn hết 11 trường',
     'Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, '
     'Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối.'),
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
     '– Hiển thị “Xuất Excel thành công” và đóng cửa sổ.'),
])

# ------------------------------------------------------------ 2.13 Lich su
d.h3('2.13 Xem lịch sử thay đổi')

d.p('2.13.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Hiển thị các mốc thao tác đã thực hiện trên phiếu: tạo mới, chỉnh sửa, gửi duyệt, '
         'duyệt, từ chối, kèm người thực hiện, thời điểm và nội dung thay đổi.',
    tacnhan='Nhân viên kinh doanh; Trưởng phòng; Ban giám đốc; Kế toán',
    dieukien='Người dùng xem được phiếu.',
    chinh='1. Người dùng bấm biểu tượng Lịch sử ở cột Hành động, hoặc bấm Xem lịch sử ở khối '
          'Lịch sử thay đổi trong màn chi tiết.\n'
          '2. Hệ thống nạp danh sách mốc thay đổi của phiếu.\n'
          '3. Danh sách hiển thị theo thứ tự mới nhất trước.',
    phu='• Phiếu chưa có thao tác nào được ghi nhận → hiện dòng “Chưa có lịch sử thao tác nào.”. '
        'Các phiếu lập từ hệ thống cũ trước khi bật tính năng này sẽ không có dữ liệu lịch sử.\n'
        '• Bấm Làm mới → nạp lại danh sách.',
    dacbiet=None)

d.p('2.13.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Lịch sử',
         shot=shot('09-lich-su-duyet-va-thay-doi.png'),
         shot_caption='Khối Lịch sử duyệt và Lịch sử thay đổi ở màn chi tiết')

d.p('2.13.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề khối', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi',
     'Kèm số mốc thay đổi khi đã nạp dữ liệu.'),
    ('Nút Xem lịch sử / Thu gọn', 'Button', 'Enable', '–', 'Thu gọn',
     'Chỉ nạp dữ liệu ở lần bấm mở đầu tiên.'),
    ('Nút Làm mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Chỉ hiện khi khối đang mở.'),
    ('Danh sách mốc thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi mốc gồm nhóm thao tác, người thực hiện, thời điểm và chi tiết giá trị thay đổi '
     'của các trường: Trạng thái, Ghi chú, File đính kèm, Hàng hoá, SL gia hạn, Hạn giữ mới.'),
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

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu gia hạn hàng giữ; không lặp '
           'lại các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Nguồn dòng hàng của phiếu', [
        '– Bảng Chi tiết chỉ nạp các lô hàng giữ thỏa mãn đồng thời: do chính người lập phiếu '
        'đứng tên giữ, còn số lượng lớn hơn 0, cùng công ty với người lập, và có hạn giữ trước '
        '“ngày hiện tại + số ngày cảnh báo” (hiện là 7 ngày).',
        '– Người lập KHÔNG được thêm dòng hàng bằng tay.',
        '– Không có lô nào thỏa điều kiện thì không lập được phiếu.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-02', 'Trần hạn giữ mới', [
        '– Hạn giữ mới phải là ngày trong tương lai và không vượt quá “ngày hiện tại + số ngày '
        'giữ tối đa” (hiện là 30 ngày).',
        '– Ràng buộc này áp dụng cả lúc lập phiếu lẫn lúc người duyệt sửa lại hạn giữ mới.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Duyệt']),
    ('BR-03', 'Số lượng cần gia hạn', [
        '– Phải lớn hơn 0 và không vượt quá số lượng Đang giữ của chính lô đó.',
        '– Tối đa 6 chữ số.',
        '– Nhập sai thì hệ thống báo đỏ ngay tại dòng và giữ nguyên giá trị đã gõ, không tự '
        'kéo về mức trần.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-04', 'Bắt buộc có ghi chú', [
        '– Ô Ghi chú là bắt buộc, tối đa 255 ký tự.',
        '– Đây là chỗ duy nhất người lập nêu lý do xin gia hạn và cả ba cấp duyệt đều đọc.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-05', 'Luồng duyệt ba cấp', [
        '– Gửi duyệt đưa phiếu về trạng thái Chờ TP duyệt.',
        '– Trưởng phòng duyệt: phiếu chuyển sang Chờ BGĐ duyệt nếu thuộc diện phải qua Ban '
        'giám đốc, ngược lại chuyển thẳng sang Chờ KT duyệt.',
        '– Ban giám đốc duyệt: chuyển sang Chờ KT duyệt.',
        '– Kế toán duyệt: phiếu chuyển sang Đã duyệt.',
    ], 'Duyệt'),
    ('BR-06', 'Điều kiện phải qua Ban giám đốc', [
        '– Xét từng dòng hàng được đề nghị gia hạn.',
        '– Dòng có gắn hợp đồng: nếu tỉ lệ tiền đã thu trên tổng giá trị hợp đồng thấp hơn '
        'ngưỡng phần trăm cấu hình theo loại hợp đồng của công ty thì phiếu phải qua Ban '
        'giám đốc.',
        '– Dòng không gắn hợp đồng: cộng dồn giá trị hàng đề nghị gia hạn; vượt hạn mức cấu '
        'hình của công ty thì phiếu phải qua Ban giám đốc.',
        '– Chỉ cần một dòng thỏa điều kiện là cả phiếu phải qua Ban giám đốc.',
    ], 'Duyệt'),
    ('BR-07', 'Điều kiện duyệt của từng cấp', [
        '– Người duyệt phải cùng công ty với phiếu.',
        '– Trưởng phòng còn phải quản lý đúng phòng ban ghi trên phiếu.',
        '– Người có vai trò quản trị hệ thống được bỏ qua ràng buộc phòng ban.',
        '– Duyệt sai cấp hoặc phiếu đã được người khác xử lý trước đó đều bị từ chối.',
    ], 'Duyệt'),
    ('BR-08', 'Thời điểm ghi tồn hàng giữ', [
        '– Chỉ bước Kế toán duyệt mới ghi tồn hàng giữ. Ba bước trước đó không đụng tới tồn.',
        '– Gia hạn không sửa hạn của lô cũ: hệ thống trừ số lượng ở lô cũ rồi cộng vào lô có '
        'cùng nhân viên, khách hàng, hàng hóa nhưng hạn giữ là hạn giữ mới; chưa có lô đó thì '
        'tạo mới.',
        '– Lô mới lấy công ty theo lô nguồn, không lấy theo người đang duyệt.',
        '– Mỗi lần chuyển ghi hai dòng nhật ký biến động tồn hàng giữ: một dòng trừ và một '
        'dòng cộng.',
        '– Dòng có hạn giữ mới trùng hạn giữ hiện tại sẽ bị bỏ qua, không ghi tồn.',
    ], 'Duyệt'),
    ('BR-09', 'Từ chối phiếu', [
        '– Lý do từ chối là bắt buộc, tối đa 255 ký tự.',
        '– Phiếu bị từ chối quay về đúng trạng thái Đang tạo; hệ thống không có trạng thái '
        '“Từ chối” riêng.',
        '– Lý do được ghi vào bộ cột của đúng cấp đã từ chối và hiển thị ở khối Lịch sử duyệt '
        'với nhãn đỏ Từ chối.',
    ], ['Duyệt', 'Từ chối']),
    ('BR-10', 'Điều kiện sửa và xóa', [
        '– Chỉ người lập phiếu mới sửa hoặc xóa được, và chỉ khi phiếu đang ở trạng thái '
        'Đang tạo.',
        '– Phiếu đã gửi duyệt hoặc đã duyệt không sửa, không xóa.',
        '– Nút không dùng được thì ẩn hẳn ở cả màn danh sách lẫn màn chi tiết.',
    ], ['Chỉnh sửa', 'Xóa']),
    ('BR-11', 'Phạm vi dữ liệu', [
        '– Áp theo thứ tự ưu tiên: tổng công ty → công ty → phòng ban → chỉ phiếu của mình.',
        '– Người có quyền duyệt được xem thêm mọi phiếu khác nháp trong cùng công ty.',
        '– Phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy.',
        '– Phạm vi này áp cho cả danh sách, màn chi tiết, bản in và tệp Excel xuất ra.',
    ], 'Toàn màn hình'),
    ('BR-12', 'Đơn vị tính của dòng hàng', [
        '– Tồn hàng giữ luôn ghi theo đơn vị cơ bản của hàng hóa nên ô Đơn vị tính bị khóa.',
        '– Muốn đổi đơn vị thì phải sửa ở danh mục hàng hóa.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xem chi tiết']),
    ('BR-13', 'Tệp đính kèm', [
        '– Nhận các định dạng PDF, ảnh, Word, Excel.',
        '– Mỗi tệp tối đa 13 MB; đính kèm được nhiều tệp trên một phiếu.',
    ], ['Tạo mới', 'Chỉnh sửa']),
])

d.save()
