# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man "Yeu cau dieu chuyen hang giu" (phan he Tai chinh).

Viet MOI hoan toan tu code HRM nhanh `gop_db` (user chot 05/09/2026).
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

MODULE = 'YC điều chuyển hàng giữ'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn hình Yêu cầu điều chuyển hàng giữ (mã phiếu ĐCHG) dùng để chuyển hàng đang giữ của '
     'người lập sang một nhân viên nhận và một khách hàng nhận khác.\n'
     'Phiếu đi qua ba cấp duyệt: Trưởng phòng → Ban giám đốc (chỉ với phiếu thuộc diện phải '
     'trình) → Kế toán. Hàng chỉ thực sự đổi chủ khi Kế toán duyệt ở bước cuối.\n'
     'Hạn giữ GIỮ NGUYÊN theo lô nguồn — điều chuyển không kéo dài thời gian giữ hàng.\n'
     'Đường dẫn: Phân hệ Tài chính → Giữ hàng → Phiếu Yêu cầu điều chuyển hàng giữ.'),
    ('2. Đối tượng được tính / hiển thị',
     'Danh sách hiển thị phiếu theo phạm vi quyền của người đăng nhập:\n'
     '- Có quyền "Xem phiếu hàng giữ theo tổng công ty": toàn bộ phiếu của mọi công ty.\n'
     '- Có quyền "Xem phiếu hàng giữ theo công ty": phiếu thuộc công ty của mình.\n'
     '- Có quyền "Xem phiếu hàng giữ theo phòng ban": phiếu thuộc phòng ban mình quản lý và '
     'phòng ban của chính mình.\n'
     '- Không có quyền nào ở trên: chỉ phiếu do chính mình lập.\n'
     '- Ngoài phạm vi trên, mọi người đều thấy thêm phiếu đang chờ chính mình duyệt.\n'
     'Popup chọn hàng liệt kê hàng mà chính người lập đang giữ, cho MỌI khách hàng.\n'
     'Ô "Từ xuất giữ" chỉ liệt kê lô do chính người lập đang giữ và còn hàng.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu ở trạng thái Không duyệt của người khác: KHÔNG hiện trong danh sách và không mở '
     'được màn chi tiết.\n'
     '- Hàng hóa đã có trong phiếu: bị loại khỏi popup chọn hàng.\n'
     '- Lô hàng giữ đã hết hạn giữ: không được chọn làm lô nguồn.\n'
     '- Lô đã chọn ở một dòng: không được chọn lại ở dòng khác trong cùng phiếu.\n'
     '- Lô hàng giữ của nhân viên khác: không xuất hiện trong ô Từ xuất giữ.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Hai ô "Ngày tạo từ" và "Ngày tạo đến" lọc theo NGÀY LẬP PHIẾU, không phải ngày duyệt và '
     'không phải hạn giữ.\n'
     'Khoảng ngày lấy trọn hai đầu mút. Chỉ nhập một đầu thì lọc một chiều.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Một phiếu gồm phần thông tin chung (người nhận, khách hàng nhận, ghi chú, tệp đính kèm) '
     'và nhiều dòng hàng hóa.\n'
     'Mỗi dòng hàng gắn với một lô hàng giữ NGUỒN cụ thể và một số lượng chuyển; có thể gắn '
     'thêm hợp đồng do người lập chọn tay.\n'
     'Phiếu có ba bộ thông tin duyệt tương ứng ba cấp Trưởng phòng, Ban giám đốc, Kế toán.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     'Mỗi lô hàng giữ chỉ được chọn ở MỘT dòng trong cùng một phiếu.\n'
     'Khi Kế toán duyệt, phần mềm trừ số lượng ở lô nguồn rồi CỘNG vào lô có cùng hàng hóa, '
     'cùng người nhận, cùng khách hàng nhận và CÙNG HẠN GIỮ với lô nguồn; chưa có lô đó thì '
     'tạo lô mới.\n'
     'Lô đích lấy công ty theo lô nguồn, không theo người duyệt.'),
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
     'hàng giữ của chính mình, và chỉ sửa/xóa được phiếu của mình khi phiếu ở trạng thái '
     'Không duyệt.'),
    ('8. Cách tính các ô thống kê',
     'Ô "Hiển thị a–b / N": a là dòng đầu trang, b là dòng cuối trang, N là tổng số phiếu khớp '
     'bộ lọc TRONG PHẠM VI QUYỀN của người đang xem.\n'
     'Cột "Đang giữ" = số lượng còn lại của chính lô nguồn đã chọn.\n'
     'Cột "Có thể giữ" = tồn kho khả dụng của hàng hóa trong công ty; là số THAM KHẢO, khác '
     'hoàn toàn với cột "Đang giữ".\n'
     'Dòng "Tổng cộng" trên bản in = tổng cột Chuyển của các dòng được in.'),
    ('9. Ghi chú đọc bảng',
     'Các bẫy dễ sai nhất của màn này:\n'
     '- Màn KHÔNG có bản nháp: bấm Gửi duyệt là phiếu vào thẳng bước Chờ TP duyệt.\n'
     '- Chỉ phiếu ở trạng thái "Không duyệt" mới sửa hoặc xóa lại được (khác hai màn cùng nhóm '
     'dùng trạng thái "Đang tạo").\n'
     '- Sửa lại phiếu thì phần mềm XÓA dấu duyệt của cả ba cấp, phiếu đi lại từ đầu.\n'
     '- Trưởng phòng duyệt xét theo phòng ban của NGƯỜI NHẬN, không phải người lập.\n'
     '- Hạn giữ GIỮ NGUYÊN sau khi chuyển; muốn kéo dài phải lập phiếu gia hạn.\n'
     '- "Có thể giữ" và "Đang giữ" là hai con số khác nhau, đừng so với nhau.\n'
     '- Nhãn nút là "Từ chối" nhưng tên trạng thái phiếu là "Không duyệt" — khác nhau có chủ ý.\n'
     '- Cột Hành động ngoài danh sách KHÔNG có nút Từ chối; phải mở phiếu ra mới từ chối được.\n'
     '- Nhóm test bảo mật gọi thẳng chức năng bằng công cụ kiểm thử dành cho tester kỹ thuật.'),
]

ROLE_TCS = [
    ('00', 'Tài khoản không có quyền nào của nhóm hàng giữ vẫn vào được màn hình', 'P0',
     'Tài khoản A không có quyền duyệt và không có quyền xem theo cấp; A đã lập 48 phiếu; '
     'toàn hệ thống có 1.295 phiếu.',
     '1. Đăng nhập bằng tài khoản A.\n'
     '2. Vào Tài chính → Giữ hàng → Phiếu Yêu cầu điều chuyển hàng giữ.',
     '—',
     '- Màn hình mở được, không báo lỗi quyền.\n'
     '- Danh sách chỉ có 48 phiếu do A lập.\n'
     '- Ô "Hiển thị a–b / N" ghi N = 48.\n'
     '- Nút Tạo mới vẫn hiển thị.\n'
     '- Bảng lọc nâng cao KHÔNG có ô Công ty và ô Phòng ban.'),
    ('01', 'Quyền "Xem phiếu hàng giữ theo tổng công ty" thấy phiếu của mọi công ty', 'P0',
     'Tài khoản B chỉ có quyền Xem phiếu hàng giữ theo tổng công ty. Hệ thống có phiếu của ít '
     'nhất 2 công ty khác nhau.',
     '1. Đăng nhập bằng B.\n2. Mở màn danh sách và đọc N.\n3. Lọc lần lượt từng công ty.',
     '—',
     '- N bằng tổng số phiếu khác trạng thái Không duyệt của toàn hệ thống, cộng phiếu Không '
     'duyệt của chính B.\n'
     '- Bảng lọc CÓ ô Công ty và ô Phòng ban.'),
    ('02', 'Quyền "Xem phiếu hàng giữ theo công ty" chỉ thấy phiếu công ty mình', 'P0',
     'Tài khoản C thuộc công ty 1, chỉ có quyền Xem phiếu hàng giữ theo công ty. Công ty 1 có '
     '1.100 phiếu, công ty 4 có 150 phiếu.',
     '1. Đăng nhập bằng C.\n2. Đọc N.\n'
     '3. Mở một phiếu của công ty 4 bằng đường dẫn trực tiếp.',
     '—',
     '- N = 1.100, không thấy phiếu công ty 4.\n'
     '- Bảng lọc CÓ ô Phòng ban, KHÔNG có ô Công ty.\n'
     '- ⚠️ Mở phiếu công ty 4 bằng đường dẫn: phần mềm báo không có quyền xem phiếu này.'),
    ('03', 'Quyền "Xem phiếu hàng giữ theo phòng ban"', 'P0',
     'Tài khoản D quản lý phòng "Phòng KD Khu vực 1" có 55 phiếu; phòng khác có 70 phiếu.',
     '1. Đăng nhập bằng D.\n2. Đọc N và bật cột Phòng ban trong Tuỳ chỉnh cột.',
     '—',
     '- N = 55 cộng số phiếu Không duyệt của chính D.\n'
     '- Mọi dòng đều thuộc phòng D quản lý hoặc phòng của chính D.'),
    ('04', 'Quyền "Trưởng phòng duyệt hàng giữ" xét theo phòng ban NGƯỜI NHẬN', 'P0',
     'Tài khoản E có quyền Trưởng phòng duyệt hàng giữ, quản lý phòng P1. Phiếu X ở Chờ TP '
     'duyệt có NGƯỜI NHẬN thuộc phòng P1 nhưng người lập thuộc phòng P2. Phiếu Y ở Chờ TP '
     'duyệt có người nhận thuộc phòng P2, người lập thuộc P1.',
     '1. Đăng nhập bằng E.\n2. Mở phiếu X.\n3. Mở phiếu Y.',
     '—',
     '- ⚠️ Phiếu X: CÓ nút "TP duyệt" và "Từ chối" (xét theo phòng người nhận).\n'
     '- ⚠️ Phiếu Y: KHÔNG có hai nút đó, dù người lập thuộc phòng E quản lý.'),
    ('05', 'Quyền "Ban giám đốc duyệt hàng giữ"', 'P0',
     'Tài khoản F có quyền Ban giám đốc duyệt hàng giữ, cùng công ty với phiếu M đang ở trạng '
     'thái Chờ BGĐ duyệt.',
     '1. Đăng nhập bằng F.\n2. Mở phiếu M.',
     '—',
     '- Cuối màn có nút "BGĐ duyệt" và "Từ chối".\n'
     '- Với phiếu ở trạng thái Chờ TP duyệt hoặc Chờ KT duyệt, hai nút này không hiển thị.'),
    ('06', 'Quyền "Kế toán duyệt hàng giữ"', 'P0',
     'Tài khoản G có quyền Kế toán duyệt hàng giữ, cùng công ty với phiếu N đang ở Chờ KT duyệt.',
     '1. Đăng nhập bằng G.\n2. Mở phiếu N.\n3. Rê chuột vào nút duyệt.',
     '—',
     '- Cuối màn có nút "KT duyệt" và "Từ chối".\n'
     '- Chú thích khi rê chuột nêu rõ đây là bước ghi tồn hàng giữ.'),
    ('07', 'Người duyệt khác công ty với phiếu thì không duyệt được', 'P0',
     'Tài khoản H có quyền Kế toán duyệt hàng giữ, thuộc công ty 4. Phiếu K ở Chờ KT duyệt '
     'thuộc công ty 1.',
     '1. Đăng nhập bằng H.\n2. Tìm phiếu K.\n'
     '3. Dùng công cụ kiểm thử gọi thẳng chức năng duyệt phiếu K.',
     '—',
     '- Nếu H thấy được phiếu K thì nút KT duyệt KHÔNG hiển thị.\n'
     '- ⚠️ Gọi thẳng chức năng: phần mềm từ chối, báo không có quyền duyệt bước này; trạng thái '
     'phiếu K không đổi và hàng giữ không thay đổi.'),
    ('08', 'Bỏ qua giao diện gọi thẳng chức năng Sửa phiếu của người khác', 'P0',
     'Phiếu P đang ở trạng thái Không duyệt do tài khoản B lập.',
     '1. Đăng nhập bằng A.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa với phiếu P.',
     '—',
     '- Phần mềm từ chối.\n- Nội dung phiếu P không thay đổi.'),
    ('09', 'Bỏ qua giao diện gọi thẳng chức năng Xóa phiếu đang chờ duyệt', 'P0',
     'Phiếu Q do tài khoản A lập, đang ở trạng thái Chờ TP duyệt.',
     '1. Đăng nhập bằng A.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa với phiếu Q.',
     '—',
     '- Phần mềm từ chối xóa.\n- Phiếu Q vẫn còn và giữ nguyên trạng thái Chờ TP duyệt.'),
    ('10', 'Bỏ qua giao diện gọi thẳng chức năng Từ chối khi không đúng cấp', 'P0',
     'Tài khoản E chỉ có quyền Trưởng phòng duyệt hàng giữ. Phiếu R đang ở Chờ KT duyệt.',
     '1. Đăng nhập bằng E.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Từ chối với phiếu R.',
     '—',
     '- Phần mềm từ chối, báo không có quyền từ chối phiếu này.\n'
     '- Phiếu R vẫn ở trạng thái Chờ KT duyệt.'),
    ('11', 'Xem lịch sử thay đổi của phiếu ngoài phạm vi quyền', 'P1',
     'Tài khoản C (xem theo công ty 1) và phiếu S thuộc công ty 4.',
     '1. Đăng nhập bằng C.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng xem lịch sử phiếu S.',
     '—',
     '- Phần mềm từ chối, báo không có quyền xem phiếu này.'),
]

# ============================================================== I
S1 = [
    ('001', 'Mở màn hình từ menu', 'P0', 'Tài khoản có ít nhất 1 phiếu trong phạm vi.',
     '1. Đăng nhập.\n2. Chọn phân hệ Tài chính.\n3. Mở nhóm Hàng hoá - Dịch vụ - Vận chuyển → '
     'Giữ hàng.\n4. Bấm mục Phiếu Yêu cầu điều chuyển hàng giữ.',
     '—',
     '- Tiêu đề trên thanh trên cùng và tiêu đề bảng đều ghi "Yêu cầu điều chuyển hàng giữ".\n'
     '- Bảng hiện dữ liệu, không có thông báo lỗi.'),
    ('002', 'Vòng quay chờ hiện ngay khi vào màn', 'P1', 'Danh sách có trên 1.000 phiếu.',
     '1. Mở màn hình và quan sát bảng trong lúc dữ liệu đang tải.',
     '—',
     '- Trong lúc chờ, bảng hiện vòng quay chờ.\n'
     '- ⚠️ KHÔNG nhấp nháy dòng "Không có dữ liệu phù hợp." rồi mới hiện dữ liệu.'),
    ('003', 'Thanh công cụ có đủ 4 nút', 'P0', 'Đã vào màn hình.',
     '1. Quan sát thanh công cụ phía trên bảng.',
     '—',
     '- Có bốn nút: Tạo mới, In, Xuất Excel và biểu tượng cấu hình cột.'),
    ('004', 'Đủ cột theo cấu hình mặc định', 'P0', 'Người dùng chưa từng đổi cấu hình cột.',
     '1. Quan sát tiêu đề các cột.',
     '—',
     '- Hiện sẵn: STT, Mã phiếu, Người tạo, Ngày tạo, Người nhận, Khách nhận, Trạng thái, '
     'Người duyệt, Ngày duyệt, Hành động.\n'
     '- Ẩn sẵn: Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do không duyệt.'),
    ('005', 'Mã phiếu là liên kết mở màn chi tiết', 'P0', 'Danh sách có ít nhất 1 phiếu.',
     '1. Bấm vào mã phiếu ở dòng đầu tiên.',
     '—',
     '- Mở màn chi tiết đúng phiếu vừa bấm.\n'
     '- Tiêu đề màn ghi "Chi tiết yêu cầu điều chuyển hàng giữ: <mã phiếu>".'),
    ('006', 'Màu trạng thái đúng quy ước', 'P0',
     'Danh sách có phiếu ở các trạng thái Chờ TP duyệt, Chờ BGĐ duyệt, Chờ KT duyệt, Đã duyệt '
     'và Không duyệt.',
     '1. Lọc lần lượt từng trạng thái và quan sát màu nhãn.',
     'Trạng thái: lần lượt 5 giá trị',
     '- Ba trạng thái chờ duyệt: nhãn CAM.\n- Đã duyệt: nhãn XANH LÁ.\n'
     '- ⚠️ Không duyệt: nhãn ĐỎ (đây là trạng thái riêng của màn này).'),
    ('007', 'Phiếu Không duyệt của người khác không hiện', 'P0',
     'Tài khoản A có quyền xem theo tổng công ty. Tài khoản B đang có 1 phiếu ở trạng thái '
     'Không duyệt.',
     '1. Đăng nhập bằng A.\n2. Lọc Trạng thái = Không duyệt.',
     'Trạng thái: Không duyệt',
     '- ⚠️ Danh sách KHÔNG có phiếu Không duyệt của B.\n'
     '- Chỉ hiện phiếu Không duyệt do chính A lập.'),
    ('008', 'Người duyệt thấy thêm phiếu đang chờ mình duyệt', 'P0',
     'Tài khoản E không có quyền xem theo cấp, có quyền Trưởng phòng duyệt hàng giữ và quản lý '
     'phòng P1. Có 3 phiếu Chờ TP duyệt với người nhận thuộc P1. E tự lập 2 phiếu.',
     '1. Đăng nhập bằng E.\n2. Mở màn danh sách và đọc N.',
     '—',
     '- N = 5 (2 phiếu của E cộng 3 phiếu đang chờ E duyệt).\n'
     '- 3 phiếu chờ duyệt đều có biểu tượng duyệt ở cột Hành động.'),
    ('009', 'Trạng thái rỗng khi không có dữ liệu', 'P1',
     'Tài khoản mới, chưa lập phiếu nào và không có quyền xem theo cấp.',
     '1. Mở màn hình.',
     '—', '- Bảng hiện dòng "Không có dữ liệu phù hợp.". Ô thống kê ghi N = 0.'),
    ('010', 'Tiêu đề tab trình duyệt', 'P2', 'Đã vào màn hình.',
     '1. Quan sát tên tab trình duyệt.',
     '—', '- Tên tab ghi "Yêu cầu điều chuyển hàng giữ".'),
]

# ============================================================== II
S2 = [
    ('001', 'Tìm nhanh theo mã phiếu đầy đủ', 'P0', 'Tồn tại phiếu ĐCHG-01307.',
     '1. Gõ ĐCHG-01307 vào ô tìm nhanh.\n2. Bấm nút Tìm kiếm.',
     'Ô tìm nhanh: ĐCHG-01307',
     '- Danh sách còn đúng 1 dòng.\n- N = 1.'),
    ('002', 'Tìm nhanh theo một phần mã phiếu', 'P1', 'Có nhiều phiếu mã bắt đầu ĐCHG-013.',
     '1. Gõ 013 vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: 013',
     '- Mọi dòng trả về đều có mã phiếu chứa chuỗi 013.'),
    ('003', 'Ô tìm nhanh KHÔNG tự tìm khi đang gõ', 'P1', 'Đang ở màn danh sách.',
     '1. Gõ vài ký tự vào ô tìm nhanh.\n2. Chờ 5 giây, không bấm gì.',
     'Ô tìm nhanh: ĐCHG',
     '- Danh sách giữ nguyên, chỉ lọc khi bấm nút Tìm kiếm hoặc nhấn Enter.'),
    ('004', 'Đủ 11 ô lọc theo quyền cao nhất', 'P0',
     'Tài khoản có quyền Xem phiếu hàng giữ theo tổng công ty, chưa đổi Cài đặt bộ lọc.',
     '1. Mở bảng lọc nâng cao.\n2. Đếm và đọc nhãn từng ô.',
     '—',
     '- Có đủ: Công ty, Phòng ban, Mã phiếu, Trạng thái, Người nhận, Khách nhận, Người tạo, '
     'Người duyệt, Tên - mã hàng, Số hợp đồng, Ngày tạo từ, Ngày tạo đến.'),
    ('005', 'Ô Công ty và Phòng ban ẩn theo quyền', 'P0',
     'Tài khoản không có quyền xem theo cấp nào.',
     '1. Mở bảng lọc nâng cao.',
     '—', '- KHÔNG có ô Công ty và ô Phòng ban; các ô còn lại vẫn đủ.'),
    ('006', 'Lọc theo Trạng thái', 'P0', 'Có phiếu ở nhiều trạng thái.',
     '1. Chọn Trạng thái = Đã duyệt.',
     'Trạng thái: Đã duyệt',
     '- Danh sách tự lọc lại NGAY, không cần bấm nút.\n- Mọi dòng đều có nhãn Đã duyệt.'),
    ('007', 'Lọc theo Người nhận', 'P0', 'Nhân viên "Lại Văn Hiệp" là người nhận của 12 phiếu.',
     '1. Chọn Người nhận = Lại Văn Hiệp.',
     'Người nhận: Lại Văn Hiệp',
     '- N = 12.\n- ⚠️ Mọi dòng đều có cột Người nhận là Lại Văn Hiệp (không phải cột Người tạo).'),
    ('008', 'Lọc theo Khách nhận', 'P0', 'Có phiếu có Khách nhận là một khách hàng cụ thể.',
     '1. Chọn Khách nhận = CÔNG TY CỔ PHẦN CARON HOLDINGS.',
     'Khách nhận: CÔNG TY CỔ PHẦN CARON HOLDINGS',
     '- Mọi dòng trả về đều có cột Khách nhận đúng khách hàng đã chọn.'),
    ('009', 'Lọc theo Người tạo', 'P1', 'Nhân viên "Nguyễn Văn Nam" có nhiều phiếu.',
     '1. Chọn Người tạo = Nguyễn Văn Nam.',
     'Người tạo: Nguyễn Văn Nam',
     '- Mọi dòng đều có cột Người tạo đúng nhân viên đã chọn.'),
    ('010', 'Lọc theo Người duyệt', 'P1', 'Có phiếu đã duyệt bởi nhiều người khác nhau.',
     '1. Chọn Người duyệt = Võ Thị Hà.',
     'Người duyệt: Võ Thị Hà',
     '- Mọi dòng trả về đều có cột Người duyệt đúng người đã chọn.'),
    ('011', 'Lọc theo Tên, mã hàng', 'P0',
     'Có phiếu chứa hàng "Kích cá sấu 3 tấn, siêu mỏng" mã TORI-T830036.',
     '1. Nhập "Kích cá sấu" vào ô Tên, mã hàng.\n2. Xóa đi, nhập TORI-T830036.',
     'Tên, mã hàng: lần lượt 2 giá trị',
     '- ⚠️ Cùng MỘT ô lọc tìm được cả theo tên lẫn theo mã hàng.\n'
     '- Cả hai lần đều trả về phiếu chứa hàng hóa đó.'),
    ('012', 'Lọc theo Số hợp đồng', 'P0',
     'Có phiếu có dòng hàng gắn hợp đồng số HĐ_TPE_HN_KD2_26_0955_VDA.',
     '1. Nhập HĐ_TPE_HN_KD2_26_0955_VDA vào ô Số hợp đồng.',
     'Số hợp đồng: HĐ_TPE_HN_KD2_26_0955_VDA',
     '- Chỉ còn phiếu có ít nhất một dòng hàng gắn hợp đồng đó.\n'
     '- Mở một phiếu trong kết quả để kiểm chứng cột Hợp đồng.'),
    ('013', 'Lọc theo khoảng Ngày tạo', 'P0', 'Có phiếu lập trong tháng 06/2026.',
     '1. Chọn Ngày tạo từ = 01/06/2026 và Ngày tạo đến = 30/06/2026.',
     'Khoảng 01/06–30/06/2026',
     '- Mọi dòng có Ngày tạo trong tháng 6, lấy trọn hai đầu mút.'),
    ('014', 'Chọn Ngày tạo từ lớn hơn Ngày tạo đến', 'P1', 'Đang ở màn danh sách.',
     '1. Chọn Ngày tạo từ = 30/06/2026 và Ngày tạo đến = 01/06/2026.',
     'Ngày tạo từ: 30/06/2026; đến: 01/06/2026',
     '- Không treo, không lỗi hệ thống.\n- Danh sách rỗng kèm dòng "Không có dữ liệu phù hợp.".'),
    ('015', 'Kết hợp nhiều tiêu chí lọc', 'P0', 'Có dữ liệu phù hợp.',
     '1. Chọn Trạng thái = Đã duyệt.\n2. Chọn Người nhận.\n3. Chọn khoảng Ngày tạo.',
     'Trạng thái: Đã duyệt; Người nhận: Nguyễn Văn Nam; tháng 06/2026',
     '- Kết quả thỏa mãn ĐỒNG THỜI cả ba điều kiện.'),
    ('016', 'Đổi Công ty thì Phòng ban được nạp lại', 'P0',
     'Tài khoản có quyền xem theo tổng công ty.',
     '1. Chọn Công ty = công ty 1 rồi chọn một Phòng ban.\n2. Đổi Công ty sang công ty 4.',
     '—',
     '- Giá trị Phòng ban bị xóa; danh sách phòng ban nạp lại theo công ty mới.'),
    ('017', 'Nút Làm mới xóa hết điều kiện lọc', 'P0', 'Đang áp ít nhất 3 điều kiện lọc.',
     '1. Bấm nút Làm mới.',
     '—',
     '- Mọi ô lọc trở về trống.\n'
     '- ⚠️ Danh sách được TẢI LẠI ngay, N trở về tổng phiếu trong phạm vi quyền.\n'
     '- Thứ tự sắp xếp trở về mặc định.'),
    ('018', 'Bộ lọc được ghi nhớ khi quay lại màn', 'P1',
     'Đang áp bộ lọc Trạng thái = Đã duyệt.',
     '1. Mở một phiếu rồi bấm Quay lại (trong vòng 10 phút).',
     '—', '- Bộ lọc vẫn còn và danh sách vẫn đang lọc.'),
    ('019', 'Lọc ra kết quả rỗng', 'P1', 'Đang ở màn danh sách.',
     '1. Nhập vào ô Số hợp đồng một chuỗi chắc chắn không tồn tại.',
     'Số hợp đồng: ZZZ-KHONG-CO',
     '- Bảng hiện "Không có dữ liệu phù hợp.".\n- N = 0, không lỗi hệ thống.'),
    ('020', 'Cài đặt bộ lọc — bỏ tích một ô lọc', 'P1', 'Đang ở màn danh sách.',
     '1. Bấm Cài đặt bộ lọc.\n2. Bỏ tích ô "Số hợp đồng".\n3. Bấm Lưu.\n'
     '4. Mở lại bảng lọc nâng cao.',
     '—',
     '- Cửa sổ liệt kê 11 mục lọc kèm số thứ tự.\n'
     '- Sau khi lưu, bảng lọc nâng cao KHÔNG còn ô Số hợp đồng.'),
    ('021', 'Cài đặt bộ lọc — kéo đổi thứ tự', 'P2', 'Cửa sổ Cài đặt bộ lọc đang mở.',
     '1. Kéo mục "Người nhận" lên vị trí số 1.\n2. Bấm Lưu.',
     '—', '- Bảng lọc nâng cao hiển thị ô Người nhận ở vị trí đầu tiên.'),
    ('022', 'Cài đặt bộ lọc — Khôi phục mặc định', 'P2',
     'Đã bỏ tích và đổi thứ tự vài ô lọc.',
     '1. Mở Cài đặt bộ lọc.\n2. Bấm Khôi phục mặc định.\n3. Bấm Lưu.',
     '—', '- Danh sách ô lọc trở về đủ 11 mục theo thứ tự ban đầu.'),
    ('023', 'Cấu hình bộ lọc lưu riêng theo người dùng', 'P1',
     'Tài khoản A đã bỏ tích ô Số hợp đồng.',
     '1. Đăng nhập bằng tài khoản B.\n2. Mở bảng lọc nâng cao.',
     '—', '- Tài khoản B vẫn thấy đủ 11 ô lọc.'),
]

# ============================================================== III
S3 = [
    ('001', 'Phân trang mặc định 10 dòng', 'P0', 'Danh sách có 1.245 phiếu.',
     '1. Mở màn hình và quan sát.',
     '—', '- Bảng hiện đúng 10 dòng. Ô thống kê ghi "Hiển thị 1–10 / 1245".'),
    ('002', 'Chuyển sang trang 2', 'P0', 'Danh sách nhiều hơn 1 trang.',
     '1. Bấm số 2 ở thanh phân trang.',
     '—',
     '- Ô thống kê ghi "Hiển thị 11–20 / N".\n'
     '- Cột STT chạy tiếp từ 11 đến 20, KHÔNG quay về 1.'),
    ('003', 'Đổi số dòng mỗi trang', 'P0', 'Danh sách nhiều hơn 50 phiếu.',
     '1. Đang ở trang 3, đổi Số dòng/trang sang 50.',
     'Số dòng/trang: 50',
     '- Bảng hiện 50 dòng.\n- ⚠️ Quay về TRANG 1.'),
    ('004', 'Nút về đầu và về cuối', 'P1', 'Danh sách có ít nhất 5 trang.',
     '1. Bấm nút về cuối.\n2. Bấm nút về đầu.',
     '—', '- Về cuối hiện trang cuối; về đầu quay lại trang 1.'),
    ('005', 'Đổi trang giữ nguyên bộ lọc', 'P0', 'Đang lọc Trạng thái = Đã duyệt, nhiều trang.',
     '1. Chuyển sang trang 2.',
     '—', '- ⚠️ Mọi dòng ở trang 2 vẫn là Đã duyệt; N không đổi.'),
    ('006', 'Đổi bộ lọc thì quay về trang 1', 'P0', 'Đang ở trang 3.',
     '1. Đổi ô lọc Trạng thái sang giá trị khác.',
     '—', '- Danh sách quay về trang 1 với kết quả mới.'),
    ('007', 'Sắp xếp theo Mã phiếu', 'P0', 'Danh sách có nhiều phiếu.',
     '1. Bấm tiêu đề cột Mã phiếu hai lần.',
     '—', '- Lần 1 tăng dần, lần 2 GIẢM DẦN; quay về trang 1 sau mỗi lần đổi.'),
    ('008', 'Sắp xếp theo Ngày tạo và Ngày duyệt', 'P0', 'Danh sách có nhiều phiếu.',
     '1. Bấm tiêu đề cột Ngày tạo.\n2. Bấm tiêu đề cột Ngày duyệt.',
     '—',
     '- Cả hai cột sắp xếp đúng theo ngày giờ.\n'
     '- Phiếu chưa duyệt (ô trống) không gây lỗi hiển thị.'),
    ('009', 'Các cột khác không sắp xếp được', 'P2', 'Đang ở màn danh sách.',
     '1. Quan sát tiêu đề các cột.',
     '—', '- Chỉ ba cột Mã phiếu, Ngày tạo, Ngày duyệt có biểu tượng sắp xếp.'),
    ('010', 'Tuỳ chỉnh cột — bật cột đang ẩn', 'P0', 'Đang ở màn danh sách.',
     '1. Bấm biểu tượng cấu hình cột.\n2. Tích cột Lý do không duyệt.\n3. Bấm Lưu.',
     '—',
     '- Cửa sổ có tiêu đề "Tuỳ chỉnh cột".\n'
     '- Bảng hiện thêm cột Lý do không duyệt; phiếu bị trả về có nội dung, phiếu khác để trống.'),
    ('011', 'Tuỳ chỉnh cột — ba cột bị khóa', 'P0', 'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Thử bỏ tích cột STT, Mã phiếu và Hành động.',
     '—', '- Ba cột này có biểu tượng ổ khóa, không bỏ tích được.'),
    ('012', 'Tuỳ chỉnh cột — Đóng không lưu', 'P2', 'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Bỏ tích một cột.\n2. Bấm Đóng.',
     '—', '- Bảng giữ nguyên như trước.'),
    ('013', 'Cấu hình cột còn nguyên sau khi thoát và vào lại', 'P1',
     'Vừa bật cột Phòng ban và lưu.',
     '1. Chuyển sang màn khác rồi quay lại.',
     '—', '- Cột Phòng ban vẫn đang hiển thị.'),
    ('014', 'Bảng cuộn ngang khi bật nhiều cột', 'P2', 'Đã bật cả 5 cột ẩn.',
     '1. Cuộn ngang bảng.',
     '—',
     '- Có thanh cuộn ngang ở cả trên và dưới bảng.\n'
     '- Cột STT, Mã phiếu và Hành động vẫn dính khi cuộn.'),
]

# ============================================================== IV
S4 = [
    ('001', 'Mở màn lập phiếu', 'P0', 'Tài khoản đang giữ ít nhất 2 lô hàng còn hạn.',
     '1. Bấm nút Tạo mới ở màn danh sách.',
     '—',
     '- Có ô Người nhận và Khách hàng nhận đều có dấu sao đỏ, ô Ghi chú và khối File đính kèm.\n'
     '- Bảng Chi tiết trống, có câu nhắc bấm Thêm hàng hóa để chọn từ hàng đang giữ.\n'
     '- ⚠️ Cuối màn KHÔNG có nút Lưu nháp, chỉ có Gửi duyệt, Lưu và tiếp tục, Quay lại.'),
    ('002', 'Popup chọn hàng liệt kê hàng của mọi khách hàng', 'P0',
     'Tài khoản A đang giữ 2 mặt hàng cho khách K và 3 mặt hàng cho khách L.',
     '1. Bấm Thêm hàng hóa.',
     '—',
     '- Popup có tiêu đề "Hàng bạn đang giữ" kèm dòng phụ nêu rõ gồm mọi khách hàng.\n'
     '- ⚠️ Có đủ 5 mặt hàng, KHÔNG lọc theo khách hàng nào (khác màn Yêu cầu hủy hàng giữ).'),
    ('003', 'Popup có ô tìm kiếm', 'P1', 'Popup đang mở với nhiều dòng.',
     '1. Nhập một phần tên hàng vào ô Tên hàng hóa.\n2. Bấm Tìm kiếm.\n3. Bấm Làm mới.',
     'Tên hàng hóa: Kích cá sấu',
     '- Danh sách trong popup lọc lại theo từ khóa.\n'
     '- Bấm Làm mới trả về danh sách đầy đủ.'),
    ('004', 'Hàng đã có trong phiếu bị loại khỏi popup', 'P0',
     'Phiếu đã có 2 dòng hàng; người lập đang giữ tổng 5 mặt hàng.',
     '1. Bấm Thêm hàng hóa lần nữa.',
     '—', '- ⚠️ Popup chỉ còn 3 mặt hàng chưa có trong phiếu.'),
    ('005', 'Đủ cột ở bảng Chi tiết', 'P0', 'Bảng đã có dòng hàng.',
     '1. Đọc tiêu đề các cột.',
     '—',
     '- Có đủ: STT, Tên hàng hóa, Mã hàng hóa, ĐVT, Từ xuất giữ, Có thể giữ, Số lượng (gồm hai '
     'cột con Đang giữ và Chuyển), Hạn giữ, Hợp đồng và cột Xóa.'),
    ('006', 'Chọn lô ở ô Từ xuất giữ', 'P0',
     'Hàng H của người lập có 2 lô: lô hạn 28/06 có 5, lô hạn 12/07 có 3.',
     '1. Mở ô Từ xuất giữ của dòng hàng H.\n2. Chọn lô hạn 28/06.',
     'Từ xuất giữ: 5 - 28/06/2026',
     '- Danh sách lô hiển thị dạng số lượng – hạn giữ.\n'
     '- Sau khi chọn: cột Đang giữ hiện 5, cột Hạn giữ hiện 28/06/2026.'),
    ('007', 'Ô Từ xuất giữ chỉ có lô của chính người lập', 'P0',
     'Hàng H cũng đang được nhân viên khác giữ.',
     '1. Mở ô Từ xuất giữ của dòng hàng H.',
     '—', '- ⚠️ Chỉ liệt kê lô do chính người lập đang giữ, không có lô của người khác.'),
    ('008', 'Cột Đang giữ mở lịch sử của lô', 'P1', 'Đã chọn lô nguồn cho một dòng.',
     '1. Bấm vào con số ở cột Đang giữ.',
     '—', '- Mở cửa sổ lịch sử tăng giảm của đúng lô hàng giữ đó.'),
    ('009', 'Phân biệt cột Có thể giữ và Đang giữ', 'P0',
     'Một hàng hóa có tồn kho khả dụng 77 và lô nguồn đang giữ 5.',
     '1. Rê chuột vào biểu tượng chữ i cạnh tiêu đề cột Có thể giữ.\n2. Đọc số ở hai cột.',
     '—',
     '- Lời giải thích nêu rõ hai con số khác nhau.\n'
     '- Cột Có thể giữ = 77, cột Đang giữ = 5.'),
    ('010', 'Ô ĐVT bị khóa và có giải thích', 'P1', 'Đang ở màn lập phiếu.',
     '1. Rê chuột vào biểu tượng chữ i cạnh tiêu đề cột ĐVT.',
     '—',
     '- Hiện lời giải thích: hàng giữ luôn ghi theo đơn vị cơ bản nên không chọn được đơn vị '
     'khác.'),
    ('011', 'Chọn hợp đồng cho dòng hàng', 'P1', 'Đang ở màn lập phiếu, đã có dòng hàng.',
     '1. Bấm nút tìm kiếm ở ô Hợp đồng của một dòng.\n2. Chọn một hợp đồng.',
     '—',
     '- Popup chọn hợp đồng mở ra.\n- Sau khi chọn, ô Hợp đồng của dòng hiện số hợp đồng.\n'
     '- ⚠️ Hợp đồng do người lập chọn tay, phần mềm KHÔNG tự suy từ lô nguồn.'),
    ('012', 'Xóa một dòng hàng', 'P1', 'Bảng có 3 dòng.',
     '1. Bấm biểu tượng thùng rác ở dòng 2.',
     '—', '- Dòng 2 biến mất; hai dòng còn lại giữ nguyên.'),
    ('013', 'Gửi duyệt thành công', 'P0',
     'Đã chọn Người nhận, Khách hàng nhận và 1 dòng hàng có lô nguồn cùng số lượng hợp lệ.',
     '1. Bấm Gửi duyệt.',
     'Người nhận: Đỗ Quốc Bảo; Chuyển: 2',
     '- Hiện thông báo thành công, quay về màn danh sách.\n'
     '- ⚠️ Phiếu mới có trạng thái Chờ TP duyệt ngay (không qua bản nháp).\n'
     '- Mã phiếu dạng ĐCHG-NNNNN.\n'
     '- Trưởng phòng quản lý phòng ban của NGƯỜI NHẬN nhận được thông báo.'),
    ('014', 'Lưu và tiếp tục', 'P1', 'Đang ở màn lập phiếu với dữ liệu hợp lệ.',
     '1. Bấm Lưu và tiếp tục.',
     '—',
     '- Phiếu được lưu và vào trạng thái Chờ TP duyệt.\n'
     '- ⚠️ KHÔNG quay về danh sách; màn hình được làm mới để lập phiếu tiếp theo.'),
    ('015', 'Nút Lưu và tiếp tục chỉ có ở màn Tạo mới', 'P2',
     'Có phiếu ở trạng thái Không duyệt do chính mình lập.',
     '1. Mở màn Sửa của phiếu đó.',
     '—', '- Màn Sửa chỉ có Gửi duyệt và Quay lại.'),
    ('016', 'Đính kèm tệp hợp lệ', 'P1', 'Đang ở màn lập phiếu.',
     '1. Bấm nút Chọn tệp.\n2. Chọn một tệp PDF 2 MB.',
     'Tệp: bien-ban-ban-giao.pdf (2 MB)',
     '- Tên tệp hiện trong danh sách đính kèm kèm nút gỡ.\n'
     '- Dòng hướng dẫn ghi rõ nhận PDF, ảnh, Word, Excel, mỗi tệp tối đa 13 MB.'),
    ('017', 'Gỡ tệp đính kèm', 'P2', 'Đã đính kèm 2 tệp.',
     '1. Bấm nút gỡ ở tệp thứ nhất.',
     '—', '- Tệp thứ nhất biến mất, tệp thứ hai còn nguyên.'),
    ('018', 'Cảnh báo khi rời màn lúc chưa lưu', 'P0', 'Đang ở màn lập phiếu.',
     '1. Chọn Người nhận.\n2. Bấm nút Quay lại.',
     '—',
     '- Phần mềm hỏi xác nhận rời khỏi trang.\n'
     '- Chọn ở lại: giữ nguyên dữ liệu; chọn rời đi: bỏ mọi thay đổi.'),
    ('019', 'Mã phiếu sinh tự động không trùng', 'P0', 'Vừa lập liên tiếp 3 phiếu.',
     '1. Lập 3 phiếu liên tiếp.\n2. Xem mã ở danh sách.',
     '—', '- Ba mã khác nhau, dạng ĐCHG kèm 5 chữ số, không trùng phiếu cũ.'),
    ('020', 'Hạn giữ không đổi sau khi chọn lô', 'P0',
     'Lô nguồn có hạn giữ 12/07/2026.',
     '1. Chọn lô đó ở ô Từ xuất giữ.\n2. Quan sát cột Hạn giữ.',
     '—',
     '- ⚠️ Cột Hạn giữ hiện đúng 12/07/2026 và KHÔNG sửa được — điều chuyển giữ nguyên hạn giữ.'),
]

# ============================================================== V
S5 = [
    ('001', 'Nút Sửa chỉ hiện với phiếu Không duyệt của mình', 'P0',
     'Tài khoản A có: phiếu 1 Không duyệt do A lập, phiếu 2 Chờ TP duyệt do A lập, phiếu 3 '
     'Đã duyệt do A lập.',
     '1. Xem cột Hành động của từng phiếu.',
     '—',
     '- Phiếu 1: có biểu tượng Sửa và Xóa.\n'
     '- ⚠️ Phiếu 2 và 3: KHÔNG có (khác hai màn cùng nhóm — ở đây không có bản nháp).'),
    ('002', 'Mở màn Sửa', 'P0', 'Có phiếu Không duyệt do chính mình lập.',
     '1. Bấm biểu tượng bút chì ở cột Hành động.',
     '—',
     '- Tiêu đề màn ghi "Sửa yêu cầu điều chuyển hàng giữ: <mã phiếu>".\n'
     '- Ô Trạng thái hiển thị nhãn ĐỎ "Không duyệt".\n'
     '- Ô Mã phiếu và Phòng ban yêu cầu bị khóa.'),
    ('003', 'Dữ liệu đã lưu được nạp lại đúng', 'P0',
     'Phiếu Không duyệt có 1 dòng hàng đã chọn lô nguồn và số lượng 2.',
     '1. Mở màn Sửa của phiếu đó.',
     '—',
     '- Người nhận, Khách hàng nhận và Ghi chú hiện đúng dữ liệu đã lưu.\n'
     '- Dòng hàng hiện đúng lô nguồn, số lượng 2, hạn giữ và hợp đồng đã chọn.'),
    ('004', 'Sửa Người nhận rồi gửi lại', 'P0', 'Đang ở màn Sửa.',
     '1. Đổi Người nhận sang nhân viên khác.\n2. Bấm Gửi duyệt.',
     'Người nhận: đổi sang Nguyễn Hồng Quân',
     '- Phiếu chuyển sang trạng thái Chờ TP duyệt.\n'
     '- ⚠️ Thông báo được gửi cho Trưởng phòng quản lý phòng ban của NGƯỜI NHẬN MỚI.\n'
     '- Lịch sử thay đổi ghi nhận việc đổi người nhận.'),
    ('005', 'Sửa lại thì đặt lại toàn bộ ba cấp duyệt', 'P0',
     'Phiếu đã được Trưởng phòng và Ban giám đốc duyệt, sau đó bị Kế toán từ chối.',
     '1. Người lập mở màn Sửa, chỉnh số lượng.\n2. Bấm Gửi duyệt.\n'
     '3. Mở màn chi tiết xem khối Lịch sử duyệt.',
     '—',
     '- Phiếu quay về trạng thái Chờ TP duyệt.\n'
     '- ⚠️ Dấu duyệt của CẢ BA cấp bị đặt lại; phiếu phải đi lại quy trình từ đầu, không nhảy '
     'thẳng sang Kế toán.'),
    ('006', 'Thêm dòng hàng vào phiếu đang sửa', 'P1', 'Phiếu có 1 dòng hàng.',
     '1. Bấm Thêm hàng hóa, chọn thêm 1 mặt hàng.\n2. Chọn lô nguồn và nhập số lượng.\n'
     '3. Bấm Gửi duyệt.',
     'Chuyển: 1',
     '- Phiếu có 2 dòng sau khi lưu.\n- Lịch sử thay đổi ghi nhận dòng hàng được thêm.'),
    ('007', 'Mở màn Sửa của phiếu đang chờ duyệt bằng đường dẫn', 'P0',
     'Phiếu đang ở trạng thái Chờ KT duyệt do chính mình lập.',
     '1. Gõ thẳng đường dẫn màn sửa của phiếu đó.',
     '—',
     '- Phần mềm không cho vào màn sửa.\n- Nội dung phiếu không thay đổi.'),
    ('008', 'Sửa phiếu của người khác qua đường dẫn', 'P0',
     'Phiếu Không duyệt do tài khoản B lập.',
     '1. Đăng nhập bằng A.\n2. Gõ đường dẫn màn sửa của phiếu đó.',
     '—', '- Phần mềm từ chối, không hiển thị dữ liệu phiếu.'),
    ('009', 'Cảnh báo rời màn Sửa khi chưa lưu', 'P1', 'Đang ở màn Sửa.',
     '1. Đổi Ghi chú.\n2. Bấm Quay lại.',
     '—', '- Phần mềm hỏi xác nhận rời khỏi trang.'),
]

# ============================================================== VI
S6 = [
    ('001', 'Mở màn chi tiết', 'P0', 'Có phiếu trong phạm vi quyền.',
     '1. Bấm vào mã phiếu.',
     '—',
     '- Tiêu đề ghi "Chi tiết yêu cầu điều chuyển hàng giữ: <mã phiếu>".\n'
     '- Có đủ khối Thông tin chung, File đính kèm, Chi tiết, Lịch sử duyệt (nếu đã có ai duyệt) '
     'và Lịch sử thay đổi.'),
    ('002', 'Mọi ô ở chế độ chỉ đọc', 'P0', 'Đang ở màn chi tiết.',
     '1. Thử bấm vào ô Người nhận, Khách hàng nhận, Ghi chú và các ô trong bảng.',
     '—',
     '- Không sửa được ô nào.\n'
     '- ⚠️ Kể cả người đúng cấp duyệt cũng KHÔNG sửa được số lượng và lô nguồn.'),
    ('003', 'Khối Lịch sử duyệt hiển thị đủ các cấp đã đi qua', 'P0',
     'Phiếu đã qua đủ ba cấp và đang ở trạng thái Đã duyệt.',
     '1. Mở phiếu, xem khối Lịch sử duyệt.',
     '—',
     '- Có ba dòng: Trưởng phòng, Ban giám đốc, Kế toán.\n'
     '- Mỗi dòng đủ Người duyệt, Thời gian và Ghi chú.'),
    ('004', 'Dòng duyệt không ghi chú vẫn hiển thị', 'P0',
     'Có phiếu mà cấp duyệt đã duyệt nhưng để trống ô ghi chú.',
     '1. Mở phiếu, xem khối Lịch sử duyệt.',
     '—',
     '- ⚠️ Dòng đó VẪN hiển thị, chỉ để trống cột Ghi chú.\n'
     '- Không được mất dòng chỉ vì không có ghi chú.'),
    ('005', 'Phiếu chưa qua bước nào thì không có khối Lịch sử duyệt', 'P1',
     'Phiếu vừa lập, đang ở Chờ TP duyệt.',
     '1. Mở phiếu.',
     '—', '- Không hiển thị khối Lịch sử duyệt.'),
    ('006', 'Bấm số ở cột Đang giữ mở lịch sử lô', 'P1', 'Đang ở màn chi tiết.',
     '1. Bấm vào con số ở cột Đang giữ của một dòng.',
     '—', '- Mở cửa sổ lịch sử tăng giảm của đúng lô hàng giữ đó.'),
    ('007', 'Xem tệp đính kèm', 'P1', 'Phiếu có 1 tệp đính kèm.',
     '1. Bấm vào tên tệp ở khối File đính kèm.',
     '—', '- Tệp mở ở tab mới, xem được nội dung.'),
    ('008', 'Phiếu không có tệp đính kèm', 'P2', 'Phiếu không đính kèm gì.',
     '1. Mở phiếu.',
     '—', '- Khối File đính kèm hiện dòng "Chưa có tệp đính kèm".'),
    ('009', 'Nút cuối màn khớp với cột Hành động ngoài danh sách', 'P0',
     'Một phiếu Không duyệt do chính mình lập.',
     '1. Đếm nút ở cột Hành động ngoài danh sách.\n2. Mở phiếu, đếm nút cuối màn.',
     '—',
     '- ⚠️ Số nút khớp nhau, chỉ khác ở chỗ màn chi tiết có thêm nút Từ chối cho người đúng cấp '
     'duyệt.'),
    ('010', 'Mở phiếu Không duyệt của người khác bằng đường dẫn', 'P0',
     'Phiếu Không duyệt do tài khoản B lập; tài khoản A có quyền xem theo tổng công ty.',
     '1. Đăng nhập bằng A.\n2. Gõ đường dẫn màn chi tiết của phiếu đó.',
     '—',
     '- Phần mềm báo không có quyền xem phiếu này.\n- Không hiển thị nội dung phiếu.'),
    ('011', 'Mở phiếu bằng mã không tồn tại', 'P1', 'Đang đăng nhập.',
     '1. Gõ đường dẫn màn chi tiết với mã số không có thật.',
     '—', '- Phần mềm báo không tìm thấy dữ liệu, không treo trang.'),
]

# ============================================================== VII
S7 = [
    ('001', 'Trưởng phòng duyệt — phiếu không phải trình Ban giám đốc', 'P0',
     'Phiếu X ở Chờ TP duyệt, các dòng hàng đều gắn hợp đồng đã thu đủ tỉ lệ quy định. Tài khoản '
     'E có quyền Trưởng phòng duyệt hàng giữ và quản lý phòng của NGƯỜI NHẬN.',
     '1. Đăng nhập bằng E.\n2. Mở phiếu X.\n3. Bấm nút TP duyệt.',
     '—',
     '- Hiện thông báo "Yêu cầu đã được chuyển đến Kế toán.".\n'
     '- Phiếu chuyển thẳng sang Chờ KT duyệt, BỎ QUA bước Ban giám đốc.\n'
     '- Khối Lịch sử duyệt có thêm dòng Trưởng phòng.'),
    ('002', 'Trưởng phòng duyệt — phiếu phải trình Ban giám đốc', 'P0',
     'Phiếu Y ở Chờ TP duyệt, có dòng hàng không gắn hợp đồng với tổng giá trị vượt hạn mức '
     'của công ty.',
     '1. Mở phiếu Y.\n2. Bấm TP duyệt.',
     '—',
     '- Hiện thông báo "Yêu cầu đã được chuyển đến Ban giám đốc.".\n'
     '- Phiếu chuyển sang trạng thái Chờ BGĐ duyệt.'),
    ('003', 'Ban giám đốc duyệt', 'P0',
     'Phiếu ở Chờ BGĐ duyệt; tài khoản F có quyền Ban giám đốc duyệt hàng giữ cùng công ty.',
     '1. Mở phiếu.\n2. Bấm BGĐ duyệt.',
     '—',
     '- Hiện "Yêu cầu đã được chuyển đến Kế toán.".\n- Phiếu chuyển sang Chờ KT duyệt.'),
    ('004', 'Kế toán duyệt — hàng đổi chủ đúng', 'P0',
     'Phiếu ở Chờ KT duyệt, 1 dòng: hàng H, lô nguồn của A (khách K, hạn 28/06/2026) đang giữ 5, '
     'số lượng chuyển 2. Người nhận B, khách hàng nhận L. Trước khi duyệt B chưa giữ hàng H nào.',
     '1. Ghi lại số lượng lô nguồn trước khi duyệt.\n2. Bấm KT duyệt.\n'
     '3. Mở màn Danh sách hàng giữ kiểm tra lại.',
     'Chuyển: 2',
     '- Hiện "Duyệt phiếu thành công.", phiếu chuyển sang Đã duyệt.\n'
     '- Lô của A (khách K, hạn 28/06/2026) còn 3.\n'
     '- ⚠️ Xuất hiện lô mới của B với khách L, hàng H, số lượng 2 và HẠN GIỮ VẪN LÀ 28/06/2026.\n'
     '- Lịch sử biến động của hàng hóa có ĐÚNG HAI dòng: một dòng trừ 2 và một dòng cộng 2.'),
    ('005', 'Kế toán duyệt khi lô đích đã tồn tại', 'P0',
     'Người nhận B đã có sẵn lô hàng H, khách L, hạn 28/06/2026 với số lượng 4. Phiếu chuyển '
     'thêm 2 từ lô của A cùng hạn giữ.',
     '1. Bấm KT duyệt.\n2. Kiểm tra hai lô.',
     '—',
     '- Lô của B tăng từ 4 lên 6 (cộng dồn, KHÔNG tạo lô thứ hai).\n'
     '- Lô của A giảm đúng 2.'),
    ('006', 'Hai bước đầu không đụng tới hàng giữ', 'P0',
     'Phiếu ở Chờ TP duyệt với 1 dòng chuyển 2.',
     '1. Ghi lại số lượng lô nguồn.\n2. Trưởng phòng duyệt.\n3. Ban giám đốc duyệt.\n'
     '4. Kiểm tra lại số lượng lô nguồn.',
     '—',
     '- ⚠️ Sau bước Trưởng phòng và Ban giám đốc, số lượng các lô KHÔNG đổi.\n'
     '- Chỉ sau bước Kế toán mới thay đổi.'),
    ('007', 'Trưởng phòng không quản lý phòng ban của người nhận', 'P0',
     'Tài khoản E có quyền Trưởng phòng duyệt hàng giữ nhưng không quản lý phòng ban của NGƯỜI '
     'NHẬN trên phiếu Z (Chờ TP duyệt, cùng công ty).',
     '1. Mở phiếu Z.',
     '—',
     '- Nút TP duyệt và Từ chối KHÔNG hiển thị.\n'
     '- ⚠️ Chỉ có quyền là chưa đủ; phải quản lý phòng ban của NGƯỜI NHẬN.'),
    ('008', 'Duyệt sai cấp', 'P0',
     'Phiếu đang ở Chờ TP duyệt; tài khoản chỉ có quyền Kế toán duyệt hàng giữ.',
     '1. Mở phiếu.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng duyệt.',
     '—',
     '- Nút KT duyệt KHÔNG hiển thị.\n'
     '- Gọi thẳng chức năng: phần mềm báo không có quyền duyệt bước này; trạng thái phiếu và '
     'hàng giữ không đổi.'),
    ('009', 'Lô nguồn không còn đủ hàng lúc duyệt', 'P0',
     'Phiếu chuyển 5 nhưng lô nguồn chỉ còn 2 do đã bị hủy giữ bớt sau khi lập phiếu.',
     '1. Kế toán bấm KT duyệt.\n2. Kiểm tra hàng giữ.',
     '—',
     '- Phần mềm báo lỗi và KHÔNG duyệt.\n'
     '- ⚠️ Hàng giữ giữ nguyên, không bị trừ một phần rồi dừng giữa chừng.'),
    ('010', 'Hai người cùng duyệt một phiếu', 'P0',
     'Phiếu ở Chờ KT duyệt; hai kế toán cùng mở phiếu trên hai máy.',
     '1. Máy 1 bấm KT duyệt thành công.\n2. Máy 2 bấm KT duyệt (chưa tải lại trang).',
     '—',
     '- Máy 2 nhận thông báo "Phiếu không ở trạng thái chờ duyệt.".\n'
     '- ⚠️ Hàng giữ chỉ chuyển MỘT lần.'),
    ('011', 'Từ chối ở cấp Trưởng phòng', 'P0', 'Phiếu ở Chờ TP duyệt.',
     '1. Mở phiếu, bấm nút Từ chối.\n2. Nhập lý do.\n3. Xác nhận.',
     'Lý do: Người nhận không đúng bộ phận phụ trách khách hàng',
     '- ⚠️ Nhãn nút là "Từ chối" nhưng sau khi xác nhận, trạng thái phiếu hiển thị là '
     '"Không duyệt" (nhãn đỏ).\n'
     '- Cột Lý do không duyệt ngoài danh sách hiện đúng nội dung.\n'
     '- Người lập nhận được thông báo.'),
    ('012', 'Không có nút Từ chối ở cột Hành động', 'P1',
     'Phiếu đang chờ chính mình duyệt.',
     '1. Quan sát cột Hành động của phiếu đó.',
     '—',
     '- ⚠️ Cột Hành động chỉ có biểu tượng duyệt, In và Lịch sử; KHÔNG có nút Từ chối.\n'
     '- Muốn từ chối phải mở phiếu ra.'),
    ('013', 'Từ chối bỏ trống lý do', 'P0', 'Cửa sổ Từ chối đang mở.',
     '1. Không nhập gì.\n2. Bấm nút xác nhận.',
     'Lý do: (bỏ trống)',
     '- Phần mềm báo bắt buộc phải nhập lý do ngay dưới ô.\n'
     '- ⚠️ Cửa sổ KHÔNG đóng, phiếu không đổi trạng thái.'),
    ('014', 'Từ chối với lý do quá dài', 'P1', 'Cửa sổ Từ chối đang mở.',
     '1. Nhập lý do dài hơn 255 ký tự.\n2. Bấm xác nhận.',
     'Lý do: chuỗi 260 ký tự',
     '- Phần mềm báo "Không được vượt quá 255 ký tự" hoặc ô không cho nhập quá giới hạn.'),
    ('015', 'Từ chối ở cấp Kế toán', 'P0', 'Phiếu ở Chờ KT duyệt.',
     '1. Kế toán bấm Từ chối, nhập lý do và xác nhận.\n2. Kiểm tra hàng giữ.',
     'Lý do: Hàng đã có khách khác đặt',
     '- Phiếu chuyển sang trạng thái Không duyệt.\n'
     '- ⚠️ Hàng giữ KHÔNG thay đổi vì phiếu chưa từng được duyệt xong.'),
    ('016', 'Phiếu Không duyệt chỉ người lập nhìn thấy', 'P0',
     'Phiếu vừa bị từ chối; tài khoản khác có quyền xem theo tổng công ty.',
     '1. Đăng nhập bằng tài khoản khác.\n2. Lọc Trạng thái = Không duyệt.',
     'Trạng thái: Không duyệt',
     '- ⚠️ Không thấy phiếu vừa bị từ chối của người khác.'),
]

# ============================================================== VIII
S8 = [
    ('001', 'Xóa phiếu Không duyệt của mình', 'P0',
     'Phiếu ở trạng thái Không duyệt do chính mình lập.',
     '1. Bấm biểu tượng thùng rác.\n2. Đọc hộp thoại.\n3. Bấm Xóa.',
     '—',
     '- Hộp thoại có tiêu đề "Xác nhận xóa" và ghi rõ mã phiếu.\n'
     '- Sau khi xác nhận: danh sách tải lại, không còn phiếu đó, N giảm 1.'),
    ('002', 'Hủy thao tác xóa', 'P0', 'Hộp thoại xác nhận xóa đang mở.',
     '1. Bấm nút Hủy.',
     '—', '- Hộp thoại đóng, phiếu vẫn còn nguyên.'),
    ('003', 'Nút Xóa ẩn với phiếu đang chờ duyệt', 'P0',
     'Phiếu ở Chờ TP duyệt do chính mình lập.',
     '1. Xem cột Hành động và nút cuối màn chi tiết.',
     '—', '- Không có nút Xóa ở cả hai nơi; nút bị ẩn hẳn.'),
    ('004', 'Nút Xóa ẩn với phiếu đã duyệt', 'P0', 'Phiếu ở trạng thái Đã duyệt.',
     '1. Xem cột Hành động.',
     '—', '- Không có nút Xóa.'),
    ('005', 'Xóa phiếu đã duyệt bằng cách gọi thẳng chức năng', 'P0',
     'Phiếu ở trạng thái Đã duyệt.',
     '1. Dùng công cụ kiểm thử gọi thẳng chức năng xóa.',
     '—',
     '- Phần mềm từ chối.\n- ⚠️ Phiếu vẫn còn và hàng giữ đã chuyển không bị ảnh hưởng.'),
    ('006', 'Xóa phiếu rồi mở lại bằng đường dẫn cũ', 'P1', 'Vừa xóa một phiếu.',
     '1. Gõ đường dẫn màn chi tiết của phiếu vừa xóa.',
     '—', '- Phần mềm báo không tìm thấy dữ liệu, không treo trang.'),
]

# ============================================================== IX
S9 = [
    ('001', 'In một phiếu từ cột Hành động', 'P0', 'Có phiếu trong phạm vi quyền.',
     '1. Bấm biểu tượng máy in ở cột Hành động.',
     '—',
     '- Mở tab mới, tiêu đề tab ghi "In phiếu yêu cầu điều chuyển hàng giữ".\n'
     '- Bản xem trước hiển thị khung tờ giấy A4 NGANG trên nền xám, nút In canh phải mép giấy.'),
    ('002', 'Nội dung bản in phiếu', 'P0', 'Phiếu đã duyệt đủ ba cấp, có 3 dòng hàng.',
     '1. Mở bản in của phiếu đó.',
     '—',
     '- Phần đầu có logo và thông tin công ty GHI TRÊN PHIẾU.\n'
     '- Tiêu đề "PHIẾU YÊU CẦU ĐIỀU CHUYỂN HÀNG GIỮ", số phiếu và ngày tạo.\n'
     '- Khối thông tin: Người yêu cầu, Phòng ban, Người nhận, Trạng thái.\n'
     '- Bảng hàng hóa đủ cột STT, Tên hàng hóa, Mã hàng hóa, ĐVT, Từ xuất giữ, Đang giữ, '
     'Chuyển, Hạn giữ, Hợp đồng và dòng Tổng cộng.\n'
     '- Bảng lịch sử duyệt đủ 3 dòng với 4 cột Cấp duyệt, Người duyệt, Thời gian, Ghi chú.\n'
     '- Khối ký có 4 ô: Người lập, Trưởng phòng, Ban giám đốc, Kế toán.'),
    ('003', 'Bản in lấy đúng công ty của phiếu', 'P0',
     'Người đăng nhập thuộc công ty 1; phiếu thuộc công ty 4 (Tân Phát ETEK Sài Gòn).',
     '1. Mở bản in của phiếu đó.',
     '—',
     '- ⚠️ Phần đầu chứng từ hiển thị thông tin công ty 4, KHÔNG phải công ty người đang in.'),
    ('004', 'Dòng Tổng cộng trên bản in', 'P1',
     'Phiếu có 3 dòng với số lượng Chuyển lần lượt 1, 1, 1.',
     '1. Mở bản in, xem dòng Tổng cộng.',
     '—', '- Dòng Tổng cộng ghi 3.'),
    ('005', 'Bản in giữ dòng duyệt không có ghi chú', 'P0',
     'Phiếu có cấp duyệt để trống ghi chú.',
     '1. Mở bản in, xem bảng lịch sử duyệt.',
     '—', '- ⚠️ Dòng đó vẫn được in, chỉ để trống cột Ghi chú.'),
    ('006', 'In danh sách theo bộ lọc', 'P0', 'Đang lọc còn 48 phiếu.',
     '1. Bấm nút In trên thanh công cụ.',
     '—',
     '- Mở tab mới, tiêu đề "In danh sách yêu cầu điều chuyển hàng giữ".\n'
     '- Dòng "Tổng số phiếu" ghi đúng 48.\n'
     '- ⚠️ In toàn bộ phiếu khớp bộ lọc, không chỉ 10 dòng của trang đang xem.'),
    ('007', 'Bản in danh sách áp cả ô lọc Số hợp đồng', 'P0',
     'Đang lọc Số hợp đồng = HĐ_TPE_HN_KD2_26_0955_VDA, còn 6 phiếu.',
     '1. Bấm nút In trên thanh công cụ.',
     '—',
     '- ⚠️ Dòng Tổng số phiếu ghi 6, đúng theo điều kiện lọc Số hợp đồng.'),
    ('008', 'Cột trên bản in danh sách', 'P1', 'Đang ở bản in danh sách.',
     '1. Đọc tiêu đề các cột.',
     '—',
     '- Có các cột STT, Mã phiếu, Người tạo, Ngày tạo, Người nhận, Khách nhận, Trạng thái, '
     'Người duyệt, Ngày duyệt.'),
    ('009', 'Mở cửa sổ chọn trường xuất Excel', 'P0', 'Đang ở màn danh sách.',
     '1. Bấm nút Xuất Excel.',
     '—',
     '- Cửa sổ "Chọn trường xuất Excel" mở ra.\n'
     '- Mặc định đang chọn 13/13 trường.\n'
     '- Có nút Chọn tất cả và Bỏ chọn hết.'),
    ('010', 'Xuất Excel đủ trường', 'P0', 'Đang lọc còn 48 phiếu.',
     '1. Giữ nguyên 13 trường.\n2. Bấm Xuất file.\n3. Mở tệp vừa tải.',
     '—',
     '- Hiện thông báo xuất thành công và cửa sổ đóng lại.\n'
     '- Tệp có đúng 48 dòng dữ liệu.\n'
     '- Có đủ 13 cột, trong đó có Người nhận, Khách nhận và Lý do không duyệt.'),
    ('011', 'Thứ tự cột theo thứ tự chọn', 'P0', 'Cửa sổ chọn trường đang mở.',
     '1. Bấm Bỏ chọn hết.\n2. Chọn lần lượt: Người nhận, Mã phiếu, Khách nhận.\n'
     '3. Bấm Xuất file.',
     'Trường xuất: Người nhận, Mã phiếu, Khách nhận',
     '- Tệp có đúng 3 cột theo THỨ TỰ đã chọn.'),
    ('012', 'Xuất Excel theo bộ lọc đang áp', 'P0',
     'Đang lọc còn 48 phiếu, đang xem trang 1 (10 dòng).',
     '1. Xuất file và đếm số dòng trong tệp.',
     '—', '- ⚠️ Tệp có đủ 48 dòng, không phải 10 dòng của trang đang xem.'),
    ('013', 'Nút Xuất file bị khóa trong lúc xuất', 'P1', 'Danh sách lớn.',
     '1. Bấm Xuất file và quan sát nút.',
     '—', '- Nút bị khóa cho tới khi xong; không tạo hai tệp trùng.'),
    ('014', 'Xuất Excel khi danh sách rỗng', 'P2', 'Đang lọc ra 0 kết quả.',
     '1. Xuất file.',
     '—', '- Tệp chỉ có dòng tiêu đề, không báo lỗi hệ thống.'),
    ('015', 'Số liệu trong tệp Excel dùng định dạng số', 'P1', 'Tệp vừa xuất.',
     '1. Mở tệp, bấm vào một ô có giá trị số.',
     '—',
     '- Ô là số thật, tính tổng được.\n'
     '- ⚠️ Không xuất hiện cảnh báo số đang lưu dưới dạng chữ.'),
]

# ============================================================== X
S10 = [
    ('001', 'Bỏ trống Người nhận', 'P0', 'Đang ở màn lập phiếu, đã có dòng hàng hợp lệ.',
     '1. Không chọn Người nhận.\n2. Bấm Gửi duyệt.',
     'Người nhận: (bỏ trống)',
     '- Hiện lỗi đỏ "Bắt buộc phải chọn" ngay dưới ô Người nhận.\n'
     '- Phiếu KHÔNG được lưu, dữ liệu đã nhập vẫn còn.'),
    ('002', 'Bỏ trống Khách hàng nhận', 'P0', 'Đang ở màn lập phiếu.',
     '1. Không chọn Khách hàng nhận.\n2. Bấm Gửi duyệt.',
     'Khách hàng nhận: (bỏ trống)',
     '- Hiện lỗi đỏ "Bắt buộc phải chọn" ngay dưới ô Khách hàng nhận.'),
    ('003', 'Chưa thêm dòng hàng nào', 'P0', 'Đã chọn Người nhận và Khách hàng nhận.',
     '1. Bấm Gửi duyệt.',
     '—', '- Phần mềm báo bắt buộc phải chọn hàng hóa. Phiếu không được lưu.'),
    ('004', 'Chưa chọn lô ở ô Từ xuất giữ', 'P0', 'Đã thêm 1 dòng hàng nhưng chưa chọn lô.',
     '1. Nhập số lượng và bấm Gửi duyệt.',
     'Từ xuất giữ: (bỏ trống)',
     '- Báo lỗi "Từ xuất giữ – Lô hàng giữ không còn tồn tại hoặc không thuộc người lập phiếu." '
     'tại dòng.\n- Phiếu không được lưu.'),
    ('005', 'Chọn cùng một lô ở hai dòng', 'P0',
     'Cùng một hàng hóa được thêm hai lần với cùng một lô nguồn.',
     '1. Chọn cùng lô cho cả hai dòng.\n2. Bấm Gửi duyệt.',
     '—',
     '- Báo "Từ xuất giữ – Lô hàng giữ này đã được chọn ở dòng …".\n'
     '- ⚠️ Thông báo nêu rõ số thứ tự dòng bị trùng.'),
    ('006', 'Chọn lô đã hết hạn giữ', 'P0',
     'Người lập có một lô đã quá hạn giữ.',
     '1. Chọn lô đó ở ô Từ xuất giữ.\n2. Bấm Gửi duyệt.',
     '—',
     '- Báo "Từ xuất giữ – Lô hàng đã hết hạn giữ ngày …".\n'
     '- ⚠️ Thông báo nêu rõ ngày hết hạn. Phiếu không được lưu.'),
    ('007', 'Số lượng bằng 0', 'P0', 'Đã chọn lô nguồn.',
     '1. Nhập 0 vào ô Chuyển.\n2. Bấm Gửi duyệt.',
     'Chuyển: 0',
     '- Báo "Số lượng chuyển – Phải lớn hơn 0." tại dòng.'),
    ('008', 'Số lượng vượt số Đang giữ', 'P0', 'Lô nguồn đang giữ 3.',
     '1. Nhập 8 vào ô Chuyển.\n2. Bấm Gửi duyệt.',
     'Đang giữ: 3; Chuyển: 8',
     '- Báo "Số lượng chuyển – Không được vượt số đang giữ (3)".\n'
     '- ⚠️ Phần mềm GIỮ NGUYÊN số 8 người dùng đã gõ, không tự kéo về 3.'),
    ('009', 'Số lượng vượt 6 chữ số', 'P1', 'Đã chọn lô nguồn.',
     '1. Nhập 1234567 vào ô Chuyển.',
     'Chuyển: 1234567',
     '- Báo "Không được vượt quá 6 chữ số" hoặc lỗi tương đương.'),
    ('010', 'Nhập chữ vào ô số lượng', 'P0', 'Đã chọn lô nguồn.',
     '1. Gõ "abc" vào ô Chuyển.',
     'Chuyển: abc',
     '- Ô chỉ nhận ký tự số.'),
    ('011', 'Ghi chú vượt 255 ký tự', 'P1', 'Đang ở màn lập phiếu.',
     '1. Nhập chuỗi 300 ký tự vào ô Ghi chú.',
     'Ghi chú: chuỗi 300 ký tự',
     '- Ô không cho nhập quá 255 ký tự, hoặc báo lỗi khi lưu.\n'
     '- ⚠️ Không tự cắt bớt rồi lưu im lặng.'),
    ('012', 'Đính kèm tệp quá 13 MB', 'P1', 'Đang ở màn lập phiếu.',
     '1. Chọn tệp PDF dung lượng 20 MB.',
     'Tệp: 20 MB',
     '- Phần mềm báo tệp vượt dung lượng cho phép và không đính kèm.'),
    ('013', 'Đính kèm định dạng không được phép', 'P1', 'Đang ở màn lập phiếu.',
     '1. Chọn một tệp nén .zip.',
     'Tệp: tai-lieu.zip',
     '- Hộp chọn tệp không cho chọn định dạng này, hoặc phần mềm báo không hỗ trợ.'),
    ('014', 'Lỗi hiển thị đúng tại dòng bị sai', 'P0',
     'Phiếu có 5 dòng, chỉ dòng thứ 3 nhập số lượng vượt số đang giữ.',
     '1. Bấm Gửi duyệt.',
     '—',
     '- ⚠️ Lỗi đỏ hiện ngay dưới ô của DÒNG THỨ 3, không phải chỉ một thông báo chung.\n'
     '- Màn hình tự cuộn tới dòng bị lỗi.'),
]

# ============================================================== XI
S11 = [
    ('001', 'Lô nguồn bị hủy giữ hết trong lúc lập phiếu', 'P0',
     'Người lập mở màn lập phiếu, đã chọn lô L. Trong lúc đó lô L bị hủy giữ hết.',
     '1. Bấm Gửi duyệt.',
     '—',
     '- Phần mềm báo lô hàng giữ không còn tồn tại hoặc không thuộc người lập phiếu.\n'
     '- Phiếu không được lưu, dữ liệu trên màn vẫn còn.'),
    ('002', 'Lô nguồn hết hạn giữ giữa lúc chờ duyệt', 'P0',
     'Phiếu đang ở Chờ KT duyệt; lô nguồn đã quá hạn giữ.',
     '1. Kế toán bấm KT duyệt.',
     '—',
     '- Phần mềm xử lý nhất quán: hoặc từ chối kèm thông báo rõ ràng, hoặc duyệt và chuyển hàng '
     'với đúng hạn giữ cũ.\n'
     '- ⚠️ Không được để hàng chuyển sang người nhận với hạn giữ khác lô nguồn.'),
    ('003', 'Hàng hóa bị khóa trong danh mục', 'P1',
     'Một hàng hóa trong phiếu bị khóa ở danh mục sau khi phiếu đã lập.',
     '1. Mở màn chi tiết phiếu.',
     '—', '- Tên hàng hóa vẫn hiển thị đúng, không lỗi hệ thống.'),
    ('004', 'Hàng hóa bị xóa khỏi danh mục', 'P1',
     'Hàng hóa trong phiếu không còn trong danh mục.',
     '1. Duyệt phiếu đó ở bước Kế toán.',
     '—', '- Phần mềm báo "Hàng hoá không còn tồn tại trong danh mục." và không duyệt.'),
    ('005', 'Người nhận nghỉ việc sau khi lập phiếu', 'P1',
     'Người nhận trên phiếu đã bị vô hiệu hóa tài khoản.',
     '1. Mở màn chi tiết phiếu.',
     '—',
     '- ⚠️ Tên người nhận VẪN hiển thị đúng, không bị trống.\n'
     '- Không lỗi hệ thống.'),
    ('006', 'Hai người cùng sửa một phiếu Không duyệt', 'P1',
     'Phiếu Không duyệt của A, mở trên hai tab.',
     '1. Tab 1 sửa Ghi chú và gửi duyệt.\n2. Tab 2 (chưa tải lại) cũng bấm Gửi duyệt.',
     '—',
     '- Tab 2 nhận thông báo phiếu không còn ở trạng thái cho phép sửa.\n'
     '- Phiếu chỉ được gửi duyệt một lần.'),
    ('007', 'Xóa phiếu đang được người khác mở xem', 'P1',
     'A xóa phiếu P trong khi B đang mở màn chi tiết của P.',
     '1. B bấm nút In trên màn đang mở.',
     '—', '- Phần mềm báo không tìm thấy dữ liệu, không treo trang.'),
    ('008', 'Phiên đăng nhập hết hạn', 'P1', 'Đang mở màn danh sách.',
     '1. Để phiên hết hạn.\n2. Bấm sang trang 2.',
     '—', '- Phần mềm đưa về màn đăng nhập, không hiện lỗi kỹ thuật khó hiểu.'),
]

# ============================================================== XII
S12 = [
    ('001', 'Mở lịch sử từ cột Hành động', 'P0', 'Phiếu đã có ít nhất 1 mốc thay đổi.',
     '1. Bấm biểu tượng đồng hồ ở cột Hành động.',
     '—',
     '- Mở cửa sổ lịch sử với tiêu đề nêu tên màn và mã phiếu.\n'
     '- Danh sách hiển thị mới nhất trước.'),
    ('002', 'Mở lịch sử từ màn chi tiết', 'P0', 'Đang ở màn chi tiết phiếu.',
     '1. Kéo xuống khối Lịch sử thay đổi.\n2. Bấm nút Xem lịch sử.',
     '—',
     '- ⚠️ Khối mặc định THU GỌN, chỉ nạp dữ liệu khi bấm mở.\n'
     '- Sau khi mở, nhãn nút đổi thành Thu gọn và có thêm nút Làm mới.'),
    ('003', 'Ghi nhận mốc Tạo mới', 'P0', 'Vừa lập một phiếu mới.',
     '1. Mở lịch sử của phiếu vừa lập.',
     '—', '- Có mốc tạo mới, ghi đúng người lập và thời điểm.'),
    ('004', 'Ghi nhận mốc Chỉnh sửa kèm giá trị thay đổi', 'P0',
     'Vừa đổi Người nhận của một phiếu Không duyệt rồi gửi lại.',
     '1. Mở lịch sử.',
     '—', '- Có mốc chỉnh sửa, nêu rõ người nhận cũ và người nhận mới.'),
    ('005', 'Ghi nhận thay đổi dòng hàng', 'P0',
     'Vừa thêm 1 dòng và bỏ 1 dòng khỏi phiếu Không duyệt.',
     '1. Mở lịch sử.',
     '—',
     '- Mốc chỉnh sửa nêu rõ tên hàng được thêm và tên hàng bị bỏ.\n'
     '- Có ghi cả thay đổi về số lượng chuyển và lô nguồn nếu có.'),
    ('006', 'Ghi nhận mốc Duyệt', 'P0', 'Vừa duyệt một phiếu ở cấp Trưởng phòng.',
     '1. Mở lịch sử.',
     '—', '- Có mốc duyệt, ghi người duyệt, thời điểm và trạng thái mới.'),
    ('007', 'Ghi nhận mốc Từ chối', 'P0', 'Vừa từ chối một phiếu.',
     '1. Mở lịch sử.',
     '—', '- Có mốc từ chối, ghi người thực hiện, thời điểm và lý do.'),
    ('008', 'Thứ tự mới nhất trước', 'P0', 'Phiếu có ít nhất 3 mốc thay đổi.',
     '1. Mở lịch sử, đọc thời điểm từng mốc.',
     '—', '- ⚠️ Mốc mới nhất nằm trên cùng, cũ nhất nằm dưới cùng.'),
    ('009', 'Phiếu chưa có lịch sử', 'P1',
     'Phiếu lập từ hệ thống cũ trước khi bật ghi lịch sử.',
     '1. Mở lịch sử của phiếu đó.',
     '—', '- Hiện dòng "Chưa có lịch sử thao tác nào." — đây là đúng, không phải lỗi.'),
    ('010', 'Nút Làm mới trong khối lịch sử', 'P2', 'Khối đang mở; người khác vừa sửa phiếu.',
     '1. Bấm nút Làm mới.',
     '—', '- Danh sách được nạp lại và có thêm mốc mới nhất.'),
]

# ============================================================== XIII
S13 = [
    ('001', 'Luồng đầy đủ: lập phiếu → ba cấp duyệt → hàng đổi chủ', 'P0',
     'Nhân viên A đang giữ hàng H cho khách K, lô hạn 28/06/2026 có 5. Người nhận B thuộc phòng '
     'P1; có tài khoản đủ ba cấp duyệt cùng công ty, trong đó Trưởng phòng quản lý P1.',
     '1. A lập phiếu: chọn Người nhận B, Khách hàng nhận L, thêm hàng H, chọn lô hạn 28/06, '
     'số lượng 2, bấm Gửi duyệt.\n'
     '2. Trưởng phòng duyệt.\n3. Ban giám đốc duyệt (nếu phiếu đi qua bước này).\n'
     '4. Kế toán duyệt.\n5. Mở màn Danh sách hàng giữ để đối chiếu.',
     'Chuyển: 2',
     '- Sau bước 1: phiếu trạng thái Chờ TP duyệt ngay, hàng giữ chưa đổi.\n'
     '- Sau bước 2: Chờ BGĐ duyệt hoặc Chờ KT duyệt tuỳ điều kiện.\n'
     '- Sau bước 4: trạng thái Đã duyệt.\n'
     '- Lô của A (khách K) còn 3; xuất hiện lô của B với khách L số lượng 2.\n'
     '- ⚠️ Hạn giữ của lô mới VẪN là 28/06/2026, không đổi.\n'
     '- Lịch sử duyệt đủ các dòng đã đi qua; lịch sử thay đổi đủ các mốc.'),
    ('002', 'Luồng bị từ chối rồi sửa và duyệt lại', 'P0',
     'Phiếu vừa lập đang ở Chờ TP duyệt.',
     '1. Trưởng phòng từ chối kèm lý do.\n2. Người lập mở phiếu, bấm Sửa, chỉnh số lượng, '
     'gửi lại.\n3. Trưởng phòng duyệt.\n4. Kế toán duyệt.',
     'Lý do: Số lượng chuyển quá nhiều',
     '- Sau bước 1: phiếu chuyển sang Không duyệt, cột Lý do không duyệt có nội dung.\n'
     '- Sau bước 2: phiếu về Chờ TP duyệt và ⚠️ dấu duyệt của cả ba cấp bị đặt lại.\n'
     '- Sau bước 4: Đã duyệt và hàng chuyển đúng theo số lượng ĐÃ SỬA.'),
    ('003', 'Luồng lập phiếu rồi bị từ chối rồi xóa', 'P1',
     'Phiếu vừa bị từ chối, đang ở trạng thái Không duyệt.',
     '1. Người lập xóa phiếu.\n2. Kiểm tra hàng giữ.',
     '—',
     '- Phiếu biến mất khỏi danh sách.\n'
     '- ⚠️ Hàng giữ hoàn toàn không thay đổi vì phiếu chưa từng được duyệt xong.'),
    ('004', 'Điều chuyển rồi người nhận lập phiếu gia hạn', 'P1',
     'Vừa điều chuyển 2 sang cho B với hạn giữ 28/06/2026, ngày hiện tại còn cách hạn dưới '
     '7 ngày.',
     '1. Đăng nhập bằng B.\n2. Mở màn Yêu cầu gia hạn hàng giữ và bấm Tạo mới.',
     '—',
     '- ⚠️ Lô vừa nhận xuất hiện trong danh sách lô sắp hết hạn của B, cho phép B lập phiếu '
     'gia hạn.\n'
     '- Điều này xác nhận hàng đã thực sự đổi chủ và hạn giữ giữ nguyên.'),
    ('005', 'Kiểm tra chéo với màn Danh sách hàng giữ', 'P0',
     'Vừa duyệt xong một phiếu điều chuyển 2 đơn vị.',
     '1. Mở màn Tài chính → Giữ hàng → Danh sách hàng giữ.\n'
     '2. Lọc theo người lập, rồi lọc theo người nhận.',
     '—',
     '- Hàng giữ của người lập giảm đúng 2; hàng giữ của người nhận tăng đúng 2.\n'
     '- ⚠️ Tổng hàng giữ toàn hệ thống KHÔNG đổi — chỉ đổi chủ sở hữu.'),
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
      feature_name='Yêu cầu điều chuyển hàng giữ',
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
