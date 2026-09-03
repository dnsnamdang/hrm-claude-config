# -*- coding: utf-8 -*-
"""Sinh SRS (.docx) cho man "Phieu yeu cau chuyen hang" (phan he Tai chinh).

Form chuan 2026-08-28 (4 chuong, Layout ghi MENU, rule_ref dau moi muc Gioi thieu,
Phan 4 la bang 5 cot, so do tong quan co phan cap).

Nguon doc code 03/09/2026 (nhanh gop_db) — xem docblock gen_testcase.py cung thu muc.
Anh that: pycch_shots/ (cong dev hrm-crm.eteksofts.com, 03/09/2026) — dung chung voi HDSD.

Chay:  python .plans/gop-db/finance-product-transfer-request/gen_srs.py
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

SHOTS = os.path.join(HERE, 'pycch_shots')
OUT = os.path.join(HERE, 'SRS - Phiếu yêu cầu chuyển hàng.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = ('Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Điều chuyển '
        '=> Phiếu điều chuyển hàng')

ACTOR_LAP = 'Người lập phiếu'
ACTOR_KTK = 'Kế toán kho'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/product-transfer-requests',
           full_url='https://hrm-crm.eteksofts.com/finance/product-transfer-requests',
           img_prefix='pycch_')

# ============================================================== TRANG ĐẦU
d.title_block('Phiếu yêu cầu chuyển hàng')

d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu yêu cầu chuyển hàng, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ cơ chế phạm vi dữ liệu bốn cấp (tổng công ty / công ty / phòng ban / bộ phận) và '
    'lớp bảo vệ luôn ẩn phiếu nháp của người khác.',
    'Làm rõ điều kiện được Sửa / Xóa (chỉ phiếu Đang tạo do chính mình lập) và điều kiện được '
    'Không duyệt / Tổng hợp (quyền Kế toán kho + phiếu Chờ duyệt + cùng công ty).',
    'Làm rõ quy tắc nới lỏng của trường Ngày cần hàng khi sửa phiếu cũ — điểm khác biệt có chủ '
    'đích so với màn hình tương ứng ở hệ thống cũ.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu yêu cầu chuyển hàng',
     'Chứng từ do người kinh doanh lập để đề nghị bộ phận kho chuyển hàng về phục vụ khách '
     'hàng. Mã phiếu sinh tự động dạng PYCCH kèm 5 chữ số.'),
    ('Dòng hàng hoá',
     'Một dòng trong bảng Danh sách hàng hóa, ứng với một mã hàng. Mỗi mã hàng chỉ được xuất '
     'hiện một lần trong cùng một phiếu.'),
    ('Dòng khách hàng',
     'Dòng con trong ô Khách hàng của một dòng hàng hoá, gồm khách hàng cần hàng, số lượng, '
     'ngày cần và ghi chú. Mỗi dòng hàng hoá phải có ít nhất một dòng khách hàng.'),
    ('ĐVT',
     'Đơn vị tính của hàng hoá trên phiếu. Đơn vị có hệ số quy đổi khác 1 hiển thị kèm hệ số, '
     'ví dụ “Thùng (x10)”.'),
    ('Giá niêm yết',
     'Giá tham khảo theo đơn vị tính đang chọn. Chỉ hiển thị trên form, KHÔNG lưu vào phiếu và '
     'không xuất hiện trên bản in.'),
    ('SL tồn',
     'Tồn tham khảo tại kho đang chọn ở ô “Xem tồn theo kho”, đã quy đổi theo đơn vị tính đang '
     'chọn. Hệ thống không chặn khi số lượng đề nghị vượt tồn.'),
    ('Đang tạo', 'Phiếu nháp. Chỉ người lập nhìn thấy, sửa và xóa được.'),
    ('Chờ duyệt', 'Phiếu đã gửi, chờ bộ phận kho tiếp nhận hoặc từ chối.'),
    ('Đã tiếp nhận / Đang đề nghị / Đang xuất kho / Đã xuất kho / Đang vận chuyển / '
     'Đang nhập kho / Đã nhập kho / Đã nhập hàng / Đã phân bổ / Đã hủy',
     'Các trạng thái do chuỗi nghiệp vụ kho cập nhật. Màn hình này chỉ hiển thị, không thao '
     'tác được. Riêng “Đang nhập kho” ứng với hai bước kho khác nhau nhưng trùng tên hiển thị.'),
    ('Không duyệt',
     'Thao tác của Kế toán kho: đưa phiếu Chờ duyệt về trạng thái Đang tạo kèm lý do, để người '
     'lập sửa và gửi lại. KHÔNG phải hủy phiếu.'),
    ('Tổng hợp',
     'Thao tác mở màn lập phiếu đề nghị xuất hàng của hệ thống cũ ở tab mới, mang sẵn phiếu '
     'đang xem. Không làm đổi trạng thái phiếu.'),
], widths=[1.9, 4.1])

# ========================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán kho',
     'Mở được màn chi tiết phiếu của người khác trong cùng công ty. Với phiếu ở trạng thái Chờ '
     'duyệt và cùng công ty: hiện khối “Ghi chú duyệt” cùng hai nút “Không duyệt” và “Tổng '
     'hợp”. Đồng thời là nhóm nhận thông báo khi có phiếu mới được gửi duyệt.'),
], widths=[0.8, 2.0, 3.2])
d.p('Các chức năng còn lại (Xem danh sách, Tạo mới, Sửa, Xóa, Xem chi tiết, In, Xuất Excel, '
    'Lịch sử) KHÔNG gắn quyền riêng: mọi người dùng đã đăng nhập đều thực hiện được, trong '
    'phạm vi dữ liệu và điều kiện trạng thái nêu ở mục dưới.')

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem yêu cầu chuyển hàng theo tổng công ty',
     'Toàn bộ phiếu của mọi công ty.'),
    ('V2', 'Xem yêu cầu chuyển hàng theo công ty',
     'Phiếu thuộc công ty của người đăng nhập. Người chưa gắn hồ sơ nhân viên (không xác định '
     'được công ty) thì phạm vi là RỖNG.'),
    ('V3', 'Xem yêu cầu chuyển hàng theo phòng ban',
     'Phiếu thuộc các phòng ban người đăng nhập được giao quản lý trong công ty mình, CỘNG '
     'THÊM mọi phiếu do chính mình lập.'),
    ('V4', 'Xem yêu cầu chuyển hàng theo bộ phận',
     'Phiếu thuộc các bộ phận người đăng nhập được giao quản lý trong công ty mình, CỘNG THÊM '
     'mọi phiếu do chính mình lập.'),
    ('—', '(không có cấp nào)', 'Chỉ phiếu do chính mình lập.'),
], widths=[0.8, 2.2, 3.0])
d.p('Vai trò quản trị hệ thống được xử lý tương đương V1 về phạm vi xem. Tuy nhiên với hai '
    'thao tác Không duyệt và Tổng hợp, quản trị hệ thống chỉ thay thế vế QUYỀN — điều kiện '
    'cùng công ty với phiếu vẫn phải thoả.')
d.p('Hai lớp bảo vệ dữ liệu áp dụng SAU CÙNG, không quyền nào gỡ được:')
d.bullets([
    'Phiếu ở trạng thái Đang tạo của người khác luôn bị loại khỏi danh sách, kể cả với V1 và '
    'quản trị hệ thống.',
    'Chỉ sửa và xóa được phiếu ở trạng thái Đang tạo do chính người đăng nhập lập; kiểm tra '
    'được thực hiện ở phía máy chủ nên bỏ qua giao diện cũng không vượt qua được.',
])

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Không có quyền nào'], [
    ('FR-01 Truy cập & xem danh sách', '✅ (theo phạm vi V1–V4)',
     '✅ (chỉ phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc danh sách', '✅', '✅'),
    ('FR-03 Tuỳ chỉnh bộ lọc và cột hiển thị', '✅', '✅'),
    ('FR-04 Xuất Excel danh sách', '✅ (theo phạm vi)', '✅ (chỉ phiếu của mình)'),
    ('FR-05 Tạo mới phiếu', '✅', '✅'),
    ('FR-06 Sửa phiếu', '✅ (chỉ phiếu Đang tạo của chính mình)',
     '✅ (chỉ phiếu Đang tạo của chính mình)'),
    ('FR-07 Chọn hàng hoá từ popup', '✅', '✅'),
    ('FR-08 Chọn khách hàng từ popup', '✅', '✅'),
    ('FR-09 Xem chi tiết phiếu', '✅ (thêm phiếu người khác cùng công ty)',
     '✅ (chỉ phiếu của mình)'),
    ('FR-10 Xóa phiếu', '✅ (chỉ phiếu Đang tạo của chính mình)',
     '✅ (chỉ phiếu Đang tạo của chính mình)'),
    ('FR-11 Không duyệt phiếu', '✅ (phiếu Chờ duyệt, cùng công ty)', '❌'),
    ('FR-12 Tổng hợp sang phiếu xuất hàng', '✅ (phiếu Chờ duyệt, cùng công ty)', '❌'),
    ('FR-13 In phiếu', '✅', '✅ (phiếu xem được)'),
    ('FR-14 Xem lịch sử thay đổi', '✅', '✅ (phiếu xem được)'),
], widths=[2.4, 2.0, 1.6])

# ========================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR_LAP, [0, 1, 2, 3]),
     (ACTOR_KTK, [0, 3])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Tạo mới phiếu', 'crud'),
     ('FR-06', 'Sửa phiếu', 'crud'),
     ('FR-09', 'Xem chi tiết phiếu', 'view')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Tuỳ chỉnh bộ lọc và cột', 'view', 'extend', [0], None),
     ('FR-04', 'Xuất Excel danh sách', 'io', 'extend', [0], None),
     ('FR-10', 'Xóa phiếu', 'action', 'extend', [0], None),
     ('FR-14', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-07', 'Chọn hàng hoá từ popup', 'crud', 'include', [1, 2], None),
     ('FR-08', 'Chọn khách hàng từ popup', 'crud', 'include', [1, 2], None),
     ('FR-11', 'Không duyệt phiếu', 'action', 'extend', [3], None),
     ('FR-12', 'Tổng hợp sang phiếu xuất hàng', 'action', 'extend', [3], None),
     ('FR-13', 'In phiếu', 'io', 'extend', [3], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu yêu cầu chuyển hàng')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------ 2.1 FR-01
d.h3('2.1 Xem danh sách phiếu yêu cầu chuyển hàng')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu yêu cầu chuyển hàng tại phần mô tả '
           'chi tiết.', anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu yêu cầu chuyển hàng',
    mota='Hiển thị bảng phiếu yêu cầu chuyển hàng nằm trong phạm vi dữ liệu của người đăng '
         'nhập, kèm phân trang và ô thống kê tổng số phiếu khớp bộ lọc. Chỉ có duy nhất một '
         'mục menu trỏ vào màn này; phiếu chờ duyệt nằm chung trong danh sách và được lọc bằng '
         'ô Trạng thái.',
    tacnhan='%s; %s; Người dùng đã đăng nhập' % (ACTOR_LAP, ACTOR_KTK),
    dieukien='Người dùng đã đăng nhập vào phân hệ Tài chính.',
    chinh='1. Người dùng vào menu Tài chính → Hàng hoá - Dịch vụ - Vận chuyển → Điều chuyển → '
          'Phiếu điều chuyển hàng.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem cao nhất mà người dùng có '
          '(V1 → V2 → V3 → V4 → không có cấp nào).\n'
          '3. Hệ thống loại bỏ phiếu Đang tạo của người khác khỏi kết quả.\n'
          '4. Hệ thống trả về trang đầu tiên, sắp xếp theo Ngày tạo giảm dần, kèm tổng số '
          'phiếu và các cờ quyền dùng để dựng bộ lọc.\n'
          '5. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp bộ lọc.” và '
        'dòng đếm ghi “Không có phiếu nào.”\n'
        '• Người dùng chỉ có quyền V2 nhưng chưa gắn hồ sơ nhân viên → phạm vi rỗng, KHÔNG trả '
        'về các phiếu chưa xác định công ty.\n'
        '• Có bộ lọc đã lưu trong vòng 10 phút → khôi phục bộ lọc đó rồi mới nạp dữ liệu.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('01-danh-sach.png'),
         shot_caption='Màn Phiếu yêu cầu chuyển hàng lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Phiếu yêu cầu chuyển hàng',
     'Hiển thị ở thanh tiêu đề và ở đầu khối lưới.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Luôn hiển thị, không gắn quyền. Mở màn Thêm phiếu yêu cầu chuyển hàng.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Chọn trường xuất file.'),
    ('Nút cấu hình cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột hiển thị.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự theo trang',
     'Luôn hiển thị, không tắt được. Trang 2 với cỡ 10 dòng bắt đầu từ 11.'),
    ('Cột Mã yêu cầu', 'Table/Grid', 'Read-only', 'PYCCH-xxxxx', 'Theo dữ liệu',
     'Luôn hiển thị, không tắt được; là đường dẫn sang màn chi tiết. Sắp xếp được.'),
    ('Cột Người tiếp nhận', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Chưa ai xử lý thì hiển thị dấu gạch ngang.'),
    ('Cột Ngày tiếp nhận', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn',
     'Mặc định ẩn, bật trong Tuỳ chỉnh cột. Sắp xếp được.'),
    ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Ẩn', 'Mặc định ẩn.'),
    ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn',
     'Mặc định ẩn. Có biểu tượng sắp xếp nhưng KHÔNG sắp xếp được — bấm vào thì danh sách trở '
     'về thứ tự mặc định.'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người lập phiếu.'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Cột sắp xếp mặc định, chiều giảm dần.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 13 giá trị', 'Theo dữ liệu',
     'Nhãn đỏ với Chờ duyệt / Đang tạo / Đã hủy; nhãn xanh với các trạng thái còn lại.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo trạng thái và quyền',
     'Luôn hiển thị, không tắt được. Tối đa 2 nút chính, phần còn lại nằm trong menu ba chấm.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc và nằm trong phạm vi quyền.'),
    ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, cỡ 10',
     'Đổi cỡ trang đưa danh sách về trang 1.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi N = 0.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Ẩn',
     'Hiện dòng “Đang tải dữ liệu...” trong lúc nạp.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Khôi phục bộ lọc đã lưu nếu còn trong 10 phút.\n'
     '– Xác định cấp quyền xem cao nhất của người dùng.\n'
     'During:\n– Áp phạm vi dữ liệu theo cấp quyền; V3 và V4 cộng thêm phiếu do chính người '
     'dùng lập.\n'
     '– Loại bỏ phiếu Đang tạo của người khác.\n'
     'After:\n– Trả về trang 1 sắp xếp theo Ngày tạo giảm dần, kèm tổng số phiếu và danh sách '
     'trạng thái để dựng ô lọc.'),
    ('Bấm tiêu đề cột sắp xếp', 'Click',
     'Before:\n– Chỉ nhận ba cột: Mã yêu cầu, Ngày tạo, Ngày tiếp nhận.\n'
     'During:\n– Cột không nằm trong danh sách trên (ví dụ Ngày cập nhật) bị bỏ qua.\n'
     'After:\n– Đảo chiều sắp xếp, đưa về trang 1, giữ nguyên bộ lọc.'),
    ('Bấm số trang / nút tiến lùi', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và chiều sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu trang mới, số thứ tự tiếp tục liên tục.'),
    ('Bấm mã yêu cầu', 'Click',
     'After:\n– Điều hướng sang màn chi tiết của phiếu tương ứng.'),
    ('Đổi số dòng mỗi trang', 'Change',
     'After:\n– Đưa về trang 1 và nạp lại theo cỡ trang mới.'),
])

# ------------------------------------------------------ 2.2 FR-02
d.h3('2.2 Tìm kiếm và lọc danh sách')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn '
           'Phiếu yêu cầu chuyển hàng tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu yêu cầu chuyển hàng',
    mota='Thu hẹp danh sách theo mã yêu cầu, tên người tạo, trạng thái, hàng hoá, người tạo, '
         'người tiếp nhận và khoảng ngày tạo. Các điều kiện cộng dồn với nhau.',
    tacnhan='%s; %s; Người dùng đã đăng nhập' % (ACTOR_LAP, ACTOR_KTK),
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng nhập từ khoá vào ô tìm nhanh và bấm nút Tìm kiếm; hoặc bấm Tìm kiếm '
          'nâng cao rồi đặt điều kiện ở các ô lọc.\n'
          '2. Với ô tìm nhanh: hệ thống chờ thao tác bấm nút mới truy vấn.\n'
          '3. Với các ô lọc nâng cao: hệ thống truy vấn ngay khi giá trị thay đổi.\n'
          '4. Hệ thống áp bộ lọc BÊN TRONG phạm vi dữ liệu theo quyền, đưa về trang 1 và trả '
          'kết quả.\n'
          '5. Hệ thống lưu bộ lọc trong 10 phút để khôi phục khi quay lại màn.',
    phu='• Không kết quả → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Khoảng ngày ngược (từ ngày lớn hơn đến ngày) → trả về rỗng, không báo lỗi.\n'
        '• Bấm Làm mới → xoá mọi điều kiện, về trang 1, phạm vi quyền giữ nguyên.\n'
        '• Tham số lạ thêm vào đường dẫn không mở rộng được phạm vi dữ liệu.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('02-loc-nang-cao.png'),
         shot_caption='Khối Tìm kiếm nâng cao khi đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Dòng gợi ý “Tìm theo mã yêu cầu...”. Thực tế tìm theo mã yêu cầu HOẶC tên người tạo. '
     'KHÔNG tự tìm khi gõ — phải bấm nút Tìm kiếm.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Áp giá trị ô tìm nhanh và đưa về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Xoá mọi điều kiện lọc và ô tìm nhanh, nạp lại danh sách trang 1.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đóng/mở khối 6 ô lọc; đổi chữ thành “Ẩn tìm kiếm nâng cao” khi đang mở.'),
    ('Ô lọc Trạng thái', 'Dropdown', 'Enable', 'Danh sách 13 giá trị', 'Không', 'Trống',
     'Tự lọc ngay khi chọn. Chọn “Đang tạo” chỉ ra nháp của chính người dùng.'),
    ('Ô lọc Tên/mã hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm phiếu có hàng hoá khớp tên hoặc mã hàng. TỰ TÌM ngay khi gõ.'),
    ('Ô lọc Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu.'),
    ('Ô lọc Người tiếp nhận', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Phiếu chưa có người tiếp nhận không nằm trong kết quả.'),
    ('Ô lọc Ngày tạo từ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc theo Ngày tạo phiếu, tính từ ngày này trở đi.'),
    ('Ô lọc Ngày tạo đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc theo Ngày tạo phiếu, lấy TRỌN ngày được chọn.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Gõ vào ô tìm nhanh', 'Keypress',
     'During:\n– Chỉ ghi nhận giá trị, KHÔNG truy vấn.\n'
     'After:\n– Danh sách giữ nguyên cho tới khi bấm nút Tìm kiếm.'),
    ('Bấm nút Tìm kiếm', 'Click',
     'During:\n– Ghép điều kiện “mã yêu cầu chứa từ khoá HOẶC tên người tạo chứa từ khoá” '
     'thành một nhóm riêng để không phá vỡ điều kiện phạm vi quyền.\n'
     'After:\n– Đưa về trang 1 và nạp lại danh sách.'),
    ('Đổi giá trị một ô lọc nâng cao', 'Change',
     'During:\n– Cộng dồn với các điều kiện đang có (quan hệ VÀ).\n'
     'After:\n– Đưa về trang 1, nạp lại danh sách, lưu bộ lọc trong 10 phút.'),
    ('Bấm nút Làm mới', 'Click',
     'After:\n– Đưa mọi ô lọc và ô tìm nhanh về trống, về trang 1, nạp lại danh sách. Phạm vi '
     'dữ liệu theo quyền không thay đổi.'),
])

# ------------------------------------------------------ 2.3 FR-03
d.h3('2.3 Tuỳ chỉnh bộ lọc và cột hiển thị')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Tuỳ chỉnh bộ lọc và cột hiển thị', 'view',
            [('extend', 'Ẩn / hiện ô lọc'),
             ('extend', 'Ẩn / hiện và đổi thứ tự cột')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-03 Tuỳ chỉnh bộ lọc và cột hiển thị')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Phiếu yêu '
           'cầu chuyển hàng tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh bộ lọc và cột hiển thị',
    mota='Cho phép mỗi người dùng tự chọn những ô lọc và những cột muốn nhìn thấy, kèm thứ tự '
         'hiển thị. Cấu hình lưu riêng theo từng người và từng màn hình.',
    tacnhan='%s; %s' % (ACTOR_LAP, ACTOR_KTK),
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc (hoặc nút cấu hình cột).\n'
          '2. Hệ thống mở cửa sổ với danh sách các ô lọc (hoặc các cột) kèm ô tích chọn.\n'
          '3. Người dùng bỏ tích mục không cần và kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống áp cấu hình ngay lên khối lọc (hoặc lưới) và ghi nhớ cho lần sau.',
    phu='• Bấm Khôi phục mặc định ở cửa sổ Cài đặt bộ lọc → đưa về đủ 6 ô theo thứ tự ban đầu.\n'
        '• Bấm Đóng → thoát mà không lưu thay đổi.\n'
        '• Ba cột STT, Mã yêu cầu và Hành động bị khoá, không bỏ tích được.',
    dacbiet='Cấu hình cột của màn này không ảnh hưởng tới cấu hình cột của màn hình khác.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột',
         note='Hai cửa sổ được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
         shot=shot('05-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc')
d.figure(shot('03-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột hiển thị', width_in=6.2)

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Danh sách ô lọc / cột', 'Table/Grid', 'Enable', 'Danh sách', 'Không',
     'Theo cấu hình đã lưu', 'Mỗi dòng có ô tích, tay cầm kéo thả và số thứ tự.'),
    ('Ô tích chọn', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình đã lưu',
     'Cột khoá (STT, Mã yêu cầu, Hành động) hiện biểu tượng ổ khoá và bị vô hiệu.'),
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
     'After:\n– Ghi cấu hình, đóng cửa sổ và áp dụng ngay lên khối lọc hoặc lưới.\n'
     '– Hiển thị thông báo lưu cấu hình thành công.'),
])

# ------------------------------------------------------ 2.4 FR-04
d.h3('2.4 Xuất Excel danh sách')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Xuất Excel danh sách', 'io',
            [('include', 'Chọn trường xuất file'),
             ('include', 'Áp phạm vi dữ liệu và bộ lọc hiện tại')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-04 Xuất Excel danh sách')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Phiếu yêu '
           'cầu chuyển hàng tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Xuất Excel danh sách phiếu yêu cầu chuyển hàng',
    mota='Tải về tệp Excel chứa toàn bộ phiếu khớp bộ lọc đang áp dụng, trong phạm vi dữ liệu '
         'của người đăng nhập. Người dùng tự chọn các trường và thứ tự cột.',
    tacnhan='%s; %s' % (ACTOR_LAP, ACTOR_KTK),
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Xuất Excel.\n'
          '2. Hệ thống mở cửa sổ Chọn trường xuất file với 6 trường được chọn sẵn.\n'
          '3. Người dùng chọn lại các trường (thứ tự chọn cũng là thứ tự cột trong tệp).\n'
          '4. Người dùng bấm Xuất file.\n'
          '5. Hệ thống lấy TẤT CẢ phiếu khớp bộ lọc (không phân trang) trong phạm vi quyền, '
          'dựng tệp và trả về trình duyệt.\n'
          '6. Hệ thống hiển thị thông báo “Xuất Excel thành công”.',
    phu='• Kết quả rỗng → tệp vẫn tải về, chỉ có dòng tiêu đề cột.\n'
        '• Có đặt điều kiện ngày tạo → tệp có thêm dòng tiêu đề khoảng ngày phía trên bảng.\n'
        '• Lỗi trong lúc dựng tệp → hiển thị thông báo lỗi, không tải tệp rỗng.',
    dacbiet='Tên tệp cố định: danh_sach_yeu_cau_chuyen_hang.xlsx')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Xuất Excel',
         note='Cửa sổ Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường '
              'dẫn ở trên.',
         shot=shot('04-xuat-excel.png'),
         shot_caption='Cửa sổ Chọn trường xuất file')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô Trường xuất', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Có',
     'Chọn sẵn cả 6 trường',
     'Sáu trường: Mã yêu cầu, Người tiếp nhận, Ngày tiếp nhận, Trạng thái, Người tạo, Ngày tạo.'),
    ('Dòng “Thứ tự cột trong file”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn',
     'Cho biết thứ tự cột sẽ xuất, chạy theo trình tự người dùng chọn.'),
    ('Dòng “Đang chọn n/6 trường”', 'Label', 'Read-only', '–', '–', 'Đang chọn 6/6 trường',
     'Cập nhật theo số trường đang chọn.'),
    ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích lại đủ 6 trường.'),
    ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá toàn bộ lựa chọn.'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Bị khoá trong lúc đang dựng tệp để tránh tải trùng.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất tệp.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xuất Excel', 'Click',
     'After:\n– Mở cửa sổ Chọn trường xuất file với 6 trường mặc định.'),
    ('Bấm Xuất file', 'Click',
     'During:\n– Áp ĐÚNG bộ lọc đang hiển thị trên màn danh sách.\n'
     '– Áp phạm vi dữ liệu theo cấp quyền và loại phiếu Đang tạo của người khác.\n'
     '– Lấy tất cả bản ghi, không phân trang.\n'
     'After:\n– Trả tệp danh_sach_yeu_cau_chuyen_hang.xlsx về trình duyệt.\n'
     '– Hiển thị thông báo “Xuất Excel thành công”.'),
])

# ------------------------------------------------------ 2.5 FR-05
d.h3('2.5 Tạo mới phiếu yêu cầu chuyển hàng')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Tạo mới phiếu yêu cầu chuyển hàng', 'crud',
            [('include', 'Chọn hàng hoá từ popup'),
             ('include', 'Chọn khách hàng từ popup'),
             ('include', 'Sinh mã phiếu tự động'),
             ('extend', 'Gửi thông báo cho Kế toán kho khi gửi duyệt')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-05 Tạo mới phiếu yêu cầu chuyển hàng')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới phiếu yêu cầu chuyển hàng',
    mota='Lập một phiếu yêu cầu chuyển hàng mới gồm thông tin chung, danh sách hàng hoá kèm '
         'các dòng khách hàng cần hàng và tệp đính kèm dạng PDF. Người lập chọn lưu nháp hoặc '
         'lưu và gửi duyệt.',
    tacnhan='%s; Người dùng đã đăng nhập' % ACTOR_LAP,
    dieukien='Người dùng đã đăng nhập vào phân hệ Tài chính. Không yêu cầu quyền riêng.',
    chinh='1. Người dùng bấm nút Tạo mới.\n'
          '2. Hệ thống mở màn Thêm phiếu yêu cầu chuyển hàng, điền sẵn Ngày lập là hôm nay, '
          'Người lập là người đang đăng nhập và chọn sẵn kho mặc định ở ô Xem tồn theo kho.\n'
          '3. Người dùng thêm hàng hoá từ popup, chọn đơn vị tính, nhập các dòng khách hàng '
          '(khách hàng, số lượng, ngày cần, ghi chú) và đính kèm tệp PDF.\n'
          '4. Người dùng bấm Lưu nháp (trạng thái Đang tạo) hoặc Lưu và gửi duyệt (trạng thái '
          'Chờ duyệt, có hộp xác nhận).\n'
          '5. Hệ thống kiểm tra dữ liệu, tải tệp đính kèm lên, ghi phiếu, sinh mã tự động dạng '
          'PYCCH kèm 5 chữ số và ghi công ty / phòng ban / bộ phận theo hồ sơ người lập.\n'
          '6. Nếu gửi duyệt, hệ thống gửi thông báo cho mọi người có quyền Kế toán kho cùng '
          'công ty với phiếu.\n'
          '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Thiếu trường bắt buộc → báo lỗi đỏ ngay dưới từng ô, cuộn tới ô lỗi đầu tiên, không '
        'đóng màn, giữ nguyên dữ liệu đã nhập.\n'
        '• Trùng hàng hoá trong phiếu → báo “Hàng hóa bị trùng trong phiếu”, không lưu.\n'
        '• Tệp không phải PDF hoặc PDF hỏng → chặn ngay tại bước chọn tệp, hiện lỗi dưới khối '
        'đính kèm.\n'
        '• Bấm Quay lại khi đã nhập dở → hỏi xác nhận rời trang.\n'
        '• Bấm nút lưu nhiều lần liên tiếp → chỉ tạo đúng một phiếu.',
    dacbiet='Lưu nháp KHÔNG gửi thông báo cho ai và phiếu chỉ người lập nhìn thấy. Ô Giá niêm '
            'yết và SL tồn chỉ để tham khảo, không lưu vào phiếu và không chặn khi số lượng '
            'vượt tồn.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới',
         shot=shot('06-tao-moi.png'),
         shot_caption='Màn Thêm phiếu yêu cầu chuyển hàng khi vừa mở')
d.figure(shot('23-form-da-nhap-day-du.png'),
         'Màn Thêm phiếu sau khi đã nhập đầy đủ hàng hoá, dòng khách hàng và tệp đính kèm',
         width_in=6.2)

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ngày lập', 'Text', 'Read-only', 'dd/mm/yyyy', '–', 'Ngày hôm nay',
     'Không sửa được. Hệ thống tự ghi thời điểm lưu.'),
    ('Người lập', 'Text', 'Read-only', '–', '–', 'Người đang đăng nhập',
     'Không sửa được, không đổi sang người khác.'),
    ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Vượt 255 ký tự báo “Vui lòng nhập tối đa 255 ký tự.” ngay khi gõ.'),
    ('Ô Xem tồn theo kho', 'Dropdown', 'Enable', 'Danh sách kho', 'Không', 'Kho mặc định',
     'Đổi kho làm nạp lại cột SL tồn của mọi dòng. Chọn giá trị rỗng thì SL tồn hiện dấu gạch '
     'ngang.'),
    ('Nút thêm hàng hoá', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Dấu cộng ở tiêu đề cột cuối, mở popup Thêm hàng hoá.'),
    ('Cột Hàng hóa', 'Table/Grid', 'Read-only', '–', 'Có', 'Trống',
     'Chỉ chọn được từ popup. Hiển thị tên hàng kèm Model và Mã hàng.'),
    ('Cột ĐVT', 'Dropdown', 'Enable', 'Danh sách đơn vị của hàng', 'Có',
     'Đơn vị đầu tiên của hàng',
     'Nhãn kèm hệ số khi khác 1. Đổi đơn vị làm đổi Giá niêm yết và SL tồn.'),
    ('Cột Giá niêm yết', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
     'Chỉ tham khảo, không lưu vào phiếu, không có trên bản in.'),
    ('Cột SL tồn', 'Number', 'Read-only', '≥ 0', '–', 'Theo kho đang chọn',
     'Đã quy đổi theo đơn vị đang chọn. Không chặn khi số lượng vượt tồn.'),
    ('Ô Khách hàng của dòng con', 'Textbox', 'Read-only', '–', 'Có', 'Trống',
     'Bấm vào để mở popup Chọn khách hàng. Hiển thị dạng “mã - tên khách hàng”.'),
    ('Ô SL của dòng con', 'Number', 'Enable', '1 – 999.999.999', 'Có', 'Trống',
     'Số nguyên. Nhỏ hơn 1 báo “Không được nhỏ hơn 1”; vượt trần báo “Tối đa 999999999”.'),
    ('Ô Ngày cần của dòng con', 'Datepicker', 'Enable', 'dd/mm/yyyy, > ngày hôm nay', 'Có',
     'Trống', 'Lịch chặn chọn hôm nay và các ngày trước đó.'),
    ('Ô Ghi chú của dòng con', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
     'BẮT BUỘC nhập, khác với ô Ghi chú của phiếu.'),
    ('Nút Thêm khách hàng', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Thêm một dòng khách hàng trống cho hàng hoá đó.'),
    ('Nút xoá dòng khách hàng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Xoá ngay, không hỏi. Không xoá được dòng cuối cùng của một hàng hoá.'),
    ('Dòng Tổng cộng', 'Label', 'Read-only', '≥ 0', '–', '0',
     'Tổng số lượng các dòng khách hàng của chính hàng hoá đó, ngăn cách hàng nghìn bằng dấu '
     'phẩy.'),
    ('Nút xoá hàng hoá', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở hộp xác nhận; xoá hàng sẽ xoá toàn bộ dòng khách hàng của hàng đó.'),
    ('Khối File đính kèm', 'Modal', 'Enable', 'Chỉ nhận tệp PDF', 'Có', 'Trống',
     'Bắt buộc ít nhất 1 tệp khi tạo mới. Kiểm tra định dạng ngay tại bước chọn tệp.'),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Lưu ở trạng thái Đang tạo, KHÔNG hỏi xác nhận. Bị khoá trong lúc xử lý.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Mở hộp xác nhận trước khi lưu ở trạng thái Chờ duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi inline', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi; ô có viền đỏ.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'After:\n– Mở màn Thêm phiếu với Ngày lập là hôm nay, Người lập là người đang đăng nhập, '
     'bảng hàng hoá trống và kho mặc định đã chọn sẵn.'),
    ('Đổi ô ĐVT', 'Change',
     'During:\n– Tra hệ số quy đổi của đơn vị vừa chọn trong dữ liệu đã tải.\n'
     'After:\n– Cập nhật Giá niêm yết và SL tồn theo đơn vị mới, không gọi lại dữ liệu.'),
    ('Đổi ô Xem tồn theo kho', 'Change',
     'After:\n– Nạp lại SL tồn cho toàn bộ dòng hàng hoá. Chọn giá trị rỗng thì đặt SL tồn về '
     'dấu gạch ngang mà không truy vấn.'),
    ('Chọn tệp đính kèm', 'Change',
     'During:\n– Tệp không mang đuôi .pdf → hiển thị “File "tên tệp" không phải PDF”.\n'
     '– Tệp mang đuôi .pdf nhưng nội dung không phải PDF → hiển thị “File "tên tệp" không phải '
     'PDF hợp lệ (file hỏng hoặc tải về lỗi) — hãy tải lại file”.\n'
     'After:\n– Tệp hợp lệ được thêm vào danh sách chờ, chưa tải lên máy chủ.'),
    ('Bấm Lưu nháp / Lưu và gửi duyệt', 'Click',
     'Before:\n– Chống bấm nhiều lần: bỏ qua nếu đang có một lần lưu chưa xong.\n'
     '– Với Lưu và gửi duyệt: mở hộp xác nhận, chỉ tiếp tục khi người dùng đồng ý.\n'
     'During:\n'
     '– Chưa có hàng hoá nào → hiển thị “Bắt buộc phải có ít nhất 1 hàng hóa”.\n'
     '– Chưa chọn đơn vị tính → hiển thị “Bắt buộc chọn”.\n'
     '– Chưa chọn khách hàng → hiển thị “Bắt buộc chọn”.\n'
     '– Số lượng trống hoặc nhỏ hơn 1 → hiển thị “Không được nhỏ hơn 1”.\n'
     '– Số lượng vượt 999.999.999 → hiển thị “Tối đa 999999999”.\n'
     '– Chưa chọn ngày cần → hiển thị “Bắt buộc chọn”.\n'
     '– Ngày cần không lớn hơn hôm nay → hiển thị “Ngày cần hàng phải sau ngày hôm nay”.\n'
     '– Ghi chú dòng khách hàng trống → hiển thị “Bắt buộc nhập”.\n'
     '– Ghi chú vượt 255 ký tự → hiển thị “Vui lòng nhập tối đa 255 ký tự.”.\n'
     '– Chưa đính kèm tệp → hiển thị “Bắt buộc phải nhập”.\n'
     '– Tệp không phải PDF → hiển thị “File đính kèm phải là file PDF”.\n'
     '– Hàng hoá bị trùng → hiển thị “Hàng hóa bị trùng trong phiếu”.\n'
     '– Nếu có lỗi thì cuộn tới ô lỗi đầu tiên và KHÔNG thực hiện bước After.\n'
     'After:\n– Tải tệp đính kèm lên, ghi phiếu với trạng thái tương ứng, sinh mã tự động và '
     'ghi công ty / phòng ban / bộ phận theo hồ sơ người lập.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Nếu trạng thái là Chờ duyệt: gửi thông báo tới mọi người có quyền Kế toán kho cùng '
     'công ty với phiếu, nội dung “<Họ tên người lập> vừa tạo yêu cầu chuyển hàng: <mã phiếu>”.\n'
     '– Hiển thị thông báo “Yêu cầu của bạn đã được lưu. Bạn cần gửi để yêu cầu được xử lý” '
     '(lưu nháp) hoặc “Yêu cầu của bạn đã được gửi” (gửi duyệt), rồi quay về danh sách.'),
    ('Bấm Quay lại khi đã nhập dở', 'Click',
     'Before:\n– So sánh dữ liệu hiện tại với mốc lúc mở màn.\n'
     'After:\n– Có thay đổi → hiển thị hộp “Thông tin chưa lưu”; chọn Ở lại thì giữ nguyên, '
     'chọn Thoát thì rời màn và bỏ dữ liệu.\n'
     '– Không có thay đổi → về thẳng danh sách.'),
])

# ------------------------------------------------------ 2.6 FR-06
d.h3('2.6 Sửa phiếu yêu cầu chuyển hàng')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Sửa phiếu yêu cầu chuyển hàng', 'crud',
            [('include', 'Kiểm tra trạng thái Đang tạo và đúng người lập'),
             ('include', 'Chọn hàng hoá từ popup'),
             ('include', 'Chọn khách hàng từ popup'),
             ('extend', 'Xoá tệp đính kèm đã lưu')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-06 Sửa phiếu yêu cầu chuyển hàng')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Sửa phiếu yêu cầu chuyển hàng',
    mota='Cập nhật nội dung của một phiếu đang ở trạng thái Đang tạo do chính người đăng nhập '
         'lập. Có thể lưu tiếp ở dạng nháp hoặc gửi duyệt luôn.',
    tacnhan='%s (người lập chính phiếu đó)' % ACTOR_LAP,
    dieukien='Phiếu ở trạng thái Đang tạo VÀ do chính người đăng nhập lập.',
    chinh='1. Người dùng bấm nút Sửa trên dòng phiếu hoặc trên màn chi tiết.\n'
          '2. Hệ thống kiểm tra điều kiện sửa; không thoả thì từ chối và đưa về danh sách.\n'
          '3. Hệ thống mở màn Sửa, nạp đầy đủ thông tin chung, danh sách hàng hoá, dòng khách '
          'hàng và tệp đính kèm đã lưu.\n'
          '4. Người dùng chỉnh sửa và bấm Lưu nháp hoặc Lưu và gửi duyệt.\n'
          '5. Hệ thống kiểm tra dữ liệu, nối thêm tệp mới vào danh sách tệp cũ, ghi phiếu và '
          'cập nhật người sửa gần nhất.\n'
          '6. Hệ thống ghi lịch sử chỉnh sửa, và ghi riêng một dòng lịch sử thay đổi trạng '
          'thái nếu trạng thái đổi.\n'
          '7. Nếu chuyển sang Chờ duyệt, hệ thống gửi thông báo cho Kế toán kho cùng công ty.',
    phu='• Phiếu không còn ở trạng thái Đang tạo hoặc không phải của mình → từ chối với thông '
        'báo “Chỉ sửa được phiếu Đang tạo do chính bạn lập” và đưa về danh sách.\n'
        '• Xoá tệp đính kèm đã lưu → có hộp xác nhận, xoá có hiệu lực NGAY và vĩnh viễn, không '
        'chờ bấm Lưu.\n'
        '• Bấm Quay lại khi đã sửa dở → hỏi xác nhận rời trang.',
    dacbiet='Quy tắc Ngày cần hàng được nới khi sửa: dòng khách hàng cũ GIỮ NGUYÊN ngày cũ (kể '
            'cả ngày đã qua) thì bỏ qua kiểm tra; dòng mới thêm hoặc dòng vừa đổi ngày thì vẫn '
            'phải lớn hơn ngày hôm nay. Đây là khác biệt có chủ đích so với hệ thống cũ, nhằm '
            'giúp phiếu nháp để lâu vẫn sửa được. Khi sửa, tệp đính kèm KHÔNG bắt buộc chọn '
            'thêm; tệp cũ vẫn giữ nguyên.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa',
         shot=shot('26-sua-phieu.png'),
         shot_caption='Màn Sửa phiếu yêu cầu chuyển hàng với dữ liệu đã lưu')
d.figure(shot('27-xac-nhan-xoa-file.png'),
         'Hộp xác nhận xoá tệp đính kèm đã lưu', width_in=6.2)

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', '–', 'Sửa phiếu yêu cầu chuyển hàng',
     'Khác với màn Tạo mới ghi “Thêm phiếu yêu cầu chuyển hàng”.'),
    ('Ngày lập', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', '–', 'Ngày giờ lập phiếu gốc',
     'Không đổi theo lần sửa.'),
    ('Người lập', 'Text', 'Read-only', '–', '–', 'Người lập phiếu gốc',
     'Không đổi sang người đang sửa.'),
    ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Theo dữ liệu', '–'),
    ('Bảng hàng hoá', 'Table/Grid', 'Enable', '–', 'Có', 'Theo dữ liệu',
     'Thêm, sửa, xoá dòng hàng hoá và dòng khách hàng như màn Tạo mới.'),
    ('Ô Ngày cần của dòng cũ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Theo dữ liệu',
     'Giữ nguyên giá trị cũ thì hợp lệ kể cả ngày đã qua; đổi sang ngày khác thì phải lớn hơn '
     'hôm nay.'),
    ('Khối File đính kèm', 'Modal', 'Enable', 'Chỉ nhận tệp PDF', 'Không', 'Theo dữ liệu',
     'KHÔNG có dấu sao đỏ. Tệp mới nối thêm, không ghi đè tệp cũ.'),
    ('Nút xoá tệp đã lưu', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở hộp xác nhận; xác nhận thì xoá vĩnh viễn ngay, không chờ bấm Lưu.'),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Giữ phiếu ở trạng thái Đang tạo.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Có hộp xác nhận; chuyển phiếu sang Chờ duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Kiểm tra phiếu ở trạng thái Đang tạo và do chính người đăng nhập lập.\n'
     '– Nếu không thoả → hiển thị “Chỉ sửa được phiếu Đang tạo do chính bạn lập” và đưa về '
     'danh sách; nút Sửa cũng không được hiển thị trên giao diện.\n'
     'After:\n– Mở màn Sửa và nạp dữ liệu đã lưu, sau đó chốt mốc so sánh dữ liệu để cảnh báo '
     'chưa lưu không hiểu nhầm dữ liệu nạp về là người dùng vừa nhập.'),
    ('Bấm nút xoá tệp đính kèm đã lưu', 'Click',
     'Before:\n– Kiểm tra điều kiện sửa; không thoả thì từ chối.\n'
     '– Hiển thị hộp xác nhận nêu rõ tên tệp và cảnh báo xoá vĩnh viễn.\n'
     'During:\n– Tệp không thuộc phiếu này → báo lỗi và không xoá.\n'
     'After:\n– Xoá tệp khỏi kho lưu trữ và khỏi danh sách tệp của phiếu, cập nhật người sửa '
     'gần nhất.\n'
     '– Hiển thị thông báo “Xóa file thành công”.'),
    ('Bấm Lưu nháp / Lưu và gửi duyệt', 'Click',
     'Before:\n– Kiểm tra lại điều kiện sửa ở phía máy chủ.\n'
     'During:\n– Áp toàn bộ quy tắc kiểm tra như màn Tạo mới, riêng tệp đính kèm không bắt '
     'buộc và Ngày cần được nới theo quy tắc BR-06.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Ghi lại nội dung phiếu, nối thêm tệp mới, cập nhật người sửa gần nhất.\n'
     '– Ghi một dòng lịch sử chỉnh sửa; nếu trạng thái đổi thì ghi thêm một dòng lịch sử thay '
     'đổi trạng thái bằng TÊN trạng thái.\n'
     '– Nếu chuyển sang Chờ duyệt: gửi thông báo cho Kế toán kho cùng công ty.\n'
     '– Hiển thị thông báo thành công tương ứng và quay về danh sách.'),
])

# ------------------------------------------------------ 2.7 FR-07
d.h3('2.7 Chọn hàng hoá từ popup')

d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Chọn hàng hoá từ popup', 'crud',
            [('include', 'Tìm kiếm hàng hoá'),
             ('extend', 'Chặn hàng hoá đã có trong phiếu')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-07 Chọn hàng hoá từ popup')

d.p('2.7.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn '
           'Phiếu yêu cầu chuyển hàng tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Chọn hàng hoá từ popup',
    mota='Cửa sổ tìm và chọn hàng hoá để thêm vào bảng Danh sách hàng hóa của phiếu. Chọn được '
         'nhiều hàng trong một lần.',
    tacnhan='%s' % ACTOR_LAP,
    dieukien='Đang ở màn Tạo mới hoặc màn Sửa phiếu.',
    chinh='1. Người dùng bấm dấu cộng ở tiêu đề bảng hàng hoá.\n'
          '2. Hệ thống mở cửa sổ Thêm hàng hoá, hiển thị danh mục hàng hoá có phân trang.\n'
          '3. Người dùng tìm hàng cần thêm rồi tích chọn một hoặc nhiều dòng.\n'
          '4. Người dùng bấm nút Thêm N hàng hoá.\n'
          '5. Hệ thống thêm các hàng đã chọn vào bảng, chọn sẵn đơn vị tính đầu tiên, nạp giá '
          'niêm yết và tồn kho, tạo sẵn một dòng khách hàng trống cho từng hàng.\n'
          '6. Cửa sổ vẫn mở để chọn tiếp; người dùng bấm Đóng khi xong.',
    phu='• Hàng hoá đã có trong phiếu → cửa sổ đánh dấu và không cho chọn lại; nếu vẫn lọt thì '
        'hệ thống bỏ qua và báo “Hàng hóa đã có trong phiếu: ...”.\n'
        '• Bản ghi không phải hàng hoá thật trong danh mục (hàng tạm) → bị bỏ qua kèm cảnh báo '
        'phiếu chuyển hàng chỉ nhận hàng hoá có trong danh mục.\n'
        '• Không tìm thấy hàng nào → danh sách rỗng, không báo lỗi.',
    dacbiet='Cửa sổ KHÔNG có đường tạo hàng tạm — phiếu yêu cầu chuyển hàng chỉ nhận hàng hoá '
            'có thật trong danh mục.')

d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới / Sửa => Thêm hàng hoá',
         note='Cửa sổ Thêm hàng hoá được mở ngay trên màn Tạo mới hoặc màn Sửa phiếu.',
         shot=shot('07-popup-hang-hoa.png'),
         shot_caption='Cửa sổ Thêm hàng hoá')

d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh hàng hoá', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Dòng gợi ý “Nhập tên, mã hoặc model hàng hoá...”. Bấm Tìm kiếm để áp dụng.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở thêm các ô lọc chi tiết của danh mục hàng hoá.'),
    ('Ô tích chọn dòng', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Bỏ tích',
     'Bị vô hiệu với hàng đã có trong phiếu.'),
    ('Bảng danh mục hàng hoá', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Hiển thị ảnh, loại hàng, tên, model, mã hàng, giá niêm yết, bảo hành và các cột tồn kho.'),
    ('Nút Thêm N hàng hoá', 'Button', 'Enable / Disable', '–', '–', 'Thêm 0 hàng hoá',
     'N cập nhật theo số dòng đang tích. Bị vô hiệu khi chưa tích dòng nào.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đóng cửa sổ; các hàng đã thêm vẫn giữ nguyên trên bảng.'),
    ('Phân trang của cửa sổ', 'Pagination', 'Enable', '–', '–', 'Trang 1, cỡ 20',
     'Chuyển trang không làm mất các dòng đã tích.'),
])

d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm dấu cộng ở tiêu đề bảng hàng hoá', 'Click',
     'After:\n– Mở cửa sổ Thêm hàng hoá và truyền danh sách hàng đang có trên phiếu để cửa sổ '
     'tự chặn trùng.'),
    ('Bấm Thêm N hàng hoá', 'Click',
     'During:\n– Bỏ qua bản ghi không phải hàng hoá thật, kèm cảnh báo.\n'
     '– Bỏ qua hàng đã có trong phiếu, kèm cảnh báo “Hàng hóa đã có trong phiếu: ...”.\n'
     'After:\n– Thêm các hàng hợp lệ vào bảng, nạp đơn vị tính và giá theo đơn vị, nạp tồn kho '
     'theo kho đang chọn, tạo sẵn một dòng khách hàng trống.\n'
     '– Giữ cửa sổ mở để tiếp tục chọn.'),
])

# ------------------------------------------------------ 2.8 FR-08
d.h3('2.8 Chọn khách hàng từ popup')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Chọn khách hàng từ popup', 'crud',
            [('include', 'Tìm kiếm khách hàng')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-08 Chọn khách hàng từ popup')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn '
           'Phiếu yêu cầu chuyển hàng tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Chọn khách hàng cho dòng khách hàng cần hàng',
    mota='Cửa sổ tìm và chọn MỘT khách hàng để gán vào một dòng khách hàng của hàng hoá đang '
         'nhập.',
    tacnhan='%s' % ACTOR_LAP,
    dieukien='Đang ở màn Tạo mới hoặc màn Sửa phiếu, đã có ít nhất một dòng hàng hoá.',
    chinh='1. Người dùng bấm vào ô Khách hàng của dòng cần nhập.\n'
          '2. Hệ thống mở cửa sổ Chọn khách hàng với danh sách khách hàng có phân trang.\n'
          '3. Người dùng tìm theo tên / mã khách hàng, mã số thuế hoặc số điện thoại.\n'
          '4. Người dùng bấm vào dòng khách hàng cần chọn.\n'
          '5. Cửa sổ tự đóng và điền khách hàng vào đúng dòng đã mở.',
    phu='• Không tìm thấy khách hàng → danh sách rỗng, không báo lỗi.\n'
        '• Bấm Đóng → cửa sổ đóng, ô Khách hàng giữ nguyên giá trị cũ.',
    dacbiet='Cửa sổ này KHÔNG có đường thêm nhanh khách hàng mới. Cùng một khách hàng được '
            'phép xuất hiện ở nhiều dòng của cùng một hàng hoá.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới / Sửa => Chọn khách hàng',
         note='Cửa sổ Chọn khách hàng được mở ngay trên màn Tạo mới hoặc màn Sửa phiếu.',
         shot=shot('09-popup-khach-hang.png'),
         shot_caption='Cửa sổ Chọn khách hàng')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô Tên / Mã khách hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo tên hoặc mã khách hàng.'),
    ('Ô Mã số thuế', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Ô Số điện thoại', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp các điều kiện đã nhập.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá điều kiện tìm.'),
    ('Bảng danh sách khách hàng', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu',
     'Cột: STT, Mã KH - Tên khách hàng, Loại, Mã số thuế, Số điện thoại, Email, Nhóm KH, '
     'Địa chỉ. Bấm vào dòng để chọn.'),
    ('Phân trang của cửa sổ', 'Pagination', 'Enable', '–', '–', 'Trang 1, cỡ 10', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không chọn gì.'),
])

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm vào ô Khách hàng của dòng con', 'Click',
     'Before:\n– Ghi nhớ vị trí dòng đang mở để điền đúng chỗ khi chọn xong.\n'
     'After:\n– Mở cửa sổ Chọn khách hàng.'),
    ('Bấm vào một dòng khách hàng', 'Click',
     'After:\n– Điền mã và tên khách hàng vào ô của đúng dòng đã mở.\n'
     '– Tự đóng cửa sổ.\n'
     '– Nếu ô đang báo lỗi thiếu khách hàng thì lỗi tự biến mất.'),
])

# ------------------------------------------------------ 2.9 FR-09
d.h3('2.9 Xem chi tiết phiếu')

d.p('2.9.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Phiếu yêu '
           'cầu chuyển hàng tại phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu yêu cầu chuyển hàng',
    mota='Hiển thị toàn bộ nội dung một phiếu ở chế độ chỉ đọc: thông tin chung, tệp đính kèm, '
         'danh sách hàng hoá kèm các dòng khách hàng, ghi chú duyệt và các nút thao tác phù '
         'hợp với trạng thái và quyền của người xem.',
    tacnhan='%s; %s' % (ACTOR_LAP, ACTOR_KTK),
    dieukien='Người xem là người lập phiếu, hoặc là quản trị hệ thống, hoặc có quyền Kế toán '
             'kho và cùng công ty với phiếu.',
    chinh='1. Người dùng bấm vào mã yêu cầu trên danh sách (hoặc mở từ thông báo).\n'
          '2. Hệ thống nạp phiếu kèm hàng hoá, dòng khách hàng, tệp đính kèm và người liên quan.\n'
          '3. Hệ thống kiểm tra quyền xem phiếu.\n'
          '4. Hệ thống hiển thị nội dung phiếu và bộ nút phù hợp với trạng thái và quyền.',
    phu='• Không đủ quyền xem → từ chối với thông báo “Bạn không có quyền xem phiếu này” và '
        'đưa về danh sách.\n'
        '• Mã phiếu không tồn tại → báo không tìm thấy dữ liệu và đưa về danh sách.\n'
        '• Phiếu không có tệp đính kèm → hiển thị “Không có file đính kèm.”',
    dacbiet=None)

d.p('2.9.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết',
         shot=shot('15-chi-tiet.png'),
         shot_caption='Màn chi tiết phiếu Chờ duyệt, xem bằng tài khoản có quyền Kế toán kho')
d.figure(shot('28-chi-tiet-phieu-nhap.png'),
         'Màn chi tiết phiếu nháp của chính người xem — chỉ có Sửa, In, Quay lại',
         width_in=6.2)

d.p('2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu yêu cầu chuyển hàng · <mã phiếu>',
     'Kèm nhãn trạng thái ở góc phải.'),
    ('Mã yêu cầu', 'Text', 'Read-only', 'PYCCH-xxxxx', 'Theo dữ liệu', '–'),
    ('Ngày lập', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', '–'),
    ('Người lập', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Người tiếp nhận', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Hiển thị dạng “Họ tên · ngày giờ tiếp nhận”. Chưa có thì hiện dấu gạch ngang.'),
    ('Ghi chú', 'Text', 'Read-only', '0–255 ký tự', 'Theo dữ liệu',
     'Trống thì hiện dấu gạch ngang.'),
    ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Bấm tên tệp mở ở tab mới. Không có nút xoá ở màn này.'),
    ('Bảng hàng hoá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cột STT, Hàng hóa, ĐVT, Giá niêm yết, SL cần.'),
    ('Bảng con khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cột Khách hàng, SL cần, Ngày cần, Ghi chú.'),
    ('Cột Được nhận', 'Table/Grid', 'Read-only', '≥ 0', 'Ẩn',
     'CHỈ hiển thị khi phiếu ở trạng thái Đã phân bổ.'),
    ('Khối Ghi chú duyệt', 'Textarea', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Hiện ô nhập kèm dấu sao đỏ khi người xem được phép Không duyệt; hiện chỉ đọc khi phiếu '
     'đã có lý do từ chối; ẩn hẳn nếu không thuộc hai trường hợp trên.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu Đang tạo do chính người xem lập.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Luôn hiện với người xem được phiếu.'),
    ('Nút Không duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu Chờ duyệt, người xem có quyền Kế toán kho và cùng công ty.'),
    ('Nút Tổng hợp', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Cùng điều kiện với nút Không duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị',
     'Về danh sách, giữ nguyên bộ lọc đang lưu.'),
], required=False)

d.p('2.9.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Nạp phiếu kèm hàng hoá, dòng khách hàng, tệp đính kèm và người liên quan.\n'
     '– Kiểm tra quyền xem: là người lập, hoặc là quản trị hệ thống, hoặc có quyền Kế toán kho '
     'và cùng công ty với phiếu.\n'
     '– Không đủ quyền → hiển thị “Bạn không có quyền xem phiếu này” và đưa về danh sách.\n'
     'After:\n– Hiển thị nội dung phiếu và tính các cờ quyết định nút Sửa, Không duyệt, '
     'Tổng hợp.'),
    ('Bấm tên tệp đính kèm', 'Click', 'After:\n– Mở tệp ở tab mới.'),
    ('Bấm nút Quay lại', 'Click',
     'After:\n– Về màn danh sách; bộ lọc đã lưu trong 10 phút được khôi phục.'),
])

# ------------------------------------------------------ 2.10 FR-10
d.h3('2.10 Xóa phiếu')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu yêu cầu chuyển hàng', 'action',
            [('include', 'Kiểm tra trạng thái Đang tạo và đúng người lập'),
             ('include', 'Xoá kèm hàng hoá và dòng khách hàng')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu yêu cầu chuyển hàng')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Chỉ bổ sung các quy tắc riêng của màn Phiếu yêu cầu '
           'chuyển hàng tại phần mô tả chi tiết.', anchor='notice')
d.intro_table(
    ten='Xóa phiếu yêu cầu chuyển hàng',
    mota='Xoá vĩnh viễn một phiếu đang ở trạng thái Đang tạo do chính người đăng nhập lập, '
         'kèm toàn bộ dòng hàng hoá và dòng khách hàng của phiếu.',
    tacnhan='%s (người lập chính phiếu đó)' % ACTOR_LAP,
    dieukien='Phiếu ở trạng thái Đang tạo VÀ do chính người đăng nhập lập.',
    chinh='1. Người dùng bấm nút Xóa trên dòng phiếu.\n'
          '2. Hệ thống mở hộp xác nhận nêu rõ mã phiếu.\n'
          '3. Người dùng bấm Xóa để xác nhận.\n'
          '4. Hệ thống kiểm tra lại điều kiện xoá, ghi một dòng lịch sử xoá rồi xoá phiếu cùng '
          'toàn bộ dòng hàng hoá và dòng khách hàng trong một giao dịch duy nhất.\n'
          '5. Hệ thống hiển thị thông báo “Xóa thành công” và nạp lại danh sách.',
    phu='• Không thoả điều kiện xoá → từ chối với thông báo “Chỉ xóa được phiếu Đang tạo do '
        'chính bạn lập”; hệ thống tự nạp lại danh sách cho khớp hiện trạng.\n'
        '• Phiếu đã bị xoá ở nơi khác → báo dữ liệu không còn và nạp lại danh sách.\n'
        '• Bấm Hủy ở hộp xác nhận → không xoá gì.',
    dacbiet='Đây là xoá thật, không phải chuyển vào thùng rác — không khôi phục lại được. Mã '
            'phiếu đã dùng không được cấp lại cho phiếu mới.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa',
         note='Hộp xác nhận xoá được mở ngay trên màn hình danh sách theo đường dẫn ở trên.',
         shot=shot('29-xac-nhan-xoa.png'),
         shot_caption='Hộp xác nhận xoá phiếu')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa',
     'Cố định.'),
    ('Nội dung hộp thoại', 'Label', 'Hiển thị',
     'Bạn có chắc muốn xóa phiếu yêu cầu chuyển hàng "<mã phiếu>"?',
     'Có nêu rõ mã phiếu sẽ bị xoá.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xoá.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xoá.'),
    ('Nút Xóa trên dòng', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu Đang tạo do chính người xem lập.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu ở trạng thái Đang tạo và do chính người đăng nhập '
     'lập.\n'
     'After:\n– Mở hộp xác nhận có nêu mã phiếu.'),
    ('Bấm Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra lại ở phía máy chủ: phiếu ở trạng thái Đang tạo và do chính người '
     'đăng nhập lập.\n'
     '– Không thoả → hiển thị “Chỉ xóa được phiếu Đang tạo do chính bạn lập” và dừng xử lý.\n'
     'After:\n– Ghi một dòng lịch sử xoá.\n'
     '– Xoá phiếu cùng toàn bộ dòng hàng hoá và dòng khách hàng trong một giao dịch duy nhất.\n'
     '– Hiển thị thông báo “Xóa thành công” và nạp lại danh sách.'),
])

# ------------------------------------------------------ 2.11 FR-11
d.h3('2.11 Không duyệt phiếu')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Không duyệt phiếu', 'action',
            [('include', 'Kiểm tra quyền Kế toán kho, trạng thái Chờ duyệt và cùng công ty'),
             ('include', 'Nhập ghi chú duyệt'),
             ('extend', 'Gửi thông báo cho người lập phiếu')],
            actor=ACTOR_KTK,
            caption='Biểu đồ Use Case — FR-11 Không duyệt phiếu')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa, Validate dữ liệu. Chỉ bổ sung các quy tắc riêng của '
           'màn Phiếu yêu cầu chuyển hàng tại phần mô tả chi tiết.', anchor='notice')
d.intro_table(
    ten='Không duyệt phiếu yêu cầu chuyển hàng',
    mota='Kế toán kho từ chối một phiếu đang Chờ duyệt kèm lý do, đưa phiếu trở về trạng thái '
         'Đang tạo để người lập sửa và gửi lại.',
    tacnhan='%s' % ACTOR_KTK,
    dieukien='Người dùng có quyền Kế toán kho (hoặc là quản trị hệ thống), phiếu ở trạng thái '
             'Chờ duyệt và thuộc cùng công ty với người dùng.',
    chinh='1. Người dùng mở màn chi tiết của phiếu đang Chờ duyệt.\n'
          '2. Người dùng nhập lý do vào khối Ghi chú duyệt.\n'
          '3. Người dùng bấm nút Không duyệt.\n'
          '4. Hệ thống mở hộp xác nhận nêu rõ mã phiếu và hệ quả.\n'
          '5. Người dùng xác nhận.\n'
          '6. Hệ thống kiểm tra quyền, ghi trạng thái Đang tạo, ghi lý do, ghi người tiếp nhận '
          'và thời điểm tiếp nhận.\n'
          '7. Hệ thống gửi thông báo cho người lập phiếu và hiển thị thông báo thành công.',
    phu='• Ghi chú duyệt để trống → không mở hộp xác nhận, hiển thị lỗi đỏ “Vui lòng nhập ghi '
        'chú duyệt” dưới ô nhập.\n'
        '• Không đủ điều kiện (thiếu quyền, phiếu không ở trạng thái Chờ duyệt, khác công ty) '
        '→ từ chối với thông báo “Bạn không có quyền thực hiện thao tác này”.\n'
        '• Người khác vừa xử lý phiếu trước → thao tác bị từ chối vì phiếu không còn ở trạng '
        'thái Chờ duyệt.\n'
        '• Bấm nút nhiều lần liên tiếp → chỉ ghi nhận một lần.\n'
        '• Lỗi gửi thông báo → KHÔNG làm hỏng thao tác không duyệt.',
    dacbiet='Không duyệt KHÔNG phải hủy phiếu. Ghi chú duyệt của lần từ chối trước vẫn được '
            'giữ trên phiếu sau khi người lập gửi lại.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Không duyệt',
         note='Hộp xác nhận được mở ngay trên màn chi tiết theo đường dẫn ở trên.',
         shot=shot('17-xac-nhan-khong-duyet.png'),
         shot_caption='Hộp xác nhận không duyệt')
d.figure(shot('16-loi-ghi-chu-duyet.png'),
         'Lỗi “Vui lòng nhập ghi chú duyệt” khi bấm Không duyệt lúc ô còn trống',
         width_in=6.2)

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Khối Ghi chú duyệt', 'Textarea', 'Enable / Ẩn', '–', 'Có', 'Trống',
     'Có dấu sao đỏ. Dòng gợi ý “Nhập ghi chú duyệt (bắt buộc khi Không duyệt)”. Chỉ hiện khi '
     'đủ điều kiện không duyệt.'),
    ('Lỗi inline của Ghi chú duyệt', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chỉ hiện sau lần bấm Không duyệt đầu tiên; tự biến mất khi người dùng gõ nội dung.'),
    ('Nút Không duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện',
     'Mở hộp xác nhận khi ghi chú duyệt đã hợp lệ.'),
    ('Hộp xác nhận không duyệt', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Nội dung nêu mã phiếu và câu “Phiếu sẽ chuyển về trạng thái Đang tạo để người lập sửa '
     'lại”; có hai nút Không duyệt và Hủy.'),
])

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Không duyệt', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu ở trạng thái Chờ duyệt, người dùng có quyền Kế '
     'toán kho hoặc là quản trị hệ thống, và cùng công ty với phiếu.\n'
     'During:\n– Ghi chú duyệt trống → hiển thị “Vui lòng nhập ghi chú duyệt”, không mở hộp '
     'xác nhận và không thực hiện bước After.\n'
     'After:\n– Mở hộp xác nhận nêu mã phiếu và hệ quả.'),
    ('Xác nhận Không duyệt', 'Click',
     'Before:\n– Chống bấm nhiều lần: bỏ qua nếu đang có một lần xử lý chưa xong.\n'
     '– Kiểm tra lại ở phía máy chủ: phiếu ở trạng thái Chờ duyệt, người dùng có quyền và cùng '
     'công ty. Không thoả → hiển thị “Bạn không có quyền thực hiện thao tác này” và dừng xử lý.\n'
     'During:\n– Ghi chú duyệt trống ở phía máy chủ → hiển thị “Vui lòng nhập ghi chú duyệt”.\n'
     'After:\n– Chuyển phiếu về trạng thái Đang tạo, ghi lý do, ghi người tiếp nhận là người '
     'thực hiện và thời điểm tiếp nhận là thời điểm hiện tại.\n'
     '– Ghi một dòng lịch sử thay đổi trạng thái.\n'
     '– Gửi thông báo cho người lập phiếu với nội dung “<Họ tên người từ chối> vừa từ chối yêu '
     'cầu chuyển hàng: <mã phiếu>”; lỗi gửi thông báo không làm hỏng thao tác.\n'
     '– Hiển thị thông báo “Đã từ chối yêu cầu chuyển hàng”.'),
])

# ------------------------------------------------------ 2.12 FR-12
d.h3('2.12 Tổng hợp sang phiếu đề nghị xuất hàng')

d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Tổng hợp sang phiếu đề nghị xuất hàng', 'action',
            [('include', 'Kiểm tra quyền Kế toán kho, trạng thái Chờ duyệt và cùng công ty')],
            actor=ACTOR_KTK,
            caption='Biểu đồ Use Case — FR-12 Tổng hợp sang phiếu đề nghị xuất hàng')

d.p('2.12.2 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Phiếu yêu '
           'cầu chuyển hàng tại phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='Tổng hợp phiếu sang màn lập phiếu đề nghị xuất hàng',
    mota='Mở màn lập phiếu đề nghị xuất hàng của hệ thống cũ ở tab mới, mang sẵn phiếu đang '
         'xem, để bộ phận kho gom vào lệnh xuất.',
    tacnhan='%s' % ACTOR_KTK,
    dieukien='Người dùng có quyền Kế toán kho (hoặc là quản trị hệ thống), phiếu ở trạng thái '
             'Chờ duyệt và thuộc cùng công ty với người dùng.',
    chinh='1. Người dùng bấm nút Tổng hợp trên màn chi tiết, hoặc nút Tổng hợp trên dòng của '
          'màn danh sách.\n'
          '2. Hệ thống mở tab mới trỏ sang màn lập phiếu đề nghị xuất hàng, mang sẵn phiếu '
          'đang xem.\n'
          '3. Người dùng hoàn tất thao tác ở màn bên kia.',
    phu='• Không đủ điều kiện → nút không hiển thị.\n'
        '• Trình duyệt chặn mở tab mới → người dùng cần cho phép mở tab từ hệ thống.',
    dacbiet='Thao tác này KHÔNG làm đổi trạng thái phiếu. Trạng thái chỉ đổi khi bộ phận kho '
            'hoàn tất nghiệp vụ của họ ở màn bên kia.')

d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Tổng hợp',
         note='Nút Tổng hợp nằm ở thanh nút cuối màn chi tiết và ở cột Hành động của màn danh '
              'sách.',
         shot=shot('15-chi-tiet.png'),
         shot_caption='Nút Tổng hợp trên thanh nút cuối màn chi tiết')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Tổng hợp trên màn chi tiết', 'Button', 'Enable / Ẩn',
     'Ẩn khi không đủ điều kiện',
     'Nằm sau nút Không duyệt theo thứ tự nút cố định của thanh nút cuối màn.'),
    ('Nút Tổng hợp trên dòng danh sách', 'Icon Button', 'Enable / Ẩn',
     'Ẩn khi không đủ điều kiện',
     'Biểu tượng dấu tích kép, cùng điều kiện hiển thị với nút trên màn chi tiết.'),
], required=False, scope=False)

d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tổng hợp', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu ở trạng thái Chờ duyệt, người dùng có quyền Kế '
     'toán kho hoặc là quản trị hệ thống, và cùng công ty với phiếu.\n'
     'After:\n– Mở tab mới trỏ sang màn lập phiếu đề nghị xuất hàng của hệ thống cũ, mang sẵn '
     'phiếu đang xem.\n'
     '– Tab hiện tại giữ nguyên; phiếu không đổi trạng thái và không phát sinh lịch sử.'),
])

# ------------------------------------------------------ 2.13 FR-13
d.h3('2.13 In phiếu')

d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'In phiếu yêu cầu chuyển hàng', 'io',
            [('include', 'Kiểm tra quyền xem phiếu'),
             ('include', 'Lấy ảnh tiêu đề thư theo công ty ghi trên phiếu')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-13 In phiếu yêu cầu chuyển hàng')

d.p('2.13.2 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Phiếu yêu '
           'cầu chuyển hàng tại phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='In phiếu yêu cầu chuyển hàng',
    mota='Mở bản in của phiếu ở tab mới theo mẫu in của hệ thống, kèm ảnh tiêu đề thư của công '
         'ty ghi trên phiếu.',
    tacnhan='%s; %s' % (ACTOR_LAP, ACTOR_KTK),
    dieukien='Người dùng xem được phiếu (theo điều kiện của chức năng Xem chi tiết).',
    chinh='1. Người dùng bấm nút In trên màn chi tiết hoặc trên dòng của màn danh sách.\n'
          '2. Hệ thống mở tab mới trỏ tới trang in của phiếu.\n'
          '3. Hệ thống kiểm tra quyền xem, lấy mẫu in và điền dữ liệu phiếu vào mẫu.\n'
          '4. Hệ thống thay khối tiêu đề mặc định của mẫu bằng ảnh tiêu đề thư của công ty ghi '
          'trên phiếu.\n'
          '5. Trang in hiển thị; người dùng bấm nút In để mở hộp thoại in của trình duyệt.',
    phu='• Không đủ quyền xem → từ chối với thông báo “Bạn không có quyền xem phiếu này”.\n'
        '• Không tìm thấy mẫu in → báo lỗi không tìm thấy mẫu in, không hiển thị trang trắng.\n'
        '• Công ty chưa cấu hình ảnh tiêu đề thư → giữ khối tiêu đề mặc định của mẫu, bản in '
        'không bị vỡ.',
    dacbiet='Ảnh tiêu đề thư lấy theo CÔNG TY GHI TRÊN PHIẾU, không phải công ty của người '
            'đang in và cũng không phải công ty của người tạo phiếu. Bản in KHÔNG có cột Giá '
            'niêm yết. In phiếu không làm đổi trạng thái, người cập nhật hay lịch sử.')

d.p('2.13.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In',
         shot=shot('18-man-in.png'),
         shot_caption='Bản in phiếu yêu cầu chuyển hàng')

d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ảnh tiêu đề thư', 'Icon Button', 'Hiển thị', '–', 'Theo công ty ghi trên phiếu',
     'Chiếm hết chiều ngang trang in.'),
    ('Tiêu đề bản in', 'Label', 'Hiển thị', 'PHIẾU YÊU CẦU CHUYỂN HÀNG', 'Cố định', '–'),
    ('Dòng số phiếu', 'Label', 'Hiển thị', 'No: <mã phiếu>', 'Theo dữ liệu', '–'),
    ('Ngày yêu cầu / Người yêu cầu', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Lấy từ Ngày lập và Người lập của phiếu.'),
    ('Bảng nội dung', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cột STT, Hàng hóa (tên và mã), ĐVT, SL và nhóm cột Chi tiết gồm Khách hàng, SL, Ngày '
     'cần, Ghi chú. KHÔNG có cột Giá niêm yết.'),
    ('Ô ký cuối trang', 'Label', 'Hiển thị', '–', 'Người lập phiếu / Giám đốc công ty',
     'Dưới ô Người lập phiếu có sẵn họ tên người lập.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
     'Nằm ở góc trên bên phải trang in, mở hộp thoại in của trình duyệt.'),
], required=False)

d.p('2.13.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In', 'Click',
     'After:\n– Mở tab mới trỏ tới trang in của phiếu.'),
    ('Mở trang in', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu như chức năng Xem chi tiết; không đủ quyền → hiển '
     'thị “Bạn không có quyền xem phiếu này”.\n'
     'During:\n– Lấy mẫu in và điền dữ liệu phiếu vào mẫu.\n'
     '– Xác định công ty ghi trên phiếu và lấy ảnh tiêu đề thư của công ty đó; nếu công ty '
     'chưa cấu hình ảnh thì giữ khối tiêu đề mặc định của mẫu.\n'
     '– Không tìm thấy mẫu in → báo lỗi, không hiển thị trang trắng.\n'
     'After:\n– Hiển thị bản in đã điền dữ liệu; không ghi bất kỳ thay đổi nào lên phiếu.'),
])

# ------------------------------------------------------ 2.14 FR-14
d.h3('2.14 Xem lịch sử thay đổi')

d.p('2.14.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Phiếu yêu cầu chuyển '
           'hàng tại phần mô tả chi tiết.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Hiển thị các mốc thay đổi của một phiếu: tạo mới, chỉnh sửa từng trường và thay đổi '
         'trạng thái, kèm người thực hiện và thời điểm.',
    tacnhan='%s; %s' % (ACTOR_LAP, ACTOR_KTK),
    dieukien='Người dùng nhìn thấy phiếu trên danh sách.',
    chinh='1. Người dùng bấm nút Lịch sử trên dòng phiếu (với phiếu nháp thì nút nằm trong '
          'menu ba chấm).\n'
          '2. Hệ thống mở cửa sổ Lịch sử thay đổi và nạp các mốc của phiếu.\n'
          '3. Cửa sổ hiển thị từng mốc kèm thời điểm, loại thao tác, người thực hiện và các '
          'trường thay đổi.\n'
          '4. Người dùng có thể lọc theo nhóm thao tác hoặc bấm Đóng để trở về.',
    phu='• Phiếu mới tạo chưa sửa lần nào → chỉ có một mốc “Tạo mới”.\n'
        '• Không có mốc nào khớp bộ lọc trong cửa sổ → hiển thị danh sách rỗng.',
    dacbiet=None)

d.p('2.14.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử',
         note='Cửa sổ Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở '
              'trên.',
         shot=shot('19-lich-su.png'),
         shot_caption='Cửa sổ Lịch sử thay đổi của một phiếu')

d.p('2.14.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi', '–'),
    ('Phụ đề', 'Label', 'Hiển thị', '–', 'Phiếu yêu cầu: <mã phiếu>', '–'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc các mốc theo nhóm thao tác.'),
    ('Danh sách mốc lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi mốc gồm thời điểm, loại thao tác, dòng “Người thực hiện: Họ tên — Phòng ban” và các '
     'trường thay đổi kèm giá trị cũ, giá trị mới.'),
    ('Thay đổi trạng thái', 'Label', 'Read-only', 'Danh sách 13 giá trị', 'Theo dữ liệu',
     'Ghi bằng TÊN trạng thái, ví dụ “Đang tạo” chuyển thành “Chờ duyệt”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị',
     'Đóng cửa sổ, danh sách phía sau giữ nguyên trang và bộ lọc.'),
], required=False)

d.p('2.14.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lịch sử', 'Click',
     'After:\n– Mở cửa sổ Lịch sử thay đổi và nạp các mốc của đúng phiếu đó.'),
    ('Chọn nhóm thao tác trong Bộ lọc', 'Change',
     'After:\n– Lọc lại danh sách mốc theo nhóm đã chọn; bỏ lọc thì hiển thị đầy đủ.'),
])

# ========================================================= PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('Các quy tắc chung về danh sách, tìm kiếm, validate, thông báo và ghi lịch sử. '
           'Bảng dưới đây chỉ liệt kê các quy tắc ĐẶC THÙ của màn Phiếu yêu cầu chuyển hàng.',
           anchor='list', head='Quy tắc áp dụng', lead='')
d.rule_table([
    ('BR-01', 'Phạm vi dữ liệu bốn cấp',
     ['– Cấp quyền xem được xét theo thứ tự ưu tiên V1 → V2 → V3 → V4; có cấp nào trước thì áp '
      'cấp đó, không cộng dồn.',
      '– V3 và V4 cộng thêm mọi phiếu do chính người dùng lập, kể cả phiếu ngoài phạm vi quản '
      'lý.',
      '– Không có cấp nào: chỉ phiếu do chính mình lập.',
      '– Quản trị hệ thống được xử lý tương đương V1.',
      '– Người có V2 nhưng chưa xác định được công ty thì phạm vi là RỖNG, KHÔNG trả về các '
      'phiếu chưa có công ty.'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),

    ('BR-02', 'Luôn ẩn phiếu nháp của người khác',
     ['– Phiếu ở trạng thái Đang tạo của người khác luôn bị loại khỏi kết quả, áp dụng SAU CÙNG '
      'sau mọi điều kiện lọc và mọi cấp quyền.',
      '– Không bộ lọc nào, không tham số nào trên đường dẫn gỡ được quy tắc này.'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),

    ('BR-03', 'Điều kiện xem chi tiết một phiếu',
     ['– Xem được khi: là người lập phiếu, HOẶC là quản trị hệ thống, HOẶC có quyền Kế toán kho '
      'và cùng công ty với phiếu.',
      '– Không thoả → từ chối với thông báo “Bạn không có quyền xem phiếu này”.',
      '– Quy tắc áp dụng cả với trang in.'],
     ['Xem chi tiết', 'In phiếu']),

    ('BR-04', 'Điều kiện sửa và xóa phiếu',
     ['– Chỉ sửa và xóa được phiếu ở trạng thái Đang tạo VÀ do chính người đăng nhập lập.',
      '– Thiếu một trong hai điều kiện thì nút không hiển thị; gọi thẳng chức năng bỏ qua giao '
      'diện cũng bị từ chối với thông báo “Chỉ sửa được phiếu Đang tạo do chính bạn lập” hoặc '
      '“Chỉ xóa được phiếu Đang tạo do chính bạn lập”.',
      '– Xóa phiếu xóa kèm toàn bộ dòng hàng hoá và dòng khách hàng trong một giao dịch duy '
      'nhất; không khôi phục lại được.'],
     ['Sửa phiếu', 'Xóa phiếu']),

    ('BR-05', 'Điều kiện Không duyệt và Tổng hợp',
     ['– Chỉ thực hiện được khi thoả ĐỒNG THỜI ba điều kiện: phiếu ở trạng thái Chờ duyệt; '
      'người dùng có quyền Kế toán kho hoặc là quản trị hệ thống; phiếu cùng công ty với người '
      'dùng.',
      '– Quản trị hệ thống chỉ thay thế vế QUYỀN — điều kiện cùng công ty vẫn phải thoả.',
      '– Ghi chú duyệt là bắt buộc khi Không duyệt; để trống thì báo “Vui lòng nhập ghi chú '
      'duyệt”.',
      '– Không duyệt đưa phiếu về trạng thái Đang tạo, KHÔNG phải hủy phiếu.'],
     ['Không duyệt phiếu', 'Tổng hợp']),

    ('BR-06', 'Ngày cần hàng',
     ['– Khi tạo mới: mọi dòng khách hàng phải có ngày cần LỚN HƠN ngày hôm nay.',
      '– Khi sửa: dòng khách hàng cũ GIỮ NGUYÊN ngày cũ (kể cả ngày đã qua) thì bỏ qua kiểm '
      'tra; dòng mới thêm hoặc dòng vừa đổi ngày thì vẫn phải lớn hơn ngày hôm nay.',
      '– Vi phạm thì báo “Ngày cần hàng phải sau ngày hôm nay”.',
      '– Đây là khác biệt CÓ CHỦ ĐÍCH so với hệ thống cũ (hệ thống cũ kiểm tra lại tất cả các '
      'dòng khi sửa, khiến phiếu nháp để lâu không sửa được).'],
     ['Tạo mới phiếu', 'Sửa phiếu']),

    ('BR-07', 'Cấu trúc hàng hoá và khách hàng của phiếu',
     ['– Phiếu phải có ít nhất một dòng hàng hoá.',
      '– Mỗi mã hàng chỉ được xuất hiện MỘT lần trong cùng một phiếu; trùng thì báo “Hàng hóa '
      'bị trùng trong phiếu”.',
      '– Mỗi dòng hàng hoá phải có ít nhất một dòng khách hàng; không xoá được dòng khách hàng '
      'cuối cùng.',
      '– Cùng một khách hàng ĐƯỢC PHÉP xuất hiện nhiều dòng trong cùng một hàng hoá.',
      '– Chỉ nhận hàng hoá có thật trong danh mục; không nhận hàng tạm.'],
     ['Tạo mới phiếu', 'Sửa phiếu', 'Chọn hàng hoá từ popup']),

    ('BR-08', 'Tệp đính kèm',
     ['– Khi tạo mới: bắt buộc ít nhất một tệp PDF.',
      '– Khi sửa: KHÔNG bắt buộc chọn thêm tệp; tệp mới được nối thêm, không ghi đè tệp cũ.',
      '– Kiểm tra hai lớp ở phía giao diện: đúng đuôi .pdf và đúng nội dung PDF; tệp mang đuôi '
      '.pdf nhưng nội dung hỏng bị chặn ngay tại bước chọn.',
      '– Xoá tệp đã lưu có hiệu lực NGAY và vĩnh viễn (xoá cả trên kho lưu trữ), không chờ bấm '
      'nút Lưu; chỉ người đủ điều kiện sửa phiếu mới xoá được.'],
     ['Tạo mới phiếu', 'Sửa phiếu']),

    ('BR-09', 'Giá niêm yết và tồn kho chỉ để tham khảo',
     ['– Giá niêm yết và SL tồn đổi theo đơn vị tính đang chọn, chỉ hiển thị trên form.',
      '– Cả hai KHÔNG được lưu vào phiếu và KHÔNG xuất hiện trên bản in.',
      '– Hệ thống KHÔNG chặn khi số lượng đề nghị vượt tồn, kể cả khi tồn bằng 0.',
      '– Chưa chọn kho ở ô Xem tồn theo kho thì SL tồn hiển thị dấu gạch ngang và không truy '
      'vấn tồn.'],
     ['Tạo mới phiếu', 'Sửa phiếu']),

    ('BR-10', 'Sinh mã phiếu và ghi cấp tổ chức',
     ['– Mã phiếu do hệ thống sinh tự động dạng PYCCH kèm 5 chữ số; người dùng không nhập được.',
      '– Mã đã dùng không được cấp lại, kể cả khi phiếu bị xoá.',
      '– Công ty, phòng ban và bộ phận của phiếu lấy theo hồ sơ của NGƯỜI LẬP tại thời điểm '
      'tạo, và không đổi khi người khác sửa phiếu.'],
     ['Tạo mới phiếu']),

    ('BR-11', 'Thông báo',
     ['– Gửi duyệt (lưu ở trạng thái Chờ duyệt, cả khi tạo mới lẫn khi sửa): gửi thông báo tới '
      'MỌI người có quyền Kế toán kho thuộc cùng công ty với phiếu, nội dung “<Họ tên người '
      'lập> vừa tạo yêu cầu chuyển hàng: <mã phiếu>”.',
      '– Không duyệt: gửi thông báo tới người lập phiếu, nội dung “<Họ tên người từ chối> vừa '
      'từ chối yêu cầu chuyển hàng: <mã phiếu>”.',
      '– Lưu nháp KHÔNG gửi thông báo cho ai.',
      '– Bấm vào thông báo mở đúng màn chi tiết của phiếu.',
      '– Lỗi gửi thông báo không được làm hỏng thao tác nghiệp vụ đã thực hiện.'],
     ['Tạo mới phiếu', 'Sửa phiếu', 'Không duyệt phiếu']),

    ('BR-12', 'Sắp xếp và bộ lọc của màn danh sách',
     ['– Chỉ ba cột sắp xếp được: Mã yêu cầu, Ngày tạo, Ngày tiếp nhận. Yêu cầu sắp xếp theo '
      'cột khác bị bỏ qua và danh sách trở về thứ tự mặc định (Ngày tạo giảm dần).',
      '– Ô tìm nhanh tìm theo mã yêu cầu HOẶC tên người tạo và chỉ chạy khi bấm nút Tìm kiếm.',
      '– Mọi ô lọc nâng cao tự truy vấn ngay khi giá trị thay đổi.',
      '– Mốc “Ngày tạo đến” lấy trọn ngày được chọn.',
      '– Bộ lọc và trạng thái đóng/mở của khối lọc nâng cao được ghi nhớ trong 10 phút.'],
     ['Xem danh sách', 'Tìm kiếm và lọc']),

    ('BR-13', 'Xuất Excel bám phạm vi và bộ lọc',
     ['– Tệp chứa TẤT CẢ phiếu khớp bộ lọc đang áp dụng, không giới hạn theo trang đang xem.',
      '– Tệp không bao giờ vượt phạm vi dữ liệu của người đăng nhập và vẫn loại phiếu nháp của '
      'người khác.',
      '– Thứ tự cột trong tệp chạy theo đúng thứ tự người dùng chọn ở cửa sổ Chọn trường xuất '
      'file.',
      '– Có đặt điều kiện ngày tạo thì tệp có thêm dòng tiêu đề khoảng ngày.'],
     ['Xuất Excel']),

    ('BR-14', 'Ảnh tiêu đề thư của bản in',
     ['– Ảnh tiêu đề thư lấy theo CÔNG TY GHI TRÊN PHIẾU, không lấy theo người tạo phiếu và '
      'càng không lấy theo người đang đăng nhập.',
      '– Công ty chưa cấu hình ảnh tiêu đề thư thì giữ khối tiêu đề mặc định của mẫu in, bản in '
      'không bị vỡ.',
      '– Bản in không có cột Giá niêm yết.'],
     ['In phiếu']),

    ('BR-15', 'Cột Được nhận của màn chi tiết',
     ['– Cột “Được nhận” trong bảng con khách hàng CHỈ hiển thị khi phiếu ở trạng thái Đã phân '
      'bổ.',
      '– Các trạng thái khác không có cột này.'],
     ['Xem chi tiết']),

    ('BR-16', 'Ghi lịch sử',
     ['– Ghi một dòng lịch sử khi: tạo mới phiếu, chỉnh sửa phiếu, thay đổi trạng thái và xoá '
      'phiếu.',
      '– Thay đổi trạng thái được tách thành dòng lịch sử riêng và ghi bằng TÊN trạng thái, '
      'không ghi giá trị mã.',
      '– Xem lịch sử không cần quyền riêng; ai nhìn thấy phiếu thì xem được lịch sử của phiếu '
      'đó.'],
     ['Tạo mới phiếu', 'Sửa phiếu', 'Xóa phiếu', 'Không duyệt phiếu', 'Xem lịch sử']),
])

d.save()
d.selfcheck()
