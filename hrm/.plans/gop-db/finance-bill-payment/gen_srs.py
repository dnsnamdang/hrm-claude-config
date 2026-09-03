# -*- coding: utf-8 -*-
"""Sinh SRS (.docx) cho man "Phieu chi tien" (phan he Tai chinh).

Form chuan 2026-08-28 (4 chuong, Layout ghi MENU, rule_ref dau moi muc Gioi thieu,
Phan 4 la bang 5 cot, so do tong quan co phan cap).

Nguon doc code 03/09/2026 (nhanh gop_db) — xem docblock gen_testcase.py cung thu muc.
Anh that: pc_shots/ (dung chung voi HDSD).

Chay:  python .plans/gop-db/finance-bill-payment/gen_srs.py
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

SHOTS = os.path.join(HERE, 'pc_shots')
OUT = os.path.join(HERE, 'SRS - Phiếu chi tiền.docx')


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu chi'

ACTOR_KT = 'Kế toán thanh toán'
ACTOR_KTT = 'Kế toán trưởng'
ACTOR_TQ = 'Thủ quỹ'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/bill-payments',
           full_url='https://hrm-crm.eteksofts.com/finance/bill-payments',
           img_prefix='pc_')

# ============================================================== TRANG ĐẦU
d.title_block('Phiếu chi tiền')

d.h2('Mục lục')
d.toc()

# ========================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu chi tiền, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng và phân quyền của màn hình.',
    'Làm rõ HAI luồng nghiệp vụ tách biệt trên cùng một màn: luồng lập từ Đề nghị thanh toán '
    '(một cấp duyệt) và luồng Chi thu nhập cho nhân viên (hai cấp duyệt), cùng cách hệ thống tự '
    'nhận biết cấp duyệt theo trạng thái.',
    'Làm rõ thời điểm DUY NHẤT hệ thống ghi bút toán vào sổ kế toán (bước Thủ quỹ duyệt) và các '
    'cơ chế chống ghi trùng bút toán.',
    'Làm rõ quy tắc "lưu nháp không bắt buộc trường nào trừ Loại chi" và bảng loại chi nào bắt '
    'buộc có phiếu đề nghị — hai điểm dễ bị hiểu là sót kiểm tra.',
    'Làm rõ các điểm siết chặt hơn hệ thống cũ: điều kiện Sửa/Xóa theo người lập, kiểm trần số '
    'tiền lúc duyệt, và nơi lưu lý do hủy / ghi chú của người duyệt.',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu chi tiền',
     'Chứng từ kế toán ghi nhận khoản tiền doanh nghiệp chi ra. Mã sinh tự động dạng '
     '“{mã công ty}.PC{tháng năm}.{5 chữ số}”, ví dụ TPE.PC0826.00025.'),
    ('Luồng lập từ Đề nghị thanh toán',
     'Áp dụng với 6 loại chi: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, '
     'Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển NCC. Duyệt MỘT cấp '
     '(Thủ quỹ). Vòng đời: Đang tạo → Chờ chi tiền → Đã duyệt, hoặc → Hủy.'),
    ('Luồng Chi thu nhập cho nhân viên',
     'Lập TRỰC TIẾP, không qua phiếu đề nghị. Chọn phòng ban, hệ thống hút 6 khoản thu nhập của '
     'từng nhân viên từ sổ kế toán. Duyệt HAI cấp. Vòng đời: Đang tạo → Chờ KT trưởng duyệt → '
     'Chờ chi tiền → Đã duyệt, hoặc → Hủy.'),
    ('Tài khoản có',
     'Tài khoản ghi bên Có của bút toán, khai một lần cho cả phiếu (thường là tài khoản tiền).'),
    ('Tài khoản nợ', 'Tài khoản ghi bên Nợ, khai riêng cho từng dòng chi tiết.'),
    ('Số tiền đề nghị chi', 'Số tiền lấy từ phiếu đề nghị thanh toán. Chỉ đọc.'),
    ('Số tiền chi',
     'Số tiền kế toán chốt sẽ chi, do người lập phiếu nhập. Không được lớn hơn số tiền đề nghị '
     'chi của chính dòng đó.'),
    ('Số tiền thực chi',
     'Số tiền người duyệt xác nhận chi thật, nhập trong cửa sổ Duyệt. Bị kiểm trần một lần nữa '
     'ở bước duyệt.'),
    ('Số dư (bảng thu nhập nhân viên)',
     'Số tiền hệ thống tính cho từng nhân viên từ sổ kế toán. ĐƯỢC PHÉP ÂM (truy thu); trần số '
     'tiền chi so theo GIÁ TRỊ TUYỆT ĐỐI của số dư.'),
    ('Hình thức thanh toán',
     'TM (tiền mặt) hoặc CK (chuyển khoản). Chọn CK thì form hiện thêm khối “Ngân hàng nhận '
     'tiền” và “Ngân hàng trung gian”.'),
    ('Đang tạo', 'Phiếu nháp. Chỉ người lập nhìn thấy, sửa được và xoá được.'),
    ('Chờ KT trưởng duyệt',
     'Chỉ phát sinh với loại Chi thu nhập cho nhân viên. Chờ Kế toán trưởng duyệt (cấp 1).'),
    ('Chờ chi tiền', 'Chờ Thủ quỹ duyệt — cấp duyệt cuối, ghi bút toán vào sổ kế toán.'),
    ('Đã duyệt',
     'Thủ quỹ đã duyệt; hệ thống đã ghi bút toán. Không sửa, không xoá, không hủy được nữa.'),
    ('Hủy',
     'Người duyệt ở cấp đang chờ đã hủy phiếu kèm lý do. Không ghi bút toán nào.'),
], widths=[1.9, 4.1])

# ========================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán thanh toán',
     'Lập, sửa, xoá, gửi duyệt phiếu chi; mở được cửa sổ chọn phiếu đề nghị và endpoint lấy số '
     'liệu thu nhập nhân viên. Kiểm tra thực hiện ở phía máy chủ tại các endpoint ghi dữ liệu.'),
    ('Q2', 'Kế toán trưởng duyệt phiếu chi',
     'Duyệt và hủy phiếu ở trạng thái Chờ KT trưởng duyệt (chỉ phát sinh với loại Chi thu nhập '
     'cho nhân viên). Bắt buộc cùng công ty với phiếu.'),
    ('Q3', 'Thủ quỹ duyệt phiếu chi',
     'Duyệt và hủy phiếu ở trạng thái Chờ chi tiền. Đây là cấp duyệt cuối, ghi bút toán vào sổ '
     'kế toán. Bắt buộc cùng công ty với phiếu.'),
], widths=[0.8, 2.0, 3.2])
d.p('Các chức năng Xem danh sách, Xem chi tiết, In, Xuất Excel và Lịch sử KHÔNG gắn quyền riêng: '
    'chỉ cần người dùng nhìn thấy được phiếu theo phạm vi dữ liệu ở mục dưới.')

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả phiếu chi của tổng công ty', 'Toàn bộ phiếu chi của mọi công ty.'),
    ('V2', 'Xem tất cả phiếu chi của công ty',
     'Phiếu chi thuộc công ty của người đăng nhập. Không xác định được công ty thì rơi về nhánh '
     '“chỉ phiếu của mình”.'),
    ('—', '(không có cấp nào)', 'Chỉ phiếu chi do chính mình lập.'),
], widths=[0.8, 2.2, 3.0])
d.p('Vai trò quản trị hệ thống được xử lý tương đương V1 và được coi như có Q1, Q2, Q3. '
    'NGOẠI LỆ QUAN TRỌNG: với chức năng Sửa và Xóa, quản trị hệ thống KHÔNG được miễn trừ — vẫn '
    'phải là người lập phiếu, vì sửa vào phiếu của người khác là làm sai số liệu của họ.')
d.p('Bốn lớp bảo vệ dữ liệu áp dụng SAU CÙNG, không quyền nào gỡ được:')
d.bullets([
    'Phiếu ở trạng thái Đang tạo của người khác luôn bị loại khỏi danh sách; quyền xem theo cấp '
    'cũng KHÔNG mở được màn chi tiết của nháp người khác.',
    'Không xác định được người đăng nhập thì danh sách rỗng tuyệt đối.',
    'Người đã duyệt một phiếu (ở bất kỳ cấp nào) luôn mở lại được phiếu đó ở màn chi tiết.',
    'Người có quyền duyệt luôn mở được phiếu CÙNG CÔNG TY đang chờ ĐÚNG cấp mình — không có '
    'nhánh này thì người sắp phải duyệt lại không mở nổi phiếu để duyệt.',
])
d.p('So sánh công ty: hai vế cùng rỗng KHÔNG được coi là cùng công ty. Hệ thống cũ so bằng phép '
    'so lỏng nên mọi người chưa gắn hồ sơ nhân viên đều “cùng công ty” với các phiếu chưa xác '
    'định công ty — đây là lỗ hổng đã được bịt.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Không có quyền nào'], [
    ('FR-01 Truy cập & xem danh sách', '✅ (theo phạm vi V1–V2)', '✅ (theo phạm vi V1–V2)',
     '✅ (theo phạm vi V1–V2)', '✅ (chỉ phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc danh sách', '✅', '✅', '✅', '✅'),
    ('FR-03 Tuỳ chỉnh bộ lọc và cột hiển thị', '✅', '✅', '✅', '✅'),
    ('FR-04 Tạo mới phiếu chi', '✅', '❌', '❌', '❌'),
    ('FR-05 Chọn phiếu đề nghị từ popup', '✅', '❌', '❌', '❌'),
    ('FR-06 Lấy số liệu thu nhập nhân viên', '✅', '❌', '❌', '❌'),
    ('FR-07 Sửa phiếu chi', '✅ (nháp của chính mình)', '❌', '❌', '❌'),
    ('FR-08 Xem chi tiết phiếu chi', '✅', '✅', '✅', '✅ (chỉ phiếu của mình)'),
    ('FR-09 Duyệt phiếu chi', '❌', '✅ (Chờ KT trưởng duyệt)', '✅ (Chờ chi tiền)', '❌'),
    ('FR-10 Hủy phiếu chi', '❌', '✅ (Chờ KT trưởng duyệt)', '✅ (Chờ chi tiền)', '❌'),
    ('FR-11 Xóa phiếu chi', '✅ (nháp của chính mình)', '❌', '❌', '❌'),
    ('FR-12 In phiếu chi', '✅', '✅', '✅', '✅ (phiếu xem được)'),
    ('FR-13 Xuất Excel một phiếu', '✅', '✅', '✅', '✅ (phiếu xem được)'),
    ('FR-14 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅ (phiếu xem được)'),
], widths=[2.0, 1.4, 1.3, 1.3, 1.2])

# ========================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR_KT, [0, 1, 2, 3]),
     (ACTOR_KTT, [0, 3]),
     (ACTOR_TQ, [0, 3])],
    [('FR-01', 'Xem danh sách phiếu chi', 'view'),
     ('FR-04', 'Tạo mới phiếu chi', 'crud'),
     ('FR-07', 'Sửa phiếu chi', 'crud'),
     ('FR-08', 'Xem chi tiết phiếu chi', 'view')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Tuỳ chỉnh bộ lọc và cột', 'view', 'extend', [0], None),
     ('FR-11', 'Xóa phiếu chi', 'action', 'extend', [0], None),
     ('FR-14', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-05', 'Chọn phiếu đề nghị từ popup', 'crud', 'include', [1, 2], None),
     ('FR-06', 'Lấy số liệu thu nhập nhân viên', 'crud', 'include', [1, 2], None),
     ('FR-09', 'Duyệt phiếu chi', 'action', 'extend', [3], None),
     ('FR-10', 'Hủy phiếu chi', 'action', 'extend', [3], None),
     ('FR-12', 'In phiếu chi', 'io', 'extend', [3], None),
     ('FR-13', 'Xuất Excel một phiếu', 'io', 'extend', [3], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu chi tiền')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------ 2.1 FR-01
d.h3('2.1 Xem danh sách phiếu chi')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu chi tiền tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu chi',
    mota='Hiển thị bảng phiếu chi nằm trong phạm vi dữ liệu của người đăng nhập, kèm phân trang '
         'và ô thống kê tổng số phiếu khớp bộ lọc. Chỉ có một mục menu trỏ vào màn này; các cách '
         'xem riêng của hệ thống cũ nay là ô lọc Người lập và ô lọc Trạng thái.',
    tacnhan='%s; %s; %s; Người dùng đã đăng nhập' % (ACTOR_KT, ACTOR_KTT, ACTOR_TQ),
    dieukien='Người dùng đã đăng nhập vào phân hệ Tài chính.',
    chinh='1. Người dùng vào menu Tài chính → Quản lý tiền → Thanh toán tiền mặt → Phiếu chi.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền cao nhất mà người dùng có '
          '(V1 → V2 → không có cấp nào).\n'
          '3. Hệ thống loại bỏ phiếu Đang tạo của người khác khỏi kết quả.\n'
          '4. Hệ thống trả về trang đầu tiên, sắp xếp theo Ngày tạo giảm dần, kèm tổng số phiếu, '
          'danh sách trạng thái, danh sách loại chi và danh sách phòng ban để dựng ô lọc.\n'
          '5. Bảng hiển thị dữ liệu; ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có phiếu nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”\n'
        '• Không xác định được người đăng nhập → danh sách rỗng tuyệt đối.\n'
        '• Có bộ lọc đã lưu trong vòng 10 phút → khôi phục bộ lọc đó rồi mới nạp dữ liệu.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('01-danh-sach.png'),
         shot_caption='Màn Danh sách phiếu chi lúc mới truy cập')
d.figure(shot('02-danh-sach-cot-phai.png'),
         'Danh sách sau khi cuộn ngang — thấy cột Trạng thái và Hành động', width_in=6.2)

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Danh sách phiếu chi',
     'Hiển thị ở thanh tiêu đề và ở đầu khối lưới.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Luôn hiển thị, không gắn cờ quyền ở giao diện; quyền Q1 chặn ở phía máy chủ.'),
    ('Nút cấu hình cột', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ Tuỳ chỉnh cột hiển thị.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự theo trang',
     'Luôn hiển thị, không tắt được.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '{mã công ty}.PC{tháng năm}.{5 chữ số}',
     'Theo dữ liệu',
     'Luôn hiển thị, không tắt được; là đường dẫn sang màn chi tiết. Sắp xếp được.'),
    ('Cột Mã phiếu đề nghị chi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Là đường dẫn sang màn chi tiết Đề nghị thanh toán. Loại Chi thu nhập cho nhân viên hiện '
     'dấu gạch ngang.'),
    ('Cột Loại chi', 'Table/Grid', 'Read-only', 'Danh sách 7 giá trị', 'Theo dữ liệu', '–'),
    ('Cột Khách hàng / Nhà cung cấp', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Đối tượng nhận tiền của dòng chi tiết đầu tiên; không có thì hiện dấu gạch ngang.'),
    ('Cột Số tiền', 'Number', 'Read-only', '≥ 0', 'Theo dữ liệu',
     'Tổng số tiền chi của phiếu, căn phải, ngăn cách hàng nghìn. Sắp xếp được.'),
    ('Cột Người đề nghị', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người lập phiếu đề nghị thanh toán, khác cột Người tạo.'),
    ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Cột sắp xếp mặc định, chiều giảm dần.'),
    ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'Người lập phiếu chi.'),
    ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
     'Sắp xếp được.'),
    ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 5 giá trị', 'Theo dữ liệu',
     'Nhãn xám với Đang tạo, vàng với hai trạng thái chờ duyệt, xanh với Đã duyệt, đỏ với Hủy. '
     'Sắp xếp được.'),
    ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Theo trạng thái và quyền',
     'Luôn hiển thị, không tắt được. Tối đa 2–3 nút chính, phần còn lại trong menu ba chấm.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc và nằm trong phạm vi quyền.'),
    ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, cỡ 10',
     'Đổi cỡ trang đưa danh sách về trang 1.'),
    ('Thanh cuộn ngang', 'Table/Grid', 'Enable', '–', 'Hiển thị',
     'Có ở cả trên và dưới bảng vì bảng 14 cột rộng hơn màn hình.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Khôi phục bộ lọc đã lưu nếu còn trong 10 phút.\n'
     '– Xác định cấp quyền xem cao nhất của người dùng.\n'
     'During:\n– Áp phạm vi dữ liệu theo cấp quyền.\n'
     '– Loại bỏ phiếu Đang tạo của người khác.\n'
     'After:\n– Trả về trang 1 sắp xếp theo Ngày tạo giảm dần, kèm tổng số phiếu và các danh '
     'sách dùng để dựng ô lọc.'),
    ('Bấm tiêu đề cột sắp xếp', 'Click',
     'Before:\n– Chỉ nhận các cột nằm trong danh sách cho phép sắp xếp.\n'
     'After:\n– Đảo chiều sắp xếp, đưa về trang 1, giữ nguyên bộ lọc.'),
    ('Bấm mã phiếu', 'Click', 'After:\n– Điều hướng sang màn chi tiết phiếu chi tương ứng.'),
    ('Bấm mã phiếu đề nghị chi', 'Click',
     'After:\n– Điều hướng sang màn chi tiết Đề nghị thanh toán tương ứng.'),
    ('Bấm số trang / đổi số dòng mỗi trang', 'Click / Change',
     'Before:\n– Giữ nguyên bộ lọc và chiều sắp xếp.\n'
     'After:\n– Nạp lại dữ liệu; đổi cỡ trang thì đưa về trang 1.'),
])

# ------------------------------------------------------ 2.2 FR-02
d.h3('2.2 Tìm kiếm và lọc danh sách')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Phiếu '
           'chi tiền tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu chi',
    mota='Thu hẹp danh sách theo mã phiếu, mã phiếu đề nghị, loại chi, trạng thái, người lập, '
         'người đề nghị, phòng ban, đối tượng nhận tiền, khoảng số tiền và khoảng ngày lập. Các '
         'điều kiện cộng dồn với nhau.',
    tacnhan='%s; %s; %s' % (ACTOR_KT, ACTOR_KTT, ACTOR_TQ),
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
        '• Tham số lạ thêm vào đường dẫn không mở rộng được phạm vi dữ liệu.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('03-loc-nang-cao.png'),
         shot_caption='Khối Tìm kiếm nâng cao khi đang mở')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Dòng gợi ý “Tìm theo mã phiếu chi...”. KHÔNG tự tìm khi gõ — phải bấm nút Tìm kiếm.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Áp giá trị ô tìm nhanh và đưa về trang 1.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Xoá mọi điều kiện lọc và ô tìm nhanh, nạp lại danh sách trang 1.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Đóng/mở khối 9 ô lọc; đổi chữ thành “Ẩn tìm kiếm nâng cao” khi đang mở.'),
    ('Ô lọc Mã phiếu đề nghị chi', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tự lọc ngay khi đổi giá trị.'),
    ('Ô lọc Loại chi', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Không', 'Trống', '–'),
    ('Ô lọc Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống',
     'Chọn “Đang tạo” chỉ ra nháp của chính người dùng.'),
    ('Ô lọc Người lập', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu chi.'),
    ('Ô lọc Người đề nghị', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu đề nghị thanh toán.'),
    ('Ô lọc Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống', '–'),
    ('Ô lọc Khách hàng / Nhà cung cấp', 'Dropdown', 'Enable', 'Danh sách tìm từ xa', 'Không',
     'Trống', 'Phải gõ từ 2 ký tự trở lên mới hiện gợi ý; gộp chung nguồn khách hàng và nhà cung '
     'cấp.'),
    ('Ô lọc Số tiền từ / Số tiền đến', 'Number', 'Enable', '≥ 0', 'Không', 'Trống',
     'So theo cột “Số tiền” của lưới.'),
    ('Ô lọc Ngày lập từ / Ngày lập đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc theo ngày lập phiếu chi; cả hai mốc lấy trọn ngày.'),
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
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Phiếu chi '
           'tiền tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Tuỳ chỉnh bộ lọc và cột hiển thị',
    mota='Cho phép mỗi người dùng tự chọn những ô lọc và những cột muốn nhìn thấy, kèm thứ tự '
         'hiển thị. Cấu hình lưu riêng theo từng người và từng màn hình.',
    tacnhan='%s; %s; %s' % (ACTOR_KT, ACTOR_KTT, ACTOR_TQ),
    dieukien='Đang ở màn danh sách.',
    chinh='1. Người dùng bấm nút Cài đặt bộ lọc (hoặc nút cấu hình cột).\n'
          '2. Hệ thống mở cửa sổ với danh sách ô lọc (hoặc cột) kèm ô tích chọn.\n'
          '3. Người dùng bỏ tích mục không cần và kéo thả để đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống áp cấu hình ngay và ghi nhớ cho lần sau.',
    phu='• Bấm Khôi phục mặc định ở cửa sổ Cài đặt bộ lọc → đưa về đủ 9 nhóm ô theo thứ tự ban '
        'đầu.\n'
        '• Bấm Đóng → thoát mà không lưu thay đổi.\n'
        '• Ba cột STT, Mã phiếu và Hành động bị khoá, không bỏ tích được.',
    dacbiet='Cấu hình cột của màn này không ảnh hưởng tới cấu hình cột của màn hình khác.')

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
d.h3('2.4 Tạo mới phiếu chi')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới phiếu chi', 'crud',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Chọn phiếu đề nghị từ popup'),
             ('include', 'Lấy số liệu thu nhập nhân viên'),
             ('include', 'Sinh mã phiếu tự động'),
             ('extend', 'Gửi thông báo cho cấp duyệt khi gửi duyệt')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-04 Tạo mới phiếu chi')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Tạo mới phiếu chi',
    mota='Lập phiếu chi theo một trong hai luồng nghiệp vụ, phân biệt bằng ô Loại chi. Người lập '
         'có thể lưu nháp để làm tiếp, hoặc lưu và gửi duyệt ngay.',
    tacnhan='%s' % ACTOR_KT,
    dieukien='Người dùng có quyền Q1 (hoặc là quản trị hệ thống).',
    chinh='1. Người dùng bấm nút Tạo mới; hệ thống mở màn Thêm phiếu chi tiền với các giá trị '
          'mặc định (hình thức thanh toán TM, loại tiền VNĐ, tỷ giá 1, người đề nghị và phòng '
          'ban theo người đăng nhập).\n'
          '2. Người dùng chọn Loại chi — bước này quyết định cấu trúc form.\n'
          '3a. Luồng lập từ Đề nghị thanh toán: chọn phiếu đề nghị; hệ thống kéo về hình thức '
          'thanh toán, loại tiền, tỷ giá, lý do chi, thông tin đối tượng nhận tiền và toàn bộ '
          'dòng chi tiết.\n'
          '3b. Luồng Chi thu nhập cho nhân viên: chọn Phòng ban chi; hệ thống hút số liệu thu '
          'nhập của từng nhân viên trong phòng ban đó.\n'
          '4. Người dùng nhập Người nhận, Tài khoản có, tài khoản nợ và số tiền của từng dòng.\n'
          '5. Người dùng bấm Lưu nháp, hoặc bấm Lưu và gửi duyệt (có hộp xác nhận).\n'
          '6. Hệ thống khóa dòng phiếu đề nghị, kiểm tra chưa có phiếu chi nào, sinh mã tự động '
          'và ghi phiếu cùng các dòng chi tiết.\n'
          '7. Nếu gửi duyệt: phiếu chuyển sang trạng thái chờ duyệt tương ứng luồng và hệ thống '
          'gửi thông báo cho cấp duyệt đó trong cùng công ty.',
    phu='• Thiếu quyền Q1 → từ chối với thông báo “Bạn không có quyền lập phiếu chi tiền”.\n'
        '• Lưu nháp: KHÔNG bắt buộc trường nào ngoài Loại chi; các rule định dạng vẫn áp.\n'
        '• Gửi duyệt thiếu trường bắt buộc → báo lỗi đỏ ngay dưới từng ô, không đóng màn, giữ '
        'nguyên dữ liệu đã nhập.\n'
        '• Phiếu đề nghị đã có phiếu chi khác → bị chặn, không tạo phiếu thứ hai.\n'
        '• Bấm nút lưu nhiều lần liên tiếp → chỉ tạo đúng một phiếu.\n'
        '• Bấm Quay lại khi đã nhập dở → hỏi xác nhận rời trang.',
    dacbiet='Hai điểm KHÁC hệ thống cũ có chủ đích: (1) lưu nháp không bắt buộc trường nào ngoài '
            'Loại chi — hệ thống cũ áp cùng một bộ luật cho cả hai nút; (2) số tiền chi bị kiểm '
            'trần “không vượt số tiền đề nghị chi” ngay ở bước lưu — hệ thống cũ kẹp cứng giá '
            'trị ở giao diện nên người dùng không hiểu vì sao số tự nhảy về.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới',
         shot=shot('06-tao-moi.png'),
         shot_caption='Màn Thêm phiếu chi tiền khi vừa mở')
d.figure(shot('08-chon-loai-chi.png'), 'Danh sách 7 loại chi trên form', width_in=6.2)
d.figure(shot('12-form-da-chon-de-nghi.png'),
         'Luồng lập từ Đề nghị thanh toán — form sau khi chọn phiếu đề nghị', width_in=6.2)
d.figure(shot('09-form-chi-thu-nhap-nv.png'),
         'Luồng Chi thu nhập cho nhân viên — form đổi cấu trúc, xuất hiện ô Phòng ban chi',
         width_in=6.2)

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Số phiếu đề nghị', 'Textbox', 'Read-only / Ẩn', '–', 'Tuỳ loại chi', 'Trống',
     'Bấm vào ô để mở cửa sổ chọn. Ẩn hẳn với loại Chi thu nhập cho nhân viên. Bắt buộc khi gửi '
     'duyệt với 3 loại: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD.'),
    ('Tài khoản có', 'Dropdown', 'Enable', 'Danh sách tài khoản', 'Có khi gửi duyệt', 'Trống',
     'Chỉ liệt kê tài khoản đang hoạt động và là tài khoản cấp cuối.'),
    ('Loại chi', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Có — kể cả khi lưu nháp', 'Trống',
     'Trường DUY NHẤT bắt buộc ở đường lưu nháp; quyết định cấu trúc form và luồng duyệt.'),
    ('Hình thức thanh toán', 'Dropdown', 'Enable', 'TM / CK', 'Có với luồng Chi thu nhập nhân '
     'viên', 'TM', 'Chọn CK thì hiện thêm hai khối thông tin ngân hàng.'),
    ('Người nhận', 'Textbox', 'Enable', '0–255 ký tự', 'Có khi gửi duyệt', 'Trống', '–'),
    ('Loại tiền', 'Dropdown / Text', 'Enable / Read-only', '–',
     'Có với luồng Chi thu nhập nhân viên', 'VietNamDong',
     'Luồng lập từ đề nghị thì tự điền theo phiếu đề nghị.'),
    ('Tỷ giá (VND)', 'Number', 'Enable', '> 0', 'Có với luồng Chi thu nhập nhân viên', '1',
     'Tự điền theo phiếu đề nghị khi chọn phiếu.'),
    ('Người đề nghị', 'Text', 'Read-only', '–', '–', 'Người đang đăng nhập',
     'Đổi theo phiếu đề nghị đã chọn.'),
    ('Phòng ban', 'Text', 'Read-only', '–', '–', 'Phòng ban của người đăng nhập', '–'),
    ('Phòng ban chi', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban',
     'Có với luồng Chi thu nhập nhân viên', 'Trống',
     'CHỈ hiện với loại Chi thu nhập cho nhân viên; chọn xong hệ thống mới nạp bảng chi tiết.'),
    ('Lý do chi', 'Textarea', 'Enable / Read-only', '–', 'Có với luồng Chi thu nhập nhân viên',
     'Trống', 'Luồng lập từ đề nghị thì tự điền theo phiếu đề nghị.'),
    ('Khối Ngân hàng nhận tiền', 'Table/Grid', 'Enable / Ẩn', '–', 'Không', 'Ẩn',
     'Chỉ hiện với hình thức CK: Ngân hàng, Số tài khoản, Tài khoản, Tên ngân hàng, Swift Code, '
     'IBAN Number, Địa chỉ.'),
    ('Khối Ngân hàng trung gian', 'Table/Grid', 'Enable / Ẩn', '–', 'Không', 'Ẩn',
     'Cùng điều kiện hiện và cùng bộ trường với khối trên.'),
    ('Cột Tài khoản nợ', 'Dropdown', 'Enable', 'Danh sách tài khoản', 'Có khi gửi duyệt',
     'Theo phiếu đề nghị / theo dữ liệu hệ thống', '–'),
    ('Cột Số tiền đề nghị chi', 'Number', 'Read-only', '≥ 0', '–', 'Theo phiếu đề nghị', '–'),
    ('Cột Số tiền chi', 'Number', 'Enable', '0 – số tiền đề nghị chi của dòng', 'Có khi gửi '
     'duyệt', 'Theo phiếu đề nghị', 'Vượt trần thì báo “Không được lớn hơn số tiền đề nghị chi”.'),
    ('Bảng thu nhập nhân viên', 'Table/Grid', 'Enable / Ẩn', '–',
     'Có với luồng Chi thu nhập nhân viên', 'Ẩn',
     'Hai tab “Chi tiết” và “Chi tiết vụ việc”; cột ô tích, STT, Số tài khoản nợ, Tên tài khoản, '
     'Nhân viên, Số dư, Số tiền chi. Số dư được phép âm.'),
    ('Dòng Tổng cộng', 'Label', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
     'Cộng dọc từng cột tiền, cập nhật tức thời.'),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'KHÔNG hỏi xác nhận. Bị khoá trong lúc xử lý.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Mở hộp xác nhận trước khi lưu và gửi duyệt.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi inline', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Chữ đỏ ngay dưới ô bị lỗi; ô có viền đỏ.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'After:\n– Mở màn Thêm phiếu chi tiền với các giá trị mặc định.'),
    ('Chọn Loại chi', 'Change',
     'During:\n– Loại thuộc nhóm lập-từ-đề-nghị → giữ ô Số phiếu đề nghị, ẩn ô Phòng ban chi.\n'
     '– Loại Chi thu nhập cho nhân viên → ẩn ô Số phiếu đề nghị, hiện ô Phòng ban chi và đặt Lý '
     'do chi thành bắt buộc.\n'
     'After:\n– Dựng lại bảng chi tiết theo luồng tương ứng.'),
    ('Chọn Hình thức thanh toán', 'Change',
     'After:\n– Giá trị CK → hiện khối Ngân hàng nhận tiền và Ngân hàng trung gian; giá trị TM → '
     'ẩn hai khối đó.'),
    ('Bấm Lưu nháp / Lưu và gửi duyệt', 'Click',
     'Before:\n– Kiểm tra quyền Q1; không có quyền → hiển thị “Bạn không có quyền lập phiếu chi '
     'tiền” và dừng xử lý.\n'
     '– Với Lưu và gửi duyệt: mở hộp xác nhận, chỉ tiếp tục khi người dùng đồng ý.\n'
     'During:\n'
     '– Chưa chọn Loại chi → hiển thị “Bắt buộc chọn loại chi” (áp cả khi lưu nháp).\n'
     '– Loại chi ngoài danh sách hợp lệ → hiển thị “Loại chi không hợp lệ”.\n'
     '– Chỉ khi GỬI DUYỆT mới áp các ràng buộc bắt buộc sau:\n'
     '– Chưa chọn Tài khoản có → “Bắt buộc chọn tài khoản có”; tài khoản không tồn tại → “Tài '
     'khoản có không tồn tại”.\n'
     '– Chưa nhập Người nhận → “Bắt buộc nhập người nhận”; quá 255 ký tự → “Người nhận tối đa '
     '255 ký tự”.\n'
     '– Với 3 loại bắt buộc: chưa chọn phiếu đề nghị → “Bắt buộc chọn phiếu đề nghị thanh toán”; '
     'bảng chi tiết rỗng → “Phiếu chi phải có ít nhất 1 dòng chi tiết”.\n'
     '– Chưa chọn Tài khoản nợ của một dòng → “Bắt buộc chọn tài khoản nợ”.\n'
     '– Số tiền chi vượt số tiền đề nghị chi của dòng → “Không được lớn hơn số tiền đề nghị '
     'chi”.\n'
     '– Số tiền chi âm → “Số tiền duyệt chi không được âm”.\n'
     '– Luồng Chi thu nhập nhân viên: chưa chọn phòng ban → “Bắt buộc chọn phòng ban được chi”; '
     'chưa nhập lý do chi → “Bắt buộc nhập lý do chi”; thiếu tỷ giá → “Bắt buộc nhập tỷ giá”; tỷ '
     'giá không phải số → “Tỷ giá phải là số”.\n'
     '– Sáu khoản thu nhập cho phép SỐ ÂM (truy thu) nên không áp ràng buộc không-âm.\n'
     '– Nếu có lỗi thì KHÔNG thực hiện bước After.\n'
     'After:\n– Khóa dòng phiếu đề nghị rồi kiểm tra chưa có phiếu chi nào; đã có thì chặn và '
     'dừng.\n'
     '– Sinh mã phiếu tự động (có khóa dòng để hai người lưu cùng lúc không trùng mã), ghi phiếu '
     'và các dòng chi tiết.\n'
     '– Ghi công ty / phòng ban / bộ phận theo hồ sơ người lập, gán đè vô điều kiện.\n'
     '– Nếu gửi duyệt: chuyển phiếu sang “Chờ chi tiền” (luồng lập-từ-đề-nghị) hoặc “Chờ KT '
     'trưởng duyệt” (luồng Chi thu nhập nhân viên), cập nhật ngược trạng thái phiếu đề nghị và '
     'gửi thông báo tới cấp duyệt tương ứng trong cùng công ty.\n'
     '– Ghi một dòng lịch sử tạo mới.\n'
     '– Hiển thị “Thêm phiếu chi tiền thành công!” và quay về danh sách.'),
])

# ------------------------------------------------------ 2.5 FR-05
d.h3('2.5 Chọn phiếu đề nghị từ popup')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chọn phiếu đề nghị từ popup', 'crud',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Lọc phiếu Chờ tạo phiếu chi và chưa có phiếu chi')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-05 Chọn phiếu đề nghị từ popup')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Kịch bản tìm kiếm, Bộ lọc và Dropdown. Chỉ bổ sung các quy tắc riêng của màn Phiếu '
           'chi tiền tại phần mô tả chi tiết.', anchor='search')
d.intro_table(
    ten='Chọn phiếu đề nghị thanh toán',
    mota='Cửa sổ tìm và chọn MỘT phiếu đề nghị thanh toán để lập phiếu chi. Chỉ liệt kê phiếu đủ '
         'điều kiện.',
    tacnhan='%s' % ACTOR_KT,
    dieukien='Đang ở màn Tạo mới hoặc màn Sửa, đã chọn Loại chi thuộc luồng lập-từ-đề-nghị, và '
             'người dùng có quyền Q1.',
    chinh='1. Người dùng bấm vào ô “Số phiếu đề nghị”.\n'
          '2. Hệ thống kiểm tra quyền Q1 rồi mở cửa sổ, liệt kê phiếu đề nghị đang ở trạng thái '
          'Chờ tạo phiếu chi VÀ chưa có phiếu chi nào, sắp xếp mới nhất trước.\n'
          '3. Người dùng tìm theo mã phiếu đề nghị, loại chi hoặc người lập.\n'
          '4. Người dùng bấm vào dòng cần chọn.\n'
          '5. Cửa sổ tự đóng, hệ thống kéo dữ liệu phiếu đề nghị về form.',
    phu='• Thiếu quyền Q1 → từ chối với thông báo “Bạn không có quyền xem danh sách phiếu đề '
        'nghị chi”.\n'
        '• Không tìm thấy phiếu nào → danh sách rỗng, không báo lỗi.\n'
        '• Bấm Đóng → cửa sổ đóng, ô Số phiếu đề nghị giữ nguyên giá trị cũ.',
    dacbiet='Cửa sổ này CỐ Ý không áp phạm vi xem của màn Đề nghị thanh toán — mọi kế toán thanh '
            'toán đều chọn được mọi phiếu đề nghị đủ điều kiện. Vì vậy endpoint kéo dữ liệu phiếu '
            'đề nghị về form cũng gate bằng đúng quyền Q1, không gate bằng quyền xem của màn đề '
            'nghị; nếu không, người dùng chọn được phiếu rồi bị từ chối ngay lúc kéo dữ liệu.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới / Sửa => Chọn phiếu đề nghị chi',
         note='Cửa sổ được mở ngay trên màn Tạo mới hoặc màn Sửa phiếu chi.',
         shot=shot('11-popup-chon-de-nghi.png'),
         shot_caption='Cửa sổ Chọn phiếu đề nghị chi')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Không', 'Chọn phiếu đề nghị chi',
     'Phụ đề màu đỏ ghi “Chỉ phiếu Chờ tạo phiếu chi và chưa lập phiếu chi”.'),
    ('Ô Mã phiếu đề nghị', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm gần đúng theo mã.'),
    ('Ô Loại chi', 'Dropdown', 'Enable', 'Danh sách loại chi', 'Không', 'Trống', '–'),
    ('Ô Người lập', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu đề nghị.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp các điều kiện đã nhập.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xoá điều kiện tìm.'),
    ('Bảng danh sách', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu',
     'Bảy cột: STT, Mã phiếu đề nghị, Loại chi, Khách hàng / Nhà cung cấp, Số tiền, Người lập, '
     'Ngày lập. Bấm vào dòng để chọn.'),
    ('Phân trang của cửa sổ', 'Pagination', 'Enable', '–', '–', 'Trang 1, cỡ 10', '–'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không chọn gì.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm vào ô Số phiếu đề nghị', 'Click',
     'Before:\n– Kiểm tra quyền Q1; thiếu quyền → hiển thị “Bạn không có quyền xem danh sách '
     'phiếu đề nghị chi” và không mở cửa sổ.\n'
     'After:\n– Mở cửa sổ và nạp danh sách phiếu đề nghị đủ điều kiện.'),
    ('Bấm vào một dòng phiếu đề nghị', 'Click',
     'Before:\n– Kiểm tra quyền Q1 một lần nữa ở endpoint kéo dữ liệu; thiếu quyền → “Bạn không '
     'có quyền xem phiếu đề nghị chi”.\n'
     'After:\n– Điền mã phiếu đề nghị vào ô; kéo về hình thức thanh toán, loại tiền, tỷ giá, lý '
     'do chi, thông tin đối tượng nhận tiền và toàn bộ dòng chi tiết.\n'
     '– Hình thức CK thì hiện thêm hai khối thông tin ngân hàng.\n'
     '– Tự đóng cửa sổ.'),
])

# ------------------------------------------------------ 2.6 FR-06
d.h3('2.6 Lấy số liệu thu nhập nhân viên')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Lấy số liệu thu nhập nhân viên', 'crud',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Tổng hợp 6 khoản thu nhập từ sổ kế toán')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-06 Lấy số liệu thu nhập nhân viên')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Lấy số liệu thu nhập nhân viên theo phòng ban',
    mota='Với loại Chi thu nhập cho nhân viên, sau khi người dùng chọn Phòng ban chi, hệ thống tự '
         'tổng hợp 6 khoản thu nhập của từng nhân viên trong phòng ban đó từ sổ kế toán và nạp '
         'vào bảng chi tiết.',
    tacnhan='%s' % ACTOR_KT,
    dieukien='Đang ở màn Tạo mới hoặc màn Sửa, Loại chi = Chi thu nhập cho nhân viên, và người '
             'dùng có quyền Q1.',
    chinh='1. Người dùng chọn Phòng ban chi.\n'
          '2. Hệ thống kiểm tra quyền Q1 và sự tồn tại của phòng ban.\n'
          '3. Hệ thống tổng hợp số dư 6 khoản thu nhập của từng nhân viên trong phòng ban.\n'
          '4. Bảng chi tiết nạp mỗi nhân viên một dòng, tích chọn sẵn, điền sẵn tài khoản nợ.',
    phu='• Thiếu quyền Q1 → từ chối với thông báo “Bạn không có quyền xem số liệu thu nhập nhân '
        'viên”.\n'
        '• Phòng ban không tồn tại → báo “Không tìm thấy phòng ban”.\n'
        '• Phòng ban không có số liệu → bảng hiện “Không có dữ liệu phù hợp”, không báo lỗi.\n'
        '• Đổi sang phòng ban khác → bảng nạp lại toàn bộ, dữ liệu cũ bị thay.',
    dacbiet='Cột Số dư ĐƯỢC PHÉP ÂM (trường hợp truy thu). Trần số tiền chi so theo GIÁ TRỊ TUYỆT '
            'ĐỐI của số dư, nếu không thì các dòng số dư âm sẽ bị chặn oan.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Chi thu nhập cho nhân viên => Phòng ban chi',
         note='Bảng số liệu nạp ngay trên màn Tạo mới sau khi chọn Phòng ban chi.',
         shot=shot('10-bang-thu-nhap-nhan-vien.png'),
         shot_caption='Bảng thu nhập nhân viên sau khi chọn Phòng ban chi')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tab “Chi tiết”', 'Table/Grid', 'Enable', '–', 'Có', 'Hiển thị',
     'Bảng chính, mỗi dòng là một nhân viên.'),
    ('Tab “Chi tiết vụ việc”', 'Table/Grid', 'Enable', '–', 'Không', 'Ẩn',
     'Bảng phụ tách 6 khoản thu nhập của từng nhân viên.'),
    ('Ô tích chọn dòng', 'Checkbox', 'Enable', '–', 'Không', 'Tích sẵn tất cả',
     'Bỏ tích để loại nhân viên đó khỏi phiếu.'),
    ('Cột Số tài khoản nợ', 'Dropdown', 'Enable', 'Danh sách tài khoản', 'Có khi gửi duyệt',
     'Điền sẵn theo dữ liệu hệ thống', '–'),
    ('Cột Tên tài khoản', 'Text', 'Read-only', '–', '–', 'Theo tài khoản đã chọn', '–'),
    ('Cột Nhân viên', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', 'Mã và họ tên nhân viên.'),
    ('Cột Số dư', 'Number', 'Read-only', 'Có thể ÂM', '–', 'Theo sổ kế toán',
     'Giá trị âm là trường hợp truy thu, hiển thị đúng dấu.'),
    ('Cột Số tiền chi', 'Number', 'Enable', '≤ trị tuyệt đối của Số dư', 'Có khi gửi duyệt', '0',
     'Sáu khoản thu nhập bên trong cho phép số âm.'),
    ('Dòng Tổng cộng', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Cộng dọc cả 6 khoản thu nhập lẫn cột Số tiền chi.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Phòng ban chi', 'Change',
     'Before:\n– Kiểm tra quyền Q1; thiếu quyền → hiển thị “Bạn không có quyền xem số liệu thu '
     'nhập nhân viên” và không nạp bảng.\n'
     'During:\n– Phòng ban không tồn tại → báo “Không tìm thấy phòng ban”.\n'
     '– Tổng hợp 6 khoản thu nhập của từng nhân viên trong phòng ban từ sổ kế toán.\n'
     'After:\n– Nạp bảng chi tiết, tích chọn sẵn mọi dòng và điền sẵn tài khoản nợ.\n'
     '– Không có nhân viên nào có số liệu → hiển thị “Không có dữ liệu phù hợp”.'),
    ('Bỏ tích một dòng nhân viên', 'Change',
     'After:\n– Loại dòng đó khỏi phiếu và trừ khỏi dòng Tổng cộng.'),
])

# ------------------------------------------------------ 2.7 FR-07
d.h3('2.7 Sửa phiếu chi')

d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Sửa phiếu chi', 'crud',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Kiểm tra trạng thái Đang tạo và đúng người lập'),
             ('include', 'Chọn phiếu đề nghị từ popup')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-07 Sửa phiếu chi')

d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng theo '
           'SRS Các quy tắc chung - Quy tắc ghi lịch sử.', anchor='create')
d.intro_table(
    ten='Sửa phiếu chi',
    mota='Cập nhật nội dung của một phiếu chi đang ở trạng thái Đang tạo do chính người đăng nhập '
         'lập. Có thể lưu tiếp ở dạng nháp hoặc gửi duyệt luôn.',
    tacnhan='%s (người lập chính phiếu đó)' % ACTOR_KT,
    dieukien='Phiếu ở trạng thái Đang tạo, do chính người đăng nhập lập, VÀ người đó có quyền Q1 '
             '— đủ cả ba.',
    chinh='1. Người dùng bấm nút Sửa trên dòng danh sách hoặc trên màn chi tiết.\n'
          '2. Hệ thống kiểm tra đủ ba điều kiện; không thoả thì từ chối.\n'
          '3. Hệ thống mở màn Sửa, nạp đầy đủ thông tin chung và bảng chi tiết đã lưu.\n'
          '4. Người dùng chỉnh sửa rồi bấm Lưu nháp hoặc Lưu và gửi duyệt.\n'
          '5. Hệ thống áp lại toàn bộ quy tắc kiểm tra như màn Tạo mới rồi ghi lại phiếu.\n'
          '6. Hệ thống ghi một dòng lịch sử chỉnh sửa và một dòng lịch sử đổi trạng thái nếu '
          'trạng thái thay đổi.',
    phu='• Không thoả điều kiện sửa → từ chối và đưa về danh sách.\n'
        '• Đổi Loại chi sang luồng khác → cấu trúc form và bảng chi tiết đổi theo, dữ liệu cũ bị '
        'thay.\n'
        '• Đổi sang phiếu đề nghị khác → ràng buộc “một phiếu đề nghị một phiếu chi” vẫn được '
        'kiểm, bỏ qua chính phiếu đang sửa.\n'
        '• Bấm Quay lại khi đã sửa dở → hỏi xác nhận rời trang.',
    dacbiet='ĐIỂM SIẾT CHẶT HƠN HỆ THỐNG CŨ: hệ thống cũ chỉ kiểm trạng thái nên bất kỳ ai gọi '
            'được đường dẫn đều sửa được phiếu nháp của người khác. Quản trị hệ thống CỐ Ý không '
            'được miễn trừ ở chức năng này — miễn trừ chỉ áp cho việc XEM. Màn Sửa có thêm ba ô '
            'chỉ đọc: Mã phiếu, Người lập, Ngày lập.')

d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa',
         shot=shot('22-sua-phieu.png'),
         shot_caption='Màn Sửa phiếu chi tiền với dữ liệu đã lưu')

d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', '–', 'Sửa phiếu chi tiền',
     'Khác màn Tạo mới ghi “Thêm phiếu chi tiền”.'),
    ('Mã phiếu', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Chỉ có ở màn Sửa và màn Xem chi tiết.'),
    ('Người lập', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu',
     'Người lập gốc, không đổi sang người đang sửa.'),
    ('Ngày lập', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', '–', 'Theo dữ liệu', '–'),
    ('Các ô còn lại của Thông tin chung', 'Textbox / Dropdown', 'Enable', '–', 'Theo từng ô',
     'Theo dữ liệu', 'Quy tắc giống màn Tạo mới.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', 'Có khi gửi duyệt', 'Theo dữ liệu',
     'Sửa được Tài khoản nợ, Số tiền chi và Ghi chú từng dòng.'),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Giữ phiếu ở trạng thái Đang tạo.'),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Có hộp xác nhận; chuyển phiếu sang trạng thái chờ duyệt tương ứng luồng.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
])

d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Sửa', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu ở trạng thái Đang tạo, do chính người đăng nhập lập, '
     'và người đó có quyền Q1.\n'
     '– Kiểm tra lại ở phía máy chủ; không thoả → từ chối và đưa về danh sách.\n'
     'After:\n– Mở màn Sửa và nạp dữ liệu đã lưu, kèm tài khoản đã khóa (nếu có) để select không '
     'bị rỗng.'),
    ('Bấm Lưu nháp / Lưu và gửi duyệt', 'Click',
     'Before:\n– Kiểm tra lại đủ ba điều kiện sửa ở phía máy chủ.\n'
     'During:\n– Áp toàn bộ quy tắc kiểm tra như màn Tạo mới.\n'
     '– Khóa dòng phiếu đề nghị và kiểm tra ràng buộc một phiếu đề nghị một phiếu chi, bỏ qua '
     'chính phiếu đang sửa.\n'
     '– Nếu có lỗi thì KHÔNG thực hiện bước After.\n'
     'After:\n– Chụp lại nội dung cũ trước khi ghi để lấy được phần chênh lệch.\n'
     '– Ghi lại phiếu và các dòng chi tiết, cập nhật người sửa gần nhất.\n'
     '– Nếu chuyển sang trạng thái chờ duyệt: cập nhật ngược trạng thái phiếu đề nghị và gửi '
     'thông báo cho cấp duyệt tương ứng.\n'
     '– Ghi một dòng lịch sử chỉnh sửa; nếu trạng thái đổi thì ghi thêm một dòng lịch sử đổi '
     'trạng thái bằng TÊN trạng thái.\n'
     '– Hiển thị “Cập nhật phiếu chi tiền thành công!” và quay về danh sách.'),
])

# ------------------------------------------------------ 2.8 FR-08
d.h3('2.8 Xem chi tiết phiếu chi')

d.p('2.8.1 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Phiếu chi '
           'tiền tại phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu chi',
    mota='Hiển thị toàn bộ nội dung một phiếu chi ở chế độ chỉ đọc, kèm khối Lịch sử và bộ nút '
         'thao tác phù hợp với trạng thái và quyền của người xem.',
    tacnhan='%s; %s; %s' % (ACTOR_KT, ACTOR_KTT, ACTOR_TQ),
    dieukien='Người xem thoả một trong: là người lập phiếu; là người đã duyệt phiếu; là quản trị '
             'hệ thống; có V1; có V2 và cùng công ty; có quyền duyệt cấp đang chờ và cùng công ty.',
    chinh='1. Người dùng bấm vào mã phiếu trên danh sách (hoặc mở từ thông báo).\n'
          '2. Hệ thống nạp phiếu kèm dòng chi tiết, đối tượng nhận tiền, hợp đồng, phiếu đề nghị '
          'và người liên quan.\n'
          '3. Hệ thống kiểm tra quyền xem phiếu.\n'
          '4. Hệ thống hiển thị nội dung và tính các cờ quyết định 7 nút thao tác.',
    phu='• Không đủ quyền xem → từ chối với thông báo “Bạn không có quyền xem phiếu chi này”.\n'
        '• Mã phiếu không tồn tại → báo không tìm thấy dữ liệu.\n'
        '• Phiếu Đang tạo của người khác → không xem được.\n'
        '• Phiếu đã hủy → hiện thêm dải băng ở đầu màn với Lý do hủy và Ghi chú.',
    dacbiet='Bảy cờ quyền (xem / sửa / xoá / gửi duyệt / duyệt / hủy / in / xuất Excel) được tính '
            'ở MỘT nơi duy nhất và dùng chung cho cả màn danh sách lẫn màn chi tiết, nên hai màn '
            'không bao giờ lệch số nút.')

d.p('2.8.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết',
         shot=shot('15-chi-tiet-cho-chi-tien.png'),
         shot_caption='Màn chi tiết phiếu đang Chờ chi tiền, xem bằng tài khoản Thủ quỹ')
d.figure(shot('25-chi-tiet-da-xu-ly.png'),
         'Màn chi tiết phiếu đã hủy — dải băng đầu màn hiện Lý do hủy và Ghi chú', width_in=6.2)

d.p('2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu chi: {mã phiếu}', '–'),
    ('Dải băng Lý do hủy', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
     'CHỈ hiện với phiếu đã hủy; nền vàng, hiện Lý do hủy và Ghi chú của người duyệt.'),
    ('Khối Thông tin chung', 'Text', 'Read-only', '–', 'Theo dữ liệu',
     'Số phiếu đề nghị, Mã phiếu, Tài khoản có, Loại chi, Hình thức thanh toán, Người nhận, Loại '
     'tiền, Tỷ giá (VND), Người đề nghị, Phòng ban, Người lập, Ngày lập, Lý do chi.'),
    ('Khối thông tin ngân hàng', 'Table/Grid', 'Read-only', '–', 'Ẩn',
     'Chỉ với phiếu hình thức chuyển khoản: Nhà cung cấp, Phí, Ngân hàng nhận tiền, Ngân hàng '
     'trung gian.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Phiếu ngoại tệ có 2 cột cho mỗi nhóm tiền. Cuối bảng có dòng Tổng cộng.'),
    ('Khối Lịch sử', 'Table/Grid', 'Hiển thị', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để bung ra; có nút “Làm mới” và “Bộ lọc”.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện với phiếu Đang tạo do chính người xem lập và có quyền Q1.'),
    ('Nút Duyệt phiếu chi', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện khi phiếu đang chờ ĐÚNG cấp duyệt của người xem và cùng công ty.'),
    ('Nút Hủy phiếu chi', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Cùng điều kiện với nút Duyệt phiếu chi.'),
    ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Hiện với người xem được phiếu.'),
    ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', 'Hiện với người xem được phiếu.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Cùng điều kiện với nút Sửa.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị',
     'Về danh sách, giữ nguyên bộ lọc đã lưu.'),
], required=False)

d.p('2.8.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Nạp phiếu kèm dòng chi tiết, đối tượng nhận tiền, hợp đồng, phiếu đề nghị và '
     'người liên quan.\n'
     '– Kiểm tra quyền xem theo 6 nhánh nêu ở mục Điều kiện ban đầu; phiếu Đang tạo của người '
     'khác luôn bị chặn.\n'
     '– Không đủ quyền → hiển thị “Bạn không có quyền xem phiếu chi này”.\n'
     'After:\n– Hiển thị nội dung và tính 7 cờ quyền quyết định các nút thao tác.\n'
     '– Phiếu đã hủy → hiển thị thêm dải băng Lý do hủy và Ghi chú lấy từ lịch sử.'),
    ('Bấm nút Quay lại', 'Click',
     'After:\n– Về màn danh sách; bộ lọc đã lưu trong 10 phút được khôi phục.'),
])

# ------------------------------------------------------ 2.9 FR-09
d.h3('2.9 Duyệt phiếu chi')

d.p('2.9.1 Biểu đồ Usecase')
d.uc_figure('FR-09', 'Duyệt phiếu chi', 'action',
            [('include', 'Tự nhận cấp duyệt theo trạng thái phiếu'),
             ('include', 'Kiểm trần số tiền thực chi'),
             ('include', 'Ghi bút toán vào sổ kế toán'),
             ('extend', 'Chặn duyệt lại bằng khóa dòng')],
            actor=ACTOR_TQ,
            caption='Biểu đồ Use Case — FR-09 Duyệt phiếu chi')

d.p('2.9.2 Giới thiệu')
d.rule_ref('- Thông báo và Validate dữ liệu. Chỉ bổ sung các quy tắc riêng của màn Phiếu chi tiền '
           'tại phần mô tả chi tiết.', anchor='notice')
d.intro_table(
    ten='Duyệt phiếu chi',
    mota='Người duyệt xác nhận số tiền thực chi rồi duyệt phiếu. Hệ thống TỰ NHẬN BIẾT cấp duyệt '
         'theo trạng thái phiếu: Chờ KT trưởng duyệt cần quyền Q2, Chờ chi tiền cần quyền Q3. '
         'Chỉ bước Thủ quỹ mới ghi bút toán vào sổ kế toán.',
    tacnhan='%s (cấp 1, chỉ luồng Chi thu nhập nhân viên); %s (cấp cuối)' % (ACTOR_KTT, ACTOR_TQ),
    dieukien='Phiếu ở trạng thái Chờ KT trưởng duyệt (cần Q2) hoặc Chờ chi tiền (cần Q3), VÀ '
             'người dùng cùng công ty với phiếu.',
    chinh='1. Người duyệt mở màn chi tiết phiếu đang chờ duyệt.\n'
          '2. Bấm nút Duyệt phiếu chi; hệ thống mở cửa sổ hiện lại bảng chi tiết với cột Số tiền '
          'thực chi là ô nhập.\n'
          '3. Người duyệt điều chỉnh số tiền thực chi từng dòng và nhập Ghi chú nếu cần.\n'
          '4. Bấm Duyệt. Hệ thống khóa dòng phiếu, kiểm tra chưa duyệt rồi mới kiểm quyền.\n'
          '5a. Cấp Kế toán trưởng: chuyển phiếu sang Chờ chi tiền, KHÔNG ghi sổ kế toán, gửi '
          'thông báo cho Thủ quỹ cùng công ty.\n'
          '5b. Cấp Thủ quỹ: kiểm trần số tiền, ghi số duyệt chi vào từng dòng, chuyển phiếu sang '
          'Đã duyệt, ghi ngày hạch toán và người duyệt, cập nhật ngược phiếu đề nghị, ghi bút '
          'toán vào sổ kế toán, rồi gửi thông báo cho người lập.\n'
          '6. Hệ thống ghi lịch sử và hiển thị “Duyệt phiếu chi thành công!”.',
    phu='• Phiếu đã ở trạng thái Đã duyệt → từ chối với thông báo “Phiếu chi đã được duyệt trước '
        'đó.”\n'
        '• Không đủ quyền hoặc khác công ty → từ chối với thông báo “Bạn không có quyền duyệt '
        'phiếu chi này.”\n'
        '• Số tiền thực chi vượt trần → từ chối, không ghi bút toán nào.\n'
        '• Ghi chú vượt 500 ký tự → báo lỗi.\n'
        '• Bấm nút nhiều lần liên tiếp → chỉ ghi nhận một lần.\n'
        '• Toàn bộ bước ghi nằm trong một giao dịch: hoặc thành công trọn vẹn, hoặc không đổi gì.',
    dacbiet='Bước Thủ quỹ KHÔNG HOÀN TÁC ĐƯỢC. Hai điểm KHÁC hệ thống cũ: (1) hệ thống cũ không '
            'khóa dòng nên duyệt hai lần là nhân đôi bút toán trong sổ kế toán thật; (2) hệ thống '
            'cũ KHÔNG kiểm trần số tiền lúc duyệt do điều kiện kiểm tra bị viết sai nhánh. Chốt '
            'chặn “đã duyệt” được kiểm TRƯỚC chốt quyền, để người vừa duyệt xong không nhận thông '
            'báo thiếu quyền sai sự thật.')

d.p('2.9.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Duyệt phiếu chi',
         note='Cửa sổ Duyệt được mở ngay trên màn chi tiết.',
         shot=shot('16-popup-duyet.png'),
         shot_caption='Cửa sổ Duyệt phiếu chi tiền')

d.p('2.9.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Không', 'Duyệt phiếu chi tiền',
     'Phụ đề ghi “Phiếu chi: {mã phiếu}”.'),
    ('Bảng chi tiết trong cửa sổ', 'Table/Grid', 'Read-only', '–', 'Không', 'Theo dữ liệu',
     'Cột STT, Tài khoản nợ, Đối tượng, Số đơn hàng/Hợp đồng, Số tiền đề nghị chi, Đề nghị quy '
     'đổi, Số tiền thực chi, Thực chi quy đổi; kèm dòng Tổng cộng.'),
    ('Cột Số tiền thực chi', 'Number', 'Enable', '0 – số tiền đề nghị chi của dòng', 'Có',
     'Theo dữ liệu', 'Có dấu sao đỏ. Với luồng Chi thu nhập nhân viên, trần so theo giá trị '
     'tuyệt đối của số dư.'),
    ('Ô Ghi chú', 'Textarea', 'Enable', '0–500 ký tự', 'Không', 'Trống',
     'Gợi ý “Nhập ghi chú của người duyệt (nếu có)”. Lưu vào lịch sử, không lưu lên phiếu.'),
    ('Nút Duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     'Bị khoá trong lúc đang xử lý để chống bấm nhiều lần.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không duyệt.'),
])

d.p('2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Duyệt phiếu chi ở màn chi tiết', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu đang chờ ĐÚNG cấp duyệt của người xem và cùng công '
     'ty với phiếu.\n'
     'After:\n– Mở cửa sổ Duyệt, nạp lại bảng chi tiết với cột Số tiền thực chi là ô nhập.'),
    ('Bấm Duyệt trong cửa sổ', 'Click',
     'Before:\n– Chống bấm nhiều lần: bỏ qua nếu đang có một lần xử lý chưa xong.\n'
     '– KHÓA DÒNG phiếu rồi mới đọc trạng thái.\n'
     '– Phiếu đã ở trạng thái Đã duyệt → hiển thị “Phiếu chi đã được duyệt trước đó.” và dừng '
     'xử lý (kiểm TRƯỚC chốt quyền).\n'
     '– Không đủ quyền cấp đang chờ, hoặc khác công ty → hiển thị “Bạn không có quyền duyệt '
     'phiếu chi này.” và dừng xử lý.\n'
     'During:\n– Số tiền thực chi vượt trần của dòng → từ chối với thông báo số tiền chi không '
     'được vượt quá số dư; luồng Chi thu nhập nhân viên so theo giá trị tuyệt đối của số dư.\n'
     '– Số tiền thực chi âm → “Số tiền chi không được âm”.\n'
     '– Ghi chú vượt 500 ký tự → báo lỗi.\n'
     '– Nếu có lỗi thì KHÔNG thực hiện bước After.\n'
     'After (cấp Kế toán trưởng):\n– Chuyển phiếu sang Chờ chi tiền và ghi người duyệt cấp kế '
     'toán.\n'
     '– KHÔNG ghi một dòng bút toán nào — tiền chưa ra khỏi quỹ.\n'
     '– Gửi thông báo cho Thủ quỹ cùng công ty.\n'
     'After (cấp Thủ quỹ):\n– Ghi số duyệt chi vào từng dòng chi tiết.\n'
     '– Chuyển phiếu sang Đã duyệt, ghi ngày hạch toán và người duyệt.\n'
     '– Cập nhật ngược trạng thái phiếu đề nghị thanh toán và đẩy số duyệt chi xuống các dòng '
     'của phiếu đề nghị.\n'
     '– Dựng và ghi bút toán vào sổ kế toán; luồng Chi thu nhập nhân viên ghi theo cơ chế gộp.\n'
     '– Ghi một dòng log riêng (mã phiếu, số dòng sổ cái, tổng tiền) để đối soát về sau.\n'
     '– Gửi thông báo cho người lập phiếu.\n'
     '– Ghi lịch sử và hiển thị “Duyệt phiếu chi thành công!”.'),
])

# ------------------------------------------------------ 2.10 FR-10
d.h3('2.10 Hủy phiếu chi')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Hủy phiếu chi', 'action',
            [('include', 'Kiểm tra quyền duyệt cấp đang chờ và cùng công ty'),
             ('include', 'Nhập lý do hủy'),
             ('extend', 'Ghi lý do hủy và ghi chú vào lịch sử')],
            actor=ACTOR_TQ,
            caption='Biểu đồ Use Case — FR-10 Hủy phiếu chi')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa, Validate dữ liệu. Chỉ bổ sung các quy tắc riêng của màn '
           'Phiếu chi tiền tại phần mô tả chi tiết.', anchor='notice')
d.intro_table(
    ten='Hủy phiếu chi',
    mota='Người duyệt ở cấp đang chờ từ chối khoản chi kèm lý do. Phiếu chuyển sang trạng thái '
         'Hủy; KHÔNG ghi bút toán nào.',
    tacnhan='%s; %s' % (ACTOR_KTT, ACTOR_TQ),
    dieukien='Đúng bằng điều kiện Duyệt: phiếu ở trạng thái chờ duyệt của cấp mình VÀ cùng công '
             'ty với người dùng.',
    chinh='1. Người duyệt mở màn chi tiết phiếu đang chờ duyệt.\n'
          '2. Bấm nút Hủy phiếu chi; hệ thống mở cửa sổ nhập lý do.\n'
          '3. Nhập Lý do hủy (bắt buộc) và Ghi chú (tuỳ chọn), rồi bấm Xác nhận.\n'
          '4. Hệ thống khóa dòng phiếu, kiểm tra lại quyền.\n'
          '5. Hệ thống chuyển phiếu sang Hủy và ghi một dòng lịch sử kèm lý do hủy và ghi chú.',
    phu='• Lý do hủy để trống → hiển thị “Vui lòng nhập lý do hủy phiếu chi.”; cửa sổ không đóng.\n'
        '• Lý do hủy hoặc Ghi chú vượt 500 ký tự → báo lỗi tương ứng.\n'
        '• Không đủ quyền → từ chối với thông báo “Bạn không có quyền hủy phiếu chi này.”\n'
        '• Bấm Đóng → cửa sổ đóng, phiếu giữ nguyên trạng thái.',
    dacbiet='Người lập CỐ Ý không được tự hủy phiếu đã gửi duyệt: gửi đi rồi thì quyền định đoạt '
            'thuộc về người duyệt. Lý do hủy và Ghi chú KHÔNG được lưu lên phiếu (bảng dùng chung '
            'với hệ thống cũ không có cột tương ứng) mà lưu vào lịch sử thay đổi; màn chi tiết '
            'phiếu đã hủy hiện lại hai nội dung này ở dải băng đầu màn. Hệ thống cũ có ô ghi chú '
            'nhưng chữ gõ vào bị mất.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Hủy phiếu chi',
         note='Cửa sổ nhập lý do hủy được mở ngay trên màn chi tiết.',
         shot=shot('17-popup-huy.png'),
         shot_caption='Cửa sổ Hủy phiếu chi tiền')
d.figure(shot('18-loi-ly-do-huy.png'),
         'Lỗi khi bấm Xác nhận lúc chưa nhập lý do hủy', width_in=6.2)

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', 'Hủy phiếu chi tiền',
     'Phụ đề ghi “Phiếu chi: {mã phiếu}”; biểu tượng và viền màu đỏ.'),
    ('Ô Lý do hủy', 'Textarea', 'Enable', 'Trống',
     'Có dấu sao đỏ, bắt buộc, tối đa 500 ký tự.'),
    ('Ô Ghi chú', 'Textarea', 'Enable', 'Trống', 'Không bắt buộc, tối đa 500 ký tự.'),
    ('Lỗi inline của Lý do hủy', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     'Chữ đỏ ngay dưới ô; tự mất khi người dùng gõ nội dung.'),
    ('Nút Xác nhận', 'Button', 'Enable / Disable', 'Hiển thị',
     'Bị khoá trong lúc đang xử lý.'),
    ('Nút Đóng', 'Button', 'Enable', 'Hiển thị', 'Đóng cửa sổ, không hủy phiếu.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Hủy phiếu chi', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu đang chờ đúng cấp duyệt của người xem và cùng công '
     'ty.\n'
     'After:\n– Mở cửa sổ nhập lý do hủy, xoá lỗi cũ nếu có.'),
    ('Bấm Xác nhận trong cửa sổ hủy', 'Click',
     'Before:\n– Chống bấm nhiều lần: bỏ qua nếu đang có một lần xử lý chưa xong.\n'
     '– Khóa dòng phiếu rồi kiểm tra lại quyền hủy; không thoả → hiển thị “Bạn không có quyền '
     'hủy phiếu chi này.” và dừng xử lý.\n'
     'During:\n– Lý do hủy trống → hiển thị “Vui lòng nhập lý do hủy phiếu chi.”\n'
     '– Lý do hủy vượt 500 ký tự → “Lý do hủy không được quá 500 ký tự.”\n'
     '– Ghi chú vượt 500 ký tự → “Ghi chú không được quá 500 ký tự.”\n'
     '– Nếu có lỗi thì KHÔNG thực hiện bước After.\n'
     'After:\n– Chuyển phiếu sang trạng thái Hủy.\n'
     '– Ghi một dòng lịch sử đổi trạng thái, kèm lý do hủy và ghi chú của người duyệt.\n'
     '– KHÔNG ghi bút toán nào vào sổ kế toán.\n'
     '– Hiển thị “Hủy phiếu chi thành công!”.'),
])

# ------------------------------------------------------ 2.11 FR-11
d.h3('2.11 Xóa phiếu chi')

d.p('2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Xóa phiếu chi', 'action',
            [('include', 'Kiểm tra trạng thái Đang tạo, đúng người lập và quyền Q1'),
             ('include', 'Xoá kèm toàn bộ dòng chi tiết')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-11 Xóa phiếu chi')

d.p('2.11.2 Giới thiệu')
d.rule_ref('- Thông báo và Quy tắc Xóa. Chỉ bổ sung các quy tắc riêng của màn Phiếu chi tiền tại '
           'phần mô tả chi tiết.', anchor='notice')
d.intro_table(
    ten='Xóa phiếu chi',
    mota='Xoá vĩnh viễn một phiếu chi đang ở trạng thái Đang tạo do chính người đăng nhập lập, '
         'kèm toàn bộ dòng chi tiết.',
    tacnhan='%s (người lập chính phiếu đó)' % ACTOR_KT,
    dieukien='Đúng bằng điều kiện Sửa: phiếu ở trạng thái Đang tạo, do chính người đăng nhập lập, '
             'và người đó có quyền Q1.',
    chinh='1. Người dùng bấm nút Xóa trên dòng danh sách hoặc trên màn chi tiết.\n'
          '2. Hệ thống mở hộp xác nhận nêu rõ mã phiếu.\n'
          '3. Người dùng bấm Xóa để xác nhận.\n'
          '4. Hệ thống kiểm tra lại điều kiện, chụp lại nội dung phiếu rồi xoá phiếu cùng toàn '
          'bộ dòng chi tiết trong một giao dịch.\n'
          '5. Hệ thống ghi một dòng lịch sử xoá và nạp lại danh sách.',
    phu='• Không thoả điều kiện xoá → từ chối; hệ thống nạp lại danh sách cho khớp hiện trạng.\n'
        '• Bấm Hủy ở hộp xác nhận → không xoá gì.',
    dacbiet='Đây là xoá thật, không khôi phục lại được. Sau khi xoá, phiếu đề nghị thanh toán gắn '
            'với phiếu chi đó xuất hiện trở lại trong cửa sổ chọn và lập được phiếu chi mới. Mã '
            'phiếu đã dùng không được cấp lại.')

d.p('2.11.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa',
         note='Hộp xác nhận xoá được mở ngay trên màn danh sách hoặc màn chi tiết.',
         shot=shot('21-xac-nhan-xoa.png'),
         shot_caption='Hộp xác nhận xoá phiếu chi')

d.p('2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', 'Cố định.'),
    ('Nội dung hộp thoại', 'Label', 'Hiển thị',
     'Bạn có chắc muốn xóa phiếu chi tiền "{mã phiếu}"?', 'Có nêu rõ mã phiếu sẽ bị xoá.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Thực hiện xoá.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp thoại, không xoá.'),
    ('Nút Xóa trên dòng danh sách', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện',
     'Cùng điều kiện với nút Sửa.'),
], required=False, scope=False)

d.p('2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa', 'Click',
     'Before:\n– Nút chỉ hiển thị khi phiếu ở trạng thái Đang tạo, do chính người đăng nhập lập '
     'và người đó có quyền Q1.\n'
     'After:\n– Mở hộp xác nhận có nêu mã phiếu.'),
    ('Bấm Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra lại đủ ba điều kiện ở phía máy chủ; không thoả → từ chối và nạp lại '
     'danh sách.\n'
     'After:\n– Chụp lại nội dung phiếu kèm bảng chi tiết để ghi vào lịch sử.\n'
     '– Xoá phiếu cùng toàn bộ dòng chi tiết trong một giao dịch duy nhất.\n'
     '– Ghi một dòng lịch sử xoá.\n'
     '– Hiển thị “Xóa phiếu chi thành công!” và nạp lại danh sách.'),
])

# ------------------------------------------------------ 2.12 FR-12
d.h3('2.12 In phiếu chi')

d.p('2.12.1 Biểu đồ Usecase')
d.uc_figure('FR-12', 'In phiếu chi', 'io',
            [('include', 'Kiểm tra quyền xem phiếu'),
             ('include', 'Chọn mẫu in theo loại chi'),
             ('extend', 'Bổ sung 2 bảng kê với loại Chi thu nhập nhân viên')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-12 In phiếu chi')

d.p('2.12.2 Giới thiệu')
d.rule_ref('- Màn Xem chi tiết và Phân quyền. Chỉ bổ sung các quy tắc riêng của màn Phiếu chi '
           'tiền tại phần mô tả chi tiết.', anchor='detail')
d.intro_table(
    ten='In phiếu chi',
    mota='Mở bản in của phiếu ở tab mới, gồm ĐỦ 2 LIÊN, kèm ảnh tiêu đề thư của công ty.',
    tacnhan='%s; %s; %s' % (ACTOR_KT, ACTOR_KTT, ACTOR_TQ),
    dieukien='Người dùng xem được phiếu.',
    chinh='1. Người dùng bấm nút In trên màn chi tiết hoặc trên dòng danh sách.\n'
          '2. Hệ thống mở tab mới trỏ tới trang in.\n'
          '3. Hệ thống kiểm tra quyền xem, chọn mẫu in theo loại chi rồi điền dữ liệu phiếu vào '
          'mẫu.\n'
          '4. Trang in hiển thị 2 liên và trình duyệt tự mở hộp thoại in.',
    phu='• Không đủ quyền xem → từ chối với thông báo “Bạn không có quyền in phiếu chi này”.\n'
        '• Người dùng đóng hộp thoại in → vẫn xem được bản in trên trang và in lại bằng nút In.',
    dacbiet='Phiếu loại Chi thu nhập cho nhân viên dùng mẫu in riêng, có THÊM hai bảng kê ở cuối '
            'bản in: “Bảng kê chi tiết số tiền chi” và “Bảng kê chi tiết theo vụ việc” (6 khoản '
            'thu nhập). In phiếu KHÔNG làm thay đổi trạng thái, người cập nhật hay lịch sử.')

d.p('2.12.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => In',
         shot=shot('23-man-in.png'),
         shot_caption='Bản in phiếu chi loại Chi thu nhập cho nhân viên — có thêm 2 bảng kê')

d.p('2.12.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút In trên trang in', 'Button', 'Enable', '–', 'Hiển thị',
     'Nằm ở góc trên bên trái, mở lại hộp thoại in của trình duyệt.'),
    ('Ảnh tiêu đề thư', 'Icon Button', 'Hiển thị', '–', 'Theo công ty của phiếu',
     'Gồm logo, tên công ty, địa chỉ, điện thoại, email, website.'),
    ('Tiêu đề bản in', 'Label', 'Hiển thị', 'PHIẾU CHI', 'Cố định',
     'Dưới tiêu đề là ngày viết bằng chữ.'),
    ('Khối số liên và số phiếu', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Gồm “Liên số”, “Quyển số”, số phiếu, dòng “Nợ:” và “Có:” kèm số tiền.'),
    ('Thông tin đầu phiếu', 'Label', 'Hiển thị', '–', 'Theo dữ liệu',
     'Họ và tên người nhận tiền, Phòng ban, Lý do chi, Số tiền thực chi, dòng “Bằng chữ”.'),
    ('Khối ô ký', 'Label', 'Hiển thị', '–', 'Cố định',
     'Năm ô: BAN GIÁM ĐỐC, KẾ TOÁN TRƯỞNG, NGƯỜI NHẬN TIỀN, NGƯỜI LẬP PHIẾU, THỦ QUỸ.'),
    ('Bảng kê chi tiết số tiền chi', 'Table/Grid', 'Read-only', '–', 'Ẩn',
     'CHỈ với loại Chi thu nhập cho nhân viên: STT, Nhân viên, Số dư, Số tiền chi.'),
    ('Bảng kê chi tiết theo vụ việc', 'Table/Grid', 'Read-only', '–', 'Ẩn',
     'CHỈ với loại Chi thu nhập cho nhân viên: STT, Nhân viên và 6 khoản thu nhập kèm cột Tổng '
     'cộng.'),
], required=False)

d.p('2.12.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút In', 'Click', 'After:\n– Mở tab mới trỏ tới trang in của phiếu.'),
    ('Mở trang in', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu như chức năng Xem chi tiết; không đủ quyền → hiển thị '
     '“Bạn không có quyền in phiếu chi này”.\n'
     'During:\n– Chọn mẫu in theo loại chi rồi điền dữ liệu phiếu vào mẫu.\n'
     '– Loại Chi thu nhập cho nhân viên → dựng thêm hai bảng kê.\n'
     'After:\n– Hiển thị bản in 2 liên và mở hộp thoại in của trình duyệt; không ghi bất kỳ thay '
     'đổi nào lên phiếu.'),
])

# ------------------------------------------------------ 2.13 FR-13
d.h3('2.13 Xuất Excel một phiếu')

d.p('2.13.1 Biểu đồ Usecase')
d.uc_figure('FR-13', 'Xuất Excel một phiếu', 'io',
            [('include', 'Kiểm tra quyền xem phiếu')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-13 Xuất Excel một phiếu')

d.p('2.13.2 Giới thiệu')
d.rule_ref('- Quy tắc Excel và Cấu hình cột. Chỉ bổ sung các quy tắc riêng của màn Phiếu chi tiền '
           'tại phần mô tả chi tiết.', anchor='excel')
d.intro_table(
    ten='Xuất Excel một phiếu chi',
    mota='Tải về tệp Excel chứa nội dung của ĐÚNG MỘT phiếu chi đang xem. Màn hình không có chức '
         'năng xuất Excel cả danh sách.',
    tacnhan='%s; %s; %s' % (ACTOR_KT, ACTOR_KTT, ACTOR_TQ),
    dieukien='Người dùng xem được phiếu.',
    chinh='1. Người dùng bấm nút Xuất Excel trên màn chi tiết hoặc trên dòng danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống dựng tệp từ dữ liệu phiếu và trả về trình duyệt.',
    phu='• Không đủ quyền xem → từ chối với thông báo “Bạn không có quyền xuất Excel phiếu chi '
        'này”.\n'
        '• Nút bị khoá trong lúc đang dựng tệp để tránh tải trùng.',
    dacbiet=None)

d.p('2.13.3 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết => Xuất Excel',
         note='Nút Xuất Excel nằm ở thanh nút cuối màn chi tiết và ở cột Hành động của màn danh '
              'sách.',
         shot=shot('25-chi-tiet-da-xu-ly.png'),
         shot_caption='Nút Xuất Excel trên thanh nút cuối màn chi tiết')

d.p('2.13.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Nút Xuất Excel trên màn chi tiết', 'Button', 'Enable / Disable', 'Hiển thị',
     'Bị khoá trong lúc đang dựng tệp.'),
    ('Nút Xuất Excel trên dòng danh sách', 'Icon Button', 'Enable / Ẩn',
     'Hiện với phiếu xem được', 'Biểu tượng bảng tính.'),
], required=False, scope=False)

d.p('2.13.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xuất Excel', 'Click',
     'Before:\n– Kiểm tra quyền xem phiếu; không đủ quyền → hiển thị “Bạn không có quyền xuất '
     'Excel phiếu chi này” và dừng xử lý.\n'
     'After:\n– Dựng tệp Excel từ dữ liệu của đúng phiếu đó và trả về trình duyệt.'),
])

# ------------------------------------------------------ 2.14 FR-14
d.h3('2.14 Xem lịch sử thay đổi')

d.p('2.14.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử. Chỉ bổ sung các quy tắc riêng của màn Phiếu chi tiền tại phần '
           'mô tả chi tiết.', anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu chi',
    mota='Hiển thị các mốc thay đổi của một phiếu: tạo mới, chỉnh sửa từng trường, đổi trạng thái '
         'ở từng cấp duyệt và xoá, kèm người thực hiện và thời điểm. Có ở hai nơi với nội dung '
         'giống hệt nhau.',
    tacnhan='%s; %s; %s' % (ACTOR_KT, ACTOR_KTT, ACTOR_TQ),
    dieukien='Người dùng nhìn thấy phiếu.',
    chinh='1. Người dùng bấm nút Lịch sử trên dòng danh sách; hoặc mở màn chi tiết rồi bấm Xem '
          'lịch sử ở khối Lịch sử cuối trang.\n'
          '2. Hệ thống nạp các mốc lịch sử của phiếu, mới nhất trước.\n'
          '3. Người dùng có thể lọc theo nhóm thao tác hoặc bấm Làm mới.',
    phu='• Phiếu chưa từng thao tác trên hệ thống mới → hiển thị “Chưa có lịch sử thao tác nào.”\n'
        '• Không có mốc nào khớp bộ lọc → danh sách rỗng.',
    dacbiet='Lịch sử là NƠI DUY NHẤT lưu Lý do hủy và Ghi chú của người duyệt, vì bảng phiếu dùng '
            'chung với hệ thống cũ không có cột tương ứng. Đổi trạng thái luôn là một dòng lịch '
            'sử RIÊNG, tách khỏi dòng thay đổi thông tin.')

d.p('2.14.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử',
         note='Cửa sổ Lịch sử mở từ danh sách; khối Lịch sử nằm cuối màn chi tiết.',
         shot=shot('20-lich-su.png'),
         shot_caption='Cửa sổ Lịch sử thay đổi mở từ màn danh sách')
d.figure(shot('19-lich-su-man-chi-tiet.png'),
         'Khối Lịch sử ở cuối màn chi tiết', width_in=6.2)

d.p('2.14.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi', '–'),
    ('Phụ đề', 'Label', 'Hiển thị', '–', 'Phiếu: {mã phiếu}', '–'),
    ('Khối Lịch sử ở màn chi tiết', 'Table/Grid', 'Hiển thị', '–', 'Thu gọn',
     'Nút “Xem lịch sử” / “Thu gọn” và nút “Làm mới”.'),
    ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc các mốc theo nhóm thao tác.'),
    ('Danh sách mốc lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi mốc gồm thời điểm, loại thao tác, dòng “Người thực hiện: Họ tên — Phòng ban” và các '
     'trường thay đổi kèm giá trị cũ, giá trị mới.'),
    ('Dòng Trạng thái', 'Label', 'Read-only', 'Danh sách 5 giá trị', 'Theo dữ liệu',
     'Ghi bằng TÊN trạng thái, ví dụ “Chờ chi tiền → Hủy”.'),
    ('Dòng Ghi chú', 'Label', 'Read-only', '0–500 ký tự', 'Theo dữ liệu',
     'Ghi chú của người duyệt tại thao tác đó.'),
    ('Dòng Lý do hủy', 'Label', 'Read-only', '0–500 ký tự', 'Theo dữ liệu',
     'Hiển thị nổi bật ở mốc hủy phiếu.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Chưa có lịch sử thao tác nào.” khi phiếu chưa có mốc nào.'),
], required=False)

d.p('2.14.4 Danh sách event và xử lý event')
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
           'dưới đây chỉ liệt kê các quy tắc ĐẶC THÙ của màn Phiếu chi tiền.',
           anchor='list', head='Quy tắc áp dụng', lead='')
d.rule_table([
    ('BR-01', 'Hai luồng nghiệp vụ tách biệt theo Loại chi',
     ['– Sáu loại chi (Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, Chi thưởng '
      'thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển NCC) thuộc luồng LẬP TỪ ĐỀ '
      'NGHỊ THANH TOÁN, duyệt MỘT cấp (Thủ quỹ).',
      '– Loại Chi thu nhập cho nhân viên thuộc luồng LẬP TRỰC TIẾP, duyệt HAI cấp (Kế toán '
      'trưởng rồi Thủ quỹ).',
      '– Loại chi quyết định cấu trúc form: luồng thứ nhất có ô Số phiếu đề nghị, luồng thứ hai '
      'có ô Phòng ban chi và đặt Lý do chi thành bắt buộc.',
      '– Loại chi nằm ngoài 7 giá trị hợp lệ bị chặn ngay: giá trị lạ sẽ không rẽ được nhánh nào '
      'và có thể chiếm mất một phiếu đề nghị chưa dùng.'],
     ['Tạo mới phiếu chi', 'Sửa phiếu chi']),

    ('BR-02', 'Lưu nháp không bắt buộc trường nào ngoài Loại chi',
     ['– Đường LƯU NHÁP chỉ bắt buộc Loại chi; mọi ràng buộc bắt buộc khác chỉ áp khi GỬI DUYỆT.',
      '– Các rule về ĐỊNH DẠNG (kiểu số, tồn tại trong danh mục) vẫn áp ở cả hai đường — nới '
      'required là để lưu được form dở dang, không phải để ghi dữ liệu rác.',
      '– Đây là điểm KHÁC hệ thống cũ có chủ đích: hệ thống cũ áp cùng một bộ luật cho cả hai '
      'nút nên không cất được form đang làm dở.',
      '– Phiếu nháp được lưu với tài khoản “chưa chọn”; mở lại phiếu nháp đó vẫn sửa và lưu tiếp '
      'được bình thường.'],
     ['Tạo mới phiếu chi', 'Sửa phiếu chi']),

    ('BR-03', 'Loại chi nào bắt buộc có phiếu đề nghị',
     ['– CHỈ ba loại Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD mới bắt buộc '
      'có phiếu đề nghị thanh toán VÀ ít nhất một dòng chi tiết khi gửi duyệt.',
      '– Ba loại còn lại của luồng lập-từ-đề-nghị (Chi thưởng thực hiện hợp đồng, Chi khác, '
      'Thanh toán chi phí vận chuyển NCC) gửi duyệt được dù trống cả hai.',
      '– Đây là quyết định nghiệp vụ ĐÃ CHỐT, giữ đúng hệ thống cũ — KHÔNG phải sót kiểm tra, '
      'đừng siết lại ở lần soát sau.'],
     ['Tạo mới phiếu chi', 'Sửa phiếu chi']),

    ('BR-04', 'Phạm vi dữ liệu và các lớp bảo vệ',
     ['– Cấp quyền xem xét theo thứ tự ưu tiên V1 → V2; không có cấp nào thì chỉ thấy phiếu của '
      'chính mình.',
      '– Phiếu Đang tạo của người khác luôn bị loại khỏi danh sách và không mở được màn chi tiết.',
      '– Người đã duyệt một phiếu luôn mở lại được phiếu đó; người có quyền duyệt luôn mở được '
      'phiếu cùng công ty đang chờ đúng cấp mình.',
      '– Hai vế công ty cùng rỗng KHÔNG được coi là cùng công ty (lỗ hổng của hệ thống cũ đã '
      'được bịt).'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xem chi tiết']),

    ('BR-05', 'Điều kiện Sửa và Xóa',
     ['– Phải thoả ĐỦ BA: phiếu ở trạng thái Đang tạo; người thao tác là NGƯỜI LẬP phiếu; người '
      'đó có quyền Kế toán thanh toán.',
      '– Quản trị hệ thống CỐ Ý không được miễn trừ ở đây — miễn trừ chỉ áp cho việc XEM.',
      '– Đây là điểm SIẾT CHẶT HƠN hệ thống cũ: hệ thống cũ chỉ kiểm trạng thái nên bất kỳ ai '
      'gọi được đường dẫn đều sửa hoặc xoá được phiếu nháp của người khác.',
      '– Xóa phiếu xoá kèm toàn bộ dòng chi tiết trong một giao dịch; không khôi phục lại được.'],
     ['Sửa phiếu chi', 'Xóa phiếu chi']),

    ('BR-06', 'Một phiếu đề nghị chỉ lập được một phiếu chi',
     ['– Cửa sổ chọn phiếu đề nghị chỉ liệt kê phiếu đang ở trạng thái Chờ tạo phiếu chi VÀ chưa '
      'có phiếu chi nào — kể cả phiếu chi mới chỉ là nháp.',
      '– Khi lưu, hệ thống KHÓA DÒNG phiếu đề nghị rồi mới kiểm tra, nên hai người bấm lưu cùng '
      'lúc vẫn chỉ tạo được một phiếu chi.',
      '– Khi sửa, ràng buộc vẫn được kiểm nhưng bỏ qua chính phiếu đang sửa.',
      '– Xoá phiếu chi nháp thì phiếu đề nghị trở lại danh sách chọn được.'],
     ['Tạo mới phiếu chi', 'Sửa phiếu chi', 'Xóa phiếu chi']),

    ('BR-07', 'Hệ thống tự nhận cấp duyệt theo trạng thái',
     ['– Giao diện chỉ có MỘT nút Duyệt phiếu chi và MỘT endpoint duyệt; nơi gọi không phải '
      'truyền cấp vào.',
      '– Trạng thái Chờ KT trưởng duyệt → cần quyền Kế toán trưởng duyệt phiếu chi.',
      '– Trạng thái Chờ chi tiền → cần quyền Thủ quỹ duyệt phiếu chi.',
      '– Cả hai cấp đều bắt buộc CÙNG CÔNG TY với phiếu.',
      '– Trạng thái khác hai giá trị trên (nháp, đã duyệt, đã hủy) thì không có gì để duyệt, nút '
      'bị ẩn.',
      '– Điều kiện Hủy đúng bằng điều kiện Duyệt.'],
     ['Xem chi tiết', 'Duyệt phiếu chi', 'Hủy phiếu chi']),

    ('BR-08', 'Ghi bút toán vào sổ kế toán',
     ['– Bước THỦ QUỸ duyệt là THỜI ĐIỂM DUY NHẤT hệ thống ghi bút toán; mọi thao tác khác (lưu, '
      'sửa, xoá, hủy, Kế toán trưởng duyệt) không ghi gì vào sổ kế toán.',
      '– Bước Kế toán trưởng CỐ Ý chưa ghi sổ: tiền chưa ra khỏi quỹ, và nếu ghi ngay thì phiếu '
      'bị Thủ quỹ từ chối vẫn để lại bút toán trong sổ dùng chung.',
      '– Luồng Chi thu nhập nhân viên ghi sổ theo cơ chế GỘP, khác luồng còn lại ghi thẳng từng '
      'dòng.',
      '– Toàn bộ bước duyệt nằm trong MỘT giao dịch: ghi sổ hỏng thì phiếu quay về trạng thái '
      'cũ, không được để phiếu “Đã duyệt” mà sổ cái trống. Hệ thống cũ đẩy phần ghi sổ của luồng '
      'thứ hai ra ngoài giao dịch nên không có bảo đảm này.',
      '– Thao tác này KHÔNG hoàn tác được; hệ thống không có chức năng gỡ bút toán hay bỏ duyệt.'],
     ['Duyệt phiếu chi']),

    ('BR-09', 'Chặn duyệt lại và chặn tạo trùng',
     ['– Trước khi duyệt hoặc hủy, hệ thống KHÓA DÒNG phiếu rồi mới đọc lại trạng thái.',
      '– Chốt “đã duyệt” được kiểm TRƯỚC chốt quyền: người vừa duyệt xong bấm lại sẽ nhận thông '
      'báo “Phiếu chi đã được duyệt trước đó.” chứ không phải thông báo thiếu quyền — hai nguyên '
      'nhân được tách rõ.',
      '– Nhờ vậy hai người duyệt cùng lúc không thể ghi trùng bút toán. Hệ thống cũ không khóa '
      'dòng nên duyệt hai lần là nhân đôi bút toán trong sổ kế toán thật.',
      '– Sinh mã phiếu cũng dùng khóa dòng để hai người lưu cùng lúc không ra trùng mã.',
      '– Giao diện chống bấm nhiều lần bằng cách khoá nút trong lúc xử lý, nhưng chốt chặn thật '
      'nằm ở phía máy chủ.'],
     ['Tạo mới phiếu chi', 'Duyệt phiếu chi', 'Hủy phiếu chi']),

    ('BR-10', 'Trần số tiền chi',
     ['– Số tiền chi của một dòng KHÔNG được lớn hơn số tiền đề nghị chi của chính dòng đó.',
      '– Luật này được kiểm ở HAI thời điểm bằng CÙNG một hàm: lúc lập/sửa phiếu và lúc duyệt. '
      'Viết luật ở hai nơi khác nhau sẽ dẫn tới lưu được nhưng bị chặn ở bước duyệt (hoặc ngược '
      'lại, nguy hiểm hơn).',
      '– Với luồng Chi thu nhập nhân viên, trần so theo GIÁ TRỊ TUYỆT ĐỐI của số dư vì cột số dư '
      'là số có dấu; so trực tiếp sẽ chặn oan mọi dòng có số dư âm.',
      '– Hệ thống cũ KHÔNG hề kiểm trần lúc duyệt do điều kiện kiểm tra bị viết sai nhánh — đây '
      'là lỗi đã được sửa.',
      '– Sáu khoản thu nhập của luồng Chi thu nhập nhân viên CHO PHÉP số âm (truy thu) nên không '
      'áp ràng buộc không-âm.'],
     ['Tạo mới phiếu chi', 'Sửa phiếu chi', 'Duyệt phiếu chi']),

    ('BR-11', 'Đồng bộ ngược sang Đề nghị thanh toán',
     ['– Phiếu chi chuyển sang trạng thái chờ duyệt: phiếu đề nghị được cập nhật trạng thái '
      'tương ứng.',
      '– Thủ quỹ duyệt: phiếu đề nghị chuyển sang trạng thái duyệt phiếu chi và được đẩy số '
      'duyệt chi xuống từng dòng tương ứng.',
      '– Việc khớp dòng phiếu chi với dòng phiếu đề nghị dựa trên bộ khóa nhiều trường, không '
      'chỉ dựa trên thứ tự dòng.'],
     ['Tạo mới phiếu chi', 'Sửa phiếu chi', 'Duyệt phiếu chi']),

    ('BR-12', 'Thông báo đi đúng cấp đang chờ',
     ['– Phiếu chuyển sang Chờ KT trưởng duyệt → thông báo gửi cho người có quyền Kế toán trưởng '
      'cùng công ty; Thủ quỹ CHƯA nhận.',
      '– Phiếu chuyển sang Chờ chi tiền → thông báo gửi cho người có quyền Thủ quỹ cùng công ty.',
      '– Thủ quỹ duyệt xong → thông báo gửi cho người lập phiếu.',
      '– Lưu nháp KHÔNG gửi thông báo cho ai.',
      '– Lỗi gửi thông báo KHÔNG được làm hỏng thao tác nghiệp vụ đã thực hiện.'],
     ['Tạo mới phiếu chi', 'Sửa phiếu chi', 'Duyệt phiếu chi']),

    ('BR-13', 'Lý do hủy và Ghi chú của người duyệt',
     ['– Lý do hủy là BẮT BUỘC khi hủy phiếu; Ghi chú là tuỳ chọn. Cả hai tối đa 500 ký tự.',
      '– Cả hai KHÔNG được lưu lên phiếu mà lưu vào LỊCH SỬ THAY ĐỔI, vì bảng phiếu dùng chung '
      'với hệ thống cũ không có cột tương ứng và feature này không migration.',
      '– Màn chi tiết của phiếu đã hủy hiện lại hai nội dung này ở dải băng đầu màn, để không '
      'phải mở Lịch sử mới biết vì sao phiếu bị hủy.',
      '– Hệ thống cũ có ô Ghi chú ở màn duyệt nhưng chữ gõ vào bị mất — đây là lỗi đã được sửa.',
      '– Người lập CỐ Ý không được tự hủy phiếu đã gửi duyệt.'],
     ['Hủy phiếu chi', 'Duyệt phiếu chi', 'Xem chi tiết']),

    ('BR-14', 'Sinh mã phiếu và ghi cấp tổ chức',
     ['– Mã phiếu sinh tự động dạng “{mã công ty}.PC{tháng năm}.{5 chữ số}”; người dùng không '
      'nhập được và mã đã dùng không được cấp lại.',
      '– Sinh mã có khóa dòng; hệ thống cũ không khóa nên hai phiếu tạo cùng lúc sinh trùng mã '
      'và một phiếu chết vì mã là duy nhất.',
      '– Công ty, phòng ban và bộ phận của phiếu lấy theo hồ sơ của NGƯỜI LẬP tại thời điểm tạo, '
      'gán đè vô điều kiện, không nhận giá trị do phía giao diện gửi lên.'],
     ['Tạo mới phiếu chi']),

    ('BR-15', 'Danh sách tài khoản cho hai ô chọn',
     ['– Chỉ liệt kê tài khoản đang hoạt động VÀ là tài khoản cấp cuối; tài khoản tổng hợp bị '
      'loại vì không được hạch toán trực tiếp.',
      '– Ngoại lệ: phiếu đang gắn tài khoản đã bị khóa thì tài khoản đó vẫn được trả kèm để '
      'select hiện đúng tên, tránh việc người dùng vô tình lưu đè mất giá trị cũ.'],
     ['Tạo mới phiếu chi', 'Sửa phiếu chi', 'Xem chi tiết']),

    ('BR-16', 'Bản in theo loại chi',
     ['– Bản in luôn gồm ĐỦ 2 LIÊN, mỗi liên có ảnh tiêu đề thư của công ty và 5 ô ký.',
      '– Phiếu loại Chi thu nhập cho nhân viên dùng mẫu riêng, có THÊM hai bảng kê ở cuối: bảng '
      'kê chi tiết số tiền chi và bảng kê chi tiết theo vụ việc (6 khoản thu nhập).',
      '– In phiếu và xuất Excel chỉ cần quyền XEM phiếu, không gắn quyền riêng.',
      '– Màn hình KHÔNG có chức năng xuất Excel cả danh sách; mỗi lần chỉ xuất được một phiếu.'],
     ['In phiếu chi', 'Xuất Excel']),

    ('BR-17', 'Ghi lịch sử',
     ['– Ghi một dòng lịch sử khi: tạo mới, chỉnh sửa, gửi duyệt, mỗi cấp duyệt, hủy và xoá '
      'phiếu.',
      '– Đổi trạng thái luôn là một dòng lịch sử RIÊNG, tách khỏi dòng thay đổi thông tin, và '
      'ghi bằng TÊN trạng thái.',
      '– Bước Thủ quỹ duyệt ghi thêm một dòng đối soát riêng (mã phiếu, số dòng sổ cái, tổng '
      'tiền) để tra lại về sau.',
      '– Xem lịch sử không cần quyền riêng; ai nhìn thấy phiếu thì xem được lịch sử của phiếu đó.'],
     ['Tạo mới phiếu chi', 'Sửa phiếu chi', 'Duyệt phiếu chi', 'Hủy phiếu chi', 'Xóa phiếu chi',
      'Xem lịch sử']),
])

d.save()
d.selfcheck()
