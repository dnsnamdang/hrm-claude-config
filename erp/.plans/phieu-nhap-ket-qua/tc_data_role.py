# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Phieu nhap ket qua'."""

MENU = "Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu nhập kết quả\""
MENU_PGV = "Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu giao việc\""
MENU_DG = "Mở menu Bảo hành sửa chữa > mục \"Giao việc\" > bấm \"Phiếu giao việc được giao\""

# Du lieu mau dung chung
DATA = ("Công ty TPE có phòng kỹ thuật PKT1; công ty TPC có phòng PKT9.\n"
        "Tài khoản:\n"
        "- KTV-1: kỹ thuật viên PKT1, là người thực hiện trên phiếu công tác của PGV-01 đến PGV-05\n"
        "- KTV-2: kỹ thuật viên PKT1, không thực hiện phiếu nào, không có quyền gì thêm\n"
        "- TP-1: trưởng PKT1, phụ trách PKT1, có quyền \"Xem phiếu nhập kết quả theo phòng ban\"\n"
        "- QL-1: thuộc TPE, có quyền \"Duyệt phiếu nhập kết quả\"\n"
        "- QL-9: thuộc TPC, có quyền \"Duyệt phiếu nhập kết quả\"\n"
        "Phiếu giao việc của PKT1 (đều Chờ thực hiện, phiếu công tác đã duyệt, trừ PGV-05):\n"
        "- PGV-01: từ yêu cầu lắp đặt LD-01 của hợp đồng hàng HDH-01: 3 máy M3 có serial, định mức công 1, "
        "mỗi người lắp 2 máy, hệ số hưởng 0,8; phiếu yêu cầu xuất hàng XH-01 của máy M3 đã hạch toán\n"
        "- PGV-02: từ hợp đồng SC - BH HD-01: sửa máy M1 serial S1 lỗi E1 định mức công 2, dịch vụ \"Vệ sinh "
        "máy\", vật tư VT1 SL 3\n"
        "- PGV-03: từ phiếu bảo hành BH-01: máy M2 serial S2 lỗi E2 định mức công 1,5\n"
        "- PGV-04: từ yêu cầu giao việc khác YC-01: dòng \"Khảo sát mặt bằng\" định mức công 0,5\n"
        "- PGV-05: như PGV-02 nhưng phiếu công tác CHƯA duyệt")

OPEN_KTV1 = "Đăng nhập KTV-1, " + MENU
OPEN_QL1 = "Đăng nhập QL-1, " + MENU
FROM_PGV = ("Đăng nhập KTV-1, " + MENU_DG + ", bấm nút bánh răng dòng {pgv}, chọn \"Nhập kết quả\"")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu nhập kết quả: người thực hiện ghi lại kết quả thực tế của một phiếu giao việc (đã hoàn thành "
     "hay chưa, % hoàn thành, SL bàn giao, serial, vật tư, công phụ, ảnh công trình, ảnh biên bản bàn giao, "
     "file đính kèm) để người duyệt xét công khoán.\n"
     "Người dùng làm được:\n"
     "- Tạo phiếu từ nút \"Nhập kết quả\" của phiếu giao việc, bấm Lưu (Đang tạo) hoặc \"Lưu & Gửi duyệt\" "
     "(Chờ duyệt kết quả).\n"
     "- Sửa / Xóa phiếu của mình khi Đang tạo hoặc Không duyệt kết quả.\n"
     "- Người có quyền \"Duyệt phiếu nhập kết quả\" cùng công ty: \"Duyệt kết quả\" (mở phiếu duyệt kết quả) "
     "hoặc \"Không duyệt kết quả\" (bắt buộc lý do).\n"
     "Màn không có nút Tạo mới, không có In, không có Xuất excel."),

    ("2. Đối tượng được tính / hiển thị",
     "- Mỗi phiếu giao việc chỉ có tối đa 1 phiếu nhập kết quả.\n"
     "- Danh sách \"Phiếu nhập kết quả\": phiếu trong phạm vi quyền xem, mới nhất lên đầu; phiếu Đang tạo "
     "chỉ người lập thấy.\n"
     "- Danh sách chờ duyệt (từ ô trang chủ): phiếu Chờ duyệt kết quả của công ty mình.\n"
     "- Trạng thái: Đang tạo, Chờ duyệt kết quả, Đang duyệt kết quả, Đã duyệt kết quả, Không duyệt kết quả "
     "(bộ lọc còn có Chờ BKS duyệt kết quả).\n"
     "- Phiếu giao việc đi theo: Lưu thì \"Đang nhập kết quả\"; Gửi duyệt thì \"Đã nhập kết quả\"; xóa phiếu "
     "nhập kết quả thì về \"Chờ thực hiện\"."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu Đang tạo của người khác (kể cả với người có quyền xem rộng).\n"
     "- Nút \"Nhập kết quả\" bị ẩn khi phiếu giao việc đã có phiếu nhập kết quả, phiếu công tác chưa duyệt, "
     "phiếu giao việc không còn Chờ thực hiện, hoặc người dùng không phải người thực hiện và không có quyền "
     "\"Nhập kết quả thực hiện\".\n"
     "- Nút Sửa / Xóa ẩn khi không phải người lập hoặc phiếu không ở Đang tạo / Không duyệt kết quả.\n"
     "- Nút Duyệt / Không duyệt kết quả ẩn khi phiếu không Chờ duyệt kết quả hoặc khác công ty."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày / Đến ngày lọc theo Ngày tạo phiếu nhập kết quả (tính trọn ngày Đến ngày)."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Danh sách: STT, Số phiếu nhập kết quả (bấm mở), Số phiếu giao việc (bấm mở), Số hợp đồng (bấm mở hợp đồng "
     "SC - BH / phiếu bảo hành / PL / hợp đồng hàng), Số phiếu Y/C (lắp đặt hoặc giao việc khác), Khách hàng, "
     "Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái, Hành động.\n"
     "Bộ lọc: Số phiếu nhập kết quả, Số phiếu giao việc, Số hợp đồng, Số phiếu y/c, Khách hàng, Người tạo, "
     "Người duyệt, Trạng thái, Từ ngày / Đến ngày; người có quyền xem rộng thấy thêm Công ty, Phòng ban.\n"
     "Form: Thông tin khách hàng (phiếu giao việc, khách hàng, địa chỉ, người liên hệ, người yêu cầu, ghi chú, "
     "ảnh công trình, ảnh biên bản bàn giao); A - phần việc theo nguồn (Bảo hành / Dịch vụ sửa chữa + Thiết bị "
     "bảo dưỡng / Lắp đặt bàn giao / Dịch vụ đính kèm) với cột Đã hoàn thành, % Hoàn thành, SL bàn giao, Serial, "
     "ĐM công, CK đề xuất duyệt, CK được tính dự kiến, Ghi chú; B - Công phụ tính P3; Tổng công định mức; Danh "
     "sách giao nhận vật tư, hàng bán thêm, dịch vụ trả tiền, chi phí liên quan."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Tích \"Đã hoàn thành\" thì % Hoàn thành = 100 và khóa ô; không tích thì nhập % nhỏ hơn 100.\n"
     "- Lắp đặt: SL tính công khoán = SL bàn giao chia số máy mỗi người, làm tròn lên; CK đề xuất duyệt = ĐM "
     "công x SL tính công khoán x % Hoàn thành, không vượt ĐM công x SL tính công khoán.\n"
     "- Sửa chữa / bảo hành: CK đề xuất duyệt = ĐM công x % Hoàn thành.\n"
     "- CK được tính dự kiến = CK đề xuất duyệt x hệ số hưởng.\n"
     "- Tổng công định mức = Công khoán chính + Công khoán phụ (chỉ dòng công phụ có tích Đã hoàn thành).\n"
     "Với dữ liệu mẫu: PGV-01 bàn giao đủ 3 máy, Đã hoàn thành: SL tính công khoán 2, CK đề xuất 2, CK dự kiến "
     "1,6; PGV-02 M1 hoàn thành 50%: CK đề xuất 1."),

    ("7. Phân quyền cấp",
     "- Danh sách: \"Xem phiếu nhập kết quả theo tổng công ty\" thấy mọi phiếu; \"... theo công ty\" thấy "
     "phiếu công ty mình và phiếu mình lập; \"... theo phòng ban\" thấy phiếu của phòng mình phụ trách và "
     "phiếu mình lập; không có quyền nào thì chỉ thấy phiếu mình lập.\n"
     "- Xem chi tiết: như danh sách, cộng Super Admin và người duyệt cùng công ty khi phiếu Chờ duyệt kết quả; "
     "ngoài phạm vi thì ra trang không tìm thấy.\n"
     "- Nhập kết quả: người thực hiện của phiếu giao việc, người có quyền \"Nhập kết quả thực hiện\", hoặc Super "
     "Admin; phiếu công tác phải đã duyệt.\n"
     "- Duyệt / Không duyệt: quyền \"Duyệt phiếu nhập kết quả\", cùng công ty với phiếu.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Ô trang chủ \"Chờ duyệt phiếu nhập kết quả giao việc\" (người có quyền duyệt): đếm phiếu Chờ duyệt "
     "kết quả của công ty mình; bấm vào mở danh sách chờ duyệt.\n"
     "- Dòng \"Tổng công được tính\" của bảng lắp đặt cộng SL bàn giao, SL tính công khoán, CK đề xuất, CK dự "
     "kiến của mọi dòng.\n"
     "- Gửi duyệt: người có quyền duyệt cùng công ty nhận thông báo \"Bạn có 1 phiếu kết quả giao việc cần "
     "duyệt\"; Không duyệt: người lập nhận \"<tên người duyệt> vừa không duyệt phiếu nhập kết quả của bạn!\"."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Chức năng nhận kết quả dành cho ứng dụng HRM không yêu cầu đăng nhập: tạo / sửa được phiếu mà không "
     "cần tài khoản.\n"
     "- Lưu phiếu không kiểm tra người lưu có phải người thực hiện; Sửa không kiểm tra người lập và trạng thái.\n"
     "- Danh sách chờ duyệt mở bởi người không có quyền duyệt thì hiện mọi phiếu mọi công ty.\n"
     "- Lọc Công ty / Phòng ban không có tác dụng.\n"
     "- % Hoàn thành âm vẫn nhận, CK đề xuất ra số âm.\n"
     "- Hai người cùng lưu một phiếu giao việc: người sau thấy đoạn lỗi kỹ thuật thay vì câu báo."),
]


ROLE_TCS = [
    ("00", "Nhân viên không có quyền chỉ thấy phiếu mình lập", "P0",
     DATA + "\nNKQ-01 do KTV-1 lập (Chờ duyệt kết quả); NKQ-07 do KTV-3 (PKT1) lập (Chờ duyệt kết quả)",
     "1. Đăng nhập KTV-2\n"
     "2. " + MENU,
     "Tài khoản: KTV-2",
     "- Bảng không có NKQ-01, NKQ-07\n"
     "- Không có ô lọc Công ty, Phòng ban"),

    ("01", "Quyền theo phòng ban thấy phiếu của phòng phụ trách", "P0",
     DATA + "\nNKQ-01 (PKT1, Chờ duyệt kết quả); NKQ-09 của TPC (Chờ duyệt kết quả); NKQ-02 do KTV-1 lập, "
     "Đang tạo",
     "1. Đăng nhập TP-1, mở màn từ menu",
     "Tài khoản: TP-1",
     "- Có NKQ-01\n"
     "- Không có NKQ-09 (công ty khác), không có NKQ-02 (Đang tạo của người khác)"),

    ("02", "Quyền theo tổng công ty thấy phiếu mọi công ty", "P1",
     DATA + "\nTGĐ có quyền \"Xem phiếu nhập kết quả theo tổng công ty\"; có NKQ-01 (TPE), NKQ-09 (TPC)",
     "1. Đăng nhập TGĐ, mở màn",
     "—",
     "- Có cả NKQ-01 và NKQ-09\n"
     "- Bấm NKQ-09 mở được chi tiết"),

    ("03", "Mở chi tiết phiếu ngoài phạm vi", "P0",
     DATA + "\nKTV-2 có đường dẫn chi tiết NKQ-01",
     "1. Đăng nhập KTV-2, dán đường dẫn chi tiết NKQ-01",
     "—",
     "- Ra trang không tìm thấy"),

    ("04", "Người duyệt cùng công ty mở được phiếu Chờ duyệt", "P0",
     DATA + "\nQL-1 không có quyền xem phiếu nhập kết quả; NKQ-01 Chờ duyệt kết quả",
     "1. Đăng nhập QL-1, dán đường dẫn chi tiết NKQ-01",
     "—",
     "- Mở được chi tiết, có nút \"Không duyệt\" và \"Duyệt kết quả\""),

    ("05", "Người duyệt khác công ty không duyệt được", "P0",
     DATA + "\nNKQ-01 (TPE) Chờ duyệt kết quả",
     "1. Đăng nhập QL-9 (TPC), dán đường dẫn chi tiết NKQ-01",
     "—",
     "- Ra trang không tìm thấy, không có nút duyệt"),

    ("06", "Danh sách chờ duyệt khi không có quyền duyệt", "P1",
     DATA + "\nKTV-2 dán đường dẫn danh sách chờ duyệt (đường dẫn của ô trang chủ)",
     "1. Đăng nhập KTV-2, dán đường dẫn danh sách chờ duyệt",
     "—",
     "- Mong đợi: bảng trống hoặc chỉ phiếu mình lập\n"
     "- Lưu ý: theo code hiện tại hiện mọi phiếu nhập kết quả của mọi công ty, kể cả phiếu Đang tạo của người "
     "khác - ghi Failed"),

    ("07", "Mở thẳng form Sửa phiếu của người khác", "P0",
     DATA + "\nNKQ-02 do KTV-1 lập, Đang tạo; KTV-2 có đường dẫn Sửa NKQ-02",
     "1. Đăng nhập KTV-2, dán đường dẫn Sửa NKQ-02\n"
     "2. Đổi Ghi chú, bấm Lưu",
     "—",
     "- Mong đợi: báo không có quyền, không mở được form\n"
     "- Lưu ý: theo code hiện tại mở được form và Lưu thành công - ghi Failed"),

    ("08", "Tạo / sửa phiếu qua chức năng của ứng dụng HRM khi không đăng nhập", "P0",
     DATA + "\nKhông đăng nhập ERP",
     "1. Dùng công cụ kiểm thử API gọi chức năng lưu kết quả dành cho ứng dụng HRM, gửi kết quả cho PGV-03, "
     "người tạo là KTV-1\n"
     "2. Gọi tiếp chức năng sửa của ứng dụng HRM cho NKQ-04 (Đã duyệt kết quả), đổi Ghi chú",
     "—",
     "- Mong đợi: cả 2 lần đều bị chặn vì chưa đăng nhập\n"
     "- Lưu ý: theo code hiện tại cả 2 lần đều thành công, phiếu mang tên KTV-1 - ghi Failed (cần xác nhận "
     "máy chủ có lớp chặn bên ngoài không)"),

    ("09", "Không duyệt qua đường dẫn khi không có quyền", "P1",
     DATA + "\nNKQ-01 Chờ duyệt kết quả",
     "1. Đăng nhập KTV-2\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt NKQ-01 kèm lý do",
     "—",
     "- Báo \"Không có quyền!\"\n"
     "- NKQ-01 vẫn Chờ duyệt kết quả"),
]
