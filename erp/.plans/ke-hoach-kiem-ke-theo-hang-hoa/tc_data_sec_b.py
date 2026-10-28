# -*- coding: utf-8 -*-
"""Section IV, V - tao / sua / chi tiet; gui kiem & lap phieu kiem ke."""
from tc_data_role import P1

SEC_IV = [
    ("001", "Ô Kho chỉ liệt kê kho đang hoạt động của công ty mình", "P0",
     "NV-A thuộc công ty 1; công ty 1 có kho K1, K2 (hoạt động), K9 (ngừng hoạt động); công ty 3 có kho K5",
     "1. Bấm Tạo mới\n"
     "2. Mở ô Kho",
     "—",
     "- Ô Kho liệt kê K1, K2 dạng \"mã - tên\"\n"
     "- Không có K9, K5\n"
     "- Chọn được nhiều kho cùng lúc"),

    ("002", "Nút thêm hàng bị khóa khi chưa chọn kho", "P0",
     "—",
     "1. Bấm Tạo mới\n"
     "2. Quan sát nút dấu cộng ở bảng Hàng hóa khi ô Kho còn trống",
     "—",
     "- Nút dấu cộng bị mờ, bấm không có tác dụng"),

    ("003", "Cửa sổ chọn hàng chỉ có hàng còn tồn kế toán", "P0",
     "Kho K1: hàng H1 tồn kế toán 10, hàng H2 tồn kế toán 0, hàng H3 không có ở K1",
     "1. Bấm Tạo mới, chọn Kho K1\n"
     "2. Bấm nút dấu cộng ở bảng Hàng hóa\n"
     "3. Tìm H1, H2, H3",
     "Kho: K1",
     "- Tìm thấy H1\n"
     "- Không tìm thấy H2, H3"),

    ("004", "Thêm hàng lấy tồn theo từng kho kế toán", "P0",
     "Kho K1 có 2 kho kế toán: KT1 (công ty 1) tồn H1 = 6, KT2 (công ty thuê) tồn H1 = 4",
     "1. Bấm Tạo mới, chọn Kho K1\n"
     "2. Bấm dấu cộng, chọn hàng H1",
     "Hàng: H1",
     "- Báo \"Thêm thành công\"\n"
     "- Dòng H1 hiện Tên hàng, Model, Mã hàng, ĐVT cơ bản\n"
     "- Bên dưới có 2 dòng: \"KT1 mã - tên\" SL 6 và \"KT2 mã - tên\" SL 4\n"
     "- Tổng SL = 10"),

    ("005", "Kho kế toán có tồn bằng 0 không hiện", "P1",
     "Kho K1: KT1 tồn H1 = 6, KT2 tồn H1 = 0",
     "1. Tạo mới, chọn K1, thêm H1",
     "—",
     "- Chỉ có dòng KT1 SL 6, Tổng SL = 6"),

    ("006", "Chọn lại hàng đã có trong danh sách", "P0",
     "Đã thêm H1 vào kế hoạch",
     "1. Bấm dấu cộng, chọn H1 lần nữa",
     "—",
     "- Báo \"Hàng hóa đã được chọn\"\n"
     "- Danh sách vẫn chỉ có 1 dòng H1"),

    ("007", "Chọn nhiều kho thì Tổng SL gồm tồn của mọi kho", "P0",
     "Hàng H1: kho K1 tồn kế toán 6 (kho kế toán KT1), kho K2 tồn kế toán 5 (kho kế toán KT3)",
     "1. Tạo mới, chọn Kho K1 và K2\n"
     "2. Thêm H1",
     "Kho: K1, K2",
     "- Mong đợi: hiện cả KT1 (6) và KT3 (5), Tổng SL = 11\n"
     "- Lưu ý: theo code hiện tại chỉ hiện kho kế toán của MỘT kho, Tổng SL = 6 hoặc 5 - ghi Failed"),

    ("008", "Bớt hàng khỏi danh sách", "P1",
     "Đã thêm H1, H2",
     "1. Bấm dấu trừ ở dòng H1",
     "—",
     "- H1 biến mất, H2 lên STT 1\n"
     "- Bớt hết thì bảng hiện \"Chưa chọn hàng hóa\""),

    ("009", "Đổi kho làm xóa sạch danh sách hàng", "P0",
     "Đã chọn Kho K1 và thêm H1, H2",
     "1. Thêm Kho K2 vào ô Kho (giữ K1)\n"
     "2. Quan sát bảng Hàng hóa",
     "—",
     "- Theo code hiện tại: danh sách hàng bị xóa hết, KHÔNG hỏi xác nhận\n"
     "- Phải chọn lại H1, H2\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu cảnh báo trước khi xóa"),

    ("010", "Thêm thành viên Hội đồng kiểm kê", "P0",
     "Nhân viên NV-K có 2 vai trò: \"Kế toán kho\" (đầu tiên), \"Thủ kho\"",
     "1. Tạo mới, mở tab Hội đồng kiểm kê\n"
     "2. Bấm dấu cộng\n"
     "3. Chọn thành viên NV-K\n"
     "4. Mở ô Chức vụ",
     "Thành viên: NV-K",
     "- Ô Thành viên hiện dạng \"Họ tên - mã phòng ban\"\n"
     "- Chức vụ tự chọn \"Kế toán kho\"\n"
     "- Ô Chức vụ chỉ có 2 vai trò của NV-K, đổi sang Thủ kho được"),

    ("011", "Danh sách thành viên gồm nhân viên mọi công ty", "P2",
     "Nhân viên NV-Z thuộc công ty 3, đang làm việc; nhân viên NV-Q đã nghỉ việc",
     "1. Tạo mới, mở tab Hội đồng kiểm kê, thêm dòng\n"
     "2. Tìm NV-Z và NV-Q trong ô Thành viên",
     "—",
     "- Tìm thấy NV-Z (khác công ty)\n"
     "- Không tìm thấy NV-Q"),

    ("012", "Bớt thành viên", "P2",
     "Hội đồng có 2 thành viên",
     "1. Bấm dấu trừ ở dòng 1",
     "—",
     "- Còn 1 thành viên, STT đánh lại từ 1"),

    ("013", "Lưu nháp kế hoạch hợp lệ", "P0",
     "Tài khoản NV-A công ty mã TPE",
     "1. Tạo mới, chọn Kho K1, Ghi chú \"Kiểm quý 4\"\n"
     "2. Thêm H1, H2\n"
     "3. Thêm 2 thành viên\n"
     "4. Bấm Lưu",
     "Kho: K1\n"
     "Hàng: H1, H2\n"
     "Ghi chú: Kiểm quý 4",
     "- Báo \"Tạo thành công\", chuyển về danh sách lối vào menu\n"
     "- Dòng mới: Số phiếu TPE.KHKKHH-xxxxx, Ngày kiểm kê hôm nay, Kho K1, Trạng thái Đang tạo, Người "
     "lập NV-A\n"
     "- Không gửi thông báo cho ai"),

    ("014", "Số phiếu tăng liên tiếp", "P1",
     "Kế hoạch gần nhất là TPE.KHKKHH-00125",
     "1. Tạo và Lưu 1 kế hoạch mới",
     "—",
     "- Số phiếu mới có phần số lớn hơn số trước, đủ 5 chữ số, tiền tố là mã công ty người lập kèm dấu "
     "chấm"),

    ("015", "Xem chi tiết hiển thị đúng dữ liệu đã lưu", "P0",
     "Kế hoạch KH-1 vừa lưu ở TC_04.013",
     "1. Bấm Số phiếu KH-1\n"
     "2. Soát từng ô, từng tab",
     "—",
     "- Kho K1, Ghi chú \"Kiểm quý 4\", Ngày kiểm kê đúng ngày lập\n"
     "- Tab Hàng hóa: H1, H2 với kho kế toán và SL như lúc lưu\n"
     "- Tab Hội đồng kiểm kê: 2 thành viên và chức vụ như lúc lưu\n"
     "- Mọi ô bị khóa"),

    ("016", "Chi tiết giữ số tồn lúc lưu", "P0",
     "KH-1 lưu lúc H1 tồn KT1 = 6; sau đó xuất kho 2 cái H1, tồn còn 4",
     "1. Mở Chi tiết KH-1",
     "—",
     "- SL tồn kho kế toán của H1 vẫn là 6, Tổng SL vẫn 6"),

    ("017", "Nút làm mới số liệu trên màn nhập", "P2",
     "Đang tạo kế hoạch, đã thêm H1 (tồn 6); người khác vừa xuất 2 cái H1",
     "1. Bấm nút biểu tượng mũi tên tròn ở góc phải hàng tab",
     "—",
     "- Mong đợi: SL tồn cập nhật thành 4\n"
     "- Lưu ý: theo code hiện tại bấm không có tác dụng gì - ghi Failed nếu nghiệp vụ cần nút này"),

    ("018", "Mở màn Sửa kế hoạch nháp", "P0",
     "KH-1 Đang tạo do NV-A lập",
     "1. Đăng nhập NV-A, bấm bánh răng > Sửa ở KH-1",
     "—",
     "- Tiêu đề trang \"Kế hoạch kiểm kê hàng hóa: <Số phiếu KH-1>\"\n"
     "- Kho, Ghi chú, hàng hóa, thành viên điền sẵn như đã lưu\n"
     "- Nút cuối trang: Lưu, Lưu & gửi, Hủy"),

    ("019", "Màn Sửa lấy lại tồn hiện tại", "P0",
     "KH-1 lưu lúc H1 tồn KT1 = 6; sau đó tồn còn 4",
     "1. Mở Sửa KH-1, đọc SL của H1\n"
     "2. Bấm Lưu\n"
     "3. Mở Chi tiết KH-1",
     "—",
     "- Bước 1: SL tồn H1 = 4\n"
     "- Bước 3: SL tồn H1 = 4 (số cũ bị ghi đè)"),

    ("020", "Sửa ghi chú, thêm hàng rồi Lưu", "P0",
     "KH-1 Đang tạo, có H1, H2",
     "1. Mở Sửa KH-1\n"
     "2. Đổi Ghi chú thành \"Kiểm bổ sung\", bớt H2, thêm H3\n"
     "3. Bấm Lưu",
     "Ghi chú: Kiểm bổ sung",
     "- Báo \"Sửa thành công\", về danh sách\n"
     "- Chi tiết KH-1: Ghi chú mới, hàng H1, H3; Số phiếu không đổi\n"
     "- Trạng thái vẫn Đang tạo"),

    ("021", "Màn Sửa khi một hàng đã hết tồn kế toán", "P1",
     "KH-1 Đang tạo có H1, H2; sau khi lưu, H2 bị xuất hết, tồn kế toán = 0",
     "1. Mở Sửa KH-1\n"
     "2. Quan sát bảng Hàng hóa\n"
     "3. Bấm Lưu",
     "—",
     "- Mong đợi: H2 được bỏ khỏi danh sách hoặc có cảnh báo rõ ràng\n"
     "- Lưu ý: theo code hiện tại có thể hiện 1 dòng trống thông tin và Lưu báo lỗi - ghi lại thực tế"),

    ("022", "Bấm Hủy trên màn Tạo mới không lưu gì", "P1",
     "—",
     "1. Tạo mới, chọn kho, thêm hàng\n"
     "2. Bấm Hủy",
     "—",
     "- Về danh sách lối vào menu\n"
     "- Không có kế hoạch mới"),

    ("023", "Nút Lưu bị khóa khi đang gửi", "P2",
     "Mạng chậm",
     "1. Tạo kế hoạch hợp lệ, bấm Lưu & kiểm\n"
     "2. Bấm tiếp Lưu & kiểm khi biểu tượng xoay còn hiện",
     "—",
     "- Cả hai nút Lưu và Lưu & kiểm bị mờ, chỉ tạo 1 kế hoạch"),

    ("024", "Màn Chi tiết hiện Hội đồng kiểm kê", "P1",
     "KH-1 có 2 thành viên",
     "1. Mở Chi tiết KH-1, bấm tab Hội đồng kiểm kê",
     "—",
     "- Hiện 2 dòng Thành viên, Chức vụ; ô khóa; không có dấu cộng / trừ"),
]


SEC_V = [
    ("001", "Lưu & kiểm chuyển kế hoạch sang Đang kiểm", "P0",
     "Không có phiếu nhập / xuất kho nào chưa xong chứa H1, H2 ở kho K1\n"
     "TK1, TK2 có quyền \"Lập phiếu kiểm kê kho theo hàng hóa\"",
     "1. Tạo kế hoạch kho K1, hàng H1, H2, 1 thành viên\n"
     "2. Bấm Lưu & kiểm",
     "—",
     "- Báo \"Tạo thành công\"\n"
     "- Kế hoạch ở trạng thái Đang kiểm\n"
     "- TK1, TK2 nhận thông báo \"Bạn có 1 phiếu kế hoạch kiểm kê kho cần duyệt\""),

    ("002", "Lưu & gửi từ màn Sửa", "P0",
     "KH-1 Đang tạo do NV-A lập, không có phiếu kho chưa xong",
     "1. Mở Sửa KH-1, bấm Lưu & gửi",
     "—",
     "- Báo \"Sửa thành công\"\n"
     "- KH-1 chuyển Đang kiểm, menu bánh răng không còn Sửa / Xóa\n"
     "- Người có quyền Lập phiếu nhận thông báo"),

    ("003", "Bấm vào thông báo gửi kiểm", "P1",
     "TK1 vừa nhận thông báo của kế hoạch KH-7",
     "1. Đăng nhập TK1, bấm vào thông báo",
     "—",
     "- Mong đợi: mở kế hoạch KH-7\n"
     "- Lưu ý: theo code hiện tại mở " + P1 + " có cùng số thứ tự với KH-7 (hoặc trang không tìm thấy) - "
     "ghi Failed"),

    ("004", "Thông báo gửi cho cả người có quyền ở công ty khác", "P2",
     "TK5 thuộc công ty 3 có quyền \"Lập phiếu kiểm kê kho theo hàng hóa\"; kế hoạch thuộc công ty 1",
     "1. NV-A công ty 1 Lưu & kiểm một kế hoạch\n"
     "2. Đăng nhập TK5 xem thông báo",
     "—",
     "- Theo code hiện tại: TK5 CŨNG nhận thông báo\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ chỉ báo cho người cùng công ty / cùng kho"),

    ("005", "Lưu & kiểm bị chặn khi còn phiếu nhập kho chưa xong", "P0",
     "Kho K1 có phiếu nhập kho PNK-1 chứa hàng H1 chưa hoàn tất",
     "1. Tạo kế hoạch kho K1, chỉ hàng H1\n"
     "2. Bấm Lưu & kiểm",
     "Hàng: H1",
     "- Hiện cửa sổ \"Cảnh báo phiếu chưa xử lí xong !\"\n"
     "- Có dòng \"Phiếu nhập kho\" kèm số PNK-1, bấm số mở phiếu ở thẻ mới\n"
     "- Kế hoạch KHÔNG được lưu"),

    ("006", "Lưu & kiểm bị chặn khi còn phiếu xuất kho chưa xong", "P0",
     "Kho K1 có phiếu xuất kho PXK-1 chứa H1 chưa hoàn tất",
     "1. Tạo kế hoạch kho K1, hàng H1, bấm Lưu & kiểm",
     "—",
     "- Cửa sổ cảnh báo có dòng \"Còn xuất kho\" kèm số PXK-1\n"
     "- Bấm Đóng thì quay lại form, dữ liệu đã nhập còn nguyên"),

    ("007", "Phiếu kho chưa xong không chặn Lưu nháp", "P1",
     "Như TC_05.005",
     "1. Tạo kế hoạch kho K1, hàng H1, bấm Lưu",
     "—",
     "- Báo \"Tạo thành công\", kế hoạch Đang tạo"),

    ("008", "Cảnh báo phiếu chưa xong chỉ xét hàng cuối danh sách", "P0",
     "Kho K1 có phiếu nhập kho PNK-1 chưa xong chứa H1; H2 không vướng phiếu nào",
     "1. Tạo kế hoạch kho K1, thêm H1 trước rồi H2\n"
     "2. Bấm Lưu & kiểm",
     "Hàng: H1, H2 (theo thứ tự)",
     "- Mong đợi: bị chặn vì H1 vướng PNK-1\n"
     "- Lưu ý: theo code hiện tại kế hoạch LƯU ĐƯỢC, Đang kiểm (chỉ xét hàng cuối là H2) - ghi Failed"),

    ("009", "Lập phiếu kiểm kê từ kế hoạch", "P0",
     "KH-2 Đang kiểm: kho K1, hàng H1, H2, 2 thành viên\n"
     "TK1 có quyền \"Lập phiếu kiểm kê kho theo hàng hóa\"",
     "1. Đăng nhập TK1, bấm bánh răng > \"Lập phiếu kiểm kê theo hàng hóa\" ở KH-2\n"
     "2. Quan sát màn mở ra",
     "—",
     "- Mở màn " + P1 + ", báo \"Lấy dữ liệu thành công\"\n"
     "- Ô Kế hoạch kiểm kê hiện số phiếu KH-2\n"
     "- Kho K1, hàng H1, H2 và Hội đồng kiểm kê được điền sẵn theo kế hoạch"),

    ("010", "Lưu phiếu kiểm kê chuyển kế hoạch sang Đã lập phiếu kiểm kê", "P0",
     "Đang ở màn lập phiếu từ KH-2 (TC_05.009)",
     "1. Nhập đủ dữ liệu bắt buộc, bấm Lưu (nháp)\n"
     "2. Quay lại danh sách kế hoạch, tìm KH-2",
     "—",
     "- KH-2 chuyển \"Đã lập phiếu kiểm kê\" (nhãn xanh), kể cả khi phiếu kiểm kê chỉ lưu nháp\n"
     "- Menu bánh răng KH-2 không còn \"Lập phiếu kiểm kê theo hàng hóa\""),

    ("011", "Kế hoạch chọn được trong cửa sổ Kế hoạch kiểm kê của phiếu kiểm kê", "P1",
     "KH-2 Đang kiểm, KH-4 Đã lập phiếu kiểm kê",
     "1. Mở màn " + P1 + " > Tạo mới\n"
     "2. Bấm chọn Kế hoạch kiểm kê, tìm KH-2 và KH-4\n"
     "3. Chọn KH-2",
     "—",
     "- Cửa sổ có KH-2, không có KH-4\n"
     "- Chọn KH-2 thì dữ liệu kế hoạch được điền sẵn như TC_05.009"),

    ("012", "Xóa phiếu kiểm kê không trả kế hoạch về Đang kiểm", "P1",
     "KH-2 đã chuyển Đã lập phiếu kiểm kê nhờ phiếu kiểm kê nháp PKK-1",
     "1. Xóa PKK-1 ở màn " + P1 + "\n"
     "2. Quay lại danh sách kế hoạch, xem KH-2",
     "—",
     "- Theo code hiện tại: KH-2 vẫn Đã lập phiếu kiểm kê, không lập lại phiếu được\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu kế hoạch quay về Đang kiểm"),

    ("013", "Phiếu kiểm kê hoàn thành nhưng kế hoạch không Hoàn thành", "P1",
     "Phiếu kiểm kê PKK-2 lập từ KH-2 đã được duyệt, trạng thái Hoàn thành",
     "1. Mở danh sách kế hoạch, xem KH-2",
     "—",
     "- Mong đợi: KH-2 Hoàn thành\n"
     "- Lưu ý: theo code hiện tại KH-2 vẫn \"Đã lập phiếu kiểm kê\" - ghi Failed"),
]
