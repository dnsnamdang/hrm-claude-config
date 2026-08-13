# -*- coding: utf-8 -*-
"""Sinh SRS theo FORM CHUAN cho man 'Danh muc tai khoan' (phan he Tai chinh).

Nguon doi chieu (doc truc tiep tu code):
  BE  Modules/Finance/{Routes/api.php, Entities/Account/Account.php,
                       Http/Requests/Account/AccountRequest.php,
                       Http/Controllers/V1/AccountController.php}
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
  FE  hrm-client/pages/finance/accounts/{index.vue, add.vue, print.vue,
                                         _id/edit.vue, components/AccountFormComponent.vue}
      hrm-client/components/subsystem-menu/finance.js
"""
import os
import sys

# Console Windows mac dinh cp1252 -> print() chuoi tieng Viet se nem UnicodeEncodeError.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 2 module dung chung (srs_docx_lib, srs_uml_render) nam trong assets cua skill srs-documenter
# -> di theo repo, ai clone ve cung chay duoc.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "srs-documenter", "assets"))
from srs_docx_lib import SrsDoc, ACTOR_P1, ACTOR_BOTH  # noqa: E402

OUT = (r"d:\CompanyProject\hrm\hrm-claude-config\hrm\.plans\gop-db"
       r"\finance-account-catalog\SRS - Danh mục tài khoản.docx")

d = SrsDoc(
    out=OUT,
    menu='Phân hệ Tài chính → Danh mục → Danh mục tài khoản',
    route='/finance/accounts',
    full_url='https://<host-hrm>/finance/accounts',
    img_prefix='acc_')

# ================================================================ TRANG BIA
d.h1('SOFTWARE REQUIREMENTS SPECIFICATION (SRS)')
d.h2('Màn hình: Danh mục tài khoản')
d.h2('Phân hệ: Tài chính – nhóm Danh mục')

d.info_table([
    ('Mã màn hình', 'TC-DM-ACCOUNT'),
    ('Đường dẫn', '/finance/accounts'),
    ('Phiên bản', '1.0'),
    ('Ngày lập', '12/08/2026'),
    ('Người lập', '@junfoke'),
    ('Trạng thái tài liệu', 'Draft'),
    ('Nguồn đối chiếu', 'Màn ERP admin/accounting/account (bảng accounts trên DB gộp)'),
])

# ================================================================ 1. GIOI THIEU
d.h1('1. Giới thiệu')

d.h2('1.1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm (SRS) cho màn hình quản lý danh mục tài khoản kế toán, '
    'nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa BA/PO/Dev/Test',
    'Là căn cứ nghiệm thu chức năng và phân quyền',
    'Làm rõ ràng buộc của cây tài khoản 3 bậc — điều kiện chọn tài khoản mẹ, quy tắc đánh số '
    'và các trường hợp bị chặn sửa/xoá',
    'Làm rõ điều kiện “chỉ người tạo mới được khoá/xoá” kế thừa từ hệ thống ERP',
])

d.h2('1.2 Phạm vi')
d.p('Màn hình Danh mục tài khoản cung cấp chức năng:')
d.bullets([
    'Xem danh sách tài khoản dưới dạng cây 3 bậc, tìm kiếm nhanh và lọc nâng cao theo 8 tiêu chí',
    'Thêm mới và chỉnh sửa tài khoản trên màn hình riêng, có kiểm tra ràng buộc cây tài khoản',
    'Khoá / Mở khoá tài khoản',
    'Xoá tài khoản khi thoả điều kiện ràng buộc',
    'Xem lịch sử chỉnh sửa của từng tài khoản',
    'Xuất danh sách ra file Excel và In danh sách',
    'Nhập dữ liệu hàng loạt từ file Excel, có bước kiểm tra dữ liệu trước khi ghi',
])
d.p('Ngoài phạm vi:')
d.bullets([
    'Thay đổi cấu trúc bảng dữ liệu: giữ nguyên dữ liệu dùng chung với hệ thống ERP đang chạy song song',
    'Phân quyền theo cấp (tổng công ty / công ty / phòng ban): danh mục dùng chung toàn hệ thống',
    'Trường “Ghi chú” có trên form ERP — dữ liệu gốc không có cột này nên màn hình HRM bỏ hẳn',
    'Cây tài khoản sâu hơn 3 bậc',
])

d.h2('1.3 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Tài khoản', 'Một tài khoản kế toán trong hệ thống tài khoản của doanh nghiệp'),
    ('Số tài khoản', 'Chuỗi chữ số định danh tài khoản, duy nhất trong toàn danh mục'),
    ('Bậc tài khoản', 'Vị trí của tài khoản trên cây: bậc 1 là tài khoản tổng, bậc 2 và 3 là '
                      'tài khoản chi tiết'),
    ('Tài khoản mẹ', 'Tài khoản ở bậc liền trên, chứa tài khoản hiện tại'),
    ('Tài khoản con', 'Tài khoản ở bậc liền dưới, có tài khoản hiện tại làm tài khoản mẹ'),
    ('Loại tài khoản', 'Phân loại theo bản chất kế toán (tài sản, nợ phải trả, doanh thu…)'),
    ('Theo dõi công nợ', 'Cờ đánh dấu tài khoản có theo dõi chi tiết công nợ hay không'),
    ('Lịch sử chỉnh sửa', 'Danh sách các lần thay đổi thông tin tài khoản, ghi rõ giá trị trước '
                          'và sau'),
    ('P1', 'Quyền “Quản lý danh mục tài khoản”'),
    ('P2', 'Quyền “Xem danh mục tài khoản”'),
    ('Quick Search', 'Tìm kiếm nhanh'),
    ('Advanced Filter', 'Bộ lọc nâng cao'),
    ('SRS', 'Software Requirements Specification'),
], widths=[1.8, 4.2])

# ================================================================ 2. TONG QUAN
d.h1('2. Tổng quan')

d.h2('2.1 Bối cảnh nghiệp vụ')
d.p('Danh mục tài khoản là xương sống của toàn bộ nghiệp vụ kế toán, dùng để:')
d.bullets([
    'Cung cấp hệ thống tài khoản cho các bút toán hạch toán',
    'Xác định tài khoản nào cần theo dõi chi tiết công nợ',
    'Phân loại số liệu theo bản chất kế toán để lên báo cáo tài chính',
])
d.p('Do đó cần:')
d.bullets([
    'Bảo đảm cây tài khoản luôn nhất quán: tài khoản con phải nối tiếp số của tài khoản mẹ và '
    'nằm đúng bậc liền dưới',
    'Ngăn thao tác làm mồ côi tài khoản con: không cho đổi bậc hoặc đổi số của tài khoản đang có con',
    'Ngăn xoá tài khoản đã phát sinh số liệu hạch toán',
    'Ghi lại lịch sử chỉnh sửa để truy vết khi số liệu kế toán có sai lệch',
    'Hỗ trợ nhập liệu hàng loạt vì hệ thống tài khoản thường được khai báo một lần với số lượng lớn',
])

d.h2('2.2 Nhóm người dùng')
d.bullets([
    'Người dùng có quyền P1: được quản lý danh mục (thêm/sửa/khoá/xoá/nhập từ Excel) và xem lịch sử',
    'Người dùng có quyền P2: chỉ được xem/tra cứu, xem lịch sử, xuất Excel và in danh sách',
    'Người dùng không có P1/P2: bị chặn truy cập',
])

# ================================================================ 3. PHAN QUYEN
d.h1('3. Phân quyền và kiểm soát truy cập')

d.h2('3.1 Danh sách quyền')
d.table(['Ký hiệu', 'Tên quyền', 'Mã quyền', 'Nhóm quyền'], [
    ('P1', 'Quản lý danh mục tài khoản', '1107', 'Danh mục tài chính'),
    ('P2', 'Xem danh mục tài khoản', '1108', 'Danh mục tài chính'),
], widths=[0.8, 2.8, 0.9, 1.5])
d.p('Ghi chú: màn hình tương ứng bên ERP không gate quyền nào, hai quyền trên là quyền mới của HRM.')

d.h2('3.2 Quy tắc truy cập bắt buộc')
d.bullets([
    'Chỉ user có P1 hoặc P2 mới được truy cập màn hình.',
    'User không có P1/P2: không hiển thị menu điều hướng tới màn hình.',
    'User không có P1/P2: truy cập trực tiếp URL bị chặn, gọi API trả về lỗi 403.',
    'User chỉ có P2: mọi thao tác ghi (thêm/sửa/khoá/mở khoá/xoá/nhập Excel) bị chặn ở cả giao diện '
    'lẫn API (403), không phụ thuộc vào việc giao diện có ẩn nút hay không.',
    'Ngoài quyền P1, thao tác Khoá / Mở khoá / Xoá còn yêu cầu người thực hiện chính là người đã '
    'tạo ra tài khoản đó — quy tắc kế thừa từ hệ thống ERP.',
    'Danh sách rút gọn phục vụ ô chọn tài khoản ở các màn khác không gate quyền, vì nhiều màn '
    'nghiệp vụ đều cần đọc danh sách này.',
])

d.h2('3.3 Ma trận phân quyền')
d.table(['Chức năng', 'P1', 'P2', 'Không có quyền'], [
    ('Truy cập màn', '✅', '✅', '❌'),
    ('Xem danh sách', '✅', '✅', '❌'),
    ('Tìm kiếm nhanh / Lọc nâng cao / Phân trang', '✅', '✅', '❌'),
    ('Xem lịch sử chỉnh sửa', '✅', '✅', '❌'),
    ('Thêm mới', '✅', '❌', '❌'),
    ('Chỉnh sửa', '✅', '❌', '❌'),
    ('Khoá / Mở khoá (chỉ người tạo)', '✅', '❌', '❌'),
    ('Xoá (chỉ người tạo)', '✅', '❌', '❌'),
    ('Nhập từ Excel', '✅', '❌', '❌'),
    ('Xuất Excel / In danh sách', '✅', '✅', '❌'),
], widths=[3.0, 0.8, 0.8, 1.4])

# ================================================================ 4. FUNCTION LIST
d.h1('4. Danh mục chức năng (Function list)')
d.table(['ID', 'Chức năng', 'Mô tả đặc tả thu nhỏ (Mini-Spec)', 'Quyền'], [
    ('FR-01', 'Truy cập màn hình',
     'Kiểm tra quyền P1/P2. Không có quyền sẽ bị chặn (ẩn menu, chặn URL, API trả 403).', 'P1, P2'),
    ('FR-02', 'Xem danh sách',
     'Hiển thị bảng 11 cột với 3 cột số tài khoản tách theo bậc, sắp xếp theo thứ tự cây tài khoản, '
     'có phân trang.', 'P1, P2'),
    ('FR-03', 'Tìm kiếm & Lọc',
     'Kết hợp Quick Search và Advanced Filter theo 8 tiêu chí: Số tài khoản, Tên, Bậc, Loại, '
     'Theo dõi công nợ, Trạng thái, Người tạo, Người cập nhật.', 'P1, P2'),
    ('FR-04', 'Thêm mới',
     'Màn hình riêng. Nhập Số tài khoản (*), Bậc (*), Tài khoản mẹ (*, với bậc 2-3), Tên (*), '
     'Loại (*), Theo dõi công nợ, Trạng thái. Kiểm tra ràng buộc cây tài khoản.', 'P1'),
    ('FR-05', 'Chỉnh sửa',
     'Màn hình riêng, nạp sẵn dữ liệu. Tài khoản đang có tài khoản con bị chặn đổi Bậc và '
     'Số tài khoản.', 'P1'),
    ('FR-06', 'Khoá / Mở khoá',
     'Đổi trạng thái sau khi xác nhận. Chỉ người tạo tài khoản mới thực hiện được.', 'P1'),
    ('FR-07', 'Xoá',
     'Xoá bản ghi sau khi xác nhận. Chặn khi không phải người tạo, khi tài khoản còn tài khoản con, '
     'hoặc khi đã phát sinh số liệu hạch toán.', 'P1'),
    ('FR-08', 'Xem lịch sử chỉnh sửa',
     'Mở modal liệt kê các lần thay đổi, mỗi lần nêu rõ trường thay đổi kèm giá trị trước và sau.',
     'P1, P2'),
    ('FR-09', 'Xuất Excel',
     'Xuất danh sách theo đúng bộ lọc đang áp dụng ra file Excel.', 'P1, P2'),
    ('FR-10', 'Nhập từ Excel',
     'Tải file mẫu 6 cột, dán/nhập dữ liệu, kiểm tra trước khi ghi rồi nhập hàng loạt.', 'P1'),
    ('FR-11', 'In danh sách',
     'Mở màn hình in danh sách theo bộ lọc đang áp dụng.', 'P1, P2'),
], widths=[0.7, 1.4, 3.4, 0.8])

# ================================================================ 5. DAC TA CHI TIET
d.h1('5. Đặc tả chi tiết theo từng chức năng (FUNCTIONAL PACKAGING)')

d.h2('5.1 Sơ đồ UML tổng quan')
d.p('Sơ đồ Use Case tổng quan của màn hình, thể hiện quan hệ giữa hai nhóm người dùng và '
    'mười một chức năng:')
d.overview_figure(
    'HỆ THỐNG HRM — Danh mục tài khoản',
    [(ACTOR_P1, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
     ('Người xem danh mục (P2)', [0, 1, 2, 7, 8, 10])],
    [('FR-01', 'Truy cập màn hình', 'view', None),
     ('FR-02', 'Xem danh sách', 'view', None),
     ('FR-03', 'Tìm kiếm & Lọc', 'view', None),
     ('FR-04', 'Thêm mới', 'crud', None),
     ('FR-05', 'Chỉnh sửa', 'crud', None),
     ('FR-06', 'Khoá / Mở khoá', 'action', None),
     ('FR-07', 'Xoá', 'action', '«include» Kiểm tra ràng buộc cây và số liệu'),
     ('FR-08', 'Xem lịch sử chỉnh sửa', 'view', None),
     ('FR-09', 'Xuất Excel', 'io', None),
     ('FR-10', 'Nhập từ Excel', 'io', None),
     ('FR-11', 'In danh sách', 'io', None)],
    'Sơ đồ Use Case tổng quan màn hình Danh mục tài khoản')

d.h2('5.2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------ 5.2.1
d.h2('5.2.1 Truy cập màn hình danh mục tài khoản')

d.h3('5.2.1.1 Biểu đồ Usecase')
d.uc_figure('FR-01', 'Truy cập màn hình danh mục tài khoản', 'view',
            [('include', 'Kiểm tra quyền truy cập')], actor=ACTOR_BOTH)

d.h3('5.2.1.2 Giới thiệu')
d.intro_table(
    'Truy cập màn hình danh mục tài khoản',
    'Cho phép người dùng truy cập vào màn hình quản lý danh mục tài khoản kế toán để tra cứu '
    'và quản lý hệ thống tài khoản.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng đã đăng nhập thành công vào hệ thống.',
    '1. Người dùng chọn menu Tài chính → Danh mục → Danh mục tài khoản.\n'
    '2. Hệ thống xác thực quyền truy cập (P1 hoặc P2).\n'
    '3. Hệ thống điều hướng tới màn hình danh sách và tải dữ liệu trang đầu tiên.\n'
    '4. Hệ thống khôi phục bộ lọc đã lưu của lần truy cập trước (nếu còn hiệu lực).',
    '• Người dùng không có quyền → Hệ thống ẩn menu; truy cập trực tiếp URL bị chặn.\n'
    '• Gọi trực tiếp API khi không có quyền → Hệ thống trả về lỗi 403.',
    '')

d.h3('5.2.1.3 Layout màn hình')
d.layout('Ghi chú: tài liệu này không đính kèm ảnh chụp màn hình, người đọc truy cập trực tiếp '
         'đường dẫn trên để đối chiếu giao diện.')

d.h3('5.2.1.4 Tiêu chí nghiệm thu')
d.p('Người dùng có quyền truy cập:')
d.bullets([
    'Nhìn thấy menu Danh mục tài khoản.',
    'Truy cập được màn hình danh sách.',
    'Hiển thị mặc định: danh sách phải hiển thị đúng cấu trúc bảng gồm STT, Cấp 1, Cấp 2, Cấp 3, '
    'Tên tài khoản, Loại tài khoản, Theo dõi công nợ, Ngày tạo, Cập nhật, Trạng thái, Hành động.',
])
d.p('Người dùng không có quyền:')
d.bullets([
    'Không nhìn thấy menu.',
    'Truy cập trực tiếp URL bị chặn, gọi API trả về 403.',
])

d.h3('5.2.1.5 Danh sách event và xử lý event')
d.event_table([
    ('Click menu Danh mục tài khoản', 'Click',
     'Kiểm tra quyền (P1 hoặc P2) và điều hướng tới màn hình danh sách.'),
    ('Truy cập URL trực tiếp', 'System',
     'Kiểm tra quyền; nếu không hợp lệ → chặn truy cập (giao diện) và trả về lỗi 403 (API).'),
    ('Load màn hình', 'System', 'Khôi phục bộ lọc đã lưu và tải danh sách trang 1.'),
])

# ------------------------------------------------ 5.2.2
d.h2('5.2.2 Xem danh sách tài khoản')

d.h3('5.2.2.1 Giới thiệu')
d.intro_table(
    'Xem danh sách tài khoản',
    'Hiển thị danh sách tài khoản kế toán theo cấu trúc cây 3 bậc, kèm loại tài khoản, cờ theo dõi '
    'công nợ, thông tin người tạo/người cập nhật và trạng thái.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng truy cập thành công màn hình danh mục tài khoản.',
    '1. Hệ thống lấy danh sách tài khoản theo bộ lọc hiện tại.\n'
    '2. Hệ thống sắp xếp theo thứ tự cây tài khoản để tài khoản con luôn nằm ngay dưới tài khoản mẹ.\n'
    '3. Hệ thống hiển thị số tài khoản ở đúng cột bậc tương ứng (Cấp 1 / Cấp 2 / Cấp 3).\n'
    '4. Hệ thống hiển thị danh sách theo phân trang.',
    '• Không có dữ liệu → Hiển thị danh sách trống kèm thông báo không có dữ liệu.\n'
    '• Tài khoản chưa có loại → Cột Loại tài khoản để trống.\n'
    '• Tài khoản chưa từng được cập nhật → Cột Cập nhật để trống.',
    '• Số tài khoản chỉ hiển thị ở đúng một trong ba cột Cấp 1 / Cấp 2 / Cấp 3 theo bậc của nó, '
    'nhờ đó bảng phẳng vẫn đọc được như cây.\n'
    '• Danh sách hiển thị cả tài khoản Hoạt động lẫn tài khoản Khoá.')

d.h3('5.2.2.2 Layout màn hình')
d.layout()

d.h3('5.2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Bảng danh sách tài khoản', 'Table/Grid', 'Enable', '–', '–', '–',
     'Hiển thị danh sách tài khoản theo phân trang'),
    ('STT', 'Label', 'Enable', '–', '–', '–', 'Số thứ tự bản ghi, tính theo trang hiện tại'),
    ('Cấp 1', 'Text', 'Enable', '3 – 15 chữ số', '–', 'Lấy từ hệ thống',
     'Số tài khoản, chỉ hiển thị khi tài khoản ở bậc 1'),
    ('Cấp 2', 'Text', 'Enable', '3 – 15 chữ số', '–', 'Lấy từ hệ thống',
     'Số tài khoản, chỉ hiển thị khi tài khoản ở bậc 2'),
    ('Cấp 3', 'Text', 'Enable', '3 – 15 chữ số', '–', 'Lấy từ hệ thống',
     'Số tài khoản, chỉ hiển thị khi tài khoản ở bậc 3'),
    ('Tên tài khoản', 'Text', 'Enable', '0–255 ký tự', '–', 'Lấy từ hệ thống',
     'Tên đầy đủ của tài khoản, tự xuống dòng khi dài'),
    ('Loại tài khoản', 'Text', 'Enable', 'Danh sách', '–', 'Lấy từ hệ thống',
     'Phân loại theo bản chất kế toán'),
    ('Theo dõi công nợ', 'Badge', 'Enable', 'Có / Không', '–', 'Không',
     'Đánh dấu tài khoản có theo dõi chi tiết công nợ'),
    ('Ngày tạo', 'Text', 'Enable', 'dd/mm/yyyy', '–', 'Lấy từ hệ thống',
     'Ngày tạo kèm tên người tạo'),
    ('Cập nhật', 'Text', 'Enable', 'dd/mm/yyyy', '–', 'Lấy từ hệ thống',
     'Ngày cập nhật gần nhất kèm tên người cập nhật; để trống nếu chưa từng cập nhật'),
    ('Trạng thái', 'Badge', 'Enable', 'Hoạt động / Khoá', '–', 'Hoạt động', 'Trạng thái tài khoản'),
    ('Khoá / Mở khoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Ẩn khi không có P1; vô hiệu hoá khi người dùng không phải người tạo hoặc trạng thái không '
     'cho phép, chú giải nêu rõ lý do'),
    ('Lịch sử chỉnh sửa', 'Icon Button', 'Enable', '–', '–', '–',
     'Mở modal xem lịch sử thay đổi của tài khoản'),
    ('Sửa', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Chuyển sang màn hình chỉnh sửa. Ẩn khi không có P1'),
    ('Xoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Ẩn khi không có P1; vô hiệu hoá khi không đủ điều kiện xoá, chú giải nêu rõ lý do'),
    ('Tạo mới', 'Button', 'Enable / Ẩn', '–', '–', '–',
     'Chuyển sang màn hình thêm mới. Ẩn khi không có P1'),
    ('In danh sách', 'Button', 'Enable', '–', '–', '–', 'Mở màn hình in theo bộ lọc hiện tại'),
    ('Xuất Excel', 'Button', 'Enable', '–', '–', '–', 'Tải file Excel theo bộ lọc hiện tại'),
    ('Import Excel', 'Button', 'Enable / Ẩn', '–', '–', '–',
     'Mở modal nhập dữ liệu hàng loạt. Ẩn khi không có P1'),
    ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1', 'Điều hướng giữa các trang danh sách'),
    ('Chọn số dòng/trang', 'Dropdown', 'Enable', 'Danh sách', 'Không', '10',
     'Thay đổi số bản ghi hiển thị mỗi trang'),
    ('Trạng thái rỗng', 'Label', 'Enable', '–', '–', 'Ẩn', 'Hiển thị khi danh sách trống'),
    ('Loading', 'Loading', 'Hiển thị', '–', '–', 'Ẩn', 'Hiển thị trong lúc chờ tải danh sách'),
])

d.h3('5.2.2.4 Tiêu chí nghiệm thu')
d.bullets([
    'Số tài khoản bậc 1 chỉ hiện ở cột Cấp 1, bậc 2 chỉ ở cột Cấp 2, bậc 3 chỉ ở cột Cấp 3.',
    'Tài khoản con luôn nằm ngay dưới tài khoản mẹ trong danh sách.',
    'Danh sách hiển thị đủ cả tài khoản Hoạt động lẫn tài khoản Khoá.',
    'Cột Theo dõi công nợ hiển thị nhãn tiếng Việt, không hiển thị giá trị số 0/1.',
    'Nút Khoá / Xoá bị vô hiệu hoá với tài khoản do người khác tạo, chú giải nêu rõ lý do.',
    'Vào màn hình chỉ phát sinh đúng một yêu cầu tải danh sách, không tải lặp.',
    'Phân trang hoạt động đúng, không trùng hoặc thiếu dữ liệu.',
])

d.h3('5.2.2.5 Danh sách event và xử lý event')
d.event_table([
    ('Load danh sách', 'System',
     'Tải danh sách theo bộ lọc và phân trang hiện tại; hiển thị hiệu ứng chờ trong lúc tải.'),
    ('Đổi trang', 'Click', 'Tải lại danh sách theo trang mới, giữ nguyên bộ lọc.'),
    ('Đổi số dòng/trang', 'Change', 'Tải lại danh sách với số dòng mới, quay về trang 1.'),
    ('Rê chuột lên nút bị vô hiệu hoá', 'Hover', 'Hiển thị chú giải nêu lý do không thao tác được.'),
])

# ------------------------------------------------ 5.2.3
d.h2('5.2.3 Tìm kiếm và lọc danh sách tài khoản')

d.h3('5.2.3.1 Giới thiệu')
d.intro_table(
    'Tìm kiếm và lọc danh sách tài khoản',
    'Cho phép người dùng thu hẹp danh sách tài khoản theo từ khoá hoặc theo nhiều tiêu chí kết hợp.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng đang ở màn hình danh sách tài khoản.',
    '1. Người dùng nhập từ khoá vào ô tìm kiếm nhanh hoặc mở bộ lọc nâng cao.\n'
    '2. Người dùng nhập/chọn các tiêu chí: Số tài khoản, Tên tài khoản, Bậc tài khoản, '
    'Loại tài khoản, Theo dõi công nợ, Trạng thái, Người tạo, Người cập nhật.\n'
    '3. Người dùng bấm Tìm kiếm.\n'
    '4. Hệ thống lấy danh sách khớp điều kiện, quay về trang 1 và hiển thị kết quả.',
    '• Bấm Làm mới → Hệ thống xoá toàn bộ điều kiện lọc và tải lại danh sách đầy đủ.\n'
    '• Không có kết quả → Hiển thị danh sách trống kèm thông báo.\n'
    '• Thay đổi tiêu chí ở bộ lọc nâng cao → Hệ thống tự tìm lại ngay, không cần bấm Tìm kiếm.',
    '• Tìm theo tên là tìm gần đúng ở bất kỳ vị trí nào trong tên — khác màn ERP cũ vốn chỉ khớp '
    'phần đuôi của tên.\n'
    '• Điều kiện lọc được ghi nhớ và dùng lại khi quay về màn hình.')

d.h3('5.2.3.2 Layout màn hình')
d.layout()

d.h3('5.2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Khung bộ lọc', 'Modal', 'Enable', '–', '–', 'Thu gọn',
     'Khung “Bộ lọc danh mục tài khoản”, có thể mở rộng / thu gọn'),
    ('Tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo số tài khoản hoặc tên tài khoản'),
    ('Số tài khoản', 'Textbox', 'Enable', '0–15 chữ số', 'Không', 'Trống', 'Lọc theo một phần của số tài khoản'),
    ('Tên tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Lọc theo một phần của tên'),
    ('Bậc tài khoản', 'Dropdown', 'Enable', '1 / 2 / 3', 'Không', 'Trống', 'Lọc theo bậc trên cây'),
    ('Loại tài khoản', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Lọc theo phân loại kế toán'),
    ('Theo dõi công nợ', 'Dropdown', 'Enable', 'Có / Không', 'Không', 'Trống', 'Lọc theo cờ theo dõi công nợ'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khoá', 'Không', 'Trống',
     'Lọc theo trạng thái; để trống là lấy tất cả'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Lọc theo người tạo bản ghi'),
    ('Người cập nhật', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Lọc theo người cập nhật gần nhất'),
    ('Tìm kiếm', 'Button', 'Enable', '–', '–', '–', 'Áp dụng bộ lọc và quay về trang 1'),
    ('Làm mới', 'Button', 'Enable', '–', '–', '–', 'Xoá toàn bộ điều kiện lọc và tải lại danh sách'),
])

d.h3('5.2.3.4 Tiêu chí nghiệm thu')
d.bullets([
    'Tìm kiếm nhanh tìm được theo cả số tài khoản và tên tài khoản.',
    'Tìm theo tên khớp cả khi từ khoá nằm ở giữa tên, không chỉ ở cuối tên.',
    'Từ khoá chứa ký tự đặc biệt của phép tìm gần đúng vẫn được tìm như ký tự thông thường.',
    'Kết hợp nhiều tiêu chí cho ra kết quả thoả mãn đồng thời tất cả tiêu chí.',
    'Bấm Tìm kiếm luôn quay về trang 1.',
    'Bấm Làm mới thì danh sách được tải lại đầy đủ, không giữ điều kiện cũ.',
])

d.h3('5.2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Nhập ô tìm kiếm nhanh', 'Keypress', 'Ghi nhận từ khoá, chưa gọi tìm kiếm.'),
    ('Bấm Tìm kiếm', 'Click', 'Quay về trang 1 và tải lại danh sách theo toàn bộ điều kiện lọc.'),
    ('Đổi tiêu chí lọc nâng cao', 'Change',
     'Quay về trang 1 và tải lại danh sách ngay theo điều kiện mới.'),
    ('Bấm Làm mới', 'Click', 'Xoá toàn bộ điều kiện lọc, quay về trang 1 và tải lại danh sách.'),
])

# ------------------------------------------------ 5.2.4
d.h2('5.2.4 Thêm mới tài khoản')

d.h3('5.2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Thêm mới tài khoản', 'crud',
            [('include', 'Kiểm tra trùng số tài khoản'),
             ('include', 'Kiểm tra ràng buộc cây tài khoản')])

d.h3('5.2.4.2 Giới thiệu')
d.intro_table(
    'Thêm mới tài khoản',
    'Cho phép người quản lý danh mục khai báo một tài khoản kế toán mới và gắn nó vào đúng vị trí '
    'trên cây tài khoản.',
    'Admin; User được phân quyền P1',
    'Người dùng đang ở màn hình danh sách và có quyền quản lý danh mục tài khoản.',
    '1. Người dùng bấm nút Tạo mới → Hệ thống mở màn hình thêm mới tài khoản.\n'
    '2. Người dùng nhập Số tài khoản và chọn Bậc tài khoản.\n'
    '3. Với bậc 2 và bậc 3, người dùng chọn Tài khoản mẹ trong danh sách tài khoản bậc liền trên '
    'đang hoạt động.\n'
    '4. Người dùng nhập Tên tài khoản, chọn Loại tài khoản, đánh dấu Theo dõi công nợ nếu cần '
    'và chọn Trạng thái.\n'
    '5. Người dùng bấm Lưu.\n'
    '6. Hệ thống kiểm tra hợp lệ và ràng buộc cây tài khoản rồi ghi bản ghi mới.\n'
    '7. Hệ thống hiển thị thông báo thành công và quay về màn hình danh sách.',
    '• Người dùng bấm Lưu & Thêm tiếp → Hệ thống lưu bản ghi rồi giữ nguyên màn hình với các '
    'trường trống để nhập tiếp.\n'
    '• Người dùng bấm Quay lại → Hệ thống trở về danh sách, không lưu gì.\n'
    '• Chọn bậc 1 → Hệ thống vô hiệu hoá ô Tài khoản mẹ vì tài khoản bậc 1 nằm ở gốc cây.\n'
    '• Dữ liệu không hợp lệ → Hệ thống hiển thị lỗi ngay dưới từng trường và không lưu.',
    '• Ô Tài khoản mẹ chỉ liệt kê tài khoản ở bậc liền trên và đang hoạt động.\n'
    '• Số tài khoản của tài khoản con bắt buộc bắt đầu bằng số tài khoản mẹ; đây là cơ sở để hệ '
    'thống sắp xếp đúng cây tài khoản.')

d.h3('5.2.4.3 Layout màn hình')
d.p('Đường dẫn màn hình:')
d.bullets([
    'Menu: Phân hệ Tài chính → Danh mục → Danh mục tài khoản → nút Tạo mới',
    'Route (FE): /finance/accounts/add',
    'URL đầy đủ: https://<host-hrm>/finance/accounts/add',
])

d.h3('5.2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Số tài khoản', 'Textbox', 'Enable', '3 – 15 chữ số', 'Có', 'Trống',
     'Chỉ nhận chữ số, không được trùng với tài khoản khác'),
    ('Bậc tài khoản', 'Dropdown', 'Enable', '1 / 2 / 3', 'Có', 'Trống',
     'Bậc 1 là tài khoản tổng, bậc 2-3 là tài khoản chi tiết'),
    ('Tài khoản mẹ', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Có với bậc 2 và 3', 'Trống',
     'Chỉ liệt kê tài khoản bậc liền trên đang hoạt động; vô hiệu hoá khi chọn bậc 1'),
    ('Tên tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống', 'Tên đầy đủ của tài khoản'),
    ('Loại tài khoản', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Trống', 'Phân loại theo bản chất kế toán'),
    ('Theo dõi công nợ', 'Badge', 'Enable', 'Có / Không', 'Không', 'Không',
     'Đánh dấu tài khoản có theo dõi chi tiết công nợ'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khoá', 'Không', 'Hoạt động', 'Trạng thái sử dụng'),
    ('Ghi chú hướng dẫn theo trường', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     'Giải thích ngắn ngay dưới ô nhập, ví dụ điều kiện chọn tài khoản mẹ'),
    ('Lưu', 'Button', 'Enable', '–', '–', '–', 'Kiểm tra hợp lệ và ghi bản ghi mới'),
    ('Lưu & Thêm tiếp', 'Button', 'Enable', '–', '–', '–',
     'Ghi bản ghi và giữ màn hình để nhập tiếp; chỉ hiển thị ở chế độ thêm mới'),
    ('Quay lại', 'Button', 'Enable', '–', '–', '–', 'Trở về màn hình danh sách, không lưu'),
    ('Thông báo lỗi theo trường', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị ngay dưới trường tương ứng'),
])

d.h3('5.2.4.5 Tiêu chí nghiệm thu')
d.bullets([
    'Bỏ trống Số tài khoản / Tên / Bậc / Loại thì không lưu được và hiển thị lỗi tương ứng.',
    'Nhập số tài khoản đã tồn tại thì hiển thị lỗi “Số tài khoản đã tồn tại”.',
    'Nhập số tài khoản có chữ cái hoặc ít hơn 3 chữ số thì bị chặn với thông báo rõ ràng.',
    'Chọn bậc 2 hoặc bậc 3 mà không chọn Tài khoản mẹ thì bị chặn.',
    'Chọn tài khoản mẹ không thuộc bậc liền trên thì bị chặn kèm thông báo nêu rõ bậc hiện tại '
    'của tài khoản mẹ.',
    'Nhập số tài khoản con không bắt đầu bằng số tài khoản mẹ thì bị chặn kèm ví dụ minh hoạ.',
    'Chọn bậc 1 thì ô Tài khoản mẹ bị vô hiệu hoá.',
    'Bấm Lưu & Thêm tiếp thì màn hình vẫn ở chế độ thêm mới với các trường trống.',
    'Người dùng chỉ có P2 gọi trực tiếp API tạo mới thì bị từ chối với lỗi 403.',
])

d.h3('5.2.4.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tạo mới', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì nút không hiển thị.\n'
     'After:\n– Chuyển sang màn hình thêm mới tài khoản với các trường trống.'),
    ('Chọn Bậc tài khoản', 'Change',
     'Bậc 1 → xoá và vô hiệu hoá ô Tài khoản mẹ.\n'
     'Bậc 2 hoặc 3 → nạp lại danh sách tài khoản mẹ theo bậc liền trên.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n'
     '– Số tài khoản trống → hiển thị “Bắt buộc phải nhập”\n'
     '– Số tài khoản sai định dạng → hiển thị “Số tài khoản chỉ được nhập chữ số, từ 3 đến 15 chữ số”\n'
     '– Số tài khoản trùng → hiển thị “Số tài khoản đã tồn tại”\n'
     '– Tên tài khoản trống → hiển thị “Bắt buộc phải nhập”\n'
     '– Bậc tài khoản chưa chọn → hiển thị “Bắt buộc phải chọn”\n'
     '– Loại tài khoản chưa chọn → hiển thị “Bắt buộc phải chọn”\n'
     '– Bậc 2/3 mà chưa chọn tài khoản mẹ → hiển thị “Bắt buộc phải chọn tài khoản mẹ với bậc 2 và 3”\n'
     '– Tài khoản mẹ không đúng bậc liền trên → hiển thị thông báo nêu bậc hiện tại của tài khoản mẹ\n'
     '– Số tài khoản con không bắt đầu bằng số tài khoản mẹ → hiển thị thông báo kèm ví dụ\n'
     '– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Ghi bản ghi mới vào danh mục tài khoản kèm người tạo.\n'
     '– Hiển thị thông báo thành công và quay về màn hình danh sách.'),
    ('Bấm Lưu & Thêm tiếp', 'Click',
     'Xử lý như bấm Lưu; sau khi ghi thành công thì giữ nguyên màn hình và xoá trắng các trường.'),
    ('Bấm Quay lại', 'Click', 'Trở về màn hình danh sách, huỷ dữ liệu đang nhập dở.'),
])

# ------------------------------------------------ 5.2.5
d.h2('5.2.5 Chỉnh sửa tài khoản')

d.h3('5.2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa tài khoản', 'crud',
            [('include', 'Kiểm tra ràng buộc cây tài khoản'),
             ('extend', 'Chặn đổi bậc và số khi đang có tài khoản con')])

d.h3('5.2.5.2 Giới thiệu')
d.intro_table(
    'Chỉnh sửa tài khoản',
    'Cho phép người quản lý danh mục cập nhật thông tin của một tài khoản đã khai báo, '
    'đồng thời bảo vệ tính toàn vẹn của cây tài khoản.',
    'Admin; User được phân quyền P1',
    'Bản ghi tài khoản đang tồn tại; người dùng có quyền quản lý danh mục tài khoản.',
    '1. Người dùng bấm biểu tượng Sửa ở dòng cần chỉnh sửa.\n'
    '2. Hệ thống mở màn hình chỉnh sửa và nạp sẵn dữ liệu hiện tại.\n'
    '3. Hệ thống kiểm tra tài khoản có tài khoản con hay không để quyết định khoá bớt trường nhập.\n'
    '4. Người dùng chỉnh sửa các trường cần thay đổi.\n'
    '5. Người dùng bấm Lưu.\n'
    '6. Hệ thống kiểm tra hợp lệ, ghi cập nhật và ghi nhận lịch sử thay đổi.\n'
    '7. Hệ thống hiển thị thông báo thành công và quay về màn hình danh sách.',
    '• Tài khoản đang có tài khoản con → Hệ thống vô hiệu hoá ô Bậc tài khoản và Số tài khoản, '
    'kèm ghi chú nêu rõ lý do.\n'
    '• Bản ghi đã bị xoá bởi người dùng khác → Hệ thống báo dữ liệu đã thay đổi và yêu cầu tải lại.\n'
    '• Người dùng bấm Quay lại → Hệ thống trở về danh sách, huỷ thay đổi chưa lưu.',
    '• Không cho đổi Bậc và Số tài khoản khi tài khoản đang có tài khoản con: cây chỉ có 3 bậc nên '
    'không thể đẩy các tài khoản con xuống, còn đổi số sẽ làm tài khoản con mất liên kết với '
    'tài khoản mẹ.\n'
    '• Mọi thay đổi trên 7 trường được theo dõi đều được ghi vào lịch sử chỉnh sửa.')

d.h3('5.2.5.3 Layout màn hình')
d.p('Đường dẫn màn hình:')
d.bullets([
    'Menu: Phân hệ Tài chính → Danh mục → Danh mục tài khoản → biểu tượng Sửa ở dòng dữ liệu',
    'Route (FE): /finance/accounts/{id}/edit',
    'URL đầy đủ: https://<host-hrm>/finance/accounts/{id}/edit',
])

d.h3('5.2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Số tài khoản', 'Textbox', 'Enable / Disable', '3 – 15 chữ số', 'Có', 'Lấy từ hệ thống',
     'Vô hiệu hoá khi tài khoản đang có tài khoản con'),
    ('Bậc tài khoản', 'Dropdown', 'Enable / Disable', '1 / 2 / 3', 'Có', 'Lấy từ hệ thống',
     'Vô hiệu hoá khi tài khoản đang có tài khoản con'),
    ('Tài khoản mẹ', 'Dropdown', 'Enable / Disable', 'Danh sách', 'Có với bậc 2 và 3', 'Lấy từ hệ thống',
     'Chỉ liệt kê tài khoản bậc liền trên đang hoạt động'),
    ('Tên tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Lấy từ hệ thống', 'Cho phép sửa'),
    ('Loại tài khoản', 'Dropdown', 'Enable', 'Danh sách', 'Có', 'Lấy từ hệ thống', 'Cho phép sửa'),
    ('Theo dõi công nợ', 'Badge', 'Enable', 'Có / Không', 'Không', 'Lấy từ hệ thống', 'Cho phép bật/tắt'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khoá', 'Không', 'Lấy từ hệ thống', 'Cho phép đổi'),
    ('Ghi chú chặn đổi bậc / số', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện khi tài khoản đang có tài khoản con, nêu rõ số lượng tài khoản con'),
    ('Lưu', 'Button', 'Enable', '–', '–', '–', 'Kiểm tra hợp lệ và cập nhật bản ghi'),
    ('Quay lại', 'Button', 'Enable', '–', '–', '–', 'Trở về danh sách, huỷ thay đổi chưa lưu'),
])

d.h3('5.2.5.5 Tiêu chí nghiệm thu')
d.bullets([
    'Màn hình nạp đúng dữ liệu của tài khoản được chọn.',
    'Tài khoản đang có tài khoản con: ô Bậc và ô Số tài khoản bị vô hiệu hoá kèm ghi chú lý do.',
    'Gọi trực tiếp API cập nhật để đổi bậc hoặc số của tài khoản đang có con vẫn bị chặn kèm '
    'thông báo nêu số lượng tài khoản con.',
    'Đổi số tài khoản trùng với tài khoản khác thì báo lỗi và không lưu.',
    'Giữ nguyên số tài khoản của chính bản ghi đang sửa thì lưu được bình thường.',
    'Sau khi lưu, các trường đã thay đổi phải xuất hiện trong lịch sử chỉnh sửa với giá trị '
    'trước và sau.',
    'Người dùng chỉ có P2 gọi trực tiếp API cập nhật thì bị từ chối với lỗi 403.',
])

d.h3('5.2.5.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Sửa', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì biểu tượng không hiển thị.\n'
     'After:\n– Chuyển sang màn hình chỉnh sửa, nạp dữ liệu và xác định tài khoản có con hay không.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n'
     '– Các lỗi hợp lệ giống chức năng Thêm mới\n'
     '– Tài khoản đang có tài khoản con mà đổi bậc → hiển thị “Tài khoản đang có N tài khoản con '
     'nên không được đổi bậc. Hãy chuyển hoặc xóa các tài khoản con trước.”\n'
     '– Tài khoản đang có tài khoản con mà đổi số tài khoản → hiển thị thông báo tương ứng\n'
     '– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Cập nhật bản ghi kèm người cập nhật.\n'
     '– Ghi lịch sử thay đổi cho các trường được theo dõi.\n'
     '– Hiển thị thông báo thành công và quay về màn hình danh sách.'),
    ('Bấm Quay lại', 'Click', 'Trở về màn hình danh sách, huỷ thay đổi chưa lưu.'),
])

# ------------------------------------------------ 5.2.6
d.h2('5.2.6 Khoá / Mở khoá tài khoản')

d.h3('5.2.6.1 Biểu đồ Usecase')
d.uc_figure('FR-06', 'Khoá / Mở khoá tài khoản', 'action',
            [('include', 'Kiểm tra người tạo và trạng thái')])

d.h3('5.2.6.2 Giới thiệu')
d.intro_table(
    'Khoá / Mở khoá tài khoản',
    'Cho phép người tạo tài khoản ngừng sử dụng tài khoản đó mà vẫn giữ lại toàn bộ số liệu '
    'lịch sử, hoặc cho dùng lại tài khoản đã khoá.',
    'Admin; User được phân quyền P1 và là người đã tạo tài khoản',
    'Bản ghi tài khoản đang tồn tại; người dùng có quyền P1 và là người tạo bản ghi.',
    '1. Người dùng bấm biểu tượng Khoá (hoặc Mở khoá) ở dòng tương ứng.\n'
    '2. Hệ thống hiển thị hộp thoại xác nhận nêu rõ số và tên tài khoản.\n'
    '3. Người dùng xác nhận.\n'
    '4. Hệ thống đổi trạng thái bản ghi và hiển thị thông báo thành công.\n'
    '5. Hệ thống tải lại danh sách.',
    '• Người dùng không phải người tạo tài khoản → Nút bị vô hiệu hoá, chú giải nêu rõ lý do.\n'
    '• Trạng thái hiện tại không phù hợp với hành động → Nút bị vô hiệu hoá.\n'
    '• Người dùng bấm Huỷ → Hệ thống đóng hộp thoại, không thay đổi gì.',
    '• Điều kiện “chỉ người tạo mới được khoá/mở khoá” được kế thừa từ hệ thống ERP để giữ hành vi '
    'thống nhất giữa hai cổng.\n'
    '• Thao tác chỉ thay đổi trạng thái, không ảnh hưởng số liệu hạch toán đã phát sinh.')

d.h3('5.2.6.3 Layout màn hình')
d.layout()

d.h3('5.2.6.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng Khoá / Mở khoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Biểu tượng đổi theo trạng thái hiện tại. Ẩn khi không có P1; vô hiệu hoá khi không đủ điều kiện'),
    ('Chú giải nút', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện khi rê chuột, nêu hành động hoặc lý do bị chặn'),
    ('Hộp thoại xác nhận', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Tiêu đề “Xác nhận khóa” / “Xác nhận mở khóa”, nội dung nêu số và tên tài khoản'),
    ('Nút xác nhận', 'Button', 'Enable', '–', '–', '–', 'Nhãn “Khóa” hoặc “Mở khóa”'),
    ('Huỷ', 'Button', 'Enable', '–', '–', '–', 'Đóng hộp thoại, không thực hiện gì'),
])

d.h3('5.2.6.5 Tiêu chí nghiệm thu')
d.bullets([
    'Tài khoản đang Hoạt động: nút hiển thị hành động Khoá; tài khoản đang Khoá: nút hiển thị '
    'hành động Mở khoá.',
    'Người dùng không phải người tạo tài khoản thì nút bị vô hiệu hoá; gọi trực tiếp API cũng bị chặn.',
    'Xác nhận Khoá thì trạng thái đổi thành Khoá và danh sách hiển thị đúng ngay sau đó.',
    'Bấm Huỷ thì trạng thái giữ nguyên.',
    'Người dùng chỉ có P2 gọi trực tiếp API khoá/mở khoá thì bị từ chối với lỗi 403.',
])

d.h3('5.2.6.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Khoá / Mở khoá', 'Click',
     'Before:\n– Kiểm tra quyền P1 và điều kiện người tạo; không đủ điều kiện thì nút bị vô hiệu hoá.\n'
     'After:\n– Mở hộp thoại xác nhận với nội dung tương ứng hành động.'),
    ('Xác nhận trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền P1 và điều kiện người tạo.\n'
     '– Nếu không đủ điều kiện → hiển thị thông báo từ chối và dừng xử lý.\n'
     'During:\n– Trạng thái hiện tại không phù hợp với hành động → hiển thị thông báo lỗi tương ứng\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Cập nhật trạng thái bản ghi.\n'
     '– Hiển thị thông báo thành công và tải lại danh sách.'),
    ('Bấm Huỷ', 'Click', 'Đóng hộp thoại, không thay đổi trạng thái.'),
])

# ------------------------------------------------ 5.2.7
d.h2('5.2.7 Xoá tài khoản')

d.h3('5.2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Xoá tài khoản', 'action',
            [('include', 'Kiểm tra tài khoản con'),
             ('include', 'Kiểm tra số liệu đã hạch toán')])

d.h3('5.2.7.2 Giới thiệu')
d.intro_table(
    'Xoá tài khoản',
    'Cho phép người tạo xoá một tài khoản khai báo nhầm, với điều kiện tài khoản đó chưa có '
    'tài khoản con và chưa phát sinh số liệu hạch toán.',
    'Admin; User được phân quyền P1 và là người đã tạo tài khoản',
    'Bản ghi tài khoản đang tồn tại; người dùng có quyền P1 và là người tạo bản ghi.',
    '1. Người dùng bấm biểu tượng Xoá ở dòng cần xoá.\n'
    '2. Hệ thống hiển thị hộp thoại xác nhận nêu rõ số và tên tài khoản.\n'
    '3. Người dùng xác nhận.\n'
    '4. Hệ thống kiểm tra lại toàn bộ điều kiện xoá rồi xoá bản ghi.\n'
    '5. Hệ thống hiển thị thông báo thành công và tải lại danh sách.',
    '• Người dùng không phải người tạo → Nút bị vô hiệu hoá, chú giải nêu rõ lý do.\n'
    '• Tài khoản còn tài khoản con → Nút bị vô hiệu hoá, phải xử lý tài khoản con trước.\n'
    '• Tài khoản đã phát sinh số liệu hạch toán → Nút bị vô hiệu hoá, không được xoá.\n'
    '• Người dùng bấm Huỷ → Hệ thống đóng hộp thoại, không xoá gì.',
    '• Ba điều kiện xoá được kiểm tra ở cả giao diện lẫn máy chủ; kiểm tra tại máy chủ là chốt '
    'chặn cuối cùng.\n'
    '• Trường hợp không xoá được, cách xử lý đúng nghiệp vụ là chuyển tài khoản sang trạng thái Khoá.')

d.h3('5.2.7.3 Layout màn hình')
d.layout()

d.h3('5.2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng Xoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Ẩn khi không có P1; vô hiệu hoá khi không đủ một trong ba điều kiện xoá'),
    ('Chú giải nút Xoá', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện khi rê chuột, nêu lý do bị chặn'),
    ('Hộp thoại xác nhận xoá', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Tiêu đề “Xác nhận xóa”, nội dung nêu số và tên tài khoản'),
    ('Xoá', 'Button', 'Enable', '–', '–', '–', 'Xác nhận xoá bản ghi'),
    ('Huỷ', 'Button', 'Enable', '–', '–', '–', 'Đóng hộp thoại, không xoá'),
    ('Thông báo chặn xoá', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Nêu lý do không xoá được'),
])

d.h3('5.2.7.5 Tiêu chí nghiệm thu')
d.bullets([
    'Tài khoản do chính người dùng tạo, không có tài khoản con và chưa phát sinh hạch toán thì '
    'xoá được và biến mất khỏi danh sách.',
    'Tài khoản còn tài khoản con thì không xoá được, kể cả khi gọi trực tiếp API.',
    'Tài khoản đã phát sinh số liệu hạch toán thì không xoá được, kể cả khi gọi trực tiếp API.',
    'Tài khoản do người khác tạo thì không xoá được, kể cả khi gọi trực tiếp API.',
    'Bấm Huỷ ở hộp thoại thì bản ghi vẫn còn nguyên.',
    'Người dùng chỉ có P2 gọi trực tiếp API xoá thì bị từ chối với lỗi 403.',
])

d.h3('5.2.7.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Xoá', 'Click',
     'Before:\n– Kiểm tra quyền P1 và ba điều kiện xoá; không đủ thì nút bị vô hiệu hoá kèm chú giải.\n'
     'After:\n– Mở hộp thoại “Xác nhận xóa”.'),
    ('Xác nhận xoá', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n'
     '– Người thực hiện không phải người tạo → hiển thị thông báo từ chối\n'
     '– Tài khoản còn tài khoản con → hiển thị thông báo yêu cầu xử lý tài khoản con trước\n'
     '– Tài khoản đã phát sinh số liệu hạch toán → hiển thị thông báo không được xoá\n'
     '– Nếu bị chặn → không thực hiện bước After.\n'
     'After:\n– Xoá bản ghi khỏi danh mục tài khoản.\n'
     '– Hiển thị thông báo thành công và tải lại danh sách.'),
    ('Bấm Huỷ', 'Click', 'Đóng hộp thoại, không xoá bản ghi.'),
])

# ------------------------------------------------ 5.2.8
d.h2('5.2.8 Xem lịch sử chỉnh sửa tài khoản')

d.h3('5.2.8.1 Giới thiệu')
d.intro_table(
    'Xem lịch sử chỉnh sửa tài khoản',
    'Hiển thị danh sách các lần thay đổi thông tin của một tài khoản, mỗi lần nêu rõ trường '
    'thay đổi kèm giá trị trước và sau, phục vụ truy vết khi số liệu kế toán có sai lệch.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Bản ghi tài khoản đang tồn tại; người dùng đang ở màn hình danh sách.',
    '1. Người dùng bấm biểu tượng Lịch sử chỉnh sửa ở dòng cần xem.\n'
    '2. Hệ thống mở modal và tải danh sách các lần thay đổi của tài khoản đó.\n'
    '3. Hệ thống hiển thị theo thứ tự mới nhất trước, mỗi lần nêu người thực hiện, thời điểm và '
    'các trường đã đổi.\n'
    '4. Người dùng xem xong thì bấm Đóng.',
    '• Tài khoản chưa từng được chỉnh sửa → Hiển thị thông báo chưa có lịch sử.\n'
    '• Không có quyền → Hệ thống trả về lỗi 403 và không mở modal.',
    'Chỉ 7 trường được theo dõi mới sinh bản ghi lịch sử: Số tài khoản, Tên tài khoản, Tài khoản mẹ, '
    'Bậc tài khoản, Loại tài khoản, Theo dõi công nợ và Trạng thái.')

d.h3('5.2.8.2 Layout màn hình')
d.layout(modal='Lịch sử chỉnh sửa tài khoản')

d.h3('5.2.8.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Modal Lịch sử chỉnh sửa', 'Modal', 'Read-only', '–', '–', 'Ẩn',
     'Tiêu đề “Lịch sử chỉnh sửa tài khoản”'),
    ('Danh sách lần thay đổi', 'Table/Grid', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Mỗi dòng là một lần chỉnh sửa, sắp xếp mới nhất trước'),
    ('Người thực hiện', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống', 'Người đã chỉnh sửa'),
    ('Thời điểm', 'Text', 'Read-only', 'dd/mm/yyyy', '–', 'Lấy từ hệ thống', 'Thời điểm chỉnh sửa'),
    ('Trường thay đổi', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Tên trường bị thay đổi, hiển thị bằng nhãn tiếng Việt'),
    ('Giá trị trước / sau', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Giá trị cũ và giá trị mới, đã quy đổi sang nhãn hiển thị'),
    ('Trạng thái rỗng', 'Label', 'Enable', '–', '–', 'Ẩn', 'Hiển thị khi tài khoản chưa có lịch sử'),
    ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal'),
])

d.h3('5.2.8.4 Tiêu chí nghiệm thu')
d.bullets([
    'Sửa một trường được theo dõi thì lịch sử ghi đúng tên trường, giá trị trước và giá trị sau.',
    'Giá trị của Loại tài khoản, Theo dõi công nợ và Trạng thái hiển thị bằng nhãn tiếng Việt, '
    'không hiển thị giá trị số.',
    'Lịch sử sắp xếp mới nhất trước.',
    'Tài khoản chưa từng chỉnh sửa thì hiển thị thông báo chưa có lịch sử.',
    'Người dùng chỉ có P2 vẫn xem được lịch sử.',
])

d.h3('5.2.8.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Lịch sử chỉnh sửa', 'Click',
     'Tải danh sách lần thay đổi của tài khoản và mở modal ở chế độ chỉ đọc.'),
    ('Bấm Đóng', 'Click', 'Đóng modal.'),
])

# ------------------------------------------------ 5.2.9
d.h2('5.2.9 Xuất Excel danh mục tài khoản')

d.h3('5.2.9.1 Giới thiệu')
d.intro_table(
    'Xuất Excel danh mục tài khoản',
    'Cho phép người dùng tải danh sách tài khoản ra file Excel để đối chiếu hoặc gửi ra ngoài.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng đang ở màn hình danh sách tài khoản.',
    '1. Người dùng áp dụng bộ lọc mong muốn (không bắt buộc).\n'
    '2. Người dùng bấm nút Xuất Excel.\n'
    '3. Hệ thống dựng file theo đúng bộ lọc đang áp dụng và trả về cho trình duyệt tải xuống.',
    '• Không có dữ liệu khớp bộ lọc → Hệ thống vẫn trả file chỉ gồm dòng tiêu đề.\n'
    '• Xảy ra lỗi trong lúc dựng file → Hệ thống hiển thị thông báo lỗi, không tải file.',
    'File xuất ra lấy toàn bộ dữ liệu khớp bộ lọc, không giới hạn theo trang đang xem.')

d.h3('5.2.9.2 Layout màn hình')
d.layout()

d.h3('5.2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Xuất Excel', 'Button', 'Enable', '–', '–', '–', 'Nằm ở thanh thao tác dưới bảng danh sách'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Hiển thị khi không dựng được file'),
])

d.h3('5.2.9.4 Tiêu chí nghiệm thu')
d.bullets([
    'Dữ liệu trong file khớp đúng bộ lọc đang áp dụng trên màn hình.',
    'File chứa toàn bộ bản ghi khớp bộ lọc, không chỉ các dòng của trang đang xem.',
    'Người dùng chỉ có P2 vẫn xuất được Excel.',
    'Người dùng không có quyền gọi trực tiếp đường dẫn xuất Excel thì bị từ chối với lỗi 403.',
])

d.h3('5.2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Kiểm tra quyền P1 hoặc P2; không có quyền → trả về lỗi 403.\n'
     'After:\n– Dựng file Excel theo bộ lọc hiện tại và tải xuống.'),
])

# ------------------------------------------------ 5.2.10
d.h2('5.2.10 Nhập danh mục tài khoản từ Excel')

d.h3('5.2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Nhập danh mục tài khoản từ Excel', 'io',
            [('include', 'Kiểm tra dữ liệu trước khi ghi'),
             ('include', 'Kiểm tra ràng buộc cây tài khoản')])

d.h3('5.2.10.2 Giới thiệu')
d.intro_table(
    'Nhập danh mục tài khoản từ Excel',
    'Cho phép người quản lý danh mục khai báo nhiều tài khoản cùng lúc từ file Excel, '
    'có bước kiểm tra dữ liệu trước khi ghi để tránh nhập sai hàng loạt.',
    'Admin; User được phân quyền P1',
    'Người dùng đang ở màn hình danh sách và có quyền quản lý danh mục tài khoản.',
    '1. Người dùng bấm nút Import Excel → Hệ thống mở modal nhập dữ liệu.\n'
    '2. Người dùng tải file mẫu, điền dữ liệu rồi dán hoặc tải lên bảng nhập gồm 6 cột.\n'
    '3. Người dùng bấm Kiểm tra dữ liệu.\n'
    '4. Hệ thống kiểm tra từng dòng và báo lỗi tại đúng dòng, đúng cột.\n'
    '5. Người dùng sửa các dòng lỗi rồi bấm Nhập dữ liệu.\n'
    '6. Hệ thống ghi các bản ghi hợp lệ và hiển thị kết quả nhập.\n'
    '7. Hệ thống đóng modal và tải lại danh sách.',
    '• Còn dòng lỗi → Hệ thống không cho ghi và yêu cầu sửa hết lỗi trước.\n'
    '• Cột Theo dõi công nợ để trống → Hệ thống hiểu là Không.\n'
    '• Cột Theo dõi công nợ nhập giá trị không hợp lệ → Hệ thống báo lỗi thay vì ngầm hiểu là Không.\n'
    '• Người dùng đóng modal giữa chừng → Hệ thống huỷ toàn bộ dữ liệu đang nhập dở.',
    '• Bảng nhập gồm 6 cột: Số tài khoản (*), Tên tài khoản (*), Bậc (*), Tài khoản mẹ, '
    'Loại tài khoản (*), Theo dõi công nợ.\n'
    '• Tiêu đề cột chấp nhận nhiều cách viết (có dấu, không dấu, viết tắt) để dùng lại được file '
    'mẫu cũ của hệ thống ERP.\n'
    '• Toàn bộ ràng buộc của chức năng Thêm mới đều được áp dụng cho từng dòng nhập.')

d.h3('5.2.10.3 Layout màn hình')
d.layout(modal='Import tài khoản')

d.h3('5.2.10.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Modal Import tài khoản', 'Modal', 'Enable', '–', '–', 'Ẩn', 'Mở khi bấm nút Import Excel'),
    ('Tải file mẫu', 'Button', 'Enable', '–', '–', '–', 'Tải về file Excel mẫu 6 cột'),
    ('Bảng nhập dữ liệu', 'Table/Grid', 'Enable', '–', '–', 'Trống',
     'Cho phép dán dữ liệu từ Excel hoặc nhập trực tiếp'),
    ('Số tài khoản', 'Textbox', 'Enable', '3 – 15 chữ số', 'Có', 'Trống', 'Cột bắt buộc'),
    ('Tên tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống', 'Cột bắt buộc'),
    ('Bậc', 'Textbox', 'Enable', '1 / 2 / 3', 'Có', 'Trống', 'Cột bắt buộc'),
    ('Tài khoản mẹ', 'Textbox', 'Enable', '3 – 15 chữ số', 'Có với bậc 2 và 3', 'Trống',
     'Số tài khoản mẹ; để trống với bậc 1'),
    ('Loại tài khoản', 'Textbox', 'Enable', 'Danh sách', 'Có', 'Trống', 'Cột bắt buộc'),
    ('Theo dõi công nợ', 'Textbox', 'Enable', 'Có / Không', 'Không', 'Trống',
     'Để trống được hiểu là Không; giá trị không hợp lệ sẽ báo lỗi'),
    ('Kiểm tra dữ liệu', 'Button', 'Enable', '–', '–', '–', 'Kiểm tra toàn bộ dòng và đánh dấu lỗi'),
    ('Nhập dữ liệu', 'Button', 'Enable / Disable', '–', '–', 'Disable',
     'Chỉ bật khi dữ liệu đã hợp lệ'),
    ('Thông báo lỗi theo dòng', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị tại đúng ô dữ liệu bị lỗi'),
    ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal và huỷ dữ liệu đang nhập'),
])

d.h3('5.2.10.5 Tiêu chí nghiệm thu')
d.bullets([
    'Dán dữ liệu từ Excel vào bảng nhập thì các cột được nhận đúng theo tiêu đề, kể cả tiêu đề '
    'viết không dấu.',
    'Dòng thiếu cột bắt buộc bị báo lỗi tại đúng dòng, đúng cột.',
    'Dòng có số tài khoản trùng với dữ liệu đã có bị báo lỗi.',
    'Dòng bậc 2/3 mà tài khoản mẹ không tồn tại hoặc sai bậc bị báo lỗi.',
    'Cột Theo dõi công nợ để trống thì bản ghi được nhập với giá trị Không.',
    'Cột Theo dõi công nợ nhập giá trị lạ thì báo lỗi, không ngầm hiểu là Không.',
    'Khi còn dòng lỗi thì nút Nhập dữ liệu không thực hiện được.',
    'Nhập thành công thì danh sách phía sau hiển thị đầy đủ các bản ghi vừa thêm.',
    'Người dùng chỉ có P2 gọi trực tiếp API nhập dữ liệu thì bị từ chối với lỗi 403.',
])

d.h3('5.2.10.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Import Excel', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì nút không hiển thị.\n'
     'After:\n– Mở modal nhập dữ liệu với bảng nhập trống.'),
    ('Dán dữ liệu vào bảng nhập', 'Change',
     'Nhận diện tiêu đề cột theo các cách viết được chấp nhận và điền dữ liệu vào đúng cột.'),
    ('Bấm Kiểm tra dữ liệu', 'Click',
     'During:\n'
     '– Thiếu cột bắt buộc → đánh dấu lỗi tại ô tương ứng\n'
     '– Số tài khoản sai định dạng hoặc trùng → đánh dấu lỗi\n'
     '– Tài khoản mẹ không tồn tại hoặc sai bậc → đánh dấu lỗi\n'
     '– Số tài khoản con không bắt đầu bằng số tài khoản mẹ → đánh dấu lỗi\n'
     '– Theo dõi công nợ nhập giá trị không hợp lệ → đánh dấu lỗi\n'
     'After:\n– Không còn lỗi → cho phép bấm Nhập dữ liệu.'),
    ('Bấm Nhập dữ liệu', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n– Còn dòng lỗi → không ghi bản ghi nào.\n'
     'After:\n– Ghi các bản ghi hợp lệ vào danh mục tài khoản.\n'
     '– Hiển thị kết quả nhập, đóng modal và tải lại danh sách.'),
    ('Bấm Đóng', 'Click', 'Đóng modal và huỷ toàn bộ dữ liệu đang nhập dở.'),
])

# ------------------------------------------------ 5.2.11
d.h2('5.2.11 In danh sách tài khoản')

d.h3('5.2.11.1 Giới thiệu')
d.intro_table(
    'In danh sách tài khoản',
    'Cho phép người dùng in danh sách tài khoản theo đúng bộ lọc đang áp dụng.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng đang ở màn hình danh sách tài khoản.',
    '1. Người dùng áp dụng bộ lọc mong muốn (không bắt buộc).\n'
    '2. Người dùng bấm nút In danh sách.\n'
    '3. Hệ thống mở màn hình in và tải dữ liệu theo bộ lọc.\n'
    '4. Người dùng thực hiện in từ trình duyệt.',
    '• Không có dữ liệu khớp bộ lọc → Màn hình in chỉ hiển thị phần tiêu đề.\n'
    '• Đang tải dữ liệu → Hệ thống hiển thị trạng thái đang tải.',
    'Màn hình in lấy toàn bộ dữ liệu khớp bộ lọc, không giới hạn theo trang đang xem.')

d.h3('5.2.11.2 Layout màn hình')
d.p('Đường dẫn màn hình:')
d.bullets([
    'Menu: Phân hệ Tài chính → Danh mục → Danh mục tài khoản → nút In danh sách',
    'Route (FE): /finance/accounts/print',
    'URL đầy đủ: https://<host-hrm>/finance/accounts/print',
])

d.h3('5.2.11.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('In danh sách', 'Button', 'Enable', '–', '–', '–', 'Nằm ở thanh thao tác dưới bảng danh sách'),
    ('Màn hình in', 'Table/Grid', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Bảng dữ liệu đã định dạng cho khổ giấy in'),
    ('Trạng thái đang tải', 'Loading', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị “Đang tải dữ liệu in...” trong lúc chờ'),
])

d.h3('5.2.11.4 Tiêu chí nghiệm thu')
d.bullets([
    'Dữ liệu trên màn hình in khớp đúng bộ lọc đang áp dụng.',
    'Màn hình in chứa toàn bộ bản ghi khớp bộ lọc, không chỉ trang đang xem.',
    'Bảng in vừa khổ giấy, không bị cắt cột khi in.',
    'Người dùng chỉ có P2 vẫn in được danh sách.',
])

d.h3('5.2.11.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm In danh sách', 'Click',
     'Before:\n– Kiểm tra quyền P1 hoặc P2; không có quyền → trả về lỗi 403.\n'
     'After:\n– Mở màn hình in và tải dữ liệu theo bộ lọc hiện tại.'),
])

# ================================================================ 6. BUSINESS RULES
d.h1('6. Quy tắc nghiệp vụ (Business Rules)')

d.p('BR-01 — Số tài khoản là duy nhất và chỉ gồm chữ số')
d.bullets([
    'Số tài khoản không được trùng với bất kỳ tài khoản nào khác.',
    'Số tài khoản chỉ gồm chữ số, độ dài từ 3 đến 15 chữ số.',
    'Giới hạn 15 chữ số nhằm bảo đảm giá trị không bị làm tròn hoặc cắt cụt trong quá trình '
    'truyền và hiển thị.',
])

d.p('BR-02 — Cây tài khoản có đúng 3 bậc')
d.bullets([
    'Bậc 1 là tài khoản tổng, không có tài khoản mẹ.',
    'Bậc 2 và bậc 3 bắt buộc phải có tài khoản mẹ và tài khoản mẹ phải tồn tại.',
    'Tài khoản mẹ phải ở đúng bậc liền trên: bậc 2 có mẹ bậc 1, bậc 3 có mẹ bậc 2.',
])

d.p('BR-03 — Số tài khoản con phải nối tiếp số tài khoản mẹ')
d.bullets([
    'Số tài khoản con bắt buộc bắt đầu bằng số tài khoản mẹ.',
    'Quy tắc này là cơ sở để hệ thống sắp xếp danh sách theo đúng thứ tự cây tài khoản.',
    'Vi phạm quy tắc thì bản ghi sẽ nằm sai vị trí trên cây và không có cách nào đưa về đúng chỗ.',
])

d.p('BR-04 — Bảo vệ tài khoản đang có tài khoản con')
d.bullets([
    'Tài khoản đang có tài khoản con không được đổi Bậc tài khoản.',
    'Tài khoản đang có tài khoản con không được đổi Số tài khoản, vì tài khoản con liên kết với '
    'tài khoản mẹ qua số tài khoản.',
    'Muốn đổi thì phải chuyển hoặc xoá các tài khoản con trước.',
])

d.p('BR-05 — Điều kiện khoá / mở khoá')
d.bullets([
    'Chỉ người đã tạo tài khoản mới được khoá hoặc mở khoá tài khoản đó.',
    'Chỉ tài khoản đang Hoạt động mới khoá được; chỉ tài khoản đang Khoá mới mở khoá được.',
    'Quy tắc này kế thừa từ hệ thống ERP để hai cổng hành xử giống nhau.',
])

d.p('BR-06 — Điều kiện xoá tài khoản')
d.bullets([
    'Chỉ người đã tạo tài khoản mới được xoá tài khoản đó.',
    'Tài khoản còn tài khoản con thì không được xoá.',
    'Tài khoản đã phát sinh số liệu hạch toán thì không được xoá.',
    'Cả ba điều kiện được kiểm tra lại tại máy chủ trước khi xoá thật.',
])

d.p('BR-07 — Ghi lịch sử chỉnh sửa')
d.bullets([
    'Mỗi lần cập nhật, hệ thống ghi lại các trường đã thay đổi kèm giá trị trước và sau.',
    '7 trường được theo dõi: Số tài khoản, Tên tài khoản, Tài khoản mẹ, Bậc tài khoản, '
    'Loại tài khoản, Theo dõi công nợ, Trạng thái.',
    'Giá trị của Loại tài khoản, Theo dõi công nợ và Trạng thái được ghi bằng nhãn hiển thị '
    'chứ không phải giá trị số.',
])

d.p('BR-08 — Quy tắc nhập dữ liệu từ Excel')
d.bullets([
    'Bốn cột bắt buộc: Số tài khoản, Tên tài khoản, Bậc, Loại tài khoản.',
    'Cột Theo dõi công nợ để trống được hiểu là Không; giá trị không nằm trong tập giá trị hợp lệ '
    'thì bị báo lỗi thay vì ngầm hiểu là Không.',
    'Toàn bộ ràng buộc của chức năng Thêm mới đều được áp dụng cho từng dòng nhập.',
    'Chỉ được ghi dữ liệu khi không còn dòng lỗi.',
])

d.p('BR-09 — Dữ liệu dùng chung với hệ thống ERP')
d.bullets([
    'Danh mục tài khoản dùng chung một nguồn dữ liệu với hệ thống ERP đang chạy song song.',
    'Trường “Ghi chú” có trên form ERP không được đưa sang vì dữ liệu gốc không có cột này — '
    'nhập vào cũng không lưu được.',
    'Bộ lọc theo tên của HRM tìm gần đúng ở mọi vị trí, khác ERP vốn chỉ khớp phần đuôi của tên.',
])

d.p('Chức năng liên quan: FR-01 … FR-11.')

d.save()
