# -*- coding: utf-8 -*-
"""Sinh SRS man "Danh sach hang giu" theo FORM CHUAN 2026-08-28.

Man BAO CAO CHI DOC (khong them / sua / xoa) — tra cuu ton hang giu theo cay 3 tang
Hang hoa -> Nhan vien -> Lo giu theo khach hang. Dung chung service voi man
"Hang sap het han giu" (man kia bat co bo vao cua so ngay canh bao).

Nguon: code HRM nhanh `gop_db` (doc ngay 05/10/2026)
  BE  Modules/Finance/{Services/PrepickStockReportService.php,
      Http/Controllers/V1/PrepickStockController.php, Routes/api.php,
      Resources/views/prints/prepick-stock-list.blade.php}
  FE  pages/finance/prepick-stocks/{index.vue, components/export-excel.js},
      components/finance/prepick/PrepickStockLogModal.vue
Anh chup that: ./prepick_stock_shots (dev, tai khoan DNS Admin, 05/10/2026).
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

SHOTS = os.path.join(BASE, 'prepick_stock_shots')
OUT = os.path.join(BASE, 'SRS - Danh sach hang giu.docx')

ACTOR = 'Người quản lý giữ hàng'


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Giữ hàng => Danh sách hàng giữ'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/prepick-stocks',
           full_url='https://<host-hrm>/finance/prepick-stocks',
           img_prefix='dshg_')

# ============================================================== TRANG DAU
d.title_block('Danh sách hàng giữ')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh sách hàng giữ (phân hệ Tài chính, '
    'nhóm Giữ hàng), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng tra cứu tồn hàng giữ và phân quyền của màn hình.',
    'Làm rõ bản chất của màn hình: đây là màn BÁO CÁO CHỈ ĐỌC — không thêm, không sửa, không xóa, '
    'không làm thay đổi số hàng giữ của bất kỳ ai.',
    'Làm rõ cấu trúc cây ba tầng Hàng hóa → Nhân viên giữ → Lô giữ theo khách hàng, và ý nghĩa '
    'số lượng ở từng tầng.',
    'Làm rõ cách tính Trạng thái hạn giữ (Trong hạn / Đến hạn / Hết hạn) và cột Tổng SL trong kho.',
    'Làm rõ phạm vi dữ liệu mà mỗi cấp quyền xem được, áp thống nhất cho bảng, Xuất Excel và In.',
    'Ghi nhận các điểm khác có chủ đích so với màn gốc trên hệ thống cũ (ERP).',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên kinh '
                 'doanh đứng tên giữ, có hạn giữ. Đây là số tồn riêng, tách khỏi tồn kho thông '
                 'thường.'),
    ('Lô hàng giữ', 'Một bản ghi hàng giữ xác định bởi hàng hóa × nhân viên giữ × khách hàng × '
                    'công ty × hạn giữ. Một hàng hóa có thể có nhiều lô.'),
    ('Phiếu xuất giữ', 'Chứng từ sinh ra lô hàng giữ. Các phiếu gia hạn, hủy, điều chuyển hàng giữ '
                       'và phiếu xuất bán làm lô biến động. Màn này chỉ ĐỌC kết quả của chúng.'),
    ('Hạn giữ', 'Ngày cuối cùng hàng còn được giữ cho khách.'),
    ('Trạng thái hạn giữ', 'Tính tại thời điểm xem, so hạn giữ với ngày hôm nay: Trong hạn (hạn '
                           'giữ sau hôm nay), Đến hạn (đúng hôm nay), Hết hạn (trước hôm nay). '
                           'Không lưu cố định.'),
    ('SL giữ', 'Số lượng đang giữ. Tầng hàng hóa = tổng mọi lô khớp bộ lọc; tầng nhân viên = tổng '
               'các lô của nhân viên đó; tầng lô = số của riêng lô đó.'),
    ('Tổng SL trong kho', 'Tổng tồn kho kế toán của hàng hóa ở các kho kế toán trong phạm vi '
                          'công ty người dùng được xem.'),
    ('Đơn vị cơ bản', 'Đơn vị tính gốc của hàng hóa. Hàng giữ luôn lưu theo đơn vị này; ô Đơn vị '
                      'trên màn chỉ đổi cách hiển thị.'),
    ('Sổ biến động (Lịch sử giữ hàng)', 'Danh sách các lần số hàng giữ tăng / giảm kèm chứng từ '
                                        'gây ra, sắp từ cũ đến mới.'),
], widths=[1.6, 4.9])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')
d.p('Màn hình chỉ đọc nên chỉ có MỘT quyền thao tác là quyền vào màn. Phạm vi dữ liệu do ba '
    'quyền xem theo cấp dùng chung với nhóm nghiệp vụ Giữ hàng quyết định. Tài khoản Quản trị hệ '
    'thống (Super admin) được coi như có Q1 và V1.')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý giữ hàng',
     'Được vào màn và dùng mọi chức năng: xem, lọc, mở cây chi tiết, xem lịch sử giữ hàng, '
     'Xuất Excel, In. Thiếu quyền này thì mọi yêu cầu lấy dữ liệu đều bị từ chối với thông báo '
     '“Bạn không có quyền xem danh sách hàng giữ” và bảng rỗng.'),
], widths=[0.8, 1.9, 3.8])

d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét theo thứ tự, lấy cấp cao nhất người dùng có):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu hàng giữ theo tổng công ty',
     'Xem hàng giữ của mọi công ty. Ô lọc Công ty chỉ hiện với cấp này.'),
    ('V2', 'Xem phiếu hàng giữ theo công ty',
     'Xem các lô hàng giữ thuộc công ty của mình.'),
    ('V3', 'Xem phiếu hàng giữ theo phòng ban',
     'Xem các lô do nhân viên thuộc các phòng ban mình quản lý (kể cả phòng của chính mình) '
     'đứng tên giữ, cộng lô của chính mình.'),
    ('–', 'Không có V1/V2/V3', 'Chỉ xem các lô do chính mình đứng tên giữ.'),
], widths=[0.8, 1.9, 3.8])

d.p('Ba quy tắc chung:')
d.bullets([
    'V1/V2/V3 KHÔNG thay được Q1: người chỉ có quyền xem theo cấp mà không có Quản lý giữ hàng '
    'thì không vào được màn.',
    'Phạm vi áp thống nhất cho bảng ba tầng, các danh sách chọn của bộ lọc, Xuất Excel và bản In — '
    'bốn nơi luôn ra cùng một tập dữ liệu.',
    'Cột Tổng SL trong kho của người không có V1 chỉ cộng tồn ở kho kế toán thuộc công ty mình.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1/V2/V3 không kèm Q1', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách hàng giữ', '✅', '❌', '❌'),
    ('FR-02 Tìm kiếm và lọc hàng giữ', '✅', '❌', '❌'),
    ('FR-03 Cài đặt bộ lọc', '✅', '❌', '❌'),
    ('FR-04 Tuỳ chỉnh cột hiển thị', '✅', '❌', '❌'),
    ('FR-05 Xem chi tiết giữ hàng theo nhân viên và khách hàng', '✅', '❌', '❌'),
    ('FR-06 Đổi đơn vị hiển thị số lượng', '✅', '❌', '❌'),
    ('FR-07 Xem lịch sử giữ hàng của lô', '✅', '❌', '❌'),
    ('FR-08 Xuất danh sách hàng giữ ra Excel', '✅', '❌', '❌'),
    ('FR-09 In danh sách hàng giữ', '✅', '❌', '❌'),
], widths=[2.9, 0.5, 1.4, 1.2])
d.p('Ghi chú: với người có Q1, dữ liệu thấy được ở mọi chức năng giới hạn theo V1/V2/V3 như bảng '
    'trên.')

# ================================================ PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR, [0, 1])],
    [('FR-01', 'Xem danh sách hàng giữ', 'view'),
     ('FR-05', 'Xem chi tiết giữ hàng theo nhân viên và khách hàng', 'view')],
    [('FR-02', 'Tìm kiếm và lọc hàng giữ', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tuỳ chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-06', 'Đổi đơn vị hiển thị số lượng', 'view', 'extend', [0], None),
     ('FR-08', 'Xuất danh sách hàng giữ ra Excel', 'io', 'extend', [0], None),
     ('FR-09', 'In danh sách hàng giữ', 'io', 'extend', [0], None),
     ('FR-07', 'Xem lịch sử giữ hàng của lô', 'view', 'extend', [1], None)],
    'Sơ đồ Use Case tổng quan màn Danh sách hàng giữ')

d.h2('2 Đặc tả chi tiết từng chức năng')

TACNHAN = ACTOR + '; Người dùng đã đăng nhập'

# ------------------------------------------------------------ 2.1
d.h3('2.1 Xem danh sách hàng giữ')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Danh sách hàng giữ tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách hàng hóa đang bị giữ',
    mota='Hiển thị tầng 1 của cây: mỗi dòng là MỘT HÀNG HÓA đang có hàng giữ (số lượng lớn hơn '
         '0) trong phạm vi dữ liệu của người đăng nhập, kèm tổng SL giữ và tổng SL trong kho. Bảng '
         'phân trang theo hàng hóa.',
    tacnhan=TACNHAN,
    dieukien='Người dùng đã đăng nhập và có quyền Quản lý giữ hàng (hoặc là Super admin).',
    chinh='1. Người dùng vào menu Tài chính → Giữ hàng → Danh sách hàng giữ.\n'
          '2. Hệ thống kiểm tra quyền Quản lý giữ hàng.\n'
          '3. Hệ thống xác định phạm vi dữ liệu theo V1 → V2 → V3 → chỉ lô của mình.\n'
          '4. Hệ thống gom các lô còn hàng theo hàng hóa, cộng SL giữ, ghép Tổng SL trong kho.\n'
          '5. Bảng hiển thị trang 1 (10 hàng hóa), sắp theo Tên hàng hóa A → Z; ô “Hiển thị a–b / '
          'N” cho biết tổng số hàng hóa.',
    phu='• Thiếu quyền Quản lý giữ hàng → hiện thông báo “Bạn không có quyền xem danh sách hàng '
        'giữ”, bảng rỗng.\n'
        '• Không có hàng hóa nào trong phạm vi → bảng hiện dòng “Không có dữ liệu phù hợp bộ '
        'lọc.”.\n'
        '• Bộ lọc của lần vào trước (trong vòng 10 phút) còn hiệu lực thì được khôi phục.\n'
        '• Màn được mở kèm mã hàng hóa trên đường dẫn (từ màn khác chuyển sang) → chỉ hiện đúng '
        'hàng hóa đó, đè lên bộ lọc đã lưu.\n'
        '• Lỗi khi tải → hiện thông báo “Lỗi khi tải dữ liệu”.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Màn Danh sách hàng giữ lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Danh sách hàng giữ',
     'Tiêu đề cố định phía trên bảng. Màn không có nút Thêm mới, Import, Sửa, Xóa.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ xem trước bản in theo bộ lọc đang áp (FR-09).'),
    ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
     'Mở cửa sổ chọn trường xuất (FR-08); bị khóa trong lúc đang xuất.'),
    ('Nút Tuỳ chỉnh cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Biểu tượng cột, mở cửa sổ Tuỳ chỉnh cột (FR-04).'),
    ('Cột STT', 'Icon Button', 'Enable', '–', 'Nút “>”',
     'Ở tầng hàng hóa là nút tròn “>” mở / thu cây chi tiết (FR-05), KHÔNG in số thứ tự. Đang '
     'tải thì hiện biểu tượng quay. Cột cố định, không tắt được.'),
    ('Cột Mã hàng hóa / Nhân viên / Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tầng 1 hiện mã hàng hóa (chữ thường, không phải liên kết). Cột cố định, sắp xếp được.'),
    ('Cột Tên hàng hóa / Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tầng 1 hiện tên hàng hóa, tự xuống dòng. Sắp xếp được.'),
    ('Cột Đơn vị', 'Dropdown', 'Enable / Read-only', 'Danh sách đơn vị của hàng hóa',
     'Đơn vị cơ bản',
     'Hàng hóa có từ 2 đơn vị trở lên thì là ô chọn (FR-06); chỉ 1 đơn vị thì hiện chữ.'),
    ('Cột Model', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Chỉ có ở tầng 1.'),
    ('Cột Thương hiệu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Chỉ có ở tầng 1.'),
    ('Cột Tổng SL trong kho', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Tổng tồn kho kế toán của hàng hóa; để trống nếu hàng hóa chưa có tồn kho kế toán. Sắp xếp '
     'được.'),
    ('Cột SL giữ', 'Table/Grid', 'Read-only', '> 0', 'Theo dữ liệu',
     'Tổng SL giữ của mọi lô khớp bộ lọc. Sắp xếp được.'),
    ('Cột Hạn giữ / Trạng thái / Hành động', 'Table/Grid', 'Read-only', '–', 'Trống ở tầng 1',
     'Chỉ có dữ liệu ở tầng lô (FR-05). Cột Hành động cố định cuối bảng.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số HÀNG HÓA khớp bộ lọc, không phải số lô.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5 / 10 / 20 / 50 / 100', '10',
     'Đổi thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1', 'Nút đầu, lùi, số trang, tiến, cuối.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện dòng “Không có dữ liệu phù hợp bộ lọc.” khi không có hàng hóa nào khớp.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Hiển thị',
     'Hiện khi vào màn và trong lúc nạp lại dữ liệu.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng (hoặc Super admin).\n'
     '– Không có quyền → hiển thị “Bạn không có quyền xem danh sách hàng giữ” và dừng xử lý.\n'
     'During:\n– Khôi phục bộ lọc đã lưu (còn hiệu lực 10 phút); mã hàng hóa trên đường dẫn đè '
     'lên bộ lọc đã lưu.\n'
     '– Áp phạm vi dữ liệu V1 → V2 → V3 → chỉ lô của mình.\n'
     '– Chỉ lấy lô có số lượng lớn hơn 0; gom theo hàng hóa, cộng SL giữ.\n'
     'After:\n– Trả về trang 1, tổng số hàng hóa; nạp song song danh sách chọn cho bộ lọc và cấu '
     'hình cột của người dùng.'),
    ('Bấm tiêu đề cột có biểu tượng sắp xếp', 'Click',
     'During:\n– Chỉ bốn cột Mã hàng hóa / Nhân viên / Khách hàng, Tên hàng hóa / Phòng ban, '
     'Tổng SL trong kho, SL giữ sắp xếp được.\n'
     '– Bấm lần đầu sắp tăng dần, bấm lại đổi tăng ↔ giảm; muốn bỏ sắp xếp thì bấm Làm mới (về '
     'mặc định Tên hàng hóa A → Z).\n'
     '– Sắp xếp áp cho tầng hàng hóa; tầng nhân viên và tầng lô giữ thứ tự riêng.\n'
     'After:\n– Nạp lại từ trang 1, giữ nguyên bộ lọc, thu gọn mọi cây đang mở.'),
    ('Bấm số trang / tiến lùi / đổi số dòng mỗi trang', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\n'
     'After:\n– Nạp lại trang mới; mọi cây chi tiết đang mở bị thu gọn.'),
])

# ------------------------------------------------------------ 2.2
d.h3('2.2 Tìm kiếm và lọc hàng giữ')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các tiêu chí lọc riêng của '
           'màn Danh sách hàng giữ tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách hàng giữ',
    mota='Thu hẹp danh sách theo ô tìm nhanh khách hàng và chín tiêu chí lọc nâng cao. Một bộ '
         'điều kiện duy nhất áp cho cả ba tầng của cây, Xuất Excel và In.',
    tacnhan=TACNHAN,
    dieukien='Đang ở màn Danh sách hàng giữ.',
    chinh='1. Người dùng gõ tên, số điện thoại hoặc mã khách hàng vào ô tìm nhanh, hoặc bấm '
          '“Tìm kiếm nâng cao” để mở khu vực lọc.\n'
          '2. Người dùng nhập / chọn các tiêu chí cần lọc.\n'
          '3. Người dùng bấm Tìm kiếm (bắt buộc với ô tìm nhanh).\n'
          '4. Hệ thống nạp lại danh sách từ trang 1, trong phạm vi quyền.',
    phu='• Đổi giá trị một ô lọc nâng cao → hệ thống tự nạp lại, không cần bấm Tìm kiếm.\n'
        '• Bấm Làm mới → xóa toàn bộ điều kiện lọc và thứ tự sắp xếp rồi nạp lại.\n'
        '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khu vực lọc, điều kiện đang chọn vẫn giữ.\n'
        '• Không có hàng hóa nào khớp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU, shot=shot('02-bo-loc-nang-cao.png'),
         shot_caption='Khu vực Tìm kiếm nâng cao đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Placeholder “Nhập tên, số điện thoại hoặc mã KH để tìm kiếm”. Tìm gần đúng theo tên, mã '
     'hoặc số điện thoại KHÁCH HÀNG của lô. Chỉ áp dụng khi bấm Tìm kiếm.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng toàn bộ điều kiện.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Xóa hết điều kiện lọc, bỏ sắp xếp và tự nạp lại danh sách.'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–',
     'Tìm kiếm nâng cao', 'Mở / thu khu vực lọc nâng cao.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở FR-03.'),
    ('Ô lọc Mã hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm gần đúng theo mã hàng hóa.'),
    ('Ô lọc Tên hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm gần đúng theo tên hàng hóa.'),
    ('Ô lọc Lọc theo kho', 'Dropdown', 'Enable', 'Danh sách kho kế toán', 'Không', 'Trống',
     'Liệt kê kho kế toán (dạng “Mã - Tên”) của công ty người dùng; người có V1 thấy kho mọi '
     'công ty. Gồm cả kho đang Chờ xóa / ngừng dùng. Chọn kho → chỉ giữ hàng hóa có tồn kho kế '
     'toán ghi nhận ở kho đó.'),
    ('Ô lọc Thương hiệu', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Chỉ liệt kê thương hiệu của hàng hóa đang có hàng giữ trong phạm vi.'),
    ('Ô lọc Model', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Chỉ liệt kê model của hàng hóa đang có hàng giữ trong phạm vi.'),
    ('Ô lọc Trạng thái', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống',
     'Trong hạn / Hết hạn / Đến hạn — lọc theo trạng thái hạn giữ của từng lô.'),
    ('Ô lọc Nhân viên', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Chỉ liệt kê nhân viên ĐANG giữ hàng trong phạm vi; thu hẹp theo Công ty / Phòng ban đang '
     'chọn.'),
    ('Ô lọc Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống',
     'Chỉ hiện với người có V1 (hoặc Super admin). Biểu tượng ổ khóa cạnh nhãn là công tắc '
     '“Hiện cả công ty đã khoá”.'),
    ('Ô lọc Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống',
     'Người có V1 thấy phòng ban mọi công ty, còn lại thấy phòng ban công ty mình. Lọc lô theo '
     'nhân viên thuộc phòng ban. Biểu tượng ổ khóa là công tắc “Hiện cả phòng ban đã khoá”.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tìm kiếm', 'Click',
     'During:\n– Gom toàn bộ điều kiện, kể cả ô tìm nhanh.\n'
     'After:\n– Nạp lại từ trang 1; ô “Hiển thị a–b / N” cập nhật.'),
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'After:\n– Tự nạp lại từ trang 1, không cần bấm Tìm kiếm; thu gọn mọi cây đang mở.'),
    ('Đổi Công ty hoặc Phòng ban', 'Change',
     'During:\n– Xóa giá trị ô Nhân viên đang chọn và thu hẹp danh sách Nhân viên theo đơn vị '
     'mới.\nAfter:\n– Nạp lại danh sách.'),
    ('Bấm Làm mới', 'Click',
     'During:\n– Xóa toàn bộ điều kiện lọc, kể cả mã hàng hóa nhận từ đường dẫn, và bỏ sắp xếp.\n'
     'After:\n– Nạp lại danh sách mặc định từ trang 1.'),
    ('Rời màn rồi quay lại trong vòng 10 phút', 'System',
     'After:\n– Khôi phục bộ lọc và trạng thái đóng / mở của khu vực lọc nâng cao.'),
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
    mota='Cho phép người dùng chọn ô lọc nào được hiện ở khu vực Tìm kiếm nâng cao và sắp xếp '
         'thứ tự các ô.',
    tacnhan=TACNHAN,
    dieukien='Đang ở màn Danh sách hàng giữ.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc.\n'
          '2. Cửa sổ hiện tám mục: Mã hàng hóa, Tên hàng hóa, Lọc theo kho, Thương hiệu, Model, '
          'Trạng thái, Nhân viên, Công ty – Phòng ban, kèm ô tích chọn.\n'
          '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu; khu vực lọc vẽ lại theo cấu hình mới.',
    phu='• Bấm Khôi phục mặc định → về đủ tám mục theo thứ tự gốc.\n'
        '• Bấm Đóng hoặc dấu × → thoát, không lưu.\n'
        '• Mục “Công ty – Phòng ban” là một khối gồm hai ô, bật / tắt cùng nhau.',
    dacbiet='Cấu hình lưu theo từng màn hình, không ảnh hưởng màn khác.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc', modal='Cài đặt bộ lọc',
         shot=shot('03-cai-dat-bo-loc.png'), shot_caption='Cửa sổ Cài đặt bộ lọc')

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
     '“Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng '
     'màn hình.”'),
    ('Danh sách ô lọc', 'Table/Grid', 'Enable', 'Tám mục', 'Không', 'Theo cấu hình đã lưu',
     'Mỗi mục gồm số thứ tự, tay nắm kéo thả, ô tích chọn và tên ô lọc.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi nhận cấu hình và đóng cửa sổ.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đưa về cấu hình gốc của màn.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thoát, không lưu.'),
])

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi nhận các ô lọc được tích và thứ tự hiện tại.\n'
     'After:\n– Lưu cấu hình, đóng cửa sổ và vẽ lại khu vực lọc.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về đủ tám mục theo thứ tự gốc.'),
    ('Kéo thả một mục', 'Click', 'After:\n– Đổi vị trí ô lọc trong danh sách.'),
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
    mota='Cho phép bật / tắt và sắp xếp các cột của bảng cây hàng giữ.',
    tacnhan=TACNHAN,
    dieukien='Đang ở màn Danh sách hàng giữ.',
    chinh='1. Người dùng bấm nút biểu tượng cột ở thanh công cụ.\n'
          '2. Cửa sổ “Tuỳ chỉnh cột” hiện mười một cột kèm ô tích chọn.\n'
          '3. Người dùng tích / bỏ tích và kéo thả sắp xếp.\n'
          '4. Người dùng bấm Lưu; bảng vẽ lại theo cấu hình mới.',
    phu='• Cột STT, Mã hàng hóa / Nhân viên / Khách hàng (có biểu tượng ổ khóa) và Hành động bị '
        'khóa, không tắt được.\n'
        '• Bấm Đóng → thoát, không lưu.',
    dacbiet='Cấu hình lưu riêng cho từng người dùng.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tuỳ chỉnh cột', modal='Tuỳ chỉnh cột',
         shot=shot('04-cau-hinh-cot.png'), shot_caption='Cửa sổ Tuỳ chỉnh cột')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách cột', 'Table/Grid', 'Enable', 'Mười một cột', 'Không', 'Theo cấu hình đã lưu',
     'STT, Mã hàng hóa / Nhân viên / Khách hàng, Tên hàng hóa / Phòng ban, Đơn vị, Model, '
     'Thương hiệu, Tổng SL trong kho, SL giữ, Hạn giữ, Trạng thái, Hành động. Mặc định bật hết.'),
    ('Ô tích của cột bị khóa', 'Icon Button', 'Disable', '–', '–', 'Đang bật',
     'STT, Mã hàng hóa / Nhân viên / Khách hàng, Hành động luôn hiện.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi nhận cấu hình và vẽ lại bảng.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thoát, không lưu.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi nhận các cột được tích và thứ tự.\n'
     'After:\n– Lưu cấu hình theo người dùng và vẽ lại bảng.'),
    ('Bỏ tích một cột bị khóa', 'Click',
     'During:\n– Hệ thống không cho bỏ tích ba cột bị khóa.'),
])

# ------------------------------------------------------------ 2.5
d.h3('2.5 Xem chi tiết giữ hàng theo nhân viên và khách hàng')

d.p('2.5.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và Màn Xem chi tiết.', anchor='detail')
d.intro_table(
    ten='Mở cây chi tiết của một hàng hóa',
    mota='Bấm nút “>” ở dòng hàng hóa để chèn ngay bên dưới tầng 2 (mỗi nhân viên đang giữ hàng '
         'hóa đó) và tầng 3 (mỗi lô giữ theo khách hàng của nhân viên đó, kèm hạn giữ và trạng '
         'thái). Hai tầng nạp cùng một lần.',
    tacnhan=TACNHAN,
    dieukien='Đang ở màn Danh sách hàng giữ, bảng có ít nhất một hàng hóa.',
    chinh='1. Người dùng bấm nút tròn “>” ở cột STT của một hàng hóa.\n'
          '2. Nút chuyển sang biểu tượng quay trong lúc tải.\n'
          '3. Hệ thống lấy mọi lô còn hàng của hàng hóa đó, áp CÙNG phạm vi quyền và bộ lọc đang '
          'dùng ở tầng 1.\n'
          '4. Hệ thống gom theo nhân viên (sắp theo tên), trong mỗi nhân viên sắp lô theo tên '
          'khách hàng rồi hạn giữ.\n'
          '5. Bảng chèn dòng nhân viên (nền xanh nhạt) và dòng lô (nền xanh dương nhạt); nút đổi '
          'thành “v”.',
    phu='• Bấm lại nút “v” → thu gọn; mở lại lần sau dùng dữ liệu đã tải, không tải lại.\n'
        '• Đổi bộ lọc, sắp xếp hoặc lật trang → mọi cây đang mở bị thu gọn và dữ liệu đã tải bị '
        'xóa.\n'
        '• Lỗi khi tải → thông báo “Lỗi khi tải chi tiết giữ hàng”, cây không mở.\n'
        '• Có thể mở nhiều hàng hóa cùng lúc.',
    dacbiet=None)

d.p('2.5.2 Layout màn hình')
d.layout(menu=MENU + ' => Mở rộng dòng hàng hóa', shot=shot('05-mo-rong-nhan-vien-khach-hang.png'),
         shot_caption='Cây chi tiết: dòng nhân viên và dòng lô theo khách hàng')
d.layout(menu=MENU + ' => Mở rộng dòng hàng hóa', shot=shot('06-cot-han-giu-trang-thai.png'),
         shot_caption='Các cột Hạn giữ, Trạng thái, Hành động ở tầng lô')

d.p('2.5.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Dòng nhân viên – cột Mã hàng hóa / Nhân viên / Khách hàng', 'Table/Grid', 'Read-only', '–',
     'Theo dữ liệu', 'Biểu tượng người + họ tên nhân viên đang giữ.'),
    ('Dòng nhân viên – cột Tên hàng hóa / Phòng ban', 'Table/Grid', 'Read-only', '–',
     'Theo dữ liệu', 'Phòng ban hiện tại của nhân viên.'),
    ('Dòng nhân viên – cột SL giữ', 'Table/Grid', 'Read-only', '> 0', 'Theo dữ liệu',
     'Tổng SL các lô của nhân viên đó (khớp bộ lọc).'),
    ('Dòng nhân viên – các cột còn lại', 'Table/Grid', 'Read-only', '–', 'Trống',
     'Đơn vị, Model, Thương hiệu, Tổng SL trong kho, Hạn giữ, Trạng thái, Hành động để trống.'),
    ('Dòng lô – cột Mã hàng hóa / Nhân viên / Khách hàng', 'Table/Grid', 'Read-only', '–',
     'Theo dữ liệu', 'Biểu tượng cửa hàng + “Mã KH - Tên KH”.'),
    ('Dòng lô – cột SL giữ', 'Table/Grid', 'Read-only', '> 0', 'Theo dữ liệu',
     'Số lượng của riêng lô đó.'),
    ('Dòng lô – cột Hạn giữ', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
     'Để trống nếu lô không có hạn giữ.'),
    ('Dòng lô – cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 3 giá trị', 'Theo dữ liệu',
     'Trong hạn (xanh lá), Đến hạn (vàng), Hết hạn (đỏ) — tính theo ngày hôm nay.'),
    ('Dòng lô – nút Lịch sử giữ hàng', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Biểu tượng đồng hồ, mở FR-07. Chỉ có ở tầng lô.'),
    ('Ký hiệu nhánh “└”', 'Label', 'Hiển thị', '–', 'Hiển thị',
     'Thay cho nút ở cột STT của dòng nhân viên và dòng lô.'),
], required=False)

d.p('2.5.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút “>” ở dòng hàng hóa', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng.\n'
     'During:\n– Lần đầu: tải chi tiết với cùng phạm vi + bộ lọc của tầng 1 (kể cả từ khóa khách '
     'hàng, nhân viên, công ty, phòng ban, trạng thái).\n'
     '– Chỉ lấy lô có số lượng lớn hơn 0.\n'
     'After:\n– Chèn dòng nhân viên và dòng lô ngay dưới hàng hóa; cộng SL giữ ở dòng nhân viên.'),
    ('Bấm nút “v” ở dòng hàng hóa đang mở', 'Click',
     'After:\n– Thu gọn, giữ dữ liệu đã tải để lần mở sau hiện ngay.'),
])

# ------------------------------------------------------------ 2.6
d.h3('2.6 Đổi đơn vị hiển thị số lượng')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Đổi đơn vị hiển thị số lượng', 'view', (), actor=ACTOR,
            caption='Biểu đồ Use Case — FR-06 Đổi đơn vị hiển thị số lượng')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Danh sách.', anchor='list')
d.intro_table(
    ten='Đổi đơn vị tính để xem số lượng',
    mota='Với hàng hóa có từ hai đơn vị tính trở lên, người dùng chọn đơn vị khác ở cột Đơn vị để '
         'xem mọi số lượng của hàng hóa đó quy đổi theo đơn vị vừa chọn. Chỉ đổi cách hiển thị, '
         'không đổi dữ liệu.',
    tacnhan=TACNHAN,
    dieukien='Hàng hóa có từ hai đơn vị tính trở lên.',
    chinh='1. Người dùng mở ô Đơn vị ở dòng hàng hóa.\n'
          '2. Danh sách hiện các đơn vị, đơn vị cơ bản đứng đầu; đơn vị có hệ số khác 1 ghi kèm '
          '“(x hệ số)”.\n'
          '3. Người dùng chọn một đơn vị.\n'
          '4. Hệ thống chia mọi số lượng của hàng hóa đó cho hệ số, làm tròn XUỐNG 2 chữ số thập '
          'phân.',
    phu='• Hàng hóa chỉ có một đơn vị → cột Đơn vị chỉ hiện chữ, không có ô chọn.\n'
        '• Việc đổi đơn vị không lưu lại: tải lại trang thì về đơn vị cơ bản.\n'
        '• Xuất Excel và bản In luôn dùng đơn vị cơ bản, không theo đơn vị đang chọn.',
    dacbiet='Áp cho Tổng SL trong kho, SL giữ ở cả ba tầng và các số lượng trong cửa sổ Lịch sử '
            'giữ hàng của hàng hóa đó.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU, shot=shot('01-danh-sach.png'),
         shot_caption='Cột Đơn vị trên bảng danh sách')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô chọn Đơn vị', 'Dropdown', 'Enable / Read-only', 'Danh sách đơn vị của hàng hóa', 'Không',
     'Đơn vị cơ bản', 'Không có nút xóa trắng; placeholder “Chọn đơn vị”.'),
    ('Số lượng sau quy đổi', 'Number', 'Read-only', '≥ 0, tối đa 2 chữ số thập phân', '–',
     'Theo đơn vị cơ bản', 'Định dạng 1,234.56; làm tròn xuống.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn một đơn vị', 'Change',
     'During:\n– Lấy hệ số quy đổi của đơn vị vừa chọn.\n'
     'After:\n– Hiển thị lại số lượng của hàng hóa đó ở cả ba tầng, không gọi lại máy chủ.'),
])

# ------------------------------------------------------------ 2.7
d.h3('2.7 Xem lịch sử giữ hàng của lô')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Màn này hiển thị SỔ BIẾN ĐỘNG số lượng, không phải lịch sử '
           'chỉnh sửa bản ghi.', anchor='history')
d.intro_table(
    ten='Xem lịch sử giữ hàng',
    mota='Cửa sổ liệt kê mọi lần số hàng giữ tăng / giảm của cặp hàng hóa × nhân viên × khách '
         'hàng × công ty, kèm chứng từ gây ra biến động, sắp từ CŨ đến MỚI.',
    tacnhan=TACNHAN,
    dieukien='Đã mở cây chi tiết của một hàng hóa (FR-05).',
    chinh='1. Người dùng bấm nút Lịch sử giữ hàng ở một dòng lô.\n'
          '2. Cửa sổ “Lịch sử giữ hàng” mở, tiêu đề phụ “Hàng hóa: Mã - Tên”.\n'
          '3. Khối thông tin hiện Mã hàng, Tên hàng, Kinh doanh, Khách hàng, Trạng thái kèm “(Hạn '
          'giữ hiện tại: dd/mm/yyyy)”.\n'
          '4. Hệ thống tải sổ biến động và hiển thị bảng.\n'
          '5. Người dùng bấm vào mã chứng từ để mở chứng từ ở thẻ mới, hoặc bấm Đóng.',
    phu='• Chưa có biến động → dòng “Chưa có biến động nào.”.\n'
        '• Lỗi khi tải → “Không tải được lịch sử giữ hàng.” kèm nút Thử lại.\n'
        '• Chứng từ không dựng được liên kết → hiện mã dạng chữ; không xác định được chứng từ → '
        'hiện “—”.',
    dacbiet=None)

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Mở rộng dòng hàng hóa => Lịch sử giữ hàng',
         modal='Lịch sử giữ hàng', shot=shot('07-lich-su-giu-hang.png'),
         shot_caption='Cửa sổ Lịch sử giữ hàng')

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử giữ hàng',
     'Kèm dòng phụ “Hàng hóa: <mã> - <tên>”.'),
    ('Khối thông tin', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mã hàng; Tên hàng; Kinh doanh (“Mã NV - Tên NV”); Khách hàng (“Mã KH - Tên KH”); Trạng '
     'thái (badge + “(Hạn giữ hiện tại: dd/mm/yyyy)”).'),
    ('Dòng Số lượng giữ hiện tại', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
     '“Số lượng giữ hiện tại: <SL của lô> <đơn vị đang chọn>”.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự', '–'),
    ('Cột SL biến động', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tăng có dấu “+” chữ xanh lá; giảm có dấu “-” chữ đỏ.'),
    ('Cột Ngày', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Ngày phát sinh biến động.'),
    ('Cột SL giữ', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Số lượng giữ CỘNG DỒN sau lần biến động đó.'),
    ('Cột Hạn giữ', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', 'Hạn giữ của lô.'),
    ('Cột Chứng từ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mã chứng từ (vd PXG-, PPBHĐC-, PGHHG-…) là liên kết mở thẻ mới.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lịch sử giữ hàng', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng.\n'
     'During:\n– Tìm mọi lô của cặp hàng hóa × nhân viên × khách hàng × công ty rồi lấy sổ biến '
     'động của chúng, sắp cũ → mới.\n'
     '– Biến động không ghi chứng từ thì lấy chứng từ gốc đã sinh ra lô.\n'
     'After:\n– Hiển thị bảng, số lượng quy đổi theo đơn vị đang chọn ở dòng hàng hóa.'),
    ('Bấm mã chứng từ', 'Click', 'After:\n– Mở màn chi tiết chứng từ ở thẻ mới.'),
    ('Bấm Thử lại', 'Click', 'After:\n– Tải lại sổ biến động.'),
])

# ------------------------------------------------------------ 2.8
d.h3('2.8 Xuất danh sách hàng giữ ra Excel')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Xuất danh sách hàng giữ ra Excel', 'io', (), actor=ACTOR,
            caption='Biểu đồ Use Case — FR-08 Xuất danh sách hàng giữ ra Excel')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột.', anchor='excel')
d.intro_table(
    ten='Xuất danh sách hàng giữ ra Excel',
    mota='Xuất tệp Excel PHẲNG — mỗi dòng là MỘT LÔ giữ (hàng hóa × nhân viên × khách hàng × hạn '
         'giữ) — theo bộ lọc đang áp, với các trường người dùng tự chọn.',
    tacnhan=TACNHAN,
    dieukien='Đang ở màn Danh sách hàng giữ.',
    chinh='1. Người dùng bấm nút Xuất Excel.\n'
          '2. Cửa sổ “Chọn trường xuất Excel” mở, tích sẵn đủ 12 trường.\n'
          '3. Người dùng tích thêm / bỏ bớt, kéo thả đổi thứ tự.\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống tải về tệp “danh_sach_hang_giu.xlsx” và báo “Xuất Excel thành công”.',
    phu='• Bấm “Chọn tất cả” / “Bỏ chọn hết” để chọn nhanh; dòng cuối hiện “Đang chọn x/12 '
        'trường”.\n'
        '• Đang xuất thì nút bị khóa để tránh bấm hai lần.\n'
        '• Bấm Đóng → thoát, không xuất.\n'
        '• Lỗi khi xuất → “Lỗi khi xuất Excel”.',
    dacbiet='Thứ tự cột trong tệp theo thứ tự trường đã chọn; cột STT luôn đứng đầu. Số lượng '
            'luôn theo đơn vị cơ bản. Tệp chỉ chứa lô trong phạm vi quyền.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel', modal='Chọn trường xuất Excel',
         shot=shot('08-xuat-excel.png'), shot_caption='Cửa sổ Chọn trường xuất Excel')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn trường xuất Excel', '–'),
    ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
     '“Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
    ('Danh sách trường', 'Table/Grid', 'Enable', 'Mười hai trường', 'Có',
     'Tích đủ 12 trường',
     'Mã hàng hóa, Tên hàng hóa, ĐVT, Model, Thương hiệu, Nhân viên giữ, Phòng ban, Khách hàng, '
     'SL giữ, Tổng SL trong kho, Hạn giữ, Trạng thái.'),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Dòng “Đang chọn x/12 trường”', 'Label', 'Read-only', '0 – 12', '–', 'Theo lựa chọn', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Bị khóa trong lúc đang xuất.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thoát, không xuất.'),
])

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ chọn trường, tích sẵn đủ 12 trường (không phụ thuộc cột đang ẩn / '
     'hiện trên bảng).'),
    ('Bấm Xuất file', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng; khóa nút.\n'
     'During:\n– Lấy mọi lô khớp bộ lọc + phạm vi quyền, sắp theo Phòng ban → Nhân viên → Tên '
     'hàng hóa (không theo thứ tự sắp xếp trên bảng).\n'
     'After:\n– Dựng tệp: dòng tiêu đề “DANH SÁCH HÀNG GIỮ”, dòng tên cột, mỗi lô một dòng; cột '
     'số là số thật định dạng 1,234.5; ngày dạng dd/mm/yyyy.\n'
     '– Tải tệp về máy, đóng cửa sổ và hiển thị “Xuất Excel thành công”.'),
])

# ------------------------------------------------------------ 2.9
d.h3('2.9 In danh sách hàng giữ')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'In danh sách hàng giữ', 'io', (), actor=ACTOR,
            caption='Biểu đồ Use Case — FR-09 In danh sách hàng giữ')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX.', anchor='notice')
d.intro_table(
    ten='In danh sách hàng giữ',
    mota='Mở cửa sổ xem trước bản in khổ A4 ngang của toàn bộ lô khớp bộ lọc, gom theo Phòng ban '
         '→ Nhân viên → Lô hàng, rồi gửi lệnh in.',
    tacnhan=TACNHAN,
    dieukien='Đang ở màn Danh sách hàng giữ.',
    chinh='1. Người dùng bấm nút In trên thanh công cụ.\n'
          '2. Hệ thống dựng bản in theo bộ lọc đang áp và phạm vi quyền.\n'
          '3. Cửa sổ “Xem trước danh sách hàng giữ” mở ngay trên màn.\n'
          '4. Người dùng bấm nút In trong cửa sổ để gửi lệnh in của trình duyệt.',
    phu='• Danh sách vượt 10,000 dòng in → cửa sổ hiện “Danh sách có N dòng, vượt mức in tối đa '
        '10,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) '
        'rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.” và ẩn nút In.\n'
        '• Không có lô nào → bảng in một dòng “Không có dữ liệu”.\n'
        '• Lỗi khi tải → “Không tải được dữ liệu in”.\n'
        '• Bấm dấu × → đóng cửa sổ.',
    dacbiet='Bố cục bản in gom Phòng ban → Nhân viên → Lô, KHÁC bảng trên màn (Hàng hóa → Nhân '
            'viên → Khách hàng); giữ đúng bố cục của hệ thống cũ để kế toán đối chiếu.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => In', modal='Xem trước danh sách hàng giữ',
         shot=shot('09-in-danh-sach.png'), shot_caption='Cửa sổ xem trước bản in danh sách hàng giữ')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Xem trước danh sách hàng giữ', '–'),
    ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', 'Ẩn khi vượt mức in tối đa.'),
    ('Tiêu đề công ty (letterhead)', 'Label', 'Read-only', '–', 'Theo công ty',
     'Lấy theo công ty của người đang đăng nhập.'),
    ('Tiêu đề bản in', 'Label', 'Read-only', '–', 'DANH SÁCH HÀNG GIỮ', '–'),
    ('Khối thông tin', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Ngày in (dd/mm/yyyy); Số phòng ban; Số nhân viên; Số mục hàng (số lô).'),
    ('Bảng in', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cột STT, Tên hàng hóa, Mã hàng, ĐVT, SL giữ, Hạn giữ, Khách hàng, Trạng thái. STT đánh '
     '1 (phòng ban – “Tên PB - N nhân viên - M mục hàng”), 1.1 (nhân viên – “Tên NV - K mục '
     'hàng”), 1.1.1 (lô). Nhân viên chưa gán phòng ban gom vào “Chưa gán phòng ban”.'),
    ('Dòng thông báo vượt mức in', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
     'Hiện khi tổng số dòng in vượt 10,000.'),
    ('Nút đóng (×)', 'Icon Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ xem trước.'),
], required=False)

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In trên thanh công cụ', 'Click',
     'Before:\n– Kiểm tra quyền Quản lý giữ hàng.\n'
     'During:\n– Lấy mọi lô khớp bộ lọc + phạm vi, gom Phòng ban → Nhân viên → Lô; số dòng in = '
     'số phòng ban + số nhân viên + số lô.\n'
     '– Vượt 10,000 dòng → không dựng nội dung, trả thông báo thu hẹp bộ lọc.\n'
     'After:\n– Mở cửa sổ xem trước khổ A4 ngang.'),
    ('Bấm In trong cửa sổ', 'Click', 'After:\n– Gửi lệnh in của trình duyệt.'),
])

# ==================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('- Quy tắc chung toàn hệ thống. Bảng dưới đây chỉ liệt kê quy tắc đặc thù của màn '
           'Danh sách hàng giữ.', head='Quy tắc áp dụng', anchor='list')

d.rule_table([
    ('BR-01', 'Màn chỉ đọc', [
        '– Màn không có Thêm, Sửa, Xóa, Import; không thao tác nào làm thay đổi hàng giữ.',
        '– Hàng giữ chỉ thay đổi qua các phiếu: xuất giữ, gia hạn, hủy, điều chuyển hàng giữ, '
        'xuất bán.',
    ], 'Toàn màn hình'),
    ('BR-02', 'Quyền vào màn', [
        '– Bắt buộc có quyền Quản lý giữ hàng, hoặc là Super admin.',
        '– Quyền xem theo cấp KHÔNG thay được quyền này.',
        '– Khác hệ thống cũ (mọi tài khoản đều vào được) — chủ đích, user chốt 18/08/2026.',
    ], 'Toàn màn hình'),
    ('BR-03', 'Phạm vi dữ liệu', [
        '– Xét theo thứ tự: V1 mọi công ty → V2 lô thuộc công ty mình → V3 lô của nhân viên '
        'thuộc phòng ban mình quản lý + phòng mình + chính mình → còn lại chỉ lô của mình.',
        '– Cấp công ty xét theo CÔNG TY GHI TRÊN LÔ, không theo công ty hiện tại của nhân viên.',
        '– Áp thống nhất cho ba tầng, danh sách chọn của bộ lọc, Xuất Excel, In và Lịch sử.',
    ], 'Toàn màn hình'),
    ('BR-04', 'Lô được tính', [
        '– Chỉ tính lô có số lượng lớn hơn 0; lô đã về 0 không hiện ở bảng, Excel hay bản In.',
        '– Tầng hàng hóa chỉ hiện hàng hóa có tổng SL giữ lớn hơn 0 sau khi lọc.',
    ], ['Xem danh sách', 'Xuất Excel', 'In']),
    ('BR-05', 'Trạng thái hạn giữ', [
        '– Tính tại thời điểm xem: hạn giữ sau hôm nay → Trong hạn; đúng hôm nay → Đến hạn; '
        'trước hôm nay → Hết hạn.',
        '– So theo NGÀY, không theo giờ, ở mọi nơi (bảng, bộ lọc, Excel, In) — vá lỗi hệ thống cũ '
        'so ngày với giờ nên lô hết hạn hôm nay ra hai kết quả.',
        '– Màu: Trong hạn xanh lá, Đến hạn vàng, Hết hạn đỏ.',
    ], ['Xem chi tiết', 'Tìm kiếm và lọc', 'Xuất Excel', 'In', 'Lịch sử']),
    ('BR-06', 'Cách cộng số lượng', [
        '– SL giữ tầng hàng hóa = tổng các lô khớp bộ lọc; tầng nhân viên = tổng các lô của '
        'nhân viên đó; tầng lô = số của lô.',
        '– Tầng hàng hóa không hiện nhân viên / hạn giữ (vá lỗi hệ thống cũ hiện giá trị của một '
        'lô bất kỳ).',
    ], ['Xem danh sách', 'Xem chi tiết']),
    ('BR-07', 'Tổng SL trong kho', [
        '– Tổng tồn kho kế toán của hàng hóa ở các kho kế toán.',
        '– Người không có V1 chỉ cộng kho thuộc công ty mình; chọn ô lọc Công ty thì chỉ cộng kho '
        'của công ty đó.',
        '– Ô lọc Kho KHÔNG làm thay đổi con số này (vẫn cộng mọi kho trong phạm vi công ty).',
        '– Hàng hóa chưa có tồn kho kế toán thì để trống.',
    ], ['Xem danh sách', 'Xuất Excel']),
    ('BR-08', 'Một bộ điều kiện lọc cho mọi nơi', [
        '– Cùng một bộ điều kiện áp cho tầng 1, tầng 2–3, Xuất Excel và In — vá lỗi hệ thống cũ '
        'lọc khách hàng ở tầng 1 nhưng xổ chi tiết vẫn hiện mọi khách, và In / Xuất khóa cứng công '
        'ty người đăng nhập.',
        '– Ô tìm nhanh tìm theo khách hàng của lô (tên, mã, số điện thoại).',
        '– Lọc theo kho: chỉ giữ hàng hóa có tồn kho kế toán ghi nhận ở kho đã chọn (hàng giữ '
        'không gắn kho).',
        '– Danh sách chọn Thương hiệu, Model, Nhân viên chỉ gồm giá trị đang có hàng giữ trong '
        'phạm vi.',
    ], ['Tìm kiếm và lọc', 'Xem chi tiết', 'Xuất Excel', 'In']),
    ('BR-09', 'Đơn vị tính', [
        '– Hàng giữ luôn lưu theo đơn vị cơ bản.',
        '– Ô Đơn vị chỉ đổi cách hiển thị: chia cho hệ số, làm tròn xuống 2 chữ số thập phân.',
        '– Xuất Excel và In luôn theo đơn vị cơ bản, có cột ĐVT.',
    ], ['Đổi đơn vị', 'Xuất Excel', 'In', 'Lịch sử']),
    ('BR-10', 'Sổ biến động sắp cũ → mới', [
        '– Lịch sử giữ hàng sắp từ cũ đến mới vì cột SL giữ là số cộng dồn sau mỗi lần biến '
        'động.',
        '– Đây là ngoại lệ có chủ đích so với quy tắc chung “lịch sử sắp mới → cũ”.',
        '– Biến động không ghi chứng từ thì hiển thị chứng từ gốc sinh ra lô.',
    ], 'Lịch sử giữ hàng'),
    ('BR-11', 'Bản in và giới hạn', [
        '– Bản in gom Phòng ban → Nhân viên → Lô, khổ A4 ngang, số lượng theo đơn vị cơ bản, '
        'định dạng 1,234.5.',
        '– Tối đa 10,000 dòng in; vượt thì không in, hướng dẫn thu hẹp bộ lọc hoặc Xuất Excel '
        '(hệ thống cũ chuyển sang gửi thư — không chuyển sang hệ thống mới).',
    ], 'In'),
    ('BR-12', 'Xuất Excel phẳng', [
        '– Mỗi dòng là một lô; cột Tổng SL trong kho lặp lại trên mọi dòng của cùng hàng hóa, '
        'không cộng dọc cột này.',
        '– Thứ tự cột theo thứ tự chọn; STT luôn đầu tiên.',
    ], 'Xuất Excel'),
])

d.save()
