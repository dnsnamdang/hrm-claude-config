# -*- coding: utf-8 -*-
"""Sinh SRS theo FORM CHUAN cho man 'Danh muc loai tai khoan' (phan he Tai chinh).

Nguon doi chieu (doc truc tiep tu code):
  BE  Modules/Finance/{Routes/api.php, Entities/TypeAccount/TypeAccount.php,
                       Http/Requests/TypeAccount/TypeAccountRequest.php,
                       Http/Controllers/V1/TypeAccountController.php}
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (1109/1110)
  FE  hrm-client/pages/finance/type-accounts/index.vue
      hrm-client/components/modal/finance/type-account-modal.vue
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
       r"\finance-account-catalog\SRS - Danh mục loại tài khoản.docx")

d = SrsDoc(
    out=OUT,
    menu='Phân hệ Tài chính → Danh mục → Danh mục loại tài khoản',
    route='/finance/type-accounts',
    full_url='https://<host-hrm>/finance/type-accounts',
    img_prefix='tacc_')

# ================================================================ TRANG BIA
d.h1('SOFTWARE REQUIREMENTS SPECIFICATION (SRS)')
d.h2('Màn hình: Danh mục loại tài khoản')
d.h2('Phân hệ: Tài chính – nhóm Danh mục')

d.info_table([
    ('Mã màn hình', 'TC-DM-TYPEACCOUNT'),
    ('Đường dẫn', '/finance/type-accounts'),
    ('Phiên bản', '1.0'),
    ('Ngày lập', '12/08/2026'),
    ('Người lập', '@junfoke'),
    ('Trạng thái tài liệu', 'Draft'),
    ('Nguồn đối chiếu', 'Màn ERP admin/accounting/type_accounts (bảng type_accounts trên DB gộp)'),
])

# ================================================================ 1. GIOI THIEU
d.h1('1. Giới thiệu')

d.h2('1.1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm (SRS) cho màn hình quản lý danh mục loại tài khoản, nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa BA/PO/Dev/Test',
    'Là căn cứ nghiệm thu chức năng và phân quyền',
    'Làm rõ ràng buộc: loại tài khoản đã được tài khoản kế toán sử dụng thì không được xoá và '
    'không được khoá',
])

d.h2('1.2 Phạm vi')
d.p('Màn hình Danh mục loại tài khoản cung cấp chức năng:')
d.bullets([
    'Xem danh sách loại tài khoản, tìm kiếm nhanh và lọc nâng cao theo 6 tiêu chí',
    'Thêm mới, chỉnh sửa, xem chi tiết loại tài khoản qua modal ngay trên màn danh sách',
    'Khoá / Mở khoá loại tài khoản',
    'Xoá loại tài khoản khi chưa được sử dụng',
    'Xem lịch sử chỉnh sửa của từng loại tài khoản',
    'Xuất danh sách ra file Excel',
    'Nhập dữ liệu hàng loạt từ file Excel, có bước kiểm tra dữ liệu trước khi ghi',
])
d.p('Ngoài phạm vi:')
d.bullets([
    'In danh sách — màn hình không có chức năng này',
    'Thay đổi cấu trúc bảng dữ liệu: giữ nguyên dữ liệu dùng chung với hệ thống ERP đang chạy song song',
    'Phân quyền theo cấp: danh mục dùng chung toàn hệ thống',
])

d.h2('1.3 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Loại tài khoản', 'Phân loại tài khoản kế toán theo bản chất (tài sản, nợ phải trả, doanh thu…)'),
    ('Mã loại tài khoản', 'Chuỗi định danh loại tài khoản, duy nhất, luôn viết hoa'),
    ('Đang được sử dụng', 'Loại tài khoản đã được gán cho ít nhất một tài khoản kế toán'),
    ('Khoá', 'Trạng thái ngừng sử dụng: bản ghi vẫn còn trong danh mục nhưng không xuất hiện '
             'ở các danh sách chọn của màn khác'),
    ('Lịch sử chỉnh sửa', 'Danh sách các lần thay đổi thông tin, ghi rõ giá trị trước và sau'),
    ('P1', 'Quyền “Quản lý danh mục loại tài khoản”'),
    ('P2', 'Quyền “Xem danh mục loại tài khoản”'),
    ('Quick Search', 'Tìm kiếm nhanh'),
    ('Advanced Filter', 'Bộ lọc nâng cao'),
    ('SRS', 'Software Requirements Specification'),
], widths=[1.8, 4.2])

# ================================================================ 2. TONG QUAN
d.h1('2. Tổng quan')

d.h2('2.1 Bối cảnh nghiệp vụ')
d.p('Danh mục loại tài khoản là dữ liệu nền của hệ thống tài khoản kế toán, dùng để:')
d.bullets([
    'Cung cấp danh sách phân loại cho ô chọn Loại tài khoản khi khai báo tài khoản kế toán',
    'Nhóm các tài khoản theo bản chất kế toán phục vụ lên báo cáo',
])
d.p('Do đó cần:')
d.bullets([
    'Bảo đảm mã và tên loại tài khoản không trùng nhau để tránh nhầm lẫn khi chọn',
    'Ngăn xoá hoặc khoá loại tài khoản đang được tài khoản kế toán sử dụng — nếu không, các tài '
    'khoản đó sẽ mất phân loại',
    'Ghi lại lịch sử chỉnh sửa để truy vết',
    'Hỗ trợ nhập liệu hàng loạt khi khai báo lần đầu',
])

d.h2('2.2 Nhóm người dùng')
d.bullets([
    'Người dùng có quyền P1: được quản lý danh mục (thêm/sửa/khoá/xoá/nhập từ Excel) và xem lịch sử',
    'Người dùng có quyền P2: chỉ được xem/tra cứu, xem lịch sử và xuất Excel',
    'Người dùng không có P1/P2: bị chặn truy cập',
])

# ================================================================ 3. PHAN QUYEN
d.h1('3. Phân quyền và kiểm soát truy cập')

d.h2('3.1 Danh sách quyền')
d.table(['Ký hiệu', 'Tên quyền', 'Mã quyền', 'Nhóm quyền'], [
    ('P1', 'Quản lý danh mục loại tài khoản', '1109', 'Danh mục tài chính'),
    ('P2', 'Xem danh mục loại tài khoản', '1110', 'Danh mục tài chính'),
], widths=[0.8, 2.8, 0.9, 1.5])
d.p('Ghi chú: màn hình tương ứng bên ERP không gate quyền nào, hai quyền trên là quyền mới của HRM.')

d.h2('3.2 Quy tắc truy cập bắt buộc')
d.bullets([
    'Chỉ user có P1 hoặc P2 mới được truy cập màn hình.',
    'User không có P1/P2: không hiển thị menu điều hướng tới màn hình.',
    'User không có P1/P2: truy cập trực tiếp URL bị chặn, gọi API trả về lỗi 403.',
    'User chỉ có P2: mọi thao tác ghi (thêm/sửa/khoá/mở khoá/xoá/nhập Excel) bị chặn ở cả giao diện '
    'lẫn API (403), không phụ thuộc vào việc giao diện có ẩn nút hay không.',
    'Danh sách rút gọn phục vụ ô chọn Loại tài khoản ở màn Danh mục tài khoản không gate quyền.',
])

d.h2('3.3 Ma trận phân quyền')
d.table(['Chức năng', 'P1', 'P2', 'Không có quyền'], [
    ('Truy cập màn', '✅', '✅', '❌'),
    ('Xem danh sách', '✅', '✅', '❌'),
    ('Tìm kiếm nhanh / Lọc nâng cao / Sắp xếp / Phân trang', '✅', '✅', '❌'),
    ('Xem chi tiết', '✅', '✅', '❌'),
    ('Xem lịch sử chỉnh sửa', '✅', '✅', '❌'),
    ('Thêm mới', '✅', '❌', '❌'),
    ('Chỉnh sửa', '✅', '❌', '❌'),
    ('Khoá / Mở khoá', '✅', '❌', '❌'),
    ('Xoá', '✅', '❌', '❌'),
    ('Nhập từ Excel', '✅', '❌', '❌'),
    ('Xuất Excel', '✅', '✅', '❌'),
], widths=[3.0, 0.8, 0.8, 1.4])

# ================================================================ 4. FUNCTION LIST
d.h1('4. Danh mục chức năng (Function list)')
d.table(['ID', 'Chức năng', 'Mô tả đặc tả thu nhỏ (Mini-Spec)', 'Quyền'], [
    ('FR-01', 'Truy cập màn hình',
     'Kiểm tra quyền P1/P2. Không có quyền sẽ bị chặn (ẩn menu, chặn URL, API trả 403).', 'P1, P2'),
    ('FR-02', 'Xem danh sách',
     'Hiển thị bảng 7 cột, phân trang, sắp xếp phía máy chủ trên cột Mã và Tên.', 'P1, P2'),
    ('FR-03', 'Tìm kiếm & Lọc',
     'Kết hợp Quick Search và Advanced Filter theo 6 tiêu chí: Mã, Tên, Trạng thái, Người tạo, '
     'Người cập nhật, khoảng thời gian cập nhật.', 'P1, P2'),
    ('FR-04', 'Thêm mới',
     'Mở modal, nhập Mã (*), Tên (*), Ghi chú, Trạng thái. Mã tự viết hoa; mã và tên đều '
     'không được trùng. Có nút Lưu & Tiếp tục.', 'P1'),
    ('FR-05', 'Chỉnh sửa', 'Mở modal nạp sẵn dữ liệu, cho phép sửa toàn bộ trường và Trạng thái.', 'P1'),
    ('FR-06', 'Xem chi tiết',
     'Mở modal ở chế độ chỉ đọc, mọi trường bị vô hiệu hoá và ẩn nút Lưu.', 'P1, P2'),
    ('FR-07', 'Khoá / Mở khoá',
     'Đổi trạng thái sau khi xác nhận. Chỉ khoá được khi loại tài khoản chưa được sử dụng.', 'P1'),
    ('FR-08', 'Xoá',
     'Xoá bản ghi sau khi xác nhận. Chặn khi đã có tài khoản kế toán dùng loại này.', 'P1'),
    ('FR-09', 'Xem lịch sử chỉnh sửa',
     'Mở modal liệt kê các lần thay đổi, mỗi lần nêu rõ trường thay đổi kèm giá trị trước và sau.',
     'P1, P2'),
    ('FR-10', 'Xuất Excel', 'Xuất danh sách theo đúng bộ lọc đang áp dụng ra file Excel.', 'P1, P2'),
    ('FR-11', 'Nhập từ Excel',
     'Tải file mẫu 4 cột, dán/nhập dữ liệu, kiểm tra trước khi ghi rồi nhập hàng loạt.', 'P1'),
], widths=[0.7, 1.4, 3.4, 0.8])

# ================================================================ 5. DAC TA CHI TIET
d.h1('5. Đặc tả chi tiết theo từng chức năng (FUNCTIONAL PACKAGING)')

d.h2('5.1 Sơ đồ UML tổng quan')
d.p('Sơ đồ Use Case tổng quan của màn hình, thể hiện quan hệ giữa hai nhóm người dùng và '
    'mười một chức năng:')
d.overview_figure(
    'HỆ THỐNG HRM — Danh mục loại tài khoản',
    [(ACTOR_P1, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
     ('Người xem danh mục (P2)', [0, 1, 2, 5, 8, 9])],
    [('FR-01', 'Truy cập màn hình', 'view', None),
     ('FR-02', 'Xem danh sách', 'view', None),
     ('FR-03', 'Tìm kiếm & Lọc', 'view', None),
     ('FR-04', 'Thêm mới', 'crud', None),
     ('FR-05', 'Chỉnh sửa', 'crud', None),
     ('FR-06', 'Xem chi tiết', 'view', None),
     ('FR-07', 'Khoá / Mở khoá', 'action', None),
     ('FR-08', 'Xoá', 'action', '«include» Kiểm tra loại tài khoản đang sử dụng'),
     ('FR-09', 'Xem lịch sử chỉnh sửa', 'view', None),
     ('FR-10', 'Xuất Excel', 'io', None),
     ('FR-11', 'Nhập từ Excel', 'io', None)],
    'Sơ đồ Use Case tổng quan màn hình Danh mục loại tài khoản')

d.h2('5.2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------ 5.2.1
d.h2('5.2.1 Truy cập màn hình danh mục loại tài khoản')

d.h3('5.2.1.1 Biểu đồ Usecase')
d.uc_figure('FR-01', 'Truy cập màn hình danh mục loại tài khoản', 'view',
            [('include', 'Kiểm tra quyền truy cập')], actor=ACTOR_BOTH)

d.h3('5.2.1.2 Giới thiệu')
d.intro_table(
    'Truy cập màn hình danh mục loại tài khoản',
    'Cho phép người dùng truy cập vào màn hình quản lý danh mục loại tài khoản để tra cứu và '
    'quản lý dữ liệu.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng đã đăng nhập thành công vào hệ thống.',
    '1. Người dùng chọn menu Tài chính → Danh mục → Danh mục loại tài khoản.\n'
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
    'Nhìn thấy menu Danh mục loại tài khoản.',
    'Truy cập được màn hình danh sách.',
    'Hiển thị mặc định: danh sách phải hiển thị đúng cấu trúc bảng gồm STT, Mã loại tài khoản, '
    'Tên loại tài khoản, Ghi chú, Cập nhật, Trạng thái, Hành động.',
])
d.p('Người dùng không có quyền:')
d.bullets([
    'Không nhìn thấy menu.',
    'Truy cập trực tiếp URL bị chặn, gọi API trả về 403.',
])

d.h3('5.2.1.5 Danh sách event và xử lý event')
d.event_table([
    ('Click menu Danh mục loại tài khoản', 'Click',
     'Kiểm tra quyền (P1 hoặc P2) và điều hướng tới màn hình danh sách.'),
    ('Truy cập URL trực tiếp', 'System',
     'Kiểm tra quyền; nếu không hợp lệ → chặn truy cập (giao diện) và trả về lỗi 403 (API).'),
    ('Load màn hình', 'System', 'Khôi phục bộ lọc đã lưu và tải danh sách trang 1.'),
])

# ------------------------------------------------ 5.2.2
d.h2('5.2.2 Xem danh sách loại tài khoản')

d.h3('5.2.2.1 Giới thiệu')
d.intro_table(
    'Xem danh sách loại tài khoản',
    'Hiển thị danh sách loại tài khoản đã khai báo kèm ghi chú, thông tin cập nhật gần nhất '
    'và trạng thái sử dụng.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng truy cập thành công màn hình danh mục loại tài khoản.',
    '1. Hệ thống lấy danh sách loại tài khoản theo bộ lọc hiện tại.\n'
    '2. Hệ thống hiển thị danh sách theo phân trang.\n'
    '3. Hệ thống xác định với mỗi bản ghi có được phép khoá / xoá hay không để bật hoặc vô hiệu hoá '
    'các nút thao tác tương ứng.',
    '• Không có dữ liệu → Hiển thị danh sách trống kèm thông báo không có dữ liệu.\n'
    '• Bản ghi chưa có ghi chú → Cột Ghi chú để trống.\n'
    '• Bản ghi chưa từng được cập nhật → Cột Cập nhật để trống.',
    'Danh sách hiển thị cả bản ghi Hoạt động lẫn bản ghi Khoá.')

d.h3('5.2.2.2 Layout màn hình')
d.layout()

d.h3('5.2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Bảng danh sách loại tài khoản', 'Table/Grid', 'Enable', '–', '–', '–',
     'Hiển thị danh sách theo phân trang'),
    ('STT', 'Label', 'Enable', '–', '–', '–', 'Số thứ tự bản ghi, tính theo trang hiện tại'),
    ('Mã loại tài khoản', 'Text', 'Enable', '0–255 ký tự', '–', 'Lấy từ hệ thống',
     'Mã định danh, luôn hiển thị chữ in hoa. Cho phép sắp xếp'),
    ('Tên loại tài khoản', 'Text', 'Enable', '0–255 ký tự', '–', 'Lấy từ hệ thống',
     'Tên đầy đủ, tự xuống dòng khi dài. Cho phép sắp xếp'),
    ('Ghi chú', 'Text', 'Enable', '0–255 ký tự', '–', 'Lấy từ hệ thống', 'Ghi chú thêm, có thể để trống'),
    ('Cập nhật', 'Text', 'Enable', 'dd/mm/yyyy', '–', 'Lấy từ hệ thống',
     'Thời điểm cập nhật gần nhất kèm tên người cập nhật'),
    ('Trạng thái', 'Badge', 'Enable', 'Hoạt động / Khoá', '–', 'Hoạt động', 'Trạng thái loại tài khoản'),
    ('Khoá / Mở khoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Ẩn khi không có P1; vô hiệu hoá khi loại tài khoản đang được sử dụng hoặc trạng thái '
     'không cho phép, chú giải nêu rõ lý do'),
    ('Xem', 'Icon Button', 'Enable', '–', '–', '–', 'Mở modal xem chi tiết ở chế độ chỉ đọc'),
    ('Lịch sử chỉnh sửa', 'Icon Button', 'Enable', '–', '–', '–',
     'Mở modal xem lịch sử thay đổi của bản ghi'),
    ('Sửa', 'Icon Button', 'Enable / Ẩn', '–', '–', '–', 'Mở modal chỉnh sửa. Ẩn khi không có P1'),
    ('Xoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Ẩn khi không có P1; vô hiệu hoá khi loại tài khoản đang được sử dụng'),
    ('Tạo mới', 'Button', 'Enable / Ẩn', '–', '–', '–', 'Mở modal thêm mới. Ẩn khi không có P1'),
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
    'Danh sách hiển thị đủ cả bản ghi Hoạt động lẫn bản ghi Khoá.',
    'Loại tài khoản đang được tài khoản kế toán sử dụng thì nút Khoá và nút Xoá đều bị vô hiệu hoá.',
    'Sắp xếp trên cột Mã và cột Tên đổi đúng thứ tự dữ liệu.',
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
d.h2('5.2.3 Tìm kiếm và lọc danh sách loại tài khoản')

d.h3('5.2.3.1 Giới thiệu')
d.intro_table(
    'Tìm kiếm và lọc danh sách loại tài khoản',
    'Cho phép người dùng thu hẹp danh sách theo từ khoá hoặc theo nhiều tiêu chí kết hợp, '
    'và sắp xếp danh sách theo cột mong muốn.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng đang ở màn hình danh sách loại tài khoản.',
    '1. Người dùng nhập từ khoá vào ô tìm kiếm nhanh hoặc mở bộ lọc nâng cao.\n'
    '2. Người dùng nhập/chọn các tiêu chí: Mã, Tên, Trạng thái, Người tạo, Người cập nhật, '
    'Cập nhật từ ngày – đến ngày.\n'
    '3. Người dùng bấm Tìm kiếm.\n'
    '4. Hệ thống lấy danh sách khớp điều kiện, quay về trang 1 và hiển thị kết quả.\n'
    '5. Người dùng có thể bấm tiêu đề cột Mã hoặc Tên để đổi thứ tự sắp xếp.',
    '• Bấm Làm mới → Hệ thống xoá toàn bộ điều kiện lọc và tải lại danh sách đầy đủ.\n'
    '• Không có kết quả → Hiển thị danh sách trống kèm thông báo.\n'
    '• Thay đổi tiêu chí ở bộ lọc nâng cao → Hệ thống tự tìm lại ngay, không cần bấm Tìm kiếm.\n'
    '• Chỉ nhập một trong hai mốc thời gian → Hệ thống lọc theo mốc đã nhập.',
    'Điều kiện lọc được ghi nhớ và dùng lại khi quay về màn hình.')

d.h3('5.2.3.2 Layout màn hình')
d.layout()

d.h3('5.2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Khung bộ lọc', 'Modal', 'Enable', '–', '–', 'Thu gọn',
     'Khung bộ lọc danh mục loại tài khoản, có thể mở rộng / thu gọn'),
    ('Tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Tìm theo mã hoặc tên'),
    ('Mã loại tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Lọc theo một phần của mã'),
    ('Tên loại tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Lọc theo một phần của tên'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khoá', 'Không', 'Trống',
     'Lọc theo trạng thái; để trống là lấy tất cả'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Lọc theo người tạo bản ghi'),
    ('Người cập nhật', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Lọc theo người cập nhật gần nhất'),
    ('Cập nhật từ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Mốc đầu của khoảng thời gian cập nhật'),
    ('Cập nhật đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', 'Mốc cuối của khoảng thời gian cập nhật'),
    ('Tìm kiếm', 'Button', 'Enable', '–', '–', '–', 'Áp dụng bộ lọc và quay về trang 1'),
    ('Làm mới', 'Button', 'Enable', '–', '–', '–', 'Xoá toàn bộ điều kiện lọc và tải lại danh sách'),
    ('Tiêu đề cột sắp xếp', 'Button', 'Enable', 'Mã / Tên', '–', 'Không sắp xếp',
     'Bấm để đổi chiều sắp xếp; sắp xếp thực hiện phía máy chủ'),
])

d.h3('5.2.3.4 Tiêu chí nghiệm thu')
d.bullets([
    'Tìm kiếm nhanh tìm được theo cả mã và tên.',
    'Từ khoá chứa ký tự đặc biệt của phép tìm gần đúng vẫn được tìm như ký tự thông thường.',
    'Kết hợp nhiều tiêu chí cho ra kết quả thoả mãn đồng thời tất cả tiêu chí.',
    'Lọc theo khoảng thời gian cập nhật trả về đúng các bản ghi nằm trong khoảng, tính cả hai đầu mốc.',
    'Bấm Tìm kiếm luôn quay về trang 1.',
    'Bấm Làm mới thì danh sách được tải lại đầy đủ, không giữ điều kiện cũ.',
])

d.h3('5.2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Nhập ô tìm kiếm nhanh', 'Keypress', 'Ghi nhận từ khoá, chưa gọi tìm kiếm.'),
    ('Bấm Tìm kiếm', 'Click', 'Quay về trang 1 và tải lại danh sách theo toàn bộ điều kiện lọc.'),
    ('Đổi tiêu chí lọc nâng cao', 'Change', 'Quay về trang 1 và tải lại danh sách ngay theo điều kiện mới.'),
    ('Chọn khoảng thời gian cập nhật', 'Change', 'Lọc theo khoảng đã chọn và tải lại danh sách.'),
    ('Bấm Làm mới', 'Click', 'Xoá toàn bộ điều kiện lọc, quay về trang 1 và tải lại danh sách.'),
    ('Bấm tiêu đề cột', 'Click', 'Đổi cột và chiều sắp xếp, tải lại danh sách.'),
])

# ------------------------------------------------ 5.2.4
d.h2('5.2.4 Thêm mới loại tài khoản')

d.h3('5.2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Thêm mới loại tài khoản', 'crud',
            [('include', 'Kiểm tra trùng mã và tên')])

d.h3('5.2.4.2 Giới thiệu')
d.intro_table(
    'Thêm mới loại tài khoản',
    'Cho phép người quản lý danh mục khai báo một loại tài khoản mới để dùng khi phân loại '
    'tài khoản kế toán.',
    'Admin; User được phân quyền P1',
    'Người dùng đang ở màn hình danh sách và có quyền quản lý danh mục loại tài khoản.',
    '1. Người dùng bấm nút Tạo mới → Hệ thống mở modal Thêm loại tài khoản với các trường trống.\n'
    '2. Người dùng nhập Mã loại tài khoản, Tên loại tài khoản, Ghi chú (tuỳ chọn) và chọn Trạng thái.\n'
    '3. Người dùng bấm Lưu.\n'
    '4. Hệ thống chuẩn hoá dữ liệu: mã viết hoa và bỏ khoảng trắng thừa.\n'
    '5. Hệ thống kiểm tra hợp lệ rồi ghi bản ghi mới.\n'
    '6. Hệ thống hiển thị thông báo thành công, đóng modal và tải lại danh sách.',
    '• Người dùng bấm Lưu & Tiếp tục → Hệ thống lưu bản ghi rồi giữ modal mở với các trường trống '
    'để nhập tiếp.\n'
    '• Người dùng bấm Đóng → Hệ thống đóng modal, không lưu gì.\n'
    '• Dữ liệu không hợp lệ → Hệ thống hiển thị lỗi ngay dưới từng trường và không lưu.\n'
    '• Không chọn Trạng thái → Hệ thống mặc định là Hoạt động.',
    'Cả Mã và Tên loại tài khoản đều phải là duy nhất trong toàn danh mục.')

d.h3('5.2.4.3 Layout màn hình')
d.layout(modal='Thêm loại tài khoản')

d.h3('5.2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Modal Thêm loại tài khoản', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Mở khi bấm Tạo mới; tiêu đề “Thêm loại tài khoản”'),
    ('Mã loại tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
     'Tự viết hoa khi lưu, không được trùng'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khoá', 'Không', 'Hoạt động', 'Trạng thái sử dụng'),
    ('Tên loại tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống', 'Không được trùng'),
    ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Ghi chú thêm, có thể bỏ trống'),
    ('Lưu', 'Button', 'Enable', '–', '–', '–',
     'Kiểm tra hợp lệ và ghi bản ghi; vô hiệu hoá trong lúc đang gửi'),
    ('Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', '–',
     'Ghi bản ghi và giữ modal mở để nhập tiếp; chỉ hiển thị ở chế độ thêm mới'),
    ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal, không lưu'),
    ('Thông báo lỗi theo trường', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị ngay dưới trường tương ứng kèm viền đỏ'),
])

d.h3('5.2.4.5 Tiêu chí nghiệm thu')
d.bullets([
    'Bỏ trống Mã hoặc Tên thì không lưu được và hiển thị lỗi “Bắt buộc phải nhập”.',
    'Nhập mã đã tồn tại thì hiển thị lỗi “Mã loại tài khoản đã tồn tại”.',
    'Nhập tên đã tồn tại thì hiển thị lỗi “Tên loại tài khoản đã tồn tại”.',
    'Nhập mã chữ thường thì bản ghi lưu xuống phải ở dạng chữ in hoa.',
    'Nhập quá 255 ký tự ở bất kỳ trường nào thì hiển thị lỗi “Tối đa 255 ký tự”.',
    'Không chọn Trạng thái thì bản ghi mới ở trạng thái Hoạt động.',
    'Bấm Lưu & Tiếp tục thì modal vẫn mở với các trường trống và danh sách phía sau đã có bản ghi mới.',
    'Người dùng chỉ có P2 gọi trực tiếp API tạo mới thì bị từ chối với lỗi 403.',
])

d.h3('5.2.4.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tạo mới', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì nút không hiển thị.\n'
     'After:\n– Xoá dữ liệu cũ trong modal và mở modal Thêm loại tài khoản.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n'
     '– Mã loại tài khoản trống → hiển thị “Bắt buộc phải nhập”\n'
     '– Tên loại tài khoản trống → hiển thị “Bắt buộc phải nhập”\n'
     '– Mã trùng → hiển thị “Mã loại tài khoản đã tồn tại”\n'
     '– Tên trùng → hiển thị “Tên loại tài khoản đã tồn tại”\n'
     '– Trường vượt 255 ký tự → hiển thị “Tối đa 255 ký tự”\n'
     '– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Ghi bản ghi mới kèm người tạo.\n'
     '– Hiển thị thông báo thành công, đóng modal và tải lại danh sách.'),
    ('Bấm Lưu & Tiếp tục', 'Click',
     'Xử lý như bấm Lưu; sau khi ghi thành công thì giữ modal mở và xoá trắng các trường.'),
    ('Bấm Đóng', 'Click', 'Đóng modal và xoá dữ liệu đang nhập dở, không lưu bất kỳ thay đổi nào.'),
])

# ------------------------------------------------ 5.2.5
d.h2('5.2.5 Chỉnh sửa loại tài khoản')

d.h3('5.2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa loại tài khoản', 'crud',
            [('include', 'Kiểm tra trùng mã và tên'),
             ('include', 'Ghi lịch sử thay đổi')])

d.h3('5.2.5.2 Giới thiệu')
d.intro_table(
    'Chỉnh sửa loại tài khoản',
    'Cho phép người quản lý danh mục cập nhật thông tin của một loại tài khoản đã khai báo.',
    'Admin; User được phân quyền P1',
    'Bản ghi loại tài khoản đang tồn tại; người dùng có quyền quản lý danh mục loại tài khoản.',
    '1. Người dùng bấm biểu tượng Sửa ở dòng cần chỉnh sửa.\n'
    '2. Hệ thống mở modal Sửa loại tài khoản và nạp sẵn dữ liệu hiện tại.\n'
    '3. Người dùng chỉnh sửa các trường cần thay đổi.\n'
    '4. Người dùng bấm Lưu.\n'
    '5. Hệ thống kiểm tra hợp lệ, cập nhật bản ghi và ghi nhận lịch sử thay đổi.\n'
    '6. Hệ thống hiển thị thông báo thành công, đóng modal và tải lại danh sách.',
    '• Bản ghi đã bị xoá bởi người dùng khác → Hệ thống báo dữ liệu đã thay đổi và yêu cầu tải lại.\n'
    '• Mã hoặc tên mới trùng với bản ghi khác → Hệ thống báo lỗi và không lưu.\n'
    '• Không gửi Trạng thái → Hệ thống giữ nguyên trạng thái cũ.',
    '• Kiểm tra trùng bỏ qua chính bản ghi đang sửa.\n'
    '• Mọi thay đổi trên 4 trường được theo dõi (Mã, Tên, Ghi chú, Trạng thái) đều được ghi vào '
    'lịch sử chỉnh sửa.')

d.h3('5.2.5.3 Layout màn hình')
d.layout(modal='Sửa loại tài khoản')

d.h3('5.2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Modal Sửa loại tài khoản', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Mở khi bấm biểu tượng Sửa; tiêu đề “Sửa loại tài khoản”'),
    ('Thông tin cập nhật gần nhất', 'Label', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Hiển thị trên tiêu đề modal khi bản ghi đã có lịch sử cập nhật'),
    ('Mã loại tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Lấy từ hệ thống',
     'Cho phép sửa, không được trùng'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khoá', 'Không', 'Lấy từ hệ thống', 'Cho phép đổi'),
    ('Tên loại tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Lấy từ hệ thống',
     'Cho phép sửa, không được trùng'),
    ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Lấy từ hệ thống', 'Cho phép sửa hoặc xoá trống'),
    ('Lưu', 'Button', 'Enable', '–', '–', '–', 'Kiểm tra hợp lệ và cập nhật bản ghi'),
    ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal, huỷ thay đổi chưa lưu'),
])

d.h3('5.2.5.5 Tiêu chí nghiệm thu')
d.bullets([
    'Modal nạp đúng dữ liệu của dòng được chọn.',
    'Đổi mã hoặc tên trùng với bản ghi khác thì báo lỗi tương ứng và không lưu.',
    'Giữ nguyên mã và tên của chính bản ghi đang sửa thì lưu được bình thường.',
    'Xoá trống Ghi chú thì bản ghi được cập nhật thành không có ghi chú.',
    'Sau khi lưu, các trường đã thay đổi phải xuất hiện trong lịch sử chỉnh sửa với giá trị '
    'trước và sau.',
    'Người dùng chỉ có P2 gọi trực tiếp API cập nhật thì bị từ chối với lỗi 403.',
])

d.h3('5.2.5.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Sửa', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì biểu tượng không hiển thị.\n'
     'After:\n– Nạp dữ liệu bản ghi và mở modal Sửa loại tài khoản.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n'
     '– Mã / Tên trống → hiển thị “Bắt buộc phải nhập”\n'
     '– Mã trùng bản ghi khác → hiển thị “Mã loại tài khoản đã tồn tại”\n'
     '– Tên trùng bản ghi khác → hiển thị “Tên loại tài khoản đã tồn tại”\n'
     '– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Cập nhật bản ghi kèm người cập nhật.\n'
     '– Ghi lịch sử thay đổi cho các trường được theo dõi.\n'
     '– Hiển thị thông báo thành công, đóng modal và tải lại danh sách.'),
    ('Bản ghi không còn tồn tại', 'System',
     'Hiển thị thông báo dữ liệu đã thay đổi và yêu cầu tải lại danh sách.'),
])

# ------------------------------------------------ 5.2.6
d.h2('5.2.6 Xem chi tiết loại tài khoản')

d.h3('5.2.6.1 Giới thiệu')
d.intro_table(
    'Xem chi tiết loại tài khoản',
    'Cho phép người dùng xem đầy đủ thông tin của một loại tài khoản mà không thay đổi dữ liệu.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Bản ghi loại tài khoản đang tồn tại; người dùng đang ở màn hình danh sách.',
    '1. Người dùng bấm biểu tượng Xem ở dòng cần xem.\n'
    '2. Hệ thống mở modal ở chế độ chỉ đọc và nạp dữ liệu bản ghi.\n'
    '3. Người dùng xem xong thì bấm Đóng.',
    '• Không có quyền → Hệ thống trả về lỗi 403 và không mở modal.\n'
    '• Bản ghi không còn tồn tại → Hệ thống báo dữ liệu đã thay đổi và yêu cầu tải lại.',
    'Ở chế độ chỉ đọc, toàn bộ trường nhập bị vô hiệu hoá và các nút Lưu không hiển thị.')

d.h3('5.2.6.2 Layout màn hình')
d.layout(modal='Xem loại tài khoản')

d.h3('5.2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Modal Xem loại tài khoản', 'Modal', 'Read-only', '–', '–', 'Ẩn', 'Tiêu đề “Xem loại tài khoản”'),
    ('Mã loại tài khoản', 'Textbox', 'Disable', '–', '–', 'Lấy từ hệ thống', 'Chỉ đọc'),
    ('Trạng thái', 'Dropdown', 'Disable', '–', '–', 'Lấy từ hệ thống', 'Chỉ đọc'),
    ('Tên loại tài khoản', 'Textbox', 'Disable', '–', '–', 'Lấy từ hệ thống', 'Chỉ đọc'),
    ('Ghi chú', 'Textarea', 'Disable', '–', '–', 'Lấy từ hệ thống', 'Chỉ đọc'),
    ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal'),
])

d.h3('5.2.6.4 Tiêu chí nghiệm thu')
d.bullets([
    'Modal mở ở chế độ chỉ đọc, không sửa được bất kỳ trường nào.',
    'Nút Lưu và Lưu & Tiếp tục không hiển thị.',
    'Người dùng chỉ có P2 vẫn xem được chi tiết.',
])

d.h3('5.2.6.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Xem', 'Click', 'Nạp dữ liệu bản ghi và mở modal ở chế độ chỉ đọc.'),
    ('Bấm Đóng', 'Click', 'Đóng modal và xoá dữ liệu đang hiển thị.'),
])

# ------------------------------------------------ 5.2.7
d.h2('5.2.7 Khoá / Mở khoá loại tài khoản')

d.h3('5.2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Khoá / Mở khoá loại tài khoản', 'action',
            [('include', 'Kiểm tra loại tài khoản đang sử dụng')])

d.h3('5.2.7.2 Giới thiệu')
d.intro_table(
    'Khoá / Mở khoá loại tài khoản',
    'Cho phép người quản lý danh mục ngừng sử dụng một loại tài khoản chưa được dùng đến, '
    'hoặc cho dùng lại loại tài khoản đã khoá.',
    'Admin; User được phân quyền P1',
    'Bản ghi loại tài khoản đang tồn tại; người dùng có quyền quản lý danh mục loại tài khoản.',
    '1. Người dùng bấm biểu tượng Khoá (hoặc Mở khoá) ở dòng tương ứng.\n'
    '2. Hệ thống hiển thị hộp thoại xác nhận nêu rõ tên loại tài khoản.\n'
    '3. Người dùng xác nhận.\n'
    '4. Hệ thống đổi trạng thái bản ghi và hiển thị thông báo thành công.\n'
    '5. Hệ thống tải lại danh sách.',
    '• Loại tài khoản đã được tài khoản kế toán sử dụng → Nút Khoá bị vô hiệu hoá, '
    'chú giải nêu rõ lý do.\n'
    '• Trạng thái hiện tại không phù hợp với hành động → Nút bị vô hiệu hoá.\n'
    '• Người dùng bấm Huỷ → Hệ thống đóng hộp thoại, không thay đổi gì.',
    '• Điều kiện “chỉ khoá được khi chưa được sử dụng” kế thừa từ hệ thống ERP.\n'
    '• Mở khoá không bị ràng buộc điều kiện sử dụng.')

d.h3('5.2.7.3 Layout màn hình')
d.layout()

d.h3('5.2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng Khoá / Mở khoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Biểu tượng đổi theo trạng thái hiện tại. Ẩn khi không có P1; vô hiệu hoá khi không đủ điều kiện'),
    ('Chú giải nút', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện khi rê chuột, nêu hành động hoặc lý do bị chặn'),
    ('Hộp thoại xác nhận', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Tiêu đề “Xác nhận khóa” / “Xác nhận mở khóa”, nội dung nêu tên loại tài khoản'),
    ('Nút xác nhận', 'Button', 'Enable', '–', '–', '–', 'Nhãn “Khóa” hoặc “Mở khóa”'),
    ('Huỷ', 'Button', 'Enable', '–', '–', '–', 'Đóng hộp thoại, không thực hiện gì'),
])

d.h3('5.2.7.5 Tiêu chí nghiệm thu')
d.bullets([
    'Loại tài khoản đang được sử dụng thì nút Khoá bị vô hiệu hoá; gọi trực tiếp API cũng bị chặn.',
    'Loại tài khoản chưa được sử dụng thì khoá được, trạng thái đổi thành Khoá.',
    'Loại tài khoản đang Khoá thì mở khoá được, kể cả khi đã có tài khoản sử dụng.',
    'Bấm Huỷ thì trạng thái giữ nguyên.',
    'Loại tài khoản đang Khoá không còn xuất hiện trong ô chọn Loại tài khoản ở màn Danh mục tài khoản.',
    'Người dùng chỉ có P2 gọi trực tiếp API khoá/mở khoá thì bị từ chối với lỗi 403.',
])

d.h3('5.2.7.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Khoá / Mở khoá', 'Click',
     'Before:\n– Kiểm tra quyền P1 và điều kiện khoá; không đủ điều kiện thì nút bị vô hiệu hoá.\n'
     'After:\n– Mở hộp thoại xác nhận với nội dung tương ứng hành động.'),
    ('Xác nhận trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n'
     '– Loại tài khoản đang được sử dụng mà yêu cầu khoá → hiển thị thông báo từ chối\n'
     '– Trạng thái hiện tại không phù hợp với hành động → hiển thị thông báo lỗi tương ứng\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Cập nhật trạng thái bản ghi.\n'
     '– Hiển thị thông báo thành công và tải lại danh sách.'),
    ('Bấm Huỷ', 'Click', 'Đóng hộp thoại, không thay đổi trạng thái.'),
])

# ------------------------------------------------ 5.2.8
d.h2('5.2.8 Xoá loại tài khoản')

d.h3('5.2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Xoá loại tài khoản', 'action',
            [('include', 'Kiểm tra loại tài khoản đang sử dụng'),
             ('extend', 'Chuyển sang trạng thái Khoá khi không xoá được')])

d.h3('5.2.8.2 Giới thiệu')
d.intro_table(
    'Xoá loại tài khoản',
    'Cho phép người quản lý danh mục xoá một loại tài khoản khai báo nhầm, với điều kiện chưa có '
    'tài khoản kế toán nào dùng loại đó.',
    'Admin; User được phân quyền P1',
    'Bản ghi loại tài khoản đang tồn tại; người dùng có quyền quản lý danh mục loại tài khoản.',
    '1. Người dùng bấm biểu tượng Xoá ở dòng cần xoá.\n'
    '2. Hệ thống hiển thị hộp thoại xác nhận nêu rõ tên loại tài khoản.\n'
    '3. Người dùng xác nhận.\n'
    '4. Hệ thống kiểm tra lại điều kiện xoá rồi xoá bản ghi.\n'
    '5. Hệ thống hiển thị thông báo thành công và tải lại danh sách.',
    '• Loại tài khoản đã được tài khoản kế toán sử dụng → Nút Xoá bị vô hiệu hoá và hệ thống '
    'không cho xoá.\n'
    '• Người dùng bấm Huỷ → Hệ thống đóng hộp thoại, không xoá gì.\n'
    '• Dữ liệu phát sinh ngay giữa lúc thao tác → Hệ thống chặn ở lần kiểm tra tại máy chủ.',
    '• Ràng buộc được kiểm tra ở cả giao diện lẫn máy chủ; kiểm tra tại máy chủ là chốt chặn cuối cùng.\n'
    '• Trường hợp không xoá được, cách xử lý đúng nghiệp vụ là chuyển sang trạng thái Khoá.')

d.h3('5.2.8.3 Layout màn hình')
d.layout()

d.h3('5.2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng Xoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Ẩn khi không có P1; vô hiệu hoá khi loại tài khoản đang được sử dụng'),
    ('Chú giải nút Xoá', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện khi rê chuột, nêu lý do bị chặn'),
    ('Hộp thoại xác nhận xoá', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Tiêu đề “Xác nhận xóa”, nội dung nêu tên loại tài khoản'),
    ('Xoá', 'Button', 'Enable', '–', '–', '–', 'Xác nhận xoá bản ghi'),
    ('Huỷ', 'Button', 'Enable', '–', '–', '–', 'Đóng hộp thoại, không xoá'),
    ('Thông báo chặn xoá', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Nêu lý do không xoá được'),
])

d.h3('5.2.8.5 Tiêu chí nghiệm thu')
d.bullets([
    'Loại tài khoản chưa được tài khoản nào sử dụng thì xoá được và biến mất khỏi danh sách.',
    'Loại tài khoản đã được sử dụng thì không xoá được, kể cả khi gọi trực tiếp API.',
    'Bấm Huỷ ở hộp thoại thì bản ghi vẫn còn nguyên.',
    'Người dùng chỉ có P2 gọi trực tiếp API xoá thì bị từ chối với lỗi 403.',
])

d.h3('5.2.8.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Xoá', 'Click',
     'Before:\n– Kiểm tra quyền P1 và điều kiện xoá; không đủ thì nút bị vô hiệu hoá kèm chú giải.\n'
     'After:\n– Mở hộp thoại “Xác nhận xóa”.'),
    ('Xác nhận xoá', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n– Loại tài khoản đang được sử dụng → hiển thị thông báo không xoá được kèm hướng dẫn '
     'chuyển sang trạng thái Khoá.\n'
     '– Nếu bị chặn → không thực hiện bước After.\n'
     'After:\n– Xoá bản ghi khỏi danh mục.\n'
     '– Hiển thị thông báo thành công và tải lại danh sách.'),
    ('Bấm Huỷ', 'Click', 'Đóng hộp thoại, không xoá bản ghi.'),
])

# ------------------------------------------------ 5.2.9
d.h2('5.2.9 Xem lịch sử chỉnh sửa loại tài khoản')

d.h3('5.2.9.1 Giới thiệu')
d.intro_table(
    'Xem lịch sử chỉnh sửa loại tài khoản',
    'Hiển thị danh sách các lần thay đổi thông tin của một loại tài khoản, mỗi lần nêu rõ trường '
    'thay đổi kèm giá trị trước và sau.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Bản ghi loại tài khoản đang tồn tại; người dùng đang ở màn hình danh sách.',
    '1. Người dùng bấm biểu tượng Lịch sử chỉnh sửa ở dòng cần xem.\n'
    '2. Hệ thống mở modal và tải danh sách các lần thay đổi của bản ghi đó.\n'
    '3. Hệ thống hiển thị theo thứ tự mới nhất trước.\n'
    '4. Người dùng xem xong thì bấm Đóng.',
    '• Bản ghi chưa từng được chỉnh sửa → Hiển thị thông báo chưa có lịch sử.\n'
    '• Không có quyền → Hệ thống trả về lỗi 403 và không mở modal.',
    'Chỉ 4 trường được theo dõi mới sinh bản ghi lịch sử: Mã loại tài khoản, Tên loại tài khoản, '
    'Ghi chú và Trạng thái.')

d.h3('5.2.9.2 Layout màn hình')
d.layout(modal='Lịch sử chỉnh sửa loại tài khoản')

d.h3('5.2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Modal Lịch sử chỉnh sửa', 'Modal', 'Read-only', '–', '–', 'Ẩn', 'Tiêu đề nêu rõ đối tượng đang xem'),
    ('Danh sách lần thay đổi', 'Table/Grid', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Mỗi dòng là một lần chỉnh sửa, sắp xếp mới nhất trước'),
    ('Người thực hiện', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống', 'Người đã chỉnh sửa'),
    ('Thời điểm', 'Text', 'Read-only', 'dd/mm/yyyy', '–', 'Lấy từ hệ thống', 'Thời điểm chỉnh sửa'),
    ('Trường thay đổi', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Tên trường bị thay đổi, hiển thị bằng nhãn tiếng Việt'),
    ('Giá trị trước / sau', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Giá trị cũ và giá trị mới, đã quy đổi sang nhãn hiển thị'),
    ('Trạng thái rỗng', 'Label', 'Enable', '–', '–', 'Ẩn', 'Hiển thị khi bản ghi chưa có lịch sử'),
    ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal'),
])

d.h3('5.2.9.4 Tiêu chí nghiệm thu')
d.bullets([
    'Sửa một trường được theo dõi thì lịch sử ghi đúng tên trường, giá trị trước và giá trị sau.',
    'Giá trị Trạng thái hiển thị bằng nhãn tiếng Việt, không hiển thị giá trị số.',
    'Lịch sử sắp xếp mới nhất trước.',
    'Bản ghi chưa từng chỉnh sửa thì hiển thị thông báo chưa có lịch sử.',
    'Người dùng chỉ có P2 vẫn xem được lịch sử.',
])

d.h3('5.2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Lịch sử chỉnh sửa', 'Click',
     'Tải danh sách lần thay đổi của bản ghi và mở modal ở chế độ chỉ đọc.'),
    ('Bấm Đóng', 'Click', 'Đóng modal.'),
])

# ------------------------------------------------ 5.2.10
d.h2('5.2.10 Xuất Excel danh mục loại tài khoản')

d.h3('5.2.10.1 Giới thiệu')
d.intro_table(
    'Xuất Excel danh mục loại tài khoản',
    'Cho phép người dùng tải danh sách loại tài khoản ra file Excel để đối chiếu hoặc gửi ra ngoài.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng đang ở màn hình danh sách loại tài khoản.',
    '1. Người dùng áp dụng bộ lọc mong muốn (không bắt buộc).\n'
    '2. Người dùng bấm nút Xuất Excel.\n'
    '3. Hệ thống dựng file theo đúng bộ lọc đang áp dụng và trả về cho trình duyệt tải xuống.',
    '• Không có dữ liệu khớp bộ lọc → Hệ thống vẫn trả file chỉ gồm dòng tiêu đề.\n'
    '• Xảy ra lỗi trong lúc dựng file → Hệ thống hiển thị thông báo lỗi, không tải file.',
    'File xuất ra lấy toàn bộ dữ liệu khớp bộ lọc, không giới hạn theo trang đang xem.')

d.h3('5.2.10.2 Layout màn hình')
d.layout()

d.h3('5.2.10.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Xuất Excel', 'Button', 'Enable', '–', '–', '–', 'Nằm ở thanh thao tác dưới bảng danh sách'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', 'Hiển thị khi không dựng được file'),
])

d.h3('5.2.10.4 Tiêu chí nghiệm thu')
d.bullets([
    'Dữ liệu trong file khớp đúng bộ lọc đang áp dụng trên màn hình.',
    'File chứa toàn bộ bản ghi khớp bộ lọc, không chỉ các dòng của trang đang xem.',
    'Người dùng chỉ có P2 vẫn xuất được Excel.',
    'Người dùng không có quyền gọi trực tiếp đường dẫn xuất Excel thì bị từ chối với lỗi 403.',
])

d.h3('5.2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Kiểm tra quyền P1 hoặc P2; không có quyền → trả về lỗi 403.\n'
     'After:\n– Dựng file Excel theo bộ lọc hiện tại và tải xuống.'),
])

# ------------------------------------------------ 5.2.11
d.h2('5.2.11 Nhập danh mục loại tài khoản từ Excel')

d.h3('5.2.11.1 Biểu đồ Usecase')
d.uc_figure('FR-11', 'Nhập danh mục loại tài khoản từ Excel', 'io',
            [('include', 'Kiểm tra dữ liệu trước khi ghi')])

d.h3('5.2.11.2 Giới thiệu')
d.intro_table(
    'Nhập danh mục loại tài khoản từ Excel',
    'Cho phép người quản lý danh mục khai báo nhiều loại tài khoản cùng lúc từ file Excel, '
    'có bước kiểm tra dữ liệu trước khi ghi.',
    'Admin; User được phân quyền P1',
    'Người dùng đang ở màn hình danh sách và có quyền quản lý danh mục loại tài khoản.',
    '1. Người dùng bấm nút Import Excel → Hệ thống mở modal nhập dữ liệu.\n'
    '2. Người dùng tải file mẫu, điền dữ liệu rồi dán hoặc tải lên bảng nhập gồm 4 cột.\n'
    '3. Người dùng bấm Kiểm tra dữ liệu.\n'
    '4. Hệ thống kiểm tra từng dòng và báo lỗi tại đúng dòng, đúng cột.\n'
    '5. Người dùng sửa các dòng lỗi rồi bấm Nhập dữ liệu.\n'
    '6. Hệ thống ghi các bản ghi hợp lệ và hiển thị kết quả nhập.\n'
    '7. Hệ thống đóng modal và tải lại danh sách.',
    '• Còn dòng lỗi → Hệ thống không cho ghi và yêu cầu sửa hết lỗi trước.\n'
    '• Cột Trạng thái để trống → Hệ thống hiểu là Hoạt động.\n'
    '• Người dùng đóng modal giữa chừng → Hệ thống huỷ toàn bộ dữ liệu đang nhập dở.',
    '• Bảng nhập gồm 4 cột: Mã loại tài khoản (*), Tên loại tài khoản (*), Ghi chú, Trạng thái.\n'
    '• Tiêu đề cột chấp nhận nhiều cách viết (có dấu, không dấu, viết tắt) để dùng lại được file '
    'mẫu cũ của hệ thống ERP.\n'
    '• Ràng buộc không trùng mã và không trùng tên được áp dụng cho từng dòng nhập, tính cả các '
    'dòng trong cùng một lần nhập.')

d.h3('5.2.11.3 Layout màn hình')
d.layout(modal='Import loại tài khoản')

d.h3('5.2.11.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Modal Import loại tài khoản', 'Modal', 'Enable', '–', '–', 'Ẩn', 'Mở khi bấm nút Import Excel'),
    ('Tải file mẫu', 'Button', 'Enable', '–', '–', '–', 'Tải về file Excel mẫu 4 cột'),
    ('Bảng nhập dữ liệu', 'Table/Grid', 'Enable', '–', '–', 'Trống',
     'Cho phép dán dữ liệu từ Excel hoặc nhập trực tiếp'),
    ('Mã loại tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống', 'Cột bắt buộc, không được trùng'),
    ('Tên loại tài khoản', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống', 'Cột bắt buộc, không được trùng'),
    ('Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Cột tuỳ chọn'),
    ('Trạng thái', 'Textbox', 'Enable', 'Hoạt động / Khoá', 'Không', 'Trống',
     'Để trống được hiểu là Hoạt động'),
    ('Kiểm tra dữ liệu', 'Button', 'Enable', '–', '–', '–', 'Kiểm tra toàn bộ dòng và đánh dấu lỗi'),
    ('Nhập dữ liệu', 'Button', 'Enable / Disable', '–', '–', 'Disable', 'Chỉ bật khi dữ liệu đã hợp lệ'),
    ('Thông báo lỗi theo dòng', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị tại đúng ô dữ liệu bị lỗi'),
    ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal và huỷ dữ liệu đang nhập'),
])

d.h3('5.2.11.5 Tiêu chí nghiệm thu')
d.bullets([
    'Dán dữ liệu từ Excel vào bảng nhập thì các cột được nhận đúng theo tiêu đề, kể cả tiêu đề '
    'viết không dấu.',
    'Dòng thiếu Mã hoặc Tên bị báo lỗi tại đúng dòng, đúng cột.',
    'Dòng có mã hoặc tên trùng với dữ liệu đã có bị báo lỗi.',
    'Hai dòng trong cùng một lần nhập trùng mã hoặc trùng tên nhau cũng bị báo lỗi.',
    'Cột Trạng thái để trống thì bản ghi được nhập ở trạng thái Hoạt động.',
    'Khi còn dòng lỗi thì nút Nhập dữ liệu không thực hiện được.',
    'Nhập thành công thì danh sách phía sau hiển thị đầy đủ các bản ghi vừa thêm.',
    'Người dùng chỉ có P2 gọi trực tiếp API nhập dữ liệu thì bị từ chối với lỗi 403.',
])

d.h3('5.2.11.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Import Excel', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì nút không hiển thị.\n'
     'After:\n– Mở modal nhập dữ liệu với bảng nhập trống.'),
    ('Dán dữ liệu vào bảng nhập', 'Change',
     'Nhận diện tiêu đề cột theo các cách viết được chấp nhận và điền dữ liệu vào đúng cột.'),
    ('Bấm Kiểm tra dữ liệu', 'Click',
     'During:\n'
     '– Thiếu Mã hoặc Tên → đánh dấu lỗi tại ô tương ứng\n'
     '– Mã hoặc Tên trùng dữ liệu đã có → đánh dấu lỗi\n'
     '– Mã hoặc Tên trùng giữa các dòng trong cùng lần nhập → đánh dấu lỗi\n'
     '– Trường vượt 255 ký tự → đánh dấu lỗi\n'
     'After:\n– Không còn lỗi → cho phép bấm Nhập dữ liệu.'),
    ('Bấm Nhập dữ liệu', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n– Còn dòng lỗi → không ghi bản ghi nào.\n'
     'After:\n– Ghi các bản ghi hợp lệ vào danh mục loại tài khoản.\n'
     '– Hiển thị kết quả nhập, đóng modal và tải lại danh sách.'),
    ('Bấm Đóng', 'Click', 'Đóng modal và huỷ toàn bộ dữ liệu đang nhập dở.'),
])

# ================================================================ 6. BUSINESS RULES
d.h1('6. Quy tắc nghiệp vụ (Business Rules)')

d.p('BR-01 — Mã và tên loại tài khoản đều là duy nhất')
d.bullets([
    'Mã loại tài khoản không được trùng với bất kỳ bản ghi nào khác.',
    'Tên loại tài khoản cũng không được trùng — đây là ràng buộc chặt hơn so với các danh mục khác, '
    'nhằm tránh nhầm lẫn khi chọn phân loại.',
    'Khi chỉnh sửa, phép kiểm tra trùng bỏ qua chính bản ghi đang sửa.',
    'Mã luôn được lưu ở dạng chữ in hoa và đã bỏ khoảng trắng thừa ở hai đầu.',
])

d.p('BR-02 — Giới hạn độ dài trường')
d.bullets([
    'Mã, Tên và Ghi chú đều tối đa 255 ký tự.',
    'Mã và Tên là trường bắt buộc; Ghi chú có thể để trống.',
])

d.p('BR-03 — Chặn xoá loại tài khoản đang được sử dụng')
d.bullets([
    'Không được xoá loại tài khoản đã được gán cho ít nhất một tài khoản kế toán.',
    'Trường hợp này chỉ được chuyển sang trạng thái Khoá.',
    'Ràng buộc được kiểm tra ở cả giao diện lẫn máy chủ.',
])

d.p('BR-04 — Điều kiện khoá / mở khoá')
d.bullets([
    'Chỉ khoá được loại tài khoản đang Hoạt động và chưa được tài khoản kế toán nào sử dụng.',
    'Mở khoá chỉ áp dụng cho loại tài khoản đang ở trạng thái Khoá và không bị ràng buộc điều kiện '
    'sử dụng.',
    'Chỉ loại tài khoản ở trạng thái Hoạt động mới xuất hiện trong ô chọn Loại tài khoản của màn '
    'Danh mục tài khoản.',
])

d.p('BR-05 — Trạng thái loại tài khoản')
d.bullets([
    'Loại tài khoản có 2 trạng thái: Hoạt động và Khoá.',
    'Thêm mới mà không chọn trạng thái thì mặc định là Hoạt động.',
    'Chỉnh sửa mà không gửi trạng thái thì giữ nguyên trạng thái cũ.',
])

d.p('BR-06 — Ghi lịch sử chỉnh sửa')
d.bullets([
    'Mỗi lần cập nhật, hệ thống ghi lại các trường đã thay đổi kèm giá trị trước và sau.',
    '4 trường được theo dõi: Mã loại tài khoản, Tên loại tài khoản, Ghi chú, Trạng thái.',
    'Giá trị Trạng thái được ghi bằng nhãn hiển thị chứ không phải giá trị số.',
])

d.p('BR-07 — Quy tắc nhập dữ liệu từ Excel')
d.bullets([
    'Hai cột bắt buộc: Mã loại tài khoản và Tên loại tài khoản.',
    'Cột Trạng thái để trống được hiểu là Hoạt động.',
    'Ràng buộc không trùng mã và không trùng tên áp dụng cho cả dữ liệu đã có lẫn các dòng trong '
    'cùng một lần nhập.',
    'Chỉ được ghi dữ liệu khi không còn dòng lỗi.',
])

d.p('BR-08 — Dữ liệu dùng chung với hệ thống ERP')
d.bullets([
    'Danh mục loại tài khoản dùng chung một nguồn dữ liệu với hệ thống ERP đang chạy song song.',
    'Màn hình HRM không đổi cấu trúc dữ liệu gốc để hai cổng cùng đọc ghi được.',
])

d.p('Chức năng liên quan: FR-01 … FR-11.')

d.save()
