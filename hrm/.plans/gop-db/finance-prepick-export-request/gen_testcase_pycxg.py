# -*- coding: utf-8 -*-
"""Sinh testcase cho man "Yeu cau xuat giu" (PYCXG) — phan he Tai chinh.

Viet MOI hoan toan tu code HRM nhanh `gop_db`.
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

MODULE = 'Yêu cầu xuất giữ'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn hình Yêu cầu xuất giữ (mã phiếu PYCXG) để nhân viên kinh doanh đề nghị giữ hàng trong '
     'kho cho một khách hàng tới một hạn nhất định.\n'
     '⚠️ Phiếu này KHÔNG ghi tồn hàng giữ. Hàng chỉ thực sự được giữ khi Kế toán lập Phiếu xuất '
     'giữ (PXG) và duyệt phiếu đó.\n'
     'Luồng: Đang tạo → Chờ TP duyệt → (Chờ BGĐ duyệt) → Chờ KT duyệt → Đang xuất giữ → Đã duyệt.\n'
     'Đường dẫn: Phân hệ Tài chính → Giữ hàng → Yêu cầu xuất giữ.'),
    ('2. Đối tượng được tính / hiển thị',
     'Danh sách hiển thị phiếu theo phạm vi quyền của người đăng nhập:\n'
     '- Có quyền "Xem phiếu hàng giữ theo tổng công ty": toàn bộ phiếu của mọi công ty.\n'
     '- Có quyền "Xem phiếu hàng giữ theo công ty": phiếu thuộc công ty của mình.\n'
     '- Có quyền "Xem phiếu hàng giữ theo phòng ban": phiếu thuộc phòng ban mình quản lý, phòng '
     'ban của chính mình, cộng phiếu do chính mình lập.\n'
     '- Không có quyền nào ở trên: chỉ phiếu do chính mình lập.\n'
     'Ngoài phạm vi trên, người có quyền xử lý còn thấy phiếu đang chờ chính mình: Trưởng phòng '
     'thấy phiếu Chờ TP duyệt thuộc phòng mình quản lý; Ban giám đốc thấy phiếu Chờ BGĐ duyệt; '
     'Kế toán thấy phiếu Chờ KT duyệt VÀ Đang xuất giữ.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu ở trạng thái "Đang tạo" của người khác: KHÔNG hiện trong danh sách và không mở '
     'được màn chi tiết, kể cả với người có quyền xem tổng công ty.\n'
     '- Ô lọc "Tên, mã hàng" chỉ xét dòng hàng CÓ TÍCH "Cần xuất"; dòng không tích không tính.\n'
     '- Loại "Xuất giữ HĐDV" ẩn hai cột SL hợp đồng và Đã xuất kho ở bảng chi tiết.\n'
     '- Ô Hợp đồng và ô Mã khách hàng chỉ hiện với năm loại có hợp đồng.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Hai ô "Ngày tạo từ" và "Ngày tạo đến" lọc theo NGÀY LẬP PHIẾU — không phải ngày duyệt và '
     'không phải "Giữ đến ngày".\n'
     'Khoảng ngày lấy trọn hai đầu mút. Chỉ nhập một đầu thì lọc một chiều.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Một phiếu gồm phần thông tin chung (loại yêu cầu, hợp đồng hoặc khách hàng, giữ đến ngày, '
     'ghi chú, tệp đính kèm) và nhiều dòng hàng hóa.\n'
     'Mỗi dòng hàng gồm: ô tích "Cần xuất", số lượng đề nghị, đơn vị tính, đơn giá và thành tiền.\n'
     'Phiếu có ba bộ thông tin duyệt: Trưởng phòng, Ban giám đốc và bước cuối (Kế toán, đóng dấu '
     'qua Phiếu xuất giữ).\n'
     'Quan hệ cha – con: một yêu cầu có tối đa MỘT phiếu xuất giữ.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     'Dòng hàng được ghép theo cặp "hàng hóa + đơn vị tính". Cùng một hàng hóa nhưng khác đơn vị '
     'tính là HAI dòng khác nhau.\n'
     'Khi kiểm tra số lượng còn lại của hợp đồng, hệ thống so theo đúng cặp "hàng hóa + đơn vị '
     'tính" — đúng hàng nhưng sai đơn vị vẫn bị chặn.\n'
     'Dòng không tích "Cần xuất" vẫn được lưu với số lượng 0 để giữ nguyên khuôn bảng của hợp '
     'đồng ở màn Sửa.'),
    ('7. Phân quyền cấp',
     'Quyền thao tác:\n'
     '- Trưởng phòng duyệt hàng giữ\n'
     '- Ban giám đốc duyệt hàng giữ\n'
     '- Kế toán duyệt hàng giữ\n'
     'Quyền phạm vi dữ liệu:\n'
     '- Xem phiếu hàng giữ theo tổng công ty\n'
     '- Xem phiếu hàng giữ theo công ty\n'
     '- Xem phiếu hàng giữ theo phòng ban\n'
     'Màn hình KHÔNG có quyền riêng cho Thêm / Sửa / Xóa: ai đăng nhập cũng lập được phiếu, và '
     'chỉ sửa/xóa được phiếu của mình khi phiếu ở trạng thái "Đang tạo".'),
    ('8. Cách tính các ô thống kê',
     'Ô "Hiển thị a–b / N": a là dòng đầu trang, b là dòng cuối trang, N là tổng số phiếu khớp '
     'bộ lọc TRONG PHẠM VI QUYỀN của người đang xem.\n'
     'Cột "Có thể giữ" = tồn kho khả dụng của hàng hóa, tính bằng tồn kho trừ đi phần hàng '
     'khuyến mại, quy theo đơn vị tính đang chọn của dòng.\n'
     'Phần còn lại của hợp đồng = SL hợp đồng − SL đã xuất kho, theo cặp hàng hóa + đơn vị tính.\n'
     'Cột "Thành tiền" = Đơn giá × SL đề nghị. Dòng "Tổng cộng" cộng các cột số lượng và '
     'thành tiền của những dòng đang hiển thị.'),
    ('9. Ghi chú đọc bảng',
     'Các bẫy dễ sai nhất của màn này:\n'
     '- Phiếu bị TRẢ VỀ quay đúng về trạng thái "Đang tạo"; hệ thống KHÔNG có trạng thái "Từ '
     'chối" riêng. Phân biệt bằng cột "Lý do từ chối".\n'
     '- Kế toán KHÔNG có nút duyệt ở màn này; thay vào đó là nút "Lập phiếu xuất giữ".\n'
     '- Lưu nháp KHÔNG kiểm tra tồn kho; Gửi duyệt thì CÓ.\n'
     '- Bước Ban giám đốc BẮT BUỘC nhập lại "Giữ đến ngày".\n'
     '- Sửa và lưu lại phiếu thì dấu duyệt của cả ba cấp bị xóa hết.\n'
     '- Loại "Xuất giữ khác" bắt buộc thêm ba thứ: Khách hàng, Ghi chú và ít nhất một tệp đính '
     'kèm — bắt buộc cả khi SỬA.\n'
     '- Loại yêu cầu và Hợp đồng KHÔNG đổi được sau khi phiếu đã lưu.\n'
     '- Chủ lô hàng giữ sinh ra là NGƯỜI LẬP YÊU CẦU, không phải Kế toán.\n'
     '- Nhóm test bảo mật gọi thẳng chức năng bằng công cụ kiểm thử dành cho tester kỹ thuật.'),
]

ROLE_TCS = [
    ('00', 'Tài khoản không có quyền nào của nhóm hàng giữ vẫn vào được màn hình', 'P0',
     'Tài khoản A không có quyền duyệt và không có quyền xem theo cấp; A đã lập 26 phiếu; toàn '
     'hệ thống có 2.174 phiếu.',
     '1. Đăng nhập bằng tài khoản A.\n'
     '2. Vào Tài chính → Giữ hàng → Yêu cầu xuất giữ.',
     '—',
     '- Màn hình mở được, không báo lỗi quyền.\n'
     '- Danh sách chỉ có 26 phiếu do A lập.\n'
     '- Ô "Hiển thị a–b / N" ghi N = 26.\n'
     '- Nút Tạo mới vẫn hiển thị.\n'
     '- Bảng lọc nâng cao KHÔNG có ô Công ty và ô Phòng ban.'),
    ('01', 'Quyền "Xem phiếu hàng giữ theo tổng công ty" thấy phiếu của mọi công ty', 'P0',
     'Tài khoản B chỉ có quyền Xem phiếu hàng giữ theo tổng công ty. Hệ thống có phiếu của ít '
     'nhất 2 công ty khác nhau.',
     '1. Đăng nhập bằng B.\n2. Mở màn danh sách và đọc N.\n3. Lọc lần lượt từng công ty.',
     '—',
     '- N bằng tổng số phiếu khác trạng thái "Đang tạo" của toàn hệ thống, cộng phiếu "Đang tạo" '
     'của chính B.\n'
     '- Bảng lọc CÓ ô Công ty và ô Phòng ban.'),
    ('02', 'Quyền "Xem phiếu hàng giữ theo công ty" chỉ thấy phiếu công ty mình', 'P0',
     'Tài khoản C thuộc công ty 1, chỉ có quyền Xem phiếu hàng giữ theo công ty.',
     '1. Đăng nhập bằng C.\n2. Đọc N.\n'
     '3. Mở một phiếu của công ty khác bằng đường dẫn trực tiếp.',
     '—',
     '- N chỉ đếm phiếu của công ty 1.\n'
     '- Bước 3: hệ thống báo không có quyền xem phiếu này.\n'
     '- Bảng lọc CÓ ô Phòng ban, KHÔNG có ô Công ty.'),
    ('03', 'Quyền "Xem phiếu hàng giữ theo phòng ban" thấy phòng mình quản lý và phiếu của mình',
     'P0',
     'Tài khoản D quản lý phòng P1 và P2, bản thân thuộc phòng P3. D đã lập 4 phiếu từ phòng P3.',
     '1. Đăng nhập bằng D.\n2. Đọc N và soát cột Phòng ban (bật ở Cấu hình cột).',
     '—',
     '- Danh sách có phiếu của P1, P2, P3.\n'
     '- ⚠️ 4 phiếu do chính D lập vẫn hiện đủ, kể cả nếu phòng ban ghi trên phiếu không thuộc '
     'nhóm D quản lý.'),
    ('04', 'Trưởng phòng không có quyền xem theo cấp vẫn thấy phiếu chờ mình duyệt', 'P0',
     'Tài khoản E chỉ có quyền "Trưởng phòng duyệt hàng giữ", quản lý phòng P1. Phòng P1 có '
     '3 phiếu ở trạng thái Chờ TP duyệt do người khác lập.',
     '1. Đăng nhập bằng E.\n2. Mở màn danh sách.',
     '—',
     '- ⚠️ 3 phiếu Chờ TP duyệt của phòng P1 XUẤT HIỆN trong danh sách dù E không có quyền xem '
     'theo cấp nào.\n'
     '- Mỗi dòng có biểu tượng Duyệt ở cột Hành động.'),
    ('05', 'Ban giám đốc không có quyền xem theo cấp vẫn thấy phiếu Chờ BGĐ duyệt', 'P0',
     'Tài khoản F chỉ có quyền "Ban giám đốc duyệt hàng giữ", thuộc công ty 1.',
     '1. Đăng nhập bằng F.\n2. Mở màn danh sách.',
     '—',
     '- Mọi phiếu Chờ BGĐ duyệt của công ty 1 đều hiện, không giới hạn phòng ban.\n'
     '- Phiếu ở trạng thái khác của người khác thì không hiện.'),
    ('06', 'Kế toán thấy CẢ phiếu Chờ KT duyệt lẫn phiếu Đang xuất giữ', 'P0',
     'Tài khoản G chỉ có quyền "Kế toán duyệt hàng giữ", thuộc công ty 1. Công ty 1 có 5 phiếu '
     'Chờ KT duyệt và 2 phiếu Đang xuất giữ.',
     '1. Đăng nhập bằng G.\n2. Mở màn danh sách.\n3. Lọc Trạng thái = Đang xuất giữ.',
     '—',
     '- ⚠️ Cả 7 phiếu đều hiện — kế toán còn việc ở cả hai trạng thái này.\n'
     '- Bước 3: ra đúng 2 phiếu.'),
    ('07', 'Phiếu "Đang tạo" của người khác bị giấu với MỌI cấp quyền', 'P0',
     'Người H lập một phiếu và lưu nháp (Đang tạo). Tài khoản B có quyền xem tổng công ty.',
     '1. Đăng nhập bằng B.\n2. Tìm mã phiếu của H ở ô tìm nhanh.\n'
     '3. Mở phiếu đó bằng đường dẫn trực tiếp.',
     'Mã phiếu nháp của H',
     '- Bước 2: không tìm thấy dòng nào.\n'
     '- Bước 3: hệ thống báo không có quyền xem phiếu này.\n'
     '- ⚠️ Quyền xem rộng nhất cũng KHÔNG mở được phiếu nháp của người khác.'),
    ('08', 'Danh sách và màn chi tiết dùng cùng một bộ điều kiện', 'P0',
     'Tài khoản bất kỳ đã đăng nhập.',
     '1. Ghi lại danh sách mã phiếu đang thấy ở màn danh sách.\n'
     '2. Mở lần lượt từng mã đó bằng đường dẫn trực tiếp.\n'
     '3. Lấy một mã KHÔNG có trong danh sách rồi mở bằng đường dẫn trực tiếp.',
     '—',
     '- Bước 2: mở được hết, không phiếu nào báo lỗi quyền.\n'
     '- Bước 3: hệ thống báo không có quyền xem phiếu này.'),
    ('09', 'Người có vai trò quản trị hệ thống bỏ qua ràng buộc phòng ban khi duyệt', 'P1',
     'Tài khoản quản trị hệ thống, không quản lý phòng ban nào. Có phiếu Chờ TP duyệt ở phòng P9.',
     '1. Đăng nhập bằng tài khoản quản trị.\n2. Mở phiếu Chờ TP duyệt của phòng P9.',
     '—',
     '- Nút TP duyệt và Từ chối vẫn hiển thị.\n'
     '- Duyệt được bình thường.'),
]

S1 = [
    ('001', 'Vào màn hình lần đầu hiển thị đúng bố cục', 'P0',
     'Đã đăng nhập, có ít nhất 1 phiếu trong phạm vi quyền.',
     '1. Vào Tài chính → Giữ hàng → Yêu cầu xuất giữ.',
     '—',
     '- Tiêu đề trang là "Yêu cầu xuất giữ".\n'
     '- Khối Bộ lọc danh sách ở trên, khối bảng ở dưới.\n'
     '- Thanh công cụ có 4 nút: Tạo mới, In, Xuất Excel, Cấu hình cột hiển thị.\n'
     '- Bảng hiển thị 10 dòng mỗi trang.'),
    ('002', 'Vòng quay chờ hiện trong lúc nạp dữ liệu', 'P2',
     'Đã đăng nhập.',
     '1. Vào màn hình và quan sát vùng bảng ngay khi trang vừa mở.',
     '—',
     '- Có vòng quay chờ kèm dòng "Đang tải dữ liệu..." trước khi bảng hiện dữ liệu.\n'
     '- Vòng quay biến mất khi dữ liệu về.'),
    ('003', 'Danh sách rỗng hiển thị đúng câu thông báo', 'P1',
     'Tài khoản chưa lập phiếu nào và không có quyền xem theo cấp.',
     '1. Vào màn hình.',
     '—',
     '- Bảng hiện dòng "Không có dữ liệu phù hợp.".\n'
     '- Ô "Hiển thị a–b / N" ghi N = 0.\n'
     '- Không có thông báo lỗi nào.'),
    ('004', 'Các cột mặc định hiển thị đúng thứ tự', 'P1',
     'Người dùng chưa từng đổi cấu hình cột.',
     '1. Vào màn hình và đọc dòng tiêu đề bảng.',
     '—',
     '- Thứ tự: STT, Mã phiếu, Loại yêu cầu, Người tạo, Ngày tạo, Hợp đồng, Trạng thái, '
     'Người duyệt, Ngày duyệt, Hành động.\n'
     '- Bảy cột Khách hàng, Giữ đến ngày, Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, '
     'Lý do từ chối KHÔNG hiển thị.'),
    ('005', 'Cột STT, Mã phiếu và Hành động dính khi cuộn ngang', 'P2',
     'Đã bật thêm vài cột ẩn để bảng rộng hơn khung màn hình.',
     '1. Cuộn ngang bảng sang phải.',
     '—',
     '- Cột STT và Mã phiếu luôn dính bên trái.\n'
     '- Cột Hành động luôn dính bên phải.'),
    ('006', 'Mã phiếu là liên kết mở màn chi tiết', 'P0',
     'Có ít nhất 1 phiếu trong danh sách.',
     '1. Bấm vào mã phiếu ở cột thứ hai.',
     '—',
     '- Chuyển sang màn chi tiết đúng phiếu đó.\n'
     '- Tiêu đề màn ghi "Chi tiết yêu cầu xuất giữ: <mã phiếu>".'),
    ('007', 'Màu nhãn trạng thái đúng quy ước', 'P1',
     'Danh sách có đủ các trạng thái.',
     '1. Soát cột Trạng thái.',
     '—',
     '- "Đang tạo" màu XÁM.\n'
     '- "Chờ TP duyệt", "Chờ BGĐ duyệt", "Chờ KT duyệt", "Đang xuất giữ" màu CAM.\n'
     '- "Đã duyệt" màu XANH LÁ.\n'
     '- ⚠️ Không trạng thái nào tô ĐỎ.'),
    ('008', 'Cột Người duyệt để trống khi phiếu chưa duyệt xong', 'P1',
     'Có phiếu ở trạng thái Chờ BGĐ duyệt (đã qua Trưởng phòng).',
     '1. Soát cột Người duyệt và Ngày duyệt của phiếu đó.',
     '—',
     '- ⚠️ Hai ô để TRỐNG, không hiện tên Trưởng phòng đã duyệt bước trước.\n'
     '- Cột này chỉ điền khi phiếu đã Đã duyệt.\n'
     '- Ô trống là trống hẳn, không in dấu "—" hay "-".'),
    ('009', 'Cột Hợp đồng để trống với loại Xuất giữ khác', 'P1',
     'Có phiếu loại "Xuất giữ khác" trong danh sách.',
     '1. Lọc Loại yêu cầu = Xuất giữ khác.\n2. Soát cột Hợp đồng.',
     '—',
     '- Ô Hợp đồng để trống ở mọi dòng.\n'
     '- Ô trống là trống hẳn, không in dấu gạch ngang.'),
    ('010', 'Nút hành động ẩn hẳn khi không dùng được', 'P0',
     'Danh sách có phiếu ở nhiều trạng thái.',
     '1. Soát cột Hành động của từng dòng.',
     '—',
     '- ⚠️ Không có nút nào ở trạng thái mờ / không bấm được.\n'
     '- Nút Sửa, Xóa chỉ hiện ở phiếu Đang tạo do chính mình lập.\n'
     '- Nút In và Lịch sử hiện ở mọi dòng.'),
    ('011', 'Vào màn hình bằng đường dẫn trực tiếp', 'P2',
     'Đã đăng nhập.',
     '1. Gõ /finance/product-prepick-requests lên thanh địa chỉ.',
     '—',
     '- Màn hình mở đúng, không phải qua menu.'),
    ('012', 'Phiên đăng nhập hết hạn', 'P1',
     'Đang ở màn danh sách, phiên đăng nhập đã hết hiệu lực.',
     '1. Bấm nút Tìm kiếm.',
     '—',
     '- Hệ thống điều hướng về màn đăng nhập.\n'
     '- Không hiện dữ liệu cũ kèm lỗi.'),
    ('013', 'Đổi số dòng mỗi trang giữ nguyên bộ lọc', 'P1',
     'Đang lọc Trạng thái = Đã duyệt, có hơn 20 kết quả.',
     '1. Đổi Số dòng/trang từ 10 sang 20.',
     '—',
     '- Bảng hiện 20 dòng, vẫn chỉ toàn phiếu Đã duyệt.\n'
     '- Quay về trang 1.'),
]

S2 = [
    ('001', 'Tìm nhanh theo mã phiếu đầy đủ', 'P0',
     'Có phiếu PYCXG-02219 trong phạm vi quyền.',
     '1. Gõ PYCXG-02219 vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'PYCXG-02219',
     '- Danh sách còn đúng 1 dòng.\n- N = 1.'),
    ('002', 'Tìm nhanh theo một phần mã phiếu', 'P1',
     'Có nhiều phiếu mã bắt đầu bằng PYCXG-022.',
     '1. Gõ 022 vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     '022',
     '- Mọi dòng trả về đều có chuỗi "022" trong mã phiếu.\n'
     '- ⚠️ Dòng trùng khít lên đầu, rồi tới dòng bắt đầu bằng, rồi tới dòng chỉ chứa.'),
    ('003', 'Ô tìm nhanh KHÔNG tự lọc khi đang gõ', 'P1',
     'Đang ở màn danh sách.',
     '1. Gõ vài ký tự vào ô tìm nhanh rồi dừng 5 giây, KHÔNG bấm Tìm kiếm.',
     'PYCXG',
     '- Bảng KHÔNG đổi.\n- Chỉ bấm Tìm kiếm hoặc nhấn Enter mới lọc.'),
    ('004', 'Nhấn Enter trong ô tìm nhanh tương đương bấm Tìm kiếm', 'P2',
     'Đang ở màn danh sách.',
     '1. Gõ mã phiếu rồi nhấn Enter.',
     'PYCXG-02219',
     '- Bảng lọc lại đúng như khi bấm nút Tìm kiếm.'),
    ('005', 'Tìm nhanh không khớp gì', 'P1',
     'Đang ở màn danh sách.',
     '1. Gõ chuỗi vô nghĩa rồi bấm Tìm kiếm.',
     'zzzz9999',
     '- Bảng hiện "Không có dữ liệu phù hợp.".\n- N = 0.\n- Không có lỗi đỏ.'),
    ('006', 'Mở bảng lọc nâng cao', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm nút Tìm kiếm nâng cao.',
     '—',
     '- Bảng lọc mở ra, nhãn nút đổi thành "Ẩn tìm kiếm nâng cao".\n'
     '- Có đủ các ô lọc theo cấu hình đang bật.'),
    ('007', 'Lọc theo Mã phiếu ở bảng nâng cao', 'P1',
     'Bảng lọc nâng cao đang mở.',
     '1. Gõ 02219 vào ô Mã phiếu.',
     '02219',
     '- ⚠️ Bảng tự lọc lại NGAY, không cần bấm nút Tìm kiếm.\n'
     '- Mọi dòng có chuỗi 02219 trong mã phiếu.'),
    ('008', 'Lọc theo Loại yêu cầu', 'P0',
     'Hệ thống có phiếu của nhiều loại.',
     '1. Chọn Loại yêu cầu = "Xuất giữ HĐ hãng".',
     '—',
     '- Cột Loại yêu cầu toàn bộ là "Xuất giữ HĐ hãng".\n'
     '- N giảm đúng theo số phiếu loại đó.'),
    ('009', 'Ô lọc Loại yêu cầu có đủ 6 giá trị', 'P1',
     'Bảng lọc nâng cao đang mở.',
     '1. Mở danh sách của ô Loại yêu cầu.',
     '—',
     '- Đủ 6 lựa chọn: Xuất giữ thường, Xuất giữ khuyến mại, Xuất giữ HĐDV, Xuất giữ HĐDA, '
     'Xuất giữ HĐ hãng, Xuất giữ khác.'),
    ('010', 'Ô lọc Trạng thái có đủ 6 giá trị theo đúng thứ tự vòng đời', 'P1',
     'Bảng lọc nâng cao đang mở.',
     '1. Mở danh sách của ô Trạng thái.',
     '—',
     '- Thứ tự: Đang tạo, Chờ TP duyệt, Chờ BGĐ duyệt, Chờ KT duyệt, Đang xuất giữ, Đã duyệt.\n'
     '- ⚠️ Xếp theo vòng đời, không xếp theo bảng chữ cái.'),
    ('011', 'Lọc theo Trạng thái = Đang tạo chỉ ra phiếu của mình', 'P0',
     'Hệ thống có nhiều phiếu nháp của nhiều người.',
     '1. Chọn Trạng thái = Đang tạo.',
     '—',
     '- ⚠️ Chỉ ra phiếu nháp do chính mình lập, kể cả khi có quyền xem tổng công ty.'),
    ('012', 'Lọc theo Người tạo', 'P1',
     'Có phiếu của nhiều người lập.',
     '1. Chọn Người tạo = một nhân viên cụ thể.',
     '—',
     '- Cột Người tạo toàn bộ là nhân viên đã chọn.'),
    ('013', 'Lọc theo Người duyệt chỉ ra phiếu Đã duyệt', 'P1',
     'Có phiếu đã duyệt xong.',
     '1. Chọn Người duyệt = một Kế toán cụ thể.',
     '—',
     '- ⚠️ Chỉ ra phiếu ĐÃ duyệt xong; phiếu đang chờ duyệt không có người duyệt nên không lọt.'),
    ('014', 'Lọc theo Khách hàng', 'P1',
     'Có phiếu của nhiều khách hàng.',
     '1. Chọn Khách hàng = một khách cụ thể.',
     '—',
     '- Bật cột Khách hàng ở Cấu hình cột để đối chiếu: mọi dòng đúng khách đã chọn.'),
    ('015', 'Lọc theo Tên, mã hàng chỉ xét dòng có tích Cần xuất', 'P0',
     'Phiếu X có hàng HH01 tích Cần xuất, phiếu Y có HH01 trong bảng nhưng KHÔNG tích.',
     '1. Gõ HH01 vào ô Tên, mã hàng.',
     'HH01',
     '- ⚠️ Chỉ phiếu X ra; phiếu Y KHÔNG ra.\n'
     '- Đây là hành vi đúng: dòng không tích là hàng người lập không xin giữ.'),
    ('016', 'Lọc theo Tên, mã hàng tìm được cả theo tên lẫn mã', 'P1',
     'Có phiếu chứa hàng tên "Dầu thủy lực Eneos", mã ENEO-700-V5024.',
     '1. Gõ "Dầu thủy lực" rồi ghi lại kết quả.\n2. Xóa, gõ "ENEO-700".',
     'Dầu thủy lực / ENEO-700',
     '- Cả hai lần đều tìm ra phiếu đó.\n- Một ô lọc chung cho cả tên và mã.'),
    ('017', 'Lọc theo Số hợp đồng', 'P0',
     'Có phiếu gắn hợp đồng HD_TPE_HN_KD2_26_0999.',
     '1. Gõ KD2_26_0999 vào ô Số hợp đồng.',
     'KD2_26_0999',
     '- Chỉ ra phiếu gắn hợp đồng khớp.\n'
     '- Phiếu loại Xuất giữ khác (không hợp đồng) KHÔNG ra.'),
    ('018', 'Lọc theo Số hợp đồng áp cho cả năm loại hợp đồng', 'P1',
     'Hệ thống có phiếu HĐ bán, HĐDV, HĐDA, HĐ hãng.',
     '1. Lần lượt gõ số hợp đồng của từng loại vào ô Số hợp đồng.',
     '—',
     '- Mỗi lần đều tìm ra đúng phiếu của loại tương ứng.\n'
     '- ⚠️ Không loại nào bị bỏ sót vì nằm ở bảng hợp đồng khác.'),
    ('019', 'Lọc khoảng Ngày tạo lấy trọn hai đầu mút', 'P0',
     'Có phiếu lập đúng ngày 01/08/2026 và 31/08/2026.',
     '1. Ngày tạo từ = 01/08/2026, Ngày tạo đến = 31/08/2026.',
     '01/08/2026 – 31/08/2026',
     '- ⚠️ Cả phiếu ngày 01/08 lẫn ngày 31/08 đều nằm trong kết quả.'),
    ('020', 'Chỉ nhập Ngày tạo từ', 'P1',
     'Đang ở màn danh sách.',
     '1. Nhập Ngày tạo từ = 01/09/2026, bỏ trống ô còn lại.',
     '01/09/2026',
     '- Ra mọi phiếu lập từ 01/09/2026 trở đi.'),
    ('021', 'Lọc Ngày tạo KHÔNG lẫn với Giữ đến ngày', 'P0',
     'Phiếu Z lập ngày 10/07/2026, Giữ đến ngày 25/09/2026.',
     '1. Lọc Ngày tạo từ 01/09/2026 đến 30/09/2026.',
     '—',
     '- ⚠️ Phiếu Z KHÔNG có trong kết quả, dù hạn giữ rơi vào tháng 9.'),
    ('022', 'Kết hợp nhiều tiêu chí lọc', 'P0',
     'Đang ở màn danh sách.',
     '1. Chọn Loại yêu cầu = Xuất giữ HĐ hãng.\n2. Chọn Trạng thái = Đã duyệt.\n'
     '3. Nhập khoảng Ngày tạo.',
     '—',
     '- Mọi dòng thỏa ĐỒNG THỜI cả ba tiêu chí.\n'
     '- N cập nhật đúng sau mỗi lần đổi ô lọc.'),
    ('023', 'Nút Làm mới xóa toàn bộ tiêu chí', 'P0',
     'Đang áp 3 tiêu chí lọc và đang sắp xếp theo Ngày tạo tăng dần.',
     '1. Bấm Làm mới.',
     '—',
     '- Mọi ô lọc về trống, ô tìm nhanh về trống.\n'
     '- Bỏ luôn thứ tự sắp xếp, quay về mặc định.\n'
     '- Bảng về trang 1 với toàn bộ phiếu trong phạm vi quyền.'),
    ('024', 'Bộ lọc được ghi nhớ khi rời màn rồi quay lại', 'P1',
     'Đang lọc Trạng thái = Chờ KT duyệt.',
     '1. Mở một phiếu rồi bấm Quay lại.',
     '—',
     '- Bộ lọc Trạng thái = Chờ KT duyệt vẫn còn.\n- Bảng vẫn hiện đúng kết quả đã lọc.'),
    ('025', 'Bộ lọc hết hiệu lực sau 10 phút', 'P2',
     'Đã lọc rồi rời sang màn khác quá 10 phút.',
     '1. Quay lại màn Yêu cầu xuất giữ.',
     '—',
     '- Bộ lọc đã bị xóa, danh sách về mặc định.'),
    ('026', 'Ô lọc Công ty chỉ hiện với quyền xem tổng công ty', 'P1',
     'Ba tài khoản: B (tổng công ty), C (công ty), D (phòng ban).',
     '1. Lần lượt đăng nhập và mở bảng lọc nâng cao.',
     '—',
     '- B: có cả ô Công ty và Phòng ban.\n- C: chỉ có ô Phòng ban.\n'
     '- D: không có cả hai ô.'),
    ('027', 'Ô lọc Khách hàng rỗng khi dữ liệu khách hàng chưa có', 'P2',
     'Môi trường thử nghiệm chưa đồng bộ đủ dữ liệu khách hàng.',
     '1. Mở danh sách của ô Khách hàng.',
     '—',
     '- Danh sách rỗng, có dòng thông báo không có dữ liệu.\n'
     '- ⚠️ Không báo lỗi đỏ; đây là hiển thị đúng khi thiếu dữ liệu nguồn.'),
]

S3 = [
    ('001', 'Bốn cột sắp xếp được đúng như quy định', 'P0',
     'Đang ở màn danh sách.',
     '1. Soát biểu tượng mũi tên trên dòng tiêu đề bảng.',
     '—',
     '- Chỉ bốn cột có mũi tên: Mã phiếu, Ngày tạo, Ngày duyệt, Giữ đến ngày.\n'
     '- Các cột khác KHÔNG có mũi tên và bấm không đổi thứ tự.'),
    ('002', 'Sắp xếp theo Ngày tạo tăng dần rồi giảm dần', 'P0',
     'Có hơn 10 phiếu.',
     '1. Bấm tiêu đề Ngày tạo lần 1.\n2. Bấm lần 2.',
     '—',
     '- Lần 1: cũ nhất lên đầu.\n- Lần 2: mới nhất lên đầu.\n'
     '- Mỗi lần đều quay về trang 1.'),
    ('003', 'Sắp xếp giữ nguyên bộ lọc đang áp', 'P0',
     'Đang lọc Trạng thái = Đã duyệt.',
     '1. Bấm tiêu đề Mã phiếu.',
     '—',
     '- Thứ tự đổi nhưng danh sách vẫn chỉ toàn phiếu Đã duyệt.'),
    ('004', 'Sắp xếp theo Giữ đến ngày', 'P1',
     'Đã bật cột Giữ đến ngày ở Cấu hình cột.',
     '1. Bấm tiêu đề Giữ đến ngày.',
     '—',
     '- Danh sách xếp theo hạn giữ, không phải theo ngày lập.'),
    ('005', 'STT chạy liên tục qua các trang', 'P0',
     'Có hơn 20 phiếu, đang để 10 dòng/trang.',
     '1. Xem STT ở trang 1.\n2. Sang trang 2 và xem STT.',
     '—',
     '- Trang 1: 1–10.\n- Trang 2: 11–20.\n- ⚠️ KHÔNG reset về 1 ở mỗi trang.'),
    ('006', 'Lật trang không lặp và không mất bản ghi', 'P0',
     'Có nhiều phiếu lập cùng một thời điểm.',
     '1. Ghi lại mã phiếu ở trang 1.\n2. Sang trang 2, 3 và ghi lại mã.',
     '—',
     '- ⚠️ Không mã nào xuất hiện ở hai trang.\n- Không mã nào bị nhảy mất.'),
    ('007', 'Ô "Hiển thị a–b / N" đúng ở trang cuối', 'P1',
     'Có 26 phiếu, để 10 dòng/trang.',
     '1. Chuyển tới trang 3.',
     '—',
     '- Ô ghi "Hiển thị 21–26 / 26".\n- Bảng có 6 dòng.'),
    ('008', 'Nút trang đầu / trang cuối hoạt động đúng', 'P2',
     'Có nhiều hơn 4 trang.',
     '1. Bấm nút về trang cuối.\n2. Bấm nút về trang đầu.',
     '—',
     '- Nhảy đúng trang, dữ liệu và STT khớp.'),
    ('009', 'Cấu hình cột: bật cột ẩn lên', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm Cấu hình cột hiển thị.\n2. Tích cột Khách hàng và Giữ đến ngày.\n3. Bấm Lưu.',
     '—',
     '- Bảng có thêm hai cột đúng vị trí đã chọn.\n- Dữ liệu hai cột hiển thị đúng.'),
    ('010', 'Cấu hình cột: ba cột bị khóa không bỏ tích được', 'P0',
     'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Thử bỏ tích STT, Mã phiếu, Hành động.',
     '—',
     '- Ba cột này có biểu tượng ổ khóa.\n- Không bỏ tích được, không kéo đổi thứ tự được.'),
    ('011', 'Cấu hình cột: kéo đổi thứ tự cột', 'P1',
     'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Kéo cột Trạng thái lên ngay sau Mã phiếu.\n2. Bấm Lưu.',
     '—',
     '- Bảng vẽ lại đúng thứ tự mới.'),
    ('012', 'Cấu hình cột: bấm Đóng thì bỏ thay đổi chưa lưu', 'P1',
     'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Bỏ tích cột Hợp đồng.\n2. Bấm Đóng (không bấm Lưu).\n3. Mở lại cửa sổ.',
     '—',
     '- Cột Hợp đồng vẫn hiển thị trong bảng.\n- Cửa sổ mở lại thấy cột Hợp đồng vẫn được tích.'),
    ('013', 'Cấu hình cột lưu riêng theo từng người dùng', 'P1',
     'Người A đã tắt 3 cột và lưu.',
     '1. Đăng xuất, đăng nhập bằng người B.\n2. Vào màn hình.',
     '—',
     '- Người B thấy cấu hình cột mặc định, không bị ảnh hưởng bởi A.'),
    ('014', 'Cấu hình cột còn nguyên sau khi đăng nhập lại', 'P1',
     'Người A đã lưu cấu hình cột.',
     '1. Đăng xuất rồi đăng nhập lại bằng A.\n2. Vào màn hình.',
     '—',
     '- Cấu hình cột của A vẫn như lúc lưu.'),
    ('015', 'Cài đặt bộ lọc: tắt bớt ô lọc', 'P1',
     'Đang ở màn danh sách.',
     '1. Bấm Cài đặt bộ lọc.\n2. Bỏ tích ô Khách hàng và ô Số hợp đồng.\n3. Bấm Lưu.',
     '—',
     '- Bảng lọc nâng cao không còn hai ô đó.\n- Các ô còn lại giữ nguyên thứ tự.'),
    ('016', 'Cài đặt bộ lọc: Khôi phục mặc định', 'P1',
     'Đã tắt vài ô lọc và lưu.',
     '1. Bấm Cài đặt bộ lọc.\n2. Bấm Khôi phục mặc định.\n3. Bấm Lưu.',
     '—',
     '- Bảng lọc quay về đủ 11 ô theo thứ tự ban đầu.'),
    ('017', 'Cài đặt bộ lọc: đủ 11 ô lọc', 'P2',
     'Cửa sổ Cài đặt bộ lọc đang mở.',
     '1. Đếm số mục trong cửa sổ.',
     '—',
     '- Đủ 11 mục: Công ty – Phòng ban, Mã phiếu, Loại yêu cầu, Trạng thái, Người tạo, '
     'Người duyệt, Khách hàng, Tên mã hàng, Số hợp đồng, Ngày tạo từ, Ngày tạo đến.'),
]

S4 = [
    ('001', 'Mở màn Tạo mới từ nút trên thanh công cụ', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm nút Tạo mới.',
     '—',
     '- Chuyển sang màn "Thêm yêu cầu xuất giữ".\n'
     '- Ô Loại yêu cầu để trống, chưa có ô Hợp đồng và chưa có bảng hàng.\n'
     '- Góc phải khối Thông tin chung hiện tên người lập và ngày hôm nay.'),
    ('002', 'Chọn loại có hợp đồng thì hiện ô Hợp đồng', 'P0',
     'Đang ở màn Tạo mới.',
     '1. Chọn Loại yêu cầu = Xuất giữ HĐ hãng.',
     '—',
     '- Hiện ô Hợp đồng kèm nút Chọn.\n- Hiện ô Mã khách hàng (khóa).\n'
     '- Ô Khách hàng bị khóa, có biểu tượng ⓘ giải thích.\n'
     '- KHÔNG có nút Thêm hàng hóa.'),
    ('003', 'Chọn loại Xuất giữ khác thì hiện ô chọn Khách hàng và nút Thêm hàng hóa', 'P0',
     'Đang ở màn Tạo mới.',
     '1. Chọn Loại yêu cầu = Xuất giữ khác.',
     '—',
     '- KHÔNG có ô Hợp đồng.\n- Ô Khách hàng mở khóa, có dấu * bắt buộc.\n'
     '- Có nút Thêm hàng hóa ở khối Chi tiết.\n'
     '- Ô Ghi chú có dấu * và khối File đính kèm có dấu *.'),
    ('004', 'Đổi loại yêu cầu thì xóa sạch bảng hàng đang có', 'P0',
     'Đang ở màn Tạo mới, đã chọn loại Xuất giữ khác và thêm 2 dòng hàng.',
     '1. Đổi Loại yêu cầu sang Xuất giữ HĐ hãng.',
     '—',
     '- ⚠️ Bảng Chi tiết trống trở lại.\n'
     '- Không còn dòng hàng nào của loại cũ sót lại.'),
    ('005', 'Mở cửa sổ Chọn hợp đồng', 'P0',
     'Đã chọn loại Xuất giữ HĐ hãng.',
     '1. Bấm nút Chọn cạnh ô Hợp đồng.',
     '—',
     '- Cửa sổ "Chọn hợp đồng" mở ra.\n'
     '- Có ô tìm theo số hợp đồng / tên khách hàng, bảng hợp đồng và phân trang.\n'
     '- Mỗi dòng có nút Chọn.'),
    ('006', 'Cửa sổ Chọn hợp đồng đổi bảng nguồn theo loại yêu cầu', 'P1',
     'Đang ở màn Tạo mới.',
     '1. Chọn loại Xuất giữ HĐ hãng, mở cửa sổ hợp đồng, ghi lại vài số hợp đồng.\n'
     '2. Quay lại, đổi sang Xuất giữ HĐDV, mở lại cửa sổ.',
     '—',
     '- ⚠️ Hai lần cho ra hai tập hợp đồng khác nhau.\n'
     '- Không lẫn hợp đồng của loại kia.'),
    ('007', 'Chọn hợp đồng thì tự điền khách hàng và nạp hàng', 'P0',
     'Cửa sổ Chọn hợp đồng đang mở.',
     '1. Bấm nút Chọn ở một dòng hợp đồng.',
     '—',
     '- Ô Hợp đồng điền số hợp đồng.\n'
     '- Tự điền Mã khách hàng, Khách hàng, Số điện thoại, Địa chỉ, Địa chỉ giao hàng.\n'
     '- Bảng Chi tiết nạp toàn bộ hàng hóa của hợp đồng, kèm SL hợp đồng và Đã xuất kho.\n'
     '- Mọi dòng mặc định CHƯA tích Cần xuất.'),
    ('008', 'Loại có hợp đồng không thêm và không xóa dòng được', 'P0',
     'Đã chọn hợp đồng, bảng có 5 dòng.',
     '1. Soát khối Chi tiết.',
     '—',
     '- ⚠️ KHÔNG có nút Thêm hàng hóa.\n- KHÔNG có nút xóa dòng ở cuối mỗi dòng.\n'
     '- Ô ĐVT chỉ hiển thị, không chọn được.'),
    ('009', 'Tích Cần xuất thì mở khóa ô nhập số lượng', 'P0',
     'Bảng hàng của hợp đồng đang hiển thị, chưa tích dòng nào.',
     '1. Tích ô Cần xuất ở dòng 1.',
     '—',
     '- Dòng hết bị làm mờ.\n- Ô Đề nghị của dòng đó cho nhập.\n'
     '- Các dòng chưa tích vẫn mờ và không nhập được.'),
    ('010', 'Loại Xuất giữ HĐDV ẩn hai cột hợp đồng', 'P1',
     'Đã chọn loại Xuất giữ HĐDV và chọn một hợp đồng dịch vụ.',
     '1. Soát dòng tiêu đề bảng Chi tiết.',
     '—',
     '- ⚠️ KHÔNG có cột "SL hợp đồng" và cột "Đã xuất kho".\n'
     '- Vẫn có cột Có thể giữ và cột Đề nghị.'),
    ('011', 'Thêm hàng hóa ở loại Xuất giữ khác', 'P0',
     'Đã chọn loại Xuất giữ khác.',
     '1. Bấm nút Thêm hàng hóa.\n2. Tìm và tích 2 hàng hóa.\n3. Bấm Chọn.',
     '—',
     '- Hai dòng được thêm vào bảng Chi tiết.\n'
     '- Mỗi dòng có ô chọn ĐVT, ô nhập Đề nghị và nút xóa dòng.\n'
     '- KHÔNG có cột Cần xuất ở loại này.'),
    ('012', 'Xóa dòng hàng ở loại Xuất giữ khác', 'P1',
     'Bảng Chi tiết có 3 dòng.',
     '1. Bấm biểu tượng thùng rác ở dòng 2.',
     '—',
     '- Dòng 2 biến mất, còn 2 dòng.\n- STT đánh lại liên tục 1, 2.'),
    ('013', 'Đổi ĐVT thì tính lại số Có thể giữ', 'P0',
     'Dòng hàng có 2 đơn vị tính: Cái (hệ số 1) và Thùng (hệ số 10). Tồn kho 100 Cái.',
     '1. Để ĐVT = Cái, ghi lại số Có thể giữ.\n2. Đổi ĐVT sang Thùng.',
     '—',
     '- Bước 1: Có thể giữ = 100.\n- Bước 2: Có thể giữ = 10.\n'
     '- Số ở ô Đề nghị giữ nguyên, không bị xóa.'),
    ('014', 'Lưu nháp thành công', 'P0',
     'Đã điền đủ: loại, hợp đồng, Giữ đến ngày, tích 1 dòng với số lượng hợp lệ.',
     '1. Bấm Lưu nháp.',
     '—',
     '- Thông báo lưu thành công.\n- Quay về màn danh sách.\n'
     '- Phiếu mới có mã dạng PYCXG-NNNNN và trạng thái "Đang tạo".\n'
     '- Chỉ người lập nhìn thấy phiếu này.'),
    ('015', 'Gửi duyệt thành công', 'P0',
     'Đã điền đủ dữ liệu hợp lệ, tồn kho đủ.',
     '1. Bấm Gửi duyệt.',
     '—',
     '- Thông báo thành công, quay về danh sách.\n'
     '- Phiếu ở trạng thái "Chờ TP duyệt".\n'
     '- Trưởng phòng quản lý phòng ban của người lập nhận được thông báo.'),
    ('016', 'Lưu và tiếp tục chỉ có ở màn Tạo mới', 'P1',
     'Đang ở màn Tạo mới, rồi mở một phiếu để Sửa.',
     '1. Soát bộ nút ở cuối màn Tạo mới.\n2. Soát bộ nút ở cuối màn Sửa.',
     '—',
     '- Màn Tạo mới CÓ nút "Lưu và tiếp tục".\n- Màn Sửa KHÔNG có nút đó.'),
    ('017', 'Bấm Lưu và tiếp tục thì ở lại màn', 'P1',
     'Đã điền đủ dữ liệu hợp lệ ở màn Tạo mới.',
     '1. Bấm Lưu và tiếp tục.',
     '—',
     '- Phiếu được lưu ở trạng thái Đang tạo.\n'
     '- ⚠️ KHÔNG quay về danh sách; màn hình được làm mới để nhập phiếu kế tiếp.'),
    ('018', 'Lưu nháp KHÔNG kiểm tra tồn kho', 'P0',
     'Hàng HH01 chỉ còn 2 trong kho. Nhập SL đề nghị = 50.',
     '1. Bấm Lưu nháp.',
     '—',
     '- ⚠️ Lưu THÀNH CÔNG, không báo thiếu hàng.\n- Phiếu ở trạng thái Đang tạo.'),
    ('019', 'Gửi duyệt CÓ kiểm tra tồn kho', 'P0',
     'Tiếp nối TC 018: phiếu nháp có SL đề nghị = 50 mà kho chỉ còn 2.',
     '1. Mở phiếu ra Sửa.\n2. Bấm Gửi duyệt.',
     '—',
     '- ⚠️ Bị chặn, báo đỏ tại dòng: "Vượt số có thể giữ (còn 2)."\n'
     '- Phiếu vẫn ở trạng thái Đang tạo.\n'
     '- Giá trị 50 vẫn nguyên trong ô, phần mềm KHÔNG tự kéo về 2.'),
    ('020', 'Mã phiếu sinh đúng định dạng và không trùng', 'P0',
     'Lập liên tiếp 3 phiếu.',
     '1. Lưu nháp lần lượt 3 phiếu.\n2. Soát mã của 3 phiếu.',
     '—',
     '- Mã dạng PYCXG- kèm 5 chữ số.\n- Ba mã khác nhau, tăng dần.\n'
     '- ⚠️ Không mã nào là chuỗi ngẫu nhiên vô nghĩa.'),
    ('021', 'Rời màn khi chưa lưu thì hỏi xác nhận', 'P1',
     'Đã nhập vài thông tin ở màn Tạo mới, chưa lưu.',
     '1. Bấm Quay lại.',
     '—',
     '- Hệ thống hỏi xác nhận rời trang.\n- Chọn Ở lại thì giữ nguyên dữ liệu đang nhập.'),
    ('022', 'Đính kèm nhiều tệp', 'P1',
     'Đang ở màn Tạo mới.',
     '1. Bấm Chọn tệp, tải lên 1 tệp PDF.\n2. Tải tiếp 1 ảnh.',
     'tệp PDF < 13 MB, ảnh PNG',
     '- Danh sách tệp có 2 dòng, mỗi dòng có nút gỡ.\n'
     '- Bấm vào tên tệp mở xem được.'),
    ('023', 'Gỡ tệp đính kèm', 'P1',
     'Phiếu đang có 2 tệp đính kèm.',
     '1. Bấm nút gỡ ở tệp thứ nhất.',
     '—',
     '- Còn 1 tệp trong danh sách.\n- Không phải tải lại trang.'),
    ('024', 'Phòng ban yêu cầu tự điền theo người lập', 'P1',
     'Người lập thuộc phòng "PHÒNG THIẾT BỊ Ô TÔ 2".',
     '1. Mở màn Tạo mới và soát ô Phòng ban yêu cầu.',
     '—',
     '- Ô hiển thị đúng "PHÒNG THIẾT BỊ Ô TÔ 2", khóa lại.\n'
     '- Ô khóa có biểu tượng ⓘ giải thích.'),
    ('025', 'Dòng không tích vẫn được lưu với số lượng 0', 'P1',
     'Hợp đồng có 5 dòng hàng; chỉ tích 2 dòng.',
     '1. Lưu nháp.\n2. Mở lại phiếu ở màn Sửa.',
     '—',
     '- ⚠️ Bảng vẫn có đủ 5 dòng.\n'
     '- 3 dòng không tích hiện số lượng 0 và bị làm mờ.'),
    ('026', 'Ô Giữ đến ngày chặn sẵn ngày quá khứ trên lịch', 'P0',
     'Đang ở màn Tạo mới.',
     '1. Mở lịch ở ô Giữ đến ngày.\n2. Thử bấm một ngày trước hôm nay.',
     '—',
     '- Ngày quá khứ hiển thị mờ và KHÔNG bấm được.\n'
     '- ⚠️ Chặn ngay trên lịch, không để chọn xong mới báo lỗi.'),
    ('027', 'Dòng nhắc hạn giữ tối đa hiển thị dưới ô Giữ đến ngày', 'P1',
     'Đang ở màn Tạo mới, đã chọn loại yêu cầu.',
     '1. Soát ngay dưới ô Giữ đến ngày.',
     '—',
     '- Có dòng chữ nhỏ "Không giữ quá <ngày>".\n'
     '- Ngày này bằng hôm nay cộng số ngày trần cấu hình.'),
    ('028', 'Loại HĐDA dùng trần hạn giữ riêng', 'P1',
     'Cấu hình: trần chung 60 ngày, trần cho hợp đồng dự án 90 ngày.',
     '1. Chọn loại Xuất giữ HĐDA và soát dòng nhắc hạn.\n'
     '2. Đổi sang loại khác và soát lại.',
     '—',
     '- ⚠️ Loại HĐDA hiện trần 90 ngày; loại khác hiện trần 60 ngày.'),
    ('029', 'Đơn giá và Thành tiền tính đúng', 'P1',
     'Dòng hàng có Đơn giá 1,250,000. Nhập SL đề nghị = 3.',
     '1. Nhập số lượng và rời ô.',
     '3',
     '- Cột Thành tiền hiện 3,750,000.\n'
     '- Số định dạng theo chuẩn quốc tế, dấu phẩy ngăn hàng nghìn.'),
    ('030', 'Dòng Tổng cộng cộng đúng', 'P1',
     'Bảng có 3 dòng tích với SL 2, 3, 5 và thành tiền tương ứng.',
     '1. Soát dòng Tổng cộng cuối bảng.',
     '—',
     '- Cột Đề nghị tổng = 10.\n- Cột Thành tiền tổng = tổng ba dòng.'),
]

S5 = [
    ('001', 'Nút Sửa chỉ hiện với phiếu Đang tạo của mình', 'P0',
     'Danh sách có phiếu của mình ở nhiều trạng thái và phiếu của người khác.',
     '1. Soát cột Hành động của từng dòng.',
     '—',
     '- Chỉ phiếu "Đang tạo" do chính mình lập mới có biểu tượng bút chì.\n'
     '- ⚠️ Nút ẩn hẳn, không ở trạng thái mờ.'),
    ('002', 'Mở màn Sửa từ danh sách', 'P0',
     'Có phiếu Đang tạo của mình.',
     '1. Bấm biểu tượng bút chì.',
     '—',
     '- Chuyển sang màn "Sửa yêu cầu xuất giữ: <mã phiếu>".\n'
     '- Dữ liệu đã lưu nạp đầy đủ.'),
    ('003', 'Mở màn Sửa từ màn chi tiết', 'P1',
     'Đang xem chi tiết một phiếu Đang tạo của mình.',
     '1. Bấm nút Sửa ở cuối màn.',
     '—',
     '- Chuyển sang màn Sửa đúng phiếu đó.'),
    ('004', 'Loại yêu cầu và Hợp đồng bị khóa ở màn Sửa', 'P0',
     'Đang ở màn Sửa một phiếu loại Xuất giữ HĐ hãng.',
     '1. Thử đổi ô Loại yêu cầu và ô Hợp đồng.',
     '—',
     '- ⚠️ Cả hai ô đều khóa, không đổi được.\n'
     '- Ô Loại yêu cầu có biểu tượng ⓘ giải thích vì sao.\n'
     '- Không có nút Chọn cạnh ô Hợp đồng.'),
    ('005', 'Loại Xuất giữ khác vẫn đổi được khách hàng khi sửa', 'P1',
     'Đang sửa một phiếu loại Xuất giữ khác.',
     '1. Đổi ô Khách hàng sang khách khác.\n2. Lưu nháp.\n3. Mở lại phiếu.',
     '—',
     '- Khách hàng mới được lưu.\n'
     '- ⚠️ Với loại có hợp đồng thì ô này khóa, không đổi được.'),
    ('006', 'Sửa số lượng rồi lưu nháp', 'P0',
     'Phiếu Đang tạo có dòng SL đề nghị = 2.',
     '1. Đổi thành 5.\n2. Bấm Lưu nháp.\n3. Mở lại phiếu.',
     '5',
     '- Số lượng đã đổi thành 5.\n- Trạng thái vẫn "Đang tạo".'),
    ('007', 'Sửa rồi Gửi duyệt thì đặt lại dấu duyệt của cả ba cấp', 'P0',
     'Phiếu đã qua TP duyệt và BGĐ duyệt rồi bị Kế toán từ chối, đang ở Đang tạo. Màn chi tiết '
     'trước đó còn hiện tên TP và BGĐ đã duyệt.',
     '1. Người lập mở phiếu ra Sửa, đổi số lượng.\n2. Bấm Gửi duyệt.\n3. Mở màn chi tiết.',
     '—',
     '- ⚠️ Khối Lịch sử duyệt KHÔNG còn tên TP và BGĐ cũ.\n'
     '- Phiếu ở trạng thái "Chờ TP duyệt".\n'
     '- Ô Lý do từ chối gần nhất đã bị xóa.'),
    ('008', 'Ô Lý do từ chối gần nhất hiện đúng khi phiếu bị trả về', 'P0',
     'Phiếu vừa bị Trưởng phòng từ chối với lý do "Số lượng đề nghị quá nhiều".',
     '1. Người lập mở phiếu ra Sửa.',
     '—',
     '- Cuối khối Thông tin chung có ô "Lý do từ chối gần nhất" ghi đúng nội dung.\n'
     '- Ô này chỉ hiển thị, không sửa được.'),
    ('009', 'Phiếu chưa từng gửi thì KHÔNG có ô Lý do từ chối', 'P1',
     'Phiếu nháp mới lập, chưa gửi duyệt lần nào.',
     '1. Mở phiếu ra Sửa.',
     '—',
     '- ⚠️ Không có ô "Lý do từ chối gần nhất".\n'
     '- Đây là cách phân biệt phiếu chưa gửi với phiếu bị trả về.'),
    ('010', 'Không sửa được phiếu đang chờ duyệt', 'P0',
     'Phiếu của mình đang ở "Chờ TP duyệt".',
     '1. Soát cột Hành động — không thấy nút Sửa.\n'
     '2. Mở màn Sửa bằng đường dẫn trực tiếp.',
     '—',
     '- Bước 1: không có nút Sửa.\n'
     '- Bước 2: hệ thống từ chối, không mở màn sửa.'),
    ('011', 'Không sửa được phiếu của người khác', 'P0',
     'Có phiếu "Đang tạo" của người khác (biết mã qua tài khoản quản trị).',
     '1. Mở màn Sửa phiếu đó bằng đường dẫn trực tiếp.',
     '—',
     '- Hệ thống từ chối.\n- Không đọc được dữ liệu phiếu.'),
    ('012', 'Loại Xuất giữ khác: gỡ hết tệp rồi lưu thì bị chặn', 'P0',
     'Phiếu loại Xuất giữ khác đang có 1 tệp đính kèm, trạng thái Đang tạo.',
     '1. Mở màn Sửa.\n2. Gỡ tệp duy nhất.\n3. Bấm Lưu nháp.',
     '—',
     '- ⚠️ Bị chặn, báo "Bắt buộc phải chọn" ở khối File đính kèm.\n'
     '- Phiếu giữ nguyên tệp cũ.'),
    ('013', 'Tồn kho khi sửa tính theo NGƯỜI LẬP, không theo người sửa', 'P1',
     'Tài khoản quản trị sửa phiếu của nhân viên A. Tồn kho khả dụng khác nhau giữa hai người.',
     '1. Tài khoản quản trị mở phiếu của A ra Sửa và bấm Gửi duyệt.',
     '—',
     '- ⚠️ Số được kiểm là tồn kho theo A (chủ phiếu), không theo tài khoản quản trị.'),
    ('014', 'Màn Sửa không có nút Lưu và tiếp tục', 'P2',
     'Đang ở màn Sửa.',
     '1. Soát bộ nút ở cuối màn.',
     '—',
     '- Chỉ có Lưu nháp, Gửi duyệt, Quay lại.'),
]

S6 = [
    ('001', 'Mở màn chi tiết bằng cách bấm mã phiếu', 'P0',
     'Có phiếu trong danh sách.',
     '1. Bấm mã phiếu.',
     '—',
     '- Tiêu đề màn ghi "Chi tiết yêu cầu xuất giữ: <mã phiếu>".\n'
     '- Toàn bộ ô ở chế độ chỉ đọc.'),
    ('002', 'Màn chi tiết có đủ các khối', 'P0',
     'Đang xem chi tiết một phiếu đã duyệt.',
     '1. Cuộn hết màn hình.',
     '—',
     '- Có các khối: Thông tin chung, File đính kèm, Chi tiết, Lịch sử duyệt, '
     'Lịch sử thay đổi (thu gọn).'),
    ('003', 'Nút ở màn chi tiết KHỚP với cột Hành động ngoài danh sách', 'P0',
     'Chọn 3 phiếu ở 3 trạng thái khác nhau.',
     '1. Với mỗi phiếu: ghi lại các nút ở cột Hành động.\n2. Mở chi tiết và ghi lại nút cuối màn.',
     '—',
     '- ⚠️ Hai bộ nút khớp nhau, chỉ khác: màn chi tiết CÓ THÊM nút Từ chối và nút Quay lại.'),
    ('004', 'Người xem không sửa được số lượng ở màn chi tiết', 'P0',
     'Đang xem chi tiết một phiếu Chờ TP duyệt bằng tài khoản Trưởng phòng.',
     '1. Thử bấm vào ô số lượng ở bảng Chi tiết.',
     '—',
     '- Ô chỉ hiển thị số, không nhập được.\n- Không có ô tích Cần xuất nào bấm được.'),
    ('005', 'Khối File đính kèm khi không có tệp', 'P1',
     'Phiếu loại có hợp đồng, không đính kèm tệp nào.',
     '1. Soát khối File đính kèm.',
     '—',
     '- Hiện dòng "Chưa có tệp đính kèm".\n- Không có nút Chọn tệp.'),
    ('006', 'Mở tệp đính kèm từ màn chi tiết', 'P1',
     'Phiếu có 1 tệp PDF đính kèm.',
     '1. Bấm vào tên tệp.',
     '—',
     '- Tệp mở ở tab mới, xem được nội dung.'),
    ('007', 'Khối Lịch sử duyệt ghi đủ các cấp đã duyệt', 'P0',
     'Phiếu đã duyệt xong, đã qua TP, BGĐ và Kế toán.',
     '1. Soát khối Lịch sử duyệt.',
     '—',
     '- Có dòng cho từng cấp đã duyệt, ghi tên người và thời điểm.\n'
     '- Bước Kế toán ghi rõ phiếu được duyệt qua mã phiếu xuất giữ nào.'),
    ('008', 'Phiếu Đang tạo của người khác không mở được chi tiết', 'P0',
     'Biết mã một phiếu nháp của người khác.',
     '1. Mở màn chi tiết bằng đường dẫn trực tiếp.',
     '—',
     '- Hệ thống báo không có quyền xem phiếu này.\n- Không hiện dữ liệu phiếu.'),
    ('009', 'Người lập luôn xem được phiếu của mình', 'P1',
     'Người lập không có quyền xem theo cấp nào; phiếu đã sang Chờ BGĐ duyệt.',
     '1. Người lập mở màn chi tiết phiếu của mình.',
     '—',
     '- Mở được bình thường, xem đủ thông tin.\n- Không có nút duyệt hay từ chối.'),
    ('010', 'Bảng Chi tiết ở màn chi tiết hiện đủ cột theo loại', 'P1',
     'Có phiếu loại có hợp đồng và phiếu loại Xuất giữ khác.',
     '1. Mở chi tiết từng phiếu và soát dòng tiêu đề bảng.',
     '—',
     '- Loại có hợp đồng: có cột Cần xuất, SL hợp đồng, Đã xuất kho.\n'
     '- Loại Xuất giữ khác: không có ba cột đó.'),
    ('011', 'Nút Quay lại về đúng màn danh sách', 'P2',
     'Đang xem chi tiết một phiếu, đến từ danh sách đang lọc.',
     '1. Bấm Quay lại.',
     '—',
     '- Về màn danh sách.\n- Bộ lọc trước đó vẫn còn.'),
]

S7 = [
    ('001', 'Nút TP duyệt chỉ hiện với đúng người và đúng trạng thái', 'P0',
     'Phiếu ở Chờ TP duyệt, phòng ban P1. Ba tài khoản: TP quản lý P1, TP quản lý P2, và nhân '
     'viên thường.',
     '1. Lần lượt mở màn chi tiết phiếu bằng ba tài khoản.',
     '—',
     '- TP quản lý P1: có nút "TP duyệt" và "Từ chối".\n'
     '- TP quản lý P2: KHÔNG có hai nút đó.\n'
     '- Nhân viên thường: KHÔNG có hai nút đó.'),
    ('002', 'Trưởng phòng khác công ty không duyệt được', 'P0',
     'Phiếu thuộc công ty 1. Tài khoản TP có quyền nhưng thuộc công ty 4 và quản lý phòng cùng tên.',
     '1. Mở màn chi tiết phiếu bằng tài khoản đó.',
     '—',
     '- Nút duyệt KHÔNG hiển thị.\n'
     '- Gọi thẳng chức năng duyệt thì báo "Bạn không có quyền duyệt bước này.".'),
    ('003', 'Duyệt cấp Trưởng phòng có hộp thoại xác nhận', 'P0',
     'Đang xem chi tiết phiếu Chờ TP duyệt bằng tài khoản đủ quyền.',
     '1. Bấm nút TP duyệt.',
     '—',
     '- Mở hộp thoại "Xác nhận duyệt" ghi rõ mã phiếu.\n'
     '- Có nút xác nhận "Duyệt" và nút hủy.'),
    ('004', 'Hủy ở hộp thoại xác nhận thì không làm gì', 'P1',
     'Hộp thoại xác nhận duyệt đang mở.',
     '1. Bấm Hủy.',
     '—',
     '- Hộp thoại đóng.\n- Trạng thái phiếu KHÔNG đổi.'),
    ('005', 'Trưởng phòng duyệt phiếu KHÔNG phải qua Ban giám đốc', 'P0',
     'Phiếu gắn hợp đồng có tỉ lệ thu tiền đã vượt ngưỡng cấu hình.',
     '1. Trưởng phòng bấm TP duyệt và xác nhận.',
     '—',
     '- Thông báo "Yêu cầu đã được chuyển đến Kế toán."\n'
     '- ⚠️ Phiếu sang thẳng "Chờ KT duyệt", BỎ QUA bước Ban giám đốc.\n'
     '- Quay về màn danh sách.'),
    ('006', 'Trưởng phòng duyệt phiếu PHẢI qua Ban giám đốc', 'P0',
     'Phiếu gắn hợp đồng có tỉ lệ thu tiền THẤP HƠN ngưỡng cấu hình.',
     '1. Trưởng phòng bấm TP duyệt và xác nhận.',
     '—',
     '- Thông báo "Yêu cầu đã được chuyển đến Ban giám đốc."\n'
     '- Phiếu sang "Chờ BGĐ duyệt".'),
    ('007', 'Phiếu loại Xuất giữ khác vượt hạn mức phải qua Ban giám đốc', 'P0',
     'Cấu hình hạn mức của công ty = 10,000,000. Phiếu loại Xuất giữ khác có tổng thành tiền các '
     'dòng cần xuất = 15,000,000.',
     '1. Trưởng phòng duyệt.',
     '—',
     '- ⚠️ Phiếu sang "Chờ BGĐ duyệt" vì tổng tiền vượt hạn mức.'),
    ('008', 'Phiếu loại Xuất giữ khác dưới hạn mức đi thẳng Kế toán', 'P1',
     'Cùng cấu hình TC 007. Phiếu có tổng thành tiền = 3,000,000.',
     '1. Trưởng phòng duyệt.',
     '—',
     '- Phiếu sang thẳng "Chờ KT duyệt".'),
    ('009', 'Bước Ban giám đốc BẮT BUỘC nhập lại Giữ đến ngày', 'P0',
     'Phiếu ở Chờ BGĐ duyệt; tài khoản có quyền Ban giám đốc duyệt hàng giữ.',
     '1. Mở màn chi tiết.\n2. Bấm BGĐ duyệt mà bỏ trống ô Giữ đến ngày.',
     '—',
     '- ⚠️ Bị chặn, báo "Giữ đến ngày – Bắt buộc phải nhập."\n'
     '- Phiếu vẫn ở Chờ BGĐ duyệt.'),
    ('010', 'Ban giám đốc đổi hạn giữ rồi duyệt', 'P0',
     'Phiếu ở Chờ BGĐ duyệt, hạn giữ hiện tại 30/09/2026.',
     '1. Ban giám đốc đổi Giữ đến ngày thành 15/10/2026 rồi bấm BGĐ duyệt.',
     '15/10/2026',
     '- Thông báo "Yêu cầu đã được chuyển đến Kế toán."\n'
     '- Phiếu sang "Chờ KT duyệt".\n'
     '- ⚠️ Hạn giữ trên phiếu đổi thành 15/10/2026, đi tiếp xuống Kế toán.'),
    ('011', 'Ban giám đốc nhập ngày quá khứ thì bị chặn', 'P0',
     'Phiếu ở Chờ BGĐ duyệt.',
     '1. Nhập Giữ đến ngày là ngày hôm qua rồi bấm BGĐ duyệt.',
     'ngày hôm qua',
     '- Báo "Giữ đến ngày – Phải nhập ngày tương lai."\n- Phiếu không đổi trạng thái.'),
    ('012', 'Ban giám đốc nhập ngày vượt trần thì bị chặn', 'P0',
     'Trần hạn giữ là hôm nay + 60 ngày.',
     '1. Nhập Giữ đến ngày là hôm nay + 200 ngày rồi bấm BGĐ duyệt.',
     'hôm nay + 200 ngày',
     '- Báo "Giữ đến ngày – Không thể giữ quá …"\n'
     '- ⚠️ Phần mềm KHÔNG tự kéo ngày về mức trần.'),
    ('013', 'Kế toán KHÔNG có nút duyệt ở màn này', 'P0',
     'Phiếu ở "Chờ KT duyệt"; tài khoản có quyền Kế toán duyệt hàng giữ.',
     '1. Mở màn chi tiết phiếu.\n2. Soát bộ nút ở cuối màn.',
     '—',
     '- ⚠️ KHÔNG có nút "KT duyệt".\n'
     '- Thay vào đó có nút "Lập phiếu xuất giữ" và nút "Từ chối".'),
    ('014', 'Nút Từ chối chỉ có ở màn chi tiết', 'P0',
     'Phiếu đang chờ chính mình duyệt.',
     '1. Soát cột Hành động ngoài danh sách.\n2. Mở chi tiết và soát bộ nút cuối màn.',
     '—',
     '- ⚠️ Cột Hành động KHÔNG có nút Từ chối.\n- Màn chi tiết CÓ nút Từ chối.'),
    ('015', 'Từ chối bỏ trống lý do thì bị chặn', 'P0',
     'Cửa sổ Từ chối đang mở.',
     '1. Để trống ô Lý do rồi bấm nút xác nhận.',
     '—',
     '- Báo bắt buộc nhập.\n- ⚠️ Cửa sổ KHÔNG đóng.\n- Phiếu giữ nguyên trạng thái.'),
    ('016', 'Từ chối với lý do quá 255 ký tự', 'P1',
     'Cửa sổ Từ chối đang mở.',
     '1. Nhập 300 ký tự vào ô Lý do rồi bấm xác nhận.',
     'chuỗi 300 ký tự',
     '- Báo "Không được vượt quá 255 ký tự".\n- Không lưu.'),
    ('017', 'Trưởng phòng từ chối đưa phiếu về Đang tạo', 'P0',
     'Phiếu ở Chờ TP duyệt.',
     '1. Trưởng phòng bấm Từ chối, nhập lý do, xác nhận.',
     'Lý do: Số lượng đề nghị quá nhiều',
     '- Thông báo thành công, quay về danh sách.\n'
     '- ⚠️ Phiếu về đúng trạng thái "Đang tạo", KHÔNG có trạng thái "Từ chối" riêng.\n'
     '- Bật cột Lý do từ chối: hiện đúng nội dung đã nhập.\n'
     '- Người lập nhận được thông báo.'),
    ('018', 'Ban giám đốc từ chối được', 'P1',
     'Phiếu ở Chờ BGĐ duyệt.',
     '1. Ban giám đốc bấm Từ chối, nhập lý do, xác nhận.',
     'Lý do: Chưa thu đủ tiền hợp đồng',
     '- Phiếu về "Đang tạo" kèm lý do.'),
    ('019', 'Kế toán từ chối được ở bước Chờ KT duyệt', 'P0',
     'Phiếu ở Chờ KT duyệt.',
     '1. Kế toán bấm Từ chối, nhập lý do, xác nhận.',
     'Lý do: Kho không còn đủ hàng',
     '- ⚠️ Kế toán VẪN từ chối được ở bước này.\n- Phiếu về "Đang tạo" kèm lý do.'),
    ('020', 'Phiếu bị từ chối chỉ người lập nhìn thấy', 'P0',
     'Phiếu vừa bị từ chối, đang ở "Đang tạo".',
     '1. Tài khoản có quyền xem tổng công ty tìm mã phiếu đó.\n'
     '2. Người lập tìm mã phiếu đó.',
     '—',
     '- Bước 1: không tìm thấy.\n- Bước 2: tìm thấy, mở được.'),
    ('021', 'Từ chối KHÔNG đụng tới tồn hàng giữ', 'P0',
     'Trước khi từ chối, ghi lại tồn hàng giữ của người lập với hàng HH01.',
     '1. Từ chối phiếu.\n2. Mở màn Danh sách hàng giữ và đối chiếu.',
     '—',
     '- ⚠️ Tồn hàng giữ KHÔNG đổi, vì yêu cầu chưa từng ghi tồn.'),
    ('022', 'Duyệt phiếu đã bị người khác xử lý trước', 'P0',
     'Hai người cùng mở một phiếu Chờ TP duyệt. Người 1 đã duyệt xong.',
     '1. Người 2 bấm TP duyệt trên màn đang mở.',
     '—',
     '- Báo "Phiếu không ở trạng thái chờ duyệt."\n- Phiếu không bị duyệt hai lần.'),
    ('023', 'Từ chối phiếu đã bị người khác xử lý trước', 'P1',
     'Hai người cùng mở một phiếu. Người 1 đã từ chối xong.',
     '1. Người 2 bấm Từ chối, nhập lý do, xác nhận.',
     'Lý do bất kỳ',
     '- Báo "Bạn không có quyền từ chối phiếu này."\n- Lý do của người 1 không bị ghi đè.'),
    ('024', 'Gọi thẳng chức năng duyệt khi không đủ quyền', 'P0',
     'Tester kỹ thuật dùng công cụ kiểm thử. Tài khoản không có quyền duyệt nào.',
     '1. Gọi thẳng chức năng duyệt của một phiếu Chờ TP duyệt.',
     '—',
     '- Hệ thống từ chối, báo "Bạn không có quyền duyệt bước này."\n'
     '- Trạng thái phiếu không đổi.'),
    ('025', 'Gọi thẳng chức năng duyệt với phiếu sai trạng thái', 'P1',
     'Tester kỹ thuật. Phiếu đang ở "Đang tạo".',
     '1. Gọi thẳng chức năng duyệt phiếu đó.',
     '—',
     '- Báo "Phiếu không ở trạng thái chờ duyệt."'),
    ('026', 'Người duyệt không sửa được số lượng', 'P0',
     'Trưởng phòng đang xem phiếu Chờ TP duyệt.',
     '1. Thử sửa ô số lượng ở bảng Chi tiết.',
     '—',
     '- Ô chỉ hiển thị.\n- Muốn đổi số thì phải Từ chối để người lập sửa.'),
]

S8 = [
    ('001', 'Nút Lập phiếu xuất giữ chỉ hiện với Kế toán đúng điều kiện', 'P0',
     'Phiếu ở "Chờ KT duyệt", công ty 1. Ba tài khoản: Kế toán công ty 1, Kế toán công ty 4, '
     'Trưởng phòng công ty 1.',
     '1. Lần lượt mở màn chi tiết phiếu bằng ba tài khoản.',
     '—',
     '- Kế toán công ty 1: CÓ nút "Lập phiếu xuất giữ".\n'
     '- Kế toán công ty 4: KHÔNG có nút đó.\n'
     '- Trưởng phòng: KHÔNG có nút đó.'),
    ('002', 'Nút Lập phiếu xuất giữ không hiện ở trạng thái khác', 'P0',
     'Kế toán mở lần lượt phiếu ở Chờ TP duyệt, Chờ BGĐ duyệt, Đang xuất giữ, Đã duyệt.',
     '1. Soát bộ nút cuối màn ở từng phiếu.',
     '—',
     '- Chỉ phiếu "Chờ KT duyệt" mới có nút đó.\n'
     '- ⚠️ Phiếu "Đang xuất giữ" KHÔNG có nút, vì đã có phiếu xuất giữ rồi.'),
    ('003', 'Bấm Lập phiếu xuất giữ chuyển sang màn lập phiếu con', 'P0',
     'Kế toán đang xem phiếu Chờ KT duyệt.',
     '1. Bấm nút Lập phiếu xuất giữ.',
     '—',
     '- Chuyển sang màn "Lập phiếu xuất giữ".\n'
     '- Ô Yêu cầu xuất giữ điền sẵn mã yêu cầu, khóa lại.\n'
     '- Bảng hàng nạp sẵn những dòng đã tích Cần xuất của yêu cầu.'),
    ('004', 'Lưu nháp phiếu con thì yêu cầu sang Đang xuất giữ', 'P0',
     'Đang ở màn lập phiếu xuất giữ từ yêu cầu PYCXG-XXXXX.',
     '1. Bấm Lưu nháp ở màn phiếu xuất giữ.\n2. Quay lại màn Yêu cầu xuất giữ và tìm mã đó.',
     '—',
     '- ⚠️ Yêu cầu chuyển sang trạng thái "Đang xuất giữ" (màu cam).\n'
     '- Tồn hàng giữ CHƯA đổi.\n'
     '- Lịch sử thay đổi của yêu cầu có thêm một mốc.'),
    ('005', 'Duyệt phiếu con thì yêu cầu sang Đã duyệt', 'P0',
     'Phiếu xuất giữ còn nháp từ yêu cầu PYCXG-XXXXX.',
     '1. Mở phiếu xuất giữ ra Sửa, bấm Duyệt giữ hàng và xác nhận.\n'
     '2. Quay lại màn Yêu cầu xuất giữ.',
     '—',
     '- ⚠️ Yêu cầu chuyển sang "Đã duyệt" (xanh lá).\n'
     '- Cột Người duyệt và Ngày duyệt được điền tên Kế toán và thời điểm duyệt.\n'
     '- Lịch sử thay đổi của yêu cầu ghi rõ được duyệt qua mã phiếu xuất giữ nào.'),
    ('006', 'Xóa phiếu con còn nháp thì yêu cầu quay lại Chờ KT duyệt', 'P0',
     'Yêu cầu đang ở "Đang xuất giữ", phiếu xuất giữ còn nháp.',
     '1. Xóa phiếu xuất giữ.\n2. Quay lại màn Yêu cầu xuất giữ.',
     '—',
     '- ⚠️ Yêu cầu quay về "Chờ KT duyệt".\n'
     '- Nút "Lập phiếu xuất giữ" hiện lại.'),
    ('007', 'Một yêu cầu chỉ lập được một phiếu xuất giữ', 'P0',
     'Yêu cầu đã có phiếu xuất giữ PXG-XXXXX.',
     '1. Tester kỹ thuật gọi thẳng chức năng lập phiếu xuất giữ cho yêu cầu đó lần nữa.',
     '—',
     '- ⚠️ Bị chặn, báo "Yêu cầu này đã có phiếu xuất giữ PXG-XXXXX."\n'
     '- Không sinh ra phiếu thứ hai.'),
    ('008', 'Chủ lô hàng giữ là NGƯỜI LẬP YÊU CẦU', 'P0',
     'Yêu cầu do nhân viên A lập. Kế toán B lập và duyệt phiếu xuất giữ.',
     '1. Sau khi duyệt, mở màn Tài chính → Giữ hàng → Danh sách hàng giữ.\n'
     '2. Lọc theo nhân viên A, rồi lọc theo Kế toán B.',
     '—',
     '- ⚠️ Lô hàng giữ mới đứng tên A.\n'
     '- Kế toán B KHÔNG có lô nào tăng thêm.'),
    ('009', 'Công ty của lô lấy theo yêu cầu, không theo Kế toán', 'P1',
     'Yêu cầu thuộc công ty 1. Kế toán có quyền xem tổng công ty và thuộc công ty 4.',
     '1. Kế toán lập và duyệt phiếu xuất giữ.\n2. Kiểm tra lô hàng giữ sinh ra.',
     '—',
     '- ⚠️ Lô thuộc công ty 1 (công ty của yêu cầu), không phải công ty 4.'),
    ('010', 'Gọi thẳng chức năng lập phiếu khi không đủ quyền', 'P0',
     'Tester kỹ thuật. Tài khoản không có quyền Kế toán duyệt hàng giữ.',
     '1. Gọi thẳng chức năng lập phiếu xuất giữ cho một yêu cầu Chờ KT duyệt.',
     '—',
     '- Bị chặn, báo "Bạn không đủ quyền lập phiếu xuất giữ cho yêu cầu này."'),
    ('011', 'Gọi thẳng chức năng lập phiếu khi yêu cầu sai trạng thái', 'P1',
     'Tester kỹ thuật. Yêu cầu đang ở "Chờ TP duyệt".',
     '1. Gọi thẳng chức năng lập phiếu xuất giữ cho yêu cầu đó.',
     '—',
     '- Bị chặn, báo "Yêu cầu này không ở bước Kế toán xử lý, hoặc bạn không đủ quyền lập phiếu '
     'xuất giữ."'),
]

S9 = [
    ('001', 'Nút Xóa chỉ hiện với phiếu Đang tạo của mình', 'P0',
     'Danh sách có phiếu của mình ở nhiều trạng thái.',
     '1. Soát cột Hành động.',
     '—',
     '- Chỉ phiếu "Đang tạo" của chính mình có biểu tượng thùng rác.\n'
     '- Nút ẩn hẳn ở các dòng khác.'),
    ('002', 'Hộp thoại xác nhận xóa ghi rõ mã phiếu', 'P0',
     'Có phiếu Đang tạo của mình.',
     '1. Bấm biểu tượng thùng rác.',
     '—',
     '- Hộp thoại tiêu đề "Xác nhận xóa".\n'
     '- Nội dung "Bạn có chắc muốn xóa phiếu <mã phiếu>?".\n'
     '- Nút Xóa màu đỏ và nút Hủy.'),
    ('003', 'Bấm Hủy thì không xóa gì', 'P0',
     'Hộp thoại xác nhận xóa đang mở.',
     '1. Bấm Hủy.',
     '—',
     '- Hộp thoại đóng.\n- Phiếu vẫn còn trong danh sách.'),
    ('004', 'Xóa phiếu thành công', 'P0',
     'Có phiếu Đang tạo của mình.',
     '1. Bấm thùng rác rồi bấm Xóa.',
     '—',
     '- Thông báo xóa thành công.\n- Phiếu biến mất khỏi danh sách.\n'
     '- N giảm đi 1.'),
    ('005', 'Xóa phiếu không đụng tới hàng giữ', 'P0',
     'Ghi lại tồn hàng giữ của người lập trước khi xóa.',
     '1. Xóa một phiếu Đang tạo.\n2. Đối chiếu tồn hàng giữ.',
     '—',
     '- ⚠️ Tồn hàng giữ không đổi.'),
    ('006', 'Không xóa được phiếu đang chờ duyệt', 'P0',
     'Phiếu của mình đang ở "Chờ TP duyệt".',
     '1. Soát cột Hành động — không có nút Xóa.\n'
     '2. Tester kỹ thuật gọi thẳng chức năng xóa phiếu đó.',
     '—',
     '- Bước 1: không có nút.\n'
     '- Bước 2: bị chặn, báo "Không thể xóa phiếu này."'),
    ('007', 'Không xóa được phiếu đã duyệt', 'P0',
     'Phiếu của mình đã ở trạng thái "Đã duyệt".',
     '1. Tester kỹ thuật gọi thẳng chức năng xóa phiếu đó.',
     '—',
     '- Bị chặn, báo "Không thể xóa phiếu này."\n'
     '- ⚠️ Lô hàng giữ đã sinh ra không bị ảnh hưởng.'),
    ('008', 'Không xóa được phiếu của người khác', 'P0',
     'Biết mã một phiếu "Đang tạo" của người khác.',
     '1. Tester kỹ thuật gọi thẳng chức năng xóa phiếu đó.',
     '—',
     '- Bị chặn, báo "Không thể xóa phiếu này."'),
    ('009', 'Lịch sử thay đổi được giữ lại sau khi xóa', 'P1',
     'Phiếu Đang tạo đã có vài mốc lịch sử.',
     '1. Xóa phiếu.\n2. Tra cứu lịch sử của phiếu đó qua công cụ quản trị.',
     '—',
     '- ⚠️ Các mốc lịch sử vẫn còn để tra cứu; chỉ phiếu và dòng hàng bị xóa.'),
    ('010', 'Xóa phiếu từ màn chi tiết', 'P1',
     'Đang xem chi tiết một phiếu Đang tạo của mình.',
     '1. Bấm nút Xóa ở cuối màn, rồi xác nhận.',
     '—',
     '- Xóa thành công.\n- Điều hướng về màn danh sách.'),
]

S10 = [
    ('001', 'In một phiếu từ cột Hành động', 'P0',
     'Có phiếu trong danh sách.',
     '1. Bấm biểu tượng máy in ở một dòng.',
     '—',
     '- Mở cửa sổ "Xem trước yêu cầu xuất giữ" ngay trên màn đang đứng.\n'
     '- Nội dung đúng phiếu đã chọn.'),
    ('002', 'In một phiếu từ màn chi tiết', 'P1',
     'Đang xem chi tiết một phiếu.',
     '1. Bấm nút In ở cuối màn.',
     '—',
     '- Mở cửa sổ xem trước đúng phiếu đó.'),
    ('003', 'Bản in có đủ các khối', 'P0',
     'Cửa sổ xem trước đang mở với phiếu đã duyệt.',
     '1. Soát nội dung bản in.',
     '—',
     '- Phần đầu chứng từ (logo, thông tin công ty).\n'
     '- Khối thông tin phiếu: loại yêu cầu, hợp đồng, khách hàng, địa chỉ, người yêu cầu, '
     'phòng ban, giữ đến ngày, trạng thái.\n'
     '- Bảng hàng hóa kèm dòng Tổng cộng.\n'
     '- Bảng thông tin duyệt.\n- Khối ký tên.'),
    ('004', 'Phần đầu bản in lấy theo công ty của PHIẾU', 'P0',
     'Phiếu thuộc công ty 1. Người in thuộc công ty 4 và có quyền xem tổng công ty.',
     '1. In phiếu đó.',
     '—',
     '- ⚠️ Phần đầu bản in là thông tin công ty 1, không phải công ty 4.'),
    ('005', 'Phiếu chưa duyệt thì ô Ngày duyệt trên bản in để TRỐNG', 'P0',
     'Phiếu đang ở "Chờ TP duyệt".',
     '1. In phiếu đó và soát bảng thông tin duyệt.',
     '—',
     '- ⚠️ Ô thời gian duyệt để TRỐNG.\n'
     '- KHÔNG in ngày hôm nay vào chỗ đó.'),
    ('006', 'In danh sách theo bộ lọc đang áp', 'P0',
     'Đang lọc Trạng thái = Đã duyệt, có 30 kết quả, đang ở trang 1 (10 dòng).',
     '1. Bấm nút In ở thanh công cụ.',
     '—',
     '- Mở cửa sổ xem trước bản in danh sách, khổ A4 NGANG.\n'
     '- ⚠️ In đủ 30 dòng, không chỉ 10 dòng của trang đang xem.\n'
     '- Toàn bộ là phiếu Đã duyệt.'),
    ('007', 'In danh sách áp cả ô lọc Số hợp đồng', 'P1',
     'Đang lọc Số hợp đồng = một mã cụ thể.',
     '1. Bấm In ở thanh công cụ.',
     '—',
     '- Bản in chỉ có phiếu gắn hợp đồng đó.'),
    ('008', 'In danh sách không vượt quá phạm vi quyền', 'P0',
     'Tài khoản chỉ xem được phiếu của mình.',
     '1. Bỏ hết bộ lọc rồi bấm In ở thanh công cụ.',
     '—',
     '- ⚠️ Bản in chỉ có phiếu của chính mình.'),
    ('009', 'Xuất Excel mở cửa sổ chọn trường trước', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm nút Xuất Excel.',
     '—',
     '- ⚠️ KHÔNG tải tệp ngay.\n'
     '- Mở cửa sổ "Chọn trường xuất Excel" với 15 trường, mặc định chọn hết.'),
    ('010', 'Cửa sổ chọn trường có đủ 15 trường đúng tên', 'P1',
     'Cửa sổ Chọn trường xuất Excel đang mở.',
     '1. Đếm và đọc tên các trường.',
     '—',
     '- Đủ 15: Mã phiếu, Loại yêu cầu, Người tạo, Ngày tạo, Hợp đồng, Khách hàng, Giữ đến ngày, '
     'Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, '
     'Lý do từ chối.\n'
     '- Có dòng ghi "Đang chọn 15/15 trường".'),
    ('011', 'Bỏ chọn trường thì tệp không có cột đó', 'P0',
     'Cửa sổ Chọn trường đang mở.',
     '1. Bỏ chọn Ghi chú và Lý do từ chối.\n2. Bấm Xuất file.\n3. Mở tệp tải về.',
     '—',
     '- Tệp có 13 cột, không có hai cột đã bỏ.'),
    ('012', 'Thứ tự cột trong tệp theo đúng thứ tự chọn', 'P1',
     'Cửa sổ Chọn trường đang mở.',
     '1. Bấm Bỏ chọn hết.\n2. Chọn lần lượt: Trạng thái, Mã phiếu, Khách hàng.\n'
     '3. Bấm Xuất file và mở tệp.',
     '—',
     '- Dòng xem trước trong cửa sổ ghi đúng thứ tự Trạng thái, Mã phiếu, Khách hàng.\n'
     '- Tệp có 3 cột đúng thứ tự đó.'),
    ('013', 'Tệp Excel xuất đủ dòng theo bộ lọc, không chỉ trang đang xem', 'P0',
     'Đang lọc ra 45 kết quả, để 10 dòng/trang.',
     '1. Xuất Excel với toàn bộ trường.\n2. Đếm số dòng dữ liệu trong tệp.',
     '—',
     '- ⚠️ Tệp có đủ 45 dòng dữ liệu.'),
    ('014', 'Mã phiếu trong tệp không bị Excel hiểu thành số', 'P1',
     'Đã xuất tệp Excel.',
     '1. Mở tệp và soát cột Mã phiếu.',
     '—',
     '- Mã hiển thị nguyên vẹn dạng PYCXG-02219.\n'
     '- Không có cảnh báo "Number stored as text" gây khó chịu.'),
    ('015', 'Ngày trong tệp giữ định dạng dd/mm/yyyy', 'P1',
     'Đã xuất tệp Excel.',
     '1. Soát các cột ngày.',
     '—',
     '- Ngày hiển thị dạng dd/mm/yyyy, không bị đổi theo định dạng máy.'),
    ('016', 'Nút Xuất file bị khóa trong lúc đang xuất', 'P2',
     'Đang xuất một tệp lớn.',
     '1. Bấm Xuất file rồi bấm lại ngay.',
     '—',
     '- Nút bị khóa trong lúc xử lý.\n- Chỉ tải về một tệp.'),
    ('017', 'Bấm Đóng ở cửa sổ chọn trường thì không xuất', 'P2',
     'Cửa sổ Chọn trường đang mở.',
     '1. Bấm Đóng.',
     '—',
     '- Cửa sổ đóng, không tải tệp nào về.'),
    ('018', 'Tệp Excel không vượt quá phạm vi quyền', 'P0',
     'Tài khoản chỉ xem được phiếu của mình.',
     '1. Bỏ hết bộ lọc rồi xuất Excel.',
     '—',
     '- ⚠️ Tệp chỉ có phiếu của chính mình.'),
]

S11 = [
    ('001', 'Bỏ trống Loại yêu cầu', 'P0',
     'Đang ở màn Tạo mới.',
     '1. Không chọn gì, bấm Lưu nháp.',
     '—',
     '- Báo đỏ dưới ô Loại yêu cầu: "Bắt buộc phải chọn".\n- Không lưu.'),
    ('002', 'Bỏ trống Hợp đồng ở loại có hợp đồng', 'P0',
     'Đã chọn loại Xuất giữ HĐ hãng.',
     '1. Bấm Lưu nháp mà chưa chọn hợp đồng.',
     '—',
     '- Báo đỏ dưới ô Hợp đồng: "Bắt buộc phải chọn".\n- Không lưu.'),
    ('003', 'Bỏ trống Khách hàng ở loại Xuất giữ khác', 'P0',
     'Đã chọn loại Xuất giữ khác, đã thêm hàng.',
     '1. Bấm Lưu nháp mà chưa chọn khách hàng.',
     '—',
     '- Báo đỏ dưới ô Khách hàng: "Bắt buộc phải chọn".\n- Không lưu.'),
    ('004', 'Bỏ trống Ghi chú ở loại Xuất giữ khác', 'P0',
     'Đã chọn loại Xuất giữ khác, đã chọn khách hàng và thêm hàng.',
     '1. Để trống Ghi chú, bấm Lưu nháp.',
     '—',
     '- Báo đỏ dưới ô Ghi chú: "Bắt buộc phải nhập".\n- Không lưu.'),
    ('005', 'Bỏ trống tệp đính kèm ở loại Xuất giữ khác', 'P0',
     'Đã chọn loại Xuất giữ khác, đã điền đủ các ô khác.',
     '1. Bấm Lưu nháp mà không đính kèm tệp nào.',
     '—',
     '- Báo đỏ ở khối File đính kèm: "Bắt buộc phải chọn".\n- Không lưu.'),
    ('006', 'Loại có hợp đồng KHÔNG bắt buộc tệp và ghi chú', 'P1',
     'Đã chọn loại Xuất giữ HĐ hãng, điền đủ ô bắt buộc, không đính kèm tệp, bỏ trống ghi chú.',
     '1. Bấm Lưu nháp.',
     '—',
     '- Lưu THÀNH CÔNG.\n'
     '- ⚠️ Ba ràng buộc thêm chỉ áp cho loại Xuất giữ khác.'),
    ('007', 'Bỏ trống Giữ đến ngày', 'P0',
     'Đã điền đủ các ô khác.',
     '1. Để trống Giữ đến ngày, bấm Lưu nháp.',
     '—',
     '- Báo "Giữ đến ngày – Bắt buộc phải nhập."\n- Không lưu.'),
    ('008', 'Giữ đến ngày là ngày hôm nay', 'P1',
     'Đang ở màn Tạo mới.',
     '1. Chọn Giữ đến ngày = hôm nay, bấm Lưu nháp.',
     'ngày hôm nay',
     '- Bị chặn: "Giữ đến ngày – Phải nhập ngày tương lai."\n'
     '- Lịch cũng đã chặn sẵn không cho chọn.'),
    ('009', 'Chưa thêm hàng hóa nào', 'P0',
     'Đã chọn loại Xuất giữ khác, chưa thêm dòng nào.',
     '1. Bấm Lưu nháp.',
     '—',
     '- Báo "Bắt buộc phải chọn hàng hoá cần giữ."\n- Không lưu.'),
    ('010', 'Có hàng nhưng không tích dòng nào', 'P0',
     'Loại có hợp đồng, bảng có 5 dòng, không tích dòng nào.',
     '1. Bấm Lưu nháp.',
     '—',
     '- Báo "Chưa chọn hàng hoá nào cần giữ, hoặc số lượng đề nghị đều bằng 0."\n- Không lưu.'),
    ('011', 'Tích dòng nhưng bỏ trống số lượng', 'P0',
     'Đã tích 1 dòng, ô Đề nghị để trống.',
     '1. Bấm Lưu nháp.',
     '—',
     '- Báo đỏ tại dòng đó: "Phải lớn hơn 0."\n- Không lưu.'),
    ('012', 'Tích dòng và nhập số lượng bằng 0', 'P0',
     'Đã tích 1 dòng, nhập 0.',
     '1. Bấm Lưu nháp.',
     '0',
     '- Báo đỏ tại dòng: "Phải lớn hơn 0."\n- Không lưu.'),
    ('013', 'Nhập số lượng âm', 'P1',
     'Đã tích 1 dòng.',
     '1. Gõ -5 vào ô Đề nghị.',
     '-5',
     '- Ô không nhận dấu trừ, chỉ còn 5.\n- Hoặc bị chặn khi lưu với thông báo phải lớn hơn 0.'),
    ('014', 'Nhập chữ vào ô số lượng', 'P1',
     'Đã tích 1 dòng.',
     '1. Gõ "abc" vào ô Đề nghị.',
     'abc',
     '- Ô không nhận ký tự chữ, giữ nguyên trống.'),
    ('015', 'Số lượng quá 6 chữ số', 'P1',
     'Đã tích 1 dòng, tồn kho rất lớn.',
     '1. Nhập 1234567 rồi bấm Gửi duyệt.',
     '1234567',
     '- Báo "Không được vượt quá 6 chữ số".\n- Không lưu.'),
    ('016', 'Số lượng vượt phần còn lại của hợp đồng', 'P0',
     'Dòng hàng có SL hợp đồng = 10, Đã xuất kho = 7 (còn 3). Tồn kho dư dả.',
     '1. Nhập 5 vào ô Đề nghị, bấm Lưu nháp.',
     '5',
     '- ⚠️ Bị chặn ngay ở bước Lưu nháp: "Vượt số lượng còn lại của hợp đồng (còn 3)."\n'
     '- Giá trị 5 vẫn nguyên trong ô.'),
    ('017', 'Số lượng bằng đúng phần còn lại của hợp đồng', 'P1',
     'Cùng dữ liệu TC 016 (còn 3).',
     '1. Nhập 3 rồi Lưu nháp.',
     '3',
     '- Lưu thành công, không báo lỗi.'),
    ('018', 'Hợp đồng nguyên tắc bỏ qua ràng buộc số lượng', 'P1',
     'Hợp đồng thuộc loại "nguyên tắc"; phần còn lại là 0.',
     '1. Nhập 100 vào ô Đề nghị, bấm Lưu nháp.',
     '100',
     '- ⚠️ KHÔNG bị chặn theo hợp đồng.\n'
     '- Chỉ còn ràng buộc tồn kho ở bước Gửi duyệt.'),
    ('019', 'Hàng không nằm trong hợp đồng (sai đơn vị tính)', 'P1',
     'Tester kỹ thuật gửi dòng hàng với đơn vị tính khác đơn vị ghi trên hợp đồng.',
     '1. Gọi thẳng chức năng lưu phiếu.',
     '—',
     '- Bị chặn: "Hàng hoá không có trong hợp đồng."\n'
     '- ⚠️ Hệ thống so theo cặp hàng hóa + đơn vị tính, không chỉ theo hàng hóa.'),
    ('020', 'Loại Xuất giữ khác không bị ràng buộc theo hợp đồng', 'P1',
     'Loại Xuất giữ khác, tồn kho dư dả.',
     '1. Nhập số lượng lớn tùy ý rồi Lưu nháp.',
     '500',
     '- Lưu thành công, không có thông báo về hợp đồng.'),
    ('021', 'Loại Xuất giữ khác bỏ trống ĐVT', 'P0',
     'Loại Xuất giữ khác, đã thêm 1 dòng hàng.',
     '1. Xóa trắng ô ĐVT rồi bấm Lưu nháp.',
     '—',
     '- Báo đỏ tại dòng: "Bắt buộc phải chọn đơn vị tính".\n- Không lưu.'),
    ('022', 'Ghi chú quá 255 ký tự', 'P1',
     'Đang ở màn Tạo mới.',
     '1. Nhập 300 ký tự vào ô Ghi chú rồi Lưu nháp.',
     'chuỗi 300 ký tự',
     '- Ô chặn ở 255 ký tự khi gõ, hoặc báo "Không được vượt quá 255 ký tự" khi lưu.'),
    ('023', 'Tệp đính kèm vượt 13 MB', 'P1',
     'Có tệp PDF 20 MB.',
     '1. Chọn tệp đó ở khối File đính kèm.',
     'tệp 20 MB',
     '- Bị từ chối, báo tệp vượt dung lượng cho phép.\n- Không tải lên.'),
    ('024', 'Tệp đính kèm sai định dạng', 'P1',
     'Có tệp .exe.',
     '1. Chọn tệp đó.',
     'tệp .exe',
     '- Bị từ chối; chỉ nhận PDF, ảnh, Word, Excel.'),
    ('025', 'Nhiều lỗi cùng lúc thì báo hết cùng lúc', 'P1',
     'Loại Xuất giữ khác: bỏ trống Khách hàng, Ghi chú và tệp đính kèm.',
     '1. Bấm Lưu nháp.',
     '—',
     '- Cả ba ô đều báo đỏ cùng lúc.\n'
     '- ⚠️ Không phải sửa từng lỗi rồi bấm lại mới thấy lỗi tiếp theo.'),
    ('026', 'Giá trị nhập sai KHÔNG bị tự sửa', 'P0',
     'Nhập số lượng vượt trần cho phép.',
     '1. Bấm Lưu và quan sát ô vừa nhập.',
     '—',
     '- ⚠️ Giá trị người dùng gõ vẫn nguyên trong ô.\n'
     '- Phần mềm chỉ báo đỏ, không tự kéo về mức trần.'),
]

S12 = [
    ('001', 'Hai người cùng duyệt một phiếu', 'P0',
     'Người 1 và người 2 cùng có quyền Trưởng phòng, cùng mở một phiếu Chờ TP duyệt.',
     '1. Người 1 bấm TP duyệt và xác nhận.\n'
     '2. Người 2 bấm TP duyệt trên màn đang mở (chưa tải lại).',
     '—',
     '- Người 1 thành công.\n'
     '- ⚠️ Người 2 bị chặn: "Phiếu không ở trạng thái chờ duyệt."\n'
     '- Phiếu chỉ đi 1 bước, không nhảy 2 bước.'),
    ('002', 'Một người duyệt, một người từ chối cùng lúc', 'P0',
     'Hai người cùng có quyền, cùng mở một phiếu Chờ BGĐ duyệt.',
     '1. Người 1 bấm BGĐ duyệt và xác nhận.\n2. Người 2 bấm Từ chối, nhập lý do, xác nhận.',
     '—',
     '- Người 1 thành công, phiếu sang Chờ KT duyệt.\n'
     '- Người 2 bị chặn: "Bạn không có quyền từ chối phiếu này."'),
    ('003', 'Người lập sửa phiếu trong lúc Trưởng phòng đang xem', 'P1',
     'Phiếu bị trả về, đang ở Đang tạo. Trưởng phòng vẫn mở màn chi tiết cũ.',
     '1. Người lập sửa và Gửi duyệt.\n2. Trưởng phòng bấm TP duyệt trên màn cũ.',
     '—',
     '- Trưởng phòng duyệt được (phiếu đúng đang ở Chờ TP duyệt).\n'
     '- ⚠️ Số liệu ghi nhận là số ĐÃ SỬA, không phải số Trưởng phòng đang nhìn.\n'
     '- Khuyến nghị: tải lại màn trước khi duyệt.'),
    ('004', 'Người lập xóa phiếu trong lúc người khác đang xem', 'P1',
     'Người lập xóa phiếu nháp. Người có quyền quản trị đang mở màn chi tiết phiếu đó.',
     '1. Người quản trị bấm Quay lại rồi mở lại phiếu.',
     '—',
     '- Hệ thống báo không tìm thấy phiếu.\n- Không hiện màn trắng hay lỗi kỹ thuật.'),
    ('005', 'Hai người cùng lập phiếu xuất giữ cho một yêu cầu', 'P0',
     'Hai Kế toán cùng mở một yêu cầu Chờ KT duyệt.',
     '1. Kế toán 1 lập và lưu nháp phiếu xuất giữ.\n'
     '2. Kế toán 2 bấm Lập phiếu xuất giữ trên màn cũ và lưu.',
     '—',
     '- Kế toán 1 thành công.\n'
     '- ⚠️ Kế toán 2 bị chặn: "Yêu cầu này đã có phiếu xuất giữ …".'),
    ('006', 'Phiếu của công ty khác không rò rỉ qua ô lọc', 'P0',
     'Tài khoản chỉ có quyền xem theo công ty 1.',
     '1. Lọc theo nhiều tiêu chí khác nhau, kể cả Tên mã hàng và Số hợp đồng.\n'
     '2. Bật cột Phòng ban và soát toàn bộ kết quả.',
     '—',
     '- ⚠️ Không dòng nào thuộc công ty khác, ở mọi tổ hợp bộ lọc.'),
    ('007', 'Ô lọc Tên mã hàng không làm lộ phiếu ngoài phạm vi', 'P0',
     'Hàng HH01 có mặt ở phiếu của nhiều công ty. Tài khoản chỉ xem được công ty 1.',
     '1. Lọc Tên mã hàng = HH01.',
     '—',
     '- ⚠️ Chỉ ra phiếu của công ty 1.\n'
     '- Đây là trường hợp dễ rò rỉ nhất, cần kiểm kỹ.'),
    ('008', 'Ô lọc Số hợp đồng không làm lộ phiếu ngoài phạm vi', 'P0',
     'Một hợp đồng có phiếu ở hai công ty. Tài khoản chỉ xem được công ty 1.',
     '1. Lọc Số hợp đồng = mã hợp đồng đó.',
     '—',
     '- ⚠️ Chỉ ra phiếu của công ty 1.'),
    ('009', 'Đổi quyền của người dùng thì phạm vi đổi theo ngay', 'P1',
     'Tài khoản A đang chỉ xem được phiếu của mình.',
     '1. Quản trị cấp thêm quyền "Xem phiếu hàng giữ theo công ty" cho A.\n'
     '2. A đăng xuất, đăng nhập lại và mở màn hình.',
     '—',
     '- N tăng lên đúng số phiếu của công ty A.\n- Ô lọc Phòng ban xuất hiện.'),
]

S13 = [
    ('001', 'Xem lịch sử từ cột Hành động', 'P0',
     'Có phiếu đã qua vài thao tác.',
     '1. Bấm biểu tượng đồng hồ ở cột Hành động.',
     '—',
     '- Mở cửa sổ Lịch sử thay đổi của đúng phiếu đó.\n'
     '- Các mốc xếp mới nhất trước.'),
    ('002', 'Xem lịch sử từ màn chi tiết', 'P0',
     'Đang xem chi tiết một phiếu.',
     '1. Cuộn xuống khối Lịch sử thay đổi.\n2. Bấm nút Xem lịch sử.',
     '—',
     '- Khối mở ra, hiện danh sách mốc thay đổi.\n'
     '- Tiêu đề khối hiện thêm số mốc.\n- Nút đổi nhãn thành "Thu gọn".'),
    ('003', 'Khối lịch sử chỉ nạp dữ liệu khi bấm mở', 'P1',
     'Mở màn chi tiết một phiếu.',
     '1. Quan sát khối Lịch sử thay đổi ngay khi vào màn.',
     '—',
     '- ⚠️ Khối ở trạng thái thu gọn, chưa nạp dữ liệu.\n'
     '- Chỉ bấm Xem lịch sử mới nạp.'),
    ('004', 'Mốc Tạo mới ghi đủ thông tin ban đầu', 'P0',
     'Vừa lập một phiếu mới.',
     '1. Mở lịch sử của phiếu đó.',
     '—',
     '- Có mốc "Tạo phiếu" ghi người thực hiện, thời điểm.\n'
     '- Liệt kê giá trị ban đầu: loại yêu cầu, khách hàng, giữ đến ngày, trạng thái và các dòng '
     'hàng.'),
    ('005', 'Mốc Chỉnh sửa nêu rõ giá trị cũ và mới', 'P0',
     'Sửa số lượng của một dòng từ 2 thành 5 rồi lưu.',
     '1. Mở lịch sử của phiếu.',
     '—',
     '- Có mốc "Chỉnh sửa" ghi rõ dòng hàng nào, từ 2 đổi thành 5.\n'
     '- ⚠️ Không chỉ ghi "đã sửa" chung chung.'),
    ('006', 'Mốc Duyệt ghi rõ cấp duyệt', 'P0',
     'Phiếu đã qua Trưởng phòng và Ban giám đốc.',
     '1. Mở lịch sử của phiếu.',
     '—',
     '- Có mốc duyệt cho từng cấp, ghi rõ người thực hiện và trạng thái trước → sau.'),
    ('007', 'Mốc Từ chối ghi rõ lý do', 'P0',
     'Phiếu vừa bị từ chối với lý do cụ thể.',
     '1. Mở lịch sử của phiếu.',
     '—',
     '- Có mốc từ chối ghi đúng nội dung lý do.\n'
     '- Ghi trạng thái đổi từ Chờ … về Đang tạo.'),
    ('008', 'Mốc duyệt qua Phiếu xuất giữ ghi rõ mã phiếu con', 'P0',
     'Phiếu vừa được duyệt xong qua Phiếu xuất giữ PXG-XXXXX.',
     '1. Mở lịch sử của yêu cầu.',
     '—',
     '- ⚠️ Mốc cuối ghi rõ "Duyệt qua phiếu xuất giữ PXG-XXXXX".'),
    ('009', 'Phiếu cũ chưa có lịch sử hiện đúng câu thông báo', 'P1',
     'Phiếu lập từ trước khi bật tính năng ghi lịch sử.',
     '1. Mở lịch sử của phiếu đó.',
     '—',
     '- Hiện dòng "Chưa có lịch sử thao tác nào."\n- Không báo lỗi.'),
    ('010', 'Nút Làm mới nạp lại lịch sử', 'P2',
     'Khối lịch sử đang mở. Người khác vừa duyệt phiếu ở tab khác.',
     '1. Bấm nút Làm mới.',
     '—',
     '- Danh sách mốc được nạp lại, có thêm mốc mới nhất.'),
    ('011', 'Thứ tự lịch sử là mới nhất trước', 'P1',
     'Phiếu có ít nhất 4 mốc.',
     '1. Đọc thời điểm của từng mốc từ trên xuống.',
     '—',
     '- Thời điểm giảm dần từ trên xuống.'),
]

S14 = [
    ('001', 'Luồng đầy đủ: lập → TP duyệt → KT lập phiếu → duyệt giữ hàng', 'P0',
     'Nhân viên A thuộc phòng P1, hợp đồng đã thu đủ tiền (không phải qua Ban giám đốc). '
     'Hàng HH01 tồn kho 100, A chưa giữ lô nào của HH01.',
     '1. A lập yêu cầu, tích HH01 số lượng 10, Giữ đến ngày 30/10/2026, bấm Gửi duyệt.\n'
     '2. Trưởng phòng P1 duyệt.\n'
     '3. Kế toán mở phiếu, bấm Lập phiếu xuất giữ, giữ nguyên số lượng, bấm Duyệt giữ hàng.\n'
     '4. Mở màn Danh sách hàng giữ, lọc theo A.',
     '—',
     '- Sau bước 1: phiếu ở "Chờ TP duyệt".\n'
     '- Sau bước 2: thông báo "Yêu cầu đã được chuyển đến Kế toán.", phiếu ở "Chờ KT duyệt".\n'
     '- Sau bước 3: phiếu ở "Đã duyệt", cột Người duyệt là Kế toán.\n'
     '- Sau bước 4: ⚠️ A có lô hàng giữ HH01 số lượng 10, hạn 30/10/2026.'),
    ('002', 'Luồng có Ban giám đốc: lập → TP → BGĐ đổi hạn → KT', 'P0',
     'Hợp đồng chưa thu đủ tiền, phải trình Ban giám đốc.',
     '1. A lập yêu cầu với Giữ đến ngày 30/10/2026, gửi duyệt.\n'
     '2. Trưởng phòng duyệt.\n'
     '3. Ban giám đốc đổi Giữ đến ngày thành 15/10/2026 rồi duyệt.\n'
     '4. Kế toán lập phiếu xuất giữ và duyệt giữ hàng.\n'
     '5. Kiểm tra lô hàng giữ.',
     '—',
     '- Sau bước 2: "Yêu cầu đã được chuyển đến Ban giám đốc.", phiếu ở "Chờ BGĐ duyệt".\n'
     '- Sau bước 3: phiếu ở "Chờ KT duyệt", hạn giữ trên phiếu là 15/10/2026.\n'
     '- Sau bước 5: ⚠️ Lô hàng giữ có hạn 15/10/2026 — theo Ban giám đốc, không phải 30/10.'),
    ('003', 'Luồng bị từ chối rồi sửa và gửi lại', 'P0',
     'Phiếu đang ở Chờ TP duyệt.',
     '1. Trưởng phòng từ chối với lý do.\n'
     '2. Người lập mở phiếu ra Sửa, đọc lý do, đổi số lượng từ 10 xuống 5, bấm Gửi duyệt.\n'
     '3. Trưởng phòng duyệt.\n4. Kế toán lập phiếu và duyệt giữ hàng.',
     '—',
     '- Sau bước 1: phiếu về "Đang tạo", cột Lý do từ chối có nội dung.\n'
     '- Sau bước 2: phiếu ở "Chờ TP duyệt", ⚠️ dấu duyệt của cả ba cấp bị đặt lại, ô Lý do từ '
     'chối bị xóa.\n'
     '- Sau bước 4: lô hàng giữ có số lượng 5 — theo số ĐÃ SỬA.'),
    ('004', 'Luồng lập nháp rồi xóa', 'P1',
     'Chưa có phiếu nào.',
     '1. Lập phiếu và Lưu nháp.\n2. Xóa phiếu.\n3. Kiểm tra tồn hàng giữ.',
     '—',
     '- Phiếu biến mất khỏi danh sách.\n'
     '- ⚠️ Tồn hàng giữ hoàn toàn không đổi vì yêu cầu chưa từng ghi tồn.'),
    ('005', 'Luồng Kế toán lập nháp rồi xóa phiếu con', 'P0',
     'Yêu cầu đang ở Chờ KT duyệt.',
     '1. Kế toán lập phiếu xuất giữ và Lưu nháp.\n'
     '2. Kiểm tra trạng thái yêu cầu.\n'
     '3. Kế toán xóa phiếu xuất giữ.\n4. Kiểm tra lại trạng thái yêu cầu.',
     '—',
     '- Sau bước 2: yêu cầu ở "Đang xuất giữ".\n'
     '- Sau bước 4: ⚠️ yêu cầu quay về "Chờ KT duyệt", nút Lập phiếu xuất giữ hiện lại.\n'
     '- Tồn hàng giữ không đổi suốt quá trình.'),
    ('006', 'Luồng loại Xuất giữ khác từ đầu tới cuối', 'P0',
     'Nhân viên A muốn giữ hàng không gắn hợp đồng.',
     '1. A lập yêu cầu loại Xuất giữ khác: chọn khách hàng, thêm 2 dòng hàng, chọn ĐVT, nhập số '
     'lượng, nhập Ghi chú, đính kèm 1 tệp, bấm Gửi duyệt.\n'
     '2. Trưởng phòng duyệt.\n3. Kế toán lập phiếu xuất giữ và duyệt giữ hàng.\n'
     '4. Kiểm tra lô hàng giữ.',
     '—',
     '- Sau bước 1: phiếu ở "Chờ TP duyệt", cột Hợp đồng để TRỐNG.\n'
     '- Sau bước 3: phiếu ở "Đã duyệt".\n'
     '- Sau bước 4: A có 2 lô hàng giữ mới, số lượng quy về ĐƠN VỊ CƠ BẢN theo hệ số của ĐVT '
     'đã chọn.'),
    ('007', 'Kiểm tra chéo: hàng giữ vừa sinh ra dùng được ở màn Gia hạn', 'P1',
     'Vừa duyệt xong một yêu cầu, A có lô hàng giữ mới, hạn giữ còn dưới 7 ngày.',
     '1. Đăng nhập bằng A.\n2. Mở màn Yêu cầu gia hạn hàng giữ và bấm Tạo mới.',
     '—',
     '- ⚠️ Lô vừa sinh xuất hiện trong danh sách lô sắp hết hạn của A.\n'
     '- Xác nhận phiếu xuất giữ đã thực sự sinh ra lô hàng giữ dùng chung được.'),
    ('008', 'Kiểm tra chéo: hàng giữ vừa sinh ra dùng được ở màn Hủy hàng giữ', 'P1',
     'A vừa có lô hàng giữ mới.',
     '1. Đăng nhập bằng A.\n2. Mở màn Yêu cầu hủy hàng giữ và bấm Tạo mới, chọn khách hàng '
     'tương ứng.',
     '—',
     '- Lô vừa sinh xuất hiện trong danh sách hàng đang giữ của A.'),
    ('009', 'Tồn kho giảm đúng sau khi duyệt giữ hàng', 'P0',
     'Hàng HH01 có SL có thể giữ = 100 trước khi duyệt.',
     '1. Duyệt một phiếu xuất giữ 10 đơn vị HH01.\n'
     '2. Lập một yêu cầu mới với HH01 và đọc cột Có thể giữ.',
     '—',
     '- ⚠️ Cột Có thể giữ giảm còn 90.\n'
     '- Hàng đã giữ không còn nằm trong phần khả dụng để giữ tiếp.'),
    ('010', 'Hai yêu cầu cùng giữ một hàng, cái sau bị chặn vì hết tồn', 'P0',
     'Hàng HH02 chỉ còn 5 trong kho. Hai nhân viên cùng lập yêu cầu xin giữ 5.',
     '1. Yêu cầu 1 đi hết luồng và được duyệt giữ hàng.\n'
     '2. Yêu cầu 2 tới bước Kế toán, bấm Duyệt giữ hàng.',
     '—',
     '- Bước 1 thành công.\n'
     '- ⚠️ Bước 2 bị chặn: "Kho không đủ số lượng (còn 0)."\n'
     '- Kế toán phải giảm số lượng hoặc từ chối yêu cầu.'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP PHIẾU (TẠO MỚI)', S4),
    ('V', 'SỬA PHIẾU', S5),
    ('VI', 'XEM CHI TIẾT', S6),
    ('VII', 'DUYỆT & TỪ CHỐI', S7),
    ('VIII', 'BƯỚC KẾ TOÁN — LẬP PHIẾU XUẤT GIỮ', S8),
    ('IX', 'XÓA PHIẾU', S9),
    ('X', 'IN & XUẤT EXCEL', S10),
    ('XI', 'RÀNG BUỘC NHẬP LIỆU', S11),
    ('XII', 'CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI', S12),
    ('XIII', 'LỊCH SỬ THAY ĐỔI', S13),
    ('XIV', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S14),
]

build(output_file=os.path.join(BASE, 'testcase_yeu_cau_xuat_giu.xlsx'),
      sheet_name='Trang tính1',
      feature_name='Yêu cầu xuất giữ',
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
