# -*- coding: utf-8 -*-
"""Sinh SRS man 'Danh muc khach hang' (/assign/customers) theo FORM CHUAN cua team.

Nguon doi chieu (doc truc tiep tu code 15/08/2026):
  BE  Modules/Assign/{Routes/api.php, Http/Controllers/Api/V1/CustomerController.php,
        Services/{CustomerService,CustomerImportService,CustomerManagerService}.php,
        Http/Requests/Customer/{SaveCustomerRequest,UpdateCustomerRequest}.php}
  FE  hrm-client/pages/assign/customers/{index.vue, add.vue, _id/index.vue, _id/edit.vue,
        _id/manager/index.vue}
      hrm-client/components/assign-components/customer/CustomerForm.vue
  Anh chup that: .plans/gop-db/customer-docs/kh_shots/  (Playwright, 1440x900, 15/08/2026)

Chay:  python .plans/gop-db/customer-docs/gen_srs.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "srs-documenter", "assets"))
from srs_docx_lib import SrsDoc  # noqa: E402

SHOTS = os.path.join(HERE, "kh_shots")


def shot(name):
    return os.path.join(SHOTS, name)


OUT = os.path.join(HERE, "SRS - Danh mục khách hàng.docx")

d = SrsDoc(
    out=OUT,
    menu='Phân hệ Giao việc → Danh mục chung → Danh mục khách hàng',
    route='/assign/customers',
    full_url='https://<host-hrm>/assign/customers',
    img_prefix='kh_')

ACTOR_QL = 'Nhân viên quản lý khách hàng'
ACTOR_XEM = 'Người dùng chỉ có quyền xem'

# ================================================================ TRANG BÌA
d.h1('SOFTWARE REQUIREMENTS SPECIFICATION (SRS)')
d.h2('Màn hình: Danh mục khách hàng')
d.h2('Phân hệ: Giao việc – nhóm Danh mục chung')

d.info_table([
    ('Mã màn hình', 'GV-DM-CUSTOMER'),
    ('Đường dẫn', '/assign/customers'),
    ('Phiên bản', '1.0'),
    ('Ngày lập', '15/08/2026'),
    ('Người lập', '@junfoke'),
    ('Trạng thái tài liệu', 'Draft'),
    ('Nguồn đối chiếu', 'Màn danh mục khách hàng của phần mềm ERP cũ, đã gộp về CSDL chung '
                        '(nhánh gop_db). Tài liệu bám CODE HIỆN TẠI, không bám bản thiết kế cũ.'),
])

d.h2('Mục lục')
d.toc()

# ================================================================ 1. GIỚI THIỆU
d.h1('1. Giới thiệu')

d.h2('1.1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình Danh mục khách hàng, nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa BA / PO / Dev / Test về một màn hình dùng chung cho toàn hệ thống '
    'sau khi gộp dữ liệu khách hàng của hai phần mềm cũ.',
    'Là căn cứ nghiệm thu chức năng và phân quyền.',
    'Làm rõ cơ chế phạm vi dữ liệu bốn cấp và lớp bảo vệ riêng cho khách hàng cá nhân — đây là '
    'điểm phức tạp nhất của màn hình và cũng là nơi dễ hiểu sai nhất.',
    'Làm rõ các trường bắt buộc rẽ nhánh theo loại hình tổ chức, đặc biệt quy tắc Mã số thuế '
    'chỉ bắt buộc khi khách hàng không trực thuộc công ty mẹ.',
])

d.h2('1.2 Phạm vi')
d.p('Màn hình Danh mục khách hàng cung cấp các chức năng:')
d.bullets([
    'Truy cập và xem danh sách khách hàng theo phạm vi quyền.',
    'Tìm kiếm nhanh và lọc nâng cao theo 19 tiêu chí.',
    'Cài đặt bộ lọc: chọn và sắp xếp các ô lọc hiển thị trên giao diện.',
    'Tuỳ chỉnh cột: bật / tắt và sắp xếp các cột của bảng danh sách.',
    'Tạo mới, chỉnh sửa, xem chi tiết khách hàng.',
    'Khóa / Mở khóa khách hàng.',
    'Xem lịch sử thay đổi của khách hàng.',
    'Nhập khách hàng hàng loạt từ file Excel.',
    'Xuất danh sách ra CSV, Excel, PDF.',
    'Mở màn Quản lý khách hàng gồm 6 thẻ nghiệp vụ.',
])
d.p('Ngoài phạm vi:')
d.bullets([
    'Nghiệp vụ báo giá, hợp đồng, trang thiết bị — màn hình chỉ hiển thị lại, không tạo/sửa các '
    'chứng từ đó (trừ phần trang thiết bị khai thêm ngoài hệ thống).',
    'Quản lý danh mục Nhóm khách hàng, Lĩnh vực kinh doanh, Hãng xe, danh mục địa chỉ — có màn '
    'riêng, màn này chỉ tham chiếu.',
    'Cơ chế đăng ký / giữ khách hàng cá nhân — màn này chỉ sử dụng kết quả để quyết định hiển thị.',
    'Xóa vĩnh viễn khách hàng — hệ thống KHÔNG cung cấp, chỉ có Khóa.',
])

d.h2('1.3 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Khách hàng cá nhân', 'Khách hàng có Loại hình tổ chức là “Cá nhân”. Chịu thêm lớp bảo vệ '
                           'hiển thị riêng, xem BR-02.'),
    ('Khách hàng tổ chức', 'Khách hàng thuộc một trong bốn loại: Doanh nghiệp tư nhân, Doanh '
                           'nghiệp nước ngoài, Tổ chức phi chính phủ, Cơ quan nhà nước.'),
    ('Khách hàng tự do', 'Khách hàng cá nhân chưa ai đăng ký, chưa phát sinh báo giá / cuộc họp / '
                         'dự án tiềm năng và không do người đang đăng nhập tạo ra.'),
    ('Công ty mẹ', 'Khách hàng khác được chọn làm đơn vị chủ quản. Quan hệ một cấp.'),
    ('Loại hình hoạt động', 'Vế trái của cặp phân loại ngành nghề khách hàng.'),
    ('Lĩnh vực kinh doanh', 'Vế phải của cặp phân loại, phải thuộc đúng Loại hình hoạt động đã chọn.'),
    ('Người đại diện', 'Người đại diện pháp luật của khách hàng tổ chức.'),
    ('Người liên hệ', 'Đầu mối làm việc thực tế của khách hàng tổ chức; một khách hàng có nhiều '
                      'người liên hệ.'),
    ('Khóa khách hàng', 'Đổi trạng thái sang “Khóa”. KHÔNG xóa dữ liệu; khách hàng vẫn nằm trong '
                        'danh sách nhưng không chọn được ở các màn nghiệp vụ khác.'),
    ('Phạm vi dữ liệu', 'Tập khách hàng mà người đăng nhập được nhìn thấy, quyết định bởi bốn cấp '
                        'quyền xem, xem BR-01.'),
    ('SRS', 'Software Requirements Specification'),
], widths=[1.8, 4.2])

# ================================================================ 2. TỔNG QUAN
d.h1('2. Tổng quan')

d.h2('2.1 Bối cảnh nghiệp vụ')
d.p('Danh mục khách hàng là danh mục gốc của toàn hệ thống, dùng để:')
d.bullets([
    'Chọn khách hàng khi lập báo giá, hợp đồng, phiếu sửa chữa, dự án tiềm năng, cuộc họp.',
    'Tra cứu thông tin liên hệ, mã số thuế, địa chỉ xuất hoá đơn phục vụ xuất hoá đơn.',
    'Theo dõi lịch sử giao dịch của từng khách hàng qua màn Quản lý khách hàng.',
])
d.p('Do đó cần:')
d.bullets([
    'Một danh mục DUY NHẤT sau khi gộp hai phần mềm cũ — cùng một đối tác chỉ có một bản ghi, kể '
    'cả khi đối tác đó vừa là khách hàng vừa là nhà cung cấp.',
    'Cơ chế phạm vi dữ liệu nhiều cấp để nhân viên kinh doanh không nhìn thấy khách hàng của đơn '
    'vị khác.',
    'Lớp bảo vệ riêng cho khách hàng cá nhân để tránh tình trạng tranh giành khách.',
    'Công cụ nhập hàng loạt từ Excel vì lượng khách hàng chuyển đổi rất lớn.',
])

d.h2('2.2 Nhóm người dùng')
d.bullets([
    'Nhân viên kinh doanh — tạo và chăm sóc khách hàng của mình. Thường có quyền Thêm và Sửa, '
    'phạm vi dữ liệu cấp bộ phận hoặc cấp phòng ban.',
    'Trưởng phòng / Giám đốc kinh doanh — phạm vi dữ liệu cấp phòng ban hoặc cấp công ty, có thêm '
    'quyền Xóa (dùng để khóa) và Xuất dữ liệu.',
    'Quản trị hệ thống — quyền Xem tất cả khách hàng, đầy đủ các quyền thao tác.',
    'Người dùng không được gán quyền khách hàng nào — VẪN mở được màn hình, nhưng chỉ nhìn thấy '
    'khách hàng do chính mình tạo và không thao tác được gì.',
])

# ================================================================ 3. PHÂN QUYỀN
d.h1('3. Phân quyền và kiểm soát truy cập')

d.h2('3.1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Xem khách hàng', 'Mở màn Quản lý khách hàng (thẻ Báo giá, Hợp đồng, Danh sách trang '
                             'thiết bị).'),
    ('Q2', 'Thêm khách hàng', 'Nút Tạo mới và chức năng Import Excel.'),
    ('Q3', 'Sửa khách hàng', 'Nút Sửa; sửa trang thiết bị; tải ảnh / tài liệu ở thẻ Thông tin khác.'),
    ('Q4', 'Xóa khách hàng', 'Thao tác Khóa và Mở khóa.'),
    ('Q5', 'Xuất dữ liệu khách hàng', 'Ba nút Xuất CSV, Xuất Excel, Xuất PDF.'),
], widths=[0.7, 2.0, 3.3])

d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét theo thứ tự ưu tiên từ trên xuống, '
    'cấp nào có trước thì áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem tất cả khách hàng', 'Toàn bộ khách hàng của hệ thống.'),
    ('V2', 'Xem tất cả khách hàng của công ty', 'Khách hàng đã phát sinh báo giá thuộc công ty của '
                                               'người đăng nhập.'),
    ('V3', 'Xem tất cả khách hàng của phòng ban', 'Giới hạn theo phòng ban của người đăng nhập.'),
    ('V4', 'Xem tất cả khách hàng của bộ phận', 'Giới hạn theo bộ phận của người đăng nhập.'),
    ('—', '(không có cấp nào)', 'Chỉ khách hàng do chính mình tạo, cộng khách hàng mình đang đăng '
                               'ký còn hạn hoặc đã từng tương tác.'),
], widths=[0.7, 2.0, 3.3])

d.h2('3.2 Quy tắc truy cập bắt buộc')
d.bullets([
    'Màn hình danh sách KHÔNG gắn quyền xem: mọi người dùng đã đăng nhập đều mở được. Khác biệt '
    'nằm ở LƯỢNG DỮ LIỆU nhìn thấy, không phải ở việc vào được hay không.',
    'Phạm vi dữ liệu được áp ở tầng máy chủ. Người dùng luôn nhìn thấy tối thiểu khách hàng do '
    'chính mình tạo, kể cả khi không có cấp quyền xem nào — đây là phần bổ sung có chủ đích so '
    'với phần mềm cũ, chỉ thêm chứ không bớt.',
    'Mọi thao tác ghi (thêm, sửa, khóa, mở khóa, nhập từ Excel) đều kiểm quyền ở tầng máy chủ. '
    'Gọi thẳng chức năng mà bỏ qua giao diện vẫn bị từ chối.',
    'Chức năng xuất file dùng ĐÚNG bộ lọc và ĐÚNG phạm vi dữ liệu của màn danh sách — không được '
    'phép xuất ra khách hàng mà người dùng không nhìn thấy trên lưới.',
    'Nút thao tác khi thiếu quyền được VÔ HIỆU HÓA (làm mờ) chứ không ẩn đi, để người dùng biết '
    'chức năng tồn tại và cần xin quyền.',
])

d.h2('3.3 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Không có quyền nào'], [
    ('FR-01 Truy cập & xem danh sách', '✅', '✅', '✅', '✅', '✅', '✅ (chỉ khách hàng của mình)'),
    ('FR-02 Tìm kiếm & lọc nâng cao', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tuỳ chỉnh cột', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo mới khách hàng', '❌', '✅', '❌', '❌', '❌', '❌'),
    ('FR-06 Chỉnh sửa khách hàng', '❌', '❌', '✅', '❌', '❌', '❌'),
    ('FR-07 Xem chi tiết khách hàng', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-08 Khóa / Mở khóa', '❌', '❌', '❌', '✅', '❌', '❌'),
    ('FR-09 Lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-10 Nhập từ file Excel', '❌', '✅', '❌', '❌', '❌', '❌'),
    ('FR-11 Xuất CSV / Excel / PDF', '❌', '❌', '❌', '❌', '✅', '❌'),
    ('FR-12 Màn Quản lý khách hàng', '✅', '❌', '✅ (sửa thiết bị)', '❌', '❌', '❌'),
], widths=[2.0, 0.4, 0.4, 0.75, 0.4, 0.4, 1.65])

# ================================================================ 4. DANH MỤC CHỨC NĂNG
d.h1('4. Danh mục chức năng (Function list)')
d.table(['ID', 'Chức năng', 'Mô tả đặc tả thu nhỏ (Mini-Spec)', 'Quyền'], [
    ('FR-01', 'Truy cập & xem danh sách',
     'Hiển thị bảng khách hàng theo phạm vi dữ liệu của người đăng nhập, có phân trang và ô '
     'thống kê “Hiển thị a–b / N”.', 'Không cần quyền'),
    ('FR-02', 'Tìm kiếm & bộ lọc nâng cao',
     'Ô tìm nhanh theo tên / mã / mã số thuế / số điện thoại, cộng 19 tiêu chí lọc nâng cao kết '
     'hợp theo kiểu “và”.', 'Không cần quyền'),
    ('FR-03', 'Cài đặt bộ lọc',
     'Chọn và kéo sắp xếp 15 ô lọc hiển thị trên panel bộ lọc; ghi nhớ theo từng người dùng.',
     'Không cần quyền'),
    ('FR-04', 'Tuỳ chỉnh cột',
     'Bật / tắt và sắp xếp cột của bảng; cột STT và Mã KH bị khóa luôn hiển thị; ghi nhớ theo '
     'từng người dùng.', 'Không cần quyền'),
    ('FR-05', 'Tạo mới khách hàng',
     'Form nhiều khối, các khối hiện theo Loại hình tổ chức đã chọn. Sinh mã khách hàng tự động.',
     'Q2'),
    ('FR-06', 'Chỉnh sửa khách hàng',
     'Như form tạo mới, có thêm khối Địa chỉ giao hàng; mã khách hàng không đổi.', 'Q3'),
    ('FR-07', 'Xem chi tiết khách hàng',
     'Hiển thị toàn bộ thông tin ở chế độ chỉ đọc.', 'Không cần quyền'),
    ('FR-08', 'Khóa / Mở khóa khách hàng',
     'Đổi trạng thái qua lại giữa Hoạt động và Khóa, có hộp xác nhận nêu rõ mã và tên khách hàng.',
     'Q4'),
    ('FR-09', 'Lịch sử thay đổi',
     'Liệt kê các lần Thêm mới / Sửa / đổi trạng thái, mới nhất ở trên cùng, kèm giá trị cũ và '
     'giá trị mới.', 'Không cần quyền'),
    ('FR-10', 'Nhập khách hàng từ file Excel',
     'Tải file mẫu 3 trang, nạp file lên bảng, kiểm tra dữ liệu rồi mới ghi. Tối đa 1.000 dòng '
     'mỗi lần.', 'Q2'),
    ('FR-11', 'Xuất CSV / Excel / PDF',
     'Xuất theo đúng bộ lọc đang áp dụng, có cửa sổ chọn trường và thứ tự cột.', 'Q5'),
    ('FR-12', 'Màn Quản lý khách hàng',
     'Sáu thẻ: Thông tin chung, Thông tin liên hệ, Báo giá, Hợp đồng, Danh sách trang thiết bị, '
     'Thông tin khác.', 'Q1 (Q3 để sửa thiết bị)'),
], widths=[0.6, 1.5, 3.1, 1.0])

# ================================================================ 5. + 6.
sys.path.insert(0, HERE)
import srs_chuong5  # noqa: E402
import srs_chuong5b  # noqa: E402

srs_chuong5.build(d, shot)
srs_chuong5b.build(d, shot)

d.save()
