# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu xuat dieu chinh sai so lieu' (phieu xuat lai)."""

MENU = "Mở menu Kho > cột \"Xuất kho\" > bấm \"Phiếu xuất điều chỉnh sai số liệu\""

# Du lieu mau dung chung
NK1 = ("Kho K1 (công ty TPE). TK-1 (thủ kho) lập phiếu nhập kho NK-1: H1 (ĐVT Cái) 10 cái, xếp P1 = 6, "
       "P2 = 4; H2 (ĐVT Thùng, hệ số 12) 2 thùng, xếp P3 = 2 thùng. KT-1 (kế toán kho) bấm Không duyệt "
       "NK-1, lý do \"Sai số lượng\".\n"
       "Tồn K1 trước khi xuất lại: H1 = 15 (P1 = 9, P2 = 6); H2 = 30 cái (P3 = 30, trong đó 24 cái thuộc "
       "lô của NK-1)")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu xuất điều chỉnh sai số liệu (trên màn ghi là \"phiếu xuất lại\"): khi kế toán Không duyệt một "
     "phiếu nhập kho vì sai số liệu, người lập phiếu nhập dùng phiếu này để xuất trả lại TOÀN BỘ hàng của "
     "phiếu nhập đó ra khỏi kho (trừ tồn đúng lô, đúng vị trí đã xếp), rồi lập phiếu nhập lại với số liệu "
     "đúng.\n"
     "Người dùng làm được: xem danh sách, lọc, Xuất excel danh sách; tạo phiếu xuất lại từ phiếu nhập kho "
     "Không duyệt; xem chi tiết; từ phiếu Chờ nhập lại bấm \"Tạo phiếu nhập lại\". Không có Sửa, Xóa, Duyệt: "
     "bấm Xuất lại là trừ kho ngay."),

    ("2. Đối tượng được tính / hiển thị",
     "- Danh sách: phiếu xuất lại trong phạm vi được xem (xem mục 7), mới tạo lên đầu, 10 dòng mỗi trang.\n"
     "- Cột: STT, Mã phiếu (dạng PXL-xxxxx, bấm mở chi tiết), Phiếu NK (bấm mở phiếu nhập kho gốc), Ngày "
     "lập, Người lập, Trạng thái, Hành động.\n"
     "- Trạng thái: \"Chờ nhập lại\" (nhãn đỏ, ngay sau khi tạo), \"Đã nhập lại\" (nhãn xanh, sau khi lập "
     "phiếu nhập lại từ phiếu nhập gốc).\n"
     "- Ô chọn phiếu nhập kho khi tạo chỉ liệt kê phiếu nhập kho Không duyệt do chính người đang đăng nhập "
     "lập."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu nhập kho ở trạng thái khác Không duyệt, hoặc do người khác lập: không chọn được để xuất lại.\n"
     "- Phiếu nhập kho đã xuất lại 1 lần (chuyển \"Đã xuất lại\"): không xuất lại lần 2.\n"
     "- Không có nút In trên danh sách và chi tiết.\n"
     "- Không xuất lại từng phần: luôn lấy đủ mọi hàng, mọi vị trí của phiếu nhập."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Màn danh sách không có ô Từ ngày / Đến ngày. Cột Ngày lập là ngày tạo phiếu xuất lại; thời điểm trừ "
     "tồn kho (ghi vào thẻ kho) là lúc bấm Xuất lại."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Form tạo: Chọn phiếu nhập kho (bắt buộc, bấm kính lúp mở cửa sổ tìm), Người lập (lấy từ phiếu nhập), "
     "Người giao hàng (lấy từ phiếu nhập), Ghi chú (tối đa 255 ký tự). Khung Chi tiết: tab Hàng hóa gồm STT, "
     "Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, Đơn vị tính, Tổng SL, Chi tiết Vị trí / SL; thêm 1 tab "
     "cho mỗi phụ lục hợp đồng của phiếu nhập (nếu có). Nút Xuất lại, Hủy.\n"
     "Màn chi tiết: Phiếu nhập kho (link), Kho, Ngày lập, Người lập, Người giao hàng, Ghi chú, bảng hàng như "
     "trên, nút Quay lại."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Mỗi hàng của phiếu nhập: tồn kho của hàng giảm đúng SL đã nhập (quy về ĐVT nhỏ nhất).\n"
     "- Mỗi vị trí: tồn vị trí và tồn lô của phiếu nhập tại vị trí đó giảm đúng SL đã xếp nhân hệ số ĐVT.\n"
     "- Tồn của công ty thuê kho giảm tương ứng.\n"
     "Với dữ liệu mẫu NK-1: H1 còn 5 (P1 = 3, P2 = 2); H2 còn 6 cái (P3 = 6)."),

    ("7. Phân quyền cấp",
     "- Mở danh sách: mọi tài khoản đăng nhập. Phạm vi: quyền \"Xem tất cả phiếu\" thấy mọi phiếu; \"Xem tất "
     "cả phiếu của công ty\" thấy phiếu của công ty mình; \"Xem tất cả phiếu của phòng ban\" thấy phiếu của "
     "thành viên phòng mình; không có quyền nào chỉ thấy phiếu mình lập.\n"
     "- Tạo phiếu xuất lại: chỉ người lập phiếu nhập kho, và phiếu nhập đang Không duyệt.\n"
     "- Xem chi tiết: chỉ người lập phiếu xuất lại hoặc tài khoản Super Admin.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- STT liên tục qua các trang.\n"
     "- Xuất excel: file \"danh_sach_phieu_xuat_lai.xlsx\", tiêu đề \"DANH SÁCH PHIẾU XUẤT LẠI\", cột STT, "
     "Mã phiếu, Phiếu NK, Ngày lập, Người lập, Trạng thái; theo đúng bộ lọc đang chọn, lấy hết không phân "
     "trang."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Lọc theo Người lập không có tác dụng (danh sách và file Excel vẫn ra mọi người).\n"
     "- Trưởng phòng chọn Bộ phận ở bộ lọc thì bảng báo lỗi.\n"
     "- Người cùng phòng / quản lý thấy phiếu ở danh sách nhưng bấm Mã phiếu ra trang không tìm thấy.\n"
     "- Màn chi tiết, ô Người lập hiện tên NGƯỜI ĐANG XEM chứ không phải người lập.\n"
     "- Không có nút In; mở thẳng đường dẫn in ra mẫu không có số liệu.\n"
     "- Hàng có 2 dòng cùng mã trong phiếu nhập: kiểm tra đủ tồn từng dòng riêng, có thể làm tồn âm.\n"
     "- Không chặn vị trí đang kiểm kê."),
]


ROLE_TCS = [
    ("00", "Tài khoản thường mở được danh sách", "P0",
     "NV-A không có quyền xem phiếu nào, chưa lập phiếu xuất lại nào; TK-1 đã lập PXL-1",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Tiêu đề \"Danh sách phiếu xuất lại\"\n"
     "- Bảng trống, không thấy PXL-1"),

    ("01", "Không có quyền xem phiếu chỉ thấy phiếu mình lập", "P0",
     "TK-1 không có quyền xem phiếu nào; TK-1 lập PXL-1, TK-2 lập PXL-2",
     "1. Đăng nhập TK-1, mở màn từ menu",
     "—",
     "- Chỉ có PXL-1"),

    ("02", "Quyền xem tất cả phiếu của phòng ban", "P0",
     "TP-1 có quyền \"Xem tất cả phiếu của phòng ban\", là trưởng phòng Kho TPE; TK-1 thuộc phòng này lập "
     "PXL-1; TK-9 phòng khác lập PXL-9",
     "1. Đăng nhập TP-1, mở màn",
     "—",
     "- Có PXL-1, không có PXL-9"),

    ("03", "Quyền xem tất cả phiếu của công ty", "P0",
     "GD-1 có quyền \"Xem tất cả phiếu của công ty\" (TPE); PXL-1 của TPE, PXL-5 của TPC",
     "1. Đăng nhập GD-1, mở màn",
     "—",
     "- Có PXL-1, không có PXL-5"),

    ("04", "Quyền xem tất cả phiếu", "P1",
     "TGD-1 có quyền \"Xem tất cả phiếu\"",
     "1. Đăng nhập TGD-1, mở màn",
     "—",
     "- Có cả PXL-1 và PXL-5; bộ lọc có ô Công ty"),

    ("05", "Người được xem ở danh sách mở chi tiết phiếu người khác", "P1",
     "TP-1 thấy PXL-1 (do TK-1 lập) ở danh sách; TP-1 không phải Super Admin",
     "1. Bấm Mã phiếu PXL-1",
     "—",
     "- Mong đợi: mở được màn chi tiết vì đã được xem ở danh sách\n"
     "- Lưu ý: theo code hiện tại ra trang không tìm thấy - ghi Failed"),

    ("06", "Super Admin mở chi tiết phiếu bất kỳ", "P1",
     "AD-1 là Super Admin; PXL-1 do TK-1 lập",
     "1. Đăng nhập AD-1, dán đường dẫn chi tiết PXL-1",
     "—",
     "- Mở được màn chi tiết PXL-1"),

    ("07", "Người khác không tạo được phiếu xuất lại từ phiếu nhập không phải của mình", "P0",
     NK1 + "\nTK-2 là thủ kho khác cùng kho K1",
     "1. Đăng nhập TK-2, mở màn tạo phiếu xuất lại\n"
     "2. Bấm kính lúp ở ô Chọn phiếu nhập kho",
     "—",
     "- Cửa sổ tìm không có NK-1"),

    ("08", "Gọi thẳng chức năng lưu với phiếu nhập của người khác", "P0",
     NK1 + "\nTK-2 không phải người lập NK-1",
     "1. Đăng nhập TK-2, dùng công cụ kiểm thử API gửi lệnh tạo phiếu xuất lại cho NK-1",
     "—",
     "- Báo \"Không đủ quyền!\", không tạo phiếu, tồn K1 không đổi"),

    ("09", "Mở thẳng đường dẫn tạo kèm phiếu nhập của người khác", "P1",
     NK1 + "\nTK-2 có đường dẫn tạo phiếu xuất lại kèm NK-1",
     "1. Đăng nhập TK-2, dán đường dẫn\n"
     "2. Quan sát form",
     "—",
     "- Ô phiếu nhập kho không điền NK-1, khung Chi tiết không có hàng\n"
     "- Mong đợi: có thông báo không chọn được phiếu\n"
     "- Lưu ý: theo code hiện tại không có thông báo nào - ghi Failed nếu nghiệp vụ yêu cầu báo"),
]
