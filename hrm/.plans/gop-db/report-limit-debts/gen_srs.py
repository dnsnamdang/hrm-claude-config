# -*- coding: utf-8 -*-
"""SRS màn "Báo cáo hạn mức công nợ khách hàng" (phân hệ Tài chính) — form chuẩn Danh mục quốc gia + checklist
"Mẫu tài liệu.xlsx" + quy định màn BÁO CÁO (bảng Cách lấy dữ liệu, bảng popup, Mục đích thiết kế popup) — 03/11/2026.

Chạy: python gen_srs.py  → SRS - Báo cáo hạn mức công nợ khách hàng.docx
Khung: srs-documenter (SrsDoc) + ../phieu-theo-form-quoc-gia/CHECKLIST.md. Khuôn thư mục: finance-bill-income-summarize-money.
Nguồn đọc 03/11/2026 (nhánh develop, cả 2 repo):
  FE  pages/finance/report-limit-debts/{index.vue, components/DebtByEmployeeModal.vue}; components/subsystem-menu/finance.js;
      V2BaseSmartFilterPanel, V2BaseFilterFieldControl, V2BaseSelectRemote, V2BaseDataTable, V2BaseModal,
      export-fields-modal (+ exportFieldsMixin), column-customization-modal (+ columnCustomizationMixin),
      filterStateMixin (giữ bộ lọc 10 phút, xóa khi rời màn), utils/export/listExportFile.js (dựng file ở trình duyệt).
  BE  Modules/Finance/{Services/CustomerDebt/ReportLimitDebtService.php, Services/CustomerDebt/CustomerDebtAggregator.php,
      Http/Controllers/V1/ReportLimitDebtController.php, Routes/api.php (nhóm report-limit-debts, không gắn quyền)}.
  Tài liệu: .plans/gop-db/report-limit-debts/{design.md, plan.md} + spec 2026-10-13 (hành vi hiện hành SAU #11766, #11776,
      #11777 — ưu tiên code khi lệch).
Ảnh: ./bchmcn_shots (dev-hrm 03/11/2026, DNS Admin, script bchmcn_shots/_capture/capture.js). Không bật cờ giả nào.
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

TEN = 'Báo cáo hạn mức công nợ khách hàng'
SHOTS = os.path.join(HERE, 'bchmcn_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # sơ đồ Use Case; HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Kế toán công nợ => Khách hàng => Báo cáo hạn mức công nợ khách hàng'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Báo cáo hạn mức công nợ khách hàng.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_ND = 'Kế toán công nợ'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng vào được phân hệ Tài chính (màn không gắn quyền riêng, '
      'giữ như hệ thống ERP); dữ liệu giới hạn ở hạn mức công nợ khai cho công ty người dùng đang làm việc.')
DK = ('1. Người dùng đăng nhập thành công.\n'
      '2. Người dùng vào được phân hệ Tài chính (không cần quyền riêng để mở màn).\n'
      '3. Tài khoản đã được gắn công ty làm việc (chưa gắn công ty thì báo cáo không có dòng nào).')
M_LOADERR = '“Lỗi khi tải dữ liệu”'
M_DATE = '“Đến ngày phải lớn hơn hoặc bằng Từ ngày.”'
M_EMPTY = '“Không có dữ liệu phù hợp.”'
M_FOOT_EMPTY = '“Không có khách hàng nào.”'
TARGETS = ['- Trong hạn mức tính lãi', '- Trong hạn mức được nợ', '- Vượt hạn mức tính lãi', '- Vượt hạn mức công nợ']
CTYPES = ['- Cá nhân', '- Doanh nghiệp tư nhân', '- Doanh nghiệp nước ngoài', '- Tổ chức phi chính phủ', '- Cơ quan nhà nước']
PAGE_ROWS = [
    ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
     ['- Góc trái dưới bảng', '- a–b: khoảng số thứ tự của trang đang xem',
      '- N: tổng số khách hàng có hạn mức khớp phạm vi công ty và bộ lọc']),
    ('Ô Số dòng/trang', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', '10',
     ['- Mặc định: 10', '- Lựa chọn: 5, 10, 20, 50, 100', '- Đổi giá trị → về trang 1, nạp lại']),
    ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
     ['- Nút về đầu «, lùi ‹, số trang, tiến ›, về cuối »', '- Ở trang đầu nút « ‹ mờ; ở trang cuối nút › » mờ',
      '- Giữ nguyên bộ lọc và chiều sắp xếp khi đổi trang']),
    ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
     ['- Trong bảng: ' + M_EMPTY, '- Dưới bảng: ' + M_FOOT_EMPTY + ' thay cho dòng Hiển thị']),
    ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
     ['- ' + M_LOADERR + ' khi máy chủ lỗi', '- Khoảng ngày sai: ' + M_DATE,
      '- Hết phiên đăng nhập: “Phiên đăng nhập đã hết hạn”, chuyển về màn đăng nhập']),
]

d = SrsDoc(out=OUT, menu=MENU, route='/finance/report-limit-debts', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Kế toán công nợ': 'menu_ketoancongno', 'Khách hàng': 'menu_nhom_kh',
    'Báo cáo hạn mức công nợ khách hàng': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Xuất Excel': 'btn_xuatexcel', 'Mã khách hàng': 'link_ma',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Báo cáo hạn mức công nợ khách hàng thuộc phân hệ Tài chính (chuyển từ '
    'hệ thống ERP: Kế toán › Kế toán Công nợ › Khách hàng), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu báo cáo liệt kê các khách hàng đã được khai hạn mức công nợ cho công ty của người xem, kèm hạn mức '
    'tính lãi, hạn mức được nợ, số dư nợ hiện tại và chi tiết công nợ của khách hàng tách theo nhân viên kinh doanh (NVKD).',
    'Ghi rõ các điểm GIỮ Y HỆT hệ thống ERP theo quyết định của người dùng (22/10/2026, #11777): cột Số dư nợ hiện tại luôn '
    'bằng 0 và bộ lọc Chỉ tiêu vượt hạn mức chỉ có “Trong hạn mức tính lãi” ra dòng — để người nghiệm thu không báo nhầm là lỗi.',
])
d.p('Phạm vi chức năng (6 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Tra cứu: Xem báo cáo; Tìm kiếm và lọc; Cài đặt bộ lọc; Tùy chỉnh cột hiển thị; Xuất Excel theo trường chọn.',
    'Xem chi tiết hạn mức dư nợ theo NVKD: bấm Mã khách hàng mở cửa sổ “Chi tiết hạn mức dư nợ khách hàng … theo NVKD”, '
    'công nợ tính theo sổ công nợ phải thu (tài khoản 131).',
    'Không thuộc màn này: màn chỉ đọc — không có Thêm mới, Chỉnh sửa, Xóa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel, '
    'In và không có Lịch sử thay đổi. Hạn mức được khai / sửa ở màn Khai báo hạn mức công nợ khách hàng.',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Kế toán công nợ xem nhanh khách hàng nào của công ty mình đang được cấp hạn mức tính lãi / hạn mức được nợ, thông tin liên '
    'hệ để đôn đốc.',
    'Từ một khách hàng, xem công nợ hiện tại của khách đó tách theo NVKD (người lập hợp đồng) để biết ai đang phụ trách khoản nợ.',
    'File Excel dùng để gửi đối chiếu / báo cáo nội bộ.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Mỗi dòng báo cáo là MỘT dòng khai hạn mức của khách hàng cho công ty người xem; chỉ dòng có ít nhất một hạn mức lớn hơn 0.',
    'Số dư nợ hiện tại luôn hiển thị 0 và không đổi theo Thời gian (giữ y ERP); số liệu công nợ thật xem ở cửa sổ theo NVKD.',
    'Bộ lọc Chỉ tiêu vượt hạn mức tính theo số dư 0: “Trong hạn mức tính lãi” = các dòng có hạn mức tính lãi > 0; ba chỉ tiêu còn '
    'lại luôn không có dòng nào.',
    'Bộ lọc Thời gian không thay đổi bảng chính; chỉ được chuyển sang cửa sổ theo NVKD làm mốc tính công nợ.',
    'Phạm vi dữ liệu theo công ty của người đang đăng nhập, không có quyền riêng.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hạn mức công nợ', 'Mức công nợ tối đa khai cho một khách hàng theo từng công ty, ở màn Khai báo hạn mức công nợ khách hàng. '
                        'Một khách hàng có thể có nhiều dòng hạn mức (mỗi công ty một dòng).'),
    ('Hạn mức tính lãi', 'Ô “Hạn mức công nợ tính lãi” của dòng khai hạn mức: mức dư nợ mà vượt quá sẽ bị tính lãi.'),
    ('Hạn mức được nợ', 'Ô “Hạn mức công nợ xuất hàng” của dòng khai hạn mức: mức dư nợ tối đa còn được xuất hàng.'),
    ('Số dư nợ hiện tại', 'Cột trên báo cáo; theo quyết định giữ y ERP luôn hiển thị 0 (ERP tính sai nên luôn ra 0).'),
    ('Chỉ tiêu vượt hạn mức', 'Bộ lọc 4 giá trị: Trong hạn mức tính lãi, Trong hạn mức được nợ, Vượt hạn mức tính lãi, Vượt hạn mức '
                              'công nợ. Tính theo Số dư nợ hiện tại (= 0).'),
    ('NVKD', 'Nhân viên kinh doanh — người lập hợp đồng ghi trên bút toán công nợ của khách hàng.'),
    ('Sổ công nợ 131', 'Các bút toán tài khoản 131 (phải thu khách hàng) và tài khoản con trực tiếp; nguồn tính công nợ ở cửa sổ '
                       'theo NVKD.'),
    ('Công nợ (cửa sổ NVKD)', 'Dư cuối kỳ = dư đầu kỳ + phát sinh tăng hàng hóa / dịch vụ + điều chỉnh công nợ tăng − nhập trả lại − '
                              'điều chỉnh công nợ giảm − đã thanh toán + trả lại tiền thừa, tính tới Đến ngày.'),
    ('Chưa xác định nhân viên', 'Dòng gom các bút toán công nợ không gắn NVKD mà dư khác 0.'),
    ('Loại hình tổ chức', 'Loại khách hàng: Cá nhân, Doanh nghiệp tư nhân, Doanh nghiệp nước ngoài, Tổ chức phi chính phủ, Cơ quan '
                          'nhà nước.'),
    ('Trạng thái bản ghi', 'Dòng báo cáo không có trạng thái riêng (không Khóa / Hoạt động); dòng chỉ xuất hiện khi còn ít nhất '
                           'một hạn mức > 0.'),
    ('Cấu trúc phân cấp', 'Khách hàng > dòng hạn mức theo công ty > công nợ theo NVKD. Báo cáo hiện cấp dòng hạn mức của công ty '
                          'người xem; cửa sổ NVKD hiện cấp công nợ theo nhân viên.'),
], widths=[2.1, 3.9])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn không gắn quyền riêng (giữ y ERP, người dùng chốt 13/10/2026): mọi người dùng vào được phân hệ Tài chính đều mở được '
    'màn và dùng mọi chức năng. Dữ liệu luôn giới hạn theo công ty của người đang đăng nhập.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('—', '(Không có quyền thao tác riêng)', 'Xem báo cáo, tìm kiếm, cài đặt bộ lọc, tùy chỉnh cột, xuất Excel và xem chi tiết '
                                            'theo NVKD: mọi người dùng mở được màn.'),
], widths=[0.8, 1.9, 3.3])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('—', '(Không có quyền riêng — áp cho báo cáo, xuất Excel)', 'Dòng hạn mức khai cho công ty = công ty làm việc của người '
                                                                 'đăng nhập. Chưa gắn công ty → không có dòng nào.'),
    ('—', '(Không có quyền riêng — áp cho cửa sổ theo NVKD)', 'Chỉ mở được khách hàng đang có dòng hạn mức > 0 của công ty mình; '
                                                             'công nợ trong cửa sổ tính trên toàn sổ 131 của khách (không bó '
                                                             'theo công ty, giữ y ERP).'),
], widths=[0.8, 2.6, 2.6])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Người dùng đã gắn công ty', 'Người dùng chưa gắn công ty'], [
    ('FR-01 Xem báo cáo', '✅ (công ty mình)', '✅ (bảng rỗng)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅ (luôn rỗng)'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅'),
    ('FR-05 Xuất Excel', '✅ (công ty mình)', '❌ (không có dữ liệu để xuất)'),
    ('FR-06 Xem chi tiết hạn mức dư nợ theo NVKD', '✅ (khách hàng trong báo cáo)', '❌ (không có dòng để bấm)'),
], widths=[2.6, 1.7, 1.7])
d.p('Màn không có chức năng Thêm mới, Chỉnh sửa, Xóa, Duyệt / Không duyệt, Khóa / Mở khóa, Import Excel, In và Lịch sử thay đổi '
    'nên ma trận không có các dòng tương ứng. Xuất Excel không gắn quyền riêng: ai xem được báo cáo thì xuất được, file chỉ chứa '
    'dòng của công ty mình.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Tài khoản chưa gắn công ty làm việc: bảng “Không có dữ liệu phù hợp.”, bấm Xuất file báo “Không có dữ liệu để xuất”.',
    'Mở cửa sổ theo NVKD cho khách hàng không có hạn mức của công ty mình (gọi thẳng chức năng bỏ qua giao diện): hệ thống báo '
    '“Lỗi khi tải dữ liệu”, cửa sổ không có dòng.',
    'Gọi thẳng chức năng lấy báo cáo / xuất Excel bỏ qua giao diện vẫn chỉ nhận dòng của công ty mình.',
    'Phân hệ / mục menu bị tắt ở màn Cài đặt phân hệ: không thấy mục menu.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Nút / thao tác', 'Hiện khi', 'Vị trí'], [
    ('Xuất Excel, Cấu hình cột hiển thị', 'Luôn hiện; Xuất Excel khóa trong lúc đang xuất', 'Thanh công cụ của bảng'),
    ('Liên kết Mã khách hàng (mở cửa sổ theo NVKD)', 'Mọi dòng', 'Cột Mã khách hàng'),
    ('Cài đặt bộ lọc, Tìm kiếm nâng cao', 'Luôn hiện (khối lọc có 4 tiêu chí + ô tìm nhanh)', 'Khối Bộ lọc danh sách'),
], widths=[2.2, 2.6, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_ND, [0, 1])],
    [('FR-01', 'Xem báo cáo hạn mức công nợ', 'view'),
     ('FR-05', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-06', 'Xem chi tiết hạn mức dư nợ theo NVKD', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Báo cáo hạn mức công nợ khách hàng')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
k = fr(1, 'Xem báo cáo hạn mức công nợ',
       rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
       intro=dict(
           ten='Truy cập màn Báo cáo hạn mức công nợ khách hàng và xem báo cáo',
           mota='Mở màn Báo cáo hạn mức công nợ khách hàng và hiển thị bảng các khách hàng được khai hạn mức công nợ cho công ty '
                'của người đăng nhập (ít nhất một hạn mức > 0), kèm địa chỉ, người liên hệ, số điện thoại, hạn mức tính lãi, hạn '
                'mức được nợ, số dư nợ hiện tại; có phân trang, sắp xếp và tổng số dòng. Màn chỉ đọc.',
           tacnhan=TN, dieukien=DK,
           chinh='1. Người dùng vào menu theo đường dẫn ở mục Layout.\n'
                 '2. Hệ thống mở màn “Báo cáo hạn mức công nợ khách hàng”; nếu người dùng vừa rời màn bằng cách tải lại trang '
                 '(F5) dưới 10 phút thì khôi phục bộ lọc, trạng thái khối Tìm kiếm nâng cao đã ghi tạm; ngược lại bộ lọc trống.\n'
                 '3. Hệ thống xác định công ty làm việc của người đăng nhập và lấy các dòng khai hạn mức của công ty đó có hạn mức '
                 'tính lãi > 0 hoặc hạn mức được nợ > 0.\n'
                 '4. Với mỗi dòng, hệ thống ghép địa chỉ khách hàng, danh sách người liên hệ (mỗi tên một lần), loại hình tổ chức; '
                 'hạn mức chưa khai hiện 0; Số dư nợ hiện tại = 0.\n'
                 '5. Hệ thống nạp cấu hình cột của người dùng, sắp theo thứ tự khai hạn mức (dòng khai trước ở trên), trả về trang 1 '
                 '(10 dòng) kèm tổng số dòng.',
           phu='• Không có dòng nào khớp → bảng hiện ' + M_EMPTY + ', dưới bảng ' + M_FOOT_EMPTY + '.\n'
               '• Tài khoản chưa gắn công ty → bảng rỗng như trên.\n'
               '• Bấm Mã khách hàng → mở cửa sổ Chi tiết hạn mức dư nợ theo NVKD (mục 2.6).\n'
               '• Máy chủ lỗi → hiển thị ' + M_LOADERR + '.\n'
               '• Phiên đăng nhập hết hạn → hiển thị “Phiên đăng nhập đã hết hạn”, điều hướng về màn đăng nhập.',
           dacbiet='Cột mặc định hiển thị (9): STT, Mã khách hàng, Tên khách hàng, Địa chỉ, Người liên hệ, Số điện thoại, Hạn mức '
                   'tính lãi, Hạn mức được nợ, Số dư nợ hiện tại. Không có cột mặc định ẩn. Cột bắt buộc: STT, Mã khách hàng (ghim '
                   'trái, không ẩn, không đổi vị trí). Sắp xếp được: Mã khách hàng, Tên khách hàng, Hạn mức tính lãi, Hạn mức được '
                   'nợ, Số dư nợ hiện tại. Mặc định 10 dòng/trang. Lọc, sắp xếp, cắt trang tính trên toàn bộ dòng của công ty.'),
       layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn Báo cáo hạn mức công nợ khách hàng',
                   note='Lối vào duy nhất (phân hệ Tài chính). Hiển thị: khách hàng có hạn mức khai cho công ty người đăng nhập.',
                   extra=[(shot('00_menu_panel'), 'Mục Báo cáo hạn mức công nợ khách hàng trong menu Kế toán công nợ › Khách hàng'),
                          (shot('01c_empty'), 'Trạng thái rỗng khi không có dòng khớp')]),
       ui_kw=dict(required=False),
       ui=[
           ('Tiêu đề trang', 'Label', 'Hiển thị', '–', '“Báo cáo hạn mức công nợ khách hàng”',
            '- Ở thanh trên cùng, cũng là tiêu đề tab trình duyệt'),
           ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', '“Báo cáo hạn mức công nợ khách hàng”', '- Đầu khối bảng, kèm biểu tượng tài liệu'),
           ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
            ['- Nút viền xanh lá, biểu tượng Excel', '- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.5)',
             '- Khóa trong lúc đang xuất; bên cạnh hiện tiến độ “Đã tải x/y dòng…”, “Đang dựng file x/y dòng…”']),
           ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
            ['- Biểu tượng cột, chữ gợi ý “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4)']),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Số thứ tự liên tục giữa các trang', '- Ghim bên trái; khóa trong Tùy chỉnh cột', '- Không sắp xếp']),
           ('Cột Mã khách hàng', 'Link', 'Read-only', '–', 'Theo dữ liệu',
            ['- Mã khách hàng, chữ xanh gạch chân', '- Bấm → mở cửa sổ Chi tiết hạn mức dư nợ khách hàng theo NVKD (mục 2.6)',
             '- Sắp xếp được (theo mã, so tự nhiên)', '- Ghim bên trái; khóa trong Tùy chỉnh cột']),
           ('Cột Tên khách hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Tên đầy đủ của khách hàng', '- Chữ dài tự xuống dòng', '- Sắp xếp được']),
           ('Cột Địa chỉ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Ghép: số nhà, thôn / xóm, phường / xã, tỉnh / thành phố, quốc gia', '- Quận / huyện chỉ ghép khi khách ở nước ngoài',
             '- Phần nào trống thì bỏ qua', '- Không sắp xếp']),
           ('Cột Người liên hệ', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Mọi người liên hệ của khách hàng, mỗi người 1 dòng', '- Tên trùng nhau chỉ hiện 1 lần',
             '- Trống khi khách chưa có người liên hệ', '- Không sắp xếp']),
           ('Cột Số điện thoại', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
            ['- Số điện thoại của khách hàng, giữ số 0 đầu', '- Trống khi chưa khai', '- Không sắp xếp']),
           ('Cột Hạn mức tính lãi', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Hạn mức công nợ tính lãi khai cho công ty mình', '- Căn phải, phân cách hàng nghìn bằng dấu phẩy',
             '- Chưa khai hiện 0', '- Sắp xếp được']),
           ('Cột Hạn mức được nợ', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- Hạn mức công nợ xuất hàng khai cho công ty mình', '- Căn phải, phân cách hàng nghìn', '- Chưa khai hiện 0',
             '- Sắp xếp được']),
           ('Cột Số dư nợ hiện tại', 'Table/Grid', 'Read-only', '0', '0',
            ['- Luôn hiện 0 (giữ y ERP, quyết định 22/10/2026)', '- Không đổi theo bộ lọc Thời gian',
             '- Công nợ thật xem ở cửa sổ theo NVKD (mục 2.6)', '- Có biểu tượng sắp xếp nhưng mọi dòng bằng 0 nên thứ tự giữ '
             'theo thứ tự khai hạn mức']),
       ] + PAGE_ROWS,
       ev=[('Mở màn hình', 'System',
            'Before:\n– Xác định công ty của người đăng nhập; không có công ty thì không trả dòng nào.\n'
            '– Có bộ lọc ghi tạm dưới 10 phút (tải lại trang) → khôi phục; quá hạn hoặc vừa rời sang màn khác → bộ lọc trống.\n'
            'During:\n– Nạp cấu hình cột của người dùng, danh sách loại hình tổ chức và chỉ tiêu cho ô lọc.\n'
            '– Lấy dòng khai hạn mức của công ty có ít nhất một hạn mức > 0; ghép địa chỉ, người liên hệ; hạn mức trống = 0; '
            'Số dư nợ hiện tại = 0.\n'
            'After:\n– Hiển thị trang 1 (10 dòng), thứ tự khai hạn mức tăng dần, kèm “Hiển thị a–b / N”.\n'
            '– Lỗi máy chủ → hiển thị ' + M_LOADERR + '.'),
           ('Bấm Mã khách hàng', 'Click',
            'Before:\n– Mọi dòng đều có liên kết; không kiểm tra quyền riêng.\n'
            '– Lấy Từ ngày, Đến ngày đang chọn ở bộ lọc Thời gian (nếu có).\n'
            'During:\n– Mở cửa sổ theo NVKD và nạp công nợ của khách hàng (chi tiết mục 2.6).\n'
            'After:\n– Cửa sổ hiện trên màn báo cáo; bộ lọc, trang, sắp xếp của báo cáo giữ nguyên khi đóng cửa sổ.'),
           ('Bấm tiêu đề cột có sắp xếp', 'Click',
            'Before:\n– Chỉ 5 cột Mã khách hàng, Tên khách hàng, Hạn mức tính lãi, Hạn mức được nợ, Số dư nợ hiện tại sắp xếp được.\n'
            'During:\n– Lần bấm đầu sắp tăng dần; bấm lại cùng cột đổi giảm dần; giữ nguyên bộ lọc.\n'
            '– Chữ so tự nhiên không phân biệt hoa / thường; giá trị bằng nhau xếp tiếp theo thứ tự khai hạn mức.\n'
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
d.p('Bảng dưới mô tả cách hệ thống lấy từng cột số liệu của báo cáo. “Tập dữ liệu” là các dòng khai hạn mức công nợ của khách '
    'hàng cho công ty người đăng nhập, có ít nhất một hạn mức > 0, sau khi áp ô tìm nhanh, Khách hàng, Loại hình tổ chức, Chỉ tiêu '
    'vượt hạn mức. Màn không có icon ⓘ nào.')
d.data_table([
    ('Dòng “Hiển thị a–b / N”', 'N = số dòng của tập dữ liệu (mỗi khách hàng tối đa 1 dòng vì mỗi công ty chỉ khai 1 dòng hạn mức '
                                'cho 1 khách). Không phụ thuộc bộ lọc Thời gian.', '—'),
    ('Cột Hạn mức tính lãi', 'Giá trị “Hạn mức công nợ tính lãi” của dòng khai hạn mức công ty mình ở màn Khai báo hạn mức công nợ '
                             'khách hàng. Trống → 0.', '—'),
    ('Cột Hạn mức được nợ', 'Giá trị “Hạn mức công nợ xuất hàng” của dòng khai hạn mức công ty mình. Trống → 0.', '—'),
    ('Cột Số dư nợ hiện tại', 'Luôn 0 cho mọi dòng (giữ y hệt ERP — ERP gom công nợ sai nên luôn ra 0; người dùng chốt giữ '
                              'nguyên 22/10/2026). Từ ngày / Đến ngày không đổi kết quả.', '—'),
    ('Cột Người liên hệ', 'Tên mọi người liên hệ của khách hàng theo thứ tự khai, bỏ tên trùng.', '—'),
    ('Ràng buộc khớp số', 'Tổng công nợ ở cửa sổ theo NVKD KHÔNG bằng cột Số dư nợ hiện tại (cột này luôn 0, cửa sổ tính công nợ '
                          'thật theo sổ 131).', '—'),
])
k += 1
d.p('2.1.%d Danh sách popup mở từ số liệu' % k)
d.popup_table([
    ('Mã khách hàng ở cột Mã khách hàng (mọi dòng)', 'Chi tiết hạn mức dư nợ khách hàng theo NVKD (mục 2.6)',
     'Khách hàng đang nợ bao nhiêu, nợ thuộc NVKD nào để đôn đốc đúng người',
     'Công nợ của khách tách theo NVKD, tính tới Đến ngày của bộ lọc Thời gian (trống = toàn bộ); có dòng Tổng công nợ'),
])

# ------------------------------------------------------------ 2.2
k = fr(2, 'Tìm kiếm và lọc',
       rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
       intro=dict(ten='Tìm kiếm và lọc báo cáo hạn mức công nợ',
                  mota='Thu hẹp báo cáo theo mã / tên khách hàng (ô tìm nhanh) và 4 tiêu chí của khối Tìm kiếm nâng cao: Thời gian, '
                       'Khách hàng, Loại hình tổ chức, Chỉ tiêu vượt hạn mức. Kết quả luôn nằm trong phạm vi công ty của người dùng. '
                       'Thời gian chỉ dùng làm mốc cho cửa sổ theo NVKD, không lọc bảng chính.',
                  tacnhan=TN, dieukien=DK,
                  chinh='1. Người dùng nhập mã hoặc tên khách hàng vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc Enter).\n'
                        '2. Hoặc bấm Tìm kiếm nâng cao để mở khối tiêu chí, chọn giá trị một hoặc nhiều tiêu chí.\n'
                        '3. Các ô chọn của khối nâng cao lọc ngay khi giá trị đổi; ô Thời gian chỉ áp khi đã chọn đủ cả Từ ngày và Đến '
                        'ngày (hoặc xóa cả hai); ô tìm nhanh chỉ lọc khi bấm Tìm kiếm hoặc Enter.\n'
                        '4. Hệ thống quay về trang 1, nạp lại báo cáo và tổng số dòng theo toàn bộ tiêu chí đang có.\n'
                        '5. Hệ thống ghi tạm bộ lọc trên trình duyệt (giữ 10 phút khi tải lại trang).',
                  phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh và chiều sắp xếp, nạp lại từ trang 1.\n'
                      '• Không có kết quả → bảng hiện ' + M_EMPTY + '.\n'
                      '• Ô Khách hàng: gõ từ 2 ký tự mới gợi ý; gõ dưới 3 ký tự lấy tối đa 20 khách, từ 3 ký tự tối đa 50 khách; tìm '
                      'theo tên, số điện thoại hoặc mã trong TOÀN BỘ danh mục khách hàng, khách tạo gần nhất xếp trên.\n'
                      '• Chọn khách hàng không có hạn mức của công ty mình → bảng rỗng.\n'
                      '• Chọn Chỉ tiêu “Trong hạn mức được nợ”, “Vượt hạn mức tính lãi” hoặc “Vượt hạn mức công nợ” → luôn rỗng '
                      '(giữ y ERP vì số dư luôn 0).\n'
                      '• Tiêu chí bị tắt trong Cài đặt bộ lọc → không hiện ở khối nâng cao.\n'
                      '• Rời sang màn khác rồi quay lại → bộ lọc về trống; tải lại trang (F5) trong 10 phút → giữ bộ lọc.\n'
                      '• Đến ngày nhỏ hơn Từ ngày (gọi thẳng chức năng) → báo ' + M_DATE + '; trên giao diện lịch đã chặn chọn ngày sai.',
                  dacbiet='Kiểu khớp: ô tìm nhanh khớp MỘT PHẦN mã hoặc tên khách hàng (không tìm theo số điện thoại — #11766), không '
                          'phân biệt hoa / thường và không phân biệt dấu, tự bỏ khoảng trắng đầu / cuối; ký tự % và _ được hiểu đúng '
                          'là ký tự thường. Ô tìm nhanh không giới hạn số ký tự. Khách hàng, Loại hình tổ chức, Chỉ tiêu khớp CHÍNH XÁC.'),
       layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
                   shot_caption='Khối Bộ lọc danh sách đang mở Tìm kiếm nâng cao',
                   extra=[(shot('02d_customer'), 'Ô Khách hàng gợi ý khi gõ “29TPHPTH-1”'),
                          (shot('02b_target'), 'Lọc Chỉ tiêu “Trong hạn mức tính lãi” — còn 3 khách có hạn mức tính lãi > 0')]),
       ui=[('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', '“Bộ lọc danh sách”', '- Kèm biểu tượng phễu lọc'),
           ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
            ['- Gợi ý “Tìm theo mã, tên khách hàng”', '- Khớp một phần mã hoặc tên khách hàng', '- Chỉ lọc khi bấm Tìm kiếm hoặc Enter',
             '- Có nút × xóa nhanh khi đã nhập']),
           ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp giá trị ô tìm nhanh, về trang 1, nạp lại.'),
           ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Xóa toàn bộ tiêu chí kể cả ô tìm nhanh, khách hàng đã chọn, chiều sắp xếp', '- Xóa bộ lọc ghi tạm',
             '- Nạp lại từ trang 1']),
           ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Hiển thị',
            ['- Mở / thu gọn khối tiêu chí', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
           ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
           ('Thời gian', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
            ['- 1 ô gồm 2 lịch Từ ngày → Đến ngày', '- Lịch Từ ngày không cho chọn sau Đến ngày, lịch Đến ngày không cho chọn trước '
             'Từ ngày', '- Chọn 1 bên thì chưa nạp lại; đủ 2 bên hoặc xóa cả 2 mới nạp',
             '- Không lọc bảng chính; làm mốc tính công nợ ở cửa sổ theo NVKD']),
           ('Khách hàng', 'Dropdown', 'Enable', 'Gõ tối thiểu 2 ký tự', 'Không', 'Trống',
            ['- Mặc định: trống (tất cả), gợi ý “Gõ để tìm khách hàng...”', '- Gợi ý dạng “Mã - Tên”, tìm theo tên / số điện thoại / mã',
             '- Dưới 3 ký tự: tối đa 20 khách; từ 3 ký tự: tối đa 50 khách', '- Có nút × bỏ chọn',
             '- Chọn 1 khách → chỉ còn dòng của khách đó']),
           ('Loại hình tổ chức', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống',
            ['- Mặc định: trống (tất cả)'] + CTYPES),
           ('Chỉ tiêu vượt hạn mức', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống',
            ['- Mặc định: trống (tất cả)'] + TARGETS + ['- Chỉ “Trong hạn mức tính lãi” ra dòng (hạn mức tính lãi > 0); 3 giá trị '
                                                         'còn lại luôn rỗng (mục 2.2.6)']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', 'Hiện ' + M_EMPTY + ' khi không có kết quả.'),
           ('Thông báo khoảng ngày sai', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + M_DATE)],
       ev=[('Đổi giá trị một ô chọn nâng cao', 'Change',
            'Before:\n– Áp cho Khách hàng, Loại hình tổ chức, Chỉ tiêu vượt hạn mức.\n'
            'During:\n– Ghi nhận giá trị mới, ghi tạm bộ lọc; bỏ qua lần nạp trùng y hệt điều kiện đang hiển thị.\n'
            'After:\n– Quay về trang 1 và nạp lại báo cáo theo toàn bộ tiêu chí đang có.'),
           ('Chọn ô Thời gian', 'Change',
            'Before:\n– Mới chọn 1 trong 2 ngày → chưa nạp lại.\n'
            'During:\n– Đủ 2 ngày (hoặc xóa cả 2) → gửi Từ ngày, Đến ngày; máy chủ kiểm Đến ngày ≥ Từ ngày.\n'
            '– Sai → hiển thị ' + M_DATE + '\n' + ERR + '\n'
            'After:\n– Bảng chính không đổi số dòng; Từ ngày, Đến ngày được dùng khi mở cửa sổ theo NVKD.'),
           ('Bấm Tìm kiếm hoặc Enter', 'Click',
            'Before:\n– Lấy giá trị ô tìm nhanh (và các tiêu chí đang có).\n'
            'During:\n– Máy chủ bỏ khoảng trắng đầu / cuối, so khớp một phần mã hoặc tên khách hàng.\n'
            'After:\n– Quay về trang 1 và nạp lại báo cáo.'),
           ('Gõ ô Khách hàng', 'Change',
            'Before:\n– Gợi ý khi gõ từ 2 ký tự.\n'
            'During:\n– Tìm khách hàng có tên, số điện thoại hoặc mã chứa chuỗi gõ trong toàn bộ danh mục (dưới 3 ký tự tối đa 20, '
            'từ 3 ký tự tối đa 50, mới tạo trước).\n'
            'After:\n– Hiển thị gợi ý “Mã - Tên”; chọn 1 dòng thì lọc ngay.'),
           ('Bấm Làm mới', 'Click',
            'Before:\n– Không hỏi xác nhận.\n'
            'During:\n– Đặt lại toàn bộ tiêu chí về trống, bỏ khách hàng đã chọn, bỏ chiều sắp xếp, xóa bộ lọc ghi tạm.\n'
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
    ('Ô tìm nhanh', 'Dòng có mã khách hàng hoặc tên khách hàng chứa chuỗi gõ (không theo số điện thoại).', '—'),
    ('Khách hàng', 'Dòng hạn mức của đúng khách hàng đã chọn (so theo khách hàng, không theo dòng hạn mức).', '—'),
    ('Loại hình tổ chức', 'Dòng có loại khách hàng bằng giá trị đã chọn.', '—'),
    ('Chỉ tiêu: Trong hạn mức tính lãi', 'Số dư nợ hiện tại (= 0) nhỏ hơn hạn mức tính lãi → mọi dòng có hạn mức tính lãi > 0.', '—'),
    ('Chỉ tiêu: Trong hạn mức được nợ', 'Luôn rỗng — giữ y ERP (ERP so với một cột hạn mức không tồn tại).', '—'),
    ('Chỉ tiêu: Vượt hạn mức tính lãi', 'Luôn rỗng — số dư 0 không bao giờ lớn hơn hạn mức tính lãi.', '—'),
    ('Chỉ tiêu: Vượt hạn mức công nợ', 'Luôn rỗng — giữ y ERP như chỉ tiêu Trong hạn mức được nợ.', '—'),
    ('Thời gian', 'Không lọc bảng chính; được chuyển sang cửa sổ theo NVKD làm mốc Từ ngày (chia dư đầu kỳ) và Đến ngày (chặn '
                  'bút toán sau ngày này).', '—'),
])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(ten='Cài đặt các ô lọc hiển thị',
              mota='Cho phép mỗi người dùng tự chọn những tiêu chí lọc muốn thấy ở khối Tìm kiếm nâng cao và sắp xếp lại thứ tự '
                   'của chúng. Cấu hình lưu theo người dùng cho riêng màn này (4 tiêu chí: Thời gian, Khách hàng, Loại hình tổ chức, '
                   'Chỉ tiêu vượt hạn mức).',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
                    '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 4 tiêu chí kèm ô tích, theo cấu hình đang lưu.\n'
                    '3. Người dùng tích / bỏ tích và kéo thả để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình cho người dùng, hiển thị “Cập nhật thành công” và áp ngay lên khối Tìm kiếm nâng cao.',
              phu='• Bấm Khôi phục mặc định → tích lại đủ 4 tiêu chí theo thứ tự gốc; phải bấm Lưu mới có hiệu lực.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, không lưu thay đổi.\n'
                  '• Lưu thất bại → hiển thị “Thao tác thất bại”.\n'
                  '• Ẩn một tiêu chí đang có giá trị → giá trị đó bị xóa khỏi bộ lọc, báo cáo nạp lại.\n'
                  '• Tắt bớt còn ≤ 3 ô (tính cả ô tìm nhanh) → các ô bày thẳng trên 1 hàng, nút Tìm kiếm nâng cao ẩn; nút Cài '
                  'đặt bộ lọc vẫn còn để bật lại.',
              dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Cài đặt bộ lọc”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Tích chọn trường lọc muốn hiển thị; kéo ⠿ để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách tiêu chí', 'Table/Grid', 'Enable', '4 tiêu chí', 'Không', 'Theo cấu hình đã lưu',
        ['- Thời gian, Khách hàng, Loại hình tổ chức, Chỉ tiêu vượt hạn mức', '- Mỗi mục đánh số thứ tự 1, 2, 3, 4',
         '- Ô tìm nhanh mã, tên khách hàng không nằm trong danh sách (luôn hiện)']),
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
              mota='Cho phép mỗi người dùng bật / tắt và kéo sắp xếp 9 cột của bảng báo cáo, lưu theo người dùng. Hai cột STT, '
                   'Mã khách hàng bị khóa (luôn hiện, không đổi vị trí).',
              tacnhan=TN, dieukien=DK,
              chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
                    '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 9 cột kèm ô tích theo cấu hình đang áp dụng.\n'
                    '3. Người dùng tích / bỏ tích, kéo biểu tượng ba gạch để đổi thứ tự.\n'
                    '4. Người dùng bấm Lưu.\n'
                    '5. Hệ thống ghi cấu hình, hiển thị “Cập nhật thành công”, vẽ lại bảng.',
              phu='• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, danh sách cột trả về cấu hình đang áp dụng.\n'
                  '• Cột khóa (STT, Mã khách hàng): ô tích xám, không bỏ tích, không kéo được; di chuột hiện “Cột bắt buộc — không '
                  'thể ẩn hoặc đổi vị trí”.\n'
                  '• Lưu thất bại → hiển thị “Thao tác thất bại”.\n'
                  '• Cấu hình lưu trên máy chủ theo tài khoản: giữ sau khi tải lại (F5), đổi trình duyệt / máy khác vẫn giữ; tài '
                  'khoản khác không bị ảnh hưởng.\n'
                  '• Ẩn cột thì cửa sổ Xuất Excel không tích sẵn trường tương ứng (vẫn tích thêm được).\n'
                  '• Đổi cột không làm thay đổi dữ liệu, tổng số dòng, bộ lọc đang áp.',
              dacbiet='Không có cột mặc định ẩn: lần đầu cả 9 cột đều tích. Cột STT, Mã khách hàng ghim trái khi cuộn ngang.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.'),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Tuỳ chỉnh cột”', 'Kèm nút (x) đóng ở góc phải.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Tích chọn cột cần hiển thị, kéo ≡ để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', '9 cột', '–', 'Theo cấu hình',
        ['- STT, Mã khách hàng (khóa), Tên khách hàng, Địa chỉ, Người liên hệ, Số điện thoại, Hạn mức tính lãi, Hạn mức được nợ, '
         'Số dư nợ hiện tại']),
       ('Ô tích của cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo cấu hình',
        ['- Tích: cột hiện trên bảng', '- Cột STT, Mã khách hàng: ô tích xám, không bỏ được']),
       ('Biểu tượng ba gạch', 'Icon Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Kéo để đổi vị trí cột', '- Cột STT, Mã khách hàng hiện biểu tượng ổ khóa, không kéo được']),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi cột.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi cột trừ STT, Mã khách hàng.'),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/9 cột”, n = số cột đang tích.'),
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
        'Before:\n– Cột STT, Mã khách hàng không kéo được.\nDuring:\n– Đổi thứ tự cột trong cửa sổ.\n'
        'After:\n– Chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bỏ tích một cột', 'Change',
        'Before:\n– Cột STT, Mã khách hàng không cho bỏ tích.\nDuring:\n– Ghi nhận trạng thái trong cửa sổ, cập nhật dòng đếm.\n'
        'After:\n– Chưa áp lên bảng cho tới khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình gắn với người dùng và màn này; không cần quyền riêng.\n'
        'During:\n– Ghi cấu hình; lỗi → hiển thị “Thao tác thất bại”.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng theo cấu hình mới.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Bỏ thay đổi chưa lưu.\n'
        'After:\n– Đóng cửa sổ; lần mở sau hiện lại đúng cấu hình đang áp dụng.')])

# ------------------------------------------------------------ 2.5
fr(5, 'Xuất Excel', usecase=('FR-05', 'Xuất Excel', 'io', A_ND),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(ten='Xuất báo cáo hạn mức công nợ khách hàng ra Excel',
              mota='Người dùng chọn trường và thứ tự cột trong cửa sổ “Chọn trường xuất file” rồi tải file Excel gồm TOÀN BỘ dòng '
                   'báo cáo khớp bộ lọc đang áp dụng (không riêng trang đang xem), trong phạm vi công ty của người dùng. File dựng '
                   'ngay trên trình duyệt.',
              tacnhan=TN, dieukien=DK + '\n4. Báo cáo có ít nhất 1 dòng khớp bộ lọc (rỗng thì không tạo file).',
              chinh='1. Người dùng lọc báo cáo (nếu cần) rồi bấm Xuất Excel trên thanh công cụ của bảng.\n'
                    '2. Hệ thống mở cửa sổ “Chọn trường xuất file”, tích sẵn các trường đang hiện trên bảng (theo đúng thứ tự trên '
                    'bảng), các trường đang ẩn xếp sau và không tích.\n'
                    '3. Người dùng tích / bỏ tích, kéo đổi thứ tự, bấm Xuất file.\n'
                    '4. Hệ thống đóng cửa sổ, khóa nút Xuất Excel, lấy toàn bộ dòng theo bộ lọc + sắp xếp đang áp dụng (theo từng đợt, '
                    'hiện tiến độ), lấy letterhead công ty người đăng nhập.\n'
                    '5. Hệ thống tải file “bao-cao-han-muc-cong-no-khach-hang.xlsx”, hiển thị “Xuất Excel thành công.”.',
              phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
                  '• Bấm Đóng / (x) / click ra ngoài cửa sổ → không xuất.\n'
                  '• Không có dòng khớp bộ lọc → KHÔNG tạo file, hiển thị “Không có dữ liệu để xuất”.\n'
                  '• Lỗi → hiển thị câu lỗi máy chủ trả, hoặc “Lỗi khi xuất Excel”; mở khóa nút.\n'
                  '• Không lấy được letterhead → vẫn xuất file, tiêu đề lên dòng 1.',
              dacbiet='Cấu trúc file (sheet “Han muc cong no KH”): dòng 1 letterhead công ty người đăng nhập (rộng bằng bảng); dòng 2 '
                      'tiêu đề “BÁO CÁO HẠN MỨC CÔNG NỢ KHÁCH HÀNG”; dòng 3 hàng tên cột gồm STT rồi các trường đã chọn đúng thứ tự '
                      '(có nút lọc); dữ liệu ngay sau; cuối file khối “Ngày ..., tháng ..., năm ...” / “Người lập” / “(Ký, họ tên)”. '
                      'Hạn mức, Số dư nợ là ô số #,##0 (cộng được bằng SUM); Số điện thoại giữ số 0 đầu; người liên hệ mỗi tên 1 dòng '
                      'trong ô. Mỗi đợt lấy tối đa 5.000 dòng, không giới hạn tổng số dòng. Khóa nút Xuất Excel trong lúc chờ file.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.',
               extra=[(shot('20b_export_empty'), 'Báo cáo rỗng: bấm Xuất file báo “Không có dữ liệu để xuất”')]),
   ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '“Chọn trường xuất file”', 'Kèm biểu tượng tải xuống và nút (x) đóng.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '“Tích chọn trường cần xuất, kéo ≡ để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', '8 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- Mã khách hàng, Tên khách hàng, Địa chỉ, Người liên hệ, Số điện thoại, Hạn mức tính lãi, Hạn mức được nợ, Số dư nợ hiện '
         'tại', '- STT luôn có trong file, không nằm trong danh sách', '- Trường đang hiện trên bảng tích sẵn, xếp trước']),
       ('Ô tích của trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Theo cột đang hiện', 'Tích: trường có trong file.'),
       ('Tay nắm kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Chữ gợi ý “Kéo để đổi vị trí cột trong file”', '- Thứ tự trong danh sách = thứ tự cột trong file']),
       ('Dòng đếm', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '“Đang chọn n/8 trường”.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ tích mọi trường.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → đóng cửa sổ rồi tải file']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.'),
       ('Tiến độ xuất', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Cạnh nút Xuất Excel, chỉ hiện khi đang xuất', '- “Đang chuẩn bị dữ liệu…”, “Đã tải x/y dòng…”, “Đang dựng file x/y dòng…”']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công.”', '- Rỗng: “Không có dữ liệu để xuất”', '- Lỗi: “Lỗi khi xuất Excel” hoặc câu máy chủ trả'])],
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
        'During:\n– Lấy toàn bộ dòng theo bộ lọc + sắp xếp đang áp dụng, phạm vi công ty của người dùng, mỗi đợt tối đa 5.000 dòng; '
        'cập nhật tiến độ.\n'
        '– Bỏ qua trường lạ không có trong danh sách; STT luôn đứng đầu.\n'
        '– Không có dòng → không tạo file, hiển thị “Không có dữ liệu để xuất”.\n' + ERR + '\n'
        'After:\n– Dựng file: letterhead, tiêu đề, hàng tên cột, dữ liệu, khối ký; tải “bao-cao-han-muc-cong-no-khach-hang.xlsx”.\n'
        '– Hiển thị “Xuất Excel thành công.”; mở khóa nút. Lỗi → “Lỗi khi xuất Excel” hoặc câu máy chủ trả.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ; lần mở sau tích lại theo cột đang hiện.')])

# ------------------------------------------------------------ 2.6
k = fr(6, 'Xem chi tiết hạn mức dư nợ theo NVKD',
       usecase=('FR-06', 'Xem chi tiết hạn mức dư nợ theo NVKD', 'view', A_ND),
       rule=('- Màn Xem chi tiết, Popup và Sắp xếp dữ liệu bảng.', 'detail'),
       intro=dict(ten='Xem công nợ của khách hàng tách theo nhân viên kinh doanh',
                  mota='Bấm Mã khách hàng trên một dòng báo cáo để mở cửa sổ “Chi tiết hạn mức dư nợ khách hàng <Mã> - <Tên> theo '
                       'NVKD”: mỗi NVKD (người lập hợp đồng) có bút toán công nợ với khách hàng là một dòng, kèm Bộ phận, Phòng ban, '
                       'Công nợ và dòng Tổng công nợ. Công nợ tính theo sổ 131 tới Đến ngày của bộ lọc Thời gian. Cửa sổ chỉ đọc.',
                  tacnhan=TN,
                  dieukien=DK + '\n4. Khách hàng đang có dòng hạn mức > 0 của công ty người dùng (là dòng trên báo cáo).',
                  chinh='1. Người dùng bấm Mã khách hàng ở cột Mã khách hàng.\n'
                        '2. Hệ thống mở cửa sổ, tiêu đề ghép mã và tên khách hàng, ô Chọn nhân viên trống, bảng chưa sắp theo cột nào.\n'
                        '3. Hệ thống kiểm tra khách hàng có hạn mức của công ty người dùng; lấy các bút toán sổ 131 của khách tới Đến '
                        'ngày (trống = toàn bộ), dùng Từ ngày (trống = hôm nay) làm mốc chia dư đầu kỳ, gom theo NVKD.\n'
                        '4. Hệ thống tính Công nợ (dư cuối kỳ) từng NVKD; bút toán không gắn NVKD mà dư khác 0 gom vào dòng “Chưa xác '
                        'định nhân viên”; nạp danh sách ô Chọn nhân viên = các NVKD có trong cửa sổ.\n'
                        '5. Hệ thống hiển thị bảng và dòng “Tổng công nợ: <tổng>” dưới bảng.\n'
                        '6. Người dùng chọn nhân viên / bấm tiêu đề Công nợ để lọc / sắp; bấm Đóng để về báo cáo.',
                  phu='• Khách hàng không có bút toán công nợ → bảng ' + M_EMPTY + ', không hiện dòng Tổng công nợ.\n'
                      '• Chọn nhân viên → chỉ còn dòng của nhân viên đó, Tổng công nợ tính lại theo dòng còn lại; bấm × bỏ chọn → '
                      'hiện lại đủ.\n'
                      '• Bấm tiêu đề Công nợ → sắp tăng dần, bấm lại giảm dần.\n'
                      '• Khách hàng không thuộc báo cáo của công ty mình (gọi thẳng) hoặc máy chủ lỗi → hiển thị ' + M_LOADERR + '.\n'
                      '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng; lần mở sau ô Chọn nhân viên và sắp xếp về mặc định.\n'
                      '• Công nợ có thể âm (khách trả thừa).',
                  dacbiet='Tổng công nợ trong cửa sổ KHÔNG khớp cột Số dư nợ hiện tại của báo cáo (cột đó luôn 0 — giữ y ERP). '
                          'Công nợ tính trên toàn sổ 131 của khách hàng, không bó theo công ty của hạn mức (giữ y ERP). Mở cửa sổ '
                          'nhiều lần liên tiếp chỉ lấy kết quả của lần mở sau cùng.'),
       layout=dict(menu=MENU + ' => Mã khách hàng', shot=shot('03_popup'),
                   shot_caption='Cửa sổ Chi tiết hạn mức dư nợ khách hàng 29TPHPTH-1 theo NVKD',
                   note='Modal Chi tiết hạn mức dư nợ khách hàng theo NVKD được mở ngay trên màn hình báo cáo theo đường dẫn ở trên.',
                   extra=[(shot('03b_popup_filter'), 'Cửa sổ lọc theo nhân viên Đào Phúc Sơn')]),
       ui=[('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Theo khách hàng',
            ['- “Chi tiết hạn mức dư nợ khách hàng <Mã> - <Tên> theo NVKD”', '- Kèm biểu tượng nhóm người và nút (x) đóng']),
           ('Ô Chọn nhân viên', 'Dropdown', 'Enable', 'Danh sách NVKD trong cửa sổ', 'Không', 'Trống',
            ['- Mặc định: trống (tất cả), gợi ý “Chọn nhân viên”', '- Lựa chọn dạng “Mã - Tên”, chỉ gồm NVKD đang có dòng',
             '- Có nút × bỏ chọn', '- Đổi giá trị → nạp lại cửa sổ']),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Số thứ tự 1, 2, 3… (không phân trang)'),
           ('Cột Mã nhân viên', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
            ['- Mã NVKD', '- Trống ở dòng “Chưa xác định nhân viên”']),
           ('Cột Tên nhân viên', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
            ['- Họ tên NVKD', '- “Chưa xác định nhân viên” cho bút toán không gắn NVKD']),
           ('Cột Bộ phận', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Bộ phận của NVKD', '- Trống khi chưa gắn bộ phận']),
           ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Phòng ban của NVKD'),
           ('Cột Công nợ', 'Table/Grid', 'Read-only', 'Số, có thể âm', '–', 'Theo dữ liệu',
            ['- Dư cuối kỳ của khách với NVKD tới Đến ngày', '- Căn phải, phân cách hàng nghìn; 0 vẫn hiện “0”',
             '- Sắp xếp được; mở cửa sổ chưa sắp']),
           ('Dòng Tổng công nợ', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu',
            ['- “Tổng công nợ: <tổng>” dưới bảng, căn phải', '- = tổng cột Công nợ của các dòng đang hiện',
             '- Ẩn khi bảng rỗng hoặc đang tải']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- ' + M_EMPTY),
           ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Góc phải chân cửa sổ; đóng cửa sổ.'),
           ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', 'Như nút Đóng.'),
           ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + M_LOADERR)],
       ev=[('Bấm Mã khách hàng', 'Click',
            'Before:\n– Kiểm tra khách hàng có dòng hạn mức > 0 của công ty người dùng; không có → ' + M_LOADERR + ' và dừng.\n'
            '– Lấy Từ ngày, Đến ngày đang chọn ở bộ lọc Thời gian.\n'
            'During:\n– Gom bút toán sổ 131 của khách tới Đến ngày theo NVKD, tính Công nợ; dòng không gắn NVKD dư khác 0 → “Chưa xác '
            'định nhân viên”.\n' + ERR + '\n'
            'After:\n– Hiển thị bảng chưa sắp, Tổng công nợ, danh sách ô Chọn nhân viên.'),
           ('Chọn nhân viên', 'Change',
            'Before:\n– Giá trị mới khác giá trị cũ và cửa sổ đang mở.\n'
            'During:\n– Nạp lại, giữ chiều sắp đang chọn; chỉ giữ dòng của nhân viên đã chọn.\n'
            'After:\n– Bảng và Tổng công nợ cập nhật; danh sách ô Chọn nhân viên giữ đủ.'),
           ('Bấm tiêu đề cột Công nợ', 'Click',
            'Before:\n– Chỉ cột Công nợ sắp xếp được.\n'
            'During:\n– Lần đầu tăng dần, bấm lại giảm dần; nạp lại kèm nhân viên đang chọn.\n'
            'After:\n– Bảng xếp theo Công nợ, mũi tên ở cột Công nợ.'),
           ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
            'Before:\n– Không hỏi xác nhận (cửa sổ chỉ đọc).\n'
            'During:\n– Hủy kết quả nạp còn dở; xóa ô Chọn nhân viên.\n'
            'After:\n– Đóng cửa sổ; báo cáo giữ nguyên bộ lọc, trang, sắp xếp.')])
d.p('2.6.%d Mục đích thiết kế popup' % k)
d.bullets([
    'Trả lời câu hỏi: khách hàng đang có hạn mức này thực tế nợ bao nhiêu và khoản nợ thuộc NVKD nào (để giao đúng người đôn đốc, '
    'xem ai sắp chạm hạn mức).',
    'Là cửa sổ nổi để giữ nguyên ngữ cảnh báo cáo (bộ lọc, trang, sắp xếp) — xem xong đóng là quay lại đúng chỗ, không phải chuyển '
    'màn.',
    'Ràng buộc khớp số: Tổng công nợ = tổng cột Công nợ của các dòng trong cửa sổ; KHÔNG khớp cột Số dư nợ hiện tại của báo cáo '
    '(luôn 0, giữ y ERP). Cùng mốc Từ ngày / Đến ngày với bộ lọc Thời gian của báo cáo.',
    'Người dùng làm tiếp: lọc theo nhân viên, sắp theo Công nợ; mỗi lần mở là cửa sổ mới (không giữ nhân viên / sắp xếp lần trước). '
    'Cửa sổ không có xuất Excel, không có liên kết sang chứng từ.',
])
k += 1
d.p('2.6.%d Các biến thể theo con số bấm' % k)
d.popup_variant_table([
    ('Mã khách hàng ở bất kỳ dòng nào, bộ lọc Thời gian trống', 'Mọi NVKD có bút toán công nợ với khách hàng, tính tới hiện tại',
     '“Chi tiết hạn mức dư nợ khách hàng <Mã> - <Tên> theo NVKD”', 'Không ẩn ô nào; ô Chọn nhân viên trống'),
    ('Mã khách hàng khi bộ lọc Thời gian có Từ ngày – Đến ngày', 'NVKD có bút toán tới Đến ngày; công nợ là dư cuối kỳ tới Đến ngày',
     'Như trên', 'Không ẩn ô nào; khoảng ngày không hiện trong cửa sổ'),
])
k += 1
d.p('2.6.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('“Tập dữ liệu” là các bút toán tài khoản 131 và tài khoản con trực tiếp của khách hàng đã bấm, tới hết Đến ngày của bộ lọc Thời '
    'gian (trống = toàn bộ), gom theo NVKD (người lập hợp đồng ghi trên bút toán). Không bó theo công ty.')
d.data_table([
    ('Cột Công nợ (dòng NVKD)', 'Dư cuối kỳ = dư đầu kỳ (Nợ − Có trước Từ ngày; Từ ngày trống = hôm nay) + phát sinh tăng hàng hóa / '
                                'dịch vụ + điều chỉnh công nợ tăng − nhập trả lại − điều chỉnh công nợ giảm − đã thanh toán + trả '
                                'lại tiền thừa, từ Từ ngày tới Đến ngày. Có thể âm.', '—'),
    ('Dòng “Chưa xác định nhân viên”', 'Bút toán không gắn NVKD, chỉ hiện khi dư khác 0.', '—'),
    ('Ô Chọn nhân viên', 'Các NVKD có dòng trong cửa sổ (không gồm dòng Chưa xác định), dạng “Mã - Tên”.', '—'),
    ('Dòng Tổng công nợ', 'Tổng cột Công nợ của các dòng đang hiện (sau khi lọc nhân viên).', '—'),
])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Báo cáo hạn mức công nợ khách hàng; không lặp lại các quy tắc đã có '
           'trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Điều kiện dòng lên báo cáo', [
        '– Dòng khai hạn mức của khách hàng cho công ty = công ty làm việc của người đăng nhập.',
        '– Hạn mức tính lãi > 0 hoặc hạn mức được nợ > 0; cả hai bằng 0 / trống thì không lên.',
        '– Chưa gắn công ty → không có dòng nào.'],
     ['Xem báo cáo', 'Xuất Excel']),
    ('BR-02', 'Số dư nợ hiện tại giữ y ERP', [
        '– Luôn bằng 0 cho mọi dòng, không đổi theo Thời gian (người dùng chốt 22/10/2026, #11777).',
        '– Công nợ thật xem ở cửa sổ theo NVKD.'],
     ['Xem báo cáo', 'Xuất Excel']),
    ('BR-03', 'Chỉ tiêu vượt hạn mức', [
        '– Trong hạn mức tính lãi: số dư (0) < hạn mức tính lãi → dòng có hạn mức tính lãi > 0.',
        '– Trong hạn mức được nợ, Vượt hạn mức tính lãi, Vượt hạn mức công nợ: luôn rỗng (giữ y ERP).'],
     ['Tìm kiếm và lọc', 'Xuất Excel']),
    ('BR-04', 'Bộ lọc Thời gian', [
        '– Không lọc bảng chính và file Excel.',
        '– Chuyển sang cửa sổ NVKD: Từ ngày làm mốc chia dư đầu kỳ (trống = hôm nay), Đến ngày chặn bút toán sau ngày đó.',
        '– Chỉ áp khi chọn đủ 2 ngày; Đến ngày phải ≥ Từ ngày.'],
     ['Tìm kiếm và lọc', 'Xem chi tiết hạn mức dư nợ theo NVKD']),
    ('BR-05', 'Công nợ theo NVKD', [
        '– Gom bút toán sổ 131 của khách hàng theo người lập hợp đồng; dư cuối kỳ theo công thức chung các báo cáo công nợ khách hàng.',
        '– Bút toán không gắn NVKD dư khác 0 → dòng “Chưa xác định nhân viên”.',
        '– Không bó theo công ty của hạn mức (giữ y ERP).'],
     ['Xem chi tiết hạn mức dư nợ theo NVKD']),
    ('BR-06', 'Chặn xem công nợ khách bất kỳ', [
        '– Cửa sổ NVKD chỉ mở cho khách hàng có dòng hạn mức > 0 của công ty mình; khách khác → “Lỗi khi tải dữ liệu”.'],
     ['Xem chi tiết hạn mức dư nợ theo NVKD']),
    ('BR-07', 'Chuẩn hóa dữ liệu tìm kiếm', [
        '– Ô tìm nhanh: khớp một phần mã / tên khách hàng, bỏ khoảng trắng đầu / cuối, không phân biệt hoa / thường và dấu; % và _ là '
        'ký tự thường; không tìm theo số điện thoại.',
        '– Ô Khách hàng: tìm toàn bộ danh mục theo tên / số điện thoại / mã; dưới 3 ký tự tối đa 20, từ 3 ký tự tối đa 50.',
        '– Loại hình tổ chức, Chỉ tiêu, Khách hàng đã chọn: khớp chính xác.'],
     ['Tìm kiếm và lọc']),
    ('BR-08', 'Hiển thị số và dòng', [
        '– Hạn mức trống hiện 0; số phân cách hàng nghìn bằng dấu phẩy.',
        '– Địa chỉ ghép số nhà, thôn, phường, (quận nếu ở nước ngoài), tỉnh, quốc gia; người liên hệ mỗi tên 1 lần.',
        '– Thứ tự mặc định: thứ tự khai hạn mức tăng dần; cửa sổ NVKD mở ra chưa sắp.'],
     ['Xem báo cáo', 'Xem chi tiết hạn mức dư nợ theo NVKD']),
    ('BR-09', 'Ghi nhớ bộ lọc', [
        '– Bộ lọc, trạng thái khối nâng cao ghi tạm 10 phút trên trình duyệt; tải lại trang thì khôi phục.',
        '– Rời sang màn khác hoặc bấm Làm mới → xóa.'],
     ['Tìm kiếm và lọc']),
    ('BR-10', 'Tính duy nhất', [
        '– Mỗi khách hàng tối đa 1 dòng hạn mức cho mỗi công ty nên báo cáo không có 2 dòng cùng khách.',
        '– Mã khách hàng do danh mục khách hàng quản lý, duy nhất.'],
     ['Xem báo cáo']),
    ('BR-11', 'Liên kết cha – con', [
        '– Khách hàng > dòng hạn mức theo công ty > công nợ theo NVKD.',
        '– Xóa hết hạn mức (về 0) ở màn Khai báo → dòng rời báo cáo; báo cáo không xóa được gì.'],
     ['Xem báo cáo', 'Xem chi tiết hạn mức dư nợ theo NVKD']),
    ('BR-12', 'File Excel', [
        '– Trường do người dùng chọn, đúng thứ tự, STT luôn đầu; tiền là ô số #,##0; số điện thoại giữ số 0 đầu.',
        '– Rỗng thì không tạo file, báo “Không có dữ liệu để xuất”.',
        '– Letterhead theo công ty người đăng nhập.'],
     ['Xuất Excel']),
    ('BR-13', 'Không ghi lịch sử', [
        '– Màn chỉ đọc nên không có Lịch sử thay đổi; lịch sử khai hạn mức nằm ở màn Khai báo hạn mức công nợ khách hàng.'],
     ['Xem báo cáo']),
    ('BR-14', 'Khác hệ thống ERP (có chủ đích)', [
        '– Lọc Khách hàng so đúng khách hàng (ERP so nhầm với dòng hạn mức).',
        '– Cửa sổ NVKD: đúng khách hàng, tách đúng theo NVKD, cùng công thức sổ 131 (ERP truyền nhầm, cộng dồn sai).',
        '– Người liên hệ không lặp tên; thêm ô tìm nhanh, Xuất Excel chọn trường, Tùy chỉnh cột; ô Khách hàng ≥ 3 ký tự chặn 50.'],
     ['Xem báo cáo', 'Tìm kiếm và lọc', 'Xem chi tiết hạn mức dư nợ theo NVKD']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng Danh sách các màn hình tham chiếu dữ liệu')
d.p('Báo cáo hạn mức công nợ khách hàng chỉ đọc, không ghi dữ liệu. Các màn hình dưới đây cung cấp dữ liệu cho báo cáo (dòng khai báo hạn mức và bút toán công nợ phải thu 131).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Tài chính', 'Khai báo hạn mức công nợ KH (nguồn duy nhất của báo cáo: dòng hạn mức của công ty người dùng, có hạn mức tính lãi hoặc hạn mức được nợ > 0; sửa / xóa dòng khai báo thì báo cáo đổi theo ở lần tải sau)', 'Tài chính -> Kế toán công nợ -> Khách hàng'),
    ('2', 'Tài chính', 'Các chứng từ ghi sổ công nợ phải thu 131 — Phiếu thu tiền, Phiếu báo có, Phiếu kế toán… (bút toán của khách tới Đến ngày, theo người lập hợp đồng, dùng tính Công nợ ở cửa sổ theo NVKD)', 'Tài chính -> Quản lý tiền; Tài chính -> Sổ tổng hợp'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
