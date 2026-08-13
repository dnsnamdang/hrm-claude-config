# -*- coding: utf-8 -*-
"""Sinh SRS theo FORM CHUAN cho man 'Cap nhat nhanh gia dich vu' (phan he CSKH).

Man 1 form 2 truong, moi lan luu la GHI DE he so + dinh muc dam phan cho TOAN BO goi bao duong.

Nguon doi chieu (doc truc tiep tu code):
  BE  Modules/CustomerCare/{Routes/api.php,
        Entities/ServicePriceConfig/ServicePriceConfig.php,
        Http/Requests/ServicePriceConfig/ServicePriceConfigRequest.php,
        Http/Controllers/V1/ServicePriceConfigController.php,
        Services/ServicePriceConfigService.php,
        Transformers/ServicePriceConfigResource/ServicePriceConfigResource.php}
  FE  hrm-client/pages/customer-care/service-price-config/index.vue
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
from srs_docx_lib import SrsDoc  # noqa: E402

OUT = (r"d:\CompanyProject\hrm\hrm-claude-config\hrm\.plans\gop-db"
       r"\customer-care-service-price-config\SRS - Cập nhật nhanh giá dịch vụ.docx")

ACTOR = 'Người cập nhật giá dịch vụ (P1)'

d = SrsDoc(
    out=OUT,
    menu='Phân hệ Chăm sóc khách hàng → Danh mục - Dịch vụ → Cập nhật nhanh giá dịch vụ',
    route='/customer-care/service-price-config',
    full_url='https://<host-hrm>/customer-care/service-price-config',
    img_prefix='spc_')

# ================================================================ TRANG BIA
d.h1('SOFTWARE REQUIREMENTS SPECIFICATION (SRS)')
d.h2('Màn hình: Cập nhật nhanh giá dịch vụ')
d.h2('Phân hệ: Chăm sóc khách hàng (CSKH) – nhóm Danh mục - Dịch vụ')

d.info_table([
    ('Mã màn hình', 'CSKH-DM-SERVICEPRICE'),
    ('Đường dẫn', '/customer-care/service-price-config'),
    ('Phiên bản', '1.0'),
    ('Ngày lập', '12/08/2026'),
    ('Người lập', '@junfoke'),
    ('Trạng thái tài liệu', 'Draft'),
    ('Nguồn đối chiếu', 'Màn ERP admin/service-config-price (bảng service_price_config trên DB gộp)'),
])

# ================================================================ 1. GIOI THIEU
d.h1('1. Giới thiệu')

d.h2('1.1 Mục đích')
d.p('Tài liệu này đặc tả yêu cầu phần mềm (SRS) cho màn hình cập nhật nhanh giá dịch vụ, nhằm:')
d.bullets([
    'Thống nhất yêu cầu giữa BA/PO/Dev/Test',
    'Là căn cứ nghiệm thu chức năng và phân quyền',
    'Cảnh báo rõ đặc thù nguy hiểm của màn hình: mỗi lần lưu là GHI ĐÈ hệ số và định mức đàm phán '
    'cho TOÀN BỘ gói bảo dưỡng, kể cả gói đã được chỉnh riêng',
    'Làm rõ điều kiện tính lại giá gốc của cấp dịch vụ và các trường hợp gói bị bỏ qua',
])

d.h2('1.2 Phạm vi')
d.p('Màn hình Cập nhật nhanh giá dịch vụ cung cấp chức năng:')
d.bullets([
    'Xem cấu hình giá dịch vụ dùng chung hiện tại gồm 2 giá trị: Hệ số giá bán dịch vụ và '
    'Định mức đàm phán giá (%)',
    'Xem số gói bảo dưỡng sẽ bị ảnh hưởng nếu lưu và thông tin lần cập nhật gần nhất',
    'Cập nhật cấu hình, kèm bước xác nhận trước khi ghi',
    'Áp lại hệ số và định mức đàm phán cho toàn bộ gói bảo dưỡng, tính lại giá gốc của các cấp '
    'dịch vụ khi hệ số thay đổi',
])
d.p('Ngoài phạm vi:')
d.bullets([
    'Thay đổi công thức tính giá gốc của cấp dịch vụ',
    'Chỉnh sửa hệ số hoặc định mức của riêng từng gói — việc đó thuộc màn Danh mục gói bảo dưỡng',
    'Bỏ hành vi ghi đè hàng loạt: giữ nguyên như hệ thống ERP theo yêu cầu nghiệp vụ',
    'Lịch sử thay đổi cấu hình, hoàn tác thay đổi đã ghi',
])

d.h2('1.3 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hệ số giá bán dịch vụ', 'Hệ số dùng để tính giá gốc của cấp dịch vụ từ đơn giá công và '
                              'định mức công'),
    ('Định mức đàm phán giá (%)', 'Tỷ lệ phần trăm tối đa được phép giảm khi đàm phán giá dịch vụ'),
    ('Gói bảo dưỡng', 'Gói dịch vụ bảo dưỡng bán cho khách hàng, gồm nhiều cấp dịch vụ'),
    ('Cấp dịch vụ', 'Một mức dịch vụ trong gói bảo dưỡng, có định mức công và giá gốc riêng'),
    ('Giá gốc', 'Giá cơ sở của một cấp dịch vụ, tính từ đơn giá công của công ty × định mức công '
                '× hệ số giá bán dịch vụ'),
    ('Đơn giá công', 'Đơn giá nhân công của công ty gắn với gói bảo dưỡng'),
    ('Ghi đè hàng loạt', 'Một lần lưu áp giá trị mới cho toàn bộ gói bảo dưỡng, không loại trừ gói nào'),
    ('P1', 'Quyền “Cập nhật nhanh giá dịch vụ”'),
    ('SRS', 'Software Requirements Specification'),
], widths=[1.8, 4.2])

# ================================================================ 2. TONG QUAN
d.h1('2. Tổng quan')

d.h2('2.1 Bối cảnh nghiệp vụ')
d.p('Cấu hình giá dịch vụ dùng chung là tham số nền của toàn bộ nghiệp vụ báo giá dịch vụ, dùng để:')
d.bullets([
    'Tính giá gốc cho từng cấp dịch vụ của gói bảo dưỡng',
    'Khống chế mức giảm giá tối đa khi đàm phán với khách hàng',
    'Điều chỉnh nhanh mặt bằng giá dịch vụ của toàn hệ thống trong một thao tác, thay vì sửa từng gói',
])
d.p('Do đó cần:')
d.bullets([
    'Giới hạn quyền sử dụng cho đúng người phụ trách giá dịch vụ',
    'Bắt buộc xác nhận trước khi ghi và nêu rõ số gói bảo dưỡng sẽ bị ảnh hưởng — màn ERP cũ bấm '
    'Lưu là chạy ngay, không cảnh báo gì',
    'Không xoá mất giá đang dùng của những gói thiếu dữ liệu để tính: bỏ qua và báo lại danh sách '
    'gói bị bỏ qua, thay vì ghi giá về 0 như màn ERP cũ',
    'Sao lưu dữ liệu trước khi thao tác lần đầu, vì thay đổi ghi đè hàng loạt và không hoàn tác được',
])

d.h2('2.2 Nhóm người dùng')
d.bullets([
    'Người dùng có quyền P1: được xem và cập nhật cấu hình giá dịch vụ',
    'Người dùng không có P1: bị chặn truy cập',
    'Quyền được công nhận từ cả hệ thống ERP lẫn HRM: người đã có quyền tương ứng ở ERP vẫn dùng '
    'được màn hình này',
])

# ================================================================ 3. PHAN QUYEN
d.h1('3. Phân quyền và kiểm soát truy cập')

d.h2('3.1 Danh sách quyền')
d.table(['Ký hiệu', 'Tên quyền', 'Mã quyền', 'Nhóm quyền'], [
    ('P1', 'Cập nhật nhanh giá dịch vụ', '1130', 'Danh mục dịch vụ bảo dưỡng'),
], widths=[0.8, 2.8, 0.9, 1.5])
d.p('Ghi chú: hệ thống ERP đã có sẵn một quyền cùng tên (mã 100320). Quyền của HRM được khai trùng '
    'tên có chủ đích và màn hình kiểm tra quyền theo TÊN, nên người dùng có quyền ở ERP hoặc ở HRM '
    'đều truy cập được, không phải cấp lại quyền hai lần.')

d.h2('3.2 Quy tắc truy cập bắt buộc')
d.bullets([
    'Chỉ user có P1 mới được truy cập màn hình.',
    'User không có P1: không hiển thị menu điều hướng tới màn hình.',
    'User không có P1: truy cập trực tiếp URL bị chặn, gọi API trả về lỗi 403.',
    'Nút Lưu chỉ hiển thị với user có P1; user không có quyền gọi trực tiếp API cập nhật vẫn bị '
    'chặn ở máy chủ.',
])

d.h2('3.3 Ma trận phân quyền')
d.table(['Chức năng', 'P1', 'Không có quyền'], [
    ('Truy cập màn', '✅', '❌'),
    ('Xem cấu hình hiện tại', '✅', '❌'),
    ('Cập nhật cấu hình', '✅', '❌'),
], widths=[3.4, 1.0, 1.6])

# ================================================================ 4. FUNCTION LIST
d.h1('4. Danh mục chức năng (Function list)')
d.table(['ID', 'Chức năng', 'Mô tả đặc tả thu nhỏ (Mini-Spec)', 'Quyền'], [
    ('FR-01', 'Truy cập màn hình',
     'Kiểm tra quyền P1. Không có quyền sẽ bị chặn (ẩn menu, chặn URL, API trả 403).', 'P1'),
    ('FR-02', 'Xem cấu hình giá dịch vụ',
     'Hiển thị Hệ số giá bán dịch vụ và Định mức đàm phán giá hiện tại, số gói bảo dưỡng sẽ bị '
     'ảnh hưởng và thông tin lần cập nhật gần nhất.', 'P1'),
    ('FR-03', 'Cập nhật cấu hình giá dịch vụ',
     'Nhập giá trị mới, xác nhận qua popup nêu rõ số gói bị ảnh hưởng, sau đó ghi cấu hình và áp '
     'lại cho toàn bộ gói bảo dưỡng. Kết quả nêu số gói đã áp, số cấp dịch vụ đã tính lại giá và '
     'danh sách gói bị bỏ qua.', 'P1'),
], widths=[0.7, 1.4, 3.4, 0.8])

# ================================================================ 5. DAC TA
d.h1('5. Đặc tả chi tiết theo từng chức năng (FUNCTIONAL PACKAGING)')

d.h2('5.1 Sơ đồ UML tổng quan')
d.p('Sơ đồ Use Case tổng quan của màn hình, thể hiện quan hệ giữa người dùng và ba chức năng:')
d.overview_figure(
    'HỆ THỐNG HRM — Cập nhật nhanh giá dịch vụ',
    [(ACTOR, [0, 1, 2])],
    [('FR-01', 'Truy cập màn hình', 'view', None),
     ('FR-02', 'Xem cấu hình giá dịch vụ', 'view', None),
     ('FR-03', 'Cập nhật cấu hình giá dịch vụ', 'crud',
      '«include» Áp lại giá cho toàn bộ gói bảo dưỡng')],
    'Sơ đồ Use Case tổng quan màn hình Cập nhật nhanh giá dịch vụ')

d.h2('5.2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------- 5.2.1
d.h2('5.2.1 Truy cập màn hình cập nhật nhanh giá dịch vụ')

d.h3('5.2.1.1 Biểu đồ Usecase')
d.uc_figure('FR-01', 'Truy cập màn hình cập nhật nhanh giá dịch vụ', 'view',
            [('include', 'Kiểm tra quyền truy cập')], actor=ACTOR)

d.h3('5.2.1.2 Giới thiệu')
d.intro_table(
    'Truy cập màn hình cập nhật nhanh giá dịch vụ',
    'Cho phép người phụ trách giá dịch vụ truy cập vào màn hình cấu hình giá dịch vụ dùng chung.',
    'Admin; User được phân quyền P1',
    'Người dùng đã đăng nhập thành công vào hệ thống.',
    '1. Người dùng chọn menu Chăm sóc khách hàng → Danh mục - Dịch vụ → Cập nhật nhanh giá dịch vụ.\n'
    '2. Hệ thống xác thực quyền truy cập (P1).\n'
    '3. Hệ thống điều hướng tới màn hình và tải cấu hình hiện tại cùng số gói bảo dưỡng sẽ bị '
    'ảnh hưởng.',
    '• Người dùng không có quyền → Hệ thống ẩn menu; truy cập trực tiếp URL bị chặn.\n'
    '• Gọi trực tiếp API khi không có quyền → Hệ thống trả về lỗi 403.\n'
    '• Chưa từng có cấu hình nào được lưu → Hệ thống hiển thị form trống, không báo lỗi.',
    'Quyền được đối chiếu theo TÊN nên người dùng có quyền tương ứng ở hệ thống ERP cũng truy cập '
    'được màn hình này.')

d.h3('5.2.1.3 Layout màn hình')
d.layout('Ghi chú: tài liệu này không đính kèm ảnh chụp màn hình, người đọc truy cập trực tiếp '
         'đường dẫn trên để đối chiếu giao diện.')

d.h3('5.2.1.4 Tiêu chí nghiệm thu')
d.p('Người dùng có quyền truy cập:')
d.bullets([
    'Nhìn thấy menu Cập nhật nhanh giá dịch vụ.',
    'Truy cập được màn hình và thấy đủ 2 ô nhập, dòng cảnh báo số gói bị ảnh hưởng và nút Lưu.',
])
d.p('Người dùng không có quyền:')
d.bullets([
    'Không nhìn thấy menu.',
    'Truy cập trực tiếp URL bị chặn, gọi API trả về 403.',
])
d.p('Trường hợp đặc biệt:')
d.bullets([
    'Người dùng chỉ có quyền tương ứng ở hệ thống ERP vẫn truy cập và lưu được.',
    'Hệ thống chưa có cấu hình nào thì màn hình vẫn mở được với form trống, không báo lỗi.',
])

d.h3('5.2.1.5 Danh sách event và xử lý event')
d.event_table([
    ('Click menu Cập nhật nhanh giá dịch vụ', 'Click',
     'Kiểm tra quyền P1 và điều hướng tới màn hình.'),
    ('Truy cập URL trực tiếp', 'System',
     'Kiểm tra quyền; nếu không hợp lệ → chặn truy cập (giao diện) và trả về lỗi 403 (API).'),
    ('Load màn hình', 'System',
     'Tải cấu hình hiện tại, số gói bảo dưỡng và số cấp dịch vụ sẽ bị ảnh hưởng, '
     'kèm thông tin lần cập nhật gần nhất.'),
])

# ---------------------------------------------------------- 5.2.2
d.h2('5.2.2 Xem cấu hình giá dịch vụ')

d.h3('5.2.2.1 Giới thiệu')
d.intro_table(
    'Xem cấu hình giá dịch vụ',
    'Hiển thị cấu hình giá dịch vụ dùng chung đang áp dụng cho toàn hệ thống, kèm cảnh báo phạm vi '
    'ảnh hưởng nếu thay đổi.',
    'Admin; User được phân quyền P1',
    'Người dùng truy cập thành công màn hình cập nhật nhanh giá dịch vụ.',
    '1. Hệ thống lấy bản ghi cấu hình giá dịch vụ dùng chung.\n'
    '2. Hệ thống đếm số gói bảo dưỡng và số cấp dịch vụ sẽ bị ảnh hưởng nếu lưu.\n'
    '3. Hệ thống điền giá trị hiện tại vào 2 ô nhập và hiển thị dòng cảnh báo phạm vi ảnh hưởng.\n'
    '4. Hệ thống hiển thị thời điểm và người thực hiện lần cập nhật gần nhất (nếu có).',
    '• Chưa từng có cấu hình → Hai ô nhập để trống, không hiển thị dòng cập nhật gần nhất.\n'
    '• Chưa xác định được người cập nhật gần nhất → Chỉ hiển thị thời điểm cập nhật.',
    '• Toàn hệ thống chỉ có duy nhất một bản ghi cấu hình giá dịch vụ.\n'
    '• Giá trị hiển thị ở ô nhập là số, không kèm định dạng chuỗi thừa.')

d.h3('5.2.2.2 Layout màn hình')
d.layout()

d.h3('5.2.2.3 Mô tả chi tiết giao diện')
d.ui_table([
    ('Khung cấu hình', 'Modal', 'Enable', '–', '–', '–',
     'Thẻ nội dung nằm giữa màn hình, chứa 2 ô nhập và phần ghi chú'),
    ('Hệ số giá bán dịch vụ', 'Textbox', 'Enable', '0,01 – 999,99', 'Có', 'Lấy từ hệ thống',
     'Hệ số dùng để tính giá gốc của cấp dịch vụ'),
    ('Định mức đàm phán giá (%)', 'Textbox', 'Enable', '0 – 99', 'Không', 'Lấy từ hệ thống',
     'Tỷ lệ phần trăm tối đa được phép giảm khi đàm phán'),
    ('Cảnh báo phạm vi ảnh hưởng', 'Label', 'Hiển thị', '–', '–', 'Lấy từ hệ thống',
     'Nêu rõ số gói bảo dưỡng sẽ bị áp lại và việc ghi đè giá trị đã chỉnh riêng ở từng gói'),
    ('Cập nhật gần nhất', 'Label', 'Hiển thị', 'dd/mm/yyyy hh:mm', '–', 'Ẩn',
     'Thời điểm và người thực hiện lần cập nhật gần nhất; ẩn khi chưa từng cập nhật'),
    ('Lưu', 'Button', 'Enable / Ẩn', '–', '–', 'Enable',
     'Mở popup xác nhận. Ẩn khi người dùng không có P1; vô hiệu hoá trong lúc đang lưu'),
    ('Thông báo lỗi theo trường', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị ngay dưới ô nhập tương ứng kèm viền đỏ'),
])

d.h3('5.2.2.4 Tiêu chí nghiệm thu')
d.bullets([
    'Hai ô nhập hiển thị đúng giá trị đang lưu trong hệ thống.',
    'Dòng cảnh báo nêu đúng số gói bảo dưỡng hiện có.',
    'Dòng cập nhật gần nhất hiển thị đúng thời điểm và tên người thực hiện.',
    'Hệ thống chưa có cấu hình nào thì màn hình vẫn mở được, hai ô nhập để trống và không báo lỗi.',
    'Người dùng không có P1 thì nút Lưu không hiển thị.',
])

d.h3('5.2.2.5 Danh sách event và xử lý event')
d.event_table([
    ('Load cấu hình', 'System',
     'Lấy bản ghi cấu hình duy nhất, đếm số gói bảo dưỡng và số cấp dịch vụ bị ảnh hưởng, '
     'điền vào form và phần ghi chú.'),
    ('Nhập giá trị vào ô', 'Change / Blur',
     'Kiểm tra hợp lệ tại chỗ và hiển thị lỗi ngay dưới ô nhập nếu giá trị không hợp lệ.'),
])

# ---------------------------------------------------------- 5.2.3
d.h2('5.2.3 Cập nhật cấu hình giá dịch vụ')

d.h3('5.2.3.1 Biểu đồ Usecase')
d.uc_figure('FR-03', 'Cập nhật cấu hình giá dịch vụ', 'crud',
            [('include', 'Xác nhận phạm vi ảnh hưởng'),
             ('include', 'Áp lại giá cho toàn bộ gói bảo dưỡng'),
             ('extend', 'Bỏ qua gói thiếu công ty hoặc đơn giá công')],
            actor=ACTOR)

d.h3('5.2.3.2 Giới thiệu')
d.intro_table(
    'Cập nhật cấu hình giá dịch vụ',
    'Cho phép người phụ trách giá dịch vụ thay đổi hệ số giá bán và định mức đàm phán dùng chung, '
    'đồng thời áp lại cho toàn bộ gói bảo dưỡng trong một thao tác.',
    'Admin; User được phân quyền P1',
    'Người dùng đang ở màn hình cập nhật nhanh giá dịch vụ và có quyền P1.',
    '1. Người dùng nhập Hệ số giá bán dịch vụ và Định mức đàm phán giá (%).\n'
    '2. Người dùng bấm Lưu.\n'
    '3. Hệ thống kiểm tra hợp lệ tại chỗ; nếu đạt thì mở popup xác nhận nêu rõ số gói bảo dưỡng '
    'sẽ bị áp lại.\n'
    '4. Người dùng bấm Đồng ý.\n'
    '5. Hệ thống ghi cấu hình mới.\n'
    '6. Hệ thống áp hệ số và định mức đàm phán cho toàn bộ gói bảo dưỡng.\n'
    '7. Nếu hệ số thay đổi, hệ thống tính lại giá gốc cho các cấp dịch vụ của từng gói.\n'
    '8. Hệ thống hiển thị kết quả: số gói đã áp, số cấp dịch vụ đã tính lại giá và danh sách gói '
    'bị bỏ qua (nếu có).',
    '• Người dùng bấm Hủy ở popup → Hệ thống đóng popup, không ghi gì.\n'
    '• Hệ số không đổi so với giá trị đang lưu → Hệ thống vẫn áp lại hệ số và định mức cho các gói '
    'nhưng KHÔNG tính lại giá gốc của cấp dịch vụ.\n'
    '• Gói bảo dưỡng chưa gắn công ty hoặc công ty chưa có đơn giá công → Hệ thống bỏ qua phần '
    'tính lại giá của gói đó, giữ nguyên giá đang dùng và nêu mã gói trong thông báo kết quả.\n'
    '• Không nhập Định mức đàm phán giá → Hệ thống giữ nguyên định mức của từng gói.\n'
    '• Xảy ra lỗi giữa chừng → Hệ thống huỷ toàn bộ thay đổi của lần lưu đó, dữ liệu trở về '
    'trạng thái trước khi lưu.',
    '• ĐÂY LÀ THAO TÁC GHI ĐÈ HÀNG LOẠT: mọi gói bảo dưỡng đều bị áp lại, kể cả gói đã được chỉnh '
    'riêng ở màn Danh mục gói bảo dưỡng. Không có chức năng hoàn tác.\n'
    '• Giá gốc của cấp dịch vụ được tính bằng: đơn giá công của công ty × định mức công của cấp '
    'dịch vụ × hệ số giá bán dịch vụ, làm tròn xuống.\n'
    '• Popup xác nhận là điểm khác có chủ đích so với màn ERP cũ — ERP bấm Lưu là chạy ngay.')

d.h3('5.2.3.3 Layout màn hình')
d.layout(modal='Xác nhận cập nhật giá dịch vụ')

d.h3('5.2.3.4 Mô tả chi tiết giao diện')
d.ui_table([
    ('Hệ số giá bán dịch vụ', 'Textbox', 'Enable', '0,01 – 999,99', 'Có', 'Lấy từ hệ thống',
     'Bắt buộc nhập, phải là số lớn hơn 0 và không vượt 999,99'),
    ('Định mức đàm phán giá (%)', 'Textbox', 'Enable', '0 – 99', 'Không', 'Lấy từ hệ thống',
     'Có thể để trống; nhập 0 khác với để trống'),
    ('Lưu', 'Button', 'Enable / Ẩn', '–', '–', 'Enable',
     'Kiểm tra hợp lệ rồi mở popup xác nhận; đổi nhãn thành “Đang lưu...” và bị vô hiệu hoá '
     'trong lúc ghi'),
    ('Popup xác nhận', 'Modal', 'Enable', '–', '–', 'Ẩn',
     'Tiêu đề “Xác nhận cập nhật giá dịch vụ”, nội dung nêu rõ số gói bảo dưỡng sẽ bị áp lại'),
    ('Đồng ý', 'Button', 'Enable', '–', '–', '–', 'Xác nhận ghi cấu hình và áp lại cho toàn bộ gói'),
    ('Hủy', 'Button', 'Enable', '–', '–', '–', 'Đóng popup, không ghi gì'),
    ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Nêu số gói đã áp, số cấp dịch vụ đã tính lại giá và danh sách gói bị bỏ qua'),
    ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     'Hiển thị khi ghi thất bại; dữ liệu được giữ nguyên như trước khi lưu'),
])

d.h3('5.2.3.5 Tiêu chí nghiệm thu')
d.bullets([
    'Bỏ trống Hệ số giá bán dịch vụ thì không lưu được và hiển thị lỗi “Bắt buộc phải nhập”.',
    'Nhập Hệ số bằng 0 hoặc số âm thì hiển thị lỗi “Phải lớn hơn 0”.',
    'Nhập Hệ số vượt 999,99 thì hiển thị lỗi “Tối đa 999,99”.',
    'Nhập Định mức đàm phán giá vượt 99 thì hiển thị lỗi “Tối đa 99”; nhập số âm thì hiển thị lỗi '
    '“Không được nhỏ hơn 0”.',
    'Nhập ký tự không phải số ở bất kỳ ô nào thì hiển thị lỗi “Phải là số”.',
    'Bấm Lưu luôn mở popup xác nhận, popup nêu đúng số gói bảo dưỡng sẽ bị áp lại.',
    'Bấm Hủy ở popup thì không có gói nào bị thay đổi.',
    'Bấm Đồng ý thì toàn bộ gói bảo dưỡng được áp hệ số mới, kể cả gói trước đó đã chỉnh riêng.',
    'Đổi hệ số thì giá gốc của các cấp dịch vụ được tính lại theo công thức đơn giá công × '
    'định mức công × hệ số.',
    'Giữ nguyên hệ số và chỉ đổi định mức đàm phán thì giá gốc của cấp dịch vụ KHÔNG bị tính lại.',
    'Gói chưa gắn công ty hoặc công ty chưa có đơn giá công thì giá của gói đó được giữ nguyên '
    '(không bị ghi về 0) và mã gói xuất hiện trong thông báo kết quả.',
    'Để trống Định mức đàm phán giá thì định mức của các gói giữ nguyên; nhập 0 thì các gói được '
    'đặt về 0.',
    'Lỗi xảy ra giữa chừng thì không có gói nào bị thay đổi một phần.',
    'Sau khi lưu, dòng cập nhật gần nhất hiển thị đúng thời điểm và người vừa thực hiện.',
    'Người dùng không có P1 gọi trực tiếp API cập nhật thì bị từ chối với lỗi 403.',
])

d.h3('5.2.3.6 Danh sách event và xử lý event')
d.event_table([
    ('Bấm Lưu', 'Click',
     'Before:\n– Kiểm tra quyền P1; không có quyền thì nút không hiển thị.\n'
     'During:\n'
     '– Hệ số giá bán dịch vụ trống → hiển thị “Bắt buộc phải nhập”\n'
     '– Hệ số hoặc Định mức không phải số → hiển thị “Phải là số”\n'
     '– Hệ số ≤ 0 → hiển thị “Phải lớn hơn 0”\n'
     '– Hệ số > 999,99 → hiển thị “Tối đa 999,99”\n'
     '– Định mức < 0 → hiển thị “Không được nhỏ hơn 0”\n'
     '– Định mức > 99 → hiển thị “Tối đa 99”\n'
     '– Nếu có lỗi validate → không mở popup xác nhận.\n'
     'After:\n– Mở popup “Xác nhận cập nhật giá dịch vụ” nêu rõ số gói bảo dưỡng sẽ bị áp lại.'),
    ('Bấm Đồng ý trong popup', 'Click',
     'Before:\n– Kiểm tra quyền P1.\n'
     '– Nếu không có quyền → hiển thị “Bạn không có quyền thực hiện chức năng này.” và dừng xử lý.\n'
     '– Vô hiệu hoá nút Lưu và đổi nhãn thành “Đang lưu...”.\n'
     'During:\n'
     '– Kiểm tra lại toàn bộ ràng buộc giá trị tại máy chủ; không đạt → trả lỗi và không ghi gì.\n'
     '– Gói thiếu công ty hoặc đơn giá công → bỏ qua phần tính lại giá của gói đó và ghi nhận '
     'để báo lại.\n'
     '– Lỗi phát sinh giữa chừng → huỷ toàn bộ thay đổi của lần lưu, không ghi một phần.\n'
     'After:\n– Ghi cấu hình mới kèm người cập nhật.\n'
     '– Áp hệ số và định mức đàm phán cho toàn bộ gói bảo dưỡng.\n'
     '– Nếu hệ số thay đổi thì tính lại giá gốc cho các cấp dịch vụ.\n'
     '– Hiển thị thông báo nêu số gói đã áp, số cấp dịch vụ đã tính lại giá và danh sách gói '
     'bị bỏ qua.\n'
     '– Mở lại nút Lưu và tải lại cấu hình vừa ghi.'),
    ('Bấm Hủy trong popup', 'Click', 'Đóng popup, không ghi cấu hình và không đụng tới gói nào.'),
])

# ================================================================ 6. BR
d.h1('6. Quy tắc nghiệp vụ (Business Rules)')

d.p('BR-01 — Chỉ có duy nhất một bản ghi cấu hình')
d.bullets([
    'Toàn hệ thống chỉ có một cấu hình giá dịch vụ dùng chung.',
    'Chưa có bản ghi nào thì lần lưu đầu tiên sẽ tạo mới, màn hình vẫn mở được với form trống '
    'và không báo lỗi.',
])

d.p('BR-02 — Ràng buộc giá trị nhập')
d.bullets([
    'Hệ số giá bán dịch vụ là bắt buộc, phải là số lớn hơn 0 và không vượt quá 999,99.',
    'Định mức đàm phán giá không bắt buộc, nếu nhập thì phải là số trong khoảng 0 đến 99.',
    'Nhập 0 khác với để trống: nhập 0 sẽ đặt định mức của các gói về 0, còn để trống thì giữ '
    'nguyên định mức hiện có của từng gói.',
    'Toàn bộ ràng buộc được kiểm tra lại tại máy chủ, không phụ thuộc giao diện.',
])

d.p('BR-03 — Ghi đè hàng loạt cho toàn bộ gói bảo dưỡng')
d.bullets([
    'Mỗi lần lưu sẽ áp hệ số và định mức đàm phán cho TOÀN BỘ gói bảo dưỡng.',
    'Gói đã được chỉnh riêng ở màn Danh mục gói bảo dưỡng cũng bị ghi đè, không có ngoại lệ.',
    'Hành vi này được giữ nguyên theo hệ thống ERP và là yêu cầu nghiệp vụ, không phải lỗi.',
    'Không có chức năng hoàn tác — cần sao lưu dữ liệu trước khi thao tác lần đầu.',
])

d.p('BR-04 — Điều kiện tính lại giá gốc của cấp dịch vụ')
d.bullets([
    'Giá gốc của cấp dịch vụ chỉ được tính lại khi hệ số giá bán dịch vụ thực sự thay đổi.',
    'Công thức: giá gốc = đơn giá công của công ty × định mức công của cấp dịch vụ × hệ số giá bán '
    'dịch vụ, làm tròn xuống.',
    'Chỉ đổi định mức đàm phán mà giữ nguyên hệ số thì giá gốc không bị đụng tới.',
])

d.p('BR-05 — Bỏ qua gói thiếu dữ liệu để tính giá')
d.bullets([
    'Gói bảo dưỡng chưa gắn công ty, hoặc công ty chưa có đơn giá công, thì phần tính lại giá của '
    'gói đó được bỏ qua và giá đang dùng được giữ nguyên.',
    'Mã của các gói bị bỏ qua phải được nêu trong thông báo kết quả để người dùng biết mà xử lý.',
    'Đây là khác biệt có chủ đích so với hệ thống ERP: ERP ghi thẳng giá về 0 trong trường hợp này, '
    'làm mất giá đang dùng.',
])

d.p('BR-06 — Toàn vẹn dữ liệu khi lưu')
d.bullets([
    'Việc ghi cấu hình và áp lại cho các gói phải là một thao tác trọn vẹn: lỗi giữa chừng thì '
    'toàn bộ thay đổi của lần lưu đó bị huỷ.',
    'Không được để dữ liệu ở trạng thái nửa vời — một phần gói đã áp giá mới, phần còn lại giữ giá cũ.',
])

d.p('BR-07 — Bắt buộc xác nhận trước khi ghi')
d.bullets([
    'Bấm Lưu không ghi ngay mà phải mở popup xác nhận.',
    'Popup phải nêu rõ số gói bảo dưỡng sẽ bị áp lại và việc ghi đè giá trị đã chỉnh riêng.',
    'Đây là khác biệt có chủ đích so với màn ERP cũ vốn bấm Lưu là chạy ngay, không cảnh báo.',
])

d.p('BR-08 — Quyền dùng chung giữa hai hệ thống')
d.bullets([
    'Quyền của màn hình được đối chiếu theo TÊN quyền, không phân biệt quyền đó thuộc hệ thống '
    'ERP hay HRM.',
    'Nhờ vậy người dùng đã được cấp quyền tương ứng ở ERP vẫn dùng được màn hình HRM mà không '
    'phải cấp lại quyền.',
])

d.p('Chức năng liên quan: FR-01 … FR-03.')

d.save()
