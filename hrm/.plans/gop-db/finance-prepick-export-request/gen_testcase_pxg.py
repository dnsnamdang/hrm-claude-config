# -*- coding: utf-8 -*-
"""Sinh testcase cho man "Phieu xuat giu" (PXG) — phan he Tai chinh.

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

MODULE = 'Phiếu xuất giữ'

DESCRIPTION_BLOCK = [
    ('1. Mục đích tính năng',
     'Màn hình Phiếu xuất giữ (mã phiếu PXG) dành cho Kế toán, là bước cuối của luồng giữ hàng.\n'
     '⚠️ Đây là chứng từ DUY NHẤT trong hệ thống sinh ra lô hàng giữ. Bấm "Duyệt giữ hàng" là '
     'lúc số lượng được cộng thật vào kho hàng giữ.\n'
     'Phiếu luôn thuộc về đúng một Yêu cầu xuất giữ (PYCXG) và không tồn tại độc lập.\n'
     'Đường dẫn: Phân hệ Tài chính → Giữ hàng → Phiếu xuất giữ.'),
    ('2. Đối tượng được tính / hiển thị',
     'Danh sách hiển thị phiếu theo phạm vi quyền của người đăng nhập:\n'
     '- Có quyền "Xem phiếu hàng giữ theo tổng công ty": toàn bộ phiếu của mọi công ty.\n'
     '- Có quyền "Xem phiếu hàng giữ theo công ty": phiếu thuộc công ty của mình.\n'
     '- Có quyền "Xem phiếu hàng giữ theo phòng ban": phiếu thuộc phòng ban mình quản lý, phòng '
     'ban của chính mình, cộng phiếu do chính mình lập.\n'
     '- Không có quyền nào ở trên: chỉ phiếu do chính mình lập.\n'
     '⚠️ Người có quyền "Kế toán duyệt hàng giữ" còn xem được TOÀN BỘ phiếu trong công ty mình.\n'
     '⚠️ Công ty và phòng ban ghi trên phiếu lấy theo NGƯỜI LẬP YÊU CẦU, không phải theo Kế '
     'toán lập phiếu — nên phạm vi dữ liệu chạy theo tổ chức bên yêu cầu.'),
    ('3. Đối tượng bị ẩn / không tính',
     '- Phiếu ở trạng thái "Đang tạo" (nháp) của người khác: KHÔNG hiện trong danh sách và không '
     'mở được màn chi tiết.\n'
     '- Ô lọc "Tên, mã hàng" chỉ xét dòng hàng CÓ TÍCH "Cần xuất".\n'
     '- Bảng chi tiết chỉ nạp những dòng hàng ĐÃ ĐƯỢC TÍCH "Cần xuất" ở yêu cầu nguồn; dòng '
     'người lập yêu cầu không xin giữ thì không xuất hiện.\n'
     '- Ô Hợp đồng ẩn hẳn khi yêu cầu nguồn thuộc loại "Xuất giữ khác".\n'
     '- Ô Địa chỉ ẩn hẳn khi khách hàng chưa khai địa chỉ.\n'
     '- Cột "SL giữ (ĐV cơ bản)" chỉ hiện ở màn chi tiết của phiếu đã duyệt.'),
    ('4. Bộ lọc thời gian áp dụng cho',
     'Hai ô "Ngày tạo từ" và "Ngày tạo đến" lọc theo NGÀY LẬP PHIẾU XUẤT GIỮ — không phải ngày '
     'lập yêu cầu, không phải ngày duyệt và không phải "Giữ đến ngày".\n'
     'Khoảng ngày lấy trọn hai đầu mút. Chỉ nhập một đầu thì lọc một chiều.'),
    ('5. Cấu trúc dữ liệu / cây phân cấp',
     'Quan hệ cha – con: một Yêu cầu xuất giữ có tối đa MỘT Phiếu xuất giữ.\n'
     'Một phiếu gồm phần thông tin chung (yêu cầu nguồn, khách hàng, giữ đến ngày, ghi chú, tệp '
     'đính kèm) và các dòng hàng hóa chép từ yêu cầu.\n'
     'Mỗi dòng gồm: ô tích "Cần xuất", SL yêu cầu (chỉ đọc), SL xuất giữ (Kế toán nhập) và, sau '
     'khi duyệt, SL giữ theo đơn vị cơ bản.\n'
     'Lô hàng giữ sinh ra xác định bởi bộ: hàng hóa – người yêu cầu – khách hàng – hạn giữ – '
     'công ty.'),
    ('6. Quy tắc cộng dồn / deduplicate',
     'Khi duyệt, hệ thống tìm lô hàng giữ khớp ĐÚNG bộ năm yếu tố ở trên. Có rồi thì CỘNG THÊM, '
     'chưa có thì tạo lô mới.\n'
     'Số lượng luôn được quy đổi về đơn vị cơ bản theo hệ số của đơn vị tính trên dòng trước khi '
     'cộng.\n'
     'Mỗi lần cộng ghi một dòng nhật ký biến động của lô, gồm số trước, số thay đổi và số sau.'),
    ('7. Phân quyền cấp',
     'Quyền thao tác:\n'
     '- Kế toán duyệt hàng giữ (quyền DUY NHẤT của màn này — vừa để lập phiếu, vừa để duyệt giữ '
     'hàng, vừa mở rộng phạm vi xem sang cả công ty)\n'
     'Quyền phạm vi dữ liệu:\n'
     '- Xem phiếu hàng giữ theo tổng công ty\n'
     '- Xem phiếu hàng giữ theo công ty\n'
     '- Xem phiếu hàng giữ theo phòng ban\n'
     'Sửa và xóa phiếu: chỉ người lập phiếu, và chỉ khi phiếu còn nháp.'),
    ('8. Cách tính các ô thống kê',
     'Ô "Hiển thị a–b / N": a là dòng đầu trang, b là dòng cuối trang, N là tổng số phiếu khớp '
     'bộ lọc TRONG PHẠM VI QUYỀN của người đang xem.\n'
     'Cột "SL có thể giữ" = tồn kho khả dụng, tính bằng tồn kho trừ đi phần hàng khuyến mại — '
     'đúng công thức hệ thống dùng khi kiểm tra lúc duyệt.\n'
     'Cột "SL yêu cầu" = số lượng người lập yêu cầu đã xin, là mức trần của SL xuất giữ.\n'
     'Cột "SL giữ (ĐV cơ bản)" = SL xuất giữ × hệ số quy đổi của đơn vị tính.\n'
     'Dòng "Tổng cộng" cộng cột SL yêu cầu, SL xuất giữ và SL giữ theo đơn vị cơ bản.'),
    ('9. Ghi chú đọc bảng',
     'Các bẫy dễ sai nhất của màn này:\n'
     '- ⚠️ Nút "Không duyệt" KHÔNG trả yêu cầu về cho người lập — nó lưu nháp y hệt nút "Lưu '
     'nháp". Muốn trả về thì phải sang màn Yêu cầu xuất giữ bấm "Từ chối".\n'
     '- Màn này KHÔNG có nút Tạo mới độc lập; nút "Lập từ yêu cầu" chỉ điều hướng sang màn Yêu '
     'cầu xuất giữ.\n'
     '- Lưu nháp KHÔNG kiểm tra tồn kho; Duyệt giữ hàng thì CÓ.\n'
     '- Chủ lô hàng giữ là NGƯỜI LẬP YÊU CẦU, không phải Kế toán bấm duyệt.\n'
     '- Hạn giữ ghi vào lô lấy theo ô "Giữ đến ngày" trên chính phiếu này tại lúc duyệt.\n'
     '- Đối chiếu hàng giữ phải nhìn cột "SL giữ (ĐV cơ bản)", không nhìn "SL xuất giữ".\n'
     '- Phiếu đã duyệt KHÔNG sửa và KHÔNG xóa được.\n'
     '- Cột "Người yêu cầu" và cột "Người tạo" là HAI người khác nhau.\n'
     '- Nhóm test bảo mật gọi thẳng chức năng bằng công cụ kiểm thử dành cho tester kỹ thuật.'),
]

ROLE_TCS = [
    ('00', 'Tài khoản không có quyền nào của nhóm hàng giữ vẫn vào được màn hình', 'P0',
     'Tài khoản A không có quyền Kế toán duyệt hàng giữ và không có quyền xem theo cấp. A chưa '
     'lập phiếu xuất giữ nào.',
     '1. Đăng nhập bằng A.\n'
     '2. Vào Tài chính → Giữ hàng → Phiếu xuất giữ.',
     '—',
     '- Màn hình mở được, không báo lỗi quyền.\n'
     '- Danh sách rỗng, hiện dòng "Không có dữ liệu phù hợp.".\n'
     '- Ô "Hiển thị a–b / N" ghi N = 0.\n'
     '- Bảng lọc nâng cao KHÔNG có ô Công ty và ô Phòng ban.'),
    ('01', 'Quyền "Kế toán duyệt hàng giữ" xem được toàn bộ phiếu trong công ty', 'P0',
     'Tài khoản B chỉ có quyền Kế toán duyệt hàng giữ, thuộc công ty 1. Công ty 1 có 800 phiếu '
     'đã duyệt của nhiều người lập.',
     '1. Đăng nhập bằng B.\n2. Mở màn danh sách và đọc N.',
     '—',
     '- ⚠️ N bằng số phiếu đã duyệt của công ty 1, cộng phiếu nháp của chính B.\n'
     '- B xem được phiếu do Kế toán khác trong công ty lập.'),
    ('02', 'Quyền "Xem phiếu hàng giữ theo tổng công ty" thấy phiếu của mọi công ty', 'P0',
     'Tài khoản C chỉ có quyền Xem phiếu hàng giữ theo tổng công ty.',
     '1. Đăng nhập bằng C.\n2. Đọc N.\n3. Lọc lần lượt từng công ty.',
     '—',
     '- N bằng tổng phiếu khác trạng thái "Đang tạo" của toàn hệ thống, cộng phiếu nháp của C.\n'
     '- Bảng lọc CÓ ô Công ty và ô Phòng ban.'),
    ('03', 'Quyền "Xem phiếu hàng giữ theo công ty" chỉ thấy phiếu công ty mình', 'P0',
     'Tài khoản D thuộc công ty 1, chỉ có quyền Xem phiếu hàng giữ theo công ty.',
     '1. Đăng nhập bằng D.\n2. Đọc N.\n'
     '3. Mở một phiếu của công ty khác bằng đường dẫn trực tiếp.',
     '—',
     '- N chỉ đếm phiếu của công ty 1.\n'
     '- Bước 3: hệ thống báo không có quyền xem phiếu này.'),
    ('04', 'Phạm vi phòng ban chạy theo PHÒNG CỦA NGƯỜI YÊU CẦU', 'P0',
     'Tài khoản E có quyền xem theo phòng ban, quản lý phòng P1. Kế toán thuộc phòng KT đã lập '
     'phiếu cho một yêu cầu của nhân viên thuộc phòng P1.',
     '1. Đăng nhập bằng E.\n2. Tìm phiếu đó trong danh sách.',
     '—',
     '- ⚠️ E THẤY phiếu đó, dù người lập phiếu (Kế toán) thuộc phòng KT.\n'
     '- Vì phòng ban ghi trên phiếu là phòng của người yêu cầu (P1).'),
    ('05', 'Phiếu nháp của người khác bị giấu với MỌI cấp quyền', 'P0',
     'Kế toán F lập một phiếu xuất giữ và lưu nháp. Tài khoản C có quyền xem tổng công ty.',
     '1. Đăng nhập bằng C.\n2. Tìm mã phiếu nháp của F ở ô tìm nhanh.\n'
     '3. Mở phiếu đó bằng đường dẫn trực tiếp.',
     'Mã phiếu nháp của F',
     '- Bước 2: không tìm thấy dòng nào.\n'
     '- Bước 3: hệ thống báo không có quyền xem phiếu này.\n'
     '- ⚠️ Quyền xem rộng nhất cũng KHÔNG mở được phiếu nháp của người khác.'),
    ('06', 'Người lập phiếu luôn xem được phiếu nháp của mình', 'P0',
     'Kế toán F vừa lưu nháp một phiếu.',
     '1. F mở màn danh sách và tìm mã phiếu đó.\n2. F mở màn chi tiết.',
     '—',
     '- Phiếu hiện trong danh sách với trạng thái "Đang tạo" màu xám.\n'
     '- Mở chi tiết được, có nút Sửa và Xóa.'),
    ('07', 'Danh sách và màn chi tiết dùng cùng một bộ điều kiện', 'P0',
     'Tài khoản bất kỳ đã đăng nhập.',
     '1. Ghi lại danh sách mã phiếu đang thấy ở màn danh sách.\n'
     '2. Mở lần lượt từng mã đó bằng đường dẫn trực tiếp.\n'
     '3. Lấy một mã KHÔNG có trong danh sách rồi mở bằng đường dẫn trực tiếp.',
     '—',
     '- Bước 2: mở được hết, không phiếu nào báo lỗi quyền.\n'
     '- Bước 3: hệ thống báo không có quyền xem phiếu này.'),
    ('08', 'Không có quyền Kế toán thì không lập được phiếu', 'P0',
     'Tài khoản G có quyền xem tổng công ty nhưng KHÔNG có quyền Kế toán duyệt hàng giữ.',
     '1. Đăng nhập bằng G.\n2. Mở một yêu cầu xuất giữ đang ở "Chờ KT duyệt".',
     '—',
     '- ⚠️ Nút "Lập phiếu xuất giữ" KHÔNG hiển thị.\n'
     '- Gọi thẳng chức năng lập phiếu thì bị từ chối.'),
    ('09', 'Kế toán khác công ty không lập được phiếu', 'P0',
     'Yêu cầu thuộc công ty 1. Tài khoản H có quyền Kế toán duyệt hàng giữ nhưng thuộc công ty 4.',
     '1. H mở yêu cầu đó (H có quyền xem tổng công ty nên xem được).',
     '—',
     '- Nút "Lập phiếu xuất giữ" KHÔNG hiển thị.\n'
     '- Gọi thẳng chức năng lập phiếu thì báo không đủ quyền.'),
]

S1 = [
    ('001', 'Vào màn hình lần đầu hiển thị đúng bố cục', 'P0',
     'Đã đăng nhập, có ít nhất 1 phiếu trong phạm vi quyền.',
     '1. Vào Tài chính → Giữ hàng → Phiếu xuất giữ.',
     '—',
     '- Tiêu đề trang là "Phiếu xuất giữ".\n'
     '- Khối Bộ lọc danh sách ở trên, khối bảng ở dưới.\n'
     '- Thanh công cụ có 4 nút: Lập từ yêu cầu, In, Xuất Excel, Cấu hình cột hiển thị.\n'
     '- Bảng hiển thị 10 dòng mỗi trang.'),
    ('002', 'Màn hình KHÔNG có nút Tạo mới độc lập', 'P0',
     'Đang ở màn danh sách.',
     '1. Soát thanh công cụ.',
     '—',
     '- ⚠️ Không có nút "Tạo mới".\n'
     '- Thay vào đó là nút "Lập từ yêu cầu" với chú thích "Lập phiếu xuất giữ từ một yêu cầu đã '
     'được duyệt".'),
    ('003', 'Bấm Lập từ yêu cầu chuyển sang màn Yêu cầu xuất giữ', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm nút Lập từ yêu cầu.',
     '—',
     '- ⚠️ KHÔNG mở form trống.\n'
     '- Điều hướng sang màn "Yêu cầu xuất giữ".'),
    ('004', 'Vòng quay chờ hiện trong lúc nạp dữ liệu', 'P2',
     'Đã đăng nhập.',
     '1. Vào màn hình và quan sát vùng bảng ngay khi trang vừa mở.',
     '—',
     '- Có vòng quay chờ kèm dòng "Đang tải dữ liệu..." trước khi bảng hiện dữ liệu.'),
    ('005', 'Danh sách rỗng hiển thị đúng câu thông báo', 'P1',
     'Tài khoản chưa lập phiếu nào và không có quyền xem theo cấp.',
     '1. Vào màn hình.',
     '—',
     '- Bảng hiện dòng "Không có dữ liệu phù hợp.".\n- N = 0.\n- Không có lỗi đỏ.'),
    ('006', 'Các cột mặc định hiển thị đúng thứ tự', 'P1',
     'Người dùng chưa từng đổi cấu hình cột.',
     '1. Vào màn hình và đọc dòng tiêu đề bảng.',
     '—',
     '- Thứ tự: STT, Mã phiếu, Yêu cầu xuất giữ, Người yêu cầu, Phòng yêu cầu, Người tạo, '
     'Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, Hành động.\n'
     '- Năm cột Khách hàng, Giữ đến ngày, Người cập nhật, Ngày cập nhật, Ghi chú KHÔNG hiển thị.'),
    ('007', 'Cột Người yêu cầu và cột Người tạo là hai người khác nhau', 'P0',
     'Có phiếu do Kế toán lập cho yêu cầu của nhân viên kinh doanh.',
     '1. Soát hai cột Người yêu cầu và Người tạo.',
     '—',
     '- ⚠️ Hai cột có tên khác nhau ở phần lớn các dòng.\n'
     '- Người yêu cầu là nhân viên kinh doanh, Người tạo là Kế toán.'),
    ('008', 'Cột Yêu cầu xuất giữ là liên kết mở tab mới', 'P0',
     'Có phiếu trong danh sách.',
     '1. Bấm vào mã ở cột Yêu cầu xuất giữ.',
     '—',
     '- ⚠️ Mở màn chi tiết yêu cầu trong TAB MỚI.\n'
     '- Tab hiện tại vẫn ở màn Phiếu xuất giữ.'),
    ('009', 'Mã phiếu là liên kết mở màn chi tiết', 'P0',
     'Có phiếu trong danh sách.',
     '1. Bấm vào mã phiếu ở cột thứ hai.',
     '—',
     '- Chuyển sang màn chi tiết đúng phiếu đó, cùng tab.\n'
     '- Tiêu đề màn ghi "Chi tiết phiếu xuất giữ: <mã phiếu>".'),
    ('010', 'Màu nhãn trạng thái đúng quy ước', 'P1',
     'Danh sách có cả phiếu nháp và phiếu đã duyệt.',
     '1. Soát cột Trạng thái.',
     '—',
     '- "Đang tạo" màu XÁM.\n- "Đã duyệt" màu XANH LÁ.\n'
     '- ⚠️ Không trạng thái nào tô ĐỎ.'),
    ('011', 'Cột Người duyệt để trống với phiếu còn nháp', 'P1',
     'Có phiếu ở trạng thái Đang tạo.',
     '1. Soát cột Người duyệt và Ngày duyệt của phiếu đó.',
     '—',
     '- Hai ô để TRỐNG hẳn, không in dấu "—" hay "-".'),
    ('012', 'Nút hành động ẩn hẳn khi không dùng được', 'P0',
     'Danh sách có cả phiếu nháp của mình và phiếu đã duyệt.',
     '1. Soát cột Hành động của từng dòng.',
     '—',
     '- ⚠️ Không có nút nào ở trạng thái mờ.\n'
     '- Nút Sửa, Xóa chỉ hiện ở phiếu Đang tạo do chính mình lập.\n'
     '- Nút In và Lịch sử hiện ở mọi dòng.\n'
     '- ⚠️ KHÔNG có nút Duyệt ở cột Hành động.'),
    ('013', 'Vào màn hình bằng đường dẫn trực tiếp', 'P2',
     'Đã đăng nhập.',
     '1. Gõ /finance/warehouse-prepick-requests lên thanh địa chỉ.',
     '—',
     '- Màn hình mở đúng, không phải qua menu.'),
    ('014', 'Phiên đăng nhập hết hạn', 'P1',
     'Đang ở màn danh sách, phiên đăng nhập đã hết hiệu lực.',
     '1. Bấm nút Tìm kiếm.',
     '—',
     '- Hệ thống điều hướng về màn đăng nhập.'),
]

S2 = [
    ('001', 'Tìm nhanh theo mã phiếu đầy đủ', 'P0',
     'Có phiếu PXG-02190 trong phạm vi quyền.',
     '1. Gõ PXG-02190 vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     'PXG-02190',
     '- Danh sách còn đúng 1 dòng.\n- N = 1.'),
    ('002', 'Tìm nhanh theo một phần mã phiếu', 'P1',
     'Có nhiều phiếu mã bắt đầu bằng PXG-021.',
     '1. Gõ 021 vào ô tìm nhanh.\n2. Bấm Tìm kiếm.',
     '021',
     '- Mọi dòng trả về đều có chuỗi "021" trong mã phiếu.\n'
     '- ⚠️ Dòng trùng khít lên đầu, rồi tới dòng bắt đầu bằng, rồi tới dòng chỉ chứa.'),
    ('003', 'Ô tìm nhanh KHÔNG tự lọc khi đang gõ', 'P1',
     'Đang ở màn danh sách.',
     '1. Gõ vài ký tự vào ô tìm nhanh rồi dừng 5 giây, KHÔNG bấm Tìm kiếm.',
     'PXG',
     '- Bảng KHÔNG đổi.\n- Chỉ bấm Tìm kiếm hoặc nhấn Enter mới lọc.'),
    ('004', 'Tìm nhanh không tìm theo mã yêu cầu', 'P0',
     'Có phiếu PXG-02190 lập từ yêu cầu PYCXG-02219.',
     '1. Gõ PYCXG-02219 vào ô tìm nhanh rồi bấm Tìm kiếm.',
     'PYCXG-02219',
     '- ⚠️ Không có kết quả — ô tìm nhanh chỉ tìm theo mã PHIẾU XUẤT GIỮ.\n'
     '- Muốn tìm theo yêu cầu thì dùng ô "Yêu cầu xuất giữ" ở bảng lọc nâng cao.'),
    ('005', 'Mở bảng lọc nâng cao', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm nút Tìm kiếm nâng cao.',
     '—',
     '- Bảng lọc mở ra, nhãn nút đổi thành "Ẩn tìm kiếm nâng cao".'),
    ('006', 'Lọc theo Yêu cầu xuất giữ', 'P0',
     'Có phiếu lập từ yêu cầu PYCXG-02219.',
     '1. Gõ 02219 vào ô Yêu cầu xuất giữ.',
     '02219',
     '- ⚠️ Bảng tự lọc lại NGAY, không cần bấm nút.\n'
     '- Chỉ ra phiếu có yêu cầu nguồn khớp mã đó.'),
    ('007', 'Lọc theo Mã phiếu ở bảng nâng cao', 'P1',
     'Bảng lọc nâng cao đang mở.',
     '1. Gõ 02190 vào ô Mã phiếu.',
     '02190',
     '- Bảng tự lọc lại ngay, mọi dòng có chuỗi 02190 trong mã phiếu.'),
    ('008', 'Lọc theo Trạng thái', 'P0',
     'Hệ thống có cả phiếu nháp và phiếu đã duyệt.',
     '1. Chọn Trạng thái = Đã duyệt.',
     '—',
     '- Cột Trạng thái toàn bộ là "Đã duyệt".'),
    ('009', 'Lọc Trạng thái = Đang tạo chỉ ra phiếu của mình', 'P0',
     'Hệ thống có nhiều phiếu nháp của nhiều Kế toán.',
     '1. Chọn Trạng thái = Đang tạo.',
     '—',
     '- ⚠️ Chỉ ra phiếu nháp do chính mình lập, kể cả khi có quyền xem tổng công ty.'),
    ('010', 'Lọc theo Người yêu cầu', 'P0',
     'Có phiếu lập từ yêu cầu của nhiều nhân viên.',
     '1. Chọn Người yêu cầu = một nhân viên cụ thể.',
     '—',
     '- ⚠️ Cột Người yêu cầu toàn bộ là nhân viên đã chọn.\n'
     '- Cột Người tạo có thể là nhiều Kế toán khác nhau.'),
    ('011', 'Lọc theo Người tạo', 'P1',
     'Có phiếu do nhiều Kế toán lập.',
     '1. Chọn Người tạo = một Kế toán cụ thể.',
     '—',
     '- Cột Người tạo toàn bộ là Kế toán đã chọn.'),
    ('012', 'Phân biệt rõ ô lọc Người yêu cầu với ô lọc Người tạo', 'P0',
     'Kế toán K đã lập 20 phiếu cho yêu cầu của nhân viên A.',
     '1. Lọc Người yêu cầu = A, ghi lại N.\n2. Làm mới, lọc Người tạo = A, ghi lại N.',
     '—',
     '- Bước 1: ra 20 phiếu.\n'
     '- ⚠️ Bước 2: ra 0 phiếu (A chưa lập phiếu xuất giữ nào).'),
    ('013', 'Lọc theo Người duyệt', 'P1',
     'Có phiếu đã duyệt.',
     '1. Chọn Người duyệt = một Kế toán cụ thể.',
     '—',
     '- Chỉ ra phiếu Đã duyệt do người đó bấm duyệt.'),
    ('014', 'Lọc theo Khách hàng', 'P1',
     'Có phiếu của nhiều khách hàng.',
     '1. Chọn Khách hàng = một khách cụ thể.',
     '—',
     '- Bật cột Khách hàng ở Cấu hình cột để đối chiếu: mọi dòng đúng khách đã chọn.'),
    ('015', 'Lọc theo Tên, mã hàng chỉ xét dòng có tích Cần xuất', 'P0',
     'Phiếu X có hàng HH01 tích Cần xuất, phiếu Y có HH01 nhưng Kế toán đã BỎ tích.',
     '1. Gõ HH01 vào ô Tên, mã hàng.',
     'HH01',
     '- ⚠️ Chỉ phiếu X ra; phiếu Y KHÔNG ra.'),
    ('016', 'Lọc khoảng Ngày tạo lấy trọn hai đầu mút', 'P0',
     'Có phiếu lập đúng ngày 01/08/2026 và 31/08/2026.',
     '1. Ngày tạo từ = 01/08/2026, Ngày tạo đến = 31/08/2026.',
     '01/08/2026 – 31/08/2026',
     '- ⚠️ Cả phiếu ngày 01/08 lẫn ngày 31/08 đều nằm trong kết quả.'),
    ('017', 'Lọc Ngày tạo theo ngày lập PHIẾU, không phải ngày lập YÊU CẦU', 'P0',
     'Yêu cầu lập ngày 10/07/2026, phiếu xuất giữ lập ngày 05/09/2026.',
     '1. Lọc Ngày tạo từ 01/07/2026 đến 31/07/2026.',
     '—',
     '- ⚠️ Phiếu đó KHÔNG có trong kết quả.\n'
     '- Lọc lại khoảng tháng 9 thì mới ra.'),
    ('018', 'Kết hợp nhiều tiêu chí lọc', 'P0',
     'Đang ở màn danh sách.',
     '1. Chọn Trạng thái = Đã duyệt.\n2. Chọn Người yêu cầu.\n3. Nhập khoảng Ngày tạo.',
     '—',
     '- Mọi dòng thỏa ĐỒNG THỜI cả ba tiêu chí.\n- N cập nhật đúng sau mỗi lần đổi.'),
    ('019', 'Nút Làm mới xóa toàn bộ tiêu chí', 'P0',
     'Đang áp 3 tiêu chí lọc và đang sắp xếp theo Ngày tạo tăng dần.',
     '1. Bấm Làm mới.',
     '—',
     '- Mọi ô lọc và ô tìm nhanh về trống.\n- Bỏ luôn thứ tự sắp xếp.\n'
     '- Bảng về trang 1 với toàn bộ phiếu trong phạm vi quyền.'),
    ('020', 'Bộ lọc được ghi nhớ khi rời màn rồi quay lại', 'P1',
     'Đang lọc Trạng thái = Đã duyệt.',
     '1. Mở một phiếu rồi bấm Quay lại.',
     '—',
     '- Bộ lọc vẫn còn, bảng vẫn hiện đúng kết quả đã lọc.'),
    ('021', 'Ô lọc Công ty chỉ hiện với quyền xem tổng công ty', 'P1',
     'Ba tài khoản: C (tổng công ty), D (công ty), E (phòng ban).',
     '1. Lần lượt đăng nhập và mở bảng lọc nâng cao.',
     '—',
     '- C: có cả ô Công ty và Phòng ban.\n- D: chỉ có ô Phòng ban.\n'
     '- E: không có cả hai ô.'),
    ('022', 'Tìm nhanh không khớp gì', 'P1',
     'Đang ở màn danh sách.',
     '1. Gõ chuỗi vô nghĩa rồi bấm Tìm kiếm.',
     'zzzz9999',
     '- Bảng hiện "Không có dữ liệu phù hợp.".\n- N = 0.\n- Không có lỗi đỏ.'),
]

S3 = [
    ('001', 'Bốn cột sắp xếp được đúng như quy định', 'P0',
     'Đang ở màn danh sách.',
     '1. Soát biểu tượng mũi tên trên dòng tiêu đề bảng.',
     '—',
     '- Chỉ bốn cột có mũi tên: Mã phiếu, Ngày tạo, Ngày duyệt, Giữ đến ngày.\n'
     '- Các cột khác KHÔNG có mũi tên.'),
    ('002', 'Sắp xếp theo Ngày tạo tăng dần rồi giảm dần', 'P0',
     'Có hơn 10 phiếu.',
     '1. Bấm tiêu đề Ngày tạo lần 1.\n2. Bấm lần 2.',
     '—',
     '- Lần 1: cũ nhất lên đầu.\n- Lần 2: mới nhất lên đầu.\n- Mỗi lần đều về trang 1.'),
    ('003', 'Sắp xếp giữ nguyên bộ lọc đang áp', 'P0',
     'Đang lọc Trạng thái = Đã duyệt.',
     '1. Bấm tiêu đề Mã phiếu.',
     '—',
     '- Thứ tự đổi nhưng danh sách vẫn chỉ toàn phiếu Đã duyệt.'),
    ('004', 'STT chạy liên tục qua các trang', 'P0',
     'Có hơn 20 phiếu, đang để 10 dòng/trang.',
     '1. Xem STT ở trang 1.\n2. Sang trang 2 và xem STT.',
     '—',
     '- Trang 1: 1–10.\n- Trang 2: 11–20.\n- ⚠️ KHÔNG reset về 1 ở mỗi trang.'),
    ('005', 'Lật trang không lặp và không mất bản ghi', 'P0',
     'Có nhiều phiếu lập cùng một thời điểm.',
     '1. Ghi lại mã phiếu ở trang 1, 2, 3.',
     '—',
     '- ⚠️ Không mã nào xuất hiện ở hai trang.\n- Không mã nào bị nhảy mất.'),
    ('006', 'Ô "Hiển thị a–b / N" đúng ở trang cuối', 'P1',
     'Có 26 phiếu, để 10 dòng/trang.',
     '1. Chuyển tới trang 3.',
     '—',
     '- Ô ghi "Hiển thị 21–26 / 26".\n- Bảng có 6 dòng.'),
    ('007', 'Đổi số dòng mỗi trang giữ nguyên bộ lọc', 'P1',
     'Đang lọc Trạng thái = Đã duyệt, có hơn 20 kết quả.',
     '1. Đổi Số dòng/trang từ 10 sang 20.',
     '—',
     '- Bảng hiện 20 dòng, vẫn chỉ toàn phiếu Đã duyệt.\n- Quay về trang 1.'),
    ('008', 'Cấu hình cột: bật cột ẩn lên', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm Cấu hình cột hiển thị.\n2. Tích cột Khách hàng và Giữ đến ngày.\n3. Bấm Lưu.',
     '—',
     '- Bảng có thêm hai cột đúng vị trí đã chọn, dữ liệu hiển thị đúng.'),
    ('009', 'Cấu hình cột: ba cột bị khóa không bỏ tích được', 'P0',
     'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Thử bỏ tích STT, Mã phiếu, Hành động.',
     '—',
     '- Ba cột này có biểu tượng ổ khóa, không bỏ tích và không kéo được.'),
    ('010', 'Cấu hình cột: kéo đổi thứ tự cột', 'P1',
     'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Kéo cột Trạng thái lên ngay sau Mã phiếu.\n2. Bấm Lưu.',
     '—',
     '- Bảng vẽ lại đúng thứ tự mới.'),
    ('011', 'Cấu hình cột: bấm Đóng thì bỏ thay đổi chưa lưu', 'P1',
     'Cửa sổ Tuỳ chỉnh cột đang mở.',
     '1. Bỏ tích cột Phòng yêu cầu.\n2. Bấm Đóng.\n3. Mở lại cửa sổ.',
     '—',
     '- Cột Phòng yêu cầu vẫn hiển thị trong bảng và vẫn được tích.'),
    ('012', 'Cấu hình cột lưu riêng theo từng người dùng', 'P1',
     'Người A đã tắt 3 cột và lưu.',
     '1. Đăng xuất, đăng nhập bằng người B.\n2. Vào màn hình.',
     '—',
     '- Người B thấy cấu hình cột mặc định.'),
    ('013', 'Cài đặt bộ lọc: tắt bớt ô lọc', 'P1',
     'Đang ở màn danh sách.',
     '1. Bấm Cài đặt bộ lọc.\n2. Bỏ tích ô Khách hàng.\n3. Bấm Lưu.',
     '—',
     '- Bảng lọc nâng cao không còn ô đó.\n- Các ô còn lại giữ nguyên thứ tự.'),
    ('014', 'Cài đặt bộ lọc: Khôi phục mặc định', 'P1',
     'Đã tắt vài ô lọc và lưu.',
     '1. Bấm Cài đặt bộ lọc.\n2. Bấm Khôi phục mặc định.\n3. Bấm Lưu.',
     '—',
     '- Bảng lọc quay về đủ 11 ô theo thứ tự ban đầu.'),
    ('015', 'Cài đặt bộ lọc: đủ 11 ô lọc', 'P2',
     'Cửa sổ Cài đặt bộ lọc đang mở.',
     '1. Đếm số mục trong cửa sổ.',
     '—',
     '- Đủ 11 mục: Công ty – Phòng ban, Mã phiếu, Yêu cầu xuất giữ, Trạng thái, Người tạo, '
     'Người duyệt, Người yêu cầu, Khách hàng, Tên mã hàng, Ngày tạo từ, Ngày tạo đến.'),
]

S4 = [
    ('001', 'Vào màn lập phiếu từ yêu cầu Chờ KT duyệt', 'P0',
     'Kế toán đủ quyền; có yêu cầu PYCXG ở trạng thái "Chờ KT duyệt" cùng công ty.',
     '1. Mở màn Yêu cầu xuất giữ, lọc Trạng thái = Chờ KT duyệt.\n'
     '2. Mở một yêu cầu, bấm nút "Lập phiếu xuất giữ".',
     '—',
     '- Chuyển sang màn "Lập phiếu xuất giữ".\n'
     '- Ô Yêu cầu xuất giữ điền sẵn mã yêu cầu, là liên kết, khóa lại.'),
    ('002', 'Dữ liệu nạp sẵn đầy đủ từ yêu cầu nguồn', 'P0',
     'Vừa mở màn lập phiếu từ một yêu cầu loại "Xuất giữ HĐ hãng".',
     '1. Soát toàn bộ khối Thông tin chung.',
     '—',
     '- Loại yêu cầu, Hợp đồng, Người yêu cầu, Phòng yêu cầu, Khách hàng, Địa chỉ, Ghi chú đều '
     'điền sẵn theo yêu cầu.\n'
     '- Ô Giữ đến ngày điền sẵn hạn giữ của yêu cầu.\n'
     '- Tất cả đều khóa, trừ Giữ đến ngày và Ghi chú.'),
    ('003', 'Bảng chi tiết chỉ nạp dòng ĐÃ TÍCH Cần xuất ở yêu cầu', 'P0',
     'Yêu cầu nguồn có 5 dòng hàng nhưng người lập chỉ tích 2 dòng.',
     '1. Soát bảng Chi tiết ở màn lập phiếu.',
     '—',
     '- ⚠️ Bảng chỉ có 2 dòng.\n'
     '- Ba dòng không tích ở yêu cầu KHÔNG xuất hiện.'),
    ('004', 'Ô Hợp đồng ẩn với yêu cầu loại Xuất giữ khác', 'P1',
     'Yêu cầu nguồn thuộc loại "Xuất giữ khác" (không gắn hợp đồng).',
     '1. Soát khối Thông tin chung.',
     '—',
     '- ⚠️ KHÔNG có ô Hợp đồng.\n'
     '- Không có ô xám rỗng nào gây hiểu nhầm là thiếu dữ liệu.'),
    ('005', 'Ô Địa chỉ ẩn khi khách hàng chưa khai địa chỉ', 'P1',
     'Yêu cầu nguồn có khách hàng chưa khai địa chỉ.',
     '1. Soát khối Thông tin chung.',
     '—',
     '- ⚠️ Ô Địa chỉ ẩn hẳn, không hiện ô xám trống.'),
    ('006', 'Cột SL xuất giữ điền sẵn bằng SL yêu cầu', 'P0',
     'Yêu cầu nguồn có dòng xin giữ 4.',
     '1. Soát bảng Chi tiết.',
     '—',
     '- Cột SL yêu cầu = 4.\n- Cột SL xuất giữ điền sẵn = 4.\n'
     '- Ô tích Cần xuất đã tích sẵn.'),
    ('007', 'Bỏ tích Cần xuất thì khóa ô số lượng và làm mờ dòng', 'P0',
     'Bảng có 2 dòng đều tích sẵn.',
     '1. Bỏ tích ở dòng 1.',
     '—',
     '- Dòng 1 bị làm mờ.\n- Ô SL xuất giữ của dòng 1 khóa lại, không nhập được.'),
    ('008', 'Không thêm và không xóa dòng được', 'P0',
     'Đang ở màn lập phiếu.',
     '1. Soát khối Chi tiết.',
     '—',
     '- ⚠️ KHÔNG có nút Thêm hàng hóa.\n- KHÔNG có nút xóa dòng.\n'
     '- Ô ĐVT chỉ hiển thị, không chọn được.'),
    ('009', 'Lưu nháp thành công', 'P0',
     'Dữ liệu hợp lệ, có ít nhất 1 dòng tích với số lượng > 0.',
     '1. Bấm Lưu nháp.',
     '—',
     '- Thông báo lưu thành công, quay về màn danh sách.\n'
     '- Phiếu mới có mã dạng PXG-NNNNN, trạng thái "Đang tạo".\n'
     '- ⚠️ Yêu cầu nguồn chuyển sang "Đang xuất giữ".'),
    ('010', 'Nút Không duyệt lưu y hệt nút Lưu nháp', 'P0',
     'Dữ liệu hợp lệ ở màn lập phiếu.',
     '1. Bấm nút "Không duyệt".\n2. Kiểm tra trạng thái phiếu và yêu cầu nguồn.',
     '—',
     '- ⚠️ Phiếu được lưu ở trạng thái "Đang tạo" — GIỐNG HỆT Lưu nháp.\n'
     '- ⚠️ Yêu cầu nguồn sang "Đang xuất giữ", KHÔNG bị trả về cho người lập.\n'
     '- Đây là bẫy dễ hiểu nhầm nhất của màn hình.'),
    ('011', 'Duyệt giữ hàng có hộp thoại xác nhận riêng', 'P0',
     'Dữ liệu hợp lệ ở màn lập phiếu.',
     '1. Bấm nút "Duyệt giữ hàng".',
     '—',
     '- Mở hộp thoại "Xác nhận duyệt giữ hàng".\n'
     '- Nội dung nêu rõ sẽ GHI TỒN HÀNG GIỮ và không hoàn tác được.\n'
     '- Nút xác nhận ghi "Duyệt giữ hàng".'),
    ('012', 'Hủy ở hộp thoại xác nhận thì không ghi gì', 'P0',
     'Hộp thoại xác nhận duyệt đang mở.',
     '1. Bấm Hủy.',
     '—',
     '- Hộp thoại đóng, vẫn ở màn lập phiếu.\n- Không có phiếu nào được tạo.'),
    ('013', 'Duyệt giữ hàng thành công', 'P0',
     'Dữ liệu hợp lệ, tồn kho đủ.',
     '1. Bấm Duyệt giữ hàng và xác nhận.',
     '—',
     '- Thông báo thành công, quay về màn danh sách.\n'
     '- Phiếu ở trạng thái "Đã duyệt", cột Người duyệt và Ngày duyệt được điền.\n'
     '- ⚠️ Yêu cầu nguồn chuyển sang "Đã duyệt".'),
    ('014', 'Lưu nháp KHÔNG kiểm tra tồn kho', 'P0',
     'Hàng HH01 chỉ còn 2 trong kho; SL xuất giữ để = 4 (bằng SL yêu cầu).',
     '1. Bấm Lưu nháp.',
     '—',
     '- ⚠️ Lưu THÀNH CÔNG, không báo thiếu hàng.\n- Phiếu ở trạng thái Đang tạo.'),
    ('015', 'Duyệt giữ hàng CÓ kiểm tra tồn kho', 'P0',
     'Tiếp nối TC 014: phiếu nháp có SL xuất giữ = 4 mà kho chỉ còn 2.',
     '1. Mở phiếu ra Sửa.\n2. Bấm Duyệt giữ hàng và xác nhận.',
     '—',
     '- ⚠️ Bị chặn, báo đỏ tại dòng: "Kho không đủ số lượng (còn 2)."\n'
     '- Phiếu vẫn ở "Đang tạo", tồn hàng giữ không đổi.\n'
     '- Giá trị 4 vẫn nguyên trong ô, phần mềm KHÔNG tự kéo về 2.'),
    ('016', 'Sửa hạn giữ trước khi duyệt', 'P0',
     'Yêu cầu nguồn có hạn giữ 30/09/2026.',
     '1. Đổi ô Giữ đến ngày thành 15/10/2026.\n2. Bấm Duyệt giữ hàng và xác nhận.\n'
     '3. Kiểm tra lô hàng giữ sinh ra.',
     '15/10/2026',
     '- ⚠️ Lô hàng giữ có hạn 15/10/2026 — theo phiếu xuất giữ, không theo yêu cầu.'),
    ('017', 'Mã phiếu sinh đúng định dạng và không trùng', 'P0',
     'Lập liên tiếp 2 phiếu từ 2 yêu cầu khác nhau.',
     '1. Lưu nháp lần lượt 2 phiếu.\n2. Soát mã.',
     '—',
     '- Mã dạng PXG- kèm 5 chữ số, khác nhau và tăng dần.\n'
     '- ⚠️ Không mã nào là chuỗi ngẫu nhiên vô nghĩa.'),
    ('018', 'Đính kèm tệp ở phiếu xuất giữ', 'P1',
     'Đang ở màn lập phiếu.',
     '1. Bấm Chọn tệp, tải lên 1 tệp PDF.',
     'tệp PDF < 13 MB',
     '- Tệp hiện trong danh sách, có nút gỡ.\n'
     '- ⚠️ Tệp đính kèm KHÔNG bắt buộc ở màn này.'),
    ('019', 'Rời màn khi chưa lưu thì hỏi xác nhận', 'P1',
     'Đã đổi số lượng ở màn lập phiếu, chưa lưu.',
     '1. Bấm Quay lại.',
     '—',
     '- Hệ thống hỏi xác nhận rời trang.'),
    ('020', 'Yêu cầu đã có phiếu xuất giữ thì chặn lập thêm', 'P0',
     'Yêu cầu đã có phiếu PXG-XXXXX.',
     '1. Tester kỹ thuật gọi thẳng chức năng lập phiếu cho yêu cầu đó.',
     '—',
     '- Bị chặn, báo "Yêu cầu này đã có phiếu xuất giữ PXG-XXXXX."\n'
     '- Không sinh ra phiếu thứ hai.'),
    ('021', 'Không vào được màn lập phiếu nếu thiếu yêu cầu nguồn', 'P0',
     'Tester kỹ thuật mở màn lập phiếu bằng đường dẫn trực tiếp mà không kèm yêu cầu nguồn.',
     '1. Mở /finance/warehouse-prepick-requests/create không kèm tham số.',
     '—',
     '- Màn hình không nạp được dữ liệu, hoặc báo lỗi rõ ràng.\n'
     '- ⚠️ Không tạo ra phiếu mồ côi không có yêu cầu nguồn.'),
    ('022', 'Dòng Tổng cộng cộng đúng', 'P1',
     'Bảng có 3 dòng với SL yêu cầu 2, 3, 5 và SL xuất giữ 2, 3, 4.',
     '1. Soát dòng Tổng cộng cuối bảng.',
     '—',
     '- Cột SL yêu cầu tổng = 10.\n- Cột SL xuất giữ tổng = 9.'),
]

S5 = [
    ('001', 'Nút Sửa chỉ hiện với phiếu nháp của mình', 'P0',
     'Danh sách có phiếu nháp của mình, phiếu đã duyệt của mình và phiếu của người khác.',
     '1. Soát cột Hành động của từng dòng.',
     '—',
     '- Chỉ phiếu "Đang tạo" do chính mình lập mới có biểu tượng bút chì.\n'
     '- ⚠️ Nút ẩn hẳn, không ở trạng thái mờ.'),
    ('002', 'Mở màn Sửa từ danh sách', 'P0',
     'Có phiếu nháp của mình.',
     '1. Bấm biểu tượng bút chì.',
     '—',
     '- Chuyển sang màn "Sửa phiếu xuất giữ: <mã phiếu>".\n'
     '- Dữ liệu đã lưu nạp đầy đủ.'),
    ('003', 'Yêu cầu nguồn khóa cứng ở màn Sửa', 'P0',
     'Đang ở màn Sửa.',
     '1. Thử đổi ô Yêu cầu xuất giữ.',
     '—',
     '- Ô khóa, chỉ là liên kết mở tab mới.\n'
     '- Có biểu tượng ⓘ giải thích vì sao không đổi được.'),
    ('004', 'Sửa số lượng rồi lưu nháp', 'P0',
     'Phiếu nháp có dòng SL xuất giữ = 4.',
     '1. Đổi thành 2.\n2. Bấm Lưu nháp.\n3. Mở lại phiếu.',
     '2',
     '- Số lượng đã đổi thành 2.\n- Trạng thái vẫn "Đang tạo".'),
    ('005', 'Sửa hạn giữ rồi lưu nháp', 'P1',
     'Phiếu nháp có Giữ đến ngày 30/09/2026.',
     '1. Đổi thành 20/10/2026.\n2. Lưu nháp rồi mở lại.',
     '20/10/2026',
     '- Hạn giữ mới được lưu.'),
    ('006', 'Duyệt giữ hàng ngay tại màn Sửa', 'P0',
     'Phiếu nháp của mình, tồn kho đủ.',
     '1. Mở màn Sửa, bấm Duyệt giữ hàng và xác nhận.',
     '—',
     '- ⚠️ Duyệt được ngay tại màn Sửa, không cần thao tác nào khác.\n'
     '- Phiếu sang "Đã duyệt", yêu cầu nguồn cũng sang "Đã duyệt".'),
    ('007', 'Không sửa được phiếu đã duyệt', 'P0',
     'Phiếu của mình đã ở trạng thái "Đã duyệt".',
     '1. Soát cột Hành động — không thấy nút Sửa.\n'
     '2. Mở màn Sửa bằng đường dẫn trực tiếp.',
     '—',
     '- Bước 1: không có nút Sửa.\n'
     '- Bước 2: hệ thống từ chối, không mở màn sửa.\n'
     '- ⚠️ Lô hàng giữ đã ghi nên không cho sửa lại.'),
    ('008', 'Không sửa được phiếu nháp của người khác', 'P0',
     'Kế toán K1 có phiếu nháp. Kế toán K2 biết mã phiếu đó.',
     '1. K2 mở màn Sửa phiếu đó bằng đường dẫn trực tiếp.',
     '—',
     '- Hệ thống từ chối, báo không có quyền xem phiếu này.\n'
     '- ⚠️ Màn hình không nạp được dữ liệu phiếu.'),
    ('009', 'Không đổi được danh sách hàng hóa ở màn Sửa', 'P0',
     'Đang ở màn Sửa.',
     '1. Soát khối Chi tiết.',
     '—',
     '- Không có nút Thêm hàng hóa, không có nút xóa dòng.\n'
     '- Chỉ đổi được ô tích Cần xuất và SL xuất giữ.'),
    ('010', 'Bộ nút ở màn Sửa giống màn Lập phiếu', 'P1',
     'Đang ở màn Sửa.',
     '1. Soát bộ nút ở cuối màn.',
     '—',
     '- Có đủ: Lưu nháp, Duyệt giữ hàng, Không duyệt, Quay lại.'),
    ('011', 'Số Có thể giữ được nạp lại mới nhất khi mở màn Sửa', 'P1',
     'Phiếu nháp lập hôm qua với SL có thể giữ = 100. Hôm nay kho đã xuất bớt còn 40.',
     '1. Mở phiếu ra Sửa và đọc cột SL có thể giữ.',
     '—',
     '- ⚠️ Cột hiện 40, là số tồn kho mới nhất, không phải số lúc lập phiếu.'),
]

S6 = [
    ('001', 'Mở màn chi tiết bằng cách bấm mã phiếu', 'P0',
     'Có phiếu trong danh sách.',
     '1. Bấm mã phiếu.',
     '—',
     '- Tiêu đề màn ghi "Chi tiết phiếu xuất giữ: <mã phiếu>".\n'
     '- Toàn bộ ô ở chế độ chỉ đọc.'),
    ('002', 'Màn chi tiết có đủ các khối', 'P0',
     'Đang xem chi tiết một phiếu đã duyệt.',
     '1. Cuộn hết màn hình.',
     '—',
     '- Có các khối: Thông tin chung, File đính kèm, Chi tiết, Lịch sử thay đổi (thu gọn).'),
    ('003', 'Phiếu đã duyệt có thêm cột SL giữ (ĐV cơ bản)', 'P0',
     'Phiếu đã duyệt, dòng hàng có đơn vị "Xô 18L" hệ số 1.',
     '1. Soát dòng tiêu đề bảng Chi tiết.',
     '—',
     '- ⚠️ Có cột "SL giữ (ĐV cơ bản)" ở cuối bảng.\n'
     '- Dưới bảng có dòng chú thích nhắc đối chiếu Lịch sử giữ hàng theo cột này.'),
    ('004', 'Phiếu còn nháp KHÔNG có cột SL giữ (ĐV cơ bản)', 'P1',
     'Phiếu đang ở trạng thái "Đang tạo".',
     '1. Mở màn chi tiết và soát bảng.',
     '—',
     '- ⚠️ Không có cột đó, vì chưa ghi tồn hàng giữ.\n'
     '- Không có dòng chú thích ở dưới bảng.'),
    ('005', 'Cột SL giữ (ĐV cơ bản) tính đúng với đơn vị hệ số 1', 'P0',
     'Dòng hàng SL xuất giữ = 2, đơn vị tính hệ số 1.',
     '1. Mở chi tiết phiếu đã duyệt và đọc hai cột.',
     '—',
     '- SL xuất giữ = 2, SL giữ (ĐV cơ bản) = 2.'),
    ('006', 'Cột SL giữ (ĐV cơ bản) tính đúng với đơn vị hệ số lớn hơn 1', 'P0',
     'Dòng hàng SL xuất giữ = 3, đơn vị "Thùng" hệ số 10.',
     '1. Mở chi tiết phiếu đã duyệt và đọc hai cột.',
     '—',
     '- ⚠️ SL xuất giữ = 3 nhưng SL giữ (ĐV cơ bản) = 30.\n'
     '- Con số 30 mới là số cộng vào kho hàng giữ.'),
    ('007', 'Nút ở màn chi tiết KHỚP với cột Hành động ngoài danh sách', 'P0',
     'Chọn một phiếu nháp của mình và một phiếu đã duyệt.',
     '1. Với mỗi phiếu: ghi lại nút ở cột Hành động rồi mở chi tiết ghi lại nút cuối màn.',
     '—',
     '- ⚠️ Hai bộ nút khớp nhau, màn chi tiết chỉ có thêm nút Quay lại.'),
    ('008', 'Bấm mã yêu cầu ở màn chi tiết mở tab mới', 'P1',
     'Đang xem chi tiết một phiếu.',
     '1. Bấm vào mã ở ô Yêu cầu xuất giữ.',
     '—',
     '- Mở màn chi tiết yêu cầu trong tab mới.\n- Tab hiện tại không rời khỏi phiếu.'),
    ('009', 'Khối File đính kèm khi không có tệp', 'P1',
     'Phiếu không đính kèm tệp nào.',
     '1. Soát khối File đính kèm.',
     '—',
     '- Hiện dòng "Chưa có tệp đính kèm".\n- Không có nút Chọn tệp.'),
    ('010', 'Phiếu nháp của người khác không mở được chi tiết', 'P0',
     'Biết mã một phiếu nháp của Kế toán khác.',
     '1. Mở màn chi tiết bằng đường dẫn trực tiếp.',
     '—',
     '- Hệ thống báo không có quyền xem phiếu này.\n- Không hiện dữ liệu phiếu.'),
    ('011', 'Nút Quay lại về đúng màn danh sách', 'P2',
     'Đang xem chi tiết một phiếu, đến từ danh sách đang lọc.',
     '1. Bấm Quay lại.',
     '—',
     '- Về màn danh sách, bộ lọc trước đó vẫn còn.'),
]

S7 = [
    ('001', 'Ghi tồn hàng giữ cho đúng người yêu cầu', 'P0',
     'Yêu cầu do nhân viên A lập. Kế toán B lập và duyệt phiếu. Hàng HH01, SL xuất giữ 10, '
     'đơn vị hệ số 1.',
     '1. Duyệt giữ hàng.\n'
     '2. Mở màn Tài chính → Giữ hàng → Danh sách hàng giữ, lọc theo A.\n'
     '3. Lọc lại theo B.',
     '—',
     '- Bước 2: ⚠️ A có lô hàng giữ HH01 số lượng 10.\n'
     '- Bước 3: B KHÔNG có lô nào tăng thêm.'),
    ('002', 'Lô mới được tạo khi chưa có lô khớp', 'P0',
     'A chưa giữ HH01 cho khách K với hạn 30/10/2026.',
     '1. Duyệt phiếu xuất giữ 5 đơn vị HH01 cho khách K, hạn 30/10/2026.\n'
     '2. Kiểm tra danh sách hàng giữ của A.',
     '—',
     '- Có thêm MỘT lô mới: HH01 – khách K – hạn 30/10/2026 – số lượng 5.'),
    ('003', 'Cộng dồn vào lô đã có khi khớp đủ năm yếu tố', 'P0',
     'A đã giữ HH01 cho khách K, hạn 30/10/2026, số lượng 5.',
     '1. Duyệt thêm một phiếu xuất giữ 3 đơn vị HH01 cho khách K, hạn 30/10/2026.\n'
     '2. Kiểm tra danh sách hàng giữ của A.',
     '—',
     '- ⚠️ KHÔNG sinh lô thứ hai.\n- Lô cũ tăng từ 5 lên 8.'),
    ('004', 'Khác hạn giữ thì sinh lô riêng', 'P0',
     'A đã giữ HH01 cho khách K, hạn 30/10/2026.',
     '1. Duyệt phiếu xuất giữ HH01 cho khách K nhưng hạn 15/11/2026.\n'
     '2. Kiểm tra danh sách hàng giữ của A.',
     '—',
     '- ⚠️ Sinh lô MỚI vì hạn giữ khác.\n- A có 2 lô HH01 cho khách K với 2 hạn khác nhau.'),
    ('005', 'Khác khách hàng thì sinh lô riêng', 'P1',
     'A đã giữ HH01 cho khách K1.',
     '1. Duyệt phiếu xuất giữ HH01 cho khách K2, cùng hạn.\n2. Kiểm tra hàng giữ của A.',
     '—',
     '- Sinh lô mới, hai lô riêng cho hai khách.'),
    ('006', 'Quy đổi đúng theo hệ số đơn vị tính', 'P0',
     'Dòng hàng đơn vị "Thùng" hệ số 10, SL xuất giữ = 3.',
     '1. Duyệt giữ hàng.\n2. Kiểm tra lô hàng giữ sinh ra.',
     '—',
     '- ⚠️ Lô có số lượng 30 (đơn vị cơ bản), không phải 3.\n'
     '- Cột SL giữ (ĐV cơ bản) ở màn chi tiết cũng hiện 30.'),
    ('007', 'Nhật ký biến động của lô được ghi đúng', 'P0',
     'Lô HH01 của A đang có 5.',
     '1. Duyệt thêm phiếu xuất giữ 3 đơn vị.\n'
     '2. Mở lịch sử biến động của lô đó.',
     '—',
     '- Có dòng nhật ký mới ghi rõ: số trước 5, thay đổi +3, số sau 8.\n'
     '- Ghi rõ nguồn là phiếu xuất giữ nào.'),
    ('008', 'Công ty của lô lấy theo yêu cầu, không theo Kế toán', 'P0',
     'Yêu cầu thuộc công ty 1. Kế toán có quyền xem tổng công ty và thuộc công ty 4.',
     '1. Kế toán lập và duyệt phiếu.\n2. Kiểm tra lô hàng giữ sinh ra.',
     '—',
     '- ⚠️ Lô thuộc công ty 1, không phải công ty 4.'),
    ('009', 'Dòng không tích Cần xuất KHÔNG sinh lô', 'P0',
     'Phiếu có 2 dòng, Kế toán bỏ tích dòng 2.',
     '1. Duyệt giữ hàng.\n2. Kiểm tra lô hàng giữ.',
     '—',
     '- Chỉ sinh lô cho dòng 1.\n'
     '- ⚠️ Dòng 2 được lưu với số lượng 0 và không có lô nào.'),
    ('010', 'Tồn kho không đủ thì KHÔNG ghi gì cả', 'P0',
     'Phiếu có 3 dòng; dòng 1 và 2 đủ hàng, dòng 3 thiếu hàng.',
     '1. Bấm Duyệt giữ hàng và xác nhận.\n2. Kiểm tra lô hàng giữ và trạng thái phiếu.',
     '—',
     '- ⚠️ Báo lỗi tại dòng 3: "Kho không đủ số lượng (còn …)."\n'
     '- ⚠️ KHÔNG dòng nào được ghi tồn, kể cả dòng 1 và 2.\n'
     '- Phiếu vẫn ở "Đang tạo".'),
    ('011', 'Không tích dòng nào thì bị chặn khi duyệt', 'P0',
     'Bỏ tích hết các dòng.',
     '1. Bấm Duyệt giữ hàng.',
     '—',
     '- Báo "Chưa chọn hàng hoá nào cần xuất giữ, hoặc số lượng đều bằng 0."\n- Không lưu.'),
    ('012', 'Tồn kho giảm đúng sau khi duyệt', 'P0',
     'Hàng HH01 có SL có thể giữ = 100.',
     '1. Duyệt phiếu xuất giữ 10 đơn vị HH01.\n'
     '2. Mở một phiếu xuất giữ khác có HH01 và đọc cột SL có thể giữ.',
     '—',
     '- ⚠️ Cột SL có thể giữ giảm còn 90.'),
    ('013', 'Yêu cầu nguồn được đóng dấu duyệt', 'P0',
     'Yêu cầu đang ở "Chờ KT duyệt" hoặc "Đang xuất giữ".',
     '1. Duyệt giữ hàng.\n2. Mở màn Yêu cầu xuất giữ và tìm yêu cầu đó.',
     '—',
     '- Yêu cầu ở "Đã duyệt".\n'
     '- Cột Người duyệt là Kế toán vừa bấm duyệt, Ngày duyệt là thời điểm duyệt.'),
    ('014', 'Lịch sử của yêu cầu ghi rõ mã phiếu xuất giữ', 'P0',
     'Vừa duyệt phiếu PXG-XXXXX.',
     '1. Mở lịch sử của yêu cầu nguồn.',
     '—',
     '- ⚠️ Mốc cuối ghi rõ "Duyệt qua phiếu xuất giữ PXG-XXXXX".'),
    ('015', 'Lịch sử của phiếu ghi rõ số lô đã ghi tồn', 'P1',
     'Vừa duyệt một phiếu có 2 dòng cần xuất.',
     '1. Mở lịch sử của phiếu.',
     '—',
     '- Mốc "Duyệt giữ hàng" ghi rõ đã ghi tồn giữ cho 2 lô hàng.'),
    ('016', 'Duyệt phiếu đã được người khác duyệt trước', 'P0',
     'Hai người cùng mở một phiếu nháp (người thứ hai là quản trị hệ thống).',
     '1. Người 1 duyệt xong.\n2. Người 2 bấm Duyệt giữ hàng trên màn cũ.',
     '—',
     '- ⚠️ Người 2 bị chặn; hàng KHÔNG bị cộng hai lần.'),
    ('017', 'Hạn giữ trên lô lấy theo phiếu, không theo yêu cầu', 'P0',
     'Yêu cầu có hạn 30/09/2026; Kế toán đổi trên phiếu thành 15/10/2026 trước khi duyệt.',
     '1. Duyệt giữ hàng.\n2. Kiểm tra hạn giữ của lô sinh ra.',
     '—',
     '- ⚠️ Lô có hạn 15/10/2026.'),
    ('018', 'Bỏ trống Giữ đến ngày khi duyệt thì bị chặn', 'P0',
     'Đang ở màn lập hoặc sửa phiếu.',
     '1. Xóa trắng ô Giữ đến ngày rồi bấm Duyệt giữ hàng.',
     '—',
     '- Báo "Giữ đến ngày – Bắt buộc phải nhập."\n- Không ghi tồn.'),
    ('019', 'Nhập Giữ đến ngày là ngày quá khứ khi duyệt', 'P0',
     'Đang ở màn lập phiếu.',
     '1. Nhập Giữ đến ngày là ngày hôm qua rồi bấm Duyệt giữ hàng.',
     'ngày hôm qua',
     '- Báo "Giữ đến ngày – Phải nhập ngày tương lai."\n- Không ghi tồn.'),
]

S8 = [
    ('001', 'Nút Xóa chỉ hiện với phiếu nháp của mình', 'P0',
     'Danh sách có phiếu nháp của mình và phiếu đã duyệt.',
     '1. Soát cột Hành động.',
     '—',
     '- Chỉ phiếu "Đang tạo" của chính mình có biểu tượng thùng rác.'),
    ('002', 'Hộp thoại xác nhận xóa ở màn danh sách', 'P0',
     'Có phiếu nháp của mình.',
     '1. Bấm biểu tượng thùng rác.',
     '—',
     '- Hộp thoại tiêu đề "Xác nhận xóa".\n'
     '- Nội dung "Bạn có chắc muốn xóa phiếu <mã phiếu>?".\n'
     '- Nút Xóa màu đỏ và nút Hủy.'),
    ('003', 'Hộp thoại xác nhận xóa ở màn chi tiết nói rõ hệ quả', 'P0',
     'Đang xem chi tiết một phiếu nháp của mình.',
     '1. Bấm nút Xóa ở cuối màn.',
     '—',
     '- ⚠️ Nội dung ghi "Xóa phiếu <mã phiếu>? Yêu cầu xuất giữ sẽ quay lại bước Kế toán xử lý."'),
    ('004', 'Bấm Hủy thì không xóa gì', 'P0',
     'Hộp thoại xác nhận xóa đang mở.',
     '1. Bấm Hủy.',
     '—',
     '- Hộp thoại đóng, phiếu vẫn còn.'),
    ('005', 'Xóa phiếu nháp thành công', 'P0',
     'Có phiếu nháp của mình, yêu cầu nguồn đang ở "Đang xuất giữ".',
     '1. Xóa phiếu.\n2. Mở màn Yêu cầu xuất giữ và tìm yêu cầu đó.',
     '—',
     '- Thông báo "Xóa thành công.", phiếu biến mất khỏi danh sách.\n'
     '- ⚠️ Yêu cầu nguồn quay về "Chờ KT duyệt".\n'
     '- Nút "Lập phiếu xuất giữ" hiện lại ở yêu cầu.'),
    ('006', 'Xóa phiếu nháp không đụng tới hàng giữ', 'P0',
     'Ghi lại tồn hàng giữ của người yêu cầu trước khi xóa.',
     '1. Xóa phiếu nháp.\n2. Đối chiếu tồn hàng giữ.',
     '—',
     '- ⚠️ Tồn hàng giữ không đổi, vì phiếu nháp chưa từng ghi tồn.'),
    ('007', 'Không xóa được phiếu đã duyệt', 'P0',
     'Phiếu của mình đã ở "Đã duyệt".',
     '1. Soát cột Hành động — không có nút Xóa.\n'
     '2. Tester kỹ thuật gọi thẳng chức năng xóa phiếu đó.',
     '—',
     '- Bước 1: không có nút.\n'
     '- Bước 2: bị chặn, báo "Không thể xóa phiếu này."\n'
     '- ⚠️ Lô hàng giữ đã sinh ra không bị ảnh hưởng.'),
    ('008', 'Không xóa được phiếu nháp của người khác', 'P0',
     'Biết mã phiếu nháp của Kế toán khác.',
     '1. Tester kỹ thuật gọi thẳng chức năng xóa phiếu đó.',
     '—',
     '- Bị chặn, báo "Không thể xóa phiếu này."'),
    ('009', 'Lịch sử thay đổi được giữ lại sau khi xóa', 'P1',
     'Phiếu nháp đã có vài mốc lịch sử.',
     '1. Xóa phiếu.\n2. Tra cứu lịch sử của phiếu đó qua công cụ quản trị.',
     '—',
     '- ⚠️ Các mốc lịch sử vẫn còn; chỉ phiếu và dòng hàng bị xóa.'),
    ('010', 'Xóa phiếu rồi lập lại phiếu mới cho cùng yêu cầu', 'P0',
     'Vừa xóa phiếu nháp, yêu cầu đã quay về "Chờ KT duyệt".',
     '1. Mở yêu cầu, bấm Lập phiếu xuất giữ, lưu nháp.',
     '—',
     '- Lập được phiếu mới với mã mới.\n'
     '- ⚠️ Không còn bị chặn vì "đã có phiếu xuất giữ".'),
]

S9 = [
    ('001', 'In một phiếu từ cột Hành động', 'P0',
     'Có phiếu trong danh sách.',
     '1. Bấm biểu tượng máy in ở một dòng.',
     '—',
     '- Mở cửa sổ "Xem trước phiếu xuất giữ" ngay trên màn đang đứng.\n'
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
     '- Khối thông tin phiếu: yêu cầu xuất giữ, loại yêu cầu, hợp đồng, người yêu cầu, '
     'phòng yêu cầu, khách hàng, địa chỉ, giữ đến ngày, trạng thái.\n'
     '- Bảng hàng hóa kèm dòng Tổng cộng.\n'
     '- Bảng Thông tin duyệt.\n- Khối ký tên Người lập và Kế toán duyệt.'),
    ('004', 'Phần đầu bản in lấy theo công ty của PHIẾU', 'P0',
     'Phiếu thuộc công ty 1. Người in thuộc công ty 4 và có quyền xem tổng công ty.',
     '1. In phiếu đó.',
     '—',
     '- ⚠️ Phần đầu bản in là thông tin công ty 1, không phải công ty 4.'),
    ('005', 'Phiếu chưa duyệt thì bảng Thông tin duyệt để TRỐNG', 'P0',
     'Phiếu đang ở "Đang tạo".',
     '1. In phiếu đó và soát bảng Thông tin duyệt.',
     '—',
     '- ⚠️ Ô người duyệt và thời gian duyệt để TRỐNG.\n'
     '- KHÔNG in ngày hôm nay vào chỗ đó.'),
    ('006', 'In danh sách theo bộ lọc đang áp', 'P0',
     'Đang lọc Trạng thái = Đã duyệt, có 30 kết quả, đang ở trang 1 (10 dòng).',
     '1. Bấm nút In ở thanh công cụ.',
     '—',
     '- Mở cửa sổ xem trước bản in danh sách, khổ A4 NGANG.\n'
     '- ⚠️ In đủ 30 dòng, không chỉ 10 dòng của trang đang xem.'),
    ('007', 'In danh sách không vượt quá phạm vi quyền', 'P0',
     'Tài khoản chỉ xem được phiếu của mình.',
     '1. Bỏ hết bộ lọc rồi bấm In ở thanh công cụ.',
     '—',
     '- ⚠️ Bản in chỉ có phiếu của chính mình.'),
    ('008', 'Xuất Excel mở cửa sổ chọn trường trước', 'P0',
     'Đang ở màn danh sách.',
     '1. Bấm nút Xuất Excel.',
     '—',
     '- ⚠️ KHÔNG tải tệp ngay.\n'
     '- Mở cửa sổ "Chọn trường xuất Excel" với 14 trường, mặc định chọn hết.'),
    ('009', 'Cửa sổ chọn trường có đủ 14 trường đúng tên', 'P1',
     'Cửa sổ Chọn trường xuất Excel đang mở.',
     '1. Đếm và đọc tên các trường.',
     '—',
     '- Đủ 14: Mã phiếu, Yêu cầu xuất giữ, Người yêu cầu, Phòng yêu cầu, Người tạo, Ngày tạo, '
     'Khách hàng, Giữ đến ngày, Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, '
     'Ngày cập nhật, Ghi chú.\n'
     '- Có dòng ghi "Đang chọn 14/14 trường".'),
    ('010', 'Bỏ chọn trường thì tệp không có cột đó', 'P0',
     'Cửa sổ Chọn trường đang mở.',
     '1. Bỏ chọn Ghi chú và Người cập nhật.\n2. Bấm Xuất file.\n3. Mở tệp tải về.',
     '—',
     '- Tệp có 12 cột, không có hai cột đã bỏ.'),
    ('011', 'Thứ tự cột trong tệp theo đúng thứ tự chọn', 'P1',
     'Cửa sổ Chọn trường đang mở.',
     '1. Bấm Bỏ chọn hết.\n2. Chọn lần lượt: Trạng thái, Mã phiếu, Người yêu cầu.\n'
     '3. Bấm Xuất file và mở tệp.',
     '—',
     '- Dòng xem trước ghi đúng thứ tự đó.\n- Tệp có 3 cột đúng thứ tự.'),
    ('012', 'Tệp Excel xuất đủ dòng theo bộ lọc', 'P0',
     'Đang lọc ra 45 kết quả, để 10 dòng/trang.',
     '1. Xuất Excel với toàn bộ trường.\n2. Đếm số dòng dữ liệu trong tệp.',
     '—',
     '- ⚠️ Tệp có đủ 45 dòng dữ liệu.'),
    ('013', 'Mã phiếu trong tệp không bị Excel hiểu thành số', 'P1',
     'Đã xuất tệp Excel.',
     '1. Mở tệp và soát cột Mã phiếu và cột Yêu cầu xuất giữ.',
     '—',
     '- Mã hiển thị nguyên vẹn dạng PXG-02190 và PYCXG-02219.'),
    ('014', 'Ngày trong tệp giữ định dạng dd/mm/yyyy', 'P1',
     'Đã xuất tệp Excel.',
     '1. Soát các cột ngày.',
     '—',
     '- Ngày hiển thị dạng dd/mm/yyyy, không bị đổi theo định dạng máy.'),
    ('015', 'Nút Xuất file bị khóa trong lúc đang xuất', 'P2',
     'Đang xuất một tệp lớn.',
     '1. Bấm Xuất file rồi bấm lại ngay.',
     '—',
     '- Nút bị khóa trong lúc xử lý; chỉ tải về một tệp.'),
    ('016', 'Tệp Excel không vượt quá phạm vi quyền', 'P0',
     'Tài khoản chỉ xem được phiếu của mình.',
     '1. Bỏ hết bộ lọc rồi xuất Excel.',
     '—',
     '- ⚠️ Tệp chỉ có phiếu của chính mình.'),
]

S10 = [
    ('001', 'SL xuất giữ vượt SL yêu cầu', 'P0',
     'Dòng hàng có SL yêu cầu = 4.',
     '1. Nhập 6 vào ô SL xuất giữ rồi bấm Lưu nháp.',
     '6',
     '- ⚠️ Bị chặn, báo đỏ tại dòng: "Vượt số lượng đề nghị của yêu cầu (4)."\n'
     '- Giá trị 6 vẫn nguyên trong ô, phần mềm KHÔNG tự kéo về 4.'),
    ('002', 'SL xuất giữ bằng đúng SL yêu cầu', 'P1',
     'Dòng hàng có SL yêu cầu = 4.',
     '1. Để nguyên 4 rồi Lưu nháp.',
     '4',
     '- Lưu thành công, không báo lỗi.'),
    ('003', 'SL xuất giữ nhỏ hơn SL yêu cầu', 'P0',
     'Dòng hàng có SL yêu cầu = 4.',
     '1. Nhập 2 rồi Lưu nháp.',
     '2',
     '- Lưu thành công.\n'
     '- ⚠️ Kế toán được phép chốt ít hơn số người lập xin.'),
    ('004', 'SL xuất giữ bằng 0 ở dòng có tích', 'P0',
     'Dòng có tích Cần xuất.',
     '1. Nhập 0 rồi Lưu nháp.',
     '0',
     '- Báo đỏ tại dòng: "Phải lớn hơn 0."\n- Không lưu.'),
    ('005', 'Bỏ trống SL xuất giữ ở dòng có tích', 'P0',
     'Dòng có tích Cần xuất.',
     '1. Xóa trắng ô SL xuất giữ rồi Lưu nháp.',
     '—',
     '- Báo đỏ tại dòng: "Phải lớn hơn 0."\n- Không lưu.'),
    ('006', 'Nhập chữ vào ô SL xuất giữ', 'P1',
     'Dòng có tích Cần xuất.',
     '1. Gõ "abc" vào ô.',
     'abc',
     '- Ô không nhận ký tự chữ.'),
    ('007', 'Nhập số âm vào ô SL xuất giữ', 'P1',
     'Dòng có tích Cần xuất.',
     '1. Gõ -3 vào ô.',
     '-3',
     '- Ô không nhận dấu trừ, chỉ còn 3.'),
    ('008', 'Bỏ tích hết các dòng rồi lưu', 'P0',
     'Bảng có 2 dòng, bỏ tích cả hai.',
     '1. Bấm Lưu nháp.',
     '—',
     '- Báo "Chưa chọn hàng hoá nào cần xuất giữ, hoặc số lượng đều bằng 0."\n- Không lưu.'),
    ('009', 'Ghi chú quá 255 ký tự', 'P1',
     'Đang ở màn lập phiếu.',
     '1. Nhập 300 ký tự vào ô Ghi chú rồi Lưu nháp.',
     'chuỗi 300 ký tự',
     '- Ô chặn ở 255 ký tự khi gõ, hoặc báo "Không được vượt quá 255 ký tự" khi lưu.'),
    ('010', 'Tệp đính kèm vượt 13 MB', 'P1',
     'Có tệp PDF 20 MB.',
     '1. Chọn tệp đó.',
     'tệp 20 MB',
     '- Bị từ chối, báo tệp vượt dung lượng cho phép.'),
    ('011', 'Tệp đính kèm sai định dạng', 'P1',
     'Có tệp .exe.',
     '1. Chọn tệp đó.',
     'tệp .exe',
     '- Bị từ chối; chỉ nhận PDF, ảnh, Word, Excel.'),
    ('012', 'Gửi dòng hàng không có trong yêu cầu nguồn', 'P0',
     'Tester kỹ thuật gửi một dòng hàng không nằm trong yêu cầu.',
     '1. Gọi thẳng chức năng lưu phiếu với dòng hàng lạ.',
     '—',
     '- Bị chặn: "Hàng hoá không có trong yêu cầu xuất giữ."\n'
     '- ⚠️ Không cho phép Kế toán tự thêm hàng ngoài yêu cầu.'),
    ('013', 'Gửi dòng hàng đúng hàng nhưng sai đơn vị tính', 'P1',
     'Tester kỹ thuật gửi dòng hàng đúng hàng hóa nhưng khác đơn vị tính so với yêu cầu.',
     '1. Gọi thẳng chức năng lưu phiếu.',
     '—',
     '- Bị chặn: "Hàng hoá không có trong yêu cầu xuất giữ."\n'
     '- ⚠️ Hệ thống ghép theo cặp hàng hóa + đơn vị tính.'),
    ('014', 'Giá trị nhập sai KHÔNG bị tự sửa', 'P0',
     'Nhập SL xuất giữ vượt SL yêu cầu.',
     '1. Bấm Lưu và quan sát ô vừa nhập.',
     '—',
     '- ⚠️ Giá trị người dùng gõ vẫn nguyên trong ô.\n'
     '- Phần mềm chỉ báo đỏ, không tự kéo về mức trần.'),
    ('015', 'Nhiều lỗi cùng lúc thì báo hết cùng lúc', 'P1',
     'Hai dòng đều nhập SL xuất giữ vượt SL yêu cầu.',
     '1. Bấm Lưu nháp.',
     '—',
     '- Cả hai dòng đều báo đỏ cùng lúc.'),
]

S11 = [
    ('001', 'Hai Kế toán cùng lập phiếu cho một yêu cầu', 'P0',
     'Hai Kế toán cùng mở một yêu cầu Chờ KT duyệt.',
     '1. Kế toán 1 lập và lưu nháp phiếu.\n'
     '2. Kế toán 2 bấm Lập phiếu xuất giữ trên màn cũ rồi lưu.',
     '—',
     '- Kế toán 1 thành công.\n'
     '- ⚠️ Kế toán 2 bị chặn: "Yêu cầu này đã có phiếu xuất giữ …".'),
    ('002', 'Hai người cùng duyệt một phiếu nháp', 'P0',
     'Kế toán và tài khoản quản trị cùng mở một phiếu nháp.',
     '1. Người 1 bấm Duyệt giữ hàng và xác nhận.\n'
     '2. Người 2 bấm Duyệt giữ hàng trên màn cũ.',
     '—',
     '- Người 1 thành công.\n'
     '- ⚠️ Người 2 bị chặn; hàng KHÔNG bị cộng hai lần vào kho hàng giữ.'),
    ('003', 'Kế toán xóa phiếu trong lúc người khác đang xem', 'P1',
     'Kế toán xóa phiếu nháp. Tài khoản quản trị đang mở màn chi tiết phiếu đó.',
     '1. Người quản trị bấm Quay lại rồi mở lại phiếu.',
     '—',
     '- Hệ thống báo không tìm thấy phiếu.\n- Không hiện màn trắng hay lỗi kỹ thuật.'),
    ('004', 'Người lập yêu cầu sửa yêu cầu trong lúc Kế toán đang lập phiếu', 'P1',
     'Yêu cầu đã sang "Đang xuất giữ" sau khi Kế toán lưu nháp phiếu.',
     '1. Người lập yêu cầu thử mở màn Sửa yêu cầu.',
     '—',
     '- ⚠️ Không sửa được, vì yêu cầu không còn ở trạng thái "Đang tạo".'),
    ('005', 'Phiếu của công ty khác không rò rỉ qua ô lọc', 'P0',
     'Tài khoản chỉ có quyền xem theo công ty 1.',
     '1. Lọc theo nhiều tiêu chí khác nhau, kể cả Tên mã hàng và Yêu cầu xuất giữ.\n'
     '2. Bật cột Phòng yêu cầu và soát toàn bộ kết quả.',
     '—',
     '- ⚠️ Không dòng nào thuộc công ty khác, ở mọi tổ hợp bộ lọc.'),
    ('006', 'Ô lọc Tên mã hàng không làm lộ phiếu ngoài phạm vi', 'P0',
     'Hàng HH01 có mặt ở phiếu của nhiều công ty. Tài khoản chỉ xem được công ty 1.',
     '1. Lọc Tên mã hàng = HH01.',
     '—',
     '- ⚠️ Chỉ ra phiếu của công ty 1.'),
    ('007', 'Ô lọc Yêu cầu xuất giữ không làm lộ phiếu ngoài phạm vi', 'P0',
     'Tài khoản chỉ xem được phiếu của mình.',
     '1. Lọc theo một mã yêu cầu của phiếu người khác.',
     '—',
     '- ⚠️ Không có kết quả.'),
    ('008', 'Đổi quyền của người dùng thì phạm vi đổi theo ngay', 'P1',
     'Tài khoản A đang chỉ xem được phiếu của mình.',
     '1. Quản trị cấp thêm quyền "Kế toán duyệt hàng giữ" cho A.\n'
     '2. A đăng xuất, đăng nhập lại và mở màn hình.',
     '—',
     '- N tăng lên đúng số phiếu của công ty A.'),
]

S12 = [
    ('001', 'Xem lịch sử từ cột Hành động', 'P0',
     'Có phiếu đã qua vài thao tác.',
     '1. Bấm biểu tượng đồng hồ ở cột Hành động.',
     '—',
     '- Mở cửa sổ Lịch sử thay đổi của đúng phiếu đó, mới nhất trước.'),
    ('002', 'Xem lịch sử từ màn chi tiết', 'P0',
     'Đang xem chi tiết một phiếu.',
     '1. Cuộn xuống khối Lịch sử thay đổi.\n2. Bấm nút Xem lịch sử.',
     '—',
     '- Khối mở ra, hiện danh sách mốc thay đổi.\n'
     '- Tiêu đề khối hiện thêm số mốc, nút đổi nhãn thành "Thu gọn".'),
    ('003', 'Khối lịch sử chỉ nạp dữ liệu khi bấm mở', 'P1',
     'Mở màn chi tiết một phiếu.',
     '1. Quan sát khối Lịch sử thay đổi ngay khi vào màn.',
     '—',
     '- ⚠️ Khối ở trạng thái thu gọn, chưa nạp dữ liệu.'),
    ('004', 'Mốc Tạo phiếu ghi đủ thông tin ban đầu', 'P0',
     'Vừa lập một phiếu mới.',
     '1. Mở lịch sử của phiếu đó.',
     '—',
     '- Có mốc "Tạo phiếu" ghi người thực hiện, thời điểm.\n'
     '- Liệt kê yêu cầu xuất giữ, khách hàng, giữ đến ngày, trạng thái và các dòng hàng.'),
    ('005', 'Mốc Chỉnh sửa nêu rõ giá trị cũ và mới', 'P0',
     'Sửa SL xuất giữ của một dòng từ 4 thành 2 rồi lưu.',
     '1. Mở lịch sử của phiếu.',
     '—',
     '- Có mốc "Chỉnh sửa" ghi rõ dòng hàng nào, từ 4 đổi thành 2.'),
    ('006', 'Mốc Duyệt giữ hàng ghi rõ số lô đã ghi tồn', 'P0',
     'Vừa duyệt một phiếu có 1 dòng cần xuất.',
     '1. Mở lịch sử của phiếu.',
     '—',
     '- ⚠️ Mốc "Duyệt giữ hàng" ghi rõ "Đã ghi tồn giữ cho 1 lô hàng."\n'
     '- Ghi trạng thái đổi từ Đang tạo sang Đã duyệt.'),
    ('007', 'Phiếu cũ chưa có lịch sử hiện đúng câu thông báo', 'P1',
     'Phiếu lập từ trước khi bật tính năng ghi lịch sử.',
     '1. Mở lịch sử của phiếu đó.',
     '—',
     '- Hiện dòng "Chưa có lịch sử thao tác nào."\n- Không báo lỗi.'),
    ('008', 'Nút Làm mới nạp lại lịch sử', 'P2',
     'Khối lịch sử đang mở.',
     '1. Bấm nút Làm mới.',
     '—',
     '- Danh sách mốc được nạp lại.'),
    ('009', 'Thứ tự lịch sử là mới nhất trước', 'P1',
     'Phiếu có ít nhất 3 mốc.',
     '1. Đọc thời điểm của từng mốc từ trên xuống.',
     '—',
     '- Thời điểm giảm dần từ trên xuống.'),
]

S13 = [
    ('001', 'Luồng đầy đủ: lập phiếu → duyệt giữ hàng', 'P0',
     'Yêu cầu của nhân viên A đang ở "Chờ KT duyệt", xin giữ HH01 số lượng 10. Kho còn 100. '
     'A chưa giữ lô nào của HH01.',
     '1. Kế toán mở yêu cầu, bấm Lập phiếu xuất giữ.\n'
     '2. Giữ nguyên số lượng, bấm Duyệt giữ hàng và xác nhận.\n'
     '3. Mở màn Danh sách hàng giữ, lọc theo A.\n'
     '4. Quay lại màn Yêu cầu xuất giữ và tìm yêu cầu đó.',
     '—',
     '- Sau bước 2: phiếu ở "Đã duyệt".\n'
     '- Sau bước 3: ⚠️ A có lô hàng giữ HH01 số lượng 10.\n'
     '- Sau bước 4: yêu cầu ở "Đã duyệt", cột Người duyệt là Kế toán.'),
    ('002', 'Luồng lưu nháp rồi duyệt sau', 'P0',
     'Yêu cầu đang ở "Chờ KT duyệt".',
     '1. Kế toán lập phiếu và Lưu nháp.\n2. Kiểm tra trạng thái yêu cầu.\n'
     '3. Hôm sau mở phiếu ra Sửa và bấm Duyệt giữ hàng.\n4. Kiểm tra lại.',
     '—',
     '- Sau bước 2: yêu cầu ở "Đang xuất giữ", tồn hàng giữ CHƯA đổi.\n'
     '- Sau bước 4: phiếu và yêu cầu đều ở "Đã duyệt", hàng giữ đã được ghi.'),
    ('003', 'Luồng lưu nháp rồi xóa, yêu cầu quay lại bước Kế toán', 'P0',
     'Yêu cầu đang ở "Chờ KT duyệt".',
     '1. Kế toán lập phiếu và Lưu nháp.\n2. Kế toán xóa phiếu.\n'
     '3. Kiểm tra trạng thái yêu cầu và tồn hàng giữ.',
     '—',
     '- ⚠️ Yêu cầu quay về "Chờ KT duyệt".\n'
     '- Tồn hàng giữ không đổi suốt quá trình.\n'
     '- Nút Lập phiếu xuất giữ hiện lại ở yêu cầu.'),
    ('004', 'Luồng Kế toán chốt số ít hơn số người lập xin', 'P0',
     'Yêu cầu xin giữ 10, nhưng kho chỉ còn 6.',
     '1. Kế toán lập phiếu, đổi SL xuất giữ thành 6.\n2. Bấm Duyệt giữ hàng.\n'
     '3. Kiểm tra lô hàng giữ.',
     '6',
     '- Duyệt thành công.\n'
     '- ⚠️ Lô hàng giữ có số lượng 6, không phải 10.\n'
     '- Yêu cầu vẫn chuyển sang "Đã duyệt".'),
    ('005', 'Luồng Kế toán bỏ tích một dòng', 'P0',
     'Yêu cầu có 2 dòng hàng được xin giữ.',
     '1. Kế toán lập phiếu, bỏ tích dòng 2.\n2. Duyệt giữ hàng.\n3. Kiểm tra lô hàng giữ.',
     '—',
     '- Chỉ sinh lô cho dòng 1.\n- Dòng 2 lưu với số lượng 0, không có lô.'),
    ('006', 'Luồng Kế toán bấm Không duyệt rồi đổi ý duyệt', 'P0',
     'Yêu cầu đang ở "Chờ KT duyệt".',
     '1. Kế toán lập phiếu, bấm "Không duyệt".\n2. Kiểm tra trạng thái phiếu và yêu cầu.\n'
     '3. Mở phiếu ra Sửa, bấm Duyệt giữ hàng.\n4. Kiểm tra lại.',
     '—',
     '- Sau bước 2: ⚠️ phiếu ở "Đang tạo", yêu cầu ở "Đang xuất giữ" — KHÔNG bị trả về người lập.\n'
     '- Sau bước 4: cả hai đều "Đã duyệt", hàng giữ đã ghi.'),
    ('007', 'Muốn trả yêu cầu về thì phải từ chối ở màn Yêu cầu xuất giữ', 'P0',
     'Yêu cầu đang ở "Chờ KT duyệt".',
     '1. Kế toán mở màn Yêu cầu xuất giữ, mở yêu cầu, bấm nút "Từ chối", nhập lý do, xác nhận.\n'
     '2. Kiểm tra trạng thái yêu cầu.',
     'Lý do: Kho không còn đủ hàng',
     '- ⚠️ Yêu cầu về "Đang tạo" kèm lý do, người lập sửa lại được.\n'
     '- Không có phiếu xuất giữ nào được tạo.'),
    ('008', 'Đối chiếu chéo với màn Lịch sử giữ hàng', 'P0',
     'Vừa duyệt một phiếu xuất giữ 3 đơn vị, đơn vị "Thùng" hệ số 10.',
     '1. Mở màn chi tiết phiếu, đọc cột SL xuất giữ và cột SL giữ (ĐV cơ bản).\n'
     '2. Mở lịch sử biến động của lô hàng giữ tương ứng.',
     '—',
     '- Bước 1: SL xuất giữ = 3, SL giữ (ĐV cơ bản) = 30.\n'
     '- ⚠️ Bước 2: nhật ký lô ghi +30, khớp với cột SL giữ (ĐV cơ bản), KHÔNG khớp cột SL '
     'xuất giữ.'),
    ('009', 'Hàng vừa giữ dùng được ngay ở màn Gia hạn hàng giữ', 'P1',
     'Vừa duyệt xong, A có lô hàng giữ mới với hạn còn dưới 7 ngày.',
     '1. Đăng nhập bằng A.\n2. Mở màn Yêu cầu gia hạn hàng giữ và bấm Tạo mới.',
     '—',
     '- ⚠️ Lô vừa sinh xuất hiện trong danh sách lô sắp hết hạn của A.'),
    ('010', 'Hàng vừa giữ dùng được ngay ở màn Hủy hàng giữ', 'P1',
     'A vừa có lô hàng giữ mới.',
     '1. Đăng nhập bằng A.\n'
     '2. Mở màn Yêu cầu hủy hàng giữ, bấm Tạo mới, chọn khách hàng tương ứng.',
     '—',
     '- Lô vừa sinh xuất hiện trong danh sách hàng đang giữ của A.'),
    ('011', 'Hàng vừa giữ dùng được ngay ở màn Điều chuyển hàng giữ', 'P1',
     'A vừa có lô hàng giữ mới.',
     '1. Đăng nhập bằng A.\n2. Mở màn Yêu cầu điều chuyển hàng giữ, bấm Tạo mới, bấm Thêm '
     'hàng hóa.',
     '—',
     '- Lô vừa sinh xuất hiện trong popup hàng A đang giữ.'),
    ('012', 'Hai phiếu cùng giữ một hàng, cái sau bị chặn vì hết tồn', 'P0',
     'Hàng HH02 chỉ còn 5 trong kho. Hai yêu cầu cùng xin giữ 5, cả hai đã tới bước Kế toán.',
     '1. Kế toán duyệt phiếu xuất giữ của yêu cầu 1.\n'
     '2. Kế toán lập phiếu cho yêu cầu 2 và bấm Duyệt giữ hàng.',
     '—',
     '- Bước 1 thành công.\n'
     '- ⚠️ Bước 2 bị chặn: "Kho không đủ số lượng (còn 0)."\n'
     '- Kế toán phải giảm số lượng hoặc từ chối yêu cầu 2.'),
]

SECTIONS = [
    ('I', 'HIỂN THỊ TRANG & TRUY CẬP', S1),
    ('II', 'BỘ LỌC & TÌM KIẾM', S2),
    ('III', 'DANH SÁCH, SẮP XẾP & PHÂN TRANG', S3),
    ('IV', 'LẬP PHIẾU XUẤT GIỮ', S4),
    ('V', 'SỬA PHIẾU NHÁP', S5),
    ('VI', 'XEM CHI TIẾT', S6),
    ('VII', 'DUYỆT GIỮ HÀNG — GHI TỒN HÀNG GIỮ', S7),
    ('VIII', 'XÓA PHIẾU', S8),
    ('IX', 'IN & XUẤT EXCEL', S9),
    ('X', 'RÀNG BUỘC NHẬP LIỆU', S10),
    ('XI', 'CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI', S11),
    ('XII', 'LỊCH SỬ THAY ĐỔI', S12),
    ('XIII', 'LUỒNG NGHIỆP VỤ ĐẦU CUỐI', S13),
]

build(output_file=os.path.join(BASE, 'testcase_phieu_xuat_giu.xlsx'),
      sheet_name='Trang tính1',
      feature_name='Phiếu xuất giữ',
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
