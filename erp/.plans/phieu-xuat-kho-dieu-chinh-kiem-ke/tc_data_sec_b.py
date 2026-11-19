# -*- coding: utf-8 -*-
"""Section V, VI, VII, VIII - luu / gui duyet / sua, ton ke toan, tru ton & duyet, in & excel."""
from tc_data_role import MENU, PKK, TON_KT, TK1, KT1, TAO

SEC_V = [
    ("001", "Lưu tạo phiếu Đang tạo", "P0",
     TK1 + "\n" + PKK + "\n" + TON_KT,
     "1. " + TAO + "\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Phiếu đã được gửi\", về màn danh sách\n"
     "- Có phiếu mới số PXKĐCKK-..., trạng thái Đang tạo, Kho K1, Người lập TK-1\n"
     "- PKK-1 chuyển trạng thái Đang xử lý"),

    ("002", "Gửi duyệt ngay khi tạo", "P0",
     TK1 + "\n" + PKK + "\n" + TON_KT,
     "1. " + TAO + "\n"
     "2. Bấm Gửi duyệt",
     "—",
     "- Báo \"Phiếu đã được gửi\"\n"
     "- Phiếu mới trạng thái Chờ duyệt\n"
     "- Người có quyền Kế toán kho nhận thông báo \"Bạn có 1 phiếu xuất kho điều chỉnh cần duyệt\""),

    ("003", "Số phiếu tăng dần", "P1",
     "Phiếu gần nhất là PXKĐCKK-00034",
     "1. Tạo phiếu mới từ một phiếu kiểm kê có hàng thiếu, bấm Lưu",
     "—",
     "- Số phiếu mới là PXKĐCKK-00035"),

    ("004", "Chi tiết phiếu sau khi lưu khớp dữ liệu lấy về", "P0",
     "Vừa Lưu phiếu PX-3 từ PKK-1",
     "1. Bấm Số phiếu PX-3",
     "—",
     "- 2 dòng: H1 P1 L01 SL xuất 5, Đơn giá 150,000, Thành tiền 750,000; H2 P2 L02 SL xuất 2, 250,000, "
     "500,000\n"
     "- Ghi chú \"Xuất thiếu sau kiểm kê\", có file PDF đã đính kèm"),

    ("005", "Mở Sửa phiếu Đang tạo", "P0",
     "PX-3 Đang tạo do TK-1 lập",
     "1. TK-1 mở Hành động > Sửa của PX-3",
     "—",
     "- Tiêu đề \"Phiếu xuất kho điều chỉnh kiểm kê PXKĐCKK-...\"\n"
     "- Hiện đúng Kho, Ghi chú, file cũ, bảng Chi tiết đã lưu\n"
     "- Nút Lưu, Gửi duyệt, Hủy"),

    ("006", "Sửa Ghi chú rồi Lưu", "P0",
     "PX-3 Đang tạo do TK-1 lập",
     "1. Mở Sửa PX-3, đổi Ghi chú thành \"Đã đối chiếu\"\n"
     "2. Bấm Lưu",
     "Ghi chú: Đã đối chiếu",
     "- Báo \"Phiếu đã được gửi\"\n"
     "- PX-3 vẫn Đang tạo, Ghi chú mới đã lưu"),

    ("007", "Sửa thêm file khi đã có file cũ", "P1",
     "PX-3 Đang tạo đã có 1 file PDF",
     "1. Mở Sửa PX-3, không thêm file, bấm Lưu\n"
     "2. Mở Sửa lại, thêm 1 file PDF mới, bấm Lưu",
     "—",
     "- Bước 1: lưu được (không bắt thêm file)\n"
     "- Bước 2: phiếu có 2 file"),

    ("008", "Gửi duyệt từ màn Sửa", "P0",
     "PX-3 Đang tạo do TK-1 lập",
     "1. Mở Sửa PX-3, bấm Gửi duyệt",
     "—",
     "- Báo \"Phiếu đã được gửi\"\n"
     "- PX-3 chuyển Chờ duyệt, mất nút Sửa\n"
     "- Kế toán kho nhận thông báo cần duyệt"),

    ("009", "Phiếu Chờ duyệt không sửa được", "P0",
     "PX-2 Chờ duyệt do TK-1 lập",
     "1. TK-1 dán đường dẫn Sửa PX-2",
     "—",
     "- Ra trang không tìm thấy"),

    ("010", "Đổi Kho ở màn Sửa", "P1",
     "PX-8 Đang tạo lập từ PKK-4 (kiểm kê K1, K2), Kho K1 có H1 = 5; K2 thiếu H6 = 1",
     "1. Mở Sửa PX-8, đổi Kho sang K2\n"
     "2. Bấm Lưu, mở Chi tiết PX-8",
     "—",
     "- Mong đợi: bảng đổi thành H6 = 1\n"
     "- Lưu ý: theo code hiện tại báo \"Không có quyền\", bảng vẫn là H1 của K1; lưu xong phiếu ghi Kho K2 "
     "nhưng hàng là của K1 - ghi Failed"),

    ("011", "Bấm Gửi duyệt hai lần liên tiếp", "P2",
     "Đang ở form tạo từ PKK-1",
     "1. Bấm Gửi duyệt rồi bấm ngay lần nữa",
     "—",
     "- Nút bị mờ khi đang gửi, chỉ tạo 1 phiếu"),
]


SEC_VI = [
    ("001", "Tồn kế toán đủ thì lưu được", "P0",
     PKK + "\n" + TON_KT,
     "1. " + TAO + ", bấm Gửi duyệt",
     "—",
     "- Lưu thành công (H1 xuất 5 trên 20, H2 xuất 2 trên 8)"),

    ("002", "Tồn kế toán không đủ thì chặn", "P0",
     PKK + "\nTồn kế toán TPE: H1 = 3, H2 = 8",
     "1. " + TAO + ", bấm Gửi duyệt",
     "—",
     "- Báo \"MH-H1: Tồn kế toán không đủ để xuất (SL được xuất: 3, SL xuất: 5). Kiểm tra hàng đang giữ "
     "chỗ/giữ hàng của công ty.\"\n"
     "- Không tạo phiếu, PKK-1 giữ nguyên trạng thái"),

    ("003", "Hàng bị giữ chỗ làm giảm SL được xuất", "P0",
     PKK + "\nTồn kế toán TPE: H1 = 5, trong đó 1 cái đang giữ chỗ cho khách",
     "1. " + TAO + ", bấm Lưu",
     "—",
     "- Báo tồn kế toán không đủ, SL được xuất: 4, SL xuất: 5"),

    ("004", "Nút Lưu cũng kiểm tra tồn kế toán", "P1",
     PKK + "\nTồn kế toán TPE: H1 = 3",
     "1. " + TAO + ", bấm Lưu",
     "—",
     "- Báo tồn kế toán không đủ, không tạo phiếu Đang tạo"),

    ("005", "Gộp nhiều dòng cùng hàng khi kiểm tra", "P0",
     "PKK-7 kho K1: H1 thiếu 3 ở P1 lô L01 và thiếu 3 ở P2 lô L05 (cùng của TPE); tồn kế toán TPE H1 = 5",
     "1. Mở form từ PKK-7, thêm file, nhập Ghi chú, bấm Gửi duyệt",
     "—",
     "- Báo tồn kế toán không đủ, SL được xuất: 5, SL xuất: 6\n"
     "- Không tạo phiếu"),

    ("006", "Lô của hai công ty thuê kho tách riêng khi kiểm tra", "P1",
     "PKK-8 kho K1: H1 thiếu 3 ở lô L01 của TPE, thiếu 2 ở lô L09 của TPC; tồn kế toán TPE H1 = 3, TPC H1 = 2",
     "1. Mở form từ PKK-8, thêm file, nhập Ghi chú, bấm Gửi duyệt",
     "—",
     "- Lưu thành công (mỗi công ty đủ tồn)"),

    ("007", "Sửa phiếu khi tồn kế toán đã giảm", "P1",
     "PX-3 Đang tạo có H1 = 5; sau khi lưu, tồn kế toán TPE H1 giảm còn 4 do có phiếu xuất khác",
     "1. Mở Sửa PX-3, bấm Gửi duyệt",
     "—",
     "- Báo tồn kế toán không đủ (SL được xuất: 4, SL xuất: 5), PX-3 vẫn Đang tạo"),
]


SEC_VII = [
    ("001", "Gửi duyệt khi tạo trừ tồn kho vật lý ngay", "P0",
     PKK + "\n" + TON_KT,
     "1. " + TAO + ", bấm Gửi duyệt\n"
     "2. Mở Báo cáo tồn kho theo vị trí, kho K1",
     "—",
     "- Vị trí P1: H1 lô L01 còn 15 (trước 20)\n"
     "- Vị trí P2: H2 lô L02 còn 6 (trước 8)"),

    ("002", "Gửi duyệt trừ tồn tổng của kho", "P0",
     "Trước khi gửi: tồn H1 tại K1 (mọi vị trí) = 30",
     "1. Gửi duyệt phiếu có H1 = 5 tại K1\n"
     "2. Mở Báo cáo tồn kho tổng hợp theo mặt hàng, kho K1",
     "—",
     "- H1 còn 25"),

    ("003", "Lưu Đang tạo chưa trừ tồn", "P0",
     "Tồn H1 tại P1 lô L01 = 20",
     "1. " + TAO + ", bấm Lưu\n"
     "2. Xem tồn H1 tại P1 lô L01",
     "—",
     "- Vẫn 20"),

    ("004", "Gửi duyệt từ màn Sửa phải trừ tồn", "P0",
     "PX-3 Đang tạo có H1 P1 L01 = 5; tồn H1 tại P1 lô L01 = 20",
     "1. Mở Sửa PX-3, bấm Gửi duyệt\n"
     "2. Xem tồn H1 tại P1 lô L01",
     "—",
     "- Mong đợi: còn 15\n"
     "- Lưu ý: theo code hiện tại vẫn 20 (không trừ tồn) - ghi Failed"),

    ("005", "Gửi duyệt chưa trừ tồn kế toán", "P0",
     TON_KT,
     "1. Gửi duyệt phiếu có H1 = 5\n"
     "2. Xem tồn kế toán H1 của TPE",
     "—",
     "- Vẫn 20 (chỉ trừ khi Phiếu xuất hàng điều chỉnh kiểm kê hoàn thành)"),

    ("006", "Kế toán kho tạo phiếu xuất hàng từ phiếu Chờ duyệt", "P0",
     KT1 + "; PX-2 Chờ duyệt có H1 = 5, H2 = 2",
     "1. KT-1 mở Hành động > \"Tạo phiếu xuất hàng\" của PX-2",
     "—",
     "- Mở form Phiếu xuất hàng điều chỉnh kiểm kê, đã có sẵn PX-2 và 2 dòng hàng H1 = 5, H2 = 2"),

    ("007", "Phiếu xuất hàng còn Đang tạo thì phiếu này Đang hạch toán", "P0",
     KT1 + "; PX-2 Chờ duyệt",
     "1. KT-1 tạo phiếu xuất hàng từ PX-2, chọn kho kế toán, bấm lưu ở trạng thái Đang tạo\n"
     "2. Quay lại danh sách phiếu xuất kho điều chỉnh kiểm kê",
     "—",
     "- PX-2 trạng thái Đang hạch toán\n"
     "- Mất nút \"Tạo phiếu xuất hàng\""),

    ("008", "Phiếu xuất hàng hoàn thành thì phiếu này Đã hạch toán", "P0",
     KT1 + "; PX-2 Chờ duyệt có H1 = 5; " + TON_KT,
     "1. KT-1 tạo phiếu xuất hàng từ PX-2, chọn kho kế toán, bấm hoàn thành\n"
     "2. Xem PX-2 và tồn kế toán H1",
     "—",
     "- PX-2 Đã hạch toán, nhãn xanh\n"
     "- Tồn kế toán H1 của TPE còn 15"),

    ("009", "Người duyệt, ngày duyệt sau khi hạch toán", "P1",
     "KT-1 vừa tạo phiếu xuất hàng từ PX-2 ngày 27/10/2026",
     "1. In danh sách có PX-2, đọc cột Người duyệt, Ngày duyệt",
     "—",
     "- Người duyệt KT-1, Ngày duyệt 27/10/2026"),

    ("010", "Không có nút Không duyệt / trả lại", "P2",
     KT1 + "; PX-2 Chờ duyệt",
     "1. KT-1 mở Chi tiết PX-2 và nút Hành động",
     "—",
     "- Không có Duyệt, Không duyệt; chỉ có \"Tạo phiếu xuất hàng\" và In\n"
     "- Phiếu Chờ duyệt đã trừ tồn không có cách trả lại"),
]


SEC_VIII = [
    ("001", "In một phiếu", "P0",
     "PX-2 kho K1 lập từ PKK-1, Ghi chú \"Xuất thiếu sau kiểm kê\"",
     "1. Mở Hành động > In của PX-2",
     "—",
     "- Mở bản in khổ ngang ở tab mới\n"
     "- Có Số phiếu, Ngày lập, Kho K1, Ghi chú, Phiếu kiểm kê PKK-1\n"
     "- Bảng: STT, Tên hàng, Model, Mã hàng, ĐVT, Vị trí, Lô, cột số lượng với H1 = 5, H2 = 2"),

    ("002", "Tên cột số lượng trên bản in", "P2",
     "PX-2 có hàng",
     "1. In PX-2, đọc tiêu đề cột số lượng",
     "—",
     "- Mong đợi: \"SL xuất\"\n"
     "- Lưu ý: hiện ghi \"SL nhập\" - ghi Failed"),

    ("003", "In danh sách chỉ gồm phiếu đã hạch toán", "P0",
     "Bộ lọc Trạng thái Đã hạch toán còn PX-4 (KT-1 duyệt ngày 20/10/2026)",
     "1. Bấm In",
     "—",
     "- Bản in có cột STT, Số phiếu, Phiếu kiểm kê, Kho, Người lập, Ngày lập, Người duyệt, Ngày duyệt, Trạng "
     "thái; dòng PX-4 đủ thông tin"),

    ("004", "In danh sách có phiếu chưa duyệt", "P0",
     "Danh sách có PX-2 Chờ duyệt (chưa có người duyệt)",
     "1. Không lọc gì, bấm In",
     "—",
     "- Mong đợi: bản in đủ các phiếu, ô Người duyệt / Ngày duyệt của PX-2 để trống\n"
     "- Lưu ý: theo code hiện tại trang in báo lỗi - ghi Failed"),

    ("005", "Xuất Excel danh sách", "P0",
     "Bộ lọc Trạng thái Đã hạch toán còn PX-4",
     "1. Bấm Xuất excel",
     "—",
     "- Tải file \"danh_sach_phieu_xuat_kho_dieu_chinh_kiem_ke.xlsx\", tiêu đề \"Danh sách phiếu xuất kho "
     "điều chỉnh kiểm kê\", có dòng PX-4"),

    ("006", "Xuất Excel danh sách có phiếu chưa duyệt", "P0",
     "Danh sách có PX-2 Chờ duyệt",
     "1. Không lọc gì, bấm Xuất excel",
     "—",
     "- Mong đợi: tải được file đủ phiếu\n"
     "- Lưu ý: theo code hiện tại báo lỗi, không tải được file - ghi Failed"),

    ("007", "In danh sách theo bộ lọc đang chọn", "P1",
     "Có 3 phiếu Đã hạch toán, 2 Chờ duyệt",
     "1. Lọc Trạng thái Đã hạch toán, bấm In",
     "—",
     "- Bản in có đúng 3 phiếu"),

    ("008", "Tiêu đề cột ngày duyệt trên bản in danh sách", "P2",
     "Bộ lọc còn phiếu Đã hạch toán",
     "1. Bấm In, đọc tiêu đề các cột",
     "—",
     "- Mong đợi: \"Ngày duyệt\"\n"
     "- Lưu ý: hiện ghi \"Ngày duyêtk\" - ghi Failed"),
]
