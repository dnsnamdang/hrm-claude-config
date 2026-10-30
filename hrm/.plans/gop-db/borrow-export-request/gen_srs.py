# -*- coding: utf-8 -*-
"""SRS màn "Yêu cầu xuất hàng mượn" (mã phiếu PYCXHM) — form chuẩn Danh mục quốc gia (30/10/2026).

Chạy: python gen_srs.py  → SRS - Yêu cầu xuất hàng mượn.docx
Khung: srs-documenter (SrsDoc, form 2026-09-24) + checklist ../../phieu-theo-form-quoc-gia/CHECKLIST.md
  (tác nhân ghi quyền, điều kiện ban đầu đánh số, vế "Chỉ bổ sung quy tắc riêng…", câu lỗi kiểm tra ở
  During, Use Case kiểu quốc gia chỉ cho chức năng thao tác + Xem chi tiết, Phần 5 màn tham chiếu).
Nguồn đọc 30/10/2026 (nhánh develop, cả 2 repo):
  BE  Modules/Finance/{Entities/BorrowExport/BorrowExportRequest*.php,
      Services/BorrowExportRequest{,History,Notify}Service.php, Services/BorrowStockService.php,
      Services/BorrowExportService.php, Http/Controllers/V1/BorrowExportRequestController.php,
      Http/Requests/BorrowExport/BorrowExportRequest*Request.php, Routes/api.php}
  FE  pages/finance/borrow-export-requests/**, components/subsystem-menu/{finance,sale-hub}.js
Ảnh: ./pycxhm_shots (dev-hrm 30/10/2026 bằng _capture/capture.js; ảnh cần phiếu Chờ duyệt / phiếu có lịch sử
  / phiếu mượn để chọn chụp trên local bằng _capture/capture_local.js vì dev không có dữ liệu đó).
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
from srs_split_rows import split_ui_rows  # noqa: E402  (tách dòng gộp: mỗi đối tượng 1 hàng)

TEN = 'Yêu cầu xuất hàng mượn'
SHOTS = os.path.join(HERE, 'pycxhm_shots')
ICONS = os.path.join(SHOTS, 'icons')
UML = os.path.join(SHOTS, 'uml')   # sơ đồ Use Case; HDSD dùng lại uml/overview.png
OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN)
os.makedirs(UML, exist_ok=True)


def shot(n):
    return os.path.join(SHOTS, n + '.png')


MENU = 'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng => Yêu cầu xuất hàng mượn'
MENU_SALE = 'Phân hệ Bán hàng => Yêu cầu => Hàng hóa => YC xuất hàng mượn'
RIENG = 'Chỉ bổ sung quy tắc riêng của màn Yêu cầu xuất hàng mượn.'
ERR = ('– Nếu có lỗi kiểm tra → gửi thông báo lỗi theo quy tắc thông báo chung '
       '(SRS_Các quy tắc chung_VN_1.0), không thực hiện bước After.')

A_LAP = 'Người lập phiếu'
A_KT = 'Kế toán kho'
TN_MOI = 'Người dùng có quyền thực hiện chức năng: mọi người dùng đã đăng nhập (không cần quyền riêng).'
TN_XEM = ('Người dùng có quyền thực hiện chức năng: người lập phiếu; người có quyền Kế toán kho; người có '
          'một trong các quyền Xem phiếu hàng mượn theo tổng công ty / theo công ty / theo phòng ban.')
TN_KT = 'Người dùng có quyền thực hiện chức năng: Kế toán kho.'
DK_XEM = '1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn danh sách Yêu cầu xuất hàng mượn.'

d = SrsDoc(out=OUT, menu=MENU, route='/finance/borrow-export-requests', full_url='', img_dir=UML)

d.set_menu_icons({k: os.path.join(ICONS, v + '.png') for k, v in {
    'Phân hệ Tài chính': 'menu_phanhe', 'Hàng hoá - Dịch vụ - Vận chuyển': 'menu_nhom',
    'Mượn hàng': 'menu_muonhang', 'Yêu cầu xuất hàng mượn': 'menu_muc',
    'Phân hệ Bán hàng': 'menu_phanhe_banhang', 'Yêu cầu': 'menu_yeucau', 'Hàng hóa': 'menu_hanghoa',
    'YC xuất hàng mượn': 'menu_muc_sale',
    'Tìm kiếm nâng cao': 'btn_timkiemnangcao', 'Cài đặt bộ lọc': 'btn_caidatboloc',
    'Cấu hình cột': 'btn_cauhinhcot', 'Tạo mới': 'btn_taomoi', 'Thêm phiếu': 'btn_themphieu',
    'Từ chối': 'btn_tuchoi', 'Tạo phiếu xuất hàng mượn': 'btn_taophieuxuat', 'In': 'btn_in',
    'Xuất Excel': 'btn_xuatexcel', 'Lịch sử': 'btn_lichsu_row',
}.items()})

# Mô tả riêng cho hàng sau khi tách dòng gộp (srs_split_rows) — mỗi đối tượng 1 hàng.
UI_OVER = {
    'Cột Người cập nhật': {'scope': '–', 'desc': ['- Người sửa phiếu gần nhất, dạng “Họ tên - Mã phòng ban”',
                                                 '- Ẩn mặc định; bật trong cửa sổ Tùy chỉnh cột']},
    'Cột Ngày cập nhật': ['- Thời điểm sửa phiếu gần nhất', '- Ẩn mặc định; bật trong cửa sổ Tùy chỉnh cột'],
    ('Nút Tìm kiếm / Làm mới', 'Nút Tìm kiếm'): 'Lọc theo Mã phiếu xuất mượn đã nhập, về trang 1.',
    ('Nút Tìm kiếm / Làm mới', 'Nút Làm mới'): 'Xóa ô Mã phiếu xuất mượn, nạp lại danh sách.',
}
UI_EXPLICIT = {}

_uc_n = [0]


def uc(code, name, group, actor):
    """Biểu đồ Use Case 1 chức năng theo khổ mẫu quốc gia (actor + 1 use case)."""
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None):
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
    if 'entries' in layout:     # màn nhiều lối vào: mỗi lối vào 1 dòng Menu + phạm vi hiển thị
        d.p('Đường dẫn màn hình:')
        for m, note in layout['entries']:
            d._menu_para(m)
            d.p(note)
        d.figure(layout['shot'], layout['shot_caption'], width_in=6.2)
    else:
        d.layout(**layout)
    k += 1
    assert ui and ev, 'Thiếu bảng giao diện / event ở 2.%d' % no
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (no, k))
    d.ui_table(split_ui_rows(ui, UI_OVER, UI_EXPLICIT), **(ui_kw or {}))
    k += 1
    d.p('2.%d.%d Danh sách event và xử lý event' % (no, k))
    d.event_table(ev)


# ============================================================== TRANG ĐẦU
d.title_block(TEN)
d.h2('Mục lục')
d.toc()

# ============================================================== PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn hình Yêu cầu xuất hàng mượn (mã phiếu PYCXHM), nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu chức năng, phân quyền và luồng xử lý của màn hình.',
    'Làm rõ cách người đang mượn hàng gom các phiếu mượn liên quan vào một phiếu để xin Kế toán kho '
    'tất toán phần hàng KHÔNG trả lại mà xuất hẳn.',
    'Làm rõ cách hệ thống tính số lượng còn “Đang mượn” được phép xuất và các điều kiện chặn khi gửi.',
    'Làm rõ phạm vi dữ liệu theo từng cấp quyền và hai lối vào của màn hình.',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Phiếu yêu cầu xuất hàng mượn', 'Phiếu PYCXHM-NNNNN của màn này: đề nghị Kế toán kho xuất hẳn một phần '
                                    'hàng đang mượn (không trả lại nữa).'),
    ('Phiếu xuất mượn (phiếu mượn)', 'Phiếu yêu cầu xuất hàng loại Xuất mượn (mã PYCXH-…) đã xuất kho cho '
                                    'người mượn, đang ở trạng thái Đã mượn.'),
    ('Đang mượn', 'Số lượng của một mặt hàng trên một phiếu mượn còn được phép xuất: đã xuất − đã trả − phần '
                  'đang chờ xử lý ở các phiếu khác (trả hàng, xuất bán hàng mượn, xuất hàng mượn) chưa duyệt, '
                  'quy theo đơn vị tính đang chọn và làm tròn xuống.'),
    ('Phiếu xuất hàng mượn', 'Chứng từ PXHM-NNNNN do Kế toán kho lập từ phiếu yêu cầu này. Lập phiếu xuất '
                             'chính là thao tác DUYỆT phiếu yêu cầu.'),
    ('Kế toán kho', 'Người có quyền Kế toán kho — vai trò duy nhất duyệt hoặc từ chối phiếu.'),
    ('Chờ duyệt / Đã duyệt / Không duyệt', 'Ba trạng thái của phiếu. Phiếu gửi đi là vào thẳng Chờ duyệt '
                                           '(không có bản nháp). Không duyệt là trạng thái cuối.'),
], widths=[1.9, 4.1])

# ============================================================== PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Lập phiếu không cần quyền riêng: mọi người dùng đã đăng nhập lập được phiếu cho các phiếu mượn do chính '
    'mình lập. Màn không có chức năng Sửa / Xóa ở bất kỳ trạng thái nào.')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('Q1', 'Kế toán kho',
     'Thấy dữ liệu ở lối vào của Kế toán kho; xem mọi phiếu đã gửi; với phiếu Chờ duyệt: hiện nút Tạo phiếu '
     'xuất hàng mượn (duyệt) và Từ chối, nút Duyệt trên dòng; nhận thông báo khi có phiếu mới cùng công ty.'),
], widths=[0.8, 1.6, 3.6])
d.p('Nhóm quyền quyết định phạm vi dữ liệu (xét từ trên xuống, có cấp nào áp cấp đó):')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem phiếu hàng mượn theo tổng công ty', 'Toàn bộ phiếu của mọi công ty.'),
    ('V2', 'Xem phiếu hàng mượn theo công ty', 'Phiếu thuộc công ty của người đăng nhập + phiếu mình lập.'),
    ('V3', 'Xem phiếu hàng mượn theo phòng ban',
     'Phiếu thuộc các phòng ban người đăng nhập quản lý + phiếu mình lập.'),
    ('—', '(không có quyền nào)', 'Chỉ phiếu do chính mình lập.'),
], widths=[0.8, 2.2, 3.0])
d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'Q1', 'V1', 'V2', 'V3', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-02 Tìm kiếm và lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-03 Cài đặt bộ lọc', '✅', '✅', '✅', '✅', '✅'),
    ('FR-04 Tùy chỉnh cột hiển thị', '✅', '✅', '✅', '✅', '✅'),
    ('FR-05 Lập phiếu', '✅', '✅', '✅', '✅', '✅'),
    ('FR-06 Chọn phiếu xuất mượn', '✅', '✅', '✅', '✅', '✅ (phiếu mượn của mình)'),
    ('FR-07 Xem chi tiết phiếu', '✅', '✅', '✅ (cùng công ty)', '✅ (phòng ban quản lý)', '✅ (phiếu của mình)'),
    ('FR-08 Từ chối phiếu', '✅ (Chờ duyệt)', '❌', '❌', '❌', '❌'),
    ('FR-09 Tạo phiếu xuất hàng mượn (duyệt)', '✅ (Chờ duyệt)', '❌', '❌', '❌', '❌'),
    ('FR-10 In phiếu / In danh sách', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-11 Xuất Excel', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
    ('FR-12 Xem lịch sử thay đổi', '✅', '✅', '✅', '✅', '✅ (phiếu của mình)'),
], widths=[2.0, 0.9, 0.6, 0.85, 0.95, 1.0])

# ============================================================== PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_LAP, [0, 1, 4, 5]), (A_KT, [0, 2, 3, 4, 5])],
    [('FR-01', 'Xem danh sách phiếu', 'view'),
     ('FR-05', 'Lập phiếu', 'crud'),
     ('FR-08', 'Từ chối phiếu', 'action'),
     ('FR-09', 'Tạo phiếu xuất hàng mượn', 'action'),
     ('FR-10', 'In phiếu / In danh sách', 'io'),
     ('FR-11', 'Xuất Excel', 'io')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột hiển thị', 'view', 'extend', [0], None),
     ('FR-07', 'Xem chi tiết phiếu', 'view', 'extend', [0], None),
     ('FR-12', 'Xem lịch sử thay đổi', 'view', 'extend', [0], None),
     ('FR-06', 'Chọn phiếu xuất mượn', 'crud', 'extend', [1], None)],
    'Sơ đồ Use Case tổng quan màn Yêu cầu xuất hàng mượn')

d.h2('2 Đặc tả chi tiết từng chức năng')

# ------------------------------------------------------------ 2.1
fr(1, 'Xem danh sách phiếu',
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'),
   intro=dict(
       ten='Truy cập và xem danh sách phiếu yêu cầu xuất hàng mượn',
       mota='Hiển thị các phiếu trong phạm vi dữ liệu của người đăng nhập. Màn có hai lối vào: lối vào chung '
            '(phân hệ Bán hàng) và lối vào của Kế toán kho (phân hệ Tài chính).',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.',
       chinh='1. Người dùng vào màn theo một trong hai lối vào ở mục Layout.\n'
             '2. Hệ thống xác định lối vào và phạm vi dữ liệu theo quyền.\n'
             '3. Hệ thống hiển thị trang đầu 10 dòng, mới tạo xếp trên, kèm tổng số phiếu.',
       phu='• Lối vào Kế toán kho mà người dùng không có quyền Kế toán kho → bảng không có dữ liệu.\n'
           '• Phiếu Đang tạo (dữ liệu cũ) của người khác không bao giờ hiện.\n'
           '• Đang ở màn, bấm sang lối vào còn lại → danh sách tự nạp lại theo lối vào mới, về trang 1.',
       dacbiet=None),
   layout=dict(entries=[
       (MENU_SALE, 'Hiển thị: tiêu đề “Yêu cầu xuất hàng mượn”; phiếu trong phạm vi quyền (V1/V2/V3, không có '
                   'quyền thì phiếu của mình); Kế toán kho thấy mọi phiếu đã gửi.'),
       (MENU, 'Hiển thị: tiêu đề “Yêu cầu xuất hàng mượn (Kế toán kho)”; chỉ người có quyền Kế toán kho thấy dữ '
              'liệu — mọi phiếu đã gửi (Chờ duyệt, Đã duyệt, Không duyệt).')],
       shot=shot('01_list'), shot_caption='Màn danh sách Yêu cầu xuất hàng mượn'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Theo lối vào',
        ['- Lối vào chung: “Yêu cầu xuất hàng mượn”', '- Lối vào Kế toán kho: “Yêu cầu xuất hàng mượn (Kế toán kho)”']),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị', 'Mở màn Thêm yêu cầu xuất hàng mượn (FR-05).'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ xem trước bản in danh sách (FR-10).'),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        'Mở cửa sổ Chọn trường xuất Excel (FR-11); khóa trong lúc đang xuất.'),
       ('Nút Cấu hình cột hiển thị', 'Button', 'Enable', '–', 'Hiển thị', 'Mở cửa sổ Tùy chỉnh cột (FR-04).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Đánh số liên tục theo trang; cột khóa, luôn hiện.'),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PYCXHM-NNNNN', 'Hiển thị',
        ['- Bấm mã → mở màn chi tiết (FR-07)', '- Sắp xếp được; cột khóa, luôn hiện']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', 'Dạng “Họ tên - Mã phòng ban”.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', 'Sắp xếp được.'),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Chờ duyệt: nhãn màu cam', '- Đã duyệt: nhãn màu xanh lá', '- Không duyệt: nhãn màu đỏ']),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        'Kế toán kho đã duyệt hoặc đã từ chối; trống khi phiếu còn Chờ duyệt.'),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị', 'Sắp xếp được.'),
       ('Cột Người cập nhật / Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn',
        'Bật trong cửa sổ Tùy chỉnh cột.'),
       ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Ẩn', 'Phòng ban của người lập lúc lập phiếu.'),
       ('Cột Ghi chú', 'Table/Grid', 'Read-only', '0–255 ký tự', 'Ẩn', 'Ghi chú người lập nhập.'),
       ('Cột Lý do từ chối', 'Table/Grid', 'Read-only', '0–255 ký tự', 'Ẩn', 'Lý do Kế toán kho nhập khi từ chối.'),
       ('Cột Hành động', 'Table/Grid', 'Read-only', '–', 'Hiển thị', [
           '- Nút Duyệt: chỉ hiện với Kế toán kho khi phiếu Chờ duyệt; bấm → mở màn chi tiết để duyệt',
           '- Nút In: mở bản xem trước phiếu (FR-10)',
           '- Nút Lịch sử: mở cửa sổ Lịch sử thay đổi (FR-12)']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang', '- N: tổng số phiếu khớp bộ lọc trong phạm vi quyền']),
       ('Phân trang', 'Pagination', 'Enable', '5 / 10 / 20 / 50 / 100', 'Trang 1, 10 dòng',
        'Nút về đầu, lùi, số trang, tiến, về cuối và ô Số dòng/trang.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định lối vào: chung hoặc Kế toán kho; giá trị lạ coi là lối vào chung.\n'
        'During:\n– Lối vào chung: áp phạm vi V1 → V2 → V3 → phiếu của mình; Kế toán kho thấy mọi phiếu đã gửi.\n'
        '– Lối vào Kế toán kho: người có quyền thấy mọi phiếu đã gửi; không có quyền thì rỗng.\n'
        '– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất.\n'
        'After:\n– Hiển thị trang 1, sắp theo Ngày tạo mới nhất.'),
       ('Bấm Mã phiếu', 'Click', 'After:\n– Mở màn chi tiết phiếu (FR-07).'),
       ('Bấm tiêu đề cột Mã phiếu / Ngày tạo / Ngày duyệt', 'Click',
        'After:\n– Sắp xếp tăng / giảm theo cột, nạp lại từ trang 1, giữ bộ lọc.'),
       ('Đổi trang / số dòng mỗi trang', 'Click',
        'After:\n– Nạp lại dữ liệu; đổi số dòng thì về trang 1.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu',
       mota='Thu hẹp danh sách theo mã phiếu, trạng thái, người tạo, người duyệt, hàng hóa, ngày tạo và '
            'công ty – phòng ban.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng nhập mã phiếu vào ô tìm nhanh rồi bấm Tìm kiếm, hoặc bấm Tìm kiếm nâng cao.\n'
             '2. Người dùng chọn / nhập các tiêu chí lọc.\n'
             '3. Hệ thống nạp lại danh sách và cập nhật tổng số phiếu.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí, bỏ sắp xếp, nạp lại từ trang 1, giữ nguyên lối vào.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm kiếm theo mã phiếu”', '- Chỉ tìm theo mã phiếu, chạy khi bấm Tìm kiếm']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Áp ô tìm nhanh, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Xóa mọi tiêu chí và sắp xếp.'),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn', 'Mở / đóng các ô lọc nâng cao.'),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Cài đặt bộ lọc (FR-03).'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống', 'Chỉ hiện với V1.'),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Không', 'Trống',
        ['- Hiện với V1, V2, V3', '- Phụ thuộc Công ty; đổi công ty thì xóa phòng ban đã chọn']),
       ('Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Mã phiếu chứa chuỗi nhập.'),
       ('Trạng thái', 'Dropdown', 'Enable', 'Chờ duyệt, Đã duyệt, Không duyệt', 'Không', 'Trống', '–'),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Người lập phiếu.'),
       ('Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống', 'Kế toán kho đã xử lý phiếu.'),
       ('Mã hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Phiếu có dòng hàng mã chứa chuỗi nhập.'),
       ('Tên hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Phiếu có dòng hàng tên chứa chuỗi nhập.'),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        'Một ô chọn từ ngày → đến ngày, lấy trọn hai đầu.'),
   ],
   ev=[
       ('Đổi giá trị một ô lọc nâng cao', 'Change', 'After:\n– Về trang 1 và nạp lại danh sách ngay.'),
       ('Bấm Tìm kiếm', 'Click', 'After:\n– Áp ô tìm nhanh, về trang 1, nạp lại danh sách.'),
       ('Bấm Làm mới', 'Click', 'After:\n– Xóa mọi tiêu chí, bỏ sắp xếp, nạp lại từ trang 1.'),
       ('Chọn lại Công ty', 'Change', 'After:\n– Xóa Phòng ban đã chọn và nạp danh sách phòng ban của công ty mới.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị', mota='Bật / tắt và sắp thứ tự các ô lọc; lưu riêng theo người dùng.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n2. Hệ thống mở cửa sổ Cài đặt bộ lọc với 8 ô lọc.\n'
             '3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Lưu.\n4. Hệ thống lưu và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → trả về danh sách và thứ tự ban đầu.\n• Bấm Đóng → bỏ thay đổi.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Danh sách ô lọc', 'Table/Grid', 'Enable', '8 mục', '–', 'Theo cấu hình đã lưu',
        'Công ty – Phòng ban, Mã phiếu, Trạng thái, Người tạo, Người duyệt, Mã hàng hóa, Tên hàng hóa, Ngày tạo.'),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', '–', 'Đang tích', 'Bỏ tích thì ô lọc không hiện.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Trả về cấu hình ban đầu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, bỏ thay đổi chưa lưu.'),
   ],
   ev=[
       ('Kéo đổi vị trí một mục', 'Drag', 'After:\n– Cập nhật thứ tự; chỉ lưu khi bấm Lưu.'),
       ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình theo người dùng, vẽ lại khối lọc.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Bật / tắt và kéo sắp xếp 13 cột; cột STT, Mã phiếu, Hành động bị khóa.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n2. Hệ thống mở cửa sổ Tùy chỉnh cột.\n'
             '3. Người dùng tích / bỏ tích, kéo đổi thứ tự rồi bấm Lưu.\n4. Hệ thống lưu và vẽ lại bảng.',
       phu='• Bấm Đóng → bỏ thay đổi.',
       dacbiet='Mặc định ẩn 5 cột: Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Danh sách cột', 'Table/Grid', 'Enable', '13 cột', '–', 'Theo cấu hình đã lưu',
        'STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, '
        'Phòng ban, Ghi chú, Lý do từ chối, Hành động.'),
       ('Cột bị khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích', 'STT, Mã phiếu, Hành động — có biểu tượng ổ khóa.'),
       ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Tích / bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/13 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình', 'Số cột đang tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, bỏ thay đổi.'),
   ],
   ev=[
       ('Kéo biểu tượng ba gạch', 'Drag', 'After:\n– Đổi thứ tự cột trong danh sách.'),
       ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình, vẽ lại bảng theo cột đã chọn.'),
   ])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu yêu cầu xuất hàng mượn', usecase=('FR-05', 'Lập phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu yêu cầu xuất hàng mượn',
       mota='Gom một hoặc nhiều phiếu mượn của chính người lập, chọn mặt hàng và số lượng xuất hẳn, gửi Kế '
            'toán kho duyệt. Phiếu không có bản nháp.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n'
                '2. Người dùng có ít nhất 1 phiếu xuất mượn đủ điều kiện (BR-01).',
       chinh='1. Người dùng bấm Tạo mới ở màn danh sách.\n'
             '2. Hệ thống mở màn “Thêm yêu cầu xuất hàng mượn”.\n'
             '3. Người dùng bấm Thêm phiếu, chọn một hoặc nhiều phiếu xuất mượn (FR-06).\n'
             '4. Người dùng nhập Ghi chú, đính kèm ít nhất 1 file PDF.\n'
             '5. Người dùng bấm nút + ở bảng Chi tiết, chọn hàng hóa trong cửa sổ Thêm hàng hoá.\n'
             '6. Với mỗi hàng, người dùng chọn Đơn vị tính và nhập số Xuất theo từng phiếu mượn.\n'
             '7. Người dùng bấm Gửi duyệt, xác nhận ở hộp “Xác nhận gửi duyệt”.\n'
             '8. Hệ thống kiểm tra, sinh mã phiếu, lưu phiếu ở trạng thái Chờ duyệt.\n'
             '9. Hệ thống ghi nhận “Tạo mới” trong lịch sử và gửi thông báo cho Kế toán kho cùng công ty.\n'
             '10. Hệ thống báo “Yêu cầu của bạn đã được gửi.” và quay về màn danh sách.',
       phu='• Lỗi kiểm tra → báo đỏ ngay dưới ô lỗi kèm thông báo “Bạn chưa nhập đầy đủ thông tin.”, không gửi.\n'
           '• Bấm Lưu và tiếp tục → gửi duyệt như trên rồi ở lại màn Thêm mới với form trống.\n'
           '• Hàng thêm vào không có trên phiếu mượn nào đã chọn → dòng bị khóa, ghi “Chưa có phiếu mượn”, '
           'không nhập số lượng và không được gửi đi.\n'
           '• Bỏ một phiếu mượn (dấu ×) → các dòng hàng giữ nguyên, chỉ mất phần chi tiết của phiếu đó.\n'
           '• Bấm Hủy ở hộp xác nhận → ở lại màn, dữ liệu giữ nguyên.\n'
           '• Bấm Quay lại / rời màn khi chưa nhập gì → về danh sách; đã nhập → hỏi xác nhận rời trang.',
       dacbiet='Công ty, phòng ban của phiếu lấy theo người lập tại thời điểm lập. Số lượng “Đang mượn” tính '
               'lại ở máy chủ lúc gửi, không tin số trên màn hình (BR-02).'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'),
               shot_caption='Màn Thêm yêu cầu xuất hàng mượn đã nhập dữ liệu'),
   ui=[
       ('Người lập – Ngày lập', 'Label', 'Read-only', '–', '–', 'Người đăng nhập – thời điểm hiện tại',
        'Góc phải khối Thông tin chung.'),
       ('Phiếu xuất mượn', 'Table/Grid', 'Enable', 'Ít nhất 1 phiếu', 'Có', '“Chưa chọn phiếu xuất mượn”',
        ['- Mỗi phiếu đã chọn là 1 thẻ mã kèm dấu × để bỏ', '- Lỗi: “Bắt buộc phải chọn ít nhất 1 phiếu xuất mượn”']),
       ('Nút Thêm phiếu', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Mở cửa sổ Chọn phiếu xuất mượn (FR-06).'),
       ('Ghi chú', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống',
        ['- Gợi ý “Nhập lý do xuất số hàng đang mượn này...”', '- Lỗi: “Bắt buộc phải nhập”']),
       ('File đính kèm', 'Table/Grid', 'Enable', 'Chỉ PDF, tối đa 20 MB / file', 'Có', 'Chưa có file',
        ['- Nút Thêm tài liệu; bảng STT, Upload / File, Dung lượng', '- File tải lên ngay khi chọn, xem / gỡ được',
         '- Lỗi: “Bắt buộc phải đính kèm ít nhất 1 file”']),
       ('Nút + (Thêm hàng hóa)', 'Button', 'Enable', '–', '–', 'Hiển thị',
        'Đầu cột cuối bảng Chi tiết; mở cửa sổ Thêm hàng hoá (chỉ hàng hóa thật trong danh mục, chọn nhiều).'),
       ('Cột Tên hàng hóa', 'Table/Grid', 'Read-only', '–', '–', 'Theo hàng đã chọn', 'Tên kèm Model, Mã, Thương hiệu.'),
       ('Cột Đơn vị tính', 'Dropdown', 'Enable', 'Đơn vị của hàng', 'Có', 'Đơn vị đầu tiên',
        ['- Đơn vị khác 1 hiện kèm hệ số, ví dụ “Thùng (x24)”', '- Đổi đơn vị → tính lại Đơn giá, Đang mượn; số Xuất '
         'vượt Đang mượn thì tự kéo về bằng Đang mượn']),
       ('Cột Đơn giá', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo đơn vị tính', 'Định dạng 1,234,567.'),
       ('Cột Số lượng xuất', 'Table/Grid', 'Read-only', '≥ 0', '–', '0', 'Tổng số Xuất của các phiếu mượn trên dòng.'),
       ('Cột Phiếu mượn', 'Table/Grid', 'Read-only', 'PYCXH-…', '–', 'Theo dữ liệu',
        'Mỗi phiếu mượn có hàng này 1 dòng con; bấm mã → mở chi tiết phiếu mượn ở tab mới.'),
       ('Cột Đang mượn', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu', 'Cách tính: BR-02.'),
       ('Cột Xuất', 'Textbox', 'Enable', 'Số nguyên 0 – Đang mượn', 'Có', '0', [
           '- Lỗi “Không hợp lệ” / “Phải lớn hơn hoặc bằng 0” / “Không được vượt quá 6 chữ số” / “Vượt quá số đang mượn”',
           '- Cả dòng hàng chưa có số Xuất > 0: “Chưa nhập số lượng xuất”']),
       ('Dòng bị khóa', 'Table/Grid', 'Disable', '–', '–', 'Ẩn',
        'Hàng không có trên phiếu mượn nào đã chọn: tô mờ, 3 ô chi tiết gộp thành “Chưa có phiếu mượn”.'),
       ('Cột Thành tiền', 'Table/Grid', 'Read-only', '≥ 0', '–', '0', 'Số lượng xuất × Đơn giá.'),
       ('Nút Xóa dòng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Bỏ dòng hàng khỏi phiếu.'),
       ('Dòng Tổng cộng', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Ẩn khi chưa có hàng', 'Tổng số lượng và tổng tiền.'),
       ('Thông báo dưới bảng', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        '“Chưa có hàng hoá nào để xuất.” khi không có dòng nào nhập được.'),
       ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khóa trong lúc đang gửi.'),
       ('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Gửi duyệt rồi mở form trống.'),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Về màn danh sách.'),
   ],
   ev=[
       ('Bấm Thêm tài liệu, chọn file', 'Click',
        'During:\n– Không phải PDF / quá 20 MB → báo lỗi, không nhận file.\n'
        'After:\n– Tải file lên, hiện tên và dung lượng.'),
       ('Nhập số Xuất', 'Change', 'During:\n– Kiểm tra số nguyên, ≥ 0, ≤ 999999, ≤ Đang mượn; sai → báo đỏ dưới ô.'),
       ('Bấm Gửi duyệt / Lưu và tiếp tục', 'Click',
        'Before:\n– Không cần quyền riêng.\n'
        'During:\n– Thiếu phiếu xuất mượn / Ghi chú / file, hoặc không có dòng nhập được → báo đỏ tại ô, '
        'thông báo “Bạn chưa nhập đầy đủ thông tin.”.\n'
        '– Hiện hộp “Xác nhận gửi duyệt”: “Gửi duyệt phiếu yêu cầu xuất hàng mượn này? Sau khi gửi, phiếu không '
        'sửa được nữa.”; bấm Hủy thì dừng.\n'
        '– Máy chủ kiểm tra lại: phiếu mượn không còn hợp lệ → “Có yêu cầu xuất mượn không hợp lệ!”; vượt số '
        'đang mượn → “Số lượng vượt quá số đang mượn (n).”; hàng chưa nhập số → “Hàng hoá “<tên>” chưa nhập số '
        'lượng xuất.”; tổng bằng 0 → “Chưa có hàng hoá nào để xuất.”.\n' + ERR + '\n'
        'After:\n– Sinh mã PYCXHM-NNNNN, lưu phiếu ở trạng thái Chờ duyệt.\n'
        '– Ghi nhận “Tạo mới” trong lịch sử.\n'
        '– Gửi thông báo “[YCXHM] Chờ duyệt: <mã>” (số mặt hàng, tổng tiền, người lập, ghi chú) cho Kế toán kho '
        'cùng công ty.\n'
        '– Báo “Yêu cầu của bạn đã được gửi.”; Gửi duyệt → về danh sách, Lưu và tiếp tục → form trống.'),
       ('Bấm Quay lại / rời màn', 'Click',
        'Before:\n– Có dữ liệu chưa gửi → hỏi xác nhận rời trang.\nAfter:\n– Về màn danh sách.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn phiếu xuất mượn', usecase=('FR-06', 'Chọn phiếu xuất mượn', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn phiếu xuất mượn đưa vào phiếu yêu cầu',
       mota='Cửa sổ liệt kê các phiếu mượn đủ điều kiện của chính người lập để chọn từng phiếu.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng đang ở màn Thêm yêu cầu xuất hàng mượn.',
       chinh='1. Người dùng bấm Thêm phiếu.\n2. Hệ thống mở cửa sổ “Chọn phiếu xuất mượn” (10 phiếu / trang).\n'
             '3. Người dùng tìm theo mã nếu cần, bấm vào dòng phiếu.\n'
             '4. Hệ thống nạp hàng còn mượn của phiếu, thêm thẻ mã vào ô Phiếu xuất mượn, báo “Thêm thành công.”.',
       phu='• Bấm phiếu đã chọn → “Phiếu này đã được chọn.”.\n'
           '• Phiếu vừa hết điều kiện → “Không thể chọn phiếu này: phiếu không phải phiếu xuất mượn đang mượn của bạn.”.\n'
           '• Không có phiếu → “Không có phiếu xuất mượn phù hợp.”.',
       dacbiet='Chọn phiếu chỉ nạp dữ liệu cho các dòng hàng; bảng Chi tiết không tự sinh dòng.'),
   layout=dict(menu=MENU + ' => Tạo mới => Thêm phiếu', shot=shot('11_picker'),
               shot_caption='Cửa sổ Chọn phiếu xuất mượn',
               note='Modal Chọn phiếu xuất mượn được mở ngay trên màn hình Thêm yêu cầu xuất hàng mượn theo đường dẫn ở trên.'),
   ui=[
       ('Dòng mô tả', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Chỉ hiện phiếu yêu cầu xuất hàng loại Xuất mượn do bạn lập, đang ở trạng thái Đã mượn và còn hàng chưa trả hết”.'),
       ('Mã phiếu xuất mượn', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống', 'Gợi ý “Nhập mã phiếu xuất mượn”.'),
       ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Lọc theo mã / xóa điều kiện.'),
       ('Bảng phiếu', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', [
           '- Cột STT, Mã phiếu xuất mượn, Ngày tạo, Trạng thái', '- Trạng thái “Bấm để chọn” hoặc “Đã chọn”',
           '- Mới tạo xếp trên']),
       ('Phân trang', 'Pagination', 'Enable', '–', '–', 'Trang 1, 10 dòng', '–'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ.'),
   ],
   ev=[
       ('Mở cửa sổ', 'System', 'After:\n– Lấy phiếu mượn đủ điều kiện (BR-01) của người đăng nhập.'),
       ('Bấm Tìm kiếm', 'Click', 'After:\n– Lọc theo mã, về trang 1.'),
       ('Bấm một dòng phiếu', 'Click',
        'During:\n– Phiếu đã chọn → “Phiếu này đã được chọn.”, dừng.\n'
        '– Phiếu không còn hợp lệ → báo lỗi.\n' + ERR + '\n'
        'After:\n– Thêm thẻ mã, nạp hàng còn mượn của phiếu vào các dòng hàng đã có, báo “Thêm thành công.”.'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Xem chi tiết phiếu', usecase=('FR-07', 'Xem chi tiết phiếu', 'view', A_LAP),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu yêu cầu xuất hàng mượn',
       mota='Xem toàn bộ thông tin phiếu ở chế độ chỉ đọc, kèm các nút thao tác theo quyền và trạng thái.',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng được xem phiếu (BR-04).',
       chinh='1. Người dùng bấm Mã phiếu ở danh sách (hoặc nút Duyệt trên dòng, hoặc thông báo).\n'
             '2. Hệ thống mở màn “Chi tiết yêu cầu xuất hàng mượn: <mã>”.',
       phu='• Phiếu không tồn tại → “Không tìm thấy dữ liệu”, về danh sách.\n'
           '• Không được xem → “Bạn không có quyền xem phiếu này”, về danh sách.\n'
           '• Bấm Quay lại → về màn trước đó; mở thẳng bằng thông báo / tab mới → về danh sách.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'),
               shot_caption='Màn chi tiết phiếu đang Chờ duyệt (tài khoản Kế toán kho)'),
   ui_kw=dict(required=False),
   ui=[
       ('Người lập – Ngày lập', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Góc phải khối Thông tin chung.'),
       ('Phiếu xuất mượn', 'Label', 'Read-only', '–', 'Theo dữ liệu', 'Thẻ mã từng phiếu mượn; bấm → mở ở tab mới.'),
       ('Ghi chú', 'Textarea', 'Read-only', '0–255 ký tự', 'Theo dữ liệu', '–'),
       ('Phòng ban yêu cầu', 'Textbox', 'Read-only', '–', 'Theo dữ liệu', 'Phòng ban của người lập lúc lập.'),
       ('File đính kèm', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', 'STT, tên file (xem / tải), Dung lượng.'),
       ('Bảng Chi tiết', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Cột STT, Tên hàng hóa, Đơn vị tính, Đơn giá, Số lượng, Phiếu mượn, Xuất, Được duyệt, Thành tiền',
           '- Được duyệt: số Kế toán kho chấp nhận khi lập phiếu xuất; 0 khi chưa duyệt', '- Dòng Tổng cộng']),
       ('Khối Ghi chú duyệt', 'Textarea', 'Read-only', '–', 'Ẩn', 'Chỉ hiện khi phiếu có lý do từ chối.'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn', 'Bấm Xem lịch sử để mở (FR-12).'),
       ('Nút Tạo phiếu xuất hàng mượn', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Chỉ Kế toán kho, phiếu Chờ duyệt (FR-09).'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Mở bản xem trước phiếu (FR-10).'),
       ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn', 'Chỉ Kế toán kho, phiếu Chờ duyệt (FR-08).'),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', 'Về màn trước đó.'),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra quyền xem (BR-04); không được xem → “Bạn không có quyền xem phiếu này”.\n'
        'After:\n– Hiển thị dữ liệu; nút Tạo phiếu xuất hàng mượn / Từ chối chỉ hiện khi đủ điều kiện.'),
       ('Bấm mã phiếu mượn', 'Click', 'After:\n– Mở chi tiết phiếu yêu cầu xuất hàng ở tab mới.'),
       ('Bấm Quay lại', 'Click', 'After:\n– Về màn trước đó (mặc định màn danh sách).'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'Từ chối phiếu', usecase=('FR-08', 'Từ chối phiếu', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Từ chối phiếu yêu cầu xuất hàng mượn',
       mota='Kế toán kho không duyệt phiếu, bắt buộc nêu lý do. Phiếu sang Không duyệt và dừng hẳn.',
       tacnhan=TN_KT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán kho.\n'
                '3. Phiếu đang ở trạng thái Chờ duyệt.',
       chinh='1. Kế toán kho bấm Từ chối ở màn chi tiết.\n'
             '2. Hệ thống mở cửa sổ “Từ chối yêu cầu xuất hàng mượn”.\n'
             '3. Kế toán kho nhập Lý do từ chối, bấm Xác nhận từ chối.\n'
             '4. Hệ thống chuyển phiếu sang Không duyệt, lưu lý do, người và thời điểm từ chối.\n'
             '5. Hệ thống ghi nhận “Không duyệt” kèm lý do trong lịch sử, thông báo cho người lập.\n'
             '6. Hệ thống báo “Thao tác thành công.” và quay về màn danh sách đã mở trước đó.',
       phu='• Lý do trống → “Bắt buộc phải nhập lý do từ chối”, cửa sổ không đóng.\n'
           '• Phiếu vừa được xử lý ở nơi khác → “Phiếu không còn ở trạng thái Chờ duyệt hoặc bạn không đủ quyền.”.\n'
           '• Bấm Đóng / dấu × → đóng cửa sổ, không lưu.',
       dacbiet='Phiếu Không duyệt không sửa, không gửi lại được; người lập phải lập phiếu mới.'),
   layout=dict(menu=MENU + ' => Xem chi tiết => Từ chối', shot=shot('15_reject'),
               shot_caption='Cửa sổ Từ chối yêu cầu xuất hàng mượn',
               note='Modal Từ chối yêu cầu xuất hàng mượn được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '–', '“Từ chối yêu cầu xuất hàng mượn”, kèm “Mã phiếu: <mã>”.'),
       ('Lý do từ chối', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống',
        ['- Gợi ý “Nhập lý do không duyệt phiếu...”', '- Lỗi: “Bắt buộc phải nhập lý do từ chối”']),
       ('Dòng nhắc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '“Phiếu sẽ chuyển sang trạng thái Không duyệt và không sửa lại được.”'),
       ('Nút Xác nhận từ chối', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Màu đỏ; khóa khi đang xử lý.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng cửa sổ, bỏ nội dung đã nhập.'),
   ],
   ev=[
       ('Bấm Xác nhận từ chối', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán kho và phiếu còn Chờ duyệt; sai → “Phiếu không còn ở trạng thái Chờ '
        'duyệt hoặc bạn không đủ quyền.”.\n'
        'During:\n– Lý do trống → “Bắt buộc phải nhập lý do từ chối”; quá 255 ký tự → “Không được vượt quá 255 ký tự”.\n'
        + ERR + '\n'
        'After:\n– Chuyển phiếu sang Không duyệt, lưu lý do, người duyệt, ngày duyệt.\n'
        '– Ghi nhận “Không duyệt” (Trạng thái: Chờ duyệt → Không duyệt, kèm lý do) trong lịch sử.\n'
        '– Gửi thông báo “[YCXHM] Từ chối: <mã>” (người từ chối, lý do) cho người lập.\n'
        '– Báo “Thao tác thành công.”, quay về màn danh sách.'),
       ('Bấm Đóng', 'Click', 'After:\n– Đóng cửa sổ, không lưu.'),
   ])

# ------------------------------------------------------------ 2.9
fr(9, 'Tạo phiếu xuất hàng mượn (duyệt phiếu)', usecase=('FR-09', 'Tạo phiếu xuất hàng mượn', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Duyệt phiếu bằng cách lập Phiếu xuất hàng mượn',
       mota='Kế toán kho chuyển sang màn Phiếu xuất hàng mượn với phiếu yêu cầu này chọn sẵn. Lưu phiếu xuất '
            'thành công là phiếu yêu cầu được duyệt.',
       tacnhan=TN_KT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán kho.\n'
                '3. Phiếu đang ở trạng thái Chờ duyệt.',
       chinh='1. Kế toán kho bấm Tạo phiếu xuất hàng mượn ở màn chi tiết.\n'
             '2. Hệ thống mở màn lập Phiếu xuất hàng mượn, gắn sẵn phiếu yêu cầu này.\n'
             '3. Kế toán kho lập và lưu phiếu xuất (đặc tả ở SRS màn Phiếu xuất hàng mượn).\n'
             '4. Hệ thống chuyển phiếu yêu cầu sang Đã duyệt, ghi Người duyệt, Ngày duyệt và số Được duyệt.\n'
             '5. Hệ thống ghi nhận “Duyệt” trong lịch sử phiếu yêu cầu (kèm mã phiếu xuất) và thông báo người lập.',
       phu='• Kế toán kho thoát màn phiếu xuất không lưu → phiếu yêu cầu vẫn Chờ duyệt.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết => Tạo phiếu xuất hàng mượn', shot=shot('21_borrow_export_create'),
               shot_caption='Màn Lập phiếu xuất hàng mượn mở từ phiếu yêu cầu (phiếu yêu cầu điền sẵn)'),
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Tạo phiếu xuất hàng mượn', 'Button', 'Enable / Ẩn', 'Ẩn',
        'Chỉ hiện với Kế toán kho khi phiếu Chờ duyệt; bấm → mở màn lập Phiếu xuất hàng mượn.'),
       ('Nút Duyệt trên dòng danh sách', 'Button', 'Enable / Ẩn', 'Ẩn',
        'Cùng điều kiện; bấm → mở màn chi tiết phiếu để duyệt.'),
   ],
   ev=[
       ('Bấm Tạo phiếu xuất hàng mượn', 'Click',
        'Before:\n– Nút chỉ hiện khi đủ quyền và phiếu Chờ duyệt.\n'
        'After:\n– Mở màn lập Phiếu xuất hàng mượn với phiếu yêu cầu chọn sẵn.'),
       ('Lưu Phiếu xuất hàng mượn thành công', 'System',
        'After:\n– Phiếu yêu cầu sang Đã duyệt; ghi số Được duyệt cho từng dòng.\n'
        '– Ghi nhận “Duyệt” (Trạng thái: Chờ duyệt → Đã duyệt; Phiếu xuất hàng mượn: PXHM-…) trong lịch sử.\n'
        '– Gửi thông báo “[YCXHM] Đã duyệt: <mã>” (phiếu xuất, người duyệt) cho người lập.'),
   ])

# ------------------------------------------------------------ 2.10
fr(10, 'In phiếu và in danh sách', usecase=('FR-10', 'In phiếu / In danh sách', 'io', A_LAP),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu yêu cầu xuất hàng mượn / In danh sách',
       mota='Xem trước và in một phiếu, hoặc in danh sách theo bộ lọc đang áp.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm In ở cột Hành động / màn chi tiết (in phiếu), hoặc nút In trên bảng (in danh sách).\n'
             '2. Hệ thống mở cửa sổ xem trước ngay trên màn đang đứng.\n'
             '3. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Danh sách khớp bộ lọc quá 2.000 phiếu → không dựng bản in, nhắc thu hẹp bộ lọc.\n'
           '• Bấm Đóng → đóng cửa sổ xem trước.',
       dacbiet='Logo / tên công ty đầu bản in phiếu lấy theo công ty ghi trên phiếu.'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–',
        ['- In phiếu: “Xem trước phiếu <mã>”', '- In danh sách: “Xem trước danh sách yêu cầu xuất hàng mượn” (khổ ngang)']),
       ('Bản in phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- Đầu trang: logo, tên công ty của phiếu; tiêu đề “PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN”, Số phiếu, Ngày tạo',
         '- Thông tin người lập, phòng ban, phiếu mượn, ghi chú, trạng thái, người / ngày duyệt',
         '- Bảng hàng: STT, Tên hàng hóa, ĐVT, Số lượng xuất, Đơn giá, Thành tiền, Chi tiết theo phiếu mượn',
         '- Chỗ ký Người lập, Kế toán kho']),
       ('Bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        'Tiêu đề “DANH SÁCH PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN”, dòng điều kiện lọc, bảng phiếu.'),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', 'Mở hộp thoại in của trình duyệt.'),
       ('Nút Đóng (×)', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ xem trước.'),
   ],
   ev=[
       ('Bấm In (phiếu)', 'Click', 'Before:\n– Kiểm tra quyền xem phiếu (BR-04).\nAfter:\n– Dựng bản xem trước phiếu.'),
       ('Bấm In (danh sách)', 'Click',
        'During:\n– Lấy phiếu theo bộ lọc + phạm vi quyền; quá 2.000 dòng → nhắc thu hẹp bộ lọc, ẩn bản in.\n'
        'After:\n– Dựng bản xem trước danh sách khổ ngang.'),
       ('Bấm In trong cửa sổ xem trước', 'Click', 'After:\n– Mở hộp thoại in.'),
   ])

# ------------------------------------------------------------ 2.11
fr(11, 'Xuất danh sách ra Excel', usecase=('FR-11', 'Xuất Excel', 'io', A_LAP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất danh sách theo bộ lọc đang áp.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm Xuất Excel.\n2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 11 trường.\n'
             '3. Người dùng tích trường, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống tải file Excel về và báo “Xuất Excel thành công”.',
       phu='• Không có phiếu khớp → vẫn xuất file có tiêu đề và dòng tên cột.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”.\n• Bấm Đóng → không xuất.',
       dacbiet='Thứ tự cột trong file theo đúng thứ tự trường đã chọn.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Danh sách trường', 'Table/Grid', 'Enable', '11 trường', 'Ít nhất 1', 'Tích tất cả',
        'Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt, Người cập nhật, Ngày cập nhật, '
        'Phòng ban, Ghi chú, Lý do từ chối.'),
       ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
       ('Dòng “Đang chọn n/11 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn', '–'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', 'Khóa khi đang xuất.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', 'Đóng, không xuất.'),
   ],
   ev=[
       ('Kéo biểu tượng ba gạch', 'Drag', 'After:\n– Đổi thứ tự trường.'),
       ('Bấm Xuất file', 'Click',
        'During:\n– Lấy phiếu theo bộ lọc + phạm vi quyền.\n' + ERR + '\n'
        'After:\n– Tải file “DANH SÁCH PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN”, báo “Xuất Excel thành công”.'),
   ])

# ------------------------------------------------------------ 2.12
fr(12, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu',
       mota='Xem các mốc Tạo mới, Duyệt, Không duyệt của phiếu: người thực hiện, thời điểm, nội dung thay đổi.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động, hoặc Xem lịch sử ở khối Lịch sử màn chi tiết.\n'
             '2. Hệ thống hiển thị các mốc, mới nhất ở trên.',
       phu='• Bấm Bộ lọc → lọc theo loại hành động, người thực hiện, khoảng ngày.\n• Bấm Đóng → đóng cửa sổ.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề', 'Label', 'Hiển thị', '–', '–', '“Lịch sử thay đổi: <mã phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Duyệt: “Trạng thái: Chờ duyệt → Đã duyệt” và mã phiếu xuất hàng mượn',
           '- Không duyệt: “Trạng thái: Chờ duyệt → Không duyệt” và lý do']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', 'Lọc theo loại hành động, người thực hiện, từ ngày, đến ngày.'),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', 'Đóng cửa sổ.'),
   ],
   ev=[
       ('Mở lịch sử', 'Click', 'Before:\n– Kiểm tra quyền xem phiếu.\nAfter:\n– Hiển thị các mốc, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change', 'After:\n– Lọc lại danh sách mốc.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu xuất hàng mượn; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phiếu xuất mượn được chọn', [
        '– Là phiếu yêu cầu xuất hàng loại Xuất mượn, do CHÍNH người lập phiếu này lập.',
        '– Đã xuất kho và đang ở trạng thái Đã mượn.',
        '– Một phiếu yêu cầu gom được nhiều phiếu mượn; mỗi phiếu mượn chỉ chọn 1 lần trong cùng phiếu.',
        '– Máy chủ kiểm tra lại điều kiện lúc gửi.'], ['Lập phiếu', 'Chọn phiếu xuất mượn']),
    ('BR-02', 'Số lượng Đang mượn được phép xuất', [
        '– Đang mượn = đã xuất − đã trả − phần đang chờ ở các phiếu chưa duyệt khác (yêu cầu nhập trả hàng, '
        'yêu cầu xuất bán hàng mượn, yêu cầu xuất hàng mượn khác đang Chờ duyệt).',
        '– Quy theo hệ số đơn vị tính đang chọn, làm tròn xuống.',
        '– Số Xuất là số nguyên 0 – Đang mượn; máy chủ tính lại ngay trước khi lưu.'], ['Lập phiếu']),
    ('BR-03', 'Dòng hàng hợp lệ khi gửi', [
        '– Chỉ dòng hàng có trên ít nhất 1 phiếu mượn đã chọn mới được gửi; dòng “Chưa có phiếu mượn” bị bỏ qua.',
        '– Mỗi dòng gửi đi phải có tổng số Xuất > 0; tổng cả phiếu phải > 0.',
        '– Đơn giá theo đơn vị tính; Thành tiền = Số lượng xuất × Đơn giá.'], ['Lập phiếu']),
    ('BR-04', 'Phạm vi xem phiếu', [
        '– Người lập luôn xem được phiếu của mình.',
        '– Kế toán kho và V1 xem mọi phiếu đã gửi; V2 xem phiếu cùng công ty; V3 xem phiếu thuộc phòng ban mình quản lý.',
        '– Phiếu Đang tạo (dữ liệu cũ) chỉ người lập xem được.',
        '– Danh sách và màn chi tiết dùng chung một phạm vi.'], ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel']),
    ('BR-05', 'Vòng đời trạng thái', [
        '– Gửi đi → Chờ duyệt (không có nháp, không Sửa / Xóa).',
        '– Kế toán kho lập Phiếu xuất hàng mượn → Đã duyệt.',
        '– Kế toán kho từ chối (bắt buộc lý do) → Không duyệt, trạng thái cuối.'],
     ['Lập phiếu', 'Từ chối', 'Tạo phiếu xuất hàng mượn']),
    ('BR-06', 'Hai lối vào màn hình', [
        '– Bán hàng › Yêu cầu › Hàng hóa › YC xuất hàng mượn: phạm vi theo BR-04.',
        '– Tài chính › Hàng hoá - Dịch vụ - Vận chuyển › Mượn hàng › Yêu cầu xuất hàng mượn: dành cho Kế toán kho, '
        'mọi phiếu đã gửi; người không có quyền thấy danh sách rỗng.'], ['Xem danh sách']),
    ('BR-07', 'Thông báo', [
        '– Gửi phiếu → báo Kế toán kho cùng công ty.',
        '– Duyệt / Không duyệt → báo người lập (kèm mã phiếu xuất / lý do).'],
     ['Lập phiếu', 'Từ chối', 'Tạo phiếu xuất hàng mượn']),
    ('BR-08', 'Thao tác xong quay về danh sách', [
        '– Gửi duyệt và Từ chối thành công đều quay về màn danh sách (Từ chối: đúng lối vào đã mở trước đó).'],
     ['Lập phiếu', 'Từ chối']),
])

# ============================================================== PHẦN 5
d.h1('Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu')
d.p('Các màn hình dưới đây đọc dữ liệu do màn Yêu cầu xuất hàng mượn ghi ra.')
d.table(['STT', 'Nhóm', 'Màn hình', 'Đường dẫn'], [
    ('1', 'Mượn hàng', 'Phiếu xuất hàng mượn — chọn phiếu yêu cầu Chờ duyệt để lập phiếu xuất (duyệt), ghi ngược '
     'số Được duyệt và trạng thái Đã duyệt',
     'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng => Phiếu xuất hàng mượn'),
    ('2', 'Mượn hàng', 'Yêu cầu xuất bán hàng mượn — trừ phần đang chờ của phiếu yêu cầu Chờ duyệt khỏi số còn mượn',
     'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng => Yêu cầu xuất bán hàng mượn'),
    ('3', 'Mượn hàng', 'Phiếu xuất bán hàng mượn — trừ phần đang chờ của phiếu yêu cầu Chờ duyệt khỏi số còn mượn',
     'Phân hệ Tài chính => Hàng hoá - Dịch vụ - Vận chuyển => Mượn hàng => Phiếu xuất bán hàng mượn'),
], widths=[0.45, 1.0, 2.6, 2.4])

d.save()
print('Đã ghi', OUT)
