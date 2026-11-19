# -*- coding: utf-8 -*-
"""Section I, II, III, IV - hien thi, bo loc, danh sach, lap phieu tu hop dong."""
from tc_data_role import MENU, MENU_HD, HD, KD1, KT1

SEC_I = [
    ("001", "Vào màn từ menu Kế toán", "P0",
     KD1 + ", đã lập ít nhất 1 phiếu",
     "1. " + MENU + "\n"
     "2. Quan sát tiêu đề và bảng",
     "—",
     "- Tiêu đề \"Danh sách yêu cầu hạch toán làm dịch vụ\"\n"
     "- Bảng tải dữ liệu, không báo lỗi"),

    ("002", "Vào màn từ menu Dịch vụ", "P1",
     KD1,
     "1. Mở menu Dịch vụ > bấm \"Yêu cầu hạch toán dịch vụ - HĐBH\"",
     "—",
     "- Mở cùng danh sách như từ menu Kế toán"),

    ("003", "Bố cục mặc định của danh sách", "P0",
     "KD-1 đã lập 12 phiếu",
     "1. Mở màn từ menu\n"
     "2. Quan sát từ trên xuống",
     "—",
     "- Hàng nút: Bộ lọc, Tạo mới, Xuất excel; không có nút In\n"
     "- Cột: STT, Ngày lập, Mã phiếu, Số đơn hàng/hợp đồng, Kinh doanh, Khách hàng, Tổng thanh toán, Người "
     "lập, Người duyệt, Ngày duyệt, Trạng thái, Hành động\n"
     "- 10 dòng mỗi trang, phiếu mới lập nhất lên đầu"),

    ("004", "Nhãn trạng thái đúng màu", "P2",
     "Có phiếu Đang tạo, Chờ duyệt, Không duyệt, Đã hạch toán",
     "1. Quan sát cột Trạng thái",
     "—",
     "- Đang tạo, Không duyệt: nhãn đỏ\n"
     "- Chờ duyệt: nhãn vàng\n"
     "- Đã hạch toán: nhãn xanh"),

    ("005", "Bấm Mã phiếu mở chi tiết ở tab mới", "P0",
     "YC-1 Chờ duyệt do KD-1 lập, kiểu Chi phí khác, HD-01",
     "1. KD-1 bấm Mã phiếu YC-1",
     "—",
     "- Mở tab mới, tiêu đề \"Yêu cầu hạch toán làm dịch vụ - <mã YC-1>\"\n"
     "- Có Kiểu hạch toán (khóa), Hợp đồng/đơn hàng (liên kết HD-01), Ghi chú, thông tin khách hàng, File "
     "đính kèm, tab Chi phí\n"
     "- Cuối trang có nút Quay lại"),

    ("006", "Bấm Số đơn hàng/hợp đồng mở hợp đồng", "P2",
     "YC-1 của HD-01",
     "1. Bấm số HD-01 ở cột Số đơn hàng/hợp đồng",
     "—",
     "- Mở chi tiết HD-01 ở tab mới"),

    ("007", "Chi tiết phiếu kiểu Dịch vụ hiện hợp đồng", "P1",
     "YC-3 kiểu Dịch vụ của HD-01, Chờ duyệt",
     "1. Mở chi tiết YC-3",
     "—",
     "- Mong đợi: có ô Hợp đồng/đơn hàng là HD-01\n"
     "- Lưu ý: theo code hiện tại hiện ô \"Phiếu yêu cầu làm dịch vụ\" để trống, không có hợp đồng - ghi "
     "Failed"),

    ("008", "Chi tiết phiếu kiểu Chi phí vận chuyển hiện hợp đồng", "P2",
     "YC-4 kiểu Chi phí vận chuyển của HD-01",
     "1. Mở chi tiết YC-4",
     "—",
     "- Mong đợi: có ô Hợp đồng/đơn hàng là HD-01\n"
     "- Lưu ý: nếu không có ô hợp đồng thì ghi Failed"),
]

SEC_II = [
    ("001", "Lọc theo Mã phiếu một phần", "P0",
     "Có phiếu TPE.YCHTDV.00015 và TPE.YCHTDV.00150",
     "1. Bấm Bộ lọc, gõ \"0015\" vào ô Mã\n"
     "2. Bấm Tìm kiếm",
     "Mã: 0015",
     "- Ra cả 2 phiếu"),

    ("002", "Lọc theo Số hợp đồng", "P0",
     "YC-1, YC-3 của HD-01; YC-5 của HD-02",
     "1. Gõ số HD-01 vào ô Số hợp đồng, tìm kiếm",
     "—",
     "- Chỉ ra YC-1, YC-3"),

    ("003", "Lọc theo Trạng thái", "P0",
     "Có 3 phiếu Chờ duyệt, 2 Đã hạch toán",
     "1. Chọn Trạng thái \"Chờ duyệt\", tìm kiếm",
     "—",
     "- Ra 3 phiếu Chờ duyệt"),

    ("004", "Lọc theo Khách hàng", "P1",
     "HD-01 của khách KH-1, HD-02 của KH-2",
     "1. Chọn Khách hàng KH-1, tìm kiếm",
     "—",
     "- Chỉ ra phiếu của HD-01"),

    ("005", "Lọc theo Người lập", "P1",
     "KD-1 lập 3 phiếu, KD-2 lập 2 phiếu; QL-1 có quyền xem của công ty",
     "1. QL-1 chọn Người lập KD-2, tìm kiếm",
     "—",
     "- Ra 2 phiếu của KD-2"),

    ("006", "Lọc theo Người yêu cầu (người lập hợp đồng)", "P1",
     "HD-01 do KD-1 lập, HD-02 do KD-2 lập",
     "1. QL-1 chọn Người yêu cầu KD-1, tìm kiếm",
     "—",
     "- Chỉ ra phiếu của các hợp đồng do KD-1 lập"),

    ("007", "Lọc theo Người duyệt", "P1",
     "YC-6 Đã hạch toán do KT-1 duyệt, YC-7 do KT-2 duyệt",
     "1. Chọn Người duyệt KT-1, tìm kiếm",
     "—",
     "- Mong đợi: chỉ ra YC-6\n"
     "- Lưu ý: theo code hiện tại ra cả YC-7 (ô Người duyệt không có tác dụng) - ghi Failed"),

    ("008", "Lọc Đến ngày", "P0",
     "YC-8 lập ngày 01/11/2026, YC-9 lập ngày 04/11/2026",
     "1. Chọn Đến ngày 02/11/2026, tìm kiếm",
     "—",
     "- Ra YC-8, không ra YC-9"),

    ("009", "Lọc Từ ngày", "P0",
     "YC-8 lập ngày 01/11/2026, YC-9 lập ngày 04/11/2026",
     "1. Chọn Từ ngày 03/11/2026, tìm kiếm",
     "—",
     "- Mong đợi: chỉ ra YC-9\n"
     "- Lưu ý: theo code hiện tại vẫn ra YC-8 (Từ ngày không có tác dụng) - ghi Failed"),

    ("010", "Lọc theo Công ty", "P1",
     "TGD có quyền xem của tổng công ty; TPE có 5 phiếu, TPC có 2 phiếu",
     "1. TGD chọn Công ty TPC, tìm kiếm",
     "—",
     "- Ra 2 phiếu do nhân viên TPC lập"),

    ("011", "Kết hợp nhiều điều kiện lọc", "P1",
     "HD-01 có YC-1 Chờ duyệt, YC-6 Đã hạch toán",
     "1. Gõ số HD-01, chọn Trạng thái \"Đã hạch toán\", tìm kiếm",
     "—",
     "- Chỉ ra YC-6"),

    ("012", "Lọc không có kết quả", "P2",
     "—",
     "1. Gõ Mã \"ZZZ999\", tìm kiếm",
     "—",
     "- Bảng báo không có dữ liệu, không lỗi"),
]

SEC_III = [
    ("001", "Phiếu Đang tạo của mình có Sửa, Xóa", "P0",
     "YC-2 Đang tạo do KD-1 lập",
     "1. KD-1 mở menu Hành động của YC-2",
     "—",
     "- Có Sửa và Xóa, không có Hạch toán dịch vụ"),

    ("002", "Phiếu Chờ duyệt không có Sửa, Xóa", "P0",
     "YC-1 Chờ duyệt do KD-1 lập",
     "1. KD-1 mở menu Hành động của YC-1",
     "—",
     "- Menu trống, không có Sửa, Xóa"),

    ("003", "Phiếu Không duyệt có lại Sửa, Xóa", "P0",
     "YC-10 Không duyệt do KD-1 lập",
     "1. KD-1 mở menu Hành động của YC-10",
     "—",
     "- Có Sửa và Xóa"),

    ("004", "Kế toán thấy Hạch toán dịch vụ ở phiếu Chờ duyệt", "P0",
     KT1 + "; YC-1 Chờ duyệt",
     "1. KT-1 mở danh sách chờ duyệt từ ô trang chủ\n"
     "2. Mở menu Hành động của YC-1",
     "—",
     "- Có \"Hạch toán dịch vụ\"\n"
     "- Không có Sửa, Xóa"),

    ("005", "Phiếu Đã hạch toán không còn thao tác", "P1",
     "YC-6 Đã hạch toán",
     "1. Người lập và KT-1 lần lượt mở menu Hành động của YC-6",
     "—",
     "- Không có Sửa, Xóa, Hạch toán dịch vụ"),

    ("006", "Cột Kinh doanh là người lập hợp đồng", "P1",
     "YC-1 do KD-1 lập, HD-01 do KD-1 lập; YC-11 do KD-2 lập cho HD-03 của KD-3",
     "1. Quan sát cột Kinh doanh và Người lập",
     "—",
     "- YC-11: Kinh doanh là KD-3 (kèm mã phòng)\n"
     "- Người lập là KD-2 (kèm mã phòng)"),

    ("007", "Tổng thanh toán hiện có dấu phân cách", "P2",
     "YC-1 Tổng thanh toán 3.300.000",
     "1. Quan sát cột Tổng thanh toán",
     "—",
     "- Hiện 3,300,000"),

    ("008", "Ngày duyệt hiện đúng định dạng", "P2",
     "YC-6 Đã hạch toán ngày 04/11/2026 09:30",
     "1. Quan sát cột Ngày duyệt",
     "—",
     "- Mong đợi: hiện 04/11/2026 - 09:30 như cột Ngày lập\n"
     "- Lưu ý: nếu hiện dạng năm-tháng-ngày giờ:phút:giây thì ghi Failed"),

    ("009", "Ô trang chủ đếm phiếu chờ duyệt", "P0",
     KT1 + "; TPE có 3 phiếu Chờ duyệt, TPC có 2",
     "1. KT-1 mở trang chủ, xem ô \"Yêu cầu hạch toán dịch vụ cần phê duyệt\"\n"
     "2. Bấm vào ô",
     "—",
     "- Ô hiện 3\n"
     "- Danh sách mở ra có đúng 3 phiếu Chờ duyệt của TPE"),

    ("010", "Xóa phiếu Đang tạo", "P0",
     "YC-2 Đang tạo do KD-1 lập",
     "1. KD-1 bấm Xóa ở YC-2, xác nhận",
     "—",
     "- Thông báo \"Xóa thành công!\"\n"
     "- YC-2 không còn trong danh sách"),

    ("011", "Xóa phiếu Không duyệt trả lại dòng cho hợp đồng", "P1",
     "YC-10 Không duyệt của HD-01 gồm CP1",
     "1. KD-1 xóa YC-10\n"
     "2. Lập phiếu Chi phí khác mới từ HD-01",
     "—",
     "- Xóa thành công\n"
     "- CP1 không bị tô đỏ, chọn và gửi duyệt được"),
]

SEC_IV = [
    ("001", "Lập phiếu Chi phí khác từ Danh sách HĐ", "P0",
     HD,
     "1. " + KD1 + "\n"
     "2. " + MENU_HD + ", ở HD-01 mở Hành động > \"Yêu cầu hạch toán chi phí\"",
     "—",
     "- Mở form \"Yêu cầu hạch toán dịch vụ\" ở tab mới\n"
     "- Kiểu hạch toán \"Chi phí khác\" bị khóa\n"
     "- Ô Chọn đơn hàng/hợp đồng có HD-01; hiện mã, tên khách hàng, địa chỉ\n"
     "- Tab Chi phí liệt kê CP1, chưa chọn dòng nào"),

    ("002", "Lập phiếu Dịch vụ từ Danh sách HĐ", "P0",
     HD,
     "1. KD-1 ở HD-01 bấm Hành động > \"Yêu cầu hạch toán dịch vụ\"",
     "—",
     "- Kiểu hạch toán \"Dịch vụ\" bị khóa\n"
     "- Tab Dịch vụ đi kèm liệt kê DV1, DV2 với Giá niêm yết, Doanh số vượt trội, Giảm giá, Giá trị sau giảm "
     "giá"),

    ("003", "Lập phiếu Chi phí vận chuyển từ Danh sách HĐ", "P0",
     HD,
     "1. KD-1 ở HD-01 bấm Hành động > \"Yêu cầu hạch toán chi phí vận chuyển\"",
     "—",
     "- Kiểu hạch toán \"Chi phí vận chuyển\" bị khóa, không có ô chọn hợp đồng\n"
     "- Bảng Chi phí có 1 dòng \"Chi phí vận chuyển\" 300.000, đã được chọn sẵn\n"
     "- VAT(8%) 24.000, Tổng sau thuế 324.000"),

    ("004", "Không có mục vận chuyển khi hợp đồng không có cước", "P1",
     "HD-02 Có hiệu lực, cước vận chuyển 0, không vượt trội, không giảm",
     "1. KD-1 mở Hành động của HD-02",
     "—",
     "- Không có \"Yêu cầu hạch toán chi phí vận chuyển\""),

    ("005", "Không có mục vận chuyển khi đã hạch toán vận chuyển", "P1",
     "HD-01 đã có phiếu hạch toán chi phí vận chuyển được duyệt",
     "1. KD-1 mở Hành động của HD-01",
     "—",
     "- Không còn \"Yêu cầu hạch toán chi phí vận chuyển\""),

    ("006", "Hợp đồng chưa Có hiệu lực không có mục yêu cầu", "P0",
     "HD-04 do KD-1 lập đang Chờ duyệt",
     "1. KD-1 mở Hành động của HD-04",
     "—",
     "- Không có các mục \"Yêu cầu hạch toán ...\""),

    ("007", "Người không lập hợp đồng không có mục yêu cầu", "P0",
     "HD-01 do KD-1 lập; KD-2 xem được HD-01",
     "1. Đăng nhập KD-2, mở Hành động của HD-01",
     "—",
     "- Không có các mục \"Yêu cầu hạch toán ...\""),

    ("008", "Dòng giảm không hiện khi lập phiếu", "P1",
     "HD-01 có thêm dòng CP2 giảm 100.000 do phụ lục giảm",
     "1. KD-1 lập phiếu Chi phí khác từ HD-01",
     "—",
     "- Tab Chi phí chỉ có CP1, không có dòng giảm CP2"),

    ("009", "Dòng đã gửi duyệt bị tô đỏ", "P0",
     "YC-1 Chờ duyệt của HD-01 đã gồm CP1",
     "1. KD-1 lập phiếu Chi phí khác mới từ HD-01",
     "—",
     "- Dòng CP1 tô đỏ (đã yêu cầu)"),

    ("010", "Hợp đồng chưa có Hỗ trợ hạch toán", "P0",
     "HD-05 Có hiệu lực do KD-1 lập, chưa có phiếu Hỗ trợ hạch toán, có chi phí CP5",
     "1. KD-1 lập phiếu Chi phí khác từ HD-05, chọn CP5\n"
     "2. Bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- Thông báo \"Hợp đồng không có hỗ trợ hạch toán\"\n"
     "- Không tạo phiếu"),

    ("011", "Tạo mới từ danh sách và chọn hợp đồng", "P1",
     HD,
     "1. KD-1 bấm Tạo mới ở danh sách\n"
     "2. Kiểu hạch toán chọn \"Chi phí khác\", bấm nút tìm ở ô Chọn đơn hàng/hợp đồng\n"
     "3. Chọn HD-01, xác nhận",
     "—",
     "- Popup \"Hợp đồng/Đơn hàng\" có cột Loại hợp đồng, Số hợp đồng, Khách hàng, Tổng thanh toán\n"
     "- Hỏi xác nhận \"Nếu bạn thay đổi hợp đồng các chi phí hiện có sẽ bị thay thế!\"\n"
     "- Sau khi xác nhận: tab Chi phí liệt kê CP1"),

    ("012", "Chọn hợp đồng của người khác trong popup", "P1",
     "HD-03 Có hiệu lực do KD-3 lập",
     "1. KD-1 bấm Tạo mới, chọn HD-03 trong popup",
     "—",
     "- Báo lỗi, không tải chi phí của HD-03"),

    ("013", "Ghi chú không bị thay bằng ghi chú hợp đồng", "P1",
     "HD-01 có ghi chú \"Giao trước 30/11\"",
     "1. KD-1 lập phiếu Chi phí khác từ HD-01\n"
     "2. Quan sát ô Ghi chú",
     "—",
     "- Mong đợi: ô Ghi chú trống để người lập nhập\n"
     "- Lưu ý: nếu ô Ghi chú tự điền \"Giao trước 30/11\" thì ghi Failed nếu nghiệp vụ không muốn vậy"),

    ("014", "Nút Hủy ở form quay về danh sách yêu cầu", "P2",
     "KD-1 đang ở form lập phiếu",
     "1. Bấm Hủy",
     "—",
     "- Mong đợi: về danh sách Yêu cầu hạch toán dịch vụ - HĐBH\n"
     "- Lưu ý: theo code hiện tại chuyển sang danh sách Phiếu yêu cầu làm dịch vụ - ghi Failed"),
]
