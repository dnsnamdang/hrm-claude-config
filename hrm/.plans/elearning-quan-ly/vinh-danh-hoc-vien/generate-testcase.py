# -*- coding: utf-8 -*-
"""Testcase Vinh danh học viên (quản lý) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Màn quản trị cấu hình khối 'Vinh danh học viên' (bảng vàng) trên trang chủ elearning. Admin định nghĩa danh hiệu (tiêu chí + kỳ tính + lấy top N), hệ thống tự tính top học viên. Có danh hiệu composite 'Gương mặt tiêu biểu'."),
    ("2. Đối tượng được tính / hiển thị",
     "► Danh hiệu is_active=1 'Đang bật', is_active=0 'Đã tắt'.\n► Tiêu chí: 7 loại (khoá/lộ trình/chứng chỉ/bài học hoàn thành, đúng hạn, điểm thi TB, Gương mặt tiêu biểu).\n► Composite: ẩn Kỳ tính, hiện Số tiêu chí tối thiểu."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Không có quyền 'Quản lý vinh danh học viên' → trang lỗi 403.\n► Chỉ 1 danh hiệu composite được tồn tại.\n► Khối setting is_enabled=0 → ẩn bảng vàng trên trang chủ elearning."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Không có bộ lọc ở màn. 'Kỳ tính' là thuộc tính của từng danh hiệu (30 ngày/tháng/quý/năm/toàn thời gian)."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bảng phẳng danh hiệu + 1 dòng cấu hình chung (is_enabled). Thứ tự danh hiệu = thứ tự hiển thị + ưu tiên."),
    ("6. Quy tắc cộng dồn / deduplicate",
     "Tên danh hiệu unique. Thứ tự ưu tiên: 1 người lọt nhiều bảng chỉ hiện 1 thẻ (danh hiệu trên cùng)."),
    ("7. Phân quyền cấp",
     "• Quản lý vinh danh học viên — quyền DUY NHẤT. Không phân quyền theo công ty/phòng ban."),
    ("8. Cách tính các ô thống kê",
     "Không tính tay. Hệ thống tự xếp top theo metric + period, lấy top_n. Composite đếm ai lọt top của ≥ min_criteria bảng khác."),
    ("9. Ghi chú đọc bảng",
     "Nút 'Lưu' cấu hình chung chỉ bấm được khi công tắc đổi. Sửa danh hiệu không đụng thứ tự (thứ tự quản lý riêng qua 'Sắp xếp thứ tự')."),
]

ROLE_TCS = [
    ("01", "Vào màn khi CÓ quyền", "P0",
     "Tài khoản có quyền 'Quản lý vinh danh học viên'",
     "1. Vào menu Đào tạo > Vinh danh học viên", "Tài khoản: có quyền",
     "- Hiển thị khối cấu hình chung + bảng 'Danh sách danh hiệu' + nút Thêm mới/Sắp xếp thứ tự", "Quyền: Quản lý vinh danh học viên"),
    ("02", "Vào màn khi KHÔNG quyền", "P0",
     "Tài khoản không có quyền", "1. Mở màn Vinh danh học viên", "Tài khoản: không quyền",
     "- Hiển thị trang lỗi 403 (không thấy dữ liệu)", "FE chặn theo quyền"),
]

SECTIONS = [
    ("I", "CẤU HÌNH CHUNG", [
        ("001", "Bật/tắt khối vinh danh", "P0", "Công tắc đang 'Đang hiển thị'",
         "1. Gạt công tắc sang 'Đang ẩn'\n2. Bấm 'Lưu'", "—",
         "- Toast 'Lưu thành công'; khối vinh danh ẩn trên trang chủ elearning", "UC-01"),
        ("002", "Nút Lưu vô hiệu khi chưa đổi", "P2", "Vừa vào màn",
         "1. Chưa gạt công tắc\n2. Quan sát nút 'Lưu'", "—",
         "- Nút 'Lưu' bị vô hiệu (chỉ bật khi công tắc đổi)", "—"),
    ]),
    ("II", "THÊM / SỬA DANH HIỆU", [
        ("001", "Thêm danh hiệu thường hợp lệ", "P0", "Chưa có danh hiệu 'Top học tập tháng'",
         "1. Bấm 'Thêm mới'\n2. Tên='Top học tập tháng'\n3. Tiêu chí='Số khoá học hoàn thành'\n4. Kỳ tính='Tháng hiện tại'\n5. Lấy top=3\n6. Bấm 'Lưu'", "top=3",
         "- Toast 'Thêm mới thành công'; danh hiệu xuất hiện, trạng thái 'Đang bật'", "BR-01,BR-02,BR-03"),
        ("002", "Thiếu tên", "P0", "Modal thêm",
         "1. Để trống 'Tên danh hiệu'\n2. Bấm 'Lưu'", "—",
         "- Lỗi 'Bắt buộc nhập' tại ô Tên", "—"),
        ("003", "Tên trùng", "P0", "Đã có 'Top học tập tháng'",
         "1. Thêm mới, nhập tên trùng\n2. Bấm 'Lưu'", "—",
         "- Lỗi 'Tên danh hiệu đã tồn tại'", "BR-01"),
        ("004", "Không composite thiếu Kỳ tính", "P0", "Modal, tiêu chí thường",
         "1. Không chọn 'Kỳ tính'\n2. Bấm 'Lưu'", "—",
         "- Lỗi 'Chưa chọn kỳ tính'", "BR-03"),
        ("005", "Lấy top ngoài 1-20", "P1", "Modal thêm",
         "1. Nhập 'Lấy top'=0 (hoặc 25)\n2. Bấm 'Lưu'", "top=0",
         "- Lỗi 'Phải lấy ít nhất 1 người' (hoặc 'Tối đa 20 người')", "BR-02"),
        ("006", "Sửa danh hiệu", "P1", "Có danh hiệu đang bật",
         "1. Bấm 'Sửa' 1 dòng\n2. Đổi 'Lấy top'=5\n3. Bấm 'Lưu'", "top=5",
         "- Toast 'Cập nhật thành công'; thứ tự KHÔNG đổi", "BR-06"),
    ]),
    ("III", "DANH HIỆU COMPOSITE", [
        ("001", "Ẩn/hiện trường theo composite", "P1", "Modal thêm",
         "1. Chọn Tiêu chí='Gương mặt tiêu biểu'", "—",
         "- Ẩn 'Kỳ tính'; hiện 'Số tiêu chí tối thiểu' + ghi chú", "BR-04"),
        ("002", "Composite thiếu số tiêu chí", "P0", "Tiêu chí=Gương mặt tiêu biểu",
         "1. Để trống 'Số tiêu chí tối thiểu'\n2. Bấm 'Lưu'", "—",
         "- Lỗi 'Bắt buộc nhập với danh hiệu Gương mặt tiêu biểu'", "BR-04"),
        ("003", "Chỉ 1 composite", "P0", "Đã có 1 danh hiệu composite",
         "1. Thêm danh hiệu composite thứ 2\n2. Bấm 'Lưu'", "—",
         "- Lỗi 'Đã có danh hiệu tổng hợp. Mỗi hệ thống chỉ dùng 1 danh hiệu Gương mặt tiêu biểu.'", "BR-05"),
        ("004", "Composite hợp lệ", "P1", "Chưa có composite nào",
         "1. Tiêu chí='Gương mặt tiêu biểu', Số tiêu chí tối thiểu=2, Lấy top=5\n2. Bấm 'Lưu'", "min=2",
         "- Toast 'Thêm mới thành công'", "BR-04"),
    ]),
    ("IV", "BẬT/TẮT · XÓA · SẮP XẾP", [
        ("001", "Tắt danh hiệu", "P0", "Danh hiệu 'Đang bật'",
         "1. Bấm nút Tắt (tooltip 'Tắt danh hiệu')", "—",
         "- Trạng thái chuyển 'Đã tắt'", "—"),
        ("002", "Xóa danh hiệu", "P0", "Danh hiệu bất kỳ",
         "1. Bấm 'Xóa'\n2. Xác nhận 'Xóa danh hiệu \"…\"?'", "—",
         "- Toast 'Xóa thành công'; danh hiệu biến mất", "BR-08"),
        ("003", "Sắp xếp thứ tự kéo thả", "P1", "Có ≥2 danh hiệu",
         "1. Bấm 'Sắp xếp thứ tự'\n2. Kéo đổi vị trí\n3. Bấm 'Lưu'", "—",
         "- Toast 'Lưu thành công'; thứ tự trên bảng vàng + ưu tiên cập nhật", "BR-07"),
    ]),
    ("V", "LUỒNG XUYÊN SUỐT (E2E)", [
        ("001", "Cấu hình bảng vàng đầy đủ", "P0", "Có quyền",
         "1. Thêm 2 danh hiệu thường + 1 composite\n2. Sắp xếp thứ tự\n3. Bật khối vinh danh (Lưu cấu hình chung)", "—",
         "- Các danh hiệu tạo thành công; thứ tự đúng; trang chủ elearning hiện bảng vàng", "—"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-quan-ly\vinh-danh-hoc-vien\testcase.xlsx",
    sheet_name="VinhDanhHocVien", feature_name="Vinh danh học viên (quản lý)", module_name="Vinh danh",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=ROLE_TCS,
)
