# -*- coding: utf-8 -*-
"""SRS màn "Tổng hợp tiền về ngân hàng" (phân hệ Tài chính + phân hệ Thông báo) — form chuẩn Danh mục quốc gia +
checklist "Mẫu tài liệu.xlsx" (03/11/2026).

Chạy: python gen_srs.py  → SRS - Tổng hợp tiền về ngân hàng.docx
Khung: srs-documenter (SrsDoc) + ../phieu-theo-form-quoc-gia/CHECKLIST.md. Khuôn thư mục: lookup-product-arrived-notifies.
Nguồn đọc 03/11/2026 (nhánh develop, cả 2 repo):
  FE  pages/finance/bill-income-reports/summarize-money.vue; components/subsystem-menu/{finance.js, lookup.js};
      V2BaseSmartFilterPanel, V2BaseFilterFieldControl, V2BaseDataTable, export-fields-modal, column-customization-modal
      (+ columnCustomizationMixin), filter-customization-modal, filterStateMixin, utils/download-excel, plugins/axios (hết
      phiên); màn đích: pages/finance/bill-adjust-dept-requests/{create.vue, components/BillAdjustDeptRequestForm.vue};
      màn Chi tiết phiếu báo có: pages/finance/bill-income-reports/_id/index.vue + components/BillIncomeReportForm.vue.
  BE  Modules/Finance/{Services/BillIncomeReportSummarizeService.php, Services/BillIncomeReportLookupService.php
      (searchSummarizeCustomers, debtAccountIds), Exports/BillIncomeReportSummarizeExport.php,
      Http/Controllers/V1/BillIncomeReportController.php (summarizeMoney, exportSummarizeMoney, summarizeCustomers, show),
      Entities/BillIncomeReport/{BillIncomeReport, BillIncomeReportDetail, BillIncomeReportAccess},
      Services/BillAdjustDeptLookupService::billIncomeReportDetails, Services/BillAdjustDeptWriteService (cộng tiền đã
      điều chỉnh khi duyệt Phiếu kế toán), Routes/api.php}.
  Tài liệu: .plans/gop-db/finance-bill-income-report/{design.md, plan.md} + spec 2026-08-24 (ưu tiên code khi lệch).
Ảnh: ./thtv_shots (dev-hrm 03/11/2026, DNS Admin, script thtv_shots/_capture/capture.js). Không bật cờ giả nào.
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
HRM = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(HRM, '.claude', 'skills', 'srs-documenter', 'assets'))
sys.path.insert(0, os.path.join(HERE, '..', 'phieu-theo-form-quoc-gia'))
from srs_docx_lib import SrsDoc  # noqa: E402
from srs_split_rows import split_ui_rows  # noqa: E402

TEN = 'Tổng hợp tiền về ngân hàng'
SHOTS = os.path.join(HERE, 'thtv_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # sơ đồ Use Case; HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Quản lý tiền => Thanh toán tiền mặt => Tổng hợp tiền về ngân hàng'
MENU_TC = 'Phân hệ Thông báo => Tra cứu - thông báo => Tổng hợp tiền về'
MENU_TB = 'Phân hệ Thông báo => Thông báo => Tổng hợp tiền về ngân hàng'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Tổng hợp tiền về ngân hàng.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_ND = 'Kế toán / người dùng'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được phân hệ Tài chính hoặc phân hệ Thông báo (màn không '
      'gắn quyền riêng); dữ liệu giới hạn ở phiếu báo có của công ty người dùng đang làm việc.')
DK = ('1. Người dùng đăng nhập thành công.\n'
      '2. Người dùng vào được phân hệ Tài chính hoặc phân hệ Thông báo (không cần quyền riêng để mở màn).\n'
      '3. Tài khoản đã được gắn công ty làm việc (chưa gắn công ty thì màn không có dòng nào).')
M_LOADERR = '“Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”'
M_REJECT = '“Không thể chọn 2 phiếu báo có khác nhau! Vui lòng bỏ chọn dòng cũ trước.”'
M_NONE = '“Vui lòng chọn ít nhất một chi tiết báo có.”'
STATUS_LIST = ['- Chưa điều chỉnh hết công nợ: nhãn vàng (Số tiền chưa điều chỉnh > 0)',
               '- Đã điều chỉnh hết công nợ: nhãn xanh lá (Số tiền chưa điều chỉnh = 0)']
PAGE_ROWS = [
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     ['- Góc trái dưới bảng', '- a–b: khoảng số thứ tự của trang đang xem',
      '- N: tổng số dòng tiền về khớp phạm vi công ty và bộ lọc']),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', '10',
     ['- Mặc định: 10', '- Lựa chọn: 5, 10, 20, 50, 100', '- Đổi giá trị → về trang 1, nạp lại']),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
     ['- Nút về đầu «, lùi ‹, số trang, tiến ›, về cuối »', '- Ở trang đầu nút « ‹ mờ; ở trang cuối nút › » mờ',
      '- Giữ nguyên bộ lọc, sắp xếp và các dòng đang tích khi đổi trang']),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     ['- Trong bảng: “Không có dữ liệu phù hợp bộ lọc.”', '- Dưới bảng: “Không có dòng nào.” thay cho dòng Hiển thị']),
    ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
     ['- ' + M_LOADERR + ' khi máy chủ lỗi', '- Hết phiên đăng nhập: “Phiên đăng nhập đã hết hạn”, chuyển về màn đăng nhập']),
]

d = SrsDoc(out=OUT, menu=MENU, route='/finance/bill-income-reports/summarize-money', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Quản lý tiền': 'menu_quanlytien', 'Thanh toán tiền mặt': 'menu_nhom_tttm',
    'Tổng hợp tiền về ngân hàng': 'menu_muc',
    'Phân hệ Thông báo': 'menu_phanhe_tb', 'Tra cứu - thông báo': 'menu_tracuu', 'Tổng hợp tiền về': 'menu_muc_tracuu',
    'Thông báo': 'menu_thongbao',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Xuất Excel': 'btn_xuatexcel', 'Số báo có': 'link_ma', 'Tích chọn dòng': 'chk_dong',
    'Tạo mới điều chỉnh công nợ': 'btn_taomoi_dc',
}.items()})

UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None):
    """Một chức năng 2.x: (Biểu đồ Usecase) · Giới thiệu · Layout · Mô tả giao diện · Event."""
    d.h3('2.%d %s' % (no, title))
    k = 1
    if usecase:
        d.p('2.%d.%d Biểu đồ Usecase' % (no, k))
        uc(*usecase)
        k += 1
    d.p('2.%d.%d Giới thiệu' % (no, k))
    tail, anchor = rule
    d.rule_ref(tail + ' ' + RIENG, anchor=anchor)
    d.intro_table(**intro)
    k += 1
    d.p('2.%d.%d Layout màn hình' % (no, k))
    extra = layout.pop('extra', [])
    if 'entries' in layout:
        d.p('Đường dẫn màn hình:')
        for m, note in layout['entries']:
            d._menu_para(m)
            d.p(note)
        d.figure(layout['shot'], layout['shot_caption'], width_in=6.2)
    else:
        d.layout(**layout)
    for s, cap in extra:
        d.figure(s, cap, width_in=6.2)
    k += 1
    assert ui and ev, 'Thiếu bảng giao diện / event ở 2.%d' % no
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (no, k))
    d.ui_table(split_ui_rows(ui, UI_OVER, UI_EXPLICIT), **(ui_kw or {}))
    k += 1
    d.p('2.%d.%d Danh sách event và xử lý event' % (no, k))
    d.event_table(ev)


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.doc.add_page_break()  # Mục lục sang trang riêng như bản Drive đã chuẩn hoá
d.h2('Mục lục')
d.doc.paragraphs[-1].alignment = 1  # căn giữa chữ 'Mục lục'
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Tổng hợp tiền về ngân hàng thuộc phân hệ Tài chính (có thêm lối vào '
    'từ phân hệ Thông báo), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng tra cứu các khoản tiền về tài khoản ngân hàng đã ghi nhận trên phiếu báo có, phạm vi '
    'dữ liệu và thao tác chuyển các khoản tiền chưa đối chiếu sang phiếu yêu cầu điều chỉnh công nợ.',
    'Làm rõ điều kiện một dòng tiền về được đưa lên màn (phiếu báo có đã duyệt, tài khoản công nợ 1311 / 1312 / 3311, '
    'chưa đánh dấu không báo tiền về, không phải phiếu thu nhà cung cấp, đúng công ty) và cách tính Số tiền chưa điều '
    'chỉnh, Trạng thái.',
])
d.p('Phạm vi chức năng (7 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Tra cứu: Xem danh sách dòng tiền về; Tìm kiếm và lọc; Cài đặt bộ lọc; Tùy chỉnh cột hiển thị; Xuất Excel theo '
    'trường chọn.',
    'Xem phiếu báo có: bấm Số báo có để mở màn Chi tiết phiếu báo có (màn của chức năng Phiếu báo có).',
    'Tạo mới điều chỉnh công nợ: tích chọn các dòng còn tiền chưa điều chỉnh của CÙNG một phiếu báo có rồi chuyển sang màn '
    'Tạo phiếu yêu cầu điều chỉnh công nợ với các dòng đó điền sẵn.',
    'Không thuộc màn này: màn không có Thêm mới, Chỉnh sửa, Xóa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel và '
    'không có Lịch sử thay đổi. Phiếu báo có được lập / duyệt ở màn Phiếu báo có; nội dung form phiếu yêu cầu điều chỉnh '
    'công nợ theo SRS màn Phiếu yêu cầu điều chỉnh công nợ.',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Kế toán công nợ đối chiếu từng khoản tiền khách chuyển về ngân hàng (theo sao kê) với công nợ: khoản nào đã được gán '
    'đúng khách hàng / hợp đồng, khoản nào còn treo (thường gắn “KHÁCH KHÔNG RÕ”).',
    'Khoản còn tiền chưa điều chỉnh là nguồn để lập phiếu yêu cầu điều chỉnh công nợ, chuyển tiền sang đúng khách hàng / '
    'hợp đồng; khi phiếu kế toán điều chỉnh được duyệt, Số tiền chưa điều chỉnh của dòng giảm tương ứng.',
    'File Excel dùng để gửi đối chiếu / báo cáo nội bộ theo khoảng ngày hạch toán.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Mỗi dòng trên màn là MỘT DÒNG CHI TIẾT của phiếu báo có (một phiếu có nhiều dòng thì hiện nhiều dòng, cùng Số báo có).',
    'Chỉ dòng còn tiền chưa điều chỉnh (> 0) mới tích chọn được; không được chọn dòng của 2 phiếu báo có khác nhau trong '
    'cùng một lần.',
    'Màn chỉ đọc: mọi thay đổi số tiền đã điều chỉnh diễn ra ở luồng Phiếu yêu cầu điều chỉnh công nợ → Phiếu kế toán.',
    'Phạm vi dữ liệu theo công ty của người đang đăng nhập, không phụ thuộc quyền xem phiếu báo có.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu báo có', 'Chứng từ ghi nhận tiền về tài khoản ngân hàng công ty theo sao kê, mã dạng TPE.PBCmmyy.NNNNN (mm/yy = '
                     'tháng / năm, NNNNN = số thứ tự). Vòng đời: Đang tạo → Đã duyệt.'),
    ('Dòng tiền về', 'Một dòng chi tiết của phiếu báo có: một khoản tiền về, kèm khách hàng, diễn giải, tài khoản có, số tiền. '
                     'Là đơn vị hiển thị (1 dòng bảng) của màn này.'),
    ('Số báo có', 'Mã của phiếu báo có chứa dòng tiền về.'),
    ('Ngày hạch toán', 'Ngày hạch toán của phiếu báo có; giờ hiển thị kèm lấy theo thời điểm tạo phiếu (chỉ để tham khảo).'),
    ('Tài khoản công nợ', 'Tài khoản có của dòng thuộc 1311 (Phải thu khách hàng ngắn hạn), 1312 (Phải thu khách hàng dài '
                          'hạn), 3311 (Phải trả người bán). Chỉ dòng có tài khoản này mới lên màn.'),
    ('Số tiền', 'Số tiền quy đổi (VNĐ) của dòng tiền về.'),
    ('Số tiền chưa điều chỉnh', 'Số tiền − tổng tiền đã điều chỉnh công nợ của dòng (cộng dồn mỗi khi phiếu kế toán điều chỉnh '
                                'gắn với dòng được duyệt).'),
    ('Trạng thái dòng', 'Tính từ Số tiền chưa điều chỉnh, không lưu riêng: “Chưa điều chỉnh hết công nợ” (nhãn vàng, còn tiền > '
                        '0, tích chọn được) và “Đã điều chỉnh hết công nợ” (nhãn xanh lá, còn 0, không tích được).'),
    ('Không báo tiền về', 'Cờ đánh trên từng dòng ở màn Chi tiết phiếu báo có; dòng được đánh dấu không lên màn này.'),
    ('KHÁCH KHÔNG RÕ', 'Khách hàng mặc định gán cho khoản tiền chưa rõ của ai; cần chuyển sang đúng khách bằng phiếu yêu cầu '
                       'điều chỉnh công nợ.'),
    ('Phiếu yêu cầu điều chỉnh công nợ', 'Chứng từ đề nghị chuyển công nợ từ khách hàng / hợp đồng này sang khách hàng / hợp '
                                         'đồng khác; lập từ các dòng đã tích ở màn này.'),
    ('Cấu trúc phân cấp', 'Phiếu báo có > dòng tiền về. Màn hiện cấp dòng; các dòng cùng phiếu có chung Số báo có, Ngày hạch '
                          'toán, Người tạo, Ngân hàng, STK ngân hàng.'),
    ('STK', 'Số tài khoản ngân hàng của công ty nhận tiền (ghi trên phiếu báo có).'),
], widths=[2.1, 3.9])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn không gắn quyền riêng: mọi người dùng vào được phân hệ Tài chính hoặc phân hệ Thông báo đều mở được màn và dùng mọi '
    'chức năng. Dữ liệu luôn giới hạn theo công ty của người đang đăng nhập. Riêng chức năng Xem phiếu báo có (mở màn Chi '
    'tiết phiếu báo có) chịu quyền xem của màn Phiếu báo có.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('—', '(Không có quyền thao tác riêng)', 'Xem, tìm kiếm, cài đặt bộ lọc, tùy chỉnh cột, xuất Excel, tích chọn dòng và tạo '
                                            'mới điều chỉnh công nợ: mọi người dùng mở được màn.'),
], widths=[0.8, 1.9, 3.3])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('—', '(Không có quyền riêng — áp cho danh sách, xuất Excel)', 'Dòng tiền về của phiếu báo có ghi công ty = công ty của '
                                                                  'người đăng nhập. Chưa gắn công ty → không có dòng nào.'),
    ('V1', 'Xem tất cả phiếu báo có của tổng công ty (quyền của màn Phiếu báo có)', 'Chỉ ảnh hưởng chức năng Xem phiếu báo '
                                                                                   'có: mở được chi tiết mọi phiếu đã duyệt.'),
    ('V2', 'Xem tất cả phiếu báo có của công ty (quyền của màn Phiếu báo có)', 'Chỉ ảnh hưởng Xem phiếu báo có: mở được chi '
                                                                              'tiết phiếu đã duyệt cùng công ty.'),
    ('—', '(không có V1, V2)', 'Xem phiếu báo có: chỉ mở được chi tiết phiếu do chính mình tạo.'),
], widths=[0.8, 2.6, 2.6])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người dùng có V1', 'Người dùng có V2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ (công ty mình)', '✅ (công ty mình)', '✅ (công ty mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅'),
    ('FR-05 Xuất Excel', '✅ (công ty mình)', '✅ (công ty mình)', '✅ (công ty mình)'),
    ('FR-06 Xem phiếu báo có', '✅', '✅ (phiếu cùng công ty)', '✅ (chỉ phiếu mình tạo)'),
    ('FR-07 Tạo mới điều chỉnh công nợ', '✅', '✅', '✅'),
], widths=[2.4, 1.2, 1.2, 1.2])
d.p('Màn không có chức năng Thêm mới, Chỉnh sửa, Xóa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel và Lịch sử thay đổi '
    'nên ma trận không có các dòng tương ứng. Xuất Excel không gắn quyền riêng: ai xem được danh sách thì xuất được, file chỉ '
    'chứa dòng của công ty mình.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Tài khoản chưa gắn công ty làm việc: bảng “Không có dữ liệu phù hợp bộ lọc.”, file Excel chỉ có dòng “Không có dữ liệu '
    'phù hợp”.',
    'Bấm Số báo có của phiếu không thuộc phạm vi xem phiếu báo có (không có V1 / V2 và không phải người tạo): màn Chi tiết '
    'phiếu báo có báo “Không tải được phiếu báo có”, không hiện dữ liệu.',
    'Gọi thẳng chức năng lấy danh sách / xuất Excel bỏ qua giao diện vẫn chỉ nhận dòng của công ty mình.',
    'Phân hệ / mục menu bị tắt ở màn Cài đặt phân hệ: không thấy mục menu; gõ thẳng đường dẫn thì chuyển sang trang thông báo '
    'chức năng không khả dụng.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Nút / thao tác', 'Hiện khi', 'Vị trí'], [
    ('Tạo mới điều chỉnh công nợ, Xuất Excel, Cấu hình cột hiển thị', 'Luôn hiện', 'Thanh công cụ của bảng'),
    ('Ô tích cột Điều chỉnh công nợ', 'Dòng có Số tiền chưa điều chỉnh > 0; dòng đã điều chỉnh hết để trống', 'Cột Điều chỉnh '
                                                                                                         'công nợ'),
    ('Liên kết Số báo có', 'Mọi dòng', 'Cột Số báo có'),
    ('Cài đặt bộ lọc, Tìm kiếm nâng cao', 'Luôn hiện (khối lọc có 8 tiêu chí)', 'Khối Bộ lọc danh sách'),
], widths=[2.2, 2.6, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_ND, [0, 1, 2])],
    [('FR-01', 'Xem danh sách tiền về', 'view'),
     ('FR-05', 'Xuất Excel', 'io'),
     ('FR-07', 'Tạo mới điều chỉnh công nợ', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-06', 'Xem phiếu báo có', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Tổng hợp tiền về ngân hàng')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách tiền về',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập màn Tổng hợp tiền về ngân hàng và xem danh sách dòng tiền về',
       mota='Mở màn Tổng hợp tiền về ngân hàng và hiển thị bảng các dòng tiền về (dòng chi tiết của phiếu báo có đã duyệt) cần '
            'đối chiếu công nợ của công ty người đăng nhập, kèm số tiền chưa điều chỉnh, trạng thái điều chỉnh, phân trang, '
            'sắp xếp và tổng số dòng. Một phiếu báo có nhiều dòng thì hiện nhiều dòng cùng Số báo có.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng vào menu theo một trong 3 đường dẫn ở mục Layout.\n'
             '2. Hệ thống mở màn “Tổng hợp tiền về ngân hàng” với bộ lọc trống (màn không giữ bộ lọc của lần trước).\n'
             '3. Hệ thống lấy các dòng chi tiết thỏa đủ: phiếu báo có Đã duyệt; loại thu khác Thu nhà cung cấp; tài khoản có '
             'của dòng là 1311, 1312 hoặc 3311; dòng chưa đánh dấu Không báo tiền về; phiếu ghi công ty = công ty người dùng.\n'
             '4. Hệ thống tính Số tiền chưa điều chỉnh = Số tiền − tiền đã điều chỉnh và Trạng thái từng dòng.\n'
             '5. Hệ thống nạp cấu hình cột của người dùng, trả về trang 1 (10 dòng), dòng nhập gần nhất xếp trên, kèm tổng '
             'số dòng; dòng còn tiền có ô tích ở cột Điều chỉnh công nợ.',
       phu='• Không có dòng nào khớp → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”, dưới bảng “Không có dòng nào.”.\n'
           '• Tài khoản chưa gắn công ty → bảng rỗng như trên.\n'
           '• Bấm Số báo có → mở màn Chi tiết phiếu báo có (mục 2.6).\n'
           '• Tích ô ở cột Điều chỉnh công nợ / bấm Tạo mới điều chỉnh công nợ → mục 2.7.\n'
           '• Máy chủ lỗi → hiển thị ' + M_LOADERR + '.\n'
           '• Phiên đăng nhập hết hạn → hiển thị “Phiên đăng nhập đã hết hạn”, điều hướng về màn đăng nhập.',
       dacbiet='Cột mặc định hiển thị (12): STT, Số báo có, Ngày hạch toán, Người tạo, Khách hàng, Ghi chú, Ngân hàng, STK ngân '
               'hàng, Số tiền, Số tiền chưa điều chỉnh, Trạng thái, Điều chỉnh công nợ. Không có cột mặc định ẩn. Cột bắt buộc: '
               'STT, Số báo có (ghim trái, không ẩn, không đổi vị trí). Sắp xếp được: Số báo có, Ngày hạch toán, Ngân hàng, Số '
               'tiền, Số tiền chưa điều chỉnh. Mặc định 10 dòng/trang. Bảng cuộn ngang khi màn hẹp, STT và Số báo có đứng yên.'),
   layout=dict(entries=[
       (MENU, 'Lối vào chính (phân hệ Tài chính). Hiển thị: dòng tiền về của công ty người đăng nhập.'),
       (MENU_TC, 'Lối vào từ phân hệ Thông báo, nhóm Tra cứu - thông báo (nhãn rút gọn “Tổng hợp tiền về”). Mở CÙNG màn, cùng '
                 'phạm vi dữ liệu.'),
       (MENU_TB, 'Lối vào từ phân hệ Thông báo, nhóm Thông báo (đúng vị trí menu của hệ thống ERP). Mở CÙNG màn, cùng phạm vi.')],
       shot=shot('01_list'), shot_caption='Màn Tổng hợp tiền về ngân hàng',
       extra=[(shot('01b_list_done'), 'Dòng Đã điều chỉnh hết công nợ — cột Điều chỉnh công nợ để trống')]),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Tổng hợp tiền về ngân hàng”', '- Ở thanh trên cùng, cũng là tiêu đề tab trình duyệt'),
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', '“Tổng hợp tiền về ngân hàng”', '- Đầu khối bảng, kèm biểu tượng tài liệu'),
       ('Nút Tạo mới điều chỉnh công nợ', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Nút xanh, biểu tượng đổi tiền', '- Bấm → sang màn Tạo phiếu yêu cầu điều chỉnh công nợ với các dòng đang tích (mục 2.7)',
         '- Chưa tích dòng nào → báo ' + M_NONE]),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.5)', '- Khóa và hiện vòng xoay trong lúc đang xuất']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        ['- Biểu tượng cột, chữ gợi ý “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Số thứ tự liên tục giữa các trang', '- Ghim bên trái; khóa trong Tùy chỉnh cột']),
       ('Cột Số báo có', 'Link', 'Read-only', 'TPE.PBCmmyy.NNNNN', 'Theo dữ liệu',
        ['- Mã phiếu báo có chứa dòng', '- Bấm → mở màn Chi tiết phiếu báo có (mục 2.6); chuột phải mở được ở tab mới',
         '- Sắp xếp được', '- Ghim bên trái; khóa trong Tùy chỉnh cột']),
       ('Cột Ngày hạch toán', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        ['- Ngày hạch toán của phiếu', '- Giờ lấy theo thời điểm tạo phiếu (chỉ tham khảo)', '- Sắp xếp được']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Người tạo phiếu báo có, dạng “Họ tên - Mã phòng ban”', '- Không sắp xếp']),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Khách hàng của dòng, dạng “Mã - Tên” (không có mã thì chỉ tên)', '- Trống khi dòng chưa gắn khách hàng',
         '- Chữ dài tự xuống dòng', '- Không sắp xếp']),
       ('Cột Ghi chú', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Diễn giải của dòng tiền về (nội dung chuyển khoản theo sao kê)', '- Chữ dài tự xuống dòng', '- Không sắp xếp']),
       ('Cột Ngân hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mã ngân hàng nhận tiền của phiếu (vd VIETCOMBANK, VIETINBANK, MB)', '- Sắp xếp được, theo mã ngân hàng']),
       ('Cột STK ngân hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Số tài khoản công ty nhận tiền ghi trên phiếu', '- Giữ nguyên số 0 đầu', '- Không sắp xếp']),
       ('Cột Số tiền', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
        ['- Số tiền quy đổi VNĐ của dòng', '- Căn phải, phân cách hàng nghìn bằng dấu phẩy (vd 239,093,640)', '- Sắp xếp được']),
       ('Cột Số tiền chưa điều chỉnh', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
        ['- = Số tiền − tiền đã điều chỉnh công nợ của dòng', '- Căn phải, phân cách hàng nghìn', '- 0 khi đã điều chỉnh hết',
         '- Sắp xếp được']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu', STATUS_LIST + ['- Không sắp xếp']),
       ('Cột Điều chỉnh công nợ', 'Checkbox', 'Enable / Ẩn', '–', 'Bỏ tích',
        ['- Dòng còn tiền chưa điều chỉnh: ô tích', '- Dòng đã điều chỉnh hết: để trống, không tích được',
         '- Tích / bỏ tích theo mục 2.7', '- Bật / tắt, kéo đổi vị trí được trong Tùy chỉnh cột']),
   ] + PAGE_ROWS,
   ev=[('Mở màn hình', 'System',
        'Before:\n– Xác định công ty của người đăng nhập; không có công ty thì không trả dòng nào.\n'
        '– Bộ lọc về mặc định (trống), không khôi phục bộ lọc cũ.\n'
        'During:\n– Nạp cấu hình cột của người dùng và danh sách dòng theo 5 điều kiện cứng (Đã duyệt, không phải Thu nhà cung '
        'cấp, tài khoản 1311 / 1312 / 3311, không đánh dấu Không báo tiền về, đúng công ty).\n'
        '– Tính Số tiền chưa điều chỉnh, Trạng thái, cờ cho tích của từng dòng.\n'
        'After:\n– Hiển thị trang 1, dòng nhập gần nhất xếp trên, kèm tổng số dòng.\n'
        '– Lỗi máy chủ → hiển thị ' + M_LOADERR + '.'),
       ('Bấm Số báo có', 'Click',
        'Before:\n– Mọi dòng đều có liên kết.\n'
        'During:\n– Chuột phải cho phép mở ở tab mới.\n'
        'After:\n– Mở màn Chi tiết phiếu báo có của phiếu chứa dòng (mục 2.6); bộ lọc và dòng đã tích ở màn này không được giữ.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ 5 cột Số báo có, Ngày hạch toán, Ngân hàng, Số tiền, Số tiền chưa điều chỉnh sắp xếp được.\n'
        'During:\n– Lần bấm đầu sắp tăng dần; bấm lại cùng cột đổi giảm dần, bấm tiếp đổi tăng dần; giữ nguyên bộ lọc.\n'
        '– Các dòng cùng giá trị xếp tiếp theo thứ tự nhập dòng mới trước để thứ tự ổn định giữa các trang.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách; biểu tượng mũi tên ở cột đang sắp.'),
       ('Bấm số trang hoặc nút tiến lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc, thứ tự sắp xếp và các dòng đang tích.\n'
        'During:\n– Nạp dữ liệu của trang được chọn.\n'
        'After:\n– Hiển thị trang mới, STT tiếp tục liên tục, dòng “Hiển thị a–b / N” cập nhật; dòng đã tích ở trang trước '
        'vẫn được giữ.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Chọn 1 trong 5, 10, 20, 50, 100.\nDuring:\n– Ghi nhận số dòng mới.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách theo số dòng mới.'),
       ('Phiên đăng nhập hết hạn khi thao tác', 'System',
        'Before:\n– Áp cho mọi lần nạp danh sách.\nDuring:\n– Máy chủ từ chối yêu cầu.\n'
        'After:\n– Hiển thị “Phiên đăng nhập đã hết hạn”, chuyển về màn đăng nhập, không hiện dữ liệu.')])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(ten='Tìm kiếm và lọc danh sách dòng tiền về',
              mota='Thu hẹp danh sách theo số báo có (ô tìm nhanh) và 8 tiêu chí của khối Tìm kiếm nâng cao: Khách hàng, Diễn '
                   'giải, Ngân hàng, STK ngân hàng, Người tạo, Trạng thái, Số tiền (từ – đến), Ngày hạch toán (từ – đến). Kết '
                   'quả luôn nằm trong phạm vi công ty của người dùng.',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng nhập số báo có vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
                    '2. Hoặc bấm Tìm kiếm nâng cao để mở khối tiêu chí, chọn / nhập giá trị một hoặc nhiều tiêu chí.\n'
                    '3. Mọi tiêu chí của khối nâng cao (kể cả ô gõ Diễn giải, Ngân hàng, STK, Số tiền) lọc ngay khi giá trị đổi; '
                    'ô tìm nhanh chỉ lọc khi bấm Tìm kiếm hoặc Enter.\n'
                    '4. Hệ thống quay về trang 1, nạp lại danh sách và tổng số dòng theo toàn bộ tiêu chí đang có.',
              phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh và chiều sắp xếp, nạp lại từ trang 1.\n'
                  '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp bộ lọc.”.\n'
                  '• Ô Khách hàng: gõ từ 2 ký tự mới gợi ý, tối đa 50 khách hàng khớp tên, số điện thoại hoặc mã, khách tạo gần '
                  'nhất xếp trên.\n'
                  '• Tiêu chí bị tắt trong Cài đặt bộ lọc → không hiện ở khối nâng cao.\n'
                  '• Bộ lọc KHÔNG được ghi nhớ: tải lại trang (F5), sang màn khác (kể cả Chi tiết phiếu báo có, Tạo phiếu yêu '
                  'cầu điều chỉnh công nợ) rồi quay lại → bộ lọc về trống.\n'
                  '• Các dòng đã tích vẫn giữ khi đổi bộ lọc, kể cả dòng không còn hiện trong kết quả lọc.',
              dacbiet='Kiểu khớp: ô tìm nhanh (số báo có), Diễn giải, Ngân hàng (mã hoặc tên ngân hàng), STK ngân hàng khớp MỘT '
                      'PHẦN (chuỗi chứa), không phân biệt hoa / thường, tự bỏ khoảng trắng đầu / cuối; ký tự % và _ được hiểu là '
                      'ký tự đại diện. Khách hàng, Người tạo, Trạng thái khớp CHÍNH XÁC. Số tiền so với cột Số tiền (không phải '
                      'Số tiền chưa điều chỉnh), lấy cả 2 biên. Ngày hạch toán lấy trọn 2 ngày biên. Các ô gõ không giới hạn số '
                      'ký tự.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách đang mở Tìm kiếm nâng cao'),
   ui=[('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', '“Bộ lọc danh sách”', '- Kèm biểu tượng phễu lọc'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số báo có...”', '- Tìm theo một phần số báo có', '- Chỉ lọc khi bấm Tìm kiếm hoặc Enter',
         '- Có nút × xóa nhanh khi đã nhập']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp giá trị ô tìm nhanh, về trang 1, nạp lại.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Xóa toàn bộ tiêu chí kể cả ô tìm nhanh, khách hàng đã chọn, chiều sắp xếp', '- Nạp lại từ trang 1',
         '- Không bỏ các dòng đang tích']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Mở / thu gọn khối tiêu chí', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Khách hàng', 'Dropdown', 'Enable', 'Gõ tối thiểu 2 ký tự', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả)', '- Gợi ý dạng “Mã - Tên”, tối đa 50 khách hàng, tìm theo tên / số điện thoại / mã',
         '- Chọn 1 khách hàng → chỉ còn dòng gắn đúng khách hàng đó']),
       ('Diễn giải', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập diễn giải”', '- Một phần diễn giải của dòng (cột Ghi chú)', '- Lọc ngay khi gõ; có nút × xóa']),
       ('Ngân hàng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập mã hoặc tên ngân hàng”', '- Một phần mã hoặc tên ngân hàng nhận tiền của phiếu', '- Lọc ngay khi gõ']),
       ('STK ngân hàng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập số tài khoản ngân hàng”', '- Một phần số tài khoản ghi trên phiếu', '- Lọc ngay khi gõ']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả)', '- Chọn 1 nhân viên; lọc theo người tạo phiếu báo có']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (tất cả), gợi ý “Chọn trạng thái điều chỉnh”', '- Đã điều chỉnh hết công nợ',
         '- Chưa điều chỉnh hết công nợ']),
       ('Số tiền', 'Textbox', 'Enable', '≥ 0', 'Không', 'Trống',
        ['- 1 ô gồm 2 phần “Nhập số tiền từ” → “Nhập số tiền đến”', '- Tự định dạng phân cách hàng nghìn khi gõ',
         '- So với cột Số tiền, lấy cả 2 biên; nhập 1 bên thì chỉ chặn bên đó', '- Enter trong ô → tìm kiếm']),
       ('Ngày hạch toán', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- 1 ô gồm 2 lịch Từ ngày → Đến ngày', '- Lấy trọn cả 2 ngày biên', '- Chọn 1 bên thì chỉ chặn bên đó']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện “Không có dữ liệu phù hợp bộ lọc.” khi không có kết quả.')],
   ev=[('Đổi giá trị một tiêu chí nâng cao', 'Change',
        'Before:\n– Áp cho cả 8 tiêu chí: ô chọn khi chọn giá trị, ô gõ khi mỗi lần đổi nội dung.\n'
        'During:\n– Ghi nhận giá trị mới; bỏ qua lần nạp trùng y hệt điều kiện đang hiển thị.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí đang có.'),
       ('Bấm Tìm kiếm hoặc Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh (và các tiêu chí đang có).\n'
        'During:\n– Máy chủ bỏ khoảng trắng đầu / cuối, so khớp một phần số báo có.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách.'),
       ('Gõ ô Khách hàng', 'Change',
        'Before:\n– Gợi ý khi gõ từ 2 ký tự.\n'
        'During:\n– Tìm khách hàng có tên, số điện thoại hoặc mã chứa chuỗi gõ (tối đa 50, mới tạo trước).\n'
        'After:\n– Hiển thị gợi ý “Mã - Tên”; chọn 1 dòng thì lọc ngay.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Không hỏi xác nhận.\n'
        'During:\n– Đặt lại toàn bộ tiêu chí về trống, bỏ khách hàng đã chọn, bỏ chiều sắp xếp.\n'
        'After:\n– Quay về trang 1 và nạp lại danh sách; các dòng đã tích vẫn giữ.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối tiêu chí đang thu gọn.\nDuring:\n– Mở khối, nhãn nút đổi thành “Ẩn tìm kiếm nâng cao”.\n'
        'After:\n– Bấm lại để thu gọn; giá trị đã chọn vẫn áp dụng.'),
       ('Rời màn hoặc tải lại trang', 'System',
        'Before:\n– Màn chỉ giữ bộ lọc khi chuyển sang đường dẫn con của chính màn (hiện không có).\n'
        'During:\n– Xóa bộ lọc đã ghi tạm trên trình duyệt.\n'
        'After:\n– Lần vào lại màn, bộ lọc về trống.')])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho phép mỗi người dùng tự chọn những tiêu chí lọc muốn thấy ở khối Tìm kiếm nâng cao và sắp xếp lại thứ '
                   'tự của chúng. Cấu hình lưu theo người dùng cho riêng màn này (8 tiêu chí).',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 8 tiêu chí kèm ô tích, theo cấu hình đang lưu.\n'
                    '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình cho người dùng, hiển thị “Cập nhật thành công” và áp ngay lên khối Tìm kiếm nâng cao.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ 8 tiêu chí theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu thay đổi.\n'
                  '• Lưu thất bại → hiển thị “Thao tác thất bại”.\n'
                  '• Ẩn một tiêu chí đang có giá trị → giá trị đó bị xóa khỏi bộ lọc, danh sách nạp lại.\n'
                  '• Tắt bớt còn ≤ 3 ô (tính cả ô tìm nhanh) → các ô bày thẳng trên 1 hàng, nút Tìm kiếm nâng cao ẩn; nút Cài '
                  'đặt bộ lọc vẫn còn để bật lại.',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách tiêu chí', 'Table/Grid', 'Enable', '8 tiêu chí', 'Không', 'Theo cấu hình đã lưu',
        ['- Khách hàng, Diễn giải, Ngân hàng, STK ngân hàng, Người tạo, Trạng thái, Số tiền, Ngày hạch toán',
         '- Mỗi mục đánh số thứ tự 1, 2, 3…', '- Ô tìm nhanh số báo có không nằm trong danh sách (luôn hiện)']),
       ('Ô tích của tiêu chí', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu',
        ['- Tích: tiêu chí hiện ở khối Tìm kiếm nâng cao', '- Bỏ tích: ẩn tiêu chí']),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Kéo để đổi thứ tự tiêu chí.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình cho người dùng hiện tại, đóng cửa sổ, áp ngay.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích lại đủ tiêu chí, thứ tự gốc; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.'),
       ('Khối Tìm kiếm nâng cao sau khi lưu', 'Label', 'Hiển thị', '–', '–', 'Theo cấu hình',
        ['- Chỉ còn các tiêu chí được tích, đúng thứ tự đã kéo', '- Tiêu chí bị ẩn đang có giá trị thì giá trị bị xóa']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”'])],
   ev=[('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Nút hiện khi khối lọc có nhiều hơn 3 ô hoặc đang có tiêu chí bị ẩn.\n'
        'During:\n– Nạp cấu hình đang lưu của người dùng cho màn.\n'
        'After:\n– Mở cửa sổ “Cài đặt bộ lọc”.'),
       ('Kéo đổi vị trí tiêu chí', 'Drag',
        'Before:\n– Kéo bằng tay nắm của dòng.\nDuring:\n– Đổi thứ tự trong cửa sổ.\n'
        'After:\n– Chưa áp lên màn hình cho tới khi bấm Lưu.'),
       ('Bỏ tích một tiêu chí', 'Change',
        'Before:\n– Áp cho mọi tiêu chí.\nDuring:\n– Ghi nhận trạng thái tích trong cửa sổ.\n'
        'After:\n– Chưa áp lên màn hình cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng đang đăng nhập và màn này.\n'
        'During:\n– Ghi cấu hình; lỗi → hiển thị “Thao tác thất bại”.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”; khối Tìm kiếm nâng cao cập nhật ngay; xóa giá trị của tiêu chí vừa ẩn.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Tích lại toàn bộ tiêu chí, đưa thứ tự về thiết kế gốc.\n'
        'After:\n– Chưa lưu; phải bấm Lưu mới có hiệu lực.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ mọi thay đổi chưa lưu.\nAfter:\n– Đóng cửa sổ, khối lọc giữ nguyên.')])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Tùy chỉnh cột của bảng danh sách',
              mota='Cho phép mỗi người dùng bật / tắt và kéo sắp xếp 12 cột của bảng, lưu theo người dùng. Hai cột STT, Số báo '
                   'có bị khóa; cột Điều chỉnh công nợ (ô tích chọn dòng) bật / tắt và đổi vị trí được.',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
                    '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 12 cột kèm ô tích theo cấu hình đang áp dụng.\n'
                    '3. Người dùng tích / bỏ tích, kéo biểu tượng ba gạch để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình, hiển thị “Cập nhật thành công”, vẽ lại bảng.',
              phu='• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, danh sách cột trả về cấu hình đang áp dụng.\n'
                  '• Cột khóa (STT, Số báo có): ô tích xám, không bỏ tích, không kéo được; di chuột hiện “Cột bắt buộc — không thể '
                  'ẩn hoặc đổi vị trí”.\n'
                  '• Ẩn cột Điều chỉnh công nợ → không còn ô tích trên bảng, nút Tạo mới điều chỉnh công nợ chỉ còn báo '
                  + M_NONE + ' (khi chưa có dòng tích từ trước).\n'
                  '• Lưu thất bại → hiển thị “Thao tác thất bại”.\n'
                  '• Cấu hình lưu trên máy chủ theo tài khoản: giữ sau khi tải lại (F5), đổi trình duyệt / máy khác vẫn giữ; tài '
                  'khoản khác không bị ảnh hưởng.\n'
                  '• Đổi cột không làm thay đổi dữ liệu, tổng số dòng, bộ lọc đang áp.',
              dacbiet='Không có cột mặc định ẩn: lần đầu cả 12 cột đều tích. Cột STT, Số báo có ghim trái khi cuộn ngang. Cột '
                      'Xuất Excel chọn ở cửa sổ riêng (mục 2.5), không theo cấu hình cột này.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Tuỳ chỉnh cột”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Tích chọn cột cần hiển thị, kéo ≡ để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', '12 cột', '–', 'Theo cấu hình',
        ['- STT, Số báo có (khóa), Ngày hạch toán, Người tạo, Khách hàng, Ghi chú, Ngân hàng, STK ngân hàng, Số tiền, Số tiền '
         'chưa điều chỉnh, Trạng thái, Điều chỉnh công nợ']),
       ('Ô tích của cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình',
        ['- Tích: cột hiện trên bảng', '- Cột STT, Số báo có: ô tích xám, không bỏ được']),
       ('Biểu tượng ba gạch', 'Icon Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Kéo để đổi vị trí cột', '- Cột STT, Số báo có hiện biểu tượng ổ khóa, không kéo được']),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi cột.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi cột trừ STT, Số báo có.'),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/12 cột”, n = số cột đang tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Ghi cấu hình, đóng cửa sổ, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ; thay đổi chưa lưu bị bỏ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”'])],
   ev=[('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Cấu hình của người dùng đã nạp lúc mở màn; nếu đang nạp thì mở ngay khi nạp xong.\n'
        'During:\n– Liệt kê các cột theo cấu hình đang áp dụng.\n'
        'After:\n– Mở cửa sổ “Tuỳ chỉnh cột”.'),
       ('Kéo biểu tượng ba gạch', 'Drag',
        'Before:\n– Cột STT, Số báo có không kéo được.\nDuring:\n– Đổi thứ tự cột trong cửa sổ.\n'
        'After:\n– Chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bỏ tích một cột', 'Change',
        'Before:\n– Cột STT, Số báo có không cho bỏ tích.\nDuring:\n– Ghi nhận trạng thái trong cửa sổ, cập nhật dòng đếm.\n'
        'After:\n– Chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng và màn này.\n'
        'During:\n– Ghi cấu hình; lỗi → hiển thị “Thao tác thất bại”.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng theo cấu hình mới.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ thay đổi chưa lưu.\n'
        'After:\n– Đóng cửa sổ; lần mở sau hiện lại đúng cấu hình đang áp dụng.')])

# ------------------------------------------------------------ 2.5
fr(5, 'Xuất Excel', usecase=('FR-05', 'Xuất Excel', 'io', A_ND),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất danh sách dòng tiền về ra Excel',
              mota='Người dùng chọn trường và thứ tự cột trong cửa sổ “Chọn trường xuất file” rồi tải file Excel gồm TOÀN BỘ dòng '
                   'tiền về khớp bộ lọc đang áp dụng (không riêng trang đang xem), trong phạm vi công ty của người dùng.',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng lọc danh sách (nếu cần) rồi bấm Xuất Excel trên thanh công cụ của bảng.\n'
                    '2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn cả 10 trường theo thứ tự mặc định.\n'
                    '3. Người dùng tích / bỏ tích, kéo đổi thứ tự, bấm Xuất file.\n'
                    '4. Hệ thống lấy toàn bộ dòng theo bộ lọc + sắp xếp đang áp dụng, dựng file với các cột đã chọn đúng thứ tự.\n'
                    '5. Hệ thống tải file “Tong-hop-tien-ve-ngan-hang.xlsx”, đóng cửa sổ, hiển thị “Xuất Excel thành công.”.',
              phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → không xuất.\n'
                  '• Không có dòng khớp bộ lọc → vẫn tải file gồm logo, tiêu đề, hàng tên cột và 1 dòng “Không có dữ liệu phù '
                  'hợp”.\n'
                  '• Lỗi → hiển thị ' + M_LOADERR + ', cửa sổ giữ nguyên, mở khóa nút.\n'
                  '• Cột đã ẩn bằng Tùy chỉnh cột vẫn được tích sẵn (cửa sổ không theo cấu hình cột của bảng).',
              dacbiet='Cấu trúc file: dòng 1 logo / letterhead công ty của người đăng nhập (rộng bằng bảng); dòng 2 tiêu đề “TỔNG '
                      'HỢP TIỀN VỀ NGÂN HÀNG”; có lọc Ngày hạch toán thì thêm dòng “Từ ngày dd/mm/yyyy đến ngày dd/mm/yyyy” (hoặc '
                      '“Từ ngày …” / “Đến ngày …”); 1 dòng trống; hàng tên cột gồm STT rồi các trường đã chọn đúng thứ tự; dữ liệu '
                      'ngay sau. Số tiền, Số tiền chưa điều chỉnh là ô số định dạng #,##0 (cộng được bằng SUM); STK giữ số 0 đầu; '
                      'diễn giải bắt đầu bằng “=” giữ nguyên chữ. Không giới hạn số dòng. Khóa nút Xuất Excel trong lúc chờ file.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn trường xuất file”', 'Kèm biểu tượng tải xuống và nút (x) đóng.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Tích chọn trường cần xuất, kéo ≡ để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', '10 trường', 'Ít nhất 1', 'Tích cả 10',
        ['- Số báo có, Ngày hạch toán, Người tạo, Khách hàng, Diễn giải, Ngân hàng, STK ngân hàng, Số tiền, Số tiền chưa điều '
         'chỉnh, Trạng thái', '- Trường “Diễn giải” chính là cột Ghi chú trên bảng',
         '- Không có trường Điều chỉnh công nợ (ô tích)']),
       ('Ô tích của trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Tích', 'Tích: trường có trong file.'),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Chữ gợi ý “Kéo để đổi vị trí cột trong file”', '- Thứ tự trong danh sách = thứ tự cột trong file']),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/10 trường”.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi trường.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → tải file, xong thì đóng cửa sổ']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công.”', '- Lỗi: ' + M_LOADERR])],
   ev=[('Bấm Xuất Excel trên thanh công cụ', 'Click',
        'Before:\n– Nút khóa khi đang có lượt xuất chạy.\n'
        'During:\n– Lấy danh sách 10 trường do máy chủ trả cùng danh sách, tích sẵn tất cả.\n'
        'After:\n– Mở cửa sổ “Chọn trường xuất file”.'),
       ('Kéo tay nắm', 'Drag',
        'Before:\n– Áp cho mọi trường.\nDuring:\n– Đổi thứ tự trường.\nAfter:\n– Thứ tự mới là thứ tự cột trong file.'),
       ('Bấm Chọn tất cả hoặc Bỏ chọn hết', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Tích / bỏ tích mọi trường.\n'
        'After:\n– Cập nhật dòng đếm; bỏ hết thì khóa nút Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; chặn bấm lặp khi đang xuất; khóa nút Xuất Excel trong lúc chờ.\n'
        'During:\n– Lấy toàn bộ dòng theo bộ lọc + sắp xếp đang áp dụng, phạm vi công ty của người dùng (bỏ phân trang).\n'
        '– Bỏ qua trường lạ không có trong danh sách; không gửi trường nào thì xuất đủ 10 trường.\n'
        '– Dựng file: letterhead công ty, tiêu đề, dòng khoảng ngày (nếu lọc), STT + các cột đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Tải file “Tong-hop-tien-ve-ngan-hang.xlsx”; đóng cửa sổ; hiển thị “Xuất Excel thành công.”.\n'
        '– Lỗi → ' + M_LOADERR + '; mở khóa nút.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ; lần mở sau tích lại đủ 10 trường.')])

# ------------------------------------------------------------ 2.6
fr(6, 'Xem phiếu báo có', usecase=('FR-06', 'Xem phiếu báo có', 'view', A_ND),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(ten='Mở màn Chi tiết phiếu báo có từ dòng tiền về',
              mota='Bấm Số báo có trên một dòng để mở màn Chi tiết phiếu báo có (thuộc chức năng Phiếu báo có), xem toàn bộ '
                   'phiếu chứa dòng tiền về: thông tin chung, các dòng chi tiết, cờ Không báo tiền về, lịch sử. Màn chi tiết chỉ '
                   'đọc; nội dung đầy đủ theo SRS màn Phiếu báo có.',
              tacnhan=TN + ' Mở được chi tiết khi có quyền Xem tất cả phiếu báo có của tổng công ty / của công ty hoặc là người '
                           'tạo phiếu.',
              dieukien=DK + '\n4. Phiếu nằm trong phạm vi xem phiếu báo có của người dùng (Phần 2).',
              chinh='1. Người dùng bấm Số báo có ở cột Số báo có.\n'
                    '2. Hệ thống chuyển sang màn “Chi tiết phiếu báo có: <Số báo có>”.\n'
                    '3. Hệ thống kiểm tra phạm vi xem phiếu báo có và hiển thị thông tin chung, bảng Chi tiết, khối Đánh dấu không '
                    'báo tiền về, khối Lịch sử ở chế độ chỉ đọc.\n'
                    '4. Người dùng bấm Quay lại để rời màn chi tiết.',
              phu='• Ngoài phạm vi xem phiếu báo có → báo “Không tải được phiếu báo có”, không hiện dữ liệu.\n'
                  '• Phiếu đã bị xóa → báo “Không tìm thấy dữ liệu”.\n'
                  '• Nút Quay lại của màn chi tiết về danh sách Phiếu báo có (không về màn Tổng hợp tiền về); dùng nút Lùi của '
                  'trình duyệt hoặc menu để về lại màn này — bộ lọc, trang, dòng đã tích không được giữ.\n'
                  '• Ở màn chi tiết, tích Không báo tiền về cho một dòng → dòng đó không còn hiện ở màn Tổng hợp tiền về.\n'
                  '• Phiếu còn dòng chưa điều chỉnh hết → màn chi tiết có nút Tạo phiếu yêu cầu điều chỉnh công nợ (mang toàn bộ '
                  'dòng còn tiền của phiếu).',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Số báo có', shot=shot('05_detail'),
               shot_caption='Màn Chi tiết phiếu báo có mở từ Số báo có TPE.PBC1026.00052',
               note='Màn Chi tiết phiếu báo có mở thay màn danh sách (không phải cửa sổ nổi).'),
   ui_kw=dict(required=False),
   ui=[('Liên kết Số báo có', 'Link', 'Enable', '–', 'Theo dữ liệu', ['- Chữ xanh gạch chân ở cột Số báo có', '- Bấm → mở màn chi tiết']),
       ('Tiêu đề màn chi tiết', 'Label', 'Hiển thị', '–', '“Chi tiết phiếu báo có: <Số báo có>”', '- Ở thanh trên cùng'),
       ('Khối Thông tin chung', 'Label', 'Read-only', '–', 'Theo phiếu',
        ['- Góc phải: người tạo - thời điểm tạo', '- Mã phiếu, Loại thu, Tài khoản nợ, Loại tiền, Tỷ giá, Ngày hạch toán, '
         'Người lập, Phòng ban, Ngân hàng, Tài khoản, Chi nhánh, Diễn giải', '- Mọi ô khóa, không sửa']),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo phiếu',
        ['- Mỗi dòng tiền về của phiếu: Số tài khoản có, Tên tài khoản, Khách hàng, Tên khách hàng, Số đơn hàng / Hợp đồng, '
         'Phiếu YC xuất hàng, NVKD, Diễn giải, Số tiền…', '- Gồm cả dòng không lên màn Tổng hợp (tài khoản khác 1311 / 1312 / '
                                                          '3311, đã đánh dấu Không báo tiền về)']),
       ('Khối Đánh dấu không báo tiền về', 'Checkbox', 'Enable', '–', 'Theo dữ liệu',
        ['- Câu hướng dẫn: “Dòng được đánh dấu sẽ KHÔNG xuất hiện ở màn Tổng hợp tiền về ngân hàng (không cần đối chiếu công '
         'nợ). Thay đổi lưu ngay khi tích.”', '- Không hiện với phiếu Thu nhà cung cấp']),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Theo phiếu', '- Lịch sử thay đổi của phiếu báo có'),
       ('Nút Tạo phiếu yêu cầu điều chỉnh công nợ', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Chân màn, chỉ hiện khi phiếu còn dòng chưa điều chỉnh hết', '- Mang mọi dòng còn tiền của phiếu sang màn tạo']),
       ('Nút Sửa, Duyệt, Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        '- Theo quy tắc màn Phiếu báo có; phiếu Đã duyệt (mọi phiếu mở từ màn này) không có các nút này'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', ['- Góc phải chân màn', '- Bấm → về danh sách Phiếu báo có']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Không tải được phiếu báo có”: ngoài phạm vi xem hoặc lỗi máy chủ', '- “Không tìm thấy dữ liệu”: phiếu đã bị xóa']),
       ('Thông báo đánh dấu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công.”', '- Thất bại: “Cập nhật thất bại.” hoặc câu máy chủ trả'])],
   ev=[('Bấm Số báo có', 'Click',
        'Before:\n– Mọi dòng có liên kết; không hỏi xác nhận.\n'
        'During:\n– Chuyển sang màn chi tiết của phiếu; bộ lọc màn Tổng hợp bị xóa.\n'
        'After:\n– Màn chi tiết nạp dữ liệu phiếu.'),
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem: người tạo phiếu, quyền V1, V2 (cùng công ty) hoặc quản trị cao nhất.\n'
        '– Không đủ → “Không tải được phiếu báo có” và dừng.\n'
        'During:\n– Nạp thông tin chung, dòng chi tiết, lịch sử.\n' + ERR + '\n'
        'After:\n– Hiển thị chế độ chỉ đọc; hiện nút Tạo phiếu yêu cầu điều chỉnh công nợ nếu còn dòng chưa điều chỉnh hết.'),
       ('Tích Không báo tiền về ở màn chi tiết', 'Change',
        'Before:\n– Theo quy tắc màn Phiếu báo có; không phải phiếu Thu nhà cung cấp.\n'
        'During:\n– Lưu ngay cờ của dòng.\n' + ERR + '\n'
        'After:\n– “Cập nhật thành công.”; dòng biến mất khỏi màn Tổng hợp tiền về ở lần nạp sau.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Không hỏi xác nhận (màn chỉ đọc).\nDuring:\n– Rời màn chi tiết.\n'
        'After:\n– Về danh sách Phiếu báo có; muốn về màn Tổng hợp thì dùng nút Lùi của trình duyệt hoặc menu (bộ lọc về trống).')])

# ------------------------------------------------------------ 2.7
fr(7, 'Tạo mới điều chỉnh công nợ', usecase=('FR-07', 'Tạo mới điều chỉnh công nợ', 'action', A_ND),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(ten='Chọn dòng tiền về và tạo phiếu yêu cầu điều chỉnh công nợ',
              mota='Người dùng tích các dòng còn tiền chưa điều chỉnh của CÙNG một phiếu báo có rồi bấm Tạo mới điều chỉnh công nợ '
                   'để sang màn “Tạo phiếu yêu cầu điều chỉnh công nợ” với Số phiếu báo có và bảng “Điều chỉnh từ” điền sẵn theo '
                   'các dòng đã chọn. Màn này không ghi dữ liệu; phiếu chỉ được tạo khi người dùng lưu ở màn đích.',
              tacnhan=TN,
              dieukien=DK + '\n4. Có ít nhất 1 dòng Chưa điều chỉnh hết công nợ trong danh sách.',
              chinh='1. Người dùng tích ô ở cột Điều chỉnh công nợ của một hoặc nhiều dòng còn tiền, cùng Số báo có.\n'
                    '2. Hệ thống ghi nhận dòng đã chọn và phiếu báo có của dòng đầu tiên.\n'
                    '3. Người dùng bấm Tạo mới điều chỉnh công nợ.\n'
                    '4. Hệ thống chuyển sang màn “Tạo phiếu yêu cầu điều chỉnh công nợ”, mang theo danh sách dòng đã chọn và đường '
                    'quay lại màn này.\n'
                    '5. Màn đích điền sẵn: Số phiếu báo có; mỗi dòng đã chọn thành 1 dòng “Điều chỉnh từ” (Khách hàng, Hợp đồng / '
                    'Đơn hàng, Số dư cuối kỳ, NVKD, Số tiền = Số tiền chưa điều chỉnh) kèm 1 dòng “Điều chỉnh đến” trống; Loại '
                    'phiếu theo loại thu của phiếu báo có (khóa) nếu có dòng đã rõ khách hàng, còn mọi dòng là KHÁCH KHÔNG RÕ thì '
                    'người dùng tự chọn.\n'
                    '6. Người dùng nhập Diễn giải, khách hàng / hợp đồng “Điều chỉnh đến” và Lưu nháp / Gửi duyệt theo SRS màn '
                    'Phiếu yêu cầu điều chỉnh công nợ; hệ thống ghi nhận hành động tạo phiếu trong lịch sử của phiếu yêu cầu.\n'
                    '7. Lưu xong (hoặc bấm Quay lại) → hệ thống quay về màn Tổng hợp tiền về ngân hàng.',
              phu='• Chưa tích dòng nào mà bấm Tạo mới điều chỉnh công nợ → báo ' + M_NONE + ', đứng yên.\n'
                  '• Đã tích dòng của phiếu A, tích tiếp dòng của phiếu B → báo ' + M_REJECT + ', ô vừa tích trả về không tích.\n'
                  '• Bỏ tích hết dòng → được chọn lại dòng của phiếu khác.\n'
                  '• Dòng Đã điều chỉnh hết công nợ không có ô tích.\n'
                  '• Dòng đã tích vẫn giữ khi đổi trang, đổi số dòng / trang, lọc, Làm mới; mất khi rời màn hoặc tải lại.\n'
                  '• Ở màn đích bấm Quay lại khi chưa nhập gì → về màn này không hỏi; đã nhập → hỏi xác nhận rời trang theo màn đó.\n'
                  '• Màn đích nạp dòng lỗi → báo “Không tải được chi tiết phiếu báo có”.',
              dacbiet='Số tiền chưa điều chỉnh của dòng chỉ giảm khi Phiếu kế toán điều chỉnh công nợ lập từ phiếu yêu cầu được '
                      'duyệt; lưu hoặc gửi duyệt phiếu yêu cầu chưa làm đổi số trên màn này. Chặn chọn 2 phiếu báo có khác nhau '
                      'thực hiện trên giao diện.'),
   layout=dict(menu=MENU + ' => Tích chọn dòng => Tạo mới điều chỉnh công nợ', shot=shot('03_select'),
               shot_caption='Đã tích 2 dòng của phiếu TPE.PBC1026.00052',
               note='Ô tích nằm ở cột Điều chỉnh công nợ ngay trên màn danh sách; nút Tạo mới điều chỉnh công nợ ở thanh công cụ.',
               extra=[(shot('03b_reject'), 'Thông báo khi tích dòng của phiếu báo có khác'),
                      (shot('04_adjust_create'), 'Màn Tạo phiếu yêu cầu điều chỉnh công nợ mở với 2 dòng đã chọn')]),
   ui_kw=dict(required=False),
   ui=[('Ô tích cột Điều chỉnh công nợ', 'Checkbox', 'Enable / Ẩn', '–', 'Bỏ tích',
        ['- Chỉ có ở dòng Số tiền chưa điều chỉnh > 0', '- Tích: chọn dòng; bỏ tích: bỏ chọn',
         '- Không cho tích dòng của phiếu báo có khác phiếu đang chọn']),
       ('Nút Tạo mới điều chỉnh công nợ', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Luôn bấm được', '- Chưa tích dòng → báo lỗi', '- Có dòng tích → chuyển màn']),
       ('Thông báo chọn khác phiếu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- ' + M_REJECT),
       ('Thông báo chưa chọn dòng', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- ' + M_NONE),
       ('Tiêu đề màn đích', 'Label', 'Hiển thị', '–', '“Tạo phiếu yêu cầu điều chỉnh công nợ”', '- Màn của phân hệ Tài chính'),
       ('Loại phiếu (màn đích)', 'Dropdown', 'Enable / Disable', 'Danh sách 2 giá trị', 'Theo phiếu báo có',
        ['- Điều chỉnh công nợ khách hàng / Điều chỉnh công nợ nhà cung cấp', '- Khóa theo loại thu khi có dòng đã rõ khách hàng',
         '- Mọi dòng là KHÁCH KHÔNG RÕ: người dùng tự chọn']),
       ('Số phiếu báo có (màn đích)', 'Textbox', 'Read-only', '–', 'Số báo có của dòng đã chọn', '- Điền sẵn, không sửa'),
       ('Người tạo, Phòng ban (màn đích)', 'Textbox', 'Read-only', '–', 'Người đang đăng nhập', '- Điền sẵn'),
       ('Diễn giải (màn đích)', 'Textarea', 'Enable', '–', 'Trống', '- Bắt buộc, người dùng nhập'),
       ('Bảng Điều chỉnh từ (màn đích)', 'Table/Grid', 'Read-only', '–', 'Theo dòng đã chọn',
        ['- Mỗi dòng đã tích 1 dòng: Khách hàng, Hợp đồng / Đơn hàng, Số dư cuối kỳ, NVKD, Số tiền',
         '- Số tiền = Số tiền chưa điều chỉnh của dòng', '- Dòng “Tổng cộng” = tổng Số tiền các dòng']),
       ('Bảng Điều chỉnh đến (màn đích)', 'Table/Grid', 'Enable', '–', '1 dòng trống mỗi dòng “từ”',
        ['- Khách hàng, Hợp đồng / Đơn hàng, Số tiền bắt buộc', '- Nút Thêm điều chỉnh, Chọn nhanh hợp đồng',
         '- “Số tiền còn lại” = Số tiền dòng “từ” − tổng các dòng “đến”']),
       ('Nút Lưu nháp, Gửi duyệt, Lưu và tiếp tục (màn đích)', 'Button', 'Enable', '–', 'Hiển thị',
        '- Theo SRS màn Phiếu yêu cầu điều chỉnh công nợ'),
       ('Nút Quay lại (màn đích)', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn Tổng hợp tiền về ngân hàng')],
   ev=[('Tích ô một dòng', 'Change',
        'Before:\n– Dòng có Số tiền chưa điều chỉnh > 0 (dòng khác không có ô).\n'
        '– Đã có dòng tích thuộc phiếu báo có khác → hiển thị ' + M_REJECT + ', ô trả về không tích và dừng xử lý.\n'
        'During:\n– Thêm dòng vào danh sách đã chọn; ghi nhận phiếu báo có của dòng.\n'
        'After:\n– Ô hiện dấu tích; dòng giữ trạng thái chọn khi đổi trang / lọc.'),
       ('Bỏ tích một dòng', 'Change',
        'Before:\n– Dòng đang được chọn.\nDuring:\n– Bỏ dòng khỏi danh sách đã chọn.\n'
        'After:\n– Không còn dòng nào → cho phép chọn dòng của phiếu báo có khác.'),
       ('Bấm Tạo mới điều chỉnh công nợ', 'Click',
        'Before:\n– Kiểm tra có ít nhất 1 dòng đã chọn; không có → hiển thị ' + M_NONE + ' và dừng xử lý.\n'
        '– Không kiểm tra quyền riêng.\n'
        'During:\n– Chuyển sang màn Tạo phiếu yêu cầu điều chỉnh công nợ kèm danh sách dòng và đường quay lại màn này.\n'
        'After:\n– Màn đích điền sẵn Số phiếu báo có, Loại phiếu, bảng Điều chỉnh từ; không ghi dữ liệu nào.'),
       ('Màn đích nạp dòng đã chọn', 'System',
        'Before:\n– Có danh sách dòng trên đường dẫn.\n'
        'During:\n– Lấy dòng theo thứ tự nhập, Số tiền = Số tiền − tiền đã điều chỉnh; phiếu báo có lấy theo dòng đầu tiên.\n'
        '– Lỗi → “Không tải được chi tiết phiếu báo có”.\n' + ERR + '\n'
        'After:\n– Chốt mốc “chưa thay đổi” để cảnh báo rời trang chỉ hỏi khi người dùng đã nhập thêm.'),
       ('Lưu phiếu yêu cầu ở màn đích', 'Click',
        'Before:\n– Kiểm tra theo SRS màn Phiếu yêu cầu điều chỉnh công nợ (Diễn giải, Khách hàng, Hợp đồng, Số tiền…).\n'
        'During:\n– Lưu phiếu, sinh mã, ghi nhận hành động tạo phiếu trong lịch sử của phiếu yêu cầu.\n' + ERR + '\n'
        'After:\n– Hiển thị thông báo của màn đó, quay về màn Tổng hợp tiền về ngân hàng; Số tiền chưa điều chỉnh chưa đổi cho '
        'tới khi phiếu kế toán được duyệt.'),
       ('Bấm Quay lại ở màn đích', 'Click',
        'Before:\n– Chưa nhập thêm gì → không hỏi; đã nhập → hỏi xác nhận rời trang.\nDuring:\n– Không lưu.\n'
        'After:\n– Về màn Tổng hợp tiền về ngân hàng, bộ lọc về trống, không còn dòng tích.')])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Tổng hợp tiền về ngân hàng; không lặp lại các quy tắc đã có trong '
           'SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Điều kiện dòng lên màn', [
        '– Phiếu báo có ở trạng thái Đã duyệt; phiếu Đang tạo không hiện.',
        '– Loại thu khác Thu nhà cung cấp (tiền nhà cung cấp hoàn lại không cần đối chiếu công nợ khách hàng).',
        '– Tài khoản có của dòng là 1311, 1312 hoặc 3311.',
        '– Dòng chưa đánh dấu Không báo tiền về.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-02', 'Phạm vi theo công ty', [
        '– Chỉ phiếu ghi công ty = công ty làm việc của người đăng nhập; không phụ thuộc quyền xem phiếu báo có.',
        '– Chưa gắn công ty → không có dòng nào (không lộ phiếu không ghi công ty).',
        '– File Excel cùng phạm vi; letterhead theo công ty người đăng nhập.'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),
    ('BR-03', 'Số tiền chưa điều chỉnh và Trạng thái', [
        '– Số tiền chưa điều chỉnh = Số tiền − tổng tiền đã điều chỉnh của dòng.',
        '– > 0: “Chưa điều chỉnh hết công nợ” (vàng); = 0: “Đã điều chỉnh hết công nợ” (xanh lá).',
        '– Tiền đã điều chỉnh cộng thêm khi Phiếu kế toán điều chỉnh công nợ gắn với dòng được duyệt (phần phát sinh nợ).',
        '– Trạng thái là giá trị tính, lọc Trạng thái dùng cùng công thức.'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),
    ('BR-04', 'Điều kiện chọn dòng', [
        '– Chỉ dòng Chưa điều chỉnh hết công nợ có ô tích.',
        '– Mọi dòng đã chọn phải cùng một phiếu báo có (phiếu yêu cầu điều chỉnh chỉ gắn 1 phiếu báo có).',
        '– Phải chọn ít nhất 1 dòng mới chuyển sang màn tạo phiếu.'],
     ['Tạo mới điều chỉnh công nợ']),
    ('BR-05', 'Dữ liệu chuyển sang phiếu yêu cầu điều chỉnh công nợ', [
        '– Mỗi dòng chọn thành 1 dòng “Điều chỉnh từ” với Số tiền = Số tiền chưa điều chỉnh.',
        '– Loại phiếu khóa theo loại thu của phiếu báo có khi có dòng đã rõ khách hàng; mọi dòng KHÁCH KHÔNG RÕ thì tự chọn.',
        '– Lưu xong / Quay lại trở về màn Tổng hợp tiền về.'],
     ['Tạo mới điều chỉnh công nợ']),
    ('BR-06', 'Hiển thị thời gian', [
        '– Ngày hạch toán hiện dd/mm/yyyy kèm giờ hh:mm lấy theo thời điểm tạo phiếu (ngày hạch toán không lưu giờ).',
        '– Sắp theo Ngày hạch toán thì cùng ngày xếp tiếp theo thời điểm tạo phiếu.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-07', 'Chuẩn hóa dữ liệu tìm kiếm', [
        '– Ô gõ tự bỏ khoảng trắng đầu / cuối; khớp một phần; không phân biệt hoa / thường; ký tự % và _ là ký tự đại diện.',
        '– Ngân hàng khớp mã hoặc tên ngân hàng; Số tiền so với cột Số tiền, lấy cả biên; Ngày hạch toán trọn ngày biên.',
        '– Ô chọn (Khách hàng, Người tạo, Trạng thái) khớp chính xác.'],
     ['Tìm kiếm và lọc']),
    ('BR-08', 'Không ghi nhớ bộ lọc', [
        '– Bộ lọc, trang, chiều sắp xếp, dòng đã tích chỉ tồn tại trong lúc đang ở màn.',
        '– Rời màn hoặc tải lại trang → về mặc định.'],
     ['Tìm kiếm và lọc', 'Tạo mới điều chỉnh công nợ']),
    ('BR-09', 'Tính duy nhất', [
        '– Dòng tiền về không có mã riêng; định danh bằng Số báo có + thứ tự dòng. Số báo có do màn Phiếu báo có sinh, duy nhất.',
        '– Nhiều dòng có thể trùng Số báo có, Số tiền, Ghi chú (sao kê trùng khoản) — vẫn là các dòng khác nhau.'],
     ['Xem danh sách']),
    ('BR-10', 'Liên kết cha – con', [
        '– Phiếu báo có > dòng tiền về; các dòng cùng phiếu dùng chung Số báo có, Ngày hạch toán, Người tạo, Ngân hàng, STK.',
        '– Xóa / hủy duyệt phiếu báo có làm toàn bộ dòng của phiếu biến khỏi màn (thao tác ở màn Phiếu báo có).'],
     ['Xem danh sách', 'Xem phiếu báo có']),
    ('BR-11', 'File Excel', [
        '– Trường do người dùng chọn, đúng thứ tự; tiền là ô số #,##0; STK giữ số 0 đầu; chuỗi bắt đầu bằng “=” giữ nguyên.',
        '– Rỗng vẫn ra file với dòng “Không có dữ liệu phù hợp”.'],
     ['Xuất Excel']),
    ('BR-12', 'Không ghi lịch sử', [
        '– Màn chỉ đọc nên không có Lịch sử thay đổi; lịch sử nằm ở phiếu báo có và phiếu yêu cầu điều chỉnh công nợ.'],
     ['Xem danh sách']),
    ('BR-13', 'Khác hệ thống ERP (có chủ đích)', [
        '– Lọc công ty theo công ty ghi trên phiếu (ERP theo công ty người lập).',
        '– Loại phiếu Thu nhà cung cấp; Xuất Excel chọn trường; tiền trong Excel là ô số; thêm sắp xếp 5 cột.',
        '– Ô Khách hàng tìm theo tên / số điện thoại / mã (không theo mã số thuế).'],
     ['Xem danh sách', 'Tìm kiếm và lọc', 'Xuất Excel']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Màn Tổng hợp tiền về ngân hàng chỉ đọc, không tự ghi dữ liệu. Các màn hình dưới đây cung cấp hoặc dùng dữ liệu dòng tiền về hiển thị trên màn (dòng chi tiết phiếu báo có, số tiền đã điều chỉnh) — điều kiện dòng lên màn ở BR-01, dữ liệu chuyển sang phiếu yêu cầu điều chỉnh công nợ ở BR-05.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Tài chính', 'Phiếu báo có (nguồn dữ liệu của màn: phiếu Đã duyệt, dòng tài khoản 1311 / 1312 / 3311)', 'Tài chính -> Quản lý tiền -> Thanh toán tiền mặt'),
    ('2', 'Tài chính', 'Phiếu yêu cầu điều chỉnh công nợ (lập từ các dòng tiền về đã tích)', 'Tài chính -> Khởi tạo -> Khởi tạo phiếu yêu cầu - Công nợ - Thu - Chi'),
    ('3', 'Tài chính', 'Phiếu kế toán (duyệt thì cộng tiền đã điều chỉnh, giảm Số tiền chưa điều chỉnh)', 'Tài chính -> Sổ tổng hợp'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
