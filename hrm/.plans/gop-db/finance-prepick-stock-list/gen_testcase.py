# -*- coding: utf-8 -*-
"""Sinh "testcase - Danh sach hang giu.xlsx" (phan he Tai chinh, nhom Giu hang).

Man BAO CAO CHI DOC: cay 3 tang Hang hoa -> Nhan vien -> Lo giu theo khach hang.
Viet tu code HRM nhanh `gop_db` (doc ngay 05/10/2026) + anh chup that tren dev.
Ngon ngu: NGHIEP VU cho QA — khong dung thuat ngu code, khong emoji.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, '..', '..', '..', '.claude', 'skills',
                                'testcase-documenter', 'assets'))
from tc_engine import build  # noqa: E402

MODULE = 'Danh sách hàng giữ'
MENU_STEP = 'Vào phân hệ Tài chính > nhóm "Giữ hàng" > bấm "Danh sách hàng giữ".'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn hình Danh sách hàng giữ là màn TRA CỨU CHỈ ĐỌC tồn hàng giữ: hàng hóa nào đang bị giữ, '
     'ai giữ, giữ cho khách nào, đến ngày nào, và lô đó biến động ra sao.\n'
     'Màn KHÔNG có Thêm / Sửa / Xóa / Nhập file; không thao tác nào làm thay đổi số hàng giữ.\n'
     'Hàng giữ sinh ra từ Phiếu xuất giữ và thay đổi qua phiếu gia hạn / hủy / điều chuyển hàng giữ '
     'và phiếu xuất bán — các màn đó mới là nơi tạo dữ liệu để test màn này.\n'
     'Đường dẫn: Phân hệ Tài chính > Giữ hàng > Danh sách hàng giữ.'),
    ('2. Đối tượng được tính / hiển thị',
     'Chỉ các lô hàng giữ có số lượng lớn hơn 0, trong phạm vi quyền của người đăng nhập.\n'
     'Tầng 1: mỗi dòng là một HÀNG HÓA (gom mọi lô khớp bộ lọc), phân trang theo hàng hóa.\n'
     'Tầng 2: mỗi dòng là một NHÂN VIÊN đang giữ hàng hóa đó.\n'
     'Tầng 3: mỗi dòng là một LÔ giữ của nhân viên đó cho một khách hàng (kèm Hạn giữ, Trạng '
     'thái, nút Lịch sử giữ hàng).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Lô đã về 0: không hiện ở bảng, Excel, bản In.\n'
     '- Lô ngoài phạm vi quyền: không hiện ở bất kỳ đâu, kể cả trong danh sách chọn Nhân viên / '
     'Thương hiệu / Model của bộ lọc.\n'
     '- Tầng hàng hóa và tầng nhân viên KHÔNG có Hạn giữ, Trạng thái, nút Lịch sử — ô trống là '
     'đúng thiết kế.\n'
     '- Người không có quyền "Quản lý giữ hàng": không xem được gì, kể cả khi có quyền xem theo '
     'cấp.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Màn không có ô lọc theo khoảng ngày.\n'
     'Ô lọc Trạng thái so HẠN GIỮ của từng lô với NGÀY HÔM NAY (theo ngày, không theo giờ): sau '
     'hôm nay = Trong hạn; đúng hôm nay = Đến hạn; trước hôm nay = Hết hạn.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Cây trên màn: Hàng hóa > Nhân viên > Lô theo khách hàng.\n'
     'Bản In gom KHÁC: Phòng ban > Nhân viên > Mục hàng (STT 1 / 1.1 / 1.1.1).\n'
     'Excel là bảng PHẲNG: mỗi dòng một lô.\n'
     'Lịch sử giữ hàng: sổ biến động của cặp hàng hóa × nhân viên × khách hàng × công ty, sắp '
     'từ CŨ đến MỚI.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     'SL giữ tầng hàng hóa = tổng SL các lô khớp bộ lọc của hàng hóa đó.\n'
     'SL giữ tầng nhân viên = tổng SL các lô của nhân viên đó (khớp bộ lọc).\n'
     'Tổng SL trong kho = tổng tồn kho kế toán của hàng hóa ở các kho kế toán trong phạm vi công '
     'ty được xem; KHÔNG đổi theo ô Lọc theo kho.\n'
     'Excel: cột Tổng SL trong kho lặp lại trên mọi lô cùng hàng hóa (không cộng dọc).'),
    ('7. Phân quyền cấp',
     'Quyền vào màn: "Quản lý giữ hàng" (Super admin được coi như có).\n'
     'Phạm vi, xét theo thứ tự:\n'
     '- "Xem phiếu hàng giữ theo tổng công ty": mọi công ty, có thêm ô lọc Công ty.\n'
     '- "Xem phiếu hàng giữ theo công ty": lô thuộc công ty của mình (theo công ty ghi trên lô).\n'
     '- "Xem phiếu hàng giữ theo phòng ban": lô của nhân viên thuộc phòng mình quản lý + phòng '
     'mình + chính mình.\n'
     '- Không có quyền xem theo cấp: chỉ lô của chính mình.\n'
     'Phạm vi áp cho bảng, bộ lọc, Excel, In.'),
    ('8. Cách tính các ô thống kê',
     'Ô "Hiển thị a–b / N": N là tổng số HÀNG HÓA khớp bộ lọc, không phải số lô.\n'
     'Bản In: Số phòng ban, Số nhân viên, Số mục hàng (số lô) đếm trên dữ liệu đã lọc.\n'
     'Cửa sổ Lịch sử: "Số lượng giữ hiện tại" = SL của lô vừa bấm; cột SL giữ = số còn lại sau '
     'mỗi lần biến động.\n'
     'Đổi đơn vị: số = số theo đơn vị cơ bản chia hệ số, làm tròn XUỐNG 2 chữ số thập phân.'),
    ('9. Ghi chú đọc bảng',
     'Lưu ý để không ghi Failed oan:\n'
     '- Cột STT tầng hàng hóa chỉ có nút tròn ">", KHÔNG in số thứ tự — đúng thiết kế hiện tại.\n'
     '- Lịch sử giữ hàng sắp CŨ > MỚI (ngược quy tắc chung) — có chủ đích.\n'
     '- Ô tìm nhanh tìm theo KHÁCH HÀNG (tên, mã, số điện thoại), không theo hàng hóa.\n'
     '- Lọc theo kho chỉ giữ hàng hóa có ghi nhận tồn ở kho đó; SL giữ không đổi theo kho.\n'
     '- Excel và In luôn theo đơn vị cơ bản, không theo đơn vị đang chọn trên màn.\n'
     '- Số theo chuẩn quốc tế: dấu phẩy ngăn hàng nghìn, dấu chấm phần thập phân (1,234.5).\n'
     '- Ô không có dữ liệu để TRỐNG.'),
]

ROLE_TCS = [
    ('01', 'Không có quyền "Quản lý giữ hàng" thì không xem được màn', 'P0',
     'Tài khoản A không có quyền "Quản lý giữ hàng", không có quyền xem theo cấp. A đang đứng tên '
     'giữ 3 lô hàng.',
     '1. Đăng nhập bằng A.\n2. ' + MENU_STEP,
     '—',
     '- Mục menu "Danh sách hàng giữ" vẫn hiển thị.\n'
     '- Phần mềm báo "Bạn không có quyền xem danh sách hàng giữ".\n'
     '- Bảng hiện "Không có dữ liệu phù hợp bộ lọc.", không thấy cả 3 lô của chính A.\n'
     '- Các ô chọn Thương hiệu / Model / Nhân viên không có dữ liệu.'),
    ('02', 'Có quyền xem theo cấp nhưng thiếu "Quản lý giữ hàng" vẫn bị chặn', 'P0',
     'Tài khoản B có quyền "Xem phiếu hàng giữ theo công ty", KHÔNG có "Quản lý giữ hàng".',
     '1. Đăng nhập bằng B.\n2. ' + MENU_STEP,
     '—',
     '- Phần mềm báo "Bạn không có quyền xem danh sách hàng giữ".\n'
     '- Bảng rỗng. Quyền xem theo cấp không thay được quyền vào màn.'),
    ('03', 'Chỉ có "Quản lý giữ hàng": chỉ thấy lô của chính mình', 'P0',
     'Tài khoản C có "Quản lý giữ hàng", không có quyền xem theo cấp. C giữ 4 lô thuộc 2 hàng '
     'hóa; đồng nghiệp cùng phòng giữ 10 lô khác.',
     '1. Đăng nhập bằng C.\n2. ' + MENU_STEP + '\n3. Đọc ô "Hiển thị a–b / N".\n'
     '4. Mở chi tiết cả 2 hàng hóa.\n5. Mở ô lọc Nhân viên.',
     '—',
     '- N = 2.\n'
     '- Chi tiết chỉ có dòng nhân viên C, tổng 4 lô.\n'
     '- Ô lọc Nhân viên chỉ có tên C.\n'
     '- Không có ô lọc Công ty.'),
    ('04', 'Quyền "Xem phiếu hàng giữ theo phòng ban"', 'P0',
     'Tài khoản D có "Quản lý giữ hàng" + "Xem phiếu hàng giữ theo phòng ban", quản lý phòng KD1 '
     '(5 nhân viên đang giữ hàng). Phòng KD2 có 3 nhân viên đang giữ hàng.',
     '1. Đăng nhập bằng D.\n2. ' + MENU_STEP + '\n3. Mở ô lọc Nhân viên.\n'
     '4. Mở chi tiết vài hàng hóa.',
     '—',
     '- Ô Nhân viên liệt kê 5 nhân viên phòng KD1 (và D nếu D đang giữ hàng), không có ai của '
     'KD2.\n'
     '- Chi tiết không có dòng nhân viên nào thuộc KD2.'),
    ('05', 'Quyền "Xem phiếu hàng giữ theo công ty"', 'P0',
     'Tài khoản E thuộc công ty 1, có "Quản lý giữ hàng" + "Xem phiếu hàng giữ theo công ty". '
     'Công ty 1 có 1,445 lô của 600 hàng hóa; công ty 4 có 937 lô.',
     '1. Đăng nhập bằng E.\n2. ' + MENU_STEP + '\n3. Đọc N.\n4. Xuất Excel đủ 12 trường.',
     '—',
     '- N = 600 hàng hóa.\n'
     '- Tệp Excel có 1,445 dòng dữ liệu, không có lô nào của công ty 4.\n'
     '- Không có ô lọc Công ty.'),
    ('06', 'Quyền "Xem phiếu hàng giữ theo tổng công ty"', 'P0',
     'Tài khoản F có "Quản lý giữ hàng" + "Xem phiếu hàng giữ theo tổng công ty". Hệ thống có lô '
     'của công ty 1, 3, 4.',
     '1. Đăng nhập bằng F.\n2. ' + MENU_STEP + '\n3. Bấm "Tìm kiếm nâng cao".\n'
     '4. Chọn Công ty = công ty 4.',
     'Công ty: công ty 4',
     '- Trước bước 4 thấy hàng giữ của cả 3 công ty.\n'
     '- Khu vực lọc có ô Công ty.\n'
     '- Sau bước 4 chỉ còn lô của công ty 4; cột Tổng SL trong kho chỉ cộng kho của công ty 4.'),
    ('07', 'Phạm vi công ty xét theo công ty ghi trên lô', 'P0',
     'Nhân viên G chuyển từ công ty 4 sang công ty 1 nhưng vẫn còn 2 lô giữ ghi công ty 4. Tài '
     'khoản E chỉ có quyền xem theo công ty 1.',
     '1. Đăng nhập bằng E.\n2. Lọc Nhân viên = G (nếu có trong danh sách).',
     '—',
     '- E KHÔNG thấy 2 lô ghi công ty 4 của G.\n'
     '- Lưu ý: phạm vi theo công ty ghi trên lô, không theo công ty hiện tại của nhân viên.'),
    ('08', 'Tài khoản Quản trị hệ thống xem toàn bộ', 'P1',
     'Tài khoản Super admin, không gán quyền nào.',
     '1. Đăng nhập Super admin.\n2. ' + MENU_STEP,
     '—',
     '- Xem được mọi công ty, có ô lọc Công ty.\n- Không bị báo thiếu quyền.'),
    ('09', 'Gọi thẳng chức năng xem lịch sử của lô ngoài phạm vi', 'P2',
     'Tài khoản C chỉ xem được lô của mình. Lô X thuộc nhân viên khác, công ty khác.',
     '1. Dùng công cụ kiểm thử, đăng nhập bằng C.\n'
     '2. Gọi thẳng chức năng xem Lịch sử giữ hàng với hàng hóa, nhân viên, khách hàng, công ty '
     'của lô X.',
     '—',
     '- Mong đợi: phần mềm từ chối hoặc trả danh sách rỗng vì lô X ngoài phạm vi của C.\n'
     '- Lưu ý: khi đọc mã nguồn thấy chức năng này chưa áp phạm vi xem theo cấp — nếu trả về đủ '
     'sổ biến động của lô X thì ghi Failed và báo đội phát triển.'),
]

S1 = [
    ('001', 'Vào màn qua menu', 'P0',
     'Tài khoản F (xem tổng công ty) có quyền "Quản lý giữ hàng". Hệ thống có 1,035 hàng hóa đang '
     'bị giữ.',
     '1. Đăng nhập.\n2. ' + MENU_STEP,
     '—',
     '- Tiêu đề trang và tiêu đề khối bảng là "Danh sách hàng giữ".\n'
     '- Bảng hiện 10 hàng hóa đầu, ô thống kê ghi "Hiển thị 1–10 / 1,035".\n'
     '- Vòng quay chờ biến mất sau khi nạp xong.'),
    ('002', 'Bố cục khối bộ lọc', 'P1',
     'Đang ở màn Danh sách hàng giữ.',
     '1. Quan sát khối "Bộ lọc danh sách".',
     '—',
     '- Có ô tìm nhanh với chữ mờ "Nhập tên, số điện thoại hoặc mã KH để tìm kiếm".\n'
     '- Có nút "Tìm kiếm", "Làm mới", "Cài đặt bộ lọc", "Tìm kiếm nâng cao".\n'
     '- Khu vực lọc nâng cao đang thu gọn.'),
    ('003', 'Thanh công cụ chỉ có In, Xuất Excel, Tuỳ chỉnh cột', 'P0',
     'Đang ở màn danh sách.',
     '1. Quan sát góc phải khối "Danh sách hàng giữ".',
     '—',
     '- Có đúng 3 nút theo thứ tự: "In", "Xuất Excel", nút biểu tượng cột.\n'
     '- KHÔNG có nút Thêm mới, Nhập file, Sửa, Xóa ở bất kỳ đâu.'),
    ('004', 'Bộ cột mặc định của bảng', 'P0',
     'Tài khoản chưa từng tuỳ chỉnh cột ở màn này.',
     '1. Mở màn danh sách.\n2. Đọc tiêu đề các cột từ trái sang phải (cuộn ngang nếu cần).',
     '—',
     '- Đúng thứ tự: STT, Mã hàng hóa / Nhân viên / Khách hàng, Tên hàng hóa / Phòng ban, Đơn vị, '
     'Model, Thương hiệu, Tổng SL trong kho, SL giữ, Hạn giữ, Trạng thái, Hành động.'),
    ('005', 'Dòng hàng hóa hiển thị đúng dữ liệu', 'P0',
     'Hàng hóa PULI-KU-DP7 đang bị giữ 17 Bộ bởi 7 nhân viên; tổng tồn kho kế toán 41.',
     '1. Tìm dòng PULI-KU-DP7.',
     'Mã hàng hóa: PULI-KU-DP7',
     '- Cột STT có nút tròn ">", không in số thứ tự.\n'
     '- Mã hàng hóa là chữ thường, không phải liên kết.\n'
     '- Đơn vị "Bộ", Model "K.U-DP7", Thương hiệu "KOISU".\n'
     '- Tổng SL trong kho = 41; SL giữ = 17.\n'
     '- Hạn giữ, Trạng thái, Hành động để trống.'),
    ('006', 'Sắp xếp mặc định theo tên hàng hóa', 'P1',
     'Chưa bấm sắp xếp cột nào.',
     '1. Mở màn.\n2. Đọc cột Tên hàng hóa của 10 dòng đầu.',
     '—',
     '- Tên hàng hóa tăng dần theo bảng chữ cái.'),
    ('007', 'Bộ lọc được nhớ trong 10 phút', 'P1',
     'Đang lọc Trạng thái = Hết hạn, khu vực lọc nâng cao đang mở.',
     '1. Chuyển sang màn khác.\n2. Trong vòng 10 phút quay lại Danh sách hàng giữ.',
     'Trạng thái: Hết hạn',
     '- Ô Trạng thái vẫn là "Hết hạn", khu vực lọc nâng cao vẫn mở.\n'
     '- Danh sách đúng theo điều kiện cũ.'),
    ('008', 'Bộ lọc hết hiệu lực sau 10 phút', 'P2',
     'Đang lọc Trạng thái = Hết hạn.',
     '1. Rời màn hơn 10 phút.\n2. Quay lại màn.',
     '—',
     '- Bộ lọc về mặc định, danh sách hiện đầy đủ.'),
    ('009', 'Mở màn kèm mã hàng hóa trên đường dẫn', 'P2',
     'Biết mã định danh của hàng hóa H. Đang có bộ lọc đã lưu Trạng thái = Trong hạn.',
     '1. Mở màn bằng đường dẫn có kèm mã định danh của H.\n2. Bấm Làm mới.',
     '—',
     '- Bước 1: bảng chỉ còn đúng hàng hóa H.\n'
     '- Bước 2: quay về danh sách đầy đủ, điều kiện hàng hóa H bị xóa.'),
    ('010', 'Phạm vi không có dữ liệu', 'P1',
     'Tài khoản C có "Quản lý giữ hàng", không giữ lô nào, không có quyền xem theo cấp.',
     '1. Đăng nhập bằng C.\n2. ' + MENU_STEP,
     '—',
     '- Bảng hiện dòng "Không có dữ liệu phù hợp bộ lọc.".\n'
     '- Không báo lỗi quyền.'),
]

S2 = [
    ('001', 'Ô tìm nhanh theo tên khách hàng', 'P0',
     'Khách hàng "CÔNG TY TNHH ĐÔNG ĐÔ" (mã 15TPHPLE-4) đang được giữ 1 lô hàng PULI-KU-DP7.',
     '1. Gõ "ĐÔNG ĐÔ" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.\n3. Mở chi tiết PULI-KU-DP7.',
     'Ô tìm nhanh: ĐÔNG ĐÔ',
     '- Chỉ còn hàng hóa có lô giữ cho khách khớp từ khóa.\n'
     '- Chi tiết PULI-KU-DP7 chỉ còn dòng khách "15TPHPLE-4 - CÔNG TY TNHH ĐÔNG ĐÔ" và nhân viên '
     'giữ lô đó.\n'
     '- SL giữ tầng hàng hóa = 1.'),
    ('002', 'Ô tìm nhanh theo mã khách hàng', 'P1',
     'Khách mã 47TDAPTA-75 đang được giữ hàng.',
     '1. Gõ "47TDAPTA" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: 47TDAPTA',
     '- Danh sách chỉ còn hàng hóa giữ cho khách 47TDAPTA-75.'),
    ('003', 'Ô tìm nhanh theo số điện thoại khách hàng', 'P1',
     'Khách K có số điện thoại 0912345678 đang được giữ 2 hàng hóa.',
     '1. Gõ "0912345" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: 0912345',
     '- N = 2, đúng 2 hàng hóa giữ cho khách K.'),
    ('004', 'Ô tìm nhanh chỉ áp dụng khi bấm Tìm kiếm', 'P1',
     'Đang ở màn danh sách, N = 1,035.',
     '1. Gõ "ĐÔNG ĐÔ" vào ô tìm nhanh, KHÔNG bấm Tìm kiếm.\n2. Chờ 3 giây.\n3. Bấm Tìm kiếm.',
     'Ô tìm nhanh: ĐÔNG ĐÔ',
     '- Sau bước 2 danh sách chưa đổi, N vẫn là 1,035.\n'
     '- Sau bước 3 danh sách mới được lọc.'),
    ('005', 'Ô tìm nhanh không tìm theo hàng hóa', 'P2',
     'Hàng hóa PULI-KU-DP7 đang bị giữ.',
     '1. Gõ "PULI-KU-DP7" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: PULI-KU-DP7',
     '- Không tìm theo mã hàng hóa: chỉ ra kết quả nếu có khách hàng trùng chuỗi này, thường là '
     '"Không có dữ liệu phù hợp bộ lọc.".\n'
     '- Muốn tìm theo hàng hóa phải dùng ô lọc Mã hàng hóa.'),
    ('006', 'Mở / thu khu vực lọc nâng cao', 'P1',
     'Khu vực lọc nâng cao đang thu gọn.',
     '1. Bấm "Tìm kiếm nâng cao".\n2. Bấm "Ẩn tìm kiếm nâng cao".',
     '—',
     '- Bước 1 hiện các ô: Mã hàng hóa, Tên hàng hóa, Lọc theo kho, Thương hiệu, Model, Trạng '
     'thái, Nhân viên, Công ty (nếu có quyền tổng công ty), Phòng ban.\n'
     '- Nút đổi chữ thành "Ẩn tìm kiếm nâng cao".\n'
     '- Bước 2 thu gọn khu vực, điều kiện đang chọn vẫn giữ.'),
    ('007', 'Lọc Mã hàng hóa gần đúng', 'P0',
     'Có 3 hàng hóa mã bắt đầu "PULI-KU-DP" đang bị giữ.',
     '1. Mở lọc nâng cao.\n2. Gõ "PULI-KU-DP" vào ô Mã hàng hóa.',
     'Mã hàng hóa: PULI-KU-DP',
     '- Danh sách tự nạp lại, chỉ còn 3 hàng hóa PULI-KU-DP5, PULI-KU-DP7, PULI-KU-DP9:01.'),
    ('008', 'Lọc Tên hàng hóa gần đúng', 'P1',
     'Có hàng hóa tên chứa "Bàn nâng cắt kéo" đang bị giữ.',
     '1. Gõ "cắt kéo" vào ô Tên hàng hóa.',
     'Tên hàng hóa: cắt kéo',
     '- Chỉ còn hàng hóa có tên chứa "cắt kéo".'),
    ('009', 'Lọc theo kho', 'P0',
     'Hàng hóa H1 có ghi nhận tồn kho kế toán ở kho LN01; hàng hóa H2 không có ở LN01. Cả hai '
     'đang bị giữ.',
     '1. Mở ô "Lọc theo kho".\n2. Chọn kho LN01.\n3. Đọc SL giữ và Tổng SL trong kho của H1.',
     'Lọc theo kho: LN01',
     '- Danh sách kho hiển thị dạng "Mã - Tên".\n'
     '- Chỉ còn hàng hóa có tồn kho ghi nhận ở LN01: có H1, không có H2.\n'
     '- SL giữ và Tổng SL trong kho của H1 KHÔNG đổi so với trước khi lọc (hàng giữ không gắn '
     'kho).'),
    ('010', 'Danh sách kho theo phạm vi công ty', 'P1',
     'Tài khoản E chỉ xem theo công ty 1; tài khoản F xem tổng công ty.',
     '1. Đăng nhập E, mở ô "Lọc theo kho", đếm số kho.\n2. Đăng nhập F, làm tương tự.',
     '—',
     '- E chỉ thấy kho kế toán của công ty 1.\n'
     '- F thấy kho của mọi công ty (khoảng 55 kho), gồm cả kho đang Chờ xóa.'),
    ('011', 'Lọc Thương hiệu chỉ liệt kê thương hiệu đang có hàng giữ', 'P1',
     'Thương hiệu KOISU có hàng đang bị giữ; thương hiệu X có trong danh mục nhưng không có hàng '
     'đang giữ.',
     '1. Mở ô Thương hiệu.\n2. Tìm KOISU và X.\n3. Chọn KOISU.',
     'Thương hiệu: KOISU',
     '- Có KOISU, KHÔNG có X.\n- Sau bước 3 chỉ còn hàng hóa thương hiệu KOISU.'),
    ('012', 'Lọc Model', 'P1',
     'Model K.U-DP7 có hàng đang bị giữ.',
     '1. Mở ô Model, chọn K.U-DP7.',
     'Model: K.U-DP7',
     '- Chỉ còn hàng hóa model K.U-DP7.\n'
     '- Danh sách Model chỉ gồm model của hàng hóa đang có hàng giữ trong phạm vi.'),
    ('013', 'Lọc Trạng thái = Hết hạn', 'P0',
     'Hôm nay là 05/10/2026. PULI-KU-DP7 có 7 lô hạn giữ trước 05/10/2026 và không lô nào khác.',
     '1. Chọn Trạng thái = Hết hạn.\n2. Mở chi tiết PULI-KU-DP7.',
     'Trạng thái: Hết hạn',
     '- Mọi dòng lô đều có badge "Hết hạn" màu đỏ, hạn giữ trước 05/10/2026.\n'
     '- Không có lô Trong hạn hay Đến hạn.'),
    ('014', 'Lọc Trạng thái = Trong hạn', 'P0',
     'Hôm nay 05/10/2026. Có lô hạn giữ 13/10/2026.',
     '1. Chọn Trạng thái = Trong hạn.\n2. Mở chi tiết vài hàng hóa.',
     'Trạng thái: Trong hạn',
     '- Mọi lô có hạn giữ SAU 05/10/2026, badge "Trong hạn" màu xanh lá.'),
    ('015', 'Lọc Trạng thái = Đến hạn', 'P1',
     'Hôm nay 05/10/2026. Có 1 lô hạn giữ đúng 05/10/2026.',
     '1. Chọn Trạng thái = Đến hạn.',
     'Trạng thái: Đến hạn',
     '- Chỉ còn hàng hóa của lô hạn giữ 05/10/2026, badge "Đến hạn" màu vàng.'),
    ('016', 'SL giữ tầng hàng hóa cộng theo bộ lọc', 'P0',
     'Hàng hóa H có 3 lô: 2 lô Hết hạn (SL 4 và 6), 1 lô Trong hạn (SL 5).',
     '1. Không lọc, đọc SL giữ của H.\n2. Lọc Trạng thái = Hết hạn, đọc lại.',
     'Trạng thái: Hết hạn',
     '- Bước 1: SL giữ = 15.\n- Bước 2: SL giữ = 10 (chỉ cộng các lô khớp bộ lọc).'),
    ('017', 'Lọc Nhân viên', 'P0',
     'Nhân viên Đàm Phước Nhiên đang giữ 1 lô PULI-KU-DP7.',
     '1. Chọn Nhân viên = Đàm Phước Nhiên.\n2. Mở chi tiết PULI-KU-DP7.',
     'Nhân viên: Đàm Phước Nhiên',
     '- Chỉ còn hàng hóa nhân viên này đang giữ.\n'
     '- Chi tiết chỉ có dòng nhân viên Đàm Phước Nhiên.'),
    ('018', 'Danh sách Nhân viên chỉ gồm người đang giữ hàng', 'P1',
     'Nhân viên Q thuộc phạm vi xem nhưng không giữ lô nào.',
     '1. Mở ô Nhân viên, tìm Q.',
     '—',
     '- KHÔNG có Q trong danh sách.'),
    ('019', 'Đổi Phòng ban thì ô Nhân viên bị xóa và thu hẹp', 'P1',
     'Đang chọn Nhân viên = Đàm Phước Nhiên (Phòng KD Khu vực 2).',
     '1. Chọn Phòng ban = PHÒNG THIẾT BỊ Ô TÔ 1.\n2. Mở ô Nhân viên.',
     'Phòng ban: PHÒNG THIẾT BỊ Ô TÔ 1',
     '- Ô Nhân viên tự xóa giá trị.\n'
     '- Danh sách Nhân viên chỉ còn người thuộc PHÒNG THIẾT BỊ Ô TÔ 1 đang giữ hàng.\n'
     '- Bảng chỉ còn lô của nhân viên thuộc phòng đó.'),
    ('020', 'Lọc Công ty (quyền tổng công ty)', 'P1',
     'Tài khoản F. Công ty 3 có 30 lô.',
     '1. Chọn Công ty = công ty 3.\n2. Xuất Excel đủ 12 trường.',
     'Công ty: công ty 3',
     '- Bảng chỉ còn hàng hóa của công ty 3.\n'
     '- Ô Phòng ban chỉ còn phòng của công ty 3.\n'
     '- Tệp Excel có 30 dòng dữ liệu.'),
    ('021', 'Công tắc hiện công ty / phòng ban đã khóa', 'P2',
     'Tài khoản F. Có phòng ban P đã khóa.',
     '1. Bấm biểu tượng ổ khóa cạnh nhãn Phòng ban.\n2. Mở ô Phòng ban.',
     '—',
     '- Trước bước 1 không có P; sau bước 1 có P.\n'
     '- Rê chuột vào ổ khóa thấy gợi ý "Hiện cả phòng ban đã khoá".'),
    ('022', 'Kết hợp nhiều điều kiện', 'P1',
     'Có dữ liệu thương hiệu KOISU, trạng thái Hết hạn.',
     '1. Chọn Thương hiệu = KOISU.\n2. Chọn Trạng thái = Hết hạn.\n3. Gõ "DP" vào Mã hàng hóa.',
     'Thương hiệu: KOISU\nTrạng thái: Hết hạn\nMã hàng hóa: DP',
     '- Kết quả thỏa đồng thời 3 điều kiện.'),
    ('023', 'Làm mới xóa toàn bộ điều kiện và tự nạp lại', 'P0',
     'Đang lọc Thương hiệu = KOISU, ô tìm nhanh "ĐÔNG ĐÔ", đang sắp SL giữ giảm dần.',
     '1. Bấm "Làm mới".',
     '—',
     '- Mọi ô lọc và ô tìm nhanh trống.\n'
     '- Thứ tự về mặc định Tên hàng hóa A > Z.\n'
     '- Danh sách tự nạp lại đầy đủ, không cần bấm Tìm kiếm.'),
    ('024', 'Không có kết quả', 'P1',
     'Đang ở màn danh sách.',
     '1. Gõ "XYZ-KHONG-TON-TAI" vào ô Mã hàng hóa.',
     'Mã hàng hóa: XYZ-KHONG-TON-TAI',
     '- Bảng hiện "Không có dữ liệu phù hợp bộ lọc.".\n- Ô thống kê ghi tổng 0.'),
    ('025', 'Cài đặt bộ lọc: ẩn một ô', 'P1',
     'Chưa cấu hình bộ lọc.',
     '1. Bấm "Cài đặt bộ lọc".\n2. Bỏ tích "Model".\n3. Bấm Lưu.\n4. Mở lọc nâng cao.',
     '—',
     '- Cửa sổ có dòng hướng dẫn "Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài '
     'đặt được lưu theo từng màn hình.".\n'
     '- Có 8 mục: Mã hàng hóa, Tên hàng hóa, Lọc theo kho, Thương hiệu, Model, Trạng thái, Nhân '
     'viên, Công ty – Phòng ban.\n'
     '- Sau khi lưu, khu vực lọc không còn ô Model.'),
    ('026', 'Cài đặt bộ lọc: kéo đổi thứ tự', 'P2',
     'Đang mở cửa sổ Cài đặt bộ lọc.',
     '1. Kéo "Trạng thái" lên đầu.\n2. Bấm Lưu.',
     '—',
     '- Ô Trạng thái đứng đầu khu vực lọc nâng cao.'),
    ('027', 'Cài đặt bộ lọc: Khôi phục mặc định và Đóng', 'P2',
     'Đã ẩn ô Model và đổi thứ tự.',
     '1. Mở Cài đặt bộ lọc, bỏ tích "Nhân viên", bấm Đóng.\n'
     '2. Mở lại, bấm "Khôi phục mặc định", bấm Lưu.',
     '—',
     '- Bước 1: ô Nhân viên vẫn hiện (Đóng không lưu).\n'
     '- Bước 2: đủ 8 mục theo thứ tự gốc.'),
]

S3 = [
    ('001', 'Sắp xếp theo SL giữ', 'P0',
     'Đang ở trang 1.',
     '1. Bấm tiêu đề cột "SL giữ".\n2. Bấm lại lần nữa.',
     '—',
     '- Bước 1: SL giữ tăng dần.\n- Bước 2: SL giữ giảm dần.\n'
     '- Mỗi lần đều quay về trang 1, giữ nguyên bộ lọc.'),
    ('002', 'Sắp xếp theo Tổng SL trong kho', 'P1',
     'Đang ở màn danh sách.',
     '1. Bấm tiêu đề cột "Tổng SL trong kho" hai lần.',
     '—',
     '- Lần 1 tăng dần, lần 2 giảm dần theo Tổng SL trong kho.'),
    ('003', 'Sắp xếp theo Mã hàng hóa và Tên hàng hóa', 'P1',
     'Đang ở màn danh sách.',
     '1. Bấm tiêu đề "Mã hàng hóa / Nhân viên / Khách hàng".\n'
     '2. Bấm tiêu đề "Tên hàng hóa / Phòng ban" hai lần.',
     '—',
     '- Bước 1 sắp theo mã hàng hóa tăng dần.\n'
     '- Bước 2 sắp theo tên hàng hóa tăng rồi giảm dần.'),
    ('004', 'Các cột khác không sắp xếp được', 'P2',
     'Đang ở màn danh sách.',
     '1. Bấm tiêu đề cột Đơn vị, Model, Thương hiệu, Hạn giữ, Trạng thái.',
     '—',
     '- Các cột này không có biểu tượng sắp xếp, bấm không đổi thứ tự.'),
    ('005', 'Phân trang theo hàng hóa', 'P0',
     'Có 1,035 hàng hóa đang bị giữ.',
     '1. Bấm trang 2.\n2. Bấm nút trang cuối.',
     '—',
     '- Bước 1: "Hiển thị 11–20 / 1,035".\n- Bước 2: "Hiển thị 1,031–1,035 / 1,035".'),
    ('006', 'Đổi số dòng mỗi trang', 'P1',
     'Đang ở trang 3.',
     '1. Đổi "Số dòng/trang" thành 50.',
     'Số dòng/trang: 50',
     '- Danh sách chọn có 5, 10, 20, 50, 100.\n'
     '- Quay về trang 1, hiện 50 hàng hóa, "Hiển thị 1–50 / 1,035".'),
    ('007', 'Lật trang thu gọn chi tiết đang mở', 'P2',
     'Đang mở chi tiết 2 hàng hóa ở trang 1.',
     '1. Bấm trang 2.\n2. Quay lại trang 1.',
     '—',
     '- Mọi hàng hóa đều ở trạng thái thu gọn (nút ">").'),
    ('008', 'Tuỳ chỉnh cột: tắt một cột', 'P1',
     'Chưa cấu hình cột.',
     '1. Bấm nút biểu tượng cột.\n2. Bỏ tích "Model".\n3. Bấm Lưu.',
     '—',
     '- Cửa sổ "Tuỳ chỉnh cột" liệt kê 11 cột, mặc định tích hết.\n'
     '- Sau khi lưu, bảng không còn cột Model.'),
    ('009', 'Tuỳ chỉnh cột: cột bị khóa', 'P1',
     'Đang mở cửa sổ Tuỳ chỉnh cột.',
     '1. Thử bỏ tích STT, "Mã hàng hóa / Nhân viên / Khách hàng", Hành động.',
     '—',
     '- Ba cột này có ô tích mờ (hai cột đầu có biểu tượng ổ khóa), không bỏ tích được.'),
    ('010', 'Tuỳ chỉnh cột được nhớ', 'P2',
     'Đã tắt cột Model và lưu.',
     '1. Tải lại trang.\n2. Đăng xuất, đăng nhập lại, mở màn.',
     '—',
     '- Cột Model vẫn bị ẩn.'),
]

S4 = [
    ('001', 'Mở chi tiết một hàng hóa', 'P0',
     'PULI-KU-DP7 do 7 nhân viên giữ: Đàm Phước Nhiên (Phòng KD Khu vực 2, 1 lô), Đỗ Văn Chính, '
     'Đỗ Văn Sáng, Hồ Ngọc Tiến (2 lô)…',
     '1. Bấm nút ">" ở dòng PULI-KU-DP7.',
     '—',
     '- Nút quay trong lúc tải rồi đổi thành "v".\n'
     '- Dưới dòng hàng hóa chèn các dòng nhân viên (nền xanh lá nhạt, biểu tượng người) và dòng '
     'khách hàng (nền xanh dương nhạt, biểu tượng cửa hàng).\n'
     '- Dòng Đàm Phước Nhiên: cột Tên hàng hóa / Phòng ban ghi "Phòng KD Khu vực 2", SL giữ 1.'),
    ('002', 'Dòng khách hàng hiển thị đủ thông tin lô', 'P0',
     'Lô của Đàm Phước Nhiên cho khách 47TDAPTA-75, SL 1, hạn giữ 24/09/2026. Hôm nay '
     '05/10/2026.',
     '1. Mở chi tiết PULI-KU-DP7.\n2. Cuộn ngang sang phải, đọc dòng khách 47TDAPTA-75.',
     '—',
     '- Cột đầu: "47TDAPTA-75 - CÔNG TY TNHH MTV THUẬN PHÚC".\n'
     '- SL giữ 1, Hạn giữ 24/09/2026.\n'
     '- Trạng thái badge đỏ "Hết hạn".\n'
     '- Cột Hành động có nút biểu tượng đồng hồ.'),
    ('003', 'Tầng nhân viên và hàng hóa không có hạn giữ', 'P1',
     'Đang mở chi tiết PULI-KU-DP7.',
     '1. Đọc các cột Đơn vị, Model, Thương hiệu, Tổng SL trong kho, Hạn giữ, Trạng thái, Hành '
     'động ở dòng nhân viên.',
     '—',
     '- Các ô này để TRỐNG (không có dấu gạch).\n'
     '- Dòng hàng hóa cũng không có Hạn giữ, Trạng thái, nút Lịch sử.'),
    ('004', 'Tổng tầng nhân viên khớp các lô', 'P0',
     'Hồ Ngọc Tiến giữ 2 lô PULI-KU-DP7 cho 2 khách, mỗi lô SL 1.',
     '1. Mở chi tiết PULI-KU-DP7.\n2. So SL giữ dòng Hồ Ngọc Tiến với tổng các dòng khách của '
     'ông.',
     '—',
     '- SL giữ dòng nhân viên = 2 = 1 + 1.\n'
     '- Tổng SL giữ mọi dòng nhân viên = SL giữ dòng hàng hóa (17).'),
    ('005', 'Thứ tự trong cây', 'P2',
     'PULI-KU-DP7 có nhiều nhân viên và nhiều lô.',
     '1. Mở chi tiết.\n2. Đọc thứ tự dòng nhân viên và dòng khách.',
     '—',
     '- Nhân viên sắp theo họ tên.\n'
     '- Trong mỗi nhân viên, lô sắp theo tên khách hàng rồi hạn giữ.'),
    ('006', 'Chi tiết áp cùng bộ lọc với tầng hàng hóa', 'P0',
     'PULI-KU-DP7 có lô cho khách 15TPHPLE-4 và nhiều khách khác.',
     '1. Gõ "15TPHPLE-4" vào ô tìm nhanh, bấm Tìm kiếm.\n2. Mở chi tiết PULI-KU-DP7.',
     'Ô tìm nhanh: 15TPHPLE-4',
     '- Chi tiết chỉ có khách 15TPHPLE-4 và nhân viên giữ lô đó.\n'
     '- Không xuất hiện khách khác (hệ thống cũ bị lỗi hiện đủ mọi khách).'),
    ('007', 'Thu gọn và mở lại', 'P1',
     'Đang mở chi tiết PULI-KU-DP7.',
     '1. Bấm "v".\n2. Bấm ">" lần nữa.',
     '—',
     '- Bước 1: các dòng con biến mất.\n'
     '- Bước 2: hiện lại ngay, không có biểu tượng quay (dùng dữ liệu đã tải).'),
    ('008', 'Mở nhiều hàng hóa cùng lúc', 'P2',
     'Trang 1 có PULI-KU-DP5 và PULI-KU-DP7.',
     '1. Mở chi tiết cả hai.',
     '—',
     '- Cả hai cùng mở, dòng con nằm đúng dưới hàng hóa của mình.'),
    ('009', 'Đổi bộ lọc thu gọn mọi chi tiết', 'P2',
     'Đang mở chi tiết PULI-KU-DP7.',
     '1. Chọn Trạng thái = Trong hạn.',
     'Trạng thái: Trong hạn',
     '- Danh sách nạp lại, mọi hàng hóa đều thu gọn.'),
    ('010', 'Trạng thái đổi theo ngày', 'P0',
     'Lô L hạn giữ 06/10/2026.',
     '1. Ngày 05/10/2026 xem trạng thái lô L.\n2. Ngày 06/10/2026 xem lại.\n3. Ngày 07/10/2026 '
     'xem lại.',
     '—',
     '- 05/10: "Trong hạn" (xanh lá).\n- 06/10: "Đến hạn" (vàng).\n- 07/10: "Hết hạn" (đỏ).'),
    ('011', 'Đổi đơn vị hiển thị', 'P0',
     'Hàng hóa H có đơn vị cơ bản Cái và đơn vị Hộp hệ số 10. H đang bị giữ 25 Cái, Tổng SL '
     'trong kho 103 Cái.',
     '1. Ở dòng H mở ô Đơn vị.\n2. Chọn "Hộp (x10)".\n3. Mở chi tiết H.',
     'Đơn vị: Hộp (x10)',
     '- Danh sách đơn vị có "Cái" đứng đầu và "Hộp (x10)".\n'
     '- SL giữ hiện 2.5; Tổng SL trong kho hiện 10.3.\n'
     '- SL giữ ở dòng nhân viên và dòng khách cũng chia cho 10.'),
    ('012', 'Đổi đơn vị làm tròn xuống', 'P1',
     'Hàng hóa H đơn vị Thùng hệ số 3. SL giữ 10 đơn vị cơ bản.',
     '1. Chọn đơn vị Thùng.',
     'Đơn vị: Thùng (x3)',
     '- SL giữ hiện 3.33 (làm tròn xuống, không phải 3.34).'),
    ('013', 'Hàng hóa chỉ có một đơn vị', 'P2',
     'Hàng hóa SG-MN-HB-XD0107 chỉ có đơn vị "Cái.".',
     '1. Quan sát cột Đơn vị của dòng này.',
     '—',
     '- Hiện chữ "Cái.", không có ô chọn.'),
    ('014', 'Đổi đơn vị không được lưu', 'P2',
     'Đã đổi H sang Hộp.',
     '1. Tải lại trang.',
     '—',
     '- Dòng H quay về đơn vị cơ bản Cái.'),
]

S5 = [
    ('001', 'Mở cửa sổ Lịch sử giữ hàng', 'P0',
     'Lô PULI-KU-DP7 của nhân viên 21710653 - Đàm Phước Nhiên cho khách 47TDAPTA-75, hạn giữ '
     '24/09/2026, SL 1 Bộ.',
     '1. Mở chi tiết PULI-KU-DP7.\n2. Bấm nút đồng hồ ở dòng khách 47TDAPTA-75.',
     '—',
     '- Cửa sổ "Lịch sử giữ hàng", dòng phụ "Hàng hóa: PULI-KU-DP7 - Bàn nâng cắt kéo di động '
     '1.2 tấn…".\n'
     '- Mã hàng PULI-KU-DP7; Kinh doanh "21710653 - Đàm Phước Nhiên"; Khách hàng "47TDAPTA-75 - '
     'CÔNG TY TNHH MTV THUẬN PHÚC".\n'
     '- Trạng thái badge "Hết hạn" kèm "(Hạn giữ hiện tại: 24/09/2026)".\n'
     '- Dòng "Số lượng giữ hiện tại: 1 Bộ".'),
    ('002', 'Bảng biến động', 'P0',
     'Lô trên có 1 lần tăng +1 ngày 14/09/2026 từ chứng từ PPBHĐC-01438.',
     '1. Đọc bảng trong cửa sổ.',
     '—',
     '- Các cột: STT, SL biến động, Ngày, SL giữ, Hạn giữ, Chứng từ.\n'
     '- Dòng 1: "+1" chữ xanh lá, 14/09/2026, SL giữ 1, Hạn giữ 24/09/2026, chứng từ '
     'PPBHĐC-01438 là liên kết.'),
    ('003', 'Sổ biến động sắp từ cũ đến mới, SL giữ cộng dồn', 'P0',
     'Lô M: ngày 01/09 xuất giữ +10 (PXG-02132), ngày 10/09 hủy -6 (PHHG), ngày 20/09 gia hạn '
     '(PGHHG-01580).',
     '1. Mở Lịch sử giữ hàng của lô M.',
     '—',
     '- Dòng 1 là ngày 01/09 (+10, SL giữ 10), dòng 2 là 10/09 (-6 chữ đỏ, SL giữ 4).\n'
     '- Dòng gia hạn hiện chứng từ PGHHG-01580.\n'
     '- Lưu ý: sắp CŨ > MỚI là có chủ đích, không ghi Failed.'),
    ('004', 'Bấm mã chứng từ', 'P1',
     'Đang mở lịch sử có chứng từ PXG-02132.',
     '1. Bấm PXG-02132.',
     '—',
     '- Mở màn chi tiết Phiếu xuất giữ PXG-02132 ở thẻ mới; cửa sổ lịch sử vẫn mở ở thẻ cũ.'),
    ('005', 'Lịch sử theo đơn vị đang chọn', 'P1',
     'Hàng hóa H đơn vị Hộp hệ số 10; lô có biến động +20 Cái.',
     '1. Đổi đơn vị dòng H sang Hộp.\n2. Mở lịch sử một lô của H.',
     'Đơn vị: Hộp (x10)',
     '- SL biến động hiện "+2"; dòng "Số lượng giữ hiện tại: … Hộp".'),
    ('006', 'Lô chưa có biến động', 'P2',
     'Lô N không có dòng biến động nào.',
     '1. Mở Lịch sử giữ hàng của lô N.',
     '—',
     '- Bảng hiện "Chưa có biến động nào.".'),
    ('007', 'Đóng cửa sổ', 'P2',
     'Đang mở cửa sổ Lịch sử giữ hàng.',
     '1. Bấm Đóng.\n2. Mở lại, bấm dấu ×.',
     '—',
     '- Cửa sổ đóng, bảng chi tiết vẫn đang mở như trước.'),
    ('008', 'Lỗi khi tải lịch sử', 'P2',
     'Mạng chập chờn khi mở lịch sử.',
     '1. Mở Lịch sử giữ hàng khi mất mạng.\n2. Có mạng lại, bấm "Thử lại".',
     '—',
     '- Bước 1: "Không tải được lịch sử giữ hàng." kèm nút "Thử lại".\n'
     '- Bước 2: bảng hiện bình thường.'),
]

S6 = [
    ('001', 'Mở cửa sổ chọn trường xuất Excel', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm "Xuất Excel".',
     '—',
     '- Cửa sổ "Chọn trường xuất Excel" với dòng "Tích chọn trường cần xuất, kéo để đổi thứ tự cột '
     'trong file.".\n'
     '- 12 trường tích sẵn: Mã hàng hóa, Tên hàng hóa, ĐVT, Model, Thương hiệu, Nhân viên giữ, '
     'Phòng ban, Khách hàng, SL giữ, Tổng SL trong kho, Hạn giữ, Trạng thái.\n'
     '- Dòng cuối "Đang chọn 12/12 trường"; nút "Xuất file" và "Đóng".'),
    ('002', 'Xuất đủ 12 trường', 'P0',
     'Đang lọc Thương hiệu = KOISU; có 40 lô khớp.',
     '1. Bấm "Xuất Excel".\n2. Bấm "Xuất file".\n3. Mở tệp danh_sach_hang_giu.xlsx.',
     'Thương hiệu: KOISU',
     '- Phần mềm báo "Xuất Excel thành công", cửa sổ đóng.\n'
     '- Dòng 1 "DANH SÁCH HÀNG GIỮ"; dòng 2 tên cột, cột đầu là STT.\n'
     '- 40 dòng dữ liệu, mỗi dòng một lô, toàn bộ thương hiệu KOISU.'),
    ('003', 'Tệp là bảng phẳng mỗi dòng một lô', 'P0',
     'PULI-KU-DP7 có 17 lô (SL 1 mỗi lô), Tổng SL trong kho 41.',
     '1. Lọc Mã hàng hóa = PULI-KU-DP7.\n2. Xuất Excel đủ trường.',
     'Mã hàng hóa: PULI-KU-DP7',
     '- Tệp có 17 dòng, mỗi dòng ghi Nhân viên giữ, Phòng ban, Khách hàng, SL giữ, Hạn giữ, Trạng '
     'thái của một lô.\n'
     '- Cột Tổng SL trong kho ghi 41 trên CẢ 17 dòng (không cộng dọc).'),
    ('004', 'Thứ tự cột theo thứ tự chọn', 'P1',
     'Đang mở cửa sổ chọn trường.',
     '1. Bấm "Bỏ chọn hết".\n2. Tích lần lượt Khách hàng, Mã hàng hóa, SL giữ.\n3. Bấm Xuất file.',
     '—',
     '- Dòng cuối ghi "Đang chọn 3/12 trường".\n'
     '- Tệp có cột: STT, Khách hàng, Mã hàng hóa, SL giữ — đúng thứ tự.'),
    ('005', 'Kéo thả đổi thứ tự trường', 'P2',
     'Đang mở cửa sổ chọn trường, tích đủ 12.',
     '1. Kéo "Trạng thái" lên đầu.\n2. Xuất file.',
     '—',
     '- Cột thứ hai trong tệp (sau STT) là Trạng thái.'),
    ('006', 'Số lượng trong tệp theo đơn vị cơ bản', 'P0',
     'Hàng hóa H giữ 25 Cái, đang chọn hiển thị Hộp (x10) trên màn.',
     '1. Lọc hàng hóa H.\n2. Xuất Excel.',
     '—',
     '- Cột ĐVT ghi "Cái"; tổng cột SL giữ = 25 (không phải 2.5).'),
    ('007', 'Định dạng số và ngày trong tệp', 'P1',
     'Có lô SL 1,250 và hạn giữ 13/10/2026.',
     '1. Xuất Excel.\n2. Kiểm tra ô SL giữ và Hạn giữ.',
     '—',
     '- Ô SL giữ là số thật hiển thị "1,250", không có cảnh báo số dạng chữ.\n'
     '- Hạn giữ hiển thị "13/10/2026".\n'
     '- Ô không có dữ liệu để trống.'),
    ('008', 'Thứ tự dòng trong tệp', 'P2',
     'Đang sắp SL giữ giảm dần trên màn.',
     '1. Xuất Excel.',
     '—',
     '- Dòng trong tệp sắp theo Phòng ban > Nhân viên > Tên hàng hóa, không theo thứ tự trên màn.'),
    ('009', 'Chặn bấm hai lần khi đang xuất', 'P1',
     'Không lọc gì, dữ liệu lớn (khoảng 2,450 lô).',
     '1. Bấm Xuất file.\n2. Trong lúc đang xử lý bấm tiếp Xuất file và nút Xuất Excel.',
     '—',
     '- Hai nút bị khóa trong lúc xuất.\n- Chỉ tải về đúng 1 tệp.'),
    ('010', 'Đóng cửa sổ không xuất', 'P2',
     'Đang mở cửa sổ chọn trường.',
     '1. Bấm Đóng.',
     '—',
     '- Cửa sổ đóng, không tải tệp.'),
]

S7 = [
    ('001', 'Mở xem trước bản in', 'P0',
     'Tài khoản F, đang lọc Trạng thái = Hết hạn.',
     '1. Bấm "In".',
     'Trạng thái: Hết hạn',
     '- Cửa sổ "Xem trước danh sách hàng giữ" mở ngay trên màn, có nút In.\n'
     '- Bản in khổ ngang có tiêu đề công ty, dòng "DANH SÁCH HÀNG GIỮ".\n'
     '- Khối thông tin: Ngày in = ngày hôm nay, Số phòng ban, Số nhân viên, Số mục hàng.\n'
     '- Mọi dòng mục hàng có Trạng thái "Hết hạn".'),
    ('002', 'Bố cục gom Phòng ban > Nhân viên > Mục hàng', 'P0',
     'Phòng "Bộ Phận Hỗ trợ kinh doanh SG" có 2 nhân viên giữ 153 mục; Nguyễn Ngọc Hoa giữ 118 '
     'mục.',
     '1. Mở xem trước bản in.\n2. Đọc các dòng đầu bảng.',
     '—',
     '- Các cột: STT, Tên hàng hóa, Mã hàng, ĐVT, SL giữ, Hạn giữ, Khách hàng, Trạng thái.\n'
     '- Dòng "1": "Bộ Phận Hỗ trợ kinh doanh SG - 2 nhân viên - 153 mục hàng".\n'
     '- Dòng "1.1": "Nguyễn Ngọc Hoa - 118 mục hàng".\n'
     '- Dòng "1.1.1", "1.1.2"… là từng mục hàng.'),
    ('003', 'Số liệu tổng của bản in khớp dữ liệu', 'P0',
     'Bộ lọc mặc định, tài khoản F: 21 phòng ban, 88 nhân viên, 2,447 lô.',
     '1. Mở xem trước bản in.\n2. Xuất Excel cùng bộ lọc, đếm số dòng.',
     '—',
     '- Ngày in hôm nay; Số phòng ban 21; Số nhân viên 88; Số mục hàng 2,447.\n'
     '- Số mục hàng = số dòng dữ liệu tệp Excel.'),
    ('004', 'Số lượng bản in theo đơn vị cơ bản', 'P1',
     'Hàng hóa H giữ 25 Cái, đang hiển thị Hộp trên màn.',
     '1. Lọc H.\n2. Mở xem trước bản in.',
     '—',
     '- ĐVT "Cái", SL giữ 25.'),
    ('005', 'Nhân viên chưa gán phòng ban', 'P2',
     'Nhân viên R đang giữ hàng nhưng chưa có phòng ban.',
     '1. Lọc Nhân viên = R.\n2. Mở xem trước bản in.',
     'Nhân viên: R',
     '- Dòng cấp 1 ghi "Chưa gán phòng ban" kèm số nhân viên và số mục hàng.'),
    ('006', 'Bản in không có dữ liệu', 'P2',
     'Bộ lọc không khớp lô nào.',
     '1. Gõ "XYZ" vào Mã hàng hóa.\n2. Bấm In.',
     'Mã hàng hóa: XYZ',
     '- Bảng in có một dòng "Không có dữ liệu"; Số mục hàng = 0.'),
    ('007', 'Vượt mức in tối đa', 'P0',
     'Có thể dựng dữ liệu vượt 10,000 dòng in (phòng ban + nhân viên + lô).',
     '1. Bỏ mọi bộ lọc.\n2. Bấm In.',
     '—',
     '- Cửa sổ hiện "Danh sách có … dòng, vượt mức in tối đa 10,000 dòng nên chưa in được. Vui '
     'lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho '
     'danh sách dài.".\n'
     '- Không có nút In trong cửa sổ.'),
    ('008', 'Gửi lệnh in và đóng', 'P1',
     'Đang mở xem trước bản in.',
     '1. Bấm nút In trong cửa sổ.\n2. Hủy hộp thoại in của trình duyệt.\n3. Bấm dấu ×.',
     '—',
     '- Hộp thoại in của trình duyệt mở, khổ ngang.\n- Bấm × thì cửa sổ xem trước đóng.'),
]

S8 = [
    ('001', 'Màn không làm thay đổi hàng giữ', 'P0',
     'Lô L của PULI-KU-DP7 có SL 1, hạn giữ 24/09/2026.',
     '1. Mở chi tiết, mở lịch sử, đổi đơn vị, xuất Excel, in.\n2. Mở lại lịch sử lô L.',
     '—',
     '- Sổ biến động lô L không có dòng mới.\n- SL và hạn giữ lô L không đổi.'),
    ('002', 'Bảng, Excel và In ra cùng một tập dữ liệu', 'P0',
     'Lọc Thương hiệu = KOISU, Trạng thái = Hết hạn.',
     '1. Mở chi tiết mọi hàng hóa trên trang, cộng số dòng khách hàng (nếu ít hàng hóa).\n'
     '2. Xuất Excel, đếm số dòng.\n3. Mở xem trước bản in, đọc Số mục hàng.',
     'Thương hiệu: KOISU\nTrạng thái: Hết hạn',
     '- Ba con số bằng nhau.\n'
     '- Tổng SL giữ trên màn = tổng cột SL giữ trong Excel.'),
    ('003', 'Lô vừa bị hủy hết không còn hiện', 'P0',
     'Nhân viên S giữ 2 Cái hàng H cho khách K (lô duy nhất của H).',
     '1. Lập và duyệt phiếu hủy hàng giữ 2 Cái cho lô này ở màn Phiếu hủy hàng giữ.\n'
     '2. Quay lại Danh sách hàng giữ, lọc Mã hàng hóa = H.',
     '—',
     '- Hàng hóa H không còn trong danh sách (lô về 0 không hiện).'),
    ('004', 'Phạm vi công ty với Tổng SL trong kho', 'P0',
     'Hàng hóa H tồn kho kế toán 30 ở công ty 1, 20 ở công ty 4. Tài khoản E chỉ xem công ty 1.',
     '1. Đăng nhập E, đọc Tổng SL trong kho của H.\n2. Đăng nhập F (tổng công ty), đọc lại.',
     '—',
     '- E thấy 30.\n- F thấy 50; chọn Công ty = công ty 4 thì thấy 20.'),
]

S9 = [
    ('001', 'Luồng đầu cuối: xuất giữ > xem > gia hạn > hủy', 'P0',
     'Nhân viên S có hàng H trong kho. Tài khoản quản lý B có "Quản lý giữ hàng".',
     '1. Lập và duyệt Phiếu xuất giữ 5 Cái hàng H cho khách K, hạn giữ 10/10/2026.\n'
     '2. B mở Danh sách hàng giữ, tìm H, mở chi tiết.\n'
     '3. Gia hạn lô sang 20/10/2026 qua màn Yêu cầu gia hạn hàng giữ, duyệt.\n'
     '4. Hủy 2 Cái qua màn Phiếu hủy hàng giữ.\n'
     '5. Mở lại Danh sách hàng giữ và Lịch sử giữ hàng của lô.',
     'SL xuất giữ: 5\nHạn giữ: 10/10/2026 > 20/10/2026\nSL hủy: 2',
     '- Sau bước 2: dòng S cho khách K SL 5, hạn 10/10/2026, Trong hạn.\n'
     '- Sau bước 5: SL 3, hạn 20/10/2026.\n'
     '- Lịch sử có lần lượt dòng +5 (PXG-…), dòng gia hạn (PGHHG-…), dòng -2 (PHHG-…), SL giữ '
     'cộng dồn 5 > 5 > 3.'),
    ('002', 'Luồng đầu cuối: lô quá hạn được phát hiện', 'P1',
     'Lô L hạn giữ hôm qua.',
     '1. Lọc Trạng thái = Hết hạn.\n2. Tìm lô L.\n3. Mở màn Hàng sắp hết hạn giữ, tìm lô L.',
     'Trạng thái: Hết hạn',
     '- Lô L có trong kết quả, badge "Hết hạn".\n'
     '- Lô L cũng có ở màn Hàng sắp hết hạn giữ (cùng nguồn dữ liệu).'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'CHI TIẾT NHÂN VIÊN – KHÁCH HÀNG & ĐƠN VỊ', S4),
    ('V', 'LỊCH SỬ GIỮ HÀNG', S5),
    ('VI', 'XUẤT EXCEL', S6),
    ('VII', 'IN DANH SÁCH', S7),
    ('VIII', 'TOÀN VẸN DỮ LIỆU', S8),
    ('IX', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S9),
]

build(output_file=os.path.join(BASE, 'testcase - Danh sach hang giu.xlsx'),
      sheet_name='Trang tính1',
      feature_name='Danh sách hàng giữ',
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
