# -*- coding: utf-8 -*-
"""SRS màn "Kế hoạch kiểm kê theo vị trí" (mã phiếu <mã công ty>-KHKKVT-NNNNN) — form chuẩn Danh mục quốc gia, chuẩn 04/11/2026.

Chạy: python gen_srs.py  → SRS - Kế hoạch kiểm kê theo vị trí.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc
  ../borrow-export/gen_srs.py (05/11, Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn).
Nguồn đọc 05/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Entities/PositionInventory/PositionInventory.php, Services/PositionInventory{,Write,Print,Tree}Service.php,
      Http/Controllers/V1/PositionInventoryController.php, Http/Requests/PositionInventory/PositionInventoryStoreRequest.php,
      Exports/PositionInventoryExport.php, Services/WarehouseInventoryLockService.php, Services/PositionInventoryResultWriteService.php
      (đổi trạng thái kế hoạch), Services/PositionTransferWriteService.php (Hoàn thành + chặn vị trí)}, app/Services/CatalogHistoryService.php,
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (2 quyền xem theo cấp + quyền Lập phiếu kiểm kê kho theo vị trí)
  FE  pages/finance/position-inventories/** (index, create, _id/index, _id/edit, components/{PositionInventoryForm, ScopePicker,
      DetailTable, row-actions.js, export-excel.js}), components/subsystem-menu/finance.js (nhóm Kiểm kê),
      pages/warehouse/position-inventory-results/components/PlanPickerModal.vue
Ảnh: ./khkkvt_shots — dev-hrm 05/11/2026 (_capture/capture.js, chặn mọi yêu cầu ghi). Bật cờ tạm trên trình duyệt (sửa phản hồi
  GET, không gửi máy chủ): 12_edit, 13_delete, 03_rowmenu, 15_send_detail (dev không có kế hoạch Đang tạo / Đang kiểm của DNS Admin).
  10b_validate: gọi kiểm tra của form trên trình duyệt (không bấm Lưu). 10c_filled: "Lấy vị trí" là yêu cầu chỉ đọc (cho qua).
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

TEN = 'Kế hoạch kiểm kê theo vị trí'
SHOTS = os.path.join(HERE, 'khkkvt_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Kiểm kê => Kế hoạch kiểm kê theo vị trí'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Kế hoạch kiểm kê theo vị trí.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NOTFOUND = '“Không tìm thấy kế hoạch kiểm kê hoặc bạn không có quyền xem.”'

A_NV = 'Người lập kế hoạch'
A_TK = 'Thủ kho'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng đã được cấp tài khoản (màn không gắn quyền thao tác); phạm vi '
      'xem theo quyền Xem kế hoạch kiểm kê theo vị trí theo tổng công ty / theo công ty.')
TN_OWNER = 'Người dùng có quyền thực hiện chức năng: người lập kế hoạch (người tạo phiếu), phiếu đang ở trạng thái Đang tạo.'
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Kế hoạch kiểm kê theo vị trí.\n'
      '3. Dữ liệu hiển thị trong phạm vi xem theo quyền (mục Phần 2).')

d = SrsDoc(out=OUT, menu=MENU, route='/finance/position-inventories', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Kiểm kê': 'menu_nhom', 'Kế hoạch kiểm kê theo vị trí': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Lấy vị trí': 'btn_layvitri', 'Lưu và gửi': 'btn_luugui', 'Sửa': 'btn_sua_row',
    'Xóa': 'btn_xoa_row', 'Xem chi tiết': 'link_sophieu', 'Lập phiếu kiểm kê': 'btn_lapphieu_row', 'In': 'btn_in_row',
    'In danh sách': 'btn_in_list', 'Xuất Excel': 'btn_xuatexcel', 'Lịch sử': 'btn_lichsu_row',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Kế hoạch kiểm kê theo vị trí (mã phiếu <mã công ty>-KHKKVT-NNNNN, ví dụ '
    'TPE-KHKKVT-00145), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ cách người lập kế hoạch chọn kho vật lý, chọn phạm vi Nhà – Dãy – Khoang – Vị trí, lấy ảnh chụp hàng tồn từng lô '
    'tại các vị trí đó và chỉ định Hội đồng kiểm kê, rồi gửi kế hoạch cho thủ kho lập phiếu kiểm kê.',
    'Làm rõ vòng đời trạng thái của kế hoạch (Đang tạo → Đang kiểm → Đã lập kiểm kê → Hoàn thành) và các màn khác đọc / đổi '
    'trạng thái của kế hoạch.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo kế hoạch (Lưu / Lưu và tiếp tục), '
    'Chọn phạm vi kiểm kê và Lấy vị trí, Lưu và gửi kế hoạch cho thủ kho, Chỉnh sửa, Xóa, Xem chi tiết, Lập phiếu kiểm kê từ '
    'kế hoạch (mở màn Kiểm kê theo vị trí), In phiếu / In danh sách, Xuất Excel (danh sách và 1 phiếu), Xem lịch sử thay đổi. '
    'Màn KHÔNG có Duyệt / Không duyệt, Hủy, Khóa / Mở khóa và Import Excel; trạng thái Đã lập kiểm kê và Hoàn thành do màn '
    'Kiểm kê theo vị trí và Phiếu điều chuyển vị trí (phân hệ Kho) đổi.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Kế hoạch là căn cứ để thủ kho lập phiếu kiểm kê theo vị trí: phiếu kiểm kê nạp sẵn phạm vi, danh sách hàng – lô – số tồn '
    'và hội đồng kiểm kê của kế hoạch.',
    'Số tồn trên kế hoạch là ẢNH CHỤP tại thời điểm bấm Lấy vị trí, không cập nhật theo tồn kho sau đó.',
    'Kế hoạch Đang kiểm khóa các vị trí của nó: màn Phiếu điều chuyển vị trí không cho chọn / chặn điều chuyển vị trí đang kiểm kho.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Kế hoạch không ghi tồn kho, không sinh phiếu nhập / xuất (BR-01).',
    'Phạm vi xem theo quyền tổng công ty / công ty; không quyền chỉ thấy phiếu mình tạo; phiếu Đang tạo chỉ người tạo thấy (BR-02).',
    'Chỉ người tạo được Sửa / Xóa và chỉ khi phiếu còn Đang tạo (BR-04).',
    'Lưu và Lưu và gửi cùng một bộ điều kiện bắt buộc: kho vật lý, ít nhất 1 vị trí, có bảng Chi tiết, ít nhất 1 thành viên '
    'hội đồng có chức vụ (BR-03).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Kế hoạch kiểm kê theo vị trí (kế hoạch)', 'Chứng từ <mã công ty>-KHKKVT-NNNNN của màn này: phạm vi vị trí cần kiểm, ảnh '
                                               'chụp hàng tồn và hội đồng kiểm kê của một kho vật lý.'),
    ('Phiếu kiểm kê theo vị trí', 'Phiếu thủ kho lập từ kế hoạch ở màn Kiểm kê theo vị trí (phân hệ Kho) để nhập kết quả thực kiểm.'),
    ('Kho vật lý', 'Kho thật chứa hàng; mỗi kế hoạch thuộc đúng 1 kho vật lý.'),
    ('Nhà / Dãy / Khoang / Vị trí', 'Cấu trúc 4 cấp của kho: Nhà > Dãy > Khoang > Vị trí. Vị trí tự do là vị trí không thuộc '
                                    'khoang nào, luôn hiện ở cột Vị trí.'),
    ('Phạm vi kiểm kê', 'Các Nhà / Dãy / Khoang / Vị trí được tick; chỉ vị trí đã tick mới được lấy hàng tồn.'),
    ('Lấy vị trí', 'Thao tác lấy danh sách hàng tồn (số lượng > 0) theo từng lô tại các vị trí đã tick, gom theo công ty — '
                   'đây là ảnh chụp số tồn lưu trên kế hoạch.'),
    ('SL tồn / SL / Cộng', 'Trường đặc thù của bảng Chi tiết: SL tồn = tồn của hàng tại vị trí; SL = tồn của từng lô; Cộng = '
                           'tổng tồn của hàng theo từng công ty.'),
    ('Hội đồng kiểm kê', 'Danh sách nhân viên tham gia kiểm kê, mỗi người kèm 1 chức vụ.'),
    ('Thủ kho', 'Nhân viên được khai là thủ kho của kho vật lý; nhận thông báo khi kế hoạch được gửi và lập phiếu kiểm kê.'),
    ('Trạng thái Đang tạo', 'Nhãn xám: kế hoạch mới lưu (nút Lưu); chỉ người tạo thấy, sửa, xóa.'),
    ('Trạng thái Đang kiểm', 'Nhãn vàng: kế hoạch đã gửi thủ kho (nút Lưu và gửi); các vị trí của kế hoạch đang bị khóa kiểm kho.'),
    ('Trạng thái Đã lập kiểm kê', 'Nhãn xanh dương: thủ kho đã lập phiếu kiểm kê từ kế hoạch.'),
    ('Trạng thái Hoàn thành', 'Nhãn xanh lá: phiếu kiểm kê đã được duyệt kết quả không còn chênh lệch thiếu, hoặc đã điều chuyển '
                              'xử lý hết chênh lệch.'),
    ('Trạng thái Đã hủy', 'Chỉ hiển thị cho dữ liệu cũ của hệ thống trước; màn không tạo ra, không có trong ô lọc.'),
    ('Cấu trúc phân cấp', 'Kế hoạch > vị trí > hàng hóa (SL tồn) > công ty (Cộng) > lô (SL); kèm phạm vi đã tick và hội đồng.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn không gắn quyền cho thao tác Tạo / Sửa / Xóa / In / Xuất / Lịch sử: mọi người dùng đăng nhập đều lập được kế hoạch. '
    'Hai quyền riêng của màn chỉ quyết định PHẠM VI dữ liệu được xem; quyền Lập phiếu kiểm kê kho theo vị trí (của màn Kiểm kê '
    'theo vị trí, phân hệ Kho) quyết định nút Lập phiếu kiểm kê và người nhận thông báo. Super admin được coi như có đủ quyền.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Lập phiếu kiểm kê kho theo vị trí',
     'Thủ kho của kho đầu tiên của kế hoạch có quyền này thấy nút Lập phiếu kiểm kê ở kế hoạch Đang kiểm, nhận thông báo khi kế '
     'hoạch cùng công ty được gửi, xem được chi tiết kế hoạch Đang kiểm dù ngoài phạm vi xem (để bấm thông báo).'),
    ('—', 'Không cần quyền', 'Tạo mới, Lưu, Lưu và gửi, Lưu và tiếp tục; Sửa / Xóa khi là người tạo và phiếu Đang tạo; In, Xuất '
                              'Excel, Lịch sử với phiếu trong phạm vi xem.'),
], widths=[0.8, 1.8, 3.4])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem kế hoạch kiểm kê theo vị trí theo tổng công ty',
     'Mọi kế hoạch của mọi công ty; hiện thêm ô lọc Công ty – Phòng ban (Super admin như V1).'),
    ('V2', 'Xem kế hoạch kiểm kê theo vị trí theo công ty',
     'Kế hoạch của công ty người xem + kế hoạch mình tạo; công ty người xem trống → chỉ kế hoạch mình tạo.'),
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
    ('FR-06 Chọn phạm vi và Lấy vị trí', '✅', '✅', '✅', '✅'),
    ('FR-07 Lưu và gửi kế hoạch', '✅', '✅', '✅', '✅'),
    ('FR-08 Chỉnh sửa', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo'),
    ('FR-09 Xóa', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo'),
    ('FR-10 Xem chi tiết', '✅ + kế hoạch Đang kiểm của kho mình', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-11 Lập phiếu kiểm kê', '✅ thủ kho, Đang kiểm', '❌', '❌', '❌'),
    ('FR-12 In phiếu / In danh sách', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-13 Xuất Excel', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-14 Xem lịch sử thay đổi', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('Duyệt / Không duyệt / Hủy / Khóa – Mở khóa / Import', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.9, 1.1, 1.0, 1.1, 0.9])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có V1 / V2: vẫn vào màn, chỉ thấy kế hoạch mình tạo; không có ô lọc Công ty – Phòng ban.',
    'Mở chi tiết / sửa / in / xuất / lịch sử của kế hoạch ngoài phạm vi (qua đường link): hệ thống báo ' + NOTFOUND +
    '; màn chi tiết / sửa chuyển sang trang “Không tìm thấy trang”.',
    'Sửa / Xóa kế hoạch không phải mình tạo hoặc không còn Đang tạo: nút không hiện; nếu vẫn gửi yêu cầu (mở 2 tab) → báo ' +
    CONFLICT + '. Mở màn Sửa của phiếu đó → tự chuyển về màn chi tiết.',
    'Không phải thủ kho của kho / thiếu Q1: nút Lập phiếu kiểm kê không hiện.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới, Xuất Excel, In danh sách, Cấu hình cột', 'Luôn hiện', 'Không gắn quyền'),
    ('Nút Sửa, Xóa (dòng và màn chi tiết)', 'Người xem là người tạo và phiếu Đang tạo', 'Máy chủ kiểm lại khi lưu / xóa'),
    ('Nút Lập phiếu kiểm kê', 'Phiếu Đang kiểm, người xem là thủ kho kho đầu tiên của phiếu (hoặc Super admin), có Q1',
     'Mở màn Thêm phiếu kiểm kê theo vị trí'),
    ('Nút In, Xuất Excel, Lịch sử trên dòng', 'Mọi dòng', 'Tối đa 3 nút hiện thẳng, còn lại vào menu “Hành động khác”'),
    ('Ô lọc Công ty – Phòng ban', 'Có V1 hoặc V2 (V2: công ty bị khóa theo công ty mình)', 'Fail-closed: không quyền thì ẩn'),
], widths=[2.2, 2.3, 1.5])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_NV, [0, 1, 2, 3, 4, 6, 7]), (A_TK, [0, 5])],
    [('FR-01', 'Xem danh sách kế hoạch', 'view'),
     ('FR-05', 'Tạo kế hoạch', 'crud'),
     ('FR-07', 'Lưu và gửi kế hoạch', 'action'),
     ('FR-08', 'Chỉnh sửa kế hoạch', 'crud'),
     ('FR-09', 'Xóa kế hoạch', 'action'),
     ('FR-11', 'Lập phiếu kiểm kê', 'action'),
     ('FR-12', 'In phiếu / In danh sách', 'io'),
     ('FR-13', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-10', 'Xem chi tiết', 'view', 'extend', [0], None),
     ('FR-14', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn phạm vi và Lấy vị trí', 'crud', 'extend', [1, 3], None)],
    'Sơ đồ Use Case tổng quan màn Kế hoạch kiểm kê theo vị trí')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách kế hoạch',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách kế hoạch kiểm kê theo vị trí',
       mota='Hiển thị bảng các kế hoạch kiểm kê theo vị trí trong phạm vi xem của người dùng (theo quyền tổng công ty / công ty / '
            'của mình), kèm trạng thái, kho, người tạo, ngày tạo / cập nhật, phân trang và tổng số. Mỗi dòng có liên kết sang '
            'màn chi tiết và các nút thao tác theo trạng thái phiếu.',
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
       dacbiet='Cột mặc định hiện: cả 10 cột (STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái, Người tạo, Ngày tạo, Ngày cập nhật, '
               'Người cập nhật, Hành động); không có cột ẩn mặc định. Cột khóa (không ẩn, không đổi vị trí): STT, Số phiếu, '
               'Hành động; Số phiếu ghim trái khi cuộn ngang. Sắp xếp được: Số phiếu, Ngày kiểm kê, Người tạo; mặc định (chưa '
               'chọn cột) ngày tạo mới nhất ở trên. Đổi sắp xếp / bộ lọc / số dòng đều về trang 1.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Kế hoạch kiểm kê theo vị trí'),
   extra=[(shot('03_rowmenu'), 'Nút thao tác theo trạng thái: dòng Đang tạo (Sửa, Xóa, Hành động khác) và dòng Đang kiểm')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Danh sách kế hoạch kiểm kê theo vị trí” trên thanh tiêu đề, tiêu đề bảng và tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “Tạo kế hoạch kiểm kê theo vị trí”', '- Bấm → mở màn Tạo kế hoạch (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.13)',
         '- Khóa trong lúc đang xuất file']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “In danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.12)']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Đánh số liên tục theo trang', '- Cột khóa trong Tùy chỉnh cột']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', '<mã công ty>-KHKKVT-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết (mục 2.10)', '- Sắp xếp được', '- Cột khóa, ghim trái khi cuộn ngang']),
       ('Cột Ngày kiểm kê', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Ngày giờ lập kế hoạch (trùng Ngày tạo)', '- Sắp xếp được']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Tên kho vật lý của kế hoạch; không sắp xếp.'),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 4 giá trị', 'Hiển thị',
        ['- Đang tạo: nhãn xám', '- Đang kiểm: nhãn vàng', '- Đã lập kiểm kê: nhãn xanh dương', '- Hoàn thành: nhãn xanh lá',
         '- Không sắp xếp']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Họ tên người lập kế hoạch', '- Sắp xếp được']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Thời điểm lưu lần đầu; không sắp xếp.'),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        '- Thời điểm cập nhật gần nhất (kể cả khi màn khác đổi trạng thái kế hoạch).'),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Họ tên người cập nhật gần nhất.'),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Sửa (bút chì): chỉ phiếu Đang tạo của chính mình → mở màn Sửa (mục 2.8)',
           '- Xóa (thùng rác đỏ): cùng điều kiện → hộp Xác nhận xóa (mục 2.9)',
           '- Lập phiếu kiểm kê: phiếu Đang kiểm, người xem là thủ kho có quyền (mục 2.11)',
           '- In, Xuất Excel, Lịch sử: mọi dòng (mục 2.12, 2.13, 2.14)',
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
        'After:\n– Mở màn chi tiết (mục 2.10); bộ lọc được ghi nhớ 10 phút để khôi phục khi quay lại.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Số phiếu, Ngày kiểm kê, Người tạo hỗ trợ sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại một lần theo số dòng mới.'),
       ('Bấm Hành động khác (ba chấm)', 'Click',
        'Before:\n– Dòng có nhiều hơn 3 nút thao tác.\nAfter:\n– Mở menu các nút còn lại (In / Xuất Excel / Lịch sử).'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc kế hoạch',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách kế hoạch',
       mota='Thu hẹp danh sách theo số phiếu, trạng thái, người tạo, hàng hóa, ngày kiểm kê, kho – nhà – dãy – khoang – vị trí và '
            'công ty – phòng ban. Ô tìm nhanh tìm theo số phiếu; các ô lọc nằm trong khối Tìm kiếm nâng cao, bật / tắt được bằng '
            'Cài đặt bộ lọc (mục 2.3). Kho → Nhà → Dãy → Khoang → Vị trí là chuỗi ô chọn phụ thuộc.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập số phiếu vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Hệ thống lọc ngay khi một ô chọn đổi giá trị, về trang 1; ô chữ Hàng hóa áp khi bấm Tìm kiếm.\n'
             '4. Chọn Kho → hệ thống nạp Nhà / Dãy / Khoang / Vị trí của kho đó; đổi cấp cha thì xóa giá trị các cấp con.\n'
             '5. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Chưa chọn Kho → các ô Nhà / Dãy / Khoang / Vị trí không có lựa chọn.\n'
           '• Không có quyền V1 / V2 → không có ô Công ty – Phòng ban; có V2 → ô Công ty khóa ở công ty mình.\n'
           '• Ô lọc bị tắt trong Cài đặt bộ lọc → không hiện trên khối lọc.',
       dacbiet='Ô tìm nhanh / Hàng hóa khớp một phần, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối; không giới hạn số '
               'ký tự; ký tự % và _ được hiểu là ký tự đại diện. Hàng hóa khớp theo mã HOẶC tên hàng trên kế hoạch. Kho / Nhà / '
               'Dãy / Khoang / Vị trí lọc kế hoạch có tick đúng mục đó trong phạm vi kiểm kê. Ngày kiểm kê lấy trọn hai ngày '
               'biên. Mọi điều kiện kết hợp kiểu VÀ. Ghi nhớ bộ lọc trên trình duyệt 10 phút khi đi vào màn con của màn này.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số phiếu”', '- Khớp một phần số phiếu', '- Áp khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh và ô chữ, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Bấm → xóa mọi tiêu chí kể cả ô tìm nhanh', '- Nạp lại từ trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (mọi trạng thái)', '- Lựa chọn: Đang tạo / Đang kiểm / Đã lập kiểm kê / Hoàn thành']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Toàn bộ nhân viên (kể cả người chưa tạo kế hoạch nào)']),
       ('Hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Mã hoặc tên hàng”', '- Kế hoạch có ít nhất 1 hàng có mã hoặc tên chứa chuỗi nhập']),
       ('Ngày kiểm kê', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai ngày biên; được bỏ trống một đầu']),
       ('Kho', 'Dropdown', 'Enable', 'Danh sách kho vật lý', 'Không', 'Trống',
        ['- Mặc định: trống', '- Hiển thị “Mã - Tên”', '- Đổi kho → xóa Nhà, Dãy, Khoang, Vị trí']),
       ('Nhà', 'Dropdown', 'Enable', 'Nhà của kho đã chọn', 'Không', 'Trống',
        ['- Rỗng khi chưa chọn Kho', '- Đổi Nhà → xóa Dãy, Khoang, Vị trí']),
       ('Dãy', 'Dropdown', 'Enable', 'Dãy của Nhà đã chọn', 'Không', 'Trống',
        ['- Chưa chọn Nhà → mọi dãy của kho', '- Đổi Dãy → xóa Khoang, Vị trí']),
       ('Khoang', 'Dropdown', 'Enable', 'Khoang của Dãy đã chọn', 'Không', 'Trống', '- Đổi Khoang → xóa Vị trí.'),
       ('Vị trí', 'Dropdown', 'Enable', 'Vị trí của Khoang đã chọn', 'Không', 'Trống',
        '- Chưa chọn cấp cha → mọi vị trí của kho, gồm vị trí tự do.'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Ẩn khi thiếu quyền',
        ['- Chỉ hiện khi có V1 hoặc V2', '- V2: khóa ở công ty mình (biểu tượng ổ khóa)']),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Phòng ban của công ty', 'Không', 'Ẩn khi thiếu quyền',
        '- Lọc kế hoạch theo phòng ban của người lập.'),
   ],
   ev=[
       ('Đổi giá trị một ô chọn', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\n'
        'During:\n– Đổi cấp cha (Kho / Nhà / Dãy / Khoang) → xóa giá trị cấp con; đổi Kho → nạp cấu trúc kho mới.\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí (một lần).'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh và ô Hàng hóa, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm kế hoạch có số phiếu chứa chuỗi nhập (và hàng khớp ô Hàng hóa).\n'
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
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 10 mục lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 10 mục theo thứ tự thiết kế; phải bấm Lưu mới có hiệu lực.\n'
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
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách 10 mục', '–', 'Theo cấu hình đã lưu',
        ['- Trạng thái, Người tạo, Hàng hóa, Ngày kiểm kê, Kho', '- Nhà, Dãy, Khoang, Vị trí, Công ty – Phòng ban']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → mục đó không hiện ở khối Tìm kiếm nâng cao.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích lại đủ 10 mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình đang lưu (chưa lưu lần nào → đủ 10 mục).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\n'
        'During:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ 10 mục, thứ tự thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 10 cột của bảng danh sách. Ba cột STT, Số phiếu, Hành động bị khóa; '
            'cấu hình lưu riêng theo người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 10 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 10 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ nguyên sau khi tải lại trang, đăng '
               'nhập lại, đổi trình duyệt; người dùng khác không bị ảnh hưởng.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 10 cột', '–', 'Theo cấu hình đã lưu',
        ['- STT, Số phiếu, Ngày kiểm kê, Kho, Trạng thái', '- Người tạo, Ngày tạo, Ngày cập nhật, Người cập nhật, Hành động']),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Số phiếu, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/10 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
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
       ('Tích / bỏ tích một cột', 'Change', 'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/10 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5 Tạo kế hoạch
FORM_UI = [
    ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     ['- Tạo: “Tạo kế hoạch kiểm kê theo vị trí”', '- Sửa: “Sửa kế hoạch kiểm kê theo vị trí: <số phiếu>”']),
    ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại',
     '- Góc phải khối Thông tin chung: “<Họ tên> - dd/mm/yyyy hh:mm” (màn Sửa: người tạo và giờ tạo).'),
    ('Số phiếu', 'Textbox', 'Disable', '<mã công ty>-KHKKVT-NNNNN', '–', 'Ẩn ở màn Tạo',
     '- Chỉ hiện ở màn Sửa / Chi tiết; mã tự sinh khi lưu lần đầu, không sửa được.'),
    ('Ngày kiểm kê', 'Datepicker', 'Disable', 'dd/mm/yyyy', 'Có', 'Ngày hiện tại',
     ['- Không sửa được', '- Màn Tạo: hôm nay; màn Sửa: ngày tạo kế hoạch']),
    ('Kho vật lý', 'Dropdown', 'Enable', 'Danh sách kho vật lý', 'Có', 'Trống',
     ['- Gợi ý “Chọn kho vật lý”; hiển thị “Mã - Tên”', '- Chọn → nạp Nhà / Dãy / Khoang / Vị trí của kho vào khối Phạm vi',
      '- Đổi kho khi bảng Chi tiết đã có dữ liệu → hộp “Đổi kho vật lý” (mục 2.6)',
      '- Lỗi: “Kho vật lý – Vui lòng chọn kho vật lý.”']),
    ('Khối Phạm vi kiểm kê', 'Table/Grid', 'Enable', '4 cột tick', 'Có (Vị trí)', 'Trống',
     ['- 4 cột Nhà / Dãy / Khoang / Vị trí; đặc tả ở mục 2.6',
      '- Lỗi: “Phạm vi kiểm kê – Chưa chọn đủ thông tin vị trí!” (khung Vị trí viền đỏ)']),
    ('Nút Lấy vị trí', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Góc phải tiêu đề khối Phạm vi kiểm kê', '- Rê chuột: “Lấy danh sách hàng tồn tại các vị trí đã tick”',
      '- Bấm → đổ hàng tồn vào bảng Chi tiết (mục 2.6); khóa trong lúc đang lấy']),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Có', '“Không có dữ liệu”',
     ['- Tiêu đề 2 tầng: STT, Nhà kho, Vị trí, Tên hàng, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn',
      '- Nhóm “Chi tiết tồn theo công ty”: Công ty, Lô, SL, Cộng',
      '- Gộp ô theo vị trí → hàng → công ty; mỗi lô 1 dòng; tiêu đề dính khi cuộn, khung cao tối đa 600px',
      '- Lỗi: “Chi tiết – Chưa có vị trí nào. Vui lòng bấm \"Lấy vị trí\".” (viền đỏ)']),
    ('Khối Hội đồng kiểm kê', 'Table/Grid', 'Enable', '≥ 1 dòng', 'Có', '1 dòng trống (màn Tạo)',
     ['- Cột STT, Nhân viên *, Chức vụ *, Hành động', '- Không có dòng: “Không có dữ liệu”',
      '- Lỗi: “Hội đồng kiểm kê – Vui lòng thêm ít nhất 1 thành viên.”']),
    ('Nút Thêm dòng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề khối Hội đồng; bấm → thêm 1 dòng trống.'),
    ('Ô Nhân viên', 'Dropdown', 'Enable', 'Nhân viên đang làm việc', 'Có', 'Trống',
     ['- Gợi ý “Chọn nhân viên”; hiển thị “Họ tên - Mã phòng ban - Mã NV”', '- Chọn → tự điền Chức vụ đầu tiên của nhân viên',
      '- Lỗi: “Nhân viên – Vui lòng chọn nhân viên.” / “Nhân viên – Bị trùng.”']),
    ('Ô Chức vụ', 'Dropdown', 'Enable', 'Chức vụ của nhân viên', 'Có', 'Chức vụ đầu tiên',
     ['- Gợi ý “Chọn chức vụ”', '- Lỗi: “Chức vụ – Vui lòng chọn chức vụ.”']),
    ('Nút Xóa dòng hội đồng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Thùng rác đỏ; bấm → xóa dòng ngay, không hỏi.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Rê chuột: “Lưu kế hoạch ở trạng thái Đang tạo”', '- Lưu xong về danh sách; khóa trong lúc lưu']),
    ('Nút Lưu và gửi', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Rê chuột: “Lưu và gửi kế hoạch cho thủ kho (trạng thái Đang kiểm)”', '- Đặc tả ở mục 2.7']),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị ở màn Tạo',
     ['- Rê chuột: “Lưu (Đang tạo) rồi ở lại tạo kế hoạch tiếp theo”', '- Không có ở màn Sửa']),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi “Thông tin chưa lưu”.'),
    ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Nội dung: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút Thoát: rời màn, không lưu',
      '- Nút Ở lại / (x): đóng hộp, giữ dữ liệu']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Thành công: “Lưu thành công.” / “Lưu và gửi thành công.”', '- Thiếu: “Bạn chưa nhập đầy đủ thông tin.”',
      '- Phiếu đã đổi trạng thái: ' + CONFLICT, '- Lỗi khác: câu lỗi của máy chủ hoặc “Lưu thất bại.”']),
]

SAVE_DURING = ('During:\n– Kho vật lý trống → “Kho vật lý – Vui lòng chọn kho vật lý.”\n'
               '– Chưa tick vị trí → “Phạm vi kiểm kê – Chưa chọn đủ thông tin vị trí!”\n'
               '– Bảng Chi tiết trống → “Chi tiết – Chưa có vị trí nào. Vui lòng bấm \"Lấy vị trí\".”\n'
               '– Hội đồng không có dòng → “Hội đồng kiểm kê – Vui lòng thêm ít nhất 1 thành viên.”; dòng thiếu nhân viên → '
               '“Nhân viên – Vui lòng chọn nhân viên.”; trùng → “Nhân viên – Bị trùng.”; thiếu chức vụ → “Chức vụ – Vui lòng '
               'chọn chức vụ.”\n'
               '– Mọi lỗi hiện cùng lúc dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin.”, cuộn tới ô lỗi đầu tiên.\n'
               '– Máy chủ kiểm lại: vị trí không thuộc kho → “Vị trí – Không thuộc kho đã chọn.”; hàng / lô không còn → '
               '“Hàng hóa – Có hàng hóa không tồn tại. Vui lòng bấm \"Lấy vị trí\" lại.” / “Lô – Có lô nhập không tồn tại. '
               'Vui lòng bấm \"Lấy vị trí\" lại.”\n' + ERR)

fr(5, 'Tạo kế hoạch kiểm kê (Lưu / Lưu và tiếp tục)', usecase=('FR-05', 'Tạo kế hoạch', 'crud', A_NV),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo kế hoạch kiểm kê theo vị trí',
       mota='Người lập chọn kho vật lý, tick phạm vi Nhà / Dãy / Khoang / Vị trí, bấm Lấy vị trí để chụp hàng tồn từng lô, khai '
            'Hội đồng kiểm kê rồi bấm Lưu: kế hoạch được lưu ở trạng thái Đang tạo (chỉ người tạo thấy), chưa báo cho ai. '
            'Kế hoạch không ghi tồn kho.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có ít nhất 1 kho vật lý có cấu trúc vị trí.\n'
                '3. Không cần quyền riêng để tạo.',
       chinh='1. Người dùng bấm Tạo mới ở danh sách.\n'
             '2. Hệ thống mở màn “Tạo kế hoạch kiểm kê theo vị trí”: Ngày kiểm kê = hôm nay, khối Hội đồng có sẵn 1 dòng trống, '
             'góc phải ghi “<người tạo> - <ngày giờ hiện tại>”.\n'
             '3. Người dùng chọn Kho vật lý; hệ thống nạp cấu trúc kho (ẩn nhà / dãy / khoang / vị trí đã khóa).\n'
             '4. Người dùng tick phạm vi và bấm Lấy vị trí (mục 2.6); hệ thống đổ bảng Chi tiết.\n'
             '5. Người dùng chọn Nhân viên (Chức vụ tự điền), Thêm dòng nếu cần.\n'
             '6. Người dùng bấm Lưu.\n'
             '7. Hệ thống kiểm tra dữ liệu, lưu kế hoạch trạng thái Đang tạo với công ty / phòng ban / bộ phận của người tạo, sinh '
             'mã <mã công ty>-KHKKVT-NNNNN, lưu phạm vi, bảng Chi tiết (kèm 1 dòng kết quả sẵn cho mỗi lô theo đơn vị cơ sở) '
             'và hội đồng.\n'
             '8. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu.\n'
             '9. Hệ thống hiển thị “Lưu thành công.” và chuyển về màn danh sách.',
       phu='• Bấm Lưu và tiếp tục → lưu như trên (Đang tạo), ở lại màn Tạo với form trắng.\n'
           '• Thiếu dữ liệu bắt buộc → báo đủ lỗi dưới từng ô cùng lúc, thông báo “Bạn chưa nhập đầy đủ thông tin.”, không lưu.\n'
           '• Bấm Quay lại / chuyển menu / đóng tab khi đã nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì thì về '
           'danh sách ngay.\n'
           '• Màn là trang riêng, không có (x) / click ra ngoài.\n'
           '• Lỗi máy chủ → thông báo câu lỗi hoặc “Lưu thất bại.”, dữ liệu đã nhập giữ nguyên.',
       dacbiet='Các nút lưu khóa trong lúc đang lưu để một lần bấm không tạo 2 kế hoạch. Kế hoạch không có trường nhập duy nhất: '
               'mã tự sinh theo công ty người tạo + số thứ tự, không sửa được; 2 kế hoạch cùng kho cùng phạm vi vẫn lưu được. '
               'Lưu và Lưu và gửi dùng chung một bộ điều kiện bắt buộc. Số tồn trên kế hoạch là ảnh chụp lúc Lấy vị trí.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'),
               shot_caption='Màn Tạo kế hoạch sau khi chọn kho, tick phạm vi và Lấy vị trí'),
   extra=[(shot('10_create'), 'Màn Tạo kế hoạch lúc mới mở'),
          (shot('10b_validate_full'), 'Lỗi bắt buộc hiện cùng lúc khi bấm lưu thiếu dữ liệu'),
          (shot('10g_unsaved'), 'Hộp “Thông tin chưa lưu” khi rời màn')],
   ui=FORM_UI,
   ev=[
       ('Mở màn Tạo', 'System',
        'Before:\n– Không cần quyền riêng.\nDuring:\n– Nạp danh sách kho vật lý, nhân viên đang làm việc kèm chức vụ, ngày hôm nay.\n'
        '– Lỗi → “Không tải được dữ liệu.”.\nAfter:\n– Hiển thị form trống, Hội đồng có 1 dòng trống; chưa tính là đã thay đổi.'),
       ('Chọn Kho vật lý', 'Change',
        'Before:\n– Bảng Chi tiết trống (nếu đã có → hỏi “Đổi kho vật lý”, mục 2.6).\n'
        'After:\n– Xóa phạm vi và bảng Chi tiết, nạp Nhà / Dãy / Khoang / Vị trí của kho mới.'),
       ('Chọn Nhân viên', 'Change',
        'Before:\n– Nhân viên đang làm việc.\nAfter:\n– Tự điền Chức vụ đầu tiên của nhân viên; bỏ chọn → xóa Chức vụ.'),
       ('Bấm Thêm dòng / Xóa dòng hội đồng', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Thêm 1 dòng trống / bỏ dòng đó.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Không kiểm quyền riêng; khóa các nút lưu.\n' + SAVE_DURING + '\n'
        'After:\n– Lưu kế hoạch trạng thái Đang tạo, sinh số phiếu, lưu phạm vi, chi tiết, hội đồng.\n'
        '– Ghi một dòng lịch sử “Tạo mới”.\n– Hiển thị “Lưu thành công.”, về màn danh sách.'),
       ('Bấm Lưu và tiếp tục', 'Click',
        'Before:\n– Như Lưu.\nDuring:\n– Kiểm tra như Lưu.\n' + ERR + '\n'
        'After:\n– Lưu như Lưu (Đang tạo), ghi lịch sử “Tạo mới”, hiển thị “Lưu thành công.”, làm trắng form và ở lại màn Tạo.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu hiện tại với lúc mở màn.\nDuring:\n– Có thay đổi → hiện hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu; Ở lại: giữ nguyên form.'),
   ])

# ------------------------------------------------------------ 2.6 Phạm vi + Lấy vị trí
fr(6, 'Chọn phạm vi kiểm kê và Lấy vị trí', usecase=('FR-06', 'Chọn phạm vi và Lấy vị trí', 'crud', A_NV),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Chọn phạm vi kiểm kê và lấy hàng tồn tại các vị trí',
       mota='Trong khối Phạm vi kiểm kê của màn Tạo / Sửa, người lập tick Nhà → Dãy → Khoang → Vị trí của kho đã chọn rồi bấm '
            'Lấy vị trí: hệ thống lấy mọi hàng còn tồn (số lượng > 0) theo từng lô tại các vị trí đã tick, gom theo công ty và '
            'đổ vào bảng Chi tiết. Đây là ảnh chụp số tồn lưu lên kế hoạch.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo hoặc Sửa kế hoạch.\n3. Đã chọn Kho vật lý.',
       chinh='1. Người dùng tick Nhà ở cột Nhà; cột Dãy hiện các dãy của nhà đã tick, nhóm theo nhà.\n'
             '2. Người dùng tick Dãy → cột Khoang hiện khoang của dãy đã tick; tick Khoang → cột Vị trí hiện vị trí của khoang, '
             'kèm nhóm “Vị trí tự do” luôn hiện.\n'
             '3. Người dùng tick Vị trí (có thể dùng ô tìm và “Chọn hết” của cột / của nhóm).\n'
             '4. Người dùng bấm Lấy vị trí.\n'
             '5. Hệ thống lấy hàng tồn > 0 và lô tồn > 0 tại các vị trí đã tick thuộc kho đã chọn, gom theo công ty.\n'
             '6. Hệ thống thay toàn bộ bảng Chi tiết bằng kết quả mới.',
       phu='• Chưa chọn Kho vật lý mà bấm Lấy vị trí → lỗi đỏ dưới ô Kho, thông báo “Bạn chưa nhập đầy đủ thông tin.”.\n'
           '• Chưa tick vị trí nào → thông báo “Chưa chọn đủ thông tin vị trí!”, lỗi đỏ dưới khối Phạm vi.\n'
           '• Các vị trí đã tick không có hàng tồn → thông báo “Các vị trí đã chọn không có hàng tồn.”, bảng giữ nguyên.\n'
           '• Bỏ tick cấp cha → hệ thống tự bỏ tick các cấp con không còn cha (vị trí tự do không bị ảnh hưởng).\n'
           '• Đổi Kho vật lý khi bảng Chi tiết đã có dữ liệu → hộp “Đổi kho vật lý”: Đổi kho = xóa phạm vi + bảng Chi tiết, nạp '
           'kho mới; Hủy = trả ô về kho cũ.\n'
           '• Nhà / dãy / khoang / vị trí đã khóa ở danh mục kho không hiện để tick (trừ mục kế hoạch đang tick sẵn ở màn Sửa).\n'
           '• Lỗi máy chủ → câu lỗi của máy chủ hoặc “Đã có lỗi xảy ra.”.',
       dacbiet='Ô tìm của mỗi cột khớp một phần theo “mã - tên”, không phân biệt hoa / thường, có dấu × xóa nhanh. “Chọn hết” chỉ '
               'tick các mục đang hiện (sau khi tìm). Nút Lấy vị trí khóa trong lúc đang lấy. Đổi phạm vi sau khi Lấy vị trí '
               'KHÔNG tự xóa bảng Chi tiết — cần bấm Lấy vị trí lại để bảng khớp phạm vi.'),
   layout=dict(menu=MENU + ' => Tạo mới => Lấy vị trí', shot=shot('10d_scope'),
               shot_caption='Khối Phạm vi kiểm kê đã tick Nhà – Dãy – Khoang – Vị trí'),
   extra=[(shot('10e_doikho'), 'Hộp xác nhận “Đổi kho vật lý” khi bảng Chi tiết đã có dữ liệu')],
   ui=[
       ('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Phạm vi kiểm kê”, nút Lấy vị trí ở góc phải.'),
       ('Cột Nhà', 'Checkbox', 'Enable', 'Nhà của kho', 'Không', 'Chưa tick',
        ['- Nhãn có dấu * nhưng không bắt buộc riêng', '- Danh sách “Mã - Tên” các nhà của kho']),
       ('Cột Dãy', 'Checkbox', 'Enable', 'Dãy của nhà đã tick', 'Không', 'Chưa tick',
        ['- Nhóm theo nhà, tiêu đề nhóm “Mã - Tên nhà” kèm “Chọn hết” riêng',
         '- Chưa tick nhà: “Chưa chọn nhà hoặc không có dữ liệu”']),
       ('Cột Khoang', 'Checkbox', 'Enable', 'Khoang của dãy đã tick', 'Không', 'Chưa tick',
        ['- Nhóm theo dãy, tiêu đề “Mã nhà | Mã dãy” kèm “Chọn hết”', '- Chưa tick dãy: “Chưa chọn dãy hoặc không có dữ liệu”']),
       ('Cột Vị trí', 'Checkbox', 'Enable', 'Vị trí tự do + vị trí của khoang đã tick', 'Có', 'Chưa tick',
        ['- Nhóm “Vị trí tự do” luôn hiện', '- Nhóm theo khoang, tiêu đề “Mã nhà | Mã dãy | Mã khoang”',
         '- Ít nhất 1 vị trí; khung viền đỏ khi thiếu']),
       ('Ô tìm của từng cột', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo mã hoặc tên nhà / dãy / khoang / vị trí”', '- Có dấu × xóa nhanh khi có chữ']),
       ('Ô Chọn hết của cột', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Chưa tick',
        ['- Tick / bỏ tick mọi mục đang hiện của cột', '- Khóa khi cột không có mục nào']),
       ('Ô Chọn hết của nhóm', 'Checkbox', 'Enable', '–', 'Không', 'Chưa tick', '- Tick / bỏ tick các mục đang hiện của nhóm đó.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chưa chọn kho: “Chưa chọn kho vật lý” ở cả 4 cột.'),
       ('Nút Lấy vị trí', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → lấy hàng tồn tại vị trí đã tick, thay bảng Chi tiết', '- Khóa và hiện vòng xoay trong lúc lấy']),
       ('Hộp “Đổi kho vật lý”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Nội dung: “Đổi kho vật lý sẽ xóa phạm vi kiểm kê và danh sách vị trí đã lấy. Bạn có muốn tiếp tục?”',
         '- Nút Đổi kho: xóa phạm vi + bảng Chi tiết, nạp kho mới', '- Nút Hủy / (x): giữ kho cũ']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Chưa chọn đủ thông tin vị trí!”', '- “Các vị trí đã chọn không có hàng tồn.”',
         '- “Bạn chưa nhập đầy đủ thông tin.” (chưa chọn kho)', '- “Không tải được cấu trúc kho.”']),
   ],
   ev=[
       ('Tick / bỏ tick một mục', 'Change',
        'Before:\n– Đã chọn Kho vật lý.\nDuring:\n– Bỏ tick cấp cha → tự bỏ tick cấp con không còn cha.\n'
        'After:\n– Cập nhật các cột con; có vị trí được tick → xóa lỗi đỏ của khối.'),
       ('Gõ ô tìm của cột', 'Change', 'Before:\n– Cột có dữ liệu.\nAfter:\n– Chỉ hiện mục có “mã - tên” chứa chuỗi gõ.'),
       ('Bấm Chọn hết (cột / nhóm)', 'Click', 'Before:\n– Chỉ tính các mục đang hiện.\nAfter:\n– Tick / bỏ tick các mục đó.'),
       ('Bấm Lấy vị trí', 'Click',
        'Before:\n– Kho vật lý đã chọn, nếu không → lỗi dưới ô Kho, “Bạn chưa nhập đầy đủ thông tin.”.\n'
        '– Có vị trí được tick, nếu không → “Chưa chọn đủ thông tin vị trí!”.\n'
        'During:\n– Lấy vị trí đã tick thuộc kho, có tồn > 0; lấy hàng và lô tồn > 0, gom theo công ty.\n'
        '– Không có hàng → “Các vị trí đã chọn không có hàng tồn.”.\n' + ERR + '\n'
        'After:\n– Thay toàn bộ bảng Chi tiết; xóa lỗi đỏ của bảng.'),
       ('Đổi Kho vật lý khi đã có Chi tiết', 'Change',
        'Before:\n– Bảng Chi tiết có dữ liệu.\nDuring:\n– Hiện hộp “Đổi kho vật lý”.\n'
        'After:\n– Đổi kho: xóa phạm vi và Chi tiết, nạp kho mới; Hủy: trả ô về kho cũ.'),
   ])

# ------------------------------------------------------------ 2.7 Lưu và gửi
fr(7, 'Lưu và gửi kế hoạch cho thủ kho', usecase=('FR-07', 'Lưu và gửi kế hoạch', 'action', A_NV),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lưu và gửi kế hoạch (chuyển trạng thái Đang kiểm)',
       mota='Ở màn Tạo hoặc Sửa, nút Lưu và gửi lưu kế hoạch và chuyển thẳng sang trạng thái Đang kiểm: kế hoạch hiện với người '
            'có quyền xem, thủ kho của kho nhận thông báo để lập phiếu kiểm kê, các vị trí của kế hoạch bị khóa kiểm kho. Không có '
            'hộp xác nhận (giữ như hệ thống cũ).',
       tacnhan=TN + ' Sửa rồi gửi: chỉ người tạo khi phiếu Đang tạo.',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo, hoặc màn Sửa của kế hoạch Đang tạo do mình tạo.\n'
                '3. Đủ dữ liệu bắt buộc như mục 2.5.',
       chinh='1. Người dùng nhập đủ thông tin (như mục 2.5) và bấm Lưu và gửi.\n'
             '2. Hệ thống kiểm tra dữ liệu như nút Lưu.\n'
             '3. Hệ thống lưu kế hoạch với trạng thái Đang kiểm (màn Tạo: sinh số phiếu; màn Sửa: kiểm lại phiếu còn Đang tạo và '
             'đúng người tạo).\n'
             '4. Hệ thống ghi nhận hành động trong lịch sử của phiếu: màn Tạo “Tạo mới”; màn Sửa “Thay đổi thông tin” (nếu đổi '
             'dữ liệu) và “Thay đổi trạng thái” Đang tạo → Đang kiểm.\n'
             '5. Hệ thống gửi thông báo “[KHKKVT] Tạo mới: <số phiếu>. Người lập: <tên>. Chờ lập phiếu kiểm kê. Kho: <kho>” cho '
             'thủ kho của kho, cùng công ty người gửi, có quyền Lập phiếu kiểm kê kho theo vị trí; bấm thông báo mở chi tiết kế hoạch.\n'
             '6. Hệ thống hiển thị “Lưu và gửi thành công.” và chuyển về màn danh sách.',
       phu='• Thiếu dữ liệu → như mục 2.5, không lưu, không gửi.\n'
           '• Phiếu đã bị đổi trạng thái / không còn là người tạo (sửa ở tab khác) → ' + CONFLICT + ', không lưu.\n'
           '• Kho không có thủ kho / người tạo không có công ty / không ai có quyền → vẫn lưu thành công, không ai nhận thông báo.\n'
           '• Gửi thông báo lỗi → không ảnh hưởng việc lưu.',
       dacbiet='Không có hộp xác nhận; nút khóa trong lúc lưu. Sau khi gửi kế hoạch không sửa / xóa được nữa. Vị trí của kế hoạch '
               'Đang kiểm bị chặn ở màn Phiếu điều chuyển vị trí cho tới khi kế hoạch được lập phiếu kiểm kê.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới => Lưu và gửi', 'Gửi ngay khi tạo kế hoạch.'),
       (MENU + ' => Sửa => Lưu và gửi', 'Gửi kế hoạch Đang tạo đã lưu trước đó.')],
       shot=shot('10c_filled'), shot_caption='Nút Lưu và gửi ở chân màn Tạo kế hoạch'),
   ui=[
       ('Nút Lưu và gửi', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Màu chính, biểu tượng máy bay giấy', '- Rê chuột: “Lưu và gửi kế hoạch cho thủ kho (trạng thái Đang kiểm)”',
         '- Khóa trong lúc lưu']),
       ('Các trường của form', 'Table/Grid', 'Enable', '–', 'Như mục 2.5', 'Như mục 2.5',
        '- Kho vật lý, Phạm vi, Chi tiết, Hội đồng — cùng điều kiện bắt buộc với nút Lưu.'),
       ('Trạng thái sau khi gửi', 'Badge', 'Read-only', '–', '–', 'Đang kiểm', '- Nhãn vàng “Đang kiểm” ở danh sách và tiêu đề chi tiết.'),
       ('Thông báo cho thủ kho', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tiêu đề “[KHKKVT] Tạo mới: <số phiếu>”', '- Ghi chú: Người lập, “Chờ lập phiếu kiểm kê”, Kho, Ghi chú (nếu có)',
         '- Bấm → mở màn chi tiết kế hoạch']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Lưu và gửi thành công.”', '- Thiếu: “Bạn chưa nhập đầy đủ thông tin.”', '- Xung đột: ' + CONFLICT]),
   ],
   ev=[
       ('Bấm Lưu và gửi', 'Click',
        'Before:\n– Không kiểm quyền riêng; màn Sửa: phiếu phải Đang tạo và người bấm là người tạo, nếu không → ' + CONFLICT + '.\n'
        + SAVE_DURING + '\n'
        'After:\n– Lưu kế hoạch trạng thái Đang kiểm (tạo mới: sinh số phiếu).\n'
        '– Ghi lịch sử: “Tạo mới” (màn Tạo) hoặc “Thay đổi thông tin” + “Thay đổi trạng thái” Đang tạo → Đang kiểm (màn Sửa).\n'
        '– Gửi thông báo cho thủ kho cùng công ty có quyền Lập phiếu kiểm kê kho theo vị trí.\n'
        '– Hiển thị “Lưu và gửi thành công.”, về màn danh sách.'),
       ('Bấm thông báo (thủ kho)', 'Click',
        'Before:\n– Thủ kho nhận thông báo.\nAfter:\n– Mở màn chi tiết kế hoạch; thấy nút Lập phiếu kiểm kê (mục 2.11).'),
   ])

# ------------------------------------------------------------ 2.8 Sửa
fr(8, 'Chỉnh sửa kế hoạch', usecase=('FR-08', 'Chỉnh sửa kế hoạch', 'crud', A_NV),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Chỉnh sửa kế hoạch kiểm kê theo vị trí',
       mota='Người tạo sửa kế hoạch còn Đang tạo: đổi kho, phạm vi, lấy lại vị trí (cập nhật ảnh chụp tồn), sửa hội đồng; lưu '
            'giữ Đang tạo (Lưu) hoặc gửi luôn (Lưu và gửi, mục 2.7). Số phiếu, Ngày kiểm kê không sửa được.',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo kế hoạch.\n3. Kế hoạch đang ở trạng thái Đang tạo.',
       chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
             '2. Hệ thống mở màn “Sửa kế hoạch kiểm kê theo vị trí: <số phiếu>”, điền sẵn kho, phạm vi đã tick, bảng Chi tiết đã '
             'lưu, hội đồng (cả nhân viên đã nghỉ / chức vụ cũ vẫn hiện tên).\n'
             '3. Người dùng sửa thông tin, bấm Lấy vị trí nếu đổi phạm vi.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống kiểm lại phiếu còn Đang tạo và đúng người tạo, kiểm tra dữ liệu như mục 2.5.\n'
             '6. Hệ thống ghi đè phạm vi, chi tiết, hội đồng; cập nhật người / ngày cập nhật.\n'
             '7. Hệ thống ghi nhận hành động “Thay đổi thông tin” trong lịch sử (giá trị cũ → mới của Kho vật lý, Nhà, Dãy, Khoang, '
             'Vị trí, Danh sách thành viên hội đồng kiểm kê) — không đổi gì thì không ghi.\n'
             '8. Hệ thống hiển thị “Lưu thành công.” và chuyển về màn danh sách.',
       phu='• Mở màn Sửa của kế hoạch không còn Đang tạo / không phải người tạo → tự chuyển sang màn chi tiết.\n'
           '• Kế hoạch ngoài phạm vi / đã bị xóa → trang “Không tìm thấy trang”.\n'
           '• Lưu khi phiếu vừa bị gửi / xóa ở tab khác → ' + CONFLICT + ' hoặc ' + NOTFOUND + '.\n'
           '• Thiếu dữ liệu → như mục 2.5.\n'
           '• Quay lại khi đã sửa → hộp “Thông tin chưa lưu”; không sửa gì → về danh sách ngay.\n'
           '• Hai người không thể cùng sửa: chỉ người tạo được sửa.',
       dacbiet='Kế hoạch không có trường duy nhất nên không có kiểm tra trùng. Bảng Chi tiết chỉ đổi khi bấm Lấy vị trí. Màn Sửa '
               'không có nút Lưu và tiếp tục.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('12_edit'), shot_caption='Màn Sửa kế hoạch kiểm kê theo vị trí'),
   ui=FORM_UI[:2] + [
       ('Số phiếu', 'Textbox', 'Disable', '<mã công ty>-KHKKVT-NNNNN', '–', 'Theo dữ liệu', '- Không sửa được.'),
       ('Ngày kiểm kê', 'Datepicker', 'Disable', 'dd/mm/yyyy', 'Có', 'Ngày tạo kế hoạch', '- Không sửa được.'),
   ] + FORM_UI[4:15] + FORM_UI[16:],
   ev=[
       ('Mở màn Sửa', 'System',
        'Before:\n– Kiểm tra phạm vi xem, nếu ngoài phạm vi → trang “Không tìm thấy trang”.\n'
        '– Kiểm tra người tạo + Đang tạo, nếu không → chuyển sang màn chi tiết.\n'
        'After:\n– Điền sẵn dữ liệu; chưa tính là đã thay đổi.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Kiểm lại phiếu còn Đang tạo và người bấm là người tạo, nếu không → ' + CONFLICT + '.\n' + SAVE_DURING + '\n'
        'After:\n– Ghi đè phạm vi, chi tiết, hội đồng; cập nhật người / ngày cập nhật.\n'
        '– Ghi một dòng lịch sử “Thay đổi thông tin” (cũ → mới) nếu có thay đổi.\n'
        '– Hiển thị “Lưu thành công.”, về màn danh sách.'),
       ('Bấm Lưu và gửi', 'Click', 'Before:\n– Như Lưu.\nDuring:\n– Như mục 2.7.\nAfter:\n– Như mục 2.7.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu với lúc mở.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu, không ghi lịch sử; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.9 Xóa
fr(9, 'Xóa kế hoạch', usecase=('FR-09', 'Xóa kế hoạch', 'action', A_NV),
   rule=('- Hộp thoại xác nhận Xóa và Thông báo.', 'delete'),
   intro=dict(
       ten='Xóa kế hoạch kiểm kê theo vị trí',
       mota='Người tạo xóa hẳn kế hoạch còn Đang tạo cùng toàn bộ dữ liệu con (phạm vi, chi tiết, kết quả sẵn, hội đồng). Kế hoạch '
            'đã gửi (Đang kiểm trở đi) không xóa được.',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo.\n3. Kế hoạch đang Đang tạo.',
       chinh='1. Người dùng bấm Xóa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa” với nội dung “Bạn có chắc muốn xóa bản ghi này không?”.\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm lại phiếu còn Đang tạo và đúng người tạo.\n'
             '5. Hệ thống ghi nhận hành động “Xóa” trong lịch sử, rồi xóa kế hoạch và mọi dữ liệu con.\n'
             '6. Hệ thống hiển thị “Xóa thành công.”; ở danh sách nạp lại, ở màn chi tiết quay về danh sách.',
       phu='• Bấm Hủy / (x) → đóng hộp, không xóa.\n'
           '• Phiếu vừa bị gửi / không còn là người tạo → ' + CONFLICT + ', không xóa.\n'
           '• Phiếu đã bị xóa ở tab khác → ' + NOTFOUND + '.\n'
           '• Kế hoạch Đang tạo chưa có phiếu kiểm kê nào nên không có ràng buộc dữ liệu đang sử dụng.',
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
        ['- Thành công: “Xóa thành công.”', '- Thất bại: ' + CONFLICT + ' hoặc “Xóa thất bại.”']),
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

# ------------------------------------------------------------ 2.10 Chi tiết
fr(10, 'Xem chi tiết kế hoạch',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết kế hoạch kiểm kê theo vị trí',
       mota='Màn chỉ đọc hiển thị thông tin chung, phạm vi đã tick (các mục khác bị mờ), bảng Chi tiết hàng tồn, hội đồng và khối '
            'Lịch sử; tiêu đề kèm nhãn trạng thái. Chân màn có nút theo cờ: Sửa / Xóa (Đang tạo, người tạo), Lập phiếu kiểm kê '
            '(Đang kiểm, thủ kho), In, Xuất Excel, Quay lại.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Kế hoạch trong phạm vi xem (hoặc là kế hoạch Đang kiểm của kho mình là '
                'thủ kho có quyền Q1).',
       chinh='1. Người dùng bấm Số phiếu ở danh sách (hoặc bấm thông báo).\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết kế hoạch kiểm kê theo vị trí: <số phiếu>” kèm nhãn trạng thái.\n'
             '4. Hệ thống hiển thị Thông tin chung, Phạm vi kiểm kê, Chi tiết, Hội đồng kiểm kê, khối Lịch sử (thu gọn, có số mốc).',
       phu='• Ngoài phạm vi / không tồn tại → trang “Không tìm thấy trang”.\n'
           '• Kế hoạch Đang tạo của người khác → coi như ngoài phạm vi.\n'
           '• Bấm Quay lại → về danh sách, khôi phục bộ lọc (trong 10 phút).',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết kế hoạch kiểm kê theo vị trí'),
   extra=[(shot('15_send_detail'), 'Màn chi tiết kế hoạch Đang kiểm của thủ kho — có nút Lập phiếu kiểm kê')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Chi tiết kế hoạch kiểm kê theo vị trí: <số phiếu>”', '- Kèm nhãn trạng thái màu theo trạng thái']),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Số phiếu', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- Mã kế hoạch.'),
       ('Ngày kiểm kê', 'Textbox', 'Disable', 'dd/mm/yyyy', 'Theo dữ liệu', '- Ngày tạo kế hoạch.'),
       ('Kho vật lý', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- Tên kho.'),
       ('Khối Phạm vi kiểm kê', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- 4 cột Nhà / Dãy / Khoang / Vị trí, mục đã tick được tích, không bấm được', '- Không có ô tìm, Chọn hết, Lấy vị trí']),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột như màn Tạo: STT, Nhà kho, Vị trí, Tên hàng, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn, Công ty, Lô, SL, Cộng',
         '- Số dạng 1,234']),
       ('Bảng Hội đồng kiểm kê', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- STT, Nhân viên, Chức vụ (ô khóa).'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
        ['- Số mốc cạnh tiêu đề', '- Nút Xem lịch sử / Thu gọn, Làm mới, Bộ lọc', '- Nội dung như mục 2.14']),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Phiếu Đang tạo của mình → mở màn Sửa.'),
       ('Nút Lập phiếu kiểm kê', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Đang kiểm + thủ kho có quyền (mục 2.11).'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Cửa sổ Xem trước (mục 2.12).'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', '- Tải file Excel kế hoạch (mục 2.13).'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Phiếu Đang tạo của mình (mục 2.9).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn danh sách.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → trang “Không tìm thấy trang”.\n'
        'During:\n– Lấy dữ liệu kế hoạch, cấu trúc kho, cờ nút.\nAfter:\n– Hiển thị màn chỉ đọc, nút theo cờ.'),
       ('Bấm Xem lịch sử', 'Click', 'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở rộng khối, hiện các mốc.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Không có dữ liệu cần lưu.\nAfter:\n– Về danh sách, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.11 Lập phiếu kiểm kê
fr(11, 'Lập phiếu kiểm kê từ kế hoạch', usecase=('FR-11', 'Lập phiếu kiểm kê', 'action', A_TK),
   rule=('- Màn Danh sách và Phân quyền.', 'list'),
   intro=dict(
       ten='Lập phiếu kiểm kê theo vị trí từ kế hoạch Đang kiểm',
       mota='Thủ kho bấm Lập phiếu kiểm kê ở kế hoạch Đang kiểm để mở màn Thêm phiếu kiểm kê theo vị trí (phân hệ Kho) đã nạp sẵn '
            'kế hoạch. Khi phiếu kiểm kê được lưu, kế hoạch chuyển Đã lập kiểm kê (màn Kiểm kê theo vị trí thực hiện).',
       tacnhan='Người dùng có quyền thực hiện chức năng: Lập phiếu kiểm kê kho theo vị trí, là thủ kho của kho (đầu tiên) của kế '
               'hoạch; Super admin.',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Kế hoạch đang Đang kiểm.\n3. Người dùng là thủ kho của kho kế hoạch '
                '(hoặc Super admin) và có quyền Lập phiếu kiểm kê kho theo vị trí.',
       chinh='1. Thủ kho bấm Lập phiếu kiểm kê ở cột Hành động hoặc chân màn chi tiết.\n'
             '2. Hệ thống mở màn Thêm phiếu kiểm kê theo vị trí với kế hoạch đã chọn sẵn: phạm vi, chi tiết lô, hội đồng.\n'
             '3. Thủ kho lưu phiếu kiểm kê ở màn đó; hệ thống đổi kế hoạch sang Đã lập kiểm kê và ghi “Thay đổi trạng thái” Đang '
             'kiểm → Đã lập kiểm kê (ghi chú “Lập phiếu kiểm kê <mã>.”) vào lịch sử kế hoạch.',
       phu='• Kế hoạch không còn Đang kiểm khi lưu phiếu kiểm kê → màn kia báo ' + CONFLICT + '.\n'
           '• Xóa phiếu kiểm kê → kế hoạch trở về Đang kiểm (lập lại được).\n'
           '• Phiếu kiểm kê duyệt kết quả không còn chênh lệch thiếu, hoặc điều chuyển xử lý hết chênh lệch → kế hoạch Hoàn thành.\n'
           '• Không đủ điều kiện → nút không hiện.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Lập phiếu kiểm kê', shot=shot('15_send_detail'),
               shot_caption='Nút Lập phiếu kiểm kê ở màn chi tiết kế hoạch Đang kiểm'),
   ui_kw=dict(required=False),
   ui=[
       ('Nút Lập phiếu kiểm kê trên dòng', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
        ['- Biểu tượng tài liệu có dấu cộng', '- Rê chuột: “Lập phiếu kiểm kê”']),
       ('Nút Lập phiếu kiểm kê ở chi tiết', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
        '- Rê chuột: “Lập phiếu kiểm kê theo vị trí từ kế hoạch này”.'),
       ('Nhãn trạng thái kế hoạch', 'Badge', 'Read-only', 'Danh sách 4 giá trị', 'Theo dữ liệu',
        ['- Đang kiểm → Đã lập kiểm kê khi lập phiếu', '- Đã lập kiểm kê → Đang kiểm khi xóa phiếu kiểm kê',
         '- → Hoàn thành khi phiếu kiểm kê hoàn tất']),
   ],
   ev=[
       ('Bấm Lập phiếu kiểm kê', 'Click',
        'Before:\n– Nút chỉ hiện khi Đang kiểm + thủ kho có quyền Lập phiếu kiểm kê kho theo vị trí.\n'
        'After:\n– Mở màn Thêm phiếu kiểm kê theo vị trí, nạp sẵn kế hoạch.'),
       ('Màn Kiểm kê theo vị trí lưu / xóa / hoàn tất phiếu', 'System',
        'Before:\n– Phiếu kiểm kê gắn với kế hoạch.\n'
        'After:\n– Đổi trạng thái kế hoạch tương ứng, cập nhật người / ngày cập nhật, ghi “Thay đổi trạng thái” vào lịch sử kế hoạch.'),
   ])

# ------------------------------------------------------------ 2.12 In
fr(12, 'In phiếu và in danh sách', usecase=('FR-12', 'In phiếu / In danh sách', 'io', A_NV),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In kế hoạch / In danh sách kế hoạch',
       mota='Xem trước và in một kế hoạch (mẫu in “Kế hoạch kiểm kê theo vị trí”: số phiếu, ngày kiểm kê, kho, hội đồng, bảng chi '
            'tiết, chỗ ký Người lập) hoặc in danh sách theo bộ lọc đang áp. Bản in mở trong cửa sổ trên màn đang đứng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm In ở cột Hành động / màn chi tiết (in phiếu), hoặc In danh sách trên bảng.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ xem trước, hiện “Đang tải dữ liệu in…” trong lúc dựng.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Danh sách quá 2.000 dòng → không dựng bản in, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc.\n'
           '• Không có dòng nào → “Không có dữ liệu để in”.\n'
           '• Ngoài phạm vi → ' + NOTFOUND + '.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in kế hoạch kiểm kê theo vị trí.” / “Thiếu mẫu in danh sách kế hoạch kiểm kê theo vị trí.”.\n'
           '• Bấm (x) → đóng cửa sổ.',
       dacbiet='Logo / tên công ty đầu bản in phiếu lấy theo công ty ghi trên kế hoạch; bản in danh sách theo công ty người in. '
               'Ngày ở khối ký là ngày in.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước kế hoạch',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   extra=[(shot('19_printlist'), 'Cửa sổ Xem trước danh sách kế hoạch')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–',
        ['- In phiếu: “Xem trước kế hoạch kiểm kê theo vị trí <số phiếu>”',
         '- In danh sách: “Xem trước danh sách kế hoạch kiểm kê theo vị trí”']),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', ['- Cạnh tiêu đề; bấm → hộp thoại in', '- Ẩn khi vượt 2.000 dòng']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Đang tải dữ liệu in…”.'),
       ('Đầu bản in phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Logo, tên công ty của kế hoạch', '- “KẾ HOẠCH KIỂM KÊ THEO VỊ TRÍ”, Số phiếu, Ngày kiểm kê',
         '- Kho vật lý, Hội đồng kiểm kê']),
       ('Bảng chi tiết bản in phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Nhà kho, Vị trí, Tên hàng, Mã hàng, ĐVT, SL tồn', '- Chi tiết tồn theo công ty: Công ty, Lô, SL, Cộng']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- “Ngày … Tháng … Năm …”, Người lập (tên người tạo kế hoạch).'),
       ('Bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        ['- Tiêu đề “DANH SÁCH KẾ HOẠCH KIỂM KÊ THEO VỊ TRÍ”', '- Cột: STT, Số phiếu, Ngày kiểm kê, Kho, Người tạo, Trạng thái',
         '- Khối ký bên phải: Ngày … Tháng … Năm …, Người lập']),
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
        'After:\n– Hiện bản xem trước khổ ngang.'),
       ('Bấm In trong cửa sổ', 'Click', 'Before:\n– Bản in đã dựng.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, giữ nguyên màn đang đứng.'),
   ])

# ------------------------------------------------------------ 2.13 Xuất Excel
fr(13, 'Xuất Excel', usecase=('FR-13', 'Xuất Excel', 'io', A_NV),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách / xuất 1 kế hoạch ra Excel',
       mota='(1) Xuất danh sách: chọn trường và thứ tự rồi xuất toàn bộ kế hoạch khớp bộ lọc (không phân trang). (2) Xuất 1 kế '
            'hoạch: nút Xuất Excel trên dòng / màn chi tiết tải file chi tiết của kế hoạch đó.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel trên bảng.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 8 trường (tích sẵn theo cột đang hiện).\n'
             '3. Người dùng tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy mọi kế hoạch theo bộ lọc + phạm vi xem, dựng file có letterhead công ty, tiêu đề, dòng thời gian '
             '(khi lọc Ngày kiểm kê), cột STT + trường đã chọn, khối ký.\n'
             '5. Hệ thống tải file “danh_sach_ke_hoach_kiem_ke_theo_vi_tri.xlsx”, báo “Xuất Excel thành công.”.\n'
             '6. Xuất 1 kế hoạch: bấm Xuất Excel trên dòng / chi tiết → tải “ke_hoach_kiem_ke_theo_vi_tri_<số phiếu>.xlsx”.',
       phu='• Không có kế hoạch khớp → vẫn ra file có tiêu đề, dòng tên cột và khối ký.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi → “Lỗi khi xuất Excel.”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng; nút Xuất Excel khóa trong lúc đang xuất. Ngày giữ dạng chữ dd/mm/yyyy hh:mm.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 8 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- Số phiếu, Ngày kiểm kê, Kho, Trạng thái', '- Người tạo, Ngày tạo, Ngày cập nhật, Người cập nhật']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/8 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Bấm → tải file', '- Khóa khi chưa tích / đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('File danh sách', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Letterhead công ty, tiêu đề “DANH SÁCH KẾ HOẠCH KIỂM KÊ THEO VỊ TRÍ”', '- Dòng “Từ ngày … đến ngày …” khi lọc Ngày kiểm kê',
         '- Cột STT + trường đã chọn; khối ký cuối file']),
       ('File 1 kế hoạch', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Tên “ke_hoach_kiem_ke_theo_vi_tri_<số phiếu>.xlsx”', '- Thông tin chung + bảng chi tiết như bản in (số giữ dạng số)']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công.”', '- Thất bại: “Lỗi khi xuất Excel.”']),
   ],
   ev=[
       ('Bấm Xuất Excel (bảng)', 'Click', 'Before:\n– Không có lượt xuất đang chạy.\nAfter:\n– Mở cửa sổ chọn trường.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Kéo bằng biểu tượng.\nAfter:\n– Đổi thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất.\n'
        'During:\n– Lấy toàn bộ kế hoạch theo bộ lọc + phạm vi xem.\n– Lỗi → “Lỗi khi xuất Excel.”.\n' + ERR + '\n'
        'After:\n– Tải file danh sách, báo “Xuất Excel thành công.”.'),
       ('Bấm Xuất Excel trên dòng / chi tiết', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → “Lỗi khi xuất Excel.”.\n'
        'After:\n– Tải file 1 kế hoạch, báo “Xuất Excel thành công.”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.14 Lịch sử
fr(14, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của kế hoạch',
       mota='Xem các mốc thao tác của kế hoạch: Tạo mới, Thay đổi thông tin (giá trị cũ → mới), Thay đổi trạng thái (kể cả do màn '
            'Kiểm kê theo vị trí / Phiếu điều chuyển vị trí đổi, kèm ghi chú mã phiếu), Xóa. Cửa sổ ở danh sách và khối Lịch sử ở '
            'màn chi tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động (hoặc trong menu Hành động khác), hoặc Xem lịch sử ở màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ “Lịch sử thay đổi: <số phiếu>” và hiển thị các mốc, mới nhất ở trên.',
       phu='• Kế hoạch từ hệ thống cũ chưa có mốc → “Chưa có lịch sử thao tác nào.”.\n'
           '• Bấm Bộ lọc → các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Lịch sử ghi phạm vi (Nhà / Dãy / Khoang / Vị trí), Kho vật lý, Danh sách thành viên hội đồng; KHÔNG ghi từng lô '
               'hàng tồn. Xem, in, xuất Excel không ghi mốc.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('16b_history_empty'), 'Kế hoạch chưa có lịch sử')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <số phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái: “Trạng thái: <cũ> → <mới>” kèm ghi chú (vd “Lập phiếu kiểm kê TPE-KKVT-00139.”)',
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
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng; danh sách giữ nguyên trang, bộ lọc.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Kế hoạch kiểm kê theo vị trí; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Kế hoạch không ghi tồn', [
        '– Lưu / gửi / sửa / xóa kế hoạch không đổi tồn kho, không sinh phiếu nhập / xuất.',
        '– Số tồn trên kế hoạch là ảnh chụp lúc bấm Lấy vị trí; muốn cập nhật phải Lấy vị trí lại (chỉ khi còn Đang tạo).'],
     ['Tạo', 'Chỉnh sửa', 'Lấy vị trí']),
    ('BR-02', 'Phạm vi xem', [
        '– V1 (hoặc Super admin): mọi kế hoạch; V2: công ty mình + của mình (công ty trống → chỉ của mình); không quyền: của mình.',
        '– Kế hoạch Đang tạo chỉ người tạo thấy.',
        '– Thủ kho có quyền Lập phiếu kiểm kê kho theo vị trí xem được chi tiết kế hoạch Đang kiểm của kho mình.',
        '– Ngoài phạm vi: chi tiết / in / xuất / lịch sử đều bị từ chối.'], ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất', 'Lịch sử']),
    ('BR-03', 'Dữ liệu bắt buộc khi lưu', [
        '– Lưu và Lưu và gửi cùng điều kiện: Kho vật lý, ≥ 1 vị trí tick, bảng Chi tiết có dữ liệu, ≥ 1 thành viên hội đồng có '
        'nhân viên + chức vụ, nhân viên không trùng.',
        '– Vị trí phải thuộc kho đã chọn; hàng, lô phải còn tồn tại; số lượng lô > 0.',
        '– Nhà / Dãy / Khoang có dấu * nhưng không bắt buộc riêng (vị trí tự do không cần khoang).'], ['Tạo', 'Chỉnh sửa', 'Lưu và gửi']),
    ('BR-04', 'Điều kiện sửa / xóa', [
        '– Chỉ người tạo, chỉ khi Đang tạo; máy chủ kiểm lại lúc lưu / xóa, sai → báo trạng thái đã thay đổi.',
        '– Xóa là xóa hẳn kế hoạch và dữ liệu con; kế hoạch đã gửi không xóa được nên không có ràng buộc phiếu kiểm kê.'],
     ['Chỉnh sửa', 'Xóa']),
    ('BR-05', 'Vòng đời trạng thái', [
        '– Lưu → Đang tạo; Lưu và gửi → Đang kiểm (không hỏi xác nhận).',
        '– Lập phiếu kiểm kê → Đã lập kiểm kê; xóa phiếu kiểm kê → Đang kiểm; phiếu kiểm kê duyệt kết quả không thiếu / điều chuyển '
        'xử lý hết → Hoàn thành.',
        '– Không có Duyệt / Không duyệt / Hủy / Khóa trên màn này.'], ['Lưu và gửi', 'Lập phiếu kiểm kê']),
    ('BR-06', 'Tính duy nhất', [
        '– Không có trường nhập duy nhất; mã <mã công ty>-KHKKVT-NNNNN tự sinh (công ty người tạo + số thứ tự), không sửa được.',
        '– Hai kế hoạch cùng kho, cùng phạm vi vẫn được lưu.', '– Nút lưu khóa trong lúc lưu chống tạo trùng.'], ['Tạo']),
    ('BR-07', 'Chuẩn hóa dữ liệu nhập', [
        '– Ngày kiểm kê = ngày tạo, không nhập tay.', '– Tổ chức (công ty / phòng ban / bộ phận) của kế hoạch = của người tạo.',
        '– Chọn nhân viên tự điền chức vụ đầu tiên; danh mục kho đã khóa không hiện để chọn mới.'], ['Tạo', 'Chỉnh sửa']),
    ('BR-08', 'Liên kết cấp cha – con', [
        '– Phạm vi: bỏ tick cấp cha tự bỏ tick cấp con; vị trí tự do độc lập.',
        '– Chi tiết: vị trí > hàng (SL tồn) > công ty (Cộng = tổng các lô) > lô (SL); mỗi lô kèm 1 dòng kết quả sẵn theo đơn vị cơ sở.'],
     ['Tạo', 'Chỉnh sửa', 'Lấy vị trí']),
    ('BR-09', 'Khóa vị trí đang kiểm kho', [
        '– Vị trí thuộc kế hoạch Đang kiểm bị coi là đang kiểm kho: màn Phiếu điều chuyển vị trí không cho chọn và chặn khi điều chuyển.'],
     ['Lưu và gửi']),
    ('BR-10', 'Thông báo', [
        '– Lưu với trạng thái Đang kiểm (tạo hoặc sửa) → gửi “[KHKKVT] Tạo mới: <số phiếu>” cho thủ kho của kho, cùng công ty người '
        'gửi, có quyền Lập phiếu kiểm kê kho theo vị trí; lỗi gửi không làm hỏng việc lưu.'], ['Lưu và gửi']),
    ('BR-11', 'In và xuất', [
        '– Letterhead bản in / file 1 kế hoạch theo công ty ghi trên kế hoạch; bản in danh sách theo công ty người in.',
        '– In danh sách tối đa 2.000 dòng; Xuất Excel danh sách không giới hạn, rỗng vẫn ra file.'], ['In', 'Xuất Excel']),
    ('BR-12', 'Sử dụng ở màn khác', [
        '– Kho vật lý, Nhà kho, Dãy, Khoang, Vị trí, hàng hóa đã có trong kế hoạch không xóa được ở danh mục.',
        '– Màn Kiểm kê theo vị trí chỉ chọn kế hoạch Đang kiểm mà người dùng được lập phiếu.'], ['Tạo', 'Lưu và gửi']),
    ('BR-13', 'Quy tắc ghi lịch sử', [
        '– Ghi: Tạo mới; Thay đổi thông tin (Kho vật lý, Nhà, Dãy, Khoang, Vị trí, Danh sách thành viên hội đồng — cũ → mới, '
        'không đổi thì không ghi); Thay đổi trạng thái (kèm ghi chú mã phiếu khi màn khác đổi); Xóa.',
        '– Không ghi từng lô hàng tồn; xem / in / xuất không ghi; hiển thị mới nhất ở trên.'], ['Tạo', 'Chỉnh sửa', 'Xóa', 'Lịch sử']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Kế hoạch kiểm kê theo vị trí (trạng thái, phạm vi vị trí, hàng – lô, '
    'hội đồng).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Kiểm kê theo vị trí (popup Chọn kế hoạch chỉ hiện kế hoạch Đang kiểm mà người dùng được lập phiếu; nạp sẵn phạm '
                 'vi, hàng – lô, hội đồng; lập phiếu → kế hoạch Đã lập kiểm kê, xóa phiếu → trả về Đang kiểm, duyệt kết quả '
                 'không thiếu → Hoàn thành; liên kết mở chi tiết kế hoạch)', 'Kho -> Kiểm kho -> Theo vị trí'),
    ('2', 'Kho', 'Phiếu điều chuyển vị trí (vị trí của kế hoạch Đang kiểm bị đánh dấu đang kiểm kho, không chọn / chặn điều chuyển; '
                 'điều chuyển xử lý hết chênh lệch của phiếu kiểm kê → kế hoạch Hoàn thành)', 'Kho -> Điều chuyển'),
    ('3', 'Kho', 'Kho vật lý (không xóa được kho đã có trong kế hoạch)', 'Kho -> Danh mục'),
    ('4', 'Kho', 'Nhà kho (không xóa được nhà đã tick trong kế hoạch; nhà đã khóa không hiện để tick mới)', 'Kho -> Danh mục'),
    ('5', 'Kho', 'Dãy (không xóa được dãy đã tick trong kế hoạch; dãy đã khóa không hiện để tick mới)', 'Kho -> Danh mục'),
    ('6', 'Kho', 'Khoang (không xóa được khoang đã tick trong kế hoạch; khoang đã khóa không hiện để tick mới)', 'Kho -> Danh mục'),
    ('7', 'Kho', 'Vị trí (không xóa được vị trí đã có trong kế hoạch; vị trí đã khóa không hiện để tick mới)', 'Kho -> Danh mục'),
    ('8', 'Danh mục dùng chung', 'Hàng hoá, vật tư (các màn danh sách hàng hoá: không xóa được hàng đã có trong chi tiết kế hoạch)',
     'Danh mục dùng chung -> Hàng hoá -> Hàng hoá, vật tư'),
    ('9', 'Hệ thống ERP', 'Trang chủ — thẻ “Kế hoạch kiểm kê vị trí chờ duyệt” (đếm kế hoạch Đang kiểm của kho mà thủ kho phụ trách)',
     'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
