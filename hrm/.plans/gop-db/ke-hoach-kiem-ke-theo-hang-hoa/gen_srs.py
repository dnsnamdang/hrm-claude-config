# -*- coding: utf-8 -*-
"""SRS màn "Kế hoạch kiểm kê theo hàng hóa" (mã phiếu <mã công ty>.KHKKHH-NNNNN) — form chuẩn Danh mục quốc gia, chuẩn 04/11/2026.

Chạy: python gen_srs.py  → SRS - Kế hoạch kiểm kê theo hàng hóa.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc
  ../ke-hoach-kiem-ke-theo-vi-tri/gen_srs.py (05/11, Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn).
Nguồn đọc 05/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Entities/SelfInventoryRequest/SelfInventoryRequest.php, Services/SelfInventoryRequest{,Write,Print}Service.php,
      Http/Controllers/V1/SelfInventoryRequestController.php, Http/Requests/SelfInventoryRequest/SelfInventoryRequestStoreRequest.php,
      Exports/SelfInventoryRequestExport.php + views/exports/self_inventory_request.blade.php, Services/SelfInventoryWriteService.php
      (đổi trạng thái kế hoạch khi lập phiếu), Services/SelfInventoryService.php (popup chọn kế hoạch)}, MasterData ProductPickerService
      (stock_warehouse_ids), app/Services/CatalogHistoryService.php, Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (3 quyền)
  FE  pages/finance/self-inventory-requests/** (index, create, _id/index, _id/edit, components/{SelfInventoryRequestForm,
      PendingVouchersModal, row-actions.js, export-excel.js}), components/subsystem-menu/finance.js (nhóm Kiểm kê),
      components/product/picker/V2ProductPickerModal.vue
Phân biệt: màn "Kế hoạch tổng kiểm kê hàng hóa" (/finance/self-inventory-request-alls) dùng BẢNG RIÊNG, chỉ dùng CHUNG 3 tên quyền.
Ảnh: ./khkkhh_shots — dev-hrm 05/11/2026 (_capture/capture.js, chặn mọi yêu cầu ghi; cho qua yêu cầu chỉ đọc tồn kế toán). Bật cờ tạm
  trên trình duyệt (sửa phản hồi GET, không gửi máy chủ): 12_edit, 13_delete, 03_rowmenu, 15_send_detail (dev chỉ có kế hoạch
  Đã lập phiếu kiểm kê). 10b_validate: gọi kiểm tra của form trên trình duyệt. 10f_pending: mở popup cảnh báo trên trình duyệt.
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

TEN = 'Kế hoạch kiểm kê theo hàng hóa'
SHOTS = os.path.join(HERE, 'khkkhh_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Kiểm kê => Kế hoạch kiểm kê theo hàng hóa'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Kế hoạch kiểm kê theo hàng hóa.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NOTFOUND = '“Không tìm thấy kế hoạch kiểm kê hoặc bạn không có quyền xem.”'
Q1 = 'Lập phiếu kiểm kê kho theo hàng hóa'
V1 = 'Tổng kiểm kê kho theo hàng hóa - tổng công ty'
V2 = 'Tổng kiểm kê kho theo hàng hóa'

A_NV = 'Người lập kế hoạch'
A_TK = 'Người lập phiếu kiểm kê'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng đã được cấp tài khoản (màn không gắn quyền thao tác); phạm vi '
      'xem theo quyền “%s” / “%s”.' % (V1, V2))
TN_OWNER = 'Người dùng có quyền thực hiện chức năng: người lập kế hoạch (người tạo phiếu), phiếu đang ở trạng thái Đang tạo.'
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Kế hoạch kiểm kê theo hàng hóa.\n'
      '3. Dữ liệu hiển thị trong phạm vi xem theo quyền (mục Phần 2).')

d = SrsDoc(out=OUT, menu=MENU, route='/finance/self-inventory-requests', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Kiểm kê': 'menu_nhom', 'Kế hoạch kiểm kê theo hàng hóa': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Thêm hàng hóa': 'btn_themhang', 'Lưu và kiểm': 'btn_luukiem', 'Sửa': 'btn_sua_row',
    'Xóa': 'btn_xoa_row', 'Xem chi tiết': 'link_sophieu', 'Lập phiếu kiểm kê theo hàng hóa': 'btn_lapphieu_row',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Kế hoạch kiểm kê theo hàng hóa (mã phiếu <mã công ty>.KHKKHH-NNNNN, ví dụ '
    'TPE.KHKKHH-00020), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ cách người lập kế hoạch chọn một hoặc nhiều kho, chọn các mặt hàng cần kiểm (chỉ hàng còn tồn kho kế toán trong các '
    'kho đã chọn), chụp số tồn kế toán theo từng kho kế toán và chỉ định Hội đồng kiểm kê, rồi chuyển kế hoạch sang Đang kiểm để '
    'người có quyền lập phiếu kiểm kê theo hàng hóa.',
    'Làm rõ vòng đời trạng thái của kế hoạch (Đang tạo → Đang kiểm → Đã lập phiếu kiểm kê) và màn khác đổi trạng thái của kế hoạch.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo kế hoạch (Lưu / Lưu và tiếp tục), '
    'Thêm hàng hóa (popup chọn hàng) và Làm mới số liệu tồn, Lưu và kiểm (kiểm phiếu nhập / xuất kho còn treo), Chỉnh sửa, Xóa, '
    'Xem chi tiết, Lập phiếu kiểm kê theo hàng hóa từ kế hoạch (mở màn Kiểm kê theo hàng hóa), In phiếu / In danh sách, Xuất Excel '
    '(danh sách và 1 phiếu), Xem lịch sử thay đổi. Màn KHÔNG có Duyệt / Không duyệt, Hủy, Khóa / Mở khóa và Import Excel; trạng '
    'thái Đã lập phiếu kiểm kê do màn Kiểm kê theo hàng hóa (phân hệ Kho) đổi.')
d.p('Phân biệt với màn Kế hoạch tổng kiểm kê hàng hóa (cùng nhóm menu Kiểm kê): màn đó lưu dữ liệu riêng, không đọc / ghi kế hoạch của '
    'màn này; hai màn chỉ dùng chung 3 tên quyền ở Phần 2.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Kế hoạch là căn cứ để lập phiếu kiểm kê theo hàng hóa: phiếu kiểm kê nạp sẵn kho, danh sách hàng và hội đồng của kế hoạch, '
    'không cho thêm / bớt hàng.',
    'Số tồn trên kế hoạch là ẢNH CHỤP lúc thêm hàng (hoặc lúc bấm Làm mới số liệu rồi Lưu), không tự cập nhật theo tồn kho sau đó.',
    'Kế hoạch không ghi tồn kho, không sinh phiếu nhập / xuất.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Phạm vi xem theo quyền tổng công ty / công ty; không quyền chỉ thấy phiếu mình tạo; phiếu Đang tạo chỉ người tạo thấy (BR-02).',
    'Chỉ người tạo được Sửa / Xóa và chỉ khi phiếu còn Đang tạo (BR-04).',
    'Lưu và Lưu và kiểm cùng một bộ điều kiện bắt buộc: ít nhất 1 kho, ít nhất 1 hàng hóa có tồn kho kế toán, ít nhất 1 thành viên '
    'hội đồng có chức vụ (BR-03).',
    'Lưu và kiểm bị chặn khi các kho đã chọn còn phiếu nhập kho / xuất kho chưa xử lý xong có chứa hàng của kế hoạch (BR-09).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Kế hoạch kiểm kê theo hàng hóa (kế hoạch)', 'Chứng từ <mã công ty>.KHKKHH-NNNNN của màn này: các kho, danh sách hàng cần '
                                                 'kiểm kèm ảnh chụp tồn kho kế toán và hội đồng kiểm kê.'),
    ('Phiếu kiểm kê theo hàng hóa', 'Phiếu lập từ kế hoạch ở màn Kiểm kê theo hàng hóa (phân hệ Kho) để nhập kết quả thực kiểm.'),
    ('Kho', 'Kho vật lý chứa hàng; một kế hoạch có thể gồm nhiều kho. Chỉ chọn được kho đang hoạt động có kho kế toán thuộc công '
            'ty người đăng nhập.'),
    ('Kho kế toán', 'Kho sổ sách gắn với kho vật lý, theo công ty; mỗi hàng của kế hoạch có một hoặc nhiều dòng kho kế toán.'),
    ('SL tồn kho kế toán / Tổng SL', 'Trường đặc thù của bảng Hàng hóa: SL tồn kho kế toán = tồn của hàng ở từng kho kế toán (> 0); '
                                     'Tổng SL = cộng SL tồn kho kế toán của hàng.'),
    ('Làm mới số liệu', 'Thao tác lấy lại tồn kho kế toán hiện tại của các hàng trong bảng, bỏ hàng hết tồn; chỉ đổi trên màn, phải '
                        'bấm Lưu mới ghi.'),
    ('Phiếu chưa xử lý xong', 'Phiếu nhập kho / xuất kho của các kho đã chọn có chứa hàng của kế hoạch nhưng chưa hoàn tất; chặn '
                              'Lưu và kiểm.'),
    ('Hội đồng kiểm kê', 'Danh sách nhân viên tham gia kiểm kê, mỗi người kèm 1 chức vụ.'),
    ('Trạng thái Đang tạo', 'Nhãn xám: kế hoạch lưu bằng nút Lưu; chỉ người tạo thấy, sửa, xóa.'),
    ('Trạng thái Đang kiểm', 'Nhãn vàng: kế hoạch lưu bằng nút Lưu và kiểm; chờ lập phiếu kiểm kê, không sửa / xóa được.'),
    ('Trạng thái Đã lập phiếu kiểm kê', 'Nhãn xanh dương: đã có phiếu kiểm kê theo hàng hóa lập từ kế hoạch.'),
    ('Trạng thái Hoàn thành', 'Nhãn xanh lá: chỉ hiển thị cho dữ liệu cũ; không luồng nào đưa kế hoạch về trạng thái này nên không '
                              'có trong ô lọc.'),
    ('Cấu trúc phân cấp', 'Kế hoạch > kho > hàng hóa (Tổng SL) > kho kế toán (SL tồn kho kế toán); kèm hội đồng kiểm kê.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn không gắn quyền cho thao tác Tạo / Sửa / Xóa / In / Xuất / Lịch sử: mọi người dùng đăng nhập đều lập được kế hoạch. '
    'Hai quyền riêng của màn chỉ quyết định PHẠM VI dữ liệu được xem; quyền “%s” (nhóm Kiểm kê theo hàng hóa, phân hệ Kho) '
    'quyết định nút Lập phiếu kiểm kê theo hàng hóa và người nhận thông báo. Super admin được coi như có đủ quyền. Ba tên quyền '
    'này cũng được màn Kế hoạch tổng kiểm kê hàng hóa dùng.' % Q1)
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1,
     'Thấy nút Lập phiếu kiểm kê theo hàng hóa ở kế hoạch Đang kiểm; nhận thông báo khi kế hoạch cùng công ty được Lưu và kiểm; '
     'xem được chi tiết kế hoạch Đang kiểm dù ngoài phạm vi xem (để bấm thông báo).'),
    ('—', 'Không cần quyền', 'Tạo mới, Lưu, Lưu và kiểm, Lưu và tiếp tục; Sửa / Xóa khi là người tạo và phiếu Đang tạo; In, Xuất '
                              'Excel, Lịch sử với phiếu trong phạm vi xem.'),
], widths=[0.8, 1.8, 3.4])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Mọi kế hoạch của mọi công ty; ô lọc Công ty – Phòng ban chọn được mọi công ty (Super admin như V1).'),
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
    ('FR-06 Thêm hàng hóa và Làm mới số liệu', '✅', '✅', '✅', '✅'),
    ('FR-07 Lưu và kiểm', '✅', '✅', '✅', '✅'),
    ('FR-08 Chỉnh sửa', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo'),
    ('FR-09 Xóa', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo'),
    ('FR-10 Xem chi tiết', '✅ + kế hoạch Đang kiểm', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-11 Lập phiếu kiểm kê theo hàng hóa', '✅ Đang kiểm', '❌', '❌', '❌'),
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
    'Thiếu Q1: nút Lập phiếu kiểm kê theo hàng hóa không hiện; lưu phiếu kiểm kê từ kế hoạch ở màn Kiểm kê theo hàng hóa bị từ chối '
    '“Bạn không có quyền thực hiện chức năng này.”.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới, Xuất Excel, In danh sách, Cấu hình cột', 'Luôn hiện', 'Không gắn quyền'),
    ('Nút Sửa, Xóa (dòng và màn chi tiết)', 'Người xem là người tạo và phiếu Đang tạo', 'Máy chủ kiểm lại khi lưu / xóa'),
    ('Nút Lập phiếu kiểm kê theo hàng hóa', 'Phiếu Đang kiểm, người xem có Q1 (hoặc Super admin)',
     'Mở màn Tạo phiếu kiểm kê theo hàng hóa, cùng tab'),
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
     ('FR-07', 'Lưu và kiểm', 'action'),
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
     ('FR-06', 'Thêm hàng hóa, Làm mới số liệu', 'crud', 'extend', [1, 3], None)],
    'Sơ đồ Use Case tổng quan màn Kế hoạch kiểm kê theo hàng hóa')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách kế hoạch',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách kế hoạch kiểm kê theo hàng hóa',
       mota='Hiển thị bảng các kế hoạch kiểm kê theo hàng hóa trong phạm vi xem của người dùng (theo quyền tổng công ty / công ty '
            '/ của mình), kèm trạng thái, các kho, người tạo, ngày tạo / cập nhật, phân trang và tổng số. Mỗi dòng có liên kết sang '
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
               'Hành động; Số phiếu ghim trái khi cuộn ngang. Sắp xếp được: Số phiếu, Ngày kiểm kê, Ngày tạo; mặc định (chưa '
               'chọn cột) ngày tạo mới nhất ở trên. Đổi sắp xếp / bộ lọc / số dòng đều về trang 1.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Kế hoạch kiểm kê theo hàng hóa'),
   extra=[(shot('03_rowmenu'), 'Nút thao tác theo trạng thái: dòng Đang tạo (Sửa, Xóa, Hành động khác) và dòng Đang kiểm')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Danh sách kế hoạch kiểm kê theo hàng hóa” trên thanh tiêu đề, tiêu đề bảng và tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “Tạo kế hoạch kiểm kê theo hàng hóa”', '- Bấm → mở màn Tạo kế hoạch (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.13)',
         '- Khóa trong lúc đang xuất file']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “In danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.12)']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Đánh số liên tục theo trang', '- Cột khóa trong Tùy chỉnh cột']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', '<mã công ty>.KHKKHH-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết (mục 2.10)', '- Sắp xếp được', '- Cột khóa, ghim trái khi cuộn ngang']),
       ('Cột Ngày kiểm kê', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Ngày giờ lập kế hoạch (trùng Ngày tạo)', '- Sắp xếp được']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Tên các kho của kế hoạch, nối bằng dấu phẩy theo thứ tự đã chọn', '- Không sắp xếp']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 4 giá trị', 'Hiển thị',
        ['- Đang tạo: nhãn xám', '- Đang kiểm: nhãn vàng', '- Đã lập phiếu kiểm kê: nhãn xanh dương',
         '- Hoàn thành: nhãn xanh lá (chỉ dữ liệu cũ)', '- Không sắp xếp']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Họ tên người lập kế hoạch', '- Không sắp xếp']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', ['- Thời điểm lưu lần đầu', '- Sắp xếp được']),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        '- Thời điểm cập nhật gần nhất (kể cả khi màn Kiểm kê theo hàng hóa đổi trạng thái kế hoạch); không sắp xếp.'),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Họ tên người cập nhật gần nhất.'),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Sửa (bút chì): chỉ phiếu Đang tạo của chính mình → mở màn Sửa (mục 2.8)',
           '- Xóa (thùng rác đỏ): cùng điều kiện → hộp Xác nhận xóa (mục 2.9)',
           '- Lập phiếu kiểm kê theo hàng hóa: phiếu Đang kiểm, người xem có Q1 (mục 2.11)',
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
        'Before:\n– Chỉ Số phiếu, Ngày kiểm kê, Ngày tạo hỗ trợ sắp xếp.\n'
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
       mota='Thu hẹp danh sách theo số phiếu, kho, trạng thái, người tạo, mã hàng hóa, tên hàng hóa, ngày kiểm kê và công ty – phòng '
            'ban. Ô tìm nhanh tìm theo số phiếu; các ô lọc nằm trong khối Tìm kiếm nâng cao, bật / tắt được bằng Cài đặt bộ lọc '
            '(mục 2.3).',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập số phiếu vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Hệ thống lọc ngay khi một ô chọn đổi giá trị, về trang 1; ô chữ Mã hàng hóa / Tên hàng hóa áp khi bấm Tìm kiếm.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Không có quyền V1 / V2 → không có ô Công ty – Phòng ban; có V2 → ô Công ty khóa ở công ty mình.\n'
           '• Ô lọc bị tắt trong Cài đặt bộ lọc → không hiện trên khối lọc.',
       dacbiet='Ô tìm nhanh / Mã hàng hóa / Tên hàng hóa khớp một phần, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối; '
               'không giới hạn số ký tự; ký tự % và _ được hiểu là ký tự đại diện. Mã / Tên hàng hóa so với mã, tên hàng đã lưu '
               'trên kế hoạch. Kho lọc kế hoạch có chứa kho đó. Ngày kiểm kê lấy trọn hai ngày biên. Ô Trạng thái không có '
               'Hoàn thành. Mọi điều kiện kết hợp kiểu VÀ. Ghi nhớ bộ lọc trên trình duyệt 10 phút khi đi vào màn con của màn này.'),
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
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (mọi trạng thái)', '- Lựa chọn: Đang tạo / Đang kiểm / Đã lập phiếu kiểm kê']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Toàn bộ nhân viên (kể cả người chưa tạo kế hoạch nào)']),
       ('Mã hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        '- Kế hoạch có ít nhất 1 hàng có mã chứa chuỗi nhập.'),
       ('Tên hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        '- Kế hoạch có ít nhất 1 hàng có tên chứa chuỗi nhập.'),
       ('Ngày kiểm kê', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai ngày biên; được bỏ trống một đầu']),
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
        'During:\n– Tìm kế hoạch có số phiếu chứa chuỗi nhập (và hàng khớp mã / tên).\n'
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
        ['- Kho, Trạng thái, Người tạo, Mã hàng hóa', '- Tên hàng hóa, Ngày kiểm kê, Công ty – Phòng ban']),
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
     ['- Tạo: “Tạo kế hoạch kiểm kê theo hàng hóa”', '- Sửa: “Sửa kế hoạch kiểm kê theo hàng hóa: <số phiếu>”']),
    ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập',
     '- Góc phải khối Thông tin chung: màn Tạo ghi tên người đăng nhập; màn Sửa ghi “<Người tạo> - dd/mm/yyyy hh:mm”.'),
    ('Ngày kiểm kê', 'Datepicker', 'Disable', 'dd/mm/yyyy', 'Có', 'Ngày hiện tại',
     ['- Ô khóa nền xám, không sửa được', '- Màn Tạo: hôm nay; màn Sửa: ngày kiểm kê đã lưu',
      '- Mỗi lần lưu (kể cả khi sửa) hệ thống ghi lại bằng ngày lưu']),
    ('Kho', 'Dropdown', 'Enable', 'Danh sách kho', 'Có', 'Trống',
     ['- Chọn được NHIỀU kho; gợi ý “Chọn kho”; hiển thị “Mã - Tên”',
      '- Chỉ kho đang hoạt động có kho kế toán thuộc công ty người đăng nhập (màn Sửa: luôn có kho phiếu đang gắn)',
      '- Đổi kho khi bảng Hàng hóa đã có dòng → hộp “Đổi kho” (mục 2.6)', '- Lỗi: “Kho – Vui lòng chọn kho.”']),
    ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     ['- Gợi ý “Nhập ghi chú”, 2 dòng', '- Không gõ quá 255 ký tự', '- Lỗi: “Ghi chú – Tối đa 255 ký tự.”']),
    ('Nút Làm mới số liệu', 'Button', 'Enable / Disable', '–', '–', 'Disable khi bảng trống',
     ['- Góc phải tiêu đề khối Hàng hóa', '- Rê chuột: “Cập nhật lại tồn kho kế toán của các hàng trong bảng”',
      '- Bấm → lấy lại tồn kho kế toán (mục 2.6)']),
    ('Nút Thêm hàng hóa', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Góc phải tiêu đề khối Hàng hóa', '- Bấm → mở popup “Thêm hàng hóa” (mục 2.6)',
      '- Chưa chọn kho → lỗi đỏ dưới ô Kho, thông báo “Vui lòng chọn kho trước khi thêm hàng hóa.”',
      '- Khóa trong lúc đang lấy tồn']),
    ('Bảng Hàng hóa', 'Table/Grid', 'Read-only', '–', 'Có', '“Không có dữ liệu”',
     ['- Cột: STT, Tên hàng, Model, Mã hàng, ĐVT, Kho kế toán, SL tồn kho kế toán, Tổng SL, Hành động',
      '- Mỗi kho kế toán 1 dòng; STT, Tên hàng, Model, Mã hàng, ĐVT, Tổng SL, Hành động gộp ô theo hàng',
      '- Kho kế toán ghi “Mã - Tên”; số dạng 1,234.5; khung cao tối đa 600px, tiêu đề dính khi cuộn',
      '- Lỗi: “Hàng hóa – Vui lòng thêm ít nhất 1 hàng hóa.” (khung bảng viền đỏ)']),
    ('Nút Xóa dòng hàng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Thùng rác đỏ ở cột Hành động; bấm → bỏ hàng ngay, không hỏi.'),
    ('Khối Hội đồng kiểm kê', 'Table/Grid', 'Enable', '≥ 1 dòng', 'Có', '1 dòng trống (màn Tạo)',
     ['- Cột STT, Thành viên *, Chức vụ *, Hành động', '- Không có dòng: “Không có dữ liệu”',
      '- Lỗi: “Hội đồng kiểm kê – Vui lòng thêm ít nhất 1 thành viên.”']),
    ('Nút Thêm dòng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề khối Hội đồng; bấm → thêm 1 dòng trống.'),
    ('Ô Thành viên', 'Dropdown', 'Enable', 'Nhân viên đang làm việc', 'Có', 'Trống',
     ['- Gợi ý “Chọn thành viên”', '- Chọn → tự điền Chức vụ đầu tiên của nhân viên; bỏ chọn → xóa Chức vụ',
      '- Lỗi: “Thành viên – Vui lòng chọn thành viên.” / “Thành viên – Bị trùng.”']),
    ('Ô Chức vụ', 'Dropdown', 'Enable', 'Chức vụ của nhân viên', 'Có', 'Chức vụ đầu tiên',
     ['- Gợi ý “Chọn chức vụ”', '- Lỗi: “Chức vụ – Vui lòng chọn chức vụ.”']),
    ('Nút Xóa dòng hội đồng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Thùng rác đỏ; bấm → xóa dòng ngay, không hỏi.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Rê chuột: “Lưu kế hoạch ở trạng thái Đang tạo”', '- Lưu xong về danh sách; khóa trong lúc lưu']),
    ('Nút Lưu và kiểm', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Rê chuột: “Lưu và chuyển kế hoạch sang trạng thái Đang kiểm”', '- Đặc tả ở mục 2.7']),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị ở màn Tạo',
     ['- Rê chuột: “Lưu (Đang tạo) rồi ở lại tạo kế hoạch tiếp theo”', '- Không có ở màn Sửa']),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi “Thông tin chưa lưu”.'),
    ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Nội dung: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút Thoát: rời màn, không lưu',
      '- Nút Ở lại / (x): đóng hộp, giữ dữ liệu']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Thành công: “Lưu thành công.” / “Lưu và kiểm thành công.”', '- Thiếu: “Bạn chưa nhập đầy đủ thông tin.”',
      '- Phiếu đã đổi trạng thái: ' + CONFLICT, '- Lỗi khác: câu lỗi của máy chủ hoặc “Lưu thất bại.”']),
]

SAVE_DURING = ('During:\n– Kho trống → “Kho – Vui lòng chọn kho.”\n'
               '– Ghi chú quá 255 ký tự → “Ghi chú – Tối đa 255 ký tự.”\n'
               '– Bảng Hàng hóa trống → “Hàng hóa – Vui lòng thêm ít nhất 1 hàng hóa.”\n'
               '– Hội đồng không có dòng → “Hội đồng kiểm kê – Vui lòng thêm ít nhất 1 thành viên.”; dòng thiếu thành viên → '
               '“Thành viên – Vui lòng chọn thành viên.”; trùng → “Thành viên – Bị trùng.”; thiếu chức vụ → “Chức vụ – Vui lòng '
               'chọn chức vụ.”\n'
               '– Mọi lỗi hiện cùng lúc dưới từng ô, thông báo “Bạn chưa nhập đầy đủ thông tin.”, cuộn tới ô lỗi đầu tiên.\n'
               '– Máy chủ kiểm lại: hàng không còn → “Hàng hóa – Không tồn tại.”; hàng không có dòng kho kế toán → “Hàng hóa – '
               'Không có tồn kho kế toán.”; kho kế toán không còn → “Kho kế toán – Có kho kế toán không tồn tại. Vui lòng thêm '
               'lại hàng hóa.”; kho chọn trùng → “Kho – Bị trùng.”\n' + ERR)

fr(5, 'Tạo kế hoạch kiểm kê (Lưu / Lưu và tiếp tục)', usecase=('FR-05', 'Tạo kế hoạch', 'crud', A_NV),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo kế hoạch kiểm kê theo hàng hóa',
       mota='Người lập chọn một hoặc nhiều kho, thêm các hàng cần kiểm (kèm ảnh chụp tồn kho kế toán theo từng kho kế toán), nhập '
            'ghi chú, khai Hội đồng kiểm kê rồi bấm Lưu: kế hoạch được lưu ở trạng thái Đang tạo (chỉ người tạo thấy), chưa báo '
            'cho ai. Kế hoạch không ghi tồn kho.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Công ty của người dùng có ít nhất 1 kho đang hoạt động có kho kế toán.\n'
                '3. Không cần quyền riêng để tạo.',
       chinh='1. Người dùng bấm Tạo mới ở danh sách.\n'
             '2. Hệ thống mở màn “Tạo kế hoạch kiểm kê theo hàng hóa”: Ngày kiểm kê = hôm nay, khối Hội đồng có sẵn 1 dòng trống, '
             'góc phải ghi tên người tạo.\n'
             '3. Người dùng chọn Kho (một hoặc nhiều).\n'
             '4. Người dùng bấm Thêm hàng hóa, chọn hàng ở popup (mục 2.6); hệ thống đổ hàng kèm tồn kho kế toán vào bảng Hàng hóa.\n'
             '5. Người dùng nhập Ghi chú (nếu cần), chọn Thành viên (Chức vụ tự điền), Thêm dòng nếu cần.\n'
             '6. Người dùng bấm Lưu.\n'
             '7. Hệ thống kiểm tra dữ liệu, lưu kế hoạch trạng thái Đang tạo với công ty / phòng ban của người tạo, Ngày kiểm kê = '
             'hôm nay, sinh mã <mã công ty>.KHKKHH-NNNNN; lưu các kho, hàng hóa (tên, mã, model, ĐVT chụp từ danh mục) kèm SL tồn '
             'từng kho kế toán và Tổng SL, hội đồng (kèm phòng ban, tên chức vụ).\n'
             '8. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu.\n'
             '9. Hệ thống hiển thị “Lưu thành công.” và chuyển về màn danh sách.',
       phu='• Bấm Lưu và tiếp tục → lưu như trên (Đang tạo), ở lại màn Tạo với form trắng.\n'
           '• Thiếu dữ liệu bắt buộc → báo đủ lỗi dưới từng ô cùng lúc, thông báo “Bạn chưa nhập đầy đủ thông tin.”, không lưu.\n'
           '• Bấm Quay lại / chuyển menu / đóng tab khi đã nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì thì về '
           'danh sách ngay.\n'
           '• Màn là trang riêng, không có (x) / click ra ngoài.\n'
           '• Nút Lưu không kiểm phiếu nhập / xuất kho còn treo (chỉ Lưu và kiểm kiểm).\n'
           '• Lỗi máy chủ → thông báo câu lỗi hoặc “Lưu thất bại.”, dữ liệu đã nhập giữ nguyên.',
       dacbiet='Các nút lưu khóa trong lúc đang lưu để một lần bấm không tạo 2 kế hoạch. Kế hoạch không có trường nhập duy nhất: '
               'mã tự sinh theo công ty người tạo + số thứ tự, không sửa được; 2 kế hoạch cùng kho cùng hàng vẫn lưu được. '
               'Lưu và Lưu và kiểm dùng chung một bộ điều kiện bắt buộc. Số tồn trên kế hoạch là ảnh chụp lúc thêm hàng.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'),
               shot_caption='Màn Tạo kế hoạch sau khi chọn kho, thêm hàng hóa và hội đồng'),
   extra=[(shot('10_create'), 'Màn Tạo kế hoạch lúc mới mở'),
          (shot('10b_validate_full'), 'Lỗi bắt buộc hiện cùng lúc khi bấm lưu thiếu dữ liệu'),
          (shot('10g_unsaved'), 'Hộp “Thông tin chưa lưu” khi rời màn')],
   ui=FORM_UI,
   ev=[
       ('Mở màn Tạo', 'System',
        'Before:\n– Không cần quyền riêng.\nDuring:\n– Nạp danh sách kho của công ty, nhân viên đang làm việc kèm chức vụ, người '
        'tạo, ngày hôm nay.\n– Lỗi → “Không tải được dữ liệu.”.\nAfter:\n– Hiển thị form trống, Hội đồng có 1 dòng trống; chưa '
        'tính là đã thay đổi.'),
       ('Chọn Kho', 'Change',
        'Before:\n– Bảng Hàng hóa trống (nếu đã có dòng → hỏi “Đổi kho”, mục 2.6).\n'
        'After:\n– Ghi nhận các kho đã chọn, xóa lỗi đỏ của ô Kho và bảng Hàng hóa.'),
       ('Chọn Thành viên', 'Change',
        'Before:\n– Nhân viên đang làm việc.\nAfter:\n– Tự điền Chức vụ đầu tiên của nhân viên; bỏ chọn → xóa Chức vụ.'),
       ('Bấm Thêm dòng / Xóa dòng hội đồng', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Thêm 1 dòng trống / bỏ dòng đó.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Không kiểm quyền riêng; khóa các nút lưu.\n' + SAVE_DURING + '\n'
        'After:\n– Lưu kế hoạch trạng thái Đang tạo, sinh số phiếu, lưu kho, hàng hóa, tồn kho kế toán, hội đồng.\n'
        '– Ghi một dòng lịch sử “Tạo mới”.\n– Hiển thị “Lưu thành công.”, về màn danh sách.'),
       ('Bấm Lưu và tiếp tục', 'Click',
        'Before:\n– Như Lưu.\nDuring:\n– Kiểm tra như Lưu.\n' + ERR + '\n'
        'After:\n– Lưu như Lưu (Đang tạo), ghi lịch sử “Tạo mới”, hiển thị “Lưu thành công.”, làm trắng form và ở lại màn Tạo.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu hiện tại với lúc mở màn.\nDuring:\n– Có thay đổi → hiện hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu; Ở lại: giữ nguyên form.'),
   ])

# ------------------------------------------------------------ 2.6 Thêm hàng hóa + Làm mới số liệu
fr(6, 'Thêm hàng hóa và Làm mới số liệu tồn', usecase=('FR-06', 'Thêm hàng hóa, Làm mới số liệu', 'crud', A_NV),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Chọn hàng cần kiểm và lấy tồn kho kế toán',
       mota='Trong khối Hàng hóa của màn Tạo / Sửa, người lập bấm Thêm hàng hóa để mở popup chọn hàng dùng chung: popup chỉ liệt kê '
            'hàng còn tồn kho kế toán trong các kho đã chọn. Hàng chọn xong được hệ thống lấy tồn theo từng kho kế toán (> 0) và '
            'đổ vào bảng. Nút Làm mới số liệu lấy lại tồn hiện tại của các hàng đã có trong bảng (cả ở màn Chi tiết, chỉ để xem).',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo hoặc Sửa kế hoạch (Làm mới số liệu: cả màn Chi tiết).\n'
                '3. Đã chọn ít nhất 1 Kho.',
       chinh='1. Người dùng bấm Thêm hàng hóa.\n'
             '2. Hệ thống mở popup “Thêm hàng hóa” khóa sẵn điều kiện còn tồn kho kế toán trong các kho đã chọn; hàng đã có trong '
             'bảng được đánh dấu.\n'
             '3. Người dùng tìm hàng (mã, tên, model, barcode, mã đặt hàng), lọc theo cây phân loại, tick nhiều hàng rồi bấm Thêm '
             '(n); hoặc bấm vào tên hàng để chọn nhanh 1 hàng.\n'
             '4. Hệ thống lấy tồn kho kế toán của các hàng vừa chọn trong các kho đã chọn: mỗi kho kế toán có tồn > 0 là 1 dòng, '
             'Tổng SL = cộng các dòng.\n'
             '5. Hệ thống thêm các hàng mới vào cuối bảng, báo “Thêm thành công.”.\n'
             '6. Bấm Làm mới số liệu → hệ thống lấy lại tồn kho kế toán của mọi hàng trong bảng (500 hàng / lần), ghi đè SL tồn '
             'từng kho kế toán + Tổng SL, bỏ hàng đã hết tồn, báo “Làm mới số liệu thành công.”.',
       phu='• Chưa chọn Kho mà bấm Thêm hàng hóa → lỗi đỏ “Kho – Vui lòng chọn kho.” dưới ô Kho, thông báo “Vui lòng chọn kho trước '
           'khi thêm hàng hóa.”, không mở popup.\n'
           '• Hàng vừa chọn đều đã có trong bảng → thông báo “Hàng hóa đã được chọn.”.\n'
           '• Hàng không còn tồn kho kế toán trong các kho đã chọn → không thêm, thông báo “Hàng hóa không còn tồn kho kế toán '
           'trong kho đã chọn: <mã hàng>.”.\n'
           '• Làm mới số liệu bỏ hàng hết tồn → “Làm mới số liệu thành công. Đã bỏ N hàng hóa hết tồn.” (N = số hàng bị bỏ).\n'
           '• Làm mới số liệu khi chưa chọn kho → “Vui lòng chọn kho trước khi làm mới số liệu.”.\n'
           '• Đổi Kho khi bảng Hàng hóa đã có dòng → hộp “Đổi kho”: Đổi kho = xóa hết hàng hóa; Hủy = trả ô về kho cũ.\n'
           '• Bấm Đóng / (x) popup → đóng, không thêm hàng.\n'
           '• Lỗi máy chủ → “Không tải được tồn kho kế toán của hàng hóa.” / “Làm mới số liệu thất bại.”.',
       dacbiet='Làm mới số liệu KHÔNG tự lưu: ở màn Tạo / Sửa phải bấm Lưu mới ghi; ở màn Chi tiết chỉ đổi số trên màn, rời màn '
               'không hỏi “chưa lưu”, tải lại trang về số đã lưu. Nút Thêm hàng hóa khóa trong lúc đang lấy tồn; Làm mới số liệu '
               'khóa khi bảng trống hoặc đang lấy.'),
   layout=dict(menu=MENU + ' => Tạo mới => Thêm hàng hóa', shot=shot('11_picker'),
               shot_caption='Popup Thêm hàng hóa (chỉ hàng còn tồn kho kế toán trong kho đã chọn)'),
   extra=[(shot('10e_doikho'), 'Hộp xác nhận “Đổi kho” khi bảng Hàng hóa đã có dòng'),
          (shot('10h_refresh'), 'Kết quả bấm Làm mới số liệu')],
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Thêm hàng hóa”; có nút phóng to toàn màn hình và (x).'),
       ('Ô tìm hàng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        '- Gợi ý “Tìm theo mã, tên hàng hoá, model, barcode, mã đặt hàng”.'),
       ('Cây phân loại', 'Table/Grid', 'Enable', '–', 'Không', 'Tất cả hàng đã xếp catalog',
        '- Bấm nhánh → chỉ hiện hàng thuộc nhánh; kèm số đếm.'),
       ('Ô Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Công ty người đăng nhập',
        '- Công ty dùng để tính số đếm của cây phân loại.'),
       ('Công tắc Còn tồn, Gồm hàng ngoài catalog', 'Checkbox', 'Enable', '–', 'Không', 'Theo popup',
        ['- Lọc thêm trong popup', '- Dù bật / tắt, popup luôn chỉ liệt kê hàng có tổng tồn kho kế toán > 0 trong các kho đã chọn ở form']),
       ('Bảng hàng hóa của popup', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu',
        ['- Cột: STT, Ảnh, Mã hàng, Tên hàng hoá, Model, Thương hiệu, Loại sản phẩm, ĐVT, Tồn bán được',
         '- Ô tick từng dòng; hàng đã có trong bảng được đánh dấu', '- Bấm tên hàng → chọn nhanh 1 hàng, đóng popup']),
       ('Dòng “Đã chọn n hàng hoá”', 'Label', 'Read-only', '–', '–', '0',
        ['- n = số hàng đang tick (giữ qua các trang)', '- Kèm liên kết “Bỏ chọn tất cả”']),
       ('Nút Thêm (n)', 'Button', 'Enable / Disable', '–', '–', 'Disable',
        ['- Bấm → thêm các hàng đã tick vào bảng', '- Khóa khi chưa tick hàng nào']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup, không thêm hàng.'),
       ('Nút Làm mới số liệu', 'Button', 'Enable / Disable', '–', '–', 'Disable khi bảng trống',
        ['- Bấm → lấy lại tồn kho kế toán của mọi hàng trong bảng', '- Có ở cả màn Tạo, Sửa, Chi tiết']),
       ('Bảng Hàng hóa sau khi thêm', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Mỗi kho kế toán có tồn > 0 là 1 dòng', '- Tổng SL = cộng SL tồn kho kế toán của hàng']),
       ('Hộp “Đổi kho”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Nội dung: “Đổi kho sẽ xóa danh sách hàng hóa đã chọn. Bạn có muốn tiếp tục?”',
         '- Nút Đổi kho: xóa hết hàng hóa, giữ kho mới', '- Nút Hủy / (x): trả ô Kho về kho cũ']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Thêm thành công.” / “Hàng hóa đã được chọn.”',
         '- “Hàng hóa không còn tồn kho kế toán trong kho đã chọn: <mã hàng>.”',
         '- “Làm mới số liệu thành công.” / “… Đã bỏ N hàng hóa hết tồn.”', '- “Vui lòng chọn kho trước khi thêm hàng hóa.”']),
   ],
   ev=[
       ('Bấm Thêm hàng hóa', 'Click',
        'Before:\n– Đã chọn Kho, nếu không → lỗi dưới ô Kho, “Vui lòng chọn kho trước khi thêm hàng hóa.”.\n'
        'After:\n– Mở popup, khóa điều kiện còn tồn kho kế toán trong các kho đã chọn.'),
       ('Bấm Thêm (n) / bấm tên hàng', 'Click',
        'Before:\n– Có ít nhất 1 hàng được chọn; bỏ hàng đã có trong bảng.\n'
        'During:\n– Lấy tồn kho kế toán theo kho kế toán (> 0) của các hàng trong các kho đã chọn.\n'
        '– Hàng không còn tồn → không thêm, báo “Hàng hóa không còn tồn kho kế toán trong kho đã chọn: <mã hàng>.”.\n' + ERR + '\n'
        'After:\n– Thêm hàng vào cuối bảng, báo “Thêm thành công.”; xóa lỗi đỏ của bảng.'),
       ('Bấm Làm mới số liệu', 'Click',
        'Before:\n– Bảng có hàng và đã chọn Kho, nếu không → “Vui lòng chọn kho trước khi làm mới số liệu.”.\n'
        'During:\n– Lấy lại tồn của các hàng trong bảng, 500 hàng / lần.\n– Lỗi → “Làm mới số liệu thất bại.”.\n'
        'After:\n– Ghi đè SL tồn từng kho kế toán + Tổng SL, bỏ hàng hết tồn; không lưu (Chi tiết: không tính là chưa lưu).'),
       ('Đổi Kho khi đã có hàng', 'Change',
        'Before:\n– Bảng Hàng hóa có dòng.\nDuring:\n– Hiện hộp “Đổi kho”.\n'
        'After:\n– Đổi kho: giữ kho mới, xóa hết hàng; Hủy: trả ô về kho cũ.'),
       ('Bấm Xóa dòng hàng', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Bỏ hàng khỏi bảng, xóa lỗi của dòng đó.'),
       ('Bấm Đóng / (x) popup', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng popup, bảng giữ nguyên.'),
   ])

# ------------------------------------------------------------ 2.7 Lưu và kiểm
PENDING = '“Còn phiếu nhập kho / xuất kho chưa xử lý xong của hàng hóa trong kế hoạch. Vui lòng xử lý xong các phiếu dưới đây trước khi lưu và kiểm.”'
fr(7, 'Lưu và kiểm (chuyển kế hoạch sang Đang kiểm)', usecase=('FR-07', 'Lưu và kiểm', 'action', A_NV),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lưu và kiểm (chuyển trạng thái Đang kiểm)',
       mota='Ở màn Tạo hoặc Sửa, nút Lưu và kiểm lưu kế hoạch và chuyển thẳng sang trạng thái Đang kiểm: kế hoạch hiện với người có '
            'quyền xem, người có quyền Lập phiếu kiểm kê kho theo hàng hóa cùng công ty nhận thông báo để lập phiếu kiểm kê. Trước '
            'khi lưu, hệ thống chặn nếu các kho đã chọn còn phiếu nhập / xuất kho chưa xử lý xong có hàng của kế hoạch. Không có '
            'hộp xác nhận (giữ như hệ thống cũ).',
       tacnhan=TN + ' Sửa rồi kiểm: chỉ người tạo khi phiếu Đang tạo.',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo, hoặc màn Sửa của kế hoạch Đang tạo do mình tạo.\n'
                '3. Đủ dữ liệu bắt buộc như mục 2.5.',
       chinh='1. Người dùng nhập đủ thông tin (như mục 2.5) và bấm Lưu và kiểm.\n'
             '2. Hệ thống kiểm tra dữ liệu như nút Lưu.\n'
             '3. Hệ thống tìm phiếu nhập kho / xuất kho của các kho đã chọn có chứa bất kỳ hàng nào của kế hoạch mà chưa xử lý xong; '
             'không có phiếu nào mới lưu tiếp.\n'
             '4. Hệ thống lưu kế hoạch với trạng thái Đang kiểm (màn Tạo: sinh số phiếu; màn Sửa: kiểm lại phiếu còn Đang tạo và '
             'đúng người tạo).\n'
             '5. Hệ thống ghi nhận hành động trong lịch sử của phiếu: màn Tạo “Tạo mới”; màn Sửa “Thay đổi thông tin” (nếu đổi '
             'dữ liệu) và “Thay đổi trạng thái” Đang tạo → Đang kiểm.\n'
             '6. Hệ thống gửi thông báo “[KHKKHH] Tạo mới: <số phiếu>” (ghi chú: Người lập, “Chờ lập phiếu kiểm kê”, Ngày kiểm kê, '
             'Kho, Ghi chú) cho nhân viên có quyền ' + Q1 + ' cùng công ty người lưu; bấm thông báo mở chi tiết kế hoạch.\n'
             '7. Hệ thống hiển thị “Lưu và kiểm thành công.” và chuyển về màn danh sách.',
       phu='• Thiếu dữ liệu → như mục 2.5, không lưu, không gửi.\n'
           '• Còn phiếu chưa xử lý xong → popup “Cảnh báo phiếu chưa xử lý xong” liệt kê Loại phiếu + Số phiếu, KHÔNG lưu, không '
           'hiện thông báo lỗi khác; người dùng xử lý xong phiếu (hoặc bỏ hàng khỏi kế hoạch) rồi bấm lại.\n'
           '• Phiếu đã bị đổi trạng thái / không còn là người tạo (sửa ở tab khác) → ' + CONFLICT + ', không lưu.\n'
           '• Người lưu không có công ty / không ai có quyền → vẫn lưu thành công, không ai nhận thông báo.\n'
           '• Gửi thông báo lỗi → không ảnh hưởng việc lưu.',
       dacbiet='Không có hộp xác nhận; nút khóa trong lúc lưu. Sau khi chuyển Đang kiểm kế hoạch không sửa / xóa được nữa. Phiếu '
               'chưa xử lý xong = phiếu nhập / xuất kho chưa hoàn tất, hoặc phiếu nhập / xuất hàng gắn kèm chưa hoàn tất; xét mọi '
               'hàng của kế hoạch. Liên kết Phiếu nhập kho mở màn chi tiết ở tab mới; Phiếu xuất kho mở hệ thống ERP ở tab mới.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới => Lưu và kiểm', 'Chuyển Đang kiểm ngay khi tạo kế hoạch.'),
       (MENU + ' => Sửa => Lưu và kiểm', 'Chuyển Đang kiểm kế hoạch Đang tạo đã lưu trước đó.')],
       shot=shot('10f_pending'), shot_caption='Popup “Cảnh báo phiếu chưa xử lý xong” khi Lưu và kiểm bị chặn'),
   ui=[
       ('Nút Lưu và kiểm', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Màu chính, biểu tượng máy bay giấy', '- Rê chuột: “Lưu và chuyển kế hoạch sang trạng thái Đang kiểm”',
         '- Khóa trong lúc lưu']),
       ('Các trường của form', 'Table/Grid', 'Enable', '–', 'Như mục 2.5', 'Như mục 2.5',
        '- Kho, Ghi chú, Hàng hóa, Hội đồng — cùng điều kiện bắt buộc với nút Lưu.'),
       ('Tiêu đề popup cảnh báo', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- “Cảnh báo phiếu chưa xử lý xong”, biểu tượng chấm than vàng.'),
       ('Nội dung popup cảnh báo', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- ' + PENDING),
       ('Bảng phiếu chưa xử lý xong', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Cột: STT, Loại phiếu (Phiếu nhập kho / Phiếu xuất kho), Số phiếu', '- Phiếu nhập kho trước, phiếu xuất kho sau']),
       ('Liên kết Số phiếu', 'Link', 'Enable', '–', '–', 'Hiển thị',
        ['- Phiếu nhập kho: bấm → mở chi tiết phiếu nhập kho ở tab mới', '- Phiếu xuất kho: bấm → mở phiếu trên hệ thống ERP ở tab mới']),
       ('Nút Đóng popup', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup, form giữ nguyên dữ liệu, chưa lưu.'),
       ('Trạng thái sau khi lưu', 'Badge', 'Read-only', '–', '–', 'Đang kiểm', '- Nhãn vàng “Đang kiểm” ở danh sách.'),
       ('Thông báo cho người lập phiếu kiểm kê', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tiêu đề “[KHKKHH] Tạo mới: <số phiếu>”',
         '- Ghi chú: Người lập, “Chờ lập phiếu kiểm kê”, Ngày kiểm kê, Kho (tối đa 3 tên + “và N kho khác”), Ghi chú (nếu có)',
         '- Bấm → mở màn chi tiết kế hoạch']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Lưu và kiểm thành công.”', '- Thiếu: “Bạn chưa nhập đầy đủ thông tin.”', '- Xung đột: ' + CONFLICT]),
   ],
   ev=[
       ('Bấm Lưu và kiểm', 'Click',
        'Before:\n– Không kiểm quyền riêng; màn Sửa: phiếu phải Đang tạo và người bấm là người tạo, nếu không → ' + CONFLICT + '.\n'
        + SAVE_DURING + '\n'
        '– Còn phiếu nhập / xuất kho chưa xử lý xong → mở popup “Cảnh báo phiếu chưa xử lý xong”, không lưu.\n'
        'After:\n– Lưu kế hoạch trạng thái Đang kiểm (tạo mới: sinh số phiếu).\n'
        '– Ghi lịch sử: “Tạo mới” (màn Tạo) hoặc “Thay đổi thông tin” + “Thay đổi trạng thái” Đang tạo → Đang kiểm (màn Sửa).\n'
        '– Gửi thông báo cho nhân viên cùng công ty có quyền ' + Q1 + '.\n'
        '– Hiển thị “Lưu và kiểm thành công.”, về màn danh sách.'),
       ('Bấm Số phiếu trong popup cảnh báo', 'Click',
        'Before:\n– Popup đang mở.\nAfter:\n– Mở phiếu nhập kho (tab mới) hoặc phiếu xuất kho trên ERP (tab mới); form giữ nguyên.'),
       ('Bấm Đóng / (x) popup cảnh báo', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng popup; kế hoạch chưa được lưu.'),
       ('Bấm thông báo (người lập phiếu kiểm kê)', 'Click',
        'Before:\n– Người nhận có quyền ' + Q1 + '.\nAfter:\n– Mở màn chi tiết kế hoạch; thấy nút Lập phiếu kiểm kê theo hàng hóa (mục 2.11).'),
   ])

# ------------------------------------------------------------ 2.8 Sửa
fr(8, 'Chỉnh sửa kế hoạch', usecase=('FR-08', 'Chỉnh sửa kế hoạch', 'crud', A_NV),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Chỉnh sửa kế hoạch kiểm kê theo hàng hóa',
       mota='Người tạo sửa kế hoạch còn Đang tạo: đổi kho, thêm / bỏ hàng, làm mới số liệu tồn, sửa ghi chú và hội đồng; lưu giữ '
            'Đang tạo (Lưu) hoặc chuyển luôn Đang kiểm (Lưu và kiểm, mục 2.7). Số phiếu không sửa được; Ngày kiểm kê được hệ thống '
            'ghi lại bằng ngày lưu.',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo kế hoạch.\n3. Kế hoạch đang ở trạng thái Đang tạo.',
       chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
             '2. Hệ thống mở màn “Sửa kế hoạch kiểm kê theo hàng hóa: <số phiếu>”, điền sẵn kho (kể cả kho đã khóa / khác công '
             'ty vẫn hiện đúng tên), ghi chú, bảng Hàng hóa đã lưu, hội đồng (nhân viên đã nghỉ / chức vụ cũ vẫn hiện tên).\n'
             '3. Người dùng sửa thông tin, thêm / bỏ hàng, bấm Làm mới số liệu nếu cần.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống kiểm lại phiếu còn Đang tạo và đúng người tạo, kiểm tra dữ liệu như mục 2.5.\n'
             '6. Hệ thống ghi đè kho, hàng hóa, hội đồng; Ngày kiểm kê = ngày lưu; cập nhật người / ngày cập nhật.\n'
             '7. Hệ thống ghi nhận hành động “Thay đổi thông tin” trong lịch sử (giá trị cũ → mới của Kho, Ghi chú, Danh sách hàng '
             'hóa, Danh sách thành viên hội đồng kiểm kê) — không đổi gì thì không ghi.\n'
             '8. Hệ thống hiển thị “Lưu thành công.” và chuyển về màn danh sách.',
       phu='• Mở màn Sửa của kế hoạch không còn Đang tạo / không phải người tạo → tự chuyển sang màn chi tiết.\n'
           '• Kế hoạch ngoài phạm vi / đã bị xóa → trang “Không tìm thấy trang”.\n'
           '• Lưu khi phiếu vừa bị chuyển Đang kiểm / xóa ở tab khác → ' + CONFLICT + ' hoặc ' + NOTFOUND + '.\n'
           '• Thiếu dữ liệu → như mục 2.5.\n'
           '• Quay lại khi đã sửa → hộp “Thông tin chưa lưu”; không sửa gì → về danh sách ngay.\n'
           '• Hai người không thể cùng sửa: chỉ người tạo được sửa.',
       dacbiet='Kế hoạch không có trường duy nhất nên không có kiểm tra trùng. Số tồn chỉ đổi khi thêm hàng mới hoặc bấm Làm mới số '
               'liệu rồi lưu. Màn Sửa không có nút Lưu và tiếp tục.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('12_edit'), shot_caption='Màn Sửa kế hoạch kiểm kê theo hàng hóa'),
   ui=FORM_UI[:16] + FORM_UI[17:],
   ev=[
       ('Mở màn Sửa', 'System',
        'Before:\n– Kiểm tra phạm vi xem, nếu ngoài phạm vi → trang “Không tìm thấy trang”.\n'
        '– Kiểm tra người tạo + Đang tạo, nếu không → chuyển sang màn chi tiết.\n'
        'After:\n– Điền sẵn dữ liệu; chưa tính là đã thay đổi.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Kiểm lại phiếu còn Đang tạo và người bấm là người tạo, nếu không → ' + CONFLICT + '.\n' + SAVE_DURING + '\n'
        'After:\n– Ghi đè kho, hàng hóa, hội đồng; Ngày kiểm kê = ngày lưu; cập nhật người / ngày cập nhật.\n'
        '– Ghi một dòng lịch sử “Thay đổi thông tin” (cũ → mới) nếu có thay đổi.\n'
        '– Hiển thị “Lưu thành công.”, về màn danh sách.'),
       ('Bấm Lưu và kiểm', 'Click', 'Before:\n– Như Lưu.\nDuring:\n– Như mục 2.7.\nAfter:\n– Như mục 2.7.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu với lúc mở.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu, không ghi lịch sử; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.9 Xóa
fr(9, 'Xóa kế hoạch', usecase=('FR-09', 'Xóa kế hoạch', 'action', A_NV),
   rule=('- Hộp thoại xác nhận Xóa và Thông báo.', 'delete'),
   intro=dict(
       ten='Xóa kế hoạch kiểm kê theo hàng hóa',
       mota='Người tạo xóa hẳn kế hoạch còn Đang tạo cùng toàn bộ dữ liệu con (kho, hàng hóa, tồn kho kế toán, hội đồng). Kế hoạch '
            'đã chuyển Đang kiểm trở đi không xóa được.',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo.\n3. Kế hoạch đang Đang tạo.',
       chinh='1. Người dùng bấm Xóa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa” với nội dung “Bạn có chắc muốn xóa bản ghi này không?”.\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm lại phiếu còn Đang tạo và đúng người tạo.\n'
             '5. Hệ thống ghi nhận hành động “Xóa” trong lịch sử, rồi xóa kế hoạch và mọi dữ liệu con.\n'
             '6. Hệ thống hiển thị “Xóa thành công.”; ở danh sách nạp lại, ở màn chi tiết quay về danh sách.',
       phu='• Bấm Hủy / (x) → đóng hộp, không xóa.\n'
           '• Phiếu vừa chuyển Đang kiểm / không còn là người tạo → ' + CONFLICT + ', không xóa.\n'
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

# ------------------------------------------------------------ 2.10 Chi tiết
fr(10, 'Xem chi tiết kế hoạch',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết kế hoạch kiểm kê theo hàng hóa',
       mota='Màn chỉ đọc hiển thị thông tin chung (Ngày kiểm kê, Kho, Ghi chú), bảng Hàng hóa kèm tồn kho kế toán, hội đồng và khối '
            'Lịch sử. Chân màn có nút theo cờ: Sửa / Xóa (Đang tạo, người tạo), Lập phiếu kiểm kê theo hàng hóa (Đang kiểm, có Q1), '
            'In, Xuất Excel, Quay lại; khối Hàng hóa có nút Làm mới số liệu (chỉ để xem).',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Kế hoạch trong phạm vi xem (hoặc là kế hoạch Đang kiểm và người dùng có '
                'quyền Q1).',
       chinh='1. Người dùng bấm Số phiếu ở danh sách (hoặc bấm thông báo).\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết kế hoạch kiểm kê theo hàng hóa: <số phiếu>”.\n'
             '4. Hệ thống hiển thị Thông tin chung, Hàng hóa, Hội đồng kiểm kê, khối Lịch sử (thu gọn).',
       phu='• Ngoài phạm vi / không tồn tại → trang “Không tìm thấy trang”.\n'
           '• Kế hoạch Đang tạo của người khác → coi như ngoài phạm vi.\n'
           '• Bấm Làm mới số liệu → chỉ đổi số trên màn, không lưu; tải lại trang về số đã lưu.\n'
           '• Bấm Quay lại → về danh sách, khôi phục bộ lọc (trong 10 phút).',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết kế hoạch kiểm kê theo hàng hóa'),
   extra=[(shot('15_send_detail'), 'Màn chi tiết kế hoạch Đang kiểm — có nút Lập phiếu kiểm kê theo hàng hóa')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Chi tiết kế hoạch kiểm kê theo hàng hóa: <số phiếu>”', '- Không kèm nhãn trạng thái']),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Ngày kiểm kê', 'Textbox', 'Disable', 'dd/mm/yyyy', 'Theo dữ liệu', ['- Ô khóa, có dấu *', '- Ngày lưu gần nhất']),
       ('Kho', 'Textbox', 'Disable', '–', 'Theo dữ liệu', ['- Ô khóa, có dấu *', '- Tên các kho nối dấu phẩy']),
       ('Ghi chú', 'Textarea', 'Disable', '–', 'Theo dữ liệu', '- Ô khóa; trống thì để trống.'),
       ('Bảng Hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột: STT, Tên hàng, Model, Mã hàng, ĐVT, Kho kế toán, SL tồn kho kế toán, Tổng SL (không có cột Hành động)',
         '- Số dạng 1,234.5; không có nút Thêm hàng hóa']),
       ('Nút Làm mới số liệu', 'Button', 'Enable / Disable', '–', 'Hiển thị', '- Lấy lại tồn hiện tại để xem, không lưu (mục 2.6).'),
       ('Bảng Hội đồng kiểm kê', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- STT, Thành viên, Chức vụ (ô khóa).'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
        ['- Nút Xem lịch sử / Thu gọn, Làm mới, Bộ lọc', '- Nội dung như mục 2.14']),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Phiếu Đang tạo của mình → mở màn Sửa.'),
       ('Nút Lập phiếu kiểm kê theo hàng hóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
        '- Đang kiểm + có Q1 (mục 2.11).'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Cửa sổ Xem trước (mục 2.12).'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', '- Tải file Excel kế hoạch (mục 2.13).'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Phiếu Đang tạo của mình (mục 2.9).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn danh sách.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → trang “Không tìm thấy trang”.\n'
        'During:\n– Lấy dữ liệu kế hoạch, cờ nút.\nAfter:\n– Hiển thị màn chỉ đọc, nút theo cờ.'),
       ('Bấm Xem lịch sử', 'Click', 'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở rộng khối, hiện các mốc.'),
       ('Bấm Làm mới số liệu', 'Click', 'Before:\n– Bảng có hàng.\nAfter:\n– Đổi số trên màn, không lưu, không hỏi “chưa lưu” khi rời.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Không có dữ liệu cần lưu.\nAfter:\n– Về danh sách, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.11 Lập phiếu kiểm kê
fr(11, 'Lập phiếu kiểm kê theo hàng hóa từ kế hoạch', usecase=('FR-11', 'Lập phiếu kiểm kê', 'action', A_TK),
   rule=('- Màn Danh sách và Phân quyền.', 'list'),
   intro=dict(
       ten='Lập phiếu kiểm kê theo hàng hóa từ kế hoạch Đang kiểm',
       mota='Người có quyền Lập phiếu kiểm kê kho theo hàng hóa bấm nút ở kế hoạch Đang kiểm để mở màn Tạo phiếu kiểm kê theo hàng '
            'hóa (phân hệ Kho) đã nạp sẵn kế hoạch. Khi phiếu kiểm kê được lưu, kế hoạch chuyển Đã lập phiếu kiểm kê (màn Kiểm kê '
            'theo hàng hóa thực hiện).',
       tacnhan='Người dùng có quyền thực hiện chức năng: ' + Q1 + '; Super admin.',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Kế hoạch đang Đang kiểm.\n3. Người dùng có quyền ' + Q1 + ' (hoặc Super admin).',
       chinh='1. Người dùng bấm Lập phiếu kiểm kê theo hàng hóa ở cột Hành động hoặc chân màn chi tiết.\n'
             '2. Hệ thống mở màn Tạo phiếu kiểm kê theo hàng hóa (cùng tab) với kế hoạch đã chọn sẵn: kho, hàng hóa, hội đồng; '
             'không cho thêm / bớt hàng.\n'
             '3. Người dùng lưu phiếu kiểm kê ở màn đó; hệ thống kiểm lại kế hoạch còn Đang kiểm và người lưu có quyền, đổi kế hoạch '
             'sang Đã lập phiếu kiểm kê và ghi “Thay đổi trạng thái” Đang kiểm → Đã lập phiếu kiểm kê (ghi chú “Lập phiếu kiểm kê '
             '<mã phiếu>.”) vào lịch sử kế hoạch.',
       phu='• Kế hoạch không còn Đang kiểm khi lưu phiếu kiểm kê → màn kia báo ' + CONFLICT + '.\n'
           '• Người lưu thiếu quyền → “Bạn không có quyền thực hiện chức năng này.”.\n'
           '• Xóa phiếu kiểm kê sau đó KHÔNG trả kế hoạch về Đang kiểm.\n'
           '• Không đủ điều kiện → nút không hiện.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Lập phiếu kiểm kê theo hàng hóa', shot=shot('15_send_detail'),
               shot_caption='Nút Lập phiếu kiểm kê theo hàng hóa ở màn chi tiết kế hoạch Đang kiểm'),
   ui_kw=dict(required=False),
   ui=[
       ('Nút Lập phiếu kiểm kê trên dòng', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
        ['- Biểu tượng tài liệu có dấu cộng', '- Rê chuột: “Lập phiếu kiểm kê theo hàng hóa”']),
       ('Nút Lập phiếu kiểm kê ở chi tiết', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện',
        '- Rê chuột: “Lập phiếu kiểm kê theo hàng hóa từ kế hoạch này”.'),
       ('Nhãn trạng thái kế hoạch', 'Badge', 'Read-only', 'Danh sách 4 giá trị', 'Theo dữ liệu',
        ['- Đang kiểm → Đã lập phiếu kiểm kê khi lưu phiếu kiểm kê', '- Không có luồng trả về Đang kiểm']),
   ],
   ev=[
       ('Bấm Lập phiếu kiểm kê theo hàng hóa', 'Click',
        'Before:\n– Nút chỉ hiện khi Đang kiểm + có quyền ' + Q1 + '.\n'
        'After:\n– Mở màn Tạo phiếu kiểm kê theo hàng hóa, nạp sẵn kế hoạch.'),
       ('Màn Kiểm kê theo hàng hóa lưu phiếu', 'System',
        'Before:\n– Phiếu kiểm kê gắn với kế hoạch; kế hoạch còn Đang kiểm.\n'
        'After:\n– Đổi trạng thái kế hoạch sang Đã lập phiếu kiểm kê, cập nhật người / ngày cập nhật, ghi “Thay đổi trạng thái” '
        'vào lịch sử kế hoạch.'),
   ])

# ------------------------------------------------------------ 2.12 In
fr(12, 'In phiếu và in danh sách', usecase=('FR-12', 'In phiếu / In danh sách', 'io', A_NV),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In kế hoạch / In danh sách kế hoạch',
       mota='Xem trước và in một kế hoạch (mẫu in “Kế hoạch kiểm kê theo mặt hàng”: số phiếu, ngày kiểm kê, kho, ghi chú, hội đồng, '
            'bảng hàng hóa, chỗ ký Người lập) hoặc in danh sách theo bộ lọc đang áp. Bản in mở trong cửa sổ trên màn đang đứng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm In ở cột Hành động / màn chi tiết (in phiếu), hoặc In danh sách trên bảng.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ xem trước, hiện “Đang tải dữ liệu in…” trong lúc dựng.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Danh sách quá 2.000 dòng → không dựng bản in, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc.\n'
           '• Không có dòng nào → “Không có dữ liệu để in”.\n'
           '• Ngoài phạm vi → ' + NOTFOUND + '.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in kế hoạch kiểm kê theo hàng hóa.” / “Thiếu mẫu in danh sách kế hoạch kiểm kê theo hàng '
           'hóa.”.\n'
           '• Bấm (x) → đóng cửa sổ.',
       dacbiet='Logo / tên công ty đầu bản in phiếu lấy theo công ty ghi trên kế hoạch; bản in danh sách theo công ty người in. '
               'Ngày ở khối ký là ngày in; Người lập của bản in phiếu là người tạo kế hoạch, của bản in danh sách là người in.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước kế hoạch',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   extra=[(shot('19_printlist'), 'Cửa sổ Xem trước danh sách kế hoạch')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–',
        ['- In phiếu: “Xem trước kế hoạch kiểm kê theo hàng hóa <số phiếu>”',
         '- In danh sách: “Xem trước danh sách kế hoạch kiểm kê theo hàng hóa”']),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', ['- Cạnh tiêu đề; bấm → hộp thoại in', '- Ẩn khi vượt 2.000 dòng']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Đang tải dữ liệu in…”.'),
       ('Đầu bản in phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Logo, tên công ty của kế hoạch', '- “KẾ HOẠCH KIỂM KÊ THEO MẶT HÀNG”, Số phiếu, Ngày kiểm kê',
         '- Kho, Ghi chú, Hội đồng kiểm kê (tên nối “; ”)']),
       ('Bảng chi tiết bản in phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Tên hàng, Mã hàng, ĐVT, Kho kế toán, SL tồn, Tổng SL', '- Gộp ô theo hàng; số dạng 1,234']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- “Ngày … Tháng … Năm …”, Người lập (tên người tạo kế hoạch), sát lề phải.'),
       ('Bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        ['- Tiêu đề danh sách kế hoạch kiểm kê theo hàng hóa', '- Cột: STT, Số phiếu, Ngày kiểm kê, Kho, Người tạo, Trạng thái',
         '- Khối ký bên phải: Ngày … Tháng … Năm …, Người lập (người in)']),
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
             '5. Hệ thống tải file “danh_sach_ke_hoach_kiem_ke_theo_hang_hoa.xlsx”, báo “Xuất Excel thành công.”.\n'
             '6. Xuất 1 kế hoạch: bấm Xuất Excel trên dòng / chi tiết → tải “ke_hoach_kiem_ke_theo_mat_hang_<số phiếu>.xlsx” '
             '(dấu chấm trong số phiếu đổi thành “-”).',
       phu='• Không có kế hoạch khớp → vẫn ra file có tiêu đề, dòng tên cột và khối ký.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi → “Lỗi khi xuất Excel.”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng; nút Xuất Excel khóa trong lúc đang xuất. Ngày giữ dạng chữ dd/mm/yyyy hh:mm. File 1 kế hoạch '
               'giữ số lượng là ô số có dấu phân cách hàng nghìn.'),
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
        ['- Letterhead công ty, tiêu đề “DANH SÁCH KẾ HOẠCH KIỂM KÊ THEO HÀNG HÓA”', '- Dòng “Từ ngày … đến ngày …” khi lọc Ngày kiểm kê',
         '- Cột STT + trường đã chọn; khối ký cuối file; trang tính “Kế hoạch kiểm kê”']),
       ('File 1 kế hoạch', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Tên “ke_hoach_kiem_ke_theo_mat_hang_<số phiếu>.xlsx”',
         '- Letterhead công ty của kế hoạch, “KẾ HOẠCH KIỂM KÊ THEO MẶT HÀNG”, Số phiếu, Ngày kiểm kê, Kho vật lý, Hội đồng kiểm kê, Ghi chú',
         '- Bảng 7 cột như bản in; “Nhận xét, đánh giá:”; khối ký Hội đồng kiểm kê / Trưởng bộ phận kho']),
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
            'Kiểm kê theo hàng hóa đổi, kèm ghi chú mã phiếu kiểm kê), Xóa. Cửa sổ ở danh sách và khối Lịch sử ở màn chi tiết dùng '
            'chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động (hoặc trong menu Hành động khác), hoặc Xem lịch sử ở màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ “Lịch sử thay đổi: <số phiếu>” và hiển thị các mốc, mới nhất ở trên.',
       phu='• Kế hoạch từ hệ thống cũ chưa có mốc → “Chưa có lịch sử thao tác nào.”.\n'
           '• Bấm Bộ lọc → các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Lịch sử ghi Kho, Ghi chú, Danh sách hàng hóa (mỗi hàng × kho kế toán: Mã hàng, Kho kế toán, SL tồn), Danh sách thành '
               'viên hội đồng kiểm kê (Chức vụ). Xem, in, xuất Excel, Làm mới số liệu không ghi mốc.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('16b_history_empty'), 'Kế hoạch chưa có lịch sử')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <số phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái: “Trạng thái: <cũ> → <mới>” kèm ghi chú (vd “Lập phiếu kiểm kê <mã phiếu kiểm kê>.”)',
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
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Kế hoạch kiểm kê theo hàng hóa; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Kế hoạch không ghi tồn', [
        '– Lưu / Lưu và kiểm / sửa / xóa kế hoạch không đổi tồn kho, không sinh phiếu nhập / xuất.',
        '– Số tồn trên kế hoạch là ảnh chụp lúc thêm hàng; muốn cập nhật phải bấm Làm mới số liệu rồi Lưu (chỉ khi còn Đang tạo).'],
     ['Tạo', 'Chỉnh sửa', 'Thêm hàng hóa']),
    ('BR-02', 'Phạm vi xem', [
        '– V1 (hoặc Super admin): mọi kế hoạch; V2: công ty mình + của mình (công ty trống → chỉ của mình); không quyền: của mình.',
        '– Kế hoạch Đang tạo chỉ người tạo thấy.',
        '– Người có quyền Lập phiếu kiểm kê kho theo hàng hóa xem được chi tiết mọi kế hoạch Đang kiểm.',
        '– Ngoài phạm vi: chi tiết / in / xuất / lịch sử đều bị từ chối.'], ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất', 'Lịch sử']),
    ('BR-03', 'Dữ liệu bắt buộc khi lưu', [
        '– Lưu và Lưu và kiểm cùng điều kiện: ≥ 1 kho (không trùng), ≥ 1 hàng hóa có ít nhất 1 dòng kho kế toán, ≥ 1 thành viên '
        'hội đồng có thành viên + chức vụ, thành viên không trùng; Ghi chú ≤ 255 ký tự.',
        '– Hàng, kho kế toán phải còn tồn tại; SL tồn kho kế toán và Tổng SL ≥ 0.'], ['Tạo', 'Chỉnh sửa', 'Lưu và kiểm']),
    ('BR-04', 'Điều kiện sửa / xóa', [
        '– Chỉ người tạo, chỉ khi Đang tạo; máy chủ kiểm lại lúc lưu / xóa, sai → báo trạng thái đã thay đổi.',
        '– Xóa là xóa hẳn kế hoạch và dữ liệu con; kế hoạch đã Đang kiểm không xóa được nên không có ràng buộc phiếu kiểm kê.'],
     ['Chỉnh sửa', 'Xóa']),
    ('BR-05', 'Vòng đời trạng thái', [
        '– Lưu → Đang tạo; Lưu và kiểm → Đang kiểm (không hỏi xác nhận).',
        '– Lưu phiếu kiểm kê theo hàng hóa từ kế hoạch → Đã lập phiếu kiểm kê; xóa phiếu kiểm kê không trả kế hoạch về.',
        '– Hoàn thành chỉ còn ở dữ liệu cũ; không có Duyệt / Không duyệt / Hủy / Khóa trên màn này.'], ['Lưu và kiểm', 'Lập phiếu kiểm kê']),
    ('BR-06', 'Tính duy nhất', [
        '– Không có trường nhập duy nhất; mã <mã công ty>.KHKKHH-NNNNN tự sinh (công ty người tạo + số thứ tự), không sửa được.',
        '– Hai kế hoạch cùng kho, cùng hàng vẫn được lưu; trong một kế hoạch mỗi hàng chỉ 1 lần.',
        '– Nút lưu khóa trong lúc lưu chống tạo trùng.'], ['Tạo']),
    ('BR-07', 'Chuẩn hóa dữ liệu nhập', [
        '– Ngày kiểm kê = ngày lưu, không nhập tay (sửa lại cũng ghi ngày lưu mới).',
        '– Công ty / phòng ban của kế hoạch = của người tạo.',
        '– Tên, mã, model, ĐVT (đơn vị cơ sở) của hàng chụp từ danh mục lúc lưu; tên chức vụ chụp lúc lưu.',
        '– Chọn thành viên tự điền chức vụ đầu tiên; kho chỉ gồm kho đang hoạt động có kho kế toán thuộc công ty người đăng nhập.'],
     ['Tạo', 'Chỉnh sửa']),
    ('BR-08', 'Liên kết cấp cha – con', [
        '– Kế hoạch > kho; kế hoạch > hàng hóa (Tổng SL) > kho kế toán (SL tồn kho kế toán > 0); Tổng SL = cộng các dòng kho kế toán.',
        '– Đổi kho khi đã có hàng → xóa hết hàng (hỏi xác nhận).'], ['Tạo', 'Chỉnh sửa', 'Thêm hàng hóa']),
    ('BR-09', 'Chặn Lưu và kiểm khi còn phiếu treo', [
        '– Lưu và kiểm bị chặn khi các kho đã chọn có phiếu nhập kho / xuất kho chứa bất kỳ hàng nào của kế hoạch mà phiếu chưa '
        'hoàn tất, hoặc phiếu nhập / xuất hàng gắn kèm chưa hoàn tất; popup liệt kê các phiếu đó.',
        '– Nút Lưu (Đang tạo) không kiểm điều kiện này.'], ['Lưu và kiểm']),
    ('BR-10', 'Thông báo', [
        '– Lưu với trạng thái Đang kiểm (tạo hoặc sửa) → gửi “[KHKKHH] Tạo mới: <số phiếu>” cho nhân viên có quyền Lập phiếu kiểm '
        'kê kho theo hàng hóa cùng công ty người lưu; người lưu không có công ty → không gửi; lỗi gửi không làm hỏng việc lưu.'],
     ['Lưu và kiểm']),
    ('BR-11', 'In và xuất', [
        '– Letterhead bản in / file 1 kế hoạch theo công ty ghi trên kế hoạch; bản in danh sách theo công ty người in.',
        '– In danh sách tối đa 2.000 dòng; Xuất Excel danh sách không giới hạn, rỗng vẫn ra file.'], ['In', 'Xuất Excel']),
    ('BR-12', 'Sử dụng ở màn khác', [
        '– Kho vật lý đã có trong kế hoạch không xóa được ở danh mục Kho vật lý.',
        '– Màn Kiểm kê theo hàng hóa chỉ chọn kế hoạch Đang kiểm; phiếu lập từ kế hoạch không cho thêm / bớt hàng.'],
     ['Tạo', 'Lưu và kiểm', 'Lập phiếu kiểm kê']),
    ('BR-13', 'Quy tắc ghi lịch sử', [
        '– Ghi: Tạo mới; Thay đổi thông tin (Kho, Ghi chú, Danh sách hàng hóa, Danh sách thành viên hội đồng kiểm kê — cũ → mới, '
        'không đổi thì không ghi); Thay đổi trạng thái (kèm ghi chú mã phiếu khi màn khác đổi); Xóa.',
        '– Xem / in / xuất / Làm mới số liệu không ghi; hiển thị mới nhất ở trên.'], ['Tạo', 'Chỉnh sửa', 'Xóa', 'Lịch sử']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Kế hoạch kiểm kê theo hàng hóa (trạng thái, kho, hàng hóa – tồn kho kế '
    'toán, hội đồng).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Kiểm kê theo hàng hóa (popup Chọn kế hoạch chỉ hiện kế hoạch Đang kiểm; nạp sẵn kho, hàng hóa, hội đồng, khóa '
                 'thêm / bớt hàng; lưu phiếu kiểm kê → kế hoạch Đã lập phiếu kiểm kê + mốc lịch sử; chi tiết phiếu có liên kết mở '
                 'kế hoạch)', 'Kho -> Kiểm kho -> Theo vị trí'),
    ('2', 'Tài chính', 'Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả (cùng màn Kiểm kê theo hàng hóa, lối vào lọc phiếu chờ duyệt '
                       'kết quả; số kế hoạch trên phiếu là liên kết mở kế hoạch)', 'Tài chính -> Kiểm kê'),
    ('3', 'Kho', 'Kho vật lý (không xóa được kho đã có trong kế hoạch)', 'Kho -> Danh mục'),
    ('4', 'Hệ thống ERP', 'Phiếu kiểm kê theo hàng hóa trên hệ thống cũ (lập phiếu từ kế hoạch Đang kiểm → kế hoạch Đã lập phiếu '
                          'kiểm kê)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
