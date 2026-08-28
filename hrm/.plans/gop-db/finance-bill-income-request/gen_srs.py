# -*- coding: utf-8 -*-
"""Sinh SRS (.docx) cho man "Phieu de nghi thu tien" (phan he Tai chinh) theo FORM CHUAN
(ban mau: .claude/skills/srs-documenter/assets/SRS_MAU.docx = SRS Danh muc khach hang).

Anh chup that dung CHUNG voi HDSD: dntt_shots/ (khong commit).

Chay:  python .plans/gop-db/finance-bill-income-request/gen_srs.py
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

SHOTS = os.path.join(HERE, 'dntt_shots')
OUT = os.path.join(HERE, 'SRS - Phiếu đề nghị thu tiền.docx')

HOST = 'http://hrm-crm.eteksofts.com'
ROUTE = '/finance/bill-income-requests'

# Ban mau moi ghi DUONG DAN MENU o muc Layout (khong con dong "URL day du").
MENU = ('Phân hệ Tài chính => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi '
        '=> Đề nghị thu tiền')
MENU_PENDING = ('Phân hệ Tài chính => Phê duyệt - Công nợ - Thu - Chi '
                '=> Phiếu đề nghị thu tiền chờ duyệt')

ACTOR_LAP = 'Người lập phiếu (kinh doanh)'
ACTOR_KT = 'Kế toán thanh toán'


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT,
           menu=MENU,
           route=ROUTE,
           full_url=HOST + ROUTE,
           img_prefix='dntt_')

# ============================================================== TRANG ĐẦU
d.title_block('Phiếu đề nghị thu tiền')
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1. GIỚI THIỆU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu đề nghị thu tiền thuộc phân hệ '
    'Tài chính, nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho toàn bộ vòng đời '
    'một phiếu đề nghị thu tiền: lập nháp → gửi duyệt → kế toán xử lý.',
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ cơ chế phạm vi dữ liệu theo bốn cấp quyền xem và quy tắc luôn ẩn phiếu nháp của '
    'người khác.',
    'Làm rõ khác biệt giữa hai nút lưu: Lưu nháp nới lỏng ràng buộc, Lưu và gửi duyệt bắt buộc '
    'đủ thông tin.',
    'Làm rõ ranh giới với màn Phiếu thu: màn này chỉ đặt hai trạng thái Chờ KT duyệt và '
    'Không duyệt; ba trạng thái Đã tạo phiếu thu, Đã hạch toán, Hủy do màn Phiếu thu đặt.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu đề nghị thu tiền',
     'Chứng từ do bộ phận kinh doanh lập, đề nghị kế toán thu tiền theo một hoặc nhiều hợp đồng.'),
    ('Loại thu',
     'Phân loại nguồn tiền. Hai giá trị chọn được: Thu bán hàng (theo hợp đồng bán của khách '
     'hàng) và Thu nhà cung cấp (theo hợp đồng mua của nhà cung cấp). Giá trị Thu khác chỉ còn '
     'để hiển thị dữ liệu cũ, không chọn mới được.'),
    ('Dòng chi tiết',
     'Một dòng trong bảng Chi tiết, gồm một đối tượng (khách hàng hoặc nhà cung cấp), một hợp '
     'đồng của chính đối tượng đó và số tiền đề nghị thu. Một phiếu có nhiều dòng và có thể gom '
     'nhiều đối tượng khác nhau.'),
    ('Số tiền còn nợ',
     'Số dư công nợ của hợp đồng theo sổ kế toán tại thời điểm mở phiếu. Hệ thống tự tính, '
     'không lưu vào phiếu.'),
    ('Tỷ giá (VND)',
     'Tỷ lệ quy đổi loại tiền của phiếu sang đồng Việt Nam. Loại tiền VNĐ thì tỷ giá bằng 1 và '
     'ô bị khóa.'),
    ('Đang tạo', 'Trạng thái phiếu nháp; chỉ người lập nhìn thấy, sửa và xóa được.'),
    ('Chờ KT duyệt', 'Phiếu đã gửi, đang chờ kế toán thanh toán xử lý.'),
    ('Không duyệt',
     'Kế toán từ chối phiếu kèm lý do bắt buộc; phiếu quay lại cho người lập chỉnh sửa và gửi lại.'),
    ('Đã tạo phiếu thu', 'Đã có phiếu thu được lập và gửi duyệt từ phiếu đề nghị này.'),
    ('Đã hạch toán', 'Phiếu thu tương ứng đã được duyệt và vào sổ kế toán.'),
    ('Hủy', 'Phiếu thu tương ứng đã bị hủy.'),
    ('Màn chờ duyệt',
     'Màn Phiếu đề nghị thu tiền chờ duyệt, chỉ liệt kê phiếu ở trạng thái Chờ KT duyệt thuộc '
     'công ty của người đăng nhập.'),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2. PHÂN QUYỀN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán thanh toán',
     'Mở màn Phiếu đề nghị thu tiền chờ duyệt; hiện nút Không duyệt và nút Tạo phiếu thu ở màn '
     'chi tiết của phiếu đang Chờ KT duyệt.'),
], widths=[0.8, 2.0, 3.2])

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả phiếu đề nghị thu của tổng công ty',
     'Phiếu của mọi công ty trong hệ thống.'),
    ('V2', 'Xem tất cả phiếu đề nghị thu của công ty',
     'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem tất cả phiếu đề nghị thu của phòng ban',
     'Phiếu thuộc các phòng ban mà người đăng nhập được giao quản lý, trong công ty của mình.'),
    ('V4', 'Xem tất cả phiếu đề nghị thu của bộ phận',
     'Phiếu thuộc các bộ phận mà người đăng nhập được giao quản lý, trong công ty của mình.'),
    ('—', '(không có cấp nào)', 'Chỉ phiếu do chính người đăng nhập lập.'),
], widths=[0.8, 2.0, 3.2])
d.p('Ràng buộc bổ sung áp cho mọi cấp: phiếu ở trạng thái Đang tạo của người khác luôn bị ẩn, '
    'kể cả với người có quyền V1. Việc lập phiếu không gắn quyền — mọi người dùng vào được màn '
    'hình đều lập được phiếu của mình. Sửa và xóa chỉ áp cho phiếu do chính mình lập và đang ở '
    'trạng thái Đang tạo hoặc Không duyệt.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1', 'V2', 'V3', 'V4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách phiếu', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc danh sách', '✅', '✅', '✅', '✅', '✅', '✅ (trong phạm vi của mình)'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Lập phiếu đề nghị thu tiền', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Chọn đối tượng và hợp đồng cho dòng chi tiết', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Sửa phiếu', '✅ (phiếu của mình)', '✅ (phiếu của mình)', '✅ (phiếu của mình)',
     '✅ (phiếu của mình)', '✅ (phiếu của mình)', '✅ (phiếu của mình)'),
    ('FR-07 Xem chi tiết phiếu', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-08 Xem danh sách phiếu chờ duyệt', '✅', '❌', '❌', '❌', '❌', '❌'),
    ('FR-09 Không duyệt phiếu', '✅', '❌', '❌', '❌', '❌', '❌'),
    ('FR-10 Xóa phiếu', '✅ (phiếu của mình)', '✅ (phiếu của mình)', '✅ (phiếu của mình)',
     '✅ (phiếu của mình)', '✅ (phiếu của mình)', '✅ (phiếu của mình)'),
    ('FR-11 In phiếu', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-12 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
], widths=[2.0, 0.62, 0.5, 0.5, 0.5, 0.5, 1.38])

# ================================================ PHẦN 3. ĐẶC TẢ CHI TIẾT
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
# Chi 5 use case duoi day la "man hinh" that su -> noi thang toi actor.
# Cac thao tac con lai deu nam NGAY TREN mot trong 5 man do (loc/tuy chinh cot/xoa o man
# danh sach; chon doi tuong & hop dong trong form lap-sua; in, lich su, khong duyet o man
# chi tiet) -> phai la use case phu, noi bang «include» / «extend».
d.overview_figure2(
    [(ACTOR_LAP, [0, 1, 2, 3]),
     (ACTOR_KT, [0, 3, 4])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-04', 'Lập phiếu đề nghị thu tiền', 'crud'),
     ('FR-06', 'Sửa phiếu', 'crud'),
     ('FR-07', 'Xem chi tiết phiếu', 'view'),
     ('FR-08', 'Xem danh sách phiếu chờ duyệt', 'view')],
    [('FR-02', 'Tìm kiếm và lọc danh sách', 'view', 'extend', [0],
      'Dùng chung cho cả màn chờ duyệt'),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-10', 'Xóa phiếu', 'action', 'extend', [0],
      'Phiếu của mình, đang Đang tạo hoặc Không duyệt'),
     ('FR-05', 'Chọn đối tượng và hợp đồng', 'crud', 'include', [1, 2], None),
     ('FR-09', 'Không duyệt phiếu', 'action', 'extend', [3], 'Chỉ Kế toán thanh toán'),
     ('FR-11', 'In phiếu', 'io', 'extend', [3], None),
     ('FR-12', 'Xem lịch sử thay đổi', 'view', 'extend', [3],
      'Mở từ danh sách hoặc màn chi tiết')],
    'Sơ đồ Use Case tổng quan màn Phiếu đề nghị thu tiền')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1 FR-01
d.h3('2.1 Xem danh sách phiếu đề nghị thu tiền')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung các '
           'quy tắc riêng của Phiếu đề nghị thu tiền tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Xem danh sách phiếu đề nghị thu tiền',
    mota='Hiển thị bảng phiếu đề nghị thu tiền nằm trong phạm vi dữ liệu của người đăng nhập, '
         'kèm phân trang, sắp xếp và tổng số bản ghi khớp bộ lọc.',
    tacnhan='Người lập phiếu; Kế toán thanh toán; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và đang ở phân hệ Tài chính.',
    chinh='1. Người dùng vào menu Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi → '
          'Đề nghị thu tiền (hoặc menu Đề nghị → Đề nghị thu tiền).\n'
          '2. Hệ thống xác định cấp quyền xem của người dùng theo thứ tự V1 → V2 → V3 → V4, '
          'không có cấp nào thì giới hạn ở phiếu do chính người đó lập.\n'
          '3. Hệ thống loại bỏ phiếu ở trạng thái Đang tạo của người khác.\n'
          '4. Hệ thống trả về trang đầu tiên, sắp xếp phiếu lập gần nhất lên trước, kèm tổng số '
          'bản ghi.\n'
          '5. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó thay cho bộ cột mặc định.\n'
        '• Vào lại màn trong vòng 10 phút sau khi rời đi → hệ thống khôi phục bộ lọc đã dùng.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách Phiếu đề nghị thu tiền lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Phiếu đề nghị thu tiền',
     'Hiển thị trên thanh tiêu đề và tiêu đề bảng.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Không gắn quyền. Ẩn ở màn chờ duyệt.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cột bắt buộc, không ẩn và không đổi vị trí được.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là liên kết mở màn chi tiết; sắp xếp được; cột bắt buộc.'),
    ('Cột Loại thu', 'Table/Grid', 'Read-only', 'Danh sách 3 giá trị', 'Theo dữ liệu',
     'Thu bán hàng / Thu nhà cung cấp / Thu khác (giá trị cũ).'),
    ('Cột Khách hàng / Nhà cung cấp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Lấy đối tượng của dòng chi tiết đầu tiên, dạng mã - tên.'),
    ('Cột Lý do thu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tự xuống dòng khi dài.'),
    ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Phòng ban của người lập tại thời điểm lập phiếu.'),
    ('Cột Tổng tiền đề nghị', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Tổng số tiền đề nghị thu quy đổi VND của mọi dòng chi tiết; canh phải.'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 6 giá trị', 'Theo dữ liệu',
     'Đã tạo phiếu thu và Đã hạch toán nền xanh; Đang tạo, Chờ KT duyệt, Hủy, Không duyệt nền đỏ.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo quyền và trạng thái',
     'Cột bắt buộc. Chứa các nút Sửa, In phiếu, Tạo phiếu thu và nút ba chấm (Xóa, Lịch sử).'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc, không phải tổng toàn hệ thống.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách', '10',
     'Đổi giá trị thì quay về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
     'Có nút về đầu / lùi / số trang / tiến / về cuối.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi N = 0.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Ẩn', 'Hiện trong lúc nạp dữ liệu.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định cấp quyền xem theo thứ tự V1 → V2 → V3 → V4; không có cấp nào thì '
     'giới hạn ở phiếu do chính người dùng lập.\n'
     'During:\n– Áp phạm vi dữ liệu; loại bỏ phiếu Đang tạo của người khác.\n'
     '– Khôi phục bộ lọc đã lưu trong 10 phút gần nhất (nếu có) và cấu hình cột của người dùng.\n'
     'After:\n– Trả về trang 1, sắp xếp theo ngày tạo giảm dần, kèm tổng số bản ghi.'),
    ('Bấm vào mã phiếu', 'Click',
     'After:\n– Mở màn chi tiết của phiếu tương ứng (FR-07).\n'
     '– Bấm chuột phải cho phép mở ở tab mới.'),
    ('Bấm tiêu đề cột có sắp xếp', 'Click',
     'Before:\n– Chỉ ba cột Mã phiếu, Ngày tạo, Ngày cập nhật hỗ trợ sắp xếp.\n'
     'After:\n– Đổi chiều sắp xếp, quay về trang 1 và nạp lại danh sách.'),
    ('Bấm số trang / nút tiến lùi', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'),
    ('Đổi Số dòng/trang', 'Change',
     'After:\n– Quay về trang 1 và nạp lại danh sách theo số dòng mới.'),
])

# ---------------------------------------------------------------- 2.2 FR-02
d.h3('2.2 Tìm kiếm và lọc danh sách')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang và quy tắc bộ lọc chọn nhiều giá '
           'trị. Chỉ bổ sung các tiêu chí tìm kiếm/lọc riêng của Phiếu đề nghị thu tiền.',
           anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu',
    mota='Thu hẹp danh sách theo mã phiếu, cấp tổ chức, loại thu, trạng thái, hợp đồng, đối '
         'tượng thu, người tạo, khoảng số tiền và khoảng ngày tạo.',
    tacnhan='Người lập phiếu; Kế toán thanh toán; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách hoặc màn chờ duyệt.',
    chinh='1. Người dùng bấm Tìm kiếm nâng cao để mở khối tiêu chí.\n'
          '2. Người dùng chọn hoặc nhập giá trị cho một hoặc nhiều tiêu chí.\n'
          '3. Hệ thống lọc ngay khi giá trị thay đổi, quay về trang 1.\n'
          '4. Riêng ô tìm nhanh theo mã phiếu chỉ lọc khi người dùng bấm nút Tìm kiếm.\n'
          '5. Hệ thống ghi nhớ bộ lọc trong 10 phút để khôi phục khi quay lại màn hình.',
    phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, nạp lại danh sách từ trang 1.\n'
        '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Đổi Công ty → hệ thống xóa giá trị đang chọn ở Phòng ban và Bộ phận.\n'
        '• Tiêu chí bị tắt trong Cài đặt bộ lọc → giá trị của tiêu chí đó cũng bị xóa, danh sách '
        'không bị lọc ngầm.\n'
        '• Bộ lọc của màn chờ duyệt lưu riêng, không dùng chung với màn danh sách.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao ở trạng thái mở với đủ 9 tiêu chí')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô Tìm theo mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo một phần mã phiếu; chỉ lọc khi bấm nút Tìm kiếm.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Áp giá trị ô tìm nhanh và quay về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa toàn bộ tiêu chí đang lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở / thu gọn khối tiêu chí; khi mở, nhãn đổi thành Ẩn tìm kiếm nâng cao.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ chọn tiêu chí (FR-03).'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Chỉ hiện với người có quyền V1.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện với V1, V2, V3; chỉ liệt kê phòng ban của công ty đang chọn.'),
    ('Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống', 'Hiện với V4.'),
    ('Loại thu', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
     'Thu bán hàng, Thu nhà cung cấp.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Không', 'Trống',
     'Đang tạo, Chờ KT duyệt, Đã tạo phiếu thu, Đã hạch toán, Hủy, Không duyệt.'),
    ('Số đơn hàng/hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo số hợp đồng nằm trong dòng chi tiết của phiếu.'),
    ('Khách hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm được cả theo mã và theo tên khách hàng.'),
    ('Nhà cung cấp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Danh sách tìm từ xa, cần nhập tối thiểu 2 ký tự mới gợi ý.'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Chọn nhân sự đã lập phiếu.'),
    ('Số tiền đề nghị từ', 'Number', 'Enable', '≥ 0', 'Không', 'Trống',
     'So sánh trên tổng tiền đề nghị quy đổi của cả phiếu.'),
    ('Số tiền đề nghị đến', 'Number', 'Enable', '≥ 0', 'Không', 'Trống', 'Bỏ trống thì không chặn trên.'),
    ('Ngày tạo từ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Lấy trọn ngày.'),
    ('Ngày tạo đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lấy trọn ngày, phiếu lập trong chính ngày đó vẫn nằm trong kết quả.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Đổi giá trị một tiêu chí trong Tìm kiếm nâng cao', 'Change',
     'During:\n– Ghi nhận giá trị mới và ghi nhớ bộ lọc trong 10 phút.\n'
     'After:\n– Quay về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí đang có.'),
    ('Bấm nút Tìm kiếm', 'Click',
     'After:\n– Áp giá trị ô tìm nhanh theo mã phiếu, quay về trang 1 và nạp lại danh sách.'),
    ('Bấm nút Làm mới', 'Click',
     'After:\n– Đặt lại toàn bộ tiêu chí về trống, xóa nhãn nhà cung cấp đã chọn, quay về '
     'trang 1 và nạp lại danh sách.'),
    ('Đổi Công ty', 'Change',
     'During:\n– Xóa giá trị Phòng ban và Bộ phận đang chọn.\n'
     'After:\n– Nạp lại danh sách phòng ban theo công ty mới và nạp lại danh sách phiếu.'),
    ('Nhập từ khóa ô Nhà cung cấp', 'Keypress',
     'Before:\n– Chỉ gợi ý khi từ khóa từ 2 ký tự trở lên.\n'
     'After:\n– Hiển thị danh sách gợi ý dạng mã - tên; chọn một dòng thì lọc ngay.'),
])

# ---------------------------------------------------------------- 2.3 FR-03
d.h3('2.3 Cài đặt bộ lọc và tuỳ chỉnh cột hiển thị')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view',
            [('include', 'Lưu cấu hình theo từng người dùng'),
             ('extend', 'Khôi phục cấu hình mặc định')],
            actor='Người dùng đã đăng nhập',
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Cấu hình bộ lọc và Tùy chỉnh cột. Chỉ bổ sung danh sách tiêu chí lọc và bộ cột '
           'riêng của Phiếu đề nghị thu tiền.',
           anchor='list')
d.intro_table(
    ten='Cài đặt bộ lọc và tuỳ chỉnh cột hiển thị',
    mota='Cho phép mỗi người dùng tự chọn những tiêu chí lọc và những cột muốn thấy, đồng thời '
         'sắp xếp lại thứ tự của chúng. Cấu hình lưu riêng theo người dùng và theo màn hình.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách hoặc màn chờ duyệt.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ liệt kê toàn bộ tiêu chí (hoặc toàn bộ cột) kèm ô tích chọn.\n'
          '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống ghi nhận, hiển thị thông báo “Cập nhật thành công” và áp ngay lên màn hình.',
    phu='• Bấm Khôi phục mặc định ở cửa sổ Cài đặt bộ lọc → tích lại đủ 9 tiêu chí, vẫn phải '
        'bấm Lưu mới có hiệu lực.\n'
        '• Bấm Đóng → thoát mà không lưu thay đổi.\n'
        '• Bỏ tích một tiêu chí lọc → giá trị đang lọc của tiêu chí đó bị xóa.\n'
        '• Ba cột STT, Mã phiếu, Hành động bị khóa, không bỏ tích và không đổi vị trí được.',
    dacbiet='Cấu hình cột dùng chung giữa màn danh sách và màn chờ duyệt vì hai màn có cùng bộ '
            'cột; cấu hình bộ lọc thì lưu riêng cho từng màn.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột',
         modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('04-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc với đủ 9 tiêu chí')
d.figure(shot('03-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột', width_in=6.2)

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc / Tuỳ chỉnh cột', '–'),
    ('Ô tích chọn từng tiêu chí', 'Modal', 'Enable', 'Danh sách 9 tiêu chí', 'Không',
     'Theo cấu hình đã lưu', 'Bỏ tích thì tiêu chí không hiển thị ở bộ lọc nâng cao.'),
    ('Ô tích chọn từng cột', 'Modal', 'Enable', 'Danh sách 13 cột', 'Không',
     'Theo cấu hình đã lưu', 'Ba cột bắt buộc bị khóa kèm biểu tượng ổ khóa.'),
    ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Kéo để đổi thứ tự tiêu chí / cột.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Ghi cấu hình cho người dùng hiện tại và áp ngay lên màn hình.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Chỉ có ở cửa sổ Cài đặt bộ lọc; tích lại đủ 9 tiêu chí theo thiết kế.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Thoát mà không lưu.'),
    ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện “Cập nhật thành công” sau khi lưu.'),
])

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Cài đặt bộ lọc / Cấu hình cột hiển thị', 'Click',
     'After:\n– Mở cửa sổ tương ứng, nạp cấu hình đang lưu của người dùng.'),
    ('Bỏ tích một mục', 'Change',
     'During:\n– Mục bắt buộc (STT, Mã phiếu, Hành động) không cho bỏ tích.\n'
     'After:\n– Ghi nhận trạng thái tích trong cửa sổ, chưa áp lên màn hình cho tới khi bấm Lưu.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi cấu hình cho người dùng hiện tại theo từng màn hình.\n'
     'After:\n– Hiển thị “Cập nhật thành công”; bộ lọc / bảng cập nhật ngay.\n'
     '– Với tiêu chí vừa bị bỏ tích, xóa luôn giá trị đang lọc của tiêu chí đó.'),
    ('Bấm Khôi phục mặc định', 'Click',
     'After:\n– Tích lại toàn bộ 9 tiêu chí và đưa thứ tự về thiết kế gốc; chưa lưu.'),
])

# ---------------------------------------------------------------- 2.4 FR-04
d.h3('2.4 Lập phiếu đề nghị thu tiền')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Lập phiếu đề nghị thu tiền', 'crud',
            [('include', 'Sinh mã phiếu tự động'),
             ('include', 'Chọn đối tượng và hợp đồng cho dòng chi tiết'),
             ('extend', 'Gửi thông báo cho kế toán khi gửi duyệt')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-04 Lập phiếu đề nghị thu tiền')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Lập phiếu đề nghị thu tiền',
    mota='Tạo một phiếu đề nghị thu tiền mới. Người dùng chọn loại thu, loại tiền, nhập lý do '
         'thu và các dòng chi tiết, sau đó lưu nháp hoặc gửi duyệt.',
    tacnhan='Người lập phiếu; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách. Chức năng không gắn quyền.',
    chinh='1. Người dùng bấm nút Tạo mới, hệ thống mở màn Thêm phiếu đề nghị thu tiền.\n'
          '2. Người dùng chọn Loại thu và Loại tiền, nhập Lý do thu.\n'
          '3. Người dùng bấm dấu cộng ở tiêu đề bảng Chi tiết để thêm dòng, chọn đối tượng và '
          'hợp đồng cho từng dòng (FR-05), nhập Số tiền đề nghị thu.\n'
          '4. Người dùng bấm Lưu nháp, hoặc bấm Lưu và gửi duyệt rồi xác nhận.\n'
          '5. Hệ thống kiểm tra dữ liệu theo nút được bấm, sinh mã phiếu, ghi phiếu và các dòng '
          'chi tiết.\n'
          '6. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Bấm Lưu và gửi duyệt mà thiếu Lý do thu hoặc chưa có dòng chi tiết → báo lỗi đỏ ngay '
        'dưới ô / dưới bảng, không lưu, giữ nguyên dữ liệu đã nhập.\n'
        '• Đổi Loại thu khi bảng chi tiết đã có dòng → hệ thống hỏi xác nhận trước khi xóa các '
        'dòng đó.\n'
        '• Đổi Loại tiền → tỷ giá tự điền theo loại tiền; loại tiền VNĐ thì tỷ giá về 1 và bị khóa.\n'
        '• Rời màn khi đã nhập dở → hệ thống hỏi xác nhận trước khi thoát.\n'
        '• Hai người cùng lưu tại một thời điểm → mã phiếu vẫn duy nhất, không trùng.',
    dacbiet='Lưu nháp và Lưu và gửi duyệt có ràng buộc khác nhau: lưu nháp cho phép bỏ trống Lý '
            'do thu và chưa có dòng chi tiết nào; gửi duyệt bắt buộc cả hai. Dòng chi tiết đã '
            'thêm thì trong cả hai trường hợp đều phải đủ đối tượng, hợp đồng và số tiền.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Thêm mới',
         shot=shot('06-tao-moi.png'),
         shot_caption='Màn Thêm phiếu đề nghị thu tiền lúc vừa mở')
d.figure(shot('11-tao-moi-ghi-chu.png'),
         'Màn lập phiếu đã nhập đủ ba khối Thông tin chung, Chi tiết và Ghi chú', width_in=6.2)

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Loại thu', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Có', 'Thu bán hàng',
     'Quyết định bảng Chi tiết chọn khách hàng hay nhà cung cấp.'),
    ('Loại tiền', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'VNĐ — VietNamDong',
     'Hiển thị dạng mã — tên; đổi giá trị thì tự điền tỷ giá tương ứng.'),
    ('Tỷ giá (VND)', 'Number', 'Enable / Disable', '> 0', 'Có', '1',
     'Bị khóa khi Loại tiền là VNĐ; mở khóa và tự điền khi chọn ngoại tệ.'),
    ('Lý do thu', 'Textbox', 'Enable', '0–255 ký tự', 'Có khi gửi duyệt', 'Trống',
     'Bỏ trống khi gửi duyệt thì báo “Bắt buộc nhập”.'),
    ('Ghi chú', 'Textarea', 'Enable', '–', 'Không', 'Trống',
     'Nằm ở khối Ghi chú cuối màn; khi phiếu bị từ chối, ô này chứa lý do không duyệt.'),
    ('Nút thêm dòng (dấu cộng)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Nằm ở góc phải hàng tiêu đề bảng Chi tiết; thêm một dòng trống.'),
    ('Cột Khách hàng / Nhà cung cấp của dòng', 'Textbox', 'Read-only', '–', 'Có', 'Trống',
     'Bấm vào ô để mở cửa sổ chọn đối tượng (FR-05); nhãn cột đổi theo Loại thu.'),
    ('Cột Số đơn hàng/Hợp đồng của dòng', 'Textbox', 'Read-only', '–', 'Có', 'Trống',
     'Bị khóa cho tới khi dòng đã chọn đối tượng; gợi ý “Chọn khách hàng trước”.'),
    ('Cột Số tiền còn nợ của dòng', 'Number', 'Read-only', '≥ 0', '–', '0',
     'Hệ thống điền theo hợp đồng vừa chọn.'),
    ('Cột Số tiền đề nghị thu của dòng', 'Number', 'Enable', '≥ 0', 'Có', '0',
     'Định dạng có dấu ngăn nghìn; khi dùng ngoại tệ tách thành hai cột con.'),
    ('Cột quy đổi VND của dòng', 'Number', 'Read-only', '≥ 0', '–', '0',
     'Chỉ hiện khi Loại tiền khác VNĐ; bằng số tiền nhân tỷ giá.'),
    ('Cột Ghi chú của dòng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Nút xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Xóa dòng và đánh số lại các dòng còn lại.'),
    ('Dòng Tổng cộng', 'Label', 'Read-only', '≥ 0', '–', '0',
     'Cộng dồn ngay theo từng phím gõ, gồm tổng Số tiền còn nợ, tổng Số tiền đề nghị thu và '
     'tổng quy đổi.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu phiếu ở trạng thái Đang tạo.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở hộp xác nhận, sau đó lưu phiếu ở trạng thái Chờ KT duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu đã nhập dở mà chưa lưu.'),
    ('Hộp xác nhận lưu và gửi duyệt', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Tiêu đề “Xác nhận lưu và gửi duyệt”, nội dung “Bạn đồng ý lưu và duyệt?”.'),
    ('Hộp xác nhận đổi loại thu', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Tiêu đề “Đổi loại thu”, nội dung “Đổi loại thu sẽ xóa toàn bộ dòng chi tiết đã chọn. '
     'Bạn có chắc chắn?”.'),
    ('Hộp cảnh báo chưa lưu', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Tiêu đề “Thông tin chưa lưu”, hai nút Thoát và Ở lại.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi; ô đổi sang viền đỏ.'),
])
d.figure(shot('24-loi-validate.png'),
         'Thông báo bắt buộc nhập ở ô Lý do thu và dưới bảng Chi tiết', width_in=6.2)
d.figure(shot('12-xac-nhan-gui-duyet.png'),
         'Hộp xác nhận trước khi gửi duyệt', width_in=6.2)
d.figure(shot('13-canh-bao-chua-luu.png'),
         'Hộp cảnh báo khi rời màn hình mà chưa lưu', width_in=6.2)
d.figure(shot('25-xac-nhan-doi-loai-thu.png'),
         'Hộp xác nhận khi đổi Loại thu lúc bảng chi tiết đã có dòng', width_in=6.2)

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'After:\n– Mở màn thêm mới với Loại thu = Thu bán hàng, Loại tiền = VNĐ, Tỷ giá = 1 '
     '(khóa), các ô còn lại để trống, bảng Chi tiết rỗng.'),
    ('Đổi Loại thu', 'Change',
     'Before:\n– Nếu bảng Chi tiết chưa có dòng nào → đổi ngay, không hỏi.\n'
     'During:\n– Nếu đã có dòng → hiển thị hộp xác nhận “Đổi loại thu”.\n'
     'After:\n– Chọn Xác nhận: xóa toàn bộ dòng chi tiết và mọi lỗi của các dòng đó, đổi nhãn '
     'cột sang Nhà cung cấp / Hợp đồng mua (hoặc ngược lại).\n'
     '– Chọn Hủy: giữ nguyên các dòng chi tiết.'),
    ('Đổi Loại tiền', 'Change',
     'After:\n– Loại tiền VNĐ: đặt Tỷ giá = 1 và khóa ô, ẩn cột quy đổi.\n'
     '– Loại tiền khác: mở khóa ô Tỷ giá và tự điền tỷ giá của loại tiền đó, hiện thêm cột '
     'quy đổi VND.\n'
     '– Tính lại cột quy đổi của mọi dòng chi tiết.'),
    ('Nhập Số tiền đề nghị thu của một dòng', 'Change',
     'After:\n– Tính lại cột quy đổi VND của dòng đó và ba ô của dòng Tổng cộng.'),
    ('Bấm Lưu nháp', 'Click',
     'During:\n– Tỷ giá trống hoặc không lớn hơn 0 → hiển thị “Phải lớn hơn 0”.\n'
     '– Dòng chi tiết đã thêm mà thiếu đối tượng / hợp đồng / số tiền → hiển thị “Bắt buộc nhập” '
     'ngay dưới ô tương ứng của đúng dòng đó.\n'
     '– Không bắt buộc Lý do thu và cho phép bảng Chi tiết rỗng.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Sinh mã phiếu theo dạng <mã công ty>.DNTT<tháng năm>.<5 chữ số>, ghi phiếu ở '
     'trạng thái Đang tạo cùng công ty / phòng ban / bộ phận của người lập.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Hiển thị “Lưu phiếu đề nghị thu thành công!” và quay về màn danh sách.'),
    ('Bấm Lưu và gửi duyệt', 'Click',
     'Before:\n– Hiển thị hộp xác nhận “Xác nhận lưu và gửi duyệt”; chọn Hủy thì dừng xử lý.\n'
     'During:\n– Lý do thu trống → hiển thị “Bắt buộc nhập”.\n'
     '– Bảng Chi tiết chưa có dòng nào → hiển thị “Bắt buộc nhập” ngay dưới bảng.\n'
     '– Dòng chi tiết thiếu đối tượng / hợp đồng / số tiền → hiển thị “Bắt buộc nhập” ở đúng ô.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Sinh mã phiếu và ghi phiếu ở trạng thái Chờ KT duyệt.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Gửi thông báo tới các kế toán thanh toán cùng công ty với phiếu, nội dung dạng '
     '“[DNTT] Chờ duyệt: <mã phiếu>. Người đề nghị: <tên>. Số tiền: <tổng tiền>”.\n'
     '– Hiển thị “Gửi duyệt phiếu đề nghị thu thành công!” và quay về màn danh sách.'),
    ('Bấm Quay lại khi đã nhập dở', 'Click',
     'During:\n– Hiển thị hộp “Thông tin chưa lưu”.\n'
     'After:\n– Chọn Ở lại thì giữ nguyên dữ liệu; chọn Thoát thì bỏ mọi thay đổi và về danh sách.'),
])

# ---------------------------------------------------------------- 2.5 FR-05
d.h3('2.5 Chọn đối tượng và hợp đồng cho dòng chi tiết')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chọn đối tượng và hợp đồng', 'crud',
            [('include', 'Lọc hợp đồng theo đối tượng của dòng'),
             ('include', 'Tính số tiền còn nợ theo sổ kế toán'),
             ('extend', 'Chặn chọn trùng hợp đồng trong cùng phiếu')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-05 Chọn đối tượng và hợp đồng cho dòng chi tiết')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Dropdown, Popup chọn dữ liệu và Validate dữ liệu. Chỉ bổ sung nguồn dữ liệu và '
           'điều kiện lọc riêng của Phiếu đề nghị thu tiền.',
           anchor='create')
d.intro_table(
    ten='Chọn đối tượng và hợp đồng cho dòng chi tiết',
    mota='Trên từng dòng của bảng Chi tiết, người dùng chọn một khách hàng (loại thu Thu bán '
         'hàng) hoặc một nhà cung cấp (loại thu Thu nhà cung cấp), sau đó chọn một hợp đồng '
         'của chính đối tượng đó. Hệ thống tự điền số tiền còn nợ của hợp đồng.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn lập phiếu hoặc màn sửa phiếu, bảng Chi tiết đã có ít nhất một dòng.',
    chinh='1. Người dùng bấm vào ô đối tượng của dòng, hệ thống mở cửa sổ chọn tương ứng.\n'
          '2. Người dùng tìm kiếm và bấm vào một dòng để chọn; cửa sổ tự đóng.\n'
          '3. Ô hợp đồng của dòng được mở khóa.\n'
          '4. Người dùng bấm vào ô hợp đồng, hệ thống mở cửa sổ chọn hợp đồng đã lọc theo đúng '
          'đối tượng của dòng.\n'
          '5. Người dùng bấm vào một hợp đồng; cửa sổ tự đóng, ô hợp đồng và cột Số tiền còn nợ '
          'được điền.',
    phu='• Chưa chọn đối tượng mà bấm ô hợp đồng → ô bị khóa, không mở cửa sổ, gợi ý ghi '
        '“Chọn khách hàng trước” (hoặc “Chọn nhà cung cấp trước”).\n'
        '• Đổi đối tượng của dòng đã chọn hợp đồng → hệ thống xóa hợp đồng của dòng và đưa Số '
        'tiền còn nợ về 0.\n'
        '• Hợp đồng đã có ở dòng khác trong cùng phiếu → hiển thị chú thích “Hợp đồng đã có '
        'trong phiếu” và không cho chọn.\n'
        '• Hợp đồng chưa phát sinh bút toán kế toán → Số tiền còn nợ hiển thị 0.',
    dacbiet='Danh sách hợp đồng bán gồm ba nguồn: hợp đồng bán từ trạng thái Có hiệu lực trở '
            'lên (Có hiệu lực, Đang xuất hàng, Đã xuất hàng, Đã thanh lý, Đang quyết toán, '
            'Đã quyết toán), hợp đồng đầu kỳ và hợp đồng bảo dưỡng. Danh sách hợp đồng mua gồm '
            'năm nguồn hợp đồng mua của nhà cung cấp.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Thêm mới => Chọn khách hàng / Chọn nhà cung cấp / '
                     'Chọn đơn hàng - hợp đồng',
         modal='Chọn khách hàng, Chọn nhà cung cấp và Chọn đơn hàng/hợp đồng',
         shot=shot('08-popup-khach-hang.png'),
         shot_caption='Cửa sổ Chọn khách hàng')
d.figure(shot('09-popup-hop-dong.png'),
         'Cửa sổ Chọn đơn hàng/hợp đồng, đã lọc theo khách hàng của dòng', width_in=6.2)
d.figure(shot('22-popup-nha-cung-cap.png'), 'Cửa sổ Chọn nhà cung cấp', width_in=6.2)

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ chọn đối tượng', 'Label', 'Hiển thị', '–', '–',
     'Chọn khách hàng / Chọn nhà cung cấp', 'Đổi theo Loại thu của phiếu.'),
    ('Ô Tên / Mã khách hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Chỉ có ở cửa sổ Chọn khách hàng.'),
    ('Ô Mã số thuế', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Chỉ có ở cửa sổ Chọn khách hàng.'),
    ('Ô Số điện thoại', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Chỉ có ở cửa sổ Chọn khách hàng.'),
    ('Ô Mã / Tên nhà cung cấp', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Chỉ có ở cửa sổ Chọn nhà cung cấp; tìm theo cả mã và tên.'),
    ('Bảng kết quả chọn đối tượng', 'Table/Grid', 'Read-only', '–', '–', 'Trang 1',
     'Bấm vào một dòng để chọn; cửa sổ tự đóng.'),
    ('Ô Số đơn hàng/Hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Ô tìm trong cửa sổ Chọn đơn hàng/hợp đồng.'),
    ('Bảng hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Trang 1',
     'Cột STT, Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ.'),
    ('Dòng hợp đồng đã có trong phiếu', 'Table/Grid', 'Disable', '–', '–', 'Ẩn',
     'Hiển thị khác biệt kèm chú thích “Hợp đồng đã có trong phiếu”, không chọn được.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp điều kiện tìm trong cửa sổ.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa điều kiện tìm trong cửa sổ.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không chọn gì.'),
    ('Phân trang trong cửa sổ', 'Pagination', 'Enable', '–', 'Trang 1, 10 dòng',
     'Không', 'Có ô chọn số dòng mỗi trang.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm vào ô đối tượng của dòng', 'Click',
     'Before:\n– Màn xem chi tiết ở chế độ chỉ đọc thì không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ Chọn khách hàng hoặc Chọn nhà cung cấp theo Loại thu; ghi nhận dòng '
     'đang thao tác.'),
    ('Chọn một đối tượng trong cửa sổ', 'Click',
     'After:\n– Gán đối tượng cho dòng và hiển thị dạng mã - tên.\n'
     '– Xóa hợp đồng đã chọn của dòng và đưa Số tiền còn nợ về 0.\n'
     '– Xóa thông báo lỗi bắt buộc của ô đối tượng; đóng cửa sổ.'),
    ('Bấm vào ô hợp đồng của dòng', 'Click',
     'Before:\n– Dòng chưa chọn đối tượng → không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ hợp đồng, lọc theo đối tượng của dòng và theo Loại thu của phiếu.'),
    ('Chọn một hợp đồng trong cửa sổ', 'Click',
     'Before:\n– Hợp đồng đã có ở dòng khác trong cùng phiếu → không cho chọn.\n'
     'After:\n– Gán hợp đồng cho dòng, điền Số tiền còn nợ theo sổ kế toán, xóa lỗi bắt buộc '
     'của ô hợp đồng; đóng cửa sổ.'),
    ('Bấm nút xóa dòng', 'Click',
     'After:\n– Xóa dòng, đánh số lại các dòng còn lại, dồn thông báo lỗi về đúng dòng tương ứng '
     'và tính lại dòng Tổng cộng.'),
])

# ---------------------------------------------------------------- 2.6 FR-06
d.h3('2.6 Sửa phiếu đề nghị thu tiền')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Sửa phiếu đề nghị thu tiền', 'crud',
            [('include', 'Kiểm tra phiếu do chính người dùng lập'),
             ('include', 'Kiểm tra trạng thái Đang tạo hoặc Không duyệt'),
             ('extend', 'Gửi duyệt lại phiếu bị từ chối')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-06 Sửa phiếu đề nghị thu tiền')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.',
           anchor='notice')
d.intro_table(
    ten='Sửa phiếu đề nghị thu tiền',
    mota='Chỉnh sửa nội dung phiếu do chính người dùng lập, khi phiếu còn ở trạng thái Đang tạo '
         'hoặc Không duyệt. Dùng cả cho việc sửa lại phiếu bị kế toán từ chối rồi gửi duyệt lại.',
    tacnhan='Người lập phiếu',
    dieukien='Phiếu do chính người đăng nhập lập và đang ở trạng thái Đang tạo hoặc Không duyệt.',
    chinh='1. Người dùng bấm nút Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở màn Sửa phiếu đề nghị thu tiền, nạp toàn bộ dữ liệu của phiếu.\n'
          '3. Người dùng chỉnh sửa thông tin chung và bảng chi tiết.\n'
          '4. Người dùng bấm Lưu nháp hoặc Lưu và gửi duyệt rồi xác nhận.\n'
          '5. Hệ thống kiểm tra dữ liệu, ghi lại phiếu và các dòng chi tiết, ghi lịch sử thay đổi.\n'
          '6. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Phiếu không phải của người đăng nhập → nút Sửa không hiển thị; gọi thẳng chức năng '
        'thì hệ thống từ chối với thông báo không có quyền sửa phiếu này.\n'
        '• Phiếu vừa bị người khác đổi trạng thái → hệ thống báo “Thao tác không thành công. '
        'Dữ liệu đã được thay đổi hoặc chuyển trạng thái bởi người dùng khác. Vui lòng tải lại '
        'trang để cập nhật thông tin mới nhất.”.\n'
        '• Sửa lại một phiếu vốn đã ở trạng thái Chờ KT duyệt → không gửi lại thông báo cho kế '
        'toán.\n'
        '• Rời màn khi đã sửa mà chưa lưu → hệ thống hỏi xác nhận trước khi thoát.',
    dacbiet='Ba ô Mã phiếu, Người tạo và Phòng ban chỉ để xem, không sửa được. Công ty, phòng '
            'ban và bộ phận của phiếu giữ nguyên như lúc lập, không đổi theo người sửa.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa',
         shot=shot('21-sua.png'),
         shot_caption='Màn Sửa phiếu đề nghị thu tiền')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mã phiếu', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', 'Chỉ để xem, không sửa được.'),
    ('Người tạo', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', 'Chỉ để xem.'),
    ('Phòng ban', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu',
     'Phòng ban của người lập tại thời điểm lập phiếu.'),
    ('Dòng người tạo - ngày lập', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
     'Hiển thị ở góc phải tiêu đề khối Thông tin chung.'),
    ('Loại thu', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Có', 'Theo dữ liệu',
     'Đổi giá trị thì hỏi xác nhận xóa dòng chi tiết.'),
    ('Loại tiền', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Theo dữ liệu', '–'),
    ('Tỷ giá (VND)', 'Number', 'Enable / Disable', '> 0', 'Có', 'Theo dữ liệu',
     'Bị khóa khi Loại tiền là VNĐ.'),
    ('Lý do thu', 'Textbox', 'Enable', '0–255 ký tự', 'Có khi gửi duyệt', 'Theo dữ liệu', '–'),
    ('Ghi chú', 'Textarea', 'Enable', '–', 'Không', 'Theo dữ liệu',
     'Với phiếu bị từ chối, ô này đang chứa lý do không duyệt của kế toán.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', 'Có khi gửi duyệt', 'Theo dữ liệu',
     'Thao tác thêm, sửa, xóa dòng giống màn lập phiếu (FR-05).'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Giữ phiếu ở trạng thái hiện tại.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đưa phiếu sang trạng thái Chờ KT duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu đã sửa mà chưa lưu.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu do chính người dùng lập và đang ở trạng thái Đang '
     'tạo hoặc Không duyệt.\n'
     'After:\n– Mở màn sửa và nạp toàn bộ dữ liệu của phiếu, kể cả các dòng chi tiết.'),
    ('Bấm Lưu nháp / Lưu và gửi duyệt', 'Click',
     'Before:\n– Kiểm tra phiếu do chính người dùng lập; nếu không → từ chối với thông báo '
     'không có quyền sửa phiếu này và dừng xử lý.\n'
     '– Kiểm tra phiếu còn ở trạng thái Đang tạo hoặc Không duyệt; nếu không → hiển thị thông '
     'báo dữ liệu đã được thay đổi và đề nghị tải lại trang.\n'
     'During:\n– Áp cùng bộ kiểm tra dữ liệu như màn lập phiếu, khác nhau theo nút được bấm.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Ghi lại thông tin chung và ghi lại toàn bộ dòng chi tiết theo dữ liệu mới.\n'
     '– Ghi một dòng lịch sử “Thay đổi thông tin”, liệt kê từng trường đã đổi và từng dòng chi '
     'tiết được thêm, sửa hoặc bỏ.\n'
     '– Nếu phiếu chuyển từ trạng thái khác sang Chờ KT duyệt thì gửi thông báo cho kế toán '
     'thanh toán cùng công ty.\n'
     '– Hiển thị thông báo thành công tương ứng và quay về màn danh sách.'),
])

# ---------------------------------------------------------------- 2.7 FR-07
d.h3('2.7 Xem chi tiết phiếu')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các khối thông tin riêng của phiếu đề '
           'nghị thu tiền.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu đề nghị thu tiền',
    mota='Hiển thị toàn bộ nội dung một phiếu ở chế độ chỉ đọc, kèm bộ nút thao tác phù hợp với '
         'trạng thái phiếu và quyền của người xem, và khối Lịch sử ở cuối trang.',
    tacnhan='Người lập phiếu; Kế toán thanh toán; Người dùng đã đăng nhập',
    dieukien='Phiếu nằm trong phạm vi dữ liệu người dùng được xem.',
    chinh='1. Người dùng bấm vào mã phiếu ở màn danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống tính lại Số tiền còn nợ của từng dòng theo sổ kế toán tại thời điểm mở.\n'
          '4. Màn chi tiết hiển thị thông tin chung, bảng chi tiết kèm dòng Tổng cộng, ghi chú '
          'và khối Lịch sử.\n'
          '5. Thanh nút dưới cùng hiển thị các thao tác mà người dùng được phép thực hiện.',
    phu='• Không đủ quyền xem phiếu → hệ thống từ chối, thông báo không có quyền xem phiếu này '
        'và đưa về màn danh sách.\n'
        '• Phiếu ở trạng thái Đang tạo của người khác → luôn bị từ chối, kể cả người có quyền V1.\n'
        '• Phiếu vừa bị xóa ở nơi khác → hệ thống báo không tải được phiếu và đưa về danh sách.',
    dacbiet=None)

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết',
         shot=shot('15-chi-tiet.png'),
         shot_caption='Màn chi tiết phiếu đề nghị thu tiền')

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu đề nghị thu tiền: <mã phiếu>',
     'Hiển thị cả trên thanh tiêu đề và tiêu đề tab trình duyệt.'),
    ('Khối Thông tin chung', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Gồm Mã phiếu, Loại thu, Loại tiền, Tỷ giá, Người tạo, Phòng ban, Lý do thu — mọi ô đều khóa.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Bấm vào ô đối tượng không mở cửa sổ chọn; có dòng Tổng cộng.'),
    ('Cột Số tiền còn nợ', 'Number', 'Read-only', '≥ 0', 'Theo sổ kế toán',
     'Tính lại tại thời điểm mở phiếu, không lấy giá trị đã lưu.'),
    ('Khối Ghi chú', 'Textarea', 'Read-only', '–', 'Theo dữ liệu',
     'Với phiếu bị từ chối, hiển thị lý do không duyệt.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu của chính mình ở trạng thái Đang tạo hoặc Không duyệt.'),
    ('Nút Tạo phiếu thu', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Chỉ hiện với người có quyền Kế toán thanh toán, phiếu đang Chờ KT duyệt và chưa có phiếu '
     'thu nào lập từ phiếu này.'),
    ('Nút In phiếu', 'Button', 'Enable', '–', 'Hiển thị', 'Mở bản in ở tab mới.'),
    ('Nút Không duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Chỉ hiện với người có quyền Kế toán thanh toán và phiếu đang Chờ KT duyệt.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Cùng điều kiện với nút Sửa.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
    ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Bấm Xem lịch sử để mở; nội dung như FR-12.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu theo cấp quyền và người lập.\n'
     '– Nếu không đủ quyền → hiển thị thông báo không có quyền xem phiếu này và đưa về danh sách.\n'
     'During:\n– Tính lại Số tiền còn nợ của từng dòng theo sổ kế toán.\n'
     'After:\n– Hiển thị dữ liệu ở chế độ chỉ đọc và bộ nút phù hợp với trạng thái, quyền.'),
    ('Bấm nút Sửa', 'Click', 'After:\n– Chuyển sang màn sửa phiếu (FR-06).'),
    ('Bấm nút In phiếu', 'Click', 'After:\n– Mở bản in của phiếu ở tab mới (FR-11).'),
    ('Bấm nút Quay lại', 'Click',
     'After:\n– Về màn danh sách, không hỏi xác nhận vì màn chi tiết không sửa được gì.'),
])

# ---------------------------------------------------------------- 2.8 FR-08
d.h3('2.8 Xem danh sách phiếu chờ duyệt')

d.p('2.8.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung điều '
           'kiện lọc riêng của màn chờ duyệt.',
           anchor='list')
d.intro_table(
    ten='Xem danh sách phiếu đề nghị thu tiền chờ duyệt',
    mota='Màn riêng của kế toán thanh toán, liệt kê các phiếu đang ở trạng thái Chờ KT duyệt '
         'thuộc công ty của người đăng nhập để xử lý.',
    tacnhan='Kế toán thanh toán',
    dieukien='Người dùng có quyền Kế toán thanh toán.',
    chinh='1. Người dùng vào menu Phê duyệt - Công nợ - Thu - Chi → Phiếu đề nghị thu tiền chờ '
          'duyệt.\n'
          '2. Hệ thống kiểm tra quyền Kế toán thanh toán.\n'
          '3. Hệ thống lọc phiếu ở trạng thái Chờ KT duyệt và thuộc công ty của người đăng nhập.\n'
          '4. Bảng hiển thị danh sách với cùng bộ cột như màn danh sách.',
    phu='• Không có quyền Kế toán thanh toán → mục menu không hiển thị; truy cập trực tiếp bằng '
        'đường dẫn thì hệ thống không trả về phiếu nào, bảng hiện rỗng, trang không bị lỗi.\n'
        '• Người dùng có thêm quyền V1 vẫn không thấy phiếu của công ty khác ở màn này.\n'
        '• Bộ lọc của màn này lưu riêng, không dùng chung với màn danh sách.',
    dacbiet='Màn dùng chung giao diện với màn danh sách nhưng bỏ nút Tạo mới và bỏ nút Sửa, '
            'Xóa ở cột Hành động.')

d.p('2.8.2 Layout màn hình')
d.layout(menu=MENU_PENDING,
         shot=shot('14-cho-duyet.png'),
         shot_caption='Màn Phiếu đề nghị thu tiền chờ duyệt')

d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Phiếu đề nghị thu tiền chờ duyệt', '–'),
    ('Khối bộ lọc', 'Table/Grid', 'Enable', '–', 'Theo cấu hình người dùng',
     'Cùng bộ tiêu chí với màn danh sách, nhưng lưu riêng.'),
    ('Bảng danh sách', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Cùng bộ cột với màn danh sách; mọi dòng đều ở trạng thái Chờ KT duyệt.'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Không hiển thị ở màn này.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo quyền',
     'Chỉ còn In phiếu, Tạo phiếu thu và Lịch sử; không có Sửa và Xóa.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện khi không có phiếu nào chờ duyệt hoặc người dùng thiếu quyền.'),
], required=False)

d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chờ duyệt', 'System',
     'Before:\n– Kiểm tra quyền Kế toán thanh toán; không có quyền thì không trả về dữ liệu.\n'
     'During:\n– Lọc phiếu ở trạng thái Chờ KT duyệt và thuộc công ty của người đăng nhập.\n'
     'After:\n– Hiển thị danh sách kèm phân trang; bảng rỗng nếu không có phiếu nào.'),
    ('Bấm vào mã phiếu', 'Click', 'After:\n– Mở màn chi tiết phiếu (FR-07) với đủ nút xử lý.'),
])

# ---------------------------------------------------------------- 2.9 FR-09
d.h3('2.9 Không duyệt phiếu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Không duyệt phiếu', 'action',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Kiểm tra phiếu đang ở trạng thái Chờ KT duyệt'),
             ('include', 'Ghi lý do từ chối bắt buộc')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-09 Không duyệt phiếu')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.',
           anchor='history')
d.intro_table(
    ten='Không duyệt phiếu đề nghị thu tiền',
    mota='Kế toán thanh toán từ chối một phiếu đang chờ duyệt kèm lý do bắt buộc. Phiếu chuyển '
         'sang trạng thái Không duyệt và quay lại cho người lập chỉnh sửa.',
    tacnhan='Kế toán thanh toán',
    dieukien='Người dùng có quyền Kế toán thanh toán và phiếu đang ở trạng thái Chờ KT duyệt.',
    chinh='1. Người dùng mở màn chi tiết phiếu và bấm nút Không duyệt.\n'
          '2. Hệ thống mở hộp thoại Không duyệt phiếu kèm mã phiếu.\n'
          '3. Người dùng nhập Lý do không duyệt và bấm nút Không duyệt.\n'
          '4. Hệ thống kiểm tra quyền, trạng thái phiếu và lý do.\n'
          '5. Hệ thống chuyển phiếu sang trạng thái Không duyệt, ghi lý do vào ô Ghi chú của '
          'phiếu và ghi nhận người xử lý.\n'
          '6. Hệ thống hiển thị thông báo thành công, đóng hộp thoại và nạp lại màn chi tiết.',
    phu='• Bỏ trống lý do (kể cả chỉ nhập khoảng trắng) → báo lỗi đỏ ngay dưới ô: “Bắt buộc nhập '
        'lý do không duyệt”, hộp thoại không đóng, trạng thái phiếu không đổi.\n'
        '• Không có quyền Kế toán thanh toán → nút không hiển thị; gọi thẳng chức năng thì hệ '
        'thống từ chối với thông báo không có quyền duyệt phiếu đề nghị thu.\n'
        '• Phiếu không còn ở trạng thái Chờ KT duyệt (kế toán khác vừa xử lý) → hệ thống báo dữ '
        'liệu đã được thay đổi và đề nghị tải lại trang.\n'
        '• Bấm Đóng → thoát hộp thoại, phiếu không đổi; mở lại thì ô lý do trở về trống.',
    dacbiet='Màn hình này không có nút Duyệt. Việc chấp thuận phiếu được thực hiện bằng nút Tạo '
            'phiếu thu, dẫn sang màn Phiếu thu; trạng thái phiếu đề nghị chỉ chuyển sang Đã tạo '
            'phiếu thu khi phiếu thu được lập và gửi duyệt ở màn đó.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU_PENDING + ' => Xem chi tiết => Không duyệt',
         modal='Không duyệt phiếu',
         shot=shot('17-khong-duyet.png'),
         shot_caption='Hộp thoại Không duyệt phiếu')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', '–', '–', 'Không duyệt phiếu',
     'Dòng phụ hiển thị mã phiếu đang xử lý.'),
    ('Lý do không duyệt', 'Textarea', 'Enable', '0–1000 ký tự', 'Có', 'Trống',
     'Bỏ trống thì báo “Bắt buộc nhập lý do không duyệt”. Nội dung được ghi vào ô Ghi chú của '
     'phiếu và hiển thị trên bản in, trong lịch sử thay đổi.'),
    ('Nút Không duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Bị khóa trong lúc đang xử lý để tránh gửi hai lần.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng hộp thoại, không thay đổi phiếu.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô Lý do không duyệt.'),
])

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Không duyệt ở màn chi tiết', 'Click',
     'Before:\n– Nút chỉ hiển thị khi người dùng có quyền Kế toán thanh toán và phiếu đang ở '
     'trạng thái Chờ KT duyệt.\n'
     'After:\n– Mở hộp thoại với ô lý do để trống và xóa mọi thông báo lỗi cũ.'),
    ('Bấm nút Không duyệt trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền Kế toán thanh toán; không có quyền → hiển thị thông báo không '
     'có quyền duyệt phiếu đề nghị thu và dừng xử lý.\n'
     '– Kiểm tra phiếu còn ở trạng thái Chờ KT duyệt; nếu không → hiển thị thông báo dữ liệu đã '
     'được thay đổi và đề nghị tải lại trang.\n'
     'During:\n– Lý do trống hoặc chỉ có khoảng trắng → hiển thị “Bắt buộc nhập lý do không '
     'duyệt” và dừng, không đóng hộp thoại.\n'
     'After:\n– Chuyển phiếu sang trạng thái Không duyệt, ghi lý do vào ô Ghi chú và ghi nhận '
     'người xử lý.\n'
     '– Ghi một dòng lịch sử “Thay đổi trạng thái” từ Chờ KT duyệt sang Không duyệt kèm lý do.\n'
     '– Hiển thị “Không duyệt phiếu đề nghị thu thành công!”, đóng hộp thoại và nạp lại màn chi '
     'tiết.'),
    ('Bấm nút Tạo phiếu thu', 'Click',
     'Before:\n– Nút chỉ hiển thị khi người dùng có quyền Kế toán thanh toán, phiếu đang Chờ KT '
     'duyệt và chưa có phiếu thu nào lập từ phiếu này.\n'
     'After:\n– Chuyển sang màn lập Phiếu thu, gắn sẵn phiếu đề nghị hiện tại. Trạng thái phiếu '
     'đề nghị chưa đổi tại bước này.'),
])

# ---------------------------------------------------------------- 2.10 FR-10
d.h3('2.10 Xóa phiếu')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu', 'action',
            [('include', 'Kiểm tra phiếu do chính người dùng lập'),
             ('include', 'Kiểm tra trạng thái Đang tạo hoặc Không duyệt')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa, Thông báo và Quy tắc ghi lịch sử.',
           anchor='notice')
d.intro_table(
    ten='Xóa phiếu đề nghị thu tiền',
    mota='Xóa hẳn một phiếu cùng toàn bộ dòng chi tiết của phiếu đó. Dữ liệu không khôi phục được.',
    tacnhan='Người lập phiếu',
    dieukien='Phiếu do chính người đăng nhập lập và đang ở trạng thái Đang tạo hoặc Không duyệt.',
    chinh='1. Người dùng bấm nút ba chấm ở cột Hành động rồi chọn Xóa (hoặc bấm nút Xóa ở màn '
          'chi tiết).\n'
          '2. Hệ thống hiển thị hộp xác nhận kèm mã phiếu sắp xóa.\n'
          '3. Người dùng bấm nút Xóa.\n'
          '4. Hệ thống kiểm tra người lập và trạng thái phiếu.\n'
          '5. Hệ thống ghi lịch sử xóa, xóa các dòng chi tiết và xóa phiếu.\n'
          '6. Hệ thống hiển thị “Xóa thành công” và nạp lại danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, phiếu giữ nguyên.\n'
        '• Phiếu không phải của người đăng nhập → nút không hiển thị; gọi thẳng chức năng thì hệ '
        'thống từ chối với thông báo không có quyền xóa phiếu này.\n'
        '• Phiếu vừa bị người khác đổi trạng thái → hệ thống báo dữ liệu đã được thay đổi và '
        'nạp lại danh sách.',
    dacbiet='Mã phiếu đã dùng không được cấp lại cho phiếu mới sau khi xóa.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa',
         modal='Xác nhận xóa',
         shot=shot('19-xac-nhan-xoa.png'),
         shot_caption='Hộp thoại Xác nhận xóa phiếu')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', '–'),
    ('Nội dung xác nhận', 'Label', 'Hiển thị', 'Bạn có chắc muốn xóa phiếu đề nghị thu tiền '
     '‘<mã phiếu>’?', 'Hiển thị đúng mã phiếu của dòng đang thao tác.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa phiếu.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     'Hiện “Xóa thành công” hoặc thông báo lỗi tương ứng.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm mục Xóa', 'Click',
     'Before:\n– Mục chỉ hiển thị khi phiếu do chính người dùng lập và đang ở trạng thái Đang '
     'tạo hoặc Không duyệt.\n'
     'After:\n– Mở hộp xác nhận kèm mã phiếu.'),
    ('Bấm nút Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra phiếu do chính người dùng lập; nếu không → từ chối với thông báo '
     'không có quyền xóa phiếu này và dừng xử lý.\n'
     '– Kiểm tra phiếu còn ở trạng thái Đang tạo hoặc Không duyệt; nếu không → hiển thị thông '
     'báo dữ liệu đã được thay đổi và nạp lại danh sách.\n'
     'After:\n– Ghi một dòng lịch sử “Xóa” kèm ảnh chụp nội dung phiếu trước khi xóa.\n'
     '– Xóa toàn bộ dòng chi tiết rồi xóa phiếu.\n'
     '– Hiển thị “Xóa thành công” và nạp lại danh sách.'),
    ('Bấm nút Hủy', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.11 FR-11
d.h3('2.11 In phiếu')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'In phiếu', 'io',
            [('include', 'Nạp lại dữ liệu phiếu và số tiền còn nợ'),
             ('extend', 'Đổi nhãn ghi chú thành lý do không duyệt')],
            actor='Người dùng xem được phiếu',
            caption='Biểu đồ Use Case — FR-11 In phiếu')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Thông báo và UI/UX. Chỉ bổ sung bố cục và dữ liệu riêng của bản in Giấy đề nghị '
           'thu tiền.',
           anchor='list')
d.intro_table(
    ten='In phiếu đề nghị thu tiền',
    mota='Mở bản in Giấy đề nghị thu tiền của một phiếu ở tab mới và gửi lệnh in tới trình duyệt.',
    tacnhan='Người lập phiếu; Kế toán thanh toán; Người dùng đã đăng nhập',
    dieukien='Phiếu nằm trong phạm vi dữ liệu người dùng được xem. Chức năng không gắn quyền riêng.',
    chinh='1. Người dùng bấm nút In phiếu ở cột Hành động hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở tab mới với bản in của phiếu.\n'
          '3. Hệ thống nạp dữ liệu phiếu, tính lại Số tiền còn nợ và dựng bản in.\n'
          '4. Người dùng bấm nút In để mở hộp thoại in của trình duyệt.',
    phu='• Phiếu ở trạng thái Không duyệt → nhãn dòng ghi chú đổi thành “Lý do không duyệt:”.\n'
        '• Phiếu loại Thu nhà cung cấp → hai cột đổi nhãn thành Nhà cung cấp và Hợp đồng mua.\n'
        '• Không tải được phiếu → hệ thống hiển thị thông báo lỗi tương ứng.',
    dacbiet='Bản in không hiển thị nút In và menu bên trái; bảng chi tiết giữ đủ viền khi sang '
            'trang mới.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In phiếu',
         shot=shot('23-in-phieu.png'),
         shot_caption='Bản in Giấy đề nghị thu tiền')

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở hộp thoại in của trình duyệt; không xuất hiện trên bản in.'),
    ('Logo và thông tin công ty', 'Icon Button', 'Hiển thị', '–', 'Theo cấu hình',
     'Nằm ở đầu trang in.'),
    ('Tiêu đề bản in', 'Label', 'Hiển thị', '–', 'GIẤY ĐỀ NGHỊ THU TIỀN', 'Canh giữa, in đậm.'),
    ('Dòng số phiếu và ngày lập', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Dạng “Số phiếu: <mã> · Ngày lập: <ngày giờ>”.'),
    ('Khối thông tin hai cột', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Trái: Người đề nghị, Loại thu, Trạng thái. Phải: Phòng ban, Loại tiền (kèm tỷ giá), '
     'Lý do thu. Bản in không có dòng Người nộp tiền.'),
    ('Bảng chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'STT, Khách hàng / Nhà cung cấp, Số đơn hàng/Hợp đồng hoặc Hợp đồng mua, Số tiền còn nợ, '
     'Số tiền đề nghị thu, Ghi chú.'),
    ('Dòng tổng cộng', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Nhãn “Tổng cộng (quy đổi VND)”.'),
    ('Dòng ghi chú', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Nhãn “Ghi chú:”; với phiếu Không duyệt đổi thành “Lý do không duyệt:”.'),
    ('Khối ký tên', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Ba ô NGƯỜI ĐỀ NGHỊ, KẾ TOÁN, GIÁM ĐỐC kèm dòng “(Ký, ghi rõ họ tên)”; ô Người đề nghị '
     'điền sẵn tên người lập, ô Kế toán điền sẵn tên người đã xử lý.'),
], required=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In phiếu', 'Click',
     'After:\n– Mở tab mới tới bản in của phiếu tương ứng.'),
    ('Mở bản in', 'System',
     'During:\n– Nạp dữ liệu phiếu và tính lại Số tiền còn nợ của từng dòng.\n'
     'After:\n– Dựng bản in với nhãn cột và nhãn ghi chú theo loại thu và trạng thái của phiếu.'),
    ('Bấm nút In trên bản in', 'Click',
     'After:\n– Mở hộp thoại in của trình duyệt, ẩn nút In và menu bên trái khỏi bản in.'),
])

# ---------------------------------------------------------------- 2.12 FR-12
d.h3('2.12 Xem lịch sử thay đổi')

d.p('2.12.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung các trường được ghi lịch sử '
           'riêng của Phiếu đề nghị thu tiền.',
           anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Hiển thị toàn bộ thao tác đã tác động lên phiếu theo dòng thời gian: tạo mới, thay '
         'đổi thông tin, thay đổi trạng thái, kèm người thực hiện và giá trị trước / sau.',
    tacnhan='Người lập phiếu; Kế toán thanh toán; Người dùng đã đăng nhập',
    dieukien='Phiếu nằm trong phạm vi dữ liệu người dùng được xem. Chức năng không gắn quyền riêng.',
    chinh='1. Người dùng bấm nút Lịch sử ở cột Hành động, hoặc bấm Xem lịch sử ở khối Lịch sử '
          'cuối màn chi tiết.\n'
          '2. Hệ thống nạp các mốc thay đổi của phiếu.\n'
          '3. Hệ thống hiển thị danh sách mốc theo thứ tự thời gian, mốc mới nhất ở trên.',
    phu='• Phiếu chưa từng có thao tác nào trên màn hình này → hiển thị “Chưa có lịch sử thao '
        'tác nào.”.\n'
        '• Bấm Làm mới ở khối Lịch sử → nạp lại các mốc mới nhất.\n'
        '• Bấm Thu gọn → đóng khối Lịch sử.',
    dacbiet=None)

d.p('2.12.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử',
         modal='Lịch sử thay đổi',
         shot=shot('20-popup-lich-su.png'),
         shot_caption='Cửa sổ Lịch sử thay đổi của một phiếu')
d.figure(shot('16-lich-su.png'), 'Khối Lịch sử ở cuối màn chi tiết', width_in=6.2)

d.p('2.12.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi',
     'Dòng phụ ghi “Phiếu: <mã phiếu>”.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc các mốc theo loại thao tác.'),
    ('Mốc thời gian', 'Label', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Kèm tên thao tác: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.'),
    ('Dòng người thực hiện', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Dạng “Người thực hiện: <tên> – <phòng ban>”.'),
    ('Khối giá trị thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi trường một dòng, mũi tên từ giá trị cũ sang giá trị mới; giá trị hiển thị bằng tên '
     'tiếng Việt chứ không phải mã.'),
    ('Khối thay đổi dòng chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Ghi rõ dòng nào được thêm, sửa hay bỏ, kèm đối tượng, hợp đồng và số tiền đề nghị thu.'),
    ('Lý do thao tác', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Hiển thị lý do không duyệt ở mốc chuyển sang trạng thái Không duyệt.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', 'Hiện “Chưa có lịch sử thao tác nào.”.'),
    ('Nút Đóng / Thu gọn', 'Button', 'Enable', '–', 'Hiển thị',
     'Đóng cửa sổ hoặc thu gọn khối Lịch sử.'),
], required=False)

d.p('2.12.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lịch sử ở cột Hành động', 'Click',
     'After:\n– Mở cửa sổ Lịch sử thay đổi và nạp các mốc của phiếu.'),
    ('Bấm nút Xem lịch sử ở màn chi tiết', 'Click',
     'After:\n– Mở khối Lịch sử; chỉ gọi dữ liệu ở lần mở đầu tiên; nút đổi thành Thu gọn.'),
    ('Bấm nút Làm mới', 'Click', 'After:\n– Nạp lại các mốc lịch sử mới nhất.'),
])

# ==================================================== PHẦN 4. QUY TẮC NGHIỆP VỤ
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Phiếu đề nghị thu tiền; không lặp lại '
           'các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Mã phiếu sinh tự động và duy nhất', [
        '– Mã phiếu do hệ thống sinh khi lưu lần đầu, theo dạng <mã công ty>.DNTT<tháng năm>.'
        '<5 chữ số>, số chạy tăng dần trong cùng công ty và cùng tháng.',
        '– Người dùng không nhập và không sửa được mã phiếu.',
        '– Hai người lưu phiếu cùng lúc vẫn nhận hai mã khác nhau; mã đã dùng không được cấp '
        'lại kể cả khi phiếu bị xóa.',
    ], 'Lập phiếu'),

    ('BR-02', 'Phạm vi dữ liệu theo cấp quyền xem', [
        '– Hệ thống xét quyền theo đúng thứ tự V1 → V2 → V3 → V4; cấp nào có trước thì áp cấp '
        'đó, người có nhiều quyền lấy phạm vi rộng nhất.',
        '– Không có cấp nào thì người dùng chỉ thấy phiếu do chính mình lập.',
        '– Quy tắc này áp cho cả màn danh sách và cho việc mở chi tiết một phiếu bằng đường dẫn '
        'trực tiếp.',
    ], ['Xem danh sách', 'Xem chi tiết', 'In phiếu']),

    ('BR-03', 'Phiếu nháp của người khác luôn bị ẩn', [
        '– Phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy, kể cả người có quyền V1.',
        '– Quy tắc này áp cả ở danh sách lẫn khi mở chi tiết bằng đường dẫn trực tiếp.',
    ], ['Xem danh sách', 'Xem chi tiết']),

    ('BR-04', 'Ràng buộc dữ liệu khác nhau giữa Lưu nháp và Lưu và gửi duyệt', [
        '– Lưu nháp: cho phép bỏ trống Lý do thu và cho phép bảng Chi tiết chưa có dòng nào.',
        '– Lưu và gửi duyệt: bắt buộc có Lý do thu và ít nhất một dòng chi tiết.',
        '– Trong cả hai trường hợp, dòng chi tiết đã thêm đều phải có đủ đối tượng, hợp đồng và '
        'số tiền đề nghị thu; tỷ giá luôn phải lớn hơn 0.',
    ], ['Lập phiếu', 'Sửa phiếu']),

    ('BR-05', 'Điều kiện sửa và xóa phiếu', [
        '– Chỉ người lập phiếu mới sửa và xóa được phiếu của mình.',
        '– Chỉ sửa và xóa được khi phiếu đang ở trạng thái Đang tạo hoặc Không duyệt.',
        '– Hệ thống kiểm tra người lập trước, trạng thái sau: phiếu của người khác luôn báo '
        'thiếu quyền, còn phiếu của mình vừa bị đổi trạng thái thì báo dữ liệu đã được thay đổi.',
    ], ['Sửa phiếu', 'Xóa phiếu']),

    ('BR-06', 'Loại thu quyết định nguồn dữ liệu của bảng chi tiết', [
        '– Thu bán hàng: dòng chi tiết chọn khách hàng và hợp đồng bán.',
        '– Thu nhà cung cấp: dòng chi tiết chọn nhà cung cấp và hợp đồng mua.',
        '– Đổi Loại thu khi bảng đã có dòng thì toàn bộ dòng bị xóa; hệ thống hỏi xác nhận trước.',
        '– Giá trị Thu khác chỉ còn để hiển thị dữ liệu cũ, không xuất hiện trong danh sách chọn.',
    ], ['Lập phiếu', 'Sửa phiếu']),

    ('BR-07', 'Mỗi dòng chi tiết chọn đối tượng riêng', [
        '– Một phiếu được phép gom nhiều khách hàng hoặc nhiều nhà cung cấp khác nhau, mỗi dòng '
        'một đối tượng.',
        '– Cửa sổ chọn hợp đồng luôn lọc theo đối tượng của chính dòng đang thao tác.',
        '– Đổi đối tượng của một dòng thì hợp đồng đã chọn của dòng đó bị xóa và Số tiền còn nợ '
        'về 0.',
        '– Cột Khách hàng / Nhà cung cấp trên danh sách chỉ hiển thị đối tượng của dòng chi tiết '
        'đầu tiên.',
    ], ['Lập phiếu', 'Sửa phiếu', 'Xem danh sách']),

    ('BR-08', 'Nguồn hợp đồng được phép chọn', [
        '– Hợp đồng bán lấy từ ba nguồn: hợp đồng bán, hợp đồng đầu kỳ và hợp đồng bảo dưỡng '
        'của khách hàng.',
        '– Hợp đồng bán chỉ lấy các hợp đồng từ trạng thái Có hiệu lực trở lên: Có hiệu lực, '
        'Đang xuất hàng, Đã xuất hàng, Đã thanh lý, Đang quyết toán, Đã quyết toán.',
        '– Hợp đồng mua lấy từ năm nguồn hợp đồng mua của nhà cung cấp.',
        '– Cửa sổ hợp đồng bắt buộc phải có đối tượng của dòng; gọi thẳng chức năng mà thiếu '
        'đối tượng thì hệ thống yêu cầu chọn khách hàng (hoặc nhà cung cấp) trước.',
    ], 'Chọn đối tượng và hợp đồng'),

    ('BR-09', 'Một hợp đồng chỉ chọn một lần trong cùng phiếu', [
        '– Hợp đồng đã có ở một dòng vẫn hiển thị trong cửa sổ nhưng bị đánh dấu và không chọn '
        'lại được.',
        '– Quy tắc xét theo cặp loại hợp đồng và hợp đồng cụ thể, không xét theo số hợp đồng '
        'hiển thị.',
    ], 'Chọn đối tượng và hợp đồng'),

    ('BR-10', 'Tỷ giá và quy đổi VND', [
        '– Loại tiền VNĐ: tỷ giá luôn bằng 1, ô bị khóa, bảng chi tiết chỉ có một cột số tiền.',
        '– Loại tiền khác VNĐ: hệ thống tự điền tỷ giá của loại tiền đó khi người dùng đổi loại '
        'tiền; người dùng vẫn sửa tay được.',
        '– Số tiền quy đổi VND của một dòng bằng Số tiền đề nghị thu nhân với tỷ giá; dòng Tổng '
        'cộng cộng dồn ngay theo từng phím gõ.',
        '– Tỷ giá bằng 0 hoặc để trống thì hệ thống báo “Phải lớn hơn 0” và không cho lưu.',
    ], ['Lập phiếu', 'Sửa phiếu']),

    ('BR-11', 'Số tiền còn nợ tính theo sổ kế toán, không lưu trong phiếu', [
        '– Số tiền còn nợ được tính lại mỗi lần mở phiếu hoặc mở cửa sổ chọn hợp đồng, dựa trên '
        'sổ công nợ của hợp đồng.',
        '– Phiếu Thu bán hàng lấy công nợ phải thu của khách hàng; phiếu Thu nhà cung cấp lấy '
        'công nợ phải trả của nhà cung cấp.',
        '– Hợp đồng chưa phát sinh bút toán kế toán thì giá trị hiển thị bằng 0 — đây là hiện '
        'trạng đã được chấp nhận, không phải lỗi dữ liệu.',
    ], ['Lập phiếu', 'Sửa phiếu', 'Xem chi tiết']),

    ('BR-12', 'Thông báo cho kế toán khi gửi duyệt', [
        '– Khi phiếu chuyển sang trạng thái Chờ KT duyệt, hệ thống gửi thông báo cho tất cả '
        'người có quyền Kế toán thanh toán thuộc CÙNG CÔNG TY với phiếu.',
        '– Nội dung theo dạng “[DNTT] Chờ duyệt: <mã phiếu>. Người đề nghị: <tên>. Số tiền: '
        '<tổng tiền>”; bấm vào thông báo mở đúng phiếu.',
        '– Sửa lại một phiếu vốn đã ở trạng thái Chờ KT duyệt thì không gửi thông báo thêm lần '
        'nào.',
        '– Lỗi gửi thông báo không làm hỏng việc lưu phiếu.',
    ], ['Lập phiếu', 'Sửa phiếu']),

    ('BR-13', 'Xử lý phiếu chờ duyệt của kế toán', [
        '– Màn chờ duyệt chỉ hiển thị phiếu ở trạng thái Chờ KT duyệt và thuộc công ty của '
        'người đăng nhập, kể cả người đó có quyền V1.',
        '– Không duyệt: bắt buộc nhập lý do; phiếu chuyển sang trạng thái Không duyệt, lý do '
        'ghi vào ô Ghi chú và hệ thống ghi nhận người xử lý.',
        '– Màn hình này không có nút Duyệt: việc chấp thuận thực hiện bằng nút Tạo phiếu thu, '
        'dẫn sang màn Phiếu thu.',
        '– Nút Tạo phiếu thu bị ẩn khi đã tồn tại một phiếu thu lập từ phiếu đề nghị này, kể cả '
        'phiếu thu còn ở dạng nháp; nút Không duyệt vẫn hiển thị trong trường hợp đó.',
    ], ['Xem danh sách phiếu chờ duyệt', 'Không duyệt phiếu']),

    ('BR-14', 'Ba trạng thái do màn Phiếu thu đặt', [
        '– Màn Phiếu đề nghị thu tiền chỉ đặt hai trạng thái: Chờ KT duyệt (khi gửi duyệt) và '
        'Không duyệt (khi kế toán từ chối).',
        '– Ba trạng thái Đã tạo phiếu thu, Đã hạch toán và Hủy do màn Phiếu thu đặt; màn này '
        'chỉ hiển thị và không cho thao tác gì làm thay đổi phiếu.',
    ], 'Toàn màn hình'),

    ('BR-15', 'Xử lý xung đột khi nhiều người thao tác cùng lúc', [
        '– Khi phiếu vừa bị người khác đổi trạng thái, mọi thao tác ghi (lưu, xóa, không duyệt) '
        'đều bị từ chối với thông báo: “Thao tác không thành công. Dữ liệu đã được thay đổi '
        'hoặc chuyển trạng thái bởi người dùng khác. Vui lòng tải lại trang để cập nhật thông '
        'tin mới nhất.”.',
        '– Thông báo này khác hẳn thông báo thiếu quyền: thiếu quyền nghĩa là phiếu không phải '
        'của người dùng, còn thông báo này nghĩa là dữ liệu đã cũ.',
        '– Hai kế toán cùng không duyệt một phiếu thì chỉ ghi nhận một lần, lịch sử không sinh '
        'hai mốc trùng nhau.',
    ], ['Sửa phiếu', 'Xóa phiếu', 'Không duyệt phiếu']),

    ('BR-16', 'Ghi lịch sử thay đổi', [
        '– Mọi thao tác tạo mới, sửa, xóa và đổi trạng thái đều được ghi một dòng lịch sử kèm '
        'người thực hiện và thời điểm.',
        '– Giá trị trong lịch sử lưu theo tên hiển thị tiếng Việt (loại thu, loại tiền, trạng '
        'thái) nên đổi tên danh mục về sau không làm sai lịch sử cũ.',
        '– Bảng chi tiết được ghi theo TỪNG DÒNG: sửa một ô số tiền chỉ in đúng dòng đó, không '
        'in lại cả bảng.',
        '– Thao tác Không duyệt ghi kèm lý do mà kế toán đã nhập.',
        '– Lỗi ghi lịch sử không làm hỏng thao tác nghiệp vụ đang thực hiện.',
    ], 'Toàn màn hình'),

    ('BR-17', 'Ghi nhớ bộ lọc và cấu hình hiển thị theo người dùng', [
        '– Bộ lọc đang áp dụng được ghi nhớ trong 10 phút để khôi phục khi người dùng quay lại '
        'màn hình; sau 10 phút tự hết hiệu lực.',
        '– Bộ lọc của màn danh sách và màn chờ duyệt lưu riêng, không ảnh hưởng lẫn nhau.',
        '– Cấu hình tiêu chí lọc và cấu hình cột lưu riêng theo từng người dùng; cấu hình cột '
        'dùng chung giữa hai màn vì hai màn có cùng bộ cột.',
        '– Ba cột STT, Mã phiếu và Hành động luôn hiển thị và không đổi vị trí được.',
    ], ['Xem danh sách', 'Tìm kiếm và lọc', 'Cài đặt bộ lọc']),
])

d.save()
