# -*- coding: utf-8 -*-
"""SRS màn "Kiểm kê theo vị trí" (phiếu kiểm kê, mã <mã công ty>-KKVT-NNNNN) — form chuẩn Danh mục quốc gia, chuẩn 04/11/2026.

Chạy: python gen_srs.py  → SRS - Kiểm kê theo vị trí.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc màn anh em
  ../ke-hoach-kiem-ke-theo-vi-tri/gen_srs.py (05/11, Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn).
Nguồn đọc 06/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Entities/PositionInventory/PositionInventoryResult.php, Services/PositionInventoryResult{,Write,Print,
      Attachment}Service.php, Services/PositionInventoryTreeService.php, Http/Controllers/V1/PositionInventoryResultController.php,
      Http/Requests/PositionInventoryResult/{PositionInventoryResultStoreRequest,PositionInventoryResultSaveResultRequest}.php
      (+ PositionInventory/PositionInventoryStoreRequest.php — bộ rule cha), Exports/PositionInventoryResultExport.php,
      Services/WarehouseInventoryLockService.php, Services/WarehouseImportWriteService.php (chặn vị trí đang kiểm kho),
      Services/PositionTransfer{,Write}Service.php (lập phiếu điều chuyển từ phiếu kiểm kê)}, MasterData (chặn xóa danh mục),
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (5 quyền nhóm "Kiểm kê theo vị trí", type 21)
  FE  pages/warehouse/position-inventory-results/** (index, create, _id/index, _id/edit, components/{PositionInventoryResultForm,
      PlanPickerModal, ResultCell, ApproveNoteModal, result-units.js, row-actions.js, export-excel.js}), dùng lại
      pages/finance/position-inventories/components/{ScopePicker, DetailTable}.vue, components/subsystem-menu/warehouse.js (Kiểm kho › Theo vị trí)
  Bối cảnh + quyết định: design.md, plan.md (Redmine #11786 #11787 #11803–#11808), spec docs/superpowers/specs/gop-db/2026-10-19-…
Ảnh: ./kkvt_shots — dev-hrm 06/11/2026 (_capture/capture.js, chặn mọi yêu cầu ghi; 0 yêu cầu ghi phát sinh). Giả trạng thái trên
  trình duyệt (sửa phản hồi GET, không gửi máy chủ): 12_edit, 13_delete (phiếu 144 giả Đang tạo); 15_wait_detail, 15_approve,
  15b_reject (phiếu 140 giả Chờ duyệt kết quả); 16b_complete (phiếu 142 giả không còn dòng cần điều chuyển); 11_plan_picker,
  11b_from_plan (popup Chọn kế hoạch giả 1 dòng, dữ liệu nạp dựng từ phiếu 146). Ảnh lỗi 10b_validate, 14b_result_validate:
  gọi hàm kiểm của form trên trình duyệt (không bấm Lưu / Lưu kết quả). 14_result, 16_handle là trạng thái THẬT trên dev.
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

TEN = 'Kiểm kê theo vị trí'
SHOTS = os.path.join(HERE, 'kkvt_shots')
ICONS = os.path.join(SHOTS, 'icons')
KH_ICONS = os.path.join(HERE, '..', 'ke-hoach-kiem-ke-theo-vi-tri', 'khkkvt_shots', 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Kiểm kho => Theo vị trí => Kiểm kê theo vị trí'
MENU_KH = 'Phân hệ Tài chính => Kiểm kê => Kế hoạch kiểm kê theo vị trí'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Kiểm kê theo vị trí.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NOTFOUND = '“Không tìm thấy phiếu kiểm kê hoặc bạn không có quyền xem.”'
NOPERM = '“Bạn không có quyền thực hiện chức năng này.”'
MISS = '“Bạn chưa nhập đầy đủ thông tin.”'
Q1 = 'Lập phiếu kiểm kê kho theo vị trí'
Q2 = 'Ban kiểm soát duyệt kết quả kiểm kê'
Q3 = 'Xử lý phiếu kiểm kê vị trí'
V1 = 'Xem phiếu kiểm kê vị trí - theo tổng công ty'
V2 = 'Xem phiếu kiểm kê vị trí - theo công ty'

A_LP = 'Người lập phiếu (thủ kho)'
A_BKS = 'Ban kiểm soát'
A_XL = 'Người xử lý phiếu'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng đã được cấp tài khoản; phạm vi xem theo quyền “%s” / “%s”, '
      'không có quyền xem chỉ thấy phiếu mình tạo.' % (V1, V2))
TN_OWNER = 'Người dùng có quyền thực hiện chức năng: người lập phiếu (người tạo phiếu), phiếu đang ở trạng thái Đang tạo.'
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Kiểm kê theo vị trí.\n'
      '3. Dữ liệu hiển thị trong phạm vi xem theo quyền (Phần 2).')

d = SrsDoc(out=OUT, menu=MENU, route='/warehouse/position-inventory-results', full_url='', img_dir=UML)

d.set_menu_icons({**{k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Kiểm kho': 'menu_nhom', 'Theo vị trí': 'menu_nhom2', 'Kiểm kê theo vị trí': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Chọn kế hoạch kiểm kê': 'o_kehoach', 'Lấy vị trí': 'btn_layvitri', 'Lưu và gửi': 'btn_luugui',
    'Sửa': 'btn_sua_row', 'Xóa': 'btn_xoa_row', 'Xem chi tiết': 'link_sophieu', 'Nhập kết quả': 'btn_nhapkq_row',
    'Lưu kết quả': 'btn_luukq', 'Duyệt kết quả': 'btn_duyet_row', 'Không duyệt': 'btn_khongduyet',
    'Xử lý': 'btn_dieuchuyen_row', 'In': 'btn_in_row', 'In danh sách': 'btn_in_list', 'Xuất Excel': 'btn_xuatexcel',
    'Lịch sử': 'btn_lichsu_row', 'Lập phiếu kiểm kê': 'btn_lapphieu_row',
}.items()}, **{k: os.path.join(KH_ICONS, v + '.png') for k, v in {   # chặng menu màn Kế hoạch: icon thật của màn đó
    'Phân hệ Tài chính': 'menu_phanhe', 'Kiểm kê': 'menu_nhom', 'Kế hoạch kiểm kê theo vị trí': 'menu_muc',
}.items()}})

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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Kiểm kê theo vị trí — phiếu kiểm kê theo vị trí (mã phiếu <mã công ty>-KKVT-NNNNN, '
    'ví dụ TPE-KKVT-00146), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ cách thủ kho lập phiếu kiểm kê (từ Kế hoạch kiểm kê theo vị trí hoặc lập tay), chọn ĐVT kiểm kê cho từng lô, nhập kết '
    'quả thực kiểm kèm file đính kèm, Ban kiểm soát duyệt / không duyệt kết quả và người xử lý xử lý chênh lệch thiếu.',
    'Làm rõ vòng đời trạng thái của phiếu (Đang tạo → Đang kiểm → Chờ duyệt kết quả → Chờ xử lý → Hoàn thành) và các màn khác '
    'đọc / ghi ngược dữ liệu phiếu (Kế hoạch kiểm kê theo vị trí, Phiếu điều chuyển vị trí, Phiếu nhập kho).',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo phiếu (Lưu / Lưu và tiếp tục), Chọn kế '
    'hoạch kiểm kê, Chọn phạm vi – Lấy vị trí – ĐVT kiểm kê, Lưu và gửi (chuyển Đang kiểm), Chỉnh sửa, Xóa, Xem chi tiết, Nhập kết '
    'quả kiểm kê (Lưu kết quả), Duyệt kết quả, Không duyệt, Xử lý phiếu (Tổng kiểm kê, Tạo phiếu điều chuyển vị trí, Hoàn thành), '
    'In phiếu / In danh sách, Xuất Excel (danh sách và 1 phiếu), Xem lịch sử thay đổi. Màn KHÔNG có Hủy phiếu, Khóa / Mở khóa và '
    'Import Excel.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phiếu ghi kết quả thực kiểm từng lô tại từng vị trí so với số tồn chụp lúc lập phiếu; Chênh lệch = Thực kiểm − SL.',
    'Dòng chênh lệch thiếu (Chênh lệch < 0, chưa tick Tổng kiểm kê) là nguồn để lập Phiếu điều chuyển vị trí; điều chuyển xử lý hết '
    'thì phiếu tự Hoàn thành.',
    'Phiếu Đang kiểm / Chờ duyệt kết quả khóa các vị trí của nó: Phiếu điều chuyển vị trí không chọn được, Phiếu nhập kho chặn nhập '
    'vào vị trí của phiếu Đang kiểm.',
    'Trạng thái phiếu đổi trạng thái của kế hoạch cha (Đã lập kiểm kê / Đang kiểm / Hoàn thành).',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Phiếu không tự ghi tồn kho; chỉ Phiếu điều chuyển vị trí lập từ phiếu mới đổi tồn (BR-01).',
    'Chỉ người có quyền “%s” mới tạo phiếu; chỉ người tạo mới Sửa / Xóa (khi Đang tạo) và Nhập kết quả (khi Đang kiểm) (BR-03, BR-05).' % Q1,
    'Mỗi lô phải có ít nhất 1 dòng ĐVT kiểm kê, tổng SL × hệ số quy đổi = SL lô (BR-04).',
    'Lưu kết quả bắt buộc Thực kiểm mọi dòng, Ghi chú khi có chênh lệch, file đính kèm khi phiếu chưa có file (BR-06).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu kiểm kê theo vị trí (phiếu)', 'Chứng từ <mã công ty>-KKVT-NNNNN của màn này: phạm vi vị trí, danh sách hàng – lô – số tồn, '
                                          'ĐVT kiểm kê, kết quả thực kiểm và hội đồng kiểm kê của một kho vật lý.'),
    ('Kế hoạch kiểm kê theo vị trí (kế hoạch)', 'Chứng từ <mã công ty>-KHKKVT-NNNNN (phân hệ Tài chính) mà phiếu được lập từ; tùy chọn.'),
    ('Kho vật lý', 'Kho thật chứa hàng; mỗi phiếu thuộc đúng 1 kho vật lý.'),
    ('Nhà / Dãy / Khoang / Vị trí', 'Cấu trúc 4 cấp của kho. Vị trí tự do là vị trí không thuộc khoang nào.'),
    ('Phạm vi kiểm kê', 'Các Nhà / Dãy / Khoang / Vị trí được tick; chỉ vị trí đã tick mới được lấy hàng tồn.'),
    ('Lấy vị trí', 'Lấy hàng tồn (> 0) theo từng lô tại các vị trí đã tick (chỉ khi lập tay, không chọn kế hoạch).'),
    ('ĐVT kiểm kê', 'Đơn vị tính dùng để đếm 1 lô. Mặc định ĐVT cơ sở; đổi sang ĐVT lớn hơn thì lô tách thành nhiều dòng '
                    '(vd 119 Cái → 5 Hộp 20 + 19 Cái).'),
    ('SL tồn / SL / Cộng', 'SL tồn = tồn của hàng tại vị trí; SL = tồn của lô (theo ĐVT kiểm kê ở dòng kết quả); Cộng = tổng tồn của '
                           'hàng theo công ty (phần trong ngoặc chữ đỏ).'),
    ('Thực kiểm / Chênh lệch', 'Thực kiểm = số đếm được; Chênh lệch = Thực kiểm − SL (âm = thiếu, chữ đỏ khi khác 0).'),
    ('Tổng kiểm kê', 'Ô tick ở dòng có chênh lệch: dòng thiếu được tick thì không cần điều chuyển (coi như xử lý theo tổng kiểm kê).'),
    ('Ban kiểm soát (BKS)', 'Người có quyền “%s”; duyệt / không duyệt kết quả.' % Q2),
    ('Trạng thái Đang tạo', 'Nhãn xám: phiếu mới lưu (nút Lưu); chỉ người tạo thấy, sửa, xóa.'),
    ('Trạng thái Đang kiểm', 'Nhãn vàng: phiếu đã gửi (Lưu và gửi) hoặc bị Không duyệt; người tạo nhập kết quả.'),
    ('Trạng thái Chờ duyệt kết quả', 'Nhãn vàng: đã Lưu kết quả, chờ Ban kiểm soát.'),
    ('Trạng thái Chờ xử lý', 'Nhãn vàng: đã duyệt, còn dòng chênh lệch thiếu cần xử lý.'),
    ('Trạng thái Hoàn thành', 'Nhãn xanh lá: duyệt không thiếu, bấm Hoàn thành, hoặc điều chuyển xử lý hết chênh lệch.'),
    ('Cấu trúc phân cấp', 'Phiếu > vị trí > hàng (SL tồn) > công ty (Cộng) > lô > dòng ĐVT kiểm kê (SL, Thực kiểm, Chênh lệch, Ghi chú, '
                          'Tổng kiểm kê); kèm phạm vi, hội đồng, file đính kèm.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn dùng 5 quyền nhóm “Kiểm kê theo vị trí” (phân hệ Kho). Ba quyền thao tác quyết định Tạo, Duyệt / Không duyệt, Xử lý; hai '
    'quyền phạm vi quyết định phiếu nào được xem. Sửa / Xóa / Nhập kết quả không cần quyền riêng mà gắn với người tạo phiếu. Super '
    'admin được coi như có đủ quyền thao tác và xem mọi công ty.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1, 'Hiện nút Tạo mới, lưu phiếu mới; chọn được kế hoạch Đang kiểm của kho mình là thủ kho trong popup Chọn kế hoạch; '
               'nút Lập phiếu kiểm kê ở màn Kế hoạch.'),
    ('Q2', Q2, 'Nút Duyệt kết quả / Không duyệt ở phiếu Chờ duyệt kết quả; nhận thông báo khi phiếu cùng công ty được Lưu kết quả; xem '
               'được phiếu Chờ duyệt kết quả dù ngoài phạm vi xem.'),
    ('Q3', Q3, 'Tick Tổng kiểm kê, Tạo phiếu điều chuyển vị trí, Hoàn thành ở phiếu Chờ xử lý; nhận thông báo khi phiếu cùng công ty '
               'được duyệt có chênh lệch thiếu; xem được phiếu Chờ xử lý dù ngoài phạm vi xem.'),
    ('—', 'Không cần quyền (gắn người tạo)', 'Sửa, Xóa (phiếu Đang tạo); Nhập kết quả – Lưu kết quả (phiếu Đang kiểm); In, Xuất '
                                              'Excel, Lịch sử với phiếu trong phạm vi xem.'),
], widths=[0.8, 1.9, 3.3])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Mọi phiếu của mọi công ty; ô lọc Công ty chọn được mọi công ty (Super admin như V1).'),
    ('V2', V2, 'Phiếu của công ty người xem + phiếu mình tạo; công ty người xem trống → chỉ phiếu mình tạo.'),
    ('—', 'Không có quyền nào', 'Chỉ phiếu do chính mình tạo.'),
], widths=[0.8, 2.2, 3.0])
d.p('Với mọi quyền: phiếu Đang tạo chỉ hiện với chính người tạo (kể cả Super admin).')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'V1', 'V2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ (theo V)', '✅ (theo V)', '✅ (theo V)', '✅ mọi công ty', '✅ công ty mình + của mình', '✅ của mình'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅ (Công ty – Phòng ban)', '✅ (Công ty – Phòng ban)', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo phiếu', '✅', '❌', '❌', '❌', '❌', '❌'),
    ('FR-06 Chọn kế hoạch kiểm kê', '✅ thủ kho của kho kế hoạch', '❌', '❌', '❌', '❌', '❌'),
    ('FR-07 Phạm vi, Lấy vị trí, ĐVT kiểm kê', '✅', '❌', '❌', '❌', '❌', '❌'),
    ('FR-08 Lưu và gửi', '✅', '❌', '❌', '❌', '❌', '✅ người tạo, sửa phiếu Đang tạo'),
    ('FR-09 Chỉnh sửa', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo',
     '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo'),
    ('FR-10 Xóa', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo',
     '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo'),
    ('FR-11 Xem chi tiết', '✅ trong phạm vi', '✅ + phiếu Chờ duyệt kết quả', '✅ + phiếu Chờ xử lý', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-12 Nhập kết quả', '✅ người tạo, Đang kiểm', '✅ người tạo, Đang kiểm', '✅ người tạo, Đang kiểm', '✅ người tạo, Đang kiểm',
     '✅ người tạo, Đang kiểm', '✅ người tạo, Đang kiểm'),
    ('FR-13 Duyệt kết quả', '❌', '✅ Chờ duyệt kết quả', '❌', '❌', '❌', '❌'),
    ('FR-14 Không duyệt', '❌', '✅ Chờ duyệt kết quả', '❌', '❌', '❌', '❌'),
    ('FR-15 Xử lý phiếu', '❌', '❌', '✅ Chờ xử lý', '❌', '❌', '❌'),
    ('FR-16 In phiếu / In danh sách', '✅', '✅', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-17 Xuất Excel', '✅', '✅', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-18 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('Hủy / Khóa – Mở khóa / Import', '—', '—', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.55, 0.8, 0.8, 0.75, 0.7, 0.8, 0.8])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có Q1: không có nút Tạo mới; nếu vẫn lưu phiếu mới (mở thẳng màn Tạo) → hệ thống báo ' + NOPERM + '; popup Chọn kế hoạch rỗng.',
    'Không có V1 / V2: vẫn vào màn, chỉ thấy phiếu mình tạo; không có ô lọc Công ty – Phòng ban.',
    'Mở chi tiết / sửa / in / xuất / lịch sử của phiếu ngoài phạm vi (qua đường link): hệ thống báo ' + NOTFOUND +
    '; màn chi tiết / sửa chuyển sang trang “Không tìm thấy trang”.',
    'Thao tác khi phiếu đã đổi trạng thái (mở 2 tab) → ' + CONFLICT + '; đúng trạng thái nhưng không phải người tạo / thiếu quyền → ' + NOPERM + '.',
    'Mở màn Sửa của phiếu không còn Đang tạo hoặc không phải người tạo → tự chuyển về màn chi tiết.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới', 'Có Q1 (hoặc Super admin)', 'Fail-closed: mặc định ẩn tới khi máy chủ trả quyền'),
    ('Nút Sửa, Xóa', 'Phiếu Đang tạo và người xem là người tạo', 'Máy chủ kiểm lại khi lưu / xóa'),
    ('Nút Nhập kết quả (dòng), Lưu kết quả (chi tiết)', 'Phiếu Đang kiểm và người xem là người tạo', 'Nhập kết quả trên dòng chỉ mở màn chi tiết'),
    ('Nút Duyệt kết quả, Không duyệt', 'Phiếu Chờ duyệt kết quả và có Q2', 'Trên dòng chỉ có Duyệt kết quả (mở chi tiết)'),
    ('Nút Tạo phiếu điều chuyển vị trí', 'Phiếu Chờ xử lý, có Q3, còn dòng chênh lệch thiếu chưa xử lý', 'Mở màn Tạo phiếu điều chuyển vị trí'),
    ('Nút Xử lý (dòng), Hoàn thành (chi tiết)', 'Phiếu Chờ xử lý, có Q3, không còn dòng cần điều chuyển', 'Hoàn thành hỏi xác nhận'),
    ('Nút In, Xuất Excel, Lịch sử', 'Mọi dòng trong phạm vi', 'Hiện thẳng tối đa 3 nút, còn lại trong “Hành động khác”'),
    ('Ô lọc Công ty – Phòng ban', 'Có V1 hoặc V2 (V2: khóa công ty mình)', 'Không quyền thì ẩn'),
], widths=[2.2, 2.3, 1.5])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_LP, [0, 1, 2, 3, 4, 5, 9, 10]), (A_BKS, [0, 6, 7]), (A_XL, [0, 8])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Tạo phiếu kiểm kê', 'crud'),
     ('FR-08', 'Lưu và gửi', 'action'),
     ('FR-09', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-10', 'Xóa phiếu', 'action'),
     ('FR-12', 'Nhập kết quả kiểm kê', 'crud'),
     ('FR-13', 'Duyệt kết quả', 'action'),
     ('FR-14', 'Không duyệt', 'action'),
     ('FR-15', 'Xử lý phiếu', 'action'),
     ('FR-16', 'In phiếu / In danh sách', 'io'),
     ('FR-17', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-11', 'Xem chi tiết', 'view', 'extend', [0], None),
     ('FR-18', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn kế hoạch kiểm kê', 'crud', 'extend', [1], None),
     ('FR-07', 'Phạm vi, Lấy vị trí, ĐVT kiểm kê', 'crud', 'extend', [1, 3], None)],
    'Sơ đồ Use Case tổng quan màn Kiểm kê theo vị trí')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu kiểm kê',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu kiểm kê theo vị trí',
       mota='Hiển thị bảng các phiếu kiểm kê theo vị trí trong phạm vi xem của người dùng (theo quyền tổng công ty / công ty / của '
            'mình), kèm kế hoạch cha, kho, trạng thái, người tạo, người duyệt, ngày tạo / cập nhật, phân trang và tổng số. Mỗi dòng '
            'có liên kết sang màn chi tiết, liên kết sang kế hoạch và nút thao tác theo trạng thái phiếu và quyền của người xem.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng vào màn từ menu, từ thông báo, hoặc từ liên kết ở màn Phiếu '
                'điều chuyển vị trí.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem theo quyền (V1 / V2 / của mình), luôn ẩn phiếu Đang tạo của người khác.\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu vừa đi vào màn con của màn này) và cấu hình cột đã '
             'lưu của người dùng.\n'
             '4. Hệ thống lấy phiếu khớp bộ lọc, sắp phiếu tạo gần nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, dòng “Hiển thị a–b / N”, phân trang và nút thao tác theo cờ của từng phiếu.',
       phu='• Không có phiếu nào khớp → trong bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Máy chủ lỗi khi nạp danh sách → thông báo “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”, bảng trống.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
           '• Phiên đăng nhập hết hạn khi đang thao tác → thông báo hết phiên, chuyển về màn đăng nhập.\n'
           '• Bấm mã kế hoạch ở cột Kế hoạch kiểm kê → mở chi tiết kế hoạch ở tab mới.',
       dacbiet='Cột mặc định hiện: cả 13 cột (STT, Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho, Trạng thái, Người tạo, Người duyệt, '
               'Ngày duyệt, Ngày tạo, Ngày cập nhật, Người cập nhật, Hành động); không có cột ẩn mặc định. Cột khóa: STT, Số phiếu, '
               'Hành động; Số phiếu ghim trái khi cuộn ngang. Sắp xếp được: Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho; mặc định '
               '(chưa chọn cột) phiếu tạo mới nhất ở trên. Đổi sắp xếp / bộ lọc / số dòng đều về trang 1.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Kiểm kê theo vị trí'),
   extra=[(shot('00b_menu'), 'Menu phân hệ Kho › Kiểm kho › Theo vị trí'),
          (shot('03_rowmenu'), 'Nút thao tác theo trạng thái: dòng Đang kiểm (Nhập kết quả, In, Hành động khác) và dòng Chờ xử lý')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Kiểm kê theo vị trí” trên thanh tiêu đề, tiêu đề bảng và tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
        ['- Chỉ hiện khi có quyền “%s”' % Q1, '- Rê chuột: “Tạo phiếu kiểm kê theo vị trí”', '- Bấm → mở màn Tạo phiếu (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → cửa sổ Chọn trường xuất Excel (mục 2.17)',
         '- Khóa trong lúc đang xuất']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “In danh sách theo bộ lọc đang áp”', '- Bấm → cửa sổ Xem trước danh sách (mục 2.16)']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', '<mã công ty>-KKVT-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết (mục 2.11)', '- Sắp xếp được', '- Cột khóa, ghim trái khi cuộn ngang']),
       ('Cột Kế hoạch kiểm kê', 'Link', 'Read-only', '<mã công ty>-KHKKVT-NNNNN', 'Theo dữ liệu',
        ['- Mã kế hoạch cha; trống nếu phiếu lập tay', '- Bấm → mở chi tiết kế hoạch ở tab mới', '- Sắp xếp được']),
       ('Cột Ngày kiểm kê', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Hiển thị',
        ['- Lập từ kế hoạch: ngày tạo kế hoạch; lập tay: ngày lập phiếu', '- Sắp xếp được']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Tên kho vật lý', '- Sắp xếp được (theo tên kho)']),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 5 giá trị', 'Hiển thị',
        ['- Đang tạo: nhãn xám', '- Đang kiểm, Chờ duyệt kết quả, Chờ xử lý: nhãn vàng', '- Hoàn thành: nhãn xanh lá',
         '- Không sắp xếp']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Họ tên người lập phiếu; không sắp xếp.'),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Người bấm Duyệt kết quả; trống khi chưa duyệt.'),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '- Ngày duyệt kết quả; trống khi chưa duyệt.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        '- Cùng giá trị Ngày kiểm kê kèm giờ (phiếu không có ngày tạo riêng).'),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Thời điểm cập nhật gần nhất.'),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Họ tên người cập nhật gần nhất.'),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Sửa, Xóa: phiếu Đang tạo của chính mình (mục 2.9, 2.10)',
           '- Nhập kết quả: phiếu Đang kiểm của mình → mở chi tiết (mục 2.12)',
           '- Duyệt kết quả: phiếu Chờ duyệt kết quả, có Q2 → mở chi tiết (mục 2.13)',
           '- Tạo phiếu điều chuyển vị trí / Xử lý: phiếu Chờ xử lý, có Q3 (mục 2.15)',
           '- In, Xuất Excel, Lịch sử: mọi dòng (mục 2.16, 2.17, 2.18)',
           '- Hiện thẳng tối đa 3 nút; nhiều hơn thì nút cuối là “Hành động khác” (ba chấm) chứa phần còn lại', '- Cột khóa']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', ['- Trong bảng: “Không có dữ liệu phù hợp.”', '- Chỉ hiện khi N = 0']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang đang xem', '- N: tổng số phiếu khớp bộ lọc trong phạm vi xem']),
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
        'During:\n– Lấy phiếu khớp bộ lọc; ẩn phiếu Đang tạo của người khác; tính cờ nút từng phiếu.\n'
        '– Máy chủ lỗi → hiển thị “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, phiếu tạo mới nhất ở trên; hiện nút Tạo mới nếu có quyền “%s”.' % Q1),
       ('Bấm Số phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem.\nAfter:\n– Mở màn chi tiết (mục 2.11); bộ lọc được ghi nhớ 10 phút.'),
       ('Bấm mã ở cột Kế hoạch kiểm kê', 'Click',
        'Before:\n– Phiếu lập từ kế hoạch.\nAfter:\n– Mở chi tiết kế hoạch ở tab mới; danh sách giữ nguyên.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho hỗ trợ sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc.'),
       ('Bấm số trang hoặc đổi Số dòng/trang', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới (đổi số dòng → về trang 1, nạp 1 lần); STT liên tục.'),
       ('Bấm Hành động khác (ba chấm)', 'Click',
        'Before:\n– Dòng có nhiều hơn 3 nút thao tác.\nAfter:\n– Mở menu các nút còn lại (vd Xuất Excel / Lịch sử).'),
       ('Bấm Nhập kết quả / Duyệt kết quả / Xử lý trên dòng', 'Click',
        'Before:\n– Nút chỉ hiện theo cờ của phiếu.\nAfter:\n– Mở màn chi tiết phiếu; thao tác thật làm ở chân màn chi tiết.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu kiểm kê',
       mota='Thu hẹp danh sách theo số phiếu, trạng thái, người tạo, người duyệt, hàng hóa, ngày kiểm kê, kho – nhà – dãy – khoang – '
            'vị trí và công ty – phòng ban. Ô tìm nhanh tìm theo số phiếu; các ô lọc nằm trong khối Tìm kiếm nâng cao, bật / tắt '
            'được bằng Cài đặt bộ lọc (mục 2.3). Kho → Nhà → Dãy → Khoang → Vị trí là chuỗi ô chọn phụ thuộc.',
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
               'ký tự; ký tự % và _ được hiểu là ký tự đại diện. Hàng hóa khớp theo mã HOẶC tên hàng trên phiếu. Kho / Nhà / Dãy / '
               'Khoang / Vị trí lọc phiếu có tick đúng mục đó trong phạm vi kiểm kê. Ngày kiểm kê lấy trọn hai ngày biên. Mọi điều '
               'kiện kết hợp kiểu VÀ. Người tạo / Người duyệt liệt kê toàn bộ nhân viên. Ghi nhớ bộ lọc 10 phút khi đi vào màn con.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'), shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số phiếu”', '- Khớp một phần số phiếu', '- Áp khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh và ô chữ, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Bấm → xóa mọi tiêu chí kể cả ô tìm nhanh', '- Nạp lại từ trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (mọi trạng thái)', '- Lựa chọn: Đang tạo / Đang kiểm / Chờ duyệt kết quả / Chờ xử lý / Hoàn thành']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', ['- Mặc định: trống', '- Toàn bộ nhân viên']),
       ('Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Lọc phiếu do người đó duyệt kết quả']),
       ('Hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Mã hoặc tên hàng”', '- Phiếu có ít nhất 1 hàng có mã hoặc tên chứa chuỗi nhập']),
       ('Ngày kiểm kê', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai ngày biên; được bỏ trống một đầu']),
       ('Kho', 'Dropdown', 'Enable', 'Danh sách kho vật lý', 'Không', 'Trống',
        ['- Mặc định: trống', '- Hiển thị “Mã - Tên”', '- Đổi kho → xóa Nhà, Dãy, Khoang, Vị trí']),
       ('Nhà', 'Dropdown', 'Enable', 'Nhà của kho đã chọn', 'Không', 'Trống', ['- Rỗng khi chưa chọn Kho', '- Đổi Nhà → xóa Dãy, Khoang, Vị trí']),
       ('Dãy', 'Dropdown', 'Enable', 'Dãy của Nhà đã chọn', 'Không', 'Trống', ['- Chưa chọn Nhà → mọi dãy của kho', '- Đổi Dãy → xóa Khoang, Vị trí']),
       ('Khoang', 'Dropdown', 'Enable', 'Khoang của Dãy đã chọn', 'Không', 'Trống', '- Đổi Khoang → xóa Vị trí.'),
       ('Vị trí', 'Dropdown', 'Enable', 'Vị trí của Khoang đã chọn', 'Không', 'Trống',
        '- Chưa chọn cấp cha → mọi vị trí của kho, gồm vị trí tự do.'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Ẩn khi thiếu quyền',
        ['- Chỉ hiện khi có V1 hoặc V2', '- V2: khóa ở công ty mình (biểu tượng ổ khóa)']),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Phòng ban của công ty', 'Không', 'Ẩn khi thiếu quyền',
        '- Lọc phiếu theo phòng ban của người lập.'),
   ],
   ev=[
       ('Đổi giá trị một ô chọn', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\n'
        'During:\n– Đổi cấp cha (Kho / Nhà / Dãy / Khoang) → xóa giá trị cấp con; đổi Kho → nạp cấu trúc kho mới.\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí (một lần).'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh và ô Hàng hóa, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm phiếu có số phiếu chứa chuỗi nhập (và hàng khớp ô Hàng hóa).\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Có hoặc không có tiêu chí đang áp.\nAfter:\n– Xóa mọi tiêu chí, bỏ sắp xếp, nạp lại từ trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\nAfter:\n– Mở / thu gọn khối; lần mở đầu nạp lựa chọn Trạng thái, Kho.'),
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
            'người dùng cho màn này, không ảnh hưởng người khác và không đổi dữ liệu phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 11 mục lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 11 mục theo thứ tự thiết kế; phải bấm Lưu mới có hiệu lực.\n'
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
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách 11 mục', '–', 'Theo cấu hình đã lưu',
        ['- Trạng thái, Người tạo, Người duyệt, Hàng hóa, Ngày kiểm kê, Kho', '- Nhà, Dãy, Khoang, Vị trí, Công ty – Phòng ban']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → mục đó không hiện ở khối Tìm kiếm nâng cao.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích lại đủ 11 mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
       ('Khối lọc sau khi lưu', 'Table/Grid', 'Read-only', '–', '–', 'Theo cấu hình',
        '- Chỉ hiện mục đã tích, đúng thứ tự đã kéo.'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click', 'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình đang lưu (chưa lưu lần nào → đủ 11 mục).'),
       ('Kéo đổi vị trí một mục', 'Drag', 'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ 11 mục, thứ tự thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click', 'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 13 cột của bảng danh sách. Ba cột STT, Số phiếu, Hành động bị khóa; cấu '
            'hình lưu riêng theo người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 13 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 13 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ nguyên sau khi tải lại trang, đăng nhập '
               'lại, đổi trình duyệt; người dùng khác không bị ảnh hưởng.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 13 cột', '–', 'Theo cấu hình đã lưu',
        ['- STT, Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho, Trạng thái, Người tạo',
         '- Người duyệt, Ngày duyệt, Ngày tạo, Ngày cập nhật, Người cập nhật, Hành động']),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Số phiếu, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/13 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click', 'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu của người dùng.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Cột khóa không đổi được vị trí.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change', 'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/13 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5 Tạo phiếu
FORM_UI = [
    ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     ['- Tạo: “Tạo phiếu kiểm kê theo vị trí”', '- Sửa: “Sửa phiếu kiểm kê theo vị trí: <số phiếu>”']),
    ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại',
     '- Góc phải khối Thông tin chung: “<Họ tên> - dd/mm/yyyy hh:mm” (màn Sửa: người tạo và giờ tạo).'),
    ('Số phiếu', 'Textbox', 'Disable', '<mã công ty>-KKVT-NNNNN', '–', 'Ẩn ở màn Tạo',
     '- Chỉ hiện ở màn Sửa / Chi tiết; mã tự sinh khi lưu lần đầu, không sửa được.'),
    ('Ô Kế hoạch kiểm kê', 'Textbox', 'Enable', 'Kế hoạch Đang kiểm được lập', 'Không', 'Trống',
     ['- Màn Tạo: gợi ý “Chọn kế hoạch kiểm kê”, bấm vào ô → popup Chọn kế hoạch (mục 2.6), nút × bỏ chọn',
      '- Màn Sửa / Chi tiết: chỉ đọc, mã là liên kết mở kế hoạch ở tab mới']),
    ('Ngày kiểm kê', 'Textbox', 'Disable', 'dd/mm/yyyy', 'Có', 'Ngày hiện tại',
     ['- Không sửa được', '- Lập tay: hôm nay; lập từ kế hoạch: ngày tạo kế hoạch']),
    ('Kho vật lý', 'Dropdown', 'Enable / Disable', 'Danh sách kho vật lý', 'Có', 'Trống',
     ['- Gợi ý “Chọn kho vật lý”; hiển thị “Mã - Tên”', '- Có kế hoạch: khóa, lấy kho của kế hoạch',
      '- Đổi kho khi bảng Chi tiết đã có dữ liệu → hộp “Đổi kho vật lý” (mục 2.7)', '- Lỗi: “Kho vật lý – Vui lòng chọn kho vật lý.”']),
    ('Khối Phạm vi kiểm kê', 'Table/Grid', 'Enable / Disable', '4 cột tick', 'Có (Vị trí)', 'Trống',
     ['- 4 cột Nhà / Dãy / Khoang / Vị trí; đặc tả ở mục 2.7', '- Có kế hoạch: khóa theo phạm vi kế hoạch',
      '- Lỗi: “Phạm vi kiểm kê – Chưa chọn đủ thông tin vị trí!”']),
    ('Nút Lấy vị trí', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị khi lập tay',
     ['- Góc phải tiêu đề khối Phạm vi kiểm kê; ẩn khi đã chọn kế hoạch', '- Rê chuột: “Lấy danh sách hàng tồn tại các vị trí đã tick”']),
    ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Có', '“Không có dữ liệu”',
     ['- Cột: STT, Nhà kho, Vị trí, Tên hàng, Model, Mã hàng, Thương hiệu, ĐVT, SL tồn',
      '- Nhóm “Chi tiết tồn theo công ty”: Công ty (Cộng trong ngoặc đỏ), Lô (SL lô trong ngoặc đỏ), SL, ĐVT kiểm kê *',
      '- Lỗi: “Chi tiết – Chưa có vị trí nào. Vui lòng bấm \"Lấy vị trí\".” (có kế hoạch: “Chi tiết – Kế hoạch kiểm kê không có vị trí nào.”)']),
    ('Ô ĐVT kiểm kê', 'Dropdown', 'Enable', 'ĐVT của hàng', 'Có', 'ĐVT cơ sở',
     ['- Mỗi dòng kết quả của lô 1 ô; đổi ĐVT tách / gộp dòng (mục 2.7)', '- Lỗi: “Bắt buộc phải nhập” / “Không thuộc hàng hóa này.”']),
    ('Khối Hội đồng kiểm kê', 'Table/Grid', 'Enable', '≥ 1 dòng', 'Có', '1 dòng trống (lập tay)',
     ['- Cột STT, Nhân viên *, Chức vụ *, Hành động', '- Có kế hoạch: nạp sẵn hội đồng của kế hoạch, vẫn sửa được',
      '- Lỗi: “Hội đồng kiểm kê – Vui lòng thêm ít nhất 1 thành viên.”']),
    ('Nút Thêm dòng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề khối Hội đồng; bấm → thêm 1 dòng trống.'),
    ('Ô Nhân viên', 'Dropdown', 'Enable', 'Nhân viên đang làm việc', 'Có', 'Trống',
     ['- Gợi ý “Chọn nhân viên”', '- Chọn → tự điền Chức vụ đầu tiên của nhân viên',
      '- Lỗi: “Nhân viên – Vui lòng chọn nhân viên.” / “Nhân viên – Bị trùng.”']),
    ('Ô Chức vụ', 'Dropdown', 'Enable', 'Chức vụ của nhân viên', 'Có', 'Chức vụ đầu tiên',
     ['- Gợi ý “Chọn chức vụ”', '- Lỗi: “Chức vụ – Vui lòng chọn chức vụ.”']),
    ('Nút Xóa dòng hội đồng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Thùng rác đỏ; bấm → xóa dòng ngay, không hỏi.'),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Rê chuột: “Lưu phiếu ở trạng thái Đang tạo”', '- Lưu xong về danh sách; khóa trong lúc lưu']),
    ('Nút Lưu và gửi', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Rê chuột: “Lưu và gửi phiếu sang bước kiểm (trạng thái Đang kiểm)”', '- Đặc tả ở mục 2.8']),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị ở màn Tạo',
     ['- Rê chuột: “Lưu (Đang tạo) rồi ở lại tạo phiếu tiếp theo”', '- Không có ở màn Sửa']),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi “Thông tin chưa lưu”.'),
    ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Nội dung: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút Thoát: rời màn, không lưu',
      '- Nút Ở lại / (x): đóng hộp, giữ dữ liệu']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Thành công: “Lưu thành công.” / “Lưu và gửi thành công.”', '- Thiếu: ' + MISS,
      '- Không quyền tạo: ' + NOPERM, '- Phiếu / kế hoạch đã đổi trạng thái: ' + CONFLICT, '- Lỗi khác: câu lỗi máy chủ hoặc “Lưu thất bại.”']),
]

SAVE_DURING = ('During:\n– Kho vật lý trống → “Kho vật lý – Vui lòng chọn kho vật lý.”\n'
               '– Chưa tick vị trí → “Phạm vi kiểm kê – Chưa chọn đủ thông tin vị trí!”\n'
               '– Bảng Chi tiết trống → “Chi tiết – Chưa có vị trí nào. Vui lòng bấm \"Lấy vị trí\".”\n'
               '– Hội đồng không có dòng → “Hội đồng kiểm kê – Vui lòng thêm ít nhất 1 thành viên.”; thiếu nhân viên → “Nhân viên – '
               'Vui lòng chọn nhân viên.”; trùng → “Nhân viên – Bị trùng.”; thiếu chức vụ → “Chức vụ – Vui lòng chọn chức vụ.”\n'
               '– Mọi lỗi hiện cùng lúc dưới từng ô, thông báo ' + MISS + ', cuộn tới ô lỗi đầu tiên.\n'
               '– Máy chủ kiểm lại: ĐVT kiểm kê không thuộc hàng → “Không thuộc hàng hóa này.”; tổng quy đổi lệch SL lô → '
               '“Tổng số lượng quy đổi (x) khác SL lô (y).”; lô không có dòng kiểm kê → “Lô chưa có dòng kiểm kê.”\n' + ERR)

fr(5, 'Tạo phiếu kiểm kê (Lưu / Lưu và tiếp tục)', usecase=('FR-05', 'Tạo phiếu kiểm kê', 'crud', A_LP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo phiếu kiểm kê theo vị trí',
       mota='Thủ kho có quyền “%s” lập phiếu kiểm kê: chọn kế hoạch kiểm kê (nạp sẵn kho, phạm vi, hàng – lô, hội đồng) hoặc lập '
            'tay (chọn kho, tick phạm vi, Lấy vị trí), chỉnh ĐVT kiểm kê, khai hội đồng rồi bấm Lưu: phiếu ở trạng thái Đang tạo '
            '(chỉ người tạo thấy). Lập từ kế hoạch thì kế hoạch chuyển Đã lập kiểm kê.' % Q1,
       tacnhan='Người dùng có quyền thực hiện chức năng: %s.' % Q1,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có quyền “%s”.\n3. Có kho vật lý có cấu trúc vị trí, hoặc có kế hoạch '
                'Đang kiểm mà người dùng là thủ kho.' % Q1,
       chinh='1. Người dùng bấm Tạo mới ở danh sách (hoặc Lập phiếu kiểm kê ở màn Kế hoạch — form nạp sẵn kế hoạch).\n'
             '2. Hệ thống mở màn “Tạo phiếu kiểm kê theo vị trí”: Ngày kiểm kê = hôm nay, Hội đồng có 1 dòng trống.\n'
             '3. Người dùng chọn kế hoạch (mục 2.6) hoặc chọn Kho vật lý, tick phạm vi, bấm Lấy vị trí (mục 2.7).\n'
             '4. Người dùng chỉnh ĐVT kiểm kê từng lô nếu cần; khai Nhân viên (Chức vụ tự điền), Thêm dòng nếu cần.\n'
             '5. Người dùng bấm Lưu.\n'
             '6. Hệ thống kiểm tra dữ liệu, lưu phiếu trạng thái Đang tạo với công ty / phòng ban / bộ phận của người tạo, sinh mã '
             '<mã công ty>-KKVT-NNNNN; ngày phiếu = ngày tạo kế hoạch (nếu có) hoặc hiện tại.\n'
             '7. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu; có kế hoạch → kế hoạch chuyển Đã lập kiểm kê, ghi '
             '“Thay đổi trạng thái” vào lịch sử kế hoạch (ghi chú “Lập phiếu kiểm kê <số phiếu>.”).\n'
             '8. Hệ thống hiển thị “Lưu thành công.” và chuyển về màn danh sách.',
       phu='• Bấm Lưu và tiếp tục → lưu như trên (Đang tạo), ở lại màn Tạo với form trắng (vào từ kế hoạch thì bỏ kế hoạch đã chọn).\n'
           '• Thiếu dữ liệu bắt buộc → báo đủ lỗi dưới từng ô cùng lúc, thông báo ' + MISS + ', không lưu.\n'
           '• Kế hoạch vừa bị người khác lập phiếu / đổi trạng thái → ' + CONFLICT + ', không lưu.\n'
           '• Không có quyền “%s” → %s.\n' % (Q1, NOPERM) +
           '• Bấm Quay lại / chuyển menu / đóng tab khi đã nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì → về danh '
           'sách ngay. Màn là trang riêng, không có (x) / click ra ngoài.\n'
           '• Lỗi máy chủ → câu lỗi hoặc “Lưu thất bại.”, dữ liệu đã nhập giữ nguyên.',
       dacbiet='Các nút lưu khóa trong lúc đang lưu để một lần bấm không tạo 2 phiếu. Phiếu không có trường nhập duy nhất: mã tự sinh '
               'theo công ty người tạo + số thứ tự, không sửa được. Lưu và Lưu và gửi dùng chung một bộ điều kiện. Không có ô Ghi chú '
               'trên form. Số tồn là ảnh chụp lúc Lấy vị trí / lúc lập kế hoạch.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'), shot_caption='Màn Tạo phiếu lập tay sau khi chọn kho, phạm vi và Lấy vị trí'),
   extra=[(shot('10_create'), 'Màn Tạo phiếu lúc mới mở'),
          (shot('10b_validate_full'), 'Lỗi bắt buộc hiện cùng lúc khi bấm lưu thiếu dữ liệu'),
          (shot('10g_unsaved'), 'Hộp “Thông tin chưa lưu” khi rời màn')],
   ui=FORM_UI,
   ev=[
       ('Mở màn Tạo', 'System',
        'Before:\n– Nút Tạo mới chỉ hiện khi có quyền “%s”.\nDuring:\n– Nạp danh sách kho vật lý, nhân viên kèm chức vụ, ngày hôm nay; '
        'vào từ kế hoạch → nạp kế hoạch, không được lập → trang “Không tìm thấy trang”.\n– Lỗi → “Không tải được dữ liệu.”.\n'
        'After:\n– Hiển thị form, Hội đồng có 1 dòng trống; chưa tính là đã thay đổi.' % Q1),
       ('Chọn Nhân viên', 'Change',
        'Before:\n– Nhân viên đang làm việc.\nAfter:\n– Tự điền Chức vụ đầu tiên của nhân viên; bỏ chọn → xóa Chức vụ.'),
       ('Bấm Thêm dòng / Xóa dòng hội đồng', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Thêm 1 dòng trống / bỏ dòng đó.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Kiểm tra quyền “%s”.\n– Nếu không có quyền → hiển thị %s và dừng xử lý.\n'
        '– Có kế hoạch: kế hoạch phải còn Đang kiểm và người dùng được lập, nếu không → %s.\n' % (Q1, NOPERM, CONFLICT) + SAVE_DURING + '\n'
        'After:\n– Lưu phiếu trạng thái Đang tạo, sinh số phiếu, lưu phạm vi, chi tiết + ĐVT kiểm kê, hội đồng.\n'
        '– Ghi một dòng lịch sử “Tạo mới”; có kế hoạch → kế hoạch Đã lập kiểm kê + lịch sử kế hoạch.\n'
        '– Hiển thị “Lưu thành công.”, về màn danh sách.'),
       ('Bấm Lưu và tiếp tục', 'Click',
        'Before:\n– Như Lưu.\nDuring:\n– Kiểm tra như Lưu.\n' + ERR + '\n'
        'After:\n– Lưu như Lưu (Đang tạo), ghi lịch sử “Tạo mới”, hiển thị “Lưu thành công.”, làm trắng form và ở lại màn Tạo.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu hiện tại với lúc mở màn.\nDuring:\n– Có thay đổi → hiện hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu; Ở lại: giữ nguyên form.'),
   ])

# ------------------------------------------------------------ 2.6 Chọn kế hoạch
fr(6, 'Chọn kế hoạch kiểm kê', usecase=('FR-06', 'Chọn kế hoạch kiểm kê', 'crud', A_LP),
   rule=('- Màn Thêm mới, Bộ lọc và Dropdown.', 'create'),
   intro=dict(
       ten='Chọn kế hoạch kiểm kê để lập phiếu',
       mota='Ở màn Tạo, bấm ô Kế hoạch kiểm kê mở popup “Chọn kế hoạch kiểm kê theo vị trí” chỉ liệt kê kế hoạch Đang kiểm mà người '
            'dùng được lập phiếu (có quyền “%s” và là thủ kho của một kho trong kế hoạch). Chọn 1 dòng → form nạp toàn bộ dữ liệu '
            'kế hoạch: kho, phạm vi đã tick, hàng – lô – số tồn (ĐVT cơ sở, SL = SL lô), hội đồng; Ngày kiểm kê = ngày tạo kế hoạch.' % Q1,
       tacnhan='Người dùng có quyền thực hiện chức năng: %s, là thủ kho của kho trong kế hoạch.' % Q1,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo phiếu.\n3. Có kế hoạch Đang kiểm của kho mình là thủ kho.',
       chinh='1. Người dùng bấm vào ô Kế hoạch kiểm kê.\n'
             '2. Hệ thống mở popup, nạp trang 1 danh sách kế hoạch được lập.\n'
             '3. Người dùng nhập mã kế hoạch, bấm Tìm kiếm (hoặc Enter); sắp xếp / đổi trang nếu cần.\n'
             '4. Người dùng bấm vào một dòng.\n'
             '5. Hệ thống đóng popup, nạp kế hoạch vào form; khóa Kho vật lý và Phạm vi kiểm kê, ẩn nút Lấy vị trí.',
       phu='• Không có kế hoạch nào → “Không có kế hoạch kiểm kê nào bạn được lập phiếu.”.\n'
           '• Bấm mã kế hoạch trong popup → mở chi tiết kế hoạch ở tab mới, không chọn dòng.\n'
           '• Kế hoạch không còn được lập khi nạp → “Không tìm thấy kế hoạch kiểm kê hoặc bạn không được lập phiếu cho kế hoạch này.”.\n'
           '• Bấm × trong ô Kế hoạch → bỏ kế hoạch, form về trạng thái lập tay trống.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng popup, form giữ nguyên.\n'
           '• Màn Sửa không đổi được kế hoạch (ô chỉ đọc; rê nhãn hiện gợi ý).',
       dacbiet='Super admin cũng phải là thủ kho mới thấy kế hoạch trong popup. Vào từ nút Lập phiếu kiểm kê ở màn Kế hoạch: form tự '
               'nạp kế hoạch, không mở popup; không được lập → trang “Không tìm thấy trang”.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới => Chọn kế hoạch kiểm kê', 'Popup mở ngay trên màn Tạo phiếu.'),
       (MENU_KH + ' => Lập phiếu kiểm kê', 'Mở màn Tạo phiếu đã nạp sẵn kế hoạch (thủ kho, kế hoạch Đang kiểm).')],
       shot=shot('11_plan_picker'), shot_caption='Popup Chọn kế hoạch kiểm kê theo vị trí'),
   extra=[(shot('11b_from_plan'), 'Màn Tạo phiếu sau khi chọn kế hoạch: kho, phạm vi khóa, chi tiết và hội đồng nạp sẵn')],
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        ['- “Chọn kế hoạch kiểm kê theo vị trí”', '- Dòng phụ “Chỉ kế hoạch đang kiểm mà bạn được lập phiếu”']),
       ('Ô Mã phiếu', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập mã kế hoạch kiểm kê”', '- Khớp một phần mã', '- Có nút × xóa nhanh']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Áp ô Mã phiếu, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Xóa ô Mã phiếu, bỏ sắp xếp, nạp lại trang 1.'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- Liên tục theo trang.'),
       ('Cột Mã phiếu', 'Link', 'Read-only', '–', '–', 'Hiển thị', ['- Mã kế hoạch; sắp xếp được', '- Bấm → mở chi tiết kế hoạch ở tab mới']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- Kho của kế hoạch.'),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- Người lập kế hoạch; sắp xếp được.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', '–', 'Hiển thị', '- Sắp xếp được; mặc định kế hoạch mới nhất trên.'),
       ('Dòng kế hoạch', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu', '- Bấm cả dòng → chọn kế hoạch, đóng popup.'),
       ('Phân trang popup', 'Pagination', 'Enable', '10, 20, 50, 100', '–', '10', ['- Mặc định: 10 dòng', '- Dòng “Hiển thị a–b / N”']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- “Không có kế hoạch kiểm kê nào bạn được lập phiếu.”'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup, không chọn.'),
       ('Nút × trong ô Kế hoạch', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi chưa chọn', '- Bỏ kế hoạch, làm trắng form.'),
   ],
   ev=[
       ('Bấm ô Kế hoạch kiểm kê', 'Click',
        'Before:\n– Chỉ màn Tạo.\nDuring:\n– Lấy kế hoạch Đang kiểm mà người dùng có quyền “%s” và là thủ kho của kho trong kế hoạch.\n'
        'After:\n– Mở popup, hiện trang 1.' % Q1),
       ('Bấm Tìm kiếm / Làm mới / sắp xếp / đổi trang', 'Click',
        'Before:\n– Popup đang mở.\nAfter:\n– Nạp lại danh sách theo mã, thứ tự, trang mới.'),
       ('Bấm một dòng kế hoạch', 'Click',
        'Before:\n– Kế hoạch phải còn Đang kiểm và người dùng được lập (kiểm thủ kho kho đầu tiên / Super admin).\n'
        'During:\n– Không còn được lập → “Không tìm thấy kế hoạch kiểm kê hoặc bạn không được lập phiếu cho kế hoạch này.”.\n'
        'After:\n– Đóng popup, nạp kho, phạm vi, chi tiết (ĐVT cơ sở, SL = SL lô), hội đồng; Ngày kiểm kê = ngày tạo kế hoạch.'),
       ('Bấm × bỏ kế hoạch', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Xóa kế hoạch, kho, phạm vi, chi tiết; hội đồng 1 dòng trống.'),
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng popup, form giữ nguyên.'),
   ])

# ------------------------------------------------------------ 2.7 Phạm vi + Lấy vị trí + ĐVT
fr(7, 'Chọn phạm vi, Lấy vị trí và ĐVT kiểm kê', usecase=('FR-07', 'Phạm vi, Lấy vị trí, ĐVT kiểm kê', 'crud', A_LP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Chọn phạm vi, lấy hàng tồn và chọn ĐVT kiểm kê',
       mota='Khi lập tay: tick Nhà → Dãy → Khoang → Vị trí của kho đã chọn rồi bấm Lấy vị trí để đổ hàng tồn (> 0) theo từng lô vào '
            'bảng Chi tiết. Với mọi phiếu (lập tay hoặc từ kế hoạch): mỗi lô có ô ĐVT kiểm kê, mặc định ĐVT cơ sở; đổi sang ĐVT lớn '
            'hơn thì lô tự tách dòng sao cho tổng SL × hệ số = SL lô.',
       tacnhan='Người dùng có quyền thực hiện chức năng: %s (màn Tạo) hoặc người tạo phiếu Đang tạo (màn Sửa).' % Q1,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo hoặc Sửa phiếu.\n3. Lấy vị trí: đã chọn Kho vật lý, không '
                'chọn kế hoạch.',
       chinh='1. Người dùng tick Nhà; cột Dãy hiện dãy của nhà đã tick (nhóm theo nhà); tick Dãy → cột Khoang; tick Khoang → cột Vị '
             'trí, kèm nhóm “Vị trí tự do” luôn hiện.\n'
             '2. Người dùng tick Vị trí (có ô tìm và “Chọn hết” của cột / nhóm).\n'
             '3. Người dùng bấm Lấy vị trí; hệ thống lấy hàng và lô tồn > 0 tại vị trí đã tick, gom theo công ty, kèm danh sách ĐVT.\n'
             '4. Hệ thống thay toàn bộ bảng Chi tiết; mỗi lô 1 dòng ĐVT cơ sở, SL = SL lô.\n'
             '5. Người dùng đổi ĐVT kiểm kê của một dòng: hệ thống tính SL dòng = phần nguyên (SL còn lại / hệ số); phần dư > 0 thêm '
             '1 dòng ĐVT cơ sở; dư 0 bỏ các dòng sau.',
       phu='• Chưa chọn Kho mà bấm Lấy vị trí → lỗi đỏ dưới ô Kho, thông báo ' + MISS + '.\n'
           '• Chưa tick vị trí → “Chưa chọn đủ thông tin vị trí!”, lỗi đỏ dưới khối Phạm vi.\n'
           '• Vị trí đã tick không có hàng tồn → “Các vị trí đã chọn không có hàng tồn.”, bảng giữ nguyên.\n'
           '• Đổi ĐVT mà SL không đủ quy đổi (phần nguyên = 0) → “Số lượng không đủ để quy đổi!”, trả ĐVT cũ.\n'
           '• Bỏ tick cấp cha → tự bỏ tick cấp con không còn cha (vị trí tự do không ảnh hưởng).\n'
           '• Đổi Kho khi bảng Chi tiết có dữ liệu → hộp “Đổi kho vật lý”: Đổi kho = xóa phạm vi + Chi tiết; Hủy = giữ kho cũ.',
       dacbiet='Ô tìm mỗi cột khớp một phần “mã - tên”, có × xóa nhanh; “Chọn hết” chỉ tick mục đang hiện. Nút Lấy vị trí khóa trong '
               'lúc lấy. Đổi phạm vi sau Lấy vị trí KHÔNG tự xóa bảng Chi tiết. Ô ĐVT không để trống được (bấm × tự trả ĐVT cũ). '
               'Máy chủ đọc lại hệ số quy đổi theo danh mục hàng, không tin hệ số gửi lên.'),
   layout=dict(menu=MENU + ' => Tạo mới => Lấy vị trí', shot=shot('10d_scope'), shot_caption='Khối Phạm vi kiểm kê đã tick Nhà – Dãy – Khoang – Vị trí'),
   extra=[(shot('10c_filled_full'), 'Bảng Chi tiết sau Lấy vị trí, cột ĐVT kiểm kê từng lô'),
          (shot('10e_doikho'), 'Hộp xác nhận “Đổi kho vật lý”')],
   ui=[
       ('Tiêu đề khối', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Phạm vi kiểm kê”, nút Lấy vị trí ở góc phải.'),
       ('Cột Nhà', 'Checkbox', 'Enable', 'Nhà của kho', 'Không', 'Chưa tick', ['- Nhãn có dấu * nhưng không bắt buộc riêng', '- “Mã - Tên” các nhà']),
       ('Cột Dãy', 'Checkbox', 'Enable', 'Dãy của nhà đã tick', 'Không', 'Chưa tick',
        ['- Nhóm theo nhà, kèm “Chọn hết” của nhóm', '- Chưa tick nhà: “Chưa chọn nhà hoặc không có dữ liệu”']),
       ('Cột Khoang', 'Checkbox', 'Enable', 'Khoang của dãy đã tick', 'Không', 'Chưa tick',
        ['- Nhóm “Mã nhà | Mã dãy”', '- Chưa tick dãy: “Chưa chọn dãy hoặc không có dữ liệu”']),
       ('Cột Vị trí', 'Checkbox', 'Enable', 'Vị trí tự do + vị trí của khoang đã tick', 'Có', 'Chưa tick',
        ['- Nhóm “Vị trí tự do” luôn hiện', '- Ít nhất 1 vị trí; khung viền đỏ khi thiếu']),
       ('Ô tìm của từng cột', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', '- Lọc mục theo “mã - tên”, có × xóa nhanh.'),
       ('Ô Chọn hết', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Chưa tick', '- Tick / bỏ tick mọi mục đang hiện của cột hoặc nhóm.'),
       ('Nút Lấy vị trí', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → lấy hàng tồn tại vị trí đã tick, thay bảng Chi tiết', '- Khóa, hiện vòng xoay trong lúc lấy', '- Ẩn khi có kế hoạch']),
       ('Ô ĐVT kiểm kê', 'Dropdown', 'Enable', 'ĐVT của hàng', 'Có', 'ĐVT cơ sở',
        ['- Lựa chọn: các ĐVT khai cho hàng', '- Đổi → tách / gộp dòng của lô', '- Gợi ý “Chọn ĐVT”']),
       ('Cột SL', 'Table/Grid', 'Read-only', '> 0', '–', 'SL lô', '- SL của dòng theo ĐVT kiểm kê; tự tính khi đổi ĐVT.'),
       ('Hộp “Đổi kho vật lý”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Đổi kho vật lý sẽ xóa phạm vi kiểm kê và danh sách vị trí đã lấy. Bạn có muốn tiếp tục?”', '- Nút Đổi kho, Hủy, (x)']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Chưa chọn đủ thông tin vị trí!”', '- “Các vị trí đã chọn không có hàng tồn.”', '- “Số lượng không đủ để quy đổi!”',
         '- “Không tải được cấu trúc kho.”']),
   ],
   ev=[
       ('Tick / bỏ tick một mục', 'Change',
        'Before:\n– Đã chọn Kho vật lý, phiếu không có kế hoạch.\nDuring:\n– Bỏ tick cấp cha → tự bỏ tick cấp con không còn cha.\n'
        'After:\n– Cập nhật các cột con; có vị trí → xóa lỗi đỏ của khối.'),
       ('Bấm Lấy vị trí', 'Click',
        'Before:\n– Kho vật lý đã chọn, nếu không → lỗi dưới ô Kho, ' + MISS + '.\n– Có vị trí tick, nếu không → “Chưa chọn đủ thông tin vị trí!”.\n'
        'During:\n– Lấy hàng và lô tồn > 0, gom theo công ty, kèm ĐVT.\n– Không có hàng → “Các vị trí đã chọn không có hàng tồn.”.\n' + ERR + '\n'
        'After:\n– Thay toàn bộ bảng Chi tiết, mỗi lô 1 dòng ĐVT cơ sở.'),
       ('Đổi ĐVT kiểm kê', 'Change',
        'Before:\n– Lấy SL còn lại của lô trước dòng đó.\nDuring:\n– Phần nguyên SL / hệ số = 0 → “Số lượng không đủ để quy đổi!”, trả ĐVT cũ.\n'
        'After:\n– Đặt SL dòng; phần dư > 0 thêm dòng ĐVT cơ sở; dư 0 bỏ các dòng sau.'),
       ('Đổi Kho vật lý khi đã có Chi tiết', 'Change',
        'Before:\n– Bảng Chi tiết có dữ liệu.\nDuring:\n– Hiện hộp “Đổi kho vật lý”.\nAfter:\n– Đổi kho: xóa phạm vi và Chi tiết, nạp kho mới; Hủy: giữ kho cũ.'),
   ])

# ------------------------------------------------------------ 2.8 Lưu và gửi
fr(8, 'Lưu và gửi phiếu (chuyển Đang kiểm)', usecase=('FR-08', 'Lưu và gửi', 'action', A_LP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lưu và gửi phiếu sang bước kiểm',
       mota='Ở màn Tạo hoặc Sửa, nút Lưu và gửi lưu phiếu và chuyển thẳng sang trạng thái Đang kiểm: phiếu hiện với người có quyền '
            'xem, người tạo bắt đầu nhập kết quả, các vị trí của phiếu bị khóa kiểm kho. Không có hộp xác nhận và không gửi thông báo '
            '(giữ như hệ thống cũ).',
       tacnhan='Người dùng có quyền thực hiện chức năng: %s (màn Tạo); người tạo phiếu Đang tạo (màn Sửa).' % Q1,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo, hoặc màn Sửa của phiếu Đang tạo do mình tạo.\n'
                '3. Đủ dữ liệu bắt buộc như mục 2.5.',
       chinh='1. Người dùng nhập đủ thông tin (như mục 2.5) và bấm Lưu và gửi.\n'
             '2. Hệ thống kiểm tra dữ liệu như nút Lưu.\n'
             '3. Hệ thống lưu phiếu trạng thái Đang kiểm (màn Tạo: sinh số phiếu, kế hoạch → Đã lập kiểm kê; màn Sửa: kiểm lại phiếu '
             'còn Đang tạo, đúng người tạo).\n'
             '4. Hệ thống ghi nhận lịch sử: màn Tạo “Tạo mới”; màn Sửa “Thay đổi thông tin” (nếu đổi dữ liệu) và “Thay đổi trạng '
             'thái” Đang tạo → Đang kiểm.\n'
             '5. Hệ thống hiển thị “Lưu và gửi thành công.” và chuyển về màn danh sách.',
       phu='• Thiếu dữ liệu → như mục 2.5, không lưu.\n'
           '• Phiếu đã bị đổi trạng thái / xóa ở tab khác → ' + CONFLICT + ' / ' + NOTFOUND + ', không lưu.\n'
           '• Không phải người tạo → ' + NOPERM + '.\n'
           '• Sau khi gửi phiếu không sửa / xóa được nữa; người tạo thấy nút Nhập kết quả.',
       dacbiet='Không hộp xác nhận; nút khóa trong lúc lưu. Vị trí của phiếu Đang kiểm bị chặn ở Phiếu điều chuyển vị trí và Phiếu nhập '
               'kho cho tới khi phiếu được duyệt kết quả.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới => Lưu và gửi', 'Gửi ngay khi tạo phiếu.'),
       (MENU + ' => Sửa => Lưu và gửi', 'Gửi phiếu Đang tạo đã lưu trước đó.')],
       shot=shot('10c_filled'), shot_caption='Nút Lưu và gửi ở chân màn Tạo phiếu'),
   ui=[
       ('Nút Lưu và gửi', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Màu chính, biểu tượng máy bay giấy', '- Rê chuột: “Lưu và gửi phiếu sang bước kiểm (trạng thái Đang kiểm)”', '- Khóa trong lúc lưu']),
       ('Các trường của form', 'Table/Grid', 'Enable', '–', 'Như mục 2.5', 'Như mục 2.5',
        '- Kho vật lý, Phạm vi, Chi tiết + ĐVT kiểm kê, Hội đồng — cùng điều kiện bắt buộc với nút Lưu.'),
       ('Nhãn trạng thái sau khi gửi', 'Badge', 'Read-only', '–', '–', 'Đang kiểm', '- Nhãn vàng “Đang kiểm” ở danh sách.'),
       ('Nút Nhập kết quả trên dòng', 'Icon Button', 'Read-only', '–', '–', 'Hiển thị với người tạo', '- Xuất hiện sau khi gửi (mục 2.12).'),
       ('Nút Sửa, Xóa trên dòng', 'Icon Button', 'Read-only', '–', '–', 'Ẩn sau khi gửi', '- Phiếu không còn Đang tạo.'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Lưu và gửi thành công.”'),
       ('Thông báo thiếu dữ liệu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + MISS),
       ('Thông báo xung đột', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + CONFLICT, '- ' + NOPERM]),
       ('Lỗi dưới từng ô', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Như mục 2.5 (Kho, Phạm vi, Chi tiết, Nhân viên, Chức vụ, ĐVT kiểm kê).'),
       ('Lịch sử sau khi gửi', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Mốc “Tạo mới” hoặc “Thay đổi trạng thái” Đang tạo → Đang kiểm.'),
       ('Khóa vị trí', 'Label', 'Read-only', '–', '–', 'Không hiển thị trên màn', '- Vị trí của phiếu bị đánh dấu đang kiểm kho ở màn khác (BR-10).'),
   ],
   ev=[
       ('Bấm Lưu và gửi (màn Tạo)', 'Click',
        'Before:\n– Kiểm tra quyền “%s”.\n– Nếu không có quyền → hiển thị %s và dừng xử lý.\n' % (Q1, NOPERM) + SAVE_DURING + '\n'
        'After:\n– Lưu phiếu trạng thái Đang kiểm, sinh số phiếu; có kế hoạch → kế hoạch Đã lập kiểm kê.\n'
        '– Ghi một dòng lịch sử “Tạo mới”.\n– Hiển thị “Lưu và gửi thành công.”, về danh sách.'),
       ('Bấm Lưu và gửi (màn Sửa)', 'Click',
        'Before:\n– Phiếu phải Đang tạo, nếu không → ' + CONFLICT + '; người bấm phải là người tạo, nếu không → ' + NOPERM + '.\n' + SAVE_DURING + '\n'
        'After:\n– Ghi đè dữ liệu, trạng thái Đang kiểm.\n– Ghi lịch sử “Thay đổi thông tin” (nếu có) + “Thay đổi trạng thái”.\n'
        '– Hiển thị “Lưu và gửi thành công.”, về danh sách.'),
       ('Mở lại phiếu đã gửi', 'System',
        'Before:\n– Phiếu Đang kiểm.\nAfter:\n– Danh sách / chi tiết không còn Sửa, Xóa; người tạo có Nhập kết quả.'),
       ('Màn khác kiểm vị trí', 'System',
        'Before:\n– Phiếu Đang kiểm / Chờ duyệt kết quả.\nAfter:\n– Phiếu điều chuyển vị trí không cho chọn vị trí; Phiếu nhập kho chặn nhập vào vị trí '
        'của phiếu Đang kiểm.'),
   ])

# ------------------------------------------------------------ 2.9 Sửa
fr(9, 'Chỉnh sửa phiếu kiểm kê', usecase=('FR-09', 'Chỉnh sửa phiếu', 'crud', A_LP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Chỉnh sửa phiếu kiểm kê theo vị trí',
       mota='Người tạo sửa phiếu còn Đang tạo: đổi kho / phạm vi và Lấy vị trí lại (phiếu lập tay), chỉnh ĐVT kiểm kê, sửa hội '
            'đồng; lưu giữ Đang tạo (Lưu) hoặc gửi luôn (Lưu và gửi, mục 2.8). Số phiếu, Ngày kiểm kê, Kế hoạch kiểm kê không sửa '
            'được; phiếu có kế hoạch thì Kho và Phạm vi cũng khóa.',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo phiếu.\n3. Phiếu đang ở trạng thái Đang tạo.',
       chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
             '2. Hệ thống mở màn “Sửa phiếu kiểm kê theo vị trí: <số phiếu>”, điền sẵn dữ liệu đã lưu.\n'
             '3. Người dùng sửa thông tin.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống kiểm lại phiếu còn Đang tạo và đúng người tạo, kiểm tra dữ liệu như mục 2.5.\n'
             '6. Hệ thống ghi đè phạm vi, chi tiết + ĐVT kiểm kê, hội đồng; cập nhật người / ngày cập nhật; giữ nguyên kế hoạch.\n'
             '7. Hệ thống ghi nhận “Thay đổi thông tin” trong lịch sử (cũ → mới của Kho vật lý, Nhà, Dãy, Khoang, Vị trí, Danh sách '
             'hàng tồn theo lô, Hội đồng) — không đổi gì thì không ghi.\n'
             '8. Hệ thống hiển thị “Lưu thành công.” và chuyển về màn danh sách.',
       phu='• Mở màn Sửa của phiếu không còn Đang tạo / không phải người tạo → tự chuyển sang màn chi tiết.\n'
           '• Phiếu ngoài phạm vi / đã bị xóa → trang “Không tìm thấy trang”.\n'
           '• Lưu khi phiếu vừa bị gửi / xóa ở tab khác → ' + CONFLICT + ' hoặc ' + NOTFOUND + '.\n'
           '• Thiếu dữ liệu → như mục 2.5.\n'
           '• Quay lại khi đã sửa → hộp “Thông tin chưa lưu”; không sửa gì → về danh sách ngay.',
       dacbiet='Phiếu không có trường duy nhất nên không kiểm trùng. Màn Sửa không có nút Lưu và tiếp tục, không có ô chọn kế hoạch '
               '(rê nhãn Kế hoạch kiểm kê: “Kế hoạch kiểm kê chỉ chọn được lúc tạo phiếu, khi sửa phiếu giữ nguyên kế hoạch đã chọn.”).'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('12_edit'), shot_caption='Màn Sửa phiếu kiểm kê lập từ kế hoạch (kho, phạm vi khóa)'),
   ui=FORM_UI[:2] + [
       ('Số phiếu', 'Textbox', 'Disable', '<mã công ty>-KKVT-NNNNN', '–', 'Theo dữ liệu', '- Không sửa được.'),
       ('Ô Kế hoạch kiểm kê', 'Link', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Không đổi được', '- Mã là liên kết mở kế hoạch ở tab mới']),
       ('Ngày kiểm kê', 'Textbox', 'Disable', 'dd/mm/yyyy', 'Có', 'Ngày của phiếu', '- Không sửa được.'),
   ] + FORM_UI[5:17] + FORM_UI[18:],
   ev=[
       ('Mở màn Sửa', 'System',
        'Before:\n– Kiểm tra phạm vi xem, ngoài phạm vi → trang “Không tìm thấy trang”.\n'
        '– Kiểm tra người tạo + Đang tạo, nếu không → chuyển sang màn chi tiết.\nAfter:\n– Điền sẵn dữ liệu; chưa tính là đã thay đổi.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Phiếu phải còn Đang tạo, nếu không → ' + CONFLICT + '.\n– Người bấm phải là người tạo, nếu không → ' + NOPERM + '.\n' + SAVE_DURING + '\n'
        'After:\n– Ghi đè phạm vi, chi tiết, hội đồng; cập nhật người / ngày cập nhật.\n'
        '– Ghi một dòng lịch sử “Thay đổi thông tin” (cũ → mới) nếu có thay đổi.\n– Hiển thị “Lưu thành công.”, về danh sách.'),
       ('Bấm Lưu và gửi', 'Click', 'Before:\n– Như Lưu.\nDuring:\n– Như mục 2.8.\nAfter:\n– Như mục 2.8.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu với lúc mở.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu, không ghi lịch sử; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.10 Xóa
fr(10, 'Xóa phiếu kiểm kê', usecase=('FR-10', 'Xóa phiếu', 'action', A_LP),
   rule=('- Hộp thoại xác nhận Xóa và Thông báo.', 'delete'),
   intro=dict(
       ten='Xóa phiếu kiểm kê theo vị trí',
       mota='Người tạo xóa hẳn phiếu còn Đang tạo cùng toàn bộ dữ liệu con (phạm vi, chi tiết, dòng ĐVT kiểm kê, hội đồng). Phiếu lập '
            'từ kế hoạch mà kế hoạch đang Đã lập kiểm kê → kế hoạch trở về Đang kiểm để lập lại được phiếu (lệch hệ thống cũ có chủ đích).',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo.\n3. Phiếu đang Đang tạo.',
       chinh='1. Người dùng bấm Xóa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa” với nội dung “Bạn có chắc muốn xóa bản ghi này không?”.\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm lại phiếu còn Đang tạo và đúng người tạo.\n'
             '5. Hệ thống ghi nhận hành động “Xóa” trong lịch sử; nếu kế hoạch cha Đã lập kiểm kê → chuyển Đang kiểm, ghi “Thay đổi '
             'trạng thái” vào lịch sử kế hoạch (ghi chú “Xóa phiếu kiểm kê <số phiếu>.”).\n'
             '6. Hệ thống xóa phiếu và mọi dữ liệu con, hiển thị “Xóa thành công.”; ở danh sách nạp lại, ở chi tiết quay về danh sách.',
       phu='• Bấm Hủy / (x) → đóng hộp, không xóa.\n'
           '• Phiếu vừa bị gửi ở tab khác → ' + CONFLICT + ', không xóa.\n'
           '• Phiếu đã bị xóa ở tab khác → ' + NOTFOUND + '.\n'
           '• Kế hoạch cha đã Hoàn thành → giữ nguyên kế hoạch.',
       dacbiet='Nút Xóa khóa trong lúc đang xóa. Xóa là xóa hẳn, không khôi phục.'),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp Xác nhận xóa phiếu',
               note='Hộp xác nhận được mở ngay trên màn hình danh sách hoặc màn chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Xóa trên dòng', 'Icon Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện', ['- Thùng rác đỏ', '- Chỉ phiếu Đang tạo của mình']),
       ('Nút Xóa ở màn chi tiết', 'Button', 'Enable / Ẩn', 'Ẩn khi không đủ điều kiện', '- Nút đỏ ở chân màn chi tiết.'),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Hiển thị', '- “Xác nhận xóa”.'),
       ('Nội dung hộp', 'Label', 'Hiển thị', 'Hiển thị', '- “Bạn có chắc muốn xóa bản ghi này không?”'),
       ('Nút Xóa (xác nhận)', 'Button', 'Enable', 'Hiển thị', '- Nút đỏ; bấm → xóa phiếu.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không xóa.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống Hủy.'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', 'Ẩn', '- “Xóa thành công.”'),
       ('Thông báo thất bại', 'Toast / Alert', 'Hiển thị', 'Ẩn', ['- ' + CONFLICT, '- ' + NOTFOUND, '- “Xóa thất bại.”']),
       ('Danh sách sau xóa', 'Table/Grid', 'Read-only', 'Theo dữ liệu', '- Phiếu biến mất, tổng N giảm 1.'),
       ('Kế hoạch cha sau xóa', 'Badge', 'Read-only', 'Theo dữ liệu', '- Đã lập kiểm kê → Đang kiểm (ở màn Kế hoạch).'),
   ],
   ev=[
       ('Bấm Xóa', 'Click', 'Before:\n– Nút chỉ hiện với phiếu Đang tạo của mình.\nAfter:\n– Hiện hộp Xác nhận xóa.'),
       ('Bấm Xóa (xác nhận)', 'Click',
        'Before:\n– Kiểm tra phạm vi xem, ngoài phạm vi → ' + NOTFOUND + '.\n'
        '– Phiếu phải còn Đang tạo, nếu không → ' + CONFLICT + '; không phải người tạo → ' + NOPERM + '.\n'
        'During:\n– Xóa trọn gói phiếu và dữ liệu con; lỗi thì không xóa gì.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Xóa”; kế hoạch cha Đã lập kiểm kê → Đang kiểm.\n– Hiển thị “Xóa thành công.”; nạp lại / về danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nAfter:\n– Đóng hộp, dữ liệu giữ nguyên.'),
       ('Màn Kế hoạch sau khi xóa', 'System', 'Before:\n– Phiếu lập từ kế hoạch Đã lập kiểm kê.\nAfter:\n– Kế hoạch Đang kiểm, có lại nút Lập phiếu kiểm kê.'),
   ])

# ------------------------------------------------------------ 2.11 Chi tiết
fr(11, 'Xem chi tiết phiếu kiểm kê',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu kiểm kê theo vị trí',
       mota='Màn hiển thị thông tin chung, file đính kèm (khi có), phạm vi đã tick, bảng Chi tiết kèm ĐVT kiểm kê và kết quả (Thực kiểm, '
            'Chênh lệch, Ghi chú, Tổng kiểm kê — khi đã / đang nhập kết quả), hội đồng và khối Lịch sử. Chân màn có nút theo cờ: Lưu '
            'kết quả, Duyệt kết quả, Không duyệt, Tạo phiếu điều chuyển vị trí, Hoàn thành, Sửa, Xóa, In, Xuất Excel, Quay lại.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu trong phạm vi xem, hoặc người dùng đang có việc trên phiếu (Ban kiểm soát '
                'với phiếu Chờ duyệt kết quả, người xử lý với phiếu Chờ xử lý).',
       chinh='1. Người dùng bấm Số phiếu ở danh sách (hoặc bấm thông báo / liên kết ở màn Phiếu điều chuyển vị trí).\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết phiếu kiểm kê theo vị trí: <số phiếu>”.\n'
             '4. Hệ thống hiển thị Thông tin chung, File đính kèm, Phạm vi, Chi tiết, Hội đồng, khối Lịch sử (thu gọn, có số mốc).',
       phu='• Ngoài phạm vi / không tồn tại → trang “Không tìm thấy trang”.\n'
           '• Phiếu Đang tạo của người khác → coi như ngoài phạm vi.\n'
           '• Phiếu chưa có file và không đang nhập kết quả → không hiện khối File đính kèm.\n'
           '• Bấm Quay lại → về danh sách, khôi phục bộ lọc (trong 10 phút).',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết phiếu kiểm kê Hoàn thành'),
   extra=[(shot('17b_detail_full'), 'Chi tiết đầy đủ: bảng kết quả, hội đồng, khối Lịch sử')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Chi tiết phiếu kiểm kê theo vị trí: <số phiếu>” (không kèm nhãn trạng thái).'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Số phiếu', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- Mã phiếu.'),
       ('Kế hoạch kiểm kê', 'Link', 'Read-only', '–', 'Theo dữ liệu', '- Mã kế hoạch, bấm → tab mới; trống nếu lập tay.'),
       ('Ngày kiểm kê', 'Textbox', 'Disable', 'dd/mm/yyyy', 'Theo dữ liệu', '- Ngày của phiếu.'),
       ('Kho vật lý', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- Tên kho.'),
       ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Ẩn khi chưa có file',
        ['- STT, tên file (bấm để xem / tải), dung lượng', '- Chỉ sửa được ở bước Nhập kết quả (mục 2.12)']),
       ('Khối Phạm vi kiểm kê', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- 4 cột, mục đã tick được tích, không bấm được.'),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột như màn Tạo + ĐVT kiểm kê (chữ)', '- Khi đã nhập kết quả: thêm Thực kiểm, Chênh lệch (khác 0 chữ đỏ), Ghi chú, Tổng kiểm kê']),
       ('Bảng Hội đồng kiểm kê', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- STT, Nhân viên, Chức vụ (ô khóa).'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', ['- Số mốc cạnh tiêu đề', '- Nút Xem lịch sử / Thu gọn, Làm mới, Bộ lọc']),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Phiếu Đang tạo của mình → màn Sửa.'),
       ('Nút Lưu kết quả', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Đang kiểm + người tạo (mục 2.12).'),
       ('Nút Duyệt kết quả', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Chờ duyệt kết quả + Q2 (mục 2.13).'),
       ('Nút Không duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Chờ duyệt kết quả + Q2 (mục 2.14).'),
       ('Nút Tạo phiếu điều chuyển vị trí', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Chờ xử lý + Q3 + còn dòng thiếu (mục 2.15).'),
       ('Nút Hoàn thành', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Chờ xử lý + Q3 + không còn dòng cần điều chuyển.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Cửa sổ Xem trước (mục 2.16).'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', '- Tải file Excel phiếu (mục 2.17).'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Phiếu Đang tạo của mình (mục 2.10).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn danh sách.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → trang “Không tìm thấy trang”.\n'
        'During:\n– Lấy dữ liệu phiếu, cấu trúc kho, cờ nút.\nAfter:\n– Hiển thị màn, nút theo cờ; chưa tính là đã thay đổi.'),
       ('Bấm Xem lịch sử', 'Click', 'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở rộng khối, hiện các mốc (mục 2.18).'),
       ('Bấm mã kế hoạch', 'Click', 'Before:\n– Phiếu có kế hoạch.\nAfter:\n– Mở chi tiết kế hoạch ở tab mới.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Đang nhập kết quả mà có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Về danh sách, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.12 Nhập kết quả
fr(12, 'Nhập kết quả kiểm kê (Lưu kết quả)', usecase=('FR-12', 'Nhập kết quả kiểm kê', 'crud', A_LP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Nhập kết quả thực kiểm và gửi Ban kiểm soát',
       mota='Ở màn chi tiết của phiếu Đang kiểm, người tạo nhập Thực kiểm cho từng dòng ĐVT kiểm kê, Ghi chú cho dòng có chênh lệch, '
            'tick Tổng kiểm kê nếu cần, đính kèm file biên bản rồi bấm Lưu kết quả: phiếu chuyển Chờ duyệt kết quả và Ban kiểm soát '
            'cùng công ty nhận thông báo.',
       tacnhan='Người dùng có quyền thực hiện chức năng: người tạo phiếu, phiếu đang ở trạng thái Đang kiểm.',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo phiếu.\n3. Phiếu đang Đang kiểm.',
       chinh='1. Người tạo bấm Nhập kết quả ở danh sách hoặc mở chi tiết phiếu.\n'
             '2. Hệ thống hiện thêm cột Thực kiểm * (mặc định = SL khi nhập lần đầu), Chênh lệch, Ghi chú, Tổng kiểm kê và khối File '
             'đính kèm có nút Thêm tài liệu.\n'
             '3. Người dùng sửa Thực kiểm; Chênh lệch tự tính = Thực kiểm − SL (khác 0 chữ đỏ); nhập Ghi chú cho dòng chênh lệch.\n'
             '4. Người dùng đính kèm file (bắt buộc nếu phiếu chưa có file) rồi bấm Lưu kết quả.\n'
             '5. Hệ thống kiểm tra đủ mọi dòng, ghi Thực kiểm, Chênh lệch (máy chủ tự tính), Ghi chú, Tổng kiểm kê (bỏ khi chênh = 0), '
             'nối file mới vào danh sách file.\n'
             '6. Hệ thống chuyển phiếu Chờ duyệt kết quả, ghi lịch sử “Thay đổi thông tin” (kết quả, file) và “Thay đổi trạng thái” '
             'Đang kiểm → Chờ duyệt kết quả.\n'
             '7. Hệ thống gửi thông báo “[KKVT] Chờ duyệt: <số phiếu>” (Người nhập kết quả, Kho, Kế hoạch) cho người có quyền “%s” '
             'cùng công ty người thao tác.\n'
             '8. Hệ thống hiển thị “Lưu kết quả thành công.” và về danh sách.' % Q2,
       phu='• Thiếu Thực kiểm → “Bắt buộc phải nhập” dưới ô; vượt 999,999,999 → “Giá trị nhập vào không được vượt quá 999,999,999.”; '
           'âm → “Không được nhỏ hơn 0”.\n'
           '• Có chênh lệch mà thiếu Ghi chú → “Bắt buộc phải nhập”; Ghi chú quá 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”.\n'
           '• Phiếu chưa có file và không đính file → “File đính kèm – Vui lòng chọn file đính kèm.”.\n'
           '• File sai loại → “Chỉ nhận file pdf, png, jpg, jpeg, doc, docx, xls, xlsx”; quá 20MB → “Dung lượng tối đa 20MB”.\n'
           '• Phiếu đã đổi trạng thái → ' + CONFLICT + '.\n'
           '• Rời màn khi đã nhập → hộp “Thông tin chưa lưu”.',
       dacbiet='Lỗi hiện cùng lúc ở mọi ô, thông báo ' + MISS + '. Nút Lưu kết quả khóa trong lúc lưu. Gõ Thực kiểm chỉ vẽ lại ô của '
               'dòng đó (phiếu vài trăm lô không giật). Xóa file đã lưu chỉ được khi phiếu còn Đang kiểm. Thông báo lỗi gửi không làm '
               'hỏng việc lưu.'),
   layout=dict(menu=MENU + ' => Nhập kết quả', shot=shot('14_result'), shot_caption='Màn chi tiết phiếu Đang kiểm ở bước Nhập kết quả'),
   extra=[(shot('14b_result_validate_full'), 'Lỗi “Bắt buộc phải nhập” ở Ghi chú khi dòng có chênh lệch')],
   ui=[
       ('Nút Nhập kết quả trên dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Đang kiểm + người tạo; bấm → mở chi tiết.'),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, png, jpg, jpeg, doc, docx, xls, xlsx; ≤ 20MB', 'Có khi chưa có file', 'File đã lưu',
        ['- Nút Thêm tài liệu: chọn file, tải lên ngay', '- Mỗi file: tên, dung lượng, nút thay / xóa',
         '- Lỗi: “File đính kèm – Vui lòng chọn file đính kèm.”']),
       ('Cột Thực kiểm', 'Textbox', 'Enable', '0 – 999,999,999, tối đa 2 số lẻ', 'Có', '= SL (lần đầu)',
        ['- Gợi ý “Nhập thực kiểm”', '- Lỗi: “Bắt buộc phải nhập” / “Vui lòng nhập số hợp lệ.” / “Không được nhỏ hơn 0” / “Giá trị nhập vào không được vượt quá 999,999,999.”']),
       ('Cột Chênh lệch', 'Label', 'Read-only', 'Số', '–', '0', ['- = Thực kiểm − SL', '- Khác 0: chữ đỏ']),
       ('Cột Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Có khi Chênh lệch ≠ 0', 'Trống',
        ['- Gợi ý “Nhập ghi chú”', '- Lỗi: “Bắt buộc phải nhập” / “Vui lòng nhập tối đa 255 ký tự.”']),
       ('Cột Tổng kiểm kê', 'Checkbox', 'Enable / Ẩn', '–', 'Không', 'Chưa tick', '- Chỉ hiện ở dòng Chênh lệch ≠ 0; về 0 thì tự bỏ tick.'),
       ('Nhãn Công ty (Cộng), Lô (SL)', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '- Phần trong ngoặc chữ đỏ.'),
       ('Nút Lưu kết quả', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Rê chuột: “Lưu kết quả kiểm kê và gửi Ban kiểm soát duyệt”', '- Khóa trong lúc lưu']),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Có thay đổi → hộp “Thông tin chưa lưu”.'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Lưu kết quả thành công.”'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + MISS, '- ' + CONFLICT, '- “Đã có lỗi xảy ra.”']),
       ('Thông báo cho Ban kiểm soát', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tiêu đề “[KKVT] Chờ duyệt: <số phiếu>”', '- Ghi chú: Người nhập kết quả, Kho, Kế hoạch', '- Bấm → mở chi tiết phiếu']),
   ],
   ev=[
       ('Gõ Thực kiểm', 'Change',
        'Before:\n– Chỉ nhận số, tối đa 2 số lẻ.\nAfter:\n– Tính lại Chênh lệch; về 0 → bỏ tick Tổng kiểm kê, xóa lỗi Ghi chú.'),
       ('Bấm Thêm tài liệu', 'Click',
        'Before:\n– Đúng loại file, ≤ 20MB, nếu không → “Chỉ nhận file pdf, png, jpg, jpeg, doc, docx, xls, xlsx” / “Dung lượng tối đa 20MB”.\n'
        'After:\n– Tải file lên, hiện trong danh sách chờ lưu.'),
       ('Bấm Lưu kết quả', 'Click',
        'Before:\n– Phiếu phải Đang kiểm, nếu không → ' + CONFLICT + '; không phải người tạo → ' + NOPERM + '.\n'
        'During:\n– Thực kiểm trống / sai → câu lỗi dưới ô.\n– Chênh lệch ≠ 0 mà Ghi chú trống → “Bắt buộc phải nhập”.\n'
        '– Phiếu chưa có file → “File đính kèm – Vui lòng chọn file đính kèm.”.\n'
        '– Thiếu dòng → “Thực kiểm – Vui lòng nhập kết quả cho tất cả các dòng. Vui lòng tải lại trang.”.\n' + ERR + '\n'
        'After:\n– Ghi kết quả, nối file; phiếu Chờ duyệt kết quả.\n– Ghi lịch sử “Thay đổi thông tin” + “Thay đổi trạng thái”.\n'
        '– Gửi thông báo “[KKVT] Chờ duyệt” cho người có quyền “%s” cùng công ty.\n– Hiển thị “Lưu kết quả thành công.”, về danh sách.' % Q2),
       ('Xóa file đã lưu', 'Click',
        'Before:\n– Phiếu còn Đang kiểm.\nDuring:\n– File không thuộc phiếu → “File không nằm trong phiếu này”.\n'
        'After:\n– Xóa file, ghi lịch sử “Thay đổi thông tin” (File đính kèm), “Xóa file thành công”.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– So kết quả, file với lúc mở.\nAfter:\n– Có thay đổi → hộp “Thông tin chưa lưu”; không → về danh sách.'),
   ])

# ------------------------------------------------------------ 2.13 Duyệt
fr(13, 'Duyệt kết quả kiểm kê', usecase=('FR-13', 'Duyệt kết quả', 'action', A_BKS),
   rule=('- Màn Xem chi tiết, Thông báo và Phân quyền.', 'detail'),
   intro=dict(
       ten='Ban kiểm soát duyệt kết quả kiểm kê',
       mota='Ở phiếu Chờ duyệt kết quả, người có quyền “%s” bấm Duyệt kết quả, nhập ghi chú (tùy chọn) trong popup rồi xác nhận. Còn '
            'dòng chênh lệch thiếu → phiếu Chờ xử lý và người có quyền “%s” nhận thông báo; không thiếu → phiếu Hoàn thành và kế '
            'hoạch cha cũng Hoàn thành.' % (Q2, Q3),
       tacnhan='Người dùng có quyền thực hiện chức năng: %s.' % Q2,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có quyền “%s”.\n3. Phiếu đang Chờ duyệt kết quả.' % Q2,
       chinh='1. Người dùng bấm Duyệt kết quả trên dòng (mở chi tiết) hoặc mở chi tiết phiếu từ thông báo.\n'
             '2. Người dùng bấm Duyệt kết quả ở chân màn chi tiết.\n'
             '3. Hệ thống mở popup “Duyệt kết quả kiểm kê” (Phiếu: <số phiếu>) với ô Ghi chú duyệt.\n'
             '4. Người dùng nhập ghi chú (không bắt buộc) và bấm Duyệt kết quả.\n'
             '5. Hệ thống kiểm lại trạng thái + quyền, ghi người duyệt, ngày duyệt, ghi chú duyệt.\n'
             '6. Còn dòng Chênh lệch < 0 → phiếu Chờ xử lý, gửi thông báo “[KKVT] Đã duyệt: <số phiếu>” (Người duyệt, “Có chênh lệch '
             'thiếu cần xử lý”, Kho, Kế hoạch, Ghi chú duyệt) cho người có quyền “%s” cùng công ty; không → phiếu Hoàn thành, kế hoạch '
             'cha Hoàn thành (lịch sử kế hoạch “Phiếu kiểm kê <số phiếu> được duyệt kết quả.”).\n'
             '7. Hệ thống ghi lịch sử “Duyệt” (Trạng thái cũ → mới, ghi chú duyệt), hiển thị “Duyệt kết quả thành công.”, về danh sách.' % Q3,
       phu='• Bấm Hủy / (x) ở popup → đóng popup, không duyệt.\n'
           '• Phiếu đã được người khác duyệt / không duyệt → ' + CONFLICT + '.\n'
           '• Không có quyền → nút không hiện; vẫn gửi → ' + NOPERM + '.\n'
           '• Ghi chú duyệt quá 5000 ký tự → “Ghi chú duyệt – Tối đa 5000 ký tự.”.',
       dacbiet='Popup chính là bước xác nhận (không hỏi thêm). Nút khóa trong lúc gửi. Ghi chú duyệt không hiện trên màn chi tiết, chỉ '
               'nằm ở Lịch sử, bản in (Nhận xét, đánh giá) và file Excel.'),
   layout=dict(menu=MENU + ' => Duyệt kết quả', shot=shot('15_approve'), shot_caption='Popup Duyệt kết quả kiểm kê',
               note='Popup mở trên màn chi tiết phiếu Chờ duyệt kết quả theo đường dẫn ở trên.'),
   extra=[(shot('15_wait_detail'), 'Màn chi tiết phiếu Chờ duyệt kết quả: nút Duyệt kết quả, Không duyệt')],
   ui=[
       ('Nút Duyệt kết quả trên dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Chờ duyệt kết quả + Q2; bấm → mở chi tiết.'),
       ('Nút Duyệt kết quả ở chi tiết', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Màu chính, biểu tượng dấu tích.'),
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', ['- “Duyệt kết quả kiểm kê”', '- Dòng phụ “Phiếu: <số phiếu>”']),
       ('Ô Ghi chú duyệt', 'Textarea', 'Enable', '0–5000 ký tự', 'Không', 'Trống', ['- Gợi ý “Nhập ghi chú duyệt”', '- 3 dòng']),
       ('Nút Duyệt kết quả trong popup', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Xác nhận duyệt; khóa trong lúc gửi.'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Biểu tượng mũi tên trái; đóng popup.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống Hủy.'),
       ('Cột Người duyệt, Ngày duyệt', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Cập nhật sau khi duyệt.'),
       ('Nhãn trạng thái sau duyệt', 'Badge', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Có thiếu: Chờ xử lý (vàng)', '- Không thiếu: Hoàn thành (xanh)']),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Duyệt kết quả thành công.”'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + CONFLICT, '- ' + NOPERM, '- “Ghi chú duyệt – Tối đa 5000 ký tự.”']),
       ('Thông báo cho người xử lý', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “[KKVT] Đã duyệt: <số phiếu>”', '- Chỉ khi còn chênh lệch thiếu', '- Bấm → mở chi tiết phiếu']),
   ],
   ev=[
       ('Bấm Duyệt kết quả (chi tiết)', 'Click', 'Before:\n– Nút chỉ hiện khi Chờ duyệt kết quả + quyền “%s”.\nAfter:\n– Mở popup, con trỏ ở ô Ghi chú duyệt.' % Q2),
       ('Bấm Duyệt kết quả (popup)', 'Click',
        'Before:\n– Kiểm tra quyền “%s”; không có → %s.\n– Phiếu phải Chờ duyệt kết quả, nếu không → %s.\n' % (Q2, NOPERM, CONFLICT) +
        'During:\n– Ghi chú > 5000 ký tự → “Ghi chú duyệt – Tối đa 5000 ký tự.”.\n' + ERR + '\n'
        'After:\n– Ghi người / ngày / ghi chú duyệt; Chờ xử lý (có thiếu) hoặc Hoàn thành (+ kế hoạch Hoàn thành).\n'
        '– Ghi lịch sử “Duyệt”; có thiếu → gửi thông báo “[KKVT] Đã duyệt” cho người có quyền “%s”.\n'
        '– Hiển thị “Duyệt kết quả thành công.”, về danh sách.' % Q3),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nAfter:\n– Đóng popup, phiếu giữ Chờ duyệt kết quả.'),
       ('Bấm thông báo (người xử lý)', 'Click', 'Before:\n– Người nhận có quyền “%s”.\nAfter:\n– Mở chi tiết phiếu Chờ xử lý (mục 2.15).' % Q3),
   ])

# ------------------------------------------------------------ 2.14 Không duyệt
fr(14, 'Không duyệt kết quả kiểm kê', usecase=('FR-14', 'Không duyệt', 'action', A_BKS),
   rule=('- Màn Xem chi tiết, Thông báo và Phân quyền.', 'detail'),
   intro=dict(
       ten='Ban kiểm soát không duyệt kết quả kiểm kê',
       mota='Ở phiếu Chờ duyệt kết quả, người có quyền “%s” bấm Không duyệt, nhập lý do (bắt buộc) trong popup rồi xác nhận: phiếu '
            'trả về Đang kiểm để người tạo nhập lại kết quả; người tạo nhận thông báo kèm lý do.' % Q2,
       tacnhan='Người dùng có quyền thực hiện chức năng: %s.' % Q2,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có quyền “%s”.\n3. Phiếu đang Chờ duyệt kết quả.' % Q2,
       chinh='1. Người dùng mở chi tiết phiếu, bấm Không duyệt (nút đỏ).\n'
             '2. Hệ thống mở popup “Không duyệt kết quả kiểm kê” (Phiếu: <số phiếu>) với ô Ghi chú duyệt * bắt buộc.\n'
             '3. Người dùng nhập lý do và bấm Không duyệt.\n'
             '4. Hệ thống kiểm lại trạng thái + quyền, ghi lý do, đưa phiếu về Đang kiểm, bỏ cờ đã nhập kết quả (kết quả cũ vẫn giữ để sửa).\n'
             '5. Hệ thống ghi lịch sử “Từ chối” (Trạng thái Chờ duyệt kết quả → Đang kiểm, lý do).\n'
             '6. Hệ thống gửi thông báo “[KKVT] Từ chối: <số phiếu>” (Người từ chối, Lý do) cho người tạo phiếu.\n'
             '7. Hệ thống hiển thị “Không duyệt kết quả thành công.”, về danh sách.',
       phu='• Bỏ trống lý do → lỗi đỏ “Vui lòng nhập lý do không duyệt” dưới ô, không gửi (máy chủ: “Ghi chú duyệt – Vui lòng nhập lý do không duyệt.”).\n'
           '• Lý do quá 5000 ký tự → “Ghi chú duyệt – Tối đa 5000 ký tự.”.\n'
           '• Bấm Hủy / (x) → đóng popup, không đổi gì.\n'
           '• Phiếu đã được duyệt / không duyệt ở tab khác → ' + CONFLICT + '.',
       dacbiet='Popup nhập lý do là bước xác nhận. Lý do được bỏ khoảng trắng đầu / cuối; chỉ khoảng trắng coi như trống. Sau Không '
               'duyệt, nút Nhập kết quả hiện lại cho người tạo, cột Thực kiểm hiện giá trị đã nhập trước đó.'),
   layout=dict(menu=MENU + ' => Không duyệt', shot=shot('15b_reject'), shot_caption='Popup Không duyệt kết quả kiểm kê khi bỏ trống lý do',
               note='Popup mở trên màn chi tiết phiếu Chờ duyệt kết quả theo đường dẫn ở trên.'),
   ui=[
       ('Nút Không duyệt ở chi tiết', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Nút đỏ, biểu tượng dấu x tròn.'),
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', ['- “Không duyệt kết quả kiểm kê”', '- Dòng phụ “Phiếu: <số phiếu>”']),
       ('Ô Ghi chú duyệt', 'Textarea', 'Enable', '1–5000 ký tự', 'Có', 'Trống',
        ['- Gợi ý “Nhập lý do không duyệt”', '- Lỗi: “Vui lòng nhập lý do không duyệt” (viền đỏ)']),
       ('Nút Không duyệt trong popup', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Nút đỏ; khóa trong lúc gửi.'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống Hủy.'),
       ('Nhãn trạng thái sau không duyệt', 'Badge', 'Read-only', '–', '–', 'Đang kiểm', '- Nhãn vàng “Đang kiểm”.'),
       ('Nút Nhập kết quả sau không duyệt', 'Icon Button', 'Read-only', '–', '–', 'Hiển thị với người tạo', '- Người tạo nhập lại kết quả.'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Không duyệt kết quả thành công.”'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + CONFLICT, '- ' + NOPERM]),
       ('Thông báo cho người tạo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “[KKVT] Từ chối: <số phiếu>”', '- Ghi chú: Người từ chối, Lý do', '- Bấm → mở chi tiết phiếu']),
   ],
   ev=[
       ('Bấm Không duyệt (chi tiết)', 'Click', 'Before:\n– Nút chỉ hiện khi Chờ duyệt kết quả + quyền “%s”.\nAfter:\n– Mở popup Không duyệt.' % Q2),
       ('Bấm Không duyệt (popup)', 'Click',
        'Before:\n– Lý do trống → “Vui lòng nhập lý do không duyệt”, dừng xử lý.\n– Kiểm tra quyền “%s”; không có → %s.\n'
        '– Phiếu phải Chờ duyệt kết quả, nếu không → %s.\n' % (Q2, NOPERM, CONFLICT) +
        'During:\n– Lý do > 5000 ký tự → “Ghi chú duyệt – Tối đa 5000 ký tự.”.\n' + ERR + '\n'
        'After:\n– Phiếu Đang kiểm, ghi lý do.\n– Ghi lịch sử “Từ chối”.\n– Gửi thông báo “[KKVT] Từ chối” cho người tạo.\n'
        '– Hiển thị “Không duyệt kết quả thành công.”, về danh sách.'),
       ('Gõ lý do sau khi báo lỗi', 'Change', 'Before:\n– Đang có lỗi đỏ.\nAfter:\n– Lỗi biến mất khi ô có chữ.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nAfter:\n– Đóng popup, phiếu giữ Chờ duyệt kết quả.'),
   ])

# ------------------------------------------------------------ 2.15 Xử lý
fr(15, 'Xử lý phiếu (Tổng kiểm kê, Điều chuyển, Hoàn thành)', usecase=('FR-15', 'Xử lý phiếu', 'action', A_XL),
   rule=('- Màn Xem chi tiết, Thông báo và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xử lý chênh lệch thiếu của phiếu Chờ xử lý',
       mota='Người có quyền “%s” xử lý phiếu Chờ xử lý: tick Tổng kiểm kê cho dòng thiếu không cần điều chuyển (lưu ngay), bấm Tạo '
            'phiếu điều chuyển vị trí để điều chuyển các dòng thiếu còn lại, hoặc bấm Hoàn thành khi không còn dòng cần điều chuyển. '
            'Điều chuyển xử lý hết chênh lệch thì phiếu tự Hoàn thành cùng kế hoạch cha.' % Q3,
       tacnhan='Người dùng có quyền thực hiện chức năng: %s.' % Q3,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có quyền “%s”.\n3. Phiếu đang Chờ xử lý.' % Q3,
       chinh='1. Người dùng bấm Tạo phiếu điều chuyển vị trí / Xử lý trên dòng, hoặc mở chi tiết phiếu từ thông báo.\n'
             '2. Hệ thống hiển thị bảng kết quả; ô Tổng kiểm kê ở dòng có chênh lệch bấm được.\n'
             '3. Người dùng tick / bỏ tick Tổng kiểm kê một dòng; hệ thống lưu ngay, báo “Cập nhật thành công.”, ghi lịch sử “Thay đổi '
             'thông tin” và nạp lại nút.\n'
             '4. Còn dòng thiếu chưa tick, chưa điều chuyển hết → nút Tạo phiếu điều chuyển vị trí: mở màn Tạo phiếu điều chuyển vị '
             'trí đã nạp kho và các dòng thiếu của phiếu.\n'
             '5. Không còn dòng cần điều chuyển → nút Hoàn thành; bấm → hộp “Xác nhận hoàn thành”, bấm Hoàn thành.\n'
             '6. Hệ thống đổi phiếu Hoàn thành, ghi lịch sử “Thay đổi trạng thái” Chờ xử lý → Hoàn thành, hiển thị “Hoàn thành phiếu '
             'kiểm kê thành công.”, về danh sách.',
       phu='• Bấm Hủy ở hộp xác nhận → không đổi gì.\n'
           '• Hoàn thành khi vẫn còn dòng cần điều chuyển (tab khác bỏ tick) → “Còn dòng chênh lệch thiếu chưa xử lý. Vui lòng tạo '
           'phiếu điều chuyển vị trí hoặc tick \"Tổng kiểm kê\".”.\n'
           '• Tick ở dòng không chênh lệch → “Tổng kiểm kê – Chỉ áp dụng cho dòng có chênh lệch.”; lưu lỗi → trả ô về như cũ.\n'
           '• Phiếu đã đổi trạng thái → ' + CONFLICT + '.\n'
           '• Phiếu điều chuyển vị trí lập từ phiếu này được Điều chuyển và xử lý hết → phiếu tự Hoàn thành, kế hoạch cha Hoàn thành.',
       dacbiet='Bấm Hoàn thành ở bước Xử lý KHÔNG cập nhật kế hoạch cha (giữ như hệ thống cũ). Tick Tổng kiểm kê lưu ngay, không tính '
               'là “chưa lưu”. Ô tick khóa trong lúc đang lưu.'),
   layout=dict(menu=MENU + ' => Xử lý', shot=shot('16_handle'), shot_caption='Màn chi tiết phiếu Chờ xử lý còn dòng cần điều chuyển'),
   extra=[(shot('16b_complete'), 'Hộp “Xác nhận hoàn thành” khi không còn dòng cần điều chuyển')],
   ui=[
       ('Nút Tạo phiếu điều chuyển vị trí trên dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện',
        '- Chờ xử lý + Q3 + còn dòng thiếu; bấm → màn Tạo phiếu điều chuyển vị trí.'),
       ('Nút Xử lý trên dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Chờ xử lý + Q3, không còn dòng cần điều chuyển; bấm → chi tiết.'),
       ('Ô Tổng kiểm kê', 'Checkbox', 'Enable / Disable', '–', 'Không', 'Theo dữ liệu',
        ['- Chỉ ở dòng Chênh lệch ≠ 0', '- Tick là lưu ngay', '- Khóa trong lúc đang lưu']),
       ('Nút Tạo phiếu điều chuyển vị trí', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện',
        ['- Rê chuột: “Tạo phiếu điều chuyển vị trí cho các dòng chênh lệch thiếu”', '- Mở màn Tạo phiếu điều chuyển vị trí']),
       ('Nút Hoàn thành', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Bấm → hộp xác nhận.'),
       ('Hộp “Xác nhận hoàn thành”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Hoàn thành phiếu kiểm kê \"<số phiếu>\"? Phiếu sẽ chuyển sang trạng thái Hoàn thành và không xử lý thêm được nữa.”',
         '- Nút Hoàn thành, Hủy, (x)']),
       ('Cột Chênh lệch', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '- Âm = thiếu, chữ đỏ.'),
       ('Thông báo tick', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- “Cập nhật thành công.”', '- “Cập nhật thất bại.” / câu lỗi máy chủ']),
       ('Thông báo hoàn thành', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Hoàn thành phiếu kiểm kê thành công.”'),
       ('Thông báo lỗi hoàn thành', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Còn dòng chênh lệch thiếu chưa xử lý. Vui lòng tạo phiếu điều chuyển vị trí hoặc tick \"Tổng kiểm kê\".”', '- ' + CONFLICT]),
       ('Nhãn trạng thái', 'Badge', 'Read-only', '–', '–', 'Chờ xử lý', '- → Hoàn thành sau khi xong.'),
   ],
   ev=[
       ('Tick / bỏ tick Tổng kiểm kê', 'Change',
        'Before:\n– Kiểm tra quyền “%s” + phiếu Chờ xử lý; sai → %s / %s.\n' % (Q3, NOPERM, CONFLICT) +
        'During:\n– Dòng không chênh lệch → “Tổng kiểm kê – Chỉ áp dụng cho dòng có chênh lệch.”; dòng không thuộc phiếu → báo không tìm thấy.\n' + ERR + '\n'
        'After:\n– Lưu ô tick, ghi lịch sử “Thay đổi thông tin”.\n– Hiển thị “Cập nhật thành công.”, nạp lại nút Tạo phiếu điều chuyển / Hoàn thành.'),
       ('Bấm Tạo phiếu điều chuyển vị trí', 'Click',
        'Before:\n– Nút chỉ hiện khi còn dòng thiếu chưa xử lý.\nAfter:\n– Mở màn Tạo phiếu điều chuyển vị trí (phân hệ Kho) đã nạp kho + dòng thiếu.'),
       ('Bấm Hoàn thành', 'Click', 'Before:\n– Không còn dòng cần điều chuyển.\nAfter:\n– Hiện hộp “Xác nhận hoàn thành”.'),
       ('Bấm Hoàn thành (xác nhận)', 'Click',
        'Before:\n– Kiểm tra quyền “%s” + phiếu Chờ xử lý; sai → %s / %s.\n' % (Q3, NOPERM, CONFLICT) +
        'During:\n– Còn dòng cần điều chuyển → “Còn dòng chênh lệch thiếu chưa xử lý. …”.\n' + ERR + '\n'
        'After:\n– Phiếu Hoàn thành; ghi lịch sử “Thay đổi trạng thái”.\n– Hiển thị “Hoàn thành phiếu kiểm kê thành công.”, về danh sách.'),
       ('Phiếu điều chuyển xử lý hết', 'System',
        'Before:\n– Phiếu điều chuyển lập từ phiếu này được Điều chuyển.\nAfter:\n– Cộng số đã xử lý từng dòng; hết dòng cần điều chuyển → phiếu + kế hoạch Hoàn thành.'),
   ])

# ------------------------------------------------------------ 2.16 In
fr(16, 'In phiếu và in danh sách', usecase=('FR-16', 'In phiếu / In danh sách', 'io', A_LP),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu kiểm kê / In danh sách phiếu',
       mota='Xem trước và in một phiếu (mẫu in “Kiểm kê theo vị trí”: số phiếu, ngày kiểm kê, kế hoạch, kho, hội đồng, bảng chi tiết '
            'kèm Thực kiểm và Ghi chú, nhận xét đánh giá, khối ký) hoặc in danh sách theo bộ lọc đang áp. Bản in mở trong cửa sổ trên '
            'màn đang đứng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm In ở cột Hành động / màn chi tiết (in phiếu), hoặc In danh sách trên bảng.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ xem trước, hiện “Đang tải dữ liệu in…” trong lúc dựng.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Danh sách quá 2.000 dòng → không dựng bản in, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc.\n'
           '• Không có dòng nào → “Không có dữ liệu để in”.\n'
           '• Ngoài phạm vi → ' + NOTFOUND + '.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in phiếu kiểm kê theo vị trí.”.\n'
           '• Bấm (x) → đóng cửa sổ.',
       dacbiet='Logo / letterhead bản in phiếu lấy theo công ty ghi trên phiếu; bản in danh sách theo công ty người in, Người lập = người '
               'in. Thực kiểm chỉ in khi phiếu đã nhập kết quả. Bảng in không bị đẩy cả sang trang 2, khối ký thẳng hàng.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu kiểm kê theo vị trí',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   extra=[(shot('19_printlist'), 'Cửa sổ Xem trước danh sách kiểm kê theo vị trí')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–',
        ['- In phiếu: “Xem trước phiếu kiểm kê theo vị trí <số phiếu>”', '- In danh sách: “Xem trước danh sách kiểm kê theo vị trí”']),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', ['- Cạnh tiêu đề; bấm → hộp thoại in', '- Ẩn khi vượt 2.000 dòng']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Đang tải dữ liệu in…”.'),
       ('Đầu bản in phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Logo, tên công ty của phiếu', '- “KIỂM KÊ THEO VỊ TRÍ”, Số phiếu, Ngày kiểm kê, Kế hoạch kiểm kê', '- Kho vật lý, Hội đồng kiểm kê']),
       ('Bảng chi tiết bản in phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Nhà kho, Vị trí, Tên hàng, Mã hàng, ĐVT, SL tồn', '- Chi tiết tồn theo công ty: Công ty, Lô, SL, ĐVT kiểm kê', '- Thực kiểm, Ghi chú']),
       ('Nhận xét, đánh giá', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Ghi chú duyệt / lý do không duyệt.'),
       ('Chỗ ký phiếu', 'Label', 'Read-only', '–', 'Hiển thị', '- Hội đồng kiểm kê, Trưởng bộ phận kho.'),
       ('Bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        ['- Tiêu đề “DANH SÁCH PHIẾU KIỂM KÊ THEO VỊ TRÍ”',
         '- Cột: STT, Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho, Người tạo, Người duyệt, Ngày duyệt, Trạng thái',
         '- Khối ký: Ngày … Tháng … Năm …, Người lập']),
       ('Dòng nhắc vượt trần in', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Danh sách có N dòng, vượt mức in tối đa 2,000 dòng …”.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', ['- “Không tải được dữ liệu in”', '- “Không có dữ liệu để in”']),
   ],
   ev=[
       ('Bấm In (phiếu)', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → ' + NOTFOUND + '.\n'
        'During:\n– Dựng bản in theo mẫu; thiếu mẫu → “Thiếu mẫu in phiếu kiểm kê theo vị trí.”.\nAfter:\n– Hiện bản xem trước khổ dọc.'),
       ('Bấm In danh sách', 'Click',
        'Before:\n– Lấy bộ lọc đang áp.\nDuring:\n– Quá 2.000 dòng → dòng nhắc, ẩn bản in và nút In.\nAfter:\n– Hiện bản xem trước.'),
       ('Bấm In trong cửa sổ', 'Click', 'Before:\n– Bản in đã dựng.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, giữ nguyên màn đang đứng.'),
   ])

# ------------------------------------------------------------ 2.17 Xuất Excel
fr(17, 'Xuất Excel', usecase=('FR-17', 'Xuất Excel', 'io', A_LP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách / xuất 1 phiếu ra Excel',
       mota='(1) Xuất danh sách: chọn trường và thứ tự rồi xuất toàn bộ phiếu khớp bộ lọc (không phân trang). (2) Xuất 1 phiếu: nút '
            'Xuất Excel trên dòng / màn chi tiết tải file chi tiết của phiếu đó (thông tin chung, bảng chi tiết, nhận xét, khối ký).',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel trên bảng.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 11 trường (tích sẵn theo cột đang hiện).\n'
             '3. Người dùng tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy mọi phiếu theo bộ lọc + phạm vi xem, dựng file có letterhead công ty người xuất, tiêu đề “DANH SÁCH '
             'PHIẾU KIỂM KÊ THEO VỊ TRÍ”, dòng thời gian (khi lọc Ngày kiểm kê), cột STT + trường đã chọn, khối ký.\n'
             '5. Hệ thống tải file “danh_sach_phieu_kiem_ke_theo_vi_tri.xlsx”, báo “Xuất Excel thành công.”.\n'
             '6. Xuất 1 phiếu: bấm Xuất Excel trên dòng / chi tiết → tải “kiem_ke_theo_vi_tri_<số phiếu>.xlsx”.',
       phu='• Không có phiếu khớp → vẫn ra file có tiêu đề, dòng tên cột và khối ký.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi → “Lỗi khi xuất Excel.”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng; nút Xuất Excel khóa trong lúc đang xuất. File 1 phiếu: letterhead theo công ty ghi trên phiếu, '
               'số lượng là ô số. Ngày ở file danh sách giữ dạng chữ.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('21_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 11 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho, Trạng thái, Người tạo',
         '- Người duyệt, Ngày duyệt, Ngày tạo, Ngày cập nhật, Người cập nhật']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/11 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Bấm → tải file', '- Khóa khi chưa tích / đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('File danh sách', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Letterhead, tiêu đề “DANH SÁCH PHIẾU KIỂM KÊ THEO VỊ TRÍ”', '- Dòng “Từ ngày … đến ngày …” khi lọc Ngày kiểm kê',
         '- Cột STT + trường đã chọn; khối ký cuối file']),
       ('File 1 phiếu', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Tên “kiem_ke_theo_vi_tri_<số phiếu>.xlsx”', '- Số phiếu, Ngày kiểm kê, Kế hoạch kiểm kê, Kho vật lý, Hội đồng',
         '- Bảng chi tiết, “Nhận xét, đánh giá:”, khối ký Hội đồng kiểm kê / Trưởng bộ phận kho']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- Thành công: “Xuất Excel thành công.”', '- Thất bại: “Lỗi khi xuất Excel.”']),
   ],
   ev=[
       ('Bấm Xuất Excel (bảng)', 'Click', 'Before:\n– Không có lượt xuất đang chạy.\nAfter:\n– Mở cửa sổ chọn trường.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Kéo bằng biểu tượng.\nAfter:\n– Đổi thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc + phạm vi xem.\n– Lỗi → “Lỗi khi xuất Excel.”.\n' + ERR + '\n'
        'After:\n– Tải file danh sách, báo “Xuất Excel thành công.”.'),
       ('Bấm Xuất Excel trên dòng / chi tiết', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → “Lỗi khi xuất Excel.”.\nAfter:\n– Tải file 1 phiếu, báo “Xuất Excel thành công.”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.18 Lịch sử
fr(18, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu',
       mota='Xem các mốc thao tác của phiếu: Tạo mới, Thay đổi thông tin (giá trị cũ → mới: Kho vật lý, phạm vi, danh sách hàng tồn '
            'theo lô, hội đồng, file đính kèm, kết quả kiểm kê), Thay đổi trạng thái, Duyệt (kèm ghi chú duyệt), Từ chối (kèm lý do), '
            'Xóa. Cửa sổ ở danh sách và khối Lịch sử ở màn chi tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động (hoặc trong menu Hành động khác), hoặc Xem lịch sử ở màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ “Lịch sử thay đổi: <số phiếu>” và hiển thị các mốc, mới nhất ở trên.',
       phu='• Phiếu từ hệ thống cũ chưa có mốc → “Chưa có lịch sử thao tác nào.”.\n'
           '• Bấm Bộ lọc → các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Kết quả kiểm kê ghi theo từng dòng (Hàng – Vị trí – Lô – ĐVT kiểm kê: Thực kiểm, Chênh lệch, Ghi chú, Tổng kiểm kê cũ → '
               'mới). Xem, in, xuất Excel không ghi mốc.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('20_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('20b_history_empty'), 'Phiếu chưa có lịch sử')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <số phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái / Duyệt / Từ chối: “Trạng thái: <cũ> → <mới>” kèm ghi chú',
           '- Thay đổi thông tin: từng trường, từng dòng kết quả cũ → mới', '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách hành động', 'Trống', ['- Mặc định: trống', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Người đã thao tác', 'Trống', '- Chọn là lọc ngay.'),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc từ ngày này.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc đến hết ngày này.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', ['- “Chưa có lịch sử thao tác nào.”', '- “Không có lịch sử phù hợp bộ lọc.”']),
       ('Khối Lịch sử ở chi tiết', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Số mốc cạnh tiêu đề, nút Xem lịch sử / Thu gọn, Làm mới.'),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Giống nút Đóng.'),
   ],
   ev=[
       ('Mở lịch sử', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → ' + NOTFOUND + '.\n'
        'During:\n– Nạp các mốc; chưa có → “Chưa có lịch sử thao tác nào.”.\nAfter:\n– Hiển thị, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change', 'Before:\n– Không có nút Tìm kiếm.\nAfter:\n– Lọc lại danh sách mốc.'),
       ('Bấm Làm mới (khối ở chi tiết)', 'Click', 'Before:\n– Khối đang mở.\nAfter:\n– Nạp lại các mốc mới nhất.'),
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng; danh sách giữ nguyên trang, bộ lọc.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Kiểm kê theo vị trí; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phiếu không ghi tồn', [
        '– Lưu / gửi / nhập kết quả / duyệt / hoàn thành không đổi tồn kho, không sinh phiếu nhập / xuất.',
        '– Chỉ Phiếu điều chuyển vị trí lập từ phiếu mới đổi tồn; số tồn trên phiếu là ảnh chụp lúc lấy.'], ['Tạo', 'Duyệt', 'Xử lý']),
    ('BR-02', 'Phạm vi xem', [
        '– V1 (hoặc Super admin): mọi phiếu; V2: công ty mình + của mình (công ty trống → của mình); không quyền: của mình.',
        '– Phiếu Đang tạo chỉ người tạo thấy.',
        '– Ngoài phạm vi vẫn mở được chi tiết khi đang có việc: Q2 với phiếu Chờ duyệt kết quả, Q3 với phiếu Chờ xử lý.'],
     ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất', 'Lịch sử']),
    ('BR-03', 'Quyền và điều kiện thao tác', [
        '– Tạo: Q1. Sửa / Xóa: người tạo + Đang tạo. Nhập kết quả: người tạo + Đang kiểm.',
        '– Duyệt / Không duyệt: Q2 + Chờ duyệt kết quả. Xử lý: Q3 + Chờ xử lý.',
        '– Máy chủ kiểm lại khi thao tác: sai trạng thái → báo trạng thái đã thay đổi; đúng trạng thái nhưng thiếu quyền → báo không có quyền.'],
     ['Tạo', 'Chỉnh sửa', 'Xóa', 'Nhập kết quả', 'Duyệt', 'Xử lý']),
    ('BR-04', 'Dữ liệu bắt buộc khi lưu phiếu', [
        '– Lưu và Lưu và gửi cùng điều kiện: Kho vật lý, ≥ 1 vị trí, bảng Chi tiết có dữ liệu, ≥ 1 thành viên hội đồng có nhân viên + chức vụ, không trùng nhân viên.',
        '– Mỗi lô ≥ 1 dòng ĐVT kiểm kê; ĐVT phải thuộc hàng; SL > 0; tổng SL × hệ số = SL lô (hệ số lấy từ danh mục).'],
     ['Tạo', 'Chỉnh sửa', 'Lưu và gửi']),
    ('BR-05', 'Kế hoạch kiểm kê', [
        '– Chỉ chọn kế hoạch Đang kiểm mà người dùng có Q1 và là thủ kho của kho trong kế hoạch; chỉ chọn lúc tạo.',
        '– Lập phiếu từ kế hoạch: kho, phạm vi lấy theo kế hoạch (khóa), ngày phiếu = ngày tạo kế hoạch; kế hoạch → Đã lập kiểm kê.',
        '– Xóa phiếu: kế hoạch Đã lập kiểm kê → Đang kiểm (lệch hệ thống cũ có chủ đích).'], ['Tạo', 'Chọn kế hoạch', 'Xóa']),
    ('BR-06', 'Nhập kết quả', [
        '– Bắt buộc Thực kiểm mọi dòng (0 – 999,999,999); Chênh lệch = Thực kiểm − SL do máy chủ tính.',
        '– Chênh lệch ≠ 0 bắt buộc Ghi chú (≤ 255 ký tự); Chênh lệch = 0 thì Tổng kiểm kê tự bỏ.',
        '– Phiếu chưa có file bắt buộc đính kèm (pdf, png, jpg, jpeg, doc, docx, xls, xlsx; ≤ 20MB); file mới nối thêm vào file cũ.'],
     ['Nhập kết quả']),
    ('BR-07', 'Vòng đời trạng thái', [
        '– Lưu → Đang tạo; Lưu và gửi → Đang kiểm; Lưu kết quả → Chờ duyệt kết quả.',
        '– Duyệt: còn dòng thiếu → Chờ xử lý; không → Hoàn thành (+ kế hoạch Hoàn thành). Không duyệt → Đang kiểm.',
        '– Hoàn thành ở bước Xử lý (không cập nhật kế hoạch); điều chuyển xử lý hết → Hoàn thành (+ kế hoạch Hoàn thành).'],
     ['Lưu và gửi', 'Nhập kết quả', 'Duyệt', 'Không duyệt', 'Xử lý']),
    ('BR-08', 'Dòng cần điều chuyển', [
        '– Dòng có Chênh lệch < 0, chưa tick Tổng kiểm kê, số đã xử lý chưa bằng |Chênh lệch| → cần điều chuyển.',
        '– Còn dòng cần điều chuyển: hiện Tạo phiếu điều chuyển vị trí, chặn Hoàn thành; hết: hiện Hoàn thành.'], ['Xử lý']),
    ('BR-09', 'Tính duy nhất và chuẩn hóa', [
        '– Không có trường nhập duy nhất; mã <mã công ty>-KKVT-NNNNN tự sinh theo công ty người tạo, không sửa được.',
        '– Tổ chức của phiếu = của người tạo; chọn nhân viên tự điền chức vụ đầu tiên; ghi chú / lý do bỏ khoảng trắng đầu / cuối.',
        '– Nút thao tác khóa trong lúc gửi chống tạo trùng.'], ['Tạo', 'Chỉnh sửa', 'Nhập kết quả']),
    ('BR-10', 'Khóa vị trí đang kiểm kho', [
        '– Vị trí thuộc phiếu Đang kiểm / Chờ duyệt kết quả bị coi là đang kiểm kho ở Phiếu điều chuyển vị trí (không chọn, chặn khi điều chuyển).',
        '– Phiếu nhập kho chặn nhập vào vị trí của phiếu Đang kiểm.'], ['Lưu và gửi', 'Nhập kết quả']),
    ('BR-11', 'Thông báo', [
        '– Lưu kết quả → “[KKVT] Chờ duyệt” cho người có Q2; Duyệt có thiếu → “[KKVT] Đã duyệt” cho người có Q3 — cùng công ty người thao tác.',
        '– Không duyệt → “[KKVT] Từ chối” cho người tạo. Bấm thông báo mở chi tiết phiếu; lỗi gửi không làm hỏng thao tác.'],
     ['Nhập kết quả', 'Duyệt', 'Không duyệt']),
    ('BR-12', 'In và xuất', [
        '– Letterhead bản in / file 1 phiếu theo công ty ghi trên phiếu; bản in / file danh sách theo công ty người in.',
        '– In danh sách tối đa 2.000 dòng; Xuất Excel danh sách không giới hạn, rỗng vẫn ra file.'], ['In', 'Xuất Excel']),
    ('BR-13', 'Liên kết cấp cha – con và sử dụng ở màn khác', [
        '– Phạm vi: bỏ tick cấp cha tự bỏ cấp con; vị trí tự do độc lập. Chi tiết: vị trí > hàng > công ty > lô > dòng ĐVT kiểm kê.',
        '– Xóa phiếu xóa hết dữ liệu con. Kho, nhà, dãy, khoang, vị trí, hàng hóa đã có trong phiếu không xóa được ở danh mục.'],
     ['Tạo', 'Xóa', 'Lấy vị trí']),
    ('BR-14', 'Quy tắc ghi lịch sử', [
        '– Ghi: Tạo mới; Thay đổi thông tin (Kho, Nhà, Dãy, Khoang, Vị trí, Danh sách hàng tồn theo lô, Hội đồng, File đính kèm, '
        'Danh sách kết quả kiểm kê — cũ → mới, không đổi thì không ghi); Thay đổi trạng thái; Duyệt; Từ chối; Xóa.',
        '– Kế hoạch cha ghi “Thay đổi trạng thái” kèm mã phiếu khi phiếu đổi trạng thái kế hoạch. Xem / in / xuất không ghi.'],
     ['Tạo', 'Chỉnh sửa', 'Xóa', 'Nhập kết quả', 'Duyệt', 'Lịch sử']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Kiểm kê theo vị trí (trạng thái phiếu, kết quả và chênh lệch từng lô, '
    'phạm vi vị trí đang kiểm kho).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Tài chính', 'Kế hoạch kiểm kê theo vị trí (nút Lập phiếu kiểm kê mở màn Tạo phiếu đã nạp kế hoạch; trạng thái kế hoạch đổi '
                       'theo phiếu: lập phiếu → Đã lập kiểm kê, xóa phiếu → Đang kiểm, duyệt không thiếu / điều chuyển xử lý hết → '
                       'Hoàn thành; lịch sử kế hoạch ghi mã phiếu)', 'Tài chính -> Kiểm kê'),
    ('2', 'Kho', 'Phiếu điều chuyển vị trí (lập từ phiếu Chờ xử lý — đọc dòng chênh lệch thiếu, ghi ngược số đã xử lý, xử lý hết thì '
                 'phiếu + kế hoạch Hoàn thành; vị trí của phiếu Đang kiểm / Chờ duyệt kết quả không chọn được; cột nguồn liên kết về '
                 'phiếu)', 'Kho -> Điều chuyển'),
    ('3', 'Kho', 'Phiếu nhập kho (chặn nhập vào vị trí thuộc phiếu kiểm kê Đang kiểm — “Vị trí … đang kiểm kho”)', 'Kho -> Nhập kho'),
    ('4', 'Kho', 'Kho vật lý (không xóa được kho đã có trong phiếu)', 'Kho -> Danh mục'),
    ('5', 'Kho', 'Vị trí (không xóa được vị trí đã có trong phiếu; vị trí đã khóa không hiện để tick mới)', 'Kho -> Danh mục'),
    ('6', 'Kho', 'Nhà kho, Dãy, Khoang (không xóa được mục đã tick trong phiếu; mục đã khóa không hiện để tick mới)', 'Kho -> Danh mục'),
    ('7', 'Danh mục dùng chung', 'Hàng hoá, vật tư (không xóa được hàng đã có trong chi tiết phiếu; ĐVT và hệ số quy đổi lấy từ hàng)',
     'Danh mục dùng chung -> Hàng hoá -> Hàng hoá, vật tư'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
