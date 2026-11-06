# -*- coding: utf-8 -*-
"""Sinh testcase ERP "Kết chuyển chi phí phải trả" theo đúng mẫu testcase-yeu-cau-hach-toan-dich-vu.xlsx.
Giữ nguyên dòng 1-17 của mẫu (định dạng, công thức TEST SUMMARY, DV, CF), chỉ thay nội dung.
Chạy: python3 -I gen_testcase.py <mau.xlsx> <ra.xlsx>"""
import sys, copy, math
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

TEN = "Kết chuyển chi phí phải trả"
CHUNG = ('KD1-TPE có: NV-A, NV-B; KD2-TPE có NV-C. Số dư tài khoản 3351 đến 31/10/2026 của KD1-TPE: '
         'VV-01 = 5,000,000 (NV-A, HD-01: 3,000,000; NV-B, HD-02: 2,000,000)')

MO_TA = {
2: ('Kết chuyển chi phí phải trả: cuối kỳ, kế toán chuyển số dư chi phí phải trả (tài khoản 3351) của một phòng ban theo từng vụ việc sang tài khoản phải trả nhân viên (33481).\n'
    'Người dùng làm được: xem danh sách, lập phiếu (lưu là ghi sổ luôn, không qua bước duyệt), xem chi tiết phiếu. Màn không có Sửa, Xóa, In, Xuất excel.', 66),
3: ('- Danh sách theo quyền: quyền tổng công ty thấy tất cả; quyền công ty thấy phiếu có Phòng ban thuộc công ty mình; không có quyền xem thì chỉ thấy phiếu mình lập.\n'
    '- Số tiền một vụ việc = tổng (Có - Nợ) tài khoản 3351 của các bút toán có nhân viên và hợp đồng, hợp đồng là Hợp đồng hãng hoặc Hợp đồng dịch vụ có xuất hóa đơn, phòng của nhân viên ghi trên bút toán = Phòng ban đã chọn, ngày hạch toán thuộc Năm đã chọn và không sau Tình đến ngày.', 99.95),
4: ('- Bút toán của hợp đồng không xuất hóa đơn; bút toán không gắn nhân viên hoặc hợp đồng; bút toán của hợp đồng loại khác.\n'
    '- Bút toán của năm trước (không chuyển số dư sang năm sau) hoặc sau Tình đến ngày.\n'
    '- Vụ việc đã khóa và phòng ban đã đóng không có trong danh sách chọn.\n'
    '- Bút toán kết chuyển không tính vào các báo cáo hoa hồng, thưởng, kế hoạch doanh số.', 83.1),
5: ('Ô Từ ngày / Đến ngày ở Bộ lọc lọc theo Ngày tạo phiếu, không theo Đến ngày hay Ngày hạch toán của phiếu.\n'
    'Lưu ý: theo code hiện tại ô Đến ngày không gồm phiếu tạo trong chính ngày đó (xem mục 9).', 48.95),
6: ('Bộ lọc: Số tiền từ, Số tiền đến, Số phiếu, Người lập, Vụ việc, Phòng ban, Từ ngày / Đến ngày.\n'
    'Bảng: STT, Số phiếu (mã dạng <mã công ty người lập>.KCCPPT<năm>.xxxxx), Đến ngày, Ngày hạch toán, Phòng ban, Số tiền kết chuyển, Người tạo, Ngày tạo. Phiếu mới nhất lên đầu.\n'
    'Form: Năm, Tình đến ngày, Ngày hạch toán (tự bằng Tình đến ngày, không sửa được), Phòng ban, Ghi chú; bảng Chi tiết: STT, Mã vụ việc, Tài khoản nợ 3351, Tài khoản có 33481, Số tiền (tự tính, không sửa được).', 99.95),
7: ('- Mỗi vụ việc chỉ được chọn một lần trong phiếu.\n'
    '- Bút toán gộp theo hợp đồng + nhân viên ở dòng 3351 và theo nhân viên + vụ việc ở dòng 33481; dòng có số tiền 0 thì bỏ qua.\n'
    '- Số dương: Nợ 3351 / Có 33481. Số âm: Có 3351 / Nợ 33481.\n'
    '- Lập lại cùng vụ việc sau khi đã kết chuyển: chỉ còn phần mới phát sinh.', 83.1),
8: ('- Xem danh sách: mọi người đăng nhập mở được, dữ liệu theo quyền "Xem kết chuyển chi phí phải trả theo tổng công ty", "Xem kết chuyển chi phí phải trả theo công ty".\n'
    '- Lập phiếu: quyền "Tạo kết chuyển chi phí phải trả".\n'
    '- Xem chi tiết: Super Admin, người lập, quyền tổng công ty, quyền công ty khi Phòng ban thuộc công ty mình. Không đủ quyền thì ra trang không tìm thấy.\n'
    '- Người có quyền xem theo công ty chỉ chọn được phòng của công ty mình khi lập; người khác chọn được phòng của mọi công ty.\n'
    'Các TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật.', 117),
9: ('- Số tiền từng vụ việc lấy theo số dư lúc chọn vụ việc, không có dòng tổng trên form.\n'
    '- Số tiền kết chuyển ở danh sách = tổng Số tiền các dòng chi tiết.\n'
    '- Đổi Năm, Tình đến ngày hoặc Phòng ban thì toàn bộ dòng chi tiết bị xóa, phải chọn lại.', 66),
10: ('Các bẫy dễ sai nhất (theo code hiện tại, ghi Failed nếu nghiệp vụ yêu cầu khác):\n'
    '- Sau khi đã kết chuyển đến ngày muộn, lập phiếu lùi về ngày sớm hơn vẫn ra số tiền cũ và ghi sổ lần hai, số dư 3351 bị âm.\n'
    '- Hai tab cùng lập một vụ việc: phiếu sau vẫn lưu với số tiền cũ nhưng không sinh bút toán, phiếu lệch sổ.\n'
    '- Lọc Số tiền từ, Số tiền đến, Vụ việc không có tác dụng; Đến ngày không gồm phiếu tạo trong ngày đó.\n'
    '- Bấm sắp xếp cột Phòng ban thì bảng báo lỗi.\n'
    '- Người có quyền công ty lập phiếu cho phòng công ty khác thì không thấy phiếu đó ở danh sách; phiếu của phòng đã đóng thì mất khỏi danh sách.\n'
    '- Lưu phiếu không kiểm tra quyền Tạo khi gọi thẳng.\n'
    '- Ghi chú ở màn chi tiết gõ được nhưng không lưu; nhãn "Tình đến ngày" sai chính tả.', 150.95),
}

S = []  # (tiêu đề section, nhóm, danh sách TC)
def sec(title, group, rows): S.append((title, group, rows))

sec("Phân quyền & truy cập", "Phân quyền & truy cập", [
("Không có quyền xem chỉ thấy phiếu mình lập","P0",'KT-T chỉ có quyền "Tạo kết chuyển chi phí phải trả", đã lập 1 phiếu; KT-1 lập 3 phiếu','1. Đăng nhập KT-T\n2. Mở menu Kế toán > Kết chuyển cuối kỳ > bấm "Kết chuyển chi phí phải trả"','Tài khoản: KT-T','- Danh sách chỉ có 1 phiếu của KT-T'),
("Quyền xem theo công ty thấy phiếu của phòng trong công ty","P0",'KT-1 thuộc TPE có quyền "Xem kết chuyển chi phí phải trả theo công ty"; phòng TPE có 5 phiếu, phòng TPC có 2 phiếu','1. Đăng nhập KT-1, mở màn từ menu','Tài khoản: KT-1','- Thấy 5 phiếu của phòng TPE, không thấy 2 phiếu của phòng TPC'),
("Quyền xem theo tổng công ty thấy tất cả","P0",'KT-TCT có quyền "Xem kết chuyển chi phí phải trả theo tổng công ty"; TPE có 5 phiếu, TPC có 2 phiếu','1. Đăng nhập KT-TCT, mở màn từ menu','Tài khoản: KT-TCT','- Thấy đủ 7 phiếu của cả TPE và TPC'),
("Không có quyền nào vẫn mở được danh sách","P1",'NV-A không có quyền nào của màn và chưa lập phiếu nào','1. Đăng nhập NV-A, mở màn từ menu','Tài khoản: NV-A','- Màn mở được, bảng trống\n- Không có nút Thêm mới'),
("Nút Thêm mới chỉ hiện khi có quyền Tạo","P0",'KT-1 có quyền Tạo; KT-TCT chỉ có quyền xem theo tổng công ty','1. Đăng nhập KT-1, xem nút trên danh sách\n2. Đăng nhập KT-TCT, xem nút trên danh sách','—','- KT-1 thấy nút Thêm mới\n- KT-TCT không thấy nút Thêm mới'),
("Không có quyền Tạo mở màn lập phiếu bằng đường dẫn","P0",'KT-TCT không có quyền Tạo; lấy đường dẫn màn lập phiếu từ tài khoản KT-1','1. Đăng nhập KT-TCT\n2. Dán đường dẫn màn "Tạo kết chuyển chi phí phải trả"','—','- Ra trang không tìm thấy'),
("Lưu phiếu khi không có quyền Tạo (gọi thẳng)","P0",'NV-A không có quyền Tạo; '+CHUNG,'1. Dùng công cụ kiểm thử API với phiên đăng nhập NV-A\n2. Gửi yêu cầu lưu phiếu cho KD1-TPE, VV-01, 5,000,000','Tài khoản: NV-A','- Mong đợi: bị từ chối, không có phiếu mới\n- Lưu ý: theo code hiện tại phiếu vẫn lưu thành công và ghi sổ - ghi Failed'),
("Xem chi tiết phiếu ngoài phạm vi","P0",'Phiếu P-TPC của phòng TPC do KT-2 lập; KT-T chỉ có quyền Tạo; KT-1 có quyền theo công ty TPE','1. Đăng nhập KT-T, mở đường dẫn chi tiết P-TPC\n2. Đăng nhập KT-1, mở đường dẫn chi tiết P-TPC','—','- Cả 2 tài khoản đều ra trang không tìm thấy'),
("Xem chi tiết phiếu trong phạm vi","P1",'Phiếu P-TPE của phòng KD1-TPE do KT-1 lập; KT-3 thuộc TPE có quyền theo công ty; KT-TCT có quyền tổng công ty','1. Lần lượt đăng nhập KT-1, KT-3, KT-TCT, Super Admin\n2. Mở chi tiết P-TPE','—','- Cả 4 tài khoản đều xem được'),
("Quyền công ty lập phiếu cho phòng công ty khác không thấy ở danh sách","P1",'KT-T2 có quyền Tạo và thuộc TPE, không có quyền xem theo công ty, đã lập phiếu cho KD1-TPC; sau đó được gán thêm quyền "Xem kết chuyển chi phí phải trả theo công ty"','1. Đăng nhập KT-T2, mở danh sách\n2. Tìm phiếu vừa nói theo Số phiếu','Tài khoản: KT-T2','- Mong đợi: người lập luôn thấy phiếu mình lập\n- Lưu ý: theo code hiện tại phiếu không có trong danh sách dù vẫn mở được chi tiết bằng đường dẫn - ghi Failed'),
("Phiếu của phòng đã đóng với quyền công ty","P1",'Phòng PD-TPE của TPE đã đóng, có 1 phiếu do KT-3 lập; KT-1 có quyền theo công ty TPE','1. Đăng nhập KT-1, mở danh sách\n2. Mở đường dẫn chi tiết phiếu đó','—','- Mong đợi: vẫn tra được phiếu cũ của công ty mình\n- Lưu ý: theo code hiện tại phiếu không có ở danh sách và chi tiết ra trang không tìm thấy - ghi Failed'),
])

sec("I. HIỂN THỊ TRANG & TRUY CẬP","HIỂN THỊ TRANG & TRUY CẬP",[
("Mở màn từ menu","P0",'Đăng nhập KT-1','1. Mở menu Kế toán > Kết chuyển cuối kỳ > bấm "Kết chuyển chi phí phải trả"','—','- Tiêu đề "Kết chuyển chi phí phải trả"\n- Có nút Bộ lọc, Thêm mới và bảng danh sách'),
("Đủ cột trong bảng","P0",'Có ít nhất 1 phiếu','1. Xem tiêu đề bảng','—','- Đúng thứ tự: STT, Số phiếu, Đến ngày, Ngày hạch toán, Phòng ban, Số tiền kết chuyển, Người tạo, Ngày tạo'),
("Không có chức năng ngoài phạm vi","P1",'Đăng nhập Super Admin','1. Xem nút trên danh sách và trên từng dòng','—','- Không có nút Sửa, Xóa, In, Xuất excel và không có cột Hành động'),
("Bảng trống","P2",'Tài khoản KT-T chưa lập phiếu nào','1. Mở danh sách','—','- Bảng báo không có dữ liệu, không lỗi'),
("Mở màn lập phiếu","P0",'Đăng nhập KT-1','1. Bấm Thêm mới','—','- Tiêu đề "Tạo kết chuyển chi phí phải trả"\n- Có khối Thông tin chung và Chi tiết\n- Có nút "Lưu và duyệt", "Hủy"'),
("Nhãn ô ngày trên form","P2",'Đăng nhập KT-1','1. Mở màn lập phiếu, đọc nhãn ô thứ 2','—','- Mong đợi: "Tính đến ngày"\n- Lưu ý: theo code hiện tại nhãn là "Tình đến ngày" - ghi Failed'),
("Nút Hủy trên màn lập phiếu","P1",'Đang nhập dở form','1. Chọn Năm, Phòng ban\n2. Bấm Hủy','—','- Quay về danh sách, không có phiếu mới'),
])

sec("II. BỘ LỌC & TÌM KIẾM","BỘ LỌC & TÌM KIẾM",[
("Mở khối Bộ lọc","P1",'Đăng nhập KT-TCT','1. Bấm Bộ lọc','—','- Hiện đủ ô: Số tiền từ, Số tiền đến, Số phiếu, Người lập, Vụ việc, Phòng ban, Từ ngày, Đến ngày'),
("Lọc theo Số phiếu đầy đủ","P0",'Có phiếu TPE.KCCPPT2026.00056','1. Nhập Số phiếu, bấm tìm kiếm','Số phiếu: TPE.KCCPPT2026.00056','- Chỉ ra 1 phiếu đó'),
("Lọc theo một phần Số phiếu","P1",'Có phiếu TPE.KCCPPT2026.00056 và TPC.KCCPPT2026.00010','1. Nhập một phần Số phiếu, bấm tìm kiếm','Số phiếu: KCCPPT2026.0005','- Ra các phiếu có chứa chuỗi đã nhập'),
("Lọc theo Người lập","P0",'KT-1 lập 3 phiếu, KT-2 lập 2 phiếu','1. Chọn Người lập KT-1, bấm tìm kiếm','Người lập: KT-1','- Ra đúng 3 phiếu của KT-1'),
("Lọc theo Phòng ban","P0",'KD1-TPE có 4 phiếu, KD2-TPE có 1 phiếu','1. Chọn Phòng ban KD1-TPE, bấm tìm kiếm','Phòng ban: KD1-TPE','- Ra đúng 4 phiếu của KD1-TPE'),
("Lọc Số tiền từ","P0",'Phiếu P1 = 500,000; P2 = 5,000,000','1. Nhập Số tiền từ, bấm tìm kiếm','Số tiền từ: 1,000,000','- Mong đợi: chỉ ra P2\n- Lưu ý: theo code hiện tại ô này không có tác dụng, vẫn ra cả 2 phiếu - ghi Failed'),
("Lọc Số tiền đến","P0",'Phiếu P1 = 500,000; P2 = 5,000,000','1. Nhập Số tiền đến, bấm tìm kiếm','Số tiền đến: 1,000,000','- Mong đợi: chỉ ra P1\n- Lưu ý: theo code hiện tại ô này không có tác dụng, vẫn ra cả 2 phiếu - ghi Failed'),
("Lọc theo Vụ việc","P0",'P1 có VV-01; P2 có VV-02','1. Chọn Vụ việc VV-01, bấm tìm kiếm','Vụ việc: VV-01','- Mong đợi: chỉ ra P1\n- Lưu ý: theo code hiện tại ô này không có tác dụng, vẫn ra cả 2 phiếu - ghi Failed'),
("Lọc Từ ngày theo Ngày tạo","P1",'P1 tạo 01/10/2026 (Đến ngày 30/09/2026); P2 tạo 05/11/2026','1. Nhập Từ ngày, bấm tìm kiếm','Từ ngày: 01/11/2026','- Chỉ ra P2'),
("Lọc Đến ngày đúng ngày tạo phiếu","P0",'Phiếu P2 tạo lúc 10:10 ngày 05/11/2026','1. Nhập Từ ngày và Đến ngày cùng 05/11/2026, bấm tìm kiếm','Từ ngày: 05/11/2026\nĐến ngày: 05/11/2026','- Mong đợi: ra P2\n- Lưu ý: theo code hiện tại không ra phiếu nào vì Đến ngày tính tới 00:00 của ngày đó - ghi Failed'),
("Kết hợp nhiều điều kiện","P1",'KT-1 có 2 phiếu của KD1-TPE, 1 phiếu của KD2-TPE','1. Chọn Người lập KT-1, Phòng ban KD1-TPE, bấm tìm kiếm','—','- Ra đúng 2 phiếu thỏa cả hai điều kiện'),
("Không có kết quả","P2",'—','1. Nhập Số phiếu không tồn tại, bấm tìm kiếm','Số phiếu: ABC999','- Bảng báo không có dữ liệu'),
("Nút làm mới bộ lọc","P1",'Đang lọc theo Phòng ban KD1-TPE','1. Bấm nút làm mới cạnh nút tìm kiếm','—','- Các ô lọc về trống\n- Bảng hiện lại toàn bộ phiếu trong phạm vi quyền'),
("Giữ bộ lọc khi quay lại từ chi tiết","P2",'Đang lọc Phòng ban KD1-TPE, ở trang 2','1. Bấm Số phiếu để mở chi tiết\n2. Bấm Back trên trình duyệt','—','- Quay lại vẫn giữ bộ lọc và trang đang xem'),
("Danh sách Vụ việc và Phòng ban ở bộ lọc","P2",'VV-KHOA đã khóa; PD-TPE đã đóng','1. Mở ô Vụ việc, ô Phòng ban','—','- Không có VV-KHOA, không có PD-TPE'),
])

sec("III. DANH SÁCH & HÀNH ĐỘNG","DANH SÁCH & HÀNH ĐỘNG",[
("Thứ tự mặc định","P0",'Có phiếu tạo 01/10/2026 và 05/11/2026','1. Mở danh sách','—','- Phiếu tạo 05/11/2026 ở trên phiếu tạo 01/10/2026'),
("Dữ liệu từng cột đúng với phiếu","P0",'Phiếu P-TPE: KD1-TPE, Tình đến ngày 31/10/2026, 5,000,000, KT-1 tạo ngày 05/11/2026','1. Tìm P-TPE, đọc dòng','—','- Đến ngày 31/10/2026, Ngày hạch toán 31/10/2026\n- Phòng ban KD1-TPE, Số tiền kết chuyển 5,000,000\n- Người tạo KT-1, Ngày tạo 05/11/2026'),
("Số tiền âm hiển thị đúng","P1",'Phiếu có tổng -426,000','1. Tìm phiếu, đọc cột Số tiền kết chuyển','—','- Hiện -426,000'),
("Bấm Số phiếu mở chi tiết","P0",'Có phiếu P-TPE','1. Bấm Số phiếu','—','- Mở màn "Chi tiết kết chuyển chi phí phải trả" đúng phiếu'),
("Phân trang và STT","P1",'Có 25 phiếu','1. Mở danh sách\n2. Sang trang 2','—','- Mỗi trang 10 dòng\n- Trang 2 STT từ 11 đến 20'),
("Sắp xếp theo Số phiếu, Đến ngày, Ngày hạch toán, Số tiền kết chuyển, Ngày tạo","P1",'Có ít nhất 3 phiếu khác nhau','1. Bấm lần lượt từng tiêu đề cột 2 lần','—','- Bảng đổi đúng thứ tự tăng, giảm theo cột đã bấm'),
("Sắp xếp theo Phòng ban","P1",'Có ít nhất 3 phiếu','1. Bấm tiêu đề cột Phòng ban','—','- Mong đợi: sắp theo tên phòng\n- Lưu ý: theo code hiện tại bảng báo lỗi và không tải được dữ liệu, phải tải lại trang - ghi Failed'),
("Sắp xếp theo Người tạo","P2",'Có phiếu của nhiều người tạo','1. Bấm tiêu đề cột Người tạo','—','- Mong đợi: sắp theo tên người tạo\n- Lưu ý: theo code hiện tại sắp theo mã tài khoản nên tên không theo thứ tự chữ cái - ghi Failed'),
("Mở đường dẫn sửa, xóa phiếu","P2",'Có phiếu P-TPE; tester kỹ thuật','1. Dùng công cụ kiểm thử API gọi chức năng sửa, xóa của P-TPE','—','- Mong đợi: bị từ chối, phiếu không đổi\n- Lưu ý: chức năng chưa được làm, hệ thống báo lỗi kỹ thuật thay vì thông báo rõ ràng'),
])

sec("IV. LẬP PHIẾU - THÔNG TIN CHUNG","LẬP PHIẾU",[
("Giá trị mặc định","P0",'Ngày hiện tại thuộc năm 2026','1. Mở màn lập phiếu','—','- Năm = 2026\n- Tình đến ngày, Ngày hạch toán, Phòng ban trống\n- Bảng Chi tiết hiện "Không có dữ liệu"'),
("Danh sách Năm","P1",'Ngày hiện tại thuộc năm 2026','1. Mở ô Năm','—','- Có từ 2025 đến 2036'),
("Ngày hạch toán tự theo Tình đến ngày","P0",'Đang ở màn lập phiếu','1. Chọn Tình đến ngày\n2. Thử bấm vào ô Ngày hạch toán','Tình đến ngày: 31/10/2026','- Ngày hạch toán tự thành 31/10/2026\n- Ô Ngày hạch toán không sửa được'),
("Phòng ban với người có quyền xem theo công ty","P0",'KT-1 thuộc TPE có quyền Tạo và quyền xem theo công ty','1. Đăng nhập KT-1, mở ô Phòng ban','—','- Chỉ có phòng đang hoạt động của TPE'),
("Phòng ban với người chỉ có quyền Tạo","P1",'KT-T thuộc TPE chỉ có quyền Tạo','1. Đăng nhập KT-T, mở ô Phòng ban','—','- Mong đợi: chỉ chọn được phòng của công ty mình\n- Lưu ý: theo code hiện tại có phòng của mọi công ty - ghi Failed nếu nghiệp vụ yêu cầu giới hạn'),
("Phòng đã đóng không có trong ô Phòng ban","P1",'PD-TPE đã đóng','1. Mở ô Phòng ban','—','- Không có PD-TPE'),
("Thêm dòng khi chưa chọn Năm","P1",'Chọn lại ô Năm về "Chọn năm"','1. Bấm dấu + ở bảng Chi tiết','—','- Hiện cảnh báo "Chưa chọn năm", không thêm dòng'),
("Thêm dòng khi chưa chọn Tình đến ngày","P1",'Năm đã chọn, Tình đến ngày trống','1. Bấm dấu +','—','- Hiện cảnh báo "Chưa chọn tính đến ngày", không thêm dòng'),
("Thêm dòng khi chưa chọn Phòng ban","P1",'Đã chọn Năm và Tình đến ngày, Phòng ban trống','1. Bấm dấu +','—','- Hiện cảnh báo "Chưa chọn phòng ban", không thêm dòng'),
("Đổi Năm xóa dòng chi tiết","P0",'Đã chọn KD1-TPE, có 2 dòng VV-01, VV-02','1. Đổi Năm','Năm: 2025','- Toàn bộ dòng chi tiết bị xóa, bảng về "Không có dữ liệu"'),
("Đổi Tình đến ngày xóa dòng chi tiết","P0",'Đã chọn KD1-TPE, có 2 dòng VV-01, VV-02','1. Đổi Tình đến ngày','Tình đến ngày: 30/09/2026','- Toàn bộ dòng chi tiết bị xóa'),
("Đổi Phòng ban xóa dòng chi tiết","P0",'Đã chọn KD1-TPE, có 2 dòng VV-01, VV-02','1. Đổi Phòng ban','Phòng ban: KD2-TPE','- Toàn bộ dòng chi tiết bị xóa'),
("Dòng chi tiết cố định tài khoản","P1",'Đã bấm dấu + thêm 1 dòng','1. Xem dòng vừa thêm','—','- Tài khoản nợ 3351, Tài khoản có 33481\n- Số tiền không sửa được'),
("Xóa dòng chi tiết","P1",'Có 3 dòng','1. Bấm thùng rác ở dòng 2','—','- Dòng 2 bị xóa, STT đánh lại 1, 2\n- Dòng đầu tiên không có thùng rác'),
("Ô Mã vụ việc không có vụ việc đã khóa","P1",'VV-KHOA đã khóa','1. Mở ô Mã vụ việc','—','- Không có VV-KHOA'),
])

sec("V. TÍNH SỐ TIỀN KẾT CHUYỂN","TÍNH SỐ TIỀN",[
("Tổng hợp nhiều nhân viên, hợp đồng trong vụ việc","P0",CHUNG,'1. Chọn Năm 2026, Tình đến ngày 31/10/2026, Phòng ban KD1-TPE\n2. Thêm dòng, chọn VV-01','Mã vụ việc: VV-01','- Thông báo "Thêm thành công"\n- Số tiền = 5,000,000'),
("Lấy Có trừ Nợ","P0",'VV-07 của KD1-TPE: Có 3,300,000; Nợ 300,000 trong năm 2026','1. Thêm dòng, chọn VV-07','Mã vụ việc: VV-07','- Số tiền = 3,000,000'),
("Chỉ tính đến Tình đến ngày","P0",'VV-01: 3,000,000 ngày 20/03/2026; 2,000,000 ngày 10/10/2026','1. Chọn Tình đến ngày 31/03/2026\n2. Thêm dòng, chọn VV-01','—','- Số tiền = 3,000,000'),
("Bút toán đúng ngày Tình đến ngày được tính","P1",'VV-08 có Có 600,000 ngày 31/10/2026','1. Chọn Tình đến ngày 31/10/2026, thêm dòng VV-08','—','- Số tiền = 600,000'),
("Không cộng số dư năm trước","P0",'VV-05 của KD1-TPE: Có 1,500,000 ngày 15/12/2025 chưa kết chuyển; Có 400,000 ngày 05/10/2026','1. Chọn Năm 2026, Tình đến ngày 31/10/2026, thêm dòng VV-05','—','- Số tiền = 400,000\n- Lưu ý: 1,500,000 của năm 2025 không chuyển sang 2026, phải lập phiếu Năm 2025 riêng; ghi Failed nếu nghiệp vụ yêu cầu chuyển số dư'),
("Lập phiếu cho năm trước","P1",'VV-05 như trên','1. Chọn Năm 2025, Tình đến ngày 31/12/2025, thêm dòng VV-05','—','- Số tiền = 1,500,000'),
("Bỏ hợp đồng không xuất hóa đơn","P0",'VV-04 của KD1-TPE chỉ có bút toán 900,000 của HD-03 (Hợp đồng hãng không xuất hóa đơn)','1. Thêm dòng, chọn VV-04','—','- Số tiền = 0'),
("Tính cả Hợp đồng hãng và Hợp đồng dịch vụ","P0",'VV-09: HD-01 (Hợp đồng hãng, có hóa đơn) 1,000,000; HD-02 (Hợp đồng dịch vụ, có hóa đơn) 700,000','1. Thêm dòng, chọn VV-09','—','- Số tiền = 1,700,000'),
("Bỏ bút toán của hợp đồng loại khác","P1",'VV-10: HD-01 1,000,000; Đơn hàng nước ngoài DH-01 500,000','1. Thêm dòng, chọn VV-10','—','- Số tiền = 1,000,000'),
("Chỉ lấy theo phòng đã chọn","P0",'VV-06: NV-A (KD1-TPE) 800,000; NV-C (KD2-TPE) 700,000','1. Chọn Phòng ban KD2-TPE, thêm dòng VV-06','—','- Số tiền = 700,000'),
("Nhân viên đã chuyển phòng","P2",'NV-B có bút toán 600,000 khi còn ở KD1-TPE, sau đó chuyển sang KD2-TPE','1. Chọn KD1-TPE, thêm vụ việc có bút toán đó','—','- Số tiền vẫn tính 600,000 cho KD1-TPE theo phòng ghi trên bút toán'),
("Số dư âm","P0",'VV-02 của KD1-TPE: Nợ 1,200,000, không có Có','1. Thêm dòng, chọn VV-02','—','- Số tiền = -1,200,000'),
("Vụ việc có số dư bằng 0","P1",'VV-03: Có 800,000; Nợ 800,000','1. Thêm dòng, chọn VV-03','—','- Thông báo "Thêm thành công"\n- Số tiền = 0'),
("Chọn trùng vụ việc trên form","P0",'Dòng 1 đã chọn VV-01','1. Thêm dòng 2, chọn VV-01','—','- Thông báo "Vụ việc đã được chọn!"\n- Dòng 2 không có Số tiền'),
("Đổi vụ việc trên dòng đã có","P1",'Dòng 1 đang VV-01, Số tiền 5,000,000','1. Đổi Mã vụ việc dòng 1 thành VV-07','—','- Số tiền đổi thành 3,000,000'),
])

sec("VI. LƯU VÀ DUYỆT & BÚT TOÁN","LƯU VÀ DUYỆT & BÚT TOÁN",[
("Lưu phiếu hợp lệ","P0",CHUNG,'1. Đăng nhập KT-1, nhập Năm 2026, Tình đến ngày 31/10/2026, KD1-TPE, thêm VV-01\n2. Bấm "Lưu và duyệt"','Mã vụ việc: VV-01','- Thông báo "Tạo kết chuyển thành công!"\n- Quay về danh sách, phiếu mới ở đầu bảng với 5,000,000'),
("Số phiếu theo công ty người lập và Năm","P0",'KT-1 thuộc TPE; phiếu cuối của TPE năm 2026 là TPE.KCCPPT2026.00056','1. Lập phiếu Năm 2026 hợp lệ','—','- Số phiếu = TPE.KCCPPT2026.00057'),
("Số phiếu khi lập cho phòng công ty khác","P1",'KT-T thuộc TPE chỉ có quyền Tạo; KD1-TPC có số dư','1. Đăng nhập KT-T, lập phiếu cho KD1-TPC','—','- Số phiếu mang mã TPE, Phòng ban là KD1-TPC\n- Lưu ý: ghi Failed nếu nghiệp vụ yêu cầu mã theo công ty của phòng'),
("Số phiếu đánh riêng từng năm","P1",'Phiếu cuối TPE năm 2025 là TPE.KCCPPT2025.00066','1. Lập phiếu Năm 2025, Tình đến ngày 31/12/2025','—','- Số phiếu = TPE.KCCPPT2025.00067'),
("Tổng phiếu nhiều vụ việc","P0",'VV-01 = 5,000,000; VV-07 = 3,000,000','1. Thêm 2 dòng, lưu','—','- Số tiền kết chuyển ở danh sách = 8,000,000'),
("Bút toán số dương","P0",CHUNG,'1. Lưu phiếu VV-01\n2. Mở Kế toán > Sổ chi tiết các tài khoản, xem 3351 và 33481 theo Số phiếu','—','- Nợ 3351: 3,000,000 (NV-A, HD-01); 2,000,000 (NV-B, HD-02)\n- Có 33481: 3,000,000 (NV-A); 2,000,000 (NV-B)\n- Tổng Nợ = tổng Có = 5,000,000'),
("Bút toán số âm đảo chiều","P0",'VV-02 của KD1-TPE = -1,200,000 (NV-A, HD-01)','1. Lưu phiếu VV-02\n2. Xem Sổ chi tiết các tài khoản theo Số phiếu','—','- Phiếu lưu thành công với -1,200,000\n- Có 3351: 1,200,000; Nợ 33481: 1,200,000'),
("Một nhân viên có hợp đồng dương và âm","P1",'VV-11: NV-A, HD-01 = 3,000,000; NV-A, HD-05 = -1,000,000','1. Lưu phiếu VV-11, xem Sổ chi tiết các tài khoản','—','- Nợ 3351: 3,000,000 (HD-01); Có 3351: 1,000,000 (HD-05)\n- Có 33481: 2,000,000 (NV-A)'),
("Thông tin trên bút toán","P0",'KT-1 thuộc phòng KT-TPE lập phiếu VV-01 cho KD1-TPE','1. Lưu phiếu, xem dòng bút toán trên Sổ chi tiết các tài khoản','—','- Ngày hạch toán 31/10/2026\n- Có vụ việc VV-01, nhân viên, hợp đồng ở dòng 3351\n- Phòng nhân viên = KD1-TPE\n- Công ty, phòng ghi sổ theo người lập KT-1'),
("Số dư 3351 về 0 sau kết chuyển","P0",CHUNG,'1. Lưu phiếu VV-01\n2. Mở lại form, cùng Năm, Tình đến ngày, Phòng ban, thêm VV-01','—','- Số tiền = 0'),
("Phiếu thấy ở Sổ chi tiết công nợ nhân viên","P1",'Đã lưu phiếu VV-01','1. Mở Sổ chi tiết công nợ nhân viên, chọn NV-A, tài khoản 33481\n2. Bấm Số phiếu kết chuyển','—','- Có dòng phải trả 3,000,000\n- Bấm Số phiếu mở đúng màn chi tiết'),
("Lập phần phát sinh mới","P0",'VV-01 đã kết chuyển 5,000,000 đến 31/10/2026; ngày 03/11/2026 phát sinh thêm Có 200,000','1. Lập phiếu Tình đến ngày hôm nay, thêm VV-01, lưu','—','- Số tiền = 200,000\n- Bút toán chỉ có 200,000'),
("Bấm Lưu và duyệt 2 lần liên tiếp","P1",'Form hợp lệ','1. Bấm nhanh 2 lần "Lưu và duyệt"','—','- Nút bị khóa, có biểu tượng đang xử lý trong lúc lưu\n- Chỉ tạo 1 phiếu'),
])

sec("VII. XEM CHI TIẾT PHIẾU","XEM CHI TIẾT PHIẾU",[
("Dữ liệu chi tiết đúng phiếu","P0",'Phiếu P-TPE: Năm 2026, 31/10/2026, KD1-TPE, ghi chú "Kết chuyển T10", VV-01 5,000,000','1. Bấm Số phiếu ở danh sách','—','- Tiêu đề "Chi tiết kết chuyển chi phí phải trả"\n- Hiện đúng Số phiếu, Năm, Tình đến ngày, Ngày hạch toán, Phòng ban, Xuất hóa đơn Có, Ghi chú\n- Bảng Chi tiết có VV-01, 3351, 33481, 5,000,000'),
("Không có nút thao tác","P0",'Đăng nhập Super Admin, mở P-TPE','1. Xem toàn màn','—','- Không có nút Lưu, Sửa, Xóa, In'),
("Ghi chú ở màn chi tiết","P1",'Mở P-TPE','1. Gõ thêm vào ô Ghi chú\n2. Tải lại trang','—','- Mong đợi: ô chỉ đọc\n- Lưu ý: theo code hiện tại gõ được nhưng không lưu, tải lại mất - ghi Failed'),
("Vụ việc đã khóa sau khi lập phiếu","P1",'P-TPE có VV-01, sau đó VV-01 bị khóa','1. Mở P-TPE','—','- Mong đợi: vẫn hiện tên VV-01\n- Lưu ý: theo code hiện tại ô Mã vụ việc trống - ghi Failed'),
("Phòng đã đóng sau khi lập phiếu","P1",'Phiếu của PD-TPE, sau đó phòng bị đóng; mở bằng tài khoản người lập','1. Mở phiếu','—','- Mong đợi: vẫn hiện tên phòng\n- Lưu ý: theo code hiện tại ô Phòng ban trống - ghi Failed'),
("Phiếu năm cũ ngoài danh sách Năm","P2",'Có phiếu mà Năm nhỏ hơn năm hiện tại trừ 1 (ví dụ phiếu Năm 2025 khi đã sang năm 2027)','1. Mở phiếu','—','- Mong đợi: vẫn hiện Năm của phiếu\n- Lưu ý: theo code hiện tại ô Năm trống - ghi Failed'),
("Mở phiếu không tồn tại","P2",'—','1. Sửa đường dẫn sang mã phiếu không có','—','- Báo không tìm thấy, không lộ thông tin lỗi'),
])

sec("VIII. RÀNG BUỘC NHẬP LIỆU","RÀNG BUỘC NHẬP LIỆU",[
("Lưu khi để trống Tình đến ngày","P0",'Đã chọn Năm, Phòng ban','1. Bấm "Lưu và duyệt"','—','- Thông báo "Tạo kết chuyển thất bại!"\n- Ô Tình đến ngày báo "Bắt buộc phải nhập"'),
("Lưu khi để trống Phòng ban","P0",'Đã chọn Năm, Tình đến ngày','1. Bấm "Lưu và duyệt"','—','- Thông báo "Tạo kết chuyển thất bại!"\n- Ô Phòng ban báo "Bắt buộc phải nhập"'),
("Lưu khi không có dòng chi tiết","P0",'Đã nhập đủ thông tin chung, bảng Chi tiết trống','1. Bấm "Lưu và duyệt"','—','- Thông báo "Tạo kết chuyển thất bại!", không có phiếu mới'),
("Dòng chưa chọn vụ việc","P0",'Đã thêm 1 dòng, chưa chọn Mã vụ việc','1. Bấm "Lưu và duyệt"','—','- Thông báo "Tạo kết chuyển thất bại!"\n- Dòng báo "Bắt buộc phải nhập"'),
("Lưu khi trùng vụ việc","P0",'Dòng 1 và 2 đều chọn VV-01 (dòng 2 đã nhận thông báo "Vụ việc đã được chọn!")','1. Bấm "Lưu và duyệt"','—','- Thông báo "Tạo kết chuyển thất bại!"\n- Báo "Không được nhập trùng", không có phiếu mới'),
("Số tiền bằng 0","P0",'Dòng VV-03 có Số tiền 0','1. Bấm "Lưu và duyệt"','—','- Thông báo "Số tiền kết chuyển phải khác 0", không có phiếu mới'),
("Một dòng bằng 0 trong nhiều dòng","P1",'Dòng VV-01 = 5,000,000; dòng VV-03 = 0','1. Bấm "Lưu và duyệt"','—','- Thông báo "Số tiền kết chuyển phải khác 0"\n- Cả phiếu không lưu, phải xóa dòng VV-03'),
("Tình đến ngày là ngày tương lai","P0",'Ngày hiện tại 06/11/2026; Năm 2026','1. Chọn Tình đến ngày 31/12/2026, thêm VV-01\n2. Bấm "Lưu và duyệt"','Tình đến ngày: 31/12/2026','- Thông báo "Ngày đến không được chọn ngày tương lai", không có phiếu mới'),
("Tình đến ngày bằng hôm nay","P1",'Ngày hiện tại 06/11/2026; VV-01 có số dư','1. Chọn Tình đến ngày là hôm nay, thêm VV-01, lưu','—','- Lưu thành công'),
("Tình đến ngày khác Năm","P0",'Năm 2025','1. Chọn Tình đến ngày 31/10/2026, thêm vụ việc có số dư\n2. Bấm "Lưu và duyệt"','—','- Thông báo "Ngày đến không trùng với năm được chọn", không có phiếu mới'),
("Vừa tương lai vừa khác Năm","P2",'Năm 2025, ngày hiện tại 06/11/2026','1. Chọn Tình đến ngày 31/12/2026, thêm vụ việc, lưu','—','- Thông báo "Ngày đến không trùng với năm được chọn", không có phiếu mới'),
("Ghi chú dài và ký tự đặc biệt","P2",'Form hợp lệ','1. Nhập Ghi chú 500 ký tự có dấu nháy, thẻ <b>\n2. Lưu, mở chi tiết','—','- Lưu thành công\n- Ghi chú hiện đúng nguyên văn, không bị hiểu thành định dạng'),
])

sec("IX. CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI","CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI",[
("Lập phiếu lùi ngày sau khi đã kết chuyển","P0",'VV-01 của KD1-TPE: 3,000,000 ngày 20/03/2026; 2,000,000 ngày 10/10/2026; đã có phiếu kết chuyển 5,000,000 Tình đến ngày 31/10/2026','1. Lập phiếu mới Tình đến ngày 31/03/2026, thêm VV-01\n2. Bấm "Lưu và duyệt"\n3. Xem số dư VV-01 đến 31/10/2026','—','- Mong đợi: không kết chuyển lại, Số tiền = 0 hoặc bị chặn\n- Lưu ý: theo code hiện tại Số tiền vẫn = 3,000,000, lưu được và ghi sổ lần hai, số dư 3351 thành -3,000,000 - ghi Failed'),
("Hai tab cùng lập một vụ việc","P0",CHUNG,'1. Mở 2 tab màn lập phiếu, cùng chọn VV-01 (5,000,000)\n2. Lưu tab 1\n3. Lưu tab 2\n4. Xem Sổ chi tiết các tài khoản theo Số phiếu của tab 2','—','- Mong đợi: tab 2 bị chặn vì số dư đã thay đổi\n- Lưu ý: theo code hiện tại tab 2 lưu thành công, phiếu ghi 5,000,000 nhưng không có bút toán nào - ghi Failed'),
("Số dư đổi sau khi chọn vụ việc","P0",'Form đã chọn VV-01 = 5,000,000, chưa lưu','1. Kế toán khác ghi thêm Có 3351 200,000 cho VV-01, ngày trong kỳ\n2. Bấm "Lưu và duyệt"\n3. So sánh Số tiền của phiếu với bút toán','—','- Mong đợi: số trên phiếu khớp bút toán\n- Lưu ý: theo code hiện tại phiếu ghi 5,000,000, bút toán ghi 5,200,000 - ghi Failed'),
("Sửa số tiền khi gửi lên (gọi thẳng)","P1",CHUNG,'1. Dùng công cụ kiểm thử API gửi lưu phiếu VV-01 với số tiền 5,001,000','Số tiền: 5,001,000','- Mong đợi: hệ thống tự tính lại hoặc từ chối\n- Lưu ý: theo code hiện tại phiếu ghi 5,001,000, bút toán ghi 5,000,000 - ghi Failed'),
("Hai công ty đánh số độc lập","P1",'Phiếu cuối TPE 00056, TPC 00010','1. KT-1 lập 1 phiếu\n2. KT-2 lập 1 phiếu','—','- TPE.KCCPPT2026.00057\n- TPC.KCCPPT2026.00011'),
("Hai người cùng lưu một lúc","P2",'KT-1 và KT-3 cùng thuộc TPE, 2 phòng khác nhau','1. Cùng bấm "Lưu và duyệt" trong một thời điểm','—','- Không có 2 phiếu trùng Số phiếu\n- Nếu một phiếu lỗi thì không có bút toán dở dang'),
("Lỗi giữa chừng không để lại dữ liệu dở","P1",'Tester kỹ thuật','1. Gửi lưu phiếu có Năm khác Tình đến ngày','—','- Không có phiếu, dòng chi tiết hay bút toán mới'),
("Vụ việc khóa sau khi đã chọn trên form","P2",'Form đã chọn VV-01, chưa lưu','1. Quản trị khóa VV-01\n2. Bấm "Lưu và duyệt"','—','- Mong đợi: báo vụ việc đã khóa\n- Lưu ý: theo code hiện tại vẫn lưu thành công - ghi Failed nếu nghiệp vụ yêu cầu chặn'),
])

sec("X. LUỒNG NGHIỆP VỤ ĐẦU - CUỐI","LUỒNG NGHIỆP VỤ ĐẦU - CUỐI",[
("Kết chuyển cuối kỳ một phòng, nhiều vụ việc","P0",'VV-01 = 5,000,000; VV-02 = -1,200,000; VV-07 = 3,000,000 ở KD1-TPE','1. KT-1 lập phiếu 3 vụ việc Tình đến ngày 31/10/2026, lưu\n2. Tìm phiếu ở danh sách, mở chi tiết\n3. Xem Sổ chi tiết các tài khoản theo Số phiếu\n4. Lập phiếu mới cùng kỳ, chọn lại 3 vụ việc','—','- Phiếu có tổng 6,800,000, chi tiết đủ 3 dòng\n- Tổng Nợ = tổng Có trên bút toán\n- Bước 4 cả 3 vụ việc có Số tiền 0, không lưu được'),
("Kết chuyển hai kỳ liên tiếp","P0",'VV-01: 3,000,000 ngày 20/03/2026; 2,000,000 ngày 10/10/2026','1. Lập phiếu Tình đến ngày 31/03/2026, lưu\n2. Lập phiếu Tình đến ngày 31/10/2026, lưu','—','- Phiếu 1 = 3,000,000\n- Phiếu 2 = 2,000,000\n- Số dư VV-01 đến 31/10/2026 = 0'),
("Kết chuyển rồi đối chiếu công nợ nhân viên","P0",'NV-A có 3,000,000 ở VV-01','1. Lập phiếu VV-01, lưu\n2. Mở Sổ chi tiết công nợ nhân viên của NV-A, tài khoản 33481\n3. Mở Bảng cân đối phát sinh công nợ nhân viên, tài khoản 33481','—','- Hai màn đều tăng phải trả NV-A 3,000,000\n- Bấm Số phiếu từ sổ về đúng phiếu'),
("Phân quyền xuyên suốt hai công ty","P1",'KT-1 thuộc TPE, KT-2 thuộc TPC, KT-TCT quyền tổng công ty','1. KT-1 lập phiếu KD1-TPE\n2. KT-2 lập phiếu KD1-TPC\n3. Mỗi người mở danh sách','—','- KT-1 chỉ thấy phiếu TPE, KT-2 chỉ thấy phiếu TPC\n- KT-TCT thấy cả 2'),
])

# ---------- dựng file từ mẫu ----------
src, out = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(src); ws = wb.active
for rng in list(ws.merged_cells.ranges):
    if rng.min_row >= 18: ws.unmerge_cells(str(rng))
ws.delete_rows(18, ws.max_row)
for r in list(ws.row_dimensions):
    if r >= 18: del ws.row_dimensions[r]
for r, (txt, h) in MO_TA.items():
    ws.cell(r, 2).value = txt; ws.row_dimensions[r].height = h
ws['A11'] = f"Testcase _ {TEN} (ERP) - Cập nhật ngày 06/11/2026"

thin = Side(style='thin'); BD = Border(left=thin, right=thin, top=thin, bottom=thin)
F = Font(name='Times New Roman', size=12); W = PatternFill('solid', fgColor='FFFFFF')
SF = Font(name='Times New Roman', size=12, bold=True, color='1F4E79'); SP = PatternFill('solid', fgColor='D6E4F0')
WIDTH = {4:22.8, 6:44.8, 7:37.1, 8:22, 9:43.9}
def lines(t, w):
    return sum(max(1, math.ceil(len(x) * 1.08 / w)) for x in str(t).split('\n'))
r = 18; num = 0
for si, (title, group, rows) in enumerate(S):
    for c in range(1, 18):
        x = ws.cell(r, c); x.fill = SP; x.border = BD; x.font = SF
    ws.cell(r, 3).value = title; ws.cell(r, 3).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=17)
    ws.row_dimensions[r].height = 26.1; r += 1
    for i, (name, pri, pre, step, data, exp) in enumerate(rows):
        tc = f"TC-ROLE-{i:02d}" if si == 0 else f"TC_{si:02d}.{i+1:03d}"
        vals = [TEN, group, tc, name, pri, pre, step, data, exp, None, "Not Executed", "Not Executed", "Not Executed", None, None, None, None]
        for c, v in enumerate(vals, 1):
            x = ws.cell(r, c); x.value = v; x.font = F; x.fill = W; x.border = BD
            x.alignment = Alignment(horizontal='center' if c in (3, 5, 11, 12, 13, 14, 15, 16, 17) else 'left', vertical='center', wrap_text=True)
        n = max(lines(vals[c-1], WIDTH[c]) for c in WIDTH)
        ws.row_dimensions[r].height = max(31.5, 15.75 * n); r += 1
wb.calculation.fullCalcOnLoad = True
wb.save(out)
print("rows to", r - 1)
