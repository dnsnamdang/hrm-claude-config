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
31/10/2026: nâng độ chi tiết ngang SRS_MAU (mỗi đối tượng 1 dòng, đủ nút / cột / trạng thái rỗng / toast nguyên
  văn, event đủ Before–During–After) — đối chiếu lại code develop cả 2 repo.
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
TN_MOI = ('Người dùng có quyền thực hiện chức năng: người lập phiếu — chức năng không gắn quyền riêng, '
          'nhân sự nào có phiếu xuất mượn do chính mình lập (đang ở trạng thái Đã mượn) đều thực hiện được.')
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

# Mô tả riêng cho hàng sau khi tách dòng gộp (srs_split_rows). Bản 31/10/2026 đã viết sẵn mỗi đối tượng
# 1 hàng nên không còn dòng gộp nào cần mô tả riêng — giữ khung để split_ui_rows vẫn kiểm.
UI_OVER = {}
UI_EXPLICIT = {}

_uc_n = [0]


def uc(code, name, group, actor):
    """Biểu đồ Use Case 1 chức năng theo khổ mẫu quốc gia (actor + 1 use case)."""
    from formqg_lib import draw_usecase_qg
    png = os.path.join(UML, 'uc_%s.png' % code.replace('-', ''))
    draw_usecase_qg(png, actor, code, name, group)
    d.figure(png, 'Biểu đồ Use Case — %s %s' % (code, name), width_in=6.2)


def fr(no, title, intro, layout, ui, ev, ui_kw=None, usecase=None, rule=None, extra=None):
    """Một chức năng 2.x: (Biểu đồ Usecase) · Giới thiệu · Layout · Mô tả giao diện · Event.

    extra: [(ảnh, chú thích)] — ảnh bổ sung đặt ngay sau ảnh Layout (lỗi kiểm tra, popup con…).
    """
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
       mota='Hiển thị bảng phiếu yêu cầu xuất hàng mượn nằm trong phạm vi dữ liệu của người đăng nhập, kèm '
            'phân trang, sắp xếp và tổng số phiếu khớp bộ lọc. Màn có hai lối vào dùng chung một màn hình: lối '
            'vào chung (phân hệ Bán hàng) cho người lập và cấp quản lý, lối vào của Kế toán kho (phân hệ Tài '
            'chính) để tìm phiếu cần duyệt; hai lối vào chỉ khác tiêu đề và phạm vi dữ liệu.',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n'
                '2. Lối vào Kế toán kho chỉ có dữ liệu khi người dùng có quyền Kế toán kho.',
       chinh='1. Người dùng vào màn theo một trong hai lối vào ở mục Layout.\n'
             '2. Hệ thống xác định lối vào theo đường dẫn; giá trị lạ coi là lối vào chung.\n'
             '3. Lối vào chung: hệ thống xác định phạm vi dữ liệu theo thứ tự V1 → V2 → V3, không có quyền nào '
             'thì chỉ lấy phiếu do chính người dùng lập; Kế toán kho thấy mọi phiếu (BR-04).\n'
             '4. Lối vào Kế toán kho: hệ thống lấy mọi phiếu đã gửi (Chờ duyệt, Đã duyệt, Không duyệt).\n'
             '5. Hệ thống loại phiếu Đang tạo (dữ liệu cũ) của người khác ở cả hai lối vào.\n'
             '6. Hệ thống khôi phục bộ lọc đã dùng trong 10 phút gần nhất và cấu hình cột đã lưu của người dùng.\n'
             '7. Hệ thống hiển thị trang 1, 10 dòng/trang, phiếu tạo gần nhất xếp trên, kèm dòng “Hiển thị a–b / N”.',
       phu='• Không có phiếu nào khớp → trong bảng hiện “Không có dữ liệu phù hợp.”, dưới bảng hiện “Không có '
           'phiếu nào.”.\n'
           '• Vào lối vào Kế toán kho mà không có quyền Kế toán kho → bảng không có dữ liệu.\n'
           '• Đang ở màn, bấm sang lối vào còn lại → danh sách tự nạp lại theo lối vào mới, về trang 1.\n'
           '• Máy chủ lỗi khi nạp danh sách → thông báo “Lỗi khi tải dữ liệu”, bảng giữ trống.\n'
           '• Người dùng đã lưu cấu hình cột riêng → bảng áp cấu hình đó thay cho bộ cột mặc định.',
       dacbiet=None),
   layout=dict(entries=[
       (MENU_SALE, 'Hiển thị: tiêu đề “Yêu cầu xuất hàng mượn”; phiếu trong phạm vi quyền (V1/V2/V3, không có '
                   'quyền thì phiếu của mình); Kế toán kho thấy mọi phiếu đã gửi.'),
       (MENU, 'Hiển thị: tiêu đề “Yêu cầu xuất hàng mượn (Kế toán kho)”; chỉ người có quyền Kế toán kho thấy dữ '
              'liệu — mọi phiếu đã gửi (Chờ duyệt, Đã duyệt, Không duyệt).')],
       shot=shot('01_list'), shot_caption='Màn danh sách Yêu cầu xuất hàng mượn'),
   extra=[(shot('01b_list_accounting'), 'Màn danh sách ở lối vào của Kế toán kho')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Theo lối vào',
        ['- Lối vào chung: “Yêu cầu xuất hàng mượn”', '- Lối vào Kế toán kho: “Yêu cầu xuất hàng mượn (Kế toán kho)”',
         '- Cùng chữ hiện trên thanh tiêu đề và tab trình duyệt']),
       ('Nút Tạo mới', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Không gắn quyền, hiện ở cả hai lối vào', '- Bấm → mở màn Thêm yêu cầu xuất hàng mượn (mục 2.5)']),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị',
        ['- Rê chuột: “In danh sách theo bộ lọc đang áp”',
         '- Bấm → mở cửa sổ Xem trước danh sách (mục 2.10)']),
       ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị',
        ['- Rê chuột: “Xuất Excel danh sách theo bộ lọc đang áp”',
         '- Bấm → mở cửa sổ Chọn trường xuất Excel (mục 2.11)', '- Khóa trong lúc đang xuất file']),
       ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị',
        '- Biểu tượng cột; bấm → mở cửa sổ Tùy chỉnh cột (mục 2.4).'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Đánh số liên tục theo trang (trang 2 bắt đầu từ số dòng/trang + 1)',
         '- Cột khóa: luôn hiện, không đổi vị trí, ghim bên trái khi cuộn ngang']),
       ('Cột Mã phiếu', 'Table/Grid', 'Read-only', 'PYCXHM-NNNNN', 'Hiển thị',
        ['- Là liên kết: bấm → mở màn chi tiết phiếu (mục 2.7); chuột phải mở được ở tab mới',
         '- Sắp xếp được', '- Cột khóa, ghim bên trái khi cuộn ngang']),
       ('Cột Người tạo', 'Table/Grid', 'Read-only', '–', 'Hiển thị', '- Dạng “Họ tên - Mã phòng ban” của người lập.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Thời điểm gửi phiếu', '- Sắp xếp được; mặc định mới nhất xếp trên']),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', 'Danh sách 3 giá trị', 'Hiển thị',
        ['- Chờ duyệt: nhãn màu cam', '- Đã duyệt: nhãn màu xanh lá', '- Không duyệt: nhãn màu đỏ',
         '- Chữ và màu do máy chủ trả về']),
       ('Cột Người duyệt', 'Table/Grid', 'Read-only', '–', 'Hiển thị',
        ['- Họ tên Kế toán kho đã duyệt hoặc đã từ chối phiếu', '- Trống khi phiếu còn Chờ duyệt']),
       ('Cột Ngày duyệt', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Hiển thị',
        ['- Thời điểm duyệt hoặc từ chối', '- Sắp xếp được', '- Trống khi phiếu còn Chờ duyệt']),
       ('Cột Người cập nhật', 'Table/Grid', 'Read-only', '–', 'Ẩn',
        ['- Người sửa phiếu gần nhất, dạng “Họ tên - Mã phòng ban”', '- Ẩn mặc định; bật trong cửa sổ Tùy chỉnh cột']),
       ('Cột Ngày cập nhật', 'Table/Grid', 'Read-only', 'dd/mm/yyyy hh:mm', 'Ẩn',
        ['- Thời điểm sửa phiếu gần nhất', '- Ẩn mặc định; bật trong cửa sổ Tùy chỉnh cột']),
       ('Cột Phòng ban', 'Table/Grid', 'Read-only', '–', 'Ẩn',
        ['- Phòng ban hiện tại của người tạo', '- Ẩn mặc định']),
       ('Cột Ghi chú', 'Table/Grid', 'Read-only', '0–255 ký tự', 'Ẩn',
        ['- Ghi chú người lập nhập khi gửi phiếu', '- Ẩn mặc định; tự xuống dòng khi dài']),
       ('Cột Lý do từ chối', 'Table/Grid', 'Read-only', '0–255 ký tự', 'Ẩn',
        ['- Lý do Kế toán kho nhập khi từ chối', '- Trống với phiếu chưa bị từ chối', '- Ẩn mặc định']),
       ('Cột Hành động', 'Table/Grid', 'Enable', '–', 'Hiển thị', [
           '- Nút Duyệt: chỉ hiện với Kế toán kho khi phiếu Chờ duyệt; bấm → mở màn chi tiết để duyệt (mục 2.9)',
           '- Nút In: bấm → mở cửa sổ Xem trước phiếu (mục 2.10)',
           '- Nút Lịch sử: bấm → mở cửa sổ Lịch sử thay đổi (mục 2.12)',
           '- Không có nút Sửa / Xóa ở bất kỳ trạng thái nào', '- Cột khóa trong Tùy chỉnh cột']),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- Trong bảng: “Không có dữ liệu phù hợp.”', '- Dưới bảng: “Không có phiếu nào.”', '- Chỉ hiện khi N = 0']),
       ('Dòng “Hiển thị a–b / N”', 'Label', 'Read-only', '–', 'Theo kết quả',
        ['- a–b: thứ tự dòng đầu – cuối của trang đang xem', '- N: tổng số phiếu khớp bộ lọc trong phạm vi quyền']),
       ('Ô Số dòng/trang', 'Dropdown', 'Enable', '5, 10, 20, 50, 100', '10',
        ['- Mặc định: 10', '- Lựa chọn: 5 / 10 / 20 / 50 / 100', '- Đổi giá trị → về trang 1']),
       ('Phân trang', 'Pagination', 'Enable', '–', 'Trang 1',
        '- Nút về đầu, lùi, số trang, tiến, về cuối; giữ nguyên bộ lọc và sắp xếp.'),
       ('Thông báo lỗi tải dữ liệu', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        '- “Lỗi khi tải dữ liệu” khi máy chủ trả lỗi lúc nạp danh sách.'),
   ],
   ev=[
       ('Mở màn hình', 'System',
        'Before:\n– Xác định lối vào: chung hoặc Kế toán kho; giá trị lạ coi là lối vào chung.\n'
        '– Khôi phục bộ lọc đã dùng trong 10 phút gần nhất và cấu hình cột đã lưu.\n'
        'During:\n– Lối vào chung: áp phạm vi V1 → V2 → V3 → phiếu của mình; Kế toán kho thấy mọi phiếu.\n'
        '– Lối vào Kế toán kho: người có quyền thấy mọi phiếu đã gửi; không có quyền thì trả rỗng.\n'
        '– Loại phiếu Đang tạo của người khác.\n'
        '– Máy chủ lỗi → hiển thị “Lỗi khi tải dữ liệu”.\n'
        'After:\n– Hiển thị trang 1, 10 dòng, sắp theo Ngày tạo mới nhất, kèm dòng “Hiển thị a–b / N”.'),
       ('Bấm Mã phiếu', 'Click',
        'Before:\n– Phiếu nằm trong phạm vi xem của người dùng (đã lọc ở danh sách).\n'
        'After:\n– Mở màn chi tiết phiếu (mục 2.7); chuột phải cho phép mở ở tab mới.'),
       ('Bấm tiêu đề cột có sắp xếp', 'Click',
        'Before:\n– Chỉ ba cột Mã phiếu, Ngày tạo, Ngày duyệt hỗ trợ sắp xếp.\n'
        'After:\n– Đổi chiều sắp xếp tăng / giảm theo cột; nạp lại từ trang 1, giữ bộ lọc.'),
       ('Bấm số trang hoặc nút tiến / lùi', 'Click',
        'Before:\n– Giữ nguyên bộ lọc và thứ tự sắp xếp đang áp.\n'
        'After:\n– Nạp dữ liệu trang mới; STT tiếp tục liên tục.'),
       ('Đổi Số dòng/trang', 'Change',
        'Before:\n– Giữ nguyên bộ lọc và sắp xếp.\nAfter:\n– Về trang 1 và nạp lại theo số dòng mới.'),
       ('Bấm sang lối vào còn lại trên menu', 'Click',
        'Before:\n– Hai lối vào dùng chung một màn, chỉ khác tham số lối vào.\n'
        'After:\n– Đổi tiêu đề, về trang 1 và nạp lại danh sách theo phạm vi của lối vào mới.'),
   ])

# ------------------------------------------------------------ 2.2
fr(2, 'Tìm kiếm và lọc phiếu',
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Dropdown.', 'search'),
   intro=dict(
       ten='Tìm kiếm và lọc danh sách phiếu',
       mota='Thu hẹp danh sách theo mã phiếu, trạng thái, người tạo, người duyệt, mã / tên hàng hóa, ngày tạo '
            'và công ty – phòng ban. Ô lọc Công ty, Phòng ban chỉ hiện theo cấp quyền xem; Kế toán kho tìm việc '
            'cần làm bằng ô Trạng thái = Chờ duyệt.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng nhập mã phiếu vào ô tìm nhanh rồi bấm Tìm kiếm.\n'
             '2. Hoặc bấm Tìm kiếm nâng cao để mở khối ô lọc, chọn / nhập một hoặc nhiều tiêu chí.\n'
             '3. Hệ thống lọc ngay khi một ô lọc nâng cao đổi giá trị, về trang 1.\n'
             '4. Hệ thống nạp lại danh sách, cập nhật dòng “Hiển thị a–b / N”.\n'
             '5. Hệ thống ghi nhớ bộ lọc trong 10 phút để khôi phục khi quay lại màn.',
       phu='• Bấm Làm mới → xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1, giữ nguyên lối vào.\n'
           '• Không có kết quả → bảng hiện “Không có dữ liệu phù hợp.”.\n'
           '• Đổi Công ty → hệ thống xóa Phòng ban đang chọn và nạp lại danh sách phòng ban của công ty mới.\n'
           '• Gõ vào ô tìm nhanh mà chưa bấm Tìm kiếm → danh sách chưa đổi.\n'
           '• Ô lọc bị tắt trong Cài đặt bộ lọc → không hiện trên khối lọc.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Tìm kiếm nâng cao', shot=shot('02_filter'),
               shot_caption='Khối Bộ lọc danh sách đang mở tìm kiếm nâng cao'),
   ui=[
       ('Tiêu đề khối lọc', 'Label', 'Hiển thị', '–', '–', 'Bộ lọc danh sách', '- Chữ cố định “Bộ lọc danh sách”.'),
       ('Ô tìm nhanh', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Tìm kiếm theo mã phiếu”', '- Tìm theo một phần mã phiếu',
         '- Chỉ lọc khi bấm Tìm kiếm, không lọc khi đang gõ']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → áp ô tìm nhanh, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Bấm → xóa mọi tiêu chí kể cả ô tìm nhanh', '- Bỏ sắp xếp, nạp lại từ trang 1']),
       ('Nút Tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn',
        ['- Bấm → mở khối ô lọc nâng cao', '- Khi mở, nhãn đổi thành “Ẩn tìm kiếm nâng cao”; bấm lại để thu gọn']),
       ('Nút Cài đặt bộ lọc', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → mở cửa sổ Cài đặt bộ lọc (mục 2.3).'),
       ('Công ty', 'Dropdown', 'Enable / Ẩn', 'Danh sách công ty', 'Không', 'Trống',
        ['- Chỉ hiện với người có quyền V1', '- Mặc định: trống (mọi công ty)', '- Chọn → lọc phiếu thuộc công ty đó']),
       ('Phòng ban', 'Dropdown', 'Enable / Ẩn', 'Danh sách phòng ban', 'Không', 'Trống',
        ['- Hiện với V1, V2, V3', '- Mặc định: trống', '- Chỉ liệt kê phòng ban của công ty đang chọn',
         '- Đổi Công ty → tự xóa phòng ban đã chọn']),
       ('Mã phiếu', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Phiếu có mã chứa chuỗi nhập', '- Lọc ngay khi đổi giá trị']),
       ('Trạng thái', 'Dropdown', 'Enable', 'Danh sách 3 giá trị', 'Không', 'Trống',
        ['- Mặc định: trống (mọi trạng thái)', '- Lựa chọn: Chờ duyệt', '- Lựa chọn: Đã duyệt',
         '- Lựa chọn: Không duyệt']),
       ('Người tạo', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Nhân viên đang làm việc thuộc công ty của người đăng nhập',
         '- Lọc phiếu do người đó lập']),
       ('Người duyệt', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Không', 'Trống',
        ['- Mặc định: trống', '- Lọc phiếu do Kế toán kho đó duyệt hoặc từ chối']),
       ('Mã hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        '- Phiếu có ít nhất 1 dòng hàng có mã chứa chuỗi nhập.'),
       ('Tên hàng hóa', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        '- Phiếu có ít nhất 1 dòng hàng có tên chứa chuỗi nhập.'),
       ('Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống',
        ['- Một ô chọn khoảng từ ngày → đến ngày', '- Lấy trọn hai đầu: phiếu lập trong chính ngày cuối vẫn có',
         '- Được bỏ trống một đầu']),
   ],
   ev=[
       ('Đổi giá trị một ô lọc nâng cao', 'Change',
        'Before:\n– Ô lọc đang bật trong Cài đặt bộ lọc.\n'
        'During:\n– Ghi nhận giá trị mới và ghi nhớ bộ lọc trong 10 phút.\n'
        'After:\n– Về trang 1 và nạp lại danh sách theo toàn bộ tiêu chí đang có.'),
       ('Bấm Tìm kiếm', 'Click',
        'Before:\n– Lấy giá trị ô tìm nhanh.\nAfter:\n– Áp ô tìm nhanh, về trang 1, nạp lại danh sách.'),
       ('Bấm Làm mới', 'Click',
        'Before:\n– Giữ nguyên lối vào đang mở.\n'
        'After:\n– Xóa mọi tiêu chí kể cả ô tìm nhanh, bỏ sắp xếp, nạp lại từ trang 1.'),
       ('Chọn lại Công ty', 'Change',
        'Before:\n– Ô Công ty chỉ hiện với người có quyền V1.\n'
        'During:\n– Xóa Phòng ban đang chọn.\n'
        'After:\n– Nạp danh sách phòng ban của công ty mới và nạp lại danh sách phiếu.'),
       ('Bấm Tìm kiếm nâng cao', 'Click',
        'Before:\n– Khối lọc đang thu gọn hoặc đang mở.\n'
        'After:\n– Mở / thu gọn khối ô lọc; trạng thái mở được ghi nhớ cùng bộ lọc.'),
   ])

# ------------------------------------------------------------ 2.3
fr(3, 'Cài đặt bộ lọc',
   rule=('- Bộ lọc và Cấu hình cột.', 'search'),
   intro=dict(
       ten='Cài đặt các ô lọc hiển thị',
       mota='Cho mỗi người dùng tự chọn những ô lọc muốn thấy trong khối Tìm kiếm nâng cao và sắp lại thứ tự của '
            'chúng. Cấu hình lưu riêng theo người dùng cho màn Yêu cầu xuất hàng mượn.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm Cài đặt bộ lọc.\n'
             '2. Hệ thống mở cửa sổ “Cài đặt bộ lọc” liệt kê 8 ô lọc kèm ô tích, theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích và kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công”, đóng cửa sổ và vẽ lại khối lọc.',
       phu='• Bấm Khôi phục mặc định → tích lại đủ 8 ô theo thứ tự thiết kế; vẫn phải bấm Lưu mới có hiệu lực.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, bỏ thay đổi chưa lưu.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”, cấu hình cũ giữ nguyên.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Cài đặt bộ lọc', shot=shot('26_filtercfg'), shot_caption='Cửa sổ Cài đặt bộ lọc',
               note='Modal Cài đặt bộ lọc được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Cài đặt bộ lọc”.'),
       ('Danh sách ô lọc', 'Table/Grid', 'Enable', 'Danh sách 8 ô lọc', '–', 'Theo cấu hình đã lưu',
        ['- Công ty – Phòng ban', '- Mã phiếu', '- Trạng thái', '- Người tạo', '- Người duyệt', '- Mã hàng hóa',
         '- Tên hàng hóa', '- Ngày tạo']),
       ('Ô tích từng mục', 'Checkbox', 'Enable', '–', 'Không', 'Đang tích',
        '- Bỏ tích → ô lọc đó không hiện ở khối Tìm kiếm nâng cao.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        '- Rê chuột: “Kéo để sắp xếp”; kéo để đổi vị trí ô lọc.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, đóng cửa sổ.'),
       ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị',
        '- Bấm → tích lại đủ 8 ô theo thứ tự thiết kế; chưa lưu.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cài đặt bộ lọc', 'Click',
        'Before:\n– Không cần quyền riêng.\n'
        'After:\n– Mở cửa sổ, nạp cấu hình đang lưu của người dùng (chưa lưu lần nào → đủ 8 ô theo thiết kế).'),
       ('Kéo đổi vị trí một mục', 'Drag', 'Before:\n– Kéo bằng biểu tượng kéo thả.\nAfter:\n– Cập nhật thứ tự trong cửa sổ; chỉ áp lên màn khi bấm Lưu.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Không cần quyền riêng; cấu hình lưu theo người dùng hiện tại.\n'
        'During:\n– Gửi danh sách ô đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại khối lọc.'),
       ('Bấm Khôi phục mặc định', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Tích lại đủ 8 ô và đưa thứ tự về thiết kế gốc; chưa lưu.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\nAfter:\n– Đóng cửa sổ, bỏ thay đổi chưa lưu.'),
   ])

# ------------------------------------------------------------ 2.4
fr(4, 'Tùy chỉnh cột hiển thị',
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Tùy chỉnh cột của bảng danh sách',
       mota='Cho mỗi người dùng bật / tắt và kéo sắp xếp 13 cột của bảng danh sách. Ba cột STT, Mã phiếu, Hành '
            'động bị khóa; cấu hình lưu riêng theo người dùng cho màn này.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm nút Cấu hình cột hiển thị.\n'
             '2. Hệ thống mở cửa sổ “Tuỳ chỉnh cột” liệt kê 13 cột theo cấu hình đang lưu.\n'
             '3. Người dùng tích / bỏ tích, kéo biểu tượng kéo thả để đổi thứ tự.\n'
             '4. Người dùng bấm Lưu.\n'
             '5. Hệ thống lưu cấu hình, báo “Cập nhật thành công” và vẽ lại bảng.',
       phu='• Bấm Chọn tất cả / Bỏ chọn hết → tích / bỏ tích mọi cột không khóa; chưa lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng, danh sách trả về đúng cấu hình đang áp.\n'
           '• Lưu không thành công → thông báo “Thao tác thất bại”.',
       dacbiet='Mặc định ẩn 5 cột: Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối.'),
   layout=dict(menu=MENU + ' => Cấu hình cột', shot=shot('25_colcfg'), shot_caption='Cửa sổ Tùy chỉnh cột',
               note='Modal Tùy chỉnh cột được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Tuỳ chỉnh cột”.'),
       ('Danh sách cột', 'Table/Grid', 'Enable', 'Danh sách 13 cột', '–', 'Theo cấu hình đã lưu',
        ['- STT, Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt',
         '- Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối, Hành động']),
       ('Ô tích cột thường', 'Checkbox', 'Enable', '–', 'Không', 'Theo cấu hình',
        ['- Bỏ tích → cột ẩn khỏi bảng', '- Mặc định bỏ tích 5 cột Người cập nhật, Ngày cập nhật, Phòng ban, '
         'Ghi chú, Lý do từ chối']),
       ('Ô tích cột khóa', 'Checkbox', 'Disable', '–', '–', 'Đang tích',
        ['- STT, Mã phiếu, Hành động', '- Biểu tượng ổ khóa, rê chuột: “Cột bắt buộc — không thể ẩn hoặc đổi vị trí”']),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        '- Kéo để đổi vị trí cột; cột khóa không kéo được.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi cột không khóa.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi cột không khóa.'),
       ('Dòng “Đang chọn n/13 cột”', 'Label', 'Read-only', '–', '–', 'Theo cấu hình',
        '- n = số cột đang tích, cập nhật ngay khi tích / bỏ tích.'),
       ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lưu cấu hình theo người dùng, vẽ lại bảng.'),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng, bỏ thay đổi chưa lưu.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả lưu', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Cập nhật thành công”', '- Thất bại: “Thao tác thất bại”']),
   ],
   ev=[
       ('Bấm Cấu hình cột hiển thị', 'Click', 'Before:\n– Không cần quyền riêng.\nAfter:\n– Mở cửa sổ, nạp cấu hình cột đang lưu của người dùng.'),
       ('Kéo biểu tượng kéo thả', 'Drag',
        'Before:\n– Cột khóa không đổi được vị trí.\nAfter:\n– Đổi thứ tự cột trong danh sách; chưa áp lên bảng.'),
       ('Tích / bỏ tích một cột', 'Change',
        'Before:\n– Cột khóa không cho bỏ tích.\nAfter:\n– Cập nhật dòng “Đang chọn n/13 cột”.'),
       ('Bấm Lưu', 'Click',
        'Before:\n– Không cần quyền riêng; cấu hình lưu theo người dùng hiện tại.\n'
        'During:\n– Gửi danh sách cột đã tích theo đúng thứ tự.\n' + ERR + '\n'
        'After:\n– Hiển thị “Cập nhật thành công”, đóng cửa sổ, vẽ lại bảng theo cột đã chọn.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã đổi.\n'
        'After:\n– Đóng cửa sổ; danh sách cột trả về đúng cấu hình đang áp.'),
   ])

# ------------------------------------------------------------ 2.5
fr(5, 'Lập phiếu yêu cầu xuất hàng mượn', usecase=('FR-05', 'Lập phiếu', 'crud', A_LAP),
   rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo và Quy tắc ghi lịch sử.', 'create'),
   intro=dict(
       ten='Lập phiếu yêu cầu xuất hàng mượn',
       mota='Người đang mượn hàng gom một hoặc nhiều phiếu xuất mượn của chính mình, chọn mặt hàng và số lượng '
            'không trả lại mà xuất hẳn, đính kèm chứng từ PDF rồi gửi Kế toán kho duyệt. Phiếu không có bản '
            'nháp: gửi đi là vào thẳng Chờ duyệt và không sửa / xóa được nữa.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n'
                '2. Chức năng không gắn quyền riêng; người dùng có ít nhất 1 phiếu xuất mượn đủ điều kiện (BR-01).\n'
                '3. Người dùng đang ở màn danh sách Yêu cầu xuất hàng mượn.',
       chinh='1. Người dùng bấm Tạo mới ở màn danh sách.\n'
             '2. Hệ thống mở màn “Thêm yêu cầu xuất hàng mượn”, góc phải khối Thông tin chung hiện “<người '
             'đăng nhập> - <thời điểm hiện tại>”.\n'
             '3. Người dùng bấm Thêm phiếu, chọn một hoặc nhiều phiếu xuất mượn (mục 2.6).\n'
             '4. Người dùng nhập Ghi chú, bấm Thêm tài liệu đính kèm ít nhất 1 file PDF.\n'
             '5. Người dùng bấm nút + ở bảng Chi tiết, chọn hàng hóa trong cửa sổ “Thêm hàng hoá”.\n'
             '6. Với mỗi hàng, người dùng chọn Đơn vị tính và nhập số Xuất theo từng phiếu mượn.\n'
             '7. Người dùng bấm Gửi duyệt, xác nhận ở hộp “Xác nhận gửi duyệt”.\n'
             '8. Hệ thống kiểm tra lại phiếu mượn, số đang mượn, đơn giá; sinh mã PYCXHM-NNNNN, lưu phiếu ở '
             'trạng thái Chờ duyệt.\n'
             '9. Hệ thống ghi nhận hành động “Tạo mới” trong lịch sử của phiếu.\n'
             '10. Hệ thống gửi thông báo cho Kế toán kho cùng công ty với phiếu.\n'
             '11. Hệ thống báo “Yêu cầu của bạn đã được gửi.” và quay về màn danh sách.',
       phu='• Thiếu dữ liệu bắt buộc → báo đỏ ngay dưới ô lỗi kèm thông báo “Bạn chưa nhập đầy đủ thông tin.”, '
           'con trỏ về ô lỗi đầu tiên, không gửi.\n'
           '• Bấm Lưu và tiếp tục → gửi duyệt như trên rồi ở lại màn Thêm mới với form trống.\n'
           '• Hàng thêm vào không có trên phiếu mượn nào đã chọn → dòng bị khóa, ghi “Chưa có phiếu mượn”, '
           'không nhập số lượng và không được gửi đi.\n'
           '• Chọn trong cửa sổ Thêm hàng hoá một hàng đã có trong phiếu → bỏ qua, báo “Hàng hóa đã có trong '
           'phiếu: <tên>”.\n'
           '• Bỏ một phiếu mượn (dấu ×) → các dòng hàng giữ nguyên, chỉ mất phần chi tiết của phiếu đó.\n'
           '• Bấm Hủy ở hộp xác nhận → ở lại màn, dữ liệu giữ nguyên.\n'
           '• Bấm Quay lại khi chưa nhập gì → về danh sách; đã nhập → hộp “Thông tin chưa lưu”: Ở lại giữ dữ '
           'liệu, Thoát bỏ dữ liệu và về danh sách.\n'
           '• Máy chủ từ chối dữ liệu (phiếu mượn hết hợp lệ, vượt số đang mượn…) → báo đỏ tại ô và thông báo '
           'câu lỗi của máy chủ, không lưu.',
       dacbiet='Công ty, phòng ban của phiếu lấy theo người lập tại thời điểm lập. Số “Đang mượn” và Đơn giá '
               'được máy chủ tính lại ngay trước khi lưu, không tin số trên màn hình (BR-02, BR-09). Nút Gửi '
               'duyệt và Lưu và tiếp tục bị khóa trong lúc đang gửi để không tạo trùng phiếu.'),
   layout=dict(menu=MENU + ' => Tạo mới', shot=shot('10c_filled'),
               shot_caption='Màn Thêm yêu cầu xuất hàng mượn đã nhập dữ liệu'),
   extra=[(shot('10b_validate'), 'Lỗi kiểm tra khi bấm Gửi duyệt mà chưa nhập đủ thông tin'),
          (shot('12_product'), 'Cửa sổ Thêm hàng hoá mở từ nút + của bảng Chi tiết')],
   ui=[
       ('Tiêu đề màn', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Thêm yêu cầu xuất hàng mượn”.'),
       ('Người tạo – Ngày tạo', 'Label', 'Read-only', '–', '–', 'Người đăng nhập – thời điểm hiện tại',
        '- Góc phải khối Thông tin chung, dạng “<Họ tên> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu xuất mượn', 'Table/Grid', 'Enable', 'Ít nhất 1 phiếu', 'Có', '“Chưa chọn phiếu xuất mượn”',
        ['- Mỗi phiếu đã chọn là 1 thẻ mã kèm dấu ×', '- Bấm × (rê chuột: “Bỏ phiếu này”) → bỏ phiếu khỏi danh sách',
         '- Lỗi dưới ô: “Bắt buộc phải chọn ít nhất 1 phiếu xuất mượn”']),
       ('Nút Thêm phiếu', 'Button', 'Enable', '–', '–', 'Hiển thị',
        '- Bấm → mở cửa sổ Chọn phiếu xuất mượn (mục 2.6).'),
       ('Ghi chú', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống',
        ['- Gợi ý “Nhập lý do xuất số hàng đang mượn này...”', '- Không gõ được quá 255 ký tự',
         '- Lỗi dưới ô: “Bắt buộc phải nhập”']),
       ('Khối File đính kèm', 'Table/Grid', 'Enable', 'Chỉ PDF, tối đa 20 MB / file', 'Có', 'Chưa có file',
        ['- Bảng cột STT, Upload / File, Dung lượng', '- File tải lên ngay khi chọn; xem trước, tải xuống được',
         '- Lỗi dưới khối: “Bắt buộc phải đính kèm ít nhất 1 file”']),
       ('Nút Thêm tài liệu', 'Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Bấm → thêm 1 dòng trống và mở hộp chọn file', '- Sai đuôi: “File "<tên>" không thuộc định dạng cho phép”',
         '- Quá 20 MB: “File "<tên>" vượt quá 20MB”']),
       ('Nút Xóa file', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        '- Bấm → gỡ file chưa lưu khỏi danh sách ngay, không hỏi lại.'),
       ('Nút + (Thêm hàng hóa)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        ['- Đầu cột cuối bảng Chi tiết, rê chuột: “Thêm hàng hóa”',
         '- Bấm → mở cửa sổ “Thêm hàng hoá” (chỉ tab Hàng hoá, chọn nhiều, không có Thêm hàng tạm)',
         '- Click ra ngoài cửa sổ không đóng; đóng bằng nút Đóng / (x)']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Theo dòng hàng', '- Số thứ tự dòng hàng, gộp theo các dòng con.'),
       ('Cột Tên hàng hóa', 'Table/Grid', 'Read-only', '–', '–', 'Theo hàng đã chọn',
        ['- Tên hàng', '- Các dòng phụ: Model, Mã, Thương hiệu (thiếu thì hiện “—”)']),
       ('Cột Đơn vị tính', 'Dropdown', 'Enable', 'Đơn vị của hàng', 'Có', 'Đơn vị ghi trên phiếu mượn',
        ['- Mặc định: đơn vị ghi trên phiếu mượn; không có thì đơn vị đầu tiên của hàng',
         '- Đơn vị có hệ số khác 1 hiện kèm hệ số, ví dụ “Thùng (x24)”',
         '- Đổi đơn vị → tính lại Đơn giá, Đang mượn; số Xuất vượt Đang mượn tự kéo về bằng Đang mượn']),
       ('Cột Đơn giá', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo đơn vị tính',
        ['- Giá bán theo đơn vị đang chọn', '- Định dạng 1,234,567']),
       ('Cột Số lượng xuất', 'Table/Grid', 'Read-only', '≥ 0', '–', '0',
        '- Tổng số Xuất của mọi phiếu mượn trên dòng hàng.'),
       ('Cột Phiếu mượn', 'Link', 'Enable', 'PYCXH-…', '–', 'Theo dữ liệu',
        ['- Mỗi phiếu mượn có hàng này là 1 dòng con', '- Bấm mã → mở chi tiết phiếu yêu cầu xuất hàng ở tab mới '
         '(không mất dữ liệu đang nhập)']),
       ('Cột Đang mượn', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Theo dữ liệu',
        ['- Số còn được phép xuất của hàng trên phiếu mượn đó, quy theo đơn vị đang chọn', '- Cách tính: BR-02']),
       ('Cột Xuất', 'Textbox', 'Enable', 'Số nguyên 0 – Đang mượn', 'Có', '0', [
           '- Gợi ý “0”, chỉ nhận số nguyên',
           '- Lỗi dưới ô: “Không hợp lệ” / “Phải lớn hơn hoặc bằng 0” / “Không được vượt quá 6 chữ số” / “Vượt quá số đang mượn”',
           '- Cả dòng hàng chưa có số Xuất > 0 khi gửi: “Chưa nhập số lượng xuất”']),
       ('Dòng hàng bị khóa', 'Table/Grid', 'Disable', '–', '–', 'Ẩn',
        ['- Hàng không có trên phiếu mượn nào đã chọn', '- Tô mờ, 3 ô chi tiết gộp thành “Chưa có phiếu mượn”',
         '- Không gửi đi khi lưu']),
       ('Cột Thành tiền', 'Table/Grid', 'Read-only', '≥ 0', '–', '0', '- Số lượng xuất × Đơn giá, định dạng 1,234,567.'),
       ('Nút Xóa dòng', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        '- Rê chuột: “Xóa dòng”; bấm → bỏ dòng hàng khỏi phiếu ngay, không hỏi lại.'),
       ('Dòng Tổng cộng', 'Table/Grid', 'Read-only', '≥ 0', '–', 'Ẩn khi chưa có hàng',
        '- Tổng Số lượng xuất và tổng Thành tiền của mọi dòng hàng.'),
       ('Trạng thái rỗng bảng Chi tiết', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Không có hàng hóa. Chọn phiếu xuất mượn ở trên, rồi bấm + ở góc phải bảng để thêm hàng hóa.”'),
       ('Thông báo dưới bảng', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        '- “Chưa có hàng hoá nào để xuất.” khi bấm gửi mà không có dòng hàng nào nhập được.'),
       ('Nút Gửi duyệt', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → kiểm tra, hỏi xác nhận rồi gửi phiếu', '- Khóa trong lúc đang gửi']),
       ('Nút Lưu và tiếp tục', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Rê chuột: “Gửi duyệt phiếu này rồi tiếp tục lập phiếu mới”', '- Gửi duyệt xong ở lại màn với form trống',
         '- Khóa trong lúc đang gửi']),
       ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị',
        '- Bấm → về màn danh sách (lối vào chung); đã nhập dở thì hỏi xác nhận.'),
       ('Hộp Xác nhận gửi duyệt', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tiêu đề “Xác nhận gửi duyệt”',
         '- Nội dung “Gửi duyệt phiếu yêu cầu xuất hàng mượn này? Sau khi gửi, phiếu không sửa được nữa.”',
         '- Nút Gửi duyệt và nút Hủy']),
       ('Hộp Thông tin chưa lưu', 'Popup', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Tiêu đề “Thông tin chưa lưu”', '- Nội dung “Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?”',
         '- Nút Thoát và nút Ở lại']),
       ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Chữ đỏ ngay dưới ô lỗi, ô đổi viền đỏ', '- Chỉ hiện sau lần bấm Gửi duyệt đầu tiên']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Yêu cầu của bạn đã được gửi.”', '- Thiếu dữ liệu: “Bạn chưa nhập đầy đủ thông tin.”',
         '- Máy chủ từ chối: câu lỗi đầu tiên máy chủ trả về', '- Lỗi khác: “Đã có lỗi xảy ra”']),
   ],
   ev=[
       ('Bấm Tạo mới', 'Click',
        'Before:\n– Không cần quyền riêng.\n'
        'During:\n– Khởi tạo form trống, ghi nhận người tạo là người đăng nhập.\n'
        'After:\n– Mở màn Thêm mới: Phiếu xuất mượn trống, Ghi chú trống, chưa có file, bảng Chi tiết rỗng.'),
       ('Bấm Thêm tài liệu, chọn file', 'Click',
        'Before:\n– Không cần quyền riêng; chỉ nhận file PDF.\n'
        'During:\n– Không phải PDF → “File "<tên>" không thuộc định dạng cho phép”.\n'
        '– Quá 20 MB → “File "<tên>" vượt quá 20MB”.\n'
        '– Tải lên thất bại → “Tải lên thất bại: <tên>” hoặc câu lỗi của máy chủ.\n' + ERR + '\n'
        'After:\n– Tải file lên kho lưu trữ, hiện tên và dung lượng, xem trước được.'),
       ('Bấm + và chọn hàng trong cửa sổ Thêm hàng hoá', 'Click',
        'Before:\n– Cửa sổ chỉ cho chọn hàng hóa có trong danh mục.\n'
        'During:\n– Hàng đã có trong phiếu → bỏ qua, báo “Hàng hóa đã có trong phiếu: <tên>”.\n'
        '– Hàng tạm → bỏ qua, báo “Bỏ qua "<tên>": phiếu xuất hàng mượn chỉ nhận hàng hóa có trong danh mục '
        '(không nhận hàng tạm)”.\n'
        '– Không tải được đơn vị tính → “Lỗi khi tải đơn vị tính của hàng "<tên>"”.\n'
        'After:\n– Thêm dòng hàng, nạp đơn vị tính và giá, rải chi tiết theo các phiếu mượn đã chọn.'),
       ('Đổi Đơn vị tính', 'Change',
        'Before:\n– Chỉ đổi được ở dòng hàng đã nạp đơn vị tính.\n'
        'During:\n– Lấy hệ số và giá của đơn vị mới.\n'
        'After:\n– Tính lại Đơn giá, Đang mượn của mọi dòng con.\n'
        '– Số Xuất vượt Đang mượn mới → tự kéo về bằng Đang mượn; tính lại Thành tiền, Tổng cộng.'),
       ('Nhập số Xuất', 'Change',
        'Before:\n– Chỉ nhập được ở dòng hàng có phiếu mượn (dòng không bị khóa).\n'
        'During:\n– Không phải số → “Không hợp lệ”; âm → “Phải lớn hơn hoặc bằng 0”.\n'
        '– Lớn hơn 999999 → “Không được vượt quá 6 chữ số”; lớn hơn Đang mượn → “Vượt quá số đang mượn”.\n'
        'After:\n– Tính lại Số lượng xuất, Thành tiền của dòng và dòng Tổng cộng.'),
       ('Bấm Gửi duyệt hoặc Lưu và tiếp tục', 'Click',
        'Before:\n– Không cần quyền riêng; chỉ nhận phiếu mượn do chính người dùng lập (BR-01).\n'
        '– Khóa hai nút trong lúc gửi.\n'
        'During:\n– Chưa chọn phiếu xuất mượn → “Bắt buộc phải chọn ít nhất 1 phiếu xuất mượn”.\n'
        '– Ghi chú trống → “Bắt buộc phải nhập”.\n'
        '– Chưa có file → “Bắt buộc phải đính kèm ít nhất 1 file”.\n'
        '– Không có dòng hàng nhập được → “Chưa có hàng hoá nào để xuất.”; dòng chưa nhập số → “Chưa nhập số '
        'lượng xuất”.\n'
        '– Có lỗi → thông báo “Bạn chưa nhập đầy đủ thông tin.”, con trỏ về ô lỗi đầu tiên, dừng.\n'
        '– Hiện hộp “Xác nhận gửi duyệt”; bấm Hủy thì dừng.\n'
        '– Máy chủ kiểm tra lại: phiếu mượn không còn hợp lệ → “Có yêu cầu xuất mượn không hợp lệ!”; vượt số '
        'đang mượn → “Số lượng vượt quá số đang mượn (n).”; hàng chưa nhập số → “Hàng hoá "<tên>" chưa nhập số '
        'lượng xuất.”; tổng bằng 0 → “Chưa có hàng hoá nào để xuất.”; đơn vị sai → “Đơn vị tính không thuộc '
        'hàng hoá này.”.\n' + ERR + '\n'
        'After:\n– Sinh mã PYCXHM-NNNNN, lưu phiếu ở trạng thái Chờ duyệt kèm công ty, phòng ban của người lập.\n'
        '– Ghi một dòng lịch sử “Tạo mới” (kèm đủ dòng hàng, chi tiết theo phiếu mượn).\n'
        '– Gửi thông báo “[YCXHM] Chờ duyệt: <mã>” (số mặt hàng, tổng tiền, người lập, ghi chú) cho Kế toán kho '
        'cùng công ty.\n'
        '– Hiển thị “Yêu cầu của bạn đã được gửi.”; Gửi duyệt → về danh sách, Lưu và tiếp tục → form trống.'),
       ('Bấm Quay lại hoặc rời màn', 'Click',
        'Before:\n– Kiểm tra form có thay đổi chưa gửi.\n'
        'During:\n– Có thay đổi → hiện hộp “Thông tin chưa lưu”.\n'
        'After:\n– Ở lại: giữ nguyên dữ liệu; Thoát hoặc chưa nhập gì: về màn danh sách.'),
   ])

# ------------------------------------------------------------ 2.6
fr(6, 'Chọn phiếu xuất mượn', usecase=('FR-06', 'Chọn phiếu xuất mượn', 'crud', A_LAP),
   rule=('- Kịch bản tìm kiếm, Bộ lọc và Phân trang.', 'search'),
   intro=dict(
       ten='Chọn phiếu xuất mượn đưa vào phiếu yêu cầu',
       mota='Cửa sổ liệt kê các phiếu xuất mượn đủ điều kiện của chính người lập (BR-01) để chọn từng phiếu đưa '
            'vào phiếu yêu cầu. Chọn phiếu chỉ nạp số còn mượn cho các dòng hàng, không tự sinh dòng hàng.',
       tacnhan=TN_MOI,
       dieukien='1. Người dùng đăng nhập thành công.\n'
                '2. Chức năng không gắn quyền riêng; chỉ thấy phiếu mượn do chính mình lập.\n'
                '3. Người dùng đang ở màn Thêm yêu cầu xuất hàng mượn.',
       chinh='1. Người dùng bấm Thêm phiếu.\n'
             '2. Hệ thống mở cửa sổ “Chọn phiếu xuất mượn”, 10 phiếu / trang, phiếu tạo gần nhất xếp trên.\n'
             '3. Người dùng nhập mã nếu cần rồi bấm Tìm kiếm (hoặc Enter).\n'
             '4. Người dùng bấm vào một dòng phiếu “Bấm để chọn”.\n'
             '5. Hệ thống kiểm tra lại phiếu, nạp hàng còn mượn của phiếu.\n'
             '6. Hệ thống thêm thẻ mã vào ô Phiếu xuất mượn, báo “Thêm thành công.”; dòng đổi sang “Đã chọn”, '
             'cửa sổ vẫn mở để chọn tiếp.',
       phu='• Bấm dòng phiếu đã chọn → không làm gì (rê chuột: “Phiếu này đã được chọn”); muốn bỏ thì bấm × ở thẻ '
           'mã ngoài form.\n'
           '• Phiếu vừa hết điều kiện → “Không thể chọn phiếu này: phiếu không phải phiếu xuất mượn đang mượn '
           'của bạn.”.\n'
           '• Phiếu không còn tồn tại → “Không tìm thấy phiếu xuất mượn.”.\n'
           '• Không có phiếu → bảng hiện “Không có phiếu xuất mượn phù hợp.”.\n'
           '• Lỗi tải danh sách → “Không tải được danh sách phiếu xuất mượn”.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng cửa sổ; các phiếu đã chọn vẫn giữ trên form.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Tạo mới => Thêm phiếu', shot=shot('11_picker'),
               shot_caption='Cửa sổ Chọn phiếu xuất mượn',
               note='Modal Chọn phiếu xuất mượn được mở ngay trên màn hình Thêm yêu cầu xuất hàng mượn theo đường dẫn ở trên.'),
   extra=[(shot('10c_after_pick'), 'Màn Thêm mới sau khi chọn phiếu xuất mượn')],
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn phiếu xuất mượn”.'),
       ('Dòng mô tả', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Chỉ hiện phiếu yêu cầu xuất hàng loại Xuất mượn do bạn lập, đang ở trạng thái Đã mượn và còn hàng chưa '
        'trả hết”.'),
       ('Mã phiếu xuất mượn', 'Textbox', 'Enable', '0–255 ký tự', 'Không', 'Trống',
        ['- Gợi ý “Nhập mã phiếu xuất mượn”', '- Tìm theo một phần mã', '- Enter = bấm Tìm kiếm']),
       ('Nút Tìm kiếm', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → lọc theo mã đã nhập, về trang 1.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → xóa ô mã, nạp lại từ trang 1.'),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Đánh số liên tục theo trang.'),
       ('Cột Mã phiếu xuất mượn', 'Table/Grid', 'Read-only', 'PYCXH-…', '–', 'Theo dữ liệu',
        '- Mã phiếu yêu cầu xuất hàng loại Xuất mượn.'),
       ('Cột Ngày tạo', 'Table/Grid', 'Read-only', 'dd/mm/yyyy', '–', 'Theo dữ liệu', '- Ngày lập phiếu mượn; trống hiện “—”.'),
       ('Cột Trạng thái', 'Table/Grid', 'Read-only', '–', '–', 'Bấm để chọn',
        ['- “Bấm để chọn”: dòng bấm được, rê chuột “Bấm để chọn phiếu này”',
         '- “Đã chọn”: phiếu đã có trên form, dòng tô khác màu']),
       ('Dòng phiếu', 'Table/Grid', 'Enable', '–', '–', 'Theo dữ liệu',
        '- Bấm vào bất kỳ chỗ nào trên dòng → chọn phiếu (dòng “Đã chọn” bấm không có tác dụng).'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Đang nạp: “Đang tải...”', '- Không có phiếu: “Không có phiếu xuất mượn phù hợp.”']),
       ('Phân trang', 'Pagination', 'Enable', '10, 20, 50, 100', '–', 'Trang 1, 10 dòng',
        ['- Dòng “Hiển thị a–b / N phiếu”', '- Ô Số dòng/trang: mặc định 10, lựa chọn 10 / 20 / 50 / 100',
         '- Ẩn khi không có phiếu']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo kết quả chọn', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Thêm thành công.”', '- Thất bại: câu lỗi máy chủ trả về (xem Dòng sự kiện phụ)']),
   ],
   ev=[
       ('Mở cửa sổ', 'System',
        'Before:\n– Chỉ lấy phiếu do chính người đăng nhập lập.\n'
        'During:\n– Lấy phiếu mượn đủ điều kiện (BR-01), 10 dòng / trang, mới tạo xếp trên.\n'
        '– Lỗi → “Không tải được danh sách phiếu xuất mượn”.\n'
        'After:\n– Hiển thị bảng; phiếu đã có trên form hiện “Đã chọn”.'),
       ('Bấm Tìm kiếm hoặc Enter ở ô mã', 'Click',
        'Before:\n– Giữ số dòng/trang đang chọn.\nAfter:\n– Lọc theo mã, về trang 1.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Giữ số dòng/trang đang chọn.\nAfter:\n– Xóa ô mã, nạp lại từ trang 1.'),
       ('Bấm một dòng phiếu', 'Click',
        'Before:\n– Dòng đã chọn → không làm gì, dừng.\n'
        'During:\n– Máy chủ kiểm tra lại: không tồn tại → “Không tìm thấy phiếu xuất mượn.”; không còn đủ điều kiện '
        '→ “Không thể chọn phiếu này: phiếu không phải phiếu xuất mượn đang mượn của bạn.”.\n' + ERR + '\n'
        'After:\n– Thêm thẻ mã vào ô Phiếu xuất mượn, nạp hàng còn mượn của phiếu vào các dòng hàng đã có (giữ số '
        'Xuất đã nhập), báo “Thêm thành công.”.'),
       ('Đổi trang hoặc số dòng/trang', 'Click',
        'Before:\n– Giữ ô mã đang lọc.\nAfter:\n– Nạp trang mới; đổi số dòng thì về trang 1.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận.\n'
        'After:\n– Đóng cửa sổ; các phiếu đã chọn vẫn giữ trên form.'),
   ])

# ------------------------------------------------------------ 2.7
fr(7, 'Xem chi tiết phiếu', usecase=('FR-07', 'Xem chi tiết phiếu', 'view', A_LAP),
   rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'),
   intro=dict(
       ten='Xem chi tiết phiếu yêu cầu xuất hàng mượn',
       mota='Xem toàn bộ thông tin phiếu ở chế độ chỉ đọc: phiếu mượn đã gom, ghi chú, file đính kèm, bảng hàng '
            'theo từng phiếu mượn, số Được duyệt, lý do từ chối và lịch sử. Màn hiện thêm nút Tạo phiếu xuất '
            'hàng mượn / Từ chối cho Kế toán kho khi phiếu Chờ duyệt.',
       tacnhan=TN_XEM,
       dieukien='1. Người dùng đăng nhập thành công.\n'
                '2. Người dùng được xem phiếu theo phạm vi quyền (BR-04).',
       chinh='1. Người dùng bấm Mã phiếu ở danh sách (hoặc nút Duyệt trên dòng, hoặc bấm thông báo).\n'
             '2. Hệ thống kiểm tra phiếu tồn tại và quyền xem.\n'
             '3. Hệ thống mở màn “Chi tiết yêu cầu xuất hàng mượn: <mã>”.\n'
             '4. Hệ thống hiển thị Thông tin chung, File đính kèm, Chi tiết, Ghi chú duyệt (nếu có), khối Lịch sử '
             'thu gọn và các nút theo quyền, trạng thái.',
       phu='• Phiếu không tồn tại → “Không tìm thấy dữ liệu”, về danh sách.\n'
           '• Không được xem → “Bạn không có quyền xem phiếu này”, về danh sách.\n'
           '• Lỗi khác khi tải → “Không tải được chi tiết phiếu.” hoặc câu lỗi của máy chủ, về danh sách.\n'
           '• Phiếu không có file đính kèm → không hiện khối File đính kèm.\n'
           '• Bấm Quay lại → về màn trước đó; mở thẳng bằng đường dẫn / thông báo / tab mới → về danh sách lối vào chung.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Xem chi tiết', shot=shot('17_detail'),
               shot_caption='Màn chi tiết phiếu đang Chờ duyệt (tài khoản Kế toán kho)'),
   extra=[(shot('17b_detail_rej'), 'Màn chi tiết phiếu Không duyệt, có khối Ghi chú duyệt')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề màn', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '- “Chi tiết yêu cầu xuất hàng mượn: <mã phiếu>”.'),
       ('Người tạo – Ngày tạo', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        '- Góc phải khối Thông tin chung, dạng “<Họ tên> - dd/mm/yyyy hh:mm”.'),
       ('Phiếu xuất mượn', 'Link', 'Read-only', '–', 'Theo dữ liệu',
        ['- Thẻ mã từng phiếu mượn kèm biểu tượng mở ngoài', '- Bấm → mở chi tiết phiếu yêu cầu xuất hàng ở tab mới']),
       ('Ghi chú', 'Textarea', 'Read-only', '0–255 ký tự', 'Theo dữ liệu', '- Ghi chú người lập; trống hiện “—”.'),
       ('Phòng ban yêu cầu', 'Textbox', 'Read-only', '–', 'Theo dữ liệu',
        '- Phòng ban ghi trên phiếu lúc lập; thiếu thì lấy phòng ban hiện tại của người tạo.'),
       ('Khối File đính kèm', 'Table/Grid', 'Read-only', '–', 'Ẩn khi không có file',
        ['- Cột STT, tên file, Dung lượng', '- Nút Xem trước, Tải xuống trên từng file; không có nút xóa']),
       ('Cột STT', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Bảng Chi tiết: số thứ tự dòng hàng.'),
       ('Cột Tên hàng hóa', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Tên kèm dòng phụ Model, Mã, Thương hiệu.'),
       ('Cột Đơn vị tính', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '- Đơn vị người lập đã chọn.'),
       ('Cột Đơn giá', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '- Đơn giá lưu lúc gửi phiếu, định dạng 1,234,567.'),
       ('Cột Số lượng', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '- Tổng số Xuất của dòng hàng.'),
       ('Cột Phiếu mượn', 'Link', 'Read-only', '–', 'Theo dữ liệu',
        ['- Mỗi phiếu mượn 1 dòng con', '- Bấm mã → mở chi tiết phiếu yêu cầu xuất hàng',
         '- Dòng hàng không gắn phiếu nào: 3 ô gộp “Chưa có phiếu mượn”']),
       ('Cột Xuất', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '- Số người lập xin xuất trên phiếu mượn đó.'),
       ('Cột Được duyệt', 'Table/Grid', 'Read-only', '≥ 0', '0',
        ['- Số Kế toán kho chấp nhận khi lập phiếu xuất hàng mượn', '- 0 khi phiếu chưa duyệt']),
       ('Cột Thành tiền', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '- Số lượng × Đơn giá.'),
       ('Dòng Tổng cộng', 'Table/Grid', 'Read-only', '≥ 0', 'Theo dữ liệu', '- Tổng Số lượng và tổng Thành tiền.'),
       ('Trạng thái rỗng bảng Chi tiết', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Không có hàng hóa”.'),
       ('Khối Ghi chú duyệt', 'Textarea', 'Read-only', '0–255 ký tự', 'Ẩn',
        '- Chỉ hiện khi phiếu có lý do từ chối; nội dung là lý do Kế toán kho nhập.'),
       ('Khối Lịch sử', 'Table/Grid', 'Read-only', '–', 'Thu gọn',
        ['- Nút “Xem lịch sử” mở khối, đổi thành “Thu gọn”', '- Nội dung như cửa sổ Lịch sử thay đổi (mục 2.12)']),
       ('Nút Tạo phiếu xuất hàng mượn', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Chỉ hiện với Kế toán kho khi phiếu Chờ duyệt', '- Bấm → mở màn lập Phiếu xuất hàng mượn (mục 2.9)']),
       ('Nút In', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở cửa sổ Xem trước phiếu (mục 2.10).'),
       ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', 'Ẩn',
        ['- Màu đỏ; chỉ hiện với Kế toán kho khi phiếu Chờ duyệt', '- Bấm → mở cửa sổ Từ chối (mục 2.8)']),
       ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị',
        '- Bấm → về màn trước đó; mở thẳng bằng đường dẫn thì về danh sách.'),
       ('Thông báo lỗi tải', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Không tìm thấy dữ liệu”', '- “Bạn không có quyền xem phiếu này”', '- “Không tải được chi tiết phiếu.”']),
   ],
   ev=[
       ('Mở màn chi tiết', 'System',
        'Before:\n– Kiểm tra quyền xem (BR-04).\n'
        '– Nếu không được xem → hiển thị “Bạn không có quyền xem phiếu này” và về danh sách.\n'
        'During:\n– Phiếu không tồn tại → “Không tìm thấy dữ liệu”, về danh sách.\n'
        '– Lỗi khác → “Không tải được chi tiết phiếu.”, về danh sách.\n'
        'After:\n– Hiển thị dữ liệu; nút Tạo phiếu xuất hàng mượn và Từ chối chỉ hiện khi Kế toán kho + Chờ duyệt.'),
       ('Bấm mã phiếu mượn', 'Click',
        'Before:\n– Thẻ mã ở Thông tin chung mở tab mới; mã trong bảng Chi tiết mở ngay trên tab hiện tại.\n'
        'After:\n– Mở chi tiết phiếu yêu cầu xuất hàng tương ứng.'),
       ('Bấm Xem lịch sử', 'Click',
        'Before:\n– Người dùng đã được xem phiếu.\nAfter:\n– Mở khối Lịch sử, nạp các mốc ở lần mở đầu tiên.'),
       ('Bấm Xem trước / Tải xuống file', 'Click', 'Before:\n– Khối File đính kèm chỉ hiện khi phiếu có file.\nAfter:\n– Mở xem trước PDF hoặc tải file về máy.'),
       ('Bấm Quay lại', 'Click',
        'Before:\n– Xác định màn đứng trước.\n'
        'After:\n– Về màn trước đó; không có màn trước thì về danh sách lối vào chung.'),
   ])

# ------------------------------------------------------------ 2.8
fr(8, 'Từ chối phiếu', usecase=('FR-08', 'Từ chối phiếu', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Từ chối phiếu yêu cầu xuất hàng mượn',
       mota='Kế toán kho không duyệt phiếu, bắt buộc nêu lý do. Phiếu sang trạng thái cuối Không duyệt, người lập '
            'được báo kèm lý do và phải lập phiếu mới nếu vẫn cần xuất hàng.',
       tacnhan=TN_KT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán kho.\n'
                '3. Phiếu đang ở trạng thái Chờ duyệt.\n4. Người dùng đang ở màn chi tiết phiếu.',
       chinh='1. Kế toán kho bấm Từ chối ở màn chi tiết.\n'
             '2. Hệ thống mở cửa sổ “Từ chối yêu cầu xuất hàng mượn” kèm “Mã phiếu: <mã>”.\n'
             '3. Kế toán kho nhập Lý do từ chối, bấm Xác nhận từ chối.\n'
             '4. Hệ thống kiểm tra lại quyền và trạng thái phiếu.\n'
             '5. Hệ thống chuyển phiếu sang Không duyệt, lưu lý do, người và thời điểm từ chối.\n'
             '6. Hệ thống ghi nhận hành động “Không duyệt” kèm lý do trong lịch sử của phiếu.\n'
             '7. Hệ thống gửi thông báo cho người lập phiếu.\n'
             '8. Hệ thống báo “Thao tác thành công.” và quay về màn danh sách đã mở trước đó.',
       phu='• Lý do trống → “Bắt buộc phải nhập lý do từ chối” dưới ô, cửa sổ không đóng.\n'
           '• Phiếu vừa được xử lý ở nơi khác hoặc mất quyền → “Phiếu không còn ở trạng thái Chờ duyệt hoặc bạn '
           'không đủ quyền.” dưới ô, không lưu.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng cửa sổ ngay, không hỏi lại, nội dung đã nhập bị bỏ.',
       dacbiet='Phiếu Không duyệt không sửa, không gửi lại được. Cửa sổ nhập lý do đã là bước xác nhận nên không '
               'hỏi xác nhận thêm. Nút Xác nhận từ chối bị khóa trong lúc đang xử lý.'),
   layout=dict(menu=MENU + ' => Xem chi tiết => Từ chối', shot=shot('15_reject'),
               shot_caption='Cửa sổ Từ chối yêu cầu xuất hàng mượn',
               note='Modal Từ chối yêu cầu xuất hàng mượn được mở ngay trên màn hình chi tiết phiếu theo đường dẫn ở trên.'),
   extra=[(shot('15b_reject_err'), 'Lỗi khi bấm Xác nhận từ chối mà chưa nhập lý do')],
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        ['- “Từ chối yêu cầu xuất hàng mượn”', '- Dòng phụ “Mã phiếu: <mã phiếu>”']),
       ('Lý do từ chối', 'Textarea', 'Enable', '1–255 ký tự', 'Có', 'Trống',
        ['- Gợi ý “Nhập lý do không duyệt phiếu...”', '- Không gõ được quá 255 ký tự',
         '- Lỗi dưới ô: “Bắt buộc phải nhập lý do từ chối”']),
       ('Dòng nhắc', 'Label', 'Hiển thị', '–', '–', 'Hiển thị',
        '- “Phiếu sẽ chuyển sang trạng thái Không duyệt và không sửa lại được.”'),
       ('Nút Xác nhận từ chối', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Màu đỏ', '- Bấm → kiểm tra và từ chối phiếu', '- Khóa trong lúc đang xử lý']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng cửa sổ, bỏ nội dung đã nhập.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Thông báo lỗi dưới ô', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- “Bắt buộc phải nhập lý do từ chối”',
         '- “Phiếu không còn ở trạng thái Chờ duyệt hoặc bạn không đủ quyền.”',
         '- Lỗi khác: “Không thực hiện được thao tác”']),
       ('Thông báo thành công', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- “Thao tác thành công.”'),
   ],
   ev=[
       ('Bấm Từ chối ở màn chi tiết', 'Click',
        'Before:\n– Nút chỉ hiện với Kế toán kho khi phiếu Chờ duyệt.\n'
        'During:\n– Quyền và trạng thái được máy chủ kiểm tra lại khi bấm Xác nhận từ chối.\n'
        'After:\n– Mở cửa sổ Từ chối với ô Lý do trống.'),
       ('Bấm Xác nhận từ chối', 'Click',
        'Before:\n– Kiểm tra quyền Kế toán kho và phiếu còn Chờ duyệt.\n'
        '– Nếu không đạt → hiển thị “Phiếu không còn ở trạng thái Chờ duyệt hoặc bạn không đủ quyền.” và dừng xử lý.\n'
        'During:\n– Lý do trống → “Bắt buộc phải nhập lý do từ chối”; quá 255 ký tự → “Không được vượt quá 255 ký tự”.\n'
        + ERR + '\n'
        'After:\n– Chuyển phiếu sang Không duyệt, lưu lý do, người duyệt, ngày duyệt.\n'
        '– Ghi một dòng lịch sử “Không duyệt” (Trạng thái: Chờ duyệt → Không duyệt, kèm lý do).\n'
        '– Gửi thông báo “[YCXHM] Từ chối: <mã>” (người từ chối, lý do) cho người lập.\n'
        '– Hiển thị “Thao tác thành công.”, quay về màn danh sách đã mở trước đó.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click',
        'Before:\n– Không hỏi xác nhận kể cả khi đã nhập lý do.\nAfter:\n– Đóng cửa sổ, không lưu.'),
   ])

# ------------------------------------------------------------ 2.9
fr(9, 'Tạo phiếu xuất hàng mượn (duyệt phiếu)', usecase=('FR-09', 'Tạo phiếu xuất hàng mượn', 'action', A_KT),
   rule=('- Thông báo và Quy tắc ghi lịch sử.', 'notice'),
   intro=dict(
       ten='Duyệt phiếu bằng cách lập Phiếu xuất hàng mượn',
       mota='Kế toán kho chuyển sang màn Phiếu xuất hàng mượn với phiếu yêu cầu này chọn sẵn. Lưu phiếu xuất '
            'thành công chính là duyệt phiếu yêu cầu: phiếu sang Đã duyệt và ghi số Được duyệt cho từng dòng.',
       tacnhan=TN_KT,
       dieukien='1. Người dùng đăng nhập thành công.\n2. Người dùng có quyền Kế toán kho.\n'
                '3. Phiếu đang ở trạng thái Chờ duyệt.',
       chinh='1. Kế toán kho bấm Tạo phiếu xuất hàng mượn ở màn chi tiết (hoặc bấm Duyệt trên dòng danh sách rồi '
             'bấm nút này).\n'
             '2. Hệ thống mở màn lập Phiếu xuất hàng mượn, gắn sẵn phiếu yêu cầu này.\n'
             '3. Kế toán kho lập và lưu phiếu xuất (đặc tả ở SRS màn Phiếu xuất hàng mượn).\n'
             '4. Hệ thống chuyển phiếu yêu cầu sang Đã duyệt, ghi Người duyệt, Ngày duyệt và số Được duyệt.\n'
             '5. Hệ thống ghi nhận hành động “Duyệt” trong lịch sử của phiếu yêu cầu (kèm mã phiếu xuất).\n'
             '6. Hệ thống gửi thông báo cho người lập phiếu yêu cầu.',
       phu='• Kế toán kho thoát màn phiếu xuất không lưu → phiếu yêu cầu vẫn Chờ duyệt.\n'
           '• Phiếu đã Đã duyệt / Không duyệt hoặc người dùng không có quyền Kế toán kho → không hiện nút Tạo phiếu '
           'xuất hàng mượn và nút Duyệt.',
       dacbiet='Màn Yêu cầu xuất hàng mượn không có nút “Duyệt” ghi dữ liệu riêng: thao tác duyệt chỉ xảy ra khi '
               'lưu Phiếu xuất hàng mượn.'),
   layout=dict(menu=MENU + ' => Xem chi tiết => Tạo phiếu xuất hàng mượn', shot=shot('21_borrow_export_create'),
               shot_caption='Màn Lập phiếu xuất hàng mượn mở từ phiếu yêu cầu (phiếu yêu cầu điền sẵn)'),
   ui_kw=dict(required=False, scope=False),
   ui=[
       ('Nút Tạo phiếu xuất hàng mượn', 'Button', 'Enable / Ẩn', 'Ẩn',
        ['- Ở chân màn chi tiết, chỉ hiện với Kế toán kho khi phiếu Chờ duyệt',
         '- Bấm → mở màn lập Phiếu xuất hàng mượn với phiếu yêu cầu này chọn sẵn']),
       ('Nút Duyệt trên dòng danh sách', 'Icon Button', 'Enable / Ẩn', 'Ẩn',
        ['- Ở cột Hành động, cùng điều kiện hiện', '- Bấm → mở màn chi tiết phiếu để duyệt']),
       ('Ô Phiếu yêu cầu trên màn phiếu xuất', 'Label', 'Read-only', 'Mã phiếu yêu cầu',
        '- Màn Phiếu xuất hàng mượn nạp sẵn phiếu yêu cầu và các dòng hàng của phiếu.'),
       ('Cột Được duyệt ở màn chi tiết', 'Table/Grid', 'Read-only', '0',
        '- Sau khi lưu phiếu xuất: số Kế toán kho chấp nhận cho từng dòng chi tiết.'),
       ('Cột Trạng thái ở danh sách', 'Table/Grid', 'Read-only', 'Chờ duyệt',
        '- Sau khi lưu phiếu xuất: đổi sang Đã duyệt (nhãn xanh lá), có Người duyệt, Ngày duyệt.'),
   ],
   ev=[
       ('Bấm Duyệt trên dòng danh sách', 'Click',
        'Before:\n– Nút chỉ hiện với Kế toán kho khi phiếu Chờ duyệt.\n'
        'During:\n– Màn chi tiết kiểm tra lại quyền xem phiếu (BR-04).\n'
        'After:\n– Mở màn chi tiết phiếu.'),
       ('Bấm Tạo phiếu xuất hàng mượn', 'Click',
        'Before:\n– Nút chỉ hiện khi có quyền Kế toán kho và phiếu Chờ duyệt.\n'
        'During:\n– Truyền mã phiếu yêu cầu sang màn Phiếu xuất hàng mượn để nạp sẵn.\n'
        'After:\n– Mở màn lập Phiếu xuất hàng mượn với phiếu yêu cầu chọn sẵn.'),
       ('Lưu Phiếu xuất hàng mượn thành công', 'System',
        'Before:\n– Kiểm tra quyền và trạng thái theo SRS màn Phiếu xuất hàng mượn.\n'
        'During:\n– Lỗi kiểm tra ở màn phiếu xuất → phiếu yêu cầu giữ nguyên Chờ duyệt.\n' + ERR + '\n'
        'After:\n– Phiếu yêu cầu sang Đã duyệt; ghi Người duyệt, Ngày duyệt, số Được duyệt cho từng dòng.\n'
        '– Ghi một dòng lịch sử “Duyệt” (Trạng thái: Chờ duyệt → Đã duyệt; Phiếu xuất hàng mượn: PXHM-…).\n'
        '– Gửi thông báo “[YCXHM] Đã duyệt: <mã>” (phiếu xuất, người duyệt) cho người lập.'),
       ('Thoát màn phiếu xuất không lưu', 'Click', 'Before:\n– Phiếu xuất hàng mượn chưa được lưu.\nAfter:\n– Phiếu yêu cầu giữ nguyên Chờ duyệt.'),
   ])

# ------------------------------------------------------------ 2.10
fr(10, 'In phiếu và in danh sách', usecase=('FR-10', 'In phiếu / In danh sách', 'io', A_LAP),
   rule=('- Màn Danh sách và Quy tắc Excel.', 'list'),
   intro=dict(
       ten='In phiếu yêu cầu xuất hàng mượn / In danh sách',
       mota='Xem trước và in một phiếu (khổ dọc) hoặc in danh sách theo bộ lọc đang áp (khổ ngang). Bản in mở '
            'trong cửa sổ ngay trên màn đang đứng, không mở tab mới nên không mất bộ lọc.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm In ở cột Hành động hoặc ở màn chi tiết (in phiếu), hoặc nút In trên bảng (in danh '
             'sách).\n'
             '2. Hệ thống kiểm tra quyền xem phiếu (in phiếu) hoặc áp bộ lọc + phạm vi quyền (in danh sách).\n'
             '3. Hệ thống mở cửa sổ xem trước, hiện “Đang tải dữ liệu in…” trong lúc dựng bản in.\n'
             '4. Người dùng bấm In để mở hộp thoại in của trình duyệt.',
       phu='• Danh sách khớp bộ lọc quá 2.000 phiếu → không dựng bản in, ẩn nút In, hiện dòng nhắc “Danh sách có '
           '<N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc …”.\n'
           '• Không có dữ liệu → “Không có dữ liệu để in”.\n'
           '• Không được xem phiếu → “Bạn không có quyền xem phiếu này”.\n'
           '• Lỗi khác → “Không tải được dữ liệu in” hoặc câu lỗi của máy chủ.\n'
           '• Bấm (x) / click ra ngoài cửa sổ → đóng cửa sổ xem trước.',
       dacbiet='Logo / tên công ty đầu bản in phiếu lấy theo công ty ghi trên phiếu; bản in danh sách lấy theo công '
               'ty của người đang xem. Bản in danh sách tối đa 2.000 dòng (BR-10).'),
   layout=dict(menu=MENU + ' => In', shot=shot('18_print'), shot_caption='Cửa sổ Xem trước phiếu',
               note='Modal Xem trước được mở ngay trên màn hình danh sách hoặc màn hình chi tiết theo đường dẫn ở trên.'),
   extra=[(shot('19_printlist'), 'Cửa sổ Xem trước danh sách (khổ ngang)')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–',
        ['- In phiếu: “Xem trước phiếu <mã>”', '- In danh sách: “Xem trước danh sách yêu cầu xuất hàng mượn”']),
       ('Nút In', 'Button', 'Enable / Ẩn', '–', 'Hiển thị',
        ['- Cạnh tiêu đề; bấm → mở hộp thoại in của trình duyệt', '- Khóa khi đang tải', '- Ẩn khi danh sách vượt 2.000 dòng']),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Bấm → đóng cửa sổ xem trước.'),
       ('Dòng đang tải', 'Label', 'Hiển thị', '–', 'Ẩn', '- “Đang tải dữ liệu in…” trong lúc dựng bản in.'),
       ('Đầu bản in phiếu', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Logo, tên công ty ghi trên phiếu', '- Tiêu đề “PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN”, Số phiếu, Ngày tạo']),
       ('Thông tin phiếu trên bản in', 'Label', 'Read-only', '–', 'Theo dữ liệu',
        ['- Người lập, phòng ban, phiếu mượn, ghi chú', '- Trạng thái, người duyệt, ngày duyệt']),
       ('Bảng hàng trên bản in phiếu', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu',
        ['- STT, Tên hàng hóa, ĐVT, Số lượng xuất, Đơn giá, Thành tiền', '- Chi tiết theo phiếu mượn',
         '- Số định dạng 1,234,567']),
       ('Chỗ ký', 'Label', 'Read-only', '–', 'Hiển thị', '- Người lập, Kế toán kho.'),
       ('Bản in danh sách', 'Table/Grid', 'Read-only', '≤ 2.000 dòng', 'Theo bộ lọc',
        ['- Khổ ngang; logo công ty của người đang xem', '- Tiêu đề “DANH SÁCH PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN”',
         '- Dòng khoảng ngày “Từ ngày … đến ngày …” khi có lọc Ngày tạo', '- Bảng phiếu kèm tổng số phiếu']),
       ('Dòng nhắc vượt trần in', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        '- “Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc '
        '(khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.”'),
       ('Thông báo lỗi', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn',
        ['- “Không có dữ liệu để in”', '- “Bạn không có quyền xem phiếu này”', '- “Không tải được dữ liệu in”']),
   ],
   ev=[
       ('Bấm In (phiếu)', 'Click',
        'Before:\n– Kiểm tra quyền xem phiếu (BR-04).\n'
        '– Nếu không được xem → hiển thị “Bạn không có quyền xem phiếu này” và dừng xử lý.\n'
        'During:\n– Lỗi dựng bản in → “Không tải được dữ liệu in”.\n'
        'After:\n– Dựng bản xem trước phiếu khổ dọc, letterhead theo công ty ghi trên phiếu.'),
       ('Bấm In (danh sách)', 'Click',
        'Before:\n– Lấy bộ lọc đang áp và lối vào hiện tại.\n'
        'During:\n– Lấy phiếu theo bộ lọc + phạm vi quyền; quá 2.000 dòng → hiện dòng nhắc thu hẹp bộ lọc, ẩn bản '
        'in và nút In.\n– Không có dòng nào → “Không có dữ liệu để in”.\n'
        'After:\n– Dựng bản xem trước danh sách khổ ngang.'),
       ('Bấm In trong cửa sổ xem trước', 'Click',
        'Before:\n– Bản in đã dựng xong.\nAfter:\n– Mở hộp thoại in của trình duyệt.'),
       ('Bấm (x) / click ra ngoài cửa sổ', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ xem trước, giữ nguyên màn đang đứng.'),
   ])

# ------------------------------------------------------------ 2.11
fr(11, 'Xuất danh sách ra Excel', usecase=('FR-11', 'Xuất Excel', 'io', A_LAP),
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'),
   intro=dict(
       ten='Xuất danh sách phiếu ra file Excel',
       mota='Chọn trường và thứ tự cột rồi xuất toàn bộ phiếu khớp bộ lọc đang áp (trong phạm vi quyền, không '
            'phân trang) ra file Excel. Cột STT luôn đứng đầu file.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm Xuất Excel.\n'
             '2. Hệ thống mở cửa sổ “Chọn trường xuất Excel” với 11 trường.\n'
             '3. Người dùng tích trường cần xuất, kéo đổi thứ tự rồi bấm Xuất file.\n'
             '4. Hệ thống lấy toàn bộ phiếu theo bộ lọc + phạm vi quyền, dựng file theo đúng thứ tự trường đã chọn.\n'
             '5. Hệ thống tải file “danh_sach_yeu_cau_xuat_hang_muon.xlsx” về, đóng cửa sổ, báo “Xuất Excel thành công”.',
       phu='• Không có phiếu khớp → vẫn xuất file có tiêu đề và dòng tên cột.\n'
           '• Bỏ tích hết trường → nút Xuất file bị khóa.\n'
           '• Lỗi khi xuất → “Lỗi khi xuất Excel”, cửa sổ giữ nguyên.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → không xuất.',
       dacbiet='Thứ tự cột trong file theo đúng thứ tự trường đã chọn. Nút Xuất Excel và Xuất file bị khóa trong '
               'lúc đang xuất. Không giới hạn số dòng.'),
   layout=dict(menu=MENU + ' => Xuất Excel', shot=shot('20_export'), shot_caption='Cửa sổ Chọn trường xuất Excel',
               note='Modal Chọn trường xuất Excel được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Hiển thị', '- “Chọn trường xuất Excel”.'),
       ('Danh sách trường', 'Table/Grid', 'Enable', 'Danh sách 11 trường', 'Ít nhất 1', 'Tích tất cả',
        ['- Mã phiếu, Người tạo, Ngày tạo, Trạng thái, Người duyệt, Ngày duyệt',
         '- Người cập nhật, Ngày cập nhật, Phòng ban, Ghi chú, Lý do từ chối']),
       ('Ô tích từng trường', 'Checkbox', 'Enable', '–', 'Ít nhất 1', 'Đang tích', '- Bỏ tích → trường không có trong file.'),
       ('Biểu tượng kéo thả', 'Icon Button', 'Enable', '–', '–', 'Hiển thị',
        '- Rê chuột: “Kéo để đổi vị trí cột trong file”.'),
       ('Nút Chọn tất cả', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → tích mọi trường.'),
       ('Nút Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → bỏ tích mọi trường.'),
       ('Dòng “Đang chọn n/11 trường”', 'Label', 'Read-only', '–', '–', 'Theo lựa chọn',
        '- n = số trường đang tích.'),
       ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị',
        ['- Bấm → tải file Excel', '- Khóa khi chưa tích trường nào hoặc đang xuất']),
       ('Nút Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Bấm → đóng, không xuất.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
       ('Nội dung file Excel', 'Table/Grid', 'Read-only', '–', '–', 'Theo bộ lọc',
        ['- Dòng tiêu đề “DANH SÁCH PHIẾU YÊU CẦU XUẤT HÀNG MƯỢN”',
         '- Dòng “Từ ngày … đến ngày …” khi có lọc Ngày tạo', '- Dòng tên cột: STT + các trường đã chọn']),
       ('Thông báo kết quả', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn',
        ['- Thành công: “Xuất Excel thành công”', '- Thất bại: “Lỗi khi xuất Excel”']),
   ],
   ev=[
       ('Bấm Xuất Excel', 'Click',
        'Before:\n– Nút không bị khóa (không có lượt xuất đang chạy).\n'
        'During:\n– Dựng lại danh sách 11 trường theo thứ tự thiết kế.\nAfter:\n– Mở cửa sổ, tích sẵn 11 trường.'),
       ('Kéo biểu tượng kéo thả', 'Drag', 'Before:\n– Kéo bằng biểu tượng kéo thả của trường.\nAfter:\n– Đổi thứ tự trường; thứ tự này là thứ tự cột trong file.'),
       ('Bấm Xuất file', 'Click',
        'Before:\n– Có ít nhất 1 trường được tích.\n– Khóa nút trong lúc xuất.\n'
        'During:\n– Lấy toàn bộ phiếu theo bộ lọc + phạm vi quyền.\n'
        '– Lỗi → “Lỗi khi xuất Excel”.\n' + ERR + '\n'
        'After:\n– Tải file “danh_sach_yeu_cau_xuat_hang_muon.xlsx”, đóng cửa sổ, báo “Xuất Excel thành công”.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ, không xuất.'),
   ])

# ------------------------------------------------------------ 2.12
fr(12, 'Xem lịch sử thay đổi',
   rule=('- Quy tắc ghi lịch sử.', 'history'),
   intro=dict(
       ten='Xem lịch sử thay đổi của phiếu',
       mota='Xem các mốc Tạo mới, Duyệt, Không duyệt của phiếu: người thực hiện, thời điểm và nội dung thay đổi. '
            'Cửa sổ ở danh sách và khối Lịch sử ở màn chi tiết dùng chung một nội dung, mới nhất ở trên.',
       tacnhan=TN_XEM, dieukien=DK_XEM,
       chinh='1. Người dùng bấm Lịch sử ở cột Hành động, hoặc Xem lịch sử ở khối Lịch sử màn chi tiết.\n'
             '2. Hệ thống mở cửa sổ “Lịch sử thay đổi: Phiếu <mã>” và nạp các mốc của phiếu.\n'
             '3. Hệ thống hiển thị các mốc, mới nhất ở trên.',
       phu='• Bấm Bộ lọc → mở các ô Loại hành động, Người thực hiện, Từ ngày, Đến ngày; chọn là lọc ngay.\n'
           '• Không có mốc khớp bộ lọc → “Không có lịch sử phù hợp bộ lọc.”.\n'
           '• Bấm Làm mới trong khối lọc → xóa điều kiện lọc.\n'
           '• Bấm Đóng / (x) / click ra ngoài cửa sổ → đóng cửa sổ.',
       dacbiet=None),
   layout=dict(menu=MENU + ' => Lịch sử', shot=shot('16_history'), shot_caption='Cửa sổ Lịch sử thay đổi',
               note='Modal Lịch sử thay đổi được mở ngay trên màn hình danh sách theo đường dẫn ở trên.'),
   extra=[(shot('17c_detail_history'), 'Khối Lịch sử ở màn chi tiết phiếu')],
   ui_kw=dict(required=False),
   ui=[
       ('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', '- “Lịch sử thay đổi: Phiếu <mã phiếu>”.'),
       ('Danh sách mốc', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', [
           '- Mỗi mốc: thời điểm, hành động, “Người thực hiện: <tên> — <phòng ban>”',
           '- Tạo mới: thông tin phiếu và dòng hàng lúc gửi',
           '- Duyệt: “Trạng thái: Chờ duyệt → Đã duyệt” và mã phiếu xuất hàng mượn',
           '- Không duyệt: “Trạng thái: Chờ duyệt → Không duyệt” và lý do', '- Mới nhất ở trên']),
       ('Nút Bộ lọc', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → mở / thu gọn khối ô lọc.'),
       ('Loại hành động', 'Dropdown', 'Enable', 'Danh sách hành động', 'Trống',
        ['- Gợi ý “Chọn loại hành động”', '- Mặc định: trống (mọi hành động)', '- Chọn là lọc ngay']),
       ('Người thực hiện', 'Dropdown', 'Enable', 'Danh sách người đã thao tác', 'Trống',
        ['- Gợi ý “Chọn người thực hiện”', '- Mặc định: trống', '- Chọn là lọc ngay']),
       ('Từ ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Gợi ý “Từ ngày”; lọc mốc từ ngày này.'),
       ('Đến ngày', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Trống', '- Gợi ý “Đến ngày”; lọc mốc đến hết ngày này.'),
       ('Nút Làm mới', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → xóa điều kiện lọc.'),
       ('Trạng thái rỗng', 'Label', 'Hiển thị', '–', 'Ẩn',
        ['- Phiếu chưa có mốc: “Chưa có lịch sử thao tác nào.”', '- Lọc không ra: “Không có lịch sử phù hợp bộ lọc.”']),
       ('Nút Đóng', 'Button', 'Enable', '–', 'Hiển thị', '- Bấm → đóng cửa sổ.'),
       ('Nút (x)', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Góc phải tiêu đề; giống nút Đóng.'),
   ],
   ev=[
       ('Mở lịch sử', 'Click',
        'Before:\n– Người dùng được xem phiếu (danh sách đã lọc theo phạm vi quyền).\n'
        'During:\n– Nạp các mốc lịch sử của phiếu; chưa có mốc → “Chưa có lịch sử thao tác nào.”.\n'
        'After:\n– Hiển thị các mốc, mới nhất trên.'),
       ('Đổi điều kiện Bộ lọc', 'Change',
        'Before:\n– Không có nút Tìm kiếm: chọn giá trị là lọc.\nAfter:\n– Lọc lại danh sách mốc.'),
       ('Bấm Làm mới', 'Click', 'Before:\n– Khối lọc đang mở.\nAfter:\n– Xóa điều kiện lọc, hiện lại đủ các mốc.'),
       ('Bấm Đóng / (x) / click ra ngoài cửa sổ', 'Click', 'Before:\n– Không hỏi xác nhận.\nAfter:\n– Đóng cửa sổ.'),
   ])

# ============================================================== PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('. Phần này chỉ ghi các quy tắc đặc thù của màn Yêu cầu xuất hàng mượn; không lặp lại các quy tắc '
           'đã có trong SRS quy tắc chung.', anchor='list', head='Quy tắc áp dụng',
           lead='Các quy tắc nghiệp vụ dùng chung được định nghĩa tại SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phiếu xuất mượn được chọn', [
        '– Là phiếu yêu cầu xuất hàng loại Xuất mượn, do CHÍNH người lập phiếu này lập.',
        '– Đã xuất kho và đang ở trạng thái Đã mượn; chỉ lấy dòng hàng còn số chưa trả.',
        '– Một phiếu yêu cầu gom được nhiều phiếu mượn; mỗi phiếu mượn chỉ chọn 1 lần trong cùng phiếu.',
        '– Máy chủ kiểm tra lại điều kiện lúc chọn và lúc gửi.'], ['Lập phiếu', 'Chọn phiếu xuất mượn']),
    ('BR-02', 'Số lượng Đang mượn được phép xuất', [
        '– Đang mượn = đã xuất − đã trả − phần đang chờ ở các phiếu chưa duyệt khác (yêu cầu nhập trả hàng, '
        'yêu cầu xuất bán hàng mượn, yêu cầu xuất hàng mượn khác đang Chờ duyệt).',
        '– Quy theo hệ số đơn vị tính đang chọn, làm tròn xuống.',
        '– Số Xuất là số nguyên 0 – Đang mượn; máy chủ tính lại ngay trước khi lưu.'], ['Lập phiếu']),
    ('BR-03', 'Dòng hàng hợp lệ khi gửi', [
        '– Chỉ dòng hàng có trên ít nhất 1 phiếu mượn đã chọn mới được gửi; dòng “Chưa có phiếu mượn” bị bỏ qua.',
        '– Mỗi dòng gửi đi phải có tổng số Xuất > 0; tổng cả phiếu phải > 0.',
        '– Chỉ nhận hàng hóa có trong danh mục, không nhận hàng tạm; mỗi hàng 1 dòng.'], ['Lập phiếu']),
    ('BR-04', 'Phạm vi xem phiếu', [
        '– Người lập luôn xem được phiếu của mình.',
        '– Kế toán kho và V1 xem mọi phiếu đã gửi; V2 xem phiếu cùng công ty; V3 xem phiếu thuộc phòng ban mình quản lý.',
        '– Phiếu Đang tạo (dữ liệu cũ) chỉ người lập xem được.',
        '– Danh sách, màn chi tiết, in, xuất Excel dùng chung một phạm vi.'],
     ['Xem danh sách', 'Xem chi tiết', 'In', 'Xuất Excel', 'Lịch sử']),
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
        '– Gửi phiếu → báo Kế toán kho cùng công ty với phiếu.',
        '– Duyệt / Không duyệt → báo người lập (kèm mã phiếu xuất / lý do).',
        '– Bấm thông báo → mở màn chi tiết phiếu.'],
     ['Lập phiếu', 'Từ chối', 'Tạo phiếu xuất hàng mượn']),
    ('BR-08', 'Thao tác xong quay về danh sách', [
        '– Gửi duyệt và Từ chối thành công đều quay về màn danh sách (Từ chối: đúng lối vào đã mở trước đó).',
        '– Lưu và tiếp tục: gửi xong ở lại màn Thêm mới với form trống.'],
     ['Lập phiếu', 'Từ chối']),
    ('BR-09', 'Đơn giá và công ty của phiếu', [
        '– Đơn giá lấy theo bảng giá bán của công ty ghi trên phiếu, theo đơn vị tính đang chọn.',
        '– Máy chủ lấy lại đơn giá, hệ số đơn vị từ danh mục lúc lưu, không nhận số do màn hình gửi lên.',
        '– Công ty, phòng ban của phiếu lấy theo người lập tại thời điểm lập.'], ['Lập phiếu']),
    ('BR-10', 'File đính kèm, in và xuất', [
        '– Bắt buộc ít nhất 1 file; chỉ nhận PDF, tối đa 20 MB / file.',
        '– Bản in danh sách tối đa 2.000 dòng; vượt thì không in, nhắc thu hẹp bộ lọc.',
        '– Xuất Excel không giới hạn số dòng; không có phiếu vẫn xuất file có tiêu đề và tên cột.'],
     ['Lập phiếu', 'In', 'Xuất Excel']),
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
