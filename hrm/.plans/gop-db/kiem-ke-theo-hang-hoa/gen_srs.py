# -*- coding: utf-8 -*-
"""SRS màn "Kiểm kê theo hàng hóa" (phiếu kiểm kê theo hàng hóa, mã <mã công ty>.KKK-NNNNN) — form chuẩn, chuẩn 04/11/2026.

Chạy: python gen_srs.py  → SRS - Kiểm kê theo hàng hóa.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc màn anh em
  ../kiem-ke-theo-vi-tri/gen_srs.py (06/11, Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn).
Nguồn đọc 06/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Entities/SelfInventory/SelfInventory.php, Services/SelfInventory{,Write,Print,Attachment}Service.php,
      Services/PhysicalStockReader.php, Http/Controllers/V1/SelfInventoryController.php, Http/Requests/SelfInventory/
      {SelfInventoryStoreRequest,SelfInventorySaveResultRequest}.php, Exports/SelfInventoryExport.php}, các màn đọc / ghi ngược
      (PositionTransferWriteService, WarehouseInventory{Import,Export}WriteService, Inventory{Import,Export}WriteService,
      WarehouseImportWriteService, ProductTransferWriteService, WarehouseInventoryLockService, SelfInventoryReportService,
      InventoryAuditReportService, MasterData PhysicalWarehouse / Position), PermissionsTableSeeder (nhóm "Kiểm kê theo hàng hóa").
  FE  pages/warehouse/self-inventories/** (index, create, _id/index, _id/edit, components/{SelfInventoryForm, PlanPickerModal,
      product-tree.js, row-actions.js, export-excel.js}), components/subsystem-menu/{warehouse.js, finance.js}.
  Bối cảnh + quyết định: design.md, plan.md (Redmine #11814 #11817 #11819 #11822 #11823 #11825 #11826 #11857 #11887 #12039),
  spec docs/superpowers/specs/gop-db/2026-10-20-kiem-ke-theo-hang-hoa-design.md.
Ảnh: ./kkhh_shots — dev-hrm 06/11/2026 (_capture/capture.js, chặn mọi yêu cầu ghi). Giả trạng thái trên trình duyệt (sửa phản
  hồi GET, không gửi máy chủ): 12_edit, 13_delete (phiếu 1090 giả Đang tạo). Ảnh lỗi 10b_validate: bấm Lưu, yêu cầu bị chặn tại
  trình duyệt và trả lỗi kiểm tra giả đúng câu của máy chủ; 14b_result_validate: gọi hàm kiểm của form (không bấm Gửi duyệt).
  Các ảnh còn lại là trạng thái THẬT trên dev.
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

TEN = 'Kiểm kê theo hàng hóa'
SHOTS = os.path.join(HERE, 'kkhh_shots')
ICONS = os.path.join(SHOTS, 'icons')
KH_ICONS = os.path.join(HERE, '..', 'ke-hoach-kiem-ke-theo-hang-hoa', 'khkkhh_shots', 'icons')
KHT_ICONS = os.path.join(HERE, '..', 'ke-hoach-tong-kiem-ke-hang-hoa', 'khtkkhh_shots', 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Kiểm kho => Theo vị trí => Kiểm kê theo hàng hóa'
MENU_TC = 'Phân hệ Tài chính => Kiểm kê => Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả'
MENU_KH = 'Phân hệ Tài chính => Kiểm kê => Kế hoạch kiểm kê theo hàng hóa'
MENU_KHT = 'Phân hệ Tài chính => Kiểm kê => Kế hoạch tổng kiểm kê hàng hóa'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Kiểm kê theo hàng hóa.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
CONFLICT = '“Trạng thái đã bị thay đổi. Vui lòng load lại trang”'
NOTFOUND = '“Không tìm thấy phiếu kiểm kê hoặc bạn không có quyền xem.”'
NOPERM = '“Bạn không có quyền thực hiện chức năng này.”'
INVALID = '“Vui lòng kiểm tra lại thông tin đã nhập.”'
MISS = '“Bạn chưa nhập đầy đủ thông tin.”'
REQ = '“Bắt buộc phải nhập”'
PLAN404 = '“Không tìm thấy kế hoạch kiểm kê hoặc bạn không được lập phiếu cho kế hoạch này.”'
Q1 = 'Lập phiếu kiểm kê kho theo hàng hóa'
Q2 = 'Ban kiểm soát duyệt kết quả kiểm kê'
Q3 = 'Xử lý phiếu kiểm kê hàng hóa'
Q4 = 'Kế toán kho'
Q5 = 'Tạo phiếu nhập kho điều chỉnh kiểm kê'
V1 = 'Xem phiếu kiểm kê hàng hóa - theo tổng công ty'
V2 = 'Xem phiếu kiểm kê hàng hóa - theo công ty'

A_LP = 'Người lập phiếu (thủ kho)'
A_BKS = 'Ban kiểm soát'
A_XL = 'Người xử lý phiếu'
TN = ('Người dùng có quyền thực hiện chức năng: mọi người dùng đã được cấp tài khoản; phạm vi xem theo quyền “%s” / “%s”, '
      'không có quyền xem chỉ thấy phiếu mình tạo.' % (V1, V2))
TN_OWNER = 'Người dùng có quyền thực hiện chức năng: người lập phiếu (người tạo phiếu), phiếu đang ở trạng thái Đang tạo.'
DK = ('1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Kiểm kê theo hàng hóa.\n'
      '3. Dữ liệu hiển thị trong phạm vi xem theo quyền (Phần 2).')

d = SrsDoc(out=OUT, menu=MENU, route='/warehouse/self-inventories', full_url='', img_dir=UML)

d.set_menu_icons({**{k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Kiểm kho': 'menu_nhom', 'Theo vị trí': 'menu_nhom2', 'Kiểm kê theo hàng hóa': 'menu_muc',
    'Phân hệ Tài chính': 'menu_phanhe_tc', 'Kiểm kê': 'menu_nhom_tc', 'Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả': 'menu_muc_tc',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Tạo mới': 'btn_taomoi', 'Chọn kế hoạch kiểm kê': 'o_kehoach', 'Thêm hàng hóa': 'btn_themhang', 'Lưu và gửi': 'btn_luugui',
    'Sửa': 'btn_sua_row', 'Xóa': 'btn_xoa_row', 'Xem chi tiết': 'link_sophieu', 'Cập nhật kết quả': 'btn_capnhatkq_row',
    'Gửi duyệt': 'btn_guiduyet', 'Duyệt kết quả': 'btn_duyet', 'Không duyệt': 'btn_khongduyet', 'Xử lý': 'btn_xuly_row',
    'In': 'btn_in_row', 'In danh sách': 'btn_in_list', 'Xuất Excel': 'btn_xuatexcel', 'Lịch sử': 'btn_lichsu_row',
}.items()}, **{k: os.path.join(KH_ICONS, v + '.png') for k, v in {   # chặng menu màn Kế hoạch: icon thật của màn đó
    'Kế hoạch kiểm kê theo hàng hóa': 'menu_muc', 'Lập phiếu': 'btn_lapphieu_row',
}.items()}, **{k: os.path.join(KHT_ICONS, v + '.png') for k, v in {
    'Kế hoạch tổng kiểm kê hàng hóa': 'menu_muc', 'Lập phiếu kiểm kê': 'btn_lapphieu_row',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Kiểm kê theo hàng hóa — phiếu kiểm kê theo hàng hóa (mã phiếu '
    '<mã công ty>.KKK-NNNNN, ví dụ TPE.KKK-01097), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ cách thủ kho lập phiếu kiểm kê theo từng mặt hàng (lập tay, từ Kế hoạch kiểm kê theo hàng hóa hoặc từ Kế hoạch tổng '
    'kiểm kê hàng hóa), chọn kho – công ty thuê kho, thêm hàng và chọn ĐVT kiểm kê cho từng lô; nhập kết quả thực kiểm, hàng thừa '
    'khác và file kết quả; Ban kiểm soát duyệt / không duyệt; người xử lý lập phiếu điều chuyển vị trí / nhập kho / xuất kho điều '
    'chỉnh cho phần chênh lệch.',
    'Làm rõ vòng đời trạng thái của phiếu (Đang tạo → Đang kiểm → Chờ KT duyệt → Chờ xử lý → Đang xử lý → Hoàn thành; nhánh Không '
    'duyệt) và các màn khác đọc / ghi ngược dữ liệu phiếu.',
])
d.p('Phạm vi chức năng: Xem danh sách (2 lối vào: phân hệ Kho và lối “chờ duyệt kết quả” ở phân hệ Tài chính), Tìm kiếm và lọc, '
    'Cài đặt bộ lọc, Tùy chỉnh cột, Tạo phiếu (Lưu / Lưu và tiếp tục), Chọn kế hoạch kiểm kê, Thêm hàng hóa – Làm mới số liệu – ĐVT '
    'kiểm kê, Lưu và gửi (chuyển Đang kiểm), Chỉnh sửa, Xóa, Xem chi tiết, Cập nhật kết quả (Gửi duyệt), Duyệt kết quả, Không duyệt, '
    'Xử lý phiếu (Tạo phiếu điều chuyển vị trí / nhập kho điều chuyển / xuất kho điều chuyển), In phiếu / In danh sách, Xuất Excel '
    '(danh sách và 1 phiếu), Xem lịch sử thay đổi. Màn KHÔNG có Hủy phiếu, Khóa / Mở khóa và Import Excel.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phiếu ghi kết quả thực kiểm từng lô tại từng vị trí so với tồn theo lô chụp lúc thêm hàng; Chênh lệch = Thực kiểm − SL kiểm kê.',
    'Phiếu Đang kiểm / Chờ KT duyệt khóa các mặt hàng của nó tại kho của phiếu: Phiếu nhập kho, Phiếu điều chuyển hàng, Phiếu điều '
    'chuyển vị trí chặn hàng đang kiểm kho.',
    'Dòng chênh lệch là nguồn lập Phiếu điều chuyển vị trí / Phiếu nhập kho điều chỉnh kiểm kê / Phiếu xuất kho điều chỉnh kiểm kê; '
    'các phiếu đó ghi ngược số đã xử lý và đưa phiếu sang Đang xử lý / Hoàn thành.',
    'Kết quả của phiếu Hoàn thành là nguồn của Báo cáo hàng thừa thiếu sau tổng kiểm kê hàng hóa và Biên bản xử lý hàng thừa, thiếu '
    'sau kiểm kê.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Phiếu không tự ghi tồn kho; chỉ các phiếu xử lý lập từ phiếu mới đổi tồn (BR-01).',
    'Thêm mới không cần quyền riêng; chỉ người tạo mới Sửa / Xóa (khi Đang tạo) và Cập nhật kết quả (khi Đang kiểm / Không duyệt) (BR-03).',
    'Mỗi lô ≥ 1 dòng ĐVT kiểm kê, tổng SL × hệ số = tồn theo lô; hội đồng ≥ 1 thành viên không trùng (BR-04).',
    'Gửi duyệt bắt buộc Thực kiểm mọi dòng và ≥ 1 file kết quả khi phiếu chưa có file (BR-06).',
    'Xóa phiếu KHÔNG trả trạng thái kế hoạch nguồn (giữ như hệ thống cũ — BR-05).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu kiểm kê theo hàng hóa (phiếu)', 'Chứng từ <mã công ty>.KKK-NNNNN của màn này: kho, công ty thuê kho, danh sách hàng – vị '
                                            'trí – lô – tồn, ĐVT kiểm kê, kết quả thực kiểm, hàng thừa khác, file kết quả và hội '
                                            'đồng kiểm kê.'),
    ('Kế hoạch kiểm kê theo hàng hóa', 'Chứng từ <mã công ty>.KHKKHH-NNNNN (phân hệ Tài chính). Lập phiếu từ kế hoạch Đang kiểm: '
                                       'nạp kho + hàng của kế hoạch, KHÓA thêm / bớt hàng; kế hoạch chuyển Đã lập phiếu kiểm kê.'),
    ('Kế hoạch tổng kiểm kê hàng hóa', 'Chứng từ <mã công ty>.KHTKK-NNNNN (phân hệ Tài chính). Lập phiếu từ kế hoạch Đã duyệt còn '
                                       'trong kỳ: nạp kho, tự thêm hàng; mỗi hàng chỉ có ở 1 phiếu của cùng kế hoạch tổng.'),
    ('Kho / Công ty thuê kho', 'Kho vật lý (chọn nhiều) và các công ty có kho kế toán gắn kho đó (chọn nhiều); đổi kho tự chọn hết '
                               'công ty thuê của kho mới.'),
    ('SL tồn kho / Tồn theo lô', 'SL tồn kho = tồn của hàng trong các kho đã chọn; Tồn theo lô = tồn của lô tại vị trí lúc thêm hàng.'),
    ('ĐVT kiểm kê', 'Đơn vị dùng để đếm 1 lô; mặc định ĐVT cơ sở; đổi sang ĐVT lớn hơn thì lô tự tách dòng sao cho tổng quy đổi = '
                    'tồn theo lô.'),
    ('Thực kiểm / Chênh lệch', 'Thực kiểm = số đếm được; Chênh lệch = Thực kiểm − SL dòng (dương = thừa, âm = thiếu; khác 0 chữ đỏ).'),
    ('Hàng thừa khác', 'Hàng đếm được nhưng không có trong danh sách: hàng có mã (chọn từ danh mục) hoặc hàng mới (gõ tên + ĐVT), '
                       'kèm vị trí và Thực kiểm.'),
    ('Ban kiểm soát (BKS)', 'Người có quyền “%s”; duyệt / không duyệt kết quả.' % Q2),
    ('Trạng thái Đang tạo', 'Nhãn xám: phiếu vừa Lưu; chỉ người tạo thấy, sửa, xóa.'),
    ('Trạng thái Đang kiểm', 'Nhãn xanh dương: phiếu đã Lưu và gửi; người tạo nhập kết quả.'),
    ('Trạng thái Chờ KT duyệt', 'Nhãn vàng: đã Gửi duyệt kết quả, chờ Ban kiểm soát.'),
    ('Trạng thái Không duyệt', 'Nhãn đỏ: BKS không duyệt; người tạo nhập lại kết quả và gửi lại.'),
    ('Trạng thái Chờ xử lý', 'Nhãn vàng: đã duyệt, có dòng chênh lệch cần xử lý.'),
    ('Trạng thái Đang xử lý', 'Nhãn xanh dương: đã lập phiếu điều chuyển / nhập / xuất điều chỉnh nhưng chưa xử lý hết.'),
    ('Trạng thái Hoàn thành', 'Nhãn xanh lá: duyệt không chênh lệch, hoặc các phiếu xử lý đã xử lý hết chênh lệch.'),
    ('Cấu trúc phân cấp', 'Phiếu > hàng (SL tồn kho) > vị trí > lô (công ty, tồn theo lô) > dòng ĐVT kiểm kê (Thực kiểm, Chênh '
                          'lệch, Ghi chú); kèm kho, công ty thuê kho, hàng thừa khác, hội đồng, file kết quả.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn dùng 3 quyền nhóm “Kiểm kê theo hàng hóa” (phân hệ Kho) cộng các quyền dùng chung “%s”, “%s”, “%s” và “%s”. Quyền xét '
    'theo vai trò của công ty đang đăng nhập. Thêm mới không cần quyền riêng (giữ như hệ thống cũ); Sửa / Xóa / Cập nhật kết quả gắn '
    'với người tạo phiếu.' % (Q1, Q2, Q4, Q5))
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', Q1, 'Lập phiếu TỪ kế hoạch: nạp được kế hoạch đã chọn trong popup Chọn kế hoạch, nút Lập phiếu ở 2 màn Kế hoạch (Super '
               'admin được miễn). Lập tay không cần quyền này.'),
    ('Q2', Q2, 'Nút Duyệt (dòng), Duyệt kết quả / Không duyệt (chi tiết) ở phiếu Chờ KT duyệt; lối “chờ duyệt kết quả” thấy mọi phiếu '
               'Chờ KT duyệt; xem được phiếu Chờ KT duyệt dù ngoài phạm vi xem.'),
    ('Q3', Q3, 'Nút Xử lý (dòng) và 3 nút tạo phiếu xử lý ở phiếu Chờ xử lý / Đang xử lý; nhận thông báo khi phiếu được duyệt có chênh '
               'lệch; xem được phiếu Chờ xử lý / Đang xử lý dù ngoài phạm vi.'),
    ('Q4', Q4, 'Nhận thông báo “Chờ duyệt” khi phiếu cùng công ty được Gửi duyệt (không thêm nút trên màn).'),
    ('Q5', Q5, 'Cộng với Q3 mới hiện nút Tạo phiếu nhập kho điều chuyển.'),
    ('—', 'Không cần quyền (gắn người tạo)', 'Tạo mới (lập tay); Sửa, Xóa (Đang tạo); Cập nhật kết quả – Gửi duyệt (Đang kiểm / Không '
                                              'duyệt); In, Xuất Excel, Lịch sử với phiếu trong phạm vi xem.'),
], widths=[0.8, 1.9, 3.3])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', V1, 'Mọi phiếu của mọi công ty (lối phân hệ Kho).'),
    ('V2', V2, 'Phiếu của công ty người xem + phiếu mình tạo; công ty người xem trống → chỉ phiếu mình tạo.'),
    ('—', 'Không có quyền nào', 'Chỉ phiếu do chính mình tạo.'),
], widths=[0.8, 2.2, 3.0])
d.p('Với mọi quyền: phiếu Đang tạo chỉ hiện với chính người tạo. Lối “Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả”: có Q2 → mọi '
    'phiếu Chờ KT duyệt (không bó công ty); không có Q2 → chỉ phiếu mình tạo.')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'V1', 'V2', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ (theo V)', '✅ + lối chờ duyệt', '✅ (theo V)', '✅ mọi công ty', '✅ công ty mình + của mình', '✅ của mình'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo phiếu (lập tay)', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Chọn kế hoạch kiểm kê', '✅', '❌', '❌', '❌', '❌', '❌ (popup vẫn liệt kê, nạp bị từ chối)'),
    ('FR-07 Thêm hàng, Làm mới số liệu, ĐVT', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-08 Lưu và gửi', '✅', '✅', '✅', '✅', '✅', '✅'),
    ('FR-09 Chỉnh sửa', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo',
     '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo'),
    ('FR-10 Xóa', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo',
     '✅ người tạo, Đang tạo', '✅ người tạo, Đang tạo'),
    ('FR-11 Xem chi tiết', '✅ trong phạm vi', '✅ + phiếu Chờ KT duyệt', '✅ + phiếu Chờ / Đang xử lý', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-12 Cập nhật kết quả (Gửi duyệt)', '✅ người tạo', '✅ người tạo', '✅ người tạo', '✅ người tạo', '✅ người tạo', '✅ người tạo'),
    ('FR-13 Duyệt kết quả', '❌', '✅ Chờ KT duyệt', '❌', '❌', '❌', '❌'),
    ('FR-14 Không duyệt', '❌', '✅ Chờ KT duyệt', '❌', '❌', '❌', '❌'),
    ('FR-15 Xử lý phiếu', '❌', '❌', '✅ Chờ / Đang xử lý', '❌', '❌', '❌'),
    ('FR-16 In phiếu / In danh sách', '✅', '✅', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-17 Xuất Excel', '✅', '✅', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('FR-18 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅ trong phạm vi', '✅ của mình'),
    ('Hủy / Khóa – Mở khóa / Import', '—', '—', '—', '—', '—', '— (màn không có chức năng này)'),
], widths=[1.55, 0.8, 0.8, 0.75, 0.7, 0.8, 0.8])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có Q1: vẫn Tạo mới lập tay; chọn kế hoạch trong popup → ' + PLAN404 + '; vào từ nút Lập phiếu của kế hoạch → trang '
    '“Không tìm thấy trang”.',
    'Không có V1 / V2: vẫn vào màn, chỉ thấy phiếu mình tạo.',
    'Mở chi tiết / sửa / in / xuất / lịch sử của phiếu ngoài phạm vi (qua đường link): hệ thống báo ' + NOTFOUND +
    '; màn chi tiết / sửa chuyển sang trang “Không tìm thấy trang”.',
    'Thao tác khi phiếu đã đổi trạng thái (mở 2 tab) → ' + CONFLICT + '; đúng trạng thái nhưng không phải người tạo / thiếu quyền → ' + NOPERM + '.',
    'Mở màn Sửa của phiếu không còn Đang tạo hoặc không phải người tạo → tự chuyển về màn chi tiết.',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Tạo mới', 'Mọi người dùng (máy chủ trả cờ cho phép)', 'Fail-closed: mặc định ẩn tới khi máy chủ trả cờ'),
    ('Nút Sửa, Xóa', 'Phiếu Đang tạo và người xem là người tạo', 'Máy chủ kiểm lại khi lưu / xóa'),
    ('Nút Cập nhật kết quả (dòng), Gửi duyệt (chi tiết)', 'Phiếu Đang kiểm / Không duyệt và người xem là người tạo', 'Nút trên dòng chỉ mở chi tiết'),
    ('Nút Duyệt (dòng), Duyệt kết quả / Không duyệt (chi tiết)', 'Phiếu Chờ KT duyệt và có Q2', 'Nút trên dòng chỉ mở chi tiết'),
    ('Nút Xử lý (dòng)', 'Phiếu Chờ xử lý / Đang xử lý và có Q3', 'Mở chi tiết'),
    ('Nút Tạo phiếu điều chuyển vị trí', 'Q3 + có hàng tổng chênh = 0 nhưng còn dòng thiếu chưa xử lý + chưa có phiếu điều chuyển', 'Mở màn Phiếu điều chuyển vị trí'),
    ('Nút Tạo phiếu nhập kho điều chuyển', 'Q3 + Q5 + có hàng tổng chênh ≠ 0 còn dòng thừa + chưa có phiếu nhập kho điều chỉnh', 'Mở màn Phiếu nhập kho điều chỉnh kiểm kê'),
    ('Nút Tạo phiếu xuất kho điều chuyển', 'Q3 + có hàng tổng chênh ≠ 0 còn dòng thiếu + chưa có phiếu xuất kho điều chỉnh', 'Mở màn Phiếu xuất kho điều chỉnh kiểm kê'),
    ('Nút In, Xuất Excel, Lịch sử', 'Mọi dòng trong phạm vi', 'Hiện thẳng tối đa 3 nút, còn lại trong “Hành động khác”'),
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
     ('FR-12', 'Cập nhật kết quả (Gửi duyệt)', 'crud'),
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
     ('FR-07', 'Thêm hàng, Làm mới số liệu, ĐVT', 'crud', 'extend', [1, 3], None)],
    'Sơ đồ Use Case tổng quan màn Kiểm kê theo hàng hóa')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu kiểm kê',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu kiểm kê theo hàng hóa',
       mota='Hiển thị bảng phiếu kiểm kê theo hàng hóa trong phạm vi xem của người dùng, kèm kế hoạch nguồn, kho, trạng thái, người '
            'tạo / duyệt / cập nhật và các mốc ngày; phân trang và tổng số. Màn có 2 lối vào dùng chung một màn: phân hệ Kho (tiêu đề '
            '“Danh sách phiếu kiểm kê theo hàng hóa”, phạm vi theo quyền xem) và phân hệ Tài chính › Kiểm kê (tiêu đề “Phiếu kiểm kê '
            'theo hàng hóa chờ duyệt kết quả”, chỉ phiếu Chờ KT duyệt cho Ban kiểm soát). Mỗi dòng có liên kết sang chi tiết, liên kết '
            'sang kế hoạch và nút thao tác theo trạng thái + quyền.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng vào màn từ menu (2 lối vào), từ thông báo, hoặc từ liên kết ở màn '
                'khác (Phiếu điều chuyển vị trí, Phiếu nhập / xuất kho điều chỉnh kiểm kê, Biên bản xử lý hàng thừa thiếu).',
       chinh='1. Người dùng vào màn theo một trong hai đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem: lối Kho → V1 mọi phiếu / V2 công ty mình + của mình / không quyền của mình, luôn ẩn '
             'phiếu Đang tạo của người khác; lối chờ duyệt → có Q2 thì mọi phiếu Chờ KT duyệt, không thì phiếu mình tạo.\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (lưu riêng cho từng lối vào) và cấu hình cột đã lưu.\n'
             '4. Hệ thống lấy phiếu khớp bộ lọc, sắp phiếu tạo gần nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, dòng “Hiển thị a–b / N”, phân trang và nút thao tác theo cờ từng phiếu.',
       phu='• Không có phiếu nào khớp → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Máy chủ lỗi khi nạp danh sách → thông báo “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”, bảng trống.\n'
           '• Đang ở lối Kho bấm menu lối chờ duyệt (hoặc ngược lại) → hệ thống lưu bộ lọc lối cũ, nạp bộ lọc + phạm vi lối mới, '
           'đổi tiêu đề.\n'
           '• Bấm mã kế hoạch ở cột Kế hoạch kiểm kê → mở chi tiết kế hoạch (theo hàng hóa hoặc tổng).\n'
           '• Phiên đăng nhập hết hạn khi đang thao tác → thông báo hết phiên, chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện cả 13 cột. Cột khóa: STT, Số phiếu, Hành động; Số phiếu ghim trái khi cuộn ngang. Sắp xếp được: '
               'Số phiếu, Ngày kiểm kê, Ngày tạo, Ngày duyệt, Ngày cập nhật; mặc định (chưa chọn cột) phiếu tạo mới nhất ở trên. Đổi '
               'sắp xếp / bộ lọc / số dòng đều về trang 1. Từ chi tiết bấm Quay lại về đúng lối đã vào.'),
   layout=dict(entries=[
       (MENU, 'Lối chính (phân hệ Kho): danh sách theo phạm vi quyền xem.'),
       (MENU_TC, 'Lối phụ (phân hệ Tài chính): chỉ phiếu Chờ KT duyệt cho Ban kiểm soát.')],
       shot=shot('01_list'), shot_caption='Màn danh sách Kiểm kê theo hàng hóa (lối phân hệ Kho)'),
   extra=[(shot('00b_menu'), 'Menu phân hệ Kho › Kiểm kho › Theo vị trí'),
          (shot('04_wait_list'), 'Lối “Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả” (phân hệ Tài chính)'),
          (shot('03_rowmenu'), 'Nút thao tác trên dòng và menu Hành động khác')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Theo lối vào',
        ['- Lối Kho: “Danh sách phiếu kiểm kê theo hàng hóa”', '- Lối Tài chính: “Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả”',
         '- Hiện trên thanh tiêu đề, tiêu đề bảng và tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', 'Ẩn tới khi máy chủ trả cờ',
        ['- Rê chuột: “Tạo phiếu kiểm kê theo hàng hóa”', '- Bấm → mở màn Tạo phiếu (mục 2.5)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → cửa sổ Chọn trường xuất Excel (mục 2.17)',
         '- Khóa trong lúc đang xuất']),
       ('Nút In danh sách', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “In danh sách theo bộ lọc đang áp”', '- Bấm → cửa sổ Xem trước danh sách (mục 2.16)']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Đánh số liên tục theo trang', '- Cột khóa']),
       ('Cột Số phiếu', 'Table/Grid', 'Read-only', '<mã công ty>.KKK-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết (mục 2.11)', '- Sắp xếp được', '- Cột khóa, ghim trái khi cuộn ngang']),
       ('Cột Kế hoạch kiểm kê', 'Link', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mã kế hoạch theo hàng hóa (…KHKKHH-…) hoặc kế hoạch tổng (…KHTKK-…); trống nếu lập tay',
         '- Bấm → mở chi tiết kế hoạch', '- Không sắp xếp']),
       ('Cột Ngày kiểm kê', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', 'Hiển thị',
        ['- Ngày lập phiếu (lưu lại khi sửa thì cập nhật theo ngày lưu)', '- Sắp xếp được']),
       ('Cột Kho', 'Table/Grid', 'Read-only', '–', 'Hiển thị', ['- Tên các kho của phiếu, cách nhau dấu phẩy', '- Không sắp xếp']),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 7 giá trị', 'Hiển thị',
        ['- Đang tạo: xám', '- Đang kiểm, Đang xử lý: xanh dương', '- Chờ KT duyệt, Chờ xử lý: vàng', '- Không duyệt: đỏ',
         '- Hoàn thành: xanh lá', '- Không sắp xếp']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Họ tên người lập phiếu; không sắp xếp.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Thời điểm lập phiếu; sắp xếp được.'),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Người bấm Duyệt kết quả / Không duyệt; trống khi chưa duyệt.'),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu',
        ['- Thời điểm Duyệt kết quả; trống khi chưa duyệt (phiếu cũ của hệ thống trước luôn trống)', '- Sắp xếp được']),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', '- Thời điểm cập nhật gần nhất; sắp xếp được.'),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Họ tên người cập nhật gần nhất.'),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Sửa, Xóa: phiếu Đang tạo của chính mình (mục 2.9, 2.10)',
           '- Cập nhật kết quả: phiếu Đang kiểm / Không duyệt của mình → mở chi tiết (mục 2.12)',
           '- Duyệt: phiếu Chờ KT duyệt, có Q2 → mở chi tiết (mục 2.13)',
           '- Xử lý: phiếu Chờ xử lý / Đang xử lý, có Q3 → mở chi tiết (mục 2.15)',
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
        'Before:\n– Xác định lối vào theo menu đã bấm (phân hệ Kho / lối chờ duyệt kết quả).\n'
        '– Xác định phạm vi xem theo quyền V1 / V2 / Q2; khôi phục bộ lọc (10 phút, riêng từng lối) và cấu hình cột đã lưu.\n'
        'During:\n– Lấy phiếu khớp bộ lọc; ẩn phiếu Đang tạo của người khác; tính cờ nút từng phiếu.\n'
        '– Máy chủ lỗi → hiển thị “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, phiếu tạo mới nhất ở trên; hiện nút Tạo mới khi máy chủ trả cờ cho phép.'),
       ('Chuyển giữa 2 lối vào', 'System',
        'Before:\n– Đang ở màn danh sách của lối này, bấm menu của lối kia.\nDuring:\n– Lưu bộ lọc của lối cũ.\n'
        'After:\n– Nạp bộ lọc + phạm vi của lối mới, đổi tiêu đề, nạp lại từ trang 1.'),
       ('Bấm Số phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem.\nAfter:\n– Mở màn chi tiết (mục 2.11); bộ lọc được ghi nhớ 10 phút; Quay lại về đúng lối vào.'),
       ('Bấm mã ở cột Kế hoạch kiểm kê', 'Click',
        'Before:\n– Phiếu lập từ kế hoạch.\nAfter:\n– Mở chi tiết Kế hoạch kiểm kê theo hàng hóa / Kế hoạch tổng kiểm kê hàng hóa.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ Số phiếu, Ngày kiểm kê, Ngày tạo, Ngày duyệt, Ngày cập nhật hỗ trợ sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc.'),
       ('Bấm số trang hoặc đổi Số dòng/trang', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp.\nAfter:\n– Nạp dữ liệu trang mới (đổi số dòng → về trang 1, nạp 1 lần); STT liên tục.'),
       ('Bấm Cập nhật kết quả / Duyệt / Xử lý trên dòng', 'Click',
        'Before:\n– Nút chỉ hiện theo cờ của phiếu.\nAfter:\n– Mở màn chi tiết phiếu; thao tác thật làm ở chân màn chi tiết.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu kiểm kê theo hàng hóa',
       mota='Thu hẹp danh sách theo số phiếu, kho, trạng thái, người tạo, người duyệt, mã / tên hàng hóa trên phiếu và khoảng ngày '
            'tạo. Ô tìm nhanh tìm theo số phiếu; các ô lọc nằm trong khối Tìm kiếm nâng cao, bật / tắt được bằng Cài đặt bộ lọc '
            '(mục 2.3). Ô Kho có công tắc ổ khóa để liệt kê thêm kho đã khóa.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập số phiếu vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Hệ thống lọc ngay khi một ô chọn (Kho, Trạng thái, Người tạo, Người duyệt, Ngày tạo) đổi giá trị, về trang 1; ô chữ '
             'Mã hàng hóa / Tên hàng hóa áp khi bấm Tìm kiếm.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1 (giữ lối vào đang xem).\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Bật công tắc ổ khóa ở ô Kho → danh sách kho có thêm kho đã khóa (gắn biểu tượng ổ khóa); kho đang lọc vẫn hiện dù đã khóa.\n'
           '• Ô lọc bị tắt trong Cài đặt bộ lọc → không hiện trên khối lọc.',
       dacbiet='Ô tìm nhanh / Mã hàng hóa / Tên hàng hóa khớp một phần, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối; '
               'ký tự % và _ được hiểu là ký tự đại diện. Mã / Tên hàng hóa lọc phiếu có ít nhất 1 hàng khớp. Kho lọc phiếu có gắn kho '
               'đó. Ngày tạo lấy trọn hai ngày biên. Người tạo / Người duyệt chỉ liệt kê người đã lập / duyệt phiếu. Mọi điều kiện kết '
               'hợp kiểu VÀ. Ghi nhớ bộ lọc 10 phút khi đi vào màn con, riêng từng lối vào.'),
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
       ('Kho', 'Dropdown', 'Enable', 'Danh sách kho vật lý', 'Không', 'Trống',
        ['- Mặc định: trống (mọi kho)', '- Hiển thị “Mã - Tên”', '- Công tắc ổ khóa: bật thì liệt kê thêm kho đã khóa']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 7 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (mọi trạng thái)', '- Lựa chọn: Đang tạo / Đang kiểm / Chờ KT duyệt / Không duyệt / Chờ xử lý / Đang xử lý / Hoàn thành']),
       ('Người tạo', 'Dropdown', 'Enable', 'Người đã lập phiếu', 'Không', 'Trống', ['- Mặc định: trống', '- Hiển thị “Họ tên - Phòng ban - Mã NV”']),
       ('Người duyệt', 'Dropdown', 'Enable', 'Người đã duyệt phiếu', 'Không', 'Trống', ['- Mặc định: trống', '- Lọc phiếu do người đó duyệt / không duyệt']),
       ('Mã hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', '- Phiếu có ít nhất 1 hàng có mã chứa chuỗi nhập.'),
       ('Tên hàng hóa', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống', '- Phiếu có ít nhất 1 hàng có tên chứa chuỗi nhập.'),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai ngày biên; được bỏ trống một đầu']),
   ],
   ev=[
       ('Đổi giá trị một ô chọn', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\nDuring:\n– Bỏ qua khi giá trị không đổi.\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí (một lần).'),
       ('Bấm Tìm kiếm / nhấn Enter', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, Mã hàng hóa, Tên hàng hóa, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm phiếu có số phiếu chứa chuỗi nhập (và hàng khớp mã / tên).\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Có hoặc không có tiêu chí đang áp.\nDuring:\n– Giữ lối vào hiện tại.\nAfter:\n– Xóa mọi tiêu chí, bỏ sắp xếp, nạp lại từ trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\nDuring:\n– Lần mở đầu nạp lựa chọn Trạng thái, Kho, Người tạo, Người duyệt.\nAfter:\n– Mở / thu gọn khối.'),
       ('Bật / tắt công tắc ổ khóa ở ô Kho', 'Click',
        'Before:\n– Ô Kho đang hiện.\nDuring:\n– Không gọi lại danh sách.\nAfter:\n– Bật: liệt kê thêm kho đã khóa; tắt: ẩn kho đã khóa (trừ kho đang lọc).'),
       ('Quay lại từ màn con trong 10 phút', 'System',
        'Before:\n– Người dùng vừa đi từ danh sách vào màn chi tiết / tạo / sửa.\nDuring:\n– Đọc bộ lọc đã lưu của lối vào đó.\n'
        'After:\n– Khôi phục bộ lọc và trạng thái khối lọc; quá 10 phút thì bộ lọc về trống.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự. Cấu hình lưu riêng theo '
            'người dùng cho màn này (dùng chung cho cả 2 lối vào), không ảnh hưởng người khác và không đổi dữ liệu phiếu.',
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
        ['- Kho, Trạng thái, Người tạo, Người duyệt', '- Mã hàng hóa, Tên hàng hóa, Ngày tạo']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → mục đó không hiện ở khối Tìm kiếm nâng cao.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích lại đủ 7 mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
       ('Khối lọc sau khi lưu', 'Table/Grid', 'Read-only', '–', '–', 'Theo cấu hình', '- Chỉ hiện mục đã tích, đúng thứ tự đã kéo.'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click', 'Before:\n– Không cần quyền riêng.\nDuring:\n– Đọc cấu hình đang lưu.\nAfter:\n– Mở cửa sổ (chưa lưu lần nào → đủ 7 mục).'),
       ('Kéo đổi vị trí một mục', 'Drag', 'Before:\n– Kéo bằng biểu tượng kéo thả.\nDuring:\n– Chỉ đổi trong cửa sổ.\nAfter:\n– Cập nhật thứ tự; chỉ áp khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không gửi máy chủ.\nAfter:\n– Tích lại đủ 7 mục, thứ tự thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click', 'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nDuring:\n– Không gửi máy chủ.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 13 cột của bảng danh sách. Ba cột STT, Số phiếu, Hành động bị khóa; cấu '
            'hình lưu riêng theo người dùng trên máy chủ, chỉ đổi cách hiển thị, không đổi dữ liệu, bộ lọc hay tổng số. Cột đang hiện '
            'cũng là gợi ý tích sẵn khi Xuất Excel.',
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
         '- Ngày tạo, Người duyệt, Ngày duyệt, Ngày cập nhật, Người cập nhật, Hành động']),
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
       ('Bấm Cấu hình cột hiển thị', 'Click', 'Before:\n– Không cần quyền riêng.\nDuring:\n– Đọc cấu hình cột đang lưu.\nAfter:\n– Mở cửa sổ.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Cột khóa không đổi được vị trí.\nDuring:\n– Chỉ đổi trong cửa sổ.\nAfter:\n– Đổi thứ tự cột; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change', 'Before:\n– Cột khóa không cho bỏ tích.\nDuring:\n– Đếm lại số cột đang tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/13 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\nDuring:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không gửi máy chủ.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5 Tạo phiếu
FORM_UI = [
    ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
     ['- Tạo: “Tạo phiếu kiểm kê theo hàng hóa”', '- Sửa: “Sửa phiếu kiểm kê theo hàng hóa: <số phiếu>”']),
    ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập',
     '- Góc phải khối Thông tin chung: người tạo (màn Sửa: người tạo và giờ tạo).'),
    ('Ô Kế hoạch kiểm kê', 'Textbox', 'Enable', 'Kế hoạch được lập phiếu', 'Không', 'Trống',
     ['- Màn Tạo: gợi ý “Chọn kế hoạch kiểm kê”, bấm vào ô → popup Chọn kế hoạch (mục 2.6), nút × bỏ chọn',
      '- Màn Sửa / Chi tiết: chỉ đọc, mã là liên kết mở kế hoạch ở tab mới']),
    ('Ngày kiểm kê', 'Textbox', 'Disable', 'dd/mm/yyyy', 'Có', 'Ngày hiện tại', '- Không sửa được; khi lưu ghi ngày lưu.'),
    ('Kho', 'Dropdown', 'Enable / Disable', 'Danh sách kho vật lý', 'Có', 'Trống',
     ['- Chọn nhiều; gợi ý “Chọn kho”; hiển thị “Mã - Tên”', '- Có kế hoạch: khóa, lấy kho của kế hoạch (rê nhãn: “Kho lấy theo kế hoạch kiểm kê đã chọn.”)',
      '- Đổi kho khi đã có hàng → hộp “Đổi kho” (mục 2.7)', '- Lỗi: ' + REQ]),
    ('Công ty thuê kho', 'Dropdown', 'Enable / Disable', 'Công ty có kho kế toán gắn kho đã chọn', 'Có', 'Tự chọn hết khi chọn kho',
     ['- Chọn nhiều; khóa (gợi ý “Chọn công ty thuê kho”) khi chưa chọn kho', '- Đổi khi đã có hàng → hộp “Đổi công ty thuê kho”',
      '- Lỗi: ' + REQ]),
    ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống',
     ['- Gợi ý “Nhập ghi chú”; cao bằng các ô khác', '- Lỗi: “Vui lòng nhập tối đa 255 ký tự.”']),
    ('Bảng Hàng hóa', 'Table/Grid', 'Enable', '–', 'Có', '“Không có dữ liệu”',
     ['- Cột: STT, Tên hàng, Model, Mã hàng, ĐVT, SL tồn kho, Vị trí (tồn vị trí trong ngoặc), Công ty, Lô, Tồn theo lô, ĐVT kiểm kê *, Hành động',
      '- Gộp ô theo hàng → vị trí → lô; tiêu đề dính khi cuộn, cao tối đa 600px',
      '- Lỗi: ' + REQ + ' (chưa có hàng), lỗi của từng hàng hiện dưới Tên hàng']),
    ('Nút Làm mới số liệu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Góc phải khối Hàng hóa; đặc tả ở mục 2.7.'),
    ('Nút Thêm hàng hóa', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Ẩn khi lập từ Kế hoạch kiểm kê theo hàng hóa; đặc tả mục 2.7.'),
    ('Ô ĐVT kiểm kê', 'Dropdown', 'Enable', 'ĐVT của hàng', 'Có', 'ĐVT cơ sở',
     ['- Mỗi dòng kết quả của lô 1 ô; đổi ĐVT tách / gộp dòng (mục 2.7)', '- Lỗi: ' + REQ + ' / “Không thuộc hàng hóa này.”']),
    ('Nút Xóa hàng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Thùng rác đỏ ở cột Hành động; xóa hàng ngay, không hỏi.'),
    ('Khối Hội đồng kiểm kê', 'Table/Grid', 'Enable', '≥ 1 dòng', 'Có', '1 dòng trống',
     ['- Cột STT, Thành viên *, Chức vụ *, Hành động', '- Lập từ Kế hoạch theo hàng hóa: nạp sẵn hội đồng của kế hoạch, vẫn sửa được']),
    ('Nút Thêm dòng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải khối Hội đồng; bấm → thêm 1 dòng trống.'),
    ('Ô Thành viên', 'Dropdown', 'Enable', 'Nhân viên', 'Có', 'Trống',
     ['- Gợi ý “Chọn thành viên”', '- Chọn → tự điền Chức vụ đầu tiên của nhân viên', '- Lỗi: ' + REQ + ' / “Bị trùng.”']),
    ('Ô Chức vụ', 'Dropdown', 'Enable', 'Chức vụ của nhân viên', 'Có', 'Chức vụ đầu tiên', ['- Gợi ý “Chọn chức vụ”', '- Lỗi: ' + REQ]),
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
     ['- Thành công: “Lưu thành công.” / “Lưu và gửi thành công.”', '- Lỗi kiểm tra: ' + INVALID + ' (câu lỗi chi tiết hiện dưới từng ô)',
      '- Kế hoạch / phiếu đã đổi trạng thái: ' + CONFLICT, '- Lỗi khác: câu lỗi máy chủ hoặc “Lưu thất bại.”']),
]

SAVE_DURING = ('During:\n– Ghi chú > 255 ký tự → “Vui lòng nhập tối đa 255 ký tự.” (kiểm ngay trên form, không gửi).\n'
               '– Máy chủ kiểm và trả đủ lỗi cùng lúc: Kho, Công ty thuê kho, Hàng hóa trống → ' + REQ + '; Thành viên / Chức vụ '
               'trống → ' + REQ + '; Thành viên trùng → “Bị trùng.”; ĐVT kiểm kê trống → ' + REQ + '.\n'
               '– Hàng không còn vị trí tồn → “Hàng hóa chưa có vị trí tồn.”; vị trí không còn lô → “Vị trí chưa có lô tồn.”; vị '
               'trí ngoài kho đã chọn → “Không thuộc kho đã chọn.”; ĐVT không thuộc hàng → “Không thuộc hàng hóa này.”; tổng quy đổi '
               'lệch → “Tổng số lượng quy đổi (x) khác tồn theo lô (y).”.\n'
               '– Lập từ Kế hoạch tổng mà hàng đã có ở phiếu khác cùng kế hoạch → “Hàng hóa đã lập phiếu kiểm kê.” dưới tên hàng, '
               'dòng hàng tô đỏ.\n'
               '– Có lỗi → lỗi hiện dưới từng ô, thông báo ' + INVALID + ', cuộn tới ô lỗi đầu tiên.\n' + ERR)

fr(5, 'Tạo phiếu kiểm kê (Lưu / Lưu và tiếp tục)', usecase=('FR-05', 'Tạo phiếu kiểm kê', 'crud', A_LP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo phiếu kiểm kê theo hàng hóa',
       mota='Thủ kho lập phiếu kiểm kê theo từng mặt hàng: chọn kế hoạch (mục 2.6) hoặc lập tay (chọn kho, công ty thuê kho, Thêm '
            'hàng hóa), chỉnh ĐVT kiểm kê, khai hội đồng rồi bấm Lưu: phiếu ở trạng thái Đang tạo (chỉ người tạo thấy). Lập từ Kế '
            'hoạch kiểm kê theo hàng hóa thì kế hoạch chuyển Đã lập phiếu kiểm kê (kể cả khi chỉ Lưu). Thêm mới không cần quyền riêng.',
       tacnhan='Người dùng có quyền thực hiện chức năng: mọi người dùng đã đăng nhập (lập từ kế hoạch cần quyền “%s”).' % Q1,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có kho vật lý có hàng tồn theo lô, hoặc có kế hoạch được lập phiếu.',
       chinh='1. Người dùng bấm Tạo mới ở danh sách (hoặc Lập phiếu ở màn Kế hoạch — form nạp sẵn kế hoạch).\n'
             '2. Hệ thống mở màn “Tạo phiếu kiểm kê theo hàng hóa”: Ngày kiểm kê = hôm nay, Hội đồng có 1 dòng trống.\n'
             '3. Người dùng chọn kế hoạch (mục 2.6) hoặc chọn Kho (Công ty thuê kho tự chọn hết), bấm Thêm hàng hóa (mục 2.7).\n'
             '4. Người dùng chỉnh ĐVT kiểm kê từng lô nếu cần, nhập Ghi chú; khai Thành viên (Chức vụ tự điền), Thêm dòng nếu cần.\n'
             '5. Người dùng bấm Lưu.\n'
             '6. Hệ thống kiểm tra dữ liệu, lưu phiếu trạng thái Đang tạo với công ty / phòng ban / bộ phận của người tạo, sinh mã '
             '<mã công ty>.KKK-NNNNN; tên / mã / ĐVT / hệ số đọc lại từ danh mục, tồn theo lô lưu theo ảnh chụp trên form.\n'
             '7. Hệ thống ghi “Tạo mới” vào lịch sử phiếu; lập từ Kế hoạch theo hàng hóa → kế hoạch chuyển Đã lập phiếu kiểm kê, ghi '
             '“Thay đổi trạng thái” vào lịch sử kế hoạch (ghi chú “Lập phiếu kiểm kê <số phiếu>.”).\n'
             '8. Hệ thống hiển thị “Lưu thành công.” và chuyển về màn danh sách.',
       phu='• Bấm Lưu và tiếp tục → lưu như trên (Đang tạo), ở lại màn Tạo với form trắng (vào từ kế hoạch thì bỏ kế hoạch đã chọn).\n'
           '• Thiếu / sai dữ liệu → máy chủ báo đủ lỗi dưới từng ô cùng lúc, thông báo ' + INVALID + ', không lưu.\n'
           '• Kế hoạch vừa bị người khác lập phiếu / đổi trạng thái → ' + CONFLICT + ', không lưu.\n'
           '• Lập từ Kế hoạch theo hàng hóa mà không có quyền “%s” → %s.\n' % (Q1, NOPERM) +
           '• Bấm Quay lại / chuyển menu / đóng tab khi đã nhập → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa đổi gì → về danh '
           'sách ngay. Màn là trang riêng, không có (x) / click ra ngoài.\n'
           '• Lỗi máy chủ → câu lỗi hoặc “Lưu thất bại.”, dữ liệu đã nhập giữ nguyên.',
       dacbiet='Các nút lưu khóa trong lúc đang lưu để một lần bấm không tạo 2 phiếu. Phiếu không có trường nhập duy nhất: mã tự sinh '
               'theo công ty người tạo + số thứ tự, không sửa được. Lưu và Lưu và gửi dùng chung một bộ điều kiện. Form chỉ tự chặn '
               'định dạng (Ghi chú ≤ 255), bắt buộc / trùng do máy chủ trả về. Không kiểm phiếu nhập / xuất đang treo (giữ như hệ thống cũ).'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'), shot_caption='Màn Tạo phiếu lập tay sau khi chọn kho và thêm hàng'),
   extra=[(shot('10_create'), 'Màn Tạo phiếu lúc mới mở'),
          (shot('10b_validate_full'), 'Lỗi bắt buộc hiện cùng lúc dưới từng ô khi bấm Lưu thiếu dữ liệu'),
          (shot('10g_unsaved'), 'Hộp “Thông tin chưa lưu” khi rời màn')],
   ui=FORM_UI,
   ev=[
       ('Mở màn Tạo', 'System',
        'Before:\n– Nút Tạo mới hiện khi máy chủ trả cờ cho phép (mọi người dùng).\nDuring:\n– Nạp kho vật lý, công ty thuê kho theo kho, '
        'nhân viên kèm chức vụ, người tạo, ngày hôm nay; vào từ kế hoạch → nạp kế hoạch, không được lập → trang “Không tìm thấy trang”.\n'
        '– Lỗi → “Không tải được dữ liệu.”.\nAfter:\n– Hiển thị form, Hội đồng có 1 dòng trống; chưa tính là đã thay đổi.'),
       ('Chọn Thành viên', 'Change',
        'Before:\n– Danh sách nhân viên kèm chức vụ đã nạp.\nDuring:\n– Xóa lỗi của ô.\nAfter:\n– Tự điền Chức vụ đầu tiên của nhân viên; bỏ chọn → xóa Chức vụ.'),
       ('Bấm Thêm dòng / Xóa dòng hội đồng', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không gửi máy chủ.\nAfter:\n– Thêm 1 dòng trống / bỏ dòng đó và lỗi của dòng.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Thêm mới không kiểm quyền riêng.\n– Có Kế hoạch theo hàng hóa: kế hoạch phải còn Đang kiểm (không → %s) và có quyền “%s” '
        '(không → %s); Kế hoạch tổng phải Đã duyệt (không → %s).\n' % (CONFLICT, Q1, NOPERM, CONFLICT) + SAVE_DURING + '\n'
        'After:\n– Lưu phiếu trạng thái Đang tạo, sinh số phiếu, lưu kho, công ty thuê, hàng – vị trí – lô – dòng ĐVT, hội đồng.\n'
        '– Ghi một dòng lịch sử “Tạo mới”; Kế hoạch theo hàng hóa → Đã lập phiếu kiểm kê + lịch sử kế hoạch.\n'
        '– Hiển thị “Lưu thành công.”, về màn danh sách.'),
       ('Bấm Lưu và tiếp tục', 'Click',
        'Before:\n– Như Lưu.\nDuring:\n– Kiểm tra như Lưu.\n' + ERR + '\n'
        'After:\n– Lưu như Lưu (Đang tạo), ghi lịch sử “Tạo mới”, hiển thị “Lưu thành công.”, bỏ kế hoạch trên đường dẫn, làm trắng form và ở lại màn Tạo.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– So dữ liệu hiện tại với lúc mở màn.\nDuring:\n– Có thay đổi → hiện hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách, không lưu; Ở lại: giữ nguyên form.'),
   ])

# ------------------------------------------------------------ 2.6 Chọn kế hoạch
fr(6, 'Chọn kế hoạch kiểm kê', usecase=('FR-06', 'Chọn kế hoạch kiểm kê', 'crud', A_LP),
   rule=('- Màn Thêm mới, Bộ lọc và Dropdown.', 'create'),
   intro=dict(
       ten='Chọn kế hoạch kiểm kê để lập phiếu',
       mota='Ở màn Tạo, bấm ô Kế hoạch kiểm kê mở popup “Chọn kế hoạch kiểm kê hàng hóa” liệt kê chung 2 loại: Kế hoạch kiểm kê theo '
            'hàng hóa đang ở trạng thái Đang kiểm và Kế hoạch tổng kiểm kê hàng hóa Đã duyệt còn trong kỳ (ngày bắt đầu và ngày kết '
            'thúc từ hôm nay trở đi). Chọn 1 dòng → form nạp kho, công ty thuê kho (chọn hết), ghi chú; với kế hoạch theo hàng hóa '
            'nạp thêm hàng của kế hoạch (tồn hiện tại, khóa thêm / bớt hàng) và hội đồng; với kế hoạch tổng người dùng tự thêm hàng.',
       tacnhan='Người dùng có quyền thực hiện chức năng: %s (Super admin được miễn).' % Q1,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo phiếu.\n3. Có kế hoạch Đang kiểm / kế hoạch tổng Đã duyệt còn trong kỳ.',
       chinh='1. Người dùng bấm vào ô Kế hoạch kiểm kê.\n'
             '2. Hệ thống mở popup, nạp trang 1 danh sách kế hoạch (mới nhất ở trên).\n'
             '3. Người dùng nhập mã phiếu / chọn Người tạo, bấm Tìm kiếm (hoặc Enter); sắp xếp / đổi trang nếu cần.\n'
             '4. Người dùng bấm vào một dòng.\n'
             '5. Hệ thống kiểm quyền và trạng thái kế hoạch, đóng popup, nạp kế hoạch vào form; khóa ô Kho, Công ty thuê kho; kế '
             'hoạch theo hàng hóa thì ẩn nút Thêm hàng hóa và nút xóa hàng.\n'
             '6. Hàng của kế hoạch đã hết tồn → cảnh báo vàng “Có N hàng hóa đã hết tồn trong kho đã chọn, không đưa vào phiếu: <tối đa '
             '5 mã> …”.',
       phu='• Không có kế hoạch nào → “Không có kế hoạch kiểm kê phù hợp.”.\n'
           '• Bấm mã kế hoạch trong popup → mở chi tiết kế hoạch ở tab mới, không chọn dòng.\n'
           '• Không có quyền / kế hoạch không còn được lập → ' + PLAN404 + '.\n'
           '• Bấm × trong ô Kế hoạch → bỏ kế hoạch, form về trạng thái lập tay trống.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng popup, form giữ nguyên.\n'
           '• Màn Sửa không đổi được kế hoạch (rê nhãn: “Kế hoạch kiểm kê chỉ chọn được lúc tạo phiếu, khi sửa phiếu giữ nguyên kế hoạch đã chọn.”).',
       dacbiet='Popup không lọc theo quyền (giữ như hệ thống cũ) — quyền kiểm khi nạp kế hoạch. Vào từ nút Lập phiếu ở màn Kế hoạch: '
               'form tự nạp kế hoạch, không mở popup; không được lập → trang “Không tìm thấy trang”.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới => Chọn kế hoạch kiểm kê', 'Popup mở ngay trên màn Tạo phiếu.'),
       (MENU_KH + ' => Lập phiếu', 'Mở màn Tạo phiếu đã nạp sẵn Kế hoạch kiểm kê theo hàng hóa (kế hoạch Đang kiểm).'),
       (MENU_KHT + ' => Lập phiếu kiểm kê', 'Mở màn Tạo phiếu đã nạp sẵn Kế hoạch tổng kiểm kê (kế hoạch Đã duyệt còn trong kỳ).')],
       shot=shot('11_plan_picker'), shot_caption='Popup Chọn kế hoạch kiểm kê hàng hóa'),
   extra=[(shot('11b_from_plan'), 'Màn Tạo phiếu sau khi chọn Kế hoạch tổng kiểm kê: kho, công ty thuê kho khóa theo kế hoạch')],
   ui=[
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        ['- “Chọn kế hoạch kiểm kê hàng hóa”', '- Dòng phụ “Kế hoạch kiểm kê theo hàng hóa đang kiểm và kế hoạch tổng kiểm kê đã duyệt”']),
       ('Ô Mã phiếu', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập mã kế hoạch kiểm kê”', '- Khớp một phần mã', '- Có nút × xóa nhanh']),
       ('Ô Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', '- Gợi ý “Chọn người tạo”.'),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Áp ô Mã phiếu + Người tạo, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Xóa điều kiện, bỏ sắp xếp, nạp lại trang 1.'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- Liên tục theo trang.'),
       ('Cột Mã phiếu', 'Link', 'Read-only', '–', '–', 'Hiển thị', ['- Mã kế hoạch (…KHKKHH-… hoặc …KHTKK-…); sắp xếp được', '- Bấm → mở chi tiết kế hoạch ở tab mới']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', '–', 'Hiển thị', '- Người lập kế hoạch; sắp xếp được.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', '–', 'Hiển thị', '- Sắp xếp được; mặc định mới nhất trên.'),
       ('Dòng kế hoạch', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu', '- Bấm cả dòng → chọn kế hoạch, đóng popup.'),
       ('Phân trang popup', 'Pagination', 'Enable', 'Danh sách số dòng', '–', 'Theo mặc định popup', '- Dòng “Hiển thị a–b / N”.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- “Không có kế hoạch kiểm kê phù hợp.”'),
       ('Nút × trong ô Kế hoạch', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi chưa chọn', '- Bỏ kế hoạch, làm trắng form.'),
       ('Cảnh báo hàng hết tồn', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        '- Vàng: “Có N hàng hóa đã hết tồn trong kho đã chọn, không đưa vào phiếu: <mã> … và M hàng hóa khác.”'),
   ],
   ev=[
       ('Bấm ô Kế hoạch kiểm kê', 'Click',
        'Before:\n– Chỉ màn Tạo.\nDuring:\n– Lấy Kế hoạch theo hàng hóa Đang kiểm + Kế hoạch tổng Đã duyệt còn trong kỳ (không lọc quyền).\n'
        'After:\n– Mở popup, hiện trang 1.'),
       ('Bấm Tìm kiếm / Làm mới / sắp xếp / đổi trang', 'Click',
        'Before:\n– Popup đang mở.\nDuring:\n– Lọc theo mã, người tạo.\nAfter:\n– Nạp lại danh sách theo điều kiện, thứ tự, trang mới.'),
       ('Bấm một dòng kế hoạch', 'Click',
        'Before:\n– Kiểm quyền “%s” (Super admin được miễn) và trạng thái kế hoạch; không đạt → %s.\n' % (Q1, PLAN404) +
        'During:\n– Kế hoạch theo hàng hóa: lấy hàng có tồn hiện tại tại các kho của kế hoạch theo công ty thuê kho; hàng hết tồn bị bỏ.\n'
        'After:\n– Đóng popup, nạp kho, công ty thuê kho, ghi chú, hàng (kế hoạch theo hàng hóa), hội đồng; cảnh báo hàng hết tồn nếu có.'),
       ('Bấm × bỏ kế hoạch', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không gửi máy chủ.\nAfter:\n– Xóa kế hoạch, kho, công ty thuê, hàng; hội đồng 1 dòng trống.'),
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không gửi máy chủ.\nAfter:\n– Đóng popup, form giữ nguyên.'),
   ])

# ------------------------------------------------------------ 2.7 Thêm hàng + Làm mới + ĐVT
fr(7, 'Thêm hàng hóa, Làm mới số liệu và ĐVT kiểm kê', usecase=('FR-07', 'Thêm hàng, Làm mới số liệu, ĐVT', 'crud', A_LP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Thêm hàng hóa, làm mới tồn và chọn ĐVT kiểm kê',
       mota='Thêm hàng hóa mở popup chọn hàng chỉ liệt kê hàng còn tồn ở các kho và công ty thuê kho đang chọn; mỗi hàng chọn được hệ '
            'thống lấy các vị trí có lô của công ty thuê kho, rồi nạp MỌI lô còn tồn trong vị trí đó (kể cả lô của công ty khác), '
            'mỗi lô 1 dòng ĐVT cơ sở = tồn theo lô. Làm mới số liệu cập nhật lại tồn theo lô, bỏ lô / vị trí / hàng đã hết tồn. Đổi '
            'ĐVT kiểm kê sang đơn vị lớn hơn thì lô tự tách dòng sao cho tổng quy đổi bằng tồn theo lô.',
       tacnhan='Người dùng có quyền thực hiện chức năng: người lập phiếu (màn Tạo) hoặc người tạo phiếu Đang tạo (màn Sửa).',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo hoặc Sửa phiếu.\n3. Thêm hàng: đã chọn Kho; phiếu không lập '
                'từ Kế hoạch kiểm kê theo hàng hóa.',
       chinh='1. Người dùng bấm Thêm hàng hóa; hệ thống mở popup “Thêm hàng hóa” (chỉ hàng có tồn trong kho + công ty thuê kho đã chọn, '
             'bỏ hàng đã có trên phiếu).\n'
             '2. Người dùng tích một hoặc nhiều hàng, bấm chọn.\n'
             '3. Hệ thống lấy vị trí – lô còn tồn, thêm hàng vào bảng (SL tồn kho kèm tách theo công ty thuê), báo “Thêm thành công.”.\n'
             '4. Người dùng đổi ĐVT kiểm kê của một dòng: SL dòng = phần nguyên (SL còn lại / hệ số); phần dư > 0 thêm 1 dòng ĐVT cơ '
             'sở; dư 0 bỏ các dòng sau.\n'
             '5. Người dùng bấm Làm mới số liệu; hệ thống lấy lại tồn theo lô của mọi dòng, báo “Làm mới số liệu thành công.” (hoặc '
             '“… Đã bỏ N hàng hóa hết tồn.”).',
       phu='• Chưa chọn kho mà bấm Thêm hàng hóa → “Vui lòng chọn kho trước khi thêm hàng hóa.”, ô Kho báo ' + REQ + '.\n'
           '• Chọn lại hàng đã có → “Hàng hóa đã được chọn.”.\n'
           '• Hàng chọn được nhưng đã hết tồn → cảnh báo vàng “Có N hàng hóa đã hết tồn trong kho đã chọn, không đưa vào phiếu: …”.\n'
           '• Đổi ĐVT mà SL không đủ quy đổi → “Số lượng không đủ để quy đổi!”, trả ĐVT cũ.\n'
           '• Bấm × ở ô ĐVT kiểm kê → ô trống, khi lưu máy chủ báo ' + REQ + ' tại ô.\n'
           '• Đổi Kho / Công ty thuê kho khi đã có hàng → hộp “Đổi kho” / “Đổi công ty thuê kho”: Đồng ý = đổi và xóa danh sách hàng; '
           'Hủy = giữ giá trị cũ.',
       dacbiet='Nút Thêm hàng hóa và Làm mới số liệu khóa trong lúc đang lấy tồn. Máy chủ đọc lại hệ số quy đổi theo danh mục hàng, '
               'không tin hệ số gửi lên. Đổi kho tự chọn hết công ty thuê của kho mới. Số tồn là ảnh chụp lúc thêm / làm mới.'),
   layout=dict(menu=MENU + ' => Tạo mới => Thêm hàng hóa', shot=shot('10f_picker'), shot_caption='Popup Thêm hàng hóa (chỉ hàng còn tồn trong kho đã chọn)'),
   extra=[(shot('10c_filled_full'), 'Bảng Hàng hóa sau khi thêm hàng, cột ĐVT kiểm kê từng lô'),
          (shot('10e_doikho'), 'Hộp xác nhận “Đổi kho” khi đã có hàng')],
   ui=[
       ('Nút Thêm hàng hóa', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị',
        ['- Góc phải khối Hàng hóa', '- Ẩn khi lập từ Kế hoạch kiểm kê theo hàng hóa', '- Khóa trong lúc lấy tồn']),
       ('Popup Thêm hàng hóa', 'Modal', 'Hiển thị', 'Hàng có tồn trong kho + công ty thuê đã chọn', 'Có ≥ 1 hàng', 'Ẩn',
        ['- Tìm, lọc nâng cao, tích nhiều hàng', '- Hàng đã có trên phiếu không chọn lại được']),
       ('Nút Làm mới số liệu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Rê chuột: “Cập nhật lại tồn theo lô của các hàng trong bảng”', '- Khóa trong lúc đang làm mới']),
       ('Cột SL tồn kho', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', '- Tồn của hàng trong các kho đã chọn.'),
       ('Cột Vị trí', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Mã vị trí, tồn của hàng tại vị trí trong ngoặc.'),
       ('Cột Công ty / Lô', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Mã công ty sở hữu lô, số lô.'),
       ('Cột Tồn theo lô', 'Table/Grid', 'Read-only', '> 0', '–', 'Tồn lô', '- SL của dòng theo ĐVT kiểm kê; tự tính khi đổi ĐVT.'),
       ('Ô ĐVT kiểm kê', 'Dropdown', 'Enable', 'ĐVT của hàng', 'Có', 'ĐVT cơ sở',
        ['- Lựa chọn: các ĐVT khai cho hàng', '- Đổi → tách / gộp dòng của lô', '- Gợi ý “Chọn ĐVT”; có nút × xóa']),
       ('Hộp “Đổi kho” / “Đổi công ty thuê kho”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Đổi kho sẽ xóa danh sách hàng hóa đã chọn. Bạn có muốn tiếp tục?”',
         '- “Đổi công ty thuê kho sẽ xóa danh sách hàng hóa đã chọn. Bạn có muốn tiếp tục?”', '- Nút Đồng ý, Hủy']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Thêm thành công.” / “Hàng hóa đã được chọn.”', '- “Vui lòng chọn kho trước khi thêm hàng hóa.”',
         '- “Làm mới số liệu thành công.” / “Làm mới số liệu thất bại.”', '- “Số lượng không đủ để quy đổi!”',
         '- “Không tải được tồn kho của hàng hóa.”']),
       ('Cảnh báo hàng hết tồn', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- Vàng, nêu tối đa 5 mã hàng.'),
   ],
   ev=[
       ('Bấm Thêm hàng hóa', 'Click',
        'Before:\n– Đã chọn Kho, nếu không → “Vui lòng chọn kho trước khi thêm hàng hóa.”.\nDuring:\n– Mở popup với điều kiện tồn theo kho + công ty thuê kho.\n'
        'After:\n– Hiện popup Thêm hàng hóa.'),
       ('Chọn hàng trong popup', 'Click',
        'Before:\n– Bỏ hàng đã có trên phiếu; không còn hàng mới → “Hàng hóa đã được chọn.”.\n'
        'During:\n– Lấy vị trí có lô của công ty thuê kho, nạp mọi lô còn tồn của vị trí; hàng hết tồn → cảnh báo vàng.\n' + ERR + '\n'
        'After:\n– Thêm hàng vào bảng (mỗi lô 1 dòng ĐVT cơ sở), báo “Thêm thành công.”.'),
       ('Đổi ĐVT kiểm kê', 'Change',
        'Before:\n– Lấy SL còn lại của lô trước dòng đó.\nDuring:\n– Phần nguyên SL / hệ số = 0 → “Số lượng không đủ để quy đổi!”, trả ĐVT cũ.\n'
        'After:\n– Đặt SL dòng; phần dư > 0 thêm dòng ĐVT cơ sở; dư 0 bỏ các dòng sau.'),
       ('Bấm Làm mới số liệu', 'Click',
        'Before:\n– Bảng có ít nhất 1 dòng; khóa nút.\nDuring:\n– Lấy tồn hiện tại theo vị trí – lô – ĐVT; lô / vị trí / hàng hết tồn bị bỏ.\n' + ERR + '\n'
        'After:\n– Cập nhật tồn, xóa lỗi cũ; báo “Làm mới số liệu thành công.” (kèm số hàng đã bỏ).'),
       ('Đổi Kho / Công ty thuê kho khi đã có hàng', 'Change',
        'Before:\n– Bảng Hàng hóa có dữ liệu.\nDuring:\n– Giữ giá trị cũ trên ô, hiện hộp xác nhận.\n'
        'After:\n– Đồng ý: đổi giá trị, xóa danh sách hàng (đổi kho tự chọn hết công ty thuê của kho mới); Hủy: giữ giá trị cũ.'),
   ])

# ------------------------------------------------------------ 2.8 Lưu và gửi
fr(8, 'Lưu và gửi phiếu (chuyển Đang kiểm)', usecase=('FR-08', 'Lưu và gửi', 'action', A_LP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Lưu và gửi phiếu sang bước kiểm',
       mota='Ở màn Tạo hoặc Sửa, nút Lưu và gửi lưu phiếu và chuyển thẳng sang trạng thái Đang kiểm: phiếu hiện với người có quyền '
            'xem, người tạo bắt đầu cập nhật kết quả; các mặt hàng của phiếu tại kho của phiếu bị coi là đang kiểm kho (chặn nhập / '
            'điều chuyển). Không có hộp xác nhận và không gửi thông báo (giữ như hệ thống cũ).',
       tacnhan='Người dùng có quyền thực hiện chức năng: người lập phiếu (màn Tạo); người tạo phiếu Đang tạo (màn Sửa).',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Đang ở màn Tạo, hoặc màn Sửa của phiếu Đang tạo do mình tạo.\n'
                '3. Đủ dữ liệu bắt buộc như mục 2.5.',
       chinh='1. Người dùng nhập đủ thông tin (như mục 2.5) và bấm Lưu và gửi.\n'
             '2. Hệ thống kiểm tra dữ liệu như nút Lưu.\n'
             '3. Hệ thống lưu phiếu trạng thái Đang kiểm (màn Tạo: sinh số phiếu, Kế hoạch theo hàng hóa → Đã lập phiếu kiểm kê; màn '
             'Sửa: kiểm lại phiếu còn Đang tạo, đúng người tạo; Ngày kiểm kê = ngày lưu).\n'
             '4. Hệ thống ghi nhận lịch sử: màn Tạo “Tạo mới”; màn Sửa “Thay đổi thông tin” (nếu đổi dữ liệu) và “Thay đổi trạng '
             'thái” Đang tạo → Đang kiểm.\n'
             '5. Hệ thống hiển thị “Lưu và gửi thành công.” và chuyển về màn danh sách.',
       phu='• Thiếu dữ liệu → như mục 2.5, không lưu.\n'
           '• Phiếu đã bị đổi trạng thái / xóa ở tab khác → ' + CONFLICT + ' / ' + NOTFOUND + ', không lưu.\n'
           '• Không phải người tạo → ' + NOPERM + '.\n'
           '• Sau khi gửi phiếu không sửa / xóa được nữa; người tạo thấy nút Cập nhật kết quả.',
       dacbiet='Không hộp xác nhận; nút khóa trong lúc lưu. Hàng của phiếu Đang kiểm / Chờ KT duyệt bị chặn ở Phiếu nhập kho, Phiếu '
               'điều chuyển hàng và Phiếu điều chuyển vị trí tại kho của phiếu cho tới khi phiếu được duyệt / không duyệt.'),
   layout=dict(entries=[
       (MENU + ' => Tạo mới => Lưu và gửi', 'Gửi ngay khi tạo phiếu.'),
       (MENU + ' => Sửa => Lưu và gửi', 'Gửi phiếu Đang tạo đã lưu trước đó.')],
       shot=shot('10c_filled'), shot_caption='Nút Lưu và gửi ở chân màn Tạo phiếu'),
   ui=[
       ('Nút Lưu và gửi', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Màu chính, biểu tượng máy bay giấy', '- Rê chuột: “Lưu và gửi phiếu sang bước kiểm (trạng thái Đang kiểm)”', '- Khóa trong lúc lưu']),
       ('Các trường của form', 'Table/Grid', 'Enable', '–', 'Như mục 2.5', 'Như mục 2.5',
        '- Kho, Công ty thuê kho, Hàng hóa + ĐVT kiểm kê, Hội đồng — cùng điều kiện bắt buộc với nút Lưu.'),
       ('Nhãn trạng thái sau khi gửi', 'Badge', 'Read-only', '–', '–', 'Đang kiểm', '- Nhãn xanh dương “Đang kiểm” ở danh sách.'),
       ('Nút Cập nhật kết quả trên dòng', 'Icon Button', 'Read-only', '–', '–', 'Hiển thị với người tạo', '- Xuất hiện sau khi gửi (mục 2.12).'),
       ('Nút Sửa, Xóa trên dòng', 'Icon Button', 'Read-only', '–', '–', 'Ẩn sau khi gửi', '- Phiếu không còn Đang tạo.'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Lưu và gửi thành công.”'),
       ('Thông báo lỗi kiểm tra', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- ' + INVALID),
       ('Thông báo xung đột', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + CONFLICT, '- ' + NOPERM]),
       ('Lỗi dưới từng ô', 'Label', 'Hiển thị', '–', '–', 'Ẩn', '- Như mục 2.5 (Kho, Công ty thuê kho, Hàng hóa, ĐVT kiểm kê, Thành viên, Chức vụ).'),
       ('Lịch sử sau khi gửi', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Mốc “Tạo mới” hoặc “Thay đổi trạng thái” Đang tạo → Đang kiểm.'),
       ('Khóa hàng đang kiểm kho', 'Label', 'Read-only', '–', '–', 'Không hiển thị trên màn', '- Hàng của phiếu bị chặn ở màn khác (BR-10).'),
   ],
   ev=[
       ('Bấm Lưu và gửi (màn Tạo)', 'Click',
        'Before:\n– Thêm mới không kiểm quyền riêng; có kế hoạch thì kiểm như mục 2.5.\n' + SAVE_DURING + '\n'
        'After:\n– Lưu phiếu trạng thái Đang kiểm, sinh số phiếu; Kế hoạch theo hàng hóa → Đã lập phiếu kiểm kê.\n'
        '– Ghi một dòng lịch sử “Tạo mới”.\n– Hiển thị “Lưu và gửi thành công.”, về danh sách.'),
       ('Bấm Lưu và gửi (màn Sửa)', 'Click',
        'Before:\n– Phiếu phải Đang tạo, nếu không → ' + CONFLICT + '; người bấm phải là người tạo, nếu không → ' + NOPERM + '.\n' + SAVE_DURING + '\n'
        'After:\n– Ghi đè dữ liệu, trạng thái Đang kiểm, Ngày kiểm kê = ngày lưu.\n– Ghi lịch sử “Thay đổi thông tin” (nếu có) + “Thay đổi trạng thái”.\n'
        '– Hiển thị “Lưu và gửi thành công.”, về danh sách.'),
       ('Mở lại phiếu đã gửi', 'System',
        'Before:\n– Phiếu Đang kiểm.\nDuring:\n– Tính lại cờ nút.\nAfter:\n– Danh sách / chi tiết không còn Sửa, Xóa; người tạo có Cập nhật kết quả.'),
       ('Màn khác kiểm hàng đang kiểm kho', 'System',
        'Before:\n– Phiếu Đang kiểm / Chờ KT duyệt.\nDuring:\n– Màn khác so hàng + kho của chứng từ với phiếu.\nAfter:\n– Phiếu nhập kho báo “Hàng <tên> đang kiểm kho!”; Phiếu điều chuyển hàng báo '
        '“Hàng hóa đang được kiểm kho, không thể điều chuyển”; Phiếu điều chuyển vị trí chặn hàng đang kiểm.'),
   ])

# ------------------------------------------------------------ 2.9 Sửa
fr(9, 'Chỉnh sửa phiếu kiểm kê', usecase=('FR-09', 'Chỉnh sửa phiếu', 'crud', A_LP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Chỉnh sửa phiếu kiểm kê theo hàng hóa',
       mota='Người tạo sửa phiếu còn Đang tạo: đổi kho / công ty thuê kho, thêm / bớt hàng (phiếu lập tay hoặc từ kế hoạch tổng), làm '
            'mới số liệu, chỉnh ĐVT kiểm kê, ghi chú, hội đồng; lưu giữ Đang tạo (Lưu) hoặc gửi luôn (Lưu và gửi, mục 2.8). Khi mở '
            'màn Sửa hàng được nạp lại theo TỒN HIỆN TẠI; hàng đã hết tồn bị bỏ và có cảnh báo vàng. Kế hoạch kiểm kê không đổi được.',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo phiếu.\n3. Phiếu đang ở trạng thái Đang tạo.',
       chinh='1. Người dùng bấm Sửa ở cột Hành động hoặc ở màn chi tiết.\n'
             '2. Hệ thống mở màn “Sửa phiếu kiểm kê theo hàng hóa: <số phiếu>”, điền sẵn dữ liệu, hàng nạp theo tồn hiện tại.\n'
             '3. Người dùng sửa thông tin.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống kiểm lại phiếu còn Đang tạo và đúng người tạo, kiểm tra dữ liệu như mục 2.5 (kế hoạch tổng: kiểm hàng trùng '
             'phiếu khác, trừ chính phiếu này).\n'
             '6. Hệ thống ghi đè kho, công ty thuê, hàng, hội đồng, ghi chú; Ngày kiểm kê = ngày lưu; giữ nguyên kế hoạch.\n'
             '7. Hệ thống ghi nhận “Thay đổi thông tin” trong lịch sử (cũ → mới) — không đổi gì thì không ghi.\n'
             '8. Hệ thống hiển thị “Lưu thành công.” và chuyển về màn danh sách.',
       phu='• Mở màn Sửa của phiếu không còn Đang tạo / không phải người tạo → tự chuyển sang màn chi tiết.\n'
           '• Phiếu ngoài phạm vi / đã bị xóa → trang “Không tìm thấy trang”.\n'
           '• Lưu khi phiếu vừa bị gửi / xóa ở tab khác → ' + CONFLICT + ' hoặc ' + NOTFOUND + '.\n'
           '• Thiếu dữ liệu → như mục 2.5.\n'
           '• Quay lại khi đã sửa → hộp “Thông tin chưa lưu”; không sửa gì → về danh sách ngay.',
       dacbiet='Phiếu không có trường duy nhất nên không kiểm trùng. Màn Sửa không có nút Lưu và tiếp tục, không có ô chọn kế hoạch '
               '(rê nhãn Kế hoạch kiểm kê: “Kế hoạch kiểm kê chỉ chọn được lúc tạo phiếu, khi sửa phiếu giữ nguyên kế hoạch đã chọn.”). '
               'Phiếu lập từ kế hoạch: Kho, Công ty thuê kho khóa; từ Kế hoạch theo hàng hóa thì không thêm / bớt hàng.'),
   layout=dict(menu=MENU + ' => Sửa', shot=shot('12_edit'), shot_caption='Màn Sửa phiếu kiểm kê theo hàng hóa'),
   ui=FORM_UI[:2] + [
       ('Ô Kế hoạch kiểm kê', 'Link', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Không đổi được', '- Mã là liên kết mở kế hoạch ở tab mới']),
       ('Ngày kiểm kê', 'Textbox', 'Disable', 'dd/mm/yyyy', 'Có', 'Ngày của phiếu', '- Không sửa được; lưu lại thì thành ngày lưu.'),
   ] + FORM_UI[4:19] + FORM_UI[20:],
   ev=[
       ('Mở màn Sửa', 'System',
        'Before:\n– Kiểm tra phạm vi xem, ngoài phạm vi → trang “Không tìm thấy trang”.\n'
        '– Kiểm tra người tạo + Đang tạo, nếu không → chuyển sang màn chi tiết.\nDuring:\n– Nạp hàng theo tồn hiện tại; hàng hết tồn → cảnh báo vàng.\n'
        'After:\n– Điền sẵn dữ liệu; chưa tính là đã thay đổi.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Phiếu phải còn Đang tạo, nếu không → ' + CONFLICT + '.\n– Người bấm phải là người tạo, nếu không → ' + NOPERM + '.\n' + SAVE_DURING + '\n'
        'After:\n– Ghi đè dữ liệu; cập nhật người / ngày cập nhật, Ngày kiểm kê.\n'
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
       ten='Xóa phiếu kiểm kê theo hàng hóa',
       mota='Người tạo xóa hẳn phiếu còn Đang tạo cùng toàn bộ dữ liệu con (kho, công ty thuê, hàng – vị trí – lô – dòng ĐVT, hội đồng, '
            'hàng thừa khác). Kế hoạch nguồn KHÔNG được trả trạng thái: Kế hoạch kiểm kê theo hàng hóa vẫn ở “Đã lập phiếu kiểm kê” '
            '(giữ như hệ thống cũ — đã chốt), nên không lập lại phiếu từ kế hoạch đó được.',
       tacnhan=TN_OWNER,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo.\n3. Phiếu đang Đang tạo.',
       chinh='1. Người dùng bấm Xóa ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống hiện hộp “Xác nhận xóa” với nội dung “Bạn có chắc muốn xóa bản ghi này không?”.\n'
             '3. Người dùng bấm Xóa.\n'
             '4. Hệ thống kiểm lại phiếu còn Đang tạo và đúng người tạo.\n'
             '5. Hệ thống ghi nhận hành động “Xóa” trong lịch sử, xóa phiếu và mọi dữ liệu con.\n'
             '6. Hệ thống hiển thị “Xóa thành công.”; ở danh sách nạp lại, ở chi tiết quay về danh sách.',
       phu='• Bấm Hủy / (x) → đóng hộp, không xóa.\n'
           '• Phiếu vừa bị gửi ở tab khác → ' + CONFLICT + ', không xóa.\n'
           '• Phiếu đã bị xóa ở tab khác → ' + NOTFOUND + '.\n'
           '• Phiếu lập từ kế hoạch → kế hoạch giữ nguyên trạng thái.',
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
       ('Kế hoạch nguồn sau xóa', 'Badge', 'Read-only', 'Theo dữ liệu', '- Giữ nguyên “Đã lập phiếu kiểm kê” (không trả về Đang kiểm).'),
   ],
   ev=[
       ('Bấm Xóa', 'Click', 'Before:\n– Nút chỉ hiện với phiếu Đang tạo của mình.\nDuring:\n– Không gửi máy chủ.\nAfter:\n– Hiện hộp Xác nhận xóa.'),
       ('Bấm Xóa (xác nhận)', 'Click',
        'Before:\n– Kiểm tra phạm vi xem, ngoài phạm vi → ' + NOTFOUND + '.\n'
        '– Phiếu phải còn Đang tạo, nếu không → ' + CONFLICT + '; không phải người tạo → ' + NOPERM + '.\n'
        'During:\n– Xóa trọn gói phiếu và dữ liệu con; lỗi thì không xóa gì.\n' + ERR + '\n'
        'After:\n– Ghi một dòng lịch sử “Xóa”; kế hoạch nguồn giữ nguyên.\n– Hiển thị “Xóa thành công.”; nạp lại / về danh sách.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nDuring:\n– Không gửi máy chủ.\nAfter:\n– Đóng hộp, dữ liệu giữ nguyên.'),
       ('Màn Kế hoạch sau khi xóa', 'System', 'Before:\n– Phiếu lập từ Kế hoạch theo hàng hóa (Đã lập phiếu kiểm kê).\nDuring:\n– Không đổi kế hoạch.\nAfter:\n– Kế hoạch vẫn “Đã lập phiếu kiểm kê”, không còn nút Lập phiếu.'),
   ])

# ------------------------------------------------------------ 2.11 Chi tiết
fr(11, 'Xem chi tiết phiếu kiểm kê',
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu kiểm kê theo hàng hóa',
       mota='Màn hiển thị Thông tin chung (kế hoạch, ngày kiểm kê, kho, công ty thuê kho, ghi chú), File đính kèm (khi đã / đang nhập '
            'kết quả), bảng Hàng hóa kèm ĐVT kiểm kê và kết quả (Thực kiểm, Chênh lệch khác 0 chữ đỏ, Ghi chú), Hàng thừa khác, Hội '
            'đồng kiểm kê và khối Lịch sử. Chân màn có nút theo cờ: Gửi duyệt, Duyệt kết quả, Không duyệt, 3 nút tạo phiếu xử lý, Sửa, '
            'Xóa, In, Xuất Excel, Quay lại.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu trong phạm vi xem, hoặc người dùng đang có việc trên phiếu (Ban kiểm soát '
                'với phiếu Chờ KT duyệt, người xử lý với phiếu Chờ / Đang xử lý).',
       chinh='1. Người dùng bấm Số phiếu ở danh sách (hoặc bấm thông báo / liên kết ở màn khác).\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết phiếu kiểm kê theo hàng hóa: <số phiếu>”.\n'
             '4. Hệ thống hiển thị các khối và nút theo cờ của phiếu; khối Lịch sử thu gọn, có số mốc.',
       phu='• Ngoài phạm vi / không tồn tại → trang “Không tìm thấy trang”.\n'
           '• Phiếu Đang tạo của người khác → coi như ngoài phạm vi.\n'
           '• Phiếu chưa nhập kết quả → không có cột Thực kiểm / Chênh lệch / Ghi chú, khối File đính kèm và Hàng thừa khác.\n'
           '• Đã có kết quả nhưng không có file → khối File đính kèm ghi “Không có file đính kèm.”.\n'
           '• Bấm Quay lại → về đúng lối danh sách đã vào, khôi phục bộ lọc (trong 10 phút).',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết phiếu kiểm kê Hoàn thành'),
   extra=[(shot('17b_detail_full'), 'Chi tiết đầy đủ: bảng kết quả, hàng thừa khác, hội đồng, khối Lịch sử')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị', '- “Chi tiết phiếu kiểm kê theo hàng hóa: <số phiếu>” (không kèm nhãn trạng thái).'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: người tạo và giờ tạo.'),
       ('Kế hoạch kiểm kê', 'Link', 'Read-only', '–', 'Theo dữ liệu', '- Mã kế hoạch, bấm → tab mới; ô trống khóa nếu lập tay.'),
       ('Ngày kiểm kê, Kho, Công ty thuê kho, Ghi chú', 'Textbox', 'Disable', '–', 'Theo dữ liệu', '- Ô khóa nền xám.'),
       ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Ẩn khi chưa có kết quả',
        ['- Tên file (bấm để xem / tải), dung lượng', '- Chỉ sửa được ở bước Cập nhật kết quả (mục 2.12)']),
       ('Bảng Hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Cột như màn Tạo, ĐVT kiểm kê là chữ', '- Khi có kết quả: thêm Thực kiểm, Chênh lệch (khác 0 chữ đỏ), Ghi chú',
         '- Cột số / ĐVT co theo nội dung']),
       ('Bảng Hàng thừa khác', 'Table/Grid', 'Read-only', '–', 'Hiện khi có kết quả',
        ['- STT, Tên hàng, Model, Mã hàng, ĐVT, SL tồn, Vị trí, Thực kiểm', '- Không có dòng → “Không có dữ liệu”']),
       ('Bảng Hội đồng kiểm kê', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- STT, Thành viên, Chức vụ (ô khóa).'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', ['- Số mốc cạnh tiêu đề', '- Nút Xem lịch sử / Thu gọn, Làm mới, Bộ lọc']),
       ('Nút Gửi duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Đang kiểm / Không duyệt + người tạo (mục 2.12).'),
       ('Nút Duyệt kết quả, Không duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Chờ KT duyệt + Q2 (mục 2.13, 2.14), đứng liền nhau.'),
       ('Nút Tạo phiếu điều chuyển vị trí / nhập kho điều chuyển / xuất kho điều chuyển', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Chờ / Đang xử lý + Q3 (mục 2.15).'),
       ('Nút Sửa, Xóa', 'Button', 'Enable / Ẩn', '–', 'Ẩn khi không đủ điều kiện', '- Phiếu Đang tạo của mình.'),
       ('Nút In, Xuất Excel', 'Button', 'Enable', '–', 'Hiển thị', '- Ở cuối dãy nút (mục 2.16, 2.17).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về đúng lối danh sách đã vào.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → trang “Không tìm thấy trang”.\n'
        'During:\n– Lấy dữ liệu phiếu (ảnh chụp đã lưu), cờ nút.\nAfter:\n– Hiển thị màn, nút theo cờ; chưa tính là đã thay đổi.'),
       ('Bấm Xem lịch sử', 'Click', 'Before:\n– Khối đang thu gọn.\nDuring:\n– Nạp các mốc.\nAfter:\n– Mở rộng khối, hiện các mốc (mục 2.18).'),
       ('Bấm mã kế hoạch', 'Click', 'Before:\n– Phiếu có kế hoạch.\nDuring:\n– Không đổi dữ liệu.\nAfter:\n– Mở chi tiết kế hoạch ở tab mới.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– Đang cập nhật kết quả mà có thay đổi → hộp “Thông tin chưa lưu”.\nDuring:\n– Xác định lối vào.\nAfter:\n– Về danh sách, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.12 Cập nhật kết quả
fr(12, 'Cập nhật kết quả kiểm kê (Gửi duyệt)', usecase=('FR-12', 'Cập nhật kết quả (Gửi duyệt)', 'crud', A_LP),
   rule=('- Màn Chỉnh sửa, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Nhập kết quả thực kiểm và gửi duyệt',
       mota='Ở màn chi tiết của phiếu Đang kiểm / Không duyệt, người tạo nhập Thực kiểm cho từng dòng ĐVT kiểm kê (lần đầu mặc định '
            '= SL dòng), Ghi chú dòng, khai Hàng thừa khác (hàng có mã hoặc hàng mới + ĐVT, từng vị trí + Thực kiểm), đính kèm file '
            'kết quả rồi bấm Gửi duyệt: phiếu chuyển Chờ KT duyệt và người có quyền “%s” cùng công ty nhận thông báo.' % Q4,
       tacnhan='Người dùng có quyền thực hiện chức năng: người tạo phiếu, phiếu đang ở trạng thái Đang kiểm hoặc Không duyệt.',
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo phiếu.\n3. Phiếu đang Đang kiểm / Không duyệt.',
       chinh='1. Người tạo bấm Cập nhật kết quả ở danh sách hoặc mở chi tiết phiếu.\n'
             '2. Hệ thống hiện thêm cột Thực kiểm *, Chênh lệch, Ghi chú; khối Hàng thừa khác (nút Thêm dòng) và khối File đính kèm.\n'
             '3. Người dùng sửa Thực kiểm; Chênh lệch tự tính = Thực kiểm − SL (khác 0 chữ đỏ); nhập Ghi chú nếu cần.\n'
             '4. Hàng thừa khác: bấm Thêm dòng, gõ tên hàng mới + chọn ĐVT, hoặc bấm kính lúp chọn hàng có mã (nạp vị trí có tồn); '
             'chọn Vị trí (Thêm vị trí nếu nhiều), nhập Thực kiểm.\n'
             '5. Người dùng đính kèm file (bắt buộc nếu phiếu chưa có file) rồi bấm Gửi duyệt.\n'
             '6. Hệ thống kiểm đủ mọi dòng, ghi Thực kiểm, Chênh lệch (máy chủ tự tính), Ghi chú; ghi lại Hàng thừa khác; nối file mới.\n'
             '7. Hệ thống chuyển phiếu Chờ KT duyệt, ghi lịch sử “Thay đổi thông tin” và “Thay đổi trạng thái”.\n'
             '8. Hệ thống gửi thông báo “Chờ duyệt” (Người nhập kết quả, Ngày kiểm kê, Kho, Kế hoạch, Ghi chú) cho người có quyền “%s” '
             'cùng công ty người thao tác.\n'
             '9. Hệ thống hiển thị “Gửi duyệt thành công.” và về danh sách.' % Q4,
       phu='• Thiếu Thực kiểm → ' + REQ + ' dưới ô; vượt 999,999,999 → “Không hợp lệ”.\n'
           '• Hàng thừa khác thiếu tên / ĐVT / vị trí / Thực kiểm → ' + REQ + '; vị trí ngoài kho phiếu → “Không thuộc kho của phiếu.”.\n'
           '• Phiếu chưa có file và không đính file → ' + REQ + ' ở khối File đính kèm.\n'
           '• Lỗi hiện cùng lúc, thông báo ' + MISS + ', cuộn tới ô lỗi đầu tiên.\n'
           '• File sai loại → “Chỉ nhận file pdf, png, jpg, jpeg, doc, docx, xls, xlsx”; quá 20MB → “Dung lượng tối đa 20MB”.\n'
           '• Phiếu đã đổi trạng thái → ' + CONFLICT + '.\n'
           '• Rời màn khi đã nhập → hộp “Thông tin chưa lưu”.',
       dacbiet='Gửi thẳng, không hộp xác nhận (giữ như hệ thống cũ); nút khóa trong lúc gửi. Thực kiểm chỉ nhận số, tối đa 2 chữ số '
               'thập phân, không âm. Xóa file đã lưu chỉ được khi phiếu còn ở bước nhập kết quả. Lỗi gửi thông báo không làm hỏng việc lưu.'),
   layout=dict(menu=MENU + ' => Cập nhật kết quả', shot=shot('14_result'), shot_caption='Màn chi tiết phiếu Đang kiểm ở bước Cập nhật kết quả'),
   extra=[(shot('14b_result_validate_full'), 'Lỗi bắt buộc khi Gửi duyệt thiếu Thực kiểm / file / dòng Hàng thừa khác chưa đủ')],
   ui=[
       ('Nút Cập nhật kết quả trên dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Đang kiểm / Không duyệt + người tạo; bấm → mở chi tiết.'),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'pdf, png, jpg, jpeg, doc, docx, xls, xlsx; ≤ 20MB', 'Có khi chưa có file', 'File đã lưu',
        ['- Chọn file, tải lên ngay', '- Mỗi file: tên, dung lượng, nút thay / xóa', '- Lỗi: ' + REQ]),
       ('Cột Thực kiểm', 'Textbox', 'Enable', '0 – 999,999,999, tối đa 2 số lẻ', 'Có', '= SL (lần đầu)',
        ['- Gợi ý “Nhập thực kiểm”', '- Lỗi: ' + REQ + ' / “Không hợp lệ”']),
       ('Cột Chênh lệch', 'Label', 'Read-only', 'Số', '–', '0', ['- = Thực kiểm − SL', '- Khác 0: chữ đỏ']),
       ('Cột Ghi chú', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', ['- Gợi ý “Nhập ghi chú”', '- Lỗi: “Vui lòng nhập tối đa 255 ký tự.”']),
       ('Khối Hàng thừa khác', 'Table/Grid', 'Enable', '–', 'Không', '“Không có dữ liệu”',
        ['- Cột STT, Tên hàng *, Model, Mã hàng, ĐVT *, SL tồn, Vị trí *, Thực kiểm *, Hành động', '- Nút Thêm dòng ở góc phải']),
       ('Ô Tên hàng (hàng mới)', 'Textbox', 'Enable', '1–255 ký tự', 'Có', 'Trống', ['- Gợi ý “Nhập tên hàng”', '- Nút kính lúp “Chọn hàng hóa có mã”']),
       ('Ô ĐVT (hàng mới)', 'Dropdown', 'Enable', 'Danh mục ĐVT đang dùng', 'Có', 'Trống', '- Hàng có mã: ĐVT cơ sở, chỉ đọc.'),
       ('Ô Vị trí', 'Dropdown', 'Enable', 'Vị trí của các kho phiếu', 'Có', 'Trống', ['- Nút + “Thêm vị trí” ở vị trí đầu', '- Thùng rác “Xóa vị trí” ở các vị trí sau']),
       ('Ô Thực kiểm hàng thừa', 'Textbox', 'Enable', '0 – 999,999,999', 'Có', 'Trống', '- Lỗi: ' + REQ + ' / “Không hợp lệ”.'),
       ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Rê chuột: “Lưu kết quả kiểm kê và gửi Kế toán kho duyệt”', '- Khóa trong lúc gửi']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Gửi duyệt thành công.”', '- ' + MISS + ' / ' + INVALID, '- ' + CONFLICT, '- “Đã có lỗi xảy ra.”']),
       ('Thông báo cho Kế toán kho', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Hành động “Chờ duyệt” kèm số phiếu', '- Ghi chú: Người nhập kết quả, Ngày kiểm kê, Kho, Kế hoạch, Ghi chú', '- Bấm → mở chi tiết phiếu']),
   ],
   ev=[
       ('Gõ Thực kiểm', 'Change',
        'Before:\n– Chỉ nhận số, tối đa 2 số lẻ.\nDuring:\n– Xóa lỗi của ô.\nAfter:\n– Tính lại Chênh lệch, tô đỏ khi khác 0.'),
       ('Thêm dòng / chọn hàng có mã ở Hàng thừa khác', 'Click',
        'Before:\n– Đang ở bước nhập kết quả.\nDuring:\n– Chọn hàng có mã: lấy vị trí có tồn của hàng; hàng đã có ở dòng khác → “Hàng hóa đã được chọn.”.\n'
        'After:\n– Thêm dòng hàng mới / điền tên, mã, model, ĐVT, vị trí của hàng có mã, báo “Thêm thành công.”.'),
       ('Bấm Gửi duyệt', 'Click',
        'Before:\n– Form kiểm: Thực kiểm trống / quá lớn, hàng thừa thiếu tên – ĐVT – vị trí – Thực kiểm, thiếu file → lỗi dưới ô, ' + MISS + ', dừng.\n'
        '– Phiếu phải Đang kiểm / Không duyệt, nếu không → ' + CONFLICT + '; không phải người tạo → ' + NOPERM + '.\n'
        'During:\n– Máy chủ kiểm lại: dòng không thuộc phiếu → “Không thuộc phiếu này. Vui lòng tải lại trang.”; thiếu dòng → “Vui lòng nhập kết quả '
        'cho tất cả các dòng. Vui lòng tải lại trang.”; vị trí hàng thừa ngoài kho → “Không thuộc kho của phiếu.”.\n' + ERR + '\n'
        'After:\n– Ghi kết quả, hàng thừa khác, nối file; phiếu Chờ KT duyệt.\n– Ghi lịch sử “Thay đổi thông tin” + “Thay đổi trạng thái”.\n'
        '– Gửi thông báo “Chờ duyệt” cho người có quyền “%s” cùng công ty.\n– Hiển thị “Gửi duyệt thành công.”, về danh sách.' % Q4),
       ('Xóa file đã lưu', 'Click',
        'Before:\n– Phiếu còn ở bước nhập kết quả.\nDuring:\n– File không thuộc phiếu → “File không nằm trong phiếu này”.\n'
        'After:\n– Xóa file, ghi lịch sử “Thay đổi thông tin”, “Xóa file thành công”.'),
       ('Bấm Quay lại', 'Click', 'Before:\n– So kết quả, hàng thừa, file với lúc mở.\nDuring:\n– Có thay đổi → hộp “Thông tin chưa lưu”.\nAfter:\n– Thoát: về danh sách không lưu; Ở lại: giữ màn.'),
   ])

# ------------------------------------------------------------ 2.13 Duyệt
fr(13, 'Duyệt kết quả kiểm kê', usecase=('FR-13', 'Duyệt kết quả', 'action', A_BKS),
   rule=('- Màn Xem chi tiết, Thông báo và Phân quyền.', 'detail'),
   intro=dict(
       ten='Ban kiểm soát duyệt kết quả kiểm kê',
       mota='Ở phiếu Chờ KT duyệt, người có quyền “%s” bấm Duyệt kết quả, nhập ghi chú (tùy chọn) trong popup rồi xác nhận. Có dòng '
            'chênh lệch khác 0 → phiếu Chờ xử lý và người có quyền “%s” cùng công ty nhận thông báo; không chênh lệch → phiếu Hoàn '
            'thành. Ban kiểm soát vào từ menu Tài chính › Kiểm kê › Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả.' % (Q2, Q3),
       tacnhan='Người dùng có quyền thực hiện chức năng: %s.' % Q2,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có quyền “%s”.\n3. Phiếu đang Chờ KT duyệt.' % Q2,
       chinh='1. Người dùng bấm Duyệt trên dòng (mở chi tiết) hoặc mở chi tiết phiếu từ thông báo.\n'
             '2. Người dùng bấm Duyệt kết quả ở chân màn chi tiết.\n'
             '3. Hệ thống mở popup “Duyệt kết quả kiểm kê” (Phiếu: <số phiếu>) với ô Ghi chú duyệt.\n'
             '4. Người dùng nhập ghi chú (không bắt buộc) và bấm Duyệt kết quả.\n'
             '5. Hệ thống kiểm lại trạng thái + quyền, ghi người duyệt, ngày duyệt, ghi chú duyệt.\n'
             '6. Có dòng chênh lệch ≠ 0 → phiếu Chờ xử lý, gửi thông báo “Đã duyệt” (Người duyệt, “Có chênh lệch cần xử lý”, Ngày kiểm '
             'kê, Kho, Kế hoạch, Ghi chú duyệt) cho người có quyền “%s” cùng công ty; không → phiếu Hoàn thành.\n'
             '7. Hệ thống ghi lịch sử “Thay đổi trạng thái” (cũ → mới, ghi chú duyệt), hiển thị “Duyệt thành công.”, về danh sách.' % Q3,
       phu='• Bấm Hủy / (x) ở popup → đóng popup, không duyệt.\n'
           '• Phiếu đã được người khác duyệt / không duyệt → ' + CONFLICT + '.\n'
           '• Không có quyền → nút không hiện; vẫn gửi → ' + NOPERM + '.\n'
           '• Ghi chú duyệt quá 5000 ký tự → “Vui lòng nhập tối đa 5000 ký tự.”.',
       dacbiet='Popup chính là bước xác nhận (không hỏi thêm). Nút khóa trong lúc gửi. Ghi chú duyệt không hiện trên màn chi tiết, chỉ '
               'nằm ở Lịch sử, bản in và file Excel (“Nhận xét, đánh giá”). Duyệt không cập nhật trạng thái kế hoạch.'),
   layout=dict(entries=[
       (MENU + ' => Duyệt kết quả', 'Từ danh sách phân hệ Kho, nút Duyệt mở chi tiết phiếu Chờ KT duyệt.'),
       (MENU_TC + ' => Duyệt kết quả', 'Lối Ban kiểm soát: danh sách chỉ phiếu Chờ KT duyệt.')],
       shot=shot('15_approve'), shot_caption='Popup Duyệt kết quả kiểm kê'),
   extra=[(shot('15_wait_detail'), 'Màn chi tiết phiếu Chờ KT duyệt: nút Duyệt kết quả, Không duyệt')],
   ui=[
       ('Nút Duyệt trên dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Chờ KT duyệt + Q2; bấm → mở chi tiết.'),
       ('Nút Duyệt kết quả ở chi tiết', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Màu chính, biểu tượng dấu tích.'),
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', ['- “Duyệt kết quả kiểm kê”', '- Dòng phụ “Phiếu: <số phiếu>”']),
       ('Ô Ghi chú duyệt', 'Textarea', 'Enable', '0–5000 ký tự', 'Không', 'Trống', '- Gợi ý “Nhập ghi chú duyệt”.'),
       ('Nút Duyệt kết quả trong popup', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Xác nhận duyệt; khóa trong lúc gửi.'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống Hủy.'),
       ('Cột Người duyệt, Ngày duyệt', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Cập nhật sau khi duyệt.'),
       ('Nhãn trạng thái sau duyệt', 'Badge', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Có chênh lệch: Chờ xử lý (vàng)', '- Không chênh: Hoàn thành (xanh lá)']),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Duyệt thành công.”'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + CONFLICT, '- ' + NOPERM]),
       ('Thông báo cho người xử lý', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Hành động “Đã duyệt” kèm số phiếu', '- Chỉ khi có chênh lệch', '- Bấm → mở chi tiết phiếu']),
   ],
   ev=[
       ('Bấm Duyệt kết quả (chi tiết)', 'Click', 'Before:\n– Nút chỉ hiện khi Chờ KT duyệt + quyền “%s”.\nDuring:\n– Xóa lỗi ghi chú cũ.\nAfter:\n– Mở popup Duyệt kết quả kiểm kê.' % Q2),
       ('Bấm Duyệt kết quả (popup)', 'Click',
        'Before:\n– Kiểm tra quyền “%s”; không có → %s.\n– Phiếu phải Chờ KT duyệt, nếu không → %s.\n' % (Q2, NOPERM, CONFLICT) +
        'During:\n– Ghi chú > 5000 ký tự → “Vui lòng nhập tối đa 5000 ký tự.”.\n' + ERR + '\n'
        'After:\n– Ghi người / ngày / ghi chú duyệt; Chờ xử lý (có chênh lệch) hoặc Hoàn thành.\n'
        '– Ghi lịch sử; có chênh lệch → gửi thông báo “Đã duyệt” cho người có quyền “%s”.\n'
        '– Hiển thị “Duyệt thành công.”, về danh sách.' % Q3),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nDuring:\n– Không gửi máy chủ.\nAfter:\n– Đóng popup, phiếu giữ Chờ KT duyệt.'),
       ('Bấm thông báo (người xử lý)', 'Click', 'Before:\n– Người nhận có quyền “%s”.\nDuring:\n– Kiểm phạm vi (người xử lý được xem).\nAfter:\n– Mở chi tiết phiếu Chờ xử lý (mục 2.15).' % Q3),
   ])

# ------------------------------------------------------------ 2.14 Không duyệt
fr(14, 'Không duyệt kết quả kiểm kê', usecase=('FR-14', 'Không duyệt', 'action', A_BKS),
   rule=('- Màn Xem chi tiết, Thông báo và Phân quyền.', 'detail'),
   intro=dict(
       ten='Ban kiểm soát không duyệt kết quả kiểm kê',
       mota='Ở phiếu Chờ KT duyệt, người có quyền “%s” bấm Không duyệt, nhập lý do (bắt buộc) trong popup rồi xác nhận: phiếu chuyển '
            'trạng thái Không duyệt để người tạo nhập lại kết quả và Gửi duyệt lại; người tạo nhận thông báo kèm lý do.' % Q2,
       tacnhan='Người dùng có quyền thực hiện chức năng: %s.' % Q2,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có quyền “%s”.\n3. Phiếu đang Chờ KT duyệt.' % Q2,
       chinh='1. Người dùng mở chi tiết phiếu, bấm Không duyệt (nút đỏ, ngay sau Duyệt kết quả).\n'
             '2. Hệ thống mở popup “Không duyệt kết quả kiểm kê” (Phiếu: <số phiếu>) với ô Ghi chú duyệt * bắt buộc.\n'
             '3. Người dùng nhập lý do và bấm Không duyệt.\n'
             '4. Hệ thống kiểm lại trạng thái + quyền, ghi người duyệt + lý do, đưa phiếu về Không duyệt (kết quả cũ giữ để sửa).\n'
             '5. Hệ thống ghi lịch sử “Từ chối” (Trạng thái Chờ KT duyệt → Không duyệt, lý do).\n'
             '6. Hệ thống gửi thông báo “Từ chối” (Người từ chối, Lý do) cho người tạo phiếu.\n'
             '7. Hệ thống hiển thị “Không duyệt thành công.”, về danh sách.',
       phu='• Bỏ trống lý do → lỗi đỏ “Vui lòng nhập lý do không duyệt” dưới ô, không gửi (máy chủ: ' + REQ + ').\n'
           '• Lý do quá 5000 ký tự → “Vui lòng nhập tối đa 5000 ký tự.”.\n'
           '• Bấm Hủy / (x) → đóng popup, không đổi gì.\n'
           '• Phiếu đã được duyệt / không duyệt ở tab khác → ' + CONFLICT + '.',
       dacbiet='Popup nhập lý do là bước xác nhận. Lý do được bỏ khoảng trắng đầu / cuối; chỉ khoảng trắng coi như trống. Sau Không '
               'duyệt, nút Cập nhật kết quả hiện lại cho người tạo, Thực kiểm giữ giá trị đã nhập.'),
   layout=dict(menu=MENU + ' => Không duyệt', shot=shot('15b_reject'), shot_caption='Popup Không duyệt kết quả kiểm kê khi bỏ trống lý do',
               note='Popup mở trên màn chi tiết phiếu Chờ KT duyệt theo đường dẫn ở trên.'),
   ui=[
       ('Nút Không duyệt ở chi tiết', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Nút đỏ, biểu tượng dấu x tròn.'),
       ('Tiêu đề popup', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', ['- “Không duyệt kết quả kiểm kê”', '- Dòng phụ “Phiếu: <số phiếu>”']),
       ('Ô Ghi chú duyệt', 'Textarea', 'Enable', '1–5000 ký tự', 'Có', 'Trống',
        ['- Gợi ý “Nhập lý do không duyệt”', '- Lỗi: “Vui lòng nhập lý do không duyệt” (viền đỏ)']),
       ('Nút Không duyệt trong popup', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Nút đỏ; khóa trong lúc gửi.'),
       ('Nút Hủy', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng popup.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống Hủy.'),
       ('Nhãn trạng thái sau không duyệt', 'Badge', 'Read-only', '–', '–', 'Không duyệt', '- Nhãn đỏ “Không duyệt”.'),
       ('Nút Cập nhật kết quả sau không duyệt', 'Icon Button', 'Read-only', '–', '–', 'Hiển thị với người tạo', '- Người tạo nhập lại kết quả.'),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Không duyệt thành công.”'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- ' + CONFLICT, '- ' + NOPERM]),
       ('Thông báo cho người tạo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Hành động “Từ chối” kèm số phiếu', '- Ghi chú: Người từ chối, Lý do', '- Bấm → mở chi tiết phiếu']),
   ],
   ev=[
       ('Bấm Không duyệt (chi tiết)', 'Click', 'Before:\n– Nút chỉ hiện khi Chờ KT duyệt + quyền “%s”.\nDuring:\n– Xóa lỗi cũ.\nAfter:\n– Mở popup Không duyệt.' % Q2),
       ('Bấm Không duyệt (popup)', 'Click',
        'Before:\n– Lý do trống → “Vui lòng nhập lý do không duyệt”, dừng xử lý.\n– Kiểm tra quyền “%s”; không có → %s.\n'
        '– Phiếu phải Chờ KT duyệt, nếu không → %s.\n' % (Q2, NOPERM, CONFLICT) +
        'During:\n– Lý do > 5000 ký tự → “Vui lòng nhập tối đa 5000 ký tự.”.\n' + ERR + '\n'
        'After:\n– Phiếu Không duyệt, ghi lý do.\n– Ghi lịch sử “Từ chối”.\n– Gửi thông báo “Từ chối” cho người tạo.\n'
        '– Hiển thị “Không duyệt thành công.”, về danh sách.'),
       ('Gõ lý do sau khi báo lỗi', 'Change', 'Before:\n– Đang có lỗi đỏ.\nDuring:\n– Kiểm lại ô.\nAfter:\n– Lỗi biến mất khi ô có chữ.'),
       ('Bấm Hủy / (x)', 'Click', 'Before:\n– Không hỏi thêm.\nDuring:\n– Không gửi máy chủ.\nAfter:\n– Đóng popup, phiếu giữ Chờ KT duyệt.'),
   ])

# ------------------------------------------------------------ 2.15 Xử lý
fr(15, 'Xử lý phiếu (tạo phiếu điều chuyển / nhập / xuất điều chỉnh)', usecase=('FR-15', 'Xử lý phiếu', 'action', A_XL),
   rule=('- Màn Xem chi tiết, Thông báo và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xử lý chênh lệch của phiếu Chờ xử lý / Đang xử lý',
       mota='Người có quyền “%s” mở phiếu Chờ xử lý / Đang xử lý; tùy chênh lệch theo từng hàng, chân màn hiện tối đa 3 nút mở màn tạo '
            'phiếu tương ứng (đã nạp sẵn dữ liệu từ phiếu kiểm kê): Tạo phiếu điều chuyển vị trí (hàng tổng chênh = 0 nhưng thiếu ở '
            'vị trí này, thừa ở vị trí khác), Tạo phiếu nhập kho điều chuyển (hàng tổng chênh ≠ 0 có dòng thừa, cần thêm quyền “%s”), '
            'Tạo phiếu xuất kho điều chuyển (hàng tổng chênh ≠ 0 có dòng thiếu). Mỗi loại chỉ lập 1 phiếu; các phiếu đó ghi ngược số '
            'đã xử lý và đưa phiếu kiểm kê sang Đang xử lý / Hoàn thành.' % (Q3, Q5),
       tacnhan='Người dùng có quyền thực hiện chức năng: %s.' % Q3,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Có quyền “%s”.\n3. Phiếu đang Chờ xử lý / Đang xử lý.' % Q3,
       chinh='1. Người dùng bấm Xử lý trên dòng, hoặc mở chi tiết phiếu từ thông báo “Đã duyệt”.\n'
             '2. Hệ thống hiển thị bảng kết quả và các nút xử lý theo điều kiện.\n'
             '3. Người dùng bấm Tạo phiếu điều chuyển vị trí → mở màn Tạo phiếu điều chuyển vị trí (phân hệ Kho) đã nạp kho đầu tiên '
             'của phiếu và các dòng thiếu còn lại.\n'
             '4. Hoặc bấm Tạo phiếu nhập kho điều chuyển / Tạo phiếu xuất kho điều chuyển → mở màn tạo Phiếu nhập kho / xuất kho điều '
             'chỉnh kiểm kê đã nạp các dòng thừa / thiếu.\n'
             '5. Lưu phiếu xử lý ở màn đó → phiếu kiểm kê chuyển Đang xử lý (ghi “Thay đổi trạng thái” vào lịch sử phiếu); xử lý hết '
             'chênh lệch → Hoàn thành.',
       phu='• Đã có phiếu xử lý cùng loại lập từ phiếu này → nút loại đó ẩn.\n'
           '• Không có quyền “%s” → không có nút Tạo phiếu nhập kho điều chuyển.\n' % Q5 +
           '• Phiếu đã Hoàn thành → không còn nút Xử lý.\n'
           '• Người dùng không có quyền “%s” → không có nút Xử lý, không thấy nút ở chi tiết.' % Q3,
       dacbiet='Màn này chỉ điều hướng, không tự ghi dữ liệu xử lý. Dòng cần xử lý: |Chênh lệch| chưa bằng số đã xử lý và chưa đánh '
               'dấu xong. Trạng thái Đang xử lý / Hoàn thành do các màn phiếu xử lý ghi.'),
   layout=dict(menu=MENU + ' => Xử lý', shot=shot('16_handle'), shot_caption='Màn chi tiết phiếu Chờ xử lý với nút xử lý'),
   extra=[(shot('16b_handle2'), 'Một phiếu Chờ xử lý khác (nút xử lý theo loại chênh lệch)')],
   ui=[
       ('Nút Xử lý trên dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện', '- Chờ / Đang xử lý + Q3; bấm → chi tiết.'),
       ('Nút Tạo phiếu điều chuyển vị trí', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện',
        ['- Rê chuột: “Tạo phiếu điều chuyển vị trí cho các dòng chênh lệch”', '- Mở màn Tạo phiếu điều chuyển vị trí']),
       ('Nút Tạo phiếu nhập kho điều chuyển', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện',
        ['- Rê chuột: “Tạo phiếu nhập kho điều chỉnh kiểm kê cho các dòng thừa”', '- Cần Q3 + Q5']),
       ('Nút Tạo phiếu xuất kho điều chuyển', 'Button', 'Enable / Ẩn', '–', '–', 'Ẩn khi không đủ điều kiện',
        '- Rê chuột: “Tạo phiếu xuất kho điều chỉnh kiểm kê cho các dòng thiếu”.'),
       ('Cột Chênh lệch', 'Label', 'Read-only', '–', '–', 'Theo dữ liệu', '- Dương = thừa, âm = thiếu; khác 0 chữ đỏ.'),
       ('Nhãn trạng thái', 'Badge', 'Read-only', '–', '–', 'Chờ xử lý', '- → Đang xử lý khi lập phiếu xử lý; → Hoàn thành khi xử lý hết.'),
       ('Màn Tạo phiếu điều chuyển vị trí', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Kho đầu tiên của phiếu, các dòng thiếu (SL = |chênh| − đã xử lý).'),
       ('Màn Tạo phiếu nhập / xuất kho điều chỉnh', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Nạp phiếu kiểm kê nguồn và các dòng thừa / thiếu.'),
       ('Lịch sử phiếu kiểm kê', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Mốc “Thay đổi trạng thái” khi phiếu xử lý được lưu.'),
       ('Thông báo trước đó', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Đã duyệt … Có chênh lệch cần xử lý” gửi người có Q3.'),
       ('Nút In, Xuất Excel, Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Như mục 2.11.'),
   ],
   ev=[
       ('Mở chi tiết phiếu cần xử lý', 'System',
        'Before:\n– Người có quyền “%s” xem được phiếu Chờ / Đang xử lý dù ngoài phạm vi.\nDuring:\n– Tính các dòng còn cần xử lý theo từng hàng.\n'
        'After:\n– Hiện nút xử lý đúng điều kiện.' % Q3),
       ('Bấm Tạo phiếu điều chuyển vị trí', 'Click',
        'Before:\n– Nút chỉ hiện khi còn hàng tổng chênh = 0 có dòng thiếu và chưa có phiếu điều chuyển từ phiếu này.\nDuring:\n– Không ghi dữ liệu.\n'
        'After:\n– Mở màn Tạo phiếu điều chuyển vị trí (phân hệ Kho) đã nạp dữ liệu.'),
       ('Bấm Tạo phiếu nhập kho điều chuyển', 'Click',
        'Before:\n– Có Q3 + quyền “%s”; còn dòng thừa; chưa có phiếu nhập kho điều chỉnh.\nDuring:\n– Không ghi dữ liệu.\nAfter:\n– Mở màn tạo Phiếu nhập kho điều chỉnh kiểm kê.' % Q5),
       ('Bấm Tạo phiếu xuất kho điều chuyển', 'Click',
        'Before:\n– Có Q3; còn dòng thiếu; chưa có phiếu xuất kho điều chỉnh.\nDuring:\n– Không ghi dữ liệu.\nAfter:\n– Mở màn tạo Phiếu xuất kho điều chỉnh kiểm kê.'),
       ('Phiếu xử lý được lưu ở màn khác', 'System',
        'Before:\n– Phiếu xử lý lập từ phiếu này.\nDuring:\n– Cộng số đã xử lý từng dòng.\nAfter:\n– Phiếu kiểm kê Đang xử lý; hết dòng cần xử lý → Hoàn thành.'),
   ])

# ------------------------------------------------------------ 2.16 In
fr(16, 'In phiếu và in danh sách', usecase=('FR-16', 'In phiếu / In danh sách', 'io', A_LP),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu kiểm kê / In danh sách phiếu',
       mota='Xem trước và in một phiếu (mẫu “Phiếu kiểm kê theo mặt hàng”: số phiếu, ngày kiểm kê, kho, ghi chú, bảng chi tiết kèm '
            'Thực kiểm và Ghi chú, nhận xét đánh giá, khối ký) hoặc in danh sách theo bộ lọc đang áp (mẫu “Danh sách phiếu kiểm kê '
            'theo hàng hóa”). Bản in mở trong cửa sổ trên màn đang đứng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm In ở cột Hành động / màn chi tiết (in phiếu), hoặc In danh sách trên bảng.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ xem trước, hiện “Đang tải dữ liệu in…” trong lúc dựng.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Danh sách quá 2.000 dòng → không dựng bản in, ẩn nút In, hiện dòng nhắc thu hẹp bộ lọc.\n'
           '• Không có dòng nào → “Không có dữ liệu để in”.\n'
           '• Ngoài phạm vi → ' + NOTFOUND + '.\n'
           '• Thiếu mẫu in → “Thiếu mẫu in phiếu kiểm kê theo hàng hóa.” / “Thiếu mẫu in danh sách phiếu kiểm kê theo hàng hóa.”.\n'
           '• Bấm (x) → đóng cửa sổ.',
       dacbiet='Logo / letterhead bản in phiếu lấy theo công ty ghi trên phiếu; bản in danh sách theo công ty người in, Người lập = '
               'người in. Ngày ở bản in danh sách kèm giờ. Thực kiểm chỉ in khi phiếu đã có kết quả.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu kiểm kê theo hàng hóa',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   extra=[(shot('19_printlist'), 'Cửa sổ Xem trước danh sách phiếu kiểm kê theo hàng hóa')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–',
        ['- In phiếu: “Xem trước phiếu kiểm kê theo hàng hóa <số phiếu>”', '- In danh sách: “Xem trước danh sách phiếu kiểm kê theo hàng hóa”']),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', ['- Cạnh tiêu đề; bấm → hộp thoại in', '- Ẩn khi vượt mức in']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Đang tải dữ liệu in…”.'),
       ('Đầu bản in phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Letterhead công ty của phiếu', '- “PHIẾU KIỂM KÊ THEO MẶT HÀNG”, Số phiếu, Ngày kiểm kê', '- Kho, Ghi chú']),
       ('Bảng chi tiết bản in phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Tên hàng, Mã hàng, Vị trí, Công ty, Lô, SL tồn, ĐVT kiểm kê, Thực kiểm, Ghi chú', '- Gộp ô theo hàng / vị trí / lô']),
       ('Nhận xét, đánh giá', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Ghi chú duyệt / lý do không duyệt.'),
       ('Chỗ ký phiếu', 'Label', 'Read-only', '–', 'Hiển thị', '- Hội đồng kiểm kê, Trưởng bộ phận kho.'),
       ('Bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        ['- Cột: STT, Số phiếu, Kế hoạch KK, Ngày kiểm kê, Kho, Người tạo, Người duyệt, Ngày duyệt, Trạng thái',
         '- Khối ký: Ngày … Tháng … Năm …, Người lập']),
       ('Dòng nhắc vượt trần in', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- “Danh sách có N dòng, vượt mức in tối đa …”.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', ['- “Không tải được dữ liệu in”', '- “Không có dữ liệu để in”']),
   ],
   ev=[
       ('Bấm In (phiếu)', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → ' + NOTFOUND + '.\n'
        'During:\n– Dựng bản in theo mẫu; thiếu mẫu → “Thiếu mẫu in phiếu kiểm kê theo hàng hóa.”.\nAfter:\n– Hiện bản xem trước.'),
       ('Bấm In danh sách', 'Click',
        'Before:\n– Lấy bộ lọc đang áp + lối vào.\nDuring:\n– Vượt mức in → dòng nhắc, ẩn bản in và nút In.\nAfter:\n– Hiện bản xem trước.'),
       ('Bấm In trong cửa sổ', 'Click', 'Before:\n– Bản in đã dựng.\nDuring:\n– Không ghi dữ liệu.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không ghi dữ liệu.\nAfter:\n– Đóng cửa sổ, giữ nguyên màn đang đứng.'),
   ])

# ------------------------------------------------------------ 2.17 Xuất Excel
fr(17, 'Xuất Excel', usecase=('FR-17', 'Xuất Excel', 'io', A_LP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách / xuất 1 phiếu ra Excel',
       mota='(1) Xuất danh sách: chọn trường và thứ tự rồi xuất toàn bộ phiếu khớp bộ lọc (không phân trang). (2) Xuất 1 phiếu: nút '
            'Xuất Excel trên dòng / màn chi tiết tải file chi tiết của phiếu đó (letterhead, số phiếu, ngày kiểm kê, kho, ghi chú, '
            'bảng chi tiết, nhận xét, khối ký).',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel trên bảng.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 11 trường (tích sẵn theo cột đang hiện).\n'
             '3. Người dùng tích, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy mọi phiếu theo bộ lọc + phạm vi xem, dựng file có letterhead công ty người xuất, tiêu đề “DANH SÁCH '
             'PHIẾU KIỂM KÊ THEO HÀNG HÓA”, dòng thời gian (khi lọc Ngày tạo), cột STT + trường đã chọn, khối ký.\n'
             '5. Hệ thống tải file “danh_sach_phieu_kiem_ke_theo_hang_hoa.xlsx”, báo “Xuất Excel thành công.”.\n'
             '6. Xuất 1 phiếu: bấm Xuất Excel trên dòng / chi tiết → tải “phieu_kiem_ke_theo_mat_hang_<số phiếu>.xlsx”.',
       phu='• Không có phiếu khớp → vẫn ra file có tiêu đề, dòng tên cột và khối ký.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi → “Lỗi khi xuất Excel.”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng; nút Xuất Excel khóa trong lúc đang xuất. Dòng tiêu đề cột không tô nền. Ngày duyệt kèm giờ. '
               'File 1 phiếu: letterhead theo công ty ghi trên phiếu, số lượng là ô số.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('21_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 11 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        ['- Số phiếu, Kế hoạch kiểm kê, Ngày kiểm kê, Kho, Trạng thái, Người tạo',
         '- Ngày tạo, Người duyệt, Ngày duyệt, Ngày cập nhật, Người cập nhật']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/11 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', ['- Bấm → tải file', '- Khóa khi chưa tích / đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Giống nút Đóng.'),
       ('File danh sách', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Letterhead, tiêu đề “DANH SÁCH PHIẾU KIỂM KÊ THEO HÀNG HÓA”', '- Dòng thời gian khi lọc Ngày tạo',
         '- Cột STT + trường đã chọn; khối ký cuối file']),
       ('File 1 phiếu', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu',
        ['- Tên “phieu_kiem_ke_theo_mat_hang_<số phiếu>.xlsx”', '- “PHIẾU KIỂM KÊ THEO MẶT HÀNG”, Số phiếu, Ngày kiểm kê, Kho vật lý, Ghi chú',
         '- Bảng chi tiết, “Nhận xét, đánh giá:”, khối ký Hội đồng kiểm kê / Trưởng bộ phận kho']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', ['- Thành công: “Xuất Excel thành công.”', '- Thất bại: “Lỗi khi xuất Excel.”']),
   ],
   ev=[
       ('Bấm Xuất Excel (bảng)', 'Click', 'Before:\n– Không có lượt xuất đang chạy.\nDuring:\n– Tích sẵn trường theo cột đang hiện.\nAfter:\n– Mở cửa sổ chọn trường.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Kéo bằng biểu tượng.\nDuring:\n– Chỉ đổi trong cửa sổ.\nAfter:\n– Đổi thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc + phạm vi xem + lối vào.\n– Lỗi → “Lỗi khi xuất Excel.”.\n' + ERR + '\n'
        'After:\n– Tải file danh sách, báo “Xuất Excel thành công.”.'),
       ('Bấm Xuất Excel trên dòng / chi tiết', 'Click',
        'Before:\n– Kiểm tra phạm vi xem; ngoài phạm vi → “Lỗi khi xuất Excel.”.\nDuring:\n– Dựng file theo mẫu phiếu.\nAfter:\n– Tải file 1 phiếu, báo “Xuất Excel thành công.”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không xuất.\nAfter:\n– Đóng cửa sổ.'),
   ])

# ------------------------------------------------------------ 2.18 Lịch sử
fr(18, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu',
       mota='Xem các mốc thao tác của phiếu: Tạo mới, Thay đổi thông tin (giá trị cũ → mới: kho, công ty thuê kho, ghi chú, danh sách '
            'hàng, hội đồng, kết quả kiểm kê, hàng thừa khác, file đính kèm), Thay đổi trạng thái (gồm Lưu và gửi, Gửi duyệt, Duyệt '
            'kết quả kèm ghi chú duyệt, phiếu xử lý được lập), Từ chối (kèm lý do), Xóa. Cửa sổ ở danh sách và khối Lịch sử ở màn chi '
            'tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động (hoặc trong menu Hành động khác), hoặc Xem lịch sử ở màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ “Lịch sử thay đổi: <số phiếu>” và hiển thị các mốc, mới nhất ở trên.',
       phu='• Phiếu từ hệ thống cũ chưa có mốc → “Chưa có lịch sử thao tác nào.”.\n'
           '• Bấm Bộ lọc → các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài → đóng; danh sách giữ nguyên trang, bộ lọc.',
       dacbiet='Dòng sửa kết quả chỉ ghi tên hàng + trường đổi. Mốc Duyệt kết quả hiện tiêu đề “Thay đổi trạng thái” màu cam như các '
               'mốc đổi trạng thái khác. Xem, in, xuất Excel không ghi mốc.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('20_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <số phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái / Từ chối: “Trạng thái: <cũ> → <mới>” kèm ghi chú',
           '- Thay đổi thông tin: từng trường cũ → mới', '- Mới nhất ở trên']),
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
       ('Đổi điều kiện Bộ lọc', 'Change', 'Before:\n– Không có nút Tìm kiếm.\nDuring:\n– Lọc theo hành động / người / ngày.\nAfter:\n– Lọc lại danh sách mốc.'),
       ('Bấm Làm mới (khối ở chi tiết)', 'Click', 'Before:\n– Khối đang mở.\nDuring:\n– Nạp lại.\nAfter:\n– Hiện các mốc mới nhất.'),
       ('Bấm Đóng / (x) / click ra ngoài', 'Click', 'Before:\n– Không hỏi xác nhận.\nDuring:\n– Không ghi dữ liệu.\nAfter:\n– Đóng; danh sách giữ nguyên trang, bộ lọc.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Kiểm kê theo hàng hóa; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phiếu không ghi tồn', [
        '– Lưu / gửi / gửi duyệt / duyệt không đổi tồn kho, không sinh phiếu nhập / xuất.',
        '– Chỉ phiếu điều chuyển vị trí / nhập kho / xuất kho điều chỉnh lập từ phiếu mới đổi tồn; tồn trên phiếu là ảnh chụp lúc thêm / làm mới.'],
     ['Tạo', 'Duyệt', 'Xử lý']),
    ('BR-02', 'Phạm vi xem', [
        '– Lối Kho: V1 mọi phiếu; V2 công ty mình + của mình (công ty trống → của mình); không quyền: của mình. Phiếu Đang tạo chỉ người tạo thấy.',
        '– Lối chờ duyệt kết quả: Q2 → mọi phiếu Chờ KT duyệt; không Q2 → phiếu mình tạo.',
        '– Ngoài phạm vi vẫn mở được chi tiết khi đang có việc: Q2 với phiếu Chờ KT duyệt, Q3 với phiếu Chờ / Đang xử lý.',
        '– Quyền xét theo vai trò của công ty đang đăng nhập.'],
     ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất', 'Lịch sử']),
    ('BR-03', 'Quyền và điều kiện thao tác', [
        '– Tạo (lập tay): không cần quyền. Lập từ kế hoạch: Q1 (Super admin miễn).',
        '– Sửa / Xóa: người tạo + Đang tạo. Cập nhật kết quả: người tạo + Đang kiểm / Không duyệt.',
        '– Duyệt / Không duyệt: Q2 + Chờ KT duyệt. Xử lý: Q3 + Chờ / Đang xử lý (nút nhập kho điều chuyển cần thêm Q5).',
        '– Máy chủ kiểm lại khi thao tác: sai trạng thái → báo trạng thái đã thay đổi; đúng trạng thái nhưng thiếu quyền → báo không có quyền.'],
     ['Tạo', 'Chỉnh sửa', 'Xóa', 'Cập nhật kết quả', 'Duyệt', 'Xử lý']),
    ('BR-04', 'Dữ liệu bắt buộc khi lưu phiếu', [
        '– Lưu và Lưu và gửi cùng điều kiện: ≥ 1 Kho, ≥ 1 Công ty thuê kho, ≥ 1 hàng (không trùng), mỗi hàng ≥ 1 vị trí thuộc kho đã chọn, '
        'mỗi vị trí ≥ 1 lô tồn > 0, ≥ 1 thành viên hội đồng có thành viên + chức vụ, không trùng thành viên; Ghi chú ≤ 255 ký tự.',
        '– Mỗi lô ≥ 1 dòng ĐVT kiểm kê; ĐVT phải thuộc hàng; tổng SL × hệ số = tồn theo lô (hệ số lấy từ danh mục).',
        '– Form chỉ chặn định dạng; bắt buộc / trùng do máy chủ trả về đủ một lần, hiện dưới từng ô.'],
     ['Tạo', 'Chỉnh sửa', 'Lưu và gửi']),
    ('BR-05', 'Kế hoạch kiểm kê', [
        '– Popup liệt kê Kế hoạch theo hàng hóa Đang kiểm + Kế hoạch tổng Đã duyệt có ngày bắt đầu và ngày kết thúc từ hôm nay trở đi; chỉ chọn lúc tạo.',
        '– Kế hoạch theo hàng hóa: nạp kho + hàng (tồn hiện tại) + hội đồng, khóa thêm / bớt hàng; lưu (kể cả Lưu nháp) → kế hoạch Đã lập phiếu kiểm kê.',
        '– Kế hoạch tổng: nạp kho, tự thêm hàng; hàng đã có ở phiếu khác cùng kế hoạch tổng bị chặn “Hàng hóa đã lập phiếu kiểm kê.”.',
        '– Xóa phiếu KHÔNG trả trạng thái kế hoạch (giữ như hệ thống cũ, đã chốt).'], ['Tạo', 'Chọn kế hoạch', 'Xóa']),
    ('BR-06', 'Cập nhật kết quả', [
        '– Bắt buộc Thực kiểm mọi dòng (0 – 999,999,999, tối đa 2 số lẻ); Chênh lệch = Thực kiểm − SL do máy chủ tính.',
        '– Hàng thừa khác: hàng có mã hoặc tên + ĐVT; mỗi vị trí phải thuộc kho phiếu và có Thực kiểm.',
        '– Phiếu chưa có file bắt buộc đính kèm (pdf, png, jpg, jpeg, doc, docx, xls, xlsx; ≤ 20MB); file mới nối thêm.'],
     ['Cập nhật kết quả']),
    ('BR-07', 'Vòng đời trạng thái', [
        '– Lưu → Đang tạo; Lưu và gửi → Đang kiểm; Gửi duyệt → Chờ KT duyệt.',
        '– Duyệt: có dòng chênh ≠ 0 → Chờ xử lý; không → Hoàn thành. Không duyệt → Không duyệt (gửi duyệt lại được).',
        '– Lập phiếu xử lý → Đang xử lý; xử lý hết chênh lệch → Hoàn thành.'],
     ['Lưu và gửi', 'Cập nhật kết quả', 'Duyệt', 'Không duyệt', 'Xử lý']),
    ('BR-08', 'Điều kiện nút xử lý', [
        '– Điều chuyển vị trí: có hàng tổng chênh = 0 còn dòng thiếu chưa xử lý; nhập kho điều chuyển: hàng tổng chênh ≠ 0 còn dòng thừa; '
        'xuất kho điều chuyển: hàng tổng chênh ≠ 0 còn dòng thiếu.',
        '– Mỗi loại chỉ lập 1 phiếu từ một phiếu kiểm kê.'], ['Xử lý']),
    ('BR-09', 'Tính duy nhất và chuẩn hóa', [
        '– Không có trường nhập duy nhất; mã <mã công ty>.KKK-NNNNN tự sinh theo công ty người tạo, không sửa được.',
        '– Tổ chức của phiếu = của người tạo; chọn thành viên tự điền chức vụ đầu tiên; Ngày kiểm kê = ngày lưu gần nhất.',
        '– Nút thao tác khóa trong lúc gửi chống tạo trùng.'], ['Tạo', 'Chỉnh sửa', 'Cập nhật kết quả']),
    ('BR-10', 'Khóa hàng đang kiểm kho', [
        '– Hàng thuộc phiếu Đang kiểm / Chờ KT duyệt bị coi là đang kiểm tại các kho của phiếu.',
        '– Phiếu nhập kho, Phiếu điều chuyển hàng, Phiếu điều chuyển vị trí chặn hàng đó tại kho đó.'], ['Lưu và gửi', 'Cập nhật kết quả']),
    ('BR-11', 'Thông báo', [
        '– Gửi duyệt → “Chờ duyệt” cho người có Q4; Duyệt có chênh lệch → “Đã duyệt” cho người có Q3 — cùng công ty người thao tác.',
        '– Không duyệt → “Từ chối” cho người tạo. Bấm thông báo mở chi tiết phiếu; lỗi gửi không làm hỏng thao tác.'],
     ['Cập nhật kết quả', 'Duyệt', 'Không duyệt']),
    ('BR-12', 'In và xuất', [
        '– Letterhead bản in / file 1 phiếu theo công ty ghi trên phiếu; bản in / file danh sách theo công ty người in.',
        '– In danh sách tối đa 2.000 dòng; Xuất Excel danh sách không giới hạn, rỗng vẫn ra file.'], ['In', 'Xuất Excel']),
    ('BR-13', 'Liên kết cấp cha – con và sử dụng ở màn khác', [
        '– Hàng > vị trí > lô > dòng ĐVT kiểm kê; hàng thừa khác > vị trí. Xóa phiếu xóa hết dữ liệu con.',
        '– Kho vật lý, vị trí đã có trong phiếu không xóa được ở danh mục.'],
     ['Tạo', 'Xóa']),
    ('BR-14', 'Quy tắc ghi lịch sử', [
        '– Ghi: Tạo mới; Thay đổi thông tin (cũ → mới, không đổi thì không ghi); Thay đổi trạng thái (gồm Duyệt kết quả); Từ chối; Xóa.',
        '– Kế hoạch theo hàng hóa ghi “Thay đổi trạng thái” kèm mã phiếu khi phiếu được lập. Xem / in / xuất không ghi.'],
     ['Tạo', 'Chỉnh sửa', 'Xóa', 'Cập nhật kết quả', 'Duyệt', 'Lịch sử']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Kiểm kê theo hàng hóa (trạng thái phiếu, kết quả và chênh lệch từng lô, '
    'hàng đang kiểm kho).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Tài chính', 'Kế hoạch kiểm kê theo hàng hóa (nút Lập phiếu mở màn Tạo phiếu đã nạp kế hoạch; lập phiếu → kế hoạch Đã lập '
                       'phiếu kiểm kê, lịch sử kế hoạch ghi mã phiếu; cột Kế hoạch kiểm kê liên kết về kế hoạch)', 'Tài chính -> Kiểm kê'),
    ('2', 'Tài chính', 'Kế hoạch tổng kiểm kê hàng hóa (nút Lập phiếu kiểm kê mở màn Tạo phiếu đã nạp kế hoạch tổng; chặn hàng đã có '
                       'phiếu khác cùng kế hoạch tổng)', 'Tài chính -> Kiểm kê'),
    ('3', 'Tài chính', 'Biên bản xử lý hàng thừa, thiếu sau kiểm kê (đọc chênh lệch theo hàng của phiếu Hoàn thành; liên kết về phiếu)',
     'Tài chính -> Kiểm kê'),
    ('4', 'Kho', 'Báo cáo hàng thừa thiếu sau tổng kiểm kê hàng hóa (đọc kết quả phiếu Hoàn thành: SL thừa / thiếu theo hàng)',
     'Kho -> Báo cáo kho'),
    ('5', 'Kho', 'Phiếu điều chuyển vị trí (lập từ phiếu Chờ / Đang xử lý — đọc dòng thiếu, ghi ngược số đã xử lý và trạng thái Đang xử '
                 'lý / Hoàn thành; chặn hàng đang kiểm kho)', 'Kho -> Điều chuyển'),
    ('6', 'Kho', 'Phiếu nhập kho điều chỉnh kiểm kê (lập từ dòng thừa; lưu → phiếu kiểm kê Đang xử lý)', 'Kho -> Nhập kho'),
    ('7', 'Kho', 'Phiếu xuất kho điều chỉnh kiểm kê (lập từ dòng thiếu; lưu → phiếu kiểm kê Đang xử lý)', 'Kho -> Xuất kho'),
    ('8', 'Tài chính', 'Phiếu nhập hàng điều chỉnh kiểm kê (cộng số đã xử lý vào dòng kết quả; xử lý hết → phiếu kiểm kê Hoàn thành)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Nhập hàng'),
    ('9', 'Tài chính', 'Phiếu xuất hàng điều chỉnh kiểm kê (cộng số đã xử lý vào dòng kết quả; xử lý hết → phiếu kiểm kê Hoàn thành)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Xuất hàng'),
    ('10', 'Kho', 'Phiếu nhập kho (chặn nhập hàng đang thuộc phiếu Đang kiểm / Chờ KT duyệt tại kho đó — “Hàng … đang kiểm kho!”)', 'Kho -> Nhập kho'),
    ('11', 'Tài chính', 'Phiếu điều chuyển hàng (chặn điều chuyển hàng đang kiểm kho — “Hàng hóa đang được kiểm kho, không thể điều chuyển”)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Điều chuyển'),
    ('12', 'Kho', 'Kho vật lý (không xóa được kho đã có trong phiếu)', 'Kho -> Danh mục'),
    ('13', 'Kho', 'Vị trí (không xóa được vị trí đã có trong phiếu / hàng thừa khác)', 'Kho -> Danh mục'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
