# -*- coding: utf-8 -*-
"""Sinh HDSD man "Yeu cau xuat giu" (PYCXG) tu khung HDSD_MAU.docx.

Anh chup that: ./product_prepick_shots (Playwright MCP, 1440x900, ngay 18/09/2026).
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

SHOTS = os.path.join(BASE, 'product_prepick_shots')
OUT = os.path.join(BASE, 'HDSD_Yeu cau xuat giu.docx')

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title='(Màn hình: Yêu cầu xuất giữ)',
                doc_title='HDSD - Yêu cầu xuất giữ')

# =============================================================== TONG QUAN
b.h1('TỔNG QUAN')

b.h2('1. Thuật ngữ sử dụng trong tài liệu')
b.table([
    ['Thuật ngữ', 'Ý nghĩa'],
    ['Hàng giữ', 'Số lượng hàng hóa trong kho được giữ lại cho một khách hàng cụ thể, do một '
                 'nhân viên kinh doanh đứng tên giữ, tới một hạn nhất định.'],
    ['Yêu cầu xuất giữ', 'Phiếu bạn lập để xin giữ hàng, mã bắt đầu bằng PYCXG. Đây là phiếu '
                         'ĐỀ NGHỊ — lập xong chưa có nghĩa là hàng đã được giữ.'],
    ['Phiếu xuất giữ', 'Phiếu do Kế toán lập ở bước cuối, mã bắt đầu bằng PXG. Khi phiếu này '
                       'được duyệt thì hàng mới thực sự được giữ.'],
    ['Loại yêu cầu', 'Sáu loại: Xuất giữ thường, Xuất giữ khuyến mại, Xuất giữ HĐDV, Xuất giữ '
                     'HĐDA, Xuất giữ HĐ hãng và Xuất giữ khác.'],
    ['Xuất giữ khác', 'Loại không gắn hợp đồng. Bạn tự chọn khách hàng và tự thêm từng dòng '
                      'hàng hóa.'],
    ['Giữ đến ngày', 'Hạn bạn xin giữ hàng tới. Bắt buộc nhập, phải là ngày trong tương lai.'],
    ['Cần xuất', 'Ô tích đánh dấu dòng hàng bạn thực sự muốn giữ. Dòng không tích sẽ được lưu '
                 'với số lượng 0.'],
    ['SL Có thể giữ', 'Số hàng còn trong kho có thể giữ được. Đây là số tham khảo khi bạn nhập '
                      'số lượng.'],
    ['SL Đề nghị', 'Số lượng bạn xin giữ cho dòng hàng đó.'],
    ['Đang tạo', 'Phiếu còn nháp, hoặc phiếu vừa bị một cấp trả về. Đây cũng là trạng thái duy '
                 'nhất cho phép bạn sửa và xóa phiếu.'],
    ['Đang xuất giữ', 'Kế toán đã lập Phiếu xuất giữ nhưng còn để nháp, chưa duyệt.'],
    ['TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán — ba cấp xử lý của phiếu.'],
])

b.h2('2. Cập nhật tài liệu')
b.table([
    ['Phiên bản', 'Ngày', 'Nội dung'],
    ['1.0', '18/09/2026', 'Ban hành lần đầu cho màn hình Yêu cầu xuất giữ trên phân hệ '
                          'Tài chính.'],
])

b.h2('3. Giới thiệu chung')
b.para('Màn hình Yêu cầu xuất giữ dùng khi bạn cần giữ lại một số hàng trong kho cho khách hàng '
       'của mình, để tới ngày giao thì chắc chắn còn hàng.')
b.para('Phiếu đi qua ba cấp: Trưởng phòng duyệt, rồi Ban giám đốc duyệt (chỉ với phiếu thuộc '
       'diện phải trình), rồi Kế toán. Ở bước Kế toán, người ta KHÔNG bấm nút duyệt mà lập một '
       'Phiếu xuất giữ. Chính phiếu đó khi được duyệt thì hàng mới thực sự được giữ và yêu cầu '
       'của bạn mới chuyển sang Đã duyệt.')
b.para('Lập xong yêu cầu KHÔNG có nghĩa là hàng đã được giữ. Chỉ khi phiếu chuyển sang trạng '
       'thái Đã duyệt thì hàng mới nằm trong kho hàng giữ của bạn.',
       bold_prefix='Quan trọng: ')
b.para('Đường dẫn truy cập: Phân hệ Tài chính → nhóm Giữ hàng → Yêu cầu xuất giữ. Có thể gõ '
       'thẳng địa chỉ /finance/product-prepick-requests trên thanh địa chỉ trình duyệt.')
b.para('Mã phiếu do phần mềm tự sinh theo dạng PYCXG kèm 5 chữ số, ví dụ PYCXG-02219.')

b.h2('4. Quyền sử dụng và phạm vi dữ liệu')
b.para('Màn hình này không đòi hỏi quyền riêng để lập phiếu: mọi người dùng đã đăng nhập đều '
       'lập được yêu cầu xuất giữ. Các quyền dưới đây quyết định bạn XỬ LÝ được phiếu ở cấp nào '
       'và NHÌN THẤY phiếu của những ai.', bold_prefix='Lưu ý: ')

b.h3('4.1. Bảng quyền của màn hình')
b.table([
    ['Tên quyền', 'Cho phép làm gì', 'Nút / phần tương ứng trên màn hình', 'Ghi chú'],
    ['Trưởng phòng duyệt hàng giữ',
     'Duyệt hoặc từ chối phiếu đang ở bước Chờ TP duyệt.',
     'Nút TP duyệt và nút Từ chối ở màn chi tiết; biểu tượng duyệt ở cột Hành động.',
     'Ngoài quyền còn phải quản lý phòng ban ghi trên phiếu và cùng công ty với phiếu.'],
    ['Ban giám đốc duyệt hàng giữ',
     'Duyệt hoặc từ chối phiếu đang ở bước Chờ BGĐ duyệt.',
     'Nút BGĐ duyệt và nút Từ chối.',
     'Bước này bạn nhập LẠI Giữ đến ngày. Phải cùng công ty với phiếu.'],
    ['Kế toán duyệt hàng giữ',
     'Lập Phiếu xuất giữ từ yêu cầu, hoặc từ chối phiếu.',
     'Nút Lập phiếu xuất giữ và nút Từ chối.',
     'Ở màn này Kế toán KHÔNG có nút duyệt riêng. Phải cùng công ty với phiếu.'],
    ['Xem phiếu hàng giữ theo tổng công ty', 'Xem phiếu của mọi công ty.',
     'Toàn bộ danh sách; ô lọc Công ty và Phòng ban.', 'Là phạm vi rộng nhất.'],
    ['Xem phiếu hàng giữ theo công ty', 'Xem phiếu thuộc công ty của mình.',
     'Danh sách; ô lọc Phòng ban.', '—'],
    ['Xem phiếu hàng giữ theo phòng ban',
     'Xem phiếu thuộc các phòng ban mình được phân công quản lý và phòng ban của chính mình.',
     'Danh sách.', '—'],
])

b.h3('4.2. Người dùng không có quyền nào ở trên')
b.para('Bạn vẫn vào được màn hình và lập được yêu cầu xuất giữ. Danh sách chỉ hiển thị phiếu do '
       'bạn lập. Các nút duyệt, từ chối và lập phiếu xuất giữ không hiển thị.')

b.h3('4.3. Người dùng có quyền "Trưởng phòng duyệt hàng giữ"')
b.para('Bạn duyệt các phiếu ở trạng thái Chờ TP duyệt trong công ty mình, với điều kiện bạn quản '
       'lý phòng ban ghi trên phiếu — tức phòng ban của người lập lúc lập phiếu.')
b.para('Các bước duyệt: mở phiếu bằng cách bấm vào mã phiếu → xem lại danh sách hàng và số lượng '
       'đề nghị → bấm nút TP duyệt → xác nhận.')
b.para('Sau khi bạn duyệt, phần mềm tự quyết định phiếu đi tiếp đâu: nếu phiếu thuộc diện phải '
       'trình Ban giám đốc thì báo "Yêu cầu đã được chuyển đến Ban giám đốc.", ngược lại báo '
       '"Yêu cầu đã được chuyển đến Kế toán.".')

b.h3('4.4. Người dùng có quyền "Ban giám đốc duyệt hàng giữ"')
b.para('Bạn duyệt các phiếu đang ở trạng thái Chờ BGĐ duyệt trong công ty mình. Không phải phiếu '
       'nào cũng đi qua bước này — chỉ những phiếu có tỉ lệ thu tiền của hợp đồng chưa đạt ngưỡng '
       'quy định, hoặc phiếu không gắn hợp đồng mà tổng giá trị vượt hạn mức, mới phải trình '
       'Ban giám đốc.')
b.para('Ở bước này bạn phải NHẬP LẠI ô Giữ đến ngày. Hạn giữ bạn chốt sẽ là hạn đi tiếp xuống '
       'Kế toán.', bold_prefix='Chú ý: ')

b.h3('4.5. Người dùng có quyền "Kế toán duyệt hàng giữ"')
b.para('Bạn xử lý bước cuối cùng. Màn này KHÔNG có nút duyệt dành cho bạn — thay vào đó là nút '
       '"Lập phiếu xuất giữ". Bấm nút đó, phần mềm đưa bạn sang màn lập Phiếu xuất giữ.')
b.para('Nếu bạn lưu nháp phiếu xuất giữ thì yêu cầu chuyển sang trạng thái Đang xuất giữ. Nếu '
       'bạn bấm Duyệt giữ hàng thì hàng được ghi vào kho hàng giữ và yêu cầu chuyển sang '
       'Đã duyệt.')
b.para('Bạn vẫn từ chối được phiếu ở bước này nếu thấy không hợp lệ.')

# =============================================================== PHAN 1
b.h1('PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')

b.h2('1. Cách vào màn hình')
b.bullet('Đăng nhập phần mềm.')
b.bullet('Chọn phân hệ Tài chính.')
b.bullet('Ở thanh menu bên trái, mở nhóm Hàng hoá - Dịch vụ - Vận chuyển → Giữ hàng.')
b.bullet('Bấm mục Yêu cầu xuất giữ.')

b.h2('2. Bố cục màn hình danh sách')
b.image('01-danh-sach.png', 'Màn hình Yêu cầu xuất giữ lúc mới vào')
b.para('Màn hình chia làm hai khối:')
b.bullet('Khối Bộ lọc danh sách ở trên: ô tìm nhanh, nút Tìm kiếm, nút Làm mới, nút Cài đặt '
         'bộ lọc và nút Tìm kiếm nâng cao.')
b.bullet('Khối bảng danh sách ở dưới: thanh công cụ (Tạo mới, In, Xuất Excel, Cấu hình cột), '
         'bảng dữ liệu và thanh phân trang.')

b.h2('3. Ý nghĩa các trạng thái')
b.table([
    ['Trạng thái', 'Màu', 'Nghĩa là gì', 'Bạn làm được gì'],
    ['Đang tạo', 'Xám', 'Phiếu còn nháp, hoặc vừa bị một cấp trả về.',
     'Sửa, xóa, gửi duyệt. Chỉ mình bạn nhìn thấy phiếu này.'],
    ['Chờ TP duyệt', 'Cam', 'Đang chờ Trưởng phòng xử lý.', 'Chờ. Không sửa được nữa.'],
    ['Chờ BGĐ duyệt', 'Cam', 'Đang chờ Ban giám đốc xử lý.', 'Chờ.'],
    ['Chờ KT duyệt', 'Cam', 'Đang chờ Kế toán lập Phiếu xuất giữ.', 'Chờ.'],
    ['Đang xuất giữ', 'Cam', 'Kế toán đã lập Phiếu xuất giữ nhưng còn để nháp.',
     'Chờ Kế toán duyệt phiếu đó.'],
    ['Đã duyệt', 'Xanh lá', 'Hàng ĐÃ được giữ cho khách hàng của bạn.',
     'Xem, in. Hàng đã nằm trong danh sách hàng giữ của bạn.'],
])
b.para('Phiếu bị trả về quay đúng về trạng thái "Đang tạo", không có trạng thái "Từ chối" riêng. '
       'Muốn biết phiếu có bị trả về hay không, nhìn cột "Lý do từ chối" (bật cột này ở Cấu hình '
       'cột), hoặc mở phiếu ra xem ô "Lý do từ chối gần nhất".', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 2
b.h1('PHẦN 2: DANH SÁCH PHIẾU')

b.h2('1. Các cột của bảng')
b.table([
    ['Cột', 'Nội dung'],
    ['STT', 'Số thứ tự dòng, chạy liên tục theo trang.'],
    ['Mã phiếu', 'Mã phiếu do phần mềm sinh. Bấm vào mã để mở màn chi tiết.'],
    ['Loại yêu cầu', 'Một trong sáu loại xuất giữ.'],
    ['Người tạo', 'Người đã lập phiếu.'],
    ['Ngày tạo', 'Ngày giờ lập phiếu.'],
    ['Hợp đồng', 'Số hợp đồng gắn với phiếu. Loại Xuất giữ khác để trống.'],
    ['Trạng thái', 'Xem bảng ý nghĩa trạng thái ở Phần 1.'],
    ['Người duyệt', 'Người duyệt ở bước CUỐI, tức Kế toán. Để trống cho tới khi phiếu Đã duyệt.'],
    ['Ngày duyệt', 'Thời điểm phiếu được duyệt xong.'],
    ['Khách hàng', 'Khách hàng được giữ hàng. Cột này ẩn sẵn.'],
    ['Giữ đến ngày', 'Hạn giữ hàng. Cột này ẩn sẵn.'],
    ['Người cập nhật / Ngày cập nhật', 'Lần chỉnh sửa gần nhất. Hai cột này ẩn sẵn.'],
    ['Phòng ban', 'Phòng ban của người lập phiếu. Cột này ẩn sẵn.'],
    ['Ghi chú', 'Ghi chú do người lập nhập. Cột này ẩn sẵn.'],
    ['Lý do từ chối', 'Lý do cấp xử lý trả phiếu về. Cột này ẩn sẵn.'],
    ['Hành động', 'Các nút thao tác của từng dòng.'],
])
b.para('Bốn cột có mũi tên sắp xếp là Mã phiếu, Ngày tạo, Ngày duyệt và Giữ đến ngày.')

b.h2('2. Tìm kiếm và lọc')
b.para('Ô tìm nhanh ở trên cùng tìm theo mã phiếu. Gõ xong bấm nút Tìm kiếm hoặc nhấn Enter.')
b.image('02-bo-loc-nang-cao.png', 'Bảng lọc nâng cao đang mở')
b.table([
    ['Tiêu chí lọc', 'Cách dùng'],
    ['Công ty', 'Chỉ hiện với người có quyền xem theo tổng công ty.'],
    ['Phòng ban', 'Chỉ hiện với người có quyền xem từ cấp công ty trở lên.'],
    ['Mã phiếu', 'Gõ một phần hoặc toàn bộ mã phiếu.'],
    ['Loại yêu cầu', 'Chọn một trong sáu loại.'],
    ['Trạng thái', 'Chọn một trong sáu trạng thái.'],
    ['Người tạo', 'Chọn nhân viên đã lập phiếu.'],
    ['Người duyệt', 'Chọn nhân viên đã duyệt phiếu ở bước cuối.'],
    ['Khách hàng', 'Chọn khách hàng được giữ hàng.'],
    ['Tên, mã hàng', 'Một ô chung cho cả tên và mã hàng hóa.'],
    ['Số hợp đồng', 'Tìm những phiếu gắn hợp đồng khớp số bạn nhập.'],
    ['Ngày tạo từ / Ngày tạo đến', 'Khoảng ngày LẬP phiếu — không phải ngày duyệt, cũng không '
                                   'phải hạn giữ.'],
])
b.para('Các ô lọc nâng cao tự lọc lại ngay khi bạn chọn. Bấm Làm mới để xóa toàn bộ điều kiện.')
b.para('Ô "Tên, mã hàng" chỉ tìm trong những dòng hàng CÓ TÍCH "Cần xuất". Dòng không tích là '
       'hàng của hợp đồng mà người lập không xin giữ nên không tính.', bold_prefix='Lưu ý: ')

b.h2('3. Chọn ô lọc muốn hiển thị')
b.para('Màn này có 11 ô lọc nên nút Cài đặt bộ lọc rất hữu ích: bạn tắt bớt những ô không dùng '
       'và kéo ô hay dùng lên đầu.')
b.image('03-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc')

b.h2('4. Chọn cột hiển thị của bảng')
b.image('04-cau-hinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột')
b.para('Ba cột STT, Mã phiếu và Hành động có biểu tượng ổ khóa: luôn hiển thị. Bảy cột Khách '
       'hàng, Giữ đến ngày, Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú và Lý do từ chối '
       'mặc định tắt.')

b.h2('5. Các nút trên thanh công cụ')
b.table([
    ['Nút', 'Tác dụng', 'Điều kiện hiển thị'],
    ['Tạo mới', 'Mở màn lập yêu cầu xuất giữ mới.', 'Luôn hiển thị.'],
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
     'Phiếu đang chờ chính bạn duyệt ở cấp Trưởng phòng hoặc Ban giám đốc.'],
    ['Lập phiếu xuất giữ', 'Mở màn lập Phiếu xuất giữ từ yêu cầu này.',
     'Bạn là Kế toán và phiếu đang ở Chờ KT duyệt.'],
    ['In (biểu tượng máy in)', 'Mở bản in của phiếu đó.', 'Luôn hiện.'],
    ['Lịch sử (biểu tượng đồng hồ)', 'Mở cửa sổ lịch sử thay đổi của phiếu.', 'Luôn hiện.'],
])
b.para('Cột Hành động KHÔNG có nút Từ chối. Muốn từ chối phiếu, bạn mở phiếu ra rồi bấm nút '
       'Từ chối ở cuối màn chi tiết.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 3
b.h1('PHẦN 3: LẬP YÊU CẦU XUẤT GIỮ')

b.para('Ở màn danh sách, bấm nút Tạo mới.')
b.image('06-tao-moi.png', 'Màn lập yêu cầu xuất giữ lúc mới mở')

b.h2('1. Bước đầu tiên: chọn Loại yêu cầu')
b.para('Đây là lựa chọn quan trọng nhất vì nó quyết định toàn bộ phần còn lại của phiếu. Chọn '
       'xong rồi lưu phiếu thì KHÔNG đổi lại được nữa.')
b.table([
    ['Loại yêu cầu', 'Lấy hàng từ đâu', 'Bạn phải làm gì'],
    ['Xuất giữ thường', 'Hợp đồng bán hàng', 'Chọn hợp đồng, rồi tích dòng cần giữ.'],
    ['Xuất giữ khuyến mại', 'Hàng khuyến mại của hợp đồng bán hàng',
     'Chọn hợp đồng, rồi tích dòng cần giữ.'],
    ['Xuất giữ HĐDV', 'Hợp đồng dịch vụ', 'Chọn hợp đồng, rồi tích dòng cần giữ.'],
    ['Xuất giữ HĐDA', 'Hợp đồng dự án', 'Chọn hợp đồng, rồi tích dòng cần giữ.'],
    ['Xuất giữ HĐ hãng', 'Hợp đồng hãng', 'Chọn hợp đồng, rồi tích dòng cần giữ.'],
    ['Xuất giữ khác', 'Không gắn hợp đồng',
     'Chọn Khách hàng, tự thêm từng dòng hàng, chọn đơn vị tính, nhập Ghi chú và đính kèm ít '
     'nhất một tệp.'],
])

b.h2('2. Với năm loại có hợp đồng')
b.para('Bấm nút Chọn cạnh ô Hợp đồng để mở cửa sổ tìm hợp đồng. Tìm được theo số hợp đồng hoặc '
       'tên khách hàng.')
b.image('16-popup-chon-hop-dong.png', 'Cửa sổ Chọn hợp đồng')
b.para('Chọn xong, phần mềm tự điền Mã khách hàng, Khách hàng, Số điện thoại, Địa chỉ, Địa chỉ '
       'giao hàng, và nạp toàn bộ hàng hóa của hợp đồng vào bảng Chi tiết.')
b.image('08-sua-loai-hop-dong.png', 'Phiếu loại có hợp đồng: bảng hàng đã nạp sẵn từ hợp đồng')
b.para('Bạn KHÔNG thêm hay xóa dòng hàng được. Việc của bạn chỉ là tích ô "Cần xuất" ở những '
       'dòng muốn giữ và nhập số lượng vào cột "Đề nghị". Dòng không tích sẽ bị làm mờ và lưu '
       'với số lượng 0.')

b.h2('3. Với loại Xuất giữ khác')
b.image('07-sua-loai-khac.png', 'Phiếu loại Xuất giữ khác: tự thêm từng dòng hàng')
b.bullet('Chọn Khách hàng ở ô tìm kiếm (gõ tối thiểu 2 ký tự).')
b.bullet('Bấm nút Thêm hàng hóa để mở cửa sổ tìm hàng còn tồn kho, tích các dòng cần giữ.')
b.bullet('Với mỗi dòng: chọn ĐVT và nhập số lượng ở cột Đề nghị.')
b.bullet('Nhập Ghi chú (bắt buộc với loại này).')
b.bullet('Đính kèm ít nhất một tệp (bắt buộc với loại này) — thường là phiếu báo giữ đã ký.')
b.para('Đổi ĐVT thì số ở cột "Có thể giữ" được tính lại theo đơn vị mới.', bold_prefix='Mẹo: ')

b.h2('4. Khối Thông tin chung')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Người lập – Ngày lập', 'Chỉ hiển thị', 'Không', 'Tên bạn và ngày hôm nay',
     'Nằm ở góc phải tiêu đề khối.'],
    ['Loại yêu cầu', 'Ô chọn từ danh sách', 'Có', 'Để trống',
     'Khóa lại sau khi phiếu đã lưu. Bấm biểu tượng chữ i bên cạnh để xem giải thích.'],
    ['Hợp đồng', 'Chọn từ cửa sổ tìm kiếm', 'Có (năm loại có hợp đồng)', 'Để trống',
     'Bấm nút Chọn bên cạnh ô.'],
    ['Mã khách hàng', 'Chỉ hiển thị', 'Không', 'Tự điền theo hợp đồng', 'Không sửa tại đây.'],
    ['Khách hàng', 'Ô chọn từ danh sách hoặc chỉ hiển thị', 'Có (loại Xuất giữ khác)',
     'Để trống hoặc tự điền theo hợp đồng',
     'Chỉ loại Xuất giữ khác mới chọn được khách hàng.'],
    ['Giữ đến ngày', 'Ô chọn ngày', 'Có', 'Để trống',
     'Lịch đã chặn sẵn ngày quá khứ và ngày vượt trần. Dưới ô có dòng "Không giữ quá …" cho '
     'bạn biết hạn tối đa.'],
    ['Số điện thoại / Địa chỉ / Địa chỉ giao hàng', 'Chỉ hiển thị', 'Không',
     'Tự điền theo hợp đồng hoặc khách hàng', 'Ba ô này in ra bản in của phiếu.'],
    ['Phòng ban yêu cầu', 'Chỉ hiển thị', 'Không', 'Phòng ban của bạn', 'Phần mềm tự điền.'],
    ['Ghi chú', 'Ô nhập chữ, tối đa 255 ký tự', 'Có (loại Xuất giữ khác)', 'Để trống',
     'Ghi lý do giữ hàng để các cấp xử lý nắm được.'],
    ['Lý do từ chối gần nhất', 'Chỉ hiển thị', '—', 'Ẩn',
     'Chỉ hiện khi phiếu đã từng bị trả về. Đây là chỗ DUY NHẤT bạn biết vì sao bị trả.'],
])

b.h2('5. Khối File đính kèm')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Chọn tệp', 'Nút chọn tệp từ máy', 'Có với loại Xuất giữ khác', 'Chưa có tệp đính kèm',
     'Nhận tệp PDF, ảnh, Word, Excel; mỗi tệp tối đa 13 MB. Đính kèm được nhiều tệp.'],
])

b.h2('6. Khối Chi tiết hàng hóa')
b.table([
    ['Cột', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Cần xuất', 'Ô tích', '—', 'Bỏ tích',
     'Chỉ có ở năm loại có hợp đồng. Tích dòng bạn muốn giữ.'],
    ['Tên hàng hóa / Mã hàng hóa / Model / Thương hiệu', 'Chỉ hiển thị', '—', 'Theo hàng hóa',
     'Không sửa được.'],
    ['Có thể giữ', 'Chỉ hiển thị', '—', 'Theo tồn kho',
     'Số hàng còn trong kho có thể giữ được, đã trừ hàng khuyến mại.'],
    ['SL hợp đồng / Đã xuất kho', 'Chỉ hiển thị', '—', 'Theo hợp đồng',
     'Chỉ có ở loại có hợp đồng. Loại Xuất giữ HĐDV ẩn hai cột này.'],
    ['Đề nghị', 'Ô nhập số', 'Có', 'Để trống',
     'Số lượng bạn xin giữ. Phải lớn hơn 0; với loại có hợp đồng thì không vượt phần còn lại '
     'của hợp đồng.'],
    ['ĐVT', 'Ô chọn hoặc chỉ hiển thị', 'Có với loại Xuất giữ khác', 'Đơn vị cơ bản',
     'Chỉ loại Xuất giữ khác mới chọn được.'],
    ['Đơn giá / Thành tiền', 'Chỉ hiển thị', '—', 'Theo dữ liệu',
     'Thành tiền bằng Đơn giá nhân số lượng đề nghị.'],
    ['Nút xóa dòng', 'Nút biểu tượng thùng rác', '—', '—',
     'Chỉ có ở loại Xuất giữ khác. Bỏ hẳn dòng hàng khỏi phiếu.'],
])

b.h2('7. Các nút ở cuối màn')
b.table([
    ['Nút', 'Phần mềm làm gì', 'Sau khi bấm'],
    ['Lưu nháp', 'Ghi phiếu ở trạng thái Đang tạo, chưa gửi đi đâu.',
     'Hiện thông báo thành công và quay về màn danh sách. Chỉ mình bạn thấy phiếu này.'],
    ['Gửi duyệt', 'Ghi phiếu và chuyển sang Chờ TP duyệt, đồng thời báo cho Trưởng phòng.',
     'Hiện thông báo thành công và quay về màn danh sách. Từ lúc này bạn không sửa được nữa.'],
    ['Lưu và tiếp tục', 'Lưu nháp phiếu rồi ở lại màn để lập tiếp phiếu mới.',
     'Màn hình được làm mới, không quay về danh sách. Chỉ có ở màn Tạo mới.'],
    ['Quay lại', 'Thoát khỏi màn lập phiếu.',
     'Nếu bạn đã nhập gì mà chưa lưu, phần mềm hỏi xác nhận trước khi rời trang.'],
])
b.para('Lưu nháp KHÔNG kiểm tra tồn kho, Gửi duyệt thì CÓ. Vì vậy có thể lưu nháp thành công '
       'nhưng gửi duyệt lại báo thiếu hàng — đó là hành vi đúng, không phải lỗi.',
       bold_prefix='Lưu ý: ')

b.h2('8. Các lỗi thường gặp khi lưu')
b.table([
    ['Tình huống', 'Phần mềm báo gì', 'Cách xử lý'],
    ['Chưa chọn Loại yêu cầu', 'Bắt buộc phải chọn', 'Chọn loại ở ô đầu tiên.'],
    ['Chưa chọn Hợp đồng (loại có hợp đồng)', 'Bắt buộc phải chọn',
     'Bấm nút Chọn cạnh ô Hợp đồng.'],
    ['Chưa chọn Khách hàng (loại Xuất giữ khác)', 'Bắt buộc phải chọn',
     'Gõ tối thiểu 2 ký tự vào ô Khách hàng rồi chọn.'],
    ['Chưa nhập Ghi chú (loại Xuất giữ khác)', 'Bắt buộc phải nhập',
     'Nhập lý do giữ hàng vào ô Ghi chú.'],
    ['Chưa đính kèm tệp (loại Xuất giữ khác)', 'Bắt buộc phải chọn',
     'Bấm Chọn tệp và tải lên ít nhất một tệp.'],
    ['Chưa nhập Giữ đến ngày', 'Giữ đến ngày – Bắt buộc phải nhập.', 'Chọn ngày trên lịch.'],
    ['Chọn ngày quá khứ', 'Giữ đến ngày – Phải nhập ngày tương lai.',
     'Chọn ngày sau ngày hôm nay.'],
    ['Chọn ngày vượt trần cấu hình', 'Giữ đến ngày – Không thể giữ quá …',
     'Chọn ngày trong phạm vi cho phép. Phần mềm KHÔNG tự kéo ngày về trần.'],
    ['Chưa thêm hàng hóa nào', 'Bắt buộc phải chọn hàng hoá cần giữ.',
     'Chọn hợp đồng, hoặc bấm Thêm hàng hóa.'],
    ['Không tích dòng nào, hoặc số lượng đều bằng 0',
     'Chưa chọn hàng hoá nào cần giữ, hoặc số lượng đề nghị đều bằng 0.',
     'Tích ít nhất một dòng và nhập số lớn hơn 0.'],
    ['Số lượng bằng 0 ở dòng có tích', 'Phải lớn hơn 0.', 'Nhập số lớn hơn 0 hoặc bỏ tích dòng.'],
    ['Số lượng vượt phần còn lại của hợp đồng',
     'Vượt số lượng còn lại của hợp đồng (còn …).',
     'Nhập lại số nhỏ hơn. Phần còn lại = SL hợp đồng trừ Đã xuất kho.'],
    ['Hàng không nằm trong hợp đồng, hoặc sai đơn vị tính',
     'Hàng hoá không có trong hợp đồng.',
     'Kiểm tra lại đơn vị tính của dòng hàng so với hợp đồng.'],
    ['Gửi duyệt mà kho không đủ hàng', 'Vượt số có thể giữ (còn …).',
     'Giảm số lượng, hoặc lưu nháp chờ hàng về rồi gửi sau.'],
    ['Ghi chú quá 255 ký tự', 'Không được vượt quá 255 ký tự', 'Rút ngắn nội dung ghi chú.'],
])

# =============================================================== PHAN 4
b.h1('PHẦN 4: SỬA PHIẾU')

b.para('Bạn chỉ sửa được phiếu do chính mình lập và đang ở trạng thái Đang tạo — tức phiếu còn '
       'nháp, hoặc phiếu vừa bị một cấp trả về. Phiếu đang chờ duyệt hoặc đã duyệt thì không '
       'sửa được.', bold_prefix='Quan trọng: ')
b.para('Cách vào: bấm biểu tượng bút chì ở cột Hành động, hoặc mở phiếu ra rồi bấm nút Sửa ở '
       'cuối màn chi tiết.')
b.para('Màn sửa có bố cục giống màn lập phiếu, thêm hai ô chỉ hiển thị: Mã phiếu và Trạng thái. '
       'Loại yêu cầu và Hợp đồng bị khóa, không đổi được. Không có nút Lưu và tiếp tục.')
b.para('Nếu phiếu bị trả về, hãy đọc ô "Lý do từ chối gần nhất" ở cuối khối Thông tin chung '
       'trước khi sửa.', bold_prefix='Mẹo: ')
b.para('Khi bạn lưu lại, phần mềm XÓA dấu duyệt của cả ba cấp. Bấm Gửi duyệt thì phiếu đi lại '
       'quy trình từ đầu, bắt đầu ở Chờ TP duyệt.', bold_prefix='Lưu ý: ')
b.para('Với loại Xuất giữ khác, tệp đính kèm vẫn bắt buộc khi sửa. Gỡ hết tệp rồi lưu sẽ bị '
       'chặn.')

# =============================================================== PHAN 5
b.h1('PHẦN 5: XEM CHI TIẾT PHIẾU')

b.para('Bấm vào mã phiếu ở cột thứ hai của bảng danh sách để mở màn chi tiết.')
b.image('09-chi-tiet.png', 'Màn chi tiết một phiếu đã duyệt')
b.para('Màn chi tiết gồm các khối:')
b.bullet('Thông tin chung: Mã phiếu, Trạng thái, Loại yêu cầu, Hợp đồng, Khách hàng, Giữ đến '
         'ngày, Phòng ban yêu cầu, Địa chỉ, Ghi chú, người lập và ngày lập.')
b.bullet('File đính kèm: danh sách tệp, bấm vào tên tệp để mở xem.')
b.bullet('Chi tiết: bảng hàng hóa với số lượng đề nghị, đơn giá, thành tiền và dòng Tổng cộng.')
b.bullet('Lịch sử duyệt: ai đã duyệt ở cấp nào, lúc nào.')
b.bullet('Lịch sử thay đổi, mặc định thu gọn.')
b.para('Các nút ở cuối màn chi tiết luôn khớp với các nút ở cột Hành động ngoài danh sách của '
       'đúng phiếu đó, riêng nút Từ chối thì chỉ có ở màn chi tiết.')

# =============================================================== PHAN 6
b.h1('PHẦN 6: DUYỆT VÀ TỪ CHỐI PHIẾU')

b.h2('1. Luồng xử lý ba cấp')
b.para('Sau khi người lập bấm Gửi duyệt, phiếu đi theo trình tự:')
b.bullet('Chờ TP duyệt: chờ Trưởng phòng quản lý phòng ban ghi trên phiếu.')
b.bullet('Chờ BGĐ duyệt: chỉ những phiếu thuộc diện phải trình Ban giám đốc mới qua bước này.')
b.bullet('Chờ KT duyệt: Kế toán lập Phiếu xuất giữ.')
b.bullet('Đang xuất giữ: Kế toán đã lập phiếu nhưng còn để nháp.')
b.bullet('Đã duyệt: hàng đã được giữ cho khách hàng.')
b.para('Phiếu có phải qua Ban giám đốc hay không do phần mềm tự xác định, dựa trên tỉ lệ tiền đã '
       'thu của hợp đồng, hoặc tổng giá trị hàng xin giữ với phiếu không gắn hợp đồng.')

b.h2('2. Cách duyệt một phiếu (Trưởng phòng / Ban giám đốc)')
b.image('10-chi-tiet-nguoi-duyet.png', 'Màn chi tiết nhìn từ người có quyền duyệt')
b.bullet('Mở phiếu bằng cách bấm vào mã phiếu, hoặc bấm biểu tượng dấu tích ở cột Hành động.')
b.bullet('Xem lại Khách hàng, Giữ đến ngày, danh sách hàng và số lượng đề nghị.')
b.bullet('Bấm nút duyệt ở cuối màn. Nhãn nút nêu rõ cấp bạn đang ký: TP duyệt hoặc BGĐ duyệt.')
b.bullet('Phần mềm hỏi xác nhận; bấm Duyệt để xác nhận.')
b.para('Nếu bạn là Ban giám đốc, phần mềm yêu cầu bạn nhập LẠI ô Giữ đến ngày trước khi duyệt.',
       bold_prefix='Chú ý: ')
b.para('Người duyệt KHÔNG sửa được số lượng đề nghị. Nếu thấy sai, hãy từ chối phiếu để người '
       'lập sửa lại.', bold_prefix='Lưu ý: ')

b.h2('3. Cách từ chối một phiếu')
b.image('11-popup-tu-choi.png', 'Cửa sổ Từ chối yêu cầu xuất giữ')
b.bullet('Mở phiếu và bấm nút Từ chối ở cuối màn chi tiết.')
b.bullet('Phần mềm mở cửa sổ có hiển thị mã phiếu.')
b.bullet('Nhập lý do trả phiếu về (bắt buộc, tối đa 255 ký tự) rồi bấm nút xác nhận.')
b.para('Phiếu quay về trạng thái Đang tạo và chỉ người lập nhìn thấy. Đây cũng là trạng thái duy '
       'nhất cho phép người lập sửa hoặc xóa phiếu.')
b.para('Cả ba cấp đều từ chối được, kể cả Kế toán ở bước Chờ KT duyệt.')
b.para('Vì phiếu bị trả về nằm chung trạng thái "Đang tạo" với phiếu chưa gửi bao giờ, hãy bật '
       'cột "Lý do từ chối" ở Cấu hình cột để phân biệt nhanh.', bold_prefix='Mẹo: ')

b.h2('4. Kế toán: lập phiếu xuất giữ')
b.image('15-cho-ke-toan-lap-phieu.png',
        'Phiếu ở trạng thái Chờ KT duyệt, nút Lập phiếu xuất giữ hiện ở cuối màn')
b.para('Ở bước này KHÔNG có nút duyệt. Thay vào đó Kế toán bấm "Lập phiếu xuất giữ"; phần mềm '
       'chuyển sang màn lập Phiếu xuất giữ, gắn sẵn yêu cầu này.')
b.bullet('Kế toán lưu nháp phiếu xuất giữ → yêu cầu chuyển sang Đang xuất giữ.')
b.bullet('Kế toán bấm Duyệt giữ hàng → hàng được ghi vào kho hàng giữ, yêu cầu chuyển sang '
         'Đã duyệt, cột Người duyệt và Ngày duyệt được điền.')
b.bullet('Kế toán xóa phiếu xuất giữ còn nháp → yêu cầu quay lại Chờ KT duyệt.')
b.para('Chủ hàng giữ là NGƯỜI LẬP YÊU CẦU, không phải Kế toán. Nghĩa là sau khi duyệt xong, hàng '
       'nằm trong danh sách hàng giữ của bạn — người đã lập phiếu.', bold_prefix='Quan trọng: ')
b.para('Mỗi yêu cầu chỉ lập được MỘT phiếu xuất giữ. Nếu yêu cầu đã có phiếu, phần mềm báo và '
       'không cho lập thêm.')

b.h2('5. Khi hai người cùng xử lý một phiếu')
b.para('Nếu phiếu đã được người khác duyệt hoặc từ chối trước đó, phần mềm báo "Phiếu không ở '
       'trạng thái chờ duyệt." và không thực hiện thao tác của bạn. Hãy tải lại danh sách để xem '
       'trạng thái mới nhất.')

# =============================================================== PHAN 7
b.h1('PHẦN 7: XÓA PHIẾU')

b.para('Chỉ người lập phiếu mới xóa được, và chỉ khi phiếu đang ở trạng thái Đang tạo. Phiếu '
       'đang chờ duyệt hoặc đã duyệt không xóa được.')
b.image('12-xac-nhan-xoa.png', 'Hộp thoại Xác nhận xóa phiếu')
b.bullet('Bấm biểu tượng thùng rác ở cột Hành động, hoặc nút Xóa ở cuối màn chi tiết.')
b.bullet('Phần mềm hỏi xác nhận, có ghi rõ mã phiếu để tránh xóa nhầm.')
b.bullet('Bấm Xóa để xác nhận, hoặc Hủy để thoát.')
b.para('Phiếu đã xóa không khôi phục lại được.')

# =============================================================== PHAN 8
b.h1('PHẦN 8: IN VÀ XUẤT EXCEL')

b.h2('1. In một phiếu')
b.para('Bấm biểu tượng máy in ở cột Hành động, hoặc nút In ở cuối màn chi tiết. Phần mềm mở cửa '
       'sổ xem trước ngay trên màn đang đứng.')
b.image('14-in-phieu.png', 'Cửa sổ Xem trước yêu cầu xuất giữ')
b.para('Bản in gồm: phần đầu chứng từ theo công ty ghi trên phiếu, thông tin yêu cầu và khách '
       'hàng, bảng hàng hóa kèm dòng Tổng cộng, bảng thông tin duyệt và các ô ký tên.')
b.para('Bấm nút In trên cửa sổ xem trước để gửi lệnh in.')
b.para('Phiếu chưa duyệt thì ô Ngày duyệt trên bản in để TRỐNG, không in ngày hôm nay.',
       bold_prefix='Lưu ý: ')

b.h2('2. In danh sách')
b.para('Bấm nút In trên thanh công cụ của màn danh sách. Bản in danh sách dùng khổ A4 ngang và '
       'in đúng những phiếu khớp điều kiện lọc bạn đang áp, không chỉ trang đang xem.')

b.h2('3. Xuất Excel')
b.para('Bấm nút Xuất Excel trên thanh công cụ.')
b.image('05-chon-truong-xuat-excel.png', 'Cửa sổ Chọn trường xuất Excel')
b.bullet('Mặc định chọn sẵn cả 15 trường: Mã phiếu, Loại yêu cầu, Người tạo, Ngày tạo, Hợp đồng, '
         'Khách hàng, Giữ đến ngày, Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, '
         'Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối.')
b.bullet('Bỏ chọn trường không cần bằng cách bấm dấu nhân trên thẻ tên trường.')
b.bullet('Thứ tự cột trong tệp chạy theo đúng thứ tự bạn chọn.')
b.bullet('Bấm Xuất file để tải tệp về máy.')

# =============================================================== PHAN 9
b.h1('PHẦN 9: XEM LỊCH SỬ THAY ĐỔI')

b.para('Có hai cách xem lịch sử của một phiếu:')
b.bullet('Bấm biểu tượng đồng hồ ở cột Hành động của màn danh sách.')
b.bullet('Mở phiếu ra, kéo xuống khối Lịch sử thay đổi rồi bấm nút Xem lịch sử.')
b.image('13-lich-su-thay-doi.png', 'Cửa sổ Lịch sử thay đổi của phiếu')
b.para('Danh sách hiển thị các mốc thao tác theo thứ tự mới nhất trước, mỗi mốc ghi rõ nhóm thao '
       'tác (tạo mới, chỉnh sửa, duyệt, từ chối), người thực hiện, thời điểm và những giá trị đã '
       'thay đổi.')
b.para('Các phiếu được lập từ trước khi phần mềm bật tính năng ghi lịch sử sẽ hiện dòng "Chưa có '
       'lịch sử thao tác nào." — đây không phải lỗi.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 10
b.h1('PHẦN 10: NHỮNG ĐIỀU CẦN NHỚ')

b.bullet('Lập yêu cầu xong KHÔNG có nghĩa là hàng đã được giữ. Hàng chỉ được giữ khi phiếu '
         'chuyển sang Đã duyệt.')
b.bullet('Loại yêu cầu quyết định toàn bộ phần còn lại của phiếu và KHÔNG đổi được sau khi lưu.')
b.bullet('Loại Xuất giữ khác bắt buộc ba thứ mà năm loại kia không cần: Khách hàng, Ghi chú và '
         'ít nhất một tệp đính kèm.')
b.bullet('Chỉ phiếu ở trạng thái Đang tạo mới sửa hoặc xóa lại được.')
b.bullet('Phiếu bị trả về quay đúng về "Đang tạo" — xem cột Lý do từ chối để biết vì sao.')
b.bullet('Sửa lại phiếu thì phần mềm xóa dấu duyệt của cả ba cấp, phiếu đi lại từ đầu.')
b.bullet('Lưu nháp không kiểm tra tồn kho, Gửi duyệt thì có.')
b.bullet('Ban giám đốc phải nhập lại Giữ đến ngày ở bước duyệt của mình.')
b.bullet('Kế toán không bấm duyệt mà lập Phiếu xuất giữ; mỗi yêu cầu chỉ có một phiếu xuất giữ.')
b.bullet('Chủ hàng giữ là người lập yêu cầu, không phải Kế toán lập phiếu.')

print(b.finish())
