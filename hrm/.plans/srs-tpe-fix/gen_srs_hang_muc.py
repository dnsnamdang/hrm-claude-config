# -*- coding: utf-8 -*-
"""Sinh "SRS - Hạng mục giải pháp.docx" theo FORM CHUẨN (srs-documenter) — KHỔ NGANG.

Chạy:  /opt/homebrew/bin/python3 gen_srs_hang_muc.py
Nguồn đối chiếu code (nhánh gop_db):
  FE  pages/assign/solution-modules/{index.vue, constants.js, _id/manager.vue, _id/components/*}
      pages/assign/solutions/components/{ModulesTab.vue, manager/ModuleApprovalModal.vue, manager/ProgressTab.vue}
      pages/assign/solutions/_id/edit.vue · components/modal/solution-module-version-modal.vue
      components/menu-sidebar.js (Làm giải pháp › Hạng mục giải pháp) · components/subsystems.js (Công việc)
  BE  Modules/Assign/Routes/api.php (prefix assign/solution-modules — không gắn checkPermission)
      Http/Controllers/Api/V1/SolutionModuleController.php · Services/SolutionModuleService.php
      Services/SolutionService.php (syncModules, approve_modules, auto_approve_new_modules, sendLeaderApprovalNotification)
      Entities/{SolutionModule, SolutionModuleReviewProfile}.php · Http/Requests/SolutionModule/*.php
      Services/ProspectiveProjectService.php (đóng dự án → hạng mục Đóng)
Ảnh: hang-muc-shots/ (Playwright Python headless 1440x900, client :3000, dữ liệu local, không ghi DB).
  27-leader-duyet.png lấy lại từ ảnh chụp thật của SRS Quản lý giải pháp (dữ liệu local hiện không có
  giải pháp ở Chờ Leader duyệt). 10/11 dựng popup PM duyệt bằng cách mở component với hồ sơ đặt
  tạm trạng thái Chờ duyệt NGAY TRÊN TRÌNH DUYỆT (không gọi API ghi).
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isdir(os.path.join(ROOT, '.claude', 'skills', 'srs-documenter')):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, '.claude', 'skills', 'srs-documenter', 'assets'))
import srs_docx_lib  # noqa: E402
from srs_docx_lib import SrsDoc  # noqa: E402
from docx.shared import Inches  # noqa: E402
from docx.enum.section import WD_ORIENT  # noqa: E402
from PIL import Image  # noqa: E402

SHOTS = os.path.join(HERE, 'hang-muc-shots')


def shot(name):
    return os.path.join(SHOTS, name)


TEN_MAN = 'Hạng mục giải pháp'
MENU = 'Phân hệ Công việc => Làm giải pháp => Hạng mục giải pháp'
MQL = MENU + ' => Mã hạng mục'                       # vào màn Quản lý hạng mục
MGP = 'Phân hệ Công việc => Làm giải pháp => Quản lý giải pháp => Sửa => Quản lý hạng mục'

A_ALL = 'Người dùng đã đăng nhập'
A_PM = 'PM làm giải pháp'
A_LD = 'Leader hạng mục'
A_TV = 'Người xem hạng mục'

ICONS = {
    'Phân hệ Công việc': 'icon_phanhe_cv.png', 'Làm giải pháp': 'icon_nhom_lgp.png',
    'Hạng mục giải pháp': 'icon_man_hm.png', 'Quản lý giải pháp': 'icon_man_qlgp.png',
    'Sửa': 'icon_sua.png', 'Quản lý hạng mục': 'icon_tab_qlhm.png', 'Thêm hạng mục': 'icon_themhm.png',
    'Lưu và duyệt': 'icon_luuduyet_row.png', 'Lưu và duyệt hạng mục': 'icon_luu_duyet_hm.png',
    'Tìm kiếm nâng cao': 'icon_timkiem.png', 'Cài đặt bộ lọc': 'icon_caidat.png',
    'Cấu hình cột hiển thị': 'icon_cot.png', 'Xuất Excel': 'icon_xuat.png', 'Mã hạng mục': 'icon_ma.png',
    'Thông tin': 'icon_tab_thongtin.png', 'Hồ sơ': 'icon_tab_hoso.png', 'Nhân sự': 'icon_tab_nhansu.png',
    'Nhiệm vụ': 'icon_tab_nhiemvu.png', 'Vấn đề hạng mục': 'icon_tab_vande.png',
    'Meetings': 'icon_tab_meeting.png', 'Tiến độ': 'icon_tab_tiendo.png', 'Files': 'icon_tab_files.png',
    'Ô cảnh báo': 'icon_mo_canh_bao.png', 'Tạo hồ sơ trình duyệt': 'icon_taohoso.png',
    'Xem': 'icon_xem_hs.png', 'Duyệt': 'icon_duyet.png', 'Từ chối': 'icon_tuchoi.png',
    'Thêm nhân sự': 'icon_themnhansu.png', 'Tạo version': 'icon_taoversion.png',
}

OUT = os.path.join(HERE, 'SRS - %s.docx' % TEN_MAN)
d = SrsDoc(out=OUT, menu=MENU, route='', full_url='', img_prefix='hm_')
d.set_menu_icons({k: shot(v) for k, v in ICONS.items()})

# ---------------------------------------------------------------- KHỔ NGANG (khách TPE yêu cầu)
sec = d.doc.sections[0]
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = Inches(11), Inches(8.5)
sec.left_margin = sec.right_margin = Inches(0.75)
sec.top_margin = sec.bottom_margin = Inches(0.8)
USABLE_W = 11 - 1.5          # 9.5 inch
USABLE_H = 8.5 - 1.6 - 0.6   # chừa chỗ caption
SCALE = USABLE_W / 6.0       # bảng của thư viện tính cho vùng in 6 inch → giãn đủ bề rộng trang

_orig_table = SrsDoc.table


def _table(self, headers, rows, widths=None):
    if widths:
        tot = sum(widths)
        widths = [w * USABLE_W / tot for w in widths]
    else:
        widths = [USABLE_W / len(headers)] * len(headers)
    t = _orig_table(self, headers, rows, widths=widths)
    t.autofit = False
    return t


SrsDoc.table = _table
_orig_figure = SrsDoc.figure


def _figure(self, png_path, caption, width_in=6.0):
    w = min(width_in * SCALE, USABLE_W)
    with Image.open(png_path) as im:
        ratio = im.height / float(im.width)
    if w * ratio > USABLE_H:
        w = USABLE_H / ratio
    return _orig_figure(self, png_path, caption, width_in=w)


SrsDoc.figure = _figure

NO_ROLE = '– Không đúng vai trò → nút không hiển thị.'


def L(text):
    """Ô dài viết liền → tách mỗi ý 1 dòng (quy tắc BA 05/10/2026)."""
    if isinstance(text, str) and len(text) > 180 and '\n' not in text:
        parts = [p.strip() for p in re.split(r'(?<=[.;])\s+', text) if p.strip()]
        return ['- ' + p for p in parts]
    return text


# ------------------------------------------------------------------ khung 1 chức năng
_N = [0]


def fn(title, intro, layout, ui, events, uc=None, rule=('- Màn Danh sách, Phân trang và UI/UX.', 'list'),
       ui_kind='input'):
    if not ui or not events:
        raise RuntimeError('Chức năng "%s" thiếu bảng giao diện / event' % title)
    _N[0] += 1
    n = _N[0]
    d.h3('2.%d %s' % (n, title))
    k = 1
    if uc:
        d.p('2.%d.%d Biểu đồ Usecase' % (n, k))
        d.uc_figure(uc[0], uc[1], uc[2], actor=uc[3], caption='Biểu đồ Use Case — %s %s' % (uc[0], uc[1]))
        k += 1
    d.p('2.%d.%d Giới thiệu' % (n, k)); k += 1
    d.rule_ref(rule[0] + ' Chỉ bổ sung các quy tắc riêng của màn Hạng mục giải pháp tại phần mô tả chi tiết.',
               anchor=rule[1])
    d.intro_table(**intro)
    d.p('2.%d.%d Layout màn hình' % (n, k)); k += 1
    first = True
    for item in layout:
        if item[0] == 'menu':
            if first:
                d.p('Đường dẫn màn hình:')
                first = False
            d._menu_para(item[1])
        elif item[0] == 'p':
            d.p(item[1])
        elif item[0] == 'modal':
            d.p('Cửa sổ %s được mở ngay trên màn hình theo đường dẫn ở trên.' % item[1])
        elif item[0] == 'img':
            d.figure(shot(item[1]), item[2], width_in=6.2)
    d.p('2.%d.%d Mô tả chi tiết giao diện' % (n, k)); k += 1
    rows = [tuple(r[:-1]) + (L(r[-1]),) for r in ui]
    need = {'input': 7, 'read': 6}.get(ui_kind, 5)
    bad = [r[0] for r in rows if len(r) != need]
    if bad:
        raise RuntimeError('%s: sai số ô %s' % (title, bad))
    if ui_kind == 'input':
        d.ui_table(rows)
    elif ui_kind == 'read':
        d.ui_table(rows, required=False)
    else:
        d.ui_table(rows, required=False, scope=False)
    d.p('2.%d.%d Danh sách event và xử lý event' % (n, k))
    d.event_table(events)


def ev_close(name='cửa sổ'):
    return ('Bấm nút Đóng / dấu × / phím Esc', 'Click',
            'After:\n– Đóng %s, không lưu dữ liệu, giữ nguyên màn bên dưới.' % name)


def ev_page():
    return [('Chọn trang / Số dòng/trang', 'Change',
             'After:\n– Nạp lại bảng theo trang hoặc số dòng mới (10/20/50…), giữ bộ lọc đang áp.')]


# ======================================================================= TRANG ĐẦU
d.title_block(TEN_MAN)
d.h2('Mục lục')
d.toc()

# ======================================================================= PHẦN 1
d.h1('Phần 1. Giới thiệu')
d.h2('1 Mục đích')
d.p('Tài liệu đặc tả yêu cầu phần mềm cho màn Hạng mục giải pháp (phân hệ Công việc, nhóm Làm giải pháp), '
    'màn Quản lý hạng mục mở từ từng hạng mục, và phần thao tác hạng mục nằm trên form giải pháp. Tài liệu '
    'tách từ SRS Quản lý giải pháp theo yêu cầu của khách hàng, nhằm:')
d.bullets([
    'Là căn cứ nghiệm thu: xem danh sách, tìm kiếm / lọc, cài đặt bộ lọc, tùy chỉnh cột, xuất Excel; khai '
    'hạng mục trên form giải pháp; Leader duyệt hạng mục; PM lưu và duyệt hạng mục bổ sung; màn Quản lý hạng '
    'mục với các tab Thông tin, Hồ sơ, Nhân sự, Nhiệm vụ, Vấn đề hạng mục, Meetings, Tiến độ, Files; hồ sơ '
    'trình duyệt hạng mục (tạo, trình, PM duyệt / từ chối); tạo version hạng mục.',
    'Làm rõ vòng đời trạng thái hạng mục và mối liên hệ với trạng thái giải pháp.',
    'Làm rõ ai thấy hạng mục nào và ai được thao tác gì (theo vai trò trên giải pháp / hạng mục).',
])
d.h2('2 Thuật ngữ và viết tắt')
d.table(['Thuật ngữ', 'Mô tả'], [
    ('Hạng mục (HM)', 'Phần việc con của một giải pháp có tích “Dự án có hạng mục”. Mỗi hạng mục có 1 Leader, '
     'ngày cần hoàn thành, bảng phân công nhân sự, nhiệm vụ, vấn đề, hồ sơ trình duyệt và version riêng.'),
    ('GP', 'Giải pháp kỹ thuật của một dự án tiền khả thi (dự án TKT). Đặc tả ở SRS Quản lý giải pháp.'),
    ('PM', 'PM làm giải pháp của giải pháp chứa hạng mục. Là người duyệt hồ sơ trình duyệt hạng mục.'),
    ('Leader hạng mục', 'Người phụ trách 1 hạng mục: duyệt hạng mục, lập và trình hồ sơ, phân bổ tiến độ.'),
    ('Hồ sơ trình duyệt hạng mục', 'Bộ hồ sơ (tên, nội dung, tài liệu đính kèm, BOM tổng hợp của version hạng '
     'mục) Leader lập để PM duyệt kết quả hạng mục. Mã dạng HS.TD.<Mã hạng mục>.<số thứ tự 3 chữ số>.'),
    ('BOM tổng hợp', 'BOM loại Tổng hợp gắn với version hạng mục; hồ sơ chỉ trình được khi có BOM tổng hợp ở '
     'trạng thái Hoàn thành (trừ dự án Tự triển khai).'),
    ('Version hạng mục', 'Phiên bản V1, V2… của hạng mục. V1 sinh khi tạo hạng mục; tạo version mới khi cần làm '
     'lại sau khi hồ sơ đã duyệt.'),
    ('Dự án Tự triển khai', 'Dự án TKT có Cách triển khai = Tự triển khai (KD tự làm giải pháp).'),
], widths=[2.0, 7.5])

d.h2('3 Định nghĩa')
d.p('Các bảng dưới là nguồn tham chiếu chung cho mọi chức năng ở Phần 3. Chữ và màu nhãn trạng thái do hệ '
    'thống trả về, giao diện chỉ hiển thị.')
d.h3('3.1 Trạng thái hạng mục')
d.table(['STT', 'Trạng thái', 'Màu nhãn', 'Ý nghĩa', 'Vào trạng thái này khi'], [
    ('1', 'Chưa duyệt', 'Xám #6B7280', 'Hạng mục vừa được khai, chờ Leader nhận.',
     'Thêm hạng mục khi tạo / sửa giải pháp (luôn ở trạng thái này khi mới lưu).'),
    ('2', 'Đang triển khai', 'Xanh dương #2563EB', 'Leader và nhân sự đang làm hạng mục.',
     ['- Leader bấm “Lưu và duyệt” (giải pháp Chờ Leader duyệt)',
      '- PM bấm “Lưu và duyệt hạng mục” (giải pháp Đang triển khai)',
      '- PM từ chối hồ sơ trình duyệt hạng mục', '- Tạo version hạng mục']),
    ('6', 'Chờ duyệt hồ sơ trình duyệt', 'Cam #D97706', 'Hồ sơ trình duyệt hạng mục đang chờ PM duyệt.',
     'Leader bấm “Lưu & Trình duyệt” trên cửa sổ hồ sơ.'),
    ('8', 'Đã duyệt hồ sơ trình duyệt', 'Xanh lá #16A34A', 'Kết quả hạng mục đã được PM duyệt.',
     'PM bấm “Duyệt” hồ sơ.'),
    ('10', 'Đóng', 'Xám #6B7280', 'Kết thúc, chỉ còn xem.', 'Đóng dự án TKT chứa giải pháp.'),
], widths=[0.5, 1.7, 1.3, 2.5, 3.5])
d.p('Cột STT ghi đúng mã trạng thái trong hệ thống (không liên tục: 1, 2, 6, 8, 10).')

d.h3('3.2 Ma trận chuyển trạng thái hạng mục')
d.table(['STT', 'Trạng thái hiện tại', 'Trạng thái sau', 'Thao tác (nút)', 'Người thực hiện', 'Điều kiện'], [
    ('1', '(chưa có)', 'Chưa duyệt', '“Thêm hạng mục” rồi lưu giải pháp', 'Người tạo GP (Nháp), PM (Chờ PM duyệt, '
     'Chờ Leader duyệt, Đang triển khai)', 'Giải pháp tích “Dự án có hạng mục”; đủ Tên, Leader, Ngày cần hoàn thành'),
    ('2', 'Chưa duyệt', 'Đang triển khai', '“Lưu và duyệt” (màn Duyệt giải pháp)', 'Leader hạng mục',
     'Giải pháp Chờ Leader duyệt; duyệt cùng lúc mọi hạng mục người đó làm Leader trong giải pháp'),
    ('3', 'Chưa duyệt', 'Đang triển khai', '“Lưu và duyệt hạng mục” (màn Sửa giải pháp)', 'PM',
     'Giải pháp Đang triển khai, không phải dự án Tự triển khai; áp cho mọi hạng mục Chưa duyệt của giải pháp'),
    ('4', 'Đang triển khai', 'Chờ duyệt hồ sơ trình duyệt', '“Tạo hồ sơ trình duyệt” → “Lưu & Trình duyệt”',
     'Leader hạng mục', 'Có BOM tổng hợp Hoàn thành của version hạng mục hiện tại (trừ dự án Tự triển khai)'),
    ('5', 'Chờ duyệt hồ sơ trình duyệt', 'Đã duyệt hồ sơ trình duyệt', '“Duyệt” (popup hồ sơ)',
     'PM của giải pháp (hoặc PM ghi trên hồ sơ)', 'Hồ sơ đang Chờ duyệt'),
    ('6', 'Chờ duyệt hồ sơ trình duyệt', 'Đang triển khai', '“Từ chối” (popup hồ sơ)', 'PM',
     'Bắt buộc nhập lý do (“Vui lòng nhập lý do không duyệt.”)'),
    ('7', 'Đã duyệt hồ sơ trình duyệt', 'Đang triển khai', '“Tạo version”', 'Người mở được màn Quản lý hạng mục',
     'Nhập Ngày kết thúc ≥ hôm nay; hồ sơ Đã duyệt → Hết hiệu lực; tiến độ về 0%'),
    ('8', 'Mọi trạng thái trừ Đóng', 'Đóng', 'Đóng dự án TKT', 'Người đóng dự án', 'Giải pháp cũng chuyển Đóng'),
    ('9', 'Mọi trạng thái (khi hạng mục còn sửa được trên form)', '(xoá)', 'Biểu tượng thùng rác trên khối hạng '
     'mục rồi lưu giải pháp', 'Như dòng 1', 'Hạng mục đã lưu bị khoá khi giải pháp từ Đang triển khai trở đi → '
     'không xoá được'),
], widths=[0.5, 1.6, 1.5, 2.0, 1.7, 2.7])
d.p('Không có thao tác nào khác đổi trạng thái hạng mục. Máy chủ có xử lý “giải pháp từ Đã duyệt giải pháp về '
    'Chờ PM duyệt thì mọi hạng mục về Chưa duyệt” nhưng giao diện hiện không có nút dẫn tới bước đó.')

d.h3('3.3 Trạng thái × nút hành động')
d.p('Nút không đủ điều kiện được ẩn hẳn. ✅ = có thể hiện (khi đúng vai trò ở cột cuối), ❌ = không hiện.')
Y, N = '✅', '❌'
d.table(['Nút', 'Chưa duyệt', 'Đang triển khai', 'Chờ duyệt hồ sơ', 'Đã duyệt hồ sơ', 'Đóng',
         'Vai trò / điều kiện thêm'], [
    ('Sửa, Lưu và duyệt (cột Hành động danh sách)', Y, N, N, N, N,
     'Người dùng là Leader hạng mục và giải pháp Chờ Leader duyệt'),
    ('Tạo hồ sơ trình duyệt / Sửa hồ sơ trình duyệt', N, Y, N, N, N,
     'Leader hạng mục; chưa có hồ sơ, hoặc hồ sơ mới nhất Nháp (→ Sửa) / Không duyệt / Hết hiệu lực (→ Tạo)'),
    ('Duyệt / Từ chối hồ sơ (tab Hồ sơ, popup)', N, N, Y, N, N, 'PM của giải pháp; hồ sơ Chờ duyệt'),
    ('Sửa hồ sơ Nháp (tab Hồ sơ)', N, Y, N, N, N, 'Người tạo hồ sơ'),
    ('Xem hồ sơ (tab Hồ sơ)', Y, Y, Y, Y, Y, 'Mọi người mở được màn'),
    ('Tạo version', N, N, N, Y, N, 'Mọi người mở được màn (không kiểm vai trò)'),
    ('Tạo mới nhiệm vụ / vấn đề', N, Y, Y, N, N, 'Mọi người mở được màn'),
    ('Tạo mới meeting', Y, Y, Y, Y, N, 'Hạng mục thuộc dự án TKT'),
    ('Thêm nhân sự', Y, Y, Y, Y, N, 'Mọi người mở được màn'),
    ('Sửa / Xoá nhiệm vụ, vấn đề, meeting', Y, Y, Y, Y, N, 'Theo quyền trên từng nhiệm vụ / vấn đề / meeting'),
    ('Nhập % phân bổ (tab Tiến độ)', Y, Y, Y, Y, Y, 'Leader hạng mục'),
], widths=[2.4, 0.85, 0.95, 0.95, 0.95, 0.65, 2.75])

d.h3('3.4 Các danh mục giá trị cố định')
d.table(['Danh mục', 'Giá trị (chữ trên giao diện)', 'Dùng ở'], [
    ('Trạng thái hồ sơ trình duyệt hạng mục', 'Nháp (xám #64748B) · Chờ duyệt (cam #D97706) · Đã duyệt (xanh lá '
     '#16A34A) · Không duyệt (đỏ #DC2626) · Hết hiệu lực (xám #6B7280)', 'Tab Hồ sơ, popup hồ sơ'),
    ('Nguồn file', 'Nhiệm vụ · Vấn đề · HSTD (hồ sơ trình duyệt)', 'Tab Files'),
    ('Nguồn vốn', 'Vốn tự có · Vốn vay ngân hàng · Ngân sách nhà nước · Kết hợp nhiều nguồn · Khác', 'Tab Thông tin'),
    ('Trạng thái nhiệm vụ (ô lọc)', 'Đang tạo · Chờ duyệt · Đang làm · Hoàn thành · Tồn đọng', 'Tab Nhiệm vụ, popup '
     'Nhiệm vụ sắp hết hạn'),
    ('Trạng thái nhiệm vụ (ô lọc popup cần duyệt)', 'Chờ duyệt triển khai · Chờ duyệt kết quả',
     'Popup Nhiệm vụ cần duyệt'),
    ('Trạng thái nhiệm vụ (ô lọc tab Tiến độ)', 'Chờ bắt đầu · Đang thực hiện · Tạm dừng · Hoàn thành - Chờ duyệt '
     '· Hoàn thành', 'Tab Tiến độ'),
    ('Trạng thái vấn đề (ô lọc)', 'Mới ghi nhận · Đã phân công · Đang xử lý · Đã xử lý xong · Đã đóng · Mở lại',
     'Tab Vấn đề hạng mục'),
    ('Mức độ ưu tiên vấn đề', 'Thấp · Trung bình · Cao · Khẩn cấp', 'Tab Vấn đề hạng mục'),
    ('Trạng thái meeting (ô lọc)', 'Lưu nháp · Lên lịch hẹn · Đã chốt lịch · Đã hoàn thành · Huỷ', 'Tab Meetings'),
    ('Hình thức meeting', 'Trực tiếp · Online', 'Tab Meetings'),
    ('Có biên bản?', 'Đã lập biên bản · Chưa lập biên bản', 'Tab Meetings'),
    ('Mã hạng mục', '<Mã giải pháp>_HM<số thứ tự 2 chữ số theo vị trí khối trên form> (vd …_GP01_HM02)',
     'Form giải pháp, danh sách'),
], widths=[2.4, 5.0, 2.1])

d.h2('4 Quy trình nghiệp vụ')
d.p('Sơ đồ dạng làn theo vai trò, ô ghi bước và trạng thái hạng mục sau bước đó (trong ngoặc vuông).')
d.figure(shot('flow_hm.png'), 'Quy trình làm hạng mục giải pháp', width_in=6.2)
d.table(['Bước', 'Tác nhân', 'Hành động', 'Trạng thái hạng mục sau', 'Thông báo'], [
    ('1', 'Người tạo GP / PM', 'Khai hạng mục ở tab Quản lý hạng mục khi tạo / sửa giải pháp (mục 2.6).',
     'Chưa duyệt', '–'),
    ('2', 'PM', 'Bấm “Giao cho Leader” ở màn Duyệt giải pháp (SRS Quản lý giải pháp); giải pháp → Chờ Leader '
     'duyệt.', 'Chưa duyệt', 'TB-01'),
    ("2'", 'PM', 'Giải pháp đã Đang triển khai: thêm hạng mục mới rồi bấm “Lưu và duyệt hạng mục” (mục 2.8).',
     'Đang triển khai', '–'),
    ('3', 'Leader hạng mục', 'Rà ngày, ghi chú, nhân sự hạng mục mình rồi bấm “Lưu và duyệt” (mục 2.7). Hạng mục '
     'cuối cùng được duyệt → giải pháp tự sang Đang triển khai.', 'Đang triển khai', '–'),
    ('4', 'Leader, nhân sự', 'Làm hạng mục ở màn Quản lý hạng mục: nhiệm vụ, vấn đề, meeting, phân bổ tiến độ, '
     'lập BOM tổng hợp hạng mục (SRS BOM giải pháp).', 'Đang triển khai', '–'),
    ('5', 'Leader hạng mục', 'Tạo hồ sơ trình duyệt → Lưu (Nháp) hoặc Lưu & Trình duyệt (mục 2.13).',
     'Chờ duyệt hồ sơ trình duyệt', '–'),
    ('6', 'PM', 'Duyệt hoặc Từ chối (nhập lý do) hồ sơ (mục 2.15).', 'Đã duyệt hồ sơ / Đang triển khai', '–'),
    ('7', 'Người mở được màn', 'Tạo version khi cần làm lại (mục 2.23).', 'Đang triển khai', '–'),
    ('8', 'Người đóng dự án', 'Đóng dự án TKT (SRS Quản lý dự án TKT).', 'Đóng', '–'),
], widths=[0.75, 1.4, 4.35, 1.7, 1.3])

d.h2('5 Bảng thông báo nghiệp vụ')
d.p('Thông báo không gửi cho chính người thao tác. Bấm thông báo → mở màn ở cột Ghi chú (Deep-link).')
d.table(['Mã', 'Hành động phát sinh', 'Event kích hoạt', 'Người gửi', 'Người nhận', 'Nội dung mẫu (Tiêu đề / Nội dung)',
         'Thời điểm gửi', 'Ghi chú (Deep-link)'], [
    ('TB-01', 'Giao hạng mục cho Leader', '“Giao cho Leader”: giải pháp chuyển sang Chờ Leader duyệt', 'PM',
     'Các Leader của hạng mục trong giải pháp (mỗi người 1 lần)',
     'Thông báo giải pháp chờ duyệt hạng mục / Bạn có giải pháp cần duyệt hạng mục: {Mã GP} - {Tên GP}',
     'Ngay sau khi lưu', 'Màn Chi tiết giải pháp (không mở thẳng màn Duyệt của Leader)'),
    ('TB-02', 'Phân công Leader hạng mục', 'Lưu phân công Leader ở màn Quản lý giải pháp', 'Người phân công',
     'Leader mới', 'Phân công Leader giải pháp / Bạn được phân công làm Leader giải pháp "{Mã GP} - {Tên GP}".',
     'Ngay sau khi lưu', 'Màn Quản lý giải pháp'),
    ('TB-03', 'Thay thế Leader hạng mục', 'Lưu phân công Leader ở màn Quản lý giải pháp', 'Người phân công',
     'Leader cũ', 'Thay đổi Leader giải pháp / Bạn đã được thay thế vị trí Leader giải pháp "{Mã GP} - {Tên GP}". '
     'Leader mới: {Tên}. Vai trò mới của bạn: {Vai trò}.', 'Ngay sau khi lưu', 'Màn Quản lý giải pháp'),
], widths=[0.5, 1.1, 1.3, 0.8, 1.2, 2.4, 0.8, 1.4])
d.p('Hệ thống KHÔNG gửi thông báo khi: thêm / sửa / xoá hạng mục trên form giải pháp; Leader “Lưu và duyệt” '
    'hạng mục; PM “Lưu và duyệt hạng mục”; Leader lưu nháp hoặc trình hồ sơ hạng mục; PM duyệt hoặc từ chối hồ sơ '
    'hạng mục; tạo version hạng mục; thêm nhân sự vào hạng mục; đổi % phân bổ tiến độ; hạng mục chuyển Đóng. '
    'Không có thông báo nhắc hạn hạng mục / hạn duyệt hồ sơ.')

# ======================================================================= PHẦN 2
d.h1('Phần 2. Phân quyền')
d.h2('1 Danh sách quyền')
d.p('Nhóm quyền thao tác:')
d.table(['Ký hiệu', 'Tên quyền', 'Tác dụng trên màn hình'], [
    ('–', '(không có)', 'Màn Hạng mục giải pháp không gắn quyền thao tác nào: mọi chức năng của máy chủ đều '
     'không kiểm quyền. Thao tác do VAI TRÒ của người dùng trên giải pháp / hạng mục quyết định (bảng dưới).'),
], widths=[0.8, 2.2, 6.5])
d.table(['Ký hiệu', 'Vai trò', 'Tác dụng trên màn hình'], [
    ('R1', 'PM làm giải pháp', 'Thêm / sửa hạng mục trên form giải pháp (Chờ PM duyệt, Chờ Leader duyệt, Đang '
     'triển khai); “Lưu và duyệt hạng mục”; duyệt / từ chối hồ sơ trình duyệt hạng mục.'),
    ('R2', 'Leader hạng mục', '“Lưu và duyệt” hạng mục mình; tạo / sửa / trình hồ sơ trình duyệt; nhập % phân bổ '
     'tiến độ nhiệm vụ của hạng mục.'),
    ('R3', 'Người tạo giải pháp', 'Khai hạng mục khi giải pháp còn Nháp.'),
    ('R4', 'Người xem hạng mục', 'Người thấy hạng mục trong danh sách (người tạo, Leader, thành viên, PM): mở màn '
     'Quản lý hạng mục, xem các tab, thêm nhân sự, tạo nhiệm vụ / vấn đề / meeting, tạo version.'),
], widths=[0.8, 2.2, 6.5])
d.p('Nhóm quyền quyết định phạm vi dữ liệu:')
d.table(['Ký hiệu', 'Tên quyền', 'Phạm vi dữ liệu'], [
    ('V1', 'Xem danh sách hạng mục dự án theo tổng công ty', 'Toàn bộ hạng mục.'),
    ('V2', 'Xem danh sách hạng mục dự án theo công ty', 'Hạng mục thuộc công ty đang làm việc + hạng mục mình tạo / '
     'liên quan.'),
    ('V3', 'Xem danh sách hạng mục dự án theo phòng ban', 'Hạng mục thuộc phòng ban / bộ phận mình quản lý + mình tạo '
     '/ liên quan.'),
    ('V4', 'Xem danh sách hạng mục dự án theo bộ phận', 'Hạng mục thuộc bộ phận mình quản lý + mình tạo / liên quan.'),
    ('–', 'Không có quyền nào', 'Hạng mục do mình tạo, mình là Leader, là thành viên, hoặc là PM của yêu cầu làm '
     'giải pháp tương ứng.'),
], widths=[0.8, 3.4, 5.3])
d.p('Lưu ý: 4 quyền V1–V4 được máy chủ dùng nhưng CHƯA có trong danh mục quyền của hệ thống, nên hiện không vai '
    'trò nào được gán → mọi người dùng đều rơi vào dòng “Không có quyền nào”, và bộ lọc Công ty – Phòng ban – Bộ '
    'phận không hiện. Mọi phạm vi chỉ tính hạng mục của giải pháp đã từ Chờ Leader duyệt trở đi hoặc Đóng.')

d.h2('2 Ma trận phân quyền')
d.table(['Chức năng', 'R1', 'R2', 'R3', 'R4', 'Không có quyền nào'], [
    ('FR-01 Xem danh sách hạng mục', Y, Y, Y, Y, '✅ (theo phạm vi)'),
    ('FR-02 Tìm kiếm và lọc', Y, Y, Y, Y, Y),
    ('FR-03 Cài đặt bộ lọc', Y, Y, Y, Y, Y),
    ('FR-04 Tùy chỉnh cột', Y, Y, Y, Y, Y),
    ('FR-05 Xuất Excel', Y, Y, Y, Y, Y),
    ('FR-06 Khai hạng mục trên form giải pháp', Y, N, '✅ (Nháp)', N, N),
    ('FR-07 Leader duyệt hạng mục', N, Y, N, N, N),
    ('FR-08 PM lưu và duyệt hạng mục', Y, N, N, N, N),
    ('FR-09 Mở màn Quản lý hạng mục', Y, Y, Y, Y, '✅ (hạng mục trong phạm vi)'),
    ('FR-10 Popup cảnh báo nhiệm vụ', Y, Y, Y, Y, Y),
    ('FR-11 Tab Thông tin', Y, Y, Y, Y, Y),
    ('FR-12 Tab Hồ sơ', Y, Y, Y, Y, Y),
    ('FR-13 Tạo / trình hồ sơ trình duyệt', N, Y, N, N, N),
    ('FR-14 Xem hồ sơ trình duyệt', Y, Y, Y, Y, Y),
    ('FR-15 PM duyệt / từ chối hồ sơ', Y, N, N, N, N),
    ('FR-16 Tab Nhân sự', Y, Y, Y, Y, Y),
    ('FR-17 Thêm nhân sự', Y, Y, Y, Y, Y),
    ('FR-18 Tab Nhiệm vụ', Y, Y, Y, Y, Y),
    ('FR-19 Tab Vấn đề hạng mục', Y, Y, Y, Y, Y),
    ('FR-20 Tab Meetings', Y, Y, Y, Y, Y),
    ('FR-21 Tab Tiến độ – nhập % phân bổ', '✅ (chỉ xem)', Y, '✅ (chỉ xem)', '✅ (chỉ xem)', '✅ (chỉ xem)'),
    ('FR-22 Tab Files', Y, Y, Y, Y, Y),
    ('FR-23 Tạo version hạng mục', Y, Y, Y, Y, Y),
], widths=[3.4, 1.0, 1.0, 1.0, 1.0, 2.1])
d.p('R1–R4 là vai trò trên từng giải pháp / hạng mục, không phải quyền gán cho vai trò hệ thống. Cột “Không có quyền '
    'nào” áp với người mở được hạng mục (hạng mục nằm trong phạm vi ở mục 1). Nút không dùng được thì ẩn hẳn.')

# ======================================================================= PHẦN 3
d.h1('Phần 3. Đặc tả chi tiết theo từng chức năng')
d.h2('1 Sơ đồ UML tổng quan')
d.overview_figure2(
    [(A_ALL, [0, 1, 5]), (A_PM, [2, 4, 7]), (A_LD, [3, 6, 9]), (A_TV, [8, 10])],
    [('FR-01', 'Xem danh sách hạng mục', 'view'),
     ('FR-05', 'Xuất Excel', 'io'),
     ('FR-06', 'Khai hạng mục trên form GP', 'crud'),
     ('FR-07', 'Leader duyệt hạng mục', 'action'),
     ('FR-08', 'PM lưu và duyệt hạng mục', 'action'),
     ('FR-09', 'Mở màn Quản lý hạng mục', 'view'),
     ('FR-13', 'Tạo / trình hồ sơ', 'crud'),
     ('FR-15', 'Duyệt / từ chối hồ sơ', 'action'),
     ('FR-17', 'Thêm nhân sự', 'crud'),
     ('FR-21', 'Phân bổ % tiến độ', 'crud'),
     ('FR-23', 'Tạo version hạng mục', 'action')],
    [('FR-02', 'Tìm kiếm và lọc', 'view', 'extend', [0], None),
     ('FR-03', 'Cài đặt bộ lọc', 'view', 'extend', [0], None),
     ('FR-04', 'Tùy chỉnh cột', 'view', 'extend', [0], None),
     ('FR-10', 'Popup cảnh báo nhiệm vụ', 'view', 'extend', [5], None),
     ('FR-11', 'Tab Thông tin', 'view', 'extend', [5], None),
     ('FR-12', 'Tab Hồ sơ', 'view', 'extend', [5], None),
     ('FR-14', 'Xem hồ sơ trình duyệt', 'view', 'extend', [5], None),
     ('FR-16', 'Tab Nhân sự', 'view', 'extend', [5], None),
     ('FR-18', 'Tab Nhiệm vụ', 'view', 'extend', [5], None),
     ('FR-19', 'Tab Vấn đề hạng mục', 'view', 'extend', [5], None),
     ('FR-20', 'Tab Meetings', 'view', 'extend', [5], None),
     ('FR-22', 'Tab Files', 'view', 'extend', [5], None)],
    'Sơ đồ Use Case tổng quan màn %s' % TEN_MAN)

d.h2('2 Đặc tả chi tiết từng chức năng')

# ---------------------------------------------------------------- 2.1 FR-01
fn('Xem danh sách hạng mục giải pháp',
   dict(ten='Xem danh sách hạng mục giải pháp',
        mota='Hiển thị bảng các hạng mục người dùng được xem, mới tạo trước, kèm nút thao tác theo vai trò.',
        tacnhan=A_ALL, dieukien='Người dùng đã đăng nhập hệ thống.',
        chinh='1. Người dùng mở màn theo đường dẫn menu.\n'
              '2. Hệ thống nạp hạng mục trong phạm vi được xem (Phần 2), chỉ lấy hạng mục của giải pháp đã từ Chờ '
              'Leader duyệt trở đi hoặc Đóng; sắp xếp Ngày tạo giảm dần; 10 dòng/trang.\n'
              '3. Hệ thống hiển thị bảng “Danh sách hạng mục dự án” với 13 cột (mặc định hiện hết).\n'
              '4. Người dùng bấm Mã hạng mục để mở màn Quản lý hạng mục (mục 2.9).',
        phu='• Không có dữ liệu → “Không có dữ liệu phù hợp bộ lọc.”.\n'
            '• Lỗi khi nạp → thông báo “Lỗi khi tải dữ liệu”.\n'
            '• Quay lại màn trong vòng 10 phút → khôi phục bộ lọc và trạng thái đóng/mở khối Tìm kiếm nâng cao.\n'
            '• Hạng mục của giải pháp Nháp / Chờ PM duyệt không hiển thị.'),
   [('menu', MENU), ('img', '01-danh-sach.png', 'Danh sách hạng mục dự án lúc mới mở'),
    ('img', '01b-danh-sach-phai.png', 'Các cột bên phải và cột Hành động (cuộn ngang bảng)')],
   [('Tiêu đề trang / tiêu đề bảng', 'Label', 'Hiển thị', '–', 'Danh sách hạng mục dự án',
     ['- Chữ trên trang: “Danh sách hạng mục dự án” (menu ghi “Hạng mục giải pháp”)']),
    ('Nút Xuất Excel', 'Button', 'Enable / Disable', '–', 'Hiển thị', '- Mở cửa sổ chọn trường xuất (mục 2.5); '
     'khoá trong lúc đang xuất'),
    ('Nút Cấu hình cột hiển thị', 'Icon Button', 'Enable', '–', 'Hiển thị', '- Mở cửa sổ Tuỳ chỉnh cột (mục 2.4)'),
    ('Cột STT', 'Text', 'Read-only', '≥ 1', 'Theo dữ liệu', '- Số thứ tự liên tục giữa các trang; cột ghim trái'),
    ('Cột Mã hạng mục', 'Link', 'Read-only', '–', 'Theo dữ liệu',
     ['- Dạng <Mã GP>_HMnn, ghim trái, sắp xếp được', '- Bấm → mở màn Quản lý hạng mục (mục 2.9); chuột phải mở '
      'tab mới được']),
    ('Cột Tên hạng mục', 'Text', 'Read-only', '–', 'Theo dữ liệu', ['- Tên lấy từ danh mục Hạng mục dự án (đổi tên '
     'danh mục thì hiện tên mới); tối đa 2 dòng', '- Sắp xếp được']),
    ('Cột Dự án (giải pháp)', 'Text', 'Read-only', '–', 'Theo dữ liệu', '- “<Mã GP> - <Tên GP>”, tối đa 2 dòng'),
    ('Cột Leader', 'Text', 'Read-only', '–', 'Theo dữ liệu', '- Họ tên Leader hạng mục'),
    ('Cột Hạn hoàn thành', 'Text', 'Read-only', 'dd/mm/yyyy', 'Theo dữ liệu', '- Ngày cần hoàn thành; sắp xếp được'),
    ('Cột Phiên bản', 'Badge', 'Read-only', '–', 'Theo dữ liệu', ['- “GP: Vn”: version giải pháp gắn với version '
     'hạng mục hiện tại', '- “HM: Vn”: version hạng mục hiện tại']),
    ('Cột Người tạo / Người cập nhật', 'Text', 'Read-only', '–', 'Theo dữ liệu', '- “Tên nhân viên - Mã phòng”'),
    ('Cột Ngày tạo / Ngày cập nhật', 'Text', 'Read-only', 'dd/mm/yyyy hh:mm', 'Theo dữ liệu', '- Sắp xếp được'),
    ('Cột Trạng thái', 'Badge', 'Read-only', 'Danh sách 5 giá trị', 'Theo dữ liệu', '- Chữ và màu theo bảng 3.1'),
    ('Cột Hành động', 'Icon Button', 'Enable / Ẩn', '–', 'Ẩn',
     ['- Ghim, luôn hiện trong cấu hình cột', '- Sửa (bút chì) và Lưu và duyệt (dấu tích): chỉ hiện khi người dùng '
      'là Leader, hạng mục Chưa duyệt và giải pháp Chờ Leader duyệt (mục 2.7)', '- Không có nút Xem / Xoá']),
    ('Phân trang', 'Pagination', 'Enable', '10/20/50…', '10', '- “Hiển thị a–b / tổng”, chọn số dòng/trang'),
    ('Thông báo bảng rỗng', 'Text', 'Hiển thị', '–', 'Ẩn', '- “Không có dữ liệu phù hợp bộ lọc.”')],
   [('Mở màn', 'System', 'After:\n– Khôi phục bộ lọc đã lưu (nếu còn hạn 10 phút) rồi nạp danh sách ngay.\n'
                          '– Danh mục cho ô lọc chỉ nạp khi mở Tìm kiếm nâng cao.'),
    ('Bấm tiêu đề cột sắp xếp', 'Click', 'After:\n– Cột sắp xếp được: Mã hạng mục, Tên hạng mục, Hạn hoàn thành, '
     'Ngày tạo, Ngày cập nhật.\n– Lần bấm đổi tăng ↔ giảm; về trang 1; dòng cùng giá trị xếp theo mới tạo trước.'),
    ('Bấm Mã hạng mục', 'Click', 'After:\n– Mở màn Quản lý hạng mục của dòng đó (toàn màn hình, ẩn menu trái).'),
    ('Bấm Sửa / Lưu và duyệt ở dòng', 'Click', 'Before:\n' + NO_ROLE + '\nAfter:\n– Mở màn Sửa giải pháp '
     '(Sửa) hoặc màn Duyệt giải pháp (Lưu và duyệt) của giải pháp chứa hạng mục; xử lý ở mục 2.7.')] + ev_page(),
   rule=('- Màn Danh sách, Sắp xếp dữ liệu bảng, Phân trang và Cấu hình cột.', 'list'), ui_kind='read')

# ---------------------------------------------------------------- 2.2 FR-02
fn('Tìm kiếm và lọc',
   dict(ten='Tìm kiếm và lọc hạng mục',
        mota='Thu hẹp danh sách theo từ khoá và các điều kiện lọc.',
        tacnhan=A_ALL, dieukien='Đang ở màn danh sách hạng mục.',
        chinh='1. Người dùng gõ từ khoá vào ô tìm nhanh rồi bấm “Tìm kiếm” hoặc Enter.\n'
              '2. Hoặc bấm “Tìm kiếm nâng cao” để mở các ô lọc, chọn giá trị — bảng tự lọc ngay khi chọn.\n'
              '3. Hệ thống nạp lại danh sách từ trang 1.',
        phu='• Bấm “Làm mới” → xoá mọi điều kiện, nạp lại 1 lần.\n'
            '• Bấm “Ẩn tìm kiếm nâng cao” → thu gọn khối lọc, giữ điều kiện đã chọn.'),
   [('menu', MENU + ' => Tìm kiếm nâng cao'), ('img', '02-loc.png', 'Khối Tìm kiếm nâng cao đang mở')],
   [('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống', ['- Placeholder “Tìm theo mã hạng mục, tên hạng mục”',
     '- Tìm gần đúng theo mã hạng mục hoặc tên hạng mục (tên sống từ danh mục)', '- Chỉ lọc khi bấm Tìm kiếm / Enter']),
    ('Nút Tìm kiếm / Làm mới', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Tìm kiếm: áp từ khoá; Làm mới: xoá hết điều '
     'kiện'),
    ('Nút Tìm kiếm nâng cao / Ẩn tìm kiếm nâng cao', 'Button', 'Enable', '–', '–', 'Thu gọn', '- Mở / thu khối ô lọc'),
    ('Ô Công ty – Phòng ban – Bộ phận', 'Dropdown', 'Enable / Ẩn', 'Danh sách', 'Không', 'Ẩn',
     ['- 3 ô liên cấp, chỉ hiện theo quyền phạm vi V1–V4 của người dùng', '- Hiện tại không ai có các quyền này nên '
      '3 ô không hiện']),
    ('Ô Dự án (giải pháp)', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Nguồn: danh sách giải pháp người dùng được xem (theo phạm vi màn Quản lý giải pháp), tối đa 1.000 dòng, nạp '
      '1 lần khi mở Tìm kiếm nâng cao', '- Hiển thị “<Mã GP> - <Tên GP>”, gồm cả giải pháp Đóng',
      '- Nhãn floating “Dự án (giải pháp)”, placeholder “Chọn dự án”']),
    ('Ô Leader', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Nguồn: danh sách nhân viên đang làm việc (dữ liệu chung nạp khi đăng nhập)', '- Hiển thị “Tên nhân viên - '
      'Mã phòng - Mã nhân viên”', '- Nhân viên đã nghỉ việc KHÔNG có trong danh sách (không lọc được hạng mục có '
      'Leader đã nghỉ)']),
    ('Ô Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống', '- Giá trị cố định theo bảng 3.1'),
    ('Ô Ngày tạo', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', '- Khoảng ngày Từ → Đến trong 1 ô, lọc theo '
     'ngày tạo hạng mục (gồm cả 2 đầu)')],
   [('Gõ từ khoá + Enter / bấm Tìm kiếm', 'Keypress / Click', 'After:\n– Về trang 1, nạp lại danh sách theo từ khoá.'),
    ('Chọn giá trị ở ô lọc', 'Change', 'After:\n– Tự nạp lại danh sách từ trang 1 (không cần bấm Tìm kiếm).'),
    ('Bấm Làm mới', 'Click', 'After:\n– Xoá mọi điều kiện lọc và sắp xếp về mặc định, nạp lại 1 lần.'),
    ('Bấm Tìm kiếm nâng cao (lần đầu)', 'Click', 'After:\n– Mở khối ô lọc; nạp danh sách giải pháp cho ô Dự án.')],
   rule=('- Kịch bản tìm kiếm, Bộ lọc, Dropdown.', 'search'))

# ---------------------------------------------------------------- 2.3 FR-03
fn('Cài đặt bộ lọc',
   dict(ten='Cài đặt bộ lọc', mota='Người dùng chọn ô lọc nào hiện và thứ tự các ô trên khối Tìm kiếm nâng cao.',
        tacnhan=A_ALL, dieukien='Đang ở màn danh sách hạng mục.',
        chinh='1. Bấm “Cài đặt bộ lọc”.\n2. Tích / bỏ tích ô lọc, kéo biểu tượng ⠿ để đổi thứ tự.\n3. Bấm “Lưu”.\n'
              '4. Hệ thống lưu cấu hình theo người dùng cho màn này và vẽ lại khối lọc.',
        phu='• “Khôi phục mặc định” → về đủ 5 ô theo thứ tự gốc.\n• Bỏ tích ô đang có giá trị lọc → giá trị đó bị xoá.'),
   [('menu', MENU + ' => Cài đặt bộ lọc'), ('modal', 'Cài đặt bộ lọc'), ('img', '03-cai-dat-loc.png', 'Cửa sổ Cài đặt bộ lọc')],
   [('Danh sách ô lọc', 'Checkbox', 'Enable', '5 ô', 'Không', 'Tích hết', '- Công ty – Phòng ban – Bộ phận, Dự án (giải '
     'pháp), Leader, Trạng thái, Ngày tạo; mỗi ô có số thứ tự và tay kéo'),
    ('Nút Lưu', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu cấu hình theo người dùng + màn'),
    ('Nút Khôi phục mặc định', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Trả về cấu hình gốc'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không lưu')],
   [('Kéo thả ô lọc', 'Drag', 'After:\n– Đổi thứ tự hiển thị trong cửa sổ (chưa lưu).'),
    ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình, đóng cửa sổ, vẽ lại khối lọc theo cấu hình.'),
    ('Bấm Khôi phục mặc định', 'Click', 'After:\n– Đưa danh sách về 5 ô mặc định.'), ev_close()])

# ---------------------------------------------------------------- 2.4 FR-04
fn('Tùy chỉnh cột',
   dict(ten='Tùy chỉnh cột hiển thị', mota='Chọn cột hiện trên bảng và thứ tự cột.',
        tacnhan=A_ALL, dieukien='Đang ở màn danh sách hạng mục.',
        chinh='1. Bấm biểu tượng Cấu hình cột hiển thị.\n2. Tích / bỏ tích cột, kéo ☰ đổi thứ tự.\n3. Bấm “Lưu”.',
        phu='• Cột STT, Mã hạng mục, Hành động bị khoá (xám): luôn hiện, không bỏ tích được.\n'
            '• “Chọn tất cả” / “Bỏ chọn hết” áp cho các cột không khoá.'),
   [('menu', MENU + ' => Cấu hình cột hiển thị'), ('modal', 'Tuỳ chỉnh cột'), ('img', '04-tuy-chinh-cot.png', 'Cửa sổ Tuỳ chỉnh cột')],
   [('Danh sách cột', 'Checkbox', 'Enable / Disable', '13 cột', 'Không', 'Tích hết', ['- STT, Mã hạng mục, Tên hạng mục, '
     'Dự án (giải pháp), Leader, Hạn hoàn thành, Phiên bản, Người tạo, Ngày tạo, Người cập nhật, Ngày cập nhật, Trạng '
     'thái, Hành động', '- Khoá: STT, Mã hạng mục, Hành động']),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Áp cho cột không khoá'),
    ('Dòng “Đang chọn n/13 cột”', 'Text', 'Hiển thị', '–', '–', 'Theo dữ liệu', '- Số cột đang tích'),
    ('Nút Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Lưu cấu hình theo người dùng ở máy chủ / Đóng không lưu')],
   [('Tích / bỏ tích, kéo thả cột', 'Change / Drag', 'After:\n– Cập nhật danh sách trong cửa sổ (chưa lưu).'),
    ('Bấm Lưu', 'Click', 'After:\n– Lưu cấu hình cột của người dùng cho màn này; bảng vẽ lại theo cấu hình.'), ev_close()],
   rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'))

# ---------------------------------------------------------------- 2.5 FR-05
fn('Xuất Excel',
   dict(ten='Xuất Excel danh sách hạng mục', mota='Tải file Excel các hạng mục theo bộ lọc đang áp, chọn trường xuất.',
        tacnhan=A_ALL, dieukien='Đang ở màn danh sách hạng mục.',
        chinh='1. Bấm “Xuất Excel”.\n2. Cửa sổ “Chọn trường xuất file” mở, tích sẵn các trường tương ứng cột đang hiện.\n'
              '3. Tích / bỏ / kéo đổi thứ tự trường, bấm “Xuất file”.\n4. Trình duyệt tải file '
              'danh_sach_hang_muc_du_an.xlsx, thông báo “Xuất Excel thành công”.',
        phu='• Lỗi → “Lỗi khi xuất Excel”.\n• File lấy TẤT CẢ dòng khớp bộ lọc (không theo trang), cùng phạm vi dữ liệu.'),
   [('menu', MENU + ' => Xuất Excel'), ('modal', 'Chọn trường xuất file'), ('img', '05-xuat.png', 'Cửa sổ Chọn trường xuất file')],
   [('Danh sách trường', 'Checkbox', 'Enable', '13 trường', 'Có (≥ 1)', 'Theo cột đang hiện', ['- Mã hạng mục, Tên hạng '
     'mục, Tên dự án (giải pháp), Leader, Hạn hoàn thành, Phiên bản hạng mục, Người tạo, Ngày tạo, Người cập nhật, Ngày '
     'cập nhật, Trạng thái, Mã dự án (giải pháp), Phiên bản giải pháp', '- Thứ tự trường = thứ tự cột trong file']),
    ('Nút Chọn tất cả / Bỏ chọn hết', 'Button', 'Enable', '–', '–', 'Hiển thị', '–'),
    ('Nút Xuất file', 'Button', 'Enable / Disable', '–', '–', 'Hiển thị', '- Khoá trong lúc đang xuất'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không xuất')],
   [('Bấm Xuất file', 'Click', 'Before:\n– Phải chọn ít nhất 1 trường.\nDuring:\n– Khoá nút Xuất Excel trên màn.\n'
     'After:\n– Tải file tiêu đề “Danh sách hạng mục dự án”, các cột theo trường đã chọn.\n– Thông báo “Xuất Excel '
     'thành công”; lỗi → “Lỗi khi xuất Excel”.'), ev_close()],
   uc=('FR-05', 'Xuất Excel', 'io', A_ALL), rule=('- Quy tắc Excel và Cấu hình cột.', 'excel'))

# ---------------------------------------------------------------- 2.6 FR-06
fn('Khai hạng mục trên form giải pháp',
   dict(ten='Khai hạng mục trên form giải pháp (tab Quản lý hạng mục)',
        mota='Người tạo giải pháp (khi Nháp) hoặc PM thêm, sửa, xoá hạng mục và phân công nhân sự từng hạng mục ngay '
             'trên form Tạo / Sửa giải pháp. Phần còn lại của form đặc tả ở SRS Quản lý giải pháp.',
        tacnhan='%s; Người tạo giải pháp' % A_PM,
        dieukien='Giải pháp tích “Dự án có hạng mục” (không có với dự án Tự triển khai); người dùng sửa được giải pháp.',
        chinh='1. Mở form Tạo / Sửa giải pháp, chọn tab “Quản lý hạng mục”.\n2. Bấm “Thêm hạng mục” → thêm 1 khối mở sẵn.\n'
              '3. Chọn Tên hạng mục (hoặc “Tạo nhanh”), Leader, Ngày cần hoàn thành, nhập Ghi chú.\n'
              '4. Bấm “Thêm nhân sự” để thêm dòng phân công: Phòng ban, Nhân sự, Vai trò dự án, Mô tả công việc, '
              'Ngày bắt đầu.\n5. Bấm nút lưu của form (Lưu nháp / Lưu và gửi / Lưu / Lưu hạng mục… theo trạng thái giải pháp).\n'
              '6. Hệ thống lưu hạng mục mới ở trạng thái Chưa duyệt, sinh version V1 cho hạng mục.',
        phu='• Bấm biểu tượng thùng rác trên khối → bỏ hạng mục khỏi form (không hỏi xác nhận); lưu giải pháp → '
            'hạng mục bị xoá hẳn.\n'
            '• Giải pháp Chờ Leader duyệt: PM thêm hạng mục mới bằng nút “Lưu hạng mục”; hạng mục cũ chỉ Leader của '
            'nó sửa.\n'
            '• Giải pháp từ Đang triển khai trở đi: hạng mục đã lưu bị khoá, chỉ sửa hạng mục vừa thêm.\n'
            '• Bỏ tích “Dự án có hạng mục” → xoá toàn bộ hạng mục khi lưu.',
        dacbiet='Mã hạng mục sinh trên form theo VỊ TRÍ khối (HM01, HM02…); xoá khối ở giữa thì các mã sau đổi số.'),
   [('menu', MGP + ' => Thêm hạng mục'),
    ('img', '25-gp-tab-hang-muc.png', 'Tab Quản lý hạng mục trên màn Sửa giải pháp (giải pháp Đang triển khai)'),
    ('img', '26-gp-them-hang-muc.png', 'Khối hạng mục mới sau khi bấm Thêm hạng mục')],
   [('Nút Thêm hạng mục', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', ['- Hiện khi giải pháp Nháp / Chờ PM duyệt / '
     'Chờ Leader duyệt / Đang triển khai', '- Ẩn với Leader (không phải PM) ở bước Chờ Leader duyệt']),
    ('Khối hạng mục (tiêu đề)', 'Label', 'Hiển thị', '–', '–', 'Mở sẵn', ['- “<Mã hạng mục> - <Tên>”, chưa chọn tên '
     'thì “Hạng mục n (chưa chọn)”', '- Dòng phụ: Nhân sự: n · Leader · Cần xong · “Có ghi chú”']),
    ('Nút Thu gọn / Mở chi tiết', 'Button', 'Enable / Disable', '–', '–', 'Mở', '- Ẩn / hiện thân khối'),
    ('Nút Xoá hạng mục (thùng rác)', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Chỉ hiện khi khối còn sửa '
     'được và người dùng quản lý hạng mục; bỏ khối ngay, không hỏi xác nhận'),
    ('Mã hạng mục', 'Textbox', 'Read-only', '–', 'Có', 'Sinh tự động', '- <Mã GP>_HMnn theo thứ tự khối'),
    ('Tên hạng mục', 'Dropdown', 'Enable / Disable', 'Danh mục Hạng mục dự án', 'Có', 'Trống',
     ['- Danh mục đang hoạt động; tên đã khoá mà hạng mục đang dùng vẫn hiện kèm 🔒', '- Khoá khi Leader sửa hạng mục '
      'cũ của mình ở bước Chờ Leader duyệt']),
    ('Nút Tạo nhanh', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Mở cửa sổ “Thêm hạng mục dự án”: Hạng mục dự án*, '
     'Mô tả; Lưu → “Lưu thành công”, thêm vào danh mục'),
    ('Leader hạng mục', 'Dropdown', 'Enable / Disable', 'Danh sách nhân viên', 'Có', 'Trống', '- “Tên - Mã phòng - Mã '
     'nhân viên”; khoá như ô Tên hạng mục'),
    ('Ngày cần hoàn thành', 'Datepicker', 'Enable / Disable', 'dd/mm/yyyy', 'Có', 'Trống', '- Không được trước hôm nay'),
    ('Ghi chú', 'Textarea', 'Enable / Disable', '–', 'Không', 'Trống', '- Placeholder “Ghi chú nội bộ cho hạng mục...”'),
    ('Bảng phân công nhân sự', 'Table/Grid', 'Enable / Disable', '–', '–', 'Trống', ['- Cột: STT, Phòng ban, Nhân sự*, Vai '
     'trò dự án*, Mô tả công việc, Ngày bắt đầu*, Thao tác', '- Ô Nhân sự lọc theo phòng ban đã chọn, loại Leader và người '
     'đã có ở dòng khác', '- Ngày bắt đầu mặc định hôm nay', '- Rỗng: “Chưa có nhân sự nào. Bấm Thêm nhân sự để phân công.”']),
    ('Nút Thêm nhân sự / Xoá nhân sự', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Thêm dòng / bỏ dòng; ẩn khi khối bị khoá'),
    ('Lỗi validate', 'Toast / Alert', 'Hiển thị', '–', '–', 'Ẩn', '- Chữ đỏ dưới từng ô; form tự chuyển sang tab có lỗi')],
   [('Bấm Thêm hạng mục', 'Click', 'After:\n– Thêm khối mới mở sẵn ở cuối, cuộn tới khối.'),
    ('Bấm thùng rác', 'Click', 'After:\n– Bỏ khối khỏi form ngay; mã các khối sau đánh lại.'),
    ('Bấm Tạo nhanh → Lưu', 'Click', 'During:\n– Hạng mục dự án trống → “Bắt buộc phải nhập”.\nAfter:\n– Thêm vào danh '
     'mục, thông báo “Lưu thành công”.'),
    ('Đổi Phòng ban ở dòng nhân sự', 'Change', 'After:\n– Lọc lại ô Nhân sự theo phòng ban.'),
    ('Bấm nút lưu của form giải pháp', 'Click', 'Before:\n– Đủ điều kiện sửa giải pháp (SRS Quản lý giải pháp).\n'
     'During:\n– Hạng mục thiếu Tên / Leader / Ngày cần hoàn thành; dòng nhân sự thiếu Nhân sự / Vai trò / Ngày bắt đầu → '
     '“Bắt buộc phải nhập”.\n– Ngày cần hoàn thành trước hôm nay → “Phải lớn hơn hoặc bằng ngày hiện tại”.\n– “Giao cho '
     'Leader” khi chưa có hạng mục → “Vui lòng thêm ít nhất 1 hạng mục trước khi giao cho Leader”.\nAfter:\n– Hạng mục mới: '
     'trạng thái Chưa duyệt, tạo version V1; hạng mục cũ giữ trạng thái, đổi Ngày cần hoàn thành thì cập nhật ngày kết thúc '
     'version hiện tại.\n– Hạng mục không còn trên form bị xoá.\n– Quay về danh sách.')],
   uc=('FR-06', 'Khai hạng mục trên form GP', 'crud', A_PM), rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo.', 'create'))

# ---------------------------------------------------------------- 2.7 FR-07
fn('Leader duyệt hạng mục',
   dict(ten='Leader duyệt hạng mục', mota='Leader rà hạng mục mình phụ trách (ngày, ghi chú, nhân sự) rồi duyệt nhận '
        'việc; khi mọi hạng mục đã duyệt, giải pháp tự sang Đang triển khai.',
        tacnhan=A_LD, dieukien='Giải pháp Chờ Leader duyệt; người dùng là Leader của ít nhất 1 hạng mục Chưa duyệt.',
        chinh='1. Leader bấm “Lưu và duyệt” ở dòng hạng mục (danh sách Hạng mục giải pháp) — hoặc mở từ thông báo TB-01.\n'
              '2. Hệ thống mở màn Duyệt giải pháp ở tab Quản lý hạng mục, khối của Leader viền nổi bật, mở sẵn.\n'
              '3. Leader chỉnh Ngày cần hoàn thành, Ghi chú, bảng phân công nhân sự của hạng mục mình.\n'
              '4. Bấm “Lưu và duyệt”.\n5. Hệ thống chuyển MỌI hạng mục người đó làm Leader trong giải pháp sang Đang '
              'triển khai, thông báo “Đã lưu và duyệt thành công!”, quay về danh sách.',
        phu='• Hạng mục cuối cùng được duyệt → giải pháp tự chuyển Đang triển khai (không gửi thông báo).\n'
            '• Bấm “Sửa” ở dòng → màn Sửa giải pháp, nút “Lưu” chỉ lưu, chưa duyệt.\n'
            '• Tên hạng mục, Leader của hạng mục cũ bị khoá; tab Thông tin chỉ đọc; khối của Leader khác chỉ đọc.'),
   [('menu', MENU + ' => Lưu và duyệt'), ('img', '27-leader-duyet.png', 'Màn Duyệt giải pháp của Leader hạng mục')],
   [('Khối hạng mục của Leader', 'Table/Grid', 'Enable', '–', '–', 'Mở sẵn, viền xanh', '- Sửa được Ngày cần hoàn thành, '
     'Ghi chú, bảng nhân sự; Tên và Leader bị khoá'),
    ('Khối hạng mục khác', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Chỉ xem'),
    ('Nút Lưu và duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Chỉ ở màn Duyệt và khi Leader còn hạng mục '
     'Chưa duyệt'),
    ('Nút Lưu (màn Sửa)', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Lưu thay đổi, không duyệt'),
    ('Nút Quay lại', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Về danh sách Hạng mục giải pháp')],
   [('Bấm Lưu và duyệt', 'Click', 'Before:\n– Người dùng là Leader có hạng mục Chưa duyệt; giải pháp Chờ Leader duyệt.\n'
     + NO_ROLE + '\nDuring:\n– Lỗi bắt buộc / ngày như mục 2.6 → báo đỏ dưới ô, chuyển tới tab lỗi.\nAfter:\n– Lưu thay '
     'đổi; hạng mục của Leader → Đang triển khai, ghi ngày duyệt = hôm nay.\n– Đủ mọi hạng mục → giải pháp Đang triển khai.\n'
     '– “Đã lưu và duyệt thành công!”, về danh sách.'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về danh sách; có thay đổi chưa lưu thì hỏi xác nhận rời trang.')],
   uc=('FR-07', 'Leader duyệt hạng mục', 'action', A_LD), rule=('- Validate dữ liệu, Thông báo.', 'create'))

# ---------------------------------------------------------------- 2.8 FR-08
fn('PM lưu và duyệt hạng mục bổ sung',
   dict(ten='PM lưu và duyệt hạng mục', mota='Giải pháp đã Đang triển khai, PM thêm hạng mục mới và duyệt luôn, không cần '
        'Leader duyệt.', tacnhan=A_PM,
        dieukien='Giải pháp Đang triển khai, không phải dự án Tự triển khai; người dùng là PM.',
        chinh='1. PM mở màn Sửa giải pháp, tab Quản lý hạng mục.\n2. Thêm hạng mục mới (mục 2.6).\n3. Bấm “Lưu và duyệt '
              'hạng mục”.\n4. Hệ thống lưu, chuyển mọi hạng mục Chưa duyệt của giải pháp sang Đang triển khai, thông báo '
              '“Đã lưu và duyệt thành công!”, về danh sách.',
        phu='• Hạng mục đã lưu trước đó bị khoá, chỉ sửa khối mới.\n• Không gửi thông báo cho Leader của hạng mục mới.'),
   [('menu', MGP + ' => Lưu và duyệt hạng mục'), ('img', '25-gp-tab-hang-muc.png', 'Nút Lưu và duyệt hạng mục ở chân màn Sửa giải pháp')],
   [('Nút Lưu và duyệt hạng mục', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Chỉ khi giải pháp Đang triển khai, '
     'không Tự triển khai, không ở chế độ Duyệt'),
    ('Nút Tạo / Sửa hồ sơ trình duyệt giải pháp', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Thuộc SRS Quản lý giải pháp'),
    ('Khối hạng mục mới', 'Table/Grid', 'Enable', '–', 'Có', 'Mở sẵn', '- Như mục 2.6')],
   [('Bấm Lưu và duyệt hạng mục', 'Click', 'Before:\n– Người dùng là PM, giải pháp Đang triển khai.\n' + NO_ROLE +
     '\nDuring:\n– Lỗi bắt buộc / ngày như mục 2.6.\nAfter:\n– Lưu; mọi hạng mục Chưa duyệt → Đang triển khai, ngày duyệt = '
     'hôm nay.\n– “Đã lưu và duyệt thành công!”, về danh sách.')],
   uc=('FR-08', 'PM lưu và duyệt hạng mục', 'action', A_PM), rule=('- Validate dữ liệu, Thông báo.', 'create'))

# ---------------------------------------------------------------- 2.9 FR-09
fn('Mở màn Quản lý hạng mục',
   dict(ten='Mở màn Quản lý hạng mục', mota='Màn toàn trang theo dõi 1 hạng mục: thanh đầu, 9 tab, khối cảnh báo nhiệm vụ '
        'và biểu đồ ở tab đầu tiên.', tacnhan=A_TV, dieukien='Hạng mục nằm trong danh sách người dùng được xem.',
        chinh='1. Bấm Mã hạng mục ở danh sách.\n2. Hệ thống nạp thông tin hạng mục, số liệu cảnh báo, thống kê trạng thái '
              'nhiệm vụ, danh sách vấn đề.\n3. Hiển thị thanh đầu và tab đầu tiên (thống kê).',
        phu='• Hạng mục Đóng → hiện khung đỏ “Hạng mục đã đóng – Hạng mục này đã chuyển sang trạng thái Đóng do dự án đã '
            'đóng. Không thể sửa/xoá các đối tượng bên trong.”, ẩn nút Tạo mới / Sửa / Xoá / Thêm nhân sự ở các tab.\n'
            '• Quay lại từ màn meeting → mở lại đúng tab đang xem.\n• Tiêu đề tab trình duyệt: “Quản lý hạng mục: <mã> '
            '(<trạng thái>)”.'),
   [('menu', MQL), ('img', '13-tong-quan-951.png', 'Màn Quản lý hạng mục – tab thống kê (hạng mục Đang triển khai, người dùng là Leader)'),
    ('img', '20-hm-dong.png', 'Hạng mục Đóng – khung cảnh báo đầu màn')],
   [('Tiêu đề', 'Label', 'Hiển thị', '–', 'Theo dữ liệu', '- Tên hạng mục (trống thì “Quản lý hạng mục”)'),
    ('Nhãn mã / version / tiến độ', 'Badge', 'Read-only', '–', 'Theo dữ liệu', ['- Mã hạng mục; version hiện tại (Vn)',
     '- “Tiến độ: n%”: màu xanh lá ≥ 80, xanh dương ≥ 50, cam ≥ 20, đỏ < 20']),
    ('Nút Tạo hồ sơ trình duyệt / Sửa hồ sơ trình duyệt', 'Button', 'Enable / Ẩn', '–', 'Ẩn', '- Điều kiện bảng 3.3; mục 2.13'),
    ('Nút Tạo version', 'Button', 'Enable / Ẩn', '–', 'Ẩn', '- Chỉ khi hạng mục Đã duyệt hồ sơ trình duyệt; mục 2.23'),
    ('Nút Quay lại', 'Button', 'Enable', '–', 'Hiển thị', '- Về trang trước; mở ở tab mới thì về danh sách'),
    ('Thanh tab', 'Tab', 'Enable', '9 tab', 'Tab đầu', '- Tổng quan, Thông tin, Hồ sơ, Nhân sự, Nhiệm vụ, Vấn đề hạng mục, '
     'Meetings, Tiến độ, Files'),
    ('3 ô cảnh báo', 'Text', 'Read-only', '≥ 0', 'Theo dữ liệu', ['- Nhiệm vụ sắp tới hạn: “Trong N ngày” (N = số ngày '
     'cảnh báo hạn nhiệm vụ của công ty)', '- Nhân sự nhiều nhiệm vụ trễ: “Từ M nhiệm vụ trễ trở lên”', '- Nhiệm vụ cần '
     'duyệt: “Hoàn thành chờ duyệt kết quả”', '- Bấm mũi tên ở ô → mở popup tương ứng (mục 2.10)']),
    ('Biểu đồ Phân bổ trạng thái nhiệm vụ', 'Chart', 'Read-only', '–', 'Theo dữ liệu', ['- Vành khuyên: Chưa bắt đầu, Đang '
     'làm, Hoàn thành; nhãn “Total: n”', '- Không có số liệu → “Không có dữ liệu”']),
    ('Biểu đồ Mức độ ưu tiên của Vấn đề', 'Chart', 'Read-only', '–', 'Theo dữ liệu', '- Cột theo Khẩn cấp / Cao / Trung '
     'bình / Thấp; nhãn “n issue”'),
    ('Khung Hạng mục đã đóng', 'Toast / Alert', 'Hiển thị', '–', 'Ẩn', '- Chỉ khi trạng thái Đóng')],
   [('Mở màn', 'System', 'After:\n– Nạp hạng mục + 5 nhóm số liệu (sắp tới hạn, nhân sự trễ, thống kê, cần duyệt, vấn đề).\n'
     '– Lỗi từng nhóm thì nhóm đó hiện 0, không chặn màn.'),
    ('Bấm tab', 'Click', 'After:\n– Hiện nội dung tab (mục 2.11 – 2.22).'),
    ('Bấm mũi tên ô cảnh báo', 'Click', 'After:\n– Mở popup tương ứng (mục 2.10).'),
    ('Bấm Quay lại', 'Click', 'After:\n– Về trang trước / danh sách.')],
   uc=('FR-09', 'Mở màn Quản lý hạng mục', 'view', A_TV), rule=('- Màn Xem chi tiết và Phân quyền.', 'detail'), ui_kind='read')

# ---------------------------------------------------------------- 2.10 FR-10
fn('Popup cảnh báo nhiệm vụ',
   dict(ten='Popup Nhiệm vụ sắp hết hạn / Nhân sự nhiều nhiệm vụ trễ / Nhiệm vụ cần duyệt',
        mota='Liệt kê chi tiết con số ở 3 ô cảnh báo của màn Quản lý hạng mục.', tacnhan=A_TV,
        dieukien='Đang ở màn Quản lý hạng mục.',
        chinh='1. Bấm mũi tên ở 1 trong 3 ô cảnh báo.\n2. Popup mở, nạp danh sách tương ứng của hạng mục.\n'
              '3. Người dùng tìm / lọc / sắp xếp, bấm biểu tượng ở dòng nhiệm vụ để mở chi tiết nhiệm vụ.',
        phu='• Nhiệm vụ sắp hết hạn: nhiệm vụ đang làm có hạn từ bây giờ đến N ngày tới.\n'
            '• Nhân sự nhiều nhiệm vụ trễ: người có từ M nhiệm vụ quá hạn của hạng mục trở lên (M tối thiểu 1).\n'
            '• Nhiệm vụ cần duyệt: nhiệm vụ Chờ duyệt kết quả mà người dùng là người duyệt; nếu có quyền “Duyệt triển khai '
            'task” thì thêm nhiệm vụ Chờ duyệt triển khai của nhân viên phòng mình quản lý.'),
   [('menu', MQL + ' => Ô cảnh báo'), ('img', '14a-nv-sap-toi-han.png', 'Popup Nhiệm vụ sắp hết hạn'),
    ('img', '14b-ns-tre.png', 'Popup Nhân sự nhiều nhiệm vụ trễ'), ('img', '14c-nv-can-duyet.png', 'Popup Nhiệm vụ cần duyệt')],
   [('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống', ['- Nhiệm vụ: “Tìm theo mã, tên nhiệm vụ”', '- Nhân sự: '
     '“Tìm theo họ tên, email”']),
    ('Ô lọc (nhiệm vụ)', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', ['- Người làm, Người giao: nhân viên đang làm '
     'việc (không có người đã nghỉ)', '- Mức độ ưu tiên: danh mục ưu tiên', '- Trạng thái: bảng 3.4']),
    ('Ô lọc Email / Số điện thoại (nhân sự)', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- Có trên giao diện nhưng máy chủ '
     'chưa lọc theo 2 ô này'),
    ('Bảng nhiệm vụ', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Cột: STT, Mã-Tên nhiệm vụ (kèm Cập nhật / '
     'Bởi), Trạng thái, Ưu tiên, Người làm, Người duyệt, Hạn hoàn thành (kèm Ước lượng)', '- Biểu tượng “Xem chi tiết” / '
     '“Duyệt / Xem chi tiết” mở cửa sổ nhiệm vụ (SRS Nhiệm vụ)']),
    ('Bảng nhân sự', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Cột: STT, Họ tên (mã - tên), Email, Số điện '
     'thoại, Nhiệm vụ trễ (“n nhiệm vụ trễ”, nền đỏ)'),
    ('Thông báo rỗng', 'Text', 'Hiển thị', '–', '–', 'Ẩn', ['- “Không có nhiệm vụ sắp hết hạn hoặc quá hạn.”', '- “Không '
     'có nhân sự nào có quá nhiều nhiệm vụ trễ.”', '- “Không có nhiệm vụ cần duyệt.”']),
    ('Phân trang', 'Pagination', 'Enable', '5/10/…', '–', '5 (2 popup đầu), 10', '–'),
    ('Nút đóng ×', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Chỉ có dấu ×, nút “Đóng” ở chân bị ẩn')],
   [('Mở popup', 'System', 'After:\n– Nạp danh sách trang 1 theo bộ lọc mặc định.'),
    ('Tìm / chọn ô lọc', 'Keypress / Change', 'After:\n– Nạp lại từ trang 1.'),
    ('Bấm tiêu đề cột sắp xếp', 'Click', 'After:\n– Máy chủ nhận sắp xếp: nhiệm vụ theo Hạn hoàn thành, Ngày tạo, Ngày cập '
     'nhật; nhân sự theo Số nhiệm vụ trễ, Ngày tạo. Mặc định: sắp tới hạn theo hạn tăng dần, cần duyệt theo mới tạo trước, '
     'nhân sự theo số trễ giảm dần.'),
    ('Bấm biểu tượng ở dòng nhiệm vụ', 'Click', 'After:\n– Mở cửa sổ chi tiết / nhập kết quả / duyệt của nhiệm vụ (SRS '
     'Nhiệm vụ).')] + ev_page() + [ev_close('popup')],
   rule=('- Màn Danh sách, Phân trang.', 'list'), ui_kind='input')

# ---------------------------------------------------------------- 2.11 FR-11
fn('Tab Thông tin',
   dict(ten='Tab Thông tin hạng mục', mota='Xem thông tin hạng mục, khách hàng, yêu cầu làm giải pháp, dự án TKT, tài chính.',
        tacnhan=A_TV, dieukien='Đang ở màn Quản lý hạng mục.',
        chinh='1. Bấm tab “Thông tin”.\n2. Hệ thống hiển thị 5 khối chỉ đọc.',
        phu='• Trường trống → “—”.\n• Khối Khách hàng cuối chỉ hiện khi dự án có khách hàng trung gian.'),
   [('menu', MQL + ' => Thông tin'), ('img', '07-tab-thong-tin.png', 'Tab Thông tin')],
   [('Khối THÔNG TIN HẠNG MỤC', 'Text', 'Read-only', '–', 'Theo dữ liệu', ['- Nhãn trạng thái + mã hạng mục', '- Tên hạng mục, '
     'Trưởng nhóm (Leader), Deadline (dd/mm/yyyy)', '- Giải pháp (mã - tên), Trạng thái GP (nhãn màu), Phòng ban (phòng tiếp '
     'nhận yêu cầu làm giải pháp)', '- Ghi chú (chỉ hiện khi có)']),
    ('Khối THÔNG TIN KHÁCH HÀNG', 'Text', 'Read-only', '–', 'Theo dữ liệu', ['- Khách hàng “mã . tên”: bấm → mở chi tiết khách '
     'hàng ở tab mới', '- Người liên hệ, Chức vụ, Email, SĐT người liên hệ', '- Khách hàng cuối + 4 trường liên hệ (KH cuối)']),
    ('Khối YÊU CẦU LÀM GIẢI PHÁP', 'Text', 'Read-only', '–', 'Theo dữ liệu', '- Mã YCLGP, Nội dung, Người tạo YC, Ngày tạo, '
     'Trạng thái'),
    ('Khối DỰ ÁN TIỀN KHẢ THI', 'Text', 'Read-only', '–', 'Theo dữ liệu', '- Tên dự án, PM chính (PM của giải pháp), Deadline '
     'GP (Vn), Ngành'),
    ('Khối NGUỒN VỐN & KỲ VỌNG TÀI CHÍNH', 'Text', 'Read-only', '–', 'Theo dữ liệu', '- Nguồn vốn (bảng 3.4), Ngân sách dự '
     'kiến, Giá trị HĐ dự kiến, Lợi nhuận kỳ vọng (định dạng tiền ₫, dấu phẩy ngăn nghìn)')],
   [('Bấm tab Thông tin', 'Click', 'After:\n– Hiển thị dữ liệu đã nạp khi mở màn (không gọi thêm).'),
    ('Bấm tên khách hàng / khách hàng cuối', 'Click', 'After:\n– Mở màn chi tiết khách hàng ở tab mới.')],
   rule=('- Màn Xem chi tiết.', 'detail'), ui_kind='read')

# ---------------------------------------------------------------- 2.12 FR-12
fn('Tab Hồ sơ',
   dict(ten='Tab Hồ sơ – danh sách hồ sơ trình duyệt hạng mục', mota='Liệt kê mọi hồ sơ trình duyệt của hạng mục qua các version.',
        tacnhan=A_TV, dieukien='Đang ở màn Quản lý hạng mục.',
        chinh='1. Bấm tab “Hồ sơ”.\n2. Hệ thống nạp hồ sơ, mới tạo trước, 10 dòng/trang.\n3. Bấm “Xem” để xem hồ sơ (mục 2.14); '
              'PM bấm “Duyệt” ở hồ sơ Chờ duyệt (mục 2.15); người tạo bấm “Sửa” ở hồ sơ Nháp (mục 2.13).',
        phu='• Chưa có hồ sơ → “Không có dữ liệu.”.\n• Lỗi → “Lỗi khi tải dữ liệu hồ sơ trình duyệt”.'),
   [('menu', MQL + ' => Hồ sơ'), ('img', '08-tab-ho-so.png', 'Tab Hồ sơ – hạng mục có hồ sơ Đã duyệt và Không duyệt')],
   [('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- “Tìm theo mã hồ sơ”; máy chủ tìm theo mã hoặc nội dung'),
    ('Ô lọc Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống', '- Bảng 3.4'),
    ('Ô lọc Version HM', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '- Các version của hạng mục'),
    ('Ô lọc Ngày gửi / Hạn duyệt', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', '- Khoảng ngày trong 1 ô'),
    ('Bảng hồ sơ', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Cột: STT, Mã / Nội dung hồ sơ (kèm nút), Tên hồ '
     'sơ, Version HM, Trạng thái, Ngày gửi, Hạn duyệt', '- Không cột nào sắp xếp được']),
    ('Nút Xem (con mắt)', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Mọi dòng'),
    ('Nút Sửa / Duyệt (bút)', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Ẩn', ['- “Sửa”: hồ sơ Nháp, người dùng là người tạo',
     '- “Duyệt”: hồ sơ Chờ duyệt, người dùng là PM']),
    ('Phân trang', 'Pagination', 'Enable', '10/20/50…', '–', '10', '–')],
   [('Bấm tab Hồ sơ', 'Click', 'After:\n– Nạp danh sách hồ sơ.'),
    ('Tìm / lọc', 'Keypress / Change', 'After:\n– Nạp lại từ trang 1.'),
    ('Bấm Xem', 'Click', 'After:\n– Mở cửa sổ hồ sơ chỉ đọc (mục 2.14).'),
    ('Bấm Sửa / Duyệt', 'Click', 'Before:\n' + NO_ROLE + '\nAfter:\n– Sửa → cửa sổ hồ sơ sửa được (mục 2.13); Duyệt → cửa sổ '
     'chế độ PM (mục 2.15).')] + ev_page(),
   rule=('- Màn Danh sách, Phân trang.', 'list'), ui_kind='input')

# ---------------------------------------------------------------- 2.13 FR-13
fn('Tạo / trình hồ sơ trình duyệt hạng mục',
   dict(ten='Tạo, lưu nháp và trình hồ sơ trình duyệt hạng mục',
        mota='Leader lập hồ sơ kết quả hạng mục (tên, nội dung, tài liệu, BOM tổng hợp tự gắn) để PM duyệt.',
        tacnhan=A_LD,
        dieukien='Hạng mục Đang triển khai; người dùng là Leader; chưa có hồ sơ hoặc hồ sơ mới nhất Nháp / Không duyệt / Hết hiệu lực.',
        chinh='1. Bấm “Tạo hồ sơ trình duyệt” (hoặc “Sửa hồ sơ trình duyệt” khi đã có Nháp) ở thanh đầu.\n'
              '2. Cửa sổ mở; nếu đang có hồ sơ Nháp thì nạp lại nội dung Nháp.\n3. Nhập Tên hồ sơ, Nội dung trình duyệt, thêm '
              'tài liệu, chọn Hạn duyệt.\n4. Hệ thống tự tìm BOM tổng hợp Hoàn thành của version hạng mục hiện tại để hiển thị.\n'
              '5. Bấm “Lưu” (giữ Nháp) hoặc “Lưu & Trình duyệt”.\n6. Trình duyệt thành công → hồ sơ Chờ duyệt, hạng mục Chờ duyệt '
              'hồ sơ trình duyệt, BOM gắn vào hồ sơ.',
        phu='• Mỗi hạng mục chỉ có 1 hồ sơ Nháp: lưu lại là ghi đè hồ sơ Nháp đó; hồ sơ Không duyệt / Hết hiệu lực thì tạo hồ '
            'sơ mới, mã tăng số thứ tự.\n'
            '• Không có BOM tổng hợp Hoàn thành → khung đỏ “Chưa có BOM tổng hợp ở trạng thái Hoàn thành cho version hạng mục '
            'này. Vui lòng lập BOM tổng hợp trước khi gửi hồ sơ.”; Lưu nháp vẫn được, Trình duyệt bị chặn.\n'
            '• Dự án Tự triển khai: không có BOM vẫn trình được nhưng bắt buộc có tài liệu.\n'
            '• Lưu nháp vẫn bắt buộc Tên hồ sơ, Nội dung, Hạn duyệt.',
        dacbiet='Không gửi thông báo cho PM khi trình hồ sơ.'),
   [('menu', MQL + ' => Tạo hồ sơ trình duyệt'), ('modal', 'Tạo hồ sơ trình duyệt'),
    ('img', '24-tao-ho-so.png', 'Cửa sổ Tạo hồ sơ trình duyệt (chưa có BOM tổng hợp Hoàn thành)'),
    ('img', '24b-tao-ho-so-duoi.png', 'Phần dưới cửa sổ: danh sách file, BOM tổng hợp, người phê duyệt')],
   [('Tiêu đề cửa sổ', 'Label', 'Hiển thị', '–', '–', 'Theo dữ liệu', '- “Tạo hồ sơ trình duyệt” / “Sửa hồ sơ trình duyệt: <mã>”'),
    ('Tên hồ sơ', 'Textbox', 'Enable', '0–255 ký tự', 'Có', 'Trống', '- Placeholder “Nhập tên hồ sơ”'),
    ('Nội dung trình duyệt', 'Textarea', 'Enable', 'Văn bản định dạng', 'Có', 'Trống', '- Trình soạn thảo (đậm, nghiêng, danh '
     'sách, liên kết, Source)'),
    ('Danh sách các file', 'Table/Grid', 'Enable', '–', 'Có với dự án Tự triển khai không có BOM', '1 dòng trống',
     ['- Cột: STT, Tên tài liệu*, Loại tài liệu, Người thực hiện, File đính kèm*, Dung lượng', '- Nút “Thêm file”; dòng '
      'không có file bị bỏ khi lưu', '- Dòng có file: đủ Tên tài liệu, Loại tài liệu, Người thực hiện, tên file (máy chủ '
      'kiểm)', '- Người thực hiện: nhân sự của hạng mục']),
    ('BOM tổng hợp gắn vào hồ sơ', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Có BOM: khung xanh “<mã> — <tên>”, '
     'bấm mở BOM ở tab mới', '- Không có BOM: khung đỏ (dự án thường) hoặc vàng (Tự triển khai)']),
    ('Bình luận', 'Text', 'Enable / Ẩn', '–', 'Không', 'Ẩn', '- Chỉ hiện khi hồ sơ đã được lưu ít nhất 1 lần'),
    ('Khối Thông tin tham chiếu', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Hạng mục, Giải pháp, Dự án', '- Leader '
     'phụ trách', '- Ngày trình duyệt (khi đã trình), Thời gian thực hiện (ngày duyệt hạng mục – ngày trình)', '- PM duyệt']),
    ('Hạn duyệt', 'Datepicker', 'Enable', 'dd/mm/yyyy, ≥ hôm nay', 'Có', 'Trống', '- Không gõ tay, chỉ chọn lịch'),
    ('Nút Lưu & Trình duyệt / Lưu / Đóng', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng: đóng không lưu')],
   [('Mở cửa sổ', 'System', 'After:\n– Tìm hồ sơ Nháp của hạng mục để nạp lại; tìm BOM tổng hợp Hoàn thành của version hiện tại.'),
    ('Bấm Lưu', 'Click', 'Before:\n– Hạng mục Đang triển khai, nếu không → “Chỉ được tạo hồ sơ trình duyệt khi hạng mục ở trạng '
     'thái Đang triển khai.”.\nDuring:\n– Tên trống → “Vui lòng nhập tên hồ sơ.”; Nội dung / Hạn duyệt trống → “Bắt buộc phải '
     'nhập”; Hạn duyệt trước hôm nay → “Hạn duyệt phải lớn hơn hoặc bằng ngày hôm nay.”.\n– Dòng file thiếu trường → “Bắt buộc '
     'phải nhập”.\n– Có lỗi → “Vui lòng kiểm tra lại dữ liệu nhập”, không lưu.\nAfter:\n– Lưu / ghi đè hồ sơ Nháp; thông báo '
     '“Đã lưu hồ sơ trình duyệt ở trạng thái nháp.”; đóng cửa sổ, nạp lại màn.'),
    ('Bấm Lưu & Trình duyệt', 'Click', 'Before / During:\n– Như Lưu.\n– Không có BOM tổng hợp Hoàn thành (trừ Tự triển khai) → '
     '“Chưa có BOM tổng hợp Hoàn thành cho version hạng mục này. Vui lòng lập BOM tổng hợp trước khi gửi hồ sơ.”.\n– Tự triển '
     'khai, không BOM, không file → “Vui lòng đính kèm ít nhất 1 tài liệu khi hồ sơ không đính kèm BOM list.”.\nAfter:\n– Hồ sơ → '
     'Chờ duyệt, Ngày gửi = hôm nay; gắn BOM; BOM tổng hợp cập nhật trạng thái theo hồ sơ.\n– Hạng mục → Chờ duyệt hồ sơ trình '
     'duyệt.\n– “Đã lưu và gửi trình duyệt hồ sơ hạng mục.”; đóng cửa sổ, nạp lại màn.'), ev_close()],
   uc=('FR-13', 'Tạo / trình hồ sơ', 'crud', A_LD), rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo.', 'create'))

# ---------------------------------------------------------------- 2.14 FR-14
fn('Xem hồ sơ trình duyệt',
   dict(ten='Xem hồ sơ trình duyệt hạng mục', mota='Xem chỉ đọc 1 hồ sơ, gồm lý do từ chối nếu có.', tacnhan=A_TV,
        dieukien='Đang ở tab Hồ sơ (hoặc tab Files, bấm liên kết nguồn HSTD).',
        chinh='1. Bấm “Xem” ở dòng hồ sơ.\n2. Cửa sổ “Xem hồ sơ trình duyệt: <mã>” mở, mọi ô bị khoá.',
        phu='• Hồ sơ Không duyệt → khung đỏ “Lý do từ chối” ở đầu cửa sổ.\n• Chân cửa sổ chỉ có nút Đóng.'),
   [('menu', MQL + ' => Hồ sơ => Xem'), ('modal', 'Xem hồ sơ trình duyệt'),
    ('img', '09-xem-ho-so-tu-choi.png', 'Xem hồ sơ Không duyệt – có khung Lý do từ chối'),
    ('img', '09b-xem-ho-so-da-duyet.png', 'Xem hồ sơ Đã duyệt')],
   [('Khung Lý do từ chối', 'Text', 'Read-only', '–', 'Ẩn', '- Chỉ khi hồ sơ Không duyệt và có lý do'),
    ('Tên hồ sơ, Nội dung trình duyệt', 'Text', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('Danh sách các file', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', '–'),
    ('BOM tổng hợp gắn vào hồ sơ', 'Link', 'Read-only', '–', 'Theo dữ liệu', '- Bấm → mở BOM ở tab mới'),
    ('Bình luận', 'Text', 'Enable', '–', 'Theo dữ liệu', '- Xem và thêm bình luận của hồ sơ'),
    ('Khối Thông tin tham chiếu', 'Text', 'Read-only', '–', 'Theo dữ liệu', '- Như mục 2.13'),
    ('Nút Đóng / ×', 'Button', 'Enable', '–', 'Hiển thị', '–')],
   [('Bấm Xem', 'Click', 'After:\n– Mở cửa sổ chỉ đọc với dữ liệu dòng đã chọn.'),
    ('Bấm liên kết BOM', 'Click', 'After:\n– Mở chi tiết BOM ở tab mới.'), ev_close()],
   rule=('- Màn Xem chi tiết.', 'detail'), ui_kind='read')

# ---------------------------------------------------------------- 2.15 FR-15
fn('PM duyệt / từ chối hồ sơ hạng mục',
   dict(ten='PM duyệt / từ chối hồ sơ trình duyệt hạng mục', mota='PM chấp thuận kết quả hạng mục hoặc trả về cho Leader làm lại.',
        tacnhan=A_PM, dieukien='Hồ sơ Chờ duyệt; người dùng là PM của giải pháp (hoặc PM ghi trên hồ sơ).',
        chinh='1. Ở tab Hồ sơ, PM bấm “Duyệt” (biểu tượng bút) ở hồ sơ Chờ duyệt.\n2. Cửa sổ “Duyệt hồ sơ trình duyệt: <mã>” mở '
              'chỉ đọc.\n3. Bấm “Duyệt” → hồ sơ Đã duyệt, hạng mục Đã duyệt hồ sơ trình duyệt.\n4. Hoặc bấm “Từ chối” → nhập '
              '“Lý do từ chối” → bấm “Từ chối” → hồ sơ Không duyệt, hạng mục về Đang triển khai.',
        phu='• Nút “Duyệt” KHÔNG hỏi xác nhận.\n• Hồ sơ đã được xử lý trước → “Chỉ được duyệt hồ sơ đang ở trạng thái chờ duyệt.”.\n'
            '• Không phải PM → “Bạn không có quyền duyệt hồ sơ trình duyệt này.”.',
        dacbiet='Không gửi thông báo cho Leader khi duyệt / từ chối.'),
   [('menu', MQL + ' => Hồ sơ => Duyệt'), ('modal', 'Duyệt hồ sơ trình duyệt'),
    ('img', '10-pm-duyet-ho-so.png', 'Cửa sổ Duyệt hồ sơ trình duyệt (chế độ PM)'),
    ('img', '11-tu-choi-ho-so.png', 'Cửa sổ nhập lý do Từ chối hồ sơ')],
   [('Nội dung hồ sơ', 'Text', 'Read-only', '–', '–', 'Theo dữ liệu', '- Như mục 2.14'),
    ('Nút Duyệt', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Chỉ ở chế độ PM + hồ sơ Chờ duyệt'),
    ('Nút Từ chối', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Mở cửa sổ “Từ chối hồ sơ: <mã>”'),
    ('Lý do từ chối', 'Textarea', 'Enable', '0–1000 ký tự', 'Có', 'Trống', '- Placeholder “Nhập lý do từ chối”'),
    ('Nút Từ chối / Hủy (cửa sổ lý do)', 'Button', 'Enable', '–', '–', 'Hiển thị', '- Hủy: đóng cửa sổ lý do, giữ cửa sổ hồ sơ')],
   [('Bấm Duyệt', 'Click', 'Before:\n– Người dùng là PM, hồ sơ Chờ duyệt, nếu không → thông báo lỗi của máy chủ.\nAfter:\n– Hồ '
     'sơ → Đã duyệt, ghi thời điểm duyệt; BOM tổng hợp cập nhật theo.\n– Hạng mục → Đã duyệt hồ sơ trình duyệt.\n– “Đã duyệt hồ '
     'sơ trình duyệt.”; đóng cửa sổ, nạp lại màn.'),
    ('Bấm Từ chối (cửa sổ lý do)', 'Click', 'During:\n– Lý do trống → “Vui lòng nhập lý do không duyệt.”; quá 1000 ký tự → “Lý '
     'do không duyệt không được vượt quá 1000 ký tự.”.\nAfter:\n– Hồ sơ → Không duyệt, lưu lý do; hạng mục → Đang triển khai.\n'
     '– “Đã từ chối hồ sơ trình duyệt.”; đóng cả 2 cửa sổ, nạp lại màn.'),
    ('Bấm Hủy (cửa sổ lý do)', 'Click', 'After:\n– Đóng cửa sổ lý do, không lưu.'), ev_close()],
   uc=('FR-15', 'Duyệt / từ chối hồ sơ', 'action', A_PM), rule=('- Thông báo, Quy tắc ghi lịch sử.', 'notice'))

# ---------------------------------------------------------------- 2.16 FR-16
fn('Tab Nhân sự',
   dict(ten='Tab Nhân sự hạng mục', mota='Xem Leader và thành viên của hạng mục, vai trò, số nhiệm vụ đang phụ trách.',
        tacnhan=A_TV, dieukien='Đang ở màn Quản lý hạng mục.',
        chinh='1. Bấm tab “Nhân sự”.\n2. Hệ thống hiển thị Leader (dòng đầu, vai trò “Leader hạng mục”) và các thành viên.',
        phu='• Một người có nhiều vai trò → gộp 1 dòng, vai trò nối bằng dấu phẩy.\n• Không có ai → “Chưa có nhân sự nào trong '
            'hạng mục”.'),
   [('menu', MQL + ' => Nhân sự'), ('img', '15-tab-nhan-su.png', 'Tab Nhân sự')],
   [('Nhãn Leader / Thành viên', 'Badge', 'Read-only', '–', 'Theo dữ liệu', '- “Leader: <tên>” (chưa có: “Chưa có Leader”), '
     '“Thành viên: n” (n tính cả Leader)'),
    ('Nút Thêm nhân sự', 'Button', 'Enable / Ẩn', '–', 'Hiển thị', '- Ẩn khi hạng mục Đóng; mục 2.17'),
    ('Bảng nhân sự', 'Table/Grid', 'Read-only', '–', 'Theo dữ liệu', ['- Cột: STT, Thành viên (ảnh, tên, email), Vai trò, Ngày '
     'bắt đầu, Ngày kết thúc (= ngày cần hoàn thành hạng mục), Nhiệm vụ đang phụ trách (số nhiệm vụ đang làm), Trạng thái '
     '(luôn “Active”)', '- Không phân trang, không sắp xếp'])],
   [('Bấm tab Nhân sự', 'Click', 'After:\n– Nạp danh sách nhân sự; lỗi → “Không thể tải danh sách nhân sự”.')],
   rule=('- Màn Xem chi tiết.', 'detail'), ui_kind='read')

# ---------------------------------------------------------------- 2.17 FR-17
fn('Thêm nhân sự vào hạng mục',
   dict(ten='Thêm nhân sự vào hạng mục', mota='Bổ sung thành viên cho hạng mục ngay ở màn Quản lý.', tacnhan=A_TV,
        dieukien='Hạng mục không Đóng.',
        chinh='1. Bấm “Thêm nhân sự” ở tab Nhân sự.\n2. Cửa sổ “Thêm nhân sự vào hạng mục” mở.\n3. Chọn Thành viên, Vai trò dự án, '
              'nhập Mô tả công việc, chọn Ngày bắt đầu.\n4. Bấm “Thêm nhân sự” ở chân cửa sổ.\n5. Hệ thống thêm thành viên, '
              'đóng cửa sổ, nạp lại bảng.',
        phu='• Ô Thành viên đã loại những người đang là thành viên.\n• Thành công không hiện thông báo.',
        dacbiet='Hiện tại chân cửa sổ bị ẩn nên không thấy nút “Thêm nhân sự” / “Huỷ” — xem danh sách điểm lệch.'),
   [('menu', MQL + ' => Nhân sự => Thêm nhân sự'), ('modal', 'Thêm nhân sự vào hạng mục'),
    ('img', '16-them-nhan-su.png', 'Cửa sổ Thêm nhân sự vào hạng mục')],
   [('Thành viên', 'Dropdown', 'Enable', 'Danh sách nhân viên', 'Có', 'Trống', '- Nhân viên của dữ liệu chung, trừ người đã là '
     'thành viên; placeholder “Chọn thành viên”'),
    ('Vai trò dự án', 'Dropdown', 'Enable', 'Danh mục Vai trò dự án', 'Có', 'Trống', '- Nạp khi mở cửa sổ'),
    ('Mô tả công việc', 'Textarea', 'Enable', '–', 'Không', 'Trống', '- “Nhập mô tả công việc...”'),
    ('Ngày bắt đầu', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Có', 'Trống', '–'),
    ('Nút Thêm nhân sự / Huỷ', 'Button', 'Ẩn', '–', '–', 'Ẩn', '- Khai ở chân cửa sổ nhưng chân đang bị ẩn'),
    ('Nút ×', 'Icon Button', 'Enable', '–', '–', 'Hiển thị', '- Đóng, không lưu')],
   [('Bấm Thêm nhân sự (tab)', 'Click', 'After:\n– Xoá form cũ, nạp danh mục vai trò, mở cửa sổ.'),
    ('Bấm Thêm nhân sự (chân cửa sổ)', 'Click', 'During:\n– Thiếu Thành viên → “Vui lòng chọn thành viên.”; thiếu Vai trò → '
     '“Vui lòng chọn vai trò dự án.”; thiếu / sai Ngày bắt đầu → “Vui lòng chọn ngày bắt đầu.” / “Ngày bắt đầu không hợp '
     'lệ.”.\nAfter:\n– Thêm thành viên vào hạng mục; đóng cửa sổ, nạp lại bảng.'), ev_close()],
   uc=('FR-17', 'Thêm nhân sự', 'crud', A_TV), rule=('- Màn Thêm mới, Validate dữ liệu.', 'create'))

# ---------------------------------------------------------------- 2.18 FR-18
fn('Tab Nhiệm vụ',
   dict(ten='Tab Nhiệm vụ của hạng mục', mota='Danh sách nhiệm vụ thuộc hạng mục và lối tạo / xử lý nhiệm vụ. Cửa sổ nhiệm vụ '
        'đặc tả ở SRS Nhiệm vụ.', tacnhan=A_TV, dieukien='Đang ở màn Quản lý hạng mục.',
        chinh='1. Bấm tab “Nhiệm vụ”.\n2. Hệ thống nạp nhiệm vụ của hạng mục (trừ nhiệm vụ Nháp của người khác), mới tạo trước.\n'
              '3. Người dùng lọc nhanh Tôi làm / Tôi giao / Tôi theo dõi / Tôi duyệt kết quả, tạo mới, xem, sửa, nhập kết quả, '
              'duyệt, xem lịch sử, xoá.',
        phu='• Nút Tạo mới chỉ hiện khi hạng mục Đang triển khai hoặc Chờ duyệt hồ sơ trình duyệt.\n'
            '• Xoá: hộp xác nhận “Bạn có chắc muốn xoá task “<tên>” không?” → “Xóa nhiệm vụ thành công”.'),
   [('menu', MQL + ' => Nhiệm vụ'), ('img', '17-tab-nhiem-vu.png', 'Tab Nhiệm vụ')],
   [('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- “Tìm theo mã, tên nhiệm vụ”'),
    ('Ô lọc Người thực hiện / Người giao / Người duyệt kết quả', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     '- Nhân viên đang làm việc; người đã nghỉ không có'),
    ('Ô lọc Trạng thái / Mức độ ưu tiên / Version hạng mục', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     '- Trạng thái theo bảng 3.4; version: các version của hạng mục'),
    ('Ô lọc Ngày cập nhật / Hạn hoàn thành', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', '- Khoảng ngày'),
    ('Nút Tạo mới / Xuất Excel / Cấu hình cột', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Xuất file danh_sach_nhiem_vu.xls '
     'theo bộ lọc; cấu hình cột lưu theo người dùng'),
    ('Nhãn Quá hạn + 4 nút lọc nhanh', 'Button', 'Enable', '–', '–', 'Hiển thị', '- “Quá hạn: n”; bấm lại nút đang chọn để bỏ lọc; '
     'dòng “Đang lọc: …” kèm nút ×'),
    ('Bảng nhiệm vụ', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', ['- Cột: STT, Mã-Tên nhiệm vụ (kèm Cập nhật/Bởi, '
     'trạng thái hạn), Version HM, Trạng thái, Ưu tiên, Người làm, Người theo dõi, Người duyệt, Người tạo, Ngày bắt đầu, Hạn '
     'hoàn thành (kèm Ước lượng), Checklist-Nhiệm vụ con', '- Không cột nào sắp xếp được']),
    ('Nút ở dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo dữ liệu', '- Xem, Sửa, Nhập kết quả, Duyệt, Lịch sử chỉnh sửa, '
     'Xoá theo cờ quyền của từng nhiệm vụ; Sửa / Xoá ẩn khi hạng mục Đóng'),
    ('Phân trang', 'Pagination', 'Enable', '10/20/50…', '–', '10', '–')],
   [('Bấm tab Nhiệm vụ', 'Click', 'After:\n– Nạp danh sách + số quá hạn; lỗi → “Lỗi khi tải dữ liệu nhiệm vụ”.'),
    ('Bấm nút lọc nhanh', 'Click', 'After:\n– Đặt điều kiện theo người đang đăng nhập, nạp lại từ trang 1.'),
    ('Bấm Tạo mới', 'Click', 'After:\n– Mở cửa sổ tạo nhiệm vụ, điền sẵn giải pháp, hạng mục, dự án.'),
    ('Bấm nút ở dòng', 'Click', 'After:\n– Mở cửa sổ tương ứng của nhiệm vụ (SRS Nhiệm vụ); Xoá → hộp xác nhận rồi xoá.'),
    ('Bấm Xuất Excel', 'Click', 'After:\n– Tải file; “Xuất Excel thành công” / “Lỗi khi xuất Excel”.')] + ev_page(),
   rule=('- Màn Danh sách, Phân trang, Quy tắc Xoá.', 'list'), ui_kind='input')

# ---------------------------------------------------------------- 2.19 FR-19
fn('Tab Vấn đề hạng mục',
   dict(ten='Tab Vấn đề hạng mục', mota='Danh sách vấn đề gắn với hạng mục; cửa sổ vấn đề đặc tả ở SRS Vấn đề.', tacnhan=A_TV,
        dieukien='Đang ở màn Quản lý hạng mục.',
        chinh='1. Bấm tab “Vấn đề hạng mục”.\n2. Hệ thống nạp vấn đề của hạng mục (theo phạm vi xem vấn đề của người dùng).\n'
              '3. Người dùng lọc nhanh Tôi làm / Tôi báo cáo / Tôi theo dõi, tạo mới, xem, sửa, xử lý, xem lịch sử, xoá.',
        phu='• Tạo mới chỉ khi hạng mục Đang triển khai / Chờ duyệt hồ sơ trình duyệt; giải pháp, hạng mục, dự án bị khoá sẵn.\n'
            '• Rỗng → “Không có Vấn đề nào phù hợp bộ lọc.”.'),
   [('menu', MQL + ' => Vấn đề hạng mục'), ('img', '18-tab-van-de.png', 'Tab Vấn đề hạng mục')],
   [('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- “Tìm theo mã, tên vấn đề”'),
    ('Ô lọc Người xử lý / Người tạo / Người duyệt', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '- Nhân viên đang làm việc'),
    ('Ô lọc Trạng thái / Mức độ ưu tiên / Ngày tạo / Version hạng mục', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     '- Giá trị theo bảng 3.4'),
    ('Nút Tạo mới / Xuất Excel / Tùy chỉnh cột', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- File danh_sach_issue.xls'),
    ('Bảng vấn đề', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Cột: STT, Mã-Tên Vấn đề, Version HM, Người xử lý (kèm '
     'người theo dõi), Ưu tiên, Trạng thái; máy chủ sắp theo Ngày tạo giảm dần'),
    ('Nút ở dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo dữ liệu', '- Xem, Sửa, Lịch sử, Xoá, Xử lý theo cờ của từng vấn '
     'đề; ẩn Sửa / Xoá / Xử lý khi hạng mục Đóng'),
    ('Phân trang', 'Pagination', 'Enable', '10/20/50…', '–', '10', '–')],
   [('Bấm tab', 'Click', 'After:\n– Nạp danh sách; lỗi → “Lỗi khi tải dữ liệu Vấn đề”.'),
    ('Bấm Xoá ở dòng', 'Click', 'After:\n– Hộp xác nhận “Bạn có chắc muốn xoá issue “<tên>” không?” → “Xóa Vấn đề thành công”.'),
    ('Bấm Xem / Sửa / Xử lý / Lịch sử', 'Click', 'After:\n– Mở cửa sổ vấn đề tương ứng (SRS Vấn đề).')] + ev_page(),
   rule=('- Màn Danh sách, Phân trang, Quy tắc Xoá.', 'list'), ui_kind='input')

# ---------------------------------------------------------------- 2.20 FR-20
fn('Tab Meetings',
   dict(ten='Tab Meetings của hạng mục', mota='Danh sách meeting gắn với hạng mục; màn meeting đặc tả ở SRS Meeting.', tacnhan=A_TV,
        dieukien='Đang ở màn Quản lý hạng mục.',
        chinh='1. Bấm tab “Meetings”.\n2. Hệ thống nạp meeting gắn hạng mục (trừ meeting đang tạo của người khác), mới tạo trước.\n'
              '3. Người dùng tạo mới, xem, sửa, in biên bản, tạo phiếu công tác, xoá.',
        phu='• Rỗng → “Không có dữ liệu.”.\n• Xoá: hộp xác nhận “Bạn có chắc muốn xóa meeting ‘<tên>’?” → “Xóa thành công”.'),
   [('menu', MQL + ' => Meetings'), ('img', '19-tab-meetings.png', 'Tab Meetings')],
   [('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- “Tìm theo mã, tên meeting”'),
    ('Ô lọc', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '- Loại Meeting (danh mục), Hình thức, Trạng thái, Có biên bản?, '
     'Người cập nhật gần nhất (nhân viên đang làm việc), Version hạng mục'),
    ('Nút Tạo mới', 'Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Khi hạng mục thuộc dự án và chưa Đóng; mở màn tạo meeting gắn '
     'sẵn dự án, hạng mục'),
    ('Nút Xuất Excel / Tùy chỉnh cột', 'Button', 'Enable', '–', '–', 'Hiển thị', '- File danh_sach_cuoc_hop.xls'),
    ('Bảng meeting', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Cột: STT, Mã / Tên Meeting (người tạo, ngày tạo, cập '
     'nhật), Version HM, Thời gian (sắp xếp được), Thời lượng họp, Loại & Hình thức, Khách hàng, Thành phần tham dự, Trạng '
     'thái, Biên bản'),
    ('Nút ở dòng', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Theo dữ liệu', ['- Xem (mở tab mới được), In', '- Chỉnh sửa, Tạo phiếu '
     'công tác khác: ẩn khi meeting Đã hoàn thành / Huỷ hoặc hạng mục Đóng', '- Xoá: chỉ meeting Lưu nháp, hạng mục chưa Đóng']),
    ('Phân trang', 'Pagination', 'Enable', '10/20/50…', '–', '10', '–')],
   [('Bấm tab', 'Click', 'After:\n– Nạp danh sách; lỗi → “Lỗi khi tải dữ liệu meeting”.'),
    ('Bấm tiêu đề cột Thời gian', 'Click', 'After:\n– Gửi yêu cầu sắp xếp (xem điểm lệch: máy chủ chưa nhận khoá cột này).'),
    ('Bấm Xem / Chỉnh sửa', 'Click', 'After:\n– Chuyển sang màn meeting; Quay lại → về đúng tab Meetings.'),
    ('Bấm In', 'Click', 'After:\n– Mở cửa sổ xem trước “Xem biên bản cuộc họp”.'),
    ('Bấm Xoá → Xóa', 'Click', 'After:\n– Xoá meeting, “Xóa thành công”, nạp lại; lỗi → thông báo của máy chủ.')] + ev_page(),
   rule=('- Màn Danh sách, Phân trang, Quy tắc Xoá.', 'list'), ui_kind='input')

# ---------------------------------------------------------------- 2.21 FR-21
fn('Tab Tiến độ – phân bổ % nhiệm vụ',
   dict(ten='Phân bổ % tiến độ theo nhiệm vụ', mota='Leader chia trọng số % cho từng nhiệm vụ của version hạng mục hiện tại; '
        'tiến độ hạng mục và giải pháp tính lại theo trọng số.', tacnhan=A_LD,
        dieukien='Đang ở màn Quản lý hạng mục. Chỉ Leader nhập được; người khác chỉ xem.',
        chinh='1. Bấm tab “Tiến độ”.\n2. Hệ thống liệt kê nhiệm vụ (trừ Nháp) của version hạng mục hiện tại.\n3. Leader nhập % ở cột '
              'Phân bổ.\n4. Sau 1 giây ngừng gõ hệ thống tự lưu, hiện “Đã lưu”.',
        phu='• Tổng > 100 → “Tổng trọng số không được vượt quá 100%”, không lưu.\n• Lỗi → “Lỗi khi lưu”.\n'
            '• Ô ngoài 0–100 → viền đỏ.'),
   [('menu', MQL + ' => Tiến độ'), ('img', '21-tab-tien-do.png', 'Tab Tiến độ (người dùng là Leader)')],
   [('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- “Tìm theo mã, tên nhiệm vụ”'),
    ('Ô lọc Người thực hiện', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống', '- Nguồn: nhân sự của hạng mục'),
    ('Ô lọc Ngày giao', 'Datepicker', 'Enable', 'dd/mm/yyyy', 'Không', 'Trống', '- Máy chủ lọc theo HẠN hoàn thành của nhiệm vụ'),
    ('Ô lọc Trạng thái', 'Dropdown', 'Enable', 'Danh sách 5 giá trị', 'Không', 'Trống', '- Bảng 3.4'),
    ('Nhãn Đã phân bổ / Chưa phân bổ', 'Text', 'Hiển thị', '0–100', '–', 'Theo dữ liệu', '- Tổng % và phần còn lại'),
    ('Bảng phân bổ', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Cột: STT, Mã nhiệm vụ, Tên công việc, Người thực hiện, '
     'Version, Phân bổ (%), Tiến độ TT (%) (thanh tiến độ), Trạng thái'),
    ('Ô Phân bổ (%)', 'Number', 'Enable / Read-only', '0 – 100', 'Không', 'Theo dữ liệu', '- Leader: ô nhập; người khác: “n%”'),
    ('Dòng “Thay đổi được lưu tự động”', 'Text', 'Hiển thị', '–', '–', 'Hiển thị', '- Chỉ với Leader')],
   [('Bấm tab', 'Click', 'After:\n– Nạp danh sách và nhân sự cho ô lọc.'),
    ('Nhập % phân bổ', 'Change', 'Before:\n– Chỉ Leader, nếu không → “Bạn không có quyền cập nhật trọng số”.\nDuring:\n– Tổng > 100 '
     '→ “Tổng trọng số không được vượt quá 100%”.\nAfter:\n– Lưu trọng số; tính lại tiến độ hạng mục và giải pháp; “Đã lưu”.'),
    ('Tìm / lọc / Làm mới', 'Keypress / Change', 'After:\n– Nạp lại danh sách.')],
   uc=('FR-21', 'Phân bổ % tiến độ', 'crud', A_LD), rule=('- Validate dữ liệu, Thông báo.', 'create'))

# ---------------------------------------------------------------- 2.22 FR-22
fn('Tab Files',
   dict(ten='Tab Files của hạng mục', mota='Gom mọi file đính kèm của nhiệm vụ, vấn đề, hồ sơ trình duyệt thuộc hạng mục.',
        tacnhan=A_TV, dieukien='Đang ở màn Quản lý hạng mục.',
        chinh='1. Bấm tab “Files”.\n2. Hệ thống nạp file, mới tạo trước.\n3. Người dùng xem trước, tải xuống, bấm Liên kết để mở '
              'đối tượng gốc.',
        phu='• Rỗng → “Không có file phù hợp bộ lọc.”.\n• File không có đường dẫn → “File chưa có đường dẫn tải xuống”.'),
   [('menu', MQL + ' => Files'), ('img', '22-tab-files.png', 'Tab Files')],
   [('Ô tìm nhanh', 'Textbox', 'Enable', '–', 'Không', 'Trống', '- “Tìm theo tên file, tên tài liệu, mã liên kết” (cả tên nhiệm vụ '
     '/ vấn đề, nhóm tài liệu)'),
    ('Ô lọc Nguồn / Nhóm tài liệu / Version / Người tạo', 'Dropdown', 'Enable', 'Danh sách', 'Không', 'Trống',
     ['- Nguồn: bảng 3.4; Nhóm tài liệu: danh mục loại tài liệu', '- Version: lấy từ các dòng đang hiển thị',
      '- Người tạo: nhân viên đang làm việc']),
    ('Bảng file', 'Table/Grid', 'Read-only', '–', '–', 'Theo dữ liệu', '- Cột: STT, Tên tài liệu, File, Nguồn (nhãn màu), Nhóm tài '
     'liệu, Version, Liên kết, Người tạo, Ngày tạo, Dung lượng, Thao tác; không cột nào sắp xếp được'),
    ('Cột Liên kết', 'Link', 'Enable', '–', '–', 'Theo dữ liệu', '- Bấm → mở chi tiết nhiệm vụ / vấn đề (ẩn nút thao tác) hoặc cửa '
     'sổ xem hồ sơ trình duyệt'),
    ('Nút Xem trước / Tải xuống', 'Icon Button', 'Enable / Ẩn', '–', '–', 'Hiển thị', '- Xem trước chỉ với định dạng xem được'),
    ('Phân trang', 'Pagination', 'Enable', '10/20/50…', '–', '10', '–')],
   [('Bấm tab', 'Click', 'After:\n– Nạp danh sách; lỗi → “Lỗi khi tải dữ liệu file”.'),
    ('Bấm Liên kết', 'Click', 'After:\n– Mở đối tượng gốc ở dạng chỉ xem.'),
    ('Bấm Xem trước / Tải xuống', 'Click', 'After:\n– Mở cửa sổ xem file / tải file.')] + ev_page(),
   rule=('- Màn Danh sách, Phân trang.', 'list'), ui_kind='input')

# ---------------------------------------------------------------- 2.23 FR-23
fn('Tạo version hạng mục',
   dict(ten='Tạo version hạng mục', mota='Mở phiên bản mới để làm lại hạng mục sau khi hồ sơ đã được duyệt.', tacnhan=A_TV,
        dieukien='Hạng mục Đã duyệt hồ sơ trình duyệt.',
        chinh='1. Bấm “Tạo version” ở thanh đầu.\n2. Cửa sổ “Tạo phiên bản hạng mục mới” mở, Mã phiên bản điền sẵn V(n+1).\n'
              '3. Nhập Mô tả (tuỳ chọn), chọn Ngày kết thúc.\n4. Bấm “Tạo mới”.\n5. Hệ thống tạo version, hạng mục về Đang triển '
              'khai, “Tạo phiên bản hạng mục mới thành công”.',
        phu='• Không hỏi xác nhận trước khi tạo.\n• Hạng mục không còn Đã duyệt hồ sơ → “Chỉ có thể tạo phiên bản mới khi hạng mục ở '
            'trạng thái Đã duyệt hồ sơ trình duyệt!”.'),
   [('menu', MQL + ' => Tạo version'), ('modal', 'Tạo phiên bản hạng mục mới'), ('img', '12-tao-version.png', 'Cửa sổ Tạo phiên bản hạng mục mới')],
   [('Mã phiên bản', 'Textbox', 'Read-only', '–', '–', 'V(n+1)', '- n = số version hiện tại'),
    ('Mô tả', 'Textarea', 'Enable', '–', 'Không', 'Trống', '- “Mô tả phiên bản (tuỳ chọn)”'),
    ('Ngày kết thúc', 'Datepicker', 'Enable', 'dd/mm/yyyy, ≥ hôm nay', 'Có', 'Trống', '- Nhãn chưa có dấu * nhưng máy chủ bắt buộc'),
    ('Nút Tạo mới / Đóng / ×', 'Button', 'Enable', '–', '–', 'Hiển thị', '–')],
   [('Bấm Tạo mới', 'Click', 'Before:\n– Hạng mục Đã duyệt hồ sơ trình duyệt.\nDuring:\n– Ngày kết thúc trống → “Bắt buộc phải '
     'nhập”; trước hôm nay → “Ngày kết thúc phải lớn hơn hoặc bằng ngày hiện tại”; toast “Vui lòng kiểm tra lại thông tin”.\n'
     'After:\n– Hồ sơ Đã duyệt của hạng mục → Hết hiệu lực.\n– Lưu trọng số, tiến độ của version cũ; tiến độ hạng mục về 0%.\n– '
     'Tạo version mới gắn version hiện tại của giải pháp, ngày bắt đầu = hôm nay.\n– Hạng mục → Đang triển khai.\n– “Tạo phiên '
     'bản hạng mục mới thành công”, nạp lại màn.'), ev_close()],
   uc=('FR-23', 'Tạo version hạng mục', 'action', A_TV), rule=('- Màn Thêm mới, Validate dữ liệu, Thông báo.', 'create'))

# ======================================================================= PHẦN 4
d.h1('Phần 4. Quy tắc nghiệp vụ')
d.rule_ref('- chỉ liệt kê quy tắc đặc thù của Hạng mục giải pháp.', anchor='list', head='Quy tắc áp dụng',
           lead='Ngoài SRS Các quy tắc chung ')
d.rule_table([
    ('BR-01', 'Phạm vi danh sách', ['– Theo quyền V1–V4 (Phần 2); không quyền: hạng mục mình tạo, mình là Leader / thành viên, '
     'hoặc là PM của yêu cầu làm giải pháp.', '– Chỉ hạng mục của giải pháp từ Chờ Leader duyệt trở đi hoặc Đóng.'],
     ['Xem danh sách', 'Xuất Excel']),
    ('BR-02', 'Hạng mục mới luôn Chưa duyệt', ['– Mọi hạng mục mới lưu ở trạng thái Chưa duyệt, tạo kèm version V1 gắn version '
     'hiện tại của giải pháp.'], ['Khai hạng mục']),
    ('BR-03', 'Khoá hạng mục trên form', ['– Chờ Leader duyệt: hạng mục cũ chỉ Leader của nó sửa (không đổi Tên, Leader).',
     '– Từ Đang triển khai: hạng mục đã lưu bị khoá, chỉ sửa / xoá hạng mục vừa thêm.'], ['Khai hạng mục']),
    ('BR-04', 'Leader duyệt theo người', ['– “Lưu và duyệt” duyệt mọi hạng mục người đó làm Leader trong giải pháp.',
     '– Mọi hạng mục đã duyệt → giải pháp tự sang Đang triển khai.'], ['Leader duyệt hạng mục']),
    ('BR-05', 'Điều kiện trình hồ sơ', ['– Hạng mục Đang triển khai.', '– Có BOM tổng hợp Hoàn thành của version hạng mục hiện tại; '
     'dự án Tự triển khai thì không cần BOM nhưng phải có ít nhất 1 tài liệu.'], ['Tạo / trình hồ sơ']),
    ('BR-06', '1 hồ sơ Nháp / hạng mục', ['– Lưu hồ sơ luôn ghi đè hồ sơ Nháp gần nhất; không có Nháp thì tạo hồ sơ mới mã '
     'HS.TD.<Mã HM>.<nnn>.'], ['Tạo / trình hồ sơ']),
    ('BR-07', 'Người duyệt hồ sơ', ['– PM của giải pháp hoặc PM ghi trên hồ sơ; chỉ hồ sơ Chờ duyệt.', '– Từ chối bắt buộc lý do ≤ '
     '1000 ký tự.'], ['Duyệt / từ chối hồ sơ']),
    ('BR-08', 'Tạo version', ['– Chỉ khi hạng mục Đã duyệt hồ sơ trình duyệt; hồ sơ Đã duyệt → Hết hiệu lực; tiến độ về 0%; hạng mục '
     '→ Đang triển khai.'], ['Tạo version']),
    ('BR-09', 'Đóng dự án', ['– Đóng dự án TKT → mọi hạng mục chưa Đóng chuyển Đóng; màn Quản lý ẩn nút Tạo mới / Sửa / Xoá / Thêm '
     'nhân sự.'], ['Mọi chức năng']),
    ('BR-10', 'Trọng số tiến độ', ['– Chỉ Leader nhập; tổng trọng số nhiệm vụ ≤ 100%; lưu xong tính lại tiến độ hạng mục và giải pháp.'],
     ['Tab Tiến độ']),
    ('BR-11', 'Thông báo', ['– Chỉ “Giao cho Leader” gửi thông báo cho các Leader (TB-01); luồng hồ sơ, version, nhân sự không gửi.'],
     ['Mọi chức năng']),
])

d.save()
