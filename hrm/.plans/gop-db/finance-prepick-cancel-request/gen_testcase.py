# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man "Yeu cau huy hang giu" (phan he Tai chinh).

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

MODULE = 'YC hủy hàng giữ'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn hình Yêu cầu hủy hàng giữ (mã phiếu PYCHHG) dùng để nhân viên kinh doanh đề nghị trả '
     'lại kho phần hàng đang giữ cho khách mà khách không lấy nữa.\n'
     'Người có quyền Quản lý giữ hàng xem xét rồi hoặc trả phiếu về kèm lý do, hoặc lập '
     'Phiếu hủy hàng giữ (mã PHHG) để chấp thuận. Hàng giữ chỉ bị trừ tại thời điểm lưu '
     'phiếu hủy đó.\n'
     'Đường dẫn: Phân hệ Tài chính → Giữ hàng → Yêu cầu hủy hàng giữ.'),
    ('2. Đối tượng được tính / hiển thị',
     'Danh sách hiển thị phiếu theo phạm vi quyền của người đăng nhập:\n'
     '- Có quyền "Xem phiếu hàng giữ theo tổng công ty": toàn bộ phiếu của mọi công ty.\n'
     '- Có quyền "Xem phiếu hàng giữ theo công ty": phiếu thuộc công ty của mình.\n'
     '- Có quyền "Xem phiếu hàng giữ theo phòng ban": phiếu thuộc phòng ban mình quản lý và '
     'phòng ban của chính mình.\n'
     '- Không có quyền nào ở trên: chỉ phiếu do chính mình lập.\n'
     '- Có quyền "Quản lý giữ hàng": xem được mọi phiếu khác bản nháp.\n'
     'Ô Khách hàng ở màn lập phiếu chỉ liệt kê khách đang có hàng giữ của CHÍNH người lập, '
     'trong cùng công ty.\n'
     'Popup chọn hàng chỉ liệt kê hàng người lập đang giữ cho đúng khách hàng đã chọn.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu ở trạng thái Đang tạo của người khác: KHÔNG hiện trong danh sách và không mở được '
     'màn chi tiết.\n'
     '- Khách hàng mà người lập không giữ hàng: không có trong ô Khách hàng.\n'
     '- Hàng hóa đã có trong phiếu: bị loại khỏi popup chọn hàng để tránh chọn trùng.\n'
     '- Dòng bỏ tích ô "Cần hủy": không được gửi lên khi lưu phiếu.\n'
     '- Dòng có số lượng duyệt hủy bằng 0: bị bỏ qua, không trừ hàng giữ và không ghi nhật ký.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Hai ô "Ngày tạo từ" và "Ngày tạo đến" lọc theo NGÀY LẬP PHIẾU, không phải ngày duyệt.\n'
     'Khoảng ngày lấy trọn hai đầu mút. Chỉ nhập một đầu thì lọc một chiều.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Một phiếu yêu cầu gồm phần thông tin chung (khách hàng, ghi chú, trạng thái, phòng ban '
     'yêu cầu) và nhiều dòng hàng hóa.\n'
     'Một phiếu yêu cầu đã duyệt sinh ra đúng một Phiếu hủy hàng giữ; màn chi tiết có liên kết '
     'mở phiếu hủy đó.\n'
     'Mỗi dòng hàng có hai số lượng: "Yêu cầu hủy" (người lập đề nghị) và "Duyệt hủy" (người '
     'duyệt chấp thuận).'),
    ('6. Quy tắc cộng dồn / deduplicate',
     'Mỗi hàng hóa chỉ được thêm một lần vào phiếu; popup tự loại hàng đã có.\n'
     'Khi lập phiếu hủy, phần mềm trừ hàng giữ theo thứ tự hạn giữ sớm trước, muộn sau, cộng '
     'dồn qua nhiều lô cho tới khi đủ số lượng duyệt hủy.\n'
     'Số lượng dùng để tìm lô tồn tính theo NGƯỜI LẬP PHIẾU YÊU CẦU, không phải người lập '
     'phiếu hủy.'),
    ('7. Phân quyền cấp',
     'Quyền thao tác:\n'
     '- Quản lý giữ hàng\n'
     'Quyền phạm vi dữ liệu:\n'
     '- Xem phiếu hàng giữ theo tổng công ty\n'
     '- Xem phiếu hàng giữ theo công ty\n'
     '- Xem phiếu hàng giữ theo phòng ban\n'
     'Màn hình KHÔNG có quyền riêng cho Thêm / Sửa / Xóa: ai đăng nhập cũng lập được phiếu cho '
     'hàng giữ của chính mình, và chỉ sửa/xóa được phiếu của mình khi phiếu còn Đang tạo.'),
    ('8. Cách tính các ô thống kê',
     'Ô "Hiển thị a–b / N": a là dòng đầu trang, b là dòng cuối trang, N là tổng số phiếu khớp '
     'bộ lọc TRONG PHẠM VI QUYỀN của người đang xem.\n'
     'Cột "Có thể hủy" = số lượng hàng giữ còn có thể hủy, đã TRỪ phần đang nằm trong đề nghị '
     'xuất kho chưa hoàn thành.\n'
     'Cột "Có thể giữ" ở màn chi tiết = tồn kho khả dụng tại thời điểm mở phiếu; là số tham '
     'khảo, khác với số đã yêu cầu hủy và số đã duyệt hủy.\n'
     'Dòng "Tổng cộng" trên bản in = tổng cột SL yêu cầu hủy của các dòng được in.'),
    ('9. Ghi chú đọc bảng',
     'Các bẫy dễ sai nhất của màn này:\n'
     '- Màn này KHÔNG có nút "Duyệt" thông thường; duyệt chính là bấm "Tạo phiếu hủy hàng giữ" '
     'để lập phiếu hủy. Hàng chỉ bị trừ khi phiếu hủy được lưu.\n'
     '- Người duyệt được cắt bớt số lượng nên "Duyệt hủy" có thể nhỏ hơn "Yêu cầu hủy".\n'
     '- Ba con số "Có thể hủy", "Có thể giữ" và số trên phiếu là ba thứ khác nhau, đừng so '
     'với nhau.\n'
     '- Lưu nháp KHÔNG bắt buộc có dòng hàng, nhưng Lưu và gửi duyệt thì bắt buộc.\n'
     '- Ô Khách hàng bị khóa ở màn Sửa.\n'
     '- Trạng thái "Đang tạo" hiển thị màu XÁM (nháp), không phải màu đỏ.\n'
     '- Phiếu bị trả về quay lại đúng trạng thái "Đang tạo", không có trạng thái riêng.\n'
     '- Thanh công cụ màn danh sách hiện chưa có nút In danh sách; muốn xem phải mở bằng '
     'đường dẫn trực tiếp.\n'
     '- Nhóm test bảo mật gọi thẳng chức năng bằng công cụ kiểm thử dành cho tester kỹ thuật.'),
]

ROLE_TCS = [
    ('00', 'Tài khoản không có quyền nào của nhóm hàng giữ vẫn vào được màn hình', 'P0',
     'Tài khoản A không có quyền Quản lý giữ hàng và không có quyền xem theo cấp; A đã lập '
     '8 phiếu; toàn hệ thống có 3.478 phiếu.',
     '1. Đăng nhập bằng tài khoản A.\n2. Vào Tài chính → Giữ hàng → Yêu cầu hủy hàng giữ.',
     '—',
     '- Màn hình mở được, không báo lỗi quyền.\n'
     '- Danh sách chỉ có 8 phiếu do A lập.\n'
     '- Ô "Hiển thị a–b / N" ghi N = 8.\n'
     '- Nút Tạo mới vẫn hiển thị.\n'
     '- Bảng lọc nâng cao KHÔNG có ô Công ty và ô Phòng ban.'),
    ('01', 'Quyền "Quản lý giữ hàng" thấy mọi phiếu khác bản nháp', 'P0',
     'Tài khoản B có quyền Quản lý giữ hàng. Hệ thống có 3.478 phiếu đã duyệt, 43 phiếu nháp '
     'của nhiều người khác nhau.',
     '1. Đăng nhập bằng B.\n2. Mở màn danh sách và đọc N.\n3. Lọc Trạng thái = Đang tạo.',
     '—',
     '- N bao gồm mọi phiếu khác bản nháp.\n'
     '- ⚠️ Lọc trạng thái Đang tạo chỉ ra phiếu nháp của CHÍNH B, không thấy nháp của người khác.'),
    ('02', 'Quyền "Quản lý giữ hàng" hiện nút duyệt đúng phiếu', 'P0',
     'Tài khoản B có quyền Quản lý giữ hàng. Phiếu X ở trạng thái Chờ duyệt; phiếu Y đã duyệt; '
     'phiếu Z là nháp của chính B.',
     '1. Đăng nhập bằng B.\n2. Xem cột Hành động của X, Y, Z.\n3. Mở từng phiếu.',
     '—',
     '- Phiếu X: có biểu tượng duyệt; mở ra có nút "Tạo phiếu hủy hàng giữ" và "Không duyệt".\n'
     '- Phiếu Y: KHÔNG có hai nút trên.\n'
     '- Phiếu Z: chỉ có Sửa, Xóa, In, Lịch sử.'),
    ('03', 'Quyền "Xem phiếu hàng giữ theo tổng công ty"', 'P0',
     'Tài khoản C chỉ có quyền này. Hệ thống có phiếu của ít nhất 2 công ty.',
     '1. Đăng nhập bằng C.\n2. Mở màn danh sách.\n3. Lọc lần lượt từng công ty.',
     '—',
     '- Thấy phiếu của mọi công ty.\n'
     '- Bảng lọc CÓ ô Công ty và ô Phòng ban.\n'
     '- Nút duyệt không hiển thị vì C không có quyền Quản lý giữ hàng.'),
    ('04', 'Quyền "Xem phiếu hàng giữ theo công ty"', 'P0',
     'Tài khoản D thuộc công ty 1, chỉ có quyền này. Công ty 1 có 3.100 phiếu, công ty 4 có '
     '300 phiếu.',
     '1. Đăng nhập bằng D.\n2. Đọc N.\n3. Mở một phiếu của công ty 4 bằng đường dẫn trực tiếp.',
     '—',
     '- N = 3.100, không thấy phiếu công ty 4.\n'
     '- Bảng lọc CÓ ô Phòng ban, KHÔNG có ô Công ty.\n'
     '- ⚠️ Mở phiếu công ty 4 bằng đường dẫn: phần mềm báo không có quyền xem phiếu này.'),
    ('05', 'Quyền "Xem phiếu hàng giữ theo phòng ban"', 'P0',
     'Tài khoản E quản lý phòng "Phòng Chăm sóc khách hàng SG" có 60 phiếu; phòng khác có '
     '80 phiếu.',
     '1. Đăng nhập bằng E.\n2. Đọc N và bật cột Phòng ban.',
     '—',
     '- N = 60 cộng số phiếu nháp của chính E.\n'
     '- Mọi dòng đều thuộc phòng E quản lý hoặc phòng của chính E.'),
    ('06', 'Người không có quyền Quản lý giữ hàng không duyệt được', 'P0',
     'Tài khoản A không có quyền Quản lý giữ hàng; phiếu X đang ở trạng thái Chờ duyệt.',
     '1. Đăng nhập bằng A.\n2. Mở phiếu X (nếu thấy).\n'
     '3. Dùng công cụ kiểm thử gọi thẳng chức năng lập phiếu hủy cho phiếu X.',
     '—',
     '- Nút "Tạo phiếu hủy hàng giữ" và "Không duyệt" KHÔNG hiển thị.\n'
     '- ⚠️ Gọi thẳng chức năng: phần mềm từ chối, báo phiếu không còn ở trạng thái chờ duyệt '
     'hoặc không đủ quyền duyệt; hàng giữ không thay đổi.'),
    ('07', 'Bỏ qua giao diện gọi thẳng chức năng Sửa phiếu của người khác', 'P0',
     'Phiếu P ở trạng thái Đang tạo do tài khoản B lập.',
     '1. Đăng nhập bằng A.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Sửa với phiếu P.',
     '—',
     '- Phần mềm từ chối.\n- Nội dung phiếu P không thay đổi.'),
    ('08', 'Bỏ qua giao diện gọi thẳng chức năng Xóa phiếu đã duyệt', 'P0',
     'Phiếu Q đã ở trạng thái Đã duyệt và đã sinh phiếu hủy.',
     '1. Dùng công cụ kiểm thử gọi thẳng chức năng Xóa với phiếu Q.',
     '—',
     '- Phần mềm từ chối xóa.\n'
     '- ⚠️ Phiếu Q vẫn còn, phiếu hủy tương ứng và hàng giữ đã trừ không bị ảnh hưởng.'),
    ('09', 'Bỏ qua giao diện gọi thẳng chức năng Không duyệt khi thiếu quyền', 'P0',
     'Tài khoản A không có quyền Quản lý giữ hàng; phiếu R đang ở trạng thái Chờ duyệt.',
     '1. Đăng nhập bằng A.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng Không duyệt phiếu R.',
     '—',
     '- Phần mềm từ chối.\n- Phiếu R vẫn ở trạng thái Chờ duyệt, không phát sinh lý do.'),
    ('10', 'Xem lịch sử thay đổi của phiếu ngoài phạm vi quyền', 'P1',
     'Tài khoản D (xem theo công ty 1) và phiếu S thuộc công ty 4.',
     '1. Đăng nhập bằng D.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng xem lịch sử phiếu S.',
     '—',
     '- Phần mềm từ chối, báo không có quyền xem phiếu này.'),
]

# ============================================================== I
S1 = [
    ('001', 'Mở màn hình từ menu', 'P0', 'Tài khoản có ít nhất 1 phiếu trong phạm vi.',
     '1. Đăng nhập.\n2. Chọn phân hệ Tài chính.\n3. Mở nhóm Hàng hoá - Dịch vụ - Vận chuyển → '
     'Giữ hàng.\n4. Bấm mục Yêu cầu hủy hàng giữ.',
     '—',
     '- Tiêu đề trên thanh trên cùng và tiêu đề bảng đều ghi "Yêu cầu hủy hàng giữ".\n'
     '- Bảng hiện dữ liệu, không có thông báo lỗi.'),
    ('002', 'Vòng quay chờ hiện ngay khi vào màn', 'P1', 'Danh sách có trên 1.000 phiếu.',
     '1. Mở màn hình và quan sát bảng trong lúc dữ liệu đang tải.',
     '—',
     '- Trong lúc chờ, bảng hiện vòng quay chờ.\n'
     '- ⚠️ KHÔNG nhấp nháy dòng "Không có dữ liệu phù hợp." rồi mới hiện dữ liệu.'),
    ('003', 'Thanh công cụ chỉ có 3 nút', 'P0', 'Đã vào màn hình.',
     '1. Quan sát thanh công cụ phía trên bảng.',
     '—',
     '- Có đúng ba nút: Tạo mới, Xuất Excel và biểu tượng cấu hình cột.\n'
     '- ⚠️ Màn này KHÔNG có nút In trên thanh công cụ (khác màn Yêu cầu gia hạn hàng giữ).'),
    ('004', 'Đủ cột theo cấu hình mặc định', 'P0', 'Người dùng chưa từng đổi cấu hình cột.',
     '1. Quan sát tiêu đề các cột.',
     '—',
     '- Hiện sẵn: STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, '
     'Người cập nhật, Ngày cập nhật, Hành động.\n'
     '- Ẩn sẵn: Khách hàng, Phòng ban, Ghi chú, Lý do không duyệt.'),
    ('005', 'Mã phiếu là liên kết mở màn chi tiết', 'P0', 'Danh sách có ít nhất 1 phiếu.',
     '1. Bấm vào mã phiếu ở dòng đầu tiên.',
     '—',
     '- Mở màn chi tiết đúng phiếu vừa bấm.\n'
     '- Tiêu đề màn ghi "Chi tiết yêu cầu hủy hàng giữ: <mã phiếu>".'),
    ('006', 'Màu trạng thái đúng quy ước', 'P0',
     'Danh sách có phiếu ở cả ba trạng thái Đang tạo, Chờ duyệt, Đã duyệt.',
     '1. Lọc lần lượt từng trạng thái và quan sát màu nhãn.',
     'Trạng thái: lần lượt 3 giá trị',
     '- Đang tạo: nhãn XÁM.\n- Chờ duyệt: nhãn CAM.\n- Đã duyệt: nhãn XANH LÁ.\n'
     '- ⚠️ "Đang tạo" là bản nháp nên phải xám, tuyệt đối không đỏ.'),
    ('007', 'Phiếu nháp của người khác không hiện', 'P0',
     'Tài khoản B có quyền Quản lý giữ hàng. Tài khoản A đang có 1 phiếu Đang tạo.',
     '1. Đăng nhập bằng B.\n2. Lọc Trạng thái = Đang tạo.',
     'Trạng thái: Đang tạo',
     '- Danh sách KHÔNG có phiếu nháp của A.\n- Chỉ hiện phiếu nháp do chính B lập.'),
    ('008', 'Trạng thái rỗng khi không có dữ liệu', 'P1',
     'Tài khoản mới, chưa lập phiếu nào và không có quyền xem theo cấp.',
     '1. Mở màn hình.',
     '—',
     '- Bảng hiện dòng "Không có dữ liệu phù hợp.".\n- Ô thống kê ghi N = 0.'),
    ('009', 'Tiêu đề tab trình duyệt', 'P2', 'Đã vào màn hình.',
     '1. Quan sát tên tab trình duyệt.',
     '—', '- Tên tab ghi "Yêu cầu hủy hàng giữ".'),
]

# ============================================================== II
S2 = [
    ('001', 'Tìm nhanh theo mã phiếu đầy đủ', 'P0', 'Tồn tại phiếu PYCHHG-03530.',
     '1. Gõ PYCHHG-03530 vào ô tìm nhanh.\n2. Bấm nút Tìm kiếm.',
     'Ô tìm nhanh: PYCHHG-03530',
     '- Danh sách còn đúng 1 dòng.\n- N = 1.'),
    ('002', 'Tìm nhanh theo một phần mã phiếu', 'P1', 'Có nhiều phiếu mã bắt đầu PYCHHG-035.',
     '1. Gõ 035 vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: 035',
     '- Mọi dòng trả về đều có mã phiếu chứa chuỗi 035.'),
    ('003', 'Ô tìm nhanh KHÔNG tự tìm khi đang gõ', 'P1', 'Đang ở màn danh sách.',
     '1. Gõ vài ký tự vào ô tìm nhanh.\n2. Chờ 5 giây, không bấm gì.',
     'Ô tìm nhanh: PYCH',
     '- Danh sách giữ nguyên, chỉ lọc khi bấm nút Tìm kiếm hoặc nhấn Enter.'),
    ('004', 'Mở và đóng bảng lọc nâng cao', 'P1', 'Đang ở màn danh sách.',
     '1. Bấm nút Tìm kiếm nâng cao.\n2. Bấm lại nút đó.',
     '—',
     '- Lần 1 mở bảng lọc, lần 2 thu gọn lại.'),
    ('005', 'Đủ các ô lọc theo quyền cao nhất', 'P0',
     'Tài khoản có quyền Xem phiếu hàng giữ theo tổng công ty.',
     '1. Mở bảng lọc nâng cao.',
     '—',
     '- Có đủ: Công ty, Phòng ban, Mã phiếu, Trạng thái, Người tạo, Người duyệt, Tên hàng hóa, '
     'Mã hàng hóa, Ngày tạo từ, Ngày tạo đến.'),
    ('006', 'Ô Công ty và Phòng ban ẩn theo quyền', 'P0',
     'Tài khoản không có quyền xem theo cấp nào.',
     '1. Mở bảng lọc nâng cao.',
     '—', '- KHÔNG có ô Công ty và ô Phòng ban; các ô còn lại vẫn đủ.'),
    ('007', 'Lọc theo Trạng thái', 'P0', 'Có phiếu ở nhiều trạng thái.',
     '1. Chọn Trạng thái = Chờ duyệt.',
     'Trạng thái: Chờ duyệt',
     '- Danh sách tự lọc lại NGAY, không cần bấm nút.\n'
     '- Mọi dòng đều có nhãn Chờ duyệt.'),
    ('008', 'Lọc theo Người tạo', 'P1', 'Nhân viên "Nguyễn Việt Triều" có 105 phiếu.',
     '1. Chọn Người tạo = Nguyễn Việt Triều.',
     'Người tạo: Nguyễn Việt Triều',
     '- N = 105.\n- Mọi dòng đều đúng người tạo.'),
    ('009', 'Lọc theo Người duyệt', 'P1', 'Có phiếu đã duyệt bởi nhiều người khác nhau.',
     '1. Chọn Người duyệt = Võ Thị Hà.',
     'Người duyệt: Võ Thị Hà',
     '- Mọi dòng trả về đều có cột Người duyệt là Võ Thị Hà.\n'
     '- Phiếu chưa duyệt không xuất hiện.'),
    ('010', 'Lọc theo Tên hàng hóa', 'P0',
     'Có phiếu chứa hàng "Van 1 chiều bình tích".',
     '1. Nhập "Van 1 chiều" vào ô Tên hàng hóa.',
     'Tên hàng hóa: Van 1 chiều',
     '- Chỉ còn phiếu có ít nhất một dòng hàng khớp tên.\n'
     '- Mở một phiếu trong kết quả để kiểm chứng.'),
    ('011', 'Lọc theo Mã hàng hóa', 'P0', 'Có phiếu chứa hàng mã TORI-TY30001DNNC.',
     '1. Nhập TORI-TY30001DNNC vào ô Mã hàng hóa.',
     'Mã hàng hóa: TORI-TY30001DNNC',
     '- Chỉ còn phiếu có dòng hàng đúng mã đó.'),
    ('012', 'Lọc theo khoảng Ngày tạo', 'P0', 'Có phiếu lập trong tháng 07/2026.',
     '1. Chọn Ngày tạo từ = 01/07/2026 và Ngày tạo đến = 31/07/2026.',
     'Khoảng 01/07–31/07/2026',
     '- Mọi dòng có Ngày tạo trong tháng 7, lấy trọn hai đầu mút.'),
    ('013', 'Chọn Ngày tạo từ lớn hơn Ngày tạo đến', 'P1', 'Đang ở màn danh sách.',
     '1. Chọn Ngày tạo từ = 31/08/2026 và Ngày tạo đến = 01/08/2026.',
     'Ngày tạo từ: 31/08/2026; đến: 01/08/2026',
     '- Không treo, không lỗi hệ thống.\n- Danh sách rỗng kèm dòng "Không có dữ liệu phù hợp.".'),
    ('014', 'Kết hợp nhiều tiêu chí lọc', 'P0', 'Có dữ liệu phù hợp.',
     '1. Chọn Trạng thái = Đã duyệt.\n2. Chọn Người tạo.\n3. Chọn khoảng Ngày tạo.',
     'Trạng thái: Đã duyệt; Người tạo: Phạm Hữu Thái; tháng 07/2026',
     '- Kết quả thỏa mãn ĐỒNG THỜI cả ba điều kiện.'),
    ('015', 'Đổi Công ty thì Phòng ban được nạp lại', 'P0',
     'Tài khoản có quyền xem theo tổng công ty.',
     '1. Chọn Công ty = công ty 1 rồi chọn một Phòng ban.\n2. Đổi Công ty sang công ty 4.',
     '—',
     '- Giá trị Phòng ban bị xóa; danh sách phòng ban nạp lại theo công ty mới.'),
    ('016', 'Nút Làm mới xóa hết điều kiện lọc', 'P0', 'Đang áp ít nhất 3 điều kiện lọc.',
     '1. Bấm nút Làm mới.',
     '—',
     '- Mọi ô lọc trở về trống.\n'
     '- ⚠️ Danh sách được TẢI LẠI ngay, N trở về tổng phiếu trong phạm vi quyền.\n'
     '- Thứ tự sắp xếp trở về mặc định.'),
    ('017', 'Bộ lọc được ghi nhớ khi quay lại màn', 'P1',
     'Đang áp bộ lọc Trạng thái = Đã duyệt.',
     '1. Mở một phiếu rồi bấm Quay lại (trong vòng 10 phút).',
     '—', '- Bộ lọc vẫn còn và danh sách vẫn đang lọc.'),
    ('018', 'Lọc ra kết quả rỗng', 'P1', 'Đang ở màn danh sách.',
     '1. Nhập vào ô Mã phiếu một chuỗi chắc chắn không tồn tại.',
     'Mã phiếu: ZZZZ-99999',
     '- Bảng hiện "Không có dữ liệu phù hợp.".\n- N = 0, không lỗi hệ thống.'),
    ('019', 'Cài đặt bộ lọc — bỏ tích một ô lọc', 'P1', 'Đang ở màn danh sách.',
     '1. Bấm Cài đặt bộ lọc.\n2. Bỏ tích ô "Mã hàng hóa".\n3. Bấm Lưu.\n'
     '4. Mở lại bảng lọc nâng cao.',
     '—',
     '- Sau khi lưu, bảng lọc nâng cao KHÔNG còn ô Mã hàng hóa.'),
    ('020', 'Cài đặt bộ lọc — Khôi phục mặc định', 'P2',
     'Đã bỏ tích và đổi thứ tự vài ô lọc.',
     '1. Mở Cài đặt bộ lọc.\n2. Bấm Khôi phục mặc định.\n3. Bấm Lưu.',
     '—', '- Danh sách ô lọc trở về đủ theo thứ tự ban đầu.'),
    ('021', 'Cài đặt bộ lọc — Đóng không lưu', 'P2', 'Cửa sổ Cài đặt bộ lọc đang mở.',
     '1. Bỏ tích 2 ô lọc.\n2. Bấm nút Đóng.\n3. Mở lại cửa sổ.',
     '—', '- Hai ô vừa bỏ tích vẫn đang được tích.'),
    ('022', 'Cấu hình bộ lọc lưu riêng theo người dùng', 'P1',
     'Tài khoản A đã bỏ tích ô Mã hàng hóa.',
     '1. Đăng nhập bằng tài khoản B.\n2. Mở bảng lọc nâng cao.',
     '—', '- Tài khoản B vẫn thấy đủ ô lọc mặc định.'),
]

# ============================================================== III
S3 = [
    ('001', 'Phân trang mặc định 10 dòng', 'P0', 'Danh sách có 3.478 phiếu.',
     '1. Mở màn hình và quan sát.',
     '—',
     '- Bảng hiện đúng 10 dòng.\n- Ô thống kê ghi "Hiển thị 1–10 / 3478".'),
    ('002', 'Chuyển sang trang 2', 'P0', 'Danh sách nhiều hơn 1 trang.',
     '1. Bấm số 2 ở thanh phân trang.',
     '—',
     '- Ô thống kê ghi "Hiển thị 11–20 / N".\n'
     '- Cột STT chạy tiếp từ 11 đến 20, KHÔNG quay về 1.'),
    ('003', 'Đổi số dòng mỗi trang', 'P0', 'Danh sách nhiều hơn 50 phiếu.',
     '1. Đang ở trang 3, đổi Số dòng/trang sang 50.',
     'Số dòng/trang: 50',
     '- Bảng hiện 50 dòng.\n- ⚠️ Quay về TRANG 1.'),
    ('004', 'Đổi trang giữ nguyên bộ lọc', 'P0', 'Đang lọc Trạng thái = Đã duyệt, nhiều trang.',
     '1. Chuyển sang trang 2.',
     '—', '- ⚠️ Mọi dòng ở trang 2 vẫn là Đã duyệt; N không đổi.'),
    ('005', 'Đổi bộ lọc thì quay về trang 1', 'P0', 'Đang ở trang 3.',
     '1. Đổi ô lọc Trạng thái sang giá trị khác.',
     '—', '- Danh sách quay về trang 1 với kết quả mới.'),
    ('006', 'Sắp xếp theo Mã phiếu', 'P0', 'Danh sách có nhiều phiếu.',
     '1. Bấm tiêu đề cột Mã phiếu hai lần.',
     '—',
     '- Lần 1 tăng dần, lần 2 GIẢM DẦN.\n- Quay về trang 1 sau mỗi lần đổi.'),
    ('007', 'Sắp xếp theo Ngày tạo và Ngày cập nhật', 'P0', 'Danh sách có nhiều phiếu.',
     '1. Bấm tiêu đề cột Ngày tạo.\n2. Bấm tiêu đề cột Ngày cập nhật.',
     '—', '- Cả hai cột sắp xếp đúng theo ngày giờ.'),
    ('008', 'Các cột khác không sắp xếp được', 'P2', 'Đang ở màn danh sách.',
     '1. Quan sát tiêu đề các cột.',
     '—',
     '- Chỉ ba cột Mã phiếu, Ngày tạo, Ngày cập nhật có biểu tượng sắp xếp.'),
    ('009', 'Tuỳ chỉnh cột — bật cột Khách hàng', 'P0', 'Đang ở màn danh sách.',
     '1. Bấm biểu tượng cấu hình cột.\n2. Tích cột Khách hàng.\n3. Bấm Lưu.',
     '—',
     '- Cửa sổ có tiêu đề "Tuỳ chỉnh cột".\n'
     '- Bảng hiện thêm cột Khách hàng với đúng khách của từng phiếu.'),
    ('010', 'Tuỳ chỉnh cột — ba cột bị khóa', 'P0', 'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Thử bỏ tích cột STT, Mã phiếu và Hành động.',
     '—', '- Ba cột này có biểu tượng ổ khóa, không bỏ tích được.'),
    ('011', 'Tuỳ chỉnh cột — Đóng không lưu', 'P2', 'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Bỏ tích một cột.\n2. Bấm Đóng.',
     '—', '- Bảng giữ nguyên như trước.'),
    ('012', 'Cấu hình cột còn nguyên sau khi thoát và vào lại', 'P1',
     'Vừa bật cột Ghi chú và lưu.',
     '1. Chuyển sang màn khác rồi quay lại.',
     '—', '- Cột Ghi chú vẫn đang hiển thị.'),
    ('013', 'Bảng cuộn ngang khi bật nhiều cột', 'P2', 'Đã bật cả 4 cột ẩn.',
     '1. Cuộn ngang bảng.',
     '—',
     '- Có thanh cuộn ngang ở cả trên và dưới bảng.\n'
     '- Cột STT, Mã phiếu và Hành động vẫn dính khi cuộn.'),
]

# ============================================================== IV
S4 = [
    ('001', 'Mở màn lập phiếu', 'P0', 'Tài khoản đang giữ hàng cho ít nhất 1 khách hàng.',
     '1. Bấm nút Tạo mới ở màn danh sách.',
     '—',
     '- Tiêu đề màn ghi "Thêm yêu cầu hủy hàng giữ".\n'
     '- Có ô Khách hàng với dấu sao đỏ và ô Ghi chú.\n'
     '- Bảng Chi tiết trống, hiện dòng "Chưa có hàng hóa".\n'
     '- ⚠️ Nút Thêm hàng hóa đang bị KHÓA.'),
    ('002', 'Nút Thêm hàng hóa bị khóa khi chưa chọn khách', 'P0', 'Đang ở màn lập phiếu.',
     '1. Rê chuột vào nút Thêm hàng hóa khi chưa chọn Khách hàng.',
     '—',
     '- Nút không bấm được.\n'
     '- Hiện chú thích nhắc chọn khách hàng trước khi thêm hàng hóa.'),
    ('003', 'Danh sách khách hàng chỉ gồm khách đang giữ hàng của mình', 'P0',
     'Tài khoản A đang giữ hàng cho 7 khách hàng; hệ thống có hàng nghìn khách hàng khác.',
     '1. Đăng nhập bằng A.\n2. Mở màn lập phiếu và bấm vào ô Khách hàng.',
     '—',
     '- ⚠️ Danh sách chỉ có 7 khách hàng đang được A giữ hàng, KHÔNG phải toàn bộ danh mục '
     'khách hàng.\n'
     '- Ngay dưới ô có dòng chú thích giải thích phạm vi danh sách.'),
    ('004', 'Người lập không giữ hàng cho khách nào', 'P0',
     'Tài khoản B hiện không giữ hàng cho khách nào.',
     '1. Đăng nhập bằng B.\n2. Bấm Tạo mới.',
     '—',
     '- Ô Khách hàng rỗng, gợi ý ghi rõ không có khách hàng đang giữ hàng.\n'
     '- Dòng chú thích giải thích vì sao rỗng.\n'
     '- ⚠️ Không được để trống trơn không giải thích.'),
    ('005', 'Chọn khách hàng thì mở khóa nút Thêm hàng hóa', 'P0', 'Đang ở màn lập phiếu.',
     '1. Chọn một khách hàng.',
     '—', '- Nút Thêm hàng hóa mở khóa và bấm được.'),
    ('006', 'Popup chọn hàng chỉ liệt kê hàng đang giữ cho khách đó', 'P0',
     'Tài khoản A đang giữ 4 mặt hàng cho khách K và 10 mặt hàng cho khách L.',
     '1. Chọn Khách hàng = K.\n2. Bấm Thêm hàng hóa.',
     '—',
     '- Popup có tiêu đề "Hàng đang giữ cho khách hàng".\n'
     '- ⚠️ Chỉ có đúng 4 mặt hàng của khách K, không có hàng của khách L.'),
    ('007', 'Popup có ô tìm kiếm', 'P1', 'Popup chọn hàng đang mở với nhiều dòng.',
     '1. Nhập một phần tên hàng vào ô Tên hàng hóa.\n2. Bấm Tìm kiếm.',
     'Tên hàng hóa: Van',
     '- Danh sách trong popup lọc lại theo từ khóa.\n'
     '- Bấm Làm mới trả về danh sách đầy đủ.'),
    ('008', 'Chọn hàng từ popup', 'P0', 'Popup đang mở với ít nhất 2 dòng.',
     '1. Tích 2 dòng.\n2. Bấm nút Chọn.',
     '—',
     '- Nút Chọn hiển thị số dòng đang tích.\n'
     '- Popup đóng lại, hai dòng được thêm vào bảng Chi tiết với ô Cần hủy tích sẵn.'),
    ('009', 'Hàng đã có trong phiếu bị loại khỏi popup', 'P0',
     'Phiếu đã có 2 dòng hàng; khách đó có tổng 4 mặt hàng đang giữ.',
     '1. Bấm Thêm hàng hóa lần nữa.',
     '—',
     '- ⚠️ Popup chỉ còn 2 mặt hàng chưa có trong phiếu.'),
    ('010', 'Đủ cột ở bảng Chi tiết màn lập phiếu', 'P0', 'Bảng đã có dòng hàng.',
     '1. Đọc tiêu đề các cột.',
     '—',
     '- Có đủ: STT, Cần hủy, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, Có thể hủy, '
     'Yêu cầu hủy, ĐVT và cột nút xóa dòng.'),
    ('011', 'Bỏ tích ô Cần hủy', 'P1', 'Bảng có 2 dòng đang tích.',
     '1. Bỏ tích dòng 1.',
     '—',
     '- Ô Yêu cầu hủy của dòng 1 bị khóa, dòng bị làm mờ.\n'
     '- Dòng này sẽ không được gửi đi khi lưu.'),
    ('012', 'Xóa một dòng hàng', 'P1', 'Bảng có 3 dòng.',
     '1. Bấm biểu tượng thùng rác ở dòng 2.',
     '—', '- Dòng 2 biến mất khỏi bảng; hai dòng còn lại giữ nguyên.'),
    ('013', 'Lưu nháp KHÔNG bắt buộc có dòng hàng', 'P0',
     'Đã chọn Khách hàng nhưng chưa thêm hàng hóa nào.',
     '1. Bấm Lưu nháp.',
     '—',
     '- ⚠️ Lưu thành công, phiếu ở trạng thái Đang tạo với 0 dòng hàng.\n'
     '- Quay về màn danh sách; phiếu mới có mã dạng PYCHHG-NNNNN.'),
    ('014', 'Lưu và gửi duyệt BẮT BUỘC có dòng hàng', 'P0',
     'Đã chọn Khách hàng nhưng chưa thêm hàng hóa nào.',
     '1. Bấm Lưu và gửi duyệt.',
     '—',
     '- Phần mềm báo "Phải chọn ít nhất 1 hàng hoá cần hủy với số lượng lớn hơn 0".\n'
     '- Phiếu không được lưu.'),
    ('015', 'Lưu và gửi duyệt thành công', 'P0',
     'Đã chọn Khách hàng và thêm 2 dòng hàng có số lượng hợp lệ.',
     '1. Bấm Lưu và gửi duyệt.',
     'Yêu cầu hủy: 2 và 5',
     '- Hiện thông báo thành công, quay về màn danh sách.\n'
     '- Phiếu mới có trạng thái Chờ duyệt (nhãn cam).\n'
     '- Người có quyền Quản lý giữ hàng cùng công ty nhận được thông báo.'),
    ('016', 'Lưu và tiếp tục', 'P1', 'Đang ở màn lập phiếu với dữ liệu hợp lệ.',
     '1. Bấm Lưu và tiếp tục.',
     '—',
     '- Phiếu được lưu ở trạng thái Đang tạo.\n'
     '- ⚠️ KHÔNG quay về danh sách; màn hình được làm mới để lập phiếu tiếp theo.'),
    ('017', 'Nút Lưu và tiếp tục chỉ có ở màn Tạo mới', 'P2',
     'Có phiếu Đang tạo do chính mình lập.',
     '1. Mở màn Sửa của phiếu đó.',
     '—',
     '- Màn Sửa chỉ có Lưu nháp, Lưu và gửi duyệt và Quay lại.'),
    ('018', 'Cảnh báo khi rời màn lúc chưa lưu', 'P0', 'Đang ở màn lập phiếu.',
     '1. Chọn Khách hàng.\n2. Bấm nút Quay lại.',
     '—',
     '- Phần mềm hỏi xác nhận rời khỏi trang.\n'
     '- Chọn ở lại: giữ nguyên dữ liệu; chọn rời đi: bỏ mọi thay đổi.'),
    ('019', 'Mã phiếu sinh tự động không trùng', 'P0', 'Vừa lập liên tiếp 3 phiếu.',
     '1. Lập 3 phiếu liên tiếp.\n2. Xem mã ở danh sách.',
     '—',
     '- Ba mã khác nhau, dạng PYCHHG kèm 5 chữ số, không trùng phiếu cũ.'),
    ('020', 'Màn Tạo mới không có ô Mã phiếu và Trạng thái', 'P1', 'Đang ở màn lập phiếu.',
     '1. Quan sát khối Thông tin chung.',
     '—',
     '- ⚠️ Chỉ có Khách hàng và Ghi chú; các ô Mã phiếu, Trạng thái, Người duyệt, Ngày duyệt, '
     'Phòng ban yêu cầu chỉ xuất hiện ở màn Sửa và màn Chi tiết.'),
]

# ============================================================== V
S5 = [
    ('001', 'Nút Sửa chỉ hiện với phiếu nháp của mình', 'P0',
     'Tài khoản A có: phiếu 1 Đang tạo do A lập, phiếu 2 Chờ duyệt do A lập, phiếu 3 Đã duyệt.',
     '1. Xem cột Hành động của từng phiếu.',
     '—',
     '- Phiếu 1: có biểu tượng Sửa và Xóa.\n- Phiếu 2 và 3: KHÔNG có.'),
    ('002', 'Mở màn Sửa', 'P0', 'Có phiếu Đang tạo do chính mình lập.',
     '1. Bấm biểu tượng bút chì ở cột Hành động.',
     '—',
     '- Tiêu đề màn ghi "Sửa yêu cầu hủy hàng giữ".\n'
     '- Các ô Mã phiếu, Trạng thái, Phòng ban yêu cầu hiển thị và bị khóa.'),
    ('003', 'Ô Khách hàng bị khóa ở màn Sửa', 'P0', 'Đang ở màn Sửa.',
     '1. Thử bấm vào ô Khách hàng.',
     '—',
     '- ⚠️ Ô bị khóa, không đổi được khách hàng.\n'
     '- Muốn đổi khách thì phải lập phiếu mới.'),
    ('004', 'Dữ liệu đã lưu được nạp lại đúng', 'P0',
     'Phiếu Đang tạo đã có 1 dòng hàng với số lượng 6.',
     '1. Mở màn Sửa của phiếu đó.',
     '—',
     '- Ghi chú hiện đúng nội dung đã lưu.\n'
     '- Dòng hàng được tích sẵn với số lượng 6.'),
    ('005', 'Khối Lý do không duyệt hiện trên màn Sửa', 'P0',
     'Phiếu từng bị trả về kèm lý do "Chị Hoa y/c hủy phiếu".',
     '1. Mở màn Sửa của phiếu đó.',
     '—',
     '- ⚠️ Có khối "Lý do không duyệt" hiển thị nguyên văn lý do.\n'
     '- Nhờ đó người lập biết cần chỉnh gì trước khi gửi lại.'),
    ('006', 'Thêm dòng hàng vào phiếu đang sửa', 'P1', 'Phiếu có 1 dòng hàng.',
     '1. Bấm Thêm hàng hóa, chọn thêm 1 mặt hàng.\n2. Nhập số lượng.\n3. Bấm Lưu nháp.',
     'Yêu cầu hủy: 3',
     '- Phiếu có 2 dòng sau khi lưu.\n- Lịch sử thay đổi ghi nhận dòng hàng được thêm.'),
    ('007', 'Sửa rồi gửi duyệt', 'P0', 'Phiếu Đang tạo do chính mình lập.',
     '1. Chỉnh số lượng.\n2. Bấm Lưu và gửi duyệt.',
     '—',
     '- Phiếu chuyển sang trạng thái Chờ duyệt.\n'
     '- Nút Sửa và Xóa biến mất khỏi cột Hành động.'),
    ('008', 'Sửa phiếu bị trả về rồi gửi lại', 'P0',
     'Phiếu đã bị trả về, đang ở trạng thái Đang tạo và có lý do không duyệt.',
     '1. Mở màn Sửa, chỉnh theo yêu cầu.\n2. Bấm Lưu và gửi duyệt.',
     '—',
     '- Sửa được bình thường.\n- Phiếu quay lại trạng thái Chờ duyệt.'),
    ('009', 'Mở màn Sửa của phiếu đã duyệt bằng đường dẫn', 'P0',
     'Phiếu đang ở trạng thái Đã duyệt do chính mình lập.',
     '1. Gõ thẳng đường dẫn màn sửa của phiếu đó.',
     '—',
     '- Phần mềm không cho vào màn sửa.\n- Nội dung phiếu không thay đổi.'),
    ('010', 'Sửa phiếu của người khác qua đường dẫn', 'P0',
     'Phiếu Đang tạo do tài khoản B lập.',
     '1. Đăng nhập bằng A.\n2. Gõ đường dẫn màn sửa của phiếu đó.',
     '—', '- Phần mềm từ chối, không hiển thị dữ liệu phiếu.'),
    ('011', 'Cảnh báo rời màn Sửa khi chưa lưu', 'P1', 'Đang ở màn Sửa.',
     '1. Đổi Ghi chú.\n2. Bấm Quay lại.',
     '—', '- Phần mềm hỏi xác nhận rời khỏi trang.'),
]

# ============================================================== VI
S6 = [
    ('001', 'Mở màn chi tiết', 'P0', 'Có phiếu trong phạm vi quyền.',
     '1. Bấm vào mã phiếu.',
     '—',
     '- Tiêu đề ghi "Chi tiết yêu cầu hủy hàng giữ: <mã phiếu>".\n'
     '- Có đủ khối Thông tin chung, Chi tiết và Lịch sử thay đổi.'),
    ('002', 'Hai cột số lượng ở màn chi tiết', 'P0',
     'Phiếu đã duyệt: dòng hàng đề nghị hủy 5 nhưng người duyệt chỉ chấp thuận 3.',
     '1. Mở màn chi tiết, xem bảng Chi tiết.',
     '—',
     '- Tiêu đề "Số lượng" gộp trên hai cột con Yêu cầu hủy và Duyệt hủy.\n'
     '- ⚠️ Cột Yêu cầu hủy = 5, cột Duyệt hủy = 3 — hai số KHÁC nhau là đúng.'),
    ('003', 'Cột Có thể giữ có giải thích', 'P1', 'Đang ở màn chi tiết.',
     '1. Rê chuột vào biểu tượng chữ i cạnh tiêu đề cột Có thể giữ.',
     '—',
     '- Hiện lời giải thích: đây là tồn kho tại thời điểm mở phiếu, KHÁC với số đã yêu cầu hủy '
     'và số đã duyệt hủy ghi trên phiếu.'),
    ('004', 'Liên kết sang Phiếu hủy hàng giữ', 'P0',
     'Phiếu đã duyệt, có phiếu hủy tương ứng mã PHHG-03474.',
     '1. Mở màn chi tiết.\n2. Bấm vào giá trị ở ô Phiếu hủy hàng giữ.',
     '—',
     '- Ô hiển thị mã PHHG-03474 dưới dạng liên kết.\n'
     '- Bấm vào mở đúng màn chi tiết của phiếu hủy đó.'),
    ('005', 'Phiếu chưa duyệt thì ô Phiếu hủy hàng giữ trống', 'P1',
     'Phiếu đang ở trạng thái Chờ duyệt.',
     '1. Mở màn chi tiết.',
     '—', '- Ô Phiếu hủy hàng giữ để trống, không có liên kết.'),
    ('006', 'Mọi ô ở chế độ chỉ đọc', 'P0', 'Đang ở màn chi tiết.',
     '1. Thử bấm vào ô Khách hàng, Ghi chú và các ô số lượng.',
     '—', '- Không sửa được ô nào.'),
    ('007', 'Khối Lý do không duyệt ở màn chi tiết', 'P1', 'Phiếu từng bị trả về.',
     '1. Mở màn chi tiết.',
     '—', '- Có khối Lý do không duyệt hiển thị nguyên văn lý do.'),
    ('008', 'Nút cuối màn khớp với cột Hành động ngoài danh sách', 'P0',
     'Một phiếu Đang tạo do chính mình lập.',
     '1. Đếm nút ở cột Hành động ngoài danh sách.\n2. Mở phiếu, đếm nút cuối màn.',
     '—',
     '- ⚠️ Số nút khớp nhau; không có tình trạng ngoài danh sách ẩn nút mà chi tiết vẫn hiện.'),
    ('009', 'Mở phiếu nháp của người khác bằng đường dẫn', 'P0',
     'Phiếu Đang tạo do tài khoản B lập; tài khoản A có quyền Quản lý giữ hàng.',
     '1. Đăng nhập bằng A.\n2. Gõ đường dẫn màn chi tiết của phiếu đó.',
     '—',
     '- Phần mềm báo không có quyền xem phiếu này.\n- Không hiển thị nội dung phiếu.'),
    ('010', 'Mở phiếu bằng mã không tồn tại', 'P1', 'Đang đăng nhập.',
     '1. Gõ đường dẫn màn chi tiết với mã số không có thật.',
     '—', '- Phần mềm báo không tìm thấy dữ liệu, không treo trang.'),
]

# ============================================================== VII
S7 = [
    ('001', 'Nút duyệt có nhãn đúng việc nó làm', 'P0',
     'Tài khoản có quyền Quản lý giữ hàng; phiếu đang ở trạng thái Chờ duyệt.',
     '1. Mở phiếu và quan sát nút cuối màn.',
     '—',
     '- ⚠️ Nhãn nút là "Tạo phiếu hủy hàng giữ", KHÔNG phải "Duyệt".\n'
     '- Bấm vào KHÔNG hiện hộp thoại xác nhận duyệt, mà mở thẳng màn lập phiếu hủy.'),
    ('002', 'Mở màn lập phiếu hủy từ phiếu yêu cầu', 'P0',
     'Phiếu yêu cầu ở trạng thái Chờ duyệt có 3 dòng hàng.',
     '1. Bấm "Tạo phiếu hủy hàng giữ".',
     '—',
     '- Mở màn lập Phiếu hủy hàng giữ.\n'
     '- Ba dòng hàng được nạp sẵn từ phiếu yêu cầu, số lượng duyệt hủy điền sẵn bằng số '
     'yêu cầu hủy.'),
    ('003', 'Mở màn lập phiếu hủy từ cột Hành động', 'P1',
     'Phiếu ở trạng thái Chờ duyệt.',
     '1. Bấm biểu tượng dấu tích ở cột Hành động.',
     '—', '- Mở thẳng màn lập Phiếu hủy hàng giữ của đúng phiếu yêu cầu đó.'),
    ('004', 'Duyệt đủ số lượng đề nghị — hàng giữ bị trừ đúng', 'P0',
     'Phiếu yêu cầu 1 dòng: hàng H, khách K, người lập A, yêu cầu hủy 3. Trước khi duyệt A đang '
     'giữ hàng H cho khách K tổng 10 (lô hạn 10/09 có 4, lô hạn 20/09 có 6).',
     '1. Ghi lại số lượng hai lô trước khi duyệt.\n2. Bấm "Tạo phiếu hủy hàng giữ".\n'
     '3. Giữ nguyên số lượng 3 và bấm Lưu.\n4. Mở màn Danh sách hàng giữ kiểm tra lại.',
     'Duyệt hủy: 3',
     '- Phần mềm báo đã lập phiếu hủy hàng giữ kèm mã phiếu.\n'
     '- Phiếu yêu cầu chuyển sang trạng thái Đã duyệt, có Người duyệt và Ngày duyệt.\n'
     '- ⚠️ Trừ theo hạn giữ SỚM TRƯỚC: lô hạn 10/09 còn 1, lô hạn 20/09 vẫn 6.\n'
     '- Tổng hàng giữ của A cho khách K giảm từ 10 xuống 7.'),
    ('005', 'Trừ qua nhiều lô khi một lô không đủ', 'P0',
     'A giữ hàng H cho khách K: lô hạn 10/09 có 2, lô hạn 20/09 có 6. Phiếu yêu cầu hủy 5.',
     '1. Duyệt phiếu với số lượng 5.\n2. Kiểm tra các lô.',
     'Duyệt hủy: 5',
     '- ⚠️ Lô hạn 10/09 về 0, lô hạn 20/09 còn 3 (trừ tiếp 3).\n'
     '- Lịch sử biến động của hàng hóa ghi nhận trừ ở cả hai lô.'),
    ('006', 'Người duyệt cắt bớt số lượng', 'P0',
     'Phiếu yêu cầu hủy 5; A đang giữ tổng 10.',
     '1. Bấm "Tạo phiếu hủy hàng giữ".\n2. Sửa số lượng duyệt hủy xuống 2.\n3. Bấm Lưu.\n'
     '4. Mở lại phiếu yêu cầu.',
     'Duyệt hủy: 2',
     '- Hàng giữ chỉ giảm 2, còn lại 8.\n'
     '- ⚠️ Ở màn chi tiết phiếu yêu cầu: cột Yêu cầu hủy = 5, cột Duyệt hủy = 2.'),
    ('007', 'Duyệt với số lượng vượt hàng đang giữ', 'P0',
     'A chỉ còn giữ tổng 3 nhưng số duyệt hủy được đặt là 8.',
     '1. Đặt số lượng duyệt hủy 8 và bấm Lưu.\n2. Kiểm tra hàng giữ.',
     'Duyệt hủy: 8',
     '- Phần mềm báo lỗi và KHÔNG lưu phiếu hủy.\n'
     '- ⚠️ Hàng giữ giữ nguyên 3 — không bị trừ một phần rồi dừng giữa chừng.'),
    ('008', 'Duyệt khi mọi dòng đều bằng 0', 'P0', 'Phiếu yêu cầu có 2 dòng.',
     '1. Đặt số lượng duyệt hủy của cả 2 dòng về 0.\n2. Bấm Lưu.',
     'Duyệt hủy: 0 và 0',
     '- Phần mềm báo "Phải chọn ít nhất 1 hàng hoá cần hủy với số lượng lớn hơn 0".\n'
     '- Không lập phiếu hủy, phiếu yêu cầu giữ nguyên trạng thái Chờ duyệt.'),
    ('009', 'Dòng có số lượng bằng 0 bị bỏ qua', 'P1',
     'Phiếu yêu cầu có 2 dòng; người duyệt để dòng 2 bằng 0.',
     '1. Duyệt với dòng 1 = 3, dòng 2 = 0.\n2. Kiểm tra hàng giữ và lịch sử biến động.',
     'Duyệt hủy: 3 và 0',
     '- Chỉ hàng ở dòng 1 bị trừ.\n'
     '- ⚠️ Hàng ở dòng 2 không đổi và KHÔNG phát sinh dòng nhật ký nào.'),
    ('010', 'Không duyệt phiếu', 'P0', 'Phiếu ở trạng thái Chờ duyệt.',
     '1. Mở phiếu, bấm nút "Không duyệt".\n2. Nhập lý do.\n3. Xác nhận.',
     'Lý do không duyệt: Khách đã xác nhận vẫn lấy hàng',
     '- Sau khi xác nhận: phiếu quay về trạng thái Đang tạo (nhãn xám).\n'
     '- Cột Lý do không duyệt ngoài danh sách hiện đúng nội dung.\n'
     '- ⚠️ Hàng giữ KHÔNG thay đổi.\n'
     '- Người lập nhận được thông báo.'),
    ('011', 'Không duyệt bỏ trống lý do', 'P0', 'Cửa sổ Không duyệt đang mở.',
     '1. Không nhập gì.\n2. Bấm nút xác nhận.',
     'Lý do: (bỏ trống)',
     '- Phần mềm báo "Bắt buộc phải nhập lý do không duyệt" ngay dưới ô.\n'
     '- ⚠️ Cửa sổ KHÔNG đóng, phiếu không đổi trạng thái.'),
    ('012', 'Không duyệt với lý do quá dài', 'P1', 'Cửa sổ Không duyệt đang mở.',
     '1. Nhập lý do dài hơn 255 ký tự.\n2. Bấm xác nhận.',
     'Lý do: chuỗi 260 ký tự',
     '- Phần mềm báo "Không được vượt quá 255 ký tự" hoặc ô không cho nhập quá giới hạn.'),
    ('013', 'Người lập sửa và gửi lại sau khi bị trả về', 'P0',
     'Phiếu vừa bị trả về, đang ở Đang tạo.',
     '1. Người lập mở phiếu, bấm Sửa, chỉnh số lượng.\n2. Bấm Lưu và gửi duyệt.',
     '—',
     '- Phiếu quay lại trạng thái Chờ duyệt.\n'
     '- Khối Lý do không duyệt của lần trước vẫn còn để tra cứu.'),
    ('014', 'Hai người cùng duyệt một phiếu', 'P0',
     'Phiếu ở Chờ duyệt; hai người quản lý giữ hàng cùng mở phiếu.',
     '1. Người 1 lập phiếu hủy và lưu thành công.\n'
     '2. Người 2 (chưa tải lại trang) cũng bấm Lưu.',
     '—',
     '- Người 2 nhận thông báo phiếu yêu cầu không còn ở trạng thái chờ duyệt hoặc không đủ '
     'quyền duyệt.\n'
     '- ⚠️ Hàng giữ chỉ bị trừ MỘT lần; chỉ có MỘT phiếu hủy được tạo.'),
    ('015', 'Duyệt phiếu đã bị trả về trước đó', 'P1',
     'Phiếu đang ở trạng thái Đang tạo do bị trả về.',
     '1. Người quản lý giữ hàng mở phiếu.',
     '—',
     '- Nút "Tạo phiếu hủy hàng giữ" và "Không duyệt" KHÔNG hiển thị (phiếu không ở trạng thái '
     'Chờ duyệt).'),
    ('016', 'Hàng hóa không nằm trong phiếu yêu cầu', 'P1',
     'Đang ở màn lập phiếu hủy.',
     '1. Dùng công cụ kiểm thử gửi thêm một hàng hóa không có trong phiếu yêu cầu.',
     '—',
     '- Phần mềm từ chối với thông báo hàng hóa không nằm trong phiếu yêu cầu.\n'
     '- Không lập phiếu hủy, hàng giữ không đổi.'),
]

# ============================================================== VIII
S8 = [
    ('001', 'Xóa phiếu nháp của mình', 'P0', 'Phiếu Đang tạo do chính mình lập.',
     '1. Bấm biểu tượng thùng rác.\n2. Đọc hộp thoại.\n3. Bấm Xóa.',
     '—',
     '- Hộp thoại có tiêu đề "Xác nhận xóa" và ghi rõ mã phiếu.\n'
     '- Sau khi xác nhận: danh sách tải lại, không còn phiếu đó, N giảm 1.'),
    ('002', 'Hủy thao tác xóa', 'P0', 'Hộp thoại xác nhận xóa đang mở.',
     '1. Bấm nút Hủy.',
     '—', '- Hộp thoại đóng, phiếu vẫn còn nguyên.'),
    ('003', 'Nút Xóa ẩn với phiếu đã gửi duyệt', 'P0',
     'Phiếu ở Chờ duyệt do chính mình lập.',
     '1. Xem cột Hành động và nút cuối màn chi tiết.',
     '—', '- Không có nút Xóa ở cả hai nơi; nút bị ẩn hẳn.'),
    ('004', 'Nút Xóa ẩn với phiếu của người khác', 'P0',
     'Phiếu Chờ duyệt do người khác lập, mình có quyền xem.',
     '1. Xem cột Hành động.',
     '—', '- Không có nút Xóa.'),
    ('005', 'Xóa phiếu đã duyệt bằng cách gọi thẳng chức năng', 'P0',
     'Phiếu đã duyệt và đã sinh phiếu hủy.',
     '1. Dùng công cụ kiểm thử gọi thẳng chức năng xóa.',
     '—',
     '- Phần mềm từ chối.\n'
     '- ⚠️ Phiếu hủy tương ứng và hàng giữ đã trừ không bị ảnh hưởng.'),
    ('006', 'Xóa phiếu rồi mở lại bằng đường dẫn cũ', 'P1', 'Vừa xóa một phiếu.',
     '1. Gõ đường dẫn màn chi tiết của phiếu vừa xóa.',
     '—', '- Phần mềm báo không tìm thấy dữ liệu, không treo trang.'),
]

# ============================================================== IX
S9 = [
    ('001', 'In một phiếu từ cột Hành động', 'P0', 'Có phiếu trong phạm vi quyền.',
     '1. Bấm biểu tượng máy in ở cột Hành động.',
     '—',
     '- Mở tab mới, tiêu đề tab ghi "In phiếu yêu cầu hủy hàng giữ".\n'
     '- Bản xem trước hiển thị khung tờ giấy A4 dọc trên nền xám, nút In canh phải mép giấy.'),
    ('002', 'Nội dung bản in phiếu', 'P0', 'Phiếu đã duyệt có 4 dòng hàng.',
     '1. Mở bản in của phiếu đó.',
     '—',
     '- Phần đầu có logo và thông tin công ty GHI TRÊN PHIẾU.\n'
     '- Tiêu đề "PHIẾU YÊU CẦU HỦY HÀNG GIỮ", số phiếu và ngày tạo.\n'
     '- Khối thông tin: Khách hàng, Người yêu cầu, Phòng ban, Trạng thái, Ghi chú.\n'
     '- Bảng hàng hóa đủ cột STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, ĐVT, '
     'SL yêu cầu hủy và dòng Tổng cộng.\n'
     '- Có khối ký tên.'),
    ('003', 'Bản in lấy đúng công ty của phiếu', 'P0',
     'Người đăng nhập thuộc công ty 1; phiếu thuộc công ty 4 (Tân Phát ETEK Sài Gòn).',
     '1. Mở bản in của phiếu đó.',
     '—',
     '- ⚠️ Phần đầu chứng từ hiển thị thông tin công ty 4, KHÔNG phải công ty người đang in.'),
    ('004', 'Dòng Tổng cộng trên bản in', 'P1',
     'Phiếu có 4 dòng với SL yêu cầu hủy 2, 5, 1, 5.',
     '1. Mở bản in, xem dòng Tổng cộng.',
     '—', '- Dòng Tổng cộng ghi 13.'),
    ('005', 'Ô trống trên bản in vẫn giữ chỗ', 'P1',
     'Phiếu không nhập Ghi chú.',
     '1. Mở bản in.',
     '—',
     '- Dòng Ghi chú vẫn có trong bảng, chỉ để trống giá trị.\n'
     '- ⚠️ Không được mất hẳn dòng.'),
    ('006', 'Mở bản in danh sách', 'P0',
     'Đang lọc Người tạo = Nguyễn Việt Triều, còn 105 phiếu.',
     '1. Gõ đường dẫn /finance/prepick-cancel-requests/print-list trên thanh địa chỉ.',
     '—',
     '- Mở màn in danh sách, tiêu đề tab ghi "In danh sách yêu cầu hủy hàng giữ".\n'
     '- Dòng "Tổng số phiếu" ghi đúng 105.\n'
     '- ⚠️ Thanh công cụ màn danh sách hiện CHƯA có nút mở màn này — ghi nhận là điểm cần bổ '
     'sung.'),
    ('007', 'Bản in danh sách dùng khổ ngang', 'P1', 'Đang ở bản in danh sách.',
     '1. Quan sát khung tờ giấy.',
     '—',
     '- Tờ giấy nằm ngang, đủ chỗ cho các cột STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, '
     'Người duyệt, Ngày duyệt.'),
    ('008', 'Mở cửa sổ chọn trường xuất Excel', 'P0', 'Đang ở màn danh sách.',
     '1. Bấm nút Xuất Excel.',
     '—',
     '- Cửa sổ "Chọn trường xuất Excel" mở ra.\n'
     '- Mặc định đang chọn 12/12 trường.\n'
     '- Có nút Chọn tất cả và Bỏ chọn hết.'),
    ('009', 'Xuất Excel đủ trường', 'P0', 'Đang lọc còn 105 phiếu.',
     '1. Giữ nguyên 12 trường.\n2. Bấm Xuất file.\n3. Mở tệp vừa tải.',
     '—',
     '- Hiện thông báo xuất thành công và cửa sổ đóng lại.\n'
     '- Tệp có đúng 105 dòng dữ liệu.\n'
     '- Có đủ 12 cột, trong đó có cột Khách hàng và Lý do không duyệt.'),
    ('010', 'Thứ tự cột theo thứ tự chọn', 'P0', 'Cửa sổ chọn trường đang mở.',
     '1. Bấm Bỏ chọn hết.\n2. Chọn lần lượt: Khách hàng, Mã phiếu, Trạng thái.\n'
     '3. Bấm Xuất file.',
     'Trường xuất: Khách hàng, Mã phiếu, Trạng thái',
     '- Tệp có đúng 3 cột theo THỨ TỰ đã chọn.'),
    ('011', 'Xuất Excel theo bộ lọc đang áp', 'P0',
     'Đang lọc còn 105 phiếu, đang xem trang 1 (10 dòng).',
     '1. Xuất file và đếm số dòng trong tệp.',
     '—', '- ⚠️ Tệp có đủ 105 dòng, không phải 10 dòng của trang đang xem.'),
    ('012', 'Nút Xuất file bị khóa trong lúc xuất', 'P1', 'Danh sách lớn.',
     '1. Bấm Xuất file và quan sát nút.',
     '—', '- Nút bị khóa cho tới khi xong; không tạo hai tệp trùng.'),
    ('013', 'Xuất Excel khi danh sách rỗng', 'P2', 'Đang lọc ra 0 kết quả.',
     '1. Xuất file.',
     '—', '- Tệp chỉ có dòng tiêu đề, không báo lỗi hệ thống.'),
    ('014', 'Số liệu trong tệp Excel dùng định dạng số', 'P1', 'Tệp vừa xuất.',
     '1. Mở tệp, bấm vào một ô có giá trị số.',
     '—',
     '- Ô là số thật, tính tổng được.\n'
     '- ⚠️ Không xuất hiện cảnh báo số đang lưu dưới dạng chữ.'),
]

# ============================================================== X
S10 = [
    ('001', 'Bỏ trống Khách hàng', 'P0', 'Đang ở màn lập phiếu.',
     '1. Không chọn Khách hàng.\n2. Bấm Lưu nháp.',
     'Khách hàng: (bỏ trống)',
     '- Hiện lỗi đỏ "Bắt buộc phải chọn" ngay dưới ô Khách hàng.\n'
     '- Phiếu KHÔNG được lưu.'),
    ('002', 'Ghi chú vượt 255 ký tự', 'P1', 'Đang ở màn lập phiếu.',
     '1. Nhập chuỗi 300 ký tự vào ô Ghi chú.',
     'Ghi chú: chuỗi 300 ký tự',
     '- Ô không cho nhập quá 255 ký tự, hoặc báo "Không được vượt quá 255 ký tự" khi lưu.\n'
     '- ⚠️ Không tự cắt bớt rồi lưu im lặng.'),
    ('003', 'Số lượng bằng 0', 'P0', 'Đã thêm 1 dòng hàng.',
     '1. Nhập 0 vào ô Yêu cầu hủy.\n2. Bấm Lưu và gửi duyệt.',
     'Yêu cầu hủy: 0',
     '- Báo lỗi đỏ tại dòng: "Phải lớn hơn 0".\n- Phiếu không được gửi duyệt.'),
    ('004', 'Số lượng vượt số Có thể hủy', 'P0', 'Dòng có Có thể hủy = 6.',
     '1. Nhập 10 vào ô Yêu cầu hủy.\n2. Bấm Lưu và gửi duyệt.',
     'Có thể hủy: 6; Yêu cầu hủy: 10',
     '- Báo lỗi đỏ tại dòng.\n'
     '- ⚠️ Phần mềm GIỮ NGUYÊN số 10 người dùng đã gõ, không tự kéo về 6.'),
    ('005', 'Số lượng vượt 6 chữ số', 'P1', 'Đã thêm 1 dòng hàng.',
     '1. Nhập 1234567 vào ô Yêu cầu hủy.',
     'Yêu cầu hủy: 1234567',
     '- Báo "Không được vượt quá 6 chữ số" hoặc lỗi tương đương.'),
    ('006', 'Nhập chữ vào ô số lượng', 'P0', 'Đã thêm 1 dòng hàng.',
     '1. Gõ "abc" vào ô Yêu cầu hủy.',
     'Yêu cầu hủy: abc',
     '- Ô chỉ nhận ký tự số.'),
    ('007', 'Bỏ trống số lượng rồi gửi duyệt', 'P0', 'Đã thêm 1 dòng hàng, để trống số lượng.',
     '1. Bấm Lưu và gửi duyệt.',
     'Yêu cầu hủy: (bỏ trống)',
     '- Báo "Bắt buộc nhập" tại dòng.\n- Phiếu không được gửi duyệt.'),
    ('008', 'Bỏ tích hết các dòng rồi gửi duyệt', 'P0', 'Phiếu có 2 dòng hàng.',
     '1. Bỏ tích cả 2 dòng.\n2. Bấm Lưu và gửi duyệt.',
     '—',
     '- Báo "Phải chọn ít nhất 1 hàng hoá cần hủy với số lượng lớn hơn 0".'),
    ('009', 'Lỗi hiển thị đúng tại dòng bị sai', 'P0',
     'Phiếu có 5 dòng, chỉ dòng thứ 4 nhập số lượng vượt Có thể hủy.',
     '1. Bấm Lưu và gửi duyệt.',
     '—',
     '- ⚠️ Lỗi đỏ hiện ngay dưới ô của DÒNG THỨ 4, không phải chỉ một thông báo chung.\n'
     '- Màn hình tự cuộn tới dòng bị lỗi.'),
    ('010', 'Số lượng nhập số thập phân', 'P1', 'Dòng có Có thể hủy = 5.',
     '1. Nhập 2.5 vào ô Yêu cầu hủy.\n2. Bấm Lưu nháp.',
     'Yêu cầu hủy: 2.5',
     '- Phần mềm xử lý nhất quán: hoặc chấp nhận, hoặc báo lỗi rõ ràng.\n'
     '- ⚠️ Không tự làm tròn im lặng.'),
]

# ============================================================== XI
S11 = [
    ('001', 'Hàng bị hủy giữ hết trong lúc lập phiếu', 'P0',
     'A mở màn lập phiếu, đã chọn hàng H. Trong lúc đó hàng H bị hủy giữ hết bởi một phiếu khác.',
     '1. A bấm Lưu và gửi duyệt.',
     '—',
     '- Phần mềm báo hàng H không đủ số lượng đang giữ.\n'
     '- Phiếu không được gửi duyệt, dữ liệu trên màn vẫn còn.'),
    ('002', 'Khách hàng không còn hàng giữ khi mở lại phiếu nháp', 'P1',
     'Phiếu nháp đã chọn khách K; sau đó toàn bộ hàng giữ cho K đã bị hủy hết.',
     '1. Mở màn Sửa của phiếu nháp đó.',
     '—',
     '- ⚠️ Ô Khách hàng VẪN hiển thị đúng khách K, không bị trống.\n'
     '- Popup chọn hàng không còn dòng nào.'),
    ('003', 'Hàng hóa bị khóa trong danh mục', 'P1',
     'Một hàng hóa trong phiếu bị khóa ở danh mục sau khi phiếu đã lập.',
     '1. Mở màn chi tiết phiếu.',
     '—', '- Tên hàng hóa vẫn hiển thị đúng, không lỗi hệ thống.'),
    ('004', 'Hai người cùng sửa một phiếu nháp', 'P1', 'Phiếu nháp của A, mở trên hai tab.',
     '1. Tab 1 sửa Ghi chú và lưu.\n2. Tab 2 (chưa tải lại) sửa Ghi chú khác và lưu.',
     '—',
     '- Lần lưu sau ghi đè lần trước.\n- Lịch sử thay đổi ghi nhận đủ hai mốc.'),
    ('005', 'Xóa phiếu đang được người khác mở xem', 'P1',
     'A xóa phiếu P trong khi B đang mở màn chi tiết của P.',
     '1. B bấm nút In trên màn đang mở.',
     '—', '- Phần mềm báo không tìm thấy dữ liệu, không treo trang.'),
    ('006', 'Phiếu bị trả về trong lúc người lập đang sửa', 'P1',
     'Phiếu đang ở Chờ duyệt; người lập mở màn sửa bằng đường dẫn cũ; người duyệt trả phiếu về.',
     '1. Người lập bấm Lưu.',
     '—',
     '- Phần mềm xử lý nhất quán: hoặc lưu được vì phiếu đã về Đang tạo, hoặc từ chối kèm thông '
     'báo rõ ràng.'),
    ('007', 'Phiên đăng nhập hết hạn', 'P1', 'Đang mở màn danh sách.',
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
     'Vừa sửa Ghi chú của một phiếu nháp.',
     '1. Mở lịch sử.',
     '—', '- Có mốc chỉnh sửa, nêu rõ giá trị cũ và giá trị mới của ô Ghi chú.'),
    ('005', 'Ghi nhận thay đổi dòng hàng', 'P0',
     'Vừa thêm 1 dòng và bỏ 1 dòng khỏi phiếu nháp.',
     '1. Mở lịch sử.',
     '—', '- Mốc chỉnh sửa nêu rõ tên hàng được thêm và tên hàng bị bỏ.'),
    ('006', 'Ghi nhận mốc Duyệt', 'P0', 'Vừa lập phiếu hủy cho một phiếu yêu cầu.',
     '1. Mở lịch sử của phiếu yêu cầu.',
     '—', '- Có mốc duyệt, ghi người duyệt, thời điểm và trạng thái mới.'),
    ('007', 'Ghi nhận mốc Không duyệt', 'P0', 'Vừa trả về một phiếu.',
     '1. Mở lịch sử.',
     '—', '- Có mốc không duyệt, ghi người thực hiện, thời điểm và lý do.'),
    ('008', 'Thứ tự mới nhất trước', 'P0', 'Phiếu có ít nhất 3 mốc thay đổi.',
     '1. Mở lịch sử, đọc thời điểm từng mốc.',
     '—', '- ⚠️ Mốc mới nhất nằm trên cùng.'),
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
    ('001', 'Luồng đầy đủ: lập nháp → gửi duyệt → duyệt → hàng về kho', 'P0',
     'Nhân viên A đang giữ hàng H cho khách K tổng 10 (lô hạn 10/09 có 4, lô hạn 20/09 có 6). '
     'Có tài khoản B với quyền Quản lý giữ hàng.',
     '1. A lập phiếu: chọn khách K, thêm hàng H, số lượng 3, bấm Lưu nháp.\n'
     '2. A mở lại phiếu, bấm Sửa rồi bấm Lưu và gửi duyệt.\n'
     '3. B mở phiếu, bấm "Tạo phiếu hủy hàng giữ", giữ nguyên số lượng 3 và Lưu.\n'
     '4. Mở màn Danh sách hàng giữ đối chiếu.',
     'Yêu cầu hủy: 3',
     '- Sau bước 1: phiếu trạng thái Đang tạo, hàng giữ chưa đổi (vẫn 10).\n'
     '- Sau bước 2: trạng thái Chờ duyệt, hàng giữ vẫn 10.\n'
     '- Sau bước 3: phiếu trạng thái Đã duyệt, có mã phiếu hủy ở ô Phiếu hủy hàng giữ.\n'
     '- ⚠️ Lô hạn 10/09 còn 1, lô hạn 20/09 vẫn 6; tổng còn 7.\n'
     '- Lịch sử thay đổi đủ các mốc tạo mới, gửi duyệt và duyệt.'),
    ('002', 'Luồng bị trả về rồi sửa và duyệt lại', 'P0',
     'Phiếu vừa gửi duyệt đang ở Chờ duyệt, đề nghị hủy 5.',
     '1. Người duyệt bấm Không duyệt kèm lý do.\n'
     '2. Người lập sửa số lượng xuống 2 rồi gửi lại.\n'
     '3. Người duyệt lập phiếu hủy với số lượng 2 và Lưu.',
     'Lý do: Số lượng đề nghị quá nhiều',
     '- Sau bước 1: phiếu về Đang tạo, cột Lý do không duyệt có nội dung, hàng giữ không đổi.\n'
     '- Sau bước 2: phiếu về Chờ duyệt.\n'
     '- Sau bước 3: phiếu Đã duyệt, hàng giữ giảm đúng 2.'),
    ('003', 'Luồng người duyệt cắt bớt số lượng', 'P0',
     'Phiếu đề nghị hủy 5, người duyệt chỉ chấp thuận 2.',
     '1. Người duyệt lập phiếu hủy, sửa số lượng xuống 2, bấm Lưu.\n'
     '2. Mở lại màn chi tiết phiếu yêu cầu.\n3. Mở phiếu hủy bằng liên kết trên phiếu yêu cầu.',
     'Duyệt hủy: 2',
     '- Phiếu yêu cầu: cột Yêu cầu hủy = 5, cột Duyệt hủy = 2.\n'
     '- Phiếu hủy ghi số lượng 2.\n- Hàng giữ giảm đúng 2, không phải 5.'),
    ('004', 'Luồng lập nháp rồi xóa', 'P1', 'Nhân viên A đang giữ hàng cho khách K.',
     '1. A lập phiếu và Lưu nháp.\n2. A xóa phiếu vừa lập.\n3. Kiểm tra hàng giữ.',
     '—',
     '- Phiếu biến mất khỏi danh sách.\n'
     '- ⚠️ Hàng giữ hoàn toàn không thay đổi vì phiếu chưa từng được duyệt.'),
    ('005', 'Kiểm tra chéo với màn Danh sách hàng giữ', 'P0',
     'Vừa duyệt xong một phiếu hủy.',
     '1. Mở màn Tài chính → Giữ hàng → Danh sách hàng giữ.\n'
     '2. Lọc theo nhân viên và khách hàng của phiếu.',
     '—',
     '- Số lượng hiển thị khớp đúng với kết quả sau khi duyệt.\n'
     '- ⚠️ Tổng hàng giữ GIẢM đúng bằng số đã duyệt hủy (khác màn gia hạn — nơi tổng không đổi).'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP PHIẾU (TẠO MỚI)', S4),
    ('V', 'SỬA PHIẾU', S5),
    ('VI', 'XEM CHI TIẾT', S6),
    ('VII', 'DUYỆT & KHÔNG DUYỆT', S7),
    ('VIII', 'XÓA PHIẾU', S8),
    ('IX', 'IN & XUẤT EXCEL', S9),
    ('X', 'RÀNG BUỘC NHẬP LIỆU', S10),
    ('XI', 'CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI', S11),
    ('XII', 'LỊCH SỬ THAY ĐỔI', S12),
    ('XIII', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S13),
]

build(output_file=os.path.join(BASE, 'testcase.xlsx'),
      sheet_name='Trang tính1',
      feature_name='Yêu cầu hủy hàng giữ',
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
