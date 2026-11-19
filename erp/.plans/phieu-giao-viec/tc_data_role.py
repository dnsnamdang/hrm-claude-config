# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu giao viec'."""

MENU = "Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu giao việc\""
MENU_DG = "Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu giao việc được giao\""
MENU_CHO = "Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu chờ giao việc\""

# Du lieu mau dung chung
DATA = ("Công ty TPE có phòng PKT1 (kỹ thuật) và PKD (kinh doanh); công ty TPC có phòng PKT9.\n"
        "Tài khoản:\n"
        "- TP-1: trưởng PKT1, phụ trách PKT1, có quyền \"Tạo phiếu giao việc\"\n"
        "- KTV-1, KTV-2: kỹ thuật viên PKT1, không có quyền xem phiếu giao việc\n"
        "- KD-1: nhân viên PKD, người lập hợp đồng và các yêu cầu\n"
        "Chứng từ chờ giao (phòng tiếp nhận PKT1):\n"
        "- HD-01: hợp đồng SC - BH Có hiệu lực: máy M1 serial S1 lỗi E1 (định mức công 2), dịch vụ \"Vệ sinh "
        "máy\" SL 1, vật tư bán thêm VT1 SL 3\n"
        "- BH-01: phiếu bảo hành Đã duyệt: máy M2 lỗi E2 (định mức công 1,5)\n"
        "- LD-01: yêu cầu lắp đặt bàn giao của hợp đồng hàng HDH-01: 3 máy M3, định mức công 1, cấu hình mỗi "
        "người lắp 2 máy\n"
        "- YC-01: yêu cầu giao việc khác: dòng \"Khảo sát mặt bằng\" định mức công 0,5")

OPEN_TP1 = "Đăng nhập TP-1, " + MENU
FROM_HD01 = ("Đăng nhập TP-1, mở Phiếu chờ giao việc, tab Hợp đồng, bấm nút bánh răng dòng HD-01, chọn "
             "\"Tạo phiếu giao việc\"")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu giao việc: trưởng phòng kỹ thuật (phòng tiếp nhận xử lý) giao phần việc của một chứng từ cho phòng "
     "mình thực hiện: sửa chữa, bảo dưỡng, bảo hành, lắp đặt bàn giao hoặc việc khác.\n"
     "Người dùng làm được:\n"
     "- Tạo phiếu từ màn Phiếu chờ giao việc (5 nguồn: Hợp đồng, PL bổ sung, Phiếu bảo hành, Lắp đặt bàn "
     "giao, Giao việc khác), chọn số lượng giao lần này, thêm công phụ, bấm \"Lưu & duyệt\".\n"
     "- Xem danh sách, lọc, In, Xuất excel, xem chi tiết.\n"
     "- Xóa phiếu khi chưa có phiếu công tác (xóa = hủy phiếu, trả lại số còn giao cho chứng từ gốc).\n"
     "Người thực hiện không chọn trên màn này: được gắn từ phiếu công tác bên HRM."),

    ("2. Đối tượng được tính / hiển thị",
     "- Danh sách \"Phiếu giao việc\": phiếu giao việc (không gồm phiếu duyệt kết quả) trong phạm vi quyền xem, "
     "mới nhất lên đầu.\n"
     "- Danh sách \"Phiếu giao việc được giao\": phiếu mà người đăng nhập là người thực hiện.\n"
     "- Vòng đời trạng thái: Chờ thực hiện > Đang nhập kết quả > Đã nhập kết quả > Đang duyệt kết quả > Đã "
     "duyệt kết quả (bộ lọc còn có Chờ BKS duyệt kết quả, Đang đề nghị thanh toán, Đã thanh toán)."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu đã Xóa (Hủy): không hiện ở bất kỳ danh sách nào, kể cả với người lập.\n"
     "- Phiếu duyệt kết quả (phiếu con) không nằm ở danh sách này.\n"
     "- Màn không có nút Tạo mới, không có nút Sửa.\n"
     "- Trên form, dòng có số còn trên hợp đồng bằng 0 thì ô SL giao lần này bị khóa (sửa chữa)."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "- \"Thời gian dự kiến từ ngày\": Ngày dự kiến bắt đầu của phiếu từ ngày này trở đi.\n"
     "- \"Thời gian dự kiến đến ngày\": Ngày dự kiến kết thúc của phiếu đến hết ngày này.\n"
     "- Khi tạo phiếu: Ngày dự kiến bắt đầu và kết thúc bắt buộc, không trước hôm nay, kết thúc không trước bắt "
     "đầu."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách: STT, Số phiếu giao việc (bấm mở), Số hợp đồng (bấm mở chứng từ gốc), Số phiếu yêu cầu (lắp "
     "đặt / giao việc khác), Khách hàng, Người yêu cầu, Người lập, Người thực hiện (người trưởng nhóm, kèm SĐT), "
     "Thời gian dự kiến, Tổng công định mức, Trạng thái, Hành động (Nhập kết quả, Xóa, Xem phiếu nhập kết quả, "
     "Xem phiếu duyệt kết quả).\n"
     "Bộ lọc: Số phiếu giao việc, Số hợp đồng, Số phiếu yêu cầu, Khách hàng, Người yêu cầu, Trạng thái, Người "
     "lập, Người thực hiện, Thời gian dự kiến từ / đến ngày; người có quyền xem rộng có thêm Công ty, Phòng ban.\n"
     "Form: Thông tin khách hàng; A - Bảo hành hoặc A - Dịch vụ sửa chữa bảo dưỡng (I. Dịch vụ sửa chữa, II. "
     "Danh mục thiết bị cần bảo dưỡng) hoặc A - Lắp đặt bàn giao hoặc A - Dịch vụ đính kèm; B - Vật tư bán "
     "thêm; Công việc phụ (Công phụ tính P3); Tổng hợp; Thời gian dự kiến thực hiện."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- SL giao lần này mặc định = SL còn trên hợp đồng, không nhập được quá số này.\n"
     "- Lắp đặt: SL tính công khoán = SL bàn giao chia số máy mỗi người, làm tròn lên; Tổng công định mức của "
     "dòng = SL tính công khoán x Định mức công.\n"
     "- Tổng công định mức được giao = Công chính (bảo hành + sửa chữa có SL khác 0 + bảo dưỡng + lắp đặt + giao "
     "việc khác) + Công phụ (P3).\n"
     "Với dữ liệu mẫu: giao đủ HD-01 thì Tổng công 2; LD-01 giao 3 máy thì SL tính công khoán 2, Tổng công 2; "
     "thêm công phụ 0,5 thì Tổng 2,5."),

    ("7. Phân quyền cấp",
     "- Xem danh sách \"Phiếu giao việc\": quyền \"Xem phiếu giao việc theo tổng công ty\" thấy mọi phiếu; "
     "\"... theo công ty\" thấy phiếu công ty mình; \"... theo phòng ban\" thấy phiếu của phòng mình phụ trách; "
     "không có các quyền này thì chỉ thấy phiếu mình lập hoặc mình thực hiện.\n"
     "- Xem chi tiết: như trên, cộng người lập, người thực hiện, Super Admin; ngoài phạm vi thì ra trang không "
     "tìm thấy.\n"
     "- Tạo: nút ở màn Phiếu chờ giao việc (cần quyền \"Tạo phiếu giao việc\" và là phòng tiếp nhận).\n"
     "- Xóa: chỉ người lập hoặc Super Admin, phiếu Chờ thực hiện, chưa có phiếu công tác.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Phân trang, STT liên tục qua các trang.\n"
     "- Cột Tổng công định mức hiện 2 số lẻ.\n"
     "- In / Xuất excel: danh sách theo phạm vi quyền xem, mới nhất lên đầu; tiêu đề \"DANH SÁCH PHIẾU GIAO "
     "VIỆC\", file danh_sach_phieu_giao_viec.xlsx."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- In / Xuất excel bỏ qua mọi bộ lọc đang chọn.\n"
     "- In / Xuất excel ở menu \"Phiếu giao việc được giao\" ra cả phiếu không giao cho mình.\n"
     "- Lọc Người yêu cầu chỉ tìm được phiếu từ hợp đồng / phiếu bảo hành; lọc Phòng ban làm mất phiếu lắp đặt "
     "và giao việc khác; lọc Bộ phận không có tác dụng.\n"
     "- Dòng bảo hành để SL giao 0 vẫn cộng công vào Tổng công định mức.\n"
     "- Lưu phiếu không kiểm tra lại quyền, phòng, số còn giao, và nhận trạng thái do trình duyệt gửi lên.\n"
     "- Đường dẫn Sửa mở được với phiếu Đã duyệt kết quả."),
]


ROLE_TCS = [
    ("00", "Không có quyền xem vẫn mở được danh sách, chỉ thấy phiếu của mình", "P0",
     "NV-A không có quyền xem phiếu giao việc, chưa lập và chưa được giao phiếu nào; có phiếu PGV-01 do TP-1 "
     "lập",
     "1. Đăng nhập NV-A\n"
     "2. " + MENU,
     "Tài khoản: NV-A",
     "- Mở trang \"Danh sách phiếu giao việc\"\n"
     "- Bảng không có dữ liệu, không thấy PGV-01"),

    ("01", "Quyền theo công ty thấy phiếu công ty mình", "P0",
     "QL-C có quyền \"Xem phiếu giao việc theo công ty\", thuộc TPE; PGV-01 của TPE, PGV-09 của TPC",
     "1. Đăng nhập QL-C, " + MENU,
     "—",
     "- Thấy PGV-01, không thấy PGV-09\n"
     "- Có ô lọc Phòng ban, không có ô Công ty"),

    ("02", "Quyền theo tổng công ty thấy mọi công ty", "P0",
     "QL-T có quyền \"Xem phiếu giao việc theo tổng công ty\"; PGV-01 (TPE), PGV-09 (TPC)",
     "1. Đăng nhập QL-T, " + MENU,
     "—",
     "- Thấy PGV-01 và PGV-09\n"
     "- Có ô lọc Công ty và Phòng ban"),

    ("03", "Quyền theo phòng ban thấy phiếu phòng mình phụ trách", "P0",
     "QL-P có quyền \"Xem phiếu giao việc theo phòng ban\", phụ trách PKT1; PGV-01 do TP-1 (PKT1) lập, PGV-02 do "
     "trưởng PKT2 lập",
     "1. Đăng nhập QL-P, " + MENU,
     "—",
     "- Thấy PGV-01, không thấy PGV-02\n"
     "- Có ô lọc Phòng ban (chỉ phòng mình phụ trách) và Bộ phận"),

    ("04", "Người thực hiện thấy phiếu mình được giao", "P0",
     "PGV-01 có người thực hiện KTV-1 (gắn từ phiếu công tác); KTV-1 không có quyền xem phiếu giao việc",
     "1. Đăng nhập KTV-1, " + MENU,
     "—",
     "- Thấy PGV-01\n"
     "- Bấm số phiếu mở được chi tiết"),

    ("05", "Mở chi tiết phiếu ngoài phạm vi qua đường dẫn", "P0",
     "NV-A như TC 00; có đường dẫn chi tiết PGV-01",
     "1. Đăng nhập NV-A, dán đường dẫn chi tiết PGV-01",
     "—",
     "- Ra trang không tìm thấy"),

    ("06", "Quyền theo công ty mở chi tiết phiếu công ty khác", "P1",
     "QL-C như TC 01; có đường dẫn chi tiết PGV-09 (TPC)",
     "1. Đăng nhập QL-C, dán đường dẫn chi tiết PGV-09",
     "—",
     "- Ra trang không tìm thấy"),

    ("07", "Người không phải người lập không có nút Xóa", "P0",
     "QL-C như TC 01; PGV-01 Chờ thực hiện, chưa có phiếu công tác, do TP-1 lập",
     "1. Đăng nhập QL-C, mở danh sách\n"
     "2. Bấm nút bánh răng ở PGV-01",
     "—",
     "- Không có \"Xóa\""),

    ("08", "Gọi thẳng đường dẫn Xóa của phiếu người khác", "P0",
     "QL-C như TC 07; có đường dẫn Xóa của PGV-01",
     "1. Đăng nhập QL-C, dán đường dẫn Xóa của PGV-01",
     "—",
     "- Ra trang không tìm thấy\n"
     "- PGV-01 vẫn Chờ thực hiện"),

    ("09", "Gọi thẳng chức năng lưu phiếu giao việc khi không có quyền giao việc", "P1",
     "NV-A không có quyền \"Tạo phiếu giao việc\", không thuộc PKT1\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu phiếu giao việc cho HD-01 với đủ thông tin bắt "
     "buộc",
     "—",
     "- Mong đợi: bị chặn, không tạo phiếu\n"
     "- Lưu ý: theo code hiện tại lưu thành công (đã ghi ở bộ Phiếu chờ giao việc) - ghi Failed"),
]
