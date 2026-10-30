# -*- coding: utf-8 -*-
"""Khoi 9 muc mo ta + nhom TC phan quyen cho man ERP 'Tong hop gia van chuyen de xuat'."""

MENU = ("Mở menu \"Vận chuyển - Bốc xếp\" > nhóm \"Vận chuyển với NCC\" > bấm \"Tổng hợp giá vận chuyển "
        "đề xuất\"")

MENU_MAU = ("Mở menu \"Vận chuyển - Bốc xếp\" > nhóm \"Vận chuyển với NCC\" > bấm \"Danh mục mẫu báo giá "
            "vận chuyển\"")

# Du lieu mau dung chung
MAU = ("Mẫu báo giá MB-1 (mã BGVC-...) do NV-VC1 lập, hiệu lực 01/11/2026 - 31/12/2026, không gắn bảng giá "
       "hiệu lực nào:\n"
       "- Loại xe \"Xe tải\" có 2 trọng tải \"1,5 tấn\" và \"5 tấn\"\n"
       "- 2 tuyến: \"K1 đi Hải Phòng\" 120 km, \"K1 đi Bắc Ninh\" 40 km")

NCC = ("File báo giá đã điền theo mẫu MB-1:\n"
       "- NCC A: giá cước vượt trội 1,5 tấn = 12.000, 5 tấn = 18.000; Hải Phòng: 2.000.000 / 3.500.000; "
       "Bắc Ninh: 1.000.000 / 1.800.000\n"
       "- NCC B: giá cước vượt trội 10.000 / 20.000; Hải Phòng: 2.200.000 / 3.200.000; Bắc Ninh: 900.000 / 0")

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Tổng hợp giá vận chuyển đề xuất: phiếu gom báo giá của nhiều nhà cung cấp (NCC) vận chuyển theo cùng "
     "một Mẫu báo giá vận chuyển (cùng loại xe, trọng tải, tuyến đường), so sánh giá từng ô và trình người có "
     "quyền \"Duyệt giá vận chuyển\" chốt giá.\n"
     "Luồng: ở Danh mục mẫu báo giá vận chuyển bấm \"Tổng hợp giá đề xuất\" để tạo phiếu (Đang tạo); ở danh "
     "sách bấm \"Nhập báo giá của NCC\" để tải file Excel của từng NCC; vào Sửa để chỉnh giá, bỏ NCC, đính kèm "
     "file rồi Gửi; người duyệt nhập giá duyệt, bấm Duyệt hoặc Không duyệt.\n"
     "Khi Duyệt: giá duyệt được ghi vào Bảng giá hiệu lực vận chuyển (tạo bảng mới, hoặc cập nhật bảng mà "
     "mẫu báo giá đã gắn) và người lập có nút \"Lập hợp đồng\" ở từng tab NCC."),

    ("2. Đối tượng được tính / hiển thị",
     "Phiếu có các trạng thái:\n"
     "- Đang tạo (nhãn xanh dương): vừa lưu hoặc bị Không duyệt; chỉ người lập thấy và sửa.\n"
     "- Chờ duyệt (nhãn vàng): đã Gửi.\n"
     "- Đã duyệt (nhãn xanh lá).\n"
     "- Đã lập hợp đồng / Đang lập hợp đồng: có trong bộ lọc nhưng theo code hiện tại không có thao tác nào "
     "đưa phiếu sang 2 trạng thái này.\n"
     "Danh sách mới tạo nhất lên đầu; cột: STT, Mã, Ghi chú, Người duyệt, Ngày duyệt, Người tạo, Ngày tạo, "
     "Ngày gửi, Trạng thái, Mẫu báo giá, Hành động."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Phiếu Đang tạo của người khác (kể cả khi có quyền xem theo công ty / tổng công ty).\n"
     "- Phiếu ngoài phạm vi quyền xem (phòng ban / công ty).\n"
     "- Màn danh sách không có nút Tạo mới: chỉ tạo được từ Danh mục mẫu báo giá vận chuyển.\n"
     "- Không có nút In; chỉ có Xuất excel từng phiếu."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Màn không có bộ lọc ngày. Ô lọc gồm: Mã, Ghi chú, Người tạo, Người duyệt, Trạng thái, Nhà cung cấp; "
     "người có quyền xem theo phòng ban / công ty / tổng công ty có thêm Công ty, Phòng ban.\n"
     "Ngày hiệu lực của bảng giá tạo ra khi Duyệt lấy theo Mẫu báo giá (Từ ngày - Đến ngày)."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Phiếu > nhiều NCC (mỗi NCC 1 tab, kèm file báo giá đã tải) > Loại xe > Trọng tải > Tuyến đường.\n"
     "Mỗi trọng tải có 1 Giá cước vượt trội; mỗi ô Tuyến x Trọng tải có 1 giá.\n"
     "File báo giá NCC lấy theo \"Mẫu báo giá\" tải ở cửa sổ nhập: dòng 8 tên loại xe, dòng 9 trọng tải, dòng "
     "10 giá cước vượt trội, từ dòng 11 mỗi dòng 1 tuyến (Tuyến, Số km, giá từng trọng tải).\n"
     "Màn Chi tiết có tab \"Tổng hợp\": mỗi trọng tải có cột từng NCC và cột \"Duyệt\"."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Ô giá nhỏ nhất khác 0 giữa các NCC được tô chữ xanh.\n"
     "- Cột Duyệt mặc định = giá nhỏ nhất khác 0 giữa các NCC; nếu mọi NCC đều 0 thì 0.\n"
     "- Giá duyệt là 1 bộ giá chung, áp cho mọi NCC của phiếu.\n"
     "- Nhập lại file cho NCC đã có: thay toàn bộ giá tuyến và giá cước vượt trội của NCC đó.\n"
     "Với dữ liệu mẫu: vượt trội 1,5 tấn 10.000, 5 tấn 18.000; Hải Phòng 2.000.000 / 3.200.000; Bắc Ninh "
     "900.000 / 1.800.000."),

    ("7. Phân quyền cấp",
     "- \"Quản lý chi phí vận chuyển\": mở danh sách, tạo, sửa, xóa, nhập báo giá NCC, Xuất excel.\n"
     "- \"Xem tổng hợp giá vận chuyển đề xuất theo tổng công ty / theo công ty / theo phòng ban\": phạm vi phiếu "
     "thấy ở danh sách; không có quyền nào chỉ thấy phiếu mình lập.\n"
     "- \"Duyệt giá vận chuyển\": thẻ chờ duyệt ở trang chủ, màn \"Tổng hợp giá đề xuất cần duyệt\" (phiếu Chờ "
     "duyệt của công ty mình), nút Duyệt / Không duyệt.\n"
     "- Sửa, Xóa, Nhập báo giá NCC: chỉ người lập, khi phiếu Đang tạo.\n"
     "Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật."),

    ("8. Cách tính các ô thống kê",
     "- Mã phiếu: THGVC- + số tự tăng 5 chữ số.\n"
     "- Ngày gửi: ngày bấm Gửi ở màn Sửa. Ngày duyệt, Người duyệt: ghi khi Duyệt hoặc Không duyệt.\n"
     "- Thẻ trang chủ \"Tổng hợp giá vận chuyển đề xuất\" = số phiếu Chờ duyệt do người cùng công ty lập.\n"
     "- Bảng giá hiệu lực tạo mới: công ty = công ty người duyệt, ngày hiệu lực và số km vượt trội lấy theo "
     "Mẫu báo giá; trùng khoảng ngày với bảng giá hiệu lực khác của công ty thì báo lỗi, không duyệt được."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n"
     "- File NCC để các tuyến khác thứ tự so với mẫu: tab Tổng hợp đặt giá sai tuyến.\n"
     "- Sửa giá ở màn Sửa lưu ngay khi bấm Lưu lại ở cửa sổ con, bấm Hủy phiếu không hoàn tác; gõ giá có dấu "
     "phẩy ngăn cách (1,500,000) chỉ lưu 1.\n"
     "- Duyệt bị chặn vì trùng bảng giá hiệu lực nhưng người lập vẫn nhận thông báo \"vừa duyệt\".\n"
     "- Nút Lập hợp đồng mở form hợp đồng trống, phiếu không bao giờ sang Đã lập hợp đồng.\n"
     "- Lọc Ghi chú, lọc Phòng ban không có tác dụng."),
]


ROLE_TCS = [
    ("00", "Không có quyền Quản lý chi phí vận chuyển thì không mở được màn", "P0",
     "NV-A không có quyền \"Quản lý chi phí vận chuyển\"",
     "1. Đăng nhập NV-A\n"
     "2. Dán đường dẫn màn Tổng hợp giá vận chuyển đề xuất",
     "Tài khoản: NV-A",
     "- Ra trang không tìm thấy"),

    ("01", "Nhân viên không có quyền xem chỉ thấy phiếu mình lập", "P0",
     "NV-VC1, NV-VC2 cùng phòng Vận tải, chỉ có quyền \"Quản lý chi phí vận chuyển\"; NV-VC2 có phiếu "
     "THGVC-2 Chờ duyệt",
     "1. Đăng nhập NV-VC1, " + MENU,
     "—",
     "- Không thấy THGVC-2\n"
     "- Chỉ thấy phiếu do NV-VC1 lập"),

    ("02", "Quyền xem theo phòng ban thấy phiếu của phòng", "P0",
     "TP-VC có quyền Quản lý chi phí vận chuyển và \"Xem tổng hợp giá vận chuyển đề xuất theo phòng ban\", "
     "cùng phòng NV-VC2; NV-VC2 có THGVC-2 Chờ duyệt và THGVC-3 Đang tạo",
     "1. Đăng nhập TP-VC, mở màn",
     "—",
     "- Thấy THGVC-2\n"
     "- Không thấy THGVC-3 (Đang tạo của người khác)"),

    ("03", "Quyền xem theo công ty thấy phiếu cả công ty", "P0",
     "GD-1 có quyền \"... theo công ty\", thuộc TPE; phiếu THGVC-2 của phòng Vận tải TPE, THGVC-9 của TPC "
     "(đều Chờ duyệt)",
     "1. Đăng nhập GD-1, mở màn",
     "—",
     "- Thấy THGVC-2, không thấy THGVC-9"),

    ("04", "Quyền xem theo tổng công ty thấy mọi công ty", "P1",
     "TGD có quyền \"... theo tổng công ty\"",
     "1. Đăng nhập TGD, mở màn",
     "—",
     "- Thấy cả THGVC-2 và THGVC-9\n"
     "- Không thấy phiếu Đang tạo của người khác"),

    ("05", "Người duyệt không có quyền Quản lý vẫn duyệt được từ trang chủ", "P0",
     "DGV-1 chỉ có quyền \"Duyệt giá vận chuyển\", thuộc TPE; THGVC-2 Chờ duyệt do NV-VC2 (TPE) lập",
     "1. Đăng nhập DGV-1, bấm thẻ \"Tổng hợp giá vận chuyển đề xuất\" ở trang chủ\n"
     "2. Bấm mã THGVC-2",
     "—",
     "- Thẻ hiện số 1, mở màn \"Tổng hợp giá đề xuất cần duyệt\" có THGVC-2\n"
     "- Màn Chi tiết có cột Duyệt nhập được, ô Ghi chú duyệt, nút Duyệt, Không duyệt"),

    ("06", "Người duyệt công ty khác không thấy phiếu", "P0",
     "DGV-2 có quyền Duyệt giá vận chuyển, thuộc TPC",
     "1. Đăng nhập DGV-2, mở thẻ chờ duyệt ở trang chủ\n"
     "2. Dán đường dẫn Chi tiết của THGVC-2 (TPE)",
     "—",
     "- Thẻ không đếm THGVC-2, danh sách cần duyệt không có THGVC-2\n"
     "- Mở đường dẫn: ra trang không tìm thấy"),

    ("07", "Gọi thẳng chức năng Duyệt cho phiếu công ty khác", "P1",
     "DGV-2 (TPC) có quyền Duyệt giá vận chuyển; THGVC-2 của TPE đang Chờ duyệt",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Duyệt THGVC-2 kèm giá duyệt và ghi chú",
     "—",
     "- Mong đợi: bị chặn \"Không có quyền!\"\n"
     "- Lưu ý: theo code hiện tại chỉ kiểm tra quyền và trạng thái, không kiểm tra công ty, nên duyệt được - "
     "ghi Failed"),

    ("08", "Người khác không thấy nút Sửa, Xóa, Nhập báo giá NCC", "P0",
     "NV-VC2 lập THGVC-2 Chờ duyệt; TP-VC thấy phiếu này nhờ quyền xem theo phòng ban",
     "1. Đăng nhập TP-VC, mở menu Hành động của THGVC-2",
     "—",
     "- Chỉ có \"Xuất excel\"\n"
     "- Không có Sửa, Xóa, Nhập báo giá của NCC"),

    ("09", "Gọi thẳng chức năng lưu Sửa phiếu không phải của mình", "P1",
     "NV-VC1 có quyền Quản lý chi phí vận chuyển; THGVC-4 Đã duyệt do NV-VC2 lập",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu Sửa THGVC-4 với trạng thái Đang tạo",
     "—",
     "- Mong đợi: bị chặn \"Không có quyền\"\n"
     "- Lưu ý: theo code hiện tại chức năng lưu Sửa không kiểm tra người lập và trạng thái; phiếu Đã duyệt "
     "bị đưa về Đang tạo, ghi chú bị đổi - ghi Failed"),

    ("10", "Xuất excel phiếu ngoài phạm vi xem qua đường dẫn", "P1",
     "NV-VC1 chỉ có quyền Quản lý chi phí vận chuyển; THGVC-9 của TPC",
     "1. Đăng nhập NV-VC1, dán đường dẫn Xuất excel của THGVC-9",
     "—",
     "- Mong đợi: không tải được file\n"
     "- Lưu ý: theo code hiện tại Xuất excel không kiểm tra quyền xem phiếu, tải được đủ giá các NCC - ghi Failed"),

    ("11", "Người duyệt tự duyệt phiếu của mình", "P2",
     "NV-VC3 có cả quyền Quản lý chi phí vận chuyển và Duyệt giá vận chuyển, lập và Gửi THGVC-6",
     "1. NV-VC3 mở Chi tiết THGVC-6",
     "—",
     "- Có nút Duyệt, Không duyệt và duyệt được\n"
     "- Lưu ý: nếu nghiệp vụ không cho tự duyệt phiếu mình lập thì ghi Failed"),
]
