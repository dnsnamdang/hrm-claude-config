# -*- coding: utf-8 -*-
"""Section V, VI, VII - Luu / Luu & Duyet / Sua, man Chi tiet, but toan & cong no."""
from tc_data_role import MENU, MENU_YC, HD, YC1, YC2, KT1, TAO, TIEN_YC1

SEC_V = [
    ("001", "Bấm Lưu tạo phiếu Đang tạo", "P0",
     HD + "\n" + YC1 + "\n" + KT1,
     "1. " + TAO + "\n"
     "2. Nhập Ghi chú \"Lắp đặt tháng 11\", bấm Lưu",
     "—",
     "- Thông báo \"Thao tác thành công\", về danh sách\n"
     "- Phiếu mới mã TPE.HTDV.<5 số>, Trạng thái Đang tạo, " + TIEN_YC1 + "\n"
     "- Tab Hạch toán của phiếu chưa có bút toán"),

    ("002", "Lưu không đổi trạng thái phiếu yêu cầu", "P0",
     "KT-1 vừa Lưu HT-3 (Đang tạo) từ YC-1",
     "1. Mở Chi tiết YC-1",
     "—",
     "- YC-1 vẫn Chờ duyệt, NV-1 không nhận thông báo"),

    ("003", "Bấm Lưu & Duyệt khi tạo", "P0",
     HD + "\n" + YC1 + "\n" + KT1,
     "1. " + TAO + "\n"
     "2. Bấm \"Lưu & Duyệt\"",
     "—",
     "- Thông báo \"Thao tác thành công\", về danh sách\n"
     "- Phiếu mới Trạng thái Đã duyệt, Ngày duyệt là lúc bấm\n"
     "- Tab Hạch toán có bút toán (xem mục VII)"),

    ("004", "Lưu & Duyệt đổi phiếu yêu cầu sang Đã hạch toán", "P0",
     "KT-1 vừa Lưu & Duyệt HT-2 từ YC-1",
     "1. Mở Chi tiết YC-1",
     "—",
     "- YC-1 Trạng thái Đã hạch toán, Người duyệt KT-1\n"
     "- Không còn nút \"Hạch toán dịch vụ\", \"Không duyệt\""),

    ("005", "Người lập phiếu yêu cầu nhận thông báo", "P0",
     "KT-1 vừa Lưu & Duyệt HT-2 từ YC-1 (NV-1 lập)",
     "1. Đăng nhập NV-1, mở chuông thông báo",
     "—",
     "- Có \"Phiếu yêu cầu hạch toán làm dịch vụ của bạn đã được duyệt\"\n"
     "- Bấm vào mở Chi tiết YC-1"),

    ("006", "Lưu & Duyệt đổi đề nghị xuất dịch vụ gốc", "P1",
     "YC-1 được lập từ đề nghị xuất dịch vụ DN-1; KT-1 vừa Lưu & Duyệt HT-2 từ YC-1",
     "1. Mở Chi tiết DN-1",
     "—",
     "- DN-1 Trạng thái Đã hạch toán"),

    ("007", "Sửa phiếu Đang tạo rồi Lưu", "P1",
     "HT-3 Đang tạo do KT-1 lập từ YC-1",
     "1. KT-1 mở Sửa HT-3\n"
     "2. Đổi Ghi chú thành \"Đã kiểm tra\", bấm Lưu",
     "—",
     "- Thông báo \"Thao tác thành công\"\n"
     "- HT-3 vẫn Đang tạo, Ghi chú mới; YC-1 vẫn Chờ duyệt"),

    ("008", "Màn Sửa hiện đúng dữ liệu đã lưu", "P1",
     "HT-3 Đang tạo do KT-1 lập từ YC-1, Ghi chú \"Lắp đặt tháng 11\"",
     "1. KT-1 mở Sửa HT-3",
     "—",
     "- Ô phiếu yêu cầu YC-1, Ghi chú \"Lắp đặt tháng 11\"\n"
     "- Bảng chi tiết dòng \"Lắp đặt\" giống lúc tạo, " + TIEN_YC1),

    ("009", "Sửa rồi Lưu & Duyệt", "P0",
     HD + "\nHT-3 Đang tạo do KT-1 lập từ YC-1",
     "1. KT-1 mở Sửa HT-3, bấm \"Lưu & Duyệt\"",
     "—",
     "- HT-3 Đã duyệt, có bút toán như mục VII\n"
     "- YC-1 Đã hạch toán, NV-1 nhận thông báo đã được duyệt"),

    ("010", "Sửa rồi Lưu & Duyệt cập nhật ngày bàn giao hợp đồng", "P0",
     "HD-01 đã xuất hàng đủ; dịch vụ còn lại duy nhất là dòng trong YC-1; HT-3 Đang tạo do KT-1 lập từ YC-1",
     "1. KT-1 mở Sửa HT-3, bấm \"Lưu & Duyệt\"\n"
     "2. Mở Chi tiết HD-01, xem Ngày bàn giao và hạn thanh toán",
     "—",
     "- Mong đợi: Ngày bàn giao là hôm nay, hạn thanh toán = hôm nay cộng số ngày được nợ, giống khi Lưu & "
     "Duyệt ngay lúc tạo\n"
     "- Lưu ý: theo code hiện tại duyệt từ màn Sửa không cập nhật 2 ngày này - ghi Failed"),

    ("011", "Lưu & Duyệt khi tạo cập nhật ngày bàn giao hợp đồng", "P0",
     "HD-01 đã xuất hàng đủ; dịch vụ còn lại duy nhất là dòng trong YC-1",
     "1. " + TAO + ", bấm \"Lưu & Duyệt\"\n"
     "2. Mở Chi tiết HD-01",
     "—",
     "- Ngày bàn giao là hôm nay\n"
     "- Hạn thanh toán = hôm nay cộng số ngày được nợ của hợp đồng"),

    ("012", "Lưu & Duyệt khi hợp đồng chưa hạch toán hết", "P1",
     "HD-01 còn YC-2 (vận chuyển) chưa hạch toán",
     "1. " + TAO + ", bấm \"Lưu & Duyệt\"\n"
     "2. Mở Chi tiết HD-01",
     "—",
     "- Ngày bàn giao chưa được ghi, hạn thanh toán để trống"),

    ("013", "Duyệt dòng Chi phí vận chuyển đánh dấu hợp đồng", "P0",
     HD + "\n" + YC2,
     "1. KT-1 bấm \"Hạch toán dịch vụ\" ở YC-2, bấm \"Lưu & Duyệt\"\n"
     "2. NV-1 mở HD-01, thử lập thêm yêu cầu hạch toán vận chuyển",
     "—",
     "- HT mới Đã duyệt\n"
     "- HD-01 không cho lập thêm yêu cầu hạch toán vận chuyển"),

    ("014", "Chỉ Lưu dòng Chi phí vận chuyển không đánh dấu hợp đồng", "P1",
     HD + "\n" + YC2,
     "1. KT-1 bấm \"Hạch toán dịch vụ\" ở YC-2, bấm Lưu",
     "—",
     "- Phiếu Đang tạo; HD-01 chưa bị đánh dấu đã hạch toán vận chuyển"),

    ("015", "Bấm Lưu & Duyệt 2 lần liên tiếp", "P1",
     YC1,
     "1. " + TAO + "\n"
     "2. Bấm \"Lưu & Duyệt\" và bấm thêm lần nữa ngay",
     "—",
     "- Nút bị mờ trong lúc xử lý\n"
     "- Chỉ có 1 phiếu được tạo"),
]

SEC_VI = [
    ("001", "Chi tiết phiếu Đang tạo của mình", "P1",
     "HT-3 Đang tạo do KT-1 lập; KT-1 không có quyền \"Duyệt yêu cầu làm dịch vụ\"",
     "1. KT-1 bấm mã HT-3",
     "—",
     "- Mở Chi tiết, tab Hạch toán trống\n"
     "- Cuối trang chỉ có Quay lại"),

    ("002", "Nút Duyệt, Không duyệt ở Chi tiết", "P1",
     "HT-3 Đang tạo do KT-1 lập; KT-1 có quyền \"Duyệt yêu cầu làm dịch vụ\"",
     "1. KT-1 bấm mã HT-3",
     "—",
     "- Cuối trang có Không duyệt, Duyệt, Quay lại"),

    ("003", "Bấm Duyệt ở Chi tiết giữ đúng dòng chi phí", "P0",
     HD + "\nHT-3 Đang tạo do KT-1 lập từ YC-1; KT-1 có quyền \"Duyệt yêu cầu làm dịch vụ\"",
     "1. KT-1 mở Chi tiết HT-3, bấm Duyệt\n"
     "2. Mở lại Chi tiết HT-3, xem bảng chi tiết và tab Hạch toán",
     "—",
     "- Mong đợi: HT-3 Đã duyệt, vẫn là dòng \"Lắp đặt\" của YC-1, bút toán như mục VII\n"
     "- Lưu ý: theo code hiện tại nút Duyệt gửi nhầm mã dòng, phiếu có thể bị thay bằng dòng chi phí của "
     "một phiếu yêu cầu khác hoặc báo \"Thao tác thất bại\" - ghi Failed"),

    ("004", "Bấm Không duyệt ở Chi tiết", "P1",
     "HT-3 Đang tạo do KT-1 lập; KT-1 có quyền \"Duyệt yêu cầu làm dịch vụ\"",
     "1. KT-1 mở Chi tiết HT-3, bấm Không duyệt\n"
     "2. Nhập Ghi chú duyệt \"Sai số tiền\", bấm Xác nhận",
     "—",
     "- Mong đợi: HT-3 chuyển trạng thái không duyệt, lưu Ghi chú duyệt\n"
     "- Lưu ý: theo code hiện tại luôn báo \"Thao tác thất bại\" và phiếu không đổi - ghi Failed"),

    ("005", "Tab Hạch toán của phiếu Đã duyệt", "P0",
     "HT-2 Đã duyệt từ YC-1",
     "1. Mở Chi tiết HT-2, bấm tab Hạch toán",
     "—",
     "- Bảng bút toán chia nhóm: doanh thu, giảm trừ doanh thu, giá vốn, thưởng, thuế, quỹ rủi ro\n"
     "- Mỗi dòng có tài khoản, Nợ / Có, số tiền, đối tượng (khách hàng hoặc nhân viên)"),

    ("006", "Chi tiết hiện VAT theo kiểu phiếu", "P1",
     HD + "\nHT-8 Đã duyệt từ YC-2 (vận chuyển)",
     "1. Mở Chi tiết HT-8",
     "—",
     "- VAT(8%) 40,000; Tổng thành tiền 540,000"),

    ("007", "Quay lại từ Chi tiết", "P2",
     "Đang ở Chi tiết HT-2",
     "1. Bấm Quay lại",
     "—",
     "- Về danh sách Phiếu hạch toán dịch vụ"),
]

SEC_VII = [
    ("001", "Bút toán doanh thu kiểu Dịch vụ", "P0",
     HD + "\nKT-1 vừa Lưu & Duyệt HT-2 từ YC-1",
     "1. Mở tab Hạch toán của HT-2, xem nhóm doanh thu",
     "—",
     "- Nợ 1311 2.200.000 (khách KH-1)\n"
     "- Có 5113 2.000.000\n"
     "- Có 33311 200.000"),

    ("002", "Bút toán giảm trừ doanh thu", "P0",
     "HT-2 như trên",
     "1. Xem nhóm giảm trừ doanh thu",
     "—",
     "- Nợ 5213 200.000\n"
     "- Nợ 33311 20.000\n"
     "- Có 1311 220.000 (khách KH-1)"),

    ("003", "Bút toán giá vốn", "P0",
     "HT-2 như trên",
     "1. Xem nhóm giá vốn",
     "—",
     "- Nợ 632 1.200.000\n"
     "- Có 1541 1.200.000 gắn dòng \"Lắp đặt\""),

    ("004", "Công nợ khách hàng tăng đúng Tổng thanh toán", "P0",
     "Trước khi duyệt KH-1 dư nợ 1311 bằng 0; KT-1 vừa Lưu & Duyệt HT-2",
     "1. Mở báo cáo công nợ khách hàng, lọc KH-1, hợp đồng HD-01",
     "—",
     "- Phát sinh Nợ 2.200.000, phát sinh Có 220.000\n"
     "- Dư nợ cuối 1.980.000, bằng Tổng thanh toán của HT-2"),

    ("005", "Bút toán kiểu Vận chuyển không có giá vốn", "P0",
     HD + "\nKT-1 vừa Lưu & Duyệt HT-8 từ YC-2",
     "1. Mở tab Hạch toán của HT-8",
     "—",
     "- Nợ 1311 540.000 / Có 5113 500.000, Có 33311 40.000\n"
     "- Không có nhóm giá vốn, không có nhóm thưởng, quỹ rủi ro"),

    ("006", "Giảm giá bằng 0 không sinh bút toán giảm trừ", "P1",
     "HD-03 dịch vụ \"Bảo trì\" 1.000.000, giảm giá 0, VAT 10%; YC-5 Chờ duyệt",
     "1. KT-1 hạch toán YC-5, bấm \"Lưu & Duyệt\", xem tab Hạch toán",
     "—",
     "- Có nhóm doanh thu Nợ 1311 1.100.000\n"
     "- Không có dòng 5213"),

    ("007", "Bút toán thưởng theo tỷ lệ chỉ có ở kiểu Dịch vụ", "P1",
     "HD-01 có khai báo thưởng thực hiện hợp đồng, quỹ rủi ro phòng; HT-2 kiểu Dịch vụ, HT-9 kiểu Chi phí "
     "cùng HD-01, cùng Đã duyệt",
     "1. So sánh tab Hạch toán của HT-2 và HT-9",
     "—",
     "- HT-2 có nhóm thưởng thực hiện hợp đồng, thuế TNCN tạm tính, thưởng năng suất, quỹ rủi ro\n"
     "- HT-9 chỉ có doanh thu, giảm trừ, giá vốn"),

    ("008", "Phụ lục bổ sung ghi bút toán về hợp đồng gốc", "P0",
     "PL-01 là phụ lục bổ sung của HD-01; YC-6 kiểu Dịch vụ của PL-01 Chờ duyệt",
     "1. KT-1 hạch toán YC-6, bấm \"Lưu & Duyệt\"\n"
     "2. Mở báo cáo công nợ KH-1 theo hợp đồng",
     "—",
     "- Phát sinh công nợ nằm ở HD-01, không tách riêng PL-01"),

    ("009", "Phiếu Đang tạo không ghi công nợ", "P0",
     "KT-1 vừa Lưu HT-3 (Đang tạo) từ YC-1",
     "1. Mở báo cáo công nợ KH-1",
     "—",
     "- Không có phát sinh từ HT-3"),

    ("010", "Tổng thanh toán khớp số dư 1311 của phiếu", "P0",
     "HT-2 Đã duyệt",
     "1. Lấy Nợ 1311 trừ Có 1311 trong tab Hạch toán, so với Tổng thanh toán trên danh sách",
     "—",
     "- 2.200.000 trừ 220.000 = 1.980.000, bằng Tổng thanh toán"),
]
