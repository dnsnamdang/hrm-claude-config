# -*- coding: utf-8 -*-
"""Section IV, V - tao / sua / chi tiet; cap nhat ket qua & gui duyet."""
from tc_data_role import H1

KH = "Kế hoạch kiểm kê theo hàng hóa"

SEC_IV = [
    ("001", "Ô Kho chỉ liệt kê kho của công ty mình", "P0",
     "NV-A thuộc công ty 1; công ty 1 có kho K1, K2; công ty 3 có kho K5",
     "1. Tạo mới, mở ô Kho",
     "—",
     "- Có K1, K2; không có K5\n"
     "- Chọn được nhiều kho"),

    ("002", "Chọn kho tự điền Công ty thuê kho", "P1",
     "Kho K1 có 2 kho kế toán thuộc công ty TPE và công ty thuê ENE",
     "1. Tạo mới, chọn Kho K1\n"
     "2. Mở ô Công ty thuê kho",
     "—",
     "- Ô Công ty thuê kho tự chọn sẵn cả TPE và ENE\n"
     "- Trước khi chọn kho, ô này bị khóa"),

    ("003", "Thêm hàng hiện đủ vị trí, công ty, lô", "P0",
     H1,
     "1. Tạo mới, chọn Kho K1\n"
     "2. Bấm dấu cộng ở bảng Hàng hóa, chọn H1",
     "Hàng: H1",
     "- Báo \"Thêm thành công\"\n"
     "- Dòng H1: SL tồn kho 40\n"
     "- Vị trí P1 (30): TPE, L01, Tồn theo lô 30, ĐVT kiểm kê Cái\n"
     "- Vị trí P2 (10): TPE, L02, Tồn theo lô 10, ĐVT kiểm kê Cái"),

    ("004", "Cửa sổ chọn hàng chỉ có hàng còn tồn", "P0",
     "Kho K1: H1 có tồn, H2 tồn 0",
     "1. Tạo mới, chọn K1, bấm dấu cộng, tìm H1, H2",
     "—",
     "- Tìm thấy H1, không thấy H2\n"
     "- Nút dấu cộng bị mờ khi chưa chọn kho"),

    ("005", "Chọn lại hàng đã có", "P1",
     "Đã thêm H1",
     "1. Bấm dấu cộng, chọn H1 lần nữa",
     "—",
     "- Báo \"Hàng hóa đã được chọn\", không thêm dòng"),

    ("006", "Đổi ĐVT kiểm kê sang đơn vị lớn tự tách dòng", "P0",
     H1,
     "1. Thêm H1\n"
     "2. Ở lô L01 (30 Cái) chọn ĐVT kiểm kê \"Thùng\"",
     "ĐVT: Thùng (hệ số 12)",
     "- Dòng L01 thành 2 Thùng\n"
     "- Tự thêm dòng 6 Cái ngay dưới\n"
     "- Chọn lại \"Cái\" thì dòng phụ biến mất, L01 về 30 Cái"),

    ("007", "Lô chia hết cho đơn vị lớn không sinh dòng lẻ", "P2",
     "Lô L03 tồn 24 Cái, Thùng hệ số 12",
     "1. Chọn ĐVT kiểm kê Thùng cho L03",
     "—",
     "- Dòng thành 2 Thùng, không có dòng lẻ"),

    ("008", "Đổi kho xóa sạch danh sách hàng", "P1",
     "Đã chọn K1 và thêm H1",
     "1. Thêm K2 vào ô Kho",
     "—",
     "- Danh sách hàng bị xóa, không hỏi xác nhận\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu cảnh báo"),

    ("009", "Thêm Hội đồng kiểm kê", "P1",
     "Nhân viên NV-K có vai trò đầu tiên \"Thủ kho\"",
     "1. Mở tab Hội đồng kiểm kê, bấm dấu cộng, chọn NV-K",
     "—",
     "- Chức vụ tự chọn \"Thủ kho\", đổi được trong các vai trò của NV-K"),

    ("010", "Lưu nháp phiếu tự do", "P0",
     "NV-A công ty TPE; " + H1,
     "1. Tạo mới, chọn K1, thêm H1, thêm 1 thành viên, Ghi chú \"Kiểm đột xuất\"\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo thành công\", về danh sách lối vào menu\n"
     "- Dòng mới: Số phiếu TPE.KKK-xxxxx, Kho K1, Trạng thái Đang tạo, Người lập NV-A"),

    ("011", "Lưu & gửi chuyển phiếu sang Đang kiểm", "P0",
     "Như TC_04.010",
     "1. Tạo phiếu hợp lệ, bấm Lưu & gửi",
     "—",
     "- Báo \"Tạo thành công\"\n"
     "- Phiếu Đang kiểm, menu bánh răng có \"Cập nhật kết quả\""),

    ("012", "Lưu & gửi khi còn phiếu kho chưa xong", "P0",
     "Kho K1 có phiếu nhập kho PNK-1 chứa H1 chưa hoàn tất",
     "1. Tạo phiếu kho K1, hàng H1, bấm Lưu & gửi",
     "—",
     "- Mong đợi: bị chặn, báo còn phiếu kho chưa xử lý xong\n"
     "- Lưu ý: theo code hiện tại phiếu vẫn lưu được, Đang kiểm - ghi Failed"),

    ("013", "Lập phiếu từ " + KH, "P0",
     "KH-2 Đang kiểm: kho K1, hàng H1, 2 thành viên; TK1 có quyền \"Lập phiếu kiểm kê kho theo hàng hóa\"",
     "1. TK1 mở " + KH + ", bấm bánh răng > \"Lập phiếu kiểm kê theo hàng hóa\" ở KH-2\n"
     "2. Quan sát form",
     "—",
     "- Báo \"Lấy dữ liệu thành công\"\n"
     "- Ô Kế hoạch kiểm kê hiện số KH-2 (bấm mở kế hoạch ở thẻ mới)\n"
     "- Kho K1, hàng H1 (đủ vị trí, lô), Hội đồng 2 người điền sẵn\n"
     "- Ô Kho, Công ty thuê kho bị khóa; KHÔNG có dấu cộng / trừ hàng"),

    ("014", "Chọn kế hoạch qua cửa sổ Kế hoạch kiểm kê", "P1",
     "KH-2 Đang kiểm, KH-4 Đã lập phiếu kiểm kê",
     "1. Tạo mới, bấm nút tìm ở ô Kế hoạch kiểm kê\n"
     "2. Tìm KH-2, KH-4; chọn KH-2",
     "—",
     "- Cửa sổ có KH-2, không có KH-4\n"
     "- Chọn KH-2 thì form điền sẵn như TC_04.013"),

    ("015", "Lưu phiếu từ kế hoạch chuyển kế hoạch sang Đã lập phiếu kiểm kê", "P0",
     "Đang ở form lập từ KH-2",
     "1. Bấm Lưu\n"
     "2. Mở " + KH + ", tìm KH-2",
     "—",
     "- Phiếu mới Đang tạo, ô Kế hoạch kiểm kê ở Chi tiết là KH-2\n"
     "- KH-2 chuyển \"Đã lập phiếu kiểm kê\" (kể cả khi phiếu chỉ lưu nháp)"),

    ("016", "Bỏ chọn kế hoạch xóa dữ liệu form", "P2",
     "Đang ở form lập từ KH-2",
     "1. Bấm nút xóa (dấu x) ở ô Kế hoạch kiểm kê",
     "—",
     "- Ô Kế hoạch về \"-\", kho, hàng, hội đồng bị xóa trắng"),

    ("017", "Kế hoạch tổng kiểm kê trong cửa sổ chọn kế hoạch", "P1",
     "Kế hoạch tổng kiểm kê TKK-1 đã duyệt, hiệu lực từ 15/10 đến 30/10, hôm nay 21/10",
     "1. Tạo mới, mở cửa sổ Kế hoạch kiểm kê, tìm TKK-1",
     "—",
     "- Mong đợi: thấy TKK-1\n"
     "- Lưu ý: theo code hiện tại không thấy (chỉ hiện kế hoạch có từ ngày và đến ngày cùng là hôm nay) - "
     "ghi Failed"),

    ("018", "Phiếu từ tổng kiểm kê chặn hàng đã kiểm", "P1",
     "Đã có phiếu kiểm kê lập từ TKK-1 chứa H1",
     "1. Lập phiếu mới từ TKK-1 (qua bánh răng ở màn Kế hoạch tổng kiểm kê), thêm H1, bấm Lưu",
     "—",
     "- Báo \"Hàng hóa đã lập phiếu kiểm kê\"\n"
     "- Dòng H1 tô đỏ, không lưu"),

    ("019", "Sửa phiếu lập từ tổng kiểm kê", "P1",
     "Phiếu KK-9 Đang tạo lập từ TKK-1, chứa H3 (chưa có phiếu khác)",
     "1. Mở Sửa KK-9, đổi Ghi chú, bấm Lưu",
     "—",
     "- Mong đợi: \"Sửa thành công\"\n"
     "- Lưu ý: theo code hiện tại luôn báo \"Hàng hóa đã lập phiếu kiểm kê\" - ghi Failed"),

    ("020", "Mở màn Sửa lấy tồn hiện tại", "P0",
     "KK-1 Đang tạo lưu lúc L01 = 30; sau đó xuất 5, tồn còn 25",
     "1. Mở Sửa KK-1\n"
     "2. Bấm Lưu, mở Chi tiết",
     "—",
     "- Tiêu đề \"Kiểm kê hàng hóa: <Số phiếu>\"\n"
     "- Tồn theo lô L01 hiện 25 (tự làm mới số liệu)\n"
     "- Sau Lưu: \"Sửa thành công\", Chi tiết hiện 25"),

    ("021", "Màn Sửa đặt lại ĐVT kiểm kê", "P2",
     "KK-1 lưu với L01 tách 2 Thùng + 6 Cái",
     "1. Mở Sửa KK-1, xem lô L01",
     "—",
     "- Theo code hiện tại: L01 trở về 1 dòng theo ĐVT cơ bản\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ muốn giữ cách chia đã lưu"),

    ("022", "Nút làm mới số liệu", "P1",
     "Đang tạo phiếu, đã thêm H1 (L01 = 30); người khác xuất hết L02",
     "1. Bấm nút mũi tên tròn ở góc phải hàng tab",
     "—",
     "- L01 cập nhật theo tồn mới\n"
     "- Dòng L02 (về 0) bị bỏ; vị trí không còn lô nào bị bỏ"),

    ("023", "Chi tiết hiện đúng dữ liệu đã lưu", "P0",
     "KK-1 vừa lưu ở TC_04.010",
     "1. Mở Chi tiết KK-1",
     "—",
     "- Kho, Ghi chú, hàng, vị trí, lô, ĐVT kiểm kê, Hội đồng đúng như lúc lưu\n"
     "- Mọi ô khóa"),

    ("024", "Bấm Hủy trên màn Tạo mới", "P2",
     "—",
     "1. Tạo mới, chọn kho, thêm hàng, bấm Hủy",
     "—",
     "- Về danh sách, không có phiếu mới"),
]


SEC_V = [
    ("001", "Mở Cập nhật kết quả", "P0",
     "KK-2 Đang kiểm do NV-A lập, có H1 như mô tả",
     "1. NV-A bấm bánh răng > Cập nhật kết quả ở KK-2",
     "—",
     "- Có cột Thực kiểm (ô nhập), Chênh lệch, Ghi chú\n"
     "- Thực kiểm mặc định bằng Tồn theo lô, Chênh lệch 0\n"
     "- Có tab \"Hàng thừa khác\", ô \"File kết quả (PDF)\" với nút dấu cộng\n"
     "- Nút cuối trang: Gửi duyệt, Quay lại"),

    ("002", "Nhập Thực kiểm thấy Chênh lệch", "P0",
     "KK-2 như trên",
     "1. Nhập Thực kiểm L01 = 28, L02 = 11",
     "Thực kiểm: L01 = 28, L02 = 11",
     "- Chênh lệch L01 = -2, L02 = 1, hiện chữ đỏ"),

    ("003", "Gửi duyệt khi chưa có file kết quả", "P0",
     "KK-2 chưa từng gửi file",
     "1. Nhập Thực kiểm, KHÔNG thêm file\n"
     "2. Bấm Gửi duyệt",
     "—",
     "- Báo \"Thao tác thất bại!\"\n"
     "- Dưới ô File kết quả có lỗi (tiếng Anh) \"The attachments field is required.\""),

    ("004", "Gửi duyệt hợp lệ", "P0",
     "KK-2 như trên; người dùng nhóm Kế toán kho KT1",
     "1. Nhập Thực kiểm L01 = 28, L02 = 11, ghi chú dòng L01 \"vỡ 2\"\n"
     "2. Bấm dấu cộng ở File kết quả, chọn file PDF\n"
     "3. Bấm Gửi duyệt",
     "File: ket_qua.pdf",
     "- Báo \"Thao tác thành công\", về danh sách Phiếu của tôi\n"
     "- KK-2 Chờ KT duyệt; Chi tiết hiện Thực kiểm, Chênh lệch, Ghi chú đã nhập, có liên kết File 1\n"
     "- KT1 nhận thông báo \"Bạn có 1 phiếu kiểm kê hàng hóa cần duyệt\""),

    ("005", "Người có quyền Ban kiểm soát có nhận thông báo gửi duyệt không", "P1",
     "BKS có quyền Ban kiểm soát, không thuộc nhóm Kế toán kho",
     "1. NV-A Gửi duyệt KK-2\n"
     "2. Đăng nhập BKS xem thông báo",
     "—",
     "- Mong đợi: BKS nhận thông báo\n"
     "- Lưu ý: theo code hiện tại thông báo gửi cho nhóm Kế toán kho, BKS có thể không nhận - ghi lại thực tế"),

    ("006", "Thực kiểm để trống được hiểu là 0", "P1",
     "KK-2 Đang kiểm, L02 tồn 10",
     "1. Xóa trống ô Thực kiểm L02\n"
     "2. Gửi duyệt (đủ file), mở Chi tiết",
     "—",
     "- Theo code hiện tại: Thực kiểm L02 = 0, Chênh lệch = -10\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu bắt buộc nhập"),

    ("007", "Thực kiểm có dấu phẩy", "P1",
     "Hàng Kg, lô tồn 3",
     "1. Nhập Thực kiểm \"2,5\"",
     "Thực kiểm: 2,5",
     "- Mong đợi: hiểu là 2,5 Kg\n"
     "- Lưu ý: theo code hiện tại hiểu là 25 (dấu phẩy là phân cách hàng nghìn) - ghi Failed"),

    ("008", "Thực kiểm số lớn hiện phân cách hàng nghìn", "P2",
     "Lô tồn 1000",
     "1. Nhập Thực kiểm 1200",
     "—",
     "- Ô hiện \"1,200\", Chênh lệch 200"),

    ("009", "Thêm hàng thừa khác là hàng có sẵn", "P0",
     "Hàng H9 có trong danh mục, không có trong phiếu",
     "1. Mở tab Hàng thừa khác, bấm dấu cộng\n"
     "2. Bấm nút tìm ở ô Tên hàng, chọn H9\n"
     "3. Nhập Thực kiểm 3 ở vị trí P1, Gửi duyệt",
     "Hàng: H9",
     "- Dòng hiện tên, model, mã, ĐVT của H9\n"
     "- Chi tiết sau gửi: tab Hàng thừa khác có H9, P1, 3"),

    ("010", "Thêm hàng thừa khác là hàng mới chưa có mã", "P1",
     "—",
     "1. Tab Hàng thừa khác, bấm dấu cộng\n"
     "2. Gõ tên \"Thùng carton lạ\", chọn ĐVT Cái, chọn Vị trí P1, Thực kiểm 5\n"
     "3. Bấm dấu cộng cạnh Vị trí, thêm P2 = 2\n"
     "4. Gửi duyệt",
     "Tên: Thùng carton lạ",
     "- Lưu thành công, Chi tiết hiện 1 hàng với 2 vị trí P1 = 5, P2 = 2\n"
     "- Ô Vị trí chỉ liệt kê vị trí của kho đã chọn"),

    ("011", "Hàng thừa khác thiếu tên / ĐVT / vị trí", "P1",
     "—",
     "1. Thêm 1 dòng Hàng thừa khác để trống tên, ĐVT, vị trí\n"
     "2. Gửi duyệt",
     "—",
     "- Báo \"Thao tác thất bại!\"\n"
     "- Lỗi tiếng Anh dưới ô tên, ĐVT, vị trí"),

    ("012", "Cập nhật lại kết quả sau khi Không duyệt", "P0",
     "KK-7 Không duyệt (đã có File 1), do NV-A lập",
     "1. NV-A bấm Cập nhật kết quả ở KK-7\n"
     "2. Sửa Thực kiểm L01 = 29, bấm Gửi duyệt (không thêm file)",
     "—",
     "- Ô Thực kiểm hiện số đã gửi lần trước\n"
     "- Không có nút thêm file, File 1 vẫn hiện\n"
     "- Gửi được, KK-7 về Chờ KT duyệt, Chi tiết hiện L01 = 29"),

    ("013", "File kết quả sai định dạng", "P2",
     "—",
     "1. Gọi thẳng chức năng Gửi duyệt kèm file Word",
     "File: ket_qua.docx",
     "- Báo \"Thao tác thất bại!\", lỗi định dạng file\n"
     "- Giao diện chỉ cho chọn PDF; ảnh png, jpg vẫn được hệ thống chấp nhận khi gọi thẳng"),
]
