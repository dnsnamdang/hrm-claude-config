# -*- coding: utf-8 -*-
"""Sinh LẠI testcase ĐIỂM DANH THÀNH VIÊN meeting theo chuẩn team hiện tại (Redmine #10534).

Thay cho bản cũ meeting-diem-danh/testcase-diem-danh.xlsx (15 cột + thuật ngữ code).
"""
import os
import sys

sys.path.insert(0, r"D:\CompanyProject\hrm-cursor\.claude\skills\testcase-documenter\assets")
from tc_engine import build  # noqa: E402

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "testcase - Điểm danh thành viên meeting.xlsx")
SHEET_NAME = "DiemDanh"
FEATURE_NAME = "Điểm danh thành viên Meeting"
MODULE_NAME = "Điểm danh Meeting"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Cho phép người phụ trách điểm danh từng thành viên tham dự cuộc họp (nội bộ + khách hàng) tại "
     "tab 'Điểm danh' của màn Chi tiết/Sửa meeting.\n"
     "Điểm danh đầy đủ là điều kiện bắt buộc trước khi hoàn thành cuộc họp."),
    ("2. Đối tượng được hiển thị",
     "► Thành viên Nội bộ — lấy từ khối 'Thành phần — Phía Công ty', gắn nhãn 'Nội bộ'.\n"
     "► Thành viên Khách hàng — lấy từ khối 'Thành phần — Phía Khách hàng', gắn nhãn 'Khách hàng' "
     "(chỉ có khi loại họp có khách hàng).\n"
     "► Trạng thái điểm danh mỗi người: 'Dự kiến tham gia' (mặc định), 'Có mặt', 'Vắng có lý do', "
     "'Vắng không lý do'.\n"
     "► Mỗi dòng gồm: STT, Họ và tên, Chức vụ / Phòng ban, Thành phần, Trạng thái điểm danh, Ghi chú / Lý do."),
    ("3. Đối tượng bị ẩn / không hiển thị",
     "► Cuộc họp chưa có thành viên nào: hiển thị 'Chưa có thành viên nào để điểm danh', không hiện bảng.\n"
     "► Cuộc họp nội bộ: tab Điểm danh không liệt kê khách hàng (vì không có khối khách hàng)."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "— Không áp dụng. Tab Điểm danh không có bộ lọc."),
    ("5. Cấu trúc dữ liệu",
     "► Danh sách điểm danh dựng từ danh sách người tham gia đã khai ở tab Thông tin: nội bộ trước, "
     "khách hàng sau.\n"
     "► Mỗi người lưu kèm trạng thái điểm danh và ghi chú/lý do riêng."),
    ("6. Quy tắc điền mặc định",
     "► Người chưa điểm danh mặc định là 'Dự kiến tham gia'.\n"
     "► Ghi chú/Lý do để trống nếu không nhập."),
    ("7. Phân quyền",
     "— Không có quyền riêng cho tab Điểm danh. Quyền điểm danh đi kèm quyền SỬA meeting.\n"
     "► Chỉ điểm danh được khi đang ở màn Sửa VÀ cuộc họp ở trạng thái 'Đã chốt lịch'.\n"
     "► Các trạng thái khác ('Lưu nháp', 'Lên lịch hẹn', 'Đã hoàn thành', 'Huỷ') hoặc màn Xem → chỉ đọc.\n"
     "► Nhóm quyền 'Quản lý meeting' chỉ có quyền xem theo cấp: tổng công ty / công ty / phòng ban / bộ phận."),
    ("8. Cách tính các ô thống kê",
     "— Không có ô thống kê dạng số.\n"
     "► 'Điểm danh đầy đủ' = không còn ai ở trạng thái 'Dự kiến tham gia' (mọi người đã ở 'Có mặt' "
     "hoặc 'Vắng có lý do' hoặc 'Vắng không lý do')."),
    ("9. Ghi chú đọc bảng",
     "► Bẫy hay gặp: điểm danh chỉ mở khi cuộc họp 'Đã chốt lịch' và đang ở màn Sửa — ở màn Xem hay "
     "trạng thái khác chỉ đọc.\n"
     "► Muốn hoàn thành cuộc họp phải: (1) đã có biên bản, (2) điểm danh đầy đủ. Thiếu biên bản hệ "
     "thống chuyển sang tab Biên bản; thiếu điểm danh chuyển sang tab Điểm danh.\n"
     "► Điểm danh của mỗi người độc lập; chọn người này không ảnh hưởng người khác."),
]

HAS_ROLE = True
ROLE_TCS = [
    ("01", "Được điểm danh khi Sửa cuộc họp 'Đã chốt lịch'", "P0",
     "Tài khoản có quyền vào màn Quản lý meeting; cuộc họp ở trạng thái 'Đã chốt lịch'",
     "1. Mở Sửa cuộc họp 'Đã chốt lịch'\n2. Vào tab Điểm danh",
     "Trạng thái: Đã chốt lịch",
     "- Cho phép chọn trạng thái điểm danh và nhập ghi chú cho từng người"),
    ("02", "Chỉ đọc khi mở ở màn Xem chi tiết", "P0",
     "Cuộc họp 'Đã chốt lịch', mở màn Xem",
     "1. Mở Chi tiết cuộc họp (không phải Sửa)\n2. Vào tab Điểm danh",
     "Màn: Xem chi tiết",
     "- Không cho chọn trạng thái/nhập ghi chú; chỉ hiển thị trạng thái điểm danh dạng chữ"),
    ("03", "Không có quyền nào trong nhóm Quản lý meeting → không vào được", "P1",
     "Tài khoản không có quyền 'Xem danh sách meeting…' nào",
     "1. Đăng nhập\n2. Tìm menu Quản lý meeting",
     "Quyền: (không có)",
     "- Không vào được menu, không điểm danh được cuộc họp nào"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TAB ĐIỂM DANH & DANH SÁCH", [
        ("001", "Mở tab 'Điểm danh' từ màn chi tiết", "P0",
         "Cuộc họp có 2 thành viên nội bộ + 1 khách hàng",
         "1. Mở Chi tiết cuộc họp\n2. Bấm tab 'Điểm danh'",
         "2 nội bộ + 1 khách hàng",
         "- Hiển thị tiêu đề 'Điểm danh thành viên'\n- Bảng liệt kê đủ 3 người: nội bộ trước, khách hàng sau; STT 1,2,3"),
        ("002", "Hiển thị đủ 6 cột", "P1",
         "Cuộc họp có thành viên",
         "1. Mở tab Điểm danh\n2. Quan sát tiêu đề cột",
         "—",
         "- Các cột: STT | Họ và tên | Chức vụ / Phòng ban | Thành phần | Trạng thái điểm danh | Ghi chú / Lý do"),
        ("003", "Nhãn Thành phần đúng loại", "P1",
         "Cuộc họp có 1 nội bộ + 1 khách hàng",
         "1. Mở tab Điểm danh\n2. Quan sát cột Thành phần",
         "—",
         "- Dòng nội bộ gắn nhãn 'Nội bộ'\n- Dòng khách hàng gắn nhãn 'Khách hàng'"),
        ("004", "Cuộc họp không có thành viên", "P1",
         "Cuộc họp chưa khai người tham gia",
         "1. Mở tab Điểm danh",
         "Không có thành viên",
         "- Hiển thị 'Chưa có thành viên nào để điểm danh', không hiện bảng"),
        ("005", "Hiển thị tên & chức vụ, thiếu thì '-'", "P2",
         "Có 1 thành viên thiếu chức vụ",
         "1. Mở tab Điểm danh\n2. Quan sát dòng thiếu chức vụ",
         "Chức vụ: trống",
         "- Cột Họ và tên hiển thị đúng tên\n- Cột Chức vụ / Phòng ban hiển thị '-'"),
    ]),
    ("II", "ĐIỀU KIỆN ĐƯỢC PHÉP ĐIỂM DANH", [
        ("001", "Cho điểm danh khi Sửa cuộc họp 'Đã chốt lịch'", "P0",
         "Cuộc họp 'Đã chốt lịch', mở màn Sửa",
         "1. Mở Sửa cuộc họp\n2. Vào tab Điểm danh\n3. Quan sát điều khiển",
         "Trạng thái: Đã chốt lịch",
         "- Mỗi dòng có cụm chọn trạng thái: 'Có mặt', 'Vắng có lý do', 'Vắng không lý do'\n- Ô Ghi chú cho nhập\n- Có nút 'Điểm danh nhanh: Tất cả có mặt'"),
        ("002", "Chỉ đọc ở màn Xem chi tiết", "P0",
         "Cuộc họp 'Đã chốt lịch', màn Xem",
         "1. Mở Chi tiết cuộc họp\n2. Vào tab Điểm danh",
         "Màn: Xem",
         "- Không có cụm chọn trạng thái\n- Hiển thị trạng thái dạng chữ\n- Ô Ghi chú không nhập được\n- Không có nút 'Điểm danh nhanh'"),
        ("003", "Chỉ đọc khi cuộc họp 'Lên lịch hẹn'", "P0",
         "Cuộc họp 'Lên lịch hẹn', mở màn Sửa",
         "1. Mở Sửa\n2. Vào tab Điểm danh",
         "Trạng thái: Lên lịch hẹn",
         "- Chỉ đọc: không chọn trạng thái, không có nút Điểm danh nhanh"),
        ("004", "Chỉ đọc khi cuộc họp 'Lưu nháp'", "P1",
         "Cuộc họp 'Lưu nháp', mở màn Sửa",
         "1. Mở Sửa\n2. Vào tab Điểm danh",
         "Trạng thái: Lưu nháp",
         "- Chỉ đọc, không điểm danh được"),
        ("005", "Chỉ đọc khi cuộc họp 'Đã hoàn thành'", "P0",
         "Cuộc họp 'Đã hoàn thành'",
         "1. Mở Chi tiết\n2. Vào tab Điểm danh",
         "Trạng thái: Đã hoàn thành",
         "- Hiển thị lại trạng thái điểm danh đã ghi trước đó, không sửa được"),
        ("006", "Chỉ đọc khi cuộc họp 'Huỷ'", "P1",
         "Cuộc họp 'Huỷ'",
         "1. Mở Chi tiết\n2. Vào tab Điểm danh",
         "Trạng thái: Huỷ",
         "- Chỉ đọc, không sửa được"),
    ]),
    ("III", "ĐIỂM DANH TỪNG THÀNH VIÊN", [
        ("001", "Chọn 'Có mặt'", "P0",
         "Đang Sửa cuộc họp 'Đã chốt lịch', tab Điểm danh, một người đang 'Dự kiến tham gia'",
         "1. Tại dòng thành viên, chọn 'Có mặt'",
         "Từ 'Dự kiến tham gia' → chọn 'Có mặt'",
         "- Mục 'Có mặt' được tô chọn (nền xanh)\n- Các lựa chọn khác trở về bình thường"),
        ("002", "Chọn 'Vắng có lý do'", "P0",
         "Đang Sửa cuộc họp 'Đã chốt lịch', tab Điểm danh",
         "1. Chọn 'Vắng có lý do' tại một dòng",
         "Chọn 'Vắng có lý do'",
         "- Mục 'Vắng có lý do' được tô chọn (nền vàng)"),
        ("003", "Chọn 'Vắng không lý do'", "P0",
         "Đang Sửa cuộc họp 'Đã chốt lịch', tab Điểm danh",
         "1. Chọn 'Vắng không lý do' tại một dòng",
         "Chọn 'Vắng không lý do'",
         "- Mục 'Vắng không lý do' được tô chọn (nền đỏ)"),
        ("004", "Đổi trạng thái qua lại", "P1",
         "Đang Sửa cuộc họp 'Đã chốt lịch'",
         "1. Chọn 'Có mặt'\n2. Chọn 'Vắng không lý do'\n3. Chọn lại 'Có mặt'",
         "—",
         "- Mỗi bước chỉ một trạng thái được chọn; kết quả cuối là 'Có mặt'"),
        ("005", "Nhập Ghi chú / Lý do", "P1",
         "Đang Sửa cuộc họp 'Đã chốt lịch'",
         "1. Nhập 'Đi công tác đột xuất' vào ô Ghi chú của một dòng",
         "Ghi chú: Đi công tác đột xuất",
         "- Ô nhận đúng nội dung; lưu lại sau khi lưu cuộc họp"),
        ("006", "Ô Ghi chú bị khoá ở chế độ chỉ đọc", "P1",
         "Màn Xem chi tiết",
         "1. Vào tab Điểm danh ở màn Xem\n2. Thử nhập ô Ghi chú",
         "Màn: Xem",
         "- Ô Ghi chú không nhập được"),
        ("007", "Điểm danh độc lập từng dòng", "P1",
         "Cuộc họp có 3 người, đang Sửa 'Đã chốt lịch'",
         "1. Dòng 1 → 'Có mặt'\n2. Dòng 2 → 'Vắng có lý do'\n3. Dòng 3 → giữ nguyên",
         "—",
         "- Dòng 1 'Có mặt', dòng 2 'Vắng có lý do', dòng 3 vẫn 'Dự kiến tham gia'; không ảnh hưởng lẫn nhau"),
    ]),
    ("IV", "ĐIỂM DANH NHANH — TẤT CẢ CÓ MẶT", [
        ("001", "Nút 'Điểm danh nhanh' đặt tất cả thành 'Có mặt'", "P0",
         "Đang Sửa cuộc họp 'Đã chốt lịch', 3 người ở các trạng thái khác nhau",
         "1. Bấm 'Điểm danh nhanh: Tất cả có mặt'",
         "3 người trạng thái khác nhau",
         "- Tất cả các dòng chuyển sang 'Có mặt'"),
        ("002", "Nút 'Điểm danh nhanh' chỉ hiện khi được phép điểm danh", "P1",
         "So sánh màn Sửa 'Đã chốt lịch' và màn Xem",
         "1. Xem màn Sửa 'Đã chốt lịch'\n2. Xem màn Xem",
         "—",
         "- Màn Sửa 'Đã chốt lịch': có nút\n- Màn Xem hoặc trạng thái khác: ẩn nút"),
    ]),
    ("V", "CHẾ ĐỘ XEM — HIỂN THỊ TRẠNG THÁI DẠNG CHỮ", [
        ("001", "Hiển thị 'Có mặt' màu xanh", "P1",
         "Màn Xem, một người 'Có mặt'",
         "1. Vào tab Điểm danh màn Xem",
         "Trạng thái: Có mặt",
         "- Chữ 'Có mặt' màu xanh"),
        ("002", "Hiển thị 'Vắng…' màu đỏ", "P1",
         "Màn Xem, có người 'Vắng có lý do' và 'Vắng không lý do'",
         "1. Vào tab Điểm danh màn Xem",
         "—",
         "- 'Vắng có lý do' và 'Vắng không lý do' đều màu đỏ"),
        ("003", "Hiển thị 'Dự kiến tham gia' cho người chưa điểm danh", "P1",
         "Màn Xem, một người chưa điểm danh",
         "1. Vào tab Điểm danh màn Xem",
         "Trạng thái: Dự kiến tham gia",
         "- Chữ 'Dự kiến tham gia' màu xám, in nghiêng"),
    ]),
    ("VI", "ĐIỀU KIỆN HOÀN THÀNH CUỘC HỌP", [
        ("001", "Chặn Hoàn thành khi còn người chưa điểm danh", "P0",
         "Đang Sửa 'Đã chốt lịch', đã có biên bản, còn ≥1 người 'Dự kiến tham gia'",
         "1. Bấm nút 'Hoàn thành'",
         "1 người chưa điểm danh, đã có biên bản",
         "- Thông báo: 'Vui lòng hoàn thành điểm danh cho tất cả thành viên trước khi chốt biên bản và hoàn thành cuộc họp.'\n- Tự chuyển sang tab 'Điểm danh'\n- Cuộc họp KHÔNG chuyển sang 'Đã hoàn thành'"),
        ("002", "Cho Hoàn thành khi đã điểm danh đủ + có biên bản", "P0",
         "Đang Sửa 'Đã chốt lịch', đã có biên bản, mọi người đã điểm danh",
         "1. Bấm 'Hoàn thành'",
         "Điểm danh đủ, đã có biên bản",
         "- Không báo lỗi điểm danh\n- Cuộc họp chuyển sang 'Đã hoàn thành'"),
        ("003", "Chặn Hoàn thành khi chưa có biên bản (ưu tiên trước điểm danh)", "P1",
         "Đang Sửa 'Đã chốt lịch', CHƯA có biên bản",
         "1. Bấm 'Hoàn thành'",
         "Chưa có biên bản",
         "- Thông báo: 'Vui lòng thêm biên bản cuộc họp trước khi hoàn thành!'\n- Tự chuyển sang tab 'Biên bản'\n- Chưa kiểm tra điểm danh ở bước này"),
        ("004", "Bỏ qua giao diện, Hoàn thành khi còn người chưa điểm danh", "P0",
         "Dùng công cụ kiểm thử gọi thẳng chức năng Hoàn thành cuộc họp, còn người chưa điểm danh",
         "1. Gọi thẳng chức năng Hoàn thành, một người còn 'Dự kiến tham gia'",
         "1 người chưa điểm danh",
         "- Hệ thống từ chối, báo phải hoàn thành điểm danh cho tất cả thành viên; không chuyển 'Đã hoàn thành'"),
        ("005", "Bỏ qua giao diện, Hoàn thành khi đã điểm danh đủ", "P0",
         "Gọi thẳng chức năng Hoàn thành, mọi người đã điểm danh",
         "1. Gọi thẳng chức năng Hoàn thành khi điểm danh đủ + có biên bản",
         "Điểm danh đủ",
         "- Qua điều kiện, cuộc họp chuyển sang 'Đã hoàn thành'"),
    ]),
    ("VII", "LƯU TRỮ DỮ LIỆU & EDGE CASE", [
        ("001", "Lưu giữ trạng thái điểm danh sau khi mở lại", "P0",
         "Đang Sửa 'Đã chốt lịch'; điểm danh A='Có mặt', B='Vắng có lý do' + ghi chú",
         "1. Điểm danh như trên\n2. Lưu cuộc họp (giữ 'Đã chốt lịch')\n3. Mở lại Chi tiết",
         "A: Có mặt; B: Vắng có lý do, ghi chú 'Bận'",
         "- Mở lại: A 'Có mặt', B 'Vắng có lý do' kèm ghi chú 'Bận'"),
        ("002", "Người giữ 'Dự kiến tham gia' vẫn lưu đúng", "P0",
         "Đang Sửa 'Đã chốt lịch', một người giữ 'Dự kiến tham gia'",
         "1. Lưu cuộc họp\n2. Mở lại tab Điểm danh",
         "Một người: Dự kiến tham gia",
         "- Mở lại vẫn hiển thị 'Dự kiến tham gia' cho người đó"),
        ("003", "Xoá một thành viên ở tab Thông tin rồi lưu", "P1",
         "Cuộc họp 'Đã chốt lịch' có 3 người đã điểm danh; xoá 1 người ở tab Thông tin",
         "1. Xoá 1 người ở tab Thông tin\n2. Lưu\n3. Vào lại tab Điểm danh",
         "Còn 2 người",
         "- Tab Điểm danh còn 2 người, trạng thái điểm danh của họ giữ nguyên"),
        ("004", "Nội bộ và khách hàng lưu đúng thành phần", "P1",
         "Cuộc họp 'Đã chốt lịch', điểm danh cả nội bộ + khách hàng rồi lưu",
         "1. Điểm danh A (nội bộ)='Có mặt', K (khách hàng)='Vắng có lý do'\n2. Lưu\n3. Mở lại",
         "—",
         "- A hiển thị nhãn 'Nội bộ' trạng thái 'Có mặt'; K nhãn 'Khách hàng' trạng thái 'Vắng có lý do'"),
    ]),
]

build(output_file=OUTPUT_FILE, sheet_name=SHEET_NAME, feature_name=FEATURE_NAME,
      module_name=MODULE_NAME, description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
