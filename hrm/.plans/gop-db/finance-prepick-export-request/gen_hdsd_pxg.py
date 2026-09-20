# -*- coding: utf-8 -*-
"""Sinh HDSD man "Phieu xuat giu" (PXG) tu khung HDSD_MAU.docx.

Anh chup that: ./warehouse_prepick_shots (Playwright MCP, 1440x900, ngay 18/09/2026).
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

SHOTS = os.path.join(BASE, 'warehouse_prepick_shots')
OUT = os.path.join(BASE, 'HDSD_Phieu xuat giu.docx')

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title='(Màn hình: Phiếu xuất giữ)',
                doc_title='HDSD - Phiếu xuất giữ')

# =============================================================== TONG QUAN
b.h1('TỔNG QUAN')

b.h2('1. Thuật ngữ sử dụng trong tài liệu')
b.table([
    ['Thuật ngữ', 'Ý nghĩa'],
    ['Hàng giữ', 'Số lượng hàng hóa trong kho được giữ lại cho một khách hàng cụ thể, do một '
                 'nhân viên kinh doanh đứng tên giữ, tới một hạn nhất định.'],
    ['Lô hàng giữ', 'Một dòng hàng giữ cụ thể, gồm: người giữ – khách hàng – hàng hóa – hạn giữ '
                    '– công ty.'],
    ['Yêu cầu xuất giữ', 'Phiếu do nhân viên kinh doanh lập để xin giữ hàng, mã bắt đầu bằng '
                         'PYCXG. Là phiếu nguồn của phiếu xuất giữ.'],
    ['Phiếu xuất giữ', 'Phiếu bạn lập ở bước Kế toán, mã bắt đầu bằng PXG. Khi phiếu này được '
                       'duyệt thì hàng mới thực sự được giữ.'],
    ['Người yêu cầu', 'Người đã lập yêu cầu xuất giữ. Chính người này sẽ đứng tên giữ hàng, '
                      'không phải bạn.'],
    ['Phòng yêu cầu', 'Phòng ban của người yêu cầu.'],
    ['SL có thể giữ', 'Số hàng còn trong kho có thể giữ được, đã trừ hàng khuyến mại.'],
    ['SL yêu cầu', 'Số lượng người lập yêu cầu đã xin giữ cho dòng hàng đó.'],
    ['SL xuất giữ', 'Số lượng bạn chốt thực xuất giữ. Không được vượt SL yêu cầu.'],
    ['SL giữ (ĐV cơ bản)', 'Số lượng đã quy đổi về đơn vị cơ bản và cộng thật vào kho hàng giữ. '
                           'Chỉ hiện ở màn chi tiết của phiếu đã duyệt.'],
    ['Đang tạo', 'Phiếu còn nháp, chưa ghi hàng giữ. Đây là trạng thái duy nhất cho phép sửa và '
                 'xóa phiếu.'],
    ['Đã duyệt', 'Phiếu đã duyệt, hàng đã được giữ, yêu cầu nguồn cũng chuyển sang Đã duyệt.'],
])

b.h2('2. Cập nhật tài liệu')
b.table([
    ['Phiên bản', 'Ngày', 'Nội dung'],
    ['1.0', '18/09/2026', 'Ban hành lần đầu cho màn hình Phiếu xuất giữ trên phân hệ Tài chính.'],
])

b.h2('3. Giới thiệu chung')
b.para('Màn hình Phiếu xuất giữ dành cho Kế toán. Đây là bước cuối của luồng giữ hàng: nhân viên '
       'kinh doanh lập Yêu cầu xuất giữ, Trưởng phòng và Ban giám đốc duyệt, rồi tới bạn.')
b.para('Đây là chứng từ DUY NHẤT trong phần mềm sinh ra hàng giữ. Khi bạn bấm "Duyệt giữ hàng", '
       'phần mềm cộng số lượng vào kho hàng giữ và từ đó các màn Danh sách hàng giữ, Gia hạn, '
       'Hủy, Điều chuyển mới có dữ liệu để làm việc.', bold_prefix='Quan trọng: ')
b.para('Phiếu xuất giữ không tồn tại độc lập: mỗi phiếu luôn thuộc về đúng một yêu cầu xuất giữ, '
       'và một yêu cầu chỉ có tối đa một phiếu.')
b.para('Đường dẫn truy cập: Phân hệ Tài chính → nhóm Giữ hàng → Phiếu xuất giữ. Có thể gõ thẳng '
       'địa chỉ /finance/warehouse-prepick-requests trên thanh địa chỉ trình duyệt.')
b.para('Mã phiếu do phần mềm tự sinh theo dạng PXG kèm 5 chữ số, ví dụ PXG-02190.')

b.h2('4. Quyền sử dụng và phạm vi dữ liệu')
b.para('Khác các màn khác, màn này không có nút "Tạo mới" độc lập. Muốn lập phiếu bạn phải đi từ '
       'một yêu cầu xuất giữ đang ở bước Kế toán xử lý.', bold_prefix='Lưu ý: ')

b.h3('4.1. Bảng quyền của màn hình')
b.table([
    ['Tên quyền', 'Cho phép làm gì', 'Nút / phần tương ứng trên màn hình', 'Ghi chú'],
    ['Kế toán duyệt hàng giữ',
     'Lập phiếu xuất giữ từ yêu cầu, sửa phiếu nháp của mình và bấm Duyệt giữ hàng.',
     'Nút Lập phiếu xuất giữ (ở màn Yêu cầu xuất giữ); nút Lưu nháp, Duyệt giữ hàng, Không '
     'duyệt ở màn phiếu.',
     'Phải cùng công ty với yêu cầu nguồn. Người có quyền này còn xem được mọi phiếu trong công '
     'ty mình.'],
    ['Xem phiếu hàng giữ theo tổng công ty', 'Xem phiếu của mọi công ty.',
     'Toàn bộ danh sách; ô lọc Công ty và Phòng ban.', 'Là phạm vi rộng nhất.'],
    ['Xem phiếu hàng giữ theo công ty', 'Xem phiếu thuộc công ty của mình.',
     'Danh sách; ô lọc Phòng ban.', '—'],
    ['Xem phiếu hàng giữ theo phòng ban',
     'Xem phiếu thuộc các phòng ban mình được phân công quản lý và phòng ban của chính mình.',
     'Danh sách.', '—'],
])

b.h3('4.2. Phạm vi dữ liệu chạy theo bên YÊU CẦU')
b.para('Công ty và phòng ban ghi trên phiếu xuất giữ được chép từ NGƯỜI LẬP YÊU CẦU, không phải '
       'từ bạn. Vì vậy khi lọc theo phòng ban, bạn đang lọc theo phòng của người yêu cầu.')

b.h3('4.3. Người dùng không có quyền nào ở trên')
b.para('Bạn vẫn vào được màn hình nhưng danh sách chỉ hiển thị phiếu do chính bạn lập. Nút lập '
       'phiếu và các nút duyệt không dùng được.')

# =============================================================== PHAN 1
b.h1('PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')

b.h2('1. Cách vào màn hình')
b.bullet('Đăng nhập phần mềm.')
b.bullet('Chọn phân hệ Tài chính.')
b.bullet('Ở thanh menu bên trái, mở nhóm Hàng hoá - Dịch vụ - Vận chuyển → Giữ hàng.')
b.bullet('Bấm mục Phiếu xuất giữ.')

b.h2('2. Bố cục màn hình danh sách')
b.image('01-danh-sach.png', 'Màn hình Phiếu xuất giữ lúc mới vào')
b.para('Màn hình chia làm hai khối:')
b.bullet('Khối Bộ lọc danh sách ở trên: ô tìm nhanh, nút Tìm kiếm, nút Làm mới, nút Cài đặt '
         'bộ lọc và nút Tìm kiếm nâng cao.')
b.bullet('Khối bảng danh sách ở dưới: thanh công cụ (Lập từ yêu cầu, In, Xuất Excel, Cấu hình '
         'cột), bảng dữ liệu và thanh phân trang.')

b.h2('3. Ý nghĩa các trạng thái')
b.table([
    ['Trạng thái', 'Màu', 'Nghĩa là gì', 'Yêu cầu nguồn đang ở đâu'],
    ['Đang tạo', 'Xám', 'Phiếu còn nháp, CHƯA ghi hàng giữ.',
     'Yêu cầu nguồn ở trạng thái "Đang xuất giữ".'],
    ['Đã duyệt', 'Xanh lá', 'Hàng ĐÃ được ghi vào kho hàng giữ.',
     'Yêu cầu nguồn ở trạng thái "Đã duyệt".'],
    ['Chờ duyệt', 'Cam', 'Chỉ còn ở dữ liệu cũ; phần mềm hiện tại không sinh trạng thái này nữa.',
     '—'],
])

# =============================================================== PHAN 2
b.h1('PHẦN 2: DANH SÁCH PHIẾU')

b.h2('1. Các cột của bảng')
b.table([
    ['Cột', 'Nội dung'],
    ['STT', 'Số thứ tự dòng, chạy liên tục theo trang.'],
    ['Mã phiếu', 'Mã phiếu xuất giữ. Bấm vào mã để mở màn chi tiết.'],
    ['Yêu cầu xuất giữ', 'Mã yêu cầu nguồn. Bấm vào để mở yêu cầu đó trong TAB MỚI.'],
    ['Người yêu cầu', 'Người đã lập yêu cầu — cũng là người sẽ đứng tên giữ hàng.'],
    ['Phòng yêu cầu', 'Phòng ban của người yêu cầu.'],
    ['Người tạo', 'Người đã lập phiếu xuất giữ, tức Kế toán.'],
    ['Ngày tạo', 'Ngày giờ lập phiếu xuất giữ.'],
    ['Trạng thái', 'Đang tạo (xám) hoặc Đã duyệt (xanh lá).'],
    ['Người duyệt', 'Người đã bấm Duyệt giữ hàng.'],
    ['Ngày duyệt', 'Thời điểm duyệt.'],
    ['Khách hàng', 'Khách hàng được giữ hàng. Cột này ẩn sẵn.'],
    ['Giữ đến ngày', 'Hạn giữ hàng ghi trên phiếu. Cột này ẩn sẵn.'],
    ['Người cập nhật / Ngày cập nhật', 'Lần chỉnh sửa gần nhất. Hai cột này ẩn sẵn.'],
    ['Ghi chú', 'Ghi chú trên phiếu. Cột này ẩn sẵn.'],
    ['Hành động', 'Các nút thao tác của từng dòng.'],
])
b.para('Bốn cột có mũi tên sắp xếp là Mã phiếu, Ngày tạo, Ngày duyệt và Giữ đến ngày.')
b.para('Cột "Người yêu cầu" và cột "Người tạo" là HAI người khác nhau: người yêu cầu là nhân '
       'viên kinh doanh, người tạo là Kế toán lập phiếu.', bold_prefix='Lưu ý: ')

b.h2('2. Tìm kiếm và lọc')
b.para('Ô tìm nhanh ở trên cùng tìm theo mã phiếu xuất giữ. Gõ xong bấm nút Tìm kiếm hoặc nhấn '
       'Enter.')
b.image('02-bo-loc-nang-cao.png', 'Bảng lọc nâng cao đang mở')
b.table([
    ['Tiêu chí lọc', 'Cách dùng'],
    ['Công ty', 'Chỉ hiện với người có quyền xem theo tổng công ty.'],
    ['Phòng ban', 'Chỉ hiện với người có quyền xem từ cấp công ty trở lên.'],
    ['Mã phiếu', 'Gõ một phần hoặc toàn bộ mã phiếu xuất giữ.'],
    ['Yêu cầu xuất giữ', 'Gõ mã yêu cầu nguồn để tìm phiếu lập từ yêu cầu đó.'],
    ['Trạng thái', 'Chọn Đang tạo hoặc Đã duyệt.'],
    ['Người tạo', 'Chọn Kế toán đã lập phiếu.'],
    ['Người duyệt', 'Chọn người đã duyệt giữ hàng.'],
    ['Người yêu cầu', 'Chọn nhân viên đã lập yêu cầu — người đứng tên giữ hàng.'],
    ['Khách hàng', 'Chọn khách hàng được giữ hàng.'],
    ['Tên, mã hàng', 'Một ô chung cho cả tên và mã hàng hóa.'],
    ['Ngày tạo từ / Ngày tạo đến', 'Khoảng ngày LẬP phiếu — không phải ngày duyệt, cũng không '
                                   'phải hạn giữ.'],
])
b.para('Các ô lọc nâng cao tự lọc lại ngay khi bạn chọn. Bấm Làm mới để xóa toàn bộ điều kiện.')

b.h2('3. Chọn ô lọc muốn hiển thị')
b.image('04-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc')
b.para('Tắt bớt những ô lọc không dùng và kéo ô hay dùng lên đầu. Cấu hình lưu riêng cho từng '
       'người và từng màn.')

b.h2('4. Chọn cột hiển thị của bảng')
b.image('05-cau-hinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột')
b.para('Ba cột STT, Mã phiếu và Hành động có biểu tượng ổ khóa: luôn hiển thị. Năm cột Khách '
       'hàng, Giữ đến ngày, Người cập nhật, Ngày cập nhật và Ghi chú mặc định tắt.')

b.h2('5. Các nút trên thanh công cụ')
b.table([
    ['Nút', 'Tác dụng', 'Điều kiện hiển thị'],
    ['Lập từ yêu cầu', 'Đưa bạn sang màn Yêu cầu xuất giữ để chọn yêu cầu cần lập phiếu.',
     'Luôn hiển thị.'],
    ['In', 'Mở bản in danh sách theo đúng điều kiện lọc đang áp.', 'Luôn hiển thị.'],
    ['Xuất Excel', 'Mở cửa sổ chọn trường rồi tải tệp Excel về máy.', 'Luôn hiển thị.'],
    ['Cấu hình cột hiển thị', 'Mở cửa sổ Tuỳ chỉnh cột.', 'Luôn hiển thị.'],
])
b.para('Nút "Lập từ yêu cầu" KHÔNG mở form trống — nó chỉ chuyển bạn sang màn Yêu cầu xuất giữ. '
       'Ở đó bạn tìm yêu cầu đang ở trạng thái "Chờ KT duyệt", mở ra rồi bấm "Lập phiếu xuất '
       'giữ".', bold_prefix='Quan trọng: ')

b.h2('6. Các thao tác trên từng dòng')
b.table([
    ['Thao tác', 'Tác dụng', 'Khi nào hiện'],
    ['Sửa (biểu tượng bút chì)', 'Mở màn sửa phiếu nháp.',
     'Phiếu do chính bạn lập và đang ở trạng thái Đang tạo.'],
    ['Xóa (biểu tượng thùng rác)', 'Xóa hẳn phiếu nháp; yêu cầu nguồn quay lại bước Kế toán.',
     'Phiếu do chính bạn lập và đang ở trạng thái Đang tạo.'],
    ['In (biểu tượng máy in)', 'Mở bản in của phiếu đó.', 'Luôn hiện.'],
    ['Lịch sử (biểu tượng đồng hồ)', 'Mở cửa sổ lịch sử thay đổi của phiếu.', 'Luôn hiện.'],
])
b.para('Màn này KHÔNG có nút Duyệt ở cột Hành động. Việc duyệt giữ hàng nằm trong màn lập hoặc '
       'màn sửa phiếu.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 3
b.h1('PHẦN 3: LẬP PHIẾU XUẤT GIỮ')

b.h2('1. Đường vào')
b.bullet('Vào màn Yêu cầu xuất giữ (Tài chính → Giữ hàng → Yêu cầu xuất giữ).')
b.bullet('Lọc Trạng thái = "Chờ KT duyệt" để thấy những yêu cầu đang chờ bạn.')
b.bullet('Bấm vào mã yêu cầu để mở chi tiết, rồi bấm nút "Lập phiếu xuất giữ" ở cuối màn.')
b.para('Nếu bạn không thấy nút đó thì một trong các điều sau đang đúng: yêu cầu không ở trạng '
       'thái Chờ KT duyệt, bạn không có quyền Kế toán duyệt hàng giữ, hoặc yêu cầu thuộc công '
       'ty khác.')

b.h2('2. Màn lập phiếu')
b.image('03-lap-phieu.png', 'Màn lập phiếu xuất giữ, dữ liệu nạp sẵn từ yêu cầu nguồn')
b.para('Phần mềm điền sẵn gần như toàn bộ phiếu từ yêu cầu nguồn: yêu cầu xuất giữ, loại yêu '
       'cầu, hợp đồng, người yêu cầu, phòng yêu cầu, khách hàng, địa chỉ, giữ đến ngày, và toàn '
       'bộ dòng hàng đã được xin giữ.')

b.h3('2.1. Khối Thông tin chung')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Yêu cầu xuất giữ', 'Chỉ hiển thị (là liên kết)', '—', 'Theo yêu cầu nguồn',
     'Bấm vào để mở yêu cầu trong tab mới. Không đổi được yêu cầu nguồn.'],
    ['Loại yêu cầu', 'Chỉ hiển thị', '—', 'Theo yêu cầu nguồn', 'Không sửa được.'],
    ['Hợp đồng', 'Chỉ hiển thị', '—', 'Theo yêu cầu nguồn',
     'Ẩn hẳn nếu yêu cầu thuộc loại Xuất giữ khác (loại đó không gắn hợp đồng).'],
    ['Người yêu cầu / Phòng yêu cầu', 'Chỉ hiển thị', '—', 'Theo yêu cầu nguồn',
     'Chính người này sẽ đứng tên giữ hàng, không phải bạn.'],
    ['Giữ đến ngày', 'Ô chọn ngày', 'Có', 'Theo yêu cầu nguồn',
     'Bạn sửa lại được. Hạn này sẽ ghi thẳng vào lô hàng giữ khi bấm Duyệt giữ hàng.'],
    ['Khách hàng / Địa chỉ', 'Chỉ hiển thị', '—', 'Theo yêu cầu nguồn',
     'Ô Địa chỉ ẩn đi nếu khách hàng chưa khai địa chỉ.'],
    ['Ghi chú', 'Ô nhập chữ, tối đa 255 ký tự', 'Không', 'Theo yêu cầu nguồn', '—'],
])

b.h3('2.2. Khối File đính kèm')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Chọn tệp', 'Nút chọn tệp từ máy', 'Không', 'Chưa có tệp đính kèm',
     'Nhận tệp PDF, ảnh, Word, Excel; mỗi tệp tối đa 13 MB. Đính kèm được nhiều tệp.'],
])

b.h3('2.3. Khối Chi tiết hàng hóa')
b.table([
    ['Cột', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Cần xuất', 'Ô tích', '—', 'Tích sẵn theo yêu cầu',
     'Bỏ tích nếu không xuất giữ dòng đó. Dòng bỏ tích bị làm mờ và lưu với số lượng 0.'],
    ['Tên hàng hóa / Mã hàng hóa / Model / Thương hiệu', 'Chỉ hiển thị', '—',
     'Theo yêu cầu nguồn', 'Không sửa được; không thêm hay xóa dòng.'],
    ['SL có thể giữ', 'Chỉ hiển thị', '—', 'Theo tồn kho',
     'Số hàng còn trong kho, đã trừ hàng khuyến mại. Đây đúng là con số phần mềm dùng khi kiểm '
     'tra lúc duyệt.'],
    ['SL yêu cầu', 'Chỉ hiển thị', '—', 'Theo yêu cầu nguồn',
     'Là mức trần của SL xuất giữ.'],
    ['SL xuất giữ', 'Ô nhập số', 'Có', 'Bằng SL yêu cầu',
     'Bạn chốt số thực xuất. Phải lớn hơn 0 và không vượt SL yêu cầu.'],
    ['ĐVT', 'Chỉ hiển thị', '—', 'Theo yêu cầu nguồn', 'Không đổi đơn vị tính ở màn này.'],
])

b.h2('3. Bốn nút ở cuối màn')
b.table([
    ['Nút', 'Phần mềm làm gì', 'Sau khi bấm'],
    ['Lưu nháp', 'Ghi phiếu ở trạng thái Đang tạo. CHƯA ghi hàng giữ.',
     'Yêu cầu nguồn chuyển sang "Đang xuất giữ". Bạn quay lại sửa tiếp lúc nào cũng được.'],
    ['Duyệt giữ hàng', 'Kiểm tra tồn kho rồi GHI HÀNG GIỮ cho người yêu cầu.',
     'Phần mềm hỏi xác nhận trước. Sau khi duyệt, phiếu sang Đã duyệt và yêu cầu nguồn cũng '
     'sang Đã duyệt. Không hoàn tác được.'],
    ['Không duyệt', 'Lưu phiếu ở trạng thái Đang tạo — GIỐNG HỆT nút Lưu nháp.',
     'Yêu cầu nguồn chuyển sang "Đang xuất giữ". Nút này KHÔNG trả yêu cầu về cho người lập.'],
    ['Quay lại', 'Thoát khỏi màn lập phiếu.',
     'Nếu bạn đã nhập gì mà chưa lưu, phần mềm hỏi xác nhận trước khi rời trang.'],
])
b.para('Nút "Không duyệt" KHÔNG trả yêu cầu về cho người lập. Muốn trả yêu cầu về, bạn phải sang '
       'màn Yêu cầu xuất giữ, mở yêu cầu đó ra và bấm nút "Từ chối".',
       bold_prefix='Rất dễ nhầm: ')

b.h2('4. Các lỗi thường gặp khi lưu')
b.table([
    ['Tình huống', 'Phần mềm báo gì', 'Cách xử lý'],
    ['Yêu cầu nguồn không còn ở bước Kế toán',
     'Yêu cầu này không ở bước Kế toán xử lý, hoặc bạn không đủ quyền lập phiếu xuất giữ.',
     'Tải lại màn Yêu cầu xuất giữ để xem trạng thái mới nhất.'],
    ['Yêu cầu đã có phiếu xuất giữ rồi', 'Yêu cầu này đã có phiếu xuất giữ …',
     'Mở phiếu đã có ra sửa, hoặc xóa phiếu nháp cũ rồi lập lại.'],
    ['Chưa nhập Giữ đến ngày', 'Giữ đến ngày – Bắt buộc phải nhập.', 'Chọn ngày trên lịch.'],
    ['Chọn ngày quá khứ', 'Giữ đến ngày – Phải nhập ngày tương lai.',
     'Chọn ngày sau ngày hôm nay.'],
    ['Không tích dòng nào, hoặc số lượng đều bằng 0',
     'Chưa chọn hàng hoá nào cần xuất giữ, hoặc số lượng đều bằng 0.',
     'Tích ít nhất một dòng và nhập số lớn hơn 0.'],
    ['Số lượng bằng 0 ở dòng có tích', 'Phải lớn hơn 0.', 'Nhập số lớn hơn 0 hoặc bỏ tích dòng.'],
    ['SL xuất giữ vượt SL yêu cầu', 'Vượt số lượng đề nghị của yêu cầu (…).',
     'Nhập lại số nhỏ hơn hoặc bằng cột SL yêu cầu.'],
    ['Duyệt mà kho không đủ hàng', 'Kho không đủ số lượng (còn …).',
     'Giảm SL xuất giữ, hoặc lưu nháp chờ hàng về rồi duyệt sau.'],
    ['Ghi chú quá 255 ký tự', 'Không được vượt quá 255 ký tự', 'Rút ngắn nội dung ghi chú.'],
])
b.para('Lưu nháp KHÔNG kiểm tra tồn kho, Duyệt giữ hàng thì CÓ. Vì vậy lưu nháp thành công nhưng '
       'duyệt lại báo thiếu hàng là hành vi đúng, không phải lỗi.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 4
b.h1('PHẦN 4: DUYỆT GIỮ HÀNG')

b.para('Đây là thao tác quan trọng nhất của màn hình và KHÔNG hoàn tác được. Hãy kiểm kỹ trước '
       'khi bấm.', bold_prefix='Quan trọng: ')

b.h2('1. Cần kiểm gì trước khi duyệt')
b.bullet('Người yêu cầu đúng chưa — chính người này sẽ đứng tên giữ hàng.')
b.bullet('Khách hàng đúng chưa.')
b.bullet('Giữ đến ngày đúng chưa — đây là hạn sẽ ghi vào lô hàng giữ.')
b.bullet('Những dòng nào thực sự cần xuất, và số lượng từng dòng.')
b.bullet('Cột SL có thể giữ có đủ cho SL xuất giữ không.')

b.h2('2. Các bước')
b.bullet('Bấm nút "Duyệt giữ hàng" ở cuối màn lập hoặc màn sửa phiếu.')
b.bullet('Phần mềm mở hộp thoại "Xác nhận duyệt giữ hàng", nói rõ thao tác sẽ ghi tồn hàng giữ '
         'và không hoàn tác được.')
b.bullet('Bấm "Duyệt giữ hàng" để xác nhận, hoặc Hủy để quay lại.')

b.h2('3. Phần mềm làm gì sau khi bạn xác nhận')
b.bullet('Kiểm tra tồn kho khả dụng của từng dòng. Nếu bất kỳ dòng nào thiếu hàng thì phần mềm '
         'báo lỗi tại dòng đó và KHÔNG ghi gì cả.')
b.bullet('Quy đổi số lượng của từng dòng về đơn vị cơ bản.')
b.bullet('Tìm lô hàng giữ khớp đúng bộ: hàng hóa – người yêu cầu – khách hàng – hạn giữ – công '
         'ty. Chưa có lô đó thì tạo lô mới.')
b.bullet('Cộng số lượng vào lô và ghi một dòng nhật ký tăng giảm của lô.')
b.bullet('Đóng dấu người duyệt, thời điểm duyệt lên phiếu; phiếu chuyển sang Đã duyệt.')
b.bullet('Đưa yêu cầu nguồn sang Đã duyệt.')
b.para('Sau khi duyệt, mở màn chi tiết của phiếu bạn sẽ thấy thêm cột "SL giữ (ĐV cơ bản)". Đây '
       'là con số đã cộng thật vào kho hàng giữ. Khi đối chiếu với màn Lịch sử giữ hàng phải '
       'nhìn cột này, không nhìn cột SL xuất giữ.', bold_prefix='Mẹo: ')

# =============================================================== PHAN 5
b.h1('PHẦN 5: SỬA PHIẾU')

b.para('Bạn chỉ sửa được phiếu do chính mình lập và đang ở trạng thái Đang tạo. Phiếu đã duyệt '
       'KHÔNG sửa được trong mọi trường hợp, vì hàng giữ đã được ghi.', bold_prefix='Quan trọng: ')
b.image('10-sua-phieu.png', 'Màn sửa phiếu xuất giữ còn nháp')
b.para('Cách vào: bấm biểu tượng bút chì ở cột Hành động, hoặc mở phiếu ra rồi bấm nút Sửa ở '
       'cuối màn chi tiết.')
b.para('Ở màn sửa bạn đổi được: Giữ đến ngày, Ghi chú, tệp đính kèm, ô tích Cần xuất và SL xuất '
       'giữ của từng dòng. Yêu cầu nguồn và danh sách hàng hóa thì khóa cứng.')
b.para('Bộ nút ở cuối màn giống hệt màn lập phiếu: Lưu nháp, Duyệt giữ hàng, Không duyệt và '
       'Quay lại. Bạn duyệt được ngay tại màn sửa.')

# =============================================================== PHAN 6
b.h1('PHẦN 6: XEM CHI TIẾT PHIẾU')

b.para('Bấm vào mã phiếu ở cột thứ hai của bảng danh sách để mở màn chi tiết.')
b.image('07-chi-tiet.png', 'Màn chi tiết một phiếu đã duyệt')
b.para('Màn chi tiết gồm các khối:')
b.bullet('Thông tin chung: Mã phiếu, Trạng thái, Yêu cầu xuất giữ, Loại yêu cầu, Hợp đồng, '
         'Người yêu cầu, Phòng yêu cầu, Giữ đến ngày, Khách hàng, Địa chỉ và Ghi chú.')
b.bullet('File đính kèm: danh sách tệp, bấm vào tên tệp để mở xem.')
b.bullet('Chi tiết: bảng hàng hóa; với phiếu đã duyệt có thêm cột SL giữ (ĐV cơ bản).')
b.bullet('Lịch sử thay đổi, mặc định thu gọn.')
b.para('Bấm vào mã yêu cầu xuất giữ để mở yêu cầu nguồn trong tab mới — tiện khi cần đối chiếu '
       'số lượng người lập đã xin.', bold_prefix='Mẹo: ')

# =============================================================== PHAN 7
b.h1('PHẦN 7: XÓA PHIẾU')

b.para('Chỉ người lập phiếu mới xóa được, và chỉ khi phiếu đang ở trạng thái Đang tạo. Phiếu đã '
       'duyệt không xóa được.')
b.image('11-xac-nhan-xoa.png', 'Hộp thoại Xác nhận xóa phiếu')
b.bullet('Bấm biểu tượng thùng rác ở cột Hành động, hoặc nút Xóa ở cuối màn chi tiết.')
b.bullet('Phần mềm hỏi xác nhận, có ghi rõ mã phiếu. Khi xóa từ màn chi tiết, câu hỏi còn nói '
         'rõ yêu cầu xuất giữ sẽ quay lại bước Kế toán xử lý.')
b.bullet('Bấm Xóa để xác nhận, hoặc Hủy để thoát.')
b.para('Sau khi xóa, yêu cầu nguồn quay về trạng thái "Chờ KT duyệt" và bạn lập lại phiếu khác '
       'được. Kho hàng giữ không thay đổi vì phiếu nháp chưa từng ghi hàng giữ.')

# =============================================================== PHAN 8
b.h1('PHẦN 8: IN VÀ XUẤT EXCEL')

b.h2('1. In một phiếu')
b.para('Bấm biểu tượng máy in ở cột Hành động, hoặc nút In ở cuối màn chi tiết. Phần mềm mở cửa '
       'sổ xem trước ngay trên màn đang đứng.')
b.image('09-in-phieu.png', 'Cửa sổ Xem trước phiếu xuất giữ')
b.para('Bản in gồm: phần đầu chứng từ theo công ty ghi trên phiếu, thông tin yêu cầu và khách '
       'hàng, bảng hàng hóa kèm dòng Tổng cộng, bảng thông tin duyệt và hai ô ký tên (Người lập, '
       'Kế toán duyệt).')
b.para('Phần đầu bản in lấy theo công ty của người yêu cầu, không lấy theo bạn.',
       bold_prefix='Lưu ý: ')

b.h2('2. In danh sách')
b.para('Bấm nút In trên thanh công cụ của màn danh sách. Bản in danh sách dùng khổ A4 ngang và '
       'in đúng những phiếu khớp điều kiện lọc bạn đang áp, không chỉ trang đang xem.')

b.h2('3. Xuất Excel')
b.para('Bấm nút Xuất Excel trên thanh công cụ.')
b.image('06-chon-truong-xuat-excel.png', 'Cửa sổ Chọn trường xuất Excel')
b.bullet('Mặc định chọn sẵn cả 14 trường: Mã phiếu, Yêu cầu xuất giữ, Người yêu cầu, Phòng yêu '
         'cầu, Người tạo, Ngày tạo, Khách hàng, Giữ đến ngày, Trạng thái, Người duyệt, '
         'Ngày duyệt, Người cập nhật, Ngày cập nhật, Ghi chú.')
b.bullet('Bỏ chọn trường không cần bằng cách bấm dấu nhân trên thẻ tên trường.')
b.bullet('Thứ tự cột trong tệp chạy theo đúng thứ tự bạn chọn.')
b.bullet('Bấm Xuất file để tải tệp về máy.')

# =============================================================== PHAN 9
b.h1('PHẦN 9: XEM LỊCH SỬ THAY ĐỔI')

b.para('Có hai cách xem lịch sử của một phiếu:')
b.bullet('Bấm biểu tượng đồng hồ ở cột Hành động của màn danh sách.')
b.bullet('Mở phiếu ra, kéo xuống khối Lịch sử thay đổi rồi bấm nút Xem lịch sử.')
b.image('08-lich-su-thay-doi.png', 'Khối Lịch sử thay đổi ở cuối màn chi tiết')
b.para('Danh sách hiển thị các mốc thao tác theo thứ tự mới nhất trước, mỗi mốc ghi rõ nhóm thao '
       'tác (tạo phiếu, chỉnh sửa, duyệt giữ hàng), người thực hiện, thời điểm và những giá trị '
       'đã thay đổi.')
b.para('Mốc "Duyệt giữ hàng" còn ghi rõ số lô hàng giữ đã được ghi, ví dụ "Đã ghi tồn giữ cho '
       '1 lô hàng.".', bold_prefix='Mẹo: ')

# =============================================================== PHAN 10
b.h1('PHẦN 10: NHỮNG ĐIỀU CẦN NHỚ')

b.bullet('Đây là chứng từ DUY NHẤT sinh ra hàng giữ trong phần mềm.')
b.bullet('Không có nút Tạo mới độc lập: phải đi từ một yêu cầu đang ở bước Chờ KT duyệt.')
b.bullet('Mỗi yêu cầu chỉ có tối đa một phiếu xuất giữ.')
b.bullet('Chủ hàng giữ là NGƯỜI LẬP YÊU CẦU, không phải bạn.')
b.bullet('Hạn giữ ghi vào lô lấy theo ô Giữ đến ngày trên phiếu này tại lúc bấm duyệt.')
b.bullet('Nút "Không duyệt" chỉ lưu nháp, KHÔNG trả yêu cầu về cho người lập — muốn trả thì sang '
         'màn Yêu cầu xuất giữ bấm Từ chối.')
b.bullet('Lưu nháp không kiểm tra tồn kho, Duyệt giữ hàng thì có.')
b.bullet('Phiếu đã duyệt không sửa và không xóa được.')
b.bullet('Xóa phiếu nháp thì yêu cầu nguồn quay lại bước Kế toán xử lý.')
b.bullet('Đối chiếu hàng giữ phải nhìn cột SL giữ (ĐV cơ bản), không nhìn cột SL xuất giữ.')

print(b.finish())
