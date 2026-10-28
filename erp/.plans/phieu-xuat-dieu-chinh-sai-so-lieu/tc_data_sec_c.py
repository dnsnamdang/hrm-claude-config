# -*- coding: utf-8 -*-
"""Section VII, VIII, IX, X - in & xuat excel, nhap lai, dong thoi & co lap, luong dau cuoi."""
from tc_data_role import NK1

SEC_VII = [
    ("063", "Xuất excel danh sách", "P0",
     "TK-1 có 3 phiếu xuất lại",
     "1. Mở danh sách, bấm Xuất excel",
     "—",
     "- Tải file \"danh_sach_phieu_xuat_lai.xlsx\" ở tab mới\n"
     "- Có tiêu đề công ty, dòng \"DANH SÁCH PHIẾU XUẤT LẠI\"; cột STT, Mã phiếu, Phiếu NK, Ngày lập, Người "
     "lập, Trạng thái; đúng 3 dòng, khớp số liệu trên màn"),

    ("064", "Excel theo bộ lọc", "P0",
     "Có 2 phiếu Chờ nhập lại, 1 phiếu Đã nhập lại",
     "1. Lọc Trạng thái Chờ nhập lại\n"
     "2. Bấm Xuất excel",
     "—",
     "- File chỉ có 2 dòng Chờ nhập lại"),

    ("065", "Excel lấy hết, không phân trang", "P1",
     "TK-1 có 12 phiếu, đang ở trang 1",
     "1. Bấm Xuất excel",
     "—",
     "- File có đủ 12 dòng"),

    ("066", "Excel theo phạm vi quyền", "P0",
     "TK-1 không có quyền xem phiếu nào; TK-2 lập PXL-2",
     "1. Đăng nhập TK-1, bấm Xuất excel",
     "—",
     "- File không có PXL-2"),

    ("067", "Excel khi lọc Người lập", "P2",
     "TP-1 thấy PXL-1 (TK-1) và PXL-3 (TK-3)",
     "1. Chọn Người lập TK-1, bấm Xuất excel",
     "—",
     "- Mong đợi: chỉ có PXL-1\n"
     "- Lưu ý: theo code hiện tại có cả PXL-3 - ghi Failed"),

    ("068", "Excel khi không có dữ liệu", "P2",
     "Bộ lọc không ra phiếu nào",
     "1. Bấm Xuất excel",
     "—",
     "- Tải được file chỉ có tiêu đề và dòng tên cột"),

    ("069", "In phiếu xuất lại", "P1",
     "PXL-1 do TK-1 lập",
     "1. Tìm nút In ở danh sách và màn chi tiết PXL-1",
     "—",
     "- Mong đợi: in được phiếu có đủ hàng, vị trí, SL\n"
     "- Lưu ý: theo code hiện tại không có nút In; dán thẳng đường dẫn in thì ra mẫu in không có số liệu - "
     "ghi Failed nếu nghiệp vụ cần in"),
]

SEC_VIII = [
    ("070", "Tạo phiếu nhập lại từ danh sách phiếu xuất lại", "P0",
     NK1 + "\nTK-1 đã xuất lại NK-1 (PXL-1 Chờ nhập lại); NK-1 đã xếp hàng xong",
     "1. Bấm bánh răng dòng PXL-1 > \"Tạo phiếu nhập lại\"",
     "—",
     "- Mở form nhập lại của NK-1, dữ liệu lấy theo NK-1"),

    ("071", "Nhập lại xong thì phiếu xuất lại chuyển Đã nhập lại", "P0",
     "Như trên",
     "1. Ở form nhập lại sửa H1 thành 8, xếp P1 = 8, bấm lưu và gửi\n"
     "2. Quay lại danh sách phiếu xuất lại",
     "—",
     "- PXL-1 \"Đã nhập lại\", bánh răng trống\n"
     "- NK-1 ở danh sách Phiếu nhập kho \"Đã nhập lại\""),

    ("072", "Tồn kho sau khi nhập lại", "P0",
     "Như TC 071 (tồn H1 sau xuất lại = 5)",
     "1. Xem tồn H1 tại K1",
     "—",
     "- H1 = 13 (5 + 8); P1 = 11"),

    ("073", "Chỉ lưu nháp phiếu nhập lại", "P1",
     "PXL-1 Chờ nhập lại, tồn H1 sau xuất lại = 5",
     "1. Bấm \"Tạo phiếu nhập lại\", nhập H1 = 8, chỉ bấm lưu (không gửi)\n"
     "2. Xem danh sách phiếu xuất lại và tồn H1",
     "—",
     "- Tồn H1 vẫn 5 (phiếu nhập lại đang tạo chưa cộng kho)\n"
     "- Mong đợi: PXL-1 vẫn Chờ nhập lại cho tới khi gửi\n"
     "- Lưu ý: theo code hiện tại PXL-1 chuyển ngay \"Đã nhập lại\" - ghi Failed nếu nghiệp vụ yêu cầu chờ gửi"),

    ("074", "Nhập lại khi chưa xếp hàng xong", "P1",
     "PXL-7 Chờ nhập lại từ NK-7; NK-7 chưa hoàn thành xếp hàng",
     "1. Bấm \"Tạo phiếu nhập lại\" ở dòng PXL-7",
     "—",
     "- Báo \"Chưa hoàn thành xếp hàng!\", ở lại danh sách"),

    ("075", "Phiếu nhập kho khác trạng thái không xuất lại được", "P0",
     "TK-1 có NK-2 Chờ duyệt, NK-3 Đã hạch toán",
     "1. Dùng công cụ kiểm thử API gửi lệnh tạo phiếu xuất lại cho NK-2, rồi NK-3",
     "—",
     "- Cả 2 lần báo \"Không đủ quyền!\", tồn không đổi"),
]

SEC_IX = [
    ("076", "Hai tab cùng xuất lại 1 phiếu nhập", "P1",
     NK1,
     "1. TK-1 mở form tạo ở 2 tab, cùng chọn NK-1\n"
     "2. Bấm Xuất lại ở tab 1, ngay sau đó ở tab 2",
     "—",
     "- Mong đợi: chỉ tab 1 thành công; tab 2 báo không đủ quyền hoặc không đủ tồn\n"
     "- H1 còn 5, không bị trừ 2 lần\n"
     "- Lưu ý: nếu có 2 phiếu xuất lại cho NK-1 thì ghi Failed"),

    ("077", "Xuất bán cùng lúc với xuất lại", "P2",
     NK1 + "\nTK-3 đang xuất kho 6 H1 tại P1 cùng lúc",
     "1. TK-1 bấm Xuất lại NK-1 cùng lúc TK-3 lưu phiếu xuất",
     "—",
     "- Một trong hai bị báo không đủ tồn; tồn P1 không âm"),

    ("078", "Người cùng công ty khác phòng không thấy phiếu", "P1",
     "TP-2 có quyền Xem tất cả phiếu của phòng ban, phòng Kinh doanh; PXL-1 phòng Kho",
     "1. Đăng nhập TP-2, mở màn",
     "—",
     "- Không thấy PXL-1"),

    ("079", "Xem chi tiết phiếu người khác qua đường dẫn", "P0",
     "PXL-1 do TK-1 lập; NV-A không phải Super Admin",
     "1. Đăng nhập NV-A, dán đường dẫn chi tiết PXL-1",
     "—",
     "- Ra trang không tìm thấy"),
]

SEC_X = [
    ("080", "Luồng chuẩn: nhập sai, không duyệt, xuất lại, nhập lại", "P0",
     "Kho K1 tồn H1 = 5 (P1 = 3, P2 = 2)",
     "1. TK-1 lập phiếu nhập kho NK-1 nhập H1 = 10 (P1 6, P2 4), xếp hàng xong\n"
     "2. KT-1 Không duyệt NK-1, lý do \"Sai SL, thực tế 8\"\n"
     "3. TK-1 mở Phiếu nhập kho, bánh răng NK-1 > \"Tạo phiếu xuất lại\", bấm Xuất lại\n"
     "4. TK-1 bấm \"Tạo phiếu nhập lại\", nhập H1 = 8 (P1 8), lưu và gửi duyệt\n"
     "5. KT-1 duyệt phiếu nhập lại",
     "—",
     "- Sau bước 1: H1 = 15\n"
     "- Sau bước 3: H1 = 5; NK-1 Đã xuất lại; PXL-1 Chờ nhập lại\n"
     "- Sau bước 4: H1 = 13; PXL-1 Đã nhập lại; NK-1 Đã nhập lại\n"
     "- Thẻ kho H1 có đủ 3 dòng: nhập 10, xuất lại 10, nhập 8"),

    ("081", "Luồng bị chặn do hàng đã xuất bán", "P0",
     "Như TC 080 sau bước 2; trước khi xuất lại, TK-3 đã xuất bán 7 H1 (tồn còn 8)",
     "1. TK-1 xuất lại NK-1",
     "—",
     "- Báo không đủ tồn (cần 10 còn 8); NK-1 vẫn Không duyệt, không có phiếu xuất lại\n"
     "- Tester ghi nhận: cần nhập bù hoặc xử lý khác trước khi xuất lại"),

    ("082", "Luồng phiếu nhập nhiều hàng, nhiều vị trí, có ĐVT lớn", "P0",
     NK1,
     "1. TK-1 xuất lại NK-1\n"
     "2. Kiểm tra Báo cáo tồn kho theo vị trí và Thẻ kho của H1, H2",
     "—",
     "- H1: P1 = 3, P2 = 2; H2: P3 = 6 Cái\n"
     "- Thẻ kho H1 có dòng xuất 10, H2 có dòng xuất 24 Cái, cùng chứng từ phiếu xuất lại"),

    ("083", "Phiếu xuất lại hiện đúng ở danh sách của người xem các cấp", "P1",
     "TK-1 (phòng Kho TPE) vừa tạo PXL-1",
     "1. Lần lượt đăng nhập TK-1, TP-1, GD-1, TGD-1, NV-A và mở màn",
     "—",
     "- TK-1, TP-1, GD-1, TGD-1 thấy PXL-1; NV-A không thấy"),
]
