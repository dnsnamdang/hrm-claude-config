# -*- coding: utf-8 -*-
"""Testcase Danh sách khóa học (elearning) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Màn danh sách/lọc khóa học (Học theo loại đào tạo & Học theo kỹ năng). Cho tìm/lọc/sắp xếp/phân trang danh sách khóa và mở chi tiết. Hai màn giống nhau, khác nhóm lọc đầu."),
    ("2. Đối tượng được tính / hiển thị",
     "► Thẻ khóa (LearnCard) hiển thị pill loại, 'Bắt buộc', trạng thái học ('Đã hoàn thành'/'Đang học {n}%').\n► Bộ lọc nhiều lựa chọn (checkbox)."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Không có kết quả → EmptyState.\n► Trạng thái học cá nhân cần đăng nhập."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Nhóm 'Thời lượng' (Dưới 60 / 60-120 / 120-240 / Trên 240 phút) là lọc theo thời lượng khóa, không phải ngày."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Breadcrumb + pill → FilterSidebar (trái) + AppliedFilters + ListTopbar + lưới LearnCard + Pagination."),
    ("6. Quy tắc cộng dồn / deduplicate", "Bộ lọc lưu vào URL; reload giữ nguyên. Vào kèm ?training_type_id/?skill_id tự chọn sẵn."),
    ("7. Phân quyền cấp", "Public."),
    ("8. Cách tính các ô thống kê", "ListTopbar: '{total} nội dung • Trang p/tp'. Mặc định 18/trang (options 12/18/24), sort 'Phổ biến'."),
    ("9. Ghi chú đọc bảng", "Tick/bỏ lọc → reset trang 1 + tải lại ngay. Đổi sort/page size → reset trang 1."),
]

SECTIONS = [
    ("I", "HIỂN THỊ & PHÂN TRANG", [
        ("001", "Xem danh sách khóa", "P0", "Có > 18 khóa",
         "1. Mở /hoc-theo-loai-dao-tao", "—",
         "- Lưới thẻ khóa; ListTopbar '{total} nội dung • Trang 1 / {tp}'; phân trang", "—"),
        ("002", "Chuyển trang", "P1", "Có > 1 trang",
         "1. Bấm số trang 2", "—",
         "- Tải trang 2, cuộn lên đầu", "—"),
        ("003", "Đổi số mục/trang", "P2", "Ở danh sách",
         "1. Chọn '24 / trang'", "—",
         "- Hiển thị 24 mục/trang, về trang 1", "—"),
    ]),
    ("II", "TÌM & LỌC", [
        ("001", "Tìm theo từ khóa", "P0", "Có khóa 'An toàn lao động'",
         "1. Gõ 'An toàn' vào 'Nhập tên khoá/môn...'", "Từ khóa: An toàn",
         "- Lưới lọc còn khóa khớp; chip 'Từ khoá: An toàn'", "—"),
        ("002", "Lọc theo Độ khó", "P1", "Có khóa nhiều độ khó",
         "1. Tick 'Cơ bản' ở nhóm Độ khó", "Độ khó: Cơ bản",
         "- Chỉ còn khóa Cơ bản; chip 'Độ khó: Cơ bản'", "BR-01"),
        ("003", "Lọc theo Thời lượng", "P1", "Có khóa nhiều thời lượng",
         "1. Tick 'Dưới 60 phút'", "Thời lượng: Dưới 60 phút",
         "- Chỉ còn khóa < 60 phút", "BR-02"),
        ("004", "Lọc theo Loại đào tạo (màn category)", "P0", "Màn Học theo loại đào tạo",
         "1. Tick 1 loại đào tạo", "—",
         "- Lọc theo loại; breadcrumb hiện tên loại; pill đổi", "—"),
        ("005", "Lọc theo Kỹ năng (màn skill)", "P0", "Màn Học theo kỹ năng",
         "1. Tick 1 kỹ năng", "—",
         "- Lọc theo kỹ năng; breadcrumb hiện tên kỹ năng", "—"),
        ("006", "Lọc Trạng thái = Bắt buộc", "P1", "Có khóa bắt buộc/tự chọn",
         "1. Tick 'Bắt buộc'", "Trạng thái: Bắt buộc",
         "- Chỉ còn khóa 'Bắt buộc'", "—"),
        ("007", "Vào màn kèm ?training_type_id", "P2", "URL có training_type_id",
         "1. Mở /hoc-theo-loai-dao-tao?training_type_id=5", "—",
         "- Tự chọn sẵn loại đó, danh sách đã lọc", "—"),
    ]),
    ("III", "SẮP XẾP", [
        ("001", "Sắp xếp Mới nhất", "P1", "Ở danh sách",
         "1. 'Sắp xếp' chọn 'Mới nhất'", "—",
         "- Danh sách theo mới nhất, về trang 1", "BR-03"),
        ("002", "Sắp xếp Đánh giá cao / Thời lượng", "P2", "Ở danh sách",
         "1. Chọn 'Đánh giá cao' rồi 'Thời lượng tăng'", "—",
         "- Danh sách sắp theo lựa chọn", "—"),
    ]),
    ("IV", "CHIP LỌC & RESET", [
        ("001", "Xóa 1 chip lọc", "P1", "Đang áp nhiều lọc",
         "1. Bấm X trên chip 'Độ khó: ...'", "—",
         "- Bỏ nhóm lọc đó, danh sách tải lại", "—"),
        ("002", "Xóa tất cả bộ lọc", "P1", "Đang áp lọc",
         "1. Bấm 'Xoá tất cả' (hoặc 'Reset')", "—",
         "- Bỏ toàn bộ lọc, về danh sách đầy đủ", "—"),
        ("003", "Danh sách rỗng", "P1", "Lọc không ra kết quả",
         "1. Lọc điều kiện không có khóa nào", "—",
         "- EmptyState 'Không có nội dung phù hợp bộ lọc' + nút 'Reset bộ lọc'", "BR-05"),
    ]),
    ("V", "MỞ CHI TIẾT", [
        ("001", "Click thẻ khóa", "P0", "Có kết quả",
         "1. Click 1 thẻ khóa (hoặc nút 'Chi tiết')", "—",
         "- Mở chi tiết khóa (/khoa-hoc/:slug)", "—"),
        ("002", "Nút thẻ theo trạng thái", "P2", "Có khóa đang học/đã xong",
         "1. Quan sát nút thẻ", "—",
         "- Đang học → 'Học tiếp'; đã xong → 'Xem lại'; còn lại → 'Chi tiết'", "—"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-hoc-vien\danh-sach-khoa-hoc\testcase.xlsx",
    sheet_name="DanhSachKhoaHoc", feature_name="Danh sách khóa học", module_name="DS khóa học",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=None,
)
