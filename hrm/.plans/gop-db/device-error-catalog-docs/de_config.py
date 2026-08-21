# -*- coding: utf-8 -*-
"""Cau hinh man 'Danh muc cong viec, loi thiet bi' (/customer-care/device-errors).

Doc code 18/08/2026:
  BE  Modules/CustomerCare/Routes/api.php (118-142) — 1 quyen duy nhat
      Modules/CustomerCare/Http/Requests/DeviceErrorRequest.php
      Modules/CustomerCare/Entities/DeviceError/DeviceError.php (TYPES, STATUSES, mau in 279/280)
  FE  pages/customer-care/device-errors/{index.vue, create.vue, print.vue, _id/*}
      components/{DeviceErrorFormComponent.vue, CostSearchModal.vue}
  Anh that: de_shots/ (cong dev hrm-crm.eteksofts.com, 18/08/2026)
"""

HOST = 'http://hrm-crm.eteksofts.com'
TEN = 'Danh mục công việc, lỗi thiết bị'
DOI_TUONG = 'công việc / lỗi thiết bị'
ROUTE = '/customer-care/device-errors'
QUYEN = 'Quản lý danh mục công việc - lỗi thiết bị'

LOAI = ['Lỗi đã xác định', 'Lỗi chưa xác định', 'Lắp đặt bàn giao',
        'Thiết kế nền móng', 'Tư vấn, khảo sát', 'Giám sát thi công']

THUAT_NGU = [
    ('Công việc / lỗi thiết bị',
     'Một hạng mục công việc sửa chữa hoặc một tình trạng lỗi của thiết bị, dùng làm cơ sở lập '
     'báo giá và phiếu sửa chữa.'),
    ('Loại công việc / lỗi',
     'Sáu nhóm phân loại: %s.' % ', '.join(LOAI)),
    ('Định mức công',
     'Số công chuẩn để hoàn thành hạng mục này, là căn cứ tính Công kỹ thuật.'),
    ('Công kỹ thuật',
     'Giá trị công tính tự động từ Định mức công. Để trống thì hệ thống tự tính.'),
    ('Hệ số giá bán dịch vụ',
     'Hệ số nhân dùng khi tính giá bán. Để trống thì lấy theo cấu hình của công ty.'),
    ('Hệ số công nghệ',
     'Hệ số phản ánh mức độ phức tạp công nghệ, bắt buộc lớn hơn 0.'),
    ('Định mức giảm giá (%)', 'Tỷ lệ giảm giá tối đa được phép áp cho hạng mục này.'),
    ('VAT (%)', 'Thuế suất giá trị gia tăng áp cho hạng mục, tối đa 100.'),
    ('Đơn giá bán', 'Giá bán của hạng mục. Để trống thì hệ thống tự tính theo công thức.'),
    ('Áp dụng cho thiết bị',
     'Danh sách hàng hóa / thiết bị mà hạng mục này áp dụng. Bắt buộc khai ít nhất một.'),
    ('Vật tư thay thế', 'Danh sách hàng hóa dùng để thay thế khi thực hiện hạng mục.'),
    ('Dịch vụ sửa chữa kèm theo',
     'Các dịch vụ đi kèm, mỗi dòng phải khai đủ Giá vốn và Giá dịch vụ.'),
    ('Trạng thái Hoạt động', 'Hạng mục còn chọn được khi lập báo giá và phiếu sửa chữa mới.'),
    ('Trạng thái Khóa',
     'Hạng mục không còn chọn được ở nghiệp vụ mới nhưng vẫn nằm trong danh mục.'),
]

COT = [
    ('STT', 'Số thứ tự, chạy liên tục qua các trang. Luôn hiển thị.'),
    ('Tên công việc / Tình trạng lỗi', 'Tên đầy đủ của hạng mục. Luôn hiển thị, sắp xếp được.'),
    ('Loại công việc / lỗi thiết bị', 'Một trong sáu loại. Mặc định ẩn.'),
    ('Áp dụng cho thiết bị', 'Danh sách thiết bị áp dụng. Mặc định ẩn.'),
    ('Định mức công', 'Số công chuẩn. Mặc định ẩn.'),
    ('Công kỹ thuật', 'Giá trị công tính được. Mặc định ẩn.'),
    ('Đơn giá bán', 'Giá bán của hạng mục. Mặc định ẩn, sắp xếp được.'),
    ('Người cập nhật', 'Người sửa gần nhất. Mặc định ẩn.'),
    ('Ngày cập nhật', 'Thời điểm sửa gần nhất. Mặc định ẩn, sắp xếp được.'),
    ('Người tạo', 'Người đã thêm bản ghi.'),
    ('Ngày tạo', 'Thời điểm thêm, sắp xếp được.'),
    ('Trạng thái', 'Hoạt động hoặc Khóa.'),
    ('Hành động', 'Sửa, Xóa, Khóa/Mở khóa, In và Lịch sử — hai nút đầu hiện thẳng, '
                  'còn lại nằm trong nút ba chấm.'),
]

LOC = [
    ('Ô tìm kiếm nhanh', 'Textbox', '0–255 ký tự', 'Trống',
     'Tìm theo tên công việc / tình trạng lỗi.'),
    ('Loại', 'Dropdown', 'Sáu loại', 'Trống', 'Lọc theo nhóm phân loại của hạng mục.'),
    ('Trạng thái', 'Dropdown', 'Hoạt động / Khóa', 'Trống',
     'Bỏ trống thì hiện cả hai trạng thái.'),
    ('Nhóm hàng hóa', 'Dropdown', 'Danh sách nhóm', 'Trống',
     'Lọc theo nhóm của thiết bị được áp dụng.'),
    ('Tên hoặc mã hàng hóa', 'Textbox', '0–255 ký tự', 'Trống',
     'Tìm hạng mục có áp dụng cho hàng hóa khớp tên hoặc mã đã nhập.'),
    ('Người tạo', 'Dropdown', 'Danh sách nhân viên', 'Trống', 'Lọc theo người đã thêm bản ghi.'),
    ('Người sửa', 'Dropdown', 'Danh sách nhân viên', 'Trống', 'Lọc theo người sửa gần nhất.'),
    ('Đơn giá bán: từ – đến', 'Number', '≥ 0', 'Trống',
     'Lọc theo khoảng đơn giá bán. Nhập một đầu hoặc cả hai đầu.'),
    ('Định mức công', 'Number', '≥ 0', 'Trống', 'Lọc theo số công chuẩn.'),
]

TRUONG = [
    ('Loại công việc / lỗi', 'Dropdown', 'Sáu loại', 'Có', 'Trống',
     'Quyết định nhóm phân loại. Bỏ trống thì bị chặn khi lưu.'),
    ('Tên công việc / tình trạng lỗi', 'Textbox', '0–255 ký tự', 'Có', 'Trống',
     'KHÔNG được trùng tên TRONG CÙNG MỘT LOẠI. Hai loại khác nhau được phép trùng tên. '
     'Bỏ trống báo “Bắt buộc phải nhập”.'),
    ('Định mức công', 'Number', '≥ 0', 'Có', 'Trống',
     'Là căn cứ tính Công kỹ thuật.'),
    ('Hệ số giá bán dịch vụ', 'Number', '≥ 0', 'Không', 'Trống',
     'Để trống thì lấy theo cấu hình của công ty.'),
    ('Định mức giảm giá (%)', 'Number', '0 – 100', 'Có', 'Trống',
     'Tỷ lệ giảm giá tối đa được phép.'),
    ('VAT (%)', 'Number', '0 – 100', 'Có', 'Trống',
     'Vượt 100 báo “Tối đa 100”; nhập chữ báo “Phải là số”.'),
    ('Công kỹ thuật', 'Number', '≥ 0', 'Không', 'Trống',
     'Để trống thì hệ thống tự tính theo Định mức công.'),
    ('Đơn giá công kỹ thuật', 'Number', '≥ 0', 'Không', 'Trống',
     'Để trống thì lấy theo cấu hình của công ty.'),
    ('Đơn giá bán', 'Number', '≥ 0', 'Không', 'Trống',
     'Để trống thì hệ thống tự tính. Nhập số âm báo “Không được nhỏ hơn 0”.'),
    ('Hệ số công nghệ', 'Number', '> 0', 'Có', 'Trống',
     'Nhập 0 báo “Nhập hệ số lớn hơn 0”.'),
    ('Ghi chú', 'Textarea', '–', 'Không', 'Trống', 'Ghi chú tự do.'),
    ('Áp dụng cho thiết bị', 'Table/Grid', 'Danh sách hàng hóa', 'Có', 'Trống',
     'Bắt buộc chọn ít nhất một thiết bị, chọn qua cửa sổ tìm kiếm hàng hóa.'),
    ('Vật tư thay thế', 'Table/Grid', 'Danh sách hàng hóa', 'Không', 'Trống',
     'Khai thêm nếu hạng mục có vật tư thay thế.'),
    ('Dịch vụ sửa chữa kèm theo', 'Table/Grid', 'Danh sách dịch vụ', 'Không', 'Trống',
     'Mỗi dòng đã thêm thì BẮT BUỘC nhập đủ Giá vốn và Giá dịch vụ.'),
]

SHOTS = dict(
    danhsach='de_01_danhsach.png',
    boloc='de_02_boloc.png',
    taomoi='de_03_taomoi.png',
    validate='de_04_validate.png',
    menu='de_05_menu_hanhdong.png',
    khoa='de_06_xacnhan_khoa.png',
    lichsu='de_07_lichsu.png',
    cot='de_08_cauhinh_cot.png',
)
