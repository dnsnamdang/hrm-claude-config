# -*- coding: utf-8 -*-
"""Testcase màn "Phiếu yêu cầu vận chuyển, bốc xếp" — skill testcase-documenter (tc_engine), 30/10/2026.

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
MENU = 'Vào phân hệ Bán hàng > nhóm "Yêu cầu" > "Hàng hóa" > bấm "YC vận chuyển, bốc xếp".'
TAO = '1. ' + MENU + '\n2. Bấm "Tạo mới".'
CHON = ('3. Bấm ô Đơn hàng/Hợp đồng, chọn HĐ_TPE_HN_01.\n'
        '4. Bấm ô Phiếu YCXH, chọn PYCXH-44434.')

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn Phiếu yêu cầu vận chuyển, bốc xếp dùng để người bán hàng đề nghị thủ kho bố trí vận chuyển và bốc xếp cho '
     'một phiếu yêu cầu xuất hàng của một đơn hàng/hợp đồng.\n'
     'Phiếu lưu nháp được (Đang tạo), gửi duyệt sang Chờ duyệt; thủ kho của kho xuất hàng Duyệt hoặc Từ chối (kèm lý do).'),
    ('2. Đối tượng được tính / hiển thị',
     '- Trạng thái: Đang tạo (xám), Chờ duyệt (cam), Đã duyệt (xanh lá), Từ chối (đỏ).\n'
     '- Danh sách: phiếu theo quyền xem theo cấp; không có quyền thì phiếu mình lập.\n'
     '- Luôn thấy thêm phiếu mình đã duyệt / từ chối và phiếu mình là thủ kho của kho xuất hàng.\n'
     '- Popup Chọn phiếu YCXH: phiếu yêu cầu xuất hàng trạng thái 1, 2, 3, 10, 11 và đã gắn khách hàng.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu Đang tạo của người khác: luôn ẩn.\n'
     '- Phiếu YCXH chưa gắn khách hàng: không có trong popup.\n'
     '- Dòng hàng số lượng bằng 0 trên phiếu YCXH: không đưa vào bảng Chi tiết.'),
    ('4. Bộ lọc thời gian áp dụng cho', 'Ô Ngày tạo lọc theo ngày lập phiếu, lấy trọn hai đầu mút.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Phiếu > danh sách dòng hàng chép từ phiếu YCXH (Tên hàng, Model, Mã hàng hóa, ĐVT, Số lượng) + Số kiện người dùng nhập.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Khách hàng, người liên hệ, địa điểm giao, dòng hàng luôn đọc lại từ phiếu YCXH lúc lưu.\n'
     '- Đổi Đơn hàng/Hợp đồng thì xóa phiếu YCXH đã chọn.'),
    ('7. Phân quyền cấp',
     '- Xem tất cả phiếu yêu cầu vận chuyển của tổng công ty.\n'
     '- Xem tất cả phiếu yêu cầu vận chuyển của công ty.\n'
     '- Xem tất cả phiếu yêu cầu vận chuyển của phòng ban.\n'
     '- Xem tất cả phiếu yêu cầu vận chuyển của bộ phận.\n'
     '- Duyệt / Từ chối: thủ kho của kho xuất hàng (không phải quyền, khai ở danh mục Kho), Super admin.\n'
     '- Sửa / Xóa: người lập, phiếu Đang tạo hoặc Từ chối.'),
    ('8. Cách tính các ô thống kê',
     '- Ô "Hiển thị a–b / N": a, b là dòng đầu – cuối của trang, N là tổng phiếu khớp bộ lọc trong phạm vi quyền.'),
    ('9. Ghi chú đọc bảng',
     '- Mã phiếu dạng <mã công ty>.YCVC<tháng năm>.NNNNN.\n'
     '- Lưu ý: kho xuất hàng chưa khai thủ kho thì KHÔNG gửi duyệt được; cần chuẩn bị kho có thủ kho trước khi test.\n'
     '- Lưu ý: duyệt xong thì phiếu YCXH đổi Hình thức vận chuyển thành Công ty vận chuyển; kiểm ở màn Phiếu yêu cầu xuất hàng.\n'
     '- Xuất Excel khi không có dữ liệu: báo "Không có dữ liệu phù hợp." và KHÔNG tải file.'),
]

ROLE_TCS = [
    ('00', 'Không có quyền nào chỉ thấy phiếu mình lập', 'P0',
     'Tài khoản A không có quyền xem theo cấp, không là thủ kho.\nA lập 3 phiếu; công ty có 50 phiếu.',
     '1. Đăng nhập bằng A.\n2. ' + MENU, '—', '- Tổng số = 3.\n- Chỉ phiếu A lập.'),
    ('01', 'Quyền xem của tổng công ty', 'P1', 'Tài khoản C có quyền tổng công ty; 2 công ty có 80 phiếu (không tính nháp người khác).',
     '1. Đăng nhập bằng C.\n2. ' + MENU, '—', '- Tổng số = 80.\n- Khối lọc có Công ty, Phòng ban, Bộ phận.'),
    ('02', 'Quyền xem của công ty', 'P1', 'Tài khoản D thuộc công ty 1 có 50 phiếu.', '1. Đăng nhập bằng D.\n2. ' + MENU, '—',
     '- Tổng số = 50 (trừ nháp của người khác).\n- Không có ô lọc Công ty.'),
    ('03', 'Quyền xem của phòng ban', 'P1', 'Tài khoản E quản lý phòng Kinh doanh (12 phiếu), tự lập 2 phiếu ở phòng khác.',
     '1. Đăng nhập bằng E.\n2. ' + MENU, '—', '- Tổng số = 14.'),
    ('04', 'Quyền xem của bộ phận', 'P1', 'Tài khoản F quản lý bộ phận Bán lẻ (5 phiếu).', '1. Đăng nhập bằng F.\n2. ' + MENU, '—',
     '- Tổng số = 5 + phiếu F tự lập.'),
    ('05', 'Thủ kho thấy phiếu của kho mình', 'P0', 'Tài khoản G là thủ kho Kho Hà Nội, không có quyền xem; có 4 phiếu xuất từ Kho Hà Nội.',
     '1. Đăng nhập bằng G.\n2. ' + MENU, '—', '- Thấy 4 phiếu đó.\n- Phiếu Chờ duyệt có nút Duyệt.'),
    ('06', 'Nháp của người khác luôn ẩn', 'P0', 'Tài khoản C (tổng công ty); B có 1 phiếu Đang tạo.', '1. Đăng nhập bằng C.\n2. Lọc Trạng thái Đang tạo.', '—',
     '- Không thấy phiếu nháp của B.'),
    ('07', 'Không phải thủ kho không duyệt được', 'P0', 'Tài khoản C (tổng công ty, không phải thủ kho, không phải Super admin); phiếu Chờ duyệt TPE.YCVC1026.00004.',
     '1. Đăng nhập bằng C.\n2. Mở chi tiết phiếu.', '—', '- Không có nút Duyệt, Từ chối.\n- Cột Hành động không có nút Duyệt.'),
    ('08', 'Không phải người lập không sửa / xóa được', 'P0', 'Tài khoản C; phiếu Đang tạo của A.', '1. Mở chi tiết phiếu (nếu thấy).', '—',
     '- Không có nút Sửa, Xóa.'),
    ('09', 'Mở chi tiết phiếu ngoài phạm vi', 'P1', 'Tài khoản A; phiếu của người khác ngoài phạm vi.', '1. Mở đường link chi tiết phiếu đó.', '—',
     '- Báo "Bạn không có quyền xem phiếu này".'),
]

S1 = [
    ('001', 'Mở màn từ menu', 'P0', 'Tài khoản DNS Admin.', '1. ' + MENU, '—',
     '- Tiêu đề "Phiếu yêu cầu vận chuyển, bốc xếp".\n- Hiện 10 dòng đầu, mới tạo xếp trên.'),
    ('002', 'Các cột mặc định', 'P1', 'Tài khoản chưa tùy chỉnh cột.', '1. ' + MENU + '\n2. Quan sát tiêu đề cột.', '—',
     '- Hiện 12 cột: STT, Mã phiếu, Số hợp đồng/đơn hàng, Khách hàng, Ngày tạo, Người tạo, Ngày cập nhật, Người cập nhật, '
     'Ngày duyệt, Người duyệt, Trạng thái, Hành động.\n- Cột Phiếu YCXH ẩn.'),
    ('003', 'Màu trạng thái', 'P2', 'Có phiếu ở đủ 4 trạng thái.', '1. ' + MENU + '\n2. Quan sát cột Trạng thái.', '—',
     '- Đang tạo xám, Chờ duyệt cam, Đã duyệt xanh lá, Từ chối đỏ.'),
    ('004', 'Bấm Mã phiếu', 'P0', '—', '1. Bấm mã TPE.YCVC1026.00004.', '—',
     '- Mở màn "Chi tiết phiếu yêu cầu vận chuyển, bốc xếp: TPE.YCVC1026.00004", tiêu đề có nhãn trạng thái.'),
    ('005', 'Bấm Số hợp đồng/đơn hàng', 'P1', 'Phiếu gắn 1 hợp đồng trên HRM và 1 phiếu gắn hợp đồng ERP.',
     '1. Bấm số hợp đồng ở 2 dòng.', '—', '- Mở chứng từ ở tab mới (HRM hoặc ERP tương ứng).'),
    ('006', 'Nút trên dòng theo trạng thái', 'P0', 'A là người lập phiếu 00006 (Đang tạo), 00001 (Từ chối), 00003 (Đã duyệt).',
     '1. Đăng nhập bằng A.\n2. Quan sát cột Hành động 3 dòng.', '—',
     '- 00006, 00001: có Sửa, Xóa, Lịch sử.\n- 00003: chỉ có Lịch sử.'),
]

S2 = [
    ('001', 'Tìm nhanh theo mã phiếu', 'P0', 'Có phiếu TPE.YCVC1026.00004.', '1. Nhập "00004".\n2. Bấm Tìm kiếm.', 'Ô tìm nhanh: 00004',
     '- Chỉ còn phiếu 00004.'),
    ('002', 'Tìm nhanh theo số hợp đồng', 'P1', 'Phiếu 00003 gắn HĐ_TPE_HN_KD2_26_0412.', '1. Nhập "KD2_26_0412", bấm Tìm kiếm.',
     'Ô tìm nhanh: KD2_26_0412', '- Ra phiếu 00003.'),
    ('003', 'Tìm nhanh theo mã phiếu YCXH', 'P1', 'Phiếu 00004 gắn PYCXH-44434.', '1. Nhập "44434", bấm Tìm kiếm.',
     'Ô tìm nhanh: 44434', '- Ra phiếu 00004.'),
    ('004', 'Lọc Trạng thái', 'P0', '2 phiếu Từ chối.', '1. Tìm kiếm nâng cao.\n2. Chọn Trạng thái = Từ chối.', 'Trạng thái: Từ chối',
     '- Nạp lại ngay, còn 2 phiếu.'),
    ('005', 'Lọc Khách hàng', 'P1', 'Khách hàng "Công ty Cổ phần Thiết bị Công nghiệp Kinoko" có 1 phiếu.',
     '1. Gõ "Kinoko" vào ô Khách hàng, chọn.', 'Khách hàng: Kinoko', '- Còn 1 phiếu.'),
    ('006', 'Lọc Hợp đồng', 'P1', '—', '1. Nhập Hợp đồng = "KD2".', 'Hợp đồng: KD2', '- Chỉ phiếu có số hợp đồng chứa "KD2".'),
    ('007', 'Lọc Người tạo', 'P2', '—', '1. Chọn Người tạo = DNS Admin.', '—', '- Chỉ phiếu DNS Admin lập.'),
    ('008', 'Lọc Ngày tạo', 'P0', '3 phiếu tạo ngày 21/10/2026.', '1. Chọn Ngày tạo 21/10/2026 đến 21/10/2026.', '—',
     '- Đúng 3 phiếu.'),
    ('009', 'Công ty – Phòng ban – Bộ phận phụ thuộc', 'P2', 'Tài khoản tổng công ty.',
     '1. Chọn Công ty 1, Phòng ban Kinh doanh.\n2. Đổi Công ty.', '—', '- Phòng ban, Bộ phận bị xóa.'),
    ('010', 'Làm mới', 'P1', 'Đang lọc Trạng thái và Khách hàng.', '1. Bấm Làm mới.', '—', '- Mọi ô lọc trống, nạp lại trang 1.'),
    ('011', 'Cài đặt bộ lọc', 'P2', '—', '1. Cài đặt bộ lọc.\n2. Bỏ tích Người tạo, Lưu.', '—',
     '- Ô Người tạo không còn.\n- Khôi phục mặc định đưa về đủ 6 ô.'),
]

S3 = [
    ('001', 'Sắp xếp', 'P1', '—', '1. Bấm tiêu đề Mã phiếu, Khách hàng, Ngày duyệt.', '—',
     '- Sắp xếp đúng tăng / giảm, về trang 1.\n- Cột Người tạo, Trạng thái không sắp xếp được.'),
    ('002', 'Phân trang', 'P1', '25 phiếu.', '1. Chọn 20 dòng / trang.\n2. Bấm trang 2.', '—', '- "Hiển thị 21–25 / 25".'),
    ('003', 'Tùy chỉnh cột', 'P1', '—', '1. Cấu hình cột hiển thị.\n2. Tích Phiếu YCXH, Lưu.', '—',
     '- Cột Phiếu YCXH hiện, mã là link mở tab mới.\n- STT, Mã phiếu, Hành động có ổ khóa.'),
]

S4 = [
    ('001', 'Mở màn Tạo mới', 'P0', '—', TAO, '—',
     '- Tiêu đề "Tạo phiếu yêu cầu vận chuyển, bốc xếp".\n- Góc phải ghi tên và thời điểm hiện tại.\n- Bảng Chi tiết "Không có dữ liệu".'),
    ('002', 'Bấm Gửi duyệt khi trống', 'P0', '—', TAO + '\n3. Bấm Gửi duyệt.', '—',
     '- Thông báo "Vui lòng kiểm tra lại thông tin đã nhập".\n- Dưới Đơn hàng/Hợp đồng và Phiếu YCXH: "Bắt buộc phải nhập".'),
    ('003', 'Chọn YCXH khi chưa chọn hợp đồng', 'P1', '—', TAO + '\n3. Bấm ô Phiếu YCXH.', '—',
     '- Báo "Vui lòng chọn đơn hàng/hợp đồng trước.", không mở cửa sổ.'),
    ('004', 'Popup Chọn đơn hàng/hợp đồng', 'P0', '—', TAO + '\n3. Bấm ô Đơn hàng/Hợp đồng.', '—',
     '- Cửa sổ "Chọn đơn hàng/hợp đồng": cột STT, Số đơn hàng/Hợp đồng, Loại hợp đồng, Ngày tạo.\n- Có ô Loại hợp đồng mặc định Tất cả.'),
    ('005', 'Lọc Loại hợp đồng trong popup', 'P1', '—', '1. Chọn Loại hợp đồng = Hợp đồng mua dịch vụ.', '—',
     '- Chỉ còn hợp đồng mua dịch vụ.'),
    ('006', 'Bấm số hợp đồng trong popup', 'P2', '—', '1. Bấm số hợp đồng (chữ xanh) ở 1 dòng.', '—',
     '- Mở chứng từ ở tab mới, KHÔNG chọn dòng.'),
    ('007', 'Chọn hợp đồng', 'P0', '—', TAO + '\n3. Bấm ô Đơn hàng/Hợp đồng, bấm dòng HĐ_TPE_HN_01.', '—',
     '- Ô Đơn hàng/Hợp đồng ghi HĐ_TPE_HN_01, cửa sổ đóng.'),
    ('008', 'Popup Chọn phiếu YCXH chỉ có phiếu hợp lệ', 'P0', 'PYCXH-410 chưa gắn khách hàng.',
     '1. Sau TC_04.007, bấm ô Phiếu YCXH.\n2. Tìm "410".', '—', '- Không có PYCXH-410.'),
    ('009', 'Chọn phiếu YCXH điền dữ liệu', 'P0', 'PYCXH-44434 có 6 dòng hàng, 1 dòng số lượng 0.', TAO + '\n' + CHON, '—',
     '- Khách hàng, Người liên hệ, Số ĐT, Địa điểm giao hàng tự điền.\n- Bảng Chi tiết có 5 dòng (bỏ dòng số lượng 0).'),
    ('010', 'Đổi hợp đồng xóa YCXH', 'P1', 'Đã làm TC_04.009.', '1. Chọn lại hợp đồng khác.', '—',
     '- Phiếu YCXH, thông tin giao hàng, bảng Chi tiết bị xóa.'),
    ('011', 'Số kiện không phải số nguyên', 'P1', 'Đã làm TC_04.009.', '1. Nhập Số kiện dòng 1 = 1.5.\n2. Lưu nháp.', 'Số kiện: 1.5',
     '- Báo "Vui lòng nhập số nguyên." hoặc ô không nhận dấu chấm.'),
    ('012', 'Tổng số kiện chặn chữ', 'P2', '—', '1. Gõ "abc" vào Tổng số kiện.', 'Tổng số kiện: abc', '- Ô không nhận chữ.'),
    ('013', 'Phương thức / Địa điểm bốc xếp quá 255 ký tự', 'P2', '—', '1. Dán 300 ký tự vào Phương thức bốc xếp.', '—',
     '- Ô chỉ nhận 255 ký tự.'),
    ('014', 'Đính kèm sai định dạng / quá dung lượng', 'P1', '—', '1. Thêm tài liệu file .docx.\n2. Thêm file PDF 25 MB.', '—',
     '- Báo "Định dạng file không hợp lệ" / "File quá lớn".\n- File PDF dưới 20 MB nhận bình thường.'),
    ('015', 'Lưu nháp thành công', 'P0', 'Đã làm TC_04.009.', '1. Nhập Số kiện 2 dòng = 1.\n2. Bấm Lưu nháp.', '—',
     '- Báo "Thêm mới thành công.", về danh sách.\n- Phiếu mới mã TPE.YCVC<tháng năm>.NNNNN, trạng thái Đang tạo.\n- Lịch sử có mốc Tạo mới.'),
    ('016', 'Gửi duyệt thành công', 'P0', 'Kho xuất của PYCXH-44434 có thủ kho G.', TAO + '\n' + CHON + '\n5. Bấm Gửi duyệt.', '—',
     '- Báo "Gửi duyệt thành công.", phiếu Chờ duyệt.\n- G nhận thông báo "[YCVC] Chờ duyệt".'),
    ('017', 'Gửi duyệt khi kho chưa có thủ kho', 'P0', 'Phiếu YCXH xuất từ kho chưa khai thủ kho.', TAO + '\n3. Chọn hợp đồng và phiếu YCXH đó.\n4. Gửi duyệt.', '—',
     '- Báo "Kho xuất hàng chưa có thủ kho, chưa gửi duyệt được." dưới ô Phiếu YCXH.\n- Không lưu.'),
    ('018', 'Lưu và tiếp tục', 'P1', '—', TAO + '\n' + CHON + '\n5. Bấm Lưu và tiếp tục.', '—',
     '- Phiếu lưu Đang tạo.\n- Ở lại màn Tạo với form trống.'),
    ('019', 'Rời màn khi chưa lưu', 'P1', 'Đã chọn hợp đồng.', '1. Bấm Quay lại.', '—', '- Hỏi xác nhận rời trang.'),
]

S5 = [
    ('001', 'Mở màn Sửa', 'P0', 'A lập phiếu 00006 Đang tạo.', '1. Bấm biểu tượng Sửa ở dòng 00006.', '—',
     '- Tiêu đề "Sửa phiếu yêu cầu vận chuyển, bốc xếp: TPE.YCVC1026.00006", dữ liệu đúng như đã lưu.'),
    ('002', 'Sửa và lưu nháp', 'P0', 'Như TC_05.001.', '1. Đổi Ghi chú, Số kiện dòng 1 = 3.\n2. Lưu nháp.', 'Ghi chú: Giao buổi sáng',
     '- Báo "Cập nhật thành công.".\n- Lịch sử có mốc Thay đổi thông tin ghi Ghi chú cũ sang mới và số kiện.'),
    ('003', 'Sửa phiếu Từ chối rồi gửi lại', 'P0', 'Phiếu 00001 Từ chối, lý do "Sai địa điểm".', '1. Sửa, Gửi duyệt.', '—',
     '- Báo "Gửi duyệt thành công.", phiếu Chờ duyệt.\n- Lý do từ chối cũ bị xóa.\n- Lịch sử: mốc Thay đổi trạng thái riêng.'),
    ('004', 'Sửa khi phiếu đã bị đổi trạng thái', 'P1',
     'A mở màn Sửa phiếu 00006 ở tab 1.\nỞ tab 2, A mở Sửa cùng phiếu và bấm Gửi duyệt (phiếu sang Chờ duyệt).',
     '1. Quay lại tab 1, bấm Lưu nháp.', '—', '- Báo "Trạng thái đã bị thay đổi. Vui lòng load lại trang", chuyển sang màn chi tiết.'),
    ('005', 'Xóa phiếu', 'P0', 'A lập phiếu 00005 Đang tạo.', '1. Bấm biểu tượng Xóa ở dòng.\n2. Bấm Xóa.', '—',
     '- Hộp "Xác nhận xóa": "Bạn có chắc muốn xóa phiếu yêu cầu vận chuyển \'TPE.YCVC1026.00005\'?".\n'
     '- Báo "Xóa thành công.", phiếu biến mất.'),
    ('006', 'Hủy xóa', 'P2', '—', '1. Bấm Xóa, rồi bấm Hủy.', '—', '- Phiếu còn nguyên.'),
]

S6 = [
    ('001', 'Nội dung màn chi tiết', 'P0', 'Phiếu 00004 Chờ duyệt.', '1. Mở chi tiết.', '—',
     '- Mọi ô chỉ đọc.\n- Đơn hàng/Hợp đồng và Phiếu YCXH là link mở tab mới.\n- Có khối Lịch sử thu gọn.'),
    ('002', 'Phiếu Từ chối hiện lý do', 'P1', 'Phiếu 00001 Từ chối.', '1. Mở chi tiết.', '—',
     '- Có Người duyệt, Ngày duyệt, Lý do từ chối.'),
    ('003', 'Duyệt phiếu', 'P0', 'G là thủ kho; phiếu 00004 Chờ duyệt gắn PYCXH-44434.', '1. Đăng nhập G.\n2. Mở chi tiết.\n3. Bấm Duyệt, bấm Duyệt ở hộp xác nhận.', '—',
     '- Hộp "Xác nhận duyệt": "Bạn có chắc muốn duyệt phiếu yêu cầu vận chuyển \'TPE.YCVC1026.00004\'?".\n'
     '- Báo "Duyệt thành công.", phiếu Đã duyệt, có Người duyệt / Ngày duyệt.\n'
     '- Người lập nhận "[YCVC] Đã duyệt".\n- Mở PYCXH-44434: Hình thức vận chuyển = Công ty vận chuyển.'),
    ('004', 'Nút Duyệt trên dòng', 'P1', 'G; phiếu Chờ duyệt.', '1. Bấm biểu tượng Duyệt ở cột Hành động.', '—', '- Mở màn chi tiết phiếu.'),
    ('005', 'Từ chối thiếu lý do', 'P0', 'G; phiếu Chờ duyệt.', '1. Bấm Từ chối.\n2. Để trống, bấm Từ chối.', '—',
     '- Viền đỏ, "Bắt buộc phải nhập", cửa sổ không đóng.'),
    ('006', 'Từ chối thành công', 'P0', 'Như TC_06.005.', '1. Nhập lý do, bấm Từ chối.', 'Lý do: Sai địa điểm',
     '- Báo "Từ chối thành công.", phiếu Từ chối.\n- Người lập nhận "[YCVC] Từ chối" kèm lý do.\n- Lịch sử có mốc Thay đổi trạng thái kèm lý do.'),
    ('007', 'Hai thủ kho cùng xử lý', 'P1', 'G và G2 cùng là thủ kho, cùng mở phiếu Chờ duyệt.', '1. G duyệt.\n2. G2 bấm Từ chối, nhập lý do, xác nhận.', '—',
     '- G2 nhận "Trạng thái đã bị thay đổi. Vui lòng load lại trang".'),
]

S7 = [
    ('001', 'Xuất Excel theo trường đã chọn', 'P0', 'Lọc Trạng thái = Đã duyệt.',
     '1. Bấm Xuất Excel.\n2. Bỏ chọn hết, tích Mã phiếu, Khách hàng, Trạng thái.\n3. Xuất file.', '—',
     '- Tải file "DANH SÁCH PHIẾU YÊU CẦU VẬN CHUYỂN, BỐC XẾP" có logo, đúng 3 cột theo thứ tự đã tích.\n- Báo "Xuất Excel thành công.".'),
    ('002', 'Xuất khi không có dữ liệu', 'P2', 'Bộ lọc không có kết quả.', '1. Xuất Excel, Xuất file.', '—',
     '- Báo "Không có dữ liệu phù hợp.", không tải file.'),
    ('003', 'Xuất trong phạm vi quyền', 'P0', 'Tài khoản A (không quyền), 3 phiếu.', '1. Xuất đủ 10 trường.', '—', '- File chỉ có 3 phiếu của A.'),
    ('004', 'Lịch sử từ danh sách', 'P1', 'Phiếu 00003 có 8 mốc.', '1. Bấm biểu tượng Lịch sử ở dòng 00003.', '—',
     '- Cửa sổ "Lịch sử thay đổi: TPE.YCVC1026.00003", mốc mới nhất trên.\n- Mốc Thay đổi trạng thái ghi trạng thái cũ sang mới.'),
    ('005', 'Lịch sử từ màn chi tiết', 'P2', '—', '1. Mở chi tiết 00003, bấm Xem lịch sử.', '—', '- Nội dung giống TC_07.004.'),
]

S8 = [
    ('001', 'Luồng lập, gửi, duyệt', 'P0', 'A người lập; G thủ kho kho xuất của PYCXH-44434.',
     '1. A lập phiếu, Gửi duyệt.\n2. G duyệt.\n3. A mở lại phiếu.', '—',
     '- Bước 1: G nhận thông báo.\n- Bước 3: phiếu Đã duyệt; A nhận thông báo; không còn nút Sửa / Xóa.'),
    ('002', 'Luồng từ chối, sửa, gửi lại, duyệt', 'P0', 'Như TC_08.001.',
     '1. A gửi duyệt.\n2. G từ chối.\n3. A sửa, gửi lại.\n4. G duyệt.', '—',
     '- Lịch sử đủ các mốc theo đúng thứ tự.\n- Phiếu cuối cùng Đã duyệt, lý do cũ không còn.'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP PHIẾU (TẠO MỚI)', S4),
    ('V', 'CHỈNH SỬA & XÓA', S5),
    ('VI', 'XEM CHI TIẾT, DUYỆT & TỪ CHỐI', S6),
    ('VII', 'XUẤT EXCEL & LỊCH SỬ', S7),
    ('VIII', 'E2E FLOW', S8),
]

# ---------------------------------------------------------------- bổ sung theo chuẩn (30/10/2026)
# Mẫu Danh mục quốc gia + 8 ý góp ý tester 07/10/2026 (../phieu-theo-form-quoc-gia/tc_phieu_bosung.py).
# Màn chỉ có 1 lối vào, không có tham số chế độ trên thanh địa chỉ → không có case "tham số lạ".
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from tc_phieu_bosung import (ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases,  # noqa: E402
                             add_advanced_step, fill_pre, check_no_dash_pre)

SCREEN = ListScreen(menu=MENU, title='Phiếu yêu cầu vận chuyển, bốc xếp', total=25,
                    quick_label='mã phiếu, số hợp đồng, mã phiếu YCXH', quick_sample='YCVC1026',
                    quick_hit='6 phiếu TPE.YCVC1026.00001 đến 00006',
                    filters=[('Trạng thái', 'Đang tạo'), ('Người tạo', 'DNS Admin')],
                    org_levels=('Công ty', 'Phòng ban', 'Bộ phận'))
S1[0] = open_menu_case(SCREEN, pre='Tài khoản DNS Admin; trong phạm vi xem có 25 phiếu.')
ORG = org_cases(SCREEN, 12)
MEM = filter_memory_cases(SCREEN, 14)
S2[8] = ('009',) + ORG[2][1:]
S2[:] = add_advanced_step(S2, {'005', '006', '007', '008'}, MENU) + ORG[:2] + MEM + combo_cases(SCREEN, 19)
S4.append(('020', 'Lưu và tiếp tục khi dữ liệu lỗi', 'P0',
           'Đang ở màn Tạo; đã nhập Ghi chú "Giao buổi sáng", Tổng số kiện 3; chưa chọn Đơn hàng/Hợp đồng và Phiếu YCXH.',
           TAO + '\n3. Nhập Ghi chú, Tổng số kiện.\n4. Bấm Lưu và tiếp tục.', 'Ghi chú: Giao buổi sáng\nTổng số kiện: 3',
           '- Thông báo "Vui lòng kiểm tra lại thông tin đã nhập".\n- Chữ đỏ "Bắt buộc phải nhập" dưới Đơn hàng/Hợp đồng và Phiếu YCXH.\n'
           '- KHÔNG lưu phiếu, KHÔNG mở form mới; Ghi chú, Tổng số kiện vẫn còn.'))
S4.append(('021', 'Lưu và tiếp tục khi Số kiện sai định dạng', 'P1',
           'Đã chọn HĐ_TPE_HN_01 và PYCXH-44434 (5 dòng hàng).',
           '1. Nhập Số kiện dòng 1 = 1.5.\n2. Bấm Lưu và tiếp tục.', 'Số kiện dòng 1: 1.5',
           '- Báo "Vui lòng nhập số nguyên." dưới ô Số kiện dòng 1 (hoặc ô không nhận dấu chấm).\n- KHÔNG lưu; dữ liệu đã nhập vẫn còn.'))
PRE_LIST = 'Tài khoản DNS Admin; danh sách có 25 phiếu ở đủ 4 trạng thái.'
PRE_FORM = 'Tài khoản A có quyền lập phiếu; có HĐ_TPE_HN_01 còn hiệu lực và phiếu PYCXH-44434 gắn khách hàng.'
S1[:] = fill_pre(S1, {}, PRE_LIST)
S2[:] = fill_pre(S2, {}, PRE_LIST)
S3[:] = fill_pre(S3, {}, PRE_LIST)
S4[:] = fill_pre(S4, {
    '012': 'Đang ở màn Tạo.', '013': 'Đang ở màn Tạo; có sẵn đoạn văn 300 ký tự.',
    '014': 'Đang ở màn Tạo; có file baocao.docx và file PDF 25 MB trên máy.',
}, PRE_FORM)
S5[:] = fill_pre(S5, {'006': 'A lập phiếu 00005 Đang tạo.'})
S7[:] = fill_pre(S7, {'005': 'Phiếu TPE.YCVC1026.00003 có 8 mốc lịch sử.'})
check_no_dash_pre(SECTIONS, ROLE_TCS)

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1', feature_name='Phiếu yêu cầu vận chuyển, bốc xếp - Cập nhật ngày 30/10/2026',
          module_name='YC vận chuyển, bốc xếp', description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
