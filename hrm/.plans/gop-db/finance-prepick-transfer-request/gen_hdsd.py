# -*- coding: utf-8 -*-
"""Sinh HDSD man "Yeu cau dieu chuyen hang giu" tu khung HDSD_MAU.docx.

Anh chup that: ./prepick_transfer_shots (Playwright MCP, 1440x900, ngay 05/09/2026).
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

SHOTS = os.path.join(BASE, 'prepick_transfer_shots')
OUT = os.path.join(BASE, 'HDSD_Yeu cau dieu chuyen hang giu.docx')

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title='(Màn hình: Yêu cầu điều chuyển hàng giữ)',
                doc_title='HDSD - Yêu cầu điều chuyển hàng giữ')

# =============================================================== TONG QUAN
b.h1('TỔNG QUAN')

b.h2('1. Thuật ngữ sử dụng trong tài liệu')
b.table([
    ['Thuật ngữ', 'Ý nghĩa'],
    ['Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên '
                 'kinh doanh đứng tên giữ.'],
    ['Lô hàng giữ', 'Một dòng hàng giữ cụ thể, gồm: người giữ – khách hàng – hàng hóa – '
                    'hạn giữ – công ty.'],
    ['Điều chuyển hàng giữ', 'Chuyển hàng bạn đang giữ sang cho một nhân viên khác giữ, cho một '
                             'khách hàng khác. Hạn giữ giữ nguyên như cũ.'],
    ['Người nhận', 'Nhân viên sẽ đứng tên giữ hàng sau khi phiếu được duyệt xong.'],
    ['Khách hàng nhận', 'Khách hàng mà hàng sẽ được giữ cho sau khi phiếu được duyệt xong.'],
    ['Từ xuất giữ', 'Lô hàng giữ bạn chọn để lấy hàng chuyển đi, hiển thị dạng số lượng – '
                    'hạn giữ.'],
    ['Đang giữ', 'Số lượng còn lại của chính lô hàng giữ đã chọn.'],
    ['Có thể giữ', 'Số hàng còn trong kho có thể giữ tiếp. Đây là số tham khảo, khác với '
                   'cột Đang giữ.'],
    ['Không duyệt', 'Trạng thái phiếu bị cấp duyệt trả về. Đây cũng là trạng thái duy nhất cho '
                    'phép bạn sửa lại phiếu.'],
    ['TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán — ba cấp duyệt của phiếu.'],
])

b.h2('2. Cập nhật tài liệu')
b.table([
    ['Phiên bản', 'Ngày', 'Nội dung'],
    ['1.0', '05/09/2026', 'Ban hành lần đầu cho màn hình Yêu cầu điều chuyển hàng giữ trên '
                          'phân hệ Tài chính.'],
])

b.h2('3. Giới thiệu chung')
b.para('Màn hình Yêu cầu điều chuyển hàng giữ dùng khi bạn đang giữ hàng cho một khách hàng '
       'nhưng cần chuyển phần hàng đó sang cho đồng nghiệp khác giữ, phục vụ một khách hàng khác.')
b.para('Phiếu đi qua ba cấp duyệt: Trưởng phòng, Ban giám đốc (chỉ với phiếu thuộc diện phải '
       'trình) và cuối cùng là Kế toán. Hàng chỉ thực sự đổi chủ khi Kế toán duyệt ở bước cuối '
       'cùng. Hạn giữ của hàng giữ nguyên như lô cũ — điều chuyển KHÔNG kéo dài thời gian giữ.')
b.para('Màn hình này KHÔNG có bản nháp: bấm lưu là phiếu đi thẳng vào bước chờ Trưởng phòng '
       'duyệt. Chỉ khi phiếu bị trả về (trạng thái Không duyệt) bạn mới sửa hoặc xóa lại được.',
       bold_prefix='Quan trọng: ')
b.para('Đường dẫn truy cập: Phân hệ Tài chính → nhóm Giữ hàng → Phiếu Yêu cầu điều chuyển hàng '
       'giữ. Có thể gõ thẳng địa chỉ /finance/prepick-transfer-requests trên thanh địa chỉ '
       'trình duyệt.')
b.para('Mã phiếu do phần mềm tự sinh theo dạng ĐCHG kèm 5 chữ số, ví dụ ĐCHG-01307.')

b.h2('4. Quyền sử dụng và phạm vi dữ liệu')
b.para('Màn hình này không đòi hỏi quyền riêng để lập phiếu: mọi người dùng đã đăng nhập đều '
       'lập được phiếu điều chuyển cho hàng giữ của chính mình. Các quyền dưới đây quyết định '
       'bạn DUYỆT được phiếu ở cấp nào và NHÌN THẤY phiếu của những ai.',
       bold_prefix='Lưu ý: ')

b.h3('4.1. Bảng quyền của màn hình')
b.table([
    ['Tên quyền', 'Cho phép làm gì', 'Nút / phần tương ứng trên màn hình', 'Ghi chú'],
    ['Trưởng phòng duyệt hàng giữ',
     'Duyệt hoặc từ chối phiếu đang ở bước Chờ TP duyệt.',
     'Nút TP duyệt và nút Từ chối ở màn chi tiết; biểu tượng duyệt ở cột Hành động.',
     'Ngoài quyền còn phải là người quản lý phòng ban của NGƯỜI NHẬN, và cùng công ty với phiếu.'],
    ['Ban giám đốc duyệt hàng giữ',
     'Duyệt hoặc từ chối phiếu đang ở bước Chờ BGĐ duyệt.',
     'Nút BGĐ duyệt và nút Từ chối.', 'Phải cùng công ty với phiếu.'],
    ['Kế toán duyệt hàng giữ',
     'Duyệt hoặc từ chối phiếu đang ở bước Chờ KT duyệt. Đây là bước hàng thực sự đổi chủ.',
     'Nút KT duyệt và nút Từ chối.', 'Phải cùng công ty với phiếu.'],
    ['Xem phiếu hàng giữ theo tổng công ty', 'Xem phiếu của mọi công ty.',
     'Toàn bộ danh sách; ô lọc Công ty và Phòng ban.', 'Là phạm vi rộng nhất.'],
    ['Xem phiếu hàng giữ theo công ty', 'Xem phiếu thuộc công ty của mình.',
     'Danh sách; ô lọc Phòng ban.', '—'],
    ['Xem phiếu hàng giữ theo phòng ban',
     'Xem phiếu thuộc các phòng ban mình được phân công quản lý và phòng ban của chính mình.',
     'Danh sách.', '—'],
])

b.h3('4.2. Người dùng không có quyền nào ở trên')
b.para('Bạn vẫn vào được màn hình và lập được phiếu cho hàng giữ của chính mình. Danh sách chỉ '
       'hiển thị phiếu do bạn lập, cộng thêm những phiếu đang chờ chính bạn duyệt (nếu có). '
       'Các nút duyệt và từ chối không hiển thị.')

b.h3('4.3. Người dùng có quyền "Trưởng phòng duyệt hàng giữ"')
b.para('Bạn duyệt các phiếu ở trạng thái Chờ TP duyệt trong công ty mình, với điều kiện bạn '
       'quản lý phòng ban của NGƯỜI NHẬN hàng.')
b.para('Đây là điểm khác với màn Yêu cầu gia hạn hàng giữ: ở màn gia hạn, Trưởng phòng xét theo '
       'phòng ban ghi trên phiếu; ở màn này xét theo phòng ban của người sẽ NHẬN hàng.',
       bold_prefix='Chú ý: ')
b.para('Các bước duyệt: mở phiếu bằng cách bấm vào mã phiếu → xem lại danh sách hàng, lô nguồn '
       'và số lượng chuyển → bấm nút TP duyệt.')
b.para('Nếu bạn không quản lý phòng ban của người nhận, nút duyệt sẽ không hiển thị; trường hợp '
       'truy cập trực tiếp bằng đường dẫn, phần mềm báo lỗi không có quyền.')

b.h3('4.4. Người dùng có quyền "Ban giám đốc duyệt hàng giữ"')
b.para('Bạn duyệt các phiếu đang ở trạng thái Chờ BGĐ duyệt trong công ty mình. Không phải '
       'phiếu nào cũng đi qua bước này — chỉ những phiếu có giá trị hoặc tỉ lệ thu tiền của hợp '
       'đồng chưa đạt ngưỡng quy định mới phải trình Ban giám đốc.')

b.h3('4.5. Người dùng có quyền "Kế toán duyệt hàng giữ"')
b.para('Bạn duyệt bước cuối cùng. Ngay khi bạn bấm KT duyệt, phần mềm trừ hàng ở lô của người '
       'lập và cộng vào lô của người nhận với khách hàng nhận — đây là lúc hàng thực sự đổi chủ. '
       'Vì vậy hãy kiểm tra kỹ Người nhận, Khách hàng nhận và số lượng trước khi bấm duyệt.')

# =============================================================== PHAN 1
b.h1('PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')

b.h2('1. Cách vào màn hình')
b.bullet('Đăng nhập phần mềm.')
b.bullet('Chọn phân hệ Tài chính.')
b.bullet('Ở thanh menu bên trái, mở nhóm Hàng hoá - Dịch vụ - Vận chuyển → Giữ hàng.')
b.bullet('Bấm mục Phiếu Yêu cầu điều chuyển hàng giữ.')

b.h2('2. Bố cục màn hình danh sách')
b.image('01-danh-sach.png', 'Màn hình Yêu cầu điều chuyển hàng giữ lúc mới vào')
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
    ['Mã phiếu', 'Mã phiếu do phần mềm sinh. Bấm vào mã để mở màn chi tiết.'],
    ['Người tạo', 'Người đã lập phiếu.'],
    ['Ngày tạo', 'Ngày giờ lập phiếu.'],
    ['Người nhận', 'Nhân viên sẽ đứng tên giữ hàng sau khi phiếu được duyệt.'],
    ['Khách nhận', 'Khách hàng mà hàng sẽ được giữ cho sau khi phiếu được duyệt.'],
    ['Trạng thái', 'Chờ TP duyệt · Chờ BGĐ duyệt · Chờ KT duyệt (màu cam) · Đã duyệt '
                   '(xanh lá) · Không duyệt (đỏ).'],
    ['Người duyệt', 'Người duyệt ở bước gần nhất.'],
    ['Ngày duyệt', 'Thời điểm duyệt gần nhất.'],
    ['Người cập nhật / Ngày cập nhật', 'Lần chỉnh sửa gần nhất. Hai cột này ẩn sẵn.'],
    ['Phòng ban', 'Phòng ban của người lập phiếu. Cột này ẩn sẵn.'],
    ['Ghi chú', 'Ghi chú do người lập nhập. Cột này ẩn sẵn.'],
    ['Lý do không duyệt', 'Lý do cấp duyệt trả phiếu về. Cột này ẩn sẵn.'],
    ['Hành động', 'Các nút thao tác của từng dòng.'],
])
b.para('Ba cột có mũi tên sắp xếp là Mã phiếu, Ngày tạo và Ngày duyệt.')

b.h2('2. Tìm kiếm và lọc')
b.para('Ô tìm nhanh ở trên cùng tìm theo mã phiếu. Gõ xong bấm nút Tìm kiếm hoặc nhấn Enter.')
b.image('02-bo-loc-nang-cao.png', 'Bảng lọc nâng cao đang mở')
b.table([
    ['Tiêu chí lọc', 'Cách dùng'],
    ['Công ty', 'Chỉ hiện với người có quyền xem theo tổng công ty.'],
    ['Phòng ban', 'Chỉ hiện với người có quyền xem từ cấp công ty trở lên.'],
    ['Mã phiếu', 'Gõ một phần hoặc toàn bộ mã phiếu.'],
    ['Trạng thái', 'Chọn một trong năm trạng thái.'],
    ['Người nhận', 'Chọn nhân viên sẽ nhận hàng giữ.'],
    ['Khách nhận', 'Chọn khách hàng sẽ được giữ hàng.'],
    ['Người tạo', 'Chọn nhân viên đã lập phiếu.'],
    ['Người duyệt', 'Chọn nhân viên đã duyệt phiếu.'],
    ['Tên, mã hàng', 'Một ô chung cho cả tên và mã hàng hóa.'],
    ['Số hợp đồng', 'Tìm những phiếu có dòng hàng gắn hợp đồng khớp số bạn nhập.'],
    ['Ngày tạo từ / Ngày tạo đến', 'Khoảng ngày lập phiếu.'],
])
b.para('Các ô lọc nâng cao tự lọc lại ngay khi bạn chọn. Bấm Làm mới để xóa toàn bộ điều kiện.')
b.para('Điều kiện lọc Số hợp đồng cũng được áp cho bản in danh sách và tệp Excel xuất ra.',
       bold_prefix='Mẹo: ')

b.h2('3. Chọn ô lọc muốn hiển thị')
b.para('Màn này có tới 11 ô lọc nên nút Cài đặt bộ lọc rất hữu ích: bạn tắt bớt những ô không '
       'dùng và kéo ô hay dùng lên đầu.')
b.image('07-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc')

b.h2('4. Chọn cột hiển thị của bảng')
b.image('08-cau-hinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột')
b.para('Ba cột STT, Mã phiếu và Hành động có biểu tượng ổ khóa: luôn hiển thị. Năm cột Người '
       'cập nhật, Ngày cập nhật, Phòng ban, Ghi chú và Lý do không duyệt mặc định tắt.')

b.h2('5. Các nút trên thanh công cụ')
b.table([
    ['Nút', 'Tác dụng', 'Điều kiện hiển thị'],
    ['Tạo mới', 'Mở màn lập phiếu điều chuyển mới.', 'Luôn hiển thị.'],
    ['In', 'Mở bản in danh sách theo đúng điều kiện lọc đang áp.', 'Luôn hiển thị.'],
    ['Xuất Excel', 'Mở cửa sổ chọn trường rồi tải tệp Excel về máy.', 'Luôn hiển thị.'],
    ['Cấu hình cột hiển thị', 'Mở cửa sổ Tuỳ chỉnh cột.', 'Luôn hiển thị.'],
])

b.h2('6. Các thao tác trên từng dòng')
b.table([
    ['Thao tác', 'Tác dụng', 'Khi nào hiện'],
    ['Sửa (biểu tượng bút chì)', 'Mở màn sửa phiếu.',
     'Phiếu do chính bạn lập và đang ở trạng thái Không duyệt.'],
    ['Xóa (biểu tượng thùng rác)', 'Xóa hẳn phiếu.',
     'Phiếu do chính bạn lập và đang ở trạng thái Không duyệt.'],
    ['Duyệt (biểu tượng dấu tích)', 'Mở màn chi tiết để xem lại rồi ký duyệt.',
     'Phiếu đang chờ chính bạn duyệt ở đúng cấp của bạn.'],
    ['In (biểu tượng máy in)', 'Mở bản in của phiếu đó.', 'Luôn hiện.'],
    ['Lịch sử (biểu tượng đồng hồ)', 'Mở cửa sổ lịch sử thay đổi của phiếu.', 'Luôn hiện.'],
])
b.para('Cột Hành động KHÔNG có nút Từ chối. Muốn từ chối phiếu, bạn mở phiếu ra rồi bấm nút '
       'Từ chối ở cuối màn chi tiết.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 3
b.h1('PHẦN 3: LẬP PHIẾU ĐIỀU CHUYỂN')

b.para('Ở màn danh sách, bấm nút Tạo mới. Màn lập phiếu có bố cục giống hệt màn sửa dưới đây.')
b.image('05-sua-phieu.png', 'Màn lập / sửa phiếu yêu cầu điều chuyển hàng giữ')

b.h2('1. Khối Thông tin chung')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Người lập – Ngày lập', 'Chỉ hiển thị', 'Không', 'Tên bạn và ngày hôm nay',
     'Nằm ở góc phải tiêu đề khối.'],
    ['Người nhận', 'Ô chọn từ danh sách nhân viên', 'Có', 'Để trống',
     'Nhân viên sẽ đứng tên giữ hàng sau khi phiếu được duyệt.'],
    ['Khách hàng nhận', 'Ô chọn từ danh sách khách hàng', 'Có', 'Để trống',
     'Khách hàng mà hàng sẽ được giữ cho sau khi phiếu được duyệt.'],
    ['Ghi chú', 'Ô nhập chữ, tối đa 255 ký tự', 'Không', 'Để trống',
     'Ghi lý do điều chuyển để các cấp duyệt nắm được.'],
])

b.h2('2. Khối File đính kèm')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Chọn tệp', 'Nút chọn tệp từ máy', 'Không', 'Chưa có tệp đính kèm',
     'Nhận tệp PDF, ảnh, Word, Excel; mỗi tệp tối đa 13 MB. Đính kèm được nhiều tệp.'],
])

b.h2('3. Khối Chi tiết hàng hóa')
b.para('Bấm nút Thêm hàng hóa để mở popup chọn hàng.')
b.image('06-popup-chon-hang.png', 'Popup Hàng bạn đang giữ')
b.para('Popup liệt kê những hàng mà chính bạn đang giữ, cho MỌI khách hàng (khác với màn Yêu '
       'cầu hủy hàng giữ — nơi popup lọc theo một khách hàng). Tích các dòng cần chuyển rồi bấm '
       'nút Chọn.')
b.table([
    ['Cột', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Tên hàng hóa / Mã hàng hóa', 'Chỉ hiển thị', '—', 'Theo hàng đã chọn', 'Không sửa được.'],
    ['ĐVT', 'Chỉ hiển thị', '—', 'Đơn vị cơ bản của hàng hóa',
     'Ô này khóa vì hàng giữ luôn được ghi theo đơn vị cơ bản. Bấm biểu tượng chữ i bên cạnh '
     'tiêu đề cột để xem giải thích.'],
    ['Từ xuất giữ', 'Ô chọn lô hàng giữ', 'Có', 'Để trống',
     'Chọn lô nguồn để lấy hàng chuyển đi, hiển thị dạng số lượng – hạn giữ. Có nút tìm kiếm '
     'lô bên cạnh. Mỗi lô chỉ được chọn ở MỘT dòng.'],
    ['Có thể giữ', 'Chỉ hiển thị', '—', 'Theo tồn kho',
     'Số hàng còn trong kho có thể giữ tiếp. Đây là số tham khảo, KHÁC với cột Đang giữ.'],
    ['Đang giữ', 'Chỉ hiển thị', '—', 'Theo lô nguồn đã chọn',
     'Bấm vào con số này để mở lịch sử tăng giảm của lô đó.'],
    ['Chuyển', 'Ô nhập số', 'Có', 'Để trống',
     'Số lượng muốn chuyển sang người nhận. Phải lớn hơn 0 và không vượt quá số Đang giữ.'],
    ['Hạn giữ', 'Chỉ hiển thị', '—', 'Theo lô nguồn',
     'Hạn giữ GIỮ NGUYÊN sau khi chuyển — điều chuyển không kéo dài thời gian giữ hàng.'],
    ['Hợp đồng', 'Ô chọn từ popup', 'Không', 'Để trống',
     'Bấm nút tìm kiếm bên cạnh để chọn hợp đồng gắn cho dòng hàng.'],
    ['Nút xóa dòng', 'Nút biểu tượng thùng rác', '—', '—', 'Bỏ hẳn dòng hàng khỏi phiếu.'],
])

b.h2('4. Giá trị phần mềm điền sẵn khi lập phiếu mới')
b.bullet('Người lập: chính bạn. Ngày lập: ngày hôm nay.')
b.bullet('Phòng ban yêu cầu: phòng ban của bạn (chỉ hiện sau khi phiếu đã lưu).')
b.bullet('Trạng thái: Chờ TP duyệt ngay sau khi bấm Gửi duyệt — màn này không có bản nháp.')
b.bullet('Mã phiếu: phần mềm tự sinh khi lưu.')
b.bullet('Số Đang giữ và Hạn giữ của dòng: điền sẵn ngay khi bạn chọn lô ở ô Từ xuất giữ.')

b.h2('5. Các nút ở cuối màn')
b.table([
    ['Nút', 'Phần mềm làm gì', 'Sau khi bấm'],
    ['Gửi duyệt', 'Lưu phiếu và chuyển thẳng sang trạng thái Chờ TP duyệt, đồng thời báo cho '
                  'Trưởng phòng quản lý phòng ban của người nhận.',
     'Hiện thông báo thành công và quay về màn danh sách.'],
    ['Lưu và tiếp tục', 'Lưu phiếu rồi ở lại màn để lập tiếp phiếu mới.',
     'Màn hình được làm mới, không quay về danh sách. Chỉ có ở màn Tạo mới.'],
    ['Quay lại', 'Thoát khỏi màn lập phiếu.',
     'Nếu bạn đã nhập gì mà chưa lưu, phần mềm hỏi xác nhận trước khi rời trang.'],
])
b.para('Màn này KHÔNG có nút Lưu nháp. Bấm Gửi duyệt là phiếu đi ngay vào quy trình duyệt.',
       bold_prefix='Lưu ý: ')

b.h2('6. Các lỗi thường gặp khi lưu')
b.table([
    ['Tình huống', 'Phần mềm báo gì', 'Cách xử lý'],
    ['Chưa chọn Người nhận hoặc Khách hàng nhận', 'Bắt buộc phải chọn',
     'Chọn đủ hai ô ở khối Thông tin chung.'],
    ['Chưa thêm hàng hóa nào', 'Bắt buộc phải chọn',
     'Bấm Thêm hàng hóa để chọn hàng bạn đang giữ.'],
    ['Chưa chọn lô ở ô Từ xuất giữ',
     'Từ xuất giữ – Lô hàng giữ không còn tồn tại hoặc không thuộc người lập phiếu.',
     'Chọn lô nguồn cho từng dòng hàng.'],
    ['Chọn cùng một lô ở hai dòng', 'Từ xuất giữ – Lô hàng giữ này đã được chọn ở dòng …',
     'Mỗi lô chỉ chọn ở một dòng; xóa dòng thừa hoặc chọn lô khác.'],
    ['Lô đã hết hạn giữ', 'Từ xuất giữ – Lô hàng đã hết hạn giữ ngày …',
     'Chọn lô còn hạn, hoặc lập phiếu gia hạn trước.'],
    ['Số lượng bằng 0', 'Số lượng chuyển – Phải lớn hơn 0.', 'Nhập số lớn hơn 0.'],
    ['Số lượng vượt số Đang giữ', 'Số lượng chuyển – Không được vượt số đang giữ (…)',
     'Nhập lại số nhỏ hơn hoặc bằng cột Đang giữ.'],
    ['Ghi chú quá 255 ký tự', 'Không được vượt quá 255 ký tự', 'Rút ngắn nội dung ghi chú.'],
])

# =============================================================== PHAN 4
b.h1('PHẦN 4: SỬA PHIẾU')

b.para('Bạn chỉ sửa được phiếu do chính mình lập và đang ở trạng thái Không duyệt, tức là phiếu '
       'đã bị một cấp duyệt trả về. Phiếu đang chờ duyệt hoặc đã duyệt thì không sửa được.',
       bold_prefix='Quan trọng: ')
b.para('Cách vào: bấm biểu tượng bút chì ở cột Hành động, hoặc mở phiếu ra rồi bấm nút Sửa ở '
       'cuối màn chi tiết.')
b.para('Màn sửa có bố cục giống màn lập phiếu, thêm ba ô chỉ hiển thị: Mã phiếu, Trạng thái '
       '(nhãn đỏ Không duyệt) và Phòng ban yêu cầu. Không có nút Lưu và tiếp tục.')
b.para('Sau khi bạn sửa xong và bấm Gửi duyệt, phần mềm XÓA dấu duyệt của cả ba cấp và đưa '
       'phiếu về bước Chờ TP duyệt. Phiếu đi lại quy trình duyệt từ đầu.',
       bold_prefix='Lưu ý: ')

# =============================================================== PHAN 5
b.h1('PHẦN 5: XEM CHI TIẾT PHIẾU')

b.para('Bấm vào mã phiếu ở cột thứ hai của bảng danh sách để mở màn chi tiết.')
b.image('03-chi-tiet.png', 'Màn chi tiết phiếu ở chế độ chỉ đọc')
b.para('Màn chi tiết gồm các khối:')
b.bullet('Thông tin chung: Mã phiếu, Trạng thái, Phòng ban yêu cầu, Người nhận, Khách hàng '
         'nhận, Ghi chú, người lập và ngày lập.')
b.bullet('File đính kèm: danh sách tệp, bấm vào tên tệp để mở xem.')
b.bullet('Chi tiết: bảng hàng hóa với lô nguồn, số lượng chuyển, hạn giữ và hợp đồng.')
b.bullet('Lịch sử duyệt: ai đã duyệt ở cấp nào, lúc nào, ghi chú gì.')
b.bullet('Lịch sử thay đổi, mặc định thu gọn.')
b.para('Bấm vào con số ở cột Đang giữ để mở lịch sử tăng giảm của lô hàng giữ đó.',
       bold_prefix='Mẹo: ')
b.para('Các nút ở cuối màn chi tiết luôn khớp với các nút ở cột Hành động ngoài danh sách của '
       'đúng phiếu đó, riêng nút Từ chối thì chỉ có ở màn chi tiết.')

# =============================================================== PHAN 6
b.h1('PHẦN 6: DUYỆT VÀ TỪ CHỐI PHIẾU')

b.h2('1. Luồng duyệt ba cấp')
b.para('Sau khi người lập bấm Gửi duyệt, phiếu đi theo trình tự:')
b.bullet('Chờ TP duyệt: chờ Trưởng phòng quản lý phòng ban của NGƯỜI NHẬN.')
b.bullet('Chờ BGĐ duyệt: chỉ những phiếu thuộc diện phải trình Ban giám đốc mới qua bước này.')
b.bullet('Chờ KT duyệt: bước cuối cùng do Kế toán thực hiện.')
b.bullet('Đã duyệt: hàng đã chuyển sang người nhận và khách hàng nhận.')
b.para('Phiếu có phải qua Ban giám đốc hay không do phần mềm tự xác định, dựa trên tỉ lệ tiền '
       'đã thu của hợp đồng gắn ở từng dòng, hoặc tổng giá trị hàng chuyển với những dòng không '
       'gắn hợp đồng.')

b.h2('2. Cách duyệt một phiếu')
b.bullet('Mở phiếu bằng cách bấm vào mã phiếu, hoặc bấm biểu tượng dấu tích ở cột Hành động.')
b.bullet('Xem lại Người nhận, Khách hàng nhận, lô nguồn của từng dòng và số lượng chuyển.')
b.bullet('Bấm nút duyệt ở cuối màn. Nhãn nút nêu rõ cấp bạn đang ký: TP duyệt, BGĐ duyệt hoặc '
         'KT duyệt. Rê chuột vào nút để xem chú thích phiếu sẽ đi đâu tiếp.')
b.para('Người duyệt KHÔNG sửa được số lượng và lô nguồn. Nếu thấy sai, hãy từ chối phiếu để '
       'người lập sửa lại.', bold_prefix='Lưu ý: ')
b.para('Sau khi duyệt, phần mềm hiện thông báo Duyệt phiếu thành công, đưa bạn về màn danh sách '
       'và báo cho cấp kế tiếp. Với bước Kế toán, phần mềm đồng thời chuyển hàng sang người '
       'nhận: trừ ở lô cũ, cộng vào lô của người nhận với khách hàng nhận, giữ nguyên hạn giữ.')

b.h2('3. Cách từ chối một phiếu')
b.image('11-popup-tu-choi.png', 'Cửa sổ Từ chối yêu cầu điều chuyển hàng giữ')
b.bullet('Mở phiếu và bấm nút Từ chối ở cuối màn chi tiết.')
b.bullet('Phần mềm mở cửa sổ có hiển thị mã phiếu.')
b.bullet('Nhập lý do trả phiếu về (bắt buộc, tối đa 255 ký tự) rồi bấm nút xác nhận.')
b.para('Phiếu chuyển sang trạng thái Không duyệt (nhãn đỏ) và chỉ người lập nhìn thấy. Đây cũng '
       'là trạng thái duy nhất cho phép người lập sửa hoặc xóa phiếu.')
b.para('Nhãn nút là "Từ chối" nhưng trạng thái phiếu hiển thị là "Không duyệt" — hai chữ khác '
       'nhau là có chủ ý: nút theo bộ chữ chuẩn của phần mềm, trạng thái theo tên nghiệp vụ '
       'sẵn có.', bold_prefix='Chú ý: ')

b.h2('4. Khi hai người cùng xử lý một phiếu')
b.para('Nếu phiếu đã được người khác duyệt hoặc từ chối trước đó, phần mềm báo "Phiếu không ở '
       'trạng thái chờ duyệt." và không thực hiện thao tác của bạn. Hãy tải lại danh sách để '
       'xem trạng thái mới nhất.')

# =============================================================== PHAN 7
b.h1('PHẦN 7: XÓA PHIẾU')

b.para('Chỉ người lập phiếu mới xóa được, và chỉ khi phiếu đang ở trạng thái Không duyệt. '
       'Phiếu đang chờ duyệt hoặc đã duyệt không xóa được.')
b.image('12-xac-nhan-xoa.png', 'Hộp thoại Xác nhận xóa phiếu')
b.bullet('Bấm biểu tượng thùng rác ở cột Hành động, hoặc nút Xóa ở cuối màn chi tiết.')
b.bullet('Phần mềm hỏi xác nhận, có ghi rõ mã phiếu để tránh xóa nhầm.')
b.bullet('Bấm Xóa để xác nhận, hoặc Hủy để thoát.')
b.para('Phiếu đã xóa không khôi phục lại được.')

# =============================================================== PHAN 8
b.h1('PHẦN 8: IN VÀ XUẤT EXCEL')

b.h2('1. In một phiếu')
b.para('Bấm biểu tượng máy in ở cột Hành động, hoặc nút In ở cuối màn chi tiết. Phần mềm mở một '
       'tab mới hiển thị bản xem trước khổ A4 ngang.')
b.image('04-in-phieu.png', 'Bản in phiếu yêu cầu điều chuyển hàng giữ')
b.para('Bản in gồm: phần đầu chứng từ theo công ty ghi trên phiếu, thông tin người yêu cầu, '
       'phòng ban và người nhận, bảng hàng hóa kèm dòng Tổng cộng, bảng lịch sử duyệt và bốn ô '
       'ký tên (Người lập, Trưởng phòng, Ban giám đốc, Kế toán).')

b.h2('2. In danh sách')
b.para('Bấm nút In trên thanh công cụ của màn danh sách.')
b.image('10-in-danh-sach.png', 'Bản in danh sách phiếu yêu cầu điều chuyển hàng giữ')
b.para('Bản in danh sách in đúng những phiếu khớp điều kiện lọc bạn đang áp, không chỉ trang '
       'đang xem.')

b.h2('3. Xuất Excel')
b.para('Bấm nút Xuất Excel trên thanh công cụ.')
b.image('09-chon-truong-xuat-excel.png', 'Cửa sổ Chọn trường xuất Excel')
b.bullet('Mặc định chọn sẵn cả 13 trường: Mã phiếu, Người tạo, Ngày tạo, Người nhận, Khách '
         'nhận, Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, Phòng ban, '
         'Ghi chú, Lý do không duyệt.')
b.bullet('Bỏ chọn trường không cần bằng cách bấm dấu nhân trên thẻ tên trường.')
b.bullet('Thứ tự cột trong tệp chạy theo đúng thứ tự bạn chọn.')
b.bullet('Bấm Xuất file để tải tệp về máy.')

# =============================================================== PHAN 9
b.h1('PHẦN 9: XEM LỊCH SỬ THAY ĐỔI')

b.para('Có hai cách xem lịch sử của một phiếu:')
b.bullet('Bấm biểu tượng đồng hồ ở cột Hành động của màn danh sách.')
b.bullet('Mở phiếu ra, kéo xuống khối Lịch sử thay đổi rồi bấm nút Xem lịch sử.')
b.para('Danh sách hiển thị các mốc thao tác theo thứ tự mới nhất trước, mỗi mốc ghi rõ nhóm '
       'thao tác (tạo mới, chỉnh sửa, duyệt, từ chối), người thực hiện, thời điểm và những giá '
       'trị đã thay đổi.')
b.para('Các phiếu được lập từ trước khi phần mềm bật tính năng ghi lịch sử sẽ hiện dòng '
       '"Chưa có lịch sử thao tác nào." — đây không phải lỗi.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 10
b.h1('PHẦN 10: NHỮNG ĐIỀU CẦN NHỚ')

b.bullet('Màn này KHÔNG có bản nháp: bấm Gửi duyệt là phiếu vào ngay quy trình duyệt.')
b.bullet('Chỉ phiếu ở trạng thái Không duyệt mới sửa hoặc xóa lại được.')
b.bullet('Sửa lại phiếu thì phần mềm xóa dấu duyệt của cả ba cấp, phiếu đi lại từ đầu.')
b.bullet('Trưởng phòng duyệt xét theo phòng ban của NGƯỜI NHẬN, không phải người lập.')
b.bullet('Hàng chỉ đổi chủ khi Kế toán duyệt ở bước cuối cùng.')
b.bullet('Hạn giữ GIỮ NGUYÊN sau khi điều chuyển — muốn kéo dài thời gian giữ thì phải lập '
         'phiếu Yêu cầu gia hạn hàng giữ.')
b.bullet('Mỗi lô hàng giữ chỉ được chọn ở một dòng trong phiếu.')
b.bullet('Người duyệt không sửa được số lượng; muốn đổi thì phải từ chối để người lập sửa.')

print(b.finish())
