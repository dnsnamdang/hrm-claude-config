# -*- coding: utf-8 -*-
"""Section IV, V, VI - xuat lai & tru ton, rang buoc, xem chi tiet."""
from tc_data_role import NK1

SEC_IV = [
    ("033", "Xuất lại thành công", "P0",
     NK1,
     "1. Đăng nhập TK-1, mở form tạo, chọn NK-1\n"
     "2. Nhập Ghi chú \"Nhập sai SL H1\", bấm Xuất lại",
     "Ghi chú: Nhập sai SL H1",
     "- Báo \"Hàng đã được xuất lại\"\n"
     "- Chuyển về danh sách phiếu xuất lại của tôi, phiếu mới ở đầu: mã PXL-xxxxx, Phiếu NK = NK-1, Ngày "
     "lập hôm nay, Người lập TK-1, Trạng thái Chờ nhập lại"),

    ("034", "Tồn kho của hàng giảm đúng", "P0",
     NK1 + "\nĐã xuất lại NK-1 thành công",
     "1. Mở Báo cáo tồn kho tổng hợp theo mặt hàng, kho K1",
     "—",
     "- H1 còn 5 Cái\n"
     "- H2 còn 6 Cái"),

    ("035", "Tồn theo vị trí giảm đúng", "P0",
     NK1 + "\nĐã xuất lại NK-1",
     "1. Mở Báo cáo tồn kho theo vị trí, kho K1",
     "—",
     "- P1: H1 = 3; P2: H1 = 2; P3: H2 = 6"),

    ("036", "Hàng ĐVT lớn trừ theo hệ số", "P0",
     NK1 + "\nĐã xuất lại NK-1",
     "1. Xem tồn H2 tại P3 theo ĐVT Cái",
     "—",
     "- P3 giảm đúng 24 Cái (2 Thùng nhân 12), còn 6"),

    ("037", "Lô của phiếu nhập về 0", "P0",
     NK1 + "\nĐã xuất lại NK-1",
     "1. Mở Báo cáo tồn kho chi tiết theo mặt hàng, kho K1, hàng H1",
     "—",
     "- Không còn lô của NK-1 tại P1, P2; các lô khác giữ nguyên số"),

    ("038", "Thẻ kho ghi dòng xuất lại", "P0",
     NK1 + "\nĐã xuất lại NK-1 bằng PXL-1",
     "1. Mở Thẻ kho, kho K1, hàng H1, khoảng ngày gồm hôm nay",
     "—",
     "- Có dòng xuất 10 thuộc phiếu xuất lại PXL-1; tồn sau dòng này = 5\n"
     "- Bấm số chứng từ mở được phiếu xuất lại"),

    ("039", "Tồn của công ty thuê kho giảm đúng", "P0",
     NK1 + "\nK1 có công ty thuê kho TPE, TPC; NK-1 nhập cho TPE; TPC có H1 = 7 ở P4",
     "1. Xuất lại NK-1\n"
     "2. Xem tồn H1 theo từng công ty thuê kho",
     "—",
     "- TPE giảm 10; TPC giữ nguyên 7"),

    ("040", "Phiếu nhập gốc chuyển Đã xuất lại", "P0",
     NK1 + "\nĐã xuất lại NK-1",
     "1. Mở danh sách Phiếu nhập kho, xem dòng NK-1",
     "—",
     "- Trạng thái \"Đã xuất lại\"\n"
     "- Bánh răng không còn \"Tạo phiếu xuất lại\", có \"Tạo phiếu nhập lại\""),

    ("041", "Không xuất lại lần 2 cùng phiếu nhập", "P0",
     NK1 + "\nĐã xuất lại NK-1",
     "1. Mở form tạo, bấm kính lúp",
     "—",
     "- Cửa sổ tìm không còn NK-1"),

    ("042", "Gửi lại lệnh lưu lần 2 bằng công cụ", "P0",
     NK1 + "\nĐã xuất lại NK-1",
     "1. Dùng công cụ kiểm thử API gửi lại lệnh tạo phiếu xuất lại cho NK-1",
     "—",
     "- Báo \"Không đủ quyền!\", tồn H1 vẫn 5, không có phiếu mới"),

    ("043", "Bấm Xuất lại liên tiếp 2 lần", "P1",
     NK1,
     "1. Chọn NK-1, bấm nhanh Xuất lại 2 lần",
     "—",
     "- Nút bị khóa khi đang xử lý, chỉ tạo 1 phiếu, tồn H1 còn 5 (không âm)"),

    ("044", "Không phát sinh bút toán kế toán", "P1",
     NK1 + "\nĐã xuất lại NK-1",
     "1. Mở sổ nhật ký chung, lọc hôm nay",
     "—",
     "- Không có bút toán nào từ phiếu xuất lại PXL-1"),

    ("045", "Ghi chú được lưu", "P1",
     "Đã xuất lại với Ghi chú \"Nhập sai SL H1\"",
     "1. Mở chi tiết phiếu vừa tạo",
     "—",
     "- Ô Ghi chú = \"Nhập sai SL H1\""),

    ("046", "Phiếu xuất lại thuộc công ty, phòng ban của phiếu nhập", "P1",
     "NK-1 của TPE, phòng Kho; TK-1 xuất lại",
     "1. GD-1 (Xem tất cả phiếu của công ty TPE) mở danh sách, lọc Phòng ban Kho",
     "—",
     "- Thấy phiếu xuất lại của NK-1"),
]

SEC_V = [
    ("047", "Không chọn phiếu nhập kho", "P0",
     "Đang ở form tạo trống",
     "1. Bấm Xuất lại",
     "—",
     "- Báo \"Tạo thất bại!\"\n"
     "- Dưới ô Chọn phiếu nhập kho: \"Bắt buộc phải chọn\""),

    ("048", "Ghi chú quá 255 ký tự", "P0",
     NK1,
     "1. Chọn NK-1, nhập Ghi chú 256 ký tự, bấm Xuất lại",
     "Ghi chú: 256 ký tự",
     "- Báo \"Tạo thất bại!\", dưới ô Ghi chú: \"Không được vượt quá 255 ký tự\"\n"
     "- Tồn H1 vẫn 15"),

    ("049", "Ghi chú đúng 255 ký tự", "P1",
     NK1,
     "1. Nhập Ghi chú 255 ký tự, bấm Xuất lại",
     "Ghi chú: 255 ký tự",
     "- Tạo thành công"),

    ("050", "Ghi chú để trống", "P1",
     NK1,
     "1. Để trống Ghi chú, bấm Xuất lại",
     "—",
     "- Tạo thành công, Ghi chú trống"),

    ("051", "Tồn kho của hàng không đủ", "P0",
     NK1 + "\nSau khi NK-1 bị Không duyệt, đã xuất bán 8 H1 (tồn H1 còn 7, nhỏ hơn 10)",
     "1. Chọn NK-1, bấm Xuất lại",
     "—",
     "- Báo hàng không đủ tồn kho, cần 10 còn 7\n"
     "- Không tạo phiếu, tồn H1 vẫn 7, NK-1 vẫn Không duyệt"),

    ("052", "Tồn tại vị trí không đủ", "P0",
     NK1 + "\nĐã điều chuyển 5 H1 từ P1 sang P5 (P1 còn 4, nhỏ hơn 6)",
     "1. Chọn NK-1, bấm Xuất lại",
     "—",
     "- Báo không đủ tồn kho tại vị trí, cần 6 còn 4\n"
     "- Không tạo phiếu, mọi tồn giữ nguyên"),

    ("053", "Tồn lô tại vị trí không đủ", "P0",
     NK1 + "\nP1 vẫn đủ 9 nhưng lô của NK-1 tại P1 đã xuất 2 (còn 4)",
     "1. Chọn NK-1, bấm Xuất lại",
     "—",
     "- Báo không đủ tồn kho trong lô tại vị trí, cần 6 còn 4\n"
     "- Không tạo phiếu"),

    ("054", "Thông báo thiếu tồn ghi rõ tên hàng, vị trí", "P2",
     "Như TC 051 / 052",
     "1. Đọc thông báo lỗi",
     "—",
     "- Mong đợi: thông báo ghi tên hàng H1, mã vị trí P1\n"
     "- Lưu ý: theo code hiện tại ghi mã số nội bộ của hàng / vị trí, người dùng khó hiểu - ghi Failed nếu "
     "nghiệp vụ yêu cầu"),

    ("055", "Hàng có 2 dòng trong phiếu nhập, tồn đủ từng dòng nhưng thiếu tổng", "P1",
     "NK-6 Không duyệt có 2 dòng H1, mỗi dòng 6 (khác phụ lục); tồn H1 hiện còn 8",
     "1. Chọn NK-6, bấm Xuất lại",
     "—",
     "- Mong đợi: báo không đủ tồn (cần 12 còn 8)\n"
     "- Lưu ý: theo code hiện tại kiểm tra từng dòng riêng nên cho xuất, tồn H1 thành âm 4 - ghi Failed"),

    ("056", "Vị trí đang kiểm kê", "P1",
     NK1 + "\nP1 đang nằm trong phiếu kiểm kê chưa xong",
     "1. Chọn NK-1, bấm Xuất lại",
     "—",
     "- Mong đợi: chặn, báo vị trí đang kiểm kho (như khi nhập kho)\n"
     "- Lưu ý: theo code hiện tại vẫn cho xuất lại - ghi Failed"),

    ("057", "Lỗi giữa chừng không trừ dở dang", "P1",
     NK1 + "\nH1 đủ tồn; H2 tại P3 không đủ",
     "1. Chọn NK-1, bấm Xuất lại",
     "—",
     "- Báo lỗi thiếu tồn H2\n"
     "- H1 KHÔNG bị trừ (tồn vẫn 15), không có phiếu xuất lại nào được tạo"),
]

SEC_VI = [
    ("058", "Màn chi tiết hiển thị đúng thông tin", "P0",
     NK1 + "\nTK-1 đã xuất lại NK-1 bằng PXL-1 ngày 27/10/2026, Ghi chú \"Nhập sai SL H1\"",
     "1. Mở chi tiết PXL-1",
     "—",
     "- Phiếu nhập kho = NK-1 (bấm mở tab mới), Ngày lập 27/10/2026, Người giao hàng như NK-1, Ghi chú "
     "đúng\n"
     "- Bảng: H1 Tổng SL 10 (P1 6, P2 4); H2 Tổng SL 2 Thùng (P3 2)"),

    ("059", "Ô Kho trên màn chi tiết", "P1",
     "PXL-1 xuất lại NK-1 thuộc kho K1",
     "1. Mở chi tiết PXL-1, xem ô Kho",
     "—",
     "- Hiện tên kho K1"),

    ("060", "Ô Người lập trên chi tiết khi người khác xem", "P1",
     "PXL-1 do TK-1 lập; AD-1 (Super Admin) mở chi tiết",
     "1. Đăng nhập AD-1, mở chi tiết PXL-1, xem ô Người lập",
     "—",
     "- Mong đợi: TK-1\n"
     "- Lưu ý: theo code hiện tại hiện tên AD-1 (người đang xem) - ghi Failed"),

    ("061", "Nút Quay lại", "P2",
     "Đang ở chi tiết PXL-1",
     "1. Bấm Quay lại",
     "—",
     "- Về danh sách phiếu xuất lại do mình lập"),

    ("062", "Mở chi tiết phiếu không tồn tại", "P2",
     "—",
     "1. Dán đường dẫn chi tiết với mã phiếu không có",
     "—",
     "- Ra trang không tìm thấy, không lộ lỗi hệ thống"),
]
