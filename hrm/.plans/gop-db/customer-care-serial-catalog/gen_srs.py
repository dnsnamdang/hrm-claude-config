# -*- coding: utf-8 -*-
"""Sinh SRS theo FORM CHUAN cho man 'Danh muc serial thiet bi lam dich vu' (phan he CSKH).

Man CHI DOC: chi co xem danh sach + loc + xuat Excel. Moi thao tac ghi serial nam o man
Quan ly khach hang -> tab Trang thiet bi.

Nguon doi chieu (doc truc tiep tu code):
  BE  Modules/CustomerCare/Routes/api.php (prefix /serials)
      Modules/CustomerCare/Http/Controllers/V1/SerialController.php
      app/Models/TpSerial.php
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (1129 — design.md ghi 1126 la da drift)
  FE  hrm-client/pages/customer-care/serials/index.vue
      hrm-client/components/subsystem-menu/customer-care.js
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
from srs_docx_lib import SrsDoc, ACTOR_BOTH  # noqa: E402

OUT = (r"d:\CompanyProject\hrm\hrm-claude-config\hrm\.plans\gop-db"
       r"\customer-care-serial-catalog\SRS - Danh mục serial thiết bị làm dịch vụ.docx")

ACTOR = 'Người xem danh mục serial (P1)'

d = SrsDoc(
    out=OUT,
    menu='Phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Danh mục serial thiết bị làm dịch vụ',
    route='/customer-care/serials',
    full_url='https://<host-hrm>/customer-care/serials',
    img_prefix='sr_')

# ================================================================ TRANG BIA
d.h1('SOFTWARE REQUIREMENTS SPECIFICATION (SRS)')
d.h2('Màn hình: Danh mục serial thiết bị làm dịch vụ')
d.h2('Phân hệ: Chăm sóc khách hàng (CSKH) – nhóm Danh mục - Dịch vụ')

d.info_table([
    ('Mã màn hình', 'CSKH-DM-SERIAL'),
    ('Đường dẫn', '/customer-care/serials'),
    ('Phiên bản', '1.0'),
    ('Ngày lập', '12/08/2026'),
    ('Người lập', '@junfoke'),
    ('Trạng thái tài liệu', 'Draft'),
    ('Nguồn đối chiếu', 'Màn ERP danh mục serial thiết bị làm dịch vụ (bảng serials trên DB gộp)'),
])

# ================================================================ 1. GIOI THIEU
d.h1('1. Giới thiệu')

d.h2('1.1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm (SRS) cho màn hình tra cứu danh mục serial thiết bị '
    'làm dịch vụ, nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa BA/PO/Dev/Test',
    'Là căn cứ nghiệm thu chức năng và phân quyền',
    'Làm rõ đây là màn hình CHỈ ĐỌC: mọi thao tác ghi serial được thực hiện ở màn Quản lý '
    'khách hàng – tab Trang thiết bị, không nằm ở màn này',
    'Làm rõ cách xuất Excel cho khối dữ liệu lớn (hơn 20.000 dòng)',
])

d.h2('1.2 Phạm vi')
d.p('Màn hình Danh mục serial thiết bị làm dịch vụ cung cấp chức năng:')
d.bullets([
    'Xem danh sách serial thiết bị đang được quản lý, hiển thị 7 cột',
    'Tìm kiếm nhanh và lọc nâng cao theo 6 tiêu chí: Số serial, Khách hàng, Tên hàng, Trạng thái, '
    'Người tạo, Người cập nhật',
    'Sắp xếp phía máy chủ trên toàn bộ 7 cột dữ liệu và phân trang',
    'Xuất toàn bộ danh sách theo bộ lọc ra file Excel',
])
d.p('Ngoài phạm vi:')
d.bullets([
    'Thêm / sửa / đổi / xoá serial — các thao tác này thuộc màn Quản lý khách hàng – tab '
    'Trang thiết bị',
    'Xem chi tiết serial, lịch sử chỉnh sửa, nhập từ Excel, In danh sách',
    'Thay đổi cấu trúc bảng dữ liệu: giữ nguyên dữ liệu dùng chung với hệ thống ERP',
])

d.h2('1.3 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Serial thiết bị làm dịch vụ', 'Số serial của một thiết bị cụ thể mà đơn vị đang làm dịch vụ '
                                    'bảo dưỡng, sửa chữa'),
    ('Tên hàng', 'Tên hàng hoá / thiết bị tương ứng với serial'),
    ('Khách hàng', 'Khách hàng đang sở hữu hoặc quản lý thiết bị mang serial đó'),
    ('Trạng thái', 'Tình trạng sử dụng của serial: Đang sử dụng hoặc Ngưng sử dụng'),
    ('Xuất theo lô', 'Cách lấy dữ liệu xuất Excel theo từng khối để không làm quá tải máy chủ'),
    ('P1', 'Quyền “Xem danh mục serial thiết bị làm dịch vụ”'),
    ('Quick Search', 'Tìm kiếm nhanh'),
    ('Advanced Filter', 'Bộ lọc nâng cao'),
    ('SRS', 'Software Requirements Specification'),
], widths=[1.8, 4.2])

# ================================================================ 2. TONG QUAN
d.h1('2. Tổng quan')

d.h2('2.1 Bối cảnh nghiệp vụ')
d.p('Danh mục serial thiết bị làm dịch vụ là nơi tra cứu tập trung toàn bộ serial thiết bị, dùng để:')
d.bullets([
    'Tra cứu nhanh một serial thuộc khách hàng nào, thiết bị gì',
    'Đối chiếu tình trạng sử dụng của thiết bị khi tiếp nhận yêu cầu dịch vụ',
    'Kết xuất dữ liệu phục vụ đối chiếu và báo cáo',
])
d.p('Do đó cần:')
d.bullets([
    'Tách bạch quyền tra cứu với quyền chỉnh sửa dữ liệu: màn hình này chỉ để đọc, '
    'nguồn ghi dữ liệu duy nhất là màn Quản lý khách hàng – tab Trang thiết bị',
    'Bộ lọc đủ rộng để tìm được serial trong khối dữ liệu lớn',
    'Xuất Excel được toàn bộ danh sách mà không bị quá thời gian chờ',
])

d.h2('2.2 Nhóm người dùng')
d.bullets([
    'Người dùng có quyền P1: được tra cứu danh sách và xuất Excel',
    'Người dùng không có P1: bị chặn truy cập',
    'Việc thêm/sửa/xoá serial do người dùng có quyền quản lý khách hàng thực hiện ở màn khác',
])

# ================================================================ 3. PHAN QUYEN
d.h1('3. Phân quyền và kiểm soát truy cập')

d.h2('3.1 Danh sách quyền')
d.table(['Ký hiệu', 'Tên quyền', 'Mã quyền', 'Nhóm quyền'], [
    ('P1', 'Xem danh mục serial thiết bị làm dịch vụ', '1129', 'Danh mục dịch vụ bảo dưỡng'),
], widths=[0.8, 2.8, 0.9, 1.5])
d.p('Ghi chú: màn hình chỉ đọc nên chỉ cần một quyền xem. Màn hình tương ứng bên ERP không gate '
    'quyền nào, đây là quyền mới của HRM.')

d.h2('3.2 Quy tắc truy cập bắt buộc')
d.bullets([
    'Chỉ user có P1 mới được truy cập màn hình.',
    'User không có P1: không hiển thị menu điều hướng tới màn hình.',
    'User không có P1: truy cập trực tiếp URL bị chặn, gọi API trả về lỗi 403.',
    'Màn hình không cung cấp bất kỳ đường ghi dữ liệu nào — không có API thêm/sửa/xoá serial '
    'thuộc màn này.',
])

d.h2('3.3 Ma trận phân quyền')
d.table(['Chức năng', 'P1', 'Không có quyền'], [
    ('Truy cập màn', '✅', '❌'),
    ('Xem danh sách', '✅', '❌'),
    ('Tìm kiếm nhanh / Lọc nâng cao / Sắp xếp / Phân trang', '✅', '❌'),
    ('Xuất Excel', '✅', '❌'),
    ('Thêm / Sửa / Xoá serial', 'Không có trên màn hình này', 'Không có trên màn hình này'),
], widths=[3.4, 1.0, 1.6])

# ================================================================ 4. FUNCTION LIST
d.h1('4. Danh mục chức năng (Function list)')
d.table(['ID', 'Chức năng', 'Mô tả đặc tả thu nhỏ (Mini-Spec)', 'Quyền'], [
    ('FR-01', 'Truy cập màn hình',
     'Kiểm tra quyền P1. Không có quyền sẽ bị chặn (ẩn menu, chặn URL, API trả 403).', 'P1'),
    ('FR-02', 'Xem danh sách',
     'Hiển thị bảng dữ liệu 8 cột (kể cả STT), phân trang, sắp xếp phía máy chủ trên 7 cột dữ liệu.',
     'P1'),
    ('FR-03', 'Tìm kiếm & Lọc',
     'Kết hợp Quick Search và Advanced Filter theo 6 tiêu chí. Danh sách chọn của các bộ lọc '
     'được nạp riêng từ dữ liệu thực tế đang có.', 'P1'),
    ('FR-04', 'Xuất Excel',
     'Xuất toàn bộ danh sách theo bộ lọc; dữ liệu được lấy theo từng lô và hiển thị phần trăm '
     'tiến độ trong lúc xuất.', 'P1'),
], widths=[0.7, 1.4, 3.4, 0.8])

# ================================================================ 5. DAC TA
d.h1('5. Đặc tả chi tiết theo từng chức năng (FUNCTIONAL PACKAGING)')

d.h2('5.1 Sơ đồ UML tổng quan')
d.p('Sơ đồ Use Case tổng quan của màn hình, thể hiện quan hệ giữa người dùng và bốn chức năng:')
d.overview_figure(
    'HỆ THỐNG HRM — Danh mục serial thiết bị làm dịch vụ',
    [(ACTOR, [0, 1, 2, 3])],
    [('FR-01', 'Truy cập màn hình', 'view', None),
     ('FR-02', 'Xem danh sách', 'view', None),
     ('FR-03', 'Tìm kiếm & Lọc', 'view', None),
     ('FR-04', 'Xuất Excel', 'io', '«include» Lấy dữ liệu theo lô')],
    'Sơ đồ Use Case tổng quan màn hình Danh mục serial thiết bị làm dịch vụ')

d.h2('5.2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------- 5.2.1
d.h2('5.2.1 Truy cập màn hình danh mục serial thiết bị làm dịch vụ')

d.h3('5.2.1.1 Biểu đồ Usecase')
d.uc_figure('FR-01', 'Truy cập màn hình danh mục serial thiết bị làm dịch vụ', 'view',
            [('include', 'Kiểm tra quyền truy cập')], actor=ACTOR)

d.h3('5.2.1.2 Giới thiệu')
d.intro_table(
    'Truy cập màn hình danh mục serial thiết bị làm dịch vụ',
    'Cho phép người dùng truy cập vào màn hình tra cứu danh mục serial thiết bị làm dịch vụ.',
    'Admin; User được phân quyền P1',
    'Người dùng đã đăng nhập thành công vào hệ thống.',
    '1. Người dùng chọn menu Chăm sóc khách hàng → Danh mục - Dịch vụ → Danh mục serial thiết bị '
    'làm dịch vụ.\n'
    '2. Hệ thống xác thực quyền truy cập (P1).\n'
    '3. Hệ thống điều hướng tới màn hình danh sách và tải dữ liệu trang đầu tiên.\n'
    '4. Hệ thống nạp danh sách chọn cho các bộ lọc và khôi phục bộ lọc đã lưu của lần truy cập '
    'trước (nếu còn hiệu lực).',
    '• Người dùng không có quyền → Hệ thống ẩn menu; truy cập trực tiếp URL bị chặn.\n'
    '• Gọi trực tiếp API khi không có quyền → Hệ thống trả về lỗi 403.',
    'Màn hình không có nút thao tác ghi dữ liệu nào.')

d.h3('5.2.1.3 Layout màn hình')
d.layout('Ghi chú: tài liệu này không đính kèm ảnh chụp màn hình, người đọc truy cập trực tiếp '
         'đường dẫn trên để đối chiếu giao diện.')

d.h3('5.2.1.4 Tiêu chí nghiệm thu')
d.p('Người dùng có quyền truy cập:')
d.bullets([
    'Nhìn thấy menu Danh mục serial thiết bị làm dịch vụ.',
    'Truy cập được màn hình danh sách.',
    'Hiển thị mặc định: danh sách phải hiển thị đúng cấu trúc bảng gồm STT, Serial thiết bị làm '
    'dịch vụ, Tên hàng, Khách hàng, Trạng thái, Người tạo, Người cập nhật, Ngày cập nhật.',
    'Không có cột Hành động và không có nút thêm/sửa/xoá trên màn hình.',
])
d.p('Người dùng không có quyền:')
d.bullets([
    'Không nhìn thấy menu.',
    'Truy cập trực tiếp URL bị chặn, gọi API trả về 403.',
])

d.h3('5.2.1.5 Danh sách event và xử lý event')
d.event_table([
    ('Click menu Danh mục serial thiết bị làm dịch vụ', 'Click',
     'Kiểm tra quyền P1 và điều hướng tới màn hình danh sách.'),
    ('Truy cập URL trực tiếp', 'System',
     'Kiểm tra quyền; nếu không hợp lệ → chặn truy cập (giao diện) và trả về lỗi 403 (API).'),
    ('Load màn hình', 'System',
     'Nạp danh sách chọn cho các bộ lọc, khôi phục bộ lọc đã lưu và tải danh sách trang 1.'),
])

# ---------------------------------------------------------- 5.2.2
d.h2('5.2.2 Xem danh sách serial thiết bị làm dịch vụ')

d.h3('5.2.2.1 Giới thiệu')
d.intro_table(
    'Xem danh sách serial thiết bị làm dịch vụ',
    'Hiển thị danh sách serial thiết bị kèm tên hàng, khách hàng, trạng thái sử dụng và thông tin '
    'người tạo / người cập nhật.',
    'Admin; User được phân quyền P1',
    'Người dùng truy cập thành công màn hình danh mục serial thiết bị làm dịch vụ.',
    '1. Hệ thống lấy danh sách serial theo bộ lọc hiện tại.\n'
    '2. Hệ thống hiển thị danh sách theo phân trang.\n'
    '3. Người dùng bấm tiêu đề cột để đổi thứ tự sắp xếp nếu cần.',
    '• Không có dữ liệu → Hiển thị danh sách trống kèm thông báo không có dữ liệu.\n'
    '• Serial chưa gắn khách hàng hoặc tên hàng → Ô tương ứng để trống.\n'
    '• Không xác định được người tạo / người cập nhật → Ô tương ứng để trống, danh sách vẫn '
    'hiển thị bình thường.',
    '• Màn hình chỉ đọc: bảng không có cột Hành động.\n'
    '• Dữ liệu của màn hình được ghi từ màn Quản lý khách hàng – tab Trang thiết bị.')

d.h3('5.2.2.2 Layout màn hình')
d.layout()

d.h3('5.2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Bảng danh sách serial', 'Table/Grid', 'Read-only', '–', '–', '–',
     'Hiển thị danh sách serial theo phân trang, không có cột Hành động'),
    ('STT', 'Label', 'Enable', '–', '–', '–', 'Số thứ tự bản ghi, tính theo trang hiện tại'),
    ('Serial thiết bị làm dịch vụ', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Số serial của thiết bị. Cho phép sắp xếp'),
    ('Tên hàng', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Tên hàng hoá / thiết bị, tự xuống dòng khi dài. Cho phép sắp xếp'),
    ('Khách hàng', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Khách hàng gắn với serial, tự xuống dòng khi dài. Cho phép sắp xếp'),
    ('Trạng thái', 'Badge', 'Read-only', 'Đang sử dụng / Ngưng sử dụng', '–', 'Lấy từ hệ thống',
     'Tình trạng sử dụng của serial. Cho phép sắp xếp'),
    ('Người tạo', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Người đã tạo bản ghi serial. Cho phép sắp xếp'),
    ('Người cập nhật', 'Text', 'Read-only', '–', '–', 'Lấy từ hệ thống',
     'Người cập nhật gần nhất. Cho phép sắp xếp'),
    ('Ngày cập nhật', 'Text', 'Read-only', 'dd/mm/yyyy', '–', 'Lấy từ hệ thống',
     'Ngày cập nhật gần nhất. Cho phép sắp xếp'),
    ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1', 'Điều hướng giữa các trang danh sách'),
    ('Chọn số dòng/trang', 'Dropdown', 'Enable', 'Danh sách', 'Không', '10',
     'Thay đổi số bản ghi hiển thị mỗi trang'),
    ('Trạng thái rỗng', 'Label', 'Enable', '–', '–', 'Ẩn', 'Hiển thị khi danh sách trống'),
    ('Loading', 'Loading', 'Hiển thị', '–', '–', 'Ẩn', 'Hiển thị trong lúc chờ tải danh sách'),
])

d.h3('5.2.2.4 Tiêu chí nghiệm thu')
d.bullets([
    'Danh sách hiển thị đủ 7 cột dữ liệu và không có cột Hành động.',
    'Trạng thái hiển thị bằng nhãn tiếng Việt, không hiển thị giá trị số.',
    'Serial chưa gắn khách hàng vẫn hiển thị trong danh sách, ô Khách hàng để trống thay vì '
    'gây lỗi màn hình.',
    'Sắp xếp trên cả 7 cột đều đổi đúng thứ tự dữ liệu, không chỉ đổi mũi tên trên tiêu đề.',
    'Vào màn hình chỉ phát sinh đúng một yêu cầu tải danh sách, không tải lặp.',
    'Phân trang hoạt động đúng với khối dữ liệu lớn, không trùng hoặc thiếu dữ liệu giữa các trang.',
])

d.h3('5.2.2.5 Danh sách event và xử lý event')
d.event_table([
    ('Load danh sách', 'System',
     'Tải danh sách theo bộ lọc và phân trang hiện tại; hiển thị hiệu ứng chờ trong lúc tải.'),
    ('Đổi trang', 'Click', 'Tải lại danh sách theo trang mới, giữ nguyên bộ lọc.'),
    ('Đổi số dòng/trang', 'Change', 'Tải lại danh sách với số dòng mới, quay về trang 1.'),
    ('Bấm tiêu đề cột', 'Click',
     'Đổi cột và chiều sắp xếp, tải lại danh sách. Cột không nằm trong danh sách được phép '
     'sắp xếp thì bỏ qua điều kiện sắp xếp.'),
])

# ---------------------------------------------------------- 5.2.3
d.h2('5.2.3 Tìm kiếm và lọc danh sách serial')

d.h3('5.2.3.1 Giới thiệu')
d.intro_table(
    'Tìm kiếm và lọc danh sách serial',
    'Cho phép người dùng thu hẹp danh sách serial theo từ khoá hoặc theo nhiều tiêu chí kết hợp.',
    'Admin; User được phân quyền P1',
    'Người dùng đang ở màn hình danh sách serial.',
    '1. Người dùng nhập từ khoá vào ô tìm kiếm nhanh hoặc mở bộ lọc nâng cao.\n'
    '2. Người dùng nhập/chọn các tiêu chí: Số serial, Khách hàng, Tên hàng, Trạng thái, '
    'Người tạo, Người cập nhật.\n'
    '3. Người dùng bấm Tìm kiếm.\n'
    '4. Hệ thống lấy danh sách khớp điều kiện, quay về trang 1 và hiển thị kết quả.',
    '• Bấm Làm mới → Hệ thống xoá toàn bộ điều kiện lọc và tải lại danh sách đầy đủ.\n'
    '• Không có kết quả → Hiển thị danh sách trống kèm thông báo.\n'
    '• Thay đổi tiêu chí ở bộ lọc nâng cao → Hệ thống tự tìm lại ngay, không cần bấm Tìm kiếm.',
    '• Danh sách chọn của bộ lọc Khách hàng, Người tạo và Người cập nhật được lấy từ chính dữ liệu '
    'serial đang có, nên chỉ liệt kê những giá trị thực sự xuất hiện trong danh mục.\n'
    '• Điều kiện lọc được ghi nhớ và dùng lại khi quay về màn hình.')

d.h3('5.2.3.2 Layout màn hình')
d.layout()

d.h3('5.2.3.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Khung bộ lọc', 'Modal', 'Enable', '–', '–', 'Thu gọn',
     'Khung “Bộ lọc serial thiết bị làm dịch vụ”, có thể mở rộng / thu gọn'),
    ('Tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     'Tìm nhanh trong danh mục serial'),
    ('Số serial', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Lọc theo một phần của số serial'),
    ('Khách hàng', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Lọc theo khách hàng gắn với serial'),
    ('Tên hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Lọc theo một phần của tên hàng'),
    ('Trạng thái', 'Dropdown', 'Enable', 'Đang sử dụng / Ngưng sử dụng', 'Không', 'Trống',
     'Lọc theo tình trạng sử dụng; để trống là lấy tất cả'),
    ('Người tạo', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', 'Lọc theo người tạo bản ghi'),
    ('Người cập nhật', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     'Lọc theo người cập nhật gần nhất'),
    ('Tìm kiếm', 'Button', 'Enable', '–', '–', '–', 'Áp dụng bộ lọc và quay về trang 1'),
    ('Làm mới', 'Button', 'Enable', '–', '–', '–', 'Xoá toàn bộ điều kiện lọc và tải lại danh sách'),
])

d.h3('5.2.3.4 Tiêu chí nghiệm thu')
d.bullets([
    'Tìm kiếm nhanh trả về đúng các serial khớp từ khoá.',
    'Từ khoá chứa ký tự đặc biệt của phép tìm gần đúng vẫn được tìm như ký tự thông thường, '
    'không trả về toàn bộ danh sách.',
    'Kết hợp nhiều tiêu chí cho ra kết quả thoả mãn đồng thời tất cả tiêu chí.',
    'Danh sách chọn của bộ lọc Người tạo và Người cập nhật chỉ liệt kê những người thực sự có '
    'bản ghi trong danh mục.',
    'Bấm Tìm kiếm luôn quay về trang 1.',
    'Bấm Làm mới thì danh sách được tải lại đầy đủ, không giữ điều kiện cũ.',
])

d.h3('5.2.3.5 Danh sách event và xử lý event')
d.event_table([
    ('Nhập ô tìm kiếm nhanh', 'Keypress', 'Ghi nhận từ khoá, chưa gọi tìm kiếm.'),
    ('Bấm Tìm kiếm', 'Click', 'Quay về trang 1 và tải lại danh sách theo toàn bộ điều kiện lọc.'),
    ('Đổi tiêu chí lọc nâng cao', 'Change',
     'Quay về trang 1 và tải lại danh sách ngay theo điều kiện mới.'),
    ('Load danh sách chọn của bộ lọc', 'System',
     'Lấy danh sách khách hàng, người tạo và người cập nhật thực tế đang có trong danh mục serial.'),
    ('Bấm Làm mới', 'Click', 'Xoá toàn bộ điều kiện lọc, quay về trang 1 và tải lại danh sách.'),
])

# ---------------------------------------------------------- 5.2.4
d.h2('5.2.4 Xuất Excel danh mục serial')

d.h3('5.2.4.1 Biểu đồ Usecase')
d.uc_figure('FR-04', 'Xuất Excel danh mục serial', 'io',
            [('include', 'Lấy dữ liệu theo lô'),
             ('include', 'Hiển thị tiến độ xuất')], actor=ACTOR)

d.h3('5.2.4.2 Giới thiệu')
d.intro_table(
    'Xuất Excel danh mục serial',
    'Cho phép người dùng tải toàn bộ danh sách serial theo bộ lọc ra file Excel để đối chiếu '
    'hoặc gửi ra ngoài.',
    'Admin; User được phân quyền P1',
    'Người dùng đang ở màn hình danh sách serial.',
    '1. Người dùng áp dụng bộ lọc mong muốn (không bắt buộc).\n'
    '2. Người dùng bấm nút Xuất Excel.\n'
    '3. Hệ thống vô hiệu hoá nút Xuất Excel và hiển thị phần trăm tiến độ.\n'
    '4. Hệ thống lấy dữ liệu theo từng lô cho tới khi đủ toàn bộ bản ghi khớp bộ lọc.\n'
    '5. Hệ thống dựng file Excel và trả về cho trình duyệt tải xuống.\n'
    '6. Hệ thống hiển thị thông báo xuất thành công kèm số dòng đã xuất.',
    '• Không có dữ liệu khớp bộ lọc → Hệ thống vẫn trả file chỉ gồm dòng tiêu đề.\n'
    '• Xảy ra lỗi trong lúc lấy dữ liệu hoặc dựng file → Hệ thống hiển thị thông báo lỗi, '
    'không tải file và mở lại nút Xuất Excel.\n'
    '• Người dùng bấm lại nút trong lúc đang xuất → Nút đang bị vô hiệu hoá nên không phát sinh '
    'lượt xuất thứ hai.',
    '• File Excel được dựng ngay trên trình duyệt từ dữ liệu lấy theo lô, thay vì để máy chủ dựng '
    'sẵn cả file: danh mục có hơn 20.000 dòng, để máy chủ dựng sẽ vượt thời gian chờ cho phép.\n'
    '• File xuất ra lấy toàn bộ dữ liệu khớp bộ lọc, không giới hạn theo trang đang xem.')

d.h3('5.2.4.3 Layout màn hình')
d.layout()

d.h3('5.2.4.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Xuất Excel', 'Button', 'Enable / Disable', '–', '–', 'Enable',
     'Nằm ở thanh thao tác dưới bảng danh sách; bị vô hiệu hoá trong lúc đang xuất'),
    ('Nhãn tiến độ', 'Label', 'Hiển thị', '0 – 100', '–', 'Ẩn',
     'Trong lúc xuất, nhãn nút đổi thành “Đang xuất... N%”'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị “Xuất Excel thành công (N dòng)” khi xong'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị khi không lấy được dữ liệu hoặc không dựng được file'),
])

d.h3('5.2.4.5 Tiêu chí nghiệm thu')
d.bullets([
    'Dữ liệu trong file khớp đúng bộ lọc đang áp dụng trên màn hình.',
    'File chứa toàn bộ bản ghi khớp bộ lọc, không chỉ các dòng của trang đang xem.',
    'Xuất toàn bộ danh mục (hơn 20.000 dòng) hoàn tất được, không bị lỗi quá thời gian chờ.',
    'Trong lúc xuất, nút Xuất Excel bị vô hiệu hoá và hiển thị phần trăm tiến độ tăng dần.',
    'Xuất xong hiển thị thông báo nêu đúng số dòng đã xuất.',
    'Người dùng không có quyền gọi trực tiếp API lấy dữ liệu thì bị từ chối với lỗi 403.',
])

d.h3('5.2.4.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền → trả về lỗi 403.\n'
     '– Nếu đang có lượt xuất chạy dở → nút bị vô hiệu hoá, không phát sinh lượt xuất mới.\n'
     'During:\n– Lấy dữ liệu theo từng lô theo đúng bộ lọc hiện tại, cập nhật phần trăm tiến độ '
     'sau mỗi lô.\n'
     '– Lỗi khi lấy dữ liệu → hiển thị thông báo lỗi, mở lại nút và dừng xử lý.\n'
     'After:\n– Dựng file Excel và tải xuống.\n'
     '– Hiển thị thông báo “Xuất Excel thành công (N dòng)” và mở lại nút Xuất Excel.'),
])

# ================================================================ 6. BR
d.h1('6. Quy tắc nghiệp vụ (Business Rules)')

d.p('BR-01 — Màn hình chỉ đọc')
d.bullets([
    'Màn hình không cung cấp chức năng thêm, sửa, đổi hay xoá serial.',
    'Mọi thao tác ghi serial được thực hiện ở màn Quản lý khách hàng – tab Trang thiết bị.',
    'Bảng danh sách không có cột Hành động.',
])

d.p('BR-02 — Trạng thái serial')
d.bullets([
    'Serial có 2 trạng thái nghiệp vụ: Đang sử dụng và Ngưng sử dụng.',
    'Trạng thái luôn hiển thị bằng nhãn tiếng Việt, không hiển thị giá trị số.',
    'Bộ lọc Trạng thái để trống thì lấy toàn bộ, không phân biệt trạng thái.',
])

d.p('BR-03 — Nguồn dữ liệu của các danh sách chọn')
d.bullets([
    'Danh sách chọn Khách hàng, Người tạo, Người cập nhật được lấy từ chính dữ liệu serial đang có.',
    'Không lấy từ danh sách nhân sự chung, để tránh lệch giữa hai hệ định danh khác nhau và tránh '
    'liệt kê những người không có bản ghi nào trong danh mục.',
])

d.p('BR-04 — Hiển thị an toàn khi dữ liệu thiếu')
d.bullets([
    'Serial thiếu thông tin khách hàng, tên hàng, người tạo hoặc người cập nhật vẫn phải hiển thị '
    'trong danh sách, ô tương ứng để trống.',
    'Không được để dữ liệu thiếu làm hỏng màn hình danh sách.',
])

d.p('BR-05 — Xuất Excel cho khối dữ liệu lớn')
d.bullets([
    'File Excel được dựng trên trình duyệt từ dữ liệu lấy theo từng lô.',
    'Cách này được chọn vì danh mục có hơn 20.000 dòng: để máy chủ dựng cả file sẽ vượt thời gian '
    'chờ cho phép khi triển khai thật.',
    'Trong lúc xuất phải hiển thị tiến độ và khoá nút để không phát sinh nhiều lượt xuất cùng lúc.',
])

d.p('BR-06 — Dữ liệu dùng chung với hệ thống ERP')
d.bullets([
    'Danh mục serial dùng chung một nguồn dữ liệu với hệ thống ERP đang chạy song song.',
    'Màn hình HRM hiển thị nhiều hơn màn ERP 3 cột (Người tạo, Người cập nhật, Ngày cập nhật) '
    'và nhiều hơn 2 bộ lọc, nhưng không đổi cấu trúc dữ liệu gốc.',
    'Màn hình HRM bổ sung chức năng Xuất Excel mà màn ERP không có.',
])

d.p('Chức năng liên quan: FR-01 … FR-04.')

d.save()
