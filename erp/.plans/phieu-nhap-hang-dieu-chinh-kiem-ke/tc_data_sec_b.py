# -*- coding: utf-8 -*-
"""Section V, VI, VII - phan bo kho ke toan, luu / luu va duyet / sua, ton ke toan & but toan."""
from tc_data_role import MENU, MENU_PNK, PKK, GIA, KKT, KT1, TAO, LUU_DUYET

SEC_V = [
    ("001", "Chọn kho kế toán dòng đầu tự điền cho các dòng khác", "P0",
     PKK + "; " + KKT,
     "1. " + TAO + "\n"
     "2. Chọn KKT-A ở dòng kho kế toán đầu tiên của H4",
     "—",
     "- Dòng kho kế toán đầu tiên của H5 cũng tự chọn KKT-A"),

    ("002", "Thêm kho để chia SL của một dòng", "P0",
     "Đang ở form lập từ PNK-1, H4 SL nhập 4",
     "1. Bấm \"Thêm kho\" ở dòng H4\n"
     "2. Dòng 1 chọn KKT-A Số lượng 3; dòng 2 chọn KKT-B Số lượng 1",
     "—",
     "- H4 có 2 dòng kho kế toán: KKT-A 3, KKT-B 1"),

    ("003", "Số lượng kho kế toán không vượt phần còn lại", "P0",
     "H4 SL nhập 4, đã có KKT-A 3 và dòng thứ 2 chọn KKT-B",
     "1. Nhập Số lượng 5 ở dòng KKT-B",
     "Số lượng: 5",
     "- Ô tự về 1 (4 trừ 3)"),

    ("004", "Số lượng kho kế toán âm tự về 0", "P2",
     "Đang ở dòng kho kế toán của H5",
     "1. Nhập -2",
     "Số lượng: -2",
     "- Ô tự về 0"),

    ("005", "Chọn trùng kho kế toán trong một dòng", "P0",
     "H4 đã có dòng KKT-A, vừa bấm Thêm kho",
     "1. Chọn KKT-A ở dòng mới",
     "—",
     "- Báo \"Kho kế toán đã được chọn!\", ô chọn về trống"),

    ("006", "Xóa dòng kho kế toán thêm", "P1",
     "H4 có KKT-A 3, KKT-B 1",
     "1. Bấm dấu x ở dòng KKT-B",
     "—",
     "- Còn dòng KKT-A 3\n"
     "- Dòng kho kế toán đầu tiên không có dấu x"),

    ("007", "Tổng kho kế toán nhỏ hơn SL nhập thì không lưu được", "P0",
     "H4 SL nhập 4, chỉ có KKT-A Số lượng 3",
     "1. Bấm \"Lưu và duyệt\"",
     "—",
     "- Mong đợi: báo số lượng nhập kho kế toán không khớp, không tạo phiếu\n"
     "- Lưu ý: theo code hiện tại câu báo ghi \"Số lượng xuất kho kế toán không khớp!\" (chữ \"xuất\") - "
     "ghi Failed nếu nghiệp vụ yêu cầu đúng chữ"),

    ("008", "Không chọn kho kế toán thì không lưu được", "P0",
     "Dòng H5 để \"Chọn kho kế toán\"",
     "1. Bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", lỗi hiện dưới ô kho kế toán của H5; không tạo phiếu"),
]


SEC_VI = [
    ("001", "Lưu tạo phiếu Đang tạo", "P0",
     PKK + "; " + GIA + "; " + KKT,
     "1. " + TAO + "\n"
     "2. Chọn Nhân viên NV-K, kho kế toán KKT-A cho H4 và H5\n"
     "3. Bấm Lưu",
     "—",
     "- Báo \"Thao tác thành công!\", về danh sách\n"
     "- Có phiếu mới PNHĐCKK-xxxxx trạng thái Đang tạo\n"
     "- PNK-1 chuyển Đang hạch toán"),

    ("002", "Lưu và duyệt tạo phiếu Đã hạch toán", "P0",
     PKK + "; " + GIA + "; " + KKT,
     "1. " + TAO + "\n"
     "2. Chọn Nhân viên NV-K\n"
     "3. " + LUU_DUYET,
     "—",
     "- Báo \"Thao tác thành công!\"\n"
     "- Phiếu mới Đã hạch toán\n"
     "- PNK-1 chuyển Đã hạch toán"),

    ("003", "Số phiếu tăng dần", "P1",
     "Phiếu gần nhất là PNHĐCKK-00007",
     "1. Lập và Lưu 1 phiếu mới",
     "—",
     "- Phiếu mới có số PNHĐCKK-00008"),

    ("004", "Không chọn Nhân viên thì không lưu được", "P0",
     "Đang ở form lập từ PNK-1, ô Nhân viên trống",
     "1. Bấm Lưu",
     "—",
     "- Báo \"Tạo thất bại!\", lỗi dưới ô Nhân viên; không tạo phiếu, PNK-1 vẫn Chờ duyệt"),

    ("005", "Phiếu lưu giữ file của phiếu nhập kho và file thêm", "P1",
     "Đang ở form lập từ PNK-1 (có bb-thua.pdf)",
     "1. Thêm file kt-nhap.pdf, bấm Lưu\n"
     "2. Mở Chi tiết phiếu vừa lập",
     "File: kt-nhap.pdf",
     "- Có cả bb-thua.pdf và kt-nhap.pdf"),

    ("006", "Mở Sửa phiếu Đang tạo", "P0",
     "PNH-3 Đang tạo do KT-1 lập từ PNK-1: H4 KKT-A 4 giá 120.000, H5 KKT-A 2 giá 300.000",
     "1. KT-1 mở Hành động > Sửa của PNH-3",
     "—",
     "- Form hiện đúng Nhân viên, Ghi chú, đơn giá, kho kế toán, Số lượng đã lưu\n"
     "- Có nút Lưu, Lưu và duyệt, Hủy"),

    ("007", "Sửa đơn giá rồi Lưu", "P0",
     "Đang Sửa PNH-3",
     "1. Sửa Đơn giá H5 thành 320000\n"
     "2. Bấm Lưu\n"
     "3. Mở Chi tiết PNH-3",
     "Đơn giá H5: 320000",
     "- PNH-3 vẫn Đang tạo\n"
     "- H5 Đơn giá 320,000, Thành tiền 640,000"),

    ("008", "Sửa rồi Lưu và duyệt", "P0",
     "PNH-3 Đang tạo do KT-1 lập; " + KKT,
     "1. KT-1 Sửa PNH-3, đổi H4 thành KKT-A 3, KKT-B 1\n"
     "2. Bấm \"Lưu và duyệt\"",
     "—",
     "- PNH-3 Đã hạch toán, PNK-1 Đã hạch toán\n"
     "- Tồn kế toán H4: KKT-A tăng 3, KKT-B tăng 1; H5: KKT-A tăng 2"),

    ("009", "Phiếu Đã hạch toán không sửa được", "P0",
     "PNH-2 Đã hạch toán do KT-1 lập",
     "1. KT-1 dán đường dẫn Sửa của PNH-2",
     "—",
     "- Ra trang không tìm thấy"),

    ("010", "Hủy ở màn Sửa", "P2",
     "Đang Sửa PNH-3, đã đổi đơn giá H4",
     "1. Bấm Hủy\n"
     "2. Mở Chi tiết PNH-3",
     "—",
     "- Về danh sách; đơn giá H4 giữ như cũ"),

    ("011", "Sửa phiếu không có file nào thì phải thêm file", "P2",
     "PNH-8 Đang tạo, lập từ phiếu nhập kho không có file, khi lập không thêm file",
     "1. Sửa PNH-8, không thêm file, bấm Lưu",
     "—",
     "- Báo \"Sửa thất bại!\", lỗi dưới khu File đính kèm"),

    ("012", "Sửa thêm file", "P2",
     "Đang Sửa PNH-3 (có bb-thua.pdf)",
     "1. Thêm file bo-sung.pdf, bấm Lưu\n"
     "2. Mở Chi tiết PNH-3",
     "—",
     "- Có cả bb-thua.pdf và bo-sung.pdf"),
]


SEC_VII = [
    ("001", "Lưu và duyệt cộng tồn kế toán theo kho kế toán", "P0",
     PKK + "; " + GIA + "; " + KKT,
     "1. " + TAO + ", chọn Nhân viên NV-K\n"
     "2. H4 chia KKT-A 3, KKT-B 1; H5 chọn KKT-B 2\n"
     "3. Bấm \"Lưu và duyệt\"\n"
     "4. Xem tồn kế toán H4, H5",
     "—",
     "- H4: KKT-A = 3, KKT-B = 1\n"
     "- H5: KKT-A = 0, KKT-B = 2"),

    ("002", "Lưu (Đang tạo) không cộng tồn kế toán", "P0",
     PKK + "; " + KKT,
     "1. " + TAO + ", chọn Nhân viên, KKT-A cho cả 2 dòng, bấm Lưu\n"
     "2. Xem tồn kế toán H4, H5 tại KKT-A",
     "—",
     "- Tồn kế toán vẫn bằng 0\n"
     "- Chưa có bút toán của phiếu"),

    ("003", "Tồn kho vật lý không đổi khi hạch toán", "P0",
     PKK + "; tồn vật lý kho K1: H4 = 4, H5 = 2",
     "1. KT-1 lập phiếu từ PNK-1, " + LUU_DUYET + "\n"
     "2. Xem tồn kho K1 và tồn theo vị trí P2, P3",
     "—",
     "- H4 vẫn 4 (P2 = 4), H5 vẫn 2 (P3 = 2)"),

    ("004", "Bút toán khi Lưu và duyệt", "P0",
     PKK + "; " + GIA + "; " + KKT,
     "1. KT-1 lập phiếu từ PNK-1, Nhân viên NV-K, " + LUU_DUYET + "\n"
     "2. Xem bút toán của phiếu",
     "—",
     "- Nợ 1561 / Có 3381: H4 480.000\n"
     "- Nợ 1561 / Có 3381: H5 600.000\n"
     "- Có 3381 tổng 1.080.000, đối tượng NV-K"),

    ("005", "Bút toán theo đơn giá đã sửa", "P0",
     PKK + "; " + GIA,
     "1. KT-1 lập phiếu từ PNK-1, sửa Đơn giá H4 thành 150000\n"
     "2. " + LUU_DUYET + ", xem bút toán",
     "Đơn giá H4: 150000",
     "- Nợ 1561 H4 = 600.000; H5 = 600.000; Có 3381 tổng 1.200.000"),

    ("006", "Giá trị tồn kế toán tăng theo thành tiền nhập", "P1",
     PKK + "; " + GIA + "; tồn kế toán H4 tại KKT-A trước đó bằng 0",
     "1. KT-1 lập phiếu, H4 chọn KKT-A, Lưu và duyệt\n"
     "2. Xem Thẻ kho / sổ tồn kế toán H4 tại KKT-A",
     "—",
     "- Dòng nhập 4, giá trị sau nhập 480.000"),

    ("007", "ĐVT khác ĐVT nhỏ nhất: thành tiền và bút toán phải khớp", "P1",
     "PNK-3 Chờ duyệt có H6 SL 2 ĐVT Thùng (1 Thùng = 12 Cái), giá nhập gần nhất 50.000",
     "1. KT-1 lập phiếu từ PNK-3, quan sát Thành tiền H6\n"
     "2. Chọn kho kế toán, Lưu và duyệt, xem bút toán và tồn kế toán",
     "—",
     "- Tồn kế toán H6 tăng 24 Cái\n"
     "- Mong đợi: Thành tiền trên màn (100.000) bằng số tiền Nợ 1561\n"
     "- Lưu ý: theo code hiện tại Nợ 1561 = 1.200.000 (nhân thêm 12) - ghi Failed"),

    ("008", "Phiếu kiểm kê chuyển Hoàn thành khi xử lý xong", "P0",
     "PKK-1 chỉ còn việc nhập hàng thừa (đã xử lý xong hàng thiếu, điều chuyển)",
     "1. KT-1 lập phiếu từ PNK-1, Lưu và duyệt\n"
     "2. Mở Chi tiết PKK-1",
     "—",
     "- PKK-1 trạng thái Hoàn thành"),

    ("009", "Phiếu kiểm kê còn việc thì Đang xử lý", "P1",
     "PKK-1 còn hàng thiếu chưa có phiếu xuất",
     "1. KT-1 lập phiếu từ PNK-1, Lưu và duyệt\n"
     "2. Mở Chi tiết PKK-1",
     "—",
     "- PKK-1 trạng thái Đang xử lý"),

    ("010", "Chỉ Lưu (chưa hạch toán) mà phiếu kiểm kê đã Hoàn thành", "P1",
     "PKK-1 chỉ còn việc nhập hàng thừa",
     "1. KT-1 lập phiếu từ PNK-1, bấm Lưu (Đang tạo)\n"
     "2. Mở Chi tiết PKK-1",
     "—",
     "- Mong đợi: PKK-1 chưa Hoàn thành khi tồn kế toán chưa được nhập\n"
     "- Lưu ý: theo code hiện tại PKK-1 đã Hoàn thành - ghi Failed nếu nghiệp vụ yêu cầu chờ hạch toán"),

    ("011", "Lưu nhiều lần ở màn Sửa làm lệch số đã xử lý của kết quả kiểm kê", "P1",
     "PNH-3 Đang tạo từ PNK-1 (H4 thừa 4)",
     "1. KT-1 Sửa PNH-3, bấm Lưu\n"
     "2. Sửa lần nữa, bấm Lưu\n"
     "3. Nhờ tester kỹ thuật xem số đã xử lý của kết quả kiểm kê H4 ở PKK-1",
     "—",
     "- Mong đợi: số đã xử lý H4 = 4\n"
     "- Lưu ý: theo code hiện tại mỗi lần Lưu cộng thêm 4 (thành 12) - ghi Failed"),
]
