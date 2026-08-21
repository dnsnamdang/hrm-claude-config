# -*- coding: utf-8 -*-
"""Section V — day chuyen duyet nhieu cap va Khong duyet."""

SEC_V = [
    ("001", "Trưởng phòng duyệt phiếu", "P0",
     "TP-1 quản lý phòng P1; phiếu A do NV-A (phòng P1) lập, đang ở Chờ TP duyệt, 2 dòng đề nghị "
     "10.000.000 và 5.000.000",
     "1. Đăng nhập TP-1, mở màn Chờ duyệt, bấm Mã phiếu A\n"
     "2. Quan sát hàng nút và ô Ghi chú duyệt TP\n"
     "3. Nhập cột \"TP duyệt\" dòng 1 = 8.000.000, dòng 2 = 5.000.000\n"
     "4. Nhập Ghi chú duyệt TP, bấm nút TP Duyệt\n"
     "5. Đọc thông báo và quan sát trang chuyển tới",
     "TP duyệt: 8.000.000 + 5.000.000",
     "- Hàng nút có: TP Duyệt, Không duyệt, In, Xuất Excel, Quay lại\n"
     "- Ô Ghi chú duyệt TP mở, gõ được; 3 ô ghi chú còn lại khóa\n"
     "- ⚠️ KHÔNG có hộp thoại xác nhận khi bấm TP Duyệt\n"
     "- Thông báo \"Phiếu đề nghị thanh toán đã được gửi đến kế toán công nợ!\"\n"
     "- Hệ thống chuyển về màn Chờ duyệt, phiếu A rời khỏi danh sách của TP-1"),

    ("002", "Sau khi trưởng phòng duyệt, cột Ngày nhận và Số tiền cập nhật", "P0",
     "Vừa hoàn tất TC_05.001",
     "1. Mở màn danh sách chế độ Tất cả, tìm phiếu A\n"
     "2. Đọc cột Trạng thái, Ngày nhận, Số tiền",
     "—",
     "- Trạng thái: Chờ kế toán công nợ duyệt\n"
     "- Ngày nhận: ngày hôm nay\n"
     "- Số tiền: 13.000.000,00 (tổng cột TP duyệt), KHÔNG còn là 15.000.000"),

    ("003", "Thông báo sau khi trưởng phòng duyệt", "P1",
     "Vừa hoàn tất TC_05.001; KTCN-1 có quyền kế toán công nợ cùng công ty",
     "1. Đăng nhập KTCN-1, mở chuông thông báo\n"
     "2. Đăng nhập NV-A (người lập), mở chuông thông báo",
     "—",
     "- KTCN-1 nhận \"Bạn có một phiếu đề nghị thanh toán cần duyệt từ <tên NV-A>\"\n"
     "- NV-A nhận \"Đề nghị thanh toán bạn gửi đã được trưởng phòng duyệt\"\n"
     "- Bấm vào thông báo mở đúng màn chi tiết phiếu A"),

    ("004", "Trưởng phòng không duyệt được phiếu của phòng khác", "P0",
     "TP-1 quản lý phòng P1; phiếu B do người phòng P2 lập, đang ở Chờ TP duyệt",
     "1. Đăng nhập TP-1, mở màn Chờ duyệt, tìm phiếu B\n"
     "2. Dán thẳng đường dẫn chi tiết phiếu B",
     "—",
     "- Phiếu B KHÔNG có trong màn Chờ duyệt của TP-1\n"
     "- Mở thẳng chi tiết: hệ thống hiện trang báo không tìm thấy nội dung"),

    ("005", "Kế toán công nợ duyệt phiếu", "P0",
     "Phiếu A đang ở Chờ kế toán công nợ duyệt, cột TP duyệt là 8.000.000 và 5.000.000",
     "1. Đăng nhập KTCN-1, mở phiếu A từ màn Chờ duyệt\n"
     "2. Quan sát các cột tiền và ô ghi chú\n"
     "3. Nhập cột \"KT công nợ duyệt\" dòng 1 = 8.000.000, dòng 2 = 4.000.000\n"
     "4. Nhập Ghi chú duyệt KT công nợ, bấm KT công nợ duyệt",
     "KT công nợ duyệt: 8.000.000 + 4.000.000",
     "- Cột TP duyệt hiển thị đúng số trưởng phòng đã nhập, ở dạng chỉ đọc\n"
     "- Chỉ ô Ghi chú duyệt KT công nợ mở\n"
     "- Thông báo \"Phiếu đề nghị thanh toán đã được gửi đến kế toán trưởng!\"\n"
     "- Phiếu chuyển sang Chờ kế toán trưởng duyệt\n"
     "- Ngoài danh sách, cột Số tiền hiện 12.000.000,00"),

    ("006", "Thông báo sau khi kế toán công nợ duyệt", "P1",
     "Vừa hoàn tất TC_05.005",
     "1. Kiểm chuông thông báo của KTT-1, NV-A và TP-1",
     "—",
     "- KTT-1 nhận thông báo cần duyệt\n"
     "- NV-A nhận \"Đề nghị thanh toán bạn gửi đã được kế toán công nợ duyệt\"\n"
     "- TP-1 (người duyệt bước trước) cũng nhận được thông báo"),

    ("007", "Kế toán trưởng có hai lựa chọn duyệt", "P0",
     "Phiếu A đang ở Chờ kế toán trưởng duyệt",
     "1. Đăng nhập KTT-1, mở phiếu A\n"
     "2. Quan sát hàng nút",
     "—",
     "- Có ĐỒNG THỜI 2 nút: \"KT Trưởng Duyệt\" và \"Chuyển duyệt BGĐ\"\n"
     "- Kèm nút Không duyệt, In, Xuất Excel, Quay lại\n"
     "- Ô Ghi chú duyệt KT trưởng mở"),

    ("008", "Kế toán trưởng duyệt thẳng bỏ qua ban giám đốc", "P0",
     "Phiếu A đang ở Chờ kế toán trưởng duyệt",
     "1. Nhập cột \"KT trưởng/BGD\" cho các dòng\n"
     "2. Bấm nút KT Trưởng Duyệt\n"
     "3. Đọc thông báo, kiểm trạng thái phiếu",
     "—",
     "- Thông báo \"Phiếu đề nghị thanh toán đã được gửi đến kế toán thanh toán!\"\n"
     "- Phiếu nhảy THẲNG sang Chờ tạo phiếu chi, BỎ QUA bước ban giám đốc\n"
     "- Người lập và kế toán công nợ nhận thông báo \"...đã được kế toán trưởng duyệt\""),

    ("009", "Kế toán trưởng chuyển duyệt ban giám đốc", "P0",
     "Phiếu C đang ở Chờ kế toán trưởng duyệt",
     "1. Bấm nút Chuyển duyệt BGĐ\n"
     "2. Đọc thông báo, kiểm trạng thái phiếu\n"
     "3. Đăng nhập BGD-1, mở màn Chờ duyệt",
     "—",
     "- Thông báo \"Phiếu đề nghị thanh toán đã được gửi đến ban giám đốc!\"\n"
     "- Phiếu chuyển sang Chờ ban giám đốc duyệt\n"
     "- BGD-1 thấy phiếu C trong màn Chờ duyệt và nhận thông báo\n"
     "- Người lập và kế toán công nợ nhận thông báo \"...đã được KT trưởng chuyển BGĐ duyệt\""),

    ("010", "Ban giám đốc duyệt", "P0",
     "Phiếu C đang ở Chờ ban giám đốc duyệt",
     "1. Đăng nhập BGD-1, mở phiếu C\n"
     "2. Quan sát hàng nút và ô Ghi chú duyệt BGĐ\n"
     "3. Nhập số cột KT trưởng/BGD, nhập Ghi chú duyệt BGĐ, bấm BGD Duyệt",
     "—",
     "- Hàng nút có BGD Duyệt, Không duyệt, In, Xuất Excel, Quay lại\n"
     "- Chỉ ô Ghi chú duyệt BGĐ mở\n"
     "- Thông báo \"Phiếu đề nghị thanh toán đã được gửi đến kế toán thanh toán!\"\n"
     "- Phiếu chuyển sang Chờ tạo phiếu chi\n"
     "- Kế toán trưởng và người lập nhận thông báo \"...đã được BGĐ duyệt\""),

    ("011", "Kế toán thanh toán tạo phiếu chi cho phiếu hình thức TM", "P0",
     "KTTT-1; phiếu D hình thức TM đang ở Chờ tạo phiếu chi",
     "1. Mở chi tiết phiếu D\n"
     "2. Quan sát hàng nút\n"
     "3. Bấm nút Tạo phiếu chi\n"
     "4. Quan sát màn mở ra, quay lại kiểm trạng thái phiếu D",
     "—",
     "- Hàng nút có \"Tạo phiếu chi\", Không duyệt, In, Xuất Excel, Quay lại\n"
     "- Chuyển sang màn tạo Phiếu chi, phiếu D đã gắn sẵn\n"
     "- Trạng thái phiếu D CHƯA đổi ở bước này"),

    ("012", "Kế toán thanh toán tạo phiếu ủy nhiệm chi cho phiếu hình thức CK", "P0",
     "KTTT-1; phiếu E hình thức CK đang ở Chờ tạo phiếu chi",
     "1. Mở chi tiết phiếu E, quan sát hàng nút\n"
     "2. Bấm nút Tạo phiếu ủy nhiệm chi",
     "—",
     "- Nút hiện là \"Tạo phiếu ủy nhiệm chi\", KHÔNG phải \"Tạo phiếu chi\"\n"
     "- Chuyển sang màn tạo Phiếu ủy nhiệm chi, phiếu E đã gắn sẵn"),

    ("013", "Không duyệt ở bước trưởng phòng", "P0",
     "TP-1; phiếu F đang ở Chờ TP duyệt",
     "1. Mở chi tiết phiếu F, kéo xuống khối \"Ghi chú không duyệt\"\n"
     "2. Nhập lý do \"Sai đối tượng nhận tiền\"\n"
     "3. Bấm nút Không duyệt\n"
     "4. Đọc hộp thoại, bấm Xác nhận\n"
     "5. Quan sát trang chuyển tới, mở lại phiếu F",
     "Lý do: Sai đối tượng nhận tiền",
     "- Khối \"Ghi chú không duyệt\" hiện ra và gõ được (chỉ với người đang có quyền ở bước hiện tại)\n"
     "- Hộp thoại tiêu đề \"Xác nhận!\", nội dung \"Bạn chắc chắn muốn thực hiện hành động này?\"\n"
     "- Sau khi xác nhận: thông báo thành công, hệ thống chuyển sang chế độ Đã xử lý\n"
     "- Phiếu F chuyển sang trạng thái Không duyệt, khối Ghi chú không duyệt lưu đúng lý do"),

    ("014", "Không duyệt khi để trống lý do", "P0",
     "TP-1; phiếu G đang ở Chờ TP duyệt, khối Ghi chú không duyệt để TRỐNG",
     "1. Bấm nút Không duyệt\n"
     "2. Bấm Xác nhận trên hộp thoại\n"
     "3. Quan sát",
     "Ghi chú không duyệt: để trống",
     "- ⚠️ Hộp thoại xác nhận VẪN hiện trước, chỉ sau khi Xác nhận mới báo lỗi\n"
     "- Hệ thống chặn, hiện lỗi đỏ ngay dưới khối Ghi chú không duyệt\n"
     "- Trạng thái phiếu KHÔNG đổi"),

    ("015", "Không duyệt không gửi thông báo cho ai", "P0",
     "TP-1 vừa Không duyệt phiếu F ở TC_05.013; NV-A là người lập",
     "1. Đăng nhập NV-A, mở chuông thông báo, đếm số thông báo mới\n"
     "2. Kiểm chuông của các tài khoản có quyền Kinh doanh đề nghị thanh toán",
     "—",
     "- ⚠️ Hiện trạng: KHÔNG ai nhận được thông báo, kể cả người lập phiếu. Người lập phải tự vào xem "
     "mới biết phiếu bị từ chối. Ghi nhận Failed\n"
     "- Kỳ vọng đúng: gửi thông báo cho người lập và các cấp đã duyệt trước đó"),

    ("016", "Không duyệt được ở mọi cấp trong dây chuyền", "P0",
     "4 phiếu đang lần lượt ở: Chờ TP duyệt · Chờ kế toán công nợ duyệt · Chờ kế toán trưởng duyệt · "
     "Chờ tạo phiếu chi",
     "1. Với mỗi phiếu, đăng nhập bằng tài khoản có quyền ở đúng bước đó\n"
     "2. Mở chi tiết, kiểm sự xuất hiện của nút Không duyệt và khối Ghi chú không duyệt\n"
     "3. Nhập lý do và bấm Không duyệt",
     "4 bước",
     "- Cả 4 bước đều có nút Không duyệt và khối Ghi chú không duyệt\n"
     "- Cả 4 phiếu đều chuyển sang trạng thái Không duyệt\n"
     "- Người lập sửa lại và gửi duyệt lại được từ đầu dây chuyền"),

    ("017", "Không có nút Không duyệt khi phiếu không ở bước của mình", "P0",
     "KTCN-1 (chỉ có quyền kế toán công nợ); phiếu đang ở Chờ kế toán trưởng duyệt nhưng KTCN-1 mở "
     "được vì đã duyệt bước trước",
     "1. Mở chi tiết phiếu đó\n"
     "2. Quan sát hàng nút và khối Ghi chú không duyệt",
     "—",
     "- KHÔNG có nút Không duyệt\n"
     "- Khối Ghi chú không duyệt chỉ hiện ở dạng chỉ đọc nếu phiếu đã từng bị từ chối, ngược lại không "
     "hiện\n"
     "- Chỉ còn In, Xuất Excel, Quay lại"),

    ("018", "Người lập sửa lại phiếu bị không duyệt và chạy lại dây chuyền", "P0",
     "Phiếu F trạng thái Không duyệt, do NV-A lập",
     "1. Đăng nhập NV-A, mở chi tiết phiếu F, đọc Ghi chú không duyệt\n"
     "2. Bấm Sửa, chỉnh lại nội dung\n"
     "3. Bấm Lưu và gửi duyệt\n"
     "4. Đăng nhập TP-1, mở màn Chờ duyệt",
     "—",
     "- Phiếu F quay lại Chờ TP duyệt\n"
     "- Xuất hiện lại trong màn Chờ duyệt của TP-1\n"
     "- Ghi chú không duyệt cũ VẪN còn trên phiếu — kiểm xem có gây nhầm lẫn không"),

    ("019", "Người duyệt sửa số tiền của từng dòng", "P0",
     "Phiếu H ở Chờ kế toán công nợ duyệt, 3 dòng, cột TP duyệt lần lượt 10.000.000 / 5.000.000 / "
     "2.000.000",
     "1. Đăng nhập KTCN-1, mở phiếu H\n"
     "2. Sửa cột KT công nợ duyệt: dòng 1 = 9.000.000, dòng 2 = 5.000.000, dòng 3 = 0\n"
     "3. Đọc dòng Tổng cộng\n"
     "4. Bấm KT công nợ duyệt, mở lại phiếu",
     "9.000.000 / 5.000.000 / 0",
     "- Dòng Tổng cộng cột KT công nợ duyệt hiện 14.000.000\n"
     "- Lưu xong mở lại vẫn đúng 3 số vừa nhập\n"
     "- Cột TP duyệt giữ nguyên, không bị ghi đè"),

    ("020", "Người duyệt sửa số tiền trên phiếu ngoại tệ", "P1",
     "Phiếu ngoại tệ USD tỷ giá 25.000, đang ở Chờ kế toán công nợ duyệt, 1 dòng",
     "1. Nhập cột KT công nợ duyệt = 1.000\n"
     "2. Đọc cột quy đổi VND ngay bên cạnh\n"
     "3. Lưu và mở lại",
     "1.000 USD, tỷ giá 25.000",
     "- Cột quy đổi VND hiện 25.000.000\n"
     "- Sau khi lưu, cả số nguyên tệ và số quy đổi giữ nguyên"),

    ("021", "Người duyệt không sửa được thông tin chung của phiếu", "P1",
     "KTCN-1 mở phiếu ở bước của mình",
     "1. Thử gõ vào ô Loại chi, Hình thức thanh toán, Loại tiền, Tỷ giá, Lý do chi\n"
     "2. Thử thêm hoặc xóa dòng chi tiết",
     "—",
     "- Mọi ô thông tin chung đều khóa\n"
     "- Không có nút thêm dòng và nút xóa dòng\n"
     "- Chỉ sửa được số tiền của cấp mình và ghi chú của cấp mình"),

    ("022", "Nút duyệt không hiện với người không có quyền cấp đó", "P0",
     "Phiếu đang ở Chờ kế toán trưởng duyệt; mở lần lượt bằng KTCN-1, BGD-1, KTTT-1 (những người mở "
     "được chi tiết)",
     "1. Với mỗi tài khoản, mở chi tiết phiếu và ghi lại hàng nút",
     "3 tài khoản",
     "- Không tài khoản nào thấy nút KT Trưởng Duyệt hoặc Chuyển duyệt BGĐ\n"
     "- Không tài khoản nào thấy nút Không duyệt\n"
     "- Chỉ còn In, Xuất Excel, Quay lại"),

    ("023", "Duyệt phiếu loại Chi trả lại khách hàng có phân bổ theo phiếu xuất hàng", "P1",
     "Phiếu loại Chi trả lại khách hàng, dòng chi tiết gắn hợp đồng nguyên tắc và có bảng phân bổ theo "
     "phiếu yêu cầu xuất hàng (nếu môi trường test không dựng được thì ghi Không áp dụng)",
     "1. Mở phiếu ở bước duyệt bất kỳ\n"
     "2. Quan sát bảng phân bổ bên trong dòng chi tiết\n"
     "3. Sửa số tiền của cấp mình lệch với tổng phân bổ, bấm nút duyệt",
     "—",
     "- Bảng phân bổ hiện các cột Số phiếu, Công nợ còn lại, Số tiền\n"
     "- Nếu hệ thống chặn thì hiện cảnh báo \"Tổng số tiền chi theo phiếu xuất hàng và số tiền đề nghị "
     "chi không khớp nhau!\"\n"
     "- ⚠️ Ghi nhận hành vi thực tế: có chặn hay không chặn"),

    ("024", "Chặn chi vượt số còn lại trên hợp đồng đã quyết toán", "P0",
     "Phiếu loại Chi thưởng thực hiện hợp đồng, dòng gắn hợp đồng ĐÃ QUYẾT TOÁN còn lại 5.000.000",
     "1. Người lập nhập Số tiền đề nghị chi = 8.000.000, bấm Lưu\n"
     "2. Đọc thông báo\n"
     "3. Sửa về 5.000.000, bấm Lưu lại\n"
     "4. Ở bước duyệt, người duyệt nhập số cấp mình = 8.000.000 rồi bấm nút duyệt",
     "8.000.000 trên nền còn lại 5.000.000",
     "- Bước 1: hệ thống chặn, thông báo dạng \"Hợp đồng <mã> đã quyết toán không thể chi vượt số "
     "lượng còn lại!\"\n"
     "- Bước 3: lưu được\n"
     "- Bước 4: cũng bị chặn với cùng thông báo\n"
     "- Hợp đồng CHƯA quyết toán thì không bị chặn"),
]
