# -*- coding: utf-8 -*-
"""Sinh SRS man "Phieu uy nhiem chi" (phan he Tai chinh) theo FORM CHUAN 2026-08-28.

Nguon: doc code 04/09/2026 tren nhanh gop_db (BE Modules/Finance + FE
hrm-client/pages/finance/bill-payment-authorizations) + anh that unc_shots/.

Chay:  python .plans/gop-db/finance-bill-payment-authorization/gen_srs.py
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

SHOTS = os.path.join(HERE, 'unc_shots')
OUT = os.path.join(HERE, 'SRS - Phiếu ủy nhiệm chi.docx')

ACTOR_KT = 'Kế toán thanh toán'
ACTOR_XEM = 'Người có quyền xem phiếu ủy nhiệm chi'


def shot(name):
    return os.path.join(SHOTS, name)


MENU = 'Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt => Phiếu ủy nhiệm chi'

d = SrsDoc(out=OUT, menu=MENU,
           route='/finance/bill-payment-authorizations',
           full_url='https://hrm-crm.eteksofts.com/finance/bill-payment-authorizations',
           img_prefix='unc_')

# ============================================================== TRANG DAU
d.title_block('Phiếu ủy nhiệm chi')

d.h2('Mục lục')
d.toc()

# ========================================================= PHAN 1. GIOI THIEU
d.h1('Phần 1. Giới thiệu')

d.h2('1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Phiếu ủy nhiệm chi (phân hệ Tài chính), '
    'nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và phạm vi dữ liệu của màn hình.',
    'Làm rõ hai luồng lập phiếu khác hẳn nhau: lập TỪ Phiếu đề nghị thanh toán (6 loại chi) và '
    'lập TRỰC TIẾP cho loại chi “Chi thu nhập cho nhân viên”.',
    'Làm rõ ranh giới giữa hai đường lưu: “Lưu nháp” (chỉ bắt buộc Loại chi, không đụng sổ kế '
    'toán) và “Lưu và duyệt” (ghi bút toán vào sổ kế toán ngay, phiếu khoá vĩnh viễn).',
    'Ghi lại các quy tắc CỐ Ý giữ nguyên theo hệ thống ERP cũ để tránh bị sửa nhầm thành “lỗi” '
    'trong các đợt bảo trì sau (xem Phần 4).',
])

d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu ủy nhiệm chi (UNC)',
     'Chứng từ kế toán ghi nhận khoản tiền doanh nghiệp chi ra bằng hình thức CHUYỂN KHOẢN.'),
    ('Phiếu đề nghị thanh toán',
     'Chứng từ đề nghị chi tiền do bộ phận nghiệp vụ lập. Phiếu ủy nhiệm chi được lập từ phiếu '
     'này khi phiếu đề nghị đang ở trạng thái “Chờ tạo phiếu chi” và có hình thức thanh toán là '
     'chuyển khoản.'),
    ('Phiếu chi tiền',
     'Màn hình song sinh của Phiếu ủy nhiệm chi, lấy các phiếu đề nghị thanh toán bằng TIỀN MẶT. '
     'Hai màn không bao giờ nhận cùng một phiếu đề nghị.'),
    ('Đang tạo', 'Phiếu nháp, chỉ người lập nhìn thấy, sửa và xóa được.'),
    ('Đã hạch toán',
     'Phiếu đã ghi bút toán vào sổ kế toán. Không sửa, không xóa được nữa.'),
    ('Lưu và duyệt',
     'Thao tác chuyển phiếu từ “Đang tạo” sang “Đã hạch toán”. Màn hình KHÔNG có bước gửi duyệt '
     'hay duyệt riêng: người lập được phiếu là người duyệt.'),
    ('Tài khoản có / Tài khoản nợ',
     'Cặp tài khoản kế toán dùng để ghi bút toán. Tài khoản có là tài khoản tiền bị trừ, tài '
     'khoản nợ là tài khoản công nợ được tất toán.'),
    ('Số tiền đề nghị chi / Số tiền duyệt chi',
     'Số tiền bộ phận nghiệp vụ đề nghị và số tiền kế toán chốt chi. Số duyệt chi không được lớn '
     'hơn số đề nghị chi.'),
    ('Chi thu nhập cho nhân viên',
     'Loại chi lập trực tiếp, không qua phiếu đề nghị. Hệ thống tự lấy số thu nhập còn phải trả '
     'của từng nhân viên trong một phòng ban từ sổ kế toán.'),
], widths=[1.8, 4.2])

# ========================================================= PHAN 2. PHAN QUYEN
d.h1('Phần 2. Phân quyền')

d.h2('1 Danh sách quyền')

d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán thanh toán',
     'Lập, sửa, xóa phiếu; mở được cửa sổ Chọn phiếu đề nghị chi; lấy được số liệu thu nhập '
     'nhân viên theo phòng ban. Đây là quyền dùng chung của nhiều màn phân hệ Tài chính, không '
     'phải quyền riêng của màn này.'),
], widths=[0.8, 2.0, 3.2])

d.p('Màn hình KHÔNG có quyền duyệt riêng: người có quyền Q1 bấm “Lưu và duyệt” là phiếu vào sổ '
    'kế toán ngay. Màn hình cũng không có chức năng In và Xuất Excel nên không có quyền tương ứng.')

d.p('Nhóm quyền quyết định phạm vi dữ liệu '
    '(xét theo thứ tự ưu tiên từ trên xuống, cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả phiếu ủy nhiệm chi của tổng công ty',
     'Toàn bộ phiếu ủy nhiệm chi của mọi công ty.'),
    ('V2', 'Xem tất cả phiếu ủy nhiệm chi của công ty',
     'Phiếu thuộc công ty của người đăng nhập, cộng thêm phiếu do chính mình lập và phiếu do '
     'chính mình duyệt ở công ty khác.'),
    ('—', '(không có cấp nào)',
     'Chỉ phiếu do chính mình lập hoặc chính mình duyệt.'),
], widths=[0.8, 2.0, 3.2])

d.p('Ràng buộc phủ lên MỌI cấp quyền ở trên: phiếu ở trạng thái “Đang tạo” chỉ người lập nhìn '
    'thấy. Người quản trị hệ thống và người có quyền V1 cũng không nhìn thấy phiếu nháp của '
    'người khác.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1', 'V2', 'Không có quyền nào'], [
    ('FR-01 Truy cập & xem danh sách', '✅ (theo cấp xem)', '✅ (mọi công ty)',
     '✅ (công ty mình)', '✅ (chỉ phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc & tuỳ chỉnh cột', '✅', '✅', '✅', '✅'),
    ('FR-04 Tạo mới phiếu (lập từ phiếu đề nghị)', '✅', '❌', '❌', '❌'),
    ('FR-05 Chọn phiếu đề nghị chi', '✅', '❌', '❌', '❌'),
    ('FR-06 Tạo mới phiếu Chi thu nhập cho nhân viên', '✅', '❌', '❌', '❌'),
    ('FR-07 Chỉnh sửa phiếu', '✅ (phiếu nháp của chính mình)', '❌', '❌', '❌'),
    ('FR-08 Lưu và duyệt', '✅', '❌', '❌', '❌'),
    ('FR-09 Xem chi tiết phiếu', '✅', '✅', '✅ (cùng công ty)', '✅ (phiếu của mình)'),
    ('FR-10 Xóa phiếu', '✅ (phiếu nháp của chính mình)', '❌', '❌', '❌'),
    ('FR-11 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅'),
], widths=[2.4, 1.3, 1.0, 1.0, 1.3])

# ================================================ PHAN 3. DAC TA CHI TIET
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')

d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(ACTOR_KT, [0, 1, 2, 3]),
     (ACTOR_XEM, [0, 3])],
    [('FR-01', 'Xem danh sách', 'view'),
     ('FR-04', 'Tạo mới phiếu', 'crud'),
     ('FR-07', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-09', 'Xem chi tiết phiếu', 'view')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view', 'extend', [0], None),
     ('FR-05', 'Chọn phiếu đề nghị chi', 'crud', 'include', [1, 2], None),
     ('FR-06', 'Lấy thu nhập nhân viên', 'crud', 'include', [1, 2], None),
     ('FR-08', 'Lưu và duyệt', 'action', 'extend', [1, 2], None),
     ('FR-10', 'Xóa phiếu', 'action', 'extend', [0, 3], None),
     ('FR-11', 'Xem lịch sử thay đổi', 'view', 'extend', [0, 3], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu ủy nhiệm chi')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------ 2.1 Xem danh sach
d.h3('2.1 Xem danh sách phiếu ủy nhiệm chi')

d.p('2.1.1 Giới thiệu')
d.rule_ref('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu ủy nhiệm chi tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Truy cập và xem danh sách phiếu ủy nhiệm chi',
    mota='Hiển thị bảng phiếu ủy nhiệm chi nằm trong phạm vi dữ liệu của người đăng nhập, kèm '
         'phân trang và ô thống kê tổng số bản ghi khớp bộ lọc. Chỉ có một mục menu trỏ vào màn '
         'này; mọi người dùng đều vào cùng một danh sách, khác nhau ở phạm vi dữ liệu.',
    tacnhan='Kế toán thanh toán; Người có quyền xem phiếu ủy nhiệm chi; Người dùng đã đăng nhập',
    dieukien='Người dùng đã đăng nhập và vào được phân hệ Tài chính.',
    chinh='1. Người dùng vào menu Tài chính → Quản lý tiền → Thanh toán tiền mặt → Phiếu ủy '
          'nhiệm chi.\n'
          '2. Hệ thống xác định phạm vi dữ liệu theo cấp quyền xem của người dùng.\n'
          '3. Hệ thống loại bỏ phiếu ở trạng thái “Đang tạo” không do người dùng lập.\n'
          '4. Hệ thống trả về trang đầu tiên (10 dòng) sắp xếp theo Ngày tạo giảm dần và tổng số '
          'bản ghi.\n'
          '5. Bảng hiển thị dữ liệu, ô “Hiển thị a–b / N” hiển thị đúng khoảng và tổng.',
    phu='• Không có bản ghi nào trong phạm vi → bảng hiện “Không có dữ liệu phù hợp bộ lọc.” và '
        'dòng thống kê hiện “Không có phiếu nào.”.\n'
        '• Đang nạp dữ liệu → bảng hiện “Đang tải dữ liệu...”.\n'
        '• Không xác định được đơn vị của người đăng nhập → chỉ hiển thị phiếu do chính người đó '
        'lập hoặc duyệt.\n'
        '• Phiên đăng nhập hết hạn → điều hướng về màn đăng nhập.',
    dacbiet=None)

d.p('2.1.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('01-danh-sach.png'),
         shot_caption='Màn Danh sách phiếu ủy nhiệm chi lúc mới truy cập')

d.p('2.1.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Danh sách phiếu ủy nhiệm chi',
     'Hiển thị ở thanh trên cùng và ở đầu khối danh sách.'),
    ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
     'Luôn hiển thị với mọi người vào được màn. Việc chặn quyền lập phiếu thực hiện ở bước lưu.'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Mở cửa sổ “Tuỳ chỉnh cột”.'),
    ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Số thứ tự theo trang',
     'Cột bắt buộc, không ẩn và không đổi vị trí được.'),
    ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'Dạng <mã công ty>.UNC<tháng năm>.<5 chữ số>',
     'Theo dữ liệu',
     'Cột bắt buộc. Là liên kết mở màn chi tiết trong cùng thẻ. Sắp xếp được.'),
    ('Cột Mã phiếu đề nghị chi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Liên kết mở màn chi tiết Phiếu đề nghị thanh toán ở thẻ mới. Phiếu Chi thu nhập cho nhân '
     'viên hiển thị dấu gạch ngang.'),
    ('Cột Loại chi', 'Table/Grid', 'Read-only', '7 giá trị', 'Theo dữ liệu',
     'Lấy theo loại chi của phiếu đề nghị nguồn; phiếu không có đề nghị thì lấy theo phiếu.'),
    ('Cột Người đề nghị', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Người lập PHIẾU ĐỀ NGHỊ, khác cột Người tạo.'),
    ('Cột Ngày tạo / Người tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
     'Ngày tạo sắp xếp được và là cột sắp xếp mặc định (giảm dần).'),
    ('Cột Ngày cập nhật / Người cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm',
     'Theo dữ liệu', 'Ngày cập nhật sắp xếp được.'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Đang tạo / Đã hạch toán', 'Theo dữ liệu',
     'Đã hạch toán hiển thị nhãn xanh lá, Đang tạo hiển thị nhãn xám. Sắp xếp được.'),
    ('Cột Số tiền duyệt chi', 'Table/Grid', 'Read-only', '≥ 0', 'Ẩn mặc định',
     'Tổng số tiền duyệt chi đã quy đổi của mọi dòng chi tiết. Bật trong Tuỳ chỉnh cột. Sắp xếp '
     'được.'),
    ('Cột Ngày hạch toán', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Ẩn mặc định',
     'Bật trong Tuỳ chỉnh cột. Sắp xếp được.'),
    ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
     'Cột bắt buộc. Chứa tối đa 3 nút: Sửa, Xóa, Lịch sử.'),
    ('Nút Sửa trên dòng', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện khi phiếu đang ở trạng thái Đang tạo, do chính người đăng nhập lập và người đó có '
     'quyền Kế toán thanh toán.'),
    ('Nút Xóa trên dòng', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Cùng điều kiện với nút Sửa.'),
    ('Nút Lịch sử trên dòng', 'Icon Button', 'Enable', '–', 'Hiển thị',
     'Luôn hiển thị với mọi dòng, kể cả phiếu đã hạch toán.'),
    ('Ô “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
     'N là tổng số phiếu khớp bộ lọc và khớp phạm vi quyền, không phải tổng toàn hệ thống.'),
    ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, 10 dòng',
     'Có nút về đầu / lùi / số trang / tiến / về cuối và ô chọn số dòng mỗi trang.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi N bằng 0.'),
    ('Vòng quay chờ', 'Loading', 'Hiển thị', '–', 'Ẩn',
     'Hiện “Đang tải dữ liệu...” trong lúc nạp.'),
], required=False)

d.p('2.1.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn hình', 'System',
     'Before:\n– Xác định cấp quyền xem của người dùng theo thứ tự ưu tiên V1 → V2 → không cấp '
     'nào.\n'
     'During:\n– Áp phạm vi dữ liệu theo cấp quyền.\n'
     '– Loại bỏ mọi phiếu ở trạng thái Đang tạo không do người đăng nhập lập.\n'
     'After:\n– Trả về trang 1 sắp xếp theo Ngày tạo giảm dần, kèm tổng số bản ghi; hiển thị '
     'bảng và ô thống kê.'),
    ('Bấm tiêu đề cột có mũi tên sắp xếp', 'Click',
     'Before:\n– Giữ nguyên bộ lọc đang áp dụng.\n'
     'During:\n– Chỉ nhận sắp xếp trên 6 cột: Mã phiếu, Ngày tạo, Ngày cập nhật, Trạng thái, '
     'Ngày hạch toán, Số tiền duyệt chi. Cột khác bị bỏ qua.\n'
     'After:\n– Nạp lại danh sách theo thứ tự mới trên toàn bộ dữ liệu và quay về trang 1.'),
    ('Bấm số trang / nút tiến lùi', 'Click',
     'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp dụng.\n'
     'After:\n– Nạp lại dữ liệu trang mới, cập nhật ô “Hiển thị a–b / N”.'),
    ('Bấm mã phiếu', 'Click',
     'After:\n– Mở màn Chi tiết phiếu ủy nhiệm chi trong cùng thẻ trình duyệt.'),
    ('Bấm mã phiếu đề nghị chi', 'Click',
     'After:\n– Mở màn Chi tiết Phiếu đề nghị thanh toán ở thẻ trình duyệt mới.'),
])

# ------------------------------------------------------ 2.2 Tim kiem va loc
d.h3('2.2 Tìm kiếm và lọc')

d.p('2.2.1 Giới thiệu')
d.rule_ref('- Màn Danh sách và Tìm kiếm, lọc dữ liệu. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu ủy nhiệm chi tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Tìm kiếm và lọc danh sách phiếu ủy nhiệm chi',
    mota='Thu hẹp danh sách theo mã phiếu, mã phiếu đề nghị, loại chi, trạng thái, người lập, '
         'người đề nghị, đơn vị và khoảng ngày lập. Mọi điều kiện được cộng dồn với nhau và '
         'luôn nằm trong phạm vi quyền xem của người dùng.',
    tacnhan='Kế toán thanh toán; Người có quyền xem phiếu ủy nhiệm chi',
    dieukien='Đang ở màn Danh sách phiếu ủy nhiệm chi.',
    chinh='1. Người dùng bấm “Tìm kiếm nâng cao” để mở khối bộ lọc.\n'
          '2. Người dùng chọn hoặc nhập điều kiện.\n'
          '3. Ô dạng chọn và ô ngày: hệ thống lọc lại ngay khi chọn. Ô gõ tay: người dùng bấm '
          '“Tìm kiếm” hoặc nhấn Enter.\n'
          '4. Hệ thống áp dụng đồng thời mọi điều kiện, quay về trang 1 và cập nhật tổng bản ghi.',
    phu='• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
        '• Bấm “Làm mới” → xoá toàn bộ điều kiện, quay về danh sách đầy đủ trong phạm vi quyền.\n'
        '• Rời màn rồi quay lại trong vòng 10 phút → hệ thống ghi nhớ và khôi phục bộ lọc.\n'
        '• Khoảng ngày đảo ngược (từ lớn hơn đến) → kết quả rỗng, không báo lỗi.',
    dacbiet=None)

d.p('2.2.2 Layout màn hình')
d.layout(menu=MENU,
         shot=shot('03-loc-nang-cao.png'),
         shot_caption='Khối “Tìm kiếm nâng cao” đang mở với đầy đủ 11 ô lọc')

d.p('2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Ô tìm nhanh theo mã phiếu', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Không', 'Trống',
     'Gợi ý “Tìm theo mã phiếu ủy nhiệm chi...”. Tìm theo một phần của mã. Không tự tìm khi đang '
     'gõ; phải bấm Tìm kiếm hoặc nhấn Enter.'),
    ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp dụng toàn bộ điều kiện.'),
    ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Xoá mọi điều kiện lọc và tải lại danh sách.'),
    ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở khối lọc chi tiết; khi mở đổi chữ thành “Ẩn tìm kiếm nâng cao”. Mặc định thu gọn.'),
    ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Mở cửa sổ bật tắt và sắp xếp các ô lọc.'),
    ('Mã phiếu', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Không', 'Trống',
     'Độc lập với ô tìm nhanh; điền cả hai thì hai điều kiện cộng dồn.'),
    ('Mã phiếu đề nghị chi', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Không', 'Trống',
     'Tìm theo một phần mã phiếu đề nghị nguồn.'),
    ('Loại chi', 'Dropdown', 'Enable', 'Danh sách 6 giá trị', 'Không', 'Trống',
     'Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, Chi thưởng thực hiện hợp '
     'đồng, Chi khác, Thanh toán chi phí vận chuyển NCC. CỐ Ý không có “Chi thu nhập cho nhân '
     'viên”.'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
     'Chỉ “Đang tạo” và “Đã hạch toán”.'),
    ('Người lập', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập phiếu ủy nhiệm chi.'),
    ('Người đề nghị', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
     'Lọc theo người lập PHIẾU ĐỀ NGHỊ.'),
    ('Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống',
     'Lọc theo đơn vị ghi trên phiếu.'),
    ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống', '–'),
    ('Bộ phận', 'Dropdown', 'Enable', 'Danh sách bộ phận', 'Không', 'Trống', '–'),
    ('Ngày lập từ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc theo NGÀY TẠO PHIẾU, lấy cả ngày đầu mút.'),
    ('Ngày lập đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
     'Lọc theo NGÀY TẠO PHIẾU, lấy cả ngày đầu mút.'),
])

d.p('2.2.4 Danh sách event và xử lý event')
d.event_table([
    ('Chọn giá trị ở ô dạng chọn hoặc ô ngày', 'Change',
     'After:\n– Áp dụng ngay điều kiện mới, quay về trang 1 và cập nhật tổng bản ghi.'),
    ('Nhấn Enter hoặc bấm Tìm kiếm ở ô gõ tay', 'Keypress',
     'During:\n– Gom toàn bộ điều kiện đang có (kể cả ô dạng chọn) thành một bộ điều kiện.\n'
     'After:\n– Nạp lại danh sách, quay về trang 1.'),
    ('Bấm Làm mới', 'Click',
     'After:\n– Xoá mọi điều kiện lọc và ô tìm nhanh, tải lại danh sách đầy đủ trong phạm vi '
     'quyền, quay về trang 1.'),
    ('Rời màn rồi quay lại', 'System',
     'During:\n– Hệ thống ghi nhớ bộ lọc trong 10 phút và chỉ khi người dùng còn ở trong màn '
     'Phiếu ủy nhiệm chi.\n'
     'After:\n– Khôi phục lại đúng bộ lọc trước đó.'),
])

# --------------------------------- 2.3 Cai dat bo loc & tuy chinh cot
d.h3('2.3 Cài đặt bộ lọc và Tuỳ chỉnh cột')

d.p('2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cài đặt bộ lọc, tuỳ chỉnh cột', 'view',
            [('include', 'Ghi nhớ cấu hình theo người dùng')],
            actor=ACTOR_XEM,
            caption='Biểu đồ Use Case — FR-03 Cài đặt bộ lọc và Tuỳ chỉnh cột')

d.p('2.3.2 Giới thiệu')
d.rule_ref('- Cấu hình cột và Cài đặt bộ lọc. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu ủy nhiệm chi tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Cài đặt bộ lọc và tuỳ chỉnh cột hiển thị',
    mota='Cho phép người dùng chọn ô lọc nào hiển thị, cột nào hiển thị và thứ tự của chúng. '
         'Cấu hình được ghi nhớ riêng cho từng người dùng.',
    tacnhan='Kế toán thanh toán; Người có quyền xem phiếu ủy nhiệm chi',
    dieukien='Đang ở màn Danh sách phiếu ủy nhiệm chi.',
    chinh='1. Người dùng bấm “Cài đặt bộ lọc” hoặc nút biểu tượng cột.\n'
          '2. Hệ thống mở cửa sổ tương ứng với danh sách mục kèm ô tích và tay nắm kéo.\n'
          '3. Người dùng bật tắt hoặc kéo đổi thứ tự.\n'
          '4. Người dùng bấm Lưu.\n'
          '5. Hệ thống ghi nhớ cấu hình cho người dùng đó và áp dụng ngay lên màn.',
    phu='• Bấm “Khôi phục mặc định” ở cửa sổ Cài đặt bộ lọc → đưa về đủ 10 mục lọc mặc định.\n'
        '• Bấm “Đóng” → giữ nguyên cấu hình cũ.\n'
        '• Cột bắt buộc (STT, Mã phiếu, Hành động) → không bỏ tích và không kéo được.',
    dacbiet='Cấu hình được ghi nhớ theo từng người dùng, không ảnh hưởng người khác.')

d.p('2.3.3 Layout màn hình')
d.layout(menu=MENU + ' => Cài đặt bộ lọc / Tuỳ chỉnh cột',
         shot=shot('05-cau-hinh-cot.png'),
         shot_caption='Cửa sổ “Tuỳ chỉnh cột” — cột bắt buộc có biểu tượng ổ khoá')

d.p('2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc” / “Tuỳ chỉnh cột”',
     'Hai cửa sổ riêng biệt.'),
    ('Danh sách mục lọc', 'Modal', 'Enable', '10 mục', 'Không', 'Tất cả đang bật',
     'Mã phiếu, Mã phiếu đề nghị chi, Loại chi, Trạng thái, Người lập, Người đề nghị, Công ty, '
     'Phòng ban, Bộ phận, Khoảng ngày lập.'),
    ('Danh sách cột', 'Modal', 'Enable', '13 cột', 'Không',
     '11 cột bật, 2 cột tắt',
     'Số tiền duyệt chi và Ngày hạch toán mặc định tắt.'),
    ('Ô tích của cột bắt buộc', 'Icon Button', 'Disable', '–', '–', 'Luôn bật',
     'Hiện biểu tượng ổ khoá kèm chú thích “Cột bắt buộc — không thể ẩn hoặc đổi vị trí”.'),
    ('Tay nắm kéo', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
     'Kéo thả để đổi thứ tự; không có ở mục bị khoá.'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi nhớ cấu hình và đóng cửa sổ.'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Chỉ có ở cửa sổ Cài đặt bộ lọc.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không lưu thay đổi.'),
])

d.p('2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Bỏ tích một mục', 'Click',
     'During:\n– Nếu mục thuộc nhóm bắt buộc → không cho bỏ tích và hiển thị chú thích giải '
     'thích.\n'
     'After:\n– Mục được đánh dấu tắt trong cửa sổ, chưa áp dụng lên màn.'),
    ('Kéo đổi thứ tự', 'Click',
     'During:\n– Mục bị khoá không nhận thao tác kéo.\n'
     'After:\n– Cập nhật thứ tự tạm trong cửa sổ.'),
    ('Bấm Lưu', 'Click',
     'After:\n– Ghi nhớ cấu hình cho riêng người dùng, áp dụng ngay lên bộ lọc hoặc lưới và '
     'đóng cửa sổ.\n– Cấu hình vẫn còn sau khi tải lại trang hoặc đăng nhập lại.'),
])

# ------------------------------------- 2.4 Tao moi (lap tu phieu de nghi)
d.h3('2.4 Tạo mới phiếu ủy nhiệm chi (lập từ phiếu đề nghị)')

d.p('2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Tạo mới phiếu ủy nhiệm chi', 'crud',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Chọn phiếu đề nghị chi'),
             ('include', 'Sinh mã phiếu tự động'),
             ('extend', 'Lưu và duyệt')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-04 Tạo mới phiếu ủy nhiệm chi')

d.p('2.4.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='create')
d.intro_table(
    ten='Tạo mới phiếu ủy nhiệm chi lập từ phiếu đề nghị thanh toán',
    mota='Lập phiếu chi chuyển khoản cho 6 loại chi: Chi trả nhà cung cấp, Chi trả lại khách '
         'hàng, Chi thưởng NVKD, Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận '
         'chuyển NCC. Kế toán chọn phiếu đề nghị, hệ thống kéo toàn bộ thông tin và dòng chi '
         'tiết về; kế toán chốt số tiền duyệt chi và khai tài khoản chuyển tiền.',
    tacnhan='Kế toán thanh toán',
    dieukien='Người dùng có quyền Kế toán thanh toán. Tồn tại phiếu đề nghị thanh toán ở trạng '
             'thái “Chờ tạo phiếu chi” với hình thức thanh toán là chuyển khoản.',
    chinh='1. Người dùng bấm nút “Tạo mới” ở màn danh sách.\n'
          '2. Hệ thống mở màn “Thêm phiếu ủy nhiệm chi” với Loại chi điền sẵn “Chi trả nhà cung '
          'cấp”, Ngày hạch toán điền sẵn ngày hôm nay, Tỷ giá điền sẵn 1, Hình thức thanh toán '
          'khoá ở “CK”.\n'
          '3. Người dùng bấm vào ô “Số phiếu đề nghị” và chọn một phiếu đề nghị.\n'
          '4. Hệ thống điền tự động Tài khoản có, Tài khoản nợ, Loại tiền, Tỷ giá, Người đề '
          'nghị, Phòng ban, Lý do chi, thông tin đối tượng nhận tiền và toàn bộ dòng chi tiết; '
          'khoá lại ô Loại chi.\n'
          '5. Người dùng chốt “Số tiền duyệt chi” từng dòng, chọn Phương thức thanh toán, Ngân '
          'hàng chuyển và Số tài khoản chuyển khoản.\n'
          '6. Người dùng bấm “Lưu nháp” (hoặc “Lưu và duyệt”, xem FR-08).\n'
          '7. Hệ thống kiểm tra dữ liệu, sinh mã phiếu, ghi phiếu ở trạng thái “Đang tạo”, ghi '
          'một dòng lịch sử và quay về danh sách kèm thông báo thành công.',
    phu='• Không có quyền Kế toán thanh toán → cửa sổ chọn phiếu đề nghị không mở được dữ liệu; '
        'bấm Lưu thì hệ thống từ chối, báo không có quyền lập phiếu ủy nhiệm chi.\n'
        '• Số tiền duyệt chi của một dòng lớn hơn số tiền đề nghị chi → ô đỏ, chặn cả hai nút Lưu.\n'
        '• Nhập số âm ở ô Số tiền duyệt chi → hệ thống tự đưa về 0.\n'
        '• Đổi Tỷ giá → hệ thống tính lại cột quy đổi của toàn bộ dòng chi tiết.\n'
        '• Rời màn khi đã sửa mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
    dacbiet='Đường “Lưu nháp” CỐ Ý chỉ bắt buộc ô Loại chi; mọi ô bắt buộc khác và ràng buộc '
            'ngày hạch toán chỉ áp dụng cho đường “Lưu và duyệt”.')

d.p('2.4.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới',
         shot=shot('06-tao-moi.png'),
         shot_caption='Form Tạo mới phiếu ủy nhiệm chi khi vừa mở')
d.layout(menu=MENU + ' => Tạo mới => Đã chọn phiếu đề nghị',
         shot=shot('09-form-da-chon-de-nghi.png'),
         shot_caption='Form sau khi chọn phiếu đề nghị — dữ liệu và dòng chi tiết được kéo về')

d.p('2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Số phiếu đề nghị', 'Textbox', 'Read-only', '–', 'Có', 'Trống',
     'Gợi ý “Nhấn vào đây để chọn phiếu đề nghị chi”. Bấm vào ô mở cửa sổ chọn phiếu đề nghị. '
     'Không gõ tay được.'),
    ('Tài khoản có', 'Dropdown', 'Enable', 'Danh sách tài khoản kế toán', 'Có', 'Trống',
     'Tự điền “1121 - Tiền Việt Nam” khi chọn phiếu đề nghị.'),
    ('Tài khoản nợ', 'Dropdown', 'Enable', 'Danh sách tài khoản kế toán', 'Có', 'Trống',
     'Tự điền theo loại chi của phiếu đề nghị. Ẩn với loại chi “Chi thưởng thực hiện hợp đồng” '
     'vì loại đó khai tài khoản nợ theo từng dòng chi tiết.'),
    ('Ngày hạch toán', 'Datepicker', 'Enable', 'dd/mm/yyyy, không nhỏ hơn ngày hôm nay', 'Có',
     'Ngày hôm nay', 'Lịch làm mờ mọi ngày quá khứ.'),
    ('Loại chi', 'Dropdown', 'Enable / Disable', 'Danh sách 7 giá trị', 'Có',
     'Chi trả nhà cung cấp',
     'Không có nút xoá lựa chọn. Bị khoá ngay khi đã chọn phiếu đề nghị và ở màn Sửa.'),
    ('Hình thức thanh toán', 'Textbox', 'Disable', '–', '–', 'CK',
     'Phiếu ủy nhiệm chi luôn là chuyển khoản.'),
    ('Loại tiền', 'Textbox', 'Disable', '–', '–', 'Trống',
     'Gợi ý “Theo phiếu đề nghị”. Điền theo phiếu đề nghị sau khi chọn.'),
    ('Tỷ giá (VND)', 'Number', 'Enable / Disable', '> 0', 'Có khi dùng ngoại tệ', '1',
     'Khoá khi loại tiền là đồng Việt Nam. Đổi tỷ giá thì tính lại toàn bộ cột quy đổi.'),
    ('Người đề nghị', 'Textbox', 'Disable', '–', '–', 'Trống', 'Theo phiếu đề nghị.'),
    ('Phòng ban', 'Textbox', 'Disable', '–', '–', 'Trống', 'Theo phiếu đề nghị.'),
    ('Lý do chi', 'Textarea', 'Disable', '–', '–', 'Trống', 'Theo phiếu đề nghị.'),
    ('Khách hàng / Nhà cung cấp / Nhân viên', 'Textbox', 'Disable', '–', '–', 'Ẩn',
     'Hiện đúng một ô tương ứng với đối tượng nhận tiền của phiếu đề nghị.'),
    ('Phí', 'Textbox', 'Disable', '–', '–', 'Ẩn',
     'Chỉ hiện khi đối tượng nhận tiền là nhà cung cấp nước ngoài.'),
    ('Vụ việc', 'Textbox', 'Disable', '–', '–', 'Ẩn',
     'Chỉ hiện với loại chi “Chi thưởng thực hiện hợp đồng”.'),
    ('Phương thức thanh toán', 'Dropdown', 'Enable', 'Tiền tự có / Tiền vay', 'Có', 'Trống', '–'),
    ('Ngân hàng chuyển', 'Dropdown', 'Enable', 'Danh sách ngân hàng', 'Có', 'Trống',
     'Chọn xong thì lọc lại danh sách số tài khoản và xoá số tài khoản đang chọn.'),
    ('Số tài khoản chuyển khoản', 'Dropdown', 'Enable', 'Tài khoản của ngân hàng đã chọn', 'Có',
     'Trống',
     'Nếu ngân hàng chỉ có đúng một tài khoản và phương thức là “Tiền tự có” thì hệ thống tự chọn.'),
    ('Khối “Tài khoản nhận tiền”', 'Label', 'Read-only', '–', '–', 'Ẩn',
     'Gồm Số tài khoản, Tên tài khoản, Tên ngân hàng, Chi nhánh, Thành phố. Không hiện với nhà '
     'cung cấp nước ngoài.'),
    ('Khối “Ngân hàng” và “Ngân hàng trung gian”', 'Label', 'Read-only', '–', '–', 'Ẩn',
     'Chỉ hiện với nhà cung cấp nước ngoài; gồm Số tài khoản, Tài khoản, Tên ngân hàng, Swift '
     'Code, IBAN Number, Địa chỉ.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', 'Có', 'Rỗng',
     'Cột STT, Số đơn hàng/Hợp đồng, Số tiền đề nghị chi, Số tiền duyệt chi, Ghi chú và dòng '
     'Tổng cộng. Khi chưa chọn đề nghị hiện “Chưa chọn phiếu đề nghị chi”.'),
    ('Ô Số tiền duyệt chi trên dòng', 'Number', 'Enable', '0 đến số tiền đề nghị chi', 'Có',
     'Bằng số tiền đề nghị chi',
     'Vượt trần thì báo “Không được lớn hơn số tiền đề nghị chi”; số âm tự về 0.'),
    ('Ô Ghi chú trên dòng', 'Textbox', 'Enable', 'Chuỗi', 'Không', 'Trống', '–'),
    ('Nút Lưu nháp', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Lưu phiếu ở trạng thái “Đang tạo”, bỏ qua các luật bắt buộc trừ Loại chi.'),
    ('Nút Lưu và duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xem FR-08.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Hỏi xác nhận nếu có thay đổi chưa lưu.'),
    ('Thông báo lỗi inline', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Ô viền đỏ kèm chữ đỏ ngay dưới ô bị lỗi.'),
])

d.p('2.4.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Tạo mới', 'Click',
     'After:\n– Mở màn “Thêm phiếu ủy nhiệm chi” với các giá trị điền sẵn nêu ở bảng trên.'),
    ('Bấm vào ô Số phiếu đề nghị', 'Click',
     'Before:\n– Kiểm tra quyền Kế toán thanh toán.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền xem danh sách phiếu đề nghị chi.” và '
     'dừng xử lý.\n'
     'After:\n– Mở cửa sổ “Chọn phiếu đề nghị chi” (xem FR-05).'),
    ('Chọn một phiếu đề nghị trong cửa sổ', 'Click',
     'Before:\n– Kiểm tra quyền Kế toán thanh toán.\n'
     'During:\n– Nạp toàn bộ thông tin phiếu đề nghị và các dòng chi tiết.\n'
     'After:\n– Điền tự động các ô nêu ở dòng sự kiện chính bước 4, đặt “Số tiền duyệt chi” bằng '
     'đúng “Số tiền đề nghị chi” của từng dòng và khoá ô Loại chi.'),
    ('Nhập Số tiền duyệt chi', 'Change / Blur',
     'During:\n– Số âm → tự đưa về 0.\n'
     '– Lớn hơn số tiền đề nghị chi của dòng → ô viền đỏ, hiển thị “Không được lớn hơn số tiền '
     'đề nghị chi (<số tiền đề nghị>)”.\n'
     'After:\n– Tính lại cột quy đổi của dòng và dòng Tổng cộng.'),
    ('Chọn Ngân hàng chuyển', 'Change',
     'During:\n– Ghi lại tên ngân hàng, xoá số tài khoản đang chọn.\n'
     'After:\n– Lọc danh sách số tài khoản theo ngân hàng; nếu chỉ có đúng một tài khoản và '
     'phương thức là “Tiền tự có” thì tự chọn tài khoản đó.'),
    ('Bấm Lưu nháp', 'Click',
     'Before:\n– Kiểm tra quyền Kế toán thanh toán.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền lập phiếu ủy nhiệm chi.” và dừng xử lý.\n'
     'During:\n– Loại chi trống → hiển thị “Bắt buộc chọn loại chi”.\n'
     '– Số tiền duyệt chi vượt số đề nghị chi → hiển thị thông báo nêu rõ số thứ tự dòng sai.\n'
     '– Các ô bắt buộc khác được bỏ qua ở đường lưu nháp.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Sinh mã phiếu dạng <mã công ty>.UNC<tháng năm>.<5 chữ số>, ghi phiếu ở trạng '
     'thái “Đang tạo” cùng đơn vị của người lập.\n'
     '– KHÔNG ghi bút toán và KHÔNG đổi trạng thái phiếu đề nghị.\n'
     '– Ghi một dòng lịch sử “Thêm mới”.\n'
     '– Hiển thị “Thêm phiếu ủy nhiệm chi tiền thành công!” và quay về danh sách.'),
    ('Bấm Quay lại khi đã sửa mà chưa lưu', 'Click',
     'During:\n– Hiển thị hộp “Thông tin chưa lưu” với nội dung “Bạn có thông tin chưa lưu. Có '
     'chắc chắn muốn thoát?”.\n'
     'After:\n– Chọn “Ở lại” thì giữ nguyên dữ liệu; chọn “Thoát” thì bỏ mọi thay đổi và về '
     'danh sách.'),
])

# ---------------------------------------- 2.5 Chon phieu de nghi chi
d.h3('2.5 Chọn phiếu đề nghị chi')

d.p('2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chọn phiếu đề nghị chi', 'crud',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Kéo dữ liệu phiếu đề nghị về form')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-05 Chọn phiếu đề nghị chi')

d.p('2.5.2 Giới thiệu')
d.rule_ref('- Popup tra cứu dữ liệu, Tìm kiếm và Phân trang. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu ủy nhiệm chi tại phần mô tả chi tiết.',
           anchor='list')
d.intro_table(
    ten='Chọn phiếu đề nghị chi để lập phiếu ủy nhiệm chi',
    mota='Cửa sổ tra cứu các phiếu đề nghị thanh toán đủ điều kiện lập phiếu ủy nhiệm chi. Chỉ '
         'liệt kê phiếu đang ở trạng thái “Chờ tạo phiếu chi” VÀ có hình thức thanh toán là '
         'chuyển khoản.',
    tacnhan='Kế toán thanh toán',
    dieukien='Đang ở màn Tạo mới hoặc màn Sửa và có quyền Kế toán thanh toán.',
    chinh='1. Người dùng bấm vào ô “Số phiếu đề nghị”.\n'
          '2. Hệ thống mở cửa sổ “Chọn phiếu đề nghị chi” và nạp trang đầu tiên.\n'
          '3. Người dùng lọc theo mã phiếu, loại chi hoặc người lập (tuỳ chọn).\n'
          '4. Người dùng bấm vào một dòng.\n'
          '5. Hệ thống đóng cửa sổ và kéo toàn bộ dữ liệu phiếu đề nghị về form.',
    phu='• Không có quyền Kế toán thanh toán → hệ thống từ chối, báo không có quyền xem danh '
        'sách phiếu đề nghị chi.\n'
        '• Không có phiếu nào khớp điều kiện → hiện “Không có dữ liệu phù hợp.”.\n'
        '• Không kéo được dữ liệu phiếu đã chọn → hiển thị “Không tải được phiếu đề nghị chi”.\n'
        '• Bấm “Đóng” → giữ nguyên phiếu đề nghị đang chọn trước đó (nếu có).',
    dacbiet='Cửa sổ CỐ Ý không loại bỏ phiếu đề nghị đã có phiếu ủy nhiệm chi khác — xem BR-05.')

d.p('2.5.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới / Sửa => Chọn phiếu đề nghị chi',
         note='Cửa sổ “Chọn phiếu đề nghị chi” được mở ngay trên màn Tạo mới hoặc màn Sửa theo '
              'đường dẫn ở trên.',
         shot=shot('08-popup-chon-de-nghi.png'),
         shot_caption='Cửa sổ Chọn phiếu đề nghị chi')

d.p('2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Chọn phiếu đề nghị chi',
     'Dòng phụ đề: “Chỉ phiếu Chờ tạo phiếu chi, hình thức chuyển khoản”.'),
    ('Mã phiếu đề nghị', 'Textbox', 'Enable', 'Chuỗi bất kỳ', 'Không', 'Trống',
     'Nhấn Enter hoặc bấm Tìm kiếm để lọc.'),
    ('Loại chi', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống',
     'Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng thực hiện hợp đồng, Thanh toán '
     'chi phí vận chuyển NCC. Chọn xong lọc ngay.'),
    ('Người lập', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Chọn xong lọc ngay.'),
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Làm mới xoá mọi điều kiện trong cửa sổ.'),
    ('Bảng kết quả', 'Table/Grid', 'Enable', '–', '–', 'Trang 1, 10 dòng',
     'Cột STT, Mã phiếu đề nghị, Loại chi, Khách hàng / Nhà cung cấp, Số tiền, Người lập, Ngày '
     'lập. Bấm vào cả dòng để chọn.'),
    ('Phân trang trong cửa sổ', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Không',
     'Trang 1, 10 dòng', 'Có ô chọn số dòng mỗi trang.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện “Không có dữ liệu phù hợp.”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không chọn gì.'),
])

d.p('2.5.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở cửa sổ', 'System',
     'Before:\n– Kiểm tra quyền Kế toán thanh toán.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền xem danh sách phiếu đề nghị chi.” và '
     'dừng xử lý.\n'
     'During:\n– Lọc cố định: phiếu đề nghị ở trạng thái “Chờ tạo phiếu chi” và hình thức thanh '
     'toán là chuyển khoản. Hai điều kiện này người dùng không tắt được.\n'
     'After:\n– Hiển thị trang đầu tiên, sắp xếp phiếu mới nhất lên trước.'),
    ('Bấm vào một dòng', 'Click',
     'Before:\n– Kiểm tra quyền Kế toán thanh toán.\n'
     'During:\n– Nạp chi tiết phiếu đề nghị.\n'
     'After:\n– Đóng cửa sổ, điền dữ liệu và dòng chi tiết vào form, khoá ô Loại chi.'),
])

# --------------------------- 2.6 Tao moi phieu Chi thu nhap cho nhan vien
d.h3('2.6 Tạo mới phiếu Chi thu nhập cho nhân viên')

d.p('2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Tạo phiếu Chi thu nhập cho nhân viên', 'crud',
            [('include', 'Kiểm tra quyền Kế toán thanh toán'),
             ('include', 'Lấy thu nhập nhân viên theo phòng ban'),
             ('extend', 'Lưu và duyệt')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-06 Tạo phiếu Chi thu nhập cho nhân viên')

d.p('2.6.2 Giới thiệu')
d.rule_ref('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', anchor='create')
d.intro_table(
    ten='Tạo mới phiếu ủy nhiệm chi loại “Chi thu nhập cho nhân viên”',
    mota='Lập phiếu chi thu nhập cho nhân viên một phòng ban, KHÔNG qua phiếu đề nghị. Hệ thống '
         'tự lấy số thu nhập còn phải trả của từng nhân viên trong phòng ban đó từ sổ kế toán.',
    tacnhan='Kế toán thanh toán',
    dieukien='Người dùng có quyền Kế toán thanh toán và xác định được công ty của mình.',
    chinh='1. Người dùng bấm “Tạo mới”, chọn Loại chi = “Chi thu nhập cho nhân viên”.\n'
          '2. Hệ thống ẩn các ô của luồng lập từ đề nghị, hiện thêm ô “Người nhận”, ô “Phòng '
          'ban” dạng chọn và chuyển “Lý do chi” sang nhập tay; khoá Tài khoản có ở “1121 - Tiền '
          'Việt Nam”, Loại tiền ở đồng Việt Nam và Tỷ giá bằng 1.\n'
          '3. Người dùng chọn Phòng ban.\n'
          '4. Hệ thống lấy danh sách nhân viên còn số dư thu nhập trong phòng ban đó và điền vào '
          'bảng chi tiết, mọi dòng được tích sẵn “Cần thanh toán”.\n'
          '5. Người dùng bỏ tích nhân viên không chi, nhập “Số tiền chi” của từng người, sang '
          'tab “Chi tiết vụ việc” tách số đó thành 5 khoản.\n'
          '6. Người dùng nhập Người nhận, Lý do chi, chọn Ngân hàng chuyển và Số tài khoản '
          'chuyển khoản.\n'
          '7. Người dùng bấm “Lưu nháp” hoặc “Lưu và duyệt”.',
    phu='• Không có quyền Kế toán thanh toán → hệ thống từ chối, báo không có quyền xem số liệu '
        'thu nhập nhân viên.\n'
        '• Phòng ban không có nhân viên nào còn số dư → bảng hiện “Không có dữ liệu phù hợp”.\n'
        '• Chưa chọn phòng ban → bảng hiện “Chưa chọn phòng ban chi — chọn phòng ban để hệ thống '
        'lấy số liệu thu nhập nhân viên.”.\n'
        '• Tổng 5 khoản của một nhân viên khác “Số tiền chi” của nhân viên đó quá 0,5 đồng → hệ '
        'thống chặn khi bấm “Lưu và duyệt”.\n'
        '• Không lấy được số liệu → hiển thị “Không lấy được số liệu thu nhập nhân viên”.',
    dacbiet='Bảng nhân viên CỐ Ý chỉ có 5 khoản, không có khoản “Chi phí khác” như màn Phiếu chi '
            'tiền, vì khoản đó không bao giờ được ghi vào sổ kế toán ở luồng ủy nhiệm chi.')

d.p('2.6.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới => Chi thu nhập cho nhân viên',
         shot=shot('16-form-chi-thu-nhap-nv.png'),
         shot_caption='Form khi chọn Loại chi “Chi thu nhập cho nhân viên”')
d.layout(menu=MENU + ' => Tạo mới => Chi thu nhập cho nhân viên => Chi tiết vụ việc',
         shot=shot('18-tab-chi-tiet-vu-viec.png'),
         shot_caption='Tab “Chi tiết vụ việc” với 5 khoản thu nhập')

d.p('2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Loại chi', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Có', 'Chi trả nhà cung cấp',
     'Chọn “Chi thu nhập cho nhân viên” để vào luồng này.'),
    ('Tài khoản có', 'Dropdown', 'Disable', '–', 'Có', '1121 - Tiền Việt Nam',
     'Bị khoá cứng ở luồng này.'),
    ('Người nhận', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
     'Chỉ có ở luồng này. Gợi ý “Nhập tên người nhận tiền”.'),
    ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Có', 'Trống',
     'Gợi ý “Chọn phòng ban chi”. Chọn xong hệ thống lấy số liệu nhân viên và ghi đè bảng chi tiết.'),
    ('Lý do chi', 'Textarea', 'Enable', 'Chuỗi', 'Có', 'Trống', 'Gợi ý “Nhập lý do chi”.'),
    ('Loại tiền', 'Textbox', 'Disable', '–', '–', 'VietNamDong', 'Bị khoá cứng.'),
    ('Tỷ giá (VND)', 'Number', 'Disable', '–', '–', '1', 'Bị khoá cứng.'),
    ('Người đề nghị', 'Textbox', 'Disable', '–', '–', 'Tên người đăng nhập', '–'),
    ('Ngân hàng chuyển / Số tài khoản chuyển khoản', 'Dropdown', 'Enable', 'Danh sách', 'Có',
     'Trống', 'Giống luồng lập từ đề nghị.'),
    ('Tab Chi tiết', 'Table/Grid', 'Enable', '–', 'Có', 'Rỗng',
     'Cột: ô tích “Cần thanh toán”, STT, Số tài khoản nợ, Tên tài khoản, Nhân viên, Số dư, Số '
     'tiền chi, Tài khoản, Tên ngân hàng, Chi nhánh và dòng Tổng cộng.'),
    ('Tab Chi tiết vụ việc', 'Table/Grid', 'Enable', '–', 'Có', 'Rỗng',
     'Nhóm “Số dư” và nhóm “Số tiền chi”, mỗi nhóm 5 khoản: Chênh lệch lương, Hoa hồng tháng, '
     'Hoa hồng quý, Thưởng quý, Tiền vận chuyển.'),
    ('Ô tích Cần thanh toán', 'Icon Button', 'Enable', '–', '–', 'Bật tất cả',
     'Bỏ tích thì dòng mờ đi, mọi ô nhập của dòng bị khoá và dòng đó không được lưu.'),
    ('Ô Số tiền chi', 'Number', 'Enable / Disable', '0 đến số dư của nhân viên', 'Có', '0',
     'Bị khoá khi dòng không được tích hoặc số dư bằng 0. Vượt số dư thì tự kẹp về số dư.'),
    ('Ô 5 khoản ở tab vụ việc', 'Number', 'Enable / Disable', 'Cùng dấu với số dư của khoản',
     'Có', '0', 'Bị khoá khi chưa khai “Số tiền chi” ở tab Chi tiết.'),
    ('Số tài khoản nợ trên dòng', 'Dropdown', 'Enable', 'Danh sách tài khoản kế toán', 'Có',
     'Theo mặc định của hệ thống',
     'Đổi ở dòng đầu tiên thì áp cho toàn bộ các dòng còn lại.'),
])

d.p('2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Chọn Loại chi “Chi thu nhập cho nhân viên”', 'Change',
     'During:\n– Xoá phiếu đề nghị đang chọn và toàn bộ bảng chi tiết.\n'
     'After:\n– Ẩn Số phiếu đề nghị, Tài khoản nợ, Ngày hạch toán, Phương thức thanh toán; hiện '
     'Người nhận, Phòng ban dạng chọn; khoá Tài khoản có, Loại tiền và Tỷ giá.'),
    ('Chọn Phòng ban', 'Change',
     'Before:\n– Kiểm tra quyền Kế toán thanh toán.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền xem số liệu thu nhập nhân viên.” và '
     'dừng xử lý.\n'
     'During:\n– Lấy số thu nhập còn phải trả của nhân viên phòng ban đó, giới hạn trong công ty '
     'của người đăng nhập; loại nhân viên có toàn bộ khoản bằng 0.\n'
     'After:\n– Ghi đè bảng chi tiết, tích sẵn “Cần thanh toán” cho mọi dòng.'),
    ('Nhập Số tiền chi', 'Change / Blur',
     'During:\n– Giá trị vượt số dư → tự kẹp về đúng số dư.\n'
     'After:\n– Mở khoá 5 ô khoản của dòng ở tab “Chi tiết vụ việc” và cập nhật dòng Tổng cộng.'),
    ('Bấm Lưu và duyệt', 'Click',
     'During:\n– Người nhận / Phòng ban / Lý do chi trống → hiển thị “Bắt buộc nhập” dưới ô '
     'tương ứng.\n'
     '– Tổng 5 khoản khác “Số tiền chi” quá 0,5 đồng → hiển thị “Tổng số tiền chi theo mã vụ '
     'việc và tổng số tiền đề nghị chi khác nhau!”.\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Ghi phiếu ở trạng thái “Đã hạch toán”, ghi bút toán theo từng khoản của từng '
     'nhân viên cùng hai bút toán tổng, ghi lịch sử và quay về danh sách.'),
])

# ------------------------------------------------------ 2.7 Chinh sua
d.h3('2.7 Chỉnh sửa phiếu ủy nhiệm chi')

d.p('2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Chỉnh sửa phiếu ủy nhiệm chi', 'crud',
            [('include', 'Kiểm tra điều kiện sửa'),
             ('extend', 'Lưu và duyệt')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-07 Chỉnh sửa phiếu ủy nhiệm chi')

d.p('2.7.2 Giới thiệu')
d.rule_ref('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX. Logic ghi lịch sử áp dụng '
           'theo SRS Các quy tắc chung - Quy tắc ghi lịch sử.',
           anchor='edit')
d.intro_table(
    ten='Chỉnh sửa phiếu ủy nhiệm chi',
    mota='Sửa lại phiếu đang ở trạng thái “Đang tạo”. Toàn bộ ô và bảng chi tiết giống màn Tạo '
         'mới, bổ sung ba ô chỉ đọc Mã phiếu, Người lập, Ngày lập.',
    tacnhan='Kế toán thanh toán',
    dieukien='Phiếu ở trạng thái “Đang tạo”, do chính người đăng nhập lập, và người đó có quyền '
             'Kế toán thanh toán. Thiếu một trong ba điều kiện thì nút Sửa không hiển thị.',
    chinh='1. Người dùng bấm nút Sửa ở danh sách hoặc ở chân màn chi tiết.\n'
          '2. Hệ thống mở màn “Sửa phiếu ủy nhiệm chi” và nạp lại dữ liệu phiếu.\n'
          '3. Người dùng sửa thông tin.\n'
          '4. Người dùng bấm “Lưu nháp” hoặc “Lưu và duyệt”.\n'
          '5. Hệ thống kiểm tra điều kiện sửa, ghi lại phiếu, ghi lịch sử thay đổi và quay về '
          'danh sách.',
    phu='• Không đủ điều kiện sửa (phiếu đã hạch toán, không phải người lập, thiếu quyền) → hệ '
        'thống từ chối với thông báo “Chỉ sửa được phiếu ủy nhiệm chi ở trạng thái Đang tạo do '
        'chính bạn lập”.\n'
        '• Vào màn Sửa bằng đường dẫn trực tiếp khi không đủ điều kiện → hệ thống tự đưa về màn '
        'xem chi tiết.\n'
        '• Không nạp được phiếu → hiển thị “Không tải được phiếu ủy nhiệm chi” và quay về danh sách.\n'
        '• Rời màn khi đã sửa mà chưa lưu → hệ thống hỏi xác nhận rời trang.',
    dacbiet='Ô “Loại chi” bị khoá ở màn Sửa. Muốn đổi loại chi phải xóa phiếu và lập lại.')

d.p('2.7.3 Layout màn hình')
d.layout(menu=MENU + ' => Sửa',
         shot=shot('23-sua-phieu.png'),
         shot_caption='Màn Sửa phiếu ủy nhiệm chi với dữ liệu thật')

d.p('2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '–', 'Sửa phiếu ủy nhiệm chi', '–'),
    ('Mã phiếu', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', 'Chỉ có ở màn Sửa và màn chi tiết.'),
    ('Người lập', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', 'Chỉ có ở màn Sửa và màn chi tiết.'),
    ('Ngày lập', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', 'Chỉ có ở màn Sửa và màn chi tiết.'),
    ('Loại chi', 'Dropdown', 'Disable', '–', '–', 'Theo dữ liệu', 'Luôn bị khoá ở màn Sửa.'),
    ('Ngày hạch toán', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có khi Lưu và duyệt', 'Theo dữ liệu',
     'Nạp lại đúng ngày đã lưu; lịch vẫn chặn ngày quá khứ.'),
    ('Các ô còn lại', 'Textbox', 'Enable / Disable', '–', '–', 'Theo dữ liệu',
     'Giống hệt màn Tạo mới, kể cả bảng chi tiết và hai luồng theo loại chi.'),
    ('Nút Lưu nháp / Lưu và duyệt / Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
     'Giống màn Tạo mới.'),
])

d.p('2.7.5 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn Sửa', 'System',
     'Before:\n– Kiểm tra ba điều kiện sửa: trạng thái Đang tạo, đúng người lập, có quyền Kế '
     'toán thanh toán.\n'
     '– Nếu không đủ → tự chuyển sang màn xem chi tiết.\n'
     'After:\n– Nạp dữ liệu phiếu vào form, khoá ô Loại chi.'),
    ('Bấm Lưu nháp ở màn Sửa', 'Click',
     'Before:\n– Kiểm tra lại ba điều kiện sửa ở phía máy chủ.\n'
     '– Nếu không đủ → hiển thị “Chỉ sửa được phiếu ủy nhiệm chi ở trạng thái Đang tạo do chính '
     'bạn lập” và dừng xử lý.\n'
     'During:\n– Áp dụng các luật giống màn Tạo mới.\n'
     'After:\n– Ghi lại phiếu, thay toàn bộ dòng chi tiết bằng dữ liệu mới.\n'
     '– Ghi một dòng lịch sử ghi rõ giá trị cũ và giá trị mới của từng ô đã đổi.\n'
     '– Hiển thị “Cập nhật phiếu ủy nhiệm chi tiền thành công!” và quay về danh sách.'),
])

# ------------------------------------------------------ 2.8 Luu va duyet
d.h3('2.8 Lưu và duyệt phiếu ủy nhiệm chi')

d.p('2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Lưu và duyệt phiếu', 'action',
            [('include', 'Kiểm tra dữ liệu đầy đủ'),
             ('include', 'Ghi bút toán vào sổ kế toán'),
             ('include', 'Chuyển trạng thái phiếu đề nghị')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-08 Lưu và duyệt phiếu ủy nhiệm chi')

d.p('2.8.2 Giới thiệu')
d.rule_ref('- Hộp xác nhận thao tác, Validate dữ liệu và Thông báo.', anchor='create')
d.intro_table(
    ten='Lưu và duyệt phiếu ủy nhiệm chi',
    mota='Chuyển phiếu sang trạng thái “Đã hạch toán”, ghi bút toán vào sổ kế toán, đẩy số tiền '
         'duyệt chi về phiếu đề nghị và chuyển phiếu đề nghị ra khỏi trạng thái “Chờ tạo phiếu '
         'chi”. Toàn bộ được thực hiện trong một giao dịch: có lỗi ở bất kỳ bước nào thì mọi '
         'thay đổi bị huỷ.',
    tacnhan='Kế toán thanh toán',
    dieukien='Đang ở màn Tạo mới hoặc màn Sửa của một phiếu nháp và có quyền Kế toán thanh toán.',
    chinh='1. Người dùng bấm nút “Lưu và duyệt”.\n'
          '2. Hệ thống hiển thị hộp “Xác nhận lưu và duyệt” với nội dung “Bạn đồng ý lưu và '
          'duyệt?”.\n'
          '3. Người dùng bấm “Xác nhận”.\n'
          '4. Hệ thống kiểm tra đầy đủ dữ liệu bắt buộc và ràng buộc ngày hạch toán.\n'
          '5. Hệ thống ghi phiếu ở trạng thái “Đã hạch toán”, ghi người duyệt là người đang thao '
          'tác.\n'
          '6. Hệ thống đẩy số tiền duyệt chi về phiếu đề nghị và chuyển phiếu đề nghị ra khỏi '
          'trạng thái “Chờ tạo phiếu chi”.\n'
          '7. Hệ thống ghi bút toán vào sổ kế toán.\n'
          '8. Hệ thống ghi lịch sử và quay về danh sách kèm thông báo thành công.',
    phu='• Bấm “Hủy” ở hộp xác nhận → đóng hộp, không lưu gì.\n'
        '• Thiếu ô bắt buộc → hiển thị “Vui lòng kiểm tra lại dữ liệu nhập”, các ô thiếu viền đỏ '
        'kèm chữ “Bắt buộc nhập”, không lưu.\n'
        '• Ngày hạch toán nhỏ hơn ngày hôm nay → hiển thị “Ngày hạch toán không được nhỏ hơn '
        'ngày hôm nay”, không lưu.\n'
        '• Số tiền duyệt chi của một dòng bằng 0 → hiển thị “Phải lớn hơn 0”, không lưu.\n'
        '• Phiếu đã ở trạng thái “Đã hạch toán” (người khác vừa duyệt) → hệ thống từ chối, không '
        'ghi bút toán trùng.',
    dacbiet='Sau bước này phiếu KHÔNG sửa và KHÔNG xóa được nữa. Màn hình không có chức năng huỷ '
            'duyệt.')

d.p('2.8.3 Layout màn hình')
d.layout(menu=MENU + ' => Tạo mới / Sửa => Lưu và duyệt',
         note='Hộp xác nhận được mở ngay trên màn Tạo mới hoặc màn Sửa theo đường dẫn ở trên.',
         shot=shot('14-xac-nhan-luu-va-duyet.png'),
         shot_caption='Hộp “Xác nhận lưu và duyệt”')
d.layout(menu=MENU + ' => Tạo mới => Lưu và duyệt (thiếu dữ liệu)',
         shot=shot('15-loi-validate.png'),
         shot_caption='Báo lỗi khi bấm “Lưu và duyệt” với form còn trống')

d.p('2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp xác nhận', 'Label', 'Hiển thị', 'Xác nhận lưu và duyệt', '–'),
    ('Nội dung hộp xác nhận', 'Label', 'Hiển thị', 'Bạn đồng ý lưu và duyệt?', '–'),
    ('Nút Xác nhận', 'Button', 'Enable', 'Hiển thị', 'Thực hiện lưu và duyệt.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không lưu.'),
    ('Thông báo lỗi tổng', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     'Hiện “Vui lòng kiểm tra lại dữ liệu nhập” ở góc phải khi có ô sai.'),
    ('Lỗi inline từng ô', 'Toast / Alert', 'Hiển thị', 'Ẩn',
     'Ô viền đỏ kèm chữ đỏ ngay dưới ô.'),
], required=False, scope=False)

d.p('2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu và duyệt', 'Click',
     'Before:\n– Hiển thị hộp xác nhận. Chưa gửi dữ liệu đi.'),
    ('Bấm Xác nhận trong hộp', 'Click',
     'Before:\n– Kiểm tra quyền Kế toán thanh toán; ở màn Sửa kiểm tra thêm ba điều kiện sửa.\n'
     '– Nếu không đủ → hiển thị thông báo từ chối tương ứng và dừng xử lý.\n'
     'During:\n– Ô bắt buộc trống → hiển thị “Bắt buộc nhập” dưới ô tương ứng.\n'
     '– Loại chi trống → hiển thị “Bắt buộc chọn loại chi”.\n'
     '– Ngày hạch toán nhỏ hơn hôm nay → hiển thị “Ngày hạch toán không được nhỏ hơn ngày hôm '
     'nay”.\n'
     '– Số tiền duyệt chi bằng 0 → hiển thị “Phải lớn hơn 0”; lớn hơn số đề nghị chi → hiển thị '
     '“Không được lớn hơn số tiền đề nghị chi”.\n'
     '– Tỷ giá không lớn hơn 0 với phiếu ngoại tệ → hiển thị “Nhập số lớn hơn 0”.\n'
     '– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Ghi phiếu ở trạng thái “Đã hạch toán” và ghi người duyệt.\n'
     '– Đẩy số tiền duyệt chi về các dòng của phiếu đề nghị và chuyển phiếu đề nghị ra khỏi '
     'trạng thái “Chờ tạo phiếu chi”.\n'
     '– Ghi bút toán vào sổ kế toán theo quy tắc BR-01, BR-02, BR-03.\n'
     '– Ghi hai dòng lịch sử: nội dung thay đổi và chuyển trạng thái.\n'
     '– Hiển thị “Duyệt phiếu ủy nhiệm chi thành công!” và quay về danh sách.'),
])

# ------------------------------------------------------ 2.9 Xem chi tiet
d.h3('2.9 Xem chi tiết phiếu ủy nhiệm chi')

d.p('2.9.1 Giới thiệu')
d.rule_ref('- Màn Chi tiết và UI/UX. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu ủy nhiệm chi tại phần mô tả chi tiết.',
           anchor='detail')
d.intro_table(
    ten='Xem chi tiết phiếu ủy nhiệm chi',
    mota='Hiển thị toàn bộ thông tin phiếu ở chế độ chỉ đọc, kèm bảng chi tiết và khối Lịch sử. '
         'Các nút thao tác ở chân màn chỉ hiện khi phiếu còn cho phép thao tác đó.',
    tacnhan='Kế toán thanh toán; Người có quyền xem phiếu ủy nhiệm chi',
    dieukien='Người dùng có quyền xem phiếu đó: là người lập, là người duyệt, hoặc phiếu không '
             'phải nháp và người dùng có quyền xem theo cấp phù hợp.',
    chinh='1. Người dùng bấm vào mã phiếu ở màn danh sách.\n'
          '2. Hệ thống kiểm tra quyền xem phiếu.\n'
          '3. Hệ thống hiển thị màn chi tiết ở chế độ chỉ đọc kèm tiêu đề “Chi tiết phiếu ủy '
          'nhiệm chi: <mã phiếu>”.\n'
          '4. Người dùng có thể mở khối “Lịch sử” ở cuối trang.',
    phu='• Không có quyền xem phiếu → hệ thống từ chối, báo không có quyền xem phiếu ủy nhiệm '
        'chi này.\n'
        '• Phiếu đã bị xóa → hệ thống báo dữ liệu đã thay đổi và đưa về danh sách.',
    dacbiet=None)

d.p('2.9.2 Layout màn hình')
d.layout(menu=MENU + ' => Xem chi tiết',
         shot=shot('19-chi-tiet-da-hach-toan.png'),
         shot_caption='Màn chi tiết phiếu đã hạch toán (nhà cung cấp nước ngoài, ngoại tệ)')
d.layout(menu=MENU + ' => Xem chi tiết (phiếu nháp)',
         shot=shot('21-chi-tiet-dang-tao.png'),
         shot_caption='Màn chi tiết phiếu “Đang tạo” — chân màn có thêm nút Sửa và Xóa')

d.p('2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Chi tiết phiếu ủy nhiệm chi: <mã phiếu>',
     'Trước khi nạp xong hiển thị “Chi tiết phiếu ủy nhiệm chi”.'),
    ('Toàn bộ ô thông tin chung', 'Textbox', 'Read-only', '–', 'Theo dữ liệu',
     'Cùng danh sách ô với màn Sửa, kể cả Mã phiếu, Người lập, Ngày lập; không gõ và không bấm '
     'mở cửa sổ chọn đề nghị được.'),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mọi ô nhập chuyển thành chữ; số căn phải; ghi chú trống hiển thị dấu gạch ngang. Phiếu Chi '
     'thu nhập cho nhân viên ẩn cột tích “Cần thanh toán”.'),
    ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
     'Bấm “Xem lịch sử” để mở; có nút “Làm mới” và “Thu gọn”. Chỉ nạp dữ liệu ở lần mở đầu tiên.'),
    ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Chỉ hiện khi phiếu Đang tạo, do chính mình lập và có quyền Kế toán thanh toán.'),
    ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
     'Cùng điều kiện với nút Sửa.'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn danh sách.'),
], required=False)

d.p('2.9.4 Danh sách event và xử lý event')
d.event_table([
    ('Mở màn chi tiết', 'System',
     'Before:\n– Kiểm tra quyền xem phiếu.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền xem phiếu ủy nhiệm chi này” và dừng '
     'xử lý.\n'
     'After:\n– Hiển thị dữ liệu ở chế độ chỉ đọc; các nút thao tác được bật tắt theo cờ do hệ '
     'thống trả về, mặc định là ẩn.'),
    ('Bấm Xem lịch sử', 'Click',
     'After:\n– Mở khối lịch sử, nạp danh sách thay đổi ở lần mở đầu tiên và hiển thị giá trị cũ '
     'so với giá trị mới.'),
])

# ------------------------------------------------------ 2.10 Xoa
d.h3('2.10 Xóa phiếu ủy nhiệm chi')

d.p('2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Xóa phiếu ủy nhiệm chi', 'action',
            [('include', 'Kiểm tra điều kiện xóa'),
             ('include', 'Xóa dòng chi tiết kèm theo')],
            actor=ACTOR_KT,
            caption='Biểu đồ Use Case — FR-10 Xóa phiếu ủy nhiệm chi')

d.p('2.10.2 Giới thiệu')
d.rule_ref('- Hộp thoại xác nhận Xóa và Thông báo.', anchor='delete')
d.intro_table(
    ten='Xóa phiếu ủy nhiệm chi',
    mota='Xóa vĩnh viễn một phiếu ở trạng thái “Đang tạo” cùng toàn bộ dòng chi tiết của nó.',
    tacnhan='Kế toán thanh toán',
    dieukien='Phiếu ở trạng thái “Đang tạo”, do chính người đăng nhập lập, và người đó có quyền '
             'Kế toán thanh toán.',
    chinh='1. Người dùng bấm nút Xóa ở danh sách hoặc ở chân màn chi tiết.\n'
          '2. Hệ thống hiển thị hộp “Xác nhận xóa” kèm mã phiếu.\n'
          '3. Người dùng bấm “Xóa”.\n'
          '4. Hệ thống kiểm tra điều kiện xóa, xóa dòng chi tiết rồi xóa phiếu.\n'
          '5. Hệ thống ghi một dòng lịch sử, hiển thị thông báo thành công và tải lại danh sách.',
    phu='• Bấm “Hủy” → đóng hộp, không xóa.\n'
        '• Không đủ điều kiện xóa → hệ thống từ chối với thông báo “Chỉ xóa được phiếu ủy nhiệm '
        'chi ở trạng thái Đang tạo do chính bạn lập”.\n'
        '• Phiếu đã bị người khác xóa trước đó → hệ thống báo dữ liệu đã thay đổi và tải lại '
        'danh sách.',
    dacbiet='Xóa phiếu KHÔNG trả trạng thái phiếu đề nghị về trạng thái cũ, vì lúc lưu nháp hệ '
            'thống cũng chưa hề đổi trạng thái phiếu đề nghị.')

d.p('2.10.3 Layout màn hình')
d.layout(menu=MENU + ' => Xóa',
         note='Hộp xác nhận được mở ngay trên màn danh sách hoặc màn chi tiết theo đường dẫn ở trên.',
         shot=shot('22-xac-nhan-xoa.png'),
         shot_caption='Hộp “Xác nhận xóa” mở từ màn chi tiết')

d.p('2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề hộp thoại', 'Label', 'Hiển thị', 'Xác nhận xóa', '–'),
    ('Nội dung hộp thoại', 'Label', 'Hiển thị',
     'Bạn có chắc muốn xóa phiếu ủy nhiệm chi ‘<mã phiếu>’?', 'Luôn nêu rõ mã phiếu bị xóa.'),
    ('Nút Xóa', 'Button', 'Enable', 'Hiển thị', 'Màu đỏ; thực hiện xóa.'),
    ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', 'Đóng hộp, không xóa.'),
], required=False, scope=False)

d.p('2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm nút Xóa trên dòng hoặc ở chân màn chi tiết', 'Click',
     'Before:\n– Nút chỉ hiển thị khi đủ ba điều kiện xóa.\n'
     'After:\n– Mở hộp xác nhận kèm mã phiếu.'),
    ('Bấm Xóa trong hộp xác nhận', 'Click',
     'Before:\n– Kiểm tra lại ba điều kiện xóa ở phía máy chủ.\n'
     '– Nếu không đủ → hiển thị “Chỉ xóa được phiếu ủy nhiệm chi ở trạng thái Đang tạo do chính '
     'bạn lập” và dừng xử lý.\n'
     'During:\n– Xóa các dòng phân bổ, rồi xóa các dòng chi tiết, rồi xóa phiếu, trong cùng một '
     'giao dịch.\n'
     'After:\n– Ghi một dòng lịch sử “Xóa”.\n'
     '– Hiển thị “Xóa phiếu ủy nhiệm chi thành công!”, tải lại danh sách hoặc quay về danh sách '
     'nếu đang ở màn chi tiết.'),
])

# ------------------------------------------------------ 2.11 Lich su
d.h3('2.11 Xem lịch sử thay đổi')

d.p('2.11.1 Giới thiệu')
d.rule_ref('- Quy tắc ghi lịch sử và popup Lịch sử thay đổi. '
           'Chỉ bổ sung các quy tắc riêng của màn Phiếu ủy nhiệm chi tại phần mô tả chi tiết.',
           anchor='history')
d.intro_table(
    ten='Xem lịch sử thay đổi của phiếu ủy nhiệm chi',
    mota='Hiển thị các lần thêm mới, chỉnh sửa, chuyển trạng thái và xóa của một phiếu, kèm giá '
         'trị cũ và giá trị mới của từng ô đã đổi.',
    tacnhan='Kế toán thanh toán; Người có quyền xem phiếu ủy nhiệm chi',
    dieukien='Đang ở màn danh sách hoặc màn chi tiết của phiếu.',
    chinh='1. Người dùng bấm biểu tượng Lịch sử ở cột Hành động, hoặc bấm “Xem lịch sử” ở màn '
          'chi tiết.\n'
          '2. Hệ thống nạp và hiển thị danh sách thay đổi theo thứ tự thời gian.',
    phu='• Phiếu chưa từng bị thay đổi → hiển thị “Chưa có lịch sử thao tác nào.”.\n'
        '• Bấm “Đóng” hoặc “Thu gọn” → đóng khối lịch sử.',
    dacbiet='Hệ thống theo dõi thay đổi của thông tin chung, bảng chi tiết và bảng phân bổ. Việc '
            'chuyển trạng thái được ghi thành dòng lịch sử riêng, nên một lần bấm “Lưu và duyệt” '
            'trên phiếu nháp sinh ra hai dòng lịch sử.')

d.p('2.11.2 Layout màn hình')
d.layout(menu=MENU + ' => Lịch sử',
         note='Cửa sổ Lịch sử được mở ngay trên màn danh sách theo đường dẫn ở trên; màn chi tiết '
              'có khối Lịch sử với nội dung tương đương.',
         shot=shot('24-popup-lich-su.png'),
         shot_caption='Cửa sổ “Lịch sử thay đổi” của một phiếu chưa từng bị sửa')

d.p('2.11.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Lịch sử thay đổi',
     'Dòng phụ đề ghi “Phiếu: <mã phiếu>”.'),
    ('Danh sách thay đổi', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
     'Mỗi dòng gồm thời điểm, người thao tác, loại thao tác và các ô đã đổi kèm giá trị cũ và mới.'),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', 'Hiện “Chưa có lịch sử thao tác nào.”.'),
    ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
], required=False)

d.p('2.11.4 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Lịch sử', 'Click',
     'After:\n– Mở cửa sổ và nạp danh sách thay đổi của đúng phiếu đó.'),
    ('Bấm Làm mới ở khối Lịch sử', 'Click',
     'After:\n– Nạp lại danh sách thay đổi mới nhất.'),
])

# ==================================================== PHAN 4. QUY TAC NGHIEP VU
d.h1('Phần 4. Quy tắc nghiệp vụ')

d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu ủy nhiệm chi; không lặp lại các '
           'quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')

d.rule_table([
    ('BR-01', 'Bút toán bên Có bằng số tiền dòng cuối', [
        '– Khi duyệt phiếu lập từ phiếu đề nghị, hệ thống ghi một bút toán bên Nợ cho MỖI dòng '
        'chi tiết và ĐÚNG MỘT bút toán bên Có.',
        '– Số tiền của bút toán bên Có bằng số tiền duyệt chi của DÒNG CUỐI CÙNG trong bảng chi '
        'tiết, KHÔNG phải tổng các dòng.',
        '– Đây là hành vi CỐ Ý giữ nguyên theo hệ thống ERP cũ để hai hệ thống đối chiếu được '
        '1:1. Đã đo trên dữ liệu thật và được chốt giữ nguyên. KHÔNG được sửa thành phép cộng '
        'dồn nếu chưa có quyết định mới bằng văn bản.',
    ], 'Lưu và duyệt'),

    ('BR-02', 'Loại chi quyết định cách ghi bút toán', [
        '– Dòng chi tiết có phân bổ theo phiếu xuất hàng: mỗi phân bổ sinh một bút toán bên Nợ '
        'trên tài khoản nợ CỦA PHIẾU.',
        '– Loại chi “Chi thưởng thực hiện hợp đồng”: tài khoản nợ lấy theo TỪNG DÒNG chi tiết, '
        'đối tượng là người lập phiếu đề nghị, bút toán gắn mã vụ việc và số tài khoản chuyển '
        'khoản của phiếu.',
        '– Loại chi “Thanh toán chi phí vận chuyển NCC”: nhà cung cấp lấy theo CHUYẾN XE, không '
        'lấy theo phiếu đề nghị.',
        '– Các loại chi còn lại: tài khoản nợ lấy theo phiếu, đối tượng lấy theo phiếu đề nghị.',
    ], 'Lưu và duyệt'),

    ('BR-03', 'Loại chi “Chi khác” không sinh bút toán', [
        '– Phiếu loại “Chi khác” duyệt xong vẫn chuyển sang “Đã hạch toán” nhưng KHÔNG sinh bút '
        'toán nào trong sổ kế toán.',
        '– Đây là hành vi CỐ Ý giữ nguyên theo hệ thống ERP cũ.',
    ], 'Lưu và duyệt'),

    ('BR-04', 'Ghi sổ cho phiếu Chi thu nhập cho nhân viên', [
        '– Mỗi nhân viên sinh 5 bút toán tương ứng 5 khoản thu nhập, chiều Nợ hay Có do dấu của '
        'khoản quyết định, số tiền lấy trị tuyệt đối.',
        '– Cuối cùng sinh thêm hai bút toán tổng trên tài khoản tiền: một bút toán bên Có cho '
        'tổng các khoản dương và một bút toán bên Nợ cho tổng các khoản âm.',
        '– Khoản có giá trị bằng 0 không sinh bút toán.',
        '– Thiếu tài khoản kế toán bắt buộc → toàn bộ giao dịch bị huỷ, phiếu không được lưu.',
    ], 'Lưu và duyệt'),

    ('BR-05', 'Không chặn một phiếu đề nghị có nhiều phiếu ủy nhiệm chi', [
        '– Cửa sổ Chọn phiếu đề nghị chi KHÔNG loại bỏ phiếu đề nghị đã có phiếu ủy nhiệm chi ở '
        'trạng thái nháp.',
        '– Hệ quả đã biết: hai người có thể cùng lập hai phiếu nháp từ một phiếu đề nghị.',
        '– Đây là điểm hở CỐ Ý giữ nguyên theo hệ thống ERP cũ; nghiệp vụ tự kiểm soát. Sau khi '
        'một phiếu được duyệt thì phiếu đề nghị rời trạng thái “Chờ tạo phiếu chi” nên không '
        'chọn lại được nữa.',
    ], ['Tạo mới', 'Chỉnh sửa']),

    ('BR-06', 'Ngày hạch toán không được lùi về quá khứ', [
        '– Khi bấm “Lưu và duyệt”, ngày hạch toán phải bằng hoặc lớn hơn ngày hôm nay; áp dụng ở '
        'cả màn Tạo mới lẫn màn Sửa.',
        '– Khi bấm “Lưu nháp”, ràng buộc này được nới: ngày quá khứ vẫn lưu được, vì phiếu nháp '
        'chưa có ý nghĩa kế toán.',
        '– Hệ quả cần biết: phiếu nháp để qua đêm, hôm sau mở ra bấm “Lưu và duyệt” mà không đổi '
        'ngày sẽ bị chặn. Đây là thiết kế, không phải lỗi.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt']),

    ('BR-07', 'Hai đường lưu có mức ràng buộc khác nhau', [
        '– Đường “Lưu nháp”: chỉ bắt buộc ô Loại chi. Mọi ô bắt buộc khác được nới thành không '
        'bắt buộc, nhưng các luật định dạng (giá trị phải tồn tại trong danh mục, phải là số, '
        'phải là ngày) vẫn giữ nguyên.',
        '– Đường “Lưu và duyệt”: bắt buộc đầy đủ theo từng loại chi.',
        '– Ràng buộc “Số tiền duyệt chi không lớn hơn Số tiền đề nghị chi” áp dụng cho CẢ HAI '
        'đường.',
    ], ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt']),

    ('BR-08', 'Điều kiện sửa và xóa', [
        '– Sửa và xóa dùng CHUNG một bộ điều kiện, phải đủ cả ba: phiếu ở trạng thái “Đang tạo”, '
        'người thao tác đúng là người lập phiếu, và người đó có quyền “Kế toán thanh toán”.',
        '– Người quản trị hệ thống CỐ Ý không được miễn trừ ba điều kiện này.',
        '– Điều kiện được kiểm ở cả giao diện (ẩn nút) và phía máy chủ (từ chối thao tác gọi '
        'thẳng, bỏ qua giao diện).',
    ], ['Chỉnh sửa', 'Xóa']),

    ('BR-09', 'Phạm vi dữ liệu và phiếu nháp', [
        '– Phạm vi xem xét theo thứ tự: quản trị hệ thống hoặc quyền xem toàn tổng công ty → '
        'quyền xem theo công ty → không cấp nào (chỉ phiếu của mình).',
        '– Người dùng LUÔN nhìn thấy phiếu do mình lập và phiếu do mình duyệt, kể cả ở công ty '
        'khác.',
        '– Phiếu ở trạng thái “Đang tạo” chỉ người lập nhìn thấy; ràng buộc này phủ lên mọi cấp '
        'quyền, kể cả quản trị hệ thống.',
        '– Không xác định được đơn vị của người đăng nhập → chỉ thấy phiếu của chính mình.',
    ], 'Toàn màn hình'),

    ('BR-10', 'Nguồn phiếu đề nghị của màn hình', [
        '– Chỉ nhận phiếu đề nghị thanh toán đang ở trạng thái “Chờ tạo phiếu chi” VÀ có hình '
        'thức thanh toán là chuyển khoản.',
        '– Phiếu đề nghị thanh toán tiền mặt thuộc màn Phiếu chi tiền; hai màn không bao giờ '
        'nhận cùng một phiếu đề nghị.',
        '– Cửa sổ chọn phiếu đề nghị KHÔNG áp phạm vi xem theo cấp của màn Phiếu đề nghị thanh '
        'toán: kế toán chọn được phiếu đề nghị của công ty khác.',
    ], ['Tạo mới', 'Chỉnh sửa']),

    ('BR-11', 'Giá trị hệ thống tự quyết định', [
        '– Mã phiếu do hệ thống sinh theo dạng <mã công ty>.UNC<tháng năm>.<5 chữ số>, tăng liên '
        'tiếp trong cùng tháng và cùng công ty; không nhận mã do người dùng gửi lên.',
        '– Công ty, phòng ban, bộ phận của phiếu luôn lấy theo người lập, không nhận từ giao diện.',
        '– Hình thức thanh toán luôn là chuyển khoản.',
        '– Trạng thái chỉ nhận hai giá trị “Đang tạo” và “Đã hạch toán”; giá trị khác bị ép về '
        '“Đang tạo”.',
        '– Với loại chi “Chi thu nhập cho nhân viên”, hệ thống ép phiếu không gắn phiếu đề nghị, '
        'tài khoản có là tài khoản tiền gửi, tiền tệ là đồng Việt Nam và tỷ giá bằng 1, bất kể '
        'giao diện gửi lên giá trị gì.',
    ], ['Tạo mới', 'Chỉnh sửa']),

    ('BR-12', 'Màn hình không có bước duyệt, không in, không xuất Excel', [
        '– Không có thao tác gửi duyệt, duyệt riêng hay huỷ phiếu. Hai trạng thái “Chờ duyệt” và '
        '“Hủy” tồn tại trong hệ thống nhưng không thao tác nào tạo ra chúng.',
        '– Không có chức năng In và Xuất Excel.',
        '– Đây là phạm vi CỐ Ý giữ đúng hệ thống ERP cũ, không phải thiếu sót.',
    ], 'Toàn màn hình'),
])

d.save()
