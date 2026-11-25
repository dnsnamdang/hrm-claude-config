# -*- coding: utf-8 -*-
"""Section IX - XII cho man Phieu yeu cau hang bao hanh."""
from tc_data_role import MENU, DATA, OPEN_KD1, OPEN_CREATE

PYC1 = ("PYC-01 do KD-1 lập, BR-A / HSX-A, Công ty gửi TPE, Chờ duyệt; dòng H1 của KH-01 (HD-01), serial SN-001, "
        "nội dung \"Hỏng bo mạch\", bảo hành bằng hàng H2 SL 1, bảo hành bằng tiền \"Phí sửa chữa\" 1,500,000")
OPEN_MH1 = "Đăng nhập MH-1, mở chi tiết PYC-01"
MENU_THU = "Mở menu Mua hàng > mục \"Hãng bảo hành\" > bấm \"Thư yêu cầu bảo hành\""

SEC_IX = [
    ("001", "Xem chi tiết phiếu", "P0",
     PYC1,
     "1. " + OPEN_KD1 + ", bấm số phiếu PYC-01",
     "—",
     "- Tiêu đề \"Chi tiết yêu cầu hãng bảo hành PYCHBH-xxxxx\"\n"
     "- Thương hiệu BR-A, Hãng HSX-A, Công ty TPE, Người mua hàng MH-1, Người yêu cầu KD-1, Phòng PKD1\n"
     "- Dòng H1: serial SN-001, nội dung \"Hỏng bo mạch\", khách KH-01, hợp đồng HD-01, ngày bàn giao 10/09/2026\n"
     "- Bảo hành bằng hàng: H2 SL 1; bảo hành bằng tiền: Phí sửa chữa 1,500,000\n"
     "- Mọi ô chỉ xem, không có Lưu / Lưu & Gửi"),

    ("002", "Người mua hàng thấy khung duyệt", "P0",
     PYC1,
     "1. " + OPEN_MH1,
     "—",
     "- Có khung \"Ghi chú duyệt\" nhập được\n"
     "- Có nút \"Không duyệt\", \"Lập thư yêu cầu\", \"Quay lại\""),

    ("003", "Không duyệt bắt buộc ghi chú", "P0",
     PYC1,
     "1. " + OPEN_MH1 + "\n"
     "2. Để trống Ghi chú duyệt, bấm \"Không duyệt\"",
     "—",
     "- Mong đợi: báo cần nhập ghi chú duyệt\n"
     "- Thực tế: báo \"Tạo thất bại!\" kèm lỗi đỏ dưới Ghi chú duyệt; phiếu vẫn Chờ duyệt\n"
     "- Lưu ý: câu báo \"Tạo thất bại!\" không đúng thao tác - ghi Failed mức nhẹ"),

    ("004", "Không duyệt thành công", "P0",
     PYC1,
     "1. " + OPEN_MH1 + "\n"
     "2. Nhập Ghi chú duyệt \"Thiếu ảnh lỗi\", bấm \"Không duyệt\"",
     "—",
     "- Báo thành công, chuyển về danh sách chờ duyệt\n"
     "- PYC-01 trạng thái \"Không duyệt\"\n"
     "- KD-1 nhận thông báo \"Bạn có một yêu cầu bảo hành bị từ chối bởi MH-1\", bấm mở chi tiết PYC-01"),

    ("005", "Người lập xem lại ghi chú không duyệt", "P1",
     "PYC-01 đã bị Không duyệt với ghi chú \"Thiếu ảnh lỗi\"",
     "1. " + OPEN_KD1 + ", mở chi tiết PYC-01",
     "—",
     "- Khung Ghi chú duyệt hiện \"Thiếu ảnh lỗi\", không sửa được"),

    ("006", "Phiếu đã Không duyệt không duyệt lại được", "P1",
     "PYC-01 Không duyệt",
     "1. " + OPEN_MH1,
     "—",
     "- Không có nút Không duyệt, Lập thư yêu cầu"),

    ("007", "Nút Quay lại ở chi tiết", "P2",
     PYC1,
     "1. " + OPEN_KD1 + ", mở chi tiết PYC-01, bấm Quay lại",
     "—",
     "- Về danh sách Phiếu Yêu cầu hãng bảo hành"),

    ("008", "Mở file đính kèm ở chi tiết", "P2",
     PYC1 + "; dòng H1 có file loi_1.jpg",
     "1. " + OPEN_KD1 + ", mở chi tiết PYC-01, bấm tên file",
     "—",
     "- Mở file ở tab mới, không có dấu x xóa file"),
]

SEC_X = [
    ("001", "Lập thư yêu cầu mở form thư điền sẵn", "P0",
     PYC1,
     "1. " + OPEN_MH1 + ", bấm \"Lập thư yêu cầu\"",
     "—",
     "- Mở tab mới form Thư yêu cầu bảo hành\n"
     "- Thư điền sẵn số phiếu yêu cầu, Thương hiệu BR-A, Hãng HSX-A, các dòng hàng, serial, nội dung, hàng thay "
     "thế, khoản tiền của PYC-01"),

    ("002", "Lưu nháp thư: phiếu sang Đang gửi NCC", "P0",
     PYC1,
     "1. MH-1 lập thư yêu cầu từ PYC-01, chọn nhà cung cấp, nhập nội dung, bấm Lưu (nháp)\n"
     "2. Mở lại danh sách Phiếu Yêu cầu hãng bảo hành",
     "—",
     "- PYC-01 \"Đang gửi NCC\", Người duyệt MH-1, Ngày duyệt trống\n"
     "- Chi tiết PYC-01 không còn nút Không duyệt / Lập thư yêu cầu"),

    ("003", "Gửi thư NCC: phiếu sang Đã gửi NCC", "P0",
     PYC1,
     "1. MH-1 lập thư yêu cầu từ PYC-01, bấm gửi NCC\n"
     "2. Mở lại danh sách",
     "—",
     "- PYC-01 \"Đã gửi NCC\" màu xanh, Ngày duyệt là lúc gửi, Người duyệt MH-1\n"
     "- Người có quyền lập phiếu xác nhận bảo hành nhận thông báo \"Thư yêu cầu nhà cung cấp bảo hành cần duyệt "
     "từ MH-1\""),

    ("004", "Sửa thư nháp rồi gửi NCC", "P1",
     "PYC-01 Đang gửi NCC, thư TYC-01 nháp",
     "1. MH-1 mở Sửa TYC-01, bấm gửi NCC",
     "—",
     "- PYC-01 sang \"Đã gửi NCC\", có Ngày duyệt"),

    ("005", "Lập phiếu xác nhận bảo hành: phiếu sang Đã xác nhận BH", "P0",
     "PYC-01 Đã gửi NCC, thư TYC-01 đã gửi",
     "1. Người có quyền lập phiếu xác nhận bảo hành, " + MENU_THU + ", ở TYC-01 bấm \"Lập phiếu xác nhận bảo "
     "hành\", lưu\n"
     "2. Mở danh sách Phiếu Yêu cầu hãng bảo hành",
     "—",
     "- PYC-01 \"Đã xác nhận BH\""),

    ("006", "Xóa thư nháp trả phiếu về để lập lại", "P0",
     "PYC-01 Đang gửi NCC, thư TYC-01 nháp",
     "1. MH-1 xóa TYC-01\n"
     "2. Mở chi tiết PYC-01; KD-1 mở menu Hành động PYC-01",
     "—",
     "- Mong đợi: PYC-01 về Chờ duyệt, MH-1 lại có nút Lập thư yêu cầu\n"
     "- Lưu ý: theo code hiện tại PYC-01 vẫn \"Đang gửi NCC\", Người duyệt bị xóa trống; MH-1 không có nút duyệt, "
     "KD-1 không sửa / xóa được - phiếu kẹt - ghi Failed"),

    ("007", "Trạng thái Hoàn thành", "P2",
     "PYC-01 Đã xác nhận BH; hàng bảo hành đã nhập về kho",
     "1. Mở danh sách, lọc Trạng thái \"Hoàn thành\"",
     "—",
     "- Mong đợi: phiếu đã xử lý xong sang Hoàn thành\n"
     "- Lưu ý: theo code hiện tại không có bước nào chuyển phiếu sang Hoàn thành - ghi để nghiệp vụ quyết"),

    ("008", "Người mua hàng đổi phân công trước khi duyệt", "P1",
     "PYC-01 Chờ duyệt; phân công BR-A / HSX-A tại TPE chuyển từ MH-1 sang MH-2",
     "1. Đăng nhập MH-1, mở chi tiết PYC-01\n"
     "2. Đăng nhập MH-2, mở chi tiết PYC-01",
     "—",
     "- MH-1: không còn nút duyệt\n"
     "- MH-2: có nút Không duyệt, Lập thư yêu cầu"),

    ("009", "Mở form thư cho phiếu không còn Chờ duyệt", "P1",
     "PYC-03 Đã gửi NCC",
     "1. MH-1 dán đường dẫn tạo thư yêu cầu kèm số phiếu PYC-03",
     "—",
     "- Báo \"Không có quyền!\", form không có dữ liệu phiếu"),
]

SEC_XI = [
    ("001", "In một phiếu", "P0",
     PYC1,
     "1. " + OPEN_KD1 + ", menu Hành động PYC-01 bấm In",
     "—",
     "- Mở tab mới bản in \"Phiếu yêu cầu hãng bảo hành\", đầu trang của công ty TPE\n"
     "- Có số phiếu, ngày lập, thương hiệu, hãng, người nhận đơn, người yêu cầu, phòng yêu cầu, ghi chú\n"
     "- Bảng: H1 (Model, Code đặt hàng, Mã hàng, ĐVT), serial SN-001, nội dung, khách hàng, hợp đồng + ngày bàn "
     "giao; dòng 1.1 Bảo hành bằng hàng H2 SL 1; dòng 1.2 Bảo hành bằng tiền Phí sửa chữa 1,500,000"),

    ("002", "Bản in dòng Tên TA", "P2",
     PYC1 + "; H1 có tên tiếng Anh \"Control board\"",
     "1. In PYC-01",
     "—",
     "- Mong đợi: \"Tên TA: Control board\"\n"
     "- Lưu ý: theo code hiện tại dòng \"Tên TA:\" luôn trống - ghi Failed mức nhẹ"),

    ("003", "Xuất Excel một phiếu", "P0",
     PYC1,
     "1. " + OPEN_KD1 + ", menu Hành động PYC-01 bấm Xuất Excel",
     "—",
     "- Tải file phieu_yeu_cau_hang_bao_hanh.xlsx\n"
     "- Nội dung khớp bản in: số phiếu, ngày lập, thương hiệu, hãng, người nhận đơn, phòng yêu cầu, bảng hàng"),

    ("004", "In danh sách theo bộ lọc", "P0",
     "KD-1 có PYC-01 (Chờ duyệt), PYC-03 (Đã gửi NCC), PYC-04 (Đang tạo)",
     "1. " + OPEN_KD1 + ", lọc Trạng thái \"Chờ duyệt\"\n"
     "2. Bấm In",
     "—",
     "- Bản in khổ ngang chỉ có PYC-01\n"
     "- Cột: STT, Số phiếu, Hãng sản xuất, Người nhận đơn, Người yêu cầu, Phòng yêu cầu, Ngày duyệt, Ngày lập, "
     "Trạng thái"),

    ("005", "Xuất Excel danh sách", "P0",
     "KD-1 có PYC-01, PYC-03, PYC-04",
     "1. " + OPEN_KD1 + ", không lọc, bấm Xuất Excel",
     "—",
     "- Tải file danh_sach_phieu_yeu_cau_hang_bao_hanh.xlsx, tiêu đề \"Danh sách phiếu yêu cầu hãng bảo hành\"\n"
     "- Có đủ 3 phiếu, cột như bản in danh sách"),

    ("006", "Xuất Excel danh sách giữ phạm vi quyền", "P0",
     "KD-2 không có quyền xem; PYC-01 do KD-1 lập",
     "1. Đăng nhập KD-2, " + MENU + ", bấm Xuất Excel",
     "—",
     "- File không có PYC-01"),

    ("007", "Tên hãng có ký tự & trên bản in danh sách", "P2",
     "PYC-10 hãng \"A & B Co.\"",
     "1. In danh sách có PYC-10",
     "—",
     "- Cột Hãng sản xuất hiện \"A & B Co.\" đúng"),
]

SEC_XII = [
    ("001", "Xuất Excel phiếu không có quyền xem qua đường dẫn", "P0",
     "KD-2 không có quyền xem, không phụ trách mua hàng; PYC-01 do KD-1 lập",
     "1. Đăng nhập KD-2, dán đường dẫn Xuất Excel của PYC-01",
     "—",
     "- Mong đợi: ra trang không tìm thấy, không tải được file\n"
     "- Lưu ý: theo code hiện tại tải được file đủ thông tin khách hàng, hợp đồng, hàng, serial - ghi Failed"),

    ("002", "Gọi thẳng chức năng Không duyệt với trạng thái khác", "P0",
     PYC1,
     "1. MH-1 dùng công cụ kiểm thử API gọi thẳng chức năng Không duyệt PYC-01, ghi chú \"x\", trạng thái "
     "\"Đã xác nhận BH\"",
     "—",
     "- Mong đợi: chỉ chấp nhận Không duyệt, báo lỗi\n"
     "- Lưu ý: theo code hiện tại PYC-01 sang \"Đã xác nhận BH\" mà không có thư, không có xác nhận - ghi Failed"),

    ("003", "Gọi thẳng chức năng duyệt cũ", "P2",
     PYC1,
     "1. MH-1 dùng công cụ kiểm thử API gọi thẳng chức năng duyệt cũ của PYC-01 với trạng thái \"Đã gửi NCC\"",
     "—",
     "- Mong đợi: không có tác dụng hoặc báo không hỗ trợ\n"
     "- Lưu ý: theo code hiện tại báo lỗi hệ thống (chức năng này còn sót, gọi tới phần không tồn tại) - ghi Failed "
     "mức nhẹ"),

    ("004", "Hai tab cùng lập thư yêu cầu", "P1",
     PYC1,
     "1. MH-1 bấm \"Lập thư yêu cầu\" 2 lần, mở 2 tab form thư\n"
     "2. Tab 1 lưu nháp, tab 2 lưu nháp",
     "—",
     "- Mong đợi: tab 2 bị chặn vì PYC-01 đã có thư\n"
     "- Lưu ý: theo code hiện tại lưu được 2 thư cho cùng một phiếu - ghi Failed"),

    ("005", "Người lập sửa trong lúc người mua hàng đang mở", "P1",
     "PYC-01 Không duyệt; MH-1 đang mở chi tiết từ trước",
     "1. KD-1 sửa PYC-01, bấm Lưu & Gửi\n"
     "2. MH-1 (không tải lại) nhập ghi chú, bấm Không duyệt",
     "—",
     "- Không duyệt thành công theo dữ liệu mới, PYC-01 về Không duyệt"),

    ("006", "Không duyệt sau khi đã lập thư", "P1",
     PYC1,
     "1. MH-1 mở chi tiết PYC-01 ở tab A\n"
     "2. Ở tab B lập thư nháp cho PYC-01\n"
     "3. Quay về tab A, nhập ghi chú, bấm Không duyệt",
     "—",
     "- Báo \"Bạn không có quyền!\", PYC-01 vẫn Đang gửi NCC"),

    ("007", "Luồng đầu - cuối: tạo, gửi, lập thư, xác nhận", "P0",
     DATA,
     "1. KD-1 tạo phiếu BR-A / HSX-A, dòng H1 của KH-01 (HD-01), bấm Lưu & Gửi\n"
     "2. MH-1 mở thông báo, bấm Lập thư yêu cầu, gửi NCC\n"
     "3. Người có quyền lập phiếu xác nhận bảo hành lập xác nhận từ thư\n"
     "4. KD-1 mở danh sách, In phiếu",
     "—",
     "- Sau bước 1: Chờ duyệt; bước 2: Đã gửi NCC, Người duyệt MH-1, có Ngày duyệt; bước 3: Đã xác nhận BH\n"
     "- Bản in khớp dữ liệu đã nhập, Người nhận đơn MH-1"),

    ("008", "Luồng đầu - cuối: không duyệt, sửa, gửi lại", "P0",
     DATA,
     "1. KD-1 tạo phiếu hàng tồn kho, Lưu & Gửi\n"
     "2. MH-1 Không duyệt với ghi chú \"Bổ sung serial\"\n"
     "3. KD-1 nhận thông báo, Sửa, nhập serial, Lưu & Gửi\n"
     "4. MH-1 lập thư, gửi NCC",
     "—",
     "- Trạng thái lần lượt: Chờ duyệt, Không duyệt, Chờ duyệt, Đã gửi NCC\n"
     "- Ô chờ duyệt trang chủ của MH-1 tăng, giảm đúng theo từng bước"),
]
