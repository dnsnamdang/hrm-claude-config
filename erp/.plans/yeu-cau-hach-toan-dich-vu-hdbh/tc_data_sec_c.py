# -*- coding: utf-8 -*-
"""Section VIII, IX, X, XI - xuat excel, rang buoc nhap lieu, co lap / dong thoi, luong dau - cuoi."""
from tc_data_role import MENU, MENU_HD, HD, KD1, KT1

SEC_VIII = [
    ("001", "Xuất excel danh sách", "P0",
     "KD-1 có 3 phiếu",
     "1. " + MENU + "\n"
     "2. Bấm Xuất excel",
     "—",
     "- Tải file danh_sach_yeu_cau_hach_toan_lam_dich_vu.xlsx\n"
     "- Có tiêu đề công ty và bảng 11 cột: STT, Ngày lập, Mã phiếu, Số đơn hàng/hợp đồng, Kinh doanh, Khách "
     "hàng, Tổng thanh toán, Người lập, Người duyệt, Ngày duyệt, Trạng thái\n"
     "- Đủ 3 dòng"),

    ("002", "Excel theo bộ lọc đang chọn", "P0",
     "Có 3 phiếu Chờ duyệt, 2 Đã hạch toán",
     "1. Lọc Trạng thái \"Đã hạch toán\"\n"
     "2. Bấm Xuất excel",
     "—",
     "- File chỉ có 2 phiếu Đã hạch toán"),

    ("003", "Excel ghi khoảng ngày lọc", "P1",
     "—",
     "1. Chọn Đến ngày 05/11/2026, bấm Xuất excel",
     "—",
     "- Dòng tiêu đề ghi \"Đến ngày 05/11/2026\""),

    ("004", "Cột Kinh doanh trong Excel", "P1",
     "YC-11 do KD-2 lập cho HD-03 của KD-3",
     "1. Xuất excel, xem dòng YC-11",
     "—",
     "- Mong đợi: Kinh doanh là KD-3 như trên màn\n"
     "- Lưu ý: theo code hiện tại Kinh doanh là KD-2 (giống Người lập) - ghi Failed"),

    ("005", "Excel không có phiếu Đang tạo của người khác", "P0",
     "QL-1 có quyền xem của công ty; KD-1 có YC-2 Đang tạo",
     "1. QL-1 bấm Xuất excel",
     "—",
     "- File không có YC-2"),
]

SEC_IX = [
    ("001", "Gửi khi chưa chọn dòng chi phí nào", "P0",
     HD,
     "1. KD-1 lập phiếu Chi phí khác từ HD-01, không tích dòng nào\n"
     "2. Bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- Báo \"Bắt buộc chọn 1 chi phí\" dưới bảng Chi phí\n"
     "- Không tạo phiếu"),

    ("002", "Gửi phiếu Dịch vụ khi chưa chọn dòng", "P0",
     HD,
     "1. KD-1 lập phiếu Dịch vụ từ HD-01, không tích dòng nào, bấm Lưu",
     "—",
     "- Báo lỗi bắt buộc chọn dịch vụ dưới bảng Dịch vụ đi kèm\n"
     "- Không tạo phiếu"),

    ("003", "Tạo mới chưa chọn hợp đồng", "P0",
     "—",
     "1. KD-1 bấm Tạo mới, Kiểu hạch toán \"Chi phí khác\", không chọn hợp đồng\n"
     "2. Bấm Lưu",
     "—",
     "- Báo lỗi, không tạo phiếu"),

    ("004", "Đính kèm file đúng định dạng", "P1",
     HD,
     "1. KD-1 lập phiếu Chi phí khác, tích CP1, đính kèm hopdong.pdf (2MB)\n"
     "2. Bấm Lưu, mở chi tiết",
     "—",
     "- Lưu thành công, chi tiết có file hopdong.pdf"),

    ("005", "Đính kèm file sai định dạng", "P1",
     HD,
     "1. KD-1 đính kèm bangke.xlsx, bấm Lưu",
     "—",
     "- Báo \"Sai định dạng file quy định\", không tạo phiếu"),

    ("006", "Giới hạn dung lượng file khi lập và khi sửa", "P2",
     "File baocao.pdf 20MB",
     "1. KD-1 lập phiếu kèm baocao.pdf, bấm Lưu\n"
     "2. Mở Sửa một phiếu khác, đính kèm baocao.pdf, bấm Lưu",
     "—",
     "- Bước 1 lưu được (giới hạn 30MB)\n"
     "- Mong đợi: bước 2 cũng lưu được\n"
     "- Lưu ý: theo code hiện tại màn Sửa giới hạn 10MB và không nhận file zip - ghi Failed nếu nghiệp vụ "
     "yêu cầu giống nhau"),

    ("007", "Bấm Lưu liên tiếp nhiều lần", "P1",
     HD,
     "1. KD-1 lập phiếu, tích CP1, bấm Lưu 3 lần thật nhanh",
     "—",
     "- Nút Lưu bị khóa khi đang xử lý\n"
     "- Chỉ tạo 1 phiếu"),

    ("008", "Gọi thẳng chức năng lưu với Tổng thanh toán tự đặt", "P1",
     HD,
     "1. Dùng công cụ kiểm thử API gọi chức năng lưu phiếu Chi phí khác gồm CP1, Tổng thanh toán 1",
     "—",
     "- Mong đợi: Tổng thanh toán được tính lại là 550.000 hoặc bị từ chối\n"
     "- Lưu ý: theo code hiện tại lưu đúng số 1 - ghi Failed"),
]

SEC_X = [
    ("001", "Người khác không thấy phiếu Đang tạo", "P0",
     "YC-2 Đang tạo do KD-1 lập; QL-1 có quyền xem của tổng công ty",
     "1. QL-1 mở danh sách và lọc Mã YC-2",
     "—",
     "- Không có YC-2"),

    ("002", "Người khác mở chi tiết phiếu Đang tạo", "P0",
     "YC-2 Đang tạo do KD-1 lập",
     "1. QL-1 dán đường dẫn chi tiết YC-2",
     "—",
     "- Trang không tìm thấy"),

    ("003", "Danh sách chờ duyệt chỉ có phiếu công ty mình", "P0",
     KT1 + "; TPC có YC-14 Chờ duyệt",
     "1. KT-1 mở danh sách chờ duyệt từ ô trang chủ",
     "—",
     "- Không có YC-14"),

    ("004", "Gọi thẳng chức năng lưu cho hợp đồng người khác", "P1",
     "HD-03 Có hiệu lực do KD-3 lập, có chi phí CP3",
     "1. KD-1 dùng công cụ kiểm thử API gọi chức năng lưu phiếu Chi phí khác cho HD-03 gồm CP3, gửi duyệt",
     "—",
     "- Mong đợi: bị chặn vì KD-1 không lập HD-03\n"
     "- Lưu ý: theo code hiện tại tạo được phiếu Chờ duyệt và khóa CP3 của KD-3 - ghi Failed"),

    ("005", "Gọi thẳng chức năng lưu với chi phí của hợp đồng khác", "P1",
     "HD-01 của KD-1; CP3 thuộc HD-03",
     "1. KD-1 gọi chức năng lưu phiếu cho HD-01 nhưng gửi dòng CP3",
     "—",
     "- Mong đợi: bị chặn\n"
     "- Lưu ý: nếu lưu được phiếu HD-01 chứa CP3 thì ghi Failed"),

    ("006", "Hai tab cùng gửi duyệt một dòng lần lượt", "P0",
     HD,
     "1. KD-1 mở 2 tab lập phiếu Chi phí khác từ HD-01, cả 2 tích CP1\n"
     "2. Tab 1 bấm \"Lưu & Gửi duyệt\"\n"
     "3. Tab 2 bấm \"Lưu & Gửi duyệt\"",
     "—",
     "- Tab 1 thành công\n"
     "- Tab 2 báo \"Không thể yêu cầu hạch toán cho dịch vụ sửa chữa đã hoàn thành\""),

    ("007", "Hai tab cùng gửi duyệt đúng một lúc", "P1",
     HD,
     "1. KD-1 mở 2 tab lập phiếu Chi phí khác từ HD-01, cả 2 tích CP1\n"
     "2. Bấm \"Lưu & Gửi duyệt\" ở 2 tab cùng lúc",
     "—",
     "- Mong đợi: chỉ 1 phiếu Chờ duyệt chứa CP1\n"
     "- Lưu ý: nếu ra 2 phiếu Chờ duyệt cùng chứa CP1 thì ghi Failed"),

    ("008", "Người lập sửa trong lúc kế toán Không duyệt", "P2",
     "YC-10 Không duyệt; KD-1 đang mở Sửa YC-10",
     "1. KD-1 bấm \"Lưu & Gửi duyệt\"\n"
     "2. Cùng lúc KT-1 mở chi tiết YC-10",
     "—",
     "- YC-10 Chờ duyệt, KT-1 thấy nút Không duyệt và Hạch toán dịch vụ sau khi tải lại"),

    ("009", "Hai kế toán cùng xử lý một phiếu", "P1",
     "KT-1, KT-2 cùng có quyền Hạch toán; YC-1 Chờ duyệt",
     "1. KT-1 bấm Không duyệt YC-1\n"
     "2. KT-2 (đang mở chi tiết từ trước) bấm Hạch toán dịch vụ",
     "—",
     "- KT-2 báo \"Không thể yêu cầu hạch toán làm dịch vụ cho hợp đồng này\", không lập được phiếu hạch toán"),
]

SEC_XI = [
    ("001", "Luồng chi phí khác: lập, gửi, hạch toán", "P0",
     HD + "\n" + KT1,
     "1. " + KD1 + ", " + MENU_HD + ", HD-01 > \"Yêu cầu hạch toán chi phí\"\n"
     "2. Tích CP1, bấm \"Lưu & Gửi duyệt\"\n"
     "3. KT-1 bấm ô trang chủ, mở phiếu, bấm \"Hạch toán dịch vụ\", lưu và duyệt phiếu hạch toán",
     "—",
     "- Bước 2: phiếu Chờ duyệt 550,000, KT-1 nhận thông báo\n"
     "- Bước 3: phiếu Đã hạch toán, KD-1 nhận thông báo đã duyệt\n"
     "- Lập phiếu mới từ HD-01: CP1 tô đỏ"),

    ("002", "Luồng bị Không duyệt rồi gửi lại", "P0",
     HD + "\n" + KT1,
     "1. KD-1 gửi duyệt phiếu Dịch vụ gồm DV1, DV2\n"
     "2. KT-1 Không duyệt với ghi chú \"Thiếu DV2\"\n"
     "3. KD-1 Sửa phiếu, giữ DV1, DV2, bấm \"Lưu & Gửi duyệt\"\n"
     "4. KT-1 hạch toán",
     "—",
     "- Sau bước 2: phiếu Không duyệt, DV1, DV2 mở lại\n"
     "- Sau bước 3: phiếu Chờ duyệt 3,300,000\n"
     "- Sau bước 4: Đã hạch toán"),

    ("003", "Luồng chi phí vận chuyển", "P0",
     HD + "\n" + KT1,
     "1. KD-1 ở HD-01 bấm \"Yêu cầu hạch toán chi phí vận chuyển\", bấm \"Lưu & Gửi duyệt\"\n"
     "2. KT-1 hạch toán và duyệt\n"
     "3. KD-1 mở lại Hành động của HD-01",
     "—",
     "- Bước 1: phiếu Chờ duyệt 324,000\n"
     "- Bước 2: phiếu Đã hạch toán\n"
     "- Bước 3: không còn mục \"Yêu cầu hạch toán chi phí vận chuyển\""),

    ("004", "Luồng xóa phiếu nháp không ảnh hưởng hợp đồng", "P1",
     HD,
     "1. KD-1 lưu nháp phiếu Chi phí khác gồm CP1\n"
     "2. Xóa phiếu nháp\n"
     "3. Lập phiếu mới gồm CP1, gửi duyệt",
     "—",
     "- Bước 3 thành công, CP1 chỉ nằm trong 1 phiếu Chờ duyệt"),
]
