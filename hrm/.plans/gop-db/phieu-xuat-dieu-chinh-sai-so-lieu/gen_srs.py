# -*- coding: utf-8 -*-
"""SRS màn "Phiếu xuất điều chỉnh sai số liệu" (phiếu xuất lại, mã PXL-NNNNN) — form chuẩn, chuẩn user chốt 04/11/2026.

Chạy: python gen_srs.py  → SRS - Phiếu xuất điều chỉnh sai số liệu.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + ../phieu-theo-form-quoc-gia/CHECKLIST.md; khuôn cấu trúc
  ../borrow-export/gen_srs.py + ../kiem-ke-theo-hang-hoa/gen_srs.py (Mục lục sang trang riêng + căn giữa, Phần 5 bảng 4 cột
  STT | Nhóm | Màn hình | Đường dẫn).
Nguồn đọc 09/11/2026 (nhánh develop cả 2 repo):
  BE  Modules/Finance/{Services/WarehouseReExportService.php, Http/Controllers/V1/WarehouseReExportController.php,
      Http/Controllers/V1/WarehouseImportController.php (reExportData / reExport / reImportData / reImport),
      Services/WarehouseImportWriteService.php::reImport, Services/PhysicalStockWriter.php (exportShortage / exportLot),
      Entities/WarehouseImport/WarehouseImport.php (canReExport / canReImport / canView), Resources/views/prints/
      warehouse-reexport.blade.php, Services/StockCardReportService.php, Services/ChangeSummaryReportService.php, Routes/api.php},
      app/Helper/PermissionHelper.php::checkPermissionListWithColumn, PermissionsTableSeeder (nhóm "Phiếu xuất điều chỉnh sai
      số liệu" — nhánh develop chưa có Catalog + mã quyền, tên quyền lấy theo code hiện hành), MasterData Position / ProductUsageGuard.
  FE  pages/finance/warehouse-reexports/** (index, _id/index, components/{constants, row-actions}.js),
      pages/finance/warehouse-imports/{_id/re-export.vue, _id/re-import.vue, _id/index.vue, components/row-actions.js},
      pages/warehouse/stock-card/components/voucher-link.js, components/subsystem-menu/{warehouse.js, finance.js}.
  Bối cảnh: design.md, plan.md (#11693, #11890, #11919), spec docs/superpowers/specs/gop-db/2026-10-27-phieu-xuat-dieu-chinh-sai-so-lieu-design.md.
Ảnh: ./pxdc_shots — dev-hrm 09/11/2026 (_capture/capture.js, DNS Admin, chặn mọi yêu cầu ghi: 0 yêu cầu ghi). Mọi ảnh là
  trạng thái THẬT trên dev; form Tạo phiếu xuất lại / Tạo phiếu nhập lại và hộp Xác nhận xuất lại chỉ mở rồi Đóng / Quay lại.
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

TEN = 'Phiếu xuất điều chỉnh sai số liệu'
SHOTS = os.path.join(HERE, 'pxdc_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Kho => Xuất kho => Phiếu xuất điều chỉnh sai số liệu'
MENU_PNK = 'Phân hệ Kho => Nhập kho => Phiếu nhập kho'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Phiếu xuất điều chỉnh sai số liệu.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')
Q4 = ('Xem phiếu xuất lại theo tổng công ty / Xem phiếu xuất lại theo công ty / Xem phiếu xuất lại theo phòng ban / '
      'Xem phiếu xuất lại theo bộ phận')
A_XEM = 'Người xem phiếu'
A_NT = 'Người tạo phiếu nhập kho'
TN = ('Người dùng có quyền thực hiện chức năng: một trong 4 quyền %s (không có quyền nào thì chỉ thao tác trên phiếu '
      'mình tạo).' % Q4)
TN_NT = ('Người dùng có quyền thực hiện chức năng: người đã tạo phiếu nhập kho gốc (điều kiện theo người tạo, không theo quyền '
         'được gán).')
DK = ('1. Người dùng đăng nhập thành công.\n2. Phiếu nằm trong phạm vi xem của người dùng (theo 4 quyền xem hoặc phiếu mình '
      'tạo).\n3. Người dùng đang ở màn Danh sách phiếu xuất lại.')

d = SrsDoc(out=OUT, menu=MENU, route='/finance/warehouse-reexports', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Kho': 'menu_phanhe', 'Xuất kho': 'menu_nhom', 'Phiếu xuất điều chỉnh sai số liệu': 'menu_muc',
    'Nhập kho': 'menu_nhom_nk', 'Phiếu nhập kho': 'menu_muc_pnk',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc', 'Cấu hình cột': 'btn_cauhinhcot',
    'Xem chi tiết': 'link_sophieu', 'Tạo phiếu xuất lại': 'btn_taophieuxuatlai', 'Tạo phiếu nhập lại': 'btn_taophieunhaplai_row',
    'In': 'btn_in_row', 'Xuất Excel': 'btn_xuatexcel', 'Lịch sử': 'btn_lichsu_row', 'Xem chi tiết phiếu nhập kho': 'link_pnk',
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
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Phiếu xuất điều chỉnh sai số liệu (còn gọi là phiếu xuất lại, mã phiếu '
    'PXL-NNNNN), phân hệ Kho, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ luồng điều chỉnh khi phiếu nhập kho bị Kế toán kho Không duyệt: người tạo phiếu nhập kho lập phiếu xuất lại để '
    'trừ toàn bộ hàng đã nhập ra khỏi kho (đúng lô, đúng vị trí), sau đó lập phiếu nhập lại với số liệu đúng.',
    'Làm rõ các dữ liệu bị ghi ngược sang phiếu nhập kho gốc, tồn kho và các báo cáo kho.',
])
d.p('Phạm vi chức năng: Xem danh sách, Tìm kiếm và lọc, Cài đặt bộ lọc, Tùy chỉnh cột, Tạo phiếu xuất lại (thực hiện từ màn '
    'Phiếu nhập kho), Tạo phiếu nhập lại, Xem chi tiết, In phiếu, Xuất Excel danh sách, Xem lịch sử thay đổi. Màn KHÔNG có nút '
    'Tạo mới trên danh sách, KHÔNG có Sửa, Xóa, Gửi duyệt, Duyệt, Không duyệt, Hủy, Khóa / Mở khóa, Import Excel và In danh '
    'sách: phiếu chỉ sinh ra từ phiếu nhập kho bị Không duyệt và chỉ đổi trạng thái khi lập phiếu nhập lại.')
d.p('Mục đích sử dụng dữ liệu:')
d.bullets([
    'Phiếu xuất lại là chứng từ trừ tồn kho: toàn bộ lô hàng của phiếu nhập kho gốc được trừ đúng vị trí, đúng lô đã nhập.',
    'Phiếu nhập kho gốc chuyển trạng thái Đã xuất lại; khi lập phiếu nhập lại thì phiếu nhập kho gốc chuyển Đã nhập lại.',
    'Dòng xuất của phiếu hiện ở Thẻ kho (số chứng từ PXL-NNNNN), được cộng vào số xuất của Tổng hợp xuất nhập tồn và làm '
    'giảm tồn ở các báo cáo tồn kho.',
])
d.p('Ràng buộc nghiệp vụ quan trọng:')
d.bullets([
    'Chỉ người tạo phiếu nhập kho, khi phiếu đó đang Không duyệt, mới tạo được phiếu xuất lại (BR-02).',
    'Xuất lại là xuất TOÀN BỘ hàng của phiếu nhập kho, không sửa số lượng; kho phải đủ tồn ở từng vị trí và từng lô (BR-03).',
    'Chỉ người tạo phiếu nhập kho gốc thấy và dùng được Tạo phiếu nhập lại khi phiếu xuất lại đang Chờ nhập lại (BR-05).',
    'Phiếu xuất lại không sửa, không xóa được; phạm vi xem theo 4 quyền xem, không có quyền thì chỉ thấy phiếu mình tạo (BR-01).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu xuất điều chỉnh sai số liệu (phiếu xuất lại)', 'Chứng từ PXL-NNNNN của màn này: xuất toàn bộ hàng của một phiếu '
                                                          'nhập kho bị Không duyệt ra khỏi kho để nhập lại cho đúng.'),
    ('Phiếu nhập kho (PNK)', 'Phiếu PNK-NNNNN ở màn Phiếu nhập kho; mỗi phiếu xuất lại gắn đúng 1 phiếu nhập kho gốc.'),
    ('Phiếu nhập lại', 'Phiếu nhập kho MỚI lập bằng nút Tạo phiếu nhập lại, chép thông tin của phiếu nhập kho gốc.'),
    ('Trạng thái Chờ nhập lại', 'Nhãn màu vàng: phiếu xuất lại vừa lập, chưa có phiếu nhập lại.'),
    ('Trạng thái Đã nhập lại', 'Nhãn màu xanh lá: đã lập phiếu nhập lại từ phiếu nhập kho gốc.'),
    ('Trạng thái phiếu nhập kho liên quan', 'Không duyệt (điều kiện tạo phiếu xuất lại) → Đã xuất lại (sau khi tạo phiếu xuất '
                                            'lại) → Đã nhập lại (sau khi tạo phiếu nhập lại).'),
    ('Lô / Vị trí', 'Trường đặc thù: mỗi dòng hàng của phiếu nhập kho được nhập vào một hoặc nhiều vị trí; phiếu xuất lại trừ '
                    'đúng số lượng đó tại đúng vị trí và lô nhập.'),
    ('Tổng SL / SL', 'Tổng SL là số lượng của dòng hàng; SL là số lượng tại từng vị trí (cột con của Chi tiết).'),
    ('Cấu trúc phân cấp', 'Phiếu xuất lại > dòng hàng hóa (hàng + đơn vị tính) > dòng chi tiết theo vị trí (Vị trí, SL).'),
    ('Phạm vi xem', 'Tập phiếu người dùng được thấy theo quyền xem cao nhất đang có (tổng công ty > công ty > phòng ban > bộ phận).'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Màn có 4 quyền XEM theo cấp (nhóm quyền “Phiếu xuất điều chỉnh sai số liệu”, phân hệ Kho). Thao tác Tạo phiếu xuất lại và '
    'Tạo phiếu nhập lại KHÔNG theo quyền được gán mà theo người tạo phiếu nhập kho gốc. Người dùng là Super admin xem được mọi '
    'phiếu. Không gắn quyền ở menu: ai cũng mở được màn, dữ liệu do hệ thống giới hạn theo phạm vi.')
d.p('Nhóm quyền xem:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng / phạm vi dữ liệu'], [
    ('Q1', 'Xem phiếu xuất lại theo tổng công ty', 'Xem mọi phiếu của mọi công ty; khối lọc có ô Công ty và Phòng ban.'),
    ('Q2', 'Xem phiếu xuất lại theo công ty', 'Xem phiếu thuộc công ty đang làm việc và phiếu mình tạo; khối lọc có ô Phòng ban.'),
    ('Q3', 'Xem phiếu xuất lại theo phòng ban', 'Xem phiếu thuộc phòng ban hoặc bộ phận mình quản lý và phiếu mình tạo.'),
    ('Q4', 'Xem phiếu xuất lại theo bộ phận', 'Xem phiếu thuộc bộ phận mình quản lý và phiếu mình tạo.'),
], widths=[0.8, 2.2, 3.0])
d.p('Công ty / phòng ban / bộ phận của phiếu xuất lại lấy theo phiếu nhập kho gốc. Có nhiều quyền thì áp quyền cao nhất. Màn '
    'chi tiết, In và Lịch sử còn mở được khi người dùng xem được phiếu nhập kho gốc (liên kết từ màn Phiếu nhập kho).')
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'Q2', 'Q3', 'Q4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅ mọi phiếu', '✅ công ty', '✅ phòng ban', '✅ bộ phận', '✅ chỉ phiếu mình tạo'),
    ('FR-02 Tìm kiếm và lọc', '✅ (có ô Công ty, Phòng ban)', '✅ (có ô Phòng ban)', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Tạo phiếu xuất lại', 'Theo người tạo PNK', 'Theo người tạo PNK', 'Theo người tạo PNK', 'Theo người tạo PNK',
     'Theo người tạo PNK'),
    ('FR-06 Tạo phiếu nhập lại', 'Theo người tạo PNK', 'Theo người tạo PNK', 'Theo người tạo PNK', 'Theo người tạo PNK',
     'Theo người tạo PNK'),
    ('FR-07 Xem chi tiết', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ phiếu mình tạo'),
    ('FR-08 In phiếu', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ phiếu mình tạo'),
    ('FR-09 Xuất Excel', '✅ theo phạm vi', '✅ theo phạm vi', '✅ theo phạm vi', '✅ theo phạm vi', '✅ phiếu mình tạo'),
    ('FR-10 Xem lịch sử thay đổi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi', '✅ trong phạm vi',
     '✅ phiếu mình tạo'),
    ('Thêm mới trên danh sách / Sửa / Xóa / Khóa – Mở khóa / Duyệt / Không duyệt / Import', '—', '—', '—', '—',
     '— (màn không có chức năng này)'),
], widths=[1.9, 0.85, 0.85, 0.85, 0.85, 0.9])
d.p('Trường hợp không có quyền:')
d.bullets([
    'Không có quyền xem nào: vẫn mở được màn, danh sách chỉ có phiếu do chính mình tạo; không có ô lọc Công ty, Phòng ban.',
    'Mở màn chi tiết của phiếu ngoài phạm vi (qua đường link): hệ thống chuyển sang trang “không tìm thấy” (404), không hiện '
    'dữ liệu phiếu.',
    'Không phải người tạo phiếu nhập kho gốc: không thấy nút Tạo phiếu xuất lại / Tạo phiếu nhập lại; mở thẳng màn tạo thì hệ '
    'thống báo “Phiếu không xuất lại được hoặc bạn không có quyền.” / “Phiếu không nhập lại được hoặc bạn không có quyền.”.',
    'Bị gỡ quyền giữa lúc thao tác: lần nạp dữ liệu tiếp theo hệ thống áp phạm vi mới (quyền kiểm lại ở từng lần gọi).',
])
d.p('Điều kiện hiển thị và thao tác:')
d.table(['Đối tượng', 'Điều kiện hiển thị', 'Ghi chú'], [
    ('Nút Xuất Excel, Cấu hình cột, Cài đặt bộ lọc', 'Luôn hiện', 'Dữ liệu xuất giới hạn theo phạm vi xem'),
    ('Nút In, Lịch sử trên dòng', 'Luôn hiện trên mọi dòng', 'Không có nút Sửa / Xóa'),
    ('Nút Tạo phiếu nhập lại (dòng, màn chi tiết)', 'Người đăng nhập là người tạo phiếu nhập kho gốc VÀ phiếu nhập kho đang Đã '
                                                   'xuất lại', 'Phiếu xuất lại khi đó ở trạng thái Chờ nhập lại'),
    ('Ô lọc Công ty', 'Có quyền Q1 hoặc là Super admin', '—'),
    ('Ô lọc Phòng ban', 'Có quyền Q1 hoặc Q2 (hoặc Super admin)', '—'),
    ('Nút Tạo phiếu xuất lại (màn Phiếu nhập kho)', 'Người tạo phiếu nhập kho và phiếu đang Không duyệt',
     'Lối vào duy nhất để sinh phiếu xuất lại'),
], widths=[2.4, 2.0, 1.6])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_XEM, [0, 3, 4]), (A_NT, [1, 2])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Tạo phiếu xuất lại', 'crud'),
     ('FR-06', 'Tạo phiếu nhập lại', 'crud'),
     ('FR-08', 'In phiếu', 'io'),
     ('FR-09', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-07', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-10', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None)],
    'Sơ đồ Use Case tổng quan màn Phiếu xuất điều chỉnh sai số liệu')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu xuất lại',
       mota='Hiển thị bảng các phiếu xuất điều chỉnh sai số liệu trong phạm vi xem của người dùng (theo 4 quyền xem, không có '
            'quyền thì chỉ phiếu mình tạo), kèm phân trang, sắp xếp và tổng số phiếu khớp bộ lọc. Mỗi dòng có liên kết sang '
            'chi tiết phiếu, sang phiếu nhập kho gốc và các nút In, Lịch sử, Tạo phiếu nhập lại (khi đủ điều kiện).',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Không cần quyền riêng để mở màn; dữ liệu giới hạn theo phạm vi xem.',
       chinh='1. Người dùng vào màn theo đường dẫn ở mục Layout.\n'
             '2. Hệ thống xác định phạm vi xem theo quyền cao nhất người dùng có (Super admin: mọi phiếu).\n'
             '3. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất (nếu vừa đi vào màn chi tiết của màn này) và cấu '
             'hình cột đã lưu của người dùng.\n'
             '4. Hệ thống lấy các phiếu trong phạm vi khớp bộ lọc, sắp phiếu tạo gần nhất ở trên.\n'
             '5. Hệ thống hiển thị trang 1, 10 dòng/trang, kèm dòng “Hiển thị a–b / N” và phân trang.\n'
             '6. Với từng dòng, hệ thống tính nút Tạo phiếu nhập lại (chỉ hiện với người tạo phiếu nhập kho gốc khi phiếu nhập '
             'kho đang Đã xuất lại).',
       phu='• Không có quyền xem nào → danh sách chỉ có phiếu do chính người dùng tạo; không có phiếu nào thì bảng hiện “Không '
           'có dữ liệu phù hợp.”.\n'
           '• Không có phiếu khớp bộ lọc → bảng hiện “Không có dữ liệu phù hợp.”, không có dòng “Hiển thị”.\n'
           '• Máy chủ lỗi khi nạp → thông báo “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”, bảng trống.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó.\n'
           '• Phiên đăng nhập hết hạn → hệ thống báo hết phiên, xóa phiên và chuyển về màn đăng nhập.',
       dacbiet='Cột mặc định hiện: cả 7 cột (STT, Mã phiếu, Phiếu nhập kho, Ngày tạo, Người tạo, Trạng thái, Hành động); không '
               'có cột ẩn mặc định. Cột khóa trong Tùy chỉnh cột: STT, Mã phiếu, Hành động. Sắp xếp được: Mã phiếu, Ngày tạo; '
               'mặc định Ngày tạo mới nhất ở trên. Đổi bộ lọc, đổi sắp xếp, đổi số dòng đều về trang 1; chuyển trang giữ bộ '
               'lọc và sắp xếp. Mỗi trang tối đa 200 dòng. Màn không có nút Tạo mới và In danh sách.'),
   layout=dict(menu=MENU, shot=shot('01_list'), shot_caption='Màn Danh sách phiếu xuất lại'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        ['- “Danh sách phiếu xuất lại” trên thanh tiêu đề, tiêu đề bảng và tab trình duyệt',
         '- Mục menu vẫn ghi “Phiếu xuất điều chỉnh sai số liệu”']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”', '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.9)',
         '- Khóa trong lúc đang xuất; bên cạnh hiện tiến độ “Đang chuẩn bị dữ liệu…”']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        '- Biểu tượng cột; bấm → mở cửa sổ Tuỳ chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Đánh số liên tục theo trang (trang 2 bắt đầu từ số dòng/trang + 1)', '- Cột khóa']),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PXL-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết phiếu (mục 2.7)', '- Sắp xếp được', '- Cột khóa']),
       ('Cột Phiếu nhập kho', 'Table/Grid', 'Read-only', 'PNK-NNNNN', 'Hiển thị',
        ['- Mã phiếu nhập kho gốc', '- Là liên kết: bấm → mở chi tiết phiếu nhập kho ở TAB MỚI', '- Không sắp xếp']),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Thời điểm tạo phiếu xuất lại', '- Sắp xếp được; mặc định mới nhất ở trên']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Dạng “Mã phòng ban - Họ tên” người tạo phiếu xuất lại', '- Tự xuống dòng khi dài', '- Không sắp xếp']),
       ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 2 giá trị', 'Hiển thị',
        ['- Chờ nhập lại: nhãn màu vàng', '- Đã nhập lại: nhãn màu xanh lá', '- Không sắp xếp']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Nút Tạo phiếu nhập lại: chỉ hiện với người tạo phiếu nhập kho gốc khi phiếu nhập kho đang Đã xuất lại; bấm → mở '
           'màn Tạo phiếu nhập lại (mục 2.6)',
           '- Nút In: bấm → mở cửa sổ Xem trước phiếu (mục 2.8)',
           '- Nút Lịch sử: bấm → mở cửa sổ Lịch sử thay đổi (mục 2.10)', '- Không có nút Sửa / Xóa', '- Cột khóa']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- Trong bảng: “Không có dữ liệu phù hợp.”', '- Chỉ hiện khi N = 0']),
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
        'Before:\n– Xác định phạm vi xem theo quyền cao nhất (Q1 > Q2 > Q3 > Q4 > phiếu mình tạo).\n'
        '– Khôi phục bộ lọc (10 phút) và cấu hình cột đã lưu.\n'
        'During:\n– Lấy các phiếu trong phạm vi khớp bộ lọc; tính cờ Tạo phiếu nhập lại cho từng dòng.\n'
        '– Máy chủ lỗi → hiển thị “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, phiếu tạo mới nhất ở trên, kèm dòng “Hiển thị a–b / N”.'),
       ('Bấm Mã phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem.\n'
        'After:\n– Mở màn chi tiết phiếu (mục 2.7); bộ lọc hiện tại được ghi nhớ 10 phút để khôi phục khi quay lại.'),
       ('Bấm mã Phiếu nhập kho', 'Click',
        'Before:\n– Dòng có phiếu nhập kho gốc.\n'
        'After:\n– Mở chi tiết phiếu nhập kho ở tab mới; danh sách giữ nguyên trang và bộ lọc.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ cột Mã phiếu và Ngày tạo hỗ trợ sắp xếp; cột khác không có biểu tượng sắp xếp.\n'
        'After:\n– Lần 1 tăng dần, lần 2 giảm dần; nạp lại từ trang 1, giữ bộ lọc.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp.\nAfter:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại theo số dòng mới.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu xuất lại',
       mota='Thu hẹp danh sách theo mã phiếu, mã phiếu nhập kho, người tạo, trạng thái, ngày tạo và Công ty – Phòng ban. Ô tìm '
            'nhanh tìm đồng thời theo mã phiếu xuất lại và mã phiếu nhập kho gốc; các ô lọc nằm trong khối Tìm kiếm nâng cao, '
            'bật / tắt được bằng Cài đặt bộ lọc (mục 2.3). Mọi điều kiện chỉ lọc trong phạm vi xem của người dùng.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng nhập mã vào ô tìm nhanh rồi bấm Tìm kiếm (hoặc nhấn Enter).\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Hệ thống lọc ngay khi một ô lọc đổi giá trị (ô chữ lọc khi gõ), về trang 1.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N” và phân trang.\n'
             '5. Hệ thống ghi nhớ bộ lọc 10 phút khi người dùng đi vào màn chi tiết của màn này.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Gõ vào ô tìm nhanh mà chưa bấm Tìm kiếm / Enter → danh sách chưa đổi.\n'
           '• Bấm dấu × trong ô chọn → xóa giá trị của ô đó.\n'
           '• Người dùng không có quyền Q1 / Q2 → không có ô Công ty / Phòng ban.',
       dacbiet='Trường tìm nhanh: mã phiếu xuất lại HOẶC mã phiếu nhập kho (không tìm theo tên người). Kiểu khớp: một phần, '
               'không phân biệt hoa / thường; khoảng trắng đầu / cuối được bỏ. Không giới hạn số ký tự nhập. Ký tự % và _ được '
               'hiểu là ký tự đại diện. Mọi điều kiện kết hợp theo kiểu VÀ. Ngày tạo lấy trọn hai ngày biên, được bỏ trống một '
               'đầu. Ô Người tạo chỉ liệt kê người đã tạo phiếu trong phạm vi xem. Ô Công ty chỉ có hiệu lực với người có quyền '
               'Q1 / Super admin. Ghi nhớ bộ lọc: trên trình duyệt, 10 phút, chỉ khi đi vào màn chi tiết; F5 hoặc sang màn '
               'khác thì bộ lọc về trống.'),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm theo mã phiếu, mã phiếu nhập kho”', '- Khớp một phần mã phiếu xuất lại hoặc mã phiếu nhập kho',
         '- Chỉ lọc khi bấm Tìm kiếm / nhấn Enter']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Bấm → xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, nạp lại từ trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Mã phiếu', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Phiếu có mã chứa chuỗi nhập', '- Lọc ngay khi gõ']),
       ('Phiếu nhập kho', 'Textbox', 'Enable', 'Không giới hạn ký tự', 'Không', 'Trống',
        ['- Phiếu có mã phiếu nhập kho gốc chứa chuỗi nhập', '- Lọc ngay khi gõ']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách người đã tạo phiếu', 'Không', 'Trống',
        ['- Mặc định: trống (mọi người)', '- Lựa chọn dạng “Mã phòng ban - Họ tên”, chỉ người có phiếu trong phạm vi xem']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 2 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn: Đã nhập lại / Chờ nhập lại']),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai ngày biên; được bỏ trống một đầu']),
       ('Công ty', 'Dropdown', 'Enable', 'Danh sách công ty', 'Không', 'Trống',
        ['- Chỉ hiện với quyền Q1 / Super admin', '- Mặc định: trống (mọi công ty)']),
       ('Phòng ban', 'Dropdown', 'Enable', 'Danh sách phòng ban', 'Không', 'Trống',
        ['- Chỉ hiện với quyền Q1 hoặc Q2', '- Mặc định: trống']),
   ],
   ev=[
       ('Đổi giá trị một ô lọc', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\n'
        'During:\n– Ghi nhận giá trị mới (ô chữ: theo từng ký tự gõ).\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí trong phạm vi xem.'),
       ('Bấm Tìm kiếm / nhấn Enter ở ô tìm nhanh', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh, bỏ khoảng trắng đầu / cuối.\n'
        'During:\n– Tìm phiếu có mã phiếu hoặc mã phiếu nhập kho chứa chuỗi nhập.\n'
        'After:\n– Về trang 1, nạp lại danh sách, cập nhật tổng số.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Có hoặc không có tiêu chí đang áp.\n'
        'After:\n– Xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\n'
        'After:\n– Mở / thu gọn khối ô lọc; lần mở đầu hệ thống nạp danh sách Người tạo, Trạng thái; trạng thái mở được ghi '
        'nhớ cùng bộ lọc.'),
       ('Quay lại từ màn chi tiết trong 10 phút', 'System',
        'Before:\n– Người dùng vừa đi từ danh sách vào màn chi tiết.\n'
        'After:\n– Khôi phục bộ lọc và trạng thái khối lọc; quá 10 phút thì bộ lọc về trống.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn những ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự của chúng. Cấu '
            'hình lưu riêng theo người dùng cho màn này, không ảnh hưởng người khác và không làm đổi dữ liệu phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 6 mục lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình theo người dùng, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 6 mục theo thứ tự thiết kế; vẫn phải bấm Lưu mới có hiệu lực.\n'
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
        ['- Mã phiếu', '- Phiếu nhập kho', '- Người tạo', '- Trạng thái', '- Ngày tạo', '- Công ty – Phòng ban']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích',
        '- Bỏ tích → ô lọc đó không hiện ở khối Tìm kiếm nâng cao.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí mục lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
        '- Bấm → tích lại đủ 6 mục theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
       ('Khối Tìm kiếm nâng cao sau khi lưu', 'Label', 'Hiển thị', '–', '–', 'Theo cấu hình',
        '- Chỉ hiện các ô đã tích, đúng thứ tự đã kéo.'),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\n'
        'After:\n– Mở cửa sổ, nạp cấu hình đang lưu của người dùng (chưa lưu lần nào → đủ 6 mục theo thiết kế).'),
       ('Kéo đổi vị trí một mục', 'Drag',
        'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\n'
        'During:\n– Gửi danh sách mục đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ 6 mục và đưa thứ tự về thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 7 cột của bảng danh sách. Ba cột STT, Mã phiếu, Hành động bị khóa; cấu '
            'hình lưu riêng theo người dùng trên máy chủ cho màn này, chỉ đổi cách hiển thị, không làm đổi dữ liệu, bộ lọc hay '
            'tổng số phiếu.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 7 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bảng giữ đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định hiện đủ 7 cột. Cấu hình ghi nhớ theo người dùng trên máy chủ: giữ nguyên sau khi tải lại trang, đăng '
               'nhập lại, đổi trình duyệt / máy khác; người dùng khác không bị ảnh hưởng. Cột ẩn vẫn được tích sẵn khi Xuất '
               'Excel nếu đang hiện; cột đang ẩn thì không tích sẵn.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn cột cần hiển thị, kéo để đổi thứ tự cột trên bảng.”'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 7 cột', '–', 'Theo cấu hình đã lưu',
        '- STT, Mã phiếu, Phiếu nhập kho, Ngày tạo, Người tạo, Trạng thái, Hành động.'),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích', '- Bỏ tích → cột ẩn khỏi bảng.'),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Mã phiếu, Hành động', '- Có biểu tượng ổ khóa; không ẩn, không đổi vị trí được']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/7 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình',
        '- n = số cột đang tích, cập nhật ngay khi tích / bỏ tích.'),
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
       ('Tích / bỏ tích một cột', 'Change',
        'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/7 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Cấu hình lưu theo người dùng hiện tại.\n'
        'During:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng theo cột đã chọn.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ; bảng giữ đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5
fr(5, 'Tạo phiếu xuất lại (từ phiếu nhập kho bị Không duyệt)',
   usecase=('FR-05', 'Tạo phiếu xuất lại', 'crud', A_NT),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo phiếu xuất lại từ phiếu nhập kho bị Không duyệt',
       mota='Khi Kế toán kho Không duyệt một phiếu nhập kho đã ghi tồn, người tạo phiếu nhập kho lập phiếu xuất lại để trừ TOÀN '
            'BỘ hàng của phiếu đó ra khỏi kho, đúng lô và đúng vị trí đã nhập (không sửa số lượng). Một lần xác nhận: sinh phiếu '
            'PXL-NNNNN trạng thái Chờ nhập lại, trừ tồn, chuyển phiếu nhập kho sang Đã xuất lại và ghi lịch sử cả 2 phiếu. Chức '
            'năng thực hiện ở màn Phiếu nhập kho; lưu xong hệ thống chuyển về màn danh sách này.',
       tacnhan=TN_NT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo phiếu nhập kho.\n'
                '3. Phiếu nhập kho đang ở trạng thái Không duyệt.',
       chinh='1. Người dùng mở phiếu nhập kho Không duyệt (danh sách hoặc chi tiết Phiếu nhập kho), bấm Tạo phiếu xuất lại.\n'
             '2. Hệ thống kiểm tra người tạo và trạng thái phiếu, mở màn “Tạo phiếu xuất lại”; góc phải khối Thông tin chung ghi '
             '“<người đăng nhập> - <ngày giờ hiện tại>”.\n'
             '3. Hệ thống hiển thị thông tin phiếu nhập kho (chỉ đọc) và bảng Hàng hoá xuất lại gồm toàn bộ lô, vị trí đã nhập.\n'
             '4. Người dùng nhập Ghi chú (không bắt buộc) và bấm Xuất lại.\n'
             '5. Hệ thống hiện hộp “Xác nhận xuất lại”; người dùng bấm Xuất lại trong hộp.\n'
             '6. Hệ thống kiểm tra lại người tạo, trạng thái, Ghi chú và đủ tồn ở mọi lô / vị trí.\n'
             '7. Hệ thống sinh mã PXL-NNNNN, lưu phiếu trạng thái Chờ nhập lại (công ty / phòng ban theo phiếu nhập kho), chép '
             'dòng hàng, vị trí và nhóm hàng; trừ tồn kho, tồn vị trí, tồn lô.\n'
             '8. Hệ thống chuyển phiếu nhập kho sang Đã xuất lại.\n'
             '9. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu xuất lại và “Thay đổi trạng thái” (ghi chú '
             '“Tạo phiếu xuất lại PXL-…”) trong lịch sử của phiếu nhập kho.\n'
             '10. Hệ thống hiển thị “Hàng đã được xuất lại” và chuyển về màn Danh sách phiếu xuất lại.',
       phu='• Không phải người tạo / phiếu không còn Không duyệt khi mở màn → thông báo “Phiếu không xuất lại được hoặc bạn '
           'không có quyền.”, quay về danh sách Phiếu nhập kho.\n'
           '• Phiếu đổi trạng thái trong lúc đang mở màn → bấm xác nhận nhận thông báo “Chỉ người tạo phiếu nhập kho bị Không '
           'duyệt mới được tạo phiếu xuất lại.”, không lưu.\n'
           '• Kho không đủ tồn → thông báo dạng “Hàng <tên> không đủ tồn kho. Cần <x>, còn <y>” / “… không đủ tồn tại vị trí '
           '<mã vị trí> …” / “… không đủ tồn trong lô tại vị trí …”; không trừ gì.\n'
           '• Ghi chú quá 255 ký tự → viền đỏ, “Không được vượt quá 255 ký tự” dưới ô và thông báo cùng câu.\n'
           '• Bấm Đóng / (x) trong hộp xác nhận → đóng hộp, không lưu, giữ dữ liệu đã nhập.\n'
           '• Bấm Quay lại → về chi tiết phiếu nhập kho NGAY, không hỏi xác nhận kể cả khi đã nhập Ghi chú.',
       dacbiet='Không sửa được số lượng: phiếu xuất lại chép nguyên lô của phiếu nhập kho. Nút Xuất lại khóa trong lúc lưu để '
               'một lần bấm không tạo 2 phiếu. Phiếu không có trường nhập duy nhất: mã PXL-NNNNN tự sinh tăng dần; một phiếu '
               'nhập kho chỉ xuất lại được 1 lần vì sau đó đã chuyển Đã xuất lại. Không có Lưu nháp, Lưu và tiếp tục. Thao '
               'tác không hoàn tác được.'),
   layout=dict(entries=[
       (MENU_PNK + ' => Xem chi tiết phiếu nhập kho => Tạo phiếu xuất lại',
        'Từ màn chi tiết một phiếu nhập kho Không duyệt (chỉ người tạo phiếu thấy nút): mở màn Tạo phiếu xuất lại của phiếu đó.'),
       (MENU_PNK + ' => Tạo phiếu xuất lại',
        'Hoặc bấm biểu tượng Tạo phiếu xuất lại ở cột Hành động của dòng phiếu nhập kho Không duyệt trên danh sách.')],
       shot=shot('10_create'), shot_caption='Màn Tạo phiếu xuất lại'),
   extra=[(shot('09_pnk_deny'), 'Phiếu nhập kho Không duyệt có nút Tạo phiếu xuất lại'),
          (shot('10b_confirm'), 'Hộp Xác nhận xuất lại')],
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tạo phiếu xuất lại” (thanh tiêu đề, tab trình duyệt).'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại',
        '- Góc phải khối Thông tin chung: “<Họ tên> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu nhập kho', 'Link', 'Read-only', 'PNK-NNNNN', '–', 'Phiếu đang xuất lại',
        '- Bấm → mở chi tiết phiếu nhập kho.'),
       ('Người tạo', 'Textbox', 'Disable', '–', '–', 'Người tạo phiếu nhập kho', '- Chỉ đọc.'),
       ('Kho', 'Textbox', 'Disable', '–', '–', 'Kho của phiếu nhập kho', '- Chỉ đọc.'),
       ('Người giao hàng', 'Textbox', 'Disable', '–', '–', 'Theo phiếu nhập kho', '- Chỉ đọc.'),
       ('Lý do không duyệt', 'Textbox', 'Disable', '–', '–', 'Lý do Kế toán kho đã nhập', '- Chỉ đọc.'),
       ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập ghi chú”', '- Lỗi: “Không được vượt quá 255 ký tự” (viền đỏ, kiểm khi lưu)']),
       ('Dòng chú thích khối Hàng hoá xuất lại', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Toàn bộ hàng của phiếu nhập kho được xuất ra khỏi kho đúng lô, đúng vị trí đã nhập.”'),
       ('Bảng Hàng hoá xuất lại', 'Table/Grid', 'Read-only', '–', '–', 'Theo phiếu nhập kho',
        ['- STT, Tên hàng hoá, Model, Mã hàng hoá, Thương hiệu, ĐVT, SL đề nghị, SL thực nhập',
         '- Chi tiết: Vị trí, SL nhập (mỗi vị trí 1 dòng)', '- Dòng Tổng cộng', '- Không sửa được số lượng']),
       ('Nút Xuất lại', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → mở hộp “Xác nhận xuất lại”', '- Khóa trong lúc lưu']),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về chi tiết phiếu nhập kho; không hỏi xác nhận.'),
       ('Hộp “Xác nhận xuất lại”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Nội dung: “Toàn bộ hàng của phiếu <mã PNK> sẽ bị trừ khỏi tồn kho. Thao tác không hoàn tác được.”',
         '- Nút Xuất lại: thực hiện lưu', '- Nút Đóng / (x): đóng hộp, không lưu']),
       ('Thông báo', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Hàng đã được xuất lại”', '- Thiếu tồn: “Hàng <tên> không đủ tồn …”',
         '- Sai điều kiện: “Chỉ người tạo phiếu nhập kho bị Không duyệt mới được tạo phiếu xuất lại.”',
         '- Lỗi khác: “Xuất lại thất bại”']),
   ],
   ev=[
       ('Mở màn Tạo phiếu xuất lại', 'System',
        'Before:\n– Kiểm tra người đăng nhập là người tạo phiếu nhập kho và phiếu đang Không duyệt.\n'
        '– Nếu không đạt → hiển thị “Phiếu không xuất lại được hoặc bạn không có quyền.” và quay về danh sách Phiếu nhập kho.\n'
        'During:\n– Nạp thông tin phiếu nhập kho, toàn bộ lô và vị trí.\n'
        'After:\n– Hiển thị form; chỉ ô Ghi chú nhập được.'),
       ('Bấm Xuất lại (chân màn)', 'Click',
        'Before:\n– Không có lượt lưu đang chạy.\nAfter:\n– Mở hộp “Xác nhận xuất lại” kèm mã phiếu nhập kho.'),
       ('Bấm Xuất lại trong hộp xác nhận', 'Click',
        'Before:\n– Kiểm tra người tạo phiếu nhập kho và trạng thái Không duyệt; không đạt → “Chỉ người tạo phiếu nhập kho bị '
        'Không duyệt mới được tạo phiếu xuất lại.” và dừng xử lý.\n'
        'During:\n– Ghi chú > 255 ký tự → “Không được vượt quá 255 ký tự”.\n'
        '– Kiểm đủ tồn kho, tồn vị trí, tồn lô cho MỌI dòng trước khi trừ; thiếu → “Hàng <tên> không đủ tồn …”.\n' + ERR + '\n'
        'After:\n– Sinh phiếu PXL-NNNNN trạng thái Chờ nhập lại; trừ tồn đúng lô / vị trí.\n'
        '– Phiếu nhập kho chuyển Đã xuất lại.\n'
        '– Ghi một dòng lịch sử “Tạo mới” cho phiếu xuất lại và “Thay đổi trạng thái” cho phiếu nhập kho.\n'
        '– Hiển thị “Hàng đã được xuất lại”, chuyển về màn Danh sách phiếu xuất lại.'),
       ('Bấm Đóng / (x) trong hộp xác nhận', 'Click',
        'Before:\n– Không hỏi thêm.\nAfter:\n– Đóng hộp; form giữ nguyên Ghi chú đã nhập, không lưu.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Không kiểm tra dữ liệu đã nhập.\nAfter:\n– Về chi tiết phiếu nhập kho, Ghi chú đã nhập bị bỏ.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Tạo phiếu nhập lại',
   usecase=('FR-06', 'Tạo phiếu nhập lại', 'crud', A_NT),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và UI/UX.', 'create'),
   intro=dict(
       ten='Tạo phiếu nhập lại từ phiếu xuất lại Chờ nhập lại',
       mota='Sau khi đã xuất lại, người tạo phiếu nhập kho gốc lập phiếu nhập lại: một phiếu nhập kho MỚI chép thông tin của '
            'phiếu gốc (loại nhập, kho, người giao hàng, chuyến xe…), nhập lại đúng số lượng và vị trí. Lưu phiếu nhập lại '
            'chuyển phiếu xuất lại sang Đã nhập lại và phiếu nhập kho gốc sang Đã nhập lại. Form nhập lại dùng chung với màn '
            'Phiếu nhập kho (đặc tả chi tiết ở SRS Phiếu nhập kho); mục này chỉ mô tả phần liên quan tới phiếu xuất lại.',
       tacnhan=TN_NT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng là người tạo phiếu nhập kho gốc.\n'
                '3. Phiếu nhập kho gốc đang Đã xuất lại (phiếu xuất lại đang Chờ nhập lại).',
       chinh='1. Người dùng bấm Tạo phiếu nhập lại ở cột Hành động hoặc ở chân màn chi tiết phiếu xuất lại.\n'
             '2. Hệ thống kiểm tra người tạo và trạng thái phiếu nhập kho gốc, mở màn “Tạo phiếu nhập lại” điền sẵn dữ liệu '
             'phiếu gốc; ô Người giao hàng khóa; file đính kèm để trống; Ghi chú trống thì điền ghi chú của phiếu đề nghị nhập kho.\n'
             '3. Người dùng kiểm tra / sửa số lượng, vị trí, đính kèm file rồi bấm Lưu (phiếu Đang tạo) hoặc Lưu và nhập '
             '(gửi, ghi tồn kho).\n'
             '4. Hệ thống kiểm tra dữ liệu như màn Nhập kho, sinh phiếu nhập kho mới.\n'
             '5. Hệ thống chuyển phiếu xuất lại Chờ nhập lại → Đã nhập lại và phiếu nhập kho gốc → Đã nhập lại.\n'
             '6. Hệ thống ghi nhận hành động “Thay đổi trạng thái” (Chờ nhập lại → Đã nhập lại, ghi chú “Tạo phiếu nhập lại '
             '<mã PNK mới>”) trong lịch sử của phiếu xuất lại, và mốc tương ứng trong lịch sử phiếu nhập kho gốc.\n'
             '7. Hệ thống hiển thị thông báo kết quả và chuyển về danh sách Phiếu nhập kho.',
       phu='• Không phải người tạo phiếu nhập kho gốc / phiếu gốc không còn Đã xuất lại → nút không hiện; mở thẳng màn thì báo '
           '“Phiếu không nhập lại được hoặc bạn không có quyền.”.\n'
           '• Lưu khi điều kiện đã đổi → “Bạn không có quyền nhập lại phiếu này.”; phiếu nhập kho chưa có phiếu xuất lại → '
           '“Phiếu nhập kho chưa có phiếu xuất lại.”.\n'
           '• Dữ liệu sai (số lượng, vị trí, file bắt buộc…) → báo lỗi tại ô như màn Nhập kho; phiếu xuất lại không đổi.\n'
           '• Bấm Quay lại khi đã sửa → hộp “Thông tin chưa lưu” (Thoát / Ở lại); chưa sửa gì thì về danh sách Phiếu nhập '
           'kho ngay.',
       dacbiet='Cả Lưu (phiếu mới ở trạng thái Đang tạo) lẫn Lưu và nhập đều chuyển phiếu xuất lại sang Đã nhập lại. Sau khi Đã '
               'nhập lại, nút Tạo phiếu nhập lại biến mất trên mọi màn. Super admin không được tạo phiếu nhập lại thay người tạo.'),
   layout=dict(entries=[
       (MENU + ' => Tạo phiếu nhập lại',
        'Từ cột Hành động của dòng phiếu Chờ nhập lại (chỉ người tạo phiếu nhập kho gốc thấy nút).'),
       (MENU + ' => Xem chi tiết => Tạo phiếu nhập lại', 'Hoặc từ chân màn chi tiết phiếu xuất lại.')],
       shot=shot('22_reimport'), shot_caption='Màn Tạo phiếu nhập lại mở từ phiếu xuất lại'),
   ui=[
       ('Nút Tạo phiếu nhập lại (dòng)', 'Icon Button', 'Enable', '–', '–', 'Theo điều kiện',
        ['- Rê chuột: “Tạo phiếu nhập lại”', '- Chỉ hiện khi đủ điều kiện ở mục Điều kiện ban đầu']),
       ('Nút Tạo phiếu nhập lại (màn chi tiết)', 'Button', 'Enable', '–', '–', 'Theo điều kiện',
        '- Nút chính ở chân màn chi tiết, cùng điều kiện với nút trên dòng.'),
       ('Tiêu đề màn nhập lại', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tạo phiếu nhập lại”.'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập - giờ hiện tại', '- Góc phải khối thông tin.'),
       ('Thông tin chép từ phiếu gốc', 'Textbox', 'Disable', '–', '–', 'Theo phiếu nhập kho gốc',
        '- Loại nhập, Phiếu đề nghị nhập kho, Kho nhập, Người đề nghị, Người giao hàng (khóa).'),
       ('Ghi chú', 'Textarea', 'Enable', '0–255 ký tự', 'Không', 'Ghi chú phiếu đề nghị nhập kho', '- Sửa được.'),
       ('File đính kèm', 'Table/Grid', 'Enable', '–', 'Có', 'Trống', '- Phải đính kèm lại file (không chép từ phiếu gốc).'),
       ('Bảng hàng hoá', 'Table/Grid', 'Enable', '–', 'Có', 'Theo phiếu gốc',
        '- Vị trí và SL nhập từng dòng, quy tắc như màn Nhập kho.'),
       ('Nút Lưu', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Lưu phiếu nhập kho mới ở trạng thái Đang tạo.'),
       ('Nút Lưu và nhập', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Lưu và gửi, ghi tồn kho.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách Phiếu nhập kho; có thay đổi thì hỏi.'),
       ('Hộp “Thông tin chưa lưu”', 'Popup', 'Hiển thị', '–', '–', 'Ẩn', '- Nút Thoát / Ở lại.'),
       ('Trạng thái phiếu xuất lại sau lưu', 'Badge', 'Read-only', '–', '–', 'Đã nhập lại',
        '- Nhãn xanh lá “Đã nhập lại” ở danh sách và tiêu đề màn chi tiết.'),
   ],
   ev=[
       ('Bấm Tạo phiếu nhập lại', 'Click',
        'Before:\n– Kiểm tra người đăng nhập là người tạo phiếu nhập kho gốc và phiếu gốc đang Đã xuất lại.\n'
        '– Nếu không đạt → hiển thị “Phiếu không nhập lại được hoặc bạn không có quyền.” và dừng xử lý.\n'
        'After:\n– Mở màn Tạo phiếu nhập lại điền sẵn dữ liệu phiếu gốc.'),
       ('Bấm Lưu / Lưu và nhập', 'Click',
        'Before:\n– Kiểm tra lại người tạo và trạng thái; không đạt → “Bạn không có quyền nhập lại phiếu này.”.\n'
        '– Phiếu gốc phải có phiếu xuất lại; không có → “Phiếu nhập kho chưa có phiếu xuất lại.”.\n'
        'During:\n– Kiểm tra dữ liệu như màn Nhập kho (người giao hàng, file, số lượng, vị trí, chuyến xe).\n' + ERR + '\n'
        'After:\n– Sinh phiếu nhập kho mới; phiếu xuất lại mới nhất của phiếu gốc → Đã nhập lại; phiếu gốc → Đã nhập lại.\n'
        '– Ghi một dòng lịch sử “Thay đổi trạng thái” (Chờ nhập lại → Đã nhập lại) cho phiếu xuất lại.\n'
        '– Hiển thị thông báo kết quả, chuyển về danh sách Phiếu nhập kho.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– So dữ liệu hiện tại với lúc mở màn.\n'
        'During:\n– Có thay đổi → hiện hộp “Thông tin chưa lưu”.\n'
        'After:\n– Thoát: về danh sách Phiếu nhập kho, phiếu xuất lại vẫn Chờ nhập lại; Ở lại: giữ form.'),
       ('Mở lại danh sách phiếu xuất lại', 'System',
        'Before:\n– Đã lưu phiếu nhập lại.\nAfter:\n– Dòng phiếu xuất lại hiện “Đã nhập lại”, không còn nút Tạo phiếu nhập lại.'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Xem chi tiết phiếu', usecase=('FR-07', 'Xem chi tiết phiếu', 'view', A_XEM),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu xuất lại',
       mota='Màn chỉ đọc hiển thị thông tin chung của phiếu (lấy từ phiếu nhập kho gốc), bảng hàng hóa đã xuất theo từng vị trí và '
            'khối Lịch sử. Trạng thái phiếu hiện ngay cạnh tiêu đề trang. Màn không có Sửa / Xóa; chỉ có Tạo phiếu nhập lại (khi '
            'đủ điều kiện), In và Quay lại.',
       tacnhan=TN,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Phiếu tồn tại và nằm trong phạm vi xem, hoặc người dùng xem được '
                'phiếu nhập kho gốc.',
       chinh='1. Người dùng bấm Mã phiếu ở danh sách (hoặc liên kết Phiếu xuất lại ở màn Phiếu nhập kho, số chứng từ ở Thẻ kho).\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở màn “Chi tiết phiếu xuất điều chỉnh sai số liệu: <mã>” kèm nhãn trạng thái.\n'
             '4. Hệ thống hiển thị khối Thông tin chung, bảng Chi tiết và khối Lịch sử (thu gọn).',
       phu='• Phiếu ngoài phạm vi / không tồn tại → chuyển sang trang “không tìm thấy” (404), không báo lỗi nổi.\n'
           '• Máy chủ lỗi → thông báo “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”.\n'
           '• Dòng hàng không có vị trí → ô Vị trí, SL để trống; phiếu không có hàng → bảng hiện “Không có dữ liệu”.\n'
           '• Bấm mã phiếu nhập kho → mở chi tiết phiếu nhập kho ở tab mới.\n'
           '• Bấm Quay lại → về danh sách, khôi phục bộ lọc (trong 10 phút).',
       dacbiet='Loại nhập, Kho, Người giao hàng đọc theo phiếu nhập kho gốc tại thời điểm xem. Số lượng hiển thị dạng 1,234.5 '
               '(tối đa 2 chữ số thập phân). Góc phải khối Thông tin chung ghi họ tên người tạo (không kèm mã phòng) và ngày giờ tạo.'),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'), shot_caption='Màn Chi tiết phiếu xuất lại'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn hình', 'Label', 'Hiển thị', '–', 'Hiển thị',
        '- “Chi tiết phiếu xuất điều chỉnh sai số liệu: <mã phiếu>” kèm nhãn trạng thái (vàng Chờ nhập lại / xanh lá Đã nhập lại).'),
       ('Dòng người tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu', '- Góc phải: “<Người tạo> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu nhập kho', 'Link', 'Read-only', 'PNK-NNNNN', 'Theo dữ liệu', '- Bấm → mở chi tiết phiếu nhập kho ở tab mới.'),
       ('Loại nhập', 'Textbox', 'Disable', '–', 'Theo phiếu nhập kho', '- Ví dụ “Nhập hàng mua trong nước (TỰ DO + HÃNG)”.'),
       ('Kho', 'Textbox', 'Disable', '–', 'Theo phiếu nhập kho', '- Tên kho nhập.'),
       ('Người giao hàng', 'Textbox', 'Disable', '–', 'Theo phiếu nhập kho', '- Chỉ đọc.'),
       ('Ghi chú', 'Textbox', 'Disable', '0–255 ký tự', 'Theo dữ liệu', '- Một dòng; rê chuột xem đủ nội dung.'),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, ĐVT, Tổng SL', '- Chi tiết: Vị trí, SL (mỗi vị trí 1 dòng)']),
       ('Trạng thái rỗng của bảng', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Không có dữ liệu”.'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', '- Nút Xem lịch sử mở rộng khối; nội dung như mục 2.10.'),
       ('Nút Tạo phiếu nhập lại', 'Button', 'Enable', '–', 'Theo điều kiện', '- Như mục 2.6.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → cửa sổ Xem trước phiếu (mục 2.8).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về màn danh sách.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra phiếu nằm trong phạm vi xem hoặc người dùng xem được phiếu nhập kho gốc.\n'
        '– Không đạt → chuyển trang “không tìm thấy” và dừng xử lý.\n'
        'During:\n– Lấy dữ liệu phiếu, thông tin phiếu nhập kho, dòng hàng và vị trí.\n'
        '– Lỗi khác → “Đã xảy ra lỗi hệ thống. Vui lòng thử lại.”.\n'
        'After:\n– Hiển thị màn chỉ đọc, tính nút Tạo phiếu nhập lại.'),
       ('Bấm Xem lịch sử', 'Click',
        'Before:\n– Khối đang thu gọn.\nAfter:\n– Mở rộng khối, nạp các mốc lịch sử.'),
       ('Bấm mã Phiếu nhập kho', 'Click', 'Before:\n– Có phiếu nhập kho gốc.\nAfter:\n– Mở chi tiết phiếu nhập kho ở tab mới.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Không có dữ liệu cần lưu.\nAfter:\n– Về danh sách, khôi phục bộ lọc trong 10 phút.'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'In phiếu', usecase=('FR-08', 'In phiếu', 'io', A_XEM),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu xuất lại',
       mota='Xem trước và in một phiếu xuất lại khổ A4 dọc, có chỗ ký Người lập – Kế toán kho – Thủ kho. Bản in mở trong cửa sổ '
            'ngay trên màn đang đứng (danh sách hoặc chi tiết), không mở tab mới nên không mất bộ lọc. Màn không có In danh sách.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm In ở cột Hành động hoặc ở chân màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem.\n'
             '3. Hệ thống mở cửa sổ “Xem trước phiếu xuất lại <mã>”, hiện “Đang tải dữ liệu in…” trong lúc dựng bản in.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Phiếu ngoài phạm vi → bản in không dựng được, cửa sổ báo câu lỗi của máy chủ “Không tìm thấy phiếu xuất lại hoặc '
           'bạn không có quyền xem.”.\n'
           '• Lỗi khác → “Không tải được dữ liệu in”.\n'
           '• Bấm (x) → đóng cửa sổ xem trước, màn giữ nguyên.',
       dacbiet='Logo / tên công ty đầu bản in lấy theo công ty ghi trên phiếu (theo phiếu nhập kho gốc), không theo người đang '
               'xem. Hàng có nhiều vị trí in thành 1 nhóm dòng gộp, không bị cắt ngang khi sang trang.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu xuất lại',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Xem trước phiếu xuất lại <mã phiếu>”.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Cạnh tiêu đề; bấm → hộp thoại in của trình duyệt.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ xem trước.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Đang tải dữ liệu in…”.'),
       ('Đầu bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Logo, tên, địa chỉ công ty của phiếu', '- “PHIẾU XUẤT LẠI ĐIỀU CHỈNH SAI SỐ LIỆU”, Số phiếu, Ngày tạo']),
       ('Thông tin phiếu trên bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Người tạo, Phiếu nhập kho, Loại nhập, Kho', '- Người giao hàng, Ghi chú, Trạng thái (dòng trống thì bỏ)']),
       ('Bảng hàng trên bản in', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Tên hàng hóa, Model, Mã hàng hóa, Thương hiệu, ĐVT, Tổng SL', '- Chi tiết: Vị trí, SL',
         '- Phiếu không có hàng: “Không có hàng hoá”']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị',
        '- Người lập, Kế toán kho, Thủ kho (Ký, họ tên); dòng “Ngày ..... tháng ..... năm .....”.'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Không tìm thấy phiếu xuất lại hoặc bạn không có quyền xem.”', '- “Không tải được dữ liệu in”']),
   ],
   ev=[
       ('Bấm In (dòng / màn chi tiết)', 'Click',
        'Before:\n– Kiểm tra phạm vi xem phiếu; ngoài phạm vi → “Không tìm thấy phiếu xuất lại hoặc bạn không có quyền xem.”.\n'
        'During:\n– Dựng bản in theo dữ liệu hiện tại; lỗi → “Không tải được dữ liệu in”.\n'
        'After:\n– Hiển thị bản xem trước khổ dọc, letterhead theo công ty của phiếu.'),
       ('Bấm In trong cửa sổ xem trước', 'Click', 'Before:\n– Bản in đã dựng xong.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, giữ nguyên màn đang đứng.'),
       ('Đang dựng bản in', 'System', 'Before:\n– Vừa bấm In.\nAfter:\n– Hiện “Đang tải dữ liệu in…” tới khi có bản in.'),
   ])

# ------------------------------------------------------------ 2.9
fr(9, 'Xuất danh sách ra Excel', usecase=('FR-09', 'Xuất Excel', 'io', A_XEM),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu xuất lại ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất toàn bộ phiếu khớp bộ lọc đang áp trong phạm vi xem (không phân trang) ra file '
            'Excel. Cột STT luôn đứng đầu file; đầu file có letterhead công ty người xuất và tiêu đề, cuối file có khối ký Người lập.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 5 trường, tích sẵn các trường đang hiện trên bảng.\n'
             '3. Người dùng tích trường cần xuất, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy lần lượt toàn bộ phiếu theo bộ lọc, hiện tiến độ “Đã tải x/y dòng…”, dựng file theo đúng thứ tự '
             'trường đã chọn.\n'
             '5. Hệ thống tải file “danh_sach_phieu_xuat_lai.xlsx”, báo “Xuất Excel thành công”.',
       phu='• Không có phiếu khớp → không tạo file, báo “Không có dữ liệu để xuất”.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”.\n'
           '• Bấm Đóng / (x) → không xuất.',
       dacbiet='Không giới hạn số dòng (lấy theo từng đợt). Nút Xuất Excel khóa trong lúc đang xuất. Tiêu đề file “DANH SÁCH '
               'PHIẾU XUẤT ĐIỀU CHỈNH SAI SỐ LIỆU”, trang tính “Phieu xuat lai”.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Dòng hướng dẫn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Tích chọn trường cần xuất, kéo để đổi thứ tự cột trong file.”'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 5 trường', 'Ít nhất 1', 'Theo cột đang hiện',
        '- Mã phiếu, Phiếu nhập kho, Ngày tạo, Người tạo, Trạng thái.'),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Kéo để đổi vị trí cột trong file.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/5 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file Excel', '- Khóa khi chưa tích trường nào hoặc đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Nội dung file Excel', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Letterhead công ty của người đang xuất, dòng tiêu đề “DANH SÁCH PHIẾU XUẤT ĐIỀU CHỈNH SAI SỐ LIỆU”',
         '- Dòng tên cột: STT + các trường đã chọn', '- Khối ký cuối file: “Người lập”, “(Ký, họ tên)”']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công”', '- Rỗng: “Không có dữ liệu để xuất”', '- Thất bại: “Lỗi khi xuất Excel”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Không có lượt xuất đang chạy.\nAfter:\n– Mở cửa sổ, tích sẵn các trường ứng với cột đang hiện.'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Kéo bằng biểu tượng của trường.\nAfter:\n– Đổi thứ tự trường; đây là thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích; khóa nút trong lúc xuất.\n– Dữ liệu giới hạn theo phạm vi xem.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc theo từng đợt, hiện tiến độ.\n– Không có dòng → “Không có dữ liệu để xuất”.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.\n' + ERR + '\n'
        'After:\n– Tải file “danh_sach_phieu_xuat_lai.xlsx”, báo “Xuất Excel thành công”.'),
       ('Bấm Đóng / (x)', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.10
fr(10, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu',
       mota='Xem các mốc thao tác của phiếu: người thực hiện, thời điểm, hành động và nội dung. Phiếu có 2 loại mốc: “Tạo mới” '
            '(lúc tạo phiếu xuất lại) và “Thay đổi trạng thái” Chờ nhập lại → Đã nhập lại (lúc tạo phiếu nhập lại, kèm mã phiếu '
            'nhập kho mới). Cửa sổ ở danh sách và khối Lịch sử ở màn chi tiết dùng chung nội dung.',
       tacnhan=TN, dieukien=DK,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động, hoặc Xem lịch sử ở khối Lịch sử màn chi tiết.\n'
             '2. Hệ thống kiểm tra phạm vi xem, mở cửa sổ “Lịch sử thay đổi: <mã phiếu>” và nạp các mốc.\n'
             '3. Hệ thống hiển thị các mốc, mới nhất ở trên.',
       phu='• Phiếu lập trước khi có chức năng lịch sử (hệ thống cũ) → hệ thống dựng mốc “Tạo mới” theo người tạo và ngày tạo của '
           'phiếu, nên lịch sử không trống.\n'
           '• Bấm Bộ lọc → mở các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng; danh sách giữ nguyên trang, bộ lọc, sắp xếp.',
       dacbiet='Xem, in, xuất Excel không ghi mốc. Mốc Tạo mới chỉ hiện tên mốc và người thực hiện. Mốc đổi trạng thái của phiếu '
               'nhập kho gốc ghi ở lịch sử của PHIẾU NHẬP KHO, không ghi lặp ở đây.'),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('16c_history_filter'), 'Khối Bộ lọc trong cửa sổ Lịch sử thay đổi'),
          (shot('17c_detail_history'), 'Khối Lịch sử ở màn chi tiết phiếu')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: <mã phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm dd/mm/yyyy hh:mm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Thay đổi trạng thái: “Trạng thái: Chờ nhập lại → Đã nhập lại”, ghi chú “Tạo phiếu nhập lại PNK-…”',
           '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Trống',
        ['- Mặc định: trống', '- Lựa chọn: Tạo mới / Thay đổi thông tin / Thay đổi trạng thái', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Trống', '- Chọn là lọc ngay.'),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc từ ngày này.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Lọc mốc đến hết ngày này.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', '- Xóa điều kiện lọc.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn', '- Lọc không ra: “Không có lịch sử phù hợp bộ lọc.”'),
       ('Khối Lịch sử ở màn chi tiết', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
        ['- Nút Xem lịch sử / Thu gọn, nút Làm mới, nút Bộ lọc', '- Cùng nội dung với cửa sổ']),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
   ],
   ev=[
       ('Mở lịch sử', 'Click',
        'Before:\n– Kiểm tra phạm vi xem phiếu (như màn chi tiết).\n'
        'During:\n– Nạp các mốc; phiếu chưa có mốc tạo → dựng mốc “Tạo mới” theo người tạo, ngày tạo.\n'
        'After:\n– Hiển thị các mốc, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change', 'Before:\n– Không có nút Tìm kiếm: chọn là lọc.\nAfter:\n– Lọc lại danh sách mốc.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Khối lọc đang mở.\nAfter:\n– Xóa điều kiện lọc, hiện lại đủ các mốc.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ; danh sách giữ nguyên trang và bộ lọc.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Phiếu xuất điều chỉnh sai số liệu; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi xem', [
        '– 4 quyền xem: tổng công ty (mọi phiếu) > công ty (công ty đang làm việc + mình tạo) > phòng ban (phòng / bộ phận quản '
        'lý + mình tạo) > bộ phận (bộ phận quản lý + mình tạo); có nhiều quyền thì áp quyền cao nhất.',
        '– Không có quyền nào: chỉ phiếu mình tạo. Super admin: mọi phiếu. Menu không gắn quyền.',
        '– Chi tiết / In / Lịch sử mở được khi trong phạm vi HOẶC xem được phiếu nhập kho gốc; ngoài ra → trang 404.'],
     ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel', 'Lịch sử']),
    ('BR-02', 'Điều kiện tạo phiếu xuất lại', [
        '– Chỉ người tạo phiếu nhập kho, khi phiếu đang Không duyệt; không có ngoại lệ cho Super admin.',
        '– Kiểm cả lúc mở màn và lúc lưu; sai → thông báo, không lưu.'], ['Tạo phiếu xuất lại']),
    ('BR-03', 'Trừ tồn khi xuất lại', [
        '– Xuất toàn bộ lô của phiếu nhập kho, đúng vị trí, đúng lô nhập; không sửa số lượng.',
        '– Kiểm đủ tồn kho, tồn vị trí, tồn lô cho MỌI dòng trước rồi mới trừ; thiếu một dòng → không trừ gì.',
        '– Toàn bộ trong một lần lưu trọn gói.'], ['Tạo phiếu xuất lại']),
    ('BR-04', 'Vòng đời phiếu', [
        '– Tạo ra ở trạng thái Chờ nhập lại (vàng); lập phiếu nhập lại → Đã nhập lại (xanh lá). Không có trạng thái khác.',
        '– Không có Sửa / Xóa / Khóa / Duyệt / Hủy; điều kiện xóa: không áp dụng (màn không có Xóa).',
        '– Phiếu nhập kho gốc: Không duyệt → Đã xuất lại → Đã nhập lại.'], ['Tạo phiếu xuất lại', 'Tạo phiếu nhập lại']),
    ('BR-05', 'Điều kiện tạo phiếu nhập lại', [
        '– Nút Tạo phiếu nhập lại chỉ hiện với người tạo phiếu nhập kho gốc khi phiếu gốc đang Đã xuất lại.',
        '– Lưu (Đang tạo) hay Lưu và nhập đều chuyển phiếu xuất lại mới nhất của phiếu gốc sang Đã nhập lại.'],
     ['Tạo phiếu nhập lại', 'Xem danh sách', 'Xem chi tiết']),
    ('BR-06', 'Tính duy nhất và chống trùng', [
        '– Phiếu không có trường nhập duy nhất; mã PXL-NNNNN tự sinh tăng dần (giữ dãy mã của hệ thống cũ), không sửa được.',
        '– Một phiếu nhập kho chỉ xuất lại được 1 lần (sau đó đã Đã xuất lại); nút Xuất lại khóa khi đang lưu.'],
     ['Tạo phiếu xuất lại']),
    ('BR-07', 'Chuẩn hóa dữ liệu nhập', [
        '– Ghi chú tối đa 255 ký tự, không bắt buộc, không chặn ký tự đặc biệt, hiển thị nguyên văn.',
        '– Tìm kiếm / lọc chữ khớp một phần, không phân biệt hoa / thường, bỏ khoảng trắng đầu / cuối.'],
     ['Tạo phiếu xuất lại', 'Tìm kiếm và lọc']),
    ('BR-08', 'Liên kết cấp cha – con', [
        '– Phiếu xuất lại gắn đúng 1 phiếu nhập kho; công ty / phòng ban / bộ phận lấy theo phiếu nhập kho.',
        '– Phiếu > dòng hàng (hàng + đơn vị, tên / mã / model / thương hiệu lưu cố định lúc tạo) > dòng vị trí (Vị trí, SL).',
        '– Nhóm hàng của phiếu nhập kho được chép sang phiếu xuất lại.'], ['Tạo phiếu xuất lại', 'Xem chi tiết']),
    ('BR-09', 'In và xuất', [
        '– Bản in lấy letterhead theo công ty ghi trên phiếu, không theo người xem.',
        '– Xuất Excel không giới hạn số dòng, theo phạm vi xem; không có dòng thì không tạo file.'], ['In', 'Xuất Excel']),
    ('BR-10', 'Sử dụng ở màn khác', [
        '– Màn Phiếu nhập kho hiện liên kết “Phiếu xuất lại” tới phiếu mới nhất; Thẻ kho hiện dòng xuất PXL-… liên kết sang chi tiết.',
        '– Tồn ở các báo cáo tồn kho giảm, số xuất ở Tổng hợp xuất nhập tồn tăng theo phiếu.',
        '– Vị trí và hàng hóa đã có trên phiếu xuất lại không xóa được ở danh mục.',
        '– Dữ liệu dùng chung với hệ thống ERP: phiếu lập ở hệ thống cũ cũng hiện trên màn này.'],
     ['Tạo phiếu xuất lại', 'Tạo phiếu nhập lại']),
    ('BR-11', 'Quy tắc ghi lịch sử', [
        '– Tạo phiếu xuất lại → mốc “Tạo mới”; tạo phiếu nhập lại → mốc “Thay đổi trạng thái” Chờ nhập lại → Đã nhập lại kèm '
        'mã phiếu nhập kho mới.',
        '– Phiếu cũ chưa có mốc tạo → hiển thị mốc “Tạo mới” dựng theo người tạo, ngày tạo.',
        '– Xem, in, xuất Excel không ghi; hiển thị mới nhất ở trên.'], ['Tạo phiếu xuất lại', 'Tạo phiếu nhập lại', 'Lịch sử']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc hoặc ghi ngược dữ liệu của Phiếu xuất điều chỉnh sai số liệu (phiếu, dòng hàng, số lượng xuất '
    'theo từng vị trí / lô).')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Kho', 'Phiếu nhập kho (nút Tạo phiếu xuất lại khi phiếu Không duyệt; phiếu chuyển Đã xuất lại / Đã nhập lại; ô '
                 '“Phiếu xuất lại” liên kết tới phiếu mới nhất; nút Tạo phiếu nhập lại đổi phiếu xuất lại sang Đã nhập lại)',
     'Kho -> Nhập kho'),
    ('2', 'Tài chính', 'Phiếu nhập kho (cùng màn, mục menu ở phân hệ Tài chính)',
     'Tài chính -> Hàng hoá - Dịch vụ - Vận chuyển -> Nhập hàng'),
    ('3', 'Kho', 'Thẻ kho (dòng xuất của phiếu, số chứng từ PXL-… liên kết sang chi tiết phiếu xuất lại)', 'Kho -> Báo cáo kho'),
    ('4', 'Kho', 'Tổng hợp xuất nhập tồn (số xuất trong kỳ tăng theo phiếu)', 'Kho -> Báo cáo kho'),
    ('5', 'Kho', 'Báo cáo tồn kho chi tiết theo mặt hàng (tồn theo lô giảm)', 'Kho -> Báo cáo kho'),
    ('6', 'Kho', 'Báo cáo tồn kho tổng hợp theo mặt hàng (tồn giảm)', 'Kho -> Báo cáo kho'),
    ('7', 'Kho', 'Báo cáo tồn kho theo vị trí (tồn tại vị trí giảm)', 'Kho -> Báo cáo kho'),
    ('8', 'Kho', 'Báo cáo tồn theo kho (tồn của kho giảm)', 'Kho -> Báo cáo kho'),
    ('9', 'Kho', 'Vị trí (không xóa được vị trí đã có trên phiếu xuất lại)', 'Kho -> Danh mục'),
    ('10', 'Danh mục dùng chung', 'Hàng hoá, vật tư (không xóa được hàng hóa đã có trên phiếu xuất lại)',
     'Danh mục dùng chung -> Hàng hoá'),
], widths=[0.65, 1.2, 2.45, 2.2])

d.save()
