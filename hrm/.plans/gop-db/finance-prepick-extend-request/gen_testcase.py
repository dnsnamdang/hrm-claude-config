# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man "Yeu cau gia han hang giu" (phan he Tai chinh).

Viet MOI hoan toan tu code HRM nhanh `gop_db` (user chot 05/09/2026), khong chep bo TC ERP.
Ngon ngu: NGHIEP VU cho QA — khong dung thuat ngu code.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, '..', '..', '..', '.claude', 'skills',
                                'testcase-documenter', 'assets'))
from tc_engine import build  # noqa: E402

MODULE = 'YC gia hạn hàng giữ'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn hình Yêu cầu gia hạn hàng giữ (mã phiếu PGHHG) dùng để nhân viên kinh doanh xin kéo '
     'dài thời gian giữ hàng cho khách khi lô hàng sắp hết hạn giữ.\n'
     'Phiếu đi qua ba cấp duyệt: Trưởng phòng → Ban giám đốc (chỉ với phiếu thuộc diện phải '
     'trình) → Kế toán. Hàng chỉ thực sự được gia hạn khi Kế toán duyệt ở bước cuối.\n'
     'Đường dẫn: Phân hệ Tài chính → Giữ hàng → Yêu cầu gia hạn hàng giữ.'),
    ('2. Đối tượng được tính / hiển thị',
     'Danh sách hiển thị phiếu theo phạm vi quyền của người đăng nhập:\n'
     '- Có quyền "Xem phiếu hàng giữ theo tổng công ty": toàn bộ phiếu của mọi công ty.\n'
     '- Có quyền "Xem phiếu hàng giữ theo công ty": phiếu thuộc công ty của mình.\n'
     '- Có quyền "Xem phiếu hàng giữ theo phòng ban": phiếu thuộc phòng ban mình quản lý và '
     'phòng ban của chính mình.\n'
     '- Không có quyền nào ở trên: chỉ phiếu do chính mình lập.\n'
     '- Ngoài phạm vi trên, mọi người đều được thấy thêm những phiếu đang chờ chính mình duyệt.\n'
     'Bảng Chi tiết của màn lập phiếu chỉ liệt kê lô hàng giữ thỏa mãn cả ba điều kiện: do '
     'chính người lập đứng tên giữ, còn số lượng lớn hơn 0, và có hạn giữ trước "hôm nay + '
     '7 ngày" (số ngày cảnh báo).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu ở trạng thái Đang tạo của người khác: KHÔNG hiện trong danh sách và không mở được '
     'màn chi tiết.\n'
     '- Lô hàng giữ còn hạn dài hơn 7 ngày: không hiện ở bảng Chi tiết khi lập phiếu.\n'
     '- Lô hàng giữ đã hết số lượng: không hiện.\n'
     '- Lô hàng giữ của nhân viên khác hoặc khác công ty với người lập: không hiện.\n'
     '- Dòng không tích ô "Cần gia hạn": không được gửi lên khi lưu phiếu.\n'
     '- Dòng có Hạn giữ mới trùng đúng Hạn giữ hiện tại: bị bỏ qua, không ghi hàng giữ khi duyệt.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Hai ô "Ngày tạo từ" và "Ngày tạo đến" lọc theo NGÀY LẬP PHIẾU, không phải ngày duyệt và '
     'không phải hạn giữ.\n'
     'Khoảng ngày lấy trọn hai đầu mút. Chỉ nhập một đầu thì lọc một chiều.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Một phiếu gồm phần thông tin chung (mã phiếu, trạng thái, phòng ban yêu cầu, ghi chú, '
     'tệp đính kèm) và nhiều dòng hàng hóa.\n'
     'Mỗi dòng hàng gắn với một lô hàng giữ cụ thể, xác định bởi: người giữ – khách hàng – '
     'hàng hóa – hạn giữ – công ty.\n'
     'Phiếu có ba bộ thông tin duyệt tương ứng ba cấp Trưởng phòng, Ban giám đốc, Kế toán; mỗi '
     'bộ gồm người thực hiện, thời điểm và ghi chú.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     'Không cộng dồn dòng. Mỗi lô hàng giữ là một dòng riêng, kể cả khi trùng hàng hóa nhưng '
     'khác khách hàng hoặc khác hạn giữ.\n'
     'Khi Kế toán duyệt, phần mềm trừ số lượng ở lô cũ rồi CỘNG vào lô có cùng người giữ, cùng '
     'khách hàng, cùng hàng hóa nhưng hạn giữ là hạn giữ mới; nếu chưa có lô đó thì tạo lô mới. '
     'Lô mới lấy công ty theo lô nguồn, không theo người duyệt.'),
    ('7. Phân quyền cấp',
     'Quyền thao tác:\n'
     '- Trưởng phòng duyệt hàng giữ\n'
     '- Ban giám đốc duyệt hàng giữ\n'
     '- Kế toán duyệt hàng giữ\n'
     'Quyền phạm vi dữ liệu:\n'
     '- Xem phiếu hàng giữ theo tổng công ty\n'
     '- Xem phiếu hàng giữ theo công ty\n'
     '- Xem phiếu hàng giữ theo phòng ban\n'
     'Màn hình KHÔNG có quyền riêng cho Thêm / Sửa / Xóa: ai đăng nhập cũng lập được phiếu cho '
     'hàng giữ của chính mình, và chỉ sửa/xóa được phiếu của mình khi phiếu còn Đang tạo.'),
    ('8. Cách tính các ô thống kê',
     'Ô "Hiển thị a–b / N": a là số thứ tự dòng đầu của trang, b là dòng cuối của trang, N là '
     'tổng số phiếu khớp bộ lọc TRONG PHẠM VI QUYỀN của người đang xem (không phải tổng toàn '
     'hệ thống).\n'
     'Cột "Đang giữ" = số lượng còn lại của chính lô hàng giữ trên dòng đó.\n'
     'Cột "Có thể giữ" = tồn kho khả dụng của hàng hóa trong công ty; đây là số THAM KHẢO, '
     'khác hoàn toàn với cột "Đang giữ".\n'
     'Dòng "Tổng cộng" trên bản in = tổng cột SL gia hạn của các dòng được in.'),
    ('9. Ghi chú đọc bảng',
     'Các bẫy dễ sai nhất của màn này:\n'
     '- "Có thể giữ" và "Đang giữ" là HAI con số khác nhau; đừng so hai cột này với nhau.\n'
     '- Gia hạn KHÔNG sửa hạn của lô cũ mà chuyển số lượng sang lô có hạn mới, nên sau khi '
     'duyệt sẽ thấy hai dòng biến động (một trừ, một cộng) trong lịch sử của lô hàng.\n'
     '- Trạng thái "Đang tạo" hiển thị màu XÁM (nháp), không phải màu đỏ.\n'
     '- Phiếu bị từ chối quay về đúng trạng thái "Đang tạo", KHÔNG có trạng thái "Từ chối" '
     'riêng; phải xem cột Lý do từ chối hoặc khối Lịch sử duyệt mới biết phiếu từng bị trả về.\n'
     '- Không phải phiếu nào cũng qua Ban giám đốc; phần mềm tự quyết theo tỉ lệ tiền đã thu '
     'của hợp đồng hoặc tổng giá trị hàng xin gia hạn.\n'
     '- Trưởng phòng phải quản lý ĐÚNG phòng ban ghi trên phiếu mới duyệt được, chỉ có quyền '
     'là chưa đủ.\n'
     '- Người duyệt được sửa Hạn giữ mới nhưng KHÔNG sửa được số lượng.\n'
     '- Nhóm test bảo mật gọi thẳng chức năng bằng công cụ kiểm thử dành cho tester kỹ thuật.'),
]

ROLE_TCS = [
    ('00', 'Tài khoản không có quyền nào của nhóm hàng giữ vẫn vào được màn hình', 'P0',
     'Tài khoản A không có quyền duyệt và không có quyền xem theo cấp; A đã lập 6 phiếu; '
     'toàn hệ thống có 1.359 phiếu.',
     '1. Đăng nhập bằng tài khoản A.\n2. Vào Tài chính → Giữ hàng → Yêu cầu gia hạn hàng giữ.',
     '—',
     '- Màn hình mở được, không báo lỗi quyền.\n'
     '- Danh sách chỉ có 6 phiếu do A lập.\n'
     '- Ô "Hiển thị a–b / N" ghi N = 6.\n'
     '- Nút Tạo mới vẫn hiển thị.\n'
     '- Bảng lọc nâng cao KHÔNG có ô Công ty và ô Phòng ban.'),
    ('01', 'Quyền "Xem phiếu hàng giữ theo tổng công ty" thấy phiếu của mọi công ty', 'P0',
     'Tài khoản B chỉ có quyền Xem phiếu hàng giữ theo tổng công ty. Hệ thống có phiếu của '
     'ít nhất 2 công ty khác nhau.',
     '1. Đăng nhập bằng B.\n2. Mở màn Yêu cầu gia hạn hàng giữ.\n'
     '3. Đếm N ở ô "Hiển thị a–b / N".\n4. Lọc lần lượt từng công ty ở ô Công ty.',
     '—',
     '- N bằng tổng số phiếu khác nháp của toàn hệ thống cộng phiếu nháp của chính B.\n'
     '- Bảng lọc nâng cao CÓ ô Công ty và ô Phòng ban.\n'
     '- Lọc theo từng công ty ra đúng số phiếu của công ty đó.'),
    ('02', 'Quyền "Xem phiếu hàng giữ theo công ty" chỉ thấy phiếu công ty mình', 'P0',
     'Tài khoản C thuộc công ty 1, chỉ có quyền Xem phiếu hàng giữ theo công ty. Công ty 1 có '
     '1.200 phiếu, công ty 4 có 120 phiếu.',
     '1. Đăng nhập bằng C.\n2. Mở màn danh sách.\n3. Đọc N.\n'
     '4. Mở một phiếu bất kỳ của công ty 4 bằng đường dẫn trực tiếp.',
     '—',
     '- N = 1.200 (chỉ phiếu công ty 1), không thấy phiếu công ty 4.\n'
     '- Bảng lọc CÓ ô Phòng ban, KHÔNG có ô Công ty.\n'
     '- ⚠️ Mở phiếu công ty 4 bằng đường dẫn: phần mềm báo không có quyền xem phiếu này, '
     'không hiển thị nội dung phiếu.'),
    ('03', 'Quyền "Xem phiếu hàng giữ theo phòng ban" chỉ thấy phòng mình quản lý', 'P0',
     'Tài khoản D được phân công quản lý phòng "PHÒNG THIẾT BỊ Ô TÔ 1"; phòng này có 40 phiếu; '
     'phòng "PHÒNG THIẾT BỊ Ô TÔ 2" có 35 phiếu.',
     '1. Đăng nhập bằng D.\n2. Mở màn danh sách.\n3. Đọc N và kiểm cột Phòng ban (bật cột này '
     'trong Tuỳ chỉnh cột).',
     '—',
     '- N = 40 cộng số phiếu nháp của chính D.\n'
     '- Mọi dòng đều thuộc phòng D quản lý hoặc phòng của chính D.\n'
     '- Không có dòng nào thuộc PHÒNG THIẾT BỊ Ô TÔ 2.'),
    ('04', 'Quyền "Trưởng phòng duyệt hàng giữ" hiện nút duyệt đúng phiếu', 'P0',
     'Tài khoản E có quyền Trưởng phòng duyệt hàng giữ, quản lý phòng P1. Phiếu X ở trạng thái '
     'Chờ TP duyệt thuộc phòng P1; phiếu Y ở Chờ TP duyệt thuộc phòng P2 (E không quản lý); '
     'phiếu Z ở Chờ KT duyệt thuộc P1.',
     '1. Đăng nhập bằng E.\n2. Mở danh sách, xem cột Hành động của X, Y, Z.\n'
     '3. Mở từng phiếu ra xem nút cuối màn.',
     '—',
     '- Phiếu X: có biểu tượng duyệt và từ chối; mở ra có nút "TP duyệt" và "Từ chối".\n'
     '- Phiếu Y: KHÔNG có nút duyệt/từ chối (E không quản lý phòng P2).\n'
     '- Phiếu Z: KHÔNG có nút duyệt (sai cấp — đang chờ Kế toán).'),
    ('05', 'Quyền "Ban giám đốc duyệt hàng giữ"', 'P0',
     'Tài khoản F có quyền Ban giám đốc duyệt hàng giữ, cùng công ty với phiếu M đang ở trạng '
     'thái Chờ BGĐ duyệt.',
     '1. Đăng nhập bằng F.\n2. Mở phiếu M.',
     '—',
     '- Cuối màn có nút "BGĐ duyệt" và "Từ chối".\n'
     '- Với phiếu ở trạng thái Chờ TP duyệt hoặc Chờ KT duyệt, hai nút này không hiển thị.'),
    ('06', 'Quyền "Kế toán duyệt hàng giữ"', 'P0',
     'Tài khoản G có quyền Kế toán duyệt hàng giữ, cùng công ty với phiếu N đang ở trạng thái '
     'Chờ KT duyệt.',
     '1. Đăng nhập bằng G.\n2. Mở phiếu N.',
     '—',
     '- Cuối màn có nút "KT duyệt" và "Từ chối".\n'
     '- ⚠️ Đây là bước duy nhất làm thay đổi hàng giữ thật, phải kiểm kỹ ở nhóm VII.'),
    ('07', 'Người duyệt khác công ty với phiếu thì không duyệt được', 'P0',
     'Tài khoản H có quyền Kế toán duyệt hàng giữ, thuộc công ty 4. Phiếu K ở trạng thái Chờ KT '
     'duyệt thuộc công ty 1.',
     '1. Đăng nhập bằng H.\n2. Tìm phiếu K.',
     '—',
     '- Nếu H không có quyền xem theo cấp: phiếu K không xuất hiện trong danh sách.\n'
     '- Nếu H thấy được phiếu K: nút KT duyệt KHÔNG hiển thị.\n'
     '- ⚠️ Dùng công cụ kiểm thử để gọi thẳng chức năng duyệt phiếu K: phần mềm từ chối, báo '
     'không có quyền duyệt bước này; trạng thái phiếu K không đổi.'),
    ('08', 'Bỏ qua giao diện gọi thẳng chức năng Sửa phiếu của người khác', 'P0',
     'Tài khoản A không phải người lập phiếu P (P đang ở trạng thái Đang tạo của người khác).',
     '1. Đăng nhập bằng A.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa với phiếu P.',
     '—',
     '- Phần mềm từ chối, không cho sửa.\n- Nội dung phiếu P không thay đổi.'),
    ('09', 'Bỏ qua giao diện gọi thẳng chức năng Xóa phiếu đã gửi duyệt', 'P0',
     'Phiếu Q do tài khoản A lập nhưng đã ở trạng thái Chờ TP duyệt.',
     '1. Đăng nhập bằng A.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa với phiếu Q.',
     '—',
     '- Phần mềm từ chối xóa.\n- Phiếu Q vẫn còn và giữ nguyên trạng thái Chờ TP duyệt.'),
    ('10', 'Bỏ qua giao diện gọi thẳng chức năng Từ chối khi không đúng cấp', 'P0',
     'Tài khoản E chỉ có quyền Trưởng phòng duyệt hàng giữ. Phiếu R đang ở trạng thái Chờ KT '
     'duyệt.',
     '1. Đăng nhập bằng E.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Từ chối với phiếu R.',
     '—',
     '- Phần mềm từ chối, báo không có quyền từ chối phiếu này.\n'
     '- Phiếu R vẫn ở trạng thái Chờ KT duyệt, không phát sinh lý do từ chối.'),
    ('11', 'Xem lịch sử thay đổi của phiếu ngoài phạm vi quyền', 'P1',
     'Tài khoản C (xem theo công ty 1) và phiếu S thuộc công ty 4.',
     '1. Đăng nhập bằng C.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng xem lịch sử của phiếu S.',
     '—',
     '- Phần mềm từ chối, báo không có quyền xem phiếu này.'),
]

# ============================================================== I
S1 = [
    ('001', 'Mở màn hình từ menu', 'P0',
     'Tài khoản có ít nhất 1 phiếu trong phạm vi.',
     '1. Đăng nhập.\n2. Chọn phân hệ Tài chính.\n3. Mở nhóm Hàng hoá - Dịch vụ - Vận chuyển → '
     'Giữ hàng.\n4. Bấm mục Yêu cầu gia hạn hàng giữ.',
     '—',
     '- Tiêu đề trên thanh trên cùng ghi "Yêu cầu gia hạn hàng giữ".\n'
     '- Tiêu đề bảng cũng ghi "Yêu cầu gia hạn hàng giữ".\n'
     '- Bảng hiện dữ liệu, không có thông báo lỗi.'),
    ('002', 'Vòng quay chờ hiện ngay khi vào màn', 'P1',
     'Danh sách có trên 1.000 phiếu.',
     '1. Mở màn hình và quan sát bảng trong lúc dữ liệu đang tải.',
     '—',
     '- Trong lúc chờ, bảng hiện vòng quay chờ.\n'
     '- ⚠️ KHÔNG được nhấp nháy dòng "Không có dữ liệu phù hợp." rồi mới hiện dữ liệu.'),
    ('003', 'Bố cục màn hình đầy đủ hai khối', 'P1', 'Đã vào màn hình.',
     '1. Quan sát toàn màn hình.',
     '—',
     '- Khối trên: ô tìm nhanh, nút Tìm kiếm, Làm mới, Cài đặt bộ lọc, Tìm kiếm nâng cao.\n'
     '- Khối dưới: tiêu đề bảng, thanh công cụ (Tạo mới, In, Xuất Excel, biểu tượng cấu hình '
     'cột), bảng dữ liệu, thanh phân trang.'),
    ('004', 'Đủ 13 cột theo cấu hình mặc định', 'P0', 'Người dùng chưa từng đổi cấu hình cột.',
     '1. Quan sát tiêu đề các cột, cuộn ngang nếu cần.',
     '—',
     '- Hiện sẵn: STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, '
     'Người cập nhật, Ngày cập nhật, Hành động.\n'
     '- Ẩn sẵn: Phòng ban, Ghi chú, Lý do từ chối.'),
    ('005', 'Mã phiếu là liên kết mở màn chi tiết', 'P0', 'Danh sách có ít nhất 1 phiếu.',
     '1. Bấm vào mã phiếu ở dòng đầu tiên.',
     '—',
     '- Mở màn chi tiết đúng phiếu vừa bấm.\n'
     '- Tiêu đề màn ghi "Chi tiết yêu cầu gia hạn hàng giữ: <mã phiếu>".'),
    ('006', 'Mở mã phiếu ở tab mới bằng chuột phải', 'P2', 'Danh sách có ít nhất 1 phiếu.',
     '1. Bấm chuột phải vào mã phiếu.\n2. Chọn mở liên kết ở tab mới.',
     '—',
     '- Tab mới mở đúng màn chi tiết của phiếu đó.'),
    ('007', 'Màu trạng thái đúng quy ước', 'P0',
     'Danh sách có đủ phiếu ở các trạng thái Đang tạo, Chờ TP duyệt, Chờ BGĐ duyệt, '
     'Chờ KT duyệt, Đã duyệt.',
     '1. Lọc lần lượt từng trạng thái và quan sát màu nhãn ở cột Trạng thái.',
     'Trạng thái: lần lượt 5 giá trị',
     '- Đang tạo: nhãn XÁM.\n- Chờ TP duyệt / Chờ BGĐ duyệt / Chờ KT duyệt: nhãn CAM.\n'
     '- Đã duyệt: nhãn XANH LÁ.\n'
     '- ⚠️ "Đang tạo" là bản nháp nên phải xám, tuyệt đối không được đỏ.'),
    ('008', 'Phiếu nháp của người khác không hiện', 'P0',
     'Tài khoản A có quyền xem theo tổng công ty. Tài khoản B đang có 1 phiếu ở trạng thái '
     'Đang tạo.',
     '1. Đăng nhập bằng A.\n2. Lọc Trạng thái = Đang tạo.',
     'Trạng thái: Đang tạo',
     '- Danh sách KHÔNG có phiếu nháp của B.\n'
     '- Chỉ hiện phiếu nháp do chính A lập (nếu có).'),
    ('009', 'Người duyệt thấy thêm phiếu đang chờ mình duyệt', 'P0',
     'Tài khoản E không có quyền xem theo cấp, nhưng có quyền Trưởng phòng duyệt hàng giữ và '
     'quản lý phòng P1. Phòng P1 có 3 phiếu Chờ TP duyệt do người khác lập. E tự lập 2 phiếu.',
     '1. Đăng nhập bằng E.\n2. Mở màn danh sách và đọc N.',
     '—',
     '- N = 5 (2 phiếu của E cộng 3 phiếu đang chờ E duyệt).\n'
     '- 3 phiếu chờ duyệt đều có biểu tượng duyệt ở cột Hành động.'),
    ('010', 'Trạng thái rỗng khi không có dữ liệu', 'P1',
     'Tài khoản mới, chưa lập phiếu nào và không có quyền xem theo cấp.',
     '1. Mở màn hình.',
     '—',
     '- Bảng hiện dòng "Không có dữ liệu phù hợp.".\n- Ô thống kê ghi N = 0.'),
    ('011', 'Tiêu đề tab trình duyệt', 'P2', 'Đã vào màn hình.',
     '1. Quan sát tên tab trình duyệt.',
     '—',
     '- Tên tab ghi "Yêu cầu gia hạn hàng giữ".'),
]

# ============================================================== II
S2 = [
    ('001', 'Tìm nhanh theo mã phiếu đầy đủ', 'P0',
     'Tồn tại phiếu PGHHG-01501 trong phạm vi quyền.',
     '1. Gõ PGHHG-01501 vào ô tìm nhanh.\n2. Bấm nút Tìm kiếm.',
     'Ô tìm nhanh: PGHHG-01501',
     '- Danh sách còn đúng 1 dòng là PGHHG-01501.\n- N = 1.'),
    ('002', 'Tìm nhanh theo một phần mã phiếu', 'P1', 'Có nhiều phiếu mã bắt đầu bằng PGHHG-015.',
     '1. Gõ 015 vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: 015',
     '- Mọi dòng trả về đều có mã phiếu chứa chuỗi 015.'),
    ('003', 'Ô tìm nhanh KHÔNG tự tìm khi đang gõ', 'P1', 'Đang ở màn danh sách.',
     '1. Gõ vài ký tự vào ô tìm nhanh.\n2. Chờ 5 giây, không bấm gì.',
     'Ô tìm nhanh: PGHH',
     '- Danh sách giữ nguyên, không tự lọc lại.\n'
     '- Chỉ khi bấm nút Tìm kiếm hoặc nhấn Enter mới lọc.'),
    ('004', 'Nhấn Enter trong ô tìm nhanh', 'P2', 'Đang ở màn danh sách.',
     '1. Gõ mã phiếu vào ô tìm nhanh.\n2. Nhấn phím Enter.',
     'Ô tìm nhanh: PGHHG-01500',
     '- Danh sách lọc lại đúng như khi bấm nút Tìm kiếm.'),
    ('005', 'Mở và đóng bảng lọc nâng cao', 'P1', 'Đang ở màn danh sách.',
     '1. Bấm nút Tìm kiếm nâng cao.\n2. Bấm lại nút đó.',
     '—',
     '- Lần 1: bảng lọc mở ra, nhãn nút đổi thành "Ẩn tìm kiếm nâng cao".\n'
     '- Lần 2: bảng lọc thu gọn lại.'),
    ('006', 'Đủ các ô lọc theo quyền cao nhất', 'P0',
     'Tài khoản có quyền Xem phiếu hàng giữ theo tổng công ty và chưa đổi Cài đặt bộ lọc.',
     '1. Mở bảng lọc nâng cao.\n2. Đếm và đọc nhãn từng ô.',
     '—',
     '- Có đủ: Công ty, Phòng ban, Mã phiếu, Trạng thái, Người tạo, Người duyệt, Tên hàng hóa, '
     'Mã hàng hóa, Ngày tạo từ, Ngày tạo đến.'),
    ('007', 'Ô Công ty và Phòng ban ẩn theo quyền', 'P0',
     'Tài khoản không có quyền xem theo cấp nào.',
     '1. Mở bảng lọc nâng cao.',
     '—',
     '- KHÔNG có ô Công ty và ô Phòng ban.\n- Các ô lọc còn lại vẫn đủ.'),
    ('008', 'Lọc theo Trạng thái', 'P0', 'Có phiếu ở nhiều trạng thái khác nhau.',
     '1. Mở bảng lọc nâng cao.\n2. Chọn Trạng thái = Đã duyệt.',
     'Trạng thái: Đã duyệt',
     '- Danh sách tự lọc lại NGAY, không cần bấm nút Tìm kiếm.\n'
     '- Mọi dòng đều có nhãn Đã duyệt.\n- N giảm tương ứng.'),
    ('009', 'Lọc theo Người tạo', 'P1',
     'Nhân viên "Nguyễn Văn Mạnh" có 12 phiếu trong phạm vi quyền.',
     '1. Chọn Người tạo = Nguyễn Văn Mạnh.',
     'Người tạo: Nguyễn Văn Mạnh',
     '- N = 12.\n- Mọi dòng đều có cột Người tạo là Nguyễn Văn Mạnh.'),
    ('010', 'Lọc theo Người duyệt', 'P1', 'Có phiếu đã được duyệt bởi nhiều người khác nhau.',
     '1. Chọn Người duyệt = một nhân viên cụ thể.',
     'Người duyệt: Nguyễn Thị Mỹ',
     '- Mọi dòng trả về đều có cột Người duyệt đúng người đã chọn.\n'
     '- Phiếu chưa duyệt không xuất hiện.'),
    ('011', 'Lọc theo Mã phiếu ở bảng nâng cao', 'P1',
     'Có ít nhất 1 phiếu mã PGHHG-01499.',
     '1. Nhập PGHHG-01499 vào ô Mã phiếu của bảng lọc nâng cao.',
     'Mã phiếu: PGHHG-01499',
     '- Danh sách còn đúng phiếu đó.\n'
     '- ⚠️ Ô này lọc độc lập với ô tìm nhanh; hai ô có thể dùng cùng lúc.'),
    ('012', 'Lọc theo Tên hàng hóa', 'P0',
     'Có phiếu chứa hàng "Kích cá sấu 3 tấn, thân dài".',
     '1. Nhập "Kích cá sấu" vào ô Tên hàng hóa.',
     'Tên hàng hóa: Kích cá sấu',
     '- Chỉ còn những phiếu có ít nhất một dòng hàng khớp tên.\n'
     '- Mở một phiếu bất kỳ trong kết quả để kiểm chứng có dòng hàng đó.'),
    ('013', 'Lọc theo Mã hàng hóa', 'P0', 'Có phiếu chứa hàng mã TORI-T830036.',
     '1. Nhập TORI-T830036 vào ô Mã hàng hóa.',
     'Mã hàng hóa: TORI-T830036',
     '- Chỉ còn những phiếu có dòng hàng đúng mã đó.'),
    ('014', 'Lọc theo khoảng Ngày tạo', 'P0', 'Có phiếu lập trong tháng 07/2026.',
     '1. Chọn Ngày tạo từ = 01/07/2026.\n2. Chọn Ngày tạo đến = 31/07/2026.',
     'Ngày tạo từ: 01/07/2026; Ngày tạo đến: 31/07/2026',
     '- Mọi dòng có Ngày tạo nằm trong tháng 7, lấy trọn hai đầu mút.\n'
     '- Phiếu lập ngày 01/07 và ngày 31/07 đều được tính.'),
    ('015', 'Chỉ nhập Ngày tạo từ', 'P1', 'Có phiếu ở nhiều mốc thời gian.',
     '1. Chọn Ngày tạo từ = 01/08/2026, để trống ô Ngày tạo đến.',
     'Ngày tạo từ: 01/08/2026',
     '- Trả về mọi phiếu lập từ 01/08/2026 trở về sau.'),
    ('016', 'Chọn Ngày tạo từ lớn hơn Ngày tạo đến', 'P1', 'Đang ở màn danh sách.',
     '1. Chọn Ngày tạo từ = 31/08/2026.\n2. Chọn Ngày tạo đến = 01/08/2026.',
     'Ngày tạo từ: 31/08/2026; Ngày tạo đến: 01/08/2026',
     '- Phần mềm không treo, không báo lỗi hệ thống.\n'
     '- Danh sách trả về rỗng kèm dòng "Không có dữ liệu phù hợp.".'),
    ('017', 'Kết hợp nhiều tiêu chí lọc', 'P0', 'Có dữ liệu phù hợp.',
     '1. Chọn Trạng thái = Đã duyệt.\n2. Chọn Người tạo = một nhân viên.\n'
     '3. Chọn khoảng Ngày tạo trong tháng 7.',
     'Trạng thái: Đã duyệt; Người tạo: Lại Văn Hiệp; khoảng 01/07–31/07/2026',
     '- Kết quả thỏa mãn ĐỒNG THỜI cả ba điều kiện.\n- N cập nhật đúng.'),
    ('018', 'Đổi Công ty thì Phòng ban được nạp lại', 'P0',
     'Tài khoản có quyền xem theo tổng công ty.',
     '1. Chọn Công ty = công ty 1, chọn tiếp một Phòng ban.\n2. Đổi Công ty sang công ty 4.',
     'Công ty: lần lượt 2 giá trị',
     '- Giá trị Phòng ban đang chọn bị xóa.\n'
     '- Danh sách phòng ban được nạp lại đúng theo công ty mới.'),
    ('019', 'Nút Làm mới xóa hết điều kiện lọc', 'P0',
     'Đang áp ít nhất 3 điều kiện lọc và danh sách đang bị thu hẹp.',
     '1. Bấm nút Làm mới.',
     '—',
     '- Mọi ô lọc trở về trống.\n'
     '- ⚠️ Danh sách được TẢI LẠI ngay, N trở về đúng tổng phiếu trong phạm vi quyền — không '
     'được giữ nguyên kết quả lọc cũ.\n'
     '- Thứ tự sắp xếp cũng trở về mặc định.'),
    ('020', 'Bộ lọc được ghi nhớ khi quay lại màn', 'P1',
     'Đang áp bộ lọc Trạng thái = Đã duyệt.',
     '1. Mở một phiếu rồi bấm Quay lại (trong vòng 10 phút).',
     '—',
     '- Bộ lọc Trạng thái = Đã duyệt vẫn còn.\n- Danh sách vẫn đang lọc.'),
    ('021', 'Bộ lọc hết hạn ghi nhớ sau 10 phút', 'P2', 'Đang áp bộ lọc.',
     '1. Rời khỏi màn hình quá 10 phút.\n2. Quay lại màn hình.',
     '—',
     '- Bộ lọc trở về trống, danh sách hiển thị đầy đủ trong phạm vi quyền.'),
    ('022', 'Lọc ra kết quả rỗng', 'P1', 'Đang ở màn danh sách.',
     '1. Nhập vào ô Mã phiếu một chuỗi chắc chắn không tồn tại.',
     'Mã phiếu: ZZZZ-99999',
     '- Bảng hiện dòng "Không có dữ liệu phù hợp.".\n- N = 0.\n- Không có lỗi hệ thống.'),
    ('023', 'Cài đặt bộ lọc — bỏ tích một ô lọc', 'P1', 'Đang ở màn danh sách.',
     '1. Bấm nút Cài đặt bộ lọc.\n2. Bỏ tích ô "Mã hàng hóa".\n3. Bấm Lưu.\n'
     '4. Mở lại bảng lọc nâng cao.',
     '—',
     '- Cửa sổ liệt kê 9 mục lọc kèm số thứ tự.\n'
     '- Sau khi lưu, bảng lọc nâng cao KHÔNG còn ô Mã hàng hóa.\n'
     '- Các ô còn lại giữ nguyên thứ tự.'),
    ('024', 'Cài đặt bộ lọc — kéo đổi thứ tự', 'P2', 'Cửa sổ Cài đặt bộ lọc đang mở.',
     '1. Kéo mục "Trạng thái" lên vị trí số 1.\n2. Bấm Lưu.',
     '—',
     '- Bảng lọc nâng cao hiển thị ô Trạng thái ở vị trí đầu tiên.'),
    ('025', 'Cài đặt bộ lọc — Khôi phục mặc định', 'P2',
     'Đã bỏ tích và đổi thứ tự một vài ô lọc.',
     '1. Mở Cài đặt bộ lọc.\n2. Bấm Khôi phục mặc định.\n3. Bấm Lưu.',
     '—',
     '- Danh sách ô lọc trở về đủ 9 mục theo thứ tự ban đầu.'),
    ('026', 'Cài đặt bộ lọc — Đóng không lưu', 'P2', 'Cửa sổ Cài đặt bộ lọc đang mở.',
     '1. Bỏ tích 2 ô lọc.\n2. Bấm nút Đóng.\n3. Mở lại cửa sổ.',
     '—',
     '- Hai ô vừa bỏ tích vẫn đang được tích: thay đổi không được lưu.'),
    ('027', 'Cấu hình bộ lọc lưu riêng theo người dùng', 'P1',
     'Tài khoản A đã bỏ tích ô Mã hàng hóa.',
     '1. Đăng nhập bằng tài khoản B khác.\n2. Mở bảng lọc nâng cao.',
     '—',
     '- Tài khoản B vẫn thấy đủ 9 ô lọc; cấu hình của A không ảnh hưởng tới B.'),
]

# ============================================================== III
S3 = [
    ('001', 'Phân trang mặc định 10 dòng', 'P0', 'Danh sách có 1.359 phiếu.',
     '1. Mở màn hình và quan sát bảng, ô thống kê và ô Số dòng/trang.',
     '—',
     '- Bảng hiện đúng 10 dòng.\n- Ô thống kê ghi "Hiển thị 1–10 / 1359".\n'
     '- Ô Số dòng/trang đang là 10.'),
    ('002', 'Chuyển sang trang 2', 'P0', 'Danh sách nhiều hơn 1 trang.',
     '1. Bấm số 2 ở thanh phân trang.',
     '—',
     '- Bảng hiện 10 dòng tiếp theo.\n- Ô thống kê ghi "Hiển thị 11–20 / 1359".\n'
     '- Cột STT chạy tiếp từ 11 đến 20, KHÔNG quay về 1.'),
    ('003', 'Đổi số dòng mỗi trang', 'P0', 'Danh sách nhiều hơn 50 phiếu.',
     '1. Đang ở trang 3, đổi Số dòng/trang sang 50.',
     'Số dòng/trang: 50',
     '- Bảng hiện 50 dòng.\n- ⚠️ Quay về TRANG 1, ô thống kê ghi "Hiển thị 1–50 / N".'),
    ('004', 'Nút về đầu và về cuối', 'P1', 'Danh sách có ít nhất 5 trang.',
     '1. Bấm nút về cuối.\n2. Bấm nút về đầu.',
     '—',
     '- Về cuối: hiện trang cuối, ô thống kê ghi đúng khoảng cuối.\n'
     '- Về đầu: quay lại trang 1.'),
    ('005', 'Đổi trang giữ nguyên bộ lọc', 'P0', 'Đang lọc Trạng thái = Đã duyệt, nhiều trang.',
     '1. Chuyển sang trang 2.',
     '—',
     '- ⚠️ Bộ lọc vẫn được giữ, mọi dòng ở trang 2 vẫn là Đã duyệt.\n'
     '- N không đổi.'),
    ('006', 'Đổi bộ lọc thì quay về trang 1', 'P0', 'Đang ở trang 3.',
     '1. Đổi ô lọc Trạng thái sang một giá trị khác.',
     '—',
     '- Danh sách quay về trang 1 với kết quả mới.'),
    ('007', 'Sắp xếp theo Mã phiếu', 'P0', 'Danh sách có nhiều phiếu.',
     '1. Bấm tiêu đề cột Mã phiếu (lần 1).\n2. Bấm lại (lần 2).',
     '—',
     '- Lần 1: sắp xếp tăng dần theo mã phiếu.\n'
     '- Lần 2: sắp xếp GIẢM DẦN.\n- Danh sách quay về trang 1 sau mỗi lần đổi.'),
    ('008', 'Sắp xếp theo Ngày tạo', 'P0', 'Danh sách có nhiều phiếu.',
     '1. Bấm tiêu đề cột Ngày tạo hai lần.',
     '—',
     '- Sắp xếp đúng tăng dần rồi giảm dần theo ngày giờ lập phiếu.'),
    ('009', 'Sắp xếp theo Ngày duyệt', 'P1', 'Có cả phiếu đã duyệt và chưa duyệt.',
     '1. Bấm tiêu đề cột Ngày duyệt.',
     '—',
     '- Sắp xếp đúng theo ngày duyệt.\n'
     '- Phiếu chưa duyệt (ô trống) không gây lỗi hiển thị.'),
    ('010', 'Các cột khác không sắp xếp được', 'P2', 'Đang ở màn danh sách.',
     '1. Quan sát tiêu đề các cột.',
     '—',
     '- Chỉ ba cột Mã phiếu, Ngày tạo, Ngày duyệt có biểu tượng sắp xếp.\n'
     '- Bấm vào tiêu đề các cột khác không làm gì.'),
    ('011', 'Sắp xếp giữ nguyên khi đổi trang', 'P1', 'Đang sắp xếp giảm dần theo Ngày tạo.',
     '1. Chuyển sang trang 2.',
     '—',
     '- Thứ tự sắp xếp tiếp tục đúng, không bị đảo lại.'),
    ('012', 'Tuỳ chỉnh cột — bật cột đang ẩn', 'P0', 'Đang ở màn danh sách.',
     '1. Bấm biểu tượng cấu hình cột.\n2. Tích cột Ghi chú.\n3. Bấm Lưu.',
     '—',
     '- Cửa sổ có tiêu đề "Tuỳ chỉnh cột".\n'
     '- Sau khi lưu, bảng hiện thêm cột Ghi chú với nội dung đúng của từng phiếu.'),
    ('013', 'Tuỳ chỉnh cột — ba cột bị khóa', 'P0', 'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Thử bỏ tích cột STT, Mã phiếu và Hành động.',
     '—',
     '- Ba cột này có biểu tượng ổ khóa, không bỏ tích được.\n'
     '- Không có tay kéo để đổi vị trí.'),
    ('014', 'Tuỳ chỉnh cột — tắt cột đang hiện', 'P1', 'Cột Người cập nhật đang hiển thị.',
     '1. Mở Tuỳ chỉnh cột.\n2. Bỏ tích Người cập nhật.\n3. Bấm Lưu.',
     '—',
     '- Bảng không còn cột Người cập nhật.\n- Các cột khác giữ nguyên vị trí.'),
    ('015', 'Tuỳ chỉnh cột — Đóng không lưu', 'P2', 'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Bỏ tích một cột.\n2. Bấm Đóng.',
     '—',
     '- Bảng giữ nguyên như trước, cột không bị ẩn.'),
    ('016', 'Cấu hình cột lưu theo người dùng', 'P1', 'Tài khoản A đã bật cột Ghi chú.',
     '1. Đăng nhập bằng tài khoản B.\n2. Quan sát bảng.',
     '—',
     '- Tài khoản B vẫn thấy cấu hình mặc định, không bị ảnh hưởng bởi A.'),
    ('017', 'Cấu hình cột còn nguyên sau khi thoát và vào lại', 'P1',
     'Vừa bật cột Phòng ban và lưu.',
     '1. Chuyển sang màn khác rồi quay lại màn Yêu cầu gia hạn hàng giữ.',
     '—',
     '- Cột Phòng ban vẫn đang hiển thị.'),
    ('018', 'Bảng cuộn ngang khi bật nhiều cột', 'P2', 'Đã bật cả 3 cột ẩn.',
     '1. Cuộn ngang bảng.',
     '—',
     '- Có thanh cuộn ngang ở cả trên và dưới bảng.\n'
     '- Cột STT, Mã phiếu và Hành động vẫn dính khi cuộn.'),
]

# ============================================================== IV
S4 = [
    ('001', 'Mở màn lập phiếu', 'P0',
     'Tài khoản đang giữ 119 lô hàng có hạn giữ trong 7 ngày tới.',
     '1. Bấm nút Tạo mới ở màn danh sách.',
     '—',
     '- Tiêu đề màn ghi "Thêm yêu cầu gia hạn hàng giữ".\n'
     '- Khối Thông tin chung có ô Ghi chú với dấu sao đỏ.\n'
     '- Góc phải khối ghi tên người lập và ngày hôm nay.\n'
     '- Bảng Chi tiết đã tự nạp sẵn các lô sắp hết hạn, KHÔNG có nút thêm dòng.'),
    ('002', 'Bảng Chi tiết chỉ nạp lô sắp hết hạn', 'P0',
     'Tài khoản đang giữ 200 lô, trong đó 119 lô có hạn giữ trước "hôm nay + 7 ngày", '
     '81 lô còn hạn dài hơn.',
     '1. Mở màn lập phiếu.\n2. Đếm số dòng ở bảng Chi tiết.',
     '—',
     '- Bảng có đúng 119 dòng.\n'
     '- ⚠️ 81 lô còn hạn dài KHÔNG xuất hiện — đây là đúng thiết kế, không phải thiếu dữ liệu.'),
    ('003', 'Không có lô nào sắp hết hạn', 'P0',
     'Tài khoản không giữ lô nào có hạn trong 7 ngày tới.',
     '1. Bấm Tạo mới.',
     '—',
     '- Bảng Chi tiết trống, hiện câu giải thích: không có lô hàng giữ nào sắp hết hạn nên chưa '
     'lập được phiếu, kèm ngày mốc.\n'
     '- ⚠️ Không được để trống trơn không giải thích.'),
    ('004', 'Chỉ hiện lô của chính người lập', 'P0',
     'Tài khoản A và B đều đang giữ hàng sắp hết hạn.',
     '1. Đăng nhập bằng A, mở màn lập phiếu.\n2. Đối chiếu danh sách lô với dữ liệu hàng giữ '
     'của A và của B.',
     '—',
     '- Chỉ có lô do A đứng tên giữ.\n- Không có lô nào của B.'),
    ('005', 'Đủ cột ở bảng Chi tiết', 'P0', 'Đang ở màn lập phiếu, bảng có dữ liệu.',
     '1. Đọc tiêu đề các cột.',
     '—',
     '- Có đủ: STT, Cần gia hạn (ô tích), Tên hàng hóa, Khách hàng, Hợp đồng, ĐVT, Có thể giữ, '
     'Số lượng (gồm hai cột con Đang giữ và Cần gia hạn), Ngày bắt đầu giữ, Hạn giữ hiện tại, '
     'Hạn giữ mới, Lịch sử.\n'
     '- Tiêu đề "Số lượng" gộp trên hai cột Đang giữ và Cần gia hạn.'),
    ('006', 'Ô tích Cần gia hạn mở khóa hai ô nhập', 'P0', 'Đang ở màn lập phiếu.',
     '1. Quan sát dòng 1 khi chưa tích.\n2. Tích ô Cần gia hạn ở dòng 1.',
     '—',
     '- Khi chưa tích: ô Số lượng và ô Hạn giữ mới bị khóa, dòng bị làm mờ.\n'
     '- Sau khi tích: hai ô mở khóa, ô Số lượng được điền sẵn bằng đúng số ở cột Đang giữ.'),
    ('007', 'Bỏ tích thì khóa lại hai ô', 'P1', 'Dòng 1 đang được tích và đã nhập số lượng.',
     '1. Bỏ tích ô Cần gia hạn ở dòng 1.',
     '—',
     '- Hai ô Số lượng và Hạn giữ mới bị khóa lại, dòng làm mờ.\n'
     '- Dòng này sẽ không được gửi đi khi lưu.'),
    ('008', 'Ô ĐVT bị khóa và có giải thích', 'P1', 'Đang ở màn lập phiếu.',
     '1. Rê chuột vào biểu tượng chữ i cạnh tiêu đề cột ĐVT.',
     '—',
     '- Hiện lời giải thích: hàng giữ luôn ghi theo đơn vị cơ bản nên không chọn được đơn vị '
     'khác; muốn đổi thì sửa ở danh mục hàng hóa.\n'
     '- ⚠️ Ô khóa phải có biểu tượng giải thích, không được để trống không lý do.'),
    ('009', 'Phân biệt cột Có thể giữ và Đang giữ', 'P0',
     'Một hàng hóa có tồn kho khả dụng 49 và lô đang giữ 2.',
     '1. Rê chuột vào biểu tượng chữ i cạnh tiêu đề cột Có thể giữ.\n2. Đọc số ở hai cột.',
     '—',
     '- Lời giải thích nêu rõ "Có thể giữ" là tồn kho còn có thể giữ tiếp, khác với "Đang giữ" '
     'là số của chính lô đang xem.\n'
     '- Cột Có thể giữ = 49, cột Đang giữ = 2, hai số độc lập với nhau.'),
    ('010', 'Lưu nháp thành công', 'P0',
     'Đang ở màn lập phiếu, có ít nhất 1 lô sắp hết hạn.',
     '1. Nhập Ghi chú.\n2. Tích 1 dòng, để nguyên số lượng điền sẵn.\n'
     '3. Chọn Hạn giữ mới hợp lệ.\n4. Bấm Lưu nháp.',
     'Ghi chú: Khách xin lùi lịch nhận hàng; Hạn giữ mới: hôm nay + 10 ngày',
     '- Hiện thông báo lưu thành công.\n- Quay về màn danh sách.\n'
     '- Phiếu mới nằm đầu danh sách với trạng thái Đang tạo (nhãn xám) và mã dạng PGHHG-NNNNN.'),
    ('011', 'Gửi duyệt thành công', 'P0', 'Đang ở màn lập phiếu, dữ liệu hợp lệ.',
     '1. Nhập đủ dữ liệu.\n2. Bấm Gửi duyệt.',
     'Ghi chú: Chờ khách chốt hợp đồng; Hạn giữ mới: hôm nay + 15 ngày',
     '- Hiện thông báo thành công, quay về danh sách.\n'
     '- Phiếu mới có trạng thái Chờ TP duyệt (nhãn cam).\n'
     '- Trưởng phòng phụ trách phòng ban của người lập nhận được thông báo.'),
    ('012', 'Lưu và tiếp tục', 'P1', 'Đang ở màn lập phiếu, dữ liệu hợp lệ.',
     '1. Nhập đủ dữ liệu.\n2. Bấm Lưu và tiếp tục.',
     '—',
     '- Phiếu được lưu ở trạng thái Đang tạo.\n'
     '- ⚠️ KHÔNG quay về danh sách; màn hình được làm mới để lập phiếu tiếp theo.\n'
     '- Ô Ghi chú và các dòng tích đã được xóa sạch.'),
    ('013', 'Nút Lưu và tiếp tục chỉ có ở màn Tạo mới', 'P2',
     'Có 1 phiếu ở trạng thái Đang tạo do chính mình lập.',
     '1. Mở màn Sửa của phiếu đó.\n2. Quan sát các nút cuối màn.',
     '—',
     '- Màn Sửa chỉ có Lưu nháp, Gửi duyệt và Quay lại.\n- KHÔNG có nút Lưu và tiếp tục.'),
    ('014', 'Đính kèm tệp hợp lệ', 'P1', 'Đang ở màn lập phiếu.',
     '1. Bấm nút Chọn tệp.\n2. Chọn một tệp PDF dung lượng 2 MB.',
     'Tệp: bien-ban-lam-viec.pdf (2 MB)',
     '- Tên tệp hiện trong danh sách đính kèm kèm nút gỡ.\n'
     '- Dòng hướng dẫn ghi rõ nhận PDF, ảnh, Word, Excel, mỗi tệp tối đa 13 MB.'),
    ('015', 'Đính kèm nhiều tệp', 'P2', 'Đang ở màn lập phiếu.',
     '1. Đính kèm lần lượt 3 tệp khác nhau.',
     'Tệp: 1 ảnh, 1 Word, 1 Excel',
     '- Cả 3 tệp đều nằm trong danh sách, mỗi tệp có nút gỡ riêng.'),
    ('016', 'Gỡ tệp đính kèm', 'P2', 'Đã đính kèm 2 tệp.',
     '1. Bấm nút gỡ ở tệp thứ nhất.',
     '—',
     '- Tệp thứ nhất biến mất khỏi danh sách, tệp thứ hai còn nguyên.'),
    ('017', 'Xem lịch sử biến động của một lô', 'P1', 'Đang ở màn lập phiếu, bảng có dữ liệu.',
     '1. Bấm biểu tượng đồng hồ ở cột Lịch sử của một dòng.',
     '—',
     '- Mở cửa sổ lịch sử tăng giảm của đúng lô hàng giữ đó.\n'
     '- Cửa sổ hiển thị tên hàng hóa và nhân viên giữ tương ứng.'),
    ('018', 'Cảnh báo khi rời màn lúc chưa lưu', 'P0', 'Đang ở màn lập phiếu.',
     '1. Nhập Ghi chú.\n2. Bấm nút Quay lại.',
     'Ghi chú: test',
     '- Phần mềm hỏi xác nhận rời khỏi trang.\n'
     '- Chọn ở lại: giữ nguyên dữ liệu đã nhập.\n- Chọn rời đi: bỏ mọi thay đổi.'),
    ('019', 'Không cảnh báo khi chưa nhập gì', 'P2', 'Vừa mở màn lập phiếu.',
     '1. Bấm ngay nút Quay lại.',
     '—',
     '- Quay về màn danh sách luôn, không hỏi xác nhận.'),
    ('020', 'Mã phiếu sinh tự động không trùng', 'P0',
     'Vừa lập liên tiếp 3 phiếu mới.',
     '1. Lập 3 phiếu liên tiếp.\n2. Xem mã của 3 phiếu ở danh sách.',
     '—',
     '- Ba mã khác nhau, theo dạng PGHHG kèm 5 chữ số.\n'
     '- Không có mã nào trùng với phiếu đã có.'),
    ('021', 'Màn Tạo mới không có ô Mã phiếu và Trạng thái', 'P1', 'Đang ở màn lập phiếu.',
     '1. Quan sát khối Thông tin chung.',
     '—',
     '- ⚠️ Chỉ có ô Ghi chú; KHÔNG có ô Mã phiếu, Trạng thái, Phòng ban yêu cầu — các ô này '
     'chỉ xuất hiện ở màn Sửa và màn Chi tiết.'),
]

# ============================================================== V
S5 = [
    ('001', 'Nút Sửa chỉ hiện với phiếu nháp của mình', 'P0',
     'Tài khoản A có: phiếu 1 Đang tạo do A lập, phiếu 2 Chờ TP duyệt do A lập, '
     'phiếu 3 Đang tạo do B lập.',
     '1. Đăng nhập bằng A.\n2. Xem cột Hành động của từng phiếu.',
     '—',
     '- Phiếu 1: có biểu tượng Sửa.\n- Phiếu 2: KHÔNG có.\n'
     '- Phiếu 3: không xuất hiện trong danh sách của A.'),
    ('002', 'Mở màn Sửa từ danh sách', 'P0', 'Có phiếu Đang tạo do chính mình lập.',
     '1. Bấm biểu tượng bút chì ở cột Hành động.',
     '—',
     '- Tiêu đề màn ghi "Sửa yêu cầu gia hạn hàng giữ".\n'
     '- Ô Mã phiếu, Trạng thái, Phòng ban yêu cầu hiển thị đúng dữ liệu và bị khóa.'),
    ('003', 'Dữ liệu đã lưu được nạp lại đúng', 'P0',
     'Phiếu Đang tạo đã chọn 3 dòng hàng, mỗi dòng có số lượng và hạn giữ mới riêng.',
     '1. Mở màn Sửa của phiếu đó.',
     '—',
     '- Ghi chú hiện đúng nội dung đã lưu.\n'
     '- Đúng 3 dòng được tích sẵn, số lượng và hạn giữ mới đúng như đã lưu.\n'
     '- Các dòng khác vẫn hiện nhưng chưa tích.'),
    ('004', 'Sửa Ghi chú rồi lưu nháp', 'P0', 'Đang ở màn Sửa.',
     '1. Đổi nội dung Ghi chú.\n2. Bấm Lưu nháp.',
     'Ghi chú: Khách đã xác nhận lùi lịch sang tuần sau',
     '- Hiện thông báo thành công, quay về danh sách.\n'
     '- Mở lại phiếu thấy Ghi chú mới.\n- Lịch sử thay đổi ghi nhận mốc chỉnh sửa.'),
    ('005', 'Bỏ tích một dòng rồi lưu', 'P0', 'Phiếu đang có 3 dòng được tích.',
     '1. Bỏ tích dòng thứ 3.\n2. Bấm Lưu nháp.\n3. Mở lại phiếu.',
     '—',
     '- Phiếu chỉ còn 2 dòng được chọn.\n'
     '- Lịch sử thay đổi ghi rõ dòng hàng đã bị bỏ khỏi phiếu.'),
    ('006', 'Thêm dòng mới vào phiếu đang sửa', 'P1',
     'Phiếu có 2 dòng được tích; bảng còn nhiều lô chưa tích.',
     '1. Tích thêm 1 dòng.\n2. Nhập số lượng và hạn giữ mới.\n3. Bấm Lưu nháp.',
     'Số lượng: 1; Hạn giữ mới: hôm nay + 12 ngày',
     '- Phiếu có 3 dòng sau khi lưu.\n- Lịch sử thay đổi ghi nhận dòng hàng được thêm.'),
    ('007', 'Sửa rồi Gửi duyệt', 'P0', 'Phiếu Đang tạo do chính mình lập.',
     '1. Mở màn Sửa, chỉnh dữ liệu.\n2. Bấm Gửi duyệt.',
     '—',
     '- Phiếu chuyển sang trạng thái Chờ TP duyệt.\n'
     '- Nút Sửa và Xóa của phiếu này biến mất khỏi cột Hành động.'),
    ('008', 'Sửa phiếu bị từ chối rồi gửi lại', 'P0',
     'Phiếu đã bị Trưởng phòng từ chối, đang ở trạng thái Đang tạo và có Lý do từ chối.',
     '1. Mở màn Sửa.\n2. Chỉnh theo yêu cầu.\n3. Bấm Gửi duyệt.',
     '—',
     '- Sửa được bình thường.\n- Phiếu quay lại trạng thái Chờ TP duyệt.\n'
     '- Lịch sử duyệt vẫn giữ dòng từ chối cũ để tra cứu.'),
    ('009', 'Mở màn Sửa của phiếu đã gửi duyệt bằng đường dẫn', 'P0',
     'Phiếu đang ở trạng thái Chờ KT duyệt do chính mình lập.',
     '1. Gõ thẳng đường dẫn màn sửa của phiếu đó lên thanh địa chỉ.',
     '—',
     '- Phần mềm không cho vào màn sửa, báo lỗi hoặc chuyển về màn chi tiết.\n'
     '- Nội dung phiếu không thay đổi.'),
    ('010', 'Cảnh báo rời màn Sửa khi chưa lưu', 'P1', 'Đang ở màn Sửa.',
     '1. Đổi Ghi chú.\n2. Bấm Quay lại.',
     '—',
     '- Phần mềm hỏi xác nhận rời khỏi trang.'),
    ('011', 'Sửa phiếu của người khác qua đường dẫn', 'P0',
     'Phiếu Đang tạo do tài khoản B lập.',
     '1. Đăng nhập bằng A.\n2. Gõ đường dẫn màn sửa của phiếu đó.',
     '—',
     '- Phần mềm từ chối, không hiển thị dữ liệu phiếu.'),
]

# ============================================================== VI
S6 = [
    ('001', 'Mở màn chi tiết', 'P0', 'Có phiếu trong phạm vi quyền.',
     '1. Bấm vào mã phiếu.',
     '—',
     '- Tiêu đề ghi "Chi tiết yêu cầu gia hạn hàng giữ: <mã phiếu>".\n'
     '- Có đủ các khối: Thông tin chung, File đính kèm, Chi tiết, Lịch sử duyệt (nếu đã có ai '
     'duyệt), Lịch sử thay đổi.'),
    ('002', 'Mọi ô ở chế độ chỉ đọc với người không phải cấp duyệt hiện tại', 'P0',
     'Tài khoản không có quyền duyệt, mở một phiếu Chờ TP duyệt.',
     '1. Thử bấm vào ô Ghi chú và ô Hạn giữ mới.',
     '—',
     '- Không sửa được ô nào.\n- Cột "Cần gia hạn" (ô tích) KHÔNG hiển thị.\n'
     '- Cuối màn chỉ có nút In và Quay lại.'),
    ('003', 'Người đúng cấp duyệt được sửa Hạn giữ mới', 'P0',
     'Tài khoản có quyền Ban giám đốc duyệt hàng giữ; phiếu đang ở Chờ BGĐ duyệt cùng công ty.',
     '1. Mở phiếu.\n2. Quan sát cột Cần gia hạn và cột Hạn giữ mới.',
     '—',
     '- Cột Cần gia hạn (ô tích) hiển thị và bỏ tích được.\n'
     '- Ô Hạn giữ mới mở khóa, chọn lại ngày được.\n'
     '- ⚠️ Ô Số lượng vẫn chỉ đọc, KHÔNG sửa được.'),
    ('004', 'Khối Lịch sử duyệt hiển thị đủ ba cấp', 'P0',
     'Phiếu đã qua đủ ba cấp và đang ở trạng thái Đã duyệt.',
     '1. Mở phiếu, xem khối Lịch sử duyệt.',
     '—',
     '- Có ba dòng: Trưởng phòng, Ban giám đốc, Kế toán.\n'
     '- Mỗi dòng đủ Kết quả, Người thực hiện, Thời gian, Ghi chú.\n'
     '- Cả ba dòng có nhãn xanh "Đã duyệt".'),
    ('005', 'Dòng duyệt không ghi chú vẫn hiển thị', 'P0',
     'Có phiếu mà cấp duyệt đã duyệt nhưng để trống ô ghi chú.',
     '1. Mở phiếu, xem khối Lịch sử duyệt.',
     '—',
     '- ⚠️ Dòng đó VẪN hiển thị, chỉ để trống cột Ghi chú.\n'
     '- Không được mất dòng chỉ vì không có ghi chú.'),
    ('006', 'Phân biệt dòng duyệt và dòng từ chối', 'P0',
     'Phiếu từng bị Trưởng phòng từ chối, sau đó được gửi lại và duyệt.',
     '1. Mở phiếu, xem khối Lịch sử duyệt.',
     '—',
     '- Dòng từ chối có nhãn ĐỎ ghi "Từ chối" và có lý do ở cột Ghi chú.\n'
     '- Dòng duyệt có nhãn XANH ghi "Đã duyệt".\n'
     '- ⚠️ Hai dòng phải phân biệt được bằng mắt, không chỉ khác nhau ở giờ.'),
    ('007', 'Phiếu chưa qua bước nào thì không có khối Lịch sử duyệt', 'P1',
     'Phiếu vừa gửi duyệt, chưa ai xử lý.',
     '1. Mở phiếu.',
     '—',
     '- Không hiển thị khối Lịch sử duyệt.'),
    ('008', 'Xem tệp đính kèm', 'P1', 'Phiếu có 1 tệp đính kèm.',
     '1. Bấm vào tên tệp ở khối File đính kèm.',
     '—',
     '- Tệp mở ở tab mới, xem được nội dung.'),
    ('009', 'Phiếu không có tệp đính kèm', 'P2', 'Phiếu không đính kèm gì.',
     '1. Mở phiếu.',
     '—',
     '- Khối File đính kèm hiện dòng "Chưa có tệp đính kèm".'),
    ('010', 'Nút cuối màn khớp với cột Hành động ngoài danh sách', 'P0',
     'Một phiếu Đang tạo do chính mình lập.',
     '1. Đếm nút ở cột Hành động của phiếu ngoài danh sách.\n2. Mở phiếu, đếm nút cuối màn.',
     '—',
     '- ⚠️ Số nút khớp nhau: danh sách có Sửa, Xóa, In, Lịch sử thì màn chi tiết cũng phải có '
     'Sửa, Xóa và In.\n'
     '- Không có tình trạng ngoài danh sách ẩn nút mà trong chi tiết vẫn hiện.'),
    ('011', 'Mở phiếu nháp của người khác bằng đường dẫn', 'P0',
     'Phiếu Đang tạo do tài khoản B lập; tài khoản A có quyền xem theo tổng công ty.',
     '1. Đăng nhập bằng A.\n2. Gõ đường dẫn màn chi tiết của phiếu đó.',
     '—',
     '- Phần mềm báo không có quyền xem phiếu này.\n- Không hiển thị nội dung phiếu.'),
    ('012', 'Mở phiếu bằng mã không tồn tại', 'P1', 'Đang đăng nhập.',
     '1. Gõ đường dẫn màn chi tiết với một mã số không có thật.',
     '—',
     '- Phần mềm báo không tìm thấy dữ liệu, không treo trang.'),
]

# ============================================================== VII
S7 = [
    ('001', 'Trưởng phòng duyệt — phiếu không phải trình Ban giám đốc', 'P0',
     'Phiếu X ở trạng thái Chờ TP duyệt, các dòng hàng đều gắn hợp đồng đã thu đủ tỉ lệ quy định. '
     'Tài khoản E có quyền Trưởng phòng duyệt hàng giữ và quản lý phòng của phiếu.',
     '1. Đăng nhập bằng E.\n2. Mở phiếu X.\n3. Bấm nút TP duyệt.',
     '—',
     '- Hiện thông báo "Yêu cầu đã được chuyển đến Kế toán.".\n'
     '- Phiếu chuyển thẳng sang trạng thái Chờ KT duyệt, BỎ QUA bước Ban giám đốc.\n'
     '- Khối Lịch sử duyệt có thêm dòng Trưởng phòng – Đã duyệt.\n'
     '- Quay về màn danh sách.'),
    ('002', 'Trưởng phòng duyệt — phiếu phải trình Ban giám đốc', 'P0',
     'Phiếu Y ở Chờ TP duyệt, có dòng hàng không gắn hợp đồng với tổng giá trị vượt hạn mức '
     'của công ty.',
     '1. Đăng nhập bằng E.\n2. Mở phiếu Y.\n3. Bấm TP duyệt.',
     '—',
     '- Hiện thông báo "Yêu cầu đã được chuyển đến Ban giám đốc.".\n'
     '- Phiếu chuyển sang trạng thái Chờ BGĐ duyệt.\n'
     '- Ban giám đốc nhận được thông báo.'),
    ('003', 'Ban giám đốc duyệt', 'P0',
     'Phiếu ở trạng thái Chờ BGĐ duyệt; tài khoản F có quyền Ban giám đốc duyệt hàng giữ cùng '
     'công ty.',
     '1. Mở phiếu.\n2. Bấm BGĐ duyệt.',
     '—',
     '- Hiện "Yêu cầu đã được chuyển đến Kế toán.".\n'
     '- Phiếu chuyển sang Chờ KT duyệt.\n'
     '- Lịch sử duyệt có thêm dòng Ban giám đốc – Đã duyệt.'),
    ('004', 'Kế toán duyệt — hàng giữ được chuyển sang hạn mới', 'P0',
     'Phiếu ở Chờ KT duyệt, có 1 dòng: hàng H, khách K, đang giữ 5, xin gia hạn 3, hạn giữ hiện '
     'tại 10/09/2026, hạn giữ mới 25/09/2026. Trước khi duyệt, lô hạn 10/09 có 5 và chưa có lô '
     'hạn 25/09.',
     '1. Ghi lại số lượng hai lô trước khi duyệt.\n2. Đăng nhập tài khoản có quyền Kế toán duyệt '
     'hàng giữ.\n3. Mở phiếu và bấm KT duyệt.\n4. Mở màn Danh sách hàng giữ kiểm tra lại.',
     'Số lượng gia hạn: 3',
     '- Hiện "Duyệt phiếu thành công.", phiếu chuyển sang Đã duyệt.\n'
     '- Lô hạn 10/09/2026 còn 2.\n'
     '- Xuất hiện lô mới hạn 25/09/2026 với số lượng 3, cùng nhân viên và cùng khách hàng K.\n'
     '- ⚠️ Lịch sử biến động của hàng hóa có ĐÚNG HAI dòng: một dòng trừ 3 và một dòng cộng 3.'),
    ('005', 'Kế toán duyệt khi lô đích đã tồn tại', 'P0',
     'Đã có sẵn lô hàng H, khách K, hạn 25/09/2026 với số lượng 4. Phiếu xin gia hạn 3 từ lô '
     'hạn 10/09/2026.',
     '1. Bấm KT duyệt.\n2. Kiểm tra lại hai lô.',
     '—',
     '- Lô hạn 25/09/2026 tăng từ 4 lên 7 (cộng dồn, KHÔNG tạo lô thứ hai).\n'
     '- Lô hạn 10/09/2026 giảm đúng 3.'),
    ('006', 'Ba bước trước không đụng tới hàng giữ', 'P0',
     'Phiếu ở Chờ TP duyệt với 1 dòng gia hạn 3.',
     '1. Ghi lại số lượng lô hàng giữ.\n2. Trưởng phòng duyệt.\n3. Ban giám đốc duyệt.\n'
     '4. Kiểm tra lại số lượng lô hàng giữ.',
     '—',
     '- ⚠️ Sau bước Trưởng phòng và Ban giám đốc, số lượng các lô KHÔNG đổi.\n'
     '- Chỉ sau bước Kế toán mới thay đổi.'),
    ('007', 'Người duyệt sửa Hạn giữ mới trước khi duyệt', 'P0',
     'Phiếu ở Chờ KT duyệt, hạn giữ mới đang là 25/09/2026.',
     '1. Mở phiếu.\n2. Đổi Hạn giữ mới sang 20/09/2026.\n3. Bấm KT duyệt.\n'
     '4. Kiểm tra lô hàng giữ.',
     'Hạn giữ mới: 20/09/2026',
     '- Lô mới được tạo với hạn 20/09/2026 chứ không phải 25/09/2026.\n'
     '- Lịch sử thay đổi ghi nhận việc đổi hạn giữ mới.'),
    ('008', 'Người duyệt bỏ tích một dòng trước khi duyệt', 'P0',
     'Phiếu có 3 dòng đều đang được tích, đang ở Chờ KT duyệt.',
     '1. Bỏ tích dòng thứ 2.\n2. Bấm KT duyệt.\n3. Kiểm tra hàng giữ.',
     '—',
     '- Chỉ dòng 1 và dòng 3 được chuyển sang hạn mới.\n'
     '- Lô của dòng 2 giữ nguyên số lượng và hạn cũ.'),
    ('009', 'Bỏ tích hết các dòng rồi duyệt', 'P0', 'Phiếu ở Chờ KT duyệt có 2 dòng.',
     '1. Bỏ tích cả 2 dòng.\n2. Bấm KT duyệt.',
     '—',
     '- Phần mềm báo "Phải giữ lại ít nhất 1 hàng hoá cần gia hạn thì mới duyệt được.".\n'
     '- Phiếu KHÔNG đổi trạng thái, hàng giữ không đổi.'),
    ('010', 'Hạn giữ mới trùng hạn giữ hiện tại', 'P1',
     'Phiếu có 1 dòng, hạn giữ mới được đặt trùng đúng hạn giữ hiện tại.',
     '1. Kế toán duyệt phiếu.\n2. Kiểm tra hàng giữ.',
     '—',
     '- Dòng đó bị bỏ qua, không phát sinh biến động hàng giữ.\n'
     '- Phiếu vẫn chuyển sang Đã duyệt.'),
    ('011', 'Duyệt sai cấp', 'P0',
     'Phiếu đang ở Chờ TP duyệt; tài khoản chỉ có quyền Kế toán duyệt hàng giữ.',
     '1. Mở phiếu.',
     '—',
     '- Nút KT duyệt KHÔNG hiển thị.\n'
     '- Dùng công cụ kiểm thử gọi thẳng chức năng duyệt: phần mềm báo không có quyền duyệt '
     'bước này, trạng thái phiếu không đổi.'),
    ('012', 'Trưởng phòng không quản lý phòng ban của phiếu', 'P0',
     'Tài khoản E có quyền Trưởng phòng duyệt hàng giữ nhưng không quản lý phòng ban của '
     'phiếu Z (Chờ TP duyệt, cùng công ty).',
     '1. Mở phiếu Z.',
     '—',
     '- Nút TP duyệt và Từ chối KHÔNG hiển thị.\n'
     '- ⚠️ Chỉ có quyền là chưa đủ, phải quản lý đúng phòng ban ghi trên phiếu.'),
    ('013', 'Hai người cùng duyệt một phiếu', 'P0',
     'Phiếu ở Chờ KT duyệt; hai kế toán cùng mở phiếu trên hai máy.',
     '1. Máy 1 bấm KT duyệt thành công.\n2. Máy 2 bấm KT duyệt (chưa tải lại trang).',
     '—',
     '- Máy 2 nhận thông báo "Phiếu không ở trạng thái chờ duyệt.".\n'
     '- ⚠️ Hàng giữ chỉ bị trừ MỘT lần, không bị trừ hai lần.'),
    ('014', 'Từ chối ở cấp Trưởng phòng', 'P0', 'Phiếu ở Chờ TP duyệt.',
     '1. Bấm nút Từ chối.\n2. Nhập lý do.\n3. Xác nhận.',
     'Lý do từ chối: Khách chưa thanh toán đợt 1, chưa đồng ý gia hạn',
     '- Cửa sổ có tiêu đề "Từ chối yêu cầu gia hạn hàng giữ" và hiển thị mã phiếu.\n'
     '- Sau khi xác nhận: phiếu quay về trạng thái Đang tạo (nhãn xám).\n'
     '- Cột Lý do từ chối ngoài danh sách hiện đúng nội dung vừa nhập.\n'
     '- Người lập nhận được thông báo.'),
    ('015', 'Từ chối bỏ trống lý do', 'P0', 'Cửa sổ Từ chối đang mở.',
     '1. Không nhập gì.\n2. Bấm nút xác nhận.',
     'Lý do từ chối: (bỏ trống)',
     '- Phần mềm báo "Bắt buộc phải nhập lý do từ chối" ngay dưới ô.\n'
     '- ⚠️ Cửa sổ KHÔNG đóng, phiếu không đổi trạng thái.'),
    ('016', 'Từ chối với lý do quá dài', 'P1', 'Cửa sổ Từ chối đang mở.',
     '1. Nhập lý do dài hơn 255 ký tự.\n2. Bấm xác nhận.',
     'Lý do từ chối: chuỗi 260 ký tự',
     '- Phần mềm báo "Không được vượt quá 255 ký tự" hoặc ô không cho nhập quá giới hạn.\n'
     '- Phiếu không đổi trạng thái nếu vượt giới hạn.'),
    ('017', 'Từ chối ở cấp Kế toán', 'P0', 'Phiếu ở Chờ KT duyệt.',
     '1. Kế toán bấm Từ chối, nhập lý do và xác nhận.\n2. Kiểm tra hàng giữ.',
     'Lý do từ chối: Hàng đã có khách khác đặt',
     '- Phiếu về trạng thái Đang tạo.\n'
     '- ⚠️ Hàng giữ KHÔNG bị thay đổi vì phiếu chưa từng được duyệt xong.\n'
     '- Lịch sử duyệt ghi dòng Kế toán – Từ chối với nhãn đỏ.'),
    ('018', 'Từ chối từ cột Hành động ngoài danh sách', 'P1',
     'Phiếu đang chờ chính mình duyệt.',
     '1. Bấm biểu tượng dấu nhân ở cột Hành động.\n2. Nhập lý do và xác nhận.',
     'Lý do từ chối: Sai số lượng đề nghị',
     '- Cửa sổ Từ chối mở ngay trên màn danh sách.\n'
     '- Sau khi xác nhận, danh sách tự tải lại và phiếu đã đổi trạng thái.'),
    ('019', 'Người lập sửa và gửi lại sau khi bị từ chối', 'P0',
     'Phiếu vừa bị từ chối, đang ở Đang tạo.',
     '1. Người lập mở phiếu.\n2. Bấm Sửa, chỉnh số lượng.\n3. Bấm Gửi duyệt.',
     '—',
     '- Phiếu quay lại Chờ TP duyệt và đi lại từ đầu quy trình duyệt.\n'
     '- Lịch sử duyệt vẫn giữ dòng từ chối cũ.'),
    ('020', 'Đóng cửa sổ Từ chối không thực hiện gì', 'P2', 'Cửa sổ Từ chối đang mở.',
     '1. Nhập lý do.\n2. Bấm dấu nhân ở góc cửa sổ để đóng.',
     '—',
     '- Cửa sổ đóng, phiếu giữ nguyên trạng thái.\n- Nội dung vừa nhập không được lưu.'),
]

# ============================================================== VIII
S8 = [
    ('001', 'Xóa phiếu nháp của mình', 'P0', 'Phiếu Đang tạo do chính mình lập.',
     '1. Bấm biểu tượng thùng rác ở cột Hành động.\n2. Đọc nội dung hộp thoại.\n3. Bấm Xóa.',
     '—',
     '- Hộp thoại có tiêu đề "Xác nhận xóa" và ghi rõ mã phiếu.\n'
     '- Sau khi xác nhận: hiện "Xóa thành công.", danh sách tải lại và không còn phiếu đó.\n'
     '- Tổng N giảm 1.'),
    ('002', 'Hủy thao tác xóa', 'P0', 'Hộp thoại xác nhận xóa đang mở.',
     '1. Bấm nút Hủy.',
     '—',
     '- Hộp thoại đóng, phiếu vẫn còn nguyên trong danh sách.'),
    ('003', 'Nút Xóa ẩn với phiếu đã gửi duyệt', 'P0', 'Phiếu ở Chờ TP duyệt do chính mình lập.',
     '1. Xem cột Hành động.\n2. Mở phiếu, xem nút cuối màn.',
     '—',
     '- Không có nút Xóa ở cả hai nơi.\n- ⚠️ Nút bị ẩn hẳn, không hiện nút xám.'),
    ('004', 'Nút Xóa ẩn với phiếu của người khác', 'P0',
     'Phiếu Chờ KT duyệt do người khác lập, mình có quyền xem.',
     '1. Xem cột Hành động của phiếu đó.',
     '—',
     '- Không có nút Xóa.'),
    ('005', 'Xóa phiếu đã duyệt bằng cách gọi thẳng chức năng', 'P0',
     'Phiếu ở trạng thái Đã duyệt.',
     '1. Dùng công cụ kiểm thử gọi thẳng chức năng xóa phiếu đó.',
     '—',
     '- Phần mềm từ chối.\n- ⚠️ Phiếu vẫn còn và hàng giữ đã ghi không bị ảnh hưởng.'),
    ('006', 'Xóa phiếu rồi mở lại bằng đường dẫn cũ', 'P1', 'Vừa xóa một phiếu.',
     '1. Gõ đường dẫn màn chi tiết của phiếu vừa xóa.',
     '—',
     '- Phần mềm báo không tìm thấy dữ liệu, không treo trang.'),
]

# ============================================================== IX
S9 = [
    ('001', 'In một phiếu từ cột Hành động', 'P0', 'Có phiếu trong phạm vi quyền.',
     '1. Bấm biểu tượng máy in ở cột Hành động.',
     '—',
     '- Mở tab mới, tiêu đề tab ghi "In phiếu yêu cầu gia hạn hàng giữ".\n'
     '- Bản xem trước hiển thị khung tờ giấy A4 dọc trên nền xám, nút In canh phải mép giấy.'),
    ('002', 'Nội dung bản in phiếu', 'P0', 'Phiếu đã duyệt đủ ba cấp, có 3 dòng hàng.',
     '1. Mở bản in của phiếu đó.',
     '—',
     '- Phần đầu có logo và thông tin công ty GHI TRÊN PHIẾU.\n'
     '- Tiêu đề "PHIẾU YÊU CẦU GIA HẠN HÀNG GIỮ", số phiếu và ngày tạo.\n'
     '- Khối thông tin: Người yêu cầu, Phòng ban, Trạng thái, Ghi chú.\n'
     '- Bảng hàng hóa đủ cột STT, Tên hàng hóa, Model, Mã hàng hóa, Khách hàng, Hợp đồng, ĐVT, '
     'SL gia hạn, Hạn giữ hiện tại, Hạn giữ mới và dòng Tổng cộng.\n'
     '- Bảng lịch sử duyệt đủ 3 dòng.\n'
     '- Khối ký có 4 ô: Người lập, Trưởng phòng, Ban giám đốc, Kế toán.'),
    ('003', 'Bản in lấy đúng công ty của phiếu', 'P0',
     'Người đăng nhập thuộc công ty 1; phiếu thuộc công ty 4 (Tân Phát ETEK Sài Gòn).',
     '1. Mở bản in của phiếu đó.',
     '—',
     '- ⚠️ Phần đầu chứng từ hiển thị thông tin công ty 4, KHÔNG phải công ty của người đang in.'),
    ('004', 'Dòng Tổng cộng trên bản in', 'P1',
     'Phiếu có 3 dòng với SL gia hạn lần lượt 3, 1, 1.',
     '1. Mở bản in, xem dòng Tổng cộng.',
     '—',
     '- Dòng Tổng cộng ghi 5.'),
    ('005', 'Bản in giữ dòng duyệt không có ghi chú', 'P0',
     'Phiếu có cấp duyệt để trống ghi chú.',
     '1. Mở bản in, xem bảng lịch sử duyệt.',
     '—',
     '- ⚠️ Dòng đó vẫn được in, chỉ để trống cột Ghi chú.'),
    ('006', 'In danh sách theo bộ lọc', 'P0', 'Đang lọc Trạng thái = Đã duyệt, còn 1.244 phiếu.',
     '1. Bấm nút In trên thanh công cụ.',
     '—',
     '- Mở tab mới, tiêu đề "In danh sách yêu cầu gia hạn hàng giữ".\n'
     '- Dòng "Tổng số phiếu" ghi đúng 1.244.\n'
     '- ⚠️ In toàn bộ phiếu khớp bộ lọc, không chỉ 10 dòng của trang đang xem.'),
    ('007', 'Bản in danh sách dùng khổ ngang', 'P1', 'Đang ở bản in danh sách.',
     '1. Quan sát khung tờ giấy.',
     '—',
     '- Tờ giấy nằm ngang, đủ chỗ cho 7 cột: STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, '
     'Người duyệt, Ngày duyệt.'),
    ('008', 'Mở cửa sổ chọn trường xuất Excel', 'P0', 'Đang ở màn danh sách.',
     '1. Bấm nút Xuất Excel.',
     '—',
     '- Cửa sổ "Chọn trường xuất Excel" mở ra.\n'
     '- Mặc định đang chọn 11/11 trường.\n'
     '- Có dòng xem trước thứ tự cột và hai nút Chọn tất cả / Bỏ chọn hết.'),
    ('009', 'Xuất Excel đủ trường', 'P0', 'Cửa sổ chọn trường đang mở, đang lọc 12 phiếu.',
     '1. Giữ nguyên 11 trường.\n2. Bấm Xuất file.\n3. Mở tệp vừa tải.',
     '—',
     '- Hiện thông báo "Xuất Excel thành công" và cửa sổ đóng lại.\n'
     '- Tệp có đúng 12 dòng dữ liệu.\n'
     '- Có đủ 11 cột: Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, '
     'Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối.'),
    ('010', 'Thứ tự cột theo thứ tự chọn', 'P0', 'Cửa sổ chọn trường đang mở.',
     '1. Bấm Bỏ chọn hết.\n2. Chọn lần lượt: Trạng thái, Mã phiếu, Người tạo.\n'
     '3. Bấm Xuất file.',
     'Trường xuất: Trạng thái, Mã phiếu, Người tạo',
     '- Tệp có đúng 3 cột theo THỨ TỰ đã chọn: Trạng thái, Mã phiếu, Người tạo.'),
    ('011', 'Xuất Excel theo bộ lọc đang áp', 'P0',
     'Đang lọc Người tạo = Nguyễn Văn Mạnh, còn 12 phiếu, đang xem trang 1 (10 dòng).',
     '1. Bấm Xuất Excel và xuất file.\n2. Đếm số dòng trong tệp.',
     '—',
     '- ⚠️ Tệp có đủ 12 dòng, không phải 10 dòng của trang đang xem.\n'
     '- Mọi dòng đều có Người tạo là Nguyễn Văn Mạnh.'),
    ('012', 'Nút Xuất file bị khóa trong lúc xuất', 'P1', 'Danh sách lớn (trên 1.000 phiếu).',
     '1. Bấm Xuất file và quan sát nút trong lúc chờ.',
     '—',
     '- Nút bị khóa, không bấm lại được cho tới khi xong.\n- Không tạo hai tệp trùng.'),
    ('013', 'Đóng cửa sổ chọn trường mà không xuất', 'P2', 'Cửa sổ đang mở.',
     '1. Bấm nút Đóng.',
     '—',
     '- Cửa sổ đóng, không có tệp nào được tải về.'),
    ('014', 'Xuất Excel khi danh sách rỗng', 'P2', 'Đang lọc ra 0 kết quả.',
     '1. Bấm Xuất Excel và xuất file.',
     '—',
     '- Tệp tải về chỉ có dòng tiêu đề, không có dòng dữ liệu.\n- Không báo lỗi hệ thống.'),
    ('015', 'Số liệu trong tệp Excel dùng định dạng số', 'P1', 'Tệp vừa xuất.',
     '1. Mở tệp, bấm vào một ô có giá trị số.',
     '—',
     '- Ô là số thật, tính tổng được.\n'
     '- ⚠️ Không xuất hiện cảnh báo số đang lưu dưới dạng chữ.'),
]

# ============================================================== X
S10 = [
    ('001', 'Ghi chú bỏ trống', 'P0', 'Đang ở màn lập phiếu, đã tích 1 dòng hợp lệ.',
     '1. Để trống ô Ghi chú.\n2. Bấm Lưu nháp.',
     'Ghi chú: (bỏ trống)',
     '- Hiện lỗi đỏ "Bắt buộc phải nhập" ngay dưới ô Ghi chú.\n'
     '- Phiếu KHÔNG được lưu, dữ liệu đã nhập vẫn còn trên màn.'),
    ('002', 'Ghi chú vượt 255 ký tự', 'P1', 'Đang ở màn lập phiếu.',
     '1. Nhập chuỗi 300 ký tự vào ô Ghi chú.',
     'Ghi chú: chuỗi 300 ký tự',
     '- Ô không cho nhập quá 255 ký tự, hoặc báo "Không được vượt quá 255 ký tự" khi lưu.\n'
     '- ⚠️ Không tự cắt bớt rồi lưu im lặng.'),
    ('003', 'Không tích dòng nào', 'P0', 'Đã nhập Ghi chú, chưa tích dòng nào.',
     '1. Bấm Lưu nháp.',
     '—',
     '- Phần mềm báo "Chưa tích chọn hàng hoá nào cần gia hạn.".\n- Phiếu không được lưu.'),
    ('004', 'Số lượng bằng 0', 'P0', 'Đã tích 1 dòng.',
     '1. Xóa số lượng, nhập 0.\n2. Bấm Lưu nháp.',
     'Số lượng cần gia hạn: 0',
     '- Báo lỗi đỏ tại dòng: "Số lượng gia hạn – Phải lớn hơn 0.".\n- Phiếu không được lưu.'),
    ('005', 'Số lượng vượt số Đang giữ', 'P0', 'Dòng có Đang giữ = 2.',
     '1. Nhập số lượng 5.\n2. Bấm Lưu nháp.',
     'Đang giữ: 2; Số lượng cần gia hạn: 5',
     '- Báo "Số lượng gia hạn – Không được vượt số đang giữ (2)".\n'
     '- ⚠️ Phần mềm GIỮ NGUYÊN số 5 người dùng đã gõ, không tự kéo về 2.'),
    ('006', 'Số lượng vượt 6 chữ số', 'P1', 'Đã tích 1 dòng.',
     '1. Nhập 1234567 vào ô số lượng.',
     'Số lượng: 1234567',
     '- Báo "Không được vượt quá 6 chữ số" hoặc lỗi tương đương.\n- Phiếu không được lưu.'),
    ('007', 'Nhập chữ vào ô số lượng', 'P0', 'Đã tích 1 dòng.',
     '1. Gõ "abc" vào ô Số lượng.',
     'Số lượng: abc',
     '- Ô chỉ nhận ký tự số, các ký tự chữ không được nhập vào.'),
    ('008', 'Dán giá trị không hợp lệ vào ô số lượng', 'P1', 'Đã tích 1 dòng.',
     '1. Sao chép chuỗi "12a3" và dán vào ô Số lượng.',
     'Dán: 12a3',
     '- Ô chỉ nhận phần số hợp lệ hoặc từ chối dán, không làm hỏng giá trị đang có.'),
    ('009', 'Bỏ trống Hạn giữ mới', 'P0', 'Đã tích 1 dòng và nhập số lượng.',
     '1. Không chọn Hạn giữ mới.\n2. Bấm Lưu nháp.',
     'Hạn giữ mới: (bỏ trống)',
     '- Báo "Hạn giữ mới – Bắt buộc nhập." tại dòng.\n- Phiếu không được lưu.'),
    ('010', 'Chọn Hạn giữ mới là hôm nay', 'P0', 'Đã tích 1 dòng.',
     '1. Mở lịch ở ô Hạn giữ mới, thử chọn ngày hôm nay.',
     'Hạn giữ mới: hôm nay',
     '- Lịch chặn không cho chọn.\n'
     '- Nếu vẫn gửi được thì phần mềm báo "Hạn giữ mới – Phải là ngày tương lai.".'),
    ('011', 'Chọn Hạn giữ mới trong quá khứ', 'P0', 'Đã tích 1 dòng.',
     '1. Thử chọn ngày của tháng trước.',
     'Hạn giữ mới: ngày trong quá khứ',
     '- Lịch chặn không cho chọn; nếu gửi được thì báo lỗi ngày phải ở tương lai.'),
    ('012', 'Chọn Hạn giữ mới vượt 30 ngày', 'P0',
     'Cấu hình số ngày giữ tối đa là 30 ngày.',
     '1. Thử chọn ngày cách hôm nay 45 ngày.',
     'Hạn giữ mới: hôm nay + 45 ngày',
     '- Lịch chặn các ngày sau mốc "hôm nay + 30 ngày".\n'
     '- Nếu gửi được thì báo "Hạn giữ mới – Không được giữ quá …".'),
    ('013', 'Chọn đúng mốc biên 30 ngày', 'P0', 'Đã tích 1 dòng.',
     '1. Chọn Hạn giữ mới = đúng ngày "hôm nay + 30 ngày".\n2. Bấm Lưu nháp.',
     'Hạn giữ mới: hôm nay + 30 ngày',
     '- ⚠️ Ngày biên này PHẢI được chấp nhận, phiếu lưu thành công.'),
    ('014', 'Chọn đúng mốc biên ngày mai', 'P0', 'Đã tích 1 dòng.',
     '1. Chọn Hạn giữ mới = ngày mai.\n2. Bấm Lưu nháp.',
     'Hạn giữ mới: ngày mai',
     '- Được chấp nhận, phiếu lưu thành công.'),
    ('015', 'Dòng hướng dẫn nêu đúng mốc trần', 'P1', 'Đang ở màn lập phiếu có dữ liệu.',
     '1. Đọc dòng hướng dẫn dưới bảng Chi tiết.',
     '—',
     '- Dòng ghi rõ hạn giữ mới phải sau hôm nay và không quá ngày cụ thể (hôm nay + 30 ngày).'),
    ('016', 'Đính kèm tệp quá 13 MB', 'P1', 'Đang ở màn lập phiếu.',
     '1. Chọn tệp PDF dung lượng 20 MB.',
     'Tệp: 20 MB',
     '- Phần mềm báo tệp vượt dung lượng cho phép và không đính kèm.'),
    ('017', 'Đính kèm định dạng không được phép', 'P1', 'Đang ở màn lập phiếu.',
     '1. Chọn một tệp nén .zip.',
     'Tệp: tai-lieu.zip',
     '- Hộp chọn tệp không cho chọn định dạng này, hoặc phần mềm báo không hỗ trợ.'),
    ('018', 'Số lượng nhập số thập phân', 'P1', 'Dòng có Đang giữ = 5.',
     '1. Nhập 2.5 vào ô Số lượng.\n2. Bấm Lưu nháp.',
     'Số lượng: 2.5',
     '- Phần mềm xử lý nhất quán: hoặc chấp nhận số lẻ, hoặc báo lỗi rõ ràng.\n'
     '- ⚠️ Không được tự làm tròn im lặng rồi lưu con số khác với cái người dùng gõ.'),
    ('019', 'Lỗi hiển thị đúng tại dòng bị sai', 'P0',
     'Phiếu có 10 dòng, chỉ dòng thứ 7 nhập số lượng vượt Đang giữ.',
     '1. Bấm Lưu nháp.',
     '—',
     '- ⚠️ Lỗi đỏ hiện ngay dưới ô của DÒNG THỨ 7, không phải chỉ một thông báo chung ở góc '
     'màn hình.\n'
     '- Màn hình tự cuộn tới dòng bị lỗi.'),
]

# ============================================================== XI
S11 = [
    ('001', 'Lô hàng bị người khác hủy giữ trong lúc lập phiếu', 'P0',
     'Người dùng A mở màn lập phiếu, đang tích lô L. Trong lúc đó lô L bị hủy giữ hết bởi một '
     'phiếu hủy hàng giữ khác.',
     '1. A bấm Gửi duyệt.',
     '—',
     '- Phần mềm báo "Lô hàng giữ không còn tồn tại hoặc không thuộc người lập phiếu.".\n'
     '- Phiếu không được lưu, dữ liệu trên màn vẫn còn để A xử lý.'),
    ('002', 'Hàng hóa bị khóa trong danh mục', 'P1',
     'Một hàng hóa trong phiếu bị khóa ở danh mục hàng hóa sau khi phiếu đã lập.',
     '1. Mở màn chi tiết phiếu.',
     '—',
     '- Tên hàng hóa vẫn hiển thị đúng, không mất dữ liệu.\n- Không có lỗi hệ thống.'),
    ('003', 'Hàng hóa bị xóa khỏi danh mục', 'P1',
     'Hàng hóa trong phiếu không còn trong danh mục.',
     '1. Duyệt phiếu đó ở bước Kế toán.',
     '—',
     '- Phần mềm báo "Hàng hoá không còn tồn tại trong danh mục." và không duyệt.'),
    ('004', 'Hai người cùng sửa một phiếu nháp', 'P1',
     'Phiếu nháp của A; A mở màn sửa trên hai tab.',
     '1. Tab 1 sửa Ghi chú và lưu.\n2. Tab 2 (chưa tải lại) sửa Ghi chú khác và lưu.',
     '—',
     '- Lần lưu sau ghi đè lần trước.\n'
     '- Lịch sử thay đổi ghi nhận đủ hai mốc chỉnh sửa.'),
    ('005', 'Xóa phiếu đang được người khác mở xem', 'P1',
     'A xóa phiếu P trong khi B đang mở màn chi tiết của P.',
     '1. B bấm nút In trên màn chi tiết đang mở.',
     '—',
     '- Phần mềm báo không tìm thấy dữ liệu, không treo trang.'),
    ('006', 'Phiếu bị từ chối trong lúc người lập đang sửa', 'P1',
     'Phiếu đang ở Chờ TP duyệt; người lập mở màn sửa bằng đường dẫn cũ; Trưởng phòng từ chối.',
     '1. Người lập bấm Lưu.',
     '—',
     '- Phần mềm xử lý nhất quán: hoặc lưu được vì phiếu đã về Đang tạo, hoặc từ chối kèm '
     'thông báo rõ ràng. Không được lưu sai trạng thái.'),
    ('007', 'Đổi số dòng mỗi trang khi đang ở trang cuối', 'P2',
     'Đang ở trang cuối với 10 dòng/trang.',
     '1. Đổi sang 100 dòng/trang.',
     '—',
     '- Quay về trang 1, hiển thị 100 dòng đầu, không bị trang trắng.'),
    ('008', 'Phiên đăng nhập hết hạn', 'P1', 'Đang mở màn danh sách.',
     '1. Để phiên hết hạn.\n2. Bấm sang trang 2.',
     '—',
     '- Phần mềm đưa về màn đăng nhập, không hiển thị lỗi kỹ thuật khó hiểu.'),
]

# ============================================================== XII
S12 = [
    ('001', 'Mở lịch sử từ cột Hành động', 'P0', 'Phiếu đã có ít nhất 1 mốc thay đổi.',
     '1. Bấm biểu tượng đồng hồ ở cột Hành động.',
     '—',
     '- Mở cửa sổ lịch sử với tiêu đề nêu tên màn và mã phiếu.\n'
     '- Danh sách mốc thay đổi hiển thị mới nhất trước.'),
    ('002', 'Mở lịch sử từ màn chi tiết', 'P0', 'Đang ở màn chi tiết phiếu.',
     '1. Kéo xuống khối Lịch sử thay đổi.\n2. Bấm nút Xem lịch sử.',
     '—',
     '- ⚠️ Khối mặc định THU GỌN, chỉ nạp dữ liệu khi bấm mở.\n'
     '- Sau khi mở, nhãn nút đổi thành Thu gọn và có thêm nút Làm mới.'),
    ('003', 'Ghi nhận mốc Tạo mới', 'P0', 'Vừa lập một phiếu mới.',
     '1. Mở lịch sử của phiếu vừa lập.',
     '—',
     '- Có mốc tạo mới, ghi đúng người lập và thời điểm.'),
    ('004', 'Ghi nhận mốc Chỉnh sửa kèm giá trị thay đổi', 'P0',
     'Vừa sửa Ghi chú của một phiếu nháp.',
     '1. Mở lịch sử của phiếu.',
     '—',
     '- Có mốc chỉnh sửa, nêu rõ trường Ghi chú với giá trị cũ và giá trị mới.'),
    ('005', 'Ghi nhận thay đổi dòng hàng', 'P0',
     'Vừa bỏ 1 dòng và thêm 1 dòng khác vào phiếu nháp.',
     '1. Mở lịch sử của phiếu.',
     '—',
     '- Mốc chỉnh sửa nêu rõ tên hàng bị bỏ và tên hàng được thêm.\n'
     '- Có ghi cả thay đổi về SL gia hạn và Hạn giữ mới nếu có.'),
    ('006', 'Ghi nhận mốc Duyệt', 'P0', 'Vừa duyệt một phiếu ở cấp Trưởng phòng.',
     '1. Mở lịch sử của phiếu.',
     '—',
     '- Có mốc duyệt, ghi người duyệt, thời điểm và trạng thái mới.'),
    ('007', 'Ghi nhận mốc Từ chối', 'P0', 'Vừa từ chối một phiếu.',
     '1. Mở lịch sử của phiếu.',
     '—',
     '- Có mốc từ chối, ghi người thực hiện, thời điểm và lý do.'),
    ('008', 'Thứ tự mới nhất trước', 'P0', 'Phiếu có ít nhất 3 mốc thay đổi.',
     '1. Mở lịch sử, đọc thời điểm từng mốc.',
     '—',
     '- ⚠️ Mốc mới nhất nằm trên cùng, cũ nhất nằm dưới cùng.'),
    ('009', 'Phiếu chưa có lịch sử', 'P1',
     'Phiếu được lập từ hệ thống cũ trước khi bật ghi lịch sử.',
     '1. Mở lịch sử của phiếu đó.',
     '—',
     '- Hiện dòng "Chưa có lịch sử thao tác nào." — đây là đúng, không phải lỗi.'),
    ('010', 'Nút Làm mới trong khối lịch sử', 'P2',
     'Khối Lịch sử thay đổi đang mở; người khác vừa sửa phiếu.',
     '1. Bấm nút Làm mới.',
     '—',
     '- Danh sách được nạp lại và có thêm mốc mới nhất.'),
    ('011', 'Đếm số mốc trên tiêu đề khối', 'P2', 'Phiếu có 4 mốc thay đổi.',
     '1. Mở khối Lịch sử thay đổi.',
     '—',
     '- Cạnh chữ "Lịch sử thay đổi" hiển thị số 4.'),
]

# ============================================================== XIII
S13 = [
    ('001', 'Luồng đầy đủ: lập nháp → gửi duyệt → ba cấp duyệt → hàng được gia hạn', 'P0',
     'Nhân viên A đang giữ lô: hàng H, khách K, đang giữ 5, hạn giữ 10/09/2026. '
     'Có sẵn tài khoản đủ ba cấp duyệt cùng công ty với A.',
     '1. A lập phiếu, tích lô đó, số lượng 3, hạn giữ mới 25/09/2026, bấm Lưu nháp.\n'
     '2. A mở lại phiếu, bấm Sửa rồi bấm Gửi duyệt.\n'
     '3. Trưởng phòng duyệt.\n4. Ban giám đốc duyệt (nếu phiếu đi qua bước này).\n'
     '5. Kế toán duyệt.\n6. Mở màn Danh sách hàng giữ để đối chiếu.',
     'Số lượng: 3; Hạn giữ mới: 25/09/2026',
     '- Sau bước 1: phiếu trạng thái Đang tạo, hàng giữ chưa đổi.\n'
     '- Sau bước 2: trạng thái Chờ TP duyệt.\n'
     '- Sau bước 3: Chờ BGĐ duyệt hoặc Chờ KT duyệt tuỳ điều kiện.\n'
     '- Sau bước 5: trạng thái Đã duyệt.\n'
     '- Lô hạn 10/09/2026 còn 2; xuất hiện lô hạn 25/09/2026 số lượng 3.\n'
     '- Lịch sử duyệt đủ các dòng đã đi qua; lịch sử thay đổi đủ các mốc.'),
    ('002', 'Luồng bị từ chối rồi sửa và duyệt lại', 'P0',
     'Phiếu vừa gửi duyệt đang ở Chờ TP duyệt.',
     '1. Trưởng phòng từ chối kèm lý do.\n2. Người lập mở phiếu, sửa số lượng, gửi lại.\n'
     '3. Trưởng phòng duyệt.\n4. Kế toán duyệt.',
     'Lý do từ chối: Số lượng đề nghị quá nhiều',
     '- Sau bước 1: phiếu về Đang tạo, cột Lý do từ chối có nội dung.\n'
     '- Sau bước 2: phiếu về Chờ TP duyệt.\n'
     '- Sau bước 4: Đã duyệt và hàng giữ chuyển đúng theo số lượng ĐÃ SỬA.\n'
     '- Lịch sử duyệt giữ cả dòng từ chối cũ lẫn dòng duyệt mới.'),
    ('003', 'Luồng lập nháp rồi xóa', 'P1', 'Nhân viên A đang có lô sắp hết hạn.',
     '1. A lập phiếu và Lưu nháp.\n2. A xóa phiếu vừa lập.\n3. Kiểm tra hàng giữ.',
     '—',
     '- Phiếu biến mất khỏi danh sách.\n'
     '- ⚠️ Hàng giữ hoàn toàn không thay đổi vì phiếu chưa từng được duyệt.'),
    ('004', 'Luồng gia hạn hai lần liên tiếp cho cùng một lô', 'P1',
     'Lô hàng H, khách K, đang giữ 5, hạn 10/09/2026.',
     '1. Lập phiếu gia hạn 2 sang hạn 20/09/2026, duyệt xong đủ ba cấp.\n'
     '2. Chờ tới khi lô hạn 20/09 vào diện sắp hết hạn, lập tiếp phiếu gia hạn 2 sang hạn '
     'muộn hơn, duyệt xong.\n3. Kiểm tra các lô.',
     '—',
     '- Sau lần 1: lô 10/09 còn 3, lô 20/09 có 2.\n'
     '- Sau lần 2: lô 20/09 còn 0, lô hạn mới có 2.\n'
     '- Lịch sử biến động của hàng hóa ghi đủ 4 dòng (2 lần trừ, 2 lần cộng).'),
    ('005', 'Kiểm tra chéo với màn Danh sách hàng giữ', 'P0',
     'Vừa duyệt xong một phiếu gia hạn.',
     '1. Mở màn Tài chính → Giữ hàng → Danh sách hàng giữ.\n'
     '2. Lọc theo nhân viên và khách hàng của phiếu.',
     '—',
     '- Số lượng và hạn giữ hiển thị khớp đúng với kết quả sau khi duyệt.\n'
     '- Tổng số lượng hàng giữ của nhân viên KHÔNG đổi (chỉ chuyển giữa hai hạn giữ).'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP PHIẾU (TẠO MỚI)', S4),
    ('V', 'SỬA PHIẾU', S5),
    ('VI', 'XEM CHI TIẾT', S6),
    ('VII', 'DUYỆT & TỪ CHỐI', S7),
    ('VIII', 'XÓA PHIẾU', S8),
    ('IX', 'IN & XUẤT EXCEL', S9),
    ('X', 'RÀNG BUỘC NHẬP LIỆU', S10),
    ('XI', 'CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI', S11),
    ('XII', 'LỊCH SỬ THAY ĐỔI', S12),
    ('XIII', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S13),
]

build(output_file=os.path.join(BASE, 'testcase.xlsx'),
      sheet_name='Trang tính1',
      feature_name='Yêu cầu gia hạn hàng giữ',
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
