# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Bao cao hang gui'."""

MENU = "Mở menu Kho > \"Tra cứu tồn kho\" > bấm \"Báo cáo hàng gửi\""

# Du lieu mau dung chung (hom nay 13/11/2026)
DATA = ("Công ty TPE: phòng PKD1 có NV-A, NV-B; phòng PKD2 có NV-C. Kho K1, K2 của TPE. "
        "Hàng H1 (ĐVT Cái, thêm ĐVT Thùng hệ số 12), hàng H2 (ĐVT Cái).\n"
        "Hàng gửi đã ghi nhận:\n"
        "- 05/10/2026 PNH-01 (từ PYCNH-01 của NV-A): KH-01 gửi H1 = 24 tại K1\n"
        "- 08/10/2026 PNH-03: NV-A, KH-02 gửi H2 = 10 tại K1\n"
        "- 12/10/2026 PXH-01 (từ PYCXH-01 của NV-A): xuất từ hàng gửi H1 của KH-01 = 6 tại K1\n"
        "- 15/10/2026 PNH-04: NV-C, KH-02 gửi H1 = 5 tại K1\n"
        "- 20/10/2026 PXH-03: NV-A xuất hết H2 của KH-02 = 10 tại K1\n"
        "- 03/11/2026 PNH-02: NV-A, KH-01 gửi H1 = 12 tại K2\n"
        "- 10/11/2026 PXH-02: NV-A xuất từ hàng gửi H1 của KH-01 = 6 tại K1")

KT = "KT-1 có quyền \"Xem báo cáo hàng gửi\" phạm vi Công ty, thuộc TPE"

LOC_T11 = "Chọn Từ ngày 01/11/2026, Đến ngày 30/11/2026, bấm Lọc"
LOC_T10 = "Chọn Từ ngày 01/10/2026, Đến ngày 31/10/2026, bấm Lọc"

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Báo cáo hàng gửi: cho biết trong một khoảng ngày, mỗi nhân viên kinh doanh đang giữ hộ khách hàng "
     "những hàng nào trong kho (hàng khách đã mua, gửi lại kho, chưa lấy), đầu kỳ còn bao nhiêu, trong kỳ "
     "gửi thêm bao nhiêu, đã xuất bao nhiêu và còn lại bao nhiêu.\n"
     "Người dùng làm được: lọc theo công ty, phòng ban, nhân viên, khách hàng, hàng hóa, kho, khoảng ngày; "
     "đổi đơn vị tính từng hàng; bấm SL gửi để mở cửa sổ chi tiết từng phiếu; In, Xuất excel. Màn chỉ xem, "
     "không sửa dữ liệu."),

    ("2. Đối tượng được tính / hiển thị",
     "- Hàng gửi tăng khi phiếu nhập hàng loại \"nhập gửi\" hoàn thành: ghi cho nhân viên đã lập phiếu yêu "
     "cầu nhập hàng, khách hàng của phiếu yêu cầu, tại kho của phiếu nhập.\n"
     "- Hàng gửi giảm khi phiếu xuất hàng có dòng \"xuất từ hàng gửi\" được hạch toán: trừ của nhân viên "
     "lập phiếu yêu cầu xuất hàng, đúng khách hàng, đúng kho.\n"
     "- Mỗi dòng hàng là 1 bộ nhân viên - khách hàng - hàng hóa, cộng gộp mọi kho (trừ khi lọc Kho).\n"
     "- Bảng phân cấp: Phòng ban (STT 1) > Nhân viên (1.1) > Khách hàng \"mã - tên\" (1.1.1) > Hàng "
     "(1.1.1.1); phòng ban xếp theo thứ tự tạo phòng."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Bộ nhân viên - khách hàng - hàng - kho đang có số còn HIỆN TẠI bằng 0 (đã xuất hết), dù trong kỳ có "
     "phát sinh.\n"
     "- Nhân viên ngoài phạm vi quyền xem.\n"
     "- Hàng chưa có ĐVT cơ bản.\n"
     "- Không có dòng Tổng cộng trên bảng chính."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Từ ngày, Đến ngày bắt buộc, tính theo ngày ghi nhận hàng gửi tăng / giảm (lúc phiếu nhập hoàn thành / "
     "phiếu xuất hạch toán), tính trọn ngày.\n"
     "- SL còn đầu kì: tổng phát sinh trước Từ ngày.\n"
     "- SL gửi, SL đã xuất: phát sinh tăng / giảm từ Từ ngày tới hết Đến ngày.\n"
     "- SL còn = SL còn đầu kì + SL gửi - SL đã xuất."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Bộ lọc: Công ty (chỉ quyền tổng công ty), Phòng ban, Nhân viên (theo quyền), Khách hàng, Hàng hóa (nút "
     "kính lúp, tìm cả hàng đã xóa), Kho, Từ ngày, Đến ngày; nút Lọc, làm mới, In, Xuất excel.\n"
     "Bảng: STT, Tên hàng hóa, Mã hàng, ĐVT (chọn được), SL còn đầu kì, SL gửi (bấm được), SL đã xuất, SL "
     "còn.\n"
     "Cửa sổ chi tiết: lọc Phiếu yêu cầu, Phiếu hạch toán, Kho; In; bảng STT, Phiếu yêu cầu, Phiếu hạch "
     "toán, Ngày hạch toán, Kho vật lý, SL còn đầu kì, SL gửi, SL xuất, SL còn; dòng Tổng cộng ở đầu."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Một nhân viên gửi cùng hàng cho cùng khách ở nhiều kho: cộng chung 1 dòng.\n"
     "- Đổi ĐVT: các số của hàng đó chia cho hệ số.\n"
     "Với dữ liệu mẫu, kỳ 01/11 - 30/11/2026: NV-A / KH-01 / H1 = đầu kì 18, gửi 12, xuất 6, còn 24; "
     "NV-C / KH-02 / H1 = đầu kì 5, còn 5.\n"
     "Kỳ 01/10 - 31/10/2026: NV-A / KH-01 / H1 = gửi 24, xuất 6, còn 18; NV-A / KH-02 / H2 = gửi 10, "
     "xuất 10, còn 0."),

    ("7. Phân quyền cấp",
     "- Quyền \"Xem báo cáo hàng gửi\" có 3 phạm vi: Phòng ban (nhân viên đang thuộc phòng mình), Công ty "
     "(hàng gửi ghi cho công ty mình), Tổng công ty (mọi công ty).\n"
     "- Không có quyền vẫn mở được màn (menu không ẩn), chỉ thấy hàng gửi của chính mình.\n"
     "- Super Admin không còn được ngoại lệ: chưa gán quyền thì như người không có quyền.\n"
     "- Cửa sổ chi tiết, In, Xuất excel áp cùng phạm vi.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Phân trang theo PHÒNG BAN: 10 phòng mỗi trang.\n"
     "- Cửa sổ chi tiết: 10 dòng mỗi trang; dòng Tổng cộng = SL còn đầu kì của dòng hàng + tổng SL gửi, "
     "SL xuất các phiếu trong kỳ; cột SL còn từng dòng là số còn của KHO đó sau phiếu.\n"
     "- In / Excel: đủ mọi trang, luôn theo ĐVT nhỏ nhất."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- Xem kỳ trong quá khứ: hàng đã xuất hết SAU kỳ đó không hiện (ví dụ kỳ 01/10 - 10/10 thiếu H2 của "
     "KH-02); còn hàng gửi SAU kỳ lại hiện thành dòng toàn số 0.\n"
     "- Cửa sổ chi tiết không tính phiếu của ngày Đến ngày, nên tổng lệch bảng chính.\n"
     "- Cửa sổ chi tiết đổi ĐVT: dòng Tổng cộng SL gửi, SL xuất vẫn theo ĐVT nhỏ nhất.\n"
     "- In / Xuất excel khi chưa chọn ngày ra trang lỗi.\n"
     "- Trưởng phòng phụ trách nhiều phòng chọn phòng khác ra bảng trống."),
]


ROLE_TCS = [
    ("00", "Không có quyền vẫn mở được màn, chỉ thấy hàng gửi của mình", "P0",
     "NV-A không có quyền \"Xem báo cáo hàng gửi\"\n" + DATA,
     "1. Đăng nhập NV-A\n"
     "2. " + MENU + "\n"
     "3. " + LOC_T11,
     "Tài khoản: NV-A",
     "- Mở được màn, không có ô Công ty, Phòng ban, Nhân viên\n"
     "- Chỉ có nhánh PKD1 > NV-A > KH-01 > H1; không có NV-C\n"
     "- Lưu ý: nếu nghiệp vụ yêu cầu chặn người không có quyền thì ghi Failed"),

    ("01", "Quyền phạm vi Phòng ban", "P0",
     "TP-1 trưởng PKD1, quyền phạm vi Phòng ban\n" + DATA,
     "1. Đăng nhập TP-1, mở màn\n"
     "2. " + LOC_T11,
     "—",
     "- Có ô Nhân viên, không có ô Công ty\n"
     "- Chỉ có phòng PKD1 (NV-A); không có PKD2 / NV-C"),

    ("02", "Quyền phạm vi Công ty", "P0",
     KT + "; TPC cũng có hàng gửi\n" + DATA,
     "1. Đăng nhập KT-1, mở màn\n"
     "2. " + LOC_T11,
     "—",
     "- Có ô Phòng ban, Nhân viên; không có ô Công ty\n"
     "- Có PKD1 và PKD2 của TPE; không có hàng gửi của TPC"),

    ("03", "Quyền phạm vi Tổng công ty", "P0",
     "TGĐ có quyền phạm vi Tổng công ty",
     "1. Đăng nhập TGĐ, mở màn\n"
     "2. " + LOC_T11,
     "—",
     "- Có thêm ô Công ty\n"
     "- Bảng có hàng gửi của cả TPE và TPC"),

    ("04", "Super Admin chưa được gán quyền", "P1",
     "SA có vai trò Super Admin nhưng vai trò chưa có quyền \"Xem báo cáo hàng gửi\"",
     "1. Đăng nhập SA, mở màn, lọc kỳ 01/11 - 30/11/2026",
     "—",
     "- Chỉ thấy hàng gửi do chính SA lập (thường trống)\n"
     "- Lưu ý: hành vi theo cơ chế quyền mới, không còn ngoại lệ Super Admin"),

    ("05", "Trưởng phòng phụ trách 2 phòng chọn phòng thứ hai", "P1",
     "TP-2 thuộc PKD1, phụ trách cả PKD1 và PKD2, quyền phạm vi Phòng ban\n" + DATA,
     "1. Đăng nhập TP-2, mở màn\n"
     "2. Ô Phòng ban chọn PKD2, chọn kỳ 01/11 - 30/11/2026, bấm Lọc",
     "—",
     "- Mong đợi: có NV-C / KH-02 / H1 còn 5\n"
     "- Lưu ý: theo code hiện tại bảng trống (chỉ xem được phòng đang thuộc) - ghi Failed"),

    ("06", "Gọi thẳng cửa sổ chi tiết của nhân viên ngoài phạm vi", "P1",
     "TP-1 quyền phạm vi Phòng ban (PKD1)\n" + DATA,
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy chi tiết hàng gửi với NV-C, KH-02, H1",
     "—",
     "- Không có dòng nào"),

    ("07", "Mở đường dẫn In / Xuất excel khi không có quyền", "P1",
     "NV-B không có quyền; có sẵn đường dẫn In kỳ 01/11 - 30/11/2026 do KT-1 copy",
     "1. Đăng nhập NV-B, dán đường dẫn In, rồi đường dẫn Xuất excel",
     "—",
     "- Bản in / file chỉ có hàng gửi của NV-B (trống), không có của NV-A, NV-C"),
]
