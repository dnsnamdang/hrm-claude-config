# -*- coding: utf-8 -*-
"""SRS màn "Theo dõi theo kho" (phân hệ Kho, mục cấp 1, 2 trang) — form chuẩn + quy định màn theo dõi / báo cáo (bảng Cách lấy dữ
liệu, bảng vị trí bấm được) + chuẩn 04/11 (Mục lục trang riêng căn giữa, Phần 5 bảng 4 cột).

Chạy: python gen_srs.py  → SRS - Theo dõi theo kho.docx
Khuôn chép: ../hoat-dong-kho/gen_srs.py (10/11, CÙNG bảng hoạt động, cùng hàm WarehouseActivityService::listForWarehouses(), cùng
  component components/warehouse/activity/*) — chép khung, cách viết, tên gọi cột / ô tổng hợp; nghiệp vụ lấy từ code màn này.
Nguồn đọc 10/11/2026 (nhánh develop — con của gop_db — cả 2 repo):
  FE  pages/warehouse/warehouse-tracking/index.vue (trang 1: danh sách kho), pages/warehouse/warehouse-tracking/_id/index.vue (trang 2:
      hoạt động 1 kho), components/warehouse/activity/{ActivitySummary.vue, activity-table.js, export-excel.js},
      components/{V2BaseSmartFilterPanel, V2BaseDataTable, V2Footer}.vue, components/modal/{export-fields-modal,
      column-customization-modal}.vue, utils/mixins/{filterStateMixin, exportFieldsMixin, CheckPermission}.js,
      utils/export/listExportFile.js, middleware/checkPermission.js, components/subsystem-menu/warehouse.js (mục cấp 1
      “Theo dõi theo kho”, isShow ['Quản lý kho']).
  BE  Modules/Finance/{Services/WarehouseTrackingService.php, Services/WarehouseActivityService.php,
      Http/Controllers/V1/WarehouseTrackingController.php, Routes/api.php (group finance/warehouse-tracking,
      checkPermission:warehouse.kho.manage)}, Modules/MasterData/Services/Warehouse/WarehouseCatalogScope.php (mã
      warehouse.kho_tat_ca_cong_ty.view quyết định xem mọi công ty), app/Support/Permissions/Catalog/warehouse.php.
  Tài liệu: design.md, plan.md (fix #11931: Mã / Tên mở TAB MỚI), spec docs/superpowers/specs/gop-db/2026-10-27-theo-doi-theo-kho-design.md
  (đoạn “tô màu dòng” đã bỏ 29/10 — #11901, code không còn).
Ảnh: ./tdtk_shots — dev-hrm 10/11/2026, DNS Admin (có “Quản lý kho” + “Xem danh mục kho của tất cả công ty”), _capture/capture.js chặn
  mọi yêu cầu ghi (0 lọt). Dữ liệu THẬT, không giả trạng thái. Dev không có phiếu “Đã hoàn thành” trong ngày → không có ảnh dòng xanh.
Đối soát dev 10/11 (_capture/probe.js, chỉ GET): trang 1 = 22 kho = danh mục Kho vật lý cùng phạm vi (21 Hoạt động + 1 Khóa MT-KNXT);
  trang 2 kho PTT 55 dòng = 40 Phiếu đề nghị xuất kho + 15 Phiếu đề nghị nhập kho = đúng tập mã ở 2 màn danh sách lọc kho PTT, trạng thái
  Chờ duyệt + Đang xuất / nhập kho; ô tổng hợp 55 / 0 / 55 khớp; MT 5 = 1 + 4; KTCN 2 = 2 + 0 (Hoạt động kho bộ trước đo sáng 10/11:
  PTT 54 = 39 + 15 — chênh 1 phiếu PDNXK-39058 gửi thủ kho lúc 11:12 cùng ngày).
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

TEN = 'Theo dõi theo kho'
SHOTS = os.path.join(HERE, 'tdtk_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Theo dõi theo kho'
MENU2 = MENU + ' => Mã / Tên kho'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Theo dõi theo kho.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
EMPTY = '“Không có dữ liệu phù hợp”'
LOADERR = '“Lỗi khi tải dữ liệu”'
NOPERM = '“Bạn không có quyền thực hiện chức năng này”'
XLS_OK = '“Xuất Excel thành công.”'
XLS_ERR = '“Lỗi khi xuất Excel”'
XLS_EMPTY = '“Không có dữ liệu để xuất”'
FILE1 = 'theo_doi_theo_kho.xlsx'
FILE2 = 'hoat_dong_kho_<mã kho>.xlsx'
DNXK = 'Phiếu đề nghị xuất kho'
DNNK = 'Phiếu đề nghị nhập kho'
Q = '“Quản lý kho”'
QALL = '“Xem danh mục kho của tất cả công ty”'
T2 = '“Hoạt động nhập/xuất kho <mã kho> - <tên kho>”'
TIP_KHOI = ('HOẠT ĐỘNG NHẬP/XUẤT KHO <MÃ> - <TÊN> • Phiếu đề nghị xuất kho và đề nghị nhập kho của kho này • Gồm phiếu đang xử lý và '
            'phiếu nhận trong hôm nay (kể cả đã hoàn thành) • Danh sách tự tải lại mỗi 60 giây')
TIP_TONG = 'Tổng số phiếu nhận • Số phiếu đề nghị xuất kho + đề nghị nhập kho đang hiện ở danh sách bên dưới'
TIP_HT = 'Tổng hoàn thành • Số phiếu đã hoàn thành (đã có Thời gian hoàn thành)'
TIP_CXL = ('Tổng chưa xử lý • Tổng số phiếu nhận trừ Tổng hoàn thành • Gồm phiếu "Đã nhận đề nghị" và phiếu đang lấy hàng / xếp hàng')
FIELDS = ('Phiếu đề nghị, Loại, Người yêu cầu, Hình thức vận chuyển, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành, '
          'Trạng thái, Tổng thời gian xử lý')

A = 'Người có quyền Quản lý kho'
TN = ('Người dùng có quyền thực hiện chức năng: quyền %s (y hệ thống ERP); phạm vi kho theo công ty đang làm, có thêm quyền %s thì mọi '
      'công ty (Phần 2).' % (Q, QALL))
DK1 = ('1. Người dùng đăng nhập thành công.\n'
       '2. Người dùng có quyền %s ở công ty đang làm.\n'
       '3. Người dùng đang ở trang danh sách kho của màn Theo dõi theo kho, danh sách đã nạp xong.' % Q)
DK2 = ('1. Người dùng đăng nhập thành công.\n'
       '2. Người dùng có quyền %s; kho đang xem thuộc phạm vi của người dùng (Phần 2).\n'
       '3. Người dùng đang ở trang hoạt động nhập/xuất của một kho, bảng đã nạp xong.' % Q)

d = SrsDoc(out=OUT, menu=MENU, route='/warehouse/warehouse-tracking', full_url='', img_dir=UML)
d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Theo dõi theo kho': 'menu_muc',
    'Cấu hình cột': 'btn_cauhinhcot', 'Xuất Excel': 'btn_xuatexcel', 'Mã / Tên kho': 'link_makho', 'Phiếu đề nghị': 'link_maphieu',
}.items()})

UI_OVER = {}
UI_EXPLICIT = {}


def uc(code, name, group, actor):
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None, extra=None):
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
    return k + 1


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.doc.add_page_break()  # Mục lục sang trang riêng như bản Drive đã chuẩn hoá
d.h2('Mục lục')
d.doc.paragraphs[-1].alignment = 1  # căn giữa chữ 'Mục lục'
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Theo dõi theo kho thuộc phân hệ Kho (chuyển từ hệ thống ERP: Kho › Theo dõi theo '
    'kho), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu màn THEO DÕI 2 trang: trang 1 liệt kê các kho vật lý trong phạm vi công ty của người dùng; bấm mã / tên một kho '
    'mở trang 2 là bảng hoạt động nhập / xuất của RIÊNG kho đó — các %s và %s đang chờ xử lý / đang lấy hàng, xếp hàng, cùng phiếu nhận '
    'trong hôm nay (kể cả đã hoàn thành).' % (DNXK, DNNK),
    'Ghi rõ phạm vi kho theo quyền, điều kiện một phiếu xuất hiện trên bảng, cách xác định Trạng thái, cách tính Tổng thời gian xử lý '
    'và 3 ô tổng hợp (Tổng số phiếu nhận, Tổng hoàn thành, Tổng chưa xử lý) để người nghiệm thu đối soát được với danh mục Kho vật lý '
    'và 2 màn danh sách %s / %s.' % (DNXK, DNNK),
    'Ghi rõ các điểm khác hệ thống ERP có chủ đích: ô tìm nhanh, Cấu hình cột, Xuất Excel ở cả 2 trang; danh sách kho có phân trang; '
    'tự tải lại 60 giây thay cho cập nhật tức thời (ERP đã hỏng); khôi phục khối tổng hợp; bỏ tô màu dòng theo thời gian chờ.',
])
d.p('Phạm vi chức năng (8 chức năng, đặc tả ở Phần 3):')
d.bullets([
    'Trang 1 — Xem danh sách kho (5 cột, phân trang, sắp xếp theo Mã / Tên); Tìm kiếm và lọc danh sách kho (ô tìm mã / tên, ô Nhóm, ô '
    'Công ty khi xem mọi công ty); Xuất Excel danh sách kho.',
    'Trang 2 — Xem hoạt động nhập/xuất của kho (khối tổng hợp “Phiếu nhận” + bảng 11 cột, tự tải lại 60 giây, nút Quay lại); Tìm kiếm '
    'theo mã phiếu đề nghị; Mở phiếu đề nghị (bấm mã phiếu → màn chi tiết ở tab mới); Xuất Excel hoạt động kho.',
    'Cả 2 trang — Tùy chỉnh cột (mỗi trang một cấu hình riêng).',
    'Không thuộc màn này: màn CHỈ ĐỌC — không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Duyệt / Không duyệt, Import Excel, In, Lịch '
    'sử thay đổi, không có Tìm kiếm nâng cao / Cài đặt bộ lọc (bộ lọc gọn ≤ 3 ô). Mọi thao tác trên kho làm ở danh mục Kho vật lý, trên '
    'phiếu làm ở màn của phiếu (Phần 5).',
])
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Trưởng kho / quản lý kho chọn một kho bất kỳ trong công ty (không cần là thủ kho kho đó) để xem kho đó đang tồn bao nhiêu phiếu '
    'chờ xử lý, phiếu nào đang lấy / xếp hàng, phiếu nào đã xong trong ngày và mất bao lâu.',
    'Quản lý cấp tổng công ty (có quyền xem mọi công ty) lọc theo Công ty / Nhóm kho để so khối lượng việc giữa các kho; xuất Excel để '
    'báo cáo.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Cả 2 trang yêu cầu quyền %s (BR-01). Phạm vi kho: kho của công ty đang làm; có quyền %s (Super Admin có sẵn) thì mọi công ty và có '
    'thêm ô lọc Công ty (BR-02).' % (Q, QALL),
    'Danh sách kho gồm cả kho đang Khóa, chỉ bỏ kho đã xóa (y ERP) (BR-03). Kho ngoài phạm vi / đã xóa / không tồn tại → trang 2 chuyển '
    'sang trang “Không tìm thấy trang yêu cầu” (BR-04).',
    'Bảng hoạt động: phiếu hiện khi ở trạng thái Chờ duyệt hoặc Đang xuất kho / Đang nhập kho, HOẶC có Thời gian nhận từ 00:00 hôm nay mà '
    'không phải Đang tạo / Đã hủy (BR-05); KHÔNG bó theo thủ kho (khác màn Hoạt động kho).',
    'Màn không ghi dữ liệu nào; xem / tìm / xuất không ghi lịch sử (BR-11).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Kho / Kho vật lý', 'Kho hàng khai ở danh mục Kho vật lý (mã, tên, nhóm, công ty, trạng thái Hoạt động / Khóa). Trang 1 liệt kê kho '
                         'vật lý, không phải kho kế toán.'),
    ('Nhóm kho', 'Nhóm gom kho theo vùng (dev: Kho Hà Nội, Kho Sài Gòn); kho chưa gắn nhóm thì cột Nhóm trống.'),
    (DNXK + ' (ĐNXK)', 'Phiếu yêu cầu thủ kho xuất hàng khỏi kho, lập từ Yêu cầu xuất hàng; mã dạng PDNXK-xxxxx.'),
    (DNNK + ' (ĐNNK)', 'Phiếu yêu cầu thủ kho nhận hàng vào kho, lập từ Yêu cầu nhập hàng; mã dạng PDNNK-xxxxx.'),
    ('Thời gian nhận', 'Lúc phiếu đề nghị được gửi tới thủ kho (gửi thủ kho).'),
    ('Thời gian lấy/xếp hàng', 'Lúc thủ kho bắt đầu xử lý phiếu: lập Phiếu xuất kho (ĐNXK) / Phiếu nhập kho (ĐNNK) hoặc phiếu điều chuyển '
                               'kho — phiếu đề nghị chuyển sang Đang xuất kho / Đang nhập kho.'),
    ('Thời gian hoàn thành', 'Lúc hàng thực sự rời / vào kho (gửi Phiếu xuất kho / Phiếu nhập kho) — phiếu đề nghị chuyển sang Đã xuất kho '
                             '/ Đã nhập kho.'),
    ('Trạng thái trên bảng', '3 giá trị: “Đã nhận đề nghị” (chưa có Thời gian lấy/xếp hàng, nhãn cam) · “Đang lấy hàng” (ĐNXK) / “Đang xếp '
                             'hàng” (ĐNNK) (đã có Thời gian lấy/xếp hàng, nhãn xanh dương) · “Đã hoàn thành” (đã có Thời gian hoàn '
                             'thành, nhãn xanh lá).'),
    ('Trạng thái phiếu', 'Trạng thái lưu trên phiếu đề nghị: Đang tạo, Chờ duyệt, Đang xuất / nhập kho, Đã xuất / nhập kho, Đang hạch '
                         'toán, Đã hạch toán, Đã hủy — dùng để quyết định phiếu có lên bảng không (BR-05).'),
    ('Tổng thời gian xử lý', 'Khoảng từ Thời gian nhận tới Thời gian hoàn thành, dạng “x ngày y giờ z phút”; dưới 1 phút ghi “Vài giây”.'),
    ('Cấu trúc phân cấp', 'Không có: trang 1 bảng phẳng mỗi kho 1 dòng; trang 2 bảng phẳng mỗi phiếu đề nghị 1 dòng (ĐNXK, ĐNNK trộn chung).'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn dùng lại quyền %s của nhóm Danh mục kho (y hệ thống ERP — user chốt 27/10/2026, không tạo quyền mới). Máy chủ chặn cả 4 lời '
    'gọi dữ liệu của màn bằng quyền này; mục menu chỉ hiện khi có quyền. Phạm vi kho do quyền %s quyết định (Super Admin được cấp sẵn).'
    % (Q, QALL))
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Quản lý kho', 'Thấy mục menu, mở được 2 trang; dùng mọi chức năng: tìm / lọc, sắp xếp, phân trang, mở trang hoạt động, mở '
                          'phiếu, Xuất Excel, Cấu hình cột.'),
], widths=[0.8, 2.2, 3.0])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('P1', 'Quản lý kho (không có quyền xem mọi công ty)', 'Chỉ kho vật lý có Công ty = công ty đang làm của người dùng; không có ô lọc '
                                                         'Công ty; người dùng chưa gắn công ty → danh sách rỗng.'),
    ('P2', 'Xem danh mục kho của tất cả công ty', 'Kho của MỌI công ty (kể cả kho chưa gắn công ty) + ô lọc Công ty. Super Admin có sẵn '
                                                 'quyền này (dev 10/11/2026: DNS Admin thấy đủ 22 kho, 9 công ty trong ô lọc).'),
], widths=[0.8, 2.2, 3.0])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1 + P1', 'Q1 + P2', 'Không có Quản lý kho'], [
    ('FR-01 Xem danh sách kho', '✅ kho công ty mình', '✅ mọi công ty', '❌ trang báo không tìm thấy'),
    ('FR-02 Tìm kiếm và lọc danh sách kho', '✅ (không có ô Công ty)', '✅ (có ô Công ty)', '❌'),
    ('FR-03 Xem hoạt động nhập/xuất của kho', '✅ kho công ty mình', '✅ mọi kho', '❌ trang báo không tìm thấy'),
    ('FR-04 Tìm kiếm theo mã phiếu', '✅', '✅', '❌'),
    ('FR-05 Mở phiếu đề nghị', '✅ (màn phiếu áp quyền xem của nó)', '✅ (như trái)', '❌'),
    ('FR-06 Tùy chỉnh cột', '✅', '✅', '❌'),
    ('FR-07 Xuất Excel danh sách kho', '✅ kho công ty mình', '✅ mọi công ty', '❌'),
    ('FR-08 Xuất Excel hoạt động kho', '✅', '✅', '❌'),
], widths=[2.2, 1.4, 1.3, 1.1])
d.p('Màn không có Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, Import Excel, In, Lịch sử thay đổi, Duyệt nên ma trận không có các dòng đó.')
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có %s: mục “Theo dõi theo kho” không hiện ở menu phân hệ Kho; dán thẳng địa chỉ trang 1 → hệ thống chuyển sang trang “KHÔNG '
    'TÌM THẤY TRANG YÊU CẦU” (“Không tìm thấy hoặc không được cấp quyền truy cập trang”).' % Q,
    'Không có quyền mà mở thẳng địa chỉ trang 2 của một kho → máy chủ từ chối, trang chuyển sang trang “KHÔNG TÌM THẤY TRANG YÊU CẦU”, '
    'không lộ dữ liệu kho.',
    'Có quyền nhưng mở trang 2 của kho thuộc công ty khác (P1), kho đã xóa hoặc mã kho không tồn tại → cùng trang “KHÔNG TÌM THẤY TRANG '
    'YÊU CẦU” (máy chủ trả “Không tìm thấy kho.”), không phân biệt kho có tồn tại hay không.',
    'Bị gỡ quyền khi đang mở màn → lần nạp kế tiếp máy chủ từ chối: trang 1 báo %s; trang 2 chuyển sang trang không tìm thấy (kể cả ở '
    'lượt tự tải lại 60 giây).' % NOPERM,
    'Bấm mã phiếu ở trang 2: màn chi tiết phiếu (tab mới) tự áp quyền xem của nó.',
    'Chưa đăng nhập / phiên hết hạn → chuyển về màn đăng nhập (quy tắc chung).',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Mục menu Theo dõi theo kho', 'Có quyền Quản lý kho', 'Mục cấp 1 của phân hệ Kho, ngay sau Hoạt động kho'),
    ('Ô lọc Công ty (trang 1)', 'Có quyền xem mọi công ty (P2)', 'Người P1 không có ô này; gửi công ty khác cũng bị bỏ qua'),
    ('Nút Xuất Excel, Cấu hình cột', 'Luôn hiện ở cả 2 trang', 'Xuất Excel khóa trong lúc đang xuất (trang 2: cả khi chưa nạp xong kho)'),
    ('Khối tổng hợp “Phiếu nhận” (trang 2)', 'Hiện sau lần nạp thành công đầu tiên', 'Có nút Thu gọn / Mở rộng'),
    ('Nút Quay lại (trang 2)', 'Luôn hiện ở chân trang', 'Về trang 1 cùng tab, bộ lọc trang 1 còn nguyên (10 phút)'),
    ('Nút Thêm mới, Import, In, cột Hành động', 'Không có', 'Màn chỉ đọc (như ERP)'),
], widths=[2.2, 2.3, 1.5])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A, [0, 1, 2, 3])],
    [('FR-01', 'Xem danh sách kho', 'view'),
     ('FR-03', 'Xem hoạt động nhập/xuất của kho', 'view'),
     ('FR-07', 'Xuất Excel danh sách kho', 'io'),
     ('FR-08', 'Xuất Excel hoạt động kho', 'io')],
    [('FR-02', 'Tìm kiếm và lọc danh sách kho', 'view', 'extend', [0], None),
     ('FR-06', 'Tùy chỉnh cột', 'view', 'extend', [0, 1], None),
     ('FR-04', 'Tìm kiếm theo mã phiếu', 'view', 'extend', [1], None),
     ('FR-05', 'Mở phiếu đề nghị', 'view', 'extend', [1], None)],
    'Sơ đồ Use Case tổng quan màn Theo dõi theo kho')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1 Xem danh sách kho
k = fr(1, 'Xem danh sách kho',
       rule=('- Màn Danh sách, Phân trang, Sắp xếp dữ liệu bảng và Cấu hình cột.', 'list'),
       intro=dict(
           ten='Truy cập và xem danh sách kho',
           mota='Trang 1 của màn: hiển thị các kho vật lý trong phạm vi của người dùng (kho của công ty đang làm; có quyền xem mọi công ty '
                'thì mọi công ty), gồm cả kho đang Khóa, mỗi kho 1 dòng với Mã, Tên, Nhóm, Công ty, phân trang 10 dòng. Mã và Tên là '
                'đường dẫn mở bảng hoạt động nhập / xuất của kho đó (FR-03) ở tab mới. Trang chỉ đọc.',
           tacnhan=TN,
           dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền %s ở công ty đang làm.\n'
                    '3. Người dùng vào màn từ menu phân hệ Kho.' % Q,
           chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
                 '2. Hệ thống kiểm quyền %s; không có → chuyển trang không tìm thấy.\n'
                 '3. Hệ thống nạp cấu hình cột đã lưu của người dùng, nguồn ô Nhóm / Công ty; có bộ lọc ghi tạm dưới 10 phút thì khôi phục '
                 'vào ô tìm nhanh, ô Nhóm, ô Công ty.\n'
                 '4. Hệ thống lấy các kho chưa xóa trong phạm vi (BR-02, BR-03), áp bộ lọc, xếp ngày tạo mới nhất trước.\n'
                 '5. Hệ thống hiển thị bảng 5 cột, trang 1, 10 dòng/trang, dòng “Hiển thị 1–10 / N”.\n'
                 '6. Người dùng đổi trang / số dòng mỗi trang, bấm tiêu đề Mã hoặc Tên để sắp xếp.\n'
                 '7. Người dùng bấm Mã hoặc Tên một kho → mở trang hoạt động của kho đó ở TAB MỚI (FR-03); trang 1 giữ nguyên.' % Q,
           phu='• Đang nạp → trong bảng hiện vòng xoay “Đang tải dữ liệu...”.\n'
               '• Không có kho nào trong phạm vi / theo bộ lọc → bảng hiện ' + EMPTY + ', dòng dưới bảng “Không có kho nào.”.\n'
               '• Người dùng chưa gắn công ty (P1) → danh sách rỗng, không kéo ra kho không thuộc công ty nào.\n'
               '• Máy chủ lỗi khi nạp → thông báo ' + LOADERR + ', bảng giữ dữ liệu cũ.\n'
               '• Bị gỡ quyền giữa chừng → thông báo ' + NOPERM + '.\n'
               '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
               '• Phiên đăng nhập hết hạn khi đang thao tác → thông báo hết phiên, chuyển về màn đăng nhập.',
           dacbiet='Phân trang mặc định 10 dòng (5 / 10 / 20 / 50 / 100), tối đa 100 dòng/trang. Cột mặc định hiện: đủ 5 cột; cột khóa '
                   '(không ẩn, không đổi vị trí): STT, Mã. Sắp xếp được 2 cột: Mã, Tên; sắp xếp và trang đang xem không được ghi nhớ. '
                   'Khác ERP có chủ đích: ERP không phân trang, lọc Mã / Tên bằng 2 ô riêng → HRM gom vào ô tìm nhanh, thêm Cấu hình cột, '
                   'Xuất Excel. Bấm Mã / Tên mở tab mới (giữ y ERP, fix #11931).'),
       layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Trang 1 — danh sách kho (DNS Admin, mọi công ty, dev)'),
       extra=[(shot('00_menu'), 'Vị trí mục menu: phân hệ Kho › Theo dõi theo kho (mục cấp 1)'),
              (shot('03_sort'), 'Sắp xếp theo cột Mã (tăng dần)'),
              (shot('03b_page2'), 'Trang 2 của danh sách: “Hiển thị 11–20 / 22”')],
       ui_kw=dict(required=False),
       ui=[
           ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
            ['- “Theo dõi theo kho” trên thanh tiêu đề trang, tiêu đề bảng và tab trình duyệt', '- Không có biểu tượng giải thích cạnh tiêu đề']),
           ('Khối Bộ lọc danh sách', 'Label', 'Hiển thị', '–', 'Hiển thị',
            ['- Ô tìm nhanh, ô Nhóm, (ô Công ty), nút Tìm kiếm, Làm mới trên một hàng', '- Chi tiết ở mục 2.2']),
           ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
            ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.7)',
             '- Khóa trong lúc đang xuất; bên trái hiện tiến độ “Đã tải x/y dòng…”']),
           ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
            ['- Biểu tượng cột, rê chuột: “Cấu hình cột hiển thị”', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.6)']),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- Đánh số liên tục giữa các trang (trang 2 bắt đầu 11 khi 10 dòng/trang)', '- Cột khóa']),
           ('Cột Mã', 'Link', 'Enable', '–', 'Hiển thị',
            ['- Mã kho, vd “PTT”, chữ xanh', '- Bấm → mở trang hoạt động của kho ở TAB MỚI (mục 2.3)', '- Sắp xếp được; cột khóa']),
           ('Cột Tên', 'Link', 'Enable', '–', 'Hiển thị',
            ['- Tên kho, vd “Phan Trọng Tuệ”', '- Bấm → giống cột Mã', '- Sắp xếp được']),
           ('Cột Nhóm', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- Nhóm kho, vd “Kho Hà Nội”', '- Kho chưa gắn nhóm → trống', '- Không sắp xếp']),
           ('Cột Công ty', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- Tên công ty sở hữu kho', '- Kho chưa gắn công ty → trống', '- Không sắp xếp']),
           ('Biểu tượng sắp xếp', 'Icon Button', 'Enable', '–', 'Hiển thị',
            ['- Mũi tên 2 chiều ở cột Mã, Tên', '- Đang sắp tăng: mũi tên lên; giảm: mũi tên xuống']),
           ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo dữ liệu',
            ['- a–b: thứ tự dòng đầu–cuối của trang, N: tổng số kho theo bộ lọc', '- Không có kho: “Không có kho nào.”']),
           ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
            ['- Đổi → nạp lại từ trang 1']),
           ('Thanh phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
            ['- Nút «, ‹, số trang, ›, »', '- Nút về đầu / lùi mờ ở trang 1; tới / về cuối mờ ở trang cuối']),
           ('Trạng thái đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- Trong bảng: vòng xoay + “Đang tải dữ liệu...”.'),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', ['- Trong bảng: ' + EMPTY, '- Chỉ hiện khi không có kho nào']),
           ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
            ['- ' + LOADERR + ' khi máy chủ lỗi', '- ' + NOPERM + ' khi bị gỡ quyền giữa chừng']),
       ],
       ev=[
           ('Mở màn hình', 'System',
            'Before:\n– Kiểm tra quyền Quản lý kho; không có → chuyển trang “Không tìm thấy trang yêu cầu”, dừng xử lý.\n'
            '– Xác định phạm vi: công ty đang làm, hoặc mọi công ty nếu có quyền xem mọi công ty.\n'
            'During:\n– Nạp cấu hình cột, nguồn ô Nhóm / Công ty; khôi phục bộ lọc ghi tạm (còn hạn 10 phút).\n'
            '– Lấy kho chưa xóa trong phạm vi theo bộ lọc, xếp ngày tạo mới nhất trước; máy chủ lỗi → ' + LOADERR + '.\n'
            'After:\n– Hiển thị trang 1, 10 dòng, dòng “Hiển thị 1–10 / N”.'),
           ('Bấm tiêu đề Mã / Tên', 'Click',
            'Before:\n– Chỉ cột Mã, Tên sắp xếp được.\n'
            'During:\n– Lần 1 tăng dần, bấm tiếp đảo chiều; cột khác đang sắp thì về tăng dần cột mới.\n'
            'After:\n– Nạp lại từ trang 1 theo cột đã chọn, cùng giá trị thì kho tạo sau đứng trước; bộ lọc giữ nguyên.'),
           ('Đổi trang / đổi số dòng mỗi trang', 'Click',
            'Before:\n– Giữ bộ lọc và sắp xếp đang áp.\nDuring:\n– Đổi số dòng → về trang 1.\n'
            'After:\n– Nạp trang được chọn, STT tiếp nối theo trang, cập nhật dòng “Hiển thị a–b / N”.'),
           ('Bấm Mã / Tên một kho', 'Click',
            'Before:\n– Dòng kho trong danh sách.\nDuring:\n– Mở trang hoạt động nhập/xuất của kho ở TAB MỚI.\n'
            'After:\n– Tab danh sách giữ nguyên trang, bộ lọc, sắp xếp; không ghi dữ liệu.'),
           ('Rời màn rồi quay lại / tải lại trang', 'System',
            'Before:\n– Rời sang màn khác: xóa bộ lọc ghi tạm. Tải lại trang (F5) hoặc vào trang hoạt động của kho rồi Quay lại trong 10 '
            'phút: giữ bộ lọc.\nAfter:\n– Sắp xếp và trang về mặc định (trang 1, ngày tạo mới nhất trước); cấu hình cột vẫn giữ.'),
       ])

d.p('2.1.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('Bảng dưới mô tả cách hệ thống lấy từng cột và con số của trang danh sách kho. “Tập dữ liệu” là các kho vật lý chưa xóa trong phạm '
    'vi của người dùng, sau khi áp ô tìm nhanh, ô Nhóm, ô Công ty.')
d.data_table([
    ('Phạm vi kho', 'Kho vật lý có Công ty = công ty đang làm của người dùng; có quyền %s → mọi công ty (kể cả kho chưa gắn công ty). '
                    'Người dùng chưa gắn công ty → tập rỗng.' % QALL, '—'),
    ('Kho được liệt kê', 'Mọi trạng thái trừ đã xóa: kho Hoạt động và kho Khóa đều hiện (y ERP); bảng không có cột trạng thái.', '—'),
    ('Dòng “Hiển thị a–b / N”', 'N = số kho của tập dữ liệu; đổi theo bộ lọc. Ràng buộc khớp số: N (không lọc) = số dòng danh mục Kho vật '
                                'lý cùng phạm vi khi chọn mọi trạng thái. Đo dev 10/11/2026 (mọi công ty): 22 = 21 Hoạt động + 1 Khóa '
                                '(MT-KNXT).', '—'),
    ('Cột Nhóm / Công ty', 'Tên nhóm kho / tên công ty gắn trên kho ở danh mục Kho vật lý; chưa gắn → trống.', '—'),
    ('Thứ tự dòng', 'Mặc định: ngày tạo kho mới nhất trước, cùng lúc thì kho tạo sau trước. Bấm Mã / Tên: theo cột đó (thứ tự chữ cái của '
                    'hệ thống), rồi kho tạo sau trước.', '—'),
])
k += 1
d.p('2.1.%d Danh sách popup mở từ số liệu' % k)
d.popup_table([
    ('Mã kho ở cột Mã', 'Không phải popup — mở trang hoạt động nhập/xuất của kho ở tab mới (mục 2.3)',
     'Xem việc đang dồn ở kho mà không mất danh sách kho', 'Khối tổng hợp Phiếu nhận + bảng phiếu đề nghị xuất / nhập kho của kho'),
    ('Tên kho ở cột Tên', 'Không phải popup — như cột Mã', 'Như trên', 'Như trên'),
])

# ------------------------------------------------------------ 2.2 Tìm kiếm và lọc danh sách kho
fr(2, 'Tìm kiếm và lọc danh sách kho',
   rule=('- Kịch bản tìm kiếm và Bộ lọc.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách kho',
       mota='Thu hẹp danh sách kho theo mã / tên (ô tìm nhanh), theo Nhóm kho và — với người xem mọi công ty — theo Công ty. Bộ lọc chỉ có '
            '≤ 3 ô nên bày thẳng trên một hàng cạnh nút Tìm kiếm, Làm mới (không có Tìm kiếm nâng cao / Cài đặt bộ lọc). Bộ lọc được ghi '
            'tạm 10 phút để giữ khi tải lại trang hoặc khi Quay lại từ trang hoạt động.',
       tacnhan=TN, dieukien=DK1,
       chinh='1. Người dùng nhập mã hoặc tên kho (một phần, vd “phan”) vào ô tìm nhanh rồi bấm Tìm kiếm / nhấn Enter.\n'
             '2. Hoặc chọn một giá trị ở ô Nhóm (Kho Hà Nội, Kho Sài Gòn…) — danh sách nạp lại ngay khi chọn.\n'
             '3. Người xem mọi công ty chọn một công ty ở ô Công ty — danh sách nạp lại ngay.\n'
             '4. Hệ thống lấy lại các kho trong phạm vi thỏa mọi điều kiện (VÀ), về trang 1, cập nhật “Hiển thị a–b / N”, ghi tạm bộ '
             'lọc (10 phút).\n'
             '5. Người dùng bấm Làm mới để xóa mọi ô lọc, bỏ sắp xếp, về trang 1.',
       phu='• Không có kho khớp → bảng ' + EMPTY + ', dòng “Không có kho nào.”.\n'
           '• Bấm × trong ô tìm nhanh hoặc ô chọn → xóa giá trị; ô tìm nhanh chỉ áp khi bấm Tìm kiếm / Enter, ô chọn áp ngay.\n'
           '• Gõ chữ chưa bấm Tìm kiếm mà đổi ô Nhóm / Công ty, sắp xếp hay đổi trang → chữ đang gõ cũng được áp.\n'
           '• Người không có quyền xem mọi công ty không thấy ô Công ty; công ty khác gửi lên cũng bị máy chủ bỏ qua.\n'
           '• Tải lại trang / Quay lại từ trang hoạt động trong 10 phút → giữ bộ lọc; rời sang màn khác → xóa bộ lọc.\n'
           '• Máy chủ lỗi → ' + LOADERR + '.',
       dacbiet='Ô tìm nhanh khớp MỘT PHẦN mã HOẶC tên kho, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối; ký tự %, _ được tìm '
               'đúng nghĩa đen. Ô Nhóm, ô Công ty chọn 1 giá trị. Ô Nhóm liệt kê mọi nhóm kho (không theo công ty).'),
   layout=dict(menu=MENU + ' => Bộ lọc danh sách', shot=shot('01c_filter'), shot_caption='Khối Bộ lọc danh sách (người xem mọi công ty)'),
   extra=[(shot('02_search'), 'Tìm “phan”: 2 kho khớp mã hoặc tên'),
          (shot('02b_group'), 'Lọc Nhóm = Kho Hà Nội: 4 kho'),
          (shot('02c_company_open'), 'Ô Công ty mở danh sách công ty'),
          (shot('04_nores'), 'Không có kho khớp')],
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo mã, tên kho”', '- Khớp một phần mã hoặc tên', '- Áp khi bấm Tìm kiếm / nhấn Enter',
         '- Mặc định: trống (hoặc giá trị ghi tạm trong 10 phút)']),
       ('Nút × trong ô tìm nhanh', 'Icon Button', 'Enable', '–', '–', 'Ẩn',
        ['- Chỉ hiện khi ô có chữ', '- Bấm → xóa chữ, chưa nạp lại']),
       ('Ô Nhóm', 'Dropdown', 'Enable', 'Danh sách nhóm kho', 'Không', 'Trống',
        ['- Nhãn “Nhóm”; dev: Kho Hà Nội, Kho Sài Gòn', '- Chọn 1 giá trị, áp ngay', '- Có × để bỏ chọn']),
       ('Ô Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống',
        ['- Nhãn “Công ty”; chỉ hiện với người có quyền xem mọi công ty', '- Chọn 1 giá trị, áp ngay', '- Có × để bỏ chọn']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp bộ lọc, nạp lại từ trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Bấm → xóa mọi ô lọc, bỏ sắp xếp, xóa bộ lọc ghi tạm', '- Nạp lại trang 1 theo thứ tự mặc định']),
       ('Kết quả lọc', 'Table/Grid', 'Read-only', '–', '–', 'Theo kết quả', '- Chỉ còn kho khớp, STT đánh lại từ 1.'),
       ('Dòng “Hiển thị a–b / N” sau lọc', 'Label', 'Read-only', '–', '–', 'Theo kết quả', '- N = số kho khớp, vd tìm “phan”: 1–2 / 2.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', ['- Trong bảng: ' + EMPTY, '- Dưới bảng: “Không có kho nào.”']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + LOADERR + ' khi máy chủ lỗi.'),
   ],
   ev=[
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh (bỏ khoảng trắng đầu / cuối) + ô Nhóm, ô Công ty.\n'
        'During:\n– Tìm kho có mã HOẶC tên chứa chuỗi; %, _ hiểu đúng nghĩa đen; ô Công ty chỉ có tác dụng với người xem mọi công ty.\n'
        '– Máy chủ lỗi → ' + LOADERR + '.\nAfter:\n– Hiển thị trang 1 kết quả, cập nhật “Hiển thị a–b / N”; ghi tạm bộ lọc 10 phút.'),
       ('Chọn / bỏ chọn ô Nhóm, ô Công ty', 'Change',
        'Before:\n– Giữ chữ đang có ở ô tìm nhanh.\nDuring:\n– Nạp lại ngay theo mọi điều kiện (VÀ).\n'
        'After:\n– Về trang 1, cập nhật kết quả; ghi tạm bộ lọc.'),
       ('Gõ vào ô tìm nhanh (chưa bấm Tìm kiếm)', 'Change',
        'Before:\n– Chỉ đổi chữ trong ô.\nAfter:\n– Ghi tạm chữ; danh sách chưa đổi cho tới khi bấm Tìm kiếm / Enter hoặc đổi ô chọn / '
        'sắp xếp / trang.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có bộ lọc / sắp xếp đang áp.\nAfter:\n– Xóa mọi ô lọc (cả bản ghi tạm), bỏ sắp xếp, nạp lại trang 1.'),
   ])

# ------------------------------------------------------------ 2.3 Xem hoạt động nhập/xuất của kho
k = fr(3, 'Xem hoạt động nhập/xuất của kho',
       rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng và Cấu hình cột.', 'list'),
       intro=dict(
           ten='Xem bảng hoạt động nhập / xuất của một kho',
           mota='Trang 2 của màn, tiêu đề %s: hiển thị trong một bảng (không phân trang) mọi %s và %s của KHO ĐƯỢC CHỌN — phiếu đang xử lý '
                'và phiếu nhận trong hôm nay — kèm khối tổng hợp “Phiếu nhận” (Tổng số phiếu nhận, Tổng hoàn thành, Tổng chưa xử lý). '
                'Cùng bảng, cùng cách tính với màn Hoạt động kho nhưng không bó theo thủ kho. Bảng tự tải lại mỗi 60 giây.' % (T2, DNXK, DNNK),
           tacnhan=TN,
           dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền %s.\n'
                    '3. Kho được chọn chưa xóa và thuộc phạm vi của người dùng (Phần 2).' % Q,
           chinh='1. Người dùng bấm Mã hoặc Tên một kho ở trang 1 → trang 2 mở ở tab mới.\n'
                 '2. Hệ thống kiểm quyền và kiểm kho thuộc phạm vi; không đạt → chuyển trang “Không tìm thấy trang yêu cầu”.\n'
                 '3. Hệ thống lấy %s + %s của kho theo điều kiện BR-05, xếp phiếu chưa hoàn thành lên trước, trong mỗi nhóm Thời gian '
                 'nhận mới nhất trước (BR-08).\n'
                 '4. Hệ thống hiển thị tiêu đề %s, khối tổng hợp và bảng 11 cột, mọi dòng trên một trang.\n'
                 '5. Cứ 60 giây (khi tab đang hiện) hệ thống tự nạp lại bảng và 3 ô theo từ khóa, sắp xếp đang áp, không hiện vòng tải.\n'
                 '6. Người dùng bấm tiêu đề cột có sắp xếp, bấm Thu gọn để ẩn 3 ô tổng hợp.\n'
                 '7. Người dùng bấm Quay lại → về trang 1 cùng tab, bộ lọc trang 1 còn nguyên.' % (DNXK, DNNK, T2),
           phu='• Đang nạp (mở trang, Tìm kiếm / Làm mới / sắp xếp) → vòng xoay “Đang tải dữ liệu...” trong bảng.\n'
               '• Kho không có phiếu thỏa BR-05 → bảng ' + EMPTY + ', 3 ô = 0 (dev: kho EG_LN).\n'
               '• Kho đã xóa / ngoài phạm vi / không tồn tại / không có quyền → chuyển trang “KHÔNG TÌM THẤY TRANG YÊU CẦU”, dừng tự '
               'tải lại; không hiện thông báo lỗi.\n'
               '• Máy chủ lỗi khi nạp (do người dùng bấm) → ' + LOADERR + ', bảng giữ dữ liệu cũ; lượt tự tải lại lỗi → không báo.\n'
               '• Tab trình duyệt đang ẩn → bỏ lượt tự tải lại.\n'
               '• Quay lại sau quá 10 phút → trang 1 về bộ lọc mặc định (bộ lọc ghi tạm đã hết hạn).',
           dacbiet='Không phân trang (bảng theo dõi trong ngày, ERP cũng đổ hết). Cột mặc định hiện: đủ 11 cột; cột khóa: STT, Phiếu đề nghị. '
                   'Sắp xếp được 5 cột: Phiếu đề nghị, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành; không ghi nhớ. '
                   'Kho đang Khóa vẫn xem được. Khác ERP có chủ đích: ERP cập nhật tức thời nhưng đã hỏng → tự tải lại 60 giây; bỏ tô màu '
                   'dòng theo thời gian chờ (user chốt 29/10/2026, #11901).'),
       layout=dict(menu=MENU2, shot=shot('10_detail'), shot_caption='Trang 2 — hoạt động nhập/xuất kho PTT (dev)'),
       extra=[(shot('10e_tip'), 'Icon ⓘ của khối Phiếu nhận'),
              (shot('11b_empty'), 'Kho không có phiếu: bảng rỗng, 3 ô = 0'),
              (shot('11d_sort'), 'Sắp xếp theo cột Phiếu đề nghị (tăng dần)'),
              (shot('12_back'), 'Bấm Quay lại: về danh sách kho, bộ lọc “phan” còn nguyên'),
              (shot('13_404'), 'Mở trang 2 của kho không có / ngoài phạm vi')],
       ui_kw=dict(required=False),
       ui=[
           ('Tiêu đề trang', 'Label', 'Hiển thị', '–', 'Hiển thị',
            ['- %s, vd “Hoạt động nhập/xuất kho PTT - Phan Trọng Tuệ”' % T2,
             '- Hiện ở thanh tiêu đề, tiêu đề bảng, tab trình duyệt; chưa nạp xong: “Hoạt động nhập/xuất kho”']),
           ('Khối Bộ lọc danh sách', 'Label', 'Hiển thị', '–', 'Hiển thị',
            ['- Ô tìm mã phiếu, nút Tìm kiếm, Làm mới', '- Chi tiết ở mục 2.4']),
           ('Khối tổng hợp “Phiếu nhận”', 'Label', 'Hiển thị', '–', 'Hiển thị',
            ['- Tiêu đề “PHIẾU NHẬN” kèm icon ⓘ: “' + TIP_KHOI + '”', '- 3 ô số, đơn vị “phiếu”; số KHÔNG bấm được']),
           ('Ô Tổng số phiếu nhận', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- = số dòng đang hiện trong bảng', '- Icon ⓘ: “' + TIP_TONG + '”']),
           ('Ô Tổng hoàn thành', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- = số dòng Trạng thái “Đã hoàn thành”', '- Icon ⓘ: “' + TIP_HT + '”']),
           ('Ô Tổng chưa xử lý', 'Label', 'Read-only', '≥ 0', 'Theo dữ liệu',
            ['- = Tổng số phiếu nhận − Tổng hoàn thành', '- Icon ⓘ: “' + TIP_CXL + '”']),
           ('Nút Thu gọn', 'Button', 'Enable', '–', 'Hiển thị',
            ['- Bấm → ẩn 3 ô, chữ đổi “Mở rộng”; bấm lại → hiện', '- Không ghi nhớ']),
           ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
            ['- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.8)', '- Khóa khi đang xuất hoặc chưa nạp xong kho']),
           ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.6).'),
           ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- 1, 2, 3… theo thứ tự đang hiện', '- Cột khóa']),
           ('Cột Phiếu đề nghị', 'Link', 'Enable', '–', 'Hiển thị',
            ['- Mã PDNXK-… / PDNNK-…, chữ xanh', '- Bấm → màn chi tiết phiếu ở TAB MỚI (mục 2.5)', '- Sắp xếp được; cột khóa']),
           ('Cột Loại', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- Loại phiếu theo tên hệ thống ERP, vd “Xuất mượn”, “Xuất bán (HĐH)”, “Nhập điều chuyển kho nội bộ”', '- Không sắp xếp']),
           ('Cột Người yêu cầu', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- Họ tên người lập Yêu cầu xuất hàng / Yêu cầu nhập hàng gốc', '- Không có yêu cầu gốc → trống']),
           ('Cột Hình thức vận chuyển', 'Table/Grid', 'Read-only', '3 giá trị', 'Hiển thị',
            ['- Chỉ phiếu đề nghị xuất kho: Tự vận chuyển, Công ty vận chuyển, Khách hàng vận chuyển', '- Đề nghị nhập kho: trống']),
           ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- “Mã kho - Tên kho”, mọi dòng là kho đang xem', '- Sắp xếp được (theo mã kho)']),
           ('Cột Thời gian nhận', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', ['- Lúc gửi thủ kho', '- Sắp xếp được']),
           ('Cột Thời gian lấy/xếp hàng', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
            ['- Trống khi Đã nhận đề nghị', '- Sắp xếp được']),
           ('Cột Thời gian hoàn thành', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
            ['- Trống khi chưa hoàn thành', '- Sắp xếp được']),
           ('Cột Trạng thái', 'Badge', 'Read-only', '4 nhãn', 'Hiển thị',
            ['- “Đã nhận đề nghị” (cam)', '- “Đang lấy hàng” (ĐNXK) / “Đang xếp hàng” (ĐNNK) (xanh dương)', '- “Đã hoàn thành” (xanh lá)',
             '- Không sắp xếp']),
           ('Cột Tổng thời gian xử lý', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
            ['- Thời gian hoàn thành − Thời gian nhận, “x ngày y giờ z phút”; dưới 1 phút “Vài giây”', '- Chưa hoàn thành: trống']),
           ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', ['- Chân trang', '- Bấm → về danh sách kho (trang 1) cùng tab']),
           ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '- Trong bảng: ' + EMPTY + '; không có dòng “Hiển thị a–b / N”.'),
           ('Trang “Không tìm thấy trang yêu cầu”', 'Label', 'Hiển thị', '–', 'Ẩn',
            ['- “KHÔNG TÌM THẤY TRANG YÊU CẦU” / “Không tìm thấy hoặc không được cấp quyền truy cập trang”, nút “Về trang chủ”',
             '- Khi kho không hợp lệ hoặc thiếu quyền']),
           ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- ' + LOADERR + ' khi máy chủ lỗi ở lần nạp do người dùng bấm.'),
       ],
       ev=[
           ('Mở trang hoạt động của kho', 'System',
            'Before:\n– Kiểm tra quyền Quản lý kho; kho tồn tại, chưa xóa, thuộc phạm vi.\n'
            '– Không đạt → chuyển trang “Không tìm thấy trang yêu cầu”, không hiện thông báo, dừng xử lý.\n'
            'During:\n– Nạp cấu hình cột; lấy phiếu theo BR-05, xếp theo BR-08; máy chủ lỗi → ' + LOADERR + '.\n'
            'After:\n– Hiển thị tiêu đề, khối tổng hợp, bảng (mọi dòng); bật tự tải lại 60 giây.'),
           ('Tự tải lại sau mỗi 60 giây', 'System',
            'Before:\n– Bỏ lượt nếu tab đang ẩn; giữ từ khóa và sắp xếp.\n'
            'During:\n– Lấy lại dữ liệu, không bật vòng tải; lỗi thì bỏ qua; thiếu quyền / kho hết hợp lệ → trang không tìm thấy.\n'
            'After:\n– Cập nhật bảng và 3 ô tổng hợp.'),
           ('Bấm tiêu đề cột có sắp xếp', 'Click',
            'Before:\n– 5 cột Phiếu đề nghị, Kho, Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành.\n'
            'During:\n– Lần 1 tăng dần, bấm tiếp đảo chiều.\nAfter:\n– Nạp lại theo cột đã chọn, cùng giá trị giữ thứ tự mặc định.'),
           ('Bấm Thu gọn / Mở rộng', 'Click',
            'Before:\n– Khối tổng hợp đang hiện.\nAfter:\n– Ẩn / hiện 3 ô số; bảng không nạp lại.'),
           ('Rê chuột vào icon ⓘ', 'Click',
            'Before:\n– Ở tiêu đề khối Phiếu nhận và 3 ô.\nAfter:\n– Hiện khung giải thích (nguyên văn ở mục 2.3.4).'),
           ('Bấm Quay lại', 'Click',
            'Before:\n– Không hỏi xác nhận (trang chỉ đọc).\nDuring:\n– Dừng tự tải lại, chuyển về danh sách kho cùng tab.\n'
            'After:\n– Danh sách khôi phục bộ lọc ghi tạm (≤ 10 phút), về trang 1.'),
       ])

d.p('2.3.%d Cách lấy dữ liệu và giải thích chỉ tiêu' % k)
d.p('Bảng dưới mô tả cách hệ thống lấy từng cột, từng ô tổng hợp và nội dung icon ⓘ (nguyên văn trên giao diện). “Tập dữ liệu” là mọi %s '
    'và %s của kho đang xem, thỏa điều kiện BR-05, sau khi áp từ khóa ở ô tìm nhanh.' % (DNXK, DNNK))
d.data_table([
    ('Phạm vi', 'Đúng 1 kho được chọn ở trang 1; KHÔNG bó theo thủ kho (người xem không cần là thủ kho kho đó).',
     '“Phiếu đề nghị xuất kho và đề nghị nhập kho của kho này”'),
    ('Điều kiện phiếu lên bảng', 'Trạng thái phiếu Chờ duyệt hoặc Đang xuất kho / Đang nhập kho (bất kể ngày) HOẶC Thời gian nhận từ 00:00 '
                                 'hôm nay trở đi mà không phải Đang tạo, Đã hủy (phiếu xong trong ngày ở lại tới hết ngày).',
     '“Gồm phiếu đang xử lý và phiếu nhận trong hôm nay (kể cả đã hoàn thành)”'),
    ('Ô Tổng số phiếu nhận', 'Đếm số dòng của tập dữ liệu (ĐNXK + ĐNNK); đổi theo từ khóa; = số dòng đang thấy.', TIP_TONG),
    ('Ô Tổng hoàn thành', 'Đếm dòng có Thời gian hoàn thành.', TIP_HT),
    ('Ô Tổng chưa xử lý', 'Tổng số phiếu nhận − Tổng hoàn thành = số dòng Đã nhận đề nghị + Đang lấy hàng + Đang xếp hàng.', TIP_CXL),
    ('Cột Trạng thái', 'Có Thời gian hoàn thành → Đã hoàn thành; có Thời gian lấy/xếp hàng → Đang lấy hàng (ĐNXK) / Đang xếp hàng (ĐNNK); '
                       'còn lại → Đã nhận đề nghị.', '—'),
    ('Cột Tổng thời gian xử lý', 'Số phút giữa Thời gian nhận và Thời gian hoàn thành đổi ra ngày (1.440 phút) / giờ / phút, bỏ phần bằng 0; '
                                 '0 phút → “Vài giây”; thiếu mốc → trống.', '—'),
    ('Cột Người yêu cầu / Hình thức vận chuyển', 'Từ Yêu cầu xuất hàng / Yêu cầu nhập hàng gốc: người lập; hình thức vận chuyển chỉ có ở '
                                                 'yêu cầu xuất hàng.', '—'),
    ('Thứ tự dòng', 'Chưa hoàn thành trước, đã hoàn thành sau; trong nhóm Thời gian nhận mới nhất trước, cùng giờ phiếu tạo sau trước. '
                    'Bấm cột sắp xếp: cột đó trước, rồi thứ tự mặc định.', '—'),
    ('Ràng buộc khớp số', 'Số dòng ĐNXK = số phiếu ở màn %s lọc kho đó, trạng thái Chờ duyệt + Đang xuất kho (cộng phiếu xong nhận hôm '
                          'nay); tương tự ĐNNK; trùng từng dòng với màn Hoạt động kho của thủ kho kho đó. Đo dev 10/11/2026: PTT 55 = 40 + '
                          '15, MT 5 = 1 + 4, KTCN 2 = 2 + 0, khớp đúng từng mã.' % DNXK, '—'),
])
k += 1
d.p('2.3.%d Danh sách popup mở từ số liệu' % k)
d.popup_table([
    ('Số ở 3 ô tổng hợp', 'Không có popup — số không bấm được', 'Nắm nhanh khối lượng việc của kho',
     'Các phiếu tương ứng chính là các dòng của bảng'),
    ('Mã PDNXK-… ở cột Phiếu đề nghị', 'Không phải popup — mở màn chi tiết %s ở tab mới (mục 2.5)' % DNXK,
     'Xem phiếu mà không mất bảng đang theo dõi', 'Toàn bộ thông tin + dòng hàng của phiếu'),
    ('Mã PDNNK-… ở cột Phiếu đề nghị', 'Không phải popup — mở màn chi tiết %s ở tab mới (mục 2.5)' % DNNK,
     'Như trên', 'Toàn bộ thông tin + dòng hàng của phiếu'),
])

# ------------------------------------------------------------ 2.4 Tìm kiếm theo mã phiếu
fr(4, 'Tìm kiếm theo mã phiếu',
   rule=('- Kịch bản tìm kiếm và Bộ lọc.', 'search'),
   intro=dict(
       ten='Tìm phiếu đề nghị theo mã trong bảng hoạt động của kho',
       mota='Thu hẹp bảng hoạt động của kho đang xem về các phiếu có mã chứa chuỗi đã nhập (ô “Tìm theo mã phiếu đề nghị”). 3 ô tổng hợp '
            'tính lại theo kết quả. Từ khóa KHÔNG được ghi nhớ: mỗi lần mở trang hoạt động (kể cả tải lại trang) ô tìm trống, để không '
            'lọc ngầm khi chuyển sang kho khác.',
       tacnhan=TN, dieukien=DK2,
       chinh='1. Người dùng nhập mã hoặc một phần mã (vd “39053”, “PDNNK”) vào ô tìm nhanh.\n'
             '2. Người dùng bấm Tìm kiếm hoặc nhấn Enter.\n'
             '3. Hệ thống lấy lại các phiếu của kho theo BR-05 có mã chứa chuỗi.\n'
             '4. Hệ thống hiển thị kết quả theo thứ tự đang áp, cập nhật 3 ô tổng hợp.\n'
             '5. Người dùng bấm Làm mới để xóa từ khóa, bỏ sắp xếp, xem lại toàn bộ.',
       phu='• Không có phiếu khớp → ' + EMPTY + ', 3 ô = 0.\n'
           '• Bấm × trong ô → xóa chữ; bảng chỉ đổi khi bấm Tìm kiếm / Enter, sắp xếp hoặc lượt tự tải lại.\n'
           '• Đã gõ chưa bấm mà sắp xếp / tới lượt tự tải lại 60 giây → chữ đang gõ cũng được áp.\n'
           '• Tải lại trang (F5) → ô tìm trống, bảng đầy đủ.\n'
           '• Máy chủ lỗi → ' + LOADERR + '.',
       dacbiet='Khớp MỘT PHẦN mã phiếu (không tìm theo loại / người), không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối; %, _ đúng '
               'nghĩa đen; không giới hạn ký tự. Không có ô lọc nâng cao.'),
   layout=dict(menu=MENU2 + ' => Bộ lọc danh sách', shot=shot('11_search'), shot_caption='Khối Bộ lọc danh sách trang 2: tìm “39053”'),
   extra=[(shot('11a_search_full'), 'Kết quả tìm “39053”: 1 phiếu, ô tổng hợp 1 / 0 / 1'),
          (shot('11c_nores'), 'Không có phiếu khớp từ khóa')],
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo mã phiếu đề nghị”', '- Khớp một phần mã', '- Áp khi bấm Tìm kiếm / Enter', '- Luôn trống khi mở trang']),
       ('Nút × trong ô tìm nhanh', 'Icon Button', 'Enable', '–', '–', 'Ẩn', ['- Chỉ hiện khi ô có chữ', '- Bấm → xóa chữ, chưa nạp lại']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp từ khóa, nạp lại bảng + 3 ô.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → xóa từ khóa, bỏ sắp xếp, nạp lại toàn bộ.'),
       ('Kết quả tìm', 'Table/Grid', 'Read-only', '–', '–', 'Theo kết quả', '- Chỉ còn phiếu khớp, STT đánh lại từ 1.'),
       ('Khối tổng hợp sau tìm', 'Label', 'Read-only', '≥ 0', '–', 'Theo kết quả',
        ['- 3 ô đếm trên kết quả', '- Vd kho PTT tìm “PDNNK”: 15 / 0 / 15']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- ' + EMPTY),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + LOADERR),
   ],
   ev=[
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô, bỏ khoảng trắng đầu / cuối; giữ sắp xếp.\n'
        'During:\n– Tìm phiếu của kho có mã chứa chuỗi; %, _ đúng nghĩa đen.\n– Máy chủ lỗi → ' + LOADERR + '.\n'
        'After:\n– Hiển thị kết quả, cập nhật 3 ô; không khớp → ' + EMPTY + '.'),
       ('Gõ vào ô tìm nhanh', 'Change',
        'Before:\n– Chỉ đổi chữ trong ô.\nAfter:\n– Bảng chưa đổi tới khi bấm Tìm kiếm / Enter, sắp xếp hoặc lượt tự tải lại.'),
       ('Bấm × trong ô', 'Click', 'Before:\n– Ô đang có chữ.\nAfter:\n– Xóa chữ, chưa nạp lại.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Có / không có từ khóa, sắp xếp.\nAfter:\n– Xóa từ khóa, bỏ sắp xếp, nạp lại toàn bộ.'),
   ])

# ------------------------------------------------------------ 2.5 Mở phiếu đề nghị
fr(5, 'Mở phiếu đề nghị từ mã phiếu',
   rule=('- Màn Danh sách và Xem chi tiết.', 'list'),
   intro=dict(
       ten='Mở màn chi tiết phiếu đề nghị xuất kho / nhập kho',
       mota='Từ mã phiếu ở cột Phiếu đề nghị của trang hoạt động, mở màn chi tiết phiếu (%s hoặc %s, đã chuyển sang HRM) ở TAB MỚI, để '
            'xem / xử lý phiếu mà trang hoạt động vẫn mở và tự tải lại. Màn Theo dõi theo kho không có cửa sổ xem chi tiết riêng.' % (DNXK, DNNK),
       tacnhan=TN, dieukien=DK2 + '\n4. Bảng có ít nhất 1 dòng.',
       chinh='1. Người dùng bấm mã phiếu ở cột Phiếu đề nghị.\n'
             '2. Mã PDNXK-… → mở màn chi tiết %s ở tab mới; mã PDNNK-… → màn chi tiết %s.\n'
             '3. Màn chi tiết hiển thị thông tin + dòng hàng của phiếu, nút thao tác theo quyền và trạng thái của màn đó.\n'
             '4. Quay lại tab trang hoạt động: trạng thái phiếu cập nhật ở lượt tự tải lại kế tiếp (≤ 60 giây) hoặc khi bấm Tìm kiếm.'
             % (DNXK, DNNK),
       phu='• Thiếu quyền xem phiếu → màn chi tiết xử lý theo quy tắc của nó.\n'
           '• Phiếu đổi trạng thái / bị hủy giữa 2 lượt tải → màn chi tiết hiện trạng thái mới; dòng đổi / rời bảng ở lượt sau.\n'
           '• Đóng tab chi tiết → tab trang hoạt động giữ nguyên từ khóa, sắp xếp, cuộn.',
       dacbiet=None),
   layout=dict(menu=MENU2 + ' => Phiếu đề nghị', shot=shot('15_dnxk'),
               shot_caption='Màn chi tiết Phiếu đề nghị xuất kho mở ở tab mới từ mã phiếu'),
   extra=[(shot('15b_dnnk'), 'Màn chi tiết Phiếu đề nghị nhập kho mở ở tab mới từ mã phiếu')],
   ui_kw=dict(required=False),
   ui=[
       ('Mã phiếu ở cột Phiếu đề nghị', 'Link', 'Enable', '–', 'Hiển thị', ['- Chữ xanh', '- Bấm → mở tab mới, không rời trang hoạt động']),
       ('Đích của mã PDNXK-…', 'Link', 'Enable', '–', '–', '- Màn chi tiết %s (Kho › Xuất kho › %s).' % (DNXK, DNXK)),
       ('Đích của mã PDNNK-…', 'Link', 'Enable', '–', '–', '- Màn chi tiết %s (Kho › Nhập kho › %s).' % (DNNK, DNNK)),
       ('Tab trang hoạt động', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Giữ từ khóa, sắp xếp', '- Tiếp tục tự tải lại khi quay lại']),
   ],
   ev=[
       ('Bấm mã phiếu', 'Click',
        'Before:\n– Xác định loại phiếu theo dòng (đề nghị xuất / nhập kho).\n'
        'During:\n– Mở màn chi tiết tương ứng ở tab mới; màn đó tự kiểm quyền xem.\n'
        'After:\n– Tab trang hoạt động giữ nguyên; không ghi dữ liệu, không ghi lịch sử.'),
       ('Quay lại tab trang hoạt động', 'System',
        'Before:\n– Tab vừa ẩn thì các lượt tự tải lại đã bỏ qua.\nAfter:\n– Lượt kế tiếp (≤ 60 giây) nạp trạng thái mới của phiếu.'),
   ])

# ------------------------------------------------------------ 2.6 Tùy chỉnh cột
fr(6, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của 2 bảng',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp cột của bảng danh sách kho (5 cột) và của bảng hoạt động (11 cột). Mỗi bảng một cấu '
            'hình riêng, lưu theo người dùng trên máy chủ; cấu hình bảng hoạt động dùng chung cho mọi kho và KHÔNG chung với màn Hoạt '
            'động kho. Chỉ đổi cách hiển thị, không đổi dữ liệu.',
       tacnhan=TN, dieukien=DK1.replace('3. Người dùng đang ở trang danh sách kho', '3. Người dùng đang ở trang danh sách kho hoặc trang '
                                                                                  'hoạt động'),
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị (biểu tượng cột cạnh Xuất Excel).\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột”: trang 1 liệt kê 5 cột (“Đang chọn 5/5 cột”), trang 2 liệt kê 11 cột (“Đang chọn 11/11 '
             'cột”), theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích cột không khóa; kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.',
       phu='• Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài → đóng, bảng giữ cấu hình đang áp.\n'
           '• Lưu không thành công → “Thao tác thất bại”, cấu hình cũ giữ nguyên.\n'
           '• Trang 1: cửa sổ Xuất Excel tích sẵn đúng các cột đang hiện; trang 2: luôn tích đủ 10 trường.',
       dacbiet='Cột khóa: trang 1 STT, Mã; trang 2 STT, Phiếu đề nghị (có ổ khóa, không ẩn, không kéo). Mặc định hiện đủ cột. Cấu hình giữ '
               'sau F5, đăng nhập lại, đổi trình duyệt; người dùng khác không bị ảnh hưởng.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tuỳ chỉnh cột — trang danh sách kho',
               note='Modal Tuỳ chỉnh cột mở ngay trên trang danh sách kho; trang hoạt động có cửa sổ cùng khuôn (ảnh dưới).'),
   extra=[(shot('26_colcfg_act'), 'Cửa sổ Tuỳ chỉnh cột — trang hoạt động (11 cột)')],
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột trang 1', 'Table/Grid', 'Enable', '5 cột', '–', 'Theo cấu hình đã lưu', '- STT, Mã, Tên, Nhóm, Công ty.'),
       ('Danh sách cột trang 2', 'Table/Grid', 'Enable', '11 cột', '–', 'Theo cấu hình đã lưu', '- STT, ' + FIELDS + '.'),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', ['- Bỏ tích → cột ẩn khỏi bảng']),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- Trang 1: STT, Mã; trang 2: STT, Phiếu đề nghị', '- Có ổ khóa; không ẩn, không đổi vị trí']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi cột không khóa (còn 2 cột khóa).'),
       ('Dòng “Đang chọn n/N cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', '- N = 5 (trang 1) / 11 (trang 2).'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- “Cập nhật thành công”', '- “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click',
        'Before:\n– Đang ở trang 1 hoặc trang 2.\nAfter:\n– Mở cửa sổ với cấu hình của đúng bảng đó (chưa lưu lần nào → đủ cột).'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Cột khóa không đổi vị trí.\nAfter:\n– Đổi thứ tự trong cửa sổ; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change', 'Before:\n– Cột khóa không bỏ tích được.\nAfter:\n– Cập nhật “Đang chọn n/N cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại, theo từng bảng.\nDuring:\n– Gửi danh sách cột đã tích đúng thứ tự.\n' + ERR + '\n'
        'After:\n– “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng; dữ liệu, bộ lọc, trang giữ nguyên.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.7 Xuất Excel danh sách kho
fr(7, 'Xuất Excel danh sách kho', usecase=('FR-07', 'Xuất Excel danh sách kho', 'io', A),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất Excel danh sách kho',
       mota='Xuất TOÀN BỘ kho theo bộ lọc + sắp xếp đang áp (mọi trang, không chỉ trang đang xem) ra file Excel; người dùng chọn trường và '
            'thứ tự cột. File có letterhead công ty người xuất, tiêu đề “DANH SÁCH THEO DÕI THEO KHO”. Hệ thống ERP không có chức năng này.',
       tacnhan=TN, dieukien=DK1,
       chinh='1. Người dùng lọc / sắp xếp theo nhu cầu rồi bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” gồm 4 trường Mã, Tên, Nhóm, Công ty, tích sẵn ĐÚNG các cột đang hiện trên '
             'bảng.\n'
             '3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy dữ liệu theo từng đợt (hiện tiến độ “Đã tải x/y dòng…”, “Đang dựng file x/y dòng…”) cùng letterhead công '
             'ty của người đăng nhập.\n'
             '5. Hệ thống tạo file %s (trang “Theo dõi theo kho”): letterhead, tiêu đề, cột STT + các trường đã chọn đúng thứ tự, có '
             'nút lọc ở hàng tiêu đề cột, khối ký “Ngày ..., tháng ..., năm ...” / “Người lập” / “(Ký, họ tên)”.\n'
             '6. Hệ thống tải file về, đóng cửa sổ, hiển thị %s.' % (FILE1, XLS_OK),
       phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Danh sách rỗng theo bộ lọc → KHÔNG tạo file, báo ' + XLS_EMPTY + '.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài → không xuất.\n'
           '• Lỗi khi xuất → ' + XLS_ERR + '; thiếu quyền → ' + NOPERM + '; không lấy được letterhead → file không có ảnh đầu trang.',
       dacbiet='Phạm vi file = phạm vi danh sách (BR-02). Tối đa 5.000 dòng mỗi đợt tải, tự tải nhiều đợt. Nút Xuất Excel khóa trong lúc '
               'xuất. Xuất không ghi lịch sử.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel — danh sách kho',
               note='Modal Chọn trường xuất Excel mở ngay trên trang danh sách kho.'),
   extra=[(shot('20b_export_empty'), 'Xuất khi danh sách rỗng: báo “Không có dữ liệu để xuất”')],
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', '4 trường', '–', 'Theo cột đang hiện',
        ['- Mã, Tên, Nhóm, Công ty', '- Cột STT luôn có trong file']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Không', 'Theo cột đang hiện',
        ['- Mặc định tích đúng cột đang hiện trên bảng', '- Bỏ tích → trường không có trong file']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích cả 4 trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/4 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Khóa khi chưa tích trường nào hoặc đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('Dòng tiến độ', 'Label', 'Read-only', '–', '–', 'Ẩn', '- Cạnh nút Xuất Excel: “Đã tải x/y dòng…” / “Đang dựng file x/y dòng…”.'),
       ('File Excel', 'Table/Grid', 'Read-only', '.xlsx', '–', '–',
        ['- Tên ' + FILE1 + ', trang “Theo dõi theo kho”', '- Letterhead công ty người xuất, tiêu đề “DANH SÁCH THEO DÕI THEO KHO”',
         '- STT + trường đã chọn, có nút lọc ở hàng tiêu đề cột', '- Khối ký “Người lập” cuối file']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + XLS_OK, '- ' + XLS_EMPTY, '- ' + XLS_ERR]),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Kiểm tra quyền Quản lý kho (máy chủ); bỏ qua nếu đang có lượt xuất.\n'
        'After:\n– Mở cửa sổ chọn trường, tích sẵn cột đang hiện.'),
       ('Tích / bỏ tích, kéo thả trường', 'Change',
        'Before:\n– Trong cửa sổ.\nAfter:\n– Cập nhật “Đang chọn n/4 trường”; 0 trường → khóa Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường; khóa nút Xuất Excel; thiếu quyền → ' + NOPERM + ', dừng xử lý.\n'
        'During:\n– Lấy toàn bộ kho theo bộ lọc + sắp xếp, cùng phạm vi; lấy letterhead.\n– Rỗng → ' + XLS_EMPTY + ', dừng; lỗi → ' +
        XLS_ERR + '.\n'
        'After:\n– Dựng file, tải về, ' + XLS_OK + '; mở lại nút Xuất Excel; không ghi lịch sử.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.8 Xuất Excel hoạt động kho
fr(8, 'Xuất Excel hoạt động kho', usecase=('FR-08', 'Xuất Excel hoạt động kho', 'io', A),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất Excel bảng hoạt động nhập / xuất của kho',
       mota='Xuất các phiếu của kho đang xem (theo từ khóa + sắp xếp đang áp) ra file Excel; người dùng chọn trường và thứ tự cột. File có '
            'letterhead công ty người xuất, tiêu đề in hoa %s, bảng và khối ký. Dùng chung cách dựng file với màn Hoạt động kho.' % T2,
       tacnhan=TN, dieukien=DK2,
       chinh='1. Người dùng tìm / sắp xếp rồi bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” gồm 10 trường, tích sẵn cả 10 (“Đang chọn 10/10 trường”).\n'
             '3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy LẠI dữ liệu mới nhất của kho theo từ khóa + sắp xếp, lấy letterhead công ty người đăng nhập.\n'
             '5. Hệ thống tạo file %s (trang “Hoạt động kho”): letterhead, tiêu đề vd “HOẠT ĐỘNG NHẬP/XUẤT KHO PTT - PHAN TRỌNG TUỆ”, cột '
             'STT + trường đã chọn, khối ký “Ngày…….Tháng…….Năm…….” / “Người lập” / “(Ký, họ tên)”.\n'
             '6. Hệ thống tải file, đóng cửa sổ, hiển thị %s.' % (FILE2, XLS_OK),
       phu='• Bỏ tích hết trường → khóa Xuất file.\n'
           '• Bảng rỗng → VẪN tạo file (tiêu đề, hàng tên cột, khối ký) và báo ' + XLS_OK + ' (khác trang 1).\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài → không xuất.\n'
           '• Lỗi → ' + XLS_ERR + '; có phiếu mới sau lần tải gần nhất → file theo dữ liệu MỚI NHẤT lúc bấm.',
       dacbiet='Trường tích sẵn KHÔNG theo cột đang ẩn (luôn đủ 10). Tên file theo mã kho (ký tự lạ đổi thành “_”), vd hoat_dong_kho_PTT.xlsx. '
               'Trạng thái ghi chữ; mọi ô xuống dòng, dòng tự giãn (#11895). Nút Xuất Excel khóa khi đang xuất. Không ghi lịch sử.'),
   layout=dict(menu=MENU2 + ' => Xuất Excel', shot=shot('21_export_act'), shot_caption='Cửa sổ Chọn trường xuất Excel — trang hoạt động',
               note='Modal Chọn trường xuất Excel mở ngay trên trang hoạt động của kho.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', '10 trường', '–', 'Đủ 10 trường', ['- ' + FIELDS, '- Cột STT luôn có trong file']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', ['- Mặc định tích cả 10', '- Bỏ tích → không có trong file']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích cả 10 trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/10 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Khóa khi chưa tích trường nào hoặc đang xuất.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('File Excel', 'Table/Grid', 'Read-only', '.xlsx', '–', '–',
        ['- Tên ' + FILE2 + ', trang “Hoạt động kho”', '- Ngày giờ dd/mm/yyyy hh:mm; Trạng thái ghi chữ', '- Khối ký “Người lập” cuối file']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + XLS_OK, '- ' + XLS_ERR]),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Kho đã nạp xong; bỏ qua nếu đang có lượt xuất.\nAfter:\n– Mở cửa sổ chọn trường, tích sẵn đủ 10 trường.'),
       ('Tích / bỏ tích, kéo thả trường', 'Change', 'Before:\n– Trong cửa sổ.\nAfter:\n– Cập nhật “Đang chọn n/10 trường”; 0 → khóa Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường; khóa nút Xuất Excel; máy chủ kiểm quyền Quản lý kho + kho trong phạm vi.\n'
        'During:\n– Lấy lại phiếu của kho theo từ khóa + sắp xếp (BR-05); lấy letterhead.\n– Lỗi → ' + XLS_ERR + '.\n'
        'After:\n– Dựng file (STT + trường đã chọn + khối ký), tải về, đóng cửa sổ, ' + XLS_OK + '; không ghi lịch sử.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Theo dõi theo kho; không lặp lại các quy tắc đã có trong SRS quy tắc chung.',
           anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Quyền Quản lý kho', [
        '– Cả 2 trang và mọi lời gọi dữ liệu yêu cầu quyền Quản lý kho (y ERP, user chốt 27/10/2026); menu chỉ hiện khi có quyền.',
        '– Thiếu quyền → trang “Không tìm thấy trang yêu cầu” (mở thẳng) hoặc thông báo “Bạn không có quyền thực hiện chức năng này”.'],
     ['Xem danh sách kho', 'Xem hoạt động', 'Xuất Excel']),
    ('BR-02', 'Phạm vi kho theo công ty', [
        '– Không có quyền “Xem danh mục kho của tất cả công ty”: chỉ kho có Công ty = công ty đang làm; chưa gắn công ty → rỗng.',
        '– Có quyền đó (Super Admin có sẵn): mọi công ty + ô lọc Công ty; ô Công ty của người khác bị bỏ qua.'],
     ['Xem danh sách kho', 'Tìm kiếm và lọc', 'Xem hoạt động', 'Xuất Excel']),
    ('BR-03', 'Kho được liệt kê', [
        '– Mọi kho chưa xóa, gồm cả kho đang Khóa (y ERP); kho đã xóa không hiện.'],
     ['Xem danh sách kho']),
    ('BR-04', 'Kho không hợp lệ', [
        '– Kho không tồn tại / đã xóa / ngoài phạm vi → trang hoạt động chuyển sang trang không tìm thấy, không lộ kho có tồn tại hay không.'],
     ['Xem hoạt động']),
    ('BR-05', 'Điều kiện phiếu lên bảng hoạt động', [
        '– %s / %s của kho ở trạng thái Chờ duyệt hoặc Đang xuất kho / Đang nhập kho; HOẶC' % (DNXK, DNNK),
        '– Thời gian nhận từ 00:00 hôm nay và trạng thái không phải Đang tạo, Đã hủy.',
        '– Không bó theo thủ kho của kho.'],
     ['Xem hoạt động', 'Xuất Excel']),
    ('BR-06', 'Trạng thái trên bảng', [
        '– Có Thời gian hoàn thành → Đã hoàn thành; có Thời gian lấy/xếp hàng → Đang lấy hàng (ĐNXK) / Đang xếp hàng (ĐNNK); còn lại → '
        'Đã nhận đề nghị. Nhãn + màu do máy chủ trả.'],
     ['Xem hoạt động', 'Xuất Excel']),
    ('BR-07', 'Tổng thời gian xử lý', [
        '– = Thời gian hoàn thành − Thời gian nhận, “x ngày y giờ z phút”; dưới 1 phút “Vài giây”; thiếu mốc → trống.'],
     ['Xem hoạt động', 'Xuất Excel']),
    ('BR-08', 'Thứ tự và sắp xếp', [
        '– Danh sách kho: mặc định ngày tạo mới nhất trước; sắp được Mã, Tên.',
        '– Bảng hoạt động: chưa hoàn thành trước, trong nhóm Thời gian nhận mới nhất trước; sắp được Phiếu đề nghị, Kho, 3 cột thời gian.'],
     ['Xem danh sách kho', 'Xem hoạt động', 'Xuất Excel']),
    ('BR-09', 'Ô tổng hợp', [
        '– Tổng số phiếu nhận = số dòng; Tổng hoàn thành = số dòng Đã hoàn thành; Tổng chưa xử lý = hiệu 2 số; tính sau tìm kiếm.'],
     ['Xem hoạt động', 'Tìm kiếm theo mã phiếu']),
    ('BR-10', 'Tìm kiếm, lọc và ghi nhớ', [
        '– Khớp một phần, không phân biệt hoa / thường, bỏ khoảng trắng 2 đầu; %, _ đúng nghĩa đen.',
        '– Bộ lọc trang 1 ghi tạm 10 phút (giữ khi F5 / Quay lại, xóa khi rời màn); từ khóa trang 2 không ghi nhớ.',
        '– Trang 2 tự tải lại mỗi 60 giây khi tab đang hiện.'],
     ['Tìm kiếm và lọc', 'Tìm kiếm theo mã phiếu', 'Xem hoạt động']),
    ('BR-11', 'Chỉ đọc, không ghi lịch sử', [
        '– Màn không ghi dữ liệu kho / phiếu; xem / tìm / xuất không ghi lịch sử. Mọi thay đổi làm ở màn nguồn (Phần 5).'],
     ['Xem danh sách kho', 'Xem hoạt động', 'Xuất Excel']),
    ('BR-12', 'Xuất Excel', [
        '– Trang 1: toàn bộ kho theo bộ lọc (mọi trang), rỗng thì không tạo file; trường tích sẵn theo cột đang hiện.',
        '– Trang 2: phiếu của kho lấy lại lúc bấm, rỗng vẫn tạo file; luôn tích đủ 10 trường.',
        '– Letterhead theo công ty người xuất (file danh sách, không phải chứng từ).'],
     ['Xuất Excel']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Theo dõi theo kho (danh sách kho vật lý; phiếu đề nghị xuất / nhập kho của từng '
    'kho cùng 3 mốc Thời gian nhận, Thời gian lấy/xếp hàng, Thời gian hoàn thành). Theo dõi theo kho chỉ đọc, không ghi lại màn nào.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Kho vật lý (nguồn trang 1: mã, tên, nhóm, công ty; khóa kho vẫn hiện, xóa kho thì rời danh sách; đổi tên đồng bộ)',
     'Kho -> Danh mục'),
    ('2', 'Kho', '%s (nguồn các dòng PDNXK; mã phiếu mở màn chi tiết phiếu này; hủy phiếu → dòng rời bảng)' % DNXK, 'Kho -> Xuất kho'),
    ('3', 'Kho', '%s (nguồn các dòng PDNNK; mã phiếu mở màn chi tiết phiếu này; hủy phiếu → dòng rời bảng)' % DNNK, 'Kho -> Nhập kho'),
    ('4', 'Tài chính', 'Phiếu xuất kho (lập phiếu = duyệt đề nghị xuất kho → ghi Thời gian lấy hàng; gửi phiếu → ghi Thời gian hoàn thành)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('5', 'Kho', 'Phiếu nhập kho (lập phiếu = duyệt đề nghị nhập kho → ghi Thời gian xếp hàng; gửi phiếu → ghi Thời gian hoàn thành)',
     'Kho -> Nhập kho'),
    ('6', 'Kho', 'Điều chuyển kho (lập phiếu điều chuyển duyệt đề nghị xuất kho điều chuyển → ghi Thời gian lấy hàng)', 'Kho -> Điều chuyển'),
    ('7', 'Tài chính', 'Yêu cầu xuất hàng, Yêu cầu nhập hàng (người lập yêu cầu = cột Người yêu cầu; Hình thức vận chuyển của yêu cầu '
                       'xuất hàng)', 'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển'),
    ('8', 'Kho', 'Hoạt động kho (cùng bảng, cùng cách tính, phạm vi = kho mình là thủ kho; dùng để đối chiếu trang 2)',
     'Kho -> Hoạt động kho'),
    ('9', 'Hệ thống ERP', 'Phiếu đề nghị xuất / nhập kho lập và gửi thủ kho trên hệ thống ERP (ghi Thời gian nhận) và màn Theo dõi theo kho '
                          'gốc của ERP (đọc cùng dữ liệu)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
