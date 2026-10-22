# -*- coding: utf-8 -*-
"""Section IV — tao moi / sua phieu kiem ke."""
from tc_data_role import P1

KH3 = ("Kế hoạch KH-3 Đang kiểm của kho K1, lập ngày 01/10/2026, có vị trí P1 và hội đồng 2 người\n"
       "TK1 có quyền Lập phiếu kiểm kê kho theo vị trí, là thủ kho K1")

SEC_IV = [
    ("001", "Lập phiếu từ nút trên Kế hoạch kiểm kê", "P0",
     KH3,
     "1. TK1 mở danh sách Kế hoạch kiểm kê theo vị trí, bấm bánh răng KH-3 > \"Lập phiếu kiểm kê theo vị trí\"\n"
     "2. Quan sát màn mở ra",
     "—",
     "- Tiêu đề trang \"Kiểm kê theo vị trí\"\n"
     "- Ô Kế hoạch kiểm kê hiện mã KH-3 (là liên kết)\n"
     "- Ngày kiểm kê = 01/10/2026 (ngày lập KH-3), bị khóa\n"
     "- Kho vật lý = K1; nhà, dãy, khoang, vị trí đã tích như KH-3\n"
     "- Tab Vị trí có sẵn P1 với số liệu ĐÃ CHỤP trong KH-3; tab Hội đồng có sẵn 2 người của KH-3"),

    ("002", "Bố cục màn Tạo mới khi vào từ nút Tạo mới", "P0",
     "TK1 như trên",
     "1. Mở danh sách Kiểm kê theo vị trí, bấm Tạo mới\n"
     "2. Quan sát",
     "—",
     "- Ô Kế hoạch kiểm kê trống, có nút X và nút kính lúp\n"
     "- Ngày kiểm kê = hôm nay, bị khóa; ô Kho vật lý \"Chọn kho kiểm\"\n"
     "- 4 khung Nhà, Dãy, Khoang, Vị trí và nút \"Lấy vị trí\"\n"
     "- Bảng chi tiết có cột \"ĐVT kiểm kê\"; KHÔNG có cột Thực kiểm, Chênh lệch, Ghi chú, Tổng kiểm kê\n"
     "- Không có khối File đính kèm, Ghi chú duyệt\n"
     "- Cuối trang: Lưu, Lưu & Gửi, Quay lại"),

    ("003", "Tìm kế hoạch bằng nút kính lúp", "P0",
     KH3 + "\nKho K2 (TK1 không là thủ kho) có kế hoạch KH-20 Đang kiểm; kho K1 có KH-21 Đã lập kiểm kê",
     "1. Ở màn Tạo mới bấm nút kính lúp cạnh ô Kế hoạch kiểm kê\n"
     "2. Quan sát hộp tìm, gõ mã KH-3 vào ô Mã phiếu",
     "Mã phiếu: mã của KH-3",
     "- Hộp tiêu đề \"Kế hoạch kiểm kê vị trí\", cột STT, Mã phiếu, Người tạo, Ngày tạo\n"
     "- Chỉ có kế hoạch Đang kiểm của kho K1: có KH-3, KHÔNG có KH-20, KH-21\n"
     "- Lọc Mã phiếu ra đúng KH-3"),

    ("004", "Chọn kế hoạch trong hộp tìm", "P0",
     KH3,
     "1. Mở hộp tìm, bấm chọn KH-3",
     "—",
     "- Thông báo xanh \"Thêm thành công\"\n"
     "- Màn được điền như TC_04.001"),

    ("005", "Bỏ kế hoạch đã chọn bằng nút X", "P1",
     "Đã chọn KH-3 như TC_04.004",
     "1. Bấm nút X cạnh ô Kế hoạch kiểm kê",
     "—",
     "- Ô Kế hoạch kiểm kê trống\n"
     "- Kho, phạm vi, bảng chi tiết, hội đồng đều trống, Ngày kiểm kê về hôm nay"),

    ("006", "Lập phiếu độc lập không gắn kế hoạch", "P0",
     P1 + "\nTK1 là thủ kho K1",
     "1. Bấm Tạo mới, chọn Kho vật lý = K1, tích N1 > D1 > KG1 > P1\n"
     "2. Bấm \"Lấy vị trí\"",
     "Kho vật lý: K1\n"
     "Vị trí: P1",
     "- Thông báo \"Thành công\"\n"
     "- P1 có HH-0091, SL tồn 30; công ty TPE (25), lô L01 (10), lô L02 (15); công ty ENE (5), lô L07 (5)\n"
     "- Mỗi lô 1 dòng kết quả: SL = SL lô, ĐVT kiểm kê = Cái"),

    ("007", "Bấm Lấy vị trí lại trên phiếu lập từ kế hoạch", "P1",
     KH3 + "\nKH-3 chụp P1 tồn 30; nay P1 còn 25",
     "1. Mở màn lập phiếu từ KH-3, đọc SL tồn\n"
     "2. Bấm \"Lấy vị trí\"",
     "—",
     "- Bước 1: SL tồn = 30 (số của kế hoạch)\n"
     "- Bước 2: SL tồn = 25 (tồn hiện tại)"),

    ("008", "Đổi ĐVT kiểm kê sang đơn vị lớn tự tách dòng phần lẻ", "P0",
     P1,
     "1. Lấy vị trí P1\n"
     "2. Ở dòng lô L02 (SL 15) đổi ĐVT kiểm kê sang Thùng",
     "ĐVT kiểm kê: Thùng (hệ số 12)",
     "- Dòng 1 của lô L02: SL = 1, ĐVT Thùng\n"
     "- Tự thêm dòng 2: SL = 3, ĐVT Cái\n"
     "- Lô L01, L07 không đổi"),

    ("009", "Đổi ĐVT khi không đủ để quy đổi", "P1",
     P1,
     "1. Ở dòng lô L01 (SL 10) đổi ĐVT kiểm kê sang Thùng",
     "ĐVT kiểm kê: Thùng (hệ số 12)",
     "- Thông báo vàng \"Số lượng không đủ để quy đổi!\"\n"
     "- Dòng giữ ĐVT Cái, SL 10"),

    ("010", "Đổi ĐVT về đơn vị cơ bản thì gộp lại 1 dòng", "P1",
     "Lô L02 đang tách 1 Thùng + 3 Cái như TC_04.008",
     "1. Ở dòng 1 của lô L02 đổi ĐVT kiểm kê về Cái",
     "ĐVT kiểm kê: Cái",
     "- Lô L02 còn 1 dòng: SL = 15, ĐVT Cái"),

    ("011", "Thêm, bớt thành viên Hội đồng kiểm kê", "P1",
     "Nhân viên NV-K có 2 vai trò Thủ kho, Kế toán kho",
     "1. Tab Hội đồng kiểm kê, bấm dấu +, chọn NV-K\n"
     "2. Mở ô Chức vụ\n"
     "3. Bấm dấu - ở dòng đó",
     "Thành viên: NV-K",
     "- Chức vụ tự điền vai trò đầu tiên, chọn được 1 trong 2 vai trò của NV-K\n"
     "- Bớt hết thì hiện \"Chưa có thành viên\""),

    ("012", "Bấm Lưu tạo phiếu nháp từ kế hoạch", "P0",
     KH3 + "\nTK1 thuộc công ty mã TPE",
     "1. Mở màn lập phiếu từ KH-3, bấm \"Lưu\"\n"
     "2. Tìm phiếu mới trên danh sách\n"
     "3. Mở danh sách Kế hoạch kiểm kê, xem KH-3",
     "—",
     "- \"Tạo thành công\", về danh sách lối vào menu\n"
     "- Phiếu mới: Số phiếu TPE-KKVT-<5 chữ số>, Ngày kiểm kê 01/10/2026, Kho K1, Đang tạo, Người lập TK1, Người duyệt trống\n"
     "- KH-3 chuyển \"Đã lập kiểm kê\""),

    ("013", "Bấm Lưu & Gửi chuyển sang Đang kiểm", "P0",
     KH3,
     "1. Mở màn lập phiếu từ KH-3, bấm \"Lưu & Gửi\"\n"
     "2. Bấm bánh răng phiếu mới",
     "—",
     "- Trạng thái Đang kiểm\n"
     "- Bánh răng có \"Nhập kết quả\", không còn Sửa, Xóa\n"
     "- Không phát sinh thông báo cho ai ở bước này"),

    ("014", "Phiếu độc lập có Ngày kiểm kê là ngày lập phiếu", "P1",
     "Như TC_04.006",
     "1. Thêm thành viên, bấm \"Lưu\"\n"
     "2. Đọc cột Ngày kiểm kê và cột Kế hoạch trên Chi tiết",
     "—",
     "- Ngày kiểm kê = hôm nay\n"
     "- Ô Kế hoạch kiểm kê trên Chi tiết trống"),

    ("015", "Mở Sửa phiếu nháp tự lấy lại tồn, giữ cách tách ĐVT nếu tồn không đổi", "P0",
     "Phiếu KK-4 Đang tạo: lô L02 tách 1 Thùng + 3 Cái; HH-0091 ở P1 tồn không đổi\n"
     "Ở vị trí P2 của KK-4, hàng HH-0100 tồn đổi từ 8 thành 6 sau khi lưu",
     "1. TK1 bấm bánh răng KK-4 > Sửa\n"
     "2. Quan sát P1 và P2",
     "—",
     "- Tiêu đề \"Kiểm kê theo vị trí: <Số phiếu>\"\n"
     "- Bảng tự tải lại theo tồn hiện tại\n"
     "- P1: lô L02 vẫn tách 1 Thùng + 3 Cái\n"
     "- P2: HH-0100 hiện tồn 6, dòng kết quả đặt lại theo ĐVT cơ bản"),

    ("016", "Sửa phiếu nháp rồi Lưu / Lưu & Gửi", "P0",
     "KK-4 Đang tạo có 2 thành viên",
     "1. Mở Sửa, thêm 1 thành viên, bấm \"Lưu\"\n"
     "2. Mở Sửa lần nữa, bấm \"Lưu & Gửi\"",
     "—",
     "- Bước 1: \"Tạo thành công\" (Lưu ý: nhãn chưa đổi thành Cập nhật), vẫn Đang tạo, có 3 thành viên, số phiếu không đổi\n"
     "- Bước 2: chuyển Đang kiểm"),

    ("017", "Bấm Lưu liên tiếp không sinh 2 phiếu", "P1",
     "Dữ liệu hợp lệ",
     "1. Bấm \"Lưu\" 2 lần thật nhanh",
     "—",
     "- Sau lần bấm đầu 2 nút lưu bị khóa, có biểu tượng quay\n"
     "- Chỉ 1 phiếu được tạo"),

    ("018", "Quay lại không lưu", "P2",
     "Đang ở màn Tạo mới, đã chọn kế hoạch KH-3",
     "1. Bấm \"Quay lại\"\n"
     "2. Xem KH-3",
     "—",
     "- Không có phiếu mới; KH-3 vẫn Đang kiểm"),

    ("019", "Tiền tố Số phiếu theo công ty người lập", "P2",
     "TK4 thuộc công ty mã ENE, là thủ kho K1 (kho công ty TPE)",
     "1. TK4 lập và Lưu phiếu cho kho K1",
     "—",
     "- Số phiếu bắt đầu ENE-KKVT-"),
]
