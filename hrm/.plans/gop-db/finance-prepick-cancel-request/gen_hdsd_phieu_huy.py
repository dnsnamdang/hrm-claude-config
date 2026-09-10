# -*- coding: utf-8 -*-
"""Sinh HDSD man "Phieu huy hang giu" tu khung HDSD_MAU.docx.

Man ANH EM cua "Yeu cau huy hang giu" (gen_hdsd.py cung thu muc) — 2 file rieng.
Anh chup that: ./phieu_huy_shots (Playwright MCP, 1440x900, ngay 09/09/2026).
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

SHOTS = os.path.join(BASE, 'phieu_huy_shots')
OUT = os.path.join(BASE, 'HDSD_Phieu huy hang giu.docx')

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title='(Màn hình: Phiếu hủy hàng giữ)',
                doc_title='HDSD - Phiếu hủy hàng giữ')

# =============================================================== TONG QUAN
b.h1('TỔNG QUAN')

b.h2('1. Thuật ngữ sử dụng trong tài liệu')
b.table([
    ['Thuật ngữ', 'Ý nghĩa'],
    ['Hàng giữ', 'Số lượng hàng hóa được giữ lại cho một khách hàng cụ thể, do một nhân viên '
                 'kinh doanh đứng tên giữ.'],
    ['Lô hàng giữ', 'Một phần hàng giữ có cùng hạn giữ. Một hàng hóa có thể nằm trên nhiều lô '
                    'với hạn giữ khác nhau.'],
    ['Yêu cầu hủy hàng giữ', 'Phiếu do nhân viên kinh doanh lập để đề nghị trả lại kho phần hàng '
                             'đang giữ. Mã phiếu dạng PYCHHG. Phiếu này CHƯA trừ hàng giữ.'],
    ['Phiếu hủy hàng giữ', 'Chứng từ mô tả trong tài liệu này. Mã phiếu dạng PHHG. Bạn lập phiếu '
                           'này từ một phiếu yêu cầu đang chờ duyệt; lưu phiếu này CHÍNH LÀ '
                           'duyệt phiếu yêu cầu đó, và hàng giữ bị trừ ngay lúc đó.'],
    ['Có thể hủy', 'Số hàng giữ còn lại thực tế của người lập phiếu yêu cầu, đã trừ phần đang '
                   'nằm trong đề nghị xuất kho chưa xong. Đây là TRẦN của số bạn được duyệt.'],
    ['Yêu cầu hủy', 'Số lượng người lập phiếu yêu cầu đã đề nghị hủy. Chỉ để bạn tham khảo.'],
    ['Duyệt hủy', 'Số lượng bạn thực sự chấp thuận cho hủy. Đây là số bị trừ khỏi hàng giữ.'],
])

b.h2('2. Cập nhật tài liệu')
b.table([
    ['Phiên bản', 'Ngày', 'Nội dung'],
    ['1.0', '09/09/2026', 'Ban hành lần đầu cho màn hình Phiếu hủy hàng giữ trên phân hệ '
                          'Tài chính.'],
])

b.h2('3. Giới thiệu chung')
b.para('Màn hình Phiếu hủy hàng giữ dành cho người quản lý giữ hàng. Đây là nơi bạn xét duyệt '
       'các đề nghị hủy hàng giữ mà nhân viên kinh doanh đã gửi lên.')
b.para('Điểm quan trọng nhất cần nhớ: hệ thống KHÔNG có nút "Duyệt" riêng cho phiếu yêu cầu. '
       'Việc lập một Phiếu hủy hàng giữ chính là hành động duyệt. Ngay khi bạn lưu phiếu hủy, '
       'ba việc xảy ra cùng lúc: phiếu hủy được tạo, hàng giữ bị trừ đi, và phiếu yêu cầu gốc '
       'chuyển sang trạng thái Đã duyệt.')
b.para('Vì phiếu đã đụng tới số hàng thật nên phiếu hủy lập xong là chốt vĩnh viễn: không sửa '
       'được, không xóa được, không hủy duyệt được. Hãy kiểm tra kỹ số lượng trước khi bấm nút '
       'xác nhận.')

b.h2('4. Quyền sử dụng và phạm vi dữ liệu')

b.h3('4.1. Bảng quyền của màn hình')
b.table([
    ['Tên quyền', 'Cho phép làm gì', 'Nút / phần tương ứng trên màn hình'],
    ['Quản lý giữ hàng',
     'Lập phiếu hủy hàng giữ, tức duyệt phiếu yêu cầu. Đây là quyền DUY NHẤT cho phép thao tác '
     'ghi trên màn này. Đồng thời xem được mọi phiếu hủy thuộc công ty mình.',
     'Cửa sổ chọn phiếu yêu cầu có dữ liệu; nút Duyệt và Duyệt và tiếp tục dùng được.'],
    ['Xem phiếu hàng giữ theo tổng công ty',
     'Xem phiếu hủy của mọi công ty.',
     'Danh sách, màn chi tiết, bản in và tệp Excel đều mở rộng ra toàn bộ công ty.'],
    ['Xem phiếu hàng giữ theo công ty',
     'Xem phiếu hủy thuộc công ty của mình.',
     'Danh sách và màn chi tiết giới hạn trong công ty của bạn.'],
    ['Xem phiếu hàng giữ theo phòng ban',
     'KHÔNG có tác dụng ở màn này. Đây là điểm khác với màn Yêu cầu hủy hàng giữ.',
     'Người chỉ có quyền này xem như không có quyền phạm vi nào.'],
])

b.h3('4.2. Người dùng không có quyền nào ở trên')
b.para('Bạn vẫn vào được màn hình và vẫn thấy nút Tạo mới, nhưng:')
b.bullet('Danh sách chỉ hiện phiếu hủy do chính bạn lập, cộng thêm phiếu hủy sinh ra từ phiếu '
         'yêu cầu do chính bạn lập.')
b.bullet('Bấm Tạo mới thì mở được màn lập phiếu, nhưng cửa sổ chọn phiếu yêu cầu sẽ KHÔNG có '
         'dòng nào, nên bạn không lập được phiếu.')
b.bullet('Bạn mở được bản in và lịch sử của những phiếu bạn nhìn thấy.')

b.h3('4.3. Người dùng có quyền "Quản lý giữ hàng"')
b.para('Đây là vai trò chính của màn hình. Bạn làm được đầy đủ:')
b.bullet('Xem mọi phiếu hủy thuộc công ty của bạn.')
b.bullet('Bấm Tạo mới, chọn một phiếu yêu cầu đang chờ duyệt của công ty bạn và lập phiếu hủy.')
b.bullet('Quyết định số lượng cho hủy ở từng dòng hàng, có thể bỏ bớt dòng không đồng ý.')
b.bullet('In phiếu và xem lịch sử của mọi phiếu bạn nhìn thấy.')

b.h3('4.4. Người dùng chỉ có quyền xem theo cấp')
b.para('Bạn xem được danh sách rộng hơn nhưng KHÔNG lập được phiếu hủy. Cụ thể, cửa sổ chọn '
       'phiếu yêu cầu sẽ rỗng dù công ty đang có phiếu chờ duyệt.')

# =================================================== PHAN 1
b.h1('PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')

b.h2('1. Cách vào màn hình')
b.para('Có hai lối vào, kết quả khác nhau nên bạn cần phân biệt:')
b.bullet('Lối 1 — vào danh sách: chọn menu Tài chính → Giữ hàng → Phiếu hủy hàng giữ. Từ đây '
         'bấm Tạo mới thì màn lập phiếu mở ra với ô phiếu yêu cầu còn trống, bạn tự chọn.',
         bold_prefix='Lối 1')
b.bullet('Lối 2 — vào thẳng từ phiếu yêu cầu: mở màn Yêu cầu hủy hàng giữ, mở chi tiết một phiếu '
         'đang chờ duyệt rồi bấm nút "Tạo phiếu hủy hàng giữ". Màn lập phiếu mở ra với phiếu yêu '
         'cầu đã được điền sẵn. Ở lối này không có nút "Duyệt và tiếp tục".',
         bold_prefix='Lối 2')

b.h2('2. Bố cục màn hình danh sách')
b.para('Màn hình gồm ba khu vực từ trên xuống: khu vực bộ lọc, thanh công cụ với các nút, và '
       'bảng danh sách kèm phân trang ở cuối.')
b.image('phhg-01-danh-sach.png', 'Màn hình Phiếu hủy hàng giữ lúc mới vào')

# =================================================== PHAN 2
b.h1('PHẦN 2: DANH SÁCH PHIẾU')

b.h2('1. Các cột của bảng')
b.table([
    ['Cột', 'Ý nghĩa'],
    ['STT', 'Số thứ tự, chạy liên tục qua các trang.'],
    ['Mã phiếu', 'Mã phiếu hủy, dạng PHHG-NNNNN. Bấm vào để mở màn chi tiết.'],
    ['Phiếu yêu cầu', 'Mã phiếu yêu cầu gốc, dạng PYCHHG-NNNNN. Bấm vào để mở phiếu yêu cầu đó.'],
    ['Người yêu cầu', 'Người đã lập phiếu yêu cầu, tức người đề nghị hủy.'],
    ['Người tạo', 'Người đã lập phiếu hủy, tức người duyệt. Lưu ý đây KHÔNG phải người yêu cầu.'],
    ['Ngày tạo', 'Ngày giờ lập phiếu hủy. Sắp xếp được.'],
    ['Trạng thái', 'Luôn là "Đã đề nghị" màu xanh lá, vì phiếu hủy không có vòng đời.'],
    ['Người cập nhật / Ngày cập nhật',
     'Trùng với Người tạo và Ngày tạo, vì phiếu không sửa được.'],
    ['Khách hàng', 'Khách hàng của phiếu. Mặc định ẩn, bật lên trong cửa sổ chọn cột.'],
    ['Ghi chú', 'Ghi chú của phiếu hủy. Mặc định ẩn.'],
    ['Hành động', 'Chứa hai nút In và Lịch sử. Không có nút Sửa và Xóa.'],
])

b.h2('2. Tìm kiếm và lọc')
b.para('Ô tìm nhanh ở trên cùng tìm đồng thời theo ba thứ: mã phiếu hủy, mã phiếu yêu cầu và tên '
       'người tạo. Bạn phải bấm nút Tìm kiếm thì ô này mới có tác dụng.')
b.para('Bấm "Tìm kiếm nâng cao" để mở thêm bảy ô lọc chi tiết. Khác với ô tìm nhanh, chỉ cần đổi '
       'giá trị một ô lọc nâng cao là danh sách tự nạp lại ngay.')
b.image('phhg-02-bo-loc-nang-cao.png', 'Khu vực Tìm kiếm nâng cao đang mở')
b.table([
    ['Ô lọc', 'Cách dùng'],
    ['Trạng thái', 'Chọn "Đã đề nghị". Hai lựa chọn còn lại luôn cho danh sách rỗng vì phiếu hủy '
                   'chỉ có một trạng thái duy nhất.'],
    ['Mã phiếu yêu cầu', 'Gõ một phần mã phiếu yêu cầu, không cần gõ đủ.'],
    ['Người yêu cầu', 'Lọc theo người lập phiếu yêu cầu gốc.'],
    ['Người tạo', 'Lọc theo người đã lập phiếu hủy.'],
    ['Tên/mã hàng hóa', 'Một ô tìm được cả tên hàng lẫn mã hàng có trong chi tiết phiếu.'],
    ['Ngày tạo từ / Ngày tạo đến', 'Lọc theo ngày lập phiếu HỦY, không phải ngày lập phiếu yêu '
                                   'cầu. Lấy trọn cả hai ngày đầu mút.'],
])
b.para('Nút "Làm mới" xóa sạch mọi ô lọc, xóa cả thứ tự sắp xếp và nạp lại danh sách đầy đủ.')
b.para('Bộ lọc bạn vừa dùng được nhớ trong 10 phút. Mở một phiếu rồi bấm Quay lại thì bộ lọc vẫn '
       'còn nguyên.')

b.h2('3. Chọn ô lọc muốn hiển thị')
b.para('Bấm "Cài đặt bộ lọc" để tự chọn ô lọc nào được hiện và kéo thả để đổi thứ tự. Cấu hình '
       'lưu riêng cho tài khoản của bạn, không ảnh hưởng người khác. Bấm "Khôi phục mặc định" để '
       'quay về đủ bảy ô ban đầu.')
b.image('phhg-03-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc')

b.h2('4. Chọn cột hiển thị của bảng')
b.para('Bấm nút biểu tượng cột ở góc phải thanh công cụ để bật / tắt và sắp xếp cột. Ba cột STT, '
       'Mã phiếu và Hành động bị khóa, luôn hiển thị. Hai cột Khách hàng và Ghi chú mặc định tắt, '
       'bạn có thể bật lên.')
b.image('phhg-04-cau-hinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột hiển thị')

b.h2('5. Các nút trên thanh công cụ')
b.table([
    ['Nút', 'Tác dụng'],
    ['Tạo mới', 'Mở màn lập phiếu hủy hàng giữ.'],
    ['Xuất Excel', 'Mở cửa sổ chọn trường rồi tải danh sách về máy.'],
    ['Biểu tượng cột', 'Mở cửa sổ chọn cột hiển thị của bảng.'],
])

b.h2('6. Các thao tác trên từng dòng')
b.table([
    ['Nút', 'Tác dụng', 'Điều kiện hiện'],
    ['In (biểu tượng máy in)', 'Mở cửa sổ xem trước bản in của phiếu đó.', 'Luôn hiện.'],
    ['Lịch sử (biểu tượng đồng hồ)', 'Mở cửa sổ lịch sử thao tác của phiếu.', 'Luôn hiện.'],
])
b.para('Màn hình này không có nút Sửa và nút Xóa ở bất kỳ dòng nào, kể cả phiếu do chính bạn vừa '
       'lập. Đây là đúng thiết kế chứ không phải thiếu quyền.')

# =================================================== PHAN 3
b.h1('PHẦN 3: LẬP PHIẾU HỦY HÀNG GIỮ')

b.para('Đây là chức năng chính của màn hình, và cũng là thao tác duy nhất ghi dữ liệu. Bấm nút '
       'Tạo mới ở màn danh sách để bắt đầu.')
b.image('phhg-09-tao-moi-chua-chon.png', 'Màn lập phiếu khi chưa chọn phiếu yêu cầu')
b.para('Lúc này ba ô Người yêu cầu, Phòng ban yêu cầu và Khách hàng đều trống kèm dòng chữ mờ '
       '"Tự điền theo phiếu yêu cầu", khối Chi tiết ghi "Chưa chọn phiếu yêu cầu", và nút Duyệt '
       'chưa xuất hiện. Bạn phải chọn phiếu yêu cầu trước.')

b.h2('1. Bước 1 — Chọn phiếu yêu cầu cần duyệt')
b.para('Bấm nút biểu tượng kính lúp bên phải ô "Phiếu yêu cầu hủy hàng giữ". Cửa sổ "Phiếu chờ '
       'duyệt" mở ra.')
b.image('phhg-10-popup-chon-phieu-yeu-cau.png', 'Cửa sổ chọn phiếu yêu cầu đang chờ duyệt')
b.para('Cửa sổ chỉ liệt kê những phiếu yêu cầu thỏa mãn đồng thời hai điều kiện: đang ở trạng '
       'thái Chờ duyệt, và thuộc công ty của bạn. Phiếu của công ty khác không hiện ở đây, kể cả '
       'khi bạn có quyền xem toàn tổng công ty.')
b.table([
    ['Cột', 'Ý nghĩa'],
    ['STT', 'Số thứ tự trong cửa sổ.'],
    ['Mã phiếu', 'Mã phiếu yêu cầu, dạng PYCHHG-NNNNN.'],
    ['Người tạo', 'Người đã lập phiếu yêu cầu.'],
    ['Khách hàng', 'Khách hàng đang được giữ hàng.'],
    ['Ngày tạo', 'Ngày lập phiếu yêu cầu.'],
])
b.para('Bạn có thể lọc nhanh bằng ô "Mã phiếu" hoặc ô "Người tạo" ở phía trên. Để chọn, bấm vào '
       'bất kỳ vị trí nào trên dòng — không cần bấm đúng vào mã phiếu.')
b.para('Nếu cửa sổ trống trong khi bạn biết công ty đang có phiếu chờ duyệt, nguyên nhân gần như '
       'chắc chắn là tài khoản của bạn chưa được cấp quyền "Quản lý giữ hàng".')

b.h2('2. Bước 2 — Kiểm tra thông tin phần mềm điền sẵn')
b.image('phhg-11-tao-moi-da-chon.png', 'Màn lập phiếu sau khi đã chọn phiếu yêu cầu')
b.table([
    ['Ô', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Phiếu yêu cầu hủy hàng giữ', 'Có', 'Mã phiếu bạn vừa chọn',
     'Không gõ tay được, chỉ chọn qua cửa sổ tra cứu.'],
    ['Người yêu cầu', 'Không', 'Tên người lập phiếu yêu cầu',
     'Ô khóa, lấy tự động từ phiếu yêu cầu.'],
    ['Phòng ban yêu cầu', 'Không', 'Phòng ban của người lập phiếu yêu cầu', 'Ô khóa.'],
    ['Khách hàng', 'Không', 'Mã và tên khách hàng của phiếu yêu cầu', 'Ô khóa.'],
    ['Ghi chú', 'Không', 'Trống',
     'Ghi chú riêng của phiếu hủy, tối đa 255 ký tự. Không lấy từ phiếu yêu cầu.'],
])
b.para('Góc phải khối Thông tin chung hiển thị "Người tạo: {tên của bạn} · {ngày giờ hiện tại}".')
b.para('Màn lập phiếu KHÔNG có ô Mã phiếu và ô Kho. Mã phiếu do phần mềm sinh tự động sau khi '
       'lưu; ô Kho chỉ xuất hiện ở màn xem chi tiết.')

b.h2('3. Bước 3 — Quyết định số lượng cho hủy')
b.para('Bảng Chi tiết đã nạp sẵn những dòng hàng mà người lập phiếu yêu cầu đã tích "Cần hủy". '
       'Mỗi dòng có ba số lượng, bạn cần đọc đúng ý nghĩa của từng số:')
b.table([
    ['Cột', 'Ý nghĩa', 'Sửa được không'],
    ['Cần hủy', 'Ô tích để chọn dòng này có được duyệt hay không. Mặc định đã tích sẵn.',
     'Có. Bỏ tích thì dòng bị làm mờ và không được duyệt.'],
    ['Có thể hủy', 'Số hàng giữ còn lại thực tế, tính LẠI tại thời điểm bạn mở phiếu. Đây là '
                   'TRẦN của ô Duyệt hủy.',
     'Không.'],
    ['Yêu cầu hủy', 'Số người lập phiếu yêu cầu đề nghị. Chỉ để tham khảo.', 'Không.'],
    ['Duyệt hủy', 'Số bạn thực sự cho hủy. Đây là số bị trừ khỏi hàng giữ.',
     'Có. Phần mềm điền sẵn bằng đúng số Yêu cầu hủy.'],
    ['ĐVT', 'Đơn vị tính, luôn là đơn vị cơ bản của hàng hóa.', 'Không.'],
])
b.para('Hai điều dễ hiểu nhầm nhất ở bước này:')
b.bullet('Số Duyệt hủy KHÔNG bị chặn bởi số Yêu cầu hủy. Bạn được phép duyệt NHIỀU HƠN số nhân '
         'viên đề nghị, miễn là không vượt cột Có thể hủy. Ví dụ nhân viên đề nghị 3 mà hàng giữ '
         'còn 4 thì bạn duyệt 4 vẫn hợp lệ.')
b.bullet('Cột Có thể hủy có thể khác số trên phiếu yêu cầu, vì hàng giữ biến động liên tục do '
         'các chứng từ khác. Phần mềm luôn lấy số mới nhất tại lúc bạn mở phiếu.')
b.para('Nếu bạn không đồng ý hủy một mặt hàng nào đó, hãy bỏ tích ô "Cần hủy" của dòng đó thay vì '
       'nhập số 0. Dòng bị bỏ tích sẽ mờ đi, ô Duyệt hủy bị khóa và dòng đó không được đưa vào '
       'phiếu.')

b.h2('4. Bước 4 — Bấm Duyệt và xác nhận')
b.para('Bấm nút Duyệt ở cuối màn. Trước khi lưu, phần mềm kiểm tra lại toàn bộ các dòng đang '
       'tích. Nếu còn ô sai, phần mềm báo "Bạn chưa nhập đầy đủ thông tin.", tự cuộn màn hình tới '
       'dòng lỗi đầu tiên và KHÔNG lưu gì cả.')
b.para('Nếu mọi thứ hợp lệ, hộp thoại xác nhận hiện ra:')
b.image('phhg-12-xac-nhan-duyet.png', 'Hộp thoại xác nhận trước khi lưu phiếu hủy')
b.para('Hãy đọc kỹ nội dung hộp thoại: thao tác này TRỪ HÀNG GIỮ ngay lập tức và không thể hoàn '
       'tác. Bấm "Hủy" nếu bạn muốn xem lại — mọi dữ liệu đang nhập vẫn còn nguyên và chưa có gì '
       'được ghi. Bấm "Duyệt" để hoàn tất.')
b.para('Sau khi lưu thành công, phần mềm báo "Duyệt phiếu thành công" và đưa bạn về màn danh '
       'sách, nơi phiếu vừa lập nằm ở dòng đầu tiên.')

b.h2('5. Ba nút ở cuối màn lập phiếu')
b.table([
    ['Nút', 'Tác dụng', 'Điều kiện hiện'],
    ['Duyệt', 'Lưu phiếu hủy, trừ hàng giữ, duyệt phiếu yêu cầu rồi quay về màn danh sách.',
     'Chỉ hiện sau khi đã chọn phiếu yêu cầu.'],
    ['Duyệt và tiếp tục',
     'Làm y hệt nút Duyệt nhưng lưu xong thì Ở LẠI màn lập phiếu để bạn chọn phiếu yêu cầu kế '
     'tiếp. Tiện khi cần duyệt nhiều phiếu liên tiếp.',
     'Chỉ hiện khi bạn vào màn bằng nút Tạo mới và đã chọn phiếu yêu cầu.'],
    ['Quay lại', 'Về màn danh sách.', 'Luôn hiện.'],
])
b.para('Nút "Duyệt và tiếp tục" chạy đúng luồng duyệt chứ không phải lưu nháp. Hàng giữ bị trừ '
       'ngay khi bạn xác nhận, giống hệt nút Duyệt. Phiếu hủy hàng giữ không có trạng thái nháp.')

b.h2('6. Điều gì xảy ra sau khi bạn lưu')
b.para('Trong cùng một lần lưu, phần mềm thực hiện đầy đủ các việc sau. Nếu bất kỳ bước nào hỏng '
       'thì toàn bộ bị hủy bỏ, không để lại dữ liệu dở dang:')
b.bullet('Tạo phiếu hủy và sinh mã dạng PHHG-NNNNN.')
b.bullet('Trừ hàng giữ theo thứ tự hạn giữ SỚM TRƯỚC, muộn sau. Trừ hết lô này mới sang lô kế '
         'tiếp.')
b.bullet('Hàng giữ được trừ của NGƯỜI LẬP PHIẾU YÊU CẦU, không phải của bạn.')
b.bullet('Chuyển phiếu yêu cầu sang trạng thái Đã duyệt, ghi tên bạn và thời điểm duyệt.')
b.bullet('Ghi một mốc lịch sử cho phiếu hủy và một mốc cho phiếu yêu cầu.')
b.bullet('Gửi thông báo cho người lập phiếu yêu cầu biết phiếu của họ đã được duyệt.')

b.h2('7. Các lỗi thường gặp khi lưu')
b.table([
    ['Tình huống', 'Phần mềm báo gì', 'Cách xử lý'],
    ['Ô Duyệt hủy để trống', 'Chưa nhập số lượng', 'Nhập số, hoặc bỏ tích ô Cần hủy của dòng đó.'],
    ['Nhập chữ vào ô Duyệt hủy', 'Chỉ được nhập số', 'Xóa và nhập lại bằng số.'],
    ['Nhập 0 hoặc số âm', 'Phải lớn hơn 0',
     'Nhập số dương, hoặc bỏ tích ô Cần hủy nếu không muốn duyệt dòng đó.'],
    ['Nhập vượt cột Có thể hủy', 'Không được vượt {số có thể hủy}',
     'Giảm số xuống. Phần mềm giữ nguyên số bạn vừa gõ chứ không tự kéo về trần.'],
    ['Bỏ tích hết mọi dòng', 'Phải chọn ít nhất 1 hàng hoá cần hủy với số lượng lớn hơn 0',
     'Tích lại ít nhất một dòng.'],
    ['Ghi chú quá dài', 'Không được vượt quá 255 ký tự', 'Rút gọn ghi chú.'],
    ['Người khác vừa duyệt mất phiếu yêu cầu',
     'Phiếu yêu cầu này không còn ở trạng thái chờ duyệt hoặc bạn không đủ quyền duyệt',
     'Quay về danh sách, phiếu đã được người khác xử lý. Không có gì bị ghi sai.'],
    ['Hàng giữ vừa bị chứng từ khác lấy hết', 'Hàng "{tên hàng}" không đủ số lượng đang giữ',
     'Mở lại phiếu để lấy số Có thể hủy mới nhất rồi nhập lại. Không có dòng nào bị trừ một phần.'],
])

b.h2('8. Nếu bạn rời màn khi chưa lưu')
b.para('Phần mềm sẽ cảnh báo dữ liệu chưa được lưu và hỏi bạn có chắc muốn rời đi không. Chọn ở '
       'lại thì mọi thứ bạn đang nhập vẫn còn nguyên.')

# =================================================== PHAN 4
b.h1('PHẦN 4: XEM CHI TIẾT PHIẾU')

b.para('Bấm vào mã phiếu ở màn danh sách để mở màn chi tiết. Toàn bộ màn này chỉ để đọc, không ô '
       'nào sửa được.')
b.image('phhg-06-chi-tiet.png', 'Màn Chi tiết phiếu hủy hàng giữ')
b.table([
    ['Ô', 'Nội dung'],
    ['Mã phiếu', 'Mã phiếu hủy do phần mềm sinh. Chỉ có ở màn này.'],
    ['Phiếu yêu cầu hủy hàng giữ', 'Mã phiếu yêu cầu gốc.'],
    ['Người yêu cầu', 'Người đã lập phiếu yêu cầu.'],
    ['Phòng ban yêu cầu', 'Phòng ban của người lập phiếu yêu cầu.'],
    ['Khách hàng', 'Khách hàng đang được giữ hàng.'],
    ['Kho', 'Thường để TRỐNG. Đây là bình thường, không phải lỗi: hàng giữ được tính theo nhân '
            'viên và khách hàng chứ không gắn với kho nào. Chỉ có ở màn này.'],
    ['Ghi chú', 'Ghi chú bạn đã nhập lúc lập phiếu.'],
])
b.para('Bảng Chi tiết ở màn xem gọn hơn màn lập phiếu: chỉ còn STT, Tên hàng hóa, Model, Mã hàng '
       'hóa, Thương hiệu, Yêu cầu hủy, Duyệt hủy và ĐVT. Hai cột "Cần hủy" và "Có thể hủy" không '
       'còn, vì chúng chỉ phục vụ lúc nhập liệu.')
b.para('Cuối màn chỉ có hai nút: In và Quay lại. Không có nút Sửa, Xóa hay Hủy duyệt.')

# =================================================== PHAN 5
b.h1('PHẦN 5: IN PHIẾU')

b.para('Bạn in được từ hai chỗ: nút In ở cột Hành động ngoài danh sách, hoặc nút In ở cuối màn '
       'chi tiết. Cả hai đều mở một cửa sổ xem trước ngay trên màn, không mở thẻ mới của trình '
       'duyệt.')
b.image('phhg-08-in-phieu.png', 'Cửa sổ xem trước bản in phiếu hủy hàng giữ')
b.para('Bản in gồm tiêu đề công ty, tên phiếu, số phiếu, ngày tạo, mã phiếu yêu cầu, người yêu '
       'cầu, phòng ban, khách hàng, kho, người tạo, bảng hàng hóa và ghi chú.')
b.para('Tiêu đề công ty ở đầu bản in lấy theo công ty ghi trên phiếu, không phải công ty của '
       'người đang đăng nhập. Nên khi bạn in hộ phiếu của công ty khác, tiêu đề vẫn đúng công ty '
       'của phiếu đó.')
b.para('Bấm nút In trong cửa sổ để gửi lệnh in, hoặc bấm nút đóng để thoát.')

# =================================================== PHAN 6
b.h1('PHẦN 6: XEM LỊCH SỬ THAY ĐỔI')

b.para('Có hai cách xem: bấm nút Lịch sử ở cột Hành động ngoài danh sách, hoặc bấm "Xem lịch sử" '
       'ở khối Lịch sử thay đổi cuối màn chi tiết.')
b.image('phhg-07-lich-su.png', 'Khối Lịch sử thay đổi ở màn chi tiết')
b.para('Khối lịch sử chỉ nạp dữ liệu khi bạn bấm mở, nên lần đầu vào màn sẽ thấy nó đang thu gọn. '
       'Bấm "Thu gọn" để đóng lại, bấm "Làm mới" để nạp lại danh sách mốc.')
b.para('Mỗi mốc hiển thị thời điểm, tên thao tác, người thực hiện kèm phòng ban, và phần ghi chú. '
       'Phiếu hủy chỉ có duy nhất một loại mốc là "Tạo mới", vì phiếu không sửa và không xóa '
       'được. Ghi chú của mốc cho biết đã trừ hàng giữ trên bao nhiêu lô, ví dụ "Đã trừ tồn hàng '
       'giữ trên 1 lô.".')
b.para('Muốn xem phía phiếu yêu cầu, hãy mở phiếu yêu cầu gốc và xem lịch sử của nó — ở đó có mốc '
       'duyệt ghi rõ mã phiếu hủy đã sinh ra.')

# =================================================== PHAN 7
b.h1('PHẦN 7: XUẤT EXCEL DANH SÁCH')

b.para('Bấm nút "Xuất Excel" trên thanh công cụ. Cửa sổ chọn trường mở ra, và phần mềm tự tích '
       'sẵn đúng những trường tương ứng với các cột đang hiển thị trên bảng. Bạn tích thêm hoặc '
       'bỏ bớt tùy nhu cầu.')
b.image('phhg-05-chon-truong-xuat-excel.png', 'Cửa sổ Chọn trường xuất Excel')
b.para('Có mười trường để chọn: Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người tạo, Ngày tạo, '
       'Trạng thái, Người cập nhật, Ngày cập nhật, Khách hàng và Ghi chú.')
b.para('Thứ tự cột trong tệp theo đúng thứ tự bạn tích chọn, nên nếu muốn sắp xếp lại, hãy bấm '
       '"Bỏ chọn hết" rồi tích theo thứ tự mong muốn.')
b.para('Tệp xuất ra chứa toàn bộ phiếu khớp bộ lọc bạn đang áp dụng, và luôn giới hạn trong phạm '
       'vi dữ liệu mà bạn được xem. Trong lúc đang xuất, nút bị khóa để tránh bấm hai lần.')

# =================================================== PHAN 8
b.h1('PHẦN 8: NHỮNG ĐIỀU CẦN NHỚ')

b.bullet('Lập phiếu hủy CHÍNH LÀ duyệt phiếu yêu cầu. Không có nút Duyệt riêng ở đâu khác.')
b.bullet('Hàng giữ chỉ bị trừ tại đúng thời điểm bạn lưu phiếu hủy, không sớm hơn và không muộn '
         'hơn.')
b.bullet('Thao tác này KHÔNG hoàn tác được. Phiếu lập xong không sửa, không xóa, không hủy duyệt.')
b.bullet('Trần chặn số lượng là cột "Có thể hủy", KHÔNG phải cột "Yêu cầu hủy". Duyệt nhiều hơn '
         'số nhân viên đề nghị là hợp lệ.')
b.bullet('Hàng giữ được trừ của người lập phiếu yêu cầu, không phải của bạn.')
b.bullet('Nếu một dòng không đủ hàng giữ thì cả phiếu bị hủy bỏ, không có chuyện trừ được dòng '
         'nào hay dòng đó.')
b.bullet('Ô "Kho" ở màn chi tiết để trống là bình thường, không phải lỗi dữ liệu.')
b.bullet('Cửa sổ chọn phiếu yêu cầu rỗng thì gần như chắc chắn tài khoản của bạn thiếu quyền '
         '"Quản lý giữ hàng", hoặc công ty bạn hết phiếu chờ duyệt.')
b.bullet('Muốn từ chối một đề nghị hủy, hãy dùng nút "Không duyệt" ở màn Yêu cầu hủy hàng giữ — '
         'màn này không có chức năng từ chối.')

b.finish()
