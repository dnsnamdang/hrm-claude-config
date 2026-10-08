# -*- coding: utf-8 -*-
"""Sinh "testcase - Hang sap het han giu.xlsx" (phan he Tai chinh, nhom Giu hang).

Man CHI DOC, anh em cua "Danh sach hang giu". Viet tu code HRM nhanh `gop_db` + anh chup that
tren dev ngay 05/10/2026. Ngon ngu: NGHIEP VU cho QA — khong thuat ngu code, khong emoji/mui ten.
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

MODULE = 'Hàng sắp hết hạn giữ'
MENU = 'Vào phân hệ Tài chính > nhóm "Giữ hàng" > bấm "Hàng sắp hết hạn giữ"'
NA = '—'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn hình Hàng sắp hết hạn giữ là báo cáo tra cứu CHỈ ĐỌC: liệt kê hàng hóa có lô hàng giữ '
     'đã hoặc vừa hết hạn giữ trong N ngày gần đây (N = số ngày cảnh báo cấu hình chung, hiện là '
     '7), để nhắc nhân viên kinh doanh gia hạn hoặc trả hàng.\n'
     'Không có thao tác thêm, sửa, xóa; không làm thay đổi số hàng giữ.\n'
     'Đường dẫn: Phân hệ Tài chính > Giữ hàng > Hàng sắp hết hạn giữ.'),
    ('2. Đối tượng được tính / hiển thị',
     'Lô hàng giữ có số lượng lớn hơn 0 VÀ hạn giữ nằm trong khoảng từ (hôm nay trừ N ngày) đến '
     'hôm nay, tính cả hai đầu.\n'
     'Ví dụ hôm nay 05/10/2026, N = 7: lấy lô có hạn giữ từ 28/09/2026 đến 05/10/2026.\n'
     'Trạng thái của lô tính tại lúc xem: hạn giữ trước hôm nay là "Hết hạn" (đỏ), đúng hôm nay '
     'là "Đến hạn" (vàng).\n'
     'Dữ liệu bó theo phạm vi quyền xem của người đăng nhập (xem mục 7).'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Lô có hạn giữ SAU hôm nay (còn hạn): KHÔNG hiện, kể cả lô hết hạn ngày mai.\n'
     '- Lô có hạn giữ trước (hôm nay trừ N ngày): KHÔNG hiện, ví dụ hạn 27/09/2026 khi hôm nay '
     '05/10/2026.\n'
     '- Lô đã hết số lượng giữ (bằng 0): không hiện.\n'
     '- Lô ngoài phạm vi quyền xem: không hiện ở bảng, chi tiết, Excel, bản in.\n'
     '- Kho kế toán Chờ xóa hoặc ngừng dùng: không có trong ô Lọc theo kho.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Màn hình KHÔNG có ô chọn khoảng ngày. Mốc thời gian duy nhất là cửa sổ ngày cố định theo '
     'HẠN GIỮ của lô: [hôm nay trừ N ngày, hôm nay]. Cửa sổ này luôn được áp, kể cả sau khi bấm '
     'Làm mới, và áp cho cả bảng, chi tiết, Excel, bản in.\n'
     'Riêng cửa sổ Lịch sử giữ hàng KHÔNG bó theo cửa sổ ngày.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Bảng 3 tầng:\n'
     '- Tầng 1 = hàng hóa (được phân trang, có STT dạng nút mở rộng).\n'
     '- Tầng 2 = nhân viên đang giữ hàng hóa đó (tên, phòng ban, tổng SL giữ).\n'
     '- Tầng 3 = lô theo khách hàng (mã - tên khách hàng, SL giữ, Hạn giữ, Trạng thái, nút Lịch '
     'sử giữ hàng).\n'
     'Excel: bảng phẳng, mỗi dòng một lô. Bản in: gom Phòng ban > Nhân viên > lô.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     'SL giữ tầng 1 = tổng SL các lô TRONG CỬA SỔ NGÀY của hàng hóa (không phải toàn bộ hàng đang '
     'giữ).\n'
     'SL giữ tầng 2 = tổng các lô của nhân viên; tổng các dòng tầng 2 = SL giữ tầng 1.\n'
     'Tổng SL trong kho = tổng tồn kho kế toán của hàng hóa trên mọi kho thuộc công ty trong phạm '
     'vi; KHÔNG đổi theo ô Lọc theo kho.\n'
     'Đổi Đơn vị: số = số theo đơn vị cơ bản chia hệ số, làm tròn XUỐNG 2 chữ số thập phân.'),
    ('7. Phân quyền cấp',
     'Quyền bắt buộc: "Quản lý giữ hàng" (Super Admin được miễn). Thiếu quyền này mọi chức năng '
     'báo "Bạn không có quyền xem danh sách hàng sắp hết hạn giữ".\n'
     'Phạm vi dữ liệu (lấy cấp cao nhất):\n'
     '- "Xem phiếu hàng giữ theo tổng công ty": mọi công ty, có thêm ô lọc Công ty.\n'
     '- "Xem phiếu hàng giữ theo công ty": công ty đang đăng nhập.\n'
     '- "Xem phiếu hàng giữ theo phòng ban": nhân viên thuộc phòng ban mình quản lý và phòng mình, '
     'cộng chính mình.\n'
     '- Không có quyền xem theo cấp nào: chỉ lô do chính mình đứng tên giữ.'),
    ('8. Cách tính các ô thống kê',
     'Ô "Hiển thị a-b / N": N là tổng số HÀNG HÓA (tầng 1) khớp bộ lọc, không phải số lô.\n'
     'Bản in: Số phòng ban, Số nhân viên, Số mục hàng (= số LÔ) của toàn bộ dữ liệu khớp bộ lọc.\n'
     'Cửa sổ chọn trường Excel: "Đang chọn x/12 trường".\n'
     'Cửa sổ Lịch sử: "Số lượng giữ hiện tại: x ĐVT."'),
    ('9. Ghi chú đọc bảng',
     'BẪY DỄ SAI NHẤT của màn này:\n'
     '- Tên màn là "sắp hết hạn" nhưng màn hình liệt kê hàng ĐÃ / VỪA hết hạn trong N ngày gần '
     'đây. Đây là quyết định giữ nguyên hệ thống cũ, KHÔNG ghi Failed vì "không thấy hàng còn '
     'hạn".\n'
     '- Cột Trạng thái KHÔNG BAO GIỜ ra "Trong hạn"; ô lọc Trạng thái chỉ có Hết hạn và Đến hạn. '
     'Đúng thiết kế.\n'
     '- Hạn giữ và Trạng thái chỉ có ở dòng khách hàng (tầng 3); tầng 1, 2 để trống là đúng.\n'
     '- Ô Lọc theo kho không làm đổi số Tổng SL trong kho.\n'
     '- Danh sách lựa chọn Nhân viên / Thương hiệu / Model có thể chứa giá trị cho ra bảng rỗng.\n'
     '- Biểu tượng ổ khóa cạnh ô Công ty, Phòng ban là công tắc "Hiện cả ... đã khoá", không phải '
     'ô bị khóa.\n'
     '- Số theo chuẩn quốc tế: 1,234.5; ngày dd/mm/yyyy.\n'
     '- Nhóm TC gọi thẳng chức năng bằng công cụ kiểm thử API dành cho tester kỹ thuật.'),
]

ROLE_TCS = [
    ('01', 'Tài khoản thiếu quyền "Quản lý giữ hàng" bị từ chối', 'P0',
     'Tài khoản A không có quyền Quản lý giữ hàng, có quyền "Xem phiếu hàng giữ theo công ty".\n'
     'Công ty của A có 120 hàng hóa trong cửa sổ ngày.',
     '1. Đăng nhập bằng A.\n2. ' + MENU + '.\n3. Quan sát bảng và thông báo.',
     NA,
     '- Mục menu vẫn hiển thị và mở được trang.\n'
     '- Phần mềm báo "Bạn không có quyền xem danh sách hàng sắp hết hạn giữ".\n'
     '- Bảng không có dòng dữ liệu nào.\n'
     '- Lưu ý: có quyền xem theo công ty nhưng thiếu Quản lý giữ hàng vẫn bị từ chối.'),
    ('02', 'Thiếu quyền thì In và Xuất Excel cũng bị từ chối', 'P0',
     'Tài khoản A như TC-ROLE-01.',
     '1. Đăng nhập bằng A, mở màn.\n2. Bấm In.\n3. Bấm Xuất Excel rồi bấm Xuất file.',
     NA,
     '- Bước 2: cửa sổ xem trước báo không có quyền, không có bản in.\n'
     '- Bước 3: phần mềm báo "Bạn không có quyền xem danh sách hàng sắp hết hạn giữ", không tải '
     'tệp nào.'),
    ('03', 'Chỉ có "Quản lý giữ hàng": chỉ thấy lô của chính mình', 'P0',
     'Tài khoản B có Quản lý giữ hàng, không có quyền xem theo cấp nào.\n'
     'B đứng tên 3 lô trong cửa sổ ngày thuộc 2 hàng hóa; đồng nghiệp cùng phòng có 10 lô.',
     '1. Đăng nhập bằng B, mở màn.\n2. Đọc ô "Hiển thị a-b / N".\n3. Mở rộng cả 2 hàng hóa.\n'
     '4. Mở ô lọc Nhân viên.',
     NA,
     '- N = 2.\n'
     '- Mọi dòng nhân viên đều là B; tổng 3 dòng khách hàng.\n'
     '- Ô lọc Nhân viên chỉ có tên B.\n'
     '- Không có ô lọc Công ty.'),
    ('04', 'Quyền "Xem phiếu hàng giữ theo phòng ban"', 'P0',
     'Tài khoản C có Quản lý giữ hàng + xem theo phòng ban, được giao quản lý phòng P1; C thuộc '
     'phòng P2.\n'
     'Trong cửa sổ ngày: P1 có 8 lô, P2 có 5 lô (gồm 1 lô của C), phòng P3 có 6 lô.',
     '1. Đăng nhập bằng C, mở màn.\n2. Bấm In, đọc Số mục hàng.\n3. Xuất Excel đủ trường, đếm số '
     'dòng dữ liệu.',
     NA,
     '- Bản in: Số mục hàng = 13 (8 lô P1 + 5 lô P2).\n'
     '- Tệp Excel có 13 dòng dữ liệu.\n'
     '- Không có lô nào của phòng P3.'),
    ('05', 'Quyền "Xem phiếu hàng giữ theo công ty"', 'P0',
     'Tài khoản D có Quản lý giữ hàng + xem theo công ty, đăng nhập công ty 1.\n'
     'Trong cửa sổ ngày: công ty 1 có 300 hàng hóa, công ty 4 có 40 hàng hóa khác.',
     '1. Đăng nhập bằng D, mở màn.\n2. Đọc N.\n3. Mở khu vực Tìm kiếm nâng cao.\n'
     '4. Mở ô Lọc theo kho.',
     NA,
     '- N = 300.\n'
     '- Không có ô lọc Công ty.\n'
     '- Ô Lọc theo kho chỉ có kho kế toán đang hoạt động của công ty 1.'),
    ('06', 'Quyền "Xem phiếu hàng giữ theo tổng công ty"', 'P0',
     'Tài khoản E có Quản lý giữ hàng + xem theo tổng công ty.\n'
     'Trong cửa sổ ngày: công ty 1 có 300 hàng hóa, công ty 4 có 40 hàng hóa khác.',
     '1. Đăng nhập bằng E, mở màn.\n2. Đọc N.\n3. Mở Tìm kiếm nâng cao, chọn Công ty = công ty 4.',
     'Công ty: công ty 4',
     '- Bước 2: N = 340.\n'
     '- Có ô lọc Công ty.\n'
     '- Bước 3: N = 40, chỉ lô của công ty 4.'),
    ('07', 'Super Admin xem được toàn bộ', 'P1',
     'Tài khoản DNS Admin (Super Admin), không gán quyền nhóm Giữ hàng.',
     '1. Đăng nhập DNS Admin.\n2. Mở màn.\n3. Mở Tìm kiếm nâng cao.',
     NA,
     '- Màn hiện dữ liệu mọi công ty (trên dev 05/10/2026: "Hiển thị 1-10 / 500").\n'
     '- Có ô lọc Công ty.'),
    ('08', 'Gọi thẳng chức năng xem danh sách, bỏ qua giao diện', 'P0',
     'Tài khoản A không có quyền Quản lý giữ hàng.',
     '1. Dùng công cụ kiểm thử API, đăng nhập bằng A.\n'
     '2. Gọi thẳng các chức năng: lấy danh sách, xem chi tiết một hàng hóa, xem lịch sử một lô, '
     'xuất Excel, in.',
     NA,
     '- Cả 5 chức năng đều bị từ chối với thông báo "Bạn không có quyền xem danh sách hàng sắp '
     'hết hạn giữ".\n'
     '- Không trả dữ liệu nào.'),
    ('09', 'Gọi thẳng chức năng không thể bỏ cửa sổ ngày', 'P1',
     'Tài khoản B có Quản lý giữ hàng.\n'
     'Hàng H có 1 lô hạn 20/10/2026 (còn hạn) và không có lô nào trong cửa sổ ngày.',
     '1. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy danh sách, cố tình gửi kèm điều kiện '
     'tắt cửa sổ ngày và mã hàng H.',
     'Mã hàng hóa: mã của H',
     '- Kết quả rỗng: phần mềm luôn tự áp cửa sổ ngày, không phụ thuộc thông tin gửi lên.'),
]

S1 = [
    ('001', 'Mở màn qua menu Tài chính', 'P0',
     'Tài khoản DNS Admin. Ngày 05/10/2026.',
     '1. Đăng nhập.\n2. ' + MENU + '.',
     NA,
     '- Tiêu đề trang và tiêu đề bảng là "Hàng sắp hết hạn giữ".\n'
     '- Khối "Bộ lọc danh sách" có ô tìm nhanh, nút Cài đặt bộ lọc, Tìm kiếm nâng cao, Tìm kiếm, '
     'Làm mới.\n'
     '- Khối bảng có nút In, Xuất Excel, nút cấu hình cột.\n'
     '- Chân bảng "Hiển thị 1-10 / 500", ô "Số dòng/trang" = 10.'),
    ('002', 'Bộ cột mặc định', 'P0',
     'Tài khoản chưa từng tuỳ chỉnh cột ở màn này.',
     '1. Mở màn.\n2. Đọc tiêu đề cột từ trái sang phải (cuộn ngang nếu cần).',
     NA,
     '- Đúng thứ tự: STT, Mã hàng hóa / Nhân viên / Khách hàng, Tên hàng hóa / Phòng ban, Đơn '
     'vị, Model, Thương hiệu, Tổng SL trong kho, SL giữ, Hạn giữ, Trạng thái, Hành động.'),
    ('003', 'Màn hình không có thao tác ghi dữ liệu', 'P0',
     'Màn có dữ liệu.',
     '1. Mở màn.\n2. Rà toàn bộ nút trên thanh công cụ và mọi dòng (kể cả dòng đã mở rộng).',
     NA,
     '- KHÔNG có nút Thêm mới, Import, Sửa, Xóa ở bất kỳ đâu.\n'
     '- Cột Hành động chỉ có nút Lịch sử giữ hàng ở dòng khách hàng.'),
    ('004', 'Mã hàng hóa không phải liên kết', 'P2',
     'Màn có dữ liệu.',
     '1. Bấm vào mã hàng hóa của dòng đầu.',
     NA,
     '- Không mở màn nào; mã hiển thị dạng chữ thường.'),
    ('005', 'Ô rỗng để trống, không in dấu gạch', 'P1',
     'Hàng hóa X không có tồn kho kế toán; hàng hóa Y không có model.',
     '1. Tìm X và Y trong danh sách.\n2. Đọc cột Tổng SL trong kho của X, cột Model của Y.',
     'Mã hàng hóa: mã X, mã Y',
     '- Các ô đó để TRỐNG, không hiện "-", "—" hay số 0.'),
    ('006', 'Trạng thái bảng rỗng', 'P1',
     'Không có khách hàng nào có tên chứa "ZZZZZZ".',
     '1. Gõ "ZZZZZZ" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: ZZZZZZ',
     '- Bảng hiện "Không có dữ liệu phù hợp bộ lọc.".\n'
     '- Chân bảng N = 0, không có thông báo lỗi.'),
    ('007', 'Mở màn kèm hàng hóa trên đường dẫn', 'P1',
     'Hàng hóa SG-MN-HB-XD0107 có lô trong cửa sổ ngày. Có liên kết từ màn khác dẫn sang màn này '
     'kèm hàng hóa đó.',
     '1. Đặt sẵn bộ lọc Thương hiệu = KOISU rồi rời màn.\n'
     '2. Bấm liên kết dẫn sang màn này kèm hàng hóa SG-MN-HB-XD0107.\n3. Bấm Làm mới.',
     NA,
     '- Bước 2: bảng chỉ còn 1 dòng SG-MN-HB-XD0107 (điều kiện hàng hóa trên đường dẫn được áp).\n'
     '- Bước 3: quay về danh sách đầy đủ.'),
    ('008', 'Nhớ bộ lọc khi rời màn và quay lại', 'P1',
     'Màn có dữ liệu.',
     '1. Mở Tìm kiếm nâng cao, chọn Thương hiệu = KOISU.\n2. Chuyển sang màn Danh sách hàng giữ.\n'
     '3. Trong vòng 10 phút quay lại màn này.',
     'Thương hiệu: KOISU',
     '- Thương hiệu vẫn là KOISU, khu vực lọc nâng cao vẫn đang mở.\n'
     '- Bảng chỉ có hàng KOISU.'),
    ('009', 'Bộ lọc hết hiệu lực sau 10 phút', 'P2',
     'Như TC_01.008.',
     '1. Đặt Thương hiệu = KOISU, rời màn.\n2. Sau hơn 10 phút quay lại.',
     'Thương hiệu: KOISU',
     '- Bộ lọc trở về mặc định, bảng hiện toàn bộ.'),
]

S2 = [
    ('001', 'Chỉ hiện lô có hạn giữ trong N ngày gần đây', 'P0',
     'Ngày 05/10/2026, số ngày cảnh báo N = 7.\n'
     'Hàng H1 có 5 lô của cùng nhân viên S với hạn: 27/09/2026, 28/09/2026, 03/10/2026, '
     '05/10/2026, 06/10/2026.',
     '1. Lọc Mã hàng hóa = H1.\n2. Mở rộng dòng H1.\n3. Đọc cột Hạn giữ các dòng khách hàng.',
     'Mã hàng hóa: H1',
     '- Chỉ có 3 lô: 28/09/2026, 03/10/2026, 05/10/2026.\n'
     '- KHÔNG có lô 27/09/2026 (quá N ngày) và 06/10/2026 (còn hạn).'),
    ('002', 'Biên dưới của cửa sổ: hạn giữ đúng hôm nay trừ N ngày được tính', 'P0',
     'Ngày 05/10/2026, N = 7. Hàng H2 chỉ có 1 lô hạn 28/09/2026.',
     '1. Lọc Mã hàng hóa = H2.',
     'Mã hàng hóa: H2',
     '- H2 có trong danh sách; lô hạn 28/09/2026 trạng thái Hết hạn.'),
    ('003', 'Ngay ngoài biên dưới không được tính', 'P0',
     'Ngày 05/10/2026, N = 7. Hàng H3 chỉ có 1 lô hạn 27/09/2026.',
     '1. Lọc Mã hàng hóa = H3.',
     'Mã hàng hóa: H3',
     '- Bảng rỗng "Không có dữ liệu phù hợp bộ lọc.".\n'
     '- Lô này vẫn thấy ở màn Danh sách hàng giữ (đối chiếu).'),
    ('004', 'Lô hết hạn đúng hôm nay là "Đến hạn"', 'P0',
     'Ngày 05/10/2026. Hàng H4 có 1 lô hạn 05/10/2026.',
     '1. Lọc Mã hàng hóa = H4.\n2. Mở rộng dòng H4.',
     'Mã hàng hóa: H4',
     '- Dòng khách hàng: Hạn giữ 05/10/2026, nhãn "Đến hạn" màu vàng.'),
    ('005', 'Lô hết hạn trước hôm nay là "Hết hạn"', 'P0',
     'Ngày 05/10/2026. Hàng SG-MN-HB-XD0107 có lô hạn 03/10/2026 của Đàm Phước Nhiên.',
     '1. Lọc Mã hàng hóa = SG-MN-HB-XD0107.\n2. Mở rộng dòng.',
     'Mã hàng hóa: SG-MN-HB-XD0107',
     '- Dòng khách hàng 50TPHPPH-381: SL giữ 6, Hạn giữ 03/10/2026, nhãn "Hết hạn" màu đỏ.'),
    ('006', 'Lô còn hạn (dù hết hạn ngày mai) không hiện', 'P0',
     'Ngày 05/10/2026. Hàng H5 chỉ có 1 lô hạn 06/10/2026.',
     '1. Lọc Mã hàng hóa = H5.',
     'Mã hàng hóa: H5',
     '- Bảng rỗng.\n'
     '- Lưu ý: tên màn là "sắp hết hạn" nhưng lô còn hạn KHÔNG hiện. Đây là quy tắc giữ nguyên '
     'hệ thống cũ, KHÔNG ghi Failed.'),
    ('007', 'Không bao giờ có trạng thái "Trong hạn"', 'P0',
     'Màn có ít nhất 50 hàng hóa.',
     '1. Mở rộng 10 hàng hóa bất kỳ trên các trang khác nhau.\n2. Đọc cột Trạng thái các dòng '
     'khách hàng.\n3. Xuất Excel đủ trường, lọc cột Trạng thái.',
     NA,
     '- Mọi nhãn chỉ là "Hết hạn" hoặc "Đến hạn".\n'
     '- Tệp Excel không có dòng nào "Trong hạn".\n'
     '- Đây là đúng thiết kế.'),
    ('008', 'SL giữ tầng hàng hóa chỉ cộng lô trong cửa sổ ngày', 'P0',
     'Ngày 05/10/2026, N = 7. Hàng H6 của nhân viên S: lô A 6 cái hạn 03/10/2026, lô B 4 cái hạn '
     '20/10/2026.',
     '1. Lọc Mã hàng hóa = H6.\n2. Đọc SL giữ.\n3. Mở màn Danh sách hàng giữ, lọc H6, đọc SL giữ.',
     'Mã hàng hóa: H6',
     '- Màn này: SL giữ = 6.\n'
     '- Màn Danh sách hàng giữ: SL giữ = 10.\n'
     '- Chênh lệch 4 là lô B còn hạn, đúng quy tắc.'),
    ('009', 'Đổi số ngày cảnh báo thì cửa sổ đổi theo', 'P1',
     'Ngày 05/10/2026. Hàng H3 có 1 lô hạn 27/09/2026. Quản trị đổi số ngày cảnh báo từ 7 thành '
     '10.',
     '1. Mở lại màn (hoặc bấm Làm mới).\n2. Lọc Mã hàng hóa = H3.',
     'Số ngày cảnh báo: 10\nMã hàng hóa: H3',
     '- H3 xuất hiện (27/09/2026 nằm trong 10 ngày gần đây).\n'
     '- Đặt lại số ngày cảnh báo 7 sau khi test.'),
    ('010', 'Sang ngày mới thì lô đổi trạng thái / ra khỏi cửa sổ', 'P1',
     'Hàng H4 có lô hạn 05/10/2026 (Đến hạn trong ngày 05/10/2026), N = 7.',
     '1. Ngày 06/10/2026 mở màn, lọc H4.\n2. Ngày 13/10/2026 mở màn, lọc H4.',
     'Mã hàng hóa: H4',
     '- Ngày 06/10/2026: lô hiện nhãn "Hết hạn".\n'
     '- Ngày 13/10/2026: H4 không còn trên màn (05/10/2026 trước 13/10/2026 trừ 7 ngày).'),
    ('011', 'Ô lọc Trạng thái chỉ có 2 lựa chọn', 'P0',
     'Màn có dữ liệu.',
     '1. Mở Tìm kiếm nâng cao.\n2. Mở ô Trạng thái.',
     NA,
     '- Chỉ có "Hết hạn" và "Đến hạn".\n- KHÔNG có "Trong hạn".'),
    ('012', 'Lọc Trạng thái = Đến hạn', 'P0',
     'Ngày 05/10/2026. Có 3 hàng hóa có lô hạn 05/10/2026; hàng H4 có 1 lô hạn 05/10/2026 và 1 lô '
     'hạn 01/10/2026.',
     '1. Chọn Trạng thái = Đến hạn.\n2. Mở rộng dòng H4.',
     'Trạng thái: Đến hạn',
     '- N = 3.\n'
     '- Dòng H4 chỉ còn lô hạn 05/10/2026; lô 01/10/2026 không hiện.\n'
     '- SL giữ dòng H4 chỉ bằng số của lô đến hạn.'),
    ('013', 'Lọc Trạng thái = Hết hạn', 'P1',
     'Như TC_02.012.',
     '1. Chọn Trạng thái = Hết hạn.\n2. Mở rộng dòng H4.',
     'Trạng thái: Hết hạn',
     '- Mọi dòng khách hàng đều "Hết hạn".\n- Dòng H4 chỉ còn lô 01/10/2026.'),
    ('014', 'Làm mới không bỏ cửa sổ ngày', 'P0',
     'Hàng H5 chỉ có lô còn hạn (06/10/2026).',
     '1. Đặt vài bộ lọc rồi bấm Làm mới.\n2. Lọc Mã hàng hóa = H5.',
     'Mã hàng hóa: H5',
     '- Sau Làm mới vẫn chỉ hiện hàng trong cửa sổ ngày.\n- H5 không có.'),
]

S3 = [
    ('001', 'Tìm nhanh theo tên khách hàng', 'P0',
     'Khách hàng "TRƯỜNG CAO ĐẲNG KHOA HỌC - CÔNG NGHỆ TP.HCM" (mã 50TPHPPH-381) có 1 lô trong '
     'cửa sổ ngày của hàng SG-MN-HB-XD0107.',
     '1. Gõ "CAO ĐẲNG KHOA HỌC" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.\n3. Mở rộng dòng kết quả.',
     'Ô tìm nhanh: CAO ĐẲNG KHOA HỌC',
     '- Danh sách chỉ còn hàng hóa có lô của khách hàng khớp tên, trong đó có SG-MN-HB-XD0107.\n'
     '- Dòng chi tiết chỉ có khách hàng khớp tên.'),
    ('002', 'Tìm nhanh theo mã khách hàng', 'P0',
     'Như TC_03.001.',
     '1. Gõ "50TPHPPH-381".\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: 50TPHPPH-381',
     '- Có hàng SG-MN-HB-XD0107; mọi dòng khách hàng đều là 50TPHPPH-381.'),
    ('003', 'Tìm nhanh theo số điện thoại khách hàng', 'P1',
     'Khách hàng K có số điện thoại 0912345678 và có lô trong cửa sổ ngày.',
     '1. Gõ "0912345678".\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: 0912345678',
     '- Chỉ còn hàng hóa có lô của K.'),
    ('004', 'Ô tìm nhanh không tìm theo mã hàng hóa', 'P1',
     'Không có khách hàng nào có tên / mã / số điện thoại chứa "SG-MN-HB-XD0107".',
     '1. Gõ "SG-MN-HB-XD0107" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: SG-MN-HB-XD0107',
     '- Bảng rỗng: ô tìm nhanh chỉ tìm theo khách hàng, đúng thiết kế.'),
    ('005', 'Ô tìm nhanh chỉ áp dụng khi bấm Tìm kiếm', 'P1',
     'Màn đang N = 500.',
     '1. Gõ "50TPHPPH" vào ô tìm nhanh, KHÔNG bấm Tìm kiếm.\n2. Chờ 3 giây.\n3. Bấm Tìm kiếm.',
     'Ô tìm nhanh: 50TPHPPH',
     '- Bước 2: N vẫn = 500.\n- Bước 3: danh sách thu hẹp.'),
    ('006', 'Lọc Mã hàng hóa tìm gần đúng', 'P0',
     'Có 3 hàng hóa mã bắt đầu "NAHU-" trong cửa sổ ngày.',
     '1. Mở Tìm kiếm nâng cao.\n2. Gõ "NAHU" vào ô Mã hàng hóa.\n3. Chờ 3 giây.',
     'Mã hàng hóa: NAHU',
     '- Danh sách tự nạp lại, không cần bấm Tìm kiếm.\n'
     '- Chỉ còn 3 dòng NAHU-VTX20-BT:02, NAHU-NHXZ-3010:02, NAHU-NHXZ-04:02.'),
    ('007', 'Lọc Tên hàng hóa tìm gần đúng', 'P1',
     'Có hàng "Bệ kiểm tra rung lắc 15 tấn" trong cửa sổ ngày.',
     '1. Gõ "rung lắc" vào ô Tên hàng hóa.\n2. Chờ 3 giây.',
     'Tên hàng hóa: rung lắc',
     '- Có dòng NAHU-VTX15-PD "Bệ kiểm tra rung lắc 15 tấn"; mọi dòng đều chứa "rung lắc".'),
    ('008', 'Ô Lọc theo kho chỉ có kho đang hoạt động', 'P0',
     'Tài khoản DNS Admin. Hệ thống có 55 kho kế toán, trong đó 10 kho Chờ xóa hoặc ngừng dùng.',
     '1. Mở ô Lọc theo kho, đếm số lựa chọn.\n2. Mở màn Danh sách hàng giữ, đếm ô Lọc theo kho.',
     NA,
     '- Màn này: 45 kho, dạng "LN01 - Liên Ninh - Hàng bán", placeholder "Chọn kho".\n'
     '- Màn Danh sách hàng giữ: 55 kho.\n'
     '- Chênh lệch là đúng thiết kế (chỉ màn này bỏ kho đã khóa).'),
    ('009', 'Lọc theo kho giữ lại hàng có tồn ở kho đó', 'P0',
     'Kho LN01 có tồn kho của 3 hàng hóa đang trong cửa sổ ngày; hàng PULI-KU-DP7 không có tồn ở '
     'LN01.',
     '1. Chọn Lọc theo kho = LN01.\n2. Chờ 3 giây.',
     'Lọc theo kho: LN01',
     '- N = 3.\n- Không có PULI-KU-DP7.'),
    ('010', 'Lọc theo kho không đổi số Tổng SL trong kho', 'P1',
     'Hàng H7 tồn 20 ở LN01 và 21 ở SG01 (cùng công ty); có lô trong cửa sổ ngày.',
     '1. Chọn Lọc theo kho = LN01.\n2. Đọc Tổng SL trong kho của H7.',
     'Lọc theo kho: LN01',
     '- Tổng SL trong kho = 41 (tổng mọi kho), KHÔNG phải 20.\n'
     '- Đây là hành vi hiện tại của màn, không ghi Failed.'),
    ('011', 'Lọc Thương hiệu', 'P1',
     'Có 3 hàng KOISU trong cửa sổ ngày.',
     '1. Chọn Thương hiệu = KOISU.\n2. Chờ 3 giây.',
     'Thương hiệu: KOISU',
     '- N = 3, cột Thương hiệu mọi dòng là KOISU.'),
    ('012', 'Lọc Model', 'P1',
     'Hàng PULI-KU-DP5 có model K.U-DP5.',
     '1. Chọn Model = K.U-DP5.',
     'Model: K.U-DP5',
     '- Chỉ còn PULI-KU-DP5.'),
    ('013', 'Lựa chọn Thương hiệu không có lô trong cửa sổ cho bảng rỗng', 'P2',
     'Thương hiệu T có hàng đang giữ nhưng mọi lô đều còn hạn.',
     '1. Mở ô Thương hiệu, tìm T.\n2. Chọn T.',
     'Thương hiệu: T',
     '- T vẫn có trong danh sách lựa chọn.\n'
     '- Bảng rỗng, không báo lỗi. Đây là hành vi hiện tại.'),
    ('014', 'Lọc Nhân viên', 'P0',
     'Nhân viên Đàm Phước Nhiên có 2 lô trong cửa sổ ngày thuộc 1 hàng hóa.',
     '1. Chọn Nhân viên = Đàm Phước Nhiên.\n2. Mở rộng dòng kết quả.',
     'Nhân viên: Đàm Phước Nhiên',
     '- N = 1.\n- Dòng nhân viên chỉ có Đàm Phước Nhiên.'),
    ('015', 'Ô Nhân viên thu hẹp theo Phòng ban', 'P1',
     'Phòng "Bộ Phận Hỗ trợ kinh doanh SG" có 2 nhân viên đang giữ hàng.',
     '1. Chọn Phòng ban = Bộ Phận Hỗ trợ kinh doanh SG.\n2. Mở ô Nhân viên.',
     'Phòng ban: Bộ Phận Hỗ trợ kinh doanh SG',
     '- Ô Nhân viên chỉ còn 2 người của phòng đó.\n- Bảng chỉ còn lô của 2 người đó.'),
    ('016', 'Đổi Công ty / Phòng ban xóa giá trị ô Nhân viên', 'P1',
     'Đang chọn Nhân viên = Đàm Phước Nhiên.',
     '1. Đổi Phòng ban sang phòng khác.',
     NA,
     '- Ô Nhân viên về trống.\n- Danh sách nạp lại theo phòng ban mới.'),
    ('017', 'Công tắc ổ khóa ở ô Công ty / Phòng ban', 'P2',
     'Tài khoản DNS Admin. Có phòng ban đã khoá.',
     '1. Rê chuột vào biểu tượng ổ khóa cạnh nhãn Phòng ban.\n2. Bấm vào biểu tượng.\n'
     '3. Mở ô Phòng ban.',
     NA,
     '- Bước 1: gợi ý "Hiện cả phòng ban đã khoá".\n'
     '- Bước 3: danh sách có thêm các phòng ban đã khoá.\n'
     '- Ô Phòng ban KHÔNG bị khóa nhập.'),
    ('018', 'Kết hợp nhiều điều kiện', 'P1',
     'Có đúng 1 lô của KOISU, trạng thái Hết hạn, nhân viên S.',
     '1. Chọn Thương hiệu = KOISU, Trạng thái = Hết hạn, Nhân viên = S.',
     'Thương hiệu: KOISU\nTrạng thái: Hết hạn\nNhân viên: S',
     '- Chỉ còn 1 hàng hóa, mở rộng ra đúng 1 lô.'),
    ('019', 'Làm mới xóa mọi điều kiện và tự nạp lại', 'P0',
     'Đang có ô tìm nhanh, Thương hiệu, Trạng thái và sắp xếp SL giữ giảm dần.',
     '1. Bấm Làm mới.',
     NA,
     '- Mọi ô lọc và ô tìm nhanh về trống.\n- Bỏ sắp xếp, quay về sắp theo Tên hàng hóa.\n'
     '- Danh sách tự nạp lại trang 1, N = 500.'),
    ('020', 'Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'P2',
     'Khu vực lọc đang đóng.',
     '1. Bấm "Tìm kiếm nâng cao".\n2. Bấm "Ẩn tìm kiếm nâng cao".',
     NA,
     '- Bước 1: hiện các ô Mã hàng hóa, Tên hàng hóa, Lọc theo kho, Thương hiệu, Model, Trạng '
     'thái, Nhân viên, Công ty, Phòng ban; nút đổi chữ thành "Ẩn tìm kiếm nâng cao".\n'
     '- Bước 2: khu vực lọc đóng lại.'),
]

S4 = [
    ('001', 'Cửa sổ Cài đặt bộ lọc liệt kê đủ 8 mục', 'P1',
     'Tài khoản chưa cài đặt bộ lọc ở màn này.',
     '1. Bấm "Cài đặt bộ lọc".',
     NA,
     '- Tiêu đề "Cài đặt bộ lọc", dòng hướng dẫn tích chọn và kéo để sắp xếp.\n'
     '- 8 mục đều được tích: Mã hàng hóa, Tên hàng hóa, Lọc theo kho, Thương hiệu, Model, Trạng '
     'thái, Nhân viên, Công ty - Phòng ban.\n'
     '- Có nút Lưu, Khôi phục mặc định, Đóng.'),
    ('002', 'Ẩn ô lọc và lưu', 'P1',
     'Như TC_04.001.',
     '1. Bỏ tích "Model".\n2. Bấm Lưu.\n3. Tải lại trang.',
     NA,
     '- Khu vực lọc không còn ô Model, kể cả sau khi tải lại trang.'),
    ('003', 'Đổi thứ tự ô lọc bằng kéo thả', 'P2',
     'Như TC_04.001.',
     '1. Kéo "Nhân viên" lên vị trí 1.\n2. Bấm Lưu.',
     NA,
     '- Ô Nhân viên đứng đầu khu vực lọc.'),
    ('004', 'Khôi phục mặc định', 'P2',
     'Đã ẩn Model và đổi thứ tự.',
     '1. Mở Cài đặt bộ lọc.\n2. Bấm "Khôi phục mặc định".\n3. Bấm Lưu.',
     NA,
     '- Đủ 8 mục, đúng thứ tự gốc.'),
    ('005', 'Đóng không lưu', 'P2',
     'Như TC_04.001.',
     '1. Bỏ tích "Trạng thái".\n2. Bấm Đóng.',
     NA,
     '- Ô Trạng thái vẫn hiển thị.'),
    ('006', 'Cửa sổ Tuỳ chỉnh cột: 3 cột khóa', 'P0',
     'Tài khoản chưa tuỳ chỉnh cột.',
     '1. Bấm nút cấu hình cột ở góc phải khối bảng.\n2. Thử bỏ tích STT, Mã hàng hóa / Nhân viên / '
     'Khách hàng, Hành động.',
     NA,
     '- Cửa sổ "Tuỳ chỉnh cột" có 11 cột.\n'
     '- STT và Mã hàng hóa / Nhân viên / Khách hàng có biểu tượng ổ khóa, Hành động mờ; không bỏ '
     'tích được cả 3.'),
    ('007', 'Ẩn cột và lưu', 'P1',
     'Như TC_04.006.',
     '1. Bỏ tích "Model" và "Thương hiệu".\n2. Bấm Lưu.\n3. Tải lại trang.',
     NA,
     '- Bảng không còn 2 cột này, kể cả sau khi tải lại.'),
    ('008', 'Đổi thứ tự cột', 'P2',
     'Như TC_04.006.',
     '1. Kéo "SL giữ" lên ngay sau "Tên hàng hóa / Phòng ban".\n2. Bấm Lưu.',
     NA,
     '- Cột SL giữ đứng thứ 4 trong bảng.'),
]

S5 = [
    ('001', 'Sắp xếp mặc định theo Tên hàng hóa', 'P1',
     'Màn có dữ liệu, chưa bấm sắp xếp.',
     '1. Đọc cột Tên hàng hóa trang 1.',
     NA,
     '- Tên hàng hóa tăng dần A-Z (dòng đầu trên dev là "\'Xe để đồ 3 tầng ( màu xanh)").'),
    ('002', 'Sắp xếp theo SL giữ', 'P0',
     'Màn có dữ liệu.',
     '1. Bấm tiêu đề "SL giữ".\n2. Bấm lần nữa.',
     NA,
     '- Lần 1: SL giữ tăng dần.\n- Lần 2: giảm dần.\n- Mỗi lần bấm đều quay về trang 1.'),
    ('003', 'Sắp xếp theo Tổng SL trong kho', 'P1',
     'Màn có dữ liệu.',
     '1. Bấm tiêu đề "Tổng SL trong kho".',
     NA,
     '- Tổng SL trong kho tăng dần.'),
    ('004', 'Sắp xếp theo Mã hàng hóa', 'P1',
     'Màn có dữ liệu.',
     '1. Bấm tiêu đề "Mã hàng hóa / Nhân viên / Khách hàng".',
     NA,
     '- Mã hàng hóa tăng dần.'),
    ('005', 'Chỉ 4 cột sắp xếp được', 'P2',
     'Màn có dữ liệu.',
     '1. Bấm tiêu đề các cột Đơn vị, Model, Thương hiệu, Hạn giữ, Trạng thái.',
     NA,
     '- Các cột này không có biểu tượng sắp xếp, bấm không đổi thứ tự.'),
    ('006', 'Sắp cột mới hủy sắp cột cũ', 'P2',
     'Đang sắp SL giữ giảm dần.',
     '1. Bấm tiêu đề "Tên hàng hóa / Phòng ban".',
     NA,
     '- Chỉ còn sắp theo Tên hàng hóa; cột SL giữ không còn mũi tên đang chọn.'),
    ('007', 'Đổi số dòng mỗi trang', 'P0',
     'N = 500.',
     '1. Đang ở trang 3, đổi "Số dòng/trang" thành 20.',
     'Số dòng/trang: 20',
     '- Quay về trang 1, bảng 20 dòng hàng hóa.\n- Chân bảng "Hiển thị 1-20 / 500".'),
    ('008', 'Lật trang', 'P1',
     'N = 500, 10 dòng mỗi trang.',
     '1. Bấm trang 2.',
     NA,
     '- Chân bảng "Hiển thị 11-20 / 500".\n- Không trùng dòng với trang 1.'),
    ('009', 'Lật trang thu gọn dòng đang mở rộng', 'P2',
     'Đang mở rộng 2 hàng hóa ở trang 1.',
     '1. Bấm trang 2.\n2. Quay lại trang 1.',
     NA,
     '- Dòng đang mở ở trang 1 đã thu gọn hết.'),
    ('010', 'Dòng chi tiết không tính vào số dòng mỗi trang', 'P1',
     'Hàng hóa đầu trang có 2 nhân viên, 3 lô.',
     '1. Mở rộng hàng hóa đầu trang.\n2. Đếm số dòng hàng hóa trên trang.',
     NA,
     '- Vẫn đủ 10 dòng hàng hóa; 5 dòng chi tiết chèn thêm không làm mất dòng nào.\n'
     '- Chân bảng vẫn "Hiển thị 1-10 / 500".'),
    ('011', 'Số lẻ hiển thị chuẩn quốc tế', 'P1',
     'Hàng NAHU-NHXZ-04:02 có SL giữ 2.8 trong cửa sổ ngày.',
     '1. Tìm dòng NAHU-NHXZ-04:02.',
     'Mã hàng hóa: NAHU-NHXZ-04:02',
     '- SL giữ hiển thị "2.8" (dấu chấm thập phân), không phải "2,8".'),
    ('012', 'Đổi Đơn vị quy đổi cả 3 tầng', 'P0',
     'Hàng H8 có 2 đơn vị: Cái (cơ bản) và Thùng (hệ số 12). Trong cửa sổ ngày H8 có SL giữ 30 '
     'cái, tồn kho 50 cái; 1 nhân viên giữ 30 cái cho 2 khách (18 và 12).',
     '1. Lọc H8, mở rộng dòng.\n2. Ở cột Đơn vị chọn Thùng.',
     'Đơn vị: Thùng (x12)',
     '- Ô Đơn vị là ô chọn, mặc định Cái.\n'
     '- Sau khi đổi: Tổng SL trong kho 4.16, SL giữ 2.5, dòng nhân viên 2.5, hai dòng khách hàng '
     '1.5 và 1.\n'
     '- Lưu ý: làm tròn XUỐNG (50/12 = 4.1666 hiện 4.16, không phải 4.17).'),
    ('013', 'Hàng một đơn vị không có ô chọn', 'P2',
     'Hàng PULI-KU-DP5 chỉ có đơn vị Bộ.',
     '1. Tìm dòng PULI-KU-DP5, bấm vào ô Đơn vị.',
     NA,
     '- Ô Đơn vị hiện chữ "Bộ", không mở danh sách chọn.'),
]

S6 = [
    ('001', 'Mở rộng một hàng hóa', 'P0',
     'Hàng SG-MN-HB-XD0107 có 1 lô của Đàm Phước Nhiên cho khách 50TPHPPH-381, 6 cái, hạn '
     '03/10/2026.',
     '1. Bấm nút tròn ở cột STT dòng SG-MN-HB-XD0107.',
     NA,
     '- Nút đổi thành mũi tên xuống.\n'
     '- Dòng nhân viên: biểu tượng người + "Đàm Phước Nhiên", SL giữ 6, nền xanh lá nhạt.\n'
     '- Dòng khách hàng: "50TPHPPH-381 - TRƯỜNG CAO ĐẲNG KHOA HỌC - CÔNG NGHỆ TP.HCM", SL giữ 6, '
     'Hạn giữ 03/10/2026, nhãn "Hết hạn", nút Lịch sử giữ hàng.'),
    ('002', 'Tổng tầng nhân viên bằng SL giữ tầng hàng hóa', 'P0',
     'Hàng H9 có SL giữ 10 trong cửa sổ ngày, do 2 nhân viên giữ (7 và 3).',
     '1. Mở rộng dòng H9.\n2. Cộng SL giữ các dòng nhân viên.',
     NA,
     '- 2 dòng nhân viên 7 và 3, tổng 10 bằng SL giữ dòng H9.'),
    ('003', 'Dòng nhân viên hiển thị phòng ban', 'P1',
     'Như TC_06.001.',
     '1. Mở rộng dòng.\n2. Đọc cột Tên hàng hóa / Phòng ban ở dòng nhân viên.',
     NA,
     '- Hiện tên phòng ban của nhân viên; dòng khách hàng để trống cột này.'),
    ('004', 'Chi tiết tuân theo bộ lọc đang áp', 'P0',
     'Hàng H9 có lô của khách K1 (hạn 03/10/2026) và khách K2 (hạn 05/10/2026).',
     '1. Tìm nhanh theo mã K1, bấm Tìm kiếm.\n2. Mở rộng dòng H9.',
     'Ô tìm nhanh: mã K1',
     '- Chỉ có dòng khách hàng K1; K2 không hiện.\n- SL giữ dòng H9 chỉ là số của K1.'),
    ('005', 'Chi tiết chỉ có lô trong cửa sổ ngày', 'P0',
     'Hàng H6 như TC_02.008 (lô A hạn 03/10/2026, lô B hạn 20/10/2026).',
     '1. Mở rộng dòng H6.',
     NA,
     '- Chỉ có lô A; lô B còn hạn không hiện.'),
    ('006', 'Chi tiết bó theo phạm vi quyền', 'P0',
     'Tài khoản B chỉ có Quản lý giữ hàng. Hàng H9 do B giữ 3 và đồng nghiệp giữ 7.',
     '1. Đăng nhập B, mở rộng dòng H9.',
     NA,
     '- SL giữ dòng H9 = 3, chỉ 1 dòng nhân viên là B.'),
    ('007', 'Thu gọn và mở lại không tải lại', 'P2',
     'Đã mở rộng 1 hàng hóa.',
     '1. Bấm nút để thu gọn.\n2. Bấm lại để mở.',
     NA,
     '- Thu gọn ẩn các dòng chi tiết.\n- Mở lại hiện ngay, không có biểu tượng xoay chờ tải.'),
    ('008', 'Đổi bộ lọc thu gọn các dòng đang mở', 'P2',
     'Đang mở rộng 2 hàng hóa.',
     '1. Chọn Thương hiệu khác.',
     NA,
     '- Danh sách nạp lại, mọi dòng đều đang thu gọn.'),
    ('009', 'Hạn giữ và Trạng thái chỉ ở dòng khách hàng', 'P1',
     'Đã mở rộng 1 hàng hóa.',
     '1. Đọc cột Hạn giữ, Trạng thái, Hành động ở dòng hàng hóa và dòng nhân viên.',
     NA,
     '- Dòng hàng hóa và dòng nhân viên để trống 3 cột này.\n'
     '- Lưu ý: đây là đúng thiết kế (một hàng hóa có thể gồm nhiều lô hạn khác nhau).'),
    ('010', 'Thứ tự trong chi tiết', 'P2',
     'Hàng H10 có nhân viên "Trần B" và "Nguyễn A"; Nguyễn A giữ cho khách "Z Co" và "A Co".',
     '1. Mở rộng dòng H10.',
     NA,
     '- Nhân viên sắp theo tên (Nguyễn A trước Trần B).\n'
     '- Dưới Nguyễn A: khách sắp theo tên (A Co trước Z Co), cùng khách thì hạn giữ sớm trước.'),
]

S7 = [
    ('001', 'Mở cửa sổ Lịch sử giữ hàng', 'P0',
     'Lô SG-MN-HB-XD0107 của Đàm Phước Nhiên (mã 21710653) cho khách 50TPHPPH-381, hạn '
     '03/10/2026.',
     '1. Mở rộng dòng SG-MN-HB-XD0107.\n2. Bấm nút Lịch sử giữ hàng ở dòng khách hàng.',
     NA,
     '- Cửa sổ "Lịch sử giữ hàng", dòng phụ "Hàng hóa: SG-MN-HB-XD0107 - \'Xe để đồ 3 tầng ( màu '
     'xanh)".\n'
     '- Khối thông tin: Mã hàng SG-MN-HB-XD0107; Kinh doanh "21710653 - Đàm Phước Nhiên"; Khách '
     'hàng "50TPHPPH-381 - TRƯỜNG CAO ĐẲNG KHOA HỌC - CÔNG NGHỆ TP.HCM"; Trạng thái "Hết hạn" '
     'kèm "(Hạn giữ hiện tại: 03/10/2026)".'),
    ('002', 'Bảng biến động sắp từ cũ tới mới', 'P0',
     'Như TC_07.001.',
     '1. Đọc bảng biến động.',
     NA,
     '- Cột: STT, SL biến động, Ngày, SL giữ, Hạn giữ, Chứng từ.\n'
     '- Dòng tiêu đề phụ "Số lượng giữ hiện tại: 6 Cái.".\n'
     '- 5 dòng theo thứ tự: +6 ngày 17/07/2026 PXG-02132; -6 và +6 ngày 10/08/2026 PGHHG-01580; '
     '-6 và +6 ngày 04/09/2026 PGHHG-01727.\n'
     '- Cột SL giữ lần lượt 6, 0, 6, 0, 6; hạn giữ cuối 03/10/2026.'),
    ('003', 'Màu số biến động', 'P2',
     'Như TC_07.001.',
     '1. Quan sát cột SL biến động.',
     NA,
     '- Số dương có dấu + màu xanh; số âm màu đỏ.'),
    ('004', 'Bấm mã chứng từ mở thẻ mới', 'P1',
     'Như TC_07.001.',
     '1. Bấm "PXG-02132".',
     NA,
     '- Phiếu xuất giữ PXG-02132 mở ở thẻ mới của trình duyệt; cửa sổ lịch sử vẫn còn ở thẻ cũ.'),
    ('005', 'Lịch sử không bị bó theo cửa sổ ngày', 'P1',
     'Lô có biến động từ tháng 07/2026.',
     '1. Mở Lịch sử giữ hàng của lô.',
     NA,
     '- Vẫn thấy biến động ngày 17/07/2026 dù cũ hơn 7 ngày.'),
    ('006', 'Số lượng theo đơn vị đang chọn', 'P2',
     'Hàng H8 (Cái / Thùng x12), lô 12 cái.',
     '1. Đổi Đơn vị dòng H8 thành Thùng.\n2. Mở Lịch sử của lô.',
     'Đơn vị: Thùng',
     '- "Số lượng giữ hiện tại: 1 Thùng."; cột SL giữ quy đổi theo Thùng.'),
    ('007', 'Đóng cửa sổ', 'P2',
     'Đang mở cửa sổ lịch sử.',
     '1. Bấm Đóng.',
     NA,
     '- Cửa sổ đóng; bảng giữ nguyên các dòng đang mở rộng.'),
]

S8 = [
    ('001', 'Mở cửa sổ chọn trường', 'P0',
     'Màn có dữ liệu.',
     '1. Bấm "Xuất Excel".',
     NA,
     '- Cửa sổ "Chọn trường xuất Excel" với 12 trường đều đã tích: Mã hàng hóa, Tên hàng hóa, ĐVT, '
     'Model, Thương hiệu, Nhân viên giữ, Phòng ban, Khách hàng, SL giữ, Tổng SL trong kho, Hạn giữ, '
     'Trạng thái.\n'
     '- Dòng "Đang chọn 12/12 trường"; có nút Chọn tất cả, Bỏ chọn hết, Xuất file, Đóng.'),
    ('002', 'Xuất đủ trường', 'P0',
     'Bộ lọc mặc định. Bản in cùng bộ lọc có Số mục hàng = 734.',
     '1. Bấm Xuất Excel.\n2. Bấm Xuất file.\n3. Mở tệp tải về.',
     NA,
     '- Tải về tệp hang_sap_het_han_giu.xlsx, thông báo "Xuất Excel thành công".\n'
     '- Dòng 1 "DANH SÁCH HÀNG SẮP HẾT HẠN GIỮ"; dòng 2 tiêu đề: STT + 12 cột.\n'
     '- 734 dòng dữ liệu, mỗi dòng một lô (không chia tầng).'),
    ('003', 'Tệp gồm mọi trang, không chỉ trang đang xem', 'P0',
     'N = 500, đang ở trang 1, 10 dòng mỗi trang.',
     '1. Xuất đủ trường.',
     NA,
     '- Tệp có dữ liệu của cả 500 hàng hóa, không chỉ 10 hàng của trang 1.'),
    ('004', 'Tệp theo bộ lọc đang áp', 'P0',
     'Lọc Thương hiệu = KOISU, có 3 hàng hóa với 4 lô.',
     '1. Xuất đủ trường.',
     'Thương hiệu: KOISU',
     '- Tệp có 4 dòng, cột Thương hiệu đều là KOISU.'),
    ('005', 'Chọn bớt trường và đổi thứ tự', 'P1',
     'Màn có dữ liệu.',
     '1. Bấm "Bỏ chọn hết".\n2. Tích Khách hàng, Mã hàng hóa, Hạn giữ.\n3. Kéo Hạn giữ lên đầu '
     'danh sách.\n4. Bấm Xuất file.',
     NA,
     '- Dòng đếm "Đang chọn 3/12 trường".\n'
     '- Tệp có 4 cột: STT, Hạn giữ, rồi các cột còn lại theo thứ tự trong danh sách.\n'
     '- Cột STT luôn đứng đầu.'),
    ('006', 'Bỏ chọn hết thì không xuất', 'P2',
     'Màn có dữ liệu.',
     '1. Bấm "Bỏ chọn hết".\n2. Bấm Xuất file.',
     NA,
     '- Không tải tệp nào.'),
    ('007', 'Số lượng trong tệp theo đơn vị cơ bản', 'P0',
     'Hàng H8 (Cái / Thùng x12) có lô 24 cái. Trên màn đang chọn đơn vị Thùng (hiện 2).',
     '1. Xuất đủ trường.\n2. Tìm dòng H8.',
     NA,
     '- Cột ĐVT = Cái, SL giữ = 24 (KHÔNG phải 2 Thùng).'),
    ('008', 'Định dạng số và ngày trong tệp', 'P1',
     'Có lô SL giữ 2.8 và hàng tồn 1,250.',
     '1. Xuất đủ trường.\n2. Bấm vào các ô số.',
     NA,
     '- Ô số là kiểu số (không có cảnh báo số lưu dạng chữ), hiển thị 2.8 và 1,250.\n'
     '- Hạn giữ dạng dd/mm/yyyy.\n- Ô không có dữ liệu để trống.'),
    ('009', 'Tệp chỉ có Hết hạn / Đến hạn', 'P1',
     'Bộ lọc mặc định.',
     '1. Xuất đủ trường.\n2. Lọc cột Trạng thái trong Excel.',
     NA,
     '- Chỉ có 2 giá trị "Hết hạn" và "Đến hạn".'),
    ('010', 'Khóa nút khi đang xuất', 'P2',
     'Dữ liệu lớn (vài nghìn lô).',
     '1. Bấm Xuất file rồi bấm tiếp nhiều lần.',
     NA,
     '- Nút bị khóa trong lúc xuất, chỉ tải về 1 tệp.'),
]

S9 = [
    ('001', 'Mở bản xem trước', 'P0',
     'Tài khoản DNS Admin, bộ lọc mặc định, ngày 05/10/2026.',
     '1. Bấm "In".',
     NA,
     '- Cửa sổ "Xem trước danh sách hàng sắp hết hạn giữ", khổ ngang, nút In màu xanh.\n'
     '- Có tiêu đề công ty và tiêu đề "DANH SÁCH HÀNG SẮP HẾT HẠN GIỮ".\n'
     '- Ngày in 05/10/2026, Số phòng ban 14, Số nhân viên 44, Số mục hàng 734.'),
    ('002', 'Bố cục gom 3 cấp', 'P0',
     'Như TC_09.001.',
     '1. Đọc bảng trong bản in.',
     NA,
     '- Cột: STT, Tên hàng hóa, Mã hàng, ĐVT, SL giữ, Hạn giữ, Khách hàng, Trạng thái.\n'
     '- Dòng STT 1 dạng "Bộ Phận Hỗ trợ kinh doanh SG - 2 nhân viên - 91 mục hàng".\n'
     '- Dòng STT 1.1 dạng "Nguyễn Ngọc Hoa - 80 mục hàng".\n'
     '- Dòng STT 1.1.1 là từng lô.'),
    ('003', 'Số mục hàng khớp tệp Excel', 'P0',
     'Như TC_09.001.',
     '1. Đọc Số mục hàng trên bản in.\n2. Xuất Excel cùng bộ lọc, đếm dòng.',
     NA,
     '- Cả hai đều 734.\n'
     '- Lưu ý: 734 lô lớn hơn N = 500 hàng hóa ở chân bảng là đúng.'),
    ('004', 'Bản in theo bộ lọc đang áp', 'P0',
     'Lọc Nhân viên = Nguyễn Ngọc Hoa (80 lô).',
     '1. Bấm In.',
     'Nhân viên: Nguyễn Ngọc Hoa',
     '- Số nhân viên 1, Số mục hàng 80; chỉ có nhóm của Nguyễn Ngọc Hoa.'),
    ('005', 'Bản in chỉ có Hết hạn / Đến hạn', 'P1',
     'Như TC_09.001.',
     '1. Đọc cột Trạng thái trên bản in.',
     NA,
     '- Chỉ có "Hết hạn" hoặc "Đến hạn".'),
    ('006', 'Không có dữ liệu để in', 'P2',
     'Bộ lọc cho bảng rỗng.',
     '1. Tìm nhanh "ZZZZZZ", bấm Tìm kiếm.\n2. Bấm In.',
     'Ô tìm nhanh: ZZZZZZ',
     '- Cửa sổ báo "Không có dữ liệu để in".'),
    ('007', 'Gửi lệnh in', 'P1',
     'Đang mở bản xem trước.',
     '1. Bấm nút In màu xanh trong cửa sổ.',
     NA,
     '- Hộp thoại in của trình duyệt mở ra; nội dung đúng như bản xem trước, không mất viền khi '
     'sang trang.'),
    ('008', 'Đóng bản xem trước', 'P2',
     'Đang mở bản xem trước.',
     '1. Bấm dấu x góc phải.',
     NA,
     '- Cửa sổ đóng, màn danh sách giữ nguyên bộ lọc.'),
]

S10 = [
    ('001', 'Đối chiếu với màn Danh sách hàng giữ', 'P0',
     'Ngày 05/10/2026, N = 7. Tài khoản DNS Admin.',
     '1. Mở màn Danh sách hàng giữ, lọc Trạng thái = Hết hạn rồi xuất Excel; giữ các lô có hạn từ '
     '28/09/2026 đến 04/10/2026.\n'
     '2. Lọc Trạng thái = Đến hạn, xuất Excel.\n'
     '3. Ở màn này xuất Excel đủ trường.',
     NA,
     '- Tập lô ở bước 3 bằng đúng hợp của bước 1 (đã lọc theo hạn) và bước 2.'),
    ('002', 'Đối chiếu số liệu với hệ thống cũ', 'P1',
     'Cùng ngày, cùng tài khoản có quyền xem tổng công ty trên hệ thống cũ (màn Hàng sắp hết hạn '
     'giữ bản kế toán).',
     '1. Đếm số hàng hóa trên hệ thống cũ.\n2. Đếm N trên màn này.',
     NA,
     '- Hai số bằng nhau khi hai bên dùng cùng dữ liệu.\n'
     '- Lưu ý: dữ liệu môi trường dev và môi trường cục bộ có thể khác nhau; chỉ đối chiếu trên '
     'cùng cơ sở dữ liệu.'),
    ('003', 'Gia hạn lô thì lô rời khỏi màn', 'P0',
     'Lô L của hàng H11 hạn 03/10/2026 (đang hiện trên màn).',
     '1. Lập và duyệt phiếu gia hạn hàng giữ cho lô L tới 20/10/2026.\n2. Mở lại màn, lọc H11.\n'
     '3. Mở Lịch sử giữ hàng của lô L ở màn Danh sách hàng giữ.',
     'Hạn mới: 20/10/2026',
     '- Bước 2: lô L không còn trên màn này (đã còn hạn).\n'
     '- Bước 3: có dòng -x / +x với chứng từ phiếu gia hạn, hạn giữ mới 20/10/2026.'),
    ('004', 'Hủy hàng giữ thì số giảm', 'P1',
     'Lô L2 của hàng H12, 5 cái, hạn 04/10/2026.',
     '1. Lập và duyệt phiếu hủy hàng giữ 2 cái cho L2.\n2. Mở lại màn, lọc H12.',
     NA,
     '- SL giữ của H12 giảm 2 (còn 3).'),
    ('005', 'Màn không làm thay đổi dữ liệu', 'P1',
     'Ghi lại SL giữ của 3 hàng hóa ở màn Danh sách hàng giữ.',
     '1. Ở màn này mở rộng, xem lịch sử, xuất Excel, in nhiều lần.\n'
     '2. Mở lại màn Danh sách hàng giữ.',
     NA,
     '- SL giữ của 3 hàng hóa không đổi; không phát sinh dòng lịch sử mới nào.'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'QUY TẮC CỬA SỔ NGÀY & TRẠNG THÁI HẠN GIỮ', S2),
    ('III', 'BỘ LỌC & TÌM KIẾM', S3),
    ('IV', 'CÀI ĐẶT BỘ LỌC & TUỲ CHỈNH CỘT', S4),
    ('V', 'SẮP XẾP, PHÂN TRANG & ĐƠN VỊ', S5),
    ('VI', 'XEM CHI TIẾT THEO NHÂN VIÊN VÀ KHÁCH HÀNG', S6),
    ('VII', 'LỊCH SỬ GIỮ HÀNG', S7),
    ('VIII', 'XUẤT EXCEL', S8),
    ('IX', 'IN DANH SÁCH', S9),
    ('X', 'ĐỐI CHIẾU SỐ LIỆU & LUỒNG NGHIỆP VỤ LIÊN QUAN', S10),
]

build(output_file=os.path.join(BASE, 'testcase - Hang sap het han giu.xlsx'),
      sheet_name='Trang tính1',
      feature_name='Hàng sắp hết hạn giữ',
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
