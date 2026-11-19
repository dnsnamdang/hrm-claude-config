# -*- coding: utf-8 -*-
"""SRS màn "Phiếu xuất kho điều chỉnh kiểm kê" (mã PXKĐCKK-NNNNN) — form chuẩn, chuẩn user chốt 04/11/2026.

Chạy: python gen_srs.py  → SRS - Phiếu xuất kho điều chỉnh kiểm kê.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc
  ../phieu-xuat-dieu-chinh-sai-so-lieu/gen_srs.py (cùng nhóm Kho › Xuất kho) + ../kiem-ke-theo-hang-hoa/gen_srs.py (màn nguồn —
  thống nhất tên gọi) + ../borrow-export/gen_srs.py (có Gửi duyệt). Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột.
Nguồn đọc 09/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Entities/WarehouseInventoryExport/WarehouseInventoryExport.php (STATUSES, scopedQuery, canView / canEdit /
      canCreateProductExport), Http/Controllers/V1/WarehouseInventoryExportController.php, Services/InventoryExport/
      WarehouseInventoryExport{,Write}Service.php, Services/InventoryExport/InventoryExportWriteService.php::afterSave (Phiếu xuất
      hàng ĐCKK ghi ngược trạng thái), Services/PhysicalStockWriter.php::exportShortage, Entities/SelfInventory/SelfInventory.php
      (canInventoryExport / canHandle), Services/StockCardReportService.php, Routes/api.php}, Entities/Concerns/
      ChecksEmployeePermission.php, PermissionsTableSeeder (nhóm "Phiếu xuất kho điều chỉnh kiểm kê" — nhánh develop CHƯA có Catalog
      + mã quyền, tên quyền theo code), MasterData Position / PhysicalWarehouse (chặn xóa).
  FE  pages/warehouse/inventory-exports/** (index, create, _id/index, _id/edit, components/{InventoryExportForm.vue, constants.js,
      row-actions.js}), pages/finance/bill-payment-requests/components/AttachmentSection.vue, pages/warehouse/self-inventories/
      components/SelfInventoryForm.vue, pages/warehouse/stock-card/components/voucher-link.js, components/subsystem-menu/
      {warehouse.js, finance.js}.
  Bối cảnh: design.md, plan.md (#11893), spec docs/superpowers/specs/gop-db/2026-10-27-phieu-xuat-kho-dieu-chinh-kiem-ke-design.md.
Ảnh: ./pxkdckk_shots — dev-hrm 09/11/2026 (_capture/capture.js, DNS Admin, chặn mọi yêu cầu ghi: 0 yêu cầu ghi). GIẢ TRẠNG THÁI
  trên trình duyệt (dev không có phiếu Đang tạo): 03_list_flags (dòng PXKĐCKK-00083 hiện Đang tạo + nút Sửa), 12_edit /
  12b_confirm_send (phiếu PXKĐCKK-00091 hiện Đang tạo, sửa được). Còn lại là trạng thái thật.
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

TEN = 'Phiếu xuất kho điều chỉnh kiểm kê'
SHOTS = os.path.join(HERE, 'pxkdckk_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Xuất kho => Phiếu xuất kho điều chỉnh kiểm kê'
MENU_KK = 'Phân hệ Kho => Kiểm kho => Theo vị trí => Kiểm kê theo hàng hóa'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu xuất kho điều chỉnh kiểm kê.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
Q1 = 'Xem phiếu xuất kho điều chỉnh kiểm kê - theo tổng công ty'
Q2 = 'Xem phiếu xuất kho điều chỉnh kiểm kê - theo công ty'
Q3 = 'Kế toán kho'
Q4 = 'Xử lý phiếu kiểm kê hàng hóa'
A_XEM = 'Người xem phiếu'
A_LAP = 'Người lập phiếu'
A_KTK = 'Kế toán kho'
TN = ('Người dùng có quyền thực hiện chức năng: %s / %s (không có quyền nào thì chỉ phiếu mình tạo); %s thấy thêm mọi phiếu Chờ '
      'duyệt.' % (Q1, Q2, Q3))
TN_LAP = ('Người dùng có quyền thực hiện chức năng: %s (người lập phiếu); Sửa / Gửi duyệt phiếu Đang tạo chỉ dành cho chính người '
          'tạo phiếu.' % Q4)
TN_KTK = 'Người dùng có quyền thực hiện chức năng: %s.' % Q3
DK = ('1. Người dùng đăng nhập thành công.\n2. Phiếu nằm trong phạm vi xem của người dùng.\n'
      '3. Người dùng đang ở màn danh sách Phiếu xuất kho điều chỉnh kiểm kê.')
REQ = '“Bắt buộc phải nhập”'
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NOTFOUND = '“Không tìm thấy phiếu xuất kho điều chỉnh kiểm kê hoặc bạn không có quyền xem.”'
SRC_ERR = '“Phiếu kiểm kê không còn lập được phiếu xuất kho điều chỉnh hoặc bạn không có quyền.”'
ACC_ERR = ('“<mã hàng>: Tồn kế toán không đủ để xuất (SL được xuất: X, SL xuất: Y). Kiểm tra hàng đang giữ chỗ/giữ hàng của '
           'công ty.”')
PHY_ERR = ('“Hàng <mã - tên> không đủ tồn kho. Cần X, còn Y” / “… không đủ tồn tại vị trí <mã vị trí>. Cần X, còn Y” / “… không đủ '
           'tồn trong lô tại vị trí <mã vị trí>. Cần X, còn Y”')

d = SrsDoc(out=OUT, menu=MENU, route='/warehouse/inventory-exports', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Xuất kho': 'menu_nhom', 'Phiếu xuất kho điều chỉnh kiểm kê': 'menu_muc',
    'Kiểm kho': 'menu_nhom_kk', 'Theo vị trí': 'menu_nhom2_kk', 'Kiểm kê theo hàng hóa': 'menu_muc_kk',
    'Xem chi tiết phiếu kiểm kê': 'link_pkk', 'Tạo phiếu xuất kho điều chuyển': 'btn_xuatdc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Sửa': 'btn_sua_row', 'Gửi duyệt': 'btn_guiduyet', 'Xem chi tiết': 'link_sophieu',
    'Tạo phiếu xuất hàng': 'btn_taophieuxuathang_row', 'In': 'btn_in_row', 'In danh sách': 'btn_inds',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu xuất kho điều chỉnh kiểm kê (mã phiếu PXKĐCKK-NNNNN), phân hệ Kho, '
    'nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ luồng điều chỉnh hàng THIẾU sau kiểm kê: phiếu kiểm kê theo hàng hóa có hàng đếm được ít hơn sổ sách → người xử lý '
    'lập phiếu xuất kho điều chỉnh cho từng kho → Gửi duyệt thì hệ thống trừ ngay tồn kho thực tế theo đúng lô, đúng vị trí và báo '
    'Kế toán kho → Kế toán kho lập Phiếu xuất hàng điều chỉnh kiểm kê để hạch toán.',
    'Làm rõ các dữ liệu bị ghi ngược sang phiếu kiểm kê nguồn, tồn kho, Thẻ kho và các báo cáo kho.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới (Lưu nháp / Lưu và tiếp tục), '
    'Chỉnh sửa phiếu Đang tạo, Gửi duyệt (trừ tồn kho), Tạo phiếu xuất hàng (bước của Kế toán kho), Xem chi tiết, In phiếu, In '
    'danh sách, Xuất Excel danh sách, Xem lịch sử thay đổi. Màn KHÔNG có Xóa, Khóa / Mở khóa, Duyệt / Không duyệt trên chính màn, '
    'Hủy phiếu và Import Excel: bước hạch toán (đổi trạng thái Đang hạch toán / Đã hạch toán) thực hiện ở màn Phiếu xuất hàng điều '
    'chỉnh kiểm kê (phân hệ Tài chính).')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phiếu là chứng từ trừ tồn kho thực tế cho phần hàng thiếu: mỗi dòng trừ đúng lô nhập tại đúng vị trí của dòng kết quả kiểm kê.',
    'Đơn giá bán và Thành tiền bán trên phiếu là căn cứ giá trị hàng thiếu cho bước hạch toán.',
    'Dòng xuất của phiếu hiện ở Thẻ kho (số chứng từ PXKĐCKK-NNNNN), được cộng vào số xuất của Tổng hợp xuất nhập tồn và làm giảm '
    'tồn ở các báo cáo tồn kho.',
    'Phiếu kiểm kê nguồn chuyển Đang xử lý khi lập phiếu; Phiếu xuất hàng điều chỉnh kiểm kê đọc phiếu Chờ duyệt để hạch toán.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Chỉ lập được từ phiếu kiểm kê Chờ xử lý / Đang xử lý, còn hàng thiếu chưa xử lý, chưa có phiếu xuất kho điều chỉnh, bởi người '
    'có quyền “%s”; mỗi phiếu kiểm kê chỉ lập 1 phiếu (BR-02).' % Q4,
    'Dòng hàng do hệ thống lấy từ phiếu kiểm kê, người dùng không sửa số lượng; máy chủ lấy lại khi lưu (BR-03).',
    'Gửi duyệt trừ tồn ngay và không sửa được nữa; thiếu tồn ở bất kỳ dòng nào thì không trừ gì (BR-06).',
    'Phạm vi xem theo 2 quyền xem + Kế toán kho; không có quyền thì chỉ phiếu mình tạo; phiếu Đang tạo của người khác luôn ẩn (BR-01).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu xuất kho điều chỉnh kiểm kê (phiếu)', 'Chứng từ PXKĐCKK-NNNNN của màn này: xuất khỏi kho phần hàng THIẾU phát hiện khi '
                                                  'kiểm kê, theo từng kho của phiếu kiểm kê.'),
    ('Phiếu kiểm kê (phiếu kiểm kê theo hàng hóa)', 'Chứng từ <mã công ty>.KKK-NNNNN ở màn Kiểm kê theo hàng hóa; nguồn dữ liệu của '
                                                    'phiếu này. Mỗi phiếu kiểm kê chỉ có 1 phiếu xuất kho điều chỉnh.'),
    ('Hàng thiếu', 'Dòng kết quả kiểm kê có Thực kiểm nhỏ hơn số sổ sách (chênh lệch âm), chưa được xử lý.'),
    ('Lô / Vị trí', 'Trường đặc thù: mỗi dòng gắn 1 lô nhập (Số lô) tại 1 vị trí; khi Gửi duyệt hệ thống trừ đúng lô tại đúng vị trí.'),
    ('SL xuất', 'Số lượng thiếu còn phải xuất = |chênh lệch| − số đã xử lý, theo ĐVT của dòng kết quả kiểm kê.'),
    ('Đơn giá bán / Thành tiền bán', 'Đơn giá bán = giá bán lẻ của hàng theo công ty của phiếu kiểm kê; Thành tiền bán = SL xuất × '
                                     'Đơn giá bán.'),
    ('Tồn kế toán', 'Tồn của kho kế toán ứng với kho vật lý và công ty của lô, đã trừ hàng đang giữ chỗ / giữ hàng.'),
    ('Trạng thái Đang tạo / Chờ duyệt', 'Đang tạo (xám): lưu nháp, sửa được. Chờ duyệt (vàng): đã gửi, đã trừ tồn, chờ Kế toán kho.'),
    ('Trạng thái Đang hạch toán / Đã hạch toán', 'Đang hạch toán (xanh dương): Kế toán kho đã lập Phiếu xuất hàng ở trạng thái nháp. '
                                                 'Đã hạch toán (xanh lá): Phiếu xuất hàng đã lưu và duyệt.'),
    ('Phiếu xuất hàng điều chỉnh kiểm kê', 'Chứng từ PXHĐCKK-NNNNN (phân hệ Tài chính) do Kế toán kho lập từ phiếu Chờ duyệt.'),
    ('Cấu trúc phân cấp', 'Phiếu kiểm kê > phiếu xuất kho điều chỉnh (1 kho) > dòng hàng (hàng, ĐVT, vị trí, lô, SL xuất, giá).'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn có 2 quyền XEM theo cấp (nhóm quyền “Phiếu xuất kho điều chỉnh kiểm kê”, phân hệ Kho, tên giữ như hệ thống cũ) và dùng '
    'lại 2 quyền có sẵn: “Kế toán kho” và “Xử lý phiếu kiểm kê hàng hóa”. Không có quyền Tạo riêng: lập phiếu theo điều kiện của '
    'phiếu kiểm kê nguồn. Super admin có đủ mọi quyền. Không gắn quyền ở menu: ai cũng mở được màn, dữ liệu do hệ thống giới hạn.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q3', Q3, 'Thấy thêm MỌI phiếu Chờ duyệt (mọi công ty); có nút Tạo phiếu xuất hàng trên phiếu Chờ duyệt; nhận thông báo khi '
               'có phiếu gửi duyệt cùng công ty.'),
    ('Q4', Q4, 'Lập phiếu: ô Phiếu kiểm kê liệt kê các phiếu kiểm kê còn lập được; nút Tạo phiếu xuất kho điều chuyển ở màn Kiểm kê '
               'theo hàng hóa.'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('Q1', Q1, 'Mọi phiếu của mọi công ty; khối lọc có ô Công ty và Phòng ban.'),
    ('Q2', Q2, 'Phiếu có công ty = công ty đang làm việc; khối lọc có ô Phòng ban.'),
    ('—', 'Không có Q1 / Q2', 'Chỉ phiếu do chính mình tạo.'),
], widths=[0.8, 2.2, 3.0])
d.p('Áp chung: phiếu Đang tạo của người khác luôn bị ẩn; Kế toán kho thấy thêm mọi phiếu Chờ duyệt. Công ty / phòng ban của phiếu '
    'lấy theo người lập PHIẾU KIỂM KÊ, không theo người lập phiếu xuất.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Q4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ mọi phiếu', '✅ công ty', '✅ + phiếu Chờ duyệt', '✅ theo Q1/Q2', '✅ phiếu mình tạo'),
    ('FR-02 Tìm kiếm và lọc', '✅ (có ô Công ty, Phòng ban)', '✅ (có ô Phòng ban)', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo mới phiếu', '❌', '❌', '❌', '✅', '❌ (mở được form, ô Phiếu kiểm kê rỗng)'),
    ('FR-06 Chỉnh sửa phiếu', 'Người tạo, Đang tạo', 'Người tạo, Đang tạo', 'Người tạo, Đang tạo', 'Người tạo, Đang tạo',
     'Người tạo, Đang tạo'),
    ('FR-07 Gửi duyệt', 'Người tạo', 'Người tạo', 'Người tạo', '✅ (khi tạo)', 'Người tạo (phiếu Đang tạo)'),
    ('FR-08 Tạo phiếu xuất hàng', '❌', '❌', '✅ phiếu Chờ duyệt', '❌', '❌'),
    ('FR-09 Xem chi tiết', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ phiếu mình tạo'),
    ('FR-10 In phiếu', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ phiếu mình tạo'),
    ('FR-11 In danh sách', '✅ theo phạm vi', '✅ theo phạm vi', '✅ theo phạm vi', '✅ theo phạm vi', '✅ phiếu mình tạo'),
    ('FR-12 Xuất Excel', '✅ theo phạm vi', '✅ theo phạm vi', '✅ theo phạm vi', '✅ theo phạm vi', '✅ phiếu mình tạo'),
    ('FR-13 Xem lịch sử thay đổi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi',
     '✅ phiếu mình tạo'),
    ('Xóa / Khóa – Mở khóa / Duyệt – Không duyệt / Hủy / Import', '—', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.9, 0.85, 0.85, 0.85, 0.85, 0.9])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có Q1 / Q2: vẫn mở được màn, danh sách chỉ có phiếu do chính mình tạo; không có khối Công ty – Phòng ban.',
    'Không có Q4: vẫn thấy nút Tạo mới và mở được form, nhưng ô Phiếu kiểm kê không có lựa chọn nào nên không lập được phiếu; mở '
    'form kèm phiếu kiểm kê qua đường link thì báo %s dưới ô.' % SRC_ERR,
    'Mở chi tiết / sửa phiếu ngoài phạm vi qua đường link: hệ thống chuyển sang trang “không tìm thấy” (404), không hiện dữ liệu.',
    'Không phải người tạo / phiếu không còn Đang tạo: không có nút Sửa; mở thẳng màn Sửa thì hệ thống tự chuyển về màn chi tiết.',
    'Bị gỡ quyền giữa lúc thao tác: lần nạp dữ liệu / lần lưu tiếp theo hệ thống áp quyền mới (quyền kiểm lại ở từng lần gọi).',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới, Xuất Excel, In danh sách, Cấu hình cột, Cài đặt bộ lọc', 'Luôn hiện', 'Dữ liệu giới hạn theo phạm vi xem'),
    ('Nút Sửa (dòng, màn chi tiết)', 'Phiếu Đang tạo VÀ người đăng nhập là người tạo', '—'),
    ('Nút Tạo phiếu xuất hàng (dòng, màn chi tiết)', 'Phiếu Chờ duyệt VÀ có quyền Q3', 'Mở màn Phiếu xuất hàng điều chỉnh kiểm kê'),
    ('Nút In, Lịch sử trên dòng', 'Luôn hiện trên mọi dòng', 'Không có nút Xóa'),
    ('Khối lọc Công ty / Phòng ban', 'Q1 (hoặc Super admin): Công ty + Phòng ban; Q2: Phòng ban', '—'),
    ('Nút Tạo phiếu xuất kho điều chuyển (màn Kiểm kê theo hàng hóa)', 'Phiếu kiểm kê Chờ / Đang xử lý + Q4 + còn hàng thiếu + '
     'chưa có phiếu xuất kho điều chỉnh', 'Mở form Tạo mới chọn sẵn phiếu kiểm kê'),
], widths=[2.4, 2.0, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_XEM, [0, 5, 6, 7]), (A_LAP, [1, 2, 3]), (A_KTK, [4])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Tạo mới phiếu', 'crud'),
     ('FR-06', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-07', 'Gửi duyệt phiếu', 'action'),
     ('FR-08', 'Tạo phiếu xuất hàng', 'action'),
     ('FR-10', 'In phiếu', 'io'),
     ('FR-11', 'In danh sách', 'io'),
     ('FR-12', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-09', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu xuất kho điều chỉnh kiểm kê')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu xuất kho điều chỉnh kiểm kê',
       mota='Hiển thị bảng các phiếu xuất kho điều chỉnh kiểm kê trong phạm vi xem của người dùng (theo Q1 / Q2, không có quyền thì '
            'chỉ phiếu mình tạo; Kế toán kho thấy thêm phiếu Chờ duyệt), kèm phân trang, sắp xếp và tổng số phiếu khớp bộ lọc. Mỗi '
            'dòng có liên kết sang chi tiết phiếu, sang phiếu kiểm kê nguồn và các nút Sửa, Tạo phiếu xuất hàng, In, Lịch sử theo '
            'điều kiện.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng để mở màn; dữ liệu giới hạn theo phạm vi xem.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem: Q1 / Super admin mọi phiếu; Q2 phiếu của công ty đang làm việc; không có quyền thì '
             'phiếu mình tạo; ẩn phiếu Đang tạo của người khác; Kế toán kho thêm mọi phiếu Chờ duyệt.\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu vừa đi vào màn chi tiết / sửa của màn này) và cấu '
             'hình cột đã lưu của người dùng.\n'
             '4. Hệ thống lấy các phiếu trong phạm vi khớp bộ lọc, sắp phiếu tạo gần nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, kèm dòng “Hiển thị a–b / N” và phân trang.\n'
             '6. Với từng dòng, hệ thống tính nút Sửa (Đang tạo + người tạo) và Tạo phiếu xuất hàng (Chờ duyệt + Kế toán kho).',
       phu='• Không có phiếu nào trong phạm vi / khớp bộ lọc → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Máy chủ lỗi khi nạp → thông báo “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”, bảng trống.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, xóa phiên và chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 11 cột; không có cột ẩn mặc định. Cột khóa trong Tùy chỉnh cột: STT, Số phiếu, Hành động. '
               'Sắp xếp được: Số phiếu, Ngày tạo, Ngày duyệt; mặc định Ngày tạo mới nhất ở trên. Cột Ngày kiểm kê hiển thị NGÀY LẬP '
               'phiếu xuất (dd/mm/yyyy) — giữ như hệ thống cũ. Đổi bộ lọc, sắp xếp, số dòng đều về trang 1; mỗi trang tối đa 200 '
               'dòng.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Phiếu xuất kho điều chỉnh kiểm kê'),
   extra=[(shot('03_list_flags'), 'Dòng phiếu Đang tạo có nút Sửa; dòng Chờ duyệt có nút Tạo phiếu xuất hàng')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- Thanh tiêu đề / tab: “Phiếu xuất kho điều chỉnh kiểm kê”',
         '- Tiêu đề bảng: “Danh sách phiếu xuất kho điều chỉnh kiểm kê”']),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', '- Luôn hiện; bấm → mở màn Tạo phiếu xuất kho điều chỉnh kiểm kê (mục 2.5).'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.12)',
         '- Khóa trong lúc đang xuất; bên cạnh hiện tiến độ “Đang chuẩn bị dữ liệu…”']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.11).'),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', 'PXKĐCKK-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết phiếu (mục 2.9)', '- Sắp xếp được', '- Cột khóa']),
       ('Cột Phiếu kiểm kê', 'Table/Grid', 'Read-only', '<mã công ty>.KKK-NNNNN', 'Hiển thị',
        ['- Mã phiếu kiểm kê nguồn', '- Là liên kết: bấm → mở chi tiết phiếu kiểm kê ở TAB MỚI', '- Không sắp xếp']),
       ('Cột Ngày kiểm kê', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Hiển thị',
        ['- Ngày lập phiếu xuất kho điều chỉnh (như hệ thống cũ)', '- Không sắp xếp']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Dạng “Mã kho - Tên kho”.'),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Dạng “Mã phòng ban - Họ tên”.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Thời điểm tạo phiếu', '- Sắp xếp được; mặc định mới nhất ở trên']),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Kế toán kho đã lập Phiếu xuất hàng điều chỉnh kiểm kê', '- Trống khi phiếu Đang tạo / Chờ duyệt']),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Thời điểm lập / lưu Phiếu xuất hàng điều chỉnh kiểm kê', '- Sắp xếp được']),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 4 giá trị', 'Hiển thị',
        ['- Đang tạo: nhãn xám', '- Chờ duyệt: nhãn vàng', '- Đang hạch toán: nhãn xanh dương', '- Đã hạch toán: nhãn xanh lá']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Nút Sửa: Đang tạo + người tạo → màn Sửa (mục 2.6)',
           '- Nút Tạo phiếu xuất hàng: Chờ duyệt + Kế toán kho → màn Phiếu xuất hàng (mục 2.8)',
           '- Nút In → cửa sổ Xem trước phiếu (mục 2.10); nút Lịch sử → cửa sổ Lịch sử thay đổi (mục 2.13)',
           '- Dòng có trên 3 nút: nút cuối gom vào “Hành động khác” (ba chấm)', '- Không có nút Xóa', '- Cột khóa']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Không có dữ liệu phù hợp.” khi N = 0.'),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang', '- N: tổng số phiếu khớp bộ lọc trong phạm vi xem']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Trang đầu: về đầu / lùi mờ; trang cuối: tiến / về cuối mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.” khi máy chủ lỗi.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định phạm vi xem theo quyền (Q1 > Q2 > phiếu mình tạo; ẩn Đang tạo của người khác; Kế toán kho thêm Chờ duyệt).\n'
        '– Khôi phục bộ lọc (10 phút) và cấu hình cột đã lưu.\n'
        'During:\n– Lấy các phiếu trong phạm vi khớp bộ lọc; tính cờ Sửa / Tạo phiếu xuất hàng cho từng dòng.\n'
        '– Máy chủ lỗi → hiển thị “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, phiếu tạo mới nhất ở trên, kèm dòng “Hiển thị a–b / N”.'),
       ('Bấm Số phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem.\n'
        'After:\n– Mở màn chi tiết phiếu (mục 2.9); bộ lọc hiện tại được ghi nhớ 10 phút để khôi phục khi quay lại.'),
       ('Bấm mã Phiếu kiểm kê', 'Click',
        'Before:\n– Dòng có phiếu kiểm kê nguồn.\n'
        'After:\n– Mở chi tiết phiếu kiểm kê ở tab mới; danh sách giữ nguyên trang và bộ lọc.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Số phiếu, Ngày tạo, Ngày duyệt hỗ trợ sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại theo số dòng mới.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu xuất kho điều chỉnh kiểm kê',
       mota='Thu hẹp danh sách theo số phiếu, kho, trạng thái, người tạo, mã / tên hàng hóa trên phiếu, ngày tạo và Công ty – Phòng '
            'ban. Ô tìm nhanh tìm theo số phiếu; các ô lọc nằm trong khối Tìm kiếm nâng cao, bật / tắt được bằng Cài đặt bộ lọc '
            '(mục 2.3). Mọi điều kiện chỉ lọc trong phạm vi xem của người dùng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập số phiếu vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Hệ thống lọc ngay khi một ô lọc đổi giá trị (ô chữ lọc khi gõ), về trang 1.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.\n'
             '5. Hệ thống ghi nhớ bộ lọc 10 phút khi người dùng đi vào màn chi tiết / sửa của màn này.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Gõ vào ô tìm nhanh mà chưa bấm Tìm kiếm / Enter → danh sách chưa đổi.\n'
           '• Bấm dấu × trong ô chọn → xóa giá trị của ô đó.\n'
           '• Không có Q1 / Q2 → không có ô Công ty / Phòng ban.',
       dacbiet='Ô tìm nhanh và ô Mã phiếu cùng tìm theo số phiếu. Kiểu khớp chữ: một phần, không phân biệt hoa / thường, bỏ khoảng '
               'trắng đầu / cuối; không giới hạn số ký tự; ký tự % và _ được hiểu là ký tự đại diện. Mã hàng hóa / Tên hàng hóa lọc '
               'phiếu có ÍT NHẤT 1 dòng hàng khớp. Mọi điều kiện kết hợp kiểu VÀ. Ngày tạo lấy trọn hai ngày biên. Ô Kho / Người tạo '
               'chỉ liệt kê giá trị có trên phiếu trong phạm vi xem. Ô Công ty chỉ có hiệu lực với Q1 / Super admin. Ghi nhớ bộ lọc: '
               'trên trình duyệt, 10 phút.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số phiếu”', '- Khớp một phần số phiếu', '- Chỉ lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, về trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Mã phiếu', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', ['- Số phiếu chứa chuỗi nhập', '- Lọc ngay khi gõ']),
       ('Kho', 'Dropdown', 'Enable', 'Danh sách kho', 'Không', 'Trống',
        ['- Mặc định: trống (mọi kho)', '- Lựa chọn “Mã kho - Tên kho”, chỉ kho có trên phiếu trong phạm vi']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 4 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn: Đang tạo / Chờ duyệt / Đang hạch toán / Đã hạch toán']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách người đã tạo phiếu', 'Không', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn “Mã phòng ban - Họ tên”']),
       ('Mã hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', '- Phiếu có dòng hàng mã chứa chuỗi nhập.'),
       ('Tên hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', '- Phiếu có dòng hàng tên chứa chuỗi nhập.'),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai ngày biên; được bỏ trống một đầu']),
       ('Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống', ['- Chỉ hiện với Q1 / Super admin', '- Mặc định: trống']),
       ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống',
        ['- Chỉ hiện với Q1 hoặc Q2', '- Chọn Công ty trước thì chỉ còn phòng ban của công ty đó']),
   ],
   ev=[
       ('Đổi giá trị một ô lọc', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\nDuring:\n– Ghi nhận giá trị mới (ô chữ: theo từng ký tự gõ).\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí trong phạm vi xem.'),
       ('Bấm Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, bỏ khoảng trắng đầu / cuối.\nDuring:\n– Tìm phiếu có số phiếu chứa chuỗi nhập.\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nAfter:\n– Xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\n'
        'After:\n– Mở / thu gọn khối ô lọc; lần mở đầu hệ thống nạp danh sách Kho, Trạng thái, Người tạo.'),
       ('Quay lại từ màn chi tiết trong 10 phút', 'System',
        'Before:\n– Người dùng vừa đi từ danh sách vào màn chi tiết / sửa.\n'
        'After:\n– Khôi phục bộ lọc và trạng thái khối lọc; quá 10 phút thì bộ lọc về trống.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn những ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự. Cấu hình lưu riêng '
            'theo người dùng cho màn này, không ảnh hưởng người khác và không làm đổi dữ liệu phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 8 mục lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 8 mục theo thứ tự thiết kế; vẫn phải bấm Lưu.\n'
           '• Bỏ tích mục đang có giá trị lọc → ô bị ẩn và giá trị lọc của ô đó bị bỏ.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bỏ thay đổi chưa lưu.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.',
       dacbiet='Mục “Công ty – Phòng ban” là một mục chung cho 2 ô; ô nào hiện vẫn theo quyền (mục 2.2).'),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Cài đặt bộ lọc”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách 8 mục', '–', 'Theo cấu hình đã lưu',
        ['- Mã phiếu', '- Kho', '- Trạng thái', '- Người tạo', '- Mã hàng hóa', '- Tên hàng hóa', '- Ngày tạo',
         '- Công ty – Phòng ban']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → ô lọc đó không hiện.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích lại đủ 8 mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
       ('Khối Tìm kiếm nâng cao sau khi lưu', 'Label', 'Hiển thị', '–', '–', 'Theo cấu hình', '- Chỉ hiện ô đã tích, đúng thứ tự.'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình đang lưu (chưa lưu lần nào → đủ 8 mục).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ 8 mục, thứ tự thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 11 cột của bảng danh sách. Ba cột STT, Số phiếu, Hành động bị khóa; cấu '
            'hình lưu riêng theo người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 11 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 11 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ sau khi tải lại trang, đăng nhập lại, đổi '
               'trình duyệt; người dùng khác không bị ảnh hưởng. Cột đang hiện được tích sẵn khi Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 11 cột', '–', 'Theo cấu hình đã lưu',
        '- STT, Số phiếu, Phiếu kiểm kê, Ngày kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái, Hành động.'),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Số phiếu, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/11 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu của người dùng.'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Cột khóa không đổi được vị trí.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change',
        'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/11 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5
fr(5, 'Tạo mới phiếu xuất kho điều chỉnh kiểm kê',
   usecase=('FR-05', 'Tạo mới phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo mới phiếu xuất kho điều chỉnh kiểm kê (Lưu nháp / Lưu và tiếp tục)',
       mota='Lập phiếu xuất hàng thiếu của 1 phiếu kiểm kê tại 1 kho. Người dùng chọn Phiếu kiểm kê (hoặc vào từ nút Tạo phiếu xuất '
            'kho điều chuyển ở màn Kiểm kê theo hàng hóa — chọn sẵn), hệ thống tự điền Kho và nạp bảng Chi tiết gồm các dòng hàng '
            'thiếu chưa xử lý kèm vị trí, lô, SL xuất và giá (chỉ đọc). Lưu nháp tạo phiếu ở trạng thái Đang tạo (chưa trừ tồn); '
            'Gửi duyệt được đặc tả ở mục 2.7. Lưu xong phiếu kiểm kê nguồn chuyển Đang xử lý.',
       tacnhan=TN_LAP,
       dieukien='1. Người dùng đăng nhập thành công, có quyền “%s”.\n2. Có phiếu kiểm kê Chờ xử lý / Đang xử lý còn hàng thiếu '
                'chưa xử lý và chưa có phiếu xuất kho điều chỉnh.' % Q4,
       chinh='1. Người dùng bấm Tạo mới ở danh sách (hoặc Tạo phiếu xuất kho điều chuyển ở chi tiết phiếu kiểm kê).\n'
             '2. Hệ thống mở màn “Tạo phiếu xuất kho điều chỉnh kiểm kê”; góc phải khối Thông tin chung ghi người đăng nhập và giờ '
             'hiện tại; nạp danh sách phiếu kiểm kê còn lập được.\n'
             '3. Người dùng chọn Phiếu kiểm kê; hệ thống điền Kho = kho đầu tiên của phiếu kiểm kê và nạp bảng Chi tiết (hàng thiếu '
             'của kho đó).\n'
             '4. Người dùng có thể đổi Kho (chỉ các kho của phiếu kiểm kê) → hệ thống nạp lại hàng thiếu của kho mới.\n'
             '5. Người dùng nhập Ghi chú, đính kèm file (không bắt buộc khi lưu nháp) rồi bấm Lưu nháp.\n'
             '6. Hệ thống kiểm tra lại điều kiện phiếu kiểm kê, kho, lấy lại dòng hàng ở máy chủ và kiểm tồn kế toán.\n'
             '7. Hệ thống sinh mã PXKĐCKK-NNNNN, lưu phiếu Đang tạo (công ty / phòng ban theo người lập phiếu kiểm kê), lưu dòng '
             'hàng; chuyển phiếu kiểm kê sang Đang xử lý (ghi lịch sử phiếu kiểm kê).\n'
             '8. Hệ thống ghi mốc “Tạo mới” trong lịch sử phiếu, hiển thị “Lưu thành công.” và về danh sách.',
       phu='• Bấm Lưu và tiếp tục → lưu nháp như trên rồi ở lại màn Thêm với form trống, nạp lại danh sách phiếu kiểm kê.\n'
           '• Chưa chọn Phiếu kiểm kê → viền đỏ, %s dưới ô; thông báo “Bạn chưa nhập đầy đủ thông tin.”.\n'
           '• Kho không còn hàng thiếu → bảng ghi “Kho này không còn hàng thiếu cần xuất điều chỉnh”, lưu bị chặn với câu “Kho không '
           'còn hàng thiếu cần xuất điều chỉnh.”.\n'
           '• Phiếu kiểm kê (vào qua đường link) không còn lập được → báo %s dưới ô, bỏ chọn.\n'
           '• Hai người lập cùng lúc cho 1 phiếu kiểm kê → người lưu sau nhận “Phiếu kiểm kê không còn lập được phiếu xuất kho '
           'điều chỉnh. Vui lòng load lại trang”.\n'
           '• Tồn kế toán không đủ → %s; không lưu.\n'
           '• Bấm Quay lại khi đã chọn / nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì thì về danh sách ngay.'
           % (REQ, SRC_ERR, ACC_ERR),
       dacbiet='Không sửa được số lượng / giá: dòng hàng do hệ thống lấy từ phiếu kiểm kê. Nút lưu khóa trong lúc lưu để một lần '
               'bấm không tạo 2 phiếu. Mã PXKĐCKK-NNNNN tự sinh theo thứ tự, không nhập tay; mỗi phiếu kiểm kê chỉ lập 1 phiếu (lập '
               'xong phiếu kiểm kê biến khỏi ô chọn). File đính kèm: pdf, png, jpg, jpeg, tối đa 20 MB / file, tải lên ngay khi chọn.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới', 'Từ nút Tạo mới trên danh sách: form trống, chọn Phiếu kiểm kê tại ô.'),
       (MENU_KK + ' => Xem chi tiết phiếu kiểm kê => Tạo phiếu xuất kho điều chuyển',
        'Hoặc từ chi tiết một phiếu kiểm kê đủ điều kiện (chỉ người có quyền Q4 thấy nút): form chọn sẵn phiếu kiểm kê đó.')],
       shot=shot('10_create'), shot_caption='Màn Tạo phiếu xuất kho điều chỉnh kiểm kê lúc mới mở'),
   extra=[(shot('09_si_button'), 'Chi tiết phiếu kiểm kê có nút Tạo phiếu xuất kho điều chuyển'),
          (shot('10c_filled'), 'Đã chọn Phiếu kiểm kê: hệ thống điền Kho và nạp hàng thiếu'),
          (shot('10b_validate'), 'Lưu nháp khi chưa chọn Phiếu kiểm kê'),
          (shot('10e_unsaved'), 'Hộp Thông tin chưa lưu khi bấm Quay lại')],
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tạo phiếu xuất kho điều chỉnh kiểm kê”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', '- Góc phải khối Thông tin chung.'),
       ('Phiếu kiểm kê', 'Dropdown', 'Enable', 'Danh sách phiếu còn lập được', 'Có', 'Trống / phiếu chọn sẵn', [
           '- Gợi ý “Chọn phiếu kiểm kê” (“Đang tải...” khi đang nạp)',
           '- Icon ⓘ: “Chỉ liệt kê phiếu kiểm kê Chờ xử lý / Đang xử lý còn hàng thiếu chưa xuất điều chỉnh.”',
           '- Đã chọn: cạnh nhãn có biểu tượng mở phiếu kiểm kê ở tab mới', '- Lỗi: “Bắt buộc phải nhập”']),
       ('Kho', 'Dropdown', 'Enable / Disable', 'Kho của phiếu kiểm kê', 'Có', 'Kho đầu tiên của phiếu kiểm kê', [
           '- Khóa khi chưa chọn phiếu kiểm kê',
           '- Icon ⓘ: “Chọn phiếu kiểm kê trước — kho lấy theo các kho của phiếu kiểm kê.” (khi ô đang khóa)',
           '- Icon ⓘ: “Kho thuộc phiếu kiểm kê — đổi kho sẽ nạp lại hàng thiếu của kho đó.” (khi đã chọn phiếu)']),
       ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Có khi Gửi duyệt', 'Trống',
        ['- 2 dòng, gợi ý “Nhập ghi chú”, không gõ quá 255 ký tự', '- Nhãn luôn có dấu *, nhưng Lưu nháp được để trống',
         '- Lỗi: “Bắt buộc phải nhập” / “Vui lòng nhập tối đa 255 ký tự.”']),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, png, jpg, jpeg ≤ 20 MB', 'Có khi Gửi duyệt', 'Trống',
        ['- Nút Thêm tài liệu → thêm dòng, chọn file là tải lên ngay', '- Mỗi dòng: STT, tên file, xem trước, tải về, xóa, dung lượng',
         '- Lỗi: “Bắt buộc phải nhập”, “Định dạng file không hợp lệ”, “File quá lớn”']),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', '–', 'Theo phiếu kiểm kê + kho', [
           '- Cột: STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí, Lô, SL xuất, Đơn giá bán, Thành tiền bán',
           '- Số dạng 1,234.5 (tối đa 2 chữ số thập phân)',
           '- Rỗng: “Chọn phiếu kiểm kê để nạp hàng thiếu cần xuất điều chỉnh” / “Kho này không còn hàng thiếu cần xuất điều chỉnh”']),
       ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Rê chuột: “Lưu phiếu ở trạng thái Đang tạo”', '- Chỉ bắt chọn Phiếu kiểm kê (+ Kho)', '- Khóa trong lúc lưu']),
       ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Xem mục 2.7.'),
       ('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Chỉ ở màn Thêm', '- Rê chuột: “Lưu nháp rồi mở form trống để lập phiếu tiếp”']),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi “Thông tin chưa lưu”.'),
       ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút Thoát: rời màn, không lưu', '- Nút Ở lại: giữ form']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Lưu thành công.”', '- Thiếu dữ liệu: “Bạn chưa nhập đầy đủ thông tin.”', '- Tồn kế toán: ' + ACC_ERR,
         '- Lỗi khác: “Lưu thất bại.”']),
   ],
   ev=[
       ('Mở màn Tạo mới', 'System',
        'Before:\n– Không cần quyền để mở form.\n'
        'During:\n– Nạp danh sách phiếu kiểm kê còn lập được (không có quyền Q4 → rỗng); vào kèm phiếu kiểm kê thì nạp kho + hàng '
        'thiếu của phiếu đó; phiếu không còn lập được → ' + SRC_ERR + ' dưới ô.\n'
        'After:\n– Hiển thị form; Kho khóa khi chưa có phiếu kiểm kê.'),
       ('Chọn / bỏ chọn Phiếu kiểm kê', 'Change',
        'Before:\n– Giá trị khác giá trị đang chọn.\n'
        'During:\n– Chọn: nạp kho của phiếu (mặc định kho đầu tiên) và hàng thiếu của kho; bỏ chọn: xóa Kho và bảng Chi tiết.\n'
        'After:\n– Xóa lỗi đang hiện ở ô Phiếu kiểm kê / Kho / Chi tiết.'),
       ('Đổi Kho', 'Change',
        'Before:\n– Đã chọn phiếu kiểm kê; kho khác kho đang chọn.\nAfter:\n– Nạp lại hàng thiếu của kho mới vào bảng Chi tiết.'),
       ('Bấm Lưu nháp / Lưu và tiếp tục', 'Click',
        'Before:\n– Không có lượt lưu đang chạy.\n'
        'During:\n– Chưa chọn Phiếu kiểm kê / Kho → ' + REQ + ' dưới ô, “Bạn chưa nhập đầy đủ thông tin.”.\n'
        '– Bảng trống → “Kho không còn hàng thiếu cần xuất điều chỉnh.”; Ghi chú > 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”.\n'
        '– Máy chủ kiểm lại phiếu kiểm kê còn lập được (không → “Phiếu kiểm kê không còn lập được phiếu xuất kho điều chỉnh. Vui '
        'lòng load lại trang”), kho thuộc phiếu kiểm kê, lấy lại dòng hàng, kiểm tồn kế toán theo hàng + công ty lô.\n' + ERR + '\n'
        'After:\n– Sinh phiếu PXKĐCKK-NNNNN trạng thái Đang tạo, lưu dòng hàng; phiếu kiểm kê → Đang xử lý.\n'
        '– Ghi một dòng lịch sử “Tạo mới”.\n'
        '– Hiển thị “Lưu thành công.”; Lưu nháp → về danh sách; Lưu và tiếp tục → form trống.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– So dữ liệu hiện tại (phiếu kiểm kê, kho, ghi chú, file mới) với lúc mở.\n'
        'During:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát: về danh sách, không lưu; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Chỉnh sửa phiếu',
   usecase=('FR-06', 'Chỉnh sửa phiếu', 'crud', A_LAP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'edit'),
   intro=dict(
       ten='Chỉnh sửa phiếu xuất kho điều chỉnh kiểm kê Đang tạo',
       mota='Người tạo sửa phiếu đang ở trạng thái Đang tạo: chỉ đổi được Ghi chú và File đính kèm; Phiếu kiểm kê, Kho và bảng Chi '
            'tiết giữ nguyên như lúc tạo (không nạp lại). Lưu nháp giữ trạng thái Đang tạo; Gửi duyệt từ màn Sửa cũng trừ tồn như '
            'khi tạo (mục 2.7).',
       tacnhan=TN_LAP,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu đang Đang tạo và người đăng nhập là người tạo phiếu.',
       chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra điều kiện, mở màn “Sửa phiếu xuất kho điều chỉnh kiểm kê: <mã>” điền sẵn dữ liệu.\n'
             '3. Người dùng sửa Ghi chú, thêm / xóa file rồi bấm Lưu nháp.\n'
             '4. Hệ thống kiểm tra lại Đang tạo + người tạo, kiểm tồn kế toán theo dòng hàng của phiếu.\n'
             '5. Hệ thống lưu, ghi mốc “Thay đổi thông tin” (giá trị cũ → mới của Ghi chú / File đính kèm), báo “Lưu thành công.” '
             'và về danh sách.',
       phu='• Phiếu không còn sửa được (đã gửi / không phải người tạo) khi mở → tự chuyển về màn chi tiết.\n'
           '• Phiếu đổi trạng thái trong lúc đang sửa → %s; không lưu.\n'
           '• Xóa file ĐÃ LƯU → hộp “Xác nhận xóa” (“Bạn có chắc muốn xóa file đính kèm này?”, Xóa / Hủy); bấm Xóa là gỡ file khỏi '
           'phiếu NGAY (không chờ Lưu), báo “Xóa file thành công”, ghi lịch sử.\n'
           '• Không đổi gì mà Lưu nháp → không phát sinh mốc thay đổi thông tin.\n'
           '• Bấm Quay lại khi có thay đổi → hộp “Thông tin chưa lưu”.\n'
           '• Phiếu ngoài phạm vi / không tồn tại → trang “không tìm thấy”.' % CONFLICT,
       dacbiet='Màn Sửa không có Lưu và tiếp tục. Ghi chú ≤ 255 ký tự. Không có Xóa phiếu (giữ như hệ thống cũ).'),
   layout=dict(entries=[
       (MENU + ' => Sửa', 'Từ cột Hành động của dòng phiếu Đang tạo do mình tạo.'),
       (MENU + ' => Xem chi tiết => Sửa', 'Hoặc từ chân màn chi tiết phiếu.')],
       shot=shot('12_edit'), shot_caption='Màn Sửa phiếu xuất kho điều chỉnh kiểm kê (ảnh giả trạng thái Đang tạo trên trình duyệt)'),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Sửa phiếu xuất kho điều chỉnh kiểm kê: <mã phiếu>”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu kiểm kê', 'Link', 'Read-only', '–', '–', 'Theo dữ liệu', '- Bấm → mở chi tiết phiếu kiểm kê ở tab mới.'),
       ('Kho', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', '- Icon ⓘ: “Kho không đổi được sau khi tạo phiếu.”'),
       ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Có khi Gửi duyệt', 'Theo dữ liệu', '- Quy tắc như mục 2.5.'),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, png, jpg, jpeg ≤ 20 MB', 'Có khi Gửi duyệt', 'File đã lưu',
        ['- Thêm file mới như mục 2.5', '- Xóa file đã lưu: hỏi “Xác nhận xóa”, gỡ ngay']),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', '–', 'Dòng đã lưu', '- Không nạp lại, không sửa.'),
       ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Lưu, giữ Đang tạo.'),
       ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Xem mục 2.7.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Lưu thành công.”', '- ' + CONFLICT, '- “Xóa file thành công” / “Xóa file thất bại”']),
   ],
   ev=[
       ('Mở màn Sửa', 'System',
        'Before:\n– Phiếu trong phạm vi xem; ngoài phạm vi → trang “không tìm thấy”.\n'
        'During:\n– Phiếu không Đang tạo hoặc không phải người tạo → chuyển về màn chi tiết.\n'
        'After:\n– Hiển thị form, chỉ Ghi chú và File nhập được.'),
       ('Bấm Lưu nháp', 'Click',
        'Before:\n– Kiểm tra Đang tạo + người tạo; không đạt → ' + CONFLICT + ' và dừng xử lý.\n'
        'During:\n– Ghi chú > 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”; kiểm tồn kế toán → ' + ACC_ERR + '.\n' + ERR + '\n'
        'After:\n– Lưu Ghi chú, file mới; ghi lịch sử “Thay đổi thông tin” nếu có thay đổi; “Lưu thành công.”, về danh sách.'),
       ('Bấm xóa file đã lưu → Xóa', 'Click',
        'Before:\n– Hộp “Xác nhận xóa”; phiếu còn sửa được, không → ' + CONFLICT + '.\n'
        'After:\n– Gỡ file khỏi phiếu, ghi lịch sử, báo “Xóa file thành công”.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– So dữ liệu với lúc mở.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát: về danh sách; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Gửi duyệt phiếu (trừ tồn kho)',
   usecase=('FR-07', 'Gửi duyệt phiếu', 'action', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Gửi duyệt phiếu xuất kho điều chỉnh kiểm kê',
       mota='Từ màn Tạo mới hoặc Sửa, người lập bấm Gửi duyệt: hệ thống lưu phiếu ở trạng thái Chờ duyệt, TRỪ NGAY tồn kho thực tế '
            'của từng dòng theo đúng lô tại đúng vị trí, gửi thông báo cho Kế toán kho cùng công ty. Sau khi gửi phiếu không sửa '
            'được nữa.',
       tacnhan=TN_LAP,
       dieukien='1. Đang ở màn Tạo mới (đủ điều kiện mục 2.5) hoặc Sửa (phiếu Đang tạo của mình).\n'
                '2. Đã chọn Phiếu kiểm kê, có dòng hàng, đã nhập Ghi chú và có ít nhất 1 file đính kèm.',
       chinh='1. Người dùng bấm Gửi duyệt.\n'
             '2. Hệ thống kiểm tra đủ Phiếu kiểm kê, Kho, Ghi chú, File đính kèm.\n'
             '3. Hệ thống hiện hộp “Xác nhận gửi duyệt”: “Gửi duyệt sẽ xuất ngay hàng thiếu khỏi kho và không sửa được phiếu nữa. '
             'Bạn có chắc muốn gửi duyệt?”.\n'
             '4. Người dùng bấm Gửi duyệt trong hộp.\n'
             '5. Hệ thống kiểm tra như Lưu nháp (mục 2.5 / 2.6) và kiểm tồn kế toán.\n'
             '6. Hệ thống lưu phiếu trạng thái Chờ duyệt; với từng dòng kiểm đủ tồn kho, tồn vị trí, tồn lô rồi trừ tồn và ghi Thẻ '
             'kho (công ty theo lô).\n'
             '7. Hệ thống ghi lịch sử (Tạo mới khi gửi từ màn Thêm; “Thay đổi trạng thái” Đang tạo → Chờ duyệt khi gửi từ màn Sửa).\n'
             '8. Hệ thống gửi thông báo “[XKĐCKK] Chờ duyệt: <mã>. Người gửi: <tên>. Kho: <kho>” tới người có quyền Kế toán kho '
             'cùng công ty người gửi, báo “Gửi duyệt thành công.” và về danh sách.',
       phu='• Thiếu Ghi chú / File → viền đỏ, %s dưới ô / dưới khối file, “Bạn chưa nhập đầy đủ thông tin.”; không hiện hộp xác nhận.\n'
           '• Bấm Hủy trong hộp → đóng hộp, không lưu, form giữ nguyên.\n'
           '• Thiếu tồn ở bất kỳ dòng nào → %s; không lưu, không trừ dòng nào.\n'
           '• Tồn kế toán không đủ → %s.\n'
           '• Phiếu đã đổi trạng thái (gửi từ màn Sửa) → %s.' % (REQ, PHY_ERR, ACC_ERR, CONFLICT),
       dacbiet='Gửi duyệt KHÔNG hoàn tác được trên màn. Toàn bộ lưu + trừ tồn trong một lần lưu trọn gói. Thông báo chỉ gửi tới Kế '
               'toán kho cùng công ty người gửi; Kế toán kho thấy mọi phiếu Chờ duyệt trong danh sách.'),
   layout=dict(menu=MENU + ' => Tạo mới => Gửi duyệt', shot=shot('12b_confirm_send'),
               shot_caption='Hộp Xác nhận gửi duyệt (mở từ màn Sửa — ảnh giả trạng thái Đang tạo)'),
   extra=[(shot('10d_validate_send'), 'Gửi duyệt khi thiếu Ghi chú và File đính kèm')],
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Gửi duyệt (chân màn)', 'Button', 'Enable / Disable', 'Hiển thị',
        ['- Rê chuột: “Gửi duyệt: xuất ngay hàng thiếu khỏi kho và báo Kế toán kho”', '- Khóa trong lúc lưu']),
       ('Hộp “Xác nhận gửi duyệt”', 'Popup', 'Hiển thị', 'Ẩn',
        '- “Gửi duyệt sẽ xuất ngay hàng thiếu khỏi kho và không sửa được phiếu nữa. Bạn có chắc muốn gửi duyệt?”'),
       ('Nút Gửi duyệt (trong hộp)', 'Button', 'Enable', 'Hiển thị', '- Thực hiện lưu + trừ tồn.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống Hủy.'),
       ('Lỗi tại ô', 'Label', 'Hiển thị', 'Ẩn', ['- Ghi chú: “Bắt buộc phải nhập”', '- Khối File đính kèm: “Bắt buộc phải nhập”']),
       ('Lỗi tồn dưới bảng Chi tiết', 'Label', 'Hiển thị', 'Ẩn', ['- Tồn kho thực tế: ' + PHY_ERR, '- Tồn kế toán: ' + ACC_ERR]),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Gửi duyệt thành công.”', '- Thiếu dữ liệu: “Bạn chưa nhập đầy đủ thông tin.”']),
       ('Trạng thái sau gửi', 'Badge', 'Read-only', 'Chờ duyệt', '- Nhãn vàng “Chờ duyệt”; nút Sửa biến mất.'),
       ('Thông báo chuông tới Kế toán kho', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        '- “[XKĐCKK] Chờ duyệt: <mã>. Người gửi: <tên>. Kho: <tên kho>”; bấm → mở chi tiết phiếu.'),
   ],
   ev=[
       ('Bấm Gửi duyệt (chân màn)', 'Click',
        'Before:\n– Không có lượt lưu đang chạy.\n'
        'During:\n– Thiếu Phiếu kiểm kê / Kho / Ghi chú / File → ' + REQ + ', “Bạn chưa nhập đầy đủ thông tin.”.\n'
        'After:\n– Hiện hộp “Xác nhận gửi duyệt”.'),
       ('Bấm Gửi duyệt trong hộp', 'Click',
        'Before:\n– Kiểm điều kiện lập phiếu (Thêm) hoặc Đang tạo + người tạo (Sửa); không đạt → thông báo, dừng xử lý.\n'
        'During:\n– Kiểm Ghi chú, file, tồn kế toán.\n– Mỗi dòng: kiểm đủ tồn kho / vị trí / lô; thiếu → ' + PHY_ERR + '.\n' + ERR + '\n'
        'After:\n– Phiếu → Chờ duyệt; trừ tồn đúng lô / vị trí, ghi Thẻ kho.\n'
        '– Ghi một dòng lịch sử (Tạo mới hoặc Thay đổi trạng thái).\n'
        '– Gửi thông báo Kế toán kho cùng công ty; “Gửi duyệt thành công.”, về danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nAfter:\n– Đóng hộp; form giữ nguyên, không lưu.'),
       ('Bấm thông báo chuông', 'Click', 'Before:\n– Kế toán kho nhận thông báo.\nAfter:\n– Mở màn chi tiết phiếu.'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'Tạo phiếu xuất hàng (Kế toán kho)',
   usecase=('FR-08', 'Tạo phiếu xuất hàng', 'action', A_KTK),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo phiếu xuất hàng điều chỉnh kiểm kê từ phiếu Chờ duyệt',
       mota='Bước hạch toán của Kế toán kho: từ phiếu Chờ duyệt bấm Tạo phiếu xuất hàng → mở màn Tạo phiếu xuất hàng điều chỉnh kiểm '
            'kê (phân hệ Tài chính) chọn sẵn phiếu này. Lưu phiếu xuất hàng thì phiếu xuất kho điều chỉnh chuyển Đang hạch toán; '
            'Lưu và duyệt thì chuyển Đã hạch toán; cả hai ghi Người duyệt / Ngày duyệt. Form phiếu xuất hàng đặc tả ở SRS của màn đó.',
       tacnhan=TN_KTK,
       dieukien='1. Người dùng có quyền Kế toán kho.\n2. Phiếu đang Chờ duyệt.',
       chinh='1. Kế toán kho bấm Tạo phiếu xuất hàng ở cột Hành động hoặc chân màn chi tiết.\n'
             '2. Hệ thống mở màn “Tạo phiếu xuất hàng điều chỉnh kiểm kê” chọn sẵn phiếu xuất kho này.\n'
             '3. Kế toán kho nhập thông tin hạch toán rồi bấm Lưu hoặc Lưu và duyệt.\n'
             '4. Hệ thống ghi phiếu xuất hàng; phiếu xuất kho điều chỉnh → Đang hạch toán (Lưu) hoặc Đã hạch toán (Lưu và duyệt); '
             'ghi Người duyệt = Kế toán kho, Ngày duyệt = lúc lưu.\n'
             '5. Hệ thống ghi mốc “Thay đổi trạng thái” trên phiếu xuất kho điều chỉnh kèm ghi chú “Phiếu xuất hàng điều chỉnh kiểm '
             'kê <mã PXHĐCKK>.”; phiếu kiểm kê → Hoàn thành nếu đã xử lý hết, còn lại Đang xử lý.',
       phu='• Không phải Kế toán kho / phiếu không còn Chờ duyệt → không có nút.\n'
           '• Bấm Quay lại ở màn phiếu xuất hàng khi đã nhập → hộp “Thông tin chưa lưu”; phiếu xuất kho vẫn Chờ duyệt.\n'
           '• Lưu phiếu xuất hàng lỗi → báo lỗi tại màn đó; trạng thái phiếu xuất kho không đổi.',
       dacbiet='Nút trước đây mở hệ thống cũ, nay mở màn HRM Phiếu xuất hàng điều chỉnh kiểm kê. Sau Đang hạch toán, sửa / duyệt phiếu '
               'xuất hàng tiếp tục ở màn đó (Lưu và duyệt → Đã hạch toán).'),
   layout=dict(entries=[
       (MENU + ' => Tạo phiếu xuất hàng', 'Từ cột Hành động của dòng phiếu Chờ duyệt (chỉ Kế toán kho thấy nút).'),
       (MENU + ' => Xem chi tiết => Tạo phiếu xuất hàng', 'Hoặc từ chân màn chi tiết phiếu.')],
       shot=shot('17b_detail_px'), shot_caption='Chi tiết phiếu Chờ duyệt có nút Tạo phiếu xuất hàng'),
   extra=[(shot('23_product_export'), 'Màn Tạo phiếu xuất hàng điều chỉnh kiểm kê mở từ phiếu')],
   ui=[
       ('Nút Tạo phiếu xuất hàng (dòng)', 'Icon Button', 'Enable', '–', '–', 'Theo điều kiện',
        ['- Rê chuột: “Tạo phiếu xuất hàng”', '- Chờ duyệt + Kế toán kho']),
       ('Nút Tạo phiếu xuất hàng (màn chi tiết)', 'Button', 'Enable', '–', '–', 'Theo điều kiện',
        '- Nút chính đầu dãy; rê chuột: “Lập phiếu xuất hàng điều chỉnh kiểm kê”.'),
       ('Màn Tạo phiếu xuất hàng điều chỉnh kiểm kê', 'Label', 'Hiển thị', '–', '–', 'Phiếu xuất kho chọn sẵn',
        '- Nút Lưu, Lưu và tiếp tục, Lưu và duyệt, Quay lại (đặc tả ở SRS màn đó).'),
       ('Cột / ô Người duyệt', 'Text', 'Read-only', '–', '–', 'Kế toán kho', '- Ghi khi lưu phiếu xuất hàng.'),
       ('Cột / ô Ngày duyệt', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', '–', 'Lúc lưu', '- Ghi khi lưu phiếu xuất hàng.'),
       ('Trạng thái sau hạch toán', 'Badge', 'Read-only', 'Danh sách 2 giá trị', '–', 'Theo thao tác',
        ['- Lưu → Đang hạch toán (xanh dương)', '- Lưu và duyệt → Đã hạch toán (xanh lá)']),
       ('Mốc lịch sử', 'Label', 'Read-only', '–', '–', 'Theo thao tác',
        '- “Thay đổi trạng thái” kèm ghi chú “Phiếu xuất hàng điều chỉnh kiểm kê <mã>.”.'),
   ],
   ev=[
       ('Bấm Tạo phiếu xuất hàng', 'Click',
        'Before:\n– Phiếu Chờ duyệt + Kế toán kho (nút chỉ hiện khi đạt).\n'
        'After:\n– Mở màn Tạo phiếu xuất hàng điều chỉnh kiểm kê chọn sẵn phiếu.'),
       ('Lưu phiếu xuất hàng (Lưu)', 'Click',
        'Before:\n– Kiểm tra theo màn Phiếu xuất hàng.\nDuring:\n' + ERR + '\n'
        'After:\n– Phiếu xuất kho → Đang hạch toán; ghi Người duyệt / Ngày duyệt; ghi lịch sử “Thay đổi trạng thái”.'),
       ('Lưu phiếu xuất hàng (Lưu và duyệt)', 'Click',
        'Before:\n– Kiểm tra theo màn Phiếu xuất hàng.\nDuring:\n– Trừ tồn kế toán.\n' + ERR + '\n'
        'After:\n– Phiếu xuất kho → Đã hạch toán; ghi Người duyệt / Ngày duyệt, lịch sử; phiếu kiểm kê → Hoàn thành / Đang xử lý.'),
       ('Bấm Quay lại ở màn phiếu xuất hàng', 'Click',
        'Before:\n– So dữ liệu.\nAfter:\n– Có thay đổi → hỏi “Thông tin chưa lưu”; phiếu xuất kho không đổi.'),
   ])

# ------------------------------------------------------------ 2.9
fr(9, 'Xem chi tiết phiếu', usecase=('FR-09', 'Xem chi tiết phiếu', 'view', A_XEM),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu xuất kho điều chỉnh kiểm kê',
       mota='Màn chỉ đọc hiển thị Thông tin chung (Phiếu kiểm kê, Kho, Ghi chú, Người duyệt / Ngày duyệt khi có), File đính kèm, bảng '
            'Chi tiết và khối Lịch sử. Trạng thái phiếu hiện ngay trên tiêu đề trang. Chân màn có Tạo phiếu xuất hàng, Sửa, In theo '
            'điều kiện và Quay lại.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu tồn tại và nằm trong phạm vi xem.',
       chinh='1. Người dùng bấm Số phiếu ở danh sách (hoặc số chứng từ ở Thẻ kho, thông báo chuông).\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết phiếu xuất kho điều chỉnh kiểm kê: <mã>” kèm nhãn trạng thái.\n'
             '4. Hệ thống hiển thị các khối và khối Lịch sử (thu gọn).',
       phu='• Phiếu ngoài phạm vi / không tồn tại → chuyển sang trang “không tìm thấy” (404), không báo lỗi nổi.\n'
           '• Máy chủ lỗi → “Không tải được dữ liệu.”.\n'
           '• Phiếu không có file → khối File đính kèm ẩn.\n'
           '• Bấm mã phiếu kiểm kê → mở ở tab mới; bấm Quay lại → về danh sách, khôi phục bộ lọc (10 phút).',
       dacbiet='Các ô vẫn giữ dấu * như form nhưng khóa. Người duyệt / Ngày duyệt chỉ hiện khi đã có. Số hiển thị dạng 1,234.5.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết phiếu xuất kho điều chỉnh kiểm kê'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        '- “Chi tiết phiếu xuất kho điều chỉnh kiểm kê: <mã>” kèm nhãn trạng thái màu (xám / vàng / xanh dương / xanh lá).'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu kiểm kê', 'Link', 'Read-only', '–', 'Theo dữ liệu', '- Bấm → mở chi tiết phiếu kiểm kê ở tab mới.'),
       ('Kho', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- “Mã kho - Tên kho”.'),
       ('Ghi chú', 'Textarea', 'Disable', '0–255 ký tự', 'Theo dữ liệu', '- Chỉ đọc.'),
       ('Người duyệt / Ngày duyệt', 'Textbox', 'Disable', 'dd/mm/yyyy hh:mm', 'Ẩn khi trống', '- Kế toán kho và thời điểm lưu phiếu xuất hàng.'),
       ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Ẩn khi không có file', '- Xem trước, tải về từng file.'),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        '- STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí, Lô, SL xuất, Đơn giá bán, Thành tiền bán; rỗng: “Không có dữ liệu”.'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút Xem lịch sử mở rộng; nội dung như mục 2.13.'),
       ('Nút Tạo phiếu xuất hàng', 'Button', 'Enable', '–', 'Theo điều kiện', '- Mục 2.8.'),
       ('Nút Sửa', 'Button', 'Enable', '–', 'Theo điều kiện', '- Mục 2.6.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Mục 2.10.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về danh sách.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem; không đạt → trang “không tìm thấy”, dừng xử lý.\n'
        'During:\n– Lấy dữ liệu phiếu, file, dòng hàng, cờ nút; lỗi khác → “Không tải được dữ liệu.”.\n'
        'After:\n– Hiển thị màn chỉ đọc, trạng thái trên tiêu đề.'),
       ('Bấm Xem lịch sử', 'Click', 'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở rộng khối, nạp các mốc lịch sử.'),
       ('Bấm mã Phiếu kiểm kê', 'Click', 'Before:\n– Có phiếu kiểm kê.\nAfter:\n– Mở chi tiết phiếu kiểm kê ở tab mới.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Không có dữ liệu cần lưu.\nAfter:\n– Về danh sách, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.10
fr(10, 'In phiếu', usecase=('FR-10', 'In phiếu', 'io', A_XEM),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu xuất kho điều chỉnh kiểm kê',
       mota='Xem trước và in một phiếu theo mẫu in “PHIẾU XUẤT KHO ĐIỀU CHỈNH KIỂM KÊ”, có chỗ ký Người lập. Bản in mở trong cửa sổ '
            'ngay trên màn đang đứng (danh sách hoặc chi tiết), không mở tab mới nên không mất bộ lọc.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm In ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ “Xem trước phiếu xuất kho điều chỉnh kiểm kê <mã>”, hiện “Đang tải dữ liệu in…” trong lúc dựng.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Phiếu ngoài phạm vi → cửa sổ báo %s.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in phiếu xuất kho điều chỉnh kiểm kê.”; lỗi khác → “Không tải được dữ liệu in”.\n'
           '• Bấm (x) → đóng cửa sổ, màn giữ nguyên.' % NOTFOUND,
       dacbiet='Logo / letterhead đầu bản in lấy theo công ty ghi trên phiếu (công ty người lập phiếu kiểm kê), không theo người đang '
               'xem. Bản in KHÔNG có cột Đơn giá / Thành tiền. Ngày ký (Ngày … Tháng … Năm …) là ngày in.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu xuất kho điều chỉnh kiểm kê',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Xem trước phiếu xuất kho điều chỉnh kiểm kê <mã phiếu>”.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → hộp thoại in của trình duyệt.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ xem trước.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Đang tải dữ liệu in…”.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead công ty của phiếu', '- “PHIẾU XUẤT KHO ĐIỀU CHỈNH KIỂM KÊ”']),
       ('Thông tin phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Số phiếu, Ngày lập, Phiếu kiểm kê, Kho, Ghi chú.'),
       ('Bảng hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- STT, Tên hàng, Model, Mã hàng, ĐVT, Vị trí, Lô, SL xuất.'),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- “Ngày … Tháng … Năm …”, Người lập + họ tên người tạo phiếu.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', ['- ' + NOTFOUND, '- “Không tải được dữ liệu in”']),
   ],
   ev=[
       ('Bấm In (dòng / màn chi tiết)', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → ' + NOTFOUND + '.\n'
        'During:\n– Dựng bản in theo dữ liệu hiện tại; lỗi → “Không tải được dữ liệu in”.\n'
        'After:\n– Hiển thị bản xem trước, letterhead theo công ty của phiếu.'),
       ('Bấm In trong cửa sổ xem trước', 'Click', 'Before:\n– Bản in đã dựng xong.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, giữ nguyên màn đang đứng.'),
       ('Đang dựng bản in', 'System', 'Before:\n– Vừa bấm In.\nAfter:\n– Hiện “Đang tải dữ liệu in…” tới khi có bản in.'),
   ])

# ------------------------------------------------------------ 2.11
fr(11, 'In danh sách', usecase=('FR-11', 'In danh sách', 'io', A_XEM),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In danh sách phiếu theo bộ lọc',
       mota='Xem trước và in danh sách các phiếu khớp bộ lọc đang áp trong phạm vi xem (không phân trang), mẫu “DANH SÁCH PHIẾU XUẤT '
            'KHO ĐIỀU CHỈNH KIỂM KÊ”, có chỗ ký Người lập. Tối đa 2.000 dòng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng lọc danh sách (mục 2.2) rồi bấm In danh sách.\n'
             '2. Hệ thống lấy các phiếu theo bộ lọc trong phạm vi xem, dựng bản in.\n'
             '3. Hệ thống mở cửa sổ “Xem trước danh sách phiếu xuất kho điều chỉnh kiểm kê”.\n'
             '4. Người dùng bấm In.',
       phu='• Trên 2.000 dòng → không dựng bản in, ẩn nút In, hiện “Danh sách có N dòng, vượt mức in tối đa 2.000 dòng nên chưa in '
           'được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.”.\n'
           '• Không có dòng → “Không có dữ liệu để in”.\n'
           '• Lỗi → “Không tải được dữ liệu in”.',
       dacbiet='Letterhead theo công ty của NGƯỜI IN (danh sách gồm nhiều phiếu). Cột: STT, Số phiếu, Phiếu kiểm kê, Kho, Người tạo, '
               'Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái.'),
   layout=dict(menu=MENU + ' => In danh sách', shot=shot('19_printlist'), shot_caption='Cửa sổ Xem trước danh sách',
               note='Modal Xem trước được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Xem trước danh sách phiếu xuất kho điều chỉnh kiểm kê”.'),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', '- Ẩn khi vượt 2.000 dòng.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Letterhead công ty người in, “DANH SÁCH PHIẾU XUẤT KHO ĐIỀU CHỈNH KIỂM KÊ”.'),
       ('Bảng danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        '- STT, Số phiếu, Phiếu kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái.'),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- Ngày in, Người lập + họ tên người in.'),
       ('Dòng nhắc vượt trần', 'Label', 'Hiển thị', '–', 'Ẩn', '- Câu “Danh sách có N dòng, vượt mức in tối đa 2.000 dòng…”.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', ['- “Không có dữ liệu để in”', '- “Không tải được dữ liệu in”']),
   ],
   ev=[
       ('Bấm In danh sách', 'Click',
        'Before:\n– Áp phạm vi xem + bộ lọc đang có.\n'
        'During:\n– Đếm tổng; > 2.000 → dòng nhắc vượt trần; 0 → “Không có dữ liệu để in”.\n'
        'After:\n– Hiển thị bản xem trước danh sách.'),
       ('Bấm In', 'Click', 'Before:\n– Bản in đã dựng.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi.\nAfter:\n– Đóng cửa sổ, danh sách giữ nguyên.'),
       ('Lỗi khi dựng', 'System', 'Before:\n– Máy chủ lỗi.\nAfter:\n– “Không tải được dữ liệu in”.'),
   ])

# ------------------------------------------------------------ 2.12
fr(12, 'Xuất danh sách ra Excel', usecase=('FR-12', 'Xuất Excel', 'io', A_XEM),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất toàn bộ phiếu khớp bộ lọc trong phạm vi xem (không phân trang) ra file Excel. Cột STT '
            'luôn đứng đầu; đầu file có letterhead công ty người xuất và tiêu đề, cuối file có khối ký Người lập.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 9 trường, tích sẵn các trường ứng với cột đang hiện.\n'
             '3. Người dùng tích trường, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy lần lượt toàn bộ phiếu, hiện tiến độ “Đã tải x/y dòng…”, dựng file theo thứ tự trường đã chọn.\n'
             '5. Hệ thống tải file “danh_sach_phieu_xuat_kho_dieu_chinh_kiem_ke.xlsx”, báo “Xuất Excel thành công”.',
       phu='• Không có phiếu khớp → không tạo file, báo “Không có dữ liệu để xuất”.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng (lấy theo từng đợt). Tiêu đề file “DANH SÁCH PHIẾU XUẤT KHO ĐIỀU CHỈNH KIỂM KÊ”, trang tính '
               '“Xuat dieu chinh kiem ke”.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 9 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        '- Số phiếu, Phiếu kiểm kê, Ngày kiểm kê, Kho, Người tạo, Ngày tạo, Người duyệt, Ngày duyệt, Trạng thái.'),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/9 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file Excel', '- Khóa khi chưa tích trường nào hoặc đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('Nội dung file Excel', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Letterhead công ty người xuất, tiêu đề “DANH SÁCH PHIẾU XUẤT KHO ĐIỀU CHỈNH KIỂM KÊ”',
         '- Dòng tên cột: STT + các trường đã chọn', '- Khối ký cuối file: “Người lập”']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Xuất Excel thành công”', '- “Không có dữ liệu để xuất”', '- “Lỗi khi xuất Excel”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không có lượt xuất đang chạy.\nAfter:\n– Mở cửa sổ, tích sẵn trường ứng với cột đang hiện.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Kéo bằng biểu tượng của trường.\nAfter:\n– Đổi thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất; dữ liệu theo phạm vi xem.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc theo từng đợt, hiện tiến độ.\n– Không có dòng → “Không có dữ liệu để xuất”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.\n' + ERR + '\n'
        'After:\n– Tải file, báo “Xuất Excel thành công”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.13
fr(13, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu',
       mota='Xem các mốc thao tác của phiếu: người thực hiện, thời điểm, hành động, giá trị cũ → mới. Phiếu có các loại mốc: “Tạo mới”, '
            '“Thay đổi thông tin” (Ghi chú, File đính kèm) và “Thay đổi trạng thái” (Đang tạo → Chờ duyệt khi gửi từ màn Sửa; Chờ '
            'duyệt → Đang hạch toán → Đã hạch toán khi Kế toán kho lập phiếu xuất hàng, kèm mã phiếu xuất hàng). Cửa sổ ở danh sách '
            'và khối Lịch sử ở màn chi tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động, hoặc Xem lịch sử ở khối Lịch sử màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem, mở cửa sổ “Lịch sử thay đổi: <mã phiếu>” và nạp các mốc.\n'
             '3. Hệ thống hiển thị các mốc, mới nhất ở trên.',
       phu='• Phiếu lập ở hệ thống cũ chưa có mốc → hiện trạng thái chưa có lịch sử.\n'
           '• Bấm Bộ lọc → mở các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Xem, in, xuất Excel không ghi mốc. Lưu nháp không đổi gì thì không ghi mốc. Mốc chuyển trạng thái của PHIẾU KIỂM KÊ '
               'nguồn ghi ở lịch sử phiếu kiểm kê, không lặp ở đây.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('16c_history_filter'), 'Khối Bộ lọc trong cửa sổ Lịch sử thay đổi'),
          (shot('17c_detail_history'), 'Khối Lịch sử ở màn chi tiết phiếu')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <mã phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái: “Trạng thái: <cũ> → <mới>”, ghi chú “Phiếu xuất hàng điều chỉnh kiểm kê <mã>.”',
           '- Thay đổi thông tin: giá trị cũ → mới của Ghi chú; File đính kèm dạng bảng từng file', '- Mới nhất ở trên']),
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
        'Before:\n– Kiểm tra phạm vi xem phiếu (như màn chi tiết).\nDuring:\n– Nạp các mốc.\nAfter:\n– Hiển thị các mốc, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change', 'Before:\n– Không có nút Tìm kiếm: chọn là lọc.\nAfter:\n– Lọc lại danh sách mốc.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Khối lọc đang mở.\nAfter:\n– Xóa điều kiện lọc, hiện lại đủ các mốc.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; danh sách giữ nguyên trang và bộ lọc.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu xuất kho điều chỉnh kiểm kê; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi xem', [
        '– Q1 / Super admin: mọi phiếu; Q2: phiếu có công ty = công ty đang làm việc; không có cả hai: phiếu mình tạo.',
        '– Luôn ẩn phiếu Đang tạo của người khác; Kế toán kho thấy thêm mọi phiếu Chờ duyệt (mọi công ty).',
        '– Chi tiết / Sửa / In / Lịch sử áp cùng phạm vi; ngoài phạm vi → trang 404. Menu không gắn quyền.'],
     ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel', 'Lịch sử']),
    ('BR-02', 'Điều kiện lập phiếu', [
        '– Phiếu kiểm kê Chờ xử lý / Đang xử lý + người lập có quyền “%s” + còn hàng có tổng chênh ≠ 0 và dòng thiếu chưa xử lý + '
        'chưa có phiếu xuất kho điều chỉnh nào.' % Q4,
        '– Mỗi phiếu kiểm kê chỉ 1 phiếu xuất kho điều chỉnh (kể cả khi phiếu kiểm kê có nhiều kho); 2 người lập cùng lúc thì người '
        'sau bị chặn.'], ['Tạo mới']),
    ('BR-03', 'Dòng hàng xuất', [
        '– Dòng kết quả kiểm kê THIẾU, chưa xử lý, tại kho đã chọn; SL xuất = |chênh lệch| − đã xử lý (bỏ dòng ≤ 0); lô và vị trí '
        'theo dòng kết quả.',
        '– Đơn giá bán = giá bán lẻ của hàng theo công ty phiếu kiểm kê; Thành tiền bán = SL xuất × Đơn giá bán.',
        '– Người dùng không sửa được; máy chủ lấy lại dòng khi lưu, tên / mã / model / ĐVT lấy theo danh mục lúc lưu.'],
     ['Tạo mới', 'Xem chi tiết']),
    ('BR-04', 'Bắt buộc theo nút lưu', [
        '– Lưu nháp / Lưu và tiếp tục: chỉ bắt Phiếu kiểm kê + Kho.',
        '– Gửi duyệt: bắt thêm Ghi chú và ít nhất 1 file đính kèm (pdf, png, jpg, jpeg ≤ 20 MB).',
        '– Ghi chú tối đa 255 ký tự.'], ['Tạo mới', 'Chỉnh sửa', 'Gửi duyệt']),
    ('BR-05', 'Kiểm tồn kế toán', [
        '– Mỗi lần lưu (tạo / sửa / gửi): gom SL xuất quy về ĐVT cơ sở theo hàng + công ty của lô, so với tồn kế toán của kho kế '
        'toán ứng với kho vật lý và công ty đó (đã trừ giữ chỗ / giữ hàng).',
        '– Không có kho kế toán tương ứng thì bỏ qua; thiếu → không lưu, báo theo mã hàng.'], ['Tạo mới', 'Chỉnh sửa', 'Gửi duyệt']),
    ('BR-06', 'Trừ tồn khi Gửi duyệt', [
        '– Gửi duyệt (từ Thêm hoặc Sửa) trừ ngay tồn kho, tồn vị trí, tồn lô của từng dòng; ghi Thẻ kho theo công ty của lô.',
        '– Kiểm đủ tồn trước khi trừ; thiếu ở một dòng → không lưu, không trừ dòng nào.',
        '– Lưu nháp không trừ tồn.'], ['Gửi duyệt']),
    ('BR-07', 'Vòng đời phiếu', [
        '– Đang tạo (xám) → Gửi duyệt → Chờ duyệt (vàng) → Kế toán kho lưu phiếu xuất hàng → Đang hạch toán (xanh dương) → lưu và '
        'duyệt → Đã hạch toán (xanh lá).',
        '– Không có Xóa / Khóa / Hủy / Không duyệt; điều kiện xóa: không áp dụng.',
        '– Lập phiếu → phiếu kiểm kê Đang xử lý; hạch toán xong → phiếu kiểm kê Hoàn thành nếu đã xử lý hết.'],
     ['Tạo mới', 'Gửi duyệt', 'Tạo phiếu xuất hàng']),
    ('BR-08', 'Điều kiện sửa', [
        '– Chỉ phiếu Đang tạo và đúng người tạo; Super admin không sửa thay.',
        '– Chỉ sửa Ghi chú và File đính kèm; Phiếu kiểm kê / Kho / dòng hàng giữ nguyên.',
        '– Trạng thái đổi giữa chừng → chặn lưu, báo tải lại trang.'], ['Chỉnh sửa']),
    ('BR-09', 'Mã phiếu và đơn vị sở hữu', [
        '– Mã PXKĐCKK-NNNNN tự sinh theo thứ tự (giữ dãy mã của hệ thống cũ), không nhập / sửa được.',
        '– Công ty / phòng ban của phiếu = của người lập phiếu kiểm kê nguồn (dùng cho phạm vi Q2, letterhead bản in).'],
     ['Tạo mới', 'Xem danh sách', 'In']),
    ('BR-10', 'Thông báo', [
        '– Gửi duyệt → thông báo “[XKĐCKK] Chờ duyệt: <mã>. Người gửi: <tên>. Kho: <kho>” tới người có quyền Kế toán kho cùng '
        'công ty người gửi; bấm mở chi tiết phiếu.',
        '– Lỗi gửi thông báo không làm hỏng lần lưu.'], ['Gửi duyệt']),
    ('BR-11', 'In và xuất', [
        '– In phiếu: letterhead theo công ty của phiếu. In danh sách / Xuất Excel: letterhead theo công ty người thao tác.',
        '– In danh sách tối đa 2.000 dòng; Xuất Excel không giới hạn; cả hai theo phạm vi xem + bộ lọc.'],
     ['In phiếu', 'In danh sách', 'Xuất Excel']),
    ('BR-12', 'Quy tắc ghi lịch sử', [
        '– Tạo phiếu → “Tạo mới”; sửa Ghi chú / file → “Thay đổi thông tin” (cũ → mới); gửi từ màn Sửa → “Thay đổi trạng thái”.',
        '– Kế toán kho lưu phiếu xuất hàng → “Thay đổi trạng thái” kèm mã phiếu xuất hàng.',
        '– Xem, in, xuất Excel, lưu không đổi gì: không ghi; hiển thị mới nhất ở trên.'],
     ['Tạo mới', 'Chỉnh sửa', 'Gửi duyệt', 'Tạo phiếu xuất hàng', 'Lịch sử']),
    ('BR-13', 'Sử dụng ở màn khác', [
        '– Thẻ kho hiện dòng xuất PXKĐCKK-… liên kết sang chi tiết phiếu; báo cáo tồn giảm, Tổng hợp xuất nhập tồn tăng số xuất.',
        '– Vị trí và kho vật lý đã có trên phiếu không xóa được ở danh mục.',
        '– Dữ liệu dùng chung với hệ thống cũ: phiếu lập ở hệ thống cũ cũng hiện trên màn này.'],
     ['Gửi duyệt', 'Xem danh sách']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Phiếu xuất kho điều chỉnh kiểm kê (phiếu, trạng thái, dòng hàng, số '
    'lượng xuất theo từng vị trí / lô).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Kiểm kê theo hàng hóa (nút Tạo phiếu xuất kho điều chuyển mở form chọn sẵn phiếu; phiếu kiểm kê chuyển Đang xử lý '
                 'khi lập phiếu, Hoàn thành khi xử lý hết; đã có phiếu xuất điều chỉnh thì không lập lại)', 'Kho -> Kiểm kho -> Theo vị trí'),
    ('2', 'Tài chính', 'Phiếu xuất hàng điều chỉnh kiểm kê (Kế toán kho lập từ phiếu Chờ duyệt; ghi ngược trạng thái Đang hạch toán / '
                       'Đã hạch toán, Người duyệt, Ngày duyệt)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('3', 'Kho', 'Thẻ kho (dòng xuất theo lô của phiếu Chờ duyệt trở đi, số chứng từ PXKĐCKK-… liên kết sang chi tiết phiếu)',
     'Kho -> Báo cáo kho'),
    ('4', 'Kho', 'Tổng hợp xuất nhập tồn (số xuất trong kỳ tăng theo phiếu)', 'Kho -> Báo cáo kho'),
    ('5', 'Kho', 'Báo cáo tồn kho chi tiết theo mặt hàng (tồn theo lô giảm)', 'Kho -> Báo cáo kho'),
    ('6', 'Kho', 'Báo cáo tồn kho tổng hợp theo mặt hàng (tồn giảm)', 'Kho -> Báo cáo kho'),
    ('7', 'Kho', 'Báo cáo tồn kho theo vị trí (tồn tại vị trí giảm)', 'Kho -> Báo cáo kho'),
    ('8', 'Kho', 'Báo cáo tồn theo kho (tồn của kho giảm)', 'Kho -> Báo cáo kho'),
    ('9', 'Kho', 'Vị trí (không xóa được vị trí đã có trên phiếu)', 'Kho -> Danh mục'),
    ('10', 'Kho', 'Kho vật lý (không xóa được kho đã có phiếu)', 'Kho -> Danh mục'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
