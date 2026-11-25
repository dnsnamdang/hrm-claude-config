# -*- coding: utf-8 -*-
"""Section V - VIII cho man Phieu yeu cau hang bao hanh."""
from tc_data_role import MENU, DATA, OPEN_KD1, OPEN_CREATE

PREP = OPEN_CREATE + ", chọn Thương hiệu BR-A, Hãng sản xuất HSX-A, thêm H1"

SEC_V = [
    ("001", "Hàng của khách: chọn Khách hàng và Hợp đồng", "P0",
     DATA,
     "1. " + PREP + "\n"
     "2. Bấm kính lúp ở cột Khách hàng, chọn KH-01\n"
     "3. Bấm kính lúp ở cột Hợp đồng, chọn HD-01",
     "—",
     "- Ô Khách hàng hiện \"<mã KH-01> - <tên KH-01>\"\n"
     "- Báo \"Thêm thành công\", ô Hợp đồng hiện HD-01\n"
     "- Dưới ô hiện \"Ngày bàn giao: 10/09/2026\""),

    ("002", "Ô chọn hợp đồng chỉ liệt kê hợp đồng của khách đã chọn", "P1",
     DATA + "\nKH-02 có hợp đồng HD-05",
     "1. " + PREP + ", chọn Khách hàng KH-01\n"
     "2. Bấm kính lúp ở cột Hợp đồng",
     "—",
     "- Danh sách có HD-01, HD-02; không có HD-05"),

    ("003", "Chọn hợp đồng không có hàng cần bảo hành", "P0",
     DATA,
     "1. " + PREP + ", chọn Khách hàng KH-01\n"
     "2. Chọn hợp đồng HD-02",
     "—",
     "- Báo \"Hợp đồng không có hàng hóa cần bảo hành!\"\n"
     "- Ô Hợp đồng vẫn trống"),

    ("004", "Ô chọn hợp đồng không có hợp đồng chưa hiệu lực", "P1",
     DATA + "\nKH-01 có HD-03 đang tạo (chưa duyệt), có hàng H1",
     "1. " + PREP + ", chọn KH-01\n"
     "2. Bấm kính lúp ở cột Hợp đồng",
     "—",
     "- Không có HD-03"),

    ("005", "Bỏ Khách hàng và Hợp đồng", "P1",
     DATA,
     "1. " + PREP + ", chọn KH-01, HD-01\n"
     "2. Bấm dấu x ở ô Khách hàng và ô Hợp đồng",
     "—",
     "- Hai ô về trống, mất dòng Ngày bàn giao"),

    ("006", "Hàng tồn trong kho không cần khách hàng", "P0",
     DATA,
     "1. " + PREP + "\n"
     "2. Tích \"Hàng tồn trong kho\", nhập Nội dung \"Hỏng bo mạch\", không chọn khách, hợp đồng\n"
     "3. Bấm Lưu",
     "—",
     "- Báo \"Thao tác thành công\", phiếu Đang tạo\n"
     "- Mở chi tiết: ô Hàng tồn trong kho được tích, Khách hàng và Hợp đồng trống"),

    ("007", "Hàng không tồn kho phải có khách hàng và hợp đồng", "P0",
     DATA,
     "1. " + PREP + "\n"
     "2. Không tích Hàng tồn trong kho, nhập Nội dung, không chọn khách hàng\n"
     "3. Bấm Lưu",
     "—",
     "- Báo \"Tạo yêu cầu thất bại!\"\n"
     "- Báo lỗi đỏ dưới ô Khách hàng của dòng H1"),

    ("008", "Thêm hàng bảo hành thay thế (bảo hành bằng hàng)", "P0",
     DATA,
     "1. " + PREP + "\n"
     "2. Bấm + ở dòng \"Bảo hành bằng hàng\", chọn H2\n"
     "3. Nhập SL 2",
     "—",
     "- Báo \"Thêm thành công\"\n"
     "- Dòng con \"<mã H2> - <tên H2>\", SL 2"),

    ("009", "Hàng thay thế bị chọn trùng", "P1",
     DATA,
     "1. " + PREP + ", thêm H2 ở Bảo hành bằng hàng\n"
     "2. Bấm + lần nữa, chọn H2",
     "—",
     "- Báo \"Hàng hóa đã được chọn!\", không thêm dòng mới"),

    ("010", "Hàng thay thế khác thương hiệu", "P1",
     DATA,
     "1. " + PREP + "\n"
     "2. Bấm + ở Bảo hành bằng hàng, chọn H3",
     "—",
     "- Báo \"Hàng hóa không cùng thương hiệu!\""),

    ("011", "Thêm khoản bảo hành bằng tiền", "P0",
     DATA,
     "1. " + PREP + "\n"
     "2. Bấm + ở dòng \"Bảo hành bằng tiền\", nhập tên \"Phí sửa chữa\", Giá trị 1500000",
     "—",
     "- Ô Giá trị hiện \"1,500,000\"\n"
     "- Lưu xong mở chi tiết: dòng \"Phí sửa chữa\" giá trị 1,500,000"),

    ("012", "Đính kèm nhiều file cho một dòng hàng", "P1",
     DATA,
     "1. " + PREP + "\n"
     "2. Bấm \"Chọn file\", chọn 2 file loi_1.jpg, bien_ban.pdf\n"
     "3. Nhập Nội dung, tích Hàng tồn trong kho, bấm Lưu",
     "—",
     "- Trước khi lưu hiện 2 tên file\n"
     "- Mở chi tiết: 2 liên kết file mở được"),

    ("013", "Nhập serial", "P1",
     DATA,
     "1. " + PREP + "\n"
     "2. Nhập Số serial \"SN-001\", Nội dung, tích Hàng tồn trong kho, bấm Lưu",
     "—",
     "- Chi tiết cột Số serial hiện SN-001"),
]

SEC_VI = [
    ("001", "Lưu tạo phiếu Đang tạo", "P0",
     DATA,
     "1. " + PREP + ", tích Hàng tồn trong kho, Nội dung \"Hỏng bo mạch\"\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Thao tác thành công\", chuyển về danh sách\n"
     "- Phiếu mới số PYCHBH-xxxxx, Trạng thái \"Đang tạo\"\n"
     "- MH-1 không nhận thông báo"),

    ("002", "Lưu & Gửi chuyển Chờ duyệt và báo người mua hàng", "P0",
     DATA,
     "1. " + PREP + ", tích Hàng tồn trong kho, Nội dung \"Hỏng bo mạch\"\n"
     "2. Bấm \"Lưu & Gửi\"",
     "—",
     "- Báo \"Thao tác thành công\", phiếu \"Chờ duyệt\"\n"
     "- MH-1 nhận thông báo \"Bạn có một yêu cầu hãng bảo hành cần duyệt từ KD-1\", bấm mở chi tiết phiếu"),

    ("003", "Lưu & Gửi khi thương hiệu chưa phân công người mua hàng", "P0",
     DATA,
     "1. " + OPEN_CREATE + ", chọn BR-B, HSX-B, thêm H3, tích Hàng tồn trong kho, nhập Nội dung\n"
     "2. Bấm \"Lưu & Gửi\"",
     "—",
     "- Mong đợi: báo \"Chưa phân công người phụ trách thương hiệu, hãng sản xuất\"\n"
     "- Lưu ý: theo code hiện tại báo \"Tạo yêu cầu thất bại!\" kèm lỗi đỏ ở ô Người nhận đơn, câu báo phân công "
     "không bao giờ hiện - ghi Failed"),

    ("004", "Lưu nháp khi thương hiệu chưa phân công người mua hàng", "P1",
     DATA,
     "1. " + OPEN_CREATE + ", chọn BR-B, HSX-B, thêm H3, tích Hàng tồn trong kho, nhập Nội dung\n"
     "2. Bấm Lưu",
     "—",
     "- Mong đợi: lưu được phiếu Đang tạo\n"
     "- Lưu ý: theo code hiện tại bị chặn vì Người nhận đơn bắt buộc - ghi Failed nếu nghiệp vụ cho lưu nháp"),

    ("005", "Phiếu lưu ghi công ty, phòng của người lập", "P1",
     DATA,
     "1. KD-1 (TPE, PKD1) bấm Lưu & Gửi một phiếu, Công ty gửi chọn TPC (BR-A / HSX-A tại TPC phân công MH-7)",
     "—",
     "- Cột Phòng yêu cầu PKD1\n"
     "- MH-7 (không phải MH-1) nhận thông báo và có nút duyệt"),

    ("006", "Đổi tên hãng sau khi lập phiếu", "P2",
     "PYC-01 đã gửi, BR-A / HSX-A; sau đó đổi tên hãng HSX-A thành HSX-A1 ở danh mục",
     "1. " + OPEN_KD1 + ", xem dòng PYC-01\n"
     "2. Bấm In PYC-01",
     "—",
     "- Danh sách hiện tên mới HSX-A1\n"
     "- Bản in hiện tên lúc lập HSX-A\n"
     "- Lưu ý: hai nơi hiện khác nhau - ghi để nghiệp vụ quyết"),

    ("007", "Bấm Lưu hai lần liên tiếp", "P1",
     DATA,
     "1. " + PREP + ", tích Hàng tồn trong kho, nhập Nội dung\n"
     "2. Bấm Lưu 2 lần thật nhanh",
     "—",
     "- Nút mờ sau lần bấm đầu, chỉ tạo 1 phiếu"),

    ("008", "Quay lại không lưu", "P2",
     DATA,
     "1. " + PREP + "\n"
     "2. Bấm Quay lại",
     "—",
     "- Về danh sách, không có phiếu mới"),
]

SEC_VII = [
    ("001", "Bỏ trống Thương hiệu / Hãng sản xuất", "P0",
     DATA,
     "1. " + OPEN_CREATE + "\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo yêu cầu thất bại!\"\n"
     "- Lỗi đỏ dưới Thương hiệu, Hãng sản xuất và dưới bảng hàng"),

    ("002", "Bỏ trống Nội dung cần bảo hành", "P0",
     DATA,
     "1. " + PREP + ", tích Hàng tồn trong kho, không nhập Nội dung\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo yêu cầu thất bại!\", lỗi đỏ dưới ô Nội dung của dòng H1"),

    ("003", "Trùng hàng và serial", "P0",
     DATA,
     "1. " + PREP + ", thêm H1 lần nữa\n"
     "2. Cả hai dòng nhập serial \"SN-001\", nội dung, tích tồn kho, bấm Lưu",
     "—",
     "- Báo \"Hàng <tên H1> có serial trùng nhau!\", không lưu"),

    ("004", "Cùng hàng, khác serial", "P1",
     DATA,
     "1. " + PREP + ", thêm H1 lần nữa\n"
     "2. Dòng 1 serial SN-001, dòng 2 serial SN-002, nhập nội dung, tích tồn kho, bấm Lưu",
     "—",
     "- Lưu thành công, phiếu có 2 dòng H1"),

    ("005", "Cùng hàng, cả hai dòng không nhập serial", "P2",
     DATA,
     "1. " + PREP + ", thêm H1 lần nữa\n"
     "2. Không nhập serial cả hai dòng, nhập nội dung, tích tồn kho, bấm Lưu",
     "—",
     "- Mong đợi: lưu được (2 chiếc chưa có serial) hoặc báo rõ \"cần nhập serial\"\n"
     "- Lưu ý: theo code hiện tại báo \"có serial trùng nhau!\" - ghi Failed nếu nghiệp vụ cho lưu"),

    ("006", "SL hàng thay thế bằng 0 hoặc trống", "P1",
     DATA,
     "1. " + PREP + ", thêm H2 ở Bảo hành bằng hàng, để SL trống\n"
     "2. Nhập nội dung, tích tồn kho, bấm Lưu",
     "—",
     "- Báo \"Tạo yêu cầu thất bại!\", lỗi đỏ dưới ô SL"),

    ("007", "Khoản bảo hành bằng tiền thiếu tên hoặc giá trị", "P1",
     DATA,
     "1. " + PREP + ", thêm 1 dòng Bảo hành bằng tiền, để trống tên và giá trị\n"
     "2. Nhập nội dung, tích tồn kho, bấm Lưu",
     "—",
     "- Báo \"Tạo yêu cầu thất bại!\", lỗi đỏ dưới ô tên và ô Giá trị"),

    ("008", "Ghi chú phiếu dài hơn 255 ký tự", "P2",
     DATA,
     "1. " + PREP + ", nhập Ghi chú 300 ký tự, nội dung, tích tồn kho\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo yêu cầu thất bại!\", lỗi đỏ dưới ô Ghi chú"),

    ("009", "Gọi thẳng chức năng lưu với hàng khác thương hiệu", "P1",
     DATA,
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu: Thương hiệu BR-A, dòng hàng H3",
     "—",
     "- Báo \"Hàng <tên H3> có thương hiệu không khớp!\", không tạo phiếu"),

    ("010", "Gọi thẳng chức năng lưu với hàng cùng thương hiệu khác hãng", "P2",
     DATA,
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu: BR-A / HSX-A, dòng hàng H5 (BR-A, hãng HSX-C)",
     "—",
     "- Mong đợi: bị chặn vì hàng không thuộc hãng HSX-A\n"
     "- Lưu ý: theo code hiện tại lưu được (chỉ kiểm tra thương hiệu) - ghi Failed nếu nghiệp vụ yêu cầu cùng hãng"),
]

SEC_VII.append(
    ("011", "Có khách hàng nhưng không chọn hợp đồng", "P1",
     DATA,
     "1. " + PREP + ", không tích tồn kho, chọn Khách hàng KH-01, không chọn hợp đồng, nhập nội dung\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Tạo yêu cầu thất bại!\", lỗi đỏ dưới ô Hợp đồng của dòng H1"))

SEC_VIII = [
    ("001", "Sửa phiếu Đang tạo", "P0",
     "PYC-04 do KD-1 lập, Đang tạo, có dòng H1 tồn kho",
     "1. " + OPEN_KD1 + ", menu Hành động PYC-04 bấm Sửa\n"
     "2. Đổi Nội dung thành \"Hỏng màn hình\", thêm H2 tồn kho có nội dung\n"
     "3. Bấm Lưu",
     "—",
     "- Form hiện đủ dữ liệu cũ\n"
     "- Lưu xong: phiếu có 2 dòng H1 (Hỏng màn hình), H2; số phiếu giữ nguyên, vẫn Đang tạo"),

    ("002", "Sửa rồi Lưu & Gửi", "P0",
     "PYC-04 Đang tạo",
     "1. KD-1 mở Sửa PYC-04, bấm \"Lưu & Gửi\"",
     "—",
     "- Phiếu sang Chờ duyệt, MH-1 nhận thông báo cần duyệt"),

    ("003", "Sửa phiếu Không duyệt và gửi lại", "P0",
     "PYC-01 bị MH-1 Không duyệt với ghi chú \"Thiếu ảnh lỗi\"",
     "1. KD-1 mở Sửa PYC-01, thêm file ảnh, bấm \"Lưu & Gửi\"",
     "—",
     "- Form Sửa mở được, hiện ghi chú duyệt cũ\n"
     "- Phiếu về Chờ duyệt, MH-1 nhận thông báo lại"),

    ("004", "Giữ và xóa file cũ khi sửa", "P1",
     "PYC-04 dòng H1 có 2 file a.jpg, b.pdf",
     "1. KD-1 mở Sửa PYC-04, bấm x ở file a.jpg, xác nhận\n"
     "2. Bấm Lưu, mở chi tiết",
     "—",
     "- Hỏi \"Bạn chắc chắn muốn xóa file này?\"\n"
     "- Sau lưu chỉ còn b.pdf"),

    ("005", "Không có Sửa / Xóa với phiếu đã gửi", "P0",
     "PYC-01 Chờ duyệt, PYC-03 Đã gửi NCC (KD-1 lập)",
     "1. KD-1 mở menu Hành động PYC-01, PYC-03\n"
     "2. Dán đường dẫn Sửa PYC-03",
     "—",
     "- Không có Sửa, Xóa\n"
     "- Dán đường dẫn ra trang không tìm thấy"),

    ("006", "Người khác không sửa được phiếu Đang tạo", "P0",
     "PYC-04 do KD-1 lập, Đang tạo",
     "1. Đăng nhập KD-2, dán đường dẫn Sửa PYC-04\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lưu sửa PYC-04",
     "—",
     "- Đường dẫn ra trang không tìm thấy\n"
     "- Gọi thẳng báo \"Bạn không có quyền\""),

    ("007", "Xóa phiếu Đang tạo", "P0",
     "PYC-04 do KD-1 lập, Đang tạo",
     "1. KD-1 mở menu Hành động PYC-04, bấm Xóa, xác nhận",
     "—",
     "- Báo \"Xóa yêu cầu thành công!\"\n"
     "- PYC-04 biến mất khỏi danh sách; tìm theo số phiếu không còn"),

    ("008", "Xóa phiếu Không duyệt", "P1",
     "PYC-01 Không duyệt (KD-1 lập)",
     "1. KD-1 mở menu Hành động PYC-01, bấm Xóa, xác nhận",
     "—",
     "- Báo \"Xóa yêu cầu thành công!\""),

    ("009", "Xóa phiếu không được phép qua đường dẫn", "P1",
     "PYC-03 Đã gửi NCC (KD-1 lập)",
     "1. KD-1 dán đường dẫn Xóa PYC-03",
     "—",
     "- Báo \"Không thể xóa yêu cầu!\", PYC-03 vẫn còn"),

    ("010", "Sửa đổi Thương hiệu xóa dòng hàng cũ", "P1",
     "PYC-04 Đang tạo, BR-A, có H1",
     "1. KD-1 mở Sửa PYC-04, đổi Thương hiệu sang BR-B",
     "—",
     "- Bảng hàng về \"Chưa có hàng hóa\""),
]
