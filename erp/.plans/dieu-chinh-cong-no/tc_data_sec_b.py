# -*- coding: utf-8 -*-
"""Section IV — tao moi / sua / xem chi tiet."""

SEC_IV = [
    ("001", "Bố cục màn Tạo mới", "P0",
     "Tài khoản bất kỳ, đang ở màn danh sách",
     "1. Bấm nút Tạo mới\n"
     "2. Quan sát khối Thông tin chung",
     "—",
     "- Tiêu đề trang \"Tạo phiếu yêu cầu điều chỉnh công nợ\"\n"
     "- Khối Thông tin chung có: Loại phiếu (bắt buộc), Người tạo, Phòng ban, Diễn giải (bắt buộc)\n"
     "- Người tạo và Phòng ban điền sẵn theo người đang đăng nhập và bị khóa\n"
     "- Góc phải khối hiện tên người đăng nhập và ngày hôm nay\n"
     "- KHÔNG có ô Mã phiếu (chỉ màn Sửa mới có)\n"
     "- Dưới cùng có 3 nút: Lưu, Lưu và gửi duyệt, Quay lại"),

    ("002", "Ô Loại tiền và Tỷ giá chỉ hiện với phiếu NCC", "P0",
     "Đang ở màn Tạo mới",
     "1. Để Loại phiếu = Điều chỉnh công nợ khách hàng, quan sát khối Thông tin chung\n"
     "2. Đổi sang Điều chỉnh công nợ NCC, quan sát lại",
     "2 loại phiếu",
     "- Phiếu khách hàng: KHÔNG có ô Loại tiền và ô Tỷ giá\n"
     "- Phiếu NCC: hiện thêm ô Loại tiền (bắt buộc) và ô Tỷ giá\n"
     "- Chọn loại tiền thì ô Tỷ giá tự điền theo tỷ giá của loại tiền đó trong danh mục"),

    ("003", "Bảng chi tiết đổi hoàn toàn theo Loại phiếu", "P0",
     "Đang ở màn Tạo mới",
     "1. Chọn Loại phiếu = Điều chỉnh công nợ khách hàng, ghi lại tiêu đề các cột\n"
     "2. Đổi sang Điều chỉnh công nợ NCC, ghi lại tiêu đề các cột",
     "2 loại phiếu",
     "- Phiếu khách hàng: hai nửa \"Điều chỉnh từ\" và \"Điều chỉnh đến\", mỗi nửa gồm Khách hàng, "
     "Hợp đồng/Đơn hàng, Số dư cuối kỳ, NVKD, Số tiền\n"
     "- Phiếu NCC: hai nửa gồm Nhà cung cấp, Hợp đồng mua, Số dư, Nhân viên, Số tiền\n"
     "- Cả 2 bảng đều có nút dấu cộng ở cột cuối để thêm dòng \"Điều chỉnh từ\""),

    ("004", "Phiếu NCC dùng ngoại tệ tách đôi cột Số dư và Số tiền", "P0",
     "Loại phiếu = Điều chỉnh công nợ NCC",
     "1. Chọn Loại tiền = VND, đếm số cột của mỗi nửa bảng\n"
     "2. Đổi Loại tiền sang USD, đếm lại và đọc tiêu đề cột",
     "VND → USD",
     "- VND: mỗi nửa có 1 cột Số dư và 1 cột Số tiền\n"
     "- USD: cột Số dư tách đôi (USD và VNĐ), cột Số tiền cũng tách đôi (USD và VNĐ)\n"
     "- Cột VNĐ tính theo tỷ giá của phiếu"),

    ("005", "Không đổi được Loại phiếu khi mở màn Sửa", "P0",
     "Phiếu P trạng thái Đang tạo loại khách hàng, do chính người đăng nhập lập",
     "1. Mở màn Sửa phiếu P\n"
     "2. Thử đổi ô Loại phiếu sang Điều chỉnh công nợ NCC",
     "—",
     "- Ô Loại phiếu bị KHÓA, không đổi được\n"
     "- ⚠️ Đúng thiết kế: đã lưu rồi thì không đổi loại phiếu"),

    ("006", "Thêm và xóa dòng Điều chỉnh từ", "P0",
     "Loại phiếu = Điều chỉnh công nợ khách hàng, bảng đang có 1 dòng",
     "1. Bấm dấu cộng ở cột cuối bảng 2 lần\n"
     "2. Đếm số dòng Điều chỉnh từ\n"
     "3. Bấm biểu tượng thùng rác ở dòng 2",
     "—",
     "- Sau bước 1 có 3 dòng Điều chỉnh từ\n"
     "- Xóa dòng 2 thì còn 2 dòng, dữ liệu 2 dòng còn lại không xáo trộn\n"
     "- Xóa dòng KHÔNG hỏi xác nhận"),

    ("007", "Thêm và xóa dòng Điều chỉnh đến trong một dòng Điều chỉnh từ", "P0",
     "Dòng Điều chỉnh từ số 1 đã chọn khách hàng và hợp đồng",
     "1. Bấm nút \"Thêm dòng\" ở nửa Điều chỉnh đến của dòng 1, 2 lần\n"
     "2. Đếm số dòng đến của dòng 1\n"
     "3. Bấm thùng rác ở dòng đến thứ 2\n"
     "4. Kiểm dòng Điều chỉnh từ số 2 có bị ảnh hưởng không",
     "—",
     "- Dòng 1 có 3 dòng đến; xóa còn 2\n"
     "- Dòng Điều chỉnh từ số 2 KHÔNG bị ảnh hưởng\n"
     "- Mỗi dòng Điều chỉnh từ quản lý danh sách dòng đến riêng"),

    ("008", "Chọn khách hàng cho dòng Điều chỉnh từ", "P0",
     "Loại phiếu = Điều chỉnh công nợ khách hàng, dòng 1 còn trống",
     "1. Bấm kính lúp ở ô Khách hàng của nửa Điều chỉnh từ\n"
     "2. Quan sát cửa sổ: tiêu đề, các cột, các ô tìm\n"
     "3. Chọn KH-001",
     "—",
     "- Cửa sổ tên \"Khách hàng\", 4 cột: STT, Mã khách hàng, Tên khách hàng, Loại khách hàng\n"
     "- Có 2 ô tìm: Mã khách hàng và Tên khách hàng\n"
     "- Chọn xong hiện thông báo xanh \"Thêm khách hàng thành công!\"\n"
     "- Ô hợp đồng của dòng đó bị xóa trắng vì khách hàng vừa đổi"),

    ("009", "Chưa chọn khách hàng mà bấm chọn hợp đồng", "P0",
     "Dòng Điều chỉnh từ còn trống, chưa chọn khách hàng",
     "1. Bấm kính lúp ở ô Hợp đồng/Đơn hàng\n"
     "2. Quan sát",
     "—",
     "- Hiện cảnh báo vàng \"Chưa chọn khách hàng\"\n"
     "- Cửa sổ chọn hợp đồng KHÔNG mở"),

    ("010", "Cửa sổ chọn hợp đồng chỉ hiện hợp đồng do chính mình lập", "P0",
     "Khách hàng KH-001 có 3 hợp đồng do NV-A lập và 4 hợp đồng do NV-B lập, tất cả đều đã qua bước tạo",
     "1. Đăng nhập NV-A, chọn KH-001, mở cửa sổ chọn hợp đồng, ghi lại các mã\n"
     "2. Đăng nhập NV-B, làm lại",
     "—",
     "- NV-A chỉ thấy đúng 3 hợp đồng của mình\n"
     "- NV-B chỉ thấy đúng 4 hợp đồng của mình\n"
     "- ⚠️ Quy tắc CÓ CHỦ ĐÍCH (mục 9 ghi chú 10), không phải mất dữ liệu"),

    ("011", "Cửa sổ chọn hợp đồng loại bỏ hợp đồng chưa qua bước tạo", "P0",
     "Người đăng nhập là người lập của: 2 hợp đồng KH-002 đã có hiệu lực, 1 hợp đồng còn Đang tạo, "
     "1 hợp đồng đã Từ chối",
     "1. Chọn KH-002 cho dòng Điều chỉnh từ\n"
     "2. Mở cửa sổ chọn hợp đồng, đối chiếu với 4 hợp đồng đã biết",
     "—",
     "- Chỉ hiện 2 hợp đồng đã có hiệu lực\n"
     "- Hợp đồng Đang tạo và hợp đồng Từ chối KHÔNG hiện"),

    ("012", "Chọn hợp đồng tự điền Số dư cuối kỳ và NVKD", "P0",
     "Cửa sổ chọn hợp đồng đang mở; hợp đồng HD-2026-001 có số dư 25.000.000",
     "1. Bấm chọn dòng HD-2026-001\n"
     "2. Quan sát dòng Điều chỉnh từ",
     "—",
     "- Hiện thông báo xanh \"Thêm thành công\", cửa sổ đóng\n"
     "- Ô hợp đồng hiện HD-2026-001\n"
     "- Cột Số dư cuối kỳ hiện 25.000.000, cột NVKD hiện tên nhân viên phụ trách hợp đồng"),

    ("013", "Ô tích Số dư có đầu kì và Số dư nợ đầu kì", "P1",
     "Dòng Điều chỉnh từ đã chọn hợp đồng nguyên tắc có số dư đầu kỳ",
     "1. Quan sát ô tích ở nửa Điều chỉnh từ, đọc nhãn kèm số\n"
     "2. Tích vào ô đó, quan sát các cột thay đổi\n"
     "3. Làm tương tự với ô tích ở nửa Điều chỉnh đến",
     "—",
     "- Nửa Điều chỉnh từ có ô tích ghi \"Số dư có đầu kì: <số>\"\n"
     "- Nửa Điều chỉnh đến có ô tích ghi \"Số dư nợ đầu kì: <số>\"\n"
     "- Tích vào thì cột Số dư và giới hạn số tiền đổi theo số dư đầu kỳ"),

    ("014", "Chọn nhà cung cấp và hợp đồng mua cho phiếu NCC", "P0",
     "Loại phiếu = Điều chỉnh công nợ NCC, Loại tiền = VND, dòng 1 còn trống",
     "1. Bấm kính lúp ở ô Nhà cung cấp của nửa Điều chỉnh từ\n"
     "2. Quan sát cửa sổ và chọn NCC-01\n"
     "3. Bấm kính lúp ở ô Hợp đồng mua\n"
     "4. Chọn một hợp đồng mua",
     "—",
     "- Cửa sổ nhà cung cấp có các cột: STT, Mã NCC, Tên NCC, Đối tượng\n"
     "- Chưa chọn nhà cung cấp mà bấm ô Hợp đồng mua thì cảnh báo \"Chưa chọn NCC\"\n"
     "- Chọn hợp đồng xong, cột Số dư tự điền theo số dư công nợ phải trả của hợp đồng đó"),

    ("015", "Nhà cung cấp không rõ không bắt buộc hợp đồng mua", "P1",
     "Danh mục có nhà cung cấp tên \"KHÁCH KHÔNG RÕ\"",
     "1. Loại phiếu = Điều chỉnh công nợ NCC, chọn nhà cung cấp \"KHÁCH KHÔNG RÕ\" cho dòng Điều chỉnh từ\n"
     "2. Bỏ trống ô Hợp đồng mua\n"
     "3. Điền số tiền và các ô còn lại, bấm Lưu",
     "—",
     "- Lưu được, hệ thống KHÔNG đòi chọn hợp đồng mua\n"
     "- Với nhà cung cấp khác thì bỏ trống hợp đồng mua sẽ bị chặn\n"
     "- ⚠️ Đây là ngoại lệ có chủ đích, không ghi Failed"),

    ("016", "Nút Chọn nhanh hợp đồng cho phiếu khách hàng", "P0",
     "Dòng Điều chỉnh từ đã chọn khách hàng, hợp đồng và số tiền 10.000.000",
     "1. Bấm nút \"Chọn nhanh\" ở nửa Điều chỉnh đến\n"
     "2. Trong cửa sổ, chọn khách hàng rồi bấm nút lọc\n"
     "3. Nhập số tiền phân bổ cho 2 hợp đồng: 6.000.000 và 4.000.000\n"
     "4. Bấm nút áp dụng",
     "6.000.000 + 4.000.000 = 10.000.000",
     "- Cửa sổ liệt kê hợp đồng của khách hàng đã chọn kèm số dư còn nợ\n"
     "- Chưa chọn khách hàng mà bấm lọc thì cảnh báo \"Chưa chọn khách hàng\"\n"
     "- Áp dụng xong, 2 dòng Điều chỉnh đến được thêm vào với đúng số tiền vừa nhập"),

    ("017", "Chọn nhanh cảnh báo khi tổng phân bổ vượt số tiền điều chỉnh từ", "P0",
     "Dòng Điều chỉnh từ có số tiền 10.000.000; cửa sổ Chọn nhanh đang mở",
     "1. Nhập số tiền phân bổ cho 2 hợp đồng: 8.000.000 và 5.000.000\n"
     "2. Bấm nút áp dụng",
     "Tổng phân bổ 13.000.000 trên nền 10.000.000",
     "- Hiện cảnh báo \"Tổng số tiền điều chỉnh đến không được lớn hơn số tiền điều chỉnh từ\"\n"
     "- Không dòng nào được thêm vào bảng"),

    ("018", "Chọn nhanh cảnh báo khi điều chỉnh vào hợp đồng không có nợ", "P1",
     "Cửa sổ Chọn nhanh đang mở; có hợp đồng số dư còn nợ bằng 0",
     "1. Nhập số tiền phân bổ vào hợp đồng đó\n"
     "2. Bấm nút áp dụng\n"
     "3. Đọc hộp thoại, bấm Hủy\n"
     "4. Bấm lại và Xác nhận",
     "—",
     "- Hiện hộp thoại hỏi xác nhận với nội dung \"Số tiền điều chỉnh vào hợp đồng không có nợ!\"\n"
     "- Bấm Hủy: không thêm dòng nào\n"
     "- Bấm Xác nhận: VẪN thêm dòng bình thường\n"
     "- ⚠️ Đây là cảnh báo hỏi ý kiến, không phải lỗi chặn"),

    ("019", "Nút Chọn nhanh hợp đồng mua cho phiếu NCC", "P0",
     "Phiếu NCC, dòng Điều chỉnh từ có số tiền 10.000.000",
     "1. Bấm nút Chọn nhanh ở nửa Điều chỉnh đến\n"
     "2. Gõ mã hợp đồng mua vào ô tìm khi CHƯA chọn nhà cung cấp\n"
     "3. Chọn nhà cung cấp rồi bấm nút lọc\n"
     "4. Nhập số tiền phân bổ vượt 10.000.000 rồi bấm áp dụng",
     "—",
     "- Bước 2: cảnh báo \"Phải chọn NCC trước\"\n"
     "- Chưa chọn nhà cung cấp mà bấm lọc: cảnh báo \"Chưa chọn NCC\"\n"
     "- Bước 4: dòng vượt bị đánh dấu lỗi \"Tổng số tiền vượt quá số tiền điều chỉnh từ\" và hiện cảnh "
     "báo chung, không thêm dòng nào"),

    ("020", "Chọn nhanh thay thế dòng cũ trùng hợp đồng", "P1",
     "Dòng Điều chỉnh từ đã có 1 dòng đến gắn hợp đồng HD-A với số tiền 3.000.000",
     "1. Mở Chọn nhanh, phân bổ lại cho chính HD-A số tiền 5.000.000\n"
     "2. Bấm áp dụng, đếm số dòng đến và đọc số tiền",
     "—",
     "- Dòng cũ gắn HD-A bị THAY THẾ, không bị nhân đôi\n"
     "- Số tiền của dòng đó là 5.000.000"),

    ("021", "Phiếu khách hàng cho phép tổng điều chỉnh đến nhỏ hơn", "P0",
     "Loại phiếu = Điều chỉnh công nợ khách hàng; dòng Điều chỉnh từ số tiền 10.000.000; 1 dòng đến số "
     "tiền 6.000.000",
     "1. Bấm Lưu\n"
     "2. Đọc thông báo và kiểm phiếu vừa tạo\n"
     "3. Mở lại phiếu, bấm Lưu và gửi duyệt",
     "Từ 10.000.000 · Đến 6.000.000",
     "- Cả 2 lần đều lưu thành công, KHÔNG bị chặn\n"
     "- ⚠️ Phiếu khách hàng chỉ cấm LỚN HƠN, cho phép nhỏ hơn — khác hẳn phiếu NCC"),

    ("022", "Phiếu khách hàng chặn tổng điều chỉnh đến lớn hơn", "P0",
     "Loại phiếu = Điều chỉnh công nợ khách hàng; dòng Điều chỉnh từ số tiền 10.000.000; 2 dòng đến "
     "số tiền 6.000.000 và 5.000.000",
     "1. Bấm Lưu\n"
     "2. Quan sát",
     "Tổng đến 11.000.000 trên nền 10.000.000",
     "- Không lưu\n"
     "- Hiện cảnh báo \"Tổng số tiền điều chỉnh đến không được lớn hơn số tiền điều chỉnh từ\"\n"
     "- Ở lại form, dữ liệu còn nguyên"),

    ("023", "Phiếu NCC lưu nháp không kiểm ràng buộc bằng nhau", "P0",
     "Loại phiếu = Điều chỉnh công nợ NCC; dòng Điều chỉnh từ số tiền 10.000.000; 1 dòng đến số tiền "
     "6.000.000",
     "1. Bấm nút Lưu (lưu nháp)\n"
     "2. Đọc thông báo và tìm phiếu vừa tạo",
     "Từ 10.000.000 · Đến 6.000.000",
     "- Lưu thành công, trạng thái Đang tạo\n"
     "- ⚠️ Ở bước này hệ thống CHƯA kiểm ràng buộc bằng nhau — đúng thiết kế"),

    ("024", "Phiếu NCC bắt buộc tổng điều chỉnh đến bằng khi gửi duyệt", "P0",
     "Vẫn phiếu ở TC_04.023, đang mở màn Sửa",
     "1. Bấm nút Lưu và gửi duyệt\n"
     "2. Đọc thông báo\n"
     "3. Sửa số tiền dòng đến thành 10.000.000, bấm Lưu và gửi duyệt lại",
     "Đến 6.000.000, rồi 10.000.000",
     "- Bước 1: không lưu, cảnh báo \"Tổng số tiền điều chỉnh đến phải bằng số tiền điều chỉnh từ\"\n"
     "- Bước 3: lưu thành công, phiếu chuyển sang Chờ tạo phiếu kế toán"),

    ("025", "Phiếu NCC gửi duyệt khi tổng đến lớn hơn cũng bị chặn", "P0",
     "Phiếu NCC; dòng Điều chỉnh từ 10.000.000; tổng dòng đến 12.000.000",
     "1. Bấm Lưu và gửi duyệt\n"
     "2. Quan sát",
     "—",
     "- Không lưu, cảnh báo \"Tổng số tiền điều chỉnh đến phải bằng số tiền điều chỉnh từ\"\n"
     "- Hệ thống chặn cả trường hợp lớn hơn lẫn nhỏ hơn"),

    ("026", "Phiếu NCC tạo từ báo có chỉ cần không lớn hơn", "P0",
     "Phiếu NCC được tạo từ Phiếu báo có; dòng Điều chỉnh từ 10.000.000; tổng dòng đến 6.000.000",
     "1. Bấm Lưu và gửi duyệt\n"
     "2. Đọc thông báo\n"
     "3. Sửa tổng dòng đến thành 12.000.000, bấm Lưu và gửi duyệt lại",
     "Đến 6.000.000, rồi 12.000.000",
     "- Bước 1: lưu THÀNH CÔNG (nhỏ hơn được chấp nhận)\n"
     "- Bước 3: bị chặn, cảnh báo \"Tổng số tiền điều chỉnh đến không được lớn hơn số tiền điều chỉnh "
     "từ\"\n"
     "- ⚠️ Ba tổ hợp khác nhau ở TC_04.021, TC_04.024 và ca này — kiểm đủ cả ba"),

    ("027", "Chặn hợp đồng điều chỉnh đến trùng điều chỉnh từ", "P0",
     "Phiếu khách hàng; dòng Điều chỉnh từ gắn hợp đồng HD-A của KH-001",
     "1. Ở dòng Điều chỉnh đến, chọn cùng KH-001 và cùng hợp đồng HD-A\n"
     "2. Nhập số tiền hợp lệ, bấm Lưu",
     "Cùng hợp đồng HD-A ở cả hai nửa",
     "- Không lưu\n"
     "- Hiện thông báo \"Hợp đồng điều chuyển đến trùng với điều chuyển từ\"\n"
     "- Đổi hợp đồng đến sang hợp đồng khác thì lưu được"),

    ("028", "Chặn hợp đồng mua trùng ở phiếu NCC", "P0",
     "Phiếu NCC; dòng Điều chỉnh từ gắn nhà cung cấp NCC-01 và hợp đồng mua HDM-A",
     "1. Ở dòng Điều chỉnh đến, chọn cùng NCC-01 và cùng hợp đồng mua HDM-A\n"
     "2. Nhập số tiền bằng số điều chỉnh từ, bấm Lưu và gửi duyệt",
     "—",
     "- Không lưu\n"
     "- Hiện thông báo \"Hợp đồng mua điều chuyển đến trùng với điều chuyển từ\""),

    ("029", "Chặn số tiền điều chỉnh đến vượt số dư đầu kỳ", "P1",
     "Dòng Điều chỉnh đến đã tích ô \"Số dư nợ đầu kì\", số dư nợ đầu kỳ là 5.000.000",
     "1. Nhập số tiền 8.000.000 cho dòng đến đó\n"
     "2. Bấm Lưu",
     "—",
     "- Không lưu\n"
     "- Hiện cảnh báo \"Số tiền điều chỉnh đến vượt quá số dư nợ đầu kì của hợp đồng\"\n"
     "- Tương tự với nửa Điều chỉnh từ: cảnh báo \"Số tiền điều chỉnh từ vượt quá số dư có đầu kì của "
     "hợp đồng\""),

    ("030", "Lưu nháp phiếu khách hàng hợp lệ", "P0",
     "Màn Tạo mới, Loại phiếu = Điều chỉnh công nợ khách hàng, Diễn giải đã điền, 1 dòng Điều chỉnh từ "
     "10.000.000 và 2 dòng đến 6.000.000 + 4.000.000",
     "1. Bấm nút Lưu\n"
     "2. Đọc thông báo\n"
     "3. Quan sát trang sau khi lưu, tìm phiếu vừa tạo",
     "Tổng 10.000.000",
     "- Thông báo xanh \"Thêm phiếu yêu cầu điều chỉnh công nợ thành công!\"\n"
     "- Chuyển về màn danh sách chế độ Tất cả\n"
     "- Phiếu mới ở đầu danh sách, trạng thái Đang tạo, cột Ngày nhận TRỐNG\n"
     "- Mã phiếu sinh tự động dạng mã công ty + DNDCCN + tháng năm + 5 số"),

    ("031", "Lưu và gửi duyệt", "P0",
     "Màn Tạo mới đã điền hợp lệ như TC_04.030; KT-1 là kế toán thanh toán cùng công ty",
     "1. Bấm nút Lưu và gửi duyệt\n"
     "2. Đọc thông báo\n"
     "3. Tìm phiếu vừa tạo, đọc Trạng thái và cột Ngày nhận\n"
     "4. Đăng nhập KT-1, mở chuông thông báo và màn Chờ duyệt",
     "—",
     "- ⚠️ KHÔNG có hộp thoại xác nhận trước khi lưu\n"
     "- Thông báo \"Phiếu yêu cầu điều chỉnh tạo thành công!\"\n"
     "- Phiếu ở trạng thái Chờ tạo phiếu kế toán, cột Ngày nhận hiện ngày hôm nay\n"
     "- KT-1 nhận thông báo \"Bạn có phiếu yêu cầu điều chỉnh công nợ cần duyệt từ <tên người lập>\" và "
     "thấy phiếu trong màn Chờ duyệt"),

    ("032", "Thông báo chỉ gửi cho kế toán cùng công ty", "P1",
     "NV-A thuộc công ty 3; KT-1 là kế toán thanh toán công ty 3; KT-9 là kế toán thanh toán công ty 1",
     "1. NV-A gửi duyệt 1 phiếu\n"
     "2. Kiểm chuông thông báo của KT-1 và KT-9",
     "—",
     "- KT-1 nhận được thông báo\n"
     "- KT-9 KHÔNG nhận được"),

    ("033", "Bố cục màn Sửa", "P0",
     "Phiếu P trạng thái Đang tạo do chính người đăng nhập lập, 2 dòng Điều chỉnh từ",
     "1. Mở menu hành động dòng phiếu P, bấm Sửa\n"
     "2. Quan sát khối Thông tin chung và bảng chi tiết",
     "—",
     "- Tiêu đề trang là màn sửa phiếu yêu cầu điều chỉnh công nợ\n"
     "- Có thêm ô Mã phiếu chỉ đọc\n"
     "- Ô Loại phiếu bị khóa\n"
     "- Dữ liệu cũ nạp đủ, bảng chi tiết hiện đúng số dòng từ và số dòng đến đã lưu"),

    ("034", "Sửa phiếu và lưu lại", "P0",
     "Phiếu P trạng thái Đang tạo, 1 dòng từ 10.000.000 và 1 dòng đến 10.000.000",
     "1. Đổi Diễn giải\n"
     "2. Tách dòng đến thành 2 dòng: 6.000.000 và 4.000.000\n"
     "3. Bấm Lưu, mở lại chi tiết phiếu P",
     "—",
     "- Thông báo \"Cập nhật phiếu yêu cầu điều chỉnh công nợ!\"\n"
     "- Chuyển về màn danh sách chế độ Tất cả\n"
     "- Mở lại thấy Diễn giải mới và 2 dòng đến đúng như vừa sửa\n"
     "- Mã phiếu và Người tạo KHÔNG đổi"),

    ("035", "Sửa phiếu ở trạng thái Từ chối rồi gửi duyệt lại", "P0",
     "Phiếu Q do chính người đăng nhập lập, trạng thái Từ chối, đã có lý do không duyệt",
     "1. Mở chi tiết phiếu Q, tìm nội dung lý do không duyệt\n"
     "2. Mở menu hành động, bấm Sửa\n"
     "3. Chỉnh số tiền, bấm Lưu và gửi duyệt\n"
     "4. Kiểm trạng thái phiếu",
     "—",
     "- Nút Sửa CÓ hiện với phiếu Từ chối của chính mình\n"
     "- Sau khi lưu, phiếu quay lại Chờ tạo phiếu kế toán và cột Ngày nhận cập nhật ngày mới\n"
     "- Kế toán nhận thông báo mới"),

    ("036", "Không sửa được phiếu đã gửi duyệt qua giao diện", "P0",
     "Phiếu R do chính người đăng nhập lập, đang ở Chờ tạo phiếu kế toán",
     "1. Tìm phiếu R, mở menu hành động\n"
     "2. Mở màn chi tiết phiếu R, quan sát hàng nút",
     "—",
     "- Menu chỉ có In và Xuất Excel\n"
     "- Màn chi tiết chỉ có nút Quay lại"),

    ("037", "Bố cục màn Chi tiết", "P0",
     "Phiếu S trạng thái Đã duyệt phiếu kế toán; người đăng nhập không phải kế toán thanh toán",
     "1. Bấm Mã phiếu để mở chi tiết\n"
     "2. Quan sát toàn màn",
     "—",
     "- Tiêu đề trang \"Chi tiết phiếu yêu cầu điều chỉnh công nợ\"\n"
     "- Mọi ô đều khóa, bảng chi tiết chỉ hiển thị, không có nút thêm hay xóa dòng\n"
     "- ⚠️ Hàng nút CHỈ có Quay lại — KHÔNG có Sửa, Xóa, In và Xuất Excel. Muốn in hay xuất phải quay "
     "ra danh sách dùng menu hành động"),

    ("038", "Màn Chi tiết của kế toán trên phiếu chờ duyệt", "P0",
     "Tài khoản KT-1; phiếu đang ở Chờ tạo phiếu kế toán",
     "1. Mở chi tiết phiếu đó bằng KT-1\n"
     "2. Quan sát hàng nút",
     "—",
     "- Hàng nút có: Tạo phiếu kế toán, Không duyệt, Quay lại\n"
     "- Vẫn không có nút In và Xuất Excel"),

    ("039", "Nút Quay lại trở về danh sách", "P2",
     "Đang mở màn chi tiết",
     "1. Bấm nút Quay lại",
     "—",
     "- Về màn danh sách chế độ Tất cả\n"
     "- Bộ lọc đang dùng trước đó vẫn còn"),

    ("040", "Rời màn nhập dở không có cảnh báo", "P2",
     "Màn Tạo mới, đã nhập Diễn giải và 1 dòng chi tiết, chưa lưu",
     "1. Bấm nút Quay lại",
     "—",
     "- Về thẳng màn danh sách\n"
     "- ⚠️ KHÔNG có cảnh báo \"thông tin chưa lưu\", dữ liệu mất hẳn. Ghi nhận đúng hiện trạng"),

    ("041", "Tạo phiếu từ màn Phiếu báo có", "P0",
     "Màn Phiếu báo có có sẵn dòng chưa xử lý; người dùng có quyền vào màn đó",
     "1. Ở màn Phiếu báo có, chọn vài dòng rồi bấm chức năng tạo phiếu điều chỉnh công nợ\n"
     "2. Quan sát màn Tạo mới mở ra\n"
     "3. Tìm nút dấu cộng thêm dòng Điều chỉnh từ",
     "—",
     "- Loại phiếu tự đặt là Điều chỉnh công nợ khách hàng\n"
     "- Ô Phiếu báo có hiện mã phiếu báo có, ở dạng chỉ đọc\n"
     "- Các dòng Điều chỉnh từ được nạp sẵn theo dòng đã chọn\n"
     "- ⚠️ Nút dấu cộng thêm dòng Điều chỉnh từ bị ẨN — chỉ thêm được dòng Điều chỉnh đến"),

    ("042", "Phiếu tạo từ báo có vẫn thêm bớt được dòng Điều chỉnh đến", "P1",
     "Đang ở màn Tạo mới sinh từ Phiếu báo có",
     "1. Bấm nút Thêm dòng ở nửa Điều chỉnh đến\n"
     "2. Chọn khách hàng, hợp đồng và nhập số tiền\n"
     "3. Bấm Lưu",
     "—",
     "- Thêm được dòng đến bình thường\n"
     "- Lưu thành công, phiếu gắn đúng mã phiếu báo có\n"
     "- Cột Số phiếu báo có ngoài danh sách hiện liên kết tới phiếu báo có"),
]
