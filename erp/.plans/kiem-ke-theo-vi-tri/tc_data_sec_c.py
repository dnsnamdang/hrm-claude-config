# -*- coding: utf-8 -*-
"""Section V - X — nhap ket qua, duyet, xu ly, xoa, in/xuat, rang buoc, co lap, luong dau-cuoi."""
from tc_data_role import P1

KK3 = "Phiếu KK-3 Đang kiểm do TK1 lập, lập từ kế hoạch KH-3, có vị trí P1 (" + \
      "lô L01 = 10, L02 = 15, L07 = 5, ĐVT Cái), chưa có file đính kèm"
KK1 = "Phiếu KK-1 Chờ duyệt kết quả, thuộc công ty 1, lập từ kế hoạch KH-3"

SEC_V = [
    ("001", "Mở Nhập kết quả", "P0",
     KK3,
     "1. TK1 bấm bánh răng KK-3 > \"Nhập kết quả\"\n"
     "2. Quan sát bảng và cuối trang",
     "—",
     "- Mở màn Chi tiết KK-3\n"
     "- Bảng có thêm cột Thực kiểm (*), Chênh lệch, Ghi chú, Tổng kiểm kê\n"
     "- Thực kiểm mặc định = SL của dòng (10, 15, 5), Chênh lệch = 0\n"
     "- Khối File đính kèm có nút dấu + để chọn file\n"
     "- Có nút \"Lưu kết quả\""),

    ("002", "Chênh lệch tự tính khi thiếu", "P0",
     KK3,
     "1. Ở dòng lô L01 sửa Thực kiểm thành 8",
     "Thực kiểm L01: 8",
     "- Chênh lệch dòng L01 = -2 ngay khi gõ"),

    ("003", "Chênh lệch tự tính khi thừa", "P0",
     KK3,
     "1. Ở dòng lô L07 sửa Thực kiểm thành 7",
     "Thực kiểm L07: 7",
     "- Chênh lệch dòng L07 = 2"),

    ("004", "Dòng có chênh lệch mà thiếu Ghi chú", "P0",
     KK3 + "\nĐã đính kèm 1 file",
     "1. Sửa Thực kiểm L01 = 8, để trống Ghi chú\n"
     "2. Bấm \"Lưu kết quả\"",
     "—",
     "- Thông báo vàng \"Thao tác thất bại!\", phiếu không đổi trạng thái\n"
     "- Lưu ý: không chỉ ra dòng nào thiếu ghi chú — ghi nhận"),

    ("005", "Lần đầu Lưu kết quả mà chưa đính kèm file", "P0",
     KK3,
     "1. Giữ nguyên Thực kiểm, không chọn file\n"
     "2. Bấm \"Lưu kết quả\"",
     "—",
     "- Thông báo \"Tạo thất bại!\"\n"
     "- Chữ đỏ dưới khối File đính kèm (tiếng Anh); phiếu vẫn Đang kiểm"),

    ("006", "Chọn nhiều file và bỏ bớt trước khi lưu", "P1",
     KK3,
     "1. Bấm dấu + ở khối File đính kèm, chọn cùng lúc bienban.pdf và anh1.jpg\n"
     "2. Bấm X trên anh1.jpg",
     "File: bienban.pdf, anh1.jpg",
     "- Hiện 2 ô file với đúng tên\n"
     "- Sau khi bấm X còn bienban.pdf"),

    ("007", "File sai định dạng", "P1",
     KK3,
     "1. Bấm dấu +, thử chọn file data.zip",
     "File: data.zip",
     "- Hộp chọn file chỉ cho chọn pdf, png, jpg, jpeg, doc, docx, xls, xlsx\n"
     "- Nếu ép chọn được thì Lưu kết quả bị báo lỗi, không lưu"),

    ("008", "Lưu kết quả thành công và thông báo Ban kiểm soát", "P0",
     KK3 + "\nBKS (công ty 1) và BKS3 (công ty 3) đều có quyền Ban kiểm soát; TK1 thuộc công ty 1",
     "1. Sửa Thực kiểm L01 = 8, Ghi chú \"Rơi vỡ\"; chọn bienban.pdf\n"
     "2. Bấm \"Lưu kết quả\"\n"
     "3. Đăng nhập BKS, BKS3 xem thông báo",
     "Thực kiểm L01: 8\n"
     "Ghi chú: Rơi vỡ",
     "- \"Cập nhật thành công\", về danh sách Phiếu của tôi\n"
     "- KK-3 chuyển Chờ duyệt kết quả\n"
     "- BKS nhận \"Bạn có 1 phiếu kiểm kê vị trí cần duyệt\", bấm vào mở đúng KK-3\n"
     "- BKS3 không nhận"),

    ("009", "Tích Tổng kiểm kê ở dòng không chênh lệch", "P2",
     KK3,
     "1. Ở dòng L02 (Thực kiểm = SL) tích Tổng kiểm kê\n"
     "2. Lưu kết quả hợp lệ, mở lại Chi tiết",
     "—",
     "- Dòng L02 KHÔNG được ghi nhận Tổng kiểm kê (chỉ ghi khi Chênh lệch khác 0)"),

    ("010", "Ban kiểm soát mở phiếu chờ duyệt", "P0",
     KK1,
     "1. BKS bấm bánh răng KK-1 > \"Duyệt kết quả\"",
     "—",
     "- Bảng hiện Thực kiểm, Chênh lệch, Ghi chú ở dạng chỉ xem\n"
     "- Ô Ghi chú duyệt nhập được\n"
     "- Có nút \"Duyệt kết quả\", \"Không duyệt\""),

    ("011", "Duyệt phiếu không có dòng thiếu", "P0",
     KK1 + "\nMọi dòng chênh lệch bằng 0 hoặc dương",
     "1. BKS nhập Ghi chú duyệt \"Đã đối chiếu\", bấm \"Duyệt kết quả\"\n"
     "2. Xem KK-1 và KH-3",
     "Ghi chú duyệt: Đã đối chiếu",
     "- \"Thao tác thành công!\", về danh sách chờ duyệt, KK-1 không còn ở đó\n"
     "- KK-1 Hoàn thành; Người duyệt = BKS, Ngày duyệt = hôm nay\n"
     "- KH-3 chuyển Hoàn thành\n"
     "- Không phát sinh thông báo cho người xử lý"),

    ("012", "Duyệt phiếu có dòng thiếu", "P0",
     KK1 + "\nDòng L01 chênh lệch -2\n"
     "XL (công ty 1) có quyền Xử lý phiếu kiểm kê vị trí",
     "1. BKS bấm \"Duyệt kết quả\" (để trống Ghi chú duyệt)\n"
     "2. Xem KK-1, KH-3; XL xem thông báo",
     "—",
     "- Duyệt được dù Ghi chú duyệt trống\n"
     "- KK-1 Chờ xử lý, có Người duyệt và Ngày duyệt\n"
     "- KH-3 vẫn Đã lập kiểm kê\n"
     "- XL nhận \"Bạn có 1 phiếu kiểm kê vị trí cần xử lý\""),

    ("013", "Không duyệt khi chưa nhập Ghi chú duyệt", "P0",
     KK1,
     "1. BKS để trống Ghi chú duyệt, bấm \"Không duyệt\"",
     "—",
     "- Thông báo \"Tạo thất bại!\", chữ đỏ dưới ô Ghi chú duyệt\n"
     "- KK-1 giữ Chờ duyệt kết quả"),

    ("014", "Không duyệt trả phiếu về người lập", "P0",
     KK1 + "\nNgười lập là TK1",
     "1. BKS nhập \"Đếm lại khoang KG1\", bấm \"Không duyệt\"\n"
     "2. TK1 xem thông báo, mở KK-1",
     "Ghi chú duyệt: Đếm lại khoang KG1",
     "- \"Thao tác thành công!\", về danh sách chờ duyệt\n"
     "- KK-1 về Đang kiểm, Người duyệt trống\n"
     "- TK1 nhận \"<Họ tên BKS> đã từ chối duyệt phiếu kiểm kê vị trí của bạn\"\n"
     "- TK1 thấy lại \"Nhập kết quả\"; Ghi chú duyệt hiện \"Đếm lại khoang KG1\""),

    ("015", "Nhập lại kết quả sau khi bị Không duyệt", "P1",
     "KK-1 vừa bị Không duyệt, đã có bienban.pdf từ lần trước",
     "1. TK1 Nhập kết quả, sửa Thực kiểm, không chọn file mới\n"
     "2. Bấm \"Lưu kết quả\"",
     "—",
     "- Lưu được, không bắt đính kèm lại\n"
     "- bienban.pdf vẫn còn; KK-1 về Chờ duyệt kết quả"),

    ("016", "Xóa file đã đính kèm khi nhập lại kết quả", "P2",
     "Như TC_05.015",
     "1. Bấm X trên bienban.pdf (file đã lưu)",
     "—",
     "- Mong đợi: file bị bỏ khỏi phiếu\n"
     "- Lưu ý: nút X hiện không có tác dụng — nếu vậy ghi Failed"),

    ("017", "Người xử lý tích Tổng kiểm kê", "P0",
     "KK-2 Chờ xử lý: dòng L01 thiếu 2 cái, chưa tích Tổng kiểm kê",
     "1. XL bấm bánh răng KK-2 > \"Xử lý\"\n"
     "2. Tích ô Tổng kiểm kê dòng L01\n"
     "3. Tải lại trang",
     "—",
     "- Thông báo \"Thao tác thành công!\" ngay khi tích, không cần bấm lưu\n"
     "- Sau khi tải lại ô vẫn được tích"),

    ("018", "Nút Tạo phiếu điều chuyển vị trí và Hoàn thành đổi theo dòng thiếu", "P0",
     "KK-2 Chờ xử lý: dòng L01 thiếu 2 cái, chưa tích Tổng kiểm kê",
     "1. XL mở Chi tiết KK-2, quan sát cuối trang\n"
     "2. Tích Tổng kiểm kê dòng L01\n"
     "3. Bỏ tích lại",
     "—",
     "- Bước 1: có nút \"Tạo phiếu điều chuyển vị trí\", KHÔNG có Hoàn thành\n"
     "- Bước 2: nút đổi thành \"Hoàn thành\"\n"
     "- Bước 3: quay về \"Tạo phiếu điều chuyển vị trí\""),

    ("019", "Tạo phiếu điều chuyển vị trí từ phiếu kiểm kê", "P0",
     "KK-2 như trên",
     "1. XL bấm \"Tạo phiếu điều chuyển vị trí\"\n"
     "2. Lập và hoàn tất phiếu điều chuyển đủ 2 cái của dòng L01\n"
     "3. Mở lại Chi tiết KK-2",
     "—",
     "- Mở tab mới màn tạo Phiếu điều chuyển vị trí, đã gắn sẵn dòng thiếu của KK-2\n"
     "- Sau khi điều chuyển đủ (KK-2 chỉ có dòng thiếu này): KK-2 TỰ chuyển Hoàn thành, kế hoạch gốc cũng Hoàn thành\n"
     "- Nếu KK-2 còn dòng thiếu khác chưa xử lý: KK-2 vẫn Chờ xử lý"),

    ("020", "Bấm Hoàn thành ở phiếu Chờ xử lý", "P0",
     "KK-2 Chờ xử lý, lập từ kế hoạch KH-11; dòng thiếu duy nhất đã được tích Tổng kiểm kê (không điều chuyển)",
     "1. XL bấm \"Hoàn thành\"\n"
     "2. Xem KK-2 và KH-11",
     "—",
     "- \"Thao tác thành công!\", về danh sách Phiếu của tôi\n"
     "- KK-2 Hoàn thành\n"
     "- Mong đợi: KH-11 Hoàn thành; Lưu ý: code hiện tại KH-11 vẫn Đã lập kiểm kê — nếu vậy ghi Failed"),

    ("021", "Hàng thừa không phát sinh bước xử lý", "P1",
     KK1 + "\nChỉ có dòng L07 thừa 2, không dòng nào thiếu",
     "1. BKS Duyệt kết quả",
     "—",
     "- KK-1 Hoàn thành ngay, không qua Chờ xử lý\n"
     "- Lưu ý: số thừa không tự điều chỉnh tồn — ghi nhận cho nghiệp vụ"),

    ("022", "Không có chức năng Hủy phiếu", "P2",
     "Có phiếu ở đủ 5 trạng thái",
     "1. Bấm bánh răng và mở Chi tiết từng phiếu",
     "—",
     "- Không có nút Hủy ở đâu cả"),
]


SEC_VI = [
    ("001", "Xóa phiếu nháp", "P0",
     "KK-4 Đang tạo do TK1 lập",
     "1. Bấm bánh răng KK-4 > Xóa\n"
     "2. Bấm \"Xác nhận\"",
     "—",
     "- Hộp \"Xác nhận xóa!\", nội dung \"Bạn chắc chắn muốn xóa bản ghi này?\", nút Xác nhận và Hủy\n"
     "- \"Xóa thành công!\", KK-4 biến mất, ở lại đúng lối vào"),

    ("002", "Bấm Hủy ở hộp xác nhận", "P1",
     "KK-4 Đang tạo",
     "1. Bấm Xóa rồi bấm \"Hủy\"",
     "—",
     "- KK-4 còn nguyên"),

    ("003", "Phiếu đã gửi không có nút Xóa", "P0",
     "TK1 có phiếu ở Đang kiểm, Chờ duyệt kết quả, Chờ xử lý, Hoàn thành",
     "1. Bấm bánh răng từng phiếu",
     "—",
     "- Không có Xóa"),

    ("004", "Xóa phiếu nháp lập từ kế hoạch", "P1",
     "KK-4 Đang tạo lập từ KH-12; KH-12 đang Đã lập kiểm kê",
     "1. Xóa KK-4\n"
     "2. Xem KH-12 trên danh sách kế hoạch",
     "—",
     "- Mong đợi: KH-12 về Đang kiểm để lập lại phiếu\n"
     "- Lưu ý: code hiện tại KH-12 vẫn Đã lập kiểm kê, không lập lại được — nếu vậy ghi Failed"),
]


SEC_VII = [
    ("001", "In 1 phiếu đã nhập kết quả", "P0",
     "KK-5 Hoàn thành, lập từ KH-3, Ngày kiểm kê 01/10/2026, kho K1, hội đồng Nguyễn Văn K và Trần Thị L\n"
     "Dòng L01 thực kiểm 8 / SL 10, ghi chú \"Rơi vỡ\"; Ghi chú duyệt \"Đã đối chiếu\"",
     "1. Bấm bánh răng KK-5 > In",
     "—",
     "- Tab mới khổ ngang, tiêu đề \"KIỂM KÊ THEO VỊ TRÍ\"\n"
     "- Có Số phiếu, Ngày kiểm kê 01/10/2026, Kế hoạch kiểm kê = mã KH-3, Kho vật lý, Hội đồng \"Nguyễn Văn K; Trần Thị L\"\n"
     "- Bảng: STT, Nhà Kho, Vị trí, Tên hàng, Mã hàng, ĐVT, SL tồn, Công ty, Lô, SL, ĐVT kiểm kê, Thực kiểm, Ghi chú\n"
     "- Thực kiểm 8 tô ĐỎ, ghi chú \"Rơi vỡ\" chữ đỏ\n"
     "- Nhận xét, đánh giá = \"Đã đối chiếu\"; ngày ký cuối trang = 01/10/2026\n"
     "- Lưu ý: không có cột Chênh lệch, Tổng kiểm kê; cột Nhà Kho in mã kho"),

    ("002", "In phiếu chưa nhập kết quả", "P1",
     "KK-4 Đang tạo",
     "1. In KK-4",
     "—",
     "- In được; cột Thực kiểm để trống"),

    ("003", "Xuất excel 1 phiếu", "P0",
     "KK-5 như TC_07.001",
     "1. Bấm bánh răng KK-5 > Xuất excel, mở file",
     "—",
     "- File tên kiem_ke_theo_vi_tri_<Số phiếu>.xlsx\n"
     "- Nội dung khớp bản In"),

    ("004", "In danh sách", "P0",
     "Lối vào menu lọc Kho = K1 ra 3 phiếu, CẢ 3 đều lập từ kế hoạch",
     "1. Bấm nút \"In\" trên hàng nút",
     "Kho: K1",
     "- Bảng: STT, Số phiếu, Kế hoạch KK, Ngày kiểm kê, Kho, Người lập, Người duyệt, Ngày duyệt, Trạng thái\n"
     "- Đúng 3 dòng"),

    ("005", "Xuất excel danh sách lấy hết, không theo phân trang", "P0",
     "Phạm vi có 23 phiếu đều lập từ kế hoạch",
     "1. Bấm nút \"Xuất excel\", mở file",
     "—",
     "- File tên danh_sach_phieu_kiem_ke_theo_vi_tri.xlsx, tiêu đề \"Danh sách phiếu kiểm kê theo vị trí\"\n"
     "- Đủ 23 dòng"),

    ("006", "In / Xuất excel danh sách khi có phiếu lập độc lập", "P0",
     "Kết quả lọc có 3 phiếu, trong đó KK-8 lập độc lập (không gắn kế hoạch)",
     "1. Bấm \"In\"\n"
     "2. Bấm \"Xuất excel\"",
     "—",
     "- Mong đợi: in / xuất đủ 3 dòng, cột Kế hoạch KK của KK-8 để trống\n"
     "- Lưu ý: code hiện tại dễ báo lỗi hệ thống — nếu vậy ghi Failed"),

    ("007", "In danh sách từ lối vào chờ duyệt", "P1",
     "BKS có 2 phiếu chờ duyệt",
     "1. Mở lối vào chờ duyệt, bấm In",
     "—",
     "- Chỉ 2 phiếu Chờ duyệt kết quả"),
]


SEC_VIII = [
    ("001", "Lưu khi chưa chọn kho, chưa lấy vị trí, chưa có thành viên", "P0",
     "Màn Tạo mới trống",
     "1. Bấm \"Lưu\"",
     "—",
     "- Thông báo vàng \"Tạo thất bại!\"\n"
     "- Chữ đỏ (tiếng Anh) dưới ô Kho vật lý, dưới bảng chi tiết, dưới bảng hội đồng\n"
     "- Không tạo phiếu"),

    ("002", "Bấm Lấy vị trí khi chưa tích vị trí", "P1",
     "Đã chọn kho K1",
     "1. Bấm \"Lấy vị trí\"",
     "—",
     "- Cảnh báo \"Chưa chọn đủ thông tin vị trí!\""),

    ("003", "Thành viên trùng", "P0",
     "Hội đồng có 2 dòng cùng NV-K",
     "1. Bấm \"Lưu\"",
     "—",
     "- \"Tạo thất bại!\", chữ đỏ báo trùng dưới ô Thành viên"),

    ("004", "Lỗi trên màn Sửa", "P1",
     "KK-4 Đang tạo",
     "1. Mở Sửa, bớt hết thành viên, bấm \"Lưu\"",
     "—",
     "- \"Thao tác thất bại!\", KK-4 không đổi"),

    ("005", "Xóa trống ô Thực kiểm", "P0",
     KK3,
     "1. Xóa trắng Thực kiểm dòng L01\n"
     "2. Quan sát Chênh lệch",
     "Thực kiểm L01: (trống)",
     "- Thực kiểm được coi là 0, Chênh lệch = -10\n"
     "- Không ghi chú thì Lưu kết quả báo \"Thao tác thất bại!\"\n"
     "- Lưu ý: tester xác nhận nghiệp vụ có chấp nhận \"trống = 0\""),

    ("006", "Nhập Thực kiểm có dấu phẩy", "P0",
     KK3,
     "1. Gõ \"2,5\" vào Thực kiểm dòng L07\n"
     "2. Gõ \"2.5\"",
     "Thực kiểm L07: 2,5 rồi 2.5",
     "- \"2,5\": hệ thống hiểu thành 25, Chênh lệch = 20\n"
     "- \"2.5\": Chênh lệch = -2.5\n"
     "- Lưu ý: dấu phẩy là ngăn cách hàng nghìn — dễ nhập sai, ghi nhận"),

    ("007", "Nhập Thực kiểm là chữ hoặc số âm", "P1",
     KK3,
     "1. Gõ \"abc\" vào Thực kiểm dòng L01\n"
     "2. Gõ \"-3\"",
     "Thực kiểm L01: abc / -3",
     "- Mong đợi: không chấp nhận chữ, không chấp nhận số âm\n"
     "- Ghi lại hệ thống xử lý thế nào; lưu được số âm thì ghi Failed"),

    ("008", "Thực kiểm số lớn hiển thị ngăn cách hàng nghìn", "P2",
     KK3,
     "1. Gõ 1250 vào Thực kiểm dòng L02",
     "Thực kiểm L02: 1250",
     "- Ô hiện \"1,250\", Chênh lệch = 1235"),

    ("009", "Nhiều dòng chênh lệch, chỉ một dòng thiếu Ghi chú", "P1",
     KK3 + "\nĐã đính kèm file",
     "1. Sửa L01 = 8 có ghi chú, L07 = 7 không ghi chú\n"
     "2. Bấm \"Lưu kết quả\"\n"
     "3. Bổ sung ghi chú L07, lưu lại",
     "—",
     "- Bước 2: \"Thao tác thất bại!\", các số đã nhập vẫn còn\n"
     "- Bước 3: \"Cập nhật thành công\""),

    ("010", "Phiếu có lô SL lẻ nhỏ hơn 1", "P2",
     "Vị trí P6 có hàng tính theo mét, lô L09 tồn 0,5",
     "1. Lập phiếu độc lập, tích P6, Lấy vị trí, thêm thành viên, bấm \"Lưu\"",
     "—",
     "- Lưu được (khác với Kế hoạch kiểm kê, nơi SL lẻ bị chặn)"),
]


SEC_IX = [
    ("001", "Phiếu ghi nhận công ty của người lập", "P0",
     "TK1 công ty 1 lập KK-9; C có quyền xem theo công ty, thuộc công ty 3",
     "1. C tìm KK-9 bằng Mã phiếu",
     "—",
     "- C không tìm thấy KK-9"),

    ("002", "Hai thủ kho cùng lập phiếu từ một kế hoạch", "P0",
     "KH-3 Đang kiểm kho K1; TK1 và TK5 đều là thủ kho K1, có quyền Lập phiếu",
     "1. TK1 và TK5 cùng mở màn lập phiếu từ KH-3\n"
     "2. TK1 bấm Lưu, sau đó TK5 bấm Lưu",
     "—",
     "- Mong đợi: chỉ 1 phiếu được tạo cho KH-3\n"
     "- Lưu ý: bước lưu không kiểm tra kế hoạch đã có phiếu — nếu tạo được 2 phiếu thì ghi Failed"),

    ("003", "Hai cửa sổ cùng Lưu kết quả", "P1",
     KK3 + "\nTK1 mở Nhập kết quả KK-3 ở 2 tab",
     "1. Tab 1 nhập L01 = 8, Lưu kết quả\n"
     "2. Tab 2 (chưa tải lại) nhập L01 = 9, Lưu kết quả",
     "—",
     "- Mong đợi: tab 2 bị từ chối vì phiếu đã chuyển Chờ duyệt kết quả\n"
     "- KK-3 giữ L01 = 8"),

    ("004", "Hai Ban kiểm soát xử lý cùng một phiếu", "P1",
     KK1 + "\nBKS và BKS2 cùng mở Chi tiết KK-1",
     "1. BKS bấm Duyệt kết quả\n"
     "2. BKS2 (chưa tải lại) bấm Không duyệt có ghi chú",
     "—",
     "- BKS2 bị báo \"Không có quyền\" (phiếu đã rời bước chờ duyệt)\n"
     "- KK-1 giữ kết quả của BKS"),

    ("005", "Tồn kho đổi sau khi lập phiếu", "P2",
     KK3 + "\nSau khi KK-3 được lưu, kho xuất 3 cái HH-0091 khỏi P1",
     "1. TK1 Nhập kết quả KK-3, đọc SL các lô",
     "—",
     "- SL vẫn là số lúc lưu phiếu (10, 15, 5), không tự cập nhật"),

    ("006", "Ban kiểm soát duyệt được phiếu công ty khác", "P1",
     "BKS thuộc công ty 1; KK-10 Chờ duyệt kết quả của công ty 3",
     "1. BKS mở lối vào chờ duyệt, tìm KK-10, bấm Duyệt kết quả",
     "—",
     "- Theo code hiện tại: thấy và duyệt được KK-10\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu duyệt theo công ty"),
]


SEC_X = [
    ("001", "Luồng chuẩn: khớp số, hoàn thành ngay", "P0",
     "KH-3 Đang kiểm kho K1; TK1 thủ kho K1 có quyền Lập phiếu; BKS cùng công ty\n" + P1,
     "1. TK1 lập phiếu từ KH-3, bấm Lưu & Gửi\n"
     "2. TK1 Nhập kết quả, giữ nguyên Thực kiểm, đính kèm bienban.pdf, Lưu kết quả\n"
     "3. BKS bấm thông báo, Duyệt kết quả\n"
     "4. In và Xuất excel phiếu",
     "—",
     "- Phiếu lần lượt: Đang kiểm, Chờ duyệt kết quả, Hoàn thành\n"
     "- KH-3 lần lượt: Đã lập kiểm kê, Hoàn thành\n"
     "- Bản In, Excel khớp màn Chi tiết"),

    ("002", "Luồng có hàng thiếu, xử lý bằng điều chuyển vị trí", "P0",
     "Như TC_10.001; XL có quyền Xử lý phiếu kiểm kê vị trí",
     "1. TK1 lập phiếu, Lưu & Gửi, nhập L01 = 8 ghi chú \"Thiếu 2\", đính kèm file, Lưu kết quả\n"
     "2. BKS Duyệt kết quả\n"
     "3. XL nhận thông báo, Tạo phiếu điều chuyển vị trí cho 2 cái, hoàn tất điều chuyển\n"
     "4. Xem phiếu kiểm kê và KH-3",
     "Thực kiểm L01: 8",
     "- Sau bước 2: phiếu Chờ xử lý, XL nhận thông báo\n"
     "- Sau bước 3: phiếu kiểm kê TỰ chuyển Hoàn thành, không cần bấm nút\n"
     "- KH-3 Hoàn thành"),

    ("003", "Luồng có thiếu, xử lý bằng Tổng kiểm kê", "P1",
     "Như TC_10.002 đến hết bước 2",
     "1. XL tích Tổng kiểm kê dòng L01\n"
     "2. Bấm Hoàn thành",
     "—",
     "- Không cần tạo phiếu điều chuyển; phiếu Hoàn thành"),

    ("004", "Luồng bị Không duyệt rồi nhập lại", "P0",
     "Như TC_10.001 đến hết bước 2",
     "1. BKS Không duyệt, ghi chú \"Đếm lại\"\n"
     "2. TK1 nhận thông báo, Nhập kết quả lại (không chọn file mới), Lưu kết quả\n"
     "3. BKS Duyệt kết quả",
     "—",
     "- Phiếu: Chờ duyệt kết quả, Đang kiểm, Chờ duyệt kết quả, Hoàn thành\n"
     "- BKS nhận thông báo cần duyệt cả 2 lần"),

    ("005", "Luồng phiếu lập độc lập", "P1",
     "TK1 thủ kho K1; không dùng kế hoạch",
     "1. Tạo mới, chọn K1, tích P1, Lấy vị trí, thêm hội đồng, Lưu & Gửi\n"
     "2. Nhập kết quả, Lưu kết quả; BKS Duyệt",
     "—",
     "- Phiếu đi hết luồng tới Hoàn thành\n"
     "- Ô Kế hoạch kiểm kê trống; Ngày kiểm kê = ngày lập phiếu\n"
     "- Không kế hoạch nào bị đổi trạng thái"),
]
