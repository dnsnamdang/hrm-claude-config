# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Bao cao han muc cong no nhan vien'."""

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Theo dõi nhân viên kinh doanh đang để khách hàng nợ bao nhiêu so với Hạn mức công nợ xuất hàng "
     "khai báo trong hồ sơ nhân viên.\n"
     "- Mỗi dòng là 1 nhân viên: Mã nhân viên, Tên nhân viên, Bộ phận, Phòng ban, Hạn mức công nợ xuất "
     "hàng, Tổng công nợ khách hàng hiện tại.\n"
     "- Bấm biểu tượng chữ i cạnh Mã nhân viên để mở cửa sổ chi tiết công nợ của nhân viên đó theo "
     "từng khách hàng.\n"
     "- Màn chỉ để xem: không sửa, không xuất Excel, không in.\n"
     "- Lưu ý: Hạn mức công nợ nhân viên hiện KHÔNG được dùng để chặn Phiếu yêu cầu xuất hàng (phần kiểm "
     "tra theo nhân viên đang tắt); báo cáo này chỉ mang tính theo dõi."),

    ("2. Đối tượng được tính / hiển thị",
     "- Mọi nhân viên có ô \"Hạn mức công nợ xuất hàng\" trong hồ sơ nhân viên LỚN HƠN 0.\n"
     "- Gồm cả nhân viên đã nghỉ việc / bị khóa tài khoản, nhân viên của MỌI công ty.\n"
     "- Tổng công nợ khách hàng hiện tại = tổng phát sinh Nợ trừ tổng phát sinh Có trên tài khoản 131 "
     "(và các tài khoản con) của các bút toán gắn với hợp đồng DO CHÍNH NHÂN VIÊN ĐÓ LẬP, gồm: hợp đồng "
     "bán hàng, hợp đồng nguyên tắc / mở, biên bản thanh lý, hợp đồng dịch vụ, hợp đồng dự án; cộng "
     "dồn cho mọi khách hàng."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Nhân viên có Hạn mức công nợ xuất hàng để trống hoặc bằng 0 KHÔNG xuất hiện.\n"
     "- Công nợ trên hợp đồng do người khác lập (dù nhân viên đó phụ trách khách) KHÔNG được tính.\n"
     "- Bút toán không gắn với hợp đồng (vd chứng từ thu chi không chọn hợp đồng) KHÔNG được tính.\n"
     "- Chỉ tiêu \"Trong hạn mức\" lấy công nợ NHỎ HƠN hạn mức; \"Vượt hạn mức\" lấy công nợ LỚN HƠN hạn "
     "mức. Nhân viên có công nợ ĐÚNG BẰNG hạn mức bị loại khỏi cả hai.\n"
     "- Màn không có nút Tạo mới, Sửa, Xóa, In, Xuất Excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Hai ô \"Từ ngày\" và \"Đến ngày\" lọc theo NGÀY GHI SỔ (ngày tạo) của bút toán công nợ, không phải "
     "ngày hợp đồng. Bỏ trống = lấy toàn bộ phát sinh từ trước tới nay.\n"
     "- Lưu ý: ô \"Đến ngày\" so với mốc 0 giờ của ngày đó, nên bút toán ghi sổ trong chính ngày điền ở "
     "ô Đến ngày bị loại.\n"
     "- Bộ lọc thời gian chỉ ảnh hưởng cột \"Tổng công nợ khách hàng hiện tại\" và chỉ tiêu Trong/Vượt hạn "
     "mức; KHÔNG làm ẩn nhân viên.\n"
     "- Cửa sổ chi tiết theo khách hàng cũng nhận khoảng ngày từ màn chính, nhưng có lỗi (xem mục 9)."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Hai cấp: Nhân viên > Khách hàng (trong cửa sổ chi tiết).\n"
     "- Bộ phận, Phòng ban lấy từ hồ sơ nhân sự hiện tại của nhân viên.\n"
     "- Hạn mức công nợ xuất hàng là 1 con số chung cho nhân viên, không chia theo công ty.\n"
     "- Cửa sổ chi tiết: tiêu đề \"Thông tin chi tiết hạn mức dư nợ nhân viên <Mã> - <Tên> theo khách "
     "hàng\", các cột STT · Mã khách · Tên khách · Công nợ; ô lọc Khách hàng, Số tiền từ, Số tiền đến."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Màn chính: 1 nhân viên = 1 dòng, công nợ cộng dồn mọi khách và mọi hợp đồng do nhân viên lập.\n"
     "- Cửa sổ chi tiết: mong đợi 1 khách = 1 dòng với công nợ riêng của khách đó.\n"
     "- Lưu ý: theo code hiện tại cột Công nợ trong cửa sổ chi tiết là SỐ LŨY KẾ chạy qua các khách (khách "
     "sau cộng dồn cả công nợ khách trước), không phải công nợ riêng từng khách (xem TC_10.003)."),

    ("7. Phân quyền cấp",
     "Màn không có quyền riêng: mục menu luôn hiện, mọi tài khoản đăng nhập đều xem được TOÀN BỘ nhân "
     "viên của mọi công ty.\n"
     "Các quyền xem theo cấp dùng chung chỉ quyết định Ô LỌC nào hiện trong khối Bộ lọc, KHÔNG giới hạn "
     "dữ liệu:\n"
     "- \"Xem tất cả phiếu\": hiện ô Công ty và ô Phòng ban (mọi công ty).\n"
     "- \"Xem tất cả phiếu của công ty\": hiện ô Phòng ban (chỉ phòng ban công ty mình).\n"
     "- \"Xem tất cả phiếu của phòng ban\": hiện ô Phòng ban (các phòng mình quản lý) và ô Bộ phận.\n"
     "- Không có quyền nào ở trên: không có ô Công ty / Phòng ban / Bộ phận.\n"
     "Ô Nhân viên, Chỉ tiêu vượt hạn mức, Từ ngày, Đến ngày luôn hiện."),

    ("8. Cách tính các ô thống kê",
     "- Cột \"Tổng công nợ khách hàng hiện tại\" = tổng Nợ - tổng Có tài khoản 131 trên hợp đồng do nhân "
     "viên lập, trong khoảng ngày lọc. Có thể âm khi khách trả thừa.\n"
     "- Cột STT = thứ tự trong toàn danh sách (trang 2 bắt đầu từ 11).\n"
     "- Số tiền định dạng có dấu phẩy ngăn cách hàng nghìn, không có số lẻ.\n"
     "- Dòng \"Hiển thị a đến b của N mục\" dưới bảng: N là tổng nhân viên khớp bộ lọc."),

    ("9. Ghi chú đọc bảng",
     "- Phân trang mặc định 10 dòng, có ô chọn số dòng mỗi trang.\n"
     "- Hệ thống ghi nhớ bộ lọc lần trước khi mở lại màn trên cùng trình duyệt.\n"
     "- Bẫy 1: ô lọc \"Nhân viên\" KHÔNG có tác dụng - chọn nhân viên nào thì danh sách vẫn ra đủ.\n"
     "- Bẫy 2: Công ty / Phòng ban / Bộ phận lọc theo hồ sơ nhân sự HIỆN TẠI của nhân viên, không phải "
     "nơi phát sinh hợp đồng.\n"
     "- Bẫy 3: nhân viên có công nợ bằng đúng hạn mức không thuộc chỉ tiêu nào.\n"
     "- Bẫy 4: cửa sổ chi tiết khi có điền \"Từ ngày\" sẽ dùng ngày đó cho cả hai đầu nên gần như luôn "
     "trống; điền mỗi \"Đến ngày\" thì bị bỏ qua.\n"
     "- Bẫy 5: cột Công nợ trong cửa sổ chi tiết là số lũy kế (xem mục 6); tổng màn chính và dòng cuối "
     "của cửa sổ chi tiết mới khớp nhau.\n"
     "- Màn cùng đường dẫn với Báo cáo hạn mức công nợ khách hàng, chỉ khác mục menu; vào nhầm mục menu "
     "sẽ ra báo cáo khách hàng."),
]

ROLE_TCS = [
    ("00", "Tài khoản không có quyền xem theo cấp vẫn xem được toàn bộ", "P0",
     "Tài khoản NV-A không có quyền \"Xem tất cả phiếu\", \"Xem tất cả phiếu của công ty\", \"Xem tất cả "
     "phiếu của phòng ban\"\n"
     "Hệ thống có 14 nhân viên có hạn mức > 0, thuộc 3 công ty",
     "1. Đăng nhập bằng NV-A\n"
     "2. Vào menu Kế toán > Kế toán Công nợ > nhóm Nhân viên > bấm \"Báo cáo hạn mức công nợ nhân viên\"\n"
     "3. Bấm nút Bộ lọc\n"
     "4. Đọc tổng số dòng dưới bảng",
     "Tài khoản: NV-A",
     "- Mục menu hiển thị, màn mở được\n"
     "- Khối lọc chỉ có: Nhân viên, Chỉ tiêu vượt hạn mức, Từ ngày, Đến ngày\n"
     "- KHÔNG có ô Công ty / Phòng ban / Bộ phận\n"
     "- Tổng hiện 14 (nhân viên của cả 3 công ty)"),

    ("01", "Quyền Xem tất cả phiếu: có ô Công ty và Phòng ban", "P0",
     "Tài khoản B có quyền \"Xem tất cả phiếu\"",
     "1. Đăng nhập B, mở báo cáo\n"
     "2. Bấm Bộ lọc, quan sát các ô\n"
     "3. Chọn Công ty 3, mở ô Phòng ban",
     "Công ty: Công ty 3",
     "- Có ô Công ty và ô Phòng ban\n"
     "- Sau khi chọn Công ty 3, ô Phòng ban chỉ còn phòng ban của Công ty 3"),

    ("02", "Quyền Xem tất cả phiếu của công ty: chỉ có ô Phòng ban công ty mình", "P0",
     "Tài khoản C có quyền \"Xem tất cả phiếu của công ty\", thuộc Công ty 1",
     "1. Đăng nhập C, mở báo cáo\n"
     "2. Bấm Bộ lọc, mở ô Phòng ban\n"
     "3. Không chọn gì, bấm tìm kiếm, đọc tổng",
     "—",
     "- Không có ô Công ty\n"
     "- Ô Phòng ban chỉ liệt kê phòng ban của Công ty 1\n"
     "- Lưu ý: khi chưa chọn phòng ban, danh sách VẪN gồm nhân viên của mọi công ty (14 dòng)"),

    ("03", "Quyền Xem tất cả phiếu của phòng ban: ô Phòng ban được quản lý và ô Bộ phận", "P1",
     "Tài khoản D có quyền \"Xem tất cả phiếu của phòng ban\", quản lý Phòng KD1 và KD2",
     "1. Đăng nhập D, mở báo cáo\n"
     "2. Bấm Bộ lọc, mở ô Phòng ban và ô Bộ phận",
     "—",
     "- Ô Phòng ban chỉ có KD1, KD2\n"
     "- Có thêm ô Bộ phận"),

    ("04", "Quyền xem theo cấp không giới hạn dữ liệu", "P0",
     "Tài khoản C (quyền của công ty, Công ty 1)\n"
     "Nhân viên NV-X thuộc Công ty 3 có hạn mức 100,000,000",
     "1. Đăng nhập C, mở báo cáo, không chọn bộ lọc\n"
     "2. Tìm dòng NV-X",
     "—",
     "- NV-X VẪN hiện trong danh sách\n"
     "- Lưu ý: dữ liệu không bị khoanh theo công ty / phòng ban của người xem - ghi nhận nếu nghiệp vụ "
     "yêu cầu giới hạn"),
]
