# -*- coding: utf-8 -*-
"""Sinh testcase cho phần QUẢN LÝ DANH SÁCH NGƯỜI THAM GIA của màn Meeting (Redmine #10534).

Khối 'Thành phần — Phía Công ty' + 'Thành phần — Phía Khách hàng' trong tab Thông tin của màn
Tạo / Sửa / Xem chi tiết meeting. Viết bằng ngôn ngữ nghiệp vụ cho QA.
"""
import os
import sys

# Nạp engine dựng Excel chuẩn team
sys.path.insert(0, r"D:\CompanyProject\hrm-cursor\.claude\skills\testcase-documenter\assets")
from tc_engine import build  # noqa: E402

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "testcase - Quản lý danh sách người tham gia.xlsx")
SHEET_NAME = "NguoiThamGia"
FEATURE_NAME = "Quản lý danh sách người tham gia Meeting"
MODULE_NAME = "Người tham gia Meeting"

# =========================================================================
# 9 MỤC MÔ TẢ
# =========================================================================
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Cho phép người lập/sửa cuộc họp quản lý danh sách người tham gia ngay tại tab 'Thông tin':\n"
     "► Khối 'Thành phần — Phía Công ty': chọn nhân viên nội bộ từ popup danh bạ nhân sự.\n"
     "► Khối 'Thành phần — Phía Khách hàng': tự nhập tay họ tên / chức vụ / SĐT của khách mời.\n"
     "Danh sách này là nguồn cho tab 'Điểm danh' và cho phần Thành phần tham gia khi in biên bản."),
    ("2. Đối tượng được hiển thị",
     "► Khối 'Thành phần — Phía Công ty': LUÔN hiển thị (mọi loại họp).\n"
     "► Khối 'Thành phần — Phía Khách hàng': CHỈ hiển thị khi loại meeting đang chọn là loại có "
     "khách hàng (phân loại 'Họp đối tác').\n"
     "► Bảng Công ty gồm cột: STT, Họ tên, Chức vụ, SĐT.\n"
     "► Bảng Khách hàng gồm cột: STT, Họ tên, Chức vụ, SĐT (các ô nhập tay)."),
    ("3. Đối tượng bị ẩn / không hiển thị",
     "► Khối Khách hàng bị ẩn khi loại meeting là loại họp nội bộ (không gắn khách hàng).\n"
     "► Đổi từ loại 'Họp đối tác' sang loại họp nội bộ: hệ thống xoá danh sách khách mời đã nhập "
     "(trừ trường hợp meeting gắn dự án — vẫn giữ khách hàng kế thừa từ dự án).\n"
     "► Bảng chưa có ai: hiện dòng trống 'Chưa có thành viên nào', không hiện bảng."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "— Không áp dụng. Khối người tham gia không có bộ lọc theo thời gian.\n"
     "► Popup 'Chọn nhân viên phía công ty' có bộ lọc riêng theo: tên/mã nhân viên (ô tìm nhanh), "
     "Công ty, Phòng ban, Bộ phận, Chức vụ, Chức danh."),
    ("5. Cấu trúc dữ liệu",
     "► Mỗi cuộc họp có 2 danh sách tách biệt: thành viên Công ty và thành viên Khách hàng.\n"
     "► Thành viên Công ty gắn với một nhân viên có sẵn trong hệ thống (tự điền tên/chức vụ/SĐT theo "
     "hồ sơ). Thành viên Khách hàng là dòng nhập tay tự do.\n"
     "► Thứ tự các dòng do người dùng sắp bằng thao tác kéo-thả, được lưu lại."),
    ("6. Quy tắc chống trùng",
     "► Thêm nhân viên công ty đã có sẵn trong danh sách: hệ thống bỏ qua, KHÔNG tạo dòng trùng.\n"
     "► Trong popup chọn nhân viên: nhân viên đã có trong danh sách hiển thị mờ và không tick lại được.\n"
     "► Người liên hệ đã chọn ở khối Khách hàng & Người liên hệ có thể được tự động đưa xuống danh "
     "sách thành viên khách hàng."),
    ("7. Phân quyền",
     "► Nhóm quyền 'Quản lý meeting' chỉ có quyền XEM theo cấp tổ chức:\n"
     "   - Xem danh sách meeting theo tổng công ty\n"
     "   - Xem danh sách meeting theo công ty\n"
     "   - Xem danh sách meeting theo phòng ban\n"
     "   - Xem danh sách meeting theo bộ phận\n"
     "► KHÔNG có quyền riêng cho thao tác thêm/xoá người tham gia — quyền này đi kèm quyền mở màn "
     "Tạo/Sửa meeting. Có ít nhất một trong bốn quyền trên mới vào được menu Quản lý meeting."),
    ("8. Cách tính các ô thống kê",
     "— Không có ô thống kê dạng số ở khối người tham gia.\n"
     "► Cột STT tự đánh số lại 1,2,3… theo thứ tự dòng hiện tại của từng bảng.\n"
     "► Popup hiển thị 'Tổng: N nhân viên' = tổng số nhân viên khớp bộ lọc, và badge 'n đã chọn' = "
     "số nhân viên đang được tick."),
    ("9. Ghi chú đọc bảng",
     "► Bắt buộc có ít nhất một thành viên Công ty mới lưu được cuộc họp.\n"
     "► Họ tên thành viên Khách hàng là bắt buộc; SĐT nếu nhập phải đúng định dạng (bắt đầu bằng số 0, "
     "gồm 10–12 chữ số).\n"
     "► Ở màn Xem chi tiết: mọi nút thêm/xoá và tay cầm kéo-thả đều ẩn, danh sách chỉ đọc.\n"
     "► Kéo-thả chỉ đổi thứ tự trong CÙNG một bảng, không kéo người từ bảng Công ty sang bảng Khách "
     "hàng và ngược lại."),
]

# =========================================================================
# PHÂN QUYỀN & TRUY CẬP
# =========================================================================
ROLE_TCS = [
    ("01", "Có quyền 'Xem danh sách meeting theo tổng công ty' → vào menu Quản lý meeting và mở màn tạo/sửa",
     "P0",
     "Tài khoản chỉ được gán quyền 'Xem danh sách meeting theo tổng công ty'",
     "1. Đăng nhập\n2. Mở menu Quản lý meeting\n3. Vào một cuộc họp, bấm Sửa\n4. Quan sát khối Thành phần tham gia",
     "Quyền: Xem danh sách meeting theo tổng công ty",
     "- Menu Quản lý meeting hiển thị và mở được\n- Trong màn Sửa: khối Thành phần — Phía Công ty có nút thêm (+); thao tác thêm/xoá người tham gia dùng được bình thường"),
    ("02", "Có quyền xem theo phòng ban → chỉ thấy meeting trong phạm vi, thao tác người tham gia bình thường",
     "P1",
     "Tài khoản chỉ có quyền 'Xem danh sách meeting theo phòng ban'",
     "1. Đăng nhập\n2. Mở menu Quản lý meeting\n3. Sửa một cuộc họp thuộc phòng ban mình",
     "Quyền: Xem danh sách meeting theo phòng ban",
     "- Chỉ thấy các cuộc họp thuộc phạm vi phòng ban\n- Mở Sửa và thao tác thêm/xoá người tham gia bình thường"),
    ("03", "Không có quyền nào trong nhóm Quản lý meeting → không vào được menu",
     "P0",
     "Tài khoản không được gán bất kỳ quyền 'Xem danh sách meeting…' nào",
     "1. Đăng nhập\n2. Tìm menu Quản lý meeting",
     "Quyền: (không có)",
     "- Menu Quản lý meeting KHÔNG hiển thị / không truy cập được\n- Không xem hay sửa được danh sách người tham gia của cuộc họp nào"),
    ("04", "Bỏ qua giao diện, gọi thẳng chức năng Lưu khi danh sách thành viên công ty rỗng",
     "P0",
     "Dùng công cụ kiểm thử gọi thẳng chức năng Lưu cuộc họp (bỏ qua giao diện), gửi danh sách thành viên công ty rỗng",
     "1. Gọi thẳng chức năng Lưu với danh sách thành viên Công ty để trống",
     "Thành viên Công ty: (rỗng)",
     "- Hệ thống từ chối lưu, báo bắt buộc phải có ít nhất một thành viên công ty\n- Cuộc họp không được tạo/cập nhật (chốt chặn không chỉ nằm ở giao diện)"),
]

# =========================================================================
# SECTIONS NGHIỆP VỤ
# =========================================================================
SECTIONS = [
    ("I", "HIỂN THỊ KHỐI THÀNH PHẦN THAM GIA", [
        ("001", "Khối 'Thành phần — Phía Công ty' luôn hiển thị", "P0",
         "Mở màn Tạo meeting mới",
         "1. Vào màn Tạo meeting\n2. Quan sát cột bên phải tab Thông tin",
         "—",
         "- Hiển thị khối tiêu đề 'Thành phần — Phía Công ty' kèm nút thêm (+)\n- Bảng có các cột: STT, Họ tên, Chức vụ, SĐT"),
        ("002", "Khối 'Thành phần — Phía Khách hàng' hiện khi chọn loại họp có khách hàng", "P0",
         "Màn Tạo meeting, phân loại 'Họp đối tác'",
         "1. Chọn phân loại 'Họp đối tác'\n2. Chọn một Loại meeting thuộc nhóm có khách hàng\n3. Quan sát",
         "Phân loại: Họp đối tác",
         "- Hiện thêm khối 'Thành phần — Phía Khách hàng' với nút thêm (+) và các cột STT, Họ tên, Chức vụ, SĐT"),
        ("003", "Khối Khách hàng bị ẩn với loại họp nội bộ", "P0",
         "Màn Tạo meeting",
         "1. Chọn phân loại 'Họp nội bộ' (hoặc loại meeting không gắn khách hàng)\n2. Quan sát",
         "Phân loại: Họp nội bộ",
         "- KHÔNG hiển thị khối 'Thành phần — Phía Khách hàng'\n- Vẫn hiển thị khối 'Thành phần — Phía Công ty'"),
        ("004", "Bảng trống hiển thị dòng 'Chưa có thành viên nào'", "P1",
         "Màn Tạo meeting, chưa thêm ai vào bảng Công ty",
         "1. Quan sát khối 'Thành phần — Phía Công ty' khi chưa thêm ai",
         "—",
         "- Hiển thị dòng 'Chưa có thành viên nào', không hiển thị bảng dữ liệu"),
        ("005", "Đổi từ loại họp đối tác sang loại họp nội bộ → xoá danh sách khách mời", "P1",
         "Đang tạo meeting loại có khách hàng, đã nhập 2 khách mời",
         "1. Nhập 2 khách mời ở bảng Khách hàng\n2. Đổi Loại meeting sang loại họp nội bộ\n3. Quan sát",
         "Bảng Khách hàng: 2 dòng đã nhập",
         "- Khối Khách hàng ẩn đi và danh sách khách mời bị xoá\n⚠️ Ngoại lệ: nếu cuộc họp gắn dự án thì khách hàng kế thừa từ dự án vẫn được giữ"),
    ]),
    ("II", "THÊM NHÂN SỰ CÔNG TY QUA POPUP", [
        ("001", "Mở popup 'Chọn nhân viên phía công ty' từ nút thêm (+)", "P0",
         "Màn Tạo/Sửa meeting",
         "1. Bấm nút (+) ở khối 'Thành phần — Phía Công ty'",
         "—",
         "- Mở cửa sổ 'Chọn nhân viên phía công ty'\n- Có ô tìm nhanh 'Tìm theo tên, mã nhân viên'\n- Bảng nhân viên có cột Họ tên, Phòng ban, Email, SĐT"),
        ("002", "Tìm nhanh theo tên/mã nhân viên", "P0",
         "Đã mở popup chọn nhân viên",
         "1. Gõ tên hoặc mã nhân viên vào ô tìm nhanh\n2. Nhấn Enter hoặc bấm Tìm kiếm",
         "Từ khoá: 'Nguyễn'",
         "- Danh sách chỉ còn nhân viên có tên/mã khớp từ khoá\n⚠️ Chỉ gõ chưa tìm — phải nhấn Enter hoặc nút Tìm kiếm mới lọc; bấm X xoá từ khoá thì tìm lại ngay"),
        ("003", "Lọc nâng cao theo Công ty / Phòng ban / Bộ phận / Chức vụ / Chức danh", "P1",
         "Đã mở popup, mở panel tìm kiếm nâng cao",
         "1. Mở phần tìm kiếm nâng cao\n2. Chọn Phòng ban và Chức vụ\n3. Xem kết quả",
         "Phòng ban: Kỹ thuật; Chức vụ: Nhân viên",
         "- Danh sách chỉ còn nhân viên khớp Phòng ban + Chức vụ đã chọn"),
        ("004", "Chọn nhiều nhân viên bằng ô tick rồi Thêm", "P0",
         "Đã mở popup, danh sách có nhiều nhân viên",
         "1. Tick 3 nhân viên\n2. Quan sát badge số đã chọn và nút Thêm\n3. Bấm 'Thêm thành viên (3)'",
         "Tick 3 nhân viên",
         "- Badge hiện '3 đã chọn'\n- Nút ghi 'Thêm thành viên (3)'\n- Bấm xong: popup đóng, bảng Công ty có thêm đúng 3 dòng vừa chọn"),
        ("005", "Nút Thêm chỉ hiện khi đã tick ít nhất một người", "P2",
         "Đã mở popup, chưa tick ai",
         "1. Quan sát khu vực nút khi chưa tick\n2. Tick 1 người rồi quan sát lại",
         "—",
         "- Khi chưa tick: chỉ có nút 'Đóng'\n- Khi đã tick: xuất hiện nút 'Thêm thành viên (n)'"),
        ("006", "Chọn tất cả nhân viên theo bộ lọc (mọi trang)", "P0",
         "Đã mở popup, bộ lọc cho ra nhiều trang kết quả (ví dụ 45 nhân viên, 10 dòng/trang)",
         "1. Tick ô 'Chọn tất cả' ở đầu bảng\n2. Quan sát số đã chọn\n3. Bấm Thêm",
         "45 nhân viên khớp bộ lọc",
         "- Tick chọn TẤT CẢ nhân viên khớp bộ lọc trên MỌI trang, không chỉ trang đang xem\n- Badge hiện đúng tổng số\n- Bấm Thêm: tất cả được đưa vào bảng Công ty (trừ người đã có sẵn)"),
        ("007", "Đổi số dòng/trang và chuyển trang trong popup", "P2",
         "Đã mở popup, tổng nhân viên > 10",
         "1. Đổi số dòng mỗi trang sang 25\n2. Chuyển sang trang 2",
         "Số dòng/trang: 25",
         "- Danh sách hiển thị 25 dòng/trang\n- Chuyển trang hoạt động, dòng 'Tổng: N nhân viên' đúng tổng khớp bộ lọc"),
        ("008", "Nhân viên đã có trong danh sách bị mờ, không tick lại được", "P1",
         "Bảng Công ty đã có nhân viên A; mở lại popup",
         "1. Mở lại popup\n2. Tìm nhân viên A\n3. Thử tick A",
         "Nhân viên A đã có trong danh sách",
         "- Dòng nhân viên A hiển thị mờ và không tick được (đã có trong danh sách)"),
    ]),
    ("III", "CHỐNG TRÙNG & TỰ ĐIỀN THÔNG TIN NHÂN SỰ CÔNG TY", [
        ("001", "Thông tin nhân viên tự điền theo hồ sơ", "P1",
         "Vừa thêm một nhân viên công ty",
         "1. Thêm 1 nhân viên qua popup\n2. Quan sát dòng vừa thêm ở bảng Công ty",
         "—",
         "- Cột Họ tên, Chức vụ, SĐT tự điền theo hồ sơ nhân viên\n- Thiếu chức vụ/SĐT thì hiển thị dấu '-'"),
        ("002", "Thêm lại nhân viên đã có không tạo dòng trùng", "P0",
         "Bảng Công ty đã có nhân viên A",
         "1. Mở popup, cố thêm lại A (nếu tick được qua thao tác khác)\n2. Bấm Thêm\n3. Quan sát bảng",
         "Nhân viên A đã có sẵn",
         "- Nhân viên A vẫn chỉ xuất hiện MỘT dòng, không bị nhân đôi"),
    ]),
    ("IV", "THÊM / SỬA NHÂN SỰ KHÁCH HÀNG (NHẬP TAY)", [
        ("001", "Thêm dòng khách mời bằng nút (+)", "P0",
         "Màn Tạo meeting loại có khách hàng",
         "1. Bấm nút (+) ở khối 'Thành phần — Phía Khách hàng'",
         "—",
         "- Thêm một dòng trống ở CUỐI bảng gồm 3 ô: Họ tên, Chức vụ, SĐT để nhập tay"),
        ("002", "Nhập họ tên / chức vụ / SĐT khách mời", "P0",
         "Đã có một dòng khách mời trống",
         "1. Nhập Họ tên, Chức vụ, SĐT hợp lệ\n2. Lưu cuộc họp",
         "Họ tên: Trần Văn B; Chức vụ: Giám đốc; SĐT: 0901234567",
         "- Nhập được đủ 3 ô\n- Lưu thành công, mở lại thấy đúng dòng khách mời vừa nhập"),
        ("003", "Người liên hệ đã chọn được tự đưa xuống danh sách khách mời", "P1",
         "Đã chọn khách hàng và một người liên hệ ở khối 'Khách hàng & Người liên hệ'",
         "1. Chọn/Thêm nhanh một người liên hệ\n2. Quan sát bảng 'Thành phần — Phía Khách hàng'",
         "Người liên hệ: Lê Thị C",
         "- Người liên hệ Lê Thị C được tự thêm thành một dòng khách mời (theo ghi chú '* Mặc định có thể thêm người liên hệ đã chọn ở trên.')"),
    ]),
    ("V", "XOÁ THÀNH VIÊN", [
        ("001", "Xoá một thành viên công ty", "P0",
         "Bảng Công ty có 3 người",
         "1. Bấm nút thùng rác ở dòng thứ 2\n2. Quan sát bảng",
         "Xoá dòng số 2",
         "- Dòng số 2 bị xoá, còn 2 người\n- Cột STT đánh số lại 1, 2"),
        ("002", "Xoá một thành viên khách hàng", "P1",
         "Bảng Khách hàng có 2 người",
         "1. Bấm nút thùng rác ở một dòng khách mời",
         "—",
         "- Dòng khách mời bị xoá khỏi bảng, STT đánh số lại"),
        ("003", "Xoá hết thành viên công ty rồi lưu bị chặn", "P0",
         "Bảng Công ty còn 1 người",
         "1. Xoá người cuối cùng ở bảng Công ty\n2. Bấm Lưu (Lưu nháp / Lưu và Lên lịch / Lưu và Chốt lịch)",
         "Bảng Công ty: rỗng sau khi xoá",
         "- Hệ thống báo lỗi yêu cầu phải có ít nhất một thành viên công ty\n- Cuộc họp không được lưu cho tới khi thêm lại"),
    ]),
    ("VI", "KÉO-THẢ ĐỔI THỨ TỰ", [
        ("001", "Kéo đổi thứ tự trong bảng Công ty", "P1",
         "Bảng Công ty có 3 người theo thứ tự A, B, C",
         "1. Giữ tay cầm kéo ở dòng C, kéo lên đầu\n2. Quan sát",
         "Kéo C lên đầu",
         "- Thứ tự thành C, A, B; cột STT cập nhật 1, 2, 3\n- Thứ tự này được giữ khi lưu và mở lại"),
        ("002", "Kéo đổi thứ tự trong bảng Khách hàng", "P2",
         "Bảng Khách hàng có 2 người",
         "1. Kéo dòng 2 lên trên dòng 1",
         "—",
         "- Đổi thứ tự trong bảng Khách hàng, STT cập nhật"),
        ("003", "Không kéo được người giữa 2 bảng", "P1",
         "Cả 2 bảng đều có người",
         "1. Thử kéo một người từ bảng Công ty sang bảng Khách hàng",
         "—",
         "- Không thả được sang bảng còn lại; mỗi bảng chỉ đổi thứ tự trong nội bộ nó"),
    ]),
    ("VII", "RÀNG BUỘC NHẬP LIỆU & LƯU", [
        ("001", "Bắt buộc có ít nhất một thành viên công ty", "P0",
         "Màn Tạo meeting, bảng Công ty rỗng, các trường khác hợp lệ",
         "1. Không thêm thành viên công ty nào\n2. Bấm Lưu",
         "Bảng Công ty: rỗng",
         "- Hệ thống báo lỗi yêu cầu thêm ít nhất một thành viên công ty ngay tại khối Thành phần — Phía Công ty\n- Không lưu được"),
        ("002", "Bắt buộc nhập Họ tên khách mời", "P0",
         "Bảng Khách hàng có 1 dòng để trống Họ tên",
         "1. Thêm dòng khách mời nhưng bỏ trống Họ tên\n2. Bấm Lưu",
         "Họ tên khách mời: (trống)",
         "- Báo lỗi đỏ ngay dưới ô Họ tên của dòng đó, yêu cầu nhập họ tên\n- Không lưu được cho tới khi nhập"),
        ("003", "SĐT khách mời sai định dạng bị báo lỗi", "P1",
         "Bảng Khách hàng có 1 dòng, SĐT sai định dạng",
         "1. Nhập SĐT '12abc'\n2. Bấm Lưu",
         "SĐT: 12abc",
         "- Báo lỗi đỏ dưới ô SĐT: số phải bắt đầu bằng 0 và gồm 10–12 chữ số\n- Không lưu được"),
        ("004", "SĐT khách mời để trống vẫn lưu được", "P2",
         "Bảng Khách hàng có 1 dòng đủ Họ tên, bỏ trống SĐT",
         "1. Nhập Họ tên, để trống SĐT\n2. Bấm Lưu",
         "SĐT: (trống)",
         "- Lưu thành công (SĐT không bắt buộc)"),
        ("005", "Danh sách người tham gia được giữ nguyên sau khi lưu và mở lại", "P0",
         "Đã thêm 2 nhân viên công ty + 1 khách mời",
         "1. Lưu cuộc họp\n2. Mở lại màn Chi tiết/Sửa cuộc họp\n3. Quan sát 2 bảng",
         "2 nhân viên công ty + 1 khách mời",
         "- Cả 2 bảng hiển thị đúng người, đúng thứ tự đã sắp, đúng thông tin đã nhập"),
    ]),
    ("VIII", "CHẾ ĐỘ XEM (READONLY)", [
        ("001", "Màn Xem chi tiết ẩn mọi nút thao tác người tham gia", "P0",
         "Mở màn Xem chi tiết một cuộc họp đã có người tham gia",
         "1. Mở Chi tiết cuộc họp (không phải Sửa)\n2. Quan sát 2 khối Thành phần",
         "—",
         "- Ẩn nút thêm (+), nút thùng rác và tay cầm kéo-thả\n- Danh sách hiển thị chỉ đọc, không sửa được"),
        ("002", "Vào màn Sửa bằng đường dẫn trực tiếp khi không được phép", "P2",
         "Cuộc họp ở trạng thái không cho sửa (ví dụ đã hoàn thành)",
         "1. Mở màn Sửa cuộc họp\n2. Quan sát khối người tham gia",
         "Trạng thái: Đã hoàn thành",
         "- Danh sách người tham gia ở chế độ chỉ đọc, không thêm/xoá/kéo được"),
    ]),
    ("IX", "CÔ LẬP DỮ LIỆU & BYPASS GIAO DIỆN", [
        ("001", "Bỏ qua giao diện, lưu với thành viên công ty rỗng", "P0",
         "Dùng công cụ kiểm thử gọi thẳng chức năng Lưu cuộc họp, bỏ danh sách thành viên công ty",
         "1. Gọi thẳng chức năng Lưu với danh sách thành viên công ty rỗng",
         "Thành viên công ty: (rỗng)",
         "- Hệ thống từ chối, báo bắt buộc có ít nhất một thành viên công ty (chốt chặn không chỉ ở giao diện)"),
        ("002", "Bỏ qua giao diện, lưu khách mời có SĐT sai định dạng", "P1",
         "Gọi thẳng chức năng Lưu với một khách mời SĐT sai định dạng",
         "1. Gọi thẳng chức năng Lưu, khách mời có SĐT 'abc123'",
         "SĐT khách mời: abc123",
         "- Hệ thống từ chối, báo SĐT sai định dạng, không lưu"),
        ("003", "Bỏ qua giao diện, lưu khách mời thiếu Họ tên", "P1",
         "Gọi thẳng chức năng Lưu với một khách mời không có Họ tên",
         "1. Gọi thẳng chức năng Lưu, khách mời để trống Họ tên",
         "Họ tên khách mời: (trống)",
         "- Hệ thống từ chối, báo bắt buộc nhập họ tên khách mời"),
    ]),
]

build(output_file=OUTPUT_FILE, sheet_name=SHEET_NAME, feature_name=FEATURE_NAME,
      module_name=MODULE_NAME, description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS, sections=SECTIONS)
