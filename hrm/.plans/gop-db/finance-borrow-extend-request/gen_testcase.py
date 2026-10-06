# -*- coding: utf-8 -*-
"""Sinh testcase cho man "Phieu yeu cau gia han hang muon" (phan he Tai chinh, nhom Muon hang).

Viet tu code HRM nhanh `gop_db` (nguon chan ly), khuon cau truc chep tu man sinh doi
`finance-prepick-extend-request/gen_testcase.py` nhung noi dung doi han:
hang MUON khong co nhap, khong sua/xoa, 1 o ngay hen tra moi cho ca phieu.
Ngon ngu: NGHIEP VU cho QA - khong dung thuat ngu code.

Ra soat lai 05/10/2026 theo code nhanh `develop` (repo chinh — cac sua QA tu 02/10 lam thang vao
develop): #11534 (tong cong ty thay moi cong ty), #11533 (goc phai khoi Thong tin chung, in phieu
kho doc, sap xep popup), #11529 (cau bao ly do khong gia han duoc), #11535 (popup qua han),
#11538 (toast thieu thong tin), #11550 (nguoi nhan thong bao TP = nguoi duyet duoc). 167 -> 171 TC.
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

MODULE = 'YC gia hạn hàng mượn'

MENU_ALL = ('Vào phân hệ Tài chính > nhóm "Hàng hoá - Dịch vụ - Vận chuyển" > "Mượn hàng" > bấm '
            '"Phiếu yêu cầu gia hạn hàng mượn".')
MENU_WAIT = ('Vào phân hệ Tài chính > nhóm "Chờ duyệt" > "Hàng mượn chờ duyệt" > bấm "Phiếu yêu cầu '
             'gia hạn hàng mượn chờ duyệt".')
MENU_SALE = ('Vào phân hệ Bán hàng > nhóm "Yêu cầu" > "Hàng hóa" > bấm "YC gia hạn hàng mượn".')

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn hình Phiếu yêu cầu gia hạn hàng mượn (mã phiếu PGHHM) dùng để nhân viên đang mượn hàng '
     'xin dời ngày hẹn trả của một phiếu yêu cầu xuất hàng mượn.\n'
     'Phiếu gửi đi là vào thẳng trạng thái Chờ TP duyệt (KHÔNG có bản nháp) và đi qua các cấp: '
     'Trưởng phòng > (chỉ khi giá trị hàng còn nợ vượt hạn mức) Ban giám đốc > Kế toán.\n'
     'Ngày hẹn trả của phiếu mượn CHỈ đổi sang ngày mới khi Kế toán duyệt ở bước cuối. Màn '
     'không đụng tới tồn kho, không hạch toán.\n'
     'Lối vào: Tài chính > Hàng hoá - Dịch vụ - Vận chuyển > Mượn hàng; Tài chính > Chờ duyệt > '
     'Hàng mượn chờ duyệt (chỉ người có quyền Kế toán kho thấy mục này); Bán hàng > Yêu cầu > '
     'Hàng hóa > YC gia hạn hàng mượn.'),
    ('2. Đối tượng được tính / hiển thị',
     'Danh sách (lối vào thường) hiển thị phiếu theo phạm vi quyền:\n'
     '- Super Admin hoặc có quyền "Xem phiếu hàng mượn theo tổng công ty": phiếu của MỌI công ty '
     '(muốn xem riêng một công ty thì chọn ở ô lọc Công ty).\n'
     '- Có quyền "Xem phiếu hàng mượn theo công ty": mọi phiếu của công ty mình.\n'
     '- Có quyền "Xem phiếu hàng mượn theo phòng ban": phiếu thuộc phòng ban mình quản lý, phòng '
     'ban của chính mình, và phiếu mình lập.\n'
     '- Không có quyền xem nào: chỉ phiếu mình lập.\n'
     '- Ngoài ra ai cũng thấy lại những phiếu mình ĐÃ duyệt hoặc đã từ chối (ở bất kỳ cấp nào).\n'
     'Lối vào "chờ duyệt": chỉ phiếu đang đến lượt mình duyệt (Kế toán kho: Chờ KT duyệt; Ban '
     'giám đốc: Chờ BGĐ duyệt; Trưởng phòng: Chờ TP duyệt của phòng mình quản lý). Người không '
     'có quyền duyệt nào vào lối này chỉ thấy phiếu mình lập.\n'
     'Popup chọn phiếu mượn khi lập phiếu chỉ liệt kê phiếu yêu cầu xuất hàng mượn: do chính mình '
     'lập, đã xuất kho, còn đang mượn, chưa có yêu cầu gia hạn nào đang chờ duyệt, và hạn trả '
     'hiện tại còn trước ngày trần.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu của công ty khác: không hiện trong danh sách, TRỪ với Super Admin và người có quyền '
     'xem theo tổng công ty. Lối vào "chờ duyệt" thì luôn chỉ có phiếu cùng công ty.\n'
     '- Phiếu mượn của người khác, phiếu đã trả hết hàng, phiếu đang có yêu cầu gia hạn chờ duyệt: '
     'không hiện ở popup chọn phiếu.\n'
     '- Phiếu mượn có hạn trả hiện tại đã bằng hoặc sau ngày trần (hôm nay + số ngày mượn tối đa '
     'theo cấu hình): không hiện ở popup chọn phiếu.\n'
     '- Mặt hàng trên phiếu mượn không thuộc diện phải xuất: không hiện ở bảng Chi tiết, '
     'và bộ lọc Tên hàng hóa / Model cũng không dò trên các dòng này.\n'
     '- Thao tác duyệt / từ chối làm bên cổng ERP cũ: không có trong Lịch sử thay đổi.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô "Ngày tạo" (một ô chọn khoảng) lọc theo NGÀY LẬP PHIẾU, không phải ngày duyệt, không '
     'phải ngày hẹn trả.\n'
     'Khoảng ngày lấy trọn hai đầu mút. Chỉ chọn một đầu thì lọc một chiều.\n'
     'Khoảng ngày đang lọc được in thành dòng "Từ ngày ... đến ngày ..." trên file Excel và dòng '
     '"Khoảng thời gian" trên bản in danh sách.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Một phiếu gia hạn gắn với ĐÚNG MỘT phiếu yêu cầu xuất hàng mượn. Phiếu gia hạn KHÔNG có '
     'dòng hàng nhập tay: bảng "Chi tiết" đọc thẳng từ phiếu mượn và chỉ để xem.\n'
     'Thông tin chính: Ngày hẹn trả (chụp lại từ phiếu mượn lúc lập), Ngày hẹn trả mới (1 ô cho '
     'cả phiếu), Ghi chú, File đính kèm (PDF).\n'
     'Phiếu có ba bộ thông tin duyệt cho ba cấp Trưởng phòng, Ban giám đốc, Kế toán; mỗi bộ gồm '
     'người thực hiện, thời điểm, ghi chú / lý do từ chối.\n'
     'Công ty và phòng ban của phiếu chốt theo người lập TẠI THỜI ĐIỂM LẬP.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     'Không cộng dồn. Mỗi phiếu mượn tại một thời điểm chỉ có TỐI ĐA một yêu cầu gia hạn đang chờ '
     'duyệt; phải đợi phiếu đó Đã duyệt hoặc Không duyệt mới lập được phiếu kế tiếp.\n'
     'Bấm Gửi duyệt hai lần liên tiếp cũng chỉ sinh MỘT phiếu.\n'
     'Mã phiếu dạng PGHHM-xxxxx, dùng chung một dãy số với cổng ERP.'),
    ('7. Phân quyền cấp',
     'Quyền thao tác:\n'
     '- Trưởng phòng duyệt hàng mượn (duyệt cấp 1, chỉ phiếu thuộc phòng mình quản lý)\n'
     '- Ban giám đốc duyệt hàng mượn (duyệt cấp vượt hạn mức)\n'
     '- Kế toán kho (duyệt cấp cuối, được sửa Ngày hẹn trả mới trước khi duyệt)\n'
     'Quyền phạm vi dữ liệu:\n'
     '- Xem phiếu hàng mượn theo tổng công ty\n'
     '- Xem phiếu hàng mượn theo công ty\n'
     '- Xem phiếu hàng mượn theo phòng ban\n'
     'KHÔNG có quyền riêng cho Tạo mới: ai đăng nhập cũng lập được phiếu cho phiếu mượn của chính '
     'mình. KHÔNG có chức năng Sửa, Xóa ở bất kỳ trạng thái nào.\n'
     'Mọi cấp duyệt đều phải CÙNG CÔNG TY với phiếu.'),
    ('8. Cách tính các ô thống kê',
     'Thanh phân trang ghi tổng số phiếu khớp bộ lọc TRONG PHẠM VI QUYỀN của người đang xem.\n'
     'Bảng Chi tiết: "SL mượn" và "Đã trả" quy về đơn vị tính trên phiếu mượn; dòng '
     '"Tổng cộng" = tổng hai cột này.\n'
     'Hạn mức vượt cấp: tổng giá trị hàng còn nợ của phiếu mượn = cộng trên mọi dòng hàng '
     '(số lượng đã xuất trừ số lượng đã trả) nhân đơn giá. Tổng này LỚN HƠN hạn mức giá trị hàng '
     'mượn của công ty thì phiếu phải qua Ban giám đốc; bằng hoặc nhỏ hơn thì sang thẳng Kế toán.\n'
     'Ngày trần của Ngày hẹn trả mới = hôm nay + số ngày mượn tối đa theo cấu hình (tính từ HÔM '
     'NAY, không tính từ ngày hẹn trả cũ).\n'
     'Cột "Người duyệt / Ngày duyệt" ở danh sách = cấp đóng dấu SAU CÙNG (Kế toán, không có thì '
     'Ban giám đốc, không có nữa thì Trưởng phòng).'),
    ('9. Ghi chú đọc bảng',
     'Các bẫy dễ bị ghi Failed oan:\n'
     '- Màn KHÔNG có nháp, KHÔNG có nút Sửa, KHÔNG có nút Xóa: đó là đúng thiết kế, không phải thiếu.\n'
     '- Quyền "Xem theo tổng công ty" (và Super Admin) thấy phiếu của MỌI công ty ở lối vào thường '
     '(khác ERP — ERP bó về công ty mình); nhưng chỉ duyệt được phiếu cùng công ty.\n'
     '- Hạn mức vượt cấp lấy theo công ty GHI TRÊN PHIẾU (cũng là công ty người duyệt, vì chỉ '
     'duyệt được phiếu cùng công ty). Hạn mức của công ty để trống thì coi như 0: mọi phiếu mượn '
     'còn nợ đều phải qua Ban giám đốc.\n'
     '- Trưởng phòng nhận thông báo phiếu mới = đúng những Trưởng phòng duyệt được phiếu: quản lý '
     'phòng ban của phiếu, tích "Quản lý tất cả phòng ban", hoặc thuộc chính phòng ban của phiếu.\n'
     '- Chỉ Kế toán sửa được Ngày hẹn trả mới, và chỉ khi phiếu đang Chờ KT duyệt. Trưởng phòng và '
     'Ban giám đốc thấy ô này bị khoá là đúng.\n'
     '- Trưởng phòng duyệt xong mà phiếu chưa Đã duyệt là đúng: ngày hẹn trả của phiếu mượn chỉ '
     'đổi khi Kế toán duyệt.\n'
     '- Không phải phiếu nào cũng qua Ban giám đốc; dưới hạn mức thì nhảy thẳng sang Chờ KT duyệt.\n'
     '- Phiếu bị từ chối sang trạng thái "Không duyệt" và dừng hẳn, không quay về để sửa gửi lại; '
     'muốn gia hạn tiếp phải lập phiếu mới.\n'
     '- Phiếu "Không duyệt" hiện theo phạm vi quyền như mọi trạng thái khác, không còn bị giấu với '
     'người ngoài người lập.\n'
     '- Người đã duyệt / từ chối một phiếu vẫn thấy lại phiếu đó dù không có quyền xem theo cấp.\n'
     '- Mục menu "chờ duyệt" chỉ hiện với người có quyền Kế toán kho.\n'
     '- Phiếu được xử lý bên cổng ERP cũ không có dòng nào trong Lịch sử thay đổi.\n'
     '- Nhóm test bảo mật gọi thẳng chức năng bằng công cụ kiểm thử dành cho tester kỹ thuật.'),
]

ROLE_TCS = [
    ('00', 'Tài khoản không có quyền nào của nhóm hàng mượn vẫn vào được màn', 'P0',
     'Tài khoản A không có quyền duyệt và không có quyền xem theo cấp.\n'
     'A đã lập 6 phiếu gia hạn; công ty của A có hơn 1,000 phiếu.',
     '1. Đăng nhập bằng A.\n2. ' + MENU_ALL,
     '—',
     '- Màn mở được, không báo lỗi quyền.\n'
     '- Danh sách chỉ có đúng 6 phiếu do A lập, tổng số ở thanh phân trang = 6.\n'
     '- Nút "Tạo mới" vẫn hiển thị.\n'
     '- Bộ lọc KHÔNG có ô Công ty và ô Phòng ban.'),
    ('01', 'Quyền "Xem phiếu hàng mượn theo tổng công ty" thấy phiếu mọi công ty', 'P0',
     'Tài khoản B thuộc công ty 1, chỉ có quyền Xem phiếu hàng mượn theo tổng công ty.\n'
     'Công ty 1 có N1 phiếu, công ty 4 có N4 phiếu (N4 > 0).',
     '1. Đăng nhập bằng B.\n2. ' + MENU_ALL + '\n3. Đọc tổng số phiếu.\n'
     '4. Mở bộ lọc, chọn Công ty = công ty 4.',
     'Công ty: công ty 4',
     '- Bước 3: tổng số = N1 + N4 (có cả phiếu của công ty 4, kể cả phiếu Chờ TP duyệt).\n'
     '- Bộ lọc có ô Công ty và ô Phòng ban.\n'
     '- Bước 4: còn đúng N4 phiếu.\n'
     '- Lưu ý: ERP bó về công ty mình; hệ thống mới cho thấy mọi công ty (khớp với việc mở được '
     'chi tiết phiếu công ty khác).'),
    ('02', 'Quyền "Xem phiếu hàng mượn theo công ty" thấy mọi phiếu công ty mình', 'P0',
     'Tài khoản C thuộc công ty 1, chỉ có quyền Xem phiếu hàng mượn theo công ty. Công ty 1 có N1 '
     'phiếu.',
     '1. Đăng nhập bằng C.\n2. ' + MENU_ALL + '\n3. Đọc tổng số phiếu.',
     '—',
     '- Tổng số = N1 (ít hơn tài khoản B ở TC-ROLE-01 đúng N4 phiếu của công ty 4).\n'
     '- Có cả phiếu của các phòng ban khác trong công ty 1.\n'
     '- Có cả phiếu ở trạng thái Không duyệt do người khác lập.'),
    ('03', 'Quyền "Xem phiếu hàng mượn theo phòng ban" chỉ thấy phòng mình quản lý', 'P0',
     'Tài khoản D thuộc phòng P0, được phân công quản lý phòng P1.\n'
     'P0 có 5 phiếu, P1 có 40 phiếu, phòng P2 (D không quản lý) có 35 phiếu.\n'
     'D tự lập 2 phiếu (tính trong 5 phiếu của P0).',
     '1. Đăng nhập bằng D.\n2. ' + MENU_ALL + '\n3. Đọc tổng số phiếu.\n'
     '4. Lọc Phòng ban = P2.',
     '—',
     '- Tổng số = 45 (P0 + P1).\n'
     '- Lọc P2 ra 0 phiếu.\n'
     '- Bộ lọc có ô Phòng ban, KHÔNG có ô Công ty.'),
    ('04', 'Quyền "Trưởng phòng duyệt hàng mượn" chỉ duyệt phiếu phòng mình quản lý', 'P0',
     'Tài khoản E có quyền Trưởng phòng duyệt hàng mượn, quản lý phòng P1 (công ty 1).\n'
     'Phiếu X: Chờ TP duyệt, phòng P1.\n'
     'Phiếu Y: Chờ TP duyệt, phòng P2 (E không quản lý).\n'
     'Phiếu Z: Chờ KT duyệt, phòng P1.',
     '1. Đăng nhập bằng E.\n2. Mở lần lượt X, Y, Z (bằng đường dẫn chi tiết nếu không thấy ở danh '
     'sách).\n3. Xem các nút ở cuối màn.',
     '—',
     '- Phiếu X: có nút "TP duyệt" và "Từ chối".\n'
     '- Phiếu Y: KHÔNG có nút duyệt / từ chối.\n'
     '- Phiếu Z: KHÔNG có nút duyệt (không đúng cấp).\n'
     '- Cả ba phiếu đều có nút "In".'),
    ('05', 'Quyền "Ban giám đốc duyệt hàng mượn"', 'P0',
     'Tài khoản F có quyền Ban giám đốc duyệt hàng mượn, cùng công ty với phiếu M (Chờ BGĐ duyệt) '
     'và phiếu K (Chờ TP duyệt).',
     '1. Đăng nhập bằng F.\n2. Mở phiếu M.\n3. Mở phiếu K.',
     '—',
     '- Phiếu M: có nút "BGĐ duyệt" và "Từ chối".\n'
     '- Phiếu K: KHÔNG có nút duyệt / từ chối.\n'
     '- Ô Ngày hẹn trả mới của M bị khoá.'),
    ('06', 'Quyền "Kế toán kho" duyệt cấp cuối', 'P0',
     'Tài khoản G có quyền Kế toán kho, cùng công ty với phiếu N đang Chờ KT duyệt.',
     '1. Đăng nhập bằng G.\n2. Mở phiếu N.',
     '—',
     '- Có nút "KT duyệt" và "Từ chối".\n'
     '- Ô Ngày hẹn trả mới được MỞ KHOÁ, có dấu bắt buộc.\n'
     '- Lưu ý: đây là bước duy nhất làm đổi ngày hẹn trả của phiếu mượn, kiểm kỹ ở nhóm VI.'),
    ('07', 'Người duyệt khác công ty với phiếu không duyệt được', 'P0',
     'Tài khoản H có quyền Kế toán kho, thuộc công ty 4.\n'
     'Phiếu Q ở trạng thái Chờ KT duyệt, thuộc công ty 1.',
     '1. Đăng nhập bằng H.\n2. Tìm phiếu Q ở danh sách.\n'
     '3. Dùng công cụ kiểm thử gọi thẳng chức năng duyệt phiếu Q.',
     '—',
     '- Bước 2: phiếu Q không có trong danh sách.\n'
     '- Bước 3: phần mềm từ chối, báo "Bạn không có quyền duyệt bước này."\n'
     '- Trạng thái Q vẫn Chờ KT duyệt; ngày hẹn trả của phiếu mượn không đổi.'),
    ('08', 'Gọi thẳng chức năng duyệt khi không đúng cấp', 'P0',
     'Tài khoản E chỉ có quyền Trưởng phòng duyệt hàng mượn. Phiếu R đang Chờ KT duyệt.',
     '1. Đăng nhập bằng E.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng duyệt phiếu R.',
     '—',
     '- Phần mềm từ chối, báo "Bạn không có quyền duyệt bước này."\n'
     '- Phiếu R vẫn Chờ KT duyệt, không phát sinh dòng lịch sử mới.'),
    ('09', 'Gọi thẳng chức năng từ chối khi không đúng cấp', 'P0',
     'Tài khoản A không có quyền duyệt nào. Phiếu S đang Chờ TP duyệt.',
     '1. Đăng nhập bằng A.\n2. Dùng công cụ kiểm thử gọi thẳng chức năng từ chối phiếu S kèm lý do.',
     'Lý do: Thử từ chối',
     '- Phần mềm từ chối, báo "Bạn không có quyền từ chối phiếu này."\n'
     '- Phiếu S vẫn Chờ TP duyệt.'),
    ('10', 'Mở chi tiết phiếu ngoài phạm vi bằng đường dẫn trực tiếp', 'P0',
     'Tài khoản A không có quyền xem, không có quyền duyệt. Phiếu T cùng công ty do người khác lập, '
     'A chưa từng duyệt.',
     '1. Đăng nhập bằng A.\n2. Dán đường dẫn chi tiết phiếu T vào thanh địa chỉ.\n'
     '3. Dùng công cụ kiểm thử gọi thẳng chức năng xem lịch sử và in của phiếu T.',
     '—',
     '- Màn chi tiết KHÔNG hiện nội dung phiếu T; phần mềm báo không có quyền xem phiếu này.\n'
     '- Xem lịch sử và in cũng bị từ chối với cùng thông báo.'),
    ('11', 'Không có chức năng Sửa và Xóa phiếu', 'P0',
     'Tài khoản Super Admin; danh sách có phiếu ở đủ 5 trạng thái.',
     '1. Mở menu Hành động của từng dòng.\n2. Mở màn chi tiết một phiếu Chờ TP duyệt do chính mình '
     'lập.\n3. Dùng công cụ kiểm thử gọi chức năng sửa / xóa phiếu.',
     '—',
     '- Menu Hành động chỉ gồm: Duyệt, Từ chối (khi đến lượt mình), In, Lịch sử.\n'
     '- Màn chi tiết không có nút Sửa, Xóa; các ô thông tin chung đều khoá.\n'
     '- Không tồn tại chức năng sửa / xóa để gọi; phiếu không đổi.'),
    ('12', 'Mục menu "chờ duyệt" chỉ hiện với quyền Kế toán kho', 'P1',
     'Tài khoản G có quyền Kế toán kho; tài khoản E chỉ có quyền Trưởng phòng duyệt hàng mượn.',
     '1. Đăng nhập bằng G, mở phân hệ Tài chính > nhóm Chờ duyệt.\n'
     '2. Đăng nhập bằng E, làm lại bước 1.',
     '—',
     '- G thấy nhóm "Hàng mượn chờ duyệt" với mục "Phiếu yêu cầu gia hạn hàng mượn chờ duyệt".\n'
     '- E KHÔNG thấy mục này (giữ đúng như ERP).'),
]

# ============================================================== I
S1 = [
    ('001', 'Mở màn từ phân hệ Tài chính (lối vào thường)', 'P0',
     'Tài khoản có quyền Xem phiếu hàng mượn theo công ty; công ty có N phiếu.',
     '1. Đăng nhập.\n2. ' + MENU_ALL,
     '—',
     '- Tiêu đề bảng và tên tab trình duyệt ghi "Phiếu yêu cầu gia hạn hàng mượn".\n'
     '- Bảng hiện dữ liệu, tổng số = N.\n'
     '- Không có thông báo lỗi.'),
    ('002', 'Mở màn từ phân hệ Bán hàng', 'P0',
     'Cùng tài khoản ở TC_01.001.',
     '1. ' + MENU_SALE + '\n2. So tổng số phiếu với TC_01.001.',
     '—',
     '- Mở đúng màn "Phiếu yêu cầu gia hạn hàng mượn".\n'
     '- Tổng số phiếu BẰNG với lối vào ở phân hệ Tài chính (hai lối vào cùng phạm vi).'),
    ('003', 'Mở lối vào "chờ duyệt" với quyền Kế toán kho', 'P0',
     'Tài khoản G có quyền Kế toán kho. Công ty có 3 phiếu Chờ KT duyệt, 2 phiếu Chờ TP duyệt, 1 '
     'phiếu Chờ BGĐ duyệt.',
     '1. Đăng nhập bằng G.\n2. ' + MENU_WAIT,
     '—',
     '- Tiêu đề ghi "Phiếu yêu cầu gia hạn hàng mượn chờ duyệt".\n'
     '- Danh sách có đúng 3 phiếu, tất cả đều Chờ KT duyệt.\n'
     '- Mỗi dòng đều có hành động Duyệt và Từ chối.'),
    ('004', 'Lối vào "chờ duyệt" của người có nhiều quyền duyệt', 'P1',
     'Tài khoản có cả quyền Kế toán kho và Ban giám đốc duyệt hàng mượn. Công ty có 3 phiếu Chờ KT '
     'duyệt và 1 phiếu Chờ BGĐ duyệt.',
     '1. Đăng nhập.\n2. ' + MENU_WAIT,
     '—',
     '- Danh sách có 4 phiếu: 3 Chờ KT duyệt và 1 Chờ BGĐ duyệt.'),
    ('005', 'Lối vào "chờ duyệt" của Trưởng phòng chỉ gồm phòng mình quản lý', 'P0',
     'Tài khoản có quyền Kế toán kho (để thấy menu) và Trưởng phòng duyệt hàng mượn, quản lý phòng '
     'P1. P1 có 2 phiếu Chờ TP duyệt, P2 có 3 phiếu Chờ TP duyệt. Không có phiếu Chờ KT duyệt.',
     '1. Đăng nhập.\n2. ' + MENU_WAIT,
     '—',
     '- Danh sách chỉ có 2 phiếu của P1.\n- Không có phiếu nào của P2.'),
    ('006', 'Người không có quyền duyệt gõ đường dẫn lối vào "chờ duyệt"', 'P1',
     'Tài khoản A không có quyền duyệt nào, đã lập 6 phiếu.',
     '1. Đăng nhập bằng A.\n2. Mở màn danh sách từ menu, sau đó sửa đường dẫn trên thanh địa chỉ '
     'sang lối vào "chờ duyệt" (thêm đuôi chờ duyệt như menu Chờ duyệt dùng).',
     '—',
     '- Tiêu đề đổi sang "... chờ duyệt".\n'
     '- Danh sách chỉ có 6 phiếu do A lập; không lộ phiếu của người khác.'),
    ('007', 'Sửa tay tham số trên thanh địa chỉ thành giá trị lạ', 'P0',
     'Tài khoản A không có quyền xem nào, lập 6 phiếu; công ty có hơn 1,000 phiếu.',
     '1. Đăng nhập bằng A.\n2. Mở màn danh sách.\n'
     '3. Sửa phần tham số trên thanh địa chỉ thành một giá trị bất kỳ (ví dụ "abc"), hoặc xoá hẳn '
     'phần tham số.',
     '—',
     '- Màn không báo lỗi, tiêu đề là "Phiếu yêu cầu gia hạn hàng mượn".\n'
     '- Vẫn chỉ thấy 6 phiếu của A, KHÔNG lộ toàn bộ phiếu của công ty.\n'
     '- Lưu ý: ERP cũ để lộ toàn bộ phiếu công ty ở trường hợp này; hệ thống mới đã chặn.'),
    ('008', 'Đang ở màn, bấm menu sang lối vào khác', 'P0',
     'Tài khoản Kế toán kho, đang ở lối vào thường, đã lọc Trạng thái = Đã duyệt.',
     '1. ' + MENU_WAIT + '\n2. Quan sát danh sách.\n3. Bấm lại menu lối vào thường.',
     'Trạng thái: Đã duyệt',
     '- Sau bước 1: tiêu đề đổi sang "... chờ duyệt", danh sách tự nạp lại theo lối vào mới, về '
     'trang 1.\n'
     '- Sau bước 3: tiêu đề và phạm vi quay về lối vào thường.'),
    ('009', 'Vòng quay chờ khi đang tải dữ liệu', 'P2',
     'Công ty có hơn 1,000 phiếu.',
     '1. Mở màn và quan sát bảng trong lúc tải.',
     '—',
     '- Bảng hiện trạng thái đang tải.\n'
     '- KHÔNG nhấp nháy dòng "Không có dữ liệu phù hợp." trước khi hiện dữ liệu.'),
    ('010', 'Bố cục thanh công cụ', 'P1',
     'Đã vào màn.',
     '1. Quan sát khối bộ lọc và thanh công cụ của bảng.',
     '—',
     '- Ô tìm nhanh có gợi ý "Tìm theo mã phiếu, người tạo...".\n'
     '- Thanh công cụ theo thứ tự: Tạo mới, In, Xuất Excel, biểu tượng cấu hình cột.\n'
     '- KHÔNG có nút Xóa hàng loạt.'),
    ('011', 'Bảng rỗng khi không có dữ liệu', 'P1',
     'Tài khoản mới, chưa lập phiếu nào, không có quyền xem và không có quyền duyệt.',
     '1. Mở màn.',
     '—',
     '- Bảng hiện dòng "Không có dữ liệu phù hợp.".\n- Tổng số = 0.'),
    ('012', 'Màu nhãn trạng thái', 'P0',
     'Danh sách có phiếu ở đủ 5 trạng thái.',
     '1. Lọc lần lượt từng trạng thái, quan sát nhãn ở cột Trạng thái.',
     'Trạng thái: lần lượt 5 giá trị',
     '- Chờ TP duyệt, Chờ BGĐ duyệt, Chờ KT duyệt: nhãn màu VÀNG CAM.\n'
     '- Đã duyệt: nhãn XANH LÁ.\n'
     '- Không duyệt: nhãn ĐỎ.\n'
     '- Lưu ý: ERP tô đỏ mọi trạng thái khác Đã duyệt; hệ thống mới chỉ tô đỏ Không duyệt.'),
]

# ============================================================== II
S2 = [
    ('001', 'Tìm nhanh theo mã phiếu đầy đủ', 'P0',
     'Tồn tại phiếu PGHHM-02930 trong phạm vi.',
     '1. Gõ PGHHM-02930 vào ô tìm nhanh.\n2. Bấm Tìm kiếm (hoặc Enter).',
     'Ô tìm nhanh: PGHHM-02930',
     '- Danh sách còn đúng 1 dòng PGHHM-02930, tổng số = 1.'),
    ('002', 'Tìm nhanh theo tên người tạo', 'P0',
     'Nhân viên "Nguyễn Văn Thắng" đã lập 18 phiếu trong phạm vi.',
     '1. Gõ "Văn Thắng" vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: Văn Thắng',
     '- Mọi dòng đều có cột Người tạo chứa "Văn Thắng".\n- Tổng số = 18.'),
    ('003', 'Kết quả tìm nhanh xếp theo độ khớp mã', 'P2',
     'Có phiếu PGHHM-00215 và các phiếu khác chứa chuỗi 0215 ở giữa mã.',
     '1. Gõ PGHHM-00215 vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: PGHHM-00215',
     '- Dòng trùng khít mã đứng đầu danh sách.'),
    ('004', 'Ô tìm nhanh không tự tìm khi đang gõ', 'P1',
     'Đang ở màn danh sách.',
     '1. Gõ vài ký tự vào ô tìm nhanh.\n2. Chờ 5 giây, không bấm gì.',
     'Ô tìm nhanh: PGHH',
     '- Danh sách giữ nguyên cho tới khi bấm Tìm kiếm hoặc Enter.'),
    ('005', 'Lọc theo Mã phiếu', 'P1',
     'Có phiếu PGHHM-02930.',
     '1. Mở bộ lọc.\n2. Gõ 02930 vào ô Mã phiếu, nhấn Enter.',
     'Mã phiếu: 02930',
     '- Chỉ còn phiếu có mã chứa 02930.'),
    ('006', 'Lọc theo Phiếu mượn', 'P0',
     'Phiếu mượn PYCXH-35542 có 2 phiếu gia hạn (1 Đã duyệt, 1 Không duyệt).',
     '1. Gõ PYCXH-35542 vào ô Phiếu mượn, nhấn Enter.',
     'Phiếu mượn: PYCXH-35542',
     '- Ra đúng 2 phiếu, cột Phiếu mượn đều là PYCXH-35542.'),
    ('007', 'Ô Trạng thái có đủ 5 giá trị theo thứ tự vòng đời', 'P0',
     'Đã vào màn.',
     '1. Mở bộ lọc.\n2. Bấm mở ô Trạng thái.',
     '—',
     '- Có đúng 5 giá trị theo thứ tự: Chờ TP duyệt, Chờ BGĐ duyệt, Chờ KT duyệt, Đã duyệt, '
     'Không duyệt.\n'
     '- Lưu ý: ERP chỉ có 3 giá trị; hệ thống mới liệt kê đủ 5.'),
    ('008', 'Lọc theo từng trạng thái', 'P0',
     'Công ty có 3 phiếu Chờ TP duyệt, 2 phiếu Chờ KT duyệt.',
     '1. Chọn Trạng thái = Chờ TP duyệt.\n2. Chọn Trạng thái = Chờ KT duyệt.',
     'Trạng thái: Chờ TP duyệt\nTrạng thái: Chờ KT duyệt',
     '- Chọn xong danh sách TỰ nạp lại, không cần bấm Tìm kiếm.\n'
     '- Bước 1 ra 3 phiếu; bước 2 ra 2 phiếu; mọi dòng đúng trạng thái đã chọn.'),
    ('009', 'Lọc theo Người tạo', 'P0',
     'Nhân viên X đã lập 4 phiếu trong phạm vi.',
     '1. Chọn Người tạo = X.',
     'Người tạo: X',
     '- Ra đúng 4 phiếu, cột Người tạo đều là X.'),
    ('010', 'Lọc theo Người duyệt khớp mọi cấp đã đóng dấu', 'P1',
     'Trưởng phòng E đã duyệt 3 phiếu mà sau đó Kế toán G đã duyệt tiếp (cột Người duyệt hiện G), '
     'và 1 phiếu E vừa duyệt đang Chờ KT duyệt (cột Người duyệt hiện E).',
     '1. Chọn Người duyệt = E.',
     'Người duyệt: E',
     '- Ra 4 phiếu: có cả 3 phiếu mà cột Người duyệt đang hiện G.\n'
     '- Lưu ý: ô lọc dò trên cả 3 cấp duyệt, còn cột chỉ hiện cấp sau cùng; không phải lỗi.'),
    ('011', 'Lọc theo Tên hàng hóa', 'P1',
     'Phiếu mượn PYCXH-35542 có mặt hàng "Máy hàn điện tử"; có 1 phiếu gia hạn cho phiếu mượn này.',
     '1. Gõ "Máy hàn" vào ô Tên hàng hóa, nhấn Enter.',
     'Tên hàng hóa: Máy hàn',
     '- Ra phiếu gia hạn của PYCXH-35542 và các phiếu khác có mặt hàng tên chứa "Máy hàn".\n'
     '- Mở từng phiếu: bảng Chi tiết đều có mặt hàng chứa "Máy hàn".'),
    ('012', 'Lọc Tên hàng hóa không dò trên dòng hàng không hiển thị', 'P2',
     'Phiếu mượn M có một dòng hàng "Kìm cắt" thuộc diện không phải xuất (không hiện ở bảng Chi '
     'tiết). Có 1 phiếu gia hạn cho M.',
     '1. Gõ "Kìm cắt" vào ô Tên hàng hóa, nhấn Enter.',
     'Tên hàng hóa: Kìm cắt',
     '- Phiếu gia hạn của M KHÔNG xuất hiện.\n'
     '- Lưu ý: ERP vẫn ra phiếu này dù trên màn không có mặt hàng đó; hệ thống mới đã sửa.'),
    ('013', 'Lọc theo Model', 'P1',
     'Có phiếu mượn có mặt hàng model "WS-200".',
     '1. Gõ "WS-200" vào ô Model, nhấn Enter.',
     'Model: WS-200',
     '- Mọi phiếu trả về đều có ít nhất một mặt hàng model chứa "WS-200".'),
    ('014', 'Lọc theo khoảng Ngày tạo', 'P0',
     'Có phiếu lập ngày 01/09/2026, 15/09/2026, 30/09/2026.',
     '1. Chọn Ngày tạo từ 01/09/2026 đến 15/09/2026.',
     'Ngày tạo: 01/09/2026 - 15/09/2026',
     '- Có cả phiếu lập ngày 01/09 và 15/09 (lấy trọn hai đầu).\n'
     '- Không có phiếu ngày 30/09.'),
    ('015', 'Lọc Công ty - Phòng ban theo quyền', 'P1',
     'Tài khoản có quyền Xem phiếu hàng mượn theo công ty. Phòng P1 có 40 phiếu.',
     '1. Chọn Phòng ban = P1.',
     'Phòng ban: P1',
     '- Ra đúng 40 phiếu.\n'
     '- Khối lọc không có ô Bộ phận và ô Nhân viên.'),
    ('016', 'Kết hợp nhiều điều kiện lọc', 'P0',
     'Tài khoản có quyền Xem theo phòng ban (quản lý P1).',
     '1. Chọn Trạng thái = Đã duyệt.\n2. Chọn Người tạo = X (thuộc P1).\n'
     '3. Chọn khoảng Ngày tạo tháng 09/2026.',
     'Trạng thái: Đã duyệt\nNgười tạo: X\nNgày tạo: 01/09/2026 - 30/09/2026',
     '- Kết quả thoả đồng thời cả 3 điều kiện.\n'
     '- KHÔNG xuất hiện phiếu ngoài phòng P1 hoặc phòng của chính mình.'),
    ('017', 'Làm mới xoá điều kiện nhưng giữ lối vào', 'P0',
     'Kế toán kho đang ở lối vào "chờ duyệt", đã gõ tìm nhanh và lọc Phiếu mượn.',
     '1. Bấm nút Làm mới.',
     '—',
     '- Mọi ô lọc và ô tìm nhanh trở về trống, về trang 1.\n'
     '- Tiêu đề vẫn "... chờ duyệt" và danh sách vẫn chỉ gồm phiếu chờ mình duyệt.'),
    ('018', 'Giữ bộ lọc khi vào chi tiết rồi quay lại', 'P1',
     'Đã lọc Trạng thái = Chờ KT duyệt.',
     '1. Bấm mã phiếu một dòng để mở chi tiết.\n2. Bấm quay lại danh sách.',
     'Trạng thái: Chờ KT duyệt',
     '- Danh sách vẫn giữ điều kiện lọc Chờ KT duyệt.'),
    ('019', 'Cài đặt bộ lọc', 'P2',
     'Đã vào màn.',
     '1. Bấm Cài đặt bộ lọc.\n2. Ẩn ô Model.\n3. Lưu.',
     '—',
     '- Ô Model không còn hiện ở khối lọc.\n'
     '- Tải lại trang, cấu hình vẫn được giữ.'),
]

# ============================================================== III
S3 = [
    ('001', 'Đủ cột theo cấu hình mặc định', 'P0',
     'Người dùng chưa đổi cấu hình cột.',
     '1. Quan sát tiêu đề cột, cuộn ngang nếu cần.',
     '—',
     '- Hiện sẵn: STT, Mã phiếu, Phiếu mượn, Người tạo, Ngày tạo, Ngày hẹn trả cũ, Ngày hẹn trả '
     'mới, Trạng thái, Người duyệt, Ngày duyệt, Hành động.\n'
     '- Ẩn sẵn (bật được trong cấu hình cột): Phòng ban, Ghi chú, Lý do từ chối.\n'
     '- KHÔNG có cột Người cập nhật / Ngày cập nhật.'),
    ('002', 'Định dạng ngày trong bảng', 'P0',
     'Có phiếu đã duyệt.',
     '1. Quan sát các cột ngày.',
     '—',
     '- Ngày tạo, Ngày duyệt dạng dd/mm/yyyy hh:mm.\n'
     '- Ngày hẹn trả cũ, Ngày hẹn trả mới dạng dd/mm/yyyy.\n'
     '- Phiếu chưa ai duyệt: ô Người duyệt, Ngày duyệt để TRỐNG (không in dấu gạch).'),
    ('003', 'Cột Người duyệt hiện cấp đóng dấu sau cùng', 'P0',
     'Phiếu P1 vừa được Trưởng phòng E duyệt, đang Chờ KT duyệt.\n'
     'Phiếu P2 đã qua E và Kế toán G, Đã duyệt.\n'
     'Phiếu P3 bị Ban giám đốc F từ chối.',
     '1. Tìm 3 phiếu trên danh sách, đọc cột Người duyệt và Ngày duyệt.',
     '—',
     '- P1: E và thời điểm E duyệt.\n'
     '- P2: G và thời điểm G duyệt.\n'
     '- P3: F và thời điểm F từ chối.'),
    ('004', 'Mã phiếu mở màn chi tiết', 'P0',
     'Có ít nhất 1 phiếu.',
     '1. Bấm vào mã phiếu dòng đầu.',
     '—',
     '- Mở màn chi tiết, tiêu đề "Chi tiết yêu cầu gia hạn hàng mượn: <mã phiếu>".'),
    ('005', 'Cột Phiếu mượn mở tab mới', 'P1',
     'Dòng có Phiếu mượn PYCXH-35542.',
     '1. Bấm vào PYCXH-35542.',
     '—',
     '- Mở TAB MỚI, là màn chi tiết phiếu yêu cầu xuất hàng PYCXH-35542.\n'
     '- Tab danh sách gia hạn vẫn giữ nguyên.'),
    ('006', 'Hành động trên dòng theo lượt duyệt', 'P0',
     'Kế toán kho G. Dòng X Chờ KT duyệt (cùng công ty); dòng Y Đã duyệt.',
     '1. Mở menu Hành động dòng X.\n2. Mở menu Hành động dòng Y.',
     '—',
     '- Dòng X: Duyệt, Từ chối, In, Lịch sử.\n'
     '- Dòng Y: chỉ In, Lịch sử (Duyệt, Từ chối bị ẨN, không phải mờ đi).'),
    ('007', 'Hành động Duyệt trên dòng mở màn chi tiết', 'P0',
     'Dòng X Chờ KT duyệt, đến lượt G.',
     '1. Chọn Hành động > Duyệt ở dòng X.',
     '—',
     '- Mở màn chi tiết phiếu X (chưa duyệt ngay), để Kế toán kiểm và sửa ngày trước khi bấm duyệt.'),
    ('008', 'Sắp xếp theo các cột cho phép', 'P1',
     'Có nhiều phiếu.',
     '1. Bấm lần lượt tiêu đề Mã phiếu, Ngày tạo, Ngày hẹn trả cũ, Ngày hẹn trả mới, Ngày duyệt; '
     'mỗi cột bấm 2 lần.',
     '—',
     '- Mỗi cột đổi được tăng / giảm dần, dữ liệu xếp đúng.\n'
     '- Ngày duyệt xếp theo mốc của cấp đóng dấu sau cùng (đúng giá trị đang hiện).\n'
     '- Các cột khác (Người tạo, Trạng thái...) không sắp xếp được.'),
    ('009', 'Thứ tự mặc định mới nhất trước', 'P1',
     'Chưa bấm sắp xếp.',
     '1. Mở màn.',
     '—',
     '- Phiếu có Ngày tạo mới nhất ở đầu.'),
    ('010', 'Phân trang và đổi số dòng mỗi trang', 'P0',
     'Có 35 phiếu trong phạm vi.',
     '1. Quan sát thanh phân trang.\n2. Sang trang 4.\n3. Đổi số dòng / trang sang 20.',
     '—',
     '- Mặc định 10 dòng / trang, 4 trang.\n'
     '- Trang 4 có 5 dòng, STT chạy 31 đến 35.\n'
     '- Đổi 20 dòng: về trang 1, còn 2 trang.'),
    ('011', 'Lật trang không lặp và không sót phiếu', 'P1',
     'Có nhiều phiếu lập cùng một thời điểm.',
     '1. Lật lần lượt các trang, ghi lại mã phiếu.',
     '—',
     '- Không có mã phiếu nào lặp lại giữa các trang; tổng số mã đếm được bằng tổng số.'),
    ('012', 'Cấu hình cột hiển thị', 'P2',
     'Đã vào màn.',
     '1. Bấm biểu tượng cấu hình cột.\n2. Bật cột Lý do từ chối, tắt cột Ngày hẹn trả cũ.\n3. Lưu.',
     '—',
     '- Bảng hiện cột Lý do từ chối, ẩn cột Ngày hẹn trả cũ.\n'
     '- Cột STT, Mã phiếu, Hành động không tắt được.'),
    ('013', 'Cột Lý do từ chối hiện lý do của cấp đã từ chối', 'P1',
     'Phiếu P bị Trưởng phòng từ chối với lý do "Chưa trả hàng kỳ trước".',
     '1. Bật cột Lý do từ chối.\n2. Tìm phiếu P.',
     '—',
     '- Ô Lý do từ chối của P ghi "Chưa trả hàng kỳ trước".'),
]

# ============================================================== IV
S4 = [
    ('001', 'Mở màn Tạo mới', 'P0',
     'Nhân viên A đang có phiếu mượn đủ điều kiện gia hạn.',
     '1. Bấm nút "Tạo mới" ở danh sách.',
     '—',
     '- Tiêu đề "Thêm yêu cầu gia hạn hàng mượn".\n'
     '- Khối "Thông tin chung", góc phải ghi "<tên người đăng nhập> — <ngày hôm nay>"; các ô: Phiếu '
     'yêu cầu xuất hàng mượn (bắt buộc, có nút "Chọn phiếu"), Ngày hẹn trả (khoá), Ngày hẹn trả mới '
     '(bắt buộc), Ngày tạo (khoá, là ngày hôm nay), Ghi chú (gợi ý "Lý do cần gia hạn (không bắt '
     'buộc)").\n'
     '- Khối "File đính kèm" có nút "Thêm tài liệu" và các cột STT, UPLOAD / FILE, DUNG LƯỢNG.\n'
     '- Khối "Chi tiết" đang ghi "Chưa chọn phiếu mượn. Bấm Chọn phiếu ở trên để lấy danh sách '
     'hàng.".\n'
     '- Cuối màn có nút "Gửi duyệt" và "Lưu và tiếp tục"; KHÔNG có nút Lưu nháp.'),
    ('002', 'Ô khoá có biểu tượng chữ i giải thích', 'P1',
     'Đang ở màn Tạo mới.',
     '1. Rê chuột vào biểu tượng chữ i cạnh nhãn Ngày hẹn trả và Ngày tạo.',
     '—',
     '- Ngày hẹn trả: "Lấy từ phiếu mượn đã chọn — đây là hạn trả đang có hiệu lực trước khi gia '
     'hạn."\n'
     '- Ngày tạo: giải thích ngày lập do hệ thống tự ghi nên không sửa được.'),
    ('003', 'Popup chọn phiếu chỉ liệt kê phiếu mượn của chính mình', 'P0',
     'A có 6 phiếu mượn đủ điều kiện. Nhân viên B có 4 phiếu mượn đủ điều kiện.',
     '1. Đăng nhập bằng A, vào Tạo mới.\n2. Bấm "Chọn phiếu".',
     '—',
     '- Popup "Chọn phiếu yêu cầu xuất hàng mượn" có cột STT, Mã phiếu, Ngày tạo, Ngày hẹn trả, '
     'Ghi chú.\n'
     '- Có đúng 6 phiếu của A, không có phiếu nào của B.\n'
     '- Lưu ý: ERP liệt kê cả phiếu người khác rồi đến lúc Gửi mới báo lỗi; hệ thống mới lọc sẵn.'),
    ('004', 'Popup không liệt kê phiếu mượn đang có yêu cầu gia hạn chờ duyệt', 'P0',
     'Phiếu mượn M1 của A đang có một phiếu gia hạn Chờ TP duyệt.\n'
     'Phiếu mượn M2 của A có phiếu gia hạn cũ đã Không duyệt.\n'
     'Phiếu mượn M3 của A có phiếu gia hạn cũ Đã duyệt.',
     '1. Đăng nhập A, vào Tạo mới, bấm "Chọn phiếu".\n2. Tìm M1, M2, M3.',
     '—',
     '- M1 KHÔNG có trong popup.\n- M2 và M3 CÓ trong popup.'),
    ('005', 'Popup không liệt kê phiếu mượn đã trả hết hàng hoặc chưa xuất kho', 'P0',
     'A có phiếu mượn M4 đã trả hết hàng, và phiếu mượn M5 chưa được xuất kho.',
     '1. Bấm "Chọn phiếu", tìm M4 và M5.',
     '—',
     '- Không thấy M4 và M5.\n'
     '- Lưu ý: ERP vẫn cho gia hạn phiếu đã trả hết hàng; hệ thống mới đã chặn.'),
    ('006', 'Popup không liệt kê phiếu mượn có hạn trả đã chạm ngày trần', 'P1',
     'Cấu hình số ngày mượn tối đa = 7, hôm nay 30/09/2026 nên ngày trần là 07/10/2026.\n'
     'A có phiếu mượn M6 hạn trả 07/10/2026 và M7 hạn trả 06/10/2026.',
     '1. Bấm "Chọn phiếu", tìm M6 và M7.',
     '—',
     '- M6 KHÔNG có trong popup (không còn ngày nào để gia hạn).\n- M7 CÓ trong popup.'),
    ('007', 'Tìm phiếu trong popup theo mã', 'P1',
     'A có phiếu mượn PYCXH-35542.',
     '1. Mở popup, gõ 35542 vào ô "Tìm theo mã phiếu mượn...".\n2. Chờ khoảng 1 giây.',
     'Tìm: 35542',
     '- Popup tự lọc (không cần Enter), chỉ còn PYCXH-35542.\n'
     '- Gõ mã không tồn tại: popup ghi "Không có phiếu mượn nào khớp mã đã nhập."'),
    ('008', 'Popup rỗng nói rõ lý do', 'P1',
     'Nhân viên không có phiếu mượn nào đủ điều kiện.',
     '1. Mở popup.',
     '—',
     '- Popup ghi "Bạn không có phiếu mượn nào gia hạn được. Chỉ phiếu do chính bạn lập, đã xuất '
     'kho, còn đang mượn và chưa có yêu cầu gia hạn chờ duyệt mới hiện ở đây."'),
    ('009', 'Phân trang trong popup', 'P2',
     'A có 23 phiếu mượn đủ điều kiện.',
     '1. Mở popup.\n2. Bấm "Sau" hai lần, rồi "Trước".',
     '—',
     '- Mỗi trang 10 phiếu, có dòng "Trang 1 / 3".\n'
     '- Trang 3 có 3 phiếu; nút "Sau" không bấm được ở trang cuối.'),
    ('010', 'Chọn phiếu mượn đổ dữ liệu vào form', 'P0',
     'Phiếu mượn PYCXH-35542 hạn trả 23/09/2026, có 3 mặt hàng.',
     '1. Mở popup, bấm vào dòng PYCXH-35542.',
     '—',
     '- Popup đóng.\n'
     '- Ô Phiếu yêu cầu xuất hàng mượn = PYCXH-35542; Ngày hẹn trả = 23/09/2026.\n'
     '- Bảng Chi tiết có 3 dòng, cột: STT, Tên hàng hóa, Model, Mã hàng hóa, Thương '
     'hiệu, SL mượn, Đã trả, ĐVT; dòng "Tổng cộng" ở cuối.\n'
     '- Không phải nhập số lượng ở dòng nào (bảng chỉ để xem).'),
    ('011', 'Đổi sang phiếu mượn khác', 'P1',
     'Đã chọn PYCXH-35542.',
     '1. Bấm "Chọn phiếu" lần nữa, chọn phiếu mượn khác.',
     '—',
     '- Ô phiếu, Ngày hẹn trả và bảng Chi tiết đổi theo phiếu mới; không còn dòng của '
     'phiếu cũ.'),
    ('012', 'Lịch chỉ cho chọn ngày trong khoảng hợp lệ', 'P0',
     'Hôm nay 30/09/2026, số ngày mượn tối đa = 7 (ngày trần 07/10/2026).\n'
     'Đã chọn phiếu mượn có Ngày hẹn trả 02/10/2026.',
     '1. Mở lịch ô Ngày hẹn trả mới.\n2. Thử bấm 30/09, 02/10, 03/10, 07/10, 08/10.',
     '—',
     '- 30/09 và 02/10: bị mờ, không chọn được (phải SAU cả hôm nay lẫn ngày hẹn trả hiện tại).\n'
     '- 03/10 và 07/10: chọn được.\n'
     '- 08/10: bị mờ (vượt ngày trần).\n'
     '- Biểu tượng chữ i của ô ghi "... tối đa 07/10/2026 (theo cấu hình số ngày mượn tối đa)."'),
    ('013', 'Ngày trần tính từ hôm nay, không từ ngày hẹn trả cũ', 'P1',
     'Hôm nay 30/09/2026, số ngày mượn tối đa = 7. Phiếu mượn hạn trả 01/10/2026.',
     '1. Chọn phiếu mượn.\n2. Mở lịch ô Ngày hẹn trả mới.',
     '—',
     '- Ngày chọn được: 02/10/2026 đến 07/10/2026 (không phải tới 08/10).'),
    ('014', 'Gửi duyệt thành công', 'P0',
     'Nhân viên A thuộc phòng P1, đã chọn phiếu mượn PYCXH-35542 (hạn 23/09/2026).',
     '1. Chọn Ngày hẹn trả mới 05/10/2026.\n2. Nhập Ghi chú.\n3. Bấm "Gửi duyệt".',
     'Ngày hẹn trả mới: 05/10/2026\nGhi chú: Khách chưa nghiệm thu xong',
     '- Thông báo "Yêu cầu của bạn đã được gửi".\n'
     '- Tự quay về màn DANH SÁCH.\n'
     '- Phiếu mới có mã PGHHM-xxxxx, trạng thái Chờ TP duyệt, Ngày hẹn trả cũ 23/09/2026, Ngày hẹn '
     'trả mới 05/10/2026.\n'
     '- Ngày hẹn trả của phiếu mượn PYCXH-35542 VẪN là 23/09/2026 (chưa đổi).'),
    ('015', 'Lưu và tiếp tục', 'P0',
     'A có 2 phiếu mượn đủ điều kiện.',
     '1. Chọn phiếu mượn thứ nhất, chọn ngày mới.\n2. Bấm "Lưu và tiếp tục".\n'
     '3. Mở lại popup chọn phiếu.',
     'Ngày hẹn trả mới: 05/10/2026',
     '- Phiếu thứ nhất được GỬI ĐI luôn (trạng thái Chờ TP duyệt), không phải lưu nháp.\n'
     '- Ở lại màn Tạo mới với form trắng.\n'
     '- Popup không còn phiếu mượn thứ nhất.'),
    ('016', 'Phiếu chốt công ty và phòng ban theo người lập lúc lập', 'P0',
     'A thuộc phòng P1 công ty 1.',
     '1. A gửi một phiếu.\n2. Chuyển A sang phòng P2.\n3. Mở lại phiếu vừa gửi.',
     '—',
     '- Ô "Phòng ban yêu cầu" vẫn là P1.\n'
     '- Trưởng phòng quản lý P1 (không phải P2) là người duyệt được phiếu.'),
    ('017', 'Thông báo cho Trưởng phòng khi có phiếu mới', 'P0',
     'Trưởng phòng E có quyền Trưởng phòng duyệt hàng mượn và quản lý phòng P1; Trưởng phòng E2 '
     'có quyền nhưng chỉ quản lý phòng P2, bản thân E2 cũng thuộc P2.',
     '1. Nhân viên phòng P1 gửi một phiếu.\n2. Kiểm tra chuông thông báo của E và E2.',
     '—',
     '- E nhận thông báo "[PGHHM] Chờ duyệt: <mã phiếu>." kèm ghi chú (nếu có).\n'
     '- E2 KHÔNG nhận thông báo.\n'
     '- Bấm thông báo mở đúng màn chi tiết phiếu.'),
    ('018', 'Đính kèm file PDF', 'P1',
     'Đang ở màn Tạo mới.',
     '1. Tải lên 2 file PDF ở khối File đính kèm.\n2. Gửi duyệt.\n3. Mở chi tiết phiếu vừa gửi.',
     'File: hop_dong.pdf, bien_ban.pdf',
     '- Tải lên thành công, hiện đủ 2 file.\n'
     '- Màn chi tiết hiện 2 file, bấm mở xem được.'),
    ('019', 'Không đính kèm file vẫn gửi được', 'P1',
     'Đang ở màn Tạo mới, đã chọn phiếu và ngày.',
     '1. Không tải file nào.\n2. Bấm Gửi duyệt.',
     '—',
     '- Gửi thành công.\n'
     '- Màn chi tiết khối File đính kèm ghi "Không có file đính kèm."'),
    ('020', 'Cảnh báo khi rời màn Tạo mới chưa gửi', 'P1',
     'Đã chọn phiếu mượn và ngày mới, chưa gửi.',
     '1. Bấm nút quay lại hoặc bấm sang menu khác.',
     '—',
     '- Phần mềm hỏi xác nhận rời trang vì có dữ liệu chưa lưu.\n'
     '- Chọn ở lại: dữ liệu vẫn còn nguyên.'),
    ('021', 'Bấm Gửi duyệt hai lần liên tiếp', 'P0',
     'Đã điền đủ, mạng chậm.',
     '1. Bấm "Gửi duyệt" hai lần thật nhanh.',
     '—',
     '- Chỉ sinh ra MỘT phiếu gia hạn.\n'
     '- Danh sách không có hai phiếu trùng phiếu mượn đang chờ duyệt.'),
    ('022', 'Trưởng phòng thuộc chính phòng ban của phiếu nhận thông báo và duyệt được', 'P0',
     'Trưởng phòng E5 có quyền Trưởng phòng duyệt hàng mượn, bản thân thuộc phòng P1 nhưng KHÔNG '
     'được phân công quản lý phòng nào.',
     '1. Nhân viên phòng P1 gửi một phiếu.\n2. Kiểm tra chuông thông báo của E5.\n'
     '3. E5 bấm vào thông báo.',
     '—',
     '- E5 nhận thông báo "[PGHHM] Chờ duyệt: <mã phiếu>."\n'
     '- Mở đúng màn chi tiết, có nút "TP duyệt" và "Từ chối".\n'
     '- Lưu ý: trước đây người duyệt được nhưng không nhận thông báo (Redmine #11550), nay "duyệt '
     'được" và "nhận được thông báo" là cùng một nhóm người.'),
    ('023', 'Trưởng phòng tích "Quản lý tất cả phòng ban" nhận thông báo và duyệt được', 'P1',
     'Trưởng phòng E6 có quyền Trưởng phòng duyệt hàng mượn, được tích "Quản lý tất cả phòng ban" '
     'ở công ty 1, không thuộc phòng P1.',
     '1. Nhân viên phòng P1 (công ty 1) gửi một phiếu.\n2. Kiểm tra chuông thông báo của E6.\n'
     '3. E6 mở phiếu.',
     '—',
     '- E6 nhận thông báo "[PGHHM] Chờ duyệt: <mã phiếu>."\n'
     '- Phiếu có nút "TP duyệt" và "Từ chối" với E6.'),
    ('024', 'Sắp xếp trong popup chọn phiếu mượn', 'P2',
     'A có ít nhất 3 phiếu mượn đủ điều kiện, ngày tạo và ngày hẹn trả khác nhau.',
     '1. Mở popup chọn phiếu.\n2. Bấm lần lượt tiêu đề Mã phiếu, Ngày tạo, Ngày hẹn trả; mỗi cột '
     'bấm 2 lần.',
     '—',
     '- Mặc định phiếu tạo mới nhất ở đầu.\n'
     '- Ba cột Mã phiếu, Ngày tạo, Ngày hẹn trả đổi được tăng / giảm dần, dữ liệu xếp đúng.\n'
     '- Cột Ghi chú không sắp xếp được.'),
]

# ============================================================== V
S5 = [
    ('001', 'Bố cục màn chi tiết', 'P0',
     'Phiếu PGHHM-02930 ở trạng thái Chờ TP duyệt, có 2 file đính kèm.',
     '1. Mở chi tiết PGHHM-02930.',
     '—',
     '- Tiêu đề "Chi tiết yêu cầu gia hạn hàng mượn: PGHHM-02930".\n'
     '- Khối Thông tin chung, góc phải ghi "<người tạo> — <ngày giờ tạo>" (không còn nhãn trạng '
     'thái); các ô Mã phiếu, Phiếu yêu cầu xuất hàng mượn (liên kết), Người tạo, Phòng ban yêu cầu, '
     'Ngày hẹn trả, Ngày hẹn trả mới, Ngày tạo, Ghi chú.\n'
     '- Khối File đính kèm (xem / tải về, có cột Dung lượng), Chi tiết, Lịch sử thay đổi (thu gọn '
     'sẵn).\n'
     '- Mọi ô thông tin đều khoá (trừ trường hợp Kế toán ở TC_05.004).'),
    ('002', 'Đang tải không hiện như phiếu rỗng', 'P2',
     'Mạng chậm.',
     '1. Mở chi tiết một phiếu.',
     '—',
     '- Trong lúc chờ hiện "Đang tải dữ liệu phiếu...".\n'
     '- KHÔNG nhấp nháy dòng "Chưa chọn phiếu mượn".'),
    ('003', 'Liên kết phiếu mượn mở tab mới', 'P1',
     'Phiếu gắn với PYCXH-35542.',
     '1. Bấm vào PYCXH-35542 ở ô Phiếu yêu cầu xuất hàng mượn.',
     '—',
     '- Mở TAB MỚI màn chi tiết phiếu yêu cầu xuất hàng PYCXH-35542.'),
    ('004', 'Ô Ngày hẹn trả mới khoá / mở theo người xem', 'P0',
     'Phiếu X Chờ TP duyệt; phiếu Y Chờ KT duyệt.',
     '1. Trưởng phòng E mở X.\n2. Kế toán G mở Y.\n3. Người lập mở Y.',
     '—',
     '- E: ô khoá, biểu tượng chữ i ghi "Chỉ Kế toán được sửa lại ngày này, và chỉ khi phiếu đang '
     'chờ Kế toán duyệt."\n'
     '- G: ô mở khoá, có dấu bắt buộc.\n'
     '- Người lập: ô khoá.'),
    ('005', 'Số lượng hiển thị theo chuẩn quốc tế', 'P1',
     'Phiếu mượn có mặt hàng SL mượn 1,250 và đã trả 12.5.',
     '1. Mở chi tiết, xem bảng Chi tiết.',
     '—',
     '- SL mượn hiện "1,250"; Đã trả hiện "12.5" (không có số 0 thừa).\n'
     '- Dòng Tổng cộng cộng đúng hai cột.'),
    ('006', 'Khối Lịch sử duyệt liệt kê đủ các cấp đã đóng dấu', 'P0',
     'Phiếu đã qua Trưởng phòng E, Ban giám đốc F, Kế toán G (Đã duyệt).',
     '1. Mở chi tiết phiếu.',
     '—',
     '- Khối "Lịch sử duyệt" có 3 dòng theo thứ tự Trưởng phòng, Ban giám đốc, Kế toán.\n'
     '- Cột: STT, Cấp duyệt, Người duyệt, Thời gian, Ghi chú.\n'
     '- Lưu ý: ERP bỏ sót cấp Ban giám đốc ở khối này; hệ thống mới hiện đủ.'),
    ('007', 'Khối Lịch sử duyệt đánh dấu cấp đã từ chối', 'P0',
     'Phiếu bị Trưởng phòng E từ chối với lý do "Chưa trả hàng kỳ trước".',
     '1. Mở chi tiết phiếu.',
     '—',
     '- Có 1 dòng "Trưởng phòng" kèm nhãn đỏ "Từ chối", cột Ghi chú = "Chưa trả hàng kỳ trước".'),
    ('008', 'Phiếu chưa ai duyệt không có khối Lịch sử duyệt', 'P2',
     'Phiếu vừa lập, Chờ TP duyệt.',
     '1. Mở chi tiết phiếu.',
     '—',
     '- Không hiện khối "Lịch sử duyệt".'),
    ('009', 'Nút ở cuối màn theo trạng thái', 'P0',
     'Người lập A mở phiếu của mình ở từng trạng thái.',
     '1. Mở phiếu Chờ TP duyệt, Đã duyệt, Không duyệt.',
     '—',
     '- Cả ba chỉ có nút "In" và nút quay lại.\n'
     '- KHÔNG có nút Sửa, Xóa, Gửi lại (bị ẩn hẳn, không phải mờ).'),
    ('010', 'Người có quyền xem theo phòng ban mở phiếu phòng mình quản lý', 'P1',
     'D có quyền Xem theo phòng ban, quản lý P1. Phiếu Z thuộc P1 do người khác lập.',
     '1. D mở chi tiết Z từ danh sách.',
     '—',
     '- Xem được đầy đủ nội dung, không báo lỗi quyền.'),
    ('011', 'Người đã duyệt vẫn mở lại được phiếu', 'P0',
     'E chỉ có quyền Trưởng phòng duyệt, đã duyệt phiếu X (nay Chờ KT duyệt).',
     '1. E tìm X ở danh sách lối vào thường.\n2. Mở chi tiết X.',
     '—',
     '- X có trong danh sách của E.\n'
     '- Mở xem được, không có nút duyệt (đã qua cấp của E).'),
]

# ============================================================== VI
S6 = [
    ('001', 'Trưởng phòng duyệt phiếu dưới hạn mức sang thẳng Kế toán', 'P0',
     'Hạn mức giá trị hàng mượn công ty 1 = 20,000,000.\n'
     'Phiếu X (phòng P1) gắn phiếu mượn còn nợ 5,000,000. E quản lý P1.',
     '1. E mở X, bấm "TP duyệt".\n2. Đọc popup xác nhận, bấm "Duyệt".',
     '—',
     '- Popup "Xác nhận duyệt" ghi "Bạn xác nhận TP duyệt phiếu <mã>?", nút "Duyệt" màu xanh.\n'
     '- Thông báo "Yêu cầu đã được chuyển đến Kế toán."\n'
     '- Quay về danh sách; X ở trạng thái Chờ KT duyệt.\n'
     '- Ngày hẹn trả của phiếu mượn KHÔNG đổi.'),
    ('002', 'Trưởng phòng duyệt phiếu vượt hạn mức lên Ban giám đốc', 'P0',
     'Hạn mức công ty 1 = 20,000,000. Phiếu Y gắn phiếu mượn còn nợ 25,000,000.',
     '1. E mở Y, bấm "TP duyệt", xác nhận.',
     '—',
     '- Thông báo "Yêu cầu đã được chuyển đến Ban giám đốc."\n'
     '- Y ở trạng thái Chờ BGĐ duyệt.'),
    ('003', 'Giá trị còn nợ bằng đúng hạn mức không phải qua Ban giám đốc', 'P0',
     'Hạn mức 20,000,000. Phiếu gắn phiếu mượn còn nợ đúng 20,000,000.',
     '1. Trưởng phòng duyệt phiếu.',
     '—',
     '- Phiếu sang Chờ KT duyệt (chỉ LỚN HƠN hạn mức mới lên Ban giám đốc).'),
    ('004', 'Giá trị còn nợ chỉ tính phần chưa trả', 'P0',
     'Phiếu mượn có 1 dòng: xuất 10 cái, đã trả 6 cái, đơn giá 6,000,000 (còn nợ 24,000,000). '
     'Hạn mức 20,000,000.',
     '1. Trưởng phòng duyệt phiếu gia hạn của phiếu mượn này.',
     '—',
     '- Phiếu sang Chờ BGĐ duyệt (24,000,000 lớn hơn 20,000,000).\n'
     '- Nếu trả thêm 1 cái trước khi duyệt (còn nợ 18,000,000) thì sang thẳng Chờ KT duyệt.'),
    ('005', 'Ban giám đốc duyệt', 'P0',
     'Phiếu Y Chờ BGĐ duyệt; F có quyền Ban giám đốc duyệt hàng mượn, cùng công ty.',
     '1. F mở Y, bấm "BGĐ duyệt", xác nhận.',
     '—',
     '- Thông báo "Yêu cầu đã được chuyển đến Kế toán."\n'
     '- Quay về danh sách; Y ở Chờ KT duyệt.\n'
     '- Người có quyền Kế toán kho cùng công ty nhận thông báo "[PGHHM] Chờ duyệt: <mã>."'),
    ('006', 'Kế toán duyệt giữ nguyên ngày, phiếu mượn đổi hạn trả', 'P0',
     'Phiếu N Chờ KT duyệt, Ngày hẹn trả mới 05/10/2026, gắn phiếu mượn PYCXH-35542 hạn 23/09/2026.',
     '1. G mở N, không sửa ngày, bấm "KT duyệt".\n2. Đọc popup, bấm "Duyệt".\n'
     '3. Mở phiếu PYCXH-35542.',
     '—',
     '- Popup ghi "Duyệt bước Kế toán sẽ đổi ngày hẹn trả của phiếu mượn PYCXH-35542 sang 05/10/2026 '
     'ngay lập tức. Bạn có chắc chắn không?"\n'
     '- Thông báo "Duyệt phiếu thành công."; quay về danh sách; N Đã duyệt.\n'
     '- PYCXH-35542 có ngày hẹn trả mới là 05/10/2026.\n'
     '- Người lập nhận thông báo "[PGHHM] Đã duyệt: <mã>. Hạn trả mới: 05/10/2026."'),
    ('007', 'Kế toán sửa Ngày hẹn trả mới rồi duyệt', 'P0',
     'Phiếu N Chờ KT duyệt, Ngày hẹn trả mới 05/10/2026; hôm nay 30/09/2026, ngày trần 07/10/2026.',
     '1. G mở N, đổi Ngày hẹn trả mới sang 03/10/2026.\n2. Bấm "KT duyệt", xác nhận.\n'
     '3. Mở phiếu mượn và Lịch sử thay đổi của N.',
     'Ngày hẹn trả mới: 03/10/2026',
     '- Popup xác nhận nêu ngày 03/10/2026 (ngày vừa sửa).\n'
     '- Phiếu N Đã duyệt, Ngày hẹn trả mới = 03/10/2026.\n'
     '- Phiếu mượn có hạn trả 03/10/2026.\n'
     '- Lịch sử có dòng "Thay đổi thông tin" (Ngày hẹn trả mới: 05/10/2026 sang 03/10/2026) nằm '
     'NGAY DƯỚI dòng "Kế toán duyệt" (xảy ra trước).'),
    ('008', 'Kế toán xoá trống ô ngày rồi bấm duyệt', 'P1',
     'Phiếu N Chờ KT duyệt.',
     '1. G mở N, xoá ô Ngày hẹn trả mới (nếu xoá được).\n2. Bấm "KT duyệt".',
     '—',
     '- Báo lỗi dưới ô "Ngày hẹn trả mới – Bắt buộc phải chọn"; không mở popup xác nhận.\n'
     '- Phiếu không đổi trạng thái.'),
    ('009', 'Trưởng phòng / Ban giám đốc không sửa được ngày', 'P0',
     'Phiếu X Chờ TP duyệt, Ngày hẹn trả mới 05/10/2026.',
     '1. E mở X, thử bấm vào ô Ngày hẹn trả mới.\n2. Dùng công cụ kiểm thử gửi lệnh duyệt kèm ngày '
     '06/10/2026.',
     'Ngày hẹn trả mới: 06/10/2026',
     '- Bước 1: ô khoá, không mở được lịch.\n'
     '- Bước 2: phiếu vẫn được TP duyệt nhưng Ngày hẹn trả mới VẪN là 05/10/2026 (ngày gửi kèm bị '
     'bỏ qua).'),
    ('010', 'Hủy ở popup xác nhận duyệt', 'P1',
     'Phiếu X Chờ TP duyệt.',
     '1. E bấm "TP duyệt".\n2. Ở popup xác nhận chọn huỷ / đóng.',
     '—',
     '- Popup đóng, vẫn ở màn chi tiết; phiếu vẫn Chờ TP duyệt.'),
    ('011', 'Từ chối từ màn chi tiết', 'P0',
     'Phiếu X Chờ TP duyệt; E quản lý phòng của X.',
     '1. E mở X, bấm "Từ chối".\n2. Nhập lý do.\n3. Bấm "Xác nhận từ chối".',
     'Lý do từ chối: Chưa trả hàng kỳ trước',
     '- Popup tiêu đề "Từ chối yêu cầu gia hạn: <mã>", ô "Lý do từ chối" bắt buộc, dòng nhắc phiếu '
     'sẽ chuyển sang Không duyệt và người lập phải tạo phiếu mới.\n'
     '- Thông báo "Đã từ chối yêu cầu gia hạn hàng mượn."\n'
     '- Quay về danh sách; X ở trạng thái Không duyệt.\n'
     '- Ngày hẹn trả của phiếu mượn KHÔNG đổi.\n'
     '- Người lập nhận thông báo "[PGHHM] Từ chối: <mã>. Lý do: Chưa trả hàng kỳ trước"'),
    ('012', 'Từ chối từ menu dòng ở danh sách', 'P0',
     'Phiếu Y Chờ KT duyệt; G là Kế toán kho cùng công ty.',
     '1. Ở danh sách, chọn Hành động > Từ chối ở dòng Y.\n2. Nhập lý do, bấm "Xác nhận từ chối".',
     'Lý do từ chối: Sai phiếu mượn',
     '- Popup đóng, danh sách tự nạp lại, vẫn ở màn danh sách.\n'
     '- Dòng Y thành Không duyệt, menu Hành động chỉ còn In, Lịch sử.\n'
     '- Người duyệt / Ngày duyệt của Y hiện G và thời điểm từ chối.'),
    ('013', 'Từ chối ở cấp Ban giám đốc', 'P1',
     'Phiếu M Chờ BGĐ duyệt.',
     '1. F từ chối M với lý do.',
     'Lý do từ chối: Giá trị còn nợ quá lớn',
     '- M ở trạng thái Không duyệt.\n'
     '- Khối Lịch sử duyệt: dòng Trưởng phòng (đã duyệt) và dòng Ban giám đốc có nhãn "Từ chối" '
     'kèm lý do.'),
    ('014', 'Lý do từ chối bắt buộc', 'P0',
     'Đang mở popup Từ chối.',
     '1. Để trống ô lý do, bấm "Xác nhận từ chối".\n2. Nhập toàn khoảng trắng, bấm lại.',
     'Lý do từ chối: (trống)\nLý do từ chối: (5 dấu cách)',
     '- Cả hai lần đều báo "Lý do từ chối – Bắt buộc phải nhập", ô viền đỏ.\n'
     '- Popup không đóng, phiếu không đổi trạng thái.'),
    ('015', 'Đóng popup Từ chối không lưu', 'P2',
     'Đang mở popup Từ chối, đã gõ lý do.',
     '1. Bấm "Đóng".',
     '—',
     '- Popup đóng, phiếu vẫn giữ trạng thái chờ duyệt.'),
    ('016', 'Phiếu Không duyệt không duyệt tiếp được', 'P0',
     'Phiếu X đã Không duyệt.',
     '1. Super Admin mở X.\n2. Dùng công cụ kiểm thử gọi chức năng duyệt X.',
     '—',
     '- Không có nút duyệt / từ chối.\n'
     '- Gọi thẳng: phần mềm báo "Phiếu không ở trạng thái chờ duyệt."'),
    ('017', 'Phiếu Đã duyệt không duyệt lại được', 'P1',
     'Phiếu N Đã duyệt.',
     '1. Dùng công cụ kiểm thử gọi chức năng duyệt N bằng tài khoản Kế toán kho.',
     '—',
     '- Phần mềm báo "Phiếu không ở trạng thái chờ duyệt."; phiếu mượn không đổi hạn trả.'),
    ('018', 'Kế toán sửa ngày vượt trần', 'P0',
     'Hôm nay 30/09/2026, ngày trần 07/10/2026. Phiếu N Chờ KT duyệt.',
     '1. G mở lịch ô Ngày hẹn trả mới, thử chọn 08/10/2026.\n'
     '2. Dùng công cụ kiểm thử gửi lệnh duyệt kèm ngày 08/10/2026.',
     'Ngày hẹn trả mới: 08/10/2026',
     '- Bước 1: ngày 08/10 bị mờ, không chọn được.\n'
     '- Bước 2: báo "Không thể mượn quá 07/10/2026"; phiếu vẫn Chờ KT duyệt.'),
    ('019', 'Phiếu mượn đã được gia hạn xen giữa bởi phiếu khác', 'P0',
     'Phiếu mượn M có hạn 23/09. Phiếu gia hạn A1 (ngày mới 03/10) đã Đã duyệt nên hạn của M nay là '
     '03/10. Phiếu gia hạn A2 cũ của M (ngày mới 02/10) vẫn Chờ KT duyệt (lập bên cổng ERP).',
     '1. Kế toán mở A2, bấm "KT duyệt" giữ nguyên ngày 02/10.',
     '—',
     '- Báo lỗi dưới ô ngày "Phải sau ngày hẹn trả hiện tại (03/10/2026)".\n'
     '- A2 vẫn Chờ KT duyệt; hạn của M vẫn 03/10.'),
    ('020', 'Người duyệt sai phòng không thấy nút duyệt ở danh sách', 'P1',
     'E quản lý P1; phiếu Y Chờ TP duyệt thuộc P2.',
     '1. E xem dòng Y (nếu nhìn thấy trong phạm vi xem).',
     '—',
     '- Menu Hành động dòng Y không có Duyệt, Từ chối.'),
    ('021', 'Super Admin duyệt được mọi cấp', 'P1',
     'Super Admin cùng công ty với phiếu X Chờ TP duyệt thuộc phòng Super Admin không quản lý.',
     '1. Super Admin mở X, bấm "TP duyệt".',
     '—',
     '- Duyệt thành công (không bị ràng buộc phòng ban quản lý).'),
    ('022', 'Nhãn nút duyệt đổi theo cấp', 'P1',
     'Ba phiếu ở ba trạng thái chờ, người mở có quyền đúng cấp.',
     '1. Mở lần lượt từng phiếu.',
     '—',
     '- Chờ TP duyệt: nút "TP duyệt".\n'
     '- Chờ BGĐ duyệt: nút "BGĐ duyệt".\n'
     '- Chờ KT duyệt: nút "KT duyệt".'),
    ('023', 'Công ty chưa khai hạn mức giá trị hàng mượn', 'P1',
     'Công ty 3 để TRỐNG hạn mức giá trị hàng mượn. Phiếu X (công ty 3) gắn phiếu mượn còn nợ '
     '1,500,000.',
     '1. Trưởng phòng cùng công ty duyệt X.',
     '—',
     '- X sang Chờ BGĐ duyệt, thông báo "Yêu cầu đã được chuyển đến Ban giám đốc."\n'
     '- Lưu ý: hạn mức trống được coi là 0, nên mọi phiếu mượn còn nợ đều phải qua Ban giám đốc. '
     'Muốn bỏ bước này phải khai hạn mức cho công ty (Redmine #11550).'),
]

# ============================================================== VII
S7 = [
    ('001', 'Trưởng phòng bị chặn duyệt khi phòng có nhân viên mượn hàng quá hạn', 'P0',
     'Cấu hình chặn thao tác "Duyệt gia hạn hàng mượn" đang BẬT cho nhóm hàng mượn quá hạn.\n'
     'E quản lý P1; nhân viên V thuộc P1 đang có hàng mượn đã quá hạn trả.\n'
     'Phiếu X Chờ TP duyệt thuộc P1.',
     '1. E mở X, bấm "TP duyệt", xác nhận.',
     '—',
     '- Phần mềm báo "Phòng ban bạn quản lý có nhân viên hàng mượn quá hạn. Không thể thực hiện '
     'thao tác này."\n'
     '- Đồng thời mở cửa sổ liệt kê từng nhân viên đang quá hạn và loại hàng quá hạn.\n'
     '- X vẫn Chờ TP duyệt; không có dòng lịch sử mới.'),
    ('002', 'Không còn nhân viên quá hạn thì duyệt bình thường', 'P0',
     'Như TC_07.001, sau đó V đã trả hàng (hết quá hạn).',
     '1. E duyệt lại X.',
     '—',
     '- Duyệt thành công, X sang cấp tiếp theo.'),
    ('003', 'Tắt cấu hình chặn thì không chặn', 'P1',
     'Như TC_07.001 nhưng cấu hình chặn "Duyệt gia hạn hàng mượn" đang TẮT.',
     '1. E duyệt X.',
     '—',
     '- Duyệt thành công dù phòng còn nhân viên quá hạn.'),
    ('004', 'Từ chối không bị chặn quá hạn', 'P1',
     'Như TC_07.001.',
     '1. E bấm "Từ chối" phiếu X, nhập lý do, xác nhận.',
     'Lý do từ chối: Nhắc trả hàng quá hạn trước',
     '- Từ chối thành công, X thành Không duyệt.'),
    ('005', 'Super Admin không bị chặn', 'P2',
     'Super Admin quản lý phòng P1 đang có nhân viên quá hạn.',
     '1. Super Admin duyệt phiếu Chờ TP duyệt của P1.',
     '—',
     '- Duyệt thành công.'),
    ('006', 'Kế toán / Ban giám đốc quản lý phòng có nhân viên quá hạn', 'P1',
     'Kế toán G (quyền Kế toán kho) đồng thời được phân công quản lý phòng P3; P3 có nhân viên '
     'mượn hàng quá hạn. Cấu hình chặn đang bật. Phiếu N Chờ KT duyệt.',
     '1. G bấm "KT duyệt" phiếu N.',
     '—',
     '- Phần mềm CŨNG chặn với cùng thông báo như TC_07.001.\n'
     '- Lưu ý: chốt chặn gắn trên thao tác duyệt nói chung, xét theo phòng ban NGƯỜI DUYỆT quản lý, '
     'không riêng cấp Trưởng phòng.'),
]

# ============================================================== VIII
S8 = [
    ('001', 'In một phiếu từ màn chi tiết', 'P0',
     'Phiếu N Đã duyệt, qua đủ 3 cấp, phiếu mượn có 3 mặt hàng.',
     '1. Mở chi tiết N, bấm "In".',
     '—',
     '- Mở popup xem trước "Xem trước yêu cầu gia hạn hàng mượn <mã>" (không mở tab mới), khổ DỌC.\n'
     '- Tiêu đề "PHIẾU YÊU CẦU GIA HẠN HÀNG MƯỢN", có mã phiếu và ngày lập, đầu trang là header '
     'công ty CỦA PHIẾU.\n'
     '- Thông tin: Người yêu cầu, Phòng ban, Phiếu mượn, Ngày hẹn trả cũ, Ngày hẹn trả mới, Trạng '
     'thái, Ghi chú.\n'
     '- Bảng hàng 3 dòng + Tổng cộng; bảng cấp duyệt 3 dòng; 4 ô ký Người lập, Trưởng phòng, Ban '
     'giám đốc, Kế toán.'),
    ('002', 'In phiếu từ menu dòng ở danh sách', 'P1',
     'Có phiếu bất kỳ trong phạm vi.',
     '1. Chọn Hành động > In ở một dòng.',
     '—',
     '- Popup xem trước giống hệt khi in từ màn chi tiết.'),
    ('003', 'In phiếu bị từ chối', 'P1',
     'Phiếu bị Trưởng phòng từ chối.',
     '1. In phiếu.',
     '—',
     '- Bảng cấp duyệt ghi "Trưởng phòng (không duyệt)" kèm lý do.\n'
     '- Trạng thái ghi "Không duyệt".'),
    ('004', 'In phiếu chưa ai duyệt, ô rỗng để trống', 'P2',
     'Phiếu vừa lập, không có ghi chú.',
     '1. In phiếu.',
     '—',
     '- Không có bảng cấp duyệt.\n- Ô Ghi chú để TRỐNG, không in dấu gạch.'),
    ('005', 'In danh sách theo bộ lọc', 'P0',
     'Đã lọc Trạng thái = Đã duyệt, Ngày tạo 01/09/2026 - 30/09/2026, ra 25 phiếu (3 trang).',
     '1. Bấm nút "In" trên thanh công cụ.',
     'Trạng thái: Đã duyệt\nNgày tạo: 01/09/2026 - 30/09/2026',
     '- Popup "Xem trước danh sách yêu cầu gia hạn hàng mượn", khổ ngang.\n'
     '- Tiêu đề "DANH SÁCH PHIẾU YÊU CẦU GIA HẠN HÀNG MƯỢN"; "Khoảng thời gian: Từ ngày 01/09/2026 '
     'đến ngày 30/09/2026"; "Tổng số phiếu: 25".\n'
     '- In đủ 25 phiếu (không chỉ trang đang xem), cột: STT, Mã phiếu, Phiếu mượn, Người tạo, Ngày '
     'tạo, Ngày hẹn trả cũ, Ngày hẹn trả mới, Trạng thái, Người duyệt, Ngày duyệt.'),
    ('006', 'In danh sách không có dữ liệu', 'P2',
     'Bộ lọc không ra phiếu nào.',
     '1. Bấm "In".',
     '—',
     '- Bản in ghi "Không có dữ liệu", Tổng số phiếu: 0.'),
    ('007', 'Popup chọn trường xuất Excel tick sẵn cột đang hiện', 'P0',
     'Cấu hình cột mặc định.',
     '1. Bấm "Xuất Excel".',
     '—',
     '- Popup "Chọn trường xuất Excel" có 12 trường: Mã phiếu, Phiếu mượn, Người tạo, Ngày tạo, Ngày '
     'hẹn trả cũ, Ngày hẹn trả mới, Trạng thái, Người duyệt, Ngày duyệt, Phòng ban, Ghi chú, Lý do '
     'từ chối.\n'
     '- Tick sẵn 9 trường đang hiện trên bảng; Phòng ban, Ghi chú, Lý do từ chối chưa tick.'),
    ('008', 'Nội dung file Excel', 'P0',
     'Đã lọc Ngày tạo 01/09/2026 - 30/09/2026, ra 25 phiếu.',
     '1. Xuất Excel với các trường tick sẵn.\n2. Mở file.',
     'Ngày tạo: 01/09/2026 - 30/09/2026',
     '- Thông báo "Xuất Excel thành công"; tên file danh_sach_yeu_cau_gia_han_hang_muon.xlsx, sheet '
     '"Yêu cầu gia hạn hàng mượn".\n'
     '- Dòng 1 "DANH SÁCH PHIẾU YÊU CẦU GIA HẠN HÀNG MƯỢN"; dòng 2 "Từ ngày 01/09/2026 đến ngày '
     '30/09/2026".\n'
     '- Cột STT luôn đứng đầu, 25 dòng dữ liệu khớp màn hình.\n'
     '- Cuối file có khối ký "Ngày…….Tháng…….Năm…….", "Người lập", "(Ký, họ tên)".'),
    ('009', 'Thứ tự cột Excel theo thứ tự tick', 'P1',
     'Mở popup xuất Excel.',
     '1. Bỏ tick hết, tick lần lượt: Trạng thái, Mã phiếu, Lý do từ chối.\n2. Xuất và mở file.',
     '—',
     '- File có đúng 4 cột theo thứ tự: STT, Trạng thái, Mã phiếu, Lý do từ chối.'),
    ('010', 'Xuất Excel không lọc ngày thì không có dòng khoảng ngày', 'P2',
     'Không lọc Ngày tạo.',
     '1. Xuất Excel, mở file.',
     '—',
     '- Dòng tiêu đề nằm ngay trên dòng tên cột, không có dòng "Từ ngày...".'),
    ('011', 'Excel giữ đúng dạng mã và ngày', 'P1',
     'Xuất một file bất kỳ.',
     '1. Mở file, bấm vào ô mã phiếu và ô ngày.',
     '—',
     '- Mã phiếu PGHHM-xxxxx không bị cảnh báo "số lưu dạng chữ".\n'
     '- Ngày hiện dd/mm/yyyy (hoặc dd/mm/yyyy hh:mm), không bị Excel đổi định dạng.\n'
     '- Ô không có dữ liệu để TRỐNG.'),
    ('012', 'Xuất Excel và In danh sách tuân phạm vi quyền', 'P0',
     'Tài khoản A không có quyền xem, lập 6 phiếu.',
     '1. A xuất Excel và in danh sách, không lọc gì.',
     '—',
     '- Cả file Excel và bản in đều chỉ có 6 phiếu của A.'),
    ('013', 'Xuất Excel ở lối vào "chờ duyệt"', 'P1',
     'Kế toán kho ở lối vào "chờ duyệt" đang thấy 3 phiếu.',
     '1. Xuất Excel.',
     '—',
     '- File có đúng 3 phiếu đang chờ Kế toán duyệt.'),
]

# ============================================================== IX
S9 = [
    ('001', 'Gửi khi chưa chọn gì', 'P0',
     'Đang ở màn Tạo mới, form trống.',
     '1. Bấm "Gửi duyệt".',
     '—',
     '- Báo lỗi dưới ô phiếu "Phiếu yêu cầu xuất hàng mượn – Bắt buộc phải chọn".\n'
     '- Báo lỗi dưới ô ngày "Ngày hẹn trả mới – Bắt buộc phải chọn".\n'
     '- Kèm thông báo góc màn hình "Bạn chưa nhập đầy đủ thông tin."\n'
     '- Màn cuộn tới lỗi đầu tiên; không sinh phiếu.'),
    ('002', 'Lỗi tự tắt khi đã chọn ngày', 'P1',
     'Đang có lỗi đỏ ở ô Ngày hẹn trả mới.',
     '1. Chọn một ngày hợp lệ.',
     '—',
     '- Viền đỏ và dòng lỗi dưới ô biến mất ngay, không cần bấm Gửi lại.'),
    ('003', 'Ghi chú tối đa 255 ký tự', 'P1',
     'Đang ở màn Tạo mới.',
     '1. Dán đoạn văn 300 ký tự vào ô Ghi chú.',
     'Ghi chú: 300 ký tự',
     '- Ô chỉ nhận 255 ký tự đầu.'),
    ('004', 'Lý do từ chối tối đa 255 ký tự', 'P2',
     'Đang mở popup Từ chối.',
     '1. Dán đoạn 300 ký tự vào ô lý do.',
     'Lý do: 300 ký tự',
     '- Ô chỉ nhận 255 ký tự.'),
    ('005', 'Chỉ nhận file PDF', 'P0',
     'Đang ở màn Tạo mới.',
     '1. Tải lên file bao_gia.docx.\n2. Tải lên file anh.jpg.',
     'File: bao_gia.docx\nFile: anh.jpg',
     '- Cả hai đều bị từ chối, báo chỉ nhận file PDF; không có file nào được thêm.'),
    ('006', 'File vượt 13 MB', 'P1',
     'Có file PDF 15 MB.',
     '1. Tải lên file 15 MB.',
     'File: tai_lieu_15MB.pdf',
     '- Bị từ chối, báo file không được quá 13 MB.'),
    ('007', 'Gọi thẳng chức năng lập phiếu với ngày hôm nay', 'P1',
     'Hôm nay 30/09/2026; phiếu mượn đủ điều kiện, hạn 23/09.',
     '1. Dùng công cụ kiểm thử gửi lệnh lập phiếu với Ngày hẹn trả mới 30/09/2026.',
     'Ngày hẹn trả mới: 30/09/2026',
     '- Bị từ chối, lỗi ô Ngày hẹn trả mới "Phải sau ngày hôm nay"; không sinh phiếu.'),
    ('008', 'Gọi thẳng chức năng lập phiếu với ngày vượt trần', 'P0',
     'Hôm nay 30/09/2026, ngày trần 07/10/2026.',
     '1. Dùng công cụ kiểm thử gửi lệnh lập phiếu với Ngày hẹn trả mới 10/10/2026.',
     'Ngày hẹn trả mới: 10/10/2026',
     '- Bị từ chối, báo "Không thể mượn quá 07/10/2026"; không sinh phiếu.'),
    ('009', 'Gọi thẳng chức năng lập phiếu với ngày không sau hạn trả hiện tại', 'P0',
     'Phiếu mượn hạn trả 03/10/2026.',
     '1. Dùng công cụ kiểm thử gửi lệnh lập phiếu với Ngày hẹn trả mới 03/10/2026.',
     'Ngày hẹn trả mới: 03/10/2026',
     '- Bị từ chối, báo "Phải sau ngày hẹn trả hiện tại (03/10/2026)"; không sinh phiếu.'),
    ('010', 'Gọi thẳng chức năng lập phiếu cho phiếu mượn của người khác', 'P0',
     'Phiếu mượn M (mã PYCXH-35542) thuộc nhân viên B; đăng nhập bằng A.',
     '1. Dùng công cụ kiểm thử gửi lệnh lập phiếu gia hạn cho M.',
     '—',
     '- Bị từ chối, lỗi "Không thể gia hạn yêu cầu này: chỉ người lập phiếu PYCXH-35542 mới được '
     'gia hạn."; không sinh phiếu.'),
    ('011', 'Gọi thẳng chức năng lấy dữ liệu phiếu mượn không đủ điều kiện', 'P2',
     'Phiếu mượn M (mã PYCXH-35542) của A đang có yêu cầu gia hạn PGHHM-02950 Chờ TP duyệt.',
     '1. Đăng nhập A, dùng công cụ kiểm thử gọi chức năng lấy dữ liệu phiếu mượn M để lập phiếu.',
     '—',
     '- Báo "Không thể gia hạn yêu cầu này: phiếu PYCXH-35542 đang có yêu cầu gia hạn PGHHM-02950 '
     '(Chờ TP duyệt) chưa duyệt xong. Chờ yêu cầu đó được duyệt hoặc từ chối rồi mới lập yêu cầu '
     'mới."\n'
     '- Lưu ý: câu báo nêu đúng LÝ DO đầu tiên gặp phải (Redmine #11529), không còn câu chung '
     'chung.'),
    ('012', 'Ngày gõ tay sai định dạng', 'P2',
     'Dùng công cụ kiểm thử.',
     '1. Gửi lệnh lập phiếu với Ngày hẹn trả mới "31/02/2026".',
     'Ngày hẹn trả mới: 31/02/2026',
     '- Bị từ chối, lỗi ô Ngày hẹn trả mới "Không hợp lệ".'),
]

# ============================================================== X
S10 = [
    ('001', 'Lập phiếu thứ hai khi phiếu đầu còn chờ duyệt', 'P0',
     'A mở màn Tạo mới ở 2 tab, cả hai đều đã chọn cùng phiếu mượn M.',
     '1. Tab 1 bấm "Gửi duyệt" (thành công).\n2. Tab 2 bấm "Gửi duyệt".',
     '—',
     '- Tab 2 báo lỗi dưới ô phiếu (kèm thông báo góc màn hình) "Không thể gia hạn yêu cầu này: '
     'phiếu <mã M> đang có yêu cầu gia hạn <mã phiếu tab 1> (Chờ TP duyệt) chưa duyệt xong. Chờ yêu '
     'cầu đó được duyệt hoặc từ chối rồi mới lập yêu cầu mới."\n'
     '- M chỉ có MỘT phiếu gia hạn đang chờ duyệt.'),
    ('002', 'Hai Trưởng phòng cùng duyệt một phiếu', 'P1',
     'E và E3 cùng quản lý P1, cùng mở phiếu X Chờ TP duyệt.',
     '1. E bấm TP duyệt (thành công).\n2. E3 bấm TP duyệt ngay sau.',
     '—',
     '- E3 bị từ chối (phiếu đã sang cấp khác), báo không có quyền duyệt bước này.\n'
     '- Lịch sử chỉ có MỘT dòng "Trưởng phòng duyệt".'),
    ('003', 'Một người duyệt, người khác từ chối cùng lúc', 'P1',
     'Hai Kế toán kho G và G2 cùng mở phiếu N Chờ KT duyệt.',
     '1. G bấm KT duyệt (thành công).\n2. G2 mở popup Từ chối, nhập lý do, xác nhận.',
     'Lý do từ chối: Test đồng thời',
     '- G2 bị từ chối, popup hiện lỗi "Bạn không có quyền từ chối phiếu này."\n'
     '- N vẫn Đã duyệt; phiếu mượn giữ ngày mới.'),
    ('004', 'Người duyệt ở công ty khác không thấy phiếu', 'P0',
     'Kế toán kho H thuộc công ty 4; công ty 1 có 3 phiếu Chờ KT duyệt.',
     '1. H mở lối vào "chờ duyệt".',
     '—',
     '- Danh sách không có 3 phiếu của công ty 1.'),
    ('005', 'Trưởng phòng công ty khác trùng phòng ban không duyệt được', 'P1',
     'Trưởng phòng E4 thuộc công ty 4 nhưng được gán quản lý một phòng ban trùng với phòng của phiếu '
     'X (công ty 1).',
     '1. Dùng công cụ kiểm thử gọi chức năng duyệt X bằng E4.',
     '—',
     '- Bị từ chối "Bạn không có quyền duyệt bước này."\n'
     '- Lưu ý: ERP cho qua trường hợp này; hệ thống mới đã chặn.'),
    ('006', 'Bộ lọc không làm lộ phiếu ngoài phạm vi ở lối "chờ duyệt"', 'P0',
     'Trưởng phòng E (có thêm Kế toán kho để thấy menu) quản lý P1. P2 có phiếu Chờ TP duyệt do '
     'nhân viên X lập.',
     '1. E mở lối vào "chờ duyệt".\n2. Lọc Người tạo = X.\n3. Lọc Trạng thái = Chờ TP duyệt.',
     'Người tạo: X\nTrạng thái: Chờ TP duyệt',
     '- Không ra phiếu nào của P2.'),
    ('007', 'Phiếu Không duyệt hiện theo phạm vi quyền', 'P0',
     'Phiếu X do B lập, bị Trưởng phòng E từ chối. C có quyền Xem theo công ty.',
     '1. C lọc Trạng thái = Không duyệt.\n2. E (chỉ có quyền Trưởng phòng duyệt) mở danh sách.',
     'Trạng thái: Không duyệt',
     '- C thấy X.\n'
     '- E vẫn thấy X (người đã từ chối), bấm vào mở được.\n'
     '- Lưu ý: ERP giấu phiếu Không duyệt với mọi người trừ người lập; hệ thống mới đã bỏ luật này.'),
    ('008', 'Quyền tổng công ty thấy và mở phiếu công ty khác nhưng không duyệt được', 'P1',
     'B có quyền Xem theo tổng công ty và quyền Kế toán kho (công ty 1). Phiếu W thuộc công ty 4, '
     'đang Chờ KT duyệt.',
     '1. B tìm W ở danh sách lối vào thường.\n2. Bấm mở W.\n3. B mở lối vào "chờ duyệt".',
     '—',
     '- Bước 1: W CÓ trong danh sách (danh sách và màn chi tiết nay khớp nhau, Redmine #11534).\n'
     '- Bước 2: xem được nội dung W, KHÔNG có nút duyệt / từ chối (khác công ty).\n'
     '- Bước 3: W KHÔNG có trong danh sách chờ duyệt.'),
]

# ============================================================== XI
S11 = [
    ('001', 'Khối Lịch sử thay đổi thu gọn sẵn có đếm số mốc', 'P1',
     'Phiếu đã qua tạo và Trưởng phòng duyệt.',
     '1. Mở chi tiết phiếu.',
     '—',
     '- Khối "Lịch sử thay đổi" đang thu gọn, cạnh tiêu đề có số 2.\n'
     '- Bấm "Xem lịch sử" thì mở ra; nút đổi thành "Thu gọn" và có thêm nút "Làm mới".'),
    ('002', 'Nút Bộ lọc của lịch sử chỉ hiện khi có mốc', 'P2',
     'Phiếu A có 2 mốc lịch sử; phiếu B lập và xử lý hoàn toàn bên cổng ERP cũ (không có mốc nào).',
     '1. Mở Lịch sử thay đổi của A.\n2. Mở Lịch sử thay đổi của B.',
     '—',
     '- A: có nút "Bộ lọc" phía trên danh sách mốc.\n'
     '- B: KHÔNG có nút "Bộ lọc", chỉ có dòng "Chưa có lịch sử thao tác nào."'),
    ('003', 'Phiếu xử lý bên cổng cũ không có lịch sử', 'P0',
     'Phiếu cũ được lập và duyệt hoàn toàn bên ERP.',
     '1. Mở chi tiết, mở Lịch sử thay đổi.\n2. Ở danh sách chọn Hành động > Lịch sử.',
     '—',
     '- Cả hai nơi ghi "Chưa có lịch sử thao tác nào."\n'
     '- Không có badge số cạnh tiêu đề.\n'
     '- Đây là đúng thiết kế, không phải lỗi mất dữ liệu.'),
    ('004', 'Lịch sử đủ vòng đời, mới nhất ở trên', 'P0',
     'Phiếu tạo trên hệ thống mới, qua TP duyệt, BGĐ duyệt, Kế toán sửa ngày rồi duyệt.',
     '1. Mở Lịch sử thay đổi.',
     '—',
     '- 5 dòng theo thứ tự từ trên xuống: Kế toán duyệt, Thay đổi thông tin, Ban giám đốc duyệt, '
     'Trưởng phòng duyệt, Tạo phiếu.\n'
     '- Mỗi dòng có thời điểm dd/mm/yyyy hh:mm và "Người thực hiện: <tên> - <phòng ban>".'),
    ('005', 'Dòng Tạo phiếu ghi giá trị ban đầu', 'P1',
     'Phiếu vừa tạo, Ngày hẹn trả mới 05/10/2026, Ghi chú "Khách chưa nghiệm thu xong", 1 file.',
     '1. Mở Lịch sử thay đổi.',
     '—',
     '- Dòng "Tạo phiếu" liệt kê Trạng thái: Chờ TP duyệt, Ngày hẹn trả mới: 05/10/2026, Ghi chú, '
     'File đính kèm.'),
    ('006', 'Dòng duyệt ghi đổi trạng thái', 'P1',
     'Phiếu vừa được TP duyệt sang Chờ KT duyệt.',
     '1. Mở Lịch sử thay đổi.',
     '—',
     '- Dòng "Trưởng phòng duyệt" ghi Trạng thái: Chờ TP duyệt sang Chờ KT duyệt.'),
    ('007', 'Dòng Không duyệt hiện lý do', 'P0',
     'Phiếu bị từ chối với lý do "Chưa trả hàng kỳ trước".',
     '1. Mở Lịch sử thay đổi (ở màn chi tiết và ở popup danh sách).',
     '—',
     '- Dòng "Không duyệt" màu đỏ, Trạng thái đổi sang Không duyệt.\n'
     '- Khối ghi chú của dòng hiện "Chưa trả hàng kỳ trước".\n'
     '- Nội dung ở popup danh sách giống hệt ở màn chi tiết.'),
    ('008', 'Kế toán duyệt không đổi ngày thì không có dòng Thay đổi thông tin', 'P1',
     'Phiếu Chờ KT duyệt.',
     '1. Kế toán duyệt giữ nguyên ngày.\n2. Mở lịch sử.',
     '—',
     '- Không có dòng "Thay đổi thông tin", chỉ thêm dòng "Kế toán duyệt".'),
    ('009', 'Popup Lịch sử ở danh sách', 'P1',
     'Có phiếu có 3 mốc lịch sử.',
     '1. Chọn Hành động > Lịch sử ở dòng đó.',
     '—',
     '- Popup "Lịch sử yêu cầu gia hạn hàng mượn" kèm mã phiếu, hiện đủ 3 mốc.'),
    ('010', 'Bộ lọc trong lịch sử', 'P2',
     'Phiếu có 5 mốc lịch sử do 4 người thực hiện.',
     '1. Mở lịch sử, bấm "Bộ lọc".\n2. Mở ô Loại hành động.\n3. Chọn Loại hành động = Thay đổi '
     'thông tin.\n4. Chọn Người thực hiện = Kế toán G.',
     '—',
     '- Có các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày.\n'
     '- Ô Loại hành động chỉ liệt kê những loại ĐÃ CÓ trong lịch sử của chính phiếu này.\n'
     '- Lọc đúng các mốc khớp; không khớp thì ghi "Không có lịch sử phù hợp bộ lọc."'),
    ('011', 'Làm mới lịch sử sau thao tác', 'P2',
     'Đang mở khối lịch sử ở tab 1; tab 2 vừa có người duyệt phiếu.',
     '1. Bấm "Làm mới" trong khối lịch sử tab 1.',
     '—',
     '- Mốc duyệt mới hiện lên đầu danh sách.'),
]

# ============================================================== XII
S12 = [
    ('001', 'Luồng đầy đủ dưới hạn mức', 'P0',
     'Nhân viên A (phòng P1) có phiếu mượn M hạn 23/09/2026, còn nợ 5,000,000; hạn mức 20,000,000.',
     '1. A lập phiếu gia hạn M sang 05/10/2026.\n2. Trưởng phòng E duyệt.\n3. Kế toán G duyệt.\n'
     '4. Kiểm tra M và popup chọn phiếu của A.',
     'Ngày hẹn trả mới: 05/10/2026',
     '- Sau bước 1: Chờ TP duyệt; M vẫn 23/09.\n'
     '- Sau bước 2: Chờ KT duyệt (bỏ qua BGĐ); M vẫn 23/09.\n'
     '- Sau bước 3: Đã duyệt; M đổi hạn 05/10/2026.\n'
     '- M quay lại popup chọn phiếu của A với Ngày hẹn trả 05/10/2026 (nếu còn trước ngày trần).'),
    ('002', 'Luồng đầy đủ vượt hạn mức', 'P0',
     'Phiếu mượn M còn nợ 25,000,000; hạn mức 20,000,000.',
     '1. Lập phiếu gia hạn.\n2. TP duyệt.\n3. BGĐ duyệt.\n4. KT sửa ngày rồi duyệt.',
     '—',
     '- Trạng thái đi đúng: Chờ TP duyệt, Chờ BGĐ duyệt, Chờ KT duyệt, Đã duyệt.\n'
     '- M đổi hạn đúng ngày Kế toán đã sửa.\n'
     '- Lịch sử duyệt ở chi tiết có đủ 3 cấp; Lịch sử thay đổi có 5 mốc.'),
    ('003', 'Từ chối rồi lập phiếu mới', 'P0',
     'Phiếu gia hạn X của M bị TP từ chối.',
     '1. Người lập mở X tìm cách gửi lại.\n2. Vào Tạo mới, chọn lại M, gửi phiếu mới.\n'
     '3. TP và KT duyệt phiếu mới.',
     '—',
     '- X không có nút gửi lại / sửa, giữ Không duyệt.\n'
     '- M có trong popup chọn phiếu ngay sau khi X bị từ chối.\n'
     '- Phiếu mới đi hết luồng, M đổi hạn; X vẫn Không duyệt.'),
    ('004', 'Gia hạn hai lần liên tiếp cùng phiếu mượn', 'P0',
     'Phiếu mượn M hạn 23/09. Số ngày mượn tối đa 7.',
     '1. Lập và duyệt xong phiếu gia hạn M sang 03/10.\n2. Lập tiếp phiếu gia hạn M.',
     '—',
     '- Lần 2, Ngày hẹn trả hiện 03/10/2026; lịch chỉ cho chọn từ 04/10 đến ngày trần.\n'
     '- Không lập được phiếu có ngày mới trùng hoặc trước 03/10.'),
    ('005', 'Kiểm tra chéo với màn Hàng sắp hết hạn mượn / Danh sách hàng mượn', 'P1',
     'Vừa duyệt xong phiếu gia hạn M sang 05/10/2026.',
     '1. Mở Tài chính > Mượn hàng > Danh sách hàng mượn, tìm hàng của M.\n'
     '2. Mở Hàng sắp hết hạn mượn.',
     '—',
     '- Hạn trả của hàng thuộc M hiện 05/10/2026.\n'
     '- M không còn nằm trong diện sắp hết hạn theo hạn cũ.'),
    ('006', 'Từ chối không đụng phiếu mượn', 'P1',
     'Phiếu gia hạn M đã qua TP, đang Chờ KT duyệt.',
     '1. Kế toán từ chối.\n2. Mở phiếu mượn M.',
     'Lý do từ chối: Không đủ chứng từ',
     '- Hạn trả của M giữ nguyên như trước khi lập phiếu gia hạn.'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & LỐI VÀO', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP PHIẾU (TẠO MỚI)', S4),
    ('V', 'XEM CHI TIẾT', S5),
    ('VI', 'DUYỆT & TỪ CHỐI', S6),
    ('VII', 'CHẶN DUYỆT KHI CÒN HÀNG MƯỢN QUÁ HẠN', S7),
    ('VIII', 'IN & XUẤT EXCEL', S8),
    ('IX', 'RÀNG BUỘC NHẬP LIỆU', S9),
    ('X', 'CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI', S10),
    ('XI', 'LỊCH SỬ THAY ĐỔI', S11),
    ('XII', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S12),
]

build(output_file=os.path.join(BASE, 'testcase - Phieu yeu cau gia han hang muon.xlsx'),
      sheet_name='Trang tính1',
      feature_name='Phiếu yêu cầu gia hạn hàng mượn',
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
