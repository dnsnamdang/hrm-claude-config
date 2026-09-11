# -*- coding: utf-8 -*-
"""Sinh SRS (.docx) cho man "Phieu de nghi thanh toan" theo FORM CHUAN
(ban mau: .claude/skills/srs-documenter/assets/SRS_MAU.docx = SRS Danh muc khach hang).

Anh chup that dung CHUNG voi HDSD: dntt_chi_shots/ (khong commit).

Chay:  python .plans/gop-db/finance-bill-payment-request/gen_srs.py
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

SHOTS = os.path.join(HERE, 'dntt_chi_shots')
OUT = os.path.join(HERE, 'SRS - Phiếu đề nghị thanh toán.docx')

HOST = 'http://hrm-crm.eteksofts.com'
ROUTE = '/finance/bill-payment-requests'

# Form 2026-08-28: muc Layout ghi DUONG DAN MENU (khong con "URL day du").
# Nhan menu lay tu hrm-client/components/subsystem-menu/finance.js.
MENU = ('Phân hệ Tài chính => Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi '
        '=> Đề nghị thanh toán')
MENU_PENDING = ('Phân hệ Tài chính => Phê duyệt - Công nợ - Thu - Chi '
                '=> Phiếu đề nghị thanh toán chờ duyệt')

ACTOR_LAP = 'Người lập phiếu (kinh doanh)'
ACTOR_DUYET = 'Cấp duyệt (TP / KT công nợ / KT trưởng / BGĐ)'
ACTOR_KTTT = 'Kế toán thanh toán'


def shot(name):
    return os.path.join(SHOTS, name)


d = SrsDoc(out=OUT,
           menu=MENU,
           route=ROUTE,
           full_url=HOST + ROUTE,
           img_prefix='dnttchi_')

# ============================================================== TRANG ĐẦU
d.title_block('Phiếu đề nghị thanh toán')
d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1. GIỚI THIỆU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu đề nghị thanh toán thuộc phân hệ '
    'Tài chính, nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa nghiệp vụ, phân tích, phát triển và kiểm thử cho toàn bộ vòng đời '
    'một phiếu đề nghị thanh toán: lập nháp → gửi duyệt → 4 cấp duyệt → chờ tạo phiếu chi.',
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ cách một màn hình phục vụ bốn chế độ xem (Tất cả · Của tôi · Chờ duyệt · Đã duyệt) '
    'với phạm vi dữ liệu khác nhau ở từng chế độ.',
    'Làm rõ ma trận ràng buộc dữ liệu theo bốn loại chi nhân hai hình thức thanh toán — mỗi tổ '
    'hợp bắt buộc một bộ trường khác nhau.',
    'Làm rõ quy tắc từ chối: cấp Trưởng phòng đưa phiếu về “Đang tạo”, các cấp sau đưa phiếu '
    'sang “Không duyệt”.',
    'Làm rõ ranh giới với màn Phiếu chi và Ủy nhiệm chi: màn này dừng ở trạng thái Chờ tạo '
    'phiếu chi.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu đề nghị thanh toán',
     'Chứng từ đề nghị chi tiền do bộ phận kinh doanh lập, đi qua luồng duyệt nhiều cấp trước '
     'khi kế toán lập chứng từ chi.'),
    ('Loại chi',
     'Phân loại khoản chi. Bốn giá trị chọn được: Chi trả nhà cung cấp (1) · Chi trả lại khách '
     'hàng (2) · Chi thưởng thực hiện hợp đồng (6) · Thanh toán chi phí vận chuyển NCC (12). Ba '
     'loại cũ (Chi thưởng NVKD, Chi thu nhập cho nhân viên, Chi khác) chỉ còn để hiển thị dữ '
     'liệu cũ.'),
    ('Hình thức thanh toán',
     'TM là tiền mặt, CK là chuyển khoản. Quyết định việc chọn đối tượng nhận tiền theo phiếu '
     'hay theo từng dòng chi tiết, và quyết định có khối Thông tin ngân hàng hay không.'),
    ('Dòng chi tiết',
     'Một dòng trong bảng Chi tiết. Nội dung cột đổi theo loại chi: hợp đồng mua, hợp đồng bán '
     'hoặc chuyến xe.'),
    ('Cột tiền theo cấp',
     'Bảng chi tiết ở màn xem có bốn cột tiền: TP duyệt · KT công nợ duyệt · KT trưởng / BGĐ '
     'duyệt · Số tiền chi. Cấp Kế toán trưởng và Ban giám đốc dùng chung một cột.'),
    ('Số tiền chi',
     'Số tiền thực chi, lấy từ phiếu chi hoặc giấy ủy nhiệm chi lập từ phiếu đề nghị này. Chưa '
     'có chứng từ chi thì hiển thị dấu gạch dưới.'),
    ('Đang tạo', 'Phiếu nháp; chỉ người lập nhìn thấy, sửa và xóa được.'),
    ('Chờ TP duyệt', 'Đang chờ Trưởng phòng của phòng ban người lập xử lý.'),
    ('Chờ kế toán công nợ duyệt', 'Đã qua Trưởng phòng, đang chờ Kế toán công nợ.'),
    ('Chờ kế toán trưởng duyệt', 'Đã qua Kế toán công nợ, đang chờ Kế toán trưởng.'),
    ('Chờ ban giám đốc duyệt', 'Kế toán trưởng đã chuyển lên Ban giám đốc.'),
    ('Chờ tạo phiếu chi', 'Đã duyệt xong, chờ kế toán thanh toán lập chứng từ chi.'),
    ('Không duyệt', 'Bị một cấp từ Kế toán công nợ trở lên từ chối; người lập sửa và gửi lại được.'),
    ('Chờ duyệt phiếu chi / Duyệt phiếu chi / Đã hủy',
     'Ba trạng thái do màn Phiếu chi và Ủy nhiệm chi đặt; màn này chỉ hiển thị.'),
    ('Chế độ xem',
     'Bốn cách lọc dữ liệu trên cùng một giao diện: Tất cả · Của tôi · Chờ duyệt · Đã duyệt.'),
], widths=[1.8, 4.2])

# ========================================================= PHẦN 2. PHÂN QUYỀN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kinh doanh đề nghị thanh toán',
     'Không mở thêm chức năng nào; dùng để xác định nhóm người nhận thông báo khi phiếu bị từ '
     'chối.'),
    ('Q2', 'Trưởng phòng duyệt đề nghị thanh toán',
     'Duyệt / từ chối phiếu ở trạng thái Chờ TP duyệt, thuộc phòng ban được giao quản lý, trong '
     'công ty của mình.'),
    ('Q3', 'Kế toán công nợ duyệt đề nghị thanh toán',
     'Duyệt / từ chối phiếu ở trạng thái Chờ kế toán công nợ duyệt, trong công ty của mình.'),
    ('Q4', 'Kế toán trưởng duyệt đề nghi thanh toán',
     'Duyệt thẳng sang Chờ tạo phiếu chi, hoặc chuyển sang Chờ ban giám đốc duyệt, hoặc từ chối '
     'phiếu ở trạng thái Chờ kế toán trưởng duyệt.'),
    ('Q5', 'Ban giám đốc duyệt đề nghi thanh toán',
     'Duyệt / từ chối phiếu ở trạng thái Chờ ban giám đốc duyệt.'),
    ('Q6', 'Kế toán thanh toán',
     'Xử lý phiếu ở trạng thái Chờ tạo phiếu chi: lập phiếu chi (tiền mặt) hoặc giấy ủy nhiệm '
     'chi (chuyển khoản).'),
], widths=[0.7, 2.1, 3.2])
d.p('Hai quyền Q4 và Q5 mang tên “duyệt đề nghi thanh toán” (thiếu dấu) đúng nguyên văn hệ thống '
    'cũ; cố ý giữ nguyên để đối chiếu dữ liệu.')

d.p('Nhóm quyền quyết định phạm vi dữ liệu ở chế độ Tất cả '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả phiếu đề nghị thanh toán của tổng công ty',
     'Phiếu của mọi công ty trong hệ thống.'),
    ('V2', 'Xem tất cả phiếu đề nghị thanh toán của công ty',
     'Phiếu thuộc công ty của người đăng nhập.'),
    ('V3', 'Xem tất cả phiếu đề nghị thanh toán của phòng ban',
     'Phiếu thuộc các phòng ban mà người đăng nhập được giao quản lý, trong công ty của mình.'),
    ('V4', 'Xem tất cả phiếu đề nghị thanh toán của bộ phận',
     'Phiếu thuộc các bộ phận mà người đăng nhập được giao quản lý, trong công ty của mình.'),
    ('—', '(không có cấp nào)', 'Chỉ phiếu do chính người đăng nhập lập.'),
], widths=[0.7, 2.1, 3.2])
d.p('Ràng buộc bổ sung: phiếu ở trạng thái Đang tạo của người khác luôn bị ẩn ở chế độ Tất cả, '
    'kể cả với người giữ V1. Nhóm quyền phạm vi KHÔNG áp cho chế độ Chờ duyệt và Đã duyệt — hai '
    'chế độ đó tự mang điều kiện riêng (đúng vai duyệt và cùng công ty; hoặc chính mình đã '
    'duyệt). Việc lập phiếu không gắn quyền; sửa và xóa chỉ áp cho phiếu do chính mình lập, khi '
    'phiếu ở trạng thái Đang tạo hoặc Không duyệt.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'V1–V4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách phiếu', '✅', '✅', '✅', '✅', '✅', '✅', '✅',
     '✅ (chỉ phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc danh sách', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc và tuỳ chỉnh cột', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Lập phiếu đề nghị thanh toán', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Chọn đối tượng và hợp đồng', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Lấy dữ liệu chuyến xe', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-07 Nạp khối thông tin ngân hàng', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-08 Quản lý file đính kèm', '✅', '✅', '✅', '✅', '✅', '✅', '✅',
     '✅ (phiếu của mình)'),
    ('FR-09 Sửa phiếu', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-10 Xem chi tiết phiếu', '✅', '✅', '✅', '✅', '✅', '✅', '✅',
     '✅ (chỉ phiếu của mình)'),
    ('FR-11 Duyệt phiếu theo cấp', '❌', '✅', '✅', '✅', '✅', '❌', '❌', '❌'),
    ('FR-12 Từ chối phiếu', '❌', '✅', '✅', '✅', '✅', '❌', '❌', '❌'),
    ('FR-13 Xóa phiếu', '✅', '✅', '✅', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-14 In phiếu và xuất Excel', '✅', '✅', '✅', '✅', '✅', '✅', '✅',
     '✅ (chỉ phiếu của mình)'),
    ('FR-15 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅', '✅', '✅',
     '✅ (chỉ phiếu của mình)'),
], widths=[1.75, 0.36, 0.36, 0.36, 0.36, 0.36, 0.36, 0.55, 1.14])
d.p('Ghi chú: dấu ✅ ở FR-11 và FR-12 chỉ có hiệu lực với phiếu đang ở ĐÚNG trạng thái của cấp '
    'đó, cùng công ty, và với Q2 thì phải đúng phòng ban được giao quản lý. Chức năng lập phiếu '
    'không gắn quyền nên mọi cột đều ✅.')

# ================================================ PHẦN 3. ĐẶC TẢ CHI TIẾT
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
# Chi 4 use case duoi day la "man hinh" that su -> noi thang toi actor. Cac thao tac con lai
# deu lam NGAY TREN mot trong 4 man do (loc / tuy chinh cot / xoa o man danh sach; chon doi
# tuong, lay chuyen xe, khoi ngan hang, file dinh kem trong form lap-sua; duyet, tu choi, in,
# lich su o man chi tiet) -> phai la use case phu, noi bang «include» / «extend».
d.overview_figure2(
    [(ACTOR_LAP, [0, 1, 2, 3]),
     (ACTOR_DUYET, [0, 3]),
     (ACTOR_KTTT, [0, 3])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-04', 'Lập phiếu đề nghị thanh toán', 'crud'),
     ('FR-09', 'Sửa phiếu', 'crud'),
     ('FR-10', 'Xem chi tiết phiếu', 'view')],
    [('FR-02', 'Tìm kiếm và lọc danh sách', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc và tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-13', 'Xóa phiếu', 'action', 'extend', [0], None),
     # 4 use case cua form lap phieu — man Sua (FR-09) dung CHUNG form nay, chi noi vao
     # FR-04 cho so do de doc (noi ca 2 cha thi 8 duong net dut chong len nhau).
     ('FR-05', 'Chọn đối tượng và hợp đồng', 'crud', 'include', [1], None),
     ('FR-06', 'Lấy dữ liệu chuyến xe', 'crud', 'extend', [1], None),
     ('FR-07', 'Nạp khối thông tin ngân hàng', 'crud', 'extend', [1], None),
     ('FR-08', 'Quản lý file đính kèm', 'io', 'include', [1], None),
     ('FR-11', 'Duyệt phiếu theo cấp', 'action', 'extend', [3], None),
     ('FR-12', 'Từ chối phiếu', 'action', 'extend', [3], None),
     ('FR-14', 'In phiếu và xuất Excel', 'io', 'extend', [3], None),
     ('FR-15', 'Xem lịch sử thay đổi', 'view', 'extend', [3], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu đề nghị thanh toán')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1 FR-01
d.h3('2.1 Xem danh sách phiếu đề nghị thanh toán')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. Chỉ bổ sung điều '
           'kiện dữ liệu riêng của bốn chế độ xem trên màn Phiếu đề nghị thanh toán.',
           anchor='list')
d.intro_table(
    ten='Xem danh sách phiếu đề nghị thanh toán',
    mota='Hiển thị bảng phiếu đề nghị thanh toán theo một trong bốn chế độ xem, kèm phân trang, '
         'sắp xếp và tổng số bản ghi khớp bộ lọc.',
    tacnhan='Người lập phiếu; Cấp duyệt; Kế toán thanh toán; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và đang ở phân hệ Tài chính.',
    chinh='1. Người dùng vào màn hình bằng menu hoặc bằng đường dẫn có tham số chế độ.\n'
          '2. Hệ thống xác định chế độ xem; giá trị lạ rơi về chế độ Tất cả.\n'
          '3. Hệ thống áp điều kiện dữ liệu của chế độ đó: Tất cả áp phạm vi quyền xem theo thứ '
          'tự V1 → V2 → V3 → V4 và ẩn phiếu nháp của người khác; Của tôi lấy phiếu do chính '
          'mình lập; Chờ duyệt lấy phiếu cùng công ty và đúng trạng thái mình có quyền duyệt; '
          'Đã duyệt lấy phiếu chính mình đã duyệt.\n'
          '4. Hệ thống trả về trang đầu tiên, sắp xếp phiếu lập gần nhất lên trước, kèm tổng số '
          'bản ghi.\n'
          '5. Bảng hiển thị dữ liệu theo cấu hình cột của người dùng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Ở chế độ Chờ duyệt mà người dùng không giữ vai duyệt nào → danh sách rỗng, không báo '
        'lỗi.\n'
        '• Vào lại màn trong vòng 10 phút sau khi rời đi → hệ thống khôi phục bộ lọc đã dùng của '
        'ĐÚNG chế độ đó.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU,
         note='Chế độ Chờ duyệt có lối vào riêng: %s. Hai chế độ Của tôi và Đã duyệt '
              'chuyển ngay trên màn hình.' % MENU_PENDING,
         shot=shot('01-danh-sach.png'),
         shot_caption='Màn danh sách ở chế độ Tất cả lúc mới truy cập')
d.figure(shot('06-cho-duyet.png'), 'Chế độ Chờ duyệt — không có nút Tạo mới', width_in=6.2)
d.figure(shot('26-cua-toi.png'), 'Chế độ Của tôi', width_in=6.2)

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Theo chế độ xem',
     'Phiếu đề nghị thanh toán / … của tôi / … chờ duyệt / … đã duyệt.'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Hiển thị',
     'Không gắn quyền. Ẩn ở chế độ Chờ duyệt và Đã duyệt.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột (FR-03).'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự liên tục',
     'Cột bắt buộc, không ẩn và không đổi vị trí được.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Liên kết mở màn chi tiết; sắp xếp được; cột bắt buộc.'),
    ('Cột Loại chi', 'Table/Grid', 'Read-only', 'Danh sách 7 giá trị', 'Theo dữ liệu',
     'Bốn loại đang dùng và ba loại cũ chỉ để hiển thị.'),
    ('Cột Hình thức TT', 'Table/Grid', 'Read-only', 'TM / CK', 'Theo dữ liệu', '–'),
    ('Cột Khách hàng / Nhà cung cấp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Nguồn đổi theo loại chi và hình thức thanh toán; sắp xếp được.'),
    ('Cột Lý do chi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Tự xuống dòng khi dài.'),
    ('Cột Số tiền', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Số tiền của cấp duyệt gần nhất, kèm mã loại tiền; canh phải.'),
    ('Cột Ngày lập', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Ngày nhận', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Ngày Trưởng phòng duyệt.'),
    ('Cột Người lập', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Phòng ban của người lập tại thời điểm lập phiếu.'),
    ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 10 giá trị', 'Theo dữ liệu',
     'Chỉ Duyệt phiếu chi nền xanh; sắp xếp được.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo quyền và trạng thái',
     'Cột bắt buộc. Gồm Sửa, Duyệt, Tạo phiếu chi / Tạo ủy nhiệm chi, In phiếu và nút ba chấm '
     '(Xuất Excel, Xóa, Lịch sử).'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc của chế độ đang xem.'),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách', '10', 'Đổi giá trị thì về trang 1.'),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
     'Có nút về đầu / lùi / số trang / tiến / về cuối.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi N = 0.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Ẩn', 'Hiện trong lúc nạp dữ liệu.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định chế độ xem từ đường dẫn; giá trị lạ rơi về chế độ Tất cả.\n'
     '– Không xác định được người đăng nhập → không trả về phiếu nào.\n'
     'During:\n– Áp điều kiện dữ liệu của chế độ đang xem.\n'
     '– Khôi phục bộ lọc đã lưu trong 10 phút gần nhất của chính chế độ đó và cấu hình cột của '
     'người dùng.\n'
     'After:\n– Trả về trang 1, sắp xếp theo ngày lập giảm dần, kèm tổng số bản ghi.'),
    ('Đổi chế độ xem', 'Change',
     'During:\n– Nạp lại bộ lọc đã lưu của chế độ mới.\n'
     'After:\n– Quay về trang 1 và nạp lại danh sách theo chế độ mới; tiêu đề trang đổi theo.'),
    ('Bấm vào mã phiếu', 'Click',
     'After:\n– Mở màn chi tiết của phiếu tương ứng (FR-10); bấm chuột phải mở được ở tab mới.'),
    ('Bấm tiêu đề cột có sắp xếp', 'Click',
     'Before:\n– Chỉ năm cột Mã phiếu, Khách hàng / Nhà cung cấp, Ngày lập, Ngày cập nhật, '
     'Trạng thái hỗ trợ sắp xếp.\n'
     'After:\n– Đổi chiều sắp xếp, quay về trang 1 và nạp lại danh sách.'),
    ('Bấm số trang / nút tiến lùi', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp dữ liệu trang mới, số thứ tự tiếp tục liên tục.'),
])

# ---------------------------------------------------------------- 2.2 FR-02
d.h3('2.2 Tìm kiếm và lọc danh sách')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc, Dropdown, Phân trang và quy tắc bộ lọc chọn nhiều giá '
           'trị. Chỉ bổ sung các tiêu chí tìm kiếm/lọc riêng của Phiếu đề nghị thanh toán.',
           anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu',
    mota='Thu hẹp danh sách theo mã phiếu, cấp tổ chức, loại chi, hình thức thanh toán, trạng '
         'thái, lý do chi, đối tượng nhận tiền, người lập, khoảng số tiền và khoảng ngày lập.',
    tacnhan='Người lập phiếu; Cấp duyệt; Kế toán thanh toán; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách, bất kỳ chế độ xem nào.',
    chinh='1. Người dùng bấm Tìm kiếm nâng cao để mở khối tiêu chí.\n'
          '2. Người dùng chọn hoặc nhập giá trị cho một hoặc nhiều tiêu chí.\n'
          '3. Hệ thống lọc ngay khi giá trị thay đổi và quay về trang 1.\n'
          '4. Riêng ô tìm nhanh theo mã phiếu chỉ lọc khi người dùng bấm nút Tìm kiếm.\n'
          '5. Hệ thống ghi nhớ bộ lọc trong 10 phút, riêng cho từng chế độ xem.',
    phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, nạp lại danh sách từ trang 1.\n'
        '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Đổi Công ty → hệ thống xóa giá trị đang chọn ở Phòng ban và Bộ phận.\n'
        '• Tiêu chí bị tắt trong Cài đặt bộ lọc → giá trị của tiêu chí đó bị xóa, danh sách '
        'không bị lọc ngầm.\n'
        '• Ô Khách hàng chỉ tìm trong danh sách khách hàng; gõ tên nhà cung cấp sẽ không ra kết '
        'quả — phải dùng ô Nhà cung cấp.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('02-bo-loc.png'),
         shot_caption='Khối Tìm kiếm nâng cao ở trạng thái mở với đủ 10 tiêu chí')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô Tìm theo mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo một phần mã phiếu; chỉ lọc khi bấm nút Tìm kiếm.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Áp giá trị ô tìm nhanh và quay về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa toàn bộ tiêu chí đang lọc.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở / thu gọn khối tiêu chí; khi mở, nhãn đổi thành Ẩn tìm kiếm nâng cao.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở cửa sổ chọn tiêu chí (FR-03).'),
    ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống', 'Chỉ hiện với V1.'),
    ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống',
     'Hiện với V1, V2, V3; chỉ liệt kê phòng ban của công ty đang chọn.'),
    ('Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Trống', 'Hiện với V4.'),
    ('Loại chi', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống', '–'),
    ('Hình thức thanh toán', 'Dropdown', 'Enable', 'TM / CK', 'Không', 'Trống', '–'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 10 giá trị', 'Không', 'Trống', '–'),
    ('Lý do chi', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo một phần nội dung lý do chi.'),
    ('Khách hàng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Danh sách tìm từ xa, cần nhập tối thiểu 2 ký tự.'),
    ('Nhà cung cấp', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Danh sách tìm từ xa, cần nhập tối thiểu 2 ký tự.'),
    ('Người lập', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '–'),
    ('Số tiền đề nghị từ', 'Number', 'Enable', '≥ 0', 'Không', 'Trống',
     'So sánh trên tổng tiền đề nghị quy đổi của cả phiếu.'),
    ('Số tiền đề nghị đến', 'Number', 'Enable', '≥ 0', 'Không', 'Trống',
     'Bỏ trống thì không chặn trên.'),
    ('Ngày lập từ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Lấy trọn ngày.'),
    ('Ngày lập đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lấy trọn ngày; phiếu lập trong chính ngày đó vẫn nằm trong kết quả.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Đổi giá trị một tiêu chí trong Tìm kiếm nâng cao', 'Change',
     'During:\n– Ghi nhận giá trị mới và ghi nhớ bộ lọc trong 10 phút cho chế độ đang xem.\n'
     'After:\n– Quay về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí đang có.'),
    ('Bấm nút Tìm kiếm', 'Click',
     'After:\n– Áp giá trị ô tìm nhanh theo mã phiếu, quay về trang 1 và nạp lại danh sách.'),
    ('Bấm nút Làm mới', 'Click',
     'After:\n– Đặt lại toàn bộ tiêu chí về trống, xóa nhãn đối tượng đã chọn, quay về trang 1 '
     'và nạp lại danh sách.'),
    ('Đổi Công ty', 'Change',
     'During:\n– Xóa giá trị Phòng ban và Bộ phận đang chọn.\n'
     'After:\n– Nạp lại danh sách phòng ban theo công ty mới và nạp lại danh sách phiếu.'),
    ('Nhập từ khóa ô Khách hàng / Nhà cung cấp', 'Keypress',
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
           'riêng của Phiếu đề nghị thanh toán.',
           anchor='list')
d.intro_table(
    ten='Cài đặt bộ lọc và tuỳ chỉnh cột hiển thị',
    mota='Cho phép mỗi người dùng tự chọn tiêu chí lọc và cột muốn thấy, đồng thời sắp xếp lại '
         'thứ tự của chúng.',
    tacnhan='Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách, bất kỳ chế độ xem nào.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc (hoặc nút Cấu hình cột hiển thị).\n'
          '2. Hệ thống mở cửa sổ liệt kê toàn bộ tiêu chí (hoặc toàn bộ cột) kèm ô tích chọn.\n'
          '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống ghi nhận, hiển thị thông báo “Cập nhật thành công” và áp ngay lên màn hình.',
    phu='• Bấm Khôi phục mặc định ở cửa sổ Cài đặt bộ lọc → tích lại đủ 10 tiêu chí; vẫn phải '
        'bấm Lưu mới có hiệu lực.\n'
        '• Bấm Đóng → thoát mà không lưu thay đổi.\n'
        '• Bỏ tích một tiêu chí lọc → giá trị đang lọc của tiêu chí đó bị xóa.\n'
        '• Ba cột STT, Mã phiếu, Hành động bị khóa, không bỏ tích và không đổi vị trí được.',
    dacbiet='Cấu hình bộ lọc lưu riêng cho từng chế độ xem; cấu hình cột dùng CHUNG cho cả bốn '
            'chế độ vì bốn chế độ có cùng bộ cột.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột',
         modal='Cài đặt bộ lọc và Tuỳ chỉnh cột',
         shot=shot('03-cai-dat-bo-loc.png'),
         shot_caption='Cửa sổ Cài đặt bộ lọc với đủ 10 tiêu chí')
d.figure(shot('04-cau-hinh-cot.png'), 'Cửa sổ Tuỳ chỉnh cột', width_in=6.2)

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Cài đặt bộ lọc / Tuỳ chỉnh cột', '–'),
    ('Ô tích chọn từng tiêu chí', 'Modal', 'Enable', 'Danh sách 10 tiêu chí', 'Không',
     'Theo cấu hình đã lưu', 'Bỏ tích thì tiêu chí không hiển thị ở bộ lọc nâng cao.'),
    ('Ô tích chọn từng cột', 'Modal', 'Enable', 'Danh sách 15 cột', 'Không',
     'Theo cấu hình đã lưu', 'Ba cột bắt buộc bị khóa kèm biểu tượng ổ khóa.'),
    ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Kéo để đổi thứ tự tiêu chí / cột.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Ghi cấu hình cho người dùng hiện tại và áp ngay lên màn hình.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Chỉ có ở cửa sổ Cài đặt bộ lọc.'),
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
     'After:\n– Ghi nhận trạng thái tích trong cửa sổ, chưa áp lên màn hình.'),
    ('Bấm Lưu', 'Click',
     'During:\n– Ghi cấu hình cho người dùng hiện tại.\n'
     'After:\n– Hiển thị “Cập nhật thành công”; bộ lọc / bảng cập nhật ngay.\n'
     '– Với tiêu chí vừa bị bỏ tích, xóa luôn giá trị đang lọc của tiêu chí đó.'),
    ('Bấm Khôi phục mặc định', 'Click',
     'After:\n– Tích lại toàn bộ 10 tiêu chí và đưa thứ tự về thiết kế gốc; chưa lưu.'),
])

# ---------------------------------------------------------------- 2.4 FR-04
d.h3('2.4 Lập phiếu đề nghị thanh toán')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Lập phiếu đề nghị thanh toán', 'crud',
            [('include', 'Sinh mã phiếu tự động'),
             ('include', 'Chọn đối tượng và hợp đồng cho dòng chi tiết'),
             ('extend', 'Gửi thông báo cho nhóm Trưởng phòng khi gửi duyệt')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-04 Lập phiếu đề nghị thanh toán')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Lập phiếu đề nghị thanh toán',
    mota='Tạo một phiếu đề nghị thanh toán mới. Người dùng chọn loại chi, hình thức thanh toán, '
         'loại tiền, nhập lý do chi và các dòng chi tiết, đính kèm file, sau đó lưu nháp hoặc '
         'gửi duyệt.',
    tacnhan='Người lập phiếu; Người dùng đã đăng nhập',
    dieukien='Người dùng đang ở màn danh sách chế độ Tất cả hoặc Của tôi. Chức năng không gắn '
             'quyền.',
    chinh='1. Người dùng bấm nút Tạo mới, hệ thống mở màn Thêm phiếu đề nghị thanh toán.\n'
          '2. Người dùng chọn Loại chi, Hình thức thanh toán, Loại tiền và nhập Lý do chi.\n'
          '3. Nếu hình thức là chuyển khoản: chọn đối tượng nhận tiền; hệ thống nạp khối Thông '
          'tin ngân hàng (FR-07).\n'
          '4. Người dùng nhập bảng Chi tiết (FR-05 hoặc FR-06) và đính kèm file (FR-08).\n'
          '5. Người dùng bấm Lưu nháp, hoặc bấm Lưu và gửi duyệt rồi xác nhận.\n'
          '6. Hệ thống kiểm tra dữ liệu theo nút được bấm, sinh mã phiếu và ghi phiếu.\n'
          '7. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Thiếu dữ liệu bắt buộc → báo lỗi đỏ ngay dưới ô tương ứng, không lưu, giữ nguyên dữ '
        'liệu đã nhập.\n'
        '• Đổi Loại chi khi bảng chi tiết đã có dòng → hệ thống hỏi xác nhận rồi xóa toàn bộ '
        'dòng chi tiết và đối tượng đã chọn.\n'
        '• Đổi Hình thức thanh toán → hiện / ẩn khối Thông tin ngân hàng và đổi bố cục bảng Chi '
        'tiết.\n'
        '• Đổi Loại tiền → tỷ giá tự điền theo loại tiền; loại tiền VNĐ thì tỷ giá về 1 và bị '
        'khóa.\n'
        '• Rời màn khi đã nhập dở → hệ thống hỏi xác nhận trước khi thoát.\n'
        '• Hai người cùng lưu tại một thời điểm → mã phiếu vẫn duy nhất, không trùng.',
    dacbiet='Ràng buộc dữ liệu khác nhau giữa hai nút lưu: Lưu nháp chỉ bắt buộc Lý do chi và tỷ '
            'giá; Lưu và gửi duyệt bắt buộc thêm bảng chi tiết, khối ngân hàng (nếu chuyển '
            'khoản) và file đính kèm (nếu loại Chi trả nhà cung cấp).')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Thêm mới',
         route=ROUTE + '/create',
         shot=shot('14-tao-moi.png'),
         shot_caption='Màn Thêm phiếu đề nghị thanh toán lúc vừa mở')
d.figure(shot('15-tao-moi-ck.png'),
         'Hình thức chuyển khoản: có ô đối tượng nhận tiền và khối Thông tin ngân hàng',
         width_in=6.2)
d.figure(shot('31-tao-moi-loai2.png'),
         'Loại chi Chi trả lại khách hàng, hình thức tiền mặt', width_in=6.2)

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Loại chi', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Có', 'Chi trả nhà cung cấp',
     'Quyết định bố cục bảng Chi tiết và nguồn hợp đồng.'),
    ('Hình thức thanh toán', 'Dropdown', 'Enable', 'TM / CK', 'Có', 'TM',
     'CK hiện khối ngân hàng và ô đối tượng ở cấp phiếu; TM chọn đối tượng theo từng dòng.'),
    ('Loại tiền', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'VNĐ — VietNamDong',
     'Đổi giá trị thì tự điền tỷ giá tương ứng.'),
    ('Tỷ giá (VND)', 'Number', 'Enable / Disable', '> 0', 'Có', '1',
     'Bị khóa khi Loại tiền là VNĐ.'),
    ('Đến ngày', 'Datepicker', 'Enable / Ẩn', 'dd/mm/yyyy', 'Có khi loại chi là vận chuyển',
     'Trống', 'Mốc để lấy chuyến xe (FR-06).'),
    ('Người tạo', 'Textbox', 'Disable', '–', '–', 'Người đang đăng nhập', 'Chỉ để xem.'),
    ('Phòng ban', 'Textbox', 'Disable', '–', '–', 'Phòng ban của người đăng nhập', 'Chỉ để xem.'),
    ('Khách hàng / Nhà cung cấp', 'Textbox', 'Read-only', '–',
     'Có khi hình thức CK, hoặc khi loại chi là vận chuyển', 'Trống',
     'Bấm vào ô để mở cửa sổ chọn; nhãn đổi theo loại chi.'),
    ('Lý do chi', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
     'Bắt buộc ở cả hai nút lưu.'),
    ('Nút thêm dòng (dấu cộng)', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
     'Ẩn với loại chi vận chuyển (dòng do FR-06 sinh ra).'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', 'Có khi gửi duyệt', 'Rỗng',
     'Bố cục cột đổi theo loại chi và hình thức thanh toán; xem FR-05 và FR-06.'),
    ('Dòng Tổng cộng', 'Label', 'Read-only', '≥ 0', '–', '0',
     'Cộng dồn ngay theo từng phím gõ cho mọi cột số.'),
    ('Khối File đính kèm', 'Table/Grid', 'Enable', '–',
     'Có khi loại chi là Chi trả nhà cung cấp và đang gửi duyệt', 'Rỗng', 'Xem FR-08.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu phiếu ở trạng thái Đang tạo.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở hộp xác nhận, sau đó lưu phiếu ở trạng thái Chờ TP duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu đã nhập dở mà chưa lưu.'),
    ('Hộp xác nhận lưu và gửi duyệt', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Tiêu đề “Xác nhận lưu và gửi duyệt”.'),
    ('Hộp xác nhận đổi loại chi', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Tiêu đề “Đổi loại chi”, nội dung cảnh báo xóa toàn bộ dòng chi tiết và đối tượng đã chọn.'),
    ('Hộp cảnh báo chưa lưu', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Tiêu đề “Thông tin chưa lưu”, hai nút Thoát và Ở lại.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ kèm biểu tượng cảnh báo ngay dưới ô bị lỗi; ô đổi sang viền đỏ.'),
])
d.figure(shot('23-xac-nhan-doi-loai-chi.png'),
         'Hộp xác nhận khi đổi Loại chi lúc bảng chi tiết đã có dòng', width_in=6.2)
d.figure(shot('20-xac-nhan-gui-duyet.png'), 'Hộp xác nhận trước khi gửi duyệt', width_in=6.2)
d.figure(shot('21-loi-validate.png'),
         'Thông báo bắt buộc nhập ở ô Lý do chi và ở ô số tiền của dòng', width_in=6.2)
d.figure(shot('24-canh-bao-chua-luu.png'),
         'Hộp cảnh báo khi rời màn hình mà chưa lưu', width_in=6.2)

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'After:\n– Mở màn thêm mới với Loại chi = Chi trả nhà cung cấp, Hình thức thanh toán = TM, '
     'Loại tiền = VNĐ, Tỷ giá = 1 (khóa), Người tạo và Phòng ban theo người đăng nhập, các ô còn '
     'lại để trống.'),
    ('Đổi Loại chi', 'Change',
     'Before:\n– Nếu bảng Chi tiết chưa có dòng nào → đổi ngay, không hỏi.\n'
     'During:\n– Nếu đã có dòng → hiển thị hộp xác nhận “Đổi loại chi”.\n'
     'After:\n– Chọn Xác nhận: xóa toàn bộ dòng chi tiết, đối tượng đã chọn và mọi lỗi của các '
     'dòng đó; đổi bố cục cột theo loại chi mới.\n'
     '– Chọn Hủy: giữ nguyên mọi thứ.'),
    ('Đổi Hình thức thanh toán', 'Change',
     'After:\n– Sang CK: hiện ô đối tượng ở cấp phiếu và khối Thông tin ngân hàng; bảng Chi tiết '
     'bỏ cột đối tượng theo dòng.\n'
     '– Sang TM: ẩn khối ngân hàng và ô đối tượng cấp phiếu; bảng Chi tiết hiện lại cột đối '
     'tượng theo dòng.'),
    ('Đổi Loại tiền', 'Change',
     'After:\n– Loại tiền VNĐ: đặt Tỷ giá = 1 và khóa ô, ẩn cột quy đổi.\n'
     '– Loại tiền khác: mở khóa ô Tỷ giá, tự điền tỷ giá của loại tiền đó, hiện thêm cột quy đổi '
     'VND.\n'
     '– Tính lại cột quy đổi của mọi dòng chi tiết.'),
    ('Bấm Lưu nháp', 'Click',
     'During:\n– Lý do chi trống → hiển thị “Bắt buộc nhập”.\n'
     '– Tỷ giá trống hoặc không lớn hơn 0 → hiển thị “Phải lớn hơn 0”.\n'
     '– Loại chi là vận chuyển mà chưa chọn Đến ngày → hiển thị “Bắt buộc nhập”.\n'
     '– Dòng chi tiết đã thêm mà thiếu hợp đồng hoặc số tiền → hiển thị lỗi tại đúng ô của dòng '
     'đó; số tiền nhỏ hơn 1 → hiển thị “Không được nhỏ hơn 1”.\n'
     '– KHÔNG bắt buộc bảng chi tiết, khối ngân hàng và file đính kèm.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Sinh mã phiếu theo dạng <mã công ty>.DNTT<tháng năm>.<5 chữ số>; ghi phiếu ở '
     'trạng thái Đang tạo cùng công ty / phòng ban / bộ phận của người lập.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Hiển thị “Lưu phiếu đề nghị thanh toán thành công!” và quay về màn danh sách.'),
    ('Bấm Lưu và gửi duyệt', 'Click',
     'Before:\n– Hiển thị hộp xác nhận “Xác nhận lưu và gửi duyệt”; chọn Hủy thì dừng xử lý.\n'
     'During:\n– Áp toàn bộ kiểm tra của Lưu nháp, cộng thêm:\n'
     '– Bảng Chi tiết chưa có dòng nào → hiển thị “Bắt buộc nhập” ngay dưới bảng.\n'
     '– Dòng chi tiết chưa chọn đối tượng / hợp đồng → hiển thị “Bắt buộc nhập” ở đúng ô.\n'
     '– Hình thức CK mà khối ngân hàng còn trống → hiển thị “Bắt buộc nhập” ở Số tài khoản, Tên '
     'tài khoản, Tên ngân hàng (và Chi nhánh, Thành phố nếu nguồn dữ liệu có hai thông tin này).\n'
     '– Nhà cung cấp nước ngoài → bắt buộc thêm Ngân hàng, Swift Code và Phí.\n'
     '– Loại chi Chi trả nhà cung cấp mà chưa có file đính kèm → hiển thị “Bắt buộc đính kèm ít '
     'nhất 1 file”.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Sinh mã phiếu và ghi phiếu ở trạng thái Chờ TP duyệt.\n'
     '– Ghi một dòng lịch sử “Tạo mới”.\n'
     '– Gửi thông báo tới nhóm Trưởng phòng duyệt cùng công ty với phiếu.\n'
     '– Hiển thị “Gửi duyệt phiếu đề nghị thanh toán thành công!” và quay về màn danh sách.'),
    ('Bấm Quay lại khi đã nhập dở', 'Click',
     'During:\n– Hiển thị hộp “Thông tin chưa lưu”.\n'
     'After:\n– Chọn Ở lại thì giữ nguyên dữ liệu; chọn Thoát thì bỏ mọi thay đổi và về danh sách.'),
])

# ---------------------------------------------------------------- 2.5 FR-05
d.h3('2.5 Chọn đối tượng và hợp đồng cho dòng chi tiết')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chọn đối tượng và hợp đồng', 'crud',
            [('include', 'Lọc hợp đồng theo loại chi và đối tượng'),
             ('include', 'Tính công nợ theo sổ kế toán'),
             ('extend', 'Chặn chọn trùng hợp đồng trong cùng phiếu')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-05 Chọn đối tượng và hợp đồng cho dòng chi tiết')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Dropdown, Popup chọn dữ liệu và Validate dữ liệu. Chỉ bổ sung nguồn hợp đồng và '
           'điều kiện lọc riêng theo từng loại chi.',
           anchor='create')
d.intro_table(
    ten='Chọn đối tượng và hợp đồng cho dòng chi tiết',
    mota='Gắn đối tượng nhận tiền và hợp đồng cho từng dòng của bảng Chi tiết. Hệ thống tự điền '
         'công nợ của hợp đồng theo sổ kế toán.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn lập hoặc sửa phiếu, loại chi khác Thanh toán chi phí vận chuyển NCC.',
    chinh='1. Với hình thức tiền mặt: người dùng bấm ô đối tượng của dòng, hệ thống mở cửa sổ '
          'Chọn khách hàng hoặc Chọn nhà cung cấp theo loại chi; chọn xong cửa sổ tự đóng.\n'
          '2. Người dùng bấm ô hợp đồng của dòng, hệ thống mở cửa sổ hợp đồng đã lọc theo loại '
          'chi và theo đối tượng.\n'
          '3. Người dùng bấm chọn một hợp đồng; cửa sổ tự đóng.\n'
          '4. Hệ thống điền số hợp đồng và cột công nợ của dòng.',
    phu='• Chưa chọn đối tượng mà bấm ô hợp đồng → ô bị khóa, không mở cửa sổ (trừ loại Chi '
        'thưởng thực hiện hợp đồng, loại này mở được ngay).\n'
        '• Đổi đối tượng của dòng đã chọn hợp đồng → hệ thống xóa hợp đồng của dòng và đưa công '
        'nợ về 0.\n'
        '• Hợp đồng đã có ở dòng khác trong cùng phiếu → được đánh dấu và không cho chọn.\n'
        '• Hợp đồng chưa phát sinh bút toán kế toán → công nợ hiển thị 0.',
    dacbiet='Nguồn hợp đồng theo loại chi: Chi trả nhà cung cấp lấy 5 nguồn hợp đồng MUA; Chi '
            'trả lại khách hàng và Chi thưởng thực hiện hợp đồng lấy các nguồn hợp đồng BÁN. '
            'Riêng loại Chi thưởng thực hiện hợp đồng lọc theo quyền hưởng thưởng của người lập '
            'chứ không theo đối tượng, nên cửa sổ có thêm ô lọc Khách hàng.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Thêm mới => Chọn khách hàng / Chọn nhà cung cấp / '
              'Chọn hợp đồng',
         route=ROUTE + '/create',
         modal='Chọn khách hàng, Chọn nhà cung cấp và Chọn hợp đồng',
         shot=shot('16-popup-ncc.png'),
         shot_caption='Cửa sổ Chọn nhà cung cấp')
d.figure(shot('18-popup-hop-dong-mua.png'),
         'Cửa sổ Chọn hợp đồng mua, đã lọc theo nhà cung cấp của phiếu', width_in=6.2)

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ chọn đối tượng', 'Label', 'Hiển thị', '–', '–',
     'Chọn khách hàng / Chọn nhà cung cấp', 'Đổi theo loại chi.'),
    ('Ô tìm trong cửa sổ chọn đối tượng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Cửa sổ khách hàng có 3 ô tìm (tên/mã, mã số thuế, số điện thoại); cửa sổ nhà cung cấp có '
     '1 ô tìm theo mã hoặc tên.'),
    ('Bảng kết quả chọn đối tượng', 'Table/Grid', 'Read-only', '–', '–', 'Trang 1',
     'Bấm vào một dòng để chọn; cửa sổ tự đóng.'),
    ('Tiêu đề cửa sổ hợp đồng', 'Label', 'Hiển thị', '–', '–', 'Chọn hợp đồng mua / bán',
     'Dòng phụ hiển thị đối tượng đang lọc.'),
    ('Ô Số đơn hàng/Hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Ô tìm trong cửa sổ hợp đồng.'),
    ('Ô lọc Khách hàng trong cửa sổ hợp đồng', 'Textbox', 'Enable / Ẩn', '0–255 ký tự', 'Không',
     'Trống', 'Chỉ hiện với loại Chi thưởng thực hiện hợp đồng.'),
    ('Bảng hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Trang 1',
     'Cột STT, Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ.'),
    ('Dòng hợp đồng đã có trong phiếu', 'Table/Grid', 'Disable', '–', '–', 'Ẩn',
     'Được đánh dấu kèm chú thích, không chọn được.'),
    ('Nút Tìm kiếm / Làm mới / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Áp điều kiện tìm, xóa điều kiện tìm, đóng cửa sổ.'),
    ('Phân trang trong cửa sổ', 'Pagination', 'Enable', '–', 'Không', 'Trang 1, 10 dòng',
     'Có ô chọn số dòng mỗi trang.'),
    ('Cột công nợ của dòng', 'Number', 'Read-only', '–', '–', '0',
     'Nhãn đổi theo loại chi: Số tiền còn nợ / Công nợ còn lại / Số tiền còn lại.'),
    ('Cột Số tiền đề nghị chi', 'Number', 'Enable', '≥ 1', 'Có', '0',
     'Khi dùng ngoại tệ tách thành hai cột con: nguyên tệ và VND.'),
    ('Cột Ghi chú của dòng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', '–'),
    ('Nút xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Xóa dòng và đánh số lại các dòng còn lại.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm vào ô đối tượng của dòng', 'Click',
     'Before:\n– Màn xem chi tiết ở chế độ chỉ đọc thì không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ chọn tương ứng loại chi; ghi nhận dòng đang thao tác.'),
    ('Chọn một đối tượng trong cửa sổ', 'Click',
     'After:\n– Gán đối tượng cho dòng và hiển thị dạng mã - tên.\n'
     '– Xóa hợp đồng đã chọn của dòng và đưa công nợ về 0.\n'
     '– Xóa thông báo lỗi bắt buộc của ô đối tượng; đóng cửa sổ.'),
    ('Bấm vào ô hợp đồng của dòng', 'Click',
     'Before:\n– Dòng chưa chọn đối tượng → không mở cửa sổ (trừ loại Chi thưởng thực hiện hợp '
     'đồng).\n'
     'After:\n– Mở cửa sổ hợp đồng, lọc theo loại chi và đối tượng của dòng.'),
    ('Chọn một hợp đồng trong cửa sổ', 'Click',
     'Before:\n– Hợp đồng đã có ở dòng khác trong cùng phiếu → không cho chọn.\n'
     'After:\n– Gán hợp đồng cho dòng, điền công nợ theo sổ kế toán, xóa lỗi bắt buộc của ô hợp '
     'đồng; đóng cửa sổ.'),
    ('Nhập Số tiền đề nghị chi', 'Change',
     'After:\n– Tính lại cột quy đổi VND của dòng đó và các ô của dòng Tổng cộng.'),
    ('Bấm nút xóa dòng', 'Click',
     'After:\n– Xóa dòng, đánh số lại các dòng còn lại, dồn thông báo lỗi về đúng dòng tương ứng '
     'và tính lại dòng Tổng cộng.'),
])

# ---------------------------------------------------------------- 2.6 FR-06
d.h3('2.6 Lấy dữ liệu chuyến xe (loại chi vận chuyển)')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Lấy dữ liệu chuyến xe', 'crud',
            [('include', 'Kiểm tra đã chọn nhà cung cấp và Đến ngày'),
             ('extend', 'Xem chi tiết một chuyến xe')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-06 Lấy dữ liệu chuyến xe')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu và Thông báo. Chỉ bổ sung cách lấy dữ liệu chuyến xe của loại chi '
           'vận chuyển.',
           anchor='create')
d.intro_table(
    ten='Lấy dữ liệu chuyến xe cho loại chi vận chuyển',
    mota='Với loại chi Thanh toán chi phí vận chuyển NCC, bảng Chi tiết không nhập tay mà do hệ '
         'thống sinh ra từ các chuyến xe của nhà cung cấp phát sinh tới mốc Đến ngày.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn lập hoặc sửa phiếu, Loại chi là Thanh toán chi phí vận chuyển NCC.',
    chinh='1. Người dùng chọn Nhà cung cấp và Đến ngày ở khối Thông tin chung.\n'
          '2. Người dùng bấm nút Lấy dữ liệu ở góc phải tiêu đề bảng Chi tiết.\n'
          '3. Hệ thống sinh các dòng chuyến xe kèm Tổng cước, Đã thanh toán và Số tiền còn lại.\n'
          '4. Người dùng tích chọn các dòng cần thanh toán và nhập số tiền cho những dòng đã tích.',
    phu='• Chưa chọn Nhà cung cấp → hệ thống yêu cầu chọn nhà cung cấp trước, không sinh dòng.\n'
        '• Chưa chọn Đến ngày → hệ thống yêu cầu chọn Đến ngày trước, không sinh dòng.\n'
        '• Bấm mã ở cột Hạch toán → mở cửa sổ Chi tiết chuyến xe.\n'
        '• Bấm lại Lấy dữ liệu → bảng được dựng lại theo điều kiện mới.',
    dacbiet='Loại chi này KHÔNG cho thêm hoặc xóa dòng bằng tay: bảng không có nút dấu cộng và '
            'không có nút xóa dòng. Chỉ những dòng ĐƯỢC TÍCH mới bắt buộc nhập số tiền.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Thêm mới => Lấy dữ liệu chuyến xe',
         route=ROUTE + '/create',
         shot=shot('23-xac-nhan-doi-loai-chi.png'),
         shot_caption='Bố cục bảng Chi tiết của loại chi vận chuyển (ô Đến ngày và nút Lấy dữ liệu)')
d.figure(shot('25-chi-tiet-loai12.png'),
         'Bảng Chi tiết loại vận chuyển ở màn xem, phiếu dùng ngoại tệ', width_in=6.2)

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Lấy dữ liệu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Nằm ở góc phải tiêu đề bảng Chi tiết; chỉ có ở loại chi vận chuyển.'),
    ('Ô tích chọn ở hàng tiêu đề', 'Modal', 'Enable', '–', 'Không', 'Đã tích',
     'Tích / bỏ tích tất cả các dòng.'),
    ('Ô tích chọn của từng dòng', 'Modal', 'Enable', '–', 'Không', 'Đã tích',
     'Chỉ dòng được tích mới bắt buộc nhập số tiền.'),
    ('Cột Số chuyến xe', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '–'),
    ('Cột Hạch toán', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Là liên kết mở cửa sổ Chi tiết chuyến xe.'),
    ('Cột Tổng cước', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', '–'),
    ('Cột Đã thanh toán', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', '–'),
    ('Cột Số tiền còn lại', 'Number', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', '–'),
    ('Cột Số tiền đề nghị chi', 'Number', 'Enable', '≥ 1', 'Có với dòng được tích', '0', '–'),
    ('Cửa sổ Chi tiết chuyến xe', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị đầy đủ thông tin của chuyến xe; đóng lại không làm đổi dữ liệu phiếu.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Lấy dữ liệu', 'Click',
     'Before:\n– Chưa chọn Nhà cung cấp → hiển thị “Vui lòng chọn nhà cung cấp trước” và dừng.\n'
     '– Chưa chọn Đến ngày → hiển thị “Vui lòng chọn Đến ngày trước” và dừng.\n'
     'After:\n– Sinh danh sách dòng chuyến xe của nhà cung cấp tới mốc Đến ngày, mặc định tích '
     'chọn tất cả.'),
    ('Bấm ô tích ở hàng tiêu đề', 'Click',
     'After:\n– Tích hoặc bỏ tích toàn bộ các dòng đang hiển thị.'),
    ('Bấm mã ở cột Hạch toán', 'Click',
     'After:\n– Mở cửa sổ Chi tiết chuyến xe của dòng đó.'),
    ('Lưu phiếu', 'System',
     'During:\n– Chỉ kiểm tra số tiền của những dòng được tích; dòng không tích để trống vẫn hợp '
     'lệ.\n'
     'After:\n– Ghi các dòng chi tiết theo đúng danh sách trên màn hình.'),
])

# ---------------------------------------------------------------- 2.7 FR-07
d.h3('2.7 Nạp khối thông tin ngân hàng')

d.p('2.7.1 Giới thiệu')
d.rule_ref('- Validate dữ liệu, Dropdown và Thông báo. Chỉ bổ sung quy tắc nạp khối thông tin '
           'ngân hàng của Phiếu đề nghị thanh toán.',
           anchor='create')
d.intro_table(
    ten='Nạp khối thông tin ngân hàng của đối tượng nhận tiền',
    mota='Khi hình thức thanh toán là chuyển khoản, hệ thống tự nạp thông tin tài khoản ngân '
         'hàng của đối tượng nhận tiền vào khối Thông tin ngân hàng. Mọi ô trong khối đều chỉ '
         'đọc.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn lập hoặc sửa phiếu, Hình thức thanh toán là CK.',
    chinh='1. Người dùng chọn đối tượng nhận tiền ở khối Thông tin chung.\n'
          '2. Hệ thống tra hồ sơ đối tượng và nạp thông tin ngân hàng.\n'
          '3. Nếu đối tượng có nhiều tài khoản, hệ thống hiện ô chọn Tài khoản ngân hàng để '
          'người dùng chọn; đổi tài khoản thì các ô bên dưới đổi theo.',
    phu='• Đối tượng chưa khai tài khoản ngân hàng → khối để trống và hiện dòng hướng dẫn cập '
        'nhật hồ sơ rồi chọn lại; phiếu vẫn lưu nháp được nhưng không gửi duyệt được.\n'
        '• Đối tượng là nhà cung cấp nước ngoài → khối đổi sang bộ trường có Swift Code, IBAN '
        'Number, Địa chỉ, Phí và khối ngân hàng trung gian.\n'
        '• Loại chi Chi thưởng thực hiện hợp đồng → không có ô chọn đối tượng; hệ thống nạp tài '
        'khoản ngân hàng của chính người lập phiếu.',
    dacbiet=None)

d.p('2.7.2 Layout màn hình')
d.layout(menu=MENU + ' => Thêm mới => Thông tin ngân hàng',
         route=ROUTE + '/create',
         shot=shot('17-ngan-hang.png'),
         shot_caption='Khối Thông tin ngân hàng tự điền sau khi chọn nhà cung cấp trong nước')
d.figure(shot('08-chi-tiet.png'),
         'Khối Thông tin ngân hàng của nhà cung cấp nước ngoài (có Swift Code, IBAN và Phí)',
         width_in=6.2)

d.p('2.7.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tài khoản ngân hàng', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Trống',
     'Chỉ hiện khi đối tượng có từ 2 tài khoản trở lên.'),
    ('Số tài khoản', 'Textbox', 'Read-only', '0–255 ký tự', 'Theo hồ sơ đối tượng',
     'Bắt buộc khi gửi duyệt.'),
    ('Tên tài khoản', 'Textbox', 'Read-only', '0–255 ký tự', 'Theo hồ sơ đối tượng',
     'Bắt buộc khi gửi duyệt.'),
    ('Tên ngân hàng', 'Textbox', 'Read-only', '0–255 ký tự', 'Theo hồ sơ đối tượng',
     'Bắt buộc khi gửi duyệt.'),
    ('Chi nhánh', 'Textbox', 'Read-only', '0–255 ký tự', 'Theo hồ sơ đối tượng',
     'Bắt buộc khi gửi duyệt, trừ khi nguồn dữ liệu không có thông tin này.'),
    ('Thành phố', 'Textbox', 'Read-only', '0–255 ký tự', 'Theo hồ sơ đối tượng',
     'Cùng điều kiện với Chi nhánh.'),
    ('Địa chỉ', 'Textbox', 'Read-only', '0–255 ký tự', 'Theo hồ sơ đối tượng',
     'Thay cho Chi nhánh và Thành phố khi nguồn dữ liệu chỉ có địa chỉ ngân hàng.'),
    ('Ngân hàng', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Trống',
     'Chỉ với nhà cung cấp nước ngoài; bắt buộc khi gửi duyệt.'),
    ('Swift Code', 'Textbox', 'Read-only', '0–255 ký tự', 'Theo hồ sơ đối tượng',
     'Chỉ với nhà cung cấp nước ngoài; bắt buộc khi gửi duyệt.'),
    ('IBAN Number', 'Textbox', 'Read-only', '0–255 ký tự', 'Theo hồ sơ đối tượng',
     'Chỉ với nhà cung cấp nước ngoài; không bắt buộc.'),
    ('Phí', 'Dropdown', 'Enable / Ẩn', 'Danh sách 3 giá trị', 'Trống',
     'Chỉ với nhà cung cấp nước ngoài; bắt buộc khi gửi duyệt. Ba giá trị: Phí do người chuyển '
     'tiền chịu / Phí do người hưởng chịu / Phí chia sẻ cho 2 bên.'),
    ('Ngân hàng trung gian và bộ ô (trung gian)', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Trống',
     'Chỉ với nhà cung cấp nước ngoài; không bắt buộc.'),
    ('Dòng hướng dẫn khi thiếu tài khoản', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
     'Chữ đỏ dưới khối, hướng dẫn cập nhật hồ sơ Khách hàng / Nhà cung cấp rồi chọn lại.'),
], required=False)

d.p('2.7.4 Danh sách event và xử lý event')
d.event_table([
    ('Chọn đối tượng nhận tiền', 'Change',
     'During:\n– Tra hồ sơ đối tượng để lấy danh sách tài khoản ngân hàng.\n'
     'After:\n– Có đúng 1 tài khoản: tự điền các ô.\n'
     '– Có nhiều tài khoản: hiện ô chọn Tài khoản ngân hàng và điền theo tài khoản đầu tiên.\n'
     '– Không có tài khoản nào: để trống các ô và hiện dòng hướng dẫn.'),
    ('Đổi Tài khoản ngân hàng', 'Change',
     'After:\n– Nạp lại các ô bên dưới theo tài khoản vừa chọn.'),
    ('Đổi Hình thức thanh toán về TM', 'Change',
     'After:\n– Ẩn toàn bộ khối Thông tin ngân hàng; dữ liệu ngân hàng không còn được kiểm tra '
     'khi lưu.'),
])

# ---------------------------------------------------------------- 2.8 FR-08
d.h3('2.8 Quản lý file đính kèm')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Quản lý file đính kèm', 'io',
            [('include', 'Kiểm tra định dạng và dung lượng'),
             ('extend', 'Xem trước và tải xuống file')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-08 Quản lý file đính kèm')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Validate dữ liệu và Thông báo. Chỉ bổ sung định dạng, dung lượng và ràng buộc bắt '
           'buộc đính kèm theo loại chi.',
           anchor='create')
d.intro_table(
    ten='Quản lý file đính kèm của phiếu',
    mota='Thêm, xem trước, tải xuống, thay đổi và xóa các file tài liệu kèm theo phiếu. File '
         'được tải lên ngay lúc người dùng chọn, không chờ tới lúc lưu phiếu.',
    tacnhan='Người lập phiếu',
    dieukien='Đang ở màn lập hoặc sửa phiếu.',
    chinh='1. Người dùng bấm nút Thêm tài liệu để thêm một dòng trống.\n'
          '2. Người dùng bấm Chọn tệp và chọn file từ máy.\n'
          '3. Hệ thống kiểm tra định dạng và dung lượng rồi tải file lên, hiển thị trạng thái '
          'đang tải.\n'
          '4. Tải xong, dòng hiển thị tên file, dung lượng và các nút thao tác.\n'
          '5. Khi lưu phiếu, hệ thống gắn danh sách file đã tải lên vào phiếu.',
    phu='• File sai định dạng → báo chỉ nhận pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip.\n'
        '• File quá 20MB → báo dung lượng tối đa 20MB.\n'
        '• Xóa một dòng file → hiện hộp hỏi xác nhận; xác nhận thì file bị xóa hẳn khỏi kho lưu '
        'trữ.\n'
        '• Loại chi Chi trả nhà cung cấp mà chưa có file nào khi gửi duyệt → khối File đính kèm '
        'viền đỏ và báo bắt buộc đính kèm ít nhất 1 file.\n'
        '• Chọn file rồi bỏ form giữa chừng → file đã tải lên vẫn nằm trên kho lưu trữ.',
    dacbiet='Nút Thay đổi chỉ có với file vừa tải lên mà phiếu chưa lưu; file đã gắn vào phiếu '
            'thì phải xóa rồi thêm lại.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Thêm mới => File đính kèm',
         route=ROUTE + '/create',
         shot=shot('19-file-dinh-kem.png'),
         shot_caption='Khối File đính kèm với một dòng chờ chọn tệp')
d.figure(shot('22-loi-file.png'),
         'Lỗi bắt buộc đính kèm file ở loại chi Chi trả nhà cung cấp', width_in=6.2)

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề khối File đính kèm', 'Label', 'Hiển thị', '–',
     'Có với loại Chi trả nhà cung cấp', 'File đính kèm',
     'Có dấu sao đỏ khi bắt buộc.'),
    ('Nút Thêm tài liệu', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Thêm một dòng trống; rê chuột hiện giới hạn định dạng và dung lượng.'),
    ('Nút Chọn tệp', 'Button', 'Enable', 'pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip; ≤ 20MB',
     'Có (khi khối bắt buộc)', 'Hiển thị', 'Mở hộp chọn file của hệ điều hành.'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện vòng quay và tên file trong lúc tải lên.'),
    ('Tên file', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Kèm biểu tượng theo định dạng file.'),
    ('Cột Dung lượng', 'Textbox', 'Read-only', '–', '–', 'Theo dữ liệu', '–'),
    ('Nút Xem trước', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
     'Chỉ với các định dạng xem trước được.'),
    ('Nút Tải xuống', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Tải file về máy.'),
    ('Nút Thay đổi', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện với file chưa gắn vào phiếu.'),
    ('Nút Xóa', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
     'Ẩn ở màn xem chi tiết; có hộp hỏi xác nhận.'),
    ('Thông báo lỗi của khối', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện ngay trong khối, khối đổi sang viền đỏ.'),
])

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Thêm tài liệu', 'Click', 'After:\n– Thêm một dòng trống vào cuối danh sách.'),
    ('Chọn tệp', 'Change',
     'During:\n– Sai định dạng → hiển thị “Chỉ nhận file pdf, png, jpg, jpeg, doc, docx, xls, '
     'xlsx, zip” và dừng.\n'
     '– Quá dung lượng → hiển thị “Dung lượng tối đa 20MB” và dừng.\n'
     'After:\n– Tải file lên kho lưu trữ và hiển thị tên file, dung lượng cùng các nút thao tác.'),
    ('Bấm Xóa một dòng file', 'Click',
     'During:\n– Hiển thị hộp xác nhận “Bạn có chắc muốn xóa file đính kèm này?”.\n'
     'After:\n– Xác nhận: xóa dòng khỏi danh sách và xóa file khỏi kho lưu trữ, không hoàn tác '
     'được.\n– Hủy: không thay đổi gì.'),
    ('Lưu phiếu', 'System',
     'Before:\n– Loại chi Chi trả nhà cung cấp và đang gửi duyệt mà danh sách file rỗng → hiển '
     'thị “Bắt buộc đính kèm ít nhất 1 file” và dừng xử lý.\n'
     'After:\n– Gắn danh sách file đã tải lên vào phiếu.'),
])

# ---------------------------------------------------------------- 2.9 FR-09
d.h3('2.9 Sửa phiếu')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Sửa phiếu đề nghị thanh toán', 'crud',
            [('include', 'Kiểm tra phiếu do chính người dùng lập'),
             ('include', 'Kiểm tra trạng thái Đang tạo hoặc Không duyệt'),
             ('extend', 'Gửi duyệt lại phiếu bị từ chối')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-09 Sửa phiếu đề nghị thanh toán')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.',
           anchor='notice')
d.intro_table(
    ten='Sửa phiếu đề nghị thanh toán',
    mota='Chỉnh sửa nội dung phiếu do chính người dùng lập, khi phiếu còn ở trạng thái Đang tạo '
         'hoặc Không duyệt. Dùng cả cho việc sửa lại phiếu bị từ chối rồi gửi duyệt lại.',
    tacnhan='Người lập phiếu',
    dieukien='Phiếu do chính người đăng nhập lập và đang ở trạng thái Đang tạo hoặc Không duyệt.',
    chinh='1. Người dùng bấm nút Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
          '2. Hệ thống mở màn Sửa phiếu đề nghị thanh toán, nạp toàn bộ dữ liệu của phiếu.\n'
          '3. Người dùng chỉnh sửa thông tin chung, khối ngân hàng, bảng chi tiết và file đính '
          'kèm.\n'
          '4. Người dùng bấm Lưu nháp hoặc Lưu và gửi duyệt rồi xác nhận.\n'
          '5. Hệ thống kiểm tra quyền, kiểm tra dữ liệu rồi ghi lại phiếu và ghi lịch sử.\n'
          '6. Hệ thống hiển thị thông báo thành công và quay về màn danh sách.',
    phu='• Phiếu không phải của người đăng nhập, hoặc không còn ở trạng thái cho sửa → hệ thống '
        'từ chối với thông báo không có quyền sửa phiếu này.\n'
        '• Rời màn khi đã sửa mà chưa lưu → hệ thống hỏi xác nhận trước khi thoát.\n'
        '• Gửi duyệt lại một phiếu bị từ chối → phiếu quay về trạng thái Chờ TP duyệt và đi lại '
        'luồng duyệt từ cấp đầu tiên.',
    dacbiet='Ô Mã phiếu chỉ để xem, không sửa được. Công ty, phòng ban và bộ phận của phiếu giữ '
            'nguyên như lúc lập, không đổi theo người sửa.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa',
         route=ROUTE + '/{id}/edit',
         shot=shot('29-sua.png'),
         shot_caption='Màn Sửa phiếu đề nghị thanh toán')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Mã phiếu', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', 'Chỉ để xem, không sửa được.'),
    ('Dòng người lập - ngày lập', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu',
     'Hiển thị ở góc phải tiêu đề khối Thông tin chung.'),
    ('Loại chi', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Có', 'Theo dữ liệu',
     'Đổi giá trị thì hỏi xác nhận xóa dòng chi tiết.'),
    ('Hình thức thanh toán', 'Dropdown', 'Enable', 'TM / CK', 'Có', 'Theo dữ liệu', '–'),
    ('Loại tiền', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Theo dữ liệu', '–'),
    ('Tỷ giá (VND)', 'Number', 'Enable / Disable', '> 0', 'Có', 'Theo dữ liệu',
     'Bị khóa khi Loại tiền là VNĐ.'),
    ('Lý do chi', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Theo dữ liệu', '–'),
    ('Khối Thông tin ngân hàng', 'Table/Grid', 'Read-only', '–', 'Có khi gửi duyệt',
     'Theo dữ liệu', 'Xem FR-07.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', 'Có khi gửi duyệt', 'Theo dữ liệu',
     'Thao tác giống màn lập phiếu; xem FR-05 và FR-06.'),
    ('Khối File đính kèm', 'Table/Grid', 'Enable', '–',
     'Có khi loại chi là Chi trả nhà cung cấp và đang gửi duyệt', 'Theo dữ liệu', 'Xem FR-08.'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Giữ phiếu ở trạng thái hiện tại.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đưa phiếu sang trạng thái Chờ TP duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu đã sửa mà chưa lưu.'),
])

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu do chính người dùng lập và đang ở trạng thái Đang '
     'tạo hoặc Không duyệt.\n'
     'After:\n– Mở màn sửa và nạp toàn bộ dữ liệu của phiếu, kể cả dòng chi tiết và file đính '
     'kèm.'),
    ('Bấm Lưu nháp / Lưu và gửi duyệt', 'Click',
     'Before:\n– Kiểm tra phiếu do chính người dùng lập và còn ở trạng thái Đang tạo hoặc Không '
     'duyệt; nếu không → hiển thị “Bạn không có quyền sửa phiếu này” và dừng xử lý.\n'
     'During:\n– Áp cùng bộ kiểm tra dữ liệu như màn lập phiếu, khác nhau theo nút được bấm.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Ghi lại thông tin chung, khối ngân hàng, toàn bộ dòng chi tiết và danh sách file '
     'theo dữ liệu mới.\n'
     '– Ghi một dòng lịch sử “Thay đổi thông tin”, liệt kê từng trường đã đổi.\n'
     '– Nếu phiếu chuyển sang Chờ TP duyệt thì gửi thông báo cho nhóm Trưởng phòng duyệt cùng '
     'công ty.\n'
     '– Hiển thị thông báo thành công tương ứng và quay về màn danh sách.'),
    ('Xóa một file đã lưu của phiếu', 'Click',
     'Before:\n– Kiểm tra quyền sửa phiếu; không đủ quyền → từ chối.\n'
     'After:\n– Gỡ file khỏi phiếu và xóa file khỏi kho lưu trữ.'),
])

# ---------------------------------------------------------------- 2.10 FR-10
d.h3('2.10 Xem chi tiết phiếu')

d.p('2.10.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các khối thông tin riêng của phiếu đề '
           'nghị thanh toán.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu đề nghị thanh toán',
    mota='Hiển thị toàn bộ nội dung một phiếu ở chế độ chỉ đọc, kèm bốn cột tiền của các cấp '
         'duyệt, khối file đính kèm, khối lịch sử và bộ nút thao tác phù hợp với trạng thái phiếu '
         'và quyền của người xem.',
    tacnhan='Người lập phiếu; Cấp duyệt; Kế toán thanh toán; Người dùng đã đăng nhập',
    dieukien='Phiếu nằm trong phạm vi dữ liệu người dùng được xem.',
    chinh='1. Người dùng bấm vào mã phiếu ở màn danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu: người lập, người đã duyệt ở bất kỳ cấp nào, '
          'quyền xem theo cấp, hoặc người có quyền duyệt ở đúng trạng thái hiện tại.\n'
          '3. Hệ thống tính lại công nợ của từng dòng theo sổ kế toán tại thời điểm mở.\n'
          '4. Màn chi tiết hiển thị thông tin chung, khối ngân hàng, bảng chi tiết kèm bốn cột '
          'tiền, khối file đính kèm và khối Lịch sử.\n'
          '5. Thanh nút dưới cùng hiển thị các thao tác mà người dùng được phép thực hiện.',
    phu='• Không đủ quyền xem phiếu → hệ thống từ chối, thông báo không có quyền xem phiếu này '
        'và đưa về màn danh sách.\n'
        '• Phiếu ở trạng thái Đang tạo của người khác → luôn bị từ chối.\n'
        '• Phiếu vừa bị xóa ở nơi khác → hệ thống báo không tải được phiếu và đưa về danh sách.',
    dacbiet=None)

d.p('2.10.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết',
         route=ROUTE + '/{id}',
         shot=shot('09-chi-tiet-cot-duyet.png'),
         shot_caption='Bảng Chi tiết ở màn xem với bốn cột tiền của các cấp duyệt')

d.p('2.10.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–',
     'Chi tiết phiếu đề nghị thanh toán: <mã phiếu>',
     'Hiển thị trên thanh tiêu đề và tiêu đề tab trình duyệt.'),
    ('Khối Thông tin chung', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Có thêm ô Trạng thái so với màn nhập; mọi ô đều khóa.'),
    ('Khối Thông tin ngân hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Chỉ hiện với phiếu chuyển khoản.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Bấm ô đối tượng không mở cửa sổ chọn; có dòng Tổng cộng.'),
    ('Cột TP duyệt', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Ô nhập được khi người xem đang là cấp Trưởng phòng giữ phiếu.'),
    ('Cột KT công nợ duyệt', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Ô nhập được khi người xem đang là cấp Kế toán công nợ giữ phiếu.'),
    ('Cột KT trưởng / BGĐ duyệt', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Ô nhập được khi người xem đang là Kế toán trưởng hoặc Ban giám đốc giữ phiếu.'),
    ('Cột Số tiền chi', 'Number', 'Read-only', '≥ 0', 'Dấu gạch dưới',
     'Luôn chỉ đọc; hiện dấu gạch dưới khi chưa có chứng từ chi.'),
    ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Chỉ có nút Xem trước và Tải xuống.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Phiếu của chính mình ở trạng thái Đang tạo hoặc Không duyệt.'),
    ('Nút Duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Người xem có quyền duyệt ở đúng trạng thái hiện tại của phiếu.'),
    ('Nút Chuyển duyệt BGĐ', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Chỉ với Kế toán trưởng và phiếu ở Chờ kế toán trưởng duyệt.'),
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Cùng điều kiện với nút Duyệt.'),
    ('Nút Tạo phiếu chi', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Kế toán thanh toán, phiếu ở Chờ tạo phiếu chi, hình thức tiền mặt, chưa có chứng từ chi.'),
    ('Nút Tạo ủy nhiệm chi', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
     'Như trên nhưng hình thức chuyển khoản; hai nút loại trừ nhau.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Mở bản in ở tab mới.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Tải file Excel của phiếu.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Cùng điều kiện với nút Sửa.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
    ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', 'Xem FR-15.'),
], required=False)

d.p('2.10.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu theo thứ tự: người lập / người đã duyệt → quyền xem '
     'theo cấp → người có quyền duyệt ở trạng thái hiện tại.\n'
     '– Không đủ quyền → hiển thị “Bạn không có quyền xem phiếu này” và đưa về danh sách.\n'
     'During:\n– Tính lại công nợ của từng dòng theo sổ kế toán.\n'
     'After:\n– Hiển thị dữ liệu ở chế độ chỉ đọc và bộ nút phù hợp với trạng thái, quyền.'),
    ('Bấm nút Sửa', 'Click', 'After:\n– Chuyển sang màn sửa phiếu (FR-09).'),
    ('Bấm nút In / Xuất Excel', 'Click', 'After:\n– Thực hiện chức năng FR-14.'),
    ('Bấm nút Tạo phiếu chi / Tạo ủy nhiệm chi', 'Click',
     'After:\n– Chuyển sang màn lập chứng từ tương ứng, gắn sẵn phiếu đề nghị hiện tại. Trạng '
     'thái phiếu đề nghị chưa đổi tại bước này.'),
])

# ---------------------------------------------------------------- 2.11 FR-11
d.h3('2.11 Duyệt phiếu theo cấp')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Duyệt phiếu theo cấp', 'action',
            [('include', 'Kiểm tra quyền duyệt ở trạng thái hiện tại'),
             ('include', 'Ghi số tiền duyệt của từng dòng'),
             ('extend', 'Chuyển duyệt Ban giám đốc')],
            actor=ACTOR_DUYET,
            caption='Biểu đồ Use Case — FR-11 Duyệt phiếu theo cấp')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử. Chỉ bổ sung luồng duyệt '
           'theo cấp của Phiếu đề nghị thanh toán.',
           anchor='history')
d.intro_table(
    ten='Duyệt phiếu đề nghị thanh toán theo cấp',
    mota='Người giữ vai duyệt xem phiếu, nhập số tiền chấp thuận cho từng dòng chi tiết rồi đẩy '
         'phiếu sang cấp kế tiếp.',
    tacnhan='Cấp duyệt (Trưởng phòng / Kế toán công nợ / Kế toán trưởng / Ban giám đốc)',
    dieukien='Người dùng có quyền duyệt ở ĐÚNG trạng thái hiện tại của phiếu, phiếu cùng công ty '
             'với người duyệt; riêng cấp Trưởng phòng còn phải đúng phòng ban được giao quản lý.',
    chinh='1. Người dùng mở màn Chờ duyệt và bấm vào mã phiếu (hoặc bấm nút Duyệt ở cột Hành '
          'động — nút này chỉ mở màn chi tiết).\n'
          '2. Người dùng xem thông tin phiếu và file đính kèm.\n'
          '3. Người dùng nhập số tiền chấp thuận vào cột tiền của cấp mình cho từng dòng chi '
          'tiết.\n'
          '4. Người dùng bấm nút Duyệt (hoặc Chuyển duyệt BGĐ nếu là Kế toán trưởng).\n'
          '5. Hệ thống hiển thị hộp xác nhận nêu rõ mã phiếu và cấp sẽ nhận phiếu.\n'
          '6. Người dùng xác nhận; hệ thống kiểm tra quyền và trạng thái, ghi số tiền, đổi trạng '
          'thái phiếu và ghi lịch sử.\n'
          '7. Hệ thống hiển thị thông báo thành công kèm tên cấp nhận phiếu và gửi thông báo cho '
          'các bên liên quan.',
    phu='• Không có quyền duyệt ở trạng thái hiện tại → hệ thống từ chối với thông báo không có '
        'quyền duyệt phiếu này ở trạng thái hiện tại.\n'
        '• Trạng thái đích không hợp lệ (nhảy cóc cấp) → hệ thống từ chối với thông báo “Không '
        'thể chuyển phiếu sang trạng thái này”.\n'
        '• Người khác vừa duyệt phiếu trước đó → thao tác bị từ chối, phiếu chỉ ghi nhận một lần '
        'duyệt.\n'
        '• Bấm Hủy ở hộp xác nhận → dừng, không thay đổi gì.',
    dacbiet='Số tiền của cấp Kế toán trưởng và Ban giám đốc ghi CHUNG một cột. Ở màn chi tiết, '
            'chỉ cột tiền của cấp đang giữ phiếu là ô nhập được; các cột khác chỉ đọc.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU_PENDING + ' => Xem chi tiết => Duyệt',
         route=ROUTE + '/{id}',
         shot=shot('08-chi-tiet.png'),
         shot_caption='Màn chi tiết ở cấp Kế toán trưởng: có nút Duyệt và Chuyển duyệt BGĐ')
d.figure(shot('12-xac-nhan-duyet.png'),
         'Hộp xác nhận duyệt, nêu rõ mã phiếu và cấp sẽ nhận phiếu', width_in=6.2)

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô số tiền của cấp đang duyệt', 'Number', 'Enable', '≥ 0', 'Có', 'Theo dữ liệu',
     'Nằm ở cột tiền của cấp mình trong bảng Chi tiết; các cột khác chỉ đọc.'),
    ('Nút Duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đẩy phiếu sang cấp kế tiếp; bị khóa trong lúc đang xử lý.'),
    ('Nút Chuyển duyệt BGĐ', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn',
     'Chỉ hiện với Kế toán trưởng; đẩy phiếu sang Chờ ban giám đốc duyệt.'),
    ('Hộp xác nhận duyệt', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Tiêu đề “Xác nhận duyệt”, nội dung nêu mã phiếu và cấp sẽ nhận phiếu; hai nút Duyệt và Hủy.'),
    ('Hộp xác nhận chuyển cấp', 'Modal', 'Hiển thị', '–', '–', 'Ẩn',
     'Câu hỏi và chữ trên nút xác nhận khác với hộp xác nhận duyệt.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Nêu rõ duyệt thành công và cấp nhận phiếu tiếp theo.'),
])

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Duyệt ở cột Hành động của danh sách', 'Click',
     'After:\n– Mở màn chi tiết của phiếu; KHÔNG thực hiện duyệt tại danh sách.'),
    ('Bấm nút Duyệt ở màn chi tiết', 'Click',
     'Before:\n– Nút chỉ hiển thị khi người dùng có quyền duyệt ở đúng trạng thái hiện tại.\n'
     'During:\n– Hiển thị hộp xác nhận; chọn Hủy thì dừng xử lý.\n'
     'After:\n– Kiểm tra lại quyền duyệt; không đủ → hiển thị “Bạn không có quyền duyệt phiếu '
     'này ở trạng thái hiện tại” và dừng.\n'
     '– Kiểm tra trạng thái đích có nằm trong các bước hợp lệ; không → hiển thị “Không thể '
     'chuyển phiếu sang trạng thái này” và dừng.\n'
     '– Ghi số tiền của cấp đang duyệt cho từng dòng chi tiết.\n'
     '– Đổi trạng thái phiếu sang bước kế tiếp; riêng cấp Trưởng phòng còn ghi Ngày nhận.\n'
     '– Ghi một dòng lịch sử “Thay đổi trạng thái” kèm số tiền cấp đó vừa ghi cho từng dòng.\n'
     '– Gửi thông báo cho nhóm của cấp kế tiếp, cho người lập và cho cấp vừa duyệt trước đó.\n'
     '– Hiển thị thông báo duyệt thành công kèm tên cấp nhận phiếu.'),
    ('Bấm nút Chuyển duyệt BGĐ', 'Click',
     'During:\n– Hiển thị hộp xác nhận riêng cho việc chuyển cấp.\n'
     'After:\n– Như nút Duyệt nhưng trạng thái đích là Chờ ban giám đốc duyệt.'),
])

# ---------------------------------------------------------------- 2.12 FR-12
d.h3('2.12 Từ chối phiếu')

d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'Từ chối phiếu', 'action',
            [('include', 'Kiểm tra quyền duyệt ở trạng thái hiện tại'),
             ('include', 'Ghi chú bắt buộc của cấp đang giữ phiếu'),
             ('extend', 'Trả phiếu về Đang tạo khi từ chối ở cấp Trưởng phòng')],
            actor=ACTOR_DUYET,
            caption='Biểu đồ Use Case — FR-12 Từ chối phiếu')

d.p('2.12.2 Giới thiệu')
d.rule_ref('- Quy tắc đổi trạng thái, Thông báo và Quy tắc ghi lịch sử.',
           anchor='history')
d.intro_table(
    ten='Từ chối phiếu đề nghị thanh toán',
    mota='Người giữ vai duyệt từ chối phiếu kèm ghi chú bắt buộc của cấp mình, đưa phiếu quay '
         'lại cho người lập chỉnh sửa.',
    tacnhan='Cấp duyệt (Trưởng phòng / Kế toán công nợ / Kế toán trưởng / Ban giám đốc)',
    dieukien='Cùng điều kiện với chức năng Duyệt: có quyền duyệt ở đúng trạng thái hiện tại, '
             'cùng công ty, và với cấp Trưởng phòng thì đúng phòng ban được giao quản lý.',
    chinh='1. Người dùng mở màn chi tiết phiếu và bấm nút Từ chối.\n'
          '2. Hệ thống mở cửa sổ Từ chối phiếu, nhãn ô ghi chú đổi theo cấp đang giữ phiếu.\n'
          '3. Người dùng nhập ghi chú bắt buộc và (tuỳ chọn) lý do không duyệt.\n'
          '4. Người dùng bấm nút Từ chối.\n'
          '5. Hệ thống kiểm tra quyền và ghi chú, đổi trạng thái phiếu, ghi lịch sử và gửi thông '
          'báo.\n'
          '6. Hệ thống hiển thị thông báo thành công, đóng cửa sổ và nạp lại màn chi tiết.',
    phu='• Bỏ trống ghi chú bắt buộc (kể cả chỉ nhập khoảng trắng) → báo “Bắt buộc nhập” ngay '
        'dưới ô, cửa sổ không đóng, trạng thái phiếu không đổi.\n'
        '• Không có quyền → hệ thống từ chối với thông báo không có quyền không duyệt phiếu này.\n'
        '• Bấm Đóng → thoát cửa sổ, phiếu không đổi; mở lại thì hai ô trở về trống.',
    dacbiet='Trạng thái phiếu sau khi bị từ chối phụ thuộc vào cấp thực hiện: cấp Trưởng phòng '
            'đưa phiếu về Đang tạo; các cấp từ Kế toán công nợ trở lên đưa phiếu sang Không '
            'duyệt. Đây là quy tắc nghiệp vụ cố ý giữ nguyên.')

d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU_PENDING + ' => Xem chi tiết => Từ chối',
         route=ROUTE + '/{id}',
         modal='Từ chối phiếu',
         shot=shot('11-tu-choi.png'),
         shot_caption='Cửa sổ Từ chối phiếu ở cấp Kế toán trưởng')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Từ chối phiếu',
     'Dòng phụ hiển thị mã phiếu đang xử lý.'),
    ('Ghi chú của <cấp đang giữ phiếu>', 'Textarea', 'Enable', '0–1000 ký tự', 'Có', 'Trống',
     'Nhãn đổi theo cấp: Ghi chú của Trưởng phòng / Kế toán công nợ / Kế toán trưởng / Ban giám '
     'đốc. Nội dung lưu vào ô ghi chú riêng của cấp đó và hiện trên bản in.'),
    ('Lý do không duyệt', 'Textarea', 'Enable', '0–1000 ký tự', 'Không', 'Trống',
     'Nội dung hiển thị trên thông báo gửi người lập.'),
    ('Nút Từ chối', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Bị khóa trong lúc đang xử lý để tránh gửi hai lần.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không thay đổi phiếu.'),
    ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô ghi chú bắt buộc.'),
])

d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Từ chối ở màn chi tiết', 'Click',
     'Before:\n– Nút chỉ hiển thị khi người dùng có quyền duyệt ở đúng trạng thái hiện tại.\n'
     'After:\n– Mở cửa sổ với hai ô để trống; nhãn ô bắt buộc đổi theo trạng thái phiếu.'),
    ('Bấm nút Từ chối trong cửa sổ', 'Click',
     'Before:\n– Kiểm tra quyền duyệt ở trạng thái hiện tại; không đủ → hiển thị “Bạn không có '
     'quyền không duyệt phiếu này” và dừng.\n'
     'During:\n– Ghi chú bắt buộc của cấp đang giữ phiếu trống → hiển thị “Bắt buộc nhập” và '
     'dừng, không đóng cửa sổ.\n'
     'After:\n– Lưu ghi chú vào ô riêng của cấp đó và lưu lý do không duyệt.\n'
     '– Đổi trạng thái: từ Chờ TP duyệt về Đang tạo; từ các trạng thái khác sang Không duyệt.\n'
     '– Ghi một dòng lịch sử “Thay đổi trạng thái” kèm ghi chú đã nhập.\n'
     '– Gửi thông báo cho người lập và cho tất cả các cấp mà phiếu đã đi qua.\n'
     '– Hiển thị “Không duyệt phiếu đề nghị thanh toán thành công!”, đóng cửa sổ và nạp lại màn '
     'chi tiết.'),
])

# ---------------------------------------------------------------- 2.13 FR-13
d.h3('2.13 Xóa phiếu')

d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'Xóa phiếu', 'action',
            [('include', 'Kiểm tra phiếu do chính người dùng lập'),
             ('include', 'Kiểm tra trạng thái Đang tạo hoặc Không duyệt')],
            actor=ACTOR_LAP,
            caption='Biểu đồ Use Case — FR-13 Xóa phiếu')

d.p('2.13.2 Giới thiệu')
d.rule_ref('- Quy tắc Xóa, Thông báo và Quy tắc ghi lịch sử.',
           anchor='notice')
d.intro_table(
    ten='Xóa phiếu đề nghị thanh toán',
    mota='Xóa hẳn một phiếu cùng toàn bộ dòng chi tiết. Dữ liệu không khôi phục được.',
    tacnhan='Người lập phiếu',
    dieukien='Phiếu do chính người đăng nhập lập và đang ở trạng thái Đang tạo hoặc Không duyệt.',
    chinh='1. Người dùng bấm nút ba chấm ở cột Hành động rồi chọn Xóa (hoặc bấm nút Xóa ở màn '
          'chi tiết).\n'
          '2. Hệ thống hiển thị hộp xác nhận kèm mã phiếu.\n'
          '3. Người dùng bấm nút Xóa.\n'
          '4. Hệ thống kiểm tra người lập và trạng thái phiếu rồi xóa phiếu.\n'
          '5. Hệ thống hiển thị thông báo thành công và nạp lại danh sách.',
    phu='• Bấm Hủy → đóng hộp thoại, phiếu giữ nguyên.\n'
        '• Phiếu không phải của người đăng nhập hoặc không còn ở trạng thái cho xóa → hệ thống '
        'từ chối với thông báo không có quyền xóa phiếu này.',
    dacbiet='Mã phiếu đã dùng không được cấp lại cho phiếu mới sau khi xóa.')

d.p('2.13.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa',
         modal='Xác nhận xóa',
         shot=shot('30-xac-nhan-xoa.png'),
         shot_caption='Hộp thoại Xác nhận xóa phiếu')

d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', '–'),
    ('Nội dung xác nhận', 'Label', 'Hiển thị',
     'Bạn có chắc muốn xóa phiếu đề nghị thanh toán ‘<mã phiếu>’?',
     'Hiển thị đúng mã phiếu của phiếu đang thao tác.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xóa phiếu.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xóa.'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     'Hiện thông báo xóa thành công hoặc thông báo lỗi tương ứng.'),
], required=False, scope=False)

d.p('2.13.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm mục Xóa', 'Click',
     'Before:\n– Mục chỉ hiển thị khi phiếu do chính người dùng lập và đang ở trạng thái Đang '
     'tạo hoặc Không duyệt.\n'
     'After:\n– Mở hộp xác nhận kèm mã phiếu.'),
    ('Bấm nút Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra người lập và trạng thái; không đủ điều kiện → hiển thị “Bạn không có '
     'quyền xóa phiếu này” và dừng xử lý.\n'
     'After:\n– Xóa toàn bộ dòng chi tiết rồi xóa phiếu.\n'
     '– Hiển thị thông báo xóa thành công và nạp lại danh sách.'),
    ('Bấm nút Hủy', 'Click', 'After:\n– Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ---------------------------------------------------------------- 2.14 FR-14
d.h3('2.14 In phiếu và xuất Excel')

d.p('2.14.1 Biểu đồ Usecase')
d.uc_figure('FR-14', 'In phiếu và xuất Excel', 'io',
            [('include', 'Dựng bố cục cột theo loại chi và hình thức thanh toán'),
             ('extend', 'Chỉ in cột Số tiền chi khi phiếu đã Duyệt phiếu chi')],
            actor='Người dùng xem được phiếu',
            caption='Biểu đồ Use Case — FR-14 In phiếu và xuất Excel')

d.p('2.14.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung bố cục bản in và các trường xuất riêng '
           'của Phiếu đề nghị thanh toán.',
           anchor='excel')
d.intro_table(
    ten='In phiếu và xuất Excel',
    mota='Mở bản in Phiếu đề nghị thanh toán ở tab mới, hoặc tải file Excel của phiếu. Hai đầu '
         'ra dùng chung dữ liệu nên số liệu luôn khớp nhau.',
    tacnhan='Người lập phiếu; Cấp duyệt; Kế toán thanh toán; Người dùng đã đăng nhập',
    dieukien='Phiếu nằm trong phạm vi dữ liệu người dùng được xem. Chức năng không gắn quyền '
             'riêng.',
    chinh='1. Người dùng bấm nút In (hoặc mục Xuất Excel) ở cột Hành động hoặc ở màn chi tiết.\n'
          '2. Với In: hệ thống mở tab mới, nạp dữ liệu và dựng bản in; người dùng bấm nút In để '
          'mở hộp thoại in của trình duyệt.\n'
          '3. Với Xuất Excel: hệ thống dựng file và trình duyệt tải file về, tên file chứa mã '
          'phiếu.',
    phu='• Không đủ quyền xem phiếu → hệ thống từ chối.\n'
        '• Phiếu chưa ở trạng thái Duyệt phiếu chi → cột Số tiền chi không được in.\n'
        '• Phiếu từng bị từ chối → bản in có thêm dòng ghi chú của cấp từ chối và lý do không '
        'duyệt.',
    dacbiet='Toàn bộ cờ bố cục (phiếu ngoại tệ, có khối nhà cung cấp, nhãn cột hợp đồng, có in '
            'cột Số tiền chi hay không) do hệ thống tính một lần và dùng chung cho cả bản in lẫn '
            'file Excel — hai đầu ra không tự suy lại để tránh lệch cột.')

d.p('2.14.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In phiếu / Xuất Excel',
         route=ROUTE + '/{id}/print',
         shot=shot('13-in-phieu.png'),
         shot_caption='Bản in Phiếu đề nghị thanh toán')

d.p('2.14.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
     'Mở hộp thoại in của trình duyệt; không xuất hiện trên bản in.'),
    ('Logo và thông tin công ty', 'Icon Button', 'Hiển thị', '–', 'Theo cấu hình',
     'Nằm ở đầu trang in.'),
    ('Tiêu đề bản in', 'Label', 'Hiển thị', '–', 'PHIẾU ĐỀ NGHỊ THANH TOÁN', 'Canh giữa, in đậm.'),
    ('Dòng ngày tháng và số phiếu', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '–'),
    ('Khối thông tin hai cột', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Hình thức thanh toán, Ngày lập, Loại thanh toán, Người lập, Lý do chi, Phòng ban, Tỷ giá; '
     'thêm Đến ngày với loại vận chuyển và dòng đối tượng nhận tiền nếu có.'),
    ('Khối ngân hàng', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Chỉ với phiếu chuyển khoản; nhà cung cấp nước ngoài in thêm Swift Code, IBAN Number và Phí.'),
    ('Bảng chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Tiêu đề hai dòng, dòng dưới ghi đơn vị tiền của từng cột; nhãn cột hợp đồng đổi theo loại '
     'chi.'),
    ('Cột Số tiền chi trên bản in', 'Number', 'Read-only', '≥ 0', 'Ẩn',
     'Chỉ in khi phiếu ở trạng thái Duyệt phiếu chi.'),
    ('Dòng Tổng cộng', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Ô nhãn gộp theo số cột mô tả thật của từng bố cục.'),
    ('Dòng Ghi chú / Lý do không duyệt', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Chỉ in khi phiếu có nội dung tương ứng.'),
    ('Khối ký tên', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Năm ô: BAN GIÁM ĐỐC, KẾ TOÁN TRƯỞNG, KẾ TOÁN CÔNG NỢ, TRƯỞNG PHÒNG, NGƯỜI ĐỀ NGHỊ. Cấp đã '
     'duyệt hiện tên kèm “Đã duyệt”; người lập hiện tên kèm “Đã ký”.'),
], required=False)

d.p('2.14.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In phiếu', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu; không đủ → từ chối.\n'
     'After:\n– Mở tab mới tới bản in của phiếu tương ứng.'),
    ('Mở bản in', 'System',
     'During:\n– Nạp dữ liệu phiếu, tính lại công nợ và tính bộ cờ bố cục.\n'
     'After:\n– Dựng bản in với bố cục cột theo loại chi, hình thức thanh toán và trạng thái '
     'phiếu.'),
    ('Bấm nút In trên bản in', 'Click',
     'After:\n– Mở hộp thoại in của trình duyệt; ẩn nút In và menu bên trái khỏi bản in.'),
    ('Bấm mục Xuất Excel', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu; không đủ → từ chối.\n'
     'After:\n– Dựng file Excel dùng chung dữ liệu với bản in và trả về cho trình duyệt tải; tên '
     'file chứa mã phiếu.'),
])

# ---------------------------------------------------------------- 2.15 FR-15
d.h3('2.15 Xem lịch sử thay đổi')

d.p('2.15.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và hiển thị lịch sử. Chỉ bổ sung các trường được ghi lịch sử '
           'riêng của Phiếu đề nghị thanh toán.',
           anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu',
    mota='Hiển thị toàn bộ thao tác đã tác động lên phiếu theo dòng thời gian: tạo mới, thay đổi '
         'thông tin, thay đổi trạng thái, kèm người thực hiện, giá trị trước / sau và số tiền '
         'từng cấp duyệt đã ghi.',
    tacnhan='Người lập phiếu; Cấp duyệt; Kế toán thanh toán; Người dùng đã đăng nhập',
    dieukien='Phiếu nằm trong phạm vi dữ liệu người dùng được xem. Chức năng không gắn quyền '
             'riêng.',
    chinh='1. Người dùng bấm mục Lịch sử ở cột Hành động, hoặc bấm Xem lịch sử ở khối Lịch sử '
          'cuối màn chi tiết.\n'
          '2. Hệ thống nạp các mốc thay đổi của phiếu.\n'
          '3. Hệ thống hiển thị danh sách mốc theo thứ tự thời gian, mốc mới nhất ở trên.',
    phu='• Phiếu chưa từng có thao tác nào trên màn hình này → hiển thị “Chưa có lịch sử thao '
        'tác nào.”.\n'
        '• Bấm Làm mới ở khối Lịch sử → nạp lại các mốc mới nhất.\n'
        '• Bấm Thu gọn → đóng khối Lịch sử.',
    dacbiet=None)

d.p('2.15.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Lịch sử',
         modal='Lịch sử thay đổi',
         shot=shot('10-lich-su.png'),
         shot_caption='Khối Lịch sử ở cuối màn chi tiết')

d.p('2.15.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ / khối', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi / Lịch sử',
     'Cửa sổ có dòng phụ ghi “Phiếu: <mã phiếu>”; khối ở màn chi tiết có số đếm số mốc.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc các mốc theo loại thao tác.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', 'Nạp lại các mốc mới nhất.'),
    ('Nút Thu gọn / Đóng', 'Button', 'Enable', '–', 'Hiển thị',
     'Đóng khối Lịch sử hoặc đóng cửa sổ.'),
    ('Mốc thời gian', 'Label', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Kèm tên thao tác: Tạo mới, Thay đổi thông tin, Thay đổi trạng thái.'),
    ('Dòng người thực hiện', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Dạng “Người thực hiện: <tên> – <phòng ban>”.'),
    ('Khối giá trị thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi trường một dòng, mũi tên từ giá trị cũ sang giá trị mới, dùng tên tiếng Việt.'),
    ('Khối số tiền cấp duyệt đã ghi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Liệt kê từng dòng chi tiết kèm giá trị cũ → giá trị mới của cột tiền cấp đó.'),
    ('Ghi chú của thao tác', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     'Hiển thị ghi chú mà người từ chối đã nhập.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', 'Hiện “Chưa có lịch sử thao tác nào.”.'),
], required=False)

d.p('2.15.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm mục Lịch sử ở cột Hành động', 'Click',
     'After:\n– Mở cửa sổ Lịch sử thay đổi và nạp các mốc của phiếu.'),
    ('Bấm nút Xem lịch sử ở màn chi tiết', 'Click',
     'After:\n– Mở khối Lịch sử; chỉ gọi dữ liệu ở lần mở đầu tiên; nút đổi thành Thu gọn.'),
    ('Bấm nút Làm mới', 'Click', 'After:\n– Nạp lại các mốc lịch sử mới nhất.'),
])

# ==================================================== PHẦN 4. QUY TẮC NGHIỆP VỤ
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của Phiếu đề nghị thanh toán; không lặp '
           'lại các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Mã phiếu sinh tự động và duy nhất', [
        '– Mã phiếu do hệ thống sinh khi lưu lần đầu, theo dạng <mã công ty>.DNTT<tháng '
        'năm>.<5 chữ số>, số chạy tăng dần trong cùng công ty và cùng tháng.',
        '– Người dùng không nhập và không sửa được mã phiếu.',
        '– Hai người lưu phiếu cùng lúc vẫn nhận hai mã khác nhau; mã đã dùng không được '
        'cấp lại kể cả khi phiếu bị xóa.',
    ], 'Lập phiếu'),
    ('BR-02', 'Bốn chế độ xem, bốn điều kiện dữ liệu khác nhau', [
        '– Chế độ Tất cả: áp phạm vi quyền xem theo thứ tự V1 → V2 → V3 → V4; không có cấp '
        'nào thì chỉ thấy phiếu do chính mình lập.',
        '– Chế độ Của tôi: mọi phiếu do chính mình lập, kể cả phiếu nháp.',
        '– Chế độ Chờ duyệt: phiếu cùng công ty với người đăng nhập VÀ đang ở đúng trạng '
        'thái mà người đó có quyền duyệt; không giữ vai nào thì danh sách rỗng.',
        '– Chế độ Đã duyệt: phiếu mà chính mình đã duyệt ở bất kỳ cấp nào.',
        '– Nhóm quyền phạm vi KHÔNG áp cho chế độ Chờ duyệt và Đã duyệt — người duyệt '
        'thường không giữ quyền xem theo cấp nào.',
    ], 'Xem danh sách'),
    ('BR-03', 'Phiếu nháp của người khác luôn bị ẩn', [
        '– Ở chế độ Tất cả, phiếu ở trạng thái Đang tạo chỉ người lập nhìn thấy, kể cả '
        'người giữ V1.',
        '– Quy tắc này áp cả khi mở chi tiết bằng đường dẫn trực tiếp.',
    ], ['Xem danh sách', 'Xem chi tiết']),
    ('BR-04', 'Phạm vi duyệt của từng cấp', [
        '– Cấp Trưởng phòng chỉ duyệt được phiếu ở trạng thái Chờ TP duyệt, cùng công ty VÀ '
        'thuộc phòng ban mà người đó được giao quản lý.',
        '– Cấp Kế toán công nợ, Kế toán trưởng, Ban giám đốc và Kế toán thanh toán chỉ giới '
        'hạn theo công ty, không giới hạn theo phòng ban.',
        '– Người giữ nhiều vai duyệt thấy phiếu của tất cả các vai đó trong cùng danh sách '
        'Chờ duyệt.',
    ], ['Xem danh sách (chế độ Chờ duyệt)', 'Duyệt phiếu', 'Từ chối phiếu']),
    ('BR-05', 'Thứ tự luồng duyệt và chặn nhảy cóc', [
        '– Thứ tự: Chờ TP duyệt → Chờ kế toán công nợ duyệt → Chờ kế toán trưởng duyệt → '
        '(tuỳ chọn) Chờ ban giám đốc duyệt → Chờ tạo phiếu chi.',
        '– Cấp Kế toán trưởng có hai lựa chọn: duyệt thẳng sang Chờ tạo phiếu chi, hoặc '
        'chuyển sang Chờ ban giám đốc duyệt.',
        '– Hệ thống chỉ chấp nhận các trạng thái đích hợp lệ tính từ trạng thái hiện tại; '
        'mọi bước nhảy cóc đều bị từ chối với thông báo “Không thể chuyển phiếu sang trạng '
        'thái này”.',
        '– Người dùng không thể tự đặt phiếu sang các trạng thái do màn Phiếu chi quản lý '
        '(Chờ duyệt phiếu chi, Duyệt phiếu chi, Đã hủy).',
    ], ['Duyệt phiếu', 'Từ chối phiếu']),
    ('BR-06', 'Số tiền duyệt của từng cấp ghi vào cột riêng', [
        '– Mỗi cấp duyệt ghi số tiền chấp thuận vào cột riêng của cấp mình; cấp Kế toán '
        'trưởng và Ban giám đốc dùng CHUNG một cột.',
        '– Ở màn chi tiết, chỉ cột tiền của cấp đang giữ phiếu là ô nhập được; các cột khác '
        'chỉ đọc.',
        '– Cột Số tiền chi luôn chỉ đọc, lấy từ phiếu chi hoặc giấy ủy nhiệm chi; chưa có '
        'chứng từ chi thì hiển thị dấu gạch dưới chứ không hiển thị 0.',
        '– Số tiền hiển thị trên cột Số tiền của danh sách là số của cấp duyệt gần nhất đã '
        'ghi.',
    ], ['Duyệt phiếu', 'Xem chi tiết']),
    ('BR-07', 'Quy tắc từ chối theo cấp', [
        '– Từ chối ở cấp Trưởng phòng đưa phiếu về trạng thái Đang tạo (dạng nháp của người '
        'lập).',
        '– Từ chối ở cấp Kế toán công nợ, Kế toán trưởng hoặc Ban giám đốc đưa phiếu sang '
        'trạng thái Không duyệt.',
        '– Ghi chú bắt buộc của đúng cấp đang giữ phiếu; trạng thái dùng để xác định ô bắt '
        'buộc được đọc từ dữ liệu phiếu, không lấy theo khai báo của người gửi.',
        '– Ô Lý do không duyệt không bắt buộc; nội dung của nó hiển thị trên thông báo gửi '
        'người lập.',
        '– Phiếu bị từ chối được người lập sửa lại và gửi lại; phiếu quay về Chờ TP duyệt '
        'và đi lại luồng duyệt từ cấp đầu tiên.',
    ], ['Từ chối phiếu', 'Sửa phiếu']),
    ('BR-08', 'Điều kiện sửa và xóa phiếu', [
        '– Chỉ người lập phiếu mới sửa và xóa được phiếu của mình.',
        '– Chỉ sửa và xóa được khi phiếu đang ở trạng thái Đang tạo hoặc Không duyệt.',
        '– Người duyệt không sửa được nội dung phiếu — thao tác duyệt đi qua đường riêng, '
        'không dùng chung với chức năng sửa.',
    ], ['Sửa phiếu', 'Xóa phiếu']),
    ('BR-09', 'Ràng buộc dữ liệu theo loại chi và hình thức thanh toán', [
        '– Hình thức chuyển khoản: chọn đối tượng nhận tiền một lần ở cấp phiếu và bắt buộc '
        'khối Thông tin ngân hàng khi gửi duyệt.',
        '– Hình thức tiền mặt: chọn đối tượng theo từng dòng chi tiết, không có khối ngân '
        'hàng.',
        '– Loại Chi trả nhà cung cấp: bắt buộc ít nhất một file đính kèm khi gửi duyệt; ba '
        'loại còn lại không bắt buộc.',
        '– Loại Thanh toán chi phí vận chuyển NCC: bắt buộc Nhà cung cấp và Đến ngày; dòng '
        'chi tiết do hệ thống sinh, không thêm / xóa bằng tay; chỉ dòng được tích mới bắt '
        'buộc số tiền.',
        '– Loại Chi thưởng thực hiện hợp đồng: không chọn đối tượng; hợp đồng lọc theo '
        'quyền hưởng thưởng của người lập; với hình thức chuyển khoản thì khối ngân hàng '
        'lấy theo hồ sơ của chính người lập.',
        '– Nhà cung cấp nước ngoài: bắt buộc thêm Ngân hàng, Swift Code và Phí.',
    ], ['Lập phiếu', 'Sửa phiếu']),
    ('BR-10', 'Ràng buộc khác nhau giữa Lưu nháp và Lưu và gửi duyệt', [
        '– Lưu nháp: bắt buộc Lý do chi và tỷ giá lớn hơn 0; không bắt buộc bảng chi tiết, '
        'khối ngân hàng và file đính kèm.',
        '– Lưu và gửi duyệt: bắt buộc thêm ít nhất một dòng chi tiết hợp lệ, khối ngân hàng '
        '(nếu chuyển khoản) và file đính kèm (nếu loại Chi trả nhà cung cấp).',
        '– Trong cả hai trường hợp, dòng chi tiết đã thêm đều phải có đủ đối tượng, hợp '
        'đồng và số tiền từ 1 trở lên.',
    ], ['Lập phiếu', 'Sửa phiếu']),
    ('BR-11', 'Nguồn hợp đồng theo loại chi', [
        '– Loại Chi trả nhà cung cấp lấy từ năm nguồn hợp đồng MUA của nhà cung cấp.',
        '– Loại Chi trả lại khách hàng và Chi thưởng thực hiện hợp đồng lấy từ các nguồn '
        'hợp đồng BÁN.',
        '– Loại Thanh toán chi phí vận chuyển NCC không gắn hợp đồng mà gắn chuyến xe.',
        '– Hệ thống kiểm tra loại hợp đồng gửi lên phải đúng nhóm của loại chi; sai nhóm '
        'thì không lưu được.',
        '– Một hợp đồng chỉ được chọn một lần trong cùng một phiếu.',
    ], ['Chọn đối tượng và hợp đồng', 'Lập phiếu']),
    ('BR-12', 'Công nợ tính theo sổ kế toán, không lưu trong phiếu', [
        '– Công nợ được tính lại mỗi lần mở phiếu hoặc mở cửa sổ chọn hợp đồng, dựa trên sổ '
        'kế toán.',
        '– Hợp đồng chưa phát sinh bút toán kế toán thì giá trị hiển thị bằng 0 — đây là '
        'hiện trạng đã được chấp nhận, không phải lỗi dữ liệu.',
        '– Trần số tiền đề nghị chỉ áp khi công nợ lớn hơn 0.',
    ], ['Chọn đối tượng và hợp đồng', 'Lập phiếu', 'Xem chi tiết']),
    ('BR-13', 'Tỷ giá và quy đổi VND', [
        '– Loại tiền VNĐ: tỷ giá luôn bằng 1, ô bị khóa, bảng chi tiết chỉ có một cột số '
        'tiền.',
        '– Loại tiền khác VNĐ: hệ thống tự điền tỷ giá của loại tiền đó khi người dùng đổi '
        'loại tiền; người dùng vẫn sửa tay được.',
        '– Số tiền quy đổi VND của một dòng bằng số tiền nhập nhân với tỷ giá.',
        '– Tỷ giá bằng 0 hoặc để trống thì hệ thống báo “Phải lớn hơn 0” và không cho lưu.',
    ], ['Lập phiếu', 'Sửa phiếu']),
    ('BR-14', 'Thông báo theo sự kiện', [
        '– Gửi duyệt: báo cho nhóm Trưởng phòng duyệt cùng công ty với phiếu.',
        '– Duyệt xong một cấp: báo cho nhóm của cấp kế tiếp (việc cần làm), đồng thời báo '
        'cho người lập và cấp vừa duyệt trước đó (việc đã xong).',
        '– Từ chối: báo cho người lập và cho tất cả các cấp mà phiếu đã đi qua; các cấp '
        'chưa đi qua không nhận thông báo.',
        '– Mọi thông báo đều mở đúng phiếu khi bấm vào, và luôn giới hạn trong công ty của '
        'phiếu.',
        '– Lỗi gửi thông báo không làm hỏng thao tác nghiệp vụ đang thực hiện.',
    ], ['Lập phiếu', 'Duyệt phiếu', 'Từ chối phiếu']),
    ('BR-15', 'File đính kèm', [
        '– File được tải lên ngay lúc người dùng chọn, không chờ tới lúc lưu phiếu, để xem '
        'trước được nội dung.',
        '– Chỉ nhận các định dạng pdf, png, jpg, jpeg, doc, docx, xls, xlsx, zip và dung '
        'lượng tối đa 20MB mỗi file.',
        '– Chỉ nhận file do chính chức năng tải lên của màn này sinh ra; không nhận đường '
        'dẫn tuỳ ý.',
        '– Xóa một file đã lưu sẽ xóa hẳn file khỏi kho lưu trữ, không hoàn tác được.',
        '– Chọn file rồi bỏ form giữa chừng thì file đã tải lên vẫn nằm trên kho lưu trữ — '
        'đây là đánh đổi đã được chấp nhận.',
    ], 'Quản lý file đính kèm'),
    ('BR-16', 'Ghi lịch sử thay đổi', [
        '– Mọi thao tác tạo mới, sửa, xóa, duyệt và từ chối đều được ghi một dòng lịch sử '
        'kèm người thực hiện và thời điểm.',
        '– Giá trị trong lịch sử lưu theo tên hiển thị tiếng Việt nên đổi tên danh mục về '
        'sau không làm sai lịch sử cũ.',
        '– Thao tác duyệt ghi kèm số tiền cấp đó vừa ghi cho TỪNG DÒNG chi tiết, dạng giá '
        'trị cũ → giá trị mới.',
        '– Thao tác từ chối ghi kèm ghi chú mà người từ chối đã nhập.',
        '– Lỗi ghi lịch sử không làm hỏng thao tác nghiệp vụ đang thực hiện.',
    ], 'Toàn màn hình'),
    ('BR-17', 'Ghi nhớ bộ lọc và cấu hình hiển thị', [
        '– Bộ lọc đang áp dụng được ghi nhớ trong 10 phút và lưu RIÊNG cho từng chế độ xem.',
        '– Cấu hình tiêu chí lọc lưu riêng theo người dùng và theo chế độ; cấu hình cột lưu '
        'riêng theo người dùng nhưng dùng CHUNG cho cả bốn chế độ.',
        '– Ba cột STT, Mã phiếu và Hành động luôn hiển thị và không đổi vị trí được.',
    ], ['Xem danh sách', 'Tìm kiếm và lọc', 'Cài đặt bộ lọc']),
    ('BR-18', 'Ranh giới với màn Phiếu chi và Ủy nhiệm chi', [
        '– Màn Phiếu đề nghị thanh toán dừng ở trạng thái Chờ tạo phiếu chi.',
        '– Kế toán thanh toán chuyển tiếp bằng nút Tạo phiếu chi (hình thức tiền mặt) hoặc '
        'Tạo ủy nhiệm chi (hình thức chuyển khoản); hai nút loại trừ nhau và chỉ hiện khi '
        'phiếu chưa có chứng từ chi.',
        '– Ba trạng thái Chờ duyệt phiếu chi, Duyệt phiếu chi và Đã hủy do màn Phiếu chi / '
        'Ủy nhiệm chi đặt; màn này chỉ hiển thị.',
    ], 'Toàn màn hình'),
])

d.save()
