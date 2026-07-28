# -*- coding: utf-8 -*-
"""Testcase Tin tức - Danh mục (quản lý) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Màn 'Tin tức - Danh mục': quản lý danh mục phân loại bài viết tin tức. CRUD, bật/khóa, sắp xếp thứ tự (kéo–thả). Danh mục dùng lọc ở portal và dropdown khi tạo bài."),
    ("2. Đối tượng được tính / hiển thị",
     "► Danh mục is_active 'Hoạt động'/'Khóa', kèm 'Số bài'.\n► Thứ tự hiển thị sắp bằng kéo–thả (sort_order=0 xuống cuối)."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Không có quyền 'Quản lý tin tức elearning' → trang lỗi 403.\n► Danh mục CÒN BÀI VIẾT → chặn khóa + chặn xóa."),
    ("4. Bộ lọc thời gian áp dụng cho", "Không áp dụng (màn không có bộ lọc)."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Danh mục 1-N bài viết. Có 'Số bài' (articles_count)."),
    ("6. Quy tắc cộng dồn / deduplicate", "Tên unique, slug tự sinh. sort_order gán lại 1,2,3 khi sắp xếp."),
    ("7. Phân quyền cấp", "• Quản lý tin tức elearning — quyền DUY NHẤT."),
    ("8. Cách tính các ô thống kê", "Cột 'Số bài' = số bài viết thuộc danh mục."),
    ("9. Ghi chú đọc bảng", "Chặn kép: danh mục còn bài thì không khóa và không xóa (cả FE lẫn BE). Không có màn chi tiết — sửa lấy dữ liệu từ dòng bảng."),
]

ROLE_TCS = [
    ("01", "Vào màn khi CÓ quyền", "P0",
     "Tài khoản có quyền 'Quản lý tin tức elearning'",
     "1. Vào menu Đào tạo > Tin tức - Danh mục", "Tài khoản: có quyền",
     "- Hiển thị bảng 'Danh sách danh mục tin tức' + nút Tạo mới/Sắp xếp", "Quyền: Quản lý tin tức elearning"),
    ("02", "Vào màn khi KHÔNG quyền", "P0",
     "Tài khoản không quyền", "1. Mở màn Tin tức - Danh mục", "Tài khoản: không quyền",
     "- Trang lỗi 403", "—"),
]

SECTIONS = [
    ("I", "HIỂN THỊ", [
        ("001", "Xem danh sách danh mục", "P0", "Có ≥3 danh mục",
         "1. Vào 'Tin tức - Danh mục'", "—",
         "- Cột: STT, Tên danh mục, Slug, Số bài, Trạng thái, Hành động", "—"),
        ("002", "Danh sách rỗng", "P2", "Chưa có danh mục",
         "1. Vào màn khi chưa có danh mục", "—",
         "- 'Chưa có danh mục nào.'", "—"),
    ]),
    ("II", "THÊM / SỬA", [
        ("001", "Tạo danh mục hợp lệ", "P0", "Chưa có 'Thông báo'",
         "1. Bấm 'Tạo mới'\n2. Tên danh mục='Thông báo'\n3. Bấm 'Lưu'", "—",
         "- Toast 'Thêm mới thành công'; danh mục xuất hiện, trạng thái 'Hoạt động'", "BR-01,BR-05"),
        ("002", "Thiếu tên", "P0", "Modal tạo",
         "1. Để trống Tên danh mục\n2. Bấm 'Lưu'", "—",
         "- Lỗi 'Bắt buộc nhập'", "BR-01"),
        ("003", "Tên danh mục trùng", "P1", "Đã có 'Thông báo'",
         "1. Tạo mới, nhập 'Thông báo'\n2. Bấm 'Lưu'", "—",
         "- Lỗi 'Tên danh mục đã tồn tại'", "BR-01"),
        ("004", "Sửa tên danh mục", "P1", "Có danh mục",
         "1. Bấm 'Sửa'\n2. Đổi tên\n3. Bấm 'Lưu'", "—",
         "- Toast 'Cập nhật thành công'", "—"),
    ]),
    ("III", "KHÓA / XÓA (RÀNG BUỘC CÒN BÀI)", [
        ("001", "Xóa danh mục còn bài — bị chặn", "P0", "Danh mục có Số bài > 0",
         "1. Bấm 'Xoá' danh mục đó\n2. Xác nhận", "—",
         "- Bị chặn, toast 'Danh mục còn bài viết, không thể xoá'", "BR-02"),
        ("002", "Khóa danh mục còn bài — bị chặn", "P1", "Danh mục Hoạt động có bài",
         "1. Quan sát nút khóa", "—",
         "- Nút khóa vô hiệu (tooltip 'Không thể khóa danh mục đang có bài viết')", "BR-03"),
        ("003", "Xóa danh mục rỗng", "P1", "Danh mục Số bài = 0",
         "1. Bấm 'Xoá'\n2. Popup: Bạn có chắc muốn xóa danh mục \"…\"? → 'Xóa'", "—",
         "- Toast 'Xóa thành công'", "—"),
        ("004", "Khóa danh mục rỗng", "P2", "Danh mục Số bài = 0",
         "1. Bấm nút khóa\n2. Xác nhận", "—",
         "- Chuyển 'Khóa'; toast 'Thao tác thành công'", "—"),
    ]),
    ("IV", "SẮP XẾP", [
        ("001", "Sắp xếp danh mục kéo thả", "P1", "Có ≥2 danh mục",
         "1. Bấm 'Sắp xếp'\n2. Kéo đổi vị trí trong 'Sắp xếp danh mục tin tức'\n3. Bấm 'Lưu'", "—",
         "- Toast 'Lưu thành công'; thứ tự hiển thị (pill ở portal) cập nhật", "BR-04"),
    ]),
    ("V", "LUỒNG XUYÊN SUỐT (E2E)", [
        ("001", "Tạo → gán bài → thử xóa (chặn) → sắp xếp", "P0", "Có quyền",
         "1. Tạo danh mục 'Sự kiện'\n2. (Sang màn Bài viết) tạo 1 bài thuộc 'Sự kiện'\n3. Quay lại thử Xóa 'Sự kiện'\n4. Sắp xếp danh mục", "—",
         "- B3: bị chặn 'Danh mục còn bài viết, không thể xoá'\n- B4: thứ tự cập nhật", "—"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-quan-ly\tin-tuc-danh-muc\testcase.xlsx",
    sheet_name="TinTucDanhMuc", feature_name="Tin tức - Danh mục (quản lý)", module_name="Tin tức - Danh mục",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=ROLE_TCS,
)
