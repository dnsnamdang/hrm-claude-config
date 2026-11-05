# -*- coding: utf-8 -*-
"""Section V, VI, VII - tinh tien, luu / gui duyet / sua, khong duyet va chuyen sang hach toan."""
from tc_data_role import HD, KD1, KT1

SEC_V = [
    ("001", "Tổng tiền khi chọn hết dịch vụ đi kèm", "P0",
     HD,
     "1. KD-1 lập phiếu Dịch vụ từ HD-01\n"
     "2. Tích ô chọn tất cả ở tab Dịch vụ đi kèm",
     "—",
     "- Tổng trước thuế 3.000.000\n"
     "- VAT(10%) 300.000\n"
     "- Tổng sau thuế 3.300.000"),

    ("002", "Tổng tiền khi chọn 1 dòng", "P0",
     HD,
     "1. KD-1 lập phiếu Dịch vụ từ HD-01, chỉ tích DV2",
     "—",
     "- Tổng trước thuế 1.000.000, VAT 100.000, Tổng sau thuế 1.100.000\n"
     "- Dòng DV1 hiện mờ (không chọn)"),

    ("003", "Bỏ chọn một dòng thì ô chọn tất cả tự bỏ", "P2",
     "Đang chọn tất cả DV1, DV2",
     "1. Bỏ tích DV1",
     "—",
     "- Ô chọn tất cả bỏ tích\n"
     "- Tổng trước thuế còn 1.000.000"),

    ("004", "Tổng tiền phiếu Chi phí khác", "P0",
     HD,
     "1. KD-1 lập phiếu Chi phí khác từ HD-01, tích CP1",
     "—",
     "- Tổng trước thuế 500.000, VAT(10%) 50.000, Tổng sau thuế 550.000"),

    ("005", "Tổng thanh toán lưu đúng Tổng sau thuế", "P0",
     HD,
     "1. KD-1 lập phiếu Dịch vụ, tích DV1, DV2, bấm \"Lưu & Gửi duyệt\"\n"
     "2. Xem cột Tổng thanh toán ở danh sách",
     "—",
     "- Tổng thanh toán 3,300,000"),

    ("006", "VAT khác nhau giữa các dòng chi phí", "P1",
     "HD-06 có CP6 1.000.000 VAT 10% (dòng đầu) và CP7 1.000.000 VAT 8%",
     "1. KD-1 lập phiếu Chi phí khác từ HD-06, tích CP6, CP7",
     "—",
     "- Mong đợi: VAT = 100.000 + 80.000 = 180.000, Tổng sau thuế 2.180.000\n"
     "- Lưu ý: theo code hiện tại VAT lấy 10% của dòng đầu cho cả 2 dòng (200.000) - ghi Failed nếu nghiệp vụ "
     "yêu cầu tính theo từng dòng"),

    ("007", "Chi phí vận chuyển có vượt trội và giảm giá", "P1",
     "HD-07: cước 300.000, vượt trội 50.000, giảm 30.000, VAT 8%",
     "1. KD-1 lập phiếu Chi phí vận chuyển từ HD-07",
     "—",
     "- Dòng Chi phí vận chuyển: Giá niêm yết 300.000, Doanh số vượt trội 50.000, Giảm giá 30.000, Giá trị "
     "sau giảm giá 320.000\n"
     "- VAT 25.600, Tổng sau thuế 345.600"),

    ("008", "Vận chuyển sau phụ lục giảm cước", "P1",
     "HD-08 cước 300.000; phụ lục giảm đã duyệt giảm cước 100.000",
     "1. KD-1 lập phiếu Chi phí vận chuyển từ HD-08",
     "—",
     "- Giá niêm yết 200.000 (đã trừ phần giảm)"),
]

SEC_VI = [
    ("001", "Lưu phiếu Đang tạo", "P0",
     HD,
     "1. KD-1 lập phiếu Chi phí khác từ HD-01, tích CP1, nhập Ghi chú \"Đợt 1\"\n"
     "2. Bấm Lưu",
     "—",
     "- Thông báo \"Thao tác thành công\", về danh sách\n"
     "- Phiếu mới mã TPE.YCHTDV.xxxxx, Trạng thái Đang tạo, Tổng thanh toán 550,000"),

    ("002", "Phiếu Đang tạo không khóa dòng chi phí", "P0",
     "YC-2 Đang tạo của HD-01 gồm CP1",
     "1. KD-1 lập thêm phiếu Chi phí khác từ HD-01",
     "—",
     "- CP1 không tô đỏ, chọn được"),

    ("003", "Lưu & Gửi duyệt", "P0",
     HD + "\n" + KT1,
     "1. KD-1 lập phiếu Chi phí khác, tích CP1, bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- Thông báo thành công, phiếu Chờ duyệt\n"
     "- KT-1 nhận thông báo \"Bạn có một phiếu yêu cầu hạch toán dịch vụ cần duyệt từ <tên KD-1>\"\n"
     "- Ô trang chủ của KT-1 tăng 1"),

    ("004", "Gửi duyệt khóa dòng đã yêu cầu", "P0",
     "YC-1 vừa gửi duyệt gồm CP1",
     "1. KD-1 lập phiếu Chi phí khác mới từ HD-01, tích CP1\n"
     "2. Bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- CP1 tô đỏ\n"
     "- Thông báo \"Không thể yêu cầu hạch toán cho dịch vụ sửa chữa đã hoàn thành\", không tạo phiếu"),

    ("005", "Gửi duyệt phiếu Dịch vụ khóa từng dòng đã chọn", "P1",
     "KD-1 gửi duyệt phiếu Dịch vụ chỉ gồm DV1",
     "1. Lập phiếu Dịch vụ mới từ HD-01",
     "—",
     "- DV1 tô đỏ; DV2 bình thường, gửi duyệt được"),

    ("006", "Mở Sửa phiếu Đang tạo", "P0",
     "YC-2 Đang tạo kiểu Chi phí khác gồm CP1, Ghi chú \"Đợt 1\"",
     "1. KD-1 bấm Sửa ở YC-2",
     "—",
     "- Tiêu đề \"Sửa yêu cầu hạch toán dịch vụ\"\n"
     "- Kiểu hạch toán khóa; CP1 đã được tích; Ghi chú \"Đợt 1\""),

    ("007", "Sửa bỏ bớt dòng rồi lưu", "P0",
     "YC-12 Đang tạo kiểu Dịch vụ gồm DV1, DV2",
     "1. KD-1 mở Sửa YC-12, bỏ tích DV1\n"
     "2. Bấm Lưu",
     "—",
     "- Lưu thành công\n"
     "- Chi tiết YC-12 chỉ còn DV2, Tổng thanh toán 1,100,000"),

    ("008", "Sửa rồi Gửi duyệt", "P0",
     "YC-2 Đang tạo gồm CP1",
     "1. KD-1 mở Sửa YC-2, bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- YC-2 chuyển Chờ duyệt, CP1 bị khóa ở phiếu khác\n"
     "- KT-1 nhận thông báo cần duyệt\n"
     "- Lưu ý: theo code hiện tại thông báo gửi tới người có quyền \"Duyệt yêu cầu làm dịch vụ\", KT-1 chỉ có "
     "quyền Hạch toán sẽ không nhận - ghi Failed"),

    ("009", "Sửa giữ nguyên VAT và Tổng thanh toán", "P0",
     "YC-2 Đang tạo kiểu Chi phí khác gồm CP1, Tổng thanh toán 550.000",
     "1. KD-1 mở Sửa YC-2, không đổi gì, bấm Lưu",
     "—",
     "- Mong đợi: còn dòng VAT(10%) 50.000, Tổng thanh toán vẫn 550,000\n"
     "- Lưu ý: theo code hiện tại màn Sửa mất dòng VAT, Tổng sau thuế trống hoặc chỉ còn 500.000, lưu có "
     "thể báo lỗi - ghi Failed"),

    ("010", "Màn Sửa chỉ hiện dòng của hợp đồng như lúc lập", "P1",
     "HD-01 có CP1, dòng giảm CP2, dòng Chi phí vận chuyển; YC-2 Đang tạo kiểu Chi phí khác gồm CP1",
     "1. KD-1 mở Sửa YC-2",
     "—",
     "- Mong đợi: tab Chi phí chỉ có CP1\n"
     "- Lưu ý: nếu có thêm dòng giảm CP2 hoặc dòng Chi phí vận chuyển thì ghi Failed"),

    ("011", "Sửa phiếu Chi phí vận chuyển", "P0",
     "YC-13 Đang tạo kiểu Chi phí vận chuyển của HD-01",
     "1. KD-1 mở Sửa YC-13\n"
     "2. Bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- Mong đợi: có dòng Chi phí vận chuyển đã tích, gửi duyệt thành công\n"
     "- Lưu ý: theo code hiện tại bảng Chi phí trống, gửi báo \"Bắt buộc chọn 1 chi phí\" - ghi Failed"),

    ("012", "Sửa phiếu Không duyệt và gửi lại", "P0",
     "YC-10 Không duyệt kiểu Chi phí khác gồm CP1, ghi chú duyệt \"Sai chi phí\"",
     "1. KD-1 mở Sửa YC-10\n"
     "2. Bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- Màn Sửa có khung \"Ghi chú duyệt\" hiện \"Sai chi phí\" (khóa)\n"
     "- YC-10 chuyển Chờ duyệt, CP1 bị khóa lại"),

    ("013", "Đổi hợp đồng ở màn Sửa", "P1",
     "YC-2 Đang tạo kiểu Chi phí khác của HD-01; HD-06 của KD-1 có CP6",
     "1. KD-1 mở Sửa YC-2, chọn lại hợp đồng HD-06, tích CP6\n"
     "2. Bấm Lưu, mở chi tiết YC-2",
     "—",
     "- Mong đợi: phiếu gắn HD-06 với CP6, hoặc không cho đổi hợp đồng\n"
     "- Lưu ý: theo code hiện tại phiếu vẫn ghi HD-01 nhưng chi phí là CP6 - ghi Failed"),

    ("014", "Đường dẫn Sửa phiếu Chờ duyệt", "P1",
     "YC-1 Chờ duyệt do KD-1 lập",
     "1. KD-1 dán đường dẫn Sửa YC-1",
     "—",
     "- Trang không tìm thấy"),
]

SEC_VII = [
    ("001", "Chi tiết phiếu Chờ duyệt với kế toán", "P0",
     KT1 + ", có quyền xem của tổng công ty; YC-1 Chờ duyệt",
     "1. KT-1 mở chi tiết YC-1",
     "—",
     "- Cuối trang có Không duyệt, Hạch toán dịch vụ, Quay lại"),

    ("002", "Không duyệt phải có ghi chú", "P0",
     "KT-1 đang ở chi tiết YC-1",
     "1. Bấm Không duyệt, để trống ô Ghi chú duyệt\n"
     "2. Bấm Xác nhận",
     "—",
     "- Báo \"Bắt buộc nhập\" dưới ô ghi chú\n"
     "- YC-1 vẫn Chờ duyệt"),

    ("003", "Không duyệt thành công", "P0",
     "YC-1 Chờ duyệt gồm CP1 của HD-01",
     "1. KT-1 bấm Không duyệt, nhập \"Sai chi phí\", Xác nhận",
     "—",
     "- Thông báo thành công, về danh sách\n"
     "- YC-1 Không duyệt, Người duyệt KT-1, Ngày duyệt là lúc bấm\n"
     "- KD-1 nhận thông báo \"Phiếu yêu cầu hạch toán làm dịch vụ của bạn không được duyệt\""),

    ("004", "Không duyệt mở lại dòng cho hợp đồng", "P0",
     "YC-1 vừa bị Không duyệt, gồm CP1",
     "1. KD-1 lập phiếu Chi phí khác mới từ HD-01",
     "—",
     "- CP1 không tô đỏ, gửi duyệt được"),

    ("005", "Bấm Hạch toán dịch vụ mở phiếu hạch toán", "P0",
     "YC-1 Chờ duyệt kiểu Chi phí khác gồm CP1",
     "1. KT-1 bấm \"Hạch toán dịch vụ\" ở chi tiết YC-1",
     "—",
     "- Mở form Phiếu hạch toán dịch vụ HĐBH\n"
     "- Lấy sẵn YC-1, HD-01, dòng CP1, Tổng thanh toán 550.000"),

    ("006", "Duyệt phiếu hạch toán chuyển yêu cầu sang Đã hạch toán", "P0",
     "KT-1 đang lập phiếu hạch toán từ YC-1",
     "1. KT-1 lưu và duyệt phiếu hạch toán\n"
     "2. Mở lại danh sách yêu cầu",
     "—",
     "- YC-1 Đã hạch toán, Người duyệt KT-1, Ngày duyệt là lúc duyệt phiếu hạch toán\n"
     "- KD-1 nhận thông báo \"Phiếu yêu cầu hạch toán làm dịch vụ của bạn đã được duyệt\""),

    ("007", "Phiếu hạch toán mới lưu nháp thì yêu cầu vẫn Chờ duyệt", "P1",
     "KT-1 lập phiếu hạch toán từ YC-1, chỉ bấm Lưu (chưa duyệt)",
     "1. Mở chi tiết YC-1",
     "—",
     "- YC-1 vẫn Chờ duyệt\n"
     "- Mong đợi: không lập được phiếu hạch toán thứ hai cho YC-1\n"
     "- Lưu ý: nếu nút Hạch toán dịch vụ vẫn cho lập thêm phiếu thì ghi Failed"),

    ("008", "Phiếu Đã hạch toán không còn nút xử lý", "P0",
     "YC-6 Đã hạch toán",
     "1. KT-1 mở chi tiết YC-6",
     "—",
     "- Chỉ có nút Quay lại"),

    ("009", "Gọi thẳng Không duyệt phiếu Đã hạch toán", "P0",
     "YC-6 Đã hạch toán gồm CP1 của HD-01, đã có phiếu hạch toán và bút toán",
     "1. KT-1 dùng công cụ kiểm thử API gọi chức năng Không duyệt YC-6 với ghi chú \"test\"\n"
     "2. KD-1 lập phiếu Chi phí khác mới từ HD-01",
     "—",
     "- Mong đợi: bị chặn, YC-6 vẫn Đã hạch toán, CP1 vẫn bị khóa\n"
     "- Lưu ý: theo code hiện tại YC-6 về Không duyệt, CP1 mở lại và yêu cầu được lần nữa (hạch toán 2 lần) - "
     "ghi Failed"),

    ("010", "Gọi thẳng Hạch toán dịch vụ với phiếu Đang tạo", "P1",
     "YC-2 Đang tạo",
     "1. KT-1 dán đường dẫn lập phiếu hạch toán kèm YC-2",
     "—",
     "- Báo \"Không thể yêu cầu hạch toán làm dịch vụ cho hợp đồng này\", form không có dữ liệu"),
]
