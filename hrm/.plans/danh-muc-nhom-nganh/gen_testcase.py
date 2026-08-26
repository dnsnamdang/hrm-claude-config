# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho thay đổi: Danh mục Nhóm ngành bổ sung Lĩnh vực kinh doanh nội bộ.

Chạy: python3 .plans/danh-muc-nhom-nganh/gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

MODULE = "DM Nhóm ngành"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Mỗi Nhóm ngành phải gắn với đúng 1 Lĩnh vực kinh doanh nội bộ, để lọc và thống kê nhóm ngành "
     "theo lĩnh vực kinh doanh của công ty.\n"
     "Phạm vi thay đổi lần này: (a) form Thêm mới / Sửa nhóm ngành có thêm ô chọn Lĩnh vực kinh doanh "
     "nội bộ và được bố trí lại; (b) danh sách nhóm ngành thêm cột Lĩnh vực kinh doanh nội bộ; "
     "(c) bộ lọc thêm tiêu chí Lĩnh vực kinh doanh nội bộ; (d) Nhập từ Excel và Xuất Excel có thêm "
     "trường lĩnh vực; (e) Lĩnh vực kinh doanh nội bộ đang được nhóm ngành sử dụng thì không được "
     "Xoá / Khoá."),
    ("2. Đối tượng được tính / hiển thị",
     "- Ô chọn Lĩnh vực kinh doanh nội bộ trong form: chỉ liệt kê lĩnh vực đang ở trạng thái Hoạt động.\n"
     "- Trường hợp mở Sửa / Xem một nhóm ngành đang gắn lĩnh vực nay đã bị Khoá: lĩnh vực đó VẪN nằm "
     "trong danh sách chọn và hiển thị đúng tên, kèm biểu tượng ổ khoá trong danh sách xổ xuống.\n"
     "- Cột Lĩnh vực kinh doanh nội bộ trên lưới: hiện tên lĩnh vực đang gắn của từng nhóm ngành.\n"
     "- Bộ lọc Lĩnh vực kinh doanh nội bộ: liệt kê các lĩnh vực đang Hoạt động.\n"
     "- Nhóm ngành cũ (có trước thay đổi này) được hệ thống gán sẵn lĩnh vực mặc định tên \"Khác\"."),
    ("3. Đối tượng bị ẩn / không tính",
     "- Lĩnh vực kinh doanh nội bộ đang ở trạng thái Khoá: KHÔNG xuất hiện trong ô chọn khi tạo mới, "
     "KHÔNG xuất hiện trong danh sách chọn của bộ lọc (trừ trường hợp đang được bản ghi mở ra gắn sẵn).\n"
     "- Ở màn Lĩnh vực kinh doanh nội bộ: nút Xoá bị ẩn với lĩnh vực đã có nhóm ngành sử dụng; nút Khoá "
     "bị ẩn khi còn nhóm ngành đang Hoạt động dùng lĩnh vực đó."),
    ("4. Bộ lọc thời gian áp dụng cho",
     "Không thay đổi so với trước: 2 ô Cập nhật từ / Cập nhật đến vẫn lọc theo ngày cập nhật gần nhất "
     "của nhóm ngành. Thay đổi lần này không thêm bộ lọc thời gian mới."),
    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Quan hệ 1 - nhiều: 1 Lĩnh vực kinh doanh nội bộ có nhiều Nhóm ngành; 1 Nhóm ngành chỉ thuộc "
     "đúng 1 Lĩnh vực kinh doanh nội bộ (không cho chọn nhiều). Bên dưới Nhóm ngành vẫn là Nhóm giải "
     "pháp và Ứng dụng như cũ, thay đổi lần này không đụng tới 2 cấp đó."),
    ("6. Quy tắc cộng dồn / deduplicate",
     "Không áp dụng — màn danh sách nhóm ngành liệt kê từng bản ghi, không cộng dồn số liệu. "
     "Hai cột Số nhóm giải pháp / Số ứng dụng giữ nguyên cách đếm cũ."),
    ("7. Phân quyền cấp",
     "- Quản lý danh mục nhóm ngành: xem danh sách, Tạo mới, Sửa, Xoá, Khoá / Mở khoá, Nhập từ Excel, Xuất Excel.\n"
     "- Xem danh mục nhóm ngành: chỉ xem danh sách và xem chi tiết.\n"
     "- Quản lý danh mục lĩnh vực kinh doanh nội bộ: thao tác trên màn danh mục Lĩnh vực kinh doanh nội bộ.\n"
     "- Xem danh mục lĩnh vực kinh doanh nội bộ: chỉ xem màn danh mục Lĩnh vực kinh doanh nội bộ.\n"
     "Người dùng không có quyền nào trong nhóm trên thì không thấy mục menu tương ứng và bị hệ thống "
     "từ chối khi mở thẳng đường dẫn."),
    ("8. Cách tính các ô thống kê",
     "- Dòng đếm dưới lưới: \"Hiển thị a–b / N nhóm ngành\" — a là số thứ tự dòng đầu của trang đang xem, "
     "b là dòng cuối, N là tổng số nhóm ngành khớp bộ lọc đang áp dụng (kể cả bộ lọc Lĩnh vực kinh doanh nội bộ).\n"
     "- Cột Số nhóm giải pháp / Số ứng dụng: giữ nguyên cách tính cũ, không đổi theo lĩnh vực."),
    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai của lần thay đổi này:\n"
     "- Nhóm ngành cũ được gán sẵn lĩnh vực \"Khác\" — đừng coi đó là dữ liệu người dùng tự nhập.\n"
     "- Ô chọn lĩnh vực là BẮT BUỘC: bỏ trống khi Lưu phải báo lỗi đỏ ngay dưới ô, cửa sổ không đóng.\n"
     "- Chỉ được chọn 1 lĩnh vực; ô chọn không cho bỏ chọn về rỗng sau khi đã chọn.\n"
     "- Lĩnh vực bị Khoá vẫn phải hiện đúng tên ở nhóm ngành đang gắn nó; lưu lại không được làm mất giá trị.\n"
     "- Bố cục cửa sổ Thêm/Sửa sau khi bố trí lại: hàng 1 Mã nhóm ngành + Tên nhóm ngành; hàng 2 "
     "Lĩnh vực kinh doanh nội bộ + Trạng thái; hàng 3 Mô tả chiếm hết chiều ngang.\n"
     "- File Excel mẫu để nhập liệu đã thêm cột Mã lĩnh vực kinh doanh nội bộ — phải tải lại file mẫu mới, "
     "dùng file mẫu cũ sẽ thiếu cột và báo lỗi.\n"
     "- Nhập từ Excel chỉ bấm Nhập được khi không còn dòng lỗi."),
]

ROLE_TCS = [
    ("00", "Tài khoản có quyền Quản lý danh mục nhóm ngành", "P0",
     "Tài khoản A chỉ có quyền Quản lý danh mục nhóm ngành. Danh mục có sẵn 22 nhóm ngành và 3 lĩnh vực "
     "kinh doanh nội bộ đang Hoạt động.",
     "1. Đăng nhập bằng tài khoản A\n2. Vào Dự án & Giao việc > Danh mục > Nhóm ngành\n"
     "3. Quan sát lưới và các nút trên thanh công cụ\n4. Bấm Tạo mới",
     "—",
     "- Thấy mục menu Nhóm ngành và mở được màn danh sách\n"
     "- Lưới có cột Lĩnh vực kinh doanh nội bộ\n"
     "- Thấy đủ nút Tạo mới, Nhập từ Excel, Xuất Excel và các nút Sửa / Xoá trên từng dòng\n"
     "- Cửa sổ Tạo mới mở được, có ô Lĩnh vực kinh doanh nội bộ kèm dấu sao đỏ"),
    ("01", "Tài khoản chỉ có quyền Xem danh mục nhóm ngành", "P0",
     "Tài khoản B chỉ có quyền Xem danh mục nhóm ngành, không có quyền Quản lý.",
     "1. Đăng nhập bằng tài khoản B\n2. Mở màn Nhóm ngành\n3. Quan sát thanh công cụ và cột Hành động",
     "—",
     "- Xem được danh sách và cột Lĩnh vực kinh doanh nội bộ\n"
     "- KHÔNG thấy nút Tạo mới, Nhập từ Excel\n"
     "- KHÔNG thấy nút Sửa / Xoá trên từng dòng\n"
     "- ⚠️ Nút bị ẩn hẳn, không phải hiện màu xám"),
    ("02", "Tài khoản không có quyền nào của danh mục nhóm ngành", "P0",
     "Tài khoản C không có cả 2 quyền Quản lý / Xem danh mục nhóm ngành.",
     "1. Đăng nhập bằng tài khoản C\n2. Mở menu Danh mục\n3. Gõ thẳng đường dẫn màn Nhóm ngành lên thanh địa chỉ",
     "—",
     "- Menu Danh mục không có mục Nhóm ngành\n"
     "- Mở thẳng đường dẫn: hệ thống từ chối, báo không có quyền, không hiện dữ liệu nhóm ngành nào"),
    ("03", "Tài khoản chỉ có quyền Xem lĩnh vực kinh doanh nội bộ", "P1",
     "Tài khoản D có quyền Xem danh mục lĩnh vực kinh doanh nội bộ, không có quyền Quản lý danh mục đó.",
     "1. Đăng nhập bằng tài khoản D\n2. Vào Danh mục > Lĩnh vực kinh doanh nội bộ",
     "—",
     "- Xem được danh sách lĩnh vực\n- KHÔNG thấy nút Tạo mới / Sửa / Xoá / Khoá"),
    ("04", "Chặn thao tác ghi khi bỏ qua giao diện — Sửa nhóm ngành", "P0",
     "Tài khoản B chỉ có quyền Xem danh mục nhóm ngành. Có nhóm ngành \"NN.0001\" đang Hoạt động.",
     "1. Đăng nhập bằng tài khoản B\n2. Dùng công cụ kiểm thử giao tiếp dữ liệu gọi thẳng chức năng Sửa "
     "nhóm ngành, bỏ qua giao diện, gửi kèm một lĩnh vực kinh doanh nội bộ hợp lệ",
     "Nhóm ngành: NN.0001 · Lĩnh vực gửi lên: Khác",
     "- Hệ thống từ chối, báo không có quyền\n- Mở lại màn danh sách: nhóm ngành NN.0001 giữ nguyên "
     "lĩnh vực cũ, không bị đổi"),
    ("05", "Chặn thao tác ghi khi bỏ qua giao diện — Xoá lĩnh vực kinh doanh nội bộ", "P0",
     "Tài khoản C không có quyền Quản lý danh mục lĩnh vực kinh doanh nội bộ. Lĩnh vực \"Khác\" đang "
     "được 22 nhóm ngành sử dụng.",
     "1. Đăng nhập bằng tài khoản C\n2. Dùng công cụ kiểm thử giao tiếp dữ liệu gọi thẳng chức năng Xoá "
     "lĩnh vực \"Khác\", bỏ qua giao diện",
     "Lĩnh vực: Khác",
     "- Hệ thống từ chối, báo không có quyền\n- Lĩnh vực \"Khác\" vẫn còn trong danh mục"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", [
        ("001", "Lưới nhóm ngành có cột Lĩnh vực kinh doanh nội bộ đúng vị trí", "P0",
         "Tài khoản có quyền Quản lý danh mục nhóm ngành. Danh mục có 22 nhóm ngành.",
         "1. Mở màn Nhóm ngành\n2. Quan sát tiêu đề các cột trên lưới",
         "—",
         "- Có cột \"Lĩnh vực kinh doanh nội bộ\" nằm ngay sau cột \"Mã nhóm ngành - Tên nhóm ngành\"\n"
         "- Cột nằm trước cột Số nhóm giải pháp"),
        ("002", "Nhóm ngành cũ hiển thị lĩnh vực mặc định \"Khác\"", "P0",
         "22 nhóm ngành có sẵn từ trước thay đổi này, chưa ai chọn lĩnh vực thủ công.",
         "1. Mở màn Nhóm ngành\n2. Đọc cột Lĩnh vực kinh doanh nội bộ của 22 dòng",
         "—",
         "- Tất cả 22 dòng đều hiện \"Khác\"\n- Không dòng nào để trống hay hiện dấu gạch ngang"),
        ("003", "Nhóm ngành chưa gắn lĩnh vực hiển thị dấu gạch ngang", "P2",
         "Có 1 nhóm ngành bị xoá lĩnh vực trực tiếp dưới dữ liệu (tình huống dữ liệu lỗi).",
         "1. Mở màn Nhóm ngành\n2. Tìm dòng đó và đọc cột Lĩnh vực kinh doanh nội bộ",
         "—",
         "- Ô hiển thị \"—\", không để trống trơn và không làm vỡ lưới"),
        ("004", "Bố cục cửa sổ Tạo mới sau khi bố trí lại", "P0",
         "Tài khoản có quyền Quản lý danh mục nhóm ngành.",
         "1. Mở màn Nhóm ngành\n2. Bấm Tạo mới\n3. Quan sát thứ tự và độ rộng các ô",
         "—",
         "- Hàng 1: Mã nhóm ngành (hẹp) và Tên nhóm ngành (rộng gấp đôi)\n"
         "- Hàng 2: Lĩnh vực kinh doanh nội bộ (rộng) và Trạng thái (hẹp)\n"
         "- Hàng 3: Mô tả chiếm hết chiều ngang\n"
         "- ⚠️ Không còn ô nào nằm lẻ một mình gây khoảng trống lớn bên phải"),
        ("005", "Nhãn bắt buộc của ô Lĩnh vực kinh doanh nội bộ", "P0",
         "Tài khoản có quyền Quản lý danh mục nhóm ngành.",
         "1. Bấm Tạo mới\n2. Quan sát nhãn ô Lĩnh vực kinh doanh nội bộ",
         "—",
         "- Nhãn có dấu sao đỏ (*) như Mã nhóm ngành và Tên nhóm ngành\n"
         "- Ô có dòng gợi ý \"Chọn lĩnh vực kinh doanh nội bộ\" khi chưa chọn"),
        ("006", "Cửa sổ Xem chi tiết hiển thị lĩnh vực ở dạng chỉ đọc", "P1",
         "Nhóm ngành NN.0001 đang gắn lĩnh vực \"Khác\".",
         "1. Mở màn Nhóm ngành\n2. Bấm nút Xem (biểu tượng con mắt) ở dòng NN.0001",
         "—",
         "- Ô Lĩnh vực kinh doanh nội bộ hiện \"Khác\" và bị khoá không sửa được\n"
         "- Không có nút Lưu, chỉ có nút Đóng"),
    ]),
    ("II", "BỘ LỌC & TÌM KIẾM", [
        ("001", "Bộ lọc có tiêu chí Lĩnh vực kinh doanh nội bộ", "P0",
         "Danh mục có 3 lĩnh vực đang Hoạt động: Khác, Ô tô - Xe máy, Điện - Tự động hóa.",
         "1. Mở màn Nhóm ngành\n2. Bấm Tìm kiếm nâng cao\n3. Quan sát các ô lọc",
         "—",
         "- Có ô lọc \"Lĩnh vực kinh doanh nội bộ\" với dòng gợi ý \"Chọn lĩnh vực kinh doanh nội bộ\"\n"
         "- Danh sách xổ xuống liệt kê đủ 3 lĩnh vực đang Hoạt động"),
        ("002", "Lọc ra đúng nhóm ngành của lĩnh vực đã chọn", "P0",
         "22 nhóm ngành gắn lĩnh vực \"Khác\"; 1 nhóm ngành NN.T001 gắn \"Ô tô - Xe máy\".",
         "1. Bấm Tìm kiếm nâng cao\n2. Chọn Lĩnh vực kinh doanh nội bộ = Ô tô - Xe máy",
         "Lĩnh vực: Ô tô - Xe máy",
         "- Lưới còn đúng 1 dòng NN.T001\n- Dòng đếm dưới lưới hiện tổng là 1\n"
         "- ⚠️ Không cần bấm nút Tìm kiếm, chọn xong lưới tự lọc"),
        ("003", "Lọc theo lĩnh vực không có nhóm ngành nào", "P1",
         "Lĩnh vực \"Điện - Tự động hóa\" chưa có nhóm ngành nào gắn.",
         "1. Bấm Tìm kiếm nâng cao\n2. Chọn Lĩnh vực kinh doanh nội bộ = Điện - Tự động hóa",
         "Lĩnh vực: Điện - Tự động hóa",
         "- Lưới hiện dòng thông báo không có dữ liệu phù hợp bộ lọc\n- Không báo lỗi, không treo trang"),
        ("004", "Bỏ chọn lĩnh vực thì danh sách trở lại đầy đủ", "P0",
         "Đang lọc theo lĩnh vực \"Ô tô - Xe máy\", lưới còn 1 dòng.",
         "1. Bấm dấu × trên ô lọc Lĩnh vực kinh doanh nội bộ",
         "—",
         "- Lưới nạp lại đủ 23 nhóm ngành\n- Dòng đếm dưới lưới cập nhật đúng tổng"),
        ("005", "Kết hợp lọc Lĩnh vực với lọc Trạng thái", "P1",
         "Lĩnh vực \"Khác\" có 22 nhóm ngành: 21 Hoạt động, 1 Khoá.",
         "1. Bấm Tìm kiếm nâng cao\n2. Chọn Lĩnh vực = Khác\n3. Chọn Trạng thái = Khoá",
         "Lĩnh vực: Khác · Trạng thái: Khoá",
         "- Lưới chỉ còn nhóm ngành vừa Khoá\n- 2 điều kiện lọc cùng có hiệu lực, không cái nào ghi đè cái nào"),
        ("006", "Làm mới xoá cả tiêu chí lĩnh vực", "P0",
         "Đang lọc theo Lĩnh vực = Khác và có từ khoá tìm nhanh.",
         "1. Bấm nút Làm mới",
         "—",
         "- Ô lọc Lĩnh vực kinh doanh nội bộ trở về dòng gợi ý ban đầu\n"
         "- Ô tìm nhanh trống\n- Lưới nạp lại đầy đủ danh sách"),
        ("007", "Lĩnh vực đang Khoá không xuất hiện trong ô lọc", "P1",
         "Lĩnh vực \"Điện - Tự động hóa\" đã bị Khoá.",
         "1. Bấm Tìm kiếm nâng cao\n2. Mở danh sách xổ xuống của ô lọc Lĩnh vực kinh doanh nội bộ",
         "—",
         "- Danh sách chỉ còn các lĩnh vực đang Hoạt động\n- Không thấy \"Điện - Tự động hóa\""),
    ]),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", [
        ("001", "Thêm cột mới không làm hỏng sắp xếp sẵn có", "P1",
         "Danh mục có 23 nhóm ngành.",
         "1. Mở màn Nhóm ngành\n2. Bấm sắp xếp trên cột Cập nhật",
         "—",
         "- Danh sách sắp xếp đúng theo ngày cập nhật\n- Cột Lĩnh vực kinh doanh nội bộ vẫn hiển thị đúng "
         "tên lĩnh vực của từng dòng sau khi sắp xếp"),
        ("002", "Phân trang giữ nguyên bộ lọc lĩnh vực", "P1",
         "Lĩnh vực \"Khác\" có 22 nhóm ngành, mỗi trang 10 dòng.",
         "1. Lọc theo Lĩnh vực = Khác\n2. Chuyển sang trang 2 rồi trang 3",
         "Lĩnh vực: Khác · Số dòng/trang: 10",
         "- Mọi dòng ở cả 3 trang đều thuộc lĩnh vực Khác\n- Dòng đếm hiện đúng tổng 22"),
        ("003", "Đổi số dòng mỗi trang khi đang lọc theo lĩnh vực", "P2",
         "Đang lọc Lĩnh vực = Khác (22 dòng).",
         "1. Đổi Số dòng/trang sang 20\n2. Quan sát lưới",
         "Số dòng/trang: 20",
         "- Trang 1 hiện 20 dòng, tất cả thuộc lĩnh vực Khác\n- Tổng vẫn là 22"),
    ]),
    ("IV", "CHỨC NĂNG CHÍNH (TẠO / SỬA / XEM)", [
        ("001", "Tạo mới nhóm ngành có chọn lĩnh vực", "P0",
         "Tài khoản có quyền Quản lý danh mục nhóm ngành. Lĩnh vực \"Ô tô - Xe máy\" đang Hoạt động.",
         "1. Bấm Tạo mới\n2. Nhập Mã nhóm ngành\n3. Nhập Tên nhóm ngành\n"
         "4. Chọn Lĩnh vực kinh doanh nội bộ\n5. Bấm Lưu",
         "Mã: NN.OTO1 · Tên: Nhóm ngành ô tô · Lĩnh vực: Ô tô - Xe máy",
         "- Hệ thống báo thêm mới thành công, cửa sổ đóng\n"
         "- Dòng mới đứng đầu danh sách, cột Lĩnh vực kinh doanh nội bộ hiện \"Ô tô - Xe máy\""),
        ("002", "Bỏ trống lĩnh vực khi Lưu", "P0",
         "Tài khoản có quyền Quản lý danh mục nhóm ngành.",
         "1. Bấm Tạo mới\n2. Nhập Mã và Tên nhóm ngành hợp lệ\n3. KHÔNG chọn lĩnh vực\n4. Bấm Lưu",
         "Mã: NN.NOLV · Tên: Nhóm ngành thiếu lĩnh vực · Lĩnh vực: (bỏ trống)",
         "- Hệ thống báo lỗi đỏ \"Bắt buộc phải chọn\" ngay dưới ô Lĩnh vực kinh doanh nội bộ\n"
         "- Cửa sổ KHÔNG đóng, dữ liệu Mã và Tên đã nhập vẫn còn\n- Không có bản ghi nào được tạo"),
        ("003", "Chỉ chọn được 1 lĩnh vực", "P0",
         "Danh mục có 3 lĩnh vực đang Hoạt động.",
         "1. Bấm Tạo mới\n2. Mở ô Lĩnh vực kinh doanh nội bộ, chọn \"Khác\"\n"
         "3. Mở lại ô đó, chọn tiếp \"Ô tô - Xe máy\"",
         "Lĩnh vực chọn lần 1: Khác · lần 2: Ô tô - Xe máy",
         "- Ô chỉ giữ lại giá trị chọn sau cùng là \"Ô tô - Xe máy\"\n"
         "- ⚠️ Không cho phép hiện 2 lĩnh vực cùng lúc trong ô"),
        ("004", "Sửa nhóm ngành: ô lĩnh vực hiện sẵn giá trị đang gắn", "P0",
         "Nhóm ngành NN.0001 đang gắn lĩnh vực \"Khác\".",
         "1. Bấm nút Sửa (biểu tượng bút chì) ở dòng NN.0001\n2. Quan sát ô Lĩnh vực kinh doanh nội bộ",
         "—",
         "- Ô hiện sẵn \"Khác\"\n- Không bị trống, không tự nhảy sang lĩnh vực khác"),
        ("005", "Đổi lĩnh vực của nhóm ngành đã có", "P0",
         "Nhóm ngành NN.0001 đang gắn \"Khác\"; lĩnh vực \"Ô tô - Xe máy\" đang Hoạt động.",
         "1. Bấm Sửa ở dòng NN.0001\n2. Đổi Lĩnh vực sang \"Ô tô - Xe máy\"\n3. Bấm Lưu\n"
         "4. Quan sát dòng NN.0001 trên lưới",
         "Lĩnh vực mới: Ô tô - Xe máy",
         "- Hệ thống báo cập nhật thành công\n- Cột Lĩnh vực kinh doanh nội bộ của dòng đổi thành \"Ô tô - Xe máy\"\n"
         "- Cột Cập nhật hiện tên người vừa sửa và thời điểm vừa lưu"),
        ("006", "Lưu & Tiếp tục giữ cửa sổ mở và xoá trắng ô lĩnh vực", "P1",
         "Tài khoản có quyền Quản lý danh mục nhóm ngành.",
         "1. Bấm Tạo mới\n2. Nhập đủ Mã, Tên, chọn Lĩnh vực\n3. Bấm Lưu & Tiếp tục\n4. Quan sát cửa sổ",
         "Mã: NN.LT01 · Tên: Nhóm ngành lưu tiếp · Lĩnh vực: Khác",
         "- Báo thêm mới thành công, cửa sổ vẫn mở để nhập bản ghi kế tiếp\n"
         "- Các ô Mã, Tên, Lĩnh vực đều trở về trạng thái trống ban đầu"),
        ("007", "Thoát không lưu thì không đổi lĩnh vực", "P1",
         "Nhóm ngành NN.0002 đang gắn \"Khác\".",
         "1. Bấm Sửa ở dòng NN.0002\n2. Đổi Lĩnh vực sang \"Ô tô - Xe máy\"\n3. Bấm Đóng\n"
         "4. Xem lại dòng NN.0002",
         "—",
         "- Cột Lĩnh vực vẫn là \"Khác\"\n- Không có thông báo lưu thành công"),
    ]),
    ("V", "CÁC THAO TÁC TRẠNG THÁI", [
        ("001", "Lĩnh vực bị Khoá vẫn hiện đúng tên ở nhóm ngành đang gắn", "P0",
         "Nhóm ngành NN.T002 đang gắn lĩnh vực \"Ô tô - Xe máy\"; sau đó lĩnh vực này bị Khoá.",
         "1. Mở màn Nhóm ngành\n2. Đọc cột Lĩnh vực của dòng NN.T002\n3. Bấm Sửa dòng đó",
         "—",
         "- Trên lưới: cột Lĩnh vực vẫn hiện \"Ô tô - Xe máy\", không để trống\n"
         "- Trong cửa sổ Sửa: ô Lĩnh vực vẫn hiện \"Ô tô - Xe máy\"\n"
         "- ⚠️ Tên hiển thị là tên gốc, không bị thêm chữ \"(đã khoá)\""),
        ("002", "Lưu lại nhóm ngành mà không đổi lĩnh vực đã khoá", "P0",
         "Nhóm ngành NN.T002 gắn lĩnh vực \"Ô tô - Xe máy\" đang bị Khoá.",
         "1. Bấm Sửa dòng NN.T002\n2. Chỉ sửa Tên nhóm ngành\n3. Bấm Lưu",
         "Tên mới: Nhóm ngành ô tô (đổi tên)",
         "- Lưu thành công, không bắt phải đổi lĩnh vực\n"
         "- Cột Lĩnh vực giữ nguyên \"Ô tô - Xe máy\", KHÔNG bị xoá mất"),
        ("003", "Không cho chọn mới một lĩnh vực đang Khoá", "P0",
         "Lĩnh vực \"Điện - Tự động hóa\" đang bị Khoá.",
         "1. Bấm Tạo mới\n2. Mở danh sách xổ xuống ô Lĩnh vực kinh doanh nội bộ",
         "—",
         "- Danh sách không có \"Điện - Tự động hóa\"\n- Chỉ liệt kê lĩnh vực đang Hoạt động"),
        ("004", "Ẩn nút Khoá của lĩnh vực còn nhóm ngành đang hoạt động", "P0",
         "Lĩnh vực \"Khác\" đang được 22 nhóm ngành Hoạt động sử dụng.",
         "1. Vào Danh mục > Lĩnh vực kinh doanh nội bộ\n2. Quan sát cột Hành động của dòng \"Khác\"",
         "—",
         "- Dòng \"Khác\" chỉ còn nút Sửa\n- Nút Khoá và nút Xoá bị ẩn hẳn\n"
         "- ⚠️ Nút bị ẩn chứ không phải hiện màu xám"),
        ("005", "Khoá được lĩnh vực sau khi gỡ hết nhóm ngành", "P0",
         "Lĩnh vực \"Ô tô - Xe máy\" chỉ còn 1 nhóm ngành NN.T001 sử dụng.",
         "1. Xoá nhóm ngành NN.T001\n2. Vào Danh mục > Lĩnh vực kinh doanh nội bộ\n"
         "3. Bấm Khoá ở dòng \"Ô tô - Xe máy\" và xác nhận",
         "—",
         "- Nút Khoá đã hiện trở lại sau khi gỡ liên kết\n- Khoá thành công, trạng thái đổi sang Khoá"),
        ("006", "Chặn khoá lĩnh vực khi bỏ qua giao diện", "P1",
         "Lĩnh vực \"Khác\" đang được 22 nhóm ngành Hoạt động sử dụng.",
         "1. Dùng công cụ kiểm thử giao tiếp dữ liệu gọi thẳng chức năng Khoá lĩnh vực \"Khác\", bỏ qua giao diện",
         "Lĩnh vực: Khác",
         "- Hệ thống từ chối, báo dữ liệu đang được sử dụng\n- Lĩnh vực \"Khác\" vẫn ở trạng thái Hoạt động"),
        ("007", "Khoá nhóm ngành không ảnh hưởng lĩnh vực đang gắn", "P2",
         "Nhóm ngành NN.0003 đang gắn \"Khác\".",
         "1. Khoá nhóm ngành NN.0003\n2. Đọc lại dòng đó",
         "—",
         "- Trạng thái nhóm ngành chuyển sang Khoá\n- Cột Lĩnh vực vẫn hiện \"Khác\""),
    ]),
    ("VI", "XÓA", [
        ("001", "Chặn xoá lĩnh vực đang được nhóm ngành sử dụng", "P0",
         "Lĩnh vực \"Khác\" đang được 22 nhóm ngành sử dụng.",
         "1. Vào Danh mục > Lĩnh vực kinh doanh nội bộ\n2. Tìm dòng \"Khác\"\n3. Quan sát cột Hành động",
         "—",
         "- Nút Xoá của dòng \"Khác\" bị ẩn\n"
         "- Gọi thẳng chức năng Xoá bằng công cụ kiểm thử, bỏ qua giao diện: hệ thống từ chối và báo "
         "dữ liệu đang được sử dụng"),
        ("002", "Xoá được lĩnh vực chưa có nhóm ngành nào dùng", "P1",
         "Lĩnh vực \"Điện - Tự động hóa\" chưa có nhóm ngành nào gắn, đang Hoạt động.",
         "1. Vào Danh mục > Lĩnh vực kinh doanh nội bộ\n2. Bấm Xoá ở dòng đó và xác nhận",
         "—",
         "- Xoá thành công, dòng biến mất khỏi danh sách\n"
         "- Mở màn Nhóm ngành: không dòng nào bị mất lĩnh vực"),
        ("003", "Xoá nhóm ngành làm giảm số liên kết của lĩnh vực", "P1",
         "Lĩnh vực \"Ô tô - Xe máy\" đang có đúng 1 nhóm ngành NN.T001.",
         "1. Xoá nhóm ngành NN.T001 và xác nhận\n2. Vào Danh mục > Lĩnh vực kinh doanh nội bộ",
         "—",
         "- Nhóm ngành bị xoá khỏi danh sách\n- Dòng \"Ô tô - Xe máy\" hiện lại đủ nút Sửa, Khoá, Xoá"),
    ]),
    ("VII", "XUẤT EXCEL & NHẬP TỪ EXCEL", [
        ("001", "File xuất có cột Lĩnh vực kinh doanh nội bộ", "P0",
         "Danh mục có 23 nhóm ngành, mỗi nhóm đã gắn lĩnh vực.",
         "1. Mở màn Nhóm ngành\n2. Bấm Xuất Excel\n3. Mở file tải về",
         "—",
         "- File có cột \"Lĩnh vực kinh doanh nội bộ\" đặt sau cột Tên nhóm ngành\n"
         "- Mỗi dòng hiện đúng tên lĩnh vực như trên lưới\n- Các cột cũ không bị lệch nội dung"),
        ("002", "Xuất Excel theo đúng bộ lọc lĩnh vực đang áp dụng", "P1",
         "Đang lọc Lĩnh vực = Ô tô - Xe máy, lưới còn 1 dòng.",
         "1. Bấm Xuất Excel\n2. Mở file tải về",
         "Lĩnh vực: Ô tô - Xe máy",
         "- File chỉ có 1 dòng dữ liệu đúng nhóm ngành đang hiển thị\n- Không xuất cả 23 dòng"),
        ("003", "File mẫu nhập liệu đã có cột mã lĩnh vực", "P0",
         "Tài khoản có quyền Quản lý danh mục nhóm ngành.",
         "1. Bấm Nhập từ Excel\n2. Bấm Tải file mẫu\n3. Mở file mẫu",
         "—",
         "- Tải về được file mẫu nhóm ngành\n"
         "- File có cột \"Mã lĩnh vực kinh doanh nội bộ *\" nằm sau cột Tên nhóm ngành\n"
         "- Dòng hướng dẫn ghi rõ phải nhập mã lĩnh vực đang hoạt động\n"
         "- 2 dòng mẫu đã điền sẵn mã lĩnh vực"),
        ("004", "Nhập từ Excel thành công theo mã lĩnh vực", "P0",
         "Lĩnh vực có mã LVKDNB.KHAC đang Hoạt động; mã nhóm ngành NN.IM01 chưa tồn tại.",
         "1. Bấm Nhập từ Excel\n2. Chọn file đã điền 1 dòng hợp lệ\n3. Bấm Load lên bảng\n"
         "4. Bấm Kiểm tra dữ liệu\n5. Bấm Nhập",
         "Mã: NN.IM01 · Tên: Nhóm ngành nhập file · Mã lĩnh vực: LVKDNB.KHAC · Trạng thái: Hoạt động",
         "- Bảng xem trước hiện đúng 1 dòng, không dòng lỗi\n- Nhập thành công, cửa sổ đóng\n"
         "- Dòng mới trên lưới có cột Lĩnh vực kinh doanh nội bộ hiện \"Khác\""),
        ("005", "Nhập từ Excel thiếu mã lĩnh vực", "P0",
         "File nhập liệu có 1 dòng bỏ trống cột mã lĩnh vực.",
         "1. Bấm Nhập từ Excel\n2. Chọn file\n3. Bấm Load lên bảng\n4. Bấm Kiểm tra dữ liệu",
         "Mã: NN.IM02 · Tên: Nhóm ngành thiếu lĩnh vực · Mã lĩnh vực: (bỏ trống)",
         "- Dòng bị đánh dấu lỗi màu đỏ với nội dung báo mã lĩnh vực kinh doanh nội bộ không được để trống\n"
         "- ⚠️ Nút Nhập bị mờ, chỉ bấm được khi không còn dòng lỗi"),
        ("006", "Nhập từ Excel với mã lĩnh vực không tồn tại", "P0",
         "Không có lĩnh vực nào mang mã LVKDNB.ZZZZ.",
         "1. Bấm Nhập từ Excel\n2. Chọn file có dòng ghi mã LVKDNB.ZZZZ\n3. Bấm Load lên bảng\n"
         "4. Bấm Kiểm tra dữ liệu",
         "Mã: NN.IM03 · Mã lĩnh vực: LVKDNB.ZZZZ",
         "- Dòng bị đánh dấu lỗi, nội dung báo lĩnh vực kinh doanh nội bộ không tồn tại\n"
         "- Không bản ghi nào được tạo"),
        ("007", "Nhập từ Excel với mã lĩnh vực đang bị Khoá", "P1",
         "Lĩnh vực mã LVKDNB.ELEC đang ở trạng thái Khoá.",
         "1. Bấm Nhập từ Excel\n2. Chọn file có dòng ghi mã LVKDNB.ELEC\n3. Bấm Load lên bảng\n"
         "4. Bấm Kiểm tra dữ liệu",
         "Mã: NN.IM04 · Mã lĩnh vực: LVKDNB.ELEC",
         "- Dòng bị đánh dấu lỗi, nội dung báo lĩnh vực đã bị khoá\n- Không bản ghi nào được tạo"),
        ("008", "Dùng file mẫu cũ (thiếu cột lĩnh vực)", "P1",
         "Người dùng còn giữ file mẫu tải về từ trước thay đổi này.",
         "1. Bấm Nhập từ Excel\n2. Chọn file mẫu cũ\n3. Bấm Load lên bảng\n4. Bấm Kiểm tra dữ liệu",
         "File mẫu cũ: không có cột Mã lĩnh vực kinh doanh nội bộ",
         "- Mọi dòng đều bị đánh dấu lỗi thiếu mã lĩnh vực\n"
         "- ⚠️ Hệ thống không tự gán bừa một lĩnh vực nào"),
    ]),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", [
        ("001", "Lỗi lĩnh vực và lỗi các ô khác hiện cùng lúc", "P0",
         "Tài khoản có quyền Quản lý danh mục nhóm ngành.",
         "1. Bấm Tạo mới\n2. Để trống cả Mã, Tên và Lĩnh vực\n3. Bấm Lưu",
         "Tất cả các ô: (bỏ trống)",
         "- Cả 3 ô cùng hiện lỗi đỏ trong 1 lần bấm Lưu\n"
         "- ⚠️ Không bắt sửa xong ô này mới lòi ra lỗi ô kia"),
        ("002", "Lỗi lĩnh vực biến mất sau khi chọn giá trị hợp lệ", "P1",
         "Đang có lỗi đỏ dưới ô Lĩnh vực kinh doanh nội bộ.",
         "1. Chọn một lĩnh vực bất kỳ trong danh sách\n2. Quan sát dòng lỗi",
         "Lĩnh vực: Khác",
         "- Dòng lỗi đỏ dưới ô Lĩnh vực biến mất ngay\n- Các lỗi của ô khác (nếu còn) vẫn giữ nguyên"),
        ("003", "Danh sách lĩnh vực sắp xếp theo tên", "P2",
         "Danh mục có 3 lĩnh vực đang Hoạt động.",
         "1. Bấm Tạo mới\n2. Mở danh sách xổ xuống ô Lĩnh vực kinh doanh nội bộ",
         "—",
         "- Các lĩnh vực xếp theo thứ tự chữ cái của tên\n- Không có dòng trùng lặp"),
        ("004", "Tìm nhanh trong danh sách lĩnh vực", "P2",
         "Danh mục có 3 lĩnh vực đang Hoạt động.",
         "1. Bấm Tạo mới\n2. Mở ô Lĩnh vực kinh doanh nội bộ\n3. Gõ \"ô tô\" vào ô tìm của danh sách",
         "Từ khoá: ô tô",
         "- Danh sách lọc còn lĩnh vực \"Ô tô - Xe máy\"\n- Chọn được bình thường sau khi lọc"),
    ]),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", [
        ("001", "Hai người cùng sửa: người sau bị lĩnh vực đã khoá", "P1",
         "Người A và người B cùng mở cửa sổ Sửa nhóm ngành NN.0005 (đang gắn \"Ô tô - Xe máy\").",
         "1. Người A khoá lĩnh vực \"Ô tô - Xe máy\" ở màn danh mục lĩnh vực\n"
         "2. Người B bấm Lưu ở cửa sổ đang mở, không đổi lĩnh vực",
         "—",
         "- Người B vẫn lưu được vì giữ nguyên lĩnh vực cũ\n"
         "- Nếu người B đổi sang một lĩnh vực đã khoá khác thì hệ thống báo lỗi đỏ dưới ô Lĩnh vực"),
        ("002", "Xoá lĩnh vực trong lúc người khác đang mở cửa sổ Tạo mới", "P2",
         "Người A đang mở cửa sổ Tạo mới nhóm ngành và đã chọn lĩnh vực \"Điện - Tự động hóa\"; "
         "người B xoá lĩnh vực đó (chưa có nhóm ngành nào dùng).",
         "1. Người B xoá lĩnh vực \"Điện - Tự động hóa\"\n2. Người A bấm Lưu",
         "—",
         "- Hệ thống báo lỗi đỏ dưới ô Lĩnh vực với nội dung lĩnh vực không tồn tại\n"
         "- Cửa sổ không đóng, dữ liệu đã nhập vẫn còn"),
        ("003", "Đổi tên lĩnh vực phản ánh ngay trên danh sách nhóm ngành", "P1",
         "Lĩnh vực \"Khác\" đang gắn cho 22 nhóm ngành.",
         "1. Vào Danh mục > Lĩnh vực kinh doanh nội bộ, sửa tên \"Khác\" thành \"Khác - chưa phân loại\"\n"
         "2. Quay lại màn Nhóm ngành, tải lại danh sách",
         "Tên mới: Khác - chưa phân loại",
         "- Cột Lĩnh vực kinh doanh nội bộ của 22 dòng đều hiện tên mới\n"
         "- Không dòng nào bị mất liên kết"),
    ]),
    ("X", "LUỒNG NGHIỆP VỤ TỔNG THỂ", [
        ("001", "Luồng đầy đủ: tạo lĩnh vực → gắn cho nhóm ngành → lọc → xoá", "P0",
         "Tài khoản có đủ quyền Quản lý cả 2 danh mục.",
         "1. Tạo lĩnh vực kinh doanh nội bộ mới\n2. Vào màn Nhóm ngành, tạo nhóm ngành mới gắn lĩnh vực vừa tạo\n"
         "3. Lọc danh sách theo lĩnh vực đó\n4. Vào màn Lĩnh vực, thử Xoá lĩnh vực đó\n"
         "5. Quay lại xoá nhóm ngành vừa tạo\n6. Vào màn Lĩnh vực, xoá lĩnh vực",
         "Lĩnh vực: LVKDNB.E2E1 - Lĩnh vực kiểm thử · Nhóm ngành: NN.E2E1 - Nhóm ngành kiểm thử",
         "- Bước 2 lưu thành công, cột Lĩnh vực hiện đúng tên vừa tạo\n"
         "- Bước 3 lọc ra đúng 1 dòng\n"
         "- Bước 4 nút Xoá bị ẩn (đang được sử dụng)\n"
         "- Bước 5 xoá nhóm ngành thành công\n"
         "- Bước 6 nút Xoá hiện lại và xoá được lĩnh vực"),
        ("002", "Luồng nhập từ Excel rồi kiểm tra trên lưới và bộ lọc", "P1",
         "Có sẵn lĩnh vực mã LVKDNB.KHAC đang Hoạt động.",
         "1. Tải file mẫu, điền 2 dòng nhóm ngành mới cùng mã lĩnh vực LVKDNB.KHAC\n"
         "2. Nhập từ Excel\n3. Lọc danh sách theo lĩnh vực \"Khác\"\n4. Xuất Excel",
         "2 dòng: NN.EX01, NN.EX02 · Mã lĩnh vực: LVKDNB.KHAC",
         "- Nhập thành công 2 dòng\n- Bộ lọc hiện cả 2 dòng vừa nhập\n"
         "- File xuất có cột Lĩnh vực kinh doanh nội bộ ghi \"Khác\" ở cả 2 dòng"),
    ]),
]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testcase.xlsx")
    build(
        output_file=out,
        sheet_name="Trang tính1",
        feature_name="Danh mục Nhóm ngành - bổ sung Lĩnh vực kinh doanh nội bộ - Cập nhật ngày 23/08/2026",
        module_name=MODULE,
        description_block=DESCRIPTION_BLOCK,
        role_tcs=ROLE_TCS,
        sections=SECTIONS,
    )
