# -*- coding: utf-8 -*-
"""Sinh SRS man "Yeu cau huy hang giu" theo FORM CHUAN 2026-08-28.

Nguon: code HRM nhanh `gop_db`
  BE  Modules/Finance/{Entities/PrepickCancel, Services/PrepickCancelRequestService.php,
      Http/Controllers/V1/PrepickCancelRequestController.php, Http/Requests/PrepickCancel/*}
  FE  pages/finance/prepick-cancel-requests/*
Anh chup that: ./prepick_cancel_shots (Playwright MCP, 1440x900, ngay 05/09/2026).
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

SHOTS = os.path.join(BASE, 'prepick_cancel_shots')
OUT = os.path.join(BASE, 'SRS - Yeu cau huy hang giu.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Giữ hàng => Yêu cầu hủy hàng giữ'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/prepick-cancel-requests',
           full_url='https://<host-hrm>/finance/prepick-cancel-requests',
           img_prefix='pychhg_')

# ============================================================== TRANG DAU
d.title_block('Yêu cầu hủy hàng giữ')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Yêu cầu hủy hàng giữ '
    '(mã phiếu PYCHHG), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, luồng duyệt và phân quyền của màn hình.',
    'Làm rõ nguồn dữ liệu dòng hàng: chỉ chọn được hàng mà chính người lập đang giữ cho đúng '
    'khách hàng đã chọn.',
    'Làm rõ ý nghĩa của thao tác duyệt: duyệt một yêu cầu hủy chính là lập Phiếu hủy hàng giữ, '
    'và tồn hàng giữ chỉ bị trừ tại thời điểm lưu phiếu hủy đó.',
    'Làm rõ khác biệt giữa hai cột số lượng "Yêu cầu hủy" và "Duyệt hủy".',
    'Làm rõ phạm vi dữ liệu mà mỗi cấp quyền xem được.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên '
                 'kinh doanh đứng tên giữ.'),
    ('Lô hàng giữ', 'Một dòng tồn hàng giữ, xác định bởi bộ: nhân viên giữ – khách hàng – '
                    'hàng hóa – hạn giữ – công ty.'),
    ('Yêu cầu hủy hàng giữ', 'Phiếu đề nghị trả lại kho phần hàng đang giữ mà khách không lấy '
                             'nữa. Mã phiếu dạng PYCHHG.'),
    ('Phiếu hủy hàng giữ', 'Chứng từ do người duyệt lập từ một phiếu yêu cầu. Mã phiếu dạng '
                           'PHHG. Chính lúc lưu phiếu này tồn hàng giữ mới bị trừ.'),
    ('Yêu cầu hủy (số lượng)', 'Số lượng người lập đề nghị hủy giữ.'),
    ('Duyệt hủy (số lượng)', 'Số lượng người duyệt thực sự chấp thuận hủy; có thể nhỏ hơn số '
                             'đề nghị.'),
    ('Có thể hủy', 'Số lượng còn có thể hủy của hàng hóa đó, đã trừ phần đang nằm trong đề nghị '
                   'xuất kho chưa hoàn thành.'),
    ('Có thể giữ', 'Tồn kho khả dụng của hàng hóa trong công ty tại thời điểm mở phiếu; là số '
                   'tham khảo, khác với số đã yêu cầu hủy hoặc đã duyệt hủy ghi trên phiếu.'),
    ('Trừ tồn theo thứ tự hạn giữ', 'Khi lập phiếu hủy, phần mềm trừ dần từ lô có hạn giữ sớm '
                                    'nhất tới lô có hạn giữ muộn hơn.'),
], widths=[1.6, 4.4])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Màn hình KHÔNG có quyền riêng cho Thêm / Sửa / Xóa: mọi người dùng đã đăng nhập đều lập '
    'được phiếu yêu cầu hủy cho hàng giữ của chính mình, và chỉ sửa / xóa được phiếu do chính '
    'mình lập khi phiếu còn ở trạng thái Đang tạo.')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý giữ hàng',
     'Nút "Tạo phiếu hủy hàng giữ" (tương đương thao tác duyệt) và nút "Không duyệt" với phiếu '
     'đang ở trạng thái Chờ duyệt. Ngoài ra được xem mọi phiếu khác bản nháp.'),
], widths=[0.8, 2.0, 3.2])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu hàng giữ theo tổng công ty', 'Toàn bộ phiếu của mọi công ty.'),
    ('V2', 'Xem phiếu hàng giữ theo công ty', 'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem phiếu hàng giữ theo phòng ban',
     'Phiếu thuộc các phòng ban mà người đăng nhập được phân công quản lý, cộng phòng ban của '
     'chính người đó.'),
    ('—', '(không có cấp nào)', 'Chỉ phiếu do chính mình lập.'),
], widths=[0.8, 2.0, 3.2])

d.p('Hai quy tắc chung:')
d.bullets([
    'Phiếu ở trạng thái Đang tạo là bản nháp, chỉ người lập nhìn thấy và mở được.',
    'Người có quyền Quản lý giữ hàng được xem mọi phiếu khác bản nháp.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1/V2/V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅ (theo cấp)', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột hiển thị', '✅', '✅', '✅'),
    ('FR-05 Tạo mới phiếu', '✅', '✅', '✅'),
    ('FR-06 Chỉnh sửa phiếu', '✅ (phiếu của mình, Đang tạo)', '✅ (nt)', '✅ (nt)'),
    ('FR-07 Xem chi tiết phiếu', '✅', '✅ (trong phạm vi)', '✅ (phiếu của mình)'),
    ('FR-08 Duyệt — lập Phiếu hủy hàng giữ', '✅ (phiếu Chờ duyệt)', '❌', '❌'),
    ('FR-09 Không duyệt phiếu', '✅ (phiếu Chờ duyệt)', '❌', '❌'),
    ('FR-10 Xóa phiếu', '✅ (phiếu của mình, Đang tạo)', '✅ (nt)', '✅ (nt)'),
    ('FR-11 In phiếu / In danh sách', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-12 Xuất Excel danh sách', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-13 Xem lịch sử thay đổi', '✅', '✅', '✅ (phiếu của mình)'),
], widths=[2.3, 1.3, 1.2, 1.2])

# ================================================ PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [('Nhân viên kinh doanh', [0, 1, 2, 3]),
     ('Người quản lý giữ hàng', [0, 3])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Tạo mới phiếu', 'crud'),
     ('FR-06', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-07', 'Xem chi tiết phiếu', 'view')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-12', 'Xuất Excel danh sách', 'io', 'extend', [0], None),
     ('FR-10', 'Xóa phiếu', 'action', 'extend', [0], None),
     ('FR-14', 'Chọn hàng đang giữ từ popup', 'crud', 'include', [1, 2], None),
     ('FR-08', 'Lập Phiếu hủy hàng giữ', 'action', 'extend', [3], None),
     ('FR-09', 'Không duyệt phiếu', 'action', 'extend', [3], None),
     ('FR-11', 'In phiếu', 'io', 'extend', [3], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [3], None)],
    'Sơ đồ Use Case tổng quan màn Yêu cầu hủy hàng giữ')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách phiếu')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Yêu cầu hủy hàng giữ tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu yêu cầu hủy hàng giữ',
    mota='Hiển thị bảng phiếu nằm trong phạm vi dữ liệu của người đăng nhập, kèm bộ lọc, '
         'phân trang và ô thống kê tổng số phiếu khớp bộ lọc.',
    tacnhan='Nhân viên kinh doanh; Người quản lý giữ hàng; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập vào hệ thống.',
    chinh='1. Người dùng vào menu Tài chính → Giữ hàng → Yêu cầu hủy hàng giữ.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem của người dùng.\n'
          '3. Hệ thống trả về trang đầu tiên của danh sách và tổng số phiếu.\n'
          '4. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Phiếu ở trạng thái Đang tạo của người khác không xuất hiện trong danh sách.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Yêu cầu hủy hàng giữ lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Yêu cầu hủy hàng giữ',
     'Tiêu đề cố định phía trên bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở màn lập phiếu mới. Hiện với mọi người dùng đã đăng nhập.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ chọn trường xuất; bị khóa trong lúc đang xuất.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cột cố định, không tắt được.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PYCHHG-NNNNN', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết. Cột cố định, sắp xếp được.'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người lập phiếu.'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Đang tạo / Chờ duyệt / Đã duyệt', 'Theo dữ liệu',
     'Đang tạo màu xám; Chờ duyệt màu cam; Đã duyệt màu xanh lá.'),
    ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người đã lập phiếu hủy tương ứng; trống khi chưa duyệt.'),
    ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', '–'),
    ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Lần chỉnh sửa gần nhất. Cột Ngày cập nhật sắp xếp được.'),
    ('Cột Khách hàng / Phòng ban / Ghi chú / Lý do không duyệt', 'Table/Grid', 'Read-only', '–',
     'Ẩn mặc định', 'Bật lên trong cửa sổ Tuỳ chỉnh cột.'),
    ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Cột cố định cuối bảng, chứa các nút thao tác của dòng.'),
    ('Nút Sửa / Xóa', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện với phiếu do chính mình lập, đang ở trạng thái Đang tạo.'),
    ('Nút Duyệt', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     'Chỉ hiện với người có quyền Quản lý giữ hàng và phiếu đang ở trạng thái Chờ duyệt. '
     'Bấm vào sẽ mở màn lập Phiếu hủy hàng giữ.'),
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
     'During:\n– Áp phạm vi dữ liệu; người có quyền Quản lý giữ hàng được xem thêm mọi phiếu '
     'khác bản nháp.\n'
     '– Khôi phục bộ lọc đã lưu của người dùng nếu còn hiệu lực (10 phút).\n'
     'After:\n– Trả về trang 1, tổng số phiếu và danh sách trạng thái để đổ vào ô lọc.'),
    ('Bấm vào mã phiếu', 'Click',
     'Before:\n– Kiểm tra người dùng có được xem phiếu này không.\n'
     '– Nếu không → hệ thống báo không có quyền xem phiếu và không mở màn chi tiết.\n'
     'After:\n– Mở màn chi tiết của phiếu.'),
    ('Bấm tiêu đề cột có mũi tên sắp xếp', 'Click',
     'During:\n– Chỉ ba cột Mã phiếu, Ngày tạo, Ngày cập nhật sắp xếp được.\n'
     'After:\n– Nạp lại danh sách từ trang 1 theo thứ tự mới, giữ nguyên bộ lọc.'),
    ('Bấm số trang / nút tiến lùi / đổi số dòng mỗi trang', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu trang mới; số thứ tự tiếp tục liên tục.'),
])

# ------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các tiêu chí lọc riêng của '
           'màn Yêu cầu hủy hàng giữ tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu',
    mota='Thu hẹp danh sách theo mã phiếu, trạng thái, người tạo, người duyệt, hàng hóa, '
         'khoảng ngày tạo và khối công ty – phòng ban.',
    tacnhan='Nhân viên kinh doanh; Người quản lý giữ hàng',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng nhập từ khóa vào ô tìm nhanh hoặc bấm Tìm kiếm nâng cao để mở bảng lọc.\n'
          '2. Người dùng chọn / nhập các tiêu chí cần lọc.\n'
          '3. Hệ thống nạp lại danh sách ngay khi một ô lọc nâng cao thay đổi; riêng ô tìm '
          'nhanh chờ người dùng bấm nút Tìm kiếm.\n'
          '4. Bảng hiển thị kết quả và cập nhật lại tổng số phiếu.',
    phu='• Không có phiếu nào khớp → bảng hiện dòng “Không có dữ liệu phù hợp.”.\n'
        '• Bấm Làm mới → xóa toàn bộ tiêu chí, bỏ sắp xếp và nạp lại danh sách từ đầu.\n'
        '• Bộ lọc được ghi nhớ trong 10 phút.',
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
     'Xóa mọi tiêu chí lọc và nạp lại danh sách.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Đang thu gọn',
     'Đóng / mở bảng lọc nâng cao.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ bật / tắt và sắp xếp thứ tự các ô lọc.'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Trống',
     'Chỉ hiện với người có quyền xem theo tổng công ty.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Trống',
     'Chỉ hiện với người có quyền xem theo công ty trở lên.'),
    ('Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Trống', 'Lọc riêng theo mã phiếu.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Trống',
     'Đang tạo / Chờ duyệt / Đã duyệt.'),
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
          '2. Hệ thống mở cửa sổ liệt kê các ô lọc của màn, kèm ô tích và tay kéo.\n'
          '3. Người dùng bỏ tích ô không dùng, kéo đổi thứ tự nếu cần.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống lưu cấu hình cho riêng người dùng và vẽ lại bảng lọc.',
    phu='• Bấm Khôi phục mặc định → đưa danh sách ô lọc về trạng thái ban đầu.\n'
        '• Bấm Đóng → giữ nguyên cấu hình cũ, không lưu thay đổi.',
    dacbiet='Cấu hình chỉ ảnh hưởng tới người dùng hiện tại.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('08-cai-dat-bo-loc.png'),
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
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi cấu hình theo người dùng và theo màn hình.\n'
     'After:\n– Đóng cửa sổ và vẽ lại bảng lọc nâng cao theo cấu hình mới.'),
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
    dacbiet='Bốn cột Khách hàng, Phòng ban, Ghi chú và Lý do không duyệt mặc định TẮT.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Cấu hình cột hiển thị', shot=shot('09-cau-hinh-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Tuỳ chỉnh cột', '–'),
    ('Danh sách cột', 'Table/Grid', 'Enable', '14 cột', '–', 'Theo cấu hình đã lưu',
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
d.uc_figure('FR-05', 'Tạo mới phiếu yêu cầu hủy hàng giữ', 'crud',
            [('include', 'Nạp danh sách khách hàng đang được giữ hàng'),
             ('include', 'Chọn hàng đang giữ từ popup'),
             ('include', 'Sinh mã phiếu tự động'),
             ('extend', 'Kiểm tra đủ tồn hàng giữ khi gửi duyệt')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-05 Tạo mới phiếu')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới phiếu yêu cầu hủy hàng giữ',
    mota='Lập phiếu đề nghị trả lại kho phần hàng đang giữ cho một khách hàng. Phiếu có thể lưu '
         'nháp để bổ sung hàng sau, hoặc gửi duyệt ngay.',
    tacnhan='Nhân viên kinh doanh; Người dùng đã đăng nhập',
    dieukien='Người lập đang giữ hàng cho ít nhất một khách hàng.',
    chinh='1. Người dùng bấm nút Tạo mới ở màn danh sách.\n'
          '2. Hệ thống mở màn lập phiếu và nạp danh sách khách hàng đang được người lập giữ hàng.\n'
          '3. Người dùng chọn Khách hàng.\n'
          '4. Người dùng bấm Thêm hàng hóa để mở popup chọn hàng đang giữ cho khách đó.\n'
          '5. Người dùng nhập Số lượng yêu cầu hủy cho từng dòng.\n'
          '6. Người dùng bấm Lưu nháp hoặc Lưu và gửi duyệt.\n'
          '7. Hệ thống kiểm tra dữ liệu, sinh mã phiếu và ghi phiếu.\n'
          '8. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Người lập không giữ hàng cho khách nào → ô Khách hàng rỗng kèm câu giải thích, chưa '
        'lập được phiếu.\n'
        '• Chưa chọn Khách hàng → nút Thêm hàng hóa bị khóa kèm chú thích nhắc chọn khách trước.\n'
        '• Lưu nháp KHÔNG bắt buộc phải có dòng hàng; Lưu và gửi duyệt thì bắt buộc ít nhất một '
        'dòng có số lượng lớn hơn 0.\n'
        '• Số lượng vượt phần có thể hủy → báo lỗi, không lưu.\n'
        '• Rời màn khi đã nhập mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
    dacbiet='Danh sách khách hàng CHỈ gồm khách đang có hàng giữ của chính người lập phiếu. '
            'Danh sách rỗng là đúng nghiệp vụ, không phải lỗi dữ liệu.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('04-tao-moi.png'),
         shot_caption='Màn lập phiếu yêu cầu hủy hàng giữ')
d.layout(menu=MENU + ' => Tạo mới => Thêm hàng hóa', shot=shot('06-popup-chon-hang.png'),
         shot_caption='Popup Hàng đang giữ cho khách hàng')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Người lập – Ngày lập', 'Label', 'Read-only', '–', '–',
     'Người đăng nhập – ngày giờ hiện tại', 'Hiển thị ở góc phải khối Thông tin chung.'),
    ('Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách đang được giữ hàng', 'Có', 'Trống',
     'Có dòng chú thích ngay dưới ô giải thích phạm vi danh sách. Khóa lại ở màn Sửa.'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Nút Thêm hàng hóa', 'Button', 'Enable / Disable', '–', '–', 'Đang khóa',
     'Chỉ mở khi đã chọn Khách hàng; khi khóa có chú thích nhắc chọn khách trước.'),
    ('Popup Hàng đang giữ cho khách hàng', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Có hai ô tìm kiếm Tên hàng hóa và Mã hàng hóa, bảng hàng đang giữ, phân trang, nút Chọn '
     'kèm số dòng đã tích và nút Đóng.'),
    ('Cột Cần hủy', 'Table/Grid', 'Enable', '–', 'Không', 'Đang tích',
     'Bỏ tích thì ô Số lượng của dòng bị khóa và dòng bị làm mờ.'),
    ('Cột Tên hàng hóa / Model / Mã hàng hóa / Thương hiệu', 'Table/Grid', 'Read-only', '–', '–',
     'Theo hàng hóa đã chọn', 'Không sửa được.'),
    ('Cột Có thể hủy', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo tồn hàng giữ',
     'Đã trừ phần đang nằm trong đề nghị xuất kho chưa hoàn thành.'),
    ('Cột Yêu cầu hủy', 'Number', 'Enable / Disable', '> 0 và ≤ Có thể hủy, tối đa 6 chữ số',
     'Có', 'Trống', 'Nhập sai thì báo đỏ tại dòng và giữ nguyên số đã gõ.'),
    ('Cột ĐVT', 'Table/Grid', 'Read-only', '–', '–', 'Đơn vị cơ bản của hàng hóa', '–'),
    ('Nút xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Bỏ hẳn dòng hàng khỏi phiếu.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu phiếu ở trạng thái Đang tạo; không bắt buộc phải có dòng hàng.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu phiếu và chuyển sang trạng thái Chờ duyệt.'),
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
     'During:\n– Nạp danh sách khách hàng mà chính người lập đang giữ hàng, trong cùng công ty.\n'
     'After:\n– Hiển thị form trống; nút Thêm hàng hóa đang khóa.'),
    ('Chọn Khách hàng', 'Change',
     'After:\n– Mở khóa nút Thêm hàng hóa.\n'
     '– Nếu đã có dòng hàng của khách cũ thì các dòng đó không còn phù hợp, người dùng phải '
     'chọn lại.'),
    ('Bấm Thêm hàng hóa', 'Click',
     'Before:\n– Phải đã chọn Khách hàng.\n'
     'During:\n– Popup liệt kê hàng mà chính người lập đang giữ cho khách hàng đã chọn; các '
     'hàng đã có trong phiếu được loại khỏi danh sách.\n'
     'After:\n– Các dòng được tích sẽ được thêm vào bảng Chi tiết với ô Cần hủy tích sẵn.'),
    ('Nhập Số lượng yêu cầu hủy', 'Change / Blur',
     'During:\n– Chỉ nhận ký tự số.\n– Bằng 0 → báo “Phải lớn hơn 0”.\n'
     '– Vượt số Có thể hủy → báo lỗi tại dòng.\n'
     'After:\n– Giữ nguyên giá trị người dùng đã gõ, không tự kéo về mức trần.'),
    ('Bấm Lưu nháp', 'Click',
     'During:\n– Khách hàng trống → hiển thị “Bắt buộc phải chọn”.\n'
     '– KHÔNG bắt buộc có dòng hàng.\n'
     'After:\n– Sinh mã phiếu dạng PYCHHG-NNNNN, ghi phiếu ở trạng thái Đang tạo.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Hiển thị thông báo lưu thành công và quay về màn danh sách.'),
    ('Bấm Lưu và gửi duyệt', 'Click',
     'During:\n– Bắt buộc có ít nhất một dòng hàng được tích với số lượng lớn hơn 0, nếu không '
     'hiển thị “Phải chọn ít nhất 1 hàng hoá cần hủy với số lượng lớn hơn 0”.\n'
     '– Kiểm tra tồn hàng giữ còn đủ; thiếu thì hiển thị thông báo nêu rõ tên hàng không đủ '
     'số lượng đang giữ.\n'
     'After:\n– Ghi phiếu ở trạng thái Chờ duyệt.\n'
     '– Gửi thông báo cho những người có quyền Quản lý giữ hàng cùng công ty.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.6
d.h3('2.6 Chỉnh sửa phiếu')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Chỉnh sửa phiếu yêu cầu hủy hàng giữ', 'crud',
            [('include', 'Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo'),
             ('include', 'Chọn hàng đang giữ từ popup')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-06 Chỉnh sửa phiếu')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Chỉnh sửa phiếu yêu cầu hủy hàng giữ',
    mota='Sửa lại ghi chú và các dòng hàng của phiếu còn ở trạng thái Đang tạo, sau đó lưu nháp '
         'tiếp hoặc gửi duyệt.',
    tacnhan='Nhân viên kinh doanh — người lập phiếu',
    dieukien='Phiếu do chính người dùng lập và đang ở trạng thái Đang tạo. Phiếu bị trả về cũng '
             'quay lại trạng thái này nên sửa lại được.',
    chinh='1. Người dùng bấm nút Sửa ở màn danh sách hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở màn sửa với dữ liệu đã lưu của phiếu.\n'
          '3. Người dùng chỉnh sửa thông tin cần thiết.\n'
          '4. Người dùng bấm Lưu nháp hoặc Lưu và gửi duyệt.\n'
          '5. Hệ thống kiểm tra dữ liệu, cập nhật phiếu và ghi lịch sử thay đổi.\n'
          '6. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Ô Khách hàng bị KHÓA ở màn sửa: đổi khách thì mọi dòng hàng cũ mất ý nghĩa.\n'
        '• Phiếu đã gửi duyệt hoặc đã duyệt → nút Sửa không hiển thị.\n'
        '• Phiếu của người khác → hệ thống từ chối, không cho mở màn sửa.',
    dacbiet='Phiếu bị trả về có thêm khối “Lý do không duyệt” hiển thị ngay trên màn sửa để '
            'người lập biết cần chỉnh gì.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('05-sua-phieu.png'),
         shot_caption='Màn sửa phiếu, có khối Lý do không duyệt của lần trả về trước')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Khách hàng', 'Dropdown', 'Disable', '–', '–', 'Theo dữ liệu',
     'Khóa ở màn sửa; muốn đổi khách thì lập phiếu mới.'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Theo dữ liệu', '–'),
    ('Khối Lý do không duyệt', 'Label', 'Read-only', '–', '–', 'Ẩn',
     'Chỉ hiện khi phiếu từng bị trả về, hiển thị nguyên văn lý do.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu đã lưu',
     'Các dòng đã chọn được tích sẵn và điền sẵn số lượng.'),
    ('Nút Lưu nháp / Lưu và gửi duyệt / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Màn sửa không có nút Lưu và tiếp tục.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System',
     'Before:\n– Kiểm tra phiếu do chính người dùng lập và đang ở trạng thái Đang tạo.\n'
     '– Nếu không → hệ thống từ chối và không mở màn sửa.\n'
     'After:\n– Nạp dữ liệu phiếu; giữ nguyên khách hàng đã chọn kể cả khi khách đó không còn '
     'hàng giữ nào.'),
    ('Bấm Lưu nháp / Lưu và gửi duyệt', 'Click',
     'During:\n– Kiểm tra dữ liệu giống chức năng Tạo mới.\n'
     'After:\n– Cập nhật phiếu; Lưu và gửi duyệt thì chuyển sang Chờ duyệt và thông báo cho '
     'người có quyền Quản lý giữ hàng.\n'
     '– Ghi một dòng lịch sử “Chỉnh sửa”, nêu rõ những giá trị đã thay đổi.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.7
d.h3('2.7 Xem chi tiết phiếu')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu yêu cầu hủy hàng giữ',
    mota='Hiển thị toàn bộ thông tin phiếu ở chế độ chỉ đọc: thông tin chung, bảng hàng hóa với '
         'hai cột số lượng Yêu cầu hủy và Duyệt hủy, liên kết sang phiếu hủy đã lập và lịch sử '
         'thay đổi.',
    tacnhan='Nhân viên kinh doanh; Người quản lý giữ hàng',
    dieukien='Người dùng nằm trong phạm vi được xem phiếu.',
    chinh='1. Người dùng bấm vào mã phiếu ở màn danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống hiển thị màn chi tiết ở chế độ chỉ đọc.\n'
          '4. Các nút thao tác ở cuối màn hiện theo đúng quyền và trạng thái của phiếu.',
    phu='• Không đủ quyền xem → hệ thống báo không có quyền xem phiếu này.\n'
        '• Phiếu Đang tạo của người khác → không mở được.\n'
        '• Phiếu đã duyệt có thêm ô Phiếu hủy hàng giữ là liên kết mở phiếu hủy tương ứng.',
    dacbiet=None)

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('03-chi-tiet.png'),
         shot_caption='Màn chi tiết phiếu đã duyệt, có liên kết sang phiếu hủy hàng giữ')

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Chi tiết yêu cầu hủy hàng giữ: <mã phiếu>', '–'),
    ('Khối Thông tin chung', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm Khách hàng, Ghi chú, Mã phiếu, Trạng thái, Người duyệt, Ngày duyệt, Phòng ban yêu cầu '
     'và Phiếu hủy hàng giữ.'),
    ('Ô Phiếu hủy hàng giữ', 'Text', 'Read-only', 'PHHG-NNNNN', 'Trống',
     'Là liên kết mở phiếu hủy tương ứng; chỉ có giá trị khi phiếu đã được duyệt.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cột STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, Có thể giữ, Số lượng '
     '(gồm hai cột con Yêu cầu hủy và Duyệt hủy) và ĐVT.'),
    ('Cột Duyệt hủy', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Số lượng người duyệt thực sự chấp thuận; có thể nhỏ hơn cột Yêu cầu hủy.'),
    ('Khối Lý do không duyệt', 'Label', 'Read-only', '–', 'Ẩn',
     'Chỉ hiện khi phiếu từng bị trả về.'),
    ('Khối Lịch sử thay đổi', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Chỉ nạp dữ liệu khi người dùng bấm Xem lịch sử.'),
    ('Nút thao tác cuối màn', 'Button', 'Enable / Ẩn', '–', 'Theo quyền và trạng thái',
     'Gồm Tạo phiếu hủy hàng giữ, In, Không duyệt, Sửa, Xóa và Quay lại; nút không dùng được '
     'thì ẩn hẳn.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu theo phạm vi dữ liệu và quyền Quản lý giữ hàng.\n'
     '– Không đủ quyền → báo không có quyền xem phiếu này.\n'
     'After:\n– Hiển thị dữ liệu phiếu và các nút thao tác hợp lệ.'),
    ('Bấm vào mã phiếu hủy hàng giữ', 'Click',
     'After:\n– Mở màn chi tiết của phiếu hủy tương ứng.'),
    ('Bấm Xem lịch sử ở khối Lịch sử thay đổi', 'Click',
     'After:\n– Nạp và hiển thị danh sách mốc thay đổi của phiếu, mới nhất trước.'),
])

# ------------------------------------------------------------ 2.8
d.h3('2.8 Duyệt phiếu — lập Phiếu hủy hàng giữ')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Lập Phiếu hủy hàng giữ từ phiếu yêu cầu', 'action',
            [('include', 'Kiểm tra quyền Quản lý giữ hàng'),
             ('include', 'Kiểm tra tồn hàng giữ còn đủ'),
             ('extend', 'Cắt bớt số lượng so với đề nghị'),
             ('extend', 'Trừ tồn hàng giữ theo thứ tự hạn giữ')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-08 Lập Phiếu hủy hàng giữ')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Duyệt phiếu yêu cầu hủy hàng giữ',
    mota='Duyệt một yêu cầu hủy chính là lập Phiếu hủy hàng giữ tương ứng. Người duyệt được cắt '
         'bớt số lượng so với đề nghị. Ngay khi lưu phiếu hủy, tồn hàng giữ bị trừ.',
    tacnhan='Người quản lý giữ hàng',
    dieukien='Phiếu đang ở trạng thái Chờ duyệt; người duyệt có quyền Quản lý giữ hàng.',
    chinh='1. Người duyệt mở phiếu yêu cầu và bấm nút Tạo phiếu hủy hàng giữ, hoặc bấm biểu '
          'tượng duyệt ở cột Hành động.\n'
          '2. Hệ thống mở màn lập Phiếu hủy hàng giữ, nạp sẵn các dòng hàng từ phiếu yêu cầu.\n'
          '3. Người duyệt xem lại và điều chỉnh số lượng duyệt hủy nếu cần.\n'
          '4. Người duyệt bấm Lưu.\n'
          '5. Hệ thống kiểm tra tồn, trừ tồn hàng giữ và chuyển phiếu yêu cầu sang Đã duyệt.',
    phu='• Yêu cầu đã được người khác xử lý trước đó → hệ thống báo phiếu không còn ở trạng thái '
        'chờ duyệt hoặc không đủ quyền duyệt.\n'
        '• Số lượng duyệt hủy vượt phần còn giữ → hệ thống báo lỗi và không lưu, tồn không đổi.\n'
        '• Dòng có số lượng bằng 0 → bị bỏ qua, không trừ tồn.\n'
        '• Hàng không nằm trong phiếu yêu cầu → hệ thống từ chối.',
    dacbiet='Đây là thao tác GHI TỒN duy nhất của cả luồng. Hệ thống trừ dần từ lô có hạn giữ '
            'sớm nhất; nếu tổng các lô không đủ thì toàn bộ thao tác bị hủy bỏ, không trừ một '
            'phần.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Tạo phiếu hủy hàng giữ',
         shot=shot('03-chi-tiet.png'),
         shot_caption='Nút Tạo phiếu hủy hàng giữ nằm ở cuối màn chi tiết phiếu yêu cầu')
d.p('Màn lập Phiếu hủy hàng giữ thuộc màn hình Phiếu hủy hàng giữ, được mở từ đường dẫn ở trên.')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Tạo phiếu hủy hàng giữ', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện với người có quyền Quản lý giữ hàng và phiếu đang ở trạng thái Chờ duyệt. '
     'Nhãn nút nói đúng việc nó làm, không phải nhãn “Duyệt”.'),
    ('Biểu tượng duyệt ở cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Điều hướng thẳng sang màn lập Phiếu hủy hàng giữ của đúng phiếu yêu cầu đó.'),
    ('Cột Duyệt hủy trên màn lập phiếu hủy', 'Number', 'Enable',
     '> 0 và ≤ số còn giữ', '–', 'Bằng số Yêu cầu hủy',
     'Người duyệt được giảm bớt so với đề nghị.'),
])

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo phiếu hủy hàng giữ', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng và trạng thái phiếu là Chờ duyệt.\n'
     '– Nếu không → nút không hiển thị; gọi thẳng chức năng thì hệ thống từ chối.\n'
     'After:\n– Mở màn lập Phiếu hủy hàng giữ với dữ liệu nạp sẵn từ phiếu yêu cầu.'),
    ('Lưu Phiếu hủy hàng giữ', 'Click',
     'Before:\n– Kiểm tra lại quyền và trạng thái phiếu yêu cầu.\n'
     'During:\n– Không dòng nào có số lượng lớn hơn 0 → hiển thị “Phải chọn ít nhất 1 hàng hoá '
     'cần hủy với số lượng lớn hơn 0”.\n'
     '– Hàng không nằm trong phiếu yêu cầu → hiển thị thông báo từ chối.\n'
     '– Tồn hàng giữ không đủ → hiển thị lỗi và hủy toàn bộ thao tác.\n'
     'After:\n– Ghi Phiếu hủy hàng giữ với mã dạng PHHG-NNNNN.\n'
     '– Trừ tồn hàng giữ theo thứ tự hạn giữ sớm trước, ghi nhật ký biến động tồn hàng giữ.\n'
     '– Chuyển phiếu yêu cầu sang trạng thái Đã duyệt, ghi người duyệt và thời điểm duyệt.\n'
     '– Ghi một dòng lịch sử; gửi thông báo cho người lập phiếu yêu cầu.\n'
     '– Hiển thị thông báo đã lập phiếu hủy hàng giữ kèm mã phiếu.'),
])

# ------------------------------------------------------------ 2.9
d.h3('2.9 Không duyệt phiếu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Không duyệt phiếu yêu cầu hủy hàng giữ', 'action',
            [('include', 'Kiểm tra quyền Quản lý giữ hàng'),
             ('include', 'Bắt buộc nhập lý do không duyệt')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — FR-09 Không duyệt phiếu')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc ghi lịch sử.', anchor='notice')
d.intro_table(
    ten='Không duyệt phiếu yêu cầu hủy hàng giữ',
    mota='Trả phiếu về cho người lập kèm lý do. Phiếu quay lại trạng thái Đang tạo để người lập '
         'sửa và gửi lại.',
    tacnhan='Người quản lý giữ hàng',
    dieukien='Phiếu đang ở trạng thái Chờ duyệt.',
    chinh='1. Người duyệt bấm nút Không duyệt ở màn chi tiết.\n'
          '2. Hệ thống mở cửa sổ Không duyệt yêu cầu hủy hàng giữ.\n'
          '3. Người duyệt nhập lý do.\n'
          '4. Người duyệt bấm nút xác nhận.\n'
          '5. Hệ thống đưa phiếu về trạng thái Đang tạo, ghi lý do và gửi thông báo cho '
          'người lập.',
    phu='• Bỏ trống lý do → báo “Bắt buộc phải nhập lý do không duyệt”, cửa sổ không đóng.\n'
        '• Lý do quá 255 ký tự → báo “Không được vượt quá 255 ký tự”.\n'
        '• Phiếu đã được xử lý trước đó → báo phiếu không ở trạng thái chờ duyệt.',
    dacbiet='Hệ thống KHÔNG có trạng thái “Không duyệt” riêng. Phiếu quay về đúng trạng thái '
            'Đang tạo nên lý do là thông tin duy nhất cho người lập biết vì sao bị trả lại.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Không duyệt', shot=shot('12-popup-khong-duyet.png'),
         shot_caption='Cửa sổ Không duyệt yêu cầu hủy hàng giữ')
d.layout(menu=MENU + ' => Sửa', shot=shot('05-sua-phieu.png'),
         shot_caption='Khối Lý do không duyệt hiển thị lại cho người lập sau khi bị trả về')
d.p('Cửa sổ Không duyệt được mở ngay trên màn chi tiết theo đường dẫn ở trên.')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Không duyệt yêu cầu hủy hàng giữ',
     'Kèm dòng phụ hiển thị mã phiếu.'),
    ('Lý do không duyệt', 'Textarea', 'Enable', '0–255 ký tự', 'Trống',
     'Gợi ý “Nhập lý do trả lại phiếu cho người lập...”. Bắt buộc nhập.'),
    ('Dòng nhắc trạng thái', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Nhắc rằng phiếu sẽ quay về trạng thái Đang tạo để người lập sửa và gửi lại.'),
    ('Nút xác nhận', 'Button', 'Enable', '–', 'Hiển thị', 'Bị khóa trong lúc đang xử lý.'),
    ('Nút đóng cửa sổ', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng và bỏ nội dung đã nhập.'),
], required=False)

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Không duyệt', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng và trạng thái phiếu là Chờ duyệt.\n'
     'After:\n– Mở cửa sổ nhập lý do.'),
    ('Bấm xác nhận không duyệt', 'Click',
     'During:\n– Lý do trống → hiển thị “Bắt buộc phải nhập lý do không duyệt”, cửa sổ không '
     'đóng.\n'
     '– Lý do quá 255 ký tự → hiển thị “Không được vượt quá 255 ký tự”.\n'
     'After:\n– Đưa phiếu về trạng thái Đang tạo và ghi lý do vào phiếu.\n'
     '– ⚠ Tồn hàng giữ KHÔNG thay đổi.\n'
     '– Ghi một dòng lịch sử; gửi thông báo cho người lập phiếu.\n'
     '– Hiển thị thông báo thành công và quay về màn danh sách.'),
])

# ------------------------------------------------------------ 2.10
d.h3('2.10 Xóa phiếu')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu yêu cầu hủy hàng giữ', 'action',
            [('include', 'Kiểm tra phiếu do chính mình lập và đang ở trạng thái Đang tạo')],
            actor=ACTOR_P1,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa và Thông báo.', anchor='delete')
d.intro_table(
    ten='Xóa phiếu yêu cầu hủy hàng giữ',
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
    dacbiet='Phiếu đã duyệt không xóa được vì đã sinh ra Phiếu hủy hàng giữ và đã trừ tồn.')

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
    ten='In phiếu yêu cầu hủy hàng giữ và in danh sách',
    mota='Mở bản xem trước để in một phiếu, hoặc in toàn bộ danh sách theo đúng bộ lọc '
         'đang áp dụng.',
    tacnhan='Nhân viên kinh doanh; Người quản lý giữ hàng',
    dieukien='Với bản in phiếu: người dùng xem được phiếu đó.',
    chinh='1. Người dùng bấm nút In ở cột Hành động hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở tab mới hiển thị bản xem trước đúng khổ giấy.\n'
          '3. Người dùng bấm nút In trên bản xem trước để gửi lệnh in.',
    phu='• Bản in phiếu dùng khổ A4 dọc; bản in danh sách dùng khổ A4 ngang.\n'
        '• Bản in danh sách in đúng phạm vi và điều kiện lọc đang áp.',
    dacbiet='Phần đầu bản in lấy theo công ty ghi trên phiếu, không lấy theo người đang in. '
            'Màn danh sách hiện CHƯA có nút mở bản in danh sách trên thanh công cụ, phải mở '
            'bằng đường dẫn.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In phiếu', shot=shot('07-in-phieu.png'),
         shot_caption='Bản in phiếu yêu cầu hủy hàng giữ')
d.layout(menu=MENU + ' => In danh sách', shot=shot('11-in-danh-sach.png'),
         shot_caption='Bản in danh sách phiếu yêu cầu hủy hàng giữ')

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In trên bản xem trước', 'Button', 'Enable', '–', 'Hiển thị',
     'Nằm phía trên, canh phải mép giấy.'),
    ('Phần đầu chứng từ', 'Label', 'Read-only', '–', 'Theo công ty của phiếu',
     'Gồm logo và thông tin liên hệ của công ty ghi trên phiếu.'),
    ('Khối thông tin phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Khách hàng, Người yêu cầu, Phòng ban, Trạng thái, Ghi chú.'),
    ('Bảng hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Các cột STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, ĐVT, SL yêu cầu hủy và dòng '
     'Tổng cộng.'),
    ('Khối ký tên', 'Label', 'Read-only', '–', 'Hiển thị', 'Các ô ký theo mẫu chứng từ.'),
    ('Bản in danh sách', 'Table/Grid', 'Read-only', '–', 'Theo bộ lọc',
     'Có dòng Tổng số phiếu và các cột STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, '
     'Người duyệt, Ngày duyệt.'),
], required=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In ở dòng hoặc ở màn chi tiết', 'Click',
     'After:\n– Mở tab mới hiển thị bản in của đúng phiếu đó.'),
    ('Mở bản in danh sách', 'Click',
     'After:\n– Hiển thị bản in danh sách theo đúng bộ lọc đang áp.'),
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
    tacnhan='Nhân viên kinh doanh; Người quản lý giữ hàng',
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ Chọn trường xuất Excel với 12 trường, mặc định chọn hết.\n'
          '3. Người dùng bỏ chọn các trường không cần.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống lấy toàn bộ dữ liệu khớp bộ lọc và tải tệp về máy.',
    phu='• Trong lúc đang xuất, nút bị khóa để tránh bấm nhiều lần.\n'
        '• Xuất thất bại → hiển thị thông báo lỗi, không tải tệp.',
    dacbiet='Tệp xuất chứa toàn bộ dòng khớp bộ lọc trong phạm vi quyền, không giới hạn ở trang '
            'đang xem.')

d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', shot=shot('10-chon-truong-xuat-excel.png'),
         shot_caption='Cửa sổ Chọn trường xuất Excel')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất Excel', '–'),
    ('Ô chọn trường xuất', 'Dropdown', 'Enable', '12 trường', 'Có', 'Chọn hết 12 trường',
     'Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, '
     'Ngày cập nhật, Khách hàng, Phòng ban, Ghi chú, Lý do không duyệt.'),
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
    mota='Hiển thị các mốc thao tác đã thực hiện trên phiếu: tạo mới, chỉnh sửa, gửi duyệt, '
         'duyệt, không duyệt, kèm người thực hiện, thời điểm và nội dung thay đổi.',
    tacnhan='Nhân viên kinh doanh; Người quản lý giữ hàng',
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

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu hủy hàng giữ; không lặp lại '
           'các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Nguồn khách hàng và hàng hóa của phiếu', [
        '– Danh sách Khách hàng chỉ gồm khách đang có hàng giữ của CHÍNH người lập phiếu, trong '
        'cùng công ty.',
        '– Popup chọn hàng chỉ liệt kê hàng mà người lập đang giữ cho đúng khách hàng đã chọn.',
        '– Hàng đã có trong phiếu bị loại khỏi popup để tránh chọn trùng.',
        '– Danh sách rỗng là đúng nghiệp vụ khi người lập không giữ hàng cho khách nào.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-02', 'Khóa ô Khách hàng khi sửa', [
        '– Ô Khách hàng chỉ nhập lúc tạo mới; màn sửa khóa ô này.',
        '– Lý do: đổi khách hàng thì toàn bộ dòng hàng đã chọn không còn ý nghĩa.',
        '– Khách hàng đang chọn vẫn hiển thị đúng tên kể cả khi khách đó không còn hàng giữ nào.',
    ], 'Chỉnh sửa'),
    ('BR-03', 'Lưu nháp và Gửi duyệt có ràng buộc khác nhau', [
        '– Lưu nháp: chỉ bắt buộc chọn Khách hàng, KHÔNG bắt buộc có dòng hàng.',
        '– Lưu và gửi duyệt: bắt buộc có ít nhất một dòng được tích với số lượng lớn hơn 0.',
        '– Ghi chú không bắt buộc ở cả hai trường hợp, tối đa 255 ký tự.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-04', 'Số lượng yêu cầu hủy', [
        '– Phải lớn hơn 0 và không vượt quá số ở cột Có thể hủy.',
        '– Tối đa 6 chữ số.',
        '– Nhập sai thì hệ thống báo đỏ ngay tại dòng và giữ nguyên giá trị đã gõ.',
        '– Dòng bỏ tích “Cần hủy” bị loại khỏi phiếu khi lưu.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-05', 'Ý nghĩa hai cột số lượng', [
        '– “Yêu cầu hủy” là số người lập đề nghị.',
        '– “Duyệt hủy” là số người duyệt thực sự chấp thuận, có thể nhỏ hơn số đề nghị.',
        '– Cột “Có thể giữ” trên màn chi tiết là tồn kho tại thời điểm mở phiếu, KHÁC với hai '
        'cột trên.',
    ], ['Xem chi tiết', 'Duyệt']),
    ('BR-06', 'Duyệt là lập Phiếu hủy hàng giữ', [
        '– Màn này KHÔNG có thao tác duyệt trực tiếp; người duyệt bấm “Tạo phiếu hủy hàng giữ” '
        'để mở màn lập phiếu hủy.',
        '– Phiếu yêu cầu chỉ chuyển sang Đã duyệt khi phiếu hủy được lưu thành công.',
        '– Một phiếu yêu cầu tương ứng đúng một phiếu hủy.',
    ], 'Duyệt'),
    ('BR-07', 'Thời điểm trừ tồn hàng giữ', [
        '– Tồn hàng giữ chỉ bị trừ tại thời điểm lưu Phiếu hủy hàng giữ.',
        '– Trừ dần theo thứ tự hạn giữ sớm trước, muộn sau.',
        '– Số lượng dùng để tìm lô tồn tính theo NGƯỜI LẬP PHIẾU YÊU CẦU, không phải người lập '
        'phiếu hủy.',
        '– Nếu tổng các lô không đủ thì toàn bộ thao tác bị hủy bỏ, không trừ một phần.',
        '– Dòng có số lượng bằng 0 bị bỏ qua, không ghi nhật ký biến động.',
    ], 'Duyệt'),
    ('BR-08', 'Không duyệt phiếu', [
        '– Lý do không duyệt là bắt buộc, tối đa 255 ký tự.',
        '– Phiếu quay về đúng trạng thái Đang tạo; hệ thống không có trạng thái “Không duyệt” '
        'riêng.',
        '– Lý do hiển thị ở cột Lý do không duyệt ngoài danh sách và ở khối riêng trong màn sửa.',
        '– Thao tác này KHÔNG đụng tới tồn hàng giữ.',
    ], 'Duyệt'),
    ('BR-09', 'Điều kiện sửa và xóa', [
        '– Chỉ người lập phiếu mới sửa hoặc xóa được, và chỉ khi phiếu đang ở trạng thái '
        'Đang tạo.',
        '– Phiếu đã gửi duyệt hoặc đã duyệt không sửa, không xóa.',
        '– Nút không dùng được thì ẩn hẳn ở cả màn danh sách lẫn màn chi tiết.',
    ], ['Chỉnh sửa', 'Xóa']),
    ('BR-10', 'Phạm vi dữ liệu', [
        '– Áp theo thứ tự ưu tiên: tổng công ty → công ty → phòng ban → chỉ phiếu của mình.',
        '– Người có quyền Quản lý giữ hàng được xem mọi phiếu khác bản nháp.',
        '– Phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy.',
        '– Phạm vi này áp cho cả danh sách, màn chi tiết, bản in và tệp Excel xuất ra.',
    ], 'Toàn màn hình'),
    ('BR-11', 'Đơn vị tính của dòng hàng', [
        '– Tồn hàng giữ luôn ghi theo đơn vị cơ bản của hàng hóa nên cột ĐVT chỉ hiển thị.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xem chi tiết']),
])

d.save()
