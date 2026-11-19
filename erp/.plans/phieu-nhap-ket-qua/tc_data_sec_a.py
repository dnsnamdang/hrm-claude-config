# -*- coding: utf-8 -*-
"""Section I - IV cho man Phieu nhap ket qua."""
from tc_data_role import MENU, MENU_PGV, MENU_DG, DATA, OPEN_KTV1, OPEN_QL1, FROM_PGV

NKQ = ("Đã có các phiếu nhập kết quả:\n"
       "- NKQ-01: KTV-1 lập 01/11/2026 cho PGV-11 (lắp đặt LD-11, hợp đồng hàng HDH-11), Chờ duyệt kết quả\n"
       "- NKQ-02: KTV-1 lập 02/11/2026 cho PGV-12 (hợp đồng SC - BH HD-12), Đang tạo\n"
       "- NKQ-03: KTV-1 lập 03/11/2026 cho PGV-13 (giao việc khác YC-13), Không duyệt kết quả\n"
       "- NKQ-04: KTV-1 lập 20/10/2026 cho PGV-14 (phiếu bảo hành BH-14), Đã duyệt kết quả, QL-1 duyệt "
       "25/10/2026 09:30\n"
       "- NKQ-05: KTV-1 lập 04/11/2026 cho PGV-15, Đang duyệt kết quả (đã có phiếu duyệt kết quả lưu nháp)\n"
       "Khách hàng của các phiếu: KH-01 \"Công ty An Phát\"")

SEC_I = [
    ("001", "Mở danh sách phiếu nhập kết quả", "P0",
     NKQ,
     "1. " + OPEN_KTV1,
     "Tài khoản: KTV-1",
     "- Tiêu đề \"Danh sách phiếu nhập kết quả\"\n"
     "- Có NKQ-01 đến NKQ-05, mới nhất (NKQ-05) lên đầu\n"
     "- Không có nút Tạo mới, In, Xuất excel"),

    ("002", "Các cột của bảng", "P1",
     NKQ,
     "1. " + OPEN_KTV1,
     "—",
     "- Cột: STT, Số phiếu nhập kết quả, Số phiếu giao việc, Số hợp đồng, Số phiếu Y/C, Khách hàng, Người tạo, "
     "Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái, Hành động"),

    ("003", "Dòng phiếu từ yêu cầu lắp đặt", "P0",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Xem dòng NKQ-01",
     "—",
     "- Số phiếu giao việc PGV-11 (bấm mở tab mới)\n"
     "- Số hợp đồng HDH-11 (bấm mở hợp đồng hàng), Số phiếu Y/C LD-11 (bấm mở yêu cầu lắp đặt)\n"
     "- Khách hàng \"KH-01-Công ty An Phát\"; Người tạo KTV-1; Ngày tạo dạng 01/11/2026 - giờ:phút\n"
     "- Trạng thái \"Chờ duyệt kết quả\""),

    ("004", "Dòng phiếu từ hợp đồng SC - BH và phiếu bảo hành", "P1",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Xem dòng NKQ-02 và NKQ-04",
     "—",
     "- NKQ-02: Số hợp đồng HD-12 (mở hợp đồng SC - BH), Số phiếu Y/C trống\n"
     "- NKQ-04: Số hợp đồng BH-14 (mở phiếu bảo hành), Số phiếu Y/C trống"),

    ("005", "Dòng phiếu từ yêu cầu giao việc khác", "P1",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Xem dòng NKQ-03",
     "—",
     "- Số hợp đồng trống, Số phiếu Y/C YC-13 (bấm mở)\n"
     "- Trạng thái \"Không duyệt kết quả\""),

    ("006", "Người duyệt và ngày duyệt", "P1",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Xem dòng NKQ-04 và NKQ-01",
     "—",
     "- NKQ-04: Người duyệt QL-1, Ngày duyệt 25/10/2026 - 09:30\n"
     "- NKQ-01: Người duyệt, Ngày duyệt trống"),

    ("007", "Nút hành động theo trạng thái với người lập", "P0",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Bấm nút bánh răng từng dòng",
     "—",
     "- NKQ-02 (Đang tạo), NKQ-03 (Không duyệt kết quả): có Sửa, Xóa\n"
     "- NKQ-01, NKQ-04, NKQ-05: không có Sửa, Xóa\n"
     "- KTV-1 không có quyền duyệt nên không có Duyệt / Không duyệt kết quả"),

    ("008", "Nút hành động với người duyệt", "P0",
     NKQ + "\nQL-1 có thêm quyền \"Xem phiếu nhập kết quả theo công ty\"",
     "1. " + OPEN_QL1 + "\n"
     "2. Bấm nút bánh răng dòng NKQ-01 và NKQ-05",
     "Tài khoản: QL-1",
     "- NKQ-01: có \"Duyệt kết quả\", \"Không duyệt kết quả\"; không có Sửa, Xóa\n"
     "- NKQ-05 (Đang duyệt kết quả): không có nút duyệt\n"
     "- Không thấy NKQ-02 (Đang tạo của KTV-1)"),
]

SEC_II = [
    ("001", "Lọc theo Số phiếu nhập kết quả (gõ một phần)", "P1",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Số phiếu nhập kết quả gõ phần cuối số của NKQ-03",
     "—",
     "- Chỉ còn NKQ-03"),

    ("002", "Lọc theo Số phiếu giao việc", "P1",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Số phiếu giao việc gõ PGV-11",
     "—",
     "- Chỉ còn NKQ-01"),

    ("003", "Lọc Số hợp đồng tìm cả hợp đồng SC - BH và hợp đồng hàng", "P0",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Số hợp đồng gõ HDH-11, xem kết quả\n"
     "3. Đổi sang gõ HD-12",
     "—",
     "- Bước 2: chỉ còn NKQ-01\n"
     "- Bước 3: chỉ còn NKQ-02"),

    ("004", "Lọc theo Số phiếu y/c", "P1",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Số phiếu y/c gõ LD-11, xem kết quả\n"
     "3. Đổi sang gõ YC-13",
     "—",
     "- Bước 2: chỉ còn NKQ-01\n"
     "- Bước 3: chỉ còn NKQ-03"),

    ("005", "Lọc theo Trạng thái", "P0",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Trạng thái chọn \"Không duyệt kết quả\"",
     "—",
     "- Chỉ còn NKQ-03"),

    ("006", "Lọc theo Khách hàng", "P2",
     NKQ + "\nCó thêm NKQ-06 của khách hàng KH-02, KTV-1 lập",
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Khách hàng chọn KH-02",
     "—",
     "- Chỉ còn NKQ-06"),

    ("007", "Lọc theo Người duyệt", "P1",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Người duyệt chọn QL-1",
     "—",
     "- Chỉ còn NKQ-04"),

    ("008", "Lọc Từ ngày / Đến ngày theo Ngày tạo", "P0",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Chọn Từ ngày 01/11/2026, Đến ngày 03/11/2026",
     "—",
     "- Còn NKQ-01, NKQ-02, NKQ-03 (tính trọn ngày 03/11)\n"
     "- Không có NKQ-04 (20/10), NKQ-05 (04/11)"),

    ("009", "Lọc theo Người tạo", "P2",
     NKQ + "\nTP-1 thấy được phiếu của KTV-1 và KTV-3 (cùng PKT1); NKQ-07 do KTV-3 lập, Chờ duyệt kết quả",
     "1. Đăng nhập TP-1, mở màn\n"
     "2. Ô Người tạo chọn KTV-3",
     "—",
     "- Chỉ còn NKQ-07"),

    ("010", "Lọc Công ty / Phòng ban", "P1",
     NKQ + "\nTGĐ có quyền xem theo tổng công ty; NKQ-09 thuộc TPC",
     "1. Đăng nhập TGĐ, mở màn\n"
     "2. Ô Công ty chọn TPC",
     "—",
     "- Mong đợi: chỉ còn phiếu của TPC (NKQ-09)\n"
     "- Lưu ý: theo code hiện tại bảng không đổi, vẫn đủ phiếu mọi công ty - ghi Failed (ô Phòng ban cũng "
     "không có tác dụng)"),

    ("011", "Không có kết quả", "P2",
     NKQ,
     "1. " + OPEN_KTV1 + "\n"
     "2. Ô Số phiếu giao việc gõ \"XYZ\"",
     "—",
     "- Bảng báo không có dữ liệu"),
]

SEC_III = [
    ("001", "Nút Nhập kết quả hiện cho người thực hiện", "P0",
     DATA,
     "1. Đăng nhập KTV-1, " + MENU_DG + "\n"
     "2. Bấm nút bánh răng dòng PGV-02",
     "Tài khoản: KTV-1",
     "- Có \"Nhập kết quả\""),

    ("002", "Phiếu công tác chưa duyệt thì không có nút", "P0",
     DATA,
     "1. Đăng nhập KTV-1, " + MENU_DG + "\n"
     "2. Bấm nút bánh răng dòng PGV-05",
     "—",
     "- Không có \"Nhập kết quả\""),

    ("003", "Người không thực hiện, không có quyền thì không có nút", "P0",
     DATA + "\nKTV-2 có quyền \"Xem phiếu giao việc theo phòng ban\" nên thấy PGV-02",
     "1. Đăng nhập KTV-2, " + MENU_PGV + "\n"
     "2. Bấm nút bánh răng dòng PGV-02",
     "—",
     "- Không có \"Nhập kết quả\""),

    ("004", "Quyền \"Nhập kết quả thực hiện\" nhập thay được", "P1",
     DATA + "\nTP-1 có quyền \"Nhập kết quả thực hiện\" và thấy PGV-02",
     "1. Đăng nhập TP-1, " + MENU_PGV + "\n"
     "2. Bấm nút bánh răng dòng PGV-02",
     "—",
     "- Có \"Nhập kết quả\", bấm vào mở form nhập kết quả của PGV-02"),

    ("005", "Đã có phiếu nhập kết quả thì ẩn nút", "P0",
     DATA + "\nPGV-02 đã có NKQ-02 (Đang tạo)",
     "1. Đăng nhập KTV-1, " + MENU_DG + "\n"
     "2. Bấm nút bánh răng dòng PGV-02",
     "—",
     "- Không có \"Nhập kết quả\"\n"
     "- Có \"Xem phiếu nhập kết quả\" mở NKQ-02"),

    ("006", "Form nhập kết quả lấy sẵn thông tin phiếu giao việc", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-01"),
     "—",
     "- Tiêu đề \"Phiếu nhập kết quả\"\n"
     "- Phiếu giao việc PGV-01, Khách hàng, Địa chỉ lắp đặt, Người liên hệ, SĐT lấy theo PGV-01\n"
     "- Người yêu cầu và SĐT là người lập LD-01\n"
     "- Bảng \"A - Hạng mục lắp đặt, bàn giao\" có dòng M3\n"
     "- Có nút Lưu, \"Lưu & Gửi duyệt\", Quay lại"),

    ("007", "Form theo nguồn hợp đồng SC - BH", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-02"),
     "—",
     "- Có bảng \"A - TÍNH CÔNG BẢO HÀNH SỬA CHỮA\" với \"I - Dịch vụ sửa chữa\" dòng M1 lỗi E1, ĐM công 2\n"
     "- Dịch vụ \"Vệ sinh máy\" và vật tư VT1 nằm dưới dòng M1\n"
     "- Có \"B - Công phụ tính P3\" và \"II - Tổng công định mức\""),

    ("008", "Form theo nguồn giao việc khác", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-04"),
     "—",
     "- Có bảng \"A - TÍNH CÔNG DỊCH VỤ ĐÍNH KÈM\" dòng \"Khảo sát mặt bằng\" ĐM công 0,5\n"
     "- Ô Phiếu YCGV khác là YC-01"),

    ("009", "Mở thẳng form cho phiếu giao việc có phiếu công tác chưa duyệt", "P1",
     DATA,
     "1. Đăng nhập KTV-1, dán đường dẫn form nhập kết quả của PGV-05\n"
     "2. Tích Đã hoàn thành dòng M1, nhập serial S1, bấm Lưu",
     "—",
     "- Form vẫn mở được\n"
     "- Bấm Lưu báo \"Chỉ được nhập kết quả khi phiếu công tác (PCT) đã được duyệt\", không tạo phiếu"),
]

SEC_IV = [
    ("001", "Tích Đã hoàn thành dòng lắp đặt", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Tích Đã hoàn thành dòng M3",
     "—",
     "- % Hoàn thành = 100 và bị khóa\n"
     "- SL bàn giao tự điền 3, hiện 1 ô Serial (máy có serial)\n"
     "- SL tính công khoán 2; CK đề xuất duyệt 2; CK được tính dự kiến 1,6"),

    ("002", "Nhập một phần % Hoàn thành", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Không tích Đã hoàn thành, nhập % Hoàn thành 50, SL bàn giao 3",
     "—",
     "- CK đề xuất duyệt = 1 x 2 x 50% = 1\n"
     "- CK được tính dự kiến 0,8"),

    ("003", "% Hoàn thành từ 100 trở lên không nhận khi chưa tích", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Không tích Đã hoàn thành, gõ % Hoàn thành 120",
     "—",
     "- Ô không nhận giá trị 120 (giữ số cũ)\n"
     "- CK đề xuất duyệt không vượt 2"),

    ("004", "% Hoàn thành âm", "P1",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Không tích Đã hoàn thành, gõ % Hoàn thành -50, bấm Lưu",
     "—",
     "- Mong đợi: báo % Hoàn thành không hợp lệ\n"
     "- Lưu ý: theo code hiện tại nhận -50, CK đề xuất duyệt -1 và lưu được - ghi Failed"),

    ("005", "Đổi SL bàn giao thì đổi SL tính công khoán", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Tích Đã hoàn thành, sửa SL bàn giao thành 1",
     "—",
     "- SL tính công khoán = 1 (1 chia 2, làm tròn lên)\n"
     "- CK đề xuất duyệt 1\n"
     "- Dòng \"Tổng công được tính\": SL bàn giao 1, SL tính công khoán 1"),

    ("006", "Đã hoàn thành mà bỏ trống serial", "P0",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Tích Đã hoàn thành dòng M3, để trống Serial, bấm Lưu",
     "—",
     "- Báo lỗi bắt buộc nhập Serial ở dòng M3, không tạo phiếu"),

    ("007", "Serial đã thuộc hàng khác", "P1",
     DATA + "\nSerial SX-9 đang là serial của hàng M9",
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Tích Đã hoàn thành, nhập Serial SX-9, bấm Lưu",
     "—",
     "- Báo \"Serial \"SX-9\" đã tồn tại cho sản phẩm khác\", không tạo phiếu"),

    ("008", "Serial đã hoàn thành ở phiếu giao việc khác", "P0",
     DATA + "\nSerial S3-1 của M3 (HDH-01) đã nhập kết quả 100% ở phiếu giao việc PGV-21",
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Tích Đã hoàn thành, nhập Serial S3-1, bấm Lưu",
     "—",
     "- Báo \"Seri đã hoàn thành nhập kết quả, không được nhập tiếp!\""),

    ("009", "Serial đã làm một phần ở phiếu khác", "P1",
     DATA + "\nSerial S3-2 của M3 (HDH-01) đã nhập 60% ở PGV-22",
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Không tích Đã hoàn thành, % Hoàn thành 50, Serial S3-2, bấm Lưu",
     "—",
     "- Báo \"Bạn cần phải nhập tối đa bằng 40\", không tạo phiếu"),

    ("010", "Phiếu yêu cầu xuất hàng chưa hạch toán", "P0",
     DATA + "\nĐổi dữ liệu: XH-01 của máy M3 chưa hạch toán",
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Tích Đã hoàn thành dòng M3, nhập serial S3-5, bấm Lưu",
     "—",
     "- Hiện hộp \"Cảnh báo !\" ghi \"Phiếu yêu cầu xuất hàng 'XH-01' chưa được hạch toán\"\n"
     "- Không tạo phiếu"),

    ("011", "Dòng chưa hoàn thành không bị chặn vì phiếu xuất chưa hạch toán", "P1",
     DATA + "\nĐổi dữ liệu: XH-01 chưa hạch toán",
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Không tích Đã hoàn thành, nhập % Hoàn thành 50, SL bàn giao 1, bấm Lưu",
     "—",
     "- Thông báo \"Tạo phiếu nhập kết quả thành công!\" (chỉ chặn dòng đã hoàn thành)"),

    ("012", "Tích Đã hoàn thành ở tiêu đề cột", "P2",
     DATA,
     "1. " + FROM_PGV.format(pgv="PGV-01") + "\n"
     "2. Tích ô Đã hoàn thành ở tiêu đề cột",
     "—",
     "- Mọi dòng lắp đặt được tích Đã hoàn thành, % = 100"),
]
