# -*- coding: utf-8 -*-
"""Testcase Trang chủ (elearning) — theo nhãn UI thật."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _tc_builder import build

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Trang chủ app học viên: hoạt động gần đây, danh mục nội dung, vinh danh học viên và 4 nhóm gợi ý (Bạn cần học / Khuyến nghị cho bạn / Nội dung nhiều người học / Nội dung mới). Điều hướng tới chi tiết + trang xem tất cả."),
    ("2. Đối tượng được tính / hiển thị",
     "► 4 nhóm nội dung chỉ hiện khi có dữ liệu.\n► Thẻ hiển thị trạng thái học ('Đã hoàn thành'/'Đang học {n}%') khi đã đăng nhập.\n► Loại thẻ: 'Lộ trình' / 'Môn học' / 'Khoá học'."),
    ("3. Đối tượng bị ẩn / không tính",
     "► Nhóm không có dữ liệu bị ẩn.\n► Nội dung cá nhân hóa (Bạn cần học) cần đăng nhập."),
    ("4. Bộ lọc thời gian áp dụng cho", "Không áp dụng."),
    ("5. Cấu trúc dữ liệu / cây phân cấp", "Banner → Danh mục → Vinh danh → 4 nhóm nội dung (lưới thẻ)."),
    ("6. Quy tắc cộng dồn / deduplicate", "Nút 'Xem tất cả' của 4 nhóm điều hướng thật; các nút banner/danh mục/vinh danh chỉ demo toast."),
    ("7. Phân quyền cấp", "Public. Không phân quyền cấp."),
    ("8. Cách tính các ô thống kê", "CategoryCard hiển thị '{n} nội dung'. Không có KPI khác."),
    ("9. Ghi chú đọc bảng",
     "NHIỀU nút là DEMO (chỉ toast 'Demo: ...', không điều hướng): 'Bạn cần học', 'Khuyến nghị', 'Xem' hoạt động, 'Xem tất cả' của Danh mục, click CategoryCard, click Vinh danh. Chuỗi 'Bảng vàng tháng 01' hardcode."),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG CHỦ", [
        ("001", "Load trang chủ", "P0", "Có dữ liệu home",
         "1. Mở /", "—",
         "- Hiện banner, 'Hoạt động gần đây', 'Danh mục nội dung', 'Vinh danh học viên', các nhóm nội dung", "—"),
        ("002", "4 nhóm nội dung hiển thị", "P1", "Có dữ liệu 4 nhóm",
         "1. Cuộn xuống", "—",
         "- Thấy 'Bạn cần học', 'Khuyến nghị cho bạn', 'Nội dung nhiều người học', 'Nội dung mới'", "—"),
        ("003", "Nhóm rỗng bị ẩn", "P2", "1 nhóm không có dữ liệu",
         "1. Cuộn xem nhóm đó", "—",
         "- Nhóm không có dữ liệu không hiển thị", "BR-01"),
    ]),
    ("II", "NÚT DEMO (CHỈ TOAST)", [
        ("001", "Nút 'Bạn cần học' trên banner", "P2", "Ở trang chủ",
         "1. Bấm 'Bạn cần học' trên banner", "—",
         "- Toast 'Demo: Bạn cần học' (KHÔNG điều hướng)", "Hành vi demo"),
        ("002", "Nút 'Khuyến nghị' trên banner", "P2", "Ở trang chủ",
         "1. Bấm 'Khuyến nghị' trên banner", "—",
         "- Toast 'Demo: Khuyến nghị'", "Hành vi demo"),
        ("003", "Nút 'Xem' hoạt động gần đây", "P2", "Ở trang chủ",
         "1. Bấm 'Xem' ở panel hoạt động", "—",
         "- Toast 'Demo: Xem tất cả hoạt động'", "Hành vi demo"),
        ("004", "'Xem tất cả' Danh mục", "P2", "Ở trang chủ",
         "1. Bấm 'Xem tất cả' ở 'Danh mục nội dung'", "—",
         "- Toast 'Demo: Danh mục'", "Hành vi demo"),
        ("005", "Click danh mục", "P2", "Có danh mục",
         "1. Click 1 thẻ danh mục", "—",
         "- Toast 'Demo: mở danh mục {tên}'", "Hành vi demo"),
        ("006", "Click thẻ Vinh danh", "P2", "Có vinh danh",
         "1. Click 1 thẻ vinh danh", "—",
         "- Toast 'Demo: mở vinh danh {tên}'", "Hành vi demo"),
    ]),
    ("III", "ĐIỀU HƯỚNG THẬT", [
        ("001", "Xem tất cả 'Bạn cần học'", "P0", "Nhóm có dữ liệu",
         "1. Bấm 'Xem tất cả' ở 'Bạn cần học'", "—",
         "- Mở trang /noi-dung/bat-buoc (danh sách đầy đủ)", "BR-01"),
        ("002", "Xem tất cả 'Nội dung mới'", "P1", "Nhóm có dữ liệu",
         "1. Bấm 'Xem tất cả' ở 'Nội dung mới'", "—",
         "- Mở /noi-dung/moi", "—"),
        ("003", "Click thẻ khóa học", "P0", "Có thẻ loại 'Khoá học'",
         "1. Click 1 thẻ 'Khoá học'/'Môn học'", "—",
         "- Mở chi tiết khóa (/khoa-hoc/:slug)", "BR-02"),
        ("004", "Click thẻ lộ trình", "P0", "Có thẻ loại 'Lộ trình'",
         "1. Click 1 thẻ 'Lộ trình'", "—",
         "- Mở chi tiết lộ trình (/lo-trinh/:slug)", "BR-02"),
    ]),
    ("IV", "TRANG XEM TẤT CẢ (/noi-dung/:type)", [
        ("001", "Xem thêm nối danh sách", "P1", "Nhóm có > 12 mục",
         "1. Vào /noi-dung/pho-bien\n2. Bấm 'Xem thêm'", "—",
         "- Nối thêm 12 mục; dòng 'Đã hiển thị {n} / {total} nội dung'", "BR-04"),
        ("002", "Slug sai → mặc định", "P2", "—",
         "1. Vào /noi-dung/khong-hop-le", "—",
         "- Mặc định về 'Nội dung mới'", "—"),
    ]),
]

build(
    output_file=r"d:\CompanyProject\hrm-cursor\.plans\elearning-hoc-vien\trang-chu\testcase.xlsx",
    sheet_name="TrangChu", feature_name="Trang chủ", module_name="Trang chủ",
    description_block=DESCRIPTION_BLOCK, sections=SECTIONS, role_tcs=None,
)
