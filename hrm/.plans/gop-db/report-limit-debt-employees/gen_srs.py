# -*- coding: utf-8 -*-
"""SRS màn "Báo cáo hạn mức công nợ nhân viên" (phân hệ Tài chính) — form chuẩn Danh mục quốc gia + checklist
"Mẫu tài liệu.xlsx" + quy định màn BÁO CÁO (bảng Cách lấy dữ liệu, bảng popup, Mục đích thiết kế popup) — 03/11/2026.

Chạy: python gen_srs.py  → SRS - Báo cáo hạn mức công nợ nhân viên.docx
Khung: srs-documenter (SrsDoc) + ../phieu-theo-form-quoc-gia/CHECKLIST.md. Khuôn thư mục: màn chị em ../report-limit-debts.
Nguồn đọc 03/11/2026 (nhánh develop, cả 2 repo):
  FE  pages/finance/report-limit-debt-employees/{index.vue, components/DebtByCustomerModal.vue}; components/subsystem-menu/finance.js;
      V2BaseSmartFilterPanel, V2BaseCompanyDepartmentFilter, V2BaseDataTable (+ ReportInfoTip), V2BaseModal, V2BaseCurrencyInput,
      export-fields-modal (+ exportFieldsMixin), column-customization-modal (+ columnCustomizationMixin),
      filterStateMixin (giữ bộ lọc 10 phút, xóa khi rời màn), utils/export/listExportFile.js (allowEmpty — #11725);
      components/human-components/employee/EmployeeForm.vue (ô Hạn mức công nợ xuất hàng — Phase 2).
  BE  Modules/Finance/{Services/CustomerDebt/ReportLimitDebtEmployeeService.php, Http/Controllers/V1/ReportLimitDebtEmployeeController.php,
      Routes/api.php (nhóm report-limit-debt-employees, không gắn quyền)}; Modules/Human/Http/Requests/{Create,Update}EmployeeRequest.php.
  Tài liệu: .plans/gop-db/report-limit-debt-employees/{design.md, plan.md} + spec 2026-10-14 (hành vi hiện hành SAU #11724–#11730,
      #11928 — ưu tiên code khi lệch).
Ảnh: ./bchmcnnv_shots (dev-hrm 03/11/2026, DNS Admin, script bchmcnnv_shots/_capture/capture.js). Không bật cờ giả nào.
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

TEN = 'Báo cáo hạn mức công nợ nhân viên'
SHOTS = os.path.join(HERE, 'bchmcnnv_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # sơ đồ Use Case; HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Kế toán công nợ => Nhân viên => Báo cáo hạn mức công nợ nhân viên'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Báo cáo hạn mức công nợ nhân viên.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_ND = 'Kế toán công nợ'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được phân hệ Tài chính (màn không gắn quyền riêng, '
      'giữ như hệ thống ERP); xem được nhân viên của mọi công ty.')
DK = ('1. Người dùng đăng nhập thành công.\n'
      '2. Người dùng vào được phân hệ Tài chính (không cần quyền riêng để mở màn).\n'
      '3. Đã có tài khoản nhân viên được khai “Hạn mức công nợ xuất hàng” lớn hơn 0 ở form Tài khoản nhân viên '
      '(chưa có thì báo cáo không có dòng nào).')
M_LOADERR = '“Lỗi khi tải dữ liệu”'
M_DATE = '“Đến ngày phải lớn hơn hoặc bằng Từ ngày.”'
M_EMPTY = '“Không có dữ liệu phù hợp.”'
TARGETS = ['- Trong hạn mức', '- Vượt hạn mức']
# Chữ ⓘ chép NGUYÊN VĂN từ index.vue (COLUMN_TIPS, pageTitleInfo) — nối các dòng bằng " • "
TIP_TITLE = ('Theo dõi công nợ khách hàng hiện tại của từng nhân viên so với hạn mức công nợ xuất hàng được giao, để phát hiện '
             'nhân viên đang vượt hạn mức. Chỉ hiển thị nhân viên đã được khai hạn mức công nợ xuất hàng; công nợ tính đến '
             '"Đến ngày" của bộ lọc (bỏ trống = hôm nay).')
TIP_LIMIT = ('HẠN MỨC CÔNG NỢ XUẤT HÀNG • Mức công nợ khách hàng tối đa nhân viên được phép để tồn khi xuất hàng • '
             'Khai ở Quản trị hệ thống › Người dùng & phân quyền › Tài khoản nhân viên')
TIP_DEBT = ('TỔNG CÔNG NỢ KHÁCH HÀNG HIỆN TẠI • Công thức: Tổng phát sinh Nợ − Tổng phát sinh Có trên các tài khoản con của TK 131 • '
            'Chỉ tính bút toán gắn hợp đồng đầu kỳ / hợp đồng dịch vụ / hợp đồng dự án / hợp đồng thanh lý do nhân viên này tạo '
            '(giữ y ERP) • Tính tới "Đến ngày" của bộ lọc Thời gian (để trống = tới hôm nay) • Vượt hạn mức: Tổng công nợ > Hạn mức '
            '· Trong hạn mức: Tổng công nợ < Hạn mức (bằng nhau không thuộc chỉ tiêu nào) • Bằng tổng cột Công nợ của popup theo '
            'khách hàng (bấm Mã nhân viên)')
POPUP = 'Thông tin chi tiết hạn mức dư nợ nhân viên theo khách hàng'
PAGE_ROWS = [
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     ['- Góc trái dưới bảng', '- a–b: khoảng số thứ tự của trang đang xem',
      '- N: tổng số nhân viên có hạn mức khớp bộ lọc', '- Không có dòng nào thì để trống (không in câu “Không có … nào.”)']),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', '10',
     ['- Mặc định: 10', '- Lựa chọn: 5, 10, 20, 50, 100', '- Đổi giá trị → về trang 1, nạp lại']),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
     ['- Nút về đầu «, lùi ‹, số trang, tiến ›, về cuối »', '- Ở trang đầu nút « ‹ mờ; ở trang cuối nút › » mờ',
      '- Giữ nguyên bộ lọc và chiều sắp xếp khi đổi trang']),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     ['- Trong bảng: ' + M_EMPTY, '- Dưới bảng: không hiện dòng Hiển thị, không hiện câu “Không có nhân viên nào.” (#11928)']),
    ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
     ['- Câu lỗi máy chủ trả, hoặc ' + M_LOADERR + ' khi máy chủ lỗi', '- Khoảng ngày sai: ' + M_DATE,
      '- Hết phiên đăng nhập: “Phiên đăng nhập đã hết hạn”, chuyển về màn đăng nhập']),
]

d = SrsDoc(out=OUT, menu=MENU, route='/finance/report-limit-debt-employees', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Kế toán công nợ': 'menu_ketoancongno', 'Nhân viên': 'menu_nhom_nv',
    'Báo cáo hạn mức công nợ nhân viên': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Xuất Excel': 'btn_xuatexcel', 'Mã nhân viên': 'link_ma',
}.items()})

UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None):
    """Một chức năng 2.x: (Biểu đồ Usecase) · Giới thiệu · Layout · Mô tả giao diện · Event. Trả số mục con kế tiếp."""
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
    return k + 1


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.h2('Mục lục')
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Báo cáo hạn mức công nợ nhân viên thuộc phân hệ Tài chính (chuyển từ '
    'hệ thống ERP: Kế toán › Kế toán Công nợ › Nhân viên), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu báo cáo liệt kê các nhân viên đã được khai “Hạn mức công nợ xuất hàng”, kèm bộ phận, phòng ban, '
    'hạn mức, tổng công nợ khách hàng hiện tại do nhân viên đó phụ trách và chi tiết công nợ tách theo khách hàng.',
    'Ghi rõ các điểm GIỮ Y HỆT hệ thống ERP theo quyết định của người dùng (16/10/2026): cách tính Tổng công nợ (#11727) và '
    'cách cộng dồn số trong cửa sổ chi tiết theo khách hàng (#11729) — để người nghiệm thu không báo nhầm là lỗi.',
])
d.p('Phạm vi chức năng (6 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Tra cứu: Xem báo cáo; Tìm kiếm và lọc; Cài đặt bộ lọc; Tùy chỉnh cột hiển thị; Xuất Excel theo trường chọn.',
    'Xem chi tiết hạn mức dư nợ nhân viên theo khách hàng: bấm Mã nhân viên mở cửa sổ “' + POPUP + '”.',
    'Không thuộc màn này: màn chỉ đọc — không có Thêm mới, Chỉnh sửa, Xóa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel, '
    'In và không có Lịch sử thay đổi. Hạn mức được khai / sửa ở form Tài khoản nhân viên (Quản trị hệ thống › Người dùng & '
    'phân quyền › Tài khoản nhân viên).',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Kế toán công nợ / quản lý kinh doanh xem nhanh nhân viên nào đang có công nợ khách hàng vượt hạn mức được giao để dừng '
    'xuất hàng hoặc đôn đốc thu nợ.',
    'Từ một nhân viên, xem công nợ tách theo khách hàng để biết khoản nợ nằm ở khách nào.',
    'File Excel dùng để gửi đối chiếu / báo cáo nội bộ.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Mỗi dòng báo cáo là MỘT tài khoản nhân viên có “Hạn mức công nợ xuất hàng” > 0, không phân biệt trạng thái tài khoản.',
    'Tổng công nợ khách hàng hiện tại = Tổng phát sinh Nợ − Tổng phát sinh Có trên các tài khoản con của TK 131, CHỈ các bút toán '
    'gắn loại hợp đồng mà hệ thống ERP tính (hợp đồng đầu kỳ, hợp đồng thanh lý, hợp đồng dịch vụ, hợp đồng dự án, hợp đồng loại '
    'cũ) do nhân viên tạo — hợp đồng bán hàng và hợp đồng dịch vụ bảo hành KHÔNG được tính (giữ y ERP).',
    'Bộ lọc Thời gian chỉ dùng “Đến ngày” làm mốc tính công nợ (trống = tới hiện tại); “Từ ngày” không làm đổi số liệu.',
    'Cửa sổ theo khách hàng cộng dồn số qua các khách hàng (giữ y ERP) — số của một khách KHÔNG phải nợ riêng của khách đó.',
    'Màn không có quyền riêng và không bó theo công ty: ai vào được phân hệ Tài chính đều xem được nhân viên mọi công ty.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hạn mức công nợ xuất hàng', 'Mức công nợ khách hàng tối đa một nhân viên được phép để tồn khi xuất hàng. Khai ở ô “Hạn mức '
                                  'công nợ xuất hàng” của form Tài khoản nhân viên (Thêm / Sửa), mỗi tài khoản 1 giá trị.'),
    ('Tổng công nợ khách hàng hiện tại', 'Cột trên báo cáo: Σ phát sinh Nợ − Σ phát sinh Có trên tài khoản con của 131 của các bút '
                                         'toán gắn hợp đồng do nhân viên tạo (theo loại hợp đồng ERP tính), tới Đến ngày.'),
    ('Tài khoản con của 131', 'Các tài khoản có tài khoản cha là 131 (phải thu khách hàng), ví dụ 1311, 1312, 1313; không gồm '
                              'chính tài khoản 131.'),
    ('Hợp đồng ERP tính', 'Hợp đồng đầu kỳ, hợp đồng thanh lý, hợp đồng dịch vụ, hợp đồng dự án, hợp đồng loại cũ của ERP. Thực '
                          'tế dữ liệu hiện có chủ yếu là hợp đồng đầu kỳ.'),
    ('Chỉ tiêu vượt hạn mức', 'Bộ lọc 2 giá trị: Trong hạn mức (Tổng công nợ < Hạn mức), Vượt hạn mức (Tổng công nợ > Hạn mức). '
                              'Bằng nhau không thuộc chỉ tiêu nào.'),
    ('Công nợ (cửa sổ theo khách hàng)', 'Số cộng dồn y ERP: duyệt bút toán theo thứ tự ghi sổ, cộng Nợ trừ Có vào MỘT số lũy kế '
                                         'chung; mỗi khách hàng nhận số lũy kế tại bút toán cuối cùng của khách đó.'),
    ('Mốc Đến ngày', 'Ngày hạch toán của bút toán phải ≤ Đến ngày của bộ lọc Thời gian; trống = toàn bộ bút toán tới hiện tại.'),
    ('Trạng thái bản ghi', 'Dòng báo cáo không có trạng thái riêng (không Khóa / Hoạt động); tài khoản đã khóa hoặc nhân viên đã '
                           'nghỉ vẫn hiện nếu còn hạn mức > 0.'),
    ('Cấu trúc phân cấp', 'Công ty > Phòng ban > Bộ phận > Nhân viên (hạn mức) > công nợ theo khách hàng. Báo cáo hiện cấp nhân '
                          'viên; cửa sổ chi tiết hiện cấp khách hàng.'),
], widths=[2.1, 3.9])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn không gắn quyền riêng (giữ y ERP, người dùng chốt 14/10/2026): mọi người dùng vào được phân hệ Tài chính đều mở được '
    'màn và dùng mọi chức năng. Dữ liệu KHÔNG bó theo công ty của người đăng nhập — xem được nhân viên mọi công ty, lọc Công ty / '
    'Phòng ban / Bộ phận / Nhân viên tùy ý.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('—', '(Không có quyền thao tác riêng)', 'Xem báo cáo, tìm kiếm, cài đặt bộ lọc, tùy chỉnh cột, xuất Excel và xem chi tiết '
                                            'theo khách hàng: mọi người dùng mở được màn.'),
], widths=[0.8, 1.9, 3.3])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('—', '(Không có quyền riêng — áp cho báo cáo, xuất Excel)', 'Mọi tài khoản nhân viên có hạn mức > 0 của mọi công ty; thu hẹp '
                                                                 'bằng bộ lọc Công ty / Phòng ban / Bộ phận / Nhân viên.'),
    ('—', '(Không có quyền riêng — áp cho cửa sổ theo khách hàng)', 'Chỉ mở được nhân viên đang có hạn mức > 0 (đang là dòng của '
                                                                   'báo cáo); nhân viên khác → không tải được dữ liệu.'),
], widths=[0.8, 2.6, 2.6])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Tài khoản không có quyền nào ở Tài chính', 'Tài khoản quản trị (quyền cao nhất)'], [
    ('FR-01 Xem báo cáo', '✅ (mọi công ty)', '✅ (mọi công ty)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅ (cấu hình của riêng mình)', '✅ (cấu hình của riêng mình)'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅ (cấu hình của riêng mình)', '✅ (cấu hình của riêng mình)'),
    ('FR-05 Xuất Excel', '✅', '✅'),
    ('FR-06 Xem chi tiết hạn mức dư nợ nhân viên theo khách hàng', '✅', '✅'),
], widths=[2.6, 1.7, 1.7])
d.p('Màn không có chức năng Thêm mới, Chỉnh sửa, Xóa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel, In và Lịch sử thay đổi '
    'nên ma trận không có các dòng tương ứng. Hai cột ma trận giống hệt nhau vì màn không phân quyền.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Màn không chặn theo quyền: tài khoản không có quyền nào ở phân hệ Tài chính vẫn mở màn và thấy đủ dữ liệu như quản trị.',
    'Mở cửa sổ theo khách hàng cho nhân viên không có hạn mức (gọi thẳng chức năng bỏ qua giao diện): hệ thống trả “Không tìm '
    'thấy dữ liệu”, trên giao diện hiện “Lỗi khi tải dữ liệu”, cửa sổ không có dòng.',
    'Người dùng sửa được hạn mức chỉ khi có quyền ở màn Tài khoản nhân viên (Quản lý tài khoản nhân viên); quyền đó không ảnh '
    'hưởng việc xem báo cáo.',
    'Phân hệ / mục menu bị tắt ở màn Cài đặt phân hệ: không thấy mục menu.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Nút / thao tác', 'Hiện khi', 'Vị trí'], [
    ('Xuất Excel, Cấu hình cột hiển thị', 'Luôn hiện; Xuất Excel khóa trong lúc đang xuất', 'Thanh công cụ của bảng'),
    ('Liên kết Mã nhân viên (mở cửa sổ theo khách hàng)', 'Mọi dòng', 'Cột Mã nhân viên'),
    ('Cài đặt bộ lọc, Tìm kiếm nâng cao', 'Luôn hiện (khối lọc có 7 ô + ô tìm nhanh)', 'Khối Bộ lọc danh sách'),
    ('Icon ⓘ', 'Luôn hiện', 'Cạnh tiêu đề trang; đầu 2 cột Hạn mức công nợ xuất hàng, Tổng công nợ khách hàng hiện tại'),
], widths=[2.2, 2.6, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_ND, [0, 1])],
    [('FR-01', 'Xem báo cáo hạn mức công nợ nhân viên', 'view'),
     ('FR-05', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết hạn mức dư nợ theo khách hàng', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Báo cáo hạn mức công nợ nhân viên')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
k = fr(1, 'Xem báo cáo hạn mức công nợ nhân viên',
       rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
       intro=dict(
           ten='Truy cập màn Báo cáo hạn mức công nợ nhân viên và xem báo cáo',
           mota='Mở màn Báo cáo hạn mức công nợ nhân viên và hiển thị bảng các nhân viên đã được khai hạn mức công nợ xuất hàng '
                '(> 0) của mọi công ty, kèm bộ phận, phòng ban, hạn mức và tổng công nợ khách hàng hiện tại tính theo cách của ERP; '
                'có phân trang, sắp xếp, tổng số dòng và icon ⓘ giải thích. Màn chỉ đọc.',
           tacnhan=TN, dieukien=DK,
           chinh='1. Người dùng vào menu theo đường dẫn ở mục Layout.\n'
                 '2. Hệ thống mở màn “Báo cáo hạn mức công nợ nhân viên”; nếu người dùng vừa rời màn bằng cách tải lại trang '
                 '(F5) dưới 10 phút thì khôi phục bộ lọc, trạng thái khối Tìm kiếm nâng cao đã ghi tạm; ngược lại bộ lọc trống.\n'
                 '3. Hệ thống lấy mọi tài khoản nhân viên có Hạn mức công nợ xuất hàng > 0 (mọi công ty, mọi trạng thái), ghép mã, '
                 'tên, bộ phận, phòng ban từ hồ sơ nhân viên.\n'
                 '4. Với mỗi nhân viên, hệ thống tính Tổng công nợ khách hàng hiện tại = Σ Nợ − Σ Có trên tài khoản con của 131 của '
                 'các bút toán gắn hợp đồng (loại ERP tính) do nhân viên tạo, tới Đến ngày (trống = tới hiện tại); không có bút toán '
                 '→ 0.\n'
                 '5. Hệ thống nạp cấu hình cột của người dùng, sắp tài khoản vừa cập nhật lên đầu, trả về trang 1 (10 dòng) kèm tổng '
                 'số dòng.',
           phu='• Không có nhân viên nào khớp → bảng hiện ' + M_EMPTY + ', dưới bảng không có dòng Hiển thị.\n'
               '• Chưa tài khoản nào được khai hạn mức → bảng rỗng như trên.\n'
               '• Bấm Mã nhân viên → mở cửa sổ ' + POPUP + ' (mục 2.6).\n'
               '• Rê chuột / bấm icon ⓘ cạnh tiêu đề hoặc đầu cột → hiện khung giải thích (mục 2.1.5).\n'
               '• Máy chủ lỗi → hiển thị câu lỗi máy chủ trả hoặc ' + M_LOADERR + '.\n'
               '• Phiên đăng nhập hết hạn → hiển thị “Phiên đăng nhập đã hết hạn”, điều hướng về màn đăng nhập.',
           dacbiet='Cột mặc định hiển thị (7): STT, Mã nhân viên, Tên nhân viên, Bộ phận, Phòng ban, Hạn mức công nợ xuất hàng, '
                   'Tổng công nợ khách hàng hiện tại. Không có cột mặc định ẩn. Cột bắt buộc: STT, Mã nhân viên (ghim trái, không '
                   'ẩn, không đổi vị trí). Sắp xếp được: Mã nhân viên, Tên nhân viên, Hạn mức công nợ xuất hàng, Tổng công nợ khách '
                   'hàng hiện tại. Mặc định 10 dòng/trang. Lọc, tính công nợ, sắp xếp, cắt trang tính trên toàn bộ dòng.'),
       layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn Báo cáo hạn mức công nợ nhân viên',
                   note='Lối vào duy nhất (phân hệ Tài chính). Hiển thị: nhân viên có hạn mức công nợ xuất hàng > 0, mọi công ty.',
                   extra=[(shot('00_menu_panel'), 'Mục Báo cáo hạn mức công nợ nhân viên trong menu Kế toán công nợ › Nhân viên'),
                          (shot('01b_tip'), 'Icon ⓘ ở đầu cột Tổng công nợ khách hàng hiện tại'),
                          (shot('01c_empty'), 'Trạng thái rỗng khi không có dòng khớp')]),
       ui_kw=dict(required=False),
       ui=[
           ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Báo cáo hạn mức công nợ nhân viên”',
            ['- Ở thanh trên cùng, cũng là tiêu đề tab trình duyệt', '- Icon ⓘ: “' + TIP_TITLE + '”']),
           ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', '“Báo cáo hạn mức công nợ nhân viên”', '- Đầu khối bảng, kèm biểu tượng tài liệu'),
           ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
            ['- Nút viền xanh lá, biểu tượng Excel', '- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.5)',
             '- Khóa trong lúc đang xuất; bên cạnh hiện tiến độ “Đã tải x/y dòng…”, “Đang dựng file x/y dòng…”']),
           ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
            ['- Biểu tượng cột, chữ gợi ý “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4)']),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Số thứ tự liên tục giữa các trang', '- Ghim bên trái; khóa trong Tùy chỉnh cột', '- Không sắp xếp']),
           ('Cột Mã nhân viên', 'Link', 'Read-only', '–', 'Theo dữ liệu',
            ['- Mã hồ sơ nhân viên, chữ xanh gạch chân',
             '- Bấm → mở cửa sổ ' + POPUP + ' (mục 2.6)',
             '- Sắp xếp được (so tự nhiên)', '- Ghim bên trái; khóa trong Tùy chỉnh cột']),
           ('Cột Tên nhân viên', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Họ tên nhân viên', '- Chữ dài tự xuống dòng', '- Sắp xếp được']),
           ('Cột Bộ phận', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Bộ phận ghi trên hồ sơ nhân viên', '- Trống khi hồ sơ chưa gắn bộ phận', '- Không sắp xếp']),
           ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Phòng ban ghi trên hồ sơ nhân viên', '- Chữ dài tự xuống dòng', '- Không sắp xếp']),
           ('Cột Hạn mức công nợ xuất hàng', 'Table/Grid', 'Read-only', '> 0', 'Theo dữ liệu',
            ['- Hạn mức khai ở form Tài khoản nhân viên', '- Căn phải, phân cách hàng nghìn bằng dấu phẩy',
             '- Icon ⓘ: “' + TIP_LIMIT + '”', '- Sắp xếp được']),
           ('Cột Tổng công nợ khách hàng hiện tại', 'Table/Grid', 'Read-only', 'Số, có thể âm', 'Theo dữ liệu',
            ['- Công nợ tính theo cách ERP tới Đến ngày (mục 2.1.5)', '- Căn phải, phân cách hàng nghìn; 0 vẫn hiện “0”; số âm có '
             'dấu “-”', '- Icon ⓘ: “' + TIP_DEBT + '”', '- Sắp xếp được']),
           ('Icon ⓘ', 'Icon Button', 'Enable', '–', 'Hiển thị',
            ['- Rê chuột hoặc bấm → hiện khung giải thích, rời chuột thì ẩn', '- Bấm icon ở đầu cột KHÔNG làm sắp xếp cột']),
       ] + PAGE_ROWS,
       ev=[('Mở màn hình', 'System',
            'Before:\n– Không kiểm tra quyền riêng; không bó theo công ty.\n'
            '– Có bộ lọc ghi tạm dưới 10 phút (tải lại trang) → khôi phục; quá hạn hoặc vừa rời sang màn khác → bộ lọc trống; '
            'chiều sắp xếp đã ghi không còn hợp lệ thì bỏ.\n'
            'During:\n– Nạp cấu hình cột của người dùng và danh sách chỉ tiêu cho ô lọc.\n'
            '– Lấy tài khoản nhân viên có hạn mức > 0; tính Tổng công nợ khách hàng hiện tại theo cách ERP tới Đến ngày.\n'
            'After:\n– Hiển thị trang 1 (10 dòng), tài khoản cập nhật gần nhất ở trên, kèm “Hiển thị a–b / N”.\n'
            '– Lỗi máy chủ → hiển thị câu lỗi máy chủ trả hoặc ' + M_LOADERR + '.'),
           ('Bấm Mã nhân viên', 'Click',
            'Before:\n– Mọi dòng đều có liên kết; không kiểm tra quyền riêng.\n'
            '– Lấy Từ ngày, Đến ngày đang chọn ở bộ lọc Thời gian (nếu có).\n'
            'During:\n– Mở cửa sổ theo khách hàng và nạp công nợ của nhân viên (chi tiết mục 2.6).\n'
            'After:\n– Cửa sổ hiện trên màn báo cáo; bộ lọc, trang, sắp xếp của báo cáo giữ nguyên khi đóng cửa sổ.'),
           ('Rê chuột / bấm icon ⓘ', 'Click',
            'Before:\n– Icon cạnh tiêu đề trang và ở đầu 2 cột tiền.\n'
            'During:\n– Hiện khung giải thích ngay dưới icon (nguyên văn ở mục 2.1.5).\n'
            'After:\n– Rời chuột / bấm chỗ khác → khung ẩn; không đổi sắp xếp, không nạp lại.'),
           ('Bấm tiêu đề cột có sắp xếp', 'Click',
            'Before:\n– Chỉ 4 cột Mã nhân viên, Tên nhân viên, Hạn mức công nợ xuất hàng, Tổng công nợ khách hàng hiện tại sắp xếp '
            'được.\n'
            'During:\n– Lần bấm đầu sắp tăng dần; bấm lại cùng cột đổi giảm dần; giữ nguyên bộ lọc.\n'
            '– Chữ so tự nhiên không phân biệt hoa / thường; giá trị bằng nhau xếp tiếp theo thứ tự tạo tài khoản.\n'
            'After:\n– Quay về trang 1 và nạp lại; biểu tượng mũi tên ở cột đang sắp.'),
           ('Bấm số trang hoặc nút tiến lùi', 'Click',
            'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\n'
            'During:\n– Nạp dữ liệu của trang được chọn.\n'
            'After:\n– Hiển thị trang mới, STT tiếp tục liên tục, dòng “Hiển thị a–b / N” cập nhật.'),
           ('Đổi Số dòng/trang', 'Change',
            'Before:\n– Chọn 1 trong 5, 10, 20, 50, 100.\nDuring:\n– Ghi nhận số dòng mới.\n'
            'After:\n– Quay về trang 1 và nạp lại danh sách theo số dòng mới.'),
           ('Phiên đăng nhập hết hạn khi thao tác', 'System',
            'Before:\n– Áp cho mọi lần nạp báo cáo.\nDuring:\n– Máy chủ từ chối yêu cầu.\n'
            'After:\n– Hiển thị “Phiên đăng nhập đã hết hạn”, chuyển về màn đăng nhập, không hiện dữ liệu.')])

d.p('2.1.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('Bảng dưới mô tả cách hệ thống lấy từng cột số liệu và nội dung icon ⓘ (nguyên văn trên giao diện). “Tập dữ liệu” là các tài '
    'khoản nhân viên có Hạn mức công nợ xuất hàng > 0 (mọi công ty, mọi trạng thái) sau khi áp ô tìm nhanh, Công ty, Phòng ban, '
    'Bộ phận, Nhân viên, Chỉ tiêu vượt hạn mức.')
d.data_table([
    ('Tiêu đề “Báo cáo hạn mức công nợ nhân viên”', 'Mục đích báo cáo, không có số liệu.', TIP_TITLE),
    ('Dòng “Hiển thị a–b / N”', 'N = số tài khoản nhân viên của tập dữ liệu (mỗi tài khoản 1 dòng). Đổi Đến ngày có thể đổi N khi '
                                'đang lọc Chỉ tiêu (vì công nợ đổi).', '—'),
    ('Cột Hạn mức công nợ xuất hàng', 'Giá trị ô “Hạn mức công nợ xuất hàng” của tài khoản nhân viên ở form Tài khoản nhân viên. Chỉ '
                                      'tài khoản có giá trị > 0 mới lên báo cáo.', TIP_LIMIT),
    ('Cột Tổng công nợ khách hàng hiện tại', 'Σ phát sinh Nợ − Σ phát sinh Có (số tiền đã quy đổi VND) của các bút toán: (1) trên '
                                             'tài khoản con của 131 (không gồm 131); (2) gắn hợp đồng đầu kỳ, hợp đồng thanh lý, hợp '
                                             'đồng dịch vụ, hợp đồng dự án hoặc hợp đồng loại cũ của ERP; (3) hợp đồng đó do nhân '
                                             'viên này tạo; (4) ngày hạch toán ≤ Đến ngày (trống = tới hiện tại). Hợp đồng bán hàng, '
                                             'hợp đồng dịch vụ bảo hành không tính (giữ y ERP, #11727). Không có bút toán → 0. Có '
                                             'thể âm.', TIP_DEBT),
    ('Ràng buộc khớp số', 'Cột Tổng công nợ = số lũy kế cuối cùng của cửa sổ theo khách hàng (dòng của khách hàng có bút toán ghi sổ '
                          'sau cùng) khi cửa sổ không lọc. Cột này KHÔNG bằng tổng cột Công nợ của cửa sổ vì cửa sổ cộng dồn y ERP '
                          '(#11729) — dòng cuối của chữ ⓘ còn ghi “Bằng tổng cột Công nợ của popup” là chưa khớp cách tính.', '—'),
])
k += 1
d.p('2.1.%d Danh sách popup mở từ số liệu' % k)
d.popup_table([
    ('Mã nhân viên ở cột Mã nhân viên (mọi dòng)', POPUP + ' (mục 2.6)',
     'Công nợ của nhân viên nằm ở những khách hàng nào để đôn đốc đúng khách',
     'Công nợ cộng dồn theo khách hàng của nhân viên, tính tới Đến ngày của bộ lọc Thời gian (trống = toàn bộ); không có dòng tổng'),
])

# ------------------------------------------------------------ 2.2
k = fr(2, 'Tìm kiếm và lọc',
       rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
       intro=dict(ten='Tìm kiếm và lọc báo cáo hạn mức công nợ nhân viên',
                  mota='Thu hẹp báo cáo theo mã / tên nhân viên (ô tìm nhanh) và các tiêu chí của khối Tìm kiếm nâng cao: Thời gian, '
                       'Công ty, Phòng ban, Bộ phận, Nhân viên, Chỉ tiêu vượt hạn mức. Thời gian chỉ dùng Đến ngày làm mốc tính công '
                       'nợ; Công ty – Phòng ban – Bộ phận – Nhân viên chọn theo cấp, mọi công ty.',
                  tacnhan=TN, dieukien=DK,
                  chinh='1. Người dùng nhập mã hoặc tên nhân viên vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
                        '2. Hoặc bấm Tìm kiếm nâng cao để mở khối tiêu chí, chọn giá trị một hoặc nhiều tiêu chí.\n'
                        '3. Các ô chọn của khối nâng cao lọc ngay khi giá trị đổi; ô Thời gian chỉ áp khi đã chọn đủ cả Từ ngày và Đến '
                        'ngày (hoặc xóa cả hai); ô tìm nhanh chỉ lọc khi bấm Tìm kiếm hoặc Enter.\n'
                        '4. Đổi ô cấp trên (Công ty → Phòng ban → Bộ phận) thì các ô cấp dưới tự xóa và danh sách lựa chọn cấp dưới thu '
                        'hẹp theo cấp trên.\n'
                        '5. Hệ thống quay về trang 1, tính lại công nợ theo Đến ngày, nạp lại báo cáo và tổng số dòng theo toàn bộ tiêu chí.\n'
                        '6. Hệ thống ghi tạm bộ lọc trên trình duyệt (giữ 10 phút khi tải lại trang).',
                  phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh và chiều sắp xếp, nạp lại từ trang 1.\n'
                      '• Không có kết quả → bảng hiện ' + M_EMPTY + '.\n'
                      '• Ô Nhân viên liệt kê mọi nhân viên đang làm việc (kể cả chưa có hạn mức); chọn nhân viên chưa có hạn mức → '
                      'bảng rỗng.\n'
                      '• Bấm biểu tượng ổ khóa cạnh nhãn Công ty / Phòng ban / Bộ phận / Nhân viên → danh sách hiện cả đơn vị / nhân '
                      'viên đã khóa (bấm lại để ẩn).\n'
                      '• Chọn Chỉ tiêu “Vượt hạn mức” khi mọi nhân viên có công nợ ≤ hạn mức → bảng rỗng.\n'
                      '• Tiêu chí bị tắt trong Cài đặt bộ lọc → không hiện ở khối nâng cao.\n'
                      '• Rời sang màn khác rồi quay lại → bộ lọc về trống; tải lại trang (F5) trong 10 phút → giữ bộ lọc.\n'
                      '• Đến ngày nhỏ hơn Từ ngày (gọi thẳng chức năng) → báo ' + M_DATE + '; trên giao diện lịch đã chặn chọn ngày sai.',
                  dacbiet='Kiểu khớp: ô tìm nhanh khớp MỘT PHẦN mã hoặc họ tên nhân viên, không phân biệt hoa / thường và không phân '
                          'biệt dấu, tự bỏ khoảng trắng đầu / cuối; ký tự % và _ được hiểu đúng là ký tự thường. Ô tìm nhanh không giới '
                          'hạn số ký tự. Công ty, Phòng ban, Bộ phận (theo hồ sơ nhân viên), Nhân viên, Chỉ tiêu khớp CHÍNH XÁC.'),
       layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
                   shot_caption='Khối Bộ lọc danh sách đang mở Tìm kiếm nâng cao',
                   extra=[(shot('02d_employee'), 'Ô Nhân viên gợi ý khi gõ “Bùi Thị Phương”'),
                          (shot('02c_target_opts'), 'Ô Chỉ tiêu vượt hạn mức có 2 lựa chọn')]),
       ui=[('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', '“Bộ lọc danh sách”', '- Kèm biểu tượng phễu lọc'),
           ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
            ['- Gợi ý “Tìm theo mã hoặc tên nhân viên”', '- Khớp một phần mã hoặc họ tên nhân viên',
             '- Chỉ lọc khi bấm Tìm kiếm hoặc Enter', '- Có nút × xóa nhanh khi đã nhập']),
           ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp giá trị ô tìm nhanh, về trang 1, nạp lại.'),
           ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Xóa toàn bộ tiêu chí kể cả ô tìm nhanh, chiều sắp xếp', '- Xóa bộ lọc ghi tạm', '- Nạp lại từ trang 1']),
           ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Mở / thu gọn khối tiêu chí', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
           ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
           ('Thời gian', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
            ['- 1 ô gồm 2 lịch Từ ngày → Đến ngày', '- Lịch Từ ngày không cho chọn sau Đến ngày, lịch Đến ngày không cho chọn trước '
             'Từ ngày', '- Chọn 1 bên thì chưa nạp lại; đủ 2 bên hoặc xóa cả 2 mới nạp',
             '- Chỉ Đến ngày làm mốc tính công nợ (bảng, cửa sổ chi tiết, file Excel); Từ ngày không đổi số liệu']),
           ('Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống',
            ['- Mặc định: trống (tất cả)', '- Lựa chọn: mọi công ty đang hoạt động (không bó theo công ty người dùng)',
             '- Có nút × bỏ chọn; biểu tượng ổ khóa cạnh nhãn để hiện cả công ty đã khóa',
             '- Đổi giá trị → xóa Phòng ban, Bộ phận, Nhân viên']),
           ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống',
            ['- Mặc định: trống (tất cả)', '- Chọn Công ty thì chỉ còn phòng ban của công ty đó',
             '- Có nút × bỏ chọn; biểu tượng ổ khóa hiện cả phòng ban đã khóa', '- Đổi giá trị → xóa Bộ phận, Nhân viên']),
           ('Bộ phận', 'Dropdown', 'Enable', 'Danh sách bộ phận', 'Không', 'Trống',
            ['- Mặc định: trống (tất cả)', '- Thu hẹp theo Công ty / Phòng ban đã chọn',
             '- Có nút × bỏ chọn; biểu tượng ổ khóa hiện cả bộ phận đã khóa', '- Đổi giá trị → xóa Nhân viên']),
           ('Nhân viên', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
            ['- Mặc định: trống (tất cả)', '- Lựa chọn dạng “Tên - Mã phòng - Mã nhân viên”, gõ để tìm trong danh sách',
             '- Thu hẹp theo Công ty / Phòng ban / Bộ phận đã chọn', '- Có nút × bỏ chọn; biểu tượng ổ khóa hiện cả nhân viên đã nghỉ',
             '- Chọn 1 nhân viên → chỉ còn dòng của nhân viên đó']),
           ('Chỉ tiêu vượt hạn mức', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
            ['- Mặc định: trống (tất cả)'] + TARGETS + ['- Bằng hạn mức thì không thuộc giá trị nào (mục 2.2.6)']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện ' + M_EMPTY + ' khi không có kết quả.'),
           ('Thông báo khoảng ngày sai', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + M_DATE)],
       ev=[('Đổi giá trị một ô chọn nâng cao', 'Change',
            'Before:\n– Áp cho Công ty, Phòng ban, Bộ phận, Nhân viên, Chỉ tiêu vượt hạn mức.\n'
            'During:\n– Ghi nhận giá trị mới, xóa các ô cấp dưới nếu đổi ô cấp trên, ghi tạm bộ lọc; bỏ qua lần nạp trùng y hệt '
            'điều kiện đang hiển thị.\n'
            'After:\n– Quay về trang 1 và nạp lại báo cáo theo toàn bộ tiêu chí đang có.'),
           ('Chọn ô Thời gian', 'Change',
            'Before:\n– Mới chọn 1 trong 2 ngày → chưa nạp lại.\n'
            'During:\n– Đủ 2 ngày (hoặc xóa cả 2) → gửi Từ ngày, Đến ngày; máy chủ kiểm Đến ngày ≥ Từ ngày.\n'
            '– Sai → hiển thị ' + M_DATE + '\n' + ERR + '\n'
            'After:\n– Tổng công nợ tính lại tới Đến ngày; Từ ngày, Đến ngày được dùng khi mở cửa sổ theo khách hàng và khi xuất Excel.'),
           ('Bấm Tìm kiếm hoặc Enter', 'Click',
            'Before:\n– Lấy giá trị ô tìm nhanh (và các tiêu chí đang có).\n'
            'During:\n– Máy chủ bỏ khoảng trắng đầu / cuối, so khớp một phần mã hoặc họ tên nhân viên.\n'
            'After:\n– Quay về trang 1 và nạp lại báo cáo.'),
           ('Bấm biểu tượng ổ khóa cạnh nhãn ô tổ chức', 'Click',
            'Before:\n– Áp cho Công ty, Phòng ban, Bộ phận, Nhân viên.\n'
            'During:\n– Lần đầu tải danh sách đầy đủ (gồm mục đã khóa); mục đã khóa có biểu tượng 🔒.\n'
            'After:\n– Danh sách lựa chọn của ô hiện cả mục đã khóa; bấm lại để ẩn đi.'),
           ('Bấm Làm mới', 'Click',
            'Before:\n– Không hỏi xác nhận.\n'
            'During:\n– Đặt lại toàn bộ tiêu chí về trống, bỏ chiều sắp xếp, xóa bộ lọc ghi tạm.\n'
            'After:\n– Quay về trang 1 và nạp lại báo cáo.'),
           ('Bấm Tìm kiếm nâng cao', 'Click',
            'Before:\n– Khối tiêu chí đang thu gọn.\nDuring:\n– Mở khối, nhãn nút đổi thành “Ẩn tìm kiếm nâng cao”.\n'
            'After:\n– Bấm lại để thu gọn; giá trị đã chọn vẫn áp dụng; trạng thái mở / thu gọn được ghi tạm cùng bộ lọc.'),
           ('Rời màn hoặc tải lại trang', 'System',
            'Before:\n– Màn chỉ giữ bộ lọc khi tải lại trang (F5) trong vòng 10 phút.\n'
            'During:\n– Chuyển sang màn khác → xóa bộ lọc ghi tạm; quá 10 phút → bỏ bộ lọc cũ.\n'
            'After:\n– Lần vào lại màn bằng menu, bộ lọc về trống.')])
d.p('2.2.%d Cách lấy dữ liệu của ô lọc' % k)
d.p('Bảng dưới giải thích cách hệ thống áp từng tiêu chí. Không ô lọc nào có icon ⓘ.')
d.data_table([
    ('Ô tìm nhanh', 'Dòng có mã hồ sơ nhân viên hoặc họ tên nhân viên chứa chuỗi gõ.', '—'),
    ('Công ty / Phòng ban / Bộ phận', 'Dòng có công ty / phòng ban / bộ phận ghi trên hồ sơ nhân viên bằng giá trị đã chọn.', '—'),
    ('Nhân viên', 'Đúng dòng của tài khoản nhân viên đã chọn (rỗng nếu nhân viên chưa có hạn mức).', '—'),
    ('Chỉ tiêu: Trong hạn mức', 'Tổng công nợ khách hàng hiện tại < Hạn mức công nợ xuất hàng (gồm công nợ 0 và công nợ âm).', '—'),
    ('Chỉ tiêu: Vượt hạn mức', 'Tổng công nợ khách hàng hiện tại > Hạn mức công nợ xuất hàng. Bằng nhau không thuộc chỉ tiêu nào.', '—'),
    ('Thời gian', 'Chỉ Đến ngày có tác dụng: bút toán có ngày hạch toán sau Đến ngày bị loại khỏi công nợ (bảng, cửa sổ, file). '
                  'Từ ngày chỉ dùng kiểm Đến ngày ≥ Từ ngày.', '—'),
])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho phép mỗi người dùng tự chọn những tiêu chí lọc muốn thấy ở khối Tìm kiếm nâng cao và sắp xếp lại thứ tự '
                   'của chúng. Cấu hình lưu theo người dùng cho riêng màn này (3 mục: Thời gian; Công ty – Phòng ban – Bộ phận – '
                   'Nhân viên (một mục gồm 4 ô); Chỉ tiêu vượt hạn mức).',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 3 mục tiêu chí kèm ô tích, theo cấu hình đang lưu.\n'
                    '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình cho người dùng, hiển thị “Cập nhật thành công” và áp ngay lên khối Tìm kiếm nâng cao.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ 3 mục theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu thay đổi.\n'
                  '• Lưu thất bại → hiển thị “Thao tác thất bại”.\n'
                  '• Ẩn một mục đang có giá trị → giá trị đó bị xóa khỏi bộ lọc (ẩn mục tổ chức thì xóa cả 4 ô), báo cáo nạp lại.\n'
                  '• Tắt bớt còn ≤ 3 ô (tính cả ô tìm nhanh, mục tổ chức tính 4 ô, Thời gian tính 2 ô) → các ô bày thẳng trên 1 '
                  'hàng, nút Tìm kiếm nâng cao ẩn; nút Cài đặt bộ lọc vẫn còn để bật lại.',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách tiêu chí', 'Table/Grid', 'Enable', '3 mục', 'Không', 'Theo cấu hình đã lưu',
        ['- Thời gian; Công ty – Phòng ban – Bộ phận – Nhân viên; Chỉ tiêu vượt hạn mức', '- Mỗi mục đánh số thứ tự 1, 2, 3',
         '- Ô tìm nhanh mã, tên nhân viên không nằm trong danh sách (luôn hiện)']),
       ('Ô tích của tiêu chí', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình đã lưu',
        ['- Tích: tiêu chí hiện ở khối Tìm kiếm nâng cao', '- Bỏ tích: ẩn tiêu chí (mục tổ chức ẩn cả 4 ô)']),
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
        'Before:\n– Cấu hình gắn với người dùng đang đăng nhập và màn này; không cần quyền riêng.\n'
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
   intro=dict(ten='Tùy chỉnh cột của bảng báo cáo',
              mota='Cho phép mỗi người dùng bật / tắt và kéo sắp xếp 7 cột của bảng báo cáo, lưu theo người dùng. Hai cột STT, '
                   'Mã nhân viên bị khóa (luôn hiện, không đổi vị trí).',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
                    '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 7 cột kèm ô tích theo cấu hình đang áp dụng.\n'
                    '3. Người dùng tích / bỏ tích, kéo biểu tượng ba gạch để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình, hiển thị “Cập nhật thành công”, vẽ lại bảng.',
              phu='• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, danh sách cột trả về cấu hình đang áp dụng.\n'
                  '• Cột khóa (STT, Mã nhân viên): ô tích xám, không bỏ tích, không kéo được; di chuột hiện “Cột bắt buộc — không '
                  'thể ẩn hoặc đổi vị trí”.\n'
                  '• Lưu thất bại → hiển thị “Thao tác thất bại”.\n'
                  '• Cấu hình lưu trên máy chủ theo tài khoản: giữ sau khi tải lại (F5), đổi trình duyệt / máy khác vẫn giữ; tài '
                  'khoản khác không bị ảnh hưởng.\n'
                  '• Ẩn cột thì cửa sổ Xuất Excel không tích sẵn trường tương ứng (vẫn tích thêm được).\n'
                  '• Ẩn cột có icon ⓘ thì icon ẩn theo cột.\n'
                  '• Đổi cột không làm thay đổi dữ liệu, tổng số dòng, bộ lọc đang áp.',
              dacbiet='Không có cột mặc định ẩn: lần đầu cả 7 cột đều tích. Cột STT, Mã nhân viên ghim trái khi cuộn ngang.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Tuỳ chỉnh cột”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Tích chọn cột cần hiển thị, kéo ≡ để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', '7 cột', '–', 'Theo cấu hình',
        ['- STT, Mã nhân viên (khóa), Tên nhân viên, Bộ phận, Phòng ban, Hạn mức công nợ xuất hàng, Tổng công nợ khách hàng hiện '
         'tại']),
       ('Ô tích của cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình',
        ['- Tích: cột hiện trên bảng', '- Cột STT, Mã nhân viên: ô tích xám, không bỏ được']),
       ('Biểu tượng ba gạch', 'Icon Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Kéo để đổi vị trí cột', '- Cột STT, Mã nhân viên hiện biểu tượng ổ khóa, không kéo được']),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi cột.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi cột trừ STT, Mã nhân viên.'),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/7 cột”, n = số cột đang tích.'),
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
        'Before:\n– Cột STT, Mã nhân viên không kéo được.\nDuring:\n– Đổi thứ tự cột trong cửa sổ.\n'
        'After:\n– Chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bỏ tích một cột', 'Change',
        'Before:\n– Cột STT, Mã nhân viên không cho bỏ tích.\nDuring:\n– Ghi nhận trạng thái trong cửa sổ, cập nhật dòng đếm.\n'
        'After:\n– Chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng và màn này; không cần quyền riêng.\n'
        'During:\n– Ghi cấu hình; lỗi → hiển thị “Thao tác thất bại”.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng theo cấu hình mới.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ thay đổi chưa lưu.\n'
        'After:\n– Đóng cửa sổ; lần mở sau hiện lại đúng cấu hình đang áp dụng.')])

# ------------------------------------------------------------ 2.5
FILE = 'bao-cao-han-muc-cong-no-nhan-vien.xlsx'
fr(5, 'Xuất Excel', usecase=('FR-05', 'Xuất Excel', 'io', A_ND),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất báo cáo hạn mức công nợ nhân viên ra Excel',
              mota='Người dùng chọn trường và thứ tự cột trong cửa sổ “Chọn trường xuất file” rồi tải file Excel gồm TOÀN BỘ dòng '
                   'báo cáo khớp bộ lọc đang áp dụng (không riêng trang đang xem), công nợ tính tới Đến ngày của bộ lọc. File dựng '
                   'ngay trên trình duyệt; báo cáo rỗng vẫn ra file có tiêu đề và hàng tên cột (#11725).',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng lọc báo cáo (nếu cần) rồi bấm Xuất Excel trên thanh công cụ của bảng.\n'
                    '2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn các trường đang hiện trên bảng (theo đúng thứ tự trên '
                    'bảng), các trường đang ẩn xếp sau và không tích.\n'
                    '3. Người dùng tích / bỏ tích, kéo đổi thứ tự, bấm Xuất file.\n'
                    '4. Hệ thống đóng cửa sổ, khóa nút Xuất Excel, lấy toàn bộ dòng theo bộ lọc + sắp xếp đang áp dụng (theo từng đợt, '
                    'hiện tiến độ), lấy letterhead công ty của người đăng nhập.\n'
                    '5. Hệ thống tải file “' + FILE + '”, hiển thị “Xuất Excel thành công.”.',
              phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → không xuất.\n'
                  '• Không có dòng khớp bộ lọc → VẪN tải file gồm letterhead, tiêu đề, hàng tên cột và khối ký, phần dữ liệu trống; '
                  'hiển thị “Xuất Excel thành công.”.\n'
                  '• Lỗi → hiển thị câu lỗi máy chủ trả, hoặc “Lỗi khi xuất Excel”; mở khóa nút.\n'
                  '• Không lấy được letterhead → vẫn xuất file, tiêu đề lên dòng 1.',
              dacbiet='Cấu trúc file (sheet “Han muc cong no NV”): dòng 1 letterhead công ty người đăng nhập (rộng bằng bảng); dòng 2 '
                      'tiêu đề “BÁO CÁO HẠN MỨC CÔNG NỢ NHÂN VIÊN”; dòng 3 hàng tên cột gồm STT rồi các trường đã chọn đúng thứ tự '
                      '(có nút lọc); dữ liệu ngay sau; cuối file khối “Ngày ..., tháng ..., năm ...” / “Người lập” / “(Ký, họ tên)”. '
                      'Hạn mức, Tổng công nợ là ô số #,##0 (cộng được bằng SUM, số âm giữ dấu “-”). Mỗi đợt lấy tối đa 5.000 dòng, '
                      'không giới hạn tổng số dòng. Khóa nút Xuất Excel trong lúc chờ file.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.',
               extra=[(shot('20b_export_empty'), 'Báo cáo rỗng: bấm Xuất file vẫn tải file có tiêu đề và hàng tên cột')]),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn trường xuất file”', 'Kèm biểu tượng tải xuống và nút (x) đóng.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Tích chọn trường cần xuất, kéo ≡ để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', '6 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- Mã nhân viên, Tên nhân viên, Bộ phận, Phòng ban, Hạn mức công nợ xuất hàng, Tổng công nợ khách hàng hiện tại',
         '- STT luôn có trong file, không nằm trong danh sách', '- Trường đang hiện trên bảng tích sẵn, xếp trước']),
       ('Ô tích của trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Theo cột đang hiện', 'Tích: trường có trong file.'),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Chữ gợi ý “Kéo để đổi vị trí cột trong file”', '- Thứ tự trong danh sách = thứ tự cột trong file']),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/6 trường”.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi trường.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → đóng cửa sổ rồi tải file']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.'),
       ('Tiến độ xuất', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Cạnh nút Xuất Excel, chỉ hiện khi đang xuất', '- “Đang chuẩn bị dữ liệu…”, “Đã tải x/y dòng…”, “Đang dựng file x/y dòng…”']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công (kể cả file rỗng): “Xuất Excel thành công.”', '- Lỗi: “Lỗi khi xuất Excel” hoặc câu máy chủ trả'])],
   ev=[('Bấm Xuất Excel trên thanh công cụ', 'Click',
        'Before:\n– Nút khóa khi đang có lượt xuất chạy; không kiểm tra quyền riêng.\n'
        'During:\n– Tích sẵn các trường ứng với cột đang hiện trên bảng, xếp theo thứ tự cột.\n'
        'After:\n– Mở cửa sổ “Chọn trường xuất file”.'),
       ('Kéo tay nắm', 'Drag',
        'Before:\n– Áp cho mọi trường.\nDuring:\n– Đổi thứ tự trường.\nAfter:\n– Thứ tự mới là thứ tự cột trong file.'),
       ('Bấm Chọn tất cả hoặc Bỏ chọn hết', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Tích / bỏ tích mọi trường.\n'
        'After:\n– Cập nhật dòng đếm; bỏ hết thì khóa nút Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; chặn bấm lặp khi đang xuất; khóa nút Xuất Excel trong lúc chờ.\n'
        '– Kiểm Đến ngày ≥ Từ ngày nếu đang lọc Thời gian; sai → ' + M_DATE + '\n'
        'During:\n– Lấy toàn bộ dòng theo bộ lọc + sắp xếp đang áp dụng, công nợ tới Đến ngày, mỗi đợt tối đa 5.000 dòng; cập nhật '
        'tiến độ.\n'
        '– Bỏ qua trường lạ không có trong danh sách; STT luôn đứng đầu.\n'
        '– Không có dòng → vẫn dựng file chỉ có tiêu đề, hàng tên cột, khối ký.\n' + ERR + '\n'
        'After:\n– Dựng file: letterhead, tiêu đề, hàng tên cột, dữ liệu, khối ký; tải “' + FILE + '”.\n'
        '– Hiển thị “Xuất Excel thành công.”; mở khóa nút. Lỗi → “Lỗi khi xuất Excel” hoặc câu máy chủ trả.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ; lần mở sau tích lại theo cột đang hiện.')])

# ------------------------------------------------------------ 2.6
k = fr(6, 'Xem chi tiết hạn mức dư nợ nhân viên theo khách hàng',
       usecase=('FR-06', 'Xem chi tiết hạn mức dư nợ theo khách hàng', 'view', A_ND),
       rule=('- Màn Xem chi tiết, Popup và Sắp xếp dữ liệu bảng.', 'detail'),
       intro=dict(ten='Xem công nợ của nhân viên tách theo khách hàng',
                  mota='Bấm Mã nhân viên trên một dòng báo cáo để mở cửa sổ “Thông tin chi tiết hạn mức dư nợ nhân viên <Mã> - <Tên> '
                       'theo khách hàng”: mỗi khách hàng có bút toán công nợ thuộc hợp đồng do nhân viên tạo là một dòng, kèm Mã, Tên '
                       'khách hàng và Công nợ cộng dồn y ERP. Có ô tìm nhanh, lọc Khách hàng, Số tiền từ → đến. Cửa sổ chỉ đọc.',
                  tacnhan=TN,
                  dieukien=DK + '\n4. Nhân viên đang có Hạn mức công nợ xuất hàng > 0 (là dòng trên báo cáo).',
                  chinh='1. Người dùng bấm Mã nhân viên ở cột Mã nhân viên.\n'
                        '2. Hệ thống mở cửa sổ, tiêu đề ghép mã và tên nhân viên; bộ lọc trống; bảng chưa sắp theo cột nào.\n'
                        '3. Hệ thống kiểm tra nhân viên có hạn mức > 0; lấy cùng tập bút toán với cột Tổng công nợ (tài khoản con của '
                        '131, hợp đồng loại ERP tính do nhân viên tạo, tới Đến ngày), bỏ bút toán không có khách hàng.\n'
                        '4. Hệ thống duyệt bút toán theo thứ tự ghi sổ, cộng Nợ trừ Có vào một số lũy kế chung; mỗi khách hàng nhận số '
                        'lũy kế tại bút toán cuối cùng của khách đó; dòng xếp theo thứ tự khách hàng xuất hiện lần đầu.\n'
                        '5. Hệ thống hiển thị bảng (không phân trang, không dòng tổng) và nạp danh sách ô Khách hàng = mọi khách hàng '
                        'của nhân viên.\n'
                        '6. Người dùng tìm nhanh / chọn khách hàng / nhập khoảng số tiền / bấm tiêu đề Công nợ để lọc, sắp; bấm Đóng để '
                        'về báo cáo.',
                  phu='• Nhân viên không có bút toán công nợ → bảng ' + M_EMPTY + ', ô Khách hàng không có lựa chọn.\n'
                      '• Chọn Khách hàng → lọc ngay; số cộng dồn chỉ tính bút toán của khách đó (= Nợ − Có riêng khách đó).\n'
                      '• Ô tìm nhanh, Số tiền từ → đến lọc SAU khi cộng dồn (số từng dòng không đổi); áp khi bấm Tìm kiếm hoặc Enter; '
                      'bấm × ở ô tìm nhanh → nạp lại ngay.\n'
                      '• Bấm Làm mới → xóa ô tìm nhanh, Khách hàng, Số tiền, nạp lại.\n'
                      '• Bấm tiêu đề Công nợ → sắp tăng dần, bấm lại giảm dần.\n'
                      '• Nhân viên không có hạn mức (gọi thẳng) hoặc máy chủ lỗi → hiển thị ' + M_LOADERR + '.\n'
                      '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không hỏi; lần mở sau bộ lọc và sắp xếp về mặc định.\n'
                      '• Công nợ có thể âm.',
                  dacbiet='Số của một khách hàng là số LŨY KẾ qua các khách (giữ y ERP, #11729) nên cộng các dòng không ra tổng công nợ '
                          'và cửa sổ không có dòng tổng. Mở cửa sổ nhiều lần liên tiếp chỉ lấy kết quả của lần mở sau cùng.'),
       layout=dict(menu=MENU + ' => Mã nhân viên', shot=shot('03_popup'),
                   shot_caption='Cửa sổ Thông tin chi tiết hạn mức dư nợ nhân viên DNS01 - DNS Admin theo khách hàng (dev chưa có '
                                'bút toán của nhân viên này nên bảng rỗng)',
                   note='Modal ' + POPUP + ' được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
       ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Theo nhân viên',
            ['- “Thông tin chi tiết hạn mức dư nợ nhân viên <Mã> - <Tên> theo khách hàng”',
             '- Kèm biểu tượng người và nút (x) đóng']),
           ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', '“Bộ lọc công nợ theo khách hàng”',
            '- 3 ô bày trên 1 hàng (không có nút Tìm kiếm nâng cao, Cài đặt bộ lọc)'),
           ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
            ['- Gợi ý “Tìm theo mã, tên khách hàng”', '- Khớp một phần, không phân biệt hoa / thường, CÓ phân biệt dấu',
             '- Áp khi bấm Tìm kiếm hoặc Enter; bấm × xóa và nạp lại ngay']),
           ('Khách hàng', 'Dropdown', 'Enable', 'Danh sách khách hàng của nhân viên', 'Không', 'Trống',
            ['- Mặc định: trống (tất cả)', '- Lựa chọn dạng “Mã - Tên”, đủ mọi khách hàng của nhân viên (không thu hẹp theo bộ lọc)',
             '- Chọn → nạp lại ngay; có nút × bỏ chọn']),
           ('Số tiền', 'Textbox', 'Enable', 'Số, phân cách hàng nghìn', 'Không', 'Trống',
            ['- 2 ô Từ → Đến trong 1 khung', '- Lọc dòng có Công nợ ≥ Từ và ≤ Đến (tính cả bằng)',
             '- Áp khi bấm Tìm kiếm hoặc Enter trong ô']),
           ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp ô tìm nhanh và Số tiền, nạp lại cửa sổ.'),
           ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa cả 3 ô lọc, nạp lại cửa sổ.'),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Số thứ tự 1, 2, 3… (không phân trang)'),
           ('Cột Mã khách hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Mã khách hàng', '- Không sắp xếp']),
           ('Cột Tên khách hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Tên khách hàng', '- Không sắp xếp']),
           ('Cột Công nợ', 'Table/Grid', 'Read-only', 'Số, có thể âm', '–', 'Theo dữ liệu',
            ['- Số lũy kế y ERP tại bút toán cuối của khách (mục 2.6.8)', '- Căn phải, phân cách hàng nghìn; 0 vẫn hiện “0”',
             '- Sắp xếp được; mở cửa sổ chưa sắp (biểu tượng ⇅)']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- ' + M_EMPTY),
           ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Góc phải chân cửa sổ; đóng cửa sổ.'),
           ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.'),
           ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + M_LOADERR)],
       ev=[('Bấm Mã nhân viên', 'Click',
            'Before:\n– Kiểm tra nhân viên có hạn mức công nợ xuất hàng > 0; không có → ' + M_LOADERR + ' và dừng.\n'
            '– Lấy Từ ngày, Đến ngày đang chọn ở bộ lọc Thời gian; kiểm Đến ngày ≥ Từ ngày.\n'
            'During:\n– Lấy bút toán theo cách ERP tới Đến ngày, bỏ bút toán không có khách hàng; cộng dồn theo thứ tự ghi sổ.\n' + ERR + '\n'
            'After:\n– Hiển thị bảng chưa sắp, thứ tự khách hàng xuất hiện; nạp danh sách ô Khách hàng.'),
           ('Chọn Khách hàng', 'Change',
            'Before:\n– Giá trị mới khác giá trị cũ và cửa sổ đang mở.\n'
            'During:\n– Nạp lại, chỉ lấy bút toán của khách đó rồi cộng dồn; giữ ô tìm nhanh, Số tiền, chiều sắp đang có.\n'
            'After:\n– Bảng cập nhật; danh sách ô Khách hàng giữ đủ.'),
           ('Bấm Tìm kiếm hoặc Enter (ô tìm nhanh, ô Số tiền)', 'Click',
            'Before:\n– Lấy ô tìm nhanh (bỏ khoảng trắng đầu / cuối), Số tiền Từ, Đến (bỏ dấu phẩy).\n'
            'During:\n– Cộng dồn như khi mở, rồi giữ dòng có mã / tên khách chứa chuỗi gõ và Công nợ trong khoảng Từ → Đến.\n'
            'After:\n– Bảng cập nhật; số từng dòng không đổi so với khi chưa lọc.'),
           ('Bấm Làm mới', 'Click',
            'Before:\n– Không hỏi xác nhận.\nDuring:\n– Xóa ô tìm nhanh, Khách hàng, Số tiền.\n'
            'After:\n– Nạp lại cửa sổ như lúc mới mở (giữ chiều sắp đang chọn).'),
           ('Bấm tiêu đề cột Công nợ', 'Click',
            'Before:\n– Chỉ cột Công nợ sắp xếp được.\n'
            'During:\n– Lần đầu tăng dần, bấm lại giảm dần; nạp lại kèm bộ lọc đang có.\n'
            'After:\n– Bảng xếp theo Công nợ, mũi tên ở cột Công nợ.'),
           ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
            'Before:\n– Không hỏi xác nhận (cửa sổ chỉ đọc).\n'
            'During:\n– Hủy kết quả nạp còn dở; xóa bộ lọc của cửa sổ.\n'
            'After:\n– Đóng cửa sổ; báo cáo giữ nguyên bộ lọc, trang, sắp xếp.')])
d.p('2.6.%d Mục đích thiết kế popup' % k)
d.bullets([
    'Trả lời câu hỏi: công nợ khách hàng mà nhân viên đang “gánh” (so với hạn mức) nằm ở những khách hàng nào, để đôn đốc đúng khách.',
    'Là cửa sổ nổi để giữ nguyên ngữ cảnh báo cáo (bộ lọc, trang, sắp xếp) — xem xong đóng là quay lại đúng chỗ, không phải chuyển '
    'màn.',
    'Ràng buộc khớp số: cùng tập bút toán và cùng mốc Đến ngày với cột Tổng công nợ khách hàng hiện tại; khi không lọc, dòng của '
    'khách hàng có bút toán ghi sổ sau cùng mang số bằng cột Tổng công nợ. Do cộng dồn y ERP, cộng các dòng KHÔNG ra tổng công nợ '
    'nên cửa sổ không có dòng tổng.',
    'Người dùng làm tiếp: tìm / lọc khách hàng, lọc khoảng số tiền, sắp theo Công nợ; mỗi lần mở là cửa sổ mới (không giữ bộ lọc / '
    'sắp xếp lần trước). Cửa sổ không có xuất Excel, không có liên kết sang chứng từ.',
])
k += 1
d.p('2.6.%d Các biến thể theo con số bấm' % k)
d.popup_variant_table([
    ('Mã nhân viên ở bất kỳ dòng nào, bộ lọc Thời gian trống', 'Mọi khách hàng có bút toán (loại ERP tính) thuộc hợp đồng do nhân '
     'viên tạo, tới hiện tại', '“Thông tin chi tiết hạn mức dư nợ nhân viên <Mã> - <Tên> theo khách hàng”',
     'Không ẩn ô nào; bộ lọc trống'),
    ('Mã nhân viên khi bộ lọc Thời gian có Từ ngày – Đến ngày', 'Như trên nhưng chỉ bút toán có ngày hạch toán ≤ Đến ngày',
     'Như trên', 'Không ẩn ô nào; khoảng ngày không hiện trong cửa sổ'),
])
k += 1
d.p('2.6.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('“Tập dữ liệu” là các bút toán trên tài khoản con của 131, gắn hợp đồng đầu kỳ / thanh lý / dịch vụ / dự án / loại cũ của ERP do '
    'nhân viên đã bấm tạo, có khách hàng, tới hết Đến ngày của bộ lọc Thời gian (trống = toàn bộ). Cửa sổ không có icon ⓘ.')
d.data_table([
    ('Cột Công nợ (dòng khách hàng)', 'Duyệt bút toán theo thứ tự ghi sổ, mỗi bút toán Nợ cộng / Có trừ vào MỘT số lũy kế chung cho '
                                      'mọi khách; khách hàng nhận số lũy kế ngay sau bút toán cuối cùng của khách đó (giữ y ERP, '
                                      '#11729). Có thể âm.', '—'),
    ('Thứ tự dòng mặc định', 'Theo thứ tự khách hàng xuất hiện lần đầu trên sổ; chỉ đổi khi bấm tiêu đề Công nợ.', '—'),
    ('Khi chọn Khách hàng', 'Chỉ lấy bút toán của khách đó rồi cộng dồn → số = Σ Nợ − Σ Có của riêng khách đó với hợp đồng của '
                            'nhân viên.', '—'),
    ('Ô tìm nhanh, Số tiền', 'Lọc sau khi đã cộng dồn trên toàn tập, nên số từng dòng không đổi.', '—'),
    ('Ô Khách hàng', 'Mọi khách hàng có trong tập dữ liệu, dạng “Mã - Tên”, theo thứ tự xuất hiện.', '—'),
])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Báo cáo hạn mức công nợ nhân viên; không lặp lại các quy tắc đã có '
           'trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Điều kiện dòng lên báo cáo', [
        '– Tài khoản nhân viên có Hạn mức công nợ xuất hàng > 0 (khai ở form Tài khoản nhân viên).',
        '– Mọi công ty, mọi trạng thái tài khoản / nhân viên (kể cả đã khóa, đã nghỉ).',
        '– Hạn mức trống hoặc 0 → không lên.'],
     ['Xem báo cáo', 'Xuất Excel']),
    ('BR-02', 'Tổng công nợ khách hàng hiện tại (giữ y ERP)', [
        '– Σ phát sinh Nợ − Σ phát sinh Có, số tiền đã quy VND, chỉ trên tài khoản con của 131 (không gồm 131).',
        '– Chỉ bút toán gắn hợp đồng đầu kỳ, thanh lý, dịch vụ, dự án hoặc hợp đồng loại cũ của ERP; nhân viên = người tạo hợp '
        'đồng đó.',
        '– Hợp đồng bán hàng, hợp đồng dịch vụ bảo hành không tính (người dùng chốt 16/10/2026, #11727).'],
     ['Xem báo cáo', 'Tìm kiếm và lọc', 'Xuất Excel']),
    ('BR-03', 'Chỉ tiêu vượt hạn mức', [
        '– Trong hạn mức: Tổng công nợ < Hạn mức (gồm công nợ 0, âm).',
        '– Vượt hạn mức: Tổng công nợ > Hạn mức.',
        '– Bằng nhau: không thuộc chỉ tiêu nào.'],
     ['Tìm kiếm và lọc', 'Xuất Excel']),
    ('BR-04', 'Mốc thời gian', [
        '– Chỉ Đến ngày tác dụng: bút toán có ngày hạch toán ≤ Đến ngày; trống = tới hiện tại.',
        '– Từ ngày chỉ dùng kiểm hợp lệ: Đến ngày phải ≥ Từ ngày; chỉ áp khi chọn đủ 2 ngày.',
        '– Cùng mốc cho bảng, cửa sổ theo khách hàng và file Excel.'],
     ['Tìm kiếm và lọc', 'Xem chi tiết hạn mức dư nợ nhân viên theo khách hàng', 'Xuất Excel']),
    ('BR-05', 'Công nợ theo khách hàng cộng dồn (giữ y ERP)', [
        '– Duyệt bút toán theo thứ tự ghi sổ, một số lũy kế chung; khách nhận số lũy kế tại bút toán cuối của khách.',
        '– Lọc Khách hàng áp TRƯỚC khi cộng; tìm nhanh, Số tiền áp SAU.',
        '– Không có dòng tổng (người dùng chốt 16/10/2026, #11729).'],
     ['Xem chi tiết hạn mức dư nợ nhân viên theo khách hàng']),
    ('BR-06', 'Chặn xem công nợ nhân viên bất kỳ', [
        '– Cửa sổ theo khách hàng chỉ mở cho nhân viên có hạn mức > 0; nhân viên khác → “Lỗi khi tải dữ liệu”.'],
     ['Xem chi tiết hạn mức dư nợ nhân viên theo khách hàng']),
    ('BR-07', 'Chuẩn hóa dữ liệu tìm kiếm', [
        '– Ô tìm nhanh báo cáo: khớp một phần mã / họ tên nhân viên, bỏ khoảng trắng đầu / cuối, không phân biệt hoa / thường '
        'và dấu; % và _ là ký tự thường.',
        '– Ô tìm nhanh cửa sổ: khớp một phần mã / tên khách hàng, không phân biệt hoa / thường, có phân biệt dấu.',
        '– Công ty, Phòng ban, Bộ phận, Nhân viên, Chỉ tiêu, Khách hàng: khớp chính xác; Số tiền tính cả 2 đầu.'],
     ['Tìm kiếm và lọc', 'Xem chi tiết hạn mức dư nợ nhân viên theo khách hàng']),
    ('BR-08', 'Hiển thị số và thứ tự', [
        '– Số phân cách hàng nghìn bằng dấu phẩy; công nợ 0 hiện “0”; số âm có dấu “-”.',
        '– Thứ tự mặc định báo cáo: tài khoản cập nhật gần nhất lên đầu (#11726), bằng nhau thì tài khoản tạo sau lên trước.',
        '– Cửa sổ mở ra chưa sắp: thứ tự khách hàng xuất hiện trên sổ.'],
     ['Xem báo cáo', 'Xem chi tiết hạn mức dư nợ nhân viên theo khách hàng']),
    ('BR-09', 'Ghi nhớ bộ lọc', [
        '– Bộ lọc, trạng thái khối nâng cao ghi tạm 10 phút trên trình duyệt; tải lại trang thì khôi phục.',
        '– Rời sang màn khác hoặc bấm Làm mới → xóa. Bộ lọc cửa sổ không ghi nhớ.'],
     ['Tìm kiếm và lọc']),
    ('BR-10', 'Tính duy nhất', [
        '– Mỗi tài khoản nhân viên 1 dòng (1 giá trị hạn mức), không có 2 dòng cùng tài khoản.',
        '– Mã nhân viên do hồ sơ nhân viên quản lý.'],
     ['Xem báo cáo']),
    ('BR-11', 'Liên kết cha – con', [
        '– Công ty > Phòng ban > Bộ phận > Nhân viên (hạn mức) > công nợ theo khách hàng.',
        '– Đổi ô lọc cấp trên xóa ô cấp dưới; đặt hạn mức về 0 / trống ở form Tài khoản nhân viên → dòng rời báo cáo.'],
     ['Xem báo cáo', 'Tìm kiếm và lọc']),
    ('BR-12', 'File Excel', [
        '– Trường do người dùng chọn, đúng thứ tự, STT luôn đầu; tiền là ô số #,##0.',
        '– Rỗng vẫn tạo file có letterhead, tiêu đề, hàng tên cột, khối ký (#11725).',
        '– Letterhead theo công ty người đăng nhập.'],
     ['Xuất Excel']),
    ('BR-13', 'Lịch sử', [
        '– Màn chỉ đọc nên không có Lịch sử thay đổi.',
        '– Đổi Hạn mức công nợ xuất hàng ở form Tài khoản nhân viên được ghi vào lịch sử của tài khoản đó (giá trị cũ → mới).'],
     ['Xem báo cáo']),
    ('BR-14', 'Phạm vi dữ liệu', [
        '– Không quyền riêng, không bó theo công ty người đăng nhập (giữ y ERP, chốt 14/10/2026).'],
     ['Xem báo cáo', 'Xuất Excel', 'Xem chi tiết hạn mức dư nợ nhân viên theo khách hàng']),
    ('BR-15', 'Khác hệ thống ERP (có chủ đích)', [
        '– Ô lọc Nhân viên lọc thật (ERP không có tác dụng).',
        '– Mốc Đến ngày theo ngày hạch toán; cửa sổ dùng đúng Đến ngày của bảng (ERP lấy Đến ngày = Từ ngày).',
        '– Thêm ô tìm nhanh (bảng + cửa sổ), Xuất Excel chọn trường, Tùy chỉnh cột, icon ⓘ; thứ tự mặc định theo ngày cập nhật.'],
     ['Xem báo cáo', 'Tìm kiếm và lọc', 'Xem chi tiết hạn mức dư nợ nhân viên theo khách hàng']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu')
d.p('Báo cáo hạn mức công nợ nhân viên chỉ đọc, không ghi dữ liệu. Các màn hình dưới đây cung cấp dữ liệu cho báo cáo (hạn mức của tài khoản nhân viên và bút toán công nợ phải thu 131 theo hợp đồng).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Quản trị hệ thống', 'Tài khoản nhân viên — ô Hạn mức công nợ xuất hàng ở form Thêm / Sửa (nguồn hạn mức duy nhất; nhân viên có hạn mức > 0 mới lên báo cáo)', 'Quản trị hệ thống -> Người dùng & phân quyền'),
    ('2', 'Tài chính', 'Công nợ đầu kỳ theo khách hàng - hợp đồng (hợp đồng đầu kỳ và bút toán tài khoản con của 131; người tạo hợp đồng quyết định công nợ thuộc nhân viên nào, tính tới Đến ngày)', 'Tài chính -> Khai báo đầu kỳ; Tài chính -> Kế toán công nợ -> Khách hàng'),
    ('3', 'Hệ thống ERP', 'Hợp đồng thanh lý, hợp đồng dịch vụ, hợp đồng dự án (bút toán tài khoản con của 131 gắn các hợp đồng này cũng được cộng vào công nợ của người tạo hợp đồng)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
