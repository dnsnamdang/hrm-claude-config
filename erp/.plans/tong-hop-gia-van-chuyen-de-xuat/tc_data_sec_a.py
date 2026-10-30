# -*- coding: utf-8 -*-
"""Section I-IV: hien thi, bo loc, danh sach & hanh dong, tao moi tu mau bao gia."""
from tc_data_role import MENU, MENU_MAU, MAU

SEC_I = [
    ("001", "Vào màn từ menu", "P0",
     "NV-VC1 có quyền Quản lý chi phí vận chuyển, đã lập 3 phiếu",
     "1. " + MENU,
     "—",
     "- Tiêu đề trang \"Quản lý tổng hợp giá vận chuyển đề xuất\"\n"
     "- Bảng tải dữ liệu, không báo lỗi"),

    ("002", "Cột của bảng danh sách", "P0",
     "NV-VC1 có phiếu THGVC-1 lập từ mẫu MB-1",
     "1. Mở màn, quan sát tiêu đề cột",
     "—",
     "- Cột: STT, Mã, Ghi chú, Người duyệt, Ngày duyệt, Người tạo, Ngày tạo, Ngày gửi, Trạng thái, Mẫu báo "
     "giá, Hành động\n"
     "- Ngày hiển thị dạng ngày/tháng/năm"),

    ("003", "Không có nút Tạo mới trên danh sách", "P1",
     "—",
     "1. Mở màn, tìm nút Tạo mới",
     "—",
     "- Không có nút Tạo mới; phiếu chỉ tạo từ Danh mục mẫu báo giá vận chuyển"),

    ("004", "Nhãn trạng thái", "P1",
     "Có phiếu ở trạng thái Đang tạo, Chờ duyệt, Đã duyệt",
     "1. Quan sát cột Trạng thái",
     "—",
     "- Đang tạo: nhãn xanh dương\n"
     "- Chờ duyệt: nhãn vàng\n"
     "- Đã duyệt: nhãn xanh lá"),

    ("005", "Bấm Mã mở màn Chi tiết", "P0",
     "THGVC-1 Đang tạo của NV-VC1, đã nhập báo giá NCC A, NCC B",
     "1. Bấm mã THGVC-1",
     "—",
     "- Tiêu đề \"Tổng hợp giá vận chuyển đề xuất THGVC-...\"\n"
     "- Khối Thông tin chung: Ghi chú (khóa), file đính kèm nếu có; góc phải tên người lập - ngày lập\n"
     "- Khối Chi tiết: tab Tổng hợp, tab NCC A, tab NCC B\n"
     "- Cuối trang: nút Sửa, Quay lại"),

    ("006", "Bấm cột Mẫu báo giá mở mẫu ở tab mới", "P1",
     "THGVC-1 lập từ MB-1",
     "1. Bấm mã mẫu báo giá ở cột Mẫu báo giá",
     "—",
     "- Mở tab mới, màn Chi tiết mẫu báo giá MB-1"),

    ("007", "Tên tuyến ở tab Tổng hợp", "P2",
     "THGVC-1 có 2 tuyến K1 đi Hải Phòng, K1 đi Bắc Ninh",
     "1. Mở Chi tiết THGVC-1, xem cột Tuyến đường ở tab Tổng hợp",
     "—",
     "- Mong đợi: tên tuyến \"K1 đi Hải Phòng\", \"K1 đi Bắc Ninh\"\n"
     "- Lưu ý: theo code hiện tại tên tuyến có số thứ tự bắt đầu từ 0 phía trước (\"0 - K1 đi Hải Phòng\") - "
     "ghi Failed"),

    ("008", "Quay lại từ màn Chi tiết", "P2",
     "NV-VC1 đang ở Chi tiết THGVC-1",
     "1. Bấm Quay lại",
     "—",
     "- Về danh sách Tổng hợp giá vận chuyển đề xuất"),
]

SEC_II = [
    ("001", "Khối tìm kiếm có đủ ô lọc", "P0",
     "GD-1 có quyền xem theo công ty",
     "1. Mở màn, mở khối tìm kiếm",
     "—",
     "- Ô Mã, Ghi chú, Người tạo, Người duyệt, Trạng thái, Nhà cung cấp\n"
     "- Có thêm ô Phòng ban"),

    ("002", "Lọc theo Mã tìm gần đúng", "P0",
     "Có THGVC-00012 và THGVC-00013",
     "1. Gõ \"00012\" vào ô Mã",
     "Mã: 00012",
     "- Chỉ còn THGVC-00012"),

    ("003", "Lọc theo Trạng thái", "P0",
     "Có 2 phiếu Chờ duyệt, 1 phiếu Đã duyệt",
     "1. Chọn Trạng thái = Chờ duyệt",
     "—",
     "- Còn đúng 2 phiếu Chờ duyệt"),

    ("004", "Ô Trạng thái có cả trạng thái không dùng", "P2",
     "—",
     "1. Mở ô Trạng thái",
     "—",
     "- Có 5 lựa chọn: Đã duyệt, Chờ duyệt, Đang tạo, Đã lập hợp đồng, Đang lập hợp đồng\n"
     "- Chọn Đã lập hợp đồng hoặc Đang lập hợp đồng: không có phiếu nào (xem TC Lập hợp đồng ở mục VIII)"),

    ("005", "Lọc theo Nhà cung cấp", "P0",
     "THGVC-1 đã nhập báo giá NCC A, NCC B; THGVC-2 chỉ có NCC B",
     "1. Chọn Nhà cung cấp = NCC A",
     "—",
     "- Chỉ còn THGVC-1"),

    ("006", "Lọc theo Người tạo", "P1",
     "TP-VC thấy phiếu của NV-VC1 và NV-VC2",
     "1. Chọn Người tạo = NV-VC2",
     "—",
     "- Chỉ còn phiếu do NV-VC2 lập"),

    ("007", "Lọc theo Người duyệt", "P1",
     "THGVC-4 do DGV-1 duyệt",
     "1. Chọn Người duyệt = DGV-1",
     "—",
     "- Chỉ còn các phiếu DGV-1 đã duyệt hoặc không duyệt"),

    ("008", "Lọc theo Ghi chú", "P1",
     "THGVC-1 ghi chú \"Tuyến miền Bắc quý 4\"; THGVC-2 ghi chú \"Tuyến miền Nam\"",
     "1. Gõ \"miền Bắc\" vào ô Ghi chú",
     "Ghi chú: miền Bắc",
     "- Mong đợi: chỉ còn THGVC-1\n"
     "- Lưu ý: theo code hiện tại ô Ghi chú không được áp dụng, vẫn ra cả 2 phiếu - ghi Failed"),

    ("009", "Lọc theo Công ty", "P1",
     "TGD có quyền xem theo tổng công ty; có phiếu TPE và TPC",
     "1. Chọn Công ty = TPC",
     "—",
     "- Chỉ còn phiếu do người thuộc TPC lập"),

    ("010", "Lọc theo Phòng ban", "P1",
     "GD-1 xem theo công ty; phòng Vận tải có THGVC-2, phòng Kho có THGVC-7",
     "1. Chọn Phòng ban = Vận tải",
     "—",
     "- Mong đợi: chỉ còn THGVC-2\n"
     "- Lưu ý: theo code hiện tại ô Phòng ban không được áp dụng, vẫn ra cả THGVC-7 - ghi Failed"),

    ("011", "Kết hợp nhiều ô lọc và không có kết quả", "P2",
     "—",
     "1. Chọn Trạng thái = Đã duyệt, Nhà cung cấp = NCC chưa từng báo giá",
     "—",
     "- Bảng báo không có dữ liệu, không lỗi"),
]

SEC_III = [
    ("001", "Phiếu mới tạo lên đầu", "P1",
     "NV-VC1 vừa tạo THGVC-8",
     "1. Mở danh sách",
     "—",
     "- THGVC-8 ở dòng đầu"),

    ("002", "Phiếu Đang tạo chỉ người lập thấy", "P0",
     "NV-VC2 có THGVC-3 Đang tạo; GD-1 xem theo công ty",
     "1. GD-1 mở danh sách",
     "—",
     "- Không có THGVC-3"),

    ("003", "Hành động của người lập khi phiếu Đang tạo", "P0",
     "THGVC-1 Đang tạo của NV-VC1",
     "1. NV-VC1 mở menu Hành động của THGVC-1",
     "—",
     "- Có: Sửa, Xóa, Nhập báo giá của NCC, Xuất excel"),

    ("004", "Hành động khi phiếu Chờ duyệt hoặc Đã duyệt", "P0",
     "THGVC-2 Chờ duyệt, THGVC-4 Đã duyệt, đều của NV-VC1",
     "1. NV-VC1 mở menu Hành động 2 phiếu",
     "—",
     "- Chỉ còn Xuất excel; không Sửa, Xóa, Nhập báo giá của NCC"),

    ("005", "Màn cần duyệt chỉ có phiếu Chờ duyệt cùng công ty", "P0",
     "DGV-1 (TPE); TPE có THGVC-2 Chờ duyệt, THGVC-4 Đã duyệt; TPC có THGVC-9 Chờ duyệt",
     "1. DGV-1 mở màn \"Tổng hợp giá đề xuất cần duyệt\" từ thẻ trang chủ",
     "—",
     "- Chỉ có THGVC-2"),

    ("006", "Phiếu bị Không duyệt vẫn hiện Người duyệt", "P2",
     "THGVC-5 bị DGV-1 Không duyệt, quay về Đang tạo",
     "1. NV-VC1 xem dòng THGVC-5",
     "—",
     "- Trạng thái Đang tạo, cột Người duyệt = DGV-1, Ngày duyệt = ngày không duyệt\n"
     "- Lưu ý: nếu nghiệp vụ muốn phiếu Đang tạo để trống Người duyệt thì ghi Failed"),

    ("007", "Thẻ đếm ở trang chủ", "P1",
     "DGV-1 có quyền duyệt; TPE có 2 phiếu Chờ duyệt",
     "1. DGV-1 xem nhóm thẻ Vận chuyển ở trang chủ",
     "—",
     "- Thẻ \"Tổng hợp giá vận chuyển đề xuất\" hiện 2"),
]

SEC_IV = [
    ("001", "Nút Tổng hợp giá đề xuất ở danh mục mẫu báo giá", "P0",
     MAU,
     "1. Đăng nhập NV-VC1, " + MENU_MAU + "\n"
     "2. Mở menu Hành động của MB-1",
     "—",
     "- Có mục \"Tổng hợp giá đề xuất\""),

    ("002", "Mở form tạo từ mẫu báo giá", "P0",
     MAU + "\nMB-1 có ghi chú \"Tuyến miền Bắc quý 4\"",
     "1. Bấm \"Tổng hợp giá đề xuất\" ở MB-1",
     "—",
     "- Tiêu đề \"Tạo tổng hợp giá vận chuyển đề xuất\"\n"
     "- Ghi chú điền sẵn \"Tuyến miền Bắc quý 4\", sửa được\n"
     "- Khối File đính kèm (PDF) có nút thêm file\n"
     "- Không có khối Chi tiết; chỉ có nút Lưu và Hủy, không có nút Gửi"),

    ("003", "Lưu phiếu mới", "P0",
     MAU,
     "1. Mở form tạo từ MB-1\n"
     "2. Bấm Lưu",
     "—",
     "- Báo \"Lưu thành công. Bạn cần gửi để đề xuất được duyệt!\"\n"
     "- Về danh sách, dòng đầu là phiếu mới mã THGVC-..., Đang tạo, Mẫu báo giá = MB-1, Ngày gửi trống"),

    ("004", "Lưu kèm file đính kèm PDF", "P1",
     MAU,
     "1. Ở form tạo bấm dấu cộng, chọn file bao-gia-tong.pdf\n"
     "2. Bấm Lưu, mở Chi tiết phiếu",
     "File: bao-gia-tong.pdf",
     "- Chi tiết hiện file bao-gia-tong.pdf, bấm mở được"),

    ("005", "Tạo phiếu khóa mẫu báo giá", "P1",
     "MB-1 Đang tạo, NV-VC1 thấy nút Sửa, Xóa ở MB-1",
     "1. Tạo và Lưu phiếu tổng hợp từ MB-1\n"
     "2. Quay lại Danh mục mẫu báo giá, mở Hành động MB-1",
     "—",
     "- Không còn Sửa, Xóa ở MB-1"),

    ("006", "Người khác không tổng hợp được từ mẫu chưa dùng", "P0",
     "MB-2 do NV-VC2 lập, chưa có phiếu tổng hợp nào",
     "1. NV-VC1 mở Hành động của MB-2",
     "—",
     "- Không có mục \"Tổng hợp giá đề xuất\""),

    ("007", "Người khác tổng hợp được từ mẫu đã dùng", "P2",
     "MB-1 đã có phiếu THGVC-1 của NV-VC1",
     "1. NV-VC2 mở Hành động của MB-1, bấm \"Tổng hợp giá đề xuất\", Lưu",
     "—",
     "- Tạo được phiếu thứ 2 từ MB-1\n"
     "- Lưu ý: nếu nghiệp vụ chỉ cho 1 phiếu tổng hợp mỗi mẫu thì ghi Failed"),

    ("008", "Mở form tạo không kèm mẫu báo giá", "P2",
     "—",
     "1. Dán đường dẫn tạo phiếu tổng hợp nhưng bỏ phần mẫu báo giá",
     "—",
     "- Ra trang không tìm thấy"),

    ("009", "Hủy ở form tạo", "P2",
     "Đang ở form tạo từ MB-1",
     "1. Bấm Hủy",
     "—",
     "- Về danh sách Tổng hợp giá vận chuyển đề xuất, không tạo phiếu"),

    ("010", "Bấm Lưu 2 lần liên tiếp", "P1",
     "Đang ở form tạo từ MB-1",
     "1. Bấm Lưu 2 lần thật nhanh",
     "—",
     "- Nút Lưu mờ ngay sau lần bấm đầu\n"
     "- Chỉ tạo 1 phiếu"),
]
