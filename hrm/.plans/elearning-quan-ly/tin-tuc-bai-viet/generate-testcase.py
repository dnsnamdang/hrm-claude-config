# -*- coding: utf-8 -*-
"""Testcase Tin tức - Bài viết (quản lý) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Màn 'Tin tức - Bài viết': admin CRUD bài viết tin tức/thông báo cho portal elearning; đổi trạng thái (ẩn/hiện), đánh dấu nổi bật. Học viên đọc bài đã đăng ở /tin-tuc."),
    ("2. Đối tượng được tính / hiển thị",
     "► published → UI 'Hoạt động'; draft → 'Khóa'.\n► is_featured=1 → nổi bật (sao vàng) → hiện ở sidebar 'Tin nổi bật'."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Không có quyền 'Quản lý tin tức elearning' → trang lỗi 403.\n► Chỉ bài 'Hoạt động' hiển thị ở portal (bài Khóa/draft ẩn)."),
    ("4. Bộ lọc thời gian áp dụng cho", "Không áp dụng."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Bài viết N-1 Danh mục. Bài có Lượt xem, Ngày đăng."),
    ("6. Quy tắc cộng dồn / deduplicate", "Slug unique tự sinh. published_at chỉ set lần đầu khi publish."),
    ("7. Phân quyền cấp", "• Quản lý tin tức elearning — quyền DUY NHẤT."),
    ("8. Cách tính các ô thống kê", "Cột 'Lượt xem' = view_count (tăng ở portal)."),
    ("9. Ghi chú đọc bảng",
     "LƯU Ý nhãn: UI dùng 'Hoạt động'/'Khóa' (BE lưu published/draft). Toggle trạng thái/nổi bật thao tác 1 chạm. Bài viết XÓA không chặn (kể cả đang đăng)."),
]

ROLE_TCS = [
    ("01", "Vào màn khi CÓ quyền", "P0",
     "Tài khoản có quyền 'Quản lý tin tức elearning'",
     "1. Vào menu Đào tạo > Tin tức - Bài viết", "Tài khoản: có quyền",
     "- Hiển thị bảng 'Danh sách bài viết' + nút Tạo mới", "Quyền: Quản lý tin tức elearning"),
    ("02", "Vào màn khi KHÔNG quyền", "P0",
     "Tài khoản không quyền", "1. Mở màn Tin tức - Bài viết", "Tài khoản: không quyền",
     "- Trang lỗi 403", "—"),
]

SECTIONS = [
    ("I", "HIỂN THỊ & LỌC", [
        ("001", "Xem danh sách bài viết", "P0", "Có ≥10 bài",
         "1. Vào 'Tin tức - Bài viết'", "—",
         "- Cột: STT, Tiêu đề, Danh mục, Trạng thái, Nổi bật, Ngày đăng, Lượt xem, Hành động", "—"),
        ("002", "Tìm theo tiêu đề", "P0", "Có bài 'Thông báo nghỉ lễ'",
         "1. Gõ 'nghỉ lễ' vào 'Tìm theo tiêu đề'", "Từ khóa: nghỉ lễ",
         "- Chỉ còn bài khớp", "—"),
        ("003", "Lọc theo Trạng thái = Hoạt động", "P1", "Có bài Hoạt động/Khóa",
         "1. 'Trạng thái' chọn 'Hoạt động'", "—",
         "- Chỉ còn bài đã đăng (Hoạt động)", "—"),
        ("004", "Lọc theo Danh mục", "P1", "Có bài nhiều danh mục",
         "1. 'Danh mục' chọn 1 danh mục", "—",
         "- Chỉ còn bài thuộc danh mục đó", "—"),
    ]),
    ("II", "THÊM / SỬA", [
        ("001", "Tạo bài viết hợp lệ", "P0", "Có quyền, có danh mục",
         "1. Bấm 'Tạo mới'\n2. Tiêu đề='Thông báo A'\n3. Chọn Danh mục\n4. Trạng thái='Hoạt động'\n5. Soạn Nội dung\n6. Bấm 'Lưu'", "status=Hoạt động",
         "- Toast 'Thêm mới thành công'; bài mới xuất hiện; hiện trên portal /tin-tuc", "BR-01,BR-02,BR-03"),
        ("002", "Thiếu tiêu đề", "P0", "Modal tạo",
         "1. Để trống Tiêu đề\n2. Bấm 'Lưu'", "—",
         "- Lỗi 'Bắt buộc nhập' tại Tiêu đề", "—"),
        ("003", "Thiếu nội dung", "P0", "Modal tạo",
         "1. Để trống Nội dung\n2. Bấm 'Lưu'", "—",
         "- Lỗi 'Bắt buộc nhập nội dung'", "BR-01"),
        ("004", "Upload ảnh đại diện", "P2", "Modal tạo, có file ảnh",
         "1. Bấm 'Chọn ảnh đại diện' → chọn ảnh\n2. Bấm 'Lưu'", "ảnh",
         "- Ảnh upload thành công, hiển thị ở thẻ tin", "—"),
        ("005", "Sửa bài viết", "P1", "Có bài viết",
         "1. Bấm 'Sửa'\n2. Đổi Tiêu đề\n3. Bấm 'Lưu'", "—",
         "- Toast 'Cập nhật thành công'", "—"),
    ]),
    ("III", "TRẠNG THÁI / NỔI BẬT / XÓA", [
        ("001", "Đổi trạng thái (khóa/mở)", "P0", "Bài 'Hoạt động'",
         "1. Bấm nút khóa dòng đó (tooltip 'Khóa (ẩn) bài viết')", "—",
         "- Trạng thái chuyển 'Khóa' (ẩn khỏi portal); toast 'Thao tác thành công'", "UC-03"),
        ("002", "Đánh dấu nổi bật", "P1", "Bài chưa nổi bật",
         "1. Bấm nút sao (tooltip 'Đánh dấu nổi bật')", "—",
         "- Sao chuyển vàng đầy; bài hiện ở 'Tin nổi bật' trên portal", "BR-05"),
        ("003", "Xóa bài viết", "P0", "Bài bất kỳ (kể cả đang đăng)",
         "1. Bấm 'Xoá'\n2. Popup 'Xác nhận xóa': Bạn có chắc muốn xóa bài viết \"…\"? → 'Xóa'", "—",
         "- Toast 'Xóa thành công'; bài biến mất (không chặn xóa)", "BR-04"),
    ]),
    ("IV", "LUỒNG XUYÊN SUỐT (E2E)", [
        ("001", "Đăng bài → nổi bật → kiểm tra portal", "P0", "Có quyền, có danh mục",
         "1. Tạo bài Trạng thái Hoạt động\n2. Đánh dấu nổi bật\n3. Mở portal /tin-tuc", "—",
         "- Bài hiện trên portal + ở 'Tin nổi bật'", "—"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-quan-ly\tin-tuc-bai-viet\testcase.xlsx",
    sheet_name="TinTucBaiViet", feature_name="Tin tức - Bài viết (quản lý)", module_name="Tin tức - Bài viết",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=ROLE_TCS,
)
