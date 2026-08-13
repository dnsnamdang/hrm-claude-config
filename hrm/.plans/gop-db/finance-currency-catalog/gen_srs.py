# -*- coding: utf-8 -*-
"""Sinh SRS theo FORM CHUAN cho man 'Danh muc tien te' (phan he Tai chinh).

Nguon doi chieu (doc truc tiep tu code, khong lay lai srs.docx cu):
  BE  Modules/Finance/{Routes/api.php, Entities/Currency/Currency.php,
                       Http/Requests/Currency/CurrencyRequest.php,
                       Http/Controllers/V1/CurrencyController.php,
                       Services/CurrencyService.php}
      app/Console/Commands/UpdateExchangeRateCurrencyCommand.php + app/Console/Kernel.php
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (1115/1116)
  FE  hrm-client/pages/finance/currencies/index.vue
      hrm-client/components/modal/finance/currency-modal.vue
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
       r"\finance-currency-catalog\SRS - Danh mục tiền tệ.docx")

d = SrsDoc(
    out=OUT,
    menu='Phân hệ Tài chính → Danh mục → Danh mục tiền tệ',
    route='/finance/currencies',
    full_url='https://<host-hrm>/finance/currencies',
    img_prefix='cur_')

ACTOR_SYS = 'Hệ thống (tiến trình nền)'

# ================================================================ TRANG BIA
d.h1('SOFTWARE REQUIREMENTS SPECIFICATION (SRS)')
d.h2('Màn hình: Danh mục tiền tệ')
d.h2('Phân hệ: Tài chính – nhóm Danh mục')

d.info_table([
    ('Mã màn hình', 'TC-DM-CURRENCY'),
    ('Đường dẫn', '/finance/currencies'),
    ('Phiên bản', '1.0'),
    ('Ngày lập', '12/08/2026'),
    ('Người lập', '@junfoke'),
    ('Trạng thái tài liệu', 'Draft'),
    ('Nguồn đối chiếu', 'Màn ERP admin/accounting/currencies (bảng currencies trên DB gộp)'),
])

# ================================================================ 1. GIOI THIEU
d.h1('1. Giới thiệu')

d.h2('1.1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm (SRS) cho màn hình quản lý danh mục tiền tệ, nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa BA/PO/Dev/Test',
    'Là căn cứ nghiệm thu chức năng và phân quyền',
    'Làm rõ ràng buộc chặn xoá tiền tệ đã phát sinh dữ liệu ở nghiệp vụ khác — điểm khác biệt '
    'có chủ đích so với màn ERP cũ (ERP xoá thẳng, không kiểm tra)',
    'Đặc tả tiến trình nền cập nhật tỷ giá hằng ngày từ nguồn Vietcombank',
])

d.h2('1.2 Phạm vi')
d.p('Màn hình Danh mục tiền tệ cung cấp chức năng:')
d.bullets([
    'Xem danh sách tiền tệ, tìm kiếm nhanh và lọc nâng cao theo Mã / Tên / Trạng thái',
    'Sắp xếp phía máy chủ trên 5 cột và phân trang',
    'Thêm mới, chỉnh sửa, xem chi tiết tiền tệ qua modal ngay trên màn danh sách',
    'Khoá / Mở khoá tiền tệ ngay tại cột Trạng thái',
    'Xoá tiền tệ, có kiểm tra ràng buộc dữ liệu ở 27 cột thuộc 23 bảng nghiệp vụ',
    'Xuất danh sách ra file Excel theo đúng bộ lọc đang áp dụng',
    'Tiến trình nền cập nhật tỷ giá hằng ngày lúc 03:00',
])
d.p('Ngoài phạm vi:')
d.bullets([
    'Nhập dữ liệu từ file Excel (Import) và In danh sách — màn hình không có các chức năng này',
    'Lịch sử chỉnh sửa (version/history) — bảng dữ liệu không có cột audit nên không ghi vết được',
    'Thay đổi cấu trúc bảng dữ liệu: giữ nguyên schema đang dùng chung với ERP',
    'Phân quyền theo cấp / theo công ty — màn hình dùng chung một bộ dữ liệu cho toàn hệ thống',
])

d.h2('1.3 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Tiền tệ', 'Một đơn vị tiền được khai báo trong hệ thống, gồm mã, tên và tỷ giá quy đổi'),
    ('Tỷ giá', 'Tỷ giá bán của đồng tiền so với VNĐ; tối đa 999.999,99'),
    ('Tên gọi khác', 'Tên gọi phụ của đồng tiền, không bắt buộc (ví dụ: Đô la Mỹ)'),
    ('Định dạng VN', 'Cách viết số của người Việt: dấu chấm phân cách nghìn, dấu phẩy thập phân '
                     '(ví dụ 26.520,00)'),
    ('Đang được sử dụng', 'Tiền tệ đã phát sinh dữ liệu ở nghiệp vụ khác (báo giá, hoá đơn, '
                          'công nợ…) nên không được phép xoá'),
    ('Khoá', 'Trạng thái ngừng sử dụng: bản ghi vẫn còn trong danh mục nhưng không xuất hiện '
             'ở các danh sách chọn của màn khác'),
    ('P1', 'Quyền “Quản lý danh mục tiền tệ”'),
    ('P2', 'Quyền “Xem danh mục tiền tệ”'),
    ('Quick Search', 'Tìm kiếm nhanh'),
    ('Advanced Filter', 'Bộ lọc nâng cao'),
    ('SRS', 'Software Requirements Specification'),
], widths=[1.8, 4.2])

# ================================================================ 2. TONG QUAN
d.h1('2. Tổng quan')

d.h2('2.1 Bối cảnh nghiệp vụ')
d.p('Danh mục tiền tệ là dữ liệu nền tảng của toàn bộ nghiệp vụ có yếu tố ngoại tệ, dùng để:')
d.bullets([
    'Cung cấp danh sách đồng tiền cho báo giá, hợp đồng mua, hoá đơn, công nợ, tờ khai hải quan…',
    'Cung cấp tỷ giá quy đổi về VNĐ để hạch toán và tính giá',
    'Chuẩn hoá cách gọi tên đồng tiền trên toàn hệ thống',
])
d.p('Do đó cần:')
d.bullets([
    'Phân quyền rõ ràng giữa người quản lý danh mục và người chỉ tra cứu',
    'Ràng buộc nghiêm: không cho xoá đồng tiền đã phát sinh dữ liệu ở nghiệp vụ khác — '
    'trường hợp này chỉ được chuyển sang trạng thái Khoá',
    'Cập nhật tỷ giá tự động hằng ngày để số liệu quy đổi luôn theo sát thị trường',
    'Giữ nguyên dữ liệu dùng chung với hệ thống ERP đang chạy song song',
])

d.h2('2.2 Nhóm người dùng')
d.bullets([
    'Người dùng có quyền P1: được quản lý danh mục (thêm/sửa/khoá/xoá) và xuất Excel',
    'Người dùng có quyền P2: chỉ được xem/tra cứu và xuất Excel',
    'Người dùng không có P1/P2: bị chặn truy cập',
    'Hệ thống (tiến trình nền): tự động cập nhật tỷ giá, không cần đăng nhập',
])

# ================================================================ 3. PHAN QUYEN
d.h1('3. Phân quyền và kiểm soát truy cập')

d.h2('3.1 Danh sách quyền')
d.table(['Ký hiệu', 'Tên quyền', 'Mã quyền', 'Nhóm quyền'], [
    ('P1', 'Quản lý danh mục tiền tệ', '1115', 'Danh mục tài chính'),
    ('P2', 'Xem danh mục tiền tệ', '1116', 'Danh mục tài chính'),
], widths=[0.8, 2.8, 0.9, 1.5])
d.p('Ghi chú: màn hình tương ứng bên ERP không gate quyền nào, hai quyền trên là quyền mới của HRM.')

d.h2('3.2 Quy tắc truy cập bắt buộc')
d.bullets([
    'Chỉ user có P1 hoặc P2 mới được truy cập màn hình.',
    'User không có P1/P2: không hiển thị menu điều hướng tới màn hình.',
    'User không có P1/P2: truy cập trực tiếp URL bị chặn, gọi API trả về lỗi 403.',
    'User chỉ có P2: mọi thao tác ghi (thêm/sửa/khoá/mở khoá/xoá) bị chặn ở cả giao diện lẫn API '
    '(403), không phụ thuộc vào việc giao diện có ẩn nút hay không.',
    'Danh sách rút gọn phục vụ ô chọn tiền tệ ở các màn khác không gate quyền, '
    'vì mọi màn nghiệp vụ có ngoại tệ đều cần đọc danh sách này.',
])

d.h2('3.3 Ma trận phân quyền')
d.table(['Chức năng', 'P1', 'P2', 'Không có quyền'], [
    ('Truy cập màn', '✅', '✅', '❌'),
    ('Xem danh sách', '✅', '✅', '❌'),
    ('Tìm kiếm nhanh / Lọc nâng cao / Sắp xếp / Phân trang', '✅', '✅', '❌'),
    ('Xem chi tiết', '✅', '✅', '❌'),
    ('Thêm mới', '✅', '❌', '❌'),
    ('Chỉnh sửa', '✅', '❌', '❌'),
    ('Khoá / Mở khoá', '✅', '❌', '❌'),
    ('Xoá', '✅', '❌', '❌'),
    ('Xuất Excel', '✅', '✅', '❌'),
], widths=[3.0, 0.8, 0.8, 1.4])

# ================================================================ 4. FUNCTION LIST
d.h1('4. Danh mục chức năng (Function list)')
d.table(['ID', 'Chức năng', 'Mô tả đặc tả thu nhỏ (Mini-Spec)', 'Quyền'], [
    ('FR-01', 'Truy cập màn hình',
     'Kiểm tra quyền P1/P2. Không có quyền sẽ bị chặn (ẩn menu, chặn URL, API trả 403).', 'P1, P2'),
    ('FR-02', 'Xem danh sách',
     'Hiển thị bảng dữ liệu 7 cột, phân trang, mặc định sắp xếp theo thứ tự khai báo. '
     'Cờ “đang được sử dụng” nạp sau khi bảng hiển thị để vô hiệu hoá nút Xoá.', 'P1, P2'),
    ('FR-03', 'Tìm kiếm & Lọc',
     'Kết hợp Quick Search (mã / tên / tên gọi khác) và Advanced Filter (Mã, Tên, Trạng thái). '
     'Hỗ trợ sắp xếp phía máy chủ trên 5 cột.', 'P1, P2'),
    ('FR-04', 'Thêm mới',
     'Mở modal, nhập Mã (*), Tên (*), Tên gọi khác, Tỷ giá (*), Trạng thái. Mã tự viết hoa, '
     'tỷ giá nhận định dạng VN. Có nút Lưu & Tiếp tục để nhập liên tiếp.', 'P1'),
    ('FR-05', 'Chỉnh sửa',
     'Mở modal nạp sẵn dữ liệu, cho phép sửa toàn bộ trường và Trạng thái. '
     'Không gửi Trạng thái thì giữ nguyên giá trị cũ.', 'P1'),
    ('FR-06', 'Xem chi tiết',
     'Mở modal ở chế độ chỉ đọc, mọi trường bị vô hiệu hoá và ẩn nút Lưu.', 'P1, P2'),
    ('FR-07', 'Khoá / Mở khoá',
     'Đổi trạng thái ngay tại cột Trạng thái sau khi xác nhận. Chỉ đụng tới trạng thái, '
     'không ảnh hưởng dữ liệu khác.', 'P1'),
    ('FR-08', 'Xoá',
     'Xoá bản ghi sau khi xác nhận. Chặn khi tiền tệ đã phát sinh dữ liệu ở nghiệp vụ khác — '
     'kiểm tra 2 lớp (giao diện và máy chủ).', 'P1'),
    ('FR-09', 'Xuất Excel',
     'Xuất danh sách theo đúng bộ lọc đang áp dụng ra file Excel.', 'P1, P2'),
    ('FR-10', 'Cập nhật tỷ giá tự động',
     'Tiến trình nền chạy 03:00 hằng ngày, lấy tỷ giá bán từ nguồn Vietcombank và cập nhật '
     'cho mọi đồng tiền trừ VNĐ/VND.', 'Hệ thống'),
], widths=[0.7, 1.4, 3.4, 0.8])

# ================================================================ 5. DAC TA CHI TIET
d.h1('5. Đặc tả chi tiết theo từng chức năng (FUNCTIONAL PACKAGING)')

d.h2('5.1 Sơ đồ UML tổng quan')
d.p('Sơ đồ Use Case tổng quan của màn hình, thể hiện quan hệ giữa các nhóm người dùng và '
    'mười chức năng:')
d.overview_figure(
    'HỆ THỐNG HRM — Danh mục tiền tệ',
    [(ACTOR_P1, [0, 1, 2, 3, 4, 5, 6, 7, 8]),
     ('Người xem danh mục (P2)', [0, 1, 2, 5, 8]),
     (ACTOR_SYS, [9])],
    [('FR-01', 'Truy cập màn hình', 'view', None),
     ('FR-02', 'Xem danh sách', 'view', None),
     ('FR-03', 'Tìm kiếm & Lọc', 'view', None),
     ('FR-04', 'Thêm mới', 'crud', None),
     ('FR-05', 'Chỉnh sửa', 'crud', None),
     ('FR-06', 'Xem chi tiết', 'view', None),
     ('FR-07', 'Khoá / Mở khoá', 'action', None),
     ('FR-08', 'Xoá', 'action', '«include» Kiểm tra dữ liệu đang sử dụng'),
     ('FR-09', 'Xuất Excel', 'io', None),
     ('FR-10', 'Cập nhật tỷ giá tự động', 'io', None)],
    'Sơ đồ Use Case tổng quan màn hình Danh mục tiền tệ')

d.h2('5.2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------ 5.2.1 TRUY CAP
d.h2('5.2.1 Truy cập màn hình danh mục tiền tệ')

d.h3('5.2.1.1 Biểu đồ Usecase')
d.uc_figure('FR-01', 'Truy cập màn hình danh mục tiền tệ', 'view',
            [('include', 'Kiểm tra quyền truy cập')], actor=ACTOR_BOTH)

d.h3('5.2.1.2 Giới thiệu')
d.intro_table(
    'Truy cập màn hình danh mục tiền tệ',
    'Cho phép người dùng truy cập vào màn hình quản lý danh mục tiền tệ để tra cứu và quản lý '
    'dữ liệu tiền tệ.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng đã đăng nhập thành công vào hệ thống.',
    '1. Người dùng chọn menu Tài chính → Danh mục → Danh mục tiền tệ.\n'
    '2. Hệ thống xác thực quyền truy cập (P1 hoặc P2).\n'
    '3. Hệ thống điều hướng tới màn hình danh sách và tải dữ liệu trang đầu tiên.\n'
    '4. Hệ thống khôi phục bộ lọc đã lưu của lần truy cập trước (nếu còn hiệu lực).',
    '• Người dùng không có quyền → Hệ thống ẩn menu; truy cập trực tiếp URL bị chặn.\n'
    '• Gọi trực tiếp API khi không có quyền → Hệ thống trả về lỗi 403.\n'
    '• Bộ lọc đã lưu chứa cột sắp xếp không còn hợp lệ → Hệ thống tự bỏ điều kiện sắp xếp đó.',
    '')

d.h3('5.2.1.3 Layout màn hình')
d.layout('Ghi chú: tài liệu này không đính kèm ảnh chụp màn hình, người đọc truy cập trực tiếp '
         'đường dẫn trên để đối chiếu giao diện.')

d.h3('5.2.1.4 Tiêu chí nghiệm thu')
d.p('Người dùng có quyền truy cập:')
d.bullets([
    'Nhìn thấy menu Danh mục tiền tệ.',
    'Truy cập được màn hình danh sách.',
    'Hiển thị mặc định: danh sách phải hiển thị đúng cấu trúc bảng gồm STT, Mã tiền tệ, '
    'Tên tiền tệ, Tỷ giá (VNĐ), Cập nhật, Trạng thái, Hành động.',
])
d.p('Người dùng không có quyền:')
d.bullets([
    'Không nhìn thấy menu.',
    'Truy cập trực tiếp URL bị chặn, gọi API trả về 403.',
])

d.h3('5.2.1.5 Danh sách event và xử lý event')
d.event_table([
    ('Click menu Danh mục tiền tệ', 'Click',
     'Kiểm tra quyền (P1 hoặc P2) và điều hướng tới màn hình danh sách.'),
    ('Truy cập URL trực tiếp', 'System',
     'Kiểm tra quyền; nếu không hợp lệ → chặn truy cập (giao diện) và trả về lỗi 403 (API).'),
    ('Load màn hình', 'System',
     'Khôi phục bộ lọc đã lưu, loại bỏ điều kiện sắp xếp không hợp lệ, sau đó tải danh sách trang 1.'),
])

# ------------------------------------------------ 5.2.2 XEM DANH SACH
d.h2('5.2.2 Xem danh sách tiền tệ')

d.h3('5.2.2.1 Giới thiệu')
d.intro_table(
    'Xem danh sách tiền tệ',
    'Hiển thị danh sách các đồng tiền đã khai báo kèm tỷ giá quy đổi về VNĐ, thời điểm cập nhật '
    'gần nhất và trạng thái sử dụng.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng truy cập thành công màn hình danh mục tiền tệ.',
    '1. Hệ thống lấy danh sách tiền tệ theo bộ lọc hiện tại.\n'
    '2. Hệ thống hiển thị danh sách theo phân trang, mặc định sắp xếp theo thứ tự khai báo tăng dần.\n'
    '3. Sau khi bảng hiển thị, hệ thống nạp bổ sung cờ “đang được sử dụng” cho các dòng trên trang '
    'để vô hiệu hoá nút Xoá tương ứng.',
    '• Không có dữ liệu → Hiển thị dòng “Không có dữ liệu phù hợp bộ lọc.”.\n'
    '• Nạp cờ “đang được sử dụng” thất bại → Danh sách vẫn hiển thị bình thường, nút Xoá không bị '
    'vô hiệu hoá sẵn nhưng thao tác xoá vẫn bị chặn ở bước xác nhận.\n'
    '• Chưa có thời điểm cập nhật → Cột Cập nhật hiển thị dấu gạch ngang.',
    '• Cờ “đang được sử dụng” được nạp bằng một yêu cầu riêng sau khi bảng hiển thị, không gộp vào '
    'yêu cầu tải danh sách, để không làm chậm màn hình.\n'
    '• Danh sách hiển thị cả bản ghi Hoạt động lẫn bản ghi Khoá.')

d.h3('5.2.2.2 Layout màn hình')
d.layout()

d.h3('5.2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Bảng danh sách tiền tệ', 'Table/Grid', 'Enable', '–', '–', '–',
     'Hiển thị danh sách tiền tệ theo phân trang'),
    ('STT', 'Label', 'Enable', '–', '–', '–', 'Số thứ tự bản ghi, tính theo trang hiện tại'),
    ('Mã tiền tệ', 'Text', 'Enable', '0–255 ký tự', '–', 'Lấy từ hệ thống',
     'Mã đồng tiền, luôn hiển thị chữ in hoa. Cho phép sắp xếp'),
    ('Tên tiền tệ', 'Text', 'Enable', '0–255 ký tự', '–', 'Lấy từ hệ thống',
     'Tên đồng tiền; nếu có Tên gọi khác thì hiển thị thêm ở dòng phụ. Cho phép sắp xếp'),
    ('Tỷ giá (VNĐ)', 'Number', 'Enable', '0 < giá trị ≤ 999.999,99', '–', 'Lấy từ hệ thống',
     'Tỷ giá quy đổi, hiển thị theo định dạng VN với 2 chữ số thập phân. Cho phép sắp xếp'),
    ('Cập nhật', 'Text', 'Enable', '–', '–', 'Lấy từ hệ thống',
     'Thời điểm cập nhật gần nhất; hiển thị dấu gạch ngang nếu chưa có. Cho phép sắp xếp'),
    ('Trạng thái', 'Badge', 'Enable', 'Hoạt động / Khoá', '–', 'Lấy từ hệ thống',
     'Hiển thị trạng thái của tiền tệ. Cho phép sắp xếp'),
    ('Khoá / Mở khoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Nằm ngay trong cột Trạng thái. Ẩn khi người dùng không có P1; vô hiệu hoá khi trạng thái '
     'hiện tại không cho phép thao tác tương ứng'),
    ('Xem', 'Icon Button', 'Enable', '–', '–', '–', 'Mở modal xem chi tiết ở chế độ chỉ đọc'),
    ('Sửa', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Mở modal chỉnh sửa. Ẩn khi người dùng không có P1'),
    ('Xoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Xoá tiền tệ. Ẩn khi không có P1; vô hiệu hoá khi tiền tệ đang được sử dụng, '
     'chú giải nêu rõ nơi đang dùng'),
    ('Tạo mới', 'Button', 'Enable / Ẩn', '–', '–', '–',
     'Mở modal thêm mới. Ẩn khi người dùng không có P1'),
    ('Xuất Excel', 'Button', 'Enable', '–', '–', '–',
     'Tải file Excel theo bộ lọc đang áp dụng'),
    ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1', 'Điều hướng giữa các trang danh sách'),
    ('Chọn số dòng/trang', 'Dropdown', 'Enable', 'Danh sách', 'Không', '10',
     'Thay đổi số bản ghi hiển thị mỗi trang'),
    ('Trạng thái rỗng', 'Label', 'Enable', '–', '–', 'Ẩn',
     'Hiển thị “Không có dữ liệu phù hợp bộ lọc.” khi danh sách trống'),
    ('Loading', 'Loading', 'Hiển thị', '–', '–', 'Ẩn', 'Hiển thị trong lúc chờ tải danh sách'),
])

d.h3('5.2.2.4 Tiêu chí nghiệm thu')
d.bullets([
    'Danh sách hiển thị đủ cả bản ghi Hoạt động lẫn bản ghi Khoá.',
    'Mặc định sắp xếp theo thứ tự khai báo tăng dần khi chưa chọn cột sắp xếp nào.',
    'Tỷ giá hiển thị đúng định dạng VN, luôn có 2 chữ số thập phân (ví dụ 26.520,00).',
    'Tên gọi khác chỉ hiển thị khi bản ghi có khai báo, không hiển thị dòng phụ trống.',
    'Nút Xoá bị vô hiệu hoá đối với tiền tệ đang được sử dụng, chú giải nêu tên nơi đang dùng.',
    'Vào màn hình chỉ phát sinh đúng một yêu cầu tải danh sách, không tải lặp.',
    'Phân trang hoạt động đúng, không trùng hoặc thiếu dữ liệu.',
])

d.h3('5.2.2.5 Danh sách event và xử lý event')
d.event_table([
    ('Load danh sách', 'System',
     'Tải danh sách theo bộ lọc và phân trang hiện tại; hiển thị hiệu ứng chờ trong lúc tải.'),
    ('Danh sách hiển thị xong', 'System',
     'Gửi yêu cầu kiểm tra “đang được sử dụng” cho các dòng trên trang; nhận kết quả thì vô hiệu hoá '
     'nút Xoá tương ứng. Thất bại thì bỏ qua, không hiển thị lỗi.'),
    ('Đổi trang', 'Click', 'Tải lại danh sách theo trang mới, giữ nguyên bộ lọc.'),
    ('Đổi số dòng/trang', 'Change', 'Tải lại danh sách với số dòng mới, quay về trang 1.'),
])

# ------------------------------------------------ 5.2.3 TIM KIEM & LOC
d.h2('5.2.3 Tìm kiếm và lọc danh sách tiền tệ')

d.h3('5.2.3.1 Giới thiệu')
d.intro_table(
    'Tìm kiếm và lọc danh sách tiền tệ',
    'Cho phép người dùng thu hẹp danh sách theo từ khoá hoặc theo từng tiêu chí, và sắp xếp '
    'danh sách theo cột mong muốn.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng đang ở màn hình danh sách tiền tệ.',
    '1. Người dùng nhập từ khoá vào ô tìm kiếm nhanh hoặc mở bộ lọc nâng cao.\n'
    '2. Người dùng nhập/chọn các tiêu chí: Mã tiền tệ, Tên tiền tệ, Trạng thái.\n'
    '3. Người dùng bấm Tìm kiếm.\n'
    '4. Hệ thống lấy danh sách khớp điều kiện, quay về trang 1 và hiển thị kết quả.\n'
    '5. Người dùng có thể bấm tiêu đề cột để đổi thứ tự sắp xếp.',
    '• Bấm Làm mới → Hệ thống xoá toàn bộ điều kiện lọc và tải lại danh sách đầy đủ.\n'
    '• Không có kết quả → Hiển thị “Không có dữ liệu phù hợp bộ lọc.”.\n'
    '• Thay đổi tiêu chí ở bộ lọc nâng cao → Hệ thống tự tìm lại ngay, không cần bấm Tìm kiếm.',
    '• Ô tìm kiếm nhanh chỉ áp dụng khi người dùng bấm Tìm kiếm, để tránh gọi lại danh sách '
    'sau mỗi ký tự gõ vào.\n'
    '• Điều kiện lọc được ghi nhớ trong 10 phút, dùng lại khi quay về màn hình.')

d.h3('5.2.3.2 Layout màn hình')
d.layout()

d.h3('5.2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Khung bộ lọc', 'Modal', 'Enable', '–', '–', 'Thu gọn',
     'Khung “Bộ lọc danh mục tiền tệ”, có thể mở rộng / thu gọn'),
    ('Tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm theo mã, tên hoặc tên gọi khác'),
    ('Mã tiền tệ', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Lọc theo một phần của mã'),
    ('Tên tiền tệ', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Lọc theo một phần của tên'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khoá', 'Không', 'Trống',
     'Lọc theo trạng thái; để trống là lấy tất cả'),
    ('Tìm kiếm', 'Button', 'Enable', '–', '–', '–', 'Áp dụng bộ lọc và quay về trang 1'),
    ('Làm mới', 'Button', 'Enable', '–', '–', '–', 'Xoá toàn bộ điều kiện lọc và tải lại danh sách'),
    ('Tiêu đề cột sắp xếp', 'Button', 'Enable',
     'Mã / Tên / Tỷ giá / Cập nhật / Trạng thái', '–', 'Không sắp xếp',
     'Bấm để đổi chiều sắp xếp; sắp xếp thực hiện phía máy chủ'),
])

d.h3('5.2.3.4 Tiêu chí nghiệm thu')
d.bullets([
    'Tìm kiếm nhanh tìm được theo cả mã, tên và tên gọi khác.',
    'Từ khoá chứa ký tự đặc biệt của phép tìm gần đúng (ví dụ % hoặc _) vẫn được tìm như ký tự '
    'thông thường, không trả về toàn bộ danh sách.',
    'Kết hợp nhiều tiêu chí cho ra kết quả thoả mãn đồng thời tất cả tiêu chí.',
    'Bấm Tìm kiếm luôn quay về trang 1.',
    'Sắp xếp trên cả 5 cột đều đổi đúng thứ tự dữ liệu, không chỉ đổi mũi tên trên tiêu đề.',
    'Bấm Làm mới thì danh sách được tải lại đầy đủ, không giữ điều kiện cũ.',
])

d.h3('5.2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Nhập ô tìm kiếm nhanh', 'Keypress', 'Ghi nhận từ khoá, chưa gọi tìm kiếm.'),
    ('Bấm Tìm kiếm', 'Click', 'Quay về trang 1 và tải lại danh sách theo toàn bộ điều kiện lọc.'),
    ('Đổi tiêu chí lọc nâng cao', 'Change',
     'Quay về trang 1 và tải lại danh sách ngay theo điều kiện mới.'),
    ('Bấm Làm mới', 'Click', 'Xoá toàn bộ điều kiện lọc, quay về trang 1 và tải lại danh sách.'),
    ('Bấm tiêu đề cột', 'Click',
     'Đổi cột và chiều sắp xếp, tải lại danh sách. Cột không nằm trong danh sách được phép '
     'sắp xếp thì bỏ qua điều kiện sắp xếp.'),
])

# ------------------------------------------------ 5.2.4 THEM MOI
d.h2('5.2.4 Thêm mới tiền tệ')

d.h3('5.2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Thêm mới tiền tệ', 'crud',
            [('include', 'Kiểm tra trùng mã tiền tệ'),
             ('include', 'Chuẩn hoá mã và tỷ giá')])

d.h3('5.2.4.2 Giới thiệu')
d.intro_table(
    'Thêm mới tiền tệ',
    'Cho phép người quản lý danh mục khai báo một đồng tiền mới kèm tỷ giá quy đổi về VNĐ.',
    'Admin; User được phân quyền P1',
    'Người dùng đang ở màn hình danh sách và có quyền quản lý danh mục tiền tệ.',
    '1. Người dùng bấm nút Tạo mới → Hệ thống mở modal Thêm tiền tệ với các trường trống.\n'
    '2. Người dùng nhập Mã tiền tệ, Tên tiền tệ, Tên gọi khác (tuỳ chọn), Tỷ giá và chọn Trạng thái.\n'
    '3. Người dùng bấm Lưu.\n'
    '4. Hệ thống chuẩn hoá dữ liệu: mã viết hoa và bỏ khoảng trắng thừa, tỷ giá chuyển từ '
    'định dạng VN sang số.\n'
    '5. Hệ thống kiểm tra hợp lệ rồi lưu bản ghi.\n'
    '6. Hệ thống hiển thị thông báo thành công, đóng modal và tải lại danh sách.',
    '• Người dùng bấm Lưu & Tiếp tục → Hệ thống lưu bản ghi rồi giữ modal mở với các trường trống '
    'để nhập tiếp.\n'
    '• Người dùng bấm Đóng → Hệ thống đóng modal, không lưu gì.\n'
    '• Dữ liệu không hợp lệ → Hệ thống hiển thị lỗi ngay dưới từng trường và không lưu.\n'
    '• Không chọn Trạng thái → Hệ thống mặc định là Hoạt động.',
    '• Tỷ giá nhập theo định dạng VN (ví dụ 26.520,00); hệ thống tự chuyển đổi, người dùng không '
    'phải nhập theo định dạng máy.\n'
    '• Mã tiền tệ luôn được lưu ở dạng chữ in hoa, kể cả khi người dùng nhập chữ thường.')

d.h3('5.2.4.3 Layout màn hình')
d.layout(modal='Thêm tiền tệ')

d.h3('5.2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Modal Thêm tiền tệ', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Mở khi bấm Tạo mới; tiêu đề “Thêm tiền tệ”'),
    ('Mã tiền tệ', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống',
     'Mã đồng tiền, tự viết hoa khi lưu, không được trùng'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khoá', 'Không', 'Hoạt động',
     'Trạng thái sử dụng của tiền tệ'),
    ('Tên tiền tệ', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống', 'Tên đầy đủ của đồng tiền'),
    ('Tên gọi khác', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Tên gọi phụ, có thể bỏ trống'),
    ('Tỷ giá (VNĐ)', 'Textbox', 'Enable', '0 < giá trị ≤ 999.999,99', 'Có', 'Trống',
     'Nhập theo định dạng VN, hệ thống tự chuẩn hoá'),
    ('Lưu', 'Button', 'Enable', '–', '–', '–',
     'Kiểm tra hợp lệ và lưu bản ghi; vô hiệu hoá trong lúc đang gửi'),
    ('Lưu & Tiếp tục', 'Button', 'Enable', '–', '–', '–',
     'Lưu bản ghi và giữ modal mở để nhập tiếp; chỉ hiển thị ở chế độ thêm mới'),
    ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal, không lưu'),
    ('Thông báo lỗi theo trường', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị ngay dưới trường tương ứng kèm viền đỏ'),
])

d.h3('5.2.4.5 Tiêu chí nghiệm thu')
d.bullets([
    'Bỏ trống Mã / Tên / Tỷ giá thì không lưu được và hiển thị lỗi “Bắt buộc phải nhập”.',
    'Nhập mã đã tồn tại thì hiển thị lỗi “Mã tiền tệ đã tồn tại”.',
    'Nhập mã chữ thường thì bản ghi lưu xuống phải ở dạng chữ in hoa.',
    'Nhập tỷ giá theo định dạng VN (26.520,00) thì lưu đúng giá trị, không bị hiểu sai thành số khác.',
    'Nhập tỷ giá bằng 0 hoặc số âm thì hiển thị lỗi “Tỷ giá phải lớn hơn 0”.',
    'Nhập tỷ giá vượt 999.999,99 thì hiển thị lỗi “Tỷ giá tối đa 999.999,99”, không lưu.',
    'Không chọn Trạng thái thì bản ghi mới ở trạng thái Hoạt động.',
    'Bấm Lưu & Tiếp tục thì modal vẫn mở với các trường trống và danh sách phía sau đã có bản ghi mới.',
    'Người dùng chỉ có P2 gọi trực tiếp API tạo mới thì bị từ chối với lỗi 403.',
])

d.h3('5.2.4.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Tạo mới', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì nút không hiển thị.\n'
     'After:\n– Xoá dữ liệu cũ trong modal và mở modal Thêm tiền tệ.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n'
     '– Mã tiền tệ trống → hiển thị “Bắt buộc phải nhập”\n'
     '– Tên tiền tệ trống → hiển thị “Bắt buộc phải nhập”\n'
     '– Tỷ giá trống → hiển thị “Bắt buộc phải nhập”\n'
     '– Mã tiền tệ trùng → hiển thị “Mã tiền tệ đã tồn tại”\n'
     '– Tỷ giá không phải số → hiển thị “Tỷ giá phải là số”\n'
     '– Tỷ giá ≤ 0 → hiển thị “Tỷ giá phải lớn hơn 0”\n'
     '– Tỷ giá > 999.999,99 → hiển thị “Tỷ giá tối đa 999.999,99”\n'
     '– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Ghi bản ghi mới vào danh mục tiền tệ.\n'
     '– Hiển thị thông báo “Tạo tiền tệ thành công”, đóng modal và tải lại danh sách.'),
    ('Bấm Lưu & Tiếp tục', 'Click',
     'Xử lý như bấm Lưu; sau khi ghi thành công thì giữ modal mở và xoá trắng các trường '
     'để nhập bản ghi kế tiếp.'),
    ('Bấm Đóng', 'Click', 'Đóng modal và xoá dữ liệu đang nhập dở, không lưu bất kỳ thay đổi nào.'),
])

# ------------------------------------------------ 5.2.5 CHINH SUA
d.h2('5.2.5 Chỉnh sửa tiền tệ')

d.h3('5.2.5.1 Biểu đồ Usecase')
d.uc_figure('FR-05', 'Chỉnh sửa tiền tệ', 'crud',
            [('include', 'Kiểm tra trùng mã tiền tệ')])

d.h3('5.2.5.2 Giới thiệu')
d.intro_table(
    'Chỉnh sửa tiền tệ',
    'Cho phép người quản lý danh mục cập nhật thông tin và tỷ giá của một đồng tiền đã khai báo.',
    'Admin; User được phân quyền P1',
    'Bản ghi tiền tệ đang tồn tại; người dùng có quyền quản lý danh mục tiền tệ.',
    '1. Người dùng bấm biểu tượng Sửa ở dòng cần chỉnh sửa.\n'
    '2. Hệ thống mở modal Sửa tiền tệ và nạp sẵn dữ liệu hiện tại, tỷ giá hiển thị theo định dạng VN.\n'
    '3. Người dùng chỉnh sửa các trường cần thay đổi.\n'
    '4. Người dùng bấm Lưu.\n'
    '5. Hệ thống chuẩn hoá, kiểm tra hợp lệ rồi cập nhật bản ghi.\n'
    '6. Hệ thống hiển thị thông báo thành công, đóng modal và tải lại danh sách.',
    '• Bản ghi đã bị xoá bởi người dùng khác → Hệ thống báo dữ liệu đã thay đổi và yêu cầu tải lại.\n'
    '• Mã mới trùng với bản ghi khác → Hệ thống báo lỗi và không lưu.\n'
    '• Không gửi Trạng thái → Hệ thống giữ nguyên trạng thái cũ.',
    '• Kiểm tra trùng mã bỏ qua chính bản ghi đang sửa.\n'
    '• Tỷ giá sửa tay có thể bị tiến trình cập nhật tự động ghi đè vào 03:00 hôm sau — '
    'đây là hành vi có chủ đích, cần thông báo rõ cho người dùng cuối.')

d.h3('5.2.5.3 Layout màn hình')
d.layout(modal='Sửa tiền tệ')

d.h3('5.2.5.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Modal Sửa tiền tệ', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Mở khi bấm biểu tượng Sửa; tiêu đề “Sửa tiền tệ”'),
    ('Thông tin cập nhật gần nhất', 'Label', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Hiển thị trên tiêu đề modal khi bản ghi đã có lịch sử cập nhật'),
    ('Mã tiền tệ', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Lấy từ hệ thống', 'Cho phép sửa, không được trùng'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Hoạt động / Khoá', 'Không', 'Lấy từ hệ thống', 'Cho phép đổi trạng thái'),
    ('Tên tiền tệ', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Lấy từ hệ thống', 'Cho phép sửa'),
    ('Tên gọi khác', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Lấy từ hệ thống', 'Cho phép sửa hoặc xoá trống'),
    ('Tỷ giá (VNĐ)', 'Textbox', 'Enable', '0 < giá trị ≤ 999.999,99', 'Có', 'Lấy từ hệ thống',
     'Hiển thị theo định dạng VN, cho phép sửa'),
    ('Lưu', 'Button', 'Enable', '–', '–', '–', 'Kiểm tra hợp lệ và cập nhật bản ghi'),
    ('Đóng', 'Button', 'Enable', '–', '–', '–', 'Đóng modal, huỷ thay đổi chưa lưu'),
])

d.h3('5.2.5.5 Tiêu chí nghiệm thu')
d.bullets([
    'Modal nạp đúng dữ liệu của dòng được chọn, tỷ giá hiển thị theo định dạng VN.',
    'Mở modal rồi bấm Lưu mà không sửa gì thì tỷ giá không bị đổi giá trị.',
    'Đổi mã trùng với bản ghi khác thì báo lỗi “Mã tiền tệ đã tồn tại”, giữ nguyên mã cũ.',
    'Giữ nguyên mã của chính bản ghi đang sửa thì lưu được bình thường.',
    'Xoá trống Tên gọi khác thì bản ghi được cập nhật thành không có tên gọi khác.',
    'Đổi Trạng thái sang Khoá thì danh sách hiển thị đúng trạng thái mới.',
    'Người dùng chỉ có P2 gọi trực tiếp API cập nhật thì bị từ chối với lỗi 403.',
])

d.h3('5.2.5.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Sửa', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì biểu tượng không hiển thị.\n'
     'After:\n– Nạp dữ liệu bản ghi, chuyển tỷ giá sang định dạng VN và mở modal Sửa tiền tệ.'),
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n'
     '– Mã / Tên / Tỷ giá trống → hiển thị “Bắt buộc phải nhập”\n'
     '– Mã trùng bản ghi khác → hiển thị “Mã tiền tệ đã tồn tại”\n'
     '– Tỷ giá ngoài khoảng cho phép → hiển thị thông báo lỗi tương ứng\n'
     '– Nếu có lỗi validate → không thực hiện bước After.\n'
     'After:\n– Cập nhật bản ghi trong danh mục tiền tệ.\n'
     '– Hiển thị thông báo “Cập nhật tiền tệ thành công”, đóng modal và tải lại danh sách.'),
    ('Bản ghi không còn tồn tại', 'System',
     'Hiển thị thông báo dữ liệu đã thay đổi và yêu cầu tải lại danh sách.'),
])

# ------------------------------------------------ 5.2.6 XEM CHI TIET
d.h2('5.2.6 Xem chi tiết tiền tệ')

d.h3('5.2.6.1 Giới thiệu')
d.intro_table(
    'Xem chi tiết tiền tệ',
    'Cho phép người dùng xem đầy đủ thông tin của một đồng tiền mà không thay đổi dữ liệu.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Bản ghi tiền tệ đang tồn tại; người dùng đang ở màn hình danh sách.',
    '1. Người dùng bấm biểu tượng Xem ở dòng cần xem.\n'
    '2. Hệ thống mở modal ở chế độ chỉ đọc và nạp dữ liệu bản ghi.\n'
    '3. Người dùng xem xong thì bấm Đóng.',
    '• Không có quyền → Hệ thống trả về lỗi 403 và không mở modal.\n'
    '• Bản ghi không còn tồn tại → Hệ thống báo dữ liệu đã thay đổi và yêu cầu tải lại.',
    'Ở chế độ chỉ đọc, toàn bộ trường nhập bị vô hiệu hoá và các nút Lưu không hiển thị.')

d.h3('5.2.6.2 Layout màn hình')
d.layout(modal='Xem tiền tệ')

d.h3('5.2.6.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Modal Xem tiền tệ', 'Modal', 'Read-only', '–', '–', 'Ẩn', 'Tiêu đề “Xem tiền tệ”'),
    ('Mã tiền tệ', 'Textbox', 'Disable', '–', '–', 'Lấy từ hệ thống', 'Chỉ đọc'),
    ('Trạng thái', 'Dropdown', 'Disable', '–', '–', 'Lấy từ hệ thống', 'Chỉ đọc'),
    ('Tên tiền tệ', 'Textbox', 'Disable', '–', '–', 'Lấy từ hệ thống', 'Chỉ đọc'),
    ('Tên gọi khác', 'Textbox', 'Disable', '–', '–', 'Lấy từ hệ thống', 'Chỉ đọc'),
    ('Tỷ giá (VNĐ)', 'Textbox', 'Disable', '–', '–', 'Lấy từ hệ thống', 'Chỉ đọc, hiển thị định dạng VN'),
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

# ------------------------------------------------ 5.2.7 KHOA / MO KHOA
d.h2('5.2.7 Khoá / Mở khoá tiền tệ')

d.h3('5.2.7.1 Biểu đồ Usecase')
d.uc_figure('FR-07', 'Khoá / Mở khoá tiền tệ', 'action',
            [('include', 'Kiểm tra trạng thái hiện tại')])

d.h3('5.2.7.2 Giới thiệu')
d.intro_table(
    'Khoá / Mở khoá tiền tệ',
    'Cho phép người quản lý danh mục ngừng sử dụng một đồng tiền mà vẫn giữ lại dữ liệu lịch sử, '
    'hoặc cho dùng lại đồng tiền đã khoá.',
    'Admin; User được phân quyền P1',
    'Bản ghi tiền tệ đang tồn tại; người dùng có quyền quản lý danh mục tiền tệ.',
    '1. Người dùng bấm biểu tượng Khoá (hoặc Mở khoá) ở cột Trạng thái.\n'
    '2. Hệ thống hiển thị hộp thoại xác nhận nêu rõ tên đồng tiền và hành động sắp thực hiện.\n'
    '3. Người dùng xác nhận.\n'
    '4. Hệ thống đổi trạng thái bản ghi và hiển thị thông báo thành công.\n'
    '5. Hệ thống tải lại danh sách.',
    '• Người dùng bấm Huỷ → Hệ thống đóng hộp thoại, không thay đổi gì.\n'
    '• Bản ghi đã bị người khác đổi trạng thái trước đó → Hệ thống báo lỗi tương ứng '
    '(“Tiền tệ đang bị khóa” hoặc “Tiền tệ đang hoạt động”) và không đổi thêm.',
    '• Thao tác chỉ thay đổi trạng thái, không ảnh hưởng các thông tin khác của bản ghi.\n'
    '• Tiền tệ đang khoá không xuất hiện trong ô chọn tiền tệ của các màn nghiệp vụ khác, '
    'nhưng dữ liệu cũ đã dùng đồng tiền đó vẫn giữ nguyên.')

d.h3('5.2.7.3 Layout màn hình')
d.layout()

d.h3('5.2.7.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng Khoá / Mở khoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Nằm trong cột Trạng thái; biểu tượng đổi theo trạng thái hiện tại. Ẩn khi không có P1'),
    ('Chú giải nút', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện khi rê chuột: “Khoá” / “Mở khoá” hoặc lý do không thao tác được'),
    ('Hộp thoại xác nhận', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Tiêu đề “Xác nhận khóa” / “Xác nhận mở khóa”, nội dung nêu rõ tên đồng tiền'),
    ('Nút xác nhận', 'Button', 'Enable', '–', '–', '–', 'Nhãn “Khóa” hoặc “Mở khóa”'),
    ('Huỷ', 'Button', 'Enable', '–', '–', '–', 'Đóng hộp thoại, không thực hiện gì'),
])

d.h3('5.2.7.5 Tiêu chí nghiệm thu')
d.bullets([
    'Tiền tệ đang Hoạt động: nút hiển thị hành động Khoá; tiền tệ đang Khoá: nút hiển thị hành động Mở khoá.',
    'Nút bị vô hiệu hoá khi trạng thái hiện tại không cho phép hành động tương ứng.',
    'Xác nhận Khoá thì trạng thái đổi thành Khoá và danh sách hiển thị đúng ngay sau đó.',
    'Bấm Huỷ thì trạng thái giữ nguyên.',
    'Tiền tệ đang Khoá không còn xuất hiện trong ô chọn tiền tệ ở các màn nghiệp vụ khác.',
    'Người dùng chỉ có P2 gọi trực tiếp API khoá/mở khoá thì bị từ chối với lỗi 403.',
])

d.h3('5.2.7.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Khoá / Mở khoá', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì biểu tượng không hiển thị.\n'
     'After:\n– Mở hộp thoại xác nhận với nội dung tương ứng hành động.'),
    ('Xác nhận trong hộp thoại', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n'
     '– Tiền tệ đã ở trạng thái Khoá mà yêu cầu khoá → hiển thị “Tiền tệ đang bị khóa”\n'
     '– Tiền tệ đã ở trạng thái Hoạt động mà yêu cầu mở khoá → hiển thị “Tiền tệ đang hoạt động”\n'
     '– Nếu có lỗi → không thực hiện bước After.\n'
     'After:\n– Cập nhật trạng thái bản ghi.\n'
     '– Hiển thị “Khóa tiền tệ thành công” / “Mở khóa tiền tệ thành công” và tải lại danh sách.'),
    ('Bấm Huỷ', 'Click', 'Đóng hộp thoại, không thay đổi trạng thái.'),
])

# ------------------------------------------------ 5.2.8 XOA
d.h2('5.2.8 Xoá tiền tệ')

d.h3('5.2.8.1 Biểu đồ Usecase')
d.uc_figure('FR-08', 'Xoá tiền tệ', 'action',
            [('include', 'Kiểm tra dữ liệu đang sử dụng'),
             ('extend', 'Chuyển sang trạng thái Khoá khi không xoá được')])

d.h3('5.2.8.2 Giới thiệu')
d.intro_table(
    'Xoá tiền tệ',
    'Cho phép người quản lý danh mục xoá một đồng tiền khai báo nhầm hoặc không còn dùng, '
    'với điều kiện đồng tiền đó chưa phát sinh dữ liệu ở nghiệp vụ khác.',
    'Admin; User được phân quyền P1',
    'Bản ghi tiền tệ đang tồn tại; người dùng có quyền quản lý danh mục tiền tệ.',
    '1. Người dùng bấm biểu tượng Xoá ở dòng cần xoá.\n'
    '2. Hệ thống kiểm tra đồng tiền có đang được sử dụng ở nghiệp vụ khác hay không.\n'
    '3. Nếu chưa được sử dụng → Hệ thống hiển thị hộp thoại xác nhận.\n'
    '4. Người dùng xác nhận → Hệ thống kiểm tra lại lần nữa rồi xoá bản ghi.\n'
    '5. Hệ thống hiển thị thông báo thành công và tải lại danh sách.',
    '• Đồng tiền đang được sử dụng → Nút Xoá bị vô hiệu hoá, chú giải nêu tối đa 3 nơi đang dùng '
    'và hệ thống không mở hộp thoại xác nhận.\n'
    '• Người dùng bấm Huỷ → Hệ thống đóng hộp thoại, không xoá gì.\n'
    '• Dữ liệu phát sinh ngay giữa lúc thao tác → Hệ thống chặn ở lần kiểm tra thứ hai và báo lỗi '
    'nêu rõ nơi đang sử dụng.',
    '• Ràng buộc chặn xoá được kiểm tra 2 lớp: một lần trước khi mở hộp thoại xác nhận và một lần '
    'tại máy chủ trước khi xoá thật. Đây là điểm khác có chủ đích so với màn ERP cũ '
    '(ERP xoá thẳng, không kiểm tra).\n'
    '• Trường hợp không xoá được, cách xử lý đúng nghiệp vụ là chuyển đồng tiền sang trạng thái Khoá.')

d.h3('5.2.8.3 Layout màn hình')
d.layout()

d.h3('5.2.8.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Biểu tượng Xoá', 'Icon Button', 'Enable / Ẩn', '–', '–', '–',
     'Ẩn khi không có P1; vô hiệu hoá khi đồng tiền đang được sử dụng hoặc đang chờ kết quả kiểm tra'),
    ('Chú giải nút Xoá', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiện khi rê chuột: “Xóa” hoặc thông báo nêu nơi đang sử dụng'),
    ('Hộp thoại xác nhận xoá', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Tiêu đề “Xác nhận xóa”, nội dung nêu rõ tên đồng tiền'),
    ('Xoá', 'Button', 'Enable', '–', '–', '–', 'Xác nhận xoá bản ghi'),
    ('Huỷ', 'Button', 'Enable', '–', '–', '–', 'Đóng hộp thoại, không xoá'),
    ('Thông báo chặn xoá', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Nêu tên các nghiệp vụ đang sử dụng đồng tiền (tối đa 3 nơi)'),
])

d.h3('5.2.8.5 Tiêu chí nghiệm thu')
d.bullets([
    'Đồng tiền chưa phát sinh dữ liệu ở nghiệp vụ nào thì xoá được và biến mất khỏi danh sách.',
    'Đồng tiền đã dùng ở báo giá / hoá đơn / công nợ… thì nút Xoá bị vô hiệu hoá và không xoá được.',
    'Gọi trực tiếp API xoá đối với đồng tiền đang được sử dụng vẫn bị chặn, kèm thông báo nêu '
    'nơi đang sử dụng — không phụ thuộc vào việc giao diện có chặn hay không.',
    'Thông báo chặn xoá nêu tối đa 3 nơi đang sử dụng.',
    'Bấm Huỷ ở hộp thoại thì bản ghi vẫn còn nguyên.',
    'Người dùng chỉ có P2 gọi trực tiếp API xoá thì bị từ chối với lỗi 403.',
])

d.h3('5.2.8.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm biểu tượng Xoá', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì biểu tượng không hiển thị.\n'
     'During:\n– Kiểm tra đồng tiền có đang được sử dụng không.\n'
     '– Đang được sử dụng → hiển thị thông báo nêu nơi đang dùng và KHÔNG mở hộp thoại xác nhận.\n'
     'After:\n– Chưa được sử dụng → mở hộp thoại “Xác nhận xóa”.'),
    ('Xác nhận xoá', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     'During:\n'
     '– Kiểm tra lại ràng buộc tại máy chủ; nếu đang được sử dụng → hiển thị thông báo nêu nơi đang '
     'dùng kèm hướng dẫn chuyển sang trạng thái Khoá.\n'
     '– Nếu bị chặn → không thực hiện bước After.\n'
     'After:\n– Xoá bản ghi khỏi danh mục tiền tệ.\n'
     '– Hiển thị thông báo “Xóa tiền tệ thành công” và tải lại danh sách.'),
    ('Bấm Huỷ', 'Click', 'Đóng hộp thoại, không xoá bản ghi.'),
])

# ------------------------------------------------ 5.2.9 XUAT EXCEL
d.h2('5.2.9 Xuất Excel danh mục tiền tệ')

d.h3('5.2.9.1 Giới thiệu')
d.intro_table(
    'Xuất Excel danh mục tiền tệ',
    'Cho phép người dùng tải danh sách tiền tệ ra file Excel để đối chiếu hoặc gửi ra ngoài.',
    'Admin; User được phân quyền (P1 hoặc P2)',
    'Người dùng đang ở màn hình danh sách tiền tệ.',
    '1. Người dùng áp dụng bộ lọc mong muốn (không bắt buộc).\n'
    '2. Người dùng bấm nút Xuất Excel.\n'
    '3. Hệ thống dựng file theo đúng bộ lọc đang áp dụng và trả về cho trình duyệt tải xuống.',
    '• Không có dữ liệu khớp bộ lọc → Hệ thống vẫn trả file chỉ gồm dòng tiêu đề.\n'
    '• Xảy ra lỗi trong lúc dựng file → Hệ thống hiển thị thông báo lỗi, không tải file.',
    '• File xuất ra lấy toàn bộ dữ liệu khớp bộ lọc, không giới hạn theo trang đang xem.')

d.h3('5.2.9.2 Layout màn hình')
d.layout()

d.h3('5.2.9.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Xuất Excel', 'Button', 'Enable', '–', '–', '–',
     'Nằm ở thanh thao tác dưới bảng danh sách'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị khi không dựng được file'),
])

d.h3('5.2.9.4 Tiêu chí nghiệm thu')
d.bullets([
    'File tải về có tên danh_muc_tien_te.xlsx.',
    'Dữ liệu trong file khớp đúng bộ lọc đang áp dụng trên màn hình.',
    'File chứa toàn bộ bản ghi khớp bộ lọc, không chỉ các dòng của trang đang xem.',
    'Người dùng chỉ có P2 vẫn xuất được Excel.',
    'Người dùng không có quyền gọi trực tiếp đường dẫn xuất Excel thì bị từ chối với lỗi 403.',
])

d.h3('5.2.9.5 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Kiểm tra quyền P1 hoặc P2; không có quyền → trả về lỗi 403.\n'
     'After:\n– Dựng file Excel theo bộ lọc hiện tại và tải xuống với tên danh_muc_tien_te.xlsx.'),
])

# ------------------------------------------------ 5.2.10 CRON
d.h2('5.2.10 Cập nhật tỷ giá tự động hằng ngày')

d.h3('5.2.10.1 Biểu đồ Usecase')
d.uc_figure('FR-10', 'Cập nhật tỷ giá tự động', 'io',
            [('include', 'Lấy dữ liệu tỷ giá từ nguồn ngoài'),
             ('include', 'Kiểm tra giá trị hợp lệ')],
            actor=ACTOR_SYS)

d.h3('5.2.10.2 Giới thiệu')
d.intro_table(
    'Cập nhật tỷ giá tự động hằng ngày',
    'Tiến trình nền tự động lấy tỷ giá bán mới nhất từ nguồn công bố của ngân hàng và cập nhật '
    'vào danh mục tiền tệ, để người dùng không phải nhập tay hằng ngày.',
    'Hệ thống (tiến trình nền, không cần đăng nhập)',
    'Tiến trình nền của hệ thống đang hoạt động và máy chủ kết nối được tới nguồn dữ liệu tỷ giá.',
    '1. Đúng 03:00 hằng ngày (giờ Việt Nam), hệ thống khởi chạy tiến trình cập nhật tỷ giá.\n'
    '2. Hệ thống tải dữ liệu tỷ giá từ nguồn công bố.\n'
    '3. Hệ thống đọc toàn bộ tỷ giá bán trong dữ liệu nguồn.\n'
    '4. Hệ thống lấy danh sách tiền tệ trong danh mục, trừ đồng tiền gốc VNĐ/VND.\n'
    '5. Với từng đồng tiền, hệ thống cập nhật tỷ giá mới nếu giá trị hợp lệ và khác giá trị hiện tại.\n'
    '6. Hệ thống ghi lại số bản ghi đã cập nhật và số bản ghi bỏ qua.',
    '• Không tải được dữ liệu nguồn hoặc dữ liệu hỏng → Hệ thống dừng, ghi lỗi và không cập nhật '
    'bản ghi nào.\n'
    '• Đồng tiền không có trong dữ liệu nguồn → Hệ thống bỏ qua, giữ nguyên tỷ giá cũ.\n'
    '• Tỷ giá nguồn ≤ 0 hoặc vượt 999.999,99 → Hệ thống cảnh báo, ghi lại và bỏ qua bản ghi đó.\n'
    '• Tỷ giá nguồn bằng tỷ giá hiện tại (so tới 2 chữ số thập phân) → Hệ thống bỏ qua, không ghi thừa.',
    '• Tiến trình cùng chức năng bên hệ thống ERP đã được tắt, HRM là nơi duy nhất cập nhật tự động.\n'
    '• Tỷ giá do người dùng sửa tay có thể bị tiến trình này ghi đè vào lần chạy kế tiếp.')

d.h3('5.2.10.3 Layout màn hình')
d.p('Chức năng chạy nền, không có giao diện. Kết quả được phản ánh ở cột Tỷ giá (VNĐ) và cột '
    'Cập nhật của màn hình danh sách:')
d.bullets([
    'Menu: Phân hệ Tài chính → Danh mục → Danh mục tiền tệ',
    'Route (FE): /finance/currencies',
])

d.h3('5.2.10.4 Tiêu chí nghiệm thu')
d.bullets([
    'Tiến trình chạy đúng 03:00 hằng ngày theo giờ Việt Nam.',
    'Đồng tiền VNĐ/VND không bao giờ bị thay đổi tỷ giá.',
    'Đồng tiền đứng đầu dữ liệu nguồn cũng được cập nhật như các đồng tiền khác.',
    'Tỷ giá nguồn vượt trần cho phép thì bị bỏ qua và được ghi lại, không làm hỏng dữ liệu.',
    'Tỷ giá không đổi thì bản ghi không bị cập nhật thừa (thời điểm cập nhật giữ nguyên).',
    'Nguồn dữ liệu lỗi thì tiến trình dừng lại và ghi rõ lý do, không cập nhật sai dữ liệu.',
])

d.h3('5.2.10.5 Danh sách event và xử lý event')
d.event_table([
    ('Đến giờ chạy định kỳ', 'System',
     'Khởi chạy tiến trình cập nhật tỷ giá của phân hệ Tài chính.'),
    ('Tải dữ liệu nguồn', 'System',
     'During:\n– Lỗi kết nối, phản hồi không hợp lệ hoặc dữ liệu hỏng → ghi lỗi và kết thúc với '
     'trạng thái thất bại.\n'
     'After:\n– Đọc toàn bộ tỷ giá bán trong dữ liệu nguồn.'),
    ('Duyệt từng đồng tiền', 'System',
     'During:\n– Đồng tiền thuộc nhóm bỏ qua (VNĐ/VND) → không xử lý\n'
     '– Không có trong dữ liệu nguồn → bỏ qua\n'
     '– Tỷ giá ≤ 0 hoặc > 999.999,99 → cảnh báo, ghi lại và bỏ qua\n'
     '– Tỷ giá bằng giá trị hiện tại (so 2 chữ số thập phân) → bỏ qua\n'
     'After:\n– Cập nhật tỷ giá mới cho đồng tiền tương ứng.'),
    ('Kết thúc tiến trình', 'System',
     'Ghi lại số bản ghi đã cập nhật và số bản ghi bỏ qua.'),
])

# ================================================================ 6. BUSINESS RULES
d.h1('6. Quy tắc nghiệp vụ (Business Rules)')

d.p('BR-01 — Mã tiền tệ là duy nhất')
d.bullets([
    'Mã tiền tệ không được trùng với bất kỳ bản ghi nào khác trong danh mục.',
    'Khi chỉnh sửa, phép kiểm tra trùng bỏ qua chính bản ghi đang sửa.',
    'Mã luôn được lưu ở dạng chữ in hoa và đã bỏ khoảng trắng thừa ở hai đầu.',
])

d.p('BR-02 — Tỷ giá bắt buộc và nằm trong khoảng cho phép')
d.bullets([
    'Tỷ giá là trường bắt buộc, phải là số và lớn hơn 0.',
    'Tỷ giá tối đa là 999.999,99 — vượt trần thì bị chặn ngay khi lưu.',
])

d.p('BR-03 — Chấp nhận tỷ giá theo định dạng Việt Nam')
d.bullets([
    'Người dùng nhập tỷ giá theo thói quen Việt Nam: dấu chấm phân cách nghìn, dấu phẩy thập phân.',
    'Hệ thống tự chuyển đổi trước khi kiểm tra hợp lệ và lưu, ví dụ 999.999,99 được hiểu là 999999,99.',
    'Khi mở lại bản ghi để sửa, tỷ giá được hiển thị lại theo đúng định dạng Việt Nam.',
])

d.p('BR-04 — Chặn xoá tiền tệ đã phát sinh dữ liệu')
d.bullets([
    'Không được xoá đồng tiền đã được sử dụng ở bất kỳ nghiệp vụ nào (báo giá, hợp đồng mua, '
    'hoá đơn, công nợ, tờ khai hải quan, bảo hiểm, chi tiết tài khoản…).',
    'Thông báo chặn xoá nêu tối đa 3 nơi đang sử dụng.',
    'Trường hợp này chỉ được chuyển đồng tiền sang trạng thái Khoá.',
    'Ràng buộc được kiểm tra ở cả giao diện lẫn máy chủ; kiểm tra tại máy chủ là chốt chặn cuối cùng.',
])

d.p('BR-05 — Trạng thái tiền tệ')
d.bullets([
    'Tiền tệ có 2 trạng thái: Hoạt động và Khoá.',
    'Thêm mới mà không chọn trạng thái thì mặc định là Hoạt động.',
    'Chỉnh sửa mà không gửi trạng thái thì giữ nguyên trạng thái cũ.',
    'Chỉ tiền tệ ở trạng thái Hoạt động mới xuất hiện trong ô chọn tiền tệ của các màn nghiệp vụ khác.',
])

d.p('BR-06 — Kiểm tra “đang được sử dụng” tách khỏi lượt tải danh sách')
d.bullets([
    'Phép kiểm tra phải dò qua nhiều bảng nghiệp vụ lớn nên không được gộp vào lượt tải danh sách.',
    'Kết quả kiểm tra được nạp sau khi bảng đã hiển thị, chỉ cho các dòng đang xem.',
    'Trong lúc chờ kết quả, thao tác xoá vẫn an toàn vì máy chủ kiểm tra lại trước khi xoá.',
])

d.p('BR-07 — Tiến trình cập nhật tỷ giá tự động')
d.bullets([
    'Chạy 03:00 hằng ngày theo giờ Việt Nam.',
    'Không cập nhật cho đồng tiền gốc VNĐ/VND.',
    'Bỏ qua khi tỷ giá nguồn không hợp lệ hoặc bằng giá trị hiện tại (so tới 2 chữ số thập phân).',
    'Dừng và ghi lỗi khi không lấy được dữ liệu nguồn, không cập nhật một phần.',
    'Tỷ giá do người dùng sửa tay có thể bị ghi đè ở lần chạy kế tiếp.',
])

d.p('BR-08 — Dữ liệu dùng chung với hệ thống ERP')
d.bullets([
    'Danh mục tiền tệ dùng chung một nguồn dữ liệu với hệ thống ERP đang chạy song song.',
    'Màn hình HRM không thêm cột nào vào dữ liệu gốc, nên không có lịch sử chỉnh sửa.',
    'Hành vi chặn xoá của HRM chặt hơn ERP — đây là khác biệt có chủ đích nhằm bảo vệ dữ liệu cũ.',
])

d.p('Chức năng liên quan: FR-01 … FR-10.')

d.save()
