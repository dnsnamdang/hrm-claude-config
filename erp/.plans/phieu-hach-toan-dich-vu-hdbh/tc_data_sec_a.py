# -*- coding: utf-8 -*-
"""Section I, II, III, IV - hien thi, bo loc, danh sach, lap phieu tu phieu yeu cau."""
from tc_data_role import MENU, MENU_YC, HD, YC1, YC2, KT1, TAO, TIEN_YC1

SEC_I = [
    ("001", "Vào màn từ menu Kế toán", "P0",
     KT1 + ", đã lập ít nhất 1 phiếu",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề và bảng",
     "—",
     "- Tiêu đề \"Danh sách hạch toán dịch vụ\"\n"
     "- Bảng tải dữ liệu, không báo lỗi"),

    ("002", "Các cột của bảng danh sách", "P0",
     "KT-1 đã lập HT-2 (Đã duyệt) từ YC-1",
     "1. Mở màn từ menu, quan sát tiêu đề cột",
     "—",
     "- STT, Ngày lập, Mã, Số hợp đồng, Khách hàng, Tổng thanh toán, Người lập, Ngày duyệt, Trạng thái, Hành "
     "động\n"
     "- Phiếu mới lập nhất lên đầu"),

    ("003", "Dữ liệu một dòng Đã duyệt", "P0",
     HD + "\n" + YC1 + "\nKT-1 đã Lưu & Duyệt HT-2 từ YC-1",
     "1. Mở màn, tìm dòng HT-2",
     "—",
     "- Mã dạng TPE.HTDV.<5 số>\n"
     "- Số hợp đồng HD-01 (bấm được), Khách hàng \"<mã> - <tên> của KH-1\"\n"
     "- Tổng thanh toán 1,980,000; Người lập KT-1; Trạng thái Đã duyệt (nhãn xanh)"),

    ("004", "Cột Ngày duyệt hiển thị đúng định dạng", "P2",
     "HT-2 Đã duyệt lúc 09:30 ngày 05/11/2026",
     "1. Quan sát cột Ngày duyệt của HT-2",
     "—",
     "- Mong đợi: 05/11/2026 - 09:30 giống cột Ngày lập\n"
     "- Lưu ý: theo code hiện tại hiện dạng 2026-11-05 09:30:00 - ghi Failed"),

    ("005", "Bấm Mã mở màn Chi tiết", "P0",
     "HT-2 Đã duyệt",
     "1. Bấm mã HT-2",
     "—",
     "- Mở Chi tiết có 2 tab Thông tin, Hạch toán\n"
     "- Ô Hợp đồng / đơn hàng, Phiếu yêu cầu hạch toán (liên kết YC-1), Ghi chú\n"
     "- Cuối trang chỉ có nút Quay lại"),

    ("006", "Bấm liên kết phiếu yêu cầu ở Chi tiết", "P2",
     "Đang ở Chi tiết HT-2",
     "1. Bấm YC-1",
     "—",
     "- Mở Chi tiết YC-1 ở tab mới"),

    ("007", "Phiếu Đã duyệt không có Sửa, Xóa", "P0",
     "HT-2 Đã duyệt do KT-1 lập",
     "1. KT-1 mở nút Hành động của HT-2",
     "—",
     "- Không có Sửa, không có Xóa"),

    ("008", "Phiếu Đang tạo của mình có Sửa, Xóa", "P0",
     "HT-3 Đang tạo do KT-1 lập",
     "1. KT-1 mở nút Hành động của HT-3",
     "—",
     "- Có Sửa và Xóa\n"
     "- Trạng thái Đang tạo (nhãn xanh dương)"),
]

SEC_II = [
    ("001", "Lọc theo Mã một phần", "P1",
     "Có TPE.HTDV.00012 và TPE.HTDV.00013",
     "1. Gõ \"00012\" vào ô Mã, bấm Tìm",
     "—",
     "- Chỉ còn TPE.HTDV.00012"),

    ("002", "Lọc theo Số hợp đồng", "P0",
     "HT-2 của HD-01, HT-7 của HD-02",
     "1. Gõ \"HD-01\" vào ô Số hợp đồng, bấm Tìm",
     "—",
     "- Chỉ còn HT-2"),

    ("003", "Lọc theo Trạng thái", "P1",
     "HT-2 Đã duyệt, HT-3 Đang tạo (cùng của KT-1)",
     "1. Chọn Trạng thái Đang tạo, bấm Tìm",
     "—",
     "- Chỉ còn HT-3"),

    ("004", "Lọc theo Khách hàng", "P0",
     "HT-2 của KH-1, HT-7 của KH-2",
     "1. Chọn Khách hàng KH-1, bấm Tìm",
     "—",
     "- Chỉ còn HT-2"),

    ("005", "Lọc theo Dịch vụ", "P1",
     "HT-2 gồm dịch vụ \"Lắp đặt\", HT-8 gồm \"Chi phí vận chuyển\"",
     "1. Chọn Dịch vụ \"Lắp đặt\", bấm Tìm",
     "—",
     "- Chỉ còn HT-2"),

    ("006", "Lọc khoảng Số tiền", "P1",
     "HT-2 tổng 1.980.000, HT-8 tổng 540.000",
     "1. Nhập Số tiền từ 1.000.000, Số tiền đến 2.000.000, bấm Tìm",
     "—",
     "- Chỉ còn HT-2"),

    ("007", "Lọc Số tiền đúng bằng biên", "P2",
     "HT-8 tổng 540.000",
     "1. Nhập Số tiền từ 540.000, Số tiền đến 540.000, bấm Tìm",
     "—",
     "- Có HT-8"),

    ("008", "Lọc Từ ngày / Đến ngày theo Ngày lập", "P0",
     "HT-2 lập 03/11/2026, HT-8 lập 05/11/2026",
     "1. Chọn Từ ngày 05/11/2026, Đến ngày 05/11/2026, bấm Tìm",
     "—",
     "- Chỉ còn HT-8 (phiếu lập cuối ngày 05/11 vẫn có)"),

    ("009", "Lọc theo Người duyệt", "P1",
     "HT-2 do KT-1 duyệt, HT-9 do KT-5 duyệt",
     "1. Chọn Người duyệt KT-1, bấm Tìm",
     "—",
     "- Mong đợi: chỉ còn HT-2\n"
     "- Lưu ý: theo code hiện tại ô này không có tác dụng, vẫn ra cả HT-9 - ghi Failed"),

    ("010", "Lọc Công ty khi có quyền theo tổng công ty", "P1",
     "KT-3 có quyền theo tổng công ty; HT-2 của TPE, HT-5 của TPC",
     "1. KT-3 chọn Công ty TPC, bấm Tìm",
     "—",
     "- Chỉ còn HT-5"),

    ("011", "Không ra kết quả", "P2",
     "—",
     "1. Gõ \"KHONGCO\" vào ô Mã, bấm Tìm",
     "—",
     "- Bảng ghi không có dữ liệu, không báo lỗi"),

    ("012", "Làm mới bộ lọc", "P2",
     "Đang lọc Khách hàng KH-1",
     "1. Bấm nút làm mới bộ lọc",
     "—",
     "- Các ô lọc trống, bảng hiện lại toàn bộ"),
]

SEC_III = [
    ("001", "Phân trang danh sách", "P2",
     "Có 25 phiếu",
     "1. Mở màn, bấm sang trang 2",
     "—",
     "- Trang 2 có phiếu tiếp theo, STT nối tiếp"),

    ("002", "Bấm Số hợp đồng mở hợp đồng", "P2",
     "HT-2 của HD-01",
     "1. Bấm HD-01 ở cột Số hợp đồng",
     "—",
     "- Mở Chi tiết hợp đồng HD-01"),

    ("003", "Xóa phiếu Đang tạo", "P0",
     "HT-3 Đang tạo do KT-1 lập từ YC-1; YC-1 Chờ duyệt",
     "1. KT-1 mở Hành động của HT-3, bấm Xóa\n"
     "2. Bấm xác nhận",
     "—",
     "- Thông báo \"Xóa thành công!\", HT-3 mất khỏi danh sách\n"
     "- YC-1 vẫn Chờ duyệt, vẫn có nút \"Hạch toán dịch vụ\""),

    ("004", "Hủy hộp xác nhận xóa", "P2",
     "HT-3 Đang tạo do KT-1 lập",
     "1. Bấm Xóa ở HT-3, bấm Hủy ở hộp xác nhận",
     "—",
     "- HT-3 vẫn còn"),

    ("005", "Xóa phiếu Đã duyệt qua đường dẫn", "P0",
     "HT-2 Đã duyệt do KT-1 lập; KT-1 có đường dẫn Xóa HT-2",
     "1. KT-1 dán đường dẫn Xóa HT-2",
     "—",
     "- Thông báo \"Không thể xóa!\"\n"
     "- HT-2 và bút toán còn nguyên"),

    ("006", "Xóa phiếu của người khác qua đường dẫn", "P1",
     "HT-3 Đang tạo của KT-1; KT-5 có đường dẫn Xóa HT-3",
     "1. Đăng nhập KT-5, dán đường dẫn",
     "—",
     "- Thông báo \"Không thể xóa!\", HT-3 còn nguyên"),

    ("007", "Nút Tạo mới trên danh sách", "P1",
     KT1 + "\n" + YC1,
     "1. Bấm Tạo mới trên danh sách",
     "—",
     "- Mở form \"Phiếu hạch toán dịch vụ\" trống, ô phiếu yêu cầu chưa chọn\n"
     "- Bảng chi tiết trống"),
]

SEC_IV = [
    ("001", "Bấm Hạch toán dịch vụ từ Chi tiết phiếu yêu cầu", "P0",
     HD + "\n" + YC1 + "\n" + KT1,
     "1. " + MENU_YC + ", bấm mã YC-1\n"
     "2. Bấm \"Hạch toán dịch vụ\"",
     "—",
     "- Mở form Phiếu hạch toán dịch vụ, ô phiếu yêu cầu là mã YC-1\n"
     "- Thông tin khách KH-1 (mã, tên, MST, điện thoại, địa chỉ)\n"
     "- Tài khoản nợ 1311, doanh thu 5113, giá vốn 632, chiết khấu 5211, thuế 33311"),

    ("002", "Bấm Hạch toán dịch vụ từ danh sách phiếu yêu cầu", "P1",
     YC1 + "\n" + KT1,
     "1. " + MENU_YC + "\n"
     "2. Mở Hành động của YC-1, bấm \"Hạch toán dịch vụ\"",
     "—",
     "- Mở form như khi bấm từ Chi tiết YC-1"),

    ("003", "Bảng chi tiết lấy đúng từ phiếu yêu cầu", "P0",
     HD + "\n" + YC1,
     "1. " + TAO + "\n"
     "2. Quan sát tab Dịch vụ đi kèm",
     "—",
     "- 1 dòng \"Lắp đặt\": Giá niêm yết 2,000,000; Doanh số vượt trội 0; Giá bán 2,000,000; Giảm giá "
     "200000; Giá trên hợp đồng 1800000; Giá vốn 1,200,000\n"
     "- Không ô nào sửa được"),

    ("003b", "Định dạng số cột Giảm giá, Giá trên hợp đồng", "P2",
     HD + "\n" + YC1,
     "1. " + TAO + "\n"
     "2. Quan sát cột Doanh số vượt trội, Giảm giá, Giá trên hợp đồng",
     "—",
     "- Mong đợi: có dấu phân cách hàng nghìn như cột Giá niêm yết (200,000; 1,800,000)\n"
     "- Lưu ý: theo code hiện tại hiện số trần 200000, 1800000 - ghi Failed"),

    ("004", "Dòng tổng và VAT kiểu Dịch vụ", "P0",
     HD + "\n" + YC1,
     "1. " + TAO + "\n"
     "2. Quan sát phần cuối bảng",
     "—",
     "- Tổng Giá trên hợp đồng 1,800,000; Tổng giá vốn 1,200,000\n"
     "- VAT(10%) 180,000; Tổng thành tiền 1,980,000"),

    ("005", "Tổng Giảm giá nằm đúng cột", "P2",
     HD + "\n" + YC1,
     "1. " + TAO + "\n"
     "2. Quan sát dòng Tổng",
     "—",
     "- Mong đợi: tổng giảm giá 200,000 nằm dưới cột Giảm giá\n"
     "- Lưu ý: theo code hiện tại số này nằm dưới cột Giá bán - ghi Failed"),

    ("006", "VAT kiểu Vận chuyển lấy theo VAT vận chuyển", "P0",
     HD + "\n" + YC2,
     "1. KT-1 bấm \"Hạch toán dịch vụ\" ở YC-2\n"
     "2. Quan sát tab Chi phí",
     "—",
     "- Dòng \"Chi phí vận chuyển\" 500,000\n"
     "- VAT(8%) 40,000; Tổng thành tiền 540,000"),

    ("007", "Ô Tên viết tắt của khách hàng", "P2",
     "KH-1 có tên viết tắt \"ABC\"\n" + YC1,
     "1. " + TAO + "\n"
     "2. Quan sát ô Tên viết tắt",
     "—",
     "- Mong đợi: ABC\n"
     "- Lưu ý: theo code hiện tại luôn hiện \"_____\" - ghi Failed"),

    ("008", "Chọn phiếu yêu cầu bằng nút tìm trên form trống", "P1",
     YC1 + " (do NV-1 lập)\n" + KT1,
     "1. KT-1 bấm Tạo mới trên danh sách\n"
     "2. Bấm nút tìm ở ô \"Chọn phiếu yêu cầu hạch toán dịch vụ\"",
     "—",
     "- Mong đợi: hộp chọn liệt kê các phiếu yêu cầu Chờ duyệt KT-1 được hạch toán, có YC-1\n"
     "- Lưu ý: theo code hiện tại hộp chỉ liệt kê phiếu yêu cầu do chính KT-1 lập (mọi trạng thái), không có "
     "YC-1 - ghi Failed"),

    ("009", "Đổi phiếu yêu cầu hỏi xác nhận", "P2",
     "Form đang có YC-1; KT-1 tự lập YC-3 Chờ duyệt",
     "1. Bấm nút tìm, chọn YC-3",
     "—",
     "- Hỏi \"Nếu bạn thay đổi phiếu yêu cầu, các thông tin sẽ thay đổi theo!\"\n"
     "- Bấm Xác nhận: ô phiếu yêu cầu thành YC-3, bảng chi tiết đổi theo YC-3"),

    ("010", "Mở form với phiếu yêu cầu không còn Chờ duyệt", "P1",
     "YC-4 đã Đã hạch toán; KT-1 có đường dẫn tạo phiếu kèm YC-4",
     "1. KT-1 dán đường dẫn tạo phiếu kèm YC-4",
     "—",
     "- Báo \"Không thể yêu cầu hạch toán làm dịch vụ cho hợp đồng này\"\n"
     "- Bảng chi tiết trống"),

    ("011", "Lưu khi chưa chọn phiếu yêu cầu", "P0",
     KT1,
     "1. Bấm Tạo mới, không chọn phiếu yêu cầu, bấm Lưu",
     "—",
     "- Báo \"Thao tác thất bại\", dưới ô phiếu yêu cầu hiện \"Chọn một hợp đồng\"\n"
     "- Không tạo phiếu"),

    ("012", "Nút Hủy trên form", "P2",
     "Đang ở form tạo từ YC-1",
     "1. Bấm Hủy",
     "—",
     "- Quay về danh sách Phiếu hạch toán dịch vụ, không tạo phiếu"),
]
