# -*- coding: utf-8 -*-
"""Section VI - XI - duyet, xu ly, xoa / in / excel, rang buoc, co lap & dong thoi, luong dau - cuoi."""

PDC = "Phiếu điều chuyển vị trí"

SEC_VI = [
    ("001", "Duyệt phiếu không chênh lệch thì Hoàn thành", "P0",
     "KK-3 Chờ KT duyệt, mọi dòng Thực kiểm bằng tồn",
     "1. BKS mở Chi tiết KK-3, nhập Ghi chú duyệt \"OK\"\n"
     "2. Bấm Duyệt",
     "Ghi chú duyệt: OK",
     "- Báo \"Thao tác thành công\"\n"
     "- KK-3 Hoàn thành (nhãn xanh), Người duyệt là BKS\n"
     "- Chi tiết hiện Ghi chú duyệt \"OK\""),

    ("002", "Duyệt phiếu có chênh lệch thì Chờ xử lý", "P0",
     "KK-3 Chờ KT duyệt, L01 chênh lệch -2; XL có quyền Xử lý phiếu kiểm kê hàng hóa",
     "1. BKS bấm Duyệt KK-3",
     "—",
     "- KK-3 Chờ xử lý\n"
     "- XL nhận thông báo \"Bạn có 1 phiếu kiểm kê hàng hóa cần xử lý\""),

    ("003", "Chỉ cần một dòng chênh lệch là phải xử lý", "P1",
     "Phiếu 5 hàng, chỉ 1 dòng lẻ chênh lệch +1",
     "1. BKS bấm Duyệt",
     "—",
     "- Phiếu Chờ xử lý"),

    ("004", "Không duyệt bắt buộc Ghi chú duyệt", "P0",
     "KK-3 Chờ KT duyệt",
     "1. BKS để trống Ghi chú duyệt, bấm Không duyệt",
     "—",
     "- Báo \"Thao tác thất bại!\", lỗi tiếng Anh \"The comment field is required.\"\n"
     "- KK-3 vẫn Chờ KT duyệt"),

    ("005", "Không duyệt có lý do", "P0",
     "KK-3 Chờ KT duyệt do NV-A lập",
     "1. BKS nhập Ghi chú duyệt \"Đếm lại P1\", bấm Không duyệt",
     "Ghi chú duyệt: Đếm lại P1",
     "- Báo \"Thao tác thành công\", KK-3 Không duyệt\n"
     "- NV-A nhận thông báo \"<tên BKS> đã từ chối duyệt phiếu kiểm kê hàng hóa của bạn\"\n"
     "- NV-A thấy lại \"Cập nhật kết quả\""),

    ("006", "Phiếu đã duyệt không duyệt lại được", "P1",
     "KK-3 đã Hoàn thành",
     "1. BKS mở Chi tiết KK-3\n"
     "2. Gọi thẳng chức năng Không duyệt KK-3",
     "—",
     "- Không có nút Duyệt / Không duyệt\n"
     "- Gọi thẳng báo \"Bạn không có quyền duyệt phiếu này\""),

    ("007", "Duyệt phiếu của công ty khác", "P2",
     "BKS thuộc công ty 1; KK-6 của công ty 3 Chờ KT duyệt",
     "1. BKS mở ô chờ duyệt, tìm KK-6, bấm Duyệt",
     "—",
     "- Theo code hiện tại: duyệt được\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ chỉ cho duyệt phiếu công ty mình"),

    ("008", "Ô Ghi chú duyệt bị khóa với người không duyệt", "P2",
     "KK-3 Chờ KT duyệt; NV-A là người lập",
     "1. NV-A mở Chi tiết KK-3",
     "—",
     "- Ô Ghi chú duyệt bị khóa"),
]


SEC_VII = [
    ("001", "Lệch vị trí cần Phiếu điều chuyển vị trí", "P0",
     "KK-4 Chờ xử lý: H1 thiếu 2 ở P1 (L01), thừa 2 ở P2 (L02), tổng chênh lệch của H1 = 0",
     "1. XL mở Xử lý KK-4\n"
     "2. Quan sát nút cuối trang",
     "—",
     "- Có nút \"Tạo phiếu điều chuyển vị trí\"\n"
     "- KHÔNG có nút tạo phiếu nhập / xuất kho"),

    ("002", "Tạo điều chuyển đủ số thì phiếu kiểm kê Hoàn thành", "P0",
     "KK-4 như TC_07.001",
     "1. XL bấm \"Tạo phiếu điều chuyển vị trí\"\n"
     "2. Ở " + PDC + " điền sẵn, chuyển 2 từ P1 sang P2 (nơi hàng thực sự nằm), bấm Điều chuyển\n"
     "3. Xem lại KK-4",
     "—",
     "- " + PDC + " điền sẵn dòng thiếu của KK-4\n"
     "- Sau bước 2: KK-4 Hoàn thành, nút xử lý biến mất"),

    ("003", "Thiếu thật cần phiếu xuất kho điều chỉnh kiểm kê", "P0",
     "KK-4 Chờ xử lý: H1 thiếu 2 ở P1, không thừa ở đâu (tổng -2)",
     "1. XL mở Xử lý KK-4",
     "—",
     "- Có nút \"Tạo phiếu xuất kho điều chuyển\"\n"
     "- Bấm vào mở màn tạo phiếu xuất kho điều chỉnh kiểm kê gắn KK-4\n"
     "- Lưu ý: nhãn nút ghi \"điều chuyển\" nhưng là phiếu điều chỉnh kiểm kê - ghi Failed nếu cần đổi tên"),

    ("004", "Thừa thật cần phiếu nhập kho điều chỉnh kiểm kê", "P0",
     "KK-4 Chờ xử lý: H1 thừa 1 ở P2 (tổng +1)",
     "1. XL mở Xử lý KK-4",
     "—",
     "- Có nút \"Tạo phiếu nhập kho điều chuyển\", mở màn tạo phiếu nhập kho điều chỉnh kiểm kê gắn KK-4"),

    ("005", "Phiếu vừa thừa vừa thiếu hiện cả hai nút", "P1",
     "KK-4: H1 thiếu 2 (tổng -2); H3 thừa 1 (tổng +1)",
     "1. XL mở Xử lý KK-4",
     "—",
     "- Có cả nút tạo phiếu nhập kho và nút tạo phiếu xuất kho"),

    ("006", "Mỗi loại chứng từ xử lý chỉ tạo một lần", "P0",
     "KK-4 thiếu H1 tổng -2 và H3 tổng -1; XL đã tạo phiếu xuất kho cho H1 nhưng chưa xử lý H3",
     "1. XL mở lại Xử lý KK-4",
     "—",
     "- Nút \"Tạo phiếu xuất kho điều chuyển\" KHÔNG còn hiện\n"
     "- Lưu ý: H3 không còn đường xử lý trên màn này - ghi lại thực tế"),

    ("007", "Xử lý một phần thì phiếu Đang xử lý", "P0",
     "KK-4 thiếu 2 dòng; phiếu nhập / xuất kho chỉ xử lý 1 dòng",
     "1. Hoàn tất chứng từ xử lý cho 1 dòng\n"
     "2. Xem KK-4",
     "—",
     "- KK-4 Đang xử lý, vẫn có Xử lý trong menu bánh răng"),

    ("008", "Xử lý đủ mọi dòng thì phiếu Hoàn thành", "P0",
     "KK-4 Đang xử lý, còn 1 dòng chênh lệch",
     "1. Hoàn tất chứng từ xử lý cho dòng còn lại\n"
     "2. Xem KK-4",
     "—",
     "- KK-4 Hoàn thành, menu chỉ còn In, Xuất excel"),

    ("009", "Lưu nháp chứng từ xử lý có làm phiếu kiểm kê Hoàn thành không", "P1",
     "KK-4 thừa H1 tổng +1; XL tạo phiếu nhập hàng điều chỉnh kiểm kê đủ số nhưng chỉ Lưu nháp",
     "1. Xem KK-4 sau khi lưu nháp\n"
     "2. Kiểm tra tồn H1",
     "—",
     "- Mong đợi: KK-4 vẫn Đang xử lý cho đến khi phiếu nhập hoàn tất\n"
     "- Lưu ý: theo code hiện tại số đã xử lý được cộng ngay khi lưu nháp, KK-4 có thể Hoàn thành trong "
     "khi tồn chưa đổi - ghi lại thực tế"),

    ("010", "Hàng thừa khác không có đường xử lý", "P1",
     "KK-4 chỉ có hàng thừa khác H9 = 3, các dòng khác không chênh lệch",
     "1. BKS Duyệt KK-4\n"
     "2. Xem trạng thái",
     "—",
     "- Theo code hiện tại: KK-4 Hoàn thành ngay, H9 không được nhập kho\n"
     "- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu xử lý hàng thừa khác"),

    ("011", "Phiếu Hoàn thành có trên báo cáo hàng thừa thiếu", "P2",
     "KK-4 Hoàn thành, lập từ Kế hoạch tổng kiểm kê TKK-1, H1 thiếu 2",
     "1. Mở Báo cáo hàng thừa thiếu sau tổng kiểm kê hàng hóa, chọn TKK-1",
     "—",
     "- Có dòng H1, SL thiếu 2, Phiếu kiểm kê KK-4"),
]


SEC_VIII = [
    ("001", "Xóa phiếu nháp của mình", "P0",
     "KK-1 Đang tạo do NV-A lập",
     "1. NV-A bấm bánh răng > Xóa, đồng ý ở hộp xác nhận",
     "—",
     "- Báo \"Xóa thành công!\", KK-1 biến mất khỏi danh sách"),

    ("002", "Hủy ở hộp xác nhận xóa", "P2",
     "KK-1 Đang tạo",
     "1. Bấm Xóa, chọn hủy",
     "—",
     "- KK-1 còn nguyên"),

    ("003", "Xóa phiếu lập từ kế hoạch", "P1",
     "KK-1 Đang tạo lập từ KH-2 (KH-2 đang Đã lập phiếu kiểm kê)",
     "1. Xóa KK-1\n"
     "2. Xem KH-2 ở màn Kế hoạch kiểm kê theo hàng hóa",
     "—",
     "- Mong đợi: KH-2 về Đang kiểm để lập lại\n"
     "- Lưu ý: theo code hiện tại KH-2 vẫn Đã lập phiếu kiểm kê - ghi Failed"),

    ("004", "In một phiếu đã có kết quả", "P0",
     "KK-3 Chờ KT duyệt: L01 tồn 30, Thực kiểm 28, ghi chú \"vỡ 2\"",
     "1. Bấm bánh răng > In ở KK-3",
     "—",
     "- Khổ ngang, tiêu đề \"Phiếu kiểm kê theo mặt hàng\"\n"
     "- Bảng: STT, Tên hàng, Mã hàng, Vị trí, Công ty, Lô, SL tồn, ĐVT kiểm kê, Thực kiểm, Ghi chú\n"
     "- Thực kiểm 28 tô đỏ (khác tồn), Ghi chú \"vỡ 2\"\n"
     "- Không có phần Hàng thừa khác"),

    ("005", "In phiếu chưa có kết quả", "P1",
     "KK-2 Đang kiểm",
     "1. In KK-2",
     "—",
     "- Cột Thực kiểm để trống"),

    ("006", "Xuất excel một phiếu", "P0",
     "KK-3 như TC_08.004",
     "1. Bấm bánh răng > Xuất excel",
     "—",
     "- Tải về tệp phiếu kiểm kê, nội dung như bản In"),

    ("007", "In và Xuất excel danh sách theo bộ lọc", "P0",
     "Đang lọc Trạng thái Hoàn thành, có 3 kết quả",
     "1. Bấm In\n"
     "2. Bấm Xuất excel",
     "—",
     "- Bảng: STT, Số phiếu, Kế hoạch KK, Ngày kiểm kê, Kho, Người lập, Người duyệt, Ngày duyệt, Trạng thái\n"
     "- Đúng 3 dòng; tệp Excel tiêu đề \"Danh sách phiếu kiểm kê theo hàng hóa\""),

    ("008", "Cột Kế hoạch KK trên bản In danh sách", "P1",
     "Dòng 1 là phiếu lập từ KH-2, dòng 2 là phiếu tự do",
     "1. In danh sách, đọc cột Kế hoạch KK",
     "—",
     "- Mong đợi: dòng 2 để trống\n"
     "- Lưu ý: theo code hiện tại dòng 2 có thể hiện KH-2 - ghi Failed"),
]


SEC_IX = [
    ("001", "Lưu khi chưa chọn kho", "P0",
     "—",
     "1. Tạo mới, không chọn kho, bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", lỗi tiếng Anh dưới ô Kho"),

    ("002", "Lưu khi chưa có hàng", "P0",
     "—",
     "1. Tạo mới, chọn kho, thêm thành viên, không thêm hàng, bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", tab Hàng hóa đỏ, lỗi \"The products field is required.\""),

    ("003", "Lưu khi chưa có thành viên", "P0",
     "—",
     "1. Tạo mới, đủ kho và hàng, không thêm thành viên, bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", tab Hội đồng kiểm kê đỏ, lỗi \"The members field is required.\""),

    ("004", "Dòng thành viên chưa chọn người", "P1",
     "—",
     "1. Thêm 1 dòng thành viên để trống, bấm Lưu",
     "—",
     "- Lỗi \"The members.0.employee_id field is required.\" dưới ô Thành viên"),

    ("005", "Bỏ hết Công ty thuê kho", "P1",
     "—",
     "1. Tạo mới, chọn kho, xóa hết lựa chọn ở ô Công ty thuê kho, thêm hàng, bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", lỗi dưới ô Công ty thuê kho"),

    ("006", "Thu hẹp Công ty thuê kho", "P2",
     "Kho K1 có hàng H1 của TPE (L01) và ENE (L07) cùng vị trí P1",
     "1. Tạo mới, chọn K1, chỉ giữ Công ty thuê kho ENE\n"
     "2. Thêm H1",
     "—",
     "- Mong đợi: chỉ hiện lô L07 của ENE\n"
     "- Lưu ý: theo code hiện tại vị trí P1 vẫn hiện cả lô của TPE - ghi lại thực tế"),

    ("007", "Sửa phiếu mà bỏ hết thành viên", "P1",
     "KK-1 Đang tạo có 1 thành viên",
     "1. Mở Sửa KK-1, bớt thành viên, bấm Lưu",
     "—",
     "- Mong đợi: báo lỗi bắt buộc có thành viên\n"
     "- Lưu ý: theo code hiện tại có thể báo chung \"Đã có lỗi xảy ra\" - ghi lại thực tế"),

    ("008", "Ghi chú tối đa độ dài", "P2",
     "—",
     "1. Nhập Ghi chú 255 ký tự, Lưu\n"
     "2. Nhập Ghi chú 256 ký tự, Lưu",
     "—",
     "- 255 ký tự lưu được\n"
     "- 256 ký tự: mong đợi báo lỗi độ dài rõ ràng - ghi lại thực tế"),

    ("009", "Thực kiểm là chữ", "P1",
     "KK-2 Đang kiểm",
     "1. Nhập Thực kiểm \"abc\", Gửi duyệt",
     "Thực kiểm: abc",
     "- Không gửi được với giá trị chữ, báo \"Thao tác thất bại!\"\n"
     "- Ghi lại thực tế nếu hệ thống tự hiểu thành 0"),

    ("010", "Thực kiểm số âm", "P2",
     "KK-2 Đang kiểm",
     "1. Nhập Thực kiểm \"-5\", Gửi duyệt",
     "Thực kiểm: -5",
     "- Mong đợi: báo lỗi\n"
     "- Lưu ý: hệ thống không có ràng buộc số âm - ghi lại thực tế"),

    ("011", "Gọi thẳng chức năng Lưu với trạng thái không hợp lệ", "P2",
     "Tester kỹ thuật",
     "1. Gọi thẳng chức năng Lưu phiếu với trạng thái Hoàn thành",
     "—",
     "- Báo \"Tạo thất bại!\", chỉ chấp nhận Đang tạo hoặc Đang kiểm"),
]


SEC_X = [
    ("001", "Phiếu mang công ty của người lập", "P1",
     "NV-A công ty 1 lập KK-10",
     "1. Tài khoản quyền xem theo công ty ở công ty 1 và công ty 3 cùng tìm KK-10",
     "—",
     "- Công ty 1 thấy, công ty 3 không thấy"),

    ("002", "Hai người cùng lập phiếu từ một kế hoạch", "P0",
     "KH-2 Đang kiểm; TK1, TK2 có quyền Lập phiếu",
     "1. TK1, TK2 cùng mở form lập từ KH-2\n"
     "2. TK1 Lưu, rồi TK2 Lưu",
     "—",
     "- Mong đợi: TK2 bị từ chối\n"
     "- Lưu ý: theo code hiện tại cả hai lưu được, KH-2 có 2 phiếu - ghi Failed"),

    ("003", "Hai người duyệt cùng lúc", "P1",
     "KK-3 Chờ KT duyệt; BKS1, BKS2 cùng mở Chi tiết",
     "1. BKS1 bấm Duyệt\n"
     "2. BKS2 bấm Không duyệt trên trang đã mở",
     "—",
     "- BKS2 báo \"Bạn không có quyền duyệt phiếu này\", KK-3 giữ kết quả của BKS1"),

    ("004", "Gửi duyệt từ thẻ cũ sau khi đã gửi", "P1",
     "NV-A mở Cập nhật kết quả KK-2 ở 2 thẻ",
     "1. Thẻ 1 Gửi duyệt\n"
     "2. Thẻ 2 Gửi duyệt",
     "—",
     "- Thẻ 2 báo \"Bạn không có quyền cập nhật phiếu này\""),

    ("005", "Tạo hai chứng từ xử lý cùng lúc", "P2",
     "KK-4 Chờ xử lý cần phiếu xuất kho; XL1, XL2 cùng mở màn tạo phiếu xuất kho từ KK-4",
     "1. XL1 lưu, rồi XL2 lưu",
     "—",
     "- Mong đợi: XL2 bị từ chối vì KK-4 đã có phiếu xuất kho\n"
     "- Ghi lại thực tế số chứng từ được tạo"),

    ("006", "Sửa phiếu ở hai thẻ", "P2",
     "KK-1 Đang tạo, mở Sửa ở 2 thẻ",
     "1. Thẻ 1 đổi Ghi chú \"A\" Lưu, thẻ 2 đổi \"B\" Lưu",
     "—",
     "- Cả hai \"Sửa thành công\", Chi tiết hiện \"B\""),
]


SEC_XI = [
    ("001", "Luồng chuẩn không chênh lệch", "P0",
     "NV-A (thủ kho), BKS có quyền Ban kiểm soát cùng công ty",
     "1. NV-A tạo phiếu K1, H1, bấm Lưu & gửi\n"
     "2. NV-A Cập nhật kết quả, giữ Thực kiểm bằng tồn, đính file, Gửi duyệt\n"
     "3. BKS mở từ ô chờ duyệt ở Trang chủ, bấm Duyệt",
     "—",
     "- Sau bước 1: Đang kiểm\n"
     "- Sau bước 2: Chờ KT duyệt, ô chờ duyệt của BKS tăng 1\n"
     "- Sau bước 3: Hoàn thành, ô chờ duyệt giảm 1"),

    ("002", "Luồng có chênh lệch, không duyệt rồi xử lý", "P0",
     "NV-A, BKS, XL có quyền tương ứng",
     "1. NV-A lập từ kế hoạch KH-2, Lưu & gửi, nhập Thực kiểm L01 = 28 (thiếu 2), Gửi duyệt\n"
     "2. BKS Không duyệt, ghi \"Đếm lại\"\n"
     "3. NV-A nhập lại L01 = 27, Gửi duyệt\n"
     "4. BKS Duyệt\n"
     "5. XL tạo phiếu xuất kho điều chỉnh kiểm kê 3 cái H1 và hoàn tất",
     "—",
     "- KH-2: Đã lập phiếu kiểm kê sau bước 1\n"
     "- Sau bước 2: Không duyệt; bước 3: Chờ KT duyệt\n"
     "- Sau bước 4: Chờ xử lý, XL có thông báo\n"
     "- Sau bước 5: phiếu Hoàn thành, tồn H1 ở P1 giảm 3"),

    ("003", "Luồng lệch vị trí xử lý bằng điều chuyển", "P0",
     "Phiếu có H1 thiếu 2 ở P1, thừa 2 ở P2",
     "1. Gửi duyệt, BKS Duyệt\n"
     "2. XL bấm \"Tạo phiếu điều chuyển vị trí\", điều chuyển đủ 2\n"
     "3. Kiểm tra tồn H1",
     "—",
     "- Sau bước 1: Chờ xử lý, chỉ có nút điều chuyển\n"
     "- Sau bước 2: Hoàn thành\n"
     "- Tồn tổng H1 không đổi, chỉ đổi giữa P1 và P2"),

    ("004", "Phiếu kiểm kê Hoàn thành không đổi trạng thái kế hoạch", "P1",
     "Phiếu lập từ KH-2 vừa Hoàn thành",
     "1. Xem KH-2 ở màn Kế hoạch kiểm kê theo hàng hóa",
     "—",
     "- Mong đợi: KH-2 Hoàn thành\n"
     "- Lưu ý: theo code hiện tại KH-2 vẫn Đã lập phiếu kiểm kê - ghi Failed"),
]
