# -*- coding: utf-8 -*-
"""Testcase Chứng chỉ + Góc học tập (elearning) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Chứng chỉ: render + In/Lưu PDF chứng chỉ khóa/lộ trình. Góc học tập: không gian cá nhân 4 tab — Tổng quan, Tôi cần học, Tôi đang học, Chứng chỉ đã nhận được."),
    ("2. Đối tượng được tính / hiển thị",
     "► Chứng chỉ chỉ có khi đã hoàn thành khóa/lộ trình có bật chứng chỉ.\n► Badge tab = số đếm tương ứng.\n► Trạng thái học: Đã hoàn thành / Đang học / Chưa hoàn thành."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Cả 2 màn cần đăng nhập.\n► Chưa có chứng chỉ → 'Chưa có chứng chỉ nào'."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Tab 'Tôi đang học' có lọc thời gian đăng ký học (7/30/90 ngày gần đây, Trên 90 ngày)."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Chứng chỉ (canvas). Góc học tập: 4 tab; tab Tôi cần học có 2 bảng (khóa + lộ trình)."),
    ("6. Quy tắc cộng dồn / deduplicate", "Nhãn deadline: 'Quá hạn {n} ngày' / 'Còn {n} ngày'. Chứng chỉ canvas 1600×900."),
    ("7. Phân quyền cấp", "Không phân quyền cấp. Cần đăng nhập."),
    ("8. Cách tính các ô thống kê",
     "Tổng quan: vòng % 'Tiến độ tổng thể' + 4 dòng ('Nội dung bắt buộc chưa xong', 'Đang học', 'Đã hoàn thành', 'Mục cần chú ý ngay')."),
    ("9. Ghi chú đọc bảng", "Nhãn tab thật: 'Chứng chỉ đã nhận được'. Nút tiếp tục trên thẻ là 'Tiếp tục'. Nút chứng chỉ 'In / Lưu PDF' và 'Xem / Tải'."),
]

SECTIONS = [
    ("I", "CHỨNG CHỈ", [
        ("001", "Xem chứng chỉ khóa", "P0", "Đã hoàn thành khóa có chứng chỉ",
         "1. Mở /certificate/:slug", "—",
         "- Render canvas chứng chỉ + thanh có nút 'Quay lại', 'In / Lưu PDF'", "—"),
        ("002", "In / Lưu PDF", "P1", "Đang xem chứng chỉ",
         "1. Bấm 'In / Lưu PDF'", "—",
         "- Mở hộp thoại in (khổ landscape)", "—"),
        ("003", "Xem chứng chỉ lộ trình", "P1", "Đã hoàn thành lộ trình có chứng chỉ",
         "1. Mở /chung-chi-lo-trinh/:slug", "—",
         "- Render chứng chỉ lộ trình", "BR-01"),
        ("004", "Lỗi mẫu chứng chỉ", "P2", "Ảnh mẫu lỗi",
         "1. Mở chứng chỉ có ảnh mẫu hỏng", "—",
         "- 'Không tải được mẫu chứng chỉ' + nút 'Thử lại' + link 'Về trang chủ'", "BR-02"),
    ]),
    ("II", "GÓC HỌC TẬP — TỔNG QUAN", [
        ("001", "Xem tab Tổng quan", "P0", "Đã đăng nhập, có dữ liệu học",
         "1. Vào /goc-hoc-tap tab 'Tổng quan'", "—",
         "- Vòng tiến độ {n}% 'Tiến độ tổng thể' + 4 dòng thống kê + 'Hạn học gần nhất'", "—"),
    ]),
    ("III", "TÔI CẦN HỌC", [
        ("001", "Xem danh sách cần học", "P0", "Có khóa/lộ trình bắt buộc",
         "1. Mở tab 'Tôi cần học'", "—",
         "- pill 'Khoá cần học: {n}', 'Lộ trình cần học: {n}'; 2 bảng có cột STT/Nội dung/Loại đào tạo/Hạn hoàn thành/Trạng thái học/Tiến độ", "—"),
        ("002", "Mở drawer chi tiết", "P1", "Ở bảng cần học",
         "1. Bấm 'Chi tiết' 1 dòng", "—",
         "- Mở drawer: Trạng thái, Loại nội dung, Thời lượng, Ngày đăng ký, Tiến độ + nút 'Tiếp tục'", "—"),
    ]),
    ("IV", "TÔI ĐANG HỌC", [
        ("001", "Xem nội dung đang học", "P0", "Có nội dung đang học",
         "1. Mở tab 'Tôi đang học'", "—",
         "- Lưới StudyCard (badge loại, tiến độ 'Bài x/y'/'Khoá x/y' + %, nút 'Tiếp tục')", "—"),
        ("002", "Lọc theo loại + thời gian", "P1", "Ở tab đang học",
         "1. Lọc loại 'Khoá học'\n2. Lọc '7 ngày gần đây'", "—",
         "- Danh sách lọc theo lựa chọn", "—"),
        ("003", "Tìm theo tên", "P2", "Ở tab đang học",
         "1. Gõ vào 'Tìm theo tên khoá học / tên lộ trình'", "—",
         "- Lọc theo từ khóa; rỗng: 'Không có nội dung phù hợp bộ lọc'", "—"),
        ("004", "Xem khóa con của lộ trình", "P2", "Thẻ lộ trình",
         "1. Bấm 'Xem {n} khoá con'", "—",
         "- Bung danh sách khóa con, mỗi khóa có nút 'Học'/'Xem lại'", "—"),
        ("005", "Tiếp tục học", "P1", "Thẻ đang học",
         "1. Bấm 'Tiếp tục'", "—",
         "- Mở màn học nội dung đó", "—"),
    ]),
    ("V", "CHỨNG CHỈ ĐÃ NHẬN ĐƯỢC", [
        ("001", "Xem danh sách chứng chỉ", "P0", "Đã nhận ≥1 chứng chỉ",
         "1. Mở tab 'Chứng chỉ đã nhận được'", "—",
         "- pill '{n} chứng chỉ'; thẻ có 'Ngày cấp', 'Hiệu lực', nút 'Chi tiết' + 'Xem / Tải'", "—"),
        ("002", "Mở chứng chỉ", "P1", "Có chứng chỉ",
         "1. Bấm 'Xem / Tải' 1 chứng chỉ", "—",
         "- Mở màn chứng chỉ tương ứng (khóa/lộ trình)", "—"),
        ("003", "Chưa có chứng chỉ", "P2", "Chưa nhận chứng chỉ nào",
         "1. Mở tab", "—",
         "- 'Chưa có chứng chỉ nào' + 'Hoàn thành khoá học/lộ trình để nhận chứng chỉ.'", "—"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-hoc-vien\chung-chi-goc-hoc-tap\testcase.xlsx",
    sheet_name="ChungChiGocHocTap", feature_name="Chứng chỉ & Góc học tập", module_name="Chứng chỉ & Góc HT",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=None,
)
