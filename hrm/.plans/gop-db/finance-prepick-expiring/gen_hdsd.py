# -*- coding: utf-8 -*-
"""Sinh HDSD man "Hang sap het han giu" tu khung HDSD_MAU.docx (hdsd-documenter).

Man CHI DOC, anh em cua "Danh sach hang giu".
Anh chup that: ./prepick_expiring_shots (dev, 05/10/2026, tai khoan DNS Admin).
Ngon ngu: NGUOI DUNG CUOI — khong dung thuat ngu code.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, '..', '..', '..', '.claude', 'skills',
                                'hdsd-documenter', 'assets'))
from hdsd_engine import HdsdBuilder  # noqa: E402

SHOTS = os.path.join(BASE, 'prepick_expiring_shots')
OUT = os.path.join(BASE, 'HDSD_Hang sap het han giu.docx')

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title='(Màn hình: Hàng sắp hết hạn giữ)',
                doc_title='HDSD - Hàng sắp hết hạn giữ')

# =============================================================== TONG QUAN
b.h1('TỔNG QUAN')

b.h2('1. Thuật ngữ sử dụng trong tài liệu')
b.table([
    ['Thuật ngữ', 'Ý nghĩa'],
    ['Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên '
                 'kinh doanh đứng tên giữ, có hạn giữ.'],
    ['Lô hàng giữ', 'Một phần hàng giữ có cùng hàng hóa, nhân viên, khách hàng và hạn giữ. Mỗi '
                    'dòng khách hàng trong bảng là một lô.'],
    ['Hạn giữ', 'Ngày cuối cùng hàng được giữ cho khách hàng.'],
    ['Số ngày cảnh báo', 'Số ngày do quản trị hệ thống cấu hình chung cho nhóm Giữ hàng. Trên '
                         'dữ liệu hiện tại là 7 ngày.'],
    ['Hết hạn', 'Lô có hạn giữ TRƯỚC ngày hôm nay. Nhãn màu đỏ.'],
    ['Đến hạn', 'Lô có hạn giữ ĐÚNG ngày hôm nay. Nhãn màu vàng.'],
    ['Tổng SL trong kho', 'Tổng tồn kho kế toán của hàng hóa trên các kho thuộc công ty bạn được '
                          'xem, không phải số đang giữ.'],
    ['Đơn vị cơ bản', 'Đơn vị tính gốc của hàng hóa (Cái, Bộ…). Số hàng giữ luôn lưu theo đơn vị '
                      'này.'],
])

b.h2('2. Cập nhật tài liệu')
b.table([
    ['Phiên bản', 'Ngày', 'Nội dung'],
    ['1.0', '05/10/2026', 'Ban hành lần đầu cho màn hình Hàng sắp hết hạn giữ trên phân hệ '
                          'Tài chính.'],
])

b.h2('3. Giới thiệu chung')
b.para('Màn hình Hàng sắp hết hạn giữ là một báo cáo tra cứu, giúp người quản lý giữ hàng và kế '
       'toán kho nhìn ra những lô hàng giữ vừa hết hạn trong mấy ngày gần đây để nhắc nhân viên '
       'kinh doanh gia hạn hoặc trả hàng về kho.')
b.para('Đường dẫn trực tiếp: /finance/prepick-expiring. Màn hình CHỈ ĐỂ XEM: không có nút thêm, '
       'sửa, xóa, và không làm thay đổi số hàng giữ của ai.')
b.para('Điều quan trọng nhất cần hiểu về màn hình này — quy tắc chọn lô: màn hình chỉ hiện các lô '
       'có hạn giữ nằm trong khoảng từ (hôm nay trừ số ngày cảnh báo) đến hết hôm nay, tính cả hai '
       'đầu. Ví dụ hôm nay là 05/10/2026 và số ngày cảnh báo là 7 thì màn hình hiện các lô có hạn '
       'giữ từ 28/09/2026 đến 05/10/2026.')
b.para('Nói cách khác, dù tên màn là “sắp hết hạn”, thực tế đây là danh sách hàng ĐÃ hoặc VỪA hết '
       'hạn giữ trong 7 ngày gần đây. Cách chọn này được giữ y hệt hệ thống cũ để hai hệ thống ra '
       'cùng số liệu. Vì vậy cột Trạng thái chỉ có “Hết hạn” hoặc “Đến hạn”, không bao giờ có '
       '“Trong hạn” — đó là đúng, không phải lỗi.')
b.para('Muốn xem hàng CÒN hạn nhưng sắp tới hạn, hãy dùng màn Yêu cầu gia hạn hàng giữ. Muốn xem '
       'toàn bộ hàng đang giữ, dùng màn Danh sách hàng giữ.')

b.h2('4. Quyền sử dụng và phạm vi dữ liệu')

b.h3('4.1. Bảng quyền của màn hình')
b.table([
    ['Tên quyền', 'Cho phép làm gì', 'Phần tương ứng trên màn hình', 'Ghi chú'],
    ['Quản lý giữ hàng',
     'Mở và xem màn hình. Đây là quyền BẮT BUỘC.',
     'Toàn bộ màn hình: danh sách, mở rộng chi tiết, Lịch sử giữ hàng, Xuất Excel, In.',
     'Thiếu quyền này thì không xem được gì, kể cả khi có các quyền xem bên dưới.'],
    ['Xem phiếu hàng giữ theo tổng công ty',
     'Xem lô hàng giữ của mọi công ty.',
     'Ô lọc Công ty xuất hiện trong khu vực lọc nâng cao.',
     'Cần đi kèm quyền Quản lý giữ hàng.'],
    ['Xem phiếu hàng giữ theo công ty',
     'Xem lô hàng giữ của công ty đang đăng nhập.',
     'Không có ô lọc Công ty.',
     'Cần đi kèm quyền Quản lý giữ hàng.'],
    ['Xem phiếu hàng giữ theo phòng ban',
     'Xem lô do nhân viên thuộc phòng ban bạn quản lý và phòng ban của bạn đứng tên giữ.',
     'Không có ô lọc Công ty.',
     'Cần đi kèm quyền Quản lý giữ hàng.'],
])
b.para('Nếu có nhiều quyền xem, phần mềm lấy quyền rộng nhất theo thứ tự tổng công ty → công ty → '
       'phòng ban. Phạm vi này áp cho mọi thứ trên màn: bảng, các dòng chi tiết, danh sách lựa chọn '
       'trong ô lọc, tệp Excel và bản in.')

b.h3('4.2. Người dùng KHÔNG có quyền "Quản lý giữ hàng"')
b.para('Mục menu “Hàng sắp hết hạn giữ” vẫn hiển thị, nhưng khi mở vào phần mềm báo “Bạn không có '
       'quyền xem danh sách hàng sắp hết hạn giữ” và bảng không có dữ liệu. Các nút In, Xuất Excel '
       'cũng báo cùng thông báo đó. Hãy liên hệ quản trị để được cấp quyền.')

b.h3('4.3. Người dùng có quyền "Quản lý giữ hàng" nhưng không có quyền xem theo cấp')
b.para('Bạn chỉ thấy những lô hàng do CHÍNH BẠN đứng tên giữ. Ô lọc Nhân viên chỉ có tên bạn. Mọi '
       'thao tác xem, mở rộng, lịch sử, xuất Excel, in đều làm được trên phần dữ liệu đó.')

b.h3('4.4. Người dùng có thêm quyền "Xem phiếu hàng giữ theo phòng ban"')
b.para('Bạn thấy lô của mọi nhân viên thuộc các phòng ban bạn được giao quản lý, cộng phòng ban của '
       'bạn và lô của chính bạn. Ô lọc Nhân viên liệt kê những người đang giữ hàng trong phạm vi '
       'đó.')

b.h3('4.5. Người dùng có thêm quyền "Xem phiếu hàng giữ theo công ty"')
b.para('Bạn thấy lô hàng giữ của mọi nhân viên trong công ty đang đăng nhập. Cột Tổng SL trong '
       'kho và ô Lọc theo kho cũng chỉ tính các kho thuộc công ty này.')

b.h3('4.6. Người dùng có thêm quyền "Xem phiếu hàng giữ theo tổng công ty"')
b.para('Bạn thấy lô hàng giữ của mọi công ty. Khu vực lọc nâng cao có thêm ô Công ty để thu hẹp '
       'về một công ty; khi chọn công ty, cột Tổng SL trong kho cũng chỉ tính kho của công ty đó.')

# =================================================== PHAN 1
b.h1('PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')

b.h2('1. Vào màn này bằng cách nào')
b.table([
    ['Vào từ', 'Bấm theo đường', 'Danh sách hiện ra'],
    ['Phân hệ Tài chính', 'Tài chính → nhóm Giữ hàng → bấm Hàng sắp hết hạn giữ',
     'Hàng hóa có lô hết hạn / đến hạn trong 7 ngày gần đây, trong phạm vi quyền của bạn.'],
    ['Liên kết từ màn khác', 'Bấm liên kết “xem hàng sắp hết hạn” của một hàng hóa',
     'Chỉ đúng hàng hóa đó. Bấm Làm mới để xem lại toàn bộ.'],
])
b.para('Nếu mở màn mà danh sách trống hoặc ít hơn mong đợi, hãy kiểm tra: (1) bạn có quyền xem '
       'theo cấp nào, (2) bộ lọc lần trước có còn được giữ lại không (phần mềm nhớ bộ lọc 10 phút), '
       '(3) lô bạn tìm có hạn giữ nằm trong 7 ngày gần đây không.')

b.h2('2. Bố cục màn hình')
b.para('Màn hình gồm hai khối từ trên xuống: khối “Bộ lọc danh sách” (ô tìm nhanh, các nút Cài đặt '
       'bộ lọc, Tìm kiếm nâng cao, Tìm kiếm, Làm mới) và khối bảng “Hàng sắp hết hạn giữ” (nút In, '
       'Xuất Excel, nút cấu hình cột, bảng và phân trang).')
b.image('01-danh-sach.png', 'Màn hình Hàng sắp hết hạn giữ lúc mới vào')

# =================================================== PHAN 2
b.h1('PHẦN 2: ĐỌC BẢNG DANH SÁCH')

b.h2('1. Các cột của bảng')
b.para('Mỗi dòng của bảng là MỘT HÀNG HÓA. Bảng có ba tầng: hàng hóa → nhân viên đang giữ → '
       'khách hàng (lô). Hai cột đầu đổi nghĩa theo tầng, nên tên cột ghi gộp.')
b.table([
    ['Cột', 'Dòng hàng hóa', 'Dòng nhân viên', 'Dòng khách hàng (lô)'],
    ['STT', 'Nút tròn mở / thu chi tiết', 'Ký hiệu nhánh', 'Ký hiệu nhánh'],
    ['Mã hàng hóa / Nhân viên / Khách hàng', 'Mã hàng hóa', 'Tên nhân viên',
     'Mã khách hàng - Tên khách hàng'],
    ['Tên hàng hóa / Phòng ban', 'Tên hàng hóa', 'Phòng ban của nhân viên', 'Trống'],
    ['Đơn vị', 'Đơn vị đang xem', 'Trống', 'Trống'],
    ['Model', 'Model', 'Trống', 'Trống'],
    ['Thương hiệu', 'Thương hiệu', 'Trống', 'Trống'],
    ['Tổng SL trong kho', 'Tổng tồn kho kế toán', 'Trống', 'Trống'],
    ['SL giữ', 'Tổng các lô trong 7 ngày gần đây', 'Tổng của nhân viên', 'Số của lô'],
    ['Hạn giữ', 'Trống', 'Trống', 'Ngày hạn giữ'],
    ['Trạng thái', 'Trống', 'Trống', 'Hết hạn / Đến hạn'],
    ['Hành động', 'Trống', 'Trống', 'Nút Lịch sử giữ hàng'],
])
b.para('Các ô trống ở bảng trên là đúng thiết kế: một hàng hóa có thể gồm nhiều lô với hạn khác '
       'nhau, nên Hạn giữ và Trạng thái chỉ có ở từng lô.')
b.para('Lưu ý về số SL giữ của dòng hàng hóa: đây chỉ là tổng các lô hết hạn / đến hạn trong 7 '
       'ngày gần đây, KHÔNG phải toàn bộ số đang giữ. Ví dụ hàng H đang giữ 10 cái, trong đó 6 cái '
       'hết hạn ngày 03/10/2026 và 4 cái còn hạn tới 20/10/2026 thì màn này ghi SL giữ = 6.')
b.para('Mã hàng hóa hiển thị dạng chữ thường, không bấm vào được.')

b.h2('2. Đổi đơn vị tính')
b.para('Với hàng hóa có từ hai đơn vị trở lên, ô Đơn vị là một ô chọn. Chọn đơn vị khác thì Tổng '
       'SL trong kho và SL giữ của dòng đó cùng mọi dòng nhân viên, khách hàng bên dưới được quy '
       'đổi theo, làm tròn xuống 2 chữ số thập phân. Hàng hóa chỉ có một đơn vị thì ô này là chữ.')
b.para('Số hiển thị theo chuẩn quốc tế: dấu phẩy ngăn hàng nghìn, dấu chấm phần thập phân '
       '(ví dụ 1,234.5 hoặc 2.8).')

b.h2('3. Sắp xếp')
b.para('Bốn cột có mũi tên ⇅ bấm để sắp xếp: Mã hàng hóa / Nhân viên / Khách hàng, Tên hàng hóa / '
       'Phòng ban, Tổng SL trong kho, SL giữ. Bấm cột khác thì bỏ sắp xếp cột cũ. Mặc định danh '
       'sách sắp theo Tên hàng hóa A → Z. Sắp xếp chỉ áp cho dòng hàng hóa.')

b.h2('4. Phân trang')
b.para('Chân bảng ghi “Hiển thị a–b / N”, trong đó N là tổng số HÀNG HÓA (không phải số lô). Mặc '
       'định 10 dòng mỗi trang; đổi ở ô “Số dòng/trang” (5, 10, 20, 50, 100), đổi xong quay về '
       'trang 1. Các dòng nhân viên, khách hàng mở ra không tính vào số dòng mỗi trang.')
b.para('Khi bạn lật trang, đổi bộ lọc hoặc sắp xếp, mọi dòng đang mở rộng sẽ tự thu lại.')

# =================================================== PHAN 3
b.h1('PHẦN 3: TÌM KIẾM VÀ LỌC')

b.h2('1. Ô tìm nhanh')
b.para('Ô “Nhập tên, số điện thoại hoặc mã KH để tìm kiếm” tìm theo KHÁCH HÀNG của lô: gõ một phần '
       'tên, mã hoặc số điện thoại khách hàng rồi bấm nút Tìm kiếm. Gõ xong mà chưa bấm Tìm kiếm '
       'thì danh sách chưa đổi.')
b.para('Ô này KHÔNG tìm theo mã hàng hóa. Muốn tìm hàng hóa, dùng ô Mã hàng hóa hoặc Tên hàng hóa '
       'trong khu vực lọc nâng cao.')

b.h2('2. Khu vực lọc nâng cao')
b.para('Bấm “Tìm kiếm nâng cao” để mở thêm các ô lọc (bấm “Ẩn tìm kiếm nâng cao” để đóng). Chỉ cần '
       'đổi giá trị một ô là danh sách tự nạp lại, không cần bấm Tìm kiếm.')
b.image('02-bo-loc-nang-cao.png', 'Khu vực Tìm kiếm nâng cao đang mở')
b.table([
    ['Ô lọc', 'Cách dùng', 'Ghi chú'],
    ['Mã hàng hóa', 'Gõ một phần mã hàng hóa.', 'Tìm gần đúng.'],
    ['Tên hàng hóa', 'Gõ một phần tên hàng hóa.', 'Tìm gần đúng.'],
    ['Lọc theo kho', 'Chọn một kho kế toán (dạng “LN01 - Liên Ninh - Hàng bán”).',
     'Chỉ liệt kê kho đang hoạt động. Giữ lại hàng hóa có tồn kho ở kho đó. Cột Tổng SL trong '
     'kho vẫn là tổng mọi kho, không đổi theo kho chọn.'],
    ['Thương hiệu', 'Chọn một thương hiệu.', 'Chỉ liệt kê thương hiệu đang có hàng giữ.'],
    ['Model', 'Chọn một model.', 'Chỉ liệt kê model đang có hàng giữ.'],
    ['Trạng thái', 'Chọn Hết hạn hoặc Đến hạn.', 'Không có lựa chọn Trong hạn.'],
    ['Nhân viên', 'Chọn người đứng tên giữ.',
     'Chỉ liệt kê người đang giữ hàng trong phạm vi của bạn; thu hẹp theo Công ty / Phòng ban.'],
    ['Công ty', 'Chọn một công ty.', 'Chỉ có khi bạn có quyền xem theo tổng công ty.'],
    ['Phòng ban', 'Chọn một phòng ban.', 'Đổi Công ty hoặc Phòng ban thì ô Nhân viên bị xóa.'],
])
b.para('Biểu tượng ổ khóa cạnh nhãn Công ty và Phòng ban KHÔNG có nghĩa ô bị khóa. Đó là công tắc '
       '“Hiện cả công ty / phòng ban đã khoá”: bấm vào để danh sách lựa chọn có thêm các đơn vị đã '
       'ngừng hoạt động.')
b.para('Danh sách lựa chọn của Nhân viên, Thương hiệu, Model lấy theo toàn bộ hàng đang giữ, nên '
       'có thể chọn một giá trị mà bảng ra rỗng — nghĩa là người / thương hiệu đó không có lô nào '
       'hết hạn trong 7 ngày gần đây.')

b.h2('3. Nút Làm mới')
b.para('Nút “Làm mới” xóa mọi ô lọc, ô tìm nhanh, thứ tự sắp xếp và nạp lại danh sách từ đầu. Quy '
       'tắc 7 ngày gần đây vẫn giữ nguyên.')
b.para('Bộ lọc bạn dùng được nhớ trong 10 phút: rời màn rồi quay lại thì các điều kiện cũ và trạng '
       'thái đóng / mở khu vực lọc vẫn còn.')

b.h2('4. Chọn ô lọc muốn hiển thị')
b.para('Bấm “Cài đặt bộ lọc”. Cửa sổ liệt kê 8 mục: Mã hàng hóa, Tên hàng hóa, Lọc theo kho, '
       'Thương hiệu, Model, Trạng thái, Nhân viên, Công ty – Phòng ban.')
b.image('03-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc')
b.bullet('Bỏ tích để ẩn ô lọc, tích để hiện lại.')
b.bullet('Kéo biểu tượng ⠿ để đổi thứ tự các ô.')
b.bullet('Bấm “Lưu” để ghi lại; cài đặt lưu riêng cho tài khoản của bạn trên màn này.')
b.bullet('Bấm “Khôi phục mặc định” để về đủ 8 mục theo thứ tự ban đầu; “Đóng” để thoát không lưu.')

# =================================================== PHAN 4
b.h1('PHẦN 4: CHỌN CỘT HIỂN THỊ')
b.para('Bấm nút biểu tượng cột ở góc phải khối bảng (bên phải nút Xuất Excel). Cửa sổ “Tuỳ chỉnh '
       'cột” mở ra với 11 cột.')
b.image('04-cau-hinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột')
b.bullet('Ba cột STT, Mã hàng hóa / Nhân viên / Khách hàng và Hành động luôn hiện, không bỏ tích '
         'được.')
b.bullet('Các cột còn lại tích / bỏ tích tùy ý, kéo biểu tượng ≡ để đổi thứ tự.')
b.bullet('Bấm “Lưu” để áp dụng, “Đóng” để thoát không lưu. Cài đặt lưu riêng cho tài khoản của '
         'bạn.')

# =================================================== PHAN 5
b.h1('PHẦN 5: XEM CHI TIẾT THEO NHÂN VIÊN VÀ KHÁCH HÀNG')
b.para('Yêu cầu quyền: Quản lý giữ hàng.')
b.h2('1. Mở rộng một hàng hóa')
b.para('Bấm nút tròn có mũi tên ở cột STT của dòng hàng hóa. Trong lúc tải, nút hiện biểu tượng '
       'xoay. Tải xong, ngay dưới dòng hàng hóa xuất hiện:')
b.bullet('Dòng NHÂN VIÊN (nền xanh lá nhạt): biểu tượng người + tên nhân viên, phòng ban, và tổng '
         'SL giữ của nhân viên đó.')
b.bullet('Dòng KHÁCH HÀNG (nền xanh dương nhạt) dưới mỗi nhân viên: mã - tên khách hàng, SL giữ '
         'của lô, Hạn giữ, nhãn Trạng thái và nút Lịch sử giữ hàng.')
b.image('05-mo-rong-nhan-vien-khach-hang.png', 'Hàng hóa đã mở rộng tới nhân viên và khách hàng')
b.para('Ví dụ trên ảnh: hàng SG-MN-HB-XD0107 có SL giữ 6, do nhân viên Đàm Phước Nhiên giữ 6 cho '
       'khách hàng 50TPHPPH-381, hạn giữ 03/10/2026, trạng thái Hết hạn (vì hôm nay là '
       '05/10/2026).')
b.para('Tổng SL giữ của các dòng nhân viên luôn bằng SL giữ của dòng hàng hóa. Các dòng chi tiết '
       'cũng tuân theo đúng bộ lọc đang áp: nếu bạn đang lọc một khách hàng, chỉ lô của khách hàng '
       'đó hiện ra.')
b.h2('2. Thu gọn')
b.para('Bấm lại nút ở cột STT để thu gọn. Mở lại hàng hóa vừa xem thì hiện ngay, không phải chờ '
       'tải. Nếu tải lỗi, phần mềm báo “Lỗi khi tải chi tiết giữ hàng” và dòng không mở ra.')

# =================================================== PHAN 6
b.h1('PHẦN 6: LỊCH SỬ GIỮ HÀNG CỦA MỘT LÔ')
b.para('Yêu cầu quyền: Quản lý giữ hàng.')
b.para('Ở dòng khách hàng (lô), bấm nút biểu tượng đồng hồ ở cột Hành động. Cửa sổ “Lịch sử giữ '
       'hàng” mở ra, dòng phụ dưới tiêu đề ghi “Hàng hóa: mã - tên”.')
b.image('06-lich-su-giu-hang.png', 'Cửa sổ Lịch sử giữ hàng')
b.h2('1. Khối thông tin')
b.table([
    ['Mục', 'Nội dung'],
    ['Mã hàng', 'Mã hàng hóa.'],
    ['Tên hàng', 'Tên hàng hóa.'],
    ['Kinh doanh', 'Mã - tên nhân viên đứng tên giữ.'],
    ['Khách hàng', 'Mã - tên khách hàng.'],
    ['Trạng thái', 'Nhãn Hết hạn / Đến hạn kèm “(Hạn giữ hiện tại: dd/mm/yyyy)”.'],
])
b.h2('2. Bảng biến động')
b.table([
    ['Cột', 'Ý nghĩa'],
    ['STT', 'Thứ tự, từ biến động CŨ NHẤT tới MỚI NHẤT.'],
    ['SL biến động', 'Số tăng (+, màu xanh) hoặc giảm (−, màu đỏ) của lần đó.'],
    ['Ngày', 'Ngày phát sinh biến động.'],
    ['SL giữ', 'Số lượng còn giữ SAU lần biến động đó (cộng dồn).'],
    ['Hạn giữ', 'Hạn giữ của lô sau lần biến động.'],
    ['Chứng từ', 'Mã chứng từ gây ra biến động, ví dụ PXG-02132 (phiếu xuất giữ), PGHHG-01580 '
                 '(phiếu gia hạn hàng giữ). Bấm vào để mở chứng từ ở thẻ mới.'],
])
b.para('Dòng “Số lượng giữ hiện tại: 6 Cái.” cho biết số đang giữ, theo đơn vị bạn đang chọn ở dòng '
       'hàng hóa. Ví dụ trên ảnh: giữ 6 ngày 17/07/2026 (PXG-02132), sau đó được gia hạn hai lần '
       '(PGHHG-01580, PGHHG-01727), mỗi lần ghi −6 rồi +6 với hạn mới, hạn cuối là 03/10/2026.')
b.para('Lịch sử hiện đầy đủ mọi lần biến động, kể cả các lần cũ hơn 7 ngày. Chưa có biến động thì '
       'ghi “Chưa có biến động nào.”; tải lỗi thì hiện “Không tải được lịch sử giữ hàng.” kèm nút '
       '“Thử lại”. Bấm “Đóng” để thoát.')

# =================================================== PHAN 7
b.h1('PHẦN 7: XUẤT EXCEL')
b.para('Yêu cầu quyền: Quản lý giữ hàng.')
b.para('Bấm nút “Xuất Excel” ở khối bảng. Cửa sổ “Chọn trường xuất Excel” mở ra với đủ 12 trường '
       'đã được tích sẵn.')
b.image('07-xuat-excel.png', 'Cửa sổ Chọn trường xuất Excel')
b.table([
    ['Trường', 'Nội dung trong tệp'],
    ['Mã hàng hóa / Tên hàng hóa', 'Của hàng hóa.'],
    ['ĐVT', 'Đơn vị CƠ BẢN của hàng hóa.'],
    ['Model / Thương hiệu', 'Của hàng hóa.'],
    ['Nhân viên giữ / Phòng ban', 'Người đứng tên giữ và phòng ban của người đó.'],
    ['Khách hàng', 'Mã - tên khách hàng.'],
    ['SL giữ', 'Số của lô, theo đơn vị cơ bản.'],
    ['Tổng SL trong kho', 'Tổng tồn kho kế toán của hàng hóa.'],
    ['Hạn giữ / Trạng thái', 'Hạn giữ dd/mm/yyyy và Hết hạn / Đến hạn.'],
])
b.bullet('Bỏ tích trường không cần; dùng “Chọn tất cả” / “Bỏ chọn hết” để thao tác nhanh. Dòng '
         '“Đang chọn x/12 trường” đếm số đang tích.')
b.bullet('Kéo biểu tượng ≡ để đổi thứ tự cột trong tệp. Cột STT luôn đứng đầu.')
b.bullet('Bấm “Xuất file”. Trong lúc xuất nút bị khóa. Xong, phần mềm tải về tệp '
         'hang_sap_het_han_giu.xlsx và báo “Xuất Excel thành công”.')
b.para('Tệp Excel là bảng PHẲNG: mỗi dòng là MỘT LÔ (không chia tầng như trên màn), gồm mọi lô khớp '
       'bộ lọc bạn đang áp, không chỉ trang đang xem. Dòng đầu là tiêu đề “DANH SÁCH HÀNG SẮP HẾT '
       'HẠN GIỮ”. Thứ tự dòng theo Phòng ban → Nhân viên → Tên hàng hóa. Số lượng luôn theo đơn vị '
       'cơ bản dù trên màn bạn đang chọn đơn vị khác.')

# =================================================== PHAN 8
b.h1('PHẦN 8: IN DANH SÁCH')
b.para('Yêu cầu quyền: Quản lý giữ hàng.')
b.para('Bấm nút “In” ở khối bảng. Phần mềm dựng bản in theo đúng bộ lọc đang áp và mở cửa sổ '
       '“Xem trước danh sách hàng sắp hết hạn giữ” ngay trên màn (khổ giấy ngang).')
b.image('08-in-danh-sach.png', 'Cửa sổ xem trước bản in')
b.para('Bản in gồm: tiêu đề công ty của bạn, tên “DANH SÁCH HÀNG SẮP HẾT HẠN GIỮ”, bảng thông tin '
       'Ngày in, Số phòng ban, Số nhân viên, Số mục hàng; rồi bảng chi tiết gom theo ba cấp:')
b.bullet('Cấp 1 (STT 1, 2…): “Tên phòng ban - x nhân viên - y mục hàng”.')
b.bullet('Cấp 2 (STT 1.1, 1.2…): “Tên nhân viên - y mục hàng”.')
b.bullet('Cấp 3 (STT 1.1.1…): từng lô với Tên hàng hóa, Mã hàng, ĐVT, SL giữ, Hạn giữ, Khách hàng, '
         'Trạng thái.')
b.para('“Số mục hàng” là số LÔ nên thường lớn hơn số N ở chân bảng (N đếm hàng hóa). Ví dụ ảnh: 14 '
       'phòng ban, 44 nhân viên, 734 mục hàng trong khi bảng có 500 hàng hóa.')
b.para('Bấm nút “In” màu xanh trong cửa sổ để mở hộp thoại in của trình duyệt; bấm × để đóng.')
b.para('Nếu danh sách quá dài (vượt 10,000 dòng in), phần mềm không in mà nhắc bạn thu hẹp bộ lọc '
       'hoặc dùng Xuất Excel. Không có dữ liệu thì cửa sổ báo “Không có dữ liệu để in”.')

# =================================================== PHAN 9
b.h1('PHẦN 9: NHỮNG ĐIỀU CẦN NHỚ')
b.bullet('Màn hình chỉ hiện lô có hạn giữ trong 7 ngày gần đây tính tới hôm nay, tức hàng ĐÃ / VỪA '
         'hết hạn. Không bao giờ có Trạng thái “Trong hạn” — đó là đúng.')
b.bullet('Lô hết hạn từ hơn 7 ngày trước không còn hiện ở đây; xem ở màn Danh sách hàng giữ.')
b.bullet('SL giữ của dòng hàng hóa chỉ cộng các lô trong 7 ngày gần đây, không phải toàn bộ hàng '
         'đang giữ.')
b.bullet('Phải có quyền “Quản lý giữ hàng” mới xem được; quyền xem theo cấp chỉ quyết định bạn thấy '
         'dữ liệu của ai.')
b.bullet('Ô tìm nhanh tìm theo khách hàng, phải bấm Tìm kiếm; các ô lọc nâng cao tự áp dụng.')
b.bullet('Ô Lọc theo kho chỉ chọn ra hàng hóa có tồn ở kho đó; cột Tổng SL trong kho vẫn là tổng '
         'mọi kho.')
b.bullet('Tệp Excel và bản in luôn theo đơn vị cơ bản, mỗi dòng một lô.')
b.bullet('Màn hình chỉ để xem. Muốn xử lý lô hết hạn, dùng màn Yêu cầu gia hạn hàng giữ hoặc Yêu '
         'cầu hủy hàng giữ.')

b.finish()
