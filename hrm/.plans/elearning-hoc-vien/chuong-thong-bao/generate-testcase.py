# -*- coding: utf-8 -*-
"""Testcase Chuông Thông báo (elearning) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Chuông thông báo trên header (khi đã đăng nhập): hiển thị thông báo hệ thống real-time (onboarding tự ghi danh, chấm bài thi xong), badge số chưa đọc, dropdown danh sách, đánh dấu đã đọc, điều hướng theo link. Khác với màn Tin tức (CMS)."),
    ("2. Đối tượng được tính / hiển thị",
     "► Nhân viên: có thông báo thật + real-time socket + toast.\n► Học viên ngoài: chuông hiện nhưng danh sách rỗng.\n► Loại thông báo: OnboardingAutoEnroll, ExamGraded."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Chưa đăng nhập → không hiện chuông.\n► Học viên ngoài không kết nối socket (không real-time)."),
    ("4. Bộ lọc thời gian áp dụng cho", "Không áp dụng. Thời gian item hiển thị dd/mm HH:mm."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Danh sách phẳng item: title, url?, created_at, read_at?. Badge = unread_count."),
    ("6. Quy tắc cộng dồn / deduplicate", "Badge >9 hiển thị '9+'. Real-time nhận đúng loại → fetch lại danh sách để đồng bộ."),
    ("7. Phân quyền cấp", "Không phân quyền cấp. Phân biệt nhân viên (có thông báo) vs học viên ngoài (rỗng)."),
    ("8. Cách tính các ô thống kê", "Badge = số chưa đọc (read_at=null). 'Đánh dấu tất cả đã đọc' → unread=0."),
    ("9. Ghi chú đọc bảng", "Lỗi tải/đánh dấu im lặng (không chặn UI). Click ra ngoài dropdown → đóng."),
]

SECTIONS = [
    ("I", "HIỂN THỊ CHUÔNG", [
        ("001", "Chuông hiện khi đã đăng nhập", "P0", "Đã đăng nhập, có ≥1 thông báo chưa đọc",
         "1. Quan sát header", "—",
         "- Hiện icon chuông + badge đỏ số chưa đọc", "BR-01"),
        ("002", "Badge >9 hiển thị 9+", "P1", "Có 12 thông báo chưa đọc",
         "1. Quan sát badge", "—",
         "- Badge hiển thị '9+'", "BR-01"),
        ("003", "Không hiện chuông khi chưa đăng nhập", "P1", "Chưa đăng nhập",
         "1. Quan sát header", "—",
         "- Không có chuông thông báo (chỉ nút Đăng nhập)", "—"),
        ("004", "Học viên ngoài — danh sách rỗng", "P1", "Đăng nhập tài khoản learner",
         "1. Bấm chuông", "—",
         "- Chuông hiện nhưng dropdown 'Chưa có thông báo'", "BR-02"),
    ]),
    ("II", "ĐỌC & ĐIỀU HƯỚNG", [
        ("001", "Mở dropdown xem danh sách", "P0", "Nhân viên có thông báo",
         "1. Bấm chuông", "—",
         "- Dropdown 'Thông báo' + danh sách item (tiêu đề + dd/mm HH:mm); chưa đọc có nền nhạt + chấm đỏ", "—"),
        ("002", "Click 1 thông báo chưa đọc", "P0", "Có thông báo chưa đọc có url",
         "1. Bấm chuông\n2. Click 1 thông báo chưa đọc", "—",
         "- Đánh dấu đã đọc (badge giảm 1), dropdown đóng, điều hướng tới trang liên quan", "BR-04"),
        ("003", "Đánh dấu tất cả đã đọc", "P1", "Có ≥2 thông báo chưa đọc",
         "1. Bấm chuông\n2. Bấm 'Đánh dấu tất cả đã đọc'", "—",
         "- Tất cả về đã đọc, badge = 0, nút biến mất", "BR-05"),
        ("004", "Click ra ngoài đóng dropdown", "P2", "Dropdown đang mở",
         "1. Click vùng ngoài dropdown", "—",
         "- Dropdown đóng", "BR-07"),
    ]),
    ("III", "REAL-TIME (NHÂN VIÊN)", [
        ("001", "Nhận thông báo mới real-time", "P0", "Nhân viên đăng nhập; hệ thống phát sự kiện (VD chấm bài thi xong)",
         "1. Chờ hệ thống đẩy thông báo qua socket", "loại: ExamGraded",
         "- Danh sách cập nhật + badge tăng + toast hiện tiêu đề thông báo mới", "BR-03"),
        ("002", "Học viên ngoài không nhận real-time", "P1", "Học viên ngoài đăng nhập",
         "1. Hệ thống phát sự kiện", "—",
         "- Không kết nối socket, không nhận thông báo (danh sách vẫn rỗng)", "BR-02"),
        ("003", "Thông báo onboarding tự ghi danh", "P1", "Nhân viên mới được auto-enroll khóa",
         "1. Chờ thông báo OnboardingAutoEnroll", "loại: OnboardingAutoEnroll",
         "- Nhận thông báo tự ghi danh + toast", "BR-03"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-hoc-vien\chuong-thong-bao\testcase.xlsx",
    sheet_name="ChuongThongBao", feature_name="Chuông Thông báo (real-time)", module_name="Thông báo",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=None,
)
