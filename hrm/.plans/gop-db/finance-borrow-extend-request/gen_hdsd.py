# -*- coding: utf-8 -*-
"""Sinh HDSD man "Phieu yeu cau gia han hang muon" (ma phieu PGHHM) tu khung HDSD_MAU.docx.

Khuon: ../finance-prepick-extend-request/gen_hdsd.py (man sinh doi gia han hang GIU).
Noi dung viet tu code nhanh `develop` (05/10/2026) — xem docstring gen_srs.py cung thu muc.
Anh chup that: ./borrow_extend_shots (1440x900, dev 05/10/2026, tai khoan DNS Admin).
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

SHOTS = os.path.join(BASE, 'borrow_extend_shots')
OUT = os.path.join(BASE, 'HDSD_Phieu yeu cau gia han hang muon.docx')

b = HdsdBuilder(output=OUT, shots_dir=SHOTS,
                cover_title='(Màn hình: Phiếu yêu cầu gia hạn hàng mượn)',
                doc_title='HDSD - Phiếu yêu cầu gia hạn hàng mượn')

DUONG_TC = ('Vào phân hệ Tài chính → nhóm Hàng hoá - Dịch vụ - Vận chuyển → Mượn hàng → bấm '
            'Phiếu yêu cầu gia hạn hàng mượn.')

# =============================================================== TONG QUAN
b.h1('TỔNG QUAN')

b.h2('1. Thuật ngữ sử dụng trong tài liệu')
b.table([
    ['Thuật ngữ', 'Ý nghĩa'],
    ['Phiếu mượn', 'Phiếu yêu cầu xuất hàng mượn (mã PYCXH-xxxxx) đã được xuất kho, ghi nhận bạn '
                   'đang mượn hàng của công ty và có một ngày hẹn trả.'],
    ['Phiếu gia hạn', 'Phiếu yêu cầu gia hạn hàng mượn (mã PGHHM-xxxxx) — xin dời ngày hẹn trả '
                      'của đúng một phiếu mượn.'],
    ['Ngày hẹn trả', 'Ngày bạn phải trả hàng theo phiếu mượn hiện tại.'],
    ['Ngày hẹn trả mới', 'Ngày bạn xin dời hạn trả tới.'],
    ['Số ngày mượn tối đa', 'Cấu hình chung của phần mềm. Ngày hẹn trả mới không được vượt quá '
                            'ngày hôm nay cộng số ngày này (gọi là ngày tối đa).'],
    ['Hạn mức giá trị hàng mượn', 'Cấu hình của từng công ty. Phiếu mượn còn nợ nhiều hơn hạn mức '
                                  'này thì phiếu gia hạn phải trình thêm Ban giám đốc.'],
    ['Giá trị hàng còn nợ', 'Cộng trên mọi mặt hàng của phiếu mượn: (số lượng đã xuất trừ số '
                            'lượng đã trả) nhân đơn giá.'],
    ['TP / BGĐ / KT', 'Trưởng phòng / Ban giám đốc / Kế toán kho — các cấp duyệt của phiếu.'],
    ['Không duyệt', 'Trạng thái của phiếu bị từ chối. Phiếu dừng hẳn, không sửa, không gửi lại.'],
])

b.h2('2. Cập nhật tài liệu')
b.table([
    ['Phiên bản', 'Ngày', 'Nội dung'],
    ['1.0', '05/10/2026', 'Ban hành lần đầu cho màn hình Phiếu yêu cầu gia hạn hàng mượn trên '
                          'phân hệ Tài chính.'],
])

b.h2('3. Giới thiệu chung')
b.para('Màn hình Phiếu yêu cầu gia hạn hàng mượn dùng để xin dời ngày hẹn trả hàng mượn. Khi '
       'bạn đang mượn hàng của công ty mà chưa trả kịp hạn, bạn lập phiếu gia hạn cho phiếu mượn '
       'đó để xin thêm thời gian.')
b.para('Phiếu đi qua các cấp duyệt: Trưởng phòng → Ban giám đốc (chỉ khi phiếu mượn còn nợ nhiều '
       'hơn hạn mức của công ty) → Kế toán kho. Ngày hẹn trả của phiếu mượn chỉ thực sự đổi khi '
       'Kế toán kho duyệt ở bước cuối. Màn hình này không làm thay đổi tồn kho.')
b.para('Phiếu KHÔNG có bản nháp: bấm gửi là phiếu đi duyệt ngay. Màn hình cũng KHÔNG có chức '
       'năng Sửa hay Xóa phiếu.', bold_prefix='Lưu ý: ')
b.para('Đường dẫn: ' + DUONG_TC + ' Có thể gõ thẳng địa chỉ '
       '/finance/borrow-extend-requests trên thanh địa chỉ trình duyệt.')
b.para('Mã phiếu do phần mềm tự sinh theo dạng PGHHM kèm 5 chữ số, ví dụ PGHHM-02942.')

b.h2('4. Quyền sử dụng và phạm vi dữ liệu')
b.para('Lập phiếu không cần quyền riêng: ai đăng nhập cũng lập được phiếu gia hạn cho phiếu mượn '
       'của chính mình. Các quyền dưới đây quyết định bạn DUYỆT được ở cấp nào và NHÌN THẤY phiếu '
       'của những ai.', bold_prefix='Lưu ý: ')

b.h3('4.1. Bảng quyền của màn hình')
b.table([
    ['Tên quyền', 'Cho phép làm gì', 'Nút / phần tương ứng', 'Ghi chú'],
    ['Trưởng phòng duyệt hàng mượn',
     'Duyệt hoặc từ chối phiếu ở bước Chờ TP duyệt.',
     'Nút TP duyệt, Từ chối ở màn chi tiết; biểu tượng Duyệt, Từ chối ở cột Hành động.',
     'Phải cùng công ty với phiếu và quản lý phòng ban ghi trên phiếu (được phân công quản lý, '
     'được tích Quản lý tất cả phòng ban, hoặc chính bạn thuộc phòng ban đó).'],
    ['Ban giám đốc duyệt hàng mượn',
     'Duyệt hoặc từ chối phiếu ở bước Chờ BGĐ duyệt.',
     'Nút BGĐ duyệt, Từ chối.', 'Phải cùng công ty với phiếu.'],
    ['Kế toán kho',
     'Duyệt hoặc từ chối phiếu ở bước Chờ KT duyệt; được sửa Ngày hẹn trả mới trước khi duyệt.',
     'Nút KT duyệt, Từ chối; ô Ngày hẹn trả mới mở khóa; mục menu Hàng mượn chờ duyệt.',
     'Phải cùng công ty với phiếu. Đây là bước làm ngày hẹn trả của phiếu mượn thực sự đổi.'],
    ['Xem phiếu hàng mượn theo tổng công ty', 'Xem phiếu của mọi công ty.',
     'Danh sách; ô lọc Công ty và Phòng ban.', 'Phạm vi rộng nhất.'],
    ['Xem phiếu hàng mượn theo công ty', 'Xem phiếu thuộc công ty của mình.',
     'Danh sách; ô lọc Phòng ban.', '—'],
    ['Xem phiếu hàng mượn theo phòng ban',
     'Xem phiếu thuộc các phòng ban mình quản lý và phòng ban của chính mình.',
     'Danh sách; ô lọc Phòng ban.', '—'],
])

b.h3('4.2. Người dùng không có quyền nào ở trên')
b.para('Bạn vẫn vào được màn hình và lập được phiếu gia hạn cho phiếu mượn của mình. Danh sách chỉ '
       'hiện phiếu do bạn lập. Không có nút duyệt, từ chối.')

b.h3('4.3. Người dùng có quyền "Trưởng phòng duyệt hàng mượn"')
b.para('Khi nhân viên phòng bạn quản lý gửi phiếu, bạn nhận thông báo "[PGHHM] Chờ duyệt: <mã '
       'phiếu>." ở chuông thông báo. Bấm vào thông báo để mở phiếu, rồi bấm TP duyệt hoặc Từ chối.')
b.para('Nếu bạn không có quyền xem theo cấp, danh sách thường chỉ có phiếu bạn lập và phiếu bạn đã '
       'duyệt / từ chối — phiếu đang chờ bạn duyệt có thể KHÔNG nằm trong danh sách. Hãy mở phiếu '
       'từ thông báo.', bold_prefix='Quan trọng: ')
b.para('Nếu bạn không quản lý phòng ban của phiếu, nút duyệt sẽ không hiển thị; trường hợp gọi '
       'thao tác trực tiếp, phần mềm báo "Bạn không có quyền duyệt bước này."')

b.h3('4.4. Người dùng có quyền "Ban giám đốc duyệt hàng mượn"')
b.para('Bạn duyệt các phiếu Chờ BGĐ duyệt của công ty mình và nhận thông báo khi có phiếu chuyển '
       'đến. Không phải phiếu nào cũng qua bước này — chỉ phiếu mà phiếu mượn còn nợ nhiều hơn hạn '
       'mức giá trị hàng mượn của công ty.')

b.h3('4.5. Người dùng có quyền "Kế toán kho"')
b.para('Bạn duyệt bước cuối. Bạn có thêm mục menu Tài chính → Chờ duyệt → Hàng mượn chờ duyệt → '
       'Phiếu yêu cầu gia hạn hàng mượn chờ duyệt, liệt kê đúng những phiếu đang chờ bạn duyệt.')
b.para('Trước khi bấm KT duyệt, bạn được sửa lại Ngày hẹn trả mới. Ngay khi bạn duyệt, ngày hẹn '
       'trả của phiếu mượn đổi sang ngày mới — hãy kiểm tra kỹ.')

b.h3('4.6. Người dùng có quyền xem theo cấp')
b.para('Ba quyền "Xem phiếu hàng mượn theo tổng công ty / theo công ty / theo phòng ban" chỉ mở '
       'rộng phạm vi NHÌN, không cho duyệt. Nếu có nhiều quyền, phần mềm áp quyền rộng nhất. Dù có '
       'quyền nào, bạn luôn thấy phiếu do mình lập và phiếu mình đã duyệt / từ chối.')

# =============================================================== PHAN 1
b.h1('PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH')

b.h2('1. Vào màn này bằng cách nào')
b.para('Màn hình có ba lối vào. Hai lối đầu cho cùng một danh sách, lối thứ ba chỉ dành cho người '
       'duyệt cấp Kế toán kho:')
b.table([
    ['Vào từ', 'Bấm theo đường', 'Danh sách hiện ra'],
    ['Tài chính', 'Tài chính → Hàng hoá - Dịch vụ - Vận chuyển → Mượn hàng → Phiếu yêu cầu gia '
                  'hạn hàng mượn',
     'Mọi phiếu trong phạm vi quyền của bạn.'],
    ['Bán hàng', 'Bán hàng → Yêu cầu → Hàng hóa → YC gia hạn hàng mượn',
     'Giống hệt lối vào Tài chính.'],
    ['Tài chính (chờ duyệt)', 'Tài chính → Chờ duyệt → Hàng mượn chờ duyệt → Phiếu yêu cầu gia '
                              'hạn hàng mượn chờ duyệt',
     'Chỉ phiếu đang chờ chính bạn duyệt. Mục này chỉ hiện với người có quyền Kế toán kho.'],
])
b.para('Nếu mở màn mà danh sách trống hoặc ít hơn mong đợi, hãy kiểm tra bạn đang vào từ menu nào '
       '— lối vào chờ duyệt chỉ hiện phiếu đến lượt bạn duyệt.', bold_prefix='Lưu ý: ')

b.h2('2. Bố cục màn hình danh sách')
b.image('01-danh-sach.png', 'Màn hình Phiếu yêu cầu gia hạn hàng mượn lúc mới vào')
b.para('Màn hình chia làm hai khối:')
b.bullet('Khối Bộ lọc danh sách ở trên: ô tìm nhanh, nút Tìm kiếm, nút Làm mới, nút Cài đặt bộ '
         'lọc và nút Tìm kiếm nâng cao.')
b.bullet('Khối bảng danh sách ở dưới: thanh công cụ (Tạo mới, In, Xuất Excel, Tuỳ chỉnh cột), bảng '
         'dữ liệu và thanh phân trang (mặc định 10 dòng mỗi trang, dòng "Hiển thị 1–10 / tổng số").')

# =============================================================== PHAN 2
b.h1('PHẦN 2: DANH SÁCH PHIẾU')

b.h2('1. Vào màn này bằng cách nào')
b.para(DUONG_TC + ' Màn danh sách hiện ra ngay.')

b.h2('2. Các cột của bảng')
b.table([
    ['Cột', 'Nội dung'],
    ['STT', 'Số thứ tự dòng, chạy liên tục theo trang.'],
    ['Mã phiếu', 'Mã phiếu gia hạn. Bấm vào để mở màn chi tiết.'],
    ['Phiếu mượn', 'Mã phiếu mượn được gia hạn. Bấm vào để mở phiếu mượn ở một tab mới.'],
    ['Người tạo', 'Người lập phiếu, kèm mã phòng ban, ví dụ "Nguyễn Văn Thắng - HN_KDTM".'],
    ['Ngày tạo', 'Ngày giờ lập phiếu.'],
    ['Ngày hẹn trả cũ', 'Hạn trả của phiếu mượn lúc lập phiếu gia hạn.'],
    ['Ngày hẹn trả mới', 'Ngày xin dời hạn tới.'],
    ['Trạng thái', 'Chờ TP duyệt · Chờ BGĐ duyệt · Chờ KT duyệt (màu cam) · Đã duyệt (xanh lá) · '
                   'Không duyệt (đỏ).'],
    ['Người duyệt / Ngày duyệt', 'Người đóng dấu sau cùng và thời điểm đó — kể cả khi người đó từ '
                                 'chối. Để trống khi chưa ai duyệt.'],
    ['Phòng ban, Ghi chú, Lý do từ chối', 'Ẩn sẵn, bật lên trong Tuỳ chỉnh cột.'],
    ['Hành động', 'Các nút thao tác của từng dòng.'],
])
b.para('Năm cột có mũi tên sắp xếp: Mã phiếu, Ngày tạo, Ngày hẹn trả cũ, Ngày hẹn trả mới, Ngày '
       'duyệt. Bấm tiêu đề cột để đổi tăng dần / giảm dần. Mặc định phiếu mới nhất ở đầu.')

b.h2('3. Tìm kiếm và lọc')
b.para('Ô tìm nhanh tìm theo mã phiếu hoặc tên người tạo. Gõ xong bấm Tìm kiếm hoặc nhấn Enter — '
       'phần mềm không tự tìm khi bạn đang gõ.')
b.para('Bấm Tìm kiếm nâng cao để mở bảng lọc chi tiết (bấm lần nữa để ẩn).')
b.image('02-bo-loc-nang-cao.png', 'Bảng lọc nâng cao đang mở')
b.table([
    ['Tiêu chí lọc', 'Cách dùng'],
    ['Công ty', 'Chỉ hiện với người xem theo tổng công ty. Biểu tượng ổ khóa cạnh chữ dùng để hiện '
                'thêm cả công ty đã khóa trong danh sách chọn.'],
    ['Phòng ban', 'Hiện với người có quyền xem theo cấp. Lọc theo phòng ban ghi trên phiếu.'],
    ['Mã phiếu', 'Gõ một phần hoặc toàn bộ mã phiếu gia hạn.'],
    ['Phiếu mượn', 'Gõ một phần hoặc toàn bộ mã phiếu mượn.'],
    ['Trạng thái', 'Chọn một trong năm trạng thái.'],
    ['Người tạo', 'Chọn người đã lập phiếu.'],
    ['Người duyệt', 'Chọn người đã duyệt hoặc từ chối ở BẤT KỲ cấp nào (nên kết quả có thể gồm '
                    'phiếu mà cột Người duyệt đang hiện người khác).'],
    ['Tên hàng hóa / Model', 'Tìm phiếu có phiếu mượn chứa mặt hàng khớp.'],
    ['Ngày tạo', 'Chọn khoảng từ ngày → đến ngày lập phiếu (lấy trọn hai đầu).'],
])
b.para('Các ô lọc nâng cao tự lọc lại ngay khi bạn chọn. Bấm Làm mới để xóa toàn bộ điều kiện.')
b.para('Phần mềm ghi nhớ điều kiện lọc trong 10 phút; mở phiếu rồi quay lại vẫn giữ bộ lọc cũ.',
       bold_prefix='Mẹo: ')

b.h2('4. Chọn ô lọc muốn hiển thị')
b.para('Bấm Cài đặt bộ lọc để chọn những ô lọc bạn hay dùng và kéo sắp xếp lại thứ tự. Cấu hình '
       'lưu riêng cho tài khoản của bạn.')
b.image('03-cai-dat-bo-loc.png', 'Cửa sổ Cài đặt bộ lọc')
b.bullet('Bỏ tích ô lọc không dùng để ẩn khỏi bảng lọc nâng cao.')
b.bullet('Kéo biểu tượng sáu chấm để đổi vị trí.')
b.bullet('Bấm Lưu để ghi lại, Khôi phục mặc định để trả về ban đầu, Đóng để thoát không lưu.')

b.h2('5. Chọn cột hiển thị của bảng')
b.para('Bấm biểu tượng cột ở góc phải thanh công cụ để mở cửa sổ Tuỳ chỉnh cột.')
b.image('04-cau-hinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột')
b.para('STT, Mã phiếu và Hành động có biểu tượng ổ khóa: luôn hiển thị. Phòng ban, Ghi chú và Lý '
       'do từ chối mặc định tắt. Tích / bỏ tích, kéo đổi thứ tự rồi bấm Lưu.')

b.h2('6. Các nút trên thanh công cụ')
b.table([
    ['Nút', 'Tác dụng', 'Điều kiện hiển thị'],
    ['Tạo mới', 'Mở màn lập phiếu gia hạn.', 'Luôn hiển thị.'],
    ['In', 'Mở bản xem trước in danh sách theo điều kiện lọc đang áp.', 'Luôn hiển thị.'],
    ['Xuất Excel', 'Mở cửa sổ chọn trường rồi tải file Excel về máy.', 'Luôn hiển thị.'],
    ['Tuỳ chỉnh cột', 'Mở cửa sổ Tuỳ chỉnh cột.', 'Luôn hiển thị.'],
])

b.h2('7. Các thao tác trên từng dòng')
b.table([
    ['Thao tác', 'Tác dụng', 'Khi nào hiện'],
    ['Duyệt (biểu tượng dấu tích)', 'Mở màn chi tiết để xem lại rồi bấm duyệt.',
     'Phiếu đang chờ chính bạn duyệt ở đúng cấp.'],
    ['Từ chối (biểu tượng dấu nhân)', 'Mở cửa sổ nhập lý do từ chối.',
     'Phiếu đang chờ chính bạn duyệt ở đúng cấp.'],
    ['In (biểu tượng máy in)', 'Mở bản xem trước in phiếu.', 'Luôn hiện.'],
    ['Lịch sử (biểu tượng đồng hồ)', 'Mở cửa sổ lịch sử thay đổi của phiếu.', 'Luôn hiện.'],
])
b.para('Khi dòng có nhiều nút, các nút sau được gom vào biểu tượng ba chấm "Hành động khác". Màn '
       'hình không có nút Sửa và Xóa — đây là đúng thiết kế.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 3
b.h1('PHẦN 3: LẬP PHIẾU YÊU CẦU GIA HẠN')

b.h2('1. Vào màn này bằng cách nào')
b.para(DUONG_TC + ' Ở màn danh sách, bấm nút Tạo mới. Phần mềm mở màn "Thêm yêu cầu gia hạn hàng '
       'mượn".')
b.image('06-tao-moi.png', 'Màn Thêm yêu cầu gia hạn hàng mượn')

b.h2('2. Khối Thông tin chung')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Người lập – Ngày lập', 'Chỉ hiển thị', 'Không', 'Tên bạn — ngày hôm nay',
     'Nằm ở góc phải tiêu đề khối.'],
    ['Phiếu yêu cầu xuất hàng mượn', 'Ô chỉ đọc + nút Chọn phiếu', 'Có', 'Để trống',
     'Bấm Chọn phiếu để chọn phiếu mượn cần gia hạn (xem mục 3).'],
    ['Ngày hẹn trả', 'Chỉ hiển thị', '—', 'Lấy theo phiếu mượn đã chọn',
     'Hạn trả đang có hiệu lực. Rê chuột vào biểu tượng chữ i để xem giải thích.'],
    ['Ngày hẹn trả mới', 'Ô chọn ngày', 'Có', 'Để trống',
     'Lịch chỉ cho chọn ngày SAU cả hôm nay lẫn Ngày hẹn trả, và không quá ngày tối đa (biểu '
     'tượng chữ i ghi rõ ngày tối đa).'],
    ['Ngày tạo', 'Chỉ hiển thị', '—', 'Ngày hôm nay', 'Phần mềm tự ghi, không sửa được.'],
    ['Ghi chú', 'Ô nhập chữ, tối đa 255 ký tự', 'Không', 'Để trống',
     'Nêu lý do xin gia hạn để người duyệt dễ quyết định.'],
])

b.h2('3. Chọn phiếu mượn cần gia hạn')
b.para('Bấm nút Chọn phiếu. Phần mềm mở cửa sổ "Chọn phiếu yêu cầu xuất hàng mượn" gồm các cột STT, '
       'Mã phiếu, Ngày tạo, Ngày hẹn trả, Ghi chú; có ô "Tìm theo mã phiếu mượn..." và có thể bấm '
       'tiêu đề Mã phiếu / Ngày tạo / Ngày hẹn trả để sắp xếp. Bấm vào một dòng để chọn.')
b.image('07-popup-chon-phieu-muon.png',
        'Cửa sổ Chọn phiếu yêu cầu xuất hàng mượn khi bạn chưa có phiếu mượn nào gia hạn được')
b.para('Cửa sổ chỉ liệt kê phiếu mượn thỏa đủ các điều kiện:', bold_prefix='Quan trọng: ')
b.bullet('Do chính bạn lập.')
b.bullet('Đã xuất kho và bạn còn đang mượn (chưa trả hết hàng).')
b.bullet('Chưa có phiếu gia hạn nào đang chờ duyệt cho phiếu mượn đó.')
b.bullet('Hạn trả hiện tại còn trước ngày tối đa (đã chạm ngày tối đa thì không còn ngày nào để '
         'gia hạn).')
b.para('Nếu không có phiếu nào, cửa sổ ghi: "Bạn không có phiếu mượn nào gia hạn được. Chỉ phiếu do '
       'chính bạn lập, đã xuất kho, còn đang mượn và chưa có yêu cầu gia hạn chờ duyệt mới hiện ở '
       'đây." — đây không phải lỗi.')

b.h2('4. Khối File đính kèm')
b.table([
    ['Trường', 'Kiểu nhập', 'Bắt buộc', 'Giá trị điền sẵn', 'Ghi chú'],
    ['Thêm tài liệu', 'Nút chọn file từ máy', 'Không', 'Chưa có file',
     'Chỉ nhận file PDF, mỗi file tối đa 13 MB, chọn được nhiều file. File được tải lên ngay và '
     'hiện tên, dung lượng trong bảng (STT, UPLOAD / FILE, DUNG LƯỢNG).'],
])

b.h2('5. Khối Chi tiết')
b.para('Trước khi chọn phiếu mượn, khối ghi "Chưa chọn phiếu mượn. Bấm Chọn phiếu ở trên để lấy '
       'danh sách hàng." Sau khi chọn, bảng hiện các mặt hàng của phiếu mượn: STT, Tên hàng hóa, '
       'Model, Mã hàng hóa, Thương hiệu, SL mượn, Đã trả, ĐVT và dòng Tổng cộng. Bảng chỉ để xem, '
       'bạn không phải nhập gì.')

b.h2('6. Giá trị phần mềm điền sẵn khi lập phiếu')
b.bullet('Người lập: chính bạn. Ngày tạo: ngày hôm nay.')
b.bullet('Ngày hẹn trả và bảng Chi tiết: lấy từ phiếu mượn bạn chọn.')
b.bullet('Phòng ban, công ty của phiếu: theo phòng ban, công ty của bạn ngay lúc gửi; sau này bạn '
         'đổi phòng ban thì phiếu cũ không đổi theo.')
b.bullet('Trạng thái: Chờ TP duyệt ngay khi gửi. Mã phiếu: phần mềm tự sinh.')

b.h2('7. Các nút ở cuối màn')
b.table([
    ['Nút', 'Phần mềm làm gì', 'Sau khi bấm'],
    ['Gửi duyệt', 'Gửi phiếu, trạng thái Chờ TP duyệt, báo cho Trưởng phòng duyệt được phiếu.',
     'Hiện "Yêu cầu của bạn đã được gửi" và quay về màn danh sách.'],
    ['Lưu và tiếp tục', 'Cũng GỬI phiếu đi y như Gửi duyệt (không phải lưu nháp).',
     'Ở lại màn với form trắng để lập phiếu tiếp theo.'],
    ['Quay lại', 'Thoát màn lập phiếu.',
     'Nếu đã chọn / nhập mà chưa gửi, phần mềm hỏi xác nhận trước khi rời trang.'],
])

b.h2('8. Các lỗi thường gặp khi gửi')
b.table([
    ['Tình huống', 'Phần mềm báo gì', 'Cách xử lý'],
    ['Chưa chọn phiếu mượn', 'Phiếu yêu cầu xuất hàng mượn – Bắt buộc phải chọn (kèm "Bạn chưa '
                             'nhập đầy đủ thông tin.")', 'Bấm Chọn phiếu.'],
    ['Chưa chọn ngày mới', 'Ngày hẹn trả mới – Bắt buộc phải chọn', 'Chọn ngày ở ô Ngày hẹn trả mới.'],
    ['Ngày mới không sau ngày hẹn trả hiện tại',
     'Phải sau ngày hẹn trả hiện tại (dd/mm/yyyy)', 'Chọn ngày muộn hơn.'],
    ['Ngày mới quá xa', 'Không thể mượn quá dd/mm/yyyy', 'Chọn ngày không quá ngày tối đa.'],
    ['Phiếu mượn vừa có yêu cầu gia hạn khác đang chờ',
     'Không thể gia hạn yêu cầu này: phiếu … đang có yêu cầu gia hạn PGHHM-… (…) chưa duyệt xong. '
     'Chờ yêu cầu đó được duyệt hoặc từ chối rồi mới lập yêu cầu mới.',
     'Chờ phiếu đang chờ được xử lý xong.'],
    ['File không phải PDF / quá 13 MB', 'Chỉ nhận file PDF / File đính kèm không được quá 13 MB',
     'Chuyển file sang PDF hoặc giảm dung lượng.'],
])

# =============================================================== PHAN 4
b.h1('PHẦN 4: XEM CHI TIẾT PHIẾU')

b.h2('1. Vào màn này bằng cách nào')
b.para(DUONG_TC + ' Bấm vào mã phiếu ở cột Mã phiếu. Bạn cũng có thể bấm vào thông báo ở chuông.')
b.image('08-chi-tiet.png', 'Màn chi tiết phiếu đang Chờ TP duyệt, góc nhìn người duyệt')

b.h2('2. Các khối trên màn chi tiết')
b.bullet('Thông tin chung: góc phải ghi người tạo và ngày giờ tạo; các ô Mã phiếu, Phiếu yêu cầu '
         'xuất hàng mượn (bấm để mở phiếu mượn ở tab mới), Người tạo, Phòng ban yêu cầu, Ngày hẹn '
         'trả, Ngày hẹn trả mới, Ngày tạo, Ghi chú. Mọi ô đều khóa.')
b.bullet('File đính kèm: tên file, nút xem (con mắt), nút tải về, dung lượng. Không có file thì '
         'ghi "Không có file đính kèm."')
b.bullet('Chi tiết: các mặt hàng của phiếu mượn và dòng Tổng cộng.')
b.bullet('Lịch sử duyệt: chỉ hiện khi đã có cấp duyệt hoặc từ chối — mỗi cấp một dòng gồm Cấp '
         'duyệt, Người duyệt, Thời gian, Ghi chú; cấp đã từ chối có nhãn đỏ "Từ chối".')
b.bullet('Lịch sử thay đổi: mặc định thu gọn, cạnh tiêu đề có số mốc (xem Phần 7).')
b.para('Ô Ngày hẹn trả mới chỉ mở khóa với Kế toán kho khi phiếu đang Chờ KT duyệt. Trưởng phòng '
       'và Ban giám đốc thấy ô này khóa là đúng (rê chuột vào chữ i để xem giải thích).',
       bold_prefix='Lưu ý: ')
b.para('Nút cuối màn: TP duyệt / BGĐ duyệt / KT duyệt và Từ chối (chỉ khi đến lượt bạn), In, '
       'Quay lại. Không có Sửa, Xóa.')
b.para('Nếu bạn không được xem phiếu, phần mềm báo "Bạn không có quyền xem phiếu này".')

# =============================================================== PHAN 5
b.h1('PHẦN 5: DUYỆT VÀ TỪ CHỐI PHIẾU')

b.h2('1. Vào màn này bằng cách nào')
b.bullet('Trưởng phòng, Ban giám đốc: bấm vào thông báo "[PGHHM] Chờ duyệt: <mã phiếu>." ở chuông, '
         'hoặc mở phiếu từ danh sách nếu thấy.')
b.bullet('Kế toán kho: Tài chính → Chờ duyệt → Hàng mượn chờ duyệt → Phiếu yêu cầu gia hạn hàng '
         'mượn chờ duyệt, rồi bấm biểu tượng Duyệt hoặc mã phiếu.')

b.h2('2. Luồng duyệt')
b.bullet('Chờ TP duyệt: chờ Trưởng phòng của phòng ban ghi trên phiếu.')
b.bullet('Chờ BGĐ duyệt: chỉ khi phiếu mượn còn nợ NHIỀU HƠN hạn mức của công ty.')
b.bullet('Chờ KT duyệt: bước cuối do Kế toán kho thực hiện.')
b.bullet('Đã duyệt: ngày hẹn trả của phiếu mượn đã đổi sang ngày mới.')
b.bullet('Không duyệt: bị từ chối ở một cấp bất kỳ, phiếu dừng hẳn.')
b.para('Ví dụ: hạn mức công ty là 20,000,000. Phiếu mượn có 1 mặt hàng xuất 10 cái, đã trả 6 cái, '
       'đơn giá 6,000,000 → còn nợ 4 × 6,000,000 = 24,000,000, lớn hơn hạn mức nên sau khi Trưởng '
       'phòng duyệt, phiếu chuyển lên Ban giám đốc. Nếu trả thêm 1 cái trước khi Trưởng phòng '
       'duyệt (còn nợ 18,000,000) thì phiếu sang thẳng Kế toán kho. Còn nợ đúng bằng 20,000,000 '
       'cũng sang thẳng Kế toán kho.', bold_prefix='Ví dụ: ')
b.para('Công ty chưa khai hạn mức thì được coi là 0 — mọi phiếu mượn còn nợ đều phải qua Ban giám '
       'đốc. Phần mềm tự quyết định, người duyệt không phải chọn.', bold_prefix='Lưu ý: ')

b.h2('3. Cách duyệt một phiếu')
b.bullet('Mở phiếu, xem lại thông tin và các mặt hàng.')
b.bullet('Nếu bạn là Kế toán kho: có thể sửa lại Ngày hẹn trả mới (vẫn phải sau hôm nay, sau hạn '
         'hiện tại của phiếu mượn và không quá ngày tối đa).')
b.bullet('Bấm nút duyệt ở cuối màn: TP duyệt, BGĐ duyệt hoặc KT duyệt tùy cấp.')
b.bullet('Phần mềm mở hộp Xác nhận duyệt, bấm Duyệt để đồng ý hoặc Hủy để thoát.')
b.image('10-xac-nhan-duyet.png', 'Hộp Xác nhận duyệt ở cấp Trưởng phòng')
b.para('Ở bước Kế toán kho, hộp xác nhận ghi rõ: "Duyệt bước Kế toán sẽ đổi ngày hẹn trả của phiếu '
       'mượn <mã> sang <ngày> ngay lập tức. Bạn có chắc chắn không?"')
b.table([
    ['Cấp duyệt', 'Phần mềm báo', 'Kết quả'],
    ['Trưởng phòng', '"Yêu cầu đã được chuyển đến Ban giám đốc." hoặc "Yêu cầu đã được chuyển '
                     'đến Kế toán."', 'Phiếu sang Chờ BGĐ duyệt hoặc Chờ KT duyệt; người duyệt '
                                      'cấp kế nhận thông báo.'],
    ['Ban giám đốc', '"Yêu cầu đã được chuyển đến Kế toán."', 'Phiếu sang Chờ KT duyệt.'],
    ['Kế toán kho', '"Duyệt phiếu thành công."', 'Phiếu Đã duyệt; ngày hẹn trả của phiếu mượn đổi; '
                                                 'người lập nhận thông báo kèm hạn trả mới.'],
])
b.para('Sau khi duyệt, phần mềm đưa bạn về màn danh sách.')

b.h2('4. Khi bị chặn duyệt vì nhân viên quá hạn')
b.para('Nếu công ty bật cấu hình chặn và phòng ban bạn quản lý đang có nhân viên quá hạn trả hàng '
       '(hàng giữ, hàng mượn hoặc hàng nhập thẳng), bấm duyệt sẽ bị chặn với thông báo dạng '
       '"Phòng ban bạn quản lý có nhân viên hàng mượn quá hạn. Không thể thực hiện thao tác này." '
       'và phần mềm mở cửa sổ liệt kê từng nhân viên đang quá hạn. Hãy nhắc nhân viên xử lý hàng '
       'quá hạn rồi duyệt lại. Thao tác Từ chối không bị chặn.')

b.h2('5. Cách từ chối một phiếu')
b.image('11-popup-tu-choi.png', 'Cửa sổ Từ chối yêu cầu gia hạn')
b.bullet('Bấm nút Từ chối ở cuối màn chi tiết, hoặc biểu tượng Từ chối ở cột Hành động.')
b.bullet('Cửa sổ "Từ chối yêu cầu gia hạn: <mã phiếu>" mở ra.')
b.bullet('Nhập Lý do từ chối (bắt buộc, tối đa 255 ký tự) rồi bấm Xác nhận từ chối.')
b.para('Phần mềm báo "Đã từ chối yêu cầu gia hạn hàng mượn.", phiếu sang Không duyệt và người lập '
       'nhận thông báo kèm lý do. Ngày hẹn trả của phiếu mượn không đổi. Người lập muốn gia hạn '
       'tiếp phải lập phiếu mới.', bold_prefix='Kết quả: ')
b.para('Bỏ trống lý do thì phần mềm báo "Lý do từ chối – Bắt buộc phải nhập" và cửa sổ không đóng.')

b.h2('6. Khi hai người cùng xử lý một phiếu')
b.para('Nếu phiếu vừa được người khác duyệt hoặc từ chối, thao tác của bạn bị từ chối với thông báo '
       '"Bạn không có quyền duyệt bước này.", "Bạn không có quyền từ chối phiếu này." hoặc "Phiếu '
       'không ở trạng thái chờ duyệt." Hãy tải lại danh sách để xem trạng thái mới nhất.')

# =============================================================== PHAN 6
b.h1('PHẦN 6: IN VÀ XUẤT EXCEL')

b.h2('1. Vào màn này bằng cách nào')
b.para(DUONG_TC + ' In phiếu: biểu tượng máy in ở cột Hành động hoặc nút In ở màn chi tiết. In '
       'danh sách và Xuất Excel: nút trên thanh công cụ của danh sách.')

b.h2('2. In một phiếu')
b.para('Phần mềm mở cửa sổ "Xem trước yêu cầu gia hạn hàng mượn <mã>" ngay trên màn, khổ A4 dọc. '
       'Bấm nút In ở đầu cửa sổ để gửi lệnh in.')
b.image('12-in-phieu.png', 'Bản xem trước in phiếu yêu cầu gia hạn hàng mượn')
b.para('Bản in gồm: phần đầu của công ty ghi trên phiếu; tiêu đề PHIẾU YÊU CẦU GIA HẠN HÀNG MƯỢN, '
       'Số phiếu, Ngày tạo; Người yêu cầu, Phòng ban, Phiếu mượn, Ngày hẹn trả cũ, Ngày hẹn trả '
       'mới, Trạng thái, Ghi chú; bảng hàng kèm Tổng cộng; bảng cấp duyệt (nếu đã có cấp xử lý, '
       'cấp từ chối ghi "(không duyệt)"); bốn ô ký Người lập, Trưởng phòng, Ban giám đốc, Kế toán.')

b.h2('3. In danh sách')
b.para('Bấm nút In trên thanh công cụ. Bản in khổ A4 ngang, in TOÀN BỘ phiếu khớp điều kiện lọc '
       'đang áp (không chỉ trang đang xem), có dòng Tổng số phiếu và dòng Khoảng thời gian nếu có '
       'lọc Ngày tạo.')
b.image('13-in-danh-sach.png', 'Bản xem trước in danh sách phiếu yêu cầu gia hạn hàng mượn')

b.h2('4. Xuất Excel')
b.para('Bấm nút Xuất Excel. Cửa sổ "Chọn trường xuất Excel" mở ra.')
b.image('05-chon-truong-xuat-excel.png', 'Cửa sổ Chọn trường xuất Excel')
b.bullet('Có 12 trường: Mã phiếu, Phiếu mượn, Người tạo, Ngày tạo, Ngày hẹn trả cũ, Ngày hẹn trả '
         'mới, Trạng thái, Người duyệt, Ngày duyệt, Phòng ban, Ghi chú, Lý do từ chối.')
b.bullet('Mặc định tích sẵn các trường đang hiện trên bảng ("Đang chọn 9/12 trường"). Dùng Chọn '
         'tất cả / Bỏ chọn hết cho nhanh.')
b.bullet('Kéo biểu tượng ba gạch để đổi thứ tự cột trong file. Cột STT luôn đứng đầu.')
b.bullet('Bấm Xuất file để tải về máy; trong lúc xuất nút bị khóa. Xong phần mềm báo "Xuất Excel '
         'thành công".')
b.para('File chứa toàn bộ phiếu khớp điều kiện lọc trong phạm vi bạn được xem, có dòng tiêu đề, '
       'dòng khoảng ngày (nếu lọc Ngày tạo) và khối ký Người lập ở cuối.')

# =============================================================== PHAN 7
b.h1('PHẦN 7: XEM LỊCH SỬ THAY ĐỔI')

b.h2('1. Vào màn này bằng cách nào')
b.bullet('Bấm biểu tượng đồng hồ (Lịch sử) ở cột Hành động của danh sách — mở cửa sổ "Lịch sử yêu '
         'cầu gia hạn hàng mượn".')
b.bullet('Hoặc mở phiếu, kéo xuống khối Lịch sử thay đổi, bấm Xem lịch sử.')
b.image('09-lich-su-thay-doi.png', 'Khối Lịch sử thay đổi đang mở ở màn chi tiết')
b.para('Mỗi mốc ghi thời điểm, tên thao tác (Tạo phiếu, Thay đổi thông tin, Trưởng phòng duyệt, '
       'Ban giám đốc duyệt, Kế toán duyệt, Không duyệt), người thực hiện kèm phòng ban, và các giá '
       'trị thay đổi: Trạng thái, Ngày hẹn trả mới, Ghi chú, File đính kèm. Mốc mới nhất ở trên '
       'cùng.')
b.para('Bấm Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày. Bấm Làm mới để '
       'tải lại, Thu gọn để đóng khối.')
b.para('Phiếu được lập và xử lý trên hệ thống cũ sẽ hiện "Chưa có lịch sử thao tác nào." — đây '
       'không phải lỗi.', bold_prefix='Lưu ý: ')

# =============================================================== PHAN 8
b.h1('PHẦN 8: NHỮNG ĐIỀU CẦN NHỚ')

b.bullet('Chỉ gia hạn được phiếu mượn do chính bạn lập, đã xuất kho, còn đang mượn và chưa có '
         'phiếu gia hạn nào đang chờ duyệt.')
b.bullet('Ngày hẹn trả mới phải sau hôm nay, sau ngày hẹn trả hiện tại và không quá ngày tối đa '
         '(hôm nay cộng số ngày mượn tối đa).')
b.bullet('Không có bản nháp, không sửa, không xóa: kiểm tra kỹ trước khi bấm Gửi duyệt hoặc Lưu và '
         'tiếp tục (cả hai đều gửi phiếu đi).')
b.bullet('Ngày hẹn trả của phiếu mượn chỉ đổi khi Kế toán kho duyệt. Các bước trước chưa thay đổi '
         'gì.')
b.bullet('Phiếu bị từ chối dừng ở trạng thái Không duyệt; muốn gia hạn tiếp hãy lập phiếu mới.')
b.bullet('Trưởng phòng nên mở phiếu cần duyệt từ thông báo ở chuông.')

print(b.finish())
