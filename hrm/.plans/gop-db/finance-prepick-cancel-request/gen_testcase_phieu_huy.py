# -*- coding: utf-8 -*-
"""Sinh "testcase - Phieu huy hang giu.xlsx" (phan he Tai chinh, nhom Giu hang).

Man ANH EM cua "Yeu cau huy hang giu" (gen_testcase.py cung thu muc) — 2 file rieng,
KHONG gop chung mot file.

Viet tu code HRM nhanh `gop_db` + khao sat that tren cong dev ngay 09/09/2026.
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

MODULE = 'Phiếu hủy hàng giữ'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn hình Phiếu hủy hàng giữ (mã phiếu PHHG) là chứng từ DUYỆT của Phiếu yêu cầu hủy hàng '
     'giữ (mã PYCHHG).\n'
     'Người có quyền "Quản lý giữ hàng" chọn một phiếu yêu cầu đang Chờ duyệt, quyết định số '
     'lượng thực sự cho hủy ở từng dòng hàng rồi lưu. Chính lúc lưu phiếu này, hàng giữ mới bị '
     'trừ và phiếu yêu cầu mới chuyển sang Đã duyệt.\n'
     'Phiếu lập xong là chốt vĩnh viễn: không sửa, không xóa, không hủy duyệt.\n'
     'Đường dẫn: Phân hệ Tài chính → Giữ hàng → Phiếu hủy hàng giữ.'),
    ('2. Đối tượng được tính / hiển thị',
     'Danh sách hiển thị phiếu hủy theo phạm vi quyền của người đăng nhập:\n'
     '- Có quyền "Xem phiếu hàng giữ theo tổng công ty": toàn bộ phiếu hủy của mọi công ty.\n'
     '- Có quyền "Xem phiếu hàng giữ theo công ty": phiếu hủy thuộc công ty của mình.\n'
     '- Có quyền "Quản lý giữ hàng": phiếu hủy thuộc công ty của mình (tương đương cấp công ty).\n'
     '- Không có quyền nào ở trên: chỉ phiếu do chính mình lập, CỘNG THÊM phiếu sinh ra từ phiếu '
     'yêu cầu do chính mình lập.\n'
     'Cửa sổ chọn phiếu yêu cầu chỉ liệt kê phiếu yêu cầu ở trạng thái Chờ duyệt, thuộc công ty '
     'của người đăng nhập.\n'
     'Bảng chi tiết chỉ nạp các dòng đã được tích "Cần hủy" trên phiếu yêu cầu.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu yêu cầu ở trạng thái Đang tạo hoặc Đã duyệt: KHÔNG xuất hiện trong cửa sổ chọn '
     'phiếu yêu cầu.\n'
     '- Phiếu yêu cầu của công ty khác: không xuất hiện trong cửa sổ chọn, kể cả khi người dùng '
     'có quyền xem theo tổng công ty.\n'
     '- Người không có quyền "Quản lý giữ hàng": cửa sổ chọn phiếu yêu cầu luôn rỗng.\n'
     '- Dòng hàng bị bỏ tích "Cần hủy": không được gửi lên khi lưu, không trừ hàng giữ.\n'
     '- Dòng hàng không được đề nghị hủy trên phiếu yêu cầu: không có trong bảng chi tiết.\n'
     '- Màn hình KHÔNG có thao tác Sửa, Xóa, Hủy duyệt — không có nút nào tương ứng.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Hai ô "Ngày tạo từ" và "Ngày tạo đến" lọc theo NGÀY LẬP PHIẾU HỦY, không phải ngày lập '
     'phiếu yêu cầu.\n'
     'Khoảng ngày lấy trọn hai đầu mút. Chỉ nhập một đầu thì lọc một chiều.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Một phiếu hủy gắn với đúng MỘT phiếu yêu cầu; ngược lại một phiếu yêu cầu chỉ sinh ra đúng '
     'một phiếu hủy.\n'
     'Phiếu hủy gồm phần thông tin chung (phiếu yêu cầu, người yêu cầu, phòng ban yêu cầu, khách '
     'hàng, kho, ghi chú) và nhiều dòng hàng hóa.\n'
     'Mỗi dòng hàng có ba số lượng: "Có thể hủy" (hàng giữ còn lại, chỉ hiện ở màn lập phiếu), '
     '"Yêu cầu hủy" (người lập yêu cầu đề nghị) và "Duyệt hủy" (số thực sự bị trừ).\n'
     'Một hàng hóa có thể nằm trên nhiều lô hàng giữ khác nhau theo hạn giữ.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     'Khi lưu, phần mềm trừ hàng giữ theo thứ tự hạn giữ SỚM TRƯỚC, muộn sau; trừ hết lô này mới '
     'sang lô kế tiếp.\n'
     'Lô hàng giữ được tìm theo NGƯỜI LẬP PHIẾU YÊU CẦU và công ty của người đó, KHÔNG phải theo '
     'người đang lập phiếu hủy.\n'
     'Nếu tổng các lô không đủ số cần trừ thì toàn bộ thao tác bị hủy bỏ — không trừ một phần, '
     'không tạo phiếu.\n'
     'Số lượng được quy đổi về đơn vị cơ bản của hàng hóa trước khi trừ.'),
    ('7. Phân quyền cấp',
     'Màn hình dùng lại bốn quyền sẵn có của nhóm Giữ hàng:\n'
     '- "Quản lý giữ hàng": quyền DUY NHẤT cho phép lập phiếu hủy (tức duyệt).\n'
     '- "Xem phiếu hàng giữ theo tổng công ty": xem phiếu hủy của mọi công ty.\n'
     '- "Xem phiếu hàng giữ theo công ty": xem phiếu hủy thuộc công ty mình.\n'
     '- "Xem phiếu hàng giữ theo phòng ban": KHÔNG có tác dụng ở màn này (khác màn Yêu cầu hủy '
     'hàng giữ) — người chỉ có quyền này xem như không có quyền phạm vi nào.\n'
     'Màn hình KHÔNG có quyền riêng cho Thêm / Sửa / Xóa.'),
    ('8. Cách tính các ô thống kê',
     'Ô "Hiển thị a–b / N": a là số thứ tự dòng đầu trang, b là dòng cuối trang, N là tổng số '
     'phiếu khớp bộ lọc trong phạm vi quyền của người đăng nhập.\n'
     'Cột "Có thể hủy" = số hàng giữ còn lại của người lập phiếu yêu cầu, đã trừ phần đang nằm '
     'trên các đề nghị xuất kho chưa hoàn tất. Số này được tính LẠI tại thời điểm mở form nên có '
     'thể khác số trên phiếu yêu cầu.\n'
     'Ô "Duyệt hủy" được điền sẵn bằng đúng số "Yêu cầu hủy" khi vừa chọn phiếu yêu cầu.\n'
     'Số lô đã trừ hiện trong ghi chú của mốc lịch sử, dạng "Đã trừ tồn hàng giữ trên N lô.".'),
    ('9. Ghi chú đọc bảng',
     'BẪY DỄ SAI NHẤT của màn này:\n'
     '- Số "Duyệt hủy" KHÔNG bị chặn bởi số "Yêu cầu hủy". Duyệt 4 cho phiếu đề nghị 3 là ĐÚNG, '
     'miễn còn đủ hàng giữ. Đừng ghi Failed cho trường hợp này.\n'
     '- Trần chặn duy nhất là cột "Có thể hủy".\n'
     '- Ô "Kho" ở màn chi tiết TRỐNG là ĐÚNG, không phải lỗi: hàng giữ tính theo nhân viên và '
     'khách hàng chứ không gắn kho.\n'
     '- Ô lọc Trạng thái có ba lựa chọn nhưng chỉ "Đã đề nghị" ra kết quả; hai lựa chọn còn lại '
     'luôn rỗng — đây là chủ ý bám hệ thống cũ, KHÔNG phải lỗi.\n'
     '- Nút "Duyệt và tiếp tục" chạy đúng luồng duyệt (trừ hàng giữ ngay), không phải lưu nháp. '
     'Phiếu hủy KHÔNG có trạng thái nháp.\n'
     '- Nhập số vượt trần thì phần mềm báo đỏ dưới ô và GIỮ NGUYÊN số vừa gõ; tự kéo về trần mới '
     'là lỗi.\n'
     '- Số hiển thị theo chuẩn quốc tế: dấu phẩy ngăn hàng nghìn, dấu chấm phần thập phân.\n'
     '- Mọi thao tác lập phiếu đều KHÔNG hoàn tác được — hãy test trên dữ liệu chấp nhận mất.'),
]

ROLE_TCS = [
    ('00', 'Tài khoản không có quyền nào của nhóm hàng giữ vẫn vào được màn hình', 'P0',
     'Tài khoản A không có quyền Quản lý giữ hàng và không có quyền xem theo cấp nào; A đã lập '
     '2 phiếu hủy; A cũng là người lập 3 phiếu yêu cầu đã được người khác duyệt.',
     '1. Đăng nhập bằng tài khoản A.\n'
     '2. Vào Tài chính → Giữ hàng → Phiếu hủy hàng giữ.\n'
     '3. Đọc ô "Hiển thị a–b / N".',
     '—',
     '- Màn hình mở được, không báo lỗi quyền.\n'
     '- Danh sách có đúng 5 phiếu: 2 phiếu A tự lập và 3 phiếu sinh từ phiếu yêu cầu của A.\n'
     '- Ô "Hiển thị a–b / N" ghi N = 5.\n'
     '- Nút Tạo mới vẫn hiển thị.'),
    ('01', 'Quyền "Quản lý giữ hàng" lập được phiếu hủy', 'P0',
     'Tài khoản B có quyền Quản lý giữ hàng, thuộc công ty 1. Công ty 1 có 8 phiếu yêu cầu đang '
     'Chờ duyệt.',
     '1. Đăng nhập bằng B.\n'
     '2. Bấm Tạo mới.\n'
     '3. Bấm nút tra cứu bên phải ô "Phiếu yêu cầu hủy hàng giữ".',
     '—',
     '- Cửa sổ "Phiếu chờ duyệt" mở ra và liệt kê đúng 8 phiếu.\n'
     '- Chọn một phiếu thì form được điền sẵn và nút Duyệt hiện ra.'),
    ('02', 'Thiếu quyền "Quản lý giữ hàng" thì cửa sổ chọn phiếu yêu cầu rỗng', 'P0',
     'Tài khoản A không có quyền Quản lý giữ hàng. Công ty của A đang có 8 phiếu yêu cầu Chờ '
     'duyệt.',
     '1. Đăng nhập bằng A.\n'
     '2. Bấm Tạo mới.\n'
     '3. Bấm nút tra cứu phiếu yêu cầu.',
     '—',
     '- ⚠️ Cửa sổ mở được nhưng KHÔNG có dòng nào, dù công ty đang có 8 phiếu chờ duyệt.\n'
     '- Không chọn được phiếu nào nên nút Duyệt không bao giờ hiện.'),
    ('03', 'Quyền "Xem phiếu hàng giữ theo tổng công ty"', 'P0',
     'Tài khoản C chỉ có quyền này, thuộc công ty 1. Hệ thống có phiếu hủy của công ty 1 và '
     'công ty 4.',
     '1. Đăng nhập bằng C.\n'
     '2. Mở màn danh sách và đọc N.\n'
     '3. Mở một phiếu của công ty 4.',
     '—',
     '- Thấy phiếu hủy của mọi công ty.\n'
     '- Mở được phiếu của công ty 4, không báo lỗi quyền.\n'
     '- ⚠️ Nút Tạo mới vẫn hiện nhưng cửa sổ chọn phiếu yêu cầu rỗng vì C không có quyền Quản lý '
     'giữ hàng.'),
    ('04', 'Quyền "Xem phiếu hàng giữ theo công ty"', 'P0',
     'Tài khoản D thuộc công ty 1, chỉ có quyền này. Công ty 1 có 3,100 phiếu hủy, công ty 4 có '
     '300 phiếu hủy.',
     '1. Đăng nhập bằng D.\n'
     '2. Đọc N.\n'
     '3. Mở một phiếu của công ty 4 bằng đường dẫn trực tiếp trên thanh địa chỉ.',
     '—',
     '- N = 3,100, không thấy phiếu của công ty 4.\n'
     '- ⚠️ Mở phiếu công ty 4 bằng đường dẫn: phần mềm báo không có quyền xem phiếu này.'),
    ('05', 'Quyền "Xem phiếu hàng giữ theo phòng ban" KHÔNG mở rộng phạm vi ở màn này', 'P1',
     'Tài khoản E chỉ có quyền "Xem phiếu hàng giữ theo phòng ban", quản lý một phòng có 60 '
     'phiếu hủy do người khác trong phòng lập. E tự lập 1 phiếu hủy.',
     '1. Đăng nhập bằng E.\n'
     '2. Mở màn danh sách và đọc N.',
     '—',
     '- ⚠️ N = 1, chỉ thấy phiếu của chính E — KHÁC hẳn màn Yêu cầu hủy hàng giữ.\n'
     '- Đây là hành vi ĐÚNG theo thiết kế, không ghi Failed.'),
    ('06', 'Người lập phiếu yêu cầu xem được phiếu hủy sinh ra từ phiếu của mình', 'P1',
     'Tài khoản A không có quyền phạm vi nào. Phiếu yêu cầu do A lập đã được B (công ty khác '
     'phòng) duyệt, sinh ra phiếu hủy X.',
     '1. Đăng nhập bằng A.\n'
     '2. Tìm phiếu X trong danh sách.\n'
     '3. Mở chi tiết phiếu X.',
     '—',
     '- Phiếu X có trong danh sách của A.\n'
     '- A mở được chi tiết, thấy đủ thông tin và bảng hàng hóa.'),
    ('07', 'Gọi thẳng chức năng lập phiếu, bỏ qua giao diện', 'P0',
     'Tài khoản A không có quyền Quản lý giữ hàng. Tồn tại phiếu yêu cầu Y đang Chờ duyệt.',
     '1. Dùng công cụ kiểm thử API, đăng nhập bằng A.\n'
     '2. Gọi thẳng chức năng Lập phiếu hủy với mã phiếu yêu cầu Y và một dòng hàng hợp lệ.',
     'Số duyệt hủy: 1',
     '- ⚠️ Phần mềm từ chối, báo phiếu yêu cầu không còn ở trạng thái chờ duyệt hoặc không đủ '
     'quyền duyệt.\n'
     '- Không có phiếu hủy nào được tạo.\n'
     '- Hàng giữ của phiếu Y KHÔNG bị trừ.\n'
     '- Phiếu Y vẫn ở trạng thái Chờ duyệt.'),
]

S1 = [
    ('001', 'Vào màn qua menu Tài chính', 'P0',
     'Tài khoản B có quyền Quản lý giữ hàng, công ty 1 có 3,496 phiếu hủy.',
     '1. Đăng nhập.\n2. Vào Tài chính → Giữ hàng → Phiếu hủy hàng giữ.',
     '—',
     '- Tiêu đề màn là "Phiếu hủy hàng giữ".\n'
     '- Bảng hiện 10 dòng đầu, ô thống kê ghi "Hiển thị 1–10 / 3,496".\n'
     '- Vòng quay chờ biến mất sau khi dữ liệu nạp xong.'),
    ('002', 'Bộ cột mặc định của bảng', 'P0',
     'Tài khoản chưa từng tuỳ chỉnh cột ở màn này.',
     '1. Mở màn danh sách.\n2. Đọc tiêu đề các cột từ trái sang phải.',
     '—',
     '- Đúng thứ tự: STT, Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người tạo, Ngày tạo, '
     'Trạng thái, Người cập nhật, Ngày cập nhật, Hành động.\n'
     '- Hai cột Khách hàng và Ghi chú KHÔNG hiện (mặc định tắt).'),
    ('003', 'Cột Hành động chỉ có In và Lịch sử', 'P0',
     'Danh sách có ít nhất 1 phiếu hủy.',
     '1. Mở màn danh sách.\n2. Rê chuột vào cột Hành động của dòng đầu tiên.',
     '—',
     '- Đúng 2 nút: In (biểu tượng máy in) và Lịch sử (biểu tượng đồng hồ).\n'
     '- ⚠️ KHÔNG có nút Sửa, KHÔNG có nút Xóa ở bất kỳ dòng nào, kể cả phiếu do chính mình vừa '
     'lập. Đây là đúng thiết kế.'),
    ('004', 'Trạng thái của mọi phiếu đều là Đã đề nghị', 'P1',
     'Danh sách có ít nhất 20 phiếu hủy.',
     '1. Mở màn danh sách.\n2. Đọc cột Trạng thái của cả trang.\n3. Sang trang 2 đọc tiếp.',
     '—',
     '- Mọi dòng đều hiện huy hiệu "Đã đề nghị" màu xanh lá.\n'
     '- ⚠️ Không có phiếu nào ở trạng thái khác — đúng thiết kế, phiếu hủy không có vòng đời.'),
    ('005', 'Mã phiếu là liên kết mở màn chi tiết', 'P0',
     'Phiếu PHHG-03501 tồn tại và người dùng có quyền xem.',
     '1. Bấm vào mã phiếu PHHG-03501.',
     '—',
     '- Mở màn chi tiết, tiêu đề ghi "Chi tiết phiếu hủy hàng giữ: PHHG-03501".'),
    ('006', 'Mã phiếu yêu cầu là liên kết mở phiếu yêu cầu gốc', 'P1',
     'Phiếu PHHG-03501 sinh từ phiếu yêu cầu PYCHHG-03567.',
     '1. Ở dòng của PHHG-03501, bấm vào mã PYCHHG-03567 ở cột Phiếu yêu cầu.',
     '—',
     '- Chuyển sang màn chi tiết của phiếu yêu cầu PYCHHG-03567.\n'
     '- Phiếu yêu cầu đó ở trạng thái Đã duyệt.'),
    ('007', 'Phân biệt cột Người yêu cầu và Người tạo', 'P0',
     'Phiếu hủy Z do B lập, sinh từ phiếu yêu cầu của nhân viên S (khác người).',
     '1. Tìm phiếu Z trong danh sách.\n2. Đọc cột Người yêu cầu và cột Người tạo.',
     '—',
     '- Cột Người yêu cầu ghi tên S (người lập phiếu yêu cầu).\n'
     '- Cột Người tạo ghi tên B (người lập phiếu hủy, tức người duyệt).\n'
     '- ⚠️ Hai cột này khác nhau; ghi nhầm vai là lỗi đọc bảng.'),
    ('008', 'Danh sách rỗng khi bộ lọc không khớp gì', 'P1',
     'Không có phiếu hủy nào có mã chứa chuỗi "ZZZZZZ".',
     '1. Gõ "ZZZZZZ" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: ZZZZZZ',
     '- Bảng hiện đúng dòng "Không có dữ liệu phù hợp.".\n'
     '- Ô thống kê ghi N = 0.\n'
     '- Không có thông báo lỗi nào.'),
]

S2 = [
    ('001', 'Tìm nhanh theo mã phiếu hủy', 'P0',
     'Tồn tại phiếu PHHG-03501.',
     '1. Gõ "PHHG-03501" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: PHHG-03501',
     '- Danh sách còn đúng 1 dòng là PHHG-03501.'),
    ('002', 'Tìm nhanh theo mã phiếu YÊU CẦU', 'P0',
     'Phiếu PHHG-03501 sinh từ phiếu yêu cầu PYCHHG-03567.',
     '1. Gõ "PYCHHG-03567" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: PYCHHG-03567',
     '- ⚠️ Vẫn tìm ra phiếu hủy PHHG-03501 dù đang gõ mã của phiếu yêu cầu.\n'
     '- Đây là hành vi đúng: ô tìm nhanh tra cả hai loại mã.'),
    ('003', 'Tìm nhanh theo tên người tạo', 'P1',
     'Có ít nhất 3 phiếu hủy do "Nguyễn Anh Tú" lập.',
     '1. Gõ "Nguyễn Anh Tú" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: Nguyễn Anh Tú',
     '- Chỉ còn các phiếu có cột Người tạo là Nguyễn Anh Tú.'),
    ('004', 'Ô tìm nhanh chỉ áp dụng khi bấm Tìm kiếm', 'P1',
     'Danh sách đang có 3,496 phiếu.',
     '1. Gõ "PHHG-035" vào ô tìm nhanh nhưng KHÔNG bấm Tìm kiếm.\n2. Chờ 3 giây.',
     'Ô tìm nhanh: PHHG-035',
     '- ⚠️ Danh sách KHÔNG tự nạp lại, vẫn giữ nguyên 3,496 phiếu.\n'
     '- Chỉ khi bấm Tìm kiếm mới lọc.'),
    ('005', 'Đổi ô lọc nâng cao thì danh sách tự nạp lại', 'P0',
     'Có phiếu hủy của nhiều người tạo khác nhau.',
     '1. Mở Tìm kiếm nâng cao.\n2. Chọn một giá trị ở ô Người tạo.\n3. KHÔNG bấm Tìm kiếm, chờ '
     '3 giây.',
     'Người tạo: DNS Admin',
     '- ⚠️ Danh sách tự nạp lại ngay, không cần bấm Tìm kiếm.\n'
     '- Chỉ còn phiếu do DNS Admin lập.'),
    ('006', 'Lọc theo Mã phiếu yêu cầu (tìm gần đúng)', 'P0',
     'Có các phiếu sinh từ phiếu yêu cầu PYCHHG-03565, PYCHHG-03566, PYCHHG-03567.',
     '1. Mở Tìm kiếm nâng cao.\n2. Gõ "0356" vào ô Mã phiếu yêu cầu.\n3. Chờ danh sách nạp lại.',
     'Mã phiếu yêu cầu: 0356',
     '- Danh sách chỉ còn phiếu có mã phiếu yêu cầu chứa chuỗi 0356.'),
    ('007', 'Lọc theo Người yêu cầu', 'P0',
     'Nhân viên S đã lập 4 phiếu yêu cầu, cả 4 đã được duyệt.',
     '1. Chọn S ở ô Người yêu cầu.\n2. Chờ danh sách nạp lại.',
     'Người yêu cầu: S',
     '- Danh sách còn 4 phiếu hủy, cột Người yêu cầu đều là S.\n'
     '- ⚠️ Cột Người tạo có thể là người khác — đúng, vì S không phải người duyệt.'),
    ('008', 'Lọc theo Tên/mã hàng hóa bằng TÊN', 'P1',
     'Có phiếu hủy chứa hàng "Dầu thủy lực Eneos Super Hyrando 46".',
     '1. Gõ "Eneos" vào ô Tên/mã hàng hóa.\n2. Chờ danh sách nạp lại.',
     'Tên/mã hàng hóa: Eneos',
     '- Chỉ còn phiếu có ít nhất một dòng hàng chứa chữ Eneos trong tên hàng.'),
    ('009', 'Lọc theo Tên/mã hàng hóa bằng MÃ', 'P1',
     'Có phiếu hủy chứa hàng mã ENEO-700-V5023.',
     '1. Gõ "ENEO-700" vào ô Tên/mã hàng hóa.\n2. Chờ danh sách nạp lại.',
     'Tên/mã hàng hóa: ENEO-700',
     '- ⚠️ Vẫn ra kết quả dù đang gõ MÃ hàng chứ không phải tên — một ô tìm cả hai.'),
    ('010', 'Lọc khoảng ngày tạo hai đầu', 'P0',
     'Có 3 phiếu lập ngày 07/09/2026 và 2 phiếu lập ngày 08/09/2026.',
     '1. Chọn Ngày tạo từ = 07/09/2026.\n2. Chọn Ngày tạo đến = 08/09/2026.',
     'Ngày tạo từ: 07/09/2026; Ngày tạo đến: 08/09/2026',
     '- Danh sách có đúng 5 phiếu.\n'
     '- ⚠️ Cả hai ngày đầu mút đều được tính vào, không bị cắt.'),
    ('011', 'Lọc chỉ một đầu mút ngày', 'P1',
     'Có phiếu lập từ 2023 tới 08/09/2026.',
     '1. Chỉ chọn Ngày tạo từ = 08/09/2026, để trống Ngày tạo đến.',
     'Ngày tạo từ: 08/09/2026',
     '- Danh sách chỉ còn phiếu lập từ 08/09/2026 trở đi.'),
    ('012', 'Ô lọc Trạng thái với lựa chọn Đã đề nghị', 'P1',
     'Danh sách có 3,496 phiếu, tất cả đều Đã đề nghị.',
     '1. Chọn Trạng thái = Đã đề nghị.',
     'Trạng thái: Đã đề nghị',
     '- Danh sách giữ nguyên 3,496 phiếu.'),
    ('013', 'Ô lọc Trạng thái với hai lựa chọn còn lại luôn rỗng', 'P2',
     'Danh sách có 3,496 phiếu.',
     '1. Chọn Trạng thái = Chờ duyệt.\n2. Đọc kết quả.\n3. Chọn Trạng thái = Đang tạo.',
     'Trạng thái: Chờ duyệt, rồi Đang tạo',
     '- ⚠️ Cả hai lựa chọn đều cho danh sách RỖNG. Đây là đúng thiết kế (giữ đủ ba lựa chọn cho '
     'khớp hệ thống cũ), KHÔNG ghi Failed.'),
    ('014', 'Nút Làm mới xóa hết điều kiện lọc', 'P0',
     'Đang áp bộ lọc Người tạo + khoảng ngày + đang sắp xếp theo Ngày tạo tăng dần.',
     '1. Bấm Làm mới.\n2. Quan sát các ô lọc và thứ tự bảng.',
     '—',
     '- Mọi ô lọc trở về trống, kể cả ô tìm nhanh.\n'
     '- Thứ tự sắp xếp trở về mặc định (mới nhất trước).\n'
     '- Danh sách tự nạp lại đầy đủ từ trang 1.'),
    ('015', 'Bộ lọc được nhớ khi quay lại màn trong 10 phút', 'P1',
     'Vừa lọc Người tạo = DNS Admin ở màn danh sách.',
     '1. Mở một phiếu chi tiết.\n2. Bấm Quay lại.\n3. Quan sát ô lọc.',
     '—',
     '- Ô Người tạo vẫn giữ giá trị DNS Admin.\n'
     '- Danh sách vẫn đang lọc theo điều kiện cũ.\n'
     '- Trạng thái đóng/mở của khu vực Tìm kiếm nâng cao cũng được giữ.'),
    ('016', 'Cài đặt bộ lọc — tắt bớt ô lọc', 'P1',
     'Khu vực lọc nâng cao đang hiện đủ 7 ô.',
     '1. Bấm Cài đặt bộ lọc.\n2. Bỏ tích ô "Tên/mã hàng hóa".\n3. Bấm Lưu.',
     '—',
     '- Cửa sổ đóng lại.\n'
     '- Khu vực lọc nâng cao còn 6 ô, không còn ô Tên/mã hàng hóa.\n'
     '- Thoát ra vào lại màn thì cấu hình vẫn được giữ.'),
    ('017', 'Cài đặt bộ lọc — khôi phục mặc định', 'P2',
     'Đang tắt bớt 2 ô lọc.',
     '1. Bấm Cài đặt bộ lọc.\n2. Bấm Khôi phục mặc định.\n3. Bấm Lưu.',
     '—',
     '- Khu vực lọc nâng cao trở lại đủ 7 ô theo thứ tự gốc.'),
]

S3 = [
    ('001', 'Sắp xếp theo Mã phiếu tăng dần rồi giảm dần', 'P0',
     'Danh sách có ít nhất 30 phiếu.',
     '1. Bấm tiêu đề cột Mã phiếu.\n2. Đọc thứ tự.\n3. Bấm lần nữa.',
     '—',
     '- Lần 1: mã phiếu tăng dần.\n'
     '- Lần 2: mã phiếu giảm dần.\n'
     '- Cả hai lần đều quay về trang 1 và giữ nguyên bộ lọc.'),
    ('002', 'Sắp xếp theo Ngày tạo', 'P1',
     'Danh sách có phiếu của nhiều ngày khác nhau.',
     '1. Bấm tiêu đề cột Ngày tạo.\n2. Đọc thứ tự ngày.',
     '—',
     '- Danh sách sắp theo ngày tạo tăng dần, sau đó giảm dần khi bấm lại.'),
    ('003', 'Sắp xếp theo Ngày cập nhật', 'P2',
     'Danh sách có ít nhất 30 phiếu.',
     '1. Bấm tiêu đề cột Ngày cập nhật hai lần.',
     '—',
     '- Thứ tự đảo chiều đúng.\n'
     '- ⚠️ Với phiếu hủy, Ngày cập nhật luôn trùng Ngày tạo vì phiếu không sửa được.'),
    ('004', 'Các cột KHÔNG sắp xếp được', 'P2',
     'Danh sách có ít nhất 10 phiếu.',
     '1. Bấm lần lượt tiêu đề các cột Phiếu yêu cầu, Người yêu cầu, Người tạo, Trạng thái.',
     '—',
     '- Bốn cột này không có mũi tên sắp xếp và bấm vào không đổi thứ tự.\n'
     '- Chỉ ba cột Mã phiếu, Ngày tạo, Ngày cập nhật sắp xếp được.'),
    ('005', 'Đổi số dòng mỗi trang', 'P0',
     'Danh sách có 3,496 phiếu, đang để 10 dòng/trang.',
     '1. Đổi "Số dòng/trang" sang 50.\n2. Đọc ô thống kê.',
     'Số dòng/trang: 50',
     '- Bảng hiện 50 dòng.\n'
     '- Ô thống kê ghi "Hiển thị 1–50 / 3,496".\n'
     '- Quay về trang 1.'),
    ('006', 'Chuyển trang giữ nguyên bộ lọc', 'P0',
     'Đang lọc Người tạo = DNS Admin, kết quả nhiều hơn 1 trang.',
     '1. Sang trang 2.\n2. Đọc cột Người tạo và ô lọc.',
     '—',
     '- Ô lọc vẫn là DNS Admin.\n'
     '- Mọi dòng trang 2 đều do DNS Admin lập.\n'
     '- Số thứ tự tiếp tục liên tục (11, 12, ...).'),
    ('007', 'Số thứ tự liên tục qua các trang', 'P1',
     'Đang để 10 dòng/trang.',
     '1. Đọc STT dòng cuối trang 1.\n2. Sang trang 2, đọc STT dòng đầu.',
     '—',
     '- Trang 1 dòng cuối là 10, trang 2 dòng đầu là 11.'),
    ('008', 'Tuỳ chỉnh cột — bật cột Khách hàng và Ghi chú', 'P1',
     'Hai cột này đang tắt mặc định.',
     '1. Bấm nút Cấu hình cột hiển thị.\n2. Tích Khách hàng và Ghi chú.\n3. Bấm Lưu.',
     '—',
     '- Bảng hiện thêm 2 cột với dữ liệu đúng.\n'
     '- Phiếu không có ghi chú thì ô để TRỐNG, không có dấu gạch ngang.'),
    ('009', 'Tuỳ chỉnh cột — không tắt được cột khóa', 'P1',
     'Đang mở cửa sổ Cấu hình cột hiển thị.',
     '1. Thử bỏ tích cột STT.\n2. Thử bỏ tích cột Mã phiếu.\n3. Thử bỏ tích cột Hành động.',
     '—',
     '- Cả ba cột đều không bỏ tích được, luôn giữ trạng thái bật.'),
]

S4 = [
    ('001', 'Vào màn lập phiếu từ nút Tạo mới (không kèm phiếu yêu cầu)', 'P0',
     'Tài khoản B có quyền Quản lý giữ hàng.',
     '1. Ở màn danh sách bấm Tạo mới.\n2. Quan sát form.',
     '—',
     '- Tiêu đề màn là "Lập phiếu hủy hàng giữ".\n'
     '- Ô "Phiếu yêu cầu hủy hàng giữ" trống, hiện gợi ý "Chưa chọn phiếu yêu cầu".\n'
     '- Ba ô Người yêu cầu, Phòng ban yêu cầu, Khách hàng đều trống và hiện gợi ý "Tự điền theo '
     'phiếu yêu cầu".\n'
     '- Khối Chi tiết hiện dòng "Chưa chọn phiếu yêu cầu".\n'
     '- ⚠️ Nút Duyệt và Duyệt và tiếp tục CHƯA hiện.\n'
     '- Màn lập phiếu KHÔNG có ô Mã phiếu và ô Kho.'),
    ('002', 'Vào màn lập phiếu từ màn Yêu cầu hủy hàng giữ (kèm sẵn phiếu yêu cầu)', 'P0',
     'Phiếu yêu cầu PYCHHG-03569 đang Chờ duyệt; tài khoản B có quyền Quản lý giữ hàng.',
     '1. Mở chi tiết phiếu yêu cầu PYCHHG-03569.\n'
     '2. Bấm nút "Tạo phiếu hủy hàng giữ" ở cuối màn.\n'
     '3. Quan sát form vừa mở.',
     '—',
     '- Mở thẳng màn Lập phiếu hủy hàng giữ với phiếu yêu cầu đã được điền sẵn.\n'
     '- Bảng chi tiết đã nạp sẵn hàng hóa.\n'
     '- ⚠️ Nút "Duyệt và tiếp tục" KHÔNG hiện ở lối vào này, chỉ có nút Duyệt.\n'
     '- Đây là lối vào thứ hai của cùng một màn, phải test riêng.'),
    ('003', 'Chọn phiếu yêu cầu thì form được điền sẵn', 'P0',
     'Phiếu yêu cầu PYCHHG-03569 do DNS Admin lập, khách hàng 29TPHPHO-189, phòng ban "PHÒNG '
     'THIẾT BỊ Ô TÔ 3", có 1 dòng hàng đề nghị hủy 1.',
     '1. Bấm Tạo mới.\n2. Bấm nút tra cứu.\n3. Bấm vào dòng PYCHHG-03569.',
     '—',
     '- Ô Phiếu yêu cầu ghi PYCHHG-03569.\n'
     '- Ô Người yêu cầu ghi DNS Admin; Phòng ban yêu cầu ghi PHÒNG THIẾT BỊ Ô TÔ 3; Khách hàng '
     'ghi 29TPHPHO-189 kèm tên đầy đủ.\n'
     '- Bảng chi tiết có 1 dòng, cột Yêu cầu hủy = 1, ô Duyệt hủy điền sẵn 1, ô Cần hủy đã tích.\n'
     '- Nút Duyệt và Duyệt và tiếp tục hiện ra.'),
    ('004', 'Ba ô thông tin lấy từ phiếu yêu cầu bị khóa', 'P1',
     'Đã chọn một phiếu yêu cầu.',
     '1. Thử bấm và gõ vào ô Người yêu cầu.\n2. Làm tương tự với Phòng ban yêu cầu và Khách hàng.',
     'Gõ thử: TEST',
     '- Cả ba ô đều không gõ được, hiển thị kiểu ô khóa.\n'
     '- Giá trị không đổi.'),
    ('005', 'Ô Phiếu yêu cầu không gõ tay được', 'P1',
     'Đang ở màn lập phiếu, chưa chọn phiếu yêu cầu.',
     '1. Bấm vào ô Phiếu yêu cầu hủy hàng giữ và gõ "PYCHHG-03569".',
     'Gõ thử: PYCHHG-03569',
     '- Ô không nhận ký tự nào.\n'
     '- Chỉ chọn được qua cửa sổ tra cứu.'),
    ('006', 'Cột Có thể hủy được tính lại tại thời điểm mở form', 'P0',
     'Phiếu yêu cầu W đề nghị hủy 5 cái hàng H. Sau khi lập phiếu yêu cầu, hàng giữ của H đã bị '
     'giảm còn 3 do một chứng từ khác.',
     '1. Chọn phiếu yêu cầu W.\n2. Đọc cột Có thể hủy và cột Yêu cầu hủy.',
     '—',
     '- Cột Yêu cầu hủy ghi 5.\n'
     '- ⚠️ Cột Có thể hủy ghi 3, KHÔNG phải 5 — số được tính lại theo hàng giữ hiện tại.'),
    ('007', 'Duyệt hủy được phép LỚN HƠN Yêu cầu hủy', 'P0',
     'Phiếu yêu cầu V đề nghị hủy 3 cái hàng H; hàng giữ còn lại của người lập V là 4 (cột Có '
     'thể hủy = 4).',
     '1. Chọn phiếu yêu cầu V.\n2. Sửa ô Duyệt hủy thành 4.\n3. Bấm Duyệt và xác nhận.',
     'Duyệt hủy: 4',
     '- ⚠️ Lưu THÀNH CÔNG. Không có lỗi nào về việc vượt số đề nghị.\n'
     '- Đây là hành vi ĐÚNG theo thiết kế — đừng ghi Failed.\n'
     '- Hàng giữ bị trừ 4.'),
    ('008', 'Duyệt hủy vượt quá Có thể hủy bị chặn', 'P0',
     'Phiếu yêu cầu V có 1 dòng hàng, cột Có thể hủy = 2.',
     '1. Chọn phiếu yêu cầu V.\n2. Gõ 3 vào ô Duyệt hủy.\n3. Quan sát ngay dưới ô.',
     'Duyệt hủy: 3',
     '- Hiện chữ đỏ "Không được vượt 2" ngay dưới ô.\n'
     '- ⚠️ Ô vẫn giữ nguyên số 3 người dùng vừa gõ — phần mềm KHÔNG tự kéo về 2.\n'
     '- Bấm Duyệt lúc này thì không gọi lưu.'),
    ('009', 'Bỏ tích Cần hủy thì khóa ô Duyệt hủy', 'P0',
     'Đã chọn phiếu yêu cầu có 2 dòng hàng.',
     '1. Bỏ tích ô Cần hủy ở dòng 1.\n2. Quan sát dòng đó.',
     '—',
     '- Dòng 1 bị làm mờ.\n'
     '- Ô Duyệt hủy của dòng 1 bị khóa, không gõ được.\n'
     '- Lỗi đỏ đang treo ở dòng đó (nếu có) biến mất.'),
    ('010', 'Bỏ tích hết mọi dòng thì không lưu được', 'P0',
     'Đã chọn phiếu yêu cầu có 2 dòng hàng.',
     '1. Bỏ tích Cần hủy ở cả 2 dòng.\n2. Bấm Duyệt.',
     '—',
     '- Phần mềm báo phải chọn ít nhất 1 hàng hoá cần hủy với số lượng lớn hơn 0.\n'
     '- Không hiện hộp thoại xác nhận, không lưu.'),
    ('011', 'Hộp thoại xác nhận trước khi lưu', 'P0',
     'Đã chọn phiếu yêu cầu và nhập số hợp lệ.',
     '1. Bấm Duyệt.\n2. Đọc nội dung hộp thoại.',
     '—',
     '- Hộp thoại tiêu đề "Xác nhận duyệt".\n'
     '- Nội dung nêu rõ: lập phiếu hủy sẽ TRỪ TỒN HÀNG GIỮ ngay lập tức và không thể hoàn tác.\n'
     '- Nút xác nhận ghi "Duyệt", màu xanh kèm dấu tích.\n'
     '- ⚠️ Nút xác nhận KHÔNG được màu đỏ và không có biểu tượng thùng rác.'),
    ('012', 'Bấm Hủy trên hộp thoại xác nhận', 'P0',
     'Đang mở hộp thoại xác nhận, ô Ghi chú đã gõ "ghi chú 001".',
     '1. Bấm Hủy.\n2. Quan sát form.',
     'Ghi chú: ghi chú 001',
     '- Hộp thoại đóng lại.\n'
     '- KHÔNG có phiếu hủy nào được tạo, số phiếu ở màn danh sách không đổi.\n'
     '- Hàng giữ không bị trừ.\n'
     '- Dữ liệu đang nhập vẫn còn nguyên, ô Ghi chú vẫn là "ghi chú 001".'),
    ('013', 'Lập phiếu thành công — kết quả trên phiếu hủy', 'P0',
     'Phiếu yêu cầu PYCHHG-03569 đang Chờ duyệt, 1 dòng hàng, Có thể hủy = 2, Yêu cầu hủy = 1.',
     '1. Chọn phiếu yêu cầu.\n2. Gõ Ghi chú "duyệt hủy 001".\n3. Bấm Duyệt và xác nhận.',
     'Duyệt hủy: 1; Ghi chú: duyệt hủy 001',
     '- Hiện thông báo "Duyệt phiếu thành công".\n'
     '- Quay về màn DANH SÁCH, không ở lại màn chi tiết.\n'
     '- Dòng mới nhất có mã dạng PHHG-NNNNN, Trạng thái Đã đề nghị, cột Phiếu yêu cầu ghi '
     'PYCHHG-03569, Ghi chú ghi "duyệt hủy 001".'),
    ('014', 'Lập phiếu thành công — kết quả trên phiếu YÊU CẦU', 'P0',
     'Vừa lập phiếu hủy từ phiếu yêu cầu PYCHHG-03569.',
     '1. Vào Tài chính → Giữ hàng → Yêu cầu hủy hàng giữ.\n'
     '2. Mở chi tiết PYCHHG-03569.',
     '—',
     '- Phiếu yêu cầu chuyển sang trạng thái Đã duyệt.\n'
     '- Có ghi nhận người duyệt và thời điểm duyệt.\n'
     '- Không còn nút "Tạo phiếu hủy hàng giữ".'),
    ('015', 'Lập phiếu thành công — hàng giữ bị trừ đúng', 'P0',
     'Trước khi duyệt, hàng H của nhân viên S cho khách K còn 10 (xem ở màn Danh sách hàng giữ). '
     'Phiếu yêu cầu của S đề nghị hủy 4.',
     '1. Ghi lại số hàng giữ của H trước khi duyệt.\n'
     '2. Lập phiếu hủy với Duyệt hủy = 4.\n'
     '3. Mở lại màn Danh sách hàng giữ, tìm hàng H của S cho khách K.',
     'Duyệt hủy: 4',
     '- Số hàng giữ của H còn 6.\n'
     '- ⚠️ Trừ theo NGƯỜI LẬP PHIẾU YÊU CẦU (S), không phải người lập phiếu hủy.'),
    ('016', 'Trừ hàng giữ theo thứ tự hạn giữ sớm trước', 'P0',
     'Hàng H của S cho khách K nằm trên 2 lô: lô hạn 30/09/2026 còn 3, lô hạn 31/12/2026 còn 5.',
     '1. Lập phiếu hủy với Duyệt hủy = 4.\n'
     '2. Mở lịch sử giữ hàng của hàng H.',
     'Duyệt hủy: 4',
     '- Lô hạn 30/09/2026 bị trừ hết 3, còn 0.\n'
     '- Lô hạn 31/12/2026 bị trừ 1, còn 4.\n'
     '- ⚠️ Lô hết hạn sớm hơn phải bị trừ trước.'),
    ('017', 'Nút "Duyệt và tiếp tục"', 'P1',
     'Có ít nhất 2 phiếu yêu cầu đang Chờ duyệt. Đang ở màn lập phiếu vào từ nút Tạo mới.',
     '1. Chọn phiếu yêu cầu thứ nhất.\n2. Bấm "Duyệt và tiếp tục".\n3. Xác nhận trên hộp thoại.',
     '—',
     '- Phiếu thứ nhất được lập thành công.\n'
     '- ⚠️ Vẫn Ở LẠI màn lập phiếu (không về danh sách) để chọn phiếu yêu cầu kế tiếp.\n'
     '- Form được dọn trống để chọn phiếu mới.\n'
     '- ⚠️ Nút này chạy đúng luồng duyệt, KHÔNG phải lưu nháp — hàng giữ đã bị trừ ngay.'),
    ('018', 'Cảnh báo khi rời màn lúc chưa lưu', 'P1',
     'Đã chọn phiếu yêu cầu và sửa ô Ghi chú nhưng chưa bấm Duyệt.',
     '1. Bấm Quay lại (hoặc chuyển sang menu khác).',
     'Ghi chú: chưa lưu',
     '- Phần mềm cảnh báo dữ liệu chưa được lưu và hỏi có rời đi không.\n'
     '- Chọn ở lại thì vẫn giữ nguyên dữ liệu đang nhập.'),
]

S5 = [
    ('001', 'Cửa sổ chọn phiếu yêu cầu chỉ liệt kê phiếu Chờ duyệt', 'P0',
     'Công ty 1 có 8 phiếu yêu cầu Chờ duyệt, 12 phiếu Đang tạo và 3,412 phiếu Đã duyệt.',
     '1. Bấm Tạo mới.\n2. Bấm nút tra cứu phiếu yêu cầu.\n3. Đếm số dòng.',
     '—',
     '- Cửa sổ có đúng 8 dòng.\n'
     '- Không có phiếu nào ở trạng thái Đang tạo hoặc Đã duyệt.'),
    ('002', 'Cửa sổ chỉ liệt kê phiếu trong CÙNG CÔNG TY', 'P0',
     'Tài khoản B thuộc công ty 1 và có quyền xem theo tổng công ty. Công ty 1 có 8 phiếu chờ '
     'duyệt, công ty 4 có 5 phiếu chờ duyệt.',
     '1. Đăng nhập bằng B.\n2. Mở cửa sổ chọn phiếu yêu cầu.\n3. Đếm số dòng.',
     '—',
     '- ⚠️ Chỉ có 8 dòng của công ty 1, KHÔNG có phiếu của công ty 4 dù B xem được toàn tổng '
     'công ty. Đây là đúng thiết kế.'),
    ('003', 'Tiêu đề cột của cửa sổ', 'P1',
     'Cửa sổ đang mở và có dữ liệu.',
     '1. Đọc tiêu đề các cột.',
     '—',
     '- Đúng 5 cột: STT, Mã phiếu, Người tạo, Khách hàng, Ngày tạo.\n'
     '- Cột thứ ba ghi "Người tạo" và cột thứ năm ghi "Ngày tạo".'),
    ('004', 'Bấm bất kỳ đâu trên dòng là chọn', 'P0',
     'Cửa sổ đang mở, có ít nhất 1 dòng.',
     '1. Bấm vào ô Khách hàng của dòng đầu tiên (không bấm vào mã phiếu).',
     '—',
     '- ⚠️ Cửa sổ đóng lại và phiếu đó được chọn.\n'
     '- Không cần bấm đúng một nút nào.'),
    ('005', 'Lọc trong cửa sổ theo Mã phiếu', 'P1',
     'Cửa sổ đang liệt kê 8 phiếu, trong đó có PYCHHG-03569.',
     '1. Gõ "03569" vào ô lọc Mã phiếu.\n2. Chờ danh sách nạp lại.',
     'Mã phiếu: 03569',
     '- Chỉ còn dòng PYCHHG-03569.'),
    ('006', 'Lọc trong cửa sổ theo Người tạo', 'P1',
     'Trong 8 phiếu chờ duyệt có 3 phiếu do DNS Admin lập.',
     '1. Chọn DNS Admin ở ô lọc Người tạo.',
     'Người tạo: DNS Admin',
     '- Còn đúng 3 dòng, cột Người tạo đều là DNS Admin.'),
    ('007', 'Cửa sổ rỗng khi không còn phiếu chờ duyệt', 'P1',
     'Đã duyệt hết mọi phiếu yêu cầu của công ty; không còn phiếu nào Chờ duyệt.',
     '1. Bấm Tạo mới.\n2. Mở cửa sổ chọn phiếu yêu cầu.',
     '—',
     '- Cửa sổ hiện trạng thái rỗng, không có dòng nào.\n'
     '- Không có thông báo lỗi.'),
    ('008', 'Đóng cửa sổ mà không chọn', 'P2',
     'Cửa sổ đang mở.',
     '1. Bấm nút đóng của cửa sổ.',
     '—',
     '- Cửa sổ đóng, ô Phiếu yêu cầu vẫn trống.\n'
     '- Nút Duyệt vẫn chưa hiện.'),
]

S6 = [
    ('001', 'Nội dung khối Thông tin chung ở màn chi tiết', 'P0',
     'Phiếu PHHG-03501 sinh từ PYCHHG-03567, người yêu cầu DNS Admin, phòng ban PHÒNG THIẾT BỊ '
     'Ô TÔ 3, khách hàng 29TPHPPH-6, ghi chú "test update".',
     '1. Mở chi tiết PHHG-03501.\n2. Đọc từng ô của khối Thông tin chung.',
     '—',
     '- Ô Mã phiếu ghi PHHG-03501.\n'
     '- Ô Phiếu yêu cầu ghi PYCHHG-03567.\n'
     '- Ô Người yêu cầu, Phòng ban yêu cầu, Khách hàng, Ghi chú đúng dữ liệu.\n'
     '- Góc phải ghi "Người tạo: ... · dd/mm/yyyy hh:mm".'),
    ('002', 'Ô Kho ở màn chi tiết để trống', 'P1',
     'Phiếu PHHG-03501.',
     '1. Mở chi tiết.\n2. Đọc ô Kho.',
     '—',
     '- ⚠️ Ô Kho TRỐNG. Đây là ĐÚNG, không phải lỗi — hàng giữ tính theo nhân viên chứ không '
     'gắn kho. Không ghi Failed.\n'
     '- Ô để trống hoàn toàn, không có dấu gạch ngang.'),
    ('003', 'Bảng chi tiết ở màn xem khác màn lập phiếu', 'P0',
     'Phiếu PHHG-03501 có 1 dòng hàng.',
     '1. Mở chi tiết.\n2. Đọc tiêu đề các cột của bảng Chi tiết.',
     '—',
     '- Có các cột: STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, Yêu cầu hủy, Duyệt hủy, '
     'ĐVT.\n'
     '- ⚠️ KHÔNG có cột "Cần hủy" và KHÔNG có cột "Có thể hủy" — hai cột này chỉ có ở màn lập '
     'phiếu.'),
    ('004', 'Màn chi tiết không có nút Sửa và Xóa', 'P0',
     'Phiếu PHHG-03501 do chính người đang đăng nhập lập.',
     '1. Mở chi tiết.\n2. Đọc các nút ở cuối màn.',
     '—',
     '- Chỉ có 2 nút: In và Quay lại.\n'
     '- ⚠️ KHÔNG có nút Sửa, Xóa, Hủy duyệt — kể cả với phiếu do chính mình vừa lập.'),
    ('005', 'Mọi ô trên màn chi tiết đều chỉ đọc', 'P1',
     'Đang mở chi tiết một phiếu.',
     '1. Thử gõ vào ô Ghi chú.\n2. Thử gõ vào ô Duyệt hủy trong bảng.',
     'Gõ thử: TEST',
     '- Không ô nào nhận ký tự.\n'
     '- Ô Duyệt hủy hiện dưới dạng chữ, không phải ô nhập.'),
    ('006', 'Mở phiếu ngoài phạm vi quyền bằng đường dẫn trực tiếp', 'P0',
     'Tài khoản D thuộc công ty 1, chỉ có quyền xem theo công ty. Phiếu Y thuộc công ty 4 và '
     'không liên quan tới D.',
     '1. Đăng nhập bằng D.\n'
     '2. Gõ thẳng đường dẫn chi tiết của phiếu Y lên thanh địa chỉ.',
     '—',
     '- ⚠️ Phần mềm báo không có quyền xem phiếu này và không hiển thị dữ liệu phiếu.\n'
     '- Không bị treo trang.'),
]

S7 = [
    ('001', 'In từ cột Hành động ở danh sách', 'P0',
     'Phiếu PHHG-03501 tồn tại.',
     '1. Ở dòng PHHG-03501 bấm nút In.',
     '—',
     '- Mở CỬA SỔ xem trước ngay trên màn, tiêu đề "Xem trước phiếu PHHG-03501".\n'
     '- ⚠️ KHÔNG mở tab mới của trình duyệt.'),
    ('002', 'In từ màn chi tiết', 'P0',
     'Đang mở chi tiết PHHG-03501.',
     '1. Bấm nút In ở cuối màn.',
     '—',
     '- Mở cửa sổ xem trước "Xem trước phiếu hủy hàng giữ".\n'
     '- Nút In là nút trắng (hành động phụ), không phải nút màu chính.'),
    ('003', 'Nội dung bản in', 'P0',
     'Phiếu PHHG-03501, sinh từ PYCHHG-03567, khách hàng 29TPHPPH-6.',
     '1. Mở cửa sổ xem trước.\n2. Đọc nội dung.',
     '—',
     '- Tiêu đề "PHIẾU HỦY HÀNG GIỮ".\n'
     '- Có đủ: Số phiếu, Ngày tạo, Phiếu yêu cầu, Người yêu cầu, Phòng ban, Khách hàng, Kho, '
     'Người tạo, bảng hàng hóa và ghi chú.\n'
     '- Dòng Kho để trống hoặc dấu chấm lửng, đúng như dữ liệu.'),
    ('004', 'Tiêu đề công ty trên bản in', 'P1',
     'Phiếu X thuộc công ty 4; người đăng nhập thuộc công ty 1.',
     '1. Mở bản in của phiếu X.\n2. Đọc phần tiêu đề đầu trang.',
     '—',
     '- ⚠️ Tiêu đề là của CÔNG TY 4 (công ty ghi trên phiếu), không phải công ty của người đang '
     'đăng nhập.'),
    ('005', 'Đóng cửa sổ xem trước', 'P2',
     'Cửa sổ xem trước đang mở.',
     '1. Bấm nút đóng.',
     '—',
     '- Cửa sổ đóng, quay lại đúng màn trước đó, không mất bộ lọc.'),
]

S8 = [
    ('001', 'Mở cửa sổ chọn trường xuất', 'P0',
     'Bảng đang hiện 10 cột mặc định.',
     '1. Bấm nút Xuất Excel.',
     '—',
     '- Cửa sổ "Chọn trường xuất Excel" mở ra.\n'
     '- ⚠️ Các trường tương ứng với cột đang hiện trên bảng đã được TÍCH SẴN.'),
    ('002', 'Danh sách trường xuất', 'P1',
     'Cửa sổ chọn trường đang mở.',
     '1. Đọc danh sách trường.',
     '—',
     '- Có 10 trường: Mã phiếu, Phiếu yêu cầu, Người yêu cầu, Người tạo, Ngày tạo, Trạng thái, '
     'Người cập nhật, Ngày cập nhật, Khách hàng, Ghi chú.'),
    ('003', 'Xuất file theo bộ lọc đang áp', 'P0',
     'Đang lọc Người tạo = DNS Admin, kết quả 120 phiếu.',
     '1. Bấm Xuất Excel.\n2. Bấm Xuất file.\n3. Mở tệp vừa tải.',
     '—',
     '- Tệp có đúng 120 dòng dữ liệu.\n'
     '- Mọi dòng đều có Người tạo là DNS Admin.\n'
     '- Hiện thông báo "Xuất Excel thành công".'),
    ('004', 'Thứ tự cột trong tệp theo thứ tự tích chọn', 'P1',
     'Cửa sổ chọn trường đang mở, chưa tích gì.',
     '1. Bấm Bỏ chọn hết.\n2. Tích lần lượt: Ghi chú, rồi Mã phiếu, rồi Người tạo.\n'
     '3. Bấm Xuất file và mở tệp.',
     '—',
     '- Cột trong tệp theo đúng thứ tự: STT, Ghi chú, Mã phiếu, Người tạo.'),
    ('005', 'Định dạng ô ngày trong tệp', 'P1',
     'Tệp vừa xuất có cột Ngày tạo.',
     '1. Mở tệp và xem cột Ngày tạo.',
     '—',
     '- Ngày hiển thị dạng dd/mm/yyyy hh:mm.\n'
     '- Ô căn giữa, không bị Excel gắn cờ cảnh báo.'),
    ('006', 'Chống bấm hai lần nút Xuất', 'P2',
     'Bộ lọc đang cho ra nhiều nghìn dòng.',
     '1. Bấm Xuất file.\n2. Bấm Xuất file lần nữa ngay lập tức.',
     '—',
     '- Nút bị khóa trong lúc đang xuất, lần bấm thứ hai không có tác dụng.\n'
     '- Chỉ tải về đúng 1 tệp.'),
    ('007', 'Phạm vi quyền áp cho cả tệp xuất', 'P0',
     'Tài khoản D chỉ xem được công ty 1 (3,100 phiếu). Toàn hệ thống có 3,496 phiếu.',
     '1. Đăng nhập bằng D.\n2. Không áp bộ lọc nào, bấm Xuất Excel rồi Xuất file.\n'
     '3. Đếm số dòng trong tệp.',
     '—',
     '- ⚠️ Tệp chỉ có 3,100 dòng, không lộ phiếu của công ty khác.'),
]

S9 = [
    ('001', 'Ô Duyệt hủy bỏ trống', 'P0',
     'Đã chọn phiếu yêu cầu, dòng 1 đang tích Cần hủy.',
     '1. Xóa sạch nội dung ô Duyệt hủy của dòng 1.\n2. Bấm ra ngoài ô.',
     'Duyệt hủy: (để trống)',
     '- Hiện chữ đỏ "Chưa nhập số lượng" ngay dưới ô.'),
    ('002', 'Ô Duyệt hủy nhập chữ', 'P0',
     'Đã chọn phiếu yêu cầu.',
     '1. Gõ "abc" vào ô Duyệt hủy.',
     'Duyệt hủy: abc',
     '- Hiện chữ đỏ "Chỉ được nhập số".'),
    ('003', 'Ô Duyệt hủy nhập 0', 'P0',
     'Đã chọn phiếu yêu cầu.',
     '1. Gõ 0 vào ô Duyệt hủy.',
     'Duyệt hủy: 0',
     '- Hiện chữ đỏ "Phải lớn hơn 0".'),
    ('004', 'Ô Duyệt hủy nhập số âm', 'P1',
     'Đã chọn phiếu yêu cầu.',
     '1. Gõ -1 vào ô Duyệt hủy.',
     'Duyệt hủy: -1',
     '- Hiện chữ đỏ, không cho lưu.\n'
     '- Ô vẫn giữ nguyên nội dung vừa gõ.'),
    ('005', 'Ô Duyệt hủy đang gõ dở phần thập phân', 'P2',
     'Đã chọn phiếu yêu cầu, Có thể hủy = 5.',
     '1. Gõ "2." vào ô Duyệt hủy rồi dừng lại.',
     'Duyệt hủy: 2.',
     '- ⚠️ CHƯA báo lỗi ngay khi vừa gõ dấu chấm (tránh nháy lỗi khi đang gõ).\n'
     '- Chỉ khi bấm Duyệt mới báo lỗi nếu vẫn để dở.'),
    ('006', 'Bấm Duyệt khi còn ô lỗi', 'P0',
     'Bảng chi tiết có 10 dòng, dòng thứ 7 đang có lỗi đỏ.',
     '1. Bấm Duyệt.',
     '—',
     '- Hiện thông báo "Bạn chưa nhập đầy đủ thông tin.".\n'
     '- ⚠️ Màn hình tự cuộn tới dòng thứ 7 là dòng lỗi đầu tiên.\n'
     '- KHÔNG hiện hộp thoại xác nhận, KHÔNG lưu.'),
    ('007', 'Ghi chú vượt 255 ký tự', 'P1',
     'Đã chọn phiếu yêu cầu.',
     '1. Dán một đoạn 300 ký tự vào ô Ghi chú.\n2. Bấm Duyệt và xác nhận.',
     'Ghi chú: chuỗi 300 ký tự',
     '- Phần mềm báo Ghi chú không được vượt quá 255 ký tự.\n'
     '- Không lưu.'),
    ('008', 'Bỏ trống Ghi chú vẫn lưu được', 'P1',
     'Đã chọn phiếu yêu cầu, số lượng hợp lệ.',
     '1. Để trống ô Ghi chú.\n2. Bấm Duyệt và xác nhận.',
     'Ghi chú: (để trống)',
     '- Lưu thành công.\n'
     '- Cột Ghi chú ngoài danh sách để TRỐNG, không có dấu gạch ngang.'),
    ('009', 'Số lượng nhập nhiều chữ số', 'P2',
     'Hàng H có Có thể hủy = 1,500.',
     '1. Gõ 1000 vào ô Duyệt hủy.\n2. Bấm Duyệt và xác nhận.',
     'Duyệt hủy: 1000',
     '- Lưu thành công.\n'
     '- Số hiển thị lại theo chuẩn quốc tế: 1,000 (dấu phẩy ngăn hàng nghìn).'),
    ('010', 'Số lượng vượt 6 chữ số', 'P2',
     'Đã chọn phiếu yêu cầu.',
     '1. Gõ 1000000 vào ô Duyệt hủy.\n2. Bấm Duyệt.',
     'Duyệt hủy: 1000000',
     '- Bị chặn, phần mềm báo không được vượt quá 6 chữ số hoặc báo vượt số có thể hủy.\n'
     '- Không lưu.'),
]

S10 = [
    ('001', 'Hai người cùng duyệt một phiếu yêu cầu', 'P0',
     'Phiếu yêu cầu W đang Chờ duyệt. Hai tài khoản B1 và B2 đều có quyền Quản lý giữ hàng.',
     '1. B1 và B2 cùng mở màn lập phiếu và cùng chọn phiếu W.\n'
     '2. B1 bấm Duyệt và xác nhận, lưu thành công.\n'
     '3. B2 bấm Duyệt và xác nhận.',
     '—',
     '- B1 lưu thành công.\n'
     '- ⚠️ B2 nhận thông báo phiếu yêu cầu này không còn ở trạng thái chờ duyệt hoặc không đủ '
     'quyền duyệt.\n'
     '- Chỉ có ĐÚNG MỘT phiếu hủy được tạo cho W.\n'
     '- Hàng giữ chỉ bị trừ một lần.'),
    ('002', 'Hàng giữ bị người khác tiêu thụ hết trong lúc đang mở form', 'P0',
     'Phiếu yêu cầu W có hàng H, lúc mở form cột Có thể hủy = 5. Trong lúc đó một chứng từ khác '
     'lấy hết 5 cái hàng giữ này.',
     '1. Mở form và giữ nguyên không thao tác trong 5 phút.\n'
     '2. Nhờ người khác tiêu thụ hết hàng giữ của H.\n'
     '3. Quay lại bấm Duyệt với Duyệt hủy = 5 và xác nhận.',
     'Duyệt hủy: 5',
     '- ⚠️ Phần mềm báo hàng không đủ số lượng đang giữ.\n'
     '- KHÔNG tạo phiếu hủy nào.\n'
     '- KHÔNG trừ một phần.'),
    ('003', 'Phiếu nhiều dòng, một dòng thiếu hàng giữ', 'P0',
     'Phiếu yêu cầu W có 3 dòng hàng. Dòng 1 và 2 đủ hàng, dòng 3 chỉ còn 1 nhưng đang đặt Duyệt '
     'hủy = 5 do hàng vừa bị tiêu thụ.',
     '1. Bấm Duyệt và xác nhận.\n2. Kiểm tra hàng giữ của cả 3 hàng.',
     '—',
     '- Phần mềm báo lỗi ở hàng thiếu.\n'
     '- ⚠️ Hàng giữ của dòng 1 và 2 KHÔNG bị trừ — toàn bộ thao tác bị hủy bỏ, không trừ một '
     'phần.\n'
     '- Không có phiếu hủy nào được tạo.'),
    ('004', 'Phiếu yêu cầu bị người lập rút về nháp trong lúc đang mở form', 'P1',
     'Phiếu yêu cầu W đang Chờ duyệt và đã được mở ở màn lập phiếu hủy. Sau đó W bị Không duyệt, '
     'quay về trạng thái Đang tạo.',
     '1. Quay lại form đang mở, bấm Duyệt và xác nhận.',
     '—',
     '- Phần mềm báo phiếu yêu cầu không còn ở trạng thái chờ duyệt.\n'
     '- Không lưu, không trừ hàng giữ.'),
    ('005', 'Không tạo được hai phiếu hủy cho cùng một phiếu yêu cầu', 'P0',
     'Phiếu yêu cầu W đã được duyệt, sinh ra phiếu hủy X.',
     '1. Mở màn lập phiếu hủy, mở cửa sổ chọn phiếu yêu cầu.\n2. Tìm phiếu W.',
     '—',
     '- ⚠️ Phiếu W KHÔNG còn trong cửa sổ vì đã chuyển sang Đã duyệt.\n'
     '- Không có cách nào lập phiếu hủy thứ hai cho W qua giao diện.'),
    ('006', 'Cô lập dữ liệu giữa hai công ty khi lập phiếu', 'P1',
     'Tài khoản B thuộc công ty 1 có quyền Quản lý giữ hàng. Phiếu yêu cầu Z thuộc công ty 4 '
     'đang Chờ duyệt.',
     '1. Dùng công cụ kiểm thử API, đăng nhập bằng B.\n'
     '2. Gọi thẳng chức năng Lập phiếu hủy với mã phiếu yêu cầu Z.',
     '—',
     '- Phần mềm từ chối hoặc trả về lỗi không đủ quyền duyệt.\n'
     '- Hàng giữ của công ty 4 không bị trừ.'),
]

S11 = [
    ('001', 'Lịch sử ngay sau khi lập phiếu', 'P0',
     'Vừa lập phiếu hủy PHHG-03501, đã trừ hàng giữ trên 1 lô.',
     '1. Mở chi tiết PHHG-03501.\n2. Bấm "Xem lịch sử".',
     '—',
     '- Có đúng 1 mốc.\n'
     '- Mốc ghi thời điểm dạng dd/mm/yyyy hh:mm, tên thao tác "Tạo mới".\n'
     '- Dòng "Người thực hiện: {tên} - {phòng ban}".\n'
     '- Ghi chú "Đã trừ tồn hàng giữ trên 1 lô.".'),
    ('002', 'Số lô trong ghi chú lịch sử khớp thực tế', 'P1',
     'Phiếu hủy vừa lập trừ hàng trên 2 lô khác hạn giữ.',
     '1. Mở lịch sử của phiếu vừa lập.\n2. Đọc ghi chú.',
     '—',
     '- Ghi chú ghi "Đã trừ tồn hàng giữ trên 2 lô.".'),
    ('003', 'Lịch sử mở từ cột Hành động ngoài danh sách', 'P1',
     'Phiếu PHHG-03501 có lịch sử.',
     '1. Ở dòng PHHG-03501 bấm nút Lịch sử.',
     '—',
     '- Mở cửa sổ "Lịch sử phiếu hủy hàng giữ" kèm mã phiếu.\n'
     '- Nội dung giống khối lịch sử ở màn chi tiết.'),
    ('004', 'Khối lịch sử chỉ nạp khi bấm mở', 'P2',
     'Đang mở chi tiết một phiếu, khối Lịch sử đang thu gọn.',
     '1. Quan sát khối Lịch sử khi vừa vào màn.\n2. Bấm "Xem lịch sử".',
     '—',
     '- Lúc vừa vào màn khối đang thu gọn và chưa hiện dữ liệu.\n'
     '- Bấm mở thì mới nạp và hiện danh sách mốc.\n'
     '- Bấm "Thu gọn" thì đóng lại.'),
    ('005', 'Lịch sử phiếu YÊU CẦU cũng được ghi khi duyệt', 'P0',
     'Vừa lập phiếu hủy PHHG-A từ phiếu yêu cầu PYCHHG-B.',
     '1. Mở chi tiết phiếu yêu cầu PYCHHG-B.\n2. Xem lịch sử của nó.',
     '—',
     '- Có thêm một mốc duyệt mới nhất.\n'
     '- ⚠️ Ghi chú của mốc nêu rõ mã phiếu hủy đã sinh ra, dạng "Đã lập phiếu hủy hàng giữ '
     'PHHG-A.".'),
]

S12 = [
    ('001', 'Luồng đầu cuối: đề nghị → duyệt → hàng giữ giảm', 'P0',
     'Nhân viên S đang giữ 10 cái hàng H cho khách K. Tài khoản B có quyền Quản lý giữ hàng '
     'cùng công ty với S.',
     '1. Đăng nhập bằng S, lập phiếu yêu cầu hủy hàng giữ cho hàng H số lượng 4, gửi duyệt.\n'
     '2. Đăng nhập bằng B, vào Phiếu hủy hàng giữ, bấm Tạo mới.\n'
     '3. Chọn phiếu yêu cầu vừa gửi, giữ Duyệt hủy = 4, bấm Duyệt và xác nhận.\n'
     '4. Mở màn Danh sách hàng giữ, tìm hàng H của S cho khách K.\n'
     '5. Mở lại phiếu yêu cầu vừa gửi.',
     'Yêu cầu hủy: 4; Duyệt hủy: 4',
     '- Phiếu hủy được tạo, quay về danh sách và thấy dòng mới nhất.\n'
     '- Hàng giữ của H còn 6.\n'
     '- Phiếu yêu cầu chuyển sang Đã duyệt, có người duyệt và thời điểm duyệt.\n'
     '- S nhận được thông báo phiếu của mình đã được duyệt.\n'
     '- Cả phiếu hủy và phiếu yêu cầu đều có mốc lịch sử mới.'),
    ('002', 'Luồng đầu cuối: duyệt ít hơn số đề nghị', 'P0',
     'Nhân viên S giữ 10 cái hàng H. S đề nghị hủy 6.',
     '1. B chọn phiếu yêu cầu của S.\n2. Sửa Duyệt hủy từ 6 xuống 2.\n3. Duyệt và xác nhận.\n'
     '4. Kiểm tra hàng giữ và bảng chi tiết phiếu hủy.',
     'Yêu cầu hủy: 6; Duyệt hủy: 2',
     '- Hàng giữ của H còn 8 (bị trừ 2, không phải 6).\n'
     '- Bảng chi tiết phiếu hủy ghi Yêu cầu hủy = 6, Duyệt hủy = 2.\n'
     '- Phiếu yêu cầu vẫn chuyển sang Đã duyệt (không còn phần dư để duyệt tiếp).'),
    ('003', 'Luồng đầu cuối: hai phiếu yêu cầu liên tiếp bằng nút Duyệt và tiếp tục', 'P1',
     'Có 2 phiếu yêu cầu đang Chờ duyệt của hai nhân viên khác nhau.',
     '1. B bấm Tạo mới, chọn phiếu thứ nhất, bấm "Duyệt và tiếp tục", xác nhận.\n'
     '2. Chọn tiếp phiếu thứ hai, bấm Duyệt, xác nhận.\n'
     '3. Về màn danh sách.',
     '—',
     '- Sau bước 1 vẫn ở màn lập phiếu, form đã dọn trống.\n'
     '- Sau bước 2 quay về màn danh sách.\n'
     '- Danh sách có thêm đúng 2 phiếu hủy mới.\n'
     '- Cả 2 phiếu yêu cầu đều chuyển sang Đã duyệt.'),
    ('004', 'Luồng đầu cuối: từ chối rồi gửi lại rồi duyệt', 'P1',
     'Nhân viên S gửi duyệt phiếu yêu cầu cho hàng H số lượng 4.',
     '1. B mở phiếu yêu cầu, bấm Không duyệt kèm lý do "Sai số lượng".\n'
     '2. S sửa lại còn 2 rồi gửi duyệt lại.\n'
     '3. B vào màn Phiếu hủy hàng giữ, mở cửa sổ chọn phiếu yêu cầu.\n'
     '4. Chọn phiếu đó và duyệt với Duyệt hủy = 2.',
     'Lý do: Sai số lượng; Duyệt hủy: 2',
     '- Sau bước 1 phiếu yêu cầu về trạng thái Đang tạo và KHÔNG còn trong cửa sổ chọn.\n'
     '- ⚠️ Bước 1 KHÔNG trừ hàng giữ.\n'
     '- Sau bước 2 phiếu xuất hiện lại trong cửa sổ chọn.\n'
     '- Sau bước 4 hàng giữ bị trừ đúng 2 và phiếu hủy được tạo.'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP PHIẾU HỦY HÀNG GIỮ', S4),
    ('V', 'CHỌN PHIẾU YÊU CẦU TỪ CỬA SỔ TRA CỨU', S5),
    ('VI', 'XEM CHI TIẾT PHIẾU', S6),
    ('VII', 'IN PHIẾU', S7),
    ('VIII', 'XUẤT EXCEL', S8),
    ('IX', 'RÀNG BUỘC NHẬP LIỆU', S9),
    ('X', 'CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI', S10),
    ('XI', 'LỊCH SỬ THAY ĐỔI', S11),
    ('XII', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S12),
]

build(output_file=os.path.join(BASE, 'testcase - Phieu huy hang giu.xlsx'),
      sheet_name='Trang tính1',
      feature_name='Phiếu hủy hàng giữ',
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
