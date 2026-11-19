# -*- coding: utf-8 -*-
"""SRS màn "Phiếu chờ giao việc" (phân hệ CSKH sau bán › Giao việc) — form chuẩn SRS_MAU (12/11/2026).

Chạy: python gen_srs.py  -> "SRS - Phiếu chờ giao việc.docx" (SrsDoc.save() tự chạy srs_selfcheck).
Khuôn: ../bien-ban-ban-giao-nghiem-thu/gen_srs.py (10/11). Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột.
Nguồn đọc 12/11/2026 (nhánh develop cả 2 repo, con của gop_db):
  BE  Modules/Assign/Services/WaitingAssignTaskService.php (5 tab, "còn số lượng để giao", phạm vi, cờ hành động, từ chối PL),
      Http/Controllers/Api/V1/WaitingAssignTaskController.php, Routes/api.php (/assign/waiting-assign-tasks, checkPermission
      "Tạo phiếu giao việc" ở route từ chối PL), Exports/WaitingAssignTaskExport.php, AssemblyRequestPrintService (mẫu in 368);
      CustomerCare WrServiceContractController@rejectReception/close/unApprove + WrServiceContractService (HĐ: lịch sử + thông báo),
      WrServiceContract accessor is_can_*; WrAssignTaskStoreService / WrAssignTaskRemainingService (Tạo PGV trừ SL còn giao);
      app/Support/Permissions/Catalog/customer_care.php (customer_care.phieu_cho_giao_viec.view mức 3-4, legacy tên cũ = mức 4;
      customer_care.phieu_giao_viec.create), sale.php (sale.hop_dong_an_gia.view).
  FE  pages/customer-care/waiting-assign-tasks/{index.vue, tabConfigs.js, components/WaitingAssignTaskList.vue},
      components/subsystem-menu/customer-care.js (nhóm "Giao việc"), components/modal/base-confirm-modal.vue,
      pages/customer-care/wr-assign-tasks/components/{WrAssignTaskForm.vue, wrAssignTaskLinks.js} (Quay lại về màn chờ).
  Bối cảnh: design.md, plan.md (#11972, #11973, #11975, #11985, #11988), spec docs/superpowers/specs/gop-db/2026-10-31-phieu-cho-giao-viec-design.md.
Ảnh: ./pcgv_shots — dev-hrm 12/11/2026 (_capture/capture.js, DNS Admin, chặn mọi yêu cầu ghi: 0 yêu cầu ghi).
  GIẢ TRẠNG THÁI trên trình duyệt: DNS Admin không thuộc phòng tiếp nhận nào → cờ Tạo phiếu giao việc / Từ chối tiếp nhận tắt ở
  tab HĐ, PL, Lắp đặt; capture bật cờ dòng 1 trong dữ liệu trả về (01b_row_more, 01c_pl_actions, 01d_assembly_actions, 30*, 31, 32, 33).
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

TEN = 'Phiếu chờ giao việc'
SHOTS = os.path.join(HERE, 'pcgv_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ CSKH sau bán => Giao việc => Phiếu chờ giao việc'
M_HD = MENU + ' => Hợp đồng'
M_PL = MENU + ' => PL bổ sung'
M_BH = MENU + ' => Phiếu bảo hành'
M_LD = MENU + ' => Lắp đặt bàn giao'
M_GVK = MENU + ' => Giao việc khác'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu chờ giao việc.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
Q1 = 'Tạo phiếu giao việc'
QV = 'Xem danh sách phiếu chờ giao việc'
QG = 'Xem hợp đồng ẩn giá'
A_XEM = 'Người xem hàng đợi'
A_TN = 'Phòng tiếp nhận xử lý'
A_LAP = 'Người lập / quản lý hợp đồng'
TN = ('Người dùng có quyền thực hiện chức năng: không cần quyền riêng để mở màn; quyền “%s” mức Tổng công ty mở rộng phạm vi '
      'tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao.' % QV)
TN_TN = ('Người dùng có quyền thực hiện chức năng: %s, thuộc đúng phòng tiếp nhận xử lý của chứng từ (tab Lắp đặt bàn giao, Giao '
         'việc khác chỉ xét phòng tiếp nhận; tab Phiếu bảo hành không kiểm ở màn này).' % Q1)
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn Phiếu chờ giao việc, đúng tab của chứng từ.\n'
      '3. Chứng từ nằm trong phạm vi xem của tab.')
DK_HD = ('1. Người dùng đăng nhập thành công.\n2. Đang ở tab Hợp đồng của màn Phiếu chờ giao việc.\n'
         '3. Hợp đồng ở trạng thái Có hiệu lực và còn số lượng chưa giao việc.')
REQ_REJ = '“Bắt buộc phải nhập lý do từ chối tiếp nhận”'
REQ_UN = '“Bắt buộc phải nhập lý do hủy duyệt”'
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
PLG = '“Hợp đồng đang có PL giảm chờ duyệt!”'
NO_ERP = '“Chưa cấu hình đường dẫn ERP”'
FAIL = '“Thao tác thất bại”'
LOAD_ERR = '“Lỗi khi tải dữ liệu”'
EMPTY = '“Không có dữ liệu phù hợp.”'

d = SrsDoc(out=OUT, menu=MENU, route='/customer-care/waiting-assign-tasks', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ CSKH sau bán': 'menu_phanhe', 'Giao việc': 'menu_nhom', 'Phiếu chờ giao việc': 'menu_muc',
    'Hợp đồng': 'tab_contract', 'PL bổ sung': 'tab_addition_annex', 'Phiếu bảo hành': 'tab_warranty',
    'Lắp đặt bàn giao': 'tab_assembly', 'Giao việc khác': 'tab_other',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Xuất Excel': 'btn_xuatexcel', 'Tạo phiếu giao việc': 'btn_taopgv_row', 'Từ chối tiếp nhận xử lý': 'btn_tuchoi_row',
    'Đóng hợp đồng': 'item_dong', 'Hủy duyệt hợp đồng': 'item_huyduyet', 'Quyết toán hợp đồng': 'item_quyettoan',
    'In': 'btn_in_row', 'Xuất Excel 1 phiếu': 'btn_xuat1_row', 'Mã phiếu': 'link_mabh', 'Số phiếu': 'link_sophieu_gvk',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu chờ giao việc (phân hệ CSKH sau bán, nhóm Giao việc) — HÀNG ĐỢI điều '
    'phối của phòng tiếp nhận xử lý, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ 5 nguồn chứng từ còn việc chưa giao (mỗi nguồn 1 tab): Hợp đồng dịch vụ, Phụ lục bổ sung (PL bổ sung), Phiếu bảo hành, '
    'Phiếu yêu cầu lắp đặt bàn giao, Phiếu yêu cầu giao việc khác — và điều kiện để 1 chứng từ còn nằm trong hàng đợi.',
    'Làm rõ các hành động trên từng dòng: Tạo phiếu giao việc (mở màn Tạo phiếu giao việc), Từ chối tiếp nhận xử lý, Đóng hợp '
    'đồng, Hủy duyệt hợp đồng, In phiếu yêu cầu lắp đặt; và các hành động còn mở sang hệ thống ERP (Quyết toán hợp đồng, Xuất '
    'Excel 1 phiếu yêu cầu lắp đặt, xem phiếu yêu cầu lắp đặt / hợp đồng bán).',
])
d.p('Phạm vi chức năng: Xem danh sách 5 tab, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo phiếu giao việc, Từ chối tiếp '
    'nhận xử lý (Hợp đồng, PL bổ sung), Đóng hợp đồng, Hủy duyệt hợp đồng, Mở chức năng ở hệ thống ERP (Quyết toán hợp đồng, Xuất '
    'Excel 1 phiếu yêu cầu lắp đặt), Xem chi tiết chứng từ nguồn, In phiếu yêu cầu lắp đặt bàn giao, Xuất Excel danh sách. Màn '
    'KHÔNG có Thêm mới / Sửa / Xóa / Khóa / Duyệt / Import / Lịch sử thay đổi riêng: chứng từ được lập ở màn nguồn; lịch sử của '
    'thao tác Từ chối / Đóng / Hủy duyệt ghi vào lịch sử của hợp đồng (màn Hợp đồng dịch vụ).')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phòng tiếp nhận xử lý biết chứng từ nào còn công / dịch vụ / hàng chưa giao để lập phiếu giao việc cho kỹ thuật.',
    'Người lập / quản lý hợp đồng dọn hàng đợi: đóng hợp đồng không làm tiếp, hủy duyệt hợp đồng lập sai, quyết toán hợp đồng.',
    'Phòng được giao trả chứng từ không thuộc mình (Từ chối tiếp nhận) để người lập chọn lại phòng tiếp nhận.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Mỗi tab chỉ lấy 1 trạng thái: Hợp đồng / PL bổ sung “Có hiệu lực”, Phiếu bảo hành “Đã duyệt” và còn đánh dấu chờ giao, Lắp đặt '
    '/ Giao việc khác “Chờ giao việc” (BR-02).',
    'SL chưa giao việc = Số lượng nguồn − SL phụ lục giảm − SL đã giao (đã chốt) − SL trên phiếu giao việc đang chạy; còn ít nhất 1 '
    'dòng > 0 thì chứng từ còn trong hàng đợi (BR-03).',
    'Phạm vi: tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao bó theo phòng tiếp nhận ∈ phòng mình quản lý, trừ khi có quyền Xem mức '
    'Tổng công ty; tab Phiếu bảo hành, Giao việc khác không bó phạm vi (BR-01, giữ như ERP).',
    'Nút hành động do hệ thống tính theo từng dòng (quyền, phòng tiếp nhận, người tạo, chứng từ phía sau) — BR-05..BR-08.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu chờ giao việc', 'Hàng đợi (không phải 1 loại chứng từ riêng): danh sách chứng từ nguồn còn số lượng chưa giao việc.'),
    ('HĐ / Hợp đồng dịch vụ', 'Hợp đồng sửa chữa – bảo dưỡng – bảo trì (mã HDDV_…), lập ở màn Hợp đồng dịch vụ.'),
    ('PL bổ sung', 'Phụ lục bổ sung của hợp đồng dịch vụ (mã kết thúc -PL…); PL giảm là phụ lục giảm số lượng.'),
    ('Phiếu bảo hành (PBH)', 'Chứng từ <mã công ty>.PBH.<năm>.NNNNNN của màn Phiếu bảo hành.'),
    ('Phiếu yêu cầu lắp đặt bàn giao (YCLDBG)', 'Chứng từ <mã công ty>.YCLDBG.<năm>NNNNNN lập ở hệ thống ERP (chưa chuyển sang HRM).'),
    ('Phiếu yêu cầu giao việc khác (YCGVK)', 'Chứng từ <mã công ty>.YCGVK.<năm>NNNNNN của màn Phiếu yêu cầu giao việc khác.'),
    ('Phiếu giao việc (PGV)', 'Chứng từ giao việc cho kỹ thuật, lập từ màn này (nút Tạo phiếu giao việc). PGV đang chạy = PGV gốc '
                              'ở trạng thái Đang giao / Đang nhập kết quả / Đã nhập kết quả / Đang duyệt kết quả.'),
    ('Phòng tiếp nhận xử lý', 'Phòng được người lập chứng từ chỉ định để lập phiếu giao việc.'),
    ('SL chưa giao việc', 'Số lượng còn lại của từng dòng công / dịch vụ / hàng sau khi trừ phần đã giao (BR-03).'),
    ('Trạng thái Có hiệu lực', 'Nhãn xanh dương: hợp đồng / PL đã duyệt — trạng thái duy nhất của tab Hợp đồng, PL bổ sung.'),
    ('Trạng thái Đã duyệt', 'Nhãn xanh lá: phiếu bảo hành đã duyệt — trạng thái duy nhất của tab Phiếu bảo hành.'),
    ('Trạng thái Chờ giao việc', 'Nhãn cam: phiếu yêu cầu chờ giao việc — trạng thái duy nhất của tab Lắp đặt, Giao việc khác.'),
    ('Đóng / Không duyệt', 'Trạng thái hợp đồng sau khi Đóng hợp đồng / Hủy duyệt hợp đồng — rời khỏi hàng đợi.'),
    ('Cấu trúc phân cấp', 'Hợp đồng > phụ lục bổ sung / giảm; chứng từ nguồn > dòng công, dịch vụ, hàng > phiếu giao việc (nhiều lần).'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn không gắn quyền ở menu và không chặn quyền khi mở (giữ như ERP): ai đăng nhập cũng vào được, dữ liệu do hệ thống giới '
    'hạn theo tab. Các mã quyền liên quan: customer_care.phieu_cho_giao_viec.view (“%s”, 2 mức Tổng công ty / Công ty — màn chỉ đọc '
    'mức Tổng công ty), customer_care.phieu_giao_viec.create (“%s”), sale.hop_dong_an_gia.view (“%s”, của màn Hợp đồng). Quyền tính '
    'theo công ty đang làm việc; không có đặc cách Super admin.' % (QV, Q1, QG))
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1, 'Cùng điều kiện phòng tiếp nhận = phòng của người đăng nhập: hiện nút Tạo phiếu giao việc (tab Hợp đồng, PL bổ sung), '
               'Từ chối tiếp nhận xử lý (Hợp đồng — khi chưa có phiếu giao việc; PL bổ sung). Tab Lắp đặt / Giao việc khác KHÔNG xét '
               'Q1; tab Phiếu bảo hành luôn hiện nút (xét Q1 ở màn Tạo phiếu giao việc).'),
    ('Q2', QG, 'Hợp đồng ngoài phạm vi giá của người xem thì ô Tổng thanh toán để trống (cả trong file Excel).'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (một mã Xem, màn dùng 1 mức):')
d.table(['Ký hiệu', 'Quyền – mức phạm vi', 'Phạm vi dữ liệu'], [
    ('V1', QV + ' – Tổng công ty', 'Tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao: mọi chứng từ còn việc chưa giao, mọi công ty.'),
    ('V2', QV + ' – Công ty', 'Màn không dùng mức này: phạm vi như không có quyền (dòng dưới).'),
    ('—', 'Không có V1', 'Tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao: chỉ chứng từ có phòng tiếp nhận thuộc các phòng người xem quản lý '
                         '(mọi công ty). Không quản lý phòng nào → 3 tab rỗng.'),
    ('(mọi người)', 'Không cần quyền', 'Tab Phiếu bảo hành, Giao việc khác: mọi chứng từ còn việc chưa giao (không bó phạm vi).'),
], widths=[0.8, 2.2, 3.0])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'V1', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ theo phạm vi', '✅ (ẩn giá)', '✅ mọi chứng từ', '✅ phòng mình quản lý (HĐ, PL, LĐ); hết (BH, GVK)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo phiếu giao việc', '✅ đúng phòng tiếp nhận', '—', '—', 'Chỉ tab BH (nút luôn hiện), LĐ / GVK (đúng phòng tiếp nhận)'),
    ('FR-06 Từ chối tiếp nhận xử lý', '✅ đúng phòng tiếp nhận', '—', '—', '❌'),
    ('FR-07 Đóng hợp đồng', '—', '—', '—', 'Người lập HĐ / quản lý phòng của HĐ'),
    ('FR-08 Hủy duyệt hợp đồng', '—', '—', '—', 'Quản lý phòng của HĐ'),
    ('FR-09 Mở chức năng ở hệ thống ERP', '—', '—', '—', 'Quyết toán: người lập HĐ; Xuất Excel 1 phiếu LĐ: mọi người'),
    ('FR-10 Xem chi tiết chứng từ nguồn', '✅', '✅', '✅', '✅ (theo quyền của màn nguồn)'),
    ('FR-11 In phiếu yêu cầu lắp đặt', '✅', '✅', '✅', '✅'),
    ('FR-12 Xuất Excel danh sách', '✅ theo phạm vi', '✅ (ẩn giá)', '✅', '✅ theo phạm vi'),
    ('Thêm / Sửa / Xóa / Khóa / Duyệt / Import / Lịch sử', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.9, 1.0, 0.8, 0.9, 1.4])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có V1 và không quản lý phòng nào: tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao hiện “Không có dữ liệu phù hợp.”; tab Phiếu '
    'bảo hành, Giao việc khác vẫn đủ dữ liệu.',
    'Không có Q1: không có nút Tạo phiếu giao việc / Từ chối tiếp nhận ở tab Hợp đồng, PL bổ sung; gọi thẳng chức năng Từ chối tiếp '
    'nhận PL → hệ thống từ chối, báo không có quyền; HĐ → “Không thể từ chối tiếp nhận hợp đồng này”.',
    'Không thuộc phòng tiếp nhận của chứng từ: không có nút Tạo phiếu giao việc (trừ tab Phiếu bảo hành).',
    'Bị gỡ quyền / đổi phòng giữa lúc thao tác: lần nạp hoặc thao tác tiếp theo hệ thống tính lại (cờ nút tính lại mỗi lần nạp danh '
    'sách, thao tác ghi kiểm lại điều kiện).',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Tạo phiếu giao việc', 'HĐ / PL: Q1 + phòng tiếp nhận = phòng mình; LĐ / GVK: phòng tiếp nhận = phòng mình; BH: luôn hiện',
     'HĐ kiểm thêm PL giảm chờ duyệt khi bấm'),
    ('Từ chối tiếp nhận xử lý', 'HĐ: như Tạo PGV + HĐ chưa có phiếu giao việc; PL: như Tạo PGV', 'Lý do bắt buộc'),
    ('Quyết toán hợp đồng', 'Tab HĐ, người đăng nhập là người lập HĐ', 'Mở hệ thống ERP tab mới'),
    ('Đóng hợp đồng', 'Tab HĐ: người lập HĐ hoặc quản lý phòng của HĐ; HĐ chưa có chứng từ phía sau', 'Kéo phụ lục đóng theo'),
    ('Hủy duyệt hợp đồng', 'Tab HĐ: quản lý phòng của HĐ; chưa có chứng từ phía sau; không còn phụ lục đang sống', 'Lý do bắt buộc'),
    ('In, Xuất Excel 1 phiếu', 'Tab Lắp đặt bàn giao, mọi dòng', 'Xuất Excel 1 phiếu mở ERP'),
    ('Xuất Excel, Cấu hình cột, Cài đặt bộ lọc', 'Luôn hiện', 'Dữ liệu theo phạm vi tab'),
], widths=[1.8, 2.6, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_XEM, [0, 5, 6]), (A_TN, [1, 2]), (A_LAP, [3, 4])],
    [('FR-01', 'Xem danh sách chờ giao việc', 'view'),
     ('FR-05', 'Tạo phiếu giao việc', 'crud'),
     ('FR-06', 'Từ chối tiếp nhận xử lý', 'action'),
     ('FR-07', 'Đóng hợp đồng', 'action'),
     ('FR-08', 'Hủy duyệt hợp đồng', 'action'),
     ('FR-11', 'In phiếu yêu cầu lắp đặt', 'io'),
     ('FR-12', 'Xuất Excel danh sách', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-10', 'Xem chi tiết chứng từ nguồn', 'view', 'extend', [0], None),
     ('FR-09', 'Mở chức năng ở hệ thống ERP', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu chờ giao việc')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu chờ giao việc',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách chứng từ chờ giao việc theo 5 tab',
       mota='Hiển thị hàng đợi điều phối gồm 5 tab: Hợp đồng, PL bổ sung, Phiếu bảo hành, Lắp đặt bàn giao, Giao việc khác. Mỗi tab '
            'chỉ chứa chứng từ đúng trạng thái và còn số lượng chưa giao việc, trong phạm vi của tab. Mỗi tab có bộ cột, ô lọc, cấu '
            'hình cột và bộ lọc ghi nhớ riêng; tab đang chọn giữ trên đường dẫn nên tải lại trang vẫn đúng tab.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng để mở màn; dữ liệu giới hạn theo phạm vi từng tab.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout; màn mở tab Hợp đồng (hoặc tab đã chọn trước đó trên đường dẫn).\n'
             '2. Hệ thống xác định phạm vi: tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao — có V1 thì mọi chứng từ, không thì phòng tiếp '
             'nhận ∈ phòng mình quản lý; tab Phiếu bảo hành, Giao việc khác — mọi chứng từ.\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng của tab trong 10 phút gần nhất và cấu hình cột đã lưu của người dùng cho tab.\n'
             '4. Hệ thống lấy chứng từ đúng trạng thái của tab, còn ít nhất 1 dòng có SL chưa giao việc > 0, khớp bộ lọc; sắp mới tạo '
             'nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, tiêu đề bảng theo tab, dòng “Hiển thị a–b / N” và phân trang.\n'
             '6. Với từng dòng, hệ thống tính nút ở cột Hành động (BR-05..BR-08) và ẩn Tổng thanh toán nếu thuộc diện ẩn giá.\n'
             '7. Người dùng bấm tab khác → hệ thống dựng lại danh sách của tab đó (bộ cột, ô lọc, bộ lọc riêng), nạp trang 1.',
       phu='• Không có chứng từ trong phạm vi / khớp bộ lọc → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Máy chủ lỗi khi nạp → thông báo “Lỗi khi tải dữ liệu”, bảng trống.\n'
           '• Đường dẫn ghi tab lạ → hệ thống mở tab Hợp đồng, không báo lỗi.\n'
           '• Không có V1 và không quản lý phòng nào → tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao rỗng.\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: tất cả (HĐ / PL 11 cột, BH 8, Lắp đặt 8, Giao việc khác 8). Cột khóa: STT, Mã phiếu (Số phiếu), Hành '
               'động. Sắp xếp được: Mã phiếu / Số phiếu, Ngày tạo; HĐ / PL thêm Ngày duyệt; mặc định Ngày tạo mới nhất ở trên. Mỗi trang '
               'tối đa 100 dòng. Không có nút Tạo mới / Import (hàng đợi chỉ xem).'),
   layout=dict(entries=[
       (MENU, 'Lối vào duy nhất trên menu — mở tab Hợp đồng; 5 tab chọn trên thanh tab đầu màn. Màn Tạo phiếu giao việc bấm Quay lại '
              'cũng về đúng tab của chứng từ nguồn.')],
       shot=shot('01_list'), shot_caption='Màn Phiếu chờ giao việc — tab Hợp đồng'),
   extra=[(shot('00_menu'), 'Mục Phiếu chờ giao việc trong nhóm Giao việc (phân hệ CSKH sau bán)'),
          (shot('01_list_addition_annex'), 'Tab PL bổ sung'),
          (shot('01_list_warranty'), 'Tab Phiếu bảo hành'),
          (shot('01_list_assembly'), 'Tab Lắp đặt bàn giao'),
          (shot('01_list_other'), 'Tab Giao việc khác'),
          (shot('03_empty'), 'Trạng thái không có dữ liệu phù hợp')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Phiếu chờ giao việc” trên thanh đầu trang.'),
       ('Thanh tab', 'Button', 'Enable', 'Danh sách 5 tab', 'Hợp đồng',
        ['- Mặc định: Hợp đồng', '- Lựa chọn: Hợp đồng / PL bổ sung / Phiếu bảo hành / Lắp đặt bàn giao / Giao việc khác',
         '- Bấm tab → dựng lại danh sách của tab, giữ tab trên đường dẫn']),
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Theo tab',
        ['- Hợp đồng chờ giao việc', '- PL bổ sung chờ giao việc', '- Phiếu bảo hành chờ giao việc',
         '- Yêu cầu lắp đặt bàn giao chờ giao việc', '- Yêu cầu giao việc khác chờ giao việc']),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', ['- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.12)', '- Khóa khi đang xuất']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa, cố định khi cuộn ngang']),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Tab HĐ / PL: chữ thường, KHÔNG bấm được (giữ như ERP)',
         '- Tab Phiếu bảo hành: liên kết → mở màn chi tiết phiếu bảo hành (mục 2.10)',
         '- Mã dài tự xuống dòng, không cắt', '- Sắp xếp được; cột khóa']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Tab Lắp đặt bàn giao: liên kết → mở phiếu yêu cầu lắp đặt ở hệ thống ERP, tab mới',
         '- Tab Giao việc khác: liên kết → mở màn chi tiết phiếu yêu cầu giao việc khác (mục 2.10)', '- Sắp xếp được; cột khóa']),
       ('Cột Tổng thanh toán', 'Table/Grid', 'Read-only', '≥ 0', 'Hiển thị',
        ['- Chỉ tab HĐ / PL', '- Tổng tiền sau thuế, phân cách hàng nghìn', '- Trống khi hợp đồng thuộc diện ẩn giá với người xem (Q2)']),
       ('Cột Số hợp đồng', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Chỉ tab Lắp đặt, Giao việc khác', '- Số hợp đồng bán: liên kết mở hợp đồng ở hệ thống ERP, tab mới',
         '- Trống khi phiếu không gắn hợp đồng']),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Dạng “Mã KH - Tên khách hàng”', '- Tối đa 2 dòng']),
       ('Cột Người liên hệ - SĐT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Tab HĐ / PL / BH', '- Dạng “Tên - SĐT”, tối đa 2 dòng']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Họ tên người lập chứng từ', '- Tab Lắp đặt: “Họ tên - SĐT”']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Sắp xếp được; mặc định mới nhất ở trên.'),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Chỉ tab HĐ / PL.'),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', ['- Chỉ tab HĐ / PL', '- Sắp xếp được']),
       ('Cột Trạng thái', 'Badge', 'Read-only', '–', 'Hiển thị',
        ['- HĐ / PL: Có hiệu lực (xanh dương)', '- Phiếu bảo hành: Đã duyệt (xanh lá)', '- Lắp đặt / Giao việc khác: Chờ giao việc (cam)',
         '- Không sắp xếp']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Tạo phiếu giao việc (dấu +) → mục 2.5',
           '- Từ chối tiếp nhận xử lý (HĐ, PL) → mục 2.6', '- Quyết toán hợp đồng (HĐ) → mục 2.9',
           '- Đóng hợp đồng (HĐ) → mục 2.7', '- Hủy duyệt hợp đồng (HĐ) → mục 2.8',
           '- In (Lắp đặt) → mục 2.11', '- Xuất Excel 1 phiếu (Lắp đặt) → mục 2.9',
           '- Hiện thẳng: Tạo phiếu giao việc, Từ chối tiếp nhận, In, Xuất Excel 1 phiếu',
           '- Tab HĐ: Quyết toán, Đóng, Hủy duyệt nằm trong nút ba chấm “Hành động khác”',
           '- Nút nào không đủ điều kiện thì ẩn', '- Cột khóa']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- Giữa bảng: “Không có dữ liệu phù hợp.” khi N = 0', '- Chân bảng: “Không có phiếu nào.”']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang', '- N: tổng số chứng từ chờ giao việc khớp bộ lọc trong phạm vi tab']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Trang đầu: về đầu / lùi mờ; trang cuối: tiến / về cuối mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Lỗi khi tải dữ liệu” khi máy chủ lỗi.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định tab theo đường dẫn (tab lạ → Hợp đồng); xác định phạm vi tab theo V1 / phòng quản lý.\n'
        '– Khôi phục bộ lọc (10 phút) và cấu hình cột của tab.\n'
        'During:\n– Lấy chứng từ đúng trạng thái, còn SL chưa giao việc, khớp bộ lọc; tính cờ nút từng dòng.\n'
        '– Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, chứng từ mới tạo nhất ở trên, kèm dòng “Hiển thị a–b / N”.'),
       ('Bấm một tab', 'Click',
        'Before:\n– Bấm lại đúng tab đang mở thì bỏ qua.\n'
        'During:\n– Ghi tab lên đường dẫn; dựng lại danh sách với bộ cột, ô lọc, bộ lọc ghi nhớ của tab mới.\n'
        'After:\n– Nạp trang 1 của tab mới; tab cũ giữ bộ lọc riêng (10 phút).'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Mã phiếu / Số phiếu, Ngày tạo (HĐ / PL thêm Ngày duyệt) hỗ trợ sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc; độ rộng cột cố định nên bảng không nhảy bố cục.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp; bấm lại trang đang xem thì bỏ qua.\n'
        'After:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại theo số dòng mới.'),
       ('Bấm nút ba chấm “Hành động khác”', 'Click',
        'Before:\n– Dòng có nhiều nút hơn số nút hiện thẳng.\nAfter:\n– Mở menu các hành động còn lại ngay dưới nút.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách chờ giao việc theo từng tab',
       mota='Thu hẹp danh sách của tab đang mở. Ô tìm nhanh tìm theo mã / số phiếu của tab; các ô lọc nằm trong khối Tìm kiếm nâng cao, '
            'khác nhau theo tab (đúng như ERP) và bật / tắt được bằng Cài đặt bộ lọc. Mọi điều kiện chỉ lọc trong phạm vi và trạng '
            'thái của tab.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập mã / số phiếu vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc của tab, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Ô chọn (người duyệt, trạng thái, người tạo, khách hàng, ngày tạo, công ty, phòng ban, bộ phận) lọc ngay khi đổi; ô gõ '
             'chữ (Hàng hóa, Số hợp đồng) lọc khi bấm Tìm kiếm / nhấn Enter; về trang 1.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.\n'
             '5. Hệ thống ghi nhớ bộ lọc 10 phút cho riêng tab đang mở.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1 (giữ tab, giữ phạm vi).\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Ô Khách hàng: gõ tối thiểu 2 ký tự mới hiện gợi ý (tối đa 30, toàn bộ danh mục khách hàng).\n'
           '• Chọn trạng thái khác trạng thái của tab (vd “Đang tạo” ở tab Hợp đồng) → luôn 0 dòng, vì tab chỉ chứa 1 trạng thái.\n'
           '• Chọn Công ty → ô Phòng ban chỉ còn phòng của công ty đó; bấm × trong ô chọn → xóa giá trị ô đó.',
       dacbiet='Ô tìm nhanh: khớp một phần mã / số phiếu, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối, không giới hạn ký tự; '
               '% và _ là ký tự đại diện. Số hợp đồng: tab Lắp đặt khớp một phần, tab Giao việc khác khớp ĐÚNG số hợp đồng ghi trên '
               'phiếu (giữ như ERP). Hàng hóa (tab BH): khớp một phần tên hàng hoặc mã hàng ở các dòng của phiếu. Ngày tạo: lấy '
               'trọn 2 ngày biên ở cả 5 tab. Công ty / Phòng ban / Bộ phận lọc theo đơn vị ghi trên chứng từ; mọi người chọn được mọi '
               'công ty. Ghi nhớ bộ lọc trên trình duyệt, 10 phút, riêng từng tab.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter_contract'),
               shot_caption='Khối Bộ lọc danh sách tab Hợp đồng đang mở tìm kiếm nâng cao'),
   extra=[(shot('02_filter_warranty'), 'Ô lọc tab Phiếu bảo hành'), (shot('02_filter_assembly'), 'Ô lọc tab Lắp đặt bàn giao'),
          (shot('02_filter_other'), 'Ô lọc tab Giao việc khác'), (shot('02b_filter_full'), 'Ô Trạng thái tab Hợp đồng đang mở')],
   ui=[
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý theo tab: “Tìm theo số hợp đồng” (HĐ, PL), “Tìm theo số phiếu bảo hành” (BH), “Tìm theo số phiếu yêu cầu” (LĐ, GVK)',
         '- Khớp một phần mã / số phiếu', '- Chỉ lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh và ô gõ chữ, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, về trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn', '- Bấm → mở / thu gọn khối ô lọc của tab.'),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Người duyệt hợp đồng', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', ['- Chỉ tab HĐ / PL', '- Mặc định: trống']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách theo tab', 'Không', 'Trống',
        ['- Mặc định: trống', '- HĐ / PL: Đang tạo, Chờ duyệt, Có hiệu lực, Đang quyết toán, Đã quyết toán, Đã hoàn thành, Đóng, Hủy, '
         'Không duyệt', '- BH: Đang tạo, Đã duyệt, Đang thực hiện, Đã hoàn thành', '- GVK: Đang tạo, Chờ giao việc, Đã giao việc, Từ chối',
         '- Tab Lắp đặt không có ô này', '- Chỉ giá trị trạng thái của tab mới ra dữ liệu']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', ['- Tab HĐ, PL, LĐ, GVK', '- Mặc định: trống']),
       ('Khách hàng', 'Dropdown', 'Enable', 'Tìm trong danh mục khách hàng', 'Không', 'Trống',
        ['- Gợi ý “Gõ để tìm khách hàng...”', '- Gõ tối thiểu 2 ký tự, tối đa 30 gợi ý', '- Lọc đúng khách hàng đã chọn']),
       ('Hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Chỉ tab Phiếu bảo hành', '- Khớp một phần tên hàng / mã hàng', '- Lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Số hợp đồng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Chỉ tab Lắp đặt (khớp một phần), Giao việc khác (khớp đúng)', '- Lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai ngày biên; được bỏ trống một đầu']),
       ('Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống', ['- Mọi tab, mọi người dùng', '- Mặc định: trống']),
       ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống', '- Chọn Công ty trước thì chỉ còn phòng ban của công ty đó.'),
       ('Bộ phận', 'Dropdown', 'Enable', 'Danh sách bộ phận', 'Không', 'Trống', '- Chỉ tab HĐ, PL, BH.'),
       ('Biểu tượng ổ khóa cạnh nhãn Công ty, Phòng ban, Bộ phận', 'Icon Button', 'Enable', '–', '–', 'Khóa đóng',
        ['- Chú thích “Hiện cả công ty đã khoá” (tương tự phòng ban, bộ phận)', '- Bấm → danh sách lựa chọn gồm cả đơn vị đã khóa; bấm lại để ẩn']),
   ],
   ev=[
       ('Đổi giá trị một ô chọn', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\nDuring:\n– Ghi nhận giá trị mới; giá trị không đổi thì bỏ qua.\n'
        'After:\n– Về trang 1 và nạp lại danh sách tab theo toàn bộ tiêu chí trong phạm vi.'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh và ô gõ chữ (Hàng hóa, Số hợp đồng), bỏ khoảng trắng đầu / cuối.\nDuring:\n– Tìm chứng từ '
        'có mã chứa chuỗi nhập (và điều kiện ô gõ chữ).\nAfter:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nAfter:\n– Xóa mọi tiêu chí của tab kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\nAfter:\n– Mở / thu gọn khối ô lọc; trạng thái mở được ghi nhớ cùng bộ lọc.'),
       ('Gõ vào ô Khách hàng', 'Change',
        'Before:\n– Đã gõ tối thiểu 2 ký tự.\nAfter:\n– Hiện tối đa 30 khách hàng khớp; chọn 1 khách hàng → lọc ngay.'),
       ('Quay lại màn trong 10 phút', 'System',
        'Before:\n– Người dùng vừa rời tab (sang tab khác, chi tiết chứng từ, màn Tạo phiếu giao việc).\n'
        'After:\n– Khôi phục bộ lọc, khách hàng đã chọn và trạng thái khối lọc của tab; quá 10 phút thì bộ lọc về trống.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị của từng tab',
       mota='Cho mỗi người dùng tự chọn những ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự. Cấu hình lưu riêng theo '
            'người dùng và theo từng tab của màn, không ảnh hưởng người khác và không làm đổi dữ liệu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê các mục lọc của tab kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng + tab, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ các mục theo thứ tự thiết kế; vẫn phải bấm Lưu.\n'
           '• Bỏ tích mục đang có giá trị lọc → ô bị ẩn.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bỏ thay đổi chưa lưu.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.',
       dacbiet='Số mục theo tab: HĐ / PL 6 (Người duyệt hợp đồng, Trạng thái, Người tạo, Khách hàng, Ngày tạo, Công ty – Phòng ban – Bộ '
               'phận); BH 5; Lắp đặt 5; Giao việc khác 6.'),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc (tab Hợp đồng)',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Cài đặt bộ lọc”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách theo tab', '–', 'Theo cấu hình đã lưu',
        ['- Người duyệt hợp đồng (HĐ, PL)', '- Trạng thái (trừ Lắp đặt)', '- Người tạo (trừ BH)', '- Khách hàng', '- Hàng hóa (BH)',
         '- Số hợp đồng (LĐ, GVK)', '- Ngày tạo', '- Công ty – Phòng ban (– Bộ phận ở HĐ, PL, BH)']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → ô lọc đó không hiện.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích lại đủ các mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
       ('Khối Tìm kiếm nâng cao sau khi lưu', 'Label', 'Hiển thị', '–', '–', 'Theo cấu hình', '- Chỉ hiện ô đã tích, đúng thứ tự.'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình đang lưu của tab (chưa lưu lần nào → đủ các mục).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại và tab.\nDuring:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ các mục, thứ tự thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách từng tab',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp các cột của bảng tab đang mở. Ba cột STT, Mã phiếu (Số phiếu), Hành động bị '
            'khóa; cấu hình lưu theo người dùng và theo tab trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê các cột của tab theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ cột (HĐ / PL 11, BH / LĐ / GVK 8). Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ sau khi tải lại '
               'trang, đăng nhập lại, đổi trình duyệt; người dùng khác không bị ảnh hưởng. Cột đang hiện được tích sẵn khi Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột (tab Hợp đồng)',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách theo tab', '–', 'Theo cấu hình đã lưu',
        ['- HĐ / PL: STT, Mã phiếu, Tổng thanh toán, Khách hàng, Người liên hệ - SĐT, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, '
         'Trạng thái, Hành động', '- BH: STT, Mã phiếu, Khách hàng, Người liên hệ - SĐT, Người tạo, Ngày tạo, Trạng thái, Hành động',
         '- LĐ / GVK: STT, Số phiếu, Số hợp đồng, Khách hàng, Người tạo, Ngày tạo, Trạng thái, Hành động']),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Mã phiếu / Số phiếu, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/m cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', ['- n = số cột đang tích', '- m = số cột của tab']),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu của người dùng cho tab.'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Cột khóa không đổi được vị trí.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change',
        'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/m cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại và tab.\nDuring:\n– Gửi danh sách cột đã tích theo thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5
fr(5, 'Tạo phiếu giao việc', usecase=('FR-05', 'Tạo phiếu giao việc', 'crud', A_TN),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo phiếu giao việc từ chứng từ chờ giao việc',
       mota='Từ 1 dòng của bất kỳ tab nào, phòng tiếp nhận bấm Tạo phiếu giao việc để mở màn Tạo phiếu giao việc (HRM) với chứng từ nguồn '
            'đã chọn sẵn. Màn này chỉ kiểm điều kiện mở; nội dung phiếu, kiểm tra và lưu thuộc tài liệu Phiếu giao việc. Lưu xong, '
            'số lượng đã giao được trừ vào SL chưa giao việc của chứng từ nguồn (BR-03, BR-10).',
       tacnhan=TN_TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Dòng có nút Tạo phiếu giao việc (BR-05).\n'
                '3. Chứng từ nguồn còn SL chưa giao việc (đang nằm trong tab).',
       chinh='1. Người dùng bấm Tạo phiếu giao việc (dấu +) ở cột Hành động.\n'
             '2. Tab Hợp đồng: hệ thống kiểm tra hợp đồng có phụ lục giảm đang Chờ duyệt không; có → báo %s, dừng.\n'
             '3. Hệ thống mở màn Tạo phiếu giao việc trong cùng tab trình duyệt, chứng từ nguồn chọn sẵn theo tab: hợp đồng / PL / phiếu '
             'bảo hành, phiếu yêu cầu lắp đặt, hoặc phiếu yêu cầu giao việc khác.\n'
             '4. Màn Tạo phiếu giao việc nạp các dòng còn SL chưa giao việc của chứng từ nguồn (SL giao mặc định = SL còn).\n'
             '5. Người dùng lập và lưu phiếu giao việc ở màn đó (đặc tả ở tài liệu Phiếu giao việc).\n'
             '6. Lưu xong, hệ thống trừ SL đã giao: dòng hết SL chưa giao việc thì chứng từ rời khỏi tab; phiếu yêu cầu giao việc khác '
             'chuyển Đã giao việc; phiếu yêu cầu lắp đặt hết SL chuyển Đang giao việc; phiếu bảo hành hết SL bỏ đánh dấu chờ giao.' % PLG,
       phu='• Hợp đồng có PL giảm Chờ duyệt → thông báo %s, ở lại danh sách.\n'
           '• Máy chủ lỗi khi kiểm tra → thông báo lỗi trả về hoặc “Thao tác thất bại”.\n'
           '• Màn Tạo phiếu giao việc không lấy được chứng từ nguồn (không còn quyền / đã giao hết / đổi trạng thái) → thông báo lỗi và '
           'quay về màn này đúng tab của nguồn.\n'
           '• Ở màn Tạo bấm Quay lại → về Phiếu chờ giao việc đúng tab của chứng từ nguồn (có hộp “chưa lưu” nếu đã nhập).\n'
           '• Tab Phiếu bảo hành: nút luôn hiện; người không có quyền “%s” bị màn Tạo từ chối.' % (PLG, Q1),
       dacbiet='Tab PL bổ sung, Phiếu bảo hành, Lắp đặt, Giao việc khác mở thẳng, không kiểm PL giảm (giữ như ERP). Nút hiện theo cờ do '
               'hệ thống tính lại mỗi lần nạp danh sách.'),
   layout=dict(menu=M_BH + ' => Tạo phiếu giao việc', shot=shot('40_create_pgv'),
               shot_caption='Màn Tạo phiếu giao việc mở từ dòng tab Phiếu bảo hành',
               note='Nút Tạo phiếu giao việc nằm ở cột Hành động của cả 5 tab; ảnh chụp mở từ tab Phiếu bảo hành.'),
   extra=[(shot('01b_row_more'), 'Cột Hành động tab Hợp đồng (dòng 1 bật đủ cờ để minh họa)')],
   ui_kw=dict(required=False),
   ui=[
       ('Nút Tạo phiếu giao việc', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
        ['- Biểu tượng dấu + trong vòng tròn, chú thích “Tạo phiếu giao việc”', '- HĐ / PL: Q1 + phòng tiếp nhận = phòng mình',
         '- LĐ / GVK: phòng tiếp nhận = phòng mình', '- BH: mọi dòng']),
       ('Thông báo PL giảm chờ duyệt', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- %s (chỉ tab Hợp đồng).' % PLG),
       ('Thông báo lỗi khác', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- Câu lỗi hệ thống trả về, mặc định “Thao tác thất bại”.'),
       ('Màn Tạo phiếu giao việc', 'Label', 'Hiển thị', '–', 'Ẩn', '- Mở trong cùng tab trình duyệt; tiêu đề “Tạo phiếu giao việc”.'),
       ('Khối chứng từ nguồn', 'Label', 'Read-only', '–', 'Theo dòng đã bấm',
        ['- HĐ / PL / BH: thông tin hợp đồng / phiếu bảo hành', '- LĐ: phiếu yêu cầu lắp đặt', '- GVK: phiếu yêu cầu giao việc khác']),
       ('Bảng dòng cần giao', 'Table/Grid', 'Enable', '≥ 0', 'Theo SL chưa giao việc',
        ['- Chỉ các dòng còn SL chưa giao việc', '- SL giao mặc định = SL còn']),
       ('Nút Quay lại (màn Tạo)', 'Button', 'Enable', '–', 'Hiển thị', '- Về Phiếu chờ giao việc đúng tab của chứng từ nguồn.'),
       ('Thông báo tạo thành công', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Tạo phiếu giao việc thành công.” (màn Tạo phiếu giao việc).'),
       ('Dòng chứng từ sau khi tạo', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Còn SL chưa giao việc: vẫn nằm trong tab', '- Hết SL: rời khỏi tab, tổng N giảm 1']),
       ('Cột Trạng thái sau khi tạo', 'Badge', 'Read-only', '–', 'Theo dữ liệu',
        '- Không đổi trên màn này (dòng chỉ còn / mất); trạng thái mới xem ở màn nguồn.'),
       ('Nút ba chấm “Hành động khác”', 'Icon Button', 'Enable', '–', 'Theo số nút', '- Chứa các nút còn lại khi dòng có nhiều hành động.'),
   ],
   ev=[
       ('Bấm Tạo phiếu giao việc (tab Hợp đồng)', 'Click',
        'Before:\n– Nút chỉ hiện khi có quyền “' + Q1 + '” và phòng tiếp nhận = phòng của người đăng nhập.\n'
        '– Kiểm tra hợp đồng có phụ lục giảm Chờ duyệt.\n'
        'During:\n– Có PL giảm Chờ duyệt → hiển thị ' + PLG + ' và dừng xử lý.\n– Lỗi khác → hiển thị câu lỗi trả về.\n' + ERR + '\n'
        'After:\n– Mở màn Tạo phiếu giao việc với hợp đồng chọn sẵn.'),
       ('Bấm Tạo phiếu giao việc (tab PL, BH, LĐ, GVK)', 'Click',
        'Before:\n– Nút hiện theo BR-05 của tab.\nDuring:\n– Không kiểm thêm ở màn này.\n'
        'After:\n– Mở màn Tạo phiếu giao việc với chứng từ nguồn chọn sẵn (phụ lục / phiếu bảo hành / phiếu yêu cầu lắp đặt / phiếu '
        'yêu cầu giao việc khác).'),
       ('Màn Tạo không lấy được nguồn', 'System',
        'Before:\n– Màn Tạo kiểm lại quyền, phòng tiếp nhận, trạng thái và SL còn của nguồn.\n'
        'During:\n– Không đạt → thông báo lỗi.\nAfter:\n– Quay về Phiếu chờ giao việc đúng tab của nguồn.'),
       ('Lưu phiếu giao việc thành công (màn Tạo)', 'System',
        'Before:\n– Kiểm tra do màn Phiếu giao việc đảm nhận.\nDuring:\n– Ghi phiếu giao việc trạng thái Đang giao.\n'
        'After:\n– SL đang giao tăng → SL chưa giao việc của nguồn giảm; nguồn hết SL thì rời tab; YC giao việc khác → Đã giao việc; '
        'YC lắp đặt hết SL → Đang giao việc; phiếu bảo hành hết SL → bỏ đánh dấu chờ giao.'),
       ('Bấm Quay lại ở màn Tạo', 'Click',
        'Before:\n– Đã nhập thì hỏi “chưa lưu” (Thoát / Ở lại).\nAfter:\n– Về Phiếu chờ giao việc đúng tab nguồn; bộ lọc tab khôi phục (10 phút).'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Từ chối tiếp nhận xử lý', usecase=('FR-06', 'Từ chối tiếp nhận xử lý', 'action', A_TN),
   rule=('- Thông báo, Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Từ chối tiếp nhận xử lý hợp đồng / PL bổ sung',
       mota='Phòng được chỉ định tiếp nhận trả hợp đồng (tab Hợp đồng) hoặc phụ lục bổ sung (tab PL bổ sung) lại cho người lập để chọn '
            'phòng khác. Lý do bắt buộc. Chứng từ vẫn Có hiệu lực; hệ thống xóa phòng tiếp nhận, lưu lý do và báo cho người lập.',
       tacnhan=TN_TN,
       dieukien='1. Người dùng đăng nhập thành công, có quyền “%s”.\n2. Phòng tiếp nhận của chứng từ = phòng của người đăng nhập.\n'
                '3. Tab Hợp đồng: hợp đồng chưa có phiếu giao việc nào (trừ phiếu đã hủy).' % Q1,
       chinh='1. Người dùng bấm Từ chối tiếp nhận xử lý (biểu tượng người gạch đỏ) ở cột Hành động.\n'
             '2. Hệ thống mở hộp “Từ chối tiếp nhận xử lý” với nội dung “Bạn chắc muốn từ chối tiếp nhận xử lý cho hợp đồng '
             '\'<mã>\'?” và ô Lý do từ chối (bắt buộc).\n'
             '3. Người dùng nhập lý do, bấm Từ chối tiếp nhận.\n'
             '4. Hệ thống kiểm tra lại điều kiện; xóa phòng tiếp nhận của chứng từ, lưu lý do từ chối.\n'
             '5. Tab Hợp đồng: hệ thống ghi một dòng lịch sử “Thay đổi thông tin” (phòng tiếp nhận, kèm lý do) trong lịch sử hợp đồng và '
             'gửi thông báo cho người lập hợp đồng.\n'
             '6. Tab PL bổ sung: hệ thống gửi thông báo “HĐDV – Từ chối” cho người lập phụ lục (khách hàng, người từ chối, lý do), bấm '
             'thông báo mở màn chọn lại phòng ở hệ thống ERP; không ghi lịch sử.\n'
             '7. Hệ thống hiển thị “Từ chối tiếp nhận xử lý thành công.” và nạp lại danh sách.',
       phu='• Bỏ trống lý do → viền đỏ, %s dưới ô; hộp không đóng, không gửi.\n'
           '• Bấm Hủy / (x) → đóng hộp, không thay đổi; click ra ngoài hộp → hộp đóng, không thực hiện.\n'
           '• Hợp đồng không còn đủ điều kiện (đã có phiếu giao việc, đã đổi phòng…) → “Không thể từ chối tiếp nhận hợp đồng này”; PL → %s; '
           'danh sách nạp lại.\n'
           '• Không có quyền “%s” (PL) → hệ thống từ chối, báo không có quyền.\n'
           '• Sau khi từ chối: người không có V1 không còn thấy dòng (không còn phòng tiếp nhận); người có V1 vẫn thấy nhưng mất nút.'
           % (REQ_REJ, CONFLICT, Q1),
       dacbiet='Lý do không giới hạn độ dài, bỏ khoảng trắng đầu / cuối khi kiểm. Khóa thao tác trong lúc gửi (bấm liên tục chỉ gửi 1 '
               'lần). Thành công hay thất bại đều nạp lại danh sách.'),
   layout=dict(menu=M_HD + ' => Từ chối tiếp nhận xử lý', shot=shot('30_reject'), shot_caption='Hộp Từ chối tiếp nhận xử lý',
               note='Hộp xác nhận được mở ngay trên màn hình danh sách (tab Hợp đồng hoặc PL bổ sung).'),
   extra=[(shot('30b_reject_required'), 'Bỏ trống lý do — báo lỗi dưới ô'), (shot('33_reject_pl'), 'Từ chối tiếp nhận ở tab PL bổ sung')],
   ui=[
       ('Nút Từ chối tiếp nhận xử lý', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện',
        ['- Biểu tượng người gạch, màu đỏ', '- Chỉ tab HĐ, PL khi đủ điều kiện BR-06']),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Từ chối tiếp nhận xử lý” kèm biểu tượng cảnh báo đỏ.'),
       ('Nội dung hộp', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Bạn chắc muốn từ chối tiếp nhận xử lý cho hợp đồng \'<mã>\'?”'),
       ('Lý do từ chối', 'Textarea', 'Enable', 'Không giới hạn ký tự', 'Có', 'Trống',
        ['- Nhãn có dấu * đỏ', '- Gợi ý “Nhập lý do từ chối”', '- Bỏ trống / chỉ khoảng trắng → lỗi dưới ô']),
       ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- %s, ô viền đỏ.' % REQ_REJ),
       ('Nút Từ chối tiếp nhận', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Màu đỏ; gửi từ chối.'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng hộp, không thực hiện.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống Hủy.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Từ chối tiếp nhận xử lý thành công.”', '- “Không thể từ chối tiếp nhận hợp đồng này”', '- ' + CONFLICT,
         '- “Từ chối tiếp nhận xử lý không thành công”']),
       ('Thông báo gửi người lập', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Chuông thông báo của người lập hợp đồng / phụ lục', '- Nội dung có khách hàng, người từ chối, lý do']),
       ('Dòng sau khi từ chối', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Không có V1: dòng rời khỏi tab', '- Có V1: dòng còn, mất nút Tạo phiếu giao việc / Từ chối']),
   ],
   ev=[
       ('Bấm Từ chối tiếp nhận xử lý', 'Click',
        'Before:\n– Nút chỉ hiện khi đủ điều kiện BR-06.\nAfter:\n– Mở hộp xác nhận có ô Lý do từ chối trống.'),
       ('Bấm Từ chối tiếp nhận trong hộp', 'Click',
        'Before:\n– Kiểm tra quyền “' + Q1 + '”; nếu không có quyền → hệ thống từ chối, báo không có quyền và dừng xử lý.\n'
        '– Kiểm tra phòng tiếp nhận = phòng mình, HĐ Có hiệu lực và chưa có phiếu giao việc (HĐ).\n'
        'During:\n– Lý do trống → hiển thị ' + REQ_REJ + ', hộp không đóng.\n'
        '– Không còn đủ điều kiện → “Không thể từ chối tiếp nhận hợp đồng này” (HĐ) / ' + CONFLICT + ' (PL).\n' + ERR + '\n'
        'After:\n– Xóa phòng tiếp nhận, lưu lý do từ chối.\n– Ghi một dòng lịch sử “Thay đổi thông tin” trong lịch sử của hợp đồng (HĐ).\n'
        '– Gửi thông báo cho người lập hợp đồng / phụ lục.\n– Hiển thị “Từ chối tiếp nhận xử lý thành công.”; nạp lại danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không gửi.\nAfter:\n– Đóng hộp, danh sách giữ nguyên.'),
       ('Click ra ngoài hộp', 'Click', 'Before:\n– Không gửi.\nAfter:\n– Hộp đóng, không thực hiện thao tác.'),
       ('Gõ vào ô Lý do', 'Change', 'Before:\n– Ô đang báo lỗi.\nAfter:\n– Lỗi xóa ở lần bấm Từ chối tiếp nhận tiếp theo nếu đã có chữ.'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Đóng hợp đồng', usecase=('FR-07', 'Đóng hợp đồng', 'action', A_LAP),
   rule=('- Thông báo, Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Đóng hợp đồng dịch vụ đang chờ giao việc',
       mota='Người lập hoặc người quản lý phòng của hợp đồng đóng hợp đồng không còn làm tiếp: hợp đồng chuyển Có hiệu lực → Đóng, các phụ '
            'lục bổ sung / giảm của nó cũng chuyển Đóng, hợp đồng rời khỏi hàng đợi. Chỉ cho đóng khi chưa phát sinh chứng từ phía sau.',
       tacnhan='Người dùng có quyền thực hiện chức năng: người lập hợp đồng hoặc người quản lý phòng ban của hợp đồng (không cần quyền riêng).',
       dieukien=DK_HD + '\n4. Hợp đồng và phụ lục chưa có phiếu giao việc (trừ đã hủy), yêu cầu xuất kho, yêu cầu nhập kho, yêu cầu '
                        'hạch toán dịch vụ.',
       chinh='1. Người dùng bấm Đóng hợp đồng trong nút ba chấm “Hành động khác” ở tab Hợp đồng.\n'
             '2. Hệ thống mở hộp “Đóng hợp đồng”: “Đóng hợp đồng \'<mã>\'? Các phụ lục của hợp đồng cũng được đóng theo.”.\n'
             '3. Người dùng bấm Đóng hợp đồng.\n'
             '4. Hệ thống kiểm tra lại điều kiện; chuyển hợp đồng sang Đóng, các phụ lục bổ sung / giảm cũng sang Đóng; đóng nhu cầu dịch '
             'vụ liên quan.\n'
             '5. Hệ thống ghi một dòng lịch sử “Thay đổi trạng thái” (Có hiệu lực → Đóng) trong lịch sử hợp đồng.\n'
             '6. Hệ thống hiển thị “Đóng hợp đồng thành công.” và nạp lại danh sách (hợp đồng rời tab).',
       phu='• Bấm Hủy / (x) → đóng hộp, không thay đổi; click ra ngoài hộp → hộp đóng, không thực hiện.\n'
           '• Hợp đồng đã phát sinh chứng từ phía sau / không còn quyền → “Không thể đóng hợp đồng này (đã phát sinh chứng từ phía sau '
           'hoặc không đủ quyền)”, danh sách nạp lại.\n'
           '• Không gửi thông báo (giữ như ERP).\n'
           '• Máy chủ lỗi → thông báo lỗi trả về, mặc định “Thao tác thất bại”.',
       dacbiet='Không cần lý do. ERP hiện nút này ở màn chờ nhưng không chạy; HRM cho chạy thật (lệch ERP có chủ đích, spec mục 7). '
               'Khóa thao tác trong lúc gửi.'),
   layout=dict(menu=M_HD + ' => Đóng hợp đồng', shot=shot('31_close'), shot_caption='Hộp xác nhận Đóng hợp đồng',
               note='Hộp xác nhận được mở ngay trên màn hình danh sách tab Hợp đồng.'),
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Đóng hợp đồng', 'Icon Button', 'Enable / Ẩn', 'Theo điều kiện', ['- Biểu tượng hộp lưu trữ', '- Chỉ tab HĐ, đủ BR-07']),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Hiển thị', '- “Đóng hợp đồng” kèm biểu tượng dấu hỏi.'),
       ('Nội dung hộp', 'Label', 'Hiển thị', 'Hiển thị', '- “Đóng hợp đồng \'<mã>\'? Các phụ lục của hợp đồng cũng được đóng theo.”'),
       ('Nút Đóng hợp đồng (trong hộp)', 'Button', 'Enable', 'Hiển thị', '- Màu xanh; thực hiện đóng.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không thực hiện.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống Hủy.'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', 'Ẩn', '- “Đóng hợp đồng thành công.”'),
       ('Thông báo không đủ điều kiện', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        '- “Không thể đóng hợp đồng này (đã phát sinh chứng từ phía sau hoặc không đủ quyền)”'),
       ('Thông báo lỗi khác', 'Toast / Alert', 'Hiển thị', 'Ẩn', '- Câu lỗi trả về, mặc định “Thao tác thất bại”.'),
       ('Dòng hợp đồng sau khi đóng', 'Table/Grid', 'Read-only', 'Theo dữ liệu', '- Rời khỏi tab Hợp đồng; tổng N giảm 1.'),
       ('Phụ lục của hợp đồng', 'Table/Grid', 'Read-only', 'Theo dữ liệu', '- Phụ lục bổ sung đang Có hiệu lực cũng rời tab PL bổ sung.'),
   ],
   ev=[
       ('Bấm Đóng hợp đồng', 'Click', 'Before:\n– Nút chỉ hiện khi đủ BR-07.\nAfter:\n– Mở hộp xác nhận.'),
       ('Bấm Đóng hợp đồng trong hộp', 'Click',
        'Before:\n– Kiểm tra người đăng nhập là người lập hoặc quản lý phòng của hợp đồng; nếu không → “Không thể đóng hợp đồng này '
        '(đã phát sinh chứng từ phía sau hoặc không đủ quyền)” và dừng xử lý.\n– Kiểm tra Có hiệu lực, chưa có chứng từ phía sau.\n'
        'During:\n– Chuyển hợp đồng + phụ lục sang Đóng trong 1 lần.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Thay đổi trạng thái” Có hiệu lực → Đóng của hợp đồng.\n'
        '– Hiển thị “Đóng hợp đồng thành công.”; nạp lại danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không gửi.\nAfter:\n– Đóng hộp, danh sách giữ nguyên.'),
       ('Click ra ngoài hộp', 'Click', 'Before:\n– Không gửi.\nAfter:\n– Hộp đóng, không thực hiện thao tác.'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'Hủy duyệt hợp đồng', usecase=('FR-08', 'Hủy duyệt hợp đồng', 'action', A_LAP),
   rule=('- Thông báo, Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Hủy duyệt hợp đồng dịch vụ đang có hiệu lực',
       mota='Người quản lý phòng ban của hợp đồng hủy duyệt hợp đồng đang Có hiệu lực mà chưa làm gì phía sau: hợp đồng về Không duyệt, '
            'lưu lý do, báo người lập và rời khỏi hàng đợi. Lý do bắt buộc.',
       tacnhan='Người dùng có quyền thực hiện chức năng: người quản lý phòng ban của hợp đồng (trong công ty đang làm việc).',
       dieukien=DK_HD + '\n4. Chưa có chứng từ phía sau và không còn phụ lục bổ sung / giảm đang sống (không ở Đóng / Hủy / Không duyệt).',
       chinh='1. Người dùng bấm Hủy duyệt hợp đồng trong nút ba chấm “Hành động khác” ở tab Hợp đồng.\n'
             '2. Hệ thống mở hộp “Hủy duyệt hợp đồng”: “Hủy duyệt hợp đồng \'<mã>\'? Hợp đồng sẽ về trạng thái Không duyệt.” và ô Lý '
             'do hủy duyệt (bắt buộc).\n'
             '3. Người dùng nhập lý do, bấm Hủy duyệt.\n'
             '4. Hệ thống kiểm tra lại điều kiện; chuyển hợp đồng sang Không duyệt, lưu lý do; đóng nhu cầu dịch vụ liên quan.\n'
             '5. Hệ thống ghi một dòng lịch sử “Thay đổi trạng thái” (Có hiệu lực → Không duyệt, kèm lý do) trong lịch sử hợp đồng.\n'
             '6. Hệ thống gửi thông báo hủy duyệt cho người lập hợp đồng.\n'
             '7. Hệ thống hiển thị “Hủy duyệt hợp đồng thành công.” và nạp lại danh sách (hợp đồng rời tab).',
       phu='• Bỏ trống lý do → viền đỏ, %s dưới ô; hộp không đóng.\n'
           '• Bấm Hủy / (x) → đóng hộp; click ra ngoài hộp → hộp đóng, không thực hiện.\n'
           '• Không còn đủ điều kiện → “Không thể hủy duyệt hợp đồng này (đã phát sinh chứng từ phía sau hoặc không đủ quyền)”.\n'
           '• Máy chủ lỗi → câu lỗi trả về, mặc định “Thao tác thất bại”.' % REQ_UN,
       dacbiet='ERP hiện nút này ở màn chờ nhưng không chạy; HRM cho chạy thật (lệch ERP có chủ đích). Lý do không giới hạn độ dài. Khóa '
               'thao tác trong lúc gửi.'),
   layout=dict(menu=M_HD + ' => Hủy duyệt hợp đồng', shot=shot('32_unapprove'), shot_caption='Hộp Hủy duyệt hợp đồng',
               note='Hộp xác nhận được mở ngay trên màn hình danh sách tab Hợp đồng.'),
   ui=[
       ('Nút Hủy duyệt hợp đồng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo điều kiện', ['- Biểu tượng mũi tên quay lại, màu đỏ', '- Chỉ tab HĐ, đủ BR-08']),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Hủy duyệt hợp đồng” kèm biểu tượng cảnh báo đỏ.'),
       ('Nội dung hộp', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Hủy duyệt hợp đồng \'<mã>\'? Hợp đồng sẽ về trạng thái Không duyệt.”'),
       ('Lý do hủy duyệt', 'Textarea', 'Enable', 'Không giới hạn ký tự', 'Có', 'Trống',
        ['- Nhãn có dấu * đỏ', '- Gợi ý “Nhập lý do hủy duyệt”', '- Bỏ trống / chỉ khoảng trắng → lỗi dưới ô']),
       ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- %s, ô viền đỏ.' % REQ_UN),
       ('Nút Hủy duyệt', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Màu đỏ; thực hiện hủy duyệt.'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng hộp, không thực hiện.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống Hủy.'),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Hủy duyệt hợp đồng thành công.”', '- “Không thể hủy duyệt hợp đồng này (đã phát sinh chứng từ phía sau hoặc không đủ quyền)”']),
       ('Thông báo gửi người lập', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- Chuông thông báo của người lập hợp đồng, kèm lý do.'),
       ('Dòng hợp đồng sau khi hủy duyệt', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Rời khỏi tab Hợp đồng.'),
   ],
   ev=[
       ('Bấm Hủy duyệt hợp đồng', 'Click', 'Before:\n– Nút chỉ hiện khi đủ BR-08.\nAfter:\n– Mở hộp có ô Lý do hủy duyệt trống.'),
       ('Bấm Hủy duyệt trong hộp', 'Click',
        'Before:\n– Kiểm tra người đăng nhập quản lý phòng của hợp đồng; nếu không → “Không thể hủy duyệt hợp đồng này (đã phát sinh '
        'chứng từ phía sau hoặc không đủ quyền)” và dừng xử lý.\n– Kiểm tra Có hiệu lực, không chứng từ phía sau, không phụ lục sống.\n'
        'During:\n– Lý do trống → hiển thị ' + REQ_UN + ', hộp không đóng.\n' + ERR + '\n'
        'After:\n– Chuyển hợp đồng sang Không duyệt, lưu lý do.\n– Ghi một dòng lịch sử “Thay đổi trạng thái” kèm lý do.\n'
        '– Gửi thông báo cho người lập hợp đồng.\n– Hiển thị “Hủy duyệt hợp đồng thành công.”; nạp lại danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không gửi.\nAfter:\n– Đóng hộp, danh sách giữ nguyên.'),
       ('Click ra ngoài hộp', 'Click', 'Before:\n– Không gửi.\nAfter:\n– Hộp đóng, không thực hiện thao tác.'),
   ])

# ------------------------------------------------------------ 2.9
fr(9, 'Mở chức năng ở hệ thống ERP',
   rule=('- Màn Danh sách và Thông báo.', 'notice'),
   intro=dict(
       ten='Quyết toán hợp đồng, Xuất Excel 1 phiếu yêu cầu lắp đặt và các liên kết sang hệ thống ERP',
       mota='Các màn đích chưa chuyển sang HRM được mở ở hệ thống ERP trong tab trình duyệt mới: Quyết toán hợp đồng (tab Hợp đồng), Xuất '
            'Excel 1 phiếu yêu cầu lắp đặt (tab Lắp đặt bàn giao), Số phiếu yêu cầu lắp đặt và Số hợp đồng bán (tab Lắp đặt, Giao việc '
            'khác). Mọi thao tác tiếp theo làm bên ERP; màn này không đổi dữ liệu.',
       tacnhan='Người dùng có quyền thực hiện chức năng: Quyết toán — người lập hợp đồng; các liên kết còn lại — mọi người xem tab.',
       dieukien=DK + '\n4. Hệ thống đã cấu hình đường dẫn ERP.',
       chinh='1. Người dùng bấm Quyết toán hợp đồng (tab HĐ), Xuất Excel 1 phiếu (tab LĐ), Số phiếu (tab LĐ) hoặc Số hợp đồng (tab LĐ, '
             'GVK).\n'
             '2. Hệ thống dựng đường dẫn ERP kèm mã chứng từ: màn tạo quyết toán theo hợp đồng / xuất Excel phiếu yêu cầu lắp đặt / xem '
             'phiếu yêu cầu lắp đặt / xem hợp đồng bán.\n'
             '3. Hệ thống mở đường dẫn ở tab trình duyệt mới.\n'
             '4. Màn Phiếu chờ giao việc giữ nguyên tab, trang, bộ lọc.',
       phu='• Chưa cấu hình đường dẫn ERP → thông báo %s, không mở gì (Quyết toán, Xuất Excel 1 phiếu); liên kết Số phiếu / Số hợp đồng '
           'hiện chữ thường không bấm được.\n'
           '• Người dùng chưa đăng nhập ERP → ERP tự yêu cầu đăng nhập (ngoài phạm vi màn này).\n'
           '• Phiếu không gắn hợp đồng → ô Số hợp đồng trống, không có liên kết.\n'
           '• Trình duyệt chặn cửa sổ mới → người dùng cho phép rồi bấm lại.' % NO_ERP,
       dacbiet='Quyết toán chỉ hiện với người lập hợp đồng (không đặc cách Super admin). Xuất Excel 1 phiếu luôn hiện ở tab Lắp đặt. '
               'Khi các màn đích chuyển sang HRM sẽ đổi sang mở HRM.'),
   layout=dict(menu=M_HD + ' => Quyết toán hợp đồng', shot=shot('01b_row_more'),
               shot_caption='Menu Hành động khác tab Hợp đồng (Quyết toán hợp đồng)',
               note='Các liên kết ERP nằm ở cột Hành động / cột Số phiếu, Số hợp đồng của danh sách.'),
   extra=[(shot('01_list_assembly'), 'Tab Lắp đặt bàn giao: Số phiếu, Số hợp đồng và nút Xuất Excel 1 phiếu mở ERP')],
   ui_kw=dict(required=False),
   ui=[
       ('Nút Quyết toán hợp đồng', 'Icon Button', 'Enable / Ẩn', '–', 'Theo điều kiện',
        ['- Biểu tượng máy tính', '- Tab HĐ, người đăng nhập là người lập hợp đồng', '- Bấm → mở màn tạo quyết toán hợp đồng ở ERP, tab mới']),
       ('Nút Xuất Excel 1 phiếu', 'Icon Button', 'Enable', '–', 'Hiển thị',
        ['- Biểu tượng file Excel, chú thích “Xuất Excel”', '- Tab Lắp đặt, mọi dòng', '- Bấm → ERP tải file phiếu yêu cầu lắp đặt']),
       ('Liên kết Số phiếu (Lắp đặt)', 'Link', 'Enable', '–', 'Hiển thị', '- Bấm → xem phiếu yêu cầu lắp đặt ở ERP, tab mới.'),
       ('Liên kết Số hợp đồng', 'Link', 'Enable', '–', 'Hiển thị',
        ['- Tab Lắp đặt, Giao việc khác', '- Bấm → xem hợp đồng bán ở ERP, tab mới', '- Trống khi không gắn hợp đồng']),
       ('Thông báo chưa cấu hình', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- %s.' % NO_ERP),
       ('Tab trình duyệt mới', 'Label', 'Hiển thị', '–', 'Ẩn', '- Màn ERP tương ứng; màn HRM giữ nguyên ở tab cũ.'),
       ('Nút ba chấm “Hành động khác”', 'Icon Button', 'Enable', '–', 'Theo số nút', '- Chứa Quyết toán hợp đồng khi dòng có nhiều nút.'),
       ('Danh sách sau khi quay lại', 'Table/Grid', 'Read-only', '–', 'Giữ nguyên', '- Không nạp lại, không đổi trang / bộ lọc.'),
       ('Dữ liệu quyết toán', 'Label', 'Read-only', '–', 'Theo ERP', '- Hợp đồng chuyển Đang quyết toán ở ERP thì rời tab Hợp đồng ở lần nạp sau.'),
       ('Chữ Số phiếu khi chưa cấu hình', 'Label', 'Read-only', '–', 'Theo cấu hình', '- Hiện chữ thường, không bấm được.'),
       ('Dòng không gắn hợp đồng', 'Label', 'Read-only', '–', 'Trống', '- Ô Số hợp đồng trống.'),
   ],
   ev=[
       ('Bấm Quyết toán hợp đồng', 'Click',
        'Before:\n– Nút chỉ hiện với người lập hợp đồng.\nDuring:\n– Chưa cấu hình đường dẫn ERP → hiển thị ' + NO_ERP + '.\n'
        'After:\n– Mở màn tạo quyết toán hợp đồng ở ERP (tab mới), kèm hợp đồng.'),
       ('Bấm Xuất Excel 1 phiếu', 'Click',
        'Before:\n– Tab Lắp đặt, mọi dòng.\nDuring:\n– Chưa cấu hình đường dẫn ERP → hiển thị ' + NO_ERP + '.\n'
        'After:\n– Mở đường dẫn xuất Excel phiếu yêu cầu lắp đặt ở ERP (tab mới).'),
       ('Bấm Số phiếu (Lắp đặt)', 'Click', 'Before:\n– Có đường dẫn ERP.\nAfter:\n– Mở phiếu yêu cầu lắp đặt ở ERP (tab mới).'),
       ('Bấm Số hợp đồng', 'Click', 'Before:\n– Phiếu có hợp đồng bán.\nAfter:\n– Mở hợp đồng ở ERP (tab mới).'),
       ('Quay lại tab HRM', 'System', 'Before:\n– Màn không tự nạp lại.\nAfter:\n– Danh sách giữ nguyên; dữ liệu mới khi tải lại / đổi trang.'),
   ])

# ------------------------------------------------------------ 2.10
fr(10, 'Xem chi tiết chứng từ nguồn',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Mở màn chi tiết của chứng từ nguồn',
       mota='Bấm mã phiếu ở tab Phiếu bảo hành hoặc số phiếu ở tab Giao việc khác để mở màn chi tiết của chứng từ đó trong HRM (chỉ đọc). '
            'Màn chi tiết thuộc tài liệu của màn nguồn; mục này chỉ đặc tả cách mở và quay lại. Tab Hợp đồng / PL bổ sung để mã chữ '
            'thường (giữ như ERP); tab Lắp đặt mở ERP (mục 2.9).',
       tacnhan=TN,
       dieukien=DK + '\n4. Người dùng có quyền xem chứng từ ở màn nguồn.',
       chinh='1. Người dùng bấm Mã phiếu (tab Phiếu bảo hành) hoặc Số phiếu (tab Giao việc khác).\n'
             '2. Hệ thống ghi nhớ bộ lọc của tab (10 phút).\n'
             '3. Hệ thống mở màn chi tiết Phiếu bảo hành / Phiếu yêu cầu giao việc khác trong cùng tab trình duyệt.\n'
             '4. Người dùng xem thông tin; bấm Quay lại (hoặc nút lùi của trình duyệt).\n'
             '5. Hệ thống về Phiếu chờ giao việc, khôi phục tab, bộ lọc.',
       phu='• Không có quyền xem chứng từ ở màn nguồn → màn nguồn chuyển sang trang không tìm thấy / báo không có quyền.\n'
           '• Chứng từ vừa bị đổi / xóa ở màn nguồn → màn nguồn báo không tìm thấy.\n'
           '• Quay lại sau 10 phút → bộ lọc về trống, trang 1.\n'
           '• Mã dài tự xuống dòng; bấm vào phần nào của mã cũng mở chi tiết.',
       dacbiet='Liên kết dạng chữ xanh gạch chân. Màn chi tiết phiếu bảo hành đã sửa theo ERP ở #11985 (dấu *, in đậm thiết bị, VAT).'),
   layout=dict(menu=M_BH + ' => Mã phiếu', shot=shot('60_detail_bh'), shot_caption='Màn chi tiết Phiếu bảo hành mở từ tab Phiếu bảo hành',
               note='Màn chi tiết mở trong cùng tab trình duyệt.'),
   extra=[(shot('61_detail_gvk'), 'Màn chi tiết Phiếu yêu cầu giao việc khác mở từ tab Giao việc khác')],
   ui_kw=dict(required=False),
   ui=[
       ('Liên kết Mã phiếu (Phiếu bảo hành)', 'Link', 'Enable', '<mã công ty>.PBH.<năm>.NNNNNN', 'Hiển thị', '- Bấm → màn chi tiết Phiếu bảo hành.'),
       ('Liên kết Số phiếu (Giao việc khác)', 'Link', 'Enable', '<mã công ty>.YCGVK.<năm>NNNNNN', 'Hiển thị',
        '- Bấm → màn chi tiết Phiếu yêu cầu giao việc khác.'),
       ('Mã phiếu tab HĐ / PL', 'Label', 'Read-only', '–', 'Hiển thị', '- Chữ thường, không bấm được (giữ như ERP).'),
       ('Màn chi tiết Phiếu bảo hành', 'Label', 'Read-only', '–', 'Ẩn', ['- Chỉ đọc', '- Tiêu đề kèm mã phiếu và trạng thái']),
       ('Màn chi tiết Phiếu yêu cầu giao việc khác', 'Label', 'Read-only', '–', 'Ẩn', ['- Chỉ đọc', '- Tiêu đề kèm số phiếu và trạng thái']),
       ('Các khối thông tin', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Theo màn nguồn (khách hàng, thiết bị / công việc, chi phí…).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về Phiếu chờ giao việc, giữ tab và bộ lọc (10 phút).'),
       ('Thông báo không tìm thấy', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- Do màn nguồn hiển thị khi không có quyền / không tồn tại.'),
       ('Nút Tạo phiếu giao việc trên màn chi tiết', 'Button', 'Enable / Ẩn', '–', 'Theo màn nguồn', '- Nếu màn nguồn có, đi cùng màn Tạo phiếu giao việc (mục 2.5).'),
       ('Bộ lọc tab khi quay về', 'Label', 'Read-only', '–', 'Khôi phục', '- Trong 10 phút: giữ tiêu chí, khách hàng đã chọn, khối lọc mở / đóng.'),
       ('Trang khi quay về', 'Pagination', 'Enable', '–', 'Trang 1', '- Danh sách nạp lại từ trang 1 với bộ lọc khôi phục.'),
   ],
   ev=[
       ('Bấm Mã phiếu / Số phiếu', 'Click',
        'Before:\n– Tab Phiếu bảo hành hoặc Giao việc khác.\nAfter:\n– Ghi nhớ bộ lọc tab; mở màn chi tiết trong cùng tab trình duyệt.'),
       ('Mở màn chi tiết', 'System',
        'Before:\n– Màn nguồn kiểm tra quyền xem.\nDuring:\n– Không có quyền / không tồn tại → màn nguồn báo lỗi.\nAfter:\n– Hiển thị chi tiết chỉ đọc.'),
       ('Bấm Quay lại / nút lùi trình duyệt', 'Click',
        'Before:\n– Trong 10 phút thì còn bộ lọc.\nAfter:\n– Về Phiếu chờ giao việc đúng tab, khôi phục bộ lọc, nạp trang 1.'),
       ('Bấm mã tab HĐ / PL', 'Click', 'Before:\n– Mã không phải liên kết.\nAfter:\n– Không có hành động.'),
   ])

# ------------------------------------------------------------ 2.11
fr(11, 'In phiếu yêu cầu lắp đặt bàn giao', usecase=('FR-11', 'In phiếu yêu cầu lắp đặt', 'io', A_XEM),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='In 1 phiếu yêu cầu lắp đặt bàn giao',
       mota='Ở tab Lắp đặt bàn giao, bấm In để xem trước bản in phiếu yêu cầu lắp đặt bàn giao ngay trên màn (mẫu “Chi tiết phiếu yêu cầu '
            'lắp đặt bàn giao” của hệ thống), letterhead theo công ty ghi trên phiếu yêu cầu, rồi in. Không đổi dữ liệu.',
       tacnhan='Người dùng có quyền thực hiện chức năng: mọi người xem được tab Lắp đặt bàn giao (không gắn quyền, giữ như ERP).',
       dieukien=DK + '\n4. Hệ thống có mẫu in “Chi tiết phiếu yêu cầu lắp đặt bàn giao”.',
       chinh='1. Người dùng bấm In ở cột Hành động của dòng tab Lắp đặt bàn giao.\n'
             '2. Hệ thống lấy mẫu in, điền dữ liệu phiếu yêu cầu (khách hàng, hợp đồng, hàng cần lắp đặt…) và letterhead theo công ty '
             'của phiếu.\n'
             '3. Hệ thống mở cửa sổ “Xem trước phiếu yêu cầu lắp đặt bàn giao”.\n'
             '4. Người dùng bấm In → hộp thoại in của trình duyệt; hoặc bấm (x) để đóng.',
       phu='• Thiếu mẫu in → thông báo “Không tìm thấy mẫu in \"Chi tiết phiếu yêu cầu lắp đặt bàn giao\"”.\n'
           '• Phiếu không tồn tại → thông báo không tìm thấy phiếu.\n'
           '• Bấm (x) / phím Esc → đóng cửa sổ, danh sách giữ nguyên.\n'
           '• Máy chủ lỗi → thông báo lỗi trả về.',
       dacbiet='Trước #11988 nút này mở ERP; nay xem trước ngay trên HRM. Logo / letterhead lấy theo công ty ghi trên phiếu yêu cầu, không '
               'theo người in.'),
   layout=dict(menu=M_LD + ' => In', shot=shot('50_print'), shot_caption='Cửa sổ Xem trước phiếu yêu cầu lắp đặt bàn giao',
               note='Cửa sổ xem trước được mở ngay trên màn hình danh sách tab Lắp đặt bàn giao.'),
   ui_kw=dict(required=False),
   ui=[
       ('Nút In (dòng)', 'Icon Button', 'Enable', '–', 'Hiển thị', ['- Biểu tượng máy in', '- Mọi dòng tab Lắp đặt']),
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Xem trước phiếu yêu cầu lắp đặt bàn giao”.'),
       ('Letterhead', 'Label', 'Read-only', '–', 'Theo công ty của phiếu', '- Ảnh đầu trang của công ty ghi trên phiếu yêu cầu.'),
       ('Nội dung bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Mẫu “Chi tiết phiếu yêu cầu lắp đặt bàn giao”.'),
       ('Thông tin khách hàng', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Tên, địa chỉ, liên hệ của khách trên phiếu.'),
       ('Bảng hàng cần lắp đặt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Các dòng hàng của phiếu yêu cầu.'),
       ('Khu vực ký', 'Label', 'Read-only', '–', 'Theo mẫu', '- Các chức danh ký theo mẫu in.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', ['- Nút xanh cạnh tiêu đề', '- Mở hộp thoại in của trình duyệt']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Góc phải; đóng cửa sổ (không có nút Đóng riêng).'),
       ('Phím Esc', 'Button', 'Enable', '–', '–', '- Đóng cửa sổ như (x).'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Không tìm thấy mẫu in \"Chi tiết phiếu yêu cầu lắp đặt bàn giao\"”', '- Không tìm thấy phiếu']),
   ],
   ev=[
       ('Bấm In ở dòng', 'Click',
        'Before:\n– Tab Lắp đặt bàn giao; không kiểm quyền.\nDuring:\n– Lấy mẫu in + dữ liệu phiếu; thiếu mẫu / phiếu → thông báo lỗi.\n'
        + ERR + '\nAfter:\n– Mở cửa sổ xem trước.'),
       ('Bấm In trong cửa sổ', 'Click', 'Before:\n– Bản in đã dựng xong.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x) / phím Esc', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, danh sách giữ nguyên.'),
       ('Mở cửa sổ', 'System', 'Before:\n– Letterhead theo công ty của phiếu.\nAfter:\n– Hiển thị bản in đúng khổ A4.'),
   ])

# ------------------------------------------------------------ 2.12
fr(12, 'Xuất Excel danh sách', usecase=('FR-12', 'Xuất Excel danh sách', 'io', A_XEM),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách tab đang mở ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất toàn bộ chứng từ của tab đang mở khớp bộ lọc trong phạm vi tab (không phân trang) ra file '
            'Excel. Mỗi tab 1 bộ trường và 1 tên file riêng; đầu file có ảnh tiêu đề giãn bằng bề rộng bảng và tiêu đề “Phiếu chờ giao '
            'việc - <tab>”.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất file” với các trường của tab, tích sẵn trường ứng với cột đang hiện.\n'
             '3. Người dùng tích trường, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy toàn bộ chứng từ của tab theo bộ lọc + sắp xếp hiện tại, dựng file (cột STT đứng đầu).\n'
             '5. Hệ thống tải file theo tab và báo “Xuất Excel thành công.”.',
       phu='• Không có chứng từ khớp → vẫn tải file chỉ có dòng tiêu đề cột, báo “Xuất Excel thành công.”.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Tên file: phieu_cho_giao_viec_hop_dong / _pl_bo_sung / _phieu_bao_hanh / _lap_dat_ban_giao / _giao_viec_khac .xlsx. Tổng '
               'thanh toán để trống với hợp đồng thuộc diện ẩn giá. Không giới hạn số dòng; khóa nút Xuất Excel trong lúc xuất.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file (tab Hợp đồng)',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất file”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách theo tab', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- HĐ / PL (9): Mã phiếu, Tổng thanh toán, Khách hàng, Người liên hệ - SĐT, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, '
         'Trạng thái', '- BH (6): Mã phiếu, Khách hàng, Người liên hệ - SĐT, Người tạo, Ngày tạo, Trạng thái',
         '- LĐ / GVK (6): Số phiếu, Số hợp đồng, Khách hàng, Người tạo, Ngày tạo, Trạng thái']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file Excel', '- Khóa khi chưa tích trường nào hoặc đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('Nội dung file Excel', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Ảnh tiêu đề rộng bằng bảng, tiêu đề “Phiếu chờ giao việc - <tab>”', '- Dòng tên cột: STT + các trường đã chọn',
         '- Ngày dạng dd/mm/yyyy hh:mm; Tổng thanh toán dạng số']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- “Xuất Excel thành công.”', '- “Lỗi khi xuất Excel”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không có lượt xuất đang chạy.\nAfter:\n– Mở cửa sổ, tích sẵn trường ứng với cột đang hiện của tab.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Kéo bằng biểu tượng của trường.\nAfter:\n– Đổi thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất; dữ liệu theo phạm vi tab.\n'
        'During:\n– Lấy toàn bộ chứng từ theo bộ lọc + sắp xếp; ẩn giá theo Q2.\n– Lỗi → “Lỗi khi xuất Excel”.\n' + ERR + '\n'
        'After:\n– Tải file theo tên của tab, báo “Xuất Excel thành công.”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu chờ giao việc; không lặp lại các quy tắc đã có trong SRS quy tắc '
           'chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi theo tab và quyền', [
        '– Tab Hợp đồng, PL bổ sung, Lắp đặt bàn giao: có “%s” mức Tổng công ty → mọi chứng từ; không có (kể cả mức Công ty) → '
        'phòng tiếp nhận ∈ các phòng người xem quản lý, không lọc theo công ty.' % QV,
        '– Tab Phiếu bảo hành, Giao việc khác: không bó phạm vi (giữ như ERP).', '– Không đặc cách Super admin; quyền tính ở công ty đang làm việc.'],
     ['Xem danh sách', 'Tìm kiếm', 'Xuất Excel']),
    ('BR-02', 'Trạng thái của từng tab', [
        '– Hợp đồng / PL bổ sung: Có hiệu lực.', '– Phiếu bảo hành: Đã duyệt và còn đánh dấu chờ giao việc.',
        '– Lắp đặt bàn giao / Giao việc khác: Chờ giao việc.', '– Ô lọc Trạng thái liệt kê đủ trạng thái nhưng chỉ trạng thái trên ra dữ liệu.'],
     ['Xem danh sách', 'Tìm kiếm']),
    ('BR-03', 'Còn số lượng chưa giao việc', [
        '– HĐ / PL: còn ít nhất 1 dòng (thiết bị sửa chữa — loại xử lý sửa chữa; dịch vụ; dịch vụ mở rộng) có Số lượng − SL phụ lục '
        'giảm − SL đã giao (chốt) − SL trên phiếu giao việc đang chạy > 0.',
        '– Phiếu giao việc đang chạy: phiếu gốc ở Đang giao / Đang nhập kết quả / Đã nhập kết quả / Đang duyệt kết quả, khớp cùng thiết '
        'bị + serial + lỗi (thiết bị), cùng tên chi phí (dịch vụ), cùng dịch vụ (dịch vụ mở rộng).',
        '– Lắp đặt: còn ít nhất 1 dòng cần lắp đặt có Số lượng − SL đã giao − SL trên phiếu giao việc đang chạy (không tính Đang duyệt '
        'kết quả, giữ như ERP) > 0, khớp cùng hàng + tên hàng + ĐVT.', '– Giao việc khác: chỉ xét trạng thái Chờ giao việc.'],
     ['Xem danh sách', 'Tạo phiếu giao việc']),
    ('BR-04', 'Sắp xếp, lọc thời gian', [
        '– Mặc định Ngày tạo mới nhất ở trên; sắp được Mã phiếu / Số phiếu, Ngày tạo, Ngày duyệt (HĐ / PL).',
        '– Lọc Ngày tạo theo ngày tạo chứng từ ở cả 5 tab, lấy trọn 2 ngày biên.'],
     ['Xem danh sách', 'Tìm kiếm']),
    ('BR-05', 'Điều kiện nút Tạo phiếu giao việc', [
        '– HĐ / PL: Có hiệu lực + quyền “%s” + phòng tiếp nhận = phòng của người đăng nhập.' % Q1,
        '– Lắp đặt / Giao việc khác: phòng tiếp nhận = phòng của người đăng nhập (không xét quyền).', '– Phiếu bảo hành: luôn hiện.',
        '– HĐ: khi bấm chặn nếu có PL giảm Chờ duyệt.'],
     ['Tạo phiếu giao việc']),
    ('BR-06', 'Điều kiện Từ chối tiếp nhận', [
        '– HĐ: như BR-05 và hợp đồng chưa có phiếu giao việc (trừ đã hủy).', '– PL: như BR-05.', '– Lý do bắt buộc.'],
     ['Từ chối tiếp nhận xử lý']),
    ('BR-07', 'Điều kiện Đóng hợp đồng', [
        '– Có hiệu lực; người lập hoặc người quản lý phòng của hợp đồng (trong công ty đang làm việc).',
        '– Hợp đồng và phụ lục chưa có phiếu giao việc (trừ đã hủy), yêu cầu xuất kho, yêu cầu nhập kho, yêu cầu hạch toán dịch vụ.',
        '– Đóng kéo theo phụ lục bổ sung / giảm.'],
     ['Đóng hợp đồng']),
    ('BR-08', 'Điều kiện Hủy duyệt / Quyết toán', [
        '– Hủy duyệt: người quản lý phòng của hợp đồng; như BR-07 và không còn phụ lục bổ sung / giảm đang sống; lý do bắt buộc.',
        '– Quyết toán: người đăng nhập là người lập hợp đồng; mở ERP.'],
     ['Hủy duyệt hợp đồng', 'Mở chức năng ERP']),
    ('BR-09', 'Ẩn giá', ['– Người có “%s” mà hợp đồng ngoài phạm vi giá của mình → Tổng thanh toán trống (cả file Excel).' % QG],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-10', 'Tác động khi tạo phiếu giao việc', [
        '– SL trên phiếu mới được trừ ngay (đang chạy); hết SL → chứng từ rời tab.',
        '– Giao việc khác → Đã giao việc; Lắp đặt hết SL → Đang giao việc; Phiếu bảo hành hết SL → bỏ đánh dấu chờ giao.',
        '– Hủy phiếu giao việc → SL trả lại, chứng từ có thể quay lại tab.'],
     ['Tạo phiếu giao việc', 'Ràng buộc']),
    ('BR-11', 'Quy tắc ghi lịch sử và thông báo', [
        '– Màn không có lịch sử riêng; xem, lọc, xuất, in không ghi gì.',
        '– Từ chối tiếp nhận HĐ: lịch sử “Thay đổi thông tin” của hợp đồng + thông báo người lập.',
        '– Đóng: lịch sử “Thay đổi trạng thái”, không thông báo. Hủy duyệt: lịch sử “Thay đổi trạng thái” kèm lý do + thông báo người lập.',
        '– Từ chối tiếp nhận PL: chỉ thông báo người lập phụ lục (không ghi lịch sử).'],
     ['Từ chối tiếp nhận', 'Đóng', 'Hủy duyệt']),
    ('BR-12', 'Duy nhất, chuẩn hóa nhập', [
        '– Màn không tạo bản ghi nên không có quy tắc trùng; mã chứng từ do màn nguồn sinh.',
        '– Ô lý do bỏ khoảng trắng đầu / cuối khi kiểm bắt buộc; ô tìm / lọc chữ bỏ khoảng trắng đầu / cuối.'],
     ['Từ chối tiếp nhận', 'Hủy duyệt', 'Tìm kiếm']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Phiếu chờ giao việc (chứng từ nguồn của 5 tab, số lượng đã giao, phòng tiếp '
    'nhận, trạng thái hợp đồng).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'CSKH sau bán', 'Hợp đồng dịch vụ (nguồn tab Hợp đồng; ghi phòng tiếp nhận, trạng thái; nhận lịch sử Từ chối tiếp nhận / Đóng / '
                          'Hủy duyệt)', 'CSKH sau bán -> Kiểm tra bảo hành sửa chữa'),
    ('2', 'Hệ thống ERP', 'Phụ lục bổ sung / phụ lục giảm hợp đồng dịch vụ (nguồn tab PL bổ sung; PL giảm Chờ duyệt chặn Tạo phiếu giao '
                          'việc; chọn lại phòng tiếp nhận sau khi từ chối)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('3', 'CSKH sau bán', 'Phiếu bảo hành (nguồn tab Phiếu bảo hành; Mã phiếu mở chi tiết; đánh dấu chờ giao được tính lại khi giao)',
     'CSKH sau bán -> Kiểm tra bảo hành sửa chữa'),
    ('4', 'Hệ thống ERP', 'Phiếu yêu cầu lắp đặt bàn giao (nguồn tab Lắp đặt; Số phiếu, Xuất Excel 1 phiếu mở ERP; trạng thái đổi khi giao)',
     'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('5', 'CSKH sau bán', 'Phiếu yêu cầu giao việc khác (nguồn tab Giao việc khác; Số phiếu mở chi tiết; chuyển Đã giao việc khi lập phiếu '
                          'giao việc)', 'CSKH sau bán -> Giao việc'),
    ('6', 'CSKH sau bán', 'Phiếu giao việc (đích của nút Tạo phiếu giao việc; SL trên phiếu đang chạy trừ vào SL chưa giao; Quay lại về '
                          'màn này đúng tab)', 'CSKH sau bán -> Giao việc'),
    ('7', 'CSKH sau bán', 'Phiếu nhập kết quả (đổi trạng thái phiếu giao việc → quyết định SL còn tính là đang giao)',
     'CSKH sau bán -> Giao việc'),
    ('8', 'Hệ thống ERP', 'Hợp đồng bán / Quyết toán hợp đồng (Số hợp đồng tab Lắp đặt, Giao việc khác; nút Quyết toán hợp đồng)',
     'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('9', 'Tài chính', 'Phiếu yêu cầu xuất kho, yêu cầu nhập kho, yêu cầu hạch toán dịch vụ theo hợp đồng dịch vụ (có chứng từ thì không '
                       'Đóng / Hủy duyệt được)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
