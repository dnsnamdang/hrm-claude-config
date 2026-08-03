# -*- coding: utf-8 -*-
"""Testcase Tin tức (elearning học viên) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Học viên đọc tin tức/thông báo đã đăng: danh sách (tìm kiếm + lọc danh mục + phân trang + sidebar Tin nổi bật) và chi tiết bài + tin liên quan. Chỉ đọc, không bình luận/chia sẻ."),
    ("2. Đối tượng được tính / hiển thị",
     "► Chỉ bài đã đăng (published) hiển thị.\n► Bài nổi bật có badge lửa + hiện ở sidebar 'Tin nổi bật'.\n► Thẻ tin: ảnh/pill danh mục/tiêu đề/mô tả/ngày/lượt xem."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Bài draft (Khóa) KHÔNG hiển thị.\n► Chi tiết bài không tồn tại/đã gỡ → 'Không tìm thấy bài viết'."),
    ("4. Bộ lọc thời gian áp dụng cho", "Không áp dụng."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Danh sách (cột trái) + sidebar Tin nổi bật (cột phải). Chi tiết: bài + Tin liên quan."),
    ("6. Quy tắc cộng dồn / deduplicate", "Danh sách 8 bài/trang, sidebar 6 tin nổi bật. Chi tiết không có tác giả, không nút chia sẻ."),
    ("7. Phân quyền cấp", "Public."),
    ("8. Cách tính các ô thống kê", "Thẻ/chi tiết hiển thị 'Lượt xem' (rút gọn k/tr). Phân trang '{total} tin bài'."),
    ("9. Ghi chú đọc bảng", "Tìm kiếm chỉ trigger bằng phím Enter (không có nút Tìm). Đổi danh mục/tìm → về trang 1."),
]

SECTIONS = [
    ("I", "DANH SÁCH TIN", [
        ("001", "Xem danh sách tin", "P0", "Có ≥10 bài đã đăng",
         "1. Mở /tin-tuc", "—",
         "- Breadcrumb 'Trang chủ / Tin tức, Thông báo'; lưới thẻ tin; sidebar 'Tin nổi bật'; phân trang '{total} tin bài'", "—"),
        ("002", "Tìm kiếm bằng Enter", "P0", "Có bài 'Nghỉ lễ 2/9'",
         "1. Gõ 'nghỉ lễ' vào 'Tìm kiếm tin tức, thông báo...'\n2. Nhấn Enter", "Từ khóa: nghỉ lễ",
         "- Danh sách lọc còn bài khớp, về trang 1", "BR-02"),
        ("003", "Lọc theo danh mục (pill)", "P1", "Có nhiều danh mục",
         "1. Bấm pill 1 danh mục", "—",
         "- Chỉ hiện bài thuộc danh mục đó, về trang 1", "—"),
        ("004", "Chuyển trang", "P1", "Có > 1 trang",
         "1. Bấm số trang 2 (hoặc ›)", "—",
         "- Tải trang 2, cuộn lên đầu", "—"),
        ("005", "Sidebar Tin nổi bật", "P1", "Có bài nổi bật",
         "1. Xem cột phải 'Tin nổi bật'", "—",
         "- Danh sách tin nổi bật (thumbnail + tiêu đề + danh mục · ngày)", "—"),
        ("006", "Danh sách rỗng", "P2", "Không có bài khớp",
         "1. Tìm từ khóa không có kết quả", "—",
         "- 'Chưa có tin bài nào'", "—"),
    ]),
    ("II", "CHI TIẾT TIN", [
        ("001", "Mở chi tiết bài", "P0", "Có bài đã đăng",
         "1. Click 1 thẻ tin", "—",
         "- Trang chi tiết: pill danh mục, tiêu đề, '{ngày} • {lượt xem} lượt xem', ảnh, nội dung", "—"),
        ("002", "Không có nút chia sẻ/tác giả", "P2", "Ở chi tiết bài",
         "1. Quan sát bài viết", "—",
         "- KHÔNG có nút Chia sẻ; KHÔNG hiển thị tác giả", "—"),
        ("003", "Tin liên quan", "P1", "Bài có tin liên quan",
         "1. Cuộn xuống 'Tin liên quan'\n2. Click 1 tin", "—",
         "- Hiện tối đa 3 thẻ; click → tải nội dung bài mới + cuộn lên đầu", "BR-04"),
        ("004", "Bài không tồn tại", "P1", "slug sai/đã gỡ",
         "1. Mở /tin-tuc/slug-sai", "—",
         "- 'Không tìm thấy bài viết' + 'Bài viết không tồn tại hoặc đã bị gỡ bỏ.' + nút 'Về danh sách tin tức'", "BR-03"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-hoc-vien\tin-tuc\testcase.xlsx",
    sheet_name="TinTuc", feature_name="Tin tức / Thông báo", module_name="Tin tức",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=None,
)
