# -*- coding: utf-8 -*-
"""Testcase Chi tiết lộ trình (elearning) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Trang chi tiết lộ trình: giới thiệu lộ trình gồm nhiều khóa theo thứ tự, cho tham gia, xem điều kiện đạt, xem cây khóa→chương→bài và vào học (kèm ngữ cảnh lộ trình ?lp=)."),
    ("2. Đối tượng được tính / hiển thị",
     "► Trạng thái học: Chưa tham gia / Đã tham gia (chưa học) / Đang học / Đã hoàn thành.\n► Outline 3 cấp: Khóa → Chương → Bài.\n► Khóa sau bị khóa nếu chưa hoàn thành khóa trước."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Khách chưa đăng nhập: bấm tham gia/học → yêu cầu đăng nhập.\n► Khóa bị lock trong lộ trình → nút 'Vào học' đổi thành 'Khoá' (disabled)."),
    ("4. Bộ lọc thời gian áp dụng cho", "Không áp dụng."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Hero → Card ghi danh → Tabs → Outline 'Nội dung lộ trình' (Khóa → Chương → Bài)."),
    ("6. Quy tắc cộng dồn / deduplicate", "Vào học mở màn học với ?lp={slug}. Sau ghi danh: reload trang (không tự vào học, khác khóa học)."),
    ("7. Phân quyền cấp", "Không phân quyền cấp. Nhân viên học lộ trình được gán; học viên ngoài học lộ trình Public."),
    ("8. Cách tính các ô thống kê", "Điều kiện đạt: 'Tất cả các khoá đạt' / 'Đạt các khoá bắt buộc' / 'Đạt X% số khoá'. Hero: {n} khoá học, {n} bài học."),
    ("9. Ghi chú đọc bảng", "Nút card khác khóa học: trạng thái 'Đã tham gia (chưa học)'. Không có khối bài thi."),
]

SECTIONS = [
    ("I", "XEM CHI TIẾT", [
        ("001", "Xem trang chi tiết lộ trình", "P0", "Lộ trình tồn tại, public",
         "1. Mở /lo-trinh/:slug", "—",
         "- Hero có badge '{n} khoá học', '{n} bài học'; card ghi danh; outline 'Nội dung lộ trình'", "—"),
        ("002", "Xem tab Tiêu chí hoàn thành", "P1", "Ở trang chi tiết",
         "1. Mở tab 'Tiêu chí hoàn thành'", "—",
         "- Thẻ 'Điều kiện đạt của lộ trình' + bảng khóa (Tên khoá học, Bắt buộc, Hình thức đánh giá, Trạng thái)", "—"),
        ("003", "Lộ trình không tồn tại", "P1", "slug sai",
         "1. Mở /lo-trinh/slug-sai", "—",
         "- 'Không tìm thấy' + 'Lộ trình bạn đang tìm không tồn tại hoặc đã bị xoá.'", "—"),
    ]),
    ("II", "OUTLINE 3 CẤP & KHÓA LOCK", [
        ("001", "Mở/đóng tất cả khóa", "P2", "Lộ trình nhiều khóa",
         "1. Bấm 'Mở tất cả khoá'\n2. Bấm 'Đóng tất cả khoá'", "—",
         "- Bung/thu danh sách khóa (kèm chương → bài)", "—"),
        ("002", "Khóa sau bị lock", "P0", "Khóa 2 chưa mở do khóa 1 chưa xong",
         "1. Xem khóa 2 trong outline", "—",
         "- Khóa 2 có badge 'Khoá'; nút bài đổi thành 'Khoá' (disabled) tooltip 'Cần hoàn thành khoá trước trong lộ trình'", "BR-02"),
        ("003", "Bấm bài trong khóa bị lock", "P1", "Khóa 2 đang lock",
         "1. Bấm 1 bài trong khóa 2", "—",
         "- Toast 'Cần hoàn thành khoá trước trong lộ trình'", "—"),
    ]),
    ("III", "GHI DANH & VÀO HỌC", [
        ("001", "Tham gia lộ trình", "P0", "Đã đăng nhập, chưa tham gia",
         "1. Bấm 'Tham gia'", "—",
         "- Toast 'Đã tham gia lộ trình thành công'\n- Trang tải lại (KHÔNG tự vào học)", "BR-04"),
        ("002", "Bắt đầu học", "P0", "Đã tham gia, có khóa mở",
         "1. Bấm 'Bắt đầu học'", "—",
         "- Mở màn học khóa đầu tiên mở được, kèm ngữ cảnh lộ trình (?lp=)", "—"),
        ("003", "Bắt đầu học khi chưa có khóa", "P2", "Lộ trình chưa có khóa để học",
         "1. Bấm 'Bắt đầu học'", "—",
         "- Toast 'Lộ trình chưa có khoá để học'", "—"),
        ("004", "Vào học bài (giữ ?lp=)", "P0", "Đã tham gia, bài mở",
         "1. Bấm 'Vào học' 1 bài", "—",
         "- Mở màn học; nút quay lại là 'Lộ trình' (giữ ngữ cảnh)", "BR-03"),
        ("005", "Vào học khi chưa tham gia", "P1", "Đã đăng nhập, chưa tham gia",
         "1. Bấm 'Vào học' 1 bài", "—",
         "- Toast 'Vui lòng tham gia lộ trình trước khi học'", "—"),
    ]),
    ("IV", "THẢO LUẬN", [
        ("001", "Gửi bình luận lộ trình", "P1", "Đã đăng nhập, tab Thảo luận",
         "1. Chọn 'Đánh giá'\n2. Nhập 'Nội dung'\n3. Bấm 'Gửi'", "—",
         "- Toast 'Đã gửi bình luận'", "—"),
        ("002", "Trang thảo luận riêng", "P2", "Lộ trình có đánh giá",
         "1. Mở /lo-trinh/:slug/thao-luan", "—",
         "- Banner ngữ cảnh + nút 'Quay lại lộ trình' + tổng đánh giá + lọc theo sao", "—"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-hoc-vien\chi-tiet-lo-trinh\testcase.xlsx",
    sheet_name="ChiTietLoTrinh", feature_name="Chi tiết lộ trình", module_name="Chi tiết lộ trình",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=None,
)
