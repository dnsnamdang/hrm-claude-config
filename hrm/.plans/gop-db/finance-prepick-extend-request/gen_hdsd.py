# -*- coding: utf-8 -*-
"""Sinh HDSD man "Yeu cau gia han hang giu" tu khung HDSD_MAU.docx.

Anh chup that: ./prepick_extend_shots (Playwright MCP, 1440x900, ngay 05/09/2026).
Ngon ngu: NGUOI DUNG CUOI — khong dung thuat ngu code (xem hdsd-documenter SKILL.md).
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

SHOTS = os.path.join(BASE, 'prepick_extend_shots')
OUT = os.path.join(BASE, 'HDSD_Yeu cau gia han hang giu.docx')

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title='(Màn hình: Yêu cầu gia hạn hàng giữ)',
                doc_title='HDSD - Yêu cầu gia hạn hàng giữ')

# =============================================================== TONG QUAN
b.h1('TỔNG QUAN')

b.h2('1. Thuật ngữ sử dụng trong tài liệu')
b.table([
    ['Thuật ngữ', 'Ý nghĩa'],
    ['Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên '
                 'kinh doanh đứng tên giữ.'],
    ['Lô hàng giữ', 'Một dòng hàng giữ cụ thể, gồm: người giữ – khách hàng – hàng hóa – '
                    'hạn giữ – công ty. Mỗi lô có hạn giữ riêng.'],
    ['Hạn giữ', 'Ngày cuối cùng lô hàng còn được giữ. Quá ngày này lô bị coi là hết hạn giữ.'],
    ['Hạn giữ mới', 'Ngày mà bạn đề nghị gia hạn tới.'],
    ['Gia hạn hàng giữ', 'Kéo dài thời gian giữ hàng cho khách. Khi phiếu được duyệt xong, '
                         'phần mềm chuyển số lượng bạn xin gia hạn sang hạn giữ mới.'],
    ['Số ngày cảnh báo', 'Cấu hình chung, hiện là 7 ngày. Chỉ những lô sắp hết hạn trong '
                         'khoảng này mới hiện ra để lập phiếu gia hạn.'],
    ['Số ngày giữ tối đa', 'Cấu hình chung, hiện là 30 ngày. Hạn giữ mới không được vượt quá '
                           'ngày hôm nay cộng 30 ngày.'],
    ['Đang giữ', 'Số lượng còn lại của chính lô hàng giữ trên dòng đó.'],
    ['Có thể giữ', 'Số lượng hàng còn trong kho có thể giữ tiếp. Đây là số tham khảo, khác với '
                   'cột Đang giữ.'],
    ['TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán — ba cấp duyệt của phiếu.'],
])

b.h2('2. Cập nhật tài liệu')
b.table([
    ['Phiên bản', 'Ngày', 'Nội dung'],
    ['1.0', '05/09/2026', 'Ban hành lần đầu cho màn hình Yêu cầu gia hạn hàng giữ trên '
                          'phân hệ Tài chính.'],
])

b.h2('3. Giới thiệu chung')
b.para('Màn hình Yêu cầu gia hạn hàng giữ dùng để xin kéo dài thời gian giữ hàng cho khách. '
       'Khi một lô hàng bạn đang giữ sắp hết hạn mà khách chưa lấy hàng, bạn lập phiếu yêu cầu '
       'gia hạn để xin giữ thêm.')
b.para('Phiếu đi qua ba cấp duyệt: Trưởng phòng, Ban giám đốc (chỉ với phiếu thuộc diện phải '
       'trình Ban giám đốc) và cuối cùng là Kế toán. Hàng chỉ thực sự được gia hạn khi Kế toán '
       'duyệt ở bước cuối cùng.')
b.para('Đường dẫn truy cập: Phân hệ Tài chính → nhóm Giữ hàng → Yêu cầu gia hạn hàng giữ. '
       'Có thể gõ thẳng địa chỉ /finance/prepick-extend-requests trên thanh địa chỉ trình duyệt.')
b.para('Mã phiếu do phần mềm tự sinh theo dạng PGHHG kèm 5 chữ số, ví dụ PGHHG-01501. '
       'Bạn không phải tự đặt mã.')

b.h2('4. Quyền sử dụng và phạm vi dữ liệu')
b.para('Màn hình này không đòi hỏi quyền riêng để lập phiếu: mọi người dùng đã đăng nhập đều '
       'lập được phiếu gia hạn cho hàng giữ của chính mình. Các quyền dưới đây quyết định bạn '
       'DUYỆT được phiếu ở cấp nào và NHÌN THẤY phiếu của những ai.', bold_prefix='Lưu ý: ')

b.h3('4.1. Bảng quyền của màn hình')
b.table([
    ['Tên quyền', 'Cho phép làm gì', 'Nút / phần tương ứng trên màn hình', 'Ghi chú'],
    ['Trưởng phòng duyệt hàng giữ',
     'Duyệt hoặc từ chối phiếu đang ở bước Chờ TP duyệt.',
     'Nút TP duyệt và nút Từ chối ở màn chi tiết; hai biểu tượng duyệt và từ chối ở cột '
     'Hành động.',
     'Ngoài quyền còn phải là người quản lý đúng phòng ban ghi trên phiếu, và cùng công ty '
     'với phiếu.'],
    ['Ban giám đốc duyệt hàng giữ',
     'Duyệt hoặc từ chối phiếu đang ở bước Chờ BGĐ duyệt.',
     'Nút BGĐ duyệt và nút Từ chối.',
     'Phải cùng công ty với phiếu.'],
    ['Kế toán duyệt hàng giữ',
     'Duyệt hoặc từ chối phiếu đang ở bước Chờ KT duyệt. Đây là bước làm hàng thực sự được '
     'gia hạn.',
     'Nút KT duyệt và nút Từ chối.',
     'Phải cùng công ty với phiếu.'],
    ['Xem phiếu hàng giữ theo tổng công ty',
     'Xem phiếu của mọi công ty.', 'Toàn bộ danh sách; ô lọc Công ty và Phòng ban.',
     'Là phạm vi rộng nhất.'],
    ['Xem phiếu hàng giữ theo công ty',
     'Xem phiếu thuộc công ty của mình.', 'Danh sách; ô lọc Phòng ban.', '—'],
    ['Xem phiếu hàng giữ theo phòng ban',
     'Xem phiếu thuộc các phòng ban mình được phân công quản lý và phòng ban của chính mình.',
     'Danh sách.', '—'],
])

b.h3('4.2. Người dùng không có quyền nào ở trên')
b.para('Bạn vẫn vào được màn hình và lập được phiếu cho hàng giữ của chính mình. Danh sách chỉ '
       'hiển thị phiếu do bạn lập, cộng thêm những phiếu đang chờ chính bạn duyệt (nếu có). '
       'Các nút duyệt và từ chối không hiển thị.')

b.h3('4.3. Người dùng có quyền "Trưởng phòng duyệt hàng giữ"')
b.para('Bạn nhìn thấy các phiếu khác bản nháp trong cùng công ty với mình. Với phiếu đang ở '
       'trạng thái Chờ TP duyệt và thuộc phòng ban bạn quản lý, cột Hành động hiện thêm hai '
       'biểu tượng duyệt và từ chối; mở phiếu ra thì cuối màn có nút TP duyệt và Từ chối.')
b.para('Các bước duyệt: mở phiếu bằng cách bấm vào mã phiếu → xem lại các dòng hàng, bỏ tích '
       'những dòng không đồng ý gia hạn, sửa lại ô Hạn giữ mới nếu cần → bấm TP duyệt.')
b.para('Nếu bạn không quản lý phòng ban của phiếu, nút duyệt sẽ không hiển thị; trường hợp truy '
       'cập trực tiếp bằng đường dẫn, phần mềm báo lỗi không có quyền.')

b.h3('4.4. Người dùng có quyền "Ban giám đốc duyệt hàng giữ"')
b.para('Bạn duyệt các phiếu đang ở trạng thái Chờ BGĐ duyệt trong công ty mình. Không phải phiếu '
       'nào cũng đi qua bước này — chỉ những phiếu có giá trị hoặc tỉ lệ thu tiền của hợp đồng '
       'chưa đạt ngưỡng quy định mới phải trình Ban giám đốc.')
b.para('Nếu không có quyền này, nút BGĐ duyệt sẽ không hiển thị; trường hợp truy cập trực tiếp '
       'bằng đường dẫn, phần mềm báo lỗi không có quyền.')

b.h3('4.5. Người dùng có quyền "Kế toán duyệt hàng giữ"')
b.para('Bạn duyệt bước cuối cùng. Ngay khi bạn bấm KT duyệt, phần mềm trừ số lượng ở lô hàng '
       'giữ cũ và cộng vào lô có hạn giữ mới — đây là lúc hàng thực sự được gia hạn. Vì vậy hãy '
       'kiểm tra kỹ số lượng và hạn giữ mới trước khi bấm duyệt.')
b.para('Nếu không có quyền này, nút KT duyệt sẽ không hiển thị; trường hợp truy cập trực tiếp '
       'bằng đường dẫn, phần mềm báo lỗi không có quyền.')

# =============================================================== PHAN 1
b.h1('PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')

b.h2('1. Cách vào màn hình')
b.bullet('Đăng nhập phần mềm.')
b.bullet('Chọn phân hệ Tài chính.')
b.bullet('Ở thanh menu bên trái, mở nhóm Hàng hoá - Dịch vụ - Vận chuyển → Giữ hàng.')
b.bullet('Bấm mục Yêu cầu gia hạn hàng giữ.')

b.h2('2. Bố cục màn hình danh sách')
b.image('01-danh-sach.png', 'Màn hình Yêu cầu gia hạn hàng giữ lúc mới vào')
b.para('Màn hình chia làm hai khối:')
b.bullet('Khối Bộ lọc danh sách ở trên: ô tìm nhanh, nút Tìm kiếm, nút Làm mới, nút Cài đặt '
         'bộ lọc và nút Tìm kiếm nâng cao.')
b.bullet('Khối bảng danh sách ở dưới: thanh công cụ (Tạo mới, In, Xuất Excel, Cấu hình cột), '
         'bảng dữ liệu và thanh phân trang.')

# =============================================================== PHAN 2
b.h1('PHẦN 2: DANH SÁCH PHIẾU')

b.h2('1. Các cột của bảng')
b.table([
    ['Cột', 'Nội dung'],
    ['STT', 'Số thứ tự dòng, chạy liên tục theo trang.'],
    ['Mã phiếu', 'Mã phiếu do phần mềm sinh. Bấm vào mã để mở màn chi tiết. Bấm chuột phải để '
                 'mở ở tab mới.'],
    ['Người tạo', 'Người đã lập phiếu.'],
    ['Ngày tạo', 'Ngày giờ lập phiếu.'],
    ['Trạng thái', 'Đang tạo (xám) · Chờ TP duyệt · Chờ BGĐ duyệt · Chờ KT duyệt (ba trạng thái '
                   'chờ duyệt màu cam) · Đã duyệt (xanh lá).'],
    ['Người duyệt', 'Người duyệt ở bước gần nhất. Để trống khi chưa ai duyệt.'],
    ['Ngày duyệt', 'Thời điểm duyệt gần nhất.'],
    ['Người cập nhật / Ngày cập nhật', 'Lần chỉnh sửa gần nhất của phiếu.'],
    ['Phòng ban', 'Phòng ban của người lập phiếu. Cột này ẩn sẵn, bật lên trong Cấu hình cột.'],
    ['Ghi chú', 'Lý do xin gia hạn do người lập nhập. Cột này ẩn sẵn.'],
    ['Lý do từ chối', 'Lý do cấp duyệt trả phiếu về. Cột này ẩn sẵn.'],
    ['Hành động', 'Các nút thao tác của từng dòng.'],
])
b.para('Ba cột có mũi tên sắp xếp là Mã phiếu, Ngày tạo và Ngày duyệt. Bấm vào tiêu đề cột để '
       'đổi thứ tự tăng dần hoặc giảm dần.')

b.h2('2. Tìm kiếm và lọc')
b.para('Ô tìm nhanh ở trên cùng tìm theo mã phiếu. Gõ xong bấm nút Tìm kiếm hoặc nhấn phím '
       'Enter — phần mềm không tự tìm khi bạn đang gõ.')
b.para('Bấm nút Tìm kiếm nâng cao để mở bảng lọc chi tiết.')
b.image('02-bo-loc-nang-cao.png', 'Bảng lọc nâng cao đang mở')
b.table([
    ['Tiêu chí lọc', 'Cách dùng'],
    ['Công ty', 'Chỉ hiện với người có quyền xem theo tổng công ty.'],
    ['Phòng ban', 'Chỉ hiện với người có quyền xem từ cấp công ty trở lên. Danh sách phòng ban '
                  'thay đổi theo công ty đã chọn.'],
    ['Mã phiếu', 'Gõ một phần hoặc toàn bộ mã phiếu.'],
    ['Trạng thái', 'Chọn một trong năm trạng thái.'],
    ['Người tạo', 'Chọn nhân viên đã lập phiếu.'],
    ['Người duyệt', 'Chọn nhân viên đã duyệt phiếu.'],
    ['Tên hàng hóa', 'Tìm những phiếu có chứa hàng hóa khớp tên.'],
    ['Mã hàng hóa', 'Tìm những phiếu có chứa hàng hóa khớp mã.'],
    ['Ngày tạo từ / Ngày tạo đến', 'Khoảng ngày lập phiếu.'],
])
b.para('Các ô lọc nâng cao tự lọc lại ngay khi bạn chọn, không cần bấm nút. Bấm Làm mới để xóa '
       'toàn bộ điều kiện lọc và xem lại danh sách đầy đủ.')
b.para('Phần mềm ghi nhớ điều kiện lọc trong 10 phút. Quay lại màn hình trong khoảng thời gian '
       'đó, bạn thấy lại đúng bộ lọc cũ.', bold_prefix='Mẹo: ')

b.h2('3. Chọn ô lọc muốn hiển thị')
b.para('Bấm nút Cài đặt bộ lọc để tự chọn những ô lọc bạn hay dùng và kéo sắp xếp lại thứ tự. '
       'Cấu hình được lưu riêng cho tài khoản của bạn.')
b.image('03-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc')
b.bullet('Bỏ tích ô lọc không dùng để ẩn khỏi bảng lọc nâng cao.')
b.bullet('Kéo biểu tượng sáu chấm để đổi vị trí.')
b.bullet('Bấm Lưu để ghi lại, Khôi phục mặc định để trả về trạng thái ban đầu, Đóng để thoát '
         'mà không lưu.')

b.h2('4. Chọn cột hiển thị của bảng')
b.para('Bấm biểu tượng cột ở góc phải thanh công cụ (khi rê chuột hiện chữ Cấu hình cột hiển '
       'thị) để mở cửa sổ Tuỳ chỉnh cột.')
b.image('04-cau-hinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột')
b.para('Ba cột STT, Mã phiếu và Hành động có biểu tượng ổ khóa: luôn hiển thị, không tắt được. '
       'Ba cột Phòng ban, Ghi chú và Lý do từ chối mặc định tắt, bạn tự bật khi cần.')

b.h2('5. Các nút trên thanh công cụ')
b.table([
    ['Nút', 'Tác dụng', 'Điều kiện hiển thị'],
    ['Tạo mới', 'Mở màn lập phiếu yêu cầu gia hạn mới.', 'Luôn hiển thị.'],
    ['In', 'Mở bản in danh sách theo đúng điều kiện lọc đang áp.', 'Luôn hiển thị.'],
    ['Xuất Excel', 'Mở cửa sổ chọn trường rồi tải tệp Excel về máy.', 'Luôn hiển thị.'],
    ['Cấu hình cột hiển thị', 'Mở cửa sổ Tuỳ chỉnh cột.', 'Luôn hiển thị.'],
])

b.h2('6. Các thao tác trên từng dòng')
b.table([
    ['Thao tác', 'Tác dụng', 'Khi nào hiện'],
    ['Sửa (biểu tượng bút chì)', 'Mở màn sửa phiếu.',
     'Phiếu do chính bạn lập và đang ở trạng thái Đang tạo.'],
    ['Xóa (biểu tượng thùng rác)', 'Xóa hẳn phiếu.',
     'Phiếu do chính bạn lập và đang ở trạng thái Đang tạo.'],
    ['Duyệt (biểu tượng dấu tích)', 'Mở màn chi tiết để xem lại rồi ký duyệt.',
     'Phiếu đang chờ chính bạn duyệt ở đúng cấp của bạn.'],
    ['Từ chối (biểu tượng dấu nhân)', 'Mở cửa sổ nhập lý do trả phiếu về.',
     'Phiếu đang chờ chính bạn duyệt ở đúng cấp của bạn.'],
    ['In (biểu tượng máy in)', 'Mở bản in của phiếu đó.', 'Luôn hiện.'],
    ['Lịch sử (biểu tượng đồng hồ)', 'Mở cửa sổ lịch sử thay đổi của phiếu.', 'Luôn hiện.'],
])
b.para('Nút nào không dùng được thì phần mềm ẩn hẳn, không hiện nút mờ.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 3
b.h1('PHẦN 3: LẬP PHIẾU YÊU CẦU GIA HẠN')

b.para('Ở màn danh sách, bấm nút Tạo mới. Phần mềm mở màn lập phiếu và tự nạp sẵn tất cả các '
       'lô hàng giữ sắp hết hạn của chính bạn vào bảng Chi tiết.')
b.image('06-tao-moi.png', 'Màn lập phiếu yêu cầu gia hạn hàng giữ')

b.h2('1. Khối Thông tin chung')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Người lập – Ngày lập', 'Chỉ hiển thị', 'Không', 'Tên bạn và ngày hôm nay',
     'Nằm ở góc phải tiêu đề khối, không sửa được.'],
    ['Ghi chú', 'Ô nhập chữ, tối đa 255 ký tự', 'Có', 'Để trống',
     'Nêu lý do xin gia hạn. Cả ba cấp duyệt đều đọc dòng này nên hãy viết rõ ràng. '
     'Bỏ trống thì phần mềm báo lỗi đỏ ngay dưới ô và không lưu được.'],
])

b.h2('2. Khối File đính kèm')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Chọn tệp', 'Nút chọn tệp từ máy', 'Không', 'Chưa có tệp đính kèm',
     'Nhận tệp PDF, ảnh, Word, Excel; mỗi tệp tối đa 13 MB. Đính kèm được nhiều tệp. '
     'Mỗi tệp đã chọn có nút gỡ khỏi phiếu.'],
])

b.h2('3. Khối Chi tiết hàng hóa')
b.para('Bảng này KHÔNG có nút thêm dòng. Phần mềm tự liệt kê các lô hàng giữ thỏa mãn cả ba '
       'điều kiện: do chính bạn đứng tên giữ, còn hàng, và có hạn giữ trước ngày hôm nay cộng '
       '7 ngày.', bold_prefix='Quan trọng: ')
b.para('Nếu bạn không có lô nào sắp hết hạn, bảng sẽ trống kèm câu giải thích và bạn chưa lập '
       'được phiếu gia hạn.')
b.table([
    ['Cột', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Cần gia hạn (ô tích)', 'Ô tích', 'Không', 'Chưa tích',
     'Tích vào những dòng bạn muốn xin gia hạn. Dòng chưa tích bị làm mờ và không được gửi đi.'],
    ['Tên hàng hóa', 'Chỉ hiển thị', '—', 'Theo lô hàng giữ', 'Không sửa được.'],
    ['Khách hàng', 'Chỉ hiển thị', '—', 'Theo lô hàng giữ', 'Khách hàng đang được giữ hàng.'],
    ['Hợp đồng', 'Chỉ hiển thị', '—', 'Theo lô hàng giữ',
     'Số hợp đồng gắn với lô hàng, nếu có.'],
    ['ĐVT', 'Chỉ hiển thị', '—', 'Đơn vị cơ bản của hàng hóa',
     'Ô này khóa vì hàng giữ luôn được ghi theo đơn vị cơ bản. Bấm biểu tượng chữ i bên cạnh '
     'tiêu đề cột để xem giải thích.'],
    ['Có thể giữ', 'Chỉ hiển thị', '—', 'Theo tồn kho',
     'Số hàng còn trong kho có thể giữ tiếp. Đây là số tham khảo, KHÁC với cột Đang giữ.'],
    ['Đang giữ', 'Chỉ hiển thị', '—', 'Theo lô hàng giữ',
     'Số lượng còn lại của chính lô trên dòng đó.'],
    ['Cần gia hạn (số lượng)', 'Ô nhập số', 'Có, khi dòng đã tích', 'Bằng số Đang giữ',
     'Phải lớn hơn 0 và không vượt quá số Đang giữ. Nhập sai thì phần mềm báo đỏ ngay tại dòng '
     'và giữ nguyên con số bạn gõ.'],
    ['Ngày bắt đầu giữ', 'Chỉ hiển thị', '—', 'Theo lô hàng giữ', '—'],
    ['Hạn giữ hiện tại', 'Chỉ hiển thị', '—', 'Theo lô hàng giữ',
     'Ngày lô hàng sẽ hết hạn nếu không gia hạn.'],
    ['Hạn giữ mới', 'Ô chọn ngày', 'Có, khi dòng đã tích', 'Để trống',
     'Chọn ngày muốn gia hạn tới. Lịch chỉ cho chọn từ ngày mai đến hết ngày hôm nay cộng '
     '30 ngày.'],
    ['Lịch sử', 'Nút biểu tượng đồng hồ', '—', '—',
     'Mở cửa sổ xem lịch sử tăng giảm của lô hàng giữ đó.'],
])

b.h2('4. Giá trị phần mềm điền sẵn khi lập phiếu mới')
b.bullet('Người lập: chính bạn. Ngày lập: ngày hôm nay.')
b.bullet('Phòng ban yêu cầu: phòng ban của bạn (chỉ hiện sau khi phiếu đã lưu).')
b.bullet('Trạng thái: Đang tạo khi bấm Lưu nháp, Chờ TP duyệt khi bấm Gửi duyệt.')
b.bullet('Mã phiếu: phần mềm tự sinh khi lưu, bạn không phải nhập.')
b.bullet('Số lượng cần gia hạn của mỗi dòng: điền sẵn bằng đúng số Đang giữ ngay khi bạn tích '
         'ô Cần gia hạn.')

b.h2('5. Các nút lưu ở cuối màn')
b.table([
    ['Nút', 'Phần mềm làm gì', 'Sau khi bấm'],
    ['Lưu nháp', 'Lưu phiếu ở trạng thái Đang tạo, chưa gửi cho ai duyệt.',
     'Hiện thông báo lưu thành công và quay về màn danh sách.'],
    ['Gửi duyệt', 'Lưu phiếu và chuyển sang trạng thái Chờ TP duyệt, đồng thời báo cho Trưởng '
                  'phòng phụ trách.',
     'Hiện thông báo thành công và quay về màn danh sách.'],
    ['Lưu và tiếp tục', 'Lưu nháp phiếu này rồi ở lại màn để lập tiếp phiếu mới.',
     'Màn hình được làm mới, không quay về danh sách.'],
    ['Quay lại', 'Thoát khỏi màn lập phiếu.',
     'Nếu bạn đã nhập gì đó mà chưa lưu, phần mềm hỏi xác nhận trước khi rời trang.'],
])

b.h2('6. Các lỗi thường gặp khi lưu')
b.table([
    ['Tình huống', 'Phần mềm báo gì', 'Cách xử lý'],
    ['Bỏ trống Ghi chú', 'Bắt buộc phải nhập', 'Nhập lý do xin gia hạn rồi lưu lại.'],
    ['Chưa tích dòng nào', 'Chưa tích chọn hàng hoá nào cần gia hạn.',
     'Tích ít nhất một dòng ở cột Cần gia hạn.'],
    ['Số lượng bằng 0', 'Số lượng gia hạn – Phải lớn hơn 0.', 'Nhập số lớn hơn 0.'],
    ['Số lượng vượt số Đang giữ', 'Số lượng gia hạn – Không được vượt số đang giữ (…)',
     'Nhập lại số nhỏ hơn hoặc bằng số ở cột Đang giữ.'],
    ['Chưa chọn Hạn giữ mới', 'Hạn giữ mới – Bắt buộc nhập.', 'Chọn ngày ở ô Hạn giữ mới.'],
    ['Chọn hạn giữ mới là hôm nay hoặc ngày quá khứ',
     'Hạn giữ mới – Phải là ngày tương lai.', 'Chọn ngày từ ngày mai trở đi.'],
    ['Chọn hạn giữ mới quá xa', 'Hạn giữ mới – Không được giữ quá …',
     'Chọn ngày trong phạm vi 30 ngày kể từ hôm nay.'],
])

# =============================================================== PHAN 4
b.h1('PHẦN 4: SỬA PHIẾU')

b.para('Bạn chỉ sửa được phiếu do chính mình lập và đang ở trạng thái Đang tạo. Phiếu bị cấp '
       'duyệt trả về cũng quay lại trạng thái này nên sửa lại được.')
b.para('Cách vào: bấm biểu tượng bút chì ở cột Hành động của màn danh sách, hoặc mở phiếu ra '
       'rồi bấm nút Sửa ở cuối màn chi tiết.')
b.para('Màn sửa có bố cục giống hệt màn lập phiếu, khác ba điểm:')
b.bullet('Có thêm ba ô chỉ hiển thị: Mã phiếu, Trạng thái và Phòng ban yêu cầu.')
b.bullet('Các dòng bạn đã chọn được tích sẵn, đã điền sẵn số lượng và hạn giữ mới.')
b.bullet('Không có nút Lưu và tiếp tục.')
b.para('Phiếu đã gửi duyệt hoặc đã duyệt thì nút Sửa không hiển thị; nếu truy cập trực tiếp '
       'bằng đường dẫn, phần mềm từ chối và không mở màn sửa.')

# =============================================================== PHAN 5
b.h1('PHẦN 5: XEM CHI TIẾT PHIẾU')

b.para('Bấm vào mã phiếu ở cột thứ hai của bảng danh sách để mở màn chi tiết.')
b.image('07-chi-tiet.png', 'Màn chi tiết phiếu ở chế độ chỉ đọc')
b.para('Màn chi tiết gồm các khối:')
b.bullet('Thông tin chung: Mã phiếu, Trạng thái, Phòng ban yêu cầu, Ghi chú, người lập và '
         'ngày lập.')
b.bullet('File đính kèm: danh sách tệp, bấm vào tên tệp để mở xem.')
b.bullet('Chi tiết: bảng hàng hóa của phiếu.')
b.bullet('Lịch sử duyệt: ai đã duyệt hoặc từ chối ở cấp nào, lúc nào, ghi chú gì.')
b.bullet('Lịch sử thay đổi: các mốc thao tác trên phiếu, mặc định thu gọn.')
b.image('09-lich-su-duyet-va-thay-doi.png',
        'Khối Lịch sử duyệt và Lịch sử thay đổi ở màn chi tiết')
b.para('Trong bảng Lịch sử duyệt, dòng có nhãn xanh Đã duyệt là dòng ký duyệt, dòng có nhãn đỏ '
       'Từ chối là dòng trả phiếu về. Cột Ghi chú hiển thị lý do cấp đó ghi lại.')
b.para('Các nút ở cuối màn chi tiết luôn khớp với các nút ở cột Hành động ngoài danh sách của '
       'đúng phiếu đó.')

# =============================================================== PHAN 6
b.h1('PHẦN 6: DUYỆT VÀ TỪ CHỐI PHIẾU')

b.h2('1. Luồng duyệt ba cấp')
b.para('Sau khi người lập bấm Gửi duyệt, phiếu đi theo trình tự:')
b.bullet('Chờ TP duyệt: chờ Trưởng phòng phụ trách phòng ban của phiếu.')
b.bullet('Chờ BGĐ duyệt: chỉ những phiếu thuộc diện phải trình Ban giám đốc mới qua bước này.')
b.bullet('Chờ KT duyệt: bước cuối cùng do Kế toán thực hiện.')
b.bullet('Đã duyệt: hàng đã được gia hạn sang hạn giữ mới.')
b.para('Phiếu có phải qua Ban giám đốc hay không do phần mềm tự xác định, dựa trên tỉ lệ tiền '
       'đã thu của hợp đồng gắn với từng dòng hàng, hoặc tổng giá trị hàng xin gia hạn với '
       'những dòng không gắn hợp đồng. Người duyệt không phải chọn.')

b.h2('2. Cách duyệt một phiếu')
b.image('08-chi-tiet-nguoi-duyet.png',
        'Màn chi tiết dưới góc nhìn người duyệt — có nút duyệt và nút Từ chối')
b.bullet('Mở phiếu bằng cách bấm vào mã phiếu, hoặc bấm biểu tượng dấu tích ở cột Hành động.')
b.bullet('Xem lại từng dòng hàng. Bạn được phép bỏ tích ở cột Cần gia hạn với những dòng không '
         'đồng ý gia hạn.')
b.bullet('Bạn cũng được sửa lại ô Hạn giữ mới của từng dòng. Riêng số lượng thì không sửa được.')
b.bullet('Bấm nút duyệt ở cuối màn. Nhãn nút nêu rõ cấp bạn đang ký: TP duyệt, BGĐ duyệt hoặc '
         'KT duyệt.')
b.para('Sau khi duyệt, phần mềm hiện thông báo Duyệt phiếu thành công, đưa bạn về màn danh sách '
       'và báo cho cấp kế tiếp. Với bước Kế toán, phần mềm đồng thời chuyển số lượng sang hạn '
       'giữ mới.')
b.para('Nếu bạn bỏ tích hết tất cả các dòng rồi mới bấm duyệt, phần mềm báo "Phải giữ lại ít '
       'nhất 1 hàng hoá cần gia hạn thì mới duyệt được." và không duyệt.', bold_prefix='Lưu ý: ')

b.h2('3. Cách từ chối một phiếu')
b.image('12-popup-tu-choi.png', 'Cửa sổ Từ chối yêu cầu gia hạn hàng giữ')
b.bullet('Bấm nút Từ chối ở cuối màn chi tiết, hoặc biểu tượng dấu nhân ở cột Hành động.')
b.bullet('Phần mềm mở cửa sổ Từ chối yêu cầu gia hạn hàng giữ, có hiển thị mã phiếu.')
b.bullet('Nhập lý do trả phiếu về (bắt buộc, tối đa 255 ký tự) rồi bấm nút xác nhận.')
b.para('Phiếu quay về trạng thái Đang tạo để người lập sửa và gửi lại. Phần mềm không có trạng '
       'thái "Từ chối" riêng, nên lý do bạn ghi là thông tin duy nhất giúp người lập biết vì sao '
       'bị trả lại — hãy ghi cụ thể.', bold_prefix='Quan trọng: ')
b.para('Bỏ trống lý do thì phần mềm báo "Bắt buộc phải nhập lý do từ chối" và cửa sổ không đóng.')

b.h2('4. Khi hai người cùng xử lý một phiếu')
b.para('Nếu phiếu đã được người khác duyệt hoặc từ chối trước đó, phần mềm báo "Phiếu không ở '
       'trạng thái chờ duyệt." và không thực hiện thao tác của bạn. Hãy tải lại danh sách để '
       'xem trạng thái mới nhất.')

# =============================================================== PHAN 7
b.h1('PHẦN 7: XÓA PHIẾU')

b.para('Chỉ người lập phiếu mới xóa được, và chỉ khi phiếu đang ở trạng thái Đang tạo. '
       'Phiếu đã gửi duyệt hoặc đã duyệt không xóa được vì đã ảnh hưởng tới hàng giữ.')
b.image('13-xac-nhan-xoa.png', 'Hộp thoại Xác nhận xóa phiếu')
b.bullet('Bấm biểu tượng thùng rác ở cột Hành động, hoặc nút Xóa ở cuối màn chi tiết.')
b.bullet('Phần mềm hỏi xác nhận, có ghi rõ mã phiếu để tránh xóa nhầm.')
b.bullet('Bấm Xóa để xác nhận, hoặc Hủy để thoát.')
b.para('Xóa xong phần mềm hiện thông báo "Xóa thành công." và tải lại danh sách. Phiếu đã xóa '
       'không khôi phục lại được.')

# =============================================================== PHAN 8
b.h1('PHẦN 8: IN VÀ XUẤT EXCEL')

b.h2('1. In một phiếu')
b.para('Bấm biểu tượng máy in ở cột Hành động, hoặc nút In ở cuối màn chi tiết. Phần mềm mở '
       'một tab mới hiển thị bản xem trước đúng khổ giấy A4 dọc. Bấm nút In ở góc trên bên phải '
       'tờ giấy để gửi lệnh in.')
b.image('10-in-phieu.png', 'Bản in phiếu yêu cầu gia hạn hàng giữ')
b.para('Bản in gồm: phần đầu chứng từ theo công ty ghi trên phiếu, thông tin người yêu cầu và '
       'phòng ban, bảng hàng hóa kèm dòng Tổng cộng, bảng lịch sử duyệt và bốn ô ký tên '
       '(Người lập, Trưởng phòng, Ban giám đốc, Kế toán).')

b.h2('2. In danh sách')
b.para('Bấm nút In trên thanh công cụ của màn danh sách. Bản in danh sách dùng khổ A4 ngang và '
       'in đúng những phiếu khớp điều kiện lọc bạn đang áp, không chỉ trang đang xem.')
b.image('11-in-danh-sach.png', 'Bản in danh sách phiếu yêu cầu gia hạn hàng giữ')

b.h2('3. Xuất Excel')
b.para('Bấm nút Xuất Excel trên thanh công cụ. Phần mềm mở cửa sổ cho bạn chọn những cột muốn '
       'có trong tệp.')
b.image('05-chon-truong-xuat-excel.png', 'Cửa sổ Chọn trường xuất Excel')
b.bullet('Mặc định chọn sẵn cả 11 trường: Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người '
         'duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối.')
b.bullet('Bỏ chọn trường không cần bằng cách bấm dấu nhân trên thẻ tên trường.')
b.bullet('Thứ tự cột trong tệp chạy theo đúng thứ tự bạn chọn — muốn đổi vị trí thì bỏ chọn '
         'rồi chọn lại theo trình tự mong muốn.')
b.bullet('Bấm Xuất file để tải tệp về máy. Trong lúc đang xuất, nút bị khóa để tránh bấm hai lần.')
b.para('Tệp Excel chứa toàn bộ phiếu khớp điều kiện lọc trong phạm vi bạn được xem, không giới '
       'hạn ở trang đang mở.')

# =============================================================== PHAN 9
b.h1('PHẦN 9: XEM LỊCH SỬ THAY ĐỔI')

b.para('Có hai cách xem lịch sử của một phiếu:')
b.bullet('Bấm biểu tượng đồng hồ ở cột Hành động của màn danh sách.')
b.bullet('Mở phiếu ra, kéo xuống khối Lịch sử thay đổi rồi bấm nút Xem lịch sử.')
b.para('Danh sách hiển thị các mốc thao tác theo thứ tự mới nhất trước, mỗi mốc ghi rõ nhóm '
       'thao tác (tạo mới, chỉnh sửa, gửi duyệt, duyệt, từ chối), người thực hiện, thời điểm và '
       'những giá trị đã thay đổi: Trạng thái, Ghi chú, File đính kèm, danh sách hàng hóa, '
       'Số lượng gia hạn, Hạn giữ mới.')
b.para('Bấm Làm mới để tải lại. Bấm Thu gọn để đóng khối lại.')
b.para('Các phiếu được lập từ trước khi phần mềm bật tính năng ghi lịch sử sẽ hiện dòng '
       '"Chưa có lịch sử thao tác nào." — đây không phải lỗi.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 10
b.h1('PHẦN 10: NHỮNG ĐIỀU CẦN NHỚ')

b.bullet('Chỉ những lô hàng giữ SẮP HẾT HẠN trong 7 ngày tới của chính bạn mới hiện ra để lập '
         'phiếu. Không thấy hàng cần gia hạn nghĩa là hàng đó chưa tới hạn cảnh báo.')
b.bullet('Hạn giữ mới tối đa là 30 ngày kể từ hôm nay.')
b.bullet('Hàng chỉ thực sự được gia hạn khi Kế toán duyệt ở bước cuối cùng. Ba bước trước đó '
         'chưa thay đổi gì tới hàng giữ.')
b.bullet('Gia hạn không sửa hạn của lô cũ mà chuyển số lượng sang một lô mới có hạn giữ mới. '
         'Vì vậy sau khi duyệt, bạn sẽ thấy hai dòng biến động trong lịch sử của lô hàng.')
b.bullet('Ghi chú là bắt buộc — đây là chỗ duy nhất bạn giải thích lý do xin gia hạn cho cả ba '
         'cấp duyệt.')
b.bullet('Người duyệt được sửa Hạn giữ mới nhưng không sửa được số lượng.')
b.bullet('Phiếu bị từ chối quay về trạng thái Đang tạo, không phải trạng thái riêng — hãy đọc '
         'cột Lý do từ chối hoặc khối Lịch sử duyệt để biết vì sao.')

print(b.finish())
