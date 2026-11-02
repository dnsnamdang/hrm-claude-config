# -*- coding: utf-8 -*-
"""Section V, VI, VII - phan bo kho ke toan, luu / luu va duyet / sua, ton ke toan & gia von & but toan."""
from tc_data_role import MENU, MENU_PXK, PKK, GIA, KKT, KT1, TAO, LUU_DUYET

SEC_V = [
    ("001", "Chọn kho kế toán dòng đầu tự điền cho các dòng khác", "P0",
     PKK + "; " + KKT,
     "1. " + TAO + "\n"
     "2. Chọn KKT-A ở dòng kho kế toán đầu tiên của H1",
     "—",
     "- Dòng kho kế toán đầu tiên của H2 cũng tự chọn KKT-A\n"
     "- Số lượng tự điền bằng SL xuất: H1 3, H2 1"),

    ("002", "SL được xuất hiện theo kho kế toán đã chọn", "P0",
     PKK + "; " + KKT,
     "1. " + TAO + "\n"
     "2. Chọn KKT-A cho H1, quan sát SL được xuất\n"
     "3. Đổi sang KKT-B",
     "—",
     "- Bước 2: SL được xuất = 10\n"
     "- Bước 3: SL được xuất = 2"),

    ("003", "SL được xuất đã trừ hàng đang giữ / chờ lấy", "P0",
     PKK + "; " + KKT + "; tại KKT-A có 6 cái H1 đang được giữ cho khách",
     "1. " + TAO + "\n"
     "2. Chọn KKT-A cho H1",
     "—",
     "- SL được xuất = 4"),

    ("004", "Thêm kho để chia SL của một dòng", "P0",
     "Đang ở form lập từ PXK-1, H1 SL xuất 3",
     "1. Bấm \"Thêm kho\" ở dòng H1\n"
     "2. Dòng 1 chọn KKT-A Số lượng 1; dòng 2 chọn KKT-B Số lượng 2",
     "—",
     "- H1 có 2 dòng kho kế toán: KKT-A 1, KKT-B 2"),

    ("005", "Số lượng kho kế toán không vượt phần còn lại", "P0",
     "H1 SL xuất 3, đã có KKT-A 1 và dòng thứ 2 chọn KKT-B",
     "1. Nhập Số lượng 5 ở dòng KKT-B",
     "Số lượng: 5",
     "- Ô tự về 2 (3 trừ 1)"),

    ("006", "Số lượng kho kế toán âm tự về 0", "P2",
     "Đang ở dòng kho kế toán của H2",
     "1. Nhập -2",
     "Số lượng: -2",
     "- Ô tự về 0"),

    ("007", "Chọn trùng kho kế toán trong một dòng", "P0",
     "H1 đã có dòng KKT-A, vừa bấm Thêm kho",
     "1. Chọn KKT-A ở dòng mới",
     "—",
     "- Báo \"Kho kế toán đã được chọn!\", ô chọn về trống"),

    ("008", "Xóa dòng kho kế toán thêm", "P1",
     "H1 có KKT-A 1, KKT-B 2",
     "1. Bấm dấu x ở dòng KKT-B",
     "—",
     "- Còn dòng KKT-A 1\n"
     "- Dòng kho kế toán đầu tiên không có dấu x"),

    ("009", "Tổng kho kế toán nhỏ hơn SL xuất thì không lưu được", "P0",
     "H1 SL xuất 3, chỉ có KKT-A Số lượng 2",
     "1. Bấm \"Lưu và duyệt\"",
     "—",
     "- Báo \"<mã H1>. Số lượng xuất kho kế toán không khớp!\", không tạo phiếu"),

    ("010", "Xuất vượt SL được xuất thì không lưu được", "P0",
     PKK + "; " + KKT,
     "1. " + TAO + "\n"
     "2. Chọn KKT-A cho H1; H2 chọn KKT-B Số lượng 1 (KKT-B không có H2)\n"
     "3. Bấm \"Lưu và duyệt\"",
     "—",
     "- Báo \"Kho KKT-B: Số lượng xuất không được vượt quá số lượng được xuất!\"\n"
     "- Không tạo phiếu, tồn kế toán không đổi"),

    ("011", "Không chọn kho kế toán thì không lưu được", "P0",
     "Dòng H2 để \"Chọn kho kế toán\"",
     "1. Bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", lỗi hiện dưới ô kho kế toán của H2; không tạo phiếu"),
]


SEC_VI = [
    ("001", "Lưu tạo phiếu Đang tạo", "P0",
     PKK + "; " + KKT + "; " + KT1,
     "1. " + TAO + "\n"
     "2. Chọn Nhân viên NV-K, KKT-A cho cả 2 dòng, bấm Lưu",
     "—",
     "- Báo \"Thao tác thành công!\", về danh sách\n"
     "- Phiếu mới PXHĐCKK-xxxxx Đang tạo, Người lập KT-1\n"
     "- PXK-1 chuyển Đang hạch toán\n"
     "- Tồn kế toán KKT-A chưa đổi: H1 10, H2 5"),

    ("002", "Lưu và duyệt tạo phiếu Đã hạch toán", "P0",
     PKK + "; " + KKT + "; " + KT1,
     "1. " + TAO + "\n"
     "2. Chọn Nhân viên NV-K\n"
     "3. " + LUU_DUYET,
     "—",
     "- Báo \"Thao tác thành công!\"\n"
     "- Phiếu Đã hạch toán\n"
     "- PXK-1 chuyển Đã hạch toán\n"
     "- Tồn kế toán KKT-A: H1 7, H2 4"),

    ("003", "Số phiếu tăng dần", "P1",
     "Phiếu gần nhất là PXHĐCKK-00012",
     "1. Lập và Lưu một phiếu mới",
     "—",
     "- Số phiếu mới PXHĐCKK-00013"),

    ("004", "Sau khi lập, phiếu xuất kho không còn nút Tạo phiếu xuất hàng", "P0",
     "KT-1 vừa Lưu phiếu từ PXK-1",
     "1. " + MENU_PXK + ", mở Hành động của PXK-1",
     "—",
     "- Không còn \"Tạo phiếu xuất hàng\""),

    ("005", "Sửa phiếu Đang tạo rồi Lưu", "P0",
     "PXH-3 Đang tạo do KT-1 lập từ PXK-1, H1 KKT-A 3",
     "1. Mở Sửa PXH-3\n"
     "2. Đổi H1 thành KKT-A 1, KKT-B 2, sửa Ghi chú \"Đã đối chiếu\", bấm Lưu",
     "—",
     "- Báo \"Thao tác thành công!\"\n"
     "- PXH-3 vẫn Đang tạo, chi tiết H1 KKT-A 1, KKT-B 2, Ghi chú mới\n"
     "- Tồn kế toán chưa đổi"),

    ("006", "Sửa phiếu Đang tạo rồi Lưu và duyệt", "P0",
     "PXH-3 Đang tạo do KT-1 lập từ PXK-1, H1, H2 đều KKT-A; " + KKT,
     "1. Mở Sửa PXH-3, bấm \"Lưu và duyệt\"",
     "—",
     "- PXH-3 Đã hạch toán, PXK-1 Đã hạch toán\n"
     "- Tồn kế toán KKT-A: H1 7, H2 4\n"
     "- Không còn nút Sửa"),

    ("007", "Sửa: SL được xuất hiện khi mở màn", "P2",
     "PXH-3 Đang tạo, H1 chọn KKT-A",
     "1. Mở Sửa PXH-3, quan sát cột SL được xuất",
     "—",
     "- Mong đợi: hiện ngay SL được xuất của KKT-A\n"
     "- Lưu ý: theo code hiện tại cột trống cho tới khi chọn lại kho kế toán - ghi Failed"),

    ("008", "Hủy ở màn Sửa", "P2",
     "Đang ở Sửa PXH-3",
     "1. Bấm Hủy",
     "—",
     "- Mong đợi: về danh sách Phiếu xuất hàng điều chỉnh kiểm kê\n"
     "- Lưu ý: theo code hiện tại chuyển sang danh sách kiểm kê cũ - ghi Failed"),

    ("009", "Sửa thêm file đính kèm", "P1",
     "PXH-3 Đang tạo có file bb-thieu.pdf",
     "1. Mở Sửa PXH-3, thêm file bo-sung.pdf, bấm Lưu\n"
     "2. Mở Chi tiết PXH-3",
     "File: bo-sung.pdf",
     "- Có cả bb-thieu.pdf và bo-sung.pdf"),

    ("010", "Phiếu Đã hạch toán không sửa được qua đường dẫn", "P0",
     "PXH-2 Đã hạch toán do KT-1 lập",
     "1. KT-1 dán đường dẫn Sửa của PXH-2",
     "—",
     "- Ra trang không tìm thấy"),

    ("011", "Lưu và duyệt khi tồn kế toán đã bị dùng sau lúc Lưu", "P0",
     "PXH-3 Đang tạo, H2 KKT-A 1; sau khi Lưu, phiếu xuất hàng khác đã xuất hết 5 H2 ở KKT-A",
     "1. Mở Sửa PXH-3, bấm \"Lưu và duyệt\"",
     "—",
     "- Báo \"Kho KKT-A: Số lượng xuất không được vượt quá số lượng được xuất!\"\n"
     "- PXH-3 vẫn Đang tạo"),
]


SEC_VII = [
    ("001", "Tồn kho vật lý không đổi khi Lưu và duyệt", "P0",
     PKK + "; " + KKT + "; tồn vật lý K1 sau PXK-1: H1 = 9, H2 = 4",
     "1. " + TAO + ", " + LUU_DUYET + "\n"
     "2. Xem tồn kho vật lý H1, H2 tại K1",
     "—",
     "- H1 = 9, H2 = 4 (không bị trừ thêm)"),

    ("002", "Tồn kế toán trừ đúng theo từng kho kế toán", "P0",
     PKK + "; " + KKT,
     "1. " + TAO + "\n"
     "2. H1: KKT-A 1, KKT-B 2; H2: KKT-A 1; bấm \"Lưu và duyệt\"\n"
     "3. Xem tồn kế toán",
     "—",
     "- H1: KKT-A 9, KKT-B 0\n"
     "- H2: KKT-A 4"),

    ("003", "Đơn giá vốn, Thành tiền vốn sau hạch toán", "P0",
     PKK + "; " + KKT,
     "1. " + TAO + ", " + LUU_DUYET + "\n"
     "2. Mở Chi tiết phiếu",
     "—",
     "- H1: Đơn giá vốn 100,000, Thành tiền vốn 300,000\n"
     "- H2: Đơn giá vốn 300,000, Thành tiền vốn 300,000"),

    ("004", "Đơn giá xuất không ảnh hưởng giá vốn", "P1",
     PKK + "; " + KKT,
     "1. " + TAO + ", sửa Đơn giá xuất H1 thành 999000\n"
     "2. " + LUU_DUYET + ", mở Chi tiết",
     "—",
     "- Đơn giá vốn H1 vẫn 100,000"),

    ("005", "Lưu và duyệt ghi nhận bút toán giảm hàng tồn kho", "P0",
     PKK + "; " + KKT,
     "1. " + TAO + ", chọn Nhân viên NV-K, " + LUU_DUYET + "\n"
     "2. Xem sổ chi tiết tài khoản của phiếu",
     "—",
     "- Mong đợi: có bút toán ghi giảm 1561 theo giá vốn (H1 300.000, H2 300.000, tổng 600.000), đối tượng "
     "là NV-K\n"
     "- Lưu ý: theo code hiện tại không có bút toán nào (số tiền luôn bằng 0); nếu có thì chiều ghi Nợ 1561 / "
     "Có 3381 giống phiếu nhập - ghi Failed"),

    ("006", "Lưu không ghi bút toán", "P0",
     PKK + "; " + KKT,
     "1. " + TAO + ", bấm Lưu\n"
     "2. Xem sổ chi tiết tài khoản của phiếu",
     "—",
     "- Không có bút toán"),

    ("007", "ĐVT khác ĐVT nhỏ nhất: Thành tiền vốn", "P1",
     "Phiếu kiểm kê thiếu H3 1 Thùng (hệ số 12 Cái); tồn kế toán H3 ở KKT-A 24 Cái, bình quân 10.000 / Cái",
     "1. Lập phiếu xuất hàng từ phiếu xuất kho của H3, KKT-A, Lưu và duyệt\n"
     "2. Mở Chi tiết và In",
     "—",
     "- Tồn kế toán KKT-A còn 12 Cái\n"
     "- Mong đợi: Thành tiền vốn = 120,000\n"
     "- Lưu ý: theo code hiện tại Đơn giá vốn hiện 10,000 (theo Cái) và Thành tiền vốn = 10,000 - ghi Failed"),

    ("008", "Phiếu kiểm kê chuyển Hoàn thành khi xử lý hết", "P0",
     "PKK-1 chỉ có hàng thiếu H1, H2 (đã có PXK-1)",
     "1. Lập phiếu từ PXK-1, Lưu và duyệt\n"
     "2. Xem trạng thái PKK-1",
     "—",
     "- PKK-1 Hoàn thành"),

    ("009", "Phiếu kiểm kê Đang xử lý khi còn hàng thừa chưa nhập", "P1",
     "PKK-2 có H1 thiếu 3 (có PXK-4) và H4 thừa 4 chưa nhập hàng",
     "1. Lập phiếu từ PXK-4, Lưu và duyệt\n"
     "2. Xem PKK-2",
     "—",
     "- PKK-2 Đang xử lý"),

    ("010", "Chỉ Lưu nháp mà phiếu kiểm kê đã Hoàn thành", "P1",
     "PKK-1 chỉ có hàng thiếu H1, H2 (đã có PXK-1)",
     "1. Lập phiếu từ PXK-1, chỉ bấm Lưu\n"
     "2. Xem PKK-1",
     "—",
     "- Mong đợi: PKK-1 Đang xử lý cho tới khi Lưu và duyệt\n"
     "- Lưu ý: theo code hiện tại PKK-1 đã Hoàn thành - ghi Failed nếu nghiệp vụ yêu cầu chờ hạch toán"),

    ("011", "Lưu nhiều lần ở màn Sửa làm lệch số đã xử lý", "P1",
     "PXH-3 Đang tạo từ PXK-1, H1 SL 3",
     "1. Mở Sửa PXH-3, bấm Lưu; lặp lại 2 lần\n"
     "2. Xem kết quả kiểm kê H1 ở PKK-1",
     "—",
     "- Mong đợi: số đã xử lý H1 = 3\n"
     "- Lưu ý: theo code hiện tại số đã xử lý tăng 3 mỗi lần Lưu (thành 9) - ghi Failed"),

    ("012", "Giá vốn được Biên bản xử lý hàng thừa, thiếu lấy", "P1",
     "KT-1 đã Lưu và duyệt phiếu từ PXK-1 (giá vốn H1 100.000)",
     "1. Mở Biên bản xử lý hàng thừa, thiếu sau kiểm kê, chọn kho K1\n"
     "2. Quan sát dòng H1 của PKK-1",
     "—",
     "- Dòng H1 có chứng từ xử lý là phiếu xuất hàng vừa lập, giá vốn 100.000"),
]
