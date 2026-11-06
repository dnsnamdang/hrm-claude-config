# -*- coding: utf-8 -*-
"""SRS màn "Biên bản xử lý hàng thừa, thiếu sau kiểm kê" (mã BBXLKKHH-NNNNN) — form chuẩn Danh mục quốc gia, chuẩn 04/11/2026.

Chạy: python gen_srs.py  → SRS - Biên bản xử lý hàng thừa, thiếu sau kiểm kê.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc
  ../ke-hoach-tong-kiem-ke-hang-hoa/gen_srs.py (05/11, Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn).
Nguồn đọc 06/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Entities/InventoryAuditReport/{InventoryAuditReport,InventoryAuditReportDetail}.php,
      Services/InventoryAuditReport{,Write,Print,Attachment}Service.php, Http/Controllers/V1/InventoryAuditReportController.php,
      Http/Requests/InventoryAuditReport/{InventoryAuditReportStoreRequest,InventoryAuditReportApproveRequest}.php,
      Exports/InventoryAuditReportExport.php, Routes/api.php (/inventory-audit-reports), Services/EmployeeDebt/* (đọc bút toán)},
      MasterData PhysicalWarehouse (chặn xóa kho), app/Services/CatalogHistoryService.php,
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (3 quyền + "Kế toán kho")
  FE  pages/finance/inventory-audit-reports/** (index, create, _id/index, _id/edit, components/{InventoryAuditReportForm.vue,
      row-actions.js, export-excel.js}), components/subsystem-menu/finance.js (nhóm Kiểm kê)
  Bối cảnh + quyết định: design.md, plan.md (Redmine #11829, #11831, #11832), spec docs/superpowers/specs/gop-db/2026-10-21-…
Ảnh: ./bbxltt_shots — dev-hrm 06/11/2026 (_capture/capture.js, chặn mọi yêu cầu ghi). Giả trạng thái trên trình duyệt (sửa phản hồi
  GET, không gửi máy chủ): 12_edit, 03_rowmenu (dev không có biên bản Đang tạo — giả BBXLKKHH-00003 thành Đang tạo). Ảnh lỗi kiểm tra
  10e_row_validate / 14b_approve_validate: gọi hàm kiểm của form trên trình duyệt (không bấm Lưu / Duyệt).
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

TEN = 'Biên bản xử lý hàng thừa, thiếu sau kiểm kê'
SHOTS = os.path.join(HERE, 'bbxltt_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Kiểm kê => Biên bản xử lý hàng thừa, thiếu sau kiểm kê'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Biên bản xử lý hàng thừa, thiếu sau kiểm kê.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NOTFOUND = '“Không tìm thấy biên bản hoặc bạn không có quyền xem.”'
NOPERM = '“Bạn không có quyền thực hiện chức năng này.”'
CHANGED = '“Dữ liệu kiểm kê đã thay đổi. Vui lòng bấm "Lấy dữ liệu" lại.”'
MISS = '“Bạn chưa nhập đầy đủ thông tin.”'
Q1 = 'Kế toán kho'
Q2 = 'Duyệt biên bản xử lý hàng thừa, thiếu sau kiểm kê'
V1 = 'Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo tổng công ty'
V2 = 'Xem biên bản xử lý hàng thừa, thiếu sau kiểm kê - theo công ty'

A_KT = 'Kế toán kho (người lập biên bản)'
A_DUYET = 'Người duyệt biên bản'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng đã được cấp tài khoản; phạm vi xem theo quyền “%s” / “%s” '
      '(không quyền: chỉ biên bản mình tạo; có quyền “%s”: thêm mọi biên bản Chờ duyệt).' % (V1, V2, Q2))
TN_KT = 'Người dùng có quyền thực hiện chức năng: “%s” (hoặc Super admin).' % Q1
TN_OWNER = 'Người dùng có quyền thực hiện chức năng: người tạo biên bản, khi biên bản đang ở trạng thái Đang tạo.'
TN_DUYET = 'Người dùng có quyền thực hiện chức năng: “%s” (hoặc Super admin), khi biên bản đang ở trạng thái Chờ duyệt.' % Q2
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Biên bản xử lý hàng thừa, thiếu sau kiểm kê.\n'
      '3. Dữ liệu hiển thị trong phạm vi xem theo quyền (Phần 2).')

d = SrsDoc(out=OUT, menu=MENU, route='/finance/inventory-audit-reports', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Kiểm kê': 'menu_nhom', 'Biên bản xử lý hàng thừa, thiếu sau kiểm kê': 'menu_muc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Lấy dữ liệu': 'btn_laydulieu', 'Lưu và gửi duyệt': 'btn_luuguiduyet', 'Sửa': 'btn_sua_row',
    'Xem chi tiết': 'link_sophieu', 'Duyệt': 'btn_duyet_row', 'In': 'btn_in_row', 'In danh sách': 'btn_in_list',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Biên bản xử lý hàng thừa, thiếu sau kiểm kê (mã biên bản BBXLKKHH-NNNNN, ví dụ '
    'BBXLKKHH-00006), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ cách kế toán kho lấy kết quả các phiếu kiểm kê theo hàng hóa đã Hoàn thành của một kho vật lý trong khoảng ngày, chia '
    'thành hàng thừa / hàng thiếu, rồi ghi cho từng dòng lý do, giá xử lý (giá vốn hoặc giá bán), tỷ lệ chi phí nhân viên / công '
    'ty và nhân viên chịu.',
    'Làm rõ vòng đời trạng thái Đang tạo → Chờ duyệt → Đã duyệt và bút toán sổ cái hệ thống ghi khi người có quyền Duyệt chốt '
    'biên bản.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo biên bản (Lưu / Lưu và tiếp tục), Lấy '
    'dữ liệu kiểm kê và nhập xử lý từng dòng, Lưu và gửi duyệt, Chỉnh sửa, Xem chi tiết, Duyệt (ghi bút toán), In biên bản / In danh '
    'sách, Xuất Excel danh sách / Xuất Excel 1 biên bản, Xem lịch sử thay đổi. Màn KHÔNG có Xóa (hệ thống cũ đã tắt nút), Không '
    'duyệt / Từ chối, Hủy, Khóa / Mở khóa, Import Excel.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Biên bản là căn cứ xử lý chênh lệch sau kiểm kê: ai chịu, chịu bao nhiêu phần trăm, tính theo giá vốn hay giá bán.',
    'Khi Duyệt, hệ thống ghi bút toán: hàng thừa Nợ 3381 / Có 3341 (chi phí nhân viên) và Nợ 3381 / Có 711 (chi phí công ty); '
    'hàng thiếu Nợ 3341 / Có 1381 (chi phí nhân viên) và Nợ 811 / Có 1381 (chi phí công ty), theo từng nhân viên chịu. Các sổ '
    'công nợ nhân viên đọc lại bút toán này (Phần 5).',
    'Biên bản KHÔNG đổi tồn kho, không sinh phiếu nhập / xuất (tồn đã được điều chỉnh bằng phiếu nhập / xuất kho điều chỉnh kiểm kê).',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Chỉ người có quyền “%s” được tạo biên bản và bấm Lấy dữ liệu (BR-03).' % Q1,
    'Số lượng, giá, phiếu xử lý, mã kho do hệ thống lấy lại từ phiếu kiểm kê khi lưu; dữ liệu kiểm kê đổi giữa chừng thì phải Lấy '
    'dữ liệu lại (BR-05).',
    'Mỗi dòng bắt buộc Lý do, Giá xử lý, % chi phí, NV chịu ở cả Lưu và Lưu và gửi duyệt (BR-06).',
    'Chỉ người tạo được Sửa và chỉ khi Đang tạo; chỉ người có quyền Duyệt được Duyệt biên bản Chờ duyệt (BR-07, BR-08).',
    'Chi phí công ty lưu bằng chi phí nhân viên (giữ như hệ thống cũ — user chốt 21/10/2026), bản in / Excel in giá trị đã lưu (BR-09).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Biên bản xử lý hàng thừa, thiếu (biên bản)', 'Chứng từ BBXLKKHH-NNNNN của màn này: khoảng ngày, kho vật lý, các phiếu kiểm kê '
                                                  'được chọn, danh sách hàng thừa / thiếu và cách xử lý từng dòng.'),
    ('Phiếu kiểm kê theo hàng hóa', 'Phiếu kiểm kê ở phân hệ Kho; chỉ phiếu Hoàn thành, có kho đã chọn và ngày kiểm kê trong khoảng '
                                    'Từ ngày – Đến ngày mới được lấy.'),
    ('Hàng thừa / Hàng thiếu', 'Tổng chênh lệch thực kiểm của một hàng trong một phiếu kiểm kê: lớn hơn 0 là thừa, nhỏ hơn 0 là thiếu; '
                               'SL hiển thị là trị tuyệt đối; chênh lệch 0 bị bỏ.'),
    ('Phiếu xử lý', 'Phiếu nhập kho điều chỉnh kiểm kê (ưu tiên) hoặc phiếu xuất kho điều chỉnh kiểm kê đã Hoàn thành của cùng phiếu '
                    'kiểm kê và cùng hàng; là nguồn Đơn giá vốn và Mã kho (kho kế toán).'),
    ('Giá xử lý', 'Giá vốn (mặc định) hoặc Giá bán: chọn thành tiền nào làm cơ sở tính chi phí.'),
    ('% Chi phí nhân viên / % Chi phí công ty', 'Tỷ lệ chia chi phí; hai ô luôn cộng lại bằng 100; mặc định 100 / 0.'),
    ('NV chịu', 'Nhân viên chịu khoản chi phí nhân viên của dòng (hiển thị “Mã NV-Họ tên” trên bản đã lưu).'),
    ('Chi phí nhân viên / Chi phí công ty', 'Thành tiền theo giá xử lý × % tương ứng; trên màn tính theo %, khi lưu chi phí công ty '
                                            'được ghi bằng chi phí nhân viên (BR-09).'),
    ('Trạng thái Đang tạo', 'Nhãn xám: biên bản lưu bằng Lưu / Lưu và tiếp tục; chỉ người tạo thấy và sửa.'),
    ('Trạng thái Chờ duyệt', 'Nhãn cam: đã Lưu và gửi duyệt; không sửa được; người có quyền Duyệt nhận thông báo.'),
    ('Trạng thái Đã duyệt', 'Nhãn xanh lá: đã Duyệt, hệ thống đã ghi bút toán; không sửa / duyệt lại được.'),
    ('Cấu trúc phân cấp', 'Biên bản > các phiếu kiểm kê (có ô tích chọn) > các dòng hàng thừa / thiếu; mỗi dòng > một phiếu xử lý.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn kiểm quyền theo tên quyền (giống hệ thống cũ, vai trò gán từ hệ thống cũ vẫn có hiệu lực); không gắn quyền cho thao tác Xem / '
    'In / Xuất / Lịch sử — mọi người dùng đăng nhập vào được màn và thấy biên bản trong phạm vi. Super admin được coi như có đủ quyền.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1, 'Thấy nút Tạo mới; bấm được Lấy dữ liệu; lưu được biên bản mới. Quyền dùng chung của nhóm Kế toán kho.'),
    ('Q2', Q2, 'Thấy nút Duyệt (dòng và màn chi tiết) ở biên bản Chờ duyệt; sửa được Giá xử lý, %, NV chịu trước khi Duyệt; thấy '
               'mọi biên bản Chờ duyệt; nhận thông báo khi có biên bản gửi duyệt cùng công ty.'),
    ('—', 'Người tạo biên bản', 'Sửa (dòng và màn chi tiết) khi biên bản còn Đang tạo; Lưu và gửi duyệt từ màn Sửa.'),
], widths=[0.8, 1.8, 3.4])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Mọi biên bản của mọi công ty (Super admin như V1).'),
    ('V2', V2, 'Biên bản của công ty người xem + biên bản mình tạo; công ty người xem trống → chỉ biên bản mình tạo.'),
    ('—', 'Không có quyền nào', 'Chỉ biên bản do chính mình tạo (có Q2 thì thêm mọi biên bản Chờ duyệt).'),
], widths=[0.8, 2.2, 3.0])
d.p('Với mọi quyền: biên bản Đang tạo chỉ hiện với chính người tạo. Xem chi tiết / In / Xuất / Lịch sử áp cùng phạm vi.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'V1', 'V2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ theo V', '✅ + mọi Chờ duyệt', '✅ mọi công ty', '✅ công ty mình + của mình', '✅ chỉ của mình'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo biên bản', '✅', '❌', '❌', '❌', '❌'),
    ('FR-06 Lấy dữ liệu, nhập xử lý', '✅', '❌', '❌', '❌', '❌'),
    ('FR-07 Lưu và gửi duyệt', '✅ (tạo) / người tạo (sửa)', '❌', '❌', '❌', '❌ (trừ người tạo ở màn Sửa)'),
    ('FR-08 Chỉnh sửa', '✅ người tạo, Đang tạo', '❌', '❌', '❌', '✅ người tạo, Đang tạo'),
    ('FR-09 Xem chi tiết', '✅ trong phạm vi', '✅ + Chờ duyệt', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-10 Duyệt biên bản', '❌', '✅ Chờ duyệt', '❌', '❌', '❌'),
    ('FR-11 In biên bản, In danh sách', '✅', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-12 Xuất Excel', '✅', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-13 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('Xóa / Không duyệt / Hủy / Khóa – Mở khóa / Import', '—', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.7, 0.9, 0.9, 0.8, 0.9, 0.8])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Thiếu Q1: không thấy nút Tạo mới; mở thẳng màn Tạo vẫn hiện form nhưng bấm Lấy dữ liệu / Lưu → hệ thống báo ' + NOPERM + '.',
    'Thiếu Q2: không thấy nút Duyệt; biên bản Chờ duyệt của người khác không nằm trong danh sách (trừ khi có V1 / V2 phù hợp).',
    'Mở chi tiết / sửa / in / xuất / lịch sử của biên bản ngoài phạm vi (qua đường link): hệ thống báo ' + NOTFOUND +
    '; màn chi tiết / sửa chuyển sang trang “Không tìm thấy trang”.',
    'Mở màn Sửa của biên bản không còn Đang tạo hoặc không phải mình tạo → tự chuyển về màn chi tiết. Lưu khi biên bản vừa đổi trạng '
    'thái ở tab khác → báo ' + CONFLICT + '.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới', 'Có Q1 (hoặc Super admin)', 'Cờ do máy chủ trả, mặc định ẩn'),
    ('Nút Xuất Excel, In danh sách, Cấu hình cột', 'Luôn hiện', 'Theo phạm vi xem'),
    ('Nút Sửa (dòng và màn chi tiết)', 'Người xem là người tạo và biên bản Đang tạo', 'Máy chủ kiểm lại khi lưu'),
    ('Nút Duyệt (dòng và màn chi tiết)', 'Biên bản Chờ duyệt và người xem có Q2', 'Nút ở dòng chỉ mở màn chi tiết'),
    ('Nút In, Xuất Excel, Lịch sử trên dòng', 'Mọi dòng', 'Tối đa 3 nút hiện thẳng, còn lại vào menu “Hành động khác”'),
    ('Ô Giá xử lý, % chi phí, NV chịu ở màn chi tiết', 'Biên bản Chờ duyệt và người xem có Q2', 'Lý do vẫn chỉ đọc'),
], widths=[2.2, 2.3, 1.5])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_KT, [0, 1, 2, 3, 4, 6, 7]), (A_DUYET, [0, 5, 6, 7])],
    [('FR-01', 'Xem danh sách biên bản', 'view'),
     ('FR-05', 'Tạo biên bản', 'crud'),
     ('FR-06', 'Lấy dữ liệu, nhập xử lý', 'crud'),
     ('FR-07', 'Lưu và gửi duyệt', 'action'),
     ('FR-08', 'Chỉnh sửa biên bản', 'crud'),
     ('FR-10', 'Duyệt biên bản', 'action'),
     ('FR-11', 'In biên bản / In danh sách', 'io'),
     ('FR-12', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-09', 'Xem chi tiết', 'view', 'extend', [0], None),
     ('FR-13', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Biên bản xử lý hàng thừa, thiếu sau kiểm kê')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách biên bản',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách biên bản xử lý hàng thừa, thiếu sau kiểm kê',
       mota='Hiển thị bảng các biên bản trong phạm vi xem của người dùng (theo quyền tổng công ty / công ty / của mình, người có '
            'quyền Duyệt thấy thêm biên bản Chờ duyệt), kèm ngày tạo, kho, tổng số lượng hàng thừa / thiếu, người tạo, người duyệt, '
            'ngày duyệt, trạng thái, phân trang và tổng số. Mỗi dòng có liên kết sang màn chi tiết và các nút thao tác theo trạng thái.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng vào màn từ menu hoặc bấm thông báo biên bản chờ duyệt.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem theo quyền (V1 / V2 / của mình, + Chờ duyệt nếu có Q2), luôn ẩn biên bản Đang tạo của '
             'người khác.\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu vừa đi vào màn con của màn này) và cấu hình cột đã '
             'lưu của người dùng.\n'
             '4. Hệ thống lấy biên bản khớp bộ lọc, sắp biên bản tạo gần nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, kèm dòng “Hiển thị a–b / N”, phân trang và nút thao tác theo trạng thái; '
             'nút Tạo mới chỉ hiện khi có quyền Kế toán kho.',
       phu='• Không có biên bản nào khớp → trong bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Máy chủ lỗi khi nạp danh sách → thông báo “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”, bảng trống.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
           '• Bấm thông báo “[BBXLKKHH] Chờ duyệt: <số phiếu>” → mở thẳng màn chi tiết biên bản đó.\n'
           '• Phiên đăng nhập hết hạn khi đang thao tác → thông báo hết phiên, hệ thống xóa phiên và chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 11 cột (STT, Số phiếu, Ngày tạo, Kho, Hàng thừa, Hàng thiếu, Người tạo, Người duyệt, Ngày '
               'duyệt, Trạng thái, Hành động); không có cột ẩn mặc định. Cột khóa (không ẩn, không đổi vị trí): STT, Số phiếu, Hành '
               'động; Số phiếu ghim trái khi cuộn ngang. Sắp xếp được: Số phiếu, Ngày tạo, Kho, Hàng thừa, Hàng thiếu, Ngày duyệt; '
               'mặc định (chưa chọn cột) ngày tạo mới nhất ở trên, không cột nào có mũi tên. Đổi sắp xếp / bộ lọc / số dòng đều về '
               'trang 1. Bảng cố định bề rộng cột để không nhảy cột khi sắp xếp.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn danh sách Biên bản xử lý hàng thừa, thiếu sau kiểm kê'),
   extra=[(shot('03b_rowmenu_wait'), 'Dòng Chờ duyệt (người có quyền Duyệt): Duyệt, In và menu Hành động khác chứa Xuất Excel, Lịch sử')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Danh sách biên bản xử lý hàng thừa, thiếu sau kiểm kê” trên tiêu đề bảng và tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền',
        ['- Chỉ hiện khi có quyền Kế toán kho', '- Rê chuột: “Tạo biên bản xử lý hàng thừa, thiếu sau kiểm kê”',
         '- Bấm → mở màn Tạo biên bản (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.12)',
         '- Khóa trong lúc đang xuất file']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “In danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.11)']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa trong Tùy chỉnh cột']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', 'BBXLKKHH-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết (mục 2.9)', '- Sắp xếp được', '- Cột khóa, ghim trái khi cuộn ngang']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', ['- Thời điểm lưu lần đầu', '- Sắp xếp được']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Tên kho vật lý của biên bản', '- Kẹp 2 dòng khi dài', '- Sắp xếp được (theo tên kho)']),
       ('Cột Hàng thừa', 'Table/Grid', 'Read-only', '≥ 0', 'Hiển thị',
        ['- Tổng SL các dòng hàng thừa đã lưu, căn phải, dấu phẩy ngăn nghìn', '- Bằng 0 vẫn hiện “0”', '- Sắp xếp được']),
       ('Cột Hàng thiếu', 'Table/Grid', 'Read-only', '≥ 0', 'Hiển thị',
        ['- Tổng SL các dòng hàng thiếu (số dương), căn phải', '- Bằng 0 vẫn hiện “0”', '- Sắp xếp được']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Họ tên người lập biên bản', '- Không sắp xếp']),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Họ tên người đã Duyệt', '- Trống khi chưa duyệt', '- Không sắp xếp']),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', ['- Trống khi chưa duyệt', '- Sắp xếp được']),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 3 giá trị', 'Hiển thị',
        ['- Đang tạo: nhãn xám', '- Chờ duyệt: nhãn cam', '- Đã duyệt: nhãn xanh lá', '- Không sắp xếp']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Sửa (bút chì): biên bản Đang tạo của chính mình → mở màn Sửa (mục 2.8)',
           '- Duyệt (dấu tích): biên bản Chờ duyệt, người xem có quyền Duyệt → mở màn chi tiết để duyệt (mục 2.10)',
           '- In, Xuất Excel, Lịch sử: mọi dòng (mục 2.11, 2.12, 2.13)',
           '- Hiện thẳng tối đa 3 nút; nhiều hơn thì nút cuối là “Hành động khác” (ba chấm) chứa phần còn lại',
           '- Cột khóa trong Tùy chỉnh cột']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', ['- Trong bảng: “Không có dữ liệu phù hợp.”', '- Chỉ hiện khi N = 0']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang đang xem', '- N: tổng số biên bản khớp bộ lọc trong phạm vi xem']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        ['- Nút về đầu, lùi, số trang, tiến, về cuối', '- Ở trang đầu nút về đầu / lùi mờ; ở trang cuối nút tiến / về cuối mờ']),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.” khi máy chủ lỗi.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định phạm vi xem: V1 (hoặc Super admin) → mọi công ty; V2 → công ty mình + của mình; không quyền → của mình; '
        'có Q2 → thêm mọi biên bản Chờ duyệt.\n'
        '– Khôi phục bộ lọc (10 phút) và cấu hình cột đã lưu.\n'
        'During:\n– Lấy biên bản khớp bộ lọc; ẩn biên bản Đang tạo của người khác.\n'
        '– Máy chủ lỗi → hiển thị “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, biên bản tạo mới nhất ở trên, nút thao tác theo cờ từng biên bản; nút Tạo mới theo quyền '
        'Kế toán kho.'),
       ('Bấm Số phiếu', 'Click',
        'Before:\n– Biên bản nằm trong phạm vi xem.\n'
        'After:\n– Mở màn chi tiết (mục 2.9); bộ lọc được ghi nhớ 10 phút để khôi phục khi quay lại.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Số phiếu, Ngày tạo, Kho, Hàng thừa, Hàng thiếu, Ngày duyệt hỗ trợ sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc; cùng giá trị thì biên bản mới hơn ở trên.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại một lần theo số dòng mới.'),
       ('Bấm Hành động khác (ba chấm)', 'Click',
        'Before:\n– Dòng có nhiều hơn 3 nút thao tác (dòng Đang tạo của mình: Sửa, In, Xuất Excel, Lịch sử; dòng Chờ duyệt với người '
        'có quyền Duyệt: Duyệt, In, Xuất Excel, Lịch sử).\n'
        'After:\n– Mở menu các nút còn lại (Xuất Excel, Lịch sử).'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc biên bản',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách biên bản',
       mota='Thu hẹp danh sách theo số phiếu, kho, trạng thái, người tạo, người duyệt và ngày tạo. Ô tìm nhanh tìm theo số phiếu; '
            'các ô lọc nằm trong khối Tìm kiếm nâng cao, bật / tắt được bằng Cài đặt bộ lọc (mục 2.3). Mọi tiêu chí chỉ thu hẹp '
            'trong phạm vi xem theo quyền.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập số phiếu vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn một hoặc nhiều tiêu chí.\n'
             '3. Hệ thống lọc ngay khi một ô chọn đổi giá trị, về trang 1; ô tìm nhanh chỉ áp khi bấm Tìm kiếm / Enter.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Ô Người tạo / Người duyệt chỉ liệt kê người đã tạo / đã duyệt biên bản trong phạm vi xem; chưa có ai duyệt → ô Người '
           'duyệt không có lựa chọn.\n'
           '• Ô lọc bị tắt trong Cài đặt bộ lọc → không hiện trên khối lọc.',
       dacbiet='Ô tìm nhanh khớp một phần số phiếu, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối; không giới hạn số ký '
               'tự; ký tự % và _ được hiểu là ký tự đại diện. Ngày tạo lấy trọn hai ngày biên (theo ngày tạo biên bản, KHÔNG phải '
               'Từ ngày – Đến ngày kiểm kê). Mọi điều kiện kết hợp kiểu VÀ. Ghi nhớ bộ lọc trên trình duyệt 10 phút khi đi vào màn '
               'con của màn này.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo số phiếu”', '- Khớp một phần số phiếu', '- Áp khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', ['- Bấm → xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, nạp lại từ trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Kho', 'Dropdown', 'Enable', 'Danh sách kho', 'Không', 'Trống',
        ['- Mặc định: trống (mọi kho)', '- Hiển thị “Mã - Tên”, gồm mọi kho vật lý trong danh mục', '- Ra biên bản của kho đã chọn']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (mọi trạng thái)', '- Lựa chọn: Đang tạo / Chờ duyệt / Đã duyệt']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Người đã tạo biên bản trong phạm vi xem, hiển thị “Họ tên - Mã phòng ban - Mã nhân viên”']),
       ('Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Người đã duyệt biên bản trong phạm vi xem']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lọc theo ngày tạo biên bản, lấy trọn hai ngày biên; được bỏ trống một đầu']),
   ],
   ev=[
       ('Đổi giá trị một ô chọn', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\n'
        'During:\n– Bỏ qua khi giá trị không đổi.\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí (một lần).'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm biên bản có số phiếu chứa chuỗi nhập (không phân biệt hoa / thường).\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\nAfter:\n– Xóa mọi tiêu chí, bỏ sắp xếp, nạp lại từ trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\nAfter:\n– Mở / thu gọn khối ô lọc; lần mở đầu nạp lựa chọn Kho, Trạng thái, '
        'Người tạo, Người duyệt.'),
       ('Quay lại từ màn con trong 10 phút', 'System',
        'Before:\n– Người dùng vừa đi từ danh sách vào màn chi tiết / tạo / sửa.\n'
        'After:\n– Khôi phục bộ lọc, sắp xếp và trạng thái khối lọc; quá 10 phút thì bộ lọc về trống.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự. Cấu hình lưu riêng theo '
            'người dùng cho màn này, không ảnh hưởng người khác và không đổi dữ liệu biên bản.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 5 mục lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 5 mục theo thứ tự thiết kế; phải bấm Lưu mới có hiệu lực.\n'
           '• Bỏ tích mục đang có giá trị lọc → mục bị ẩn và giá trị lọc của mục đó bị bỏ.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ → đóng, bỏ thay đổi chưa lưu.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Cài đặt bộ lọc”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường lọc muốn hiển thị; kéo để sắp xếp thứ tự. Cài đặt được lưu theo từng màn hình.”'),
       ('Danh sách mục lọc', 'Table/Grid', 'Enable', 'Danh sách 5 mục', '–', 'Theo cấu hình đã lưu',
        ['- Kho, Trạng thái, Người tạo, Người duyệt, Ngày tạo']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → mục đó không hiện ở khối Tìm kiếm nâng cao.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích lại đủ 5 mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Vùng ngoài cửa sổ', 'Popup', 'Enable', '–', '–', 'Hiển thị', '- Click ra ngoài cửa sổ → đóng như nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình đang lưu (chưa lưu lần nào → đủ 5 mục).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\n'
        'During:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ 5 mục, thứ tự thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
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
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 11 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ nguyên sau khi tải lại trang, đăng '
               'nhập lại, đổi trình duyệt; người dùng khác không bị ảnh hưởng. Cấu hình cột không đổi bộ trường xuất Excel.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 11 cột', '–', 'Theo cấu hình đã lưu',
        ['- STT, Số phiếu, Ngày tạo, Kho, Hàng thừa, Hàng thiếu',
         '- Người tạo, Người duyệt, Ngày duyệt, Trạng thái, Hành động']),
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
       ('Bấm Đóng, (x) hoặc click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ dùng chung form
ROW_UI = [
    ('Ô Lý do (từng dòng)', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống',
     ['- Gợi ý “Nhập lý do”', '- Không gõ quá 255 ký tự', '- Lỗi: “Lý do – Vui lòng nhập lý do.”']),
    ('Ô Giá xử lý (từng dòng)', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Có', 'Giá vốn',
     ['- Mặc định: Giá vốn', '- Lựa chọn: Giá vốn / Giá bán', '- Bấm (x) xoá → trống, lỗi “Giá xử lý – Vui lòng chọn giá xử lý.”']),
    ('Ô % Chi phí nhân viên (từng dòng)', 'Textbox', 'Enable', '0 – 100, tối đa 2 số lẻ', 'Có', '100',
     ['- Gợi ý “Nhập %”, chỉ nhận số', '- Gõ số → % Chi phí công ty tự = 100 − số đã gõ',
      '- Lỗi: “% Chi phí nhân viên – Vui lòng nhập.” / “% Chi phí nhân viên – Từ 0 đến 100.”']),
    ('Ô % Chi phí công ty (từng dòng)', 'Textbox', 'Enable', '0 – 100, tối đa 2 số lẻ', 'Có', '0',
     ['- Gõ số → % Chi phí nhân viên tự = 100 − số đã gõ', '- Gõ quá 100 → ô bên kia về trống, báo “% Chi phí – Từ 0 đến 100.”',
      '- Lỗi trống: “% Chi phí công ty – Vui lòng nhập.”']),
    ('Ô NV chịu (từng dòng)', 'Dropdown', 'Enable', 'Nhân viên đang làm việc', 'Có', 'Trống',
     ['- Gợi ý “Chọn nhân viên chịu”', '- Hiển thị “Họ tên - Mã phòng ban - Mã nhân viên”',
      '- Lỗi: “NV chịu – Vui lòng chọn nhân viên chịu.”']),
]

FORM_UI = [
    ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     ['- Tạo: “Tạo biên bản xử lý hàng thừa, thiếu sau kiểm kê”', '- Sửa: “Sửa biên bản xử lý hàng thừa, thiếu: <số phiếu>”']),
    ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập',
     '- Góc phải khối Thông tin chung: “<Người tạo> - dd/mm/yyyy hh:mm” (màn Tạo: người đăng nhập, thời điểm mở màn).'),
    ('Ô Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Trống',
     ['- Gợi ý “Chọn từ ngày”', '- Lỗi: “Từ ngày – Vui lòng chọn từ ngày.”']),
    ('Ô Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Trống',
     ['- Gợi ý “Chọn đến ngày”; lịch làm mờ các ngày trước Từ ngày',
      '- Lỗi: “Đến ngày – Vui lòng chọn đến ngày.” / “Đến ngày – Phải lớn hơn hoặc bằng Từ ngày.”']),
    ('Ô Kho vật lý', 'Dropdown', 'Enable', 'Danh sách kho', 'Có', 'Trống',
     ['- Gợi ý “Chọn kho vật lý”, hiển thị “Mã - Tên”, gồm mọi kho vật lý', '- Lỗi: “Kho vật lý – Vui lòng chọn kho vật lý.”']),
    ('Ô Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     ['- Gợi ý “Nhập ghi chú”, 2 dòng', '- Không gõ quá 255 ký tự; lỗi “Ghi chú – Tối đa 255 ký tự.”']),
    ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, png, jpg, jpeg; ≤ 20MB/file; ≤ 20 file', 'Không', 'Trống',
     ['- Nút “Thêm tài liệu” chọn file; bảng STT, Upload / File, Dung lượng',
      '- Lỗi: “Chỉ nhận file pdf, png, jpg, jpeg” / “Dung lượng tối đa 20MB” / “File đính kèm – Tối đa 20 file.”']),
    ('Khối Phiếu kiểm kê', 'Checkbox', 'Enable', 'Theo dữ liệu lấy được', '–', 'Trống',
     ['- Chưa lấy dữ liệu: “Chọn Từ ngày, Đến ngày, Kho vật lý rồi bấm "Lấy dữ liệu".”',
      '- Sau khi lấy: mỗi phiếu kiểm kê 1 ô tích (mặc định tích) + số phiếu là liên kết mở phiếu ở tab mới',
      '- Bỏ tích → các dòng của phiếu đó biến khỏi 2 tab và không được lưu']),
    ('Nút Lấy dữ liệu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Ở đầu khối Chi tiết (dấu * ở tiêu đề khối)', '- Rê chuột: “Lấy kết quả các phiếu kiểm kê theo hàng hóa đã hoàn thành của kho '
      'trong khoảng ngày”', '- Đặc tả ở mục 2.6; khóa trong lúc đang lấy']),
    ('Thanh tab Hàng thừa (n), Hàng thiếu (n)', 'Button', 'Enable', '–', '–', 'Hàng thừa',
     ['- n = số dòng của tab', '- Tab có ô lỗi hiện dấu báo lỗi; lỗi chỉ nằm ở tab đang ẩn thì tự chuyển sang tab đó']),
    ('Bảng chi tiết 18 cột', 'Table/Grid', 'Read-only', '–', '–', 'Không có dữ liệu',
     ['- STT, Tên hàng, Model, Mã hàng, Mã kho, SL, Đơn giá bán, Thành tiền bán, Đơn giá vốn, Thành tiền vốn, Phiếu xử lý',
      '- Lý do*, Giá xử lý*, % Chi phí nhân viên*, % Chi phí công ty*, NV chịu*, Chi phí nhân viên, Chi phí công ty',
      '- Rỗng: “Không có dữ liệu”; cuộn trong khung cao tối đa 600px, tiêu đề cột dính khi cuộn']),
    ('Cột SL, Đơn giá, Thành tiền', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
     ['- SL = trị tuyệt đối chênh lệch', '- Thành tiền bán = Đơn giá bán × SL; Thành tiền vốn = Đơn giá vốn × SL',
      '- Số 0 hiện “0”; tối đa 3 số lẻ, dấu phẩy ngăn nghìn']),
    ('Cột Phiếu xử lý', 'Link', 'Read-only', '–', '–', 'Theo dữ liệu',
     ['- Số phiếu nhập / xuất kho điều chỉnh kiểm kê', '- Bấm → mở phiếu trên hệ thống cũ (ERP) ở tab mới; không có phiếu → trống']),
] + ROW_UI + [
    ('Cột Chi phí nhân viên, Chi phí công ty', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
     ['- = Thành tiền vốn (Giá vốn) hoặc Thành tiền bán (Giá bán) × % tương ứng', '- Tự tính lại khi đổi Giá xử lý / %',
      '- Không làm tròn, tối đa 3 số lẻ']),
    ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Rê chuột: “Lưu biên bản ở trạng thái Đang tạo”', '- Lưu xong về danh sách; khóa trong lúc lưu']),
    ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
     ['- Màu chính; rê chuột: “Lưu và gửi người có quyền duyệt”', '- Đặc tả ở mục 2.7']),
    ('Nút Lưu và tiếp tục', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị ở màn Tạo',
     ['- Rê chuột: “Lưu (Đang tạo) rồi ở lại tạo biên bản tiếp theo”', '- Không có ở màn Sửa']),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách; có thay đổi thì hỏi “Thông tin chưa lưu”.'),
    ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Nội dung: “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”', '- Nút Thoát: rời màn, không lưu',
      '- Nút Ở lại hoặc (x): đóng hộp, giữ dữ liệu']),
    ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
     ['- Thành công: “Lưu thành công.” / “Lưu và gửi duyệt thành công.”', '- Thiếu / sai: ' + MISS,
      '- Dữ liệu kiểm kê đổi: ' + CHANGED, '- Biên bản đã đổi trạng thái: ' + CONFLICT,
      '- Lỗi khác: câu lỗi của máy chủ hoặc “Lưu thất bại.”']),
]

SAVE_DURING = ('During:\n– Từ ngày / Đến ngày / Kho vật lý trống → câu lỗi “… – Vui lòng chọn …” dưới ô; Đến ngày trước Từ ngày → '
               '“Đến ngày – Phải lớn hơn hoặc bằng Từ ngày.”\n'
               '– Chưa có dòng (chưa Lấy dữ liệu hoặc bỏ tích hết phiếu) → “Chi tiết – Chưa có hàng thừa, thiếu. Vui lòng bấm '
               '"Lấy dữ liệu".”\n'
               '– Đã đổi Từ ngày / Đến ngày / Kho vật lý sau lần Lấy dữ liệu → “Chi tiết – Từ ngày / Đến ngày / Kho vật lý đã đổi. '
               'Vui lòng bấm "Lấy dữ liệu" lại.”\n'
               '– Mỗi dòng đang hiện: Lý do, Giá xử lý, % Chi phí nhân viên (0 – 100), % Chi phí công ty, NV chịu trống / sai → lỗi '
               'tại ô; Ghi chú quá 255 ký tự → “Ghi chú – Tối đa 255 ký tự.”\n'
               '– Mọi lỗi hiện cùng lúc, thông báo ' + MISS + ', chuyển sang tab có lỗi, cuộn tới ô lỗi đầu tiên.\n'
               '– Máy chủ lấy lại kết quả kiểm kê: khác bộ hàng đang gửi → ' + CHANGED + '.\n' + ERR)

fr(5, 'Tạo biên bản (Lưu / Lưu và tiếp tục)', usecase=('FR-05', 'Tạo biên bản', 'crud', A_KT),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo biên bản xử lý hàng thừa, thiếu sau kiểm kê',
       mota='Kế toán kho chọn Từ ngày, Đến ngày, Kho vật lý, bấm Lấy dữ liệu để nạp kết quả các phiếu kiểm kê Hoàn thành (mục 2.6), '
            'nhập cách xử lý cho từng dòng rồi bấm Lưu: biên bản được lưu ở trạng thái Đang tạo (chỉ người tạo thấy), chưa báo cho '
            'ai. Lưu và Lưu và gửi duyệt bắt CÙNG một bộ trường bắt buộc (như hệ thống cũ).',
       tacnhan=TN_KT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có quyền “%s” (nút Tạo mới chỉ hiện khi có quyền).\n'
                '3. Kho đã chọn có ít nhất 1 phiếu kiểm kê theo hàng hóa Hoàn thành, ngày kiểm kê trong khoảng, có hàng chênh lệch.' % Q1,
       chinh='1. Người dùng bấm Tạo mới ở danh sách.\n'
             '2. Hệ thống mở màn “Tạo biên bản xử lý hàng thừa, thiếu sau kiểm kê”: mọi ô trống, khối Phiếu kiểm kê nhắc “Chọn Từ '
             'ngày, Đến ngày, Kho vật lý rồi bấm "Lấy dữ liệu".”, 2 tab Hàng thừa (0) / Hàng thiếu (0).\n'
             '3. Người dùng chọn Từ ngày, Đến ngày, Kho vật lý, nhập Ghi chú, thêm File đính kèm (nếu có).\n'
             '4. Người dùng bấm Lấy dữ liệu và nhập Lý do, Giá xử lý, %, NV chịu cho từng dòng ở 2 tab (mục 2.6).\n'
             '5. Người dùng bấm Lưu.\n'
             '6. Hệ thống kiểm tra dữ liệu, lấy lại kết quả kiểm kê từ máy chủ, lưu biên bản trạng thái Đang tạo với công ty / phòng '
             'ban của người tạo, sinh mã BBXLKKHH-NNNNN, ghi các dòng (SL, giá, phiếu xử lý, chi phí) và tổng SL thừa / thiếu.\n'
             '7. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của biên bản.\n'
             '8. Hệ thống hiển thị “Lưu thành công.” và chuyển về màn danh sách.',
       phu='• Bấm Lưu và tiếp tục → lưu như Lưu (Đang tạo), báo “Lưu thành công.”, ở lại màn Tạo với form trắng.\n'
           '• Thiếu / sai dữ liệu → báo lỗi dưới từng ô cùng lúc, thông báo ' + MISS + ', không lưu.\n'
           '• Kết quả kiểm kê đổi giữa lúc Lấy dữ liệu và lúc lưu → ' + CHANGED + ', không lưu.\n'
           '• Không có quyền Kế toán kho (mở thẳng màn Tạo) → ' + NOPERM + ' khi Lấy dữ liệu / Lưu.\n'
           '• Bấm Quay lại / chuyển menu / đóng tab khi đã nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì thì về '
           'danh sách ngay. Màn là trang riêng, không có (x) / click ra ngoài.\n'
           '• Lỗi máy chủ → thông báo câu lỗi hoặc “Lưu thất bại.”, dữ liệu đã nhập giữ nguyên.',
       dacbiet='Các nút lưu khóa trong lúc đang lưu để một lần bấm không tạo 2 biên bản. Biên bản không có trường nhập duy nhất: mã '
               'tự sinh theo số thứ tự, không sửa được; hai biên bản cùng kho, cùng khoảng ngày, cùng phiếu kiểm kê vẫn lưu được '
               '(hệ thống không chặn lập trùng — BR-10). Số lượng, giá, phiếu xử lý không lấy từ màn hình mà máy chủ lấy lại khi lưu. '
               'Không có hộp xác nhận khi lưu.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10_create'), shot_caption='Màn Tạo biên bản lúc mới mở'),
   extra=[(shot('10b_validate'), 'Lỗi bắt buộc hiện dưới Từ ngày, Đến ngày, Kho vật lý khi bấm Lấy dữ liệu lúc form trống'),
          (shot('10g_unsaved'), 'Hộp “Thông tin chưa lưu” khi rời màn')],
   ui=FORM_UI[:1] + FORM_UI[1:],
   ev=[
       ('Mở màn Tạo', 'System',
        'Before:\n– Nút Tạo mới chỉ hiện khi có quyền Kế toán kho.\nDuring:\n– Nạp danh sách kho vật lý, nhân viên đang làm việc '
        '(ô NV chịu), người tạo.\n– Lỗi → “Không tải được danh sách kho / nhân viên.”.\nAfter:\n– Hiển thị form trống; chưa tính '
        'là đã thay đổi.'),
       ('Chọn Từ ngày / Đến ngày / Kho vật lý', 'Change',
        'Before:\n– Bỏ qua khi giá trị không đổi.\nAfter:\n– Ghi nhận giá trị, xóa lỗi đỏ của ô; lịch Đến ngày làm mờ ngày trước Từ '
        'ngày. Đổi sau khi đã Lấy dữ liệu → khi lưu bị nhắc Lấy dữ liệu lại.'),
       ('Thêm file đính kèm', 'Click',
        'Before:\n– Chỉ nhận pdf, png, jpg, jpeg, mỗi file ≤ 20MB.\nDuring:\n– Sai đuôi → “Chỉ nhận file pdf, png, jpg, jpeg”; quá '
        'dung lượng → “Dung lượng tối đa 20MB”.\nAfter:\n– File tải lên kho lưu trữ, hiện trong bảng; chỉ gắn vào biên bản khi lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán kho; không có → ' + NOPERM + ' và dừng xử lý.\n– Khóa các nút lưu.\n' + SAVE_DURING + '\n'
        'After:\n– Lưu biên bản trạng thái Đang tạo, sinh số phiếu, ghi các dòng và tổng SL thừa / thiếu, gắn file đính kèm.\n'
        '– Ghi một dòng lịch sử “Tạo mới”.\n– Hiển thị “Lưu thành công.”, về màn danh sách.'),
       ('Bấm Lưu và tiếp tục', 'Click',
        'Before:\n– Như Lưu.\nDuring:\n– Kiểm tra như Lưu.\n' + ERR + '\n'
        'After:\n– Lưu như Lưu (Đang tạo), ghi lịch sử “Tạo mới”, hiển thị “Lưu thành công.”, làm trắng form và ở lại màn Tạo.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu hiện tại với lúc mở màn (ngày, kho, ghi chú, tích phiếu, ô nhập từng dòng, file mới).\n'
        'During:\n– Có thay đổi → hiện hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu; Ở lại: giữ nguyên form.'),
   ])

# ------------------------------------------------------------ 2.6 Lấy dữ liệu
fr(6, 'Lấy dữ liệu kiểm kê và nhập xử lý từng dòng', usecase=('FR-06', 'Lấy dữ liệu, nhập xử lý', 'crud', A_KT),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lấy dữ liệu kiểm kê và nhập cách xử lý cho từng dòng hàng thừa / thiếu',
       mota='Nút Lấy dữ liệu nạp kết quả các phiếu kiểm kê theo hàng hóa đã Hoàn thành của kho đã chọn, có ngày kiểm kê trong khoảng '
            'Từ ngày – Đến ngày: mỗi hàng của mỗi phiếu là 1 dòng (chênh lệch cộng dồn, bỏ chênh 0), chia vào tab Hàng thừa / Hàng '
            'thiếu. Đơn giá vốn, Phiếu xử lý, Mã kho lấy từ phiếu nhập (ưu tiên) hoặc xuất kho điều chỉnh kiểm kê đã Hoàn thành. '
            'Người dùng tích / bỏ tích phiếu kiểm kê và nhập Lý do, Giá xử lý, %, NV chịu cho từng dòng; chi phí tự tính.',
       tacnhan=TN_KT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có quyền “%s”.\n3. Đang ở màn Tạo, hoặc màn Sửa của biên bản Đang tạo '
                'do mình tạo; đã chọn Từ ngày, Đến ngày, Kho vật lý.' % Q1,
       chinh='1. Người dùng bấm Lấy dữ liệu.\n'
             '2. Hệ thống kiểm tra 3 ô Từ ngày, Đến ngày, Kho vật lý.\n'
             '3. Hệ thống lấy phiếu kiểm kê theo hàng hóa Hoàn thành có kho đã chọn, ngày kiểm kê trong khoảng; cộng chênh lệch '
             'thực kiểm theo từng hàng của từng phiếu, bỏ hàng chênh 0.\n'
             '4. Hệ thống ghép giá vốn, số phiếu xử lý, mã kho kế toán từ phiếu nhập kho điều chỉnh kiểm kê (nếu không có thì phiếu '
             'xuất kho điều chỉnh kiểm kê) Hoàn thành của cùng phiếu kiểm kê và cùng hàng.\n'
             '5. Hệ thống hiện khối Phiếu kiểm kê (mỗi phiếu 1 ô tích, mặc định tích), chia dòng vào tab Hàng thừa (chênh > 0) và Hàng '
             'thiếu (chênh < 0), mỗi dòng mặc định Giá xử lý = Giá vốn, % nhân viên 100, % công ty 0; mở tab có dữ liệu.\n'
             '6. Người dùng nhập Lý do, chọn Giá xử lý, sửa % (ô kia tự = 100 − %), chọn NV chịu cho từng dòng; hệ thống tự tính '
             'Chi phí nhân viên / công ty.\n'
             '7. Người dùng bỏ tích phiếu kiểm kê không muốn xử lý → dòng của phiếu đó biến khỏi 2 tab.',
       phu='• Thiếu Từ ngày / Đến ngày / Kho vật lý → lỗi dưới ô, thông báo ' + MISS + ', không gọi máy chủ.\n'
           '• Không có kết quả chênh lệch → thông báo “Không có kết quả kiểm kê chênh lệch trong khoảng ngày của kho đã chọn.”, 2 '
           'tab trống.\n'
           '• Không có quyền Kế toán kho → ' + NOPERM + '.\n'
           '• Bấm Lấy dữ liệu lần nữa (đổi ngày / kho) → thay toàn bộ dòng; dòng còn trong dữ liệu mới giữ nguyên ô đã nhập và tích '
           'phiếu cũ.\n'
           '• Hàng không có phiếu nhập / xuất điều chỉnh kiểm kê → Đơn giá vốn 0, Phiếu xử lý và Mã kho trống.\n'
           '• Máy chủ lỗi → “Không lấy được dữ liệu.”.',
       dacbiet='Lấy dữ liệu chỉ đọc, không lưu gì. Phiếu xử lý mở ở hệ thống cũ (tab mới) đúng loại phiếu nhập / xuất. Chi phí trên '
               'màn tính không làm tròn (tối đa 3 số lẻ, như hệ thống cũ); khi lưu máy chủ làm tròn 2 số lẻ. Lỗi theo dòng hiện đúng '
               'tab của dòng.'),
   layout=dict(menu=MENU + ' => Tạo mới => Lấy dữ liệu', shot=shot('10c_filled'),
               shot_caption='Màn Tạo sau khi Lấy dữ liệu kho LN - Liên Ninh ngày 22/10/2026'),
   extra=[(shot('10d_rows'), 'Tab Hàng thừa: các cột chi tiết và ô nhập từng dòng'),
          (shot('10e_row_validate'), 'Lỗi từng dòng (Lý do, NV chịu trống) hiện tại ô'),
          (shot('10f_tab_thieu'), 'Tab Hàng thiếu')],
   ui=[
       ('Nút Lấy dữ liệu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → kiểm 3 ô rồi lấy dữ liệu', '- Khóa và hiện vòng quay trong lúc lấy']),
       ('Ô tích phiếu kiểm kê', 'Checkbox', 'Enable', 'Theo dữ liệu', '–', 'Đang tích',
        ['- Mỗi phiếu kiểm kê có hàng chênh lệch 1 ô', '- Bỏ tích → dòng của phiếu biến khỏi 2 tab, không được lưu']),
       ('Liên kết số phiếu kiểm kê', 'Link', 'Enable', '–', '–', 'Hiển thị',
        '- Rê chuột “Mở phiếu kiểm kê ở tab mới”; bấm → mở chi tiết phiếu kiểm kê theo hàng hóa ở tab mới.'),
       ('Tab Hàng thừa (n)', 'Button', 'Enable', '–', '–', 'Đang chọn', '- Dòng có chênh lệch > 0; n = số dòng.'),
       ('Tab Hàng thiếu (n)', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Dòng có chênh lệch < 0; n = số dòng.'),
       ('Cột Tên hàng, Model, Mã hàng', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Lấy từ hàng trên phiếu kiểm kê.'),
       ('Cột Mã kho', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        '- Mã các kho kế toán của phiếu xử lý, mỗi mã 1 dòng; trống khi không có phiếu xử lý.'),
       ('Cột Đơn giá bán', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', '- Giá bán của hàng trên phiếu kiểm kê.'),
       ('Cột Đơn giá vốn', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
        '- Giá nhập của phiếu nhập điều chỉnh kiểm kê hoặc giá xuất của phiếu xuất điều chỉnh kiểm kê; không có → 0.'),
       ('Cột Phiếu xử lý', 'Link', 'Read-only', '–', '–', 'Theo dữ liệu',
        '- Số phiếu nhập / xuất kho điều chỉnh kiểm kê; bấm → mở phiếu trên hệ thống cũ (ERP) ở tab mới.'),
   ] + ROW_UI + [
       ('Cột Chi phí nhân viên', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
        '- Thành tiền vốn (Giá vốn) hoặc Thành tiền bán (Giá bán) × % Chi phí nhân viên ÷ 100.'),
       ('Cột Chi phí công ty', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
        '- Cùng thành tiền × % Chi phí công ty ÷ 100 (trên màn); khi lưu được ghi bằng Chi phí nhân viên (BR-09).'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Không có dữ liệu: “Không có kết quả kiểm kê chênh lệch trong khoảng ngày của kho đã chọn.”',
         '- Thiếu ô: ' + MISS, '- Không quyền: ' + NOPERM, '- Lỗi khác: “Không lấy được dữ liệu.”']),
   ],
   ev=[
       ('Bấm Lấy dữ liệu', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán kho; không có → ' + NOPERM + ' và dừng xử lý.\n– Đang lấy thì bỏ qua lần bấm thêm.\n'
        'During:\n– Từ ngày / Đến ngày / Kho vật lý trống → lỗi dưới ô + ' + MISS + ', không gọi máy chủ.\n'
        '– Đến ngày trước Từ ngày → “Đến ngày – Phải lớn hơn hoặc bằng Từ ngày.”\n'
        '– Kho không còn tồn tại → “Kho vật lý – Không hợp lệ.”\n' + ERR + '\n'
        'After:\n– Thay danh sách phiếu kiểm kê và dòng chi tiết, giữ ô đã nhập của dòng cũ còn trong dữ liệu mới.\n'
        '– Mở tab Hàng thừa (hoặc Hàng thiếu nếu chỉ có hàng thiếu); không có dòng → “Không có kết quả kiểm kê chênh lệch …”.'),
       ('Tích / bỏ tích phiếu kiểm kê', 'Change',
        'Before:\n– Chỉ ở màn Tạo / Sửa.\nAfter:\n– Hiện / ẩn dòng của phiếu ở 2 tab, cập nhật số (n) trên tab, xóa lỗi cũ của các dòng.'),
       ('Nhập % Chi phí nhân viên hoặc % Chi phí công ty', 'Change',
        'Before:\n– Chỉ nhận số, tối đa 2 số lẻ.\nDuring:\n– Quá 100 → ô bên kia về trống, báo “% Chi phí – Từ 0 đến 100.”.\n'
        'After:\n– Ô bên kia = 100 − giá trị vừa nhập; tính lại Chi phí nhân viên / công ty của dòng.'),
       ('Đổi Giá xử lý', 'Change',
        'Before:\n– Lựa chọn Giá vốn / Giá bán; bấm (x) xoá → trống.\nAfter:\n– Tính lại chi phí theo thành tiền vốn hoặc bán; xóa '
        'lỗi đỏ của ô.'),
       ('Chọn NV chịu / nhập Lý do', 'Change',
        'Before:\n– NV chịu chọn trong danh sách nhân viên đang làm việc.\nAfter:\n– Ghi nhận giá trị, xóa lỗi đỏ của ô.'),
       ('Bấm số phiếu kiểm kê hoặc Phiếu xử lý', 'Click',
        'Before:\n– Liên kết có số phiếu.\nAfter:\n– Mở phiếu kiểm kê (hệ thống mới) hoặc phiếu nhập / xuất điều chỉnh kiểm kê '
        '(hệ thống cũ) ở tab mới; màn đang nhập giữ nguyên.'),
   ])

# ------------------------------------------------------------ 2.7 Lưu và gửi duyệt
fr(7, 'Lưu và gửi duyệt', usecase=('FR-07', 'Lưu và gửi duyệt', 'action', A_KT),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lưu và gửi duyệt (chuyển biên bản sang Chờ duyệt)',
       mota='Ở màn Tạo hoặc Sửa, nút Lưu và gửi duyệt lưu biên bản và chuyển sang trạng thái Chờ duyệt: biên bản không sửa được '
            'nữa, hiện với người có quyền Duyệt và người có quyền xem; nhân viên có quyền Duyệt cùng công ty người gửi nhận thông '
            'báo. Bộ trường bắt buộc giống nút Lưu. Không có hộp xác nhận (giữ như hệ thống cũ).',
       tacnhan=TN_KT + ' Sửa rồi gửi duyệt: người tạo khi biên bản Đang tạo.',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo (có quyền Kế toán kho) hoặc màn Sửa của biên bản Đang tạo do '
                'mình tạo.\n3. Đã Lấy dữ liệu và nhập đủ Lý do, Giá xử lý, %, NV chịu cho mọi dòng đang hiện.',
       chinh='1. Người dùng nhập đủ thông tin (như mục 2.5, 2.6) và bấm Lưu và gửi duyệt.\n'
             '2. Hệ thống kiểm tra dữ liệu như nút Lưu và lấy lại kết quả kiểm kê để đối chiếu.\n'
             '3. Hệ thống lưu biên bản với trạng thái Chờ duyệt (màn Tạo: sinh số phiếu; màn Sửa: kiểm lại biên bản còn Đang tạo và '
             'đúng người tạo).\n'
             '4. Hệ thống ghi nhận hành động trong lịch sử của biên bản: màn Tạo “Tạo mới” + “Thay đổi trạng thái” Đang tạo → Chờ '
             'duyệt; màn Sửa “Thay đổi thông tin” (nếu đổi dữ liệu) + “Thay đổi trạng thái”.\n'
             '5. Hệ thống gửi thông báo “[BBXLKKHH] Chờ duyệt: <số phiếu>” (ghi chú: Người lập, Kỳ, Kho, Thừa: a, thiếu: b, Ghi chú) '
             'cho nhân viên có quyền ' + Q2 + ' cùng công ty người gửi; bấm thông báo mở chi tiết biên bản.\n'
             '6. Hệ thống hiển thị “Lưu và gửi duyệt thành công.” và chuyển về màn danh sách.',
       phu='• Thiếu / sai dữ liệu → lỗi tại từng ô cùng lúc, thông báo ' + MISS + ', không lưu, không gửi.\n'
           '• Dữ liệu kiểm kê đổi → ' + CHANGED + '.\n'
           '• Biên bản đã bị đổi trạng thái (gửi ở tab khác) → ' + CONFLICT + ', không lưu.\n'
           '• Người gửi không có công ty / không ai có quyền Duyệt → vẫn lưu thành công, không ai nhận thông báo; lỗi gửi thông báo '
           'không ảnh hưởng việc lưu.',
       dacbiet='Không có hộp xác nhận; nút khóa trong lúc lưu. Sau khi Chờ duyệt, người tạo không sửa được và không có luồng trả về '
               'Đang tạo / Từ chối. Màn Tạo không có “Lưu và gửi duyệt rồi tiếp tục”.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới => Lưu và gửi duyệt', 'Gửi duyệt ngay khi tạo biên bản.'),
       (MENU + ' => Sửa => Lưu và gửi duyệt', 'Gửi duyệt biên bản Đang tạo đã lưu trước đó.')],
       shot=shot('10e_row_validate'), shot_caption='Lưu và gửi duyệt khi các dòng còn thiếu Lý do, NV chịu: lỗi hiện tại từng ô'),
   ui=[
       ('Nút Lưu và gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Màu chính, biểu tượng máy bay giấy', '- Rê chuột: “Lưu và gửi người có quyền duyệt”', '- Khóa trong lúc lưu']),
       ('Ô Từ ngày, Đến ngày, Kho vật lý', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Trống', '- Như mục 2.5; trống → lỗi dưới ô.'),
       ('Bảng chi tiết 2 tab', 'Table/Grid', 'Enable', '–', 'Có', 'Theo dữ liệu',
        ['- Phải có ít nhất 1 dòng (đã Lấy dữ liệu, có phiếu được tích)', '- Lỗi chung: “Chi tiết – Chưa có hàng thừa, thiếu. Vui '
         'lòng bấm "Lấy dữ liệu".”']),
   ] + ROW_UI + [
       ('Khung đỏ quanh bảng chi tiết', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Hiện khi có lỗi chung của khối Chi tiết.'),
       ('Dấu báo lỗi trên tab', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Tab có dòng lỗi được đánh dấu; tự chuyển sang tab có lỗi.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Lưu và gửi duyệt thành công.”', '- Thiếu / sai: ' + MISS, '- Dữ liệu kiểm kê đổi: ' + CHANGED,
         '- Đổi trạng thái: ' + CONFLICT]),
       ('Thông báo chuông cho người duyệt', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tiêu đề “[BBXLKKHH] Chờ duyệt: <số phiếu>”', '- Ghi chú: “Người lập: … Kỳ: … Kho: … Thừa: a, thiếu: b. Ghi chú: …”',
         '- Bấm → mở chi tiết biên bản']),
   ],
   ev=[
       ('Bấm Lưu và gửi duyệt', 'Click',
        'Before:\n– Màn Tạo: kiểm tra quyền Kế toán kho; không có → ' + NOPERM + ' và dừng xử lý. Màn Sửa: kiểm tra biên bản '
        'Đang tạo và người xem là người tạo; sai → ' + CONFLICT + '.\n– Khóa các nút lưu.\n' + SAVE_DURING + '\n'
        'After:\n– Lưu biên bản trạng thái Chờ duyệt (màn Tạo sinh số phiếu), ghi các dòng và tổng SL.\n'
        '– Ghi lịch sử “Tạo mới” (hoặc “Thay đổi thông tin” khi sửa) và “Thay đổi trạng thái” Đang tạo → Chờ duyệt.\n'
        '– Gửi thông báo “[BBXLKKHH] Chờ duyệt: <số phiếu>” cho người có quyền Duyệt cùng công ty người gửi.\n'
        '– Hiển thị “Lưu và gửi duyệt thành công.”, về màn danh sách.'),
       ('Lỗi chỉ nằm ở tab đang ẩn', 'System',
        'Before:\n– Có lỗi kiểm tra ở dòng của tab còn lại.\nAfter:\n– Tự chuyển sang tab có lỗi, cuộn tới ô lỗi đầu tiên.'),
       ('Sửa ô đang báo lỗi', 'Change',
        'Before:\n– Ô có viền đỏ + câu lỗi.\nAfter:\n– Xóa lỗi của ô ngay khi nhập / chọn lại; dấu lỗi trên tab mất khi hết lỗi.'),
       ('Bấm thông báo chờ duyệt', 'Click',
        'Before:\n– Người nhận có quyền Duyệt (thấy mọi biên bản Chờ duyệt).\nAfter:\n– Mở màn chi tiết biên bản với nút Duyệt '
        '(mục 2.10).'),
   ])

# ------------------------------------------------------------ 2.8 Sửa
fr(8, 'Chỉnh sửa biên bản', usecase=('FR-08', 'Chỉnh sửa biên bản', 'crud', A_KT),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Chỉnh sửa biên bản đang tạo',
       mota='Người tạo sửa biên bản còn Đang tạo: đổi khoảng ngày, kho, ghi chú, file đính kèm, Lấy dữ liệu lại, tích / bỏ tích phiếu '
            'kiểm kê, sửa Lý do, Giá xử lý, %, NV chịu từng dòng rồi Lưu (giữ Đang tạo) hoặc Lưu và gửi duyệt. Số phiếu, người tạo, '
            'ngày tạo không đổi.',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo biên bản.\n3. Biên bản đang ở trạng thái Đang tạo.',
       chinh='1. Người dùng bấm Sửa ở dòng biên bản (hoặc nút Sửa ở màn chi tiết).\n'
             '2. Hệ thống mở màn “Sửa biên bản xử lý hàng thừa, thiếu: <số phiếu>” điền sẵn Từ ngày, Đến ngày, Kho vật lý, Ghi chú, '
             'file đính kèm, phiếu kiểm kê (giữ tích như đã lưu) và các dòng với ô đã nhập.\n'
             '3. Người dùng sửa thông tin (quy tắc như mục 2.5, 2.6); đổi ngày / kho thì phải Lấy dữ liệu lại.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống kiểm lại biên bản còn Đang tạo và đúng người tạo, kiểm tra dữ liệu, lấy lại kết quả kiểm kê, ghi đè toàn bộ '
             'dòng, cập nhật tổng SL thừa / thiếu và người cập nhật.\n'
             '6. Hệ thống ghi nhận hành động “Thay đổi thông tin” trong lịch sử của biên bản (chỉ các trường đã đổi, cũ → mới).\n'
             '7. Hệ thống hiển thị “Lưu thành công.” và chuyển về màn danh sách.',
       phu='• Bấm Lưu và gửi duyệt → như mục 2.7.\n'
           '• Biên bản không còn Đang tạo / không phải người tạo khi mở màn Sửa → tự chuyển về màn chi tiết.\n'
           '• Biên bản đổi trạng thái ở tab khác trước khi lưu → ' + CONFLICT + ', không lưu.\n'
           '• Xóa file đã lưu (biểu tượng thùng rác ở khối File đính kèm) → file bị gỡ khỏi biên bản ngay, ghi lịch sử.\n'
           '• Không đổi gì mà bấm Lưu → lưu lại, không sinh dòng lịch sử “Thay đổi thông tin”.\n'
           '• Quay lại khi đã đổi → hộp “Thông tin chưa lưu” (Thoát / Ở lại).',
       dacbiet='Không có Lưu và tiếp tục ở màn Sửa. Biên bản không có trường duy nhất nên không kiểm trùng (kể cả với chính nó). Sửa '
               'không đổi Số phiếu, Người tạo, Ngày tạo, công ty / phòng ban của biên bản.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('12_edit'), shot_caption='Màn Sửa biên bản (biên bản Đang tạo)'),
   extra=[(shot('03_rowmenu'), 'Dòng Đang tạo của người tạo: nút Sửa, In và menu Hành động khác')],
   ui=FORM_UI[:2] + [
       ('Số phiếu', 'Label', 'Read-only', 'BBXLKKHH-NNNNN', '–', 'Theo dữ liệu',
        '- Chỉ hiện trên tiêu đề màn và tab trình duyệt; không có ô nhập Số phiếu (không sửa được).'),
   ] + FORM_UI[2:7] + [
       ('Biểu tượng xóa file đã lưu', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        '- Gỡ file khỏi biên bản ngay (chỉ khi còn Đang tạo); ghi lịch sử “Thay đổi thông tin”.'),
   ] + FORM_UI[7:16] + FORM_UI[17:],
   ev=[
       ('Bấm Sửa', 'Click',
        'Before:\n– Nút chỉ hiện với người tạo khi biên bản Đang tạo.\nDuring:\n– Nạp biên bản; ngoài phạm vi → trang “Không tìm '
        'thấy trang”; không còn sửa được → chuyển về màn chi tiết.\nAfter:\n– Hiển thị form điền sẵn; chưa tính là đã thay đổi.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Kiểm tra biên bản còn Đang tạo và người xem là người tạo; sai → ' + CONFLICT + ' / ' + NOPERM + '.\n'
        '– Khóa nút lưu.\n' + SAVE_DURING + '\n'
        'After:\n– Ghi đè thông tin chung và toàn bộ dòng, cập nhật tổng SL, người cập nhật, gắn file mới.\n'
        '– Ghi một dòng lịch sử “Thay đổi thông tin” (cũ → mới, chỉ trường đã đổi).\n– Hiển thị “Lưu thành công.”, về danh sách.'),
       ('Bấm Lưu và gửi duyệt', 'Click',
        'Before:\n– Như Lưu.\nDuring:\n– Kiểm tra như Lưu.\n' + ERR + '\n'
        'After:\n– Lưu như Lưu, đổi sang Chờ duyệt, ghi thêm “Thay đổi trạng thái”, gửi thông báo người duyệt (mục 2.7).'),
       ('Xóa file đã lưu', 'Click',
        'Before:\n– Biên bản còn Đang tạo, người xem là người tạo.\nDuring:\n– File không thuộc biên bản → “File không nằm trong '
        'biên bản này”.\nAfter:\n– Gỡ file, ghi lịch sử “Thay đổi thông tin”, thông báo “Xóa file thành công”.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu hiện tại với lúc mở màn.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu; Ở lại: giữ form.'),
   ])

# ------------------------------------------------------------ 2.9 Chi tiết
fr(9, 'Xem chi tiết biên bản',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết biên bản xử lý hàng thừa, thiếu',
       mota='Hiển thị toàn bộ thông tin một biên bản ở chế độ chỉ đọc: khoảng ngày, kho, ghi chú, file đính kèm, phiếu kiểm kê đã '
            'tích, 2 tab Hàng thừa / Hàng thiếu với cách xử lý từng dòng và chi phí đã lưu, khối Lịch sử, cùng các nút In, Xuất Excel, '
            'Sửa, Duyệt theo trạng thái và quyền.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Biên bản nằm trong phạm vi xem (Phần 2).',
       chinh='1. Người dùng bấm Số phiếu ở danh sách (hoặc nút Duyệt ở dòng, hoặc thông báo chờ duyệt).\n'
             '2. Hệ thống kiểm tra phạm vi xem và nạp biên bản.\n'
             '3. Hệ thống hiển thị màn “Chi tiết biên bản xử lý hàng thừa, thiếu: <số phiếu>”: các ô chỉ đọc, Kho vật lý dạng “Mã - '
             'Tên”, phiếu kiểm kê (ô tích khóa), 2 tab, khối Lịch sử.\n'
             '4. Hệ thống hiện nút ở chân màn: Duyệt (Chờ duyệt + quyền Duyệt), Sửa (người tạo + Đang tạo), In, Xuất Excel, Quay lại.\n'
             '5. Người dùng bấm Quay lại để về danh sách (giữ bộ lọc trong 10 phút).',
       phu='• Biên bản ngoài phạm vi / không tồn tại → chuyển sang trang “Không tìm thấy trang”.\n'
           '• Không có file đính kèm → khối File đính kèm ghi “Không có file đính kèm.”.\n'
           '• Biên bản chỉ có hàng thiếu → mở sẵn tab Hàng thiếu.\n'
           '• Người có quyền Duyệt xem biên bản Chờ duyệt → các ô Giá xử lý, %, NV chịu mở để sửa (mục 2.10); rời màn khi đã sửa → '
           'hộp “Thông tin chưa lưu”.',
       dacbiet='Màn chi tiết là trang riêng (không phải cửa sổ nổi). Dấu * vẫn hiện ở nhãn bắt buộc để đối chiếu với lúc tạo. Không '
               'có ô Số phiếu (số phiếu ở tiêu đề). Chi phí công ty hiển thị theo % trên màn; giá trị đã lưu in ra ở bản in / Excel.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'),
               shot_caption='Màn Chi tiết biên bản BBXLKKHH-00006 (Đã duyệt)'),
   extra=[(shot('17c_detail_history'), 'Màn chi tiết cuộn xuống: bảng chi tiết và khối Lịch sử')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        '- “Chi tiết biên bản xử lý hàng thừa, thiếu: <số phiếu>” (không gắn nhãn trạng thái).'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Ô Từ ngày, Đến ngày', 'Datepicker', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '- Khóa, có dấu *.'),
       ('Ô Kho vật lý', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', '- “Mã - Tên” kho, khóa.'),
       ('Ô Ghi chú', 'Textarea', 'Read-only', '0–255 ký tự', 'Theo dữ liệu', '- Khóa; trống thì để trắng.'),
       ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Danh sách file, bấm xem / tải', '- Không có file: “Không có file đính kèm.”']),
       ('Khối Phiếu kiểm kê', 'Checkbox', 'Read-only', '–', 'Theo dữ liệu',
        ['- Ô tích khóa, giữ đúng tích lúc lưu', '- Số phiếu là liên kết mở phiếu kiểm kê ở tab mới',
         '- Không có: “Không có phiếu kiểm kê.”']),
       ('Thanh tab Hàng thừa (n), Hàng thiếu (n)', 'Button', 'Enable', '–', 'Hàng thừa', '- Bấm để đổi tab.'),
       ('Bảng chi tiết 18 cột', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột như mục 2.5; Lý do, Giá xử lý, %, NV chịu hiện chữ (trừ người duyệt ở biên bản Chờ duyệt)',
         '- % hiện “40 %”; NV chịu “Mã NV-Họ tên”']),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút Xem lịch sử mở danh sách mốc (mục 2.13).'),
       ('Nút Duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi thiếu quyền', '- Biên bản Chờ duyệt + quyền Duyệt (mục 2.10).'),
       ('Nút Sửa', 'Button', 'Enable / Ẩn', '–', 'Ẩn', '- Người tạo + Đang tạo → mở màn Sửa (mục 2.8).'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Mở cửa sổ xem trước bản in (mục 2.11).'),
       ('Nút Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', '- Tải file Excel của biên bản (mục 2.12).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn danh sách.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem (Phần 2).\nDuring:\n– Ngoài phạm vi / không tồn tại → trang “Không tìm thấy trang”.\n'
        'After:\n– Hiển thị dữ liệu chỉ đọc, nút theo trạng thái và quyền; người duyệt được mở ô xử lý.'),
       ('Bấm tab Hàng thừa / Hàng thiếu', 'Click', 'Before:\n– Tab có dữ liệu hoặc rỗng.\nAfter:\n– Hiện dòng của tab; rỗng: “Không có dữ liệu”.'),
       ('Bấm Xem lịch sử', 'Click', 'Before:\n– Biên bản trong phạm vi.\nAfter:\n– Mở danh sách mốc lịch sử ngay trên màn (mục 2.13).'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Người duyệt đã sửa ô → hỏi “Thông tin chưa lưu”.\nAfter:\n– Về danh sách, giữ bộ lọc / trang nếu trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.10 Duyệt
fr(10, 'Duyệt biên bản', usecase=('FR-10', 'Duyệt biên bản', 'action', A_DUYET),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Duyệt biên bản xử lý hàng thừa, thiếu (ghi bút toán)',
       mota='Người có quyền Duyệt mở biên bản Chờ duyệt, được sửa Giá xử lý, % chi phí, NV chịu từng dòng (Lý do giữ nguyên) rồi bấm '
            'Duyệt: hệ thống lưu lại các ô, tính lại chi phí, chuyển Đã duyệt, ghi người / ngày duyệt và bút toán sổ cái theo từng '
            'nhân viên chịu. Không có hộp xác nhận và không có Không duyệt (như hệ thống cũ).',
       tacnhan=TN_DUYET,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có quyền “%s” (hoặc Super admin).\n3. Biên bản đang ở trạng thái Chờ duyệt.' % Q2,
       chinh='1. Người dùng bấm Duyệt ở dòng biên bản (mở màn chi tiết) hoặc mở chi tiết từ thông báo.\n'
             '2. Hệ thống hiện các ô Giá xử lý, % Chi phí nhân viên, % Chi phí công ty, NV chịu của từng dòng ở chế độ sửa.\n'
             '3. Người dùng kiểm tra, sửa nếu cần và bấm Duyệt.\n'
             '4. Hệ thống kiểm tra mọi dòng đủ Giá xử lý, % (0 – 100), NV chịu.\n'
             '5. Hệ thống khóa biên bản, kiểm lại còn Chờ duyệt và quyền Duyệt; lưu lại các ô, tính lại chi phí (chi phí công ty = '
             'chi phí nhân viên), chuyển Đã duyệt, ghi người duyệt, ngày duyệt.\n'
             '6. Hệ thống ghi bút toán theo từng NV chịu: hàng thừa Nợ 3381 / Có 3341 (chi phí nhân viên), Nợ 3381 / Có 711 (chi phí '
             'công ty); hàng thiếu Nợ 3341 / Có 1381 (chi phí nhân viên), Nợ 811 / Có 1381 (chi phí công ty); ngày hạch toán = ngày '
             'duyệt.\n'
             '7. Hệ thống ghi nhận “Thay đổi thông tin” (nếu sửa ô) và “Duyệt” (Chờ duyệt → Đã duyệt) trong lịch sử của biên bản.\n'
             '8. Hệ thống hiển thị “Duyệt thành công.” và chuyển về màn danh sách.',
       phu='• Thiếu Giá xử lý / % / NV chịu ở dòng nào → lỗi tại ô, chuyển sang tab có lỗi, thông báo ' + MISS + ', không duyệt.\n'
           '• Biên bản đã được duyệt ở tab khác / số dòng đổi → ' + CONFLICT + '.\n'
           '• Không có quyền Duyệt (gửi thẳng) → ' + NOPERM + '.\n'
           '• Ghi bút toán lỗi (vd thiếu tài khoản) → hủy toàn bộ lần duyệt, biên bản vẫn Chờ duyệt, báo câu lỗi của hệ thống.\n'
           '• Rời màn khi đã sửa ô mà chưa Duyệt → hộp “Thông tin chưa lưu”.',
       dacbiet='Không có hộp xác nhận (như hệ thống cũ). Vế bút toán bằng 0 bị bỏ. Duyệt không gửi thông báo. Biên bản Đã duyệt không '
               'sửa / duyệt lại được; không có luồng hủy duyệt.'),
   layout=dict(entries=[
       (MENU + ' => Duyệt', 'Nút Duyệt ở dòng biên bản Chờ duyệt mở màn chi tiết có nút Duyệt ở chân màn.'),
       (MENU + ' => Xem chi tiết => Duyệt', 'Mở chi tiết từ Số phiếu hoặc từ thông báo “[BBXLKKHH] Chờ duyệt”.')],
       shot=shot('14_approve'), shot_caption='Màn chi tiết biên bản Chờ duyệt BBXLKKHH-00004 với người có quyền Duyệt'),
   extra=[(shot('14b_approve_validate'), 'Duyệt khi dòng còn trống Giá xử lý, NV chịu: lỗi hiện tại ô')],
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chi tiết biên bản xử lý hàng thừa, thiếu: <số phiếu>”.'),
       ('Thông tin chung, phiếu kiểm kê', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '- Chỉ đọc như mục 2.9.'),
       ('Cột Lý do', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Người duyệt KHÔNG sửa được Lý do.'),
       ('Ô Giá xử lý (từng dòng)', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Có', 'Theo dữ liệu',
        ['- Giá vốn / Giá bán', '- Lỗi: “Giá xử lý – Vui lòng chọn giá xử lý.”']),
       ('Ô % Chi phí nhân viên (từng dòng)', 'Textbox', 'Enable', '0 – 100', 'Có', 'Theo dữ liệu',
        ['- Ô kia tự = 100 − %', '- Lỗi: “% Chi phí nhân viên – Vui lòng nhập.” / “… – Từ 0 đến 100.”']),
       ('Ô % Chi phí công ty (từng dòng)', 'Textbox', 'Enable', '0 – 100', 'Có', 'Theo dữ liệu',
        ['- Ô kia tự = 100 − %', '- Lỗi: “% Chi phí công ty – Vui lòng nhập.”']),
       ('Ô NV chịu (từng dòng)', 'Dropdown', 'Enable', 'Nhân viên đang làm việc', 'Có', 'Theo dữ liệu',
        ['- Người đang gắn ở dòng luôn có trong danh sách (kể cả đã nghỉ)', '- Lỗi: “NV chịu – Vui lòng chọn nhân viên chịu.”']),
       ('Cột Chi phí nhân viên, Chi phí công ty', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', '- Tự tính lại khi sửa ô.'),
       ('Nút Duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Màu chính, đứng đầu chân màn', '- Chỉ hiện với biên bản Chờ duyệt + quyền Duyệt', '- Khóa trong lúc xử lý']),
       ('Nút In, Xuất Excel, Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Như mục 2.9.'),
       ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', '- Rời màn khi đã sửa ô mà chưa Duyệt.'),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Duyệt thành công.”', '- Thiếu: ' + MISS, '- Đổi trạng thái: ' + CONFLICT,
         '- Lỗi bút toán / khác: câu lỗi máy chủ hoặc “Duyệt thất bại.”']),
   ],
   ev=[
       ('Bấm Duyệt ở dòng danh sách', 'Click',
        'Before:\n– Nút chỉ hiện ở biên bản Chờ duyệt với người có quyền Duyệt.\nAfter:\n– Mở màn chi tiết biên bản (không duyệt ngay).'),
       ('Sửa Giá xử lý / % / NV chịu', 'Change',
        'Before:\n– Chỉ người có quyền Duyệt ở biên bản Chờ duyệt.\nAfter:\n– Tính lại chi phí của dòng; ô % kia tự = 100 − %.'),
       ('Bấm Duyệt', 'Click',
        'Before:\n– Kiểm tra quyền “' + Q2 + '”; không có → ' + NOPERM + ' và dừng xử lý.\n'
        '– Kiểm tra biên bản đang Chờ duyệt và đủ mọi dòng; sai → ' + CONFLICT + '.\n'
        'During:\n– Dòng thiếu Giá xử lý / % / NV chịu, % ngoài 0 – 100 → lỗi tại ô, thông báo ' + MISS + ', chuyển tab có lỗi.\n'
        '– Ghi bút toán lỗi → hủy toàn bộ, báo câu lỗi.\n' + ERR + '\n'
        'After:\n– Lưu các ô, tính lại chi phí, trạng thái Đã duyệt, người / ngày duyệt.\n'
        '– Ghi bút toán 3381 / 3341 / 711 (thừa) và 3341 / 1381 / 811 (thiếu) theo từng NV chịu.\n'
        '– Ghi lịch sử “Thay đổi thông tin” (nếu có) và “Duyệt”.\n– Hiển thị “Duyệt thành công.”, về danh sách.'),
       ('Rời màn khi đã sửa ô', 'Click',
        'Before:\n– So các ô với lúc mở màn.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát: không lưu; '
        'Ở lại: giữ màn.'),
   ])

# ------------------------------------------------------------ 2.11 In
fr(11, 'In biên bản và in danh sách', usecase=('FR-11', 'In biên bản / In danh sách', 'io', A_KT),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='In biên bản và in danh sách biên bản',
       mota='In 1 biên bản (khổ ngang) theo mẫu in của hệ thống: letterhead công ty ghi trên biên bản, Số phiếu, Ngày lập, Từ ngày, '
            'Đến ngày, Phiếu kiểm kê (chỉ phiếu được tích), Kho, Ghi chú và 2 bảng Hàng thừa / Hàng thiếu 14 cột. In danh sách in '
            'các biên bản theo bộ lọc đang áp (tối đa 2.000 dòng). Cả hai mở cửa sổ xem trước rồi mới in.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Biên bản / danh sách nằm trong phạm vi xem.',
       chinh='1. Người dùng bấm In ở dòng biên bản (hoặc nút In ở màn chi tiết).\n'
             '2. Hệ thống dựng bản in khổ ngang: letterhead theo công ty của biên bản, tiêu đề “BIÊN BẢN XỬ LÝ HÀNG THỪA THIẾU SAU KIỂM KÊ”, '
             'thông tin chung, bảng “Tab1 - Hàng Thừa” và “Tab2 - Hàng Thiếu” (STT, Tên hàng, Mã hàng, Mã kho, SL, Thành tiền bán, '
             'Thành tiền vốn, Lý do và nhóm Chi tiết: Giá xử lý, Chi phí nhân viên (%), Chi phí công ty (%), NV chịu, Chi phí nhân '
             'viên, Chi phí công ty), ngày tháng năm in.\n'
             '3. Hệ thống mở cửa sổ “Xem trước biên bản xử lý hàng thừa, thiếu <số phiếu>”.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.\n'
             '5. In danh sách: bấm In danh sách → cửa sổ “Xem trước danh sách biên bản xử lý hàng thừa, thiếu sau kiểm kê” (10 cột: '
             'STT, Số phiếu, Ngày tạo, Kho vật lý, SL hàng thừa, SL hàng thiếu, Người tạo, Người duyệt, Ngày duyệt, Trạng thái).',
       phu='• Danh sách quá 2.000 dòng → không in, hiện “Danh sách có N dòng, vượt mức in tối đa 2.000 dòng nên chưa in được. Vui '
           'lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.”.\n'
           '• Danh sách rỗng → “Không có dữ liệu để in”.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in biên bản xử lý hàng thừa, thiếu sau kiểm kê.”; lỗi khác → “Không tải được dữ liệu in”.\n'
           '• Biên bản ngoài phạm vi → ' + NOTFOUND + '.\n'
           '• Bấm Đóng, (x) hoặc Esc → đóng cửa sổ, không in.',
       dacbiet='Letterhead bản in biên bản lấy theo công ty GHI TRÊN BIÊN BẢN (không theo người in); bản in danh sách lấy theo công ty '
               'người in. Chi phí công ty in giá trị đã lưu (= chi phí nhân viên). Mã hàng dài tự xuống dòng không đè cột bên cạnh. '
               'In không ghi lịch sử.'),
   layout=dict(entries=[
       (MENU + ' => In', 'In 1 biên bản từ cột Hành động hoặc màn chi tiết.'),
       (MENU + ' => In danh sách', 'In danh sách theo bộ lọc đang áp.')],
       shot=shot('18_print'), shot_caption='Cửa sổ Xem trước biên bản BBXLKKHH-00006 (khổ ngang)'),
   extra=[(shot('19_printlist'), 'Cửa sổ Xem trước danh sách biên bản')],
   ui=[
       ('Nút In (dòng)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Biểu tượng máy in ở cột Hành động.'),
       ('Nút In (màn chi tiết)', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Ở chân màn chi tiết.'),
       ('Nút In danh sách', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Thanh công cụ danh sách; in theo bộ lọc đang áp.'),
       ('Tiêu đề cửa sổ xem trước', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        ['- 1 biên bản: “Xem trước biên bản xử lý hàng thừa, thiếu <số phiếu>”',
         '- Danh sách: “Xem trước danh sách biên bản xử lý hàng thừa, thiếu sau kiểm kê”']),
       ('Nội dung bản in biên bản', 'Table/Grid', 'Read-only', 'Khổ ngang', '–', 'Theo dữ liệu',
        ['- Letterhead công ty của biên bản, tiêu đề, Số phiếu, Ngày lập, Từ ngày, Đến ngày, Phiếu kiểm kê, Kho, Ghi chú',
         '- 2 bảng “Tab1 - Hàng Thừa”, “Tab2 - Hàng Thiếu” 14 cột, tiêu đề 2 tầng nhóm “Chi tiết”', '- Ngày … tháng … năm …']),
       ('Nội dung bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', '–', 'Theo bộ lọc',
        ['- Letterhead công ty người in', '- 10 cột, cột ngày kèm giờ, số lượng căn phải']),
       ('Dòng nhắc vượt trần', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Hiện khi danh sách > 2.000 dòng; ẩn nút In.'),
       ('Nút In (trong cửa sổ)', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Mở hộp thoại in của trình duyệt.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, không in.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Không có dữ liệu để in”', '- “Không tải được dữ liệu in”', '- ' + NOTFOUND]),
   ],
   ev=[
       ('Bấm In (1 biên bản)', 'Click',
        'Before:\n– Kiểm tra biên bản trong phạm vi xem; ngoài phạm vi → ' + NOTFOUND + '.\n'
        'During:\n– Lấy mẫu in biên bản; thiếu mẫu → “Thiếu mẫu in biên bản xử lý hàng thừa, thiếu sau kiểm kê.”\n'
        'After:\n– Mở cửa sổ xem trước khổ ngang với letterhead theo công ty của biên bản.'),
       ('Bấm In danh sách', 'Click',
        'Before:\n– Lấy bộ lọc + sắp xếp đang áp.\nDuring:\n– Quá 2.000 dòng → dòng nhắc thu hẹp bộ lọc, không in; rỗng → “Không có '
        'dữ liệu để in”.\nAfter:\n– Mở cửa sổ xem trước danh sách.'),
       ('Bấm In trong cửa sổ', 'Click', 'Before:\n– Nội dung đã tải xong.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm Đóng, (x) hoặc Esc', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; màn đang xem giữ nguyên.'),
   ])

# ------------------------------------------------------------ 2.12 Xuất Excel
fr(12, 'Xuất Excel danh sách và 1 biên bản', usecase=('FR-12', 'Xuất Excel', 'io', A_KT),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất Excel danh sách biên bản và xuất Excel 1 biên bản',
       mota='Xuất danh sách biên bản theo bộ lọc + phạm vi đang xem ra file Excel, người dùng chọn trường và thứ tự cột. Ngoài ra mỗi '
            'biên bản xuất được 1 file Excel riêng (thông tin chung + 2 bảng Hàng thừa / Hàng thiếu như bản in) từ cột Hành động '
            'hoặc màn chi tiết.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn danh sách (xuất danh sách) hoặc có biên bản trong phạm vi xem.',
       chinh='1. Người dùng lọc danh sách theo nhu cầu rồi bấm Xuất Excel trên thanh công cụ.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” liệt kê 9 trường, tích sẵn 5 trường: Số phiếu, Hàng thừa, Hàng thiếu, '
             'Người tạo, Trạng thái (Ngày tạo, Kho, Người duyệt, Ngày duyệt chưa tích sẵn dù đang hiện trên bảng).\n'
             '3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy MỌI biên bản khớp bộ lọc (không phân trang) và tạo file danh_sach_bien_ban_xu_ly_hang_thua_thieu_sau_'
             'kiem_ke.xlsx: letterhead công ty người xuất, tiêu đề “DANH SÁCH BIÊN BẢN XỬ LÝ HÀNG THỪA THIẾU SAU KIỂM KÊ”, dòng khoảng '
             'Ngày tạo (nếu lọc), cột STT + các trường đã chọn, khối ký.\n'
             '5. Hệ thống tải file về và hiển thị “Xuất Excel thành công.”.\n'
             '6. Xuất 1 biên bản: bấm Xuất Excel ở dòng (hoặc màn chi tiết) → tải file bien_ban_xu_ly_hang_thua_thieu<số phiếu>.xlsx.',
       phu='• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Danh sách rỗng → vẫn tạo file có tiêu đề, tên cột, khối ký, không có dòng dữ liệu.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài cửa sổ chọn trường → không xuất.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel.”; biên bản ngoài phạm vi (xuất 1 biên bản) → không tải được, báo lỗi.',
       dacbiet='Hàng thừa / Hàng thiếu là ô SỐ (có dấu ngăn nghìn theo máy, số 0 ghi 0); ngày dạng dd/mm/yyyy hh:mm. Xuất không giới '
               'hạn số dòng, không ghi lịch sử. File 1 biên bản in chi phí công ty theo giá trị đã lưu.'),
   layout=dict(entries=[
       (MENU + ' => Xuất Excel', 'Xuất danh sách theo bộ lọc đang áp.'),
       (MENU + ' => Xem chi tiết => Xuất Excel', 'Xuất 1 biên bản (hoặc nút Xuất Excel ở cột Hành động).')],
       shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 9 trường', '–', '5/9 trường được tích',
        ['- Số phiếu, Ngày tạo, Kho, Hàng thừa, Hàng thiếu', '- Người tạo, Người duyệt, Ngày duyệt, Trạng thái',
         '- Cột STT luôn có trong file (không nằm trong danh sách)']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích 5 trường',
        ['- Mặc định tích: Số phiếu, Hàng thừa, Hàng thiếu, Người tạo, Trạng thái', '- Bỏ tích → trường không có trong file']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích cả 9 trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/9 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Khóa khi chưa tích trường nào hoặc đang xuất', '- Bấm → tải file danh sách']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng cửa sổ, không xuất.'),
       ('Nút Xuất Excel (dòng, màn chi tiết)', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tải file 1 biên bản.'),
       ('File danh sách', 'Table/Grid', 'Read-only', '.xlsx', '–', '–',
        ['- Tên danh_sach_bien_ban_xu_ly_hang_thua_thieu_sau_kiem_ke.xlsx, trang “Biên bản xử lý thừa thiếu”',
         '- Letterhead, tiêu đề, dòng khoảng Ngày tạo, STT + trường đã chọn đúng thứ tự, khối ký']),
       ('File 1 biên bản', 'Table/Grid', 'Read-only', '.xlsx', '–', '–',
        ['- Tên bien_ban_xu_ly_hang_thua_thieu<số phiếu>.xlsx', '- Thông tin chung + bảng Tab1 - Hàng Thừa, Tab2 - Hàng Thiếu']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- “Xuất Excel thành công.”', '- “Lỗi khi xuất Excel.”']),
   ],
   ev=[
       ('Bấm Xuất Excel (thanh công cụ)', 'Click',
        'Before:\n– Không cần quyền riêng; lấy bộ lọc đang áp.\nAfter:\n– Mở cửa sổ chọn trường, tích sẵn 5 trường (Số phiếu, Hàng thừa, Hàng thiếu, Người tạo, Trạng thái).'),
       ('Tích / bỏ tích, kéo thả trường', 'Change',
        'Before:\n– Trong cửa sổ chọn trường.\nAfter:\n– Cập nhật “Đang chọn n/9 trường”; 0 trường → khóa Xuất file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Ít nhất 1 trường được tích; khóa nút trong lúc xuất.\n'
        'During:\n– Lấy mọi biên bản khớp bộ lọc trong phạm vi; lỗi → “Lỗi khi xuất Excel.”\n'
        'After:\n– Tải file danh sách, hiển thị “Xuất Excel thành công.”; không ghi lịch sử.'),
       ('Bấm Xuất Excel 1 biên bản', 'Click',
        'Before:\n– Biên bản trong phạm vi xem.\nDuring:\n– Ngoài phạm vi / lỗi → “Lỗi khi xuất Excel.”\n'
        'After:\n– Tải file bien_ban_xu_ly_hang_thua_thieu<số phiếu>.xlsx, hiển thị “Xuất Excel thành công.”.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.13 Lịch sử
fr(13, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của biên bản',
       mota='Hiển thị các mốc thao tác trên một biên bản: Tạo mới, Thay đổi thông tin (từng trường cũ → mới, kể cả từng dòng chi tiết '
            'và file đính kèm), Thay đổi trạng thái (Đang tạo → Chờ duyệt), Duyệt (Chờ duyệt → Đã duyệt), kèm người thực hiện, phòng '
            'ban, thời điểm; lọc được theo loại hành động, người thực hiện, khoảng ngày.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Biên bản nằm trong phạm vi xem.',
       chinh='1. Người dùng bấm Lịch sử ở dòng (hoặc trong menu Hành động khác) hoặc bấm Xem lịch sử ở màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem và nạp các mốc lịch sử của biên bản.\n'
             '3. Hệ thống hiển thị cửa sổ “Lịch sử thay đổi: <số phiếu>” (ở màn chi tiết: khối Lịch sử), mốc mới nhất ở trên.\n'
             '4. Người dùng bấm Bộ lọc để lọc theo Loại hành động, Người thực hiện, Từ ngày, Đến ngày.\n'
             '5. Người dùng bấm Đóng để về danh sách.',
       phu='• Chưa có mốc nào → “Chưa có lịch sử thao tác nào.”.\n'
           '• Lọc không ra mốc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Biên bản ngoài phạm vi → ' + NOTFOUND + '.\n'
           '• Bấm Đóng, (x) hoặc click ra ngoài → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Lịch sử được chặn theo phạm vi xem của biên bản. Xem / In / Xuất / Lấy dữ liệu không ghi lịch sử; Lưu không đổi gì '
               'không ghi “Thay đổi thông tin”.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi biên bản BBXLKKHH-00006',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Lịch sử thay đổi: <số phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm, hành động (Tạo mới / Thay đổi thông tin / Thay đổi trạng thái / Duyệt)',
           '- “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái / Duyệt: “Trạng thái: Chờ duyệt → Đã duyệt”',
           '- Thay đổi thông tin: Từ ngày, Đến ngày, Kho vật lý, Phiếu kiểm kê, Ghi chú, từng dòng chi tiết, file — cũ → mới',
           '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách hành động', 'Trống', ['- Mặc định: trống', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Người đã thao tác', 'Trống', '- Chọn là lọc ngay.'),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc từ ngày này.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc đến hết ngày này.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- “Chưa có lịch sử thao tác nào.”', '- “Không có lịch sử phù hợp bộ lọc.”']),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('Khối Lịch sử ở màn chi tiết', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Cùng nội dung; nút Xem lịch sử mở danh sách mốc.'),
   ],
   ev=[
       ('Mở lịch sử', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → ' + NOTFOUND + '.\n'
        'During:\n– Nạp các mốc; chưa có → “Chưa có lịch sử thao tác nào.”.\nAfter:\n– Hiển thị, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change', 'Before:\n– Không có nút Tìm kiếm.\nAfter:\n– Lọc lại danh sách mốc.'),
       ('Bấm Xem lịch sử ở màn chi tiết', 'Click', 'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở danh sách mốc ngay trên màn.'),
       ('Bấm Đóng, (x) hoặc click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng; danh sách giữ nguyên trang, bộ lọc.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Biên bản xử lý hàng thừa, thiếu sau kiểm kê; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Biên bản không ghi tồn', [
        '– Lưu / gửi duyệt / sửa / duyệt biên bản không đổi tồn kho, không sinh phiếu nhập / xuất.',
        '– Tồn đã được điều chỉnh trước đó bằng phiếu nhập / xuất kho điều chỉnh kiểm kê; biên bản chỉ đọc giá vốn từ các phiếu đó.'],
     ['Tạo', 'Chỉnh sửa', 'Duyệt']),
    ('BR-02', 'Phạm vi xem', [
        '– V1 (hoặc Super admin): mọi biên bản; V2: công ty mình + của mình (công ty trống → chỉ của mình); không quyền: của mình.',
        '– Người có quyền Duyệt thấy thêm mọi biên bản Chờ duyệt.', '– Biên bản Đang tạo chỉ người tạo thấy.',
        '– Ngoài phạm vi: chi tiết / sửa / in / xuất / lịch sử đều bị từ chối.'],
     ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất', 'Lịch sử']),
    ('BR-03', 'Quyền tạo và lấy dữ liệu', [
        '– Tạo mới và Lấy dữ liệu cần quyền Kế toán kho (hoặc Super admin).',
        '– Sửa chỉ cần là người tạo khi Đang tạo.'], ['Tạo', 'Lấy dữ liệu']),
    ('BR-04', 'Nguồn dữ liệu kiểm kê', [
        '– Phiếu kiểm kê theo hàng hóa Hoàn thành, có kho đã chọn, ngày kiểm kê trong Từ ngày – Đến ngày.',
        '– Mỗi hàng của mỗi phiếu = 1 dòng; chênh lệch cộng dồn, làm tròn 2 số lẻ; chênh 0 bị bỏ; > 0 thừa, < 0 thiếu; SL = trị tuyệt đối.',
        '– Giá vốn, phiếu xử lý, mã kho: phiếu nhập kho điều chỉnh kiểm kê Hoàn thành (ưu tiên), không có thì phiếu xuất kho điều '
        'chỉnh kiểm kê Hoàn thành, cùng phiếu kiểm kê + cùng hàng; không có → giá vốn 0.'],
     ['Lấy dữ liệu', 'Tạo', 'Chỉnh sửa']),
    ('BR-05', 'Máy chủ lấy lại dữ liệu khi lưu', [
        '– SL, giá, phiếu xử lý, mã kho không nhận từ màn hình; máy chủ chạy lại nguồn kiểm kê với ngày / kho đã chọn.',
        '– Bộ hàng của các phiếu được tích phải trùng khít bộ hàng gửi lên; khác → “Dữ liệu kiểm kê đã thay đổi. Vui lòng bấm "Lấy '
        'dữ liệu" lại.”',
        '– Đổi ngày / kho mà chưa Lấy dữ liệu lại → màn chặn trước khi gửi.'], ['Tạo', 'Chỉnh sửa', 'Lưu và gửi duyệt']),
    ('BR-06', 'Dữ liệu bắt buộc', [
        '– Lưu và Lưu và gửi duyệt cùng một bộ: Từ ngày, Đến ngày (≥ Từ ngày), Kho vật lý, ít nhất 1 dòng.',
        '– Mỗi dòng: Lý do (≤ 255 ký tự), Giá xử lý, % Chi phí nhân viên (0 – 100), % Chi phí công ty, NV chịu (nhân viên tồn tại).',
        '– Ghi chú ≤ 255 ký tự; file pdf / png / jpg / jpeg, ≤ 20MB, ≤ 20 file.'], ['Tạo', 'Chỉnh sửa', 'Lưu và gửi duyệt', 'Duyệt']),
    ('BR-07', 'Điều kiện sửa', [
        '– Chỉ người tạo, chỉ khi Đang tạo; máy chủ kiểm lại lúc lưu, sai → báo trạng thái đã thay đổi.',
        '– Không có Xóa biên bản (hệ thống cũ đã tắt); không có Khóa.'], ['Chỉnh sửa']),
    ('BR-08', 'Vòng đời và duyệt', [
        '– Lưu / Lưu và tiếp tục → Đang tạo; Lưu và gửi duyệt → Chờ duyệt; Duyệt → Đã duyệt.',
        '– Chỉ người có quyền Duyệt duyệt biên bản Chờ duyệt; được sửa Giá xử lý, %, NV chịu (không sửa Lý do).',
        '– Không có Không duyệt / Từ chối / Hủy; không hỏi xác nhận khi gửi duyệt / duyệt; Đã duyệt không đổi được nữa.'],
     ['Lưu và gửi duyệt', 'Duyệt']),
    ('BR-09', 'Tính chi phí và bút toán', [
        '– % Chi phí công ty = 100 − % Chi phí nhân viên; mặc định 100 / 0; Giá xử lý mặc định Giá vốn.',
        '– Chi phí nhân viên = thành tiền (vốn hoặc bán theo Giá xử lý) × % nhân viên, làm tròn 2 số lẻ khi lưu.',
        '– Chi phí công ty LƯU bằng chi phí nhân viên (giữ như hệ thống cũ — user chốt 21/10/2026); màn hiển thị theo %, bản in / '
        'Excel in giá trị đã lưu.',
        '– Duyệt ghi bút toán theo NV chịu: thừa Nợ 3381 / Có 3341, Nợ 3381 / Có 711; thiếu Nợ 3341 / Có 1381, Nợ 811 / Có 1381; '
        'vế 0 bị bỏ; lỗi → hủy cả lần duyệt.'], ['Lấy dữ liệu', 'Duyệt', 'In', 'Xuất']),
    ('BR-10', 'Tính duy nhất', [
        '– Không có trường nhập duy nhất; mã BBXLKKHH-NNNNN tự sinh theo số thứ tự, không đổi khi sửa.',
        '– Không chặn một phiếu kiểm kê được lập nhiều biên bản (như hệ thống cũ) — người lập tự kiểm tra để tránh hạch toán trùng.',
        '– Nút lưu khóa trong lúc lưu chống tạo trùng do bấm liên tục.'], ['Tạo']),
    ('BR-11', 'Chuẩn hóa dữ liệu nhập', [
        '– Công ty / phòng ban của biên bản = của người tạo (thiếu thì ghi 0).',
        '– Lý do bỏ khoảng trắng đầu / cuối khi lưu; % giới hạn 0 – 100.',
        '– NV chịu lưu kèm “Mã NV-Họ tên”; danh sách chọn chỉ nhân viên đang làm việc.'], ['Tạo', 'Chỉnh sửa', 'Duyệt']),
    ('BR-12', 'Liên kết cấp cha – con', [
        '– Biên bản > phiếu kiểm kê (ô tích) > dòng hàng thừa / thiếu > phiếu xử lý.',
        '– Bỏ tích phiếu kiểm kê → dòng của phiếu không được lưu; lưu ghi đè toàn bộ dòng.'], ['Tạo', 'Chỉnh sửa']),
    ('BR-13', 'Thông báo', [
        '– Lưu với trạng thái Chờ duyệt (tạo hoặc sửa) → “[BBXLKKHH] Chờ duyệt: <số phiếu>” cho nhân viên có quyền Duyệt cùng công '
        'ty người gửi; người gửi không có công ty → không gửi; lỗi gửi không làm hỏng việc lưu.',
        '– Duyệt không gửi thông báo.'], ['Lưu và gửi duyệt']),
    ('BR-14', 'In và xuất', [
        '– Letterhead bản in / file 1 biên bản theo công ty ghi trên biên bản; bản in / file danh sách theo công ty người in / xuất.',
        '– In danh sách tối đa 2.000 dòng; Xuất Excel danh sách không giới hạn, rỗng vẫn ra file.'], ['In', 'Xuất Excel']),
    ('BR-15', 'Sử dụng ở màn khác', [
        '– Kho vật lý đã có trong biên bản không xóa được ở danh mục Kho vật lý.',
        '– Bút toán do Duyệt ghi hiện ở Sổ chi tiết / Bảng cân đối phát sinh công nợ nhân viên.'], ['Duyệt', 'Tạo']),
    ('BR-16', 'Quy tắc ghi lịch sử', [
        '– Ghi: Tạo mới; Thay đổi thông tin (Từ ngày, Đến ngày, Kho vật lý, Phiếu kiểm kê, Ghi chú, từng dòng chi tiết, file — cũ → '
        'mới, không đổi thì không ghi); Thay đổi trạng thái (Đang tạo → Chờ duyệt); Duyệt (Chờ duyệt → Đã duyệt).',
        '– Xem / in / xuất / lấy dữ liệu không ghi; hiển thị mới nhất ở trên.'], ['Tạo', 'Chỉnh sửa', 'Duyệt', 'Lịch sử']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Biên bản xử lý hàng thừa, thiếu sau kiểm kê (biên bản, kho vật lý, bút '
    'toán sổ cái ghi khi Duyệt).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Kho vật lý (không xóa được kho đã có trong biên bản)', 'Kho -> Danh mục'),
    ('2', 'Tài chính', 'Sổ chi tiết công nợ nhân viên (đọc bút toán 3341 / 1381 / 3381 theo NV chịu do Duyệt biên bản ghi; số chứng '
                       'từ BBXLKKHH-NNNNN)', 'Tài chính -> Kế toán công nợ -> Nhân viên'),
    ('3', 'Tài chính', 'Bảng cân đối phát sinh công nợ nhân viên (cộng phát sinh Nợ / Có của các bút toán trên theo nhân viên)',
     'Tài chính -> Kế toán công nợ -> Nhân viên'),
    ('4', 'Hệ thống ERP', 'Biên bản xử lý hàng thừa, thiếu và sổ sách kế toán trên hệ thống cũ (dùng chung dữ liệu biên bản, cùng dãy '
                          'mã; đọc lại bút toán 711 / 811 / 3381 / 3341 / 1381)', 'Hệ thống ERP (chưa chuyển sang HRM)'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
print('Đã ghi', OUT)
