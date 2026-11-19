# -*- coding: utf-8 -*-
"""SRS màn "Phiếu nhập hàng điều chỉnh kiểm kê" (phân hệ Tài chính) — form chuẩn SRS_MAU (09/11/2026).

Chạy: python gen_srs.py  -> "SRS - Phiếu nhập hàng điều chỉnh kiểm kê.docx" (SrsDoc.save() tự chạy srs_selfcheck).
Khuôn: ../phieu-xuat-kho-dieu-chinh-kiem-ke/gen_srs.py (09/11, phiếu ĐCKK) + ../phieu-dieu-chuyen-vi-tri/ (bộ mới nhất). Tên gọi
  thống nhất với ../kiem-ke-theo-hang-hoa/ (phiếu kiểm kê, hàng thừa, lô). Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột.
Nguồn đọc 09/11/2026 (nhánh develop cả 2 repo, con của gop_db):
  BE  Modules/Finance/{Entities/InventoryImport/InventoryImport.php (STATUSES, scopedQuery, canView, canEdit, generateCode),
      Http/Controllers/V1/InventoryImportController.php, Services/InventoryImport/InventoryImport{,Write}Service.php (validate,
      validateAccountingWarehouse, syncDetails, afterSave, updateWarehouse, saveAccounting, lịch sử), Services/AccountingStockWriter.php,
      Services/ProductImportPriceReader.php, Entities/WarehouseInventoryImport/WarehouseInventoryImport.php (canCreateProductImport,
      isAccountant), Entities/SelfInventory/SelfInventory.php (handleCompleted), Routes/api.php}, Entities/Concerns/
      ChecksEmployeePermission.php, PermissionsTableSeeder (nhóm "Phiếu nhập hàng điều chỉnh kiểm kê" — nhánh develop CHƯA có
      Catalog + mã quyền, tên quyền theo code), Assign/Services/StockValueFifoService.php (layer giá FIFO), MasterData Kho kế toán /
      Kho vật lý / Vị trí / ProductUsageGuard (chặn xóa), EmployeeDebt (sổ công nợ nhân viên đọc TK 3381).
  FE  pages/finance/inventory-imports/** (index, create, _id/index, _id/edit, components/{InventoryImportForm.vue, constants.js,
      row-actions.js}), pages/finance/bill-payment-requests/components/AttachmentSection.vue, pages/warehouse/inventory-imports/
      components/row-actions.js (nút Tạo phiếu nhập hàng), components/subsystem-menu/{finance.js, warehouse.js, lookup.js}.
  Bối cảnh: design.md, plan.md (#11966), spec docs/superpowers/specs/gop-db/2026-10-30-phieu-nhap-hang-dieu-chinh-kiem-ke-design.md.
Ảnh: ./pnhdckk_shots — dev-hrm 09/11/2026 (_capture/capture.js, DNS Admin = Super admin, chặn mọi yêu cầu ghi: 0 yêu cầu ghi).
  Dữ liệu dev đủ trạng thái (PNHĐCKK-00053 Đang tạo, PNHĐCKK-00052 Đã hạch toán, PNKĐCKK-00054 Chờ duyệt) — KHÔNG giả trạng thái.
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

TEN = 'Phiếu nhập hàng điều chỉnh kiểm kê'
SHOTS = os.path.join(HERE, 'pnhdckk_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Nhập hàng => Phiếu nhập hàng điều chỉnh kiểm kê'
MENU_WII = 'Phân hệ Kho => Nhập kho => Phiếu nhập kho điều chỉnh kiểm kê'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu nhập hàng điều chỉnh kiểm kê.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
Q1 = 'Xem phiếu nhập hàng điều chỉnh kiểm kê - theo tổng công ty'
Q2 = 'Xem phiếu nhập hàng điều chỉnh kiểm kê - theo công ty'
Q3 = 'Kế toán kho'
A_XEM = 'Người xem phiếu'
A_KTK = 'Kế toán kho'
TN = 'Người dùng có quyền thực hiện chức năng: %s / %s (không có quyền nào thì chỉ phiếu mình tạo).' % (Q1, Q2)
TN_KTK = ('Người dùng có quyền thực hiện chức năng: %s (lập phiếu); Sửa / Lưu và duyệt phiếu Đang tạo chỉ dành cho chính người '
          'tạo phiếu.' % Q3)
DK = ('1. Người dùng đăng nhập thành công.\n2. Phiếu nằm trong phạm vi xem của người dùng.\n'
      '3. Người dùng đang ở màn danh sách Phiếu nhập hàng điều chỉnh kiểm kê.')
REQ = '“Bắt buộc phải nhập”'
INCOMPLETE = '“Bạn chưa nhập đầy đủ thông tin.”'
MISMATCH = '“Số lượng nhập kho kế toán không khớp!”'
DUP_ACC = '“Kho kế toán đã được chọn!”'
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NOTFOUND = '“Không tìm thấy phiếu nhập hàng điều chỉnh kiểm kê hoặc bạn không có quyền xem.”'
SRC_ERR = '“Phiếu nhập kho không còn lập được phiếu nhập hàng điều chỉnh hoặc bạn không có quyền.”'
CF_TITLE = '“Xác nhận lưu và duyệt”'
CF_MSG = ('“Lưu và duyệt sẽ nhập tồn kho kế toán, hạch toán ngay và không sửa được phiếu nữa. Bạn có chắc muốn tiếp '
          'tục?”')

d = SrsDoc(out=OUT, menu=MENU, route='/finance/inventory-imports', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Hàng hoá - Dịch vụ - Vận chuyển': 'menu_nhom', 'Nhập hàng': 'menu_nhaphang',
    'Phiếu nhập hàng điều chỉnh kiểm kê': 'menu_muc',
    'Phân hệ Kho': 'menu_phanhe_kho', 'Nhập kho': 'menu_nhom_kho', 'Phiếu nhập kho điều chỉnh kiểm kê': 'menu_muc_kho',
    'Xem chi tiết phiếu nhập kho': 'link_pnk_row', 'Tạo phiếu nhập hàng': 'btn_taophieunhaphang',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Sửa': 'btn_sua_row', 'Lưu và duyệt': 'btn_luuduyet', 'Xem chi tiết': 'link_sophieu',
    'In': 'btn_in_row', 'In danh sách': 'btn_inds', 'Xuất Excel': 'btn_xuatexcel', 'Lịch sử': 'btn_lichsu_row',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu nhập hàng điều chỉnh kiểm kê (mã phiếu PNHĐCKK-NNNNN), phân hệ Tài '
    'chính, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ bước hạch toán hàng THỪA sau kiểm kê: phiếu kiểm kê theo hàng hóa có hàng đếm được nhiều hơn sổ sách → thủ kho lập '
    'Phiếu nhập kho điều chỉnh kiểm kê (phân hệ Kho) và gửi duyệt → Kế toán kho lập Phiếu nhập hàng điều chỉnh kiểm kê: điền đơn '
    'giá nhập, chọn Nhân viên chịu trách nhiệm, phân bổ từng dòng hàng vào kho kế toán → Lưu (Đang tạo) hoặc Lưu và duyệt (Đã '
    'hạch toán: cộng tồn kho kế toán và ghi bút toán Nợ 1561 / Có 3381).',
    'Làm rõ các dữ liệu bị ghi ngược sang Phiếu nhập kho điều chỉnh kiểm kê, phiếu kiểm kê nguồn, tồn kho kế toán, sổ công nợ '
    'nhân viên và giá vốn của các phiếu xuất sau này.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới (Lưu / Lưu và tiếp tục), Chỉnh '
    'sửa phiếu Đang tạo, Lưu và duyệt (hạch toán), Xem chi tiết, In phiếu, In danh sách, Xuất Excel danh sách, Xem lịch sử thay '
    'đổi. Màn KHÔNG có Xóa (giữ như hệ thống cũ), Khóa / Mở khóa, Gửi duyệt, Không duyệt, Hủy phiếu và Import Excel: phiếu chỉ '
    'có 2 trạng thái Đang tạo và Đã hạch toán, bước duyệt chính là nút Lưu và duyệt của người lập.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Đơn giá nhập × số lượng (quy đổi theo ĐVT) là giá trị hàng thừa đưa vào sổ: Nợ 1561 Giá mua hàng hóa (từng hàng), Có 3381 '
    'Tài sản thừa chờ giải quyết (tổng, theo Nhân viên được chọn).',
    'Mỗi dòng phân bổ kho kế toán là một lần nhập tồn kho kế toán (kèm giá trị) — là lớp giá nhập mà các phiếu xuất sau này dùng '
    'để tính giá vốn theo nhập trước xuất trước.',
    'Phiếu nhập kho điều chỉnh kiểm kê nguồn chuyển Đang hạch toán / Đã hạch toán; phiếu kiểm kê nguồn được cộng số đã xử lý và '
    'chuyển Hoàn thành khi xử lý hết.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Chỉ lập được từ Phiếu nhập kho điều chỉnh kiểm kê đang Chờ duyệt, bởi người có quyền “%s” (BR-02).' % Q3,
    'Mỗi dòng hàng có số lượng phải được phân bổ đủ vào 1 hoặc nhiều kho kế toán khác nhau: tổng số lượng các kho kế toán = SL '
    'nhập (BR-03).',
    'Lưu và duyệt cộng tồn kho kế toán + ghi bút toán ngay và không sửa được nữa (BR-05).',
    'Phạm vi xem theo 2 quyền xem; không có quyền thì chỉ phiếu mình tạo; phiếu Đang tạo của người khác luôn ẩn (BR-01).',
    'Giữ như hệ thống cũ (đã chốt): mỗi lần lưu — kể cả sửa phiếu Đang tạo — đều cộng thêm số đã xử lý vào phiếu kiểm kê; không '
    'chặn lập nhiều phiếu cho 1 phiếu nhập kho; lưu phiếu không kiểm quyền riêng ngoài đường vào (BR-10).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu nhập hàng điều chỉnh kiểm kê (phiếu)', 'Chứng từ PNHĐCKK-NNNNN của màn này: hạch toán phần hàng THỪA phát hiện khi '
                                                   'kiểm kê, do Kế toán kho lập từ một phiếu nhập kho điều chỉnh kiểm kê.'),
    ('Phiếu nhập kho điều chỉnh kiểm kê', 'Chứng từ PNKĐCKK-NNNNN (phân hệ Kho) do thủ kho lập để nhập hàng thừa vào kho vật lý; '
                                          'nguồn dữ liệu của phiếu này, phải ở trạng thái Chờ duyệt.'),
    ('Phiếu kiểm kê', 'Chứng từ <mã công ty>.KKK-NNNNN ở màn Kiểm kê theo hàng hóa; nguồn gốc của phiếu nhập kho điều chỉnh.'),
    ('Hàng thừa', 'Dòng kết quả kiểm kê có Thực kiểm lớn hơn số sổ sách (chênh lệch dương).'),
    ('Thủ kho', 'Người lập phiếu nhập kho điều chỉnh kiểm kê nguồn; công ty / phòng ban của phiếu lấy theo người này.'),
    ('Nhân viên', 'Trường đặc thù: nhân viên chịu trách nhiệm phần tài sản thừa — bút toán Có 3381 ghi theo nhân viên này.'),
    ('Kho kế toán', 'Kho sổ sách gắn với kho vật lý và công ty; mỗi dòng hàng phân bổ vào 1..n kho kế toán.'),
    ('SL nhập / Số lượng', 'SL nhập: số lượng hàng thừa của dòng (lấy từ phiếu nhập kho). Số lượng: phần SL nhập phân bổ vào 1 kho '
                           'kế toán.'),
    ('Đơn giá nhập / Thành tiền nhập', 'Đơn giá nhập: mặc định giá nhập gần nhất của hàng, sửa được. Thành tiền nhập = SL nhập × '
                                       'Đơn giá nhập.'),
    ('Trạng thái Đang tạo', 'Nhãn xám: phiếu đã lưu, chưa hạch toán, người tạo còn sửa được.'),
    ('Trạng thái Đã hạch toán', 'Nhãn xanh lá: đã Lưu và duyệt — tồn kho kế toán và bút toán đã ghi, không sửa được.'),
    ('Cấu trúc phân cấp', 'Phiếu kiểm kê > phiếu nhập kho điều chỉnh > phiếu nhập hàng điều chỉnh > dòng hàng (hàng, ĐVT, SL nhập, '
                          'đơn giá) > dòng phân bổ kho kế toán (kho kế toán, số lượng).'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn có 2 quyền XEM theo cấp (nhóm quyền “Phiếu nhập hàng điều chỉnh kiểm kê”, phân hệ Tài chính, tên giữ như hệ thống cũ) và '
    'dùng lại quyền có sẵn “Kế toán kho” để lập phiếu. Không có quyền Tạo / Sửa / Duyệt riêng. Super admin có đủ mọi quyền. Không '
    'gắn quyền ở menu: ai cũng mở được màn, dữ liệu do hệ thống giới hạn.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q3', Q3, 'Hiện nút Tạo mới; ô Phiếu nhập kho liệt kê các phiếu nhập kho điều chỉnh kiểm kê Chờ duyệt; có nút Tạo phiếu nhập '
               'hàng trên phiếu nhập kho Chờ duyệt (màn Phiếu nhập kho điều chỉnh kiểm kê).'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('Q1', Q1, 'Mọi phiếu của mọi công ty; khối lọc có ô Công ty và Phòng ban.'),
    ('Q2', Q2, 'Phiếu có công ty = công ty đang làm việc HOẶC do chính mình tạo; khối lọc có ô Phòng ban.'),
    ('—', 'Không có Q1 / Q2', 'Chỉ phiếu do chính mình tạo.'),
], widths=[0.8, 2.2, 3.0])
d.p('Áp chung: phiếu Đang tạo của người khác luôn bị ẩn. Công ty / phòng ban của phiếu lấy theo THỦ KHO (người lập phiếu nhập kho '
    'nguồn), không theo người lập phiếu nhập hàng.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ mọi phiếu', '✅ công ty + phiếu mình tạo', '✅ theo Q1/Q2', '✅ phiếu mình tạo'),
    ('FR-02 Tìm kiếm và lọc', '✅ (có ô Công ty, Phòng ban)', '✅ (có ô Phòng ban)', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo mới phiếu', '❌', '❌', '✅', '❌ (không có nút; mở thẳng màn thì ô Phiếu nhập kho rỗng)'),
    ('FR-06 Chỉnh sửa phiếu', 'Người tạo, Đang tạo', 'Người tạo, Đang tạo', 'Người tạo, Đang tạo', 'Người tạo, Đang tạo'),
    ('FR-07 Lưu và duyệt', 'Người tạo', 'Người tạo', '✅ (khi tạo)', 'Người tạo (phiếu Đang tạo)'),
    ('FR-08 Xem chi tiết', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ phiếu mình tạo'),
    ('FR-09 In phiếu', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ phiếu mình tạo'),
    ('FR-10 In danh sách', '✅ theo phạm vi', '✅ theo phạm vi', '✅ theo phạm vi', '✅ phiếu mình tạo'),
    ('FR-11 Xuất Excel', '✅ theo phạm vi', '✅ theo phạm vi', '✅ theo phạm vi', '✅ phiếu mình tạo'),
    ('FR-12 Xem lịch sử thay đổi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ phiếu mình tạo'),
    ('Xóa / Khóa – Mở khóa / Gửi duyệt / Không duyệt / Hủy / Import', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[2.0, 1.0, 1.0, 1.0, 1.0])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có Q1 / Q2: vẫn mở được màn, danh sách chỉ có phiếu do chính mình tạo; không có khối Công ty – Phòng ban.',
    'Không có Q3: không có nút Tạo mới; mở thẳng màn Tạo thì ô Phiếu nhập kho không có lựa chọn nào; mở màn Tạo kèm phiếu nhập kho '
    'qua đường link thì báo %s dưới ô.' % SRC_ERR,
    'Mở chi tiết / sửa phiếu ngoài phạm vi qua đường link: hệ thống chuyển sang trang “không tìm thấy” (404), không hiện dữ liệu.',
    'Không phải người tạo / phiếu đã Đã hạch toán: không có nút Sửa; mở thẳng màn Sửa thì hệ thống tự chuyển về màn chi tiết.',
    'Bị gỡ quyền giữa lúc thao tác: lần nạp dữ liệu tiếp theo hệ thống áp quyền mới (quyền kiểm lại ở từng lần gọi).',
    'Giữ như hệ thống cũ (đã chốt): lần lưu phiếu không kiểm lại quyền Kế toán kho — đường vào (nút Tạo mới, ô Phiếu nhập kho, nút '
    'Tạo phiếu nhập hàng) mới là chỗ giới hạn.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới', 'Có quyền Q3 (hoặc Super admin)', 'Ẩn khi không có quyền'),
    ('Nút Xuất Excel, In danh sách, Cấu hình cột, Cài đặt bộ lọc', 'Luôn hiện', 'Dữ liệu giới hạn theo phạm vi xem'),
    ('Nút Sửa (dòng, màn chi tiết)', 'Phiếu Đang tạo VÀ người đăng nhập là người tạo', '—'),
    ('Nút In, Lịch sử trên dòng', 'Luôn hiện trên mọi dòng', 'Không có nút Xóa'),
    ('Khối lọc Công ty / Phòng ban', 'Q1 (hoặc Super admin): Công ty + Phòng ban; Q2: Phòng ban', '—'),
    ('Nút Tạo phiếu nhập hàng (màn Phiếu nhập kho điều chỉnh kiểm kê)', 'Phiếu nhập kho Chờ duyệt + Q3',
     'Mở màn Tạo chọn sẵn phiếu nhập kho'),
], widths=[2.4, 2.0, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_XEM, [0, 4, 5, 6]), (A_KTK, [1, 2, 3])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Tạo mới phiếu', 'crud'),
     ('FR-06', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-07', 'Lưu và duyệt (hạch toán)', 'action'),
     ('FR-09', 'In phiếu', 'io'),
     ('FR-10', 'In danh sách', 'io'),
     ('FR-11', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-08', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-12', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu nhập hàng điều chỉnh kiểm kê')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu nhập hàng điều chỉnh kiểm kê',
       mota='Hiển thị bảng các phiếu nhập hàng điều chỉnh kiểm kê trong phạm vi xem của người dùng (theo Q1 / Q2, không có quyền thì '
            'chỉ phiếu mình tạo; phiếu Đang tạo của người khác luôn ẩn), kèm phân trang, sắp xếp và tổng số phiếu khớp bộ lọc. Mỗi '
            'dòng có liên kết sang chi tiết phiếu, sang phiếu nhập kho và phiếu kiểm kê nguồn, cùng các nút Sửa, In, Lịch sử theo '
            'điều kiện.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng để mở màn; dữ liệu giới hạn theo phạm vi xem.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem: Q1 / Super admin mọi phiếu; Q2 phiếu của công ty đang làm việc hoặc do mình tạo; '
             'không có quyền thì phiếu mình tạo; ẩn phiếu Đang tạo của người khác.\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu vừa đi vào màn chi tiết / sửa của màn này) và cấu '
             'hình cột đã lưu của người dùng.\n'
             '4. Hệ thống lấy các phiếu trong phạm vi khớp bộ lọc, sắp phiếu tạo gần nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, kèm dòng “Hiển thị a–b / N” và phân trang.\n'
             '6. Với từng dòng, hệ thống tính nút Sửa (Đang tạo + người tạo); nút Tạo mới chỉ hiện khi có quyền Kế toán kho.',
       phu='• Không có phiếu nào trong phạm vi / khớp bộ lọc → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Máy chủ lỗi khi nạp → thông báo “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”, bảng trống.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, xóa phiên và chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 9 cột; không có cột ẩn mặc định. Cột khóa trong Tùy chỉnh cột: STT, Số phiếu, Hành động. '
               'Sắp xếp được: Số phiếu, Ngày tạo; mặc định Ngày tạo mới nhất ở trên. Đổi bộ lọc, sắp xếp, số dòng đều về trang 1; '
               'mỗi trang tối đa 200 dòng.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Phiếu nhập hàng điều chỉnh kiểm kê'),
   extra=[(shot('00_menu'), 'Mục Phiếu nhập hàng điều chỉnh kiểm kê trong nhóm Nhập hàng (phân hệ Tài chính)')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- Thanh tiêu đề / tab: “Phiếu nhập hàng điều chỉnh kiểm kê”',
         '- Tiêu đề bảng: “Danh sách phiếu nhập hàng điều chỉnh kiểm kê”']),
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
        ['- Chỉ hiện với quyền Kế toán kho (hoặc Super admin)', '- Rê chuột: “Tạo phiếu nhập hàng điều chỉnh kiểm kê”',
         '- Bấm → mở màn Tạo phiếu nhập hàng điều chỉnh kiểm kê (mục 2.5)']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “In danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.10)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.11)',
         '- Khóa trong lúc đang xuất; bên cạnh hiện tiến độ “Đang chuẩn bị dữ liệu…”']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', 'PNHĐCKK-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết phiếu (mục 2.8)', '- Sắp xếp được', '- Cột khóa']),
       ('Cột Phiếu nhập kho', 'Table/Grid', 'Read-only', 'PNKĐCKK-NNNNN', 'Hiển thị',
        ['- Mã phiếu nhập kho điều chỉnh kiểm kê nguồn', '- Là liên kết: bấm → mở chi tiết phiếu nhập kho ở TAB MỚI',
         '- Không sắp xếp']),
       ('Cột Phiếu kiểm kê', 'Table/Grid', 'Read-only', '<mã công ty>.KKK-NNNNN', 'Hiển thị',
        ['- Mã phiếu kiểm kê gốc', '- Là liên kết: bấm → mở chi tiết phiếu kiểm kê ở TAB MỚI', '- Không sắp xếp']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Dạng “Mã kho - Tên kho”', '- Chữ dài tự xuống dòng']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Dạng “Mã phòng ban - Họ tên” của người lập phiếu.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Thời điểm tạo phiếu, căn giữa', '- Sắp xếp được; mặc định mới nhất ở trên']),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 2 giá trị', 'Hiển thị',
        ['- Đang tạo: nhãn xám', '- Đã hạch toán: nhãn xanh lá']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Nút Sửa (bút chì): chỉ phiếu Đang tạo do mình tạo → màn Sửa (mục 2.6)',
           '- Nút In → cửa sổ Xem trước phiếu (mục 2.9)', '- Nút Lịch sử → cửa sổ Lịch sử thay đổi (mục 2.12)',
           '- Không có nút Xóa', '- Cột khóa']),
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
        'Before:\n– Xác định phạm vi xem theo quyền (Q1 > Q2 > phiếu mình tạo; ẩn Đang tạo của người khác).\n'
        '– Khôi phục bộ lọc (10 phút) và cấu hình cột đã lưu.\n'
        'During:\n– Lấy các phiếu trong phạm vi khớp bộ lọc; tính cờ Sửa cho từng dòng, cờ Tạo mới theo quyền Kế toán kho.\n'
        '– Máy chủ lỗi → hiển thị “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, phiếu tạo mới nhất ở trên, kèm dòng “Hiển thị a–b / N”.'),
       ('Bấm Số phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem.\n'
        'After:\n– Mở màn chi tiết phiếu (mục 2.8); bộ lọc hiện tại được ghi nhớ 10 phút để khôi phục khi quay lại.'),
       ('Bấm mã Phiếu nhập kho / Phiếu kiểm kê', 'Click',
        'Before:\n– Dòng có phiếu nguồn.\n'
        'After:\n– Mở chi tiết phiếu nhập kho / phiếu kiểm kê ở tab mới; danh sách giữ nguyên trang và bộ lọc.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Số phiếu, Ngày tạo hỗ trợ sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc; độ rộng cột cố định nên bảng không nhảy bố cục.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại theo số dòng mới.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu nhập hàng điều chỉnh kiểm kê',
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
               'phiếu có ÍT NHẤT 1 dòng hàng khớp (hệ thống cũ có ô nhưng không lọc — HRM lọc thật, có chủ đích). Mọi điều kiện kết '
               'hợp kiểu VÀ. Ngày tạo lấy trọn hai ngày biên. Ô Kho / Người tạo chỉ liệt kê giá trị có trên phiếu trong phạm vi xem. '
               'Ô Công ty chỉ có hiệu lực với Q1 / Super admin. Ghi nhớ bộ lọc: trên trình duyệt, 10 phút.'),
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
       ('Mã phiếu', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập mã phiếu”', '- Số phiếu chứa chuỗi nhập', '- Lọc ngay khi gõ']),
       ('Kho', 'Dropdown', 'Enable', 'Danh sách kho', 'Không', 'Trống',
        ['- Mặc định: trống (mọi kho)', '- Lựa chọn “Mã kho - Tên kho”, chỉ kho có trên phiếu trong phạm vi']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn: Đang tạo / Đã hạch toán']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách người đã tạo phiếu', 'Không', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn “Mã phòng ban - Họ tên”']),
       ('Mã hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập mã hàng hóa”', '- Phiếu có dòng hàng mã chứa chuỗi nhập']),
       ('Tên hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập tên hàng hóa”', '- Phiếu có dòng hàng tên chứa chuỗi nhập']),
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
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 9 cột của bảng danh sách. Ba cột STT, Số phiếu, Hành động bị khóa; cấu '
            'hình lưu riêng theo người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 9 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 9 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ sau khi tải lại trang, đăng nhập lại, đổi '
               'trình duyệt; người dùng khác không bị ảnh hưởng. Cột đang hiện được tích sẵn khi Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 9 cột', '–', 'Theo cấu hình đã lưu',
        '- STT, Số phiếu, Phiếu nhập kho, Phiếu kiểm kê, Kho, Người tạo, Ngày tạo, Trạng thái, Hành động.'),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Số phiếu, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/9 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
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
        'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/9 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5
TABLE_COLS = ('- Cột: STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, SL nhập, Đơn giá nhập (*), Thành tiền nhập, Kho kế toán (*), '
              'Số lượng (*)')
fr(5, 'Tạo mới phiếu nhập hàng điều chỉnh kiểm kê',
   usecase=('FR-05', 'Tạo mới phiếu', 'crud', A_KTK),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo mới phiếu nhập hàng điều chỉnh kiểm kê (Lưu / Lưu và tiếp tục)',
       mota='Kế toán kho lập phiếu hạch toán hàng thừa cho 1 phiếu nhập kho điều chỉnh kiểm kê đang Chờ duyệt. Người dùng chọn Phiếu '
            'nhập kho (hoặc vào từ nút Tạo phiếu nhập hàng ở phiếu nhập kho — chọn sẵn); hệ thống điền Phiếu kiểm kê, Kho, Thủ kho và '
            'nạp bảng Chi tiết với đơn giá nhập gần nhất, mỗi dòng sẵn 1 dòng kho kế toán nhận đủ SL nhập. Người dùng chọn Nhân viên, '
            'phân bổ kho kế toán, sửa đơn giá nếu cần rồi Lưu (trạng thái Đang tạo) — Lưu và duyệt đặc tả ở mục 2.7.',
       tacnhan=TN_KTK,
       dieukien='1. Người dùng đăng nhập thành công, có quyền “%s”.\n2. Có phiếu nhập kho điều chỉnh kiểm kê đang Chờ duyệt.' % Q3,
       chinh='1. Người dùng bấm Tạo mới ở danh sách (hoặc Tạo phiếu nhập hàng ở phiếu nhập kho điều chỉnh kiểm kê Chờ duyệt).\n'
             '2. Hệ thống mở màn “Tạo phiếu nhập hàng điều chỉnh kiểm kê”; góc phải khối Thông tin chung ghi người đăng nhập và giờ '
             'hiện tại; nạp danh sách phiếu nhập kho Chờ duyệt vào ô Phiếu nhập kho.\n'
             '3. Người dùng chọn Phiếu nhập kho; hệ thống điền Phiếu kiểm kê, Kho, Thủ kho và nạp bảng Chi tiết (dòng hàng của phiếu '
             'nhập kho, Đơn giá nhập = giá nhập gần nhất của hàng, 1 dòng kho kế toán nhận đủ SL nhập).\n'
             '4. Người dùng chọn Nhân viên, chọn Kho kế toán cho từng dòng (chọn ở ô đầu tiên của dòng 1 thì hệ thống điền cùng kho '
             'cho ô đầu tiên các dòng khác), bấm Thêm kho để chia 1 dòng vào nhiều kho, sửa Đơn giá nhập nếu cần.\n'
             '5. Người dùng nhập Ghi chú, đính kèm thêm file (không bắt buộc) rồi bấm Lưu.\n'
             '6. Hệ thống kiểm tra đủ trường bắt buộc, tổng số lượng các kho kế toán của mỗi dòng = SL nhập, không trùng kho kế toán.\n'
             '7. Hệ thống sinh mã PNHĐCKK-NNNNN, lưu phiếu Đang tạo (công ty / phòng ban / thủ kho theo người lập phiếu nhập kho), '
             'kèm luôn các file của phiếu nhập kho; lưu dòng hàng + phân bổ; cộng số đã xử lý vào từng dòng kết quả kiểm kê.\n'
             '8. Hệ thống chuyển phiếu nhập kho sang Đang hạch toán (ghi Người duyệt / Ngày duyệt), cập nhật trạng thái phiếu kiểm kê '
             '(Hoàn thành khi đã xử lý hết, ngược lại Đang xử lý) — ghi lịch sử 2 phiếu đó nếu trạng thái đổi.\n'
             '9. Hệ thống ghi mốc “Tạo mới” trong lịch sử phiếu, hiển thị “Lưu thành công.” và về danh sách.',
       phu='• Bấm Lưu và tiếp tục → lưu như trên rồi ở lại màn Thêm với form trống, nạp lại danh sách phiếu nhập kho.\n'
           '• Chưa chọn Phiếu nhập kho → viền đỏ, %s dưới ô; thông báo %s.\n'
           '• Thiếu Nhân viên / Đơn giá nhập / Kho kế toán / Số lượng → %s dưới từng ô cùng lúc; %s.\n'
           '• Tổng số lượng các kho kế toán khác SL nhập → %s dưới cột Thành tiền nhập của dòng đó.\n'
           '• Chọn 2 lần cùng một kho kế toán trong 1 dòng → %s.\n'
           '• Phiếu nhập kho (vào qua đường link) không còn Chờ duyệt / không phải Kế toán kho → báo %s dưới ô, bỏ chọn.\n'
           '• Bấm Quay lại khi đã chọn / nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì thì về danh sách ngay.'
           % (REQ, INCOMPLETE, REQ, INCOMPLETE, MISMATCH, DUP_ACC, SRC_ERR),
       dacbiet='Mã PNHĐCKK-NNNNN tự sinh theo thứ tự, không nhập tay; phiếu không có trường duy nhất phải kiểm trùng. Giữ như hệ thống '
               'cũ (đã chốt): không chặn lập thêm phiếu cho cùng 1 phiếu nhập kho — ô chọn chỉ còn phiếu Chờ duyệt nên lưu xong phiếu '
               'nhập kho tự biến khỏi danh sách. Nút lưu khóa trong lúc lưu. File đính kèm: pdf, png, jpg, jpeg, tối đa 20 MB / file, '
               'tải lên ngay khi chọn. Ghi chú tối đa 65.000 ký tự.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới', 'Từ nút Tạo mới trên danh sách (chỉ Kế toán kho thấy nút): form trống, chọn Phiếu nhập kho tại ô.'),
       (MENU_WII + ' => Xem chi tiết phiếu nhập kho => Tạo phiếu nhập hàng',
        'Hoặc từ dòng / chi tiết một phiếu nhập kho điều chỉnh kiểm kê Chờ duyệt (chỉ Kế toán kho thấy nút): form chọn sẵn phiếu '
        'nhập kho đó.')],
       shot=shot('10_create'), shot_caption='Màn Tạo phiếu nhập hàng điều chỉnh kiểm kê lúc mới mở'),
   extra=[(shot('09_wii_button'), 'Chi tiết phiếu nhập kho Chờ duyệt có nút Tạo phiếu nhập hàng'),
          (shot('10c_filled'), 'Đã chọn Phiếu nhập kho: hệ thống điền thông tin và nạp dòng hàng'),
          (shot('10b_validate'), 'Lưu khi chưa chọn Phiếu nhập kho'),
          (shot('10d_validate'), 'Lưu khi chưa chọn Nhân viên và Kho kế toán'),
          (shot('10f_acc_mismatch'), 'Thêm kho kế toán nhưng tổng số lượng khác SL nhập'),
          (shot('10e_unsaved'), 'Hộp Thông tin chưa lưu khi bấm Quay lại')],
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tạo phiếu nhập hàng điều chỉnh kiểm kê”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', '- Góc phải khối Thông tin chung.'),
       ('Phiếu nhập kho', 'Dropdown', 'Enable', 'Danh sách phiếu Chờ duyệt', 'Có', 'Trống / phiếu chọn sẵn', [
           '- Gợi ý “Chọn phiếu nhập kho” (“Đang tải...” khi đang nạp)',
           '- Chỉ liệt kê phiếu nhập kho điều chỉnh kiểm kê Chờ duyệt, mới nhất trên; không phải Kế toán kho → rỗng',
           '- Chọn → nạp thông tin + dòng hàng; bấm × → xóa thông tin và bảng', '- Lỗi: “Bắt buộc phải nhập”']),
       ('Phiếu kiểm kê', 'Link', 'Read-only', '–', '–', 'Theo phiếu nhập kho', '- Mã phiếu kiểm kê; bấm → mở ở tab mới.'),
       ('Kho', 'Textbox', 'Disable', '–', '–', 'Theo phiếu nhập kho', '- “Mã kho - Tên kho” của phiếu nhập kho, không đổi được.'),
       ('Thủ kho', 'Textbox', 'Disable', '–', '–', 'Theo phiếu nhập kho', '- “Mã NV - Họ tên” người lập phiếu nhập kho.'),
       ('Nhân viên', 'Dropdown', 'Enable', 'Nhân viên đang làm việc', 'Có', 'Trống', [
           '- Gợi ý “Chọn nhân viên”; bấm là hiện danh sách, gõ để lọc',
           '- Nhân viên chịu bút toán Có 3381 khi Lưu và duyệt', '- Lỗi: “Bắt buộc phải nhập”']),
       ('Ghi chú', 'Textarea', 'Enable', '0–65.000 ký tự', 'Không', 'Trống',
        ['- 2 dòng, gợi ý “Nhập ghi chú”, cùng hàng ô Nhân viên', '- Lỗi: “Vui lòng nhập tối đa 65000 ký tự.”']),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, png, jpg, jpeg ≤ 20 MB', 'Không', 'Trống', [
           '- Nút Thêm tài liệu → thêm dòng, chọn file là tải lên ngay',
           '- Mỗi dòng: STT, tên file, xem trước, tải về, xóa, dung lượng',
           '- Lưu xong phiếu tự kèm các file của phiếu nhập kho', '- Lỗi: “Định dạng file không hợp lệ”, “File quá lớn”']),
       ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', '–', 'Theo phiếu nhập kho', [
           TABLE_COLS, '- Mỗi hàng gộp ô theo số dòng kho kế toán đã phân bổ',
           '- Rỗng: “Chọn phiếu nhập kho để nạp hàng hóa”']),
       ('Ô Đơn giá nhập', 'Textbox', 'Enable', '≥ 0, dạng 1,234', 'Có', 'Giá nhập gần nhất của hàng', [
           '- Gợi ý “Nhập đơn giá”', '- Mặc định: giá nhập gần nhất (khác 0) của hàng; chưa từng nhập → 0',
           '- Lỗi: “Bắt buộc phải nhập” / “Đơn giá nhập không hợp lệ.”']),
       ('Ô Thành tiền nhập', 'Label', 'Read-only', 'dạng 1,234', '–', 'Theo dữ liệu', '- = SL nhập × Đơn giá nhập, tự tính lại khi sửa giá.'),
       ('Nút Thêm kho', 'Button', 'Enable', '–', '–', 'Hiển thị', [
           '- Dưới Thành tiền nhập của dòng có SL nhập > 0', '- Rê chuột: “Phân bổ thêm 1 kho kế toán”',
           '- Bấm → thêm 1 dòng kho kế toán trống']),
       ('Ô Kho kế toán', 'Dropdown', 'Enable', 'Kho kế toán của kho + công ty', 'Có', 'Trống', [
           '- Gợi ý “Chọn kho kế toán”', '- Chỉ kho kế toán đang hoạt động của kho vật lý và công ty của phiếu nhập kho',
           '- Chọn ở ô đầu tiên dòng 1 → điền cùng kho cho ô đầu tiên các dòng khác',
           '- Lỗi: “Bắt buộc phải nhập” / “Kho kế toán đã được chọn!”']),
       ('Ô Số lượng (kho kế toán)', 'Textbox', 'Enable', '≥ 0, tối đa 2 chữ số thập phân', 'Có', 'SL nhập (dòng kho đầu)', [
           '- Gợi ý “Nhập số lượng”, căn phải, chỉ nhận số', '- Lỗi: “Bắt buộc phải nhập”',
           '- Tổng các kho ≠ SL nhập → “Số lượng nhập kho kế toán không khớp!”']),
       ('Nút Bỏ kho kế toán', 'Icon Button', 'Enable', '–', '–', 'Từ dòng kho thứ 2',
        ['- Thùng rác đỏ, rê chuột: “Bỏ kho kế toán này”', '- Bấm → xóa dòng kho kế toán đó, bỏ lỗi cũ của dòng']),
       ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Rê chuột: “Lưu phiếu ở trạng thái Đang tạo”', '- Khóa trong lúc lưu']),
       ('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Chỉ ở màn Thêm', '- Rê chuột: “Lưu phiếu ở trạng thái Đang tạo rồi lập tiếp phiếu khác”']),
       ('Nút Lưu và duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Nút chính; xem mục 2.7.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi “Thông tin chưa lưu”.'),
       ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút Thoát: rời màn, không lưu', '- Nút Ở lại: giữ form']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Lưu thành công.”', '- Thiếu dữ liệu: “Bạn chưa nhập đầy đủ thông tin.”', '- Lỗi khác: “Lưu thất bại.”']),
   ],
   ev=[
       ('Mở màn Tạo mới', 'System',
        'Before:\n– Không chặn mở form; ô Phiếu nhập kho chỉ có dữ liệu với quyền Kế toán kho.\n'
        'During:\n– Nạp danh sách phiếu nhập kho Chờ duyệt (không phải Kế toán kho → rỗng); vào kèm phiếu nhập kho thì nạp luôn '
        'thông tin + dòng hàng; phiếu không còn Chờ duyệt / không có quyền → ' + SRC_ERR + ' dưới ô.\n'
        'After:\n– Hiển thị form; bảng Chi tiết “Chọn phiếu nhập kho để nạp hàng hóa” khi chưa chọn.'),
       ('Chọn / bỏ chọn Phiếu nhập kho', 'Change',
        'Before:\n– Giá trị khác giá trị đang chọn.\n'
        'During:\n– Chọn: nạp Phiếu kiểm kê, Kho, Thủ kho, file của phiếu nhập kho, dòng hàng + giá nhập gần nhất, danh sách kho '
        'kế toán; bỏ chọn: xóa các ô đó và bảng Chi tiết.\n'
        'After:\n– Xóa lỗi đang hiện ở ô Phiếu nhập kho / bảng Chi tiết.'),
       ('Chọn Kho kế toán', 'Change',
        'Before:\n– Kho khác kho đang chọn ở ô đó.\n'
        'During:\n– Kho đã có ở dòng kho khác của cùng hàng → ' + DUP_ACC + '.\n'
        'After:\n– Ô đầu tiên của dòng 1: điền cùng kho cho ô đầu tiên các dòng còn lại.'),
       ('Bấm Thêm kho / Bỏ kho kế toán', 'Click',
        'Before:\n– Dòng có SL nhập > 0 (Thêm kho); dòng kho thứ 2 trở đi (Bỏ).\n'
        'After:\n– Thêm 1 dòng kho trống / xóa dòng kho; bỏ lỗi cũ của dòng hàng.'),
       ('Bấm Lưu / Lưu và tiếp tục', 'Click',
        'Before:\n– Không có lượt lưu đang chạy.\n'
        'During:\n– Chưa chọn Phiếu nhập kho, thiếu Nhân viên / Đơn giá nhập / Kho kế toán / Số lượng → ' + REQ + ' dưới ô, '
        + INCOMPLETE + '.\n'
        '– Tổng số lượng kho kế toán ≠ SL nhập → ' + MISMATCH + '; trùng kho kế toán trong 1 dòng → ' + DUP_ACC + '.\n'
        '– Phiếu không có dòng hàng → “Phiếu chưa có hàng hóa.”; Ghi chú > 65.000 ký tự → “Vui lòng nhập tối đa 65000 ký tự.”.\n'
        '– Dòng hàng không còn hợp lệ (hàng / ĐVT / vị trí đã bị xóa) → “Dòng hàng không hợp lệ. Vui lòng load lại trang”.\n'
        + ERR + '\n'
        'After:\n– Sinh phiếu PNHĐCKK-NNNNN trạng thái Đang tạo, lưu dòng hàng + phân bổ, kèm file của phiếu nhập kho.\n'
        '– Cộng số đã xử lý vào kết quả kiểm kê; phiếu nhập kho → Đang hạch toán; phiếu kiểm kê → Hoàn thành / Đang xử lý.\n'
        '– Ghi một dòng lịch sử “Tạo mới”.\n'
        '– Hiển thị “Lưu thành công.”; Lưu → về danh sách; Lưu và tiếp tục → form trống, nạp lại ô Phiếu nhập kho.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– So dữ liệu hiện tại (phiếu nhập kho, nhân viên, ghi chú, đơn giá, kho kế toán, file mới) với lúc mở.\n'
        'During:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát: về danh sách, không lưu; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Chỉnh sửa phiếu',
   usecase=('FR-06', 'Chỉnh sửa phiếu', 'crud', A_KTK),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'edit'),
   intro=dict(
       ten='Chỉnh sửa phiếu nhập hàng điều chỉnh kiểm kê Đang tạo',
       mota='Người tạo sửa phiếu đang ở trạng thái Đang tạo: đổi được Nhân viên, Ghi chú, Đơn giá nhập, phân bổ Kho kế toán / Số '
            'lượng và File đính kèm; Phiếu nhập kho, Phiếu kiểm kê, Kho, Thủ kho, dòng hàng và SL nhập giữ nguyên. Lưu giữ trạng '
            'thái Đang tạo; Lưu và duyệt từ màn Sửa hạch toán như mục 2.7.',
       tacnhan=TN_KTK,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu đang Đang tạo và người đăng nhập là người tạo phiếu.',
       chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra điều kiện, mở màn “Sửa phiếu nhập hàng điều chỉnh kiểm kê: <mã>” điền sẵn dữ liệu đã lưu.\n'
             '3. Người dùng sửa Nhân viên, Ghi chú, Đơn giá nhập, kho kế toán / số lượng, thêm / xóa file rồi bấm Lưu.\n'
             '4. Hệ thống kiểm tra như màn Tạo (mục 2.5), kiểm lại Đang tạo + người tạo, phiếu phải còn ít nhất 1 file.\n'
             '5. Hệ thống ghi lại dòng hàng + phân bổ; cộng thêm số đã xử lý vào kết quả kiểm kê (giữ như hệ thống cũ); phiếu nhập '
             'kho vẫn Đang hạch toán (ghi lại Người duyệt / Ngày duyệt).\n'
             '6. Hệ thống ghi mốc “Thay đổi thông tin” (giá trị cũ → mới của Nhân viên, Ghi chú, bảng dòng hàng, File đính kèm), báo '
             '“Lưu thành công.” và về danh sách.',
       phu='• Phiếu không còn sửa được (đã hạch toán / không phải người tạo) khi mở → tự chuyển về màn chi tiết.\n'
           '• Phiếu đổi trạng thái trong lúc đang sửa → %s; không lưu.\n'
           '• Phiếu không còn file nào khi Lưu → %s dưới khối File đính kèm.\n'
           '• Xóa file ĐÃ LƯU → hộp “Xác nhận xóa” (“Bạn có chắc muốn xóa file đính kèm này?”, Xóa / Hủy); bấm Xóa là gỡ file khỏi '
           'phiếu NGAY (không chờ Lưu), báo “Xóa file thành công”, ghi lịch sử; file cuối cùng không xóa được (“Phiếu phải có ít '
           'nhất 1 file đính kèm.”).\n'
           '• Không đổi gì mà Lưu → không phát sinh mốc thay đổi thông tin.\n'
           '• Bấm Quay lại khi có thay đổi → hộp “Thông tin chưa lưu”.\n'
           '• Phiếu ngoài phạm vi / không tồn tại → trang “không tìm thấy”.' % (CONFLICT, REQ),
       dacbiet='Màn Sửa không có Lưu và tiếp tục; File đính kèm bắt buộc (dấu *). Không có Xóa phiếu (giữ như hệ thống cũ). Giữ như '
               'hệ thống cũ (đã chốt): mỗi lần Lưu ở màn Sửa đều cộng SL nhập thêm một lần vào số đã xử lý của phiếu kiểm kê.'),
   layout=dict(entries=[
       (MENU + ' => Sửa', 'Từ cột Hành động của dòng phiếu Đang tạo do mình tạo.'),
       (MENU + ' => Xem chi tiết => Sửa', 'Hoặc từ chân màn chi tiết phiếu.')],
       shot=shot('12_edit'), shot_caption='Màn Sửa phiếu nhập hàng điều chỉnh kiểm kê'),
   extra=[(shot('17b_detail_draft'), 'Chi tiết phiếu Đang tạo có nút Sửa')],
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Sửa phiếu nhập hàng điều chỉnh kiểm kê: <mã phiếu>”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu nhập kho', 'Link', 'Read-only', '–', '–', 'Theo dữ liệu', '- Bấm → mở chi tiết phiếu nhập kho ở tab mới.'),
       ('Phiếu kiểm kê', 'Link', 'Read-only', '–', '–', 'Theo dữ liệu', '- Bấm → mở chi tiết phiếu kiểm kê ở tab mới.'),
       ('Kho', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', '- Không đổi được.'),
       ('Thủ kho', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', '- Không đổi được.'),
       ('Nhân viên', 'Dropdown', 'Enable', 'Nhân viên đang làm việc', 'Có', 'Theo dữ liệu',
        ['- Quy tắc như mục 2.5', '- Nhân viên đã nghỉ đang gắn trên phiếu vẫn hiện tên']),
       ('Ghi chú', 'Textarea', 'Enable', '0–65.000 ký tự', 'Không', 'Theo dữ liệu', '- Quy tắc như mục 2.5.'),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, png, jpg, jpeg ≤ 20 MB', 'Có', 'File đã lưu',
        ['- Thêm file mới như mục 2.5', '- Xóa file đã lưu: hỏi “Xác nhận xóa”, gỡ ngay', '- Lỗi: “Bắt buộc phải nhập”']),
       ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', '–', 'Dòng đã lưu', [
           '- Dòng hàng, SL nhập giữ nguyên', '- Sửa được Đơn giá nhập, Kho kế toán, Số lượng, Thêm kho / Bỏ kho như mục 2.5',
           '- Kho kế toán đã khóa đang gắn trên phiếu vẫn hiện, có biểu tượng ổ khóa trước tên']),
       ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Lưu, giữ Đang tạo.'),
       ('Nút Lưu và duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Xem mục 2.7.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Lưu thành công.”', '- ' + CONFLICT, '- “Xóa file thành công” / “Xóa file thất bại”']),
   ],
   ev=[
       ('Mở màn Sửa', 'System',
        'Before:\n– Phiếu trong phạm vi xem; ngoài phạm vi → trang “không tìm thấy”.\n'
        'During:\n– Phiếu không Đang tạo hoặc không phải người tạo → chuyển về màn chi tiết.\n'
        'After:\n– Hiển thị form đã điền dữ liệu, danh sách kho kế toán gồm cả kho đang gắn trên phiếu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Kiểm tra Đang tạo + người tạo; không đạt → ' + CONFLICT + ' và dừng xử lý.\n'
        'During:\n– Kiểm tra như mục 2.5 (bắt buộc, khớp số lượng, trùng kho kế toán); phiếu không còn file → ' + REQ + '.\n'
        + ERR + '\n'
        'After:\n– Ghi lại dòng hàng + phân bổ; cộng số đã xử lý vào kết quả kiểm kê; phiếu nhập kho giữ Đang hạch toán.\n'
        '– Ghi lịch sử “Thay đổi thông tin” nếu có thay đổi; “Lưu thành công.”, về danh sách.'),
       ('Bấm xóa file đã lưu → Xóa', 'Click',
        'Before:\n– Hộp “Xác nhận xóa”; phiếu còn sửa được, không → ' + CONFLICT + '.\n'
        'During:\n– Chỉ còn 1 file → “Phiếu phải có ít nhất 1 file đính kèm.”.\n'
        'After:\n– Gỡ file khỏi phiếu, ghi lịch sử, báo “Xóa file thành công”.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– So dữ liệu với lúc mở.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát: về danh sách; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Lưu và duyệt phiếu (hạch toán)',
   usecase=('FR-07', 'Lưu và duyệt', 'action', A_KTK),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lưu và duyệt phiếu nhập hàng điều chỉnh kiểm kê',
       mota='Từ màn Tạo mới hoặc Sửa, Kế toán kho bấm Lưu và duyệt: hệ thống lưu phiếu ở trạng thái Đã hạch toán, cộng ngay tồn kho '
            'kế toán theo từng dòng phân bổ (kèm giá trị theo nhập trước xuất trước), ghi bút toán Nợ 1561 / Có 3381 và chuyển phiếu '
            'nhập kho sang Đã hạch toán. Sau khi duyệt phiếu không sửa được nữa. Màn không gửi thông báo.',
       tacnhan=TN_KTK,
       dieukien='1. Đang ở màn Tạo mới (đủ điều kiện mục 2.5) hoặc Sửa (phiếu Đang tạo của mình).\n'
                '2. Đã chọn Phiếu nhập kho, Nhân viên; mọi dòng có Đơn giá nhập và phân bổ kho kế toán khớp SL nhập.',
       chinh='1. Người dùng bấm Lưu và duyệt.\n'
             '2. Hệ thống kiểm tra trên màn như Lưu (mục 2.5 / 2.6).\n'
             '3. Hệ thống hiện hộp %s: %s.\n'
             '4. Người dùng bấm Lưu và duyệt trong hộp.\n'
             '5. Hệ thống kiểm tra lại ở máy chủ như Lưu.\n'
             '6. Hệ thống lưu phiếu trạng thái Đã hạch toán, lưu dòng hàng + phân bổ, cộng số đã xử lý vào kết quả kiểm kê.\n'
             '7. Với từng dòng phân bổ: cộng tồn kho kế toán (Số lượng × hệ số quy đổi ĐVT) của kho kế toán đó và tồn kế toán của '
             'kho vật lý, ghi nhật ký tồn kèm giá trị trước / sau.\n'
             '8. Hệ thống ghi bút toán: Nợ 1561 từng hàng (Đơn giá nhập × SL nhập × hệ số), Có 3381 tổng tiền theo Nhân viên (kèm công '
             'ty / phòng ban / bộ phận của nhân viên); đơn vị bút toán = người tạo phiếu; ngày hạch toán = lúc lưu.\n'
             '9. Hệ thống chuyển phiếu nhập kho sang Đã hạch toán (ghi Người duyệt / Ngày duyệt), phiếu kiểm kê → Hoàn thành / Đang '
             'xử lý; ghi lịch sử (Tạo mới khi duyệt từ màn Thêm; “Thay đổi trạng thái” Đang tạo → Đã hạch toán khi từ màn Sửa).\n'
             '10. Hệ thống báo “Duyệt thành công.” và về danh sách.' % (CF_TITLE, CF_MSG),
       phu='• Thiếu dữ liệu / lệch số lượng → báo lỗi tại ô như mục 2.5, “Bạn chưa nhập đầy đủ thông tin.”; không hiện hộp xác nhận.\n'
           '• Bấm Hủy trong hộp → đóng hộp, không lưu, form giữ nguyên.\n'
           '• Phiếu đã đổi trạng thái (duyệt từ màn Sửa) → %s.\n'
           '• Ghi bút toán không thành công → báo lỗi, không lưu gì (toàn bộ trong một lần lưu trọn gói).' % CONFLICT,
       dacbiet='Lưu và duyệt KHÔNG hoàn tác được trên màn. Không có bước Gửi duyệt / Không duyệt riêng. Toàn bộ lưu + tồn kho kế toán + '
               'bút toán + trạng thái 2 phiếu nguồn trong một lần lưu trọn gói. Nút khóa trong lúc lưu.'),
   layout=dict(menu=MENU + ' => Tạo mới => Lưu và duyệt', shot=shot('10g_confirm_approve'),
               shot_caption='Hộp Xác nhận lưu và duyệt'),
   extra=[(shot('12b_confirm_approve'), 'Hộp Xác nhận lưu và duyệt mở từ màn Sửa')],
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Lưu và duyệt (chân màn)', 'Button', 'Enable / Disable', 'Hiển thị',
        ['- Nút chính (xanh), rê chuột: “Lưu và duyệt: nhập tồn kho kế toán và hạch toán ngay”', '- Khóa trong lúc lưu']),
       ('Hộp “Xác nhận lưu và duyệt”', 'Popup', 'Hiển thị', 'Ẩn', '- ' + CF_MSG),
       ('Nút Lưu và duyệt (trong hộp)', 'Button', 'Enable', 'Hiển thị', '- Thực hiện lưu + hạch toán.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống Hủy.'),
       ('Lỗi tại ô', 'Label', 'Hiển thị', 'Ẩn',
        ['- Phiếu nhập kho, Nhân viên, Đơn giá nhập, Kho kế toán, Số lượng: “Bắt buộc phải nhập”',
         '- Dưới Thành tiền nhập: “Số lượng nhập kho kế toán không khớp!”']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Duyệt thành công.”', '- Thiếu dữ liệu: “Bạn chưa nhập đầy đủ thông tin.”', '- Lỗi khác: “Lưu thất bại.”']),
       ('Trạng thái sau duyệt', 'Badge', 'Read-only', 'Đã hạch toán', '- Nhãn xanh lá “Đã hạch toán”; nút Sửa biến mất.'),
   ],
   ev=[
       ('Bấm Lưu và duyệt (chân màn)', 'Click',
        'Before:\n– Không có lượt lưu đang chạy.\n'
        'During:\n– Kiểm tra trên màn như Lưu: thiếu → ' + REQ + ', ' + INCOMPLETE + '; lệch số lượng → ' + MISMATCH + '.\n'
        'After:\n– Hiện hộp ' + CF_TITLE + '.'),
       ('Bấm Lưu và duyệt trong hộp', 'Click',
        'Before:\n– Thêm: phiếu nhập kho tồn tại; Sửa: Đang tạo + người tạo, không đạt → ' + CONFLICT + ', dừng xử lý.\n'
        'During:\n– Kiểm tra như Lưu ở máy chủ.\n– Cộng tồn kho kế toán từng dòng phân bổ; ghi bút toán 1561 / 3381; lỗi ghi sổ → '
        'không lưu gì.\n' + ERR + '\n'
        'After:\n– Phiếu → Đã hạch toán; phiếu nhập kho → Đã hạch toán (Người duyệt / Ngày duyệt); phiếu kiểm kê → Hoàn thành / '
        'Đang xử lý.\n'
        '– Ghi một dòng lịch sử (Tạo mới hoặc Thay đổi trạng thái).\n'
        '– Hiển thị “Duyệt thành công.”, về danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nAfter:\n– Đóng hộp; form giữ nguyên, không lưu.'),
       ('Mở lại phiếu đã duyệt ở màn Sửa', 'System',
        'Before:\n– Phiếu Đã hạch toán.\nAfter:\n– Hệ thống tự chuyển về màn chi tiết, không cho sửa.'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'Xem chi tiết phiếu', usecase=('FR-08', 'Xem chi tiết phiếu', 'view', A_XEM),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu nhập hàng điều chỉnh kiểm kê',
       mota='Màn chỉ đọc hiển thị Thông tin chung (Phiếu nhập kho, Phiếu kiểm kê, Kho, Thủ kho, Nhân viên, Ghi chú), File đính kèm, '
            'bảng Chi tiết (dòng hàng gộp theo kho kế toán) và khối Lịch sử. Chân màn có Sửa, In theo điều kiện và Quay lại.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu tồn tại và nằm trong phạm vi xem.',
       chinh='1. Người dùng bấm Số phiếu ở danh sách.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết phiếu nhập hàng điều chỉnh kiểm kê: <mã>”.\n'
             '4. Hệ thống hiển thị các khối và khối Lịch sử (thu gọn).',
       phu='• Phiếu ngoài phạm vi / không tồn tại → chuyển sang trang “không tìm thấy” (404), không báo lỗi nổi.\n'
           '• Máy chủ lỗi → “Không tải được dữ liệu.”.\n'
           '• Phiếu không có file → khối File đính kèm ẩn.\n'
           '• Bấm mã phiếu nhập kho / phiếu kiểm kê → mở ở tab mới; bấm Quay lại → về danh sách, khôi phục bộ lọc (10 phút).',
       dacbiet='Ô Phiếu nhập kho, Nhân viên vẫn giữ dấu * như form nhưng chỉ đọc; bảng Chi tiết không có dấu *. Số hiển thị dạng '
               '1,234.5; tiền dạng 1,234.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết phiếu nhập hàng điều chỉnh kiểm kê'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Chi tiết phiếu nhập hàng điều chỉnh kiểm kê: <mã>”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu nhập kho', 'Link', 'Read-only', 'PNKĐCKK-NNNNN', 'Theo dữ liệu', '- Bấm → mở chi tiết phiếu nhập kho ở tab mới.'),
       ('Phiếu kiểm kê', 'Link', 'Read-only', '–', 'Theo dữ liệu', '- Bấm → mở chi tiết phiếu kiểm kê ở tab mới.'),
       ('Kho', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- “Mã kho - Tên kho”.'),
       ('Thủ kho', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- “Mã NV - Họ tên” người lập phiếu nhập kho.'),
       ('Nhân viên', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- “Mã NV - Họ tên”.'),
       ('Ghi chú', 'Textarea', 'Disable', '0–65.000 ký tự', 'Theo dữ liệu', '- Chỉ đọc.'),
       ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Ẩn khi không có file', '- Xem trước, tải về từng file.'),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, SL nhập, Đơn giá nhập, Thành tiền nhập, Kho kế toán, Số lượng',
         '- Rỗng: “Không có dữ liệu”']),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút Xem lịch sử mở rộng; nội dung như mục 2.12.'),
       ('Nút Sửa', 'Button', 'Enable', '–', 'Theo điều kiện', '- Phiếu Đang tạo do mình tạo; mục 2.6.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Mục 2.9.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về danh sách.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem; không đạt → trang “không tìm thấy”, dừng xử lý.\n'
        'During:\n– Lấy dữ liệu phiếu, file, dòng hàng + phân bổ, cờ nút; lỗi khác → “Không tải được dữ liệu.”.\n'
        'After:\n– Hiển thị màn chỉ đọc.'),
       ('Bấm Xem lịch sử', 'Click', 'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở rộng khối, nạp các mốc lịch sử.'),
       ('Bấm mã Phiếu nhập kho / Phiếu kiểm kê', 'Click', 'Before:\n– Có phiếu nguồn.\nAfter:\n– Mở chi tiết phiếu đó ở tab mới.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Không có dữ liệu cần lưu.\nAfter:\n– Về danh sách, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.9
fr(9, 'In phiếu', usecase=('FR-09', 'In phiếu', 'io', A_XEM),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu nhập hàng điều chỉnh kiểm kê',
       mota='Xem trước và in một phiếu theo mẫu in “PHIẾU NHẬP HÀNG ĐIỀU CHỈNH KIỂM KÊ”, có bảng hàng gộp theo kho kế toán và chỗ ký '
            'Người lập. Bản in mở trong cửa sổ ngay trên màn đang đứng (danh sách hoặc chi tiết), không mở tab mới nên không mất bộ lọc.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm In ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ “Xem trước phiếu nhập hàng điều chỉnh kiểm kê <mã>”, hiện “Đang tải dữ liệu in…” trong lúc dựng.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Phiếu ngoài phạm vi → cửa sổ báo %s.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in phiếu nhập hàng điều chỉnh kiểm kê.”; lỗi khác → “Không tải được dữ liệu in”.\n'
           '• Bấm (x) → đóng cửa sổ, màn giữ nguyên.' % NOTFOUND,
       dacbiet='Logo / letterhead đầu bản in lấy theo công ty ghi trên phiếu (công ty của thủ kho), không theo người đang xem. Ô thông '
               'tin đầu phiếu căn theo đỉnh; khoảng ký Người lập → tên 15px, tên in đậm. Ngày ký (Ngày … Tháng … Năm …) là ngày in.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu nhập hàng điều chỉnh kiểm kê',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Xem trước phiếu nhập hàng điều chỉnh kiểm kê <mã phiếu>”.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → hộp thoại in của trình duyệt.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ xem trước.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Đang tải dữ liệu in…”.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead công ty của phiếu', '- “PHIẾU NHẬP HÀNG ĐIỀU CHỈNH KIỂM KÊ”']),
       ('Thông tin phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        '- Số phiếu, Ngày lập, Phiếu nhập kho, Phiếu kiểm kê, Kho, Thủ kho, Ghi chú.'),
       ('Bảng hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Tên hàng, Model, Mã hàng, ĐVT, SL nhập, Đơn giá nhập, Thành tiền nhập, Kho kế toán, Số lượng',
         '- Mỗi hàng gộp ô theo số kho kế toán']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- “Ngày … Tháng … Năm …”, Người lập + họ tên người tạo phiếu (in đậm).'),
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

# ------------------------------------------------------------ 2.10
fr(10, 'In danh sách', usecase=('FR-10', 'In danh sách', 'io', A_XEM),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In danh sách phiếu theo bộ lọc',
       mota='Xem trước và in danh sách các phiếu khớp bộ lọc đang áp trong phạm vi xem (không phân trang), mẫu “DANH SÁCH PHIẾU NHẬP '
            'HÀNG ĐIỀU CHỈNH KIỂM KÊ”, có chỗ ký Người lập. Tối đa 2.000 dòng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng lọc danh sách (mục 2.2) rồi bấm In danh sách.\n'
             '2. Hệ thống lấy các phiếu theo bộ lọc trong phạm vi xem, dựng bản in.\n'
             '3. Hệ thống mở cửa sổ “Xem trước danh sách phiếu nhập hàng điều chỉnh kiểm kê”.\n'
             '4. Người dùng bấm In.',
       phu='• Trên 2.000 dòng → không dựng bản in, ẩn nút In, hiện “Danh sách có N dòng, vượt mức in tối đa 2.000 dòng nên chưa in '
           'được. Vui lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.”.\n'
           '• Không có dòng → “Không có dữ liệu để in”.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in danh sách phiếu nhập hàng điều chỉnh kiểm kê.”; lỗi khác → “Không tải được dữ liệu in”.',
       dacbiet='Letterhead theo công ty của NGƯỜI IN (danh sách gồm nhiều phiếu). Cột: STT, Số phiếu, Phiếu nhập kho, Phiếu kiểm kê, '
               'Kho, Người tạo, Ngày tạo, Trạng thái.'),
   layout=dict(menu=MENU + ' => In danh sách', shot=shot('19_printlist'), shot_caption='Cửa sổ Xem trước danh sách',
               note='Modal Xem trước được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Xem trước danh sách phiếu nhập hàng điều chỉnh kiểm kê”.'),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', '- Ẩn khi vượt 2.000 dòng.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead công ty người in', '- “DANH SÁCH PHIẾU NHẬP HÀNG ĐIỀU CHỈNH KIỂM KÊ”']),
       ('Bảng danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        '- STT, Số phiếu, Phiếu nhập kho, Phiếu kiểm kê, Kho, Người tạo, Ngày tạo, Trạng thái.'),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- Ngày in, Người lập + họ tên người in (in đậm).'),
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

# ------------------------------------------------------------ 2.11
fr(11, 'Xuất danh sách ra Excel', usecase=('FR-11', 'Xuất Excel', 'io', A_XEM),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất toàn bộ phiếu khớp bộ lọc trong phạm vi xem (không phân trang) ra file Excel. Cột STT '
            'luôn đứng đầu; đầu file có letterhead công ty người xuất và tiêu đề, cuối file có khối ký Người lập.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 7 trường, tích sẵn các trường ứng với cột đang hiện.\n'
             '3. Người dùng tích trường, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy lần lượt toàn bộ phiếu, hiện tiến độ “Đã tải x/y dòng…”, dựng file theo thứ tự trường đã chọn.\n'
             '5. Hệ thống tải file “danh_sach_phieu_nhap_hang_dieu_chinh_kiem_ke.xlsx”, báo “Xuất Excel thành công”.',
       phu='• Không có phiếu khớp → không tạo file, báo “Không có dữ liệu để xuất”.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng (lấy theo từng đợt). Tiêu đề file “DANH SÁCH PHIẾU NHẬP HÀNG ĐIỀU CHỈNH KIỂM KÊ”, trang tính '
               '“Nhap hang dieu chinh kiem ke”.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 7 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        '- Số phiếu, Phiếu nhập kho, Phiếu kiểm kê, Kho, Người tạo, Ngày tạo, Trạng thái.'),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/7 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file Excel', '- Khóa khi chưa tích trường nào hoặc đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('Nội dung file Excel', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Letterhead công ty người xuất, tiêu đề “DANH SÁCH PHIẾU NHẬP HÀNG ĐIỀU CHỈNH KIỂM KÊ”',
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

# ------------------------------------------------------------ 2.12
fr(12, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu',
       mota='Xem các mốc thao tác của phiếu: người thực hiện, thời điểm, hành động, giá trị cũ → mới. Phiếu có các loại mốc: “Tạo mới”, '
            '“Thay đổi thông tin” (Nhân viên, Ghi chú, bảng dòng hàng — Đơn giá nhập và phân bổ Kho kế toán, File đính kèm) và “Thay '
            'đổi trạng thái” (Đang tạo → Đã hạch toán khi Lưu và duyệt từ màn Sửa). Cửa sổ ở danh sách và khối Lịch sử ở màn chi '
            'tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động, hoặc Xem lịch sử ở khối Lịch sử màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem, mở cửa sổ “Lịch sử thay đổi: <mã phiếu>” và nạp các mốc.\n'
             '3. Hệ thống hiển thị các mốc, mới nhất ở trên.',
       phu='• Phiếu lập ở hệ thống cũ chưa có mốc → hiện trạng thái chưa có lịch sử.\n'
           '• Bấm Bộ lọc → mở các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Xem, in, xuất Excel không ghi mốc. Lưu không đổi gì thì không ghi mốc. Mốc chuyển trạng thái của PHIẾU NHẬP KHO và '
               'PHIẾU KIỂM KÊ nguồn ghi ở lịch sử của 2 phiếu đó (kèm ghi chú “Phiếu nhập hàng điều chỉnh kiểm kê <mã>.”), không lặp ở '
               'đây.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('16c_history_filter'), 'Khối Bộ lọc trong cửa sổ Lịch sử thay đổi'),
          (shot('17c_detail_history'), 'Khối Lịch sử ở màn chi tiết phiếu')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <mã phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái: “Trạng thái: Đang tạo → Đã hạch toán”',
           '- Thay đổi thông tin: Nhân viên, Ghi chú cũ → mới; dòng hàng dạng bảng (Đơn giá nhập, Kho kế toán: số lượng); File '
           'đính kèm dạng bảng từng file', '- Mới nhất ở trên']),
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
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu nhập hàng điều chỉnh kiểm kê; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi xem', [
        '– Q1 / Super admin: mọi phiếu; Q2: phiếu có công ty = công ty đang làm việc HOẶC do mình tạo; không có cả hai: phiếu mình tạo.',
        '– Luôn ẩn phiếu Đang tạo của người khác.',
        '– Chi tiết / Sửa / In / Lịch sử áp cùng phạm vi; ngoài phạm vi → trang 404. Menu không gắn quyền.'],
     ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel', 'Lịch sử']),
    ('BR-02', 'Điều kiện lập phiếu', [
        '– Nguồn: phiếu nhập kho điều chỉnh kiểm kê đang Chờ duyệt; người lập có quyền “%s” (hoặc Super admin).' % Q3,
        '– Nút Tạo mới, danh sách ô Phiếu nhập kho và nút Tạo phiếu nhập hàng ở màn phiếu nhập kho đều theo điều kiện này.'],
     ['Tạo mới']),
    ('BR-03', 'Phân bổ kho kế toán', [
        '– Mỗi dòng có SL nhập > 0 phải có ≥ 1 kho kế toán; tổng Số lượng các kho kế toán = SL nhập (so tới 2 chữ số thập phân).',
        '– Không chọn trùng kho kế toán trong 1 dòng; kho kế toán chọn được = kho đang hoạt động của kho vật lý + công ty của phiếu '
        'nhập kho (kho đã khóa đang gắn trên phiếu vẫn giữ, có ổ khóa).',
        '– Mặc định mỗi dòng 1 kho kế toán nhận đủ SL nhập; chọn ô đầu dòng 1 thì điền ô đầu các dòng khác.'],
     ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-04', 'Đơn giá nhập và dòng hàng', [
        '– Dòng hàng + SL nhập lấy từ phiếu nhập kho nguồn; Đơn giá nhập mặc định = giá nhập gần nhất (khác 0) của hàng ở các phiếu '
        'nhập hàng, chưa có → 0; sửa được, ≥ 0.',
        '– Tên / mã / model / ĐVT lấy theo danh mục lúc lưu; hệ số quy đổi theo ĐVT của hàng.',
        '– Thành tiền nhập trên màn = SL nhập × Đơn giá nhập.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-05', 'Hạch toán khi Lưu và duyệt', [
        '– Cộng tồn kho kế toán = Số lượng phân bổ × hệ số ĐVT vào kho kế toán và tồn kế toán của kho vật lý; ghi nhật ký tồn kèm giá '
        'trị trước / sau (nhập trước xuất trước), đơn vị nhật ký = công ty người duyệt.',
        '– Bút toán Nợ 1561 từng hàng = Đơn giá nhập × SL nhập × hệ số; Có 3381 = tổng, theo Nhân viên (công ty / phòng ban / bộ '
        'phận của nhân viên). Đơn vị bút toán = người tạo phiếu; ngày hạch toán = lúc lưu.',
        '– Toàn bộ trong 1 lần lưu: lỗi ở bước nào thì không lưu gì.'], ['Lưu và duyệt']),
    ('BR-06', 'Vòng đời phiếu', [
        '– Lưu → Đang tạo (xám); Lưu và duyệt → Đã hạch toán (xanh lá).',
        '– Không có Xóa / Khóa / Gửi duyệt / Không duyệt / Hủy; điều kiện xóa: không áp dụng.'],
     ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-07', 'Ghi ngược phiếu nguồn', [
        '– Lưu: phiếu nhập kho → Đang hạch toán; Lưu và duyệt: → Đã hạch toán. Cả hai ghi Người duyệt = người thao tác, Ngày duyệt = '
        'lúc lưu; lịch sử phiếu nhập kho ghi “Phiếu nhập hàng điều chỉnh kiểm kê <mã>.”.',
        '– Mỗi lần lưu cộng SL nhập vào số đã xử lý của dòng kết quả kiểm kê (đủ |chênh lệch| → dòng đã xử lý); phiếu kiểm kê → '
        'Hoàn thành khi hết việc điều chuyển / xuất / nhập điều chỉnh, ngược lại Đang xử lý.'],
     ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-08', 'Điều kiện sửa và bắt buộc', [
        '– Chỉ phiếu Đang tạo và đúng người tạo; Super admin không sửa thay. Trạng thái đổi giữa chừng → chặn lưu, báo tải lại trang.',
        '– Bắt buộc: Phiếu nhập kho (khi tạo), Nhân viên, Đơn giá nhập, Kho kế toán, Số lượng; File đính kèm bắt buộc khi Sửa (tạo '
        'mới tự kèm file của phiếu nhập kho), không xóa được file cuối cùng.', '– Ghi chú tối đa 65.000 ký tự.'],
     ['Tạo mới', 'Chỉnh sửa']),
    ('BR-09', 'Mã phiếu và đơn vị sở hữu', [
        '– Mã PNHĐCKK-NNNNN tự sinh theo thứ tự (giữ dãy mã của hệ thống cũ), không nhập / sửa được; không có trường duy nhất.',
        '– Công ty / phòng ban / thủ kho của phiếu = của người lập phiếu nhập kho nguồn (dùng cho phạm vi Q2, letterhead bản in).'],
     ['Tạo mới', 'Xem danh sách', 'In']),
    ('BR-10', 'Hành vi giữ như hệ thống cũ (đã chốt 30/10/2026)', [
        '– Sửa phiếu Đang tạo vẫn cộng thêm số đã xử lý vào phiếu kiểm kê ở mỗi lần lưu.',
        '– Không chặn lập nhiều phiếu cho 1 phiếu nhập kho, không kiểm trạng thái phiếu nhập kho lúc lưu.',
        '– Dòng hàng / SL / đơn giá lấy theo dữ liệu màn gửi lên; lưu phiếu không kiểm quyền riêng ngoài đường vào.'],
     ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt']),
    ('BR-11', 'In và xuất', [
        '– In phiếu: letterhead theo công ty của phiếu. In danh sách / Xuất Excel: letterhead theo công ty người thao tác.',
        '– In danh sách tối đa 2.000 dòng; Xuất Excel không giới hạn; cả hai theo phạm vi xem + bộ lọc.'],
     ['In phiếu', 'In danh sách', 'Xuất Excel']),
    ('BR-12', 'Quy tắc ghi lịch sử', [
        '– Tạo phiếu (Lưu hoặc Lưu và duyệt) → “Tạo mới”; sửa Nhân viên / Ghi chú / dòng hàng / file → “Thay đổi thông tin” (cũ → mới).',
        '– Lưu và duyệt từ màn Sửa → thêm “Thay đổi trạng thái” Đang tạo → Đã hạch toán.',
        '– Xem, in, xuất Excel, lưu không đổi gì: không ghi; hiển thị mới nhất ở trên.'],
     ['Tạo mới', 'Chỉnh sửa', 'Lưu và duyệt', 'Lịch sử']),
    ('BR-13', 'Sử dụng ở màn khác', [
        '– Tồn kho kế toán tăng → Hàng có thể bán theo công ty tăng; lớp giá nhập dùng tính giá vốn Phiếu xuất hàng / Phiếu xuất hàng '
        'điều chỉnh kiểm kê.',
        '– Bút toán Có 3381 theo Nhân viên hiện ở Sổ chi tiết / Bảng cân đối phát sinh công nợ nhân viên.',
        '– Kho vật lý, kho kế toán, vị trí, hàng hóa đã có trên phiếu không xóa được ở danh mục.',
        '– Dữ liệu dùng chung với hệ thống cũ: phiếu lập ở hệ thống cũ cũng hiện trên màn này.'],
     ['Lưu và duyệt', 'Xem danh sách']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Phiếu nhập hàng điều chỉnh kiểm kê (phiếu, trạng thái, dòng hàng, phân '
    'bổ kho kế toán, tồn kho kế toán và bút toán).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Phiếu nhập kho điều chỉnh kiểm kê (nút Tạo phiếu nhập hàng trên phiếu Chờ duyệt mở form chọn sẵn phiếu; trạng thái '
                 'chuyển Đang hạch toán / Đã hạch toán, ghi Người duyệt, Ngày duyệt và lịch sử kèm mã phiếu nhập hàng)', 'Kho -> Nhập kho'),
    ('2', 'Kho', 'Kiểm kê theo hàng hóa (phiếu kiểm kê gốc: cộng số đã xử lý vào dòng hàng thừa, chuyển Hoàn thành / Đang xử lý; liên '
                 'kết mã phiếu kiểm kê từ danh sách / chi tiết)', 'Kho -> Kiểm kho -> Theo vị trí'),
    ('3', 'Tài chính', 'Biên bản xử lý hàng thừa, thiếu sau kiểm kê (đọc giá vốn từ phiếu nhập điều chỉnh của hệ thống cũ; liên kết '
                       '“Phiếu xử lý” còn mở hệ thống cũ)', 'Tài chính -> Kiểm kê'),
    ('4', 'Tài chính', 'Phiếu xuất hàng, Phiếu xuất hàng điều chỉnh kiểm kê (giá vốn xuất theo nhập trước xuất trước đọc lớp giá nhập do '
                       'phiếu đã duyệt ghi; kiểm tồn kho kế toán đã tăng)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('5', 'Tài chính', 'Sổ chi tiết công nợ nhân viên, Bảng cân đối phát sinh công nợ nhân viên (đọc bút toán Có 3381 theo Nhân viên '
                       'của phiếu đã duyệt)', 'Tài chính -> Kế toán công nợ -> Nhân viên'),
    ('6', 'Thông báo', 'Hàng có thể bán theo công ty (tồn kho kế toán của kho kế toán tăng sau Lưu và duyệt)',
     'Thông báo -> Tra cứu tồn kho'),
    ('7', 'Kho', 'Kho kế toán (không xóa được kho kế toán đã có trên phiếu / đã phát sinh tồn; kho đã khóa không chọn mới được)',
     'Kho -> Danh mục'),
    ('8', 'Kho', 'Kho vật lý, Vị trí (không xóa được kho / vị trí đã có trên phiếu)', 'Kho -> Danh mục'),
    ('9', 'Hệ thống ERP', 'Sổ chi tiết vật tư, Báo cáo tồn hàng theo mặt hàng / theo kho, Sổ chi tiết các tài khoản (đọc tồn kho kế '
                          'toán và bút toán 1561 / 3381 dùng chung)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
