# -*- coding: utf-8 -*-
"""Cac section nghiep vu cho man 'Bao cao han muc cong no nhan vien'."""

SEC_I = [
    ("001", "Mở báo cáo từ menu", "P0",
     "Tài khoản B có quyền \"Xem tất cả phiếu\"\n"
     "Có 14 nhân viên có hạn mức > 0",
     "1. Rê chuột vào Kế toán > Kế toán Công nợ\n"
     "2. Ở nhóm Nhân viên, bấm \"Báo cáo hạn mức công nợ nhân viên\"",
     "—",
     "- Tiêu đề trang \"Báo cáo hạn mức công nợ nhân viên\"\n"
     "- Bảng tự tải, hiện 10 dòng đầu, dòng dưới bảng ghi tổng 14"),

    ("002", "Các cột của bảng", "P1",
     "Mở báo cáo",
     "1. Quan sát dòng tiêu đề",
     "—",
     "- Đúng 7 cột: STT · Mã nhân viên · Tên nhân viên · Bộ phận · Phòng ban · Hạn mức công nợ xuất hàng · "
     "Tổng công nợ khách hàng hiện tại\n"
     "- Cạnh Mã nhân viên có biểu tượng chữ i màu xanh"),

    ("003", "Mục menu khác cùng nhóm dẫn tới báo cáo khách hàng", "P1",
     "Mở báo cáo nhân viên",
     "1. Vào Kế toán > Kế toán Công nợ > nhóm Khách hàng > \"Báo cáo hạn mức công nợ khách hàng\"\n"
     "2. So tiêu đề và các cột",
     "—",
     "- Tiêu đề đổi sang báo cáo khách hàng, cột là thông tin khách hàng\n"
     "- Hai mục menu cho ra hai báo cáo khác nhau"),

    ("004", "Sửa tay tham số trên thanh địa chỉ thành giá trị lạ", "P2",
     "Đang mở báo cáo nhân viên",
     "1. Sửa tham số loại báo cáo trên thanh địa chỉ thành giá trị bất kỳ (vd \"abc\"), nhấn Enter",
     "—",
     "- Hệ thống mở Báo cáo hạn mức công nợ khách hàng, không lỗi trang\n"
     "- Không lộ thêm dữ liệu"),

    ("005", "Không có nhân viên nào đặt hạn mức", "P2",
     "Môi trường kiểm thử: mọi nhân viên có hạn mức trống hoặc 0",
     "1. Mở báo cáo",
     "—",
     "- Bảng hiện thông báo không có dữ liệu, tổng 0, không lỗi"),

    ("006", "Màn không có thao tác thêm / sửa / xuất", "P2",
     "Mở báo cáo",
     "1. Quan sát vùng nút phía trên bảng",
     "—",
     "- Chỉ có nút Bộ lọc\n"
     "- Không có Tạo mới, In, Xuất Excel"),
]

SEC_II = [
    ("001", "Mở và đóng khối Bộ lọc", "P1",
     "Mở báo cáo",
     "1. Bấm nút Bộ lọc\n"
     "2. Bấm lại nút Bộ lọc",
     "—",
     "- Lần 1: khối lọc mở ra, có nút tìm kiếm (kính lúp) và nút làm mới\n"
     "- Lần 2: khối lọc thu lại"),

    ("002", "Chỉ tiêu Trong hạn mức", "P0",
     "NV-1 hạn mức 100,000,000, công nợ 80,000,000\n"
     "NV-2 hạn mức 100,000,000, công nợ 150,000,000\n"
     "NV-3 hạn mức 100,000,000, công nợ 100,000,000",
     "1. Bấm Bộ lọc, chọn Chỉ tiêu vượt hạn mức = Trong hạn mức\n"
     "2. Bấm kính lúp",
     "Chỉ tiêu vượt hạn mức: Trong hạn mức",
     "- Có NV-1\n"
     "- KHÔNG có NV-2, NV-3"),

    ("003", "Chỉ tiêu Vượt hạn mức", "P0",
     "Như TC_02.002",
     "1. Chọn Chỉ tiêu vượt hạn mức = Vượt hạn mức, bấm kính lúp",
     "Chỉ tiêu vượt hạn mức: Vượt hạn mức",
     "- Có NV-2\n"
     "- KHÔNG có NV-1, NV-3"),

    ("004", "Công nợ bằng đúng hạn mức không thuộc chỉ tiêu nào", "P0",
     "NV-3 hạn mức 100,000,000, công nợ đúng 100,000,000",
     "1. Lần lượt lọc Trong hạn mức, rồi Vượt hạn mức\n"
     "2. Bỏ chọn chỉ tiêu",
     "—",
     "- Hai lần lọc đều KHÔNG có NV-3\n"
     "- Bỏ chọn chỉ tiêu thì NV-3 hiện lại\n"
     "- Lưu ý: ghi nhận nếu nghiệp vụ muốn tính bằng hạn mức là Trong hạn mức"),

    ("005", "Ô lọc Nhân viên không có tác dụng", "P0",
     "Có 14 nhân viên trong báo cáo, gồm NV-1",
     "1. Chọn Nhân viên = NV-1 trong ô Nhân viên\n"
     "2. Bấm kính lúp, đọc tổng",
     "Nhân viên: NV-1",
     "- Kỳ vọng nghiệp vụ: chỉ còn dòng NV-1\n"
     "- Lưu ý: theo code hiện tại danh sách vẫn đủ 14 dòng - ghi nhận lỗi nếu xảy ra"),

    ("006", "Ô Nhân viên tìm được cả nhân viên đã nghỉ", "P2",
     "NV-OFF đã nghỉ việc",
     "1. Gõ tên NV-OFF vào ô Nhân viên",
     "Từ khóa: tên NV-OFF",
     "- Gợi ý có NV-OFF"),

    ("007", "Lọc theo Công ty", "P0",
     "Tài khoản B (Xem tất cả phiếu)\n"
     "Công ty 3 có 5 nhân viên có hạn mức",
     "1. Bấm Bộ lọc, chọn Công ty = Công ty 3, bấm kính lúp",
     "Công ty: Công ty 3",
     "- Tổng còn 5, mọi dòng là nhân viên đang thuộc Công ty 3"),

    ("008", "Lọc theo Phòng ban", "P0",
     "Phòng KD1 có 3 nhân viên có hạn mức",
     "1. Chọn Phòng ban = KD1, bấm kính lúp",
     "Phòng ban: KD1",
     "- Tổng 3, cột Phòng ban đều là KD1"),

    ("009", "Lọc theo Bộ phận", "P1",
     "Tài khoản D (Xem tất cả phiếu của phòng ban)\n"
     "Bộ phận BP-A có 2 nhân viên có hạn mức",
     "1. Chọn Bộ phận = BP-A, bấm kính lúp",
     "Bộ phận: BP-A",
     "- Tổng 2, cột Bộ phận đều là BP-A"),

    ("010", "Lọc theo khoảng ngày ghi sổ", "P0",
     "NV-1 có 2 bút toán ghi Nợ 131: 50,000,000 ngày 05/09/2026 và 30,000,000 ngày 20/09/2026, cùng hợp "
     "đồng do NV-1 lập",
     "1. Nhập Từ ngày 01/09/2026, Đến ngày 15/09/2026\n"
     "2. Bấm kính lúp, đọc cột Tổng công nợ của NV-1",
     "Từ ngày: 01/09/2026\nĐến ngày: 15/09/2026",
     "- Tổng công nợ NV-1 = 50,000,000\n"
     "- NV-1 vẫn hiện dù đổi khoảng ngày"),

    ("011", "Đến ngày loại phát sinh trong chính ngày đó", "P0",
     "NV-1 có bút toán Nợ 131 30,000,000 ghi sổ lúc 10 giờ ngày 20/09/2026",
     "1. Nhập Từ ngày 20/09/2026, Đến ngày 20/09/2026, bấm kính lúp",
     "Từ ngày: 20/09/2026\nĐến ngày: 20/09/2026",
     "- Lưu ý: Tổng công nợ NV-1 hiện 0 vì phát sinh trong ngày Đến ngày bị loại\n"
     "- Muốn lấy trọn ngày 20/09 phải nhập Đến ngày 21/09/2026"),

    ("012", "Bộ lọc thời gian kết hợp chỉ tiêu", "P1",
     "NV-2 hạn mức 100,000,000; công nợ toàn kỳ 150,000,000, riêng tháng 09/2026 là 60,000,000",
     "1. Chọn Vượt hạn mức, bấm kính lúp\n"
     "2. Thêm Từ ngày 01/09/2026, Đến ngày 01/10/2026, bấm kính lúp",
     "—",
     "- Lần 1 có NV-2\n"
     "- Lần 2 KHÔNG có NV-2 (công nợ trong kỳ 60,000,000 < hạn mức)"),

    ("013", "Nút làm mới xóa toàn bộ bộ lọc", "P0",
     "Đang lọc Công ty 3 + Vượt hạn mức + khoảng ngày",
     "1. Bấm nút làm mới (mũi tên tròn, nút xanh lá)",
     "—",
     "- Mọi ô lọc trở về trống\n"
     "- Danh sách trở lại đủ 14 dòng"),

    ("014", "Ghi nhớ bộ lọc khi quay lại màn", "P1",
     "Đang lọc Vượt hạn mức",
     "1. Chuyển sang màn khác\n"
     "2. Mở lại báo cáo từ menu",
     "—",
     "- Bộ lọc Vượt hạn mức vẫn được giữ, danh sách ra đúng theo bộ lọc đó"),
]

SEC_III = [
    ("001", "Phân trang và số dòng mỗi trang", "P1",
     "Có 14 nhân viên có hạn mức",
     "1. Đọc số dòng trang 1\n"
     "2. Sang trang 2\n"
     "3. Đổi số dòng mỗi trang sang 25",
     "—",
     "- Trang 1: 10 dòng; trang 2: 4 dòng\n"
     "- STT trang 2 bắt đầu từ 11\n"
     "- Chọn 25 dòng: 1 trang đủ 14 dòng"),

    ("002", "Sắp xếp theo cột Hạn mức công nợ xuất hàng", "P2",
     "Có nhiều nhân viên với hạn mức khác nhau",
     "1. Bấm tiêu đề cột Hạn mức công nợ xuất hàng 2 lần",
     "—",
     "- Danh sách đảo thứ tự theo hạn mức tăng / giảm\n"
     "- Các cột còn lại không sắp xếp được"),

    ("003", "Hiển thị Bộ phận / Phòng ban theo hồ sơ hiện tại", "P1",
     "NV-1 vừa được chuyển từ phòng KD1 sang KD2",
     "1. Mở báo cáo, đọc dòng NV-1",
     "—",
     "- Cột Phòng ban hiện KD2"),

    ("004", "Định dạng số tiền", "P1",
     "NV-1 hạn mức 1500000000, công nợ 1234567.6",
     "1. Đọc 2 cột tiền của NV-1",
     "—",
     "- Hạn mức: 1,500,000,000\n"
     "- Tổng công nợ: 1,234,568 (làm tròn, không số lẻ)"),

    ("005", "Công nợ âm khi khách trả thừa", "P2",
     "NV-4 hạn mức 50,000,000; hợp đồng do NV-4 lập có Nợ 131 10,000,000, Có 131 15,000,000",
     "1. Đọc dòng NV-4",
     "—",
     "- Tổng công nợ hiện -5,000,000\n"
     "- NV-4 thuộc chỉ tiêu Trong hạn mức"),
]

SEC_IV = [
    ("001", "Nhân viên mới đặt hạn mức xuất hiện trong báo cáo", "P0",
     "NV-NEW chưa có hạn mức, không có trong báo cáo",
     "1. Vào hồ sơ nhân viên NV-NEW, nhập Hạn mức công nợ xuất hàng 200000000, lưu\n"
     "2. Mở lại báo cáo",
     "Hạn mức công nợ xuất hàng: 200000000",
     "- NV-NEW xuất hiện, cột hạn mức 200,000,000"),

    ("002", "Bỏ hạn mức thì biến mất khỏi báo cáo", "P0",
     "NV-1 hạn mức 100,000,000",
     "1. Xóa trắng (hoặc nhập 0) ô Hạn mức công nợ xuất hàng trong hồ sơ NV-1, lưu\n"
     "2. Mở lại báo cáo",
     "Hạn mức công nợ xuất hàng: 0",
     "- NV-1 không còn trong báo cáo"),

    ("003", "Nhân viên nghỉ việc vẫn hiện nếu còn hạn mức", "P1",
     "NV-OFF đã nghỉ việc, hạn mức 80,000,000",
     "1. Mở báo cáo, tìm dòng NV-OFF",
     "—",
     "- NV-OFF vẫn hiện với hạn mức 80,000,000"),

    ("004", "Mở cửa sổ chi tiết theo khách hàng", "P0",
     "NV-1 có công nợ với 2 khách KH-A, KH-B trên hợp đồng do NV-1 lập",
     "1. Bấm biểu tượng chữ i cạnh mã NV-1",
     "—",
     "- Mở cửa sổ lớn tiêu đề \"Thông tin chi tiết hạn mức dư nợ nhân viên <Mã NV-1> - <Tên NV-1> theo "
     "khách hàng\"\n"
     "- Cột: STT · Mã khách · Tên khách · Công nợ\n"
     "- Có 2 dòng KH-A, KH-B"),

    ("005", "Lọc khách hàng trong cửa sổ chi tiết", "P1",
     "Cửa sổ chi tiết NV-1 đang mở, có KH-A, KH-B",
     "1. Chọn Khách hàng = KH-B, bấm tìm kiếm",
     "Khách hàng: KH-B",
     "- Chỉ còn dòng KH-B"),

    ("006", "Lọc Số tiền từ / đến trong cửa sổ chi tiết", "P1",
     "Cửa sổ chi tiết NV-1 có các dòng Công nợ 20,000,000 và 70,000,000",
     "1. Nhập Số tiền từ 50,000,000, bấm tìm kiếm\n"
     "2. Xóa, nhập Số tiền đến 50,000,000, bấm tìm kiếm",
     "Số tiền từ: 50,000,000\nSố tiền đến: 50,000,000",
     "- Lần 1 chỉ còn dòng 70,000,000\n"
     "- Lần 2 chỉ còn dòng 20,000,000\n"
     "- Số đúng bằng mốc được giữ lại"),

    ("007", "Nhân viên không có công nợ", "P2",
     "NV-5 có hạn mức nhưng chưa lập hợp đồng nào",
     "1. Đọc dòng NV-5\n"
     "2. Bấm chữ i của NV-5",
     "—",
     "- Tổng công nợ hiện 0\n"
     "- Cửa sổ chi tiết không có dòng nào"),
]

SEC_V = [
    ("001", "Không áp dụng cho feature này", "P2",
     "—", "1. Quan sát màn", "—",
     "- Báo cáo chỉ xem, không có thao tác trạng thái"),
]

SEC_VI = [
    ("001", "Không áp dụng cho feature này", "P2",
     "—", "1. Quan sát màn", "—",
     "- Không có chức năng Xóa"),
]

SEC_VII = [
    ("001", "Không có In và Xuất Excel", "P2",
     "Mở báo cáo", "1. Tìm nút In / Xuất Excel", "—",
     "- Không có nút nào"),
]

SEC_VIII = [
    ("001", "Nhập ngày sai định dạng", "P2",
     "Mở báo cáo",
     "1. Gõ tay \"2026-09-01\" vào ô Từ ngày, bấm kính lúp",
     "Từ ngày: 2026-09-01",
     "- Trang không bị treo, không báo lỗi hệ thống\n"
     "- Ghi lại kết quả lọc thực tế (ô ngày chỉ hỗ trợ dạng ngày/tháng/năm)"),

    ("002", "Từ ngày lớn hơn Đến ngày", "P2",
     "Mở báo cáo",
     "1. Nhập Từ ngày 30/09/2026, Đến ngày 01/09/2026, bấm kính lúp",
     "—",
     "- Không báo lỗi, không chặn\n"
     "- Mọi nhân viên vẫn hiện, Tổng công nợ đều 0"),

    ("003", "Số tiền chữ trong cửa sổ chi tiết", "P2",
     "Cửa sổ chi tiết đang mở",
     "1. Gõ \"abc\" vào Số tiền từ, bấm tìm kiếm",
     "Số tiền từ: abc",
     "- Ô không nhận chữ hoặc bị bỏ qua, không lỗi trang"),
]

SEC_IX = [
    ("001", "Công nợ chỉ tính hợp đồng do chính nhân viên lập", "P0",
     "KH-A có 2 hợp đồng: HĐ1 do NV-1 lập, nợ 60,000,000; HĐ2 do NV-2 lập, nợ 40,000,000",
     "1. Mở báo cáo, đọc Tổng công nợ của NV-1 và NV-2",
     "—",
     "- NV-1: 60,000,000\n"
     "- NV-2: 40,000,000\n"
     "- Không cộng chéo công nợ của nhau"),

    ("002", "Bút toán không gắn hợp đồng không được tính", "P0",
     "NV-1 có Nợ 131 60,000,000 trên HĐ1; có thêm bút toán Có 131 10,000,000 cho KH-A nhưng không chọn "
     "hợp đồng",
     "1. Đọc Tổng công nợ NV-1",
     "—",
     "- Vẫn hiện 60,000,000 (bút toán không có hợp đồng bị bỏ qua)"),

    ("003", "Công nợ cộng dồn mọi công ty", "P1",
     "NV-1 lập HĐ ở Công ty 1 (nợ 30,000,000) và HĐ ở Công ty 3 (nợ 20,000,000)",
     "1. Đọc Tổng công nợ NV-1",
     "—",
     "- Hiện 50,000,000"),

    ("004", "Số liệu cập nhật ngay khi có phát sinh mới", "P1",
     "Báo cáo đang mở, NV-1 công nợ 60,000,000",
     "1. Kế toán ghi nhận thêm Phiếu thu 20,000,000 cho HĐ1 của NV-1\n"
     "2. Bấm kính lúp trên báo cáo",
     "—",
     "- Tổng công nợ NV-1 còn 40,000,000"),
]

SEC_X = [
    ("001", "Từ đặt hạn mức đến vượt hạn mức", "P0",
     "NV-6 chưa có hạn mức; đã lập HĐ bán hàng cho KH-A",
     "1. Đặt hạn mức NV-6 = 100,000,000 trong hồ sơ nhân viên\n"
     "2. Ghi nhận công nợ HĐ của NV-6: 80,000,000\n"
     "3. Mở báo cáo, lọc Trong hạn mức\n"
     "4. Ghi nhận thêm công nợ 50,000,000 trên HĐ của NV-6\n"
     "5. Lọc Vượt hạn mức",
     "—",
     "- Bước 3: NV-6 có trong Trong hạn mức, công nợ 80,000,000\n"
     "- Bước 5: NV-6 có trong Vượt hạn mức, công nợ 130,000,000"),

    ("002", "Hạn mức nhân viên không chặn Phiếu yêu cầu xuất hàng", "P1",
     "NV-2 đang Vượt hạn mức trên báo cáo; KH-A không khai báo hạn mức khách hàng",
     "1. NV-2 lập Phiếu yêu cầu xuất hàng cho KH-A, gửi duyệt",
     "—",
     "- Không có hộp thoại vượt hạn mức nhân viên, phiếu gửi duyệt bình thường\n"
     "- Lưu ý: kiểm tra theo hạn mức nhân viên đang tắt; ghi nhận nếu nghiệp vụ yêu cầu chặn"),

    ("003", "Đối chiếu tổng màn chính với cửa sổ chi tiết", "P0",
     "NV-1 có công nợ: KH-A 30,000,000; KH-B 20,000,000",
     "1. Đọc Tổng công nợ NV-1 ở màn chính\n"
     "2. Mở cửa sổ chi tiết NV-1, đọc cột Công nợ từng khách",
     "—",
     "- Màn chính: 50,000,000\n"
     "- Kỳ vọng nghiệp vụ: KH-A 30,000,000 và KH-B 20,000,000\n"
     "- Lưu ý: theo code hiện tại cột Công nợ là số lũy kế, có thể hiện KH-A 30,000,000 và KH-B "
     "50,000,000 - ghi nhận lỗi nếu xảy ra"),

    ("004", "Cửa sổ chi tiết khi có lọc Từ ngày ở màn chính", "P0",
     "NV-1 có công nợ phát sinh rải trong tháng 09/2026",
     "1. Ở màn chính nhập Từ ngày 01/09/2026, Đến ngày 01/10/2026, bấm kính lúp\n"
     "2. Bấm chữ i của NV-1",
     "Từ ngày: 01/09/2026\nĐến ngày: 01/10/2026",
     "- Kỳ vọng nghiệp vụ: cửa sổ ra công nợ theo khách trong tháng 09/2026, tổng khớp màn chính\n"
     "- Lưu ý: theo code hiện tại cửa sổ dùng Từ ngày cho cả hai đầu nên thường không có dòng nào - "
     "ghi nhận lỗi nếu xảy ra"),

    ("005", "Cửa sổ chi tiết khi chỉ lọc Đến ngày", "P1",
     "NV-1 có công nợ phát sinh cả tháng 09 và tháng 10/2026",
     "1. Màn chính chỉ nhập Đến ngày 01/10/2026, bấm kính lúp\n"
     "2. Mở chi tiết NV-1",
     "Đến ngày: 01/10/2026",
     "- Màn chính chỉ tính phát sinh trước 01/10/2026\n"
     "- Lưu ý: cửa sổ chi tiết bỏ qua Đến ngày, vẫn tính cả tháng 10 nên lệch với màn chính"),
]
