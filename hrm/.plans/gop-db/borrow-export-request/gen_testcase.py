# -*- coding: utf-8 -*-
"""Testcase màn "Yêu cầu xuất hàng mượn" (PYCXHM) — skill testcase-documenter (tc_engine), 30/10/2026.

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
MENU_SALE = 'Vào phân hệ Bán hàng > nhóm "Yêu cầu" > "Hàng hóa" > bấm "YC xuất hàng mượn".'
MENU_KT = ('Vào phân hệ Tài chính > nhóm "Hàng hoá - Dịch vụ - Vận chuyển" > "Mượn hàng" > bấm '
           '"Yêu cầu xuất hàng mượn".')
TAO = '1. ' + MENU_SALE + '\n2. Bấm "Tạo mới".'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn Yêu cầu xuất hàng mượn (mã phiếu PYCXHM) dùng để người đang mượn hàng gom các phiếu xuất mượn của '
     'mình vào 1 phiếu, chọn phần hàng KHÔNG trả lại mà xuất hẳn, gửi Kế toán kho duyệt.\n'
     'Phiếu gửi đi vào thẳng trạng thái Chờ duyệt (không có nháp, không Sửa, không Xóa).\n'
     'Kế toán kho duyệt bằng cách lập Phiếu xuất hàng mượn từ phiếu này, hoặc Từ chối kèm lý do.'),
    ('2. Đối tượng được tính / hiển thị',
     '- Trạng thái hiển thị: Chờ duyệt (nhãn cam), Đã duyệt (nhãn xanh lá), Không duyệt (nhãn đỏ).\n'
     '- Lối vào Bán hàng: phiếu trong phạm vi quyền xem theo cấp, cộng phiếu mình lập; Kế toán kho thấy mọi '
     'phiếu đã gửi.\n'
     '- Lối vào Tài chính (Kế toán kho): mọi phiếu đã gửi, chỉ người có quyền Kế toán kho thấy dữ liệu.\n'
     '- Popup Chọn phiếu xuất mượn: chỉ phiếu yêu cầu xuất hàng loại Xuất mượn do chính mình lập, đang Đã mượn.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu trạng thái Đang tạo (dữ liệu cũ) của người khác: không bao giờ hiện.\n'
     '- Ô lọc Trạng thái không có lựa chọn Đang tạo.\n'
     '- Hàng hóa không có trên phiếu mượn nào đã chọn: dòng bị khóa, không được gửi đi.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô Ngày tạo lọc theo ngày lập phiếu, lấy trọn 2 đầu mút (từ 00:00 ngày đầu tới hết ngày cuối).'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Phiếu > dòng hàng hóa > dòng con theo từng phiếu mượn có hàng đó (cột Phiếu mượn, Đang mượn, Xuất).\n'
     'Số lượng xuất của dòng hàng = tổng Xuất các dòng con.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Mỗi phiếu mượn chỉ chọn được 1 lần trong cùng phiếu.\n'
     '- Cùng 1 hàng hóa chỉ thêm 1 dòng (popup chọn hàng báo trùng).\n'
     '- Đang mượn = đã xuất - đã trả - phần đang chờ ở các phiếu khác chưa duyệt (trả hàng, xuất bán hàng mượn, '
     'xuất hàng mượn), quy theo hệ số đơn vị tính, làm tròn xuống.'),
    ('7. Phân quyền cấp',
     '- Kế toán kho: duyệt (Tạo phiếu xuất hàng mượn), Từ chối, xem mọi phiếu đã gửi.\n'
     '- Xem phiếu hàng mượn theo tổng công ty: mọi phiếu.\n'
     '- Xem phiếu hàng mượn theo công ty: phiếu cùng công ty + phiếu mình lập.\n'
     '- Xem phiếu hàng mượn theo phòng ban: phiếu phòng ban mình quản lý + phiếu mình lập.\n'
     '- Không có quyền nào: chỉ phiếu mình lập. Lập phiếu không cần quyền riêng.'),
    ('8. Cách tính các ô thống kê',
     '- Ô "Hiển thị a–b / N": a, b là dòng đầu – cuối của trang, N là tổng phiếu khớp bộ lọc trong phạm vi quyền.\n'
     '- Thành tiền = Số lượng xuất × Đơn giá (theo đơn vị tính đang chọn).\n'
     '- Dòng Tổng cộng = tổng Số lượng xuất và tổng Thành tiền của các dòng.'),
    ('9. Ghi chú đọc bảng',
     '- Số hiển thị dạng 1,234,567 (dấu phẩy ngăn hàng nghìn).\n'
     '- Lưu ý: ô Xuất chỉ nhận số nguyên; vượt Đang mượn thì báo đỏ, KHÔNG tự kéo số về (trừ khi đổi đơn vị tính).\n'
     '- Lưu ý: phiếu gửi đi là không sửa được; muốn đổi phải chờ Từ chối rồi lập phiếu mới.\n'
     '- Lưu ý: tài khoản kiểm thử cần có sẵn phiếu xuất mượn Đã mượn do chính mình lập thì mới lập phiếu được.'),
]

ROLE_TCS = [
    ('00', 'Tài khoản không có quyền nào chỉ thấy phiếu mình lập', 'P0',
     'Tài khoản A không có quyền Kế toán kho và không có quyền xem theo cấp.\nA đã lập 3 phiếu; công ty có 300 phiếu.',
     '1. Đăng nhập bằng A.\n2. ' + MENU_SALE, '—',
     '- Màn mở được, không báo lỗi quyền.\n- Tổng số = 3, chỉ phiếu A lập.\n- Không thấy nút Duyệt trên dòng.'),
    ('01', 'Quyền Kế toán kho thấy mọi phiếu đã gửi', 'P0',
     'Tài khoản B có quyền Kế toán kho; hệ thống có 300 phiếu đã gửi ở 2 công ty.',
     '1. Đăng nhập bằng B.\n2. ' + MENU_KT, '—',
     '- Tiêu đề "Yêu cầu xuất hàng mượn (Kế toán kho)".\n- Tổng số = 300.\n- Phiếu Chờ duyệt có nút Duyệt ở cột Hành động.'),
    ('02', 'Không có quyền Kế toán kho mở lối vào Kế toán kho', 'P0',
     'Tài khoản A như TC-ROLE-00.', '1. Đăng nhập bằng A.\n2. ' + MENU_KT, '—',
     '- Bảng hiện "Không có dữ liệu phù hợp.".\n- Không lộ phiếu của người khác.'),
    ('03', 'Quyền Xem phiếu hàng mượn theo tổng công ty', 'P1',
     'Tài khoản C có quyền theo tổng công ty; công ty 1 có 200 phiếu, công ty 2 có 100 phiếu.',
     '1. Đăng nhập bằng C.\n2. ' + MENU_SALE, '—',
     '- Tổng số = 300.\n- Bộ lọc nâng cao có ô Công ty và Phòng ban.'),
    ('04', 'Quyền Xem phiếu hàng mượn theo công ty', 'P1',
     'Tài khoản D thuộc công ty 1, có quyền theo công ty; D lập 2 phiếu ở công ty 2 (điều chuyển).',
     '1. Đăng nhập bằng D.\n2. ' + MENU_SALE, '—',
     '- Tổng số = 200 phiếu công ty 1 + 2 phiếu D lập.\n- Bộ lọc không có ô Công ty, có ô Phòng ban.'),
    ('05', 'Quyền Xem phiếu hàng mượn theo phòng ban', 'P1',
     'Tài khoản E quản lý phòng Kinh doanh (40 phiếu).', '1. Đăng nhập bằng E.\n2. ' + MENU_SALE, '—',
     '- Tổng số = 40 + phiếu E tự lập.\n- Mở chi tiết 1 phiếu của phòng Kinh doanh được.'),
    ('06', 'Mở chi tiết phiếu ngoài phạm vi', 'P0',
     'Tài khoản A như TC-ROLE-00; phiếu PYCXHM-00300 của người khác, khác phòng ban.',
     '1. Đăng nhập bằng A.\n2. Mở thông báo / đường link chi tiết phiếu PYCXHM-00300 do người khác gửi.', '—',
     '- Hệ thống báo "Bạn không có quyền xem phiếu này".\n- Quay về màn danh sách, không hiện nội dung phiếu.'),
    ('07', 'Người không có quyền Kế toán kho không thấy nút duyệt / từ chối', 'P0',
     'Tài khoản A lập phiếu PYCXHM-00301 đang Chờ duyệt.', '1. Đăng nhập bằng A.\n2. Mở chi tiết PYCXHM-00301.', '—',
     '- Chỉ có nút In, Quay lại.\n- KHÔNG có nút Tạo phiếu xuất hàng mượn và Từ chối.'),
    ('08', 'Kế toán kho với phiếu đã xử lý', 'P1',
     'Tài khoản B (Kế toán kho); phiếu PYCXHM-00290 Đã duyệt, PYCXHM-00291 Không duyệt.',
     '1. Đăng nhập bằng B.\n2. Mở chi tiết lần lượt 2 phiếu.', '—',
     '- Cả 2 phiếu không có nút Tạo phiếu xuất hàng mượn và Từ chối.'),
]

S1 = [
    ('001', 'Mở màn từ phân hệ Bán hàng', 'P0', 'Tài khoản D (theo công ty), công ty có 200 phiếu.',
     '1. Đăng nhập bằng D.\n2. ' + MENU_SALE, '—',
     '- Tiêu đề bảng "Yêu cầu xuất hàng mượn".\n- Hiện 10 dòng đầu, mới tạo xếp trên.\n- Dòng "Hiển thị 1–10 / 202".'),
    ('002', 'Mở màn từ phân hệ Tài chính', 'P0', 'Tài khoản B (Kế toán kho).', '1. ' + MENU_KT + '\n2. Quan sát danh sách.', '—',
     '- Tiêu đề "Yêu cầu xuất hàng mượn (Kế toán kho)".\n- Có đủ các phiếu Chờ duyệt, Đã duyệt, Không duyệt.'),
    ('003', 'Chuyển qua lại giữa 2 lối vào', 'P1', 'Tài khoản B.',
     '1. ' + MENU_SALE + '\n2. Đổi lọc Trạng thái = Đã duyệt.\n3. ' + MENU_KT, '—',
     '- Bước 3: tiêu đề đổi sang bản Kế toán kho, danh sách nạp lại từ trang 1.'),
    ('004', 'Các cột mặc định của bảng', 'P1', 'Tài khoản chưa từng tùy chỉnh cột.', '1. ' + MENU_SALE, '—',
     '- Hiện: STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, Hành động.\n'
     '- Ẩn: Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối.'),
    ('005', 'Định dạng cột', 'P1', 'Có phiếu PYCXHM-00301 của Nguyễn Văn A phòng MT_KD, tạo 21/10/2026 07:47.',
     '1. ' + MENU_SALE + '\n2. Quan sát dòng PYCXHM-00301.', '—',
     '- Người tạo: "Nguyễn Văn A - MT_KD".\n- Ngày tạo: "21/10/2026 07:47".\n- Mã phiếu là liên kết gạch chân.'),
    ('006', 'Màu nhãn trạng thái', 'P2', 'Có phiếu ở đủ 3 trạng thái.', '1. ' + MENU_KT + '\n2. Quan sát cột Trạng thái.', '—',
     '- Chờ duyệt: cam.\n- Đã duyệt: xanh lá.\n- Không duyệt: đỏ.'),
    ('007', 'Bấm mã phiếu mở chi tiết', 'P0', 'Có phiếu PYCXHM-00301.', '1. ' + MENU_SALE + '\n2. Bấm mã PYCXHM-00301.', '—',
     '- Mở màn "Chi tiết yêu cầu xuất hàng mượn: PYCXHM-00301".'),
    ('008', 'Trạng thái rỗng', 'P2', 'Tài khoản mới chưa lập phiếu nào, không có quyền.', '1. ' + MENU_SALE, '—',
     '- Bảng hiện "Không có dữ liệu phù hợp.".'),
]

S2 = [
    ('001', 'Tìm nhanh theo mã phiếu', 'P0', 'Có phiếu PYCXHM-00301.',
     '1. ' + MENU_SALE + '\n2. Nhập "00301" vào ô tìm nhanh.\n3. Bấm Tìm kiếm.', 'Ô tìm nhanh: 00301',
     '- Chỉ còn PYCXHM-00301.\n- Tổng số = 1.'),
    ('002', 'Ô tìm nhanh chỉ chạy khi bấm Tìm kiếm', 'P1', '—',
     '1. ' + MENU_SALE + '\n2. Nhập "00301", KHÔNG bấm Tìm kiếm.', 'Ô tìm nhanh: 00301',
     '- Danh sách chưa đổi cho tới khi bấm Tìm kiếm.'),
    ('003', 'Ô tìm nhanh không tìm theo tên người tạo', 'P1', 'Người tạo Nguyễn Văn A có phiếu.',
     '1. Nhập "Nguyễn Văn A" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.', 'Ô tìm nhanh: Nguyễn Văn A',
     '- Không có kết quả (ô chỉ tìm theo mã phiếu).'),
    ('004', 'Lọc theo Trạng thái', 'P0', 'Có 5 phiếu Chờ duyệt.',
     '1. Bấm Tìm kiếm nâng cao.\n2. Chọn Trạng thái = Chờ duyệt.', 'Trạng thái: Chờ duyệt',
     '- Danh sách nạp lại ngay, chỉ còn 5 phiếu Chờ duyệt.\n- Ô Trạng thái chỉ có 3 lựa chọn: Chờ duyệt, Đã duyệt, Không duyệt.'),
    ('005', 'Lọc theo Người tạo / Người duyệt', 'P1', 'Kế toán kho Cao Thị Thùy Linh đã duyệt 20 phiếu.',
     '1. Mở Tìm kiếm nâng cao.\n2. Chọn Người duyệt = Cao Thị Thùy Linh.', 'Người duyệt: Cao Thị Thùy Linh',
     '- Chỉ còn 20 phiếu, cột Người duyệt đều là Cao Thị Thùy Linh.'),
    ('006', 'Lọc theo Mã hàng hóa / Tên hàng hóa', 'P1', 'Có 2 phiếu chứa hàng mã ENEO-408-V5041.',
     '1. Nhập Mã hàng hóa = ENEO-408.', 'Mã hàng hóa: ENEO-408',
     '- Chỉ còn các phiếu có dòng hàng mã chứa "ENEO-408".'),
    ('007', 'Lọc theo khoảng Ngày tạo', 'P0', 'Có 4 phiếu tạo từ 01/10/2026 tới 05/10/2026.',
     '1. Chọn Ngày tạo từ 01/10/2026 đến 05/10/2026.', 'Ngày tạo: 01/10/2026 đến 05/10/2026',
     '- Đúng 4 phiếu, kể cả phiếu tạo lúc 23:59 ngày 05/10/2026.'),
    ('008', 'Lọc Công ty – Phòng ban phụ thuộc nhau', 'P1', 'Tài khoản C (tổng công ty).',
     '1. Chọn Công ty 1, Phòng ban Kinh doanh.\n2. Đổi Công ty sang Công ty 2.', '—',
     '- Bước 2: ô Phòng ban bị xóa, danh sách phòng ban đổi theo Công ty 2.'),
    ('009', 'Bấm Làm mới', 'P0', 'Đang lọc Trạng thái = Chờ duyệt và sắp xếp theo Ngày duyệt.',
     '1. Bấm Làm mới.', '—', '- Mọi ô lọc về trống, bỏ sắp xếp, về trang 1.\n- Vẫn giữ đúng lối vào đang đứng.'),
    ('010', 'Ghi nhớ bộ lọc 10 phút', 'P2', 'Đang lọc Trạng thái = Đã duyệt.',
     '1. Mở chi tiết 1 phiếu.\n2. Bấm Quay lại.', '—', '- Trạng thái = Đã duyệt vẫn còn.'),
    ('011', 'Cài đặt bộ lọc: ẩn ô lọc', 'P1', '—',
     '1. Bấm Cài đặt bộ lọc.\n2. Bỏ tích "Người duyệt".\n3. Bấm Lưu.', '—',
     '- Ô Người duyệt không còn ở khối lọc.\n- Đăng xuất / đăng nhập lại vẫn giữ cấu hình.'),
    ('012', 'Cài đặt bộ lọc: Khôi phục mặc định', 'P2', 'Đã ẩn ô Người duyệt.',
     '1. Bấm Cài đặt bộ lọc.\n2. Bấm Khôi phục mặc định.\n3. Bấm Lưu.', '—', '- Đủ 8 ô lọc theo thứ tự ban đầu.'),
]

S3 = [
    ('001', 'Sắp xếp theo Mã phiếu', 'P0', '—', '1. Bấm tiêu đề cột Mã phiếu 2 lần.', '—',
     '- Lần 1 tăng dần, lần 2 giảm dần.\n- Luôn về trang 1, giữ bộ lọc.'),
    ('002', 'Sắp xếp theo Ngày tạo / Ngày duyệt', 'P1', '—', '1. Bấm tiêu đề cột Ngày duyệt.', '—',
     '- Thứ tự đúng theo ngày duyệt.\n- Cột Người tạo, Trạng thái không có mũi tên sắp xếp.'),
    ('003', 'Đổi số dòng mỗi trang', 'P1', 'Có 364 phiếu.', '1. Chọn Số dòng/trang = 50.', 'Số dòng/trang: 50',
     '- Hiện 50 dòng, "Hiển thị 1–50 / 364", về trang 1.'),
    ('004', 'Chuyển trang', 'P1', 'Có 364 phiếu, 10 dòng / trang.', '1. Bấm trang 3.', '—',
     '- "Hiển thị 21–30 / 364"; STT bắt đầu từ 21.'),
    ('005', 'Tùy chỉnh cột: bật cột ẩn', 'P1', '—',
     '1. Bấm nút Cấu hình cột hiển thị.\n2. Tích "Lý do từ chối".\n3. Bấm Lưu.', '—',
     '- Bảng có thêm cột Lý do từ chối, phiếu Không duyệt hiện đúng lý do.'),
    ('006', 'Tùy chỉnh cột: cột bị khóa', 'P1', '—', '1. Mở Tùy chỉnh cột.\n2. Thử bỏ tích STT, Mã phiếu, Hành động.', '—',
     '- Ba cột có biểu tượng ổ khóa, không bỏ tích được.'),
    ('007', 'Tùy chỉnh cột: đổi thứ tự', 'P2', '—', '1. Kéo cột Ngày tạo lên trên Người tạo.\n2. Bấm Lưu.', '—',
     '- Bảng đổi thứ tự cột theo đúng thao tác.'),
]

S4 = [
    ('001', 'Mở màn Thêm mới', 'P0', 'Tài khoản A có 3 phiếu xuất mượn Đã mượn.', TAO, '—',
     '- Tiêu đề "Thêm yêu cầu xuất hàng mượn".\n- Góc phải ghi "<tên A> - <ngày giờ hiện tại>".\n'
     '- Ô Phiếu xuất mượn ghi "Chưa chọn phiếu xuất mượn"; bảng Chi tiết trống.'),
    ('002', 'Popup Chọn phiếu xuất mượn chỉ hiện phiếu hợp lệ của mình', 'P0',
     'A có: PYCXH-TEST-023 (Xuất mượn, Đã mượn), PYCXH-TEST-030 (Xuất mượn, Đã trả), 1 phiếu Xuất bán.',
     TAO + '\n3. Bấm "Thêm phiếu".', '—',
     '- Chỉ có PYCXH-TEST-023.\n- KHÔNG có phiếu Đã trả, phiếu Xuất bán và phiếu của người khác.'),
    ('003', 'Chọn phiếu mượn', 'P0', 'Như TC_04.002.', '1. Trong popup bấm dòng PYCXH-TEST-023.', '—',
     '- Báo "Thêm thành công.".\n- Ô Phiếu xuất mượn có thẻ PYCXH-TEST-023; dòng trong popup ghi "Đã chọn".\n'
     '- Bảng Chi tiết KHÔNG tự sinh dòng hàng.'),
    ('004', 'Chọn trùng phiếu mượn', 'P1', 'Đã chọn PYCXH-TEST-023.', '1. Bấm lại dòng PYCXH-TEST-023 trong popup.', '—',
     '- Báo "Phiếu này đã được chọn.", không thêm thẻ thứ 2.'),
    ('005', 'Tìm phiếu trong popup', 'P2', '—', '1. Nhập "TEST-023" vào ô Mã phiếu xuất mượn.\n2. Bấm Tìm kiếm.',
     'Mã phiếu xuất mượn: TEST-023', '- Chỉ còn PYCXH-TEST-023.'),
    ('006', 'Thêm hàng có trên phiếu mượn', 'P0', 'PYCXH-TEST-023 có hàng ENEO-408-V5041 đã xuất 46, chưa trả.',
     '1. Bấm nút + ở bảng Chi tiết.\n2. Tìm ENEO-408-V5041, tích, bấm "Thêm 1 hàng hoá", bấm Đóng.',
     'Hàng hóa: ENEO-408-V5041',
     '- Bảng có 1 dòng hàng, dòng con Phiếu mượn = PYCXH-TEST-023, Đang mượn = 46, Xuất = 0.\n'
     '- Đơn giá theo đơn vị tính mặc định.'),
    ('007', 'Thêm hàng KHÔNG có trên phiếu mượn đã chọn', 'P0', 'Đã chọn PYCXH-TEST-023.',
     '1. Bấm +, thêm hàng "Face ID Intellegent Edge AI System".', '—',
     '- Dòng tô mờ, 3 ô chi tiết gộp thành "Chưa có phiếu mượn".\n- Không nhập được số lượng.'),
    ('008', 'Mã phiếu mượn trong bảng mở tab mới', 'P2', 'Dòng có PYCXH-TEST-023.', '1. Bấm mã PYCXH-TEST-023 trong bảng.', '—',
     '- Mở chi tiết phiếu yêu cầu xuất hàng ở tab mới; tab đang nhập giữ nguyên dữ liệu.'),
    ('009', 'Nhập số Xuất hợp lệ và tính tiền', 'P0', 'Dòng ENEO-408-V5041, Đang mượn 46, Đơn giá 60,500.',
     '1. Nhập Xuất = 5.', 'Xuất: 5',
     '- Số lượng xuất = 5.\n- Thành tiền = 302,500.\n- Dòng Tổng cộng: 5 và 302,500.'),
    ('010', 'Nhập Xuất vượt Đang mượn', 'P0', 'Như TC_04.009.', '1. Nhập Xuất = 47.', 'Xuất: 47',
     '- Chữ đỏ "Vượt quá số đang mượn" ngay dưới ô.\n- Ô KHÔNG tự đổi về 46.'),
    ('011', 'Nhập Xuất quá 6 chữ số', 'P2', '—', '1. Nhập Xuất = 1000000.', 'Xuất: 1000000',
     '- Báo "Không được vượt quá 6 chữ số" (hoặc "Vượt quá số đang mượn").'),
    ('012', 'Đổi đơn vị tính tính lại Đang mượn', 'P0',
     'Hàng có 2 đơn vị: Can 0.8L (x1) và Thùng (x24); Đang mượn 46 can; đã nhập Xuất = 30.',
     '1. Đổi Đơn vị tính sang Thùng (x24).', 'Đơn vị tính: Thùng (x24)',
     '- Đang mượn = 1 (46 / 24 làm tròn xuống).\n- Xuất tự kéo về 1.\n- Đơn giá đổi theo đơn vị Thùng.'),
    ('013', 'Đang mượn đã trừ phần đang chờ ở phiếu khác', 'P0',
     'PYCXH-TEST-025 hàng ENEO-408-V5037 đã xuất 45, đã trả 22; có 1 yêu cầu xuất bán hàng mượn Chờ duyệt 10.',
     TAO + '\n3. Chọn PYCXH-TEST-025, thêm hàng ENEO-408-V5037.', '—', '- Đang mượn = 13 (45 trừ 22 trừ 10).'),
    ('014', 'Bỏ một phiếu mượn đã chọn', 'P1', 'Đã chọn 2 phiếu mượn, cùng có hàng ENEO-408-V5041.',
     '1. Bấm dấu × trên thẻ 1 phiếu.', '—',
     '- Dòng hàng vẫn còn, chỉ mất dòng con của phiếu vừa bỏ.\n- Nếu không còn dòng con nào: dòng bị khóa "Chưa có phiếu mượn".'),
    ('015', 'Xóa dòng hàng', 'P2', 'Bảng có 2 dòng.', '1. Bấm biểu tượng thùng rác ở dòng 2.', '—',
     '- Còn 1 dòng, STT đánh lại, Tổng cộng cập nhật.'),
    ('016', 'Gửi duyệt khi form trống', 'P0', '—', TAO + '\n3. Bấm Gửi duyệt.', '—',
     '- Thông báo "Bạn chưa nhập đầy đủ thông tin.".\n'
     '- Chữ đỏ: "Bắt buộc phải chọn ít nhất 1 phiếu xuất mượn", "Bắt buộc phải nhập" (Ghi chú), '
     '"Bắt buộc phải đính kèm ít nhất 1 file", "Chưa có hàng hoá nào để xuất.".\n- Không gửi.'),
    ('017', 'Thiếu file đính kèm', 'P0', 'Đã chọn phiếu, nhập ghi chú, có dòng Xuất = 5.', '1. Bấm Gửi duyệt.', '—',
     '- Khối File đính kèm viền đỏ, "Bắt buộc phải đính kèm ít nhất 1 file".'),
    ('018', 'File đính kèm sai loại / quá dung lượng', 'P1', '—',
     '1. Bấm Thêm tài liệu, chọn file .docx.\n2. Chọn file PDF 25 MB.', 'File: baocao.docx; file.pdf 25 MB',
     '- Cả 2 file bị từ chối kèm thông báo lỗi.\n- File PDF dưới 20 MB nhận bình thường, hiện dung lượng.'),
    ('019', 'Ghi chú quá 255 ký tự', 'P2', '—', '1. Dán đoạn 300 ký tự vào Ghi chú.', 'Ghi chú: 300 ký tự',
     '- Ô chỉ nhận tối đa 255 ký tự.'),
    ('020', 'Dòng hàng có phiếu mượn nhưng chưa nhập Xuất', 'P0', 'Bảng có 2 dòng hợp lệ, dòng 2 Xuất = 0.',
     '1. Bấm Gửi duyệt.', '—', '- Dưới ô Xuất dòng 2: "Chưa nhập số lượng xuất".\n- Không gửi.'),
    ('021', 'Hộp xác nhận gửi duyệt — bấm Hủy', 'P1', 'Form hợp lệ.', '1. Bấm Gửi duyệt.\n2. Bấm Hủy.', '—',
     '- Hộp "Xác nhận gửi duyệt": "Gửi duyệt phiếu yêu cầu xuất hàng mượn này? Sau khi gửi, phiếu không sửa được nữa.".\n'
     '- Bấm Hủy: ở lại màn, dữ liệu giữ nguyên.'),
    ('022', 'Gửi duyệt thành công', 'P0', 'Form hợp lệ: 1 phiếu mượn, Ghi chú, 1 file PDF, 1 dòng Xuất = 5.',
     '1. Bấm Gửi duyệt.\n2. Bấm Gửi duyệt ở hộp xác nhận.', '—',
     '- Báo "Yêu cầu của bạn đã được gửi.".\n- Về danh sách, phiếu mới PYCXHM-NNNNN ở đầu, trạng thái Chờ duyệt.\n'
     '- Kế toán kho cùng công ty nhận thông báo "[YCXHM] Chờ duyệt: <mã>".'),
    ('023', 'Dòng bị khóa không vào phiếu', 'P0', 'Form như TC_04.022 + 1 dòng "Chưa có phiếu mượn".', '1. Gửi duyệt.', '—',
     '- Gửi thành công.\n- Mở chi tiết phiếu: chỉ có dòng hợp lệ, KHÔNG có dòng bị khóa.'),
    ('024', 'Lưu và tiếp tục', 'P1', 'Form hợp lệ.', '1. Bấm Lưu và tiếp tục.\n2. Xác nhận.', '—',
     '- Phiếu được gửi duyệt.\n- Ở lại màn Thêm mới, form trống để lập phiếu tiếp.'),
    ('025', 'Số Đang mượn thay đổi trong lúc nhập', 'P1',
     'Đang nhập Xuất = 46 cho ENEO-408-V5041; người khác vừa gửi 1 phiếu chờ trả 10 cái cùng hàng, cùng phiếu mượn.',
     '1. Bấm Gửi duyệt, xác nhận.', '—', '- Báo "Số lượng vượt quá số đang mượn (36).", không gửi.'),
    ('026', 'Quay lại khi đã nhập dữ liệu', 'P1', 'Đã chọn phiếu mượn và nhập Ghi chú.', '1. Bấm Quay lại.', '—',
     '- Hệ thống hỏi xác nhận rời trang; chọn ở lại thì dữ liệu còn nguyên.'),
]

S5 = [
    ('001', 'Nội dung màn chi tiết', 'P0', 'Phiếu PYCXHM-00337 Chờ duyệt, 2 dòng hàng, 1 file.',
     '1. Mở chi tiết PYCXHM-00337.', '—',
     '- Tiêu đề "Chi tiết yêu cầu xuất hàng mượn: PYCXHM-00337".\n- Có Phiếu xuất mượn, Ghi chú, Phòng ban yêu cầu, '
     'File đính kèm (có Dung lượng), bảng Chi tiết, khối Lịch sử.\n- Mọi ô chỉ đọc.'),
    ('002', 'Cột Được duyệt', 'P1', 'Phiếu Chờ duyệt và phiếu Đã duyệt.', '1. Mở 2 phiếu.', '—',
     '- Chờ duyệt: Được duyệt = 0.\n- Đã duyệt: Được duyệt đúng số trên Phiếu xuất hàng mượn.'),
    ('003', 'Khối Ghi chú duyệt', 'P1', 'Phiếu Không duyệt lý do "Sai số lượng".', '1. Mở chi tiết.', '—',
     '- Có khối "Ghi chú duyệt" ghi "Sai số lượng".\n- Phiếu khác không có khối này.'),
    ('004', 'Mở phiếu không tồn tại', 'P1', '—', '1. Bấm thông báo cũ của phiếu đã bị xóa khỏi hệ thống.', '—',
     '- Báo "Không tìm thấy dữ liệu", về danh sách.'),
    ('005', 'Quay lại về màn trước', 'P2', 'Vào chi tiết từ lối vào Kế toán kho.', '1. Bấm Quay lại.', '—',
     '- Về đúng danh sách Kế toán kho, giữ bộ lọc.'),
]

S6 = [
    ('001', 'Từ chối thiếu lý do', 'P0', 'Tài khoản B (Kế toán kho); PYCXHM-00337 Chờ duyệt.',
     '1. Mở chi tiết.\n2. Bấm Từ chối.\n3. Để trống lý do, bấm Xác nhận từ chối.', '—',
     '- Viền đỏ, "Bắt buộc phải nhập lý do từ chối".\n- Cửa sổ không đóng.'),
    ('002', 'Từ chối thành công', 'P0', 'Như TC_06.001.', '1. Nhập lý do, bấm Xác nhận từ chối.', 'Lý do: Sai số lượng',
     '- Báo "Thao tác thành công.", về danh sách đã mở.\n- Phiếu sang Không duyệt, Người duyệt = B, Lý do từ chối đúng.\n'
     '- Người lập nhận thông báo "[YCXHM] Từ chối" kèm lý do.\n- Lịch sử có mốc Không duyệt.'),
    ('003', 'Đóng cửa sổ từ chối', 'P2', '—', '1. Mở Từ chối, nhập lý do, bấm Đóng.', '—', '- Phiếu vẫn Chờ duyệt.'),
    ('004', 'Hai Kế toán kho cùng xử lý 1 phiếu', 'P1', 'B và B2 cùng mở chi tiết PYCXHM-00338.',
     '1. B từ chối thành công.\n2. B2 bấm Từ chối, nhập lý do, xác nhận.', '—',
     '- B2 nhận "Phiếu không còn ở trạng thái Chờ duyệt hoặc bạn không đủ quyền.".'),
    ('005', 'Duyệt bằng Tạo phiếu xuất hàng mượn', 'P0', 'B; phiếu PYCXHM-00337 Chờ duyệt.',
     '1. Mở chi tiết, bấm Tạo phiếu xuất hàng mượn.\n2. Ở màn Lập phiếu xuất hàng mượn bấm Lưu và duyệt.', '—',
     '- Màn Lập phiếu xuất mở với phiếu yêu cầu PYCXHM-00337 điền sẵn.\n- Sau khi lưu: phiếu yêu cầu Đã duyệt, có '
     'Người duyệt, Ngày duyệt, cột Được duyệt.\n- Người lập nhận "[YCXHM] Đã duyệt".'),
    ('006', 'Nút Duyệt trên dòng', 'P0', 'B; có phiếu Chờ duyệt.', '1. ' + MENU_KT + '\n2. Bấm nút Duyệt ở cột Hành động.', '—',
     '- Mở màn chi tiết phiếu đó.'),
    ('007', 'Thoát màn phiếu xuất không lưu', 'P2', 'Như TC_06.005.', '1. Bấm Tạo phiếu xuất hàng mượn.\n2. Bấm Quay lại.', '—',
     '- Phiếu yêu cầu vẫn Chờ duyệt.'),
]

S7 = [
    ('001', 'In phiếu từ danh sách', 'P1', '—', '1. Bấm biểu tượng In ở dòng PYCXHM-00337.', '—',
     '- Cửa sổ "Xem trước phiếu PYCXHM-00337".\n- Tiêu đề "PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN", đúng số phiếu, ngày tạo, hàng hóa.'),
    ('002', 'Logo bản in theo công ty của phiếu', 'P1', 'Phiếu thuộc Chi nhánh Vinh; người in thuộc công ty khác.',
     '1. In phiếu.', '—', '- Đầu bản in là logo, tên của Chi nhánh Vinh.'),
    ('003', 'In danh sách theo bộ lọc', 'P1', 'Lọc Trạng thái = Không duyệt (11 phiếu).', '1. Bấm nút In trên bảng.', '—',
     '- Cửa sổ "Xem trước danh sách yêu cầu xuất hàng mượn", khổ ngang, đúng 11 phiếu.'),
    ('004', 'In danh sách quá 2.000 phiếu', 'P2', 'Tài khoản tổng công ty, không lọc, hơn 2.000 phiếu.', '1. Bấm In.', '—',
     '- Không dựng bản in, hiện dòng nhắc thu hẹp bộ lọc.'),
    ('005', 'Xuất Excel theo trường đã chọn', 'P0', 'Lọc Trạng thái = Đã duyệt.',
     '1. Bấm Xuất Excel.\n2. Bỏ chọn hết, tích Mã phiếu, Trạng thái, Người tạo theo thứ tự này.\n3. Bấm Xuất file.', '—',
     '- Tải file tiêu đề "DANH SÁCH PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN".\n- Đúng 3 cột theo thứ tự Mã phiếu, Trạng thái, Người tạo.\n'
     '- Số dòng = số phiếu Đã duyệt.\n- Báo "Xuất Excel thành công".'),
    ('006', 'Xuất Excel khi không có dữ liệu', 'P2', 'Bộ lọc không có kết quả.', '1. Xuất Excel, Xuất file.', '—',
     '- Vẫn tải file có tiêu đề và dòng tên cột.'),
    ('007', 'Xuất Excel trong phạm vi quyền', 'P0', 'Tài khoản A (không quyền), 3 phiếu.', '1. Xuất file đủ 11 trường.', '—',
     '- File chỉ có 3 phiếu của A.'),
]

S8 = [
    ('001', 'Lịch sử từ danh sách', 'P1', 'Phiếu PYCXHM-00340 đã Tạo mới và Duyệt.', '1. Bấm biểu tượng Lịch sử ở dòng.', '—',
     '- Cửa sổ "Lịch sử thay đổi: PYCXHM-00340".\n- Mốc Duyệt ở trên: "Trạng thái: Chờ duyệt đến Đã duyệt", mã phiếu xuất PXHM-…\n'
     '- Mốc Tạo mới ở dưới, có Người thực hiện.'),
    ('002', 'Lịch sử từ màn chi tiết', 'P2', 'Như TC_08.001.', '1. Mở chi tiết.\n2. Ở khối Lịch sử bấm Xem lịch sử.', '—',
     '- Nội dung giống hệt cửa sổ ở TC_08.001.'),
    ('003', 'Lịch sử phiếu bị từ chối', 'P1', 'Phiếu Không duyệt lý do "Sai số lượng".', '1. Mở Lịch sử.', '—',
     '- Có mốc "Trạng thái: Chờ duyệt đến Không duyệt" kèm lý do "Sai số lượng".'),
]

S9 = [
    ('001', 'Luồng đầy đủ: lập đến duyệt', 'P0', 'A có phiếu mượn PYCXH-TEST-023; B là Kế toán kho cùng công ty.',
     '1. A lập phiếu xuất 5 cái ENEO-408-V5041, gửi duyệt.\n2. B mở lối vào Kế toán kho, lọc Chờ duyệt, Tạo phiếu xuất hàng mượn, '
     'Lưu và duyệt.\n3. A mở lại phiếu.', '—',
     '- Bước 1: B nhận thông báo.\n- Bước 3: phiếu Đã duyệt, Được duyệt = 5; A nhận thông báo Đã duyệt.\n'
     '- Lập phiếu mới với PYCXH-TEST-023: Đang mượn của hàng đó giảm 5.'),
    ('002', 'Luồng đầy đủ: lập đến từ chối đến lập lại', 'P0', 'Như TC_09.001.',
     '1. A gửi phiếu.\n2. B từ chối với lý do "Sai số lượng".\n3. A lập phiếu mới cùng phiếu mượn.', '—',
     '- Bước 2: A nhận thông báo kèm lý do; phiếu cũ không sửa được.\n- Bước 3: Đang mượn trở lại như trước khi gửi.'),
    ('003', 'Phiếu Chờ duyệt giữ chỗ số lượng', 'P0', 'A gửi phiếu xuất 10 cái, còn Chờ duyệt.',
     '1. A lập thêm 1 phiếu khác với cùng phiếu mượn, cùng hàng.', '—', '- Đang mượn đã trừ 10 của phiếu đang Chờ duyệt.'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & LỐI VÀO', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP PHIẾU (TẠO MỚI)', S4),
    ('V', 'XEM CHI TIẾT', S5),
    ('VI', 'DUYỆT & TỪ CHỐI', S6),
    ('VII', 'IN & XUẤT EXCEL', S7),
    ('VIII', 'LỊCH SỬ THAY ĐỔI', S8),
    ('IX', 'E2E FLOW', S9),
]

# ---------------------------------------------------------------- bổ sung theo chuẩn (30/10/2026)
# Mẫu Danh mục quốc gia + 8 ý góp ý tester 07/10/2026 (../phieu-theo-form-quoc-gia/tc_phieu_bosung.py).
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from tc_phieu_bosung import (ListScreen, open_menu_case, filter_memory_cases, combo_cases, org_cases,  # noqa: E402
                             weird_param_case, add_advanced_step, fill_pre, check_no_dash_pre)

SCREEN = ListScreen(menu=MENU_SALE, title='Yêu cầu xuất hàng mượn', total=364, quick_label='mã phiếu',
                    quick_sample='0036', quick_hit='8 phiếu PYCXHM-00360 đến PYCXHM-00367',
                    filters=[('Trạng thái', 'Đã duyệt'), ('Người duyệt', 'Cao Thị Thùy Linh')])
S1[0] = open_menu_case(SCREEN, pre='Tài khoản D có quyền Xem phiếu hàng mượn theo công ty; trong phạm vi có 364 phiếu.',
                       extra=['- Thấy phiếu cùng công ty và phiếu D tự lập; không có thông báo lỗi.'])
S1.append(weird_param_case('009', SCREEN, 'tiêu đề "Yêu cầu xuất hàng mượn"'))
S1.append(('010', 'Đang lọc rồi mở lối vào Kế toán kho', 'P1',
           'Tài khoản B có quyền Kế toán kho; đang ở lối vào Bán hàng, lọc Trạng thái = Chờ duyệt.',
           '1. ' + MENU_KT + '\n2. Quan sát tiêu đề và danh sách.', '—',
           '- Tiêu đề đổi thành "Yêu cầu xuất hàng mượn (Kế toán kho)".\n- Danh sách nạp lại theo phạm vi Kế toán kho, từ trang 1.'))
ORG = org_cases(SCREEN, 13)
MEM = filter_memory_cases(SCREEN, 14)
S2[7] = ('008',) + ORG[2][1:]
S2[9] = ('010',) + MEM[0][1:]
S2[:] = add_advanced_step(S2, {'006', '007', '008'}, MENU_SALE) + ORG[:2] + MEM[1:] + combo_cases(SCREEN, 19)
S4.append(('027', 'Lưu và tiếp tục khi dữ liệu lỗi', 'P0',
           'Tài khoản A có phiếu mượn PYCXH-TEST-023; form đã thêm 1 dòng hàng nhưng chưa chọn phiếu mượn, Ghi chú trống.',
           TAO + '\n3. Thêm hàng ENEO-408-V5041.\n4. Bấm Lưu và tiếp tục.', 'Ghi chú: trống',
           '- Thông báo "Bạn chưa nhập đầy đủ thông tin.".\n- Chữ đỏ dưới Phiếu xuất mượn, Ghi chú, File đính kèm.\n'
           '- KHÔNG lưu phiếu, KHÔNG mở form mới; dòng hàng đã thêm vẫn còn.'))
PRE_LIST = 'Tài khoản D (theo công ty); danh sách có 364 phiếu, 37 trang 10 dòng.'
S2[:] = fill_pre(S2, {}, PRE_LIST)
S3[:] = fill_pre(S3, {}, PRE_LIST)
S4[:] = fill_pre(S4, {
    '005': 'Tài khoản A có 27 phiếu mượn Đã mượn, trong đó PYCXH-TEST-023.',
    '011': 'Dòng ENEO-408-V5041, Đang mượn 46.',
    '016': 'Tài khoản A có ít nhất 1 phiếu mượn Đã mượn.',
    '018': 'Đang ở màn Tạo; có file baocao.docx và file PDF 25 MB trên máy.',
    '019': 'Đang ở màn Tạo; có sẵn đoạn văn 300 ký tự.',
})
S5[:] = fill_pre(S5, {'004': 'Tài khoản A có thông báo của một phiếu đã bị xóa khỏi hệ thống.'})
S6[:] = fill_pre(S6, {'003': 'Tài khoản B (Kế toán kho); phiếu PYCXHM-00337 Chờ duyệt.'})
S7[:] = fill_pre(S7, {'001': 'Phiếu PYCXHM-00337 có 2 dòng hàng, thuộc Chi nhánh Vinh.'})
check_no_dash_pre(SECTIONS, ROLE_TCS)

if __name__ == '__main__':
    build(output_file=OUT, sheet_name='Trang tính1', feature_name='Yêu cầu xuất hàng mượn - Cập nhật ngày 30/10/2026',
          module_name='YC xuất hàng mượn', description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
