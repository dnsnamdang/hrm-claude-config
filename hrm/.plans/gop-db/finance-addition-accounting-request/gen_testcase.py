# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu yêu cầu hạch toán bổ sung" — skill testcase-documenter (tc_engine), 30/10/2026.

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
        '"Phiếu yêu cầu hạch toán bổ sung".')
MENU_SALE = 'Vào phân hệ Bán hàng > menu "Yêu cầu" > nhóm "Công nợ - Thu - Chi" > bấm "YC hạch toán bổ sung".'
MENU_CD = ('Vào phân hệ Tài chính > menu "Chờ duyệt" > nhóm "Phê duyệt - Công nợ - Thu - Chi" > bấm '
           '"Phiếu yêu cầu hạch toán bổ sung chờ duyệt".')
TAO = '1. ' + MENU + '\n2. Bấm "Tạo mới".'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn Phiếu yêu cầu hạch toán bổ sung dùng để nhân viên đề nghị kế toán hạch toán bổ sung một khoản công nợ.\n'
     'Phiếu lưu nháp (Đang tạo), gửi duyệt (Chờ duyệt); Kế toán thanh toán Từ chối (về Đang tạo kèm Ghi chú duyệt) hoặc kế '
     'toán Lập phiếu kế toán để ghi sổ.'),
    ('2. Đối tượng được tính / hiển thị',
     '- 7 loại yêu cầu: Điều chỉnh công nợ khách hàng, Điều chỉnh công nợ nhà cung cấp, Hạch toán công nợ NCC bảo hành, '
     'Hạch toán công nợ NCC thiếu hàng, NCC hỗ trợ phát triển thị trường, Khác, Phối hợp kinh doanh.\n'
     '- Trạng thái: Đang tạo (xám), Chờ duyệt (vàng), Đang duyệt (vàng), Đã duyệt (xanh).\n'
     '- Màn chờ duyệt: luôn chỉ phiếu Chờ duyệt.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác: luôn ẩn.\n'
     '- Ở màn chờ duyệt: người không có quyền kế toán chỉ thấy phiếu của mình.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày lập phiếu, lấy trọn hai đầu mút.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     '- 2 loại Điều chỉnh công nợ: phiếu > các dòng Chi tiết hạch toán (đối tượng, hợp đồng, số tiền, ghi chú).\n'
     '- Các loại khác: phiếu có 1 đối tượng, 1 số tiền, 1 diễn giải.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Số tiền phiếu loại Điều chỉnh công nợ = tổng số tiền các dòng.\n- Đổi loại yêu cầu xóa sạch các trường phụ thuộc loại.'),
    ('7. Phân quyền cấp',
     '- Xem phiếu yêu cầu hạch toán bổ sung - tổng công ty.\n'
     '- Xem phiếu yêu cầu hạch toán bổ sung - công ty.\n'
     '- Xem phiếu yêu cầu hạch toán bổ sung - phòng ban.\n'
     '- Xem phiếu yêu cầu hạch toán bổ sung - bộ phận.\n'
     '- Kế toán thanh toán: Từ chối, Lập phiếu kế toán loại 1–6.\n'
     '- Kế toán: Lập phiếu kế toán loại Phối hợp kinh doanh (công ty có phòng hỗ trợ).\n'
     '- Kế toán kho: nhận thông báo khi có phiếu gửi duyệt.'),
    ('8. Cách tính các ô thống kê',
     '- Dòng Tổng cộng của bảng Chi tiết hạch toán = tổng Số tiền các dòng.\n'
     '- Ô "Hiển thị a–b / N": N là tổng phiếu khớp bộ lọc trong phạm vi quyền.'),
    ('9. Ghi chú đọc bảng',
     '- Số tiền hiển thị dạng 1,234,567 kèm đơn vị tiền.\n'
     '- Lưu ý: Lưu nháp chỉ bắt buộc Loại yêu cầu; Gửi duyệt mới kiểm tra đủ.\n'
     '- Lưu ý: Từ chối KHÔNG có trạng thái riêng, phiếu trở về Đang tạo và hiện Ghi chú duyệt.\n'
     '- Lưu ý: phiếu tạo trước khi bật lịch sử sẽ báo "Chưa có lịch sử thao tác nào.".'),
]

ROLE_TCS = [
    ('00', 'Không có quyền nào chỉ thấy phiếu mình lập', 'P0', 'Tài khoản A không có quyền xem, không là kế toán; A lập 3 phiếu.',
     '1. Đăng nhập bằng A.\n2. ' + MENU, '—', '- Tổng số = 3.\n- Chỉ phiếu A lập.'),
    ('01', 'Quyền xem - tổng công ty', 'P1', 'Tài khoản C có quyền tổng công ty.', '1. Đăng nhập bằng C.\n2. ' + MENU, '—',
     '- Thấy phiếu mọi công ty (trừ nháp người khác).'),
    ('02', 'Quyền xem - công ty với loại Phối hợp kinh doanh', 'P0',
     'Tài khoản D công ty 1; phiếu Phối hợp kinh doanh lập ở công ty 2 có phòng hỗ trợ thuộc công ty 1.',
     '1. Đăng nhập D.\n2. ' + MENU, '—', '- Thấy phiếu loại 1–6 của công ty 1.\n- Thấy cả phiếu Phối hợp kinh doanh đó.'),
    ('03', 'Quyền xem - phòng ban / bộ phận', 'P1', 'Tài khoản E quản lý phòng Kinh doanh.', '1. Đăng nhập E.\n2. ' + MENU, '—',
     '- Chỉ phiếu phòng Kinh doanh và phiếu E lập.'),
    ('04', 'Nháp của người khác luôn ẩn', 'P0', 'C; B có 1 phiếu Đang tạo.', '1. Đăng nhập C.\n2. Lọc Trạng thái Đang tạo.', '—',
     '- Không thấy nháp của B.'),
    ('05', 'Kế toán thanh toán ở màn chờ duyệt', 'P0', 'K có quyền Kế toán thanh toán công ty 1.', '1. Đăng nhập K.\n2. ' + MENU_CD, '—',
     '- Tiêu đề "Phiếu yêu cầu hạch toán bổ sung chờ duyệt".\n- Chỉ phiếu Chờ duyệt trong phạm vi công ty.\n- Không có nút Tạo mới.'),
    ('06', 'Người thường ở màn chờ duyệt', 'P1', 'A có 1 phiếu Chờ duyệt.', '1. Đăng nhập A.\n2. Mở màn chờ duyệt.', '—',
     '- Chỉ thấy phiếu Chờ duyệt của mình.'),
    ('07', 'Kế toán thanh toán xử lý loại 1–6', 'P0', 'K; phiếu loại Điều chỉnh công nợ khách hàng Chờ duyệt cùng công ty.',
     '1. Mở chi tiết phiếu.', '—', '- Có Từ chối và Lập phiếu kế toán.'),
    ('08', 'Kế toán xử lý loại Phối hợp kinh doanh', 'P0',
     'Tài khoản L có quyền Kế toán, công ty 1; phiếu Phối hợp kinh doanh Chờ duyệt có phòng hỗ trợ thuộc công ty 1.',
     '1. Đăng nhập L.\n2. Mở chi tiết phiếu.', '—', '- Có Lập phiếu kế toán.\n- Với phiếu loại 1–6: không có Lập phiếu kế toán.'),
    ('09', 'Không phải người lập không sửa / xóa / gửi duyệt', 'P0', 'C; phiếu Đang tạo của A trong phạm vi.', '1. Mở chi tiết.', '—',
     '- Không có Sửa, Gửi duyệt, Xóa.'),
    ('10', 'Mở chi tiết ngoài phạm vi', 'P1', 'A; phiếu người khác.', '1. Mở đường link chi tiết.', '—', '- Báo "Bạn không có quyền xem phiếu này".'),
]

S1 = [
    ('001', 'Mở màn từ phân hệ Tài chính', 'P0', 'DNS Admin.', '1. ' + MENU + '\n2. Quan sát danh sách.', '—',
     '- Tiêu đề "Phiếu yêu cầu hạch toán bổ sung".\n- Mới tạo xếp trên.'),
    ('002', 'Mở màn từ phân hệ Bán hàng', 'P1', '—', '1. ' + MENU_SALE + '\n2. So tổng số với TC_01.001.', '—', '- Cùng màn, cùng tổng số.'),
    ('003', 'Các cột mặc định', 'P1', 'Chưa tùy chỉnh cột.', '1. ' + MENU + '\n2. Quan sát tiêu đề cột.', '—',
     '- 14 cột hiện: STT, Số phiếu, Loại yêu cầu, KH / NCC, Số tiền, Diễn giải, Người tạo, Ngày tạo, Phòng ban, Ngày gửi, '
     'Người duyệt, Ngày duyệt, Trạng thái, Hành động.\n- Ngày cập nhật, Người cập nhật ẩn.'),
    ('004', 'Nút trên dòng phiếu Chờ duyệt', 'P0', 'K; phiếu PYCHTBS-002289 Chờ duyệt.', '1. Đăng nhập K, quan sát dòng 002289.', '—',
     '- Lập phiếu kế toán, In phiếu, nút ba chấm (Xuất Excel, Lịch sử).'),
    ('005', 'Bấm Số phiếu', 'P0', '—', '1. Bấm PYCHTBS-002289.', '—', '- Mở "Chi tiết phiếu yêu cầu hạch toán bổ sung: PYCHTBS-002289".'),
]

S2 = [
    ('001', 'Tìm nhanh theo số phiếu', 'P0', '—', '1. Nhập "002289", bấm Tìm kiếm.', 'Ô tìm nhanh: 002289', '- Chỉ còn phiếu 002289.'),
    ('002', 'Lọc Loại yêu cầu', 'P0', '—', '1. Tìm kiếm nâng cao.\n2. Loại yêu cầu = Điều chỉnh công nợ nhà cung cấp.', '—',
     '- Chỉ phiếu loại đó.'),
    ('003', 'Lọc Trạng thái', 'P1', '—', '1. Trạng thái = Chờ duyệt.', '—', '- Chỉ phiếu Chờ duyệt.'),
    ('004', 'Lọc Khách hàng / Nhà cung cấp', 'P1', 'NCC X xuất hiện ở dòng chi tiết của 2 phiếu.', '1. Chọn NCC X.', '—',
     '- Ra 2 phiếu (khớp cả đối tượng ở dòng chi tiết).'),
    ('005', 'Lọc Diễn giải', 'P2', 'Ghi chú dòng chứa "đối chiếu".', '1. Nhập Diễn giải = "đối chiếu".', '—',
     '- Ra phiếu có diễn giải hoặc ghi chú dòng chứa chuỗi.'),
    ('006', 'Lọc Phiếu xác nhận bảo hành', 'P2', '—', '1. Nhập mã phiếu xác nhận bảo hành.', '—', '- Chỉ phiếu gắn phiếu đó.'),
    ('007', 'Lọc Ngày tạo', 'P1', '—', '1. Ngày tạo 21/10/2026 đến 21/10/2026.', '—', '- Đúng phiếu ngày đó, kể cả 23:59.'),
    ('008', 'Làm mới', 'P1', 'Đang lọc nhiều ô.', '1. Bấm Làm mới.', '—', '- Mọi ô trống, nạp lại trang 1.'),
    ('009', 'Cài đặt bộ lọc', 'P2', '—', '1. Cài đặt bộ lọc, bỏ tích Diễn giải, Lưu.', '—', '- Ô Diễn giải không còn.'),
    ('010', 'Tùy chỉnh cột', 'P2', '—', '1. Cấu hình cột, tích Người cập nhật, Lưu.', '—', '- Cột Người cập nhật hiện.\n- STT, Số phiếu, Hành động có ổ khóa.'),
    ('011', 'Sắp xếp', 'P2', '—', '1. Bấm tiêu đề Số tiền, Ngày gửi.', '—', '- Sắp xếp đúng.'),
]

S3 = [
    ('001', 'Mở màn Tạo mới', 'P0', '—', TAO, '—',
     '- Tiêu đề "Tạo phiếu yêu cầu hạch toán bổ sung".\n- Loại yêu cầu trống, Loại tiền VNĐ.'),
    ('002', 'Lưu nháp khi chỉ chọn Loại yêu cầu', 'P0', '—', TAO + '\n3. Chọn Loại yêu cầu = Khác.\n4. Bấm Lưu nháp.', '—',
     '- Báo "Lưu thành công", phiếu Đang tạo.'),
    ('003', 'Lưu nháp khi chưa chọn Loại yêu cầu', 'P1', '—', TAO + '\n3. Bấm Lưu nháp.', '—', '- "Bắt buộc phải nhập" dưới Loại yêu cầu.'),
    ('004', 'Gửi duyệt khi trống', 'P0', '—', TAO + '\n3. Chọn Loại yêu cầu = Khác.\n4. Gửi duyệt.', '—',
     '- Báo cùng lúc: Đối tượng, Số tiền, Diễn giải, File đính kèm ("Bắt buộc phải nhập").'),
    ('005', 'Trường theo loại Điều chỉnh công nợ khách hàng', 'P0', '—', TAO + '\n3. Chọn loại Điều chỉnh công nợ khách hàng.', '—',
     '- Ẩn Số tiền, Diễn giải ở đầu phiếu.\n- Hiện bảng Chi tiết hạch toán: Khách hàng, Hợp đồng bán, Số tiền, Ghi chú.'),
    ('006', 'Gửi duyệt loại Điều chỉnh công nợ không có dòng', 'P0', 'Như TC_03.005, có file đính kèm.', '1. Gửi duyệt.', '—',
     '- Báo "Phiếu chưa có dòng chi tiết nào, không gửi duyệt được".'),
    ('007', 'Thêm dòng chi tiết đủ dữ liệu', 'P0', 'KH-A có hợp đồng HĐ-A1.',
     '1. Bấm Thêm dòng.\n2. Chọn KH-A, HĐ-A1, Số tiền 5,000,000, Ghi chú.\n3. Đính kèm 1 file.\n4. Gửi duyệt.', '—',
     '- Báo "Gửi duyệt thành công".\n- Số tiền phiếu = 5,000,000.\n- Kế toán kho nhận thông báo "[HTBS] Chờ duyệt".'),
    ('008', 'Hợp đồng khóa khi chưa chọn đối tượng', 'P1', '—', '1. Thêm dòng, bấm ô Hợp đồng bán khi chưa chọn khách hàng.', '—',
     '- Ô bị khóa.'),
    ('009', 'Loại Hạch toán công nợ NCC bảo hành', 'P1', 'Có phiếu xác nhận bảo hành đã xác nhận.',
     TAO + '\n3. Chọn loại Hạch toán công nợ NCC bảo hành.\n4. Bấm ô Phiếu xác nhận bảo hành, chọn phiếu.', '—',
     '- Nhà cung cấp, Số tiền tự điền (chỉ đọc).'),
    ('010', 'Loại Hạch toán công nợ NCC thiếu hàng nhiều NCC', 'P2', 'Phiếu xử lý hàng thiếu có 2 NCC.',
     TAO + '\n3. Chọn loại thiếu hàng, chọn phiếu xử lý.', '—', '- Ô Nhà cung cấp cho chọn 1 trong 2 NCC.'),
    ('011', 'Loại Khác chọn Nhân viên', 'P1', '—', TAO + '\n3. Chọn loại Khác, Đối tượng = Nhân viên.\n4. Gửi duyệt khi chưa chọn nhân viên.', '—',
     '- Báo "Bắt buộc phải nhập" tại ô Nhân viên.'),
    ('012', 'Đổi loại xóa trường phụ thuộc', 'P1', 'Đã chọn loại Khác, Đối tượng NCC, nhập Số tiền.', '1. Đổi sang loại Điều chỉnh công nợ khách hàng.', '—',
     '- Các ô Đối tượng, Số tiền, Diễn giải bị xóa / ẩn.'),
    ('013', 'Tỷ giá bằng 0', 'P1', '—', '1. Nhập Tỷ giá 0, Gửi duyệt.', 'Tỷ giá: 0', '- Báo Tỷ giá phải lớn hơn 0.'),
    ('014', 'Lưu và tiếp tục', 'P2', '—', TAO + '\n3. Chọn loại, bấm Lưu và tiếp tục.', '—', '- Lưu nháp, form trống.'),
    ('015', 'Rời màn khi chưa lưu', 'P1', 'Đã chọn loại.', '1. Bấm Quay lại.', '—', '- Hỏi xác nhận rời trang.'),
]

S4 = [
    ('001', 'Sửa phiếu Đang tạo', 'P0', 'A có phiếu Đang tạo.', '1. Bấm biểu tượng Sửa.\n2. Sửa Diễn giải, Lưu nháp.', '—',
     '- Tiêu đề "Sửa phiếu yêu cầu hạch toán bổ sung: <số phiếu>".\n- Lịch sử có Thay đổi thông tin (không lặp dòng trạng thái).'),
    ('002', 'Sửa rồi Gửi duyệt', 'P0', 'Như TC_04.001.', '1. Sửa Số tiền, Gửi duyệt.', '—',
     '- Lịch sử: mốc Thay đổi thông tin ghi Số tiền; mốc Thay đổi trạng thái riêng "Đang tạo sang Chờ duyệt".'),
    ('003', 'Gửi duyệt từ màn chi tiết', 'P0', 'Phiếu Đang tạo đủ dữ liệu.', '1. Mở chi tiết, Gửi duyệt.', '—', '- Báo "Gửi duyệt thành công".'),
    ('004', 'Xóa phiếu', 'P0', 'Phiếu Đang tạo của A.', '1. Bấm Xóa, bấm Xóa.', '—',
     '- Hộp "Bạn có chắc muốn xóa phiếu yêu cầu hạch toán bổ sung \'<số phiếu>\'?".\n- Báo "Xóa thành công".'),
    ('005', 'Phiếu Chờ duyệt không sửa / xóa được', 'P0', 'A có phiếu Chờ duyệt.', '1. Xem cột Hành động.', '—', '- Không có Sửa, Xóa.'),
]

S5 = [
    ('001', 'Chi tiết loại Điều chỉnh công nợ khách hàng', 'P0', 'Phiếu 002289.', '1. Mở chi tiết.', '—',
     '- Chỉ đọc; bảng Chi tiết hạch toán, File đính kèm, khối Lịch sử.'),
    ('002', 'Chi tiết loại Phối hợp kinh doanh', 'P1', 'Phiếu 002285.', '1. Mở chi tiết.', '—',
     '- Khối riêng: Khách hàng, Phòng thực hiện, Phòng hỗ trợ, Gửi tới công ty, Số hợp đồng, nội dung quyết toán, số lượng hạch toán.'),
    ('003', 'Từ chối thiếu lý do', 'P0', 'K; phiếu Chờ duyệt.', '1. Bấm Từ chối, để trống, bấm Từ chối.', '—', '- "Bắt buộc phải nhập", cửa sổ không đóng.'),
    ('004', 'Từ chối thành công', 'P0', 'Như TC_05.003.', '1. Nhập lý do, Từ chối.', 'Lý do: Sai hợp đồng',
     '- Báo "Từ chối phiếu thành công".\n- Phiếu về Đang tạo, hiện Ghi chú duyệt "Sai hợp đồng".\n- Người lập nhận "[HTBS] Từ chối".'),
    ('005', 'Lập phiếu kế toán', 'P0', 'K; phiếu 002289.', '1. Bấm Lập phiếu kế toán.', '—',
     '- Mở màn "Tạo phiếu kế toán" điền sẵn phiếu yêu cầu.'),
    ('006', 'In phiếu', 'P1', '—', '1. Bấm biểu tượng In phiếu.', '—',
     '- Cửa sổ xem trước, tiêu đề "YÊU CẦU HẠCH TOÁN BỔ SUNG", đúng loại, bảng chi tiết, tổng tiền.'),
    ('007', 'Xuất Excel danh sách chọn trường', 'P1', 'Lọc Trạng thái Chờ duyệt.',
     '1. Bấm Xuất Excel.\n2. Bỏ chọn hết, tích Số phiếu, Số tiền, Trạng thái.\n3. Xuất file.', '—',
     '- Cửa sổ "Chọn trường xuất file", mặc định 12/15.\n- File đúng 3 cột theo thứ tự đã tích, đúng các phiếu Chờ duyệt.'),
    ('008', 'Xuất Excel một phiếu', 'P2', '—', '1. Nút ba chấm, chọn Xuất Excel.', '—', '- Tải file của đúng phiếu.'),
    ('009', 'Lịch sử phiếu cũ', 'P2', 'Phiếu tạo trước khi bật lịch sử.', '1. Nút ba chấm, chọn Lịch sử.', '—',
     '- Cửa sổ "Lịch sử thay đổi: <số phiếu>" ghi "Chưa có lịch sử thao tác nào.".'),
]

S6 = [
    ('001', 'Luồng lập, gửi, lập phiếu kế toán', 'P0', 'A người lập; K Kế toán thanh toán cùng công ty.',
     '1. A lập phiếu loại Điều chỉnh công nợ khách hàng, Gửi duyệt.\n2. K mở màn chờ duyệt, Lập phiếu kế toán, lưu.', '—',
     '- Bước 1: Kế toán kho nhận thông báo; phiếu có ở màn chờ duyệt.\n- Bước 2: phiếu rời màn chờ duyệt, trạng thái Đang duyệt / Đã duyệt.'),
    ('002', 'Luồng từ chối, sửa, gửi lại', 'P0', 'Như TC_06.001.', '1. A gửi.\n2. K từ chối.\n3. A sửa, gửi lại.', '—',
     '- Lịch sử đủ mốc theo thứ tự; phiếu quay lại màn chờ duyệt.'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC, TÌM KIẾM & DANH SÁCH', S2),
    ('III', 'LẬP PHIẾU (TẠO MỚI) & RÀNG BUỘC NHẬP LIỆU', S3),
    ('IV', 'CHỈNH SỬA, GỬI DUYỆT & XÓA', S4),
    ('V', 'XEM CHI TIẾT, TỪ CHỐI, LẬP PHIẾU KẾ TOÁN, IN & XUẤT', S5),
    ('VI', 'E2E FLOW', S6),
]

# ---------------------------------------------------------------- bổ sung theo chuẩn (30/10/2026)
# Mẫu Danh mục quốc gia + 8 ý góp ý tester 07/10/2026 (../phieu-theo-form-quoc-gia/tc_phieu_bosung.py).
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from tc_phieu_bosung import (ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases,  # noqa: E402
                             weird_param_case, add_advanced_step, fill_pre, check_no_dash_pre)

SCREEN = ListScreen(menu=MENU, title='Phiếu yêu cầu hạch toán bổ sung', total=2140, quick_label='số phiếu',
                    quick_sample='0022', quick_hit='các phiếu PYCHTBS-0022xx',
                    filters=[('Loại yêu cầu', 'Điều chỉnh công nợ khách hàng'), ('Trạng thái', 'Chờ duyệt')])
S1[0] = open_menu_case(SCREEN, pre='Tài khoản DNS Admin; trong phạm vi xem có 2140 phiếu.',
                       extra=['- Lưu ý: số tổng chưa có dấu phẩy ngăn hàng nghìn (lỗi chung đã ghi nhận).'])
S1.append(weird_param_case('006', SCREEN, 'tiêu đề "Phiếu yêu cầu hạch toán bổ sung", có nút Tạo mới'))
S1.append(('007', 'Đang lọc rồi mở lối vào chờ duyệt', 'P1',
           'Tài khoản K có quyền Kế toán thanh toán; đang ở danh sách chung, lọc Trạng thái = Đã duyệt.',
           '1. ' + MENU_CD + '\n2. Quan sát tiêu đề và danh sách.', '—',
           '- Tiêu đề "Phiếu yêu cầu hạch toán bổ sung chờ duyệt", không có nút Tạo mới.\n'
           '- Danh sách chỉ còn phiếu Chờ duyệt trong phạm vi công ty / phòng hỗ trợ, từ trang 1.'))
S1.append(('008', 'Làm mới ở màn chờ duyệt giữ nguyên chế độ', 'P2', 'Tài khoản K; đang ở màn chờ duyệt, lọc Loại yêu cầu.',
           '1. Bấm Làm mới.', '—', '- Xóa điều kiện lọc nhưng vẫn ở màn chờ duyệt (tiêu đề không đổi).'))
ORG = org_cases(SCREEN, 12)
MEM = filter_memory_cases(SCREEN, 15)
S2[:] = add_advanced_step(S2, {'003', '004', '005', '006', '007'}, MENU) + ORG + MEM + combo_cases(SCREEN, 20)
S3.append(('016', 'Lưu và tiếp tục khi chưa chọn Loại yêu cầu', 'P0',
           'Đang ở màn Tạo; đã chọn Loại tiền USD, nhập Tỷ giá 25,000, đính kèm 1 file; Loại yêu cầu còn trống.',
           TAO + '\n3. Chọn Loại tiền, nhập Tỷ giá, thêm file.\n4. Bấm Lưu và tiếp tục.', 'Loại tiền: USD\nTỷ giá: 25,000',
           '- Chữ đỏ "Bắt buộc phải nhập" dưới Loại yêu cầu.\n- KHÔNG lưu, KHÔNG mở form mới; Loại tiền, Tỷ giá, file vẫn còn.'))
S3.append(('017', 'Lưu và tiếp tục khi thiếu trường của loại', 'P1',
           'Đang ở màn Tạo; chọn Loại yêu cầu = Khác, chưa chọn Đối tượng, Số tiền trống.',
           '1. Bấm Lưu và tiếp tục.', 'Loại yêu cầu: Khác',
           '- Phiếu vẫn được lưu nháp (Đang tạo) và mở form trống — nháp chỉ bắt buộc Loại yêu cầu.\n'
           '- Lưu ý: Đối tượng, Số tiền, Diễn giải chỉ bị chặn khi Gửi duyệt (TC_03.004).'))
PRE_LIST = 'Tài khoản DNS Admin; danh sách có 2140 phiếu thuộc cả 7 loại yêu cầu.'
PRE_FORM = 'Tài khoản A; KH-A có hợp đồng HĐ-A1; có file bienban.pdf trên máy.'
S1[:] = fill_pre(S1, {}, PRE_LIST)
S2[:] = fill_pre(S2, {'006': 'Có 1 phiếu loại Hạch toán công nợ NCC bảo hành gắn một phiếu xác nhận bảo hành đã xác nhận.'}, PRE_LIST)
S3[:] = fill_pre(S3, {'013': 'Đang ở màn Tạo, loại Khác.'}, PRE_FORM)
S5[:] = fill_pre(S5, {}, 'Phiếu PYCHTBS-002289 Chờ duyệt, loại Điều chỉnh công nợ khách hàng, 1 dòng chi tiết.')
check_no_dash_pre(SECTIONS, ROLE_TCS)

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1', feature_name='Phiếu yêu cầu hạch toán bổ sung - Cập nhật ngày 30/10/2026',
          module_name='YC hạch toán bổ sung', description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
