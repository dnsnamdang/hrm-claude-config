# -*- coding: utf-8 -*-
"""Sinh HDSD man "Danh sach hang giu" tu khung HDSD_MAU.docx.

Man BAO CAO CHI DOC — tra cuu ton hang giu theo cay 3 tang.
Anh chup that: ./prepick_stock_shots (dev, tai khoan DNS Admin, 05/10/2026).
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

SHOTS = os.path.join(BASE, 'prepick_stock_shots')
OUT = os.path.join(BASE, 'HDSD_Danh sach hang giu.docx')

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title='(Màn hình: Danh sách hàng giữ)',
                doc_title='HDSD - Danh sách hàng giữ')

# =============================================================== TONG QUAN
b.h1('TỔNG QUAN')

b.h2('1. Thuật ngữ sử dụng trong tài liệu')
b.table([
    ['Thuật ngữ', 'Ý nghĩa'],
    ['Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên '
                 'kinh doanh đứng tên giữ, kèm hạn giữ.'],
    ['Lô hàng giữ', 'Một phần hàng giữ của một nhân viên cho một khách hàng với cùng một hạn giữ. '
                    'Một hàng hóa có thể có nhiều lô.'],
    ['SL giữ', 'Số lượng đang giữ. Ở dòng hàng hóa là tổng mọi lô; ở dòng nhân viên là tổng các '
               'lô của nhân viên đó; ở dòng khách hàng là số của riêng lô đó.'],
    ['Tổng SL trong kho', 'Tổng tồn kho kế toán của hàng hóa ở các kho kế toán bạn được xem.'],
    ['Hạn giữ', 'Ngày cuối cùng hàng còn được giữ cho khách.'],
    ['Trong hạn / Đến hạn / Hết hạn', 'Trạng thái của lô, so hạn giữ với ngày hôm nay: hạn giữ '
                                      'sau hôm nay là Trong hạn (xanh lá), đúng hôm nay là Đến hạn '
                                      '(vàng), trước hôm nay là Hết hạn (đỏ).'],
    ['Đơn vị cơ bản', 'Đơn vị tính gốc của hàng hóa. Hàng giữ luôn được ghi theo đơn vị này.'],
])

b.h2('2. Cập nhật tài liệu')
b.table([
    ['Phiên bản', 'Ngày', 'Nội dung'],
    ['1.0', '05/10/2026', 'Ban hành lần đầu cho màn hình Danh sách hàng giữ trên phân hệ Tài '
                          'chính.'],
])

b.h2('3. Giới thiệu chung')
b.para('Màn hình Danh sách hàng giữ giúp bạn trả lời ba câu hỏi: hàng hóa nào đang bị giữ và giữ '
       'bao nhiêu so với tồn kho; ai đang giữ, giữ cho khách nào, đến ngày nào; và một lô hàng giữ '
       'đã tăng giảm thế nào, do chứng từ nào gây ra.')
b.para('Đây là màn hình TRA CỨU, chỉ để xem. Bạn không thêm, sửa hay xóa được gì ở đây, và mọi '
       'thao tác trên màn đều không làm thay đổi số hàng giữ của ai. Muốn thay đổi hàng giữ, hãy '
       'dùng các màn Phiếu xuất giữ, Yêu cầu gia hạn hàng giữ, Yêu cầu hủy hàng giữ hoặc phiếu '
       'điều chuyển hàng giữ.')
b.para('Đường dẫn trực tiếp: /finance/prepick-stocks')

b.h2('4. Quyền sử dụng và phạm vi dữ liệu')

b.h3('4.1. Bảng quyền của màn hình')
b.table([
    ['Tên quyền', 'Cho phép làm gì', 'Phần tương ứng trên màn hình'],
    ['Quản lý giữ hàng',
     'BẮT BUỘC để vào màn. Có quyền này bạn dùng được mọi chức năng: xem, lọc, mở chi tiết, xem '
     'lịch sử giữ hàng, Xuất Excel, In.',
     'Toàn bộ màn hình.'],
    ['Xem phiếu hàng giữ theo tổng công ty',
     'Xem hàng giữ của mọi công ty.',
     'Có thêm ô lọc Công ty; danh sách kho và phòng ban mở rộng ra mọi công ty.'],
    ['Xem phiếu hàng giữ theo công ty',
     'Xem các lô hàng giữ thuộc công ty của bạn.',
     'Bảng, Excel và bản In giới hạn trong công ty bạn.'],
    ['Xem phiếu hàng giữ theo phòng ban',
     'Xem các lô do nhân viên thuộc phòng ban bạn quản lý (kể cả phòng của bạn) đứng tên giữ, '
     'cộng lô của chính bạn.',
     'Bảng, Excel và bản In giới hạn trong các phòng đó.'],
])
b.para('Ba quyền "Xem phiếu hàng giữ theo …" chỉ quyết định bạn thấy dữ liệu của ai. Chúng KHÔNG '
       'thay được quyền "Quản lý giữ hàng": thiếu quyền này thì bạn không xem được màn dù có quyền '
       'xem theo cấp.')

b.h3('4.2. Người dùng không có quyền "Quản lý giữ hàng"')
b.para('Mục menu Danh sách hàng giữ vẫn hiện, nhưng khi mở màn:')
b.bullet('Phần mềm báo "Bạn không có quyền xem danh sách hàng giữ".')
b.bullet('Bảng rỗng, các ô chọn của bộ lọc không có dữ liệu.')
b.bullet('Bấm In hoặc Xuất Excel cũng bị từ chối với cùng thông báo.')
b.para('Liên hệ Quản trị viên để được cấp quyền "Quản lý giữ hàng" nếu công việc của bạn cần '
       'tra cứu hàng giữ.')

b.h3('4.3. Người dùng có quyền "Quản lý giữ hàng" nhưng không có quyền xem theo cấp')
b.para('Bạn dùng được mọi chức năng nhưng chỉ thấy các lô do CHÍNH BẠN đứng tên giữ. Ô lọc Nhân '
       'viên chỉ có tên bạn.')

b.h3('4.4. Có thêm quyền "Xem phiếu hàng giữ theo phòng ban"')
b.para('Bạn thấy hàng giữ của mọi nhân viên thuộc các phòng ban bạn đang quản lý và phòng của bạn, '
       'cộng phần của chính bạn. Ô lọc Phòng ban liệt kê các phòng ban thuộc công ty bạn.')

b.h3('4.5. Có thêm quyền "Xem phiếu hàng giữ theo công ty"')
b.para('Bạn thấy mọi lô hàng giữ thuộc công ty bạn, của bất kỳ nhân viên nào. Cột Tổng SL trong '
       'kho chỉ cộng các kho kế toán thuộc công ty bạn.')

b.h3('4.6. Có thêm quyền "Xem phiếu hàng giữ theo tổng công ty"')
b.para('Bạn thấy hàng giữ của mọi công ty. Khu vực lọc có thêm ô Công ty để thu hẹp về một công '
       'ty; khi chọn công ty, cột Tổng SL trong kho cũng chỉ cộng kho của công ty đó. Tài khoản '
       'Quản trị hệ thống được xem như có quyền này.')

# =================================================== PHAN 1
b.h1('PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')

b.h2('1. Vào màn này bằng cách nào')
b.para('Vào phân hệ Tài chính → nhóm Giữ hàng → bấm Danh sách hàng giữ.', bold_prefix='Cách vào')
b.para('Màn hình chỉ có một lối vào từ menu. Nếu danh sách trống hoặc ít hơn mong đợi, hãy kiểm '
       'tra lại quyền xem theo cấp của bạn (mục 4 phần Tổng quan) và bộ lọc đang áp.')

b.h2('2. Bố cục màn hình')
b.para('Màn hình gồm hai khối từ trên xuống: khối Bộ lọc danh sách (ô tìm nhanh và các nút tìm '
       'kiếm) và khối Danh sách hàng giữ (thanh công cụ, bảng, phân trang).')
b.image('01-danh-sach.png', 'Màn hình Danh sách hàng giữ lúc mới vào')
b.para('Lúc mới vào, bảng hiện 10 hàng hóa đầu tiên, sắp theo tên hàng hóa từ A đến Z. Dòng '
       '"Hiển thị 1–10 / 1035" ở góc dưới bên trái cho biết tổng số HÀNG HÓA đang bị giữ (không '
       'phải tổng số lô).')
b.para('Bộ lọc bạn dùng được nhớ trong 10 phút: rời sang màn khác rồi quay lại thì điều kiện lọc '
       'vẫn còn nguyên.')

# =================================================== PHAN 2
b.h1('PHẦN 2: XEM DANH SÁCH HÀNG GIỮ')

b.para('Yêu cầu quyền: Quản lý giữ hàng.')

b.h2('1. Bảng ba tầng')
b.para('Bảng được tổ chức thành cây ba tầng. Ban đầu bạn chỉ thấy tầng 1; bấm nút tròn ">" ở cột '
       'STT để mở tầng 2 và tầng 3 của một hàng hóa.')
b.table([
    ['Tầng', 'Mỗi dòng là', 'Nhận biết'],
    ['1 – Hàng hóa', 'Một hàng hóa đang bị giữ', 'Nền trắng, cột STT có nút tròn ">".'],
    ['2 – Nhân viên', 'Một nhân viên đang giữ hàng hóa đó',
     'Nền xanh lá nhạt, có biểu tượng người trước họ tên.'],
    ['3 – Khách hàng (lô)', 'Một lô hàng giữ của nhân viên đó cho một khách hàng',
     'Nền xanh dương nhạt, có biểu tượng cửa hàng trước "Mã KH - Tên KH".'],
])

b.h2('2. Các cột của bảng')
b.table([
    ['Cột', 'Tầng hàng hóa', 'Tầng nhân viên', 'Tầng khách hàng (lô)'],
    ['STT', 'Nút ">" mở / thu chi tiết (không in số thứ tự)', 'Ký hiệu nhánh', 'Ký hiệu nhánh'],
    ['Mã hàng hóa / Nhân viên / Khách hàng', 'Mã hàng hóa', 'Họ tên nhân viên', 'Mã KH - Tên KH'],
    ['Tên hàng hóa / Phòng ban', 'Tên hàng hóa', 'Phòng ban của nhân viên', 'Trống'],
    ['Đơn vị', 'Đơn vị tính (có ô chọn nếu hàng có nhiều đơn vị)', 'Trống', 'Trống'],
    ['Model', 'Model', 'Trống', 'Trống'],
    ['Thương hiệu', 'Thương hiệu', 'Trống', 'Trống'],
    ['Tổng SL trong kho', 'Tổng tồn kho kế toán', 'Trống', 'Trống'],
    ['SL giữ', 'Tổng SL giữ của hàng hóa', 'Tổng SL nhân viên này giữ', 'SL của lô'],
    ['Hạn giữ', 'Trống', 'Trống', 'Ngày hết hạn giữ dd/mm/yyyy'],
    ['Trạng thái', 'Trống', 'Trống', 'Trong hạn / Đến hạn / Hết hạn'],
    ['Hành động', 'Trống', 'Trống', 'Nút Lịch sử giữ hàng (biểu tượng đồng hồ)'],
])
b.para('Ô để trống ở tầng hàng hóa và tầng nhân viên là đúng thiết kế: một hàng hóa có nhiều lô '
       'với hạn giữ khác nhau nên chỉ tầng lô mới có Hạn giữ và Trạng thái.')
b.para('Cột Tổng SL trong kho để trống nghĩa là hàng hóa đó chưa có tồn kho kế toán. Số lượng '
       'hiển thị theo chuẩn 1,234.5 (dấu phẩy ngăn hàng nghìn, dấu chấm phần thập phân).')

b.h2('3. Sắp xếp')
b.para('Bốn cột có biểu tượng mũi tên ở tiêu đề sắp xếp được: Mã hàng hóa / Nhân viên / Khách '
       'hàng, Tên hàng hóa / Phòng ban, Tổng SL trong kho và SL giữ. Bấm lần đầu sắp tăng dần, bấm '
       'lại để đổi tăng / giảm. Muốn bỏ sắp xếp, bấm Làm mới ở khối bộ lọc.')
b.para('Sắp xếp áp cho các dòng hàng hóa. Bên trong mỗi hàng hóa, nhân viên luôn sắp theo tên, '
       'các lô sắp theo tên khách hàng rồi hạn giữ.')

b.h2('4. Phân trang')
b.para('Cuối bảng có ô "Số dòng/trang" (5, 10, 20, 50, 100 — mặc định 10) và các nút chuyển trang. '
       'Mỗi "dòng" ở đây là một hàng hóa. Lật trang hoặc đổi số dòng sẽ thu gọn mọi hàng hóa đang '
       'mở chi tiết.')

b.h2('5. Các nút trên thanh công cụ')
b.table([
    ['Nút', 'Tác dụng'],
    ['In', 'Mở cửa sổ xem trước bản in danh sách theo bộ lọc đang áp (Phần 7).'],
    ['Xuất Excel', 'Mở cửa sổ chọn trường rồi tải danh sách về máy (Phần 6).'],
    ['Biểu tượng cột', 'Mở cửa sổ Tuỳ chỉnh cột (Phần 3 mục 4).'],
])
b.para('Màn hình không có nút Thêm mới, Sửa, Xóa hay Nhập file — đây là màn chỉ đọc.')

# =================================================== PHAN 3
b.h1('PHẦN 3: TÌM KIẾM, LỌC VÀ TUỲ CHỈNH HIỂN THỊ')

b.para('Yêu cầu quyền: Quản lý giữ hàng.')

b.h2('1. Ô tìm nhanh theo khách hàng')
b.para('Ô "Nhập tên, số điện thoại hoặc mã KH để tìm kiếm" tìm theo KHÁCH HÀNG được giữ hàng, '
       'không phải theo hàng hóa. Gõ một phần tên, mã hoặc số điện thoại của khách rồi bấm nút '
       'Tìm kiếm. Ô này chỉ có tác dụng khi bạn bấm Tìm kiếm.')
b.para('Kết quả chỉ còn những hàng hóa có lô giữ cho khách khớp từ khóa; mở chi tiết cũng chỉ thấy '
       'các lô của khách đó.')

b.h2('2. Bộ lọc nâng cao')
b.para('Bấm "Tìm kiếm nâng cao" để mở thêm các ô lọc. Khác với ô tìm nhanh, chỉ cần đổi giá trị '
       'một ô lọc nâng cao là danh sách tự nạp lại. Bấm "Ẩn tìm kiếm nâng cao" để thu gọn, điều '
       'kiện đã chọn vẫn giữ.')
b.image('02-bo-loc-nang-cao.png', 'Khu vực Tìm kiếm nâng cao đang mở')
b.table([
    ['Ô lọc', 'Cách dùng'],
    ['Mã hàng hóa', 'Gõ một phần mã hàng hóa.'],
    ['Tên hàng hóa', 'Gõ một phần tên hàng hóa.'],
    ['Lọc theo kho', 'Chọn một kho kế toán (dạng "Mã - Tên"). Danh sách gồm cả kho đang chờ xóa. '
                     'Kết quả chỉ còn hàng hóa CÓ ghi nhận tồn kho kế toán ở kho đó. Lưu ý: hàng '
                     'giữ không gắn với kho, nên SL giữ và Tổng SL trong kho không đổi theo kho.'],
    ['Thương hiệu', 'Chỉ liệt kê thương hiệu của hàng hóa đang có hàng giữ mà bạn được xem.'],
    ['Model', 'Chỉ liệt kê model của hàng hóa đang có hàng giữ mà bạn được xem.'],
    ['Trạng thái', 'Trong hạn / Hết hạn / Đến hạn. Lọc theo trạng thái của từng lô.'],
    ['Nhân viên', 'Chỉ liệt kê nhân viên ĐANG giữ hàng trong phạm vi bạn được xem; thu hẹp theo '
                  'Công ty / Phòng ban đang chọn.'],
    ['Công ty', 'Chỉ hiện nếu bạn có quyền xem theo tổng công ty. Biểu tượng ổ khóa cạnh nhãn là '
                'công tắc "Hiện cả công ty đã khoá".'],
    ['Phòng ban', 'Lọc các lô theo phòng ban của nhân viên giữ. Biểu tượng ổ khóa là công tắc '
                  '"Hiện cả phòng ban đã khoá". Đổi Công ty hoặc Phòng ban thì ô Nhân viên tự '
                  'xóa giá trị đang chọn.'],
])
b.para('Nút "Làm mới" xóa sạch mọi điều kiện lọc và thứ tự sắp xếp rồi nạp lại danh sách đầy đủ.')

b.h2('3. Chọn ô lọc muốn hiển thị')
b.para('Bấm "Cài đặt bộ lọc". Cửa sổ liệt kê tám mục: Mã hàng hóa, Tên hàng hóa, Lọc theo kho, '
       'Thương hiệu, Model, Trạng thái, Nhân viên, Công ty – Phòng ban.')
b.image('03-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc')
b.bullet('Tích / bỏ tích để hiện / ẩn ô lọc.')
b.bullet('Kéo biểu tượng sáu chấm để đổi thứ tự.')
b.bullet('Bấm Lưu để áp dụng; Khôi phục mặc định để quay về đủ tám mục ban đầu; Đóng để thoát '
         'không lưu.')
b.para('Cài đặt được lưu theo từng màn hình, không ảnh hưởng màn khác.')

b.h2('4. Chọn cột hiển thị của bảng')
b.para('Bấm nút biểu tượng cột ở góc phải thanh công cụ. Cửa sổ "Tuỳ chỉnh cột" liệt kê mười một '
       'cột.')
b.image('04-cau-hinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột')
b.bullet('Ba cột STT, Mã hàng hóa / Nhân viên / Khách hàng và Hành động bị khóa, luôn hiện.')
b.bullet('Các cột còn lại tích / bỏ tích và kéo biểu tượng ba gạch để đổi thứ tự.')
b.bullet('Bấm Lưu để áp dụng, Đóng để thoát không lưu. Cấu hình lưu riêng cho tài khoản của bạn.')

b.h2('5. Đổi đơn vị hiển thị')
b.para('Với hàng hóa có từ hai đơn vị tính trở lên, cột Đơn vị là một ô chọn. Chọn đơn vị khác '
       '(ví dụ "Hộp (x10)") thì mọi số lượng của hàng hóa đó — Tổng SL trong kho, SL giữ ở cả ba '
       'tầng và số trong cửa sổ Lịch sử giữ hàng — được quy đổi theo đơn vị mới, làm tròn xuống '
       '2 chữ số thập phân.')
b.para('Việc đổi đơn vị chỉ để xem, không lưu lại; tải lại trang thì về đơn vị cơ bản. Hàng hóa '
       'chỉ có một đơn vị thì cột Đơn vị chỉ hiện chữ.')

# =================================================== PHAN 4
b.h1('PHẦN 4: XEM CHI TIẾT AI ĐANG GIỮ, GIỮ CHO KHÁCH NÀO')

b.para('Yêu cầu quyền: Quản lý giữ hàng.')

b.h2('1. Mở chi tiết một hàng hóa')
b.para('Bấm nút tròn ">" ở cột STT của hàng hóa cần xem. Nút chuyển sang biểu tượng quay trong lúc '
       'tải, sau đó các dòng nhân viên và dòng khách hàng chèn ngay bên dưới, nút đổi thành "v".')
b.image('05-mo-rong-nhan-vien-khach-hang.png',
        'Chi tiết hàng hóa: dòng nhân viên và dòng khách hàng')
b.bullet('Dòng nhân viên: họ tên, phòng ban và tổng SL nhân viên đó đang giữ hàng hóa này.')
b.bullet('Dòng khách hàng: "Mã KH - Tên KH", SL của lô, hạn giữ, trạng thái và nút Lịch sử giữ '
         'hàng.')
b.para('Kéo thanh cuộn ngang sang phải để xem các cột Hạn giữ, Trạng thái và Hành động.')
b.image('06-cot-han-giu-trang-thai.png', 'Cột Hạn giữ, Trạng thái và nút Lịch sử ở dòng khách hàng')

b.h2('2. Những điều cần biết khi mở chi tiết')
b.bullet('Chi tiết áp CÙNG bộ lọc đang dùng: đang lọc theo khách hàng, nhân viên, trạng thái hay '
         'phòng ban thì chi tiết chỉ hiện các lô khớp điều kiện đó.')
b.bullet('Bạn có thể mở nhiều hàng hóa cùng lúc. Bấm "v" để thu gọn.')
b.bullet('Đổi bộ lọc, sắp xếp hoặc chuyển trang thì mọi hàng hóa đang mở tự thu gọn.')
b.bullet('Tải lỗi thì phần mềm báo "Lỗi khi tải chi tiết giữ hàng" và không mở chi tiết.')
b.bullet('Trạng thái được tính theo ngày hôm nay, nên cùng một lô hôm qua "Đến hạn" thì hôm nay '
         'thành "Hết hạn".')

# =================================================== PHAN 5
b.h1('PHẦN 5: XEM LỊCH SỬ GIỮ HÀNG')

b.para('Yêu cầu quyền: Quản lý giữ hàng.')
b.para('Ở một dòng khách hàng (tầng 3), bấm nút biểu tượng đồng hồ ở cột Hành động. Cửa sổ "Lịch '
       'sử giữ hàng" mở ra, dòng phụ dưới tiêu đề ghi "Hàng hóa: <mã> - <tên>".')
b.image('07-lich-su-giu-hang.png', 'Cửa sổ Lịch sử giữ hàng')

b.h2('1. Khối thông tin')
b.table([
    ['Ô', 'Nội dung'],
    ['Mã hàng', 'Mã hàng hóa.'],
    ['Tên hàng', 'Tên hàng hóa.'],
    ['Kinh doanh', 'Mã và họ tên nhân viên đang giữ.'],
    ['Khách hàng', 'Mã và tên khách hàng.'],
    ['Trạng thái', 'Trạng thái lô kèm "(Hạn giữ hiện tại: dd/mm/yyyy)".'],
])

b.h2('2. Bảng biến động')
b.para('Dòng "Số lượng giữ hiện tại: <số> <đơn vị>" nằm ngay dưới tiêu đề bảng. Mỗi dòng của bảng '
       'là một lần số hàng giữ thay đổi, sắp từ CŨ đến MỚI:')
b.table([
    ['Cột', 'Ý nghĩa'],
    ['STT', 'Số thứ tự.'],
    ['SL biến động', 'Số tăng (dấu "+", chữ xanh lá) hoặc giảm (dấu "-", chữ đỏ).'],
    ['Ngày', 'Ngày phát sinh biến động.'],
    ['SL giữ', 'Số lượng giữ còn lại SAU lần biến động đó (số cộng dồn).'],
    ['Hạn giữ', 'Hạn giữ của lô.'],
    ['Chứng từ', 'Mã chứng từ gây ra biến động, ví dụ PXG (phiếu xuất giữ), PGHHG (gia hạn), '
                 'PPBHĐC… Bấm vào mã để mở chứng từ ở thẻ mới.'],
])
b.para('Vì cột SL giữ là số cộng dồn, bảng sắp từ cũ đến mới (khác các màn lịch sử khác sắp mới '
       'trước) để bạn đọc từ trên xuống thấy đúng diễn biến.')
b.para('Chưa có biến động nào thì bảng ghi "Chưa có biến động nào.". Tải lỗi thì hiện "Không tải '
       'được lịch sử giữ hàng." kèm nút Thử lại. Bấm Đóng để thoát.')

# =================================================== PHAN 6
b.h1('PHẦN 6: XUẤT EXCEL DANH SÁCH')

b.para('Yêu cầu quyền: Quản lý giữ hàng.')
b.para('Bấm nút "Xuất Excel" trên thanh công cụ. Cửa sổ "Chọn trường xuất Excel" mở ra với đủ 12 '
       'trường đã được tích sẵn.')
b.image('08-xuat-excel.png', 'Cửa sổ Chọn trường xuất Excel')
b.table([
    ['Thao tác', 'Cách làm'],
    ['Chọn trường', 'Tích / bỏ tích từng trường. Dòng cuối hiện "Đang chọn x/12 trường".'],
    ['Đổi thứ tự cột', 'Kéo biểu tượng ba gạch bên phải mỗi trường.'],
    ['Chọn nhanh', 'Bấm "Chọn tất cả" hoặc "Bỏ chọn hết".'],
    ['Xuất', 'Bấm "Xuất file". Tệp danh_sach_hang_giu.xlsx được tải về, phần mềm báo "Xuất Excel '
             'thành công".'],
    ['Thoát', 'Bấm Đóng.'],
])
b.para('Mười hai trường: Mã hàng hóa, Tên hàng hóa, ĐVT, Model, Thương hiệu, Nhân viên giữ, Phòng '
       'ban, Khách hàng, SL giữ, Tổng SL trong kho, Hạn giữ, Trạng thái.')
b.para('Tệp Excel khác bảng trên màn ở mấy điểm cần nhớ:')
b.bullet('Tệp là bảng PHẲNG: mỗi dòng là một lô (hàng hóa × nhân viên × khách hàng × hạn giữ), '
         'không có cây ba tầng. Cột STT luôn đứng đầu.')
b.bullet('Số lượng luôn theo đơn vị cơ bản (xem cột ĐVT), không theo đơn vị bạn đang chọn trên '
         'màn.')
b.bullet('Cột Tổng SL trong kho lặp lại trên mọi dòng của cùng một hàng hóa — đừng cộng dọc cột '
         'này.')
b.bullet('Các dòng sắp theo Phòng ban → Nhân viên → Tên hàng hóa, không theo thứ tự sắp xếp trên '
         'bảng.')
b.para('Tệp chứa toàn bộ lô khớp bộ lọc đang áp và luôn giới hạn trong phạm vi bạn được xem. Trong '
       'lúc đang xuất, nút bị khóa để tránh bấm hai lần.')

# =================================================== PHAN 7
b.h1('PHẦN 7: IN DANH SÁCH')

b.para('Yêu cầu quyền: Quản lý giữ hàng.')
b.para('Bấm nút "In" trên thanh công cụ. Cửa sổ "Xem trước danh sách hàng giữ" mở ngay trên màn '
       '(không mở thẻ mới). Bấm nút In trong cửa sổ để gửi lệnh in, hoặc bấm dấu × để đóng.')
b.image('09-in-danh-sach.png', 'Cửa sổ xem trước bản in danh sách hàng giữ')
b.para('Bản in khổ A4 ngang, gồm:')
b.bullet('Tiêu đề công ty và dòng "DANH SÁCH HÀNG GIỮ".')
b.bullet('Khối thông tin: Ngày in, Số phòng ban, Số nhân viên, Số mục hàng.')
b.bullet('Bảng gồm STT, Tên hàng hóa, Mã hàng, ĐVT, SL giữ, Hạn giữ, Khách hàng, Trạng thái.')
b.para('Bản in gom theo PHÒNG BAN → NHÂN VIÊN → MỤC HÀNG, khác cây trên màn (Hàng hóa → Nhân viên '
       '→ Khách hàng), để kế toán đối chiếu theo phòng ban như trước. Cột STT đánh số theo cấp: '
       '"1" là dòng phòng ban (ghi "Tên phòng - N nhân viên - M mục hàng"), "1.1" là dòng nhân viên '
       '(ghi "Họ tên - K mục hàng"), "1.1.1" là từng mục hàng. Nhân viên chưa gán phòng ban được gom '
       'vào nhóm "Chưa gán phòng ban".')
b.para('Số lượng trên bản in theo đơn vị cơ bản. Nếu danh sách vượt 10,000 dòng in, cửa sổ chỉ hiện '
       'lời nhắc thu hẹp bộ lọc hoặc dùng Xuất Excel, và không có nút In.')

# =================================================== PHAN 8
b.h1('PHẦN 8: NHỮNG ĐIỀU CẦN NHỚ')

b.bullet('Màn hình chỉ để xem; không thao tác nào ở đây làm thay đổi hàng giữ.')
b.bullet('Phải có quyền "Quản lý giữ hàng" mới xem được; quyền xem theo cấp chỉ quyết định bạn '
         'thấy dữ liệu của ai.')
b.bullet('Ô tìm nhanh tìm theo KHÁCH HÀNG, và phải bấm Tìm kiếm mới có tác dụng.')
b.bullet('Tổng ở dòng "Hiển thị a–b / N" là số hàng hóa, không phải số lô.')
b.bullet('Hạn giữ và Trạng thái chỉ có ở dòng khách hàng; ô trống ở dòng hàng hóa và nhân viên là '
         'bình thường.')
b.bullet('Trạng thái tính theo ngày hôm nay: Trong hạn, Đến hạn (đúng hôm nay), Hết hạn.')
b.bullet('Ô Lọc theo kho chỉ chọn ra hàng hóa có tồn kho ở kho đó; hàng giữ không gắn với kho.')
b.bullet('Xuất Excel và bản In luôn theo đơn vị cơ bản; Excel là bảng phẳng mỗi dòng một lô.')
b.bullet('Lịch sử giữ hàng sắp từ cũ đến mới; cột SL giữ là số còn lại sau mỗi lần biến động.')

b.finish()
