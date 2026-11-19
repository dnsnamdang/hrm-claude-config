# -*- coding: utf-8 -*-
"""SRS màn "Biên bản bàn giao nghiệm thu" (phân hệ Công việc / CSKH sau bán / Thông báo) — form chuẩn SRS_MAU (10/11/2026).

Chạy: python gen_srs.py  -> "SRS - Biên bản bàn giao nghiệm thu.docx" (SrsDoc.save() tự chạy srs_selfcheck).
Khuôn: ../phieu-nhap-hang-dieu-chinh-kiem-ke/gen_srs.py (09/11) + ../borrow-export/. Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột.
Nguồn đọc 10/11/2026 (nhánh develop cả 2 repo, con của gop_db):
  BE  Modules/CustomerCare/{Entities/HandoverAcceptanceRecord/* (STATUSES, SOURCES), Http/Controllers/V1/HandoverAcceptanceRecordController.php,
      Http/Requests/HandoverAcceptanceRecordRequest.php, Services/HandoverAcceptanceRecord{,Store,Print}Service.php,
      Services/HandoverContractSourceService.php (popup HĐ 2 nguồn, contract-data, SL theo HĐ, pendingProductIds, handover_date),
      Routes/api.php (checkPermission "Tạo biên bản bàn giao nghiệm thu")}, app/Support/Permissions/Catalog/customer_care.php
      (customer_care.bien_ban_ban_giao_nghiem_thu.create / .view mức 2-3-4), app/ExcelExport/ExportColumnRegistry.php,
      app/Services/CatalogHistoryService.php. Màn đọc ngược: Assign/Services/CustomerManagerService.php (thiết bị KH — Số BBBGNT),
      CustomerCare/Services/CustomerDeviceListService.php (Phiếu nhập kết quả), Finance/Services/CustomerDebt/CustomerDebtByEmployeeReportService.php
      (Ngày nghiệm thu), Assign/Services/ProductExportService.php (Phiếu xuất hàng ghi SL đã xuất HĐ hãng), MasterData ProductUsageGuard.
  FE  pages/assign/handover-acceptance-records/** (index, create, _id/index, _id/edit, components/HandoverAcceptanceRecordForm.vue,
      HandoverProductTable.vue, HandoverContractPickerModal.vue, handoverActions.js, handoverBuild.js), components/menu-sidebar.js,
      components/subsystem-menu/{customer-care.js, lookup.js}.
  Bối cảnh: design.md, plan.md (#12011, #12018, #12021, #12023, #12060, #12083, #12084), spec docs/superpowers/specs/gop-db/
  2026-11-03-bien-ban-ban-giao-nghiem-thu-design.md.
Ảnh: ./bbbgnt_shots — dev-hrm 10/11/2026 (_capture/capture.js, DNS Admin = Super admin có quyền Tạo, chặn mọi yêu cầu ghi: 0 yêu cầu ghi).
  Dữ liệu dev thật: TPE.BBBG.02738 / 02737 Đang tạo, TPE.BBBG.02736 Đã duyệt. Ảnh 12b_confirm_approve GIẢ trạng thái trên trình duyệt
  (SL nghiệm thu = SL đã xuất trong dữ liệu form) để tới được hộp Xác nhận lưu và duyệt.
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

TEN = 'Biên bản bàn giao nghiệm thu'
SHOTS = os.path.join(HERE, 'bbbgnt_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Công việc => Kết quả công việc => Biên bản bàn giao nghiệm thu'
MENU_CC = 'Phân hệ CSKH sau bán => Hồ sơ công việc => Biên bản bàn giao nghiệm thu'
MENU_NV = 'Phân hệ Thông báo => Thông báo => BB bàn giao nghiệm thu theo NV'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Biên bản bàn giao nghiệm thu.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
Q1 = 'Tạo biên bản bàn giao nghiệm thu'
QV = 'Xem biên bản bàn giao nghiệm thu'
A_XEM = 'Người xem biên bản'
A_LAP = 'Người lập biên bản'
TN = ('Người dùng có quyền thực hiện chức năng: %s (mức Tổng công ty / Công ty / Phòng ban); không có quyền thì chỉ biên bản '
      'mình tạo, lối “theo NV” thì biên bản mình là NVKD.' % QV)
TN_LAP = ('Người dùng có quyền thực hiện chức năng: %s; Sửa / Xóa / Lưu và duyệt biên bản Đang tạo chỉ dành cho chính người tạo '
          'biên bản (vẫn phải có quyền này).' % Q1)
DK = ('1. Người dùng đăng nhập thành công.\n2. Biên bản nằm trong phạm vi xem của người dùng.\n'
      '3. Người dùng đang ở màn danh sách Biên bản bàn giao nghiệm thu.')
REQ = '“Bắt buộc phải nhập”'
REQ_SEL = '“Bắt buộc phải chọn”'
MSG_HD = '“Bắt buộc phải chọn 1 hợp đồng”'
MSG_FILE = '“Vui lòng chọn file đính kèm”'
MSG_PHONE = '“Số điện thoại không đúng định dạng”'
MSG_DATE = '“Ngày bàn giao không được lớn hơn ngày hiện tại”'
INCOMPLETE = '“Bạn chưa nhập đầy đủ thông tin.”'
CHECK = '“Vui lòng kiểm tra lại thông tin đã nhập”'
DUP = '“Không thể tạo biên bản bàn giao nghiệm thu cho hợp đồng này”'
NOT_EXP = '“Hợp đồng chưa xuất hết hàng”'
NOT_EXP_ROW = '“Chưa xuất hết hàng”'
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
QTY_OVER = '“Không được lớn hơn số lượng đã xuất (X)”'
QTY_OVER2 = '“Không được lớn hơn tổng số lượng đã xuất và đã trả (X)”'
QTY_SER = '“Phải bằng số dòng seri (n)”'
QTY_EXP = '“Phải bằng số lượng đã xuất (X)”'
OK_CREATE = '“Tạo biên bản bàn giao nghiệm thu thành công.”'
OK_EDIT = '“Chỉnh sửa biên bản bàn giao nghiệm thu thành công.”'
CF_TITLE = '“Xác nhận lưu và duyệt”'
CF_MSG = ('“Lưu và duyệt biên bản bàn giao nghiệm thu của hợp đồng \'<số hợp đồng>\'? Biên bản đã duyệt không sửa / xóa được '
          'nữa.”')
CH_TITLE = '“Xác nhận thay đổi hợp đồng”'
CH_MSG = '“Nếu bạn thay đổi hợp đồng các thông tin hiện có sẽ bị thay thế! Bạn có chắc chắn muốn thay đổi?”'
EXISTS = '“BBBG cho hợp đồng: <số hợp đồng> đã tồn tại.”'

d = SrsDoc(out=OUT, menu=MENU, route='/assign/handover-acceptance-records', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Công việc': 'menu_phanhe_cv', 'Kết quả công việc': 'menu_nhom_cv', 'Biên bản bàn giao nghiệm thu': 'menu_muc_cv',
    'Phân hệ CSKH sau bán': 'menu_phanhe_cc', 'Hồ sơ công việc': 'menu_nhom_cc',
    'Phân hệ Thông báo': 'menu_phanhe_tb', 'Thông báo': 'menu_nhom_tb', 'BB bàn giao nghiệm thu theo NV': 'menu_muc_tb',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Sửa': 'btn_sua_row', 'Xóa': 'btn_xoa_row', 'Lưu và duyệt': 'btn_luuduyet',
    'Hợp đồng/đơn hàng': 'o_hopdong', 'Xem chi tiết': 'link_sophieu', 'In': 'btn_in_row', 'In danh sách': 'btn_inds',
    'Xuất Excel': 'btn_xuatexcel', 'Lịch sử': 'btn_lichsu_row',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Biên bản bàn giao nghiệm thu (mã <mã công ty>.BBBG.NNNNN, vd TPE.BBBG.02738), '
    'dùng chung cho phân hệ Công việc, CSKH sau bán và Thông báo, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ bước ghi nhận việc BÀN GIAO HÀNG CHO KHÁCH: hợp đồng / đơn hàng đã xuất hết hàng → người lập chọn hợp đồng (hợp đồng '
    'hãng hoặc hợp đồng HRM), hệ thống điền khách hàng, NVKD, phòng ban và danh sách hàng (SL theo hợp đồng, SL đã xuất, SL đã '
    'trả) → người lập nhập SL đã nghiệm thu, seri, ngày bàn giao, thời gian bảo hành, người nhận, NV kỹ thuật, file biên bản → Lưu '
    'nháp (Đang tạo) hoặc Lưu và duyệt (Đã duyệt).',
    'Làm rõ dữ liệu biên bản được các màn khác đọc lại: Ngày nghiệm thu của báo cáo công nợ theo nhân viên, Số BBBGNT trên danh '
    'sách thiết bị của khách hàng (yêu cầu sửa chữa – bảo hành, phiếu nhập kết quả), ngày bàn giao ghi lên hợp đồng hãng.',
])
d.p('Phạm vi chức năng: Xem danh sách (3 lối vào), Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới (Lưu nháp / Lưu và tiếp '
    'tục), Chọn hợp đồng/đơn hàng, Chỉnh sửa biên bản Đang tạo, Lưu và duyệt, Xóa biên bản Đang tạo, Xem chi tiết, In biên bản, In '
    'danh sách, Xuất Excel danh sách, Xem lịch sử thay đổi. Màn KHÔNG có Khóa / Mở khóa, Gửi duyệt, Duyệt / Không duyệt riêng, Hủy '
    'phiếu và Import Excel: bước duyệt chính là nút Lưu và duyệt của người lập (giữ như hệ thống cũ).')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Ngày bàn giao (Ngày BGNT) của biên bản mới nhất là Ngày nghiệm thu của hợp đồng hãng cần lắp đặt trong Báo cáo tổng hợp công nợ '
    'theo nhân viên (tính Số ngày nợ); lần Tạo ghi Ngày bàn giao lên hợp đồng hãng.',
    'Số biên bản (Số BBBGNT) hiện cạnh thiết bị đã giao trên danh sách thiết bị của khách hàng — dùng khi lập yêu cầu sửa chữa – '
    'bảo hành, phiếu cung cấp thông tin làm báo giá, phiếu nhập kết quả.',
    'Seri, ngày bàn giao, số ngày bảo hành, hết hạn bảo hành của từng hàng là căn cứ bảo hành cho khách.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Mỗi hợp đồng chỉ có tối đa 1 biên bản; popup chỉ liệt kê hợp đồng có hiệu lực / đã thanh lý của công ty người lập, đã xuất '
    'hết hàng, chưa có biên bản (BR-02, BR-03).',
    'Lưu nháp / Lưu và tiếp tục chỉ bắt buộc hợp đồng; Lưu và duyệt bắt buộc đủ SĐT người nhận, NV kỹ thuật, Ngày bàn giao, file '
    'đính kèm và SL đã nghiệm thu = SL đã xuất (BR-04, BR-05).',
    'Sửa / Xóa chỉ biên bản Đang tạo của chính mình và phải có quyền “%s” (BR-07).' % Q1,
    'Giữ như hệ thống cũ (đã chốt 03/11/2026): Lưu và duyệt không cần quyền duyệt riêng; trạng thái “Chờ duyệt” có trong bộ lọc '
    'nhưng không có thao tác nào tạo ra (BR-12).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Biên bản bàn giao nghiệm thu (BBBG, BBBGNT)', 'Chứng từ <mã công ty người lập>.BBBG.NNNNN của màn này: ghi nhận hàng của 1 '
                                                     'hợp đồng / đơn hàng đã bàn giao, nghiệm thu với khách hàng.'),
    ('Hợp đồng hãng', 'Hợp đồng bán hàng hóa - vật tư, Hợp đồng dự án, Đơn hàng nguyên tắc lập ở hệ thống cũ (ERP) — nguồn chính của '
                      'biên bản (dữ liệu cũ 100% thuộc loại này).'),
    ('Hợp đồng HRM', 'Hợp đồng lập ở màn Hợp đồng (dự án TKT) của HRM; nguồn thứ 2 (thêm từ 03/11/2026).'),
    ('NVKD', 'Nhân viên kinh doanh của hợp đồng — lấy theo hợp đồng; lối vào “BB bàn giao nghiệm thu theo NV” lọc theo trường này.'),
    ('NV kỹ thuật', 'Nhân viên kỹ thuật thực hiện bàn giao — chọn trên biên bản.'),
    ('SL theo hợp đồng / SL đã xuất / SL đã trả', 'Số lượng hàng trên hợp đồng (gồm phụ lục bổ sung, trừ phụ lục giảm), số đã xuất '
                                                 'kho cho khách, số khách đã trả lại — hệ thống lấy theo hợp đồng, không nhập.'),
    ('SL đã nghiệm thu', 'Số lượng hàng ghi nhận bàn giao trên biên bản — ô nhập.'),
    ('Thông tin chi tiết (dòng seri)', 'Mỗi hàng 1..n dòng: Seri, Ngày bàn giao, Thời gian bảo hành (ngày), Hết hạn, Ghi chú. Hàng '
                                       'thuộc nhóm bắt buộc seri phải có số dòng = SL đã nghiệm thu.'),
    ('Trạng thái Đang tạo', 'Nhãn xám: biên bản đã Lưu nháp, người tạo còn sửa / xóa được; chỉ người tạo nhìn thấy ở lối “tất cả”.'),
    ('Trạng thái Chờ duyệt', 'Nhãn vàng: có trong danh mục trạng thái (dữ liệu cũ), màn không có thao tác nào tạo ra.'),
    ('Trạng thái Đã duyệt', 'Nhãn xanh lá: đã Lưu và duyệt, không sửa / xóa được.'),
    ('Cấu trúc phân cấp', 'Hợp đồng > biên bản (tối đa 1) > dòng hàng (hàng, ĐVT, SL) > dòng thông tin chi tiết (seri). File đính kèm '
                          'gắn trên biên bản.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn có 2 mã quyền thuộc nhóm “Biên bản bàn giao nghiệm thu” (phân hệ CSKH sau bán, tên giữ như hệ thống cũ): '
    'customer_care.bien_ban_ban_giao_nghiem_thu.create và customer_care.bien_ban_ban_giao_nghiem_thu.view (3 mức phạm vi). Super '
    'admin có đủ mọi mức XEM; quyền Tạo phải được tích thật (Super admin chưa tích thì không có nút Tạo mới / Sửa / Xóa). Không gắn '
    'quyền ở menu: ai cũng mở được màn, dữ liệu do hệ thống giới hạn.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1, 'Hiện nút Tạo mới; được Lưu nháp / Lưu và tiếp tục / Lưu và duyệt, tải file đính kèm; cùng điều kiện người tạo + Đang '
               'tạo thì có Sửa và Xóa.'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (một mã Xem, 3 mức):')
d.table(['Ký hiệu', 'Quyền – mức phạm vi', 'Phạm vi dữ liệu'], [
    ('V1', QV + ' – Tổng công ty', 'Lối “tất cả”: mọi biên bản mọi công ty; có ô lọc Công ty và Phòng ban.'),
    ('V2', QV + ' – Công ty', 'Lối “tất cả”: biên bản có công ty = công ty của người xem; có ô lọc Phòng ban.'),
    ('V3', QV + ' – Phòng ban', 'Lối “tất cả”: biên bản thuộc các phòng ban người xem quản lý (trong công ty mình); không có ô Công ty '
                                '– Phòng ban.'),
    ('—', 'Không có V1 / V2 / V3', 'Lối “tất cả”: chỉ biên bản do chính mình tạo.'),
], widths=[0.8, 2.2, 3.0])
d.p('Áp chung: ở lối “tất cả”, biên bản Đang tạo của người khác luôn bị ẩn. Lối “BB bàn giao nghiệm thu theo NV” KHÔNG theo quyền: '
    'chỉ biên bản mà người đăng nhập là NVKD (kể cả biên bản Đang tạo của người khác). Lối không kèm tham số (không có trên menu) '
    'chỉ biên bản mình tạo. Công ty / phòng ban của biên bản lấy theo NGƯỜI LẬP.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ theo V', '✅ mọi BB', '✅ công ty', '✅ phòng quản lý', '✅ BB mình tạo / mình là NVKD'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅ (Công ty, Phòng ban)', '✅ (Phòng ban)', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo mới biên bản', '✅', '❌', '❌', '❌', '❌ (không có nút; lưu bị từ chối)'),
    ('FR-06 Chọn hợp đồng/đơn hàng', '✅', '❌', '❌', '❌', '❌'),
    ('FR-07 Chỉnh sửa biên bản', 'Người tạo, Đang tạo', '❌', '❌', '❌', '❌'),
    ('FR-08 Lưu và duyệt', '✅ (khi tạo / sửa của mình)', '❌', '❌', '❌', '❌'),
    ('FR-09 Xóa biên bản', 'Người tạo, Đang tạo', '❌', '❌', '❌', '❌'),
    ('FR-10 Xem chi tiết', '✅ BB mình tạo', '✅ mọi BB', '✅ công ty', '✅ phòng quản lý', '✅ BB mình tạo / mình là NVKD'),
    ('FR-11 In biên bản', '✅ như FR-10', '✅', '✅', '✅', '✅ như FR-10'),
    ('FR-12 In danh sách', '✅ theo phạm vi', '✅', '✅', '✅', '✅ theo phạm vi'),
    ('FR-13 Xuất Excel', '✅ theo phạm vi', '✅', '✅', '✅', '✅ theo phạm vi'),
    ('FR-14 Xem lịch sử thay đổi', '✅ như FR-10', '✅', '✅', '✅', '✅ như FR-10'),
    ('Khóa – Mở khóa / Gửi duyệt / Không duyệt / Hủy / Import', '—', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.7, 0.9, 0.8, 0.8, 0.8, 1.0])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có V1 / V2 / V3: vẫn mở được màn; lối “tất cả” chỉ có biên bản mình tạo; không có khối Công ty – Phòng ban.',
    'Không có Q1: không có nút Tạo mới, không có nút Sửa / Xóa (kể cả biên bản mình tạo trước đó); mở thẳng màn Tạo rồi bấm Lưu / '
    'tải file → hệ thống từ chối, báo không có quyền.',
    'Mở chi tiết biên bản ngoài phạm vi qua đường link: hệ thống chuyển sang trang “không tìm thấy” (404), không hiện dữ liệu.',
    'Mở màn Sửa của biên bản không phải mình tạo / đã duyệt / thiếu Q1: chuyển sang trang “không tìm thấy” (404).',
    'Bị gỡ quyền giữa lúc thao tác: lần nạp dữ liệu / lưu tiếp theo hệ thống áp quyền mới (quyền kiểm lại ở từng lần gọi).',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới', 'Có quyền Q1 (tích thật)', 'Ẩn khi không có quyền'),
    ('Nút Sửa, Xóa (dòng, màn chi tiết)', 'Q1 + người đăng nhập là người tạo + biên bản Đang tạo', 'Super admin không được Sửa / Xóa thay'),
    ('Nút In, Lịch sử trên dòng', 'Luôn hiện', 'Dòng có Sửa + Xóa: In, Lịch sử nằm trong nút ba chấm “Hành động khác”'),
    ('Nút In danh sách, Xuất Excel, Cấu hình cột, Cài đặt bộ lọc', 'Luôn hiện', 'Dữ liệu giới hạn theo phạm vi'),
    ('Khối lọc Công ty – Phòng ban', 'Chỉ lối “tất cả” và có V1 hoặc V2', 'Ô Công ty chỉ có hiệu lực với V1'),
], widths=[2.4, 2.0, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_XEM, [0, 5, 6, 7]), (A_LAP, [1, 2, 3, 4])],
    [('FR-01', 'Xem danh sách biên bản', 'view'),
     ('FR-05', 'Tạo mới biên bản', 'crud'),
     ('FR-07', 'Chỉnh sửa biên bản', 'crud'),
     ('FR-08', 'Lưu và duyệt', 'action'),
     ('FR-09', 'Xóa biên bản', 'action'),
     ('FR-11', 'In biên bản', 'io'),
     ('FR-12', 'In danh sách', 'io'),
     ('FR-13', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-10', 'Xem chi tiết biên bản', 'view', 'extend', [0], None),
     ('FR-14', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn hợp đồng/đơn hàng', 'view', 'extend', [1, 2], None)],
    'Sơ đồ Use Case tổng quan màn Biên bản bàn giao nghiệm thu')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách biên bản',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách biên bản bàn giao nghiệm thu',
       mota='Hiển thị bảng các biên bản theo lối vào: lối “tất cả” (phân hệ Công việc và CSKH sau bán) theo phạm vi quyền Xem; lối '
            '“BB bàn giao nghiệm thu theo NV” (phân hệ Thông báo) chỉ biên bản mình là NVKD. Mỗi lối vào giữ bộ lọc, cấu hình cột và '
            'cài đặt bộ lọc riêng. Mỗi dòng có liên kết sang chi tiết biên bản, sang hợp đồng, và các nút Sửa, Xóa, In, Lịch sử.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng để mở màn; dữ liệu giới hạn theo phạm vi và lối vào.',
       chinh='1. Người dùng vào màn theo một trong các đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định lối vào và phạm vi: lối “tất cả” — V1 mọi biên bản, V2 công ty mình, V3 phòng ban mình quản lý, '
             'không quyền chỉ biên bản mình tạo, luôn ẩn biên bản Đang tạo của người khác; lối “theo NV” — biên bản có NVKD là mình.\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất của lối vào đó và cấu hình cột đã lưu của người dùng.\n'
             '4. Hệ thống lấy các biên bản khớp bộ lọc, sắp biên bản tạo gần nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, dòng “Hiển thị a–b / N” và phân trang.\n'
             '6. Với từng dòng, hệ thống tính nút Sửa / Xóa (Q1 + người tạo + Đang tạo); nút Tạo mới chỉ hiện với quyền Q1.',
       phu='• Không có biên bản nào trong phạm vi / khớp bộ lọc → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Máy chủ lỗi khi nạp → thông báo “Lỗi khi tải dữ liệu”, bảng trống.\n'
           '• Đang đứng ở màn mà bấm sang lối vào khác (cùng màn, khác tham số) → hệ thống xóa bộ lọc cũ, đổi bộ khóa lưu, nạp lại.\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, xóa phiên và chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 13 cột. Cột khóa trong Tùy chỉnh cột: STT, Số BBBG, Hành động. Sắp xếp được: Số BBBG, Ngày '
               'BGNT, Số hợp đồng, Ngày tạo, Ngày cập nhật; mặc định Ngày tạo mới nhất ở trên. Đổi bộ lọc, sắp xếp, số dòng đều về trang '
               '1; mỗi trang tối đa 100 dòng.'),
   layout=dict(entries=[
       (MENU, 'Lối “tất cả” — tiêu đề “Biên bản bàn giao nghiệm thu”, phạm vi theo quyền Xem.'),
       (MENU_CC, 'Lối “tất cả” (cùng màn, cùng phạm vi với dòng trên) — nhóm Hồ sơ công việc của CSKH sau bán.'),
       (MENU_NV, 'Lối “theo NV” — tiêu đề “Biên bản bàn giao nghiệm thu theo nhân viên”, chỉ biên bản mình là NVKD, không có khối '
                 'Công ty – Phòng ban.')],
       shot=shot('01_list'), shot_caption='Màn danh sách Biên bản bàn giao nghiệm thu (lối “tất cả”)'),
   extra=[(shot('00_menu_cv'), 'Mục Biên bản bàn giao nghiệm thu trong nhóm Kết quả công việc (phân hệ Công việc)'),
          (shot('00b_menu_cc'), 'Mục Biên bản bàn giao nghiệm thu trong nhóm Hồ sơ công việc (phân hệ CSKH sau bán)'),
          (shot('00c_menu_tb'), 'Mục BB bàn giao nghiệm thu theo NV trong nhóm Thông báo (phân hệ Thông báo)'),
          (shot('01b_list_nv'), 'Lối vào BB bàn giao nghiệm thu theo NV'),
          (shot('01c_row_more'), 'Dòng Đang tạo: Sửa, Xóa và nút ba chấm chứa In, Lịch sử')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- Lối “tất cả”: “Biên bản bàn giao nghiệm thu”', '- Lối “theo NV”: “Biên bản bàn giao nghiệm thu theo nhân viên”',
         '- Không kèm tham số: “Biên bản bàn giao nghiệm thu của tôi”']),
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
        ['- Chỉ hiện với quyền “%s”' % Q1, '- Bấm → mở màn Tạo biên bản bàn giao nghiệm thu (mục 2.5)']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.12).'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Bấm → mở cửa sổ Chọn trường xuất file (mục 2.13)', '- Khóa trong lúc đang xuất; bên cạnh hiện tiến độ']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa, cố định khi cuộn ngang']),
       ('Cột Số BBBG', 'Table/Grid', 'Read-only', '<mã công ty>.BBBG.NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết (mục 2.10)', '- Sắp xếp được', '- Cột khóa']),
       ('Cột Ngày BGNT', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Ngày bàn giao của biên bản', '- Trống với biên bản nháp chưa nhập ngày', '- Sắp xếp được']),
       ('Cột Số hợp đồng', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Là liên kết, mở TAB MỚI: hợp đồng hãng → màn hợp đồng ở hệ thống cũ; hợp đồng HRM → màn Hợp đồng HRM',
         '- Sắp xếp được']),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Dạng “Mã KH - Tên khách hàng”', '- Tối đa 2 dòng']),
       ('Cột NVKD', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Dạng “Họ tên - Mã phòng ban”.'),
       ('Cột NV kỹ thuật', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Dạng “Họ tên - Mã phòng ban”; trống khi chưa chọn.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Sắp xếp được; mặc định mới nhất ở trên.'),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Dạng “Họ tên - Mã phòng ban”.'),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Sắp xếp được.'),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Dạng “Họ tên - Mã phòng ban”.'),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 3 giá trị', 'Hiển thị',
        ['- Đang tạo: nhãn xám', '- Chờ duyệt: nhãn vàng', '- Đã duyệt: nhãn xanh lá', '- Không sắp xếp']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Nút Sửa (bút chì): Đang tạo + mình tạo + có Q1 → màn Sửa (mục 2.7)',
           '- Nút Xóa (thùng rác đỏ): cùng điều kiện → hộp Xác nhận xóa (mục 2.9)',
           '- Nút In → cửa sổ Xem trước biên bản (mục 2.11)', '- Nút Lịch sử → cửa sổ Lịch sử thay đổi (mục 2.14)',
           '- Dòng có Sửa + Xóa: In, Lịch sử nằm trong nút ba chấm “Hành động khác”', '- Cột khóa']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Không có dữ liệu phù hợp.” khi N = 0.'),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang', '- N: tổng số biên bản khớp bộ lọc trong phạm vi']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Trang đầu: về đầu / lùi mờ; trang cuối: tiến / về cuối mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Lỗi khi tải dữ liệu” khi máy chủ lỗi.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định lối vào theo menu; xác định phạm vi theo quyền Xem (lối “tất cả”) hoặc NVKD (lối “theo NV”).\n'
        '– Khôi phục bộ lọc (10 phút) và cấu hình cột đã lưu của lối vào.\n'
        'During:\n– Lấy biên bản trong phạm vi khớp bộ lọc; tính cờ Sửa / Xóa từng dòng; cờ Tạo mới theo Q1.\n'
        '– Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, biên bản tạo mới nhất ở trên, kèm dòng “Hiển thị a–b / N”.'),
       ('Bấm Số BBBG', 'Click',
        'Before:\n– Biên bản nằm trong phạm vi xem.\n'
        'After:\n– Mở màn chi tiết (mục 2.10); bộ lọc hiện tại được ghi nhớ 10 phút để khôi phục khi quay lại.'),
       ('Bấm Số hợp đồng', 'Click',
        'Before:\n– Dòng có hợp đồng nhận diện được nguồn.\n'
        'After:\n– Mở hợp đồng ở tab mới; danh sách giữ nguyên trang và bộ lọc.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Số BBBG, Ngày BGNT, Số hợp đồng, Ngày tạo, Ngày cập nhật hỗ trợ sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc; độ rộng cột cố định nên bảng không nhảy bố cục.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp; bấm lại trang đang xem thì bỏ qua.\n'
        'After:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại theo số dòng mới.'),
       ('Bấm nút ba chấm “Hành động khác”', 'Click',
        'Before:\n– Dòng có đủ Sửa + Xóa.\nAfter:\n– Mở menu In, Lịch sử ngay dưới nút.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc biên bản',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách biên bản bàn giao nghiệm thu',
       mota='Thu hẹp danh sách theo số BBBG, Ngày BGNT, số hợp đồng, khách hàng, NV kỹ thuật, người tạo, trạng thái, ngày tạo và Công '
            'ty – Phòng ban. Ô tìm nhanh tìm theo số BBBG; các ô lọc nằm trong khối Tìm kiếm nâng cao, bật / tắt được bằng Cài đặt '
            'bộ lọc (mục 2.3). Mọi điều kiện chỉ lọc trong phạm vi của lối vào và quyền.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập số BBBG vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Ô chọn (ngày, khách hàng, NV kỹ thuật, người tạo, trạng thái, công ty, phòng ban) lọc ngay khi đổi; ô gõ chữ (Số hợp '
             'đồng) lọc khi bấm Tìm kiếm / nhấn Enter; về trang 1.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.\n'
             '5. Hệ thống ghi nhớ bộ lọc 10 phút cho lối vào đang dùng.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1 (giữ nguyên lối vào / phạm vi).\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Ô Khách hàng: phải gõ ít nhất 2 ký tự mới hiện gợi ý (tìm trong toàn bộ danh mục khách hàng).\n'
           '• Bấm dấu × trong ô chọn → xóa giá trị của ô đó.\n'
           '• Lối “theo NV” hoặc không có V1 / V2 → không có ô Công ty – Phòng ban.',
       dacbiet='Kiểu khớp chữ (Số BBBG, Số hợp đồng): một phần, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối; không giới '
               'hạn số ký tự; ký tự % và _ được hiểu là ký tự đại diện. Số hợp đồng lọc theo số hợp đồng ghi trên biên bản. Ngày BGNT '
               'lọc đúng 1 ngày (không tính giờ). Ngày tạo lấy trọn hai ngày biên. Mọi điều kiện kết hợp kiểu VÀ. Ô Công ty chỉ có '
               'hiệu lực với V1. Ghi nhớ bộ lọc: trên trình duyệt, 10 phút, riêng từng lối vào.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   extra=[(shot('02b_filter_full'), 'Ô Trạng thái đang mở danh sách lựa chọn')],
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số BBBG”', '- Khớp một phần số BBBG', '- Chỉ lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh và ô gõ chữ, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, về trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống',
        ['- Chỉ lối “tất cả” và có V1 hoặc V2 (V2 thấy ô khóa)', '- Mặc định: trống', '- Chỉ có hiệu lực với V1']),
       ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống',
        ['- Cùng điều kiện ô Công ty', '- Chọn Công ty trước thì chỉ còn phòng ban của công ty đó']),
       ('Ngày BGNT', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', ['- Chọn 1 ngày', '- Lọc biên bản có ngày bàn giao trong ngày đó']),
       ('Số hợp đồng', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Số hợp đồng chứa chuỗi nhập', '- Lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Khách hàng', 'Dropdown', 'Enable', 'Tìm trong danh mục khách hàng', 'Không', 'Trống',
        ['- Gợi ý “Gõ để tìm khách hàng...”', '- Gõ tối thiểu 2 ký tự, tối đa 30 gợi ý', '- Lọc đúng khách hàng đã chọn']),
       ('NV kỹ thuật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', ['- Mặc định: trống', '- Lựa chọn “Họ tên - Mã phòng ban - Mã NV”']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', ['- Mặc định: trống', '- Lựa chọn như ô NV kỹ thuật']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn: Đang tạo / Chờ duyệt / Đã duyệt']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai ngày biên; được bỏ trống một đầu']),
   ],
   ev=[
       ('Đổi giá trị một ô chọn', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\nDuring:\n– Ghi nhận giá trị mới; giá trị không đổi thì bỏ qua.\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí trong phạm vi.'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh và ô Số hợp đồng, bỏ khoảng trắng đầu / cuối.\nDuring:\n– Tìm biên bản có số BBBG / số hợp '
        'đồng chứa chuỗi nhập.\nAfter:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nAfter:\n– Xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\nAfter:\n– Mở / thu gọn khối ô lọc; trạng thái mở được ghi nhớ cùng bộ lọc.'),
       ('Gõ vào ô Khách hàng', 'Change',
        'Before:\n– Đã gõ tối thiểu 2 ký tự.\nAfter:\n– Hiện tối đa 30 khách hàng khớp; chọn 1 khách hàng → lọc ngay.'),
       ('Quay lại màn trong 10 phút', 'System',
        'Before:\n– Người dùng vừa rời danh sách (vào chi tiết / sửa / màn khác).\n'
        'After:\n– Khôi phục bộ lọc, khách hàng đã chọn và trạng thái khối lọc; quá 10 phút thì bộ lọc về trống.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn những ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự. Cấu hình lưu riêng theo '
            'người dùng và theo từng lối vào của màn, không ảnh hưởng người khác và không làm đổi dữ liệu biên bản.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê các mục lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ các mục theo thứ tự thiết kế; vẫn phải bấm Lưu.\n'
           '• Bỏ tích mục đang có giá trị lọc → ô bị ẩn và giá trị lọc của ô đó bị bỏ.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bỏ thay đổi chưa lưu.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.',
       dacbiet='Lối “tất cả” có 8 mục (Công ty – Phòng ban là 1 mục chung cho 2 ô, chỉ khi có V1 / V2); lối “theo NV” có 7 mục.'),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Cài đặt bộ lọc”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách 8 mục', '–', 'Theo cấu hình đã lưu',
        ['- Công ty – Phòng ban', '- Ngày BGNT', '- Số hợp đồng', '- Khách hàng', '- NV kỹ thuật', '- Người tạo', '- Trạng thái',
         '- Ngày tạo']),
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
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình đang lưu của lối vào (chưa lưu lần nào → đủ các mục).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại và lối vào.\nDuring:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
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
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 13 cột của bảng danh sách. Ba cột STT, Số BBBG, Hành động bị khóa; cấu hình '
            'lưu riêng theo người dùng và theo lối vào trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 13 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 13 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ sau khi tải lại trang, đăng nhập lại, đổi '
               'trình duyệt; người dùng khác không bị ảnh hưởng. Cột đang hiện được tích sẵn khi Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 13 cột', '–', 'Theo cấu hình đã lưu',
        '- STT, Số BBBG, Ngày BGNT, Số hợp đồng, Khách hàng, NVKD, NV kỹ thuật, Ngày tạo, Người tạo, Ngày cập nhật, Người cập nhật, '
        'Trạng thái, Hành động.'),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Số BBBG, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/13 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu của người dùng cho lối vào.'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Cột khóa không đổi được vị trí.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change',
        'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/13 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5
TABLE_COLS = ('- Cột: STT, Tên hàng, Mã hàng hóa, Model, ĐVT, Số lượng theo hợp đồng, Số lượng đã xuất, Số lượng đã trả, Số lượng '
              'đã nghiệm thu, nhóm Thông tin chi tiết (Seri, Ngày bàn giao, Thời gian bảo hành (ngày), Hết hạn, Ghi chú)')
fr(5, 'Tạo mới biên bản bàn giao nghiệm thu',
   usecase=('FR-05', 'Tạo mới biên bản', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo mới biên bản bàn giao nghiệm thu (Lưu nháp / Lưu và tiếp tục)',
       mota='Người có quyền Tạo lập biên bản cho 1 hợp đồng / đơn hàng đã xuất hết hàng. Người dùng chọn hợp đồng ở popup (mục 2.6); '
            'hệ thống điền khách hàng, CMT/MST, SĐT, địa chỉ, NVKD, phòng ban, người nhận + SĐT người nhận và nạp bảng Hàng hoá. '
            'Người dùng nhập SL đã nghiệm thu, thông tin chi tiết, NV kỹ thuật, Ngày bàn giao, file rồi Lưu nháp (Đang tạo) — Lưu và '
            'duyệt đặc tả ở mục 2.8.',
       tacnhan=TN_LAP,
       dieukien='1. Người dùng đăng nhập thành công, có quyền “%s”.\n2. Có hợp đồng / đơn hàng có hiệu lực hoặc đã thanh lý của công '
                'ty mình, đã xuất hết hàng, chưa có biên bản.' % Q1,
       chinh='1. Người dùng bấm Tạo mới ở danh sách.\n'
             '2. Hệ thống mở màn “Tạo biên bản bàn giao nghiệm thu”; góc phải khối Thông tin chung ghi người đăng nhập và giờ hiện tại; '
             '6 ô lấy từ hợp đồng khóa, gợi ý “Tự điền theo hợp đồng”.\n'
             '3. Người dùng bấm ô Hợp đồng/đơn hàng, chọn 1 hợp đồng trong popup (mục 2.6); hệ thống điền thông tin chung và nạp '
             'bảng Hàng hoá (SL theo hợp đồng, đã xuất, đã trả).\n'
             '4. Người dùng nhập SL đã nghiệm thu từng hàng: hàng bắt buộc seri tự thêm đủ số dòng chi tiết; hàng khác thêm 1 dòng nếu '
             'chưa có; dòng mới có Thời gian bảo hành mặc định và Ngày bàn giao = Ngày bàn giao của biên bản.\n'
             '5. Người dùng nhập Seri, Thời gian bảo hành, Ghi chú từng dòng; chọn Nhân viên kỹ thuật, Ngày bàn giao (đổi ngày → ghi '
             'đè ngày bàn giao mọi dòng chi tiết), sửa Người nhận / SĐT người nhận, nhập Ghi chú, thêm file.\n'
             '6. Người dùng bấm Lưu nháp.\n'
             '7. Hệ thống kiểm tra: bắt buộc hợp đồng; ô đã nhập phải đúng định dạng; SL đã nghiệm thu không vượt SL đã xuất + đã trả; '
             'hàng bắt buộc seri có số dòng = SL; hợp đồng chưa có biên bản; có Ngày bàn giao thì hợp đồng phải đã xuất hết hàng.\n'
             '8. Hệ thống sinh mã <mã công ty người lập>.BBBG.NNNNN, lưu biên bản Đang tạo (công ty / phòng ban / bộ phận = người lập; '
             'thông tin khách, NVKD lấy lại từ hợp đồng), lưu file, dòng hàng, dòng chi tiết (Hết hạn = Ngày bàn giao + số ngày bảo '
             'hành); với hợp đồng hãng ghi Ngày bàn giao lên hợp đồng.\n'
             '9. Hệ thống ghi mốc “Tạo mới” trong lịch sử biên bản, hiển thị %s và về danh sách lối “tất cả”.' % OK_CREATE,
       phu='• Bấm Lưu và tiếp tục → lưu như trên rồi ở lại màn Tạo với form trống.\n'
           '• Chưa chọn hợp đồng → viền đỏ, %s dưới ô; thông báo %s.\n'
           '• SĐT người nhận sai định dạng (phải bắt đầu bằng 0, 10–12 chữ số) → %s; Ngày bàn giao lớn hơn hôm nay → %s.\n'
           '• SL đã nghiệm thu vượt → %s (có SL đã trả: %s); hàng bắt buộc seri lệch số dòng → %s; thông báo %s.\n'
           '• Hợp đồng đã có biên bản (người khác vừa lập) → %s dưới ô Hợp đồng.\n'
           '• Có Ngày bàn giao nhưng hợp đồng còn hàng chưa xuất hết → %s dưới ô Hợp đồng, %s dưới từng hàng đó.\n'
           '• Không có quyền Tạo → hệ thống từ chối, báo không có quyền.\n'
           '• Bấm Quay lại khi đã chọn / nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì thì về danh sách ngay.'
           % (MSG_HD, INCOMPLETE, MSG_PHONE, MSG_DATE, QTY_OVER, QTY_OVER2, QTY_SER, CHECK, DUP, NOT_EXP, NOT_EXP_ROW),
       dacbiet='Mã tự sinh theo thứ tự của công ty người lập, không nhập tay; trường duy nhất là Hợp đồng (1 hợp đồng – tối đa 1 biên '
               'bản). Các ô có dấu * (SĐT người nhận, Nhân viên kỹ thuật, Ngày bàn giao, File đính kèm) chỉ bắt buộc khi Lưu và duyệt; '
               'Lưu nháp / Lưu và tiếp tục chỉ bắt buộc hợp đồng. Nút lưu khóa trong lúc lưu. File: pdf, jpg, jpeg, png, docx, tối đa '
               '30 MB / file, tải lên ngay khi chọn. Ghi chú tối đa 65.000 ký tự; Seri, Ghi chú dòng tối đa 255 ký tự.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10_create'), shot_caption='Màn Tạo biên bản bàn giao nghiệm thu lúc mới mở'),
   extra=[(shot('10b_validate'), 'Lưu nháp khi chưa chọn hợp đồng'),
          (shot('10c_filled'), 'Đã chọn hợp đồng: hệ thống điền thông tin và nạp bảng Hàng hoá'),
          (shot('10g_phone'), 'SĐT người nhận sai định dạng khi Lưu nháp'),
          (shot('10e_unsaved'), 'Hộp Thông tin chưa lưu khi bấm Quay lại')],
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tạo biên bản bàn giao nghiệm thu”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', '- Góc phải khối Thông tin chung.'),
       ('Hợp đồng/đơn hàng', 'Textbox', 'Enable', 'Chọn từ popup', 'Có', 'Trống', [
           '- Gợi ý “Chọn hợp đồng/đơn hàng”, biểu tượng kính lúp; không gõ tay', '- Bấm → mở popup Chọn hợp đồng/đơn hàng (mục 2.6)',
           '- Lỗi: “Bắt buộc phải chọn 1 hợp đồng”']),
       ('Khách hàng', 'Textbox', 'Disable', '–', '–', 'Theo hợp đồng', '- Gợi ý “Tự điền theo hợp đồng”.'),
       ('CMT/MST', 'Textbox', 'Disable', '–', '–', 'Theo hợp đồng', '- Gợi ý “Tự điền theo hợp đồng”.'),
       ('Số điện thoại', 'Textbox', 'Disable', '–', '–', 'Theo hợp đồng', '- SĐT khách hàng; gợi ý “Tự điền theo hợp đồng”.'),
       ('Địa chỉ', 'Textbox', 'Disable', '–', '–', 'Theo hợp đồng', '- Gợi ý “Tự điền theo hợp đồng”.'),
       ('Nhân viên kinh doanh', 'Textbox', 'Disable', '–', '–', 'Theo hợp đồng', '- NVKD của hợp đồng.'),
       ('Phòng ban', 'Textbox', 'Disable', '–', '–', 'Theo hợp đồng', '- Phòng ban của NVKD trên hợp đồng.'),
       ('Số điện thoại người nhận', 'Textbox', 'Enable', '0 + 9–11 chữ số', 'Có khi Lưu và duyệt', 'Theo hợp đồng', [
           '- Gợi ý “Nhập số điện thoại”; có nút × xóa nhanh khi có chữ', '- Lỗi định dạng: “Số điện thoại không đúng định dạng”',
           '- Lưu và duyệt mà trống: “Bắt buộc phải nhập”']),
       ('Người nhận bàn giao', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Theo hợp đồng',
        ['- Gợi ý “Nhập người nhận bàn giao”; có nút × xóa nhanh', '- Lỗi: “Tối đa 255 ký tự”']),
       ('Nhân viên kỹ thuật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Có khi Lưu và duyệt', 'Trống',
        ['- Gợi ý “Chọn nhân viên kỹ thuật”; gõ để lọc', '- Lỗi: “Bắt buộc phải chọn”']),
       ('Ngày bàn giao', 'Datepicker', 'Enable', 'dd/mm/yyyy hh:mm, ≤ hôm nay', 'Có khi Lưu và duyệt', 'Trống', [
           '- Chọn ngày + giờ, ngày tương lai bị mờ', '- Đổi → ghi đè Ngày bàn giao mọi dòng chi tiết',
           '- Lỗi: “Bắt buộc phải nhập” / “Ngày bàn giao không được lớn hơn ngày hiện tại”']),
       ('Ghi chú', 'Textarea', 'Enable', '0–65.000 ký tự', 'Không', 'Trống', '- 2 dòng, gợi ý “Nhập ghi chú”.'),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, jpg, jpeg, png, docx ≤ 30 MB', 'Có khi Lưu và duyệt', 'Trống', [
           '- Nút Thêm tài liệu → chọn file là tải lên ngay', '- Mỗi dòng: STT, tên file, xem trước, tải về, xóa, dung lượng',
           '- Rỗng: “Chưa có tài liệu nào.”', '- Lỗi: “Vui lòng chọn file đính kèm”']),
       ('Bảng Hàng hoá', 'Table/Grid', 'Enable', '–', '–', 'Theo hợp đồng', [
           TABLE_COLS, '- Mỗi hàng gộp ô theo số dòng chi tiết', '- Rỗng: “Chưa có hàng hóa nào”']),
       ('Ô Số lượng đã nghiệm thu', 'Textbox', 'Enable', '0–999.999', 'Không', 'Trống', [
           '- Gợi ý “Nhập số lượng”, căn phải, chỉ nhận số', '- Đổi → tự thêm dòng chi tiết (mục Dòng sự kiện chính bước 4)',
           '- Lỗi: “Không hợp lệ” / “Không được lớn hơn số lượng đã xuất (X)” / “Không được lớn hơn tổng số lượng đã xuất và đã '
           'trả (X)” / “Phải bằng số dòng seri (n)” / “Phải bằng số lượng đã xuất (X)” (Lưu và duyệt)',
           '- X = số tương ứng trên dòng, n = số dòng chi tiết']),
       ('Ô Seri', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', ['- Gợi ý “Nhập seri”', '- Lỗi: “Tối đa 255 ký tự”']),
       ('Ô Ngày bàn giao (dòng)', 'Datepicker', 'Enable', 'dd/mm/yyyy, ≤ hôm nay', 'Có khi Lưu và duyệt', 'Ngày bàn giao của biên bản',
        ['- Đổi ở dòng đầu của hàng bắt buộc seri → chép cho mọi dòng của hàng đó', '- Lỗi: “Bắt buộc phải nhập”']),
       ('Ô Thời gian bảo hành (ngày)', 'Textbox', 'Enable', 'Số nguyên ≥ 0', 'Không', 'Bảo hành mặc định', [
           '- Mặc định: hợp đồng có bảo hành (tháng) → × 30; không thì bảo hành của hàng theo công ty (tháng × 30, năm × 365, ngày)',
           '- Lỗi: “Không hợp lệ”']),
       ('Ô Hết hạn', 'Textbox', 'Disable', 'dd/mm/yyyy', '–', 'Tự tính', '- = Ngày bàn giao dòng + Thời gian bảo hành.'),
       ('Ô Ghi chú (dòng)', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', ['- Gợi ý “Nhập ghi chú”', '- Lỗi: “Tối đa 255 ký tự”']),
       ('Nút Xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Ẩn', [
           '- Thùng rác đỏ cuối dòng chi tiết', '- Chỉ hiện khi số dòng chi tiết > SL đã nghiệm thu', '- Bấm → bỏ dòng đó']),
       ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Lưu ở trạng thái Đang tạo', '- Khóa trong lúc lưu']),
       ('Nút Lưu và duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Nút chính; xem mục 2.8.'),
       ('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Chỉ ở màn Tạo', '- Lưu Đang tạo rồi mở form trống']),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về màn trước; có thay đổi thì hỏi “Thông tin chưa lưu”.'),
       ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút Thoát: rời màn, không lưu', '- Nút Ở lại: giữ form']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Tạo biên bản bàn giao nghiệm thu thành công.”', '- Thiếu bắt buộc: “Bạn chưa nhập đầy đủ thông tin.”',
         '- Sai định dạng: “Vui lòng kiểm tra lại thông tin đã nhập”',
         '- Lỗi khác: “Tạo biên bản bàn giao nghiệm thu không thành công”']),
   ],
   ev=[
       ('Mở màn Tạo mới', 'System',
        'Before:\n– Không chặn mở form; nút Tạo mới chỉ hiện với quyền Q1.\n'
        'After:\n– Hiển thị form trống; bảng Hàng hoá “Chưa có hàng hóa nào”.'),
       ('Đổi SL đã nghiệm thu', 'Change',
        'Before:\n– Chỉ nhận số; giá trị không đổi / rỗng / 0 thì không thêm dòng.\n'
        'After:\n– Hàng bắt buộc seri: thêm cho đủ số dòng chi tiết; hàng khác: thêm 1 dòng nếu chưa có; không tự bớt dòng.'),
       ('Đổi Ngày bàn giao', 'Change',
        'Before:\n– Ngày khác ngày đang chọn.\nAfter:\n– Ghi đè Ngày bàn giao (phần ngày) cho mọi dòng chi tiết; xóa lỗi cũ của các ô đó.'),
       ('Bấm Lưu nháp / Lưu và tiếp tục', 'Click',
        'Before:\n– Kiểm tra quyền “%s”; nếu không có quyền → hệ thống từ chối, báo không có quyền và dừng xử lý.\n'
        '– Không có lượt lưu đang chạy.\n'
        'During:\n– Chưa chọn hợp đồng → %s, %s.\n'
        '– SĐT sai → %s; ngày > hôm nay → %s; SL vượt → %s; hàng bắt buộc seri lệch → %s.\n'
        '– Hợp đồng đã có biên bản → %s; có Ngày bàn giao mà hợp đồng chưa xuất hết → %s.\n' % (
            Q1, MSG_HD, INCOMPLETE, MSG_PHONE, MSG_DATE, QTY_OVER, QTY_SER, DUP, NOT_EXP)
        + ERR + '\n'
        'After:\n– Sinh mã <mã công ty>.BBBG.NNNNN, lưu biên bản Đang tạo + file + dòng hàng + dòng chi tiết; hợp đồng hãng ghi Ngày '
        'bàn giao.\n– Ghi một dòng lịch sử “Tạo mới”.\n'
        '– Hiển thị ' + OK_CREATE + '; Lưu nháp → về danh sách; Lưu và tiếp tục → form trống.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– So dữ liệu hiện tại với lúc mở.\n'
        'During:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát: về màn trước, không lưu; Ở lại: giữ form.'),
       ('Bấm Xóa dòng chi tiết', 'Click',
        'Before:\n– Số dòng chi tiết của hàng > SL đã nghiệm thu.\nAfter:\n– Bỏ dòng; gỡ lỗi cũ của hàng đó.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn hợp đồng/đơn hàng',
   usecase=('FR-06', 'Chọn hợp đồng/đơn hàng', 'view', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Popup chọn hợp đồng/đơn hàng cho biên bản',
       mota='Popup gộp 2 nguồn hợp đồng (hợp đồng hãng và hợp đồng HRM) trong 1 danh sách: chỉ hợp đồng có hiệu lực / đã thanh lý của '
            'công ty người lập, đã xuất hết hàng, chưa có biên bản (trừ chính biên bản đang sửa). Bấm vào dòng để chọn; hệ thống '
            'điền sẵn thông tin chung và hàng hoá từ hợp đồng.',
       tacnhan=TN_LAP,
       dieukien='1. Đang ở màn Tạo mới hoặc Sửa biên bản.\n2. Người dùng thuộc 1 công ty (không có công ty → popup rỗng).',
       chinh='1. Người dùng bấm ô Hợp đồng/đơn hàng.\n'
             '2. Hệ thống mở popup “Chọn hợp đồng/đơn hàng”, nạp trang 1 (hợp đồng duyệt gần nhất ở trên).\n'
             '3. Người dùng tìm theo số hợp đồng / lọc Loại hợp đồng, sắp xếp, chuyển trang.\n'
             '4. Người dùng bấm vào dòng hợp đồng cần chọn.\n'
             '5. Nếu form đã có hợp đồng → hộp %s: %s; bấm Xác nhận để tiếp tục.\n'
             '6. Hệ thống lấy dữ liệu hợp đồng: Số hợp đồng, Khách hàng, CMT/MST, SĐT, Địa chỉ, NVKD, Phòng ban, Người nhận + SĐT '
             'người nhận (ghi đè khi hợp đồng có giá trị) và nạp lại bảng Hàng hoá (bỏ hàng cũ).\n'
             '7. Popup đóng, form hiện thông tin vừa điền.' % (CH_TITLE, CH_MSG),
       phu='• Bấm Hủy ở hộp xác nhận thay đổi → giữ hợp đồng cũ.\n'
           '• Hợp đồng vừa có biên bản (người khác lập) → báo %s, form không đổi.\n'
           '• Không có hợp đồng phù hợp → “Không có hợp đồng nào phù hợp. Chỉ hợp đồng có hiệu lực / đã thanh lý của công ty bạn, '
           'đã xuất hết hàng và chưa có biên bản bàn giao nghiệm thu mới hiện ở đây.”.\n'
           '• Bấm Số hợp đồng trong popup → mở hợp đồng ở tab mới, không chọn.\n'
           '• Bấm Đóng / (x) → đóng popup, không đổi form.' % EXISTS,
       dacbiet='Hợp đồng hãng: Hợp đồng bán hàng hóa - vật tư, Hợp đồng dự án, Đơn hàng nguyên tắc ở trạng thái Có hiệu lực / Đã thanh lý. '
               'Hợp đồng HRM: trạng thái Có hiệu lực / Đã thanh lý. “Đã xuất hết hàng” = mọi dòng hàng của hợp đồng (gồm phụ lục bổ '
               'sung) có số lượng ≤ đã xuất + đã trả. Mỗi lần mở popup bộ lọc về mặc định.'),
   layout=dict(menu=MENU + ' => Tạo mới => Hợp đồng/đơn hàng', shot=shot('11_picker'), shot_caption='Popup Chọn hợp đồng/đơn hàng',
               note='Popup được mở ngay trên màn Tạo mới / Sửa theo đường dẫn ở trên.'),
   extra=[(shot('10f_change_contract'), 'Hộp Xác nhận thay đổi hợp đồng khi form đã có hợp đồng')],
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        ['- “Chọn hợp đồng/đơn hàng”', '- Phụ đề: “Hợp đồng có hiệu lực / đã thanh lý của công ty bạn, đã xuất hết hàng, chưa có biên '
         'bản bàn giao nghiệm thu”']),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số hợp đồng”', '- Khớp một phần; lọc khi bấm Tìm kiếm / Enter']),
       ('Loại hợp đồng', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống', [
           '- Gợi ý “Chọn loại hợp đồng”', '- Lựa chọn: Hợp đồng bán hàng hóa - vật tư / Hợp đồng dự án / Đơn hàng nguyên tắc / Hợp '
           'đồng HRM', '- Chọn là lọc ngay, về trang 1']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Áp ô tìm nhanh, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Xóa điều kiện lọc, nạp lại trang 1.'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- Liên tục theo trang.'),
       ('Cột Loại hợp đồng', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- Sắp xếp được (theo tên loại).'),
       ('Cột Số hợp đồng', 'Link', 'Enable', '–', '–', 'Hiển thị', ['- Bấm → mở hợp đồng ở tab mới', '- Sắp xếp được']),
       ('Cột Khách hàng', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- Tên khách hàng, tối đa 2 dòng.'),
       ('Cột Tổng thanh toán', 'Table/Grid', 'Read-only', 'dạng 1,234', '–', 'Hiển thị', '- Sắp xếp được.'),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', '–', 'Hiển thị', '- Sắp xếp được; mặc định mới nhất ở trên.'),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- Họ tên người duyệt hợp đồng.'),
       ('Dòng hợp đồng', 'Table/Grid', 'Enable', '–', '–', 'Hiển thị', '- Bấm vào dòng (ngoài liên kết) → chọn hợp đồng.'),
       ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1', '- Số dòng/trang, Hiển thị a–b / N, nút trang.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Câu “Không có hợp đồng nào phù hợp…” (mục Dòng sự kiện phụ).'),
       ('Hộp “Xác nhận thay đổi hợp đồng”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + CH_MSG, '- Nút Xác nhận, Hủy']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- ' + EXISTS, '- “Không lấy được dữ liệu hợp đồng.”']),
   ],
   ev=[
       ('Mở popup', 'System',
        'Before:\n– Bộ lọc về mặc định, trang 1.\nAfter:\n– Nạp hợp đồng theo công ty người lập, loại sẵn hợp đồng đã có biên bản / '
        'chưa xuất hết hàng.'),
       ('Chọn Loại hợp đồng', 'Change', 'Before:\n– Giá trị khác giá trị đang chọn.\nAfter:\n– Về trang 1, nạp lại.'),
       ('Bấm Tìm kiếm / Enter', 'Click', 'Before:\n– Lấy chuỗi ô tìm nhanh.\nAfter:\n– Về trang 1, nạp lại.'),
       ('Bấm vào dòng hợp đồng', 'Click',
        'Before:\n– Form đã có hợp đồng → hộp ' + CH_TITLE + '; Hủy → dừng xử lý.\n'
        'During:\n– Lấy dữ liệu hợp đồng; hợp đồng đã có biên bản → ' + EXISTS + '.\n'
        'After:\n– Điền thông tin chung, nạp lại bảng Hàng hoá, xóa lỗi cũ của ô Hợp đồng và bảng hàng; đóng popup.'),
       ('Sắp xếp / đổi trang', 'Click', 'Before:\n– Giữ bộ lọc.\nAfter:\n– Nạp lại dữ liệu.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng popup, form giữ nguyên.'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Chỉnh sửa biên bản',
   usecase=('FR-07', 'Chỉnh sửa biên bản', 'crud', A_LAP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'edit'),
   intro=dict(
       ten='Chỉnh sửa biên bản bàn giao nghiệm thu Đang tạo',
       mota='Người tạo (có quyền Tạo) sửa biên bản ở trạng thái Đang tạo: đổi được hợp đồng (chọn lại ở popup), người nhận, SĐT, NV kỹ '
            'thuật, Ngày bàn giao, Ghi chú, file, SL đã nghiệm thu và thông tin chi tiết. Lưu nháp giữ Đang tạo; Lưu và duyệt đặc tả '
            'ở mục 2.8.',
       tacnhan=TN_LAP,
       dieukien='1. Người dùng đăng nhập thành công, có quyền “%s”.\n2. Biên bản Đang tạo và người đăng nhập là người tạo.' % Q1,
       chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra điều kiện, mở màn “Sửa biên bản bàn giao nghiệm thu: <mã>” điền sẵn dữ liệu đã lưu; SL theo hợp '
             'đồng / đã xuất / đã trả lấy mới nhất từ hợp đồng.\n'
             '3. Người dùng sửa các ô rồi bấm Lưu nháp.\n'
             '4. Hệ thống kiểm tra như màn Tạo (mục 2.5), kiểm lại người tạo + Đang tạo, hợp đồng chưa có biên bản khác.\n'
             '5. Hệ thống ghi lại thông tin chung, file (thêm / gỡ), xóa – ghi lại dòng hàng và dòng chi tiết.\n'
             '6. Hệ thống ghi mốc “Thay đổi thông tin” (giá trị cũ → mới), báo %s và về danh sách.' % OK_EDIT,
       phu='• Biên bản không còn sửa được (đã duyệt / không phải người tạo / thiếu quyền) khi mở → chuyển sang trang “không tìm thấy”.\n'
           '• Biên bản đổi trạng thái trong lúc đang sửa → %s; không lưu.\n'
           '• Không phải người tạo khi lưu → “Bạn không có quyền sửa biên bản bàn giao nghiệm thu này”.\n'
           '• Không đổi gì mà Lưu nháp → không phát sinh mốc thay đổi thông tin.\n'
           '• Bấm Quay lại khi có thay đổi → hộp “Thông tin chưa lưu”.' % CONFLICT,
       dacbiet='Màn Sửa không có Lưu và tiếp tục. SĐT người nhận không bắt buộc ở màn Sửa (kể cả Lưu và duyệt — giữ như hệ thống cũ), '
               'chỉ kiểm định dạng. Lưu nháp ở màn Sửa không kiểm “hợp đồng chưa xuất hết hàng” và không ghi lại Ngày bàn giao lên hợp '
               'đồng (giữ như hệ thống cũ).'),
   layout=dict(entries=[
       (MENU + ' => Sửa', 'Từ cột Hành động của dòng Đang tạo do mình tạo.'),
       (MENU + ' => Xem chi tiết => Sửa', 'Hoặc từ chân màn chi tiết biên bản.')],
       shot=shot('12_edit'), shot_caption='Màn Sửa biên bản bàn giao nghiệm thu'),
   extra=[(shot('17b_detail_draft'), 'Chi tiết biên bản Đang tạo có nút Sửa, Xóa')],
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Sửa biên bản bàn giao nghiệm thu: <mã>”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Hợp đồng/đơn hàng', 'Textbox', 'Enable', 'Chọn từ popup', 'Có', 'Theo dữ liệu', '- Chọn lại được (mục 2.6), hỏi xác nhận thay đổi.'),
       ('Khối ô lấy từ hợp đồng', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu',
        '- Khách hàng, CMT/MST, Số điện thoại, Địa chỉ, Nhân viên kinh doanh, Phòng ban.'),
       ('Số điện thoại người nhận', 'Textbox', 'Enable', '0 + 9–11 chữ số', 'Không', 'Theo dữ liệu',
        ['- Không có dấu *', '- Lỗi: “Số điện thoại không đúng định dạng”']),
       ('Người nhận bàn giao', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Theo dữ liệu', '- Quy tắc như mục 2.5.'),
       ('Nhân viên kỹ thuật', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Có khi Lưu và duyệt', 'Theo dữ liệu',
        ['- Quy tắc như mục 2.5', '- Nhân viên đã nghỉ đang gắn vẫn hiện tên']),
       ('Ngày bàn giao', 'Datepicker', 'Enable', 'dd/mm/yyyy hh:mm', 'Có khi Lưu và duyệt', 'Theo dữ liệu', '- Quy tắc như mục 2.5.'),
       ('Ghi chú', 'Textarea', 'Enable', '0–65.000 ký tự', 'Không', 'Theo dữ liệu', '- Quy tắc như mục 2.5.'),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, jpg, jpeg, png, docx ≤ 30 MB', 'Có khi Lưu và duyệt', 'File đã lưu',
        ['- Thêm / xóa file như mục 2.5', '- File bỏ khỏi danh sách được gỡ khỏi biên bản khi Lưu']),
       ('Bảng Hàng hoá', 'Table/Grid', 'Enable', '–', '–', 'Dòng đã lưu', '- Sửa SL đã nghiệm thu, dòng chi tiết như mục 2.5.'),
       ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Lưu, giữ Đang tạo.'),
       ('Nút Lưu và duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Xem mục 2.8.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về màn trước; có thay đổi thì hỏi.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Chỉnh sửa biên bản bàn giao nghiệm thu thành công.”', '- ' + CONFLICT,
         '- “Chỉnh sửa biên bản bàn giao nghiệm thu không thành công”']),
   ],
   ev=[
       ('Mở màn Sửa', 'System',
        'Before:\n– Kiểm tra quyền “%s”, người tạo, trạng thái Đang tạo; không đạt / không tồn tại → trang “không tìm thấy”.\n'
        'After:\n– Hiển thị form đã điền dữ liệu, SL theo hợp đồng / đã xuất / đã trả mới nhất.' % Q1),
       ('Bấm Lưu nháp', 'Click',
        'Before:\n– Kiểm tra quyền “%s”; nếu không có quyền → hệ thống từ chối, báo không có quyền và dừng xử lý.\n'
        '– Kiểm tra người tạo (không → “Bạn không có quyền sửa biên bản bàn giao nghiệm thu này”) và Đang tạo (không → %s).\n'
        'During:\n– Kiểm tra như mục 2.5; hợp đồng đã có biên bản khác → %s.\n' % (Q1, CONFLICT, DUP) + ERR + '\n'
        'After:\n– Ghi lại thông tin chung, file, dòng hàng + dòng chi tiết; giữ Đang tạo.\n'
        '– Ghi lịch sử “Thay đổi thông tin” nếu có thay đổi; ' + OK_EDIT + ', về danh sách.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– So dữ liệu với lúc mở.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát: về màn trước; Ở lại: giữ form.'),
       ('Chọn lại hợp đồng', 'Click',
        'Before:\n– Hộp ' + CH_TITLE + '.\nAfter:\n– Xác nhận: thay thông tin chung + bảng hàng theo hợp đồng mới (popup loại trừ chính '
        'biên bản đang sửa khi kiểm “đã có biên bản”).'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'Lưu và duyệt biên bản',
   usecase=('FR-08', 'Lưu và duyệt', 'action', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lưu và duyệt biên bản bàn giao nghiệm thu',
       mota='Từ màn Tạo mới hoặc Sửa, người lập bấm Lưu và duyệt: hệ thống kiểm đủ luật (SĐT người nhận, NV kỹ thuật, Ngày bàn giao, '
            'file, ngày bàn giao từng dòng, SL đã nghiệm thu = SL đã xuất, hợp đồng đã xuất hết hàng), hỏi xác nhận rồi lưu biên bản '
            'ở trạng thái Đã duyệt. Sau khi duyệt biên bản không sửa / xóa được nữa. Màn không gửi thông báo.',
       tacnhan=TN_LAP,
       dieukien='1. Đang ở màn Tạo mới (có quyền Q1) hoặc Sửa (biên bản Đang tạo của mình).\n'
                '2. Đã chọn hợp đồng; hợp đồng đã xuất hết hàng.',
       chinh='1. Người dùng bấm Lưu và duyệt.\n'
             '2. Hệ thống kiểm tra trên màn: như Lưu nháp + SĐT người nhận (màn Tạo), Nhân viên kỹ thuật, Ngày bàn giao, File đính kèm, '
             'Ngày bàn giao từng dòng chi tiết bắt buộc; SL đã nghiệm thu từng hàng = SL đã xuất.\n'
             '3. Hệ thống hiện hộp %s: %s.\n'
             '4. Người dùng bấm Lưu và duyệt trong hộp.\n'
             '5. Hệ thống kiểm tra lại ở máy chủ (gồm hợp đồng chưa có biên bản khác, hợp đồng đã xuất hết hàng).\n'
             '6. Hệ thống lưu biên bản trạng thái Đã duyệt cùng file, dòng hàng, dòng chi tiết (lần Tạo: ghi Ngày bàn giao lên hợp đồng '
             'hãng).\n'
             '7. Hệ thống ghi lịch sử: “Tạo mới” (hoặc “Thay đổi thông tin” khi từ màn Sửa) và “Thay đổi trạng thái” Đang tạo → Đã duyệt.\n'
             '8. Hệ thống báo thành công (%s / %s) và về danh sách.' % (CF_TITLE, CF_MSG, OK_CREATE, OK_EDIT),
       phu='• Thiếu dữ liệu → báo lỗi tại ô (%s, %s, %s), %s; không hiện hộp xác nhận.\n'
           '• SL đã nghiệm thu khác SL đã xuất → %s dưới ô SL.\n'
           '• Bấm Hủy / (x) trong hộp → đóng hộp, không lưu, form giữ nguyên.\n'
           '• Hợp đồng còn hàng chưa xuất hết → %s dưới ô Hợp đồng, %s dưới từng hàng đó.\n'
           '• Biên bản đã đổi trạng thái (duyệt từ màn Sửa) → %s.'
           % (REQ, REQ_SEL, MSG_FILE, INCOMPLETE, QTY_EXP, NOT_EXP, NOT_EXP_ROW, CONFLICT),
       dacbiet='Giữ như hệ thống cũ (đã chốt 03/11/2026): Lưu và duyệt KHÔNG cần quyền duyệt riêng — ai có quyền Tạo đều tự duyệt '
               'được biên bản của mình; không có bước Gửi duyệt / Không duyệt; trạng thái Chờ duyệt không có đường tạo. Không hoàn tác '
               'được trên màn. Nút khóa trong lúc lưu.'),
   layout=dict(menu=MENU + ' => Tạo mới => Lưu và duyệt', shot=shot('12b_confirm_approve'),
               shot_caption='Hộp Xác nhận lưu và duyệt'),
   extra=[(shot('10d_validate'), 'Lưu và duyệt khi thiếu NV kỹ thuật, Ngày bàn giao, file và SL đã nghiệm thu chưa bằng SL đã xuất')],
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Lưu và duyệt (chân màn)', 'Button', 'Enable / Disable', 'Hiển thị', ['- Nút chính (xanh)', '- Khóa trong lúc lưu']),
       ('Hộp “Xác nhận lưu và duyệt”', 'Popup', 'Hiển thị', 'Ẩn', '- ' + CF_MSG),
       ('Nút Lưu và duyệt (trong hộp)', 'Button', 'Enable', 'Hiển thị', '- Thực hiện lưu + duyệt.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống Hủy.'),
       ('Lỗi tại ô', 'Label', 'Hiển thị', 'Ẩn', [
           '- SĐT người nhận (màn Tạo), Ngày bàn giao, Ngày bàn giao dòng: “Bắt buộc phải nhập”',
           '- Nhân viên kỹ thuật: “Bắt buộc phải chọn”', '- File đính kèm: “Vui lòng chọn file đính kèm”',
           '- SL đã nghiệm thu: “Phải bằng số lượng đã xuất (X)”', '- Ô Hợp đồng: “Hợp đồng chưa xuất hết hàng”']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Tạo biên bản bàn giao nghiệm thu thành công.” hoặc “Chỉnh sửa biên bản bàn giao nghiệm thu thành công.”',
         '- Thiếu dữ liệu: “Bạn chưa nhập đầy đủ thông tin.”']),
       ('Trạng thái sau duyệt', 'Badge', 'Read-only', 'Đã duyệt', '- Nhãn xanh lá “Đã duyệt”; nút Sửa, Xóa biến mất.'),
   ],
   ev=[
       ('Bấm Lưu và duyệt (chân màn)', 'Click',
        'Before:\n– Không có lượt lưu đang chạy.\n'
        'During:\n– Kiểm tra trên màn: thiếu → ' + REQ + ' / ' + REQ_SEL + ' / ' + MSG_FILE + ', ' + INCOMPLETE + '; SL lệch → '
        + QTY_EXP + '.\n'
        'After:\n– Hiện hộp ' + CF_TITLE + '.'),
       ('Bấm Lưu và duyệt trong hộp', 'Click',
        'Before:\n– Kiểm tra quyền “' + Q1 + '”; nếu không có quyền → hệ thống từ chối, báo không có quyền và dừng xử lý.\n'
        '– Sửa: người tạo + Đang tạo, không đạt → ' + CONFLICT + '.\n'
        'During:\n– Kiểm tra như trên ở máy chủ; hợp đồng đã có biên bản → ' + DUP + '; chưa xuất hết hàng → ' + NOT_EXP + '.\n'
        + ERR + '\n'
        'After:\n– Lưu biên bản Đã duyệt; lần Tạo ghi Ngày bàn giao lên hợp đồng hãng.\n'
        '– Ghi lịch sử (Tạo mới / Thay đổi thông tin) và một dòng “Thay đổi trạng thái” Đang tạo → Đã duyệt.\n'
        '– Hiển thị thông báo thành công, về danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nAfter:\n– Đóng hộp; form giữ nguyên, không lưu.'),
       ('Mở lại biên bản đã duyệt ở màn Sửa', 'System',
        'Before:\n– Biên bản Đã duyệt.\nAfter:\n– Hệ thống chuyển sang trang “không tìm thấy”, không cho sửa.'),
   ])

# ------------------------------------------------------------ 2.9
fr(9, 'Xóa biên bản',
   usecase=('FR-09', 'Xóa biên bản', 'action', A_LAP),
   rule=('- Quy tắc Xóa.', 'delete'),
   intro=dict(
       ten='Xóa biên bản bàn giao nghiệm thu Đang tạo',
       mota='Người tạo (có quyền Tạo) xóa biên bản Đang tạo của mình từ cột Hành động hoặc chân màn chi tiết. Hệ thống xóa biên bản, '
            'dòng hàng, dòng chi tiết; hợp đồng được giải phóng để lập biên bản mới.',
       tacnhan=TN_LAP,
       dieukien='1. Người dùng đăng nhập thành công, có quyền “%s”.\n2. Biên bản Đang tạo, người đăng nhập là người tạo.' % Q1,
       chinh='1. Người dùng bấm Xóa (thùng rác đỏ) ở cột Hành động hoặc nút Xóa ở màn chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa”: “Bạn có chắc muốn xóa bản ghi này không?”.\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm tra người tạo + Đang tạo, xóa dòng chi tiết, dòng hàng, biên bản.\n'
             '5. Hệ thống ghi mốc “Xóa” (ảnh chụp toàn bộ dữ liệu) trong lịch sử, báo “Xóa thành công.”, nạp lại danh sách (từ màn chi '
             'tiết thì về danh sách).',
       phu='• Bấm Hủy / (x) / click ra ngoài hộp → không xóa; nút Xóa vẫn bấm được bình thường.\n'
           '• Biên bản đã đổi trạng thái → %s; danh sách nạp lại.\n'
           '• Không phải người tạo → “Bạn không có quyền xóa biên bản bàn giao nghiệm thu này”.\n'
           '• Đang ở dòng cuối của trang > 1 → sau khi xóa lùi 1 trang.' % CONFLICT,
       dacbiet='Không xóa được biên bản Đã duyệt / Chờ duyệt; Super admin không xóa thay (giữ như hệ thống cũ). File đính kèm vẫn giữ '
               'trong kho file (giữ như hệ thống cũ). Ngày bàn giao đã ghi lên hợp đồng hãng không được xóa theo.'),
   layout=dict(menu=MENU + ' => Xóa', shot=shot('13_delete'), shot_caption='Hộp Xác nhận xóa',
               note='Hộp xác nhận được mở ngay trên màn hình danh sách hoặc màn chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Xóa (dòng)', 'Icon Button', 'Enable / Ẩn', 'Theo điều kiện', '- Thùng rác đỏ; chỉ dòng Đang tạo của mình + Q1.'),
       ('Nút Xóa (màn chi tiết)', 'Button', 'Enable / Ẩn', 'Theo điều kiện', '- Nút đỏ ở chân màn chi tiết, cùng điều kiện.'),
       ('Tiêu đề hộp', 'Label', 'Hiển thị', 'Ẩn', '- “Xác nhận xóa”.'),
       ('Nội dung hộp', 'Label', 'Hiển thị', 'Ẩn', '- “Bạn có chắc muốn xóa bản ghi này không?”'),
       ('Nút Xóa (trong hộp)', 'Button', 'Enable', 'Hiển thị', '- Màu đỏ; thực hiện xóa, khóa nút trong lúc xóa.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không xóa.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống Hủy.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn', ['- “Xóa thành công.”', '- ' + CONFLICT, '- “Xóa không thành công”']),
   ],
   ev=[
       ('Bấm Xóa', 'Click', 'Before:\n– Nút chỉ hiện khi đủ điều kiện.\nAfter:\n– Hiện hộp Xác nhận xóa.'),
       ('Bấm Xóa trong hộp', 'Click',
        'Before:\n– Kiểm tra quyền “' + Q1 + '”; nếu không có quyền → hệ thống từ chối, báo không có quyền và dừng xử lý.\n'
        '– Kiểm tra người tạo (không → “Bạn không có quyền xóa biên bản bàn giao nghiệm thu này”) và Đang tạo (không → ' + CONFLICT + ').\n'
        'During:\n– Xóa dòng chi tiết, dòng hàng, biên bản trong 1 lần.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Xóa”.\n– Hiển thị “Xóa thành công.”; nạp lại danh sách / về danh sách.'),
       ('Bấm Hủy / (x) / click ra ngoài hộp', 'Click',
        'Before:\n– Không xóa.\nAfter:\n– Đóng hộp, màn giữ nguyên.'),
   ])

# ------------------------------------------------------------ 2.10
fr(10, 'Xem chi tiết biên bản', usecase=('FR-10', 'Xem chi tiết biên bản', 'view', A_XEM),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết biên bản bàn giao nghiệm thu',
       mota='Màn chỉ đọc hiển thị Thông tin chung, File đính kèm, bảng Hàng hoá (SL theo hợp đồng / đã xuất / đã trả lấy mới nhất từ hợp '
            'đồng) và khối Lịch sử. Tiêu đề kèm nhãn trạng thái. Chân màn có Sửa, In, Xóa theo điều kiện và Quay lại.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Biên bản tồn tại và người dùng là người tạo, NVKD của biên bản, hoặc có quyền '
                'Xem ở mức bao trùm.',
       chinh='1. Người dùng bấm Số BBBG ở danh sách.\n'
             '2. Hệ thống kiểm tra quyền xem.\n'
             '3. Hệ thống mở màn “Chi tiết biên bản bàn giao nghiệm thu: <mã>” kèm nhãn trạng thái.\n'
             '4. Hệ thống hiển thị các khối và khối Lịch sử (thu gọn).',
       phu='• Biên bản ngoài phạm vi / không tồn tại → chuyển sang trang “không tìm thấy” (404), không báo lỗi nổi.\n'
           '• Máy chủ lỗi → “Không tải được biên bản bàn giao nghiệm thu.”.\n'
           '• Biên bản không có file → khối File đính kèm ẩn.\n'
           '• Bấm Số hợp đồng → mở hợp đồng ở tab mới; bấm Quay lại → về danh sách, khôi phục bộ lọc (10 phút).',
       dacbiet='Các ô không còn dấu *. Ngày bàn giao dạng dd/mm/yyyy hh:mm; số dạng 1,234.5.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết biên bản Đã duyệt'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        '- “Chi tiết biên bản bàn giao nghiệm thu: <mã>” + nhãn trạng thái cùng màu cột Trạng thái.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Hợp đồng/đơn hàng', 'Link', 'Read-only', '–', 'Theo dữ liệu', '- Bấm → mở hợp đồng ở tab mới.'),
       ('Khối thông tin chung', 'Textbox', 'Disable', '–', 'Theo dữ liệu',
        '- Khách hàng, CMT/MST, Số điện thoại, Địa chỉ, Nhân viên kinh doanh, Phòng ban, Số điện thoại người nhận, Người nhận bàn '
        'giao, Nhân viên kỹ thuật, Ngày bàn giao, Ghi chú.'),
       ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Ẩn khi không có file', '- Xem trước, tải về từng file.'),
       ('Bảng Hàng hoá', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [TABLE_COLS, '- Rỗng: “Chưa có hàng hóa nào”']),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút Xem lịch sử mở rộng; nội dung như mục 2.14.'),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Đang tạo + mình tạo + Q1; mục 2.7.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Mục 2.11.'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Cùng điều kiện nút Sửa; mục 2.9.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn trước (mặc định danh sách lối “tất cả”).'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra quyền xem (người tạo, NVKD, V1, V2 cùng công ty, V3 phòng quản lý); không đạt → trang “không tìm thấy”, '
        'dừng xử lý.\n'
        'During:\n– Lấy dữ liệu biên bản, file, dòng hàng, SL sống từ hợp đồng, cờ nút; lỗi khác → “Không tải được biên bản bàn giao '
        'nghiệm thu.”.\n'
        'After:\n– Hiển thị màn chỉ đọc.'),
       ('Bấm Xem lịch sử', 'Click', 'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở rộng khối, nạp các mốc lịch sử.'),
       ('Bấm Số hợp đồng', 'Click', 'Before:\n– Có hợp đồng.\nAfter:\n– Mở hợp đồng ở tab mới.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Không có dữ liệu cần lưu.\nAfter:\n– Về màn trước, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.11
fr(11, 'In biên bản', usecase=('FR-11', 'In biên bản', 'io', A_XEM),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In biên bản bàn giao nghiệm thu',
       mota='Xem trước và in một biên bản theo mẫu “BIÊN BẢN BÀN GIAO NGHIỆM THU” (mẫu HRM tự dựng): Bên nhận (khách hàng), Bên giao '
            '(công ty, NVKD, phòng ban, NV kỹ thuật), bảng hàng theo seri, chỗ ký 2 bên. Bản in mở trong cửa sổ trên màn đang đứng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm In ở cột Hành động (dòng có Sửa / Xóa: trong nút ba chấm) hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra quyền xem như màn chi tiết.\n'
             '3. Hệ thống mở cửa sổ “Xem trước biên bản bàn giao nghiệm thu”, hiện đang tải trong lúc dựng.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Biên bản ngoài phạm vi → cửa sổ báo “Bạn không có quyền xem biên bản bàn giao nghiệm thu này”.\n'
           '• Lỗi khác → “Lấy dữ liệu in không thành công”.\n'
           '• Bấm (x) → đóng cửa sổ, màn giữ nguyên.',
       dacbiet='Logo / letterhead lấy theo công ty ghi trên biên bản (công ty người lập), không theo người đang xem. “Hôm nay, ngày … tháng '
               '… năm …” lấy theo Ngày bàn giao (trống thì để chấm). Tên ký: Bên nhận = Người nhận bàn giao, Bên giao = NV kỹ thuật.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước biên bản bàn giao nghiệm thu',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Xem trước biên bản bàn giao nghiệm thu”.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → hộp thoại in của trình duyệt.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ xem trước.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead công ty của biên bản', '- “BIÊN BẢN BÀN GIAO NGHIỆM THU”, “Số: <mã>”']),
       ('Câu mở đầu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        '- “Hôm nay, ngày dd tháng mm năm yyyy, căn cứ hợp đồng/đơn hàng số <số HĐ>, hai bên tiến hành bàn giao nghiệm thu hàng hoá như sau:”'),
       ('Khối BÊN NHẬN (BÊN A)', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        '- Khách hàng, CMT/MST, Địa chỉ, Số điện thoại, Người nhận bàn giao, Số điện thoại người nhận.'),
       ('Khối BÊN GIAO (BÊN B)', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Đơn vị, Nhân viên kinh doanh, Phòng ban, Nhân viên kỹ thuật.'),
       ('Bảng DANH SÁCH HÀNG HOÁ BÀN GIAO', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Tên hàng, Mã hàng hóa, Model, ĐVT, SL nghiệm thu, Seri, Ngày bàn giao, Bảo hành (ngày), Hết hạn, Ghi chú',
         '- Mỗi hàng gộp ô theo số dòng seri', '- Rỗng: “Không có hàng hóa”']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị',
        ['- Ghi chú biên bản (nếu có), câu cam kết lập 02 bản', '- “ĐẠI DIỆN BÊN NHẬN” / “ĐẠI DIỆN BÊN GIAO”, “(Ký, ghi rõ họ tên)”']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Bạn không có quyền xem biên bản bàn giao nghiệm thu này”', '- “Lấy dữ liệu in không thành công”']),
   ],
   ev=[
       ('Bấm In (dòng / màn chi tiết)', 'Click',
        'Before:\n– Kiểm tra quyền xem; ngoài phạm vi → báo không có quyền xem, dừng xử lý.\n'
        'During:\n– Dựng bản in theo dữ liệu hiện tại; lỗi → “Lấy dữ liệu in không thành công”.\n'
        'After:\n– Hiển thị bản xem trước, letterhead theo công ty của biên bản.'),
       ('Bấm In trong cửa sổ xem trước', 'Click', 'Before:\n– Bản in đã dựng xong.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, giữ nguyên màn đang đứng.'),
       ('Đang dựng bản in', 'System', 'Before:\n– Vừa bấm In.\nAfter:\n– Hiện trạng thái đang tải tới khi có bản in.'),
   ])

# ------------------------------------------------------------ 2.12
fr(12, 'In danh sách', usecase=('FR-12', 'In danh sách', 'io', A_XEM),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In danh sách biên bản theo bộ lọc',
       mota='Xem trước và in danh sách các biên bản khớp bộ lọc + phạm vi của lối vào đang đứng (không phân trang), mẫu “DANH SÁCH BIÊN '
            'BẢN BÀN GIAO NGHIỆM THU”, có chỗ ký Người lập. Tối đa 2.000 dòng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng lọc danh sách (mục 2.2) rồi bấm In danh sách.\n'
             '2. Hệ thống lấy các biên bản theo bộ lọc trong phạm vi, dựng bản in.\n'
             '3. Hệ thống mở cửa sổ “Xem trước danh sách biên bản bàn giao nghiệm thu” (khổ ngang).\n'
             '4. Người dùng bấm In.',
       phu='• Trên 2.000 dòng → không dựng bản in, ẩn nút In, hiện “Danh sách có N dòng, vượt mức in tối đa 2,000 dòng nên chưa in '
           'được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.”.\n'
           '• Không có dòng → bản in chỉ có tiêu đề cột.\n'
           '• Lỗi khác → thông báo lỗi tải dữ liệu in; bấm (x) → đóng cửa sổ.',
       dacbiet='Letterhead theo công ty của NGƯỜI IN. Cột: STT, Số BBBG, Ngày BGNT, Số hợp đồng, Khách hàng, NVKD, NV kỹ thuật, Ngày tạo, '
               'Người tạo, Ngày cập nhật, Người cập nhật, Trạng thái. Khoảng ký Người lập → tên 15px.'),
   layout=dict(menu=MENU + ' => In danh sách', shot=shot('19_printlist'), shot_caption='Cửa sổ Xem trước danh sách',
               note='Modal Xem trước được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('19b_printlist_over'), 'Danh sách vượt 2.000 dòng: hệ thống nhắc thu hẹp bộ lọc')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Xem trước danh sách biên bản bàn giao nghiệm thu”.'),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', '- Ẩn khi vượt 2.000 dòng.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead công ty người in', '- “DANH SÁCH BIÊN BẢN BÀN GIAO NGHIỆM THU”']),
       ('Bảng danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc', '- STT + 12 cột như danh sách (trừ Hành động).'),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- “Ngày ..... Tháng ...... Năm .....”, Người lập + họ tên người in.'),
       ('Dòng nhắc vượt trần', 'Label', 'Hiển thị', '–', 'Ẩn', '- Câu “Danh sách có N dòng, vượt mức in tối đa 2,000 dòng…”.'),
   ],
   ev=[
       ('Bấm In danh sách', 'Click',
        'Before:\n– Áp phạm vi lối vào + bộ lọc đang có.\n'
        'During:\n– Đếm tổng; > 2.000 → dòng nhắc vượt trần.\n'
        'After:\n– Hiển thị bản xem trước danh sách.'),
       ('Bấm In', 'Click', 'Before:\n– Bản in đã dựng.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi.\nAfter:\n– Đóng cửa sổ, danh sách giữ nguyên.'),
       ('Lỗi khi dựng', 'System', 'Before:\n– Máy chủ lỗi.\nAfter:\n– Thông báo lỗi tải dữ liệu in.'),
   ])

# ------------------------------------------------------------ 2.13
fr(13, 'Xuất danh sách ra Excel', usecase=('FR-13', 'Xuất Excel', 'io', A_XEM),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách biên bản ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất toàn bộ biên bản khớp bộ lọc trong phạm vi của lối vào (không phân trang) ra file Excel. '
            'Cột STT luôn đứng đầu; đầu file có letterhead công ty người xuất và tiêu đề.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất file” với 11 trường, tích sẵn các trường ứng với cột đang hiện.\n'
             '3. Người dùng tích trường, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy lần lượt toàn bộ biên bản, hiện tiến độ “Đã tải x/y dòng…” rồi “Đang dựng file x/y dòng…”.\n'
             '5. Hệ thống tải file “danh_sach_bien_ban_ban_giao_nghiem_thu.xlsx”, báo “Xuất Excel thành công.”.',
       phu='• Không có biên bản khớp → không tạo file, báo “Không có dữ liệu để xuất”.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng (lấy theo từng đợt). Tiêu đề file “DANH SÁCH BIÊN BẢN BÀN GIAO NGHIỆM THU”, trang tính '
               '“Biên bản BGNT”.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất file',
               note='Modal Chọn trường xuất file được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất file”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 11 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        '- Số BBBG, Ngày BGNT, Số hợp đồng, Khách hàng, NVKD, NV kỹ thuật, Ngày tạo, Người tạo, Ngày cập nhật, Người cập nhật, Trạng thái.'),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/11 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file Excel', '- Khóa khi chưa tích trường nào hoặc đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('Nội dung file Excel', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Letterhead công ty người xuất, tiêu đề “DANH SÁCH BIÊN BẢN BÀN GIAO NGHIỆM THU”', '- Dòng tên cột: STT + các trường đã chọn']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Xuất Excel thành công.”', '- “Không có dữ liệu để xuất”', '- “Lỗi khi xuất Excel”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không có lượt xuất đang chạy.\nAfter:\n– Mở cửa sổ, tích sẵn trường ứng với cột đang hiện.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Kéo bằng biểu tượng của trường.\nAfter:\n– Đổi thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất; dữ liệu theo phạm vi lối vào.\n'
        'During:\n– Lấy toàn bộ biên bản theo bộ lọc theo từng đợt, hiện tiến độ.\n– Không có dòng → “Không có dữ liệu để xuất”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.\n' + ERR + '\n'
        'After:\n– Tải file, báo “Xuất Excel thành công.”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.14
fr(14, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của biên bản',
       mota='Xem các mốc thao tác của biên bản: người thực hiện, thời điểm, hành động, giá trị cũ → mới. Biên bản có các loại mốc: “Tạo '
            'mới”, “Thay đổi thông tin” (Hợp đồng/đơn hàng, Khách hàng, Người nhận bàn giao, Số điện thoại, Ngày bàn giao, Nhân viên kỹ '
            'thuật, Ghi chú, bảng Hàng hoá, File đính kèm) và “Thay đổi trạng thái” (Đang tạo → Đã duyệt). Cửa sổ ở danh sách và khối '
            'Lịch sử ở màn chi tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động (hoặc trong nút ba chấm), hoặc Xem lịch sử ở khối Lịch sử màn chi tiết.\n'
             '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: <mã>” và nạp các mốc.\n'
             '3. Hệ thống hiển thị các mốc, mới nhất ở trên.',
       phu='• Biên bản lập ở hệ thống cũ chưa có mốc → hiện trạng thái chưa có lịch sử.\n'
           '• Bấm Bộ lọc → mở các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Xem, in, xuất Excel không ghi mốc. Lưu không đổi gì thì không ghi mốc. Mốc “Xóa” được ghi khi xóa biên bản nhưng biên '
               'bản đã xóa không còn trên màn để mở lịch sử. Bảng Hàng hoá ghi theo từng hàng: SL đã nghiệm thu và Thông tin chi tiết '
               '(seri · BG ngày · BH n ngày · ghi chú).'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('16c_history_filter'), 'Khối Bộ lọc trong cửa sổ Lịch sử thay đổi'),
          (shot('17c_detail_history'), 'Khối Lịch sử ở màn chi tiết biên bản')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <mã>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái: “Trạng thái: Đang tạo → Đã duyệt”',
           '- Thay đổi thông tin: từng trường cũ → mới; Hàng hoá và File đính kèm dạng bảng', '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Trống',
        ['- Lựa chọn: Tạo mới / Thay đổi thông tin / Thay đổi trạng thái', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', '- Chọn là lọc ngay.'),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc từ ngày này.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc đến hết ngày này.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', '- Xóa điều kiện lọc.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Không có lịch sử phù hợp bộ lọc.”'),
       ('Khối Lịch sử ở màn chi tiết', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút Xem lịch sử / Thu gọn, Làm mới, Bộ lọc.'),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Giống nút Đóng.'),
   ],
   ev=[
       ('Mở lịch sử', 'Click',
        'Before:\n– Biên bản đang hiển thị trên danh sách / màn chi tiết của người dùng.\nDuring:\n– Nạp các mốc.\n'
        'After:\n– Hiển thị các mốc, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change', 'Before:\n– Không có nút Tìm kiếm: chọn là lọc.\nAfter:\n– Lọc lại danh sách mốc.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Khối lọc đang mở.\nAfter:\n– Xóa điều kiện lọc, hiện lại đủ các mốc.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; danh sách giữ nguyên trang và bộ lọc.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Biên bản bàn giao nghiệm thu; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi theo lối vào và quyền', [
        '– Lối “tất cả” (Công việc, CSKH sau bán): V1 / Super admin mọi biên bản; V2 công ty của người xem; V3 phòng ban người xem quản '
        'lý trong công ty mình; không quyền: biên bản mình tạo. Luôn ẩn biên bản Đang tạo của người khác.',
        '– Lối “theo NV” (Thông báo): biên bản có NVKD = người đăng nhập, không theo quyền.',
        '– Chi tiết / In / Lịch sử: người tạo, NVKD, V1, V2 cùng công ty, V3 phòng quản lý; ngoài phạm vi → trang 404.'],
     ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel', 'Lịch sử']),
    ('BR-02', 'Nguồn hợp đồng', [
        '– Hợp đồng hãng (Hợp đồng bán hàng hóa - vật tư, Hợp đồng dự án, Đơn hàng nguyên tắc; Có hiệu lực / Đã thanh lý) và hợp đồng '
        'HRM (Có hiệu lực / Đã thanh lý), cùng công ty người lập.',
        '– Chỉ hợp đồng đã xuất hết hàng: mọi dòng hàng (gồm phụ lục bổ sung) có số lượng ≤ đã xuất + đã trả.'],
     ['Chọn hợp đồng', 'Tạo mới', 'Chỉnh sửa']),
    ('BR-03', 'Duy nhất', [
        '– 1 hợp đồng có tối đa 1 biên bản; popup loại sẵn hợp đồng đã có biên bản (trừ chính biên bản đang sửa).',
        '– Lưu mà hợp đồng đã có biên bản → “Không thể tạo biên bản bàn giao nghiệm thu cho hợp đồng này”; chọn → “BBBG cho hợp '
        'đồng: <số> đã tồn tại.”.', '– Mã biên bản tự sinh <mã công ty>.BBBG.NNNNN theo công ty người lập.'],
     ['Tạo mới', 'Chỉnh sửa']),
    ('BR-04', 'Bắt buộc khi Lưu nháp', [
        '– Lưu nháp / Lưu và tiếp tục chỉ bắt buộc hợp đồng; ô đã nhập vẫn kiểm định dạng (SĐT 0 + 9–11 chữ số, ngày ≤ hôm nay, độ dài).',
        '– Tạo có Ngày bàn giao → kiểm hợp đồng đã xuất hết hàng; Sửa chỉ kiểm khi Lưu và duyệt.'],
     ['Tạo mới', 'Chỉnh sửa']),
    ('BR-05', 'Bắt buộc khi Lưu và duyệt', [
        '– SĐT người nhận (màn Tạo), Nhân viên kỹ thuật, Ngày bàn giao, File đính kèm, Ngày bàn giao từng dòng chi tiết.',
        '– SL đã nghiệm thu từng hàng = SL đã xuất; hợp đồng đã xuất hết hàng; hỏi xác nhận trước khi lưu.'],
     ['Lưu và duyệt']),
    ('BR-06', 'Số lượng và dòng chi tiết', [
        '– SL theo hợp đồng / đã xuất / đã trả lấy ở máy chủ theo hợp đồng (hợp đồng gốc + phụ lục bổ sung, trừ phụ lục giảm; hợp '
        'đồng HRM theo dòng hàng của hợp đồng), gộp theo hàng + ĐVT.',
        '– SL đã nghiệm thu 0–999.999, không vượt đã xuất + đã trả; hàng thuộc nhóm bắt buộc seri: số dòng chi tiết = SL.',
        '– Hết hạn = Ngày bàn giao dòng + Thời gian bảo hành; bảo hành mặc định theo hợp đồng (tháng × 30) hoặc theo hàng của công ty '
        'hợp đồng (tháng × 30, năm × 365, ngày).'],
     ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-07', 'Điều kiện sửa và xóa', [
        '– Chỉ biên bản Đang tạo, người đăng nhập là người tạo và có quyền “%s”.' % Q1,
        '– Super admin không sửa / xóa thay. Trạng thái đổi giữa chừng → chặn, báo tải lại trang.',
        '– Xóa: xóa dòng chi tiết + dòng hàng + biên bản; không có dữ liệu con chặn xóa; file giữ trong kho file.'],
     ['Chỉnh sửa', 'Xóa']),
    ('BR-08', 'Vòng đời biên bản', [
        '– Lưu nháp → Đang tạo (xám); Lưu và duyệt → Đã duyệt (xanh lá); Chờ duyệt (vàng) chỉ có ở dữ liệu cũ.',
        '– Không có Khóa / Gửi duyệt / Không duyệt / Hủy.'], ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-09', 'Chuẩn hóa dữ liệu lưu', [
        '– Thông tin khách hàng, NVKD, phòng ban, tên / mã / model / ĐVT hàng lấy lại từ hợp đồng ở máy chủ khi lưu (không tin dữ liệu '
        'màn gửi); hàng không còn trên hợp đồng thì giữ chữ đã gửi.',
        '– Công ty / phòng ban / bộ phận của biên bản = của người lập; Seri, Ghi chú bỏ khoảng trắng đầu / cuối.'],
     ['Tạo mới', 'Chỉnh sửa']),
    ('BR-10', 'Ghi ngược hợp đồng', [
        '– Tạo biên bản theo hợp đồng hãng: ghi Ngày bàn giao (phần ngày) lên hợp đồng; Sửa không ghi lại (giữ như hệ thống cũ).',
        '– Hợp đồng HRM không có trường này — bỏ qua.'], ['Tạo mới', 'Lưu và duyệt']),
    ('BR-11', 'In và xuất', [
        '– In biên bản: letterhead theo công ty của biên bản. In danh sách / Xuất Excel: letterhead theo công ty người thao tác.',
        '– In danh sách tối đa 2.000 dòng; Xuất Excel không giới hạn; cả hai theo phạm vi lối vào + bộ lọc.'],
     ['In biên bản', 'In danh sách', 'Xuất Excel']),
    ('BR-12', 'Hành vi giữ như hệ thống cũ (đã chốt 03/11/2026)', [
        '– Lưu và duyệt không cần quyền duyệt riêng; trạng thái Chờ duyệt không có đường tạo.',
        '– Luật “seri trống” và “sửa bảo hành phải ghi chú” chỉ áp khi dòng hàng gửi lên có nhóm hàng — thực tế không phát sinh.',
        '– Hợp đồng còn hàng chưa xuất nhưng biên bản không có hàng đó → vẫn lưu được.'],
     ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-13', 'Quy tắc ghi lịch sử', [
        '– Tạo → “Tạo mới”; sửa trường / hàng / file → “Thay đổi thông tin” (cũ → mới); Lưu và duyệt → thêm “Thay đổi trạng thái” '
        'Đang tạo → Đã duyệt; Xóa → mốc “Xóa”.', '– Xem, in, xuất, lưu không đổi gì: không ghi; hiển thị mới nhất ở trên.'],
     ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt', 'Xóa', 'Lịch sử']),
    ('BR-14', 'Sử dụng ở màn khác', [
        '– Ngày bàn giao của biên bản mới nhất = Ngày nghiệm thu hợp đồng hãng cần lắp đặt (báo cáo Tổng hợp công nợ theo NV).',
        '– Số biên bản hiện ở cột Số BBBGNT của danh sách thiết bị khách hàng.',
        '– Hàng hóa đã có trên biên bản không xóa được ở danh mục hàng hóa.',
        '– Dữ liệu dùng chung với hệ thống cũ: biên bản lập ở hệ thống cũ cũng hiện trên màn này.'],
     ['Lưu và duyệt', 'Xem danh sách']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Biên bản bàn giao nghiệm thu (biên bản, ngày bàn giao, dòng hàng, số lượng '
    'đã xuất của hợp đồng).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Hệ thống ERP', 'Hợp đồng bán hàng hóa - vật tư, Hợp đồng dự án, Đơn hàng nguyên tắc (hợp đồng hãng: nguồn của popup và dữ liệu '
                          'điền sẵn; lần Tạo biên bản ghi Ngày bàn giao lên hợp đồng; liên kết Số hợp đồng mở hệ thống cũ)',
     'Hệ thống ERP (chưa chuyển sang HRM)'),
    ('2', 'Bán hàng', 'Hợp đồng (dự án TKT) (hợp đồng HRM: nguồn thứ 2 của popup; liên kết Số hợp đồng mở màn này)',
     'Bán hàng -> Bán hàng -> Hợp đồng bán hàng'),
    ('3', 'Tài chính', 'Phiếu xuất hàng (ghi Số lượng đã xuất về dòng hợp đồng hãng — quyết định hợp đồng có hiện trong popup và điều '
                       'kiện SL đã nghiệm thu = SL đã xuất khi Lưu và duyệt)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('4', 'Bán hàng', 'Tổng hợp công nợ theo NV (Ngày nghiệm thu = Ngày bàn giao của biên bản mới nhất với hợp đồng hãng cần lắp đặt '
                      '→ Số ngày nợ)', 'Bán hàng -> Báo cáo -> Báo cáo công nợ'),
    ('5', 'CSKH sau bán', 'Yêu cầu kiểm tra sửa chữa - bảo hành (popup chọn thiết bị của khách hàng hiện và điền sẵn Số BBBGNT theo '
                          'hợp đồng của phiếu xuất)', 'CSKH sau bán -> Kiểm tra bảo hành sửa chữa'),
    ('6', 'CSKH sau bán', 'Phiếu cung cấp thông tin làm báo giá (popup chọn thiết bị của khách hàng điền sẵn Số BBBGNT)',
     'CSKH sau bán -> Danh mục'),
    ('7', 'CSKH sau bán', 'Phiếu nhập kết quả (danh sách thiết bị của khách hàng kèm Số BBBGNT)', 'CSKH sau bán -> Giao việc'),
    ('8', 'Bán hàng', 'Báo giá dịch vụ SC-BD-BT (popup chọn thiết bị của khách hàng điền sẵn Số BBBGNT)', 'Bán hàng -> Bán dịch vụ'),
    ('9', 'Danh mục dùng chung', 'Kho dữ liệu hàng hoá (không xóa được hàng hóa đã có trên dòng hàng của biên bản)',
     'Danh mục dùng chung -> Hàng hoá, vật tư'),
    ('10', 'Hệ thống ERP', 'Danh sách biên bản bàn giao nghiệm thu ở hệ thống cũ (dùng chung dữ liệu; biên bản gắn hợp đồng HRM hệ '
                           'thống cũ chưa đọc được)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
