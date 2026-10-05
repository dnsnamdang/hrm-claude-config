# -*- coding: utf-8 -*-
"""Sinh "testcase - Phieu huy hang giu ke toan.xlsx" (phan he Tai chinh, nhom Giu hang).

Man ANH EM cua "Phieu huy hang giu" thuong (../finance-prepick-cancel-request/gen_testcase_phieu_huy.py)
nhung KHAC HAN luong: khong co phieu yeu cau, ke toan huy THANG hang giu cua 1 nhan vien,
1 hang hoa -> nhieu khach hang, chon duoc DVT.

Viet tu code HRM nhanh `gop_db` (worktree .worktrees/gop-db ca 2 repo, gom thay doi CHUA commit
cua dot Redmine #11524) ngay 30/09/2026.
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

MODULE = 'Phiếu huỷ hàng giữ kế toán'
MENU = 'Tài chính > nhóm Giữ hàng > Phiếu huỷ hàng giữ kế toán'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn hình Phiếu huỷ hàng giữ kế toán (mã phiếu KTPHHG-xxxxx) cho kế toán HUỶ THẲNG hàng đang '
     'giữ của một nhân viên, KHÔNG cần phiếu yêu cầu và KHÔNG có vòng duyệt.\n'
     'Một phiếu gồm nhiều hàng hoá; mỗi hàng hoá huỷ cho một hoặc nhiều khách hàng mà nhân viên đó '
     'đang giữ hàng; mỗi dòng khách hàng chọn được đơn vị tính.\n'
     'Bấm "Duyệt" = lưu phiếu và TRỪ hàng giữ ngay theo thứ tự hạn giữ sớm trước. Phiếu lập xong là '
     'chốt vĩnh viễn: không sửa, không xoá, không huỷ duyệt.\n'
     'Sau khi lập, nhân viên bị huỷ hàng nhận được thông báo kèm đường dẫn tới phiếu.\n'
     'Đường dẫn: Phân hệ Tài chính > nhóm Giữ hàng > Phiếu huỷ hàng giữ kế toán.'),
    ('2. Đối tượng được tính / hiển thị',
     'Danh sách phiếu:\n'
     '- Người có quyền "Quản lý giữ hàng": thấy phiếu có CÔNG TY PHIẾU = công ty của mình. Công ty '
     'phiếu là công ty của NGƯỜI LẬP phiếu, không phải công ty của nhân viên bị huỷ hàng.\n'
     '- Tài khoản quản trị cao nhất: thấy phiếu của mọi công ty và có thêm ô lọc "Công ty".\n'
     'Ô "Huỷ của nhân viên" trên form lập: toàn bộ nhân viên đang làm việc (mọi công ty) — giữ đúng '
     'như hệ thống cũ.\n'
     'Cửa sổ "Hàng đang giữ của nhân viên": hàng hoá nhân viên đã chọn còn đang giữ (số giữ lớn hơn '
     '0) cho MỌI khách hàng, thuộc công ty của chính nhân viên đó; hàng đang ngừng kinh doanh hoặc '
     'đã xoá không hiện.\n'
     'Ô "Khách hàng" của một hàng hoá: chỉ những khách hàng mà nhân viên còn số CÓ THỂ HUỶ lớn hơn 0 '
     'cho hàng đó, mỗi khách một dòng, xếp theo tên khách.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Người không có quyền "Quản lý giữ hàng" (và không phải tài khoản quản trị cao nhất): không '
     'xem được danh sách, chi tiết, bản in, tệp Excel; không lập được phiếu.\n'
     '- Phiếu có công ty phiếu khác công ty người đăng nhập: không hiện ở danh sách, mở bằng đường '
     'dẫn trực tiếp thì bị từ chối.\n'
     '- Trong cửa sổ chọn hàng: hàng hoá ĐÃ có trên phiếu bị ẩn hẳn (không phải hiện rồi khoá).\n'
     '- Trong ô Khách hàng: khách hàng đã được chọn ở dòng khác của CÙNG hàng hoá không hiện lại.\n'
     '- Khách hàng có số giữ nhưng toàn bộ đang nằm trong đề nghị xuất kho chưa hoàn tất (số có thể '
     'huỷ = 0): không có trong ô Khách hàng.\n'
     '- Màn hình KHÔNG có nút Sửa, Xoá, Huỷ duyệt ở bất kỳ đâu.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Ô lọc "Ngày tạo" (chọn một khoảng ngày) lọc theo NGÀY LẬP PHIẾU.\n'
     'Khoảng ngày lấy TRỌN hai đầu mút (phiếu lập lúc 23:59 ngày cuối vẫn được tính).\n'
     'Khi có lọc ngày, bản in danh sách và tệp Excel có thêm dòng "Từ ngày dd/mm/yyyy đến ngày '
     'dd/mm/yyyy".'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Phiếu (Mã phiếu, Huỷ của nhân viên, Ghi chú, Người tạo, Ngày tạo)\n'
     '  gồm nhiều Hàng hoá (Tên, Model, Mã hàng hóa, Thương hiệu — chụp lại tại lúc lập phiếu)\n'
     '    mỗi hàng hoá gồm nhiều dòng Khách hàng (Khách hàng, Duyệt huỷ, ĐVT).\n'
     'Bảng chi tiết hiển thị GỘP Ô: các cột thông tin hàng hoá gộp dọc theo số khách hàng của hàng '
     'đó. Nhóm tiêu đề "Số lượng" gộp các cột con: Có thể huỷ (chỉ ở màn lập), Duyệt huỷ, ĐVT.\n'
     'Hàng giữ của một nhân viên cho một khách hàng có thể nằm trên nhiều lô khác hạn giữ.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     '- Số trừ tồn = Duyệt huỷ × hệ số quy đổi của ĐVT đã chọn (quy về đơn vị cơ bản, làm tròn 2 '
     'số lẻ).\n'
     '- Trừ theo từng dòng khách hàng, trên các lô của ĐÚNG nhân viên + khách hàng đó, thứ tự hạn '
     'giữ SỚM TRƯỚC (kể cả lô đã quá hạn), hết lô này mới sang lô sau.\n'
     '- Lô được tra theo CÔNG TY CỦA NHÂN VIÊN CHỦ LÔ, không theo công ty của kế toán lập phiếu.\n'
     '- Một hàng hoá không được chọn trùng khách hàng; một phiếu không được có trùng hàng hoá.\n'
     '- Dòng khách hàng có Duyệt huỷ = 0 không được lưu; hàng hoá không còn dòng khách hàng nào thì '
     'không lưu hàng hoá đó.\n'
     '- Một dòng thiếu tồn thì TOÀN BỘ phiếu bị huỷ bỏ: không tạo phiếu, không trừ một phần.'),
    ('7. Phân quyền cấp',
     'Màn hình chỉ dùng MỘT quyền: "Quản lý giữ hàng" — mở màn, xem danh sách, xem chi tiết, in, '
     'xuất Excel và lập phiếu.\n'
     'Ba quyền "Xem phiếu hàng giữ theo tổng công ty", "Xem phiếu hàng giữ theo công ty", "Xem phiếu '
     'hàng giữ theo phòng ban" KHÔNG có tác dụng ở màn này (khác màn Phiếu hủy hàng giữ thường).\n'
     'Tài khoản quản trị cao nhất: làm được mọi việc và xem được mọi công ty.\n'
     'Không có quyền riêng cho Thêm / Sửa / Xoá.'),
    ('8. Cách tính các ô thống kê',
     'Ô "Hiển thị a–b / N": a là số thứ tự dòng đầu trang, b là dòng cuối trang, N là tổng số phiếu '
     'khớp bộ lọc trong phạm vi xem.\n'
     'Cột "Đang giữ" (cửa sổ chọn hàng) và ô "Có thể huỷ" (form lập) = tổng số đang giữ của nhân '
     'viên TRỪ phần đang nằm trong các đề nghị xuất kho chưa hoàn tất. "Đang giữ" tính theo đơn vị '
     'cơ bản, cộng mọi khách hàng; "Có thể huỷ" tính cho từng khách hàng.\n'
     '"Có thể huỷ" = số có thể huỷ theo đơn vị cơ bản ÷ hệ số ĐVT đang chọn, làm tròn XUỐNG 2 số lẻ '
     '(vd 5 cái, hộp 12 cái: 0.41 hộp).\n'
     'Ghi chú mốc lịch sử "Đã trừ tồn hàng giữ trên N lô." — N là tổng số lô bị trừ của cả phiếu.\n'
     'Bản in danh sách có dòng "Tổng số phiếu" = số phiếu khớp bộ lọc.'),
    ('9. Ghi chú đọc bảng',
     'BẪY DỄ GHI FAILED OAN:\n'
     '- KHÔNG có nút Sửa / Xoá / Huỷ duyệt ở danh sách và chi tiết là ĐÚNG thiết kế.\n'
     '- Phạm vi xem giữ như hệ thống cũ: chỉ cần quyền "Quản lý giữ hàng", danh sách lọc theo công '
     'ty người đăng nhập. KHÔNG áp 3 cấp quyền xem (tổng công ty / công ty / phòng ban).\n'
     '- Phiếu thuộc công ty NGƯỜI LẬP. Kế toán công ty 1 huỷ hàng của nhân viên công ty 4 thì phiếu '
     'nằm ở danh sách công ty 1; kế toán công ty 4 KHÔNG thấy phiếu đó — đúng thiết kế.\n'
     '- Lô hàng giữ tra theo công ty của NHÂN VIÊN CHỦ LÔ, nên kế toán khác công ty vẫn huỷ đúng lô.\n'
     '- Ô "Huỷ của nhân viên" liệt kê mọi nhân viên đang làm việc kể cả người không giữ hàng — đúng '
     'như hệ thống cũ; chọn người không giữ gì thì cửa sổ chọn hàng báo "Nhân viên này hiện không '
     'giữ hàng hoá nào.".\n'
     '- Nút "Duyệt" chính là LƯU: phiếu không có trạng thái nháp, bấm là trừ hàng giữ ngay.\n'
     '- Nút "Duyệt" và "Thêm hàng hoá" ẨN (không phải mờ) khi chưa đủ điều kiện.\n'
     '- Vượt "Có thể huỷ" thì báo đỏ dưới ô và GIỮ NGUYÊN số vừa gõ; tự kéo về trần mới là lỗi.\n'
     '- Ô Duyệt huỷ dùng DẤU CHẤM cho phần thập phân, tối đa 2 số lẻ; dấu phẩy, chữ, dấu trừ bị bỏ '
     'ngay khi gõ (gõ "1,5" sẽ thành 15).\n'
     '- Số hiển thị theo chuẩn quốc tế 1,234,567.89.\n'
     '- Ô không có dữ liệu để TRỐNG, không in dấu gạch. Riêng BẢN IN giấy, ô thông tin trống in '
     'dấu chấm "....." để viết tay — đúng mẫu in.\n'
     '- Phiếu cũ chuyển từ hệ thống cũ không có lịch sử, khối lịch sử báo "Chưa có lịch sử thao tác '
     'nào." là đúng.\n'
     '- Ô tìm nhanh CHỈ tìm theo mã phiếu.\n'
     '- Mọi thao tác Duyệt đều trừ hàng giữ THẬT, không hoàn tác — chỉ test trên dữ liệu chấp nhận '
     'mất, ghi lại số giữ trước khi test.\n'
     '- Các TC "dùng công cụ kiểm thử API" dành cho tester kỹ thuật.'),
]

ROLE_TCS = [
    ('00', 'Không có quyền "Quản lý giữ hàng" thì không xem được màn', 'P0',
     'Tài khoản A không có quyền "Quản lý giữ hàng", không phải tài khoản quản trị cao nhất.\n'
     'Công ty của A có 580 phiếu huỷ hàng giữ kế toán.',
     '1. Đăng nhập bằng A.\n'
     '2. Vào ' + MENU + '.',
     '—',
     '- Màn hình hiện biểu tượng khoá và câu "Bạn chưa có quyền Quản lý giữ hàng nên không xem được '
     'màn này.".\n'
     '- Có thông báo lỗi "Bạn chưa có quyền Quản lý giữ hàng.".\n'
     '- KHÔNG hiện bảng, bộ lọc, nút Tạo mới / In / Xuất Excel.'),
    ('01', 'Quyền "Quản lý giữ hàng" dùng được toàn bộ chức năng', 'P0',
     'Tài khoản B thuộc công ty 1, có quyền "Quản lý giữ hàng".\n'
     'Công ty 1 có 580 phiếu, công ty 4 có 24 phiếu.',
     '1. Đăng nhập bằng B.\n'
     '2. Vào ' + MENU + '.\n'
     '3. Đọc ô "Hiển thị a–b / N".\n'
     '4. Bấm Tạo mới.',
     '—',
     '- Danh sách hiện, N = 580 (chỉ phiếu công ty 1).\n'
     '- Có đủ nút Tạo mới, In, Xuất Excel, Cấu hình cột hiển thị.\n'
     '- KHÔNG có ô lọc "Công ty".\n'
     '- Bấm Tạo mới mở màn "Lập phiếu huỷ hàng giữ kế toán".'),
    ('02', 'Ba quyền xem theo cấp KHÔNG thay được quyền "Quản lý giữ hàng"', 'P0',
     'Tài khoản C có đủ 3 quyền "Xem phiếu hàng giữ theo tổng công ty", "Xem phiếu hàng giữ theo '
     'công ty", "Xem phiếu hàng giữ theo phòng ban" nhưng KHÔNG có "Quản lý giữ hàng".',
     '1. Đăng nhập bằng C.\n'
     '2. Vào ' + MENU + '.',
     '—',
     '- Màn hình báo "Bạn chưa có quyền Quản lý giữ hàng nên không xem được màn này.".\n'
     '- Lưu ý: đây là ĐÚNG thiết kế (giữ như hệ thống cũ), khác màn Phiếu hủy hàng giữ thường.'),
    ('03', 'Tài khoản quản trị cao nhất xem được mọi công ty', 'P1',
     'Tài khoản quản trị cao nhất S thuộc công ty 1.\n'
     'Công ty 1 có 580 phiếu, công ty 4 có 24 phiếu.',
     '1. Đăng nhập bằng S.\n'
     '2. Vào màn danh sách, đọc N.\n'
     '3. Mở Tìm kiếm nâng cao.',
     '—',
     '- N = 604 (cả hai công ty).\n'
     '- Tìm kiếm nâng cao có thêm ô "Công ty" đứng đầu.\n'
     '- Mở được chi tiết phiếu của công ty 4.'),
    ('04', 'Không có quyền nhưng vào thẳng đường dẫn màn lập phiếu', 'P1',
     'Tài khoản A không có quyền "Quản lý giữ hàng".\n'
     'Nhân viên N đang giữ 3 hàng hoá.',
     '1. Đăng nhập bằng A.\n'
     '2. Gõ thẳng đường dẫn màn lập phiếu huỷ hàng giữ kế toán lên thanh địa chỉ.\n'
     '3. Chọn N ở ô "Huỷ của nhân viên".\n'
     '4. Bấm "Thêm hàng hoá".',
     'Huỷ của nhân viên: N',
     '- Form mở được nhưng cửa sổ chọn hàng không có dòng nào.\n'
     '- Có thông báo lỗi "Bạn chưa có quyền Quản lý giữ hàng.".\n'
     '- Không thêm được hàng hoá nên nút Duyệt không bao giờ hiện.'),
    ('05', 'Gọi thẳng chức năng Lập phiếu khi không có quyền', 'P0',
     'Tài khoản A không có quyền "Quản lý giữ hàng".\n'
     'Nhân viên N đang giữ 10 cái hàng H cho khách K.',
     '1. Dùng công cụ kiểm thử API, đăng nhập bằng A.\n'
     '2. Gọi thẳng chức năng Lập phiếu huỷ hàng giữ kế toán cho N, hàng H, khách K, số lượng 2.',
     'Duyệt huỷ: 2',
     '- Phần mềm từ chối, báo "Bạn chưa có quyền Quản lý giữ hàng.".\n'
     '- Không có phiếu nào được tạo.\n'
     '- Hàng giữ của N vẫn là 10.\n'
     '- Lưu ý: gửi dữ liệu sai (nhân viên không tồn tại) cũng chỉ nhận câu báo không có quyền, '
     'không lộ lỗi dữ liệu.'),
    ('06', 'Gọi thẳng chức năng Xem chi tiết / In / Xuất khi không có quyền', 'P1',
     'Tài khoản A không có quyền "Quản lý giữ hàng". Phiếu KTPHHG-00604 thuộc công ty của A.',
     '1. Dùng công cụ kiểm thử API, đăng nhập bằng A.\n'
     '2. Gọi lần lượt: xem chi tiết KTPHHG-00604, lấy bản in phiếu, lấy bản in danh sách, lấy dữ '
     'liệu xuất Excel, xem lịch sử phiếu.',
     '—',
     '- Cả 5 chức năng đều bị từ chối, báo không có quyền.\n'
     '- Không trả về dữ liệu phiếu nào.'),
]

S1 = [
    ('001', 'Vào màn qua menu', 'P0',
     'Tài khoản B có quyền "Quản lý giữ hàng", công ty 1 có 580 phiếu.',
     '1. Đăng nhập bằng B.\n'
     '2. Vào ' + MENU + '.',
     '—',
     '- Tiêu đề màn là "Phiếu huỷ hàng giữ kế toán".\n'
     '- Bảng hiện 10 dòng đầu, ô thống kê ghi "Hiển thị 1–10 / 580".\n'
     '- Phiếu mới lập nhất đứng đầu.'),
    ('002', 'Mục menu nằm đúng nhóm Giữ hàng', 'P2',
     'Tài khoản B có quyền "Quản lý giữ hàng".',
     '1. Mở phân hệ Tài chính.\n'
     '2. Mở nhóm Giữ hàng, đọc thứ tự các mục.',
     '—',
     '- Có mục "Phiếu huỷ hàng giữ kế toán" nằm ngay sau "Phiếu hủy hàng giữ" và trước "Phiếu Yêu '
     'cầu điều chuyển hàng giữ".\n'
     '- Bấm vào mở đúng màn danh sách.'),
    ('003', 'Bộ cột mặc định của bảng', 'P0',
     'Tài khoản chưa từng tuỳ chỉnh cột ở màn này.',
     '1. Mở màn danh sách.\n'
     '2. Đọc tiêu đề cột từ trái sang phải.',
     '—',
     '- Đúng thứ tự: STT, Mã phiếu, Huỷ của nhân viên, Ngày tạo, Người tạo, Người cập nhật, Ngày '
     'cập nhật, Hành động.\n'
     '- Cột Ghi chú KHÔNG hiện (mặc định tắt).\n'
     '- KHÔNG có cột Trạng thái (phiếu không có trạng thái).'),
    ('004', 'Cột Hành động chỉ có In và Lịch sử', 'P0',
     'Danh sách có ít nhất 1 phiếu do chính người đăng nhập vừa lập.',
     '1. Mở màn danh sách.\n'
     '2. Xem cột Hành động của dòng đầu tiên và vài dòng khác.',
     '—',
     '- Mỗi dòng đúng 2 nút: In (biểu tượng máy in) và Lịch sử (biểu tượng đồng hồ).\n'
     '- KHÔNG có nút Sửa, KHÔNG có nút Xoá ở bất kỳ dòng nào — đúng thiết kế.'),
    ('005', 'Mã phiếu là liên kết mở màn chi tiết', 'P0',
     'Phiếu KTPHHG-00604 thuộc công ty người đăng nhập.',
     '1. Bấm vào mã KTPHHG-00604.',
     '—',
     '- Mở màn chi tiết, tiêu đề "Chi tiết phiếu huỷ hàng giữ kế toán: KTPHHG-00604".'),
    ('006', 'Phân biệt cột Huỷ của nhân viên và Người tạo', 'P0',
     'Phiếu Z do kế toán B lập để huỷ hàng giữ của nhân viên kinh doanh N.',
     '1. Tìm phiếu Z trong danh sách.\n'
     '2. Đọc cột Huỷ của nhân viên và cột Người tạo.',
     '—',
     '- Cột Huỷ của nhân viên ghi tên N (người bị huỷ hàng).\n'
     '- Cột Người tạo ghi tên B (kế toán lập phiếu).\n'
     '- Ngày tạo hiện dạng dd/mm/yyyy hh:mm.'),
    ('007', 'Danh sách rỗng khi không khớp bộ lọc', 'P1',
     'Không có phiếu nào có mã chứa "ZZZZ".',
     '1. Gõ "ZZZZ" vào ô tìm nhanh.\n'
     '2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: ZZZZ',
     '- Bảng hiện dòng "Không có dữ liệu phù hợp.".\n'
     '- Ô thống kê ghi N = 0, không có thông báo lỗi.'),
]

S2 = [
    ('001', 'Tìm nhanh theo mã phiếu', 'P0',
     'Tồn tại phiếu KTPHHG-00604.',
     '1. Gõ "00604" vào ô tìm nhanh (gợi ý "Tìm theo mã phiếu...").\n'
     '2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: 00604',
     '- Danh sách còn đúng phiếu KTPHHG-00604.'),
    ('002', 'Ô tìm nhanh KHÔNG tìm theo tên nhân viên', 'P1',
     'Có 5 phiếu huỷ hàng của nhân viên "Nguyễn Văn An".',
     '1. Gõ "Nguyễn Văn An" vào ô tìm nhanh.\n'
     '2. Bấm Tìm kiếm.',
     'Ô tìm nhanh: Nguyễn Văn An',
     '- Danh sách RỖNG.\n'
     '- Lưu ý: đúng thiết kế, ô tìm nhanh chỉ tìm theo mã phiếu; lọc theo người dùng ô "Huỷ của '
     'nhân viên".'),
    ('003', 'Ô tìm nhanh chỉ áp dụng khi bấm Tìm kiếm', 'P1',
     'Danh sách đang có 580 phiếu.',
     '1. Gõ "0060" vào ô tìm nhanh, KHÔNG bấm Tìm kiếm.\n'
     '2. Chờ 3 giây.',
     'Ô tìm nhanh: 0060',
     '- Danh sách KHÔNG tự nạp lại, vẫn 580 phiếu.\n'
     '- Bấm Tìm kiếm (hoặc Enter) mới lọc.'),
    ('004', 'Tìm kiếm nâng cao có đủ ô lọc', 'P1',
     'Tài khoản B (không phải quản trị cao nhất).',
     '1. Bấm mở Tìm kiếm nâng cao.\n'
     '2. Đọc nhãn các ô lọc.',
     '—',
     '- Có 4 ô: Huỷ của nhân viên, Người tạo, Tên/mã hàng hóa (gợi ý "Nhập tên hoặc mã hàng hóa"), '
     'Ngày tạo.\n'
     '- KHÔNG có ô Trạng thái và ô Công ty.'),
    ('005', 'Lọc theo Huỷ của nhân viên', 'P0',
     'Nhân viên N bị huỷ hàng ở 4 phiếu.',
     '1. Chọn N ở ô "Huỷ của nhân viên".\n'
     '2. Không bấm Tìm kiếm, chờ 3 giây.',
     'Huỷ của nhân viên: N',
     '- Danh sách tự nạp lại, còn đúng 4 phiếu, cột Huỷ của nhân viên đều là N.'),
    ('006', 'Lọc theo Người tạo', 'P0',
     'Kế toán B đã lập 12 phiếu.',
     '1. Chọn B ở ô "Người tạo".\n'
     '2. Chờ 3 giây.',
     'Người tạo: B',
     '- Còn đúng 12 phiếu, cột Người tạo đều là B.'),
    ('007', 'Lọc theo Tên/mã hàng hóa bằng TÊN', 'P1',
     'Có 3 phiếu chứa hàng "Dầu thủy lực Eneos Super Hyrando 46".',
     '1. Gõ "Eneos" vào ô Tên/mã hàng hóa.\n'
     '2. Chờ 3 giây.',
     'Tên/mã hàng hóa: Eneos',
     '- Chỉ còn phiếu có ít nhất một hàng hoá chứa chữ Eneos trong tên.'),
    ('008', 'Lọc theo Tên/mã hàng hóa bằng MÃ', 'P1',
     'Có phiếu chứa hàng mã ENEO-700-V5023.',
     '1. Gõ "ENEO-700" vào ô Tên/mã hàng hóa.\n'
     '2. Chờ 3 giây.',
     'Tên/mã hàng hóa: ENEO-700',
     '- Vẫn ra kết quả dù gõ MÃ hàng — một ô tìm cả tên và mã.'),
    ('009', 'Lọc khoảng Ngày tạo lấy trọn hai đầu', 'P0',
     'Có 3 phiếu lập ngày 28/09/2026 (1 phiếu lúc 23:50) và 2 phiếu lập ngày 29/09/2026.',
     '1. Chọn Ngày tạo từ 28/09/2026 đến 29/09/2026.\n'
     '2. Chờ 3 giây.',
     'Ngày tạo: 28/09/2026 - 29/09/2026',
     '- Danh sách có đúng 5 phiếu.\n'
     '- Phiếu lập 23:50 ngày 28/09/2026 và các phiếu ngày 29/09/2026 đều có mặt.'),
    ('010', 'Kết hợp nhiều ô lọc', 'P1',
     'Nhân viên N có 4 phiếu, trong đó 1 phiếu do B lập ngày 29/09/2026.',
     '1. Chọn Huỷ của nhân viên = N.\n'
     '2. Chọn Người tạo = B.\n'
     '3. Chọn Ngày tạo 29/09/2026 - 29/09/2026.',
     'Huỷ của nhân viên: N\nNgười tạo: B\nNgày tạo: 29/09/2026',
     '- Còn đúng 1 phiếu thoả cả ba điều kiện.'),
    ('011', 'Ô lọc Công ty của tài khoản quản trị cao nhất', 'P1',
     'Tài khoản quản trị cao nhất S. Công ty 4 có 24 phiếu.',
     '1. Đăng nhập bằng S.\n'
     '2. Mở Tìm kiếm nâng cao, chọn Công ty = công ty 4.',
     'Công ty: công ty 4',
     '- Còn đúng 24 phiếu.\n'
     '- Ô "Huỷ của nhân viên" đang chọn (nếu có) KHÔNG bị xoá khi đổi công ty.'),
    ('012', 'Nút Làm mới xoá hết điều kiện lọc và sắp xếp', 'P0',
     'Đang lọc Người tạo = B, Ngày tạo một khoảng, ô tìm nhanh "006", đang sắp xếp Mã phiếu tăng '
     'dần, đang ở trang 3.',
     '1. Bấm Làm mới.',
     '—',
     '- Mọi ô lọc trở về trống, kể cả ô tìm nhanh.\n'
     '- Sắp xếp trở về mặc định (mới nhất trước), quay về trang 1.\n'
     '- Danh sách tự nạp lại đầy đủ, không cần bấm Tìm kiếm.'),
    ('013', 'Bộ lọc được nhớ khi quay lại màn trong 10 phút', 'P1',
     'Vừa lọc Người tạo = B và đang mở Tìm kiếm nâng cao.',
     '1. Mở một phiếu chi tiết.\n'
     '2. Bấm Quay lại.',
     '—',
     '- Ô Người tạo vẫn là B, danh sách vẫn đang lọc.\n'
     '- Khu vực Tìm kiếm nâng cao vẫn đang mở.'),
    ('014', 'Cài đặt bộ lọc — tắt bớt ô lọc', 'P2',
     'Tìm kiếm nâng cao đang hiện 4 ô.',
     '1. Bấm Cài đặt bộ lọc.\n'
     '2. Bỏ tích ô "Tên/mã hàng hóa".\n'
     '3. Bấm Lưu.\n'
     '4. Thoát màn rồi vào lại.',
     '—',
     '- Khu vực lọc còn 3 ô, không còn Tên/mã hàng hóa.\n'
     '- Vào lại màn vẫn giữ cấu hình này.'),
]

S3 = [
    ('001', 'Sắp xếp theo Mã phiếu', 'P0',
     'Danh sách có ít nhất 30 phiếu.',
     '1. Bấm tiêu đề cột Mã phiếu.\n'
     '2. Bấm lần nữa.',
     '—',
     '- Lần 1: mã phiếu tăng dần; lần 2: giảm dần.\n'
     '- Mỗi lần đều quay về trang 1 và giữ nguyên bộ lọc.'),
    ('002', 'Sắp xếp theo Ngày tạo và Ngày cập nhật', 'P1',
     'Danh sách có phiếu nhiều ngày khác nhau.',
     '1. Bấm tiêu đề cột Ngày tạo hai lần.\n'
     '2. Bấm tiêu đề cột Ngày cập nhật hai lần.',
     '—',
     '- Thứ tự đảo chiều đúng ở cả hai cột.\n'
     '- Với phiếu lập trên hệ thống mới, Ngày cập nhật trùng Ngày tạo vì phiếu không sửa được.'),
    ('003', 'Các cột KHÔNG sắp xếp được', 'P2',
     'Danh sách có ít nhất 10 phiếu.',
     '1. Bấm lần lượt tiêu đề cột Huỷ của nhân viên, Người tạo, Người cập nhật.',
     '—',
     '- Ba cột này không có mũi tên sắp xếp, bấm vào không đổi thứ tự.\n'
     '- Chỉ Mã phiếu, Ngày tạo, Ngày cập nhật sắp xếp được.'),
    ('004', 'Đổi số dòng mỗi trang', 'P0',
     'Danh sách có 580 phiếu, đang 10 dòng/trang.',
     '1. Đổi số dòng/trang sang 50.',
     'Số dòng/trang: 50',
     '- Bảng hiện 50 dòng, ô thống kê ghi "Hiển thị 1–50 / 580".\n'
     '- Quay về trang 1.'),
    ('005', 'Chuyển trang giữ nguyên bộ lọc, STT liên tục', 'P0',
     'Đang lọc Người tạo = B, kết quả 25 phiếu, 10 dòng/trang.',
     '1. Sang trang 2.\n'
     '2. Đọc STT dòng đầu, cột Người tạo và ô lọc.',
     '—',
     '- Dòng đầu trang 2 có STT = 11.\n'
     '- Ô lọc vẫn là B, mọi dòng đều do B lập.\n'
     '- Ô thống kê ghi "Hiển thị 11–20 / 25".'),
    ('006', 'Cấu hình cột — bật cột Ghi chú', 'P1',
     'Cột Ghi chú đang tắt. Có phiếu có ghi chú và phiếu không có ghi chú.',
     '1. Bấm nút Cấu hình cột hiển thị.\n'
     '2. Tích Ghi chú, bấm Lưu.',
     '—',
     '- Bảng hiện thêm cột Ghi chú với đúng nội dung.\n'
     '- Phiếu không có ghi chú thì ô để TRỐNG, không có dấu gạch.'),
    ('007', 'Cấu hình cột — không tắt được cột khoá', 'P2',
     'Đang mở cửa sổ Cấu hình cột hiển thị.',
     '1. Thử bỏ tích STT, Mã phiếu, Hành động.',
     '—',
     '- Ba cột này không bỏ tích được, luôn hiện.'),
    ('008', 'Ô không có dữ liệu để trống', 'P2',
     'Có phiếu cũ từ hệ thống cũ không ghi người cập nhật.',
     '1. Tìm phiếu đó trong danh sách.\n'
     '2. Đọc cột Người cập nhật.',
     '—',
     '- Ô để TRỐNG, không in dấu gạch hay chữ "null".'),
]

S4 = [
    ('001', 'Màn lập phiếu khi vừa mở', 'P0',
     'Tài khoản B có quyền "Quản lý giữ hàng", tên "Trần Thị Bình".',
     '1. Ở danh sách bấm Tạo mới.\n'
     '2. Quan sát form.',
     '—',
     '- Tiêu đề màn "Lập phiếu huỷ hàng giữ kế toán".\n'
     '- Khối Thông tin chung có ô "Huỷ của nhân viên" (bắt buộc, gợi ý "Chọn nhân viên") và ô "Ghi '
     'chú" (gợi ý "Nhập ghi chú"); KHÔNG có ô Mã phiếu, Phòng ban.\n'
     '- Góc phải ghi "Người tạo: Trần Thị Bình · <ngày hôm nay dd/mm/yyyy>".\n'
     '- Khối Chi tiết hiện câu "Chọn nhân viên trước để thêm hàng hoá".\n'
     '- Nút "Thêm hàng hoá" và nút "Duyệt" đều ẨN; chỉ có nút Quay lại.'),
    ('002', 'Ô Huỷ của nhân viên liệt kê mọi nhân viên đang làm việc', 'P1',
     'Nhân viên M thuộc công ty 4, đang làm việc, không giữ hàng nào. Nhân viên X đã nghỉ việc.',
     '1. Mở ô "Huỷ của nhân viên".\n'
     '2. Gõ tìm M, rồi gõ tìm X.',
     '—',
     '- Tìm thấy M dù khác công ty và không giữ hàng — đúng như hệ thống cũ.\n'
     '- KHÔNG tìm thấy X (đã nghỉ việc).'),
    ('003', 'Chọn nhân viên thì hiện nút Thêm hàng hoá', 'P0',
     'Nhân viên N đang giữ hàng.',
     '1. Chọn N ở ô "Huỷ của nhân viên".',
     'Huỷ của nhân viên: N',
     '- Nút "Thêm hàng hoá" hiện ở đầu khối Chi tiết.\n'
     '- Bảng hiện tiêu đề cột và dòng "Chưa có hàng hoá nào".\n'
     '- Nút Duyệt vẫn ẩn vì chưa có hàng hoá.'),
    ('004', 'Nội dung cửa sổ chọn hàng', 'P0',
     'Nhân viên N đang giữ 12 mã hàng khác nhau (cho nhiều khách hàng).',
     '1. Chọn N, bấm "Thêm hàng hoá".\n'
     '2. Đọc tiêu đề, ô lọc và các cột.',
     '—',
     '- Tiêu đề "Hàng đang giữ của nhân viên", dòng phụ "Chỉ liệt kê hàng nhân viên đã chọn còn '
     'đang giữ (mọi khách hàng)".\n'
     '- Hai ô lọc Tên hàng hóa, Mã hàng hóa và hai nút Tìm kiếm, Làm mới.\n'
     '- Các cột: ô tích, STT, Mã hàng hóa, Tên hàng hóa, Model, Thương hiệu, ĐVT, Đang giữ.\n'
     '- Mặc định 10 dòng/trang, đổi được 10 / 20 / 50 / 100; ô thống kê ghi tổng 12.\n'
     '- Nút "Chọn (0)" và nút "Đóng".'),
    ('005', 'Nhân viên không giữ hàng nào', 'P0',
     'Nhân viên M đang làm việc nhưng không giữ hàng hoá nào.',
     '1. Chọn M ở ô "Huỷ của nhân viên".\n'
     '2. Bấm "Thêm hàng hoá".',
     'Huỷ của nhân viên: M',
     '- Cửa sổ mở, bảng không có dòng nào và ghi đúng câu "Nhân viên này hiện không giữ hàng hoá '
     'nào.".\n'
     '- Không có thông báo lỗi.'),
    ('006', 'Cột Đang giữ trừ phần đang chờ xuất kho', 'P0',
     'Nhân viên N giữ 10 cái hàng H (tổng mọi khách).\n'
     'Có 1 đề nghị xuất kho chưa hoàn tất lấy 4 cái từ hàng giữ đó.',
     '1. Chọn N, bấm "Thêm hàng hoá".\n'
     '2. Đọc cột Đang giữ của hàng H.',
     '—',
     '- Cột Đang giữ ghi 6, KHÔNG phải 10.\n'
     '- Số tính theo đơn vị cơ bản (cột ĐVT là đơn vị cơ bản).'),
    ('007', 'Lọc trong cửa sổ theo Tên và Mã hàng hóa', 'P1',
     'Nhân viên N giữ 12 mã hàng, trong đó 2 mã có tên chứa "Eneos", 1 mã có mã chứa "ENEO-700".',
     '1. Gõ "Eneos" ở ô Tên hàng hóa, nhấn Enter.\n'
     '2. Bấm Làm mới.\n'
     '3. Gõ "ENEO-700" ở ô Mã hàng hóa, bấm Tìm kiếm.',
     'Tên hàng hóa: Eneos\nMã hàng hóa: ENEO-700',
     '- Bước 1: còn 2 dòng.\n'
     '- Bước 2: hai ô lọc trống, trở lại 12 dòng.\n'
     '- Bước 3: còn 1 dòng.'),
    ('008', 'Chọn nhiều hàng hoá một lần', 'P0',
     'Nhân viên N giữ hàng H1, H2, H3.',
     '1. Mở cửa sổ chọn hàng.\n'
     '2. Tích H1 và H3.\n'
     '3. Bấm "Chọn (2)".',
     '—',
     '- Nút đổi số theo số dòng đã tích: "Chọn (2)".\n'
     '- Cửa sổ đóng, bảng Chi tiết có 2 hàng hoá H1, H3 với Tên, Model, Mã hàng hóa, Thương hiệu '
     'đúng.\n'
     '- Mỗi hàng hoá có sẵn 1 dòng khách hàng: ô Khách hàng đã chọn khách đầu tiên (theo tên), ô '
     'Duyệt huỷ trống (gợi ý "Nhập số lượng"), ô ĐVT là đơn vị cơ bản.\n'
     '- Nút Duyệt hiện ra.'),
    ('009', 'Hàng đã thêm bị ẩn khỏi cửa sổ lần sau', 'P0',
     'Bảng Chi tiết đã có H1, H3. Nhân viên N giữ tổng 3 mã hàng.',
     '1. Bấm "Thêm hàng hoá" lần nữa.',
     '—',
     '- Cửa sổ chỉ còn H2, ô thống kê ghi tổng 1.\n'
     '- H1, H3 không hiện (ẩn hẳn, không phải hiện rồi khoá).'),
    ('010', 'Hàng còn giữ nhưng không còn số có thể huỷ', 'P1',
     'Nhân viên N giữ 4 cái hàng H, cả 4 đang nằm trong một đề nghị xuất kho chưa hoàn tất.',
     '1. Mở cửa sổ chọn hàng, tìm hàng H.\n'
     '2. Tích H, bấm Chọn.',
     '—',
     '- Trong cửa sổ, H vẫn hiện với cột Đang giữ = 0.\n'
     '- Sau khi bấm Chọn: có thông báo cảnh báo ""<tên hàng H>" không còn số lượng có thể huỷ.".\n'
     '- H KHÔNG được thêm vào bảng Chi tiết.'),
    ('011', 'Ô trống trong cửa sổ chọn hàng', 'P2',
     'Nhân viên N giữ một hàng hoá không khai Model và Thương hiệu.',
     '1. Mở cửa sổ chọn hàng, tìm hàng đó.\n'
     '2. Đọc cột Model và Thương hiệu.',
     '—',
     '- Hai ô để TRỐNG, không in dấu gạch (quy tắc chung ô rỗng để trống).'),
    ('012', 'Xoá một hàng hoá khỏi phiếu', 'P1',
     'Bảng Chi tiết có H1 (2 khách hàng) và H3.',
     '1. Bấm biểu tượng thùng rác "Xoá hàng hoá" ở hàng H1.',
     '—',
     '- H1 cùng cả 2 dòng khách hàng biến mất ngay, không hỏi xác nhận.\n'
     '- H3 được đánh lại STT = 1.\n'
     '- Mở lại cửa sổ chọn hàng thì H1 xuất hiện trở lại.'),
    ('013', 'Đổi nhân viên khi đã có hàng hoá', 'P0',
     'Đã chọn nhân viên N và thêm 2 hàng hoá, đã gõ số lượng.',
     '1. Chọn nhân viên P ở ô "Huỷ của nhân viên".\n'
     '2. Đọc hộp thoại, bấm Hủy.\n'
     '3. Chọn lại P, lần này bấm "Đổi nhân viên".',
     'Huỷ của nhân viên: N, đổi sang P',
     '- Hộp thoại tiêu đề "Đổi nhân viên", nội dung "Đổi nhân viên sẽ xoá toàn bộ hàng hoá đã chọn. '
     'Tiếp tục?".\n'
     '- Bấm Hủy: ô vẫn hiện N, 2 hàng hoá và số đã gõ còn nguyên.\n'
     '- Bấm "Đổi nhân viên": ô hiện P, bảng Chi tiết trống, nút Duyệt ẩn.'),
    ('014', 'Xoá nhanh nhân viên bằng nút x', 'P1',
     'Đã chọn nhân viên N và thêm 1 hàng hoá.',
     '1. Bấm nút x trong ô "Huỷ của nhân viên".\n'
     '2. Bấm "Đổi nhân viên" trên hộp thoại.',
     '—',
     '- Hộp thoại xác nhận hiện ra và bấm được nút (danh sách nhân viên KHÔNG tự bung đè lên).\n'
     '- Sau khi xác nhận: ô trống, khối Chi tiết về câu "Chọn nhân viên trước để thêm hàng hoá", '
     'nút Thêm hàng hoá và Duyệt ẩn.'),
    ('015', 'Cảnh báo khi rời màn lúc chưa lưu', 'P1',
     'Đã chọn nhân viên và thêm hàng hoá nhưng chưa bấm Duyệt.',
     '1. Bấm Quay lại (hoặc bấm sang mục menu khác).',
     '—',
     '- Phần mềm cảnh báo dữ liệu chưa được lưu và hỏi có rời đi không.\n'
     '- Chọn ở lại thì dữ liệu còn nguyên.\n'
     '- Form mới mở chưa nhập gì thì bấm Quay lại về thẳng danh sách, không hỏi.'),
]

S5 = [
    ('001', 'Ô Khách hàng chỉ liệt kê khách còn số có thể huỷ', 'P0',
     'Nhân viên N giữ hàng H cho 3 khách: K1 còn 5, K2 còn 3, K3 còn 2 nhưng cả 2 đang chờ xuất kho.',
     '1. Thêm hàng H vào phiếu.\n'
     '2. Mở ô Khách hàng của dòng đầu.',
     '—',
     '- Chỉ có K1 và K2, mỗi khách đúng 1 lần, hiển thị dạng "mã khách - tên khách".\n'
     '- KHÔNG có K3.\n'
     '- Khách của hàng hoá khác mà N giữ cũng không hiện.'),
    ('002', 'Có thể huỷ đổi theo khách hàng đang chọn', 'P0',
     'Hàng H: K1 còn 5 cái, K2 còn 3 cái (đơn vị cơ bản Cái).',
     '1. Ở dòng khách đầu tiên chọn K1, đọc ô Có thể huỷ.\n'
     '2. Đổi sang K2, đọc lại.',
     'Khách hàng: K1, rồi K2',
     '- Chọn K1: Có thể huỷ = 5.\n'
     '- Chọn K2: Có thể huỷ = 3.\n'
     '- Tiêu đề nhóm cột "Số lượng" gộp 3 cột con Có thể huỷ, Duyệt huỷ, ĐVT.'),
    ('003', 'Thêm khách hàng thứ hai cho cùng hàng hoá', 'P0',
     'Hàng H đang có 1 dòng khách K1. Nhân viên N giữ H cho K1, K2.',
     '1. Bấm liên kết "Thêm khách hàng" dưới ô Khách hàng.',
     '—',
     '- Hàng H có thêm 1 dòng, ô Khách hàng tự chọn K2, ĐVT là đơn vị cơ bản, Duyệt huỷ trống.\n'
     '- Các ô STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu và nút thùng rác GỘP chung cho 2 '
     'dòng.\n'
     '- Mỗi dòng có nút x "Bỏ khách hàng này".'),
    ('004', 'Không chọn trùng khách hàng trong một hàng hoá', 'P0',
     'Hàng H có 2 dòng: dòng 1 là K1, dòng 2 là K2. N giữ H cho K1, K2, K3.',
     '1. Mở ô Khách hàng của dòng 2.',
     '—',
     '- Danh sách chỉ có K2 và K3, KHÔNG có K1 (đã chọn ở dòng 1).\n'
     '- Không có cách chọn trùng khách hàng qua giao diện.'),
    ('005', 'Hết khách để thêm thì ẩn liên kết Thêm khách hàng', 'P1',
     'N giữ hàng H cho đúng 2 khách K1, K2; hàng H đã có đủ 2 dòng K1, K2.',
     '1. Quan sát dưới ô Khách hàng của dòng cuối.',
     '—',
     '- Liên kết "Thêm khách hàng" KHÔNG hiện.\n'
     '- Bỏ 1 khách bằng nút x thì liên kết hiện lại.'),
    ('006', 'Bỏ một khách hàng', 'P1',
     'Hàng H có 3 dòng khách K1, K2, K3; dòng K2 đang có lỗi đỏ.',
     '1. Bấm nút x "Bỏ khách hàng này" ở dòng K2.',
     '—',
     '- Còn 2 dòng K1, K3, ô gộp co lại đúng 2 dòng.\n'
     '- Lỗi đỏ của dòng K2 biến mất.\n'
     '- Khi chỉ còn 1 dòng thì nút x không còn hiện (không bỏ được dòng cuối, muốn bỏ thì xoá cả '
     'hàng hoá).'),
    ('007', 'Hai khách hàng trừ tồn riêng', 'P0',
     'Hàng H: K1 còn 5 cái, K2 còn 3 cái.',
     '1. Dòng K1 gõ 2, dòng K2 gõ 3.\n'
     '2. Bấm Duyệt, xác nhận.\n'
     '3. Mở màn Danh sách hàng giữ, xem hàng H của N theo từng khách.',
     'K1: 2\nK2: 3',
     '- Lập phiếu thành công.\n'
     '- K1 còn 3, K2 còn 0.\n'
     '- Chi tiết phiếu hiện hàng H gộp 2 dòng K1 = 2, K2 = 3.'),
    ('008', 'Gọi thẳng chức năng Lập phiếu với khách hàng trùng', 'P0',
     'Hàng H: K1 còn 5 cái.',
     '1. Dùng công cụ kiểm thử API, đăng nhập kế toán có quyền.\n'
     '2. Gọi Lập phiếu cho hàng H với 2 dòng cùng khách K1, mỗi dòng 3 cái.',
     'K1: 3\nK1: 3',
     '- Phần mềm từ chối, báo "Khách hàng bị chọn trùng trong cùng một hàng hoá.".\n'
     '- Không tạo phiếu, hàng giữ của K1 vẫn là 5 (hệ thống cũ để lọt, tổng 6 vượt 5).'),
]

S6 = [
    ('001', 'Ô ĐVT liệt kê mọi đơn vị của hàng hoá', 'P0',
     'Hàng H có 3 đơn vị: Cái (cơ bản), Hộp = 12 Cái, Thùng = 144 Cái.',
     '1. Thêm hàng H vào phiếu.\n'
     '2. Mở ô ĐVT.',
     '—',
     '- Có đủ Cái, Hộp, Thùng; mặc định đang chọn Cái (đơn vị cơ bản).\n'
     '- Ô ĐVT không để trống được (không có nút xoá).'),
    ('002', 'Có thể huỷ quy đổi theo ĐVT đang chọn', 'P0',
     'Hàng H: K1 còn 30 cái. Hộp = 12 Cái.',
     '1. Ở dòng K1 đọc ô Có thể huỷ khi ĐVT = Cái.\n'
     '2. Đổi ĐVT sang Hộp.',
     'ĐVT: Cái, rồi Hộp',
     '- ĐVT Cái: Có thể huỷ = 30.\n'
     '- ĐVT Hộp: Có thể huỷ = 2.5.'),
    ('003', 'Có thể huỷ làm tròn XUỐNG 2 số lẻ', 'P0',
     'Hàng H: K1 còn 5 cái. Hộp = 12 Cái.',
     '1. Chọn ĐVT Hộp, đọc Có thể huỷ.\n'
     '2. Gõ 0.42 vào Duyệt huỷ.\n'
     '3. Xoá, gõ 0.41.',
     'Duyệt huỷ: 0.42, rồi 0.41',
     '- Có thể huỷ = 0.41 (không phải 0.42).\n'
     '- Gõ 0.42: báo đỏ "Vượt số có thể huỷ (tối đa 0.41)".\n'
     '- Gõ 0.41: hết báo lỗi, lưu được.'),
    ('004', 'Duyệt theo ĐVT lớn trừ tồn đúng số quy đổi', 'P0',
     'Hàng H: K1 còn 30 cái. Hộp = 12 Cái.',
     '1. Dòng K1 chọn ĐVT Hộp, gõ 0.5.\n'
     '2. Bấm Duyệt, xác nhận.\n'
     '3. Xem hàng giữ H của N cho K1 ở màn Danh sách hàng giữ.',
     'ĐVT: Hộp\nDuyệt huỷ: 0.5',
     '- Hàng giữ còn 24 cái (bị trừ 0.5 × 12 = 6 cái).\n'
     '- Chi tiết phiếu ghi Duyệt huỷ 0.5, ĐVT Hộp (giữ số theo ĐVT đã chọn, không đổi ra Cái).'),
    ('005', 'Đổi ĐVT sau khi đã gõ số thì kiểm lại ngay', 'P0',
     'Hàng H: K1 còn 30 cái. Hộp = 12 Cái. Dòng K1 đang ĐVT Cái, Duyệt huỷ = 20 (hợp lệ).',
     '1. Đổi ĐVT sang Hộp.',
     'ĐVT: Hộp',
     '- Ô Duyệt huỷ vẫn giữ số 20.\n'
     '- Báo đỏ ngay "Vượt số có thể huỷ (tối đa 2.5)".\n'
     '- Đổi lại Cái thì lỗi biến mất.'),
    ('006', 'ĐVT có hệ số nhỏ hơn 1', 'P1',
     'Hàng H đơn vị cơ bản Kg, có thêm đơn vị Gram = 0.001 Kg. K1 còn 10 kg.',
     '1. Chọn ĐVT Gram, gõ 1.\n'
     '2. Xoá, gõ 500.',
     'ĐVT: Gram\nDuyệt huỷ: 1, rồi 500',
     '- Gõ 1: báo đỏ "Số lượng quá nhỏ so với đơn vị tính đã chọn." (quy đổi ra 0.001 kg, làm tròn '
     '2 số lẻ thành 0).\n'
     '- Gõ 500: hợp lệ, Có thể huỷ hiện 10,000.'),
    ('007', 'Hai khách cùng hàng dùng hai ĐVT khác nhau', 'P1',
     'Hàng H: K1 còn 30 cái, K2 còn 24 cái. Hộp = 12 Cái.',
     '1. Dòng K1: ĐVT Cái, gõ 6.\n'
     '2. Dòng K2: ĐVT Hộp, gõ 1.\n'
     '3. Duyệt, xác nhận.',
     'K1: 6 Cái\nK2: 1 Hộp',
     '- Lập phiếu thành công.\n'
     '- K1 còn 24 cái, K2 còn 12 cái.'),
]

S7 = [
    ('001', 'Hộp thoại xác nhận trước khi duyệt', 'P0',
     'Đã chọn nhân viên, thêm hàng, nhập số hợp lệ.',
     '1. Bấm Duyệt.\n'
     '2. Đọc hộp thoại.',
     '—',
     '- Tiêu đề "Xác nhận duyệt".\n'
     '- Nội dung "Duyệt phiếu sẽ TRỪ TỒN HÀNG GIỮ ngay lập tức và không thể hoàn tác. Tiếp tục?".\n'
     '- Nút xác nhận "Duyệt" màu xanh, KHÔNG phải màu đỏ; có nút Hủy.'),
    ('002', 'Bấm Hủy trên hộp thoại xác nhận', 'P0',
     'Đang mở hộp thoại xác nhận, Ghi chú đã gõ "test 01". Hàng giữ H của K1 đang là 5.',
     '1. Bấm Hủy.',
     'Ghi chú: test 01',
     '- Hộp thoại đóng, vẫn ở màn lập phiếu, dữ liệu còn nguyên.\n'
     '- Không có phiếu mới ở danh sách; hàng giữ vẫn là 5.'),
    ('003', 'Lập phiếu thành công quay về danh sách', 'P0',
     'Nhân viên N giữ hàng H cho K1 còn 5 cái.',
     '1. Chọn N, thêm H, dòng K1 gõ 2, Ghi chú "huỷ test 01".\n'
     '2. Bấm Duyệt, xác nhận.',
     'Duyệt huỷ: 2\nGhi chú: huỷ test 01',
     '- Thông báo "Duyệt thành công".\n'
     '- Quay về màn DANH SÁCH (không ở lại form, không sang chi tiết).\n'
     '- Dòng đầu tiên là phiếu mới mã KTPHHG-xxxxx (5 chữ số), Huỷ của nhân viên = N, Người tạo = '
     'người đang đăng nhập, Ngày tạo = lúc vừa lập.'),
    ('004', 'Hàng giữ bị trừ đúng số', 'P0',
     'Trước khi duyệt: màn Danh sách hàng giữ ghi hàng H của N cho K1 = 5.',
     '1. Lập phiếu huỷ 2 cái hàng H cho K1.\n'
     '2. Mở lại màn Danh sách hàng giữ, tìm H của N cho K1.',
     'Duyệt huỷ: 2',
     '- Còn 3.\n'
     '- Trừ trên hàng giữ của NHÂN VIÊN BỊ HUỶ (N), không đụng hàng giữ của kế toán lập phiếu.'),
    ('005', 'Trừ theo thứ tự hạn giữ sớm trước', 'P0',
     'Hàng H của N cho K1 nằm trên 2 lô: lô hạn 15/10/2026 còn 3, lô hạn 31/12/2026 còn 5.',
     '1. Lập phiếu huỷ 4 cái H cho K1.\n'
     '2. Xem từng lô ở màn Danh sách hàng giữ (hoặc lịch sử giữ hàng của H).',
     'Duyệt huỷ: 4',
     '- Lô hạn 15/10/2026 về 0.\n'
     '- Lô hạn 31/12/2026 còn 4.\n'
     '- Lịch sử phiếu ghi "Đã trừ tồn hàng giữ trên 2 lô.".'),
    ('006', 'Lô đã quá hạn giữ vẫn bị trừ trước', 'P1',
     'Hàng H của N cho K1: lô hạn 01/09/2026 (đã quá hạn) còn 2, lô hạn 31/12/2026 còn 5.',
     '1. Lập phiếu huỷ 3 cái H cho K1.',
     'Duyệt huỷ: 3',
     '- Lô quá hạn về 0, lô 31/12/2026 còn 4.\n'
     '- Số Có thể huỷ trên form lúc đầu là 7 (tính cả lô quá hạn).'),
    ('007', 'Phiếu nhiều hàng hoá nhiều khách', 'P0',
     'N giữ H1 cho K1 (5), K2 (4); giữ H2 cho K1 (10).',
     '1. Thêm H1 và H2.\n'
     '2. H1: K1 = 1, thêm khách K2 = 4. H2: K1 = 10.\n'
     '3. Duyệt, xác nhận.',
     'H1-K1: 1\nH1-K2: 4\nH2-K1: 10',
     '- Lập phiếu thành công.\n'
     '- H1-K1 còn 4, H1-K2 còn 0, H2-K1 còn 0.\n'
     '- Chi tiết phiếu: STT 1 là H1 gộp 2 dòng khách, STT 2 là H2 một dòng.'),
    ('008', 'Không có trạng thái nháp, không sửa, không xoá sau khi lập', 'P0',
     'Vừa lập phiếu KTPHHG-00605.',
     '1. Tìm phiếu ở danh sách, xem cột Hành động.\n'
     '2. Mở chi tiết, xem các nút cuối màn.',
     '—',
     '- Danh sách chỉ có In, Lịch sử.\n'
     '- Chi tiết chỉ có In, Quay lại.\n'
     '- Không có cách nào sửa / xoá / huỷ duyệt phiếu — đúng thiết kế.'),
    ('009', 'Chống bấm Duyệt hai lần', 'P1',
     'Phiếu hợp lệ, mạng chậm.',
     '1. Bấm Duyệt, xác nhận.\n'
     '2. Trong lúc đang xử lý bấm Duyệt tiếp nhiều lần.',
     '—',
     '- Chỉ tạo đúng 1 phiếu, hàng giữ chỉ bị trừ 1 lần.'),
    ('010', 'Lập phiếu huỷ hàng giữ của chính mình', 'P2',
     'Kế toán B đang giữ 3 cái hàng H cho K1.',
     '1. B chọn chính B ở ô "Huỷ của nhân viên".\n'
     '2. Huỷ 1 cái H cho K1, Duyệt, xác nhận.',
     'Duyệt huỷ: 1',
     '- Lập phiếu thành công, hàng giữ còn 2.\n'
     '- B KHÔNG nhận thông báo (không tự báo cho chính mình).'),
    ('011', 'Hàng hoá thiếu Model / Thương hiệu vẫn lập được', 'P1',
     'N giữ hàng H không khai Model và Thương hiệu.',
     '1. Lập phiếu huỷ 1 cái H.\n'
     '2. Mở chi tiết phiếu.',
     'Duyệt huỷ: 1',
     '- Lập phiếu thành công (hệ thống cũ báo lỗi ở trường hợp này).\n'
     '- Ô Model và Thương hiệu ở chi tiết để TRỐNG.'),
    ('012', 'Kế toán khác công ty với nhân viên chủ lô', 'P0',
     'Kế toán B thuộc công ty 1. Nhân viên P thuộc công ty 4 giữ 8 cái hàng H cho K1.',
     '1. B lập phiếu huỷ 3 cái H của P cho K1.\n'
     '2. Xem hàng giữ H của P.\n'
     '3. B xem danh sách; kế toán D công ty 4 xem danh sách.',
     'Duyệt huỷ: 3',
     '- Cửa sổ chọn hàng và ô Có thể huỷ hiện đúng hàng giữ của P ở công ty 4 (Có thể huỷ = 8).\n'
     '- Lập phiếu thành công, hàng giữ H của P còn 5 (trừ đúng lô công ty 4).\n'
     '- Phiếu nằm ở danh sách của B (công ty 1); D KHÔNG thấy phiếu — đúng thiết kế.'),
]

S8 = [
    ('001', 'Ô Duyệt huỷ để trống khi bấm Duyệt', 'P0',
     'Đã thêm hàng H, dòng K1 chưa gõ số.',
     '1. Bấm Duyệt.',
     'Duyệt huỷ: (để trống)',
     '- Dưới ô hiện chữ đỏ "Chưa nhập số lượng".\n'
     '- Thông báo "Bạn chưa nhập đầy đủ thông tin.", màn tự cuộn tới ô lỗi đầu tiên.\n'
     '- KHÔNG hiện hộp thoại xác nhận, không lưu.'),
    ('002', 'Ô trống chưa báo lỗi khi đang gõ', 'P2',
     'Đã thêm hàng H.',
     '1. Gõ 3 vào Duyệt huỷ rồi xoá hết.',
     '—',
     '- Chưa báo lỗi đỏ khi chưa bấm Duyệt.'),
    ('003', 'Nhập 0', 'P0',
     'Đã thêm hàng H, Có thể huỷ = 5.',
     '1. Gõ 0 vào Duyệt huỷ.',
     'Duyệt huỷ: 0',
     '- Báo đỏ ngay "Phải lớn hơn 0".\n'
     '- Bấm Duyệt: thông báo lỗi kèm tên hàng, không lưu.'),
    ('004', 'Nhập vượt Có thể huỷ', 'P0',
     'Dòng K1 hàng H, ĐVT Cái, Có thể huỷ = 5.',
     '1. Gõ 7 vào Duyệt huỷ.\n'
     '2. Bấm Duyệt.',
     'Duyệt huỷ: 7',
     '- Báo đỏ ngay dưới ô "Vượt số có thể huỷ (tối đa 5)".\n'
     '- Ô GIỮ NGUYÊN số 7, KHÔNG tự kéo về 5.\n'
     '- Bấm Duyệt: thông báo ""<tên hàng H>": Vượt số có thể huỷ (tối đa 5)" (không phải câu '
     '"chưa nhập đầy đủ thông tin"), không hiện hộp thoại xác nhận.'),
    ('005', 'Sửa về số hợp lệ thì hết lỗi', 'P1',
     'Ô Duyệt huỷ đang 7, báo đỏ vượt 5.',
     '1. Sửa thành 5.',
     'Duyệt huỷ: 5',
     '- Lỗi đỏ biến mất ngay (bằng đúng trần vẫn hợp lệ).'),
    ('006', 'Ô số lượng không nhận chữ, dấu trừ, ký tự đặc biệt', 'P0',
     'Đã thêm hàng H.',
     '1. Gõ "abc".\n'
     '2. Gõ "-3".\n'
     '3. Gõ "5@#".',
     'Duyệt huỷ: abc / -3 / 5@#',
     '- "abc": ô vẫn trống.\n'
     '- "-3": ô chỉ còn 3.\n'
     '- "5@#": ô chỉ còn 5.'),
    ('007', 'Phần thập phân dùng dấu chấm, tối đa 2 số lẻ', 'P0',
     'Đã thêm hàng H, Có thể huỷ = 50.',
     '1. Gõ "1.255".\n'
     '2. Xoá, gõ "1,5".',
     'Duyệt huỷ: 1.255 / 1,5',
     '- "1.255" thành 1.25 (bỏ chữ số lẻ thứ ba).\n'
     '- Lưu ý: "1,5" thành 15 vì dấu phẩy bị bỏ — QA dùng dấu chấm cho số lẻ.'),
    ('008', 'Gõ dở dấu chấm', 'P2',
     'Đã thêm hàng H, Có thể huỷ = 5.',
     '1. Gõ "2." rồi dừng.\n'
     '2. Bấm Duyệt.',
     'Duyệt huỷ: 2.',
     '- Lúc gõ dở không báo lỗi.\n'
     '- Bấm Duyệt được coi là 2, hiện hộp thoại xác nhận bình thường.'),
    ('009', 'Nhiều dòng lỗi thì cuộn tới dòng lỗi đầu tiên', 'P1',
     'Phiếu có 8 dòng khách hàng, dòng thứ 6 để trống số lượng.',
     '1. Bấm Duyệt.',
     '—',
     '- Thông báo "Bạn chưa nhập đầy đủ thông tin.".\n'
     '- Màn tự cuộn tới dòng thứ 6.'),
    ('010', 'Ghi chú tối đa 255 ký tự', 'P1',
     'Đang ở màn lập phiếu.',
     '1. Dán đoạn 300 ký tự vào ô Ghi chú.',
     'Ghi chú: chuỗi 300 ký tự',
     '- Ô chỉ nhận 255 ký tự đầu.\n'
     '- Gọi thẳng chức năng Lập phiếu với ghi chú 300 ký tự: báo "Không được vượt quá 255 ký tự".'),
    ('011', 'Bỏ trống Ghi chú vẫn lập được', 'P1',
     'Phiếu hợp lệ.',
     '1. Để trống Ghi chú, Duyệt, xác nhận.',
     'Ghi chú: (để trống)',
     '- Lập thành công.\n'
     '- Ô Ghi chú ở chi tiết và cột Ghi chú ở danh sách để TRỐNG.'),
    ('012', 'Số lớn hiển thị theo chuẩn quốc tế', 'P2',
     'Hàng H: K1 còn 12,500 cái.',
     '1. Đọc ô Có thể huỷ.\n'
     '2. Gõ 1250.5, Duyệt, xác nhận, mở chi tiết.',
     'Duyệt huỷ: 1250.5',
     '- Có thể huỷ hiện 12,500.\n'
     '- Chi tiết hiện Duyệt huỷ 1,250.5.'),
]

S9 = [
    ('001', 'Nội dung khối Thông tin chung ở chi tiết', 'P0',
     'Phiếu KTPHHG-00605 huỷ hàng của nhân viên NV0123 - Nguyễn Văn An (phòng Kinh doanh 2), do '
     'Trần Thị Bình lập lúc 29/09/2026 14:05, ghi chú "huỷ test 01".',
     '1. Mở chi tiết KTPHHG-00605.',
     '—',
     '- Tiêu đề "Chi tiết phiếu huỷ hàng giữ kế toán: KTPHHG-00605".\n'
     '- Ô Mã phiếu: KTPHHG-00605; Huỷ của nhân viên: "NV0123 - Nguyễn Văn An"; Phòng ban: Kinh doanh '
     '2; Ghi chú: huỷ test 01.\n'
     '- Góc phải: "Người tạo: Trần Thị Bình · 29/09/2026 14:05".\n'
     '- Mọi ô đều chỉ đọc.'),
    ('002', 'Bảng chi tiết ở màn xem', 'P0',
     'Phiếu có hàng H1 cho 2 khách, H2 cho 1 khách.',
     '1. Mở chi tiết.\n'
     '2. Đọc tiêu đề cột và nội dung.',
     '—',
     '- Cột: STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, Khách hàng, nhóm "Số lượng" gồm '
     'Duyệt huỷ và ĐVT.\n'
     '- KHÔNG có cột Có thể huỷ, không có nút thùng rác, không có liên kết Thêm khách hàng.\n'
     '- H1 gộp ô trên 2 dòng khách; H2 một dòng.'),
    ('003', 'Chi tiết phiếu cũ từ hệ thống cũ', 'P1',
     'Một phiếu cũ nhiều khách hàng lập trên hệ thống cũ.',
     '1. Mở chi tiết phiếu đó.',
     '—',
     '- Hiển thị đủ thông tin, bảng gộp ô đúng số khách.\n'
     '- Khách hàng không còn trong danh mục thì hiện "Khách hàng #<số>", không để trống dòng.'),
    ('004', 'Nút ở cuối màn chi tiết', 'P0',
     'Phiếu do chính người đang đăng nhập lập.',
     '1. Mở chi tiết, đọc các nút cuối màn.',
     '—',
     '- Chỉ có In (nút trắng, biểu tượng máy in) và Quay lại.\n'
     '- KHÔNG có Sửa, Xoá, Duyệt.'),
    ('005', 'Quay lại về danh sách', 'P1',
     'Đang ở chi tiết, trước đó danh sách lọc Người tạo = B.',
     '1. Bấm Quay lại.',
     '—',
     '- Về màn danh sách, không hỏi cảnh báo chưa lưu.\n'
     '- Bộ lọc Người tạo = B vẫn giữ.'),
    ('006', 'Mở phiếu công ty khác bằng đường dẫn trực tiếp', 'P0',
     'Kế toán B công ty 1 có quyền "Quản lý giữ hàng". Phiếu Y thuộc công ty 4.',
     '1. Đăng nhập B.\n'
     '2. Gõ thẳng đường dẫn chi tiết phiếu Y lên thanh địa chỉ.',
     '—',
     '- Báo "Bạn không có quyền xem phiếu này".\n'
     '- Tự quay về màn danh sách, không hiện dữ liệu phiếu Y, không treo trang.'),
    ('007', 'Mở phiếu không tồn tại', 'P2',
     'Không có phiếu nào ứng với số 999999.',
     '1. Gõ đường dẫn chi tiết với số 999999.',
     '—',
     '- Báo "Không tìm thấy phiếu huỷ hàng giữ kế toán này.".\n'
     '- Tự quay về màn danh sách.'),
]

S10 = [
    ('001', 'Lịch sử ngay sau khi lập phiếu', 'P0',
     'Vừa lập phiếu KTPHHG-00605, trừ trên 2 lô.',
     '1. Mở chi tiết KTPHHG-00605.\n'
     '2. Bấm "Xem lịch sử" ở khối Lịch sử thay đổi.',
     '—',
     '- Có đúng 1 mốc, nhãn "Tạo mới" màu xanh lá.\n'
     '- Thời điểm dạng dd/mm/yyyy hh:mm.\n'
     '- Dòng "Người thực hiện: <tên> - <phòng ban>".\n'
     '- Ghi chú "Đã trừ tồn hàng giữ trên 2 lô.".\n'
     '- Mốc Tạo mới KHÔNG liệt kê chi tiết từng hàng hoá.'),
    ('002', 'Mở / thu gọn / làm mới khối lịch sử', 'P2',
     'Đang ở chi tiết phiếu có lịch sử.',
     '1. Quan sát khối Lịch sử thay đổi khi vừa vào.\n'
     '2. Bấm "Xem lịch sử".\n'
     '3. Bấm "Làm mới", rồi "Thu gọn".',
     '—',
     '- Vừa vào: khối đang thu gọn, tiêu đề có số mốc.\n'
     '- Bấm Xem lịch sử: hiện danh sách mốc, xuất hiện nút Làm mới.\n'
     '- Bấm Thu gọn: đóng lại.'),
    ('003', 'Lịch sử mở từ cột Hành động', 'P1',
     'Phiếu KTPHHG-00605 có lịch sử.',
     '1. Ở dòng KTPHHG-00605 bấm nút Lịch sử.',
     '—',
     '- Cửa sổ "Lịch sử phiếu huỷ hàng giữ kế toán" kèm mã KTPHHG-00605.\n'
     '- Nội dung giống khối lịch sử ở chi tiết; có nút Đóng.'),
    ('004', 'Phiếu cũ không có lịch sử', 'P1',
     'Phiếu cũ lập trên hệ thống cũ.',
     '1. Mở chi tiết, bấm "Xem lịch sử".',
     '—',
     '- Hiện câu "Chưa có lịch sử thao tác nào." — đúng, không phải lỗi.'),
    ('005', 'Lịch sử giữ hàng ghi nhận phiếu huỷ kế toán', 'P1',
     'Vừa lập phiếu KTPHHG-00605 huỷ 4 cái hàng H của N cho K1.',
     '1. Vào màn Danh sách hàng giữ, mở lịch sử giữ hàng của H (N, K1).',
     '—',
     '- Có dòng giảm tương ứng (tổng giảm 4) gắn với phiếu KTPHHG-00605.\n'
     '- Bấm vào mã phiếu thì mở được đúng chi tiết phiếu huỷ hàng giữ kế toán.'),
]

S11 = [
    ('001', 'Nhân viên bị huỷ hàng nhận thông báo', 'P0',
     'Kế toán Trần Thị Bình huỷ hàng giữ của nhân viên N (khác người).',
     '1. Bình lập phiếu, ra mã KTPHHG-00605.\n'
     '2. Đăng nhập bằng N, mở chuông thông báo.',
     '—',
     '- N có thông báo "[TC] Huỷ hàng giữ: KTPHHG-00605. Trần Thị Bình vừa huỷ hàng giữ của bạn.".\n'
     '- Thông báo hiện ngay (không cần tải lại trang) và có trên ứng dụng điện thoại.'),
    ('002', 'Bấm thông báo mở chi tiết phiếu', 'P1',
     'N có thông báo phiếu KTPHHG-00605. N có quyền "Quản lý giữ hàng" và cùng công ty người lập.',
     '1. N bấm vào thông báo.',
     '—',
     '- Mở đúng màn chi tiết KTPHHG-00605.'),
    ('003', 'Người nhận thông báo không có quyền xem phiếu', 'P1',
     'N là nhân viên kinh doanh, KHÔNG có quyền "Quản lý giữ hàng", có thông báo phiếu KTPHHG-00605.',
     '1. N bấm vào thông báo.',
     '—',
     '- Hành vi hiện tại: báo "Bạn không có quyền xem phiếu này" và quay về danh sách (danh sách '
     'cũng báo chưa có quyền).\n'
     '- Lưu ý: phạm vi xem giữ như hệ thống cũ nên N chỉ đọc được nội dung trên thông báo; ghi nhận '
     'kết quả để chủ dự án quyết định có mở quyền xem cho người bị huỷ hay không.'),
    ('004', 'Không gửi thông báo khi tự huỷ hàng của mình', 'P2',
     'Kế toán B huỷ hàng giữ của chính B.',
     '1. Lập phiếu.\n'
     '2. Xem chuông thông báo của B.',
     '—',
     '- Không có thông báo mới cho B.'),
]

S12 = [
    ('001', 'In phiếu từ cột Hành động', 'P0',
     'Phiếu KTPHHG-00605.',
     '1. Ở dòng KTPHHG-00605 bấm nút In.',
     '—',
     '- Mở CỬA SỔ xem trước ngay trên màn, tiêu đề "Xem trước phiếu KTPHHG-00605".\n'
     '- KHÔNG mở tab mới.'),
    ('002', 'In phiếu từ màn chi tiết', 'P0',
     'Đang ở chi tiết KTPHHG-00605.',
     '1. Bấm In ở cuối màn.',
     '—',
     '- Mở cửa sổ xem trước "Xem trước phiếu KTPHHG-00605", nội dung giống khi in từ danh sách.'),
    ('003', 'Nội dung bản in phiếu', 'P0',
     'Phiếu KTPHHG-00605 lập ngày 29/09/2026, huỷ hàng của Nguyễn Văn An, hàng H1 cho 2 khách, '
     'không có ghi chú.',
     '1. Mở xem trước bản in.\n'
     '2. Đọc nội dung.',
     '—',
     '- Tiêu đề "PHIẾU HUỶ HÀNG GIỮ KẾ TOÁN", dòng "Số phiếu: KTPHHG-00605", "Ngày tạo: 29/09/2026".\n'
     '- Khối thông tin: Huỷ của nhân viên, Phòng ban, Người tạo, Ghi chú (trống thì in ".....").\n'
     '- Bảng: STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, Khách hàng, SL duyệt huỷ, ĐVT; H1 '
     'gộp ô trên 2 dòng khách.\n'
     '- Ba ô ký: Người lập phiếu, Kế toán trưởng, Nhân viên giữ hàng.'),
    ('004', 'Tiêu đề công ty theo công ty của phiếu', 'P1',
     'Tài khoản quản trị cao nhất thuộc công ty 1 in phiếu X thuộc công ty 4.',
     '1. Mở bản in phiếu X.',
     '—',
     '- Ảnh tiêu đề đầu trang là của công ty 4 (công ty của phiếu), không phải công ty 1.'),
    ('005', 'In danh sách theo bộ lọc', 'P0',
     'Đang lọc Ngày tạo 01/09/2026 - 29/09/2026, kết quả 37 phiếu.',
     '1. Bấm nút In trên thanh công cụ danh sách.',
     'Ngày tạo: 01/09/2026 - 29/09/2026',
     '- Cửa sổ "Xem trước danh sách phiếu huỷ hàng giữ kế toán", khổ giấy NGANG.\n'
     '- Tiêu đề "DANH SÁCH PHIẾU HUỶ HÀNG GIỮ KẾ TOÁN".\n'
     '- Dòng "Khoảng thời gian: Từ ngày 01/09/2026 đến ngày 29/09/2026" và "Tổng số phiếu: 37".\n'
     '- Bảng 5 cột: STT, Mã phiếu, Huỷ của nhân viên, Ngày lập, Người lập; đúng 37 dòng.'),
    ('006', 'In danh sách không lọc ngày', 'P2',
     'Không áp lọc ngày, lọc Người tạo = B (12 phiếu).',
     '1. Bấm In trên thanh công cụ.',
     '—',
     '- KHÔNG có dòng "Khoảng thời gian".\n'
     '- "Tổng số phiếu: 12", bảng 12 dòng.'),
    ('007', 'Đóng cửa sổ xem trước', 'P2',
     'Cửa sổ xem trước đang mở.',
     '1. Bấm nút đóng.',
     '—',
     '- Cửa sổ đóng, vẫn ở màn cũ, bộ lọc không mất.'),
]

S13 = [
    ('001', 'Mở cửa sổ chọn trường xuất', 'P0',
     'Bảng đang hiện bộ cột mặc định (Ghi chú tắt).',
     '1. Bấm Xuất Excel.',
     '—',
     '- Cửa sổ "Chọn trường xuất Excel" với 7 trường: Mã phiếu, Huỷ của nhân viên, Ngày tạo, Người '
     'tạo, Người cập nhật, Ngày cập nhật, Ghi chú.\n'
     '- Tích sẵn đúng 6 trường đang hiện trên bảng; Ghi chú chưa tích.\n'
     '- Chân cửa sổ ghi "Đang chọn 6/7 trường".'),
    ('002', 'Xuất tệp theo bộ lọc đang áp', 'P0',
     'Đang lọc Người tạo = B, kết quả 12 phiếu.',
     '1. Bấm Xuất Excel, bấm Xuất file.\n'
     '2. Mở tệp tải về.',
     '—',
     '- Thông báo "Xuất Excel thành công", tệp tên danh_sach_huy_hang_giu_ke_toan.xlsx.\n'
     '- Dòng đầu "DANH SÁCH PHIẾU HUỶ HÀNG GIỮ KẾ TOÁN", cột STT luôn đứng đầu.\n'
     '- Đúng 12 dòng dữ liệu, Người tạo đều là B.'),
    ('003', 'Thứ tự cột theo thứ tự kéo trong cửa sổ', 'P1',
     'Cửa sổ chọn trường đang mở.',
     '1. Bấm Bỏ chọn hết.\n'
     '2. Tích Ghi chú, Mã phiếu, Người tạo.\n'
     '3. Kéo biểu tượng ba gạch đưa Ghi chú lên trên Mã phiếu.\n'
     '4. Xuất file, mở tệp.',
     '—',
     '- Cột trong tệp: STT, Ghi chú, Mã phiếu, Người tạo (đúng thứ tự trong cửa sổ).'),
    ('004', 'Dòng khoảng thời gian và khối ký tên', 'P1',
     'Đang lọc Ngày tạo 01/09/2026 - 29/09/2026.',
     '1. Xuất file, mở tệp.',
     '—',
     '- Dòng thứ hai ghi "Từ ngày 01/09/2026 đến ngày 29/09/2026".\n'
     '- Cuối bảng cách 1 dòng có khối "Ngày…….Tháng…….Năm…….", "Người lập", "(Ký, họ tên)".\n'
     '- Các dòng tiêu đề được cố định khi cuộn.'),
    ('005', 'Định dạng ô trong tệp', 'P1',
     'Tệp vừa xuất có cột Ngày tạo, Ghi chú; có phiếu ghi chú là "123" và phiếu không có ghi chú.',
     '1. Mở tệp, xem các ô.',
     '—',
     '- Ngày dạng dd/mm/yyyy hh:mm, căn giữa.\n'
     '- Ô ghi chú "123" KHÔNG bị Excel gắn tam giác xanh cảnh báo.\n'
     '- Ô không có dữ liệu để TRỐNG.'),
    ('006', 'Không cho xuất khi bỏ chọn hết', 'P2',
     'Cửa sổ chọn trường đang mở.',
     '1. Bấm Bỏ chọn hết.\n'
     '2. Bấm Xuất file.',
     '—',
     '- Chân cửa sổ ghi "Đang chọn 0/7 trường".\n'
     '- Bấm Xuất file không có tác dụng, không tải tệp nào.'),
    ('007', 'Phạm vi công ty áp cho tệp xuất', 'P0',
     'Kế toán B công ty 1 (580 phiếu). Toàn hệ thống 604 phiếu.',
     '1. Không lọc gì, Xuất Excel, Xuất file.\n'
     '2. Đếm dòng trong tệp.',
     '—',
     '- Tệp có đúng 580 dòng, không lộ phiếu công ty khác.'),
]

S14 = [
    ('001', 'Hai kế toán cùng huỷ một hàng giữ', 'P0',
     'N giữ hàng H cho K1 còn 5 cái. Kế toán B1, B2 đều có quyền.',
     '1. B1 và B2 cùng mở form, cùng chọn N, thêm H, dòng K1 gõ 4.\n'
     '2. B1 Duyệt, xác nhận.\n'
     '3. B2 Duyệt, xác nhận.',
     'Duyệt huỷ: 4 (cả hai)',
     '- B1 lập thành công, hàng giữ còn 1.\n'
     '- B2 bị từ chối: thông báo "Duyệt phiếu thất bại!", dưới ô báo đỏ "Vượt số có thể huỷ (tối '
     'đa 1)."; hoặc khi hai người bấm cùng lúc thì báo "Không đủ tồn hàng giữ để hủy cho "<tên '
     'hàng>": cần 4, chỉ còn 1." dưới bảng.\n'
     '- Chỉ có 1 phiếu được tạo; hàng giữ không bao giờ âm.'),
    ('002', 'Một dòng thiếu tồn thì huỷ bỏ cả phiếu', 'P0',
     'Phiếu có H1-K1 = 2 (đủ), H2-K1 = 5; trong lúc mở form, hàng giữ H2-K1 bị chứng từ khác lấy '
     'còn 1.',
     '1. Bấm Duyệt, xác nhận.\n'
     '2. Kiểm tra hàng giữ H1-K1 và danh sách phiếu.',
     '—',
     '- Báo lỗi ở dòng H2-K1, form giữ nguyên dữ liệu.\n'
     '- Hàng giữ H1-K1 KHÔNG bị trừ; không có phiếu nào được tạo — không trừ một phần.'),
    ('003', 'Đề nghị xuất kho phát sinh trong lúc mở form', 'P1',
     'Lúc mở form, H-K1 Có thể huỷ = 6. Sau đó có đề nghị xuất kho chưa hoàn tất lấy 3 cái.',
     '1. Gõ 6, Duyệt, xác nhận.',
     'Duyệt huỷ: 6',
     '- Bị từ chối, dưới ô báo "Vượt số có thể huỷ (tối đa 3).".\n'
     '- Không tạo phiếu, không trừ tồn.'),
    ('004', 'Gọi thẳng chức năng Lập phiếu với hàng trùng hoặc ĐVT lạ', 'P1',
     'Kế toán có quyền. Hàng H không có đơn vị "Thùng".',
     '1. Dùng công cụ kiểm thử API gọi Lập phiếu có hàng H xuất hiện 2 lần.\n'
     '2. Gọi lại với dòng H dùng đơn vị Thùng.',
     '—',
     '- Lần 1: từ chối, báo "Hàng hoá bị chọn trùng.".\n'
     '- Lần 2: từ chối, báo "Đơn vị tính không thuộc hàng hoá này.".\n'
     '- Không tạo phiếu, không trừ tồn.'),
    ('005', 'Gọi thẳng chức năng Lập phiếu với mọi dòng = 0', 'P1',
     'Kế toán có quyền.',
     '1. Dùng công cụ kiểm thử API gọi Lập phiếu, mọi dòng khách hàng số lượng 0.',
     'Duyệt huỷ: 0',
     '- Từ chối, báo "Phải có ít nhất 1 dòng Duyệt huỷ lớn hơn 0.".\n'
     '- Không tạo phiếu rỗng.'),
    ('006', 'Cô lập danh sách giữa hai công ty', 'P0',
     'Kế toán B công ty 1, kế toán D công ty 4, cả hai có quyền. B vừa lập phiếu KTPHHG-00605.',
     '1. D mở danh sách, tìm nhanh "00605".\n'
     '2. D xuất Excel và in danh sách không lọc.',
     'Ô tìm nhanh: 00605',
     '- D không tìm thấy KTPHHG-00605.\n'
     '- Tệp Excel và bản in danh sách của D không có phiếu nào của công ty 1.'),
]

S15 = [
    ('001', 'Đầu cuối: huỷ hàng giữ một khách một hàng', 'P0',
     'N giữ 10 cái hàng H cho K1. Kế toán B cùng công ty, có quyền.',
     '1. B vào ' + MENU + ', bấm Tạo mới.\n'
     '2. Chọn N, Thêm hàng hoá, tích H, Chọn.\n'
     '3. Dòng K1 gõ 4, Ghi chú "cuối kỳ", Duyệt, xác nhận.\n'
     '4. Mở chi tiết phiếu mới, xem lịch sử, in phiếu.\n'
     '5. Mở màn Danh sách hàng giữ; đăng nhập N xem thông báo.',
     'Duyệt huỷ: 4\nGhi chú: cuối kỳ',
     '- Sau bước 3 về danh sách, phiếu mới đứng đầu.\n'
     '- Chi tiết đúng dữ liệu; lịch sử có mốc Tạo mới "Đã trừ tồn hàng giữ trên 1 lô." (nếu 1 lô).\n'
     '- Bản in đúng nội dung.\n'
     '- Hàng giữ H-K1 còn 6; N nhận thông báo kèm mã phiếu.'),
    ('002', 'Đầu cuối: nhiều hàng, nhiều khách, nhiều ĐVT', 'P0',
     'N giữ H1 cho K1 (24 cái), K2 (12 cái); giữ H2 cho K3 (5 thùng quy đổi 5 × 20 = 100 chai). '
     'H1: Hộp = 12 Cái. H2: Thùng = 20 Chai.',
     '1. Tạo mới, chọn N, thêm H1 và H2.\n'
     '2. H1: K1 = 1 Hộp, thêm K2 = 12 Cái.\n'
     '3. H2: K3 = 2 Thùng.\n'
     '4. Duyệt, xác nhận.',
     'H1-K1: 1 Hộp\nH1-K2: 12 Cái\nH2-K3: 2 Thùng',
     '- Lập thành công.\n'
     '- H1-K1 còn 12 cái, H1-K2 còn 0, H2-K3 còn 60 chai.\n'
     '- Chi tiết ghi đúng số theo ĐVT đã chọn: 1 Hộp, 12 Cái, 2 Thùng.'),
    ('003', 'Đầu cuối: huỷ hết hàng giữ rồi mở lại form', 'P1',
     'N chỉ giữ duy nhất hàng H cho K1, còn 3 cái.',
     '1. Lập phiếu huỷ 3 cái H cho K1.\n'
     '2. Tạo mới lần nữa, chọn N, bấm Thêm hàng hoá.',
     'Duyệt huỷ: 3',
     '- Lần 1 thành công, hàng giữ về 0.\n'
     '- Lần 2 cửa sổ báo "Nhân viên này hiện không giữ hàng hoá nào.".'),
    ('004', 'Đầu cuối: phiếu huỷ thường vẫn chạy đúng sau khi có màn kế toán', 'P1',
     'N giữ 10 cái hàng H cho K1. Có phiếu yêu cầu hủy hàng giữ của N cho H-K1 số lượng 2 đang '
     'Chờ duyệt.',
     '1. Lập phiếu huỷ hàng giữ kế toán 3 cái H-K1.\n'
     '2. Vào màn Phiếu hủy hàng giữ (thường), duyệt phiếu yêu cầu kia với số 2.\n'
     '3. Xem hàng giữ và lịch sử giữ hàng của H-K1.',
     '—',
     '- Cả hai phiếu lập thành công, hàng giữ còn 5.\n'
     '- Lịch sử giữ hàng có 2 dòng giảm, mỗi dòng mở đúng loại phiếu của nó (phiếu kế toán mở chi '
     'tiết phiếu kế toán, phiếu thường mở chi tiết phiếu thường).'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP PHIẾU — CHỌN NHÂN VIÊN & HÀNG HOÁ', S4),
    ('V', 'NHIỀU KHÁCH HÀNG CHO MỘT HÀNG HOÁ', S5),
    ('VI', 'ĐƠN VỊ TÍNH & QUY ĐỔI SỐ LƯỢNG', S6),
    ('VII', 'DUYỆT PHIẾU & TRỪ HÀNG GIỮ', S7),
    ('VIII', 'RÀNG BUỘC NHẬP LIỆU', S8),
    ('IX', 'XEM CHI TIẾT PHIẾU', S9),
    ('X', 'LỊCH SỬ THAY ĐỔI', S10),
    ('XI', 'THÔNG BÁO CHO NHÂN VIÊN BỊ HUỶ HÀNG', S11),
    ('XII', 'IN PHIẾU & IN DANH SÁCH', S12),
    ('XIII', 'XUẤT EXCEL', S13),
    ('XIV', 'CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI', S14),
    ('XV', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S15),
]

build(output_file=os.path.join(BASE, 'testcase - Phieu huy hang giu ke toan.xlsx'),
      sheet_name='Trang tính1',
      feature_name='Phiếu huỷ hàng giữ kế toán',
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
