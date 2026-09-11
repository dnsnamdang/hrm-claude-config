# -*- coding: utf-8 -*-
"""Sinh SRS (.docx) cho man "Phieu thu tien" (phan he Tai chinh).

Form chuan 2026-08-28 (4 chuong, Layout ghi MENU, rule_ref dau moi muc Gioi thieu,
Phan 4 la bang 5 cot, so do tong quan co phan cap).

Nguon doc code 03/09/2026 (nhanh gop_db) — xem docblock gen_testcase.py cung thu muc.
Anh that: pt_shots/ (dung chung voi HDSD).

Chay:  python .plans/gop-db/finance-bill-income/gen_srs.py
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

SHOTS = os.path.join(HERE, 'pt_shots')
OUT = os.path.join(HERE, 'SRS - Phiếu thu tiền.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu thu'

ACTOR_KT = 'Kế toán thanh toán'
ACTOR_TQ = 'Thủ quỹ'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/bill-incomes',
           full_url='https://hrm-crm.eteksofts.com/finance/bill-incomes',
           img_prefix='pt_')

# ============================================================== TRANG ĐẦU
d.title_block('Phiếu thu tiền')

d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu thu tiền, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ vòng đời phiếu thu bốn trạng thái và ràng buộc “một phiếu đề nghị chỉ lập được một '
    'phiếu thu”.',
    'Làm rõ thời điểm DUY NHẤT hệ thống ghi bút toán vào sổ kế toán (bước Duyệt) và các cơ chế '
    'chống ghi trùng bút toán.',
    'Làm rõ cơ chế đồng bộ ngược trạng thái và số tiền thực thu sang màn Phiếu đề nghị thu tiền, '
    'kèm ba điểm hở đã biết và được chấp nhận có chủ đích.',
    'Làm rõ quy tắc cột “Số tiền” của màn danh sách luôn là tổng số tiền duyệt thu — điểm dễ bị '
    'hiểu nhầm là lỗi.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu thu tiền',
     'Chứng từ kế toán lập từ MỘT phiếu đề nghị thu tiền đang chờ duyệt. Mã sinh tự động dạng '
     '“{mã công ty}.PT{tháng năm}.{5 chữ số}”, ví dụ TPE.PT0926.00001.'),
    ('Phiếu đề nghị thu tiền',
     'Chứng từ do người kinh doanh lập trước đó. Một phiếu đề nghị chỉ lập được đúng một phiếu '
     'thu; ràng buộc này kiểm bằng khóa dòng nên hai người bấm lưu cùng lúc vẫn chỉ ra một phiếu.'),
    ('Dòng chi tiết',
     'Một dòng trong bảng Chi tiết, kéo thẳng từ phiếu đề nghị. Không thêm và không xóa dòng '
     'được; muốn đổi phải chọn phiếu đề nghị khác.'),
    ('Tài khoản nợ',
     'Tài khoản ghi bên Nợ của bút toán, khai một lần cho cả phiếu (thường là tài khoản tiền).'),
    ('Số tài khoản có',
     'Tài khoản ghi bên Có, khai riêng cho từng dòng chi tiết (thường là tài khoản phải thu).'),
    ('Số tiền đề nghị thu', 'Số tiền lấy từ phiếu đề nghị. Chỉ đọc.'),
    ('Số tiền duyệt thu',
     'Số tiền kế toán chốt sẽ thu, do người lập phiếu thu nhập. Tổng của cột này là giá trị cột '
     '“Số tiền” trên màn danh sách.'),
    ('Số tiền thực thu',
     'Số tiền thủ quỹ thực nhận, nhập ngay trong bảng ở màn xem chi tiết trước khi Duyệt. Không '
     'được lớn hơn số tiền duyệt thu của chính dòng đó.'),
    ('Phân bổ',
     'Thao tác điền hộ: thủ quỹ nhập tổng tiền thực nhận, hệ thống rải xuống cột Số tiền thực thu '
     'theo thứ tự từ trên xuống, mỗi dòng tối đa bằng số duyệt thu của nó. Chỉ điền vào ô, chưa '
     'ghi dữ liệu.'),
    ('Ngày hạch toán', 'Ngày ghi bút toán vào sổ kế toán; hệ thống lấy ngày duyệt phiếu.'),
    ('Đang tạo', 'Phiếu nháp. Chỉ người lập nhìn thấy, sửa được và xóa được.'),
    ('Chờ duyệt', 'Phiếu đã gửi, chờ thủ quỹ duyệt hoặc hủy. Không sửa, không xóa được.'),
    ('Đã duyệt',
     'Thủ quỹ đã duyệt; hệ thống đã ghi bút toán vào sổ kế toán. Không sửa, không xóa, không hủy '
     'được nữa.'),
    ('Hủy',
     'Thủ quỹ đã hủy phiếu kèm lý do. Không ghi bút toán. Phiếu đề nghị tương ứng cũng chuyển '
     'sang Hủy và không lập lại được phiếu thu khác.'),
], widths=[1.9, 4.1])

# ========================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán thanh toán',
     'Mở được cửa sổ chọn phiếu đề nghị; lập, sửa và xóa phiếu thu. Kiểm tra thực hiện ở phía '
     'máy chủ tại các endpoint ghi dữ liệu, không dựa vào việc giao diện ẩn nút.'),
    ('Q2', 'Thủ quỹ duyệt phiếu thu',
     'Nhập số tiền thực thu; bấm Duyệt phiếu thu và Hủy phiếu thu. Đồng thời là nhóm nhận thông '
     'báo khi có phiếu thu mới được gửi duyệt trong cùng công ty.'),
], widths=[0.8, 2.0, 3.2])
d.p('Các chức năng Xem danh sách, Xem chi tiết, In, Xuất Excel và Lịch sử KHÔNG gắn quyền riêng: '
    'chỉ cần người dùng nhìn thấy được phiếu theo phạm vi dữ liệu ở mục dưới.')

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả phiếu thu của tổng công ty', 'Toàn bộ phiếu thu của mọi công ty.'),
    ('V2', 'Xem tất cả phiếu thu của công ty',
     'Phiếu thu thuộc công ty của người đăng nhập. Không xác định được công ty thì rơi về nhánh '
     '“chỉ phiếu của mình”.'),
    ('—', '(không có cấp nào)', 'Chỉ phiếu thu do chính mình lập.'),
], widths=[0.8, 2.2, 3.0])
d.p('Vai trò quản trị hệ thống được xử lý tương đương V1 và được coi như có cả Q1 lẫn Q2.')
d.p('Ba lớp bảo vệ dữ liệu áp dụng SAU CÙNG, không quyền nào gỡ được:')
d.bullets([
    'Phiếu ở trạng thái Đang tạo của người khác luôn bị loại khỏi danh sách, kể cả với V1 và '
    'quản trị hệ thống.',
    'Không xác định được người đăng nhập thì danh sách rỗng tuyệt đối (fail-closed theo cấu trúc '
    'truy vấn, không dựa vào việc dữ liệu tình cờ không có giá trị rỗng).',
    'Người đã duyệt một phiếu luôn mở lại được phiếu đó ở màn chi tiết, kể cả khi phiếu thuộc '
    'công ty khác — nhưng phiếu đó vẫn không xuất hiện trên danh sách của họ.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Không có quyền nào'], [
    ('FR-01 Truy cập & xem danh sách', '✅ (theo phạm vi V1–V2)', '✅ (theo phạm vi V1–V2)',
     '✅ (chỉ phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc danh sách', '✅', '✅', '✅'),
    ('FR-03 Tuỳ chỉnh bộ lọc và cột hiển thị', '✅', '✅', '✅'),
    ('FR-04 Tạo mới phiếu thu', '✅', '❌', '❌'),
    ('FR-05 Chọn phiếu đề nghị từ popup', '✅', '❌', '❌'),
    ('FR-06 Sửa phiếu thu', '✅ (chỉ phiếu Đang tạo)', '❌', '❌'),
    ('FR-07 Xem chi tiết phiếu thu', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-08 Duyệt phiếu thu', '❌', '✅ (chỉ phiếu Chờ duyệt)', '❌'),
    ('FR-09 Hủy phiếu thu', '❌', '✅ (chỉ phiếu Chờ duyệt)', '❌'),
    ('FR-10 Xóa phiếu thu', '✅ (chỉ phiếu Đang tạo của mình)', '❌', '❌'),
    ('FR-11 In phiếu thu', '✅', '✅', '✅ (phiếu xem được)'),
    ('FR-12 Xuất Excel một phiếu', '✅', '✅', '✅ (phiếu xem được)'),
    ('FR-13 Xem lịch sử thay đổi', '✅', '✅', '✅ (phiếu xem được)'),
], widths=[2.2, 1.5, 1.4, 1.4])

# ========================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR_KT, [0, 1, 2, 3]),
     (ACTOR_TQ, [0, 3])],
    [('FR-01', 'Xem danh sách phiếu thu', 'view'),
     ('FR-04', 'Tạo mới phiếu thu', 'crud'),
     ('FR-06', 'Sửa phiếu thu', 'crud'),
     ('FR-07', 'Xem chi tiết phiếu thu', 'view')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Tuỳ chỉnh bộ lọc và cột', 'view', 'extend', [0], None),
     ('FR-10', 'Xóa phiếu thu', 'action', 'extend', [0], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-05', 'Chọn phiếu đề nghị từ popup', 'crud', 'include', [1, 2], None),
     ('FR-08', 'Duyệt phiếu thu', 'action', 'extend', [3], None),
     ('FR-09', 'Hủy phiếu thu', 'action', 'extend', [3], None),
     ('FR-11', 'In phiếu thu', 'io', 'extend', [3], None),
     ('FR-12', 'Xuất Excel một phiếu', 'io', 'extend', [3], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu thu tiền')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------ 2.1 FR-01
d.h3('2.1 Xem danh sách phiếu thu')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu thu tiền tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu thu',
    mota='Hiển thị bảng phiếu thu nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân trang '
         'và ô thống kê tổng số phiếu khớp bộ lọc. Chỉ có một mục menu trỏ vào màn này; ba cách '
         'xem trước đây (“của tôi”, “chờ duyệt”, “đã duyệt”) nay là ô lọc Người lập và ô lọc '
         'Trạng thái.',
    tacnhan='%s; %s; Người dùng đã đăng nhập' % (ACTOR_KT, ACTOR_TQ),
    dieukien='Người dùng đã đăng nhập vào phân hệ Tài chính.',
    chinh='1. Người dùng vào menu Tài chính → Quản lý tiền → Thanh toán tiền mặt → Phiếu thu.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền cao nhất mà người dùng có '
          '(V1 → V2 → không có cấp nào).\n'
          '3. Hệ thống loại bỏ phiếu Đang tạo của người khác khỏi kết quả.\n'
          '4. Hệ thống trả về trang đầu tiên, sắp xếp theo Ngày tạo giảm dần, kèm tổng số phiếu, '
          'danh sách trạng thái và danh sách loại thu để dựng ô lọc.\n'
          '5. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp bộ lọc.” và '
        'dòng đếm ghi “Không có phiếu nào.”\n'
        '• Không xác định được người đăng nhập → danh sách rỗng tuyệt đối.\n'
        '• Có bộ lọc đã lưu trong vòng 10 phút → khôi phục bộ lọc đó rồi mới nạp dữ liệu.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('01-danh-sach.png'),
         shot_caption='Màn Danh sách phiếu thu lúc mới truy cập')
d.figure(shot('02-danh-sach-cot-phai.png'),
         'Danh sách sau khi cuộn ngang — thấy cột Trạng thái và Hành động', width_in=6.2)

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Danh sách phiếu thu',
     'Hiển thị ở thanh tiêu đề và ở đầu khối lưới.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Luôn hiển thị, không gắn cờ quyền ở giao diện; quyền Q1 chặn ở phía máy chủ.'),
    ('Nút cấu hình cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột hiển thị.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự theo trang',
     'Luôn hiển thị, không tắt được.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '{mã công ty}.PT{tháng năm}.{5 chữ số}',
     'Theo dữ liệu',
     'Luôn hiển thị, không tắt được; là đường dẫn sang màn chi tiết. Sắp xếp được.'),
    ('Cột Mã phiếu đề nghị thu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là đường dẫn MỞ TAB MỚI sang màn chi tiết Phiếu đề nghị thu tiền.'),
    ('Cột Loại thu', 'Table/Grid', 'Read-only', 'Danh sách 3 giá trị', 'Theo dữ liệu',
     'Thu bán hàng / Thu nhà cung cấp / Thu khác. Đọc xuyên quan hệ từ phiếu đề nghị.'),
    ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mã và tên khách hàng của DÒNG CHI TIẾT ĐẦU TIÊN; phiếu thu nhà cung cấp hiện dấu gạch ngang.'),
    ('Cột Số tiền', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Tổng số tiền DUYỆT THU của phiếu, căn phải, ngăn cách hàng nghìn. Sắp xếp được.'),
    ('Cột Người đề nghị', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người lập phiếu đề nghị, khác cột Người tạo.'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người lập phiếu thu.'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Cột sắp xếp mặc định, chiều giảm dần.'),
    ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Luôn có dữ liệu vì hệ thống ghi người sửa ở mọi lần lưu.'),
    ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 4 giá trị', 'Theo dữ liệu',
     'Nhãn đỏ với Đang tạo / Chờ duyệt / Hủy; nhãn xanh với Đã duyệt.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo trạng thái và quyền',
     'Luôn hiển thị, không tắt được. Tối đa 2–3 nút chính, phần còn lại trong menu ba chấm.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc và nằm trong phạm vi quyền.'),
    ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, cỡ 10',
     'Đổi cỡ trang đưa danh sách về trang 1.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi N = 0.'),
    ('Thanh cuộn ngang', 'Table/Grid', 'Enable', '–', 'Hiển thị',
     'Có ở cả trên và dưới bảng vì bảng 13 cột rộng hơn màn hình.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Khôi phục bộ lọc đã lưu nếu còn trong 10 phút.\n'
     '– Xác định cấp quyền xem cao nhất của người dùng.\n'
     'During:\n– Áp phạm vi dữ liệu theo cấp quyền.\n'
     '– Loại bỏ phiếu Đang tạo của người khác.\n'
     'After:\n– Trả về trang 1 sắp xếp theo Ngày tạo giảm dần, kèm tổng số phiếu, danh sách '
     'trạng thái và danh sách loại thu.'),
    ('Bấm tiêu đề cột sắp xếp', 'Click',
     'Before:\n– Chỉ nhận bốn cột: Mã phiếu, Số tiền, Ngày tạo, Ngày cập nhật.\n'
     'During:\n– Cột ngoài danh sách trên bị bỏ qua.\n'
     'After:\n– Đảo chiều sắp xếp, đưa về trang 1, giữ nguyên bộ lọc.'),
    ('Bấm mã phiếu', 'Click', 'After:\n– Điều hướng sang màn chi tiết phiếu thu tương ứng.'),
    ('Bấm mã phiếu đề nghị thu', 'Click',
     'After:\n– Mở TAB MỚI sang màn chi tiết Phiếu đề nghị thu tiền; tab hiện tại giữ nguyên bộ '
     'lọc và trang đang xem.'),
    ('Bấm số trang / đổi số dòng mỗi trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và chiều sắp xếp.\n'
     'After:\n– Nạp lại dữ liệu; đổi cỡ trang thì đưa về trang 1.'),
])

# ------------------------------------------------------ 2.2 FR-02
d.h3('2.2 Tìm kiếm và lọc danh sách')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Phiếu '
           'thu tiền tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu thu',
    mota='Thu hẹp danh sách theo mã phiếu, đơn vị tổ chức, mã phiếu đề nghị, loại thu, trạng '
         'thái, người lập, người đề nghị, khách hàng, số hợp đồng, khoảng số tiền và khoảng ngày '
         'lập. Các điều kiện cộng dồn với nhau.',
    tacnhan='%s; %s; Người dùng đã đăng nhập' % (ACTOR_KT, ACTOR_TQ),
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng nhập từ khoá vào ô tìm nhanh rồi bấm Tìm kiếm; hoặc bấm Tìm kiếm nâng '
          'cao rồi đặt điều kiện ở các ô lọc.\n'
          '2. Với ô tìm nhanh: hệ thống chờ thao tác bấm nút mới truy vấn.\n'
          '3. Với các ô lọc nâng cao: hệ thống truy vấn ngay khi giá trị thay đổi.\n'
          '4. Hệ thống áp bộ lọc BÊN TRONG phạm vi dữ liệu theo quyền, đưa về trang 1 và trả kết '
          'quả.\n'
          '5. Hệ thống lưu bộ lọc trong 10 phút để khôi phục khi quay lại màn.',
    phu='• Không kết quả → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Bấm Làm mới → xoá mọi điều kiện, về trang 1, phạm vi quyền giữ nguyên.\n'
        '• Người dùng không có V1 lẫn V2 → nhóm ô Công ty / Phòng ban / Bộ phận không được render.\n'
        '• Tham số lạ thêm vào đường dẫn không mở rộng được phạm vi dữ liệu.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('03-loc-nang-cao.png'),
         shot_caption='Khối Tìm kiếm nâng cao khi đang mở')
d.figure(shot('17-loc-dang-tao.png'),
         'Lọc Trạng thái = Đang tạo — chỉ ra nháp của chính người đăng nhập', width_in=6.2)

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Dòng gợi ý “Tìm theo mã phiếu...”. KHÔNG tự tìm khi gõ — phải bấm nút Tìm kiếm.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Áp giá trị ô tìm nhanh và đưa về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Xoá mọi điều kiện lọc và ô tìm nhanh, nạp lại danh sách trang 1.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đóng/mở khối ô lọc; đổi chữ thành “Ẩn tìm kiếm nâng cao” khi đang mở.'),
    ('Nhóm ô Công ty – Phòng ban – Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không',
     'Ẩn khi thiếu quyền',
     'Chỉ render khi người dùng có V1 hoặc V2. Lọc theo đơn vị ghi trên PHIẾU ĐỀ NGHỊ.'),
    ('Ô lọc Mã phiếu đề nghị thu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tự lọc ngay khi đổi giá trị.'),
    ('Ô lọc Loại thu', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
     'Chỉ cho chọn “Thu bán hàng” và “Thu nhà cung cấp”; giá trị “Thu khác” không còn cho chọn '
     'nhưng phiếu cũ vẫn hiện đúng tên.'),
    ('Ô lọc Trạng thái', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống',
     'Chọn “Đang tạo” chỉ ra nháp của chính người dùng.'),
    ('Ô lọc Người lập', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu thu.'),
    ('Ô lọc Người đề nghị', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu đề nghị.'),
    ('Ô lọc Khách hàng', 'Dropdown', 'Enable', 'Danh sách tìm từ xa', 'Không', 'Trống',
     'Phải gõ từ 2 ký tự trở lên mới hiện gợi ý. Nguồn dữ liệu là danh mục khách hàng dùng chung '
     'với phiếu đề nghị.'),
    ('Ô lọc Số hợp đồng/đơn hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Lọc phiếu có ít nhất một dòng chi tiết gắn hợp đồng khớp.'),
    ('Ô lọc Số tiền từ / Số tiền đến', 'Number', 'Enable', '≥ 0', 'Không', 'Trống',
     'So theo cột “Số tiền” của lưới, tức tổng số tiền duyệt thu.'),
    ('Ô lọc Ngày lập từ / Ngày lập đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc theo ngày lập phiếu thu; cả hai mốc lấy trọn ngày.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Gõ vào ô tìm nhanh', 'Keypress',
     'During:\n– Chỉ ghi nhận giá trị, KHÔNG truy vấn.\n'
     'After:\n– Danh sách giữ nguyên cho tới khi bấm nút Tìm kiếm.'),
    ('Bấm nút Tìm kiếm', 'Click',
     'After:\n– Đưa về trang 1 và nạp lại danh sách theo mã phiếu khớp từ khoá.'),
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'During:\n– Cộng dồn với các điều kiện đang có (quan hệ VÀ).\n'
     '– Ba ô đơn vị tổ chức và ô Loại thu lọc xuyên quan hệ sang phiếu đề nghị.\n'
     'After:\n– Đưa về trang 1, nạp lại danh sách, lưu bộ lọc trong 10 phút.'),
    ('Bấm nút Làm mới', 'Click',
     'After:\n– Đưa mọi ô lọc và ô tìm nhanh về trống, về trang 1, nạp lại danh sách. Phạm vi dữ '
     'liệu theo quyền không thay đổi.'),
])

# ------------------------------------------------------ 2.3 FR-03
d.h3('2.3 Tuỳ chỉnh bộ lọc và cột hiển thị')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Tuỳ chỉnh bộ lọc và cột hiển thị', 'view',
            [('extend', 'Ẩn / hiện ô lọc'),
             ('extend', 'Ẩn / hiện và đổi thứ tự cột')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-03 Tuỳ chỉnh bộ lọc và cột hiển thị')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Phiếu thu tiền '
           'tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh bộ lọc và cột hiển thị',
    mota='Cho phép mỗi người dùng tự chọn những ô lọc và những cột muốn nhìn thấy, kèm thứ tự '
         'hiển thị. Cấu hình lưu riêng theo từng người và từng màn hình.',
    tacnhan='%s; %s' % (ACTOR_KT, ACTOR_TQ),
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc (hoặc nút cấu hình cột).\n'
          '2. Hệ thống mở cửa sổ với danh sách ô lọc (hoặc cột) kèm ô tích chọn.\n'
          '3. Người dùng bỏ tích mục không cần và kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống áp cấu hình ngay và ghi nhớ cho lần sau.',
    phu='• Bấm Khôi phục mặc định ở cửa sổ Cài đặt bộ lọc → đưa về đủ 10 nhóm ô theo thứ tự ban '
        'đầu.\n'
        '• Bấm Đóng → thoát mà không lưu thay đổi.\n'
        '• Ba cột STT, Mã phiếu và Hành động bị khoá, không bỏ tích được.',
    dacbiet='Dòng “Công ty – Phòng ban – Bộ phận” luôn có trong cửa sổ Cài đặt bộ lọc, nhưng nhóm '
            'ô đó chỉ render trên màn khi người dùng có quyền V1 hoặc V2.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột',
         note='Hai cửa sổ được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
         shot=shot('04-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('05-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột hiển thị', width_in=6.2)

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách ô lọc / cột', 'Table/Grid', 'Enable', 'Danh sách', 'Không',
     'Theo cấu hình đã lưu', 'Mỗi dòng có ô tích, tay cầm kéo thả và số thứ tự.'),
    ('Ô tích chọn', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình đã lưu',
     'Cột khoá (STT, Mã phiếu, Hành động) hiện biểu tượng ổ khoá và bị vô hiệu.'),
    ('Tay cầm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Kéo để đổi thứ tự hiển thị.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Ghi cấu hình theo từng người và từng màn hình, áp dụng ngay.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Chỉ có ở cửa sổ Cài đặt bộ lọc.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thoát không lưu thay đổi.'),
])

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc / nút cấu hình cột', 'Click',
     'After:\n– Mở cửa sổ tương ứng, nạp cấu hình đang lưu của người dùng.'),
    ('Bỏ tích một mục', 'Change',
     'During:\n– Mục bị khoá thì bỏ qua thao tác.\n'
     'After:\n– Đánh dấu mục sẽ bị ẩn sau khi lưu.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Ghi cấu hình, đóng cửa sổ, áp dụng ngay lên khối lọc hoặc lưới.'),
])

# ------------------------------------------------------ 2.4 FR-04
d.h3('2.4 Tạo mới phiếu thu')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới phiếu thu', 'crud',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Chọn phiếu đề nghị từ popup'),
             ('include', 'Sinh mã phiếu tự động'),
             ('extend', 'Gửi thông báo cho Thủ quỹ khi gửi duyệt')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-04 Tạo mới phiếu thu')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới phiếu thu',
    mota='Lập phiếu thu từ một phiếu đề nghị thu tiền đang chờ duyệt: chọn phiếu đề nghị, chốt '
         'tài khoản nợ, người nộp, tỷ giá và số tiền duyệt thu cho từng dòng, rồi lưu nháp hoặc '
         'gửi duyệt.',
    tacnhan='%s' % ACTOR_KT,
    dieukien='Người dùng có quyền Q1 (hoặc là quản trị hệ thống). Tồn tại ít nhất một phiếu đề '
             'nghị ở trạng thái Chờ KT duyệt và chưa có phiếu thu.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở màn Thêm phiếu thu tiền, chọn sẵn tài khoản nợ mặc định và điền tỷ giá '
          'bằng 1.\n'
          '3. Người dùng chọn phiếu đề nghị; hệ thống kéo về loại thu, loại tiền, người đề nghị, '
          'phòng ban, lý do thu và toàn bộ dòng chi tiết.\n'
          '4. Người dùng nhập Người nộp, chỉnh số tiền duyệt thu và ghi chú từng dòng nếu cần.\n'
          '5. Người dùng bấm Lưu (trạng thái Đang tạo) hoặc Lưu và gửi duyệt (trạng thái Chờ '
          'duyệt, có hộp xác nhận).\n'
          '6. Hệ thống khóa dòng phiếu đề nghị, kiểm tra chưa có phiếu thu nào, sinh mã tự động, '
          'ghi phiếu cùng các dòng chi tiết và tính tổng số tiền duyệt thu.\n'
          '7. Nếu gửi duyệt: phiếu đề nghị chuyển sang “Đã tạo phiếu thu” và hệ thống gửi thông '
          'báo cho mọi thủ quỹ cùng công ty với phiếu.\n'
          '8. Hệ thống ghi một dòng lịch sử tạo mới, hiển thị thông báo và quay về danh sách.',
    phu='• Thiếu quyền Q1 → từ chối với thông báo “Bạn không có quyền lập phiếu thu”.\n'
        '• Thiếu trường bắt buộc → báo lỗi đỏ ngay dưới từng ô, không đóng màn, giữ nguyên dữ '
        'liệu đã nhập kể cả bảng chi tiết.\n'
        '• Phiếu đề nghị đã có phiếu thu khác → báo “Đề nghị thu tiền đã lập phiếu thu tiền”.\n'
        '• Bấm nút lưu nhiều lần liên tiếp → chỉ tạo đúng một phiếu.\n'
        '• Bấm Quay lại khi đã nhập dở → hỏi xác nhận rời trang.',
    dacbiet='Lưu nháp KHÔNG gửi thông báo và KHÔNG đổi trạng thái phiếu đề nghị. Bảng chi tiết '
            'không thêm và không xóa dòng được — số dòng luôn đúng bằng số dòng của phiếu đề '
            'nghị. Nhóm cột “Số tiền thực thu” không xuất hiện ở màn này.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới',
         shot=shot('06-tao-moi.png'),
         shot_caption='Màn Thêm phiếu thu tiền khi vừa mở')
d.figure(shot('08-form-da-chon-de-nghi.png'),
         'Màn Thêm phiếu thu tiền sau khi chọn phiếu đề nghị — bảng Chi tiết đã nạp',
         width_in=6.2)

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Số phiếu đề nghị', 'Textbox', 'Read-only', '–', 'Có', 'Trống',
     'Bấm vào ô để mở cửa sổ chọn; dòng gợi ý “Nhấn vào đây để chọn phiếu đề nghị thu”. Thiếu thì '
     'báo “Bắt buộc nhập”.'),
    ('Tài khoản nợ', 'Dropdown', 'Enable', 'Danh sách tài khoản', 'Có',
     'Tài khoản tiền mặt mặc định',
     'Chỉ liệt kê tài khoản đang hoạt động và là tài khoản cấp cuối.'),
    ('Loại thu', 'Text', 'Read-only', 'Danh sách 3 giá trị', '–', 'Trống',
     'Tự điền theo phiếu đề nghị; dòng gợi ý “Theo phiếu đề nghị”.'),
    ('Người nộp', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
     'Thiếu thì báo “Bắt buộc nhập”.'),
    ('Loại tiền', 'Text', 'Read-only', '–', '–', 'Trống', 'Tự điền theo phiếu đề nghị.'),
    ('Tỷ giá (VND)', 'Number', 'Enable / Disable', '> 0', 'Có', '1',
     'Bị khóa khi loại tiền là VNĐ. Thiếu thì báo “Bắt buộc nhập”; không phải số thì báo “Phải là '
     'số”.'),
    ('Người đề nghị', 'Text', 'Read-only', '–', '–', 'Trống', 'Người lập phiếu đề nghị.'),
    ('Phòng ban', 'Text', 'Read-only', '–', '–', 'Trống', 'Phòng ban của người đề nghị.'),
    ('Lý do thu', 'Textarea', 'Read-only', '–', '–', 'Trống', 'Lý do ghi trên phiếu đề nghị.'),
    ('Cột Số tài khoản có', 'Dropdown', 'Enable', 'Danh sách tài khoản', 'Có',
     'Theo phiếu đề nghị', 'Thiếu thì báo “Bắt buộc nhập”.'),
    ('Cột Tên tài khoản', 'Text', 'Read-only', '–', '–', 'Theo tài khoản đã chọn', '–'),
    ('Cột Khách hàng / Nhà cung cấp', 'Text', 'Read-only', '–', '–', 'Theo phiếu đề nghị',
     'Tiêu đề cột đổi theo loại thu của phiếu đề nghị.'),
    ('Cột Số đơn hàng/Hợp đồng', 'Text', 'Read-only', '–', '–', 'Theo phiếu đề nghị', '–'),
    ('Cột Số tiền đề nghị thu', 'Number', 'Read-only', '≥ 0', '–', 'Theo phiếu đề nghị', '–'),
    ('Cột Số tiền duyệt thu', 'Number', 'Enable', '≥ 0', 'Có', 'Bằng số tiền đề nghị thu',
     'Thiếu thì báo “Bắt buộc nhập”; không phải số thì báo “Phải là số”.'),
    ('Cột Ghi chú của dòng', 'Textbox', 'Enable', '–', 'Không', 'Theo phiếu đề nghị', '–'),
    ('Dòng Tổng cộng', 'Label', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
     'Cộng dọc từng cột tiền, cập nhật tức thời.'),
    ('Ghi chú', 'Textarea', 'Enable', '0–1000 ký tự', 'Không', 'Trống',
     'Nằm ở khối riêng cuối trang.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Lưu ở trạng thái Đang tạo, KHÔNG hỏi xác nhận. Bị khoá trong lúc xử lý.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Mở hộp xác nhận trước khi lưu ở trạng thái Chờ duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi inline', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi; ô có viền đỏ.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'After:\n– Mở màn Thêm phiếu thu tiền với tài khoản nợ mặc định và tỷ giá bằng 1.'),
    ('Chọn phiếu đề nghị', 'Click',
     'Before:\n– Kiểm tra quyền Q1; không có quyền → từ chối với thông báo “Bạn không có quyền '
     'xem phiếu đề nghị thu”.\n'
     'After:\n– Kéo về loại thu, loại tiền, người đề nghị, phòng ban, lý do thu và toàn bộ dòng '
     'chi tiết.\n'
     '– Loại tiền khác VNĐ thì mở ô Tỷ giá và bổ sung cột nguyên tệ cho mỗi nhóm tiền.'),
    ('Đổi giá trị ô Số tiền duyệt thu', 'Change',
     'After:\n– Cập nhật dòng Tổng cộng; với phiếu ngoại tệ thì tính lại cột VND theo tỷ giá.'),
    ('Bấm Lưu / Lưu và gửi duyệt', 'Click',
     'Before:\n– Kiểm tra quyền Q1; không có quyền → hiển thị “Bạn không có quyền lập phiếu thu” '
     'và dừng xử lý.\n'
     '– Với Lưu và gửi duyệt: mở hộp xác nhận, chỉ tiếp tục khi người dùng đồng ý.\n'
     'During:\n'
     '– Chưa chọn phiếu đề nghị → hiển thị “Bắt buộc nhập”.\n'
     '– Chưa chọn Tài khoản nợ → hiển thị “Bắt buộc nhập”; tài khoản không tồn tại → “Không tồn '
     'tại”.\n'
     '– Chưa nhập Người nộp → hiển thị “Bắt buộc nhập”.\n'
     '– Chưa nhập Tỷ giá → hiển thị “Bắt buộc nhập”; không phải số → “Phải là số”; nhỏ hơn 0 → '
     'báo lỗi.\n'
     '– Bảng chi tiết rỗng → hiển thị “Bắt buộc nhập”.\n'
     '– Dòng thiếu Số tài khoản có → hiển thị “Bắt buộc nhập”.\n'
     '– Dòng thiếu Số tiền duyệt thu → hiển thị “Bắt buộc nhập”; không phải số → “Phải là số”.\n'
     '– Ghi chú vượt 1.000 ký tự → báo lỗi.\n'
     '– Nếu có lỗi thì KHÔNG thực hiện bước After.\n'
     'After:\n– Khóa dòng phiếu đề nghị rồi kiểm tra chưa có phiếu thu nào; đã có thì hiển thị '
     '“Đề nghị thu tiền đã lập phiếu thu tiền” và dừng.\n'
     '– Sinh mã phiếu tự động (có khóa dòng để hai người lưu cùng lúc không trùng mã), ghi phiếu '
     'và các dòng chi tiết, tính tổng số tiền duyệt thu.\n'
     '– Ghi công ty / phòng ban / bộ phận theo hồ sơ người lập.\n'
     '– Nếu trạng thái là Chờ duyệt: cập nhật phiếu đề nghị sang “Đã tạo phiếu thu”, ghi một dòng '
     'lịch sử cho phiếu đề nghị và gửi thông báo tới mọi thủ quỹ cùng công ty.\n'
     '– Ghi một dòng lịch sử tạo mới cho phiếu thu.\n'
     '– Hiển thị thông báo “Thêm phiếu thu tiền thành công!” (lưu nháp) hoặc “Phiếu thu tiền tạo '
     'thành công! Phiếu thu tiền cần được duyệt trước khi có hiệu lực, vui lòng theo dõi thông '
     'báo” (gửi duyệt), rồi quay về danh sách.'),
])

# ------------------------------------------------------ 2.5 FR-05
d.h3('2.5 Chọn phiếu đề nghị từ popup')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chọn phiếu đề nghị từ popup', 'crud',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Lọc phiếu Chờ KT duyệt và chưa có phiếu thu')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-05 Chọn phiếu đề nghị từ popup')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Phiếu '
           'thu tiền tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Chọn phiếu đề nghị thu tiền',
    mota='Cửa sổ tìm và chọn MỘT phiếu đề nghị thu tiền để lập phiếu thu. Chỉ liệt kê phiếu đủ '
         'điều kiện lập phiếu thu.',
    tacnhan='%s' % ACTOR_KT,
    dieukien='Đang ở màn Tạo mới hoặc màn Sửa phiếu thu; người dùng có quyền Q1.',
    chinh='1. Người dùng bấm vào ô “Số phiếu đề nghị”.\n'
          '2. Hệ thống kiểm tra quyền Q1 rồi mở cửa sổ, liệt kê phiếu đề nghị đang ở trạng thái '
          'Chờ KT duyệt VÀ chưa có phiếu thu nào, sắp xếp mới nhất trước.\n'
          '3. Người dùng tìm theo mã phiếu đề nghị hoặc theo người lập.\n'
          '4. Người dùng bấm vào dòng cần chọn.\n'
          '5. Cửa sổ tự đóng, hệ thống kéo dữ liệu phiếu đề nghị về form.',
    phu='• Thiếu quyền Q1 → từ chối với thông báo “Bạn không có quyền xem danh sách phiếu đề nghị '
        'thu”.\n'
        '• Không tìm thấy phiếu nào → danh sách rỗng, không báo lỗi.\n'
        '• Bấm Đóng → cửa sổ đóng, ô Số phiếu đề nghị giữ nguyên giá trị cũ.',
    dacbiet='Cửa sổ này CỐ Ý không áp phạm vi xem của màn Phiếu đề nghị thu tiền — mọi kế toán '
            'thanh toán đều chọn được mọi phiếu đề nghị đủ điều kiện. Vì vậy endpoint kéo dữ liệu '
            'phiếu đề nghị về form cũng gate bằng đúng quyền Q1, không gate bằng quyền xem của '
            'màn đề nghị.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới / Sửa => Chọn phiếu đề nghị thu',
         note='Cửa sổ được mở ngay trên màn Tạo mới hoặc màn Sửa phiếu thu.',
         shot=shot('07-popup-chon-de-nghi.png'),
         shot_caption='Cửa sổ Chọn phiếu đề nghị thu')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Không', 'Chọn phiếu đề nghị thu',
     'Phụ đề màu đỏ ghi “Chỉ phiếu Chờ duyệt và chưa lập phiếu thu”.'),
    ('Ô Mã phiếu đề nghị', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm gần đúng theo mã.'),
    ('Ô Người lập', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu đề nghị.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp các điều kiện đã nhập.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá điều kiện tìm.'),
    ('Bảng danh sách', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu',
     'Ba cột: STT, Mã phiếu đề nghị, Người lập. Bấm vào dòng để chọn.'),
    ('Phân trang của cửa sổ', 'Pagination', 'Enable', '–', '–', 'Trang 1, cỡ 10', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không chọn gì.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm vào ô Số phiếu đề nghị', 'Click',
     'Before:\n– Kiểm tra quyền Q1; thiếu quyền → hiển thị “Bạn không có quyền xem danh sách '
     'phiếu đề nghị thu” và không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ và nạp danh sách phiếu đề nghị đủ điều kiện.'),
    ('Bấm vào một dòng phiếu đề nghị', 'Click',
     'Before:\n– Kiểm tra quyền Q1 một lần nữa ở endpoint kéo dữ liệu.\n'
     'After:\n– Điền mã phiếu đề nghị vào ô; kéo về loại thu, loại tiền, người đề nghị, phòng '
     'ban, lý do thu và toàn bộ dòng chi tiết.\n'
     '– Tự đóng cửa sổ.'),
])

# ------------------------------------------------------ 2.6 FR-06
d.h3('2.6 Sửa phiếu thu')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Sửa phiếu thu', 'crud',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Kiểm tra trạng thái Đang tạo'),
             ('include', 'Chọn phiếu đề nghị từ popup')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-06 Sửa phiếu thu')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Sửa phiếu thu',
    mota='Cập nhật nội dung của một phiếu thu đang ở trạng thái Đang tạo. Có thể lưu tiếp ở dạng '
         'nháp hoặc gửi duyệt luôn.',
    tacnhan='%s' % ACTOR_KT,
    dieukien='Phiếu ở trạng thái Đang tạo VÀ người dùng có quyền Q1.',
    chinh='1. Người dùng bấm nút Sửa trên dòng danh sách hoặc trên màn chi tiết.\n'
          '2. Hệ thống kiểm tra quyền và trạng thái; không thoả thì từ chối.\n'
          '3. Hệ thống mở màn Sửa, nạp đầy đủ thông tin chung và bảng chi tiết đã lưu.\n'
          '4. Người dùng chỉnh sửa rồi bấm Lưu hoặc Lưu và gửi duyệt.\n'
          '5. Hệ thống áp lại toàn bộ quy tắc kiểm tra như màn Tạo mới, ghi lại phiếu, xoá và tạo '
          'lại toàn bộ dòng chi tiết, tính lại tổng số tiền duyệt thu.\n'
          '6. Hệ thống ghi một dòng lịch sử chỉnh sửa và một dòng lịch sử đổi trạng thái nếu '
          'trạng thái thay đổi.',
    phu='• Phiếu không còn ở trạng thái Đang tạo → từ chối với thông báo “Phiếu thu đã gửi duyệt '
        'hoặc đã duyệt, không sửa được”.\n'
        '• Thiếu quyền Q1 → từ chối với thông báo “Bạn không có quyền sửa phiếu thu”.\n'
        '• Đổi sang phiếu đề nghị khác → bảng chi tiết nạp lại theo phiếu mới, dòng cũ bị thay '
        'hết; ràng buộc “một phiếu đề nghị một phiếu thu” vẫn được kiểm, bỏ qua chính phiếu đang '
        'sửa.\n'
        '• Bấm Quay lại khi đã sửa dở → hỏi xác nhận rời trang.',
    dacbiet='Màn Sửa có THÊM hai ô chỉ đọc so với màn Tạo mới: “Mã phiếu” và “Người tạo”. Người '
            'tạo giữ nguyên người lập gốc, không đổi sang người đang sửa. Tài khoản đang gắn với '
            'phiếu mà đã bị khóa trong danh mục vẫn hiện đúng tên, tránh việc lưu đè mất giá trị '
            'cũ.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa',
         shot=shot('21-sua-phieu.png'),
         shot_caption='Màn Sửa phiếu thu tiền với dữ liệu đã lưu')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', '–', 'Sửa phiếu thu tiền',
     'Khác màn Tạo mới ghi “Thêm phiếu thu tiền”.'),
    ('Mã phiếu', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Chỉ có ở màn Sửa và màn Xem chi tiết.'),
    ('Người tạo', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Người lập gốc, không đổi sang người đang sửa.'),
    ('Số phiếu đề nghị', 'Textbox', 'Read-only', '–', 'Có', 'Theo dữ liệu',
     'Bấm vào ô để đổi sang phiếu đề nghị khác.'),
    ('Các ô còn lại của Thông tin chung', 'Textbox / Dropdown', 'Enable', '–', 'Theo từng ô',
     'Theo dữ liệu', 'Quy tắc giống màn Tạo mới.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', 'Có', 'Theo dữ liệu',
     'Sửa được Số tài khoản có, Số tiền duyệt thu và Ghi chú từng dòng. KHÔNG có nhóm cột Số tiền '
     'thực thu.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Giữ phiếu ở Đang tạo.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Có hộp xác nhận; chuyển phiếu sang Chờ duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu ở trạng thái Đang tạo.\n'
     '– Kiểm tra lại ở phía máy chủ; không thoả → hiển thị “Phiếu thu đã gửi duyệt hoặc đã duyệt, '
     'không sửa được” và đưa về danh sách.\n'
     'After:\n– Mở màn Sửa và nạp dữ liệu đã lưu, kèm tài khoản đã khóa (nếu có) để select không '
     'bị rỗng.'),
    ('Bấm Lưu / Lưu và gửi duyệt', 'Click',
     'Before:\n– Kiểm tra quyền Q1; thiếu quyền → hiển thị “Bạn không có quyền sửa phiếu thu”.\n'
     '– Kiểm tra lại trạng thái Đang tạo.\n'
     'During:\n– Áp toàn bộ quy tắc kiểm tra như màn Tạo mới.\n'
     '– Khóa dòng phiếu đề nghị và kiểm tra ràng buộc một phiếu đề nghị một phiếu thu, bỏ qua '
     'chính phiếu đang sửa.\n'
     '– Nếu có lỗi thì KHÔNG thực hiện bước After.\n'
     'After:\n– Chụp lại nội dung cũ trước khi ghi để lấy được phần chênh lệch.\n'
     '– Xoá và tạo lại toàn bộ dòng chi tiết, ghi lại phiếu, tính lại tổng số tiền duyệt thu, '
     'cập nhật người sửa gần nhất.\n'
     '– Nếu chuyển sang Chờ duyệt: cập nhật phiếu đề nghị sang “Đã tạo phiếu thu” và gửi thông '
     'báo cho thủ quỹ cùng công ty.\n'
     '– Ghi một dòng lịch sử chỉnh sửa; nếu trạng thái đổi thì ghi thêm một dòng lịch sử đổi '
     'trạng thái bằng TÊN trạng thái.\n'
     '– Hiển thị “Cập nhật phiếu thu tiền thành công!” và quay về danh sách.'),
])

# ------------------------------------------------------ 2.7 FR-07
d.h3('2.7 Xem chi tiết phiếu thu')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Phiếu thu '
           'tiền tại phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu thu',
    mota='Hiển thị toàn bộ nội dung một phiếu thu ở chế độ chỉ đọc, kèm khối Lịch sử và bộ nút '
         'thao tác phù hợp với trạng thái và quyền của người xem. Đây cũng là màn thủ quỹ nhập số '
         'tiền thực thu trước khi duyệt.',
    tacnhan='%s; %s' % (ACTOR_KT, ACTOR_TQ),
    dieukien='Người xem là người lập phiếu, hoặc là người đã duyệt phiếu, hoặc là quản trị hệ '
             'thống, hoặc có quyền V1, hoặc có quyền V2 và cùng công ty với phiếu.',
    chinh='1. Người dùng bấm vào mã phiếu trên danh sách (hoặc mở từ thông báo).\n'
          '2. Hệ thống nạp phiếu kèm dòng chi tiết, khách hàng, nhà cung cấp, hợp đồng, phiếu đề '
          'nghị và người liên quan.\n'
          '3. Hệ thống kiểm tra quyền xem phiếu.\n'
          '4. Hệ thống hiển thị nội dung và tính các cờ quyết định nút Sửa, Duyệt, Hủy, Xóa.',
    phu='• Không đủ quyền xem → từ chối với thông báo “Bạn không có quyền xem phiếu thu này”.\n'
        '• Mã phiếu không tồn tại → báo không tìm thấy dữ liệu.\n'
        '• Phiếu Đang tạo của người khác → không xem được (quyền theo cấp không mở phiếu nháp của '
        'người khác).\n'
        '• Hợp đồng đã bị xoá hoặc thuộc loại không nhận diện được → dòng đó hiện dấu gạch ngang, '
        'KHÔNG làm vỡ cả màn.',
    dacbiet=None)

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết',
         shot=shot('11-chi-tiet-cho-duyet.png'),
         shot_caption='Màn chi tiết phiếu Chờ duyệt, xem bằng tài khoản thủ quỹ')
d.figure(shot('16-chi-tiet-da-duyet.png'),
         'Màn chi tiết phiếu Đã duyệt — chỉ còn In, Xuất Excel, Quay lại', width_in=6.2)

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu thu tiền: {mã phiếu}', '–'),
    ('Khối Thông tin chung', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm Số phiếu đề nghị, Mã phiếu, Tài khoản nợ, Loại thu, Người nộp, Loại tiền, Tỷ giá (VND), '
     'Người đề nghị, Phòng ban, Người tạo, Lý do thu.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Có THÊM nhóm cột “Số tiền thực thu” so với màn Tạo mới và màn Sửa.'),
    ('Cột Số tiền thực thu', 'Number', 'Enable / Read-only', '0 – số tiền duyệt thu của dòng',
     'Ẩn khi thiếu quyền',
     'Là ô nhập khi người xem là thủ quỹ VÀ phiếu ở Chờ duyệt; các trường hợp còn lại chỉ hiển thị.'),
    ('Khối Số tiền phân bổ', 'Number', 'Enable / Ẩn', '≥ 0', 'Ẩn khi thiếu quyền',
     'Cùng điều kiện hiện với ô nhập Số tiền thực thu.'),
    ('Nút Phân bổ', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Rải số tiền vừa nhập xuống cột Số tiền thực thu; chỉ điền vào ô, không gọi lưu.'),
    ('Dòng Tổng cộng', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu', 'Cộng dọc từng cột tiền.'),
    ('Khối Ghi chú', 'Textarea', 'Read-only', '0–1000 ký tự', 'Theo dữ liệu',
     'Với phiếu đã hủy, đây là nơi hiển thị lý do hủy.'),
    ('Khối Lịch sử', 'Table/Grid', 'Hiển thị', '–', 'Thu gọn',
     'Kèm số đếm số mốc; bấm “Xem lịch sử” để bung ra.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu Đang tạo.'),
    ('Nút Duyệt phiếu thu', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu Chờ duyệt và người xem có quyền Q2.'),
    ('Nút Hủy phiếu thu', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Cùng điều kiện với nút Duyệt phiếu thu.'),
    ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Ẩn với loại thu “Thu khác”', '–'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Luôn hiện với phiếu xem được.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu Đang tạo.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị',
     'Về danh sách, giữ nguyên bộ lọc đã lưu.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Nạp phiếu kèm dòng chi tiết, đối tượng thu, hợp đồng, phiếu đề nghị và người '
     'liên quan.\n'
     '– Kiểm tra quyền xem: là người lập, hoặc là người đã duyệt, hoặc là quản trị hệ thống, hoặc '
     'có V1, hoặc có V2 và cùng công ty. Phiếu Đang tạo của người khác luôn bị chặn.\n'
     '– Không đủ quyền → hiển thị “Bạn không có quyền xem phiếu thu này”.\n'
     'During:\n– Hợp đồng không resolve được → trả về rỗng cho dòng đó và ghi log cảnh báo, '
     'không làm vỡ cả màn.\n'
     'After:\n– Hiển thị nội dung và tính các cờ Sửa / Xóa / Duyệt.'),
    ('Bấm nút Phân bổ', 'Click',
     'During:\n– Duyệt lần lượt từng dòng theo thứ tự: mỗi dòng nhận tối đa bằng số tiền duyệt '
     'thu của nó, phần còn lại chuyển sang dòng sau; hết tiền thì các dòng còn lại nhận 0.\n'
     'After:\n– Điền kết quả vào cột Số tiền thực thu; KHÔNG gọi lưu, người dùng vẫn sửa tay '
     'từng ô được.'),
    ('Gõ vào ô Số tiền thực thu', 'Change',
     'During:\n– Vượt số tiền duyệt thu của chính dòng đó → hiển thị “Không được lớn hơn số tiền '
     'duyệt thu ({số duyệt thu})” dưới ô và đánh dấu ô lỗi.\n'
     'After:\n– Nút Duyệt bị chặn cho tới khi mọi ô hợp lệ.'),
])

# ------------------------------------------------------ 2.8 FR-08
d.h3('2.8 Duyệt phiếu thu')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Duyệt phiếu thu', 'action',
            [('include', 'Kiểm tra quyền Thủ quỹ và trạng thái Chờ duyệt'),
             ('include', 'Ghi bút toán vào sổ kế toán'),
             ('include', 'Đồng bộ số thực thu về phiếu đề nghị'),
             ('extend', 'Chặn duyệt lại bằng khóa dòng')],
            actor=ACTOR_TQ,
            caption='Biểu đồ Use Case — FR-08 Duyệt phiếu thu')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Thông báo và Validate dữ liệu. Chỉ bổ sung các quy tắc riêng của màn Phiếu thu tiền '
           'tại phần mô tả chi tiết.', anchor='notice')
d.intro_table(
    ten='Duyệt phiếu thu',
    mota='Thủ quỹ xác nhận số tiền thực nhận cho từng dòng và duyệt phiếu. Đây là THỜI ĐIỂM DUY '
         'NHẤT hệ thống ghi bút toán vào sổ kế toán dùng chung, đồng thời cập nhật số thực thu '
         'ngược về phiếu đề nghị.',
    tacnhan='%s' % ACTOR_TQ,
    dieukien='Người dùng có quyền Q2 (hoặc là quản trị hệ thống) VÀ phiếu đang ở trạng thái Chờ '
             'duyệt.',
    chinh='1. Thủ quỹ mở màn chi tiết phiếu đang Chờ duyệt.\n'
          '2. Thủ quỹ nhập số tiền thực thu cho từng dòng, hoặc dùng nút Phân bổ để điền hộ.\n'
          '3. Thủ quỹ bấm nút Duyệt phiếu thu.\n'
          '4. Hệ thống khóa dòng phiếu, kiểm tra lại quyền rồi kiểm tra lại trạng thái.\n'
          '5. Hệ thống ghi số thực thu vào từng dòng chi tiết.\n'
          '6. Hệ thống chuyển phiếu sang Đã duyệt, ghi ngày hạch toán và người duyệt.\n'
          '7. Hệ thống chuyển phiếu đề nghị sang “Đã hạch toán” và ghi một dòng lịch sử cho phiếu '
          'đề nghị.\n'
          '8. Hệ thống dựng và ghi bút toán vào sổ kế toán, rồi đẩy số thực thu ngược về các dòng '
          'của phiếu đề nghị.\n'
          '9. Hệ thống ghi hai dòng lịch sử cho phiếu thu và quay về màn danh sách.',
    phu='• Thiếu quyền Q2 → từ chối với thông báo “Bạn không có quyền duyệt phiếu thu”.\n'
        '• Phiếu không còn ở trạng thái Chờ duyệt (người khác vừa duyệt hoặc hủy) → từ chối với '
        'thông báo “Phiếu thu tiền đã được duyệt!”.\n'
        '• Số thực thu vượt số duyệt thu của dòng → hiển thị “Không được lớn hơn số tiền duyệt '
        'thu”, không duyệt.\n'
        '• Số thực thu âm → hiển thị “Không được âm”.\n'
        '• Bấm nút nhiều lần liên tiếp → chỉ ghi nhận một lần.\n'
        '• Toàn bộ bước 5–8 nằm trong một giao dịch: hoặc thành công trọn vẹn, hoặc không đổi gì.',
    dacbiet='Thao tác này KHÔNG HOÀN TÁC ĐƯỢC — không có chức năng gỡ bút toán hay bỏ duyệt. '
            'Dòng có số thực thu bằng 0 KHÔNG sinh bút toán. Hệ thống CỐ Ý không tính lại cột '
            '“Số tiền” của màn danh sách sau khi duyệt — xem quy tắc BR-08.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Duyệt phiếu thu',
         note='Ô nhập số tiền thực thu và nút Duyệt nằm ngay trên màn chi tiết, không có cửa sổ '
              'riêng.',
         shot=shot('11-chi-tiet-cho-duyet.png'),
         shot_caption='Màn chi tiết phiếu Chờ duyệt — ô nhập Số tiền thực thu, khối Phân bổ và '
                      'nút Duyệt phiếu thu')
d.figure(shot('14-loi-thuc-thu-vuot.png'),
         'Lỗi khi gõ số thực thu lớn hơn số tiền duyệt thu của dòng', width_in=6.2)

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô Số tiền phân bổ', 'Number', 'Enable / Ẩn', '≥ 0', 'Không', '0',
     'Nhập tổng số tiền thực nhận. Gợi ý ghi kèm tên loại tiền của phiếu.'),
    ('Nút Phân bổ', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi thiếu quyền',
     'Rải số tiền xuống cột Số tiền thực thu theo thứ tự từ trên xuống.'),
    ('Ô Số tiền thực thu của từng dòng', 'Number', 'Enable / Ẩn',
     '0 – số tiền duyệt thu của dòng', 'Có', 'Theo dữ liệu',
     'Vượt trần thì hiển thị lỗi dưới ô và chặn duyệt; không tự kéo số về như hệ thống cũ.'),
    ('Nút Duyệt phiếu thu', 'Button', 'Enable / Disable', '–', '–', 'Ẩn khi thiếu quyền',
     'Bị khoá trong lúc đang xử lý để chống bấm nhiều lần.'),
    ('Thông báo lỗi inline', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô Số tiền thực thu bị lỗi.'),
])

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Duyệt phiếu thu', 'Click',
     'Before:\n– Chống bấm nhiều lần: bỏ qua nếu đang có một lần xử lý chưa xong.\n'
     '– Kiểm tra ở giao diện: mọi ô Số tiền thực thu phải hợp lệ, nếu không thì dừng ngay.\n'
     '– Khóa dòng phiếu ở phía máy chủ rồi mới đọc trạng thái.\n'
     '– Không có quyền Q2 → hiển thị “Bạn không có quyền duyệt phiếu thu” và dừng xử lý.\n'
     '– Phiếu không còn ở Chờ duyệt → hiển thị “Phiếu thu tiền đã được duyệt!” và dừng xử lý.\n'
     'During:\n– Số thực thu của một dòng vượt số duyệt thu của chính dòng đó → hiển thị “Không '
     'được lớn hơn số tiền duyệt thu” và dừng.\n'
     '– Số thực thu âm → hiển thị “Không được âm”; không phải số → “Phải là số”.\n'
     '– Ngày hạch toán sai định dạng → hiển thị “Sai định dạng ngày (dd/mm/yyyy)”.\n'
     '– Nếu có lỗi thì KHÔNG thực hiện bước After.\n'
     'After:\n– Chụp lại nội dung phiếu trước khi ghi.\n'
     '– Ghi số thực thu vào từng dòng chi tiết.\n'
     '– Chuyển phiếu sang Đã duyệt, ghi ngày hạch toán (mặc định là hôm nay) và người duyệt.\n'
     '– Chuyển phiếu đề nghị sang “Đã hạch toán” và ghi một dòng lịch sử cho phiếu đề nghị.\n'
     '– Dựng và ghi bút toán vào sổ kế toán cho từng dòng có số thực thu lớn hơn 0.\n'
     '– Đẩy số thực thu ngược về các dòng tương ứng của phiếu đề nghị.\n'
     '– KHÔNG tính lại tổng số tiền của phiếu (xem BR-08).\n'
     '– Ghi hai dòng lịch sử: một dòng thay đổi thông tin (số thực thu từng dòng, ngày hạch '
     'toán), một dòng đổi trạng thái kèm ghi chú đã ghi bút toán.\n'
     '– Hiển thị “Duyệt phiếu thu thành công!” và quay về danh sách.'),
])

# ------------------------------------------------------ 2.9 FR-09
d.h3('2.9 Hủy phiếu thu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Hủy phiếu thu', 'action',
            [('include', 'Kiểm tra quyền Thủ quỹ và trạng thái Chờ duyệt'),
             ('include', 'Nhập lý do hủy'),
             ('extend', 'Chuyển phiếu đề nghị sang Hủy')],
            actor=ACTOR_TQ,
            caption='Biểu đồ Use Case — FR-09 Hủy phiếu thu')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa, Validate dữ liệu. Chỉ bổ sung các quy tắc riêng của màn '
           'Phiếu thu tiền tại phần mô tả chi tiết.', anchor='notice')
d.intro_table(
    ten='Hủy phiếu thu',
    mota='Thủ quỹ từ chối khoản thu kèm lý do. Phiếu thu và phiếu đề nghị tương ứng cùng chuyển '
         'sang trạng thái Hủy; KHÔNG ghi bút toán nào.',
    tacnhan='%s' % ACTOR_TQ,
    dieukien='Người dùng có quyền Q2 (hoặc là quản trị hệ thống) VÀ phiếu đang ở trạng thái Chờ '
             'duyệt.',
    chinh='1. Thủ quỹ mở màn chi tiết phiếu đang Chờ duyệt.\n'
          '2. Thủ quỹ bấm nút Hủy phiếu thu; hệ thống mở cửa sổ nhập lý do.\n'
          '3. Thủ quỹ nhập lý do hủy và bấm Xác nhận.\n'
          '4. Hệ thống khóa dòng phiếu, kiểm tra lại quyền và trạng thái.\n'
          '5. Hệ thống chuyển phiếu sang Hủy và ghi lý do vào ô Ghi chú của phiếu.\n'
          '6. Hệ thống chuyển phiếu đề nghị sang Hủy và ghi một dòng lịch sử kèm lý do cho phiếu '
          'đề nghị.\n'
          '7. Hệ thống ghi một dòng lịch sử đổi trạng thái kèm lý do cho phiếu thu.',
    phu='• Lý do hủy để trống → hiển thị “Bắt buộc nhập lý do hủy”; cửa sổ không đóng.\n'
        '• Lý do hủy vượt 1.000 ký tự → hiển thị “Tối đa 1000 ký tự”.\n'
        '• Thiếu quyền Q2 → từ chối với thông báo “Bạn không có quyền hủy phiếu thu”.\n'
        '• Phiếu không còn ở Chờ duyệt → từ chối với thông báo “Phiếu thu tiền đã được duyệt!”.\n'
        '• Bấm Đóng → cửa sổ đóng, phiếu giữ nguyên trạng thái.',
    dacbiet='Hủy phiếu thu là NGÕ CỤT theo thiết kế: phiếu đề nghị chuyển sang Hủy và KHÔNG lập '
            'lại được phiếu thu khác cho phiếu đề nghị đó, vì ràng buộc “một phiếu đề nghị một '
            'phiếu thu” không loại trừ phiếu thu đã hủy. Đây là hành vi kế thừa có chủ đích, '
            'không phải lỗi.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Hủy phiếu thu',
         note='Cửa sổ nhập lý do hủy được mở ngay trên màn chi tiết.',
         shot=shot('12-popup-huy-phieu.png'),
         shot_caption='Cửa sổ Hủy phiếu thu tiền')
d.figure(shot('13-loi-ly-do-huy.png'),
         'Lỗi khi bấm Xác nhận lúc chưa nhập lý do hủy', width_in=6.2)

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Hủy phiếu thu tiền',
     'Phụ đề ghi “Phiếu thu: {mã phiếu}”; biểu tượng và viền màu đỏ.'),
    ('Ô Lý do hủy', 'Textarea', 'Enable', 'Trống',
     'Có dấu sao đỏ, bắt buộc, tối đa 1.000 ký tự. Gợi ý “Nhập lý do hủy phiếu thu”.'),
    ('Lỗi inline của Lý do hủy', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     'Chữ đỏ ngay dưới ô; tự mất khi người dùng gõ nội dung.'),
    ('Nút Xác nhận', 'Button', 'Enable / Disable', 'Hiển thị',
     'Bị khoá trong lúc đang xử lý để chống bấm nhiều lần.'),
    ('Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ, không hủy phiếu.'),
], required=False, scope=False)

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Hủy phiếu thu', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu ở Chờ duyệt và người xem có quyền Q2.\n'
     'After:\n– Mở cửa sổ nhập lý do hủy, xoá lỗi cũ (nếu có).'),
    ('Bấm Xác nhận trong cửa sổ hủy', 'Click',
     'Before:\n– Chống bấm nhiều lần: bỏ qua nếu đang có một lần xử lý chưa xong.\n'
     '– Khóa dòng phiếu rồi kiểm tra lại quyền Q2 và trạng thái Chờ duyệt; không thoả → hiển thị '
     '“Bạn không có quyền hủy phiếu thu” hoặc “Phiếu thu tiền đã được duyệt!” và dừng xử lý.\n'
     'During:\n– Lý do hủy trống → hiển thị “Bắt buộc nhập lý do hủy”.\n'
     '– Lý do hủy vượt 1.000 ký tự → hiển thị “Tối đa 1000 ký tự”.\n'
     '– Nếu có lỗi thì KHÔNG thực hiện bước After.\n'
     'After:\n– Chuyển phiếu sang Hủy và ghi lý do vào ô Ghi chú của phiếu.\n'
     '– Ghi một dòng lịch sử đổi trạng thái cho phiếu thu, kèm lý do hủy.\n'
     '– Chuyển phiếu đề nghị sang Hủy và ghi một dòng lịch sử kèm lý do cho phiếu đề nghị.\n'
     '– KHÔNG ghi bút toán nào vào sổ kế toán.\n'
     '– Hiển thị “Hủy phiếu thu thành công!”.'),
])

# ------------------------------------------------------ 2.10 FR-10
d.h3('2.10 Xóa phiếu thu')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu thu', 'action',
            [('include', 'Kiểm tra trạng thái Đang tạo và đúng người lập'),
             ('include', 'Xoá kèm toàn bộ dòng chi tiết')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu thu')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Chỉ bổ sung các quy tắc riêng của màn Phiếu thu tiền tại '
           'phần mô tả chi tiết.', anchor='notice')
d.intro_table(
    ten='Xóa phiếu thu',
    mota='Xoá vĩnh viễn một phiếu thu đang ở trạng thái Đang tạo do chính người đăng nhập lập, '
         'kèm toàn bộ dòng chi tiết.',
    tacnhan='%s (người lập chính phiếu đó)' % ACTOR_KT,
    dieukien='Phiếu ở trạng thái Đang tạo VÀ do chính người đăng nhập lập (hoặc người dùng là '
             'quản trị hệ thống).',
    chinh='1. Người dùng bấm nút Xóa trên dòng danh sách hoặc trên màn chi tiết.\n'
          '2. Hệ thống mở hộp xác nhận nêu rõ mã phiếu.\n'
          '3. Người dùng bấm Xóa để xác nhận.\n'
          '4. Hệ thống kiểm tra lại trạng thái và người lập, chụp lại nội dung phiếu rồi xoá '
          'phiếu cùng toàn bộ dòng chi tiết trong một giao dịch.\n'
          '5. Hệ thống ghi một dòng lịch sử xoá, hiển thị thông báo và nạp lại danh sách.',
    phu='• Phiếu không còn ở Đang tạo → từ chối với thông báo “Phiếu thu đã gửi duyệt hoặc đã '
        'duyệt, không xóa được”.\n'
        '• Không phải người lập và không phải quản trị hệ thống → từ chối với thông báo “Bạn '
        'không có quyền xóa phiếu thu này”.\n'
        '• Bấm Hủy ở hộp xác nhận → không xoá gì.',
    dacbiet='Xoá phiếu thu KHÔNG trả trạng thái phiếu đề nghị về — an toàn vì phiếu nháp chưa hề '
            'đụng tới phiếu đề nghị (phiếu đề nghị vẫn ở Chờ KT duyệt). Sau khi xoá, phiếu đề '
            'nghị đó xuất hiện lại trong cửa sổ chọn và lập được phiếu thu mới. Đây là xoá thật, '
            'không khôi phục lại được; mã phiếu đã dùng không được cấp lại.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa',
         note='Hộp xác nhận xoá được mở ngay trên màn danh sách hoặc màn chi tiết.',
         shot=shot('22-xac-nhan-xoa.png'),
         shot_caption='Hộp xác nhận xoá phiếu thu')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Cố định.'),
    ('Nội dung hộp thoại', 'Label', 'Hiển thị',
     'Bạn có chắc muốn xóa phiếu thu tiền "{mã phiếu}"?', 'Có nêu rõ mã phiếu sẽ bị xoá.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xoá.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xoá.'),
    ('Nút Xóa trên dòng danh sách', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu Đang tạo.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu ở trạng thái Đang tạo.\n'
     'After:\n– Mở hộp xác nhận có nêu mã phiếu.'),
    ('Bấm Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra lại ở phía máy chủ: phiếu ở Đang tạo; không thoả → hiển thị “Phiếu thu '
     'đã gửi duyệt hoặc đã duyệt, không xóa được”.\n'
     '– Kiểm tra người lập; không phải người lập và không phải quản trị hệ thống → hiển thị “Bạn '
     'không có quyền xóa phiếu thu này”.\n'
     'After:\n– Chụp lại nội dung phiếu kèm bảng chi tiết để ghi vào lịch sử.\n'
     '– Xoá phiếu cùng toàn bộ dòng chi tiết trong một giao dịch duy nhất.\n'
     '– Ghi một dòng lịch sử xoá.\n'
     '– Hiển thị “Xóa phiếu thu thành công!” và nạp lại danh sách.'),
])

# ------------------------------------------------------ 2.11 FR-11
d.h3('2.11 In phiếu thu')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'In phiếu thu', 'io',
            [('include', 'Kiểm tra quyền xem phiếu'),
             ('include', 'Chọn mẫu in theo loại thu và số dòng chi tiết'),
             ('extend', 'Chặn in với loại thu Thu khác')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-11 In phiếu thu')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Phiếu thu '
           'tiền tại phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='In phiếu thu',
    mota='Mở bản in của phiếu ở tab mới, gồm ĐỦ 2 LIÊN, kèm ảnh tiêu đề thư của công ty.',
    tacnhan='%s; %s' % (ACTOR_KT, ACTOR_TQ),
    dieukien='Người dùng xem được phiếu VÀ phiếu không thuộc loại thu “Thu khác”.',
    chinh='1. Người dùng bấm nút In trên màn chi tiết hoặc trên dòng danh sách.\n'
          '2. Hệ thống mở tab mới trỏ tới trang in.\n'
          '3. Hệ thống kiểm tra quyền xem, chọn mẫu in theo loại thu và số dòng chi tiết, rồi '
          'điền dữ liệu phiếu vào mẫu.\n'
          '4. Trang in hiển thị 2 liên và trình duyệt tự mở hộp thoại in.',
    phu='• Không đủ quyền xem → từ chối với thông báo “Bạn không có quyền xem phiếu thu này”.\n'
        '• Phiếu thuộc loại thu “Thu khác” → không có mẫu in; nút In bị ẩn và endpoint trả lỗi '
        'kiểm tra dữ liệu thay vì lỗi hệ thống.\n'
        '• Người dùng đóng hộp thoại in → vẫn xem được bản in trên trang và in lại bằng nút In.',
    dacbiet='In phiếu KHÔNG làm thay đổi trạng thái, người cập nhật hay lịch sử của phiếu.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In',
         shot=shot('15-man-in.png'),
         shot_caption='Bản in phiếu thu — đủ 2 liên')

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In trên trang in', 'Button', 'Enable', '–', 'Hiển thị',
     'Nằm ở góc trên bên trái, mở lại hộp thoại in của trình duyệt.'),
    ('Ảnh tiêu đề thư', 'Icon Button', 'Hiển thị', '–', 'Theo công ty của phiếu',
     'Gồm logo, tên công ty, địa chỉ, điện thoại, email, website.'),
    ('Tiêu đề bản in', 'Label', 'Hiển thị', 'PHIẾU THU', 'Cố định',
     'Dưới tiêu đề là ngày viết bằng chữ.'),
    ('Khối số liên và số phiếu', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Gồm “Liên số: 1” hoặc “Liên số: 2”, “Số: {mã phiếu}”, dòng “Nợ:” và “Có:” kèm số tiền.'),
    ('Thông tin đầu phiếu', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Người nộp tiền, Người đề nghị, Phòng ban, Lý do thu.'),
    ('Bảng nội dung', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cột STT, Khách hàng, Số đơn hàng/Hợp đồng, Số tiền, Ghi chú; kèm dòng “Tổng cộng”.'),
    ('Dòng Bằng chữ', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', 'Đọc số tiền tổng bằng chữ.'),
    ('Khối ô ký', 'Label', 'Hiển thị', '–', 'Cố định',
     'Năm ô: BAN GIÁM ĐỐC, KẾ TOÁN TRƯỞNG, NGƯỜI NỘP TIỀN, NGƯỜI LẬP PHIẾU, THỦ QUỸ.'),
], required=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu không thuộc loại thu “Thu khác”.\n'
     'After:\n– Mở tab mới trỏ tới trang in của phiếu.'),
    ('Mở trang in', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu như chức năng Xem chi tiết; không đủ quyền → hiển thị '
     '“Bạn không có quyền xem phiếu thu này”.\n'
     'During:\n– Chọn mẫu in theo loại thu và số dòng chi tiết rồi điền dữ liệu phiếu vào mẫu.\n'
     '– Loại thu “Thu khác” không có mẫu in → trả lỗi kiểm tra dữ liệu, không để lỗi hệ thống.\n'
     'After:\n– Hiển thị bản in 2 liên và mở hộp thoại in của trình duyệt; không ghi bất kỳ thay '
     'đổi nào lên phiếu.'),
])

# ------------------------------------------------------ 2.12 FR-12
d.h3('2.12 Xuất Excel một phiếu')

d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Xuất Excel một phiếu', 'io',
            [('include', 'Kiểm tra quyền xem phiếu')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-12 Xuất Excel một phiếu')

d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Phiếu thu tiền '
           'tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Xuất Excel một phiếu thu',
    mota='Tải về tệp Excel chứa nội dung của ĐÚNG MỘT phiếu thu đang xem. Màn hình không có chức '
         'năng xuất Excel cả danh sách.',
    tacnhan='%s; %s' % (ACTOR_KT, ACTOR_TQ),
    dieukien='Người dùng xem được phiếu.',
    chinh='1. Người dùng bấm nút Xuất Excel trên màn chi tiết hoặc trên dòng danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống dựng tệp từ dữ liệu phiếu và trả về trình duyệt.',
    phu='• Không đủ quyền xem → từ chối với thông báo “Bạn không có quyền xem phiếu thu này”.\n'
        '• Nút bị khoá trong lúc đang dựng tệp để tránh tải trùng.',
    dacbiet='Khác nút In, chức năng này dùng được cả với phiếu thuộc loại thu “Thu khác” vì không '
            'phụ thuộc mẫu in. Tên tệp cố định: phieu_thu.xlsx.')

d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Xuất Excel',
         note='Nút Xuất Excel nằm ở thanh nút cuối màn chi tiết và ở cột Hành động của màn danh '
              'sách.',
         shot=shot('16-chi-tiet-da-duyet.png'),
         shot_caption='Nút Xuất Excel trên thanh nút cuối màn chi tiết')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel trên màn chi tiết', 'Button', 'Enable / Disable', 'Hiển thị',
     'Bị khoá trong lúc đang dựng tệp.'),
    ('Nút Xuất Excel trên dòng danh sách', 'Icon Button', 'Enable', 'Hiển thị',
     'Biểu tượng bảng tính, luôn hiện với phiếu xem được.'),
], required=False, scope=False)

d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xuất Excel', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu; không đủ quyền → hiển thị “Bạn không có quyền xem '
     'phiếu thu này” và dừng xử lý.\n'
     'After:\n– Dựng tệp phieu_thu.xlsx từ dữ liệu của đúng phiếu đó và trả về trình duyệt.'),
])

# ------------------------------------------------------ 2.13 FR-13
d.h3('2.13 Xem lịch sử thay đổi')

d.p('2.13.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Phiếu thu tiền tại phần '
           'mô tả chi tiết.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu thu',
    mota='Hiển thị các mốc thay đổi của một phiếu: tạo mới, chỉnh sửa từng trường, đổi trạng thái '
         'và xoá, kèm người thực hiện và thời điểm. Có ở hai nơi với nội dung giống hệt nhau.',
    tacnhan='%s; %s' % (ACTOR_KT, ACTOR_TQ),
    dieukien='Người dùng nhìn thấy phiếu.',
    chinh='1. Người dùng mở menu ba chấm trên dòng danh sách rồi bấm Lịch sử; hoặc mở màn chi '
          'tiết rồi bấm Xem lịch sử ở khối Lịch sử cuối trang.\n'
          '2. Hệ thống nạp các mốc lịch sử của phiếu, mới nhất trước.\n'
          '3. Người dùng có thể lọc theo nhóm thao tác hoặc bấm Làm mới.',
    phu='• Phiếu chưa từng thao tác trên hệ thống mới → hiển thị “Chưa có lịch sử thao tác nào.”\n'
        '• Không có mốc nào khớp bộ lọc → danh sách rỗng.',
    dacbiet='Lịch sử lưu ở bảng lịch sử dùng chung của hệ thống, không có bảng riêng cho màn này. '
            'Đổi trạng thái luôn là một dòng lịch sử RIÊNG, tách khỏi dòng thay đổi thông tin.')

d.p('2.13.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử',
         note='Cửa sổ Lịch sử mở từ danh sách; khối Lịch sử nằm cuối màn chi tiết.',
         shot=shot('24-lich-su.png'),
         shot_caption='Cửa sổ Lịch sử thay đổi mở từ màn danh sách')
d.figure(shot('26-lich-su-man-chi-tiet.png'),
         'Khối Lịch sử ở cuối màn chi tiết, đang bung ra', width_in=6.2)

d.p('2.13.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi', '–'),
    ('Phụ đề', 'Label', 'Hiển thị', '–', 'Phiếu: {mã phiếu}', '–'),
    ('Khối Lịch sử ở màn chi tiết', 'Table/Grid', 'Hiển thị', '–', 'Thu gọn',
     'Kèm số đếm số mốc; nút “Xem lịch sử” / “Thu gọn” và nút “Làm mới”.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc các mốc theo nhóm thao tác.'),
    ('Danh sách mốc lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi mốc gồm thời điểm, loại thao tác, dòng “Người thực hiện: Họ tên — Phòng ban” và các '
     'trường thay đổi kèm giá trị cũ, giá trị mới.'),
    ('Thay đổi trạng thái', 'Label', 'Read-only', 'Danh sách 4 giá trị', 'Theo dữ liệu',
     'Ghi bằng TÊN trạng thái; dòng hủy kèm lý do hủy, dòng duyệt kèm ghi chú đã ghi bút toán.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Chưa có lịch sử thao tác nào.” khi phiếu chưa có mốc nào.'),
], required=False)

d.p('2.13.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lịch sử / Xem lịch sử', 'Click',
     'After:\n– Nạp các mốc lịch sử của đúng phiếu đó, sắp xếp mới nhất trước; lần mở đầu tiên '
     'mới gọi dữ liệu.'),
    ('Chọn nhóm thao tác trong Bộ lọc', 'Change',
     'After:\n– Lọc lại danh sách mốc theo nhóm đã chọn; bỏ lọc thì hiển thị đầy đủ.'),
])

# ========================================================= PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('Các quy tắc chung về danh sách, tìm kiếm, validate, thông báo và ghi lịch sử. Bảng '
           'dưới đây chỉ liệt kê các quy tắc ĐẶC THÙ của màn Phiếu thu tiền.',
           anchor='list', head='Quy tắc áp dụng', lead='')
d.rule_table([
    ('BR-01', 'Phạm vi dữ liệu hai cấp',
     ['– Cấp quyền xem được xét theo thứ tự ưu tiên V1 → V2; có cấp nào trước thì áp cấp đó.',
      '– Không có cấp nào, hoặc có V2 nhưng không xác định được công ty: chỉ thấy phiếu do chính '
      'mình lập.',
      '– Quản trị hệ thống được xử lý tương đương V1.',
      '– Không xác định được người đăng nhập thì danh sách rỗng tuyệt đối.'],
     ['Xem danh sách', 'Tìm kiếm và lọc']),

    ('BR-02', 'Luôn ẩn phiếu nháp của người khác',
     ['– Phiếu ở trạng thái Đang tạo của người khác luôn bị loại khỏi danh sách, áp dụng sau mọi '
      'điều kiện lọc và mọi cấp quyền.',
      '– Quyền xem theo cấp cũng KHÔNG mở được màn chi tiết của phiếu nháp người khác.'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xem chi tiết']),

    ('BR-03', 'Điều kiện xem chi tiết một phiếu',
     ['– Xem được khi thoả MỘT trong các điều kiện: là người lập phiếu; là người đã duyệt phiếu; '
      'là quản trị hệ thống; có V1; có V2 và cùng công ty với phiếu.',
      '– Riêng phiếu ở trạng thái Đang tạo thì chỉ người lập (và quản trị hệ thống) xem được.',
      '– Không thoả → từ chối với thông báo “Bạn không có quyền xem phiếu thu này”. Quy tắc áp '
      'dụng cả với trang in và chức năng xuất Excel.'],
     ['Xem chi tiết', 'In phiếu', 'Xuất Excel']),

    ('BR-04', 'Vòng đời phiếu thu và điều kiện thao tác',
     ['– Bốn trạng thái: Đang tạo → Chờ duyệt → Đã duyệt, hoặc Chờ duyệt → Hủy.',
      '– Sửa và Xóa: chỉ với phiếu Đang tạo. Sửa cần quyền Q1; Xóa cần thêm điều kiện đúng người '
      'lập (hoặc là quản trị hệ thống).',
      '– Duyệt và Hủy: chỉ với phiếu Chờ duyệt và người dùng có quyền Q2.',
      '– Phiếu Đã duyệt và phiếu Hủy không còn thao tác ghi nào.',
      '– Mọi kiểm tra đều thực hiện ở phía máy chủ nên bỏ qua giao diện cũng không vượt qua được.'],
     ['Tạo mới phiếu thu', 'Sửa phiếu thu', 'Duyệt phiếu thu', 'Hủy phiếu thu', 'Xóa phiếu thu']),

    ('BR-05', 'Một phiếu đề nghị chỉ lập được một phiếu thu',
     ['– Cửa sổ chọn phiếu đề nghị chỉ liệt kê phiếu đang ở trạng thái Chờ KT duyệt VÀ chưa có '
      'phiếu thu nào.',
      '– Khi lưu, hệ thống KHÓA DÒNG phiếu đề nghị rồi mới kiểm tra, nên hai người bấm lưu cùng '
      'lúc vẫn chỉ tạo được một phiếu thu; người sau nhận thông báo “Đề nghị thu tiền đã lập '
      'phiếu thu tiền”.',
      '– Ràng buộc KHÔNG loại trừ phiếu thu đã hủy: hủy phiếu thu là ngõ cụt, không lập lại được '
      'phiếu thu khác cho phiếu đề nghị đó. Đây là hành vi kế thừa có chủ đích.',
      '– Xoá phiếu thu nháp thì phiếu đề nghị trở lại danh sách chọn được.'],
     ['Tạo mới phiếu thu', 'Sửa phiếu thu', 'Hủy phiếu thu', 'Xóa phiếu thu']),

    ('BR-06', 'Cấu trúc dòng chi tiết',
     ['– Dòng chi tiết kéo thẳng từ phiếu đề nghị; KHÔNG thêm và KHÔNG xoá dòng được.',
      '– Người lập chỉ nhập được Số tài khoản có, Số tiền duyệt thu và Ghi chú của từng dòng.',
      '– Số tiền đề nghị thu, đối tượng thu và hợp đồng là dữ liệu chỉ đọc của phiếu đề nghị.',
      '– Mỗi lần lưu, hệ thống xoá và tạo lại toàn bộ dòng chi tiết rồi tính lại tổng tiền.'],
     ['Tạo mới phiếu thu', 'Sửa phiếu thu']),

    ('BR-07', 'Danh sách tài khoản cho hai ô chọn',
     ['– Chỉ liệt kê tài khoản đang hoạt động VÀ là tài khoản cấp cuối; tài khoản tổng hợp (đang '
      'là cha của tài khoản khác) bị loại vì không được hạch toán trực tiếp.',
      '– Nhãn hiển thị dạng “{số hiệu} - {tên tài khoản}”.',
      '– Ngoại lệ: phiếu đang gắn tài khoản đã bị khóa thì tài khoản đó vẫn được trả kèm để select '
      'hiện đúng tên, tránh việc người dùng vô tình lưu đè mất giá trị cũ.'],
     ['Tạo mới phiếu thu', 'Sửa phiếu thu', 'Xem chi tiết']),

    ('BR-08', 'Cột “Số tiền” luôn là tổng số tiền duyệt thu',
     ['– Giá trị cột này bằng tổng số tiền DUYỆT THU của các dòng chi tiết, tính lúc lưu phiếu.',
      '– Bước Duyệt CỐ Ý không tính lại cột này, nên phiếu đã duyệt có thực thu khác duyệt thu '
      'vẫn hiển thị số duyệt thu.',
      '– Hai ô lọc “Số tiền từ – đến” và nút sắp xếp trên cột này chạy theo cùng giá trị.',
      '– Quy tắc này giữ cho số liệu khớp với cổng cũ; đừng “sửa lại cho đúng công thức”.'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Duyệt phiếu thu']),

    ('BR-09', 'Số tiền thực thu',
     ['– Chỉ nhập được ở màn xem chi tiết, khi người xem có quyền Q2 và phiếu đang Chờ duyệt.',
      '– Không được âm và KHÔNG được lớn hơn số tiền duyệt thu của chính dòng đó; kiểm tra ở cả '
      'giao diện lẫn phía máy chủ.',
      '– Được phép nhỏ hơn số duyệt thu (thu thiếu) và được phép bằng 0.',
      '– KHÁC hệ thống cũ có chủ đích: hệ thống cũ tự kéo số về bằng số duyệt thu, ở đây cho gõ '
      'rồi báo lỗi dưới ô và chặn duyệt.',
      '– Nút Phân bổ rải tiền theo thứ tự từ trên xuống, mỗi dòng tối đa bằng số duyệt thu của nó; '
      'chỉ điền vào ô, không gọi lưu.'],
     ['Xem chi tiết', 'Duyệt phiếu thu']),

    ('BR-10', 'Ghi bút toán vào sổ kế toán',
     ['– Bước Duyệt là THỜI ĐIỂM DUY NHẤT hệ thống ghi bút toán; các thao tác khác (lưu, sửa, '
      'xoá, hủy) không ghi gì vào sổ kế toán.',
      '– Dòng chi tiết có số thực thu bằng 0 KHÔNG sinh bút toán.',
      '– Sổ kế toán dùng chung với cổng cũ nên bút toán ghi tên loại chứng từ theo định dạng của '
      'cổng cũ, không dùng bí danh nội bộ.',
      '– Toàn bộ bước duyệt nằm trong một giao dịch: hoặc phiếu đổi trạng thái và bút toán được '
      'ghi trọn vẹn, hoặc không có gì thay đổi.',
      '– Thao tác này KHÔNG hoàn tác được; hệ thống không có chức năng gỡ bút toán hay bỏ duyệt.'],
     ['Duyệt phiếu thu']),

    ('BR-11', 'Chặn duyệt lại và chặn tạo trùng',
     ['– Trước khi duyệt hoặc hủy, hệ thống KHÓA DÒNG phiếu rồi mới đọc lại trạng thái; phiếu đã '
      'rời trạng thái Chờ duyệt thì từ chối với thông báo “Phiếu thu tiền đã được duyệt!”.',
      '– Nhờ vậy hai thủ quỹ bấm duyệt cùng lúc không thể ghi trùng bút toán.',
      '– Giao diện chống bấm nhiều lần bằng cách khoá nút trong lúc xử lý, nhưng chốt chặn thật '
      'nằm ở phía máy chủ.',
      '– Sinh mã phiếu cũng dùng khóa dòng để hai người lưu cùng lúc không ra trùng mã.'],
     ['Tạo mới phiếu thu', 'Duyệt phiếu thu', 'Hủy phiếu thu']),

    ('BR-12', 'Đồng bộ ngược sang phiếu đề nghị thu tiền',
     ['– Phiếu thu chuyển sang Chờ duyệt (từ lưu mới hoặc từ sửa): phiếu đề nghị chuyển sang “Đã '
      'tạo phiếu thu”, ghi người xử lý và ghi một dòng lịch sử cho phiếu đề nghị.',
      '– Phiếu thu chuyển sang Đã duyệt: phiếu đề nghị chuyển sang “Đã hạch toán” và được ghi số '
      'tiền thực thu xuống từng dòng tương ứng.',
      '– Phiếu thu chuyển sang Hủy: phiếu đề nghị chuyển sang Hủy, kèm lý do hủy trong dòng lịch '
      'sử.',
      '– Ba điểm hở kế thừa từ cổng cũ, đã chốt GIỮ NGUYÊN: xoá phiếu thu nháp không trả trạng '
      'thái phiếu đề nghị về; hủy phiếu thu là ngõ cụt; lưu nháp phiếu thu không đổi trạng thái '
      'phiếu đề nghị nên phiếu đề nghị vẫn hiện “Chờ KT duyệt” dù đã bị khóa.'],
     ['Tạo mới phiếu thu', 'Sửa phiếu thu', 'Duyệt phiếu thu', 'Hủy phiếu thu']),

    ('BR-13', 'Thông báo',
     ['– Phiếu thu chuyển sang Chờ duyệt: gửi thông báo tới MỌI người có quyền Q2 thuộc cùng công '
      'ty với phiếu, nội dung “[TC] Chờ duyệt phiếu thu: {mã phiếu}. Người lập: {họ tên}”.',
      '– Lưu nháp KHÔNG gửi thông báo cho ai.',
      '– Bấm vào thông báo mở đúng màn chi tiết của phiếu thu.',
      '– Lỗi gửi thông báo KHÔNG được làm hỏng thao tác lưu phiếu.'],
     ['Tạo mới phiếu thu', 'Sửa phiếu thu']),

    ('BR-14', 'Sinh mã phiếu và ghi cấp tổ chức',
     ['– Mã phiếu sinh tự động dạng “{mã công ty}.PT{tháng năm}.{5 chữ số}”; người dùng không '
      'nhập được và mã đã dùng không được cấp lại.',
      '– Công ty, phòng ban và bộ phận của phiếu lấy theo hồ sơ của NGƯỜI LẬP tại thời điểm tạo, '
      'gán đè vô điều kiện, không nhận giá trị do phía giao diện gửi lên.'],
     ['Tạo mới phiếu thu']),

    ('BR-15', 'Loại thu “Thu khác” và bản in',
     ['– Ô lọc và form không cho chọn loại thu “Thu khác”, nhưng phiếu cũ mang loại này vẫn hiển '
      'thị đúng tên trên lưới và ở màn chi tiết.',
      '– Phiếu loại “Thu khác” KHÔNG có mẫu in: nút In bị ẩn ở cả danh sách lẫn màn chi tiết, và '
      'endpoint in trả lỗi kiểm tra dữ liệu thay vì lỗi hệ thống.',
      '– Chức năng Xuất Excel vẫn dùng được với loại này vì không phụ thuộc mẫu in.'],
     ['Xem danh sách', 'In phiếu', 'Xuất Excel']),

    ('BR-16', 'Ghi lịch sử',
     ['– Ghi một dòng lịch sử khi: tạo mới, chỉnh sửa, đổi trạng thái, duyệt, hủy và xoá phiếu.',
      '– Đổi trạng thái luôn là một dòng lịch sử RIÊNG, tách khỏi dòng thay đổi thông tin, và ghi '
      'bằng TÊN trạng thái.',
      '– Bước Duyệt ghi hai dòng: một dòng thay đổi thông tin (số thực thu từng dòng, ngày hạch '
      'toán) và một dòng đổi trạng thái kèm ghi chú đã ghi bút toán.',
      '– Bước Hủy ghi một dòng đổi trạng thái kèm ĐÚNG lý do hủy, để mở lịch sử là biết vì sao '
      'phiếu bị hủy.',
      '– Xem lịch sử không cần quyền riêng; ai nhìn thấy phiếu thì xem được lịch sử của phiếu đó.'],
     ['Tạo mới phiếu thu', 'Sửa phiếu thu', 'Duyệt phiếu thu', 'Hủy phiếu thu', 'Xóa phiếu thu',
      'Xem lịch sử']),
])

d.save()
d.selfcheck()
