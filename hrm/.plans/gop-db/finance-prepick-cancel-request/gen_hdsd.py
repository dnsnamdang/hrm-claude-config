# -*- coding: utf-8 -*-
"""Sinh HDSD man "Yeu cau huy hang giu" tu khung HDSD_MAU.docx.

Anh chup that: ./prepick_cancel_shots (Playwright MCP, 1440x900, ngay 05/09/2026).
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

SHOTS = os.path.join(BASE, 'prepick_cancel_shots')
OUT = os.path.join(BASE, 'HDSD_Yeu cau huy hang giu.docx')

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title='(Màn hình: Yêu cầu hủy hàng giữ)',
                doc_title='HDSD - Yêu cầu hủy hàng giữ')

# =============================================================== TONG QUAN
b.h1('TỔNG QUAN')

b.h2('1. Thuật ngữ sử dụng trong tài liệu')
b.table([
    ['Thuật ngữ', 'Ý nghĩa'],
    ['Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên '
                 'kinh doanh đứng tên giữ.'],
    ['Lô hàng giữ', 'Một dòng hàng giữ cụ thể, gồm: người giữ – khách hàng – hàng hóa – '
                    'hạn giữ – công ty.'],
    ['Yêu cầu hủy hàng giữ', 'Phiếu bạn lập để đề nghị trả lại kho phần hàng đang giữ mà khách '
                             'không lấy nữa. Mã phiếu dạng PYCHHG.'],
    ['Phiếu hủy hàng giữ', 'Chứng từ do người duyệt lập từ phiếu yêu cầu của bạn. Mã phiếu dạng '
                           'PHHG. Chính lúc lưu phiếu này hàng giữ mới thực sự bị trừ.'],
    ['Yêu cầu hủy', 'Số lượng bạn đề nghị hủy giữ.'],
    ['Duyệt hủy', 'Số lượng người duyệt thực sự chấp thuận hủy. Có thể ít hơn số bạn đề nghị.'],
    ['Có thể hủy', 'Số lượng còn có thể hủy của hàng hóa đó, đã trừ phần đang nằm trong đề nghị '
                   'xuất kho chưa xong.'],
    ['Có thể giữ', 'Số hàng còn trong kho có thể giữ tiếp tại thời điểm mở phiếu. Đây là số '
                   'tham khảo, khác với số đã yêu cầu hủy hoặc đã duyệt hủy.'],
])

b.h2('2. Cập nhật tài liệu')
b.table([
    ['Phiên bản', 'Ngày', 'Nội dung'],
    ['1.0', '05/09/2026', 'Ban hành lần đầu cho màn hình Yêu cầu hủy hàng giữ trên phân hệ '
                          'Tài chính.'],
])

b.h2('3. Giới thiệu chung')
b.para('Màn hình Yêu cầu hủy hàng giữ dùng khi bạn đang giữ hàng cho một khách hàng nhưng khách '
       'không lấy hàng nữa, và bạn muốn trả phần hàng đó về kho để bán cho người khác.')
b.para('Bạn lập phiếu yêu cầu, ghi rõ khách hàng và những hàng hóa muốn hủy giữ cùng số lượng. '
       'Người quản lý giữ hàng xem xét rồi hoặc trả phiếu về cho bạn kèm lý do, hoặc lập '
       'Phiếu hủy hàng giữ để chấp thuận. Hàng chỉ thực sự được trả về kho khi phiếu hủy '
       'được lưu.')
b.para('Đường dẫn truy cập: Phân hệ Tài chính → nhóm Giữ hàng → Yêu cầu hủy hàng giữ. '
       'Có thể gõ thẳng địa chỉ /finance/prepick-cancel-requests trên thanh địa chỉ trình duyệt.')
b.para('Mã phiếu do phần mềm tự sinh theo dạng PYCHHG kèm 5 chữ số, ví dụ PYCHHG-03530.')

b.h2('4. Quyền sử dụng và phạm vi dữ liệu')
b.para('Màn hình này không đòi hỏi quyền riêng để lập phiếu: mọi người dùng đã đăng nhập đều '
       'lập được phiếu yêu cầu hủy cho hàng giữ của chính mình. Các quyền dưới đây quyết định '
       'bạn có DUYỆT được phiếu hay không và NHÌN THẤY phiếu của những ai.',
       bold_prefix='Lưu ý: ')

b.h3('4.1. Bảng quyền của màn hình')
b.table([
    ['Tên quyền', 'Cho phép làm gì', 'Nút / phần tương ứng trên màn hình', 'Ghi chú'],
    ['Quản lý giữ hàng',
     'Duyệt (bằng cách lập Phiếu hủy hàng giữ) hoặc không duyệt phiếu đang ở trạng thái '
     'Chờ duyệt. Ngoài ra được xem mọi phiếu khác bản nháp.',
     'Nút "Tạo phiếu hủy hàng giữ" và nút "Không duyệt" ở màn chi tiết; biểu tượng duyệt ở '
     'cột Hành động.',
     'Đây là quyền duy nhất cho phép duyệt trên màn này.'],
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
       'hiển thị phiếu do bạn lập. Các nút duyệt và không duyệt không hiển thị.')

b.h3('4.3. Người dùng có quyền "Quản lý giữ hàng"')
b.para('Bạn nhìn thấy mọi phiếu khác bản nháp. Với phiếu đang ở trạng thái Chờ duyệt, cột '
       'Hành động hiện thêm biểu tượng duyệt; mở phiếu ra thì cuối màn có nút '
       '"Tạo phiếu hủy hàng giữ" và nút "Không duyệt".')
b.para('Các bước duyệt: mở phiếu bằng cách bấm vào mã phiếu → xem lại các dòng hàng và số lượng '
       'đề nghị → bấm "Tạo phiếu hủy hàng giữ" → trên màn lập phiếu hủy, chỉnh lại số lượng nếu '
       'cần rồi bấm Lưu.')
b.para('Ngay khi phiếu hủy được lưu, hàng giữ bị trừ và phiếu yêu cầu chuyển sang trạng thái '
       'Đã duyệt. Vì vậy hãy kiểm tra kỹ số lượng trước khi lưu.', bold_prefix='Quan trọng: ')
b.para('Nếu không có quyền này, hai nút trên sẽ không hiển thị; trường hợp truy cập trực tiếp '
       'bằng đường dẫn, phần mềm báo lỗi không có quyền.')

b.h3('4.4. Người dùng có quyền xem theo cấp')
b.para('Ba quyền xem theo tổng công ty, theo công ty và theo phòng ban chỉ mở rộng phạm vi dữ '
       'liệu bạn nhìn thấy, KHÔNG cho phép duyệt phiếu. Phần mềm xét theo thứ tự ưu tiên: '
       'tổng công ty trước, rồi tới công ty, rồi tới phòng ban.')

# =============================================================== PHAN 1
b.h1('PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')

b.h2('1. Cách vào màn hình')
b.bullet('Đăng nhập phần mềm.')
b.bullet('Chọn phân hệ Tài chính.')
b.bullet('Ở thanh menu bên trái, mở nhóm Hàng hoá - Dịch vụ - Vận chuyển → Giữ hàng.')
b.bullet('Bấm mục Yêu cầu hủy hàng giữ.')

b.h2('2. Bố cục màn hình danh sách')
b.image('01-danh-sach.png', 'Màn hình Yêu cầu hủy hàng giữ lúc mới vào')
b.para('Màn hình chia làm hai khối:')
b.bullet('Khối Bộ lọc danh sách ở trên: ô tìm nhanh, nút Tìm kiếm, nút Làm mới, nút Cài đặt '
         'bộ lọc và nút Tìm kiếm nâng cao.')
b.bullet('Khối bảng danh sách ở dưới: thanh công cụ (Tạo mới, Xuất Excel, Cấu hình cột), bảng '
         'dữ liệu và thanh phân trang.')

# =============================================================== PHAN 2
b.h1('PHẦN 2: DANH SÁCH PHIẾU')

b.h2('1. Các cột của bảng')
b.table([
    ['Cột', 'Nội dung'],
    ['STT', 'Số thứ tự dòng, chạy liên tục theo trang.'],
    ['Mã phiếu', 'Mã phiếu do phần mềm sinh. Bấm vào mã để mở màn chi tiết.'],
    ['Người tạo', 'Người đã lập phiếu.'],
    ['Ngày tạo', 'Ngày giờ lập phiếu.'],
    ['Trạng thái', 'Đang tạo (xám) · Chờ duyệt (cam) · Đã duyệt (xanh lá).'],
    ['Người duyệt', 'Người đã lập phiếu hủy tương ứng. Để trống khi chưa duyệt.'],
    ['Ngày duyệt', 'Thời điểm duyệt.'],
    ['Người cập nhật / Ngày cập nhật', 'Lần chỉnh sửa gần nhất của phiếu.'],
    ['Khách hàng', 'Khách hàng đang được giữ hàng. Cột này ẩn sẵn, bật lên trong Cấu hình cột.'],
    ['Phòng ban', 'Phòng ban của người lập phiếu. Cột này ẩn sẵn.'],
    ['Ghi chú', 'Ghi chú do người lập nhập. Cột này ẩn sẵn.'],
    ['Lý do không duyệt', 'Lý do người duyệt trả phiếu về. Cột này ẩn sẵn.'],
    ['Hành động', 'Các nút thao tác của từng dòng.'],
])
b.para('Ba cột có mũi tên sắp xếp là Mã phiếu, Ngày tạo và Ngày cập nhật.')

b.h2('2. Tìm kiếm và lọc')
b.para('Ô tìm nhanh ở trên cùng tìm theo mã phiếu. Gõ xong bấm nút Tìm kiếm hoặc nhấn phím Enter.')
b.para('Bấm nút Tìm kiếm nâng cao để mở bảng lọc chi tiết.')
b.image('02-bo-loc-nang-cao.png', 'Bảng lọc nâng cao đang mở')
b.table([
    ['Tiêu chí lọc', 'Cách dùng'],
    ['Công ty', 'Chỉ hiện với người có quyền xem theo tổng công ty.'],
    ['Phòng ban', 'Chỉ hiện với người có quyền xem từ cấp công ty trở lên.'],
    ['Mã phiếu', 'Gõ một phần hoặc toàn bộ mã phiếu.'],
    ['Trạng thái', 'Chọn Đang tạo, Chờ duyệt hoặc Đã duyệt.'],
    ['Người tạo', 'Chọn nhân viên đã lập phiếu.'],
    ['Người duyệt', 'Chọn nhân viên đã duyệt phiếu.'],
    ['Tên hàng hóa', 'Tìm những phiếu có chứa hàng hóa khớp tên.'],
    ['Mã hàng hóa', 'Tìm những phiếu có chứa hàng hóa khớp mã.'],
    ['Ngày tạo từ / Ngày tạo đến', 'Khoảng ngày lập phiếu.'],
])
b.para('Các ô lọc nâng cao tự lọc lại ngay khi bạn chọn, không cần bấm nút. Bấm Làm mới để xóa '
       'toàn bộ điều kiện lọc.')
b.para('Phần mềm ghi nhớ điều kiện lọc trong 10 phút.', bold_prefix='Mẹo: ')

b.h2('3. Chọn ô lọc muốn hiển thị')
b.para('Bấm nút Cài đặt bộ lọc để tự chọn những ô lọc hay dùng và kéo sắp xếp lại thứ tự. '
       'Cấu hình được lưu riêng cho tài khoản của bạn.')
b.image('08-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc')

b.h2('4. Chọn cột hiển thị của bảng')
b.para('Bấm biểu tượng cột ở góc phải thanh công cụ để mở cửa sổ Tuỳ chỉnh cột.')
b.image('09-cau-hinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột')
b.para('Ba cột STT, Mã phiếu và Hành động có biểu tượng ổ khóa: luôn hiển thị. Bốn cột '
       'Khách hàng, Phòng ban, Ghi chú và Lý do không duyệt mặc định tắt.')

b.h2('5. Các nút trên thanh công cụ')
b.table([
    ['Nút', 'Tác dụng', 'Điều kiện hiển thị'],
    ['Tạo mới', 'Mở màn lập phiếu yêu cầu hủy hàng giữ mới.', 'Luôn hiển thị.'],
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
    ['Duyệt (biểu tượng dấu tích)', 'Mở màn lập Phiếu hủy hàng giữ cho phiếu yêu cầu này.',
     'Bạn có quyền Quản lý giữ hàng và phiếu đang ở trạng thái Chờ duyệt.'],
    ['In (biểu tượng máy in)', 'Mở bản in của phiếu đó.', 'Luôn hiện.'],
    ['Lịch sử (biểu tượng đồng hồ)', 'Mở cửa sổ lịch sử thay đổi của phiếu.', 'Luôn hiện.'],
])
b.para('Nút nào không dùng được thì phần mềm ẩn hẳn, không hiện nút mờ.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 3
b.h1('PHẦN 3: LẬP PHIẾU YÊU CẦU HỦY HÀNG GIỮ')

b.para('Ở màn danh sách, bấm nút Tạo mới.')
b.image('04-tao-moi.png', 'Màn lập phiếu yêu cầu hủy hàng giữ')

b.h2('1. Khối Thông tin chung')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Người lập – Ngày lập', 'Chỉ hiển thị', 'Không', 'Tên bạn và ngày giờ hiện tại',
     'Nằm ở góc phải tiêu đề khối.'],
    ['Khách hàng', 'Ô chọn từ danh sách', 'Có', 'Để trống',
     'Danh sách CHỈ gồm khách hàng đang có hàng giữ của chính bạn. Ngay dưới ô có dòng chú '
     'thích giải thích điều này. Nếu bạn không giữ hàng cho khách nào thì danh sách rỗng và '
     'chưa lập được phiếu.'],
    ['Ghi chú', 'Ô nhập chữ, tối đa 255 ký tự', 'Không', 'Để trống',
     'Ghi lý do hủy giữ để người duyệt nắm được.'],
])

b.h2('2. Khối Chi tiết hàng hóa')
b.para('Phải chọn Khách hàng trước thì nút Thêm hàng hóa mới bấm được. Khi nút còn khóa, rê '
       'chuột vào sẽ thấy chú thích nhắc chọn khách hàng trước.', bold_prefix='Quan trọng: ')
b.para('Bấm nút Thêm hàng hóa để mở popup chọn hàng.')
b.image('06-popup-chon-hang.png', 'Popup Hàng đang giữ cho khách hàng')
b.para('Popup liệt kê những hàng mà chính bạn đang giữ cho khách hàng đã chọn. Có hai ô tìm '
       'kiếm theo Tên hàng hóa và Mã hàng hóa. Tích vào các dòng cần hủy rồi bấm nút Chọn '
       '(có kèm số dòng đang tích). Hàng đã có trong phiếu sẽ không xuất hiện lại trong popup.')
b.table([
    ['Cột', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Cần hủy (ô tích)', 'Ô tích', 'Không', 'Đã tích sẵn',
     'Bỏ tích thì ô Yêu cầu hủy của dòng bị khóa và dòng bị làm mờ; dòng đó không được gửi đi.'],
    ['Tên hàng hóa / Model / Mã hàng hóa / Thương hiệu', 'Chỉ hiển thị', '—',
     'Theo hàng hóa đã chọn', 'Không sửa được.'],
    ['Có thể hủy', 'Chỉ hiển thị', '—', 'Theo hàng giữ hiện có',
     'Số lượng còn có thể hủy, đã trừ phần đang nằm trong đề nghị xuất kho chưa xong.'],
    ['Yêu cầu hủy', 'Ô nhập số', 'Có', 'Để trống',
     'Phải lớn hơn 0 và không vượt quá số ở cột Có thể hủy.'],
    ['ĐVT', 'Chỉ hiển thị', '—', 'Đơn vị cơ bản của hàng hóa', '—'],
    ['Nút xóa dòng', 'Nút biểu tượng thùng rác', '—', '—', 'Bỏ hẳn dòng hàng khỏi phiếu.'],
])

b.h2('3. Giá trị phần mềm điền sẵn khi lập phiếu mới')
b.bullet('Người lập: chính bạn. Ngày lập: ngày giờ hiện tại.')
b.bullet('Phòng ban yêu cầu: phòng ban của bạn (chỉ hiện sau khi phiếu đã lưu).')
b.bullet('Trạng thái: Đang tạo khi bấm Lưu nháp, Chờ duyệt khi bấm Lưu và gửi duyệt.')
b.bullet('Mã phiếu: phần mềm tự sinh khi lưu.')
b.bullet('Ô tích Cần hủy: tự tích sẵn cho những dòng bạn vừa chọn từ popup.')

b.h2('4. Các nút lưu ở cuối màn')
b.table([
    ['Nút', 'Phần mềm làm gì', 'Ràng buộc'],
    ['Lưu nháp', 'Lưu phiếu ở trạng thái Đang tạo.',
     'Chỉ bắt buộc chọn Khách hàng. KHÔNG bắt buộc phải có dòng hàng — bạn có thể chọn khách '
     'rồi để đó, thêm hàng sau.'],
    ['Lưu và gửi duyệt', 'Lưu phiếu và chuyển sang trạng thái Chờ duyệt, báo cho người có quyền '
                         'Quản lý giữ hàng.',
     'Bắt buộc có ít nhất một dòng được tích với số lượng lớn hơn 0.'],
    ['Lưu và tiếp tục', 'Lưu nháp phiếu này rồi ở lại màn để lập tiếp phiếu mới.',
     'Chỉ có ở màn Tạo mới.'],
    ['Quay lại', 'Thoát khỏi màn lập phiếu.',
     'Nếu đã nhập gì mà chưa lưu, phần mềm hỏi xác nhận trước khi rời trang.'],
])

b.h2('5. Các lỗi thường gặp khi lưu')
b.table([
    ['Tình huống', 'Phần mềm báo gì', 'Cách xử lý'],
    ['Chưa chọn Khách hàng', 'Bắt buộc phải chọn', 'Chọn khách hàng ở ô đầu tiên.'],
    ['Gửi duyệt mà chưa có dòng hàng nào',
     'Phải chọn ít nhất 1 hàng hoá cần hủy với số lượng lớn hơn 0',
     'Bấm Thêm hàng hóa để chọn hàng và nhập số lượng.'],
    ['Số lượng bằng 0', 'Phải lớn hơn 0', 'Nhập số lớn hơn 0.'],
    ['Số lượng vượt số Có thể hủy', 'Báo lỗi đỏ ngay tại dòng',
     'Nhập lại số nhỏ hơn hoặc bằng cột Có thể hủy.'],
    ['Hàng đã bị hủy giữ hết trong lúc bạn đang lập phiếu',
     'Thông báo nêu rõ tên hàng không đủ số lượng đang giữ',
     'Xóa dòng đó hoặc giảm số lượng rồi lưu lại.'],
    ['Ghi chú quá 255 ký tự', 'Không được vượt quá 255 ký tự', 'Rút ngắn nội dung ghi chú.'],
])

# =============================================================== PHAN 4
b.h1('PHẦN 4: SỬA PHIẾU')

b.para('Bạn chỉ sửa được phiếu do chính mình lập và đang ở trạng thái Đang tạo. Phiếu bị người '
       'duyệt trả về cũng quay lại trạng thái này nên sửa lại được.')
b.image('05-sua-phieu.png', 'Màn sửa phiếu — có khối Lý do không duyệt của lần trả về trước')
b.para('Cách vào: bấm biểu tượng bút chì ở cột Hành động, hoặc mở phiếu ra rồi bấm nút Sửa ở '
       'cuối màn chi tiết.')
b.para('Ô Khách hàng bị KHÓA ở màn sửa. Muốn đổi khách hàng thì phải lập phiếu mới, vì đổi '
       'khách thì toàn bộ dòng hàng đã chọn không còn ý nghĩa.', bold_prefix='Lưu ý: ')
b.para('Nếu phiếu từng bị trả về, màn sửa hiển thị thêm khối "Lý do không duyệt" để bạn biết '
       'cần chỉnh gì trước khi gửi lại.')
b.para('Màn sửa có các nút Lưu nháp, Lưu và gửi duyệt và Quay lại; không có nút Lưu và tiếp tục.')

# =============================================================== PHAN 5
b.h1('PHẦN 5: XEM CHI TIẾT PHIẾU')

b.para('Bấm vào mã phiếu ở cột thứ hai của bảng danh sách để mở màn chi tiết.')
b.image('03-chi-tiet.png', 'Màn chi tiết phiếu đã duyệt')
b.para('Màn chi tiết gồm:')
b.bullet('Thông tin chung: Khách hàng, Ghi chú, Mã phiếu, Trạng thái, Người duyệt, Ngày duyệt, '
         'Phòng ban yêu cầu và ô Phiếu hủy hàng giữ.')
b.bullet('Chi tiết: bảng hàng hóa với hai cột số lượng Yêu cầu hủy và Duyệt hủy.')
b.bullet('Lý do không duyệt (chỉ hiện khi phiếu từng bị trả về).')
b.bullet('Lịch sử thay đổi, mặc định thu gọn.')
b.para('Ô "Phiếu hủy hàng giữ" là một liên kết. Bấm vào đó để mở phiếu hủy tương ứng và xem '
       'người duyệt đã chấp thuận hủy bao nhiêu.', bold_prefix='Mẹo: ')
b.para('Hai cột số lượng KHÁC nhau: "Yêu cầu hủy" là số bạn đề nghị, "Duyệt hủy" là số người '
       'duyệt thực sự chấp thuận. Cột "Có thể giữ" là tồn kho tại thời điểm mở phiếu, không '
       'liên quan tới hai cột trên.', bold_prefix='Quan trọng: ')

# =============================================================== PHAN 6
b.h1('PHẦN 6: DUYỆT VÀ KHÔNG DUYỆT PHIẾU')

b.para('Phần này dành cho người có quyền Quản lý giữ hàng.')

b.h2('1. Duyệt phiếu bằng cách lập Phiếu hủy hàng giữ')
b.para('Màn này KHÔNG có nút "Duyệt" theo nghĩa thông thường. Duyệt một yêu cầu hủy chính là '
       'lập Phiếu hủy hàng giữ tương ứng.', bold_prefix='Quan trọng: ')
b.bullet('Mở phiếu yêu cầu bằng cách bấm vào mã phiếu, hoặc bấm biểu tượng dấu tích ở cột '
         'Hành động.')
b.bullet('Xem lại danh sách hàng và số lượng người lập đề nghị.')
b.bullet('Bấm nút "Tạo phiếu hủy hàng giữ" ở cuối màn.')
b.bullet('Phần mềm mở màn lập Phiếu hủy hàng giữ, nạp sẵn các dòng hàng từ phiếu yêu cầu.')
b.bullet('Bạn được giảm bớt số lượng ở cột Duyệt hủy nếu không đồng ý hủy hết.')
b.bullet('Bấm Lưu để hoàn tất.')
b.para('Ngay khi phiếu hủy được lưu: hàng giữ bị trừ, phiếu yêu cầu chuyển sang trạng thái '
       'Đã duyệt và người lập nhận được thông báo. Phần mềm trừ dần từ lô có hạn giữ sớm nhất.')
b.para('Nếu tổng hàng giữ còn lại không đủ so với số duyệt hủy, phần mềm báo lỗi và hủy bỏ '
       'toàn bộ thao tác — không trừ một phần.', bold_prefix='Lưu ý: ')

b.h2('2. Không duyệt phiếu')
b.image('12-popup-khong-duyet.png', 'Cửa sổ Không duyệt yêu cầu hủy hàng giữ')
b.bullet('Mở phiếu yêu cầu và bấm nút "Không duyệt" ở cuối màn.')
b.bullet('Phần mềm mở cửa sổ có hiển thị mã phiếu.')
b.bullet('Nhập lý do trả phiếu về (bắt buộc, tối đa 255 ký tự) rồi bấm nút xác nhận.')
b.para('Phiếu quay về trạng thái Đang tạo để người lập sửa và gửi lại. Hàng giữ KHÔNG bị thay '
       'đổi. Phần mềm không có trạng thái "Không duyệt" riêng, nên lý do bạn ghi là thông tin '
       'duy nhất giúp người lập hiểu vì sao bị trả lại.', bold_prefix='Quan trọng: ')
b.para('Bỏ trống lý do thì phần mềm báo "Bắt buộc phải nhập lý do không duyệt" và cửa sổ '
       'không đóng.')

b.h2('3. Khi hai người cùng xử lý một phiếu')
b.para('Nếu phiếu đã được người khác duyệt hoặc trả về trước đó, phần mềm báo phiếu không còn ở '
       'trạng thái chờ duyệt hoặc bạn không đủ quyền duyệt. Hãy tải lại danh sách để xem trạng '
       'thái mới nhất.')

# =============================================================== PHAN 7
b.h1('PHẦN 7: XÓA PHIẾU')

b.para('Chỉ người lập phiếu mới xóa được, và chỉ khi phiếu đang ở trạng thái Đang tạo. Phiếu đã '
       'gửi duyệt hoặc đã duyệt không xóa được.')
b.image('13-xac-nhan-xoa.png', 'Hộp thoại Xác nhận xóa phiếu')
b.bullet('Bấm biểu tượng thùng rác ở cột Hành động, hoặc nút Xóa ở cuối màn chi tiết.')
b.bullet('Phần mềm hỏi xác nhận, có ghi rõ mã phiếu để tránh xóa nhầm.')
b.bullet('Bấm Xóa để xác nhận, hoặc Hủy để thoát.')
b.para('Phiếu đã xóa không khôi phục lại được.')

# =============================================================== PHAN 8
b.h1('PHẦN 8: IN VÀ XUẤT EXCEL')

b.h2('1. In một phiếu')
b.para('Bấm biểu tượng máy in ở cột Hành động, hoặc nút In ở cuối màn chi tiết. Phần mềm mở một '
       'tab mới hiển thị bản xem trước khổ A4 dọc. Bấm nút In ở góc trên bên phải tờ giấy để '
       'gửi lệnh in.')
b.image('07-in-phieu.png', 'Bản in phiếu yêu cầu hủy hàng giữ')
b.para('Bản in gồm: phần đầu chứng từ theo công ty ghi trên phiếu, thông tin khách hàng và '
       'người yêu cầu, bảng hàng hóa kèm dòng Tổng cộng và khối ký tên.')

b.h2('2. In danh sách')
b.image('11-in-danh-sach.png', 'Bản in danh sách phiếu yêu cầu hủy hàng giữ')
b.para('Bản in danh sách dùng khổ A4 ngang và in đúng những phiếu khớp điều kiện lọc bạn đang '
       'áp, không chỉ trang đang xem.')
b.para('Thanh công cụ của màn danh sách hiện CHƯA có nút mở bản in danh sách; muốn xem phải gõ '
       'thẳng địa chỉ /finance/prepick-cancel-requests/print-list trên thanh địa chỉ trình '
       'duyệt.', bold_prefix='Lưu ý: ')

b.h2('3. Xuất Excel')
b.para('Bấm nút Xuất Excel trên thanh công cụ.')
b.image('10-chon-truong-xuat-excel.png', 'Cửa sổ Chọn trường xuất Excel')
b.bullet('Mặc định chọn sẵn cả 12 trường: Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người '
         'duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, Khách hàng, Phòng ban, Ghi chú, '
         'Lý do không duyệt.')
b.bullet('Bỏ chọn trường không cần bằng cách bấm dấu nhân trên thẻ tên trường.')
b.bullet('Thứ tự cột trong tệp chạy theo đúng thứ tự bạn chọn.')
b.bullet('Bấm Xuất file để tải tệp về máy.')
b.para('Tệp Excel chứa toàn bộ phiếu khớp điều kiện lọc trong phạm vi bạn được xem, không giới '
       'hạn ở trang đang mở.')

# =============================================================== PHAN 9
b.h1('PHẦN 9: XEM LỊCH SỬ THAY ĐỔI')

b.para('Có hai cách xem lịch sử của một phiếu:')
b.bullet('Bấm biểu tượng đồng hồ ở cột Hành động của màn danh sách.')
b.bullet('Mở phiếu ra, kéo xuống khối Lịch sử thay đổi rồi bấm nút Xem lịch sử.')
b.para('Danh sách hiển thị các mốc thao tác theo thứ tự mới nhất trước, mỗi mốc ghi rõ nhóm '
       'thao tác (tạo mới, chỉnh sửa, gửi duyệt, duyệt, không duyệt), người thực hiện, thời '
       'điểm và những giá trị đã thay đổi.')
b.para('Các phiếu được lập từ trước khi phần mềm bật tính năng ghi lịch sử sẽ hiện dòng '
       '"Chưa có lịch sử thao tác nào." — đây không phải lỗi.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 10
b.h1('PHẦN 10: NHỮNG ĐIỀU CẦN NHỚ')

b.bullet('Danh sách Khách hàng chỉ gồm khách đang có hàng giữ của chính bạn. Danh sách rỗng '
         'nghĩa là bạn chưa giữ hàng cho ai, không phải lỗi phần mềm.')
b.bullet('Phải chọn Khách hàng trước thì mới bấm được nút Thêm hàng hóa.')
b.bullet('Lưu nháp không đòi hỏi phải có dòng hàng; Lưu và gửi duyệt thì bắt buộc.')
b.bullet('Duyệt phiếu chính là lập Phiếu hủy hàng giữ. Hàng chỉ bị trừ khi phiếu hủy được lưu.')
b.bullet('Người duyệt được cắt bớt số lượng, nên "Duyệt hủy" có thể ít hơn "Yêu cầu hủy".')
b.bullet('Phiếu bị trả về quay lại trạng thái Đang tạo, không phải trạng thái riêng — hãy đọc '
         'khối Lý do không duyệt để biết vì sao.')
b.bullet('Ô Khách hàng khóa ở màn sửa; muốn đổi khách thì lập phiếu mới.')

print(b.finish())
