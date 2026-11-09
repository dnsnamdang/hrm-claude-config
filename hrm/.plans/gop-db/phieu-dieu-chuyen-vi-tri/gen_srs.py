# -*- coding: utf-8 -*-
"""SRS màn "Phiếu điều chuyển vị trí" (mã PĐCVT-NNNNN) — form chuẩn, chuẩn user chốt 04/11/2026.

Chạy: python gen_srs.py  → SRS - Phiếu điều chuyển vị trí.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc
  ../phieu-xuat-kho-dieu-chinh-kiem-ke/gen_srs.py (phiếu kho Tạo / Sửa / trạng thái, 09/11) + ../kiem-ke-theo-vi-tri/gen_srs.py (màn có
  nút "Tạo phiếu điều chuyển vị trí" — thống nhất tên gọi Nhà / Dãy / Khoang, vị trí, lô). Mục lục sang trang riêng + căn giữa,
  Phần 5 bảng 4 cột.
Nguồn đọc 09/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Entities/PositionTransfer/PositionTransfer.php (STATUSES, 4 quyền, scopedQuery, canView / canEdit / canDelete
      / canPrint), Http/Controllers/V1/PositionTransferController.php, Http/Requests/PositionTransfer/PositionTransferStoreRequest.php,
      Services/PositionTransfer{,Write,Print,Attachment}Service.php, Services/WarehouseInventoryLockService.php,
      Services/PhysicalStockWriter.php::transferLot, Services/StockCardReportService.php, Services/ChangeSummaryReportService.php,
      Entities/PositionInventory/PositionInventoryResult.php::canTransfer, Entities/SelfInventory/SelfInventory.php::canTransfer,
      Routes/api.php}, PermissionsTableSeeder (nhóm "Điều chuyển vị trí" — nhánh develop CHƯA có Catalog + mã quyền, tên quyền
      theo code), MasterData Position / PhysicalWarehouse / ProductUsageGuard (chặn xóa).
  FE  pages/warehouse/position-transfers/** (index, create, _id/index, _id/edit, components/{PositionTransferForm.vue,
      PositionPickerModal.vue, LotPickerModal.vue, row-actions.js, export-excel.js}), components/subsystem-menu/warehouse.js,
      pages/warehouse/position-inventory-results (nút Tạo phiếu điều chuyển vị trí), pages/warehouse/self-inventories,
      pages/warehouse/stock-card/components/voucher-link.js.
  Bối cảnh: design.md, plan.md (#11789 #11791 #11808 #11811 #11812 #11813 #11815 #11855 #11875 #12036 #12037), spec
      docs/superpowers/specs/gop-db/2026-10-19-phieu-dieu-chuyen-vi-tri-design.md.
Ảnh: ./pdcvt_shots — dev-hrm 09/11/2026 (_capture/capture.js, DNS Admin, chặn mọi yêu cầu ghi: 0 yêu cầu ghi; POST In dự kiến cho
  qua vì chỉ dựng bản in). GIẢ TRÊN TRÌNH DUYỆT: (1) danh sách Kho chọn được ở form Tạo (DNS Admin trên dev không là thủ kho kho nào
  → giả 2 kho thật PTT / LN) — ảnh 10_create, 10c_filled, 10d, 10e, 10f, 10h, 11_*, 18b; (2) lỗi do máy chủ trả của Lưu nháp /
  Điều chuyển gán thẳng vào form (không bấm lưu) — ảnh 10b_validate, 10d_validate_transfer. Còn lại là dữ liệu / trạng thái thật.
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

TEN = 'Phiếu điều chuyển vị trí'
SHOTS = os.path.join(HERE, 'pdcvt_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Điều chuyển => Phiếu điều chuyển vị trí'
MENU_KKVT = 'Phân hệ Kho => Kiểm kho => Theo vị trí => Kiểm kê theo vị trí'
MENU_KKHH = 'Phân hệ Kho => Kiểm kho => Theo vị trí => Kiểm kê theo hàng hóa'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu điều chuyển vị trí.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
Q1 = 'Điều chuyển vị trí'
V1 = 'Xem điều chuyển vị trí theo tổng công ty'
V2 = 'Xem điều chuyển vị trí theo công ty'
V3 = 'Xem điều chuyển vị trí theo kho'
A_XEM = 'Người xem phiếu'
A_LAP = 'Người lập phiếu'
TN = ('Người dùng có quyền thực hiện chức năng: %s / %s / %s (không có quyền nào thì chỉ phiếu mình tạo).' % (V1, V2, V3))
TN_LAP = 'Người dùng có quyền thực hiện chức năng: %s (thủ kho của kho lập phiếu; Super admin mọi kho).' % Q1
TN_SUA = ('Người dùng có quyền thực hiện chức năng: người xem được phiếu Đang tạo (theo %s / %s / %s hoặc phiếu mình tạo) — '
          'giữ như hệ thống cũ, không bắt buộc là người tạo.' % (V1, V2, V3))
DK = ('1. Người dùng đăng nhập thành công.\n2. Phiếu nằm trong phạm vi xem của người dùng.\n'
      '3. Người dùng đang ở màn danh sách Phiếu điều chuyển vị trí.')
REQ = '“Bắt buộc phải nhập”'
MISS = '“Bạn chưa nhập đầy đủ thông tin.”'
NOPERM = '“Bạn không có quyền thực hiện chức năng này.”'
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NOTFOUND = '“Không tìm thấy phiếu điều chuyển vị trí hoặc bạn không có quyền xem.”'
SAME_POS = '“Không thể xuất và nhập cùng một vị trí!”'
NEED_FROM = '“Vui lòng chọn vị trí xuất trước.”'
CONFIRM_TF = ('“Hàng hóa sẽ được chuyển sang vị trí nhập và cập nhật tồn kho ngay. Phiếu đã điều chuyển không sửa, xóa được. Bạn '
              'có muốn tiếp tục?”')
DOIKHO = '“Nếu bạn thay đổi kho, danh sách hàng hóa sẽ được làm mới. Bạn có chắc chắn muốn thực hiện?”'
STOCK_ERR = ('“Vượt quá SL tồn của lô.” / “Vượt quá SL tồn tại vị trí xuất.” (dưới ô SL của mọi dòng thuộc nhóm vượt)')
LOCK_ERR = ('“Hàng đang kiểm kho.” (dưới ô Tên hàng hóa) / “Vị trí đang kiểm kho.” / “Vị trí không thuộc kho của phiếu.” (dưới ô '
            'Vị trí xuất / Vị trí nhập)')
SRC_ROW_ERR = '“Đã được xử lý hoặc không thuộc phiếu kiểm kê. Vui lòng tải lại trang.”'

d = SrsDoc(out=OUT, menu=MENU, route='/warehouse/position-transfers', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Điều chuyển': 'menu_nhom', 'Phiếu điều chuyển vị trí': 'menu_muc',
    'Kiểm kho': 'kkvt_menu_nhom', 'Theo vị trí': 'kkvt_menu_nhom2', 'Kiểm kê theo vị trí': 'kkvt_menu_muc',
    'Kiểm kê theo hàng hóa': 'kkhh_menu_muc', 'Tạo phiếu điều chuyển vị trí': 'btn_taodieuchuyen',
    'Xem chi tiết phiếu kiểm kê': 'link_pkk_form',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Thêm hàng hóa': 'btn_themhanghoa', 'Chọn vị trí xuất': 'o_vitrixuat', 'Chọn lô xuất': 'o_loxuat',
    'Sửa': 'btn_sua_row', 'Nút Điều chuyển': 'btn_dieuchuyen', 'Xóa': 'btn_xoa_row', 'In dự kiến': 'btn_indukien',
    'Xem chi tiết': 'link_sophieu', 'In': 'btn_in_row', 'Xuất Excel': 'btn_xuatexcel', 'Lịch sử': 'btn_lichsu_row',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu điều chuyển vị trí (mã phiếu PĐCVT-NNNNN), phân hệ Kho, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ nghiệp vụ chuyển hàng giữa 2 VỊ TRÍ trong CÙNG một kho, theo từng LÔ: thủ kho chọn hàng, vị trí xuất, lô xuất, vị trí '
    'nhập và số lượng → Lưu nháp (Đang tạo, chưa đổi tồn) → Điều chuyển (Đã chuyển: trừ tồn lô tại vị trí xuất, cộng tồn lô tại vị trí '
    'nhập; tổng tồn của kho không đổi).',
    'Làm rõ 2 lối lập phiếu từ kết quả kiểm kê (Kiểm kê theo vị trí, Kiểm kê theo hàng hóa) cho các dòng chênh THIẾU, và dữ liệu bị ghi '
    'ngược về phiếu kiểm kê nguồn, Thẻ kho, các báo cáo tồn theo vị trí.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo mới (Lưu nháp / Lưu và tiếp tục), Chọn '
    'hàng hóa – vị trí – lô (popup), Chỉnh sửa phiếu Đang tạo, Điều chuyển (ghi tồn), Xóa phiếu Đang tạo, In dự kiến, Xem chi tiết, In '
    'phiếu, Xuất Excel danh sách, Xem lịch sử thay đổi. Màn KHÔNG có Khóa / Mở khóa, Gửi duyệt / Duyệt / Không duyệt, Hủy phiếu, In danh '
    'sách và Import Excel: Điều chuyển là bước cuối, thực hiện ngay không qua duyệt (giữ như hệ thống cũ).')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phiếu Đã chuyển là chứng từ dịch chuyển tồn kho thực tế giữa các vị trí: mỗi dòng trừ tồn đúng lô tại vị trí xuất và cộng cùng lô '
    'tại vị trí nhập (theo công ty của lô).',
    'Dòng điều chuyển hiện ở Thẻ kho (số chứng từ PĐCVT-NNNNN, 1 dòng xuất ở vị trí cũ + 1 dòng nhập ở vị trí mới); báo cáo tồn theo vị '
    'trí thay đổi, tổng tồn kho không đổi.',
    'Lập từ phiếu kiểm kê: số đã điều chuyển được cộng vào phần đã xử lý của dòng kết quả kiểm kê; xử lý hết thì phiếu kiểm kê (và kế '
    'hoạch kiểm kê cha) chuyển Hoàn thành.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Chỉ lập phiếu cho kho mình là thủ kho (Super admin: mọi kho đang hoạt động), cần quyền “%s” (BR-02).' % Q1,
    'Điều chuyển kiểm đủ tồn lô tại vị trí xuất và tồn vị trí (trừ hàng phiếu nhập chưa hạch toán); vị trí xuất ≠ vị trí nhập, cùng kho; '
    'hàng / vị trí đang kiểm kho thì chặn (BR-05, BR-06).',
    'Điều chuyển ghi tồn ngay, KHÔNG hoàn tác: phiếu Đã chuyển không sửa, không xóa được (BR-07).',
    'Phiếu Đang tạo: ai xem được cũng sửa / xóa được (giữ như hệ thống cũ, đã chốt) (BR-08).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu điều chuyển vị trí (phiếu)', 'Chứng từ PĐCVT-NNNNN của màn này: chuyển hàng giữa các vị trí trong cùng 1 kho, theo lô.'),
    ('Vị trí', 'Ô chứa hàng trong kho vật lý, mã dạng <Kho>-<Nhà>-<Dãy>-<Khoang>-<Tầng> (vd PTT-N1-D1-K1-T1); cấu trúc phân cấp '
               'Nhà > Dãy > Khoang > vị trí.'),
    ('Vị trí xuất / Vị trí nhập', 'Vị trí lấy hàng ra (phải còn tồn hàng đó) / vị trí đặt hàng vào (mọi vị trí của kho); hai vị trí '
                                  'phải khác nhau.'),
    ('Lô / Lô xuất', 'Lô nhập kho của hàng (số lô kèm tiền tố mã công ty, vd TPE-29/10/2026-…); trường đặc thù: hàng được chuyển theo '
                     'đúng lô, giữ nguyên lô ở vị trí nhập.'),
    ('SL tồn', 'Tồn của lô tại vị trí xuất quy theo ĐVT của dòng (lập từ phiếu kiểm kê: tồn của cả lô); chữ đỏ khi SL > SL tồn.'),
    ('ĐVT', 'Đơn vị tính của dòng; mặc định ĐVT cơ sở, đổi được (SL quy đổi theo hệ số khi ghi tồn).'),
    ('Trạng thái Đang tạo', 'Nhãn xám: phiếu lưu nháp, chưa đổi tồn; sửa, xóa được.'),
    ('Trạng thái Đã chuyển', 'Nhãn xanh lá: đã điều chuyển, tồn đã ghi; chỉ xem, in.'),
    ('Đang kiểm kho', 'Hàng thuộc phiếu kiểm kê theo hàng hóa đang kiểm tại kho, hoặc vị trí thuộc kế hoạch / phiếu kiểm kê theo vị trí '
                      'đang kiểm / chờ duyệt kết quả: không được điều chuyển.'),
    ('Phiếu kiểm kê nguồn', 'Phiếu Kiểm kê theo vị trí (<mã cty>-KKVT-NNNNN) hoặc Kiểm kê theo hàng hóa (<mã cty>.KKK-NNNNN) mà phiếu '
                            'được lập từ đó; các dòng lấy theo phần chênh THIẾU chưa xử lý.'),
    ('In dự kiến', 'Bản in xem trước theo dữ liệu đang nhập trên form (chưa lưu), có thêm cột Ghi chú để thủ kho ghi tay.'),
    ('Cấu trúc phân cấp', 'Phiếu (1 kho) > dòng hàng (hàng, ĐVT, vị trí xuất, lô xuất, vị trí nhập, SL).'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn có 4 quyền (nhóm quyền “Điều chuyển vị trí”, phân hệ Kho, tên giữ như hệ thống cũ). Super admin có đủ mọi quyền và chọn được '
    'mọi kho. Không gắn quyền ở menu: ai cũng mở được màn, dữ liệu do hệ thống giới hạn.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1, 'Có nút Tạo mới; lập phiếu (tay hoặc từ phiếu kiểm kê) cho kho mình là thủ kho. Không có quyền thì nút Tạo mới ẩn, lối vào '
               'từ phiếu kiểm kê chuyển trang “không tìm thấy”.'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Mọi phiếu của mọi công ty; khối lọc có ô Công ty và Phòng ban.'),
    ('V2', V2, 'Phiếu có công ty = công ty đang làm việc + phiếu mình tạo; khối lọc có ô Phòng ban.'),
    ('V3', V3, 'Phiếu của các kho mình là thủ kho + phiếu mình tạo.'),
    ('—', 'Không có V1 / V2 / V3', 'Chỉ phiếu do chính mình tạo.'),
], widths=[0.8, 2.2, 3.0])
d.p('Thứ tự ưu tiên khi có nhiều quyền: V1 > V2 > V3 > phiếu mình tạo. Công ty / phòng ban của phiếu lấy theo người lập phiếu.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ theo V*', '✅ mọi phiếu', '✅ công ty', '✅ kho thủ kho', '✅ phiếu mình tạo'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅ (có ô Công ty, Phòng ban)', '✅ (có ô Phòng ban)', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo mới phiếu', '✅ kho thủ kho', '❌', '❌', '❌', '❌ (ẩn nút Tạo mới)'),
    ('FR-06 Chọn hàng hóa, vị trí, lô', '✅ khi Tạo', 'Theo FR-07', 'Theo FR-07', 'Theo FR-07', 'Theo FR-07'),
    ('FR-07 Chỉnh sửa phiếu Đang tạo', '✅ phiếu xem được', '✅ phiếu xem được', '✅ phiếu xem được', '✅ phiếu xem được',
     '✅ phiếu mình tạo'),
    ('FR-08 Điều chuyển', '✅ (Tạo / Sửa)', '✅ (Sửa)', '✅ (Sửa)', '✅ (Sửa)', '✅ (Sửa phiếu mình tạo)'),
    ('FR-09 Xóa phiếu Đang tạo', '✅ phiếu xem được', '✅ phiếu xem được', '✅ phiếu xem được', '✅ phiếu xem được',
     '✅ phiếu mình tạo'),
    ('FR-10 In dự kiến', '✅', '✅ (màn Sửa)', '✅ (màn Sửa)', '✅ (màn Sửa)', '✅ (màn Sửa)'),
    ('FR-11 Xem chi tiết', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ phiếu mình tạo'),
    ('FR-12 In phiếu (Đã chuyển)', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ phiếu mình tạo'),
    ('FR-13 Xuất Excel', '✅ theo phạm vi', '✅ theo phạm vi', '✅ theo phạm vi', '✅ theo phạm vi', '✅ phiếu mình tạo'),
    ('FR-14 Xem lịch sử thay đổi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ phiếu mình tạo'),
    ('Khóa – Mở khóa / Duyệt – Không duyệt / Hủy / In danh sách / Import', '—', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.9, 0.85, 0.85, 0.85, 0.85, 0.9])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có V1 / V2 / V3: vẫn mở được màn, danh sách chỉ có phiếu do chính mình tạo; không có khối Công ty – Phòng ban.',
    'Không có Q1: không có nút Tạo mới; mở đường link Tạo mới vẫn vào form nhưng ô Kho chỉ có kho mình là thủ kho và lưu bị từ chối '
    '%s; vào từ nút “Tạo phiếu điều chuyển vị trí” của phiếu kiểm kê thì chuyển trang “không tìm thấy” (404).' % NOPERM,
    'Có Q1 nhưng không là thủ kho kho nào (không phải Super admin): ô Kho rỗng, không lập phiếu tay được.',
    'Mở chi tiết / sửa / in / lịch sử phiếu ngoài phạm vi qua đường link: chuyển trang “không tìm thấy” (404), không hiện dữ liệu.',
    'Phiếu không còn Đang tạo: không có nút Sửa / Xóa; mở thẳng màn Sửa thì hệ thống tự chuyển về màn chi tiết.',
    'Bị gỡ quyền giữa lúc thao tác: lần nạp dữ liệu / lần lưu tiếp theo hệ thống áp quyền mới (quyền kiểm lại ở từng lần gọi).',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới', 'Có quyền Q1 (hoặc Super admin)', 'Ẩn khi thiếu quyền'),
    ('Nút Xuất Excel, Cấu hình cột, Cài đặt bộ lọc', 'Luôn hiện', 'Dữ liệu giới hạn theo phạm vi xem'),
    ('Nút Sửa, Xóa (dòng, màn chi tiết)', 'Phiếu Đang tạo VÀ nằm trong phạm vi xem', 'Không bắt buộc là người tạo (như hệ thống cũ)'),
    ('Nút In (dòng, màn chi tiết)', 'Phiếu Đã chuyển', '—'),
    ('Nút Lịch sử trên dòng', 'Luôn hiện trên mọi dòng', '—'),
    ('Khối lọc Công ty / Phòng ban', 'V1 (hoặc Super admin): Công ty + Phòng ban; V2: Phòng ban', '—'),
    ('Nút Tạo phiếu điều chuyển vị trí (Kiểm kê theo vị trí)', 'Phiếu kiểm kê Chờ xử lý + quyền Xử lý phiếu kiểm kê vị trí + còn dòng '
     'chênh thiếu chưa xử lý', 'Mở form Tạo nạp sẵn kho + dòng; cần thêm Q1'),
    ('Nút Tạo phiếu điều chuyển vị trí (Kiểm kê theo hàng hóa)', 'Phiếu kiểm kê Chờ / Đang xử lý + quyền Xử lý phiếu kiểm kê hàng hóa + '
     'còn dòng cần điều chuyển + chưa có phiếu điều chuyển', 'Mở form Tạo nạp sẵn kho + dòng; cần thêm Q1'),
], widths=[2.4, 2.0, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_XEM, [0, 6, 7]), (A_LAP, [1, 2, 3, 4, 5])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Tạo mới phiếu', 'crud'),
     ('FR-07', 'Chỉnh sửa phiếu', 'crud'),
     ('FR-08', 'Điều chuyển', 'action'),
     ('FR-09', 'Xóa phiếu', 'action'),
     ('FR-10', 'In dự kiến', 'io'),
     ('FR-12', 'In phiếu', 'io'),
     ('FR-13', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn hàng hóa, vị trí, lô', 'crud', 'extend', [1, 2], None),
     ('FR-11', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-14', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu điều chuyển vị trí')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu điều chuyển vị trí',
       mota='Hiển thị bảng các phiếu điều chuyển vị trí trong phạm vi xem của người dùng (theo V1 / V2 / V3, không có quyền thì chỉ phiếu '
            'mình tạo), kèm phân trang, sắp xếp và tổng số phiếu khớp bộ lọc. Mỗi dòng có liên kết sang chi tiết phiếu, sang phiếu kiểm '
            'kê nguồn (nếu có) và các nút Sửa, Xóa, In, Lịch sử theo trạng thái.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng để mở màn; dữ liệu giới hạn theo phạm vi xem.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem: V1 / Super admin mọi phiếu; V2 phiếu của công ty đang làm việc + phiếu mình tạo; V3 phiếu '
             'của kho mình là thủ kho + phiếu mình tạo; không có quyền thì phiếu mình tạo.\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu vừa đi vào màn chi tiết / sửa của màn này) và cấu hình cột '
             'đã lưu của người dùng.\n'
             '4. Hệ thống lấy các phiếu trong phạm vi khớp bộ lọc, sắp phiếu tạo gần nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, kèm dòng “Hiển thị a–b / N” và phân trang.\n'
             '6. Với từng dòng, hệ thống tính nút Sửa / Xóa (phiếu Đang tạo) và In (phiếu Đã chuyển); nút Tạo mới hiện khi có quyền Q1.',
       phu='• Không có phiếu nào trong phạm vi / khớp bộ lọc → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Máy chủ lỗi khi nạp → thông báo “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”, bảng trống.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, xóa phiên và chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 10 cột; không có cột ẩn mặc định. Cột khóa trong Tùy chỉnh cột: STT, Mã phiếu, Hành động. Sắp xếp '
               'được: Mã phiếu, Kho; mặc định Ngày tạo mới nhất ở trên (cột Ngày tạo, Trạng thái, Người tạo không sắp xếp). Đổi bộ lọc, '
               'sắp xếp, số dòng đều về trang 1.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Phiếu điều chuyển vị trí'),
   extra=[(shot('00_menu'), 'Menu phân hệ Kho › Điều chuyển › Phiếu điều chuyển vị trí')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- Thanh tiêu đề / tab và tiêu đề bảng: “Danh sách phiếu điều chuyển vị trí”']),
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
        ['- Chỉ hiện khi có quyền “%s”' % Q1, '- Rê chuột: “Tạo phiếu điều chuyển vị trí”', '- Bấm → mở màn Tạo phiếu (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.13)',
         '- Khóa trong lúc đang xuất']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa']),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PĐCVT-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết phiếu (mục 2.11)', '- Sắp xếp được', '- Cột khóa, dính trái khi cuộn ngang']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Thời điểm tạo phiếu', '- Không sắp xếp; mặc định danh sách mới nhất ở trên']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Dạng “Mã kho - Tên kho”', '- Sắp xếp được (theo tên kho)']),
       ('Cột Phiếu kiểm kê', 'Table/Grid', 'Read-only', '–', 'Hiển thị', [
           '- Mã phiếu kiểm kê nguồn; trống khi lập tay',
           '- Kiểm kê theo vị trí / theo hàng hóa: liên kết mở chi tiết ở TAB MỚI',
           '- Phiếu kiểm kho theo hàng hoá của hệ thống cũ: liên kết mở hệ thống cũ ở tab mới', '- Không sắp xếp']),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 2 giá trị', 'Hiển thị',
        ['- Đang tạo: nhãn xám', '- Đã chuyển: nhãn xanh lá', '- Không sắp xếp']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Dạng “Họ tên - Mã phòng ban”; không sắp xếp.'),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Lần lưu gần nhất.'),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Dạng “Họ tên - Mã phòng ban”.'),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Nút Sửa (bút chì), Xóa (thùng rác đỏ): chỉ phiếu Đang tạo trong phạm vi xem → màn Sửa (mục 2.7) / hộp Xác nhận xóa (mục 2.9)',
           '- Nút In (máy in): chỉ phiếu Đã chuyển → cửa sổ Xem trước (mục 2.12)',
           '- Nút Lịch sử: mọi dòng → cửa sổ Lịch sử thay đổi (mục 2.14)',
           '- Dòng có trên 3 nút: nút cuối gom vào “Hành động khác” (ba chấm)', '- Cột khóa']),
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
        'Before:\n– Xác định phạm vi xem theo quyền (V1 > V2 > V3 > phiếu mình tạo).\n'
        '– Khôi phục bộ lọc (10 phút) và cấu hình cột đã lưu.\n'
        'During:\n– Lấy các phiếu trong phạm vi khớp bộ lọc; tính cờ Sửa / Xóa / In cho từng dòng và cờ Tạo mới.\n'
        '– Máy chủ lỗi → hiển thị “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, phiếu tạo mới nhất ở trên, kèm dòng “Hiển thị a–b / N”.'),
       ('Bấm Mã phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem.\n'
        'After:\n– Mở màn chi tiết phiếu (mục 2.11); bộ lọc hiện tại được ghi nhớ 10 phút để khôi phục khi quay lại.'),
       ('Bấm mã Phiếu kiểm kê', 'Click',
        'Before:\n– Dòng có phiếu kiểm kê nguồn.\n'
        'After:\n– Mở chi tiết phiếu kiểm kê ở tab mới (phiếu của hệ thống cũ mở trên hệ thống cũ); danh sách giữ nguyên trang và bộ lọc.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Mã phiếu, Kho hỗ trợ sắp xếp.\n'
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
       ten='Tìm kiếm và lọc danh sách phiếu điều chuyển vị trí',
       mota='Thu hẹp danh sách theo mã phiếu, trạng thái, kho, người tạo, mã / tên hàng hóa trên phiếu, ngày tạo và Công ty – Phòng ban. '
            'Ô tìm nhanh tìm theo mã phiếu; các ô lọc nằm trong khối Tìm kiếm nâng cao, bật / tắt được bằng Cài đặt bộ lọc (mục 2.3). Mọi '
            'điều kiện chỉ lọc trong phạm vi xem của người dùng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập mã phiếu vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Ô chọn (Trạng thái, Kho, Người tạo, Ngày tạo, Công ty, Phòng ban) lọc ngay khi đổi; ô chữ Hàng hóa và ô tìm nhanh chỉ áp '
             'khi bấm Tìm kiếm / nhấn Enter; luôn về trang 1.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.\n'
             '5. Hệ thống ghi nhớ bộ lọc 10 phút khi người dùng đi vào màn chi tiết / sửa của màn này.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Gõ vào ô tìm nhanh / ô Hàng hóa mà chưa bấm Tìm kiếm / Enter → danh sách chưa đổi.\n'
           '• Bấm dấu × trong ô chọn → xóa giá trị của ô đó.\n'
           '• Không có V1 / V2 → không có ô Công ty / Phòng ban.',
       dacbiet='Kiểu khớp chữ: một phần, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối; không giới hạn số ký tự; ký tự % và _ '
               'được hiểu là ký tự đại diện; chữ Đ trong mã phiếu không tìm được bằng chữ D. Hàng hóa lọc phiếu có ÍT NHẤT 1 dòng hàng có mã '
               'HOẶC tên chứa chuỗi (cả phiếu nháp). Mọi điều kiện kết hợp kiểu VÀ. Ngày tạo lấy trọn hai ngày biên. Ô Kho liệt kê mọi kho; '
               'ô Người tạo liệt kê toàn bộ nhân viên. Ghi nhớ bộ lọc: trên trình duyệt, 10 phút.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo mã phiếu”', '- Khớp một phần mã phiếu', '- Chỉ lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh + ô Hàng hóa, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, về trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (mọi trạng thái)', '- Lựa chọn: Đang tạo / Đã chuyển', '- Lọc ngay khi chọn']),
       ('Kho', 'Dropdown', 'Enable', 'Danh sách kho', 'Không', 'Trống',
        ['- Mặc định: trống (mọi kho)', '- Lựa chọn “Mã kho - Tên kho”, mọi kho của hệ thống']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Liệt kê toàn bộ nhân viên (cả người chưa tạo phiếu nào)']),
       ('Hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Mã hoặc tên hàng”', '- Phiếu có dòng hàng mã hoặc tên chứa chuỗi nhập', '- Áp khi bấm Tìm kiếm']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai ngày biên; được bỏ trống một đầu']),
       ('Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống',
        ['- Chỉ hiện với V1 / Super admin', '- Mặc định: trống; xem được cả công ty đã khóa']),
       ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống',
        ['- Chỉ hiện với V1 hoặc V2', '- Chọn Công ty trước thì chỉ còn phòng ban của công ty đó']),
   ],
   ev=[
       ('Đổi giá trị một ô chọn', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\nDuring:\n– Ghi nhận giá trị mới.\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí trong phạm vi xem.'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh và ô Hàng hóa, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm phiếu có mã chứa chuỗi; phiếu có dòng hàng mã / tên chứa chuỗi Hàng hóa.\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nAfter:\n– Xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\n'
        'After:\n– Mở / thu gọn khối ô lọc; lần mở đầu hệ thống nạp danh sách Trạng thái, Kho.'),
       ('Quay lại từ màn chi tiết trong 10 phút', 'System',
        'Before:\n– Người dùng vừa đi từ danh sách vào màn chi tiết / sửa.\n'
        'After:\n– Khôi phục bộ lọc và trạng thái khối lọc; quá 10 phút thì bộ lọc về trống.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn những ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự. Cấu hình lưu riêng theo '
            'người dùng cho màn này, không ảnh hưởng người khác và không làm đổi dữ liệu phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 6 mục lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 6 mục theo thứ tự thiết kế; vẫn phải bấm Lưu.\n'
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
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách 6 mục', '–', 'Theo cấu hình đã lưu',
        ['- Trạng thái', '- Kho', '- Người tạo', '- Hàng hóa', '- Ngày tạo', '- Công ty – Phòng ban']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → ô lọc đó không hiện.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích lại đủ 6 mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
       ('Khối Tìm kiếm nâng cao sau khi lưu', 'Label', 'Hiển thị', '–', '–', 'Theo cấu hình', '- Chỉ hiện ô đã tích, đúng thứ tự.'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình đang lưu (chưa lưu lần nào → đủ 6 mục).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ 6 mục, thứ tự thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 10 cột của bảng danh sách. Ba cột STT, Mã phiếu, Hành động bị khóa; cấu hình lưu '
            'riêng theo người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 10 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 10 cột (gồm Ngày cập nhật, Người cập nhật thêm theo #12036). Cấu hình ghi nhớ theo người dùng trên máy '
               'chủ: giữ sau khi tải lại trang, đăng nhập lại, đổi trình duyệt; người dùng khác không bị ảnh hưởng. Cột đang hiện được tích '
               'sẵn khi Xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 10 cột', '–', 'Theo cấu hình đã lưu',
        '- STT, Mã phiếu, Ngày tạo, Kho, Phiếu kiểm kê, Trạng thái, Người tạo, Ngày cập nhật, Người cập nhật, Hành động.'),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Mã phiếu, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/10 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- n = số cột đang tích.'),
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
        'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/10 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5
fr(5, 'Tạo mới phiếu điều chuyển vị trí',
   usecase=('FR-05', 'Tạo mới phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo mới phiếu điều chuyển vị trí (Lưu nháp / Lưu và tiếp tục)',
       mota='Lập phiếu chuyển hàng giữa các vị trí của 1 kho. Lập tay: chọn Kho (kho mình là thủ kho), bấm Thêm hàng hóa để chọn hàng còn '
            'tồn trong kho, rồi chọn ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập và nhập SL cho từng dòng (mục 2.6). Lập từ phiếu kiểm kê: Kho '
            'và các dòng chênh thiếu được nạp sẵn và khóa, chỉ chọn Vị trí nhập. Lưu nháp tạo phiếu Đang tạo, chưa đổi tồn; Điều chuyển '
            'đặc tả ở mục 2.8.',
       tacnhan=TN_LAP,
       dieukien='1. Người dùng đăng nhập thành công, có quyền “%s”.\n2. Người dùng là thủ kho của ít nhất 1 kho đang hoạt động (Super '
                'admin: mọi kho).\n3. Lập từ phiếu kiểm kê: phiếu kiểm kê còn dòng chênh thiếu chưa xử lý và người dùng có quyền xử lý '
                'phiếu kiểm kê đó.' % Q1,
       chinh='1. Người dùng bấm Tạo mới ở danh sách (hoặc Tạo phiếu điều chuyển vị trí ở phiếu kiểm kê).\n'
             '2. Hệ thống mở màn “Tạo phiếu điều chuyển vị trí”; góc phải khối Thông tin chung ghi người đăng nhập và giờ hiện tại.\n'
             '3. Người dùng chọn Kho, nhập Ghi chú, đính kèm file (không bắt buộc khi lưu nháp).\n'
             '4. Người dùng bấm Thêm hàng hóa, chọn hàng trong popup; hệ thống thêm mỗi hàng 1 dòng, ĐVT mặc định = ĐVT cơ sở, báo “Thêm '
             'thành công.”.\n'
             '5. Người dùng chọn Vị trí xuất, Lô xuất, Vị trí nhập, nhập SL cho từng dòng (mục 2.6); cột SL tồn hiện tồn lô tại vị trí xuất.\n'
             '6. Người dùng bấm Lưu nháp.\n'
             '7. Hệ thống kiểm tra định dạng (Ghi chú ≤ 255 ký tự, SL ≤ 999,999,999) và bắt buộc Kho; kiểm kho thuộc danh sách kho người '
             'dùng chọn được.\n'
             '8. Hệ thống sinh mã PĐCVT-NNNNN, lưu phiếu Đang tạo (công ty / phòng ban theo người lập), lưu các dòng hàng; lập từ phiếu '
             'kiểm kê theo hàng hóa thì phiếu kiểm kê chuyển Đang xử lý.\n'
             '9. Hệ thống ghi mốc “Tạo mới” trong lịch sử phiếu, hiển thị “Lưu thành công.” và về danh sách.',
       phu='• Bấm Lưu và tiếp tục (chỉ khi lập tay) → lưu nháp như trên rồi ở lại màn Tạo với form trống.\n'
           '• Chưa chọn Kho → viền đỏ, %s dưới ô Kho; thông báo %s.\n'
           '• Bấm Thêm hàng hóa khi chưa chọn Kho → %s dưới ô Kho, thông báo “Vui lòng chọn kho trước khi thêm hàng hóa.”.\n'
           '• Đổi Kho khi bảng đã có hàng → hộp “Đổi kho” %s; Đổi kho → xóa hết dòng; Hủy → giữ kho cũ.\n'
           '• Kho không phải kho mình là thủ kho (mở qua đường link) → %s dưới ô Kho: “Bạn không phải thủ kho của kho này.”.\n'
           '• Không có quyền Q1 → %s.\n'
           '• Bấm Quay lại khi đã nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì thì về danh sách ngay.'
           % (REQ, MISS, REQ, DOIKHO, REQ, NOPERM),
       dacbiet='Lưu nháp CHỈ bắt Kho (#11813, user chốt — hệ thống cũ bắt cả Ghi chú + ít nhất 1 hàng); các ô * khác chỉ bắt khi Điều '
               'chuyển. SL lưu nháp được làm tròn xuống số nguyên (giữ như hệ thống cũ). Phiếu không có trường nhập duy nhất, mã tự sinh theo '
               'thứ tự, không nhập tay; cho phép thêm trùng hàng (mỗi dòng 1 vị trí / lô khác nhau). Nút lưu khóa trong lúc lưu để một lần '
               'bấm không tạo 2 phiếu. File đính kèm: pdf, png, jpg, jpeg, tối đa 20 MB / file, tải lên ngay khi chọn.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới', 'Từ nút Tạo mới trên danh sách (có quyền Q1): form trống, lập tay.'),
       (MENU_KKVT + ' => Xem chi tiết phiếu kiểm kê => Tạo phiếu điều chuyển vị trí',
        'Hoặc từ danh sách / chi tiết phiếu Kiểm kê theo vị trí Chờ xử lý còn dòng chênh thiếu: form nạp sẵn Kho (kho đầu tiên của phiếu '
        'kiểm kê) + các dòng chênh thiếu, khóa ĐVT / Vị trí xuất / Lô xuất / SL.'),
       (MENU_KKHH + ' => Xem chi tiết phiếu kiểm kê => Tạo phiếu điều chuyển vị trí',
        'Hoặc từ chi tiết phiếu Kiểm kê theo hàng hóa đủ điều kiện: nạp sẵn như trên (SL = phần thiếu còn lại).')],
       shot=shot('10_create'), shot_caption='Màn Tạo phiếu điều chuyển vị trí lúc mới mở (lập tay)'),
   extra=[(shot('10c_filled'), 'Đã chọn Kho, thêm hàng và chọn vị trí / lô (danh sách kho chọn được giả trên trình duyệt)'),
          (shot('10b_validate'), 'Lỗi Kho khi Lưu nháp / Thêm hàng hóa lúc chưa chọn Kho (lỗi máy chủ gán trên trình duyệt)'),
          (shot('09_pkk_button'), 'Chi tiết phiếu Kiểm kê theo vị trí có nút Tạo phiếu điều chuyển vị trí'),
          (shot('10g_from_pkk'), 'Form Tạo lập từ phiếu kiểm kê TPE-KKVT-00142: dòng nạp sẵn, chỉ chọn Vị trí nhập'),
          (shot('10h_doikho'), 'Hộp Đổi kho khi bảng đã có hàng'),
          (shot('10e_unsaved'), 'Hộp Thông tin chưa lưu khi bấm Quay lại')],
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tạo phiếu điều chuyển vị trí”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', '- Góc phải khối Thông tin chung.'),
       ('Phiếu kiểm kê', 'Link', 'Read-only', '–', '–', 'Ẩn khi lập tay',
        ['- Chỉ hiện khi lập từ phiếu kiểm kê', '- Mã phiếu kiểm kê, bấm → mở phiếu kiểm kê ở tab mới']),
       ('Kho', 'Dropdown', 'Enable / Read-only', 'Kho mình là thủ kho', 'Có', 'Trống', [
           '- Gợi ý “Chọn kho”; lựa chọn “Mã kho - Tên kho”, chỉ kho đang hoạt động mình là thủ kho (Super admin: mọi kho)',
           '- Lập từ phiếu kiểm kê: ô khóa, hiện kho đầu tiên của phiếu kiểm kê', '- Lỗi: “Bắt buộc phải nhập”']),
       ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Có khi Điều chuyển', 'Trống',
        ['- Cao 1 dòng (kéo góc để giãn), gợi ý “Nhập ghi chú”, không gõ quá 255 ký tự',
         '- Nhãn luôn có dấu *, nhưng Lưu nháp được để trống', '- Lỗi: “Bắt buộc phải nhập” / “Vui lòng nhập tối đa 255 ký tự.”']),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, png, jpg, jpeg ≤ 20 MB', 'Có khi Điều chuyển', 'Trống',
        ['- Tiêu đề có dấu *; nút Thêm tài liệu → chọn file là tải lên ngay',
         '- Mỗi dòng: STT, tên file, xem trước, tải về, xóa, dung lượng', '- Lỗi: “Bắt buộc phải nhập”, sai định dạng / quá dung lượng']),
       ('Nút Thêm hàng hóa', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
        ['- Rê chuột: “Thêm hàng hóa còn tồn trong kho”', '- Ẩn khi lập từ phiếu kiểm kê', '- Bấm → popup Thêm hàng hóa (mục 2.6)']),
       ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', 'Có khi Điều chuyển', 'Không có dữ liệu', [
           '- Cột: STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT*, Vị trí xuất*, Lô xuất*, SL tồn, Vị trí nhập*, SL*, Hành động',
           '- ĐVT: ô chọn các ĐVT của hàng; Vị trí xuất / Lô xuất / Vị trí nhập: ô bấm mở popup (mục 2.6)',
           '- SL: số ≥ 0, tối đa 2 chữ số thập phân; SL tồn chữ đỏ khi SL > SL tồn',
           '- Hành động: nút Xóa dòng (thùng rác), xóa ngay không hỏi',
           '- Lập từ phiếu kiểm kê: ĐVT, Vị trí xuất, Lô xuất, SL khóa (chữ thường)', '- Rỗng: “Không có dữ liệu”']),
       ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Rê chuột: “Lưu nháp phiếu ở trạng thái Đang tạo”', '- Chỉ bắt Kho', '- Khóa trong lúc lưu']),
       ('Nút Điều chuyển', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Xem mục 2.8.'),
       ('Nút Lưu và tiếp tục', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
        ['- Chỉ ở màn Tạo khi lập tay', '- Rê chuột: “Lưu nháp (Đang tạo) rồi ở lại tạo phiếu tiếp theo”']),
       ('Nút In dự kiến', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Xem mục 2.10.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi “Thông tin chưa lưu”.'),
       ('Hộp “Đổi kho”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + DOIKHO, '- Nút Đổi kho, Hủy']),
       ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút Thoát: rời màn, không lưu', '- Nút Ở lại: giữ form']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Lưu thành công.”', '- Thiếu / sai dữ liệu: ' + MISS, '- Lỗi khác: “Lưu thất bại.”']),
   ],
   ev=[
       ('Mở màn Tạo mới', 'System',
        'Before:\n– Nút Tạo mới chỉ hiện khi có quyền Q1.\n'
        'During:\n– Nạp danh sách kho chọn được và người tạo; vào từ phiếu kiểm kê thì nạp kho + dòng chênh thiếu của phiếu đó; không '
        'có quyền Q1 / phiếu kiểm kê không còn lập được → chuyển trang “không tìm thấy”.\n'
        'After:\n– Hiển thị form; lập từ phiếu kiểm kê thì ẩn Thêm hàng hóa, Lưu và tiếp tục.'),
       ('Chọn / đổi Kho', 'Change',
        'Before:\n– Giá trị khác kho đang chọn.\n'
        'During:\n– Bảng đã có hàng → hộp “Đổi kho”; Hủy → giữ kho cũ.\n'
        'After:\n– Đổi kho: xóa hết dòng hàng và lỗi của bảng; xóa lỗi ô Kho.'),
       ('Bấm Thêm hàng hóa', 'Click',
        'Before:\n– Đã chọn Kho; chưa chọn → ' + REQ + ' dưới ô Kho + “Vui lòng chọn kho trước khi thêm hàng hóa.”.\n'
        'After:\n– Mở popup Thêm hàng hóa chỉ gồm hàng còn tồn trong kho (mục 2.6).'),
       ('Bấm Lưu nháp / Lưu và tiếp tục', 'Click',
        'Before:\n– Không có lượt lưu đang chạy; kiểm quyền Q1, không có → ' + NOPERM + ' và dừng xử lý.\n'
        'During:\n– Ghi chú > 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”; SL > 999,999,999 → “Giá trị nhập vào không được vượt quá '
        '999,999,999.”; SL âm → “Không được nhỏ hơn 0”.\n'
        '– Chưa chọn Kho → ' + REQ + ' dưới ô Kho, ' + MISS + '.\n'
        '– Kho không thuộc kho chọn được → “Bạn không phải thủ kho của kho này.”; Vị trí xuất = Vị trí nhập → ' + SAME_POS + '.\n'
        '– Lập từ phiếu kiểm kê: phiếu kiểm kê không còn lập được → ' + CONFLICT + '.\n' + ERR + '\n'
        'After:\n– Sinh phiếu PĐCVT-NNNNN trạng thái Đang tạo, lưu dòng hàng (chưa đổi tồn).\n'
        '– Ghi một dòng lịch sử “Tạo mới”.\n'
        '– Hiển thị “Lưu thành công.”; Lưu nháp → về danh sách; Lưu và tiếp tục → form trống.'),
       ('Bấm xóa dòng hàng', 'Click',
        'Before:\n– Dòng nằm trong bảng Chi tiết.\nAfter:\n– Xóa dòng ngay (không hỏi), đánh lại STT, bỏ lỗi của dòng đó.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– So dữ liệu hiện tại (kho, ghi chú, dòng hàng, file mới) với lúc mở.\n'
        'During:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát: về danh sách, không lưu; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn hàng hóa, vị trí và lô (popup)',
   usecase=('FR-06', 'Chọn hàng hóa, vị trí, lô', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown; Màn Thêm mới.', 'search'),
   intro=dict(
       ten='Chọn hàng hóa, vị trí xuất, lô xuất và vị trí nhập cho dòng hàng',
       mota='Bốn popup chọn dữ liệu dùng trên màn Tạo / Sửa: Thêm hàng hóa (popup chọn hàng dùng chung, chỉ hàng còn tồn trong kho của '
            'phiếu), Chọn vị trí xuất (vị trí của kho còn tồn hàng đó), Chọn lô xuất (lô của hàng còn tồn tại vị trí xuất) và Chọn vị trí '
            'nhập (mọi vị trí của kho). Vị trí đang kiểm kho, vị trí trùng với vị trí còn lại của dòng và lô hết hàng hiện mờ, không chọn '
            'được. Bấm vào dòng là chọn và đóng popup.',
       tacnhan=TN_LAP + ' Ở màn Sửa: người sửa được phiếu.',
       dieukien='1. Người dùng đang ở màn Tạo hoặc Sửa phiếu Đang tạo, đã chọn Kho.\n2. Dòng hàng chưa bị khóa (lập từ phiếu kiểm kê '
                'thì chỉ chọn được Vị trí nhập).',
       chinh='1. Người dùng bấm Thêm hàng hóa → popup “Thêm hàng hóa”; tick nhiều hàng rồi bấm Thêm (N), hoặc bấm tên hàng để chọn nhanh '
             '1 hàng.\n'
             '2. Hệ thống thêm mỗi hàng 1 dòng (ĐVT cơ sở), báo “Thêm thành công.”.\n'
             '3. Người dùng bấm ô Vị trí xuất → popup “Chọn vị trí xuất” liệt kê vị trí của kho còn tồn hàng (theo ĐVT của dòng), sắp tồn '
             'giảm dần; lọc theo Mã vị trí, Nhà, Dãy, Khoang; bấm dòng để chọn.\n'
             '4. Người dùng bấm ô Lô xuất → popup “Chọn lô xuất” liệt kê lô còn tồn tại vị trí xuất (Lô, Ngày nhập, Tồn); bấm dòng để chọn; '
             'hệ thống điền SL tồn.\n'
             '5. Người dùng bấm ô Vị trí nhập → popup “Chọn vị trí nhập” liệt kê mọi vị trí của kho; bấm dòng để chọn.\n'
             '6. Hệ thống điền mã vị trí / số lô vào dòng, xóa lỗi của ô vừa chọn.',
       phu='• Bấm Vị trí xuất khi dòng chưa có ĐVT → %s dưới ô ĐVT, không mở popup.\n'
           '• Bấm Lô xuất / Vị trí nhập khi chưa chọn Vị trí xuất → %s dưới ô Vị trí xuất.\n'
           '• Đổi Vị trí xuất sang vị trí khác → Lô xuất và SL tồn bị xóa, phải chọn lại lô.\n'
           '• Rê chuột dòng mờ → hiện lý do: “Đang kiểm kho”, “Trùng vị trí xuất / nhập” (popup vị trí) hoặc “Không có hàng hóa” (popup lô).\n'
           '• Không có kết quả → “Không có vị trí nào phù hợp.” / “Không có lô nào còn tồn tại vị trí xuất.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài popup → đóng, dòng không đổi.' % (REQ, NEED_FROM),
       dacbiet='Ô tìm vị trí chỉ tìm theo MÃ vị trí (#11812); Nhà → Dãy → Khoang lọc phân cấp, chọn là tìm ngay (#11811); popup vị trí rộng '
               'tối đa 1320 px, phân trang 10 / 20 / 50 / 100; cột Tồn sắp xếp được. Popup lô tìm theo số lô đang hiển thị (gồm tiền tố công '
               'ty), không phân biệt hoa / thường. Mỗi lần mở popup bộ lọc về trống.'),
   layout=dict(menu=MENU + ' => Tạo mới => Thêm hàng hóa', shot=shot('11_product_picker'), shot_caption='Popup Thêm hàng hóa',
               note='Các popup được mở ngay trên màn hình Tạo mới / Sửa phiếu theo đường dẫn ở trên.'),
   extra=[(shot('11b_position_picker'), 'Popup Chọn vị trí xuất (lọc Mã vị trí, Nhà, Dãy, Khoang)'),
          (shot('11c_lot_picker'), 'Popup Chọn lô xuất')],
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        ['- “Thêm hàng hóa”', '- “Chọn vị trí xuất” / “Chọn vị trí nhập”', '- “Chọn lô xuất”']),
       ('Popup Thêm hàng hóa', 'Popup', 'Enable', 'Hàng còn tồn trong kho', '–', 'Hiển thị', [
           '- Cây danh mục bên trái, ô tìm “Tìm theo mã, tên hàng hoá, model, barcode, mã đất hàng”, Tìm kiếm nâng cao, Làm mới',
           '- Bảng: STT, Ảnh, Mã hàng, Tên hàng hoá, Model, Thương hiệu, Loại sản phẩm, ĐVT, Tồn bán được, Hãng sản xuất, Xuất xứ',
           '- Tick nhiều hàng rồi bấm Thêm (N); bấm tên hàng để chọn nhanh 1 hàng', '- Cho thêm trùng hàng đã có']),
       ('Ô tìm theo mã vị trí', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo mã vị trí”', '- Khớp một phần mã vị trí', '- Áp khi bấm Tìm kiếm / Enter']),
       ('Nhà', 'Dropdown', 'Enable', 'Nhà của kho', 'Không', 'Trống', ['- Mặc định: trống', '- Chọn là tìm ngay']),
       ('Dãy', 'Dropdown', 'Enable', 'Dãy của Nhà đã chọn', 'Không', 'Trống',
        ['- Mặc định: trống', '- Chỉ còn dãy của Nhà đang lọc; đổi Nhà thì bỏ Dãy không thuộc Nhà']),
       ('Khoang', 'Dropdown', 'Enable', 'Khoang của Dãy đã chọn', 'Không', 'Trống',
        ['- Mặc định: trống', '- Chỉ còn khoang của Dãy (hoặc các dãy của Nhà) đang lọc']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Áp ô tìm, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Xóa ô tìm và Nhà / Dãy / Khoang, bỏ sắp xếp.'),
       ('Bảng Danh sách vị trí', 'Table/Grid', 'Enable', '–', '–', 'Theo kho', [
           '- Cột: STT, Vị trí, Nhà, Dãy, Khoang, Tồn (“<SL> <ĐVT>”, trống khi không có tồn)',
           '- Vị trí xuất: chỉ vị trí còn tồn hàng; Vị trí nhập: mọi vị trí của kho',
           '- Mặc định sắp Tồn giảm dần; cột Tồn sắp xếp được', '- Dòng mờ: “Đang kiểm kho” / “Trùng vị trí xuất / nhập”']),
       ('Ô tìm theo số lô', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số lô”', '- Khớp một phần số lô hiển thị, không phân biệt hoa / thường']),
       ('Bảng Danh sách lô', 'Table/Grid', 'Enable', '–', '–', 'Theo hàng + vị trí xuất', [
           '- Cột: STT, Lô, Ngày nhập (dd/mm/yyyy), Tồn (theo ĐVT, làm tròn xuống)',
           '- Mặc định lô nhập trước ở trên; cột Tồn sắp xếp được', '- Lô có Tồn 0 theo ĐVT: dòng mờ “Không có hàng hóa”']),
       ('Phân trang popup', 'Pagination', 'Enable', '10, 20, 50, 100', '–', '10',
        ['- Dòng “Hiển thị a–b / N”', '- Đổi số dòng → về trang 1']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Không có vị trí nào phù hợp.”', '- “Không có lô nào còn tồn tại vị trí xuất.”']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup, không chọn.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
   ],
   ev=[
       ('Mở popup Chọn vị trí xuất / nhập', 'Click',
        'Before:\n– Vị trí xuất: dòng đã có ĐVT, chưa có → ' + REQ + ' dưới ô ĐVT; Vị trí nhập: dòng đã có Vị trí xuất, chưa có → '
        + NEED_FROM + '.\n'
        'During:\n– Nạp Nhà / Dãy / Khoang của kho và danh sách vị trí kèm tồn của hàng; đánh dấu vị trí đang kiểm kho.\n'
        'After:\n– Hiển thị popup, bộ lọc trống, trang 1.'),
       ('Đổi Nhà / Dãy / Khoang', 'Change',
        'Before:\n– Đổi cấp trên thì bỏ cấp dưới không còn thuộc về nó.\nAfter:\n– Tìm lại ngay từ trang 1.'),
       ('Bấm một dòng vị trí', 'Click',
        'Before:\n– Dòng không mờ.\n'
        'After:\n– Điền mã vị trí vào ô; đổi Vị trí xuất khác vị trí cũ → bỏ Lô xuất, SL tồn; đóng popup.'),
       ('Mở popup Chọn lô xuất', 'Click',
        'Before:\n– Dòng đã có Vị trí xuất; chưa có → ' + NEED_FROM + '.\n'
        'During:\n– Nạp các lô còn tồn của hàng tại vị trí xuất (theo ĐVT).\nAfter:\n– Hiển thị popup, phân trang 10 dòng.'),
       ('Bấm một dòng lô', 'Click',
        'Before:\n– Lô có Tồn > 0.\nAfter:\n– Điền số lô, SL tồn (tồn lô tại vị trí xuất); đóng popup.'),
       ('Bấm Thêm (N) / tên hàng ở popup Thêm hàng hóa', 'Click',
        'Before:\n– Có ít nhất 1 hàng được chọn.\n'
        'During:\n– Nạp ĐVT của các hàng; lỗi → “Không tải được đơn vị tính của hàng hóa.”.\n'
        'After:\n– Thêm mỗi hàng 1 dòng, ĐVT cơ sở; báo “Thêm thành công.”; đóng popup.'),
       ('Bấm Đóng / (x) / click ra ngoài popup', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng popup, dòng hàng giữ nguyên.'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Chỉnh sửa phiếu',
   usecase=('FR-07', 'Chỉnh sửa phiếu', 'crud', A_LAP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'edit'),
   intro=dict(
       ten='Chỉnh sửa phiếu điều chuyển vị trí Đang tạo',
       mota='Sửa phiếu đang ở trạng thái Đang tạo: đổi Ghi chú, file đính kèm và bảng Chi tiết (thêm / xóa dòng, đổi ĐVT, vị trí, lô, SL); '
            'Kho giữ nguyên như lúc tạo. Lập từ phiếu kiểm kê thì các dòng nạp sẵn vẫn khóa, chỉ đổi Vị trí nhập. Lưu nháp giữ Đang tạo; '
            'Điều chuyển từ màn Sửa ghi tồn như khi tạo (mục 2.8).',
       tacnhan=TN_SUA,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu đang Đang tạo và nằm trong phạm vi xem của người dùng.',
       chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra điều kiện, mở màn “Sửa phiếu điều chuyển vị trí: <mã>” điền sẵn dữ liệu (cột SL tồn = tồn lô hiện tại '
             'tại vị trí xuất).\n'
             '3. Người dùng sửa Ghi chú, thêm / xóa file, sửa dòng hàng rồi bấm Lưu nháp.\n'
             '4. Hệ thống kiểm tra lại Đang tạo + phạm vi, kiểm định dạng như màn Tạo.\n'
             '5. Hệ thống lưu, ghi mốc “Thay đổi thông tin” (giá trị cũ → mới của Ghi chú / Chi tiết hàng hóa / File đính kèm), báo “Lưu '
             'thành công.” và về danh sách.',
       phu='• Phiếu không còn sửa được (đã chuyển / ngoài phạm vi) khi mở → tự chuyển về màn chi tiết (ngoài phạm vi: trang “không tìm thấy”).\n'
           '• Phiếu đổi trạng thái hoặc bị xóa trong lúc đang sửa → %s; không lưu.\n'
           '• Xóa file ĐÃ LƯU → hộp “Xác nhận xóa” (“Bạn có chắc muốn xóa file đính kèm này?”); bấm Xóa là gỡ file khỏi phiếu NGAY (không '
           'chờ Lưu), báo “Xóa file thành công”, ghi lịch sử.\n'
           '• Không đổi gì mà Lưu nháp → không phát sinh mốc thay đổi thông tin.\n'
           '• Bấm Quay lại khi có thay đổi → hộp “Thông tin chưa lưu”.' % CONFLICT,
       dacbiet='Màn Sửa không có Lưu và tiếp tục. Kho hiện ô khóa, không đổi được. Ghi chú ≤ 255 ký tự. Phiếu Đang tạo ai xem được cũng sửa '
               'được (giữ như hệ thống cũ — user chốt 19/10/2026). Lịch sử dòng hàng ghép cặp theo hàng + lần xuất hiện: xóa 1 dòng giữa '
               'bảng chỉ ra 1 dòng “đã xóa”.'),
   layout=dict(entries=[
       (MENU + ' => Sửa', 'Từ cột Hành động của dòng phiếu Đang tạo.'),
       (MENU + ' => Xem chi tiết => Sửa', 'Hoặc từ chân màn chi tiết phiếu Đang tạo.')],
       shot=shot('12_edit'), shot_caption='Màn Sửa phiếu điều chuyển vị trí PĐCVT-01235 (Đang tạo)'),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Sửa phiếu điều chuyển vị trí: <mã phiếu>”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu kiểm kê', 'Link', 'Read-only', '–', '–', 'Ẩn khi lập tay', '- Bấm → mở chi tiết phiếu kiểm kê ở tab mới.'),
       ('Kho', 'Textbox', 'Disable', '–', '–', 'Theo dữ liệu', '- “Mã kho - Tên kho”; không đổi được sau khi tạo.'),
       ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Có khi Điều chuyển', 'Theo dữ liệu', '- Quy tắc như mục 2.5.'),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, png, jpg, jpeg ≤ 20 MB', 'Có khi Điều chuyển (nếu phiếu chưa có file)',
        'File đã lưu', ['- Thêm file mới như mục 2.5', '- Xóa file đã lưu: hỏi “Xác nhận xóa”, gỡ ngay']),
       ('Nút Thêm hàng hóa', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Ẩn khi phiếu lập từ phiếu kiểm kê.'),
       ('Bảng Chi tiết', 'Table/Grid', 'Enable', '–', 'Có khi Điều chuyển', 'Dòng đã lưu',
        ['- Cùng cột, cùng cách nhập như mục 2.5', '- Dòng thiếu Vị trí xuất / Lô xuất hiện ô trống “Chọn …”']),
       ('Nút Lưu nháp', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Lưu, giữ Đang tạo.'),
       ('Nút Điều chuyển', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Xem mục 2.8.'),
       ('Nút In dự kiến', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Xem mục 2.10 (in kèm mã phiếu).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Lưu thành công.”', '- ' + CONFLICT, '- “Xóa file thành công” / “Xóa file thất bại”', '- ' + MISS]),
   ],
   ev=[
       ('Mở màn Sửa', 'System',
        'Before:\n– Phiếu trong phạm vi xem; ngoài phạm vi / không tồn tại → trang “không tìm thấy”.\n'
        'During:\n– Phiếu không còn Đang tạo → chuyển về màn chi tiết.\n'
        'After:\n– Hiển thị form điền sẵn; Kho khóa.'),
       ('Bấm Lưu nháp', 'Click',
        'Before:\n– Kiểm tra Đang tạo + phạm vi; không đạt → ' + CONFLICT + ' / ' + NOPERM + ' và dừng xử lý.\n'
        'During:\n– Ghi chú > 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.”; SL vượt trần / âm → câu lỗi dưới ô SL; Vị trí xuất = nhập '
        '→ ' + SAME_POS + '.\n– Dòng lập từ phiếu kiểm kê đã được xử lý → ' + SRC_ROW_ERR + '\n' + ERR + '\n'
        'After:\n– Lưu Ghi chú, file mới, thay toàn bộ dòng hàng nháp; ghi lịch sử “Thay đổi thông tin” nếu có thay đổi; “Lưu thành '
        'công.”, về danh sách.'),
       ('Bấm xóa file đã lưu → Xóa', 'Click',
        'Before:\n– Hộp “Xác nhận xóa”; phiếu còn Đang tạo, không → ' + CONFLICT + '.\n'
        'After:\n– Gỡ file khỏi phiếu, ghi lịch sử, báo “Xóa file thành công”.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– So dữ liệu với lúc mở.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát: về danh sách; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'Điều chuyển (ghi tồn kho)',
   usecase=('FR-08', 'Điều chuyển', 'action', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Điều chuyển hàng sang vị trí nhập',
       mota='Từ màn Tạo hoặc Sửa, người dùng bấm Điều chuyển: hệ thống lưu phiếu ở trạng thái Đã chuyển và ghi tồn ngay cho từng dòng — '
            'trừ tồn lô tại vị trí xuất, cộng cùng lô tại vị trí nhập (tổng tồn của kho không đổi), ghi Thẻ kho; lập từ phiếu kiểm kê thì '
            'cộng phần đã xử lý vào dòng kết quả kiểm kê. Sau khi điều chuyển phiếu không sửa, không xóa được.',
       tacnhan='Người dùng có quyền thực hiện chức năng: %s (từ màn Tạo); người sửa được phiếu Đang tạo (từ màn Sửa).' % Q1,
       dieukien='1. Đang ở màn Tạo (đủ điều kiện mục 2.5) hoặc Sửa (phiếu Đang tạo trong phạm vi xem).\n'
                '2. Đã nhập Ghi chú, có ít nhất 1 dòng đủ ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập, SL và có ít nhất 1 file đính kèm.',
       chinh='1. Người dùng bấm Điều chuyển.\n'
             '2. Hệ thống hiện hộp “Xác nhận điều chuyển”: %s.\n'
             '3. Người dùng bấm Điều chuyển trong hộp.\n'
             '4. Hệ thống kiểm tra bắt buộc cùng một lượt: Kho, Ghi chú, ít nhất 1 dòng, từng dòng ĐVT / Vị trí xuất / Lô xuất / Vị trí '
             'nhập / SL, File đính kèm; Vị trí xuất ≠ Vị trí nhập.\n'
             '5. Hệ thống kiểm hàng / vị trí đang kiểm kho, vị trí thuộc kho của phiếu, ĐVT thuộc hàng, rồi kiểm tồn: tổng SL (quy về ĐVT cơ '
             'sở) theo hàng + vị trí + lô ≤ tồn lô tại vị trí; theo hàng + vị trí ≤ tồn vị trí trừ SL phiếu nhập kho chưa hạch toán.\n'
             '6. Hệ thống lưu phiếu Đã chuyển, ghi các dòng chi tiết; với từng dòng chuyển tồn từ vị trí xuất sang vị trí nhập theo lô '
             '(theo công ty của lô) và ghi Thẻ kho.\n'
             '7. Lập từ phiếu kiểm kê: cộng SL đã chuyển vào phần đã xử lý của dòng kết quả kiểm kê; xử lý hết thì phiếu Kiểm kê theo vị trí '
             '→ Hoàn thành (kế hoạch cha → Hoàn thành), phiếu Kiểm kê theo hàng hóa → Hoàn thành, còn việc thì Đang xử lý.\n'
             '8. Hệ thống ghi lịch sử (Tạo mới khi điều chuyển từ màn Tạo; “Thay đổi trạng thái” Đang tạo → Đã chuyển khi từ màn Sửa), '
             'báo “Điều chuyển thành công.” và về danh sách.' % CONFIRM_TF,
       phu='• Bấm Hủy / (x) trong hộp → đóng hộp, không lưu, form giữ nguyên.\n'
           '• Thiếu dữ liệu → viền đỏ, %s dưới đúng ô / đúng dòng / khối file, thông báo %s.\n'
           '• Hàng / vị trí đang kiểm kho hoặc vị trí khác kho → %s.\n'
           '• Vượt tồn → %s; không lưu, không trừ dòng nào.\n'
           '• Phiếu đã đổi trạng thái (từ màn Sửa) → %s.' % (REQ, MISS, LOCK_ERR, STOCK_ERR, CONFLICT),
       dacbiet='Điều chuyển KHÔNG hoàn tác được trên màn. Toàn bộ lưu + ghi tồn trong một lần lưu trọn gói: lỗi ở bất kỳ dòng nào thì không '
               'ghi gì. Phiếu sửa từ nháp đã có file thì không bắt thêm file. Không gửi thông báo cho ai. Cột SL tồn đỏ chỉ là cảnh báo trên '
               'form; chặn thật ở máy chủ khi Điều chuyển.'),
   layout=dict(menu=MENU + ' => Tạo mới => Nút Điều chuyển', shot=shot('10f_confirm_transfer'),
               shot_caption='Hộp Xác nhận điều chuyển (bấm Hủy để chụp, không điều chuyển)'),
   extra=[(shot('10d_validate_transfer'), 'Lỗi thiếu dữ liệu khi Điều chuyển (câu lỗi máy chủ gán trên trình duyệt)')],
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Điều chuyển (chân màn)', 'Button', 'Enable / Disable', 'Hiển thị',
        ['- Rê chuột: “Điều chuyển hàng sang vị trí nhập (ghi tồn kho, không hoàn tác)”', '- Khóa trong lúc lưu']),
       ('Hộp “Xác nhận điều chuyển”', 'Popup', 'Hiển thị', 'Ẩn', '- ' + CONFIRM_TF),
       ('Nút Điều chuyển (trong hộp)', 'Button', 'Enable', 'Hiển thị', '- Thực hiện lưu + ghi tồn.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống Hủy.'),
       ('Lỗi tại ô', 'Label', 'Hiển thị', 'Ẩn',
        ['- Kho, Ghi chú, khối File đính kèm, bảng Chi tiết (viền đỏ): “Bắt buộc phải nhập”',
         '- Từng dòng: ĐVT / Vị trí xuất / Lô xuất / Vị trí nhập / SL “Bắt buộc phải nhập”', '- Vị trí nhập: ' + SAME_POS]),
       ('Lỗi kiểm kho / tồn tại dòng', 'Label', 'Hiển thị', 'Ẩn', ['- ' + LOCK_ERR, '- ' + STOCK_ERR]),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn',
        ['- Thành công: “Điều chuyển thành công.”', '- Thiếu dữ liệu: ' + MISS, '- Lỗi khác: “Lưu thất bại.”']),
       ('Trạng thái sau điều chuyển', 'Badge', 'Read-only', 'Đã chuyển',
        '- Nhãn xanh lá “Đã chuyển”; nút Sửa, Xóa biến mất, nút In xuất hiện.'),
   ],
   ev=[
       ('Bấm Điều chuyển (chân màn)', 'Click',
        'Before:\n– Không có lượt lưu đang chạy; kiểm định dạng (Ghi chú ≤ 255, SL ≤ 999,999,999).\n'
        'After:\n– Hiện hộp “Xác nhận điều chuyển”.'),
       ('Bấm Điều chuyển trong hộp', 'Click',
        'Before:\n– Từ màn Tạo: kiểm quyền Q1, không có → ' + NOPERM + '; từ màn Sửa: Đang tạo + phạm vi, không đạt → ' + CONFLICT
        + ', dừng xử lý.\n'
        'During:\n– Thiếu Kho / Ghi chú / dòng / cột của dòng / file → ' + REQ + ', ' + MISS + '.\n'
        '– Vị trí trùng → ' + SAME_POS + '; ' + LOCK_ERR + '; ĐVT không thuộc hàng → “Không thuộc hàng hóa này.”.\n'
        '– ' + STOCK_ERR + '.\n' + ERR + '\n'
        'After:\n– Phiếu → Đã chuyển; chuyển tồn lô từ vị trí xuất sang vị trí nhập, ghi Thẻ kho; cập nhật phiếu kiểm kê nguồn.\n'
        '– Ghi một dòng lịch sử (Tạo mới hoặc Thay đổi trạng thái).\n'
        '– Hiển thị “Điều chuyển thành công.”, về danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nAfter:\n– Đóng hộp; form giữ nguyên, không lưu.'),
       ('Lỗi tại dòng sau khi máy chủ kiểm', 'System',
        'Before:\n– Máy chủ trả lỗi theo từng dòng.\nAfter:\n– Hiện lỗi dưới đúng ô của dòng, cuộn tới lỗi đầu tiên; nếu lỗi không có ô '
        'hiển thị thì đưa nguyên câu lên thông báo.'),
   ])

# ------------------------------------------------------------ 2.9
fr(9, 'Xóa phiếu',
   usecase=('FR-09', 'Xóa phiếu', 'action', A_LAP),
   rule=('- Quy tắc Xóa và Thông báo.', 'delete'),
   intro=dict(
       ten='Xóa phiếu điều chuyển vị trí Đang tạo',
       mota='Xóa hẳn một phiếu Đang tạo (phiếu và các dòng hàng nháp). Phiếu Đã chuyển không có nút Xóa vì tồn đã ghi. Phiếu nháp chưa ghi '
            'tồn nên xóa không ảnh hưởng tồn kho, Thẻ kho hay phiếu kiểm kê nguồn.',
       tacnhan=TN_SUA,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu đang Đang tạo và nằm trong phạm vi xem.',
       chinh='1. Người dùng bấm Xóa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa”: “Bạn có chắc muốn xóa bản ghi này không?”.\n'
             '3. Người dùng bấm Xóa trong hộp.\n'
             '4. Hệ thống kiểm tra phiếu còn Đang tạo và trong phạm vi.\n'
             '5. Hệ thống ghi mốc xóa vào lịch sử, xóa dòng hàng nháp, dòng chi tiết và phiếu.\n'
             '6. Hệ thống báo “Xóa thành công.”; ở danh sách nạp lại, ở màn chi tiết quay về danh sách.',
       phu='• Bấm Hủy / (x) → đóng hộp, không xóa.\n'
           '• Phiếu đã điều chuyển / đã bị xóa bởi người khác → báo %s hoặc “không tìm thấy”, không xóa.\n'
           '• Lỗi khác → “Xóa thất bại.”.' % CONFLICT,
       dacbiet='Xóa cứng, không khôi phục được. Không có ràng buộc dữ liệu con chặn xóa (phiếu nháp chưa được dùng ở màn khác). Phiếu Đang '
               'tạo ai xem được cũng xóa được (giữ như hệ thống cũ). Tổng số trên danh sách giảm 1 sau khi xóa.'),
   layout=dict(entries=[
       (MENU + ' => Xóa', 'Từ cột Hành động của dòng phiếu Đang tạo.'),
       (MENU + ' => Xem chi tiết => Xóa', 'Hoặc từ chân màn chi tiết phiếu Đang tạo.')],
       shot=shot('13_delete'), shot_caption='Hộp Xác nhận xóa (bấm Hủy để chụp, không xóa)'),
   extra=[(shot('17b_detail_draft'), 'Màn chi tiết phiếu Đang tạo có nút Sửa, Xóa')],
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Xóa (dòng)', 'Icon Button', 'Enable / Ẩn', 'Theo điều kiện', ['- Thùng rác đỏ, rê chuột “Xóa”', '- Chỉ phiếu Đang tạo']),
       ('Nút Xóa (màn chi tiết)', 'Button', 'Enable / Ẩn', 'Theo điều kiện', '- Nút đỏ ở chân màn, chỉ phiếu Đang tạo.'),
       ('Hộp “Xác nhận xóa”', 'Popup', 'Hiển thị', 'Ẩn', '- Nội dung “Bạn có chắc muốn xóa bản ghi này không?”.'),
       ('Nút Xóa (trong hộp)', 'Button', 'Enable', 'Hiển thị', '- Nút đỏ, thực hiện xóa.'),
       ('Nút Hủy', 'Button', 'Enable', 'Hiển thị', '- Đóng hộp, không xóa.'),
       ('Nút (x)', 'Icon Button', 'Enable', 'Hiển thị', '- Giống Hủy.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', 'Ẩn', ['- “Xóa thành công.”', '- ' + CONFLICT, '- “Xóa thất bại.”']),
   ],
   ev=[
       ('Bấm Xóa (dòng / màn chi tiết)', 'Click',
        'Before:\n– Nút chỉ hiện với phiếu Đang tạo trong phạm vi.\nAfter:\n– Hiện hộp “Xác nhận xóa”.'),
       ('Bấm Xóa trong hộp', 'Click',
        'Before:\n– Kiểm tra phiếu tồn tại, trong phạm vi (không → “không tìm thấy”), còn Đang tạo (không → ' + CONFLICT + ').\n'
        'During:\n– Khóa phiếu trong lúc xóa.\n' + ERR + '\n'
        'After:\n– Ghi mốc xóa vào lịch sử; xóa dòng hàng và phiếu.\n– Hiển thị “Xóa thành công.”; danh sách nạp lại / về danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nAfter:\n– Đóng hộp, phiếu giữ nguyên.'),
       ('Xóa lỗi', 'System', 'Before:\n– Máy chủ lỗi.\nAfter:\n– Hiển thị “Xóa thất bại.” (hoặc câu máy chủ trả), phiếu giữ nguyên.'),
   ])

# ------------------------------------------------------------ 2.10
fr(10, 'In dự kiến',
   usecase=('FR-10', 'In dự kiến', 'io', A_LAP),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In dự kiến phiếu điều chuyển vị trí theo dữ liệu đang nhập',
       mota='Từ màn Tạo / Sửa, xem trước và in bản “dự kiến” theo đúng dữ liệu đang nhập trên form (chưa cần lưu) để thủ kho mang đi '
            'chuyển hàng: dùng mẫu in của phiếu, thêm cột Ghi chú trống để ghi tay. Không ghi dữ liệu.',
       tacnhan='Người dùng đang ở màn Tạo / Sửa phiếu.',
       dieukien='1. Đang ở màn Tạo hoặc Sửa.\n2. Đã chọn Kho, nhập Ghi chú, có ít nhất 1 dòng đủ ĐVT, Vị trí xuất, Lô xuất (Vị trí nhập, SL '
                'không bắt buộc).',
       chinh='1. Người dùng bấm In dự kiến.\n'
             '2. Hệ thống kiểm Kho, Ghi chú, ≥ 1 dòng, ĐVT / Vị trí xuất / Lô xuất của từng dòng.\n'
             '3. Hệ thống mở cửa sổ “Xem trước phiếu dự kiến điều chuyển vị trí”, dựng bản in theo dữ liệu đang nhập: màn Sửa in kèm Số '
             'phiếu và ngày tạo phiếu; màn Tạo để trống Số phiếu, ngày = hôm nay, người lập = người đang đăng nhập.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Thiếu dữ liệu → viền đỏ %s dưới ô / dòng, thông báo %s; không mở cửa sổ.\n'
           '• Máy chủ báo lỗi dữ liệu → cửa sổ hiện %s, lỗi hiện dưới từng ô.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in phiếu điều chuyển vị trí.”; lỗi khác → “Không tải được bản in.”.\n'
           '• Bấm (x) → đóng cửa sổ, form giữ nguyên.' % (REQ, MISS, MISS),
       dacbiet='Dùng chung mẫu in của hệ thống cũ (tiêu đề in “KIỂM KÊ KHO”, dòng “Ngày kiểm kê”); bảng dự kiến: STT, Hàng hóa (tên + Model '
               '+ Mã hàng), ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập, SL, Ghi chú. Letterhead: công ty của phiếu (màn Sửa) hoặc công ty người '
               'đang lập (màn Tạo). Khối ký: Người lập phiếu, Thủ kho, Trưởng phòng (có khoảng trống ký).'),
   layout=dict(menu=MENU + ' => Tạo mới => In dự kiến', shot=shot('18b_print_expect'),
               shot_caption='Cửa sổ Xem trước phiếu dự kiến điều chuyển vị trí',
               note='Modal Xem trước được mở ngay trên màn hình Tạo mới / Sửa phiếu theo đường dẫn ở trên.'),
   extra=[(shot('12c_validate_expect'), 'In dự kiến ở màn Sửa khi thiếu Ghi chú, dòng 2 thiếu Vị trí xuất / Lô xuất')],
   ui_kw=dict(required=False),
   ui=[
       ('Nút In dự kiến', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xem trước bản in dự kiến theo dữ liệu đang nhập”', '- Khóa trong lúc dựng bản in']),
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Xem trước phiếu dự kiến điều chuyển vị trí”.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → hộp thoại in của trình duyệt.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Logo, tên, địa chỉ công ty', '- Tiêu đề “KIỂM KÊ KHO”, “No:” (Số phiếu)']),
       ('Thông tin phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu', ['- Ngày kiểm kê (ngày tạo / hôm nay)', '- Kho', '- Ghi chú']),
       ('Bảng dự kiến', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        '- STT, Hàng hóa, ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập, SL, Ghi chú (trống).'),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- Người lập phiếu (họ tên), Thủ kho, Trưởng phòng.'),
       ('Lỗi tại ô', 'Label', 'Hiển thị', '–', 'Ẩn', '- Kho, Ghi chú, bảng, ĐVT / Vị trí xuất / Lô xuất: “Bắt buộc phải nhập”.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', ['- ' + MISS, '- “Không tải được bản in.”']),
   ],
   ev=[
       ('Bấm In dự kiến', 'Click',
        'Before:\n– Không có lượt in đang chạy.\n'
        'During:\n– Thiếu Kho / Ghi chú / dòng / ĐVT / Vị trí xuất / Lô xuất → ' + REQ + ', ' + MISS + '.\n' + ERR + '\n'
        'After:\n– Mở cửa sổ, dựng bản in dự kiến; không ghi dữ liệu.'),
       ('Bấm In trong cửa sổ', 'Click', 'Before:\n– Bản in đã dựng xong.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, form giữ nguyên dữ liệu đang nhập.'),
       ('Đang dựng bản in', 'System', 'Before:\n– Vừa bấm In dự kiến.\nAfter:\n– Hiện trạng thái đang tải tới khi có bản in.'),
   ])

# ------------------------------------------------------------ 2.11
fr(11, 'Xem chi tiết phiếu', usecase=('FR-11', 'Xem chi tiết phiếu', 'view', A_XEM),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu điều chuyển vị trí',
       mota='Màn chỉ đọc hiển thị Thông tin chung (Phiếu kiểm kê nếu có, Kho, Ghi chú), File đính kèm, bảng Chi tiết và khối Lịch sử. Tiêu '
            'đề trang ghi mã phiếu (không gắn nhãn trạng thái). Chân màn có Sửa, Xóa (phiếu Đang tạo), In (phiếu Đã chuyển) và Quay lại.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu tồn tại và nằm trong phạm vi xem.',
       chinh='1. Người dùng bấm Mã phiếu ở danh sách (hoặc số chứng từ ở Thẻ kho).\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết phiếu điều chuyển vị trí: <mã>”.\n'
             '4. Hệ thống hiển thị các khối và khối Lịch sử (thu gọn).',
       phu='• Phiếu ngoài phạm vi / không tồn tại → chuyển sang trang “không tìm thấy” (404), không báo lỗi nổi.\n'
           '• Máy chủ lỗi → “Không tải được dữ liệu.”.\n'
           '• Phiếu không có file → khối File đính kèm ghi “Không có file đính kèm.”.\n'
           '• Bấm mã phiếu kiểm kê → mở ở tab mới; bấm Quay lại → về danh sách, khôi phục bộ lọc (10 phút).',
       dacbiet='Bảng Chi tiết ở màn chi tiết không có cột SL tồn, Hành động và tự co vừa khung. Số hiển thị dạng 1,234.5. Phiếu Đã chuyển '
               'đọc dòng đã ghi tồn; phiếu Đang tạo đọc dòng nháp (có thể thiếu vị trí / lô).'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết phiếu điều chuyển vị trí (Đã chuyển)'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Chi tiết phiếu điều chuyển vị trí: <mã>”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu kiểm kê', 'Link', 'Read-only', '–', 'Ẩn khi lập tay', '- Bấm → mở chi tiết phiếu kiểm kê ở tab mới.'),
       ('Kho', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- “Mã kho - Tên kho”.'),
       ('Ghi chú', 'Textarea', 'Disable', '0–255 ký tự', 'Theo dữ liệu', '- Chỉ đọc.'),
       ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, tên file, xem trước, tải về, dung lượng', '- Không có file: “Không có file đính kèm.”']),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        '- STT, Tên hàng hóa, Model, Mã hàng hóa, ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập, SL; rỗng: “Không có dữ liệu”.'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút Xem lịch sử mở rộng; nội dung như mục 2.14.'),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Phiếu Đang tạo → mục 2.7.'),
       ('Nút Xóa', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Phiếu Đang tạo → mục 2.9.'),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Theo điều kiện', '- Phiếu Đã chuyển → mục 2.12.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về danh sách.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem; không đạt → trang “không tìm thấy”, dừng xử lý.\n'
        'During:\n– Lấy dữ liệu phiếu, file, dòng hàng, cờ nút; lỗi khác → “Không tải được dữ liệu.”.\n'
        'After:\n– Hiển thị màn chỉ đọc.'),
       ('Bấm Xem lịch sử', 'Click', 'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở rộng khối, nạp các mốc lịch sử.'),
       ('Bấm mã Phiếu kiểm kê', 'Click', 'Before:\n– Có phiếu kiểm kê.\nAfter:\n– Mở chi tiết phiếu kiểm kê ở tab mới.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Không có dữ liệu cần lưu.\nAfter:\n– Về danh sách, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.12
fr(12, 'In phiếu', usecase=('FR-12', 'In phiếu', 'io', A_XEM),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu điều chuyển vị trí đã chuyển',
       mota='Xem trước và in một phiếu Đã chuyển theo mẫu in của phiếu (bản không có cột Ghi chú). Bản in mở trong cửa sổ ngay trên màn đang '
            'đứng (danh sách hoặc chi tiết), không mở tab mới nên không mất bộ lọc.',
       tacnhan=TN, dieukien=DK + '\n4. Phiếu ở trạng thái Đã chuyển.',
       chinh='1. Người dùng bấm In ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem và trạng thái Đã chuyển.\n'
             '3. Hệ thống mở cửa sổ “Xem trước phiếu điều chuyển vị trí <mã>”, dựng bản in.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Phiếu ngoài phạm vi → cửa sổ báo %s.\n'
           '• Phiếu chưa điều chuyển (mở qua đường link) → “Chỉ in được phiếu đã điều chuyển.”.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in phiếu điều chuyển vị trí.”; lỗi khác → “Không tải được dữ liệu in”.\n'
           '• Bấm (x) → đóng cửa sổ, màn giữ nguyên.' % NOTFOUND,
       dacbiet='Logo / tên / địa chỉ công ty đầu bản in lấy theo công ty ghi trên phiếu (công ty người lập), không theo người đang xem. Mẫu '
               'in dùng chung với hệ thống cũ: tiêu đề “KIỂM KÊ KHO”, “No: <mã phiếu>”, “Ngày kiểm kê” = ngày tạo phiếu.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu điều chuyển vị trí',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Xem trước phiếu điều chuyển vị trí <mã phiếu>”.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → hộp thoại in của trình duyệt.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ xem trước.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- Hiện trong lúc dựng bản in.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Logo, tên, địa chỉ công ty của phiếu', '- Tiêu đề “KIỂM KÊ KHO”, “No: <mã phiếu>”']),
       ('Thông tin phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Ngày kiểm kê (ngày tạo phiếu), Kho, Ghi chú.'),
       ('Bảng hàng', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        '- STT, Hàng hóa (tên + Model + Mã hàng), ĐVT, Vị trí xuất, Lô xuất, Vị trí nhập, SL.'),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- Người lập phiếu (họ tên người tạo), Thủ kho, Trưởng phòng.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- ' + NOTFOUND, '- “Chỉ in được phiếu đã điều chuyển.”', '- “Không tải được dữ liệu in”']),
   ],
   ev=[
       ('Bấm In (dòng / màn chi tiết)', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → ' + NOTFOUND + '; chưa Đã chuyển → “Chỉ in được phiếu đã điều chuyển.”.\n'
        'During:\n– Dựng bản in theo dữ liệu đã ghi; lỗi → “Không tải được dữ liệu in”.\n'
        'After:\n– Hiển thị bản xem trước, letterhead theo công ty của phiếu.'),
       ('Bấm In trong cửa sổ xem trước', 'Click', 'Before:\n– Bản in đã dựng xong.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, giữ nguyên màn đang đứng.'),
       ('Đang dựng bản in', 'System', 'Before:\n– Vừa bấm In.\nAfter:\n– Hiện trạng thái đang tải tới khi có bản in.'),
   ])

# ------------------------------------------------------------ 2.13
fr(13, 'Xuất danh sách ra Excel', usecase=('FR-13', 'Xuất Excel', 'io', A_XEM),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất toàn bộ phiếu khớp bộ lọc trong phạm vi xem (không phân trang) ra file Excel. Cột STT luôn '
            'đứng đầu; đầu file có letterhead công ty người xuất, tiêu đề và dòng khoảng ngày (nếu lọc Ngày tạo), cuối file có khối ký.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 8 trường, tích sẵn các trường ứng với cột đang hiện.\n'
             '3. Người dùng tích trường, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy toàn bộ phiếu theo bộ lọc, dựng file theo thứ tự trường đã chọn.\n'
             '5. Hệ thống tải file “danh_sach_phieu_dieu_chuyen_vi_tri.xlsx”, báo “Xuất Excel thành công.”.',
       phu='• Không có phiếu khớp → VẪN tạo file chỉ có tiêu đề và dòng tên cột, báo “Xuất Excel thành công.”.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel.”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng. Tiêu đề file “DANH SÁCH PHIẾU ĐIỀU CHUYỂN VỊ TRÍ”, trang tính “Điều chuyển vị trí”; dòng “Từ ngày … '
               'đến ngày …” khi có lọc Ngày tạo.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 8 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        '- Mã phiếu, Ngày tạo, Kho, Phiếu kiểm kê, Trạng thái, Người tạo, Ngày cập nhật, Người cập nhật.'),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/8 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file Excel', '- Khóa khi chưa tích trường nào hoặc đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('Nội dung file Excel', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Letterhead công ty người xuất, tiêu đề “DANH SÁCH PHIẾU ĐIỀU CHUYỂN VỊ TRÍ”',
         '- Dòng “Từ ngày … đến ngày …” khi lọc Ngày tạo', '- Dòng tên cột: STT + các trường đã chọn', '- Khối ký cuối file']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Xuất Excel thành công.”', '- “Lỗi khi xuất Excel.”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không có lượt xuất đang chạy.\nAfter:\n– Mở cửa sổ, tích sẵn trường ứng với cột đang hiện.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Kéo bằng biểu tượng của trường.\nAfter:\n– Đổi thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất; dữ liệu theo phạm vi xem + bộ lọc.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc (không phân trang) và letterhead công ty người xuất.\n'
        '– Lỗi → “Lỗi khi xuất Excel.”.\n' + ERR + '\n'
        'After:\n– Tải file, báo “Xuất Excel thành công.” (kể cả khi 0 dòng).'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.14
fr(14, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu',
       mota='Xem các mốc thao tác của phiếu: người thực hiện, thời điểm, hành động, giá trị cũ → mới. Phiếu có các loại mốc: “Tạo mới”, '
            '“Thay đổi thông tin” (Ghi chú, Chi tiết hàng hóa — dòng thêm mới / đã xóa / sửa thông tin, File đính kèm) và “Thay đổi trạng '
            'thái” (Đang tạo → Đã chuyển khi điều chuyển từ màn Sửa). Cửa sổ ở danh sách và khối Lịch sử ở màn chi tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động, hoặc Xem lịch sử ở khối Lịch sử màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem, mở cửa sổ “Lịch sử thay đổi: <mã phiếu>” và nạp các mốc.\n'
             '3. Hệ thống hiển thị các mốc, mới nhất ở trên.',
       phu='• Phiếu lập ở hệ thống cũ chưa có mốc → hiện trạng thái chưa có lịch sử.\n'
           '• Bấm Bộ lọc → mở các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Phiếu ngoài phạm vi → không mở được (không tìm thấy).\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Xem, in, in dự kiến, xuất Excel không ghi mốc. Lưu nháp không đổi gì thì không ghi mốc. Điều chuyển ngay từ màn Tạo chỉ có mốc '
               '“Tạo mới”. Dòng hàng sửa ghi “Tên hàng: trường cũ → mới” (không kèm phụ chú vị trí / lô). Mốc trạng thái của PHIẾU KIỂM KÊ '
               'nguồn ghi ở lịch sử phiếu kiểm kê (ghi chú “Phiếu điều chuyển vị trí <mã>.”), không lặp ở đây.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi của PĐCVT-01234',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('16c_history_filter'), 'Khối Bộ lọc trong cửa sổ Lịch sử thay đổi'),
          (shot('17c_detail_history'), 'Khối Lịch sử ở màn chi tiết phiếu')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <mã phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái: “Trạng thái: Đang tạo → Đã chuyển”',
           '- Thay đổi thông tin: Ghi chú cũ → mới; “Chi tiết hàng hóa thêm mới / đã xóa / sửa thông tin”; File đính kèm',
           '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Trống',
        ['- Lựa chọn: Tạo mới / Thay đổi thông tin / Thay đổi trạng thái', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', '- “Họ tên - Mã phòng - Mã nhân viên”; chọn là lọc ngay.'),
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
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu điều chuyển vị trí; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi xem', [
        '– V1 / Super admin: mọi phiếu; V2: phiếu có công ty = công ty đang làm việc + phiếu mình tạo; V3: phiếu của kho mình là thủ kho '
        '+ phiếu mình tạo; không có quyền: phiếu mình tạo. Ưu tiên V1 > V2 > V3.',
        '– Chi tiết / Sửa / Xóa / In / Lịch sử áp cùng phạm vi; ngoài phạm vi → trang 404. Menu không gắn quyền.'],
     ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel', 'Lịch sử']),
    ('BR-02', 'Điều kiện lập phiếu', [
        '– Cần quyền “%s”. Kho phải đang hoạt động và người lập là thủ kho của kho (Super admin: mọi kho); sai → “Bạn không phải thủ kho '
        'của kho này.”.' % Q1,
        '– Lập từ phiếu Kiểm kê theo vị trí: phiếu Chờ xử lý, người lập có quyền xử lý phiếu kiểm kê vị trí, còn dòng chênh thiếu chưa '
        'xử lý; kho = kho đầu tiên của phiếu kiểm kê.',
        '– Lập từ phiếu Kiểm kê theo hàng hóa: phiếu Chờ / Đang xử lý, quyền xử lý phiếu kiểm kê hàng hóa, còn dòng cần điều chuyển, '
        'chưa có phiếu điều chuyển nào lập từ phiếu đó.'], ['Tạo mới']),
    ('BR-03', 'Dòng hàng', [
        '– Lập tay: chỉ hàng còn tồn trong kho; cho trùng hàng; ĐVT mặc định = ĐVT cơ sở.',
        '– Lập từ phiếu kiểm kê: dòng = dòng kết quả chênh THIẾU chưa xử lý (SL = |chênh lệch| − đã xử lý), vị trí xuất / lô theo dòng '
        'kết quả; ĐVT, Vị trí xuất, Lô xuất, SL khóa, máy chủ lấy lại khi lưu; dòng đã xử lý → “Đã được xử lý hoặc không thuộc phiếu '
        'kiểm kê. Vui lòng tải lại trang.”.'], ['Tạo mới', 'Chỉnh sửa']),
    ('BR-04', 'Bắt buộc theo nút lưu', [
        '– Lưu nháp / Lưu và tiếp tục: chỉ bắt Kho (khi tạo). SL nháp lưu phần nguyên.',
        '– Điều chuyển: bắt thêm Ghi chú, ≥ 1 dòng, từng dòng ĐVT / Vị trí xuất / Lô xuất / Vị trí nhập / SL, ít nhất 1 file (sửa: khi '
        'phiếu chưa có file) — báo cùng một lượt.',
        '– Mọi kiểu lưu: Ghi chú ≤ 255 ký tự; 0 ≤ SL ≤ 999,999,999, tối đa 2 chữ số thập phân; Vị trí xuất ≠ Vị trí nhập.'],
     ['Tạo mới', 'Chỉnh sửa', 'Điều chuyển']),
    ('BR-05', 'Chặn khi đang kiểm kho', [
        '– Hàng thuộc phiếu kiểm kê theo hàng hóa đang kiểm (trạng thái đang kiểm / chờ duyệt) tại kho → “Hàng đang kiểm kho.”.',
        '– Vị trí thuộc kế hoạch kiểm kê theo vị trí Đang kiểm hoặc phiếu kiểm kê theo vị trí Đang kiểm / Chờ duyệt kết quả → “Vị trí đang '
        'kiểm kho.”; popup vị trí hiện mờ.',
        '– Vị trí phải thuộc kho của phiếu → “Vị trí không thuộc kho của phiếu.”.'], ['Điều chuyển', 'Chọn vị trí']),
    ('BR-06', 'Kiểm tồn khi Điều chuyển', [
        '– Quy SL về ĐVT cơ sở theo hệ số ĐVT; cộng dồn các dòng cùng hàng + vị trí + lô ≤ tồn lô tại vị trí xuất (“Vượt quá SL tồn của '
        'lô.”).',
        '– Cộng dồn cùng hàng + vị trí ≤ tồn vị trí trừ SL các phiếu nhập kho chưa hạch toán tại vị trí đó (“Vượt quá SL tồn tại vị trí '
        'xuất.”).',
        '– Lỗi gắn dưới ô SL của mọi dòng thuộc nhóm vượt; thiếu ở một dòng thì không ghi dòng nào.'], ['Điều chuyển']),
    ('BR-07', 'Ghi tồn và vòng đời', [
        '– Đang tạo (xám) → Điều chuyển → Đã chuyển (xanh lá). Không có duyệt, khóa, hủy; không hoàn tác.',
        '– Điều chuyển: trừ tồn lô tại vị trí xuất, cộng cùng lô tại vị trí nhập (tạo mới nếu vị trí nhập chưa có), theo công ty của lô; '
        'tồn tổng của kho không đổi; ghi Thẻ kho.',
        '– Lập từ phiếu kiểm kê: cộng đã xử lý; xử lý hết → phiếu kiểm kê (và kế hoạch cha của kiểm kê theo vị trí) Hoàn thành; lưu nháp '
        'từ kiểm kê theo hàng hóa → phiếu kiểm kê Đang xử lý.'], ['Điều chuyển', 'Tạo mới']),
    ('BR-08', 'Điều kiện sửa / xóa', [
        '– Phiếu Đang tạo nằm trong phạm vi xem: ai xem được cũng sửa, xóa được (giữ lỗi hệ thống cũ — user chốt 19/10/2026).',
        '– Sửa không đổi Kho. Xóa là xóa cứng phiếu + dòng; không có ràng buộc con chặn xóa.',
        '– Trạng thái đổi giữa chừng → “Trạng thái đã bị thay đổi. Vui lòng load lại trang”.'], ['Chỉnh sửa', 'Xóa']),
    ('BR-09', 'Mã phiếu và đơn vị sở hữu', [
        '– Mã PĐCVT-NNNNN tự sinh theo số thứ tự phiếu (giữ công thức hệ thống cũ), không nhập / sửa được; không có trường nhập duy nhất '
        'nên không kiểm trùng.',
        '– Công ty / phòng ban / bộ phận của phiếu = của người lập (dùng cho phạm vi V2, letterhead bản in).'],
     ['Tạo mới', 'Xem danh sách', 'In']),
    ('BR-10', 'In và xuất', [
        '– In phiếu: chỉ phiếu Đã chuyển, letterhead theo công ty của phiếu. In dự kiến: theo dữ liệu đang nhập, không ghi dữ liệu.',
        '– Xuất Excel không giới hạn số dòng, theo phạm vi xem + bộ lọc; danh sách rỗng vẫn ra file (chỉ tiêu đề).'],
     ['In phiếu', 'In dự kiến', 'Xuất Excel']),
    ('BR-11', 'Quy tắc ghi lịch sử', [
        '– Tạo phiếu (nháp hoặc điều chuyển ngay) → “Tạo mới”; sửa Ghi chú / dòng hàng / file → “Thay đổi thông tin” (cũ → mới, dòng ghép '
        'theo hàng + lần xuất hiện); điều chuyển từ màn Sửa → thêm “Thay đổi trạng thái” Đang tạo → Đã chuyển; xóa → ghi mốc xóa.',
        '– Xem, in, xuất, lưu không đổi gì: không ghi; hiển thị mới nhất ở trên.'],
     ['Tạo mới', 'Chỉnh sửa', 'Điều chuyển', 'Xóa', 'Lịch sử']),
    ('BR-12', 'Sử dụng ở màn khác', [
        '– Thẻ kho hiện dòng điều chuyển PĐCVT-… liên kết sang chi tiết phiếu; Tổng hợp xuất nhập tồn cộng cả điều chuyển (loại báo cáo '
        '“Không nhặt điều chuyển” bỏ ra); báo cáo tồn theo vị trí đổi theo vị trí.',
        '– Vị trí, kho vật lý, hàng hóa đã có trên phiếu (kể cả nháp) không xóa được ở danh mục.',
        '– Dữ liệu dùng chung với hệ thống cũ: phiếu lập ở hệ thống cũ cũng hiện trên màn này.'],
     ['Điều chuyển', 'Xem danh sách']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Phiếu điều chuyển vị trí (phiếu, trạng thái, dòng hàng, số lượng chuyển theo '
    'vị trí / lô).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Kiểm kê theo vị trí (nút Tạo phiếu điều chuyển vị trí ở danh sách + chi tiết mở form nạp sẵn dòng chênh thiếu; điều '
                 'chuyển cộng số đã xử lý, xử lý hết thì phiếu kiểm kê chuyển Hoàn thành)', 'Kho -> Kiểm kho -> Theo vị trí'),
    ('2', 'Kho', 'Kiểm kê theo hàng hóa (nút Tạo phiếu điều chuyển vị trí; lưu nháp → Đang xử lý, điều chuyển → Hoàn thành / Đang xử lý; '
                 'đã có phiếu điều chuyển thì không lập lại)', 'Kho -> Kiểm kho -> Theo vị trí'),
    ('3', 'Tài chính', 'Kế hoạch kiểm kê theo vị trí (kế hoạch cha chuyển Hoàn thành khi phiếu kiểm kê vị trí xử lý xong bằng điều '
                       'chuyển)', 'Tài chính -> Kiểm kê'),
    ('4', 'Kho', 'Thẻ kho (dòng xuất ở vị trí cũ + dòng nhập ở vị trí mới theo lô, số chứng từ PĐCVT-… liên kết sang chi tiết phiếu)',
     'Kho -> Báo cáo kho'),
    ('5', 'Kho', 'Tổng hợp xuất nhập tồn (số nhập / xuất trong kỳ cộng cả điều chuyển; loại “Không nhặt điều chuyển” bỏ ra)',
     'Kho -> Báo cáo kho'),
    ('6', 'Kho', 'Báo cáo tồn kho theo vị trí (tồn vị trí xuất giảm, vị trí nhập tăng; tổng tồn kho không đổi)', 'Kho -> Báo cáo kho'),
    ('7', 'Kho', 'Báo cáo tồn kho chi tiết theo mặt hàng (tồn theo vị trí / lô dịch chuyển)', 'Kho -> Báo cáo kho'),
    ('8', 'Kho', 'Khai báo tồn kho đầu kỳ (lô tồn đầu đã có phiếu điều chuyển — kể cả nháp — coi là đã phát sinh giao dịch)',
     'Kho -> Tồn kho đầu kỳ'),
    ('9', 'Kho', 'Vị trí (không xóa được vị trí đã dùng làm vị trí xuất / nhập trên phiếu, kể cả nháp)', 'Kho -> Danh mục'),
    ('10', 'Kho', 'Kho vật lý (không xóa được kho đã có phiếu điều chuyển vị trí)', 'Kho -> Danh mục'),
    ('11', 'Danh mục dùng chung', 'Kho dữ liệu hàng hoá (không xóa được hàng hóa đã có trên phiếu, kể cả nháp)',
     'Danh mục dùng chung -> Hàng hoá -> Hàng hoá, vật tư'),
    ('12', 'Hệ thống ERP', 'Kiểm kho theo hàng hoá / Tự kiểm kê (lập phiếu điều chuyển từ các form phụ của hệ thống cũ; cột Phiếu kiểm kê '
                           'mở hệ thống cũ)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
