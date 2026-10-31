# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu yêu cầu điều chỉnh công nợ" — skill testcase-documenter (tc_engine), 30/10/2026.

Chạy: python gen_testcase.py -> testcase.xlsx
Nguồn: cùng nguồn code với gen_srs.py (nhánh develop 30/10/2026).
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '.claude', 'skills', 'testcase-documenter', 'assets'))
from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, 'testcase.xlsx')
MENU = ('Vào phân hệ Tài chính > menu "Khởi tạo" > nhóm "Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi" > bấm '
        '"Phiếu yêu cầu điều chỉnh công nợ".')
MENU_SALE = 'Vào phân hệ Bán hàng > menu "Yêu cầu" > nhóm "Công nợ - Thu - Chi" > bấm "YC điều chỉnh công nợ".'
MENU_CD = ('Vào phân hệ Tài chính > menu "Chờ duyệt" > nhóm "Phê duyệt - Công nợ - Thu - Chi" > bấm '
           '"Phiếu yêu cầu điều chỉnh công nợ chờ duyệt".')
TAO = '1. ' + MENU + '\n2. Bấm "Tạo mới".'
DONG = ('3. Nhập Diễn giải.\n4. Bấm Thêm dòng.\n'
        '5. Bên "Điều chỉnh từ": chọn khách hàng KH-A, hợp đồng HĐ-A1, Số tiền 10,000,000.\n'
        '6. Bên "Điều chỉnh đến": chọn khách hàng KH-B, hợp đồng HĐ-B1, Số tiền 10,000,000.')

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn Phiếu yêu cầu điều chỉnh công nợ dùng để đề nghị chuyển công nợ từ khách hàng / nhà cung cấp, hợp đồng này sang '
     'khách hàng / nhà cung cấp, hợp đồng khác.\n'
     'Phiếu lưu nháp được (Đang tạo), gửi duyệt sang Chờ tạo phiếu kế toán; Kế toán thanh toán Từ chối (kèm lý do) hoặc '
     'Tạo phiếu kế toán để ghi sổ.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Hai loại phiếu: Điều chỉnh công nợ khách hàng, Điều chỉnh công nợ nhà cung cấp.\n'
     '- Trạng thái: Đang tạo, Chờ tạo phiếu kế toán, Đã tạo phiếu kế toán, Đã duyệt phiếu kế toán, Hủy (dữ liệu cũ), Từ chối.\n'
     '- Danh sách chung: phiếu theo quyền xem theo cấp; không có quyền thì phiếu mình lập.\n'
     '- Danh sách chờ duyệt: phiếu Chờ tạo phiếu kế toán của người lập cùng công ty, chỉ Kế toán thanh toán thấy.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác: luôn ẩn.\n'
     '- Ở màn chờ duyệt: người không có quyền Kế toán thanh toán thấy danh sách rỗng.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày lập phiếu, lấy trọn hai đầu mút.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Phiếu > nhiều nhóm "Điều chỉnh từ" (khách hàng / NCC, hợp đồng, số tiền) > mỗi nhóm có một hoặc nhiều dòng '
     '"Điều chỉnh đến".'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Tổng "Điều chỉnh đến" của mỗi nhóm phải bằng số tiền "Điều chỉnh từ" khi gửi duyệt.\n'
     '- Bên "đến" không được trùng khách hàng / hợp đồng với bên "từ".'),
    ('7. Phân quyền cấp',
     '- Xem tất cả phiếu yêu cầu điều chỉnh của tổng công ty.\n'
     '- Xem tất cả phiếu yêu cầu điều chỉnh của công ty.\n'
     '- Xem tất cả phiếu yêu cầu điều chỉnh của phòng ban.\n'
     '- Xem tất cả phiếu yêu cầu điều chỉnh của bộ phận.\n'
     '- Kế toán thanh toán: màn chờ duyệt, Từ chối, Tạo phiếu kế toán (cùng công ty người lập).'),
    ('8. Cách tính các ô thống kê',
     '- Dòng "Số tiền còn lại" của nhóm = Số tiền "từ" trừ tổng Số tiền "đến".\n'
     '- Dòng Tổng cộng = tổng tiền bên "từ" và bên "đến".\n'
     '- Ô "Hiển thị a–b / N": N là tổng phiếu khớp bộ lọc trong phạm vi quyền.'),
    ('9. Ghi chú đọc bảng',
     '- Số tiền hiển thị dạng 1,234,567.\n'
     '- Lưu ý: hợp đồng bên "đến" chỉ bắt buộc khi Gửi duyệt; Lưu nháp vẫn để trống được.\n'
     '- Lưu ý: bấm Gửi duyệt khi thiếu nhiều ô, mọi ô lỗi phải đỏ CÙNG MỘT LƯỢT, không báo từng ô một.\n'
     '- Lưu ý: màn chưa có cửa sổ chọn trường xuất Excel; Xuất Excel tải file ngay.'),
]

ROLE_TCS = [
    ('00', 'Không có quyền nào chỉ thấy phiếu mình lập', 'P0', 'Tài khoản A không có quyền xem, không là kế toán; A lập 3 phiếu.',
     '1. Đăng nhập bằng A.\n2. ' + MENU, '—', '- Tổng số = 3.\n- Chỉ phiếu A lập.'),
    ('01', 'Quyền xem của tổng công ty', 'P1', 'Tài khoản C có quyền tổng công ty.', '1. Đăng nhập bằng C.\n2. ' + MENU, '—',
     '- Thấy phiếu mọi công ty (trừ nháp của người khác).\n- Khối lọc có Công ty, Phòng ban, Bộ phận.'),
    ('02', 'Quyền xem của công ty', 'P1', 'Tài khoản D công ty 1.', '1. Đăng nhập bằng D.\n2. ' + MENU, '—', '- Chỉ phiếu công ty 1.'),
    ('03', 'Quyền xem của phòng ban', 'P1', 'Tài khoản E quản lý phòng Kinh doanh, tự lập 2 phiếu ở phòng khác.',
     '1. Đăng nhập bằng E.\n2. ' + MENU, '—', '- Phiếu phòng Kinh doanh + 2 phiếu E lập.'),
    ('04', 'Quyền xem của bộ phận', 'P1', 'Tài khoản F quản lý bộ phận Bán lẻ.', '1. Đăng nhập bằng F.\n2. ' + MENU, '—',
     '- Phiếu bộ phận Bán lẻ + phiếu F lập.'),
    ('05', 'Nháp của người khác luôn ẩn', 'P0', 'C (tổng công ty); B có 1 phiếu Đang tạo.', '1. Đăng nhập C.\n2. Lọc Trạng thái Đang tạo.', '—',
     '- Không thấy nháp của B.'),
    ('06', 'Kế toán thanh toán thấy màn chờ duyệt', 'P0', 'Tài khoản K có quyền Kế toán thanh toán, công ty 1; công ty 1 có 5 phiếu chờ.',
     '1. Đăng nhập K.\n2. ' + MENU_CD, '—',
     '- Tiêu đề "Phiếu yêu cầu điều chỉnh công nợ chờ duyệt".\n- Đúng 5 phiếu, đều Chờ tạo phiếu kế toán.\n- Không có nút Tạo mới.'),
    ('07', 'Không có quyền Kế toán thanh toán ở màn chờ duyệt', 'P0', 'Tài khoản A.', '1. Đăng nhập A.\n2. Mở màn chờ duyệt (nếu thấy menu).', '—',
     '- Không có mục menu chờ duyệt.\n- Mở bằng đường link thì danh sách rỗng.'),
    ('08', 'Kế toán khác công ty không xử lý được', 'P0', 'Tài khoản K2 Kế toán thanh toán công ty 2; phiếu chờ của người lập công ty 1.',
     '1. Đăng nhập K2.\n2. Mở chi tiết phiếu (nếu trong phạm vi xem).', '—', '- Không có nút Tạo phiếu kế toán, Từ chối.'),
    ('09', 'Không phải người lập không sửa / xóa / gửi duyệt', 'P0', 'C; phiếu Từ chối của A.', '1. Mở chi tiết phiếu.', '—',
     '- Không có nút Sửa, Gửi duyệt, Xóa.'),
    ('10', 'Mở chi tiết ngoài phạm vi', 'P1', 'A; phiếu người khác ngoài phạm vi.', '1. Mở đường link chi tiết.', '—',
     '- Báo "Bạn không có quyền xem phiếu này".'),
]

S1 = [
    ('001', 'Mở màn từ phân hệ Tài chính', 'P0', 'DNS Admin.', '1. ' + MENU + '\n2. Quan sát danh sách.', '—',
     '- Tiêu đề "Phiếu yêu cầu điều chỉnh công nợ".\n- Mới tạo xếp trên.'),
    ('002', 'Mở màn từ phân hệ Bán hàng', 'P1', 'Cùng tài khoản.', '1. ' + MENU_SALE + '\n2. So tổng số với TC_01.001.', '—',
     '- Cùng màn, cùng tổng số phiếu.'),
    ('003', 'Các cột mặc định', 'P1', 'Chưa tùy chỉnh cột.', '1. ' + MENU + '\n2. Quan sát tiêu đề cột.', '—',
     '- 15 cột: STT, Mã phiếu, Loại phiếu, Số phiếu báo có, KH / NCC, Số tiền, Ngày tạo, Người tạo, Ngày cập nhật, Người cập nhật, '
     'Phòng ban, Ngày nhận, Người duyệt, Trạng thái, Hành động.'),
    ('004', 'Nút trên dòng theo trạng thái', 'P0', 'A lập phiếu 00402 Đang tạo; K là kế toán; phiếu 00401 Chờ tạo phiếu kế toán.',
     '1. A mở danh sách, xem dòng 00402.\n2. K mở danh sách, xem dòng 00401.', '—',
     '- 00402 (A): Sửa, Xóa, nút ba chấm (In phiếu, Xuất Excel, Lịch sử).\n- 00401 (K): Tạo phiếu kế toán, Từ chối, nút ba chấm.'),
    ('005', 'Bấm Mã phiếu', 'P0', '—', '1. Bấm mã TPE.DNDCCN1026.00401.', '—', '- Mở màn "Chi tiết phiếu yêu cầu điều chỉnh công nợ".'),
]

S2 = [
    ('001', 'Tìm nhanh theo mã phiếu', 'P0', '—', '1. Nhập "00401", bấm Tìm kiếm.', 'Ô tìm nhanh: 00401', '- Chỉ còn phiếu 00401.'),
    ('002', 'Lọc Loại phiếu', 'P0', 'Có 3 phiếu loại nhà cung cấp chờ duyệt.', '1. Tìm kiếm nâng cao.\n2. Loại phiếu = Điều chỉnh công nợ nhà cung cấp.\n3. Trạng thái = Chờ tạo phiếu kế toán.',
     '—', '- Còn 3 phiếu.'),
    ('003', 'Lọc Trạng thái', 'P0', '—', '1. Trạng thái = Từ chối.', '—', '- Chỉ phiếu Từ chối.'),
    ('004', 'Lọc Khách hàng / Nhà cung cấp', 'P1', 'Khách hàng KH-B nhận công nợ ở 2 phiếu.', '1. Gõ tên KH-B, chọn.', '—', '- Ra 2 phiếu.'),
    ('005', 'Lọc Hợp đồng điều chỉnh từ / đến', 'P1', '—', '1. Nhập Hợp đồng điều chỉnh đến = "KD2_26_1434".', '—',
     '- Chỉ phiếu có hợp đồng "đến" chứa chuỗi.'),
    ('006', 'Lọc Số tiền', 'P1', '—', '1. Số tiền từ 1,000,000 đến 5,000,000.', '—', '- Chỉ phiếu tổng tiền trong khoảng.'),
    ('007', 'Lọc Ngày tạo', 'P1', '—', '1. Ngày tạo 21/10/2026 đến 21/10/2026.', '—', '- Chỉ phiếu tạo ngày 21/10/2026, kể cả 23:59.'),
    ('008', 'Lọc Người tạo / Người duyệt', 'P2', '—', '1. Người duyệt = Dương Đức Thái.', '—', '- Chỉ phiếu người này đã xử lý.'),
    ('009', 'Làm mới', 'P1', 'Đang lọc nhiều ô.', '1. Bấm Làm mới.', '—', '- Mọi ô trống, nạp lại trang 1.'),
    ('010', 'Cài đặt bộ lọc', 'P2', '—', '1. Cài đặt bộ lọc, bỏ tích Số tiền, Lưu.', '—', '- Ô Số tiền không còn.\n- Khôi phục mặc định đưa về đủ.'),
    ('011', 'Tùy chỉnh cột', 'P2', '—', '1. Cấu hình cột hiển thị.\n2. Bỏ tích Phòng ban, Lưu.', '—',
     '- Cột Phòng ban ẩn.\n- STT, Mã phiếu, Hành động có ổ khóa.'),
    ('012', 'Sắp xếp', 'P2', '—', '1. Bấm tiêu đề Số tiền, Ngày nhận.', '—', '- Sắp xếp đúng, về trang 1.'),
]

S3 = [
    ('001', 'Mở màn Tạo mới', 'P0', '—', TAO, '—',
     '- Loại phiếu mặc định "Điều chỉnh công nợ khách hàng".\n- Bảng ghi "Chưa có dòng điều chỉnh nào.".'),
    ('002', 'Gửi duyệt khi trống — báo lỗi một lượt', 'P0', '—', TAO + '\n3. Bấm Gửi duyệt.', '—',
     '- Báo cùng lúc: Diễn giải, bảng chưa có dòng.\n- Không lưu.'),
    ('003', 'Gửi duyệt thiếu khách hàng / hợp đồng / số tiền bên đến', 'P0', '—',
     TAO + '\n3. Nhập Diễn giải, bấm Thêm dòng.\n4. Chọn bên "từ" đủ, bên "đến" để trống, Số tiền 0.\n5. Gửi duyệt.', '—',
     '- Cùng lượt: Khách hàng "đến", Hợp đồng "đến" ("Bắt buộc chọn hợp đồng/đơn hàng"), Số tiền ("Phải lớn hơn 0").'),
    ('004', 'Lưu nháp cho phép thiếu hợp đồng bên đến', 'P0', '—', TAO + '\n3. Nhập đủ trừ hợp đồng bên "đến".\n4. Lưu nháp.', '—',
     '- Báo "Lưu phiếu yêu cầu điều chỉnh công nợ thành công", phiếu Đang tạo.'),
    ('005', 'Popup chọn khách hàng', 'P1', '—', TAO + '\n3. Thêm dòng, bấm ô Khách hàng bên "từ".', '—',
     '- Cửa sổ "Chọn khách hàng", ô tìm theo Tên / Mã, MST, SĐT.\n- Cột: Mã KH và Tên khách hàng, Loại, MST, SĐT, Email, Nhóm KH, Địa chỉ, Tỉnh/TP.'),
    ('006', 'Hợp đồng khóa khi chưa chọn khách hàng', 'P1', '—', '1. Thêm dòng, chưa chọn khách hàng, bấm ô Hợp đồng/Đơn hàng.', '—',
     '- Ô bị khóa, gợi ý "Vui lòng chọn khách hàng trước".'),
    ('007', 'Popup chọn hợp đồng', 'P0', 'KH-A có 2 hợp đồng còn nợ.', '1. Chọn KH-A, bấm ô Hợp đồng/Đơn hàng.', '—',
     '- Cửa sổ "Chọn đơn hàng/hợp đồng KH-A": Số đơn hàng/Hợp đồng, Ngày lập, Giá trị hợp đồng, Số tiền còn nợ.\n'
     '- Chọn xong: Số dư cuối kỳ, NVKD tự điền.'),
    ('008', 'Khách hàng không có hợp đồng', 'P2', 'KH-C không có hợp đồng.', '1. Chọn KH-C, mở popup hợp đồng.', '—',
     '- "Không có hợp đồng phù hợp.".'),
    ('009', 'Tổng tiền không khớp', 'P0', '—', TAO + '\n' + DONG.replace('Số tiền 10,000,000.\n', 'Số tiền 10,000,000.\n', 1)
     + '\n7. Sửa Số tiền "đến" = 8,000,000, Gửi duyệt.', '—',
     '- Dòng "Số tiền còn lại" = 2,000,000.\n- Báo "Tổng số tiền điều chỉnh đến phải bằng số tiền điều chỉnh từ (dòng 1)".'),
    ('010', 'Bên đến trùng hợp đồng bên từ', 'P0', '—', TAO + '\n3. Chọn bên "đến" cùng KH-A, HĐ-A1 như bên "từ".\n4. Gửi duyệt.', '—',
     '- Báo "Hợp đồng điều chuyển đến trùng với điều chuyển từ".'),
    ('011', 'Chia công nợ cho nhiều nơi nhận', 'P1', '—', TAO + '\n' + DONG + '\n7. Sửa "đến" 6,000,000, thêm dòng "đến" KH-C 4,000,000.\n8. Gửi duyệt.', '—',
     '- Gửi thành công; nhóm có 2 dòng "đến".'),
    ('012', 'Gửi duyệt thành công', 'P0', 'K là Kế toán thanh toán cùng công ty.', TAO + '\n' + DONG + '\n7. Gửi duyệt.', '—',
     '- Báo "Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành công".\n- Phiếu mới mã TPE.DNDCCN<tháng năm>.NNNNN, Chờ tạo phiếu kế toán, có Ngày nhận.\n'
     '- K nhận thông báo.'),
    ('013', 'Đổi loại phiếu khi đã có dòng', 'P1', 'Bảng có 1 nhóm.', '1. Đổi Loại phiếu sang nhà cung cấp.', '—',
     '- Hỏi xác nhận.\n- Đồng ý: bảng bị xóa sạch, cột đổi thành Nhà cung cấp, Hợp đồng mua, Số dư, Nhân viên.\n- Hiện Tiền tệ.'),
    ('014', 'Loại NCC ngoại tệ', 'P1', '—', '1. Loại nhà cung cấp, Tiền tệ USD.\n2. Để trống Tỷ giá, Gửi duyệt.', '—',
     '- Hiện ô Tỷ giá bắt buộc, cột Số dư (VNĐ), Số tiền (VNĐ).\n- Báo "Vui lòng nhập tỷ giá lớn hơn 0 trước khi gửi duyệt".'),
    ('015', 'NCC đến là KHÁCH KHÔNG RÕ', 'P2', '—', '1. Loại nhà cung cấp, bên "đến" chọn 29TPHPTH-203-KHÁCH KHÔNG RÕ, để trống hợp đồng mua.\n2. Gửi duyệt (tổng khớp).',
     '—', '- Gửi thành công.'),
    ('016', 'Lưu và tiếp tục', 'P1', '—', TAO + '\n' + DONG + '\n7. Bấm Lưu và tiếp tục.', '—', '- Phiếu lưu Đang tạo, form trống để lập tiếp.'),
    ('017', 'Rời màn khi chưa lưu', 'P1', 'Đã nhập Diễn giải.', '1. Bấm Quay lại.', '—', '- Hỏi xác nhận rời trang.'),
]

S4 = [
    ('001', 'Sửa phiếu Đang tạo', 'P0', 'A lập 00402 Đang tạo.', '1. Bấm biểu tượng Sửa ở dòng.\n2. Sửa Diễn giải, Lưu nháp.', '—',
     '- Tiêu đề "Sửa phiếu yêu cầu điều chỉnh công nợ: TPE.DNDCCN1026.00402".\n- Lưu thành công; lịch sử có Thay đổi thông tin.'),
    ('002', 'Sửa phiếu Từ chối, gửi lại', 'P0', 'Phiếu Từ chối của A.', '1. Sửa.\n2. Đọc Ghi chú không duyệt.\n3. Gửi duyệt.', '—',
     '- Ghi chú không duyệt hiện lý do cũ, chỉ đọc.\n- Phiếu Chờ tạo phiếu kế toán; lý do cũ bị xóa.'),
    ('003', 'Gửi duyệt từ màn chi tiết', 'P0', 'Phiếu 00402 Đang tạo đủ dữ liệu.', '1. Mở chi tiết, bấm Gửi duyệt.', '—',
     '- Báo "Gửi duyệt phiếu yêu cầu điều chỉnh công nợ thành công".'),
    ('004', 'Gửi duyệt từ chi tiết khi thiếu hợp đồng bên đến', 'P0', 'Phiếu nháp thiếu hợp đồng "đến".', '1. Mở chi tiết, Gửi duyệt.', '—',
     '- Báo lỗi dòng chưa chọn hợp đồng/đơn hàng; phiếu giữ Đang tạo.'),
    ('005', 'Xóa phiếu', 'P0', 'Phiếu nháp của A.', '1. Bấm biểu tượng Xóa.\n2. Bấm Xóa.', '—',
     '- Hộp "Bạn có chắc muốn xóa phiếu yêu cầu điều chỉnh công nợ \'<mã>\'?".\n- Báo "Xóa phiếu yêu cầu điều chỉnh công nợ thành công".'),
    ('006', 'Hủy xóa', 'P2', '—', '1. Bấm Xóa rồi Hủy.', '—', '- Phiếu còn nguyên.'),
]

S5 = [
    ('001', 'Nội dung màn chi tiết', 'P0', 'Phiếu 00401 Chờ tạo phiếu kế toán.', '1. Mở chi tiết.', '—',
     '- Mọi ô chỉ đọc; bảng "từ" / "đến" gộp dòng đúng.\n- Có khối Lịch sử.'),
    ('002', 'Từ chối thiếu lý do', 'P0', 'K; phiếu 00401.', '1. Bấm Từ chối.\n2. Để trống, bấm Từ chối.', '—',
     '- "Vui lòng nhập lý do từ chối", cửa sổ không đóng.'),
    ('003', 'Từ chối thành công', 'P0', 'Như TC_05.002.', '1. Nhập lý do, bấm Từ chối.', 'Lý do: Sai hợp đồng nhận',
     '- Báo "Từ chối phiếu yêu cầu điều chỉnh công nợ thành công", về danh sách.\n- Người lập nhận thông báo kèm lý do.'),
    ('004', 'Nút Từ chối trên dòng', 'P1', 'K; màn chờ duyệt.', '1. Bấm biểu tượng Từ chối.', '—', '- Mở màn chi tiết phiếu.'),
    ('005', 'Tạo phiếu kế toán', 'P0', 'K; phiếu 00401.', '1. Bấm Tạo phiếu kế toán.', '—',
     '- Mở màn "Tạo phiếu kế toán" điền sẵn phiếu yêu cầu và các dòng.\n- Lưu phiếu kế toán: phiếu yêu cầu sang Đã tạo phiếu kế toán.'),
    ('006', 'Thoát màn phiếu kế toán không lưu', 'P2', 'Như TC_05.005.', '1. Mở Tạo phiếu kế toán rồi Quay lại.', '—',
     '- Phiếu yêu cầu vẫn Chờ tạo phiếu kế toán.'),
    ('007', 'In phiếu', 'P1', '—', '1. Bấm nút ba chấm, chọn In phiếu.', '—',
     '- Cửa sổ "Xem trước phiếu <mã>", tiêu đề "PHIẾU YÊU CẦU ĐIỀU CHỈNH CÔNG NỢ", logo công ty của phiếu, bảng từ / đến.'),
    ('008', 'Xuất Excel danh sách', 'P1', 'Lọc Trạng thái = Từ chối.', '1. Bấm Xuất Excel trên thanh công cụ.', '—',
     '- Tải file đúng các phiếu Từ chối; báo "Xuất Excel thành công".'),
    ('009', 'Xuất Excel một phiếu', 'P2', '—', '1. Nút ba chấm, chọn Xuất Excel.', '—', '- Tải file của đúng phiếu đó.'),
    ('010', 'Lịch sử thay đổi', 'P1', 'Phiếu 00402 vừa tạo.', '1. Nút ba chấm, chọn Lịch sử.', '—',
     '- Cửa sổ "Lịch sử thay đổi: TPE.DNDCCN1026.00402" có mốc Tạo mới, người thực hiện.'),
]

S6 = [
    ('001', 'Luồng lập, gửi, tạo phiếu kế toán', 'P0', 'A người lập; K kế toán cùng công ty.',
     '1. A lập phiếu, Gửi duyệt.\n2. K mở màn chờ duyệt, Tạo phiếu kế toán, lưu.', '—',
     '- Bước 1: K nhận thông báo; phiếu có trong màn chờ duyệt.\n- Bước 2: phiếu rời màn chờ duyệt, trạng thái Đã tạo phiếu kế toán.'),
    ('002', 'Luồng từ chối, sửa, gửi lại', 'P0', 'Như TC_06.001.', '1. A gửi.\n2. K từ chối.\n3. A sửa, gửi lại.', '—',
     '- Lịch sử đủ mốc theo thứ tự; phiếu quay lại màn chờ duyệt.'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC, TÌM KIẾM & DANH SÁCH', S2),
    ('III', 'LẬP PHIẾU (TẠO MỚI) & RÀNG BUỘC NHẬP LIỆU', S3),
    ('IV', 'CHỈNH SỬA, GỬI DUYỆT & XÓA', S4),
    ('V', 'XEM CHI TIẾT, TỪ CHỐI, TẠO PHIẾU KẾ TOÁN, IN & XUẤT', S5),
    ('VI', 'E2E FLOW', S6),
]

# ---------------------------------------------------------------- bổ sung theo chuẩn (30/10/2026)
# Mẫu Danh mục quốc gia + 8 ý góp ý tester 07/10/2026 (../phieu-theo-form-quoc-gia/tc_phieu_bosung.py).
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from tc_phieu_bosung import (ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases,  # noqa: E402
                             weird_param_case, add_advanced_step, fill_pre, check_no_dash_pre)

SCREEN = ListScreen(menu=MENU, title='Phiếu yêu cầu điều chỉnh công nợ', total=12540, quick_label='mã phiếu',
                    quick_sample='DNDCCN1026', quick_hit='các phiếu lập tháng 10/2026',
                    filters=[('Loại phiếu', 'Điều chỉnh công nợ khách hàng'), ('Trạng thái', 'Chờ tạo phiếu kế toán')],
                    org_levels=('Công ty', 'Phòng ban', 'Bộ phận'))
S1[0] = open_menu_case(SCREEN, pre='Tài khoản DNS Admin; trong phạm vi xem có 12540 phiếu.',
                       extra=['- Lưu ý: số tổng chưa có dấu phẩy ngăn hàng nghìn (lỗi chung đã ghi nhận).'])
S1.append(weird_param_case('006', SCREEN, 'tiêu đề "Phiếu yêu cầu điều chỉnh công nợ", có nút Tạo mới'))
S1.append(('007', 'Đang lọc rồi mở lối vào chờ duyệt', 'P1',
           'Tài khoản K có quyền Kế toán thanh toán; đang ở danh sách chung, lọc Trạng thái = Từ chối.',
           '1. ' + MENU_CD + '\n2. Quan sát tiêu đề và danh sách.', '—',
           '- Tiêu đề "Phiếu yêu cầu điều chỉnh công nợ chờ duyệt", không có nút Tạo mới.\n'
           '- Danh sách chỉ còn phiếu Chờ tạo phiếu kế toán của người lập cùng công ty, từ trang 1.'))
S1.append(('008', 'Làm mới ở màn chờ duyệt giữ nguyên chế độ', 'P2', 'Tài khoản K; đang ở màn chờ duyệt, lọc Loại phiếu.',
           '1. Bấm Làm mới.', '—', '- Xóa điều kiện lọc nhưng vẫn ở màn chờ duyệt (tiêu đề không đổi).'))
ORG = org_cases(SCREEN, 13)
MEM = filter_memory_cases(SCREEN, 16)
S2[:] = add_advanced_step(S2, {'003', '004', '005', '006', '007', '008'}, MENU) + ORG + MEM + combo_cases(SCREEN, 21)
S3.append(('018', 'Lưu và tiếp tục khi dữ liệu còn thiếu', 'P0',
           'Đang ở màn Tạo; đã thêm 1 dòng, bên "từ" chọn KH-A nhưng chưa nhập Số tiền, bên "đến" để trống; Diễn giải trống.',
           TAO + '\n3. Bấm Thêm dòng, chọn KH-A bên "từ".\n4. Bấm Lưu và tiếp tục.', 'Diễn giải: trống\nSố tiền: trống',
           '- Phiếu vẫn được lưu nháp (trạng thái Đang tạo) và mở form trống để lập tiếp — nháp không bắt buộc các ô này.\n'
           '- Lưu ý: các ô thiếu chỉ bị chặn khi Gửi duyệt (xem TC_03.002, TC_03.003).'))
S3.append(('019', 'Gửi duyệt từ phiếu nháp vừa lưu bằng Lưu và tiếp tục', 'P1', 'Phiếu nháp ở TC_03.018.',
           '1. Mở chi tiết phiếu nháp.\n2. Bấm Gửi duyệt.', '—',
           '- Báo lỗi các ô còn thiếu (Diễn giải, Số tiền, dòng "Điều chỉnh đến"); phiếu giữ Đang tạo.'))
PRE_LIST = 'Tài khoản DNS Admin; danh sách có 12540 phiếu, đủ 2 loại phiếu và các trạng thái.'
PRE_FORM = 'Tài khoản A; KH-A có hợp đồng HĐ-A1 còn nợ 50,000,000; KH-B có hợp đồng HĐ-B1.'
S1[:] = fill_pre(S1, {}, PRE_LIST)
S2[:] = fill_pre(S2, {}, PRE_LIST)
S3[:] = fill_pre(S3, {}, PRE_FORM)
S4[:] = fill_pre(S4, {}, 'A lập phiếu nháp TPE.DNDCCN1026.00402.')
S5[:] = fill_pre(S5, {}, 'Phiếu TPE.DNDCCN1026.00401 Chờ tạo phiếu kế toán, 1 nhóm điều chỉnh.')
check_no_dash_pre(SECTIONS, ROLE_TCS)

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1', feature_name='Phiếu yêu cầu điều chỉnh công nợ - Cập nhật ngày 30/10/2026',
          module_name='YC điều chỉnh công nợ', description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
