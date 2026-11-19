# -*- coding: utf-8 -*-
"""SRS - BC chi phí vận chuyển theo NV kinh doanh (form Danh mục quốc gia — khuôn 7 danh mục kho đã duyệt
+ quy tắc màn BÁO CÁO của skill srs-documenter: bảng "Cách lấy dữ liệu và giải thích chỉ tiêu", bảng liên kết
mở từ số liệu).

Nguồn (code HRM hiện tại, 02/11/2026):
  FE hrm-client/pages/sale/transport-cost-by-staff/{index.vue, components/export-excel.js},
     components/modal/export-fields-modal.vue, utils/{filterRequiredErrors, contract-link}.js,
     components/V2BaseFilterFieldControl.vue (khoảng ngày), components/subsystem-menu/{sale-hub,transport}.js
  BE Modules/Finance/Services/TransportCostByStaffReportService.php, Http/Controllers/V1/TransportCostByStaffController.php,
     Entities/Concerns/ChecksEmployeePermission.php; quyền: Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php
  Phần 5: dò code FE/BE + menu (02/11/2026).
Số liệu ví dụ: dev-hrm 02/11/2026 (hdsd_shots/_capture_log.json).

build_srs của _lib_win không có mục con riêng cho màn báo cáo -> hàm build_srs_report ở đây (chép khuôn
_lib_win.build_srs, thêm 'them' = các mục con sau "Danh sách event"). Không sửa _lib_win.py.
Chạy:  python gen_srs.py [--no-word]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'danh-muc-kho', 'docs'))
import _lib_win as L  # noqa: E402

TEN = 'BC chi phí vận chuyển theo NV kinh doanh'
TEN_MAN = 'Báo cáo chi phí vận chuyển theo nhân viên kinh doanh'
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
PDF = os.path.join(HERE, 'out', 'SRS - %s.pdf' % TEN)
Q = ('Người dùng đã đăng nhập (mọi người dùng vào được màn hình). Quyền "Xem báo cáo chi phí vận chuyển theo nhân '
     'viên kinh doanh theo tổng công ty / theo công ty / theo phòng ban" chỉ mở rộng phạm vi số liệu (BR-01).')
DK = '1. Người dùng đăng nhập thành công.\n2. Không cần quyền để vào màn; phạm vi số liệu theo quyền đang có (BR-01).'
TRUOC = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung SRS_Các quy tắc chung_VN_1.0, '
         'không thực hiện bước After.')

UI7 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Giá trị ban đầu', 'Mô tả']
UI7W = [0.55, 1.05, 0.8, 0.8, 0.75, 0.75, 1.9]
UI8 = ['STT', 'Tên đối tượng', 'Loại', 'Trạng thái', 'Phạm vi', 'Bắt buộc', 'Giá trị ban đầu', 'Mô tả']
UI8W = [0.55, 0.95, 0.8, 0.8, 0.75, 0.65, 0.7, 1.6]


def ui(header, rows):
    return [header] + [[str(i + 1)] + [('\n'.join(c) if isinstance(c, list) else c) for c in r] for i, r in enumerate(rows)]


def J(*lines):
    return '\n'.join(lines)


# ------------------------------------------------------------------ chữ ⓘ NGUYÊN VĂN (index.vue COLUMN_TIPS)
TIP = {
    'title': 'Tổng hợp chi phí vận chuyển (cước chuyến xe) theo phòng ban và nhân viên kinh doanh trong kỳ, xem được chi '
             'tiết đến từng chuyến xe. Dữ liệu theo quyền xem (tổng công ty / công ty đang chọn / phòng ban quản lý); '
             'không có quyền thì chỉ thấy cước của chính mình.',
    'stt': 'Số thứ tự • Phòng ban đánh số 1, 2, 3… liên tục qua các trang. • Nhân viên KD trong phòng: 1.1, 1.2…; chuyến '
           'xe của nhân viên: 1.1.1… (khi bật Xem chi tiết chuyến xe).',
    'ma': 'Mã nhân viên kinh doanh chịu cước • Hiện ở dòng nhân viên, tên nhân viên ở ô bên cạnh. • Phòng ban và nhân '
          'viên lấy theo thông tin ghi trên bút toán hạch toán chuyến xe.',
    'tg': 'Ngày hạch toán của phiếu hạch toán chuyến xe • Chỉ hiện ở dòng chuyến xe. • Bộ lọc Thời gian lọc theo ngày '
          'hạch toán này.',
    'tt': 'Tải trọng dùng để tính cước • Tải trọng khai trên chuyến xe.',
    'dx': 'Dòng xe dùng để tính cước • Dòng xe khai trên chuyến xe.',
    'xe': 'Xe thực tế chạy chuyến • Hiển thị: Biển số - Tải trọng - Dòng xe của xe được gán cho chuyến.',
    'td': 'Tuyến đường của chuyến xe • Chuyến xe khác chưa chọn tuyến: hiển thị Điểm đi - Điểm đến.',
    'cuoc': 'Chi phí vận chuyển tính cho nhân viên kinh doanh • Dòng chuyến xe = Tổng số tiền (quy đổi VND) các bút toán '
            'của phiếu hạch toán chuyến xe (chuyến chở hàng và chuyến xe khác) ghi cho nhân viên đó, ngày hạch toán '
            'trong kỳ. • Không tính bút toán có mã công việc CLX, XXE, CPK, VCD, CTP hoặc chưa gắn mã công việc. • '
            'Dòng nhân viên = Tổng cước các chuyến của nhân viên; dòng phòng ban = Tổng cước các nhân viên trong phòng; '
            'dòng Tổng cộng = Tổng cước mọi phòng ban (mọi trang).',
    'yc': 'Yêu cầu xuất hàng được chở trên chuyến • Lấy từ các phiếu xuất kho gắn với chuyến xe. • Đang lọc Yêu cầu '
          'xuất hàng / Hợp đồng / Đối tượng chịu phí thì chỉ hiện yêu cầu khớp bộ lọc. • Bấm để mở yêu cầu xuất hàng '
          'ở tab mới.',
    'hd': 'Hợp đồng của yêu cầu xuất hàng trên chuyến • Hợp đồng hãng hoặc hợp đồng dịch vụ bảo hành - sửa chữa gắn '
          'trên yêu cầu xuất hàng. • Bấm để mở hợp đồng ở tab mới.',
    'sc': 'Số phiếu hạch toán chuyến xe • Gồm chuyến xe chở hàng và chuyến xe khác. • Bấm để mở phiếu ở hệ thống ERP '
          '(tab mới).',
}

# ------------------------------------------------------------------ Phần 5 (dò code 02/11/2026)
P5 = [
    ('Vận chuyển', 'Chuyến xe chở hàng (nút Hạch toán chuyến xe lập phiếu hạch toán — nguồn số của báo cáo)',
     'Vận chuyển => Chuyến xe => Chuyến xe chở hàng'),
    ('Vận chuyển', 'Chuyến xe chở hàng chờ hạch toán', 'Vận chuyển => Chuyến xe => Chuyến xe chở hàng chờ hạch toán'),
    ('Vận chuyển', 'Chuyến xe khác (lập, kết thúc chuyến; nút Hạch toán chuyến xe)', 'Vận chuyển => Chuyến xe => Chuyến xe khác'),
    ('Vận chuyển', 'Chuyến xe khác chờ duyệt / chờ hạch toán', 'Vận chuyển => Chuyến xe'),
    ('Vận chuyển', 'Báo cáo tổng hợp chi phí vận chuyển theo lái xe (cùng nguồn phiếu hạch toán chuyến xe)',
     'Vận chuyển => Báo cáo vận chuyển'),
    ('Vận chuyển', 'Báo cáo chi tiết chi phí vận chuyển theo lái xe (cùng nguồn)', 'Vận chuyển => Báo cáo vận chuyển'),
    ('Vận chuyển', 'Báo cáo chi tiết hiệu quả gộp theo chuyến xe (cùng nguồn)', 'Vận chuyển => Báo cáo vận chuyển'),
    ('Vận chuyển', 'Báo cáo hiệu quả gộp xe vận tải (cùng nguồn)', 'Vận chuyển => Báo cáo vận chuyển'),
    ('Vận chuyển', 'Báo cáo chi tiết chuyến xe (cùng nguồn, dùng chung 3 quyền của báo cáo này)',
     'Vận chuyển => Báo cáo vận chuyển'),
    ('Vận chuyển', 'Báo cáo chi phí vận chuyển theo nhân viên kinh doanh (chính màn này, lối vào thứ 2)',
     'Vận chuyển => Báo cáo vận chuyển'),
    ('Bán hàng', 'YC xuất hàng (mở từ cột Yêu cầu xuất hàng)', 'Bán hàng => Yêu cầu => Hàng hóa => YC xuất hàng'),
    ('Bán hàng', 'Danh sách hợp đồng sửa chữa - bảo dưỡng - bảo trì (mở từ cột Hợp đồng)',
     'Bán hàng => Bán dịch vụ => HĐ Sửa chữa - Bảo dưỡng - Bảo trì => Danh sách hợp đồng'),
    ('Quản trị hệ thống', 'Danh sách phân quyền (khối quyền Bán hàng: nhóm "Báo cáo chi phí vận chuyển theo NV kinh doanh"; khối quyền Vận '
     'chuyển: nhóm "Báo cáo vận chuyển")', 'Quản trị hệ thống => Người dùng & phân quyền => Danh sách phân quyền'),
]

FR = []

# 2.1 Xem báo cáo ------------------------------------------------------------------------------------------------
FR.append({
    'ten': 'Xem báo cáo chi phí vận chuyển theo NV kinh doanh',
    'qtc': 'Màn Danh sách, Phân trang, Định dạng số.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh'],
        ['Mô tả', 'Tổng hợp cước vận chuyển đã hạch toán trên phiếu hạch toán chuyến xe (chuyến xe chở hàng và chuyến '
                  'xe khác) theo 3 cấp Phòng ban → Nhân viên kinh doanh → Chuyến xe, trong khoảng Thời gian (ngày hạch '
                  'toán) người dùng chọn. Màn chỉ đọc.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK],
        ['Dòng sự kiện chính', J(
            '1. Người dùng mở màn theo một trong hai đường dẫn menu.',
            '2. Hệ thống hiển thị bộ lọc, bảng trống với dòng "Chọn thời gian để xem báo cáo." (ô Thời gian để trống).',
            '3. Người dùng chọn Thời gian (Từ ngày → Đến ngày).',
            '4. Hệ thống tải báo cáo: dòng Tổng cộng, dòng phòng ban (đậm, nền xám) và dòng nhân viên kinh doanh; phân '
            'trang theo phòng ban, mặc định 10 phòng ban/trang.')],
        ['Dòng sự kiện phụ', J(
            '• Không có số liệu khớp → bảng hiện "Không có dữ liệu phù hợp bộ lọc."',
            '• Trong lúc tải → bảng hiện "Đang tải dữ liệu...".',
            '• Lỗi hệ thống → thông báo "Lỗi khi tải dữ liệu".',
            '• Người dùng chỉ thấy số liệu trong phạm vi quyền (BR-01).')],
    ],
    'menu_them': '',
    'anh': [('03_report', 'Màn báo cáo kỳ 01/01/2026 – 02/11/2026 (chưa bật Xem chi tiết chuyến xe)'),
            ('03c_footer', 'Chân bảng: phân trang theo phòng ban')],
    'ui': ui(UI7, [
        ['Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Hiển thị',
         ['- "Báo cáo chi phí vận chuyển theo nhân viên kinh doanh".', '- Icon ⓘ: “%s”' % TIP['title']]],
        ['Ô Xem chi tiết chuyến xe', 'Checkbox', 'Enable', 'Tích / bỏ tích', 'Bỏ tích',
         '- Tích → tải thêm cấp chuyến xe (mục 2.3); bỏ tích → chỉ còn phòng ban và nhân viên.'],
        ['Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', '- Mở cửa sổ "Chọn trường xuất Excel" (mục 2.4).'],
        ['Bảng chi tiết báo cáo', 'Table/Grid', 'Read-only', '11 cột', 'Theo dữ liệu', [
            '- 3 cấp dòng: dòng phòng ban (đậm, nền xám) → dòng nhân viên kinh doanh → dòng chuyến xe (khi tích Xem chi tiết chuyến xe).',
            '- Dòng Tổng cộng (nền xám, đậm) ở trên cùng.',
            '- Tiêu đề bảng dính khi cuộn; có thanh cuộn ngang ở cả trên và dưới bảng.',
            '- Mỗi tiêu đề cột có icon ⓘ (nội dung ở từng dòng cột bên dưới).']],
        ['Dòng Tổng cộng', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
         ['- Ô cột Cước vận chuyển = tổng cước mọi phòng ban của mọi trang.', '- Bằng 0 thì in "0".',
          '- Không hiện khi bảng không có dòng.']],
        ['Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         ['- Dòng phòng ban: 1, 2, 3… liên tục qua các trang.', '- Dòng nhân viên: 1.1, 1.2…', '- Dòng chuyến xe: 1.1.1…',
          '- Icon ⓘ: “%s”' % TIP['stt']]],
        ['Cột Mã NVKD', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         ['- Dòng nhân viên: mã nhân viên kinh doanh; tên nhân viên ở ô liền bên phải (gộp 5 cột).',
          '- Dòng phòng ban: tên phòng ban gộp từ cột này tới cột Tuyến đường.', '- Dòng chuyến xe: để trống.',
          '- Icon ⓘ: “%s”' % TIP['ma']]],
        ['Cột Thời gian', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu',
         ['- Dòng chuyến xe: ngày hạch toán của phiếu hạch toán chuyến xe.', '- Dòng khác: để trống.',
          '- Icon ⓘ: “%s”' % TIP['tg']]],
        ['Cột Tải trọng tính cước', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         ['- Dòng chuyến xe: tải trọng khai trên chuyến (vd "1.21 tấn"); trống nếu chuyến không khai.',
          '- Icon ⓘ: “%s”' % TIP['tt']]],
        ['Cột Dòng xe tính cước', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         ['- Dòng chuyến xe: dòng xe khai trên chuyến (vd "Xe tải thùng kín").', '- Icon ⓘ: “%s”' % TIP['dx']]],
        ['Cột Xe chạy thực tế', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         ['- Dòng chuyến xe: "Biển số - Tải trọng - Dòng xe" của xe gán cho chuyến; chuyến chưa gán xe thì trống.',
          '- Icon ⓘ: “%s”' % TIP['xe']]],
        ['Cột Tuyến đường', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         ['- Dòng chuyến xe: tên tuyến đường của chuyến.', '- Chuyến xe khác chưa chọn tuyến: "Điểm đi - Điểm đến".',
          '- Icon ⓘ: “%s”' % TIP['td']]],
        ['Cột Cước vận chuyển', 'Table/Grid', 'Read-only', '≥ 0, dạng 1,234,567', 'Theo dữ liệu',
         ['- Có số ở mọi cấp dòng, căn phải, không lẻ; số 0 để trống (trừ dòng Tổng cộng).',
          '- Cách tính từng cấp: mục 2.1.5.', '- Icon ⓘ: “%s”' % TIP['cuoc']]],
        ['Cột Yêu cầu xuất hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         ['- Dòng chuyến xe: mã các yêu cầu xuất hàng chở trên chuyến, mỗi mã 1 dòng.',
          '- Bấm mã → mở màn YC xuất hàng ở tab mới.', '- Icon ⓘ: “%s”' % TIP['yc']]],
        ['Cột Hợp đồng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         ['- Dòng chuyến xe: mã hợp đồng gắn trên các yêu cầu xuất hàng của chuyến, mỗi mã 1 dòng, không lặp.',
          '- Bấm mã → mở hợp đồng ở tab mới (hợp đồng sửa chữa - bảo dưỡng mở màn HRM; hợp đồng hãng mở hệ thống ERP).',
          '- Icon ⓘ: “%s”' % TIP['hd']]],
        ['Cột Số chuyến xe', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
         ['- Dòng chuyến xe: số phiếu hạch toán chuyến xe (vd TPV_HTCXCH_03182, TPHP_HTCXK_00411).',
          '- Bấm số → mở phiếu hạch toán chuyến xe ở tab mới.', '- Icon ⓘ: “%s”' % TIP['sc']]],
        ['Dòng trạng thái bảng', 'Label', 'Hiển thị', '–', '"Chọn thời gian để xem báo cáo."',
         ['- Chưa chọn đủ Thời gian: "Chọn thời gian để xem báo cáo."', '- Đang tải: "Đang tải dữ liệu..."',
          '- Không có số liệu: "Không có dữ liệu phù hợp bộ lọc."']],
        ['Chân bảng phân trang', 'Pagination', 'Enable', '10 / 20 / 50 / 100', '10',
         ['- "Hiển thị a–b / N": N = số phòng ban có số liệu.', '- "Số dòng/trang": số PHÒNG BAN mỗi trang (nhân viên, chuyến đi kèm phòng, không cắt ngang).',
          '- Nút chuyển trang « ‹ 1 2 3 › ».', '- Chỉ hiện khi có số liệu.']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Mở màn hình', 'System', J('After:', '– Ô Thời gian để trống, bảng hiện "Chọn thời gian để xem báo cáo.", không tải số liệu.',
                                    '– Tải danh sách lựa chọn cho ô Công ty / Phòng ban / Nhân viên KD theo phạm vi quyền (BR-01).',
                                    '– Quay lại từ màn khác trong 10 phút: giữ bộ lọc đã chọn; tải lại trang (F5): xoá bộ lọc.')],
        ['Chọn đủ Thời gian', 'Change', J('Before:', '– Đủ cả Từ ngày và Đến ngày mới tải.', 'After:',
                                          '– Tải trang 1: dòng Tổng cộng, phòng ban, nhân viên (và chuyến xe nếu đang tích Xem chi tiết).')],
        ['Chuyển trang / đổi Số dòng/trang', 'Click / Change', J('After:', '– Giữ bộ lọc, tải lại; đổi số dòng thì về trang 1.',
                                                                '– STT phòng ban tiếp nối trang trước (trang 2 bắt đầu từ 11 khi 10 dòng/trang).')],
        ['Rê chuột vào icon ⓘ', 'Hover', J('After:', '– Hiện chú thích nguyên văn như bảng giao diện.')],
        ['Bấm mã ở cột Yêu cầu xuất hàng / Hợp đồng / Số chuyến xe', 'Click', J('After:', '– Mở chứng từ ở tab mới, màn báo cáo giữ nguyên (mục 2.1.6).')],
        ['Lỗi khi tải', 'System', J('After:', '– Thông báo "Lỗi khi tải dữ liệu"; chỉ nhận kết quả của lần lọc mới nhất.')],
    ],
    'them': [
        ('Cách lấy dữ liệu và giải thích chỉ tiêu', [
            ('p', '“Tập dữ liệu” là các bút toán của phiếu hạch toán chuyến xe chở hàng và phiếu hạch toán chuyến xe khác '
                  'có gắn nhân viên kinh doanh chịu cước, ngày hạch toán trong khoảng Thời gian, sau khi bỏ bút toán có mã '
                  'công việc Công lái xe (CLX), Xăng xe (XXE), Chi phí khác (CPK), Vé cầu đường (VCD), Công tác phí (CTP) '
                  'hoặc chưa gắn mã công việc, rồi áp phạm vi quyền (BR-01) và mọi ô lọc (mục 2.2). Ba cấp của bảng và '
                  'dòng Tổng cộng đều cộng từ cùng một tập này nên luôn khớp nhau.'),
            ('table', [['STT', 'Chỉ tiêu / Cột', 'Cách lấy dữ liệu', 'Nội dung icon ⓘ'],
                       ['1', 'Thời điểm số liệu', 'Số liệu tính tại lúc tải. Kỳ báo cáo lấy theo NGÀY HẠCH TOÁN của phiếu hạch toán chuyến xe, tính cả 2 ngày đầu và cuối. Phiếu chưa hạch toán chưa có số.', '—'],
                       ['2', 'Dòng phòng ban', 'Phòng ban ghi trên bút toán (phòng của nhân viên lúc hạch toán), KHÔNG phải phòng hiện tại trong hồ sơ. Chỉ hiện phòng có cước. Xếp theo tên phòng A → Z. Ô Cước vận chuyển = tổng cước các nhân viên của phòng.', '(dùng chung ⓘ cột Cước vận chuyển)'],
                       ['3', 'Dòng nhân viên kinh doanh', 'Nhân viên ghi trên bút toán, trong phòng ban của dòng cha. Xếp theo họ tên A → Z. Ô Cước vận chuyển = tổng cước các chuyến của nhân viên. Nhân viên đổi phòng giữa kỳ hiện ở cả 2 phòng, mỗi phòng phần cước hạch toán khi ở phòng đó.', TIP['ma']],
                       ['4', 'Dòng chuyến xe', 'Mỗi phiếu hạch toán chuyến xe của nhân viên = 1 dòng; xếp ngày hạch toán mới → cũ. Ô Cước vận chuyển = tổng số tiền quy đổi VND các bút toán của phiếu đó ghi cho nhân viên đó (một chuyến chia cho nhiều nhân viên thì mỗi nhân viên thấy phần của mình). Chỉ có khi tích Xem chi tiết chuyến xe.', '(dùng chung ⓘ cột Cước vận chuyển)'],
                       ['5', 'Dòng Tổng cộng', 'Tổng cước của MỌI phòng ban khớp bộ lọc (mọi trang, không chỉ trang đang xem) = tổng các dòng phòng ban. Bằng 0 in "0".', '(dùng chung ⓘ cột Cước vận chuyển)'],
                       ['6', 'Cột Cước vận chuyển', 'Như dòng 2–5; làm tròn hiển thị đến đồng, dấu phẩy ngăn hàng nghìn (1,234,567).', TIP['cuoc']],
                       ['7', 'Cột Thời gian', 'Ngày hạch toán của phiếu (lấy ngày muộn nhất nếu phiếu có bút toán khác ngày).', TIP['tg']],
                       ['8', 'Cột Tải trọng / Dòng xe tính cước', 'Tải trọng, dòng xe khai trên chuyến xe gốc của phiếu hạch toán.', TIP['tt'] + ' | ' + TIP['dx']],
                       ['9', 'Cột Xe chạy thực tế', 'Xe gán cho chuyến: Biển số - Tải trọng - Dòng xe của chính chiếc xe đó.', TIP['xe']],
                       ['10', 'Cột Tuyến đường', 'Tuyến đường của chuyến; chuyến xe khác không chọn tuyến thì "Điểm đi - Điểm đến".', TIP['td']],
                       ['11', 'Cột Yêu cầu xuất hàng', 'Yêu cầu xuất hàng của các phiếu xuất kho gắn với chuyến, không lặp, xếp theo mã. Đang lọc Yêu cầu xuất hàng / Hợp đồng / Đối tượng chịu phí thì chỉ còn yêu cầu khớp lọc.', TIP['yc']],
                       ['12', 'Cột Hợp đồng', 'Hợp đồng hãng hoặc hợp đồng sửa chữa - bảo dưỡng ghi trên các yêu cầu xuất hàng ở cột trước, không lặp.', TIP['hd']],
                       ['13', 'Cột Số chuyến xe', 'Số phiếu hạch toán chuyến xe (chuyến chở hàng: …_HTCXCH_…, chuyến xe khác: …_HTCXK_…).', TIP['sc']],
                       ['14', 'Chân bảng "Hiển thị a–b / N"', 'N = số phòng ban có cước trong tập dữ liệu; a–b = STT phòng ban đầu / cuối trang.', '—'],
                       ['15', 'Ràng buộc khớp số', 'Tổng cộng = tổng dòng phòng ban; dòng phòng ban = tổng dòng nhân viên của phòng; dòng nhân viên = tổng dòng chuyến của nhân viên. File Excel có cùng các số này.', '—']]),
        ]),
        ('Danh sách popup / liên kết mở từ số liệu', [
            ('p', 'Màn không có popup mở từ con số. Các mã chứng từ trên dòng chuyến xe là liên kết mở tab mới để đối chiếu, '
                  'màn báo cáo giữ nguyên bộ lọc và trang đang xem.'),
            ('table', [['STT', 'Bấm vào', 'Popup mở ra', 'Mục đích thiết kế', 'Dữ liệu hiển thị'],
                       ['1', 'Mã ở cột Yêu cầu xuất hàng (dòng chuyến xe)', 'Không phải popup — mở màn YC xuất hàng ở tab mới', 'Chuyến chở hàng của yêu cầu nào, khách nào, hàng gì', 'Đúng yêu cầu xuất hàng đã bấm'],
                       ['2', 'Mã ở cột Hợp đồng (dòng chuyến xe)', 'Không phải popup — mở hợp đồng ở tab mới (HĐ sửa chữa - bảo dưỡng: màn HRM; HĐ hãng: hệ thống ERP)', 'Cước phát sinh cho hợp đồng nào', 'Đúng hợp đồng đã bấm'],
                       ['3', 'Số ở cột Số chuyến xe (dòng chuyến xe)', 'Không phải popup — mở phiếu hạch toán chuyến xe ở tab mới (hệ thống ERP)', 'Kiểm từng bút toán làm nên con số cước của chuyến', 'Phiếu hạch toán đã bấm'],
                       ['4', 'Số cước ở mọi dòng', 'Không bấm được', '—', '—']]),
        ]),
    ],
})

# 2.2 Tìm kiếm và lọc --------------------------------------------------------------------------------------------
FR.append({
    'ten': 'Tìm kiếm và lọc báo cáo',
    'qtc': 'Kịch bản tìm kiếm, Bộ lọc, Dropdown, Datepicker.',
    'gioi_thieu': [
        ['Tên chức năng', 'Tìm kiếm và lọc báo cáo chi phí vận chuyển theo nhân viên kinh doanh'],
        ['Mô tả', 'Chọn kỳ (bắt buộc) và thu hẹp số liệu bằng ô tìm nhanh và 7 ô lọc. Ô Công ty, Phòng ban, Nhân viên KD '
                  'hiện hay ẩn theo phạm vi quyền (BR-01).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đang ở màn báo cáo.'],
        ['Dòng sự kiện chính', J('1. Người dùng chọn Thời gian (bắt buộc).',
                                 '2. Chọn giá trị ở ô chọn → báo cáo tải lại ngay; gõ ô chữ / ô tìm nhanh rồi nhấn Enter hoặc bấm Tìm kiếm.',
                                 '3. Hệ thống áp đồng thời mọi điều kiện, tải lại từ trang 1, dòng Tổng cộng tính lại theo bộ lọc.')],
        ['Dòng sự kiện phụ', J('• Bấm Tìm kiếm khi chưa đủ Thời gian → chữ đỏ "Vui lòng chọn thời gian" dưới ô, không tải.',
                               '• Không chọn được khoảng ngày ngược chiều: lịch làm mờ ngày sau Đến ngày (ô Từ) / trước Từ ngày (ô Đến); gõ tay ngày ngược chiều thì ô không nhận.',
                               '• Đổi Công ty → bỏ chọn Phòng ban, Nhân viên không thuộc công ty mới; đổi Phòng ban → bỏ chọn Nhân viên không thuộc phòng mới.',
                               '• Bấm Làm mới → xoá mọi điều kiện kể cả Thời gian, bảng về "Chọn thời gian để xem báo cáo."',
                               '• Bộ lọc được nhớ 10 phút khi rời màn rồi quay lại; tải lại trang (F5) thì xoá.')],
    ],
    'anh': [('02_filter', 'Lọc bằng ô tìm nhanh "Vinh" (mã / tên nhân viên, phòng ban, số chuyến xe)'),
            ('02_required', 'Bấm Tìm kiếm khi chưa chọn Thời gian')],
    'ui': ui(UI8, [
        ['Ô tìm kiếm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
         ['- Placeholder "Tìm theo mã / tên nhân viên KD, phòng ban hoặc số chuyến xe".',
          '- Tìm gần đúng, không phân biệt hoa thường, theo: mã / họ tên nhân viên kinh doanh, mã / tên phòng ban, số phiếu hạch toán chuyến xe.',
          '- Chỉ lọc khi nhấn Enter hoặc bấm Tìm kiếm.']],
        ['Nút Tìm kiếm', 'Button', 'Enable', '–', '–', '–', ['- Kiểm ô bắt buộc rồi áp mọi điều kiện, tải từ trang 1.']],
        ['Nút Làm mới', 'Button', 'Enable', '–', '–', '–', ['- Xoá mọi điều kiện (kể cả Thời gian), xoá chữ đỏ, bảng về trạng thái chưa chọn kỳ.']],
        ['Nút Ẩn / Hiện tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Đang mở', ['- Đóng / mở khu vực các ô lọc.']],
        ['Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', '–', ['- Chọn ô lọc nào được hiển thị (áp dụng quy tắc chung).']],
        ['Ô Thời gian', 'Datepicker', 'Enable', 'dd/mm/yyyy, Từ ≤ Đến', 'Có', 'Trống', [
            '- 2 ô Từ ngày → Đến ngày, lọc theo ngày hạch toán của phiếu hạch toán chuyến xe, tính cả 2 đầu mút.',
            '- Không chọn được khoảng ngược chiều (lịch làm mờ ngày không hợp lệ; gõ tay thì ô không nhận).',
            '- Thiếu khi bấm Tìm kiếm / Xuất Excel: chữ đỏ "Vui lòng chọn thời gian".', '- Mặc định: trống.']],
        ['Ô Công ty', 'Dropdown', 'Enable / Ẩn', 'Công ty đang hoạt động', 'Không', 'Trống', [
            '- Chỉ hiện với quyền theo tổng công ty.', '- Lọc theo công ty ghi trên bút toán (công ty của nhân viên lúc hạch toán).',
            '- Thu hẹp danh sách ô Phòng ban, Nhân viên KD.']],
        ['Ô Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Phòng ban đang hoạt động, "Mã - Tên"', 'Không', 'Trống', [
            '- Hiện với quyền theo tổng công ty / theo công ty (quyền công ty: chỉ phòng của công ty đang làm việc).',
            '- Lọc theo phòng ban ghi trên bút toán.', '- Thu hẹp danh sách ô Nhân viên KD.']],
        ['Ô Nhân viên KD', 'Dropdown', 'Enable / Ẩn', 'Nhân viên (kể cả đã nghỉ), "Mã - Họ tên"', 'Không', 'Trống', [
            '- Ẩn khi không có quyền nào (người dùng chỉ thấy cước của mình).',
            '- Danh sách theo phạm vi: mọi nhân viên / nhân viên công ty mình / nhân viên các phòng mình quản lý; thu hẹp theo Công ty, Phòng ban đang chọn (theo hồ sơ hiện tại).']],
        ['Ô Số chuyến xe', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
            '- Tìm gần đúng theo số phiếu hạch toán chuyến xe (cả chuyến chở hàng và chuyến xe khác).', '- Lọc khi nhấn Enter / Tìm kiếm.']],
        ['Ô Hợp đồng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
            '- Tìm gần đúng theo mã hợp đồng (hợp đồng hãng, hợp đồng sửa chữa - bảo dưỡng) gắn trên yêu cầu xuất hàng của chuyến VÀ hợp đồng ghi trên bút toán hạch toán (BR-05).',
            '- Lọc khi nhấn Enter / Tìm kiếm.']],
        ['Ô Yêu cầu xuất hàng', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', [
            '- Tìm gần đúng theo mã yêu cầu xuất hàng chở trên chuyến (BR-05).', '- Lọc khi nhấn Enter / Tìm kiếm.']],
        ['Ô Đối tượng chịu phí', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống', [
            '- Lựa chọn:', '  + Nhân viên chịu', '  + Công ty chịu', '- Mặc định: trống (không lọc).',
            '- Giữ chuyến có ít nhất 1 yêu cầu xuất hàng được đánh dấu đúng đối tượng chịu phí (BR-05).']],
        ['Chữ báo lỗi ô bắt buộc', 'Label', 'Hiển thị / Ẩn', '–', '–', 'Ẩn', ['- "Vui lòng chọn thời gian" màu đỏ dưới ô Thời gian; tự tắt khi chọn đủ ngày.']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Chọn / đổi Thời gian, Công ty, Phòng ban, Nhân viên KD, Đối tượng chịu phí', 'Change',
         J('Before:', '– Đổi Công ty / Phòng ban: bỏ chọn Phòng ban / Nhân viên không còn thuộc lựa chọn mới.',
           'During:', '– Thời gian chưa đủ 2 đầu → không tải, bảng hiện "Chọn thời gian để xem báo cáo."',
           'After:', '– Lưu bộ lọc, tải lại báo cáo từ trang 1.')],
        ['Gõ ô tìm nhanh / Số chuyến xe / Hợp đồng / Yêu cầu xuất hàng', 'Change', J('After:', '– Chỉ ghi nhận giá trị, chưa tải; chờ Enter hoặc nút Tìm kiếm.')],
        ['Nhấn Enter / bấm Tìm kiếm', 'Click',
         J('During:', '– Thiếu Thời gian → chữ đỏ "Vui lòng chọn thời gian", không tải.', TRUOC,
           'After:', '– Áp đồng thời mọi điều kiện, tải lại từ trang 1.')],
        ['Bấm Làm mới', 'Click', J('After:', '– Xoá mọi điều kiện và bộ lọc đã nhớ; bảng hiện "Chọn thời gian để xem báo cáo."')],
        ['Bấm Ẩn / Hiện tìm kiếm nâng cao', 'Click', J('After:', '– Đóng / mở khu vực ô lọc.')],
    ],
})

# 2.3 Xem chi tiết chuyến xe -----------------------------------------------------------------------------------
FR.append({
    'ten': 'Xem chi tiết chuyến xe', 'uc': 'uc_chitiet',
    'qtc': 'Màn Xem chi tiết, Phân quyền.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xem chi tiết chuyến xe trong báo cáo'],
        ['Mô tả', 'Tích "Xem chi tiết chuyến xe" để hiện cấp thứ 3 — từng phiếu hạch toán chuyến xe của mỗi nhân viên — '
                  'kèm thông tin xe, tuyến, yêu cầu xuất hàng, hợp đồng và liên kết mở chứng từ.'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đã chọn Thời gian, báo cáo có số liệu.'],
        ['Dòng sự kiện chính', J('1. Người dùng tích ô "Xem chi tiết chuyến xe".',
                                 '2. Hệ thống tải lại trang đang xem, dưới mỗi dòng nhân viên hiện các dòng chuyến xe (STT 1.1.1, 1.1.2…), mới → cũ.',
                                 '3. Người dùng bấm mã yêu cầu xuất hàng / hợp đồng / số chuyến xe để mở chứng từ ở tab mới.')],
        ['Dòng sự kiện phụ', J('• Bỏ tích → tải lại, ẩn cấp chuyến xe; số ở dòng phòng ban, nhân viên, Tổng cộng không đổi.',
                               '• Trạng thái tích quyết định file Excel có cấp chuyến xe hay không (mục 2.4).')],
    ],
    'menu_them': ' => Tích {icon:chk_chitiet}',
    'anh': [('04_detail', 'Báo cáo kỳ 01/10/2026 – 02/11/2026 đã tích Xem chi tiết chuyến xe'),
            ('04b_detail_right', 'Cuộn ngang: các cột Yêu cầu xuất hàng, Hợp đồng, Số chuyến xe (liên kết)')],
    'ui': ui(UI7, [
        ['Ô Xem chi tiết chuyến xe', 'Checkbox', 'Enable', 'Tích / bỏ tích', 'Bỏ tích', ['- Tích: hiện dòng chuyến xe; bỏ tích: ẩn.']],
        ['Dòng chuyến xe', 'Table/Grid', 'Read-only', '–', 'Ẩn', [
            '- STT dạng 1.1.1; cột Mã NVKD để trống.',
            '- Thời gian, Tải trọng tính cước, Dòng xe tính cước, Xe chạy thực tế, Tuyến đường, Cước vận chuyển như mục 2.1.']],
        ['Liên kết Yêu cầu xuất hàng', 'Link', 'Enable', 'Mã YCXH', 'Theo dữ liệu', ['- Chữ xanh gạch chân; bấm → mở màn YC xuất hàng ở tab mới.']],
        ['Liên kết Hợp đồng', 'Link', 'Enable', 'Mã hợp đồng', 'Theo dữ liệu', ['- Bấm → mở hợp đồng ở tab mới.', '- Loại hợp đồng không xác định được: chữ thường, không bấm được.']],
        ['Liên kết Số chuyến xe', 'Link', 'Enable', 'Số phiếu hạch toán', 'Theo dữ liệu', ['- Bấm → mở phiếu hạch toán chuyến xe ở tab mới.']],
    ]),
    'ui_widths': UI7W,
    'events': [
        ['Tích / bỏ tích Xem chi tiết chuyến xe', 'Change', J('After:', '– Tải lại trang đang xem với / không có cấp chuyến xe; giữ bộ lọc và trang.')],
        ['Bấm liên kết chứng từ', 'Click', J('After:', '– Mở chứng từ ở tab mới; màn báo cáo giữ nguyên.')],
    ],
})

# 2.4 Xuất Excel -------------------------------------------------------------------------------------------------
FR.append({
    'ten': 'Xuất báo cáo ra Excel', 'uc': 'uc_xuat',
    'qtc': 'Quy tắc Excel.',
    'gioi_thieu': [
        ['Tên chức năng', 'Xuất báo cáo chi phí vận chuyển theo nhân viên kinh doanh ra Excel'],
        ['Mô tả', 'Xuất toàn bộ số liệu khớp bộ lọc (mọi trang) ra file Excel có cấp như màn hình; người dùng chọn cột và '
                  'thứ tự cột (BR-08).'],
        ['Tác nhân', Q],
        ['Điều kiện ban đầu', DK + '\n3. Đã chọn Thời gian.'],
        ['Dòng sự kiện chính', J('1. Người dùng bấm Xuất Excel.',
                                 '2. Hệ thống mở cửa sổ "Chọn trường xuất Excel", tích sẵn 10 trường.',
                                 '3. Người dùng tích / bỏ tích, kéo ☰ đổi thứ tự rồi bấm Xuất file.',
                                 '4. Hệ thống tải file bao_cao_chi_phi_van_chuyen_theo_nhan_vien_kinh_doanh.xlsx, báo "Xuất Excel thành công", đóng cửa sổ.')],
        ['Dòng sự kiện phụ', J('• Chưa chọn đủ Thời gian → chữ đỏ "Vui lòng chọn thời gian" và thông báo "Vui lòng chọn thời gian", không mở cửa sổ.',
                               '• Bỏ chọn hết trường → nút Xuất file không bấm được.',
                               '• Không có số liệu → vẫn xuất file (tiêu đề, kỳ, tên cột, dòng Tổng cộng trống).',
                               '• Lỗi hệ thống → "Lỗi khi xuất Excel".')],
    ],
    'menu_them': ' => Xuất Excel {icon:btn_xuatexcel}',
    'ghi_chu_layout': 'Modal Chọn trường xuất Excel được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.',
    'anh': [('06_export', 'Cửa sổ Chọn trường xuất Excel')],
    'ui': ui(UI8, [
        ['Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', '–', ['- "Tích chọn trường cần xuất, kéo ☰ để đổi thứ tự cột trong file."']],
        ['Danh sách trường', 'Table/Grid', 'Enable', '10 trường', 'Có ≥ 1', 'Tích cả 10', [
            '- Mã NVKD', '- Thời gian', '- Tải trọng tính cước', '- Dòng xe tính cước', '- Xe chạy thực tế', '- Tuyến đường',
            '- Cước vận chuyển', '- Yêu cầu xuất hàng', '- Hợp đồng', '- Số chuyến xe',
            '- Mỗi trường có ô tích và ☰ kéo đổi vị trí; cột STT luôn có ở đầu file.']],
        ['Nút Chọn tất cả', 'Button', 'Enable', '–', '–', '–', ['- Tích mọi trường.']],
        ['Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', '–', ['- Bỏ tích mọi trường.']],
        ['Dòng đếm', 'Label', 'Hiển thị', '–', '–', 'Đang chọn 10/10 trường', ['- "Đang chọn x/10 trường".']],
        ['Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Enable', ['- Tải file.', '- Không bấm được khi chưa chọn trường nào hoặc đang xuất.']],
        ['Nút Đóng / dấu ×', 'Button', 'Enable', '–', '–', '–', ['- Đóng cửa sổ, không xuất.']],
    ]),
    'ui_widths': UI8W,
    'events': [
        ['Bấm Xuất Excel', 'Click', J('During:', '– Thiếu Thời gian → chữ đỏ + thông báo "Vui lòng chọn thời gian", không mở cửa sổ.',
                                      'After:', '– Mở cửa sổ, tích sẵn 10 trường.')],
        ['Bấm Xuất file', 'Click', J('During:', TRUOC, 'After:',
                                     '– Lấy mọi dòng khớp bộ lọc hiện tại (mọi trang).',
                                     '– File: tiêu đề "BÁO CÁO CHI PHÍ VẬN CHUYỂN THEO NHÂN VIÊN KINH DOANH", dòng "Từ ngày: dd/mm/yyyy đến ngày: dd/mm/yyyy", hàng tên cột, dòng Tổng cộng, rồi cấp Phòng ban (STT 1, đậm) → Nhân viên (STT 1.1, đậm xanh) → chuyến xe (STT 1.1.1, chỉ khi đang tích Xem chi tiết chuyến xe).',
                                     '– Tên phòng / nhân viên gộp ô qua các cột chữ; cột cước dạng số #,##0, số 0 để trống; kẻ khung mọi ô; cuối file khối ký "Người lập".',
                                     '– Thông báo "Xuất Excel thành công", đóng cửa sổ.')],
        ['Bấm Đóng / ×', 'Click', J('After:', '– Đóng cửa sổ.')],
    ],
})

S = {
    'ten': TEN_MAN,
    'menu': [('Bán hàng', 'menu_phanhe'), ('Báo cáo', 'menu_nhom'), ('Vận chuyển', 'menu_nhom2'),
             ('Chi phí vận chuyển theo nhân viên kinh doanh', 'menu_muc')],
    'menu2': [('Vận chuyển', 'menu2_phanhe'), ('Báo cáo vận chuyển', 'menu2_nhom'),
              ('Báo cáo chi phí vận chuyển theo nhân viên kinh doanh', 'menu2_muc')],
    'muc_dich': [
        'Là căn cứ nghiệm thu báo cáo.',
        'Làm rõ nguồn số (bút toán phiếu hạch toán chuyến xe), cách cộng 3 cấp Phòng ban → Nhân viên kinh doanh → Chuyến '
        'xe, các bút toán bị loại, phạm vi số liệu theo quyền và tác dụng của từng ô lọc.',
    ],
    'thuat_ngu': [
        ['NVKD', 'Nhân viên kinh doanh — người được ghi là chịu cước trên bút toán hạch toán chuyến xe.'],
        ['Phiếu hạch toán chuyến xe', 'Chứng từ kế toán ghi nhận chi phí của một chuyến xe chở hàng hoặc chuyến xe khác; mỗi phiếu có nhiều bút toán.'],
        ['Bút toán', 'Một dòng ghi sổ của phiếu hạch toán: số tiền, mã công việc, nhân viên / phòng ban / công ty chịu, hợp đồng, ngày hạch toán.'],
        ['Cước vận chuyển', 'Tổng số tiền (quy đổi VND) các bút toán được tính vào báo cáo.'],
        ['Mã công việc bị loại', 'Công lái xe (CLX), Xăng xe (XXE), Chi phí khác (CPK), Vé cầu đường (VCD), Công tác phí (CTP).'],
        ['YCXH', 'Yêu cầu xuất hàng — hàng được chở trên chuyến (qua phiếu xuất kho gắn với chuyến).'],
        ['Đối tượng chịu phí', 'Nhân viên chịu hoặc Công ty chịu — đánh dấu trên từng yêu cầu xuất hàng của chuyến.'],
        ['Phạm vi số liệu', 'Tập bút toán người dùng được xem theo quyền (tổng công ty / công ty / phòng ban / của mình).'],
    ],
    'quyen_truoc': [
        'Màn hình không chặn ai: mọi người dùng đăng nhập đều mở được (menu không ẩn). Quyền chỉ quyết định PHẠM VI số liệu '
        'và ô lọc nào hiện. Có nhiều quyền thì lấy phạm vi rộng nhất theo thứ tự tổng công ty → công ty → phòng ban.',
        'Phạm vi xét theo công ty / phòng ban / nhân viên GHI TRÊN BÚT TOÁN lúc hạch toán, không theo hồ sơ hiện '
                  'tại (BR-01). Super admin không có phạm vi riêng — theo quyền được gán như người dùng khác.',
    ],
    'quyen_rows': [
        ['Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh theo tổng công ty (khối Bán hàng)', 'Thấy cước của mọi công ty; hiện ô Công ty, Phòng ban, Nhân viên KD.'],
        ['Xem báo cáo vận chuyển theo công ty theo tổng công ty (khối Vận chuyển)', 'Tác dụng như dòng trên (dùng chung với các báo cáo vận chuyển).'],
        ['Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh theo công ty (khối Bán hàng)', 'Chỉ cước ghi cho công ty đang làm việc của người dùng; hiện ô Phòng ban, Nhân viên KD.'],
        ['Xem báo cáo vận chuyển theo công ty (khối Vận chuyển)', 'Tác dụng như dòng trên.'],
        ['Xem báo cáo chi phí vận chuyển theo nhân viên kinh doanh theo phòng ban (khối Bán hàng)', 'Chỉ cước ghi cho các phòng người dùng quản lý và phòng của chính mình; hiện ô Nhân viên KD.'],
        ['Không có quyền nào ở trên', 'Chỉ cước ghi cho chính người dùng; ẩn ô Công ty, Phòng ban, Nhân viên KD.'],
    ],
    'ma_tran': [['Chức năng', 'Tổng công ty', 'Công ty', 'Phòng ban', 'Không quyền']] + [[f, 'Có', 'Có', 'Có', 'Có'] for f in [
        'FR-01 Xem báo cáo', 'FR-02 Tìm kiếm và lọc', 'FR-03 Xem chi tiết chuyến xe', 'FR-04 Xuất báo cáo ra Excel']] + [
        ['Phạm vi số liệu', 'Mọi công ty', 'Công ty đang làm việc', 'Phòng quản lý + phòng mình', 'Cước của mình'],
        ['Ô Công ty', 'Có', 'Không', 'Không', 'Không'],
        ['Ô Phòng ban', 'Có', 'Có', 'Không', 'Không'],
        ['Ô Nhân viên KD', 'Có', 'Có', 'Có', 'Không']],
    'ma_tran_widths': [2.0, 1.1, 1.2, 1.3, 1.0],
    'fr': FR,
    'quy_tac': [
        ('BR-01', 'Phạm vi số liệu theo quyền', [
            '– Không cần quyền để vào màn; quyền chỉ mở rộng phạm vi, ưu tiên tổng công ty → công ty → phòng ban.',
            '– Tổng công ty: mọi bút toán. Công ty: bút toán có công ty ghi trên bút toán = công ty đang làm việc. Phòng ban: bút toán có phòng ban ghi trên bút toán thuộc các phòng người dùng quản lý hoặc phòng của mình. Không quyền: bút toán ghi cho chính người dùng.',
            '– Áp chung cho bảng, dòng Tổng cộng và file Excel; ô lọc không vượt được phạm vi.'], ['Xem báo cáo', 'Tìm kiếm và lọc', 'Xuất Excel']),
        ('BR-02', 'Nguồn số liệu', [
            '– Chỉ bút toán của phiếu hạch toán chuyến xe chở hàng và phiếu hạch toán chuyến xe khác, có gắn nhân viên kinh doanh.',
            '– Loại bút toán có mã công việc Công lái xe (CLX), Xăng xe (XXE), Chi phí khác (CPK), Vé cầu đường (VCD), Công tác phí (CTP) và bút toán chưa gắn mã công việc.',
            '– Số tiền lấy theo giá trị quy đổi VND. Chuyến xe chưa hạch toán chưa có số; phiếu chi trả tiền vận chuyển không làm đổi báo cáo.'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-03', 'Thời gian', [
            '– Bắt buộc; lọc theo ngày hạch toán, tính cả ngày đầu và ngày cuối.',
            '– Không chọn được Từ ngày lớn hơn Đến ngày.',
            '– Mở màn, tải lại trang (F5), bấm Làm mới: Thời gian về trống. Rời màn rồi quay lại trong 10 phút: giữ bộ lọc.'], ['Tìm kiếm và lọc', 'Xuất Excel']),
        ('BR-04', 'Cộng số theo cấp', [
            '– Dòng chuyến xe = tổng bút toán của 1 phiếu hạch toán ghi cho 1 nhân viên trong 1 phòng.',
            '– Dòng nhân viên = tổng các dòng chuyến; dòng phòng ban = tổng các dòng nhân viên; Tổng cộng = tổng mọi phòng ban (mọi trang).',
            '– Phòng ban / nhân viên theo thông tin ghi trên bút toán: nhân viên đổi phòng giữa kỳ hiện ở cả 2 phòng; 1 chuyến chia cho nhiều nhân viên hiện ở từng nhân viên với phần cước của người đó.'], ['Xem báo cáo', 'Xem chi tiết chuyến xe', 'Xuất Excel']),
        ('BR-05', 'Lọc theo chứng từ của chuyến', [
            '– Yêu cầu xuất hàng / Hợp đồng / Đối tượng chịu phí: giữ CẢ chuyến nếu có ít nhất 1 yêu cầu xuất hàng của chuyến khớp; cước vẫn là cước nguyên chuyến của nhân viên.',
            '– Chuyến không có yêu cầu xuất hàng nào bị loại khi dùng 3 ô lọc này (vì vậy "Nhân viên chịu" + "Công ty chịu" có thể nhỏ hơn tổng không lọc).',
            '– Cột Yêu cầu xuất hàng / Hợp đồng chỉ còn chứng từ khớp lọc.',
            '– Ô Hợp đồng còn bắt hợp đồng ghi trên bút toán hạch toán cũng khớp chữ đã nhập.'], ['Tìm kiếm và lọc']),
        ('BR-06', 'Sắp xếp và phân trang', [
            '– Phòng ban theo tên A → Z; nhân viên theo họ tên A → Z; chuyến xe theo ngày hạch toán mới → cũ.',
            '– Phân trang theo phòng ban (mặc định 10, chọn 10 / 20 / 50 / 100); STT phòng ban liên tục qua các trang.'], ['Xem báo cáo']),
        ('BR-07', 'Hiển thị số', [
            '– Định dạng 1,234,567, không lẻ, căn phải.', '– Số 0 để trống, riêng dòng Tổng cộng in "0".'], ['Xem báo cáo', 'Xuất Excel']),
        ('BR-08', 'Xuất Excel', [
            '– Xuất mọi dòng khớp bộ lọc hiện tại (không chỉ trang đang xem), cột theo thứ tự người dùng chọn, STT luôn ở đầu.',
            '– Có cấp chuyến xe khi đang tích Xem chi tiết chuyến xe; không tích thì chỉ phòng ban và nhân viên.',
            '– Tên file bao_cao_chi_phi_van_chuyen_theo_nhan_vien_kinh_doanh.xlsx; số trong file khớp số trên màn.'], ['Xuất Excel']),
    ],
    'phan5': {
        'cau_dan': 'Các màn hình dưới đây sinh ra, dùng chung hoặc được mở từ dữ liệu của báo cáo (phiếu hạch toán chuyến '
                   'xe, quyền xem báo cáo vận chuyển, chứng từ trên dòng chuyến xe).',
        'rows': P5,
    },
}

UML = {
    'actor': 'Người dùng đã đăng nhập',
    'mains': [('FR-01', 'Xem báo cáo chi phí vận chuyển theo NVKD', 'view'), ('FR-04', 'Xuất báo cáo ra Excel', 'io')],
    'subs': [('FR-02', 'Tìm kiếm và lọc báo cáo', 'view'), ('FR-03', 'Xem chi tiết chuyến xe', 'view')],
    'rieng': [('FR-03', 'Xem chi tiết chuyến xe', 'view', 'uc_chitiet'), ('FR-04', 'Xuất báo cáo ra Excel', 'io', 'uc_xuat')],
}


# ------------------------------------------------------------------ dựng (chép khuôn _lib_win.build_srs + mục báo cáo)
def build_srs_report(scr, S, out):
    from qg_writer import QgWriter
    w = QgWriter(L.SRS_TPL, L.SRS_ROLES, body_from=10, cover_replace={'Danh mục quốc gia': S['ten']})

    def img(path, cap, width=6.2):
        w.image(path, width=width, caption=cap)
        L._keep_next(w)

    def sub(text):
        w.raw('sub', text)
        L._keep_with_next(w)

    def menu_segs(items):
        m = []
        for i, (text, icon) in enumerate(items):
            m.append(('Phân hệ ' if i == 0 else ' => ') + text + ' ')
            if icon:
                m.append(scr.ic(icon, 0.24))
        return m

    L.h1_trang_moi(w, 'Phần 1. Giới thiệu')
    w.h2('1 Mục đích')
    w.p('Tài liệu này đặc tả yêu cầu phần mềm cho màn hình %s, nhằm:' % S['ten'])
    for b in S['muc_dich']:
        w.bullet(b)
    w.h2('2 Thuật ngữ và viết tắt')
    w.table([['Thuật ngữ', 'Mô tả']] + S['thuat_ngu'], widths=[1.4, 4.9])

    L.h1_trang_moi(w, 'Phần 2. Phân quyền')
    w.h2('1 Danh sách quyền')
    for p in S['quyen_truoc']:
        w.p(p)
    w.table([['Tên quyền', 'Tác dụng trên màn hình']] + S['quyen_rows'], widths=[2.8, 3.5])
    w.h2('2 Ma trận phân quyền')
    w.table(S['ma_tran'], widths=S.get('ma_tran_widths'))
    for p in S.get('quyen_sau', []):
        w.p(p)

    L.h1_trang_moi(w, 'Phần 3. Đặc tả chi tiết theo từng chức năng')
    w.h2('1 Sơ đồ UML tổng quan')
    img(os.path.join(scr.uml, 'overview.png'), 'Sơ đồ Use Case tổng quan màn %s' % S['ten'], 6.3)
    w.h2('2 Đặc tả chi tiết từng chức năng')
    for i, fr in enumerate(S['fr']):
        assert fr.get('ui') and fr.get('events'), 'FR thiếu bảng giao diện / event'
        n = '2.%d' % (i + 1)
        w.h3('%s %s' % (n, fr['ten']))
        k = 0
        if fr.get('uc'):
            k += 1
            sub('%s.%d Biểu đồ Usecase' % (n, k))
            img(os.path.join(scr.uml, fr['uc'] + '.png'), 'Biểu đồ Use Case — %s' % fr['ten'], 6.2)
        k += 1
        sub('%s.%d Giới thiệu' % (n, k))
        w.clone_texts('qtc', ['Quy tắc chung: ', 'Áp dụng SRS Các quy tắc chung ', L.QTC_LINK,
                              ' - %s Chỉ bổ sung quy tắc riêng của %s.' % (fr['qtc'], S['ten'])])
        w.table([['Mục', 'Nội dung']] + fr['gioi_thieu'], widths=[1.2, 5.1])
        k += 1
        sub('%s.%d Layout màn hình' % (n, k))
        w.p('Đường dẫn màn hình:')
        extra = scr.segs(fr['menu_them']) if fr.get('menu_them') else []
        w.raw('menu_b', 'Menu: ')
        w.raw('menu', menu_segs(S['menu']) + extra)
        w.raw('menu_b', 'Hoặc: ')
        w.raw('menu', menu_segs(S['menu2']) + extra)
        if fr.get('ghi_chu_layout'):
            w.p(fr['ghi_chu_layout'])
        for name, cap in fr.get('anh', []):
            img(scr.shot(name), cap, L._fit_width(scr.shot(name)))
        k += 1
        sub('%s.%d Mô tả chi tiết giao diện' % (n, k))
        w.table(fr['ui'], widths=fr.get('ui_widths'))
        k += 1
        sub('%s.%d Danh sách event và xử lý event' % (n, k))
        w.table([['STT', 'Event', 'Loại event', 'Xử lý event']] +
                [[str(j + 1)] + e for j, e in enumerate(fr['events'])], widths=[0.5, 1.5, 0.8, 3.5])
        for title, items in fr.get('them', []):
            k += 1
            sub('%s.%d %s' % (n, k, title))
            for kind, val in items:
                if kind == 'p':
                    w.p(val)
                else:
                    ncol = len(val[0])
                    widths = {4: [0.55, 1.3, 2.55, 1.9], 5: [0.55, 1.35, 1.5, 1.5, 1.4]}[ncol]
                    w.table(val, widths=widths)

    L.h1_trang_moi(w, 'Phần 4. Quy tắc nghiệp vụ')
    w.p('**Quy tắc áp dụng:** Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung '
        'SRS_Các quy tắc chung_VN_1.0. Phần này chỉ ghi các quy tắc đặc thù của %s; không lặp lại các quy tắc '
        'đã có trong SRS quy tắc chung.' % S['ten'])
    rows = [['STT', 'Mã quy tắc', 'Tên quy tắc', 'Mô tả', 'Phạm vi áp dụng']]
    for i, q in enumerate(S['quy_tac'], 1):
        assert q[0] == 'BR-%02d' % i
        rows.append([str(i), q[0], q[1], '\n'.join(q[2]), '\n'.join(q[3])])
    w.table(rows, widths=[0.55, 0.8, 1.15, 2.75, 1.15])

    p5 = S['phan5']
    L.h1_trang_moi(w, L.PHAN5_TITLE)
    w.p(p5['cau_dan'])
    w.table([['STT', 'Nhóm', 'Màn hình', 'Đường dẫn']] +
            [[str(i + 1)] + list(r) for i, r in enumerate(p5['rows'])], widths=[0.55, 1.0, 2.5, 2.3])

    w.rebuild_toc(levels=(1, 2, 3))
    L._exclude_toc_heading(w)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    L._table_runs_13(w)
    w.save(out)
    L.force_times_new_roman(out)
    return out


if __name__ == '__main__':
    scr = L.Screen(HERE)
    print(L.draw_uml(scr, UML['actor'], UML['mains'], UML['subs'], UML['rieng']))
    print('docx:', build_srs_report(scr, S, OUT))
    if '--no-word' not in sys.argv:
        print('Số trang:', L.word_finalize(OUT, PDF))
        L.check_docx(OUT)
