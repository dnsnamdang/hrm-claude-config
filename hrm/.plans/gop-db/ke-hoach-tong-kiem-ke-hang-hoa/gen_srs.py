# -*- coding: utf-8 -*-
"""SRS màn "Kế hoạch tổng kiểm kê hàng hóa" (mã phiếu <mã công ty>.KHTKK-NNNNN) — form chuẩn Danh mục quốc gia, chuẩn 04/11/2026.

Chạy: python gen_srs.py  → SRS - Kế hoạch tổng kiểm kê hàng hóa.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc
  ../ke-hoach-kiem-ke-theo-hang-hoa/gen_srs.py (05/11, Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn).
Nguồn đọc 05/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Entities/SelfInventoryRequest/SelfInventoryRequestAll.php (+ 3 quyền dùng chung ở SelfInventoryRequest.php),
      Services/SelfInventoryRequestAll{,Write,Print}Service.php, Http/Controllers/V1/SelfInventoryRequestAllController.php,
      Http/Requests/SelfInventoryRequest/SelfInventoryRequestAllStoreRequest.php, Services/SelfInventoryService.php (popup chọn kế
      hoạch + nạp kế hoạch tổng vào phiếu kiểm kê), Services/SelfInventoryWriteService.php (lưu phiếu kiểm kê gắn kế hoạch tổng,
      chặn hàng trùng), Services/SelfInventoryReportService.php (báo cáo hàng thừa thiếu lọc theo kế hoạch tổng)},
      MasterData PhysicalWarehouse (chặn xóa kho), app/Services/CatalogHistoryService.php, app/Support/NotificationMeta.php,
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (3 quyền)
  FE  pages/finance/self-inventory-request-alls/** (index, create, _id/index, _id/edit, components/{SelfInventoryRequestAllForm,
      row-actions.js, export-excel.js}), components/subsystem-menu/finance.js (nhóm Kiểm kê)
Phân biệt: màn "Kế hoạch kiểm kê theo hàng hóa" (/finance/self-inventory-requests) dùng BẢNG RIÊNG, chỉ dùng CHUNG 3 tên quyền.
Ảnh: ./khtkkhh_shots — dev-hrm 05/11/2026 (_capture/capture.js, chặn mọi yêu cầu ghi). Giả trạng thái trên trình duyệt (sửa phản hồi
  GET, không gửi máy chủ): 12_edit, 13_delete, 03_rowmenu (dev chỉ có kế hoạch Đã duyệt). 10b_validate: gán sẵn lỗi trên form đúng câu
  máy chủ trả khi Lưu và duyệt form trống (không bấm Lưu).
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

TEN = 'Kế hoạch tổng kiểm kê hàng hóa'
SHOTS = os.path.join(HERE, 'khtkkhh_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Kiểm kê => Kế hoạch tổng kiểm kê hàng hóa'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Kế hoạch tổng kiểm kê hàng hóa.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NOTFOUND = '“Không tìm thấy kế hoạch tổng kiểm kê hoặc bạn không có quyền xem.”'
REQ = '“Bắt buộc phải nhập”'
Q1 = 'Lập phiếu kiểm kê kho theo hàng hóa'
V1 = 'Tổng kiểm kê kho theo hàng hóa - tổng công ty'
V2 = 'Tổng kiểm kê kho theo hàng hóa'
LAP = 'Lập phiếu kiểm kê hàng hóa'

A_NV = 'Người lập kế hoạch'
A_TK = 'Người lập phiếu kiểm kê'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng đã được cấp tài khoản (màn không gắn quyền thao tác); phạm vi '
      'xem theo quyền “%s” / “%s”.' % (V1, V2))
TN_OWNER = 'Người dùng có quyền thực hiện chức năng: người lập kế hoạch (người tạo phiếu), phiếu đang ở trạng thái Đang tạo.'
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Kế hoạch tổng kiểm kê hàng hóa.\n'
      '3. Dữ liệu hiển thị trong phạm vi xem theo quyền (mục Phần 2).')

d = SrsDoc(out=OUT, menu=MENU, route='/finance/self-inventory-request-alls', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Kiểm kê': 'menu_nhom', 'Kế hoạch tổng kiểm kê hàng hóa': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Lưu và duyệt': 'btn_luuduyet', 'Sửa': 'btn_sua_row',
    'Xóa': 'btn_xoa_row', 'Xem chi tiết': 'link_sophieu', LAP: 'btn_lapphieu_row',
    'In': 'btn_in_row', 'In danh sách': 'btn_in_list', 'Xuất Excel': 'btn_xuatexcel', 'Lịch sử': 'btn_lichsu_row',
}.items()})

UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    """Biểu đồ Use Case 1 chức năng theo khổ mẫu quốc gia (actor + 1 use case)."""
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None, extra=None):
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
    if 'entries' in layout:
        d.p('Đường dẫn màn hình:')
        for m, note in layout['entries']:
            d._menu_para(m)
            d.p(note)
        d.figure(layout['shot'], layout['shot_caption'], width_in=6.2)
    else:
        d.layout(**layout)
    for img, cap in (extra or []):
        d.figure(img, cap, width_in=6.2)
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Kế hoạch tổng kiểm kê hàng hóa (mã phiếu <mã công ty>.KHTKK-NNNNN, ví dụ '
    'TPE.KHTKK-00005), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ cách người lập kế hoạch khai khoảng thời gian kiểm kê (Ngày kiểm kê từ – đến), chọn một hoặc nhiều kho, các công ty '
    'thuê kho (tự chọn theo kho), các phòng ban tham gia và nội dung yêu cầu, rồi Lưu và duyệt để người có quyền lập phiếu kiểm '
    'kê theo hàng hóa cho đợt tổng kiểm kê.',
    'Làm rõ vòng đời trạng thái của kế hoạch (Đang tạo → Đã duyệt) và cách màn Kiểm kê theo hàng hóa, báo cáo Hàng thừa thiếu sau '
    'tổng kiểm kê dùng lại kế hoạch.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo kế hoạch (Lưu nháp / Lưu và tiếp tục), '
    'Lưu và duyệt, Chỉnh sửa, Xóa, Xem chi tiết, Lập phiếu kiểm kê hàng hóa từ kế hoạch (mở màn Kiểm kê theo hàng hóa), In phiếu / '
    'In danh sách, Xuất Excel danh sách, Xem lịch sử thay đổi. Màn KHÔNG có bước Duyệt / Không duyệt riêng (nút Lưu và duyệt chuyển '
    'thẳng Đã duyệt), không có Hủy, Khóa / Mở khóa, Import Excel và Xuất Excel 1 phiếu.')
d.p('Khác với màn Kế hoạch kiểm kê theo hàng hóa (cùng nhóm menu Kiểm kê): màn này lưu dữ liệu riêng, KHÔNG có danh sách hàng '
    'hóa, tồn kho, hội đồng kiểm kê; chỉ có 2 trạng thái; phiếu kiểm kê lập từ kế hoạch không đổi trạng thái kế hoạch và một kế '
    'hoạch lập được nhiều phiếu kiểm kê. Hai màn chỉ dùng chung 3 tên quyền ở Phần 2.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Kế hoạch là căn cứ để lập các phiếu kiểm kê theo hàng hóa của đợt tổng kiểm kê: phiếu kiểm kê nạp sẵn kho, công ty thuê kho, '
    'nội dung yêu cầu của kế hoạch; người lập phiếu tự thêm hàng.',
    'Báo cáo Hàng thừa thiếu sau tổng kiểm kê hàng hóa lọc kết quả theo kế hoạch tổng.',
    'Kế hoạch không ghi tồn kho, không sinh phiếu nhập / xuất.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Phạm vi xem theo quyền tổng công ty / công ty; không quyền chỉ thấy phiếu mình tạo; phiếu Đang tạo chỉ người tạo thấy (BR-02).',
    'Chỉ người tạo được Sửa / Xóa và chỉ khi phiếu còn Đang tạo (BR-04).',
    'Lưu nháp chỉ bắt Ngày kiểm kê từ / đến; Lưu và duyệt bắt đủ 6 trường (BR-03).',
    'Nút Lập phiếu kiểm kê hàng hóa chỉ hiện khi kế hoạch Đã duyệt, người xem có quyền lập phiếu và Ngày kiểm kê từ chưa qua '
    '(từ hôm nay trở đi) (BR-09).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Kế hoạch tổng kiểm kê hàng hóa (kế hoạch)', 'Chứng từ <mã công ty>.KHTKK-NNNNN của màn này: thời gian kiểm kê, các kho, công '
                                                 'ty thuê kho, thành phần tham gia, nội dung yêu cầu.'),
    ('Phiếu kiểm kê theo hàng hóa', 'Phiếu lập từ kế hoạch ở màn Kiểm kê theo hàng hóa (phân hệ Kho) để nhập kết quả thực kiểm; '
                                    'một kế hoạch có thể có nhiều phiếu.'),
    ('Ngày kiểm kê từ / đến', 'Khoảng thời gian dự kiến kiểm kê; Ngày kiểm kê đến không trước Ngày kiểm kê từ.'),
    ('Kho', 'Kho vật lý; chỉ chọn được kho đang hoạt động có kho kế toán thuộc công ty người đăng nhập.'),
    ('Công ty thuê kho', 'Công ty có kho kế toán trong các kho đã chọn; hiển thị bằng mã công ty (vd TPE, TPHP).'),
    ('Thành phần tham gia', 'Các phòng ban tham gia đợt kiểm kê (phòng ban đang hoạt động của mọi công ty).'),
    ('Nội dung yêu cầu', 'Mô tả yêu cầu của đợt kiểm kê, tối đa 255 ký tự.'),
    ('Trạng thái Đang tạo', 'Nhãn xám: kế hoạch lưu bằng Lưu nháp / Lưu và tiếp tục; chỉ người tạo thấy, sửa, xóa.'),
    ('Trạng thái Đã duyệt', 'Nhãn xanh lá: kế hoạch lưu bằng Lưu và duyệt; không sửa / xóa được; dùng để lập phiếu kiểm kê.'),
    ('Cấu trúc phân cấp', 'Kế hoạch > các kho > các công ty thuê kho (thuộc kho đã chọn); kế hoạch > các phòng ban tham gia; '
                          'kế hoạch > các phiếu kiểm kê theo hàng hóa lập từ kế hoạch.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn không gắn quyền cho thao tác Tạo / Sửa / Xóa / In / Xuất / Lịch sử: mọi người dùng đăng nhập đều lập được kế hoạch. '
    'Hai quyền xem chỉ quyết định PHẠM VI dữ liệu; quyền “%s” (nhóm Kiểm kê theo hàng hóa, phân hệ Kho) quyết định nút %s và '
    'người nhận thông báo. Super admin được coi như có đủ quyền. Ba tên quyền này cũng được màn Kế hoạch kiểm kê theo hàng hóa '
    'dùng (kiểm trong code: cùng hằng quyền).' % (Q1, LAP))
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1,
     'Thấy nút %s ở kế hoạch Đã duyệt còn hạn; nhận thông báo khi kế hoạch được Lưu và duyệt bởi người cùng công ty; xem được '
     'chi tiết mọi kế hoạch Đã duyệt dù ngoài phạm vi xem (để bấm thông báo).' % LAP),
    ('—', 'Không cần quyền', 'Tạo mới, Lưu nháp, Lưu và duyệt, Lưu và tiếp tục; Sửa / Xóa khi là người tạo và phiếu Đang tạo; In, '
                              'Xuất Excel, Lịch sử với phiếu trong phạm vi xem.'),
], widths=[0.8, 1.8, 3.4])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Mọi kế hoạch của mọi công ty; ô lọc Công ty chọn được mọi công ty (Super admin như V1).'),
    ('V2', V2, 'Kế hoạch của công ty người xem + kế hoạch mình tạo; công ty người xem trống → chỉ kế hoạch mình tạo.'),
    ('—', 'Không có quyền nào', 'Chỉ kế hoạch do chính mình tạo.'),
], widths=[0.8, 2.2, 3.0])
d.p('Với mọi quyền: kế hoạch Đang tạo chỉ hiện với chính người tạo.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1', 'V2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ (theo V)', '✅ mọi công ty', '✅ công ty mình + của mình', '✅ chỉ của mình'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅ (có ô Công ty – Phòng ban)', '✅ (có ô Công ty – Phòng ban, khóa công ty)', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo kế hoạch', '✅', '✅', '✅', '✅'),
    ('FR-06 Lưu và duyệt', '✅', '✅', '✅', '✅'),
    ('FR-07 Chỉnh sửa', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo'),
    ('FR-08 Xóa', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo'),
    ('FR-09 Xem chi tiết', '✅ + kế hoạch Đã duyệt', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-10 Lập phiếu kiểm kê hàng hóa', '✅ Đã duyệt, còn hạn', '❌', '❌', '❌'),
    ('FR-11 In phiếu / In danh sách', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-12 Xuất Excel danh sách', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-13 Xem lịch sử thay đổi', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('Duyệt / Không duyệt riêng / Hủy / Khóa – Mở khóa / Import', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.9, 1.1, 1.0, 1.1, 0.9])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có V1 / V2: vẫn vào màn, chỉ thấy kế hoạch mình tạo; không có ô lọc Công ty – Phòng ban.',
    'Mở chi tiết / sửa / in / lịch sử của kế hoạch ngoài phạm vi (qua đường link): hệ thống báo ' + NOTFOUND +
    '; màn chi tiết / sửa chuyển sang trang “Không tìm thấy trang”.',
    'Sửa / Xóa kế hoạch không phải mình tạo hoặc không còn Đang tạo: nút không hiện; nếu vẫn gửi yêu cầu (mở 2 tab) → báo ' +
    CONFLICT + '. Mở màn Sửa của phiếu đó → tự chuyển về màn chi tiết.',
    'Thiếu Q1: nút %s không hiện; mở thẳng màn Tạo phiếu kiểm kê kèm kế hoạch → không nạp được kế hoạch.' % LAP,
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới, Xuất Excel, In danh sách, Cấu hình cột', 'Luôn hiện', 'Không gắn quyền'),
    ('Nút Sửa, Xóa (dòng và màn chi tiết)', 'Người xem là người tạo và phiếu Đang tạo', 'Máy chủ kiểm lại khi lưu / xóa'),
    ('Nút ' + LAP, 'Phiếu Đã duyệt, người xem có Q1 (hoặc Super admin), Ngày kiểm kê từ ≥ hôm nay',
     'Mở màn Tạo phiếu kiểm kê theo hàng hóa, cùng tab'),
    ('Nút In, Lịch sử trên dòng', 'Mọi dòng', 'Tối đa 3 nút hiện thẳng, còn lại vào menu “Hành động khác”'),
    ('Ô lọc Công ty – Phòng ban', 'Có V1 hoặc V2 (V2: công ty bị khóa theo công ty mình)', 'Fail-closed: không quyền thì ẩn'),
], widths=[2.2, 2.3, 1.5])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_NV, [0, 1, 2, 3, 4, 6, 7]), (A_TK, [0, 5])],
    [('FR-01', 'Xem danh sách kế hoạch', 'view'),
     ('FR-05', 'Tạo kế hoạch', 'crud'),
     ('FR-06', 'Lưu và duyệt', 'action'),
     ('FR-07', 'Chỉnh sửa kế hoạch', 'crud'),
     ('FR-08', 'Xóa kế hoạch', 'action'),
     ('FR-10', 'Lập phiếu kiểm kê', 'action'),
     ('FR-11', 'In phiếu / In danh sách', 'io'),
     ('FR-12', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-09', 'Xem chi tiết', 'view', 'extend', [0], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Kế hoạch tổng kiểm kê hàng hóa')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách kế hoạch',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách kế hoạch tổng kiểm kê hàng hóa',
       mota='Hiển thị bảng các kế hoạch tổng kiểm kê hàng hóa trong phạm vi xem của người dùng (theo quyền tổng công ty / công ty '
            '/ của mình), kèm thời gian kiểm kê, các kho, nội dung yêu cầu, trạng thái, người tạo, ngày tạo / cập nhật, phân trang '
            'và tổng số. Mỗi dòng có liên kết sang màn chi tiết và các nút thao tác theo trạng thái phiếu.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng vào màn từ menu hoặc từ thông báo.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem theo quyền (V1 / V2 / của mình), luôn ẩn kế hoạch Đang tạo của người khác.\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu vừa đi vào màn con của màn này) và cấu hình cột đã '
             'lưu của người dùng.\n'
             '4. Hệ thống lấy kế hoạch khớp bộ lọc, sắp kế hoạch tạo gần nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, kèm dòng “Hiển thị a–b / N”, phân trang và nút thao tác theo trạng thái.',
       phu='• Không có kế hoạch nào khớp → trong bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Máy chủ lỗi khi nạp danh sách → thông báo “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”, bảng trống.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
           '• Phiên đăng nhập hết hạn khi đang thao tác → thông báo hết phiên, hệ thống xóa phiên và chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 11 cột (STT, Số phiếu, Ngày kiểm kê, Kho, Nội dung yêu cầu, Trạng thái, Người tạo, Ngày tạo, '
               'Ngày cập nhật, Người cập nhật, Hành động); không có cột ẩn mặc định. Cột khóa (không ẩn, không đổi vị trí): STT, '
               'Số phiếu, Hành động; Số phiếu ghim trái khi cuộn ngang. Sắp xếp được: Số phiếu, Ngày kiểm kê (theo Ngày kiểm kê '
               'từ); mặc định (chưa chọn cột) ngày tạo mới nhất ở trên. Nội dung yêu cầu dài kẹp 2 dòng, rê chuột xem đủ. Đổi sắp '
               'xếp / bộ lọc / số dòng đều về trang 1.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Kế hoạch tổng kiểm kê hàng hóa'),
   extra=[(shot('03_rowmenu'), 'Nút thao tác theo trạng thái: dòng Đang tạo (Sửa, Xóa, Hành động khác) và dòng Đã duyệt')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Kế hoạch tổng kiểm kê hàng hóa” trên tiêu đề bảng và tab trình duyệt (không có chữ “Danh sách”)']),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “Tạo kế hoạch tổng kiểm kê hàng hóa”', '- Bấm → mở màn Tạo kế hoạch (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.12)',
         '- Khóa trong lúc đang xuất file']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “In danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.11)']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Đánh số liên tục theo trang', '- Cột khóa trong Tùy chỉnh cột']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', '<mã công ty>.KHTKK-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết (mục 2.9)', '- Sắp xếp được', '- Cột khóa, ghim trái khi cuộn ngang']),
       ('Cột Ngày kiểm kê', 'Table/Grid', 'Read-only', 'dd/mm/yyyy - dd/mm/yyyy', 'Hiển thị',
        ['- Ngày kiểm kê từ - Ngày kiểm kê đến', '- Sắp xếp được (theo Ngày kiểm kê từ)']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Tên các kho của kế hoạch, nối bằng dấu phẩy theo thứ tự đã chọn', '- Không sắp xếp']),
       ('Cột Nội dung yêu cầu', 'Table/Grid', 'Read-only', '0–255 ký tự', 'Hiển thị',
        ['- Rộng 320px, kẹp 2 dòng', '- Rê chuột xem đủ nội dung', '- Không sắp xếp']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 2 giá trị', 'Hiển thị',
        ['- Đang tạo: nhãn xám', '- Đã duyệt: nhãn xanh lá', '- Không sắp xếp']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Họ tên người lập kế hoạch', '- Không sắp xếp']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', ['- Thời điểm lưu lần đầu', '- Không sắp xếp']),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        '- Thời điểm cập nhật gần nhất; không sắp xếp.'),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Họ tên người cập nhật gần nhất.'),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Sửa (bút chì): chỉ phiếu Đang tạo của chính mình → mở màn Sửa (mục 2.7)',
           '- Xóa (thùng rác đỏ): cùng điều kiện → hộp Xác nhận xóa (mục 2.8)',
           '- ' + LAP + ': phiếu Đã duyệt còn hạn, người xem có Q1 (mục 2.10)',
           '- In, Lịch sử: mọi dòng (mục 2.11, 2.13)',
           '- Hiện thẳng tối đa 3 nút; nhiều hơn thì nút cuối là “Hành động khác” (ba chấm) chứa phần còn lại',
           '- Cột khóa trong Tùy chỉnh cột']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', ['- Trong bảng: “Không có dữ liệu phù hợp.”', '- Chỉ hiện khi N = 0']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang đang xem', '- N: tổng số kế hoạch khớp bộ lọc trong phạm vi xem']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Ở trang đầu nút về đầu / lùi mờ; ở trang cuối nút tiến / về cuối mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.” khi máy chủ lỗi.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định phạm vi xem: V1 (hoặc Super admin) → mọi công ty; V2 → công ty mình + của mình; không quyền → của mình.\n'
        '– Khôi phục bộ lọc (10 phút) và cấu hình cột đã lưu.\n'
        'During:\n– Lấy kế hoạch khớp bộ lọc; ẩn kế hoạch Đang tạo của người khác.\n'
        '– Máy chủ lỗi → hiển thị “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, kế hoạch tạo mới nhất ở trên, nút thao tác theo cờ từng phiếu.'),
       ('Bấm Số phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem.\n'
        'After:\n– Mở màn chi tiết (mục 2.9); bộ lọc được ghi nhớ 10 phút để khôi phục khi quay lại.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Số phiếu, Ngày kiểm kê hỗ trợ sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại một lần theo số dòng mới.'),
       ('Bấm Hành động khác (ba chấm)', 'Click',
        'Before:\n– Dòng có nhiều hơn 3 nút thao tác (dòng Đang tạo: Sửa, Xóa, In, Lịch sử).\n'
        'After:\n– Mở menu các nút còn lại (In / Lịch sử).'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc kế hoạch',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách kế hoạch',
       mota='Thu hẹp danh sách theo số phiếu, kho, trạng thái, người tạo, mã hàng hóa, tên hàng hóa, ngày tạo và công ty – phòng '
            'ban. Ô tìm nhanh tìm theo số phiếu; các ô lọc nằm trong khối Tìm kiếm nâng cao, bật / tắt được bằng Cài đặt bộ lọc '
            '(mục 2.3). Mã / Tên hàng hóa tìm theo hàng trong các phiếu kiểm kê đã lập từ kế hoạch (kế hoạch tổng không có hàng).',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập số phiếu vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Hệ thống lọc ngay khi một ô chọn đổi giá trị, về trang 1; ô chữ Mã hàng hóa / Tên hàng hóa áp khi bấm Tìm kiếm.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Không có quyền V1 / V2 → không có ô Công ty – Phòng ban; có V2 → ô Công ty khóa ở công ty mình.\n'
           '• Kế hoạch chưa lập phiếu kiểm kê nào → không bao giờ khớp ô Mã hàng hóa / Tên hàng hóa.\n'
           '• Ô lọc bị tắt trong Cài đặt bộ lọc → không hiện trên khối lọc.',
       dacbiet='Ô tìm nhanh / Mã hàng hóa / Tên hàng hóa khớp một phần, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối; '
               'không giới hạn số ký tự; ký tự % và _ được hiểu là ký tự đại diện. Kho lọc kế hoạch có chứa kho đó. Ngày tạo lấy '
               'trọn hai ngày biên (theo ngày tạo kế hoạch, KHÔNG phải ngày kiểm kê). Phòng ban lọc theo phòng ban của người lập. '
               'Mọi điều kiện kết hợp kiểu VÀ. Ghi nhớ bộ lọc trên trình duyệt 10 phút khi đi vào màn con của màn này.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số phiếu”', '- Khớp một phần số phiếu', '- Áp khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh và các ô chữ, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Bấm → xóa mọi tiêu chí kể cả ô tìm nhanh', '- Nạp lại từ trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Kho', 'Dropdown', 'Enable', 'Danh sách kho', 'Không', 'Trống',
        ['- Mặc định: trống (mọi kho)', '- Hiển thị “Mã - Tên”, gồm mọi kho trong danh mục', '- Ra kế hoạch có chứa kho đã chọn']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (mọi trạng thái)', '- Lựa chọn: Đang tạo / Đã duyệt']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Toàn bộ nhân viên (kể cả người chưa tạo kế hoạch nào)']),
       ('Mã hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        '- Kế hoạch có ít nhất 1 phiếu kiểm kê chứa hàng có mã chứa chuỗi nhập.'),
       ('Tên hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        '- Kế hoạch có ít nhất 1 phiếu kiểm kê chứa hàng có tên chứa chuỗi nhập.'),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lọc theo ngày tạo kế hoạch, lấy trọn hai ngày biên; được bỏ trống một đầu']),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Ẩn khi thiếu quyền',
        ['- Chỉ hiện khi có V1 hoặc V2', '- V2: khóa ở công ty mình (biểu tượng ổ khóa)']),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Phòng ban của công ty', 'Không', 'Ẩn khi thiếu quyền',
        '- Lọc kế hoạch theo phòng ban của người lập.'),
   ],
   ev=[
       ('Đổi giá trị một ô chọn', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\n'
        'During:\n– Bỏ qua khi giá trị không đổi.\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí (một lần).'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, Mã hàng hóa, Tên hàng hóa, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm kế hoạch có số phiếu chứa chuỗi nhập (và phiếu kiểm kê con có hàng khớp mã / tên).\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nAfter:\n– Xóa mọi tiêu chí, bỏ sắp xếp, nạp lại từ trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\nAfter:\n– Mở / thu gọn khối ô lọc; lần mở đầu nạp lựa chọn Trạng thái, Kho.'),
       ('Quay lại từ màn con trong 10 phút', 'System',
        'Before:\n– Người dùng vừa đi từ danh sách vào màn chi tiết / tạo / sửa.\n'
        'After:\n– Khôi phục bộ lọc và trạng thái khối lọc; quá 10 phút thì bộ lọc về trống.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự. Cấu hình lưu riêng theo '
            'người dùng cho màn này, không ảnh hưởng người khác và không đổi dữ liệu kế hoạch.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 7 mục lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 7 mục theo thứ tự thiết kế; phải bấm Lưu mới có hiệu lực.\n'
           '• Bỏ tích mục đang có giá trị lọc → mục bị ẩn và giá trị lọc của mục đó bị bỏ.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bỏ thay đổi chưa lưu.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Cài đặt bộ lọc”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách 7 mục', '–', 'Theo cấu hình đã lưu',
        ['- Kho, Trạng thái, Người tạo, Mã hàng hóa', '- Tên hàng hóa, Ngày tạo, Công ty – Phòng ban']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → mục đó không hiện ở khối Tìm kiếm nâng cao.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích lại đủ 7 mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình đang lưu (chưa lưu lần nào → đủ 7 mục).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\n'
        'During:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ 7 mục, thứ tự thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 11 cột của bảng danh sách. Ba cột STT, Số phiếu, Hành động bị khóa; '
            'cấu hình lưu riêng theo người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 11 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 11 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ nguyên sau khi tải lại trang, đăng '
               'nhập lại, đổi trình duyệt; người dùng khác không bị ảnh hưởng. Cột đang hiện cũng là các trường được tích sẵn '
               'khi Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 11 cột', '–', 'Theo cấu hình đã lưu',
        ['- STT, Số phiếu, Ngày kiểm kê, Kho, Nội dung yêu cầu, Trạng thái',
         '- Người tạo, Ngày tạo, Ngày cập nhật, Người cập nhật, Hành động']),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Số phiếu, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/11 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu của người dùng.'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Cột khóa không đổi được vị trí.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change', 'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/11 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5 Tạo kế hoạch
FORM_UI = [
    ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     ['- Tạo: “Tạo kế hoạch tổng kiểm kê hàng hóa”', '- Sửa: “Sửa kế hoạch tổng kiểm kê hàng hóa: <số phiếu>”']),
    ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập',
     '- Góc phải khối Thông tin chung: màn Tạo ghi tên người đăng nhập; màn Sửa ghi “<Người tạo> - dd/mm/yyyy hh:mm”.'),
    ('Số phiếu', 'Textbox', 'Disable', '<mã công ty>.KHTKK-NNNNN', '–', 'Ẩn ở màn Tạo',
     ['- Chỉ có ở màn Sửa / Chi tiết, ô khóa', '- Mã tự sinh lúc tạo, không đổi khi sửa']),
    ('Ngày kiểm kê từ', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Trống',
     ['- Gợi ý “Chọn ngày kiểm kê từ”', '- Bắt buộc ở cả Lưu nháp và Lưu và duyệt', '- Lỗi: ' + REQ]),
    ('Ngày kiểm kê đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Trống',
     ['- Gợi ý “Chọn ngày kiểm kê đến”', '- Lịch làm mờ các ngày trước Ngày kiểm kê từ',
      '- Bắt buộc ở cả Lưu nháp và Lưu và duyệt', '- Lỗi: ' + REQ + ' / “Phải lớn hơn hoặc bằng Ngày kiểm kê từ.”']),
    ('Kho', 'Dropdown', 'Enable', 'Danh sách kho', 'Có', 'Trống',
     ['- Chọn được NHIỀU kho; gợi ý “Chọn kho”; hiển thị “Mã - Tên”',
      '- Chỉ kho đang hoạt động có kho kế toán thuộc công ty người đăng nhập (màn Sửa: luôn có kho phiếu đang gắn)',
      '- Đổi kho → Công ty thuê kho tự chọn lại hết công ty của các kho mới', '- Bắt buộc khi Lưu và duyệt; lỗi: ' + REQ]),
    ('Công ty thuê kho', 'Dropdown', 'Enable / Disable', 'Công ty thuê các kho đã chọn', 'Có', 'Khóa khi chưa chọn kho',
     ['- Chọn được nhiều; hiển thị mã công ty, mỗi công ty 1 lần dù thuê nhiều kho',
      '- Chưa chọn kho: khóa, gợi ý “Chọn kho trước”; đã chọn kho: gợi ý “Chọn công ty thuê kho”',
      '- Bắt buộc khi Lưu và duyệt; lỗi: ' + REQ + ' / “Có công ty không thuê các kho đã chọn.”']),
    ('Thành phần tham gia', 'Dropdown', 'Enable', 'Phòng ban đang hoạt động', 'Có', 'Trống',
     ['- Chọn được nhiều; gợi ý “Chọn phòng ban”; hiển thị “Mã - Tên”', '- Gồm phòng ban của mọi công ty',
      '- Bắt buộc khi Lưu và duyệt; lỗi: ' + REQ]),
    ('Nội dung yêu cầu', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     ['- Gợi ý “Nhập nội dung yêu cầu”, 2 dòng', '- Không gõ quá 255 ký tự', '- Bắt buộc khi Lưu và duyệt',
      '- Lỗi: ' + REQ + ' / “Vui lòng nhập tối đa 255 ký tự.”']),
    ('Dấu * trên nhãn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     '- Cả 6 ô có dấu *; Lưu nháp chỉ bắt 2 ô ngày, Lưu và duyệt bắt đủ 6 ô.'),
    ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Rê chuột: “Lưu kế hoạch ở trạng thái Đang tạo”', '- Lưu xong về danh sách; khóa trong lúc lưu']),
    ('Nút Lưu và duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Màu chính; rê chuột: “Lưu và chuyển kế hoạch sang trạng thái Đã duyệt”', '- Đặc tả ở mục 2.6']),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị ở màn Tạo',
     ['- Rê chuột: “Lưu nháp rồi ở lại tạo kế hoạch tiếp theo”', '- Không có ở màn Sửa']),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi “Thông tin chưa lưu”.'),
    ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Nội dung: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút Thoát: rời màn, không lưu',
      '- Nút Ở lại / (x): đóng hộp, giữ dữ liệu']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Thành công: “Thêm mới thành công.” (tạo) / “Cập nhật thành công.” (sửa) / “Lưu và duyệt thành công.”',
      '- Thiếu / sai: “Bạn chưa nhập đầy đủ thông tin.”', '- Phiếu đã đổi trạng thái: ' + CONFLICT,
      '- Lỗi khác: câu lỗi của máy chủ hoặc “Lưu thất bại.”']),
]

SAVE_DURING = ('During:\n– Ngày kiểm kê từ / đến trống → ' + REQ + ' dưới ô.\n'
               '– Ngày kiểm kê đến trước Ngày kiểm kê từ → “Phải lớn hơn hoặc bằng Ngày kiểm kê từ.”\n'
               '– Nội dung yêu cầu quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”\n'
               '– Kho / công ty / phòng ban không còn tồn tại → “Không hợp lệ”; công ty không thuê kho nào đã chọn → “Có công ty '
               'không thuê các kho đã chọn.”\n'
               '– Mọi lỗi hiện cùng lúc dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin.”, cuộn tới ô lỗi đầu tiên.\n' + ERR)

fr(5, 'Tạo kế hoạch tổng kiểm kê (Lưu nháp / Lưu và tiếp tục)', usecase=('FR-05', 'Tạo kế hoạch', 'crud', A_NV),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo kế hoạch tổng kiểm kê hàng hóa',
       mota='Người lập khai Ngày kiểm kê từ – đến, chọn các kho (Công ty thuê kho tự chọn theo kho), Thành phần tham gia và Nội '
            'dung yêu cầu rồi bấm Lưu nháp: kế hoạch được lưu ở trạng thái Đang tạo (chỉ người tạo thấy), chưa báo cho ai. Lưu '
            'nháp chỉ bắt hai ô ngày để người lập lưu dở và hoàn thiện sau.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Công ty của người dùng có ít nhất 1 kho đang hoạt động có kho kế toán '
                '(để chọn Kho khi duyệt).\n3. Không cần quyền riêng để tạo.',
       chinh='1. Người dùng bấm Tạo mới ở danh sách.\n'
             '2. Hệ thống mở màn “Tạo kế hoạch tổng kiểm kê hàng hóa”: mọi ô trống, Công ty thuê kho khóa, góc phải ghi tên người '
             'tạo.\n'
             '3. Người dùng chọn Ngày kiểm kê từ, Ngày kiểm kê đến (lịch làm mờ ngày trước Ngày kiểm kê từ).\n'
             '4. Người dùng chọn Kho (một hoặc nhiều); hệ thống mở khóa và tự chọn hết Công ty thuê kho của các kho đó.\n'
             '5. Người dùng bỏ bớt công ty nếu cần, chọn Thành phần tham gia, nhập Nội dung yêu cầu.\n'
             '6. Người dùng bấm Lưu nháp.\n'
             '7. Hệ thống kiểm tra dữ liệu, lưu kế hoạch trạng thái Đang tạo với công ty / phòng ban của người tạo, sinh mã '
             '<mã công ty>.KHTKK-NNNNN; lưu các kho, công ty thuê kho, phòng ban tham gia.\n'
             '8. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu.\n'
             '9. Hệ thống hiển thị “Thêm mới thành công.” và chuyển về màn danh sách.',
       phu='• Bấm Lưu và tiếp tục → lưu như Lưu nháp (Đang tạo), báo “Thêm mới thành công.”, ở lại màn Tạo với form trắng.\n'
           '• Thiếu ngày / ngày sai → báo lỗi dưới từng ô cùng lúc, thông báo “Bạn chưa nhập đầy đủ thông tin.”, không lưu.\n'
           '• Bấm Quay lại / chuyển menu / đóng tab khi đã nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì thì về '
           'danh sách ngay.\n'
           '• Màn là trang riêng, không có (x) / click ra ngoài.\n'
           '• Lỗi máy chủ → thông báo câu lỗi hoặc “Lưu thất bại.”, dữ liệu đã nhập giữ nguyên.',
       dacbiet='Các nút lưu khóa trong lúc đang lưu để một lần bấm không tạo 2 kế hoạch. Kế hoạch không có trường nhập duy nhất: '
               'mã tự sinh theo công ty người tạo + số thứ tự, không sửa được; 2 kế hoạch cùng kho, cùng thời gian vẫn lưu được. '
               'Chọn trùng kho / công ty / phòng ban trong một kế hoạch bị chặn (“Bị trùng.”). Không popup xác nhận khi lưu.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'),
               shot_caption='Màn Tạo kế hoạch sau khi chọn ngày, kho, công ty thuê kho, thành phần tham gia'),
   extra=[(shot('10_create'), 'Màn Tạo kế hoạch lúc mới mở'),
          (shot('10d_dateto'), 'Lịch Ngày kiểm kê đến làm mờ các ngày trước Ngày kiểm kê từ'),
          (shot('10b_validate'), 'Lỗi bắt buộc hiện cùng lúc dưới từng ô (Lưu và duyệt khi form trống)'),
          (shot('10g_unsaved'), 'Hộp “Thông tin chưa lưu” khi rời màn')],
   ui=FORM_UI[:2] + FORM_UI[3:],
   ev=[
       ('Mở màn Tạo', 'System',
        'Before:\n– Không cần quyền riêng.\nDuring:\n– Nạp danh sách kho của công ty, công ty thuê từng kho, phòng ban đang hoạt '
        'động, người tạo.\n– Lỗi → “Không tải được dữ liệu.”.\nAfter:\n– Hiển thị form trống; chưa tính là đã thay đổi.'),
       ('Chọn Ngày kiểm kê từ', 'Change',
        'Before:\n– Bỏ qua khi giá trị không đổi.\nAfter:\n– Ghi nhận ngày, xóa lỗi đỏ của 2 ô ngày; lịch Ngày kiểm kê đến làm mờ '
        'ngày trước đó.'),
       ('Chọn Kho', 'Change',
        'Before:\n– Bỏ qua khi danh sách kho không đổi.\n'
        'After:\n– Mở khóa Công ty thuê kho, tự chọn lại HẾT công ty có kho kế toán trong các kho đã chọn (bỏ lựa chọn cũ); xóa '
        'lỗi đỏ của Kho và Công ty thuê kho. Bỏ hết kho → Công ty thuê kho khóa và trống.'),
       ('Chọn Công ty thuê kho / Thành phần tham gia', 'Change',
        'Before:\n– Chỉ chọn trong danh sách gợi ý.\nAfter:\n– Ghi nhận lựa chọn, xóa lỗi đỏ của ô.'),
       ('Bấm Lưu nháp', 'Click',
        'Before:\n– Không kiểm quyền riêng; khóa các nút lưu.\n– Chỉ bắt Ngày kiểm kê từ / đến; các ô còn lại được để trống.\n'
        + SAVE_DURING + '\n'
        'After:\n– Lưu kế hoạch trạng thái Đang tạo, sinh số phiếu, lưu kho, công ty thuê kho, phòng ban.\n'
        '– Ghi một dòng lịch sử “Tạo mới”.\n– Hiển thị “Thêm mới thành công.”, về màn danh sách.'),
       ('Bấm Lưu và tiếp tục', 'Click',
        'Before:\n– Như Lưu nháp.\nDuring:\n– Kiểm tra như Lưu nháp.\n' + ERR + '\n'
        'After:\n– Lưu như Lưu nháp (Đang tạo), ghi lịch sử “Tạo mới”, hiển thị “Thêm mới thành công.”, làm trắng form và ở lại '
        'màn Tạo.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu hiện tại với lúc mở màn.\nDuring:\n– Có thay đổi → hiện hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu; Ở lại: giữ nguyên form.'),
   ])

# ------------------------------------------------------------ 2.6 Lưu và duyệt
fr(6, 'Lưu và duyệt (chuyển kế hoạch sang Đã duyệt)', usecase=('FR-06', 'Lưu và duyệt', 'action', A_NV),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lưu và duyệt (chuyển trạng thái Đã duyệt)',
       mota='Ở màn Tạo hoặc Sửa, nút Lưu và duyệt lưu kế hoạch và chuyển thẳng sang trạng thái Đã duyệt (không có người duyệt '
            'riêng): kế hoạch hiện với người có quyền xem, người có quyền Lập phiếu kiểm kê kho theo hàng hóa cùng công ty nhận '
            'thông báo để lập phiếu kiểm kê. Lưu và duyệt bắt đủ 6 trường. Không có hộp xác nhận (giữ như hệ thống cũ).',
       tacnhan=TN + ' Sửa rồi duyệt: chỉ người tạo khi phiếu Đang tạo.',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo, hoặc màn Sửa của kế hoạch Đang tạo do mình tạo.\n'
                '3. Đủ 6 trường: Ngày kiểm kê từ, Ngày kiểm kê đến, Kho, Công ty thuê kho, Thành phần tham gia, Nội dung yêu cầu.',
       chinh='1. Người dùng nhập đủ thông tin (như mục 2.5) và bấm Lưu và duyệt.\n'
             '2. Hệ thống kiểm tra đủ 6 trường bắt buộc và các quy tắc định dạng / nghiệp vụ.\n'
             '3. Hệ thống lưu kế hoạch với trạng thái Đã duyệt (màn Tạo: sinh số phiếu; màn Sửa: kiểm lại phiếu còn Đang tạo và '
             'đúng người tạo).\n'
             '4. Hệ thống ghi nhận hành động trong lịch sử của phiếu: màn Tạo “Tạo mới”; màn Sửa “Thay đổi thông tin” (nếu đổi '
             'dữ liệu) và “Thay đổi trạng thái” Đang tạo → Đã duyệt.\n'
             '5. Hệ thống gửi thông báo “[KHTKK] Đã duyệt: <số phiếu>” (ghi chú: Người lập, “Cần lập phiếu kiểm kê”, Thời gian, '
             'Kho tối đa 3 tên + “và N kho khác”, Ghi chú) cho nhân viên có quyền ' + Q1 + ' cùng công ty người lưu; bấm thông '
             'báo mở chi tiết kế hoạch.\n'
             '6. Hệ thống hiển thị “Lưu và duyệt thành công.” và chuyển về màn danh sách.',
       phu='• Thiếu trường → mọi ô thiếu viền đỏ + ' + REQ + ' cùng lúc, thông báo “Bạn chưa nhập đầy đủ thông tin.”, không lưu, '
           'không gửi.\n'
           '• Phiếu đã bị đổi trạng thái / không còn là người tạo (sửa ở tab khác) → ' + CONFLICT + ', không lưu.\n'
           '• Người lưu không có công ty / không ai có quyền → vẫn lưu thành công, không ai nhận thông báo.\n'
           '• Gửi thông báo lỗi → không ảnh hưởng việc lưu.',
       dacbiet='Không có hộp xác nhận; nút khóa trong lúc lưu. Sau khi Đã duyệt kế hoạch không sửa / xóa được nữa và không có '
               'luồng trả về Đang tạo. Màn Tạo không có “Lưu và duyệt rồi tiếp tục”.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới => Lưu và duyệt', 'Duyệt ngay khi tạo kế hoạch.'),
       (MENU + ' => Sửa => Lưu và duyệt', 'Duyệt kế hoạch Đang tạo đã lưu nháp trước đó.')],
       shot=shot('10b_validate'), shot_caption='Lưu và duyệt khi thiếu dữ liệu: 6 ô báo lỗi cùng lúc'),
   ui=[
       ('Nút Lưu và duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Màu chính, biểu tượng dấu tích tròn', '- Rê chuột: “Lưu và chuyển kế hoạch sang trạng thái Đã duyệt”',
         '- Khóa trong lúc lưu']),
       ('Ngày kiểm kê từ / đến', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Như mục 2.5', '- Lỗi thiếu: ' + REQ + '.'),
       ('Kho', 'Dropdown', 'Enable', 'Danh sách kho', 'Có', 'Như mục 2.5', '- Ít nhất 1 kho; lỗi thiếu: ' + REQ + '.'),
       ('Công ty thuê kho', 'Dropdown', 'Enable', 'Công ty thuê các kho đã chọn', 'Có', 'Như mục 2.5',
        ['- Ít nhất 1 công ty; lỗi thiếu: ' + REQ, '- Công ty không thuê kho đã chọn: “Có công ty không thuê các kho đã chọn.”']),
       ('Thành phần tham gia', 'Dropdown', 'Enable', 'Phòng ban', 'Có', 'Như mục 2.5', '- Ít nhất 1 phòng ban; lỗi thiếu: ' + REQ + '.'),
       ('Nội dung yêu cầu', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Như mục 2.5', '- Lỗi thiếu: ' + REQ + '.'),
       ('Viền đỏ ô lỗi', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Viền đỏ + câu lỗi dưới ô', '- Sửa ô nào thì lỗi ô đó biến mất ngay']),
       ('Trạng thái sau khi lưu', 'Badge', 'Read-only', '–', '–', 'Đã duyệt', '- Nhãn xanh lá “Đã duyệt” ở danh sách.'),
       ('Thông báo cho người lập phiếu kiểm kê', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tiêu đề “[KHTKK] Đã duyệt: <số phiếu>”',
         '- Ghi chú: Người lập, “Cần lập phiếu kiểm kê”, Thời gian, Kho, Ghi chú (nội dung yêu cầu)',
         '- Bấm → mở màn chi tiết kế hoạch']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Lưu và duyệt thành công.”', '- Thiếu: “Bạn chưa nhập đầy đủ thông tin.”', '- Xung đột: ' + CONFLICT]),
   ],
   ev=[
       ('Bấm Lưu và duyệt', 'Click',
        'Before:\n– Không kiểm quyền riêng; màn Sửa: phiếu phải Đang tạo và người bấm là người tạo, nếu không → ' + CONFLICT + '.\n'
        '– Bắt đủ 6 trường.\n'
        'During:\n– Trường bắt buộc trống → ' + REQ + ' dưới ô; mọi ô thiếu đỏ cùng lúc.\n'
        + SAVE_DURING[len('During:\n'):] + '\n'
        'After:\n– Lưu kế hoạch trạng thái Đã duyệt (tạo mới: sinh số phiếu).\n'
        '– Ghi lịch sử: “Tạo mới” (màn Tạo) hoặc “Thay đổi thông tin” + “Thay đổi trạng thái” Đang tạo → Đã duyệt (màn Sửa).\n'
        '– Gửi thông báo cho nhân viên cùng công ty có quyền ' + Q1 + '.\n'
        '– Hiển thị “Lưu và duyệt thành công.”, về màn danh sách.'),
       ('Sửa ô đang báo lỗi', 'Change',
        'Before:\n– Ô đang viền đỏ.\nAfter:\n– Xóa viền đỏ và câu lỗi của ô đó; các ô khác giữ lỗi.'),
       ('Bấm thông báo (người lập phiếu kiểm kê)', 'Click',
        'Before:\n– Người nhận có quyền ' + Q1 + '.\nAfter:\n– Mở màn chi tiết kế hoạch; thấy nút ' + LAP + ' nếu Ngày kiểm kê '
        'từ chưa qua (mục 2.10).'),
       ('Gửi thông báo lỗi', 'System',
        'Before:\n– Kế hoạch đã lưu.\nAfter:\n– Chỉ ghi nhật ký lỗi; người dùng vẫn thấy “Lưu và duyệt thành công.”.'),
   ])

# ------------------------------------------------------------ 2.7 Sửa
fr(7, 'Chỉnh sửa kế hoạch', usecase=('FR-07', 'Chỉnh sửa kế hoạch', 'crud', A_NV),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Chỉnh sửa kế hoạch tổng kiểm kê hàng hóa',
       mota='Người tạo sửa kế hoạch còn Đang tạo: đổi ngày kiểm kê, kho, công ty thuê kho, thành phần tham gia, nội dung yêu cầu; '
            'lưu giữ Đang tạo (Lưu nháp) hoặc chuyển luôn Đã duyệt (Lưu và duyệt, mục 2.6). Số phiếu không sửa được.',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo kế hoạch.\n3. Kế hoạch đang ở trạng thái Đang tạo.',
       chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
             '2. Hệ thống mở màn “Sửa kế hoạch tổng kiểm kê hàng hóa: <số phiếu>”, điền sẵn Số phiếu (khóa), 2 ô ngày, kho (kể '
             'cả kho đã ngừng / khác công ty vẫn hiện đúng tên), công ty thuê kho, phòng ban (đã ngừng vẫn hiện), nội dung.\n'
             '3. Người dùng sửa thông tin (đổi kho → Công ty thuê kho tự chọn lại theo kho mới).\n'
             '4. Người dùng bấm Lưu nháp.\n'
             '5. Hệ thống kiểm lại phiếu còn Đang tạo và đúng người tạo, kiểm tra dữ liệu như mục 2.5.\n'
             '6. Hệ thống ghi đè thông tin, kho, công ty thuê kho, phòng ban; cập nhật người / ngày cập nhật; giữ nguyên số phiếu.\n'
             '7. Hệ thống ghi nhận hành động “Thay đổi thông tin” trong lịch sử (giá trị cũ → mới của Ngày kiểm kê từ, Ngày kiểm '
             'kê đến, Nội dung yêu cầu, Kho, Công ty thuê kho, Thành phần tham gia) — không đổi gì thì không ghi.\n'
             '8. Hệ thống hiển thị “Cập nhật thành công.” và chuyển về màn danh sách.',
       phu='• Mở màn Sửa của kế hoạch không còn Đang tạo / không phải người tạo → tự chuyển sang màn chi tiết.\n'
           '• Kế hoạch ngoài phạm vi / đã bị xóa → trang “Không tìm thấy trang”.\n'
           '• Lưu khi phiếu vừa bị duyệt / xóa ở tab khác → ' + CONFLICT + ' hoặc ' + NOTFOUND + '.\n'
           '• Thiếu dữ liệu → như mục 2.5 (Lưu nháp) / 2.6 (Lưu và duyệt).\n'
           '• Quay lại khi đã sửa → hộp “Thông tin chưa lưu”; không sửa gì → về danh sách ngay.\n'
           '• Hai người không thể cùng sửa: chỉ người tạo được sửa.',
       dacbiet='Kế hoạch không có trường duy nhất nên không có kiểm tra trùng với chính nó. Mở màn Sửa không tự đổi Công ty thuê '
               'kho đã lưu. Màn Sửa không có nút Lưu và tiếp tục.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('12_edit'), shot_caption='Màn Sửa kế hoạch tổng kiểm kê hàng hóa'),
   ui=FORM_UI[:12] + FORM_UI[13:],
   ev=[
       ('Mở màn Sửa', 'System',
        'Before:\n– Kiểm tra phạm vi xem, nếu ngoài phạm vi → trang “Không tìm thấy trang”.\n'
        '– Kiểm tra người tạo + Đang tạo, nếu không → chuyển sang màn chi tiết.\n'
        'After:\n– Điền sẵn dữ liệu; chưa tính là đã thay đổi.'),
       ('Đổi Kho', 'Change',
        'Before:\n– Danh sách kho khác lúc mở.\nAfter:\n– Công ty thuê kho chọn lại hết công ty của các kho mới.'),
       ('Bấm Lưu nháp', 'Click',
        'Before:\n– Kiểm lại phiếu còn Đang tạo và người bấm là người tạo, nếu không → ' + CONFLICT + '.\n' + SAVE_DURING + '\n'
        'After:\n– Ghi đè thông tin, kho, công ty thuê kho, phòng ban; cập nhật người / ngày cập nhật.\n'
        '– Ghi một dòng lịch sử “Thay đổi thông tin” (cũ → mới) nếu có thay đổi.\n'
        '– Hiển thị “Cập nhật thành công.”, về màn danh sách.'),
       ('Bấm Lưu và duyệt', 'Click', 'Before:\n– Như Lưu nháp, bắt đủ 6 trường.\nDuring:\n– Như mục 2.6.\nAfter:\n– Như mục 2.6.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu với lúc mở.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu, không ghi lịch sử; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.8 Xóa
fr(8, 'Xóa kế hoạch', usecase=('FR-08', 'Xóa kế hoạch', 'action', A_NV),
   rule=('- Hộp thoại xác nhận Xóa và Thông báo.', 'delete'),
   intro=dict(
       ten='Xóa kế hoạch tổng kiểm kê hàng hóa',
       mota='Người tạo xóa hẳn kế hoạch còn Đang tạo cùng toàn bộ dữ liệu con (kho, công ty thuê kho, phòng ban tham gia). Kế hoạch '
            'đã Đã duyệt không xóa được.',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo.\n3. Kế hoạch đang Đang tạo.',
       chinh='1. Người dùng bấm Xóa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa” với nội dung “Bạn có chắc muốn xóa bản ghi này không?”.\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm lại phiếu còn Đang tạo và đúng người tạo.\n'
             '5. Hệ thống ghi nhận hành động “Xóa” trong lịch sử, rồi xóa kế hoạch và mọi dữ liệu con.\n'
             '6. Hệ thống hiển thị “Xóa thành công.”; ở danh sách nạp lại, ở màn chi tiết quay về danh sách.',
       phu='• Bấm Hủy / (x) → đóng hộp, không xóa.\n'
           '• Phiếu vừa được duyệt / không còn là người tạo → ' + CONFLICT + ', không xóa.\n'
           '• Phiếu đã bị xóa ở tab khác → ' + NOTFOUND + '.\n'
           '• Kế hoạch Đang tạo chưa lập được phiếu kiểm kê nào (chỉ kế hoạch Đã duyệt mới lập được) nên không có ràng buộc dữ '
           'liệu đang sử dụng.',
       dacbiet='Nút Xóa khóa trong lúc đang xóa. Xóa là xóa hẳn, không khôi phục.'),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp Xác nhận xóa kế hoạch',
               note='Hộp xác nhận được mở ngay trên màn hình danh sách hoặc màn chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Xóa trên dòng', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện', ['- Thùng rác đỏ', '- Chỉ phiếu Đang tạo của mình']),
       ('Nút Xóa ở màn chi tiết', 'Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện', '- Nút đỏ ở chân màn chi tiết.'),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Hiển thị', '- “Xác nhận xóa”.'),
       ('Nội dung hộp', 'Label', 'Hiển thị', 'Hiển thị', '- “Bạn có chắc muốn xóa bản ghi này không?”'),
       ('Nút Xóa (xác nhận)', 'Button', 'Enable', 'Hiển thị', '- Nút đỏ; bấm → xóa kế hoạch.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không xóa.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống Hủy.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Xóa thành công.”', '- Thất bại: ' + CONFLICT + ', ' + NOTFOUND + ' hoặc “Xóa thất bại.”']),
   ],
   ev=[
       ('Bấm Xóa', 'Click', 'Before:\n– Nút chỉ hiện với phiếu Đang tạo của mình.\nAfter:\n– Hiện hộp Xác nhận xóa.'),
       ('Bấm Xóa (xác nhận)', 'Click',
        'Before:\n– Kiểm tra phạm vi xem, ngoài phạm vi → ' + NOTFOUND + '.\n'
        '– Kiểm lại phiếu còn Đang tạo và người bấm là người tạo, nếu không → ' + CONFLICT + '.\n'
        'During:\n– Xóa trọn gói kế hoạch và dữ liệu con; lỗi thì không xóa gì.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Xóa”.\n– Hiển thị “Xóa thành công.”; nạp lại danh sách / về danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nAfter:\n– Đóng hộp, dữ liệu giữ nguyên.'),
   ])

# ------------------------------------------------------------ 2.9 Chi tiết
fr(9, 'Xem chi tiết kế hoạch',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết kế hoạch tổng kiểm kê hàng hóa',
       mota='Màn chỉ đọc hiển thị Thông tin chung (Số phiếu, Ngày kiểm kê từ / đến, Kho, Công ty thuê kho, Thành phần tham gia, '
            'Nội dung yêu cầu) và khối Lịch sử. Chân màn có nút theo cờ: Sửa / Xóa (Đang tạo, người tạo), ' + LAP + ' (Đã duyệt, '
            'có Q1, còn hạn), In, Quay lại.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Kế hoạch trong phạm vi xem (hoặc là kế hoạch Đã duyệt và người dùng có '
                'quyền Q1).',
       chinh='1. Người dùng bấm Số phiếu ở danh sách (hoặc bấm thông báo, hoặc liên kết kế hoạch ở phiếu kiểm kê).\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết kế hoạch tổng kiểm kê hàng hóa: <số phiếu>”.\n'
             '4. Hệ thống hiển thị Thông tin chung (ô khóa, không dấu *) và khối Lịch sử (thu gọn).',
       phu='• Ngoài phạm vi / không tồn tại → trang “Không tìm thấy trang”.\n'
           '• Kế hoạch Đang tạo của người khác → coi như ngoài phạm vi.\n'
           '• Bấm Quay lại → về danh sách, khôi phục bộ lọc (trong 10 phút).',
       dacbiet='Tiêu đề không kèm nhãn trạng thái. Công ty thuê kho hiển thị mã công ty, Thành phần tham gia hiển thị tên phòng ban, '
               'nối bằng dấu phẩy.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết kế hoạch tổng kiểm kê hàng hóa'),
   extra=[(shot('15_lapphieu_detail'), 'Màn chi tiết kế hoạch Đã duyệt còn hạn — có nút ' + LAP)],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Chi tiết kế hoạch tổng kiểm kê hàng hóa: <số phiếu>”', '- Không kèm nhãn trạng thái']),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Số phiếu', 'Textbox', 'Disable', '<mã công ty>.KHTKK-NNNNN', 'Theo dữ liệu', '- Ô khóa.'),
       ('Ngày kiểm kê từ', 'Datepicker', 'Disable', 'dd/mm/yyyy', 'Theo dữ liệu', '- Ô khóa.'),
       ('Ngày kiểm kê đến', 'Datepicker', 'Disable', 'dd/mm/yyyy', 'Theo dữ liệu', '- Ô khóa.'),
       ('Kho', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- Tên các kho nối dấu phẩy.'),
       ('Công ty thuê kho', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- Mã các công ty nối dấu phẩy.'),
       ('Thành phần tham gia', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- Tên các phòng ban nối dấu phẩy.'),
       ('Nội dung yêu cầu', 'Textarea', 'Disable', '–', 'Theo dữ liệu', '- Ô khóa; trống thì để trống.'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
        ['- Nút Xem lịch sử / Thu gọn, Làm mới, Bộ lọc', '- Nội dung như mục 2.13']),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Phiếu Đang tạo của mình → mở màn Sửa.'),
       ('Nút ' + LAP, 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
        '- Đã duyệt + có Q1 + Ngày kiểm kê từ ≥ hôm nay (mục 2.10).'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Cửa sổ Xem trước (mục 2.11).'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Phiếu Đang tạo của mình (mục 2.8).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn danh sách.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → trang “Không tìm thấy trang”.\n'
        'During:\n– Lấy dữ liệu kế hoạch, cờ nút.\nAfter:\n– Hiển thị màn chỉ đọc, nút theo cờ.'),
       ('Bấm Xem lịch sử', 'Click', 'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở rộng khối, hiện các mốc.'),
       ('Bấm Sửa / Xóa / ' + LAP + ' / In', 'Click',
        'Before:\n– Nút hiện theo cờ của phiếu.\nAfter:\n– Thực hiện như mục 2.7 / 2.8 / 2.10 / 2.11.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Không có dữ liệu cần lưu.\nAfter:\n– Về danh sách, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.10 Lập phiếu kiểm kê
fr(10, 'Lập phiếu kiểm kê hàng hóa từ kế hoạch', usecase=('FR-10', 'Lập phiếu kiểm kê', 'action', A_TK),
   rule=('- Màn Danh sách và Phân quyền.', 'list'),
   intro=dict(
       ten='Lập phiếu kiểm kê theo hàng hóa từ kế hoạch Đã duyệt',
       mota='Người có quyền Lập phiếu kiểm kê kho theo hàng hóa bấm nút ở kế hoạch Đã duyệt còn hạn để mở màn Tạo phiếu kiểm kê '
            'theo hàng hóa (phân hệ Kho) đã nạp sẵn kế hoạch: kho, công ty thuê kho, nội dung yêu cầu; người lập tự thêm hàng. '
            'Kế hoạch giữ nguyên Đã duyệt và lập được nhiều phiếu kiểm kê, nhưng mỗi hàng chỉ được kiểm ở 1 phiếu của kế hoạch.',
       tacnhan='Người dùng có quyền thực hiện chức năng: ' + Q1 + '; Super admin.',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Kế hoạch đang Đã duyệt.\n3. Người dùng có quyền ' + Q1 +
                ' (hoặc Super admin).\n4. Ngày kiểm kê từ của kế hoạch là hôm nay hoặc sau hôm nay.',
       chinh='1. Người dùng bấm ' + LAP + ' ở cột Hành động hoặc chân màn chi tiết.\n'
             '2. Hệ thống mở màn Tạo phiếu kiểm kê theo hàng hóa (cùng tab) với kế hoạch đã chọn sẵn, nạp Kho, Công ty thuê kho '
             '(chọn hết theo kho), Ghi chú = Nội dung yêu cầu; danh sách hàng trống, cho thêm hàng.\n'
             '3. Người dùng thêm hàng và lưu phiếu kiểm kê ở màn đó; hệ thống kiểm lại kế hoạch còn Đã duyệt và chặn hàng đã có '
             'trong phiếu kiểm kê khác của cùng kế hoạch (“Hàng hóa đã lập phiếu kiểm kê.”).\n'
             '4. Kế hoạch KHÔNG đổi trạng thái, không ghi lịch sử; phiếu kiểm kê có cột / liên kết Kế hoạch kiểm kê mở lại kế hoạch.',
       phu='• Kế hoạch không còn Đã duyệt khi lưu phiếu kiểm kê → màn kia báo ' + CONFLICT + '.\n'
           '• Ngày kiểm kê từ đã qua (kể cả đang trong đợt kiểm) → nút không hiện, kế hoạch không có trong popup Chọn kế hoạch '
           'của màn Kiểm kê theo hàng hóa.\n'
           '• Thiếu quyền → nút không hiện.',
       dacbiet='Điều kiện ngày giữ nguyên như hệ thống cũ (người dùng chốt 20/10/2026).'),
   layout=dict(menu=MENU + ' => ' + LAP, shot=shot('15_lapphieu_detail'),
               shot_caption='Nút ' + LAP + ' ở màn chi tiết kế hoạch Đã duyệt'),
   extra=[(shot('15b_lapphieu_target'), 'Màn Tạo phiếu kiểm kê theo hàng hóa mở ra đã nạp sẵn kế hoạch tổng')],
   ui_kw=dict(required=False),
   ui=[
       ('Nút Lập phiếu trên dòng', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
        ['- Biểu tượng tài liệu có dấu cộng', '- Rê chuột: “' + LAP + '”']),
       ('Nút Lập phiếu ở chi tiết', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
        '- Rê chuột: “Lập phiếu kiểm kê hàng hóa từ kế hoạch này”.'),
       ('Nhãn trạng thái kế hoạch', 'Badge', 'Read-only', 'Danh sách 2 giá trị', 'Theo dữ liệu',
        ['- Giữ Đã duyệt sau khi lập phiếu kiểm kê', '- Không có trạng thái sau Đã duyệt']),
       ('Ô Kế hoạch kiểm kê ở phiếu kiểm kê', 'Link', 'Read-only', '<mã công ty>.KHTKK-NNNNN', 'Theo kế hoạch',
        '- Bấm → mở màn chi tiết kế hoạch tổng.'),
   ],
   ev=[
       ('Bấm ' + LAP, 'Click',
        'Before:\n– Nút chỉ hiện khi Đã duyệt + có quyền ' + Q1 + ' + Ngày kiểm kê từ ≥ hôm nay.\n'
        'After:\n– Mở màn Tạo phiếu kiểm kê theo hàng hóa, nạp sẵn kế hoạch.'),
       ('Màn Kiểm kê theo hàng hóa nạp kế hoạch', 'System',
        'Before:\n– Kiểm lại điều kiện như nút; không đạt → không nạp được kế hoạch.\n'
        'After:\n– Nạp kho, công ty thuê kho, ghi chú; hàng để trống.'),
       ('Màn Kiểm kê theo hàng hóa lưu phiếu', 'System',
        'Before:\n– Kế hoạch còn Đã duyệt; hàng chưa có trong phiếu khác của kế hoạch.\n'
        'After:\n– Lưu phiếu kiểm kê gắn kế hoạch; kế hoạch không đổi.'),
   ])

# ------------------------------------------------------------ 2.11 In
fr(11, 'In phiếu và in danh sách', usecase=('FR-11', 'In phiếu / In danh sách', 'io', A_NV),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In kế hoạch / In danh sách kế hoạch',
       mota='Xem trước và in một kế hoạch (mẫu in “KẾ HOẠCH TỔNG KIỂM KÊ HÀNG HÓA”: số phiếu, ngày lập, thời gian kiểm kê, kho '
            'vật lý, công ty thuê kho, thành phần tham gia, nội dung yêu cầu, chỗ ký Người lập) hoặc in danh sách theo bộ lọc đang '
            'áp. Bản in mở trong cửa sổ trên màn đang đứng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm In ở cột Hành động / màn chi tiết (in phiếu), hoặc In danh sách trên bảng.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ xem trước, hiện “Đang tải dữ liệu in…” trong lúc dựng.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Danh sách quá 2.000 dòng → không dựng bản in, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc.\n'
           '• Không có dòng nào → “Không có dữ liệu để in”.\n'
           '• Ngoài phạm vi → ' + NOTFOUND + '.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in kế hoạch tổng kiểm kê hàng hóa.” / “Thiếu mẫu in danh sách kế hoạch tổng kiểm kê '
           'hàng hóa.”.\n'
           '• Bấm (x) → đóng cửa sổ.',
       dacbiet='Logo / tên công ty đầu bản in phiếu lấy theo công ty ghi trên kế hoạch; bản in danh sách theo công ty người in. '
               'Ngày ở khối ký là ngày in; Người lập của bản in phiếu là người tạo kế hoạch, của bản in danh sách là người in.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước kế hoạch',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   extra=[(shot('19_printlist'), 'Cửa sổ Xem trước danh sách kế hoạch')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–',
        ['- In phiếu: “Xem trước kế hoạch tổng kiểm kê hàng hóa <số phiếu>”',
         '- In danh sách: “Xem trước danh sách kế hoạch tổng kiểm kê hàng hóa”']),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', ['- Cạnh tiêu đề; bấm → hộp thoại in', '- Ẩn khi vượt 2.000 dòng']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Đang tải dữ liệu in…”.'),
       ('Đầu bản in phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Logo, tên công ty, địa chỉ, điện thoại, email, website của công ty ghi trên kế hoạch',
         '- “KẾ HOẠCH TỔNG KIỂM KÊ HÀNG HÓA”, “Số phiếu: …”, “Ngày lập: dd/mm/yyyy” (ngày tạo)']),
       ('Nội dung bản in phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- “Thời gian kiểm kê (*): Từ ngày … đến ngày …”', '- “Kho vật lý (*)”: tên các kho; “Công ty thuê kho”: mã công ty',
         '- “Thành phần tham gia (*)”: tên phòng ban; “Nội dung yêu cầu (*)”']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- “Ngày … Tháng … Năm …”, Người lập (tên người tạo kế hoạch), sát lề phải.'),
       ('Bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        ['- Cột: STT, Số phiếu, Thời gian kiểm kê, Kho, Nội dung yêu cầu, Người tạo, Ngày tạo, Trạng thái',
         '- Ngày tạo kèm giờ; khối ký bên phải: Ngày … Tháng … Năm …, Người lập (người in)']),
       ('Dòng nhắc vượt trần in', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        '- “Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc …”.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', ['- “Không tải được dữ liệu in”', '- “Không có dữ liệu để in”']),
   ],
   ev=[
       ('Bấm In (phiếu)', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → ' + NOTFOUND + '.\n'
        'During:\n– Dựng bản in theo mẫu; lỗi → “Không tải được dữ liệu in”.\nAfter:\n– Hiện bản xem trước khổ dọc.'),
       ('Bấm In danh sách', 'Click',
        'Before:\n– Lấy bộ lọc đang áp.\nDuring:\n– Quá 2.000 dòng → dòng nhắc, ẩn bản in và nút In.\n'
        'After:\n– Hiện bản xem trước danh sách.'),
       ('Bấm In trong cửa sổ', 'Click', 'Before:\n– Bản in đã dựng.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, giữ nguyên màn đang đứng.'),
   ])

# ------------------------------------------------------------ 2.12 Xuất Excel
fr(12, 'Xuất Excel danh sách', usecase=('FR-12', 'Xuất Excel', 'io', A_NV),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách kế hoạch ra Excel',
       mota='Chọn trường và thứ tự rồi xuất toàn bộ kế hoạch khớp bộ lọc + phạm vi xem (không phân trang) ra file Excel. Màn '
            'không có xuất Excel 1 kế hoạch (hệ thống cũ không có).',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel trên bảng.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 9 trường (tích sẵn theo cột đang hiện).\n'
             '3. Người dùng tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy mọi kế hoạch theo bộ lọc + phạm vi xem, dựng file có letterhead công ty, tiêu đề, dòng thời gian '
             '(khi lọc Ngày tạo), cột STT + trường đã chọn theo đúng thứ tự, khối ký.\n'
             '5. Hệ thống tải file “danh_sach_ke_hoach_tong_kiem_ke_hang_hoa.xlsx”, báo “Xuất Excel thành công.”.',
       phu='• Không có kế hoạch khớp → vẫn ra file có tiêu đề, dòng tên cột và khối ký.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi → “Lỗi khi xuất Excel.”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng; nút Xuất Excel khóa trong lúc đang xuất. Mọi cột là chữ (ngày giữ dạng dd/mm/yyyy); dòng '
               'tên cột in đậm, có viền, không tô nền.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 9 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- Số phiếu, Thời gian kiểm kê, Kho, Nội dung yêu cầu, Trạng thái', '- Người tạo, Ngày tạo, Ngày cập nhật, Người cập nhật']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/9 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Bấm → tải file', '- Khóa khi chưa tích / đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('File danh sách', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Letterhead công ty, tiêu đề “DANH SÁCH KẾ HOẠCH TỔNG KIỂM KÊ HÀNG HÓA”',
         '- Dòng “Từ ngày … đến ngày …” khi lọc Ngày tạo',
         '- Cột STT + trường đã chọn; khối ký cuối file; trang tính “Kế hoạch tổng kiểm kê”']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công.”', '- Thất bại: “Lỗi khi xuất Excel.”']),
   ],
   ev=[
       ('Bấm Xuất Excel (bảng)', 'Click', 'Before:\n– Không có lượt xuất đang chạy.\nAfter:\n– Mở cửa sổ chọn trường.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Kéo bằng biểu tượng.\nAfter:\n– Đổi thứ tự cột trong file.'),
       ('Tích / bỏ tích trường, Chọn tất cả, Bỏ chọn hết', 'Change',
        'Before:\n– Không giới hạn số trường.\nAfter:\n– Cập nhật dòng “Đang chọn n/9 trường”; 0 trường → khóa Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất.\n'
        'During:\n– Lấy toàn bộ kế hoạch theo bộ lọc + phạm vi xem.\n– Lỗi → “Lỗi khi xuất Excel.”.\n' + ERR + '\n'
        'After:\n– Tải file danh sách, báo “Xuất Excel thành công.”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.13 Lịch sử
fr(13, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của kế hoạch',
       mota='Xem các mốc thao tác của kế hoạch: Tạo mới, Thay đổi thông tin (giá trị cũ → mới), Thay đổi trạng thái (Đang tạo → '
            'Đã duyệt), Xóa. Cửa sổ ở danh sách và khối Lịch sử ở màn chi tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động (hoặc trong menu Hành động khác), hoặc Xem lịch sử ở màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ “Lịch sử thay đổi: <số phiếu>” và hiển thị các mốc, mới nhất ở trên.',
       phu='• Kế hoạch từ hệ thống cũ chưa có mốc → “Chưa có lịch sử thao tác nào.”.\n'
           '• Bấm Bộ lọc → các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Ngoài phạm vi → ' + NOTFOUND + '.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Lịch sử ghi Ngày kiểm kê từ, Ngày kiểm kê đến, Nội dung yêu cầu, Kho (tên), Công ty thuê kho (mã), Thành phần tham '
               'gia (tên). Xem, in, xuất Excel, lập phiếu kiểm kê không ghi mốc.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('17c_detail_history'), 'Khối Lịch sử ở màn chi tiết kế hoạch')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <số phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái: “Trạng thái: Đang tạo → Đã duyệt”',
           '- Thay đổi thông tin: từng trường cũ → mới', '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách hành động', 'Trống', ['- Mặc định: trống', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Người đã thao tác', 'Trống', '- Chọn là lọc ngay.'),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc từ ngày này.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc đến hết ngày này.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- “Chưa có lịch sử thao tác nào.”', '- “Không có lịch sử phù hợp bộ lọc.”']),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Giống nút Đóng.'),
   ],
   ev=[
       ('Mở lịch sử', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → ' + NOTFOUND + '.\n'
        'During:\n– Nạp các mốc; chưa có → “Chưa có lịch sử thao tác nào.”.\nAfter:\n– Hiển thị, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change', 'Before:\n– Không có nút Tìm kiếm.\nAfter:\n– Lọc lại danh sách mốc.'),
       ('Bấm Làm mới (khối Lịch sử ở chi tiết)', 'Click', 'Before:\n– Khối đang mở.\nAfter:\n– Nạp lại các mốc mới nhất.'),
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng; danh sách giữ nguyên trang, bộ lọc.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Kế hoạch tổng kiểm kê hàng hóa; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Kế hoạch không ghi tồn', [
        '– Lưu / duyệt / sửa / xóa kế hoạch không đổi tồn kho, không sinh phiếu nhập / xuất.',
        '– Kế hoạch tổng không có danh sách hàng; hàng do phiếu kiểm kê lập từ kế hoạch tự thêm.'],
     ['Tạo', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-02', 'Phạm vi xem', [
        '– V1 (hoặc Super admin): mọi kế hoạch; V2: công ty mình + của mình (công ty trống → chỉ của mình); không quyền: của mình.',
        '– Kế hoạch Đang tạo chỉ người tạo thấy.',
        '– Người có quyền Lập phiếu kiểm kê kho theo hàng hóa xem được chi tiết mọi kế hoạch Đã duyệt.',
        '– Ngoài phạm vi: chi tiết / in / lịch sử đều bị từ chối.'], ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất', 'Lịch sử']),
    ('BR-03', 'Dữ liệu bắt buộc khi lưu', [
        '– Lưu nháp / Lưu và tiếp tục: chỉ bắt Ngày kiểm kê từ, Ngày kiểm kê đến.',
        '– Lưu và duyệt: bắt đủ 2 ngày, ≥ 1 kho, ≥ 1 công ty thuê kho, ≥ 1 phòng ban tham gia, Nội dung yêu cầu.',
        '– Luôn kiểm: Ngày kiểm kê đến ≥ Ngày kiểm kê từ; Nội dung yêu cầu ≤ 255 ký tự; kho / công ty / phòng ban không trùng, '
        'còn tồn tại; công ty thuê kho phải có kho kế toán trong các kho đã chọn.'], ['Tạo', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-04', 'Điều kiện sửa / xóa', [
        '– Chỉ người tạo, chỉ khi Đang tạo; máy chủ kiểm lại lúc lưu / xóa, sai → báo trạng thái đã thay đổi.',
        '– Xóa là xóa hẳn kế hoạch và dữ liệu con; kế hoạch Đã duyệt không xóa được nên không có ràng buộc phiếu kiểm kê.'],
     ['Chỉnh sửa', 'Xóa']),
    ('BR-05', 'Vòng đời trạng thái', [
        '– Lưu nháp / Lưu và tiếp tục → Đang tạo; Lưu và duyệt → Đã duyệt (không hỏi xác nhận, không có người duyệt riêng).',
        '– Không có luồng trả về Đang tạo; lập phiếu kiểm kê không đổi trạng thái kế hoạch.',
        '– Không có Không duyệt / Hủy / Khóa trên màn này.'], ['Lưu và duyệt', 'Lập phiếu kiểm kê']),
    ('BR-06', 'Tính duy nhất', [
        '– Không có trường nhập duy nhất; mã <mã công ty>.KHTKK-NNNNN tự sinh (công ty người tạo + số thứ tự), không đổi khi sửa.',
        '– Hai kế hoạch cùng kho, cùng thời gian vẫn được lưu.',
        '– Nút lưu khóa trong lúc lưu chống tạo trùng.'], ['Tạo']),
    ('BR-07', 'Chuẩn hóa dữ liệu nhập', [
        '– Công ty / phòng ban của kế hoạch = của người tạo.',
        '– Nội dung yêu cầu bỏ khoảng trắng đầu / cuối khi lưu.',
        '– Kho chỉ gồm kho đang hoạt động có kho kế toán thuộc công ty người đăng nhập; phòng ban chỉ gồm phòng ban đang hoạt động.',
        '– Đổi kho → Công ty thuê kho tự chọn lại hết công ty của các kho mới; mỗi công ty hiện 1 lần.'], ['Tạo', 'Chỉnh sửa']),
    ('BR-08', 'Liên kết cấp cha – con', [
        '– Kế hoạch > kho > công ty thuê kho (thuộc kho đã chọn); kế hoạch > phòng ban tham gia.',
        '– Kế hoạch > các phiếu kiểm kê theo hàng hóa; mỗi hàng chỉ kiểm ở 1 phiếu của cùng kế hoạch.'],
     ['Tạo', 'Chỉnh sửa', 'Lập phiếu kiểm kê']),
    ('BR-09', 'Điều kiện lập phiếu kiểm kê', [
        '– Kế hoạch Đã duyệt + người dùng có quyền Lập phiếu kiểm kê kho theo hàng hóa (hoặc Super admin) + Ngày kiểm kê từ ≥ '
        'hôm nay (giữ như hệ thống cũ).',
        '– Cùng điều kiện ngày áp cho popup Chọn kế hoạch ở màn Kiểm kê theo hàng hóa.'], ['Lập phiếu kiểm kê']),
    ('BR-10', 'Thông báo', [
        '– Lưu với trạng thái Đã duyệt (tạo hoặc sửa) → gửi “[KHTKK] Đã duyệt: <số phiếu>” cho nhân viên có quyền Lập phiếu kiểm '
        'kê kho theo hàng hóa cùng công ty người lưu; người lưu không có công ty → không gửi; lỗi gửi không làm hỏng việc lưu.'],
     ['Lưu và duyệt']),
    ('BR-11', 'In và xuất', [
        '– Letterhead bản in phiếu theo công ty ghi trên kế hoạch; bản in / file danh sách theo công ty người in / xuất.',
        '– In danh sách tối đa 2.000 dòng; Xuất Excel danh sách không giới hạn, rỗng vẫn ra file; không có xuất 1 kế hoạch.'],
     ['In', 'Xuất Excel']),
    ('BR-12', 'Sử dụng ở màn khác', [
        '– Kho vật lý đã có trong kế hoạch không xóa được ở danh mục Kho vật lý.',
        '– Màn Kiểm kê theo hàng hóa nạp kế hoạch Đã duyệt còn hạn; báo cáo Hàng thừa thiếu sau tổng kiểm kê lọc theo kế hoạch.'],
     ['Tạo', 'Lưu và duyệt', 'Lập phiếu kiểm kê']),
    ('BR-13', 'Quy tắc ghi lịch sử', [
        '– Ghi: Tạo mới; Thay đổi thông tin (Ngày kiểm kê từ / đến, Nội dung yêu cầu, Kho, Công ty thuê kho, Thành phần tham gia '
        '— cũ → mới, không đổi thì không ghi); Thay đổi trạng thái (Đang tạo → Đã duyệt); Xóa.',
        '– Xem / in / xuất / lập phiếu kiểm kê không ghi; hiển thị mới nhất ở trên.'], ['Tạo', 'Chỉnh sửa', 'Xóa', 'Lịch sử']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Kế hoạch tổng kiểm kê hàng hóa (trạng thái, thời gian kiểm kê, kho, công '
    'ty thuê kho, nội dung yêu cầu).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Kiểm kê theo hàng hóa (popup Chọn kế hoạch hiện kế hoạch tổng Đã duyệt còn hạn; nạp sẵn kho, công ty thuê kho, '
                 'ghi chú; chặn hàng đã có ở phiếu khác cùng kế hoạch; cột Kế hoạch kiểm kê là liên kết mở kế hoạch)',
     'Kho -> Kiểm kho -> Theo vị trí'),
    ('2', 'Tài chính', 'Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả (cùng màn Kiểm kê theo hàng hóa, lối vào lọc phiếu chờ duyệt '
                       'kết quả; số kế hoạch trên phiếu là liên kết mở kế hoạch)', 'Tài chính -> Kiểm kê'),
    ('3', 'Kho', 'Báo cáo hàng thừa thiếu sau tổng kiểm kê hàng hóa (ô lọc Kế hoạch tổng kiểm kê chọn qua popup mọi kế hoạch tổng; '
                 'dòng tóm tắt ghi số kế hoạch)', 'Kho -> Báo cáo kho'),
    ('4', 'Kho', 'Kho vật lý (không xóa được kho đã có trong kế hoạch)', 'Kho -> Danh mục'),
    ('5', 'Hệ thống ERP', 'Phiếu kiểm kê theo hàng hóa trên hệ thống cũ (lập phiếu từ kế hoạch tổng Đã duyệt)',
     'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
