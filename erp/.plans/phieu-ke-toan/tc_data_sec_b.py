# -*- coding: utf-8 -*-
"""Section IV — tao moi / sua / xem chi tiet."""

SEC_IV = [
    ("001", "Giá trị mặc định khi mở màn Tạo phiếu", "P0",
     "Tài khoản KT-1 có quyền \"Kế toán thanh toán\"",
     "1. Mở mục Phiếu kế toán, bấm nút Tạo mới\n"
     "2. Quan sát toàn bộ form từ trên xuống",
     "—",
     "- Tiêu đề trang: Tạo phiếu kế toán\n"
     "- Góc phải khối thông tin chung hiện tên người lập và ngày lập là hôm nay\n"
     "- Ngày hạch toán điền sẵn ngày hôm nay\n"
     "- Loại tiền là VNĐ, ô Tỷ giá BỊ KHÓA và nút bên phải ô Tỷ giá ghi VNĐ\n"
     "- Bảng chi tiết chưa có dòng nào, có nút \"Thêm chi tiết\"\n"
     "- Cuối trang có 3 nút: Lưu · Lưu và duyệt · Quay lại"),

    ("002", "Thêm dòng chi tiết đầu tiên", "P0",
     "Đang ở màn Tạo phiếu trắng",
     "1. Bấm nút Thêm chi tiết\n"
     "2. Quan sát bảng",
     "—",
     "- Thêm đúng 1 dòng trống, cột STT ghi 1\n"
     "- Dòng có đủ các ô: Số tài khoản, Mã khách, Phát sinh nợ, Phát sinh có, Diễn giải, Đơn "
     "hàng/Hợp đồng, Mã phí, Mã vụ việc, Ngân hàng, STK ngân hàng, Nhóm định khoản"),

    ("003", "Thêm dòng chi tiết tự bù chênh lệch nợ - có", "P0",
     "Đã có dòng 1 với Phát sinh nợ 1.000.000, chưa có dòng nào bên có",
     "1. Bấm nút Thêm chi tiết\n"
     "2. Đọc ô Phát sinh có của dòng vừa thêm",
     "Dòng 1: Phát sinh nợ 1.000.000",
     "- Dòng 2 được điền sẵn Phát sinh có bằng 1.000.000\n"
     "- Đây là tiện ích giúp cân nhanh nợ - có, người lập vẫn sửa lại được"),

    ("004", "Thêm dòng chi tiết khi bên có đang lớn hơn bên nợ", "P1",
     "Đã có dòng 1 Phát sinh có 2.000.000, chưa có dòng nợ",
     "1. Bấm nút Thêm chi tiết\n"
     "2. Đọc ô Phát sinh nợ của dòng vừa thêm",
     "Dòng 1: Phát sinh có 2.000.000",
     "- Dòng 2 được điền sẵn Phát sinh nợ bằng 2.000.000"),

    ("005", "Xóa dòng chi tiết", "P0",
     "Có 3 dòng chi tiết đã nhập dữ liệu khác nhau",
     "1. Bấm biểu tượng thùng rác ở dòng thứ 2\n"
     "2. Quan sát bảng",
     "—",
     "- Đúng dòng thứ 2 bị xóa, hai dòng còn lại giữ nguyên dữ liệu\n"
     "- Cột STT đánh lại liên tục 1, 2\n"
     "- Dòng Tổng cuối bảng trừ đi số tiền của dòng vừa xóa"),

    ("006", "Chọn Số tài khoản thì Tên tài khoản tự hiện", "P0",
     "Có dòng chi tiết trống",
     "1. Mở ô Số tài khoản, gõ 1311 để tìm\n"
     "2. Chọn tài khoản 1311\n"
     "3. Đọc cột Tên tài khoản",
     "Số tài khoản: 1311",
     "- Cột Tên tài khoản hiện đúng tên của tài khoản 1311\n"
     "- Cột Tên tài khoản là chữ, không cho gõ tay"),

    ("007", "Nhập Phát sinh nợ thì Phát sinh có tự về 0", "P0",
     "Có dòng chi tiết đã nhập Phát sinh có 500.000",
     "1. Nhập Phát sinh nợ 1.000.000\n"
     "2. Đọc ô Phát sinh có\n"
     "3. Nhập lại Phát sinh có 200.000\n"
     "4. Đọc ô Phát sinh nợ",
     "1.000.000 rồi 200.000",
     "- Sau bước 1: Phát sinh có tự về 0\n"
     "- Sau bước 3: Phát sinh nợ tự về 0\n"
     "- Mỗi dòng chỉ giữ được một bên nợ hoặc có"),

    ("008", "Dòng Tổng cuối bảng cộng đúng và cập nhật ngay", "P0",
     "Có 3 dòng: nợ 1.000.000 · có 600.000 · có 500.000",
     "1. Đọc dòng Tổng\n"
     "2. Sửa dòng 3 thành 350.000\n"
     "3. Đọc lại dòng Tổng",
     "—",
     "- Bước 1: tổng nợ 1.000.000, tổng có 1.100.000\n"
     "- Bước 3: tổng có đổi thành 950.000 ngay, không cần bấm nút nào\n"
     "- ⚠️ Dòng Tổng gộp MỌI nhóm định khoản, không dùng nó để kết luận phiếu đã cân"),

    ("009", "Nhập số tiền có dấu phân cách nghìn và phần thập phân", "P1",
     "Có dòng chi tiết",
     "1. Nhập 1,500,000 vào ô Phát sinh nợ, bấm ra ngoài\n"
     "2. Nhập 1000.555 vào dòng khác, bấm ra ngoài",
     "1,500,000 · 1000.555",
     "- Ô đầu hiển thị lại 1.500.000 đúng giá trị\n"
     "- Ô sau được làm tròn còn 2 chữ số thập phân\n"
     "- Không mất số, không thành 0"),

    ("010", "Chọn đối tượng cho dòng chi tiết", "P0",
     "Có dòng chi tiết đã chọn tài khoản 1311",
     "1. Bấm biểu tượng kính lúp ở cột Mã khách\n"
     "2. Tìm theo Mã khách hàng, rồi tìm theo Tên khách hàng\n"
     "3. Chọn một đối tượng",
     "Khách hàng: KH-01",
     "- Cửa sổ tìm kiếm mang tiêu đề Khách hàng, có 3 cột STT, Mã đối tượng, Tên đối tượng\n"
     "- Tìm được cả theo mã và theo tên\n"
     "- Chọn xong: cột Mã khách và Tên khách được điền, hệ thống báo thêm đối tượng thành công\n"
     "- Danh sách gồm cả khách hàng, nhà cung cấp và nhân viên"),

    ("011", "Đổi đối tượng thì xóa hợp đồng đã chọn", "P0",
     "Dòng chi tiết đã chọn khách hàng KH-01 và hợp đồng HD-01, cột NVKD đang có tên",
     "1. Bấm kính lúp cột Mã khách, chọn khách hàng KH-02\n"
     "2. Đọc lại cột Đơn hàng/Hợp đồng và cột NVKD",
     "Đổi sang KH-02",
     "- Cột Đơn hàng/Hợp đồng bị xóa trắng\n"
     "- Cột NVKD bị xóa trắng\n"
     "- Tránh được tình trạng hợp đồng của khách này gắn nhầm cho khách kia"),

    ("012", "Chọn hợp đồng khi chưa chọn đối tượng", "P0",
     "Dòng chi tiết chưa chọn đối tượng",
     "1. Bấm kính lúp ở cột Đơn hàng/Hợp đồng",
     "—",
     "- Hệ thống cảnh báo \"Chưa chọn đối tượng\"\n"
     "- Cửa sổ tìm hợp đồng KHÔNG mở ra"),

    ("013", "Cửa sổ hợp đồng lọc theo đúng đối tượng đã chọn", "P0",
     "Khách hàng KH-01 có 4 hợp đồng; khách hàng KH-02 có 6 hợp đồng",
     "1. Chọn đối tượng KH-01\n"
     "2. Bấm kính lúp cột Đơn hàng/Hợp đồng\n"
     "3. Đếm số hợp đồng trong cửa sổ",
     "Đối tượng: KH-01",
     "- Chỉ hiện 4 hợp đồng của KH-01\n"
     "- Không có hợp đồng của KH-02\n"
     "- Với đối tượng là nhà cung cấp thì cửa sổ lọc theo nhà cung cấp đó"),

    ("014", "Chọn hợp đồng điền đủ thông tin liên quan", "P0",
     "Đã chọn đối tượng KH-01; hợp đồng HD-01 do NVKD-1 lập",
     "1. Bấm kính lúp cột Đơn hàng/Hợp đồng, chọn HD-01\n"
     "2. Đọc cột Đơn hàng/Hợp đồng và cột NVKD",
     "Hợp đồng: HD-01",
     "- Cột Đơn hàng/Hợp đồng hiện HD-01\n"
     "- Cột NVKD tự hiện NVKD-1\n"
     "- Hệ thống báo thêm thành công"),

    ("015", "Hợp đồng nguyên tắc mở thêm ô phiếu xuất hàng và số dư đầu kỳ", "P0",
     "Khách hàng KH-01 có 1 hợp đồng nguyên tắc HD-NT và 1 hợp đồng thường HD-TH; HD-NT có số dư nợ "
     "đầu kỳ 3.000.000",
     "1. Chọn hợp đồng HD-TH, quan sát dòng\n"
     "2. Chọn lại hợp đồng HD-NT, quan sát dòng",
     "HD-TH rồi HD-NT",
     "- Với HD-TH: KHÔNG có ô chọn Số phiếu yc xuất hàng, KHÔNG có ô đánh dấu số dư đầu kỳ\n"
     "- Với HD-NT: hiện ô chọn Số phiếu yc xuất hàng và ô đánh dấu \"Số dư nợ đầu kì: 3.000.000\""),

    ("016", "Chọn phiếu yêu cầu xuất hàng", "P0",
     "Dòng chi tiết đã chọn hợp đồng nguyên tắc HD-NT; HD-NT có cả phiếu yêu cầu xuất hàng và phiếu "
     "yêu cầu xuất bán hàng mượn",
     "1. Bấm kính lúp ở cột Số phiếu yc xuất hàng\n"
     "2. Lọc theo Loại yêu cầu xuất, thử cả hai lựa chọn\n"
     "3. Chọn một phiếu",
     "—",
     "- Cửa sổ mang tiêu đề Phiếu yêu cầu xuất hàng, chỉ hiện phiếu của hợp đồng HD-NT\n"
     "- Ô lọc Loại yêu cầu xuất có 2 lựa chọn: Yêu cầu xuất hàng · Yêu cầu xuất bán hàng mượn\n"
     "- Chọn xong: cột Số phiếu yc xuất hàng hiện mã phiếu vừa chọn"),

    ("017", "Đánh dấu số dư đầu kỳ thì ẩn ô phiếu xuất hàng", "P0",
     "Dòng chi tiết đã chọn hợp đồng nguyên tắc và đã chọn một phiếu yêu cầu xuất hàng",
     "1. Tích ô \"Số dư nợ đầu kì\"\n"
     "2. Quan sát ô Số phiếu yc xuất hàng\n"
     "3. Bỏ tích, quan sát lại",
     "—",
     "- Khi tích: ô chọn Số phiếu yc xuất hàng bị ẩn\n"
     "- Khi bỏ tích: ô hiện lại\n"
     "- ⚠️ Nếu lưu phiếu khi đang tích thì thông tin phiếu xuất hàng bị bỏ đi, không lưu"),

    ("018", "Chọn Ngân hàng lọc danh sách STK và xóa STK cũ", "P0",
     "Công ty có tài khoản ở 2 ngân hàng: NH-A có 3 số tài khoản, NH-B có 2 số tài khoản",
     "1. Chọn Ngân hàng là NH-A\n"
     "2. Mở ô STK ngân hàng, đếm số lựa chọn, chọn một số\n"
     "3. Đổi Ngân hàng sang NH-B\n"
     "4. Đọc lại ô STK ngân hàng",
     "NH-A rồi NH-B",
     "- Bước 2: đúng 3 lựa chọn, mỗi lựa chọn ghi số tài khoản, loại tiền và tên tài khoản\n"
     "- Bước 4: ô STK ngân hàng bị xóa trắng và danh sách còn 2 lựa chọn của NH-B"),

    ("019", "Chọn Mã phí và Mã vụ việc", "P1",
     "Có dòng chi tiết",
     "1. Mở ô Mã phí, gõ để tìm, chọn một giá trị\n"
     "2. Mở ô Mã vụ việc, gõ để tìm, chọn một giá trị",
     "—",
     "- Cả hai ô hiển thị dạng \"Mã - Tên\" và gõ tìm được\n"
     "- Giá trị đã chọn giữ đúng sau khi lưu và mở lại phiếu"),

    ("020", "Chọn loại tiền ngoại tệ tách cột nguyên tệ", "P0",
     "Đang ở màn Tạo phiếu, đã có 2 dòng chi tiết nhập tiền VNĐ",
     "1. Đổi Loại tiền sang USD\n"
     "2. Quan sát tiêu đề bảng chi tiết và ô Tỷ giá",
     "Loại tiền: USD",
     "- Cột Phát sinh nợ tách làm 2 cột con: USD và VNĐ; cột Phát sinh có cũng vậy\n"
     "- Ô Tỷ giá được MỞ KHÓA và điền sẵn tỷ giá mặc định của USD\n"
     "- Nút bên phải ô Tỷ giá đổi thành USD\n"
     "- Dòng Tổng có đủ 4 ô tổng"),

    ("021", "Quy đổi số tiền theo tỷ giá", "P0",
     "Loại tiền USD, tỷ giá 25.000",
     "1. Nhập Phát sinh nợ (USD) là 100\n"
     "2. Đọc ô VNĐ cùng dòng",
     "100 USD",
     "- Ô VNĐ hiện 2.500.000\n"
     "- Ô VNĐ là chữ, không cho gõ tay"),

    ("022", "Sửa tỷ giá sau khi đã nhập chi tiết", "P0",
     "Loại tiền USD, tỷ giá 25.000, đã có 3 dòng nhập tiền nguyên tệ",
     "1. Sửa Tỷ giá thành 26.000\n"
     "2. Đọc lại cột VNĐ của cả 3 dòng và dòng Tổng",
     "Tỷ giá: 26.000",
     "- Cả 3 dòng đều tính lại cột VNĐ theo tỷ giá mới\n"
     "- Dòng Tổng VNĐ cập nhật theo\n"
     "- Cột nguyên tệ giữ nguyên"),

    ("023", "Đổi loại tiền ngoại tệ về VNĐ", "P1",
     "Đang là USD, tỷ giá 25.000, đã có dữ liệu chi tiết",
     "1. Đổi Loại tiền về VNĐ\n"
     "2. Quan sát bảng chi tiết và ô Tỷ giá",
     "Loại tiền: VNĐ",
     "- Hai cột nguyên tệ biến mất, chỉ còn cột VNĐ\n"
     "- Ô Tỷ giá BỊ KHÓA lại\n"
     "- ⚠️ Kiểm tra kỹ số tiền còn lại trên các dòng có đúng ý người lập không, vì hệ thống tính lại "
     "theo tỷ giá mới"),

    ("024", "Đính kèm nhiều tệp", "P0",
     "Đang ở màn Tạo phiếu",
     "1. Bấm dấu cộng ở khu vực File đính kèm 3 lần\n"
     "2. Chọn 3 tệp khác nhau\n"
     "3. Bấm dấu X trên tệp thứ 2\n"
     "4. Lưu phiếu rồi mở màn chi tiết",
     "3 tệp tài liệu",
     "- Mỗi lần bấm dấu cộng thêm một ô chọn tệp, hiện đúng tên tệp đã chọn\n"
     "- Bấm X gỡ đúng tệp thứ 2, hai tệp còn lại giữ nguyên\n"
     "- Màn chi tiết hiện đúng 2 tệp, bấm vào mở hoặc tải được"),

    ("025", "Cuộn bảng chi tiết giữ cố định tiêu đề và 3 cột đầu", "P2",
     "Phiếu có 15 dòng chi tiết, cửa sổ trình duyệt thu nhỏ",
     "1. Cuộn dọc trong bảng chi tiết\n"
     "2. Cuộn ngang trong bảng chi tiết",
     "—",
     "- Cuộn dọc: hai dòng tiêu đề bảng luôn nhìn thấy\n"
     "- Cuộn ngang: ba cột STT, Số tài khoản, Tên tài khoản luôn nhìn thấy"),

    ("026", "Cửa sổ chọn Phiếu yêu cầu điều chỉnh công nợ chỉ hiện phiếu đã duyệt", "P0",
     "Có Phiếu yêu cầu điều chỉnh công nợ ở nhiều trạng thái, trong đó 3 phiếu đã duyệt",
     "1. Ở màn Tạo phiếu, bấm kính lúp ô Phiếu yêu cầu điều chỉnh công nợ\n"
     "2. Đếm số phiếu và soát trạng thái",
     "—",
     "- Cửa sổ mang tiêu đề Yêu cầu điều chỉnh công nợ, có 3 cột STT, Mã phiếu, Ngày lập\n"
     "- Chỉ hiện 3 phiếu đã duyệt, không hiện phiếu nháp hay phiếu chờ duyệt\n"
     "- Tìm được theo Mã phiếu yêu cầu điều chỉnh"),

    ("027", "Chọn Phiếu yêu cầu điều chỉnh công nợ nạp toàn bộ dữ liệu", "P0",
     "Phiếu yêu cầu điều chỉnh công nợ YCDC-01 đã duyệt, có 4 dòng chi tiết, diễn giải và ngày hạch "
     "toán riêng",
     "1. Chọn YCDC-01 trong cửa sổ\n"
     "2. Quan sát toàn bộ form",
     "YCDC-01",
     "- Ô Phiếu yêu cầu điều chỉnh công nợ hiện mã YCDC-01\n"
     "- Diễn giải, Ngày hạch toán và đủ 4 dòng chi tiết được nạp sẵn\n"
     "- Nút \"Thêm chi tiết\" và biểu tượng thùng rác xóa dòng bị ẩn\n"
     "- Ô Loại tiền BỊ KHÓA\n"
     "- Các dòng chi tiết chỉ xem, không sửa được số tiền và đối tượng"),

    ("028", "Yêu cầu điều chỉnh công nợ của nhà cung cấp đồng bộ loại tiền và tỷ giá", "P0",
     "Phiếu yêu cầu điều chỉnh công nợ YCDC-NCC lập cho nhà cung cấp, loại tiền USD, tỷ giá 25.500",
     "1. Ở màn Tạo phiếu, chọn YCDC-NCC\n"
     "2. Đọc ô Loại tiền và ô Tỷ giá",
     "YCDC-NCC (USD, 25.500)",
     "- Loại tiền hiện USD\n"
     "- Tỷ giá hiện 25.500 lấy từ phiếu yêu cầu\n"
     "- Bảng chi tiết tách cột nguyên tệ và VNĐ"),

    ("029", "Yêu cầu điều chỉnh công nợ của khách hàng ép về VNĐ", "P1",
     "Phiếu yêu cầu điều chỉnh công nợ YCDC-KH lập cho khách hàng",
     "1. Ở màn Tạo phiếu, chọn YCDC-KH\n"
     "2. Đọc ô Loại tiền",
     "YCDC-KH",
     "- Loại tiền luôn là VNĐ, không phụ thuộc loại tiền của phiếu yêu cầu\n"
     "- Ô Tỷ giá bị khóa"),

    ("030", "Vào màn Tạo phiếu kèm sẵn Phiếu yêu cầu điều chỉnh công nợ", "P1",
     "Phiếu yêu cầu điều chỉnh công nợ YCDC-01 đã duyệt",
     "1. Từ màn chi tiết YCDC-01, bấm chức năng lập phiếu kế toán (hoặc dán đường dẫn màn Tạo phiếu "
     "kèm tham số phiếu yêu cầu)\n"
     "2. Quan sát form ngay khi mở",
     "—",
     "- Form tự nạp sẵn dữ liệu YCDC-01 mà không cần bấm kính lúp\n"
     "- Kết quả giống hệt cách chọn thủ công"),

    ("031", "Lập phiếu từ Phiếu yêu cầu hạch toán bổ sung", "P0",
     "Phiếu yêu cầu hạch toán bổ sung HTBS-01 đã duyệt, có 2 tệp đính kèm và 3 dòng chi tiết",
     "1. Từ màn chi tiết HTBS-01, bấm chức năng lập phiếu kế toán\n"
     "2. Quan sát form",
     "HTBS-01",
     "- Ô \"Phiếu yêu cầu hạch toán bổ sung\" hiện mã HTBS-01 và không sửa được\n"
     "- Loại tiền, Ngày hạch toán và 3 dòng chi tiết được nạp sẵn\n"
     "- Khu vực File đính kèm hiện sẵn 2 tệp của phiếu yêu cầu\n"
     "- Không có ô chọn Phiếu yêu cầu điều chỉnh công nợ"),

    ("032", "Phiếu lập từ Yêu cầu hạch toán bổ sung dạng thứ bảy", "P1",
     "Phiếu yêu cầu hạch toán bổ sung HTBS-07 thuộc dạng thứ bảy",
     "1. Lập phiếu kế toán từ HTBS-07\n"
     "2. Quan sát bảng chi tiết",
     "HTBS-07",
     "- Cột Số phiếu yc xuất hàng bị ẩn khỏi bảng\n"
     "- Ô Số tài khoản của các dòng đã có sẵn tài khoản bị KHÓA\n"
     "- Cột Đơn hàng/Hợp đồng hiện dạng liên kết bấm mở được, không phải ô chọn\n"
     "- Diễn giải phiếu được lấy sẵn từ phiếu yêu cầu"),

    ("033", "Lập phiếu từ Yêu cầu hạch toán hoa hồng tháng", "P1",
     "Phiếu yêu cầu hạch toán hoa hồng tháng HH-01 đã chờ hạch toán",
     "1. Từ màn chi tiết HH-01, bấm chức năng lập phiếu kế toán\n"
     "2. Quan sát form",
     "HH-01",
     "- Ô \"Phiếu yêu cầu hạch toán hoa hồng tháng\" hiện mã HH-01, không sửa được\n"
     "- Diễn giải và các dòng chi tiết được nạp sẵn\n"
     "- Loại tiền luôn là VNĐ\n"
     "- Nút Thêm chi tiết bị ẩn"),

    ("034", "Lập phiếu từ bảng Chi phí vận chuyển nhanh", "P0",
     "Bảng Chi phí vận chuyển nhanh có 2 bản ghi chưa hạch toán, số tiền 1.000.000 và 2.000.000, thuộc "
     "2 khách hàng khác nhau",
     "1. Tích chọn cả 2 bản ghi, bấm chức năng lập phiếu kế toán\n"
     "2. Quan sát ô nguồn và bảng chi tiết",
     "2 bản ghi CPVC nhanh",
     "- Ô nguồn ghi \"Chi phí vận chuyển nhanh\"\n"
     "- Bảng có 4 dòng: mỗi bản ghi sinh 1 dòng Nợ tài khoản 35241 và 1 dòng Có tài khoản 811 cùng số "
     "tiền\n"
     "- Bản ghi thứ nhất mang Nhóm định khoản 1, bản ghi thứ hai mang Nhóm định khoản 2\n"
     "- Mã khách và Tên khách của từng cặp dòng lấy đúng theo bản ghi\n"
     "- Biểu tượng xóa dòng bị ẩn"),

    ("035", "Chọn hợp đồng ở phiếu lập từ Chi phí vận chuyển nhanh", "P1",
     "Đang lập phiếu từ Chi phí vận chuyển nhanh; bản ghi thuộc khách hàng KH-01 và nhân viên NVKD-1; "
     "KH-01 có cả hợp đồng bán và hợp đồng mua",
     "1. Bấm kính lúp cột Đơn hàng/Hợp đồng ở dòng đầu\n"
     "2. Đếm và soát danh sách hợp đồng",
     "—",
     "- Chỉ hiện HỢP ĐỒNG BÁN của KH-01 do NVKD-1 lập\n"
     "- Không hiện hợp đồng mua, không hiện hợp đồng của nhân viên khác"),

    ("036", "Mở màn Sửa phiếu nháp của mình", "P0",
     "Phiếu P ở trạng thái Đang tạo do chính mình lập, có 3 dòng chi tiết, 1 tệp đính kèm, loại tiền "
     "USD",
     "1. Ở danh sách, bấm Hành động rồi bấm Sửa\n"
     "2. Đối chiếu toàn bộ dữ liệu với màn chi tiết",
     "—",
     "- Tiêu đề trang: Sửa phiếu kế toán kèm mã phiếu\n"
     "- Thông tin chung, đủ 3 dòng chi tiết, tệp đính kèm và loại tiền USD nạp đúng\n"
     "- Bảng chi tiết vẫn tách cột nguyên tệ và VNĐ\n"
     "- Có 3 nút Lưu · Lưu và duyệt · Quay lại"),

    ("037", "Không mở được màn Sửa với phiếu đã duyệt", "P0",
     "Phiếu Q đã duyệt do chính mình lập",
     "1. Mở danh sách, bấm Hành động của phiếu Q\n"
     "2. Dán đường dẫn màn Sửa của phiếu Q vào thanh địa chỉ",
     "—",
     "- Menu Hành động KHÔNG có mục Sửa\n"
     "- Mở đường dẫn trực tiếp: hệ thống báo dữ liệu không tồn tại"),

    ("038", "Sửa phiếu nháp rồi lưu lại", "P0",
     "Phiếu P Đang tạo có 2 dòng chi tiết",
     "1. Sửa Diễn giải phiếu\n"
     "2. Thêm 1 dòng chi tiết mới và xóa 1 dòng cũ, giữ cho từng nhóm vẫn cân nợ - có\n"
     "3. Bấm Lưu\n"
     "4. Mở lại phiếu P",
     "—",
     "- Hệ thống báo lưu thành công và quay về danh sách chế độ Tất cả\n"
     "- Mở lại: Diễn giải mới, đúng 2 dòng chi tiết theo dữ liệu mới, không còn dòng đã xóa\n"
     "- Cột Tổng phát sinh ngoài danh sách cập nhật theo số mới"),

    ("039", "Sửa phiếu và thêm tệp đính kèm mới", "P1",
     "Phiếu P Đang tạo đã có 1 tệp đính kèm",
     "1. Bấm dấu cộng, chọn thêm 1 tệp\n"
     "2. Bấm Lưu\n"
     "3. Mở màn chi tiết phiếu P",
     "1 tệp mới",
     "- Màn chi tiết hiện đủ 2 tệp: tệp cũ và tệp mới\n"
     "- Cả hai tệp mở hoặc tải được"),

    ("040", "Xem chi tiết phiếu", "P0",
     "Phiếu Q đã duyệt, loại tiền VNĐ, có 4 dòng chi tiết và 1 tệp đính kèm",
     "1. Bấm mã phiếu ở danh sách\n"
     "2. Quan sát toàn bộ màn",
     "—",
     "- Tiêu đề trang: Chi tiết phiếu kế toán kèm mã phiếu\n"
     "- Hiện đủ thông tin chung, 4 dòng chi tiết và tệp đính kèm\n"
     "- Mọi ô đều chỉ đọc, không gõ sửa được\n"
     "- Cuối trang CHỈ có nút Quay lại, không có Lưu và không có Lưu và duyệt"),

    ("041", "Xem chi tiết phiếu ngoại tệ", "P1",
     "Phiếu USD, tỷ giá 25.000, phát sinh nợ 100 USD",
     "1. Mở màn chi tiết phiếu đó",
     "—",
     "- Ô Loại tiền hiện USD, ô Tỷ giá hiện 25.000\n"
     "- Bảng chi tiết có đủ cột nguyên tệ và cột VNĐ\n"
     "- Dòng Tổng hiện đủ 4 ô tổng"),

    ("042", "Bấm Quay lại từ màn Tạo phiếu không lưu dữ liệu", "P2",
     "Đang ở màn Tạo phiếu, đã nhập dở thông tin chung và 2 dòng chi tiết",
     "1. Bấm nút Quay lại\n"
     "2. Kiểm tra danh sách",
     "—",
     "- Về màn danh sách chế độ Tất cả\n"
     "- Không có phiếu mới nào được tạo"),
]
