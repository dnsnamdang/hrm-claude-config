# -*- coding: utf-8 -*-
"""Testcase Danh sách lộ trình (elearning) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Màn danh sách lộ trình học tập: tìm/lọc/sắp xếp/phân trang lộ trình và mở chi tiết. Hiển thị PathCard, mặc định 8 mục/trang."),
    ("2. Đối tượng được tính / hiển thị",
     "► PathCard: pill 'Lộ trình học', 'Bắt buộc', '{n} khoá học', '{n} học viên'.\n► Đã ghi danh: thanh 'Tiến độ / {n}%'; chưa: 'Bạn chưa tham gia lộ trình này'."),
    ("3. Đối tượng bị ẩn / không tính", "Không có kết quả → EmptyState."),
    ("4. Bộ lọc thời gian áp dụng cho", "Không áp dụng."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Breadcrumb + pill → FilterSidebar + ListTopbar + lưới PathCard + Pagination."),
    ("6. Quy tắc cộng dồn / deduplicate", "Bộ lọc lưu URL; reload giữ nguyên."),
    ("7. Phân quyền cấp", "Public."),
    ("8. Cách tính các ô thống kê", "ListTopbar '{total} lộ trình • Trang p/tp'. Mặc định 8/trang (8/12/16), sort 'Phổ biến nhất'."),
    ("9. Ghi chú đọc bảng", "Sort riêng: Phổ biến nhất / Mới nhất / Ít khoá nhất / Nhiều khoá nhất."),
]

SECTIONS = [
    ("I", "HIỂN THỊ & PHÂN TRANG", [
        ("001", "Xem danh sách lộ trình", "P0", "Có > 8 lộ trình",
         "1. Mở /lo-trinh-hoc-tap", "—",
         "- Lưới PathCard; ListTopbar '{total} lộ trình • Trang 1 / {tp}'", "—"),
        ("002", "Đổi số mục/trang", "P2", "Ở danh sách",
         "1. Chọn '16 / trang'", "—",
         "- Hiển thị 16/trang, về trang 1", "BR-03"),
    ]),
    ("II", "TÌM & LỌC", [
        ("001", "Tìm theo tên lộ trình", "P0", "Có lộ trình 'An toàn'",
         "1. Gõ 'An toàn' vào 'Nhập tên lộ trình...'", "Từ khóa: An toàn",
         "- Chỉ còn lộ trình khớp; chip 'Từ khoá: An toàn'", "—"),
        ("002", "Lọc theo Loại đào tạo", "P1", "Có lộ trình nhiều loại",
         "1. Tick 1 loại đào tạo", "—",
         "- Lọc theo loại", "BR-01"),
        ("003", "Lọc theo Kỹ năng", "P1", "Có lộ trình nhiều kỹ năng",
         "1. Tick 1 kỹ năng", "—",
         "- Lọc theo kỹ năng", "—"),
        ("004", "Lọc Trạng thái = Bắt buộc", "P1", "Có lộ trình bắt buộc/tự chọn",
         "1. Tick 'Bắt buộc'", "Trạng thái: Bắt buộc",
         "- Chỉ còn lộ trình 'Bắt buộc'", "—"),
    ]),
    ("III", "SẮP XẾP & RESET", [
        ("001", "Sắp xếp Nhiều khoá nhất", "P1", "Ở danh sách",
         "1. 'Sắp xếp' chọn 'Nhiều khoá nhất'", "—",
         "- Sắp theo số khóa giảm dần", "BR-02"),
        ("002", "Reset bộ lọc", "P1", "Đang áp lọc",
         "1. Bấm 'Xoá tất cả'/'Reset'", "—",
         "- Về danh sách đầy đủ", "—"),
        ("003", "Danh sách rỗng", "P1", "Lọc không ra kết quả",
         "1. Lọc điều kiện không có lộ trình", "—",
         "- EmptyState + nút 'Reset bộ lọc'", "—"),
    ]),
    ("IV", "MỞ CHI TIẾT", [
        ("001", "Click thẻ lộ trình", "P0", "Có kết quả",
         "1. Click 1 PathCard (hoặc 'Xem chi tiết')", "—",
         "- Mở chi tiết lộ trình (/lo-trinh/:slug)", "—"),
        ("002", "Thẻ đã ghi danh có tiến độ", "P2", "Đã ghi danh lộ trình",
         "1. Quan sát thẻ", "—",
         "- Hiện thanh 'Tiến độ / {n}%' + nút 'Tiếp tục'", "—"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-hoc-vien\danh-sach-lo-trinh\testcase.xlsx",
    sheet_name="DanhSachLoTrinh", feature_name="Danh sách lộ trình", module_name="DS lộ trình",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=None,
)
