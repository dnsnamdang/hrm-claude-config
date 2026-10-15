# -*- coding: utf-8 -*-
"""HDSD Bao cao chi phi van chuyen theo NVKD theo MAU VAN XUOI (mau HDSD_YeuCauXuatHang.docx, user dua 12/10/2026).

Sinh: HDSD_Bao cao chi phi van chuyen theo NVKD.docx (thay ban gon cu)
Chay:  python ve_so_do.py && python gen_hdsd_mau.py   (anh hdsd_shots/ chup 08/10/2026, ky 06/2026)
Khung + ham dung: ../_hdsd_van_xuoi/hdsd_van_xuoi.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '_hdsd_van_xuoi'))
from hdsd_van_xuoi import HdsdVanXuoi, cap_nhat_truong  # noqa: E402

SHOTS = os.path.join(HERE, 'hdsd_shots')
NGAY = '12/10/2026'
TEN = 'Báo cáo chi phí vận chuyển theo nhân viên kinh doanh'
Q = 'Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh - '
M_YCXH = 'Khởi tạo › Hàng hóa › Nhập - xuất hàng › "Phiếu Yêu cầu xuất hàng"'


def S(name):
    return os.path.join(SHOTS, name + '.png')


def main():
    d = HdsdVanXuoi(TEN)

    # ============================================================================== TỔNG QUAN
    d.h1('TỔNG QUAN PHẦN MỀM')
    d.h2('1. Thuật ngữ & viết tắt')
    d.p('Bảng thuật ngữ giúp người dùng hiểu đúng các con số và các bước hướng dẫn.')
    d.table([['Thuật ngữ', 'Ý nghĩa'],
             ['NVKD', 'Nhân viên kinh doanh — người chịu cước vận chuyển của dòng hàng trên chuyến xe.'],
             ['Chuyến xe', 'Một lượt xe chở hàng do điều vận lập, chở hàng của một hoặc nhiều phiếu xuất kho.'],
             ['Phiếu hạch toán chuyến xe', 'Phiếu kế toán lập để ghi nhận chi phí của chuyến xe chở hàng. Mã phiếu hiện ở cột Số chuyến xe.'],
             ['Phiếu hạch toán chuyến xe khác', 'Phiếu kế toán lập cho chuyến xe không chở hàng theo phiếu xuất kho.'],
             ['Dòng hạch toán', 'Một dòng chi phí trên phiếu hạch toán: số tiền, mã công việc, nhân viên chịu.'],
             ['Mã công việc', 'Loại chi phí của dòng hạch toán (cước vận chuyển, xăng xe, vé cầu đường…).'],
             ['Cước vận chuyển', 'Tổng các dòng hạch toán được tính vào báo cáo của một nhân viên trên một chuyến.'],
             ['Ngày hạch toán', 'Ngày ghi trên phiếu hạch toán; báo cáo lọc theo ngày này.'],
             ['Đối tượng chịu phí', 'Ai chịu phí của dòng hàng trên chuyến: Nhân viên chịu hoặc Công ty chịu.'],
             ['YCXH', 'Phiếu yêu cầu xuất hàng.'],
             ['Show chi tiết', 'Ô tích ở góc bảng; tích vào thì hiện từng chuyến dưới mỗi nhân viên.']],
            widths=[2.0, 4.5])

    d.h2('2. Lịch sử cập nhật tài liệu')
    d.table([['Phiên bản', 'Ngày', 'Nội dung', 'Người thực hiện'],
             ['1.0', '08/10/2026', 'Khởi tạo HDSD bản rút gọn', 'Phòng Phát triển'],
             ['2.0', NGAY, 'Viết lại theo mẫu HDSD chuẩn, bổ sung hướng dẫn kiểm tra số liệu', 'Phòng Phát triển']],
            widths=[0.9, 1.1, 3.0, 1.5])

    d.h2('3. Giới thiệu chung & đường dẫn truy cập')
    d.p('Báo cáo tổng hợp cước vận chuyển đã hạch toán cho từng nhân viên kinh doanh, gom theo Phòng ban › Nhân viên › từng '
        'chuyến xe. Dùng để biết mỗi phòng, mỗi nhân viên đã phát sinh bao nhiêu tiền vận chuyển trong kỳ. Màn chỉ để xem, '
        'không sửa dữ liệu.')
    d.bullet('Đường dẫn 1: ', 'menu Kinh doanh › Báo cáo bán hàng › nhóm Báo cáo Vận chuyển › "Báo cáo chi phí vận chuyển theo nhân viên kinh doanh".')
    d.bullet('Đường dẫn 2: ', 'menu Kho › Vận chuyển - Bốc xếp › nhóm Báo cáo vận chuyển › cùng tên. Hai đường vào mở cùng một màn.')
    d.p('Báo cáo không tự tính ra số. Con số đến từ luồng giao hàng chuẩn của ERP:')
    d.table([['Bước', 'Chứng từ (ai lập)', 'Ảnh hưởng tới báo cáo'],
             ['1', 'Phiếu yêu cầu xuất hàng theo hợp đồng (nhân viên kinh doanh lập) → đề nghị xuất kho → phiếu xuất kho (kho)', 'Chưa có số.'],
             ['2', 'Chuyến xe chở hàng cho phiếu xuất kho (điều vận lập)', 'Chưa có số.'],
             ['3', 'Phiếu hạch toán chuyến xe (kế toán lập): mỗi dòng có số tiền, mã công việc, nhân viên chịu', 'Khi hạch toán: dòng có nhân viên và mã công việc hợp lệ được cộng vào cước của nhân viên đó.'],
             ['3b', 'Phiếu hạch toán chuyến xe khác (chuyến không chở hàng theo phiếu xuất kho)', 'Như bước 3.']],
            widths=[0.65, 3.2, 2.65])
    d.image(S('so_do'), 'Sơ đồ luồng số liệu của báo cáo')

    d.h2('4. Quyền & phạm vi (tổng quan)')
    d.p('Mọi tài khoản đều mở được màn. Phạm vi dữ liệu nhìn thấy phụ thuộc quyền:')
    d.table([['Tên quyền', 'Thấy cước của', 'Ô lọc có thêm'],
             [Q + 'Theo tổng công ty (hoặc quyền cũ "Xem báo cáo vận chuyển theo công ty theo tổng công ty")', 'Mọi công ty.', 'Công ty, Phòng ban, Nhân viên'],
             [Q + 'Theo công ty (hoặc quyền cũ "Xem báo cáo vận chuyển theo công ty")', 'Công ty của mình.', 'Phòng ban, Nhân viên'],
             [Q + 'Theo phòng ban', 'Phòng ban HIỆN TẠI của mình (không gồm phòng được phân quản lý).', 'Nhân viên'],
             ['Không có quyền nào ở trên', 'Chỉ cước ghi cho chính mình.', 'Không có']],
            widths=[3.0, 1.9, 1.6])

    # ============================================================================== PHẦN 1
    d.h1('PHẦN 1: TRUY CẬP & BỐ CỤC MÀN HÌNH')
    d.h2('1.1. Cách truy cập')
    d.p('Vào một trong hai đường dẫn ở mục 3. Màn mở ra với bảng trống — báo cáo không tự tải, phải chọn Từ ngày, Đến ngày rồi bấm Lọc.')
    d.image(S('00_menu_kd'), 'Đường vào từ menu Kinh doanh › Báo cáo bán hàng')
    d.image(S('00_menu_kho'), 'Đường vào từ menu Kho › Vận chuyển - Bốc xếp')
    d.h2('1.2. Bố cục màn hình')
    d.bullet('Khung Bộ lọc: ', 'Từ ngày, Đến ngày (bắt buộc), Công ty, Phòng ban, Nhân viên (tùy quyền), Số chuyến xe, Hợp đồng, Yêu cầu xuất hàng, Đối tượng chịu phí. Có nút thu gọn khung ở góc phải.')
    d.bullet('Hàng nút: ', 'Lọc, Làm mới (nút xanh lá biểu tượng mũi tên tròn), Xuất Excel.')
    d.bullet('Khung Chi tiết: ', 'bảng báo cáo, ô tích "Show chi tiết" ở góc phải; dòng Tổng cộng ngay dưới tiêu đề.')
    d.bullet('Phân trang: ', 'dưới bảng, mỗi trang 20 phòng ban.')
    d.image(S('01_list'), 'Màn báo cáo sau khi lọc kỳ 06/2026')

    # ============================================================================== PHẦN 2
    d.h1('PHẦN 2: BỘ LỌC & CÁC NÚT')
    d.h2('2.1. Các ô lọc')
    d.table([['Ô lọc', 'Bắt buộc', 'Cách dùng'],
             ['Từ ngày / Đến ngày', 'Có', 'Kỳ báo cáo theo ngày hạch toán của phiếu (lấy trọn 2 ngày). Nút Lọc chỉ bấm được khi đã nhập đủ 2 ô.'],
             ['Công ty / Phòng ban / Nhân viên', 'Không', 'Chỉ hiện khi có quyền (mục 4). Ô dưới thu hẹp theo ô trên.'],
             ['Số chuyến xe', 'Không', 'Nhập mã phiếu hạch toán chuyến xe.'],
             ['Hợp đồng', 'Không', 'Nhập mã hợp đồng của hàng trên chuyến.'],
             ['Yêu cầu xuất hàng', 'Không', 'Nhập mã phiếu yêu cầu xuất hàng.'],
             ['Đối tượng chịu phí', 'Không', 'Tất cả / Nhân viên chịu / Công ty chịu.']],
            widths=[2.0, 0.8, 3.7])
    d.note('Lưu ý: ', '4 ô Số chuyến xe, Hợp đồng, Yêu cầu xuất hàng, Đối tượng chịu phí lọc theo CHUYẾN: chuyến có ít nhất một dòng '
           'hàng khớp thì lấy TOÀN BỘ cước của chuyến đó; khi đã nhập một trong 4 ô này, chuyến không chở phiếu xuất kho nào bị loại.')
    d.h2('2.2. Các nút')
    d.table([['Nút', 'Kết quả'],
             ['Lọc', 'Tải báo cáo theo điều kiện đã chọn.'],
             ['Làm mới', 'Xóa Từ ngày, Đến ngày và các ô Công ty, Phòng ban, Nhân viên.'],
             ['Xuất Excel', 'Mở cửa sổ "Xuất Excel" để chọn mẫu và xuất file (PHẦN 4).'],
             ['Show chi tiết (ô tích)', 'Hiện / ẩn từng chuyến dưới mỗi nhân viên.']],
            widths=[1.8, 4.7])

    # ============================================================================== PHẦN 3
    d.h1('PHẦN 3: ĐỌC BÁO CÁO')
    d.h2('3.1. Các cấp dòng')
    d.table([['Cấp', 'Nhận biết', 'Nội dung'],
             ['Tổng cộng', 'Ngay dưới tiêu đề cột', 'Tổng cước mọi phòng ban của MỌI trang.'],
             ['Phòng ban', 'STT 1, 2…; chữ đậm', 'Tên phòng + tổng cước của các nhân viên trong phòng. Xếp theo tên phòng A-Z.'],
             ['Nhân viên', 'STT 1.1, 1.2…; chữ xanh', 'Mã nhân viên, họ tên, tổng cước. Xếp theo họ tên A-Z.'],
             ['Chuyến', 'STT 1.1.1…; chỉ hiện khi tích Show chi tiết', 'Một chuyến của nhân viên và cước nhân viên chịu trên chuyến đó.']],
            widths=[1.2, 2.2, 3.1])
    d.p('Nhân viên được xếp vào phòng ban ghi trên dòng hạch toán (phòng lúc hạch toán). Nhân viên đã chuyển phòng trong kỳ có thể xuất hiện ở 2 phòng.')
    d.h2('3.2. Các cột')
    d.table([['Cột', 'Ý nghĩa'],
             ['STT', 'Theo cấp: 1 / 1.1 / 1.1.1.'],
             ['Mã NVKD', 'Mã nhân viên (dòng nhân viên).'],
             ['Thời gian', 'Ngày của phiếu hạch toán chuyến (dòng chuyến).'],
             ['Tải trọng tính cước / Dòng xe tính cước', 'Tải trọng và loại xe dùng để tính cước của chuyến.'],
             ['Xe chạy thực tế', 'Biển số - tải trọng - loại xe thực tế chạy.'],
             ['Tuyến đường', 'Điểm đi - điểm đến của chuyến.'],
             ['Cước vận chuyển', 'Dòng chuyến: tổng các dòng hạch toán của nhân viên trong phiếu. Dòng nhân viên: tổng các chuyến. Dòng phòng: tổng các nhân viên.'],
             ['Yêu cầu xuất hàng / Hợp đồng', 'Mã phiếu yêu cầu xuất hàng và hợp đồng của hàng trên chuyến; bấm để mở ở thẻ mới.'],
             ['Số chuyến xe', 'Mã phiếu hạch toán chuyến xe; bấm để mở ở thẻ mới.']],
            widths=[2.2, 4.3])
    d.p('Số tiền có dấu phẩy ngăn cách hàng nghìn; cước bằng 0 hoặc âm hiện dấu "-".')
    d.h2('3.3. Dòng hạch toán nào được tính, nào không')
    d.table([['Được tính khi đủ cả 4 điều kiện', 'KHÔNG được tính'],
             ['Thuộc phiếu hạch toán chuyến xe hoặc phiếu hạch toán chuyến xe khác',
              'Dòng không gắn nhân viên kinh doanh'],
             ['Có gắn nhân viên kinh doanh chịu cước',
              'Dòng có mã công việc: Công lái xe, Xăng xe, Chi phí khác, Vé cầu đường, Công tác phí (chi phí nội bộ của xe)'],
             ['Ngày hạch toán nằm trong kỳ lọc', 'Dòng không chọn mã công việc'],
             ['Có mã công việc và mã đó không thuộc 5 loại ở cột bên', 'Dòng ngoài phạm vi quyền xem của người đang xem']],
            widths=[3.25, 3.25])
    d.h2('3.4. Ví dụ đọc số trên ảnh thật')
    d.p('Tích Show chi tiết (kỳ 01/06/2026 - 30/06/2026), xem phòng Kinh doanh CN Vinh:')
    d.image(S('02_detail'), 'Báo cáo khi tích Show chi tiết')
    d.table([['Dòng', 'Cách tính', 'Kết quả'],
             ['1.1 Nguyễn Văn Tế', 'Chuyến 1.1.1 (561,825) + chuyến 1.1.2 (1,320,187)', '1,882,012'],
             ['1.2 Trần Nguyễn Văn Thắng', '462,375 + 758,250 + 1,276,312', '2,496,937'],
             ['1 Kinh doanh CN Vinh', '1,882,012 + 2,496,937', '4,378,949'],
             ['Tổng cộng', 'Cộng mọi phòng ban của mọi trang', '112,850,159']],
            widths=[2.0, 3.0, 1.5])

    # ============================================================================== PHẦN 4
    d.h1('PHẦN 4: XEM CHI TIẾT & XUẤT EXCEL')
    d.h2('4.1. Xem chi tiết từng chuyến')
    d.p('Tích "Show chi tiết": dưới mỗi nhân viên hiện các chuyến xe. Bấm mã ở cột Yêu cầu xuất hàng, Hợp đồng hoặc Số chuyến xe để '
        'mở chứng từ đó ở thẻ mới. Bỏ tích để ẩn các chuyến.')
    d.h2('4.2. Xuất Excel')
    d.p('Lọc báo cáo theo dữ liệu cần lấy, bấm Xuất Excel, cửa sổ "Xuất Excel" hiện ra. Ở ô Mẫu excel chọn một trong hai mẫu rồi bấm "Xuất EXCEL":')
    d.image(S('03_export'), 'Cửa sổ Xuất Excel')
    d.table([['Mẫu', 'Nội dung'],
             ['Xuất excel đầy đủ', 'Phòng ban, nhân viên và từng chuyến.'],
             ['Xuất excel ngắn gọn', 'Chỉ phòng ban và nhân viên.']],
            widths=[2.0, 4.5])
    d.p('Kết quả dưới 50 phòng ban: trình duyệt mở thẻ mới và tải file ngay. Từ 50 phòng ban trở lên: hệ thống thông báo và gửi file qua email. '
        'Bấm dấu × để đóng cửa sổ, không xuất.')

    # ============================================================================== PHẦN 5
    d.h1('PHẦN 5: HƯỚNG DẪN KIỂM TRA SỐ LIỆU (DÀNH CHO NGƯỜI TEST)')
    d.p('Phần này hướng dẫn cách chứng minh báo cáo ĐÚNG: tự đi luồng giao hàng chuẩn của ERP tới bước hạch toán chuyến xe, '
        'rồi xem cước của nhân viên thay đổi có khớp với phiếu vừa hạch toán không.')
    d.h2('5.1. Chuẩn bị trước khi test')
    d.table([['Dữ liệu', 'Giá trị mẫu', 'Ghi chú'],
             ['Nhân viên kinh doanh', 'Nhân viên A, phòng Kinh doanh 1', 'Người sẽ chịu cước.'],
             ['Hợp đồng', 'HD-TEST-01 của A', 'Đã ký, có hàng để xuất.'],
             ['Kỳ lọc', 'Từ ngày = ngày 1 tháng hiện tại; Đến ngày = hôm nay', 'Phiếu hạch toán test đều hạch toán trong kỳ này.'],
             ['Người lập phiếu', 'Kho, điều vận, kế toán (hoặc tài khoản đủ quyền)', 'Tester không lập được bước nào thì nhờ bộ phận đó lập giúp.']],
            widths=[1.6, 2.4, 2.5])
    d.p('Quy tắc: trước mỗi bước, lọc báo cáo với Nhân viên = A, tích Show chi tiết và ghi lại cước hiện tại của A (số nền). '
        'Kết quả đúng là CHÊNH LỆCH so với số nền.')
    d.h2('5.2. Kịch bản kiểm tra theo luồng phát sinh chuẩn ERP')
    d.table([['STT', 'Việc cần làm', 'Kết quả đúng trên báo cáo'],
             ['1', 'A lập Phiếu yêu cầu xuất hàng theo HD-TEST-01 (menu ' + M_YCXH + '), gửi duyệt; kho lập đề nghị xuất kho và phiếu xuất kho.', 'Không đổi (chưa có chuyến, chưa hạch toán).'],
             ['2', 'Điều vận lập chuyến xe chở hàng cho phiếu xuất kho ở bước 1.', 'Không đổi (chuyến chưa hạch toán).'],
             ['3', 'Kế toán lập Phiếu hạch toán chuyến xe cho chuyến ở bước 2, ngày hạch toán hôm nay, một dòng cước 500,000 ghi cho A, mã công việc cước vận chuyển; hạch toán.',
              'Cước của A +500,000; phòng Kinh doanh 1 +500,000; Tổng cộng +500,000. Dưới A có thêm 1 dòng chuyến: mã yêu cầu xuất hàng, hợp đồng HD-TEST-01, số chuyến xe = mã phiếu hạch toán.'],
             ['4', 'Thêm vào phiếu ở bước 3 một dòng Xăng xe 300,000 ghi cho A (hoặc Vé cầu đường / Công tác phí / Công lái xe / Chi phí khác).', 'Cước của A KHÔNG đổi.'],
             ['5', 'Thêm vào phiếu một dòng 200,000 ghi cho A nhưng không chọn mã công việc.', 'Cước của A KHÔNG đổi.'],
             ['6', 'Thêm vào phiếu một dòng cước 150,000 không gắn nhân viên.', 'Không nhân viên nào thay đổi.'],
             ['7', 'Thêm vào phiếu một dòng cước 100,000 ghi cho A.', 'Dòng chuyến của A = 600,000 (cộng các dòng của A trong cùng phiếu); cước A +100,000.'],
             ['8', 'Kế toán lập Phiếu hạch toán chuyến xe khác (chuyến không chở hàng theo phiếu xuất kho), dòng cước 250,000 ghi cho A, hạch toán hôm nay.', 'Cước của A +250,000.']],
            widths=[0.55, 3.0, 2.95])
    d.h2('5.3. Kiểm tổng')
    d.p('Sau 8 bước, cước của A tăng so với số nền:')
    d.p([('+500,000 + 100,000 + 250,000 = +850,000', 'b'), ' (các dòng Xăng xe, không mã công việc, không gắn nhân viên không được tính).'])
    d.p('Đối chiếu: cộng tay các dòng cước hợp lệ của A trên mọi phiếu hạch toán trong kỳ phải bằng cước của A trên báo cáo.')
    d.h2('5.4. Kiểm bộ lọc và thời gian')
    d.table([['Tình huống', 'Cách làm', 'Kết quả đúng'],
             ['Phiếu ngoài kỳ', 'Đổi Đến ngày về trước ngày hạch toán của phiếu ở bước 3.', 'Chuyến mới không còn; cước A trở về số nền.'],
             ['Lọc Số chuyến xe', 'Nhập mã phiếu hạch toán ở bước 3.', 'Chỉ còn chuyến đó, đủ toàn bộ cước của chuyến.'],
             ['Lọc Hợp đồng / Yêu cầu xuất hàng', 'Nhập HD-TEST-01 hoặc mã yêu cầu xuất hàng ở bước 1.', 'Có chuyến ở bước 3; không có chuyến xe khác ở bước 8.'],
             ['Lọc Đối tượng chịu phí', 'Chọn Nhân viên chịu, rồi Công ty chịu.', 'Chuyến hiện đúng theo đối tượng chịu phí của dòng hàng.'],
             ['Xuất Excel', 'Xuất mẫu đầy đủ và mẫu ngắn gọn.', 'Số liệu khớp màn hình.']],
            widths=[1.6, 2.5, 2.4])
    d.h2('5.5. Kiểm phạm vi quyền')
    d.table([['Tài khoản', 'Kết quả đúng'],
             ['Không có quyền nào', 'Không có ô Công ty, Phòng ban, Nhân viên; chỉ thấy cước của chính mình.'],
             ['Quyền theo phòng ban', 'Chỉ có ô Nhân viên; chỉ phòng hiện tại của mình.'],
             ['Quyền theo công ty (mới hoặc cũ)', 'Mọi phòng của công ty mình, mỗi phòng đủ nhân viên và chuyến; 2 tài khoản quyền mới và quyền cũ cho kết quả giống hệt.'],
             ['Quyền theo tổng công ty (mới hoặc cũ)', 'Đủ 3 ô lọc; mọi công ty; 2 loại quyền cho kết quả giống hệt.']],
            widths=[2.2, 4.3])

    # ============================================================================== PHẦN 6
    d.h1('PHẦN 6: CÂU HỎI THƯỜNG GẶP & LƯU Ý')
    d.h2('6.1. Câu hỏi thường gặp')
    d.table([['Tình huống', 'Giải thích / cách xử lý'],
             ['Vừa hạch toán mà cước không đổi', 'Dòng không gắn nhân viên, không có mã công việc, hoặc mã công việc thuộc 5 loại bị loại; hoặc ngày hạch toán ngoài kỳ.'],
             ['Nút Lọc không bấm được', 'Chưa nhập đủ Từ ngày và Đến ngày.'],
             ['Nhân viên hiện ở 2 phòng', 'Nhân viên chuyển phòng trong kỳ: báo cáo xếp theo phòng ghi trên dòng hạch toán.'],
             ['Không thấy phòng mình quản lý', 'Quyền theo phòng ban chỉ lấy phòng hiện tại của mình, không gồm phòng được phân quản lý.'],
             ['Bấm Xuất Excel không thấy tải file', 'Kết quả từ 50 phòng ban trở lên: file gửi qua email.']],
            widths=[2.4, 4.1])
    d.h2('6.2. Lỗi đã biết của ERP (gặp đúng hiện tượng thì ghi Failed)')
    d.table([['Hiện tượng', 'Ghi chú'],
             ['Chỉ có quyền MỚI theo tổng công ty / theo công ty: nhiều phòng chỉ hiện dòng tổng, không có nhân viên bên dưới; tổng thiếu cước chuyến xe khác.', 'Tài khoản có quyền cũ không bị.'],
             ['Dòng chuyến lọc và hiện theo ngày cập nhật cuối của phiếu hạch toán, không theo ngày hạch toán.', 'Phiếu bị sửa sau ngày hạch toán sẽ lệch kỳ.'],
             ['Ô Hợp đồng nhập dấu nháy kép báo "Đã có lỗi xảy ra".', ''],
             ['Nút Làm mới không xóa ô Số chuyến xe, Hợp đồng, Yêu cầu xuất hàng, Đối tượng chịu phí.', ''],
             ['File Excel cột Tuyến đường hiện tên chuyến thay vì tuyến đường.', ''],
             ['Excel mẫu đầy đủ: nhân viên có ở 2 phòng bị lặp toàn bộ chuyến ở cả 2 phòng.', ''],
             ['Phiếu hạch toán chuyến xe khác chưa hạch toán xong vẫn được cộng vào tổng phòng / nhân viên nhưng không hiện ở dòng chuyến.', '']],
            widths=[4.4, 2.1])

    out = os.path.join(HERE, 'HDSD_Bao cao chi phi van chuyen theo NVKD.docx')
    d.save(out)
    print('OK', out, 'trang:', cap_nhat_truong(out))


if __name__ == '__main__':
    main()
