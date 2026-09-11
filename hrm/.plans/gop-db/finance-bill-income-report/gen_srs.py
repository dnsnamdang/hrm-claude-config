# -*- coding: utf-8 -*-
"""Sinh SRS man PHIEU BAO CO (phan he Tai chinh) theo FORM CHUAN 2026-08-28.

Nguon du lieu:
  BE  Modules/Finance/{Entities/BillIncomeReport, Services/BillIncomeReport*,
      Http/Controllers/V1/BillIncomeReportController, Http/Requests/BillIncomeReport,
      Transformers/BillIncomeReportResource}
  FE  pages/finance/bill-income-reports/**
  Quyen: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (id 1542-1544)

Anh: chup that bang Playwright MCP 1440x900 -> bir_shots/ (dung chung voi HDSD).
Chay:  python .plans/gop-db/finance-bill-income-report/gen_srs.py
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

SHOTS = os.path.join(HERE, 'bir_shots')
OUT = os.path.join(HERE, 'SRS - Phieu bao co.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = ('Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu báo có')
MENU_SUM = ('Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt '
            '=> Tổng hợp tiền về ngân hàng')

ACTOR_KT = 'Kế toán quản lý phiếu báo có (Q1)'
ACTOR_VIEW = 'Người xem phiếu báo có (V1/V2)'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/bill-income-reports',
           full_url='http://hrm-crm.eteksofts.com/finance/bill-income-reports',
           img_prefix='bir_')

# ============================================================== TRANG DAU
d.title_block('Phiếu báo có')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu báo có và màn phụ đi kèm '
    'Tổng hợp tiền về ngân hàng thuộc phân hệ Tài chính, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của hai màn hình nêu trên.',
    'Làm rõ vòng đời hai bước Đang tạo → Đã duyệt và thời điểm hệ thống ghi bút toán '
    'vào sổ cái kế toán (không hoàn tác được).',
    'Làm rõ phạm vi dữ liệu người dùng nhìn thấy theo quyền xem theo cấp, và điều kiện '
    'được sửa / xóa / duyệt từng phiếu.',
    'Làm rõ cách bảng chi tiết đổi bộ cột theo Loại thu và các ràng buộc bắt buộc chọn '
    'hợp đồng, phiếu yêu cầu xuất hàng.',
    'Làm rõ luồng đối chiếu tiền về ngân hàng: từ dòng chi tiết đã duyệt sang phiếu '
    'yêu cầu điều chỉnh công nợ.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu báo có', 'Chứng từ kế toán ghi nhận tiền về tài khoản ngân hàng của công ty '
                     'theo sao kê, gắn khoản tiền đó với khách hàng / nhà cung cấp / hợp đồng.'),
    ('Đang tạo', 'Trạng thái nháp. Phiếu chưa ghi vào sổ cái, người lập còn sửa và xóa được.'),
    ('Đã duyệt', 'Trạng thái cuối. Hệ thống đã ghi bút toán vào sổ cái kế toán; phiếu không '
                 'sửa, không xóa được nữa.'),
    ('Ghi bút toán vào sổ cái', 'Việc hệ thống sinh các dòng hạch toán Nợ / Có tương ứng với '
                                'phiếu vào sổ kế toán chung. Đây là dữ liệu kế toán thật, '
                                'dùng chung với cổng ERP.'),
    ('Loại thu', 'Ba loại: Thu bán hàng, Thu nhà cung cấp, Thu khác. Loại thu quyết định bộ cột '
                 'của bảng Chi tiết.'),
    ('Tài khoản nợ / Tài khoản có', 'Cặp tài khoản kế toán của bút toán. Tài khoản nợ khai ở đầu '
                                    'phiếu, tài khoản có khai trên từng dòng chi tiết.'),
    ('KHÁCH KHÔNG RÕ', 'Khách hàng mặc định hệ thống điền sẵn cho dòng chi tiết khi chưa xác định '
                       'được tiền của ai; sau đó dùng màn Tổng hợp tiền về ngân hàng để gán lại '
                       'đúng đối tượng.'),
    ('Không báo tiền về', 'Đánh dấu một dòng chi tiết là không cần đối chiếu công nợ. Dòng đã đánh '
                          'dấu sẽ không xuất hiện ở màn Tổng hợp tiền về ngân hàng.'),
    ('Số tiền chưa điều chỉnh', 'Phần tiền của một dòng chi tiết chưa được xử lý bằng phiếu yêu '
                                'cầu điều chỉnh công nợ.'),
    ('Hợp đồng nguyên tắc', 'Loại hợp đồng bán mà một lần thu tiền phải gắn với một phiếu yêu cầu '
                            'xuất hàng cụ thể, hoặc được đánh dấu là thu dư nợ đầu kỳ.'),
    ('Phiếu YCXH', 'Phiếu yêu cầu xuất hàng.'),
], widths=[1.7, 4.3])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý phiếu báo có',
     'Hiện nút Tạo mới, Import Excel; cho phép Sửa, Xóa, Duyệt phiếu và tích ô '
     '“Không báo tiền về” ở màn chi tiết.'),
], widths=[0.8, 2.0, 3.2])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả phiếu báo có của tổng công ty',
     'Toàn bộ phiếu báo có của hệ thống.'),
    ('V2', 'Xem tất cả phiếu báo có của công ty',
     'Giới hạn theo công ty ghi trên phiếu, so với công ty của người đăng nhập.'),
    ('—', '(không có quyền xem theo cấp nào)', 'Chỉ những phiếu do chính mình lập.'),
], widths=[0.8, 2.0, 3.2])

d.p('Ba quyền trên đều thuộc nhóm quyền “Phiếu báo có”. Ngoài ra, dù có quyền xem ở cấp nào, '
    'phiếu đang ở trạng thái Đang tạo của người khác vẫn luôn bị ẩn với mọi người trừ chính '
    'người lập.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1', 'V2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách phiếu báo có', '✅', '✅ (toàn hệ thống)', '✅ (theo công ty)',
     '✅ (chỉ phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột hiển thị', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo mới phiếu báo có', '✅', '❌', '❌', '❌'),
    ('FR-06 Chọn đối tượng từ popup', '✅', '❌', '❌', '❌'),
    ('FR-07 Chỉnh sửa phiếu báo có', '✅ (phiếu Đang tạo do mình lập)', '❌', '❌', '❌'),
    ('FR-08 Xem chi tiết phiếu báo có', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-09 Duyệt phiếu báo có', '✅ (phiếu Đang tạo)', '❌', '❌', '❌'),
    ('FR-10 Xóa phiếu báo có', '✅ (phiếu Đang tạo do mình lập)', '❌', '❌', '❌'),
    ('FR-11 Đánh dấu Không báo tiền về', '✅', '❌', '❌', '❌'),
    ('FR-12 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅'),
    ('FR-13 Import Excel sao kê', '✅', '❌', '❌', '❌'),
    ('FR-14 Xem Tổng hợp tiền về ngân hàng', '✅', '✅', '✅', '✅'),
    ('FR-15 Xuất Excel màn tổng hợp', '✅', '✅', '✅', '✅'),
    ('FR-16 Chuyển sang tạo phiếu yêu cầu điều chỉnh công nợ', '✅', '✅', '✅', '✅'),
], widths=[2.0, 1.1, 1.1, 1.1, 1.2])

d.p('Ghi chú: màn Tổng hợp tiền về ngân hàng luôn giới hạn theo công ty của người đăng nhập, '
    'không phụ thuộc quyền xem theo cấp; người dùng không xác định được công ty thì màn không '
    'hiển thị dòng nào.')

# ================================================ PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR_KT, [0, 1, 2, 3, 4]),
     (ACTOR_VIEW, [0, 3, 4])],
    [('FR-01', 'Xem danh sách phiếu báo có', 'view'),
     ('FR-05', 'Tạo mới phiếu báo có', 'crud'),
     ('FR-07', 'Chỉnh sửa phiếu báo có', 'crud'),
     ('FR-08', 'Xem chi tiết phiếu báo có', 'view'),
     ('FR-14', 'Xem Tổng hợp tiền về ngân hàng', 'view')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0, 4], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-13', 'Import Excel sao kê', 'io', 'extend', [0], None),
     ('FR-06', 'Chọn đối tượng từ popup', 'crud', 'include', [1, 2], None),
     ('FR-09', 'Duyệt phiếu báo có', 'action', 'extend', [3], None),
     ('FR-10', 'Xóa phiếu báo có', 'action', 'extend', [3], None),
     ('FR-11', 'Đánh dấu Không báo tiền về', 'action', 'extend', [3], None),
     ('FR-12', 'Xem lịch sử thay đổi', 'view', 'extend', [3], None),
     ('FR-15', 'Xuất Excel màn tổng hợp', 'io', 'extend', [4], None),
     ('FR-16', 'Tạo phiếu yêu cầu điều chỉnh công nợ', 'action', 'extend', [4], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu báo có')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------- 2.1 Xem danh sach
d.h3('2.1 Xem danh sách phiếu báo có')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu báo có tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu báo có',
    mota='Hiển thị danh sách phiếu báo có nằm trong phạm vi dữ liệu của người đăng nhập, '
         'kèm bộ lọc, phân trang và các nút thao tác theo quyền.',
    tacnhan='Kế toán; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và mở được phân hệ Tài chính.',
    chinh='1. Người dùng vào menu Tài chính → Quản lý tiền → Thanh toán tiền mặt → Phiếu báo có.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo quyền xem theo cấp của người dùng.\n'
          '3. Hệ thống loại bỏ các phiếu Đang tạo do người khác lập.\n'
          '4. Hệ thống trả về trang đầu tiên, sắp xếp phiếu mới nhất lên trước, kèm tổng số '
          'bản ghi khớp bộ lọc.\n'
          '5. Bảng hiển thị dữ liệu; các nút Tạo mới, Import Excel chỉ hiện khi người dùng có '
          'quyền Quản lý phiếu báo có.',
    phu='• Không có bản ghi nào trong phạm vi → bảng hiện dòng “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Lỗi hệ thống khi nạp dữ liệu → hiển thị thông báo “Đã xảy ra lỗi hệ thống. '
        'Vui lòng thử lại.”\n'
        '• Người dùng đã lưu bộ lọc trước đó trong vòng 10 phút → hệ thống khôi phục lại bộ lọc.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Danh sách phiếu báo có lúc mới truy cập')
d.figure(shot('02-danh-sach-cot-phai.png'),
         'Phần bên phải của bảng: cột Trạng thái và cột Hành động', width_in=6.2)

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Danh sách phiếu báo có',
     'Hiển thị ở thanh tiêu đề và phía trên bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Chỉ hiện khi có quyền Quản lý phiếu báo có; mở màn Thêm phiếu báo có.'),
    ('Nút Import Excel', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Chỉ hiện khi có quyền Quản lý phiếu báo có; mở cửa sổ Import phiếu báo có.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục theo trang',
     'Cột cố định, không tắt được.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là đường dẫn mở màn chi tiết; sắp xếp được; cột cố định, không tắt được.'),
    ('Cột Loại thu', 'Table/Grid', 'Read-only', 'Thu bán hàng / Thu nhà cung cấp / Thu khác',
     'Theo dữ liệu', 'Phiếu cũ chưa xác định loại hiển thị dấu gạch ngang.'),
    ('Cột Tổng PS', 'Table/Grid', 'Read-only', 'Số ≥ 0', 'Theo dữ liệu',
     'Tổng số tiền nguyên tệ của phiếu, căn phải, có dấu ngăn cách nghìn; sắp xếp được.'),
    ('Cột Tỷ giá', 'Table/Grid', 'Read-only', 'Số ≥ 0', 'Theo dữ liệu',
     'Tỷ giá quy đổi sang đồng Việt Nam.'),
    ('Cột Tổng PS VND', 'Table/Grid', 'Read-only', 'Số ≥ 0', 'Theo dữ liệu',
     'Tổng số tiền quy đổi; sắp xếp được.'),
    ('Cột Ghi chú', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Diễn giải chung của phiếu; xuống dòng khi dài.'),
    ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Lấy theo dòng chi tiết đầu tiên, dạng “Mã - Tên”; phiếu loại Thu nhà cung cấp hiển thị '
     'nhà cung cấp.'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Thời điểm lập phiếu; sắp xếp được.'),
    ('Cột Ngày hạch toán', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
     'Ngày ghi nhận tiền về; sắp xếp được.'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người lập phiếu.'),
    ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Phòng ban của người lập; bật lại ở cửa sổ Tuỳ chỉnh cột.'),
    ('Cột Số TK ngân hàng', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Số tài khoản công ty nhận tiền.'),
    ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn mặc định',
     'Lần sửa gần nhất.'),
    ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Ẩn mặc định',
     'Người sửa gần nhất.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Đang tạo / Đã duyệt', 'Theo dữ liệu',
     'Đang tạo hiển thị màu xám, Đã duyệt hiển thị màu xanh.'),
    ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Theo trạng thái và quyền',
     'Gồm Sửa, Xóa, và menu “…” chứa Duyệt, Lịch sử. Nút không dùng được thì ẩn hẳn, '
     'không hiện nút mờ.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc trong phạm vi dữ liệu của người dùng.'),
    ('Phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100 dòng', 'Trang 1, 10 dòng',
     'Có nút về đầu / lùi / số trang / tiến / về cuối và ô chọn số dòng mỗi trang.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi không có phiếu nào.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định quyền xem theo cấp của người dùng.\n'
     'During:\n– Áp phạm vi dữ liệu: có quyền xem của tổng công ty thì lấy toàn hệ thống; '
     'chỉ có quyền xem của công ty thì lọc theo công ty của người đăng nhập; không có quyền '
     'nào thì chỉ lấy phiếu do chính mình lập.\n'
     '– Loại bỏ phiếu Đang tạo do người khác lập.\n'
     'After:\n– Trả về trang 1 sắp xếp phiếu mới nhất trước, kèm tổng số bản ghi và cờ quyền '
     'thao tác để hiện/ẩn nút.'),
    ('Bấm vào Mã phiếu', 'Click',
     'After:\n– Mở màn Chi tiết phiếu báo có tương ứng.'),
    ('Bấm tiêu đề cột có mũi tên sắp xếp', 'Click',
     'During:\n– Chỉ các cột Mã phiếu, Tổng PS, Tổng PS VND, Ngày hạch toán, Ngày tạo được '
     'sắp xếp.\n'
     'After:\n– Nạp lại danh sách từ trang 1 theo thứ tự mới, giữ nguyên bộ lọc.'),
    ('Bấm số trang / đổi số dòng mỗi trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu, số thứ tự tiếp tục liên tục theo trang.'),
])

# ------------------------------------------------- 2.2 Tim kiem va loc
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các tiêu chí lọc riêng của '
           'màn Phiếu báo có tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu báo có',
    mota='Thu hẹp danh sách theo mã phiếu, loại thu, trạng thái, người tạo, ngân hàng, '
         'tài khoản, khách hàng, ghi chú, cờ không báo tiền về và các khoảng ngày.',
    tacnhan='Kế toán; Người dùng đã đăng nhập',
    dieukien='Đang ở màn Danh sách phiếu báo có.',
    chinh='1. Người dùng gõ mã phiếu vào ô tìm nhanh rồi bấm Tìm kiếm, hoặc bấm '
          '“Tìm kiếm nâng cao” để mở bảng lọc.\n'
          '2. Người dùng chọn/nhập các tiêu chí cần lọc.\n'
          '3. Hệ thống nạp lại danh sách từ trang 1 theo điều kiện lọc.\n'
          '4. Hệ thống ghi nhớ bộ lọc trong 10 phút cho lần vào màn kế tiếp.',
    phu='• Bấm “Làm mới” → xóa toàn bộ điều kiện lọc và nạp lại danh sách đầy đủ.\n'
        '• Ô tìm nhanh chỉ chạy khi bấm nút Tìm kiếm hoặc nhấn Enter; các ô còn lại tự lọc '
        'ngay khi thay đổi.\n'
        '• Ô Khách hàng yêu cầu gõ tối thiểu 2 ký tự mới gợi ý danh sách.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('03-bo-loc-nang-cao.png'),
         shot_caption='Bảng tìm kiếm nâng cao của màn Phiếu báo có')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh theo mã phiếu', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Trống',
     'Tìm tương đối theo mã phiếu; chỉ chạy khi bấm Tìm kiếm hoặc nhấn Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', 'Hiển thị', 'Áp dụng điều kiện đang nhập.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Xóa hết điều kiện lọc và nạp lại danh sách.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', 'Đang thu gọn',
     'Mở / đóng bảng lọc nhiều tiêu chí.'),
    ('Ô Công ty – Phòng ban – Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách đơn vị',
     'Ẩn khi không có quyền xem theo cấp',
     'Chỉ hiện với người có quyền xem tất cả phiếu báo có của tổng công ty hoặc của công ty.'),
    ('Ô Loại thu', 'Dropdown', 'Enable', 'Thu bán hàng / Thu nhà cung cấp / Thu khác', 'Trống',
     'Lọc đúng một loại thu.'),
    ('Ô Trạng thái', 'Dropdown', 'Enable', 'Đang tạo / Đã duyệt', 'Trống', '–'),
    ('Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống',
     'Lọc theo người lập phiếu.'),
    ('Ô Ngân hàng', 'Dropdown', 'Enable', 'Danh sách ngân hàng', 'Trống', '–'),
    ('Ô Tài khoản ngân hàng', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Trống',
     'Tìm tương đối theo số tài khoản công ty ghi trên phiếu.'),
    ('Ô Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng', 'Trống',
     'Gõ tối thiểu 2 ký tự để tìm; lọc theo khách hàng gắn ở dòng chi tiết.'),
    ('Ô Tên khách hàng (gõ tay)', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Trống',
     'Tìm tương đối theo chuỗi “Mã - Tên” của khách hàng.'),
    ('Ô Ghi chú', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Trống',
     'Tìm tương đối theo diễn giải chung của phiếu.'),
    ('Ô Không báo tiền về', 'Dropdown', 'Enable', 'Có / Không', 'Trống',
     'Chọn “Có” lấy phiếu có ít nhất một dòng đã đánh dấu; chọn “Không” lấy phiếu không có '
     'dòng nào đánh dấu.'),
    ('Ô Hạch toán từ / Hạch toán đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống',
     'Lọc theo ngày hạch toán, lấy cả hai đầu mốc.'),
    ('Ô Ngày tạo từ / Ngày tạo đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống',
     'Lọc theo ngày lập phiếu, lấy cả hai đầu mốc.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Thay đổi một ô lọc trong bảng nâng cao', 'Change',
     'During:\n– Đưa danh sách về trang 1.\n'
     'After:\n– Nạp lại dữ liệu theo toàn bộ điều kiện đang có và ghi nhớ bộ lọc trong 10 phút.'),
    ('Bấm Tìm kiếm', 'Click',
     'After:\n– Áp dụng cả ô tìm nhanh lẫn các ô nâng cao, nạp lại từ trang 1.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Xóa toàn bộ điều kiện lọc, xóa cả lựa chọn khách hàng đã chọn, nạp lại danh sách '
     'đầy đủ trong phạm vi dữ liệu của người dùng.'),
])

# ------------------------------------------------- 2.3 Cai dat bo loc
d.h3('2.3 Cài đặt bộ lọc')

d.p('2.3.1 Giới thiệu')
d.rule_ref('- Bộ lọc và Cấu hình cột. Chỉ bổ sung phần riêng của màn Phiếu báo có tại phần '
           'mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Cài đặt bộ lọc hiển thị',
    mota='Chọn những tiêu chí lọc muốn hiển thị và sắp xếp thứ tự của chúng trong bảng '
         'tìm kiếm nâng cao. Cài đặt lưu riêng cho từng người dùng và từng màn hình.',
    tacnhan='Kế toán; Người dùng đã đăng nhập',
    dieukien='Đang ở màn Danh sách phiếu báo có.',
    chinh='1. Người dùng bấm nút “Cài đặt bộ lọc”.\n'
          '2. Hệ thống mở cửa sổ liệt kê 12 tiêu chí lọc kèm ô tích và tay cầm kéo thả.\n'
          '3. Người dùng tích/bỏ tích, kéo thả để đổi thứ tự rồi bấm Lưu.\n'
          '4. Hệ thống lưu cài đặt và vẽ lại bảng lọc theo đúng lựa chọn.',
    phu='• Bấm “Khôi phục mặc định” → đưa danh sách tiêu chí về cấu hình gốc.\n'
        '• Bỏ tích một tiêu chí đang có giá trị → hệ thống xóa luôn giá trị đó để tránh lọc ngầm '
        'bằng ô không nhìn thấy.',
    dacbiet=None)

d.p('2.3.2 Layout màn hình')
d.layout(menu=MENU, modal='Cài đặt bộ lọc', shot=shot('04-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc của màn Phiếu báo có')

d.p('2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách tiêu chí lọc', 'Table/Grid', 'Enable', '12 tiêu chí', 'Tất cả được tích',
     'Gồm: Công ty – Phòng ban – Bộ phận, Loại thu, Trạng thái, Người tạo, Ngân hàng, '
     'Tài khoản ngân hàng, Khách hàng, Tên khách hàng (gõ tay), Ghi chú, Không báo tiền về, '
     'Khoảng ngày hạch toán, Khoảng ngày tạo.'),
    ('Tay cầm kéo thả', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Kéo để đổi thứ tự hiển thị của tiêu chí.'),
    ('Nút Lưu', 'Button', 'Enable', '–', 'Hiển thị', 'Lưu cài đặt cho riêng người dùng.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', 'Hiển thị',
     'Đưa về cấu hình gốc của màn.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ, không lưu thay đổi.'),
], required=False)

d.p('2.3.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu danh sách tiêu chí hiển thị và thứ tự cho người dùng hiện tại.\n'
     '– Hiển thị thông báo “Cập nhật thành công” và vẽ lại bảng lọc.'),
    ('Bỏ tích một tiêu chí đang có giá trị', 'Change',
     'After:\n– Ẩn ô lọc và xóa giá trị đang nhập của tiêu chí đó.'),
])

# ------------------------------------------------- 2.4 Tuy chinh cot
d.h3('2.4 Tuỳ chỉnh cột hiển thị')

d.p('2.4.1 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung phần riêng của màn Phiếu báo có tại '
           'phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh cột hiển thị của danh sách',
    mota='Chọn cột muốn hiển thị và thứ tự cột trên bảng danh sách. Cài đặt lưu riêng cho '
         'từng người dùng.',
    tacnhan='Kế toán; Người dùng đã đăng nhập',
    dieukien='Đang ở màn Danh sách phiếu báo có.',
    chinh='1. Người dùng bấm biểu tượng Cấu hình cột hiển thị ở góc phải thanh công cụ.\n'
          '2. Hệ thống mở cửa sổ Tuỳ chỉnh cột với danh sách 17 cột.\n'
          '3. Người dùng tích/bỏ tích, kéo thả đổi thứ tự rồi bấm Lưu.\n'
          '4. Hệ thống lưu cấu hình và vẽ lại bảng.',
    phu='• Ba cột STT, Mã phiếu và Hành động bị khóa, không bỏ tích và không đổi vị trí được.\n'
        '• Bốn cột Phòng ban, Số TK ngân hàng, Ngày cập nhật, Người cập nhật mặc định tắt.',
    dacbiet=None)

d.p('2.4.2 Layout màn hình')
d.layout(menu=MENU, modal='Tuỳ chỉnh cột', shot=shot('05-cau-hinh-cot.png'),
         shot_caption='Cửa sổ Tuỳ chỉnh cột của màn Phiếu báo có')

d.p('2.4.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách cột', 'Table/Grid', 'Enable', '17 cột', 'Theo cấu hình đã lưu',
     'Mỗi dòng gồm ô tích và tay cầm kéo thả.'),
    ('Cột bị khóa', 'Icon', 'Read-only', '–', 'Hiển thị ổ khóa',
     'STT, Mã phiếu, Hành động — không ẩn và không đổi vị trí được.'),
    ('Nút Lưu', 'Button', 'Enable', '–', 'Hiển thị', 'Lưu cấu hình cột cho người dùng.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng, không lưu.'),
], required=False)

d.p('2.4.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'After:\n– Lưu cấu hình cột cho người dùng hiện tại.\n'
     '– Hiển thị thông báo “Cập nhật thành công” và vẽ lại bảng theo cấu hình mới.'),
])

# ------------------------------------------------- 2.5 Tao moi
d.h3('2.5 Tạo mới phiếu báo có')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Tạo mới phiếu báo có', 'crud',
            [('include', 'Kiểm tra quyền Quản lý phiếu báo có'),
             ('include', 'Sinh mã phiếu tự động'),
             ('include', 'Chọn đối tượng từ popup'),
             ('extend', 'Duyệt và ghi bút toán vào sổ cái')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-05 Tạo mới phiếu báo có')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới phiếu báo có',
    mota='Lập một phiếu ghi nhận tiền về tài khoản ngân hàng, gồm thông tin chung của phiếu và '
         'ít nhất một dòng chi tiết. Người dùng chọn lưu nháp hoặc lưu và duyệt ngay.',
    tacnhan='Kế toán có quyền Quản lý phiếu báo có',
    dieukien='Người dùng có quyền Quản lý phiếu báo có.',
    chinh='1. Người dùng bấm nút Tạo mới ở màn danh sách.\n'
          '2. Hệ thống mở màn Thêm phiếu báo có với các giá trị mặc định: Loại thu Thu bán hàng, '
          'Tài khoản nợ 1121, Loại tiền VNĐ, Tỷ giá 1, Ngày hạch toán là ngày hiện tại, và một '
          'dòng chi tiết trống với tài khoản có 1311, khách hàng KHÁCH KHÔNG RÕ.\n'
          '3. Người dùng chọn Ngân hàng, chọn Tài khoản; hệ thống tự điền Chi nhánh.\n'
          '4. Người dùng nhập các dòng chi tiết: chọn tài khoản có, chọn đối tượng, nhập số tiền '
          'và diễn giải.\n'
          '5. Người dùng bấm Lưu (giữ trạng thái Đang tạo) hoặc Lưu và duyệt.\n'
          '6. Hệ thống kiểm tra dữ liệu, sinh mã phiếu, ghi phiếu và các dòng chi tiết, cập nhật '
          'hai ô tổng tiền.\n'
          '7. Nếu chọn Lưu và duyệt, hệ thống chuyển trạng thái sang Đã duyệt và ghi bút toán vào '
          'sổ cái, đồng thời gửi thông báo cho những người giữ quyền Quản lý phiếu báo có cùng '
          'công ty.\n'
          '8. Hệ thống hiển thị thông báo thành công và quay về danh sách.',
    phu='• Thiếu trường bắt buộc → báo lỗi đỏ ngay dưới ô tương ứng, không rời màn, giữ nguyên '
        'dữ liệu đã nhập.\n'
        '• Đổi Loại thu khi bảng chi tiết đã có dữ liệu → hệ thống hỏi xác nhận rồi xóa toàn bộ '
        'dòng chi tiết và tạo lại một dòng trống.\n'
        '• Bấm “Lưu và tiếp tục” → lưu phiếu ở trạng thái Đang tạo và ở lại màn Tạo mới với form '
        'trống để nhập phiếu kế tiếp.\n'
        '• Rời màn khi đã nhập mà chưa lưu → hệ thống hỏi xác nhận rời trang.\n'
        '• Không có quyền Quản lý phiếu báo có → nút Tạo mới không hiển thị; gọi thẳng chức năng '
        'thì hệ thống từ chối và báo không có quyền.',
    dacbiet='Chọn Lưu và duyệt là ghi thẳng bút toán vào sổ cái kế toán dùng chung, không hoàn '
            'tác được; sau đó phiếu không sửa và không xóa được nữa.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', shot=shot('06-form-tao-moi.png'),
         shot_caption='Form Tạo mới phiếu báo có — loại thu Thu bán hàng')
d.figure(shot('07-form-bang-chi-tiet-phai.png'),
         'Phần bên phải bảng Chi tiết: Số tiền, Diễn giải, Không báo tiền về, Xóa dòng',
         width_in=6.2)
d.figure(shot('11-form-loai-thu-ncc.png'),
         'Form khi chọn loại thu Thu nhà cung cấp — bảng chi tiết đổi bộ cột', width_in=6.2)
d.figure(shot('14-form-loai-thu-khac.png'),
         'Form khi chọn loại thu Thu khác — không có cột hợp đồng, khách hàng không bắt buộc',
         width_in=6.2)

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Loại thu', 'Dropdown', 'Enable', 'Thu bán hàng / Thu nhà cung cấp / Thu khác', 'Có',
     'Thu bán hàng', 'Đổi giá trị sẽ xóa toàn bộ dòng chi tiết đang nhập (có hỏi xác nhận).'),
    ('Tài khoản nợ', 'Dropdown', 'Enable', 'Danh mục tài khoản đang hoạt động', 'Có',
     '1121 - Tiền Việt Nam', 'Tài khoản ghi Nợ của bút toán.'),
    ('Loại tiền', 'Dropdown', 'Enable', 'Danh mục loại tiền', 'Có', 'VNĐ',
     'Chọn ngoại tệ sẽ mở khóa ô Tỷ giá và hiện thêm cột số tiền quy đổi.'),
    ('Tỷ giá (VND)', 'Number', 'Enable / Disable', 'Số > 0', 'Có', '1',
     'Khóa và luôn bằng 1 khi Loại tiền là VNĐ; đổi tỷ giá sẽ tính lại toàn bộ cột quy đổi.'),
    ('Ngày hạch toán', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Ngày hiện tại',
     'Ngày ghi nhận tiền về, dùng làm ngày hạch toán của bút toán.'),
    ('Ngân hàng', 'Dropdown', 'Enable', 'Danh mục ngân hàng', 'Có', 'Trống',
     'Đổi ngân hàng sẽ xóa Tài khoản và Chi nhánh đã chọn.'),
    ('Tài khoản', 'Dropdown', 'Enable / Disable', 'Tài khoản của ngân hàng đã chọn', 'Có',
     'Trống', 'Bị khóa cho tới khi chọn Ngân hàng.'),
    ('Chi nhánh', 'Textbox', 'Read-only', '–', '–', 'Trống',
     'Tự điền theo tài khoản đã chọn.'),
    ('Diễn giải', 'Textbox', 'Enable', '0–500 ký tự', 'Không', 'Trống',
     'Diễn giải chung của phiếu; quá 500 ký tự báo “Tối đa 500 ký tự”.'),
    ('Nút Thêm dòng', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Thêm một dòng chi tiết mới với giá trị mặc định theo loại thu.'),
    ('Cột Số tài khoản có', 'Dropdown', 'Enable', 'Danh mục tài khoản', 'Có',
     '1311 với Thu bán hàng, 3311 với Thu nhà cung cấp, trống với Thu khác',
     'Tài khoản ghi Có của dòng.'),
    ('Cột Tên tài khoản', 'Text', 'Read-only', '–', '–', 'Theo tài khoản đã chọn', '–'),
    ('Cột Khách hàng', 'Textbox', 'Read-only', '–', 'Có với Thu bán hàng',
     'KHÁCH KHÔNG RÕ', 'Bấm vào ô để mở cửa sổ Chọn khách hàng; chỉ hiện với loại thu '
     'Thu bán hàng và Thu khác.'),
    ('Cột Nhà cung cấp', 'Textbox', 'Read-only', '–', 'Có với Thu nhà cung cấp',
     'KHÁCH KHÔNG RÕ', 'Chỉ hiện với loại thu Thu nhà cung cấp; bấm để mở cửa sổ chọn.'),
    ('Cột Số đơn hàng/Hợp đồng', 'Textbox', 'Read-only', '–',
     'Có khi tài khoản có là công nợ và khách hàng khác KHÁCH KHÔNG RÕ', 'Trống',
     'Bấm để mở cửa sổ Chọn đơn hàng/hợp đồng của đúng khách hàng đã chọn.'),
    ('Ô tích Số dư nợ đầu kì', 'Checkbox', 'Enable / Ẩn', '–', '–', 'Không tích',
     'Chỉ hiện khi hợp đồng đã chọn là hợp đồng nguyên tắc; tích vào thì không phải chọn '
     'phiếu yêu cầu xuất hàng.'),
    ('Cột Phiếu YC xuất hàng', 'Textbox', 'Read-only', '–',
     'Có khi hợp đồng là hợp đồng nguyên tắc và không tích dư nợ đầu kì', 'Trống',
     'Bấm để mở cửa sổ Chọn phiếu yêu cầu xuất hàng của hợp đồng đó.'),
    ('Cột Phiếu xuất hàng', 'Textbox', 'Read-only', '–', 'Không', 'Trống',
     'Chỉ hiện với loại thu Thu nhà cung cấp; chọn xong hệ thống tự điền Hợp đồng mua và NVKD.'),
    ('Cột Hợp đồng mua', 'Text', 'Read-only', '–', '–', 'Trống',
     'Tự điền theo phiếu xuất hàng đã chọn.'),
    ('Cột NVKD', 'Text', 'Read-only', '–', '–', 'Trống',
     'Người tạo hợp đồng gắn với dòng.'),
    ('Cột Số tiền', 'Number', 'Enable', 'Số > 0', 'Có', '0',
     'Số tiền nguyên tệ; để trống hoặc bằng 0 sẽ báo “Số tiền phải lớn hơn 0”.'),
    ('Cột Số tiền (VND)', 'Text', 'Read-only', '–', '–', 'Tự tính',
     'Chỉ hiện khi loại tiền là ngoại tệ; bằng Số tiền nhân Tỷ giá.'),
    ('Cột Diễn giải', 'Textbox', 'Enable', '0–500 ký tự', 'Có', 'Trống',
     'Bỏ trống sẽ báo “Bắt buộc nhập”.'),
    ('Cột Không báo tiền về', 'Checkbox', 'Enable', '–', '–', 'Không tích',
     'Dòng được tích sẽ không xuất hiện ở màn Tổng hợp tiền về ngân hàng.'),
    ('Nút Xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Xóa dòng chi tiết khỏi bảng.'),
    ('Dòng Tổng cộng', 'Label', 'Read-only', '–', '–', 'Tự tính',
     'Tổng số tiền của tất cả dòng chi tiết, cập nhật ngay khi nhập.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu phiếu ở trạng thái Đang tạo.'),
    ('Nút Lưu và duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu rồi duyệt ngay và ghi bút toán vào sổ cái; có hộp hỏi xác nhận trước.'),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable', '–', '–', 'Hiển thị ở màn Tạo mới',
     'Lưu nháp rồi ở lại màn Tạo mới với form trống.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Về danh sách; hỏi xác nhận nếu có thay đổi chưa lưu.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý phiếu báo có.\n'
     '– Nếu không có quyền → nút không hiển thị; gọi thẳng chức năng thì hệ thống báo '
     '“Bạn không có quyền lập phiếu báo có” và dừng xử lý.\n'
     'After:\n– Mở màn Thêm phiếu báo có với đầy đủ giá trị mặc định và một dòng chi tiết trống.'),
    ('Đổi Loại thu', 'Change',
     'During:\n– Nếu bảng chi tiết đã có số tiền, hợp đồng hoặc diễn giải → hiển thị hộp xác nhận '
     '“Đổi loại thu sẽ xóa toàn bộ dòng chi tiết đang nhập. Bạn có chắc chắn?”.\n'
     'After:\n– Chọn Đồng ý thì xóa hết dòng chi tiết, tạo một dòng mới theo mặc định của loại '
     'thu mới; chọn Hủy thì giữ nguyên loại thu cũ.'),
    ('Đổi Loại tiền', 'Change',
     'After:\n– Lấy tỷ giá của loại tiền đó; chọn VNĐ thì tỷ giá về 1 và ô tỷ giá bị khóa.'),
    ('Đổi Ngân hàng', 'Change',
     'After:\n– Xóa Tài khoản và Chi nhánh đã chọn; danh sách Tài khoản chỉ còn tài khoản của '
     'ngân hàng vừa chọn.'),
    ('Chọn Tài khoản', 'Change', 'After:\n– Tự điền ô Chi nhánh theo tài khoản đã chọn.'),
    ('Nhập Số tiền của một dòng', 'Change',
     'After:\n– Tính lại cột số tiền quy đổi của dòng và dòng Tổng cộng.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý phiếu báo có; không có quyền thì từ chối và báo '
     '“Bạn không có quyền lập phiếu báo có”.\n'
     'During:\n'
     '– Loại thu, Tài khoản nợ, Loại tiền, Ngân hàng, Tài khoản để trống → hiển thị '
     '“Bắt buộc chọn” dưới ô tương ứng.\n'
     '– Tỷ giá, Ngày hạch toán để trống → hiển thị “Bắt buộc nhập”.\n'
     '– Ngày hạch toán sai định dạng → hiển thị “Không đúng định dạng”.\n'
     '– Bảng chi tiết không có dòng nào → hiển thị “Phải có ít nhất 1 dòng chi tiết”.\n'
     '– Tài khoản có của dòng để trống → “Bắt buộc chọn”.\n'
     '– Số tiền của dòng bằng 0 hoặc bỏ trống → “Số tiền phải lớn hơn 0”.\n'
     '– Diễn giải của dòng để trống → “Bắt buộc nhập”; quá 500 ký tự → “Tối đa 500 ký tự”.\n'
     '– Loại thu Thu bán hàng mà chưa chọn khách hàng → “Bắt buộc chọn”.\n'
     '– Loại thu Thu nhà cung cấp mà chưa chọn nhà cung cấp → “Bắt buộc chọn”.\n'
     '– Tài khoản có là tài khoản công nợ và khách hàng khác KHÁCH KHÔNG RÕ mà chưa chọn hợp đồng '
     '→ “Bắt buộc chọn”.\n'
     '– Hợp đồng nguyên tắc, không tích dư nợ đầu kì mà chưa chọn phiếu yêu cầu xuất hàng '
     '→ “Bắt buộc chọn”.\n'
     '– Nếu có lỗi thì không thực hiện bước After.\n'
     'After:\n– Sinh mã phiếu theo dạng “mã công ty . PBC tháng năm . số thứ tự 5 chữ số”.\n'
     '– Ghi phiếu ở trạng thái Đang tạo cùng toàn bộ dòng chi tiết, tính lại hai ô tổng tiền.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Hiển thị “Thêm phiếu báo có thành công!” và quay về danh sách.'),
    ('Bấm Lưu và duyệt', 'Click',
     'Before:\n– Hiển thị hộp xác nhận lưu và duyệt.\n'
     'During:\n– Kiểm tra dữ liệu như bước Lưu.\n'
     'After:\n– Ghi phiếu, chuyển trạng thái sang Đã duyệt, ghi người duyệt.\n'
     '– Sinh bút toán Nợ / Có tương ứng và ghi vào sổ cái kế toán.\n'
     '– Ghi dòng lịch sử “Thay đổi trạng thái: Đang tạo → Đã duyệt” kèm ghi chú đã ghi bút toán.\n'
     '– Gửi thông báo tới những người có quyền Quản lý phiếu báo có trong cùng công ty.\n'
     '– Hiển thị “Thêm phiếu báo có thành công! Phiếu đã được duyệt và ghi bút toán vào sổ cái.” '
     'và quay về danh sách.'),
    ('Bấm Quay lại khi đã nhập mà chưa lưu', 'Click',
     'During:\n– Hiển thị hộp hỏi xác nhận rời trang.\n'
     'After:\n– Chọn ở lại thì giữ nguyên dữ liệu; chọn rời đi thì bỏ mọi thay đổi.'),
])

# ------------------------------------------------- 2.6 Popup chon doi tuong
d.h3('2.6 Chọn đối tượng từ popup')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Chọn đối tượng từ popup', 'crud',
            [('include', 'Chọn khách hàng'),
             ('include', 'Chọn nhà cung cấp'),
             ('include', 'Chọn đơn hàng / hợp đồng'),
             ('include', 'Chọn phiếu xuất hàng'),
             ('include', 'Chọn phiếu yêu cầu xuất hàng')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-06 Chọn đối tượng từ popup')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung phần riêng của màn '
           'Phiếu báo có tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Chọn đối tượng cho dòng chi tiết',
    mota='Năm cửa sổ tra cứu dùng cho bảng Chi tiết: chọn khách hàng, chọn nhà cung cấp, '
         'chọn đơn hàng/hợp đồng, chọn phiếu xuất hàng và chọn phiếu yêu cầu xuất hàng.',
    tacnhan='Kế toán có quyền Quản lý phiếu báo có',
    dieukien='Đang ở màn Tạo mới hoặc Chỉnh sửa phiếu báo có.',
    chinh='1. Người dùng bấm vào ô tương ứng trên dòng chi tiết.\n'
          '2. Hệ thống mở cửa sổ tra cứu kèm ô tìm kiếm và bảng kết quả có phân trang.\n'
          '3. Người dùng gõ từ khóa, bấm Tìm kiếm rồi bấm vào dòng muốn chọn.\n'
          '4. Hệ thống điền giá trị vào dòng chi tiết và đóng cửa sổ.',
    phu='• Chưa chọn khách hàng mà bấm ô hợp đồng → báo “Chưa chọn khách hàng”.\n'
        '• Chưa chọn nhà cung cấp mà bấm ô phiếu xuất → báo “Chưa chọn nhà cung cấp”.\n'
        '• Chưa chọn hợp đồng mà bấm ô phiếu yêu cầu xuất hàng → báo “Chưa chọn hợp đồng”.\n'
        '• Chọn lại khách hàng hoặc nhà cung cấp → hệ thống xóa hợp đồng, phiếu xuất và phiếu '
        'yêu cầu xuất hàng đã chọn trước đó trên dòng.\n'
        '• Chọn trùng một phiếu xuất đã có ở dòng khác → báo “Phiếu đã tồn tại!”.\n'
        '• Hợp đồng đã dùng ở dòng khác của cùng phiếu → cửa sổ không cho chọn lại.',
    dacbiet=None)

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới', modal='Chọn khách hàng',
         shot=shot('08-popup-chon-khach-hang.png'),
         shot_caption='Cửa sổ Chọn khách hàng')
d.figure(shot('09-popup-chon-hop-dong.png'),
         'Cửa sổ Chọn đơn hàng/hợp đồng của khách hàng đã chọn', width_in=6.2)
d.figure(shot('12-popup-chon-ncc.png'), 'Cửa sổ Chọn nhà cung cấp', width_in=6.2)
d.figure(shot('13-popup-chon-phieu-xuat.png'),
         'Cửa sổ Chọn phiếu xuất hàng (trạng thái không có dữ liệu phù hợp)', width_in=6.2)

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Cửa sổ Chọn khách hàng', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Có ba ô tìm kiếm: Tên / Mã khách hàng, Mã số thuế, Số điện thoại; bảng hiển thị Mã KH - '
     'Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ.'),
    ('Cửa sổ Chọn nhà cung cấp', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Ô tìm theo Mã / Tên nhà cung cấp; bảng hiển thị Mã và Tên nhà cung cấp.'),
    ('Cửa sổ Chọn đơn hàng/hợp đồng', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Tiêu đề kèm tên khách hàng đang chọn; bảng hiển thị Số đơn hàng/Hợp đồng, Ngày lập, '
     'Giá trị hợp đồng, Số tiền còn nợ.'),
    ('Cửa sổ Chọn phiếu xuất hàng', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Chỉ liệt kê phiếu xuất trả nhà cung cấp của đúng nhà cung cấp đã chọn; bảng hiển thị '
     'Mã phiếu, Ngày lập, Người lập.'),
    ('Cửa sổ Chọn phiếu yêu cầu xuất hàng', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Chỉ liệt kê phiếu của hợp đồng đã chọn, bỏ các phiếu hàng khuyến mại; có thêm ô lọc '
     'Loại yêu cầu xuất.'),
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Tìm theo từ khóa hoặc xóa từ khóa và tải lại danh sách.'),
    ('Phân trang trong cửa sổ', 'Pagination', 'Enable', '–', '–', 'Trang 1',
     'Cho phép đổi số dòng mỗi trang.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện câu nhắc chọn đối tượng cha (khách hàng / nhà cung cấp / hợp đồng) hoặc thông báo '
     'không có dữ liệu phù hợp.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm ô chọn trên dòng chi tiết', 'Click',
     'Before:\n– Kiểm tra đối tượng cha đã được chọn chưa (khách hàng trước hợp đồng, nhà cung '
     'cấp trước phiếu xuất, hợp đồng trước phiếu yêu cầu xuất hàng).\n'
     'After:\n– Mở cửa sổ tra cứu tương ứng, giới hạn dữ liệu theo đối tượng cha.'),
    ('Bấm một dòng trong cửa sổ', 'Click',
     'After:\n– Điền mã và tên đối tượng vào dòng chi tiết, đóng cửa sổ.\n'
     '– Chọn khách hàng hoặc nhà cung cấp thì xóa hợp đồng, phiếu xuất, phiếu yêu cầu xuất hàng '
     'đã chọn trước đó của dòng.\n'
     '– Chọn hợp đồng thì xóa phiếu yêu cầu xuất hàng cũ, và hiện ô tích dư nợ đầu kì nếu là '
     'hợp đồng nguyên tắc.\n'
     '– Chọn phiếu xuất hàng thì tự điền Hợp đồng mua và NVKD; phiếu xuất không có hợp đồng mua '
     'tương ứng thì báo lỗi và không điền.'),
])

# ------------------------------------------------- 2.7 Chinh sua
d.h3('2.7 Chỉnh sửa phiếu báo có')

d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Chỉnh sửa phiếu báo có', 'crud',
            [('include', 'Kiểm tra quyền và điều kiện sửa'),
             ('include', 'Chọn đối tượng từ popup'),
             ('extend', 'Duyệt và ghi bút toán vào sổ cái')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-07 Chỉnh sửa phiếu báo có')

d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Chỉnh sửa phiếu báo có',
    mota='Sửa thông tin chung và các dòng chi tiết của một phiếu đang ở trạng thái Đang tạo '
         'do chính người dùng lập.',
    tacnhan='Kế toán có quyền Quản lý phiếu báo có và là người lập phiếu',
    dieukien='Phiếu ở trạng thái Đang tạo và do chính người dùng lập.',
    chinh='1. Người dùng bấm nút Sửa ở dòng danh sách hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở màn Sửa phiếu báo có, đổ sẵn dữ liệu hiện có, ô Mã phiếu để chỉ đọc.\n'
          '3. Người dùng chỉnh sửa thông tin chung hoặc các dòng chi tiết.\n'
          '4. Người dùng bấm Lưu hoặc Lưu và duyệt.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi lại toàn bộ dòng chi tiết, cập nhật hai ô tổng tiền '
          'và ghi lịch sử phần đã thay đổi.',
    phu='• Phiếu đã duyệt hoặc không phải của mình → nút Sửa không hiển thị; vào thẳng bằng đường '
        'dẫn thì hệ thống đưa về màn chi tiết và báo phiếu không sửa được.\n'
        '• Phiếu đã bị xóa ở nơi khác → báo “Không tìm thấy dữ liệu”.\n'
        '• Rời màn khi đã sửa mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
    dacbiet='Mã phiếu, người lập và phòng ban là thông tin chỉ đọc, không sửa được.')

d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa', shot=shot('22-man-sua.png'),
         shot_caption='Màn Sửa phiếu báo có với dữ liệu thật')

d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mã phiếu', 'Textbox', 'Read-only', '–', '–', 'Theo dữ liệu', 'Không sửa được.'),
    ('Người lập', 'Textbox', 'Read-only', '–', '–', 'Theo dữ liệu', 'Người tạo phiếu.'),
    ('Phòng ban', 'Textbox', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Phòng ban của người lập phiếu.'),
    ('Các ô thông tin chung còn lại', 'Dropdown / Datepicker / Number / Textbox', 'Enable',
     'Như màn Tạo mới', 'Như màn Tạo mới', 'Theo dữ liệu',
     'Quy tắc nhập giống hệt màn Tạo mới.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', 'Ít nhất 1 dòng', 'Có', 'Theo dữ liệu',
     'Thêm, sửa, xóa dòng như màn Tạo mới.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Giữ trạng thái Đang tạo.'),
    ('Nút Lưu và duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu rồi duyệt và ghi bút toán vào sổ cái.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Về danh sách; hỏi xác nhận nếu có thay đổi chưa lưu.'),
])

d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System',
     'Before:\n– Nạp dữ liệu phiếu và kiểm tra điều kiện sửa.\n'
     'After:\n– Phiếu không sửa được thì chuyển sang màn chi tiết; sửa được thì đổ dữ liệu vào '
     'form, giữ nguyên cả tài khoản ngân hàng đã bị khóa để không mất giá trị cũ.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý phiếu báo có; thiếu quyền thì báo “Bạn không có quyền '
     'sửa phiếu báo có”.\n'
     '– Kiểm tra phiếu vẫn ở trạng thái Đang tạo và do chính mình lập; không thỏa thì báo '
     '“Phiếu báo có đã duyệt hoặc không phải của bạn, không sửa được”.\n'
     'During:\n– Kiểm tra dữ liệu như màn Tạo mới.\n'
     'After:\n– Ghi lại thông tin chung, xóa và ghi lại toàn bộ dòng chi tiết, cập nhật hai ô '
     'tổng tiền.\n'
     '– Ghi lịch sử đúng những trường đã thay đổi, riêng bảng chi tiết ghi theo dòng được thêm, '
     'bị bỏ hoặc bị sửa.\n'
     '– Hiển thị “Cập nhật phiếu báo có thành công!” và quay về danh sách.'),
    ('Bấm Lưu và duyệt', 'Click',
     'After:\n– Lưu như trên rồi chuyển trạng thái sang Đã duyệt và ghi bút toán vào sổ cái.'),
])

# ------------------------------------------------- 2.8 Xem chi tiet
d.h3('2.8 Xem chi tiết phiếu báo có')

d.p('2.8.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung phần riêng của màn Phiếu báo có tại '
           'phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu báo có',
    mota='Xem toàn bộ thông tin của một phiếu ở chế độ chỉ đọc, kèm khối đánh dấu không báo '
         'tiền về, khối lịch sử thay đổi và các nút thao tác theo trạng thái và quyền.',
    tacnhan='Kế toán; Người dùng đã đăng nhập',
    dieukien='Phiếu nằm trong phạm vi dữ liệu người dùng được xem.',
    chinh='1. Người dùng bấm vào Mã phiếu ở danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu đó.\n'
          '3. Hệ thống hiển thị thông tin chung, bảng chi tiết ở chế độ chỉ đọc, khối đánh dấu '
          'không báo tiền về và khối lịch sử.\n'
          '4. Thanh nút phía dưới hiển thị các thao tác còn dùng được với phiếu.',
    phu='• Không có quyền xem phiếu → hệ thống báo “Bạn không có quyền xem phiếu báo có này”.\n'
        '• Phiếu đã bị xóa → báo “Không tìm thấy dữ liệu”.\n'
        '• Phiếu Đang tạo do người khác lập → không truy cập được.',
    dacbiet=None)

d.p('2.8.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('19-chi-tiet.png'),
         shot_caption='Màn Chi tiết phiếu báo có')

d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu báo có: <mã phiếu>', '–'),
    ('Khối Thông tin chung', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Bố cục giống màn Sửa nhưng mọi ô đều bị khóa.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Bộ cột theo loại thu của phiếu; không có cột xóa dòng.'),
    ('Khối Đánh dấu không báo tiền về', 'Table/Grid', 'Enable / Read-only', '–', 'Theo dữ liệu',
     'Gồm STT, Đối tượng, Hợp đồng, Số tiền (VND), Chưa điều chỉnh, Diễn giải và ô tích; '
     'ô tích bị khóa khi người dùng không có quyền Quản lý phiếu báo có.'),
    ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở, có nút Làm mới và Thu gọn.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu Đang tạo do chính người dùng lập và có quyền thao tác.'),
    ('Nút Duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu Đang tạo và người dùng có quyền thao tác.'),
    ('Nút Tạo phiếu yêu cầu điều chỉnh công nợ', 'Button', 'Enable / Ẩn', '–',
     'Ẩn khi không còn tiền chưa điều chỉnh',
     'Chỉ hiện khi phiếu còn ít nhất một dòng chưa điều chỉnh hết công nợ.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Cùng điều kiện với nút Sửa; nút màu đỏ.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
], required=False)

d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu: người lập luôn xem được; phiếu Đang tạo của người '
     'khác thì không ai xem được; còn lại xét theo quyền xem theo cấp.\n'
     'After:\n– Hiển thị dữ liệu phiếu kèm ba cờ cho biết phiếu còn sửa / xóa / duyệt được hay '
     'không để hiện đúng bộ nút.'),
    ('Bấm Tạo phiếu yêu cầu điều chỉnh công nợ', 'Click',
     'After:\n– Chuyển sang màn Tạo phiếu yêu cầu điều chỉnh công nợ, mang theo danh sách dòng '
     'chi tiết còn tiền chưa điều chỉnh; nút Quay lại của màn đó trả về đúng phiếu báo có này.'),
])

# ------------------------------------------------- 2.9 Duyet
d.h3('2.9 Duyệt phiếu báo có')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Duyệt phiếu báo có', 'action',
            [('include', 'Kiểm tra quyền và trạng thái phiếu'),
             ('include', 'Ghi bút toán vào sổ cái'),
             ('include', 'Gửi thông báo cho kế toán cùng công ty')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-09 Duyệt phiếu báo có')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX. Quy tắc ghi lịch sử áp dụng theo SRS Các quy tắc chung.',
           anchor='history')
d.intro_table(
    ten='Duyệt phiếu báo có',
    mota='Chuyển phiếu từ Đang tạo sang Đã duyệt và ghi bút toán tương ứng vào sổ cái kế toán.',
    tacnhan='Kế toán có quyền Quản lý phiếu báo có',
    dieukien='Phiếu ở trạng thái Đang tạo và người dùng có quyền Quản lý phiếu báo có.',
    chinh='1. Người dùng bấm Duyệt ở menu hành động của dòng danh sách hoặc ở màn chi tiết.\n'
          '2. Hệ thống hiển thị hộp xác nhận nêu rõ hậu quả: ghi bút toán vào sổ cái và phiếu '
          'không sửa/xóa được nữa.\n'
          '3. Người dùng xác nhận.\n'
          '4. Hệ thống khóa phiếu, kiểm tra lại trạng thái, đổi sang Đã duyệt, ghi người duyệt.\n'
          '5. Hệ thống sinh bút toán và ghi vào sổ cái, ghi lịch sử, gửi thông báo và nạp lại '
          'danh sách.',
    phu='• Phiếu vừa được người khác duyệt xong → thao tác thứ hai không ghi sổ lần nữa.\n'
        '• Phiếu không còn ở trạng thái Đang tạo hoặc thiếu quyền → hệ thống báo “Phiếu báo có '
        'không ở trạng thái Đang tạo hoặc bạn không có quyền duyệt” và nạp lại danh sách.\n'
        '• Bấm Hủy ở hộp xác nhận → không thay đổi gì.',
    dacbiet='Duyệt là thao tác không hoàn tác được vì bút toán đã ghi vào sổ kế toán dùng chung '
            'với cổng ERP.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Duyệt', shot=shot('21-xac-nhan-duyet.png'),
         shot_caption='Hộp xác nhận duyệt phiếu báo có')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận duyệt', '–'),
    ('Nội dung xác nhận', 'Label', 'Hiển thị',
     'Duyệt phiếu báo có ‘<mã phiếu>’? Hệ thống sẽ ghi bút toán vào sổ cái và phiếu không '
     'sửa/xóa được nữa.', '–'),
    ('Nút Duyệt', 'Button', 'Enable', 'Hiển thị', 'Thực hiện duyệt.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không thay đổi gì.'),
], required=False, scope=False)

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Duyệt', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý phiếu báo có và trạng thái phiếu là Đang tạo.\n'
     '– Không thỏa → báo “Phiếu báo có không ở trạng thái Đang tạo hoặc bạn không có quyền duyệt” '
     'và dừng xử lý.\n'
     'During:\n– Khóa bản ghi rồi kiểm tra lại trạng thái để hai người bấm cùng lúc không ghi sổ '
     'hai lần.\n'
     'After:\n– Đổi trạng thái sang Đã duyệt, ghi người duyệt.\n'
     '– Sinh và ghi bút toán vào sổ cái; các dòng chi tiết có số tiền bằng 0 không sinh bút toán.\n'
     '– Ghi một dòng lịch sử thay đổi trạng thái kèm ghi chú đã ghi bút toán.\n'
     '– Gửi thông báo cho những người có quyền Quản lý phiếu báo có trong cùng công ty.\n'
     '– Hiển thị “Duyệt phiếu báo có thành công.” và nạp lại danh sách.'),
])

# ------------------------------------------------- 2.10 Xoa
d.h3('2.10 Xóa phiếu báo có')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu báo có', 'action',
            [('include', 'Kiểm tra quyền và điều kiện xóa'),
             ('include', 'Xóa các dòng chi tiết của phiếu')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu báo có')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa và Thông báo.', anchor='delete')
d.intro_table(
    ten='Xóa phiếu báo có',
    mota='Xóa hẳn một phiếu đang ở trạng thái Đang tạo do chính người dùng lập, kèm toàn bộ '
         'dòng chi tiết của phiếu.',
    tacnhan='Kế toán có quyền Quản lý phiếu báo có và là người lập phiếu',
    dieukien='Phiếu ở trạng thái Đang tạo và do chính người dùng lập.',
    chinh='1. Người dùng bấm nút Xóa ở dòng danh sách hoặc ở màn chi tiết.\n'
          '2. Hệ thống hiển thị hộp xác nhận kèm mã phiếu.\n'
          '3. Người dùng xác nhận.\n'
          '4. Hệ thống ghi lịch sử xóa, xóa các dòng chi tiết rồi xóa phiếu và nạp lại danh sách.',
    phu='• Phiếu đã duyệt hoặc không phải của mình → nút Xóa không hiển thị; gọi thẳng chức năng '
        'thì báo “Phiếu báo có đã duyệt hoặc không phải của bạn, không xóa được”.\n'
        '• Phiếu vừa bị người khác xử lý → hệ thống báo lỗi tương ứng và nạp lại danh sách cho '
        'khớp thực tế.\n'
        '• Bấm Hủy → không thay đổi gì.',
    dacbiet=None)

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa', shot=shot('17-xac-nhan-xoa.png'),
         shot_caption='Hộp xác nhận xóa phiếu báo có')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', '–'),
    ('Nội dung xác nhận', 'Label', 'Hiển thị',
     'Bạn có chắc muốn xóa phiếu báo có ‘<mã phiếu>’?', '–'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Nút màu đỏ, thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xóa', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý phiếu báo có, trạng thái Đang tạo và người lập là chính '
     'người dùng.\n'
     '– Không thỏa → báo “Phiếu báo có đã duyệt hoặc không phải của bạn, không xóa được”.\n'
     'After:\n– Ghi một dòng lịch sử “Xóa”, xóa toàn bộ dòng chi tiết rồi xóa phiếu.\n'
     '– Hiển thị “Xóa thành công.” và nạp lại danh sách.'),
])

# ------------------------------------------------- 2.11 Khong bao tien ve
d.h3('2.11 Đánh dấu không báo tiền về')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Đánh dấu không báo tiền về', 'action',
            [('include', 'Kiểm tra quyền xem phiếu và quyền thao tác'),
             ('extend', 'Loại dòng khỏi màn Tổng hợp tiền về ngân hàng')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-11 Đánh dấu không báo tiền về')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX.', anchor='notice')
d.intro_table(
    ten='Đánh dấu dòng chi tiết là không báo tiền về',
    mota='Bật hoặc tắt cờ “Không báo tiền về” cho từng dòng chi tiết ngay tại màn chi tiết. '
         'Dòng đã đánh dấu sẽ không xuất hiện ở màn Tổng hợp tiền về ngân hàng.',
    tacnhan='Kế toán có quyền Quản lý phiếu báo có',
    dieukien='Người dùng xem được phiếu và có quyền Quản lý phiếu báo có.',
    chinh='1. Người dùng mở màn chi tiết phiếu.\n'
          '2. Người dùng tích hoặc bỏ tích ô ở cột “Không báo tiền về” của dòng cần đánh dấu.\n'
          '3. Hệ thống lưu ngay thay đổi của riêng dòng đó và ghi lịch sử.\n'
          '4. Hệ thống hiển thị thông báo “Cập nhật thành công.”',
    phu='• Không có quyền Quản lý phiếu báo có → ô tích bị khóa; gọi thẳng chức năng thì báo '
        '“Bạn không có quyền cập nhật phiếu báo có”.\n'
        '• Đang lưu một dòng thì các ô tích khác tạm khóa để tránh bấm chồng.\n'
        '• Lưu thất bại → hiển thị thông báo lỗi và giữ nguyên trạng thái cũ của ô tích.',
    dacbiet='Thay đổi có hiệu lực ngay, không cần bấm Lưu phiếu.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết', shot=shot('19-chi-tiet.png'),
         shot_caption='Khối Đánh dấu không báo tiền về ở màn chi tiết')

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Câu hướng dẫn', 'Label', 'Hiển thị', '–', 'Cố định',
     'Nêu rõ dòng được đánh dấu sẽ không xuất hiện ở màn Tổng hợp tiền về ngân hàng và thay đổi '
     'lưu ngay khi tích.'),
    ('Cột Đối tượng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Khách hàng hoặc nhà cung cấp của dòng.'),
    ('Cột Hợp đồng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Số tiền (VND)', 'Table/Grid', 'Read-only', 'Số ≥ 0', 'Theo dữ liệu', '–'),
    ('Cột Chưa điều chỉnh', 'Table/Grid', 'Read-only', 'Số ≥ 0', 'Theo dữ liệu',
     'Phần tiền chưa được xử lý bằng phiếu điều chỉnh công nợ.'),
    ('Ô tích Không báo tiền về', 'Checkbox', 'Enable / Disable', '–', 'Theo dữ liệu',
     'Bị khóa khi thiếu quyền hoặc khi dòng khác đang lưu.'),
], required=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Tích / bỏ tích ô Không báo tiền về', 'Change',
     'Before:\n– Kiểm tra quyền xem phiếu và quyền Quản lý phiếu báo có.\n'
     'After:\n– Lưu ngay giá trị mới cho riêng dòng đó, ghi một dòng lịch sử ghi rõ giá trị cũ '
     'và giá trị mới.\n'
     '– Hiển thị “Cập nhật thành công.”; nếu lỗi thì hiển thị thông báo lỗi và không đổi trạng '
     'thái ô tích.'),
])

# ------------------------------------------------- 2.12 Lich su
d.h3('2.12 Xem lịch sử thay đổi')

d.p('2.12.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu báo có',
    mota='Xem các mốc thao tác đã diễn ra trên phiếu: tạo mới, sửa, duyệt, đánh dấu không báo '
         'tiền về, import và xóa, kèm người thực hiện, thời điểm và giá trị cũ → giá trị mới.',
    tacnhan='Kế toán; Người dùng đã đăng nhập',
    dieukien='Người dùng xem được phiếu.',
    chinh='1. Người dùng bấm “Lịch sử” ở menu hành động của dòng danh sách, hoặc bấm '
          '“Xem lịch sử” ở màn chi tiết.\n'
          '2. Hệ thống hiển thị các mốc theo thứ tự mới nhất trước.\n'
          '3. Mỗi mốc nêu rõ loại thao tác, người thực hiện kèm phòng ban, thời điểm và những '
          'trường đã thay đổi.',
    phu='• Phiếu chưa có thao tác nào được ghi nhận → hiển thị “Chưa có lịch sử thao tác”.\n'
        '• Thay đổi ở bảng chi tiết được ghi theo dòng: dòng thêm mới, dòng bị bỏ, dòng bị sửa '
        'cột nào.',
    dacbiet=None)

d.p('2.12.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử', modal='Lịch sử thay đổi',
         shot=shot('23-popup-lich-su.png'),
         shot_caption='Cửa sổ Lịch sử thay đổi của một phiếu đã duyệt')
d.figure(shot('20-khoi-lich-su.png'), 'Khối Lịch sử ở màn chi tiết phiếu báo có', width_in=6.2)

d.p('2.12.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi — Phiếu: <mã phiếu>', '–'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị',
     'Lọc lịch sử theo nhóm thao tác và khoảng thời gian.'),
    ('Dòng thời gian', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi mốc gồm thời điểm, tên thao tác, người thực hiện kèm phòng ban và phần thay đổi.'),
    ('Khối thay đổi giá trị', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Hiển thị dạng “giá trị cũ → giá trị mới” bằng nhãn tiếng Việt, không hiển thị mã số.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Chưa có lịch sử thao tác” khi phiếu chưa có mốc nào.'),
], required=False)

d.p('2.12.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lịch sử ở danh sách', 'Click',
     'After:\n– Mở cửa sổ lịch sử của đúng phiếu đó, tải các mốc thao tác.'),
    ('Bấm Xem lịch sử ở màn chi tiết', 'Click',
     'After:\n– Mở khối lịch sử ngay trong trang; có nút Làm mới để tải lại và nút Thu gọn.'),
])

# ------------------------------------------------- 2.13 Import
d.h3('2.13 Import Excel sao kê')

d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'Import Excel sao kê', 'io',
            [('include', 'Kiểm tra quyền Quản lý phiếu báo có'),
             ('include', 'Kiểm tra dữ liệu từng dòng'),
             ('include', 'Tạo phiếu đã duyệt và ghi bút toán')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-13 Import Excel sao kê')

d.p('2.13.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Import Excel sao kê ngân hàng',
    mota='Nạp file sao kê ngân hàng để tạo hàng loạt phiếu báo có. Mỗi dòng trong file trở thành '
         'một phiếu báo có ở trạng thái Đã duyệt, gắn khách hàng KHÁCH KHÔNG RÕ và ghi bút toán '
         'vào sổ cái ngay.',
    tacnhan='Kế toán có quyền Quản lý phiếu báo có',
    dieukien='Người dùng có quyền Quản lý phiếu báo có và có file sao kê đúng mẫu.',
    chinh='1. Người dùng bấm nút Import Excel ở màn danh sách.\n'
          '2. Người dùng bấm “Tải file mẫu” để lấy file mẫu, điền dữ liệu.\n'
          '3. Người dùng bấm “Chọn file Excel” rồi “Load lên bảng” để xem trước dữ liệu.\n'
          '4. Người dùng bấm “Validate”; hệ thống kiểm tra từng dòng và báo số dòng hợp lệ, '
          'số dòng lỗi kèm lý do của từng dòng.\n'
          '5. Người dùng sửa các dòng lỗi ngay trên bảng rồi kiểm tra lại nếu cần.\n'
          '6. Người dùng bấm “Import”; hệ thống kiểm tra lại toàn bộ rồi tạo phiếu cho các dòng '
          'hợp lệ.\n'
          '7. Hệ thống báo số phiếu tạo thành công, số dòng lỗi và nạp lại danh sách.',
    phu='• File quá 500 dòng → hệ thống từ chối và yêu cầu tách file.\n'
        '• Không dòng nào hợp lệ → hệ thống báo và không cho bấm Import.\n'
        '• Một dòng lỗi khi ghi → chỉ dòng đó thất bại, các dòng còn lại vẫn được tạo.\n'
        '• Không có quyền Quản lý phiếu báo có → nút Import Excel không hiển thị; gọi thẳng chức '
        'năng thì báo “Bạn không có quyền import phiếu báo có”.',
    dacbiet='Mỗi dòng import tạo ra một phiếu ĐÃ DUYỆT và ghi bút toán vào sổ cái ngay, không '
            'hoàn tác được — phải kiểm tra kỹ file trước khi bấm Import.')

d.p('2.13.3 Layout màn hình')
d.layout(menu=MENU + ' => Import Excel', modal='Import phiếu báo có',
         shot=shot('16-import-buoc-1.png'),
         shot_caption='Cửa sổ Import phiếu báo có')

d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Chọn file Excel', 'Button', 'Enable', 'Tệp .xlsx', '–', 'Hiển thị',
     'Chọn file sao kê từ máy người dùng.'),
    ('Nút Tải file mẫu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Tải file mẫu gồm một dòng tiêu đề và một dòng ví dụ.'),
    ('Nút Load lên bảng', 'Button', 'Enable / Disable', '–', '–', 'Khóa khi chưa chọn file',
     'Đọc file và hiển thị dữ liệu lên bảng xem trước.'),
    ('Nút Validate', 'Button', 'Enable / Disable', '–', '–', 'Khóa khi chưa có dữ liệu',
     'Gửi toàn bộ dòng lên hệ thống kiểm tra.'),
    ('Nút Import', 'Button', 'Enable / Disable', '–', '–', 'Khóa khi chưa kiểm tra',
     'Tạo phiếu cho các dòng hợp lệ.'),
    ('Nút Chỉ dòng lỗi', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lọc bảng xem trước để chỉ hiện dòng lỗi.'),
    ('Cột Số tiền', 'Table/Grid', 'Enable', 'Số > 0', 'Có', 'Theo file',
     'Chấp nhận cả dấu chấm và dấu phẩy ngăn cách nghìn.'),
    ('Cột Diễn giải', 'Table/Grid', 'Enable', 'Chuỗi', 'Không', 'Theo file',
     'Dùng làm diễn giải của phiếu và của dòng chi tiết.'),
    ('Cột Ngày hạch toán', 'Table/Grid', 'Enable', 'dd/mm/yyyy hoặc yyyy-mm-dd', 'Có',
     'Theo file', 'Ngày không tồn tại như 31/02 bị coi là lỗi.'),
    ('Cột Mã ngân hàng', 'Table/Grid', 'Enable', 'Mã ngân hàng có trong danh mục', 'Có',
     'Theo file', 'Sai mã thì báo “Ngân hàng không tồn tại”.'),
    ('Cột Số tài khoản', 'Table/Grid', 'Enable', 'Số tài khoản của công ty', 'Có', 'Theo file',
     'Sai thì báo “Số tài khoản không tồn tại”.'),
    ('Cột Tên chi nhánh', 'Table/Grid', 'Enable', 'Tên chi nhánh có trong danh mục', 'Có',
     'Theo file', 'Sai thì báo “Tên chi nhánh không tồn tại”.'),
    ('Cột Loại tiền', 'Table/Grid', 'Enable', 'Mã loại tiền trong danh mục', 'Có', 'Theo file',
     'Sai thì báo “Loại tiền không tồn tại”.'),
    ('Cột Tỷ giá', 'Table/Grid', 'Enable', 'Số > 0', 'Không', 'Theo file',
     'Bỏ trống thì lấy tỷ giá của loại tiền.'),
    ('Ô thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện số dòng hợp lệ và số dòng lỗi sau khi kiểm tra.'),
])

d.p('2.13.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Validate', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý phiếu báo có; thiếu quyền thì báo “Bạn không có quyền '
     'import phiếu báo có”.\n'
     '– File rỗng → báo “Dữ liệu import rỗng”; quá 500 dòng → báo file quá lớn, yêu cầu tách file.\n'
     'During:\n– Kiểm tra từng dòng: số tiền lớn hơn 0, ngày hạch toán đúng định dạng và có thật, '
     'mã ngân hàng, số tài khoản, tên chi nhánh, loại tiền phải có trong danh mục, tỷ giá nếu có '
     'phải lớn hơn 0.\n'
     'After:\n– Hiển thị kết quả “Kiểm tra xong: X dòng hợp lệ, Y dòng lỗi” và đánh dấu lý do lỗi '
     'của từng dòng.'),
    ('Bấm Import', 'Click',
     'Before:\n– Kiểm tra quyền và giới hạn số dòng như trên.\n'
     'During:\n– Kiểm tra lại toàn bộ dòng ở máy chủ, bỏ qua các dòng lỗi.\n'
     'After:\n– Mỗi dòng hợp lệ tạo một phiếu báo có loại Thu bán hàng, tài khoản nợ 1121, một '
     'dòng chi tiết gắn khách hàng KHÁCH KHÔNG RÕ và tài khoản có 1311.\n'
     '– Chuyển phiếu sang trạng thái Đã duyệt và ghi bút toán vào sổ cái.\n'
     '– Ghi một dòng lịch sử “Import” cho từng phiếu.\n'
     '– Hiển thị “Import thành công X phiếu báo có!” hoặc nêu rõ số dòng lỗi, rồi nạp lại danh '
     'sách.'),
])

# ------------------------------------------------- 2.14 Tong hop tien
d.h3('2.14 Xem Tổng hợp tiền về ngân hàng')

d.p('2.14.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', anchor='list')
d.intro_table(
    ten='Xem danh sách Tổng hợp tiền về ngân hàng',
    mota='Liệt kê từng dòng chi tiết của các phiếu báo có đã duyệt để đối chiếu khoản tiền về '
         'với công nợ, kèm số tiền chưa điều chỉnh và trạng thái điều chỉnh.',
    tacnhan='Kế toán; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và xác định được công ty.',
    chinh='1. Người dùng vào menu Tài chính → Quản lý tiền → Thanh toán tiền mặt → '
          'Tổng hợp tiền về ngân hàng.\n'
          '2. Hệ thống lấy các dòng chi tiết thỏa đồng thời: phiếu cha đã duyệt, tài khoản có '
          'thuộc nhóm tài khoản công nợ, dòng chưa bị đánh dấu Không báo tiền về, và phiếu thuộc '
          'công ty của người đăng nhập.\n'
          '3. Hệ thống tính số tiền chưa điều chỉnh của từng dòng và gán trạng thái tương ứng.\n'
          '4. Bảng hiển thị dữ liệu kèm ô tích ở cột Điều chỉnh công nợ.',
    phu='• Không xác định được công ty của người đăng nhập → màn không hiển thị dòng nào.\n'
        '• Dòng đã điều chỉnh hết công nợ → ô tích thay bằng dấu gạch ngang, không chọn được.',
    dacbiet=None)

d.p('2.14.2 Layout màn hình')
d.layout(menu=MENU_SUM, shot=shot('24-tong-hop-tien.png'),
         shot_caption='Màn Tổng hợp tiền về ngân hàng')
d.figure(shot('25-tong-hop-cot-phai.png'),
         'Phần bên phải: Số tiền chưa điều chỉnh, Trạng thái và ô tích Điều chỉnh công nợ',
         width_in=6.2)
d.figure(shot('26-tong-hop-bo-loc.png'),
         'Bảng tìm kiếm nâng cao của màn Tổng hợp tiền về ngân hàng', width_in=6.2)

d.p('2.14.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh theo số báo có', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Trống',
     'Tìm tương đối theo mã phiếu báo có.'),
    ('Ô lọc Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng', 'Trống',
     'Gõ tối thiểu 2 ký tự để tìm.'),
    ('Ô lọc Ghi chú', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Trống',
     'Tìm theo diễn giải của dòng chi tiết.'),
    ('Ô lọc Ngân hàng', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Trống',
     'Tìm theo mã hoặc tên ngân hàng.'),
    ('Ô lọc STK ngân hàng', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Trống', '–'),
    ('Ô lọc Người lập', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', '–'),
    ('Ô lọc Lọc phiếu', 'Dropdown', 'Enable',
     'Đã điều chỉnh hết công nợ / Chưa điều chỉnh hết công nợ', 'Trống', '–'),
    ('Ô lọc Số tiền từ / đến', 'Number', 'Enable', 'Số ≥ 0', 'Trống',
     'Lọc theo số tiền quy đổi của dòng.'),
    ('Ô lọc Hạch toán từ / đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống',
     'Lọc theo ngày hạch toán của phiếu cha.'),
    ('Cột Số báo có', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là đường dẫn mở màn chi tiết phiếu báo có; cột cố định.'),
    ('Cột Ngày hạch toán', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '–'),
    ('Cột Người lập', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Dạng “Mã - Tên”.'),
    ('Cột Ghi chú', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Diễn giải của dòng chi tiết.'),
    ('Cột Ngân hàng / STK ngân hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Số tiền', 'Table/Grid', 'Read-only', 'Số ≥ 0', 'Theo dữ liệu',
     'Số tiền quy đổi của dòng; sắp xếp được.'),
    ('Cột Số tiền chưa điều chỉnh', 'Table/Grid', 'Read-only', 'Số ≥ 0', 'Theo dữ liệu',
     'Bằng Số tiền trừ đi phần đã điều chỉnh công nợ.'),
    ('Cột Trạng thái', 'Badge', 'Read-only',
     'Chưa điều chỉnh hết công nợ / Đã điều chỉnh hết công nợ', 'Theo dữ liệu',
     'Tính theo số tiền chưa điều chỉnh, không phải trạng thái lưu sẵn.'),
    ('Cột Điều chỉnh công nợ', 'Checkbox', 'Enable / Ẩn', '–', 'Không tích',
     'Chỉ dòng còn tiền chưa điều chỉnh mới có ô tích; dòng khác hiển thị dấu gạch ngang.'),
    ('Nút Tạo mới điều chỉnh công nợ', 'Button', 'Enable', '–', 'Hiển thị',
     'Chuyển các dòng đã tích sang màn tạo phiếu yêu cầu điều chỉnh công nợ.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Chọn trường xuất file.'),
], required=False)

d.p('2.14.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'During:\n– Lấy các dòng chi tiết của phiếu đã duyệt, tài khoản có thuộc nhóm công nợ, chưa '
     'bị đánh dấu Không báo tiền về và thuộc công ty của người đăng nhập.\n'
     'After:\n– Hiển thị dữ liệu kèm số tiền chưa điều chỉnh và trạng thái tương ứng.'),
    ('Tích chọn một dòng', 'Change',
     'During:\n– Nếu dòng thuộc phiếu báo có khác với dòng đang chọn → hiển thị “Không thể chọn '
     '2 phiếu báo có khác nhau! Vui lòng bỏ chọn dòng cũ trước.” và trả ô tích về trạng thái cũ.\n'
     'After:\n– Ghi nhận dòng được chọn.'),
])

# ------------------------------------------------- 2.15 Xuat Excel
d.h3('2.15 Xuất Excel màn Tổng hợp tiền về ngân hàng')

d.p('2.15.1 Biểu đồ Usecase')
d.uc_figure('FR-15', 'Xuất Excel màn tổng hợp', 'io',
            [('include', 'Chọn trường xuất file'),
             ('include', 'Áp dụng bộ lọc đang dùng')],
            actor=ACTOR_VIEW,
            caption='Biểu đồ Use Case — FR-15 Xuất Excel màn tổng hợp')

d.p('2.15.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách tổng hợp tiền về ngân hàng',
    mota='Xuất toàn bộ dòng khớp bộ lọc đang áp dụng ra file Excel, với các cột do người dùng '
         'chọn và theo đúng thứ tự chọn.',
    tacnhan='Kế toán; Người dùng đã đăng nhập',
    dieukien='Đang ở màn Tổng hợp tiền về ngân hàng.',
    chinh='1. Người dùng bấm nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ Chọn trường xuất file với 10 trường, mặc định chọn hết.\n'
          '3. Người dùng bỏ chọn hoặc chọn lại các trường theo thứ tự mong muốn.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống dựng file theo bộ lọc đang áp dụng, kèm logo và tiêu đề công ty, rồi tải '
          'về máy người dùng.',
    phu='• Bấm “Chọn tất cả” / “Bỏ chọn hết” để thao tác nhanh.\n'
        '• Có lọc theo khoảng ngày hạch toán → file có thêm dòng “Từ ngày … đến ngày …”.\n'
        '• Lỗi khi xuất → hiển thị “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”',
    dacbiet='File xuất lấy TOÀN BỘ dòng khớp bộ lọc, không giới hạn theo trang đang xem.')

d.p('2.15.3 Layout màn hình')
d.layout(menu=MENU_SUM + ' => Xuất Excel', modal='Chọn trường xuất file',
         shot=shot('27-chon-truong-xuat.png'),
         shot_caption='Cửa sổ Chọn trường xuất file')

d.p('2.15.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách Trường xuất', 'Dropdown', 'Enable', '10 trường', 'Có', 'Chọn hết 10/10',
     'Gồm Số báo có, Ngày hạch toán, Người lập, Khách hàng, Diễn giải, Ngân hàng, STK ngân hàng, '
     'Số tiền, Số tiền chưa điều chỉnh, Trạng thái.'),
    ('Dòng thứ tự cột', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn',
     'Cho biết thứ tự cột trong file đúng bằng thứ tự người dùng chọn.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Xuất file', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Tải file “Tong-hop-tien-ve-ngan-hang.xlsx”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
])

d.p('2.15.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất file', 'Click',
     'During:\n– Lấy toàn bộ dòng khớp bộ lọc đang áp dụng, không phân trang.\n'
     'After:\n– Dựng file Excel với các cột đã chọn theo đúng thứ tự chọn, ô tiền là ô số có dấu '
     'ngăn cách nghìn, phần đầu file có logo và tiêu đề của công ty ghi trên chứng từ.\n'
     '– Tải file về máy và hiển thị “Xuất Excel thành công.”'),
])

# ------------------------------------------------- 2.16 Sang dieu chinh cong no
d.h3('2.16 Tạo phiếu yêu cầu điều chỉnh công nợ từ phiếu báo có')

d.p('2.16.1 Biểu đồ Usecase')
d.uc_figure('FR-16', 'Tạo phiếu yêu cầu điều chỉnh công nợ', 'action',
            [('include', 'Chọn dòng chi tiết còn tiền chưa điều chỉnh'),
             ('extend', 'Quay lại đúng phiếu báo có ban đầu')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-16 Tạo phiếu yêu cầu điều chỉnh công nợ')

d.p('2.16.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX.', anchor='notice')
d.intro_table(
    ten='Chuyển sang màn Tạo phiếu yêu cầu điều chỉnh công nợ',
    mota='Đưa các dòng tiền về chưa gán đúng đối tượng sang màn Phiếu yêu cầu điều chỉnh công nợ '
         'để kế toán gán lại khách hàng và hợp đồng.',
    tacnhan='Kế toán; Người dùng đã đăng nhập',
    dieukien='Có ít nhất một dòng chi tiết còn tiền chưa điều chỉnh.',
    chinh='1. Từ màn Tổng hợp tiền về ngân hàng, người dùng tích chọn các dòng cần điều chỉnh '
          'rồi bấm “Tạo mới điều chỉnh công nợ”; hoặc từ màn chi tiết phiếu báo có, bấm '
          '“Tạo phiếu yêu cầu điều chỉnh công nợ”.\n'
          '2. Hệ thống chuyển sang màn tạo phiếu yêu cầu điều chỉnh công nợ, mang theo danh sách '
          'dòng chi tiết đã chọn.\n'
          '3. Người dùng tiếp tục nhập theo quy trình của màn đó.',
    phu='• Chưa tích dòng nào mà bấm nút → báo “Vui lòng chọn ít nhất một chi tiết báo có.”\n'
        '• Tích dòng của hai phiếu báo có khác nhau → hệ thống chặn và yêu cầu bỏ chọn dòng cũ.\n'
        '• Đi từ màn chi tiết phiếu báo có → nút Quay lại của màn điều chỉnh công nợ trả về đúng '
        'phiếu báo có ban đầu.',
    dacbiet='Một phiếu yêu cầu điều chỉnh công nợ chỉ gắn được với duy nhất một phiếu báo có.')

d.p('2.16.3 Layout màn hình')
d.layout(menu=MENU_SUM + ' => Tạo mới điều chỉnh công nợ',
         shot=shot('25-tong-hop-cot-phai.png'),
         shot_caption='Ô tích Điều chỉnh công nợ trên từng dòng của màn tổng hợp')

d.p('2.16.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tích trên dòng', 'Checkbox', 'Enable / Ẩn', '–', 'Không tích',
     'Chỉ dòng còn tiền chưa điều chỉnh mới có ô tích.'),
    ('Nút Tạo mới điều chỉnh công nợ', 'Button', 'Enable', '–', 'Hiển thị',
     'Ở màn Tổng hợp tiền về ngân hàng.'),
    ('Nút Tạo phiếu yêu cầu điều chỉnh công nợ', 'Button', 'Enable / Ẩn', '–',
     'Ẩn khi phiếu đã điều chỉnh hết', 'Ở màn chi tiết phiếu báo có.'),
], required=False)

d.p('2.16.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tạo mới điều chỉnh công nợ', 'Click',
     'Before:\n– Kiểm tra đã tích ít nhất một dòng; chưa tích thì báo “Vui lòng chọn ít nhất một '
     'chi tiết báo có.” và dừng.\n'
     'After:\n– Chuyển sang màn tạo phiếu yêu cầu điều chỉnh công nợ kèm danh sách dòng đã chọn.'),
    ('Bấm Tạo phiếu yêu cầu điều chỉnh công nợ ở màn chi tiết', 'Click',
     'After:\n– Chuyển sang màn tạo phiếu yêu cầu điều chỉnh công nợ với toàn bộ dòng còn tiền '
     'chưa điều chỉnh của phiếu, kèm đường dẫn quay lại đúng phiếu báo có này.'),
])

# ==================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu báo có; không lặp lại các quy '
           'tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Phạm vi dữ liệu theo quyền xem', [
        '– Có quyền Xem tất cả phiếu báo có của tổng công ty: thấy toàn bộ phiếu của hệ thống.',
        '– Chỉ có quyền Xem tất cả phiếu báo có của công ty: chỉ thấy phiếu có công ty trùng với '
        'công ty của người đăng nhập.',
        '– Không có quyền xem theo cấp nào: chỉ thấy phiếu do chính mình lập.',
        '– Trong mọi trường hợp, phiếu Đang tạo của người khác luôn bị ẩn.',
    ], ['Danh sách', 'Xem chi tiết']),
    ('BR-02', 'Vòng đời phiếu và thời điểm ghi sổ cái', [
        '– Phiếu chỉ có hai trạng thái: Đang tạo và Đã duyệt; không có bước gửi duyệt, từ chối '
        'hay hủy.',
        '– Bút toán chỉ được ghi vào sổ cái tại thời điểm duyệt (bấm Duyệt, bấm Lưu và duyệt, '
        'hoặc import).',
        '– Phiếu đã duyệt không sửa, không xóa được.',
    ], ['Toàn màn hình']),
    ('BR-03', 'Điều kiện được sửa, xóa, duyệt', [
        '– Sửa và Xóa: phiếu ở trạng thái Đang tạo, do chính người dùng lập, và người dùng có '
        'quyền Quản lý phiếu báo có.',
        '– Duyệt: phiếu ở trạng thái Đang tạo và người dùng có quyền Quản lý phiếu báo có; không '
        'bắt buộc phải là người lập phiếu.',
        '– Hai người cùng duyệt một phiếu thì chỉ lần đầu ghi sổ, lần sau bị từ chối.',
    ], ['Danh sách', 'Xem chi tiết', 'Chỉnh sửa']),
    ('BR-04', 'Sinh mã phiếu tự động', [
        '– Mã có dạng: mã công ty + “.PBC” + tháng năm (bốn chữ số) + “.” + số thứ tự năm chữ số.',
        '– Mã sinh tại thời điểm lưu lần đầu, không sửa được, không trùng nhau kể cả khi hai người '
        'lập phiếu cùng lúc.',
    ], ['Tạo mới', 'Import Excel']),
    ('BR-05', 'Bộ cột bảng chi tiết theo Loại thu', [
        '– Thu bán hàng: có cột Khách hàng (bắt buộc), Số đơn hàng/Hợp đồng, Phiếu YC xuất hàng, '
        'NVKD; tài khoản có mặc định 1311.',
        '– Thu nhà cung cấp: có cột Nhà cung cấp (bắt buộc), Phiếu xuất hàng, Hợp đồng mua, NVKD; '
        'tài khoản có mặc định 3311.',
        '– Thu khác: chỉ có cột Khách hàng (không bắt buộc); không có tài khoản có mặc định.',
        '– Đổi Loại thu sẽ xóa toàn bộ dòng chi tiết đang nhập, có hỏi xác nhận trước.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-06', 'Ràng buộc chọn hợp đồng và phiếu yêu cầu xuất hàng', [
        '– Dòng loại Thu bán hàng có tài khoản có thuộc nhóm tài khoản công nợ và khách hàng khác '
        'KHÁCH KHÔNG RÕ thì bắt buộc chọn đơn hàng/hợp đồng.',
        '– Dòng gắn hợp đồng nguyên tắc thì bắt buộc chọn phiếu yêu cầu xuất hàng, trừ khi đã tích '
        '“Số dư nợ đầu kì”.',
        '– Đổi khách hàng hoặc nhà cung cấp thì hợp đồng, phiếu xuất và phiếu yêu cầu xuất hàng '
        'đã chọn của dòng bị xóa.',
        '– Một hợp đồng chỉ được chọn ở một dòng trong cùng một phiếu.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-07', 'Quy đổi ngoại tệ', [
        '– Loại tiền là VNĐ: tỷ giá bị khóa và luôn bằng 1, bảng chi tiết không có cột số tiền '
        'quy đổi.',
        '– Loại tiền là ngoại tệ: tỷ giá lấy theo danh mục loại tiền và sửa được; số tiền quy đổi '
        'của dòng bằng số tiền nhân tỷ giá.',
        '– Hai ô tổng tiền của phiếu bằng tổng số tiền và tổng số tiền quy đổi của các dòng.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-08', 'Liên động Ngân hàng – Tài khoản – Chi nhánh', [
        '– Chỉ chọn được Tài khoản sau khi đã chọn Ngân hàng; danh sách tài khoản lọc theo ngân '
        'hàng đó.',
        '– Chọn Tài khoản thì Chi nhánh tự điền và không sửa tay được.',
        '– Đổi Ngân hàng thì Tài khoản và Chi nhánh bị xóa.',
        '– Màn Sửa vẫn giữ đúng tài khoản đang gắn với phiếu kể cả khi tài khoản đó đã bị khóa.',
    ], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-09', 'Cờ Không báo tiền về', [
        '– Dòng chi tiết được đánh dấu sẽ không xuất hiện ở màn Tổng hợp tiền về ngân hàng.',
        '– Cờ này đặt được cả lúc nhập phiếu lẫn ở màn chi tiết sau khi phiếu đã duyệt.',
        '– Mỗi lần bật/tắt đều ghi một dòng lịch sử.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Xem chi tiết']),
    ('BR-10', 'Điều kiện hiển thị của màn Tổng hợp tiền về ngân hàng', [
        '– Chỉ lấy dòng chi tiết của phiếu đã duyệt.',
        '– Tài khoản có của dòng phải thuộc nhóm tài khoản công nợ (1311, 1312, 3311).',
        '– Dòng chưa bị đánh dấu Không báo tiền về.',
        '– Phiếu thuộc công ty của người đăng nhập; không xác định được công ty thì không hiển thị '
        'dòng nào.',
        '– Trạng thái của dòng được tính tại thời điểm xem: còn tiền chưa điều chỉnh là '
        '“Chưa điều chỉnh hết công nợ”, ngược lại là “Đã điều chỉnh hết công nợ”.',
    ], ['Tổng hợp tiền về ngân hàng']),
    ('BR-11', 'Chọn dòng để điều chỉnh công nợ', [
        '– Chỉ dòng còn tiền chưa điều chỉnh mới chọn được.',
        '– Không chọn được đồng thời các dòng thuộc hai phiếu báo có khác nhau.',
    ], ['Tổng hợp tiền về ngân hàng', 'Xem chi tiết']),
    ('BR-12', 'Quy tắc import sao kê', [
        '– Mỗi dòng trong file tạo một phiếu báo có loại Thu bán hàng, tài khoản nợ 1121, một '
        'dòng chi tiết gắn khách hàng KHÁCH KHÔNG RÕ và tài khoản có 1311.',
        '– Phiếu tạo bằng import được duyệt và ghi bút toán ngay.',
        '– Toàn bộ dòng được kiểm tra trước khi ghi; dòng lỗi bị bỏ qua, dòng hợp lệ vẫn được tạo.',
        '– Một lần import tối đa 500 dòng.',
    ], ['Import Excel']),
    ('BR-13', 'Giới hạn nhập liệu', [
        '– Số tiền của dòng chi tiết phải lớn hơn 0.',
        '– Diễn giải chung của phiếu và diễn giải của từng dòng tối đa 500 ký tự; diễn giải của '
        'dòng là bắt buộc.',
        '– Ngày hạch toán bắt buộc và phải là ngày có thật.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Import Excel']),
    ('BR-14', 'Thông báo khi duyệt', [
        '– Khi một phiếu được duyệt, hệ thống gửi thông báo cho những người có quyền Quản lý '
        'phiếu báo có trong cùng công ty với phiếu.',
        '– Nội dung thông báo gồm mã phiếu và tên người lập, bấm vào mở đúng phiếu đó.',
    ], ['Duyệt', 'Tạo mới', 'Chỉnh sửa']),
])

d.save()
