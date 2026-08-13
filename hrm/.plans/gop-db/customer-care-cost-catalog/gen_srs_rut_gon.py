# -*- coding: utf-8 -*-
"""Sinh SRS theo FORM RUT GON (user chot 2026-08-12) cho man
'Danh muc dich vu sua chua va chi phi khac' (phan he CSKH).

Khac form chuan cu:
  - Bo muc "Tieu chi nghiem thu"
  - Bo muc "Layout man hinh" rieng -> gop vao "Gioi thieu + Cach truy cap"
  - Bang mo ta chi tiet doi sang 7 cot: Field name | Placeholder | Field type |
    Content | Required | Gioi han ky tu | Ghi chu
  - Them chuong "Khai niem, nguyen tac chung" + "Danh sach usecase"
  - VAN GIU anh Use Case: 1 anh tong quan + 1 anh cho moi chuc nang

Nguon doi chieu (doc truc tiep tu code 2026-08-12):
  BE  Modules/CustomerCare/{Routes/api.php, Entities/Cost/Cost.php,
        Http/Requests/Cost/CostRequest.php, Http/Controllers/V1/CostController.php}
  FE  hrm-client/pages/customer-care/costs/index.vue
      hrm-client/components/modal/customer-care/cost-modal.vue
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
       r"\customer-care-cost-catalog"
       r"\SRS - Danh mục dịch vụ sửa chữa và chi phí khác (form rút gọn).docx")

d = SrsDoc(
    out=OUT,
    menu='Phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Danh mục dịch vụ sửa chữa '
         'và chi phí khác',
    route='/customer-care/costs',
    full_url='https://<host-hrm>/customer-care/costs',
    img_prefix='cost2_')


def access(extra=None):
    """Muc 'Cach truy cap' dung chung cho moi chuc nang."""
    d.p('Cách truy cập:')
    items = [
        'Menu: %s' % d.menu,
        'Route (FE): %s' % d.route,
        'URL đầy đủ: %s' % d.full_url,
    ]
    if extra:
        items += extra
    d.bullets(items)


# ================================================================ TRANG BIA
d.h1('SOFTWARE REQUIREMENTS SPECIFICATION (SRS)')
d.h2('Màn hình: Danh mục dịch vụ sửa chữa và chi phí khác')
d.h2('Phân hệ: Chăm sóc khách hàng (CSKH) – nhóm Danh mục - Dịch vụ')

d.info_table([
    ('Mã màn hình', 'CSKH-DM-COST'),
    ('Đường dẫn', '/customer-care/costs'),
    ('Phiên bản', '2.0'),
    ('Ngày lập', '12/08/2026'),
    ('Người lập', '@junfoke'),
    ('Trạng thái tài liệu', 'Draft'),
    ('Nguồn đối chiếu', 'Màn ERP danh mục chi phí (bảng costs, nhóm dịch vụ, trên DB gộp)'),
])

d.h2('Mục lục')
d.toc()

# ================================================================ 1. TONG QUAN
d.h1('1. Tổng quan')

d.h2('1.1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình quản lý danh mục dịch vụ sửa chữa và '
    'chi phí khác, nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa BA/PO/Dev/Test',
    'Là căn cứ nghiệm thu chức năng và phân quyền',
    'Làm rõ ràng buộc nghiệp vụ: chi phí đã phát sinh chứng từ chỉ được khoá chứ không được xoá; '
    'hai chi phí hệ thống không được sửa, khoá hay xoá',
    'Làm rõ đặc thù chiết khấu tách theo từng công ty — cùng một dịch vụ, mỗi công ty một mức '
    'chiết khấu khác nhau',
])

d.h2('1.2 Thuật ngữ và các từ viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Dịch vụ sửa chữa', 'Hạng mục dịch vụ do đơn vị cung cấp, có tính doanh thu'),
    ('Chi phí khác', 'Hạng mục chi phí phát sinh, không tính doanh thu'),
    ('% Tính giá vốn', 'Tỷ lệ phần trăm dùng để tính giá vốn của dịch vụ'),
    ('% VAT', 'Thuế suất giá trị gia tăng áp cho dịch vụ / chi phí'),
    ('ĐM giảm giá', 'Định mức giảm giá (chiết khấu), khai báo RIÊNG theo từng công ty'),
    ('Phân loại', 'Nhãn phân biệt “Dịch vụ có tính doanh thu” và “Chi phí khác”'),
    ('Công ty hiện tại', 'Công ty người dùng đang chọn khi đăng nhập, quyết định mức ĐM giảm giá '
                        'được hiển thị và ghi'),
    ('Chi phí hệ thống', 'Hai chi phí “Chi phí đi lại” và “Chi phí vận chuyển” — bị chặn cứng theo '
                         'tên, không cho sửa / khoá / mở khoá / xoá'),
    ('Chứng từ phát sinh', 'Báo giá hãng hoặc Hợp đồng hãng có sử dụng dịch vụ / chi phí'),
    ('P1', 'Quyền “Quản lý dịch vụ sửa chữa và chi phí khác”'),
    ('P2', 'Quyền “Xem dịch vụ sửa chữa và chi phí khác”'),
    ('SRS', 'Software Requirements Specification'),
], widths=[1.8, 4.2])

d.h2('1.3 Phân quyền')

d.p('Danh sách quyền:')
d.table(['Ký hiệu', 'Tên quyền', 'Mã quyền', 'Nhóm quyền'], [
    ('P1', 'Quản lý dịch vụ sửa chữa và chi phí khác', '1123', 'Danh mục dịch vụ bảo dưỡng'),
    ('P2', 'Xem dịch vụ sửa chữa và chi phí khác', '1124', 'Danh mục dịch vụ bảo dưỡng'),
], widths=[0.8, 2.8, 0.9, 1.5])

d.p('Quy tắc truy cập bắt buộc:')
d.bullets([
    'Chỉ user có P1 hoặc P2 mới được truy cập màn hình.',
    'User không có P1/P2: không hiển thị menu; truy cập trực tiếp URL bị chặn (điều hướng về '
    'trang 404), gọi API trả về lỗi 403.',
    'User chỉ có P2: mọi thao tác ghi bị chặn ở cả giao diện lẫn API (403), không phụ thuộc vào '
    'việc giao diện có ẩn nút hay không.',
    'ĐM giảm giá hiển thị và ghi nhận theo công ty người dùng đang đăng nhập; không xác định được '
    'công ty thì cột ĐM giảm giá để trống và không ghi được giá trị.',
    'Màn hình chỉ hiển thị dữ liệu thuộc nhóm “Dịch vụ sửa chữa và chi phí khác”. Gọi API với bản '
    'ghi thuộc nhóm chi phí phải trả / chi phí bán hàng đều bị từ chối.',
])

d.p('Ma trận phân quyền:')
d.table(['Chức năng', 'P1', 'P2', 'Không có quyền'], [
    ('Truy cập màn hình', '✅', '✅', '❌'),
    ('Xem danh sách, tìm kiếm, lọc, sắp xếp, phân trang', '✅', '✅', '❌'),
    ('Xem chi tiết', '✅', '✅', '❌'),
    ('Thêm mới', '✅', '❌', '❌'),
    ('Sửa', '✅', '❌', '❌'),
    ('Khoá / Mở khoá', '✅', '❌', '❌'),
    ('Xoá', '✅', '❌', '❌'),
    ('Khai báo ĐM giảm giá theo công ty', '✅', '❌', '❌'),
    ('Xuất Excel', '✅', '✅', '❌'),
], widths=[3.0, 0.8, 0.8, 1.4])

# ================================================================ 2. THIET KE
d.h1('2. Thiết kế các phân hệ chức năng')

d.h2('2.1 Khái niệm, nguyên tắc chung')

d.h3('2.1.1 Dropdown')
d.bullets([
    'Dropdown ở bộ lọc luôn có nút xoá lựa chọn; bỏ trống nghĩa là không lọc theo tiêu chí đó.',
    'Bộ lọc KHÔNG dùng lựa chọn “Tất cả”; trạng thái mặc định là chưa chọn gì, hiển thị dòng gợi ý.',
    'Dropdown đặt trong modal dùng biến thể riêng cho modal để danh sách không bị modal che mất.',
    'Dropdown chỉ liệt kê dữ liệu đang ở trạng thái Hoạt động, trừ khi có ghi chú khác.',
])

d.h3('2.1.2 Thông báo')
d.bullets([
    'Thông báo thành công / thất bại hiển thị dạng toast ở góc màn hình, tự tắt.',
    'Lỗi hợp lệ của từng trường hiển thị ngay dưới ô nhập tương ứng kèm viền đỏ, không dùng toast.',
    'Thao tác xoá, khoá, mở khoá đều phải qua hộp thoại xác nhận nêu rõ tên bản ghi bị tác động.',
    'Thông báo từ chối quyền dùng chung một câu: “Bạn không có quyền thực hiện chức năng này.”',
])

d.h3('2.1.3 Tooltip')
d.bullets([
    'Mọi nút biểu tượng đều có chú giải hiện khi rê chuột.',
    'Nút bị vô hiệu hoá phải có chú giải nêu rõ LÝ DO, không được để chú giải trống.',
    'Nút thao tác bị chặn theo nghiệp vụ thì vô hiệu hoá chứ không ẩn, để người dùng biết chức '
    'năng có tồn tại.',
])

d.h3('2.1.4 Date picker')
d.p('Màn hình này không có trường ngày tháng cho người dùng nhập. Các cột ngày (Cập nhật) chỉ '
    'hiển thị, định dạng dd/mm/yyyy.')

d.h3('2.1.5 Phân trang')
d.bullets([
    'Mặc định 10 bản ghi mỗi trang, cho phép đổi số dòng hiển thị.',
    'Đổi số dòng mỗi trang luôn quay về trang 1.',
    'Bấm Tìm kiếm hoặc đổi tiêu chí lọc luôn quay về trang 1.',
    'Phân trang và sắp xếp thực hiện phía máy chủ, không cắt dữ liệu ở trình duyệt.',
    'Vào màn hình chỉ được phát sinh đúng một lượt tải danh sách.',
])

d.h3('2.1.6 Kịch bản tìm kiếm')
d.bullets([
    'Ô tìm kiếm nhanh chỉ áp dụng khi người dùng bấm nút Tìm kiếm, không tự tìm sau mỗi ký tự.',
    'Thay đổi tiêu chí ở bộ lọc nâng cao thì tự tìm lại ngay, không cần bấm Tìm kiếm.',
    'Tìm theo văn bản là tìm gần đúng ở mọi vị trí trong chuỗi.',
    'Từ khoá chứa ký tự đặc biệt của phép tìm gần đúng phải được xử lý như ký tự thông thường, '
    'không được trả về toàn bộ danh sách.',
    'Kết hợp nhiều tiêu chí cho ra kết quả thoả mãn đồng thời tất cả tiêu chí.',
    'Nút Làm mới xoá toàn bộ điều kiện lọc và tải lại danh sách đầy đủ.',
    'Điều kiện lọc được ghi nhớ và dùng lại khi người dùng quay về màn hình.',
])

d.h3('2.1.7 Quy tắc hiển thị bảng danh sách')
d.bullets([
    'Cột đầu là STT tính theo trang hiện tại, cột cuối là “Hành động”.',
    'Danh sách hiển thị cả bản ghi Hoạt động lẫn bản ghi Khoá.',
    'Giá trị dạng cờ hoặc trạng thái luôn hiển thị bằng nhãn tiếng Việt, không hiển thị giá trị số.',
    'Ô không có dữ liệu để trống, không hiển thị giá trị 0 hay “null”.',
    'Danh sách trống thì hiển thị dòng thông báo không có dữ liệu thay vì bảng rỗng.',
    'Trong lúc chờ tải dữ liệu phải hiển thị trạng thái đang tải.',
])

d.h3('2.1.8 Quy tắc sinh mã')
d.p('Màn hình này không sinh mã tự động. Định danh nghiệp vụ của bản ghi là Tên dịch vụ / chi phí '
    'và tên này phải là duy nhất trong nhóm dữ liệu của màn hình.')

d.h3('2.1.9 File tải lên')
d.p('Màn hình này không có chức năng tải file lên. Chiều ra dữ liệu duy nhất là Xuất Excel '
    '(mục 7).')

d.h2('2.2 Danh sách usecase')
d.table(['ID', 'Usecase', 'Mô tả ngắn', 'Quyền'], [
    ('UC-01', 'Xem danh sách và tìm kiếm',
     'Hiển thị bảng 9 cột, tìm kiếm nhanh, lọc theo 4 tiêu chí, sắp xếp và phân trang.', 'P1, P2'),
    ('UC-02', 'Thêm mới',
     'Mở modal khai báo dịch vụ / chi phí mới. Bản ghi mới luôn ở trạng thái Hoạt động.', 'P1'),
    ('UC-03', 'Sửa',
     'Mở modal nạp sẵn dữ liệu, cho sửa toàn bộ trường và Trạng thái. Chi phí hệ thống và chi phí '
     'đang Khoá bị chặn sửa.', 'P1'),
    ('UC-04', 'Xem chi tiết', 'Mở modal ở chế độ chỉ đọc.', 'P1, P2'),
    ('UC-05', 'Khoá / Mở khoá', 'Đổi trạng thái sử dụng của dịch vụ / chi phí.', 'P1'),
    ('UC-06', 'Xoá',
     'Xoá bản ghi; nếu đã phát sinh chứng từ thì hệ thống tự chuyển sang trạng thái Khoá.', 'P1'),
    ('UC-07', 'Xuất Excel', 'Xuất danh sách theo đúng bộ lọc đang áp dụng.', 'P1, P2'),
], widths=[0.7, 1.4, 3.4, 0.8])

d.overview_figure(
    'HỆ THỐNG HRM — Danh mục dịch vụ sửa chữa và chi phí khác',
    [(ACTOR_P1, [0, 1, 2, 3, 4, 5, 6]),
     ('Người xem danh mục (P2)', [0, 3, 6])],
    [('UC-01', 'Xem danh sách và tìm kiếm', 'view', None),
     ('UC-02', 'Thêm mới', 'crud', None),
     ('UC-03', 'Sửa', 'crud', None),
     ('UC-04', 'Xem chi tiết', 'view', None),
     ('UC-05', 'Khoá / Mở khoá', 'action', None),
     ('UC-06', 'Xoá', 'action', '«extend» Khoá khi đã phát sinh chứng từ'),
     ('UC-07', 'Xuất Excel', 'io', None)],
    'Sơ đồ Use Case tổng quan màn hình Danh mục dịch vụ sửa chữa và chi phí khác')

# ================================================================ 3. UC-01
d.h1('3. Chức năng Xem danh sách và tìm kiếm')

d.h2('3.1 Giới thiệu và cách truy cập')
d.p('Hiển thị danh sách các dịch vụ sửa chữa và chi phí khác đã khai báo, kèm % tính giá vốn, '
    '% VAT và mức ĐM giảm giá áp dụng cho công ty người dùng đang đăng nhập. Người dùng có thể '
    'thu hẹp danh sách bằng ô tìm kiếm nhanh hoặc bộ lọc nâng cao, sắp xếp theo 5 cột và chuyển trang.')
d.p('Danh sách chỉ hiển thị bản ghi thuộc nhóm “Dịch vụ sửa chữa và chi phí khác”; bản ghi thuộc '
    'nhóm chi phí phải trả / chi phí bán hàng không xuất hiện ở màn này.')
access()
d.uc_figure('UC-01', 'Xem danh sách và tìm kiếm', 'view',
            [('include', 'Kiểm tra quyền truy cập'),
             ('include', 'Xác định công ty hiện tại')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — UC-01 Xem danh sách và tìm kiếm')

d.h2('3.2 Mô tả chi tiết')
d.p('Bộ lọc:')
d.field_table([
    ('Tìm kiếm nhanh', 'Tìm theo tên dịch vụ / chi phí...', 'Textbox', 'Người dùng nhập',
     'Không', '255', 'Chỉ áp dụng khi bấm nút Tìm kiếm'),
    ('Tên dịch vụ / chi phí', 'Nhập tên', 'Textbox', 'Người dùng nhập', 'Không', '255',
     'Tìm gần đúng ở mọi vị trí trong tên'),
    ('Phân loại', 'Chọn phân loại', 'Dropdown',
     'Dịch vụ có tính doanh thu / Chi phí khác', 'Không', '–', 'Bỏ trống là lấy tất cả'),
    ('Trạng thái', 'Chọn trạng thái', 'Dropdown', 'Hoạt động / Khoá', 'Không', '–',
     'Bỏ trống là lấy tất cả'),
    ('Người cập nhật', 'Chọn người cập nhật', 'Dropdown', 'Danh sách nhân viên', 'Không', '–',
     'Lọc theo người cập nhật gần nhất'),
    ('Tìm kiếm', '–', 'Button', '–', '–', '–', 'Áp dụng bộ lọc và quay về trang 1'),
    ('Làm mới', '–', 'Button', '–', '–', '–', 'Xoá toàn bộ điều kiện lọc và tải lại danh sách'),
])

d.p('Bảng danh sách:')
d.field_table([
    ('STT', '–', 'Label', 'Số thứ tự theo trang', '–', '–', 'Không sắp xếp'),
    ('Tên dịch vụ / chi phí', '–', 'Text', 'Lấy từ hệ thống', '–', '255',
     'Tự xuống dòng khi dài. Cho phép sắp xếp'),
    ('Phân loại', '–', 'Badge', 'Dịch vụ có tính doanh thu / Chi phí khác', '–', '–',
     'Hiển thị nhãn tiếng Việt, không hiển thị giá trị số'),
    ('ĐM giảm giá', '–', 'Number', 'Lấy từ hệ thống', '–', '0 – 100',
     'Mức của CÔNG TY người dùng đang đăng nhập; để trống nếu chưa khai báo. Cho phép sắp xếp'),
    ('% Tính giá vốn', '–', 'Number', 'Lấy từ hệ thống', '–', '≥ 0',
     'Hiển thị đúng phần thập phân. Cho phép sắp xếp'),
    ('% VAT', '–', 'Number', 'Lấy từ hệ thống', '–', '0 – 100', 'Cho phép sắp xếp'),
    ('Trạng thái', '–', 'Badge', 'Hoạt động / Khoá', '–', '–',
     'Nút Khoá / Mở khoá nằm ngay trong cột này. Cho phép sắp xếp'),
    ('Cập nhật', '–', 'Text', 'Lấy từ hệ thống', '–', '–',
     'Thời điểm cập nhật gần nhất kèm người cập nhật. Cho phép sắp xếp'),
    ('Hành động', '–', 'Icon Button', 'Xem / Sửa / Xoá', '–', '–',
     'Nút Sửa và Xoá ẩn khi không có P1; vô hiệu hoá kèm chú giải khi bản ghi không đủ điều kiện'),
    ('Tạo mới', '–', 'Button', '–', '–', '–', 'Ẩn khi người dùng không có P1'),
    ('Xuất Excel', '–', 'Button', '–', '–', '–', 'Luôn hiển thị với user có quyền truy cập màn'),
    ('Phân trang', '–', 'Pagination', 'Mặc định 10 dòng/trang', '–', '–',
     'Xem quy tắc chung mục 2.1.5'),
    ('Trạng thái rỗng', '–', 'Label', 'Không có dữ liệu phù hợp bộ lọc.', '–', '–',
     'Hiển thị khi danh sách trống'),
])

d.h2('3.3 Danh sách event và thông báo')
d.notice_table([
    ('Truy cập màn hình', 'System',
     'Kiểm tra quyền P1 hoặc P2; không có quyền → điều hướng về trang 404 (giao diện), '
     'API trả về 403.\n'
     'Xác định công ty hiện tại của người dùng để lấy dữ liệu ĐM giảm giá.\n'
     'Khôi phục bộ lọc đã lưu và tải danh sách trang 1.'),
    ('Không xác định được công ty', 'System',
     'Màn hình vẫn hiển thị bình thường, toàn bộ cột ĐM giảm giá để trống.'),
    ('Nhập ô tìm kiếm nhanh', 'Keypress', 'Ghi nhận từ khoá, chưa gọi tìm kiếm.'),
    ('Bấm Tìm kiếm', 'Click', 'Quay về trang 1 và tải lại danh sách theo toàn bộ điều kiện lọc.'),
    ('Đổi tiêu chí lọc nâng cao', 'Change',
     'Quay về trang 1 và tải lại danh sách ngay theo điều kiện mới.'),
    ('Bấm Làm mới', 'Click', 'Xoá toàn bộ điều kiện lọc, quay về trang 1 và tải lại danh sách.'),
    ('Bấm tiêu đề cột', 'Click',
     'Đổi cột và chiều sắp xếp, tải lại danh sách. Cột ngoài danh sách được phép sắp xếp thì '
     'bỏ qua điều kiện sắp xếp.'),
    ('Đổi trang / đổi số dòng', 'Click / Change',
     'Tải lại danh sách theo phân trang mới, giữ nguyên bộ lọc. Đổi số dòng thì quay về trang 1.'),
    ('Không có kết quả', 'System', 'Hiển thị “Không có dữ liệu phù hợp bộ lọc.”'),
    ('Lỗi khi tải danh sách', 'System', 'Hiển thị thông báo “Lỗi khi tải dữ liệu”.'),
])

# ================================================================ 4. UC-02
d.h1('4. Chức năng Thêm mới')

d.h2('4.1 Giới thiệu và cách truy cập')
d.p('Cho phép người quản lý danh mục khai báo một dịch vụ sửa chữa hoặc chi phí khác mới. '
    'Bản ghi mới luôn ở trạng thái Hoạt động — modal thêm mới không hiển thị ô Trạng thái.')
d.p('Mức ĐM giảm giá nhập ở đây chỉ ghi cho công ty người dùng đang đăng nhập, không ảnh hưởng '
    'tới công ty khác.')
access(['Thao tác: bấm nút “Tạo mới” dưới bảng danh sách → mở modal “Thêm dịch vụ / chi phí”.'])
d.uc_figure('UC-02', 'Thêm mới dịch vụ / chi phí', 'crud',
            [('include', 'Kiểm tra trùng tên'),
             ('include', 'Ghi ĐM giảm giá theo công ty hiện tại')],
            caption='Biểu đồ Use Case — UC-02 Thêm mới')

d.h2('4.2 Mô tả chi tiết')
d.field_table([
    ('Tên dịch vụ / chi phí', 'VD: Chi phí sửa chữa, thay thế', 'Textbox', 'Người dùng nhập',
     'Có', '255', 'Không được trùng với bản ghi khác trong nhóm dữ liệu của màn'),
    ('% Tính giá vốn', 'VD: 80', 'Textbox', 'Người dùng nhập', 'Có', '≥ 0',
     'Nhận số thập phân, dấu phẩy được hiểu là dấu thập phân'),
    ('% VAT', 'VD: 8', 'Textbox', 'Người dùng nhập', 'Có', '0 – 100',
     'Nhận số thập phân, dấu phẩy được hiểu là dấu thập phân'),
    ('ĐM giảm giá (%)', 'Bỏ trống nếu không có', 'Textbox', 'Người dùng nhập', 'Không', '0 – 100',
     'Ghi riêng cho công ty người dùng đang đăng nhập'),
    ('Dịch vụ có tính doanh thu', '–', 'Checkbox', 'Bật / Tắt', 'Không', '–',
     'Bật là “Dịch vụ có tính doanh thu”, tắt là “Chi phí khác”. Mặc định tắt'),
    ('Trạng thái', '–', 'Dropdown', '–', '–', '–',
     'KHÔNG hiển thị ở chế độ thêm mới; bản ghi mới luôn ở trạng thái Hoạt động'),
    ('Lưu', '–', 'Button', '–', '–', '–', 'Vô hiệu hoá trong lúc đang gửi'),
    ('Lưu & Tiếp tục', '–', 'Button', '–', '–', '–',
     'Lưu rồi giữ modal mở với các trường trống để nhập tiếp; chỉ có ở chế độ thêm mới'),
    ('Đóng', '–', 'Button', '–', '–', '–', 'Đóng modal, huỷ dữ liệu đang nhập dở'),
])

d.h2('4.3 Danh sách event và thông báo')
d.notice_table([
    ('Bấm Tạo mới', 'Click',
     'Kiểm tra quyền P1 (không có quyền thì nút không hiển thị).\n'
     'Xoá dữ liệu cũ trong modal và mở modal “Thêm dịch vụ / chi phí”.'),
    ('Bấm Lưu', 'Click',
     'Before:\n'
     '– Kiểm tra quyền P1; không có quyền → “Bạn không có quyền thực hiện chức năng này.” '
     'và dừng xử lý.\n'
     'During:\n'
     '– Tên dịch vụ / chi phí trống → “Bắt buộc phải nhập”\n'
     '– Tên đã tồn tại → “Đã tồn tại trên hệ thống”\n'
     '– Tên vượt 255 ký tự → “Tối đa 255 ký tự”\n'
     '– % Tính giá vốn trống → “Bắt buộc phải nhập”\n'
     '– % Tính giá vốn không phải số → “Phải là số”\n'
     '– % Tính giá vốn nhỏ hơn 0 → “Không được nhỏ hơn 0”\n'
     '– % VAT trống → “Bắt buộc phải nhập”\n'
     '– % VAT không phải số → “Phải là số”\n'
     '– % VAT lớn hơn 100 → “Tối đa 100”\n'
     '– ĐM giảm giá không phải số → “Phải là số”\n'
     '– ĐM giảm giá lớn hơn 100 → “Tối đa 100”\n'
     '– Có lỗi validate → không thực hiện bước After.\n'
     'After:\n'
     '– Ghi bản ghi mới ở trạng thái Hoạt động kèm người tạo.\n'
     '– Ghi ĐM giảm giá cho công ty hiện tại (nếu có nhập).\n'
     '– Hiển thị “Tạo chi phí thành công”, đóng modal và tải lại danh sách.'),
    ('Bấm Lưu & Tiếp tục', 'Click',
     'Xử lý như bấm Lưu; sau khi ghi thành công thì giữ modal mở và xoá trắng các trường '
     'để nhập bản ghi kế tiếp.'),
    ('Nhập số có dấu phẩy', 'Change / Blur',
     'Dấu phẩy được hiểu là dấu THẬP PHÂN (12,5 = 12.5), không phải phân cách nghìn — cả ba '
     'trường phần trăm đều tối đa 100 nên không có tình huống phân cách nghìn.'),
    ('Bấm Đóng', 'Click', 'Đóng modal và huỷ dữ liệu đang nhập dở, không lưu bất kỳ thay đổi nào.'),
])

# ================================================================ 5. UC-03
d.h1('5. Chức năng Sửa')

d.h2('5.1 Giới thiệu và cách truy cập')
d.p('Cho phép người quản lý danh mục cập nhật thông tin của một dịch vụ / chi phí đã khai báo, '
    'bao gồm cả Trạng thái.')
d.p('Hai trường hợp bị chặn sửa: bản ghi là chi phí hệ thống (“Chi phí đi lại”, “Chi phí vận '
    'chuyển”) và bản ghi đang ở trạng thái Khoá — muốn sửa phải mở khoá trước. Cả hai đều được '
    'kiểm tra lại tại máy chủ, không phụ thuộc giao diện.')
access(['Thao tác: bấm biểu tượng Sửa ở dòng dữ liệu → mở modal “Sửa dịch vụ / chi phí”.'])
d.uc_figure('UC-03', 'Sửa dịch vụ / chi phí', 'crud',
            [('include', 'Kiểm tra trùng tên'),
             ('extend', 'Chặn sửa chi phí hệ thống và chi phí đang Khoá')],
            caption='Biểu đồ Use Case — UC-03 Sửa')

d.h2('5.2 Mô tả chi tiết')
d.field_table([
    ('Thông tin cập nhật gần nhất', '–', 'Label', 'Lấy từ hệ thống', '–', '–',
     'Hiển thị trên tiêu đề modal khi bản ghi đã từng được cập nhật'),
    ('Tên dịch vụ / chi phí', 'VD: Chi phí sửa chữa, thay thế', 'Textbox', 'Lấy từ hệ thống',
     'Có', '255', 'Cho phép sửa, không được trùng bản ghi khác'),
    ('% Tính giá vốn', 'VD: 80', 'Textbox', 'Lấy từ hệ thống', 'Có', '≥ 0', 'Cho phép sửa'),
    ('% VAT', 'VD: 8', 'Textbox', 'Lấy từ hệ thống', 'Có', '0 – 100', 'Cho phép sửa'),
    ('ĐM giảm giá (%)', 'Bỏ trống nếu không có', 'Textbox', 'Lấy từ hệ thống', 'Không', '0 – 100',
     'Chỉ ghi / xoá cho công ty hiện tại; xoá trống là bỏ ĐM giảm giá của công ty đó'),
    ('Dịch vụ có tính doanh thu', '–', 'Checkbox', 'Lấy từ hệ thống', 'Không', '–', 'Cho phép bật/tắt'),
    ('Trạng thái', 'Chọn trạng thái', 'Dropdown', 'Hoạt động / Khoá', 'Không', '–',
     'CHỈ hiển thị ở chế độ sửa; không gửi thì giữ nguyên giá trị cũ'),
    ('Cảnh báo chi phí hệ thống', '–', 'Label', 'Chi phí này nằm trong danh sách không được phép '
     'sửa của hệ thống.', '–', '–', 'Hiện khi bản ghi không được phép sửa'),
    ('Lưu', '–', 'Button', '–', '–', '–', 'Ẩn khi modal ở chế độ chỉ đọc'),
    ('Đóng', '–', 'Button', '–', '–', '–', 'Đóng modal, huỷ thay đổi chưa lưu'),
])

d.h2('5.3 Danh sách event và thông báo')
d.notice_table([
    ('Bấm biểu tượng Sửa', 'Click',
     'Kiểm tra quyền P1 (không có quyền thì biểu tượng không hiển thị).\n'
     'Nạp dữ liệu bản ghi và mở modal “Sửa dịch vụ / chi phí”.\n'
     'Bản ghi không được phép sửa → hiển thị dòng cảnh báo trong modal.'),
    ('Bấm Lưu', 'Click',
     'Before:\n'
     '– Kiểm tra quyền P1; không có quyền → “Bạn không có quyền thực hiện chức năng này.” '
     'và dừng xử lý.\n'
     'During:\n'
     '– Các lỗi hợp lệ giống chức năng Thêm mới (mục 4.3)\n'
     '– Tên trùng bản ghi khác → “Đã tồn tại trên hệ thống”\n'
     '– Bản ghi là chi phí hệ thống → “Chi phí này không được phép sửa”\n'
     '– Bản ghi đang ở trạng thái Khoá → “Chi phí đang bị khóa, hãy mở khóa trước khi sửa”\n'
     '– Có lỗi → không thực hiện bước After.\n'
     'After:\n'
     '– Cập nhật bản ghi kèm người cập nhật.\n'
     '– Ghi hoặc xoá ĐM giảm giá của công ty hiện tại theo giá trị vừa nhập.\n'
     '– Hiển thị “Cập nhật chi phí thành công”, đóng modal và tải lại danh sách.'),
    ('Xem chi tiết (UC-04)', 'Click',
     'Bấm biểu tượng Xem → mở modal “Xem dịch vụ / chi phí” ở chế độ chỉ đọc: mọi trường bị vô '
     'hiệu hoá, các nút Lưu không hiển thị. Người dùng chỉ có P2 vẫn xem được.'),
    ('Bản ghi không còn tồn tại', 'System',
     'Hiển thị thông báo dữ liệu đã thay đổi và yêu cầu tải lại danh sách.'),
    ('Bấm Đóng', 'Click', 'Đóng modal, huỷ thay đổi chưa lưu.'),
])

# ================================================================ 6. UC-05 + UC-06
d.h1('6. Chức năng Khoá / Mở khoá và Xoá')

d.h2('6.1 Giới thiệu và cách truy cập')
d.p('Khoá / Mở khoá: đổi trạng thái sử dụng của dịch vụ / chi phí mà vẫn giữ nguyên dữ liệu '
    'lịch sử. Dịch vụ đang Khoá không xuất hiện ở các danh sách chọn của màn nghiệp vụ khác.')
d.p('Xoá: xoá bản ghi khai báo nhầm. Nếu dịch vụ / chi phí đã phát sinh ở Báo giá hãng hoặc '
    'Hợp đồng hãng thì hệ thống KHÔNG xoá mà tự chuyển sang trạng thái Khoá, và thông báo cho '
    'người dùng biết. Chi phí hệ thống và bản ghi đang Khoá đều không xoá được.')
access(['Thao tác Khoá / Mở khoá: bấm biểu tượng khoá nằm ngay trong cột Trạng thái.',
        'Thao tác Xoá: bấm biểu tượng Xoá ở cột Hành động.'])
d.uc_figure('UC-06', 'Xoá dịch vụ / chi phí', 'action',
            [('include', 'Kiểm tra chứng từ phát sinh'),
             ('extend', 'Chuyển sang trạng thái Khoá thay vì xoá')],
            caption='Biểu đồ Use Case — UC-05 Khoá / Mở khoá và UC-06 Xoá')

d.h2('6.2 Mô tả chi tiết')
d.field_table([
    ('Biểu tượng Khoá / Mở khoá', '–', 'Icon Button', 'Khoá hoặc Mở khoá theo trạng thái hiện tại',
     '–', '–', 'Nằm trong cột Trạng thái. Ẩn khi không có P1; vô hiệu hoá khi bản ghi là chi phí '
     'hệ thống hoặc trạng thái không phù hợp'),
    ('Biểu tượng Xoá', '–', 'Icon Button', '–', '–', '–',
     'Ẩn khi không có P1; vô hiệu hoá khi bản ghi là chi phí hệ thống hoặc đang ở trạng thái Khoá'),
    ('Chú giải nút', '–', 'Label', 'Nêu hành động hoặc lý do bị chặn', '–', '–',
     'Hiện khi rê chuột; nút bị vô hiệu hoá bắt buộc có lý do'),
    ('Hộp thoại xác nhận', '–', 'Modal', 'Nêu rõ tên dịch vụ / chi phí bị tác động', '–', '–',
     'Tiêu đề đổi theo hành động: “Xác nhận xóa” / “Xác nhận khóa” / “Xác nhận mở khóa”'),
    ('Nút xác nhận', '–', 'Button', 'Xóa / Khóa / Mở khóa', '–', '–', 'Nhãn đổi theo hành động'),
    ('Huỷ', '–', 'Button', '–', '–', '–', 'Đóng hộp thoại, không thực hiện gì'),
])

d.h2('6.3 Danh sách event và thông báo')
d.notice_table([
    ('Bấm biểu tượng Khoá / Mở khoá', 'Click',
     'Kiểm tra quyền P1 và điều kiện bản ghi; không đủ điều kiện thì nút bị vô hiệu hoá kèm '
     'chú giải.\nMở hộp thoại xác nhận tương ứng hành động.'),
    ('Xác nhận Khoá', 'Click',
     'During:\n'
     '– Bản ghi là chi phí hệ thống → “Chi phí này không được phép khóa”\n'
     '– Bản ghi đã ở trạng thái Khoá → “Chi phí đang bị khóa”\n'
     'After:\n– Đổi trạng thái sang Khoá.\n'
     '– Hiển thị “Khóa chi phí thành công” và tải lại danh sách.'),
    ('Xác nhận Mở khoá', 'Click',
     'During:\n'
     '– Bản ghi là chi phí hệ thống → “Chi phí này không được phép mở khóa”\n'
     '– Bản ghi đang Hoạt động → “Chi phí đang hoạt động”\n'
     'After:\n– Đổi trạng thái sang Hoạt động.\n'
     '– Hiển thị “Mở khóa chi phí thành công” và tải lại danh sách.'),
    ('Bấm biểu tượng Xoá', 'Click',
     'Kiểm tra quyền P1 và điều kiện xoá.\n'
     'Kiểm tra bản ghi đã phát sinh chứng từ chưa; nếu có thì hộp thoại đổi tiêu đề thành '
     '“Xác nhận khóa” để người dùng biết trước kết quả là khoá chứ không phải xoá.'),
    ('Xác nhận Xoá', 'Click',
     'Before:\n'
     '– Kiểm tra quyền P1; không có quyền → “Bạn không có quyền thực hiện chức năng này.” '
     'và dừng xử lý.\n'
     'During:\n'
     '– Bản ghi là chi phí hệ thống hoặc đang Khoá → “Chi phí này không được phép xóa hoặc '
     'đã bị khóa”, không thực hiện bước After.\n'
     'After:\n'
     '– Chưa phát sinh chứng từ → xoá bản ghi, hiển thị “Xóa chi phí thành công”.\n'
     '– Đã phát sinh chứng từ → KHÔNG xoá, chuyển sang trạng thái Khoá và hiển thị '
     '“Chi phí đang được sử dụng nên đã được chuyển sang trạng thái Khóa”.\n'
     '– Tải lại danh sách.'),
    ('Bấm Huỷ', 'Click', 'Đóng hộp thoại, không thay đổi dữ liệu.'),
])

# ================================================================ 7. UC-07
d.h1('7. Chức năng Xuất Excel')

d.h2('7.1 Giới thiệu và cách truy cập')
d.p('Cho phép người dùng tải danh sách dịch vụ / chi phí ra file Excel để đối chiếu hoặc gửi ra '
    'ngoài. File lấy toàn bộ dữ liệu khớp bộ lọc đang áp dụng, không giới hạn theo trang đang xem.')
access(['Thao tác: bấm nút “Xuất Excel” dưới bảng danh sách.'])
d.uc_figure('UC-07', 'Xuất Excel danh mục', 'io',
            [('include', 'Áp bộ lọc đang dùng')],
            actor=ACTOR_BOTH,
            caption='Biểu đồ Use Case — UC-07 Xuất Excel')

d.h2('7.2 Mô tả chi tiết')
d.field_table([
    ('Xuất Excel', '–', 'Button', '–', '–', '–', 'Nằm ở thanh thao tác dưới bảng danh sách'),
    ('Nội dung file', '–', 'Table/Grid', 'Các cột như bảng danh sách', '–', '–',
     'Lấy toàn bộ bản ghi khớp bộ lọc, không chỉ trang đang xem'),
    ('Thông báo lỗi', '–', 'Toast / Alert', 'Nội dung lỗi trả về từ hệ thống', '–', '–',
     'Hiển thị khi không dựng được file'),
])

d.h2('7.3 Danh sách event và thông báo')
d.notice_table([
    ('Bấm Xuất Excel', 'Click',
     'Before:\n– Kiểm tra quyền P1 hoặc P2; không có quyền → API trả về 403.\n'
     'After:\n– Dựng file Excel theo bộ lọc hiện tại và tải xuống.'),
    ('Không có dữ liệu khớp bộ lọc', 'System', 'Vẫn trả file, chỉ gồm dòng tiêu đề.'),
    ('Lỗi khi dựng file', 'System', 'Hiển thị thông báo lỗi, không tải file.'),
])

d.save()
