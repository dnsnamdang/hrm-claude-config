# -*- coding: utf-8 -*-
"""Testcase Tìm kiếm (elearning) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Trang kết quả tìm kiếm: hiển thị khóa học + lộ trình khớp từ khóa (lấy từ URL ?q=). Có badge lọc loại và link 'Xem thêm' sang danh sách."),
    ("2. Đối tượng được tính / hiển thị",
     "► Section 'Khóa học phù hợp ({n})' + 'Lộ trình học ({n})'.\n► Badge lọc: Tất cả / Khóa học / Lộ trình (mặc định Tất cả)."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Badge lọc ẩn/hiện section (không gọi lại API).\n► Không có kết quả → 'Không tìm thấy nội dung phù hợp'."),
    ("4. Bộ lọc thời gian áp dụng cho", "Không áp dụng."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Tiêu đề + badge loại + section khóa (LearnCard) + section lộ trình (PathCard)."),
    ("6. Quy tắc cộng dồn / deduplicate", "Từ khóa lấy từ URL ?q= (ô nhập ở header). Đổi q → tìm lại."),
    ("7. Phân quyền cấp", "Public."),
    ("8. Cách tính các ô thống kê", "Section hiển thị số lượng kết quả '({n})'."),
    ("9. Ghi chú đọc bảng", "'Xem thêm →' khóa → danh sách khóa (kèm keyword); lộ trình → danh sách lộ trình."),
]

SECTIONS = [
    ("I", "TÌM KIẾM & KẾT QUẢ", [
        ("001", "Xem kết quả tìm kiếm", "P0", "Có nội dung khớp 'excel'",
         "1. Tìm 'excel' (từ header) → mở /tim-kiem?q=excel", "q=excel",
         "- Tiêu đề 'Kết quả tìm kiếm cho \"excel\"'; section 'Khóa học phù hợp ({n})' + 'Lộ trình học ({n})'", "—"),
        ("002", "Không có kết quả", "P1", "Không có nội dung khớp 'zzz'",
         "1. Mở /tim-kiem?q=zzz", "q=zzz",
         "- 'Không tìm thấy nội dung phù hợp'", "—"),
        ("003", "Đổi từ khóa tìm lại", "P2", "Đang ở trang tìm kiếm",
         "1. Đổi q trên URL", "—",
         "- Tự tìm lại theo q mới", "BR-01"),
    ]),
    ("II", "LỌC LOẠI", [
        ("001", "Lọc chỉ Khóa học", "P1", "Kết quả có cả khóa + lộ trình",
         "1. Bấm badge 'Khóa học'", "—",
         "- Chỉ hiện section khóa học (ẩn lộ trình)", "BR-02"),
        ("002", "Lọc chỉ Lộ trình", "P1", "Kết quả có cả 2",
         "1. Bấm badge 'Lộ trình'", "—",
         "- Chỉ hiện section lộ trình", "—"),
        ("003", "Về Tất cả", "P2", "Đang lọc 1 loại",
         "1. Bấm badge 'Tất cả'", "—",
         "- Hiện lại cả 2 section", "—"),
    ]),
    ("III", "ĐIỀU HƯỚNG", [
        ("001", "Xem thêm khóa học", "P1", "Section khóa có kết quả",
         "1. Bấm 'Xem thêm →' ở 'Khóa học phù hợp'", "—",
         "- Sang danh sách khóa học kèm keyword", "BR-03"),
        ("002", "Xem thêm lộ trình", "P1", "Section lộ trình có kết quả",
         "1. Bấm 'Xem thêm →' ở 'Lộ trình học'", "—",
         "- Sang danh sách lộ trình kèm keyword", "—"),
        ("003", "Click thẻ kết quả", "P0", "Có kết quả",
         "1. Click 1 thẻ khóa / lộ trình", "—",
         "- Mở chi tiết tương ứng", "—"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-hoc-vien\tim-kiem\testcase.xlsx",
    sheet_name="TimKiem", feature_name="Tìm kiếm", module_name="Tìm kiếm",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=None,
)
