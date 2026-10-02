# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho màn Danh mục Lĩnh vực Công ty kinh doanh (Redmine #11184).

Chạy:  python .plans/linh-vuc-kinh-doanh-noi-bo/gen_testcase.py
Nhánh code tham chiếu: tpe-develop-assign (chưa có trường "Thời gian hiệu lực nhu cầu").
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
# .plans/<feature>/ -> .plans/ -> HRM/ ; skill nằm ở HRM/.claude/skills/...
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", ".claude", "skills",
                                       "testcase-documenter", "assets"))
sys.path.insert(0, ASSETS)

from tc_engine import build  # noqa: E402

FEATURE = "Danh mục Lĩnh vực Công ty kinh doanh - Cập nhật ngày 15/09/2026"
MODULE = "DM Lĩnh vực Cty kinh doanh"
OUT = os.path.join(HERE, "testcase.xlsx")

P_MANAGE = "Quản lý danh mục lĩnh vực Công ty kinh doanh"
P_VIEW = "Xem danh mục lĩnh vực Công ty kinh doanh"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý danh mục Lĩnh vực Công ty kinh doanh (lĩnh vực mà công ty đang kinh doanh) dùng cho phân hệ "
     "Dự án & Giao việc. Cho phép Tạo mới / Sửa / Xem / Khoá - Mở khoá / Xoá, tìm kiếm - lọc, Xuất Excel và "
     "Import Excel.\n"
     "Đường vào: menu Danh mục › Lĩnh vực Công ty kinh doanh (đứng ngay trên mục Nhóm ngành).\n"
     "Mỗi Nhóm ngành bắt buộc thuộc 1 lĩnh vực ở danh mục này, nên dữ liệu ở đây ảnh hưởng trực tiếp tới "
     "màn Nhóm ngành."),

    ("2. Đối tượng được tính / hiển thị",
     "Bảng liệt kê TẤT CẢ lĩnh vực đã tạo, không phân biệt người tạo, không giới hạn theo công ty / phòng ban / "
     "bộ phận (danh mục dùng chung toàn hệ thống):\n"
     "- Trạng thái Hoạt động: hiện đủ các thao tác Sửa, Khoá, Xoá (tuỳ điều kiện từng dòng).\n"
     "- Trạng thái Khoá: vẫn hiện trong bảng, chỉ còn thao tác Mở khoá.\n"
     "Ô chọn lĩnh vực ở các màn khác (ví dụ Nhóm ngành) chỉ liệt kê lĩnh vực đang Hoạt động, RIÊNG lĩnh vực đang "
     "được bản ghi đó chọn thì vẫn hiện dù đã Khoá, kèm biểu tượng ổ khoá phía trước tên."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Không ẩn bản ghi nào khỏi bảng danh sách (kể cả bản ghi đã Khoá).\n"
     "- Nút bị ẩn (KHÔNG hiện mờ) theo điều kiện: Tạo mới / Import Excel ẩn với tài khoản chỉ có quyền xem; "
     "Sửa và Xoá ẩn khi bản ghi đang Khoá; Xoá còn ẩn khi lĩnh vực đang được ít nhất 1 Nhóm ngành sử dụng; "
     "Khoá ẩn khi còn Nhóm ngành ĐANG HOẠT ĐỘNG thuộc lĩnh vực đó.\n"
     "- Mục menu Lĩnh vực Công ty kinh doanh không hiện với tài khoản không có quyền nào trong 2 quyền ở mục 7."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô 'Cập nhật từ' và 'Cập nhật đến' lọc theo cột NGÀY CẬP NHẬT của bản ghi (so theo NGÀY, bỏ giờ), lấy cả "
     "hai đầu mút. Không có bộ lọc theo Ngày tạo.\n"
     "Định dạng nhập và hiển thị: dd/mm/yyyy. Cột Ngày tạo / Ngày cập nhật trong bảng hiển thị dạng "
     "dd/mm/yyyy hh:mm (không có giây)."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh mục 1 cấp, mỗi bản ghi gồm: Mã, Tên lĩnh vực Công ty kinh doanh, Trạng thái, Người tạo, Ngày tạo, "
     "Người cập nhật, Ngày cập nhật.\n"
     "Quan hệ xuống dưới: 1 Lĩnh vực có nhiều Nhóm ngành; Nhóm ngành lại có Nhóm giải pháp và Ứng dụng. Vì vậy "
     "Xoá / Khoá bị chặn khi tuyến dưới còn dùng.\n"
     "Không có màn chi tiết riêng: bấm vào MÃ ở cột đầu để mở cửa sổ Xem; Sửa mở cùng cửa sổ ở chế độ nhập."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "Không có cộng dồn. Quy tắc chống trùng:\n"
     "- Mã không được trùng với bản ghi khác (so sánh không phân biệt chữ hoa - thường, vì mã luôn được lưu dạng "
     "chữ HOA).\n"
     "- Tên không được trùng với bản ghi khác; hệ thống kiểm tra khi bấm Lưu.\n"
     "- Trong 1 file Import: trùng mã hoặc trùng tên giữa các dòng trong file cũng bị báo lỗi, có chỉ rõ trùng với "
     "dòng số mấy."),

    ("7. Phân quyền cấp",
     "Hai quyền phẳng, không phân quyền theo công ty / phòng ban / bộ phận:\n"
     "- \"%s\": xem danh sách + Tạo mới, Sửa, Xoá, Khoá / Mở khoá, Xuất Excel, Import Excel.\n"
     "- \"%s\": chỉ xem danh sách, mở cửa sổ Xem và Xuất Excel.\n"
     "Tài khoản có cả 2 quyền hưởng quyền cao hơn (quản lý). Tài khoản không có quyền nào thì không thấy mục menu "
     "và bị chặn khi mở thẳng đường dẫn." % (P_MANAGE, P_VIEW)),

    ("8. Cách tính các ô thống kê",
     "Màn không có ô thống kê. Các số hiển thị trên bảng:\n"
     "- Cột STT = số thứ tự liên tục theo trang đang xem: trang 2 với cỡ trang 10 thì dòng đầu là 11.\n"
     "- Dòng 'Hiển thị a-b / N' dưới bảng: a là số thứ tự dòng đầu trang, b là dòng cuối trang, N là tổng số bản "
     "ghi khớp điều kiện lọc hiện tại.\n"
     "- Sau khi Import, thông báo 'Import thành công X/Y ...': X là số dòng ghi được, Y là tổng số dòng trong file."),

    ("9. Ghi chú đọc bảng",
     "Bẫy dễ sai của màn này, đọc trước khi test:\n"
     "- Ô Mã có phần tiền tố 'LVCTKD.' cố định, KHÔNG xoá được; người dùng chỉ gõ phần hậu tố tối đa 4 ký tự "
     "(A-Z, 0-9, gạch dưới). Chữ thường gõ vào sẽ được lưu thành chữ HOA.\n"
     "- File mẫu Import tải về phải ghi mã theo tiền tố MỚI 'LVCTKD.'; nếu còn thấy 'LVKDNB.' là sai (lỗi đã sửa "
     "ngày 15/09/2026) và import theo mẫu sẽ hỏng toàn bộ.\n"
     "- Nút không dùng được thì ẨN HẲN, không hiện mờ: đừng báo lỗi 'thiếu nút Sửa' khi bản ghi đang Khoá.\n"
     "- Bản ghi đang Khoá thì mọi thao tác đổi dữ liệu đều bị chặn, phải Mở khoá trước.\n"
     "- Ngày trên bảng là dd/mm/yyyy hh:mm; bộ lọc ngày chỉ so phần ngày.\n"
     "- Cửa sổ Tạo mới / Sửa không đóng khi còn lỗi: lỗi hiện đỏ ngay dưới từng ô, dữ liệu đã gõ vẫn còn nguyên."),
]

ROLE_TCS = [
    ("00", "Tài khoản có quyền quản lý thấy đủ thao tác", "P0",
     "Tài khoản A được cấp quyền \"%s\". Danh mục có sẵn 8 lĩnh vực, trong đó LVCTKD.KHAC đang Hoạt động và "
     "KHÔNG có nhóm ngành nào dùng." % P_MANAGE,
     "1. Đăng nhập bằng tài khoản A\n2. Vào menu Danh mục › Lĩnh vực Công ty kinh doanh\n3. Quan sát thanh nút "
     "phía trên bảng và cột Hành động của dòng LVCTKD.KHAC",
     "—",
     "- Mục menu Lĩnh vực Công ty kinh doanh hiện trong nhóm Danh mục\n"
     "- Bảng hiện đủ 8 dòng\n"
     "- Thanh nút có: Tạo mới, Xuất Excel, Import Excel\n"
     "- Dòng LVCTKD.KHAC có đủ 3 biểu tượng: Sửa, Khoá, Xoá"),

    ("01", "Tài khoản chỉ có quyền xem bị ẩn hết nút ghi dữ liệu", "P0",
     "Tài khoản B chỉ được cấp quyền \"%s\" (không có quyền quản lý). Danh mục có 8 lĩnh vực." % P_VIEW,
     "1. Đăng nhập bằng tài khoản B\n2. Vào menu Danh mục › Lĩnh vực Công ty kinh doanh\n3. Quan sát thanh nút và "
     "cột Hành động\n4. Bấm vào mã LVCTKD.KHAC ở cột đầu",
     "—",
     "- Vẫn xem được đủ 8 dòng\n"
     "- Thanh nút CHỈ còn Xuất Excel; không có Tạo mới, không có Import Excel\n"
     "- Cột Hành động trống ở mọi dòng (không có Sửa / Khoá / Xoá)\n"
     "- Bấm vào mã vẫn mở được cửa sổ \"Xem chi tiết lĩnh vực Công ty kinh doanh\", các ô đều khoá, chỉ có nút Đóng"),

    ("02", "Tài khoản không có quyền nào không vào được màn", "P0",
     "Tài khoản C không được cấp cả 2 quyền ở mục 7.",
     "1. Đăng nhập bằng tài khoản C\n2. Mở nhóm menu Danh mục, tìm mục Lĩnh vực Công ty kinh doanh\n3. Gõ thẳng "
     "đường dẫn màn danh sách lên thanh địa chỉ",
     "—",
     "- Không có mục menu Lĩnh vực Công ty kinh doanh\n"
     "- Vào bằng đường dẫn trực tiếp: hệ thống từ chối, báo không có quyền, bảng không hiện dữ liệu\n"
     "- ⚠️ Không được hiện bảng rỗng kèm thông báo 'Lỗi khi tải dữ liệu' như một lỗi hệ thống"),

    ("03", "Chặn Tạo mới khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản B chỉ có quyền \"%s\"." % P_VIEW,
     "1. Đăng nhập bằng tài khoản B\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Tạo mới lĩnh vực, bỏ qua giao "
     "diện\n3. Mở lại màn danh sách, tìm theo mã vừa gửi",
     "Mã: LVCTKD.BYP1 · Tên: Lĩnh vực thử vượt quyền",
     "- Hệ thống từ chối vì không có quyền\n- Danh sách KHÔNG xuất hiện bản ghi LVCTKD.BYP1"),

    ("04", "Chặn Sửa khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản B chỉ có quyền xem. Có bản ghi LVCTKD.KHAC - Khác.",
     "1. Đăng nhập bằng tài khoản B\n2. Gọi thẳng chức năng Sửa bản ghi LVCTKD.KHAC, bỏ qua giao diện\n3. Mở lại "
     "màn danh sách",
     "Tên mới: Khác (đã sửa lén)",
     "- Hệ thống từ chối vì không có quyền\n- Tên bản ghi vẫn là 'Khác', cột Ngày cập nhật không đổi"),

    ("05", "Chặn Xoá khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản B chỉ có quyền xem. Có bản ghi LVCTKD.TMP1 đang Hoạt động, chưa nhóm ngành nào dùng.",
     "1. Đăng nhập bằng tài khoản B\n2. Gọi thẳng chức năng Xoá bản ghi LVCTKD.TMP1, bỏ qua giao diện\n3. Mở lại "
     "màn danh sách",
     "—",
     "- Hệ thống từ chối vì không có quyền\n- Bản ghi LVCTKD.TMP1 vẫn còn trong danh sách"),

    ("06", "Chặn Khoá / Mở khoá khi gọi thẳng chức năng", "P1",
     "Tài khoản B chỉ có quyền xem. Có bản ghi LVCTKD.TMP1 đang Hoạt động.",
     "1. Đăng nhập bằng tài khoản B\n2. Gọi thẳng chức năng Khoá bản ghi LVCTKD.TMP1, bỏ qua giao diện\n3. Mở lại "
     "màn danh sách",
     "—",
     "- Hệ thống từ chối vì không có quyền\n- Trạng thái bản ghi vẫn là Hoạt động"),

    ("07", "Chặn Import khi gọi thẳng chức năng", "P1",
     "Tài khoản B chỉ có quyền xem.",
     "1. Đăng nhập bằng tài khoản B\n2. Gọi thẳng chức năng Import danh sách lĩnh vực, bỏ qua giao diện, gửi 1 dòng "
     "hợp lệ\n3. Mở lại màn danh sách",
     "Mã: LVCTKD.IMP9 · Tên: Lĩnh vực import lén",
     "- Hệ thống từ chối vì không có quyền\n- Danh sách không có bản ghi LVCTKD.IMP9"),

    ("08", "Quyền xem vẫn Xuất Excel được", "P1",
     "Tài khoản B chỉ có quyền xem. Danh mục có 8 lĩnh vực.",
     "1. Đăng nhập bằng tài khoản B\n2. Vào màn danh sách\n3. Bấm nút Xuất Excel\n4. Mở file tải về",
     "—",
     "- Tải được file danh sách lĩnh vực Công ty kinh doanh\n- File có đủ 8 dòng, đúng các cột của bảng"),

    ("09", "Có cả 2 quyền thì hưởng quyền quản lý", "P2",
     "Tài khoản D được cấp cả \"%s\" và \"%s\"." % (P_MANAGE, P_VIEW),
     "1. Đăng nhập bằng tài khoản D\n2. Vào màn danh sách\n3. Quan sát thanh nút và cột Hành động",
     "—",
     "- Hiện đủ Tạo mới, Xuất Excel, Import Excel\n- Cột Hành động hiện đủ thao tác như tài khoản chỉ có quyền quản lý"),
]

S1 = [
    (1, "Vào màn bằng menu Danh mục", "P0",
     "Tài khoản A có quyền quản lý. Danh mục có 8 lĩnh vực.",
     "1. Đăng nhập\n2. Mở nhóm menu Danh mục ở thanh bên trái\n3. Bấm mục Lĩnh vực Công ty kinh doanh",
     "—",
     "- Chuyển sang màn 'Danh sách lĩnh vực Công ty kinh doanh'\n"
     "- Tiêu đề bảng ghi đúng 'Danh sách lĩnh vực Công ty kinh doanh'\n"
     "- Mục menu nằm ngay TRÊN mục Nhóm ngành\n"
     "- Bảng hiện 8 dòng, mặc định 10 dòng/trang"),

    (2, "Thứ tự và nhãn các cột", "P0",
     "Màn danh sách đang mở với ít nhất 1 dòng dữ liệu.",
     "1. Quan sát dòng tiêu đề của bảng từ trái sang phải",
     "—",
     "- Đúng thứ tự: STT · Mã · Tên lĩnh vực Công ty kinh doanh · Người tạo · Ngày tạo · Người cập nhật · "
     "Ngày cập nhật · Trạng thái · Hành động\n"
     "- ⚠️ Không còn chữ 'kinh doanh nội bộ' ở bất kỳ nhãn nào trên màn"),

    (3, "Bảng hiện vòng quay chờ ngay khi vào màn", "P1",
     "Mạng chậm hoặc dữ liệu nhiều.",
     "1. Vào màn danh sách\n2. Quan sát vùng bảng trong lúc dữ liệu chưa về",
     "—",
     "- Vùng bảng hiện trạng thái đang tải ngay lập tức, không để trống trắng\n- Khi dữ liệu về thì bảng thay thế "
     "trạng thái đang tải"),

    (4, "Danh mục rỗng", "P1",
     "Xoá hết hoặc lọc ra điều kiện không có bản ghi nào.",
     "1. Vào màn danh sách\n2. Nhập vào ô tìm nhanh một chuỗi chắc chắn không khớp\n3. Quan sát vùng bảng",
     "Tìm nhanh: zzzzzz",
     "- Bảng hiện dòng chữ 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- ⚠️ Dòng chữ này KHÔNG được hiển thị màu đỏ (đỏ chỉ dành cho lỗi nhập liệu)"),

    (5, "Mở cửa sổ Xem bằng cách bấm vào Mã", "P0",
     "Có bản ghi LVCTKD.KHAC - Khác, người tạo Nguyễn Văn A, tạo ngày 22/08/2026 10:30.",
     "1. Vào màn danh sách\n2. Bấm vào chữ LVCTKD.KHAC ở cột Mã",
     "—",
     "- Mở cửa sổ tiêu đề 'Xem chi tiết lĩnh vực Công ty kinh doanh'\n"
     "- Ô Mã, Tên, Trạng thái hiện đúng dữ liệu và ở trạng thái khoá không sửa được\n"
     "- Có dòng người tạo / ngày tạo, người cập nhật / ngày cập nhật\n"
     "- Chỉ có nút Đóng, KHÔNG có nút Lưu\n"
     "- ⚠️ Cột Mã không có nút 'Xem' riêng — bấm vào mã chính là xem"),

    (6, "Chữ trong ô bảng để thường", "P2",
     "Bảng có ít nhất 1 dòng.",
     "1. Quan sát cột Mã và cột Tên lĩnh vực Công ty kinh doanh",
     "—",
     "- Chữ ở cả 2 cột hiển thị kiểu thường, KHÔNG in đậm\n- Cột Mã hiển thị như một liên kết bấm được"),

    (7, "Badge trạng thái đúng chữ và màu", "P0",
     "Có 1 bản ghi Hoạt động và 1 bản ghi Khoá.",
     "1. Quan sát cột Trạng thái của 2 dòng đó",
     "—",
     "- Dòng đang dùng hiện nhãn 'Hoạt động' màu xanh lá\n- Dòng bị khoá hiện nhãn 'Khoá' màu đỏ\n"
     "- ⚠️ Chữ trạng thái lấy y như hệ thống trả về, không phải số"),

    (8, "Định dạng ngày trên bảng", "P1",
     "Bản ghi LVCTKD.KHAC tạo lúc 22/08/2026 10:30:45.",
     "1. Quan sát cột Ngày tạo và Ngày cập nhật của dòng đó",
     "—",
     "- Hiện '22/08/2026 10:30' — có giờ phút, KHÔNG có giây\n- Không hiện dạng năm-tháng-ngày"),

    (9, "Cột Người tạo / Người cập nhật chỉ hiện tên", "P1",
     "Bản ghi do nhân viên 'Nguyễn Thị Cần' (mã 11010057, phòng HN_KD1) tạo.",
     "1. Quan sát cột Người tạo của dòng đó",
     "—",
     "- Chỉ hiện 'Nguyễn Thị Cần'\n- ⚠️ Không kèm mã nhân viên, không kèm mã phòng"),

    (10, "Ô trống hiển thị dấu gạch", "P2",
     "Có bản ghi được tạo bằng công cụ nạp dữ liệu nên chưa có người cập nhật.",
     "1. Quan sát cột Người cập nhật của dòng đó",
     "—",
     "- Ô hiện dấu '—', không để trắng trơn, không hiện chữ 'null'"),
]

S2 = [
    (1, "Tìm nhanh theo Mã", "P0",
     "Có các bản ghi: LVCTKD.KHAC - Khác, LVCTKD.0001 - Công nghiệp, LVCTKD.0002 - Môi trường.",
     "1. Vào màn danh sách\n2. Gõ '0001' vào ô tìm nhanh\n3. Chờ bảng tự tải lại",
     "Tìm nhanh: 0001",
     "- Bảng chỉ còn dòng LVCTKD.0001 - Công nghiệp\n- Không cần bấm nút tìm, bảng tự lọc"),

    (2, "Tìm nhanh theo Tên", "P0",
     "Như trên.",
     "1. Gõ 'Môi trường' vào ô tìm nhanh",
     "Tìm nhanh: Môi trường",
     "- Bảng chỉ còn dòng LVCTKD.0002 - Môi trường"),

    (3, "Tìm nhanh theo tên Người tạo", "P0",
     "Bản ghi LVCTKD.0001 do 'Nguyễn Thị Cần' tạo; các bản ghi khác do người khác tạo.",
     "1. Gõ 'Nguyễn Thị Cần' vào ô tìm nhanh",
     "Tìm nhanh: Nguyễn Thị Cần",
     "- Bảng chỉ còn các dòng do Nguyễn Thị Cần tạo, trong đó có LVCTKD.0001"),

    (4, "Câu gợi ý trong ô tìm nhanh nói đúng phạm vi tìm", "P1",
     "Màn danh sách đang mở, ô tìm nhanh còn trống.",
     "1. Quan sát chữ mờ trong ô tìm nhanh",
     "—",
     "- Ghi 'Tìm theo mã, tên lĩnh vực Công ty kinh doanh, người tạo'\n"
     "- ⚠️ Không được ghi chung chung kiểu 'Tìm kiếm...'"),

    (5, "Tìm nhanh không phân biệt chữ hoa thường", "P1",
     "Có bản ghi LVCTKD.0002 - Môi trường.",
     "1. Gõ 'môi trường' (toàn chữ thường)",
     "Tìm nhanh: môi trường",
     "- Vẫn tìm ra dòng Môi trường"),

    (6, "Tìm nhanh có ký tự đặc biệt không làm hỏng bảng", "P1",
     "Danh mục có 8 bản ghi.",
     "1. Gõ lần lượt các chuỗi: %, _, ' vào ô tìm nhanh",
     "Tìm nhanh: % rồi _ rồi '",
     "- Hệ thống coi đây là ký tự thường để tìm, trả về 0 dòng hoặc dòng thật sự chứa ký tự đó\n"
     "- ⚠️ Không được trả về TOÀN BỘ danh sách khi gõ % hoặc _, không văng lỗi"),

    (7, "Mở khối tìm kiếm nâng cao", "P0",
     "Màn danh sách đang mở, khối lọc đang thu gọn.",
     "1. Bấm nút mở rộng bộ lọc\n2. Quan sát các ô lọc hiện ra",
     "—",
     "- Hiện đủ 7 ô: Mã · Tên lĩnh vực Công ty kinh doanh · Trạng thái · Người tạo · Người cập nhật · "
     "Cập nhật từ · Cập nhật đến\n- Mỗi ô đều có nhãn nằm trên"),

    (8, "Lọc theo Mã (khớp một phần)", "P0",
     "Có LVCTKD.0001, LVCTKD.0002, LVCTKD.KHAC.",
     "1. Mở bộ lọc nâng cao\n2. Nhập '000' vào ô Mã",
     "Mã: 000",
     "- Bảng còn LVCTKD.0001 và LVCTKD.0002, không còn LVCTKD.KHAC"),

    (9, "Lọc theo Tên (khớp một phần)", "P0",
     "Có 'Công nghiệp' và 'Giáo dục đào tạo'.",
     "1. Nhập 'nghiệp' vào ô Tên lĩnh vực Công ty kinh doanh",
     "Tên: nghiệp",
     "- Bảng chỉ còn dòng Công nghiệp"),

    (10, "Lọc theo Trạng thái Hoạt động", "P0",
     "Có 6 bản ghi Hoạt động và 2 bản ghi Khoá.",
     "1. Chọn Trạng thái = Hoạt động",
     "Trạng thái: Hoạt động",
     "- Bảng còn đúng 6 dòng, cột Trạng thái toàn nhãn 'Hoạt động'"),

    (11, "Lọc theo Trạng thái Khoá", "P0",
     "Như trên.",
     "1. Chọn Trạng thái = Khoá",
     "Trạng thái: Khoá",
     "- Bảng còn đúng 2 dòng, cột Trạng thái toàn nhãn 'Khoá'"),

    (12, "Lọc theo Người tạo", "P0",
     "Nguyễn Thị Cần tạo 3 bản ghi, người khác tạo 5.",
     "1. Chọn Người tạo = Nguyễn Thị Cần",
     "Người tạo: Nguyễn Thị Cần",
     "- Bảng còn đúng 3 dòng, cột Người tạo đều là Nguyễn Thị Cần"),

    (13, "Ô chọn nhân viên hiển thị đúng khuôn tên - mã phòng - mã nhân viên", "P1",
     "Nhân viên Nguyễn Thị Cần thuộc phòng HN_KD1, mã nhân viên 11010057.",
     "1. Mở ô Người tạo\n2. Gõ 'Cần' và quan sát dòng gợi ý",
     "—",
     "- Dòng gợi ý hiện 'Nguyễn Thị Cần - HN_KD1 - 11010057'"),

    (14, "Lọc theo Người cập nhật", "P1",
     "Bản ghi LVCTKD.0001 do Trần Văn B sửa lần cuối.",
     "1. Chọn Người cập nhật = Trần Văn B",
     "Người cập nhật: Trần Văn B",
     "- Bảng chỉ còn các dòng có cột Người cập nhật là Trần Văn B"),

    (15, "Lọc khoảng ngày cập nhật lấy cả 2 đầu mút", "P0",
     "3 bản ghi cập nhật lần lượt 01/09/2026, 05/09/2026, 10/09/2026.",
     "1. Chọn Cập nhật từ = 01/09/2026\n2. Chọn Cập nhật đến = 05/09/2026",
     "Cập nhật từ: 01/09/2026 · Cập nhật đến: 05/09/2026",
     "- Bảng còn đúng 2 dòng (01/09 và 05/09)\n- ⚠️ Bản ghi cập nhật lúc 05/09/2026 23:50 vẫn phải được lấy"),

    (16, "Chỉ nhập Cập nhật từ", "P1",
     "Như trên.",
     "1. Chọn Cập nhật từ = 05/09/2026, để trống ô Cập nhật đến",
     "Cập nhật từ: 05/09/2026",
     "- Bảng còn 2 dòng cập nhật ngày 05/09 và 10/09"),

    (17, "Chỉ nhập Cập nhật đến", "P1",
     "Như trên.",
     "1. Để trống ô Cập nhật từ, chọn Cập nhật đến = 05/09/2026",
     "Cập nhật đến: 05/09/2026",
     "- Bảng còn 2 dòng cập nhật ngày 01/09 và 05/09"),

    (18, "Khoảng ngày ngược (từ > đến)", "P1",
     "Như trên.",
     "1. Chọn Cập nhật từ = 10/09/2026\n2. Chọn Cập nhật đến = 01/09/2026",
     "Cập nhật từ: 10/09/2026 · Cập nhật đến: 01/09/2026",
     "- Bảng hiện 0 dòng kèm dòng chữ không có dữ liệu\n- ⚠️ Không văng lỗi, không tự đảo lại 2 ngày cho người dùng"),

    (19, "Nhiều điều kiện lọc cùng lúc", "P0",
     "Nguyễn Thị Cần tạo 3 bản ghi, trong đó 1 bản ghi đang Khoá.",
     "1. Chọn Người tạo = Nguyễn Thị Cần\n2. Chọn Trạng thái = Khoá",
     "Người tạo: Nguyễn Thị Cần · Trạng thái: Khoá",
     "- Bảng còn đúng 1 dòng thoả CẢ HAI điều kiện"),

    (20, "Nút Làm mới xoá hết điều kiện lọc", "P0",
     "Đang lọc: tìm nhanh 'Môi', Trạng thái = Khoá, Người tạo = Nguyễn Thị Cần.",
     "1. Bấm nút Làm mới\n2. Quan sát các ô lọc và bảng",
     "—",
     "- Mọi ô lọc và ô tìm nhanh về trống\n- Bảng tải lại đủ 8 dòng, về trang 1\n"
     "- ⚠️ Bảng phải tự tải lại ngay, không phải bấm thêm nút nào"),

    (21, "Lọc xong quay về trang 1", "P1",
     "Danh mục có 25 bản ghi, đang đứng ở trang 3.",
     "1. Nhập điều kiện lọc bất kỳ cho ra nhiều kết quả\n2. Quan sát số trang",
     "Trạng thái: Hoạt động",
     "- Bảng nhảy về trang 1, không giữ trang 3 rồi hiện rỗng"),

    (22, "Thu gọn khối lọc không mất điều kiện đang lọc", "P2",
     "Đang lọc Trạng thái = Khoá, bảng còn 2 dòng.",
     "1. Bấm thu gọn khối lọc\n2. Quan sát bảng",
     "—",
     "- Bảng vẫn giữ 2 dòng đang lọc, không tự tải lại toàn bộ"),
]

S3 = [
    (1, "Sắp xếp theo Mã tăng dần", "P0",
     "Có LVCTKD.0001, LVCTKD.0002, LVCTKD.KHAC.",
     "1. Bấm tiêu đề cột Mã một lần",
     "—",
     "- Thứ tự dòng theo mã tăng dần: LVCTKD.0001, LVCTKD.0002, LVCTKD.KHAC\n- Tiêu đề cột hiện dấu mũi tên tăng"),

    (2, "Sắp xếp theo Mã giảm dần", "P1",
     "Như trên.",
     "1. Bấm tiêu đề cột Mã lần thứ hai",
     "—",
     "- Thứ tự đảo lại: LVCTKD.KHAC, LVCTKD.0002, LVCTKD.0001"),

    (3, "Sắp xếp theo Tên", "P1",
     "Có 'Công nghiệp', 'Môi trường', 'Giáo dục đào tạo'.",
     "1. Bấm tiêu đề cột Tên lĩnh vực Công ty kinh doanh",
     "—",
     "- Sắp theo bảng chữ cái tăng dần: Công nghiệp, Giáo dục đào tạo, Môi trường"),

    (4, "Sắp xếp theo Ngày tạo", "P1",
     "3 bản ghi tạo lần lượt 20/08/2026, 22/08/2026, 01/09/2026.",
     "1. Bấm tiêu đề cột Ngày tạo",
     "—",
     "- Sắp theo thời gian tăng dần đúng 3 mốc trên"),

    (5, "Sắp xếp theo Ngày cập nhật", "P1",
     "Như mục 4 nhưng theo ngày cập nhật.",
     "1. Bấm tiêu đề cột Ngày cập nhật",
     "—",
     "- Sắp đúng theo cột Ngày cập nhật, không nhầm sang Ngày tạo"),

    (6, "Cột không cho sắp xếp thì không đổi thứ tự", "P2",
     "Bảng đang có 8 dòng.",
     "1. Bấm tiêu đề cột Người tạo và cột Trạng thái",
     "—",
     "- Thứ tự dòng không đổi, không hiện mũi tên sắp xếp ở 2 cột này"),

    (7, "Kết quả khớp sát từ khoá được xếp lên trên", "P1",
     "Có 'Công nghiệp' (mã LVCTKD.0001) và 'Dịch vụ công nghiệp phụ trợ' (mã LVCTKD.0009).",
     "1. Chưa bấm sắp xếp cột nào\n2. Gõ 'Công nghiệp' vào ô tìm nhanh",
     "Tìm nhanh: Công nghiệp",
     "- Dòng trùng khít 'Công nghiệp' đứng TRƯỚC dòng chỉ chứa từ khoá"),

    (8, "Sắp xếp giữ nguyên khi chuyển trang", "P1",
     "Danh mục 25 bản ghi, đang sắp theo Mã tăng dần.",
     "1. Bấm sang trang 2\n2. Quan sát mã dòng đầu trang 2",
     "—",
     "- Trang 2 tiếp nối đúng thứ tự tăng dần của trang 1, không bị xáo lại"),

    (9, "Phân trang mặc định 10 dòng", "P0",
     "Danh mục có 25 bản ghi, chưa lọc gì.",
     "1. Vào màn danh sách\n2. Quan sát bảng và dòng thông tin dưới bảng",
     "—",
     "- Bảng hiện 10 dòng\n- Dưới bảng ghi 'Hiển thị 1-10 / 25'\n- Có 3 trang"),

    (10, "Chuyển trang", "P0",
     "Như trên.",
     "1. Bấm số trang 3",
     "—",
     "- Bảng hiện 5 dòng cuối\n- Dòng thông tin ghi 'Hiển thị 21-25 / 25'\n- Cột STT bắt đầu từ 21"),

    (11, "Đổi số dòng mỗi trang", "P0",
     "Danh mục có 25 bản ghi, đang ở trang 3.",
     "1. Chọn 50 dòng / trang",
     "Số dòng/trang: 50",
     "- Bảng hiện đủ 25 dòng trên 1 trang\n- Tự quay về trang 1"),

    (12, "STT liên tục theo trang", "P1",
     "Danh mục 25 bản ghi, cỡ trang 10.",
     "1. Sang trang 2\n2. Quan sát cột STT",
     "—",
     "- Dòng đầu trang 2 mang số 11, dòng cuối mang số 20"),

    (13, "Phân trang theo kết quả lọc", "P1",
     "25 bản ghi, trong đó 12 bản ghi Hoạt động.",
     "1. Lọc Trạng thái = Hoạt động\n2. Quan sát dòng thông tin dưới bảng",
     "Trạng thái: Hoạt động",
     "- Ghi 'Hiển thị 1-10 / 12', có 2 trang\n- ⚠️ Tổng phải là 12 (số khớp lọc), không phải 25"),

    (14, "Bảng tràn ngang có thanh cuộn cả trên và dưới", "P2",
     "Thu hẹp cửa sổ trình duyệt để bảng rộng hơn màn hình.",
     "1. Thu hẹp cửa sổ\n2. Quan sát mép trên và mép dưới của bảng",
     "—",
     "- Có thanh cuộn ngang ở CẢ phía trên và phía dưới bảng, kéo thanh nào thì thanh kia chạy theo\n"
     "- Cột STT và cột Mã đứng yên khi cuộn ngang"),
]

S4 = [
    (1, "Mở cửa sổ Tạo mới", "P0",
     "Tài khoản có quyền quản lý.",
     "1. Bấm nút Tạo mới",
     "—",
     "- Mở cửa sổ tiêu đề 'Tạo mới lĩnh vực Công ty kinh doanh'\n"
     "- Ô Mã đã điền sẵn tiền tố 'LVCTKD.' và con trỏ đứng sau dấu chấm\n"
     "- Ô Tên trống, Trạng thái mặc định 'Hoạt động'\n"
     "- Chân cửa sổ có 3 nút: Lưu · Lưu & Tiếp tục · Đóng\n"
     "- Nhãn Mã và Tên có dấu * đỏ"),

    (2, "Tạo mới thành công", "P0",
     "Chưa có bản ghi nào mã LVCTKD.OTO hoặc tên 'Ô tô'.",
     "1. Bấm Tạo mới\n2. Gõ 'OTO' vào ô Mã\n3. Gõ 'Ô tô' vào ô Tên\n4. Bấm Lưu",
     "Mã: LVCTKD.OTO · Tên: Ô tô · Trạng thái: Hoạt động",
     "- Hiện thông báo 'Thêm mới thành công'\n- Cửa sổ đóng lại\n"
     "- Bảng tải lại và có dòng LVCTKD.OTO - Ô tô, trạng thái Hoạt động\n"
     "- Cột Người tạo là người đang đăng nhập, Ngày tạo là thời điểm vừa lưu"),

    (3, "Người tạo / ngày tạo được ghi tự động, không có ô nhập", "P0",
     "Đang mở cửa sổ Tạo mới.",
     "1. Quan sát toàn bộ các ô trong cửa sổ",
     "—",
     "- Chỉ có 3 ô nhập: Mã, Tên, Trạng thái\n"
     "- ⚠️ Không có ô nhập Người tạo / Ngày tạo / Người cập nhật / Ngày cập nhật — hệ thống tự ghi theo tài khoản "
     "đang thao tác"),

    (4, "Tiền tố LVCTKD. không xoá được", "P0",
     "Đang mở cửa sổ Tạo mới.",
     "1. Đặt con trỏ vào ô Mã\n2. Bấm phím xoá lùi nhiều lần\n3. Bôi đen cả ô rồi bấm xoá",
     "—",
     "- Phần 'LVCTKD.' luôn còn nguyên trong ô\n- Chỉ phần hậu tố bị xoá"),

    (5, "Ô Mã chỉ cho gõ tối đa 4 ký tự hậu tố", "P0",
     "Đang mở cửa sổ Tạo mới.",
     "1. Gõ liên tục 'ABCDEFGH' vào phần hậu tố",
     "Mã gõ: ABCDEFGH",
     "- Ô chỉ nhận 4 ký tự đầu: LVCTKD.ABCD\n"
     "- ⚠️ Ô không được tự cắt rồi lưu sai ý người dùng ở chỗ khác — phần thừa đơn giản là không gõ vào được"),

    (6, "Mã chữ thường tự chuyển thành chữ hoa", "P0",
     "Chưa có bản ghi mã LVCTKD.ELEC.",
     "1. Bấm Tạo mới\n2. Gõ 'elec' vào ô Mã\n3. Gõ Tên 'Điện - Tự động hoá'\n4. Bấm Lưu\n5. Xem dòng vừa tạo "
     "trên bảng",
     "Mã gõ: elec · Tên: Điện - Tự động hoá",
     "- Lưu thành công\n- Cột Mã trên bảng hiện 'LVCTKD.ELEC' (chữ hoa)"),

    (7, "Hậu tố có dấu gạch dưới và số", "P1",
     "Chưa có bản ghi mã LVCTKD.A_1.",
     "1. Bấm Tạo mới\n2. Gõ 'A_1' vào ô Mã, Tên hợp lệ\n3. Bấm Lưu",
     "Mã: LVCTKD.A_1 · Tên: Lĩnh vực thử A1",
     "- Lưu thành công, mã hiện đúng LVCTKD.A_1"),

    (8, "Nút Lưu & Tiếp tục giữ cửa sổ để nhập tiếp", "P0",
     "Chưa có 2 mã LVCTKD.T1, LVCTKD.T2.",
     "1. Bấm Tạo mới\n2. Nhập mã T1, tên 'Lĩnh vực thử 1'\n3. Bấm Lưu & Tiếp tục\n4. Nhập tiếp mã T2, tên "
     "'Lĩnh vực thử 2'\n5. Bấm Lưu",
     "Mã: LVCTKD.T1 / LVCTKD.T2",
     "- Sau bước 3: hiện 'Thêm mới thành công', cửa sổ VẪN MỞ, các ô về trạng thái trống với tiền tố LVCTKD.\n"
     "- Sau bước 5: cửa sổ đóng, bảng có đủ cả 2 bản ghi"),

    (9, "Nút Lưu & Tiếp tục chỉ có ở Tạo mới", "P1",
     "Có bản ghi LVCTKD.OTO đang Hoạt động.",
     "1. Bấm biểu tượng Sửa ở dòng LVCTKD.OTO\n2. Quan sát chân cửa sổ",
     "—",
     "- Chỉ có nút Lưu và Đóng\n- Không có nút Lưu & Tiếp tục"),

    (10, "Mở cửa sổ Sửa hiện đúng dữ liệu cũ", "P0",
     "Có bản ghi LVCTKD.OTO - Ô tô, Hoạt động, cập nhật lần cuối 10/09/2026 09:15 bởi Trần Văn B.",
     "1. Bấm biểu tượng Sửa ở dòng đó\n2. Quan sát cửa sổ",
     "—",
     "- Tiêu đề 'Sửa lĩnh vực Công ty kinh doanh'\n- Ô Mã: LVCTKD.OTO · Ô Tên: Ô tô · Trạng thái: Hoạt động\n"
     "- Có dòng thông tin cập nhật lần cuối: Trần Văn B - 10/09/2026 09:15"),

    (11, "Sửa tên thành công", "P0",
     "Có bản ghi LVCTKD.OTO - Ô tô.",
     "1. Bấm Sửa dòng đó\n2. Xoá tên cũ, gõ 'Ô tô và xe máy'\n3. Bấm Lưu",
     "Tên mới: Ô tô và xe máy",
     "- Hiện 'Cập nhật thành công', cửa sổ đóng\n- Bảng hiện tên mới\n"
     "- Cột Người cập nhật đổi thành người đang đăng nhập, Ngày cập nhật là thời điểm vừa lưu"),

    (12, "Sửa mã thành công", "P1",
     "Có bản ghi LVCTKD.OTO; chưa có mã LVCTKD.CAR.",
     "1. Bấm Sửa dòng LVCTKD.OTO\n2. Sửa hậu tố thành 'CAR'\n3. Bấm Lưu",
     "Mã mới: LVCTKD.CAR",
     "- Lưu thành công, bảng hiện mã LVCTKD.CAR\n- Nhóm ngành đang thuộc lĩnh vực này vẫn giữ nguyên liên kết"),

    (13, "Đổi trạng thái sang Khoá ngay trong cửa sổ Sửa", "P1",
     "Bản ghi LVCTKD.T1 đang Hoạt động, chưa nhóm ngành nào dùng.",
     "1. Bấm Sửa dòng LVCTKD.T1\n2. Chọn Trạng thái = Khoá\n3. Bấm Lưu",
     "Trạng thái: Khoá",
     "- Lưu thành công\n- Dòng trên bảng đổi nhãn sang 'Khoá' màu đỏ\n"
     "- Dòng đó chỉ còn biểu tượng Mở khoá ở cột Hành động"),

    (14, "Bấm Đóng thì không lưu gì", "P0",
     "Bản ghi LVCTKD.OTO - Ô tô.",
     "1. Bấm Sửa dòng đó\n2. Đổi tên thành 'Ô tô SỬA THỬ'\n3. Bấm nút Đóng\n4. Quan sát bảng",
     "Tên gõ: Ô tô SỬA THỬ",
     "- Cửa sổ đóng, không có thông báo lưu\n- Tên trên bảng vẫn là 'Ô tô'"),

    (15, "Mở lại cửa sổ Tạo mới sau khi Sửa không dính dữ liệu cũ", "P0",
     "Vừa mở cửa sổ Sửa của LVCTKD.OTO rồi bấm Đóng.",
     "1. Bấm nút Tạo mới\n2. Quan sát các ô",
     "—",
     "- Ô Mã chỉ có tiền tố LVCTKD., ô Tên trống, Trạng thái Hoạt động\n"
     "- ⚠️ Không còn sót dữ liệu của bản ghi vừa xem"),

    (16, "Lỗi cũ tự mất khi người dùng sửa lại ô đó", "P1",
     "Đã tồn tại bản ghi tên 'Ô tô'.",
     "1. Bấm Tạo mới, nhập mã hợp lệ và tên 'Ô tô'\n2. Bấm Lưu (hiện lỗi trùng tên)\n3. Sửa tên thành "
     "'Ô tô nhập khẩu'",
     "Tên: Ô tô -> Ô tô nhập khẩu",
     "- Ngay khi gõ lại, dòng lỗi đỏ dưới ô Tên biến mất, viền đỏ mất theo\n- Chưa cần bấm Lưu lại"),

    (17, "Cửa sổ Xem không cho sửa", "P0",
     "Có bản ghi LVCTKD.OTO.",
     "1. Bấm vào mã LVCTKD.OTO ở cột Mã\n2. Thử gõ vào ô Tên, thử mở ô Trạng thái",
     "—",
     "- Không gõ được vào ô nào, ô Trạng thái không mở danh sách chọn\n- Chỉ có nút Đóng"),
]

S5 = [
    (1, "Khoá bản ghi thành công", "P0",
     "Bản ghi LVCTKD.T1 đang Hoạt động, KHÔNG có nhóm ngành nào thuộc lĩnh vực này.",
     "1. Bấm biểu tượng Khoá ở dòng LVCTKD.T1\n2. Đọc cửa sổ xác nhận\n3. Bấm nút Khoá",
     "—",
     "- Cửa sổ xác nhận tiêu đề 'Xác nhận khoá', nội dung \"Bạn có chắc muốn khoá lĩnh vực Công ty kinh doanh "
     "'Lĩnh vực thử 1'?\"\n- Hai nút: Hủy và Khoá\n- Sau khi bấm Khoá: hiện 'Khoá thành công', dòng chuyển nhãn "
     "'Khoá', cột Người cập nhật đổi thành người vừa thao tác"),

    (2, "Hủy ở cửa sổ xác nhận khoá", "P1",
     "Như trên, bản ghi vẫn Hoạt động.",
     "1. Bấm biểu tượng Khoá\n2. Bấm nút Hủy",
     "—",
     "- Cửa sổ đóng, không có thông báo\n- Trạng thái vẫn Hoạt động"),

    (3, "Mở khoá thành công", "P0",
     "Bản ghi LVCTKD.T1 đang Khoá.",
     "1. Bấm biểu tượng Mở khoá ở dòng đó\n2. Bấm nút Mở khoá trong cửa sổ xác nhận",
     "—",
     "- Cửa sổ xác nhận tiêu đề 'Xác nhận mở khoá', nút xác nhận ghi 'Mở khoá'\n"
     "- Hiện 'Mở khoá thành công', dòng đổi về nhãn 'Hoạt động'\n- Cột Hành động hiện lại đủ Sửa, Khoá, Xoá"),

    (4, "Không cho khoá khi còn nhóm ngành đang hoạt động", "P0",
     "Lĩnh vực LVCTKD.0001 - Công nghiệp đang có 6 Nhóm ngành trạng thái Hoạt động.",
     "1. Tìm dòng LVCTKD.0001\n2. Quan sát cột Hành động",
     "—",
     "- KHÔNG có biểu tượng Khoá ở dòng này (nút bị ẩn hẳn, không phải hiện mờ)\n"
     "- Vẫn còn biểu tượng Sửa"),

    (5, "Khoá được khi nhóm ngành bên dưới đều đã khoá", "P1",
     "Lĩnh vực LVCTKD.0002 có 2 Nhóm ngành, cả 2 đều đang Khoá.",
     "1. Khoá cả 2 nhóm ngành ở màn Nhóm ngành\n2. Quay lại màn Lĩnh vực Công ty kinh doanh, tải lại\n"
     "3. Quan sát dòng LVCTKD.0002",
     "—",
     "- Biểu tượng Khoá xuất hiện trở lại\n- Bấm Khoá thì khoá được bình thường"),

    (6, "Bản ghi đang khoá thì ẩn nút Sửa và Xoá", "P0",
     "Bản ghi LVCTKD.T1 đang Khoá.",
     "1. Quan sát cột Hành động của dòng đó",
     "—",
     "- Chỉ còn biểu tượng Mở khoá\n- Không có Sửa, không có Xoá"),

    (7, "Chặn sửa bản ghi đang khoá khi gọi thẳng chức năng", "P0",
     "Bản ghi LVCTKD.T1 đang Khoá. Tài khoản có quyền quản lý.",
     "1. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa bản ghi LVCTKD.T1, bỏ qua giao diện\n2. Mở lại danh sách",
     "Tên mới: Sửa lén khi đang khoá",
     "- Hệ thống từ chối, báo bản ghi đang bị khoá, cần mở khoá trước khi cập nhật\n- Dữ liệu không đổi"),

    (8, "Chặn xoá bản ghi đang khoá khi gọi thẳng chức năng", "P0",
     "Bản ghi LVCTKD.T1 đang Khoá.",
     "1. Gọi thẳng chức năng Xoá bản ghi đó, bỏ qua giao diện\n2. Mở lại danh sách",
     "—",
     "- Hệ thống từ chối, báo bản ghi đang bị khoá\n- Bản ghi vẫn còn"),

    (9, "Lĩnh vực đã khoá vẫn hiện ở nhóm ngành đang dùng nó", "P0",
     "Nhóm ngành NN.0001 đang thuộc lĩnh vực LVCTKD.0002; sau đó LVCTKD.0002 bị khoá.",
     "1. Vào màn Nhóm ngành, mở Sửa nhóm ngành NN.0001\n2. Quan sát ô chọn Lĩnh vực Công ty kinh doanh",
     "—",
     "- Ô vẫn hiện đúng tên lĩnh vực đang chọn, kèm biểu tượng ổ khoá phía trước\n"
     "- ⚠️ Không được để trống ô, không tự nhảy sang lĩnh vực khác\n"
     "- Mở danh sách chọn ra thì lĩnh vực đã khoá này vẫn nằm trong danh sách; đổi sang lĩnh vực khác rồi mở lại thì "
     "lĩnh vực khoá đó biến mất"),

    (10, "Lĩnh vực đã khoá không hiện khi tạo nhóm ngành mới", "P1",
     "LVCTKD.0002 đang Khoá, LVCTKD.0001 đang Hoạt động.",
     "1. Vào màn Nhóm ngành, bấm Tạo mới\n2. Mở ô chọn Lĩnh vực Công ty kinh doanh",
     "—",
     "- Danh sách chỉ liệt kê lĩnh vực đang Hoạt động, không có LVCTKD.0002"),
]

S6 = [
    (1, "Xoá thành công", "P0",
     "Bản ghi LVCTKD.T2 đang Hoạt động, chưa có nhóm ngành nào dùng.",
     "1. Bấm biểu tượng Xoá ở dòng LVCTKD.T2\n2. Đọc cửa sổ xác nhận\n3. Bấm nút Xóa",
     "—",
     "- Cửa sổ 'Xác nhận xóa', nội dung \"Bạn có chắc muốn xóa lĩnh vực Công ty kinh doanh 'Lĩnh vực thử 2'?\"\n"
     "- Hai nút: Hủy và Xóa (nút Xóa màu đỏ)\n- Sau khi xoá: hiện 'Xoá thành công', dòng biến mất khỏi bảng, tổng "
     "số bản ghi giảm 1"),

    (2, "Hủy ở cửa sổ xác nhận xoá", "P0",
     "Như trên.",
     "1. Bấm biểu tượng Xoá\n2. Bấm Hủy",
     "—",
     "- Không có thông báo nào\n- Bản ghi vẫn còn nguyên trong bảng"),

    (3, "Ẩn nút Xoá khi lĩnh vực đang được nhóm ngành sử dụng", "P0",
     "Lĩnh vực LVCTKD.0001 đang có 6 nhóm ngành (kể cả nhóm ngành đã khoá).",
     "1. Quan sát cột Hành động dòng LVCTKD.0001",
     "—",
     "- KHÔNG có biểu tượng Xoá (ẩn hẳn)\n"
     "- ⚠️ Chỉ cần còn 1 nhóm ngành thuộc lĩnh vực này, dù nhóm đó đã khoá, cũng không được xoá"),

    (4, "Chặn xoá khi gọi thẳng chức năng lúc lĩnh vực đang được dùng", "P0",
     "Lĩnh vực LVCTKD.0001 đang có 6 nhóm ngành.",
     "1. Gọi thẳng chức năng Xoá lĩnh vực LVCTKD.0001, bỏ qua giao diện\n2. Mở lại danh sách",
     "—",
     "- Hệ thống từ chối, báo dữ liệu đang được sử dụng, vui lòng tải lại\n- Bản ghi vẫn còn, 6 nhóm ngành không "
     "mất liên kết"),

    (5, "Xoá bản ghi vừa bị người khác xoá", "P1",
     "Hai người cùng mở màn danh sách. Người 1 đã xoá LVCTKD.T2 nhưng người 2 chưa tải lại bảng.",
     "1. Người 2 bấm Xoá dòng LVCTKD.T2\n2. Bấm Xóa ở cửa sổ xác nhận",
     "—",
     "- Hệ thống báo 'Dữ liệu đã thay đổi, vui lòng tải lại'\n- ⚠️ Màn không treo, không văng lỗi kỹ thuật"),

    (6, "Xoá xong bảng giữ đúng điều kiện lọc", "P2",
     "Đang lọc Trạng thái = Hoạt động, bảng 6 dòng, trong đó LVCTKD.T2 xoá được.",
     "1. Xoá dòng LVCTKD.T2\n2. Quan sát bảng",
     "—",
     "- Bảng còn 5 dòng và VẪN đang lọc Trạng thái = Hoạt động, không tự bỏ điều kiện lọc"),
]

S7 = [
    (1, "Xuất Excel toàn bộ danh sách", "P0",
     "Danh mục có 8 bản ghi, chưa lọc gì.",
     "1. Bấm nút Xuất Excel\n2. Mở file vừa tải về",
     "—",
     "- Tải về file tên 'danh_sach_linh_vuc_cong_ty_kinh_doanh'\n"
     "- File có tiêu đề 'Danh sách lĩnh vực Công ty kinh doanh' và đủ 8 dòng\n"
     "- Các cột: STT, Mã, Tên lĩnh vực Công ty kinh doanh, Trạng thái, Người tạo, Ngày tạo, Người cập nhật, "
     "Ngày cập nhật"),

    (2, "File xuất ra mang mã theo tiền tố mới", "P0",
     "Danh mục đã được đổi mã sang tiền tố mới.",
     "1. Bấm Xuất Excel\n2. Mở file và soi cột Mã",
     "—",
     "- Mọi mã đều bắt đầu bằng 'LVCTKD.'\n"
     "- ⚠️ Không còn bất kỳ mã nào bắt đầu bằng 'LVKDNB.' — đây là lỗi đã sửa ngày 15/09/2026"),

    (3, "Xuất Excel theo đúng điều kiện đang lọc", "P0",
     "8 bản ghi, trong đó 2 bản ghi đang Khoá.",
     "1. Lọc Trạng thái = Khoá\n2. Bấm Xuất Excel\n3. Mở file",
     "Trạng thái: Khoá",
     "- File chỉ có 2 dòng đúng 2 bản ghi đang Khoá\n- ⚠️ Không xuất cả 8 dòng"),

    (4, "Xuất Excel khi kết quả lọc rỗng", "P1",
     "Đang lọc ra 0 dòng.",
     "1. Bấm Xuất Excel\n2. Mở file",
     "Tìm nhanh: zzzzzz",
     "- Vẫn tải được file, có dòng tiêu đề nhưng không có dòng dữ liệu\n- Không văng lỗi"),

    (5, "Trạng thái trong file là chữ", "P1",
     "Có bản ghi Hoạt động và bản ghi Khoá.",
     "1. Xuất Excel và soi cột Trạng thái",
     "—",
     "- Ghi 'Hoạt động' / 'Khoá'\n- ⚠️ Không phải số 1 / 2"),

    (6, "Mở cửa sổ Import Excel", "P0",
     "Tài khoản có quyền quản lý.",
     "1. Bấm nút Import Excel",
     "—",
     "- Mở cửa sổ 'Import Lĩnh vực Công ty kinh doanh'\n- Có dòng hướng dẫn: chỉ nhập Mã và Tên\n"
     "- Có nút tải file mẫu và vùng chọn tệp"),

    (7, "File mẫu tải về ghi mã theo tiền tố mới", "P0",
     "Đang mở cửa sổ Import Excel.",
     "1. Bấm nút tải file mẫu\n2. Mở file mẫu vừa tải",
     "—",
     "- Dòng hướng dẫn ghi 'LVCTKD.XXXX — hậu tố tối đa 4 ký tự: A-Z, 0-9, _'\n"
     "- 2 dòng ví dụ là LVCTKD.OTO và LVCTKD.ELEC\n"
     "- ⚠️ Nếu còn thấy 'LVKDNB.' là lỗi: nhập theo mẫu sẽ sai định dạng toàn bộ (lỗi đã sửa 15/09/2026)"),

    (8, "Import file mẫu hợp lệ", "P0",
     "File mẫu 2 dòng: LVCTKD.OTO - Ô tô, LVCTKD.ELEC - Điện Tự động hoá. Danh mục chưa có 2 mã này.",
     "1. Bấm Import Excel\n2. Chọn file\n3. Bấm kiểm tra dữ liệu\n4. Bấm nút Import",
     "2 dòng như tiền điều kiện",
     "- Sau bước 3: báo 2 dòng hợp lệ, 0 dòng lỗi\n- Sau bước 4: báo 'Import thành công 2 lĩnh vực Công ty kinh "
     "doanh', cửa sổ đóng\n- Bảng có thêm đúng 2 dòng, trạng thái Hoạt động"),

    (9, "Import báo lỗi từng dòng sai định dạng mã", "P0",
     "File có 3 dòng: LVCTKD.OK1 hợp lệ; LVKDNB.OTO (tiền tố cũ); LVCTKD.ABCDE (hậu tố 5 ký tự).",
     "1. Chọn file và bấm kiểm tra dữ liệu\n2. Quan sát bảng kết quả kiểm tra",
     "3 dòng như tiền điều kiện",
     "- Dòng 1 hợp lệ\n- Dòng 2 và 3 bị đánh dấu lỗi, ghi rõ mã phải có dạng LVCTKD. + tối đa 4 ký tự\n"
     "- Nút Import chỉ bật khi không còn dòng lỗi"),

    (10, "Import báo mã trùng trong hệ thống", "P0",
     "Danh mục đã có LVCTKD.OTO. File import có 1 dòng mã LVCTKD.OTO.",
     "1. Chọn file và bấm kiểm tra dữ liệu",
     "Mã: LVCTKD.OTO",
     "- Dòng bị đánh dấu lỗi 'Mã đã tồn tại trong hệ thống'"),

    (11, "Import báo trùng ngay trong file", "P0",
     "File có 2 dòng cùng mã LVCTKD.DUP.",
     "1. Chọn file và bấm kiểm tra dữ liệu",
     "2 dòng cùng mã LVCTKD.DUP",
     "- Dòng thứ hai báo lỗi trùng mã, có chỉ rõ trùng với dòng số mấy trong file"),

    (12, "Import báo trùng tên", "P1",
     "Danh mục đã có tên 'Ô tô'. File có 1 dòng tên 'Ô tô' với mã mới.",
     "1. Chọn file và bấm kiểm tra dữ liệu",
     "Mã: LVCTKD.OT2 · Tên: Ô tô",
     "- Dòng bị báo lỗi tên đã tồn tại trong hệ thống"),

    (13, "Import thiếu mã hoặc thiếu tên", "P0",
     "File có 1 dòng bỏ trống ô Mã và 1 dòng bỏ trống ô Tên.",
     "1. Chọn file và bấm kiểm tra dữ liệu",
     "2 dòng thiếu dữ liệu",
     "- Dòng thiếu mã báo 'Mã bắt buộc phải nhập'\n- Dòng thiếu tên báo 'Tên bắt buộc phải nhập'"),

    (14, "Import tên chứa dấu phẩy hoặc hai chấm", "P1",
     "File có dòng tên 'Ô tô, xe máy' và dòng tên 'Ngành: ô tô'.",
     "1. Chọn file và bấm kiểm tra dữ liệu",
     "2 dòng như tiền điều kiện",
     "- Cả 2 dòng báo lỗi tên không được chứa dấu phẩy và dấu hai chấm"),

    (15, "Import file trộn dòng đúng và dòng sai", "P1",
     "File 4 dòng: 2 dòng hợp lệ, 2 dòng sai định dạng mã.",
     "1. Chọn file, bấm kiểm tra dữ liệu\n2. Sửa lại 2 dòng sai ngay trên bảng kiểm tra\n3. Bấm kiểm tra lại\n"
     "4. Bấm Import",
     "4 dòng như tiền điều kiện",
     "- Sau bước 1: báo 2 hợp lệ, 2 không hợp lệ, nút Import chưa bật\n- Sau bước 3: 4 dòng hợp lệ\n"
     "- Sau bước 4: bảng có thêm đủ 4 dòng"),

    (16, "Import file sai cấu trúc cột", "P1",
     "File Excel bất kỳ không có cột Mã / Tên.",
     "1. Bấm Import Excel, chọn file đó",
     "—",
     "- Hệ thống báo file không đúng mẫu, chỉ rõ thiếu cột nào\n- Không nạp dòng nào vào bảng kiểm tra"),

    (17, "Import file mẫu cũ vẫn đọc được tiêu đề cột", "P2",
     "File mẫu phiên bản cũ có tiêu đề cột 'Mã lĩnh vực kinh doanh nội bộ' / 'Tên lĩnh vực kinh doanh nội bộ', "
     "dữ liệu bên trong đã sửa sang mã LVCTKD.",
     "1. Chọn file đó và bấm kiểm tra dữ liệu",
     "2 dòng mã LVCTKD hợp lệ",
     "- Hệ thống vẫn nhận đúng 2 cột (tiêu đề cũ được chấp nhận)\n- 2 dòng hợp lệ, import được"),

    (18, "Import file rỗng", "P2",
     "File Excel chỉ có dòng tiêu đề, không có dòng dữ liệu.",
     "1. Chọn file và bấm kiểm tra dữ liệu",
     "—",
     "- Hệ thống báo không có dòng dữ liệu nào để nhập\n- Không văng lỗi kỹ thuật"),
]

S8 = [
    (1, "Bỏ trống cả Mã và Tên rồi bấm Lưu", "P0",
     "Đang mở cửa sổ Tạo mới.",
     "1. Không gõ gì (ô Mã chỉ có tiền tố LVCTKD.)\n2. Bấm Lưu",
     "Mã: LVCTKD. · Tên: (trống)",
     "- Cả 2 ô cùng lúc hiện viền đỏ và dòng chữ đỏ 'Bắt buộc phải nhập'\n"
     "- ⚠️ Phải hiện lỗi của CẢ HAI ô ngay lần bấm đầu, không phải sửa xong ô này mới lòi ra lỗi ô kia\n"
     "- Con trỏ nhảy vào ô Mã\n- Cửa sổ không đóng, không tạo bản ghi nào"),

    (2, "Chỉ nhập Mã, bỏ trống Tên", "P0",
     "Đang mở cửa sổ Tạo mới.",
     "1. Gõ mã 'AB12'\n2. Bỏ trống Tên\n3. Bấm Lưu",
     "Mã: LVCTKD.AB12",
     "- Ô Tên hiện lỗi 'Bắt buộc phải nhập'\n- Ô Mã không báo lỗi\n- Không tạo bản ghi"),

    (3, "Chỉ nhập Tên, để ô Mã còn mỗi tiền tố", "P0",
     "Đang mở cửa sổ Tạo mới.",
     "1. Để ô Mã là 'LVCTKD.'\n2. Nhập Tên 'Lĩnh vực thử'\n3. Bấm Lưu",
     "Mã: LVCTKD. · Tên: Lĩnh vực thử",
     "- Ô Mã báo 'Bắt buộc phải nhập'\n"
     "- ⚠️ Không được báo nhầm thành lỗi sai định dạng"),

    (4, "Tên chỉ toàn khoảng trắng", "P1",
     "Đang mở cửa sổ Tạo mới, mã hợp lệ.",
     "1. Gõ vài dấu cách vào ô Tên\n2. Bấm Lưu",
     "Tên: '     '",
     "- Ô Tên báo bắt buộc phải nhập\n- Không tạo bản ghi tên rỗng"),

    (5, "Tên bị cắt khoảng trắng thừa hai đầu", "P1",
     "Chưa có tên 'Cơ khí chính xác'.",
     "1. Nhập mã hợp lệ\n2. Nhập Tên '  Cơ khí chính xác  '\n3. Bấm Lưu\n4. Xem dòng trên bảng",
     "Tên: '  Cơ khí chính xác  '",
     "- Lưu thành công, tên trên bảng là 'Cơ khí chính xác' không còn dấu cách thừa hai đầu"),

    (6, "Tên vượt 255 ký tự", "P0",
     "Đang mở cửa sổ Tạo mới, mã hợp lệ.",
     "1. Dán chuỗi 260 ký tự vào ô Tên\n2. Bấm Lưu",
     "Tên: chuỗi 260 ký tự",
     "- Báo lỗi tên tối đa 255 ký tự ngay dưới ô Tên\n"
     "- ⚠️ Hệ thống KHÔNG được tự cắt bớt chuỗi người dùng đã gõ"),

    (7, "Tên đúng 255 ký tự", "P1",
     "Đang mở cửa sổ Tạo mới, mã hợp lệ.",
     "1. Dán chuỗi đúng 255 ký tự vào ô Tên\n2. Bấm Lưu",
     "Tên: chuỗi 255 ký tự",
     "- Lưu thành công (255 là giới hạn được phép)"),

    (8, "Tên chứa dấu phẩy", "P0",
     "Đang mở cửa sổ Tạo mới, mã hợp lệ.",
     "1. Nhập Tên 'Ô tô, xe máy'\n2. Bấm Lưu",
     "Tên: Ô tô, xe máy",
     "- Báo lỗi tên không được chứa dấu phẩy (,) và dấu hai chấm (:)\n- Nội dung ô giữ nguyên như người dùng gõ"),

    (9, "Tên chứa dấu hai chấm", "P1",
     "Đang mở cửa sổ Tạo mới, mã hợp lệ.",
     "1. Nhập Tên 'Ngành: ô tô'\n2. Bấm Lưu",
     "Tên: Ngành: ô tô",
     "- Báo cùng dòng lỗi như mục 8"),

    (10, "Trùng mã với bản ghi khác", "P0",
     "Đã có bản ghi LVCTKD.OTO.",
     "1. Bấm Tạo mới\n2. Nhập mã 'OTO', tên 'Ô tô mới'\n3. Bấm Lưu",
     "Mã: LVCTKD.OTO",
     "- Dòng đỏ dưới ô Mã: 'Mã lĩnh vực Công ty kinh doanh đã tồn tại'\n- Cửa sổ KHÔNG đóng, dữ liệu đã gõ còn "
     "nguyên\n- Con trỏ nhảy vào ô Mã"),

    (11, "Trùng mã nhưng gõ chữ thường", "P1",
     "Đã có bản ghi LVCTKD.OTO.",
     "1. Bấm Tạo mới\n2. Nhập mã 'oto', tên hợp lệ\n3. Bấm Lưu",
     "Mã gõ: oto",
     "- Vẫn báo trùng mã\n- ⚠️ Không được tạo thêm bản ghi thứ hai chỉ khác nhau chữ hoa - thường"),

    (12, "Trùng tên với bản ghi khác", "P0",
     "Đã có bản ghi tên 'Ô tô'.",
     "1. Bấm Tạo mới\n2. Nhập mã mới hợp lệ, tên 'Ô tô'\n3. Bấm Lưu",
     "Tên: Ô tô",
     "- Dòng đỏ dưới ô Tên: 'Tên lĩnh vực Công ty kinh doanh đã tồn tại'\n- Không tạo bản ghi"),

    (13, "Sửa bản ghi mà giữ nguyên mã và tên của chính nó", "P0",
     "Bản ghi LVCTKD.OTO - Ô tô.",
     "1. Bấm Sửa dòng đó\n2. Không đổi mã và tên, chỉ đổi Trạng thái sang Khoá\n3. Bấm Lưu",
     "—",
     "- Lưu thành công\n- ⚠️ Không được báo trùng mã / trùng tên với chính bản ghi đang sửa"),

    (14, "Sửa tên thành tên của bản ghi khác", "P0",
     "Có LVCTKD.OTO - Ô tô và LVCTKD.ELEC - Điện.",
     "1. Bấm Sửa dòng LVCTKD.ELEC\n2. Đổi tên thành 'Ô tô'\n3. Bấm Lưu",
     "Tên: Ô tô",
     "- Báo tên đã tồn tại, không lưu"),

    (15, "Mã sai định dạng khi gọi thẳng chức năng, bỏ qua giao diện", "P0",
     "Tài khoản có quyền quản lý.",
     "1. Gọi thẳng chức năng Tạo mới với mã không đúng tiền tố, bỏ qua giao diện\n2. Mở lại danh sách",
     "Mã: ABC.XYZ · Tên: Lĩnh vực sai định dạng",
     "- Hệ thống từ chối, báo mã phải bắt đầu bằng LVCTKD.\n- Không có bản ghi nào được tạo\n"
     "- ⚠️ Chốt chặn phải nằm ở phía máy chủ, không chỉ chặn trên giao diện"),

    (16, "Hậu tố quá 4 ký tự khi gọi thẳng chức năng", "P0",
     "Tài khoản có quyền quản lý.",
     "1. Gọi thẳng chức năng Tạo mới với mã LVCTKD.ABCDE, bỏ qua giao diện",
     "Mã: LVCTKD.ABCDE",
     "- Hệ thống từ chối, báo hậu tố tối đa 4 ký tự gồm A-Z, 0-9 và gạch dưới\n- Không tạo bản ghi"),

    (17, "Hậu tố có ký tự tiếng Việt hoặc ký tự đặc biệt", "P1",
     "Đang mở cửa sổ Tạo mới.",
     "1. Gõ 'Ô-T' vào ô Mã\n2. Nhập tên hợp lệ\n3. Bấm Lưu",
     "Mã: LVCTKD.Ô-T",
     "- Báo lỗi ngay dưới ô Mã: hậu tố chỉ gồm chữ không dấu (A-Z), số (0-9) và dấu gạch dưới (_)\n"
     "- Giữ nguyên nội dung người dùng gõ"),

    (18, "Trạng thái không hợp lệ khi gọi thẳng chức năng", "P2",
     "Tài khoản có quyền quản lý.",
     "1. Gọi thẳng chức năng Tạo mới với trạng thái là một giá trị lạ, bỏ qua giao diện",
     "Mã: LVCTKD.ST9 · Tên: Thử trạng thái lạ · Trạng thái: 99",
     "- Hệ thống từ chối, báo trạng thái không hợp lệ\n- Không tạo bản ghi"),
]

S9 = [
    (1, "Hai người cùng sửa một bản ghi", "P1",
     "Người 1 và người 2 cùng mở cửa sổ Sửa bản ghi LVCTKD.OTO.",
     "1. Người 1 đổi tên thành 'Ô tô A' và Lưu\n2. Người 2 (chưa tải lại) đổi tên thành 'Ô tô B' và Lưu\n"
     "3. Cả hai tải lại bảng",
     "Tên: Ô tô A / Ô tô B",
     "- Lần lưu sau ghi đè lần trước: tên cuối cùng là 'Ô tô B'\n- Cột Người cập nhật là người 2, Ngày cập nhật là "
     "thời điểm lưu sau"),

    (2, "Sửa bản ghi vừa bị người khác khoá", "P1",
     "Người 1 đã khoá LVCTKD.OTO; người 2 đang mở cửa sổ Sửa bản ghi đó từ trước.",
     "1. Người 2 đổi tên và bấm Lưu\n2. Người 2 tải lại bảng",
     "Tên: Ô tô sửa muộn",
     "- Hệ thống báo bản ghi đang bị khoá, cần mở khoá trước khi cập nhật\n- Sau khi tải lại, dòng hiện trạng thái "
     "Khoá và chỉ còn nút Mở khoá"),

    (3, "Sửa bản ghi vừa bị người khác xoá", "P1",
     "Người 1 đã xoá LVCTKD.T2; người 2 đang mở cửa sổ Sửa bản ghi đó.",
     "1. Người 2 bấm Lưu",
     "—",
     "- Báo 'Dữ liệu đã thay đổi, vui lòng tải lại'\n- Không tạo lại bản ghi đã xoá"),

    (4, "Mở cửa sổ Xem bản ghi vừa bị xoá", "P2",
     "Người 1 đã xoá LVCTKD.T2; người 2 chưa tải lại bảng.",
     "1. Người 2 bấm vào mã LVCTKD.T2",
     "—",
     "- Báo 'Dữ liệu đã thay đổi, vui lòng tải lại', cửa sổ không mở ra với dữ liệu rỗng"),

    (5, "Bấm Lưu liên tục nhiều lần", "P1",
     "Đang mở cửa sổ Tạo mới với dữ liệu hợp lệ.",
     "1. Bấm nút Lưu 3 lần thật nhanh\n2. Tải lại bảng, tìm theo mã vừa nhập",
     "Mã: LVCTKD.X1 · Tên: Lĩnh vực X1",
     "- Chỉ tạo ra ĐÚNG 1 bản ghi\n- Nút Lưu bị chặn bấm lại trong lúc đang xử lý"),

    (6, "Gõ liên tục ở ô tìm nhanh", "P2",
     "Danh mục có 25 bản ghi.",
     "1. Gõ nhanh 'cong nghiep' từng ký tự một\n2. Quan sát kết quả cuối",
     "Tìm nhanh: cong nghiep",
     "- Kết quả cuối cùng khớp với chuỗi đầy đủ đã gõ\n"
     "- ⚠️ Không bị hiện tượng kết quả của lần gõ trước về sau đè lên kết quả mới"),
]

S10 = [
    (1, "Luồng đầy đủ: tạo - sửa - khoá - mở khoá - xoá", "P0",
     "Tài khoản có quyền quản lý. Chưa có mã LVCTKD.E2E1.",
     "1. Bấm Tạo mới, nhập mã 'E2E1', tên 'Lĩnh vực E2E', bấm Lưu\n2. Bấm Sửa dòng vừa tạo, đổi tên thành "
     "'Lĩnh vực E2E sửa', bấm Lưu\n3. Bấm Khoá dòng đó, xác nhận\n4. Bấm Mở khoá, xác nhận\n5. Bấm Xoá, xác nhận",
     "Mã: LVCTKD.E2E1",
     "- Bước 1: tạo thành công, dòng mới ở đầu danh sách\n- Bước 2: tên đổi, Người cập nhật là tài khoản đang dùng\n"
     "- Bước 3: nhãn chuyển 'Khoá', chỉ còn nút Mở khoá\n- Bước 4: nhãn về 'Hoạt động', hiện lại đủ 3 nút\n"
     "- Bước 5: dòng biến mất khỏi bảng"),

    (2, "Luồng dùng thật với Nhóm ngành", "P0",
     "Chưa có mã LVCTKD.E2E2 và nhóm ngành NN.E2E1.",
     "1. Tạo lĩnh vực LVCTKD.E2E2 - 'Lĩnh vực E2E 2'\n2. Sang màn Nhóm ngành, tạo NN.E2E1 chọn lĩnh vực vừa tạo\n"
     "3. Quay lại màn Lĩnh vực, quan sát dòng LVCTKD.E2E2\n4. Khoá nhóm ngành NN.E2E1, quay lại và quan sát lại\n"
     "5. Xoá nhóm ngành NN.E2E1, quay lại và quan sát lại",
     "Mã: LVCTKD.E2E2 · Nhóm ngành: NN.E2E1",
     "- Bước 3: dòng KHÔNG còn nút Khoá và KHÔNG còn nút Xoá (đang có nhóm ngành hoạt động dùng)\n"
     "- Bước 4: nút Khoá hiện lại, nút Xoá vẫn ẩn (vẫn còn nhóm ngành trỏ tới)\n"
     "- Bước 5: hiện lại đủ cả Khoá và Xoá"),

    (3, "Luồng import rồi xuất lại đối chiếu", "P1",
     "Danh mục đang có 8 bản ghi. File import 2 dòng hợp lệ mã LVCTKD.IM1, LVCTKD.IM2.",
     "1. Import file 2 dòng\n2. Bấm Xuất Excel\n3. Mở file xuất ra và đối chiếu",
     "2 dòng import như tiền điều kiện",
     "- File xuất có đủ 10 dòng, trong đó có LVCTKD.IM1 và LVCTKD.IM2\n- Người tạo của 2 dòng mới là tài khoản "
     "vừa import"),

    (4, "Luồng lọc - sắp xếp - phân trang giữ đúng nhau", "P1",
     "Danh mục 25 bản ghi, 18 bản ghi Hoạt động.",
     "1. Lọc Trạng thái = Hoạt động\n2. Sắp xếp theo Mã tăng dần\n3. Sang trang 2\n4. Bấm Làm mới",
     "Trạng thái: Hoạt động",
     "- Bước 3: trang 2 vẫn chỉ gồm bản ghi Hoạt động, thứ tự nối tiếp trang 1\n"
     "- Bước 4: mọi điều kiện lọc bị xoá, bảng về trang 1 với đủ 25 bản ghi"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "TẠO MỚI / SỬA / XEM", S4),
    ("V", "KHOÁ / MỞ KHOÁ", S5),
    ("VI", "XÓA", S6),
    ("VII", "XUẤT EXCEL / IMPORT EXCEL", S7),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", S8),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "E2E FLOW", S10),
]

if __name__ == "__main__":
    build(output_file=OUT, sheet_name="Trang tính1", feature_name=FEATURE, module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
